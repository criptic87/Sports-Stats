"""GET /api/sports — list all supported sports."""

from fastapi import APIRouter

from models import SportOut

router = APIRouter(prefix="/api")

# Static for now — will come from DB in Phase 2
SPORTS = [
    SportOut(slug="basketball", name="Basketball"),
    SportOut(slug="football", name="American Football"),
    SportOut(slug="soccer", name="Football (Soccer)"),
]


@router.get("/sports", response_model=list[SportOut])
async def list_sports():
    return SPORTS
