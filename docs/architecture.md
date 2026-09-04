# Architecture

## System Overview

AstroLogic uses a three-tier architecture with clear separation of concerns:

```
┌───────────────────────────────────┐
│          SvelteKit 5              │
│  Frontend (TypeScript/Tailwind)   │
└───────────────┬───────────────────┘
                │ HTTP/REST
┌───────────────▼───────────────────┐
│         Python FastAPI            │
│     API + Orchestration Layer     │
└──────┬────────────────┬───────────┘
       │                │
┌──────▼──────┐  ┌──────▼──────┐
│ SWI-Prolog  │  │  OpenRouter  │
│  Reasoning  │  │     LLM     │
└──────┬──────┘  └─────────────┘
       │
┌──────▼──────┐
│   SQLite    │
│  Storage    │
└─────────────┘
```

## Design Principles

### Separation of Concerns

- **Prolog** = WHAT the system reasons (knowledge, rules, inference)
- **Python** = HOW the system orchestrates (API, NLP, coordination)
- **OpenRouter** = HOW the system expresses results (natural language)
- **SvelteKit** = HOW the user experiences it (UI, interaction)

### Data Flow

1. User input → SvelteKit → FastAPI
2. FastAPI classifies question (Python NLP)
3. Prolog receives classified data and reasons
4. Prolog returns structured symbolic results
5. FastAPI sends structured results to OpenRouter
6. OpenRouter generates natural language
7. FastAPI combines everything → SvelteKit → User

### Fallback Strategy

If OpenRouter is unavailable, the system falls back to deterministic
interpretations generated from Prolog's symbolic analysis.

## Components

### Frontend (SvelteKit 5)

- Pages: Dashboard, Zodiac, Tarot, Reading, Horoscope, Compatibility, Chat, History, Analytics, About
- Components: TarotCard, ZodiacBadge, ElementBadge, ReasoningStep, LoadingSpinner, StarField, Navigation
- Stores: Profile, Reading, Chat, Loading
- API client with error handling

### Backend (FastAPI)

- API routes for all endpoints
- Services: Prolog, OpenRouter, Tarot, Horoscope, Analytics
- SQLite database for persistence
- Pydantic schemas for validation

### Prolog Knowledge Base

- `zodiac.pl` - 12 signs, elements, modalities, planets, traits
- `tarot.pl` - 78 cards, keywords, meanings, themes
- `compatibility.pl` - Element and modality compatibility
- `horoscope_rules.pl` - Mood and theme mapping
- `spread_rules.pl` - Question classification and spread recommendation
- `recommendation_rules.pl` - Card recommendations and interpretations
- `reasoning.pl` - Orchestrates all reasoning
- `main.pl` - Entry point and helper queries
