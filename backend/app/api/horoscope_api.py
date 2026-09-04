import asyncio

from fastapi import APIRouter
from app.services.horoscope_service import HoroscopeService
from app.services.prolog_service import PrologService
from app.schemas.models import HoroscopeRequest

router = APIRouter(prefix="/api/horoscope", tags=["horoscope"])


@router.post("/generate")
async def generate_horoscope(request: HoroscopeRequest):
    # PrologService calls are synchronous, blocking pyswip queries — run each
    # off the event loop so one slow query doesn't stall every other request.
    guidance = await asyncio.to_thread(
        PrologService.get_horoscope_guidance, request.zodiac_sign, request.mood
    )
    if not guidance:
        return {"error": "Could not generate horoscope"}

    result = await HoroscopeService.generate_horoscope(
        request.zodiac_sign, request.mood
    )

    trace = await asyncio.to_thread(
        PrologService.generate_horoscope_trace, request.zodiac_sign, request.mood
    )

    if result:
        result["reasoning"] = trace
        return result

    return {
        "zodiac_sign": request.zodiac_sign,
        "element": guidance["element"],
        "theme": guidance["theme"],
        "mood": request.mood,
        "guidance": f"Today emphasizes {guidance['theme']} energy for {request.zodiac_sign}.",
        "reflection": f"How can you embrace {guidance['theme']} in your daily life?",
        "opportunity": f"Look for moments of {guidance['mood_theme']} today.",
        "caution": "Remember to stay grounded and present.",
        "reasoning": trace,
    }
