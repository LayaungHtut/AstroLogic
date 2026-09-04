import random
from app.services.tarot_api_client import TarotAPIClient


class TarotService:
    @staticmethod
    async def draw_cards(count: int = 3, spread_type: str | None = None) -> list[dict]:
        cards = await TarotAPIClient.fetch_random_cards(count)
        result = []
        for card in cards:
            is_reversed = random.random() < 0.35
            result.append({
                "card": card.get("name_short", ""),
                "name": card.get("name", ""),
                "is_reversed": is_reversed,
                "keywords": TarotAPIClient.extract_keywords(card),
                "image": TarotAPIClient.get_card_image_url(card.get("name", "")),
                "meaning_upright": card.get("meaning_up", ""),
                "meaning_reversed": card.get("meaning_rev", ""),
            })
        return result

    @staticmethod
    async def draw_cards_with_positions(
        positions: list[str],
        zodiac_sign: str | None = None,
        category: str | None = None,
    ) -> list[dict]:
        count = len(positions)
        cards = await TarotAPIClient.fetch_random_cards(count)
        result = []
        for i, card in enumerate(cards):
            is_reversed = random.random() < 0.35
            result.append({
                "card": card.get("name_short", ""),
                "name": card.get("name", ""),
                "position": positions[i] if i < len(positions) else f"Position {i+1}",
                "is_reversed": is_reversed,
                "keywords": TarotAPIClient.extract_keywords(card),
                "image": TarotAPIClient.get_card_image_url(card.get("name", "")),
                "meaning_upright": card.get("meaning_up", ""),
                "meaning_reversed": card.get("meaning_rev", ""),
            })
        return result

    @staticmethod
    async def get_card_info(card_id: str) -> dict | None:
        card = await TarotAPIClient.fetch_card_by_name(card_id)
        if card:
            return {
                "card": card.get("name_short", ""),
                "name": card.get("name", ""),
                "keywords": TarotAPIClient.extract_keywords(card),
                "image": TarotAPIClient.get_card_image_url(card.get("name", "")),
                "meaning_upright": card.get("meaning_up", ""),
                "meaning_reversed": card.get("meaning_rev", ""),
            }
        return None

    @staticmethod
    async def get_all_cards() -> list[dict]:
        cards = await TarotAPIClient.fetch_all_cards()
        return [
            {
                "card": card.get("name_short", ""),
                "name": card.get("name", ""),
                "keywords": TarotAPIClient.extract_keywords(card),
                "image": TarotAPIClient.get_card_image_url(card.get("name", "")),
                "arcana": card.get("type", ""),
                "suit": card.get("suit", ""),
            }
            for card in cards
        ]

    @staticmethod
    def get_spread_positions(spread_type: str) -> list[str]:
        spreads = {
            "one_card": ["Guidance"],
            "three_card": ["Past", "Present", "Future"],
            "decision": ["Current Situation", "Path A", "Path B", "Advice"],
            "self_reflection": ["Current Self", "Hidden Influence", "What to Understand", "Guidance"],
            "relationship": ["You", "Other Person", "Connection", "Challenge", "Guidance"],
            "career": ["Current Position", "Strength", "Challenge", "Opportunity", "Advice"],
        }
        return spreads.get(spread_type, ["Past", "Present", "Future"])
