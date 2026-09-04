import json
from app.database import get_db


class AnalyticsService:
    @staticmethod
    async def get_analytics(profile_id: int = 1) -> dict:
        db = await get_db()
        try:
            cursor = await db.execute(
                "SELECT COUNT(*) FROM reading WHERE profile_id = ?",
                (profile_id,),
            )
            total = (await cursor.fetchone())[0]

            cursor = await db.execute(
                "SELECT cards_json FROM reading WHERE profile_id = ?",
                (profile_id,),
            )
            rows = await cursor.fetchall()

            card_counts: dict[str, int] = {}
            suit_counts: dict[str, int] = {"wands": 0, "cups": 0, "swords": 0, "pentacles": 0}
            major_count = 0
            minor_count = 0
            upright_count = 0
            reversed_count = 0
            theme_counts: dict[str, int] = {}
            category_counts: dict[str, int] = {}

            for row in rows:
                try:
                    cards = json.loads(row[0]) if row[0] else []
                except json.JSONDecodeError:
                    continue

                for card in cards:
                    card_name = card.get("card", "") if isinstance(card, dict) else card
                    card_counts[card_name] = card_counts.get(card_name, 0) + 1

                    if "_of_wands" in card_name:
                        suit_counts["wands"] += 1
                    elif "_of_cups" in card_name:
                        suit_counts["cups"] += 1
                    elif "_of_swords" in card_name:
                        suit_counts["swords"] += 1
                    elif "_of_pentacles" in card_name:
                        suit_counts["pentacles"] += 1

                    major_arcana = [
                        "the_fool", "the_magician", "the_high_priestess",
                        "the_empress", "the_emperor", "the_hierophant",
                        "the_lovers", "the_chariot", "strength", "the_hermit",
                        "wheel_of_fortune", "justice", "the_hanged_man",
                        "death", "temperance", "the_devil", "the_tower",
                        "the_star", "the_moon", "the_sun", "judgement",
                        "the_world",
                    ]
                    if card_name in major_arcana:
                        major_count += 1
                    else:
                        minor_count += 1

                    if isinstance(card, dict) and card.get("is_reversed"):
                        reversed_count += 1
                    else:
                        upright_count += 1

            cursor = await db.execute(
                "SELECT themes_json FROM reading WHERE profile_id = ?",
                (profile_id,),
            )
            theme_rows = await cursor.fetchall()
            for row in theme_rows:
                try:
                    themes = json.loads(row[0]) if row[0] else []
                    for theme in themes:
                        theme_counts[theme] = theme_counts.get(theme, 0) + 1
                except json.JSONDecodeError:
                    continue

            cursor = await db.execute(
                "SELECT category FROM reading WHERE profile_id = ?",
                (profile_id,),
            )
            cat_rows = await cursor.fetchall()
            for row in cat_rows:
                cat = row[0]
                if cat:
                    category_counts[cat] = category_counts.get(cat, 0) + 1

            most_drawn = sorted(
                card_counts.items(), key=lambda x: x[1], reverse=True
            )[:10]
            most_themes = sorted(
                theme_counts.items(), key=lambda x: x[1], reverse=True
            )[:10]
            most_cats = sorted(
                category_counts.items(), key=lambda x: x[1], reverse=True
            )[:10]

            most_suit = max(suit_counts, key=suit_counts.get) if suit_counts else "none"

            return {
                "total_readings": total,
                "most_drawn_cards": [
                    {"card": c, "count": n} for c, n in most_drawn
                ],
                "most_common_suit": most_suit,
                "major_vs_minor": {
                    "major": major_count,
                    "minor": minor_count,
                },
                "most_common_themes": [
                    {"theme": t, "count": n} for t, n in most_themes
                ],
                "most_common_categories": [
                    {"category": c, "count": n} for c, n in most_cats
                ],
                "upright_vs_reversed": {
                    "upright": upright_count,
                    "reversed": reversed_count,
                },
            }
        finally:
            await db.close()
