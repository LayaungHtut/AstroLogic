import aiosqlite
from pathlib import Path
from app.config import DATABASE_PATH, DATABASE_DIR

DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS user_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT NOT NULL DEFAULT 'Explorer',
    birth_date TEXT,
    zodiac_sign TEXT,
    preferred_style TEXT DEFAULT 'balanced',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reading (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER DEFAULT 1,
    question TEXT,
    category TEXT,
    zodiac_sign TEXT,
    spread_type TEXT,
    cards_json TEXT,
    orientations_json TEXT,
    themes_json TEXT,
    reasoning_json TEXT,
    ai_interpretation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES user_profile(id)
);

CREATE TABLE IF NOT EXISTS reading_card (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reading_id INTEGER NOT NULL,
    card_name TEXT NOT NULL,
    position TEXT,
    is_reversed INTEGER DEFAULT 0,
    keywords_json TEXT,
    FOREIGN KEY (reading_id) REFERENCES reading(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chat_message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER DEFAULT 1,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES user_profile(id)
);
"""


async def get_db() -> aiosqlite.Connection:
    db = await aiosqlite.connect(str(DATABASE_PATH))
    db.row_factory = aiosqlite.Row
    return db


async def init_db():
    db = await get_db()
    try:
        await db.executescript(SCHEMA_SQL)
        cursor = await db.execute("SELECT COUNT(*) FROM user_profile")
        row = await cursor.fetchone()
        if row[0] == 0:
            await db.execute(
                "INSERT INTO user_profile (nickname, zodiac_sign) VALUES (?, ?)",
                ("Explorer", "aries"),
            )
        await db.commit()
    finally:
        await db.close()
