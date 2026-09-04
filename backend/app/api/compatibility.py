from fastapi import APIRouter
from app.schemas.models import CompatibilityRequest
from app.services.prolog_service import PrologService

router = APIRouter(prefix="/api/compatibility", tags=["compatibility"])


@router.post("/analyze")
async def analyze_compatibility(request: CompatibilityRequest):
    # The endpoint displays the detailed element/modality analysis.  The
    # scoring-only compatibility result does not contain those fields.
    analysis = PrologService.analyze_synastry(
        request.sign1, request.sign2
    )
    if not analysis:
        return {"error": "Could not analyze compatibility"}

    level = PrologService.get_compatibility_level(
        request.sign1, request.sign2
    )
    trace = PrologService.generate_compatibility_trace(
        request.sign1, request.sign2
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
