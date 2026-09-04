% ============================================================
% Reasoning Engine - AstroLogic
% Core reasoning engine that orchestrates Prolog inference
% ============================================================

:- use_module(zodiac).
:- use_module(tarot).
:- use_module(compatibility).
:- use_module(horoscope_rules).
:- use_module(spread_rules).
:- use_module(recommendation_rules).

% --- Main Reasoning Predicate ---
% Full reasoning trace for a tarot reading
full_reading_reasoning(Input, Sign, ReasoningResult) :-
    question_category(Input, Category),
    recommended_spread(Category, SpreadType),
    spread(SpreadType, SpreadName, SpreadDesc, CardCount),
    spread_positions(SpreadType, Positions),
    element(Sign, Element),
    modality(Sign, Modality),
    ruling_planet(Sign, Planet),
    zodiac_traits(Sign, Traits),
    ReasoningResult = reasoning_result{
        zodiac: Sign,
        element: Element,
        modality: Modality,
        ruling_planet: Planet,
        traits: Traits,
        question: Input,
        category: Category,
        spread_type: SpreadType,
        spread_name: SpreadName,
        spread_description: SpreadDesc,
        card_count: CardCount,
        positions: Positions
    }.

% --- Generate Complete Reasoning Trace ---
generate_full_trace(Input, Sign, Trace) :-
    question_category(Input, Category),
    recommended_spread(Category, SpreadType),
    spread(SpreadType, SpreadName, _, _),
    element(Sign, Element),
    modality(Sign, Modality),
    ruling_planet(Sign, Planet),
    zodiac_traits(Sign, Traits),
    element_position_emphasis(Element, Emphasis),
    Trace = [
        trace_step{
            rule: format('zodiac(~w)', [Sign]),
            result: 'User zodiac sign identified'
        },
        trace_step{
            rule: format('element(~w, ~w)', [Sign, Element]),
            result: format('~w belongs to ~w element', [Sign, Element])
        },
        trace_step{
            rule: format('modality(~w, ~w)', [Sign, Modality]),
            result: format('~w has ~w modality', [Sign, Modality])
        },
        trace_step{
            rule: format('ruling_planet(~w, ~w)', [Sign, Planet]),
            result: format('~w is ruled by ~w', [Sign, Planet])
        },
        trace_step{
            rule: format('zodiac_traits(~w, ~w)', [Sign, Traits]),
            result: format('~w symbolic traits: ~w', [Sign, Traits])
        },
        trace_step{
            rule: format('question_category(~w, ~w)', [Input, Category]),
            result: format('Question classified as: ~w', [Category])
        },
        trace_step{
            rule: format('recommended_spread(~w, ~w)', [Category, SpreadType]),
            result: format('~w questions use ~w spread', [Category, SpreadName])
        },
        trace_step{
            rule: format('element_position_emphasis(~w, ~w)', [Element, Emphasis]),
            result: format('~w element emphasizes ~w', [Element, Emphasis])
        }
    ].

% --- Get Relevant Facts for AI ---
get_relevant_facts(Sign, Category, Facts) :-
    element(Sign, Element),
    modality(Sign, Modality),
    ruling_planet(Sign, Planet),
    zodiac_traits(Sign, Traits),
    recommended_spread(Category, SpreadType),
    spread(SpreadType, _, _, CardCount),
    Facts = facts{
        zodiac: Sign,
        element: Element,
        modality: Modality,
        ruling_planet: Planet,
        traits: Traits,
        category: Category,
        spread_type: SpreadType,
        card_count: CardCount
    }.

% --- Compatibility Reasoning ---
full_compatibility_reasoning(Sign1, Sign2, Result) :-
    compatibility_analysis(Sign1, Sign2, Analysis),
    generate_compatibility_trace(Sign1, Sign2, Trace),
    Result = compatibility_result{
        analysis: Analysis,
        trace: Trace
    }.

% --- Horoscope Reasoning ---
full_horoscope_reasoning(Sign, Mood, Result) :-
    horoscope_guidance(Sign, Mood, Guidance),
    generate_horoscope_trace(Sign, Mood, Trace),
    Result = horoscope_result{
        guidance: Guidance,
        trace: Trace
    }.

% --- Spread Reasoning ---
full_spread_reasoning(Input, Sign, Result) :-
    spread_recommendation(Input, Sign, Recommendation),
    generate_spread_trace(Input, Sign, Trace),
    Result = spread_result{
        recommendation: Recommendation,
        trace: Trace
    }.

% --- Card Interpretation Reasoning ---
full_card_reasoning(Cards, Sign, Category, Result) :-
    analyze_reading(Cards, Sign, Category, Analysis),
    generate_card_trace(Cards, Sign, Category, Trace),
    Result = card_result{
        analysis: Analysis,
        trace: Trace
    }.

% --- Question Classification Entry Point ---
classify_and_recommend(Input, Sign, ClassificationResult) :-
    question_category(Input, Category),
    spread_recommendation(Input, Sign, SpreadRec),
    ClassificationResult = classification_result{
        input: Input,
        category: Category,
        spread_recommendation: SpreadRec
    }.
