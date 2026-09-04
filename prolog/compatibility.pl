% ============================================================
% Compatibility Rules - AstroLogic
% Zodiac compatibility reasoning
% ============================================================

:- use_module(zodiac).
:- use_module(tarot).

% --- Element Compatibility ---
compatible_element(fire, fire).
compatible_element(fire, air).
compatible_element(air, fire).
compatible_element(air, air).
compatible_element(earth, earth).
compatible_element(earth, water).
compatible_element(water, earth).
compatible_element(water, water).

% --- Element Incompatibility (challenging pairs) ---
challenging_element(fire, water).
challenging_element(water, fire).
challenging_element(earth, air).
challenging_element(air, earth).

% --- Modality Compatibility ---
compatible_modality(cardinal, fixed).
compatible_modality(fixed, cardinal).
compatible_modality(fixed, fixed).
compatible_modality(mutable, cardinal).
compatible_modality(cardinal, mutable).
compatible_modality(mutable, mutable).

% --- Element Relationship Descriptions ---
element_relationship(fire, fire, 'Both share passionate, dynamic energy. Your combined fire can create tremendous warmth and drive, though be mindful of potential for explosive disagreements.').
element_relationship(fire, air, 'Air feeds Fire, creating a stimulating and dynamic connection. Air brings ideas and communication while Fire brings action and enthusiasm.').
element_relationship(air, fire, 'Air feeds Fire, creating a stimulating and dynamic connection. Air brings ideas and communication while Fire brings action and enthusiasm.').
element_relationship(air, air, 'Both share intellectual curiosity and love of communication. Your minds connect naturally, though you may both benefit from grounding activities together.').
element_relationship(earth, earth, 'Both value stability, practicality, and tangible results. Your connection is built on shared values and mutual respect for reliability.').
element_relationship(earth, water, 'Water nourishes Earth, creating a deeply supportive and nurturing bond. Water brings emotional depth while Earth provides stability.').
element_relationship(water, earth, 'Water nourishes Earth, creating a deeply supportive and nurturing bond. Water brings emotional depth while Earth provides stability.').
element_relationship(water, water, 'Both share deep emotional sensitivity and intuition. Your emotional connection runs deep, though you may need to maintain individual emotional boundaries.').
element_relationship(fire, water, 'Fire and Water can create steam - a powerful but potentially volatile combination. Fire brings passion while Water brings depth, requiring mutual understanding.').
element_relationship(water, fire, 'Fire and Water can create steam - a powerful but potentially volatile combination. Fire brings passion while Water brings depth, requiring mutual understanding.').
element_relationship(earth, air, 'Earth and Air can be challenging - Earth values the concrete while Air values ideas. Finding common ground requires patience and appreciation of differences.').
element_relationship(air, earth, 'Earth and Air can be challenging - Earth values the concrete while Air values ideas. Finding common ground requires patience and appreciation of differences.').

% --- Overall Compatibility Scoring ---
zodiac_compatibility(Sign1, Sign2, high) :-
    Sign1 \= Sign2,
    element(Sign1, E),
    element(Sign2, E),
    modality(Sign1, M1),
    modality(Sign2, M2),
    compatible_modality(M1, M2).

zodiac_compatibility(Sign1, Sign2, high) :-
    Sign1 \= Sign2,
    element(Sign1, E1),
    element(Sign2, E2),
    compatible_element(E1, E2),
    E1 \= E2.

zodiac_compatibility(Sign1, Sign2, medium) :-
    Sign1 \= Sign2,
    element(Sign1, E1),
    element(Sign2, E2),
    compatible_element(E1, E2).

zodiac_compatibility(Sign1, Sign2, medium) :-
    Sign1 \= Sign2,
    modality(Sign1, M1),
    modality(Sign2, M2),
    compatible_modality(M1, M2).

zodiac_compatibility(Sign1, Sign2, low) :-
    Sign1 \= Sign2,
    element(Sign1, E1),
    element(Sign2, E2),
    challenging_element(E1, E2).

% --- Ruling Planet Relationships ---
planet_relationship(mars, venus, complementary).
planet_relationship(mars, jupiter, supportive).
planet_relationship(venus, neptune, harmonious).
planet_relationship(mercury, uranus, innovative).
planet_relationship(moon, sun, complementary).
planet_relationship(saturn, uranus, transformative).
planet_relationship(jupiter, neptune, spiritual).
planet_relationship(pluto, moon, deep).

% --- Detailed Compatibility Analysis ---
compatibility_analysis(Sign1, Sign2, Analysis) :-
    Sign1 \= Sign2,
    element(Sign1, E1),
    element(Sign2, E2),
    modality(Sign1, M1),
    modality(Sign2, M2),
    ruling_planet(Sign1, P1),
    ruling_planet(Sign2, P2),
    zodiac_compatibility(Sign1, Sign2, Level),
    element_relationship(E1, E2, ElementDesc),
    Analysis = compatibility{
        sign1: Sign1,
        sign2: Sign2,
        element1: E1,
        element2: E2,
        modality1: M1,
        modality2: M2,
        planet1: P1,
        planet2: P2,
        level: Level,
        element_description: ElementDesc
    }.

% --- Reasoning Trace Generation ---
generate_compatibility_trace(Sign1, Sign2, Trace) :-
    Sign1 \= Sign2,
    element(Sign1, E1),
    element(Sign2, E2),
    modality(Sign1, M1),
    modality(Sign2, M2),
    ruling_planet(Sign1, P1),
    ruling_planet(Sign2, P2),
    zodiac_compatibility(Sign1, Sign2, Level),
    element_relationship(E1, E2, ElementDesc),
    findall(
        trace_step{rule: RuleStr, result: ResultStr},
        (
            (   member(step, [
                step(element_rule(Sign1, E1), 'element of Sign1'),
                step(element_rule(Sign2, E2), 'element of Sign2'),
                step(modality_rule(Sign1, M1), 'modality of Sign1'),
                step(modality_rule(Sign2, M2), 'modality of Sign2'),
                step(planet_rule(Sign1, P1), 'ruling planet of Sign1'),
                step(planet_rule(Sign2, P2), 'ruling planet of Sign2'),
                step(compatibility_result(Level), 'overall compatibility level')
            ])
            )
        ),
        Trace
    ).
