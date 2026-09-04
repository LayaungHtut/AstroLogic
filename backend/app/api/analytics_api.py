from fastapi import APIRouter
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("")
async def get_analytics():
    return await AnalyticsService.get_analytics(profile_id=1)
