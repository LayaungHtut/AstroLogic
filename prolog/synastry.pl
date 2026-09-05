% ============================================================
% Synastry & Compatibility Functions - AstroLogic
% Module 4: Compatibility & Synastry
%
% Handles symbolic relationship compatibility analysis.
% This is entertainment/self-reflection and must be presented
% as symbolic rather than scientifically validated.
% ============================================================

:- use_module(zodiac).
:- use_module(zodiac_profile).
:- use_module(card_selection).

% ============================================================
% SECTION 1: Basic Zodiac Compatibility
% ============================================================

% --- zodiac_compatibility/3 ---
% Derive compatibility from element, modality, and traits.
% NOT a single hardcoded table - computed from multiple factors.

zodiac_compatibility(Sign1, Sign2, Result) :-
    Sign1 \= Sign2,
    element(Sign1, E1),
    element(Sign2, E2),
    modality(Sign1, M1),
    modality(Sign2, M2),
    ruling_planet(Sign1, P1),
    ruling_planet(Sign2, P2),
    element_compatibility_score(E1, E2, EScore),
    modality_compatibility_score(M1, M2, MScore),
    trait_compatibility_score(Sign1, Sign2, TScore),
    planetary_compatibility_score(P1, P2, PScore),
    OverallScore is (EScore * 0.35) + (MScore * 0.20) + (TScore * 0.30) + (PScore * 0.15),
    (   OverallScore >= 75
    ->  Level = high
    ;   OverallScore >= 50
    ->  Level = moderate
    ;   Level = low
    ),
    Result = compatibility_result{
        sign1: Sign1,
        sign2: Sign2,
        level: Level,
        score: OverallScore,
        element_score: EScore,
        modality_score: MScore,
        trait_score: TScore,
        planetary_score: PScore
    }.

% ============================================================
% SECTION 2: Element Compatibility Scoring
% ============================================================

element_compatibility_score(fire, fire, 90) :- !.
element_compatibility_score(fire, air, 85) :- !.
element_compatibility_score(air, fire, 85) :- !.
element_compatibility_score(air, air, 80) :- !.
element_compatibility_score(earth, earth, 85) :- !.
element_compatibility_score(earth, water, 88) :- !.
element_compatibility_score(water, earth, 88) :- !.
element_compatibility_score(water, water, 82) :- !.
element_compatibility_score(fire, earth, 55) :- !.
element_compatibility_score(earth, fire, 55) :- !.
element_compatibility_score(fire, water, 40) :- !.
element_compatibility_score(water, fire, 40) :- !.
element_compatibility_score(air, earth, 50) :- !.
element_compatibility_score(earth, air, 50) :- !.
element_compatibility_score(air, water, 55) :- !.
element_compatibility_score(water, air, 55) :- !.

% ============================================================
% SECTION 3: Modality Compatibility Scoring
% ============================================================

modality_compatibility_score(cardinal, cardinal, 55) :- !.
modality_compatibility_score(cardinal, fixed, 80) :- !.
modality_compatibility_score(cardinal, mutable, 75) :- !.
modality_compatibility_score(fixed, cardinal, 80) :- !.
modality_compatibility_score(fixed, fixed, 50) :- !.
modality_compatibility_score(fixed, mutable, 65) :- !.
modality_compatibility_score(mutable, cardinal, 75) :- !.
modality_compatibility_score(mutable, fixed, 65) :- !.
modality_compatibility_score(mutable, mutable, 70) :- !.

% ============================================================
% SECTION 4: Trait Compatibility Scoring
% ============================================================
% Compare symbolic traits of two signs.

trait_compatibility_score(Sign1, Sign2, Score) :-
    zodiac_traits(Sign1, Traits1),
    zodiac_traits(Sign2, Traits2),
    findall(1, (member(T, Traits1), member(T, Traits2)), MatchingTraits),
    length(MatchingTraits, MatchCount),
    findall(1, (member(T, Traits1), trait_complementary(T, CT), member(CT, Traits2)), ComplementaryTraits),
    length(ComplementaryTraits, CompCount),
    TotalFactors is MatchCount * 10 + CompCount * 5,
    Score is min(100, 40 + TotalFactors).

% --- trait_complementary/2 ---
% Traits that complement each other.

trait_complementary(initiative, patience).
trait_complementary(patience, initiative).
trait_complementary(courage, sensitivity).
trait_complementary(sensitivity, courage).
trait_complementary(leadership, adaptability).
trait_complementary(adaptability, leadership).
trait_complementary(determination, flexibility).
trait_complementary(flexibility, determination).
trait_complementary(independence, nurturing).
trait_complementary(nurturing, independence).
trait_complementary(curiosity, reliability).
trait_complementary(reliability, curiosity).
trait_complementary(confidence, diplomacy).
trait_complementary(diplomacy, confidence).
trait_complementary(creativity, practicality).
trait_complementary(practicality, creativity).
trait_complementary(intensity, warmth).
trait_complementary(warmth, intensity).
trait_complementary(adventure, stability).
trait_complementary(stability, adventure).
trait_complementary(optimism, realism).
trait_complementary(realism, optimism).
trait_complementary(originality, tradition).
trait_complementary(tradition, originality).
trait_complementary(compassion, discipline).
trait_complementary(discipline, compassion).

% ============================================================
% SECTION 5: Planetary Compatibility
% ============================================================

planetary_compatibility_score(Mars, Venus, 80) :- !.   % Passion meets beauty
planetary_compatibility_score(Venus, Mars, 80) :- !.
planetary_compatibility_score(Sun, Moon, 85) :- !.    % Classic complementary pair
planetary_compatibility_score(Moon, Sun, 85) :- !.
planetary_compatibility_score(Mercury, Mercury, 70) :- !.  % Communication match
planetary_compatibility_score(Jupiter, Saturn, 75) :- !.   % Expansion meets structure
planetary_compatibility_score(Saturn, Jupiter, 75) :- !.
planetary_compatibility_score(Uranus, Pluto, 70) :- !.     % Transformation energy
planetary_compatibility_score(Pluto, Uranus, 70) :- !.
planetary_compatibility_score(Neptune, Venus, 78) :- !.    % Spiritual love
planetary_compatibility_score(Venus, Neptune, 78) :- !.
planetary_compatibility_score(_, _, 55).  % Default for unlisted combinations

% ============================================================
% SECTION 6: Element Compatibility Description
% ============================================================

element_relationship_description(fire, fire, 'Both share passionate, dynamic energy. Your combined fire creates warmth and drive, though watch for potential flare-ups when egos clash.').
element_relationship_description(fire, air, 'Air feeds Fire, creating a stimulating connection. Air brings ideas and communication while Fire brings action and enthusiasm. A naturally supportive pairing.').
element_relationship_description(air, fire, 'Air feeds Fire, creating a stimulating connection. Air brings ideas and communication while Fire brings action and enthusiasm. A naturally supportive pairing.').
element_relationship_description(air, air, 'Both share intellectual curiosity and love of conversation. Your minds connect naturally, though you may both benefit from grounding activities together.').
element_relationship_description(earth, earth, 'Both value stability, practicality, and tangible results. Your connection is built on shared values and mutual respect for reliability. A solid foundation.').
element_relationship_description(earth, water, 'Water nourishes Earth, creating a deeply supportive bond. Water brings emotional depth while Earth provides structure and security. Naturally complementary.').
element_relationship_description(water, earth, 'Water nourishes Earth, creating a deeply supportive bond. Water brings emotional depth while Earth provides structure and security. Naturally complementary.').
element_relationship_description(water, water, 'Both share deep emotional sensitivity and intuition. Your connection runs deep, though maintaining individual emotional boundaries helps sustain balance.').
element_relationship_description(fire, earth, 'Fire and Earth have different tempos - Fire acts on impulse while Earth builds steadily. With patience, you can learn much from each other different approaches.').
element_relationship_description(earth, fire, 'Fire and Earth have different tempos - Fire acts on impulse while Earth builds steadily. With patience, you can learn much from each other different approaches.').
element_relationship_description(fire, water, 'Fire and Water create steam - a powerful but potentially volatile combination. Fire brings passion while Water brings depth. Understanding and patience are key.').
element_relationship_description(water, fire, 'Fire and Water create steam - a powerful but potentially volatile combination. Fire brings passion while Water brings depth. Understanding and patience are key.').
element_relationship_description(air, earth, 'Earth and Air can be challenging - Earth values the concrete while Air values ideas. Finding common ground requires appreciation of different perspectives.').
element_relationship_description(earth, air, 'Earth and Air can be challenging - Earth values the concrete while Air values ideas. Finding common ground requires appreciation of different perspectives.').
element_relationship_description(air, water, 'Air and Water operate differently - Air thinks while Water feels. With effort, you can create a balance of mind and heart.').
element_relationship_description(water, air, 'Air and Water operate differently - Air thinks while Water feels. With effort, you can create a balance of mind and heart.').

% ============================================================
% SECTION 7: Synastry Analysis
% ============================================================

% --- synastry/3 ---
% Full synastry analysis between two profiles.

synastry(Sign1, Sign2, Analysis) :-
    Sign1 \= Sign2,
    zodiac_profile(Sign1, Profile1),
    zodiac_profile(Sign2, Profile2),
    element(Sign1, E1),
    element(Sign2, E2),
    modality(Sign1, M1),
    modality(Sign2, M2),
    ruling_planet(Sign1, P1),
    ruling_planet(Sign2, P2),
    % Element relationship
    element_compatibility(E1, E2, ELevel),
    element_relationship_description(E1, E2, EDesc),
    % Modality relationship
    modality_compatibility(M1, M2, MLevel),
    % Overall compatibility
    zodiac_compatibility(Sign1, Sign2, CompatResult),
    % Synastry strengths
    synastry_strengths(Sign1, Sign2, Strengths),
    % Synastry challenges
    synastry_challenges(Sign1, Sign2, Challenges),
    % Communication themes
    synastry_communication(Sign1, Sign2, CommTheme),
    % Balance themes
    synastry_balance(Sign1, Sign2, BalanceTheme),
    Analysis = synastry_analysis{
        sign1: Sign1,
        sign2: Sign2,
        profile1: Profile1,
        profile2: Profile2,
        element1: E1,
        element2: E2,
        modality1: M1,
        modality2: M2,
        planet1: P1,
        planet2: P2,
        element_level: ELevel,
        element_description: EDesc,
        modality_level: MLevel,
        overall_level: CompatResult.level,
        overall_score: CompatResult.score,
        strengths: Strengths,
        challenges: Challenges,
        communication_theme: CommTheme,
        balance_theme: BalanceTheme
    }.

% --- synastry_strengths/3 ---
% Identify strengths in the pairing.

synastry_strengths(Sign1, Sign2, Strengths) :-
    element(Sign1, E1),
    element(Sign2, E2),
    modality(Sign1, M1),
    modality(Sign2, M2),
    zodiac_traits(Sign1, T1),
    zodiac_traits(Sign2, T2),
    findall(
        Strength,
        (
            % Shared traits are strengths
            (member(T, T1), member(T, T2), format(atom(Strength), 'Shared ~w', [T]))
            ;
            % Complementary elements
            (compatible_element(E1, E2), Strength = 'Elemental harmony')
            ;
            % Complementary modalities
            (compatible_modality(M1, M2), Strength = 'Approach balance')
            ;
            % Complementary traits
            (member(T, T1), trait_complementary(T, CT), member(CT, T2),
             format(atom(Strength), '~w meets ~w', [T, CT]))
        ),
        RawStrengths
    ),
    sort(RawStrengths, Strengths).

% --- synastry_challenges/3 ---
% Identify potential challenges.

synastry_challenges(Sign1, Sign2, Challenges) :-
    element(Sign1, E1),
    element(Sign2, E2),
    modality(Sign1, M1),
    modality(Sign2, M2),
    findall(
        Challenge,
        (
            % Challenging elements
            (challenging_element(E1, E2),
             Challenge = 'Different emotional energies require understanding')
            ;
            % Same modality friction
            (M1 = M2, M1 = fixed,
             Challenge = 'Both prefer stability, which can lead to stubbornness')
            ;
            (M1 = M2, M1 = cardinal,
             Challenge = 'Both want to lead, which can create competition')
        ),
        RawChallenges
    ),
    sort(RawChallenges, Challenges).

% --- synastry_communication/3 ---
% Describe communication dynamics.

synastry_communication(Sign1, Sign2, Theme) :-
    element(Sign1, E1),
    element(Sign2, E2),
    (   E1 = E2
    ->  Theme = 'You speak a similar elemental language, making natural understanding easier.'
    ;   compatible_element(E1, E2)
    ->  Theme = 'Your different perspectives complement each other, creating rich and varied conversations.'
    ;   Theme = 'Communication requires extra effort as you process information differently. Patience and active listening help bridge the gap.'
    ).

% --- synastry_balance/3 ---
% Describe balance dynamics.

synastry_balance(Sign1, Sign2, Theme) :-
    modality(Sign1, M1),
    modality(Sign2, M2),
    (   M1 = M2
    ->  Theme = 'You approach life similarly, which creates understanding but may need conscious effort to bring fresh perspectives.'
    ;   compatible_modality(M1, M2)
    ->  Theme = 'Your different approaches to life create a natural balance - one initiates while the other sustains.'
    ;   Theme = 'Your approaches differ, which can create friction but also opportunities for growth through understanding different styles.'
    ).

% ============================================================
% SECTION 8: Compatibility Explanation
% ============================================================

% --- compatibility_explanation/3 ---
% Generate a full explanation trace.

compatibility_explanation(Sign1, Sign2, Explanation) :-
    element(Sign1, E1),
    element(Sign2, E2),
    modality(Sign1, M1),
    modality(Sign2, M2),
    ruling_planet(Sign1, P1),
    ruling_planet(Sign2, P2),
    zodiac_traits(Sign1, T1),
    zodiac_traits(Sign2, T2),
    element_compatibility(E1, E2, ELevel),
    modality_compatibility(M1, M2, MLevel),
    element_relationship_description(E1, E2, EDesc),
    zodiac_compatibility(Sign1, Sign2, CompatResult),
    Explanation = explanation{
        element_analysis: explanation_part{
            input: format('~w + ~w', [E1, E2]),
            result: ELevel,
            description: EDesc
        },
        modality_analysis: explanation_part{
            input: format('~w + ~w', [M1, M2]),
            result: MLevel,
            description: format('~w modality meets ~w modality', [M1, M2])
        },
        trait_analysis: explanation_part{
            input: format('~w traits: ~w', [Sign1, T1]),
            result: format('~w traits: ~w', [Sign2, T2]),
            description: 'Comparing symbolic trait profiles for overlap and complementarity'
        },
        planetary_analysis: explanation_part{
            input: format('~w (ruled by ~w) + ~w (ruled by ~w)', [Sign1, P1, Sign2, P2]),
            result: 'Symbolic planetary relationship',
            description: 'Planetary symbolism adds another layer of compatibility insight'
        },
        overall: explanation_part{
            input: 'Combined analysis',
            result: CompatResult.level,
            description: format('~w compatibility (score: ~w/100)', [CompatResult.level, CompatResult.score])
        }
    }.

% ============================================================
% SECTION 9: Compatibility Score Breakdown
% ============================================================

% --- compatibility_score_breakdown/3 ---
% Return the individual component scores.

compatibility_score_breakdown(Sign1, Sign2, Breakdown) :-
    element(Sign1, E1),
    element(Sign2, E2),
    modality(Sign1, M1),
    modality(Sign2, M2),
    ruling_planet(Sign1, P1),
    ruling_planet(Sign2, P2),
    element_compatibility_score(E1, E2, EScore),
    modality_compatibility_score(M1, M2, MScore),
    trait_compatibility_score(Sign1, Sign2, TScore),
    planetary_compatibility_score(P1, P2, PScore),
    OverallScore is (EScore * 0.35) + (MScore * 0.20) + (TScore * 0.30) + (PScore * 0.15),
    Breakdown = score_breakdown{
        element: score_component{name: 'Element', score: EScore, weight: 0.35, description: format('~w + ~w', [E1, E2])},
        modality: score_component{name: 'Modality', score: MScore, weight: 0.20, description: format('~w + ~w', [M1, M2])},
        traits: score_component{name: 'Traits', score: TScore, weight: 0.30, description: 'Symbolic trait analysis'},
        planetary: score_component{name: 'Planetary', score: PScore, weight: 0.15, description: format('~w + ~w', [P1, P2])},
        overall: OverallScore
    }.

% ============================================================
% SECTION 10: Reasoning Trace
% ============================================================

% --- synastry_reasoning_trace/3 ---
% Generate a full reasoning trace for synastry analysis.

synastry_reasoning_trace(Sign1, Sign2, Trace) :-
    element(Sign1, E1),
    element(Sign2, E2),
    modality(Sign1, M1),
    modality(Sign2, M2),
    ruling_planet(Sign1, P1),
    ruling_planet(Sign2, P2),
    element_compatibility(E1, E2, ELevel),
    modality_compatibility(M1, M2, MLevel),
    element_relationship_description(E1, E2, EDesc),
    zodiac_compatibility(Sign1, Sign2, CompatResult),
    synastry_strengths(Sign1, Sign2, Strengths),
    synastry_challenges(Sign1, Sign2, Challenges),
    Trace = [
        reasoning_step{
            rule: format('element(~w, ~w)', [Sign1, E1]),
            input: Sign1,
            result: format('~w belongs to ~w element', [Sign1, E1]),
            explanation: 'First sign element identified'
        },
        reasoning_step{
            rule: format('element(~w, ~w)', [Sign2, E2]),
            input: Sign2,
            result: format('~w belongs to ~w element', [Sign2, E2]),
            explanation: 'Second sign element identified'
        },
        reasoning_step{
            rule: format('element_compatibility(~w, ~w, ~w)', [E1, E2, ELevel]),
            input: format('~w + ~w', [E1, E2]),
            result: format('Element relationship: ~w', [ELevel]),
            explanation: EDesc
        },
        reasoning_step{
            rule: format('modality(~w, ~w)', [Sign1, M1]),
            input: Sign1,
            result: format('~w has ~w modality', [Sign1, M1]),
            explanation: 'Modality determines approach style'
        },
        reasoning_step{
            rule: format('modality(~w, ~w)', [Sign2, M2]),
            input: Sign2,
            result: format('~w has ~w modality', [Sign2, M2]),
            explanation: 'Modality determines approach style'
        },
        reasoning_step{
            rule: format('modality_compatibility(~w, ~w, ~w)', [M1, M2, MLevel]),
            input: format('~w + ~w', [M1, M2]),
            result: format('Modality relationship: ~w', [MLevel]),
            explanation: 'Modalities show how approaches interact'
        },
        reasoning_step{
            rule: format('ruling_planet(~w, ~w)', [Sign1, P1]),
            input: Sign1,
            result: format('~w ruled by ~w', [Sign1, P1]),
            explanation: 'Ruling planet adds symbolic layer'
        },
        reasoning_step{
            rule: format('ruling_planet(~w, ~w)', [Sign2, P2]),
            input: Sign2,
            result: format('~w ruled by ~w', [Sign2, P2]),
            explanation: 'Ruling planet adds symbolic layer'
        },
        reasoning_step{
            rule: format('trait_compatibility_score(~w, ~w)', [Sign1, Sign2]),
            input: 'Trait comparison',
            result: 'Symbolic trait overlap and complementarity analyzed',
            explanation: 'Traits that match or complement each other strengthen compatibility'
        },
        reasoning_step{
            rule: format('zodiac_compatibility(~w, ~w, ~w)', [Sign1, Sign2, CompatResult.level]),
            input: 'Combined analysis',
            result: format('Overall compatibility: ~w (score: ~w/100)', [CompatResult.level, CompatResult.score]),
            explanation: 'Final symbolic compatibility derived from element, modality, traits, and planetary factors'
        },
        reasoning_step{
            rule: format('synastry_strengths(~w, ~w)', [Sign1, Sign2]),
            input: 'Strength analysis',
            result: format('~w strengths identified: ~w', [length(Strengths), Strengths]),
            explanation: 'Shared traits and complementary elements create relationship strengths'
        },
        reasoning_step{
            rule: format('synastry_challenges(~w, ~w)', [Sign1, Sign2]),
            input: 'Challenge analysis',
            result: format('~w challenges identified: ~w', [length(Challenges), Challenges]),
            explanation: 'Different approaches create areas requiring understanding and patience'
        }
    ].

% ============================================================
% SECTION 8: Trait Complementarity (Synastry Deep Dive)
% ============================================================

% --- synastry_trait_pairs/3 ---
% Find every complementary trait pairing between two signs' trait sets,
% using the trait_complementary/2 facts above (e.g. initiative <-> patience).

synastry_trait_pairs(Sign1, Sign2, Pairs) :-
    zodiac_traits(Sign1, Traits1),
    zodiac_traits(Sign2, Traits2),
    findall(
        trait_pair{trait1: T1, trait2: T2},
        (
            member(T1, Traits1),
            member(T2, Traits2),
            trait_complementary(T1, T2)
        ),
        Pairs
    ).
