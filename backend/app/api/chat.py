import json
from fastapi import APIRouter
from app.schemas.models import ChatRequest
from app.services.openrouter_service import chat_with_assistant
from app.database import get_db

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("")
async def chat(request: ChatRequest):
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT role, content FROM chat_message WHERE profile_id = 1 ORDER BY id DESC LIMIT 10"
        )
        rows = await cursor.fetchall()
        history = [{"role": r[0], "content": r[1]} for r in reversed(rows)]

        response = await chat_with_assistant(
            message=request.message,
            zodiac_sign=request.zodiac_sign,
            current_reading=request.current_reading,
            chat_history=history,
        )

        await db.execute(
            "INSERT INTO chat_message (profile_id, role, content) VALUES (1, 'user', ?)",
            (request.message,),
        )
        if response:
            await db.execute(
                "INSERT INTO chat_message (profile_id, role, content) VALUES (1, 'assistant', ?)",
                (response,),
            )
        await db.commit()

        return {
            "response": response or "I'm having trouble connecting to my mystical sources right now. Please try again in a moment.",
            "context_used": {
                "zodiac_sign": request.zodiac_sign,
                "has_reading": request.current_reading is not None,
            },
        }
    finally:
        await db.close()
