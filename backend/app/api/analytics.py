import json
from fastapi import APIRouter
from app.database import get_db

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("")
async def get_history():
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT id, question, category, zodiac_sign, spread_type, cards_json, themes_json, ai_interpretation, created_at FROM reading WHERE profile_id = 1 ORDER BY created_at DESC"
        )
        rows = await cursor.fetchall()
        return [
            {
                "id": r[0],
                "question": r[1] or "",
                "category": r[2] or "general",
                "zodiac_sign": r[3] or "aries",
                "spread_type": r[4] or "three_card",
                "cards_json": r[5] or "[]",
                "themes_json": r[6] or "[]",
                "ai_interpretation": r[7] or "",
                "created_at": r[8] or "",
            }
            for r in rows
        ]
    finally:
        await db.close()


@router.get("/{reading_id}")
async def get_reading(reading_id: int):
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT id, question, category, zodiac_sign, spread_type, cards_json, orientations_json, themes_json, reasoning_json, ai_interpretation, created_at FROM reading WHERE id = ?",
            (reading_id,),
        )
        row = await cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "question": row[1] or "",
                "category": row[2] or "general",
                "zodiac_sign": row[3] or "aries",
                "spread_type": row[4] or "three_card",
                "cards": json.loads(row[5]) if row[5] else [],
                "orientations": json.loads(row[6]) if row[6] else [],
                "themes": json.loads(row[7]) if row[7] else [],
                "reasoning": json.loads(row[8]) if row[8] else [],
                "ai_interpretation": row[9] or "",
                "created_at": row[10] or "",
            }
        return {"error": "Reading not found"}
    finally:
        await db.close()


@router.delete("/{reading_id}")
async def delete_reading(reading_id: int):
    db = await get_db()
    try:
        await db.execute("DELETE FROM reading WHERE id = ?", (reading_id,))
        await db.commit()
        return {"status": "deleted"}
    finally:
        await db.close()
