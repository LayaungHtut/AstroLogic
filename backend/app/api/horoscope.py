import asyncio

from fastapi import APIRouter
from app.services.prolog_service import PrologService

router = APIRouter(prefix="/api/zodiac", tags=["zodiac"])


@router.get("")
async def get_all_zodiac():
    return await asyncio.to_thread(PrologService.get_all_zodiac_signs)


@router.get("/{sign}")
async def get_zodiac(sign: str):
    info = await asyncio.to_thread(PrologService.get_zodiac_info, sign)
    if info:
        return info
    return {"error": "Sign not found"}


def _profile_with_trace(sign: str) -> dict:
    return {
        "profile": PrologService.generate_profile(sign),
        "trace": PrologService.get_profile_reasoning_trace(sign),
    }


@router.get("/{sign}/profile")
async def get_zodiac_profile(sign: str):
    """"Why am I like this?" — the full generated personality profile for a
    sign plus the Prolog reasoning chain that derived it, step by step."""
    result = await asyncio.to_thread(_profile_with_trace, sign)
    if not result["profile"]:
        return {"error": "Sign not found"}
    return {
        "profile": result["profile"],
        "reasoning": result["trace"],
    }
