from fastapi import APIRouter
from app.services.prolog_service import PrologService
from app.services.openrouter_service import generate_tarot_interpretation
from app.services.tarot_service import TarotService
from app.schemas.models import ReadingAnalyzeRequest, ReadingAnalyzeManualRequest
import asyncio
import json
import re

router = APIRouter(prefix="/api/reading", tags=["reading"])


def _classify_and_recommend(
    question: str, sign: str, requested_spread_type: str | None, card_count: int | None
) -> dict:
    sign = (sign or "cancer").lower().strip()
    req_spread = requested_spread_type.lower().strip() if requested_spread_type else None
    category = PrologService.classify_question(question)
    topic = PrologService.classify_topic(question)
    topic_info = PrologService.get_topic_info(topic)
    spread_rec = None
    if req_spread == "custom":
        count = card_count if card_count and 1 <= card_count <= 10 else 3
        spread_rec = PrologService.recommend_custom_spread(question, sign, count)
    elif req_spread:
        spread_rec = PrologService.recommend_spread_for(question, sign, req_spread)
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


async def _finish_reading(
    question: str,
    zodiac_sign: str,
    category: str,
    topic: str,
    topic_info: dict | None,
    spread_rec: dict,
    cards: list[dict],
    spread_rationale: str,
    locale: str = "en",
) -> dict:
    """Everything from a drawn/selected set of cards to the finished reading
    response: Prolog analysis, per-card affinity/ranking, conflict
    resolution, and the AI interpretation. Shared by the random-draw and
    manual-selection endpoints — they differ only in how `cards` and
    `spread_rec` were produced, not in how a reading is built from them."""
    positions = spread_rec["positions"]
    prolog_cards = [c["prolog_card"] for c in cards]
    prolog_positions = [TarotService.to_prolog_position_atom(p) for p in positions]
    orientations = ["reversed" if c["is_reversed"] else "upright" for c in cards]

    post = await asyncio.to_thread(
        _analyze_drawn_cards,
        question, zodiac_sign, category,
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

    is_burmese = bool(re.search(r"[\u1000-\u109F]", question))
    effective_locale = "my" if (locale == "my" or is_burmese) else "en"

    ai_interpretation = await generate_tarot_interpretation(
        question=question,
        zodiac_sign=zodiac_sign,
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
        topic=topic,
        locale=effective_locale,
    )

    if not ai_interpretation:
        ai_interpretation = _fallback_interpretation(cards, themes, category, zodiac_sign, question=question, locale=effective_locale)

    return {
        "question": question,
        "category": category,
        "topic": topic,
        "topic_info": topic_info,
        "spread_rationale": spread_rationale,
        "zodiac_sign": zodiac_sign,
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


@router.post("/analyze")
async def analyze_reading(request: ReadingAnalyzeRequest):
    # PrologService calls are synchronous, blocking pyswip queries — run each
    # bundle off the event loop so slow queries don't stall every other request.
    pre = await asyncio.to_thread(
        _classify_and_recommend,
        request.question, request.zodiac_sign, request.spread_type, request.card_count,
    )
    category = pre["category"]
    spread_rec = pre["spread_rec"]

    if not spread_rec:
        fixed_spreads = {
            "one_card": {
                "category": category,
                "spread_type": "one_card",
                "name": "One Card",
                "description": "Simple guidance or daily insight",
                "card_count": 1,
                "positions": ["Guidance"],
                "element": "water",
                "modality": "cardinal",
                "emphasis": "Emotions & Intuition",
            },
            "three_card": {
                "category": category,
                "spread_type": "three_card",
                "name": "Three Card",
                "description": "Past, Present, Future",
                "card_count": 3,
                "positions": ["Past", "Present", "Future"],
                "element": "water",
                "modality": "cardinal",
                "emphasis": "Emotions & Intuition",
            },
            "decision": {
                "category": category,
                "spread_type": "decision",
                "name": "Decision Spread",
                "description": "Current Situation, Path A, Path B, Advice",
                "card_count": 4,
                "positions": ["Current Situation", "Path A", "Path B", "Advice"],
                "element": "water",
                "modality": "cardinal",
                "emphasis": "Emotions & Intuition",
            },
            "self_reflection": {
                "category": category,
                "spread_type": "self_reflection",
                "name": "Self Reflection",
                "description": "Current Self, Hidden Influence, What to Understand, Guidance",
                "card_count": 4,
                "positions": ["Current Self", "Hidden Influence", "What to Understand", "Guidance"],
                "element": "water",
                "modality": "cardinal",
                "emphasis": "Emotions & Intuition",
            },
            "relationship": {
                "category": category,
                "spread_type": "relationship",
                "name": "Relationship Spread",
                "description": "You, Other Person, Connection, Challenge, Guidance",
                "card_count": 5,
                "positions": ["You", "Other Person", "Connection", "Challenge", "Guidance"],
                "element": "water",
                "modality": "cardinal",
                "emphasis": "Emotions & Intuition",
            },
            "career": {
                "category": category,
                "spread_type": "career",
                "name": "Career Spread",
                "description": "Current Position, Strength, Challenge, Opportunity, Advice",
                "card_count": 5,
                "positions": ["Current Position", "Strength", "Challenge", "Opportunity", "Advice"],
                "element": "water",
                "modality": "cardinal",
                "emphasis": "Emotions & Intuition",
            },
        }
        spread_key = (request.spread_type or "").lower().strip()
        spread_rec = fixed_spreads.get(spread_key, fixed_spreads["three_card"])

    cards = await TarotService.draw_cards_with_positions(
        spread_rec["positions"], request.zodiac_sign, category
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

    return await _finish_reading(
        request.question, request.zodiac_sign, category, pre["topic"], pre["topic_info"],
        spread_rec, cards, spread_rationale,
        locale=request.locale or "en",
    )


@router.post("/analyze-selected")
async def analyze_selected_reading(request: ReadingAnalyzeManualRequest):
    """Like /analyze, but the seeker hand-picked the cards (and optionally
    their orientation) from the deck instead of having them drawn at
    random. The reading — themes, direction, advice, conflicts, the full
    Prolog reasoning trace, and the AI interpretation — is generated from
    exactly those cards, in the order they were picked."""
    names = [c.name for c in request.cards]
    if len(set(n.strip().lower() for n in names)) != len(names):
        return {"error": "Each card can only be selected once per reading."}

    category = await asyncio.to_thread(PrologService.classify_question, request.question)
    topic = await asyncio.to_thread(PrologService.classify_topic, request.question)
    topic_info = await asyncio.to_thread(PrologService.get_topic_info, topic)
    spread_rec = await asyncio.to_thread(
        PrologService.recommend_custom_spread, request.question, request.zodiac_sign, len(request.cards)
    )
    if not spread_rec:
        return {"error": "Could not build a reading from the selected cards."}
    # It's the seeker's own selection, not an open random draw — relabel the
    # generic custom-spread name/description to say so.
    spread_rec = {
        **spread_rec,
        "name": "Your Selection",
        "description": "Cards you hand-picked from the deck, read in the order you chose them.",
    }

    cards = await TarotService.build_cards_from_selection(
        [(c.name, c.is_reversed) for c in request.cards], spread_rec["positions"]
    )
    if cards is None:
        return {"error": "One or more selected cards weren't recognized."}

    spread_rationale = (
        f"Your question was classified as '{category}' (topic: '{topic}'). "
        f"You hand-picked {len(cards)} card{'s' if len(cards) != 1 else ''} from the deck, "
        f"read in the order you chose them."
    )

    return await _finish_reading(
        request.question, request.zodiac_sign, category, topic, topic_info,
        spread_rec, cards, spread_rationale,
        locale=request.locale or "en",
    )


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
    cards: list[dict],
    themes: list[str],
    category: str,
    zodiac: str,
    question: str = "",
    locale: str = "en",
) -> str:
    card_names = [c["name"] for c in cards]
    cards_text = ", ".join(card_names)
    themes_text = ", ".join(themes) if themes else "reflection and balance"

    is_burmese = (locale == "my") or bool(re.search(r"[\u1000-\u109F]", question))
    if is_burmese:
        category_map = {
            "education": "ပညာရေးနှင့် စာမေးပွဲ",
            "career": "အလုပ်အကိုင်နှင့် စီးပွားရေး",
            "love": "အချစ်ရေးနှင့် သံယောဇဉ်",
            "relationship": "အချစ်ရေးနှင့် ဆက်ဆံရေး",
            "spiritual": "စိတ်ပိုင်းဆိုင်ရာနှင့် လမ်းပြမှု",
            "finance": "ငွေကြေးနှင့် ဓနဥစ္စာ",
            "health": "ကျန်းမာရေးနှင့် ညီညွတ်မျှတမှု",
            "decision": "လမ်းခွဲရွေးချယ်မှု",
            "friendship": "မိတ်ဆွေနှင့် သံယောဇဉ်",
            "creativity": "တီထွင်ဖန်တီးမှုနှင့် အနုပညာ",
            "future_planning": "အနာဂတ်အစီအစဉ်",
            "self_reflection": "မိမိကိုယ်ကိုဆန်းစစ်ခြင်း",
            "general": "အထွေထွေ ဘဝခရီးလမ်း",
        }
        category_my = category_map.get(category, "ဘဝကဏ္ဍ")
        q_text = f"သင်၏ မေးခွန်းဖြစ်သော '{question}' နှင့် စပ်လျဉ်း၍ " if question else ""

        cards_lines = []
        for i, c in enumerate(cards):
            orient = " (ပြောင်းပြန်)" if c.get("is_reversed") else " (မူမှန်)"
            pos = c.get("position", f"ကတ် {i + 1}")
            cards_lines.append(f"* **{c['name']}**{orient} - တည်နေရာ: {pos}")
        cards_section = "\n".join(cards_lines)

        zodiac_clean = (zodiac or "").lower().strip()
        zodiac_guidance_map = {
            "aries": "မိဿရာသီဖွား (မီးဓာတ်) အနေဖြင့် သင်၏ ပင်ကိုရဲရင့်ပြတ်သားမှုနှင့် ရှေ့ဆောင်ဦးဆောင်လိုစိတ်ကို အပြုသဘောဆောင် အသုံးချပါ။ အလျင်စလို ဆုံးဖြတ်ခြင်းကို ရှောင်ရှားပြီး ရေရှည်မျှော်တွေးကာ အဆင့်ဆင့် လျှောက်လှမ်းပါ။",
            "taurus": "ပြိဿရာသီဖွား (မြေဓာတ်) အနေဖြင့် သင်၏ စိတ်ရှည်သည်းခံမှု၊ တည်ငြိမ်ခိုင်မာမှုနှင့် လက်တွေ့ကျသော အခြေခံများကို အားပြုပါ။ စိတ်လောကြီးခြင်းမရှိဘဲ ဖြည်းဖြည်းနှင့်မှန်မှန် ခိုင်မာစွာ တည်ဆောက်သွားပါ။",
            "gemini": "မေထုန်ရာသီဖွား (လေဓာတ်) အနေဖြင့် သင်၏ ထက်မြက်သော ဉာဏ်ပညာ၊ စူးစမ်းရှာဖွေလိုစိတ်နှင့် ပွင့်လင်းစွာ ပြောဆိုဆက်ဆံနိုင်စွမ်းကို အသုံးချပါ။ စိတ်ဒွိဟဖြစ်မှုများကို ရှင်းလင်းပြတ်သားသော သတင်းအချက်အလက်များဖြင့် ဖြေရှင်းပါ။",
            "cancer": "ကရကဋ်ရာသီဖွား (ရေဓာတ်) အနေဖြင့် သင်၏ နက်ရှိုင်းသော အလိုလိုသိစိတ်၊ နွေးထွေးသော စာနာနားလည်မှုနှင့် အတွင်းစိတ်ခွန်အားကို အပြည့်အဝ ယုံကြည်ပါ။ စိတ်ခံစားချက်များကို လုံခြုံစွာ ထိန်းသိမ်းပြီး အဆင်သင့်ဖြစ်ချိန်တွင် သဘာဝကျကျ ရှေ့ဆက်ပါ။",
            "leo": "သိဟ်ရာသီဖွား (မီးဓာတ်) အနေဖြင့် သင်၏ မွန်မြတ်သော စေတနာ၊ နှလုံးသားခွန်အားနှင့် မိမိကိုယ်ကို ယုံကြည်မှုကို မဏ္ဍိုင်ပြုပါ။ မာနထက် နားလည်မှုကို ဦးစားပေးပြီး သင်၏ တောက်ပသော စွမ်းအင်ဖြင့် အောင်မြင်မှုကို အရယူပါ။",
            "virgo": "ကန်ရာသီဖွား (မြေဓာတ်) အနေဖြင့် သင်၏ စေ့စပ်သေချာမှု၊ စနစ်တကျ ပြင်ဆင်နိုင်မှုနှင့် လက်တွေ့ကျကျ ဆန်းစစ်နိုင်စွမ်းကို အားပြုပါ။ အသေးစိတ်အချက်အလက်များကို အလေးထားသော်လည်း အရာရာ ပြီးပြည့်စုံလွန်းရမည်ဟူသော စိုးရိမ်စိတ်ကို လျှော့ချပါ။",
            "libra": "တူရာသီဖွား (လေဓာတ်) အနေဖြင့် သင်၏ မျှတစွာ ချိန်ဆနိုင်မှု၊ သဟဇာတဖြစ်လိုစိတ်နှင့် လိမ္မာပါးနပ်သော သံတမန်ဆက်ဆံရေးကို အသုံးချပါ။ လမ်းကြောင်းနှစ်ခုကြား ဝေခွဲမရဖြစ်မနေဘဲ မိမိ၏ အတွင်းစိတ်အမှန်တရားအတိုင်း သတ္တိရှိရှိ ရွေးချယ်ပါ။",
            "scorpio": "ဗြိစ္ဆာရာသီဖွား (ရေဓာတ်) အနေဖြင့် သင်၏ စူးရှထက်မြက်သော ထိုးထွင်းအမြင်၊ စိတ်ပိုင်းဖြတ်မှုနှင့် ဘဝကို အသွင်ပြောင်းလဲနိုင်သော စွမ်းအားကို ယုံကြည်ပါ။ အတိတ်ဟောင်းများကို လက်လွှတ်စွန့်လွှတ်ပြီး အသစ်တဖန် ပြန်လည်မွေးဖွားသည့်သဖွယ် အားသစ်မွေးပါ။",
            "sagittarius": "ဓနုရာသီဖွား (မီးဓာတ်) အနေဖြင့် သင်၏ အကောင်းမြင်စိတ်၊ အမြင်ကျယ်မှုနှင့် အမှန်တရားရှာဖွေလိုစိတ်ကို အားဖြည့်ပါ။ ပန်းတိုင်ကို ရှင်းလင်းစွာ မြင်ယောင်ပြီး စိတ်အားထက်သန်စွာဖြင့် ဇွဲမလျှော့ဘဲ ဆက်လက်လျှောက်လှမ်းပါ။",
            "capricorn": "မကာရရာသီဖွား (မြေဓာတ်) အနေဖြင့် သင်၏ စည်းကမ်းခိုင်မာမှု၊ မဆုတ်မနစ်သော ဇွဲလုံ့လနှင့် ရေရှည်ရည်မှန်းချက်ကြီးမားမှုကို အခြေပြုပါ။ အချိန်ယူတည်ဆောက်ရသောအရာများသည် ခိုင်ခံ့မြဲမြံစမြဲဖြစ်ကြောင်း သတိပြုကာ စိတ်ရှည်စွာ ရှေ့ဆက်ပါ။",
            "aquarius": "ကုမ်ရာသီဖွား (လေဓာတ်) အနေဖြင့် သင်၏ ထူးခြားဆန်းသစ်သော အတွေးအခေါ်၊ လွတ်လပ်မှုနှင့် ရှေ့ပြေးအမြင်များကို လက်ကိုင်ထားပါ။ သမားရိုးကျ ဘောင်များမှ ခွဲထွက်ပြီး သင့်ကိုယ်ပိုင် နည်းလမ်းသစ်ဖြင့် ဖန်တီးတီထွင်ပါ။",
            "pisces": "မိန်ရာသီဖွား (ရေဓာတ်) အနေဖြင့် သင်၏ နူးညံ့သိမ်မွေ့သော မေတ္တာ၊ အလိုလိုသိမြင်နိုင်သော စိတ်ဝိညာဉ်စွမ်းအားနှင့် အနုပညာဆန်သော စိတ်ကူးဉာဏ်ကို အသုံးချပါ။ စိတ်ကူးယဉ်မှုနှင့် လက်တွေ့ဘဝကို ဟန်ချက်ညီစေပြီး မိမိ၏ နှလုံးသားအသံကို နားထောင်ပါ။",
        }
        zodiac_advice = zodiac_guidance_map.get(
            zodiac_clean,
            "သင်၏ ပင်ကိုစွမ်းအင်နှင့် ဆင်ခြင်တွေးခေါ်မှုများကို သဟဇာတဖြစ်အောင် ညှိယူပါ။ ဤဟောကိန်းသည် အနာဂတ်ကို ကန့်သတ်ဟောကိန်းထုတ်ခြင်း မဟုတ်ဘဲ မိမိကိုယ်ကို ဆင်ခြင်သုံးသပ်ရန်အတွက် သင်္ကေတသဘော လမ်းညွှန်ချက်တစ်ခုသာ ဖြစ်ပါသည်။"
        )

        return (
            f"**၁။ မေးခွန်းနှင့် ပတ်သက်သော တိုက်ရိုက်ဆန်းစစ်ချက် ({category_my})**\n"
            f"{q_text}တားရော့ကတ်များအနက် {cards_text} တို့ ကျရောက်ခဲ့ပြီး {category_my}အတွက် အရေးပါသော လမ်းညွှန်ချက်များကို ပြသနေပါသည်။\n\n"
            f"ဤမေးခွန်းအတွက် ကတ်များသည် စိတ်ရှည်တည်ငြိမ်စွာ စူးစိုက်ဆင်ခြင်ရန်နှင့် လက်ရှိအခြေအနေကို ဉာဏ်ပညာဖြင့် သုံးသပ်ဆုံးဖြတ်ရန် အကြံပြုထားပါသည်။ "
            f"မိမိ၏ အရည်အချင်းနှင့် စိတ်အားထက်သန်မှုကို အပြည့်အဝ ယုံကြည်ပြီး ကြိုးစားအားထုတ်မှုဖြင့် အောင်မြင်မှုကို အရယူပါ။\n\n"
            f"---\n\n"
            f"**၂။ ကျရောက်သော ကတ်တစ်ခုချင်းစီ၏ လမ်းညွှန်ချက်**\n"
            f"{cards_section}\n\n"
            f"---\n\n"
            f"**၃။ လက်တွေ့ကျင့်သုံးရန် အကြံပြုချက်**\n"
            f"{zodiac_advice}"
        )

    return (
        f"Your reading draws {cards_text}, creating a narrative around {themes_text}. "
        f"As a {zodiac}, you bring your unique elemental energy to this reading. "
        f"The cards suggest a time for thoughtful consideration in matters of {category}. "
        f"Remember, these insights are offered as a tool for personal reflection and "
        f"self-exploration, not as definitive predictions. "
        f"Consider how these symbolic themes might resonate with your current situation "
        f"and what wisdom you can draw from them."
    )
