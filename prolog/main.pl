% ============================================================
% Main Entry Point - AstroLogic Prolog Knowledge Base
% Loads all modules and provides top-level queries
% ============================================================

:- use_module(zodiac).
:- use_module(tarot).
:- use_module(zodiac_profile).
:- use_module(card_selection).
:- use_module(reading_analysis).
:- use_module(compatibility).
:- use_module(synastry).
:- use_module(horoscope_rules).
:- use_module(spread_rules).
:- use_module(recommendation_rules).
:- use_module(reasoning).

% ============================================================
% Quick Query Helpers
% ============================================================

% Get zodiac info
zodiac_info(Sign, Info) :-
    zodiac(Sign),
    element(Sign, Element),
    modality(Sign, Modality),
    ruling_planet(Sign, Planet),
    zodiac_traits(Sign, Traits),
    zodiac_date_range(Sign, DateRange),
    zodiac_symbol(Sign, Symbol),
    Info = zodiac_info{
        sign: Sign,
        element: Element,
        modality: Modality,
        ruling_planet: Planet,
        traits: Traits,
        date_range: DateRange,
        symbol: Symbol
    }.

% Get tarot card info
tarot_info(Card, Info) :-
    tarot_card(Card, Arcana, Extra),
    card_name(Card, Name),
    tarot_keywords(Card, Keywords),
    tarot_upright(Card, Upright),
    tarot_reversed(Card, Reversed),
    (   tarot_themes(Card, Themes)
    ->  true
    ;   Themes = []
    ),
    Info = tarot_info{
        card: Card,
        name: Name,
        arcana: Arcana,
        extra: Extra,
        keywords: Keywords,
        upright: Upright,
        reversed: Reversed,
        themes: Themes
    }.

% Simple compatibility check
simple_compatibility(Sign1, Sign2, Level) :-
    zodiac_compatibility(Sign1, Sign2, Result),
    Level = Result.level.

% Get all cards
all_cards(Cards) :-
    all_tarot_cards(Cards).

% Get major arcana
all_major(Cards) :-
    major_arcana_cards(Cards).

% Get minor arcana
all_minor(Cards) :-
    minor_arcana_cards(Cards).

% Count total cards
total_card_count(Count) :-
    findall(_, tarot_card(_, _, _), Cards),
    length(Cards, Count).
