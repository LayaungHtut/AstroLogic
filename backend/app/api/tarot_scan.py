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

    if not result:
        return {
            "error": "Could not analyze the image. Please ensure it shows a clear tarot card.",
            "confidence": "none",
        }

    if "error" in result:
        return result

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
        return {"error": "Could not generate explanation. Please try again."}

    return {
        "card_name": card_name,
        "orientation": orientation,
        "explanation": explanation,
    }
