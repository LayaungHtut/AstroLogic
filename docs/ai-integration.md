# AI Integration

## Overview

AstroLogic uses OpenRouter as the LLM provider for natural language generation. The AI is never responsible for core reasoning - it receives structured facts from Prolog and generates human-readable interpretations.

## Architecture

```
User Question
    ↓
Python NLP (question classification)
    ↓
Prolog (symbolic reasoning)
    ↓
Structured Facts (zodiac, element, spread, cards, themes)
    ↓
OpenRouter (LLM natural language interpretation)
    ↓
Final Reading (displayed in frontend)
```

## Integration Points

### 1. Tarot Reading Interpretation

Prolog provides:
- Question category
- Recommended spread
- Card keywords and themes
- Zodiac-element associations

OpenRouter generates:
- Narrative interpretation connecting cards to the question
- Reflective guidance based on themes
- Symbolic analysis of card combinations

### 2. Horoscope Generation

Prolog provides:
- Zodiac sign traits
- Element and modality
- Daily theme
- Mood-based theme
- Focus area

OpenRouter generates:
- Today's Theme (one sentence)
- Guidance (reflective advice)
- Reflection (thought-provoking question)
- Opportunity (something to look for)
- Caution (something to be mindful of)

### 3. AI Chat Assistant

The chatbot receives:
- User's zodiac sign
- Current reading context (if any)
- Chat history (last 10 messages)

Prolog facts are included in the system prompt for context.

## Fallback Strategy

When OpenRouter is unavailable:

1. Tarot readings use Prolog-derived fallback interpretations
2. Horoscopes use template-based generation from Prolog themes
3. Chat returns a graceful error message

## Prompt Design

The system prompt enforces:
- No claims of scientific prediction
- No medical/health diagnosis
- Reflective entertainment framing
- Symbolic interpretation focus
- Use of Prolog-derived themes

## Environment Variables

```env
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=openai/gpt-3.5-turbo
```

## Error Handling

- API timeout: 30 seconds
- Rate limiting: Handled gracefully
- Invalid responses: Fallback to deterministic output
- Network errors: Graceful degradation
