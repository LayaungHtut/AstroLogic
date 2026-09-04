import httpx
import asyncio
from typing import Optional

CARDS_JSON_URL = "https://sixseeds.github.io/tarot-api/cards.json"
IMAGES_BASE_URL = "https://sixseeds.github.io/tarot-api/cards"
CARD_BACK_URL = f"{IMAGES_BASE_URL}/back.jpg"

NAME_TO_IMAGE: dict[str, str] = {
    "The Fool": "ar00", "The Magician": "ar01", "The High Priestess": "ar02",
    "The Empress": "ar03", "The Emperor": "ar04", "The Hierophant": "ar05",
    "The Lovers": "ar06", "The Chariot": "ar07", "Strength": "ar08",
    "The Hermit": "ar09", "Wheel of Fortune": "ar10", "Justice": "ar11",
    "The Hanged Man": "ar12", "Death": "ar13", "Temperance": "ar14",
    "The Devil": "ar15", "The Tower": "ar16", "The Star": "ar17",
    "The Moon": "ar18", "The Sun": "ar19", "Judgement": "ar20", "The World": "ar21",
    "Ace of Wands": "wa01", "Two of Wands": "wa02", "Three of Wands": "wa03",
    "Four of Wands": "wa04", "Five of Wands": "wa05", "Six of Wands": "wa06",
    "Seven of Wands": "wa07", "Eight of Wands": "wa08", "Nine of Wands": "wa09",
    "Ten of Wands": "wa10", "Page of Wands": "wa11", "Knight of Wands": "wa12",
    "Queen of Wands": "wa13", "King of Wands": "wa14",
    "Ace of Cups": "cu01", "Two of Cups": "cu02", "Three of Cups": "cu03",
    "Four of Cups": "cu04", "Five of Cups": "cu05", "Six of Cups": "cu06",
    "Seven of Cups": "cu07", "Eight of Cups": "cu08", "Nine of Cups": "cu09",
    "Ten of Cups": "cu10", "Page of Cups": "cu11", "Knight of Cups": "cu12",
    "Queen of Cups": "cu13", "King of Cups": "cu14",
    "Ace of Swords": "sw01", "Two of Swords": "sw02", "Three of Swords": "sw03",
    "Four of Swords": "sw04", "Five of Swords": "sw05", "Six of Swords": "sw06",
    "Seven of Swords": "sw07", "Eight of Swords": "sw08", "Nine of Swords": "sw09",
    "Ten of Swords": "sw10", "Page of Swords": "sw11", "Knight of Swords": "sw12",
    "Queen of Swords": "sw13", "King of Swords": "sw14",
    "Ace of Pentacles": "pe01", "Two of Pentacles": "pe02", "Three of Pentacles": "pe03",
    "Four of Pentacles": "pe04", "Five of Pentacles": "pe05", "Six of Pentacles": "pe06",
    "Seven of Pentacles": "pe07", "Eight of Pentacles": "pe08", "Nine of Pentacles": "pe09",
    "Ten of Pentacles": "pe10", "Page of Pentacles": "pe11", "Knight of Pentacles": "pe12",
    "Queen of Pentacles": "pe13", "King of Pentacles": "pe14",
}

BUILTIN_CARDS: list[dict] = [
    {"name_short": "00", "name": "The Fool", "type": "major", "suit": "",
     "meaning_up": "Beginnings; Innocence; Spontaneity; Free spirit",
     "meaning_rev": "Recklessness; Risk-taking; Holding back; Foolishness"},
    {"name_short": "01", "name": "The Magician", "type": "major", "suit": "",
     "meaning_up": "Manifestation; Resourcefulness; Power; Inspired action",
     "meaning_rev": "Manipulation; Poor planning; Untapped talents"},
    {"name_short": "02", "name": "The High Priestess", "type": "major", "suit": "",
     "meaning_up": "Intuition; Sacred knowledge; Divine feminine; Subconscious mind",
     "meaning_rev": "Secrets; Withdrawal; Silence; Detachment"},
    {"name_short": "03", "name": "The Empress", "type": "major", "suit": "",
     "meaning_up": "Femininity; Beauty; Nature; Abundance; Nurturing",
     "meaning_rev": "Creative block; Dependence; Emptiness"},
    {"name_short": "04", "name": "The Emperor", "type": "major", "suit": "",
     "meaning_up": "Authority; Establishment; Structure; A father figure",
     "meaning_rev": "Tyranny; Rigidity; Overbearing"},
    {"name_short": "05", "name": "The Hierophant", "type": "major", "suit": "",
     "meaning_up": "Spiritual wisdom; Religious beliefs; Tradition; Institutions",
     "meaning_rev": "Personal beliefs; Freedom; Challenging the status quo"},
    {"name_short": "06", "name": "The Lovers", "type": "major", "suit": "",
     "meaning_up": "Love; Harmony; Relationships; Values alignment; Choices",
     "meaning_rev": "Self-love; Disharmony; Imbalance; Misalignment"},
    {"name_short": "07", "name": "The Chariot", "type": "major", "suit": "",
     "meaning_up": "Control; Willpower; Success; Determination",
     "meaning_rev": "Lack of control; No direction; Aggression"},
    {"name_short": "08", "name": "Strength", "type": "major", "suit": "",
     "meaning_up": "Courage; Patience; Compassion; Inner strength",
     "meaning_rev": "Weakness; Self-doubt; Lack of discipline"},
    {"name_short": "09", "name": "The Hermit", "type": "major", "suit": "",
     "meaning_up": "Soul-searching; Introspection; Solitude; Inner guidance",
     "meaning_rev": "Isolation; Withdrawal; Loneliness"},
    {"name_short": "10", "name": "Wheel of Fortune", "type": "major", "suit": "",
     "meaning_up": "Good luck; Cycles; Fate; Turning point",
     "meaning_rev": "Bad luck; Resistance to change; Breaking cycles"},
    {"name_short": "11", "name": "Justice", "type": "major", "suit": "",
     "meaning_up": "Justice; Fairness; Truth; Law; Karma",
     "meaning_rev": "Unfairness; Dishonesty; Lack of accountability"},
    {"name_short": "12", "name": "The Hanged Man", "type": "major", "suit": "",
     "meaning_up": "Surrender; Letting go; New perspectives; Sacrifice",
     "meaning_rev": "Delays; Resistance; Indecision; Stalling"},
    {"name_short": "13", "name": "Death", "type": "major", "suit": "",
     "meaning_up": "Endings; Change; Transformation; Transition",
     "meaning_rev": "Resistance to change; Stagnation; Decay"},
    {"name_short": "14", "name": "Temperance", "type": "major", "suit": "",
     "meaning_up": "Balance; Moderation; Patience; Purpose; Harmony",
     "meaning_rev": "Imbalance; Excess; Self-healing needed"},
    {"name_short": "15", "name": "The Devil", "type": "major", "suit": "",
     "meaning_up": "Shadow self; Attachment; Addiction; Restriction",
     "meaning_rev": "Release; Breaking free; Detachment"},
    {"name_short": "16", "name": "The Tower", "type": "major", "suit": "",
     "meaning_up": "Sudden change; Upheaval; Chaos; Revelation; Awakening",
     "meaning_rev": "Personal transformation; Fear of change; Avoiding disaster"},
    {"name_short": "17", "name": "The Star", "type": "major", "suit": "",
     "meaning_up": "Hope; Faith; Purpose; Renewal; Spirituality",
     "meaning_rev": "Lack of faith; Despair; Self-trust issues"},
    {"name_short": "18", "name": "The Moon", "type": "major", "suit": "",
     "meaning_up": "Illusion; Fear; Anxiety; Subconscious; Intuition",
     "meaning_rev": "Release of fear; Repressed emotion; Inner confusion"},
    {"name_short": "19", "name": "The Sun", "type": "major", "suit": "",
     "meaning_up": "Positivity; Fun; Warmth; Success; Vitality",
     "meaning_rev": "Inner child issues; Overoptimism; Temporary depression"},
    {"name_short": "20", "name": "Judgement", "type": "major", "suit": "",
     "meaning_up": "Judgement; Rebirth; Calling; Absolution",
     "meaning_rev": "Self-doubt; Refusal of self-examination"},
    {"name_short": "21", "name": "The World", "type": "major", "suit": "",
     "meaning_up": "Completion; Integration; Accomplishment; Travel",
     "meaning_rev": "Incompletion; Lack of closure; Shortcuts"},
    {"name_short": "w01", "name": "Ace of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Inspiration; New opportunities; Growth; Potential",
     "meaning_rev": "Delays; Lack of direction; Distraction"},
    {"name_short": "w02", "name": "Two of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Future planning; Progress; Decisions; Discovery",
     "meaning_rev": "Fear of change; Playing it safe; Bad planning"},
    {"name_short": "w03", "name": "Three of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Progress; Expansion; Foresight; Overseas opportunities",
     "meaning_rev": "Obstacles; Delays; Frustration"},
    {"name_short": "w04", "name": "Four of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Celebration; Joy; Harmony; Relaxation; Homecoming",
     "meaning_rev": "Personal conflict; Transition; Lack of support"},
    {"name_short": "w05", "name": "Five of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Conflict; Disagreements; Competition; Tension",
     "meaning_rev": "Avoiding conflict; Inner conflict; Cooperation"},
    {"name_short": "w06", "name": "Six of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Success; Public recognition; Progress; Self-confidence",
     "meaning_rev": "Private achievement; Fall from grace; Egotism"},
    {"name_short": "w07", "name": "Seven of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Challenge; Competition; Perseverance; Defensive",
     "meaning_rev": "Exhaustion; Giving up; Overwhelmed"},
    {"name_short": "w08", "name": "Eight of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Movement; Fast-paced change; Action; Alignment",
     "meaning_rev": "Delays; Frustration; Waiting; Slowness"},
    {"name_short": "w09", "name": "Nine of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Resilience; Grit; Last stand; Persistence",
     "meaning_rev": "Exhaustion; Fatigue; Paranoia"},
    {"name_short": "w10", "name": "Ten of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Burden; Extra responsibility; Hard work; Completion",
     "meaning_rev": "Releasing burdens; Overcommitment; Burnout"},
    {"name_short": "w11", "name": "Page of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Enthusiasm; Exploration; Discovery; Free spirit",
     "meaning_rev": "Setbacks to new ideas; Lack of direction; Procrastination"},
    {"name_short": "w12", "name": "Knight of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Energy; Passion; Inspired action; Adventure",
     "meaning_rev": "Haste; Scattered energy; Impulsiveness"},
    {"name_short": "w13", "name": "Queen of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Courage; Confidence; Independence; Determination; Warmth",
     "meaning_rev": "Selfishness; Jealousy; Insecure"},
    {"name_short": "w14", "name": "King of Wands", "type": "minor", "suit": "wands",
     "meaning_up": "Natural-born leader; Vision; Entrepreneur; Honor",
     "meaning_rev": "Impulsive; Overbearing; Aggressive"},
    {"name_short": "c01", "name": "Ace of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Love; New feelings; Emotional awakening; Creativity",
     "meaning_rev": "Emotional loss; Blocked creativity; Emptiness"},
    {"name_short": "c02", "name": "Two of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Unified love; Partnership; Mutual attraction; Connection",
     "meaning_rev": "Self-love needed; Break-up; Imbalance in relationship"},
    {"name_short": "c03", "name": "Three of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Celebration; Friendship; Creativity; Community",
     "meaning_rev": "Independence; Solitude; Gossip"},
    {"name_short": "c04", "name": "Four of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Meditation; Contemplation; Discontent; Apathy",
     "meaning_rev": "Retreat; Withdrawal; Checking yourself"},
    {"name_short": "c05", "name": "Five of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Regret; Failure; Disappointment; Pessimism",
     "meaning_rev": "Personal setbacks; Self-forgiveness; Moving on"},
    {"name_short": "c06", "name": "Six of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Revisiting the past; Childhood memories; Innocence; Joy",
     "meaning_rev": "Living in the past; Forgiveness needed; Naivety"},
    {"name_short": "c07", "name": "Seven of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Fantasy; Illusion; Wishful thinking; Choices",
     "meaning_rev": "Alignment; Personal values; Overwhelmed by choices"},
    {"name_short": "c08", "name": "Eight of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Disappointment; Abandonment; Withdrawal; Escapism",
     "meaning_rev": "Trying one more time; Indecision; Fear of loss"},
    {"name_short": "c09", "name": "Nine of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Contentment; Satisfaction; Gratitude; Wish come true",
     "meaning_rev": "Inner happiness; Materialism; Dissatisfaction"},
    {"name_short": "c10", "name": "Ten of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Divine love; Blissful relationships; Harmony; Alignment",
     "meaning_rev": "Disconnection; Misaligned values; Broken family"},
    {"name_short": "c11", "name": "Page of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Creative opportunity; Intuition; Curiosity; Stimulus",
     "meaning_rev": "Emotional immaturity; Insecurity; Frustration"},
    {"name_short": "c12", "name": "Knight of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Creativity; Romance; Charm; Imagination; Beauty",
     "meaning_rev": "Overactive imagination; Unrealistic; Jealousy"},
    {"name_short": "c13", "name": "Queen of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Compassionate; Caring; Ethically strong; Intuitive",
     "meaning_rev": "Inner feelings; Self-care needed; Co-dependency"},
    {"name_short": "c14", "name": "King of Cups", "type": "minor", "suit": "cups",
     "meaning_up": "Emotionally balanced; Compassionate; Diplomatic",
     "meaning_rev": "Self-compassion deficit; Inner feelings; Moodiness"},
    {"name_short": "s01", "name": "Ace of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "Breakthrough; Clarity; Sharp mind; Truth; Success",
     "meaning_rev": "Inner clarity needed; Re-think idea; Confusion"},
    {"name_short": "s02", "name": "Two of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "Difficult decisions; Avoidance; Indecision; Stalemate",
     "meaning_rev": "Indecision; Confusion; Information overload"},
    {"name_short": "s03", "name": "Three of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "Heartbreak; Emotional pain; Sorrow; Grief; Hurt",
     "meaning_rev": "Recovery; Forgiveness; Releasing pain; Optimism"},
    {"name_short": "s04", "name": "Four of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "Rest; Relaxation; Meditation; Contemplation; Recovery",
     "meaning_rev": "Exhaustion; Burn-out; Overextension"},
    {"name_short": "s05", "name": "Five of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "Conflict; Defeat; Winning at all costs; Betrayal",
     "meaning_rev": "Reconciliation; Making amends; Past resentment"},
    {"name_short": "s06", "name": "Six of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "Transition; Change; Rite of passage; Release",
     "meaning_rev": "Personal transition; Resistance; Stuck in a rut"},
    {"name_short": "s07", "name": "Seven of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "Deception; Trickery; Tactics; Strategy; Resourcefulness",
     "meaning_rev": "Coming clean; Re-thinking approach; Conscience"},
    {"name_short": "s08", "name": "Eight of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "Imprisonment; Entrapment; Self-victimization; Restriction",
     "meaning_rev": "Self-acceptance; New perspective; Freedom"},
    {"name_short": "s09", "name": "Nine of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "Anxiety; Worry; Fear; Depression; Nightmare",
     "meaning_rev": "Inner turmoil; Deep-seated fears; Hope"},
    {"name_short": "s10", "name": "Ten of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "Painful endings; Deep wounds; Betrayal; Loss; Crisis",
     "meaning_rev": "Recovery; Regeneration; Resisting an inevitable end"},
    {"name_short": "s11", "name": "Page of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "New ideas; Curiosity; Breadth of viewpoint; Communication",
     "meaning_rev": "Self-expression issues; Haste; Overthink"},
    {"name_short": "s12", "name": "Knight of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "Ambitious; Action-oriented; Driven; Perfectionist",
     "meaning_rev": "Impulsive; Burnout; Self-sabotage"},
    {"name_short": "s13", "name": "Queen of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "Independent; Clear boundaries; Direct communication; Fair",
     "meaning_rev": "Cold-hearted; Cruel; Bitterness; Overly emotional"},
    {"name_short": "s14", "name": "King of Swords", "type": "minor", "suit": "swords",
     "meaning_up": "Mental clarity; Intellectual power; Authority; Truth",
     "meaning_rev": "Manipulation; Abuse of power; Coldness"},
    {"name_short": "p01", "name": "Ace of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "New financial opportunity; Prosperity; Abundance; Security",
     "meaning_rev": "Lost opportunity; Lack of planning; Lack of foresight"},
    {"name_short": "p02", "name": "Two of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "Multiple priorities; Time management; Prioritization; Flexibility",
     "meaning_rev": "Over-committed; Disorganization; Financial instability"},
    {"name_short": "p03", "name": "Three of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "Teamwork; Collaboration; Learning; Implementation",
     "meaning_rev": "Disharmony; Misalignment; Lack of skills"},
    {"name_short": "p04", "name": "Four of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "Saving; Security; Conservatism; Scarcity; Control",
     "meaning_rev": "Over-spending; Generosity; Letting go of control"},
    {"name_short": "p05", "name": "Five of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "Financial loss; Poverty; Lack mindset; Isolation; Worry",
     "meaning_rev": "Recovery from loss; Spiritual poverty ended; Help arrives"},
    {"name_short": "p06", "name": "Six of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "Giving; Receiving; Sharing wealth; Generosity; Charity",
     "meaning_rev": "Self-care needed; Strings attached; Debts; Hoarding"},
    {"name_short": "p07", "name": "Seven of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "Long-term view; Sustainable results; Perseverance; Investment",
     "meaning_rev": "Lack of long-term vision; Limited success; Impatience"},
    {"name_short": "p08", "name": "Eight of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "Apprenticeship; Repetitive tasks; Mastery; Skill development",
     "meaning_rev": "Self-development; Perfectionism; Misdirected activity"},
    {"name_short": "p09", "name": "Nine of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "Abundance; Luxury; Self-sufficiency; Financial independence",
     "meaning_rev": "Self-worth issues; Overinvestment; Overthinking"},
    {"name_short": "p10", "name": "Ten of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "Wealth; Financial security; Family; Long-term success; Inheritance",
     "meaning_rev": "Financial failure; Loneliness; Family disputes"},
    {"name_short": "p11", "name": "Page of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "Manifestation; Financial opportunity; Skill development; Studious",
     "meaning_rev": "Lack of progress; Procrastination; Learn from setbacks"},
    {"name_short": "p12", "name": "Knight of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "Hard work; Productivity; Routine; Conservatism; Service",
     "meaning_rev": "Self-discipline needed; Laziness; Boredom"},
    {"name_short": "p13", "name": "Queen of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "Nurturing; Abundance; Practical; Comfortable; Down-to-earth",
     "meaning_rev": "Financial independence threatened; Self-care neglected"},
    {"name_short": "p14", "name": "King of Pentacles", "type": "minor", "suit": "pentacles",
     "meaning_up": "Wealth; Business; Leadership; Security; Discipline; Abundance",
     "meaning_rev": "Financially inept; Obsessed with money; Stubborn"},
]


class TarotAPIClient:
    _cache: Optional[list[dict]] = None
    _cache_lock = asyncio.Lock()

    @classmethod
    async def fetch_all_cards(cls) -> list[dict]:
        if cls._cache:
            return cls._cache

        async with cls._cache_lock:
            if cls._cache:
                return cls._cache

            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(CARDS_JSON_URL)
                    response.raise_for_status()
                    remote_cards = response.json()
                    if remote_cards:
                        merged = []
                        for rc in remote_cards:
                            name = rc.get("name", "")
                            image_code = NAME_TO_IMAGE.get(name)
                            merged.append({
                                "name": name,
                                "name_short": image_code or "",
                                "image": rc.get("image", ""),
                                "type": "major" if image_code and image_code.startswith("ar") else "minor",
                                "suit": cls._suit_from_code(image_code),
                                "meaning_up": "",
                                "meaning_rev": "",
                            })
                        cls._cache = merged
                        return cls._cache
            except Exception:
                pass

            cls._cache = list(BUILTIN_CARDS)
            return cls._cache

    @staticmethod
    def _suit_from_code(code: str | None) -> str:
        if not code:
            return ""
        prefix_map = {"wa": "wands", "cu": "cups", "sw": "swords", "pe": "pentacles"}
        return prefix_map.get(code[:2], "")

    @classmethod
    async def fetch_card_by_name(cls, card_name: str) -> Optional[dict]:
        cards = await cls.fetch_all_cards()
        card_name_lower = card_name.lower().replace(" ", "-")
        for card in cards:
            if card.get("name", "").lower().replace(" ", "-") == card_name_lower:
                return card
        return None

    @classmethod
    async def fetch_random_cards(cls, count: int = 3) -> list[dict]:
        import random
        cards = await cls.fetch_all_cards()
        return random.sample(cards, min(count, len(cards)))

    @classmethod
    def extract_keywords(cls, card: dict) -> list[str]:
        meaning_up = card.get("meaning_up", "")
        if not meaning_up:
            return []
        keywords = []
        parts = meaning_up.split(";")
        for part in parts:
            part = part.strip()
            if part:
                first_keyword = part.split(",")[0].strip()
                if first_keyword:
                    keywords.append(first_keyword)
        return keywords[:3]

    @classmethod
    def get_card_image_url(cls, card_name: str) -> str:
        code = NAME_TO_IMAGE.get(card_name)
        if code:
            return f"{IMAGES_BASE_URL}/{code}.jpg"
        return CARD_BACK_URL

    @classmethod
    def get_card_back_url(cls) -> str:
        return CARD_BACK_URL
