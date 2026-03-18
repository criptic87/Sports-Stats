"""ESPN hidden-API client for NBA (and later NFL / NHL)."""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from models import CategoryLeaders, LeaderEntry

ESPN_BASE = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"

_client: httpx.AsyncClient | None = None


def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(timeout=15)
    return _client


# ── Helpers ───────────────────────────────────────────────────────────────────


def _parse_made(stat: str) -> int:
    """Parse '5-10' style stat strings, returning the made (left) value."""
    if not stat:
        return 0
    if "-" in stat:
        try:
            return int(stat.split("-")[0])
        except ValueError:
            return 0
    try:
        return int(stat)
    except ValueError:
        return 0


def _safe_int(val: str | None) -> int:
    if not val:
        return 0
    try:
        return int(val)
    except ValueError:
        return 0


def _offset_date(days_back: int) -> tuple[str, str]:
    """Return (YYYYMMDD, MM/DD/YYYY) for a date N days ago (UTC)."""
    d = datetime.now(timezone.utc) - timedelta(days=days_back)
    return d.strftime("%Y%m%d"), d.strftime("%m/%d/%Y")


# ── ESPN fetchers ─────────────────────────────────────────────────────────────


async def _fetch_scoreboard(date_str: str) -> dict | None:
    try:
        r = await _get_client().get(f"{ESPN_BASE}/scoreboard", params={"dates": date_str})
        r.raise_for_status()
        return r.json()
    except httpx.HTTPError:
        return None


async def _fetch_game_summary(game_id: str) -> dict | None:
    try:
        r = await _get_client().get(f"{ESPN_BASE}/summary", params={"event": game_id})
        r.raise_for_status()
        return r.json()
    except httpx.HTTPError:
        return None


# ── Box-score parsing ─────────────────────────────────────────────────────────


def _extract_players(summary: dict) -> list[dict[str, Any]]:
    """Pull individual player stat lines from an ESPN game summary."""
    players: list[dict[str, Any]] = []
    boxscore = summary.get("boxscore", {})

    for team_data in boxscore.get("players", []):
        team_abbr: str = team_data.get("team", {}).get("abbreviation", "")

        for stat_group in team_data.get("statistics", []):
            col_names: list[str] = stat_group.get("names", [])
            idx = {n: i for i, n in enumerate(col_names)}

            for athlete_data in stat_group.get("athletes", []):
                if athlete_data.get("didNotPlay"):
                    continue
                stats: list[str] = athlete_data.get("stats", [])
                if not stats:
                    continue

                def get(name: str) -> str:
                    i = idx.get(name)
                    if i is not None and i < len(stats):
                        return stats[i]
                    return "0"

                pts = _safe_int(get("PTS"))
                reb = _safe_int(get("REB"))
                ast = _safe_int(get("AST"))
                stl = _safe_int(get("STL"))
                blk = _safe_int(get("BLK"))
                to = _safe_int(get("TO"))
                fg3m = _parse_made(get("3PT"))
                ftm = _parse_made(get("FT"))

                # DraftKings fantasy scoring
                fantasy = (
                    pts * 1.0
                    + reb * 1.25
                    + ast * 1.5
                    + stl * 2.0
                    + blk * 2.0
                    - to * 0.5
                )
                doubles = sum(1 for v in [pts, reb, ast, stl, blk] if v >= 10)
                if doubles >= 2:
                    fantasy += 1.5
                if doubles >= 3:
                    fantasy += 3.0

                display_name = (
                    athlete_data.get("athlete", {}).get("displayName", "Unknown")
                )

                players.append(
                    {
                        "name": display_name,
                        "team": team_abbr,
                        "pts": pts,
                        "reb": reb,
                        "ast": ast,
                        "stl": stl,
                        "blk": blk,
                        "to": to,
                        "fg3m": fg3m,
                        "ftm": ftm,
                        "fantasy": round(fantasy, 1),
                    }
                )
    return players


# ── Ranking ───────────────────────────────────────────────────────────────────


def _top5(
    players: list[dict[str, Any]], key: str, ascending: bool = False
) -> list[LeaderEntry]:
    sorted_players = sorted(players, key=lambda p: p[key], reverse=not ascending)
    rows = sorted_players[:5]
    result: list[LeaderEntry] = []

    for i, p in enumerate(rows):
        if i == 0:
            rank = 1
        elif p[key] == rows[i - 1][key]:
            rank = result[i - 1].rank
        else:
            rank = i + 1

        result.append(
            LeaderEntry(
                rank=rank,
                player=p["name"],
                team=p["team"],
                stats={key: p[key]},
            )
        )
    return result


# ── Category config ───────────────────────────────────────────────────────────

NBA_CATEGORIES: dict[str, str] = {
    "points": "pts",
    "rebounds": "reb",
    "assists": "ast",
    "blocks": "blk",
    "steals": "stl",
    "turnovers": "to",
    "three_pointers": "fg3m",
    "free_throws": "ftm",
    "fantasy": "fantasy",
}


# ── Public API ────────────────────────────────────────────────────────────────


async def fetch_nba_leaders() -> dict[str, Any]:
    """Fetch top-5 NBA leaders for all categories from the most recent game day.

    Returns a dict with keys: date, days_back, season, categories.
    categories is a dict mapping category slug → list[LeaderEntry].
    """
    import asyncio

    days = [(d, *_offset_date(d)) for d in range(1, 5)]  # 1..4 days back

    # Fetch all scoreboards in parallel
    scoreboards = await asyncio.gather(
        *[_fetch_scoreboard(date_str) for _, date_str, _ in days]
    )

    for i, (days_back, date_str, display) in enumerate(days):
        sb = scoreboards[i]
        if sb is None:
            continue

        events = sb.get("events", [])
        if not events:
            continue

        # Fetch all game summaries in parallel
        summaries = await asyncio.gather(
            *[_fetch_game_summary(e["id"]) for e in events]
        )

        all_players: list[dict[str, Any]] = []
        for s in summaries:
            if s:
                all_players.extend(_extract_players(s))

        if not all_players:
            continue

        categories = {}
        for cat_slug, stat_key in NBA_CATEGORIES.items():
            categories[cat_slug] = _top5(all_players, stat_key)

        return {
            "date": display,
            "days_back": days_back,
            "season": "2024-25",
            "categories": categories,
        }

    # No games found in last 4 days
    _, _, display = days[0]
    return {
        "date": display,
        "days_back": 1,
        "season": "2024-25",
        "categories": {cat: [] for cat in NBA_CATEGORIES},
    }
