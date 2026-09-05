import asyncio

from fastapi import APIRouter
from app.schemas.models import CompatibilityRequest
from app.services.prolog_service import PrologService

router = APIRouter(prefix="/api/compatibility", tags=["compatibility"])


@router.post("/analyze")
async def analyze_compatibility(request: CompatibilityRequest):
    # The endpoint displays the detailed element/modality analysis.  The
    # scoring-only compatibility result does not contain those fields.
    # PrologService calls are synchronous, blocking pyswip queries — run each
    # off the event loop so one slow query doesn't stall every other request.
    analysis = await asyncio.to_thread(
        PrologService.analyze_synastry, request.sign1, request.sign2
    )
    if not analysis:
        return {"error": "Could not analyze compatibility"}

    level = await asyncio.to_thread(
        PrologService.get_compatibility_level, request.sign1, request.sign2
    )
    trace = await asyncio.to_thread(
        PrologService.generate_compatibility_trace, request.sign1, request.sign2
    )

    return {
        "sign1": analysis["sign1"],
        "sign2": analysis["sign2"],
        "element1": analysis["element1"],
        "element2": analysis["element2"],
        "modality1": analysis["modality1"],
        "modality2": analysis["modality2"],
        "level": level,
        "element_description": analysis["element_description"],
        "reasoning": trace,
    }


def _synastry_deep_dive(sign1: str, sign2: str) -> dict:
    """Bundle of synchronous Prolog calls for the full synastry breakdown."""
    analysis = PrologService.analyze_synastry(sign1, sign2)
    breakdown = PrologService.get_compatibility_score_breakdown(sign1, sign2)
    trait_pairs = PrologService.get_synastry_trait_pairs(sign1, sign2)
    trace = PrologService.get_synastry_reasoning_trace(sign1, sign2)
    return {
        "analysis": analysis,
        "breakdown": breakdown,
        "trait_pairs": trait_pairs,
        "trace": trace,
    }


@router.post("/synastry")
async def synastry_deep_dive(request: CompatibilityRequest):
    """Full synastry breakdown: numeric score components, communication and
    balance themes, strengths/challenges, and complementary trait pairs —
    the parts of synastry.pl the basic /analyze endpoint above doesn't use."""
    result = await asyncio.to_thread(_synastry_deep_dive, request.sign1, request.sign2)
    analysis, breakdown = result["analysis"], result["breakdown"]
    if not analysis or not breakdown:
        return {"error": "Could not analyze synastry"}

    return {
        "sign1": analysis["sign1"],
        "sign2": analysis["sign2"],
        "overall_level": analysis["overall_level"],
        "overall_score": analysis["overall_score"],
        "score_breakdown": breakdown,
        "communication_theme": analysis["communication_theme"],
        "balance_theme": analysis["balance_theme"],
        "strengths": analysis["strengths"],
        "challenges": analysis["challenges"],
        "complementary_traits": result["trait_pairs"],
        "reasoning": result["trace"],
    }
