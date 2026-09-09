from pydantic import BaseModel, Field
from typing import Optional


class ZodiacInfo(BaseModel):
    sign: str
    element: str
    modality: str
    ruling_planet: str
    traits: list[str]
    date_range: str
    symbol: str


class TarotCardInfo(BaseModel):
    card: str
    name: str
    arcana: str
    keywords: list[str]
    upright: list[str]
    reversed: list[str]
    themes: list[str]
    is_reversed: bool = False


class DrawRequest(BaseModel):
    count: int = Field(default=3, ge=1, le=10)
    spread_type: Optional[str] = None


class DrawnCard(BaseModel):
    card: str
    name: str
    position: str
    is_reversed: bool
    keywords: list[str]
    upright_meaning: list[str]
    reversed_meaning: list[str]


class DrawResponse(BaseModel):
    cards: list[DrawnCard]
    spread_type: str
    positions: list[str]


class ReadingAnalyzeRequest(BaseModel):
    question: str = Field(max_length=500)
    zodiac_sign: str
    spread_type: Optional[str] = None
    # Only used when spread_type == "custom": how many cards to draw in an
    # open/free-form spread. Fixed spreads ignore this and use their own
    # predetermined card_count instead.
    card_count: Optional[int] = Field(default=None, ge=1, le=10)
    locale: Optional[str] = "en"


class SelectedCard(BaseModel):
    # `name` must match a tarot card's display name exactly (e.g. "The Fool",
    # "Ace of Wands") — the same `name` field GET /api/tarot returns for
    # each card, so the frontend can send back whatever the user clicked
    # in the deck grid without any extra lookup.
    name: str
    is_reversed: bool = False


class ReadingAnalyzeManualRequest(BaseModel):
    """Like ReadingAnalyzeRequest, but the seeker hand-picked specific cards
    from the deck (and optionally their orientation) instead of the app
    drawing them at random — the reading is generated from exactly those
    cards, in the order they were picked."""

    question: str = Field(max_length=500)
    zodiac_sign: str
    cards: list[SelectedCard] = Field(min_length=1, max_length=10)
    locale: Optional[str] = "en"


class ReadingGenerateRequest(BaseModel):
    question: str = Field(max_length=500)
    zodiac_sign: str
    cards: list[str]
    positions: list[str]
    orientations: list[bool]
    themes: list[str]
    reasoning: list[dict]


class ReadingResult(BaseModel):
    id: int
    question: str
    category: str
    zodiac_sign: str
    spread_type: str
    cards: list[DrawnCard]
    themes: list[str]
    reasoning: list[dict]
    ai_interpretation: str
    created_at: str


class HoroscopeRequest(BaseModel):
    zodiac_sign: str
    mood: str = "neutral"
    locale: Optional[str] = "en"


class HoroscopeResult(BaseModel):
    zodiac_sign: str
    element: str
    theme: str
    mood: str
    guidance: str
    reflection: str
    opportunity: str
    caution: str
    reasoning: list[dict]


class CompatibilityRequest(BaseModel):
    sign1: str
    sign2: str


class CompatibilityResult(BaseModel):
    sign1: str
    sign2: str
    element1: str
    element2: str
    modality1: str
    modality2: str
    level: str
    element_description: str
    reasoning: list[dict]


class ChatRequest(BaseModel):
    message: str = Field(max_length=500)
    zodiac_sign: Optional[str] = None
    current_reading: Optional[dict] = None
    locale: Optional[str] = "en"


class ChatResponse(BaseModel):
    response: str
    context_used: dict


class ProfileUpdate(BaseModel):
    nickname: Optional[str] = None
    birth_date: Optional[str] = None
    zodiac_sign: Optional[str] = None
    preferred_style: Optional[str] = None


class HistoryItem(BaseModel):
    id: int
    question: str
    category: str
    zodiac_sign: str
    spread_type: str
    cards_json: str
    themes_json: str
    ai_interpretation: str
    created_at: str


class AnalyticsResult(BaseModel):
    total_readings: int
    most_drawn_cards: list[dict]
    most_common_suit: str
    major_vs_minor: dict
    most_common_themes: list[dict]
    most_common_categories: list[dict]
    upright_vs_reversed: dict
