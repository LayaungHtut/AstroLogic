% ============================================================
% History Analysis - AstroLogic
% Symbolic aggregation and pattern reasoning over a user's saved
% reading history. Replaces the ad-hoc Python counting that used
% to live in analytics_service.py: every "most drawn card" /
% "major vs minor" / "recurring theme" figure below is derived by
% Prolog rules over facts, not by looping dicts in the backend.
% ============================================================

:- use_module(tarot).
:- use_module(card_selection).

% --- Card-level classification helpers -----------------------

% is_major(+Card) - true if Card is a major arcana card.
is_major(Card) :- tarot_card(Card, major_arcana, _).

% card_suit(+Card, -Suit) - the minor-arcana suit of Card, or
% `major` for a major arcana card (so every card has exactly one
% suit-or-major bucket, which keeps the counting below total).
card_suit(Card, major) :- tarot_card(Card, major_arcana, _), !.
card_suit(Card, Suit) :- tarot_card(Card, minor_arcana, Suit).

% --- Frequency counting over a flat list ----------------------
% count_occurrences(+Items, -Counts) - Counts is a list of
% Item-N pairs, one per distinct item in Items, N = how many
% times it occurs. Sorted by N descending.
count_occurrences(Items, Counts) :-
    sort(Items, Distinct),
    findall(
        N-Item,
        ( member(Item, Distinct),
          aggregate_all(count, member(Item, Items), N)
        ),
        NCountsRev
    ),
    keysort(NCountsRev, Sorted),
    reverse(Sorted, SortedDesc),
    findall(Item-N, member(N-Item, SortedDesc), Counts).

% top_n(+Counts, +N, -TopCounts) - first N of an already-sorted
% Item-Count list (fewer if the list is shorter).
top_n(Counts, N, TopCounts) :-
    length(Counts, Len),
    (   Len =< N
    ->  TopCounts = Counts
    ;   length(TopCounts, N),
        append(TopCounts, _, Counts)
    ).

% --- Whole-history aggregate analytics ------------------------
% history_analytics(+CardOrients, +Themes, +Categories, -Analytics)
%
% CardOrients is a flat list of Card-Orientation pairs (one entry
% per card ever drawn, across every saved reading), Themes and
% Categories are the flat theme lists / one category per reading.
% Everything reported is computed here with findall/aggregate_all
% over the tarot knowledge base, not pre-counted in Python.
history_analytics(CardOrients, Themes, Categories, Analytics) :-
    findall(Card, member(Card-_, CardOrients), Cards),
    count_occurrences(Cards, CardCounts),
    top_n(CardCounts, 10, TopCards),
    findall(
        card_count{card: Card, count: N},
        member(Card-N, TopCards),
        MostDrawn
    ),

    findall(Suit, (member(Card, Cards), card_suit(Card, Suit0), Suit0 \= major, Suit = Suit0), Suits),
    ( Suits == []
    -> MostCommonSuit = none
    ;  count_occurrences(Suits, SuitCounts),
       SuitCounts = [MostCommonSuit-_|_]
    ),

    aggregate_all(count, (member(Card, Cards), is_major(Card)), MajorCount),
    length(Cards, TotalCards),
    MinorCount is TotalCards - MajorCount,

    count_occurrences(Themes, ThemeCounts),
    top_n(ThemeCounts, 10, TopThemes),
    findall(
        theme_count{theme: Theme, count: N},
        member(Theme-N, TopThemes),
        MostThemes
    ),

    count_occurrences(Categories, CategoryCounts),
    top_n(CategoryCounts, 10, TopCategories),
    findall(
        category_count{category: Cat, count: N},
        member(Cat-N, TopCategories),
        MostCategories
    ),

    aggregate_all(count, member(_-reversed, CardOrients), ReversedCount),
    UprightCount is TotalCards - ReversedCount,
    length(Categories, TotalReadings),

    Analytics = history_analytics{
        total_readings: TotalReadings,
        most_drawn_cards: MostDrawn,
        most_common_suit: MostCommonSuit,
        major_vs_minor: major_minor{major: MajorCount, minor: MinorCount},
        most_common_themes: MostThemes,
        most_common_categories: MostCategories,
        upright_vs_reversed: upright_reversed{upright: UprightCount, reversed: ReversedCount}
    }.

% --- Pattern reasoning ("why", not just "what") ---------------
% These go beyond a frequency table: they flag when a count
% crosses a threshold worth surfacing to the user, with the rule
% that fired named explicitly so it can appear in a trace.

% recurring_theme(+Themes, -Theme, -Count) - a theme drawn 3+
% times across the user's history; nondeterministic, one solution
% per qualifying theme, most frequent first.
recurring_theme(Themes, Theme, Count) :-
    count_occurrences(Themes, Counts),
    member(Theme-Count, Counts),
    Count >= 3.

recurring_themes(Themes, Recurring) :-
    findall(
        recurring_theme{theme: Theme, count: Count},
        recurring_theme(Themes, Theme, Count),
        Recurring
    ).

% suit_bias(+Cards, -Suit, -Proportion) - a minor-arcana suit that
% accounts for a large share of every card drawn, suggesting an
% elemental leaning worth naming (fire=wands, earth=pentacles,
% air=swords, water=cups).
suit_bias(Cards, Suit, Proportion) :-
    length(Cards, Total),
    Total >= 5,
    findall(S, (member(C, Cards), card_suit(C, S), S \= major), Suits),
    count_occurrences(Suits, Counts),
    Counts = [Suit-N|_],
    Proportion is N / Total,
    Proportion >= 0.4.

% suit_element/2 (Suit maps to its classical element) is already
% defined in tarot.pl - reused here as-is, not redefined.

% reversal_bias(+CardOrients, -Bias) - whether the user has been
% drawing mostly-upright, mostly-reversed, or a balanced mix.
% Reversed-heavy readings traditionally read as blocked/internal
% energy, so this is worth calling out rather than only counting.
reversal_bias(CardOrients, Bias) :-
    length(CardOrients, Total),
    Total >= 5,
    aggregate_all(count, member(_-reversed, CardOrients), Reversed),
    Proportion is Reversed / Total,
    (   Proportion >= 0.6 -> Bias = mostly_reversed
    ;   Proportion =< 0.2 -> Bias = mostly_upright
    ;   Bias = balanced
    ).

% --- Historically-aware spread recommendation -----------------
% category_suit_bias(+Records, -Category, -Suit, -Element)
% Records is a list of reading_record{category:Category, cards:Cards}
% (one per saved reading). Finds a category where a single suit
% dominates across every reading filed under it, then names the
% element that suit belongs to so the UI/AI layer can explain why.
category_suit_bias(Records, Category, Suit, Element) :-
    setof(Cat, R^(member(R, Records), get_dict(category, R, Cat)), Categories),
    member(Category, Categories),
    findall(
        Card,
        ( member(R, Records),
          get_dict(category, R, Category),
          get_dict(cards, R, Cards),
          member(Card, Cards)
        ),
        CategoryCards
    ),
    length(CategoryCards, N),
    N >= 3,
    suit_bias(CategoryCards, Suit, _),
    suit_element(Suit, Element).

% history_insights(+Records, +Themes, -Insights)
% Top-level entry point: combines recurring themes, suit/element
% bias, reversal bias and per-category suit bias into one list of
% insight{type:, ..., rule:} dicts, each naming the rule that
% produced it so callers can render it as a reasoning trace.
history_insights(Records, Themes, CardOrients, Insights) :-
    findall(
        insight{type: recurring_theme, theme: Theme, count: Count,
                 rule: 'recurring_theme/3: theme drawn 3+ times'},
        recurring_theme(Themes, Theme, Count),
        ThemeInsights
    ),
    findall(Cards1, (member(R, Records), get_dict(cards, R, Cards1)), CardLists),
    append(CardLists, AllCards),
    ( suit_bias(AllCards, Suit, Proportion), suit_element(Suit, Element)
    -> SuitInsights = [insight{type: suit_bias, suit: Suit, element: Element,
                                proportion: Proportion,
                                rule: 'suit_bias/3: one suit >= 40% of all cards drawn'}]
    ;  SuitInsights = []
    ),
    ( reversal_bias(CardOrients, Bias), Bias \= balanced
    -> ReversalInsights = [insight{type: reversal_bias, bias: Bias,
                                    rule: 'reversal_bias/2: reversed-card share crosses 60%/20%'}]
    ;  ReversalInsights = []
    ),
    findall(
        insight{type: category_suit_bias, category: Category, suit: Suit2,
                element: Element2,
                rule: 'category_suit_bias/4: one suit dominates a question category'},
        category_suit_bias(Records, Category, Suit2, Element2),
        CategoryInsights
    ),
    append([ThemeInsights, SuitInsights, ReversalInsights, CategoryInsights], Insights).
