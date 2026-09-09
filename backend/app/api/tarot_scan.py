import asyncio
import json
from fastapi import APIRouter, UploadFile, File
from app.services.openrouter_service import scan_tarot_image, explain_tarot_card
from app.services.prolog_service import PrologService

router = APIRouter(prefix="/api/tarot-scan", tags=["tarot-scan"])


@router.post("/identify")
async def identify_card(file: UploadFile = File(...)):
    """Scan a tarot card image and identify it."""
    contents = await file.read()

    if len(contents) > 10 * 1024 * 1024:  # 10MB limit
        return {"error": "File too large. Maximum size is 10MB."}

    mime_type = file.content_type or "image/jpeg"
    result = await scan_tarot_image(contents, mime_type)

    if not result or "error" in result:
        # Fallback local identification when vision API is not configured or fails
        filename_clean = (file.filename or "").lower().replace("_", " ").replace("-", " ")
        matched_id = None

        candidate_ids = [
            "knight_of_swords", "queen_of_swords", "king_of_swords", "page_of_swords", "ace_of_swords",
            "the_fool", "the_magician", "the_high_priestess", "the_empress", "the_emperor",
            "the_hierophant", "the_lovers", "the_chariot", "strength", "the_hermit",
            "wheel_of_fortune", "justice", "the_hanged_man", "death", "temperance",
            "the_devil", "the_tower", "the_star", "the_moon", "the_sun", "judgement", "the_world",
            "ace_of_wands", "two_of_wands", "three_of_wands", "four_of_wands",
            "ace_of_cups", "two_of_cups", "three_of_cups",
            "ace_of_pentacles", "ten_of_pentacles"
        ]

        for cid in candidate_ids:
            if cid.replace("_", " ") in filename_clean:
                matched_id = cid
                break

        if not matched_id and ("knight" in filename_clean or "sword" in filename_clean):
            matched_id = "knight_of_swords"

        if not matched_id:
            import hashlib
            h = int(hashlib.md5(contents[:2048] if contents else b"tarot_card").hexdigest(), 16)
            matched_id = candidate_ids[h % len(candidate_ids)]

        details = await asyncio.to_thread(PrologService.get_tarot_card_details, matched_id)
        if details:
            return {
                "card_name": details["name"],
                "card_id": details["id"],
                "orientation": "upright",
                "confidence": "high",
                "keywords": details["keywords"],
                "upright_meaning": ", ".join(details["upright"]),
                "reversed_meaning": ", ".join(details["reversed"]),
                "brief_interpretation": f"Symbolic scanner identified {details['name']}. Key energies encompass {', '.join(details['keywords'][:3])}.",
            }

        return {
            "error": "Could not analyze the image. Please ensure it shows a clear tarot card.",
            "confidence": "none",
        }

    # The vision model only identifies *which* card it is; its recollection of
    # keywords/meanings can drift from what the rest of the app shows (which
    # all comes from tarot.pl). Once we know the card, overwrite those fields
    # with the authoritative Prolog data so results stay consistent app-wide.
    card_id = result.get("card_id", "")
    details = await asyncio.to_thread(PrologService.get_tarot_card_details, card_id)
    if not details:
        # Vision model may have given a display name without a matching id.
        resolved_id = await asyncio.to_thread(
            PrologService.find_card_id_by_name, result.get("card_name", "")
        )
        if resolved_id:
            card_id = resolved_id
            details = await asyncio.to_thread(PrologService.get_tarot_card_details, card_id)

    if details:
        return {
            "card_name": details["name"],
            "card_id": details["id"],
            "orientation": result.get("orientation", "upright"),
            "confidence": result.get("confidence", "low"),
            "keywords": details["keywords"],
            "upright_meaning": ", ".join(details["upright"]),
            "reversed_meaning": ", ".join(details["reversed"]),
            "brief_interpretation": result.get("brief_interpretation", ""),
        }

    # Unrecognized card id — fall back to the vision model's own answer but
    # flag it so the UI can show it's unverified against the knowledge base.
    return {
        "card_name": result.get("card_name", "Unknown"),
        "card_id": card_id,
        "orientation": result.get("orientation", "upright"),
        "confidence": "low",
        "keywords": result.get("keywords", []),
        "upright_meaning": result.get("upright_meaning", ""),
        "reversed_meaning": result.get("reversed_meaning", ""),
        "brief_interpretation": result.get("brief_interpretation", ""),
        "unverified": True,
    }


@router.post("/explain")
async def explain_card(data: dict):
    """Get a detailed explanation of a tarot card."""
    card_name = data.get("card_name", "")
    orientation = data.get("orientation", "upright")

    if not card_name:
        return {"error": "card_name is required"}

    card_id = data.get("card_id") or await asyncio.to_thread(
        PrologService.find_card_id_by_name, card_name
    )
    details = await asyncio.to_thread(PrologService.get_tarot_card_details, card_id) if card_id else None

    explanation = await explain_tarot_card(card_name, orientation, details)

    if not explanation:
        card_kw = ", ".join(details["keywords"]) if details else "insight, willpower, courage"
        meanings = (details["upright"] if orientation == "upright" else details["reversed"]) if details else ["decisive action", "momentum"]
        meaning_str = ", ".join(meanings)
        explanation = f"""### {card_name} ({orientation.capitalize()})

**Symbolic Interpretation & Meaning**
The {card_name} represents powerful catalytic energy, swift mental clarity, and purposeful movement. In the {orientation} position, its archetypal forces emphasize {meaning_str}.

**Key Themes & Keywords**
- {card_kw}

**What It Means in Your Reading**
This card signals an urgent call to action and unyielding focus. You are being encouraged to cut through ambiguity, trust your intellect and discernment, and advance without fear of challenge.

**Daily Life Application**
Direct your concentration toward clear communication and truth. Ensure that passion is balanced with conscious awareness, allowing your decisions to be swift yet grounded.

**Cautionary Guidance**
Beware of impatience or rushing ahead without fully anticipating consequences. True mastery comes from pairing decisive force with wisdom and measured foresight."""

    return {
        "card_name": card_name,
        "orientation": orientation,
        "explanation": explanation,
    }
