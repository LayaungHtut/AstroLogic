import random
from app.services.tarot_api_client import TarotAPIClient


class TarotService:
    @staticmethod
    def to_prolog_card_atom(name: str) -> str:
        """Convert a card's display name (e.g. "The Hanged Man", "Ace of Wands")
        into the snake_case atom the Prolog knowledge base uses to identify it
        (the_hanged_man, ace_of_wands, ...) — see prolog/tarot.pl's
        tarot_card/3 facts. This is the *only* correct way to hand a drawn
        card to any Prolog predicate that reasons about specific cards
        (card_theme/2, analyze_card/3, card_priority/3, etc.): those predicates
        are keyed on this snake_case naming, not on the short display code
        ("01", "w01", ...) used for images/UI, which they will silently never
        match — themes, conflicts, and priority all resolve empty otherwise.
        """
        return name.lower().replace(" ", "_").replace("'", "")

    @staticmethod
    def to_prolog_position_atom(position: str) -> str:
        """Convert a spread position's display label (e.g. "Current Position",
        "Path A", "What to Understand") into the snake_case atom
        position_meaning_modifier/2 and position_theme_emphasis/2
        (prolog/reading_analysis.pl) are keyed on. Spread position labels
        come from spread_rules.pl's spread_positions/2, which is the
        capitalized version that wins over card_selection.pl's own
        (lowercase) definition of the same predicate — SWI keeps whichever
        file's clauses were consulted last, see prolog_service.py's load
        order. Passing the capitalized label straight into a Prolog query
        never matches the lowercase atoms those two predicates expect.
        """
        return position.lower().replace(" ", "_")

    @staticmethod
    async def draw_cards(count: int = 3, spread_type: str | None = None) -> list[dict]:
        cards = await TarotAPIClient.fetch_random_cards(count)
        result = []
        for card in cards:
            is_reversed = random.random() < 0.35
            name = card.get("name", "")
            result.append({
                "card": card.get("name_short", ""),
                "name": name,
                "prolog_card": TarotService.to_prolog_card_atom(name),
                "is_reversed": is_reversed,
                "keywords": TarotAPIClient.extract_keywords(card),
                "image": TarotAPIClient.get_card_image_url(name),
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
            name = card.get("name", "")
            result.append({
                "card": card.get("name_short", ""),
                "name": name,
                "prolog_card": TarotService.to_prolog_card_atom(name),
                "position": positions[i] if i < len(positions) else f"Position {i+1}",
                "is_reversed": is_reversed,
                "keywords": TarotAPIClient.extract_keywords(card),
                "image": TarotAPIClient.get_card_image_url(name),
                "meaning_upright": card.get("meaning_up", ""),
                "meaning_reversed": card.get("meaning_rev", ""),
            })
        return result

    @staticmethod
    async def build_cards_from_selection(
        selections: list[tuple[str, bool]],
        positions: list[str],
    ) -> list[dict] | None:
        """Build the same per-card dict shape draw_cards_with_positions
        returns, but for specific cards the user picked (name, is_reversed)
        rather than a random draw — order and orientation are exactly what
        the caller passed in, nothing is randomized here.

        Returns None if any name doesn't match a real tarot card, so the
        caller can reject the request instead of silently reading fewer
        cards than the user actually chose.
        """
        result = []
        for i, (name, is_reversed) in enumerate(selections):
            card = await TarotAPIClient.fetch_card_by_name(name)
            if not card:
                return None
            real_name = card.get("name", name)
            result.append({
                "card": card.get("name_short", ""),
                "name": real_name,
                "prolog_card": TarotService.to_prolog_card_atom(real_name),
                "position": positions[i] if i < len(positions) else f"Card {i + 1}",
                "is_reversed": is_reversed,
                "keywords": TarotAPIClient.extract_keywords(card),
                "image": TarotAPIClient.get_card_image_url(real_name),
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
