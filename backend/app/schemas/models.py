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
