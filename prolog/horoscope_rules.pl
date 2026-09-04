% ============================================================
% Horoscope Rules - AstroLogic
% Rules for generating horoscope themes and guidance
% ============================================================

:- use_module(zodiac).
:- use_module(tarot).

% --- Daily Theme Generation ---
daily_theme(aries, Theme) :-
    member(Theme, [action, courage, new_beginnings, leadership, independence]).
daily_theme(taurus, Theme) :-
    member(Theme, [stability, patience, enjoyment, building, sensuality]).
daily_theme(gemini, Theme) :-
    member(Theme, [communication, curiosity, learning, socializing, versatility]).
daily_theme(cancer, Theme) :-
    member(Theme, [nurturing, home, emotions, intuition, care]).
daily_theme(leo, Theme) :-
    member(Theme, [creativity, joy, self_expression, warmth, generosity]).
daily_theme(virgo, Theme) :-
    member(Theme, [improvement, health, service, organization, detail]).
daily_theme(libra, Theme) :-
    member(Theme, [balance, harmony, relationships, beauty, fairness]).
daily_theme(scorpio, Theme) :-
    member(Theme, [transformation, depth, passion, mystery, intensity]).
daily_theme(sagittarius, Theme) :-
    member(Theme, [adventure, freedom, philosophy, optimism, expansion]).
daily_theme(capricorn, Theme) :-
    member(Theme, [ambition, discipline, achievement, responsibility, structure]).
daily_theme(aquarius, Theme) :-
    member(Theme, [innovation, originality, humanity, independence, vision]).
daily_theme(pisces, Theme) :-
    member(Theme, [intuition, spirituality, compassion, imagination, dreams]).

% --- Element-Based Mood Influence ---
element_mood(fire, energetic).
element_mood(fire, passionate).
element_mood(fire, confident).
element_mood(earth, grounded).
element_mood(earth, practical).
element_mood(earth, stable).
element_mood(air, communicative).
element_mood(air, social).
element_mood(air, intellectual).
element_mood(water, intuitive).
element_mood(water, emotional).
element_mood(water, reflective).

% --- Horoscope Focus Areas ---
focus_area(Sign, Focus) :-
    element(Sign, fire),
    member(Focus, [career_bold_moves, creative_expression, physical_activity]).

focus_area(Sign, Focus) :-
    element(Sign, earth),
    member(Focus, [financial_planning, health_routines, practical_matters]).

focus_area(Sign, Focus) :-
    element(Sign, air),
    member(Focus, [social_connections, learning_new_things, communication]).

focus_area(Sign, Focus) :-
    element(Sign, water),
    member(Focus, [emotional_reflection, relationships, spiritual_practice]).

% --- Mood to Theme Mapping ---
mood_theme(happy, Theme) :-
    member(Theme, [celebration, gratitude, sharing, creativity]).
mood_theme(calm, Theme) :-
    member(Theme, [reflection, meditation, peace, balance]).
mood_theme(uncertain, Theme) :-
    member(Theme, [guidance, clarity, patience, inner_wisdom]).
mood_theme(stressed, Theme) :-
    member(Theme, [relief, self_care, boundaries, grounding]).
mood_theme(excited, Theme) :-
    member(Theme, [opportunity, action, growth, adventure]).
mood_theme(frustrated, Theme) :-
    member(Theme, [release, perspective, acceptance, new_approach]).
mood_theme(curious, Theme) :-
    member(Theme, [exploration, learning, discovery, openness]).
mood_theme(reflective, Theme) :-
    member(Theme, [introspection, wisdom, understanding, growth]).
mood_theme(neutral, Theme) :-
    member(Theme, [balance, awareness, presence, appreciation]).

% --- Horoscope Guidance Generation ---
horoscope_guidance(Sign, Mood, Guidance) :-
    element(Sign, Element),
    modality(Sign, Modality),
    daily_theme(Sign, Theme),
    mood_theme(Mood, MoodTheme),
    focus_area(Sign, Focus),
    Guidance = horoscope{
        sign: Sign,
        element: Element,
        modality: Modality,
        theme: Theme,
        mood: Mood,
        mood_theme: MoodTheme,
        focus: Focus
    }.

% --- Mood Classification from Text ---
classify_mood(Input, Mood) :-
    (   sub_string(Input, _, _, _, 'happy')
    ->  Mood = happy
    ;   sub_string(Input, _, _, _, 'excited')
    ->  Mood = excited
    ;   sub_string(Input, _, _, _, 'stressed')
    ->  Mood = stressed
    ;   sub_string(Input, _, _, _, 'worried')
    ->  Mood = uncertain
    ;   sub_string(Input, _, _, _, 'confused')
    ->  Mood = uncertain
    ;   sub_string(Input, _, _, _, 'calm')
    ->  Mood = calm
    ;   sub_string(Input, _, _, _, 'curious')
    ->  Mood = curious
    ;   sub_string(Input, _, _, _, 'reflective')
    ->  Mood = reflective
    ;   Mood = neutral
    ).

% --- Reasoning Trace for Horoscope ---
generate_horoscope_trace(Sign, Mood, Trace) :-
    element(Sign, Element),
    modality(Sign, Modality),
    daily_theme(Sign, Theme),
    mood_theme(Mood, MoodTheme),
    focus_area(Sign, Focus),
    Trace = [
        trace_step{rule: zodiac_rule(Sign), result: 'User zodiac sign identified'},
        trace_step{rule: element_rule(Sign, Element), result: 'Element association determined'},
        trace_step{rule: modality_rule(Sign, Modality), result: 'Modality determined'},
        trace_step{rule: theme_rule(Sign, Theme), result: 'Daily theme selected'},
        trace_step{rule: mood_rule(Mood, MoodTheme), result: 'Mood-based theme determined'},
        trace_step{rule: focus_rule(Sign, Focus), result: 'Focus area identified'}
    ].
