"""GET /api/stats/{league_slug}/{category} — leaderboard for a category."""

from fastapi import APIRouter, HTTPException

from cache import cache
from models import CategoryLeaders, LeaderEntry
from services.espn import NBA_CATEGORIES, fetch_nba_leaders

router = APIRouter(prefix="/api")

CACHE_KEY = "nba_leaders"


async def _get_nba_data() -> dict:
    """Return cached NBA data or fetch fresh."""
    data = cache.get(CACHE_KEY)
    if data is not None:
        return data
    data = await fetch_nba_leaders()
    cache.set(CACHE_KEY, data, ttl=3600)
    return data


@router.get("/stats/{league_slug}/{category}", response_model=CategoryLeaders)
async def get_leaders(league_slug: str, category: str):
    if league_slug != "nba":
        raise HTTPException(404, f"League '{league_slug}' not yet supported")

    if category not in NBA_CATEGORIES:
        valid = ", ".join(NBA_CATEGORIES.keys())
        raise HTTPException(400, f"Invalid category. Valid: {valid}")

    data = await _get_nba_data()
    leaders: list[LeaderEntry] = data["categories"].get(category, [])

    return CategoryLeaders(
        league="NBA",
        season=data["season"],
        category=category,
        updated_at=data["date"],
        leaders=leaders,
    )


@router.get("/stats/{league_slug}")
async def get_all_categories(league_slug: str):
    """Return all categories at once (used by the frontend)."""
    if league_slug != "nba":
        raise HTTPException(404, f"League '{league_slug}' not yet supported")

    data = await _get_nba_data()

    result = {}
    for cat_slug in NBA_CATEGORIES:
        leaders = data["categories"].get(cat_slug, [])
        result[cat_slug] = CategoryLeaders(
            league="NBA",
            season=data["season"],
            category=cat_slug,
            updated_at=data["date"],
            leaders=[l.model_dump() for l in leaders] if leaders and isinstance(leaders[0], LeaderEntry) else leaders,
        )

    return {
        "league": "NBA",
        "season": data["season"],
        "date": data["date"],
        "days_back": data["days_back"],
        "categories": {
            k: v.model_dump() for k, v in result.items()
        },
    }
