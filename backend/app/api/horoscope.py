from fastapi import APIRouter
from app.services.prolog_service import PrologService

router = APIRouter(prefix="/api/zodiac", tags=["zodiac"])


@router.get("")
async def get_all_zodiac():
    return PrologService.get_all_zodiac_signs()


@router.get("/{sign}")
async def get_zodiac(sign: str):
    info = PrologService.get_zodiac_info(sign)
    if info:
        return info
    return {"error": "Sign not found"}
