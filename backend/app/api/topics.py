import asyncio

from fastapi import APIRouter
from app.services.prolog_service import PrologService
from app.schemas.models import ReadingAnalyzeRequest

router = APIRouter(prefix="/api/topics", tags=["topics"])


@router.get("")
async def get_topics():
    """Get all available tarot topics."""
    return await asyncio.to_thread(PrologService.get_all_topics)


@router.get("/{topic}")
async def get_topic(topic: str):
    """Get info about a specific topic."""
    info = await asyncio.to_thread(PrologService.get_topic_info, topic)
    if info:
        return info
    return {"error": "Topic not found"}


@router.post("/classify")
async def classify_topic(data: dict):
    """Classify a question into a tarot topic."""
    question = data.get("question", "")
    if not question:
        return {"error": "question is required"}
    topic = await asyncio.to_thread(PrologService.classify_topic, question)
    info = await asyncio.to_thread(PrologService.get_topic_info, topic)
    return {
        "question": question,
        "topic": topic,
        "topic_info": info,
    }
