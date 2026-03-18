"""GET /api/leagues/{sport} — list leagues for a sport."""

from fastapi import APIRouter, HTTPException

from models import LeagueOut

router = APIRouter(prefix="/api")

# Static for Phase 1 — will come from DB later
LEAGUES: dict[str, list[LeagueOut]] = {
    "basketball": [
        LeagueOut(slug="nba", name="NBA", season="2024-25"),
    ],
    "football": [
        LeagueOut(slug="nfl", name="NFL", season="2025"),
    ],
    "soccer": [
        LeagueOut(slug="epl", name="Premier League", season="2024-25"),
        LeagueOut(slug="ucl", name="Champions League", season="2024-25"),
    ],
}


@router.get("/leagues/{sport}", response_model=list[LeagueOut])
async def list_leagues(sport: str):
    leagues = LEAGUES.get(sport)
    if leagues is None:
        raise HTTPException(404, f"Sport '{sport}' not found")
    return leagues
