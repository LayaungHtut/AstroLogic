% ============================================================
% Recommendation Rules - AstroLogic
% Rules for tarot card recommendations and interpretations
% ============================================================

:- use_module(zodiac).
:- use_module(tarot).

% --- Element-Card Affinity ---
element_card_affinity(fire, Card) :-
    tarot_card(Card, minor_arcana, wands).
element_card_affinity(earth, Card) :-
    tarot_card(Card, minor_arcana, pentacles).
element_card_affinity(air, Card) :-
    tarot_card(Card, minor_arcana, swords).
element_card_affinity(water, Card) :-
    tarot_card(Card, minor_arcana, cups).

% --- Zodiac-Card Associations ---
zodiac_card(aries, the_emperor).
zodiac_card(aries, the_chariot).
zodiac_card(aries, strength).
zodiac_card(taurus, the_empress).
zodiac_card(taurus, the_hierophant).
zodiac_card(taurus, temperance).
zodiac_card(gemini, the_lovers).
zodiac_card(gemini, the_magician).
zodiac_card(gemini, the_wheel_of_fortune).
zodiac_card(cancer, the_chariot).
zodiac_card(cancer, the_moon).
zodiac_card(cancer, the_hermit).
zodiac_card(leo, the_sun).
zodiac_card(leo, strength).
zodiac_card(leo, the_star).
zodiac_card(virgo, the_hermit).
zodiac_card(virgo, justice).
zodiac_card(virgo, temperance).
zodiac_card(libra, the_lovers).
zodiac_card(libra, justice).
zodiac_card(libra, the_wheel_of_fortune).
zodiac_card(scorpio, death).
zodiac_card(scorpio, the_hanged_man).
zodiac_card(scorpio, the_magician).
zodiac_card(sagittarius, temperance).
zodiac_card(sagittarius, the_wheel_of_fortune).
zodiac_card(sagittarius, the_sun).
zodiac_card(capricorn, the_devil).
zodiac_card(capricorn, the_tower).
zodiac_card(capricorn, the_world).
zodiac_card(aquarius, the_star).
zodiac_card(aquarius, the_hanged_man).
zodiac_card(aquarius, the_wheel_of_fortune).
zodiac_card(pisces, the_moon).
zodiac_card(pisces, the_sun).
zodiac_card(pisces, the_hierophant).

% --- Category-Card Affinity ---
category_card_affinity(career, Card) :-
    member(Card, [the_emperor, the_chariot, the_world, ace_of_pentacles, ten_of_pentacles]).
category_card_affinity(education, Card) :-
    member(Card, [the_magician, the_hermit, the_hierophant, ace_of_swords, page_of_swords]).
category_card_affinity(relationship, Card) :-
    member(Card, [the_lovers, two_of_cups, ten_of_cups, the_empress, queen_of_cups]).
category_card_affinity(decision, Card) :-
    member(Card, [the_hermit, justice, the_wheel_of_fortune, two_of_swords, temperance]).
category_card_affinity(self_reflection, Card) :-
    member(Card, [the_hermit, the_moon, the_high_priestess, four_of_swords, nine_of_cups]).
category_card_affinity(friendship, Card) :-
    member(Card, [three_of_cups, six_of_cups, the_lovers, four_of_wands]).
category_card_affinity(creativity, Card) :-
    member(Card, [the_magician, the_empress, ace_of_wands, page_of_wands, the_sun]).
category_card_affinity(future_planning, Card) :-
    member(Card, [wheel_of_fortune, two_of_wands, three_of_wands, the_world]).
category_card_affinity(general, Card) :-
    member(Card, [the_star, the_sun, temperance, strength]).

% --- Mood-Card Mapping ---
mood_card(happy, Card) :-
    member(Card, [the_sun, the_star, three_of_cups, six_of_cups, ten_of_cups]).
mood_card(calm, Card) :-
    member(Card, [temperance, four_of_swords, the_high_priestess, nine_of_cups]).
mood_card(uncertain, Card) :-
    member(Card, [the_hermit, two_of_swords, justice, the_wheel_of_fortune]).
mood_card(stressed, Card) :-
    member(Card, [four_of_swords, the_star, temperance, eight_of_cups]).
mood_card(excited, Card) :-
    member(Card, [the_chariot, ace_of_wands, the_sun, six_of_wands]).
mood_card(frustrated, Card) :-
    member(Card, [the_tower, death, the_hanged_man, five_of_cups]).
mood_card(curious, Card) :-
    member(Card, [the_magician, the_lovers, page_of_swords, seven_of_cups]).
mood_card(reflective, Card) :-
    member(Card, [the_hermit, the_moon, four_of_swords, the_high_priestess]).
mood_card(neutral, Card) :-
    member(Card, [the_wheel_of_fortune, justice, temperance, the_world]).

% --- Card Interpretation in Context ---
interpret_card(Card, Sign, Category, Interpretation) :-
    tarot_keywords(Card, Keywords),
    (   zodiac_card(Sign, Card)
    ->  Relevance = strongly_relevant
    ;   element(Sign, Element),
        element_card_affinity(Element, Card)
    ->  Relevance = relevant
    ;   Relevance = general
    ),
    (   category_card_affinity(Category, Card)
    ->  Context_match = yes
    ;   Context_match = no
    ),
    Interpretation = card_interpretation{
        card: Card,
        keywords: Keywords,
        zodiac_relevance: Relevance,
        context_match: Context_match
    }.

% --- Card Theme Extraction ---
extract_card_themes(Cards, Themes) :-
    findall(
        Theme,
        (
            member(Card, Cards),
            tarot_themes(Card, CardThemes),
            member(Theme, CardThemes)
        ),
        AllThemes
    ),
    sort(AllThemes, Themes).

% --- Combined Reading Analysis ---
analyze_reading(Cards, Sign, Category, Analysis) :-
    extract_card_themes(Cards, Themes),
    findall(
        interp,
        (
            member(Card, Cards),
            interpret_card(Card, Sign, Category, interp)
        ),
        Interpretations
    ),
    findall(
        Card,
        (
            member(Card, Cards),
            tarot_card(Card, major_arcana, _)
        ),
        MajorCards
    ),
    length(MajorCards, MajorCount),
    length(Cards, TotalCards),
    Analysis = reading_analysis{
        cards: Cards,
        themes: Themes,
        interpretations: Interpretations,
        major_arcana_count: MajorCount,
        total_cards: TotalCards
    }.

% --- Reasoning Trace for Card Interpretation ---
generate_card_trace(Cards, Sign, Category, Trace) :-
    findall(
        trace_step{
            rule: RuleStr,
            result: ResultStr
        },
        (
            member(Card, Cards),
            (   tarot_keywords(Card, Keywords)
            ->  format(atom(RuleStr), 'tarot_keywords(~w, ~w)', [Card, Keywords]),
                format(atom(ResultStr), '~w has keywords ~w', [Card, Keywords])
            ;   true
            )
        ),
        KeywordTraces
    ),
    findall(
        trace_step{
            rule: RuleStr2,
            result: ResultStr2
        },
        (
            member(Card, Cards),
            (   zodiac_card(Sign, Card)
            ->  format(atom(RuleStr2), 'zodiac_card(~w, ~w)', [Sign, Card]),
                format(atom(ResultStr2), '~w is associated with ~w', [Card, Sign])
            ;   true
            )
        ),
        ZodiacTraces
    ),
    append(KeywordTraces, ZodiacTraces, Trace).
