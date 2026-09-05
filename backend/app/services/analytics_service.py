import asyncio
import json

from app.database import get_db
from app.services.prolog_service import PrologService


class AnalyticsService:
    @staticmethod
    async def _load_reading_rows(profile_id: int) -> list[dict]:
        """Load each saved reading's cards/themes/category as plain data.

        This is the only part that stays in Python: reading rows out of
        SQLite. Everything derived from them (counts, biases, recurring
        patterns) is computed by Prolog in get_analytics below.
        """
        db = await get_db()
        try:
            cursor = await db.execute(
                "SELECT cards_json, themes_json, category FROM reading WHERE profile_id = ?",
                (profile_id,),
            )
            rows = await cursor.fetchall()
        finally:
            await db.close()

        readings = []
        for cards_json, themes_json, category in rows:
            try:
                cards = json.loads(cards_json) if cards_json else []
            except json.JSONDecodeError:
                cards = []
            try:
                themes = json.loads(themes_json) if themes_json else []
            except json.JSONDecodeError:
                themes = []
            readings.append({"cards": cards, "themes": themes, "category": category or "general"})
        return readings

    @staticmethod
    async def get_analytics(profile_id: int = 1) -> dict:
        readings = await AnalyticsService._load_reading_rows(profile_id)

        card_orientations: list[tuple[str, str]] = []
        all_themes: list[str] = []
        categories: list[str] = []
        records: list[dict] = []

        for reading in readings:
            categories.append(reading["category"])
            all_themes.extend(reading["themes"])
            reading_cards = []
            for card in reading["cards"]:
                if isinstance(card, dict):
                    name = card.get("card", "")
                    orientation = "reversed" if card.get("is_reversed") else "upright"
                else:
                    name = card
                    orientation = "upright"
                if not name:
                    continue
                card_orientations.append((name, orientation))
                reading_cards.append(name)
            records.append({"category": reading["category"], "cards": reading_cards})

        # PrologService calls are synchronous, blocking pyswip queries — run
        # off the event loop so one slow query doesn't stall other requests.
        # The two calls must stay sequential: pyswip's global Prolog engine
        # isn't safe for two concurrent queries from different threads (a
        # concurrent second query aborts the first with "query not closed").
        analytics = await asyncio.to_thread(
            PrologService.get_history_analytics, card_orientations, all_themes, categories
        )
        insights = await asyncio.to_thread(
            PrologService.get_history_insights, records, all_themes, card_orientations
        )

        if analytics is None:
            analytics = {
                "total_readings": 0,
                "most_drawn_cards": [],
                "most_common_suit": "none",
                "major_vs_minor": {"major": 0, "minor": 0},
                "most_common_themes": [],
                "most_common_categories": [],
                "upright_vs_reversed": {"upright": 0, "reversed": 0},
            }

        analytics["insights"] = insights
        return analytics
