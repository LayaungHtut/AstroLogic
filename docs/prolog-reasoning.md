# Prolog Reasoning

## Overview

SWI-Prolog serves as the symbolic reasoning engine for AstroLogic. It is organized around **four major functional modules**, each providing meaningful predicates with rules and inference. Prolog determines WHAT the system reasons - Python orchestrates HOW, and the LLM expresses results.

## Module Architecture

```
┌──────────────────────────────────────────────────┐
│                PROLOG MODULES                    │
├──────────────────────────────────────────────────┤
│                                                  │
│  Module 1: Zodiac & Chart Profile Functions      │
│  zodiac_profile.pl                               │
│                                                  │
│  Module 2: Card Selection & Spread Filtering     │
│  card_selection.pl                               │
│                                                  │
│  Module 3: Reading Analysis & Interpretation     │
│  reading_analysis.pl                             │
│                                                  │
│  Module 4: Compatibility & Synastry              │
│  synastry.pl                                     │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## Module 1: Zodiac & Chart Profile Functions

**File:** `prolog/zodiac_profile.pl`

### Core Accessors

```prolog
get_element(Sign, Element).
get_modality(Sign, Modality).
get_ruling_planet(Sign, Planet).
zodiac_traits_of(Sign, Traits).
```

### Strengths & Challenges

Derives strengths and challenges from zodiac traits via `trait_strength/2` and `trait_challenge/2`:

```prolog
zodiac_strengths(Sign, Strengths).
zodiac_challenges(Sign, Challenges).
```

### Profile Generation

```prolog
zodiac_profile(Sign, Profile).
generate_profile(Sign, Profile).
```

`generate_profile` combines:
- Base profile (element, modality, planet, traits)
- Element personality derivation (`element_personality/2`)
- Modality approach derivation (`modality_approach/2`)
- Planetary influence (`planetary_influence/2`)

### Birth Date to Zodiac

```prolog
zodiac_from_date(Month, Day, Sign).
```

Uses standard Western tropical zodiac date boundaries with cut-fail for deterministic mapping.

### Extensible Chart Profile

```prolog
chart_profile(Sign, BirthTime, BirthLocation, Chart).
```

Distinguishes "known from birth date" from "requires birth time/location":
- Known: Sun sign, element, modality, ruling planet, traits
- Requires time/location: Moon sign, Rising sign (not calculated in V1)

### Element & Modality Compatibility

```prolog
element_compatibility(E1, E2, Level).
modality_compatibility(M1, M2, Level).
```

Returns `supportive`, `moderate`, or `challenging`.

---

## Module 2: Card Selection & Spread Filtering

**File:** `prolog/card_selection.pl`

### Card Theme Classification

Every card is classified into thematic categories via `card_theme/2`:

```prolog
card_theme(the_hermit, reflection).
card_theme(the_chariot, action).
card_theme(temperance, balance).
```

### Card Filtering Rules

```prolog
card_matches_theme(Card, Theme).
card_matches_question(Card, Category).
card_matches_element(Card, Element).
card_matches_sign(Card, Sign).
card_eligible(Card, Context).
```

### Eligible Card Set Generation

```prolog
select_eligible_cards(Context, AllEligible, Filtered).
card_priority(Card, Context, Priority).
rank_cards(Cards, Context, Ranked).
```

### Spread Functions

```prolog
available_spread(Spread).
spread_positions(Spread, Positions).
spread_card_count(Spread, Count).
spread_description(Spread, Desc).
recommended_spread(Category, Spread).
filter_spreads(Context, Spreads).
filter_spreads_detailed(Context, Detailed).
```

### Card Selection for Reading

```prolog
select_cards(Sign, Category, Selection).
select_cards_reasoning(Sign, Category, Trace).
```

### Card Orientation

```prolog
card_orientation(Card, Orientation).
card_meaning(Card, Orientation, Meaning).
card_keywords_orientation(Card, Orientation, Keywords).
```

---

## Module 3: Reading Analysis & Interpretation

**File:** `prolog/reading_analysis.pl`

### Individual Card Analysis

```prolog
analyze_card(Card, Orientation, Analysis).
```

Returns keywords, themes, meaning, positive aspects, and challenging aspects.

### Position-Aware Interpretation

```prolog
interpret_card_position(Card, Position, Orientation, Interpretation).
position_meaning_modifier(Position, Context).
position_theme_emphasis(Position, Emphasis).
```

Each position (guidance, past, present, future, challenge, etc.) has a unique interpretive lens.

### Multi-Card Reading Analysis

```prolog
analyze_reading(Cards, Positions, Analysis).
analyze_reading_oriented(Cards, Positions, Orientations, Analysis).
```

Detects:
- Recurring themes
- Dominant suits
- Major/minor arcana balance
- Conflicting themes
- Complementary themes
- Dominant elements
- Overall reading direction

### Theme Detection

```prolog
reading_themes(Cards, Themes).
dominant_theme(Cards, Theme).
theme_category(Theme, Category).
```

### Conflicting Themes

```prolog
theme_conflict(Theme1, Theme2, Conflict).
reading_conflicts(Cards, Conflicts).
```

Examples: action vs patience, independence vs cooperation, change vs stability.

### Reading Summary & Advice

```prolog
reading_summary(Cards, Summary).
reading_advice(Context, Advice).
theme_based_advice(Theme, Advice).
```

### Zodiac + Tarot Interaction

```prolog
zodiac_tarot_theme(Sign, Card, Theme).
profile_reading_theme(Sign, Cards, Analysis).
```

Combines zodiac traits with card themes for deeper meaning.

---

## Module 4: Compatibility & Synastry

**File:** `prolog/synastry.pl`

### Basic Compatibility

```prolog
zodiac_compatibility(Sign1, Sign2, Result).
```

Derives score from four factors:
- Element compatibility (35% weight)
- Modality compatibility (20% weight)
- Trait compatibility (30% weight)
- Planetary symbolism (15% weight)

### Component Scoring

```prolog
element_compatibility_score(E1, E2, Score).
modality_compatibility_score(M1, M2, Score).
trait_compatibility_score(Sign1, Sign2, Score).
planetary_compatibility_score(P1, P2, Score).
```

### Trait Compatibility

```prolog
trait_complementary(Trait1, Trait2).
```

Maps complementary trait pairs (initiative+patience, courage+sensitivity, etc.)

### Synastry Analysis

```prolog
synastry(Sign1, Sign2, Analysis).
synastry_strengths(Sign1, Sign2, Strengths).
synastry_challenges(Sign1, Sign2, Challenges).
synastry_communication(Sign1, Sign2, Theme).
synastry_balance(Sign1, Sign2, Theme).
```

### Explanation & Breakdown

```prolog
compatibility_explanation(Sign1, Sign2, Explanation).
compatibility_score_breakdown(Sign1, Sign2, Breakdown).
element_relationship_description(E1, E2, Desc).
```

---

## Python API (PrologService)

All Prolog queries are encapsulated in `PrologService`:

### Module 1 Methods
```python
PrologService.get_zodiac_profile(sign)
PrologService.generate_profile(sign)
PrologService.get_element(sign)
PrologService.get_modality(sign)
PrologService.get_ruling_planet(sign)
PrologService.get_zodiac_traits(sign)
PrologService.get_zodiac_strengths(sign)
PrologService.get_zodiac_challenges(sign)
PrologService.zodiac_from_date(month, day)
PrologService.get_chart_profile(sign)
PrologService.get_element_compatibility(e1, e2)
PrologService.get_modality_compatibility(m1, m2)
PrologService.get_profile_reasoning_trace(sign)
```

### Module 2 Methods
```python
PrologService.classify_question(question)
PrologService.select_eligible_cards(sign, category)
PrologService.filter_spreads(sign, category)
PrologService.recommend_spread(question, sign)
PrologService.get_available_spreads()
PrologService.get_card_orientation_meaning(card, orientation)
PrologService.get_card_themes(card)
PrologService.get_select_cards_reasoning(sign, category)
```

### Module 3 Methods
```python
PrologService.analyze_card(card, orientation)
PrologService.interpret_card_position(card, position, orientation)
PrologService.analyze_reading(cards, positions, orientations)
PrologService.get_reading_themes(cards)
PrologService.get_dominant_theme(cards)
PrologService.get_reading_conflicts(cards)
PrologService.get_reading_summary(cards)
PrologService.get_reading_advice(category, sign)
PrologService.get_theme_based_advice(theme)
PrologService.get_zodiac_tarot_theme(sign, card)
PrologService.get_reading_analysis_trace(cards, positions)
```

### Module 4 Methods
```python
PrologService.analyze_compatibility(sign1, sign2)
PrologService.analyze_synastry(sign1, sign2)
PrologService.get_compatibility_explanation(sign1, sign2)
PrologService.get_compatibility_score_breakdown(sign1, sign2)
PrologService.get_synastry_reasoning_trace(sign1, sign2)
```

---

## Reasoning Traces

All four modules produce structured reasoning traces:

```json
[
  {
    "rule": "element(aries, fire)",
    "input": "aries",
    "result": "Aries belongs to fire element",
    "explanation": "Fire element defines personality style"
  }
]
```

The Python backend returns these to SvelteKit for visualization.

## File Reference

| File | Module | Purpose |
|------|--------|---------|
| `zodiac.pl` | Base | Zodiac facts (signs, elements, modalities, planets, traits) |
| `tarot.pl` | Base | 78-card tarot deck facts |
| `zodiac_profile.pl` | **1** | Zodiac profiles, strengths, challenges, birth date mapping |
| `card_selection.pl` | **2** | Card themes, filtering, eligibility, spreads |
| `reading_analysis.pl` | **3** | Card analysis, position interpretation, themes, conflicts |
| `synastry.pl` | **4** | Compatibility scoring, synastry, explanation |
| `horoscope_rules` | Support | Horoscope generation rules |
| `spread_rules` | Support | Spread recommendation rules |
| `recommendation_rules` | Support | Card recommendation rules |
| `reasoning` | Support | Orchestration of all modules |
| `main.pl` | Entry | Module loading and helper queries |
