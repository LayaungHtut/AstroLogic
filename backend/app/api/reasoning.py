from fastapi import APIRouter
from app.services.prolog_service import PrologService
from app.services.openrouter_service import generate_tarot_interpretation
from app.services.tarot_service import TarotService
from app.schemas.models import ReadingAnalyzeRequest
from app.database import get_db
import asyncio
import json

router = APIRouter(prefix="/api/reading", tags=["reading"])


def _classify_and_recommend(question: str, sign: str, requested_spread_type: str | None) -> dict:
    """Bundle of synchronous Prolog calls needed before cards are drawn.

    If the caller (the UI's spread picker) asked for a specific spread type,
    honor it instead of letting Prolog auto-recommend one from the question
    text — recommend_spread/2 always overrode any client-chosen spread_type
    before this, so picking a spread in the UI silently did nothing.
    """
    category = PrologService.classify_question(question)
    topic = PrologService.classify_topic(question)
    topic_info = PrologService.get_topic_info(topic)
    spread_rec = None
    if requested_spread_type:
        spread_rec = PrologService.recommend_spread_for(question, sign, requested_spread_type)
    if not spread_rec:
        spread_rec = PrologService.recommend_spread(question, sign)
    return {
        "category": category,
        "topic": topic,
        "topic_info": topic_info,
        "spread_rec": spread_rec,
    }


def _analyze_drawn_cards(
    question: str,
    sign: str,
    category: str,
    prolog_cards: list[str],
    positions: list[str],
    orientations: list[str],
) -> dict:
    """Bundle of synchronous Prolog calls needed once cards are drawn.

    Everything here reasons over specific cards, so it depends on
    TarotService.to_prolog_card_atom having already converted the drawn
    cards' display names into the snake_case atoms the rule base expects
    (e.g. "the_hanged_man") — the short display codes ("01", "w01") used
    for images never match any Prolog card fact.
    """
    prolog_analysis = PrologService.interpret_cards(prolog_cards, sign, category)
    themes = prolog_analysis["themes"] if prolog_analysis else []
    dominant_theme = PrologService.get_dominant_theme(prolog_cards) if prolog_cards else None

    reasoning = PrologService.generate_reading_trace(question, sign)
    facts = PrologService.get_relevant_facts(sign, category)

    # Feature: Reading Direction & Advice Engine
    oriented = PrologService.analyze_reading(prolog_cards, positions, orientations)
    direction = oriented["direction"] if oriented else "balanced"
    advice = {
        "category_advice": PrologService.get_reading_advice(category, sign),
        "theme_advice": PrologService.get_theme_based_advice(dominant_theme) if dominant_theme else "",
    }

    # Feature: Zodiac x Tarot Affinity — per-card affinity to the user's sign
    affinities = {
        card: PrologService.get_zodiac_tarot_theme(sign, card) for card in set(prolog_cards)
    }

    # Feature: Theme Conflict Detector
    conflicts = PrologService.get_reading_card_conflicts(prolog_cards)

    # Feature: Card Rank & Priority — where each drawn card sits among all
    # Prolog-eligible cards for this context (not how it was selected, since
    # the actual draw is random — this shows relative resonance after the fact).
    ranked_pool = PrologService.get_ranked_eligible_cards(category, sign)
    ranked_by_card = {r["card"]: r for r in ranked_pool}

    return {
        "themes": themes,
        "dominant_theme": dominant_theme,
        "reasoning": reasoning,
        "facts": facts,
        "direction": direction,
        "advice": advice,
        "affinities": affinities,
        "conflicts": conflicts,
        "ranked_by_card": ranked_by_card,
        "eligible_pool_size": len(ranked_pool),
    }


@router.post("/analyze")
async def analyze_reading(request: ReadingAnalyzeRequest):
    # PrologService calls are synchronous, blocking pyswip queries — run each
    # bundle off the event loop so slow queries don't stall every other request.
    pre = await asyncio.to_thread(
        _classify_and_recommend, request.question, request.zodiac_sign, request.spread_type
    )
    category = pre["category"]
    spread_rec = pre["spread_rec"]

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

    prolog_cards = [c["prolog_card"] for c in cards]
    prolog_positions = [TarotService.to_prolog_position_atom(p) for p in positions]
    orientations = ["reversed" if c["is_reversed"] else "upright" for c in cards]

    post = await asyncio.to_thread(
        _analyze_drawn_cards,
        request.question, request.zodiac_sign, category,
        prolog_cards, prolog_positions, orientations,
    )
    themes = post["themes"]
    facts = post["facts"]

    # Attach per-card zodiac affinity and ranking onto each card in the response.
    for i, card in enumerate(cards):
        p_card = prolog_cards[i]
        card["zodiac_affinity"] = post["affinities"].get(p_card)
        rank_info = post["ranked_by_card"].get(p_card)
        card["ranking"] = (
            {
                "rank": rank_info["rank"],
                "eligible_pool_size": post["eligible_pool_size"],
                "priority": rank_info["priority"],
                "zodiac_affinity_match": rank_info["zodiac_affinity_match"],
                "category_match": rank_info["category_match"],
                "element_match": rank_info["element_match"],
            }
            if rank_info
            else None
        )

    # Resolve the theme-conflict card indices/atoms back to display names and
    # spread positions so the UI can say "Card 1 (Past)" rather than an atom.
    conflicts = [
        {
            "card1_position": positions[c["card1_index"]] if c["card1_index"] < len(positions) else None,
            "card1_name": cards[c["card1_index"]]["name"] if c["card1_index"] < len(cards) else c["card1"],
            "theme1": c["theme1"],
            "card2_position": positions[c["card2_index"]] if c["card2_index"] < len(positions) else None,
            "card2_name": cards[c["card2_index"]]["name"] if c["card2_index"] < len(cards) else c["card2"],
            "theme2": c["theme2"],
            "title": c["title"],
            "description": c["description"],
        }
        for c in post["conflicts"]
    ]

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

    if request.spread_type:
        spread_rationale = (
            f"Your question was classified as '{category}' (topic: '{pre['topic']}'). "
            f"You chose the {spread_rec['name']} spread, which emphasizes "
            f"{spread_rec.get('emphasis', 'this area of focus')}."
        )
    else:
        spread_rationale = (
            f"Your question was classified as '{category}' (topic: '{pre['topic']}'), "
            f"which is why the {spread_rec['name']} spread was recommended — it emphasizes "
            f"{spread_rec.get('emphasis', 'this area of focus')}."
        )

    return {
        "question": request.question,
        "category": category,
        "topic": pre["topic"],
        "topic_info": pre["topic_info"],
        "spread_rationale": spread_rationale,
        "zodiac_sign": request.zodiac_sign,
        "spread_type": spread_rec["spread_type"],
        "spread_name": spread_rec["name"],
        "cards": cards,
        "themes": themes,
        "dominant_theme": post["dominant_theme"],
        "direction": post["direction"],
        "advice": post["advice"],
        "conflicts": conflicts,
        "reasoning": post["reasoning"],
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
