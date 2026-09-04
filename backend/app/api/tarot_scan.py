import json
from fastapi import APIRouter, UploadFile, File
from app.services.openrouter_service import scan_tarot_image, explain_tarot_card

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

    return {
        "card_name": result.get("card_name", "Unknown"),
        "card_id": result.get("card_id", ""),
        "orientation": result.get("orientation", "upright"),
        "confidence": result.get("confidence", "low"),
        "keywords": result.get("keywords", []),
        "upright_meaning": result.get("upright_meaning", ""),
        "reversed_meaning": result.get("reversed_meaning", ""),
        "brief_interpretation": result.get("brief_interpretation", ""),
    }


@router.post("/explain")
async def explain_card(data: dict):
    """Get a detailed explanation of a tarot card."""
    card_name = data.get("card_name", "")
    orientation = data.get("orientation", "upright")

    if not card_name:
        return {"error": "card_name is required"}

    explanation = await explain_tarot_card(card_name, orientation)

    if not explanation:
        return {"error": "Could not generate explanation. Please try again."}

    return {
        "card_name": card_name,
        "orientation": orientation,
        "explanation": explanation,
    }
