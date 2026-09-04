from fastapi import APIRouter
from app.services.prolog_service import PrologService
from app.services.openrouter_service import generate_tarot_interpretation
from app.services.tarot_service import TarotService
from app.schemas.models import ReadingAnalyzeRequest
from app.database import get_db
import json

router = APIRouter(prefix="/api/reading", tags=["reading"])


@router.post("/analyze")
async def analyze_reading(request: ReadingAnalyzeRequest):
    category = PrologService.classify_question(request.question)
    spread_rec = PrologService.recommend_spread(
        request.question, request.zodiac_sign
    )

    if not spread_rec:
        spread_rec = {
            "category": category,
            "spread_type": "three_card",
            "name": "Three Card",
            "description": "Past, Present, Future",
            "card_count": 3,
            "positions": ["Past", "Present", "Future"],
            "element": "fire",
            "modality": "cardinal",
            "emphasis": "Action & Initiative",
        }

    positions = spread_rec["positions"]
    cards = await TarotService.draw_cards_with_positions(
        positions, request.zodiac_sign, category
    )

    card_ids = [c["card"] for c in cards]
    prolog_analysis = PrologService.interpret_cards(
        card_ids, request.zodiac_sign, category
    )
    themes = prolog_analysis["themes"] if prolog_analysis else []

    reasoning = PrologService.generate_reading_trace(
        request.question, request.zodiac_sign
    )

    facts = PrologService.get_relevant_facts(request.zodiac_sign, category)

    ai_interpretation = await generate_tarot_interpretation(
        question=request.question,
        zodiac_sign=request.zodiac_sign,
        element=facts["element"] if facts else "fire",
        spread_name=spread_rec["name"],
        cards=[
            {
                "name": c["name"],
                "position": c["position"],
                "is_reversed": c["is_reversed"],
                "keywords": c["keywords"],
            }
            for c in cards
        ],
        themes=themes,
        category=category,
    )

    if not ai_interpretation:
        ai_interpretation = _fallback_interpretation(
            cards, themes, category, request.zodiac_sign
        )

    return {
        "question": request.question,
        "category": category,
        "zodiac_sign": request.zodiac_sign,
        "spread_type": spread_rec["spread_type"],
        "spread_name": spread_rec["name"],
        "cards": cards,
        "themes": themes,
        "reasoning": reasoning,
        "ai_interpretation": ai_interpretation,
        "facts": facts,
    }


@router.post("/generate")
async def generate_reading(data: dict):
    db = await get_db()
    try:
        await db.execute(
            """INSERT INTO reading
            (profile_id, question, category, zodiac_sign, spread_type,
             cards_json, orientations_json, themes_json, reasoning_json, ai_interpretation)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                data.get("question", ""),
                data.get("category", "general"),
                data.get("zodiac_sign", "aries"),
                data.get("spread_type", "three_card"),
                json.dumps(data.get("cards", [])),
                json.dumps(data.get("orientations", [])),
                json.dumps(data.get("themes", [])),
                json.dumps(data.get("reasoning", [])),
                data.get("ai_interpretation", ""),
            ),
        )
        await db.commit()
        cursor = await db.execute("SELECT last_insert_rowid()")
        row = await cursor.fetchone()
        return {"id": row[0], "status": "saved"}
    finally:
        await db.close()


def _fallback_interpretation(
    cards: list[dict], themes: list[str], category: str, zodiac: str
) -> str:
    card_names = [c["name"] for c in cards]
    cards_text = ", ".join(card_names)
    themes_text = ", ".join(themes) if themes else "reflection and balance"

    return (
        f"Your reading draws {cards_text}, creating a narrative around {themes_text}. "
        f"As a {zodiac}, you bring your unique elemental energy to this reading. "
        f"The cards suggest a time for thoughtful consideration in matters of {category}. "
        f"Remember, these insights are offered as a tool for personal reflection and "
        f"self-exploration, not as definitive predictions. "
        f"Consider how these symbolic themes might resonate with your current situation "
        f"and what wisdom you can draw from them."
    )
