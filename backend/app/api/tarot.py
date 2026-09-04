import json
from fastapi import APIRouter
from app.schemas.models import DrawRequest
from app.services.tarot_service import TarotService
from app.services.prolog_service import PrologService
from app.database import get_db

router = APIRouter(prefix="/api/tarot", tags=["tarot"])


@router.get("")
async def get_all_tarot_cards():
    return await TarotService.get_all_cards()


@router.get("/{card}")
async def get_tarot_card(card: str):
    info = await TarotService.get_card_info(card)
    if info:
        return info
    return {"error": "Card not found"}


@router.post("/draw")
async def draw_cards(request: DrawRequest):
    positions = TarotService.get_spread_positions(
        request.spread_type or "three_card"
    )
    if request.count:
        positions = positions[: request.count]

    cards = await TarotService.draw_cards_with_positions(positions)
    return {
        "cards": cards,
        "spread_type": request.spread_type or "three_card",
        "positions": positions,
    }
