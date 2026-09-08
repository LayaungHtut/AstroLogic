% ============================================================
% Spread Rules - AstroLogic
% Rules for recommending tarot spreads
% ============================================================

:- use_module(zodiac).
:- use_module(tarot).

% --- Spread Definitions ---
spread(one_card, 'One Card', 'Simple guidance or daily insight', 1).
spread(three_card, 'Three Card', 'Past, Present, Future', 3).
spread(decision, 'Decision Spread', 'Current Situation, Path A, Path B, Advice', 4).
spread(self_reflection, 'Self Reflection', 'Current Self, Hidden Influence, What to Understand, Guidance', 4).
spread(relationship, 'Relationship Spread', 'You, Other Person, Connection, Challenge, Guidance', 5).
spread(career, 'Career Spread', 'Current Position, Strength, Challenge, Opportunity, Advice', 5).

% --- Spread Position Names ---
spread_positions(one_card, ['Guidance']).
spread_positions(three_card, ['Past', 'Present', 'Future']).
spread_positions(decision, ['Current Situation', 'Path A', 'Path B', 'Advice']).
spread_positions(self_reflection, ['Current Self', 'Hidden Influence', 'What to Understand', 'Guidance']).
spread_positions(relationship, ['You', 'Other Person', 'Connection', 'Challenge', 'Guidance']).
spread_positions(career, ['Current Position', 'Strength', 'Challenge', 'Opportunity', 'Advice']).

% --- Question Category Classification ---
question_category(Input, Category) :-
    (   sub_string(Input, _, _, _, 'career')
    ->  Category = career
    ;   sub_string(Input, _, _, _, 'job')
    ->  Category = career
    ;   sub_string(Input, _, _, _, 'work')
    ->  Category = career
    ;   sub_string(Input, _, _, _, 'relationship')
    ->  Category = relationship
    ;   sub_string(Input, _, _, _, 'partner')
    ->  Category = relationship
    ;   sub_string(Input, _, _, _, 'love')
    ->  Category = relationship
    ;   sub_string(Input, _, _, _, 'education')
    ->  Category = education
    ;   sub_string(Input, _, _, _, 'study')
    ->  Category = education
    ;   sub_string(Input, _, _, _, 'school')
    ->  Category = education
    ;   sub_string(Input, _, _, _, 'university')
    ->  Category = education
    ;   sub_string(Input, _, _, _, 'major')
    ->  Category = education
    ;   sub_string(Input, _, _, _, 'decision')
    ->  Category = decision
    ;   sub_string(Input, _, _, _, 'choose')
    ->  Category = decision
    ;   sub_string(Input, _, _, _, 'choice')
    ->  Category = decision
    ;   sub_string(Input, _, _, _, 'which')
    ->  Category = decision
    ;   sub_string(Input, _, _, _, 'friend')
    ->  Category = friendship
    ;   sub_string(Input, _, _, _, 'creative')
    ->  Category = creativity
    ;   sub_string(Input, _, _, _, 'art')
    ->  Category = creativity
    ;   sub_string(Input, _, _, _, 'write')
    ->  Category = creativity
    ;   sub_string(Input, _, _, _, 'future')
    ->  Category = future_planning
    ;   sub_string(Input, _, _, _, 'plan')
    ->  Category = future_planning
    ;   sub_string(Input, _, _, _, 'myself')
    ->  Category = self_reflection
    ;   sub_string(Input, _, _, _, 'understand')
    ->  Category = self_reflection
    ;   sub_string(Input, _, _, _, 'meaning')
    ->  Category = self_reflection
    ;   Category = general
    ).

% --- Spread Recommendation Rules ---
recommended_spread(career, career).
recommended_spread(education, career).
recommended_spread(relationship, relationship).
recommended_spread(friendship, relationship).
recommended_spread(decision, decision).
recommended_spread(self_reflection, self_reflection).
recommended_spread(creativity, self_reflection).
recommended_spread(future_planning, decision).
recommended_spread(personal_growth, self_reflection).
recommended_spread(general, three_card).

% --- Modality-Based Spread Adjustment ---
modality_spread_adjustment(cardinal, Spread) :-
    member(Spread, [decision, career]).
modality_spread_adjustment(fixed, Spread) :-
    member(Spread, [self_reflection, relationship]).
modality_spread_adjustment(mutable, Spread) :-
    member(Spread, [three_card, self_reflection]).

% --- Element-Based Position Emphasis ---
element_position_emphasis(fire, 'Action & Initiative').
element_position_emphasis(earth, 'Practical Matters').
element_position_emphasis(air, 'Communication & Ideas').
element_position_emphasis(water, 'Emotions & Intuition').

% --- Complete Spread Recommendation ---
spread_recommendation(Input, Sign, Recommendation) :-
    question_category(Input, Category),
    recommended_spread(Category, SpreadType),
    element(Sign, Element),
    modality(Sign, Modality),
    element_position_emphasis(Element, Emphasis),
    spread(SpreadType, Name, Description, CardCount),
    spread_positions(SpreadType, Positions),
    Recommendation = spread_recommendation{
        category: Category,
        spread_type: SpreadType,
        name: Name,
        description: Description,
        card_count: CardCount,
        positions: Positions,
        element: Element,
        modality: Modality,
        emphasis: Emphasis
    }.

% --- spread_recommendation_for/4 ---
% Like spread_recommendation/3, but for when the caller (the user, via the
% UI's spread picker) has already chosen a specific spread type rather than
% asking Prolog to pick one from the question text. Question classification
% is still run (Category is used elsewhere for card relevance/advice), but
% the spread itself is the one requested, not recommended_spread/2's guess.

spread_recommendation_for(Input, Sign, SpreadType, Recommendation) :-
    question_category(Input, Category),
    element(Sign, Element),
    modality(Sign, Modality),
    element_position_emphasis(Element, Emphasis),
    spread(SpreadType, Name, Description, CardCount),
    spread_positions(SpreadType, Positions),
    Recommendation = spread_recommendation{
        category: Category,
        spread_type: SpreadType,
        name: Name,
        description: Description,
        card_count: CardCount,
        positions: Positions,
        element: Element,
        modality: Modality,
        emphasis: Emphasis
    }.

% ============================================================
% SECTION: Custom Draw (user-chosen card count, 1-10)
% ============================================================
% Unlike the fixed spreads above, a custom draw has no predetermined layout
% or number of positions - the seeker decides how many cards to pull. There
% is therefore no single spread/4 fact for it (that predicate assumes a
% fixed CardCount); instead the position list is generated for whatever
% count was requested.

% --- custom_spread_positions/2 ---
% Generate N generic, order-based position labels: ['Card 1', ..., 'Card N'].

custom_spread_positions(Count, Positions) :-
    integer(Count),
    Count >= 1,
    numlist(1, Count, Indices),
    findall(
        Label,
        (member(I, Indices), format(atom(Label), 'Card ~w', [I])),
        Positions
    ).

% --- custom_spread_recommendation/4 ---
% Like spread_recommendation_for/4, but for an open draw of Count cards
% (1-10, enforced by the API layer) instead of one of the fixed spreads.
% Still runs the same zodiac reasoning (element, modality, emphasis) so a
% custom draw is read with the same symbolic grounding as any other spread -
% only the layout/position semantics are generic rather than fixed.

custom_spread_recommendation(Input, Sign, Count, Recommendation) :-
    question_category(Input, Category),
    element(Sign, Element),
    modality(Sign, Modality),
    element_position_emphasis(Element, Emphasis),
    custom_spread_positions(Count, Positions),
    Recommendation = spread_recommendation{
        category: Category,
        spread_type: custom,
        name: 'Custom Draw',
        description: 'An open draw sized entirely to your own intuition, read card by card in the order you pulled them.',
        card_count: Count,
        positions: Positions,
        element: Element,
        modality: Modality,
        emphasis: Emphasis
    }.

% --- Reasoning Trace for Spread ---
generate_spread_trace(Input, Sign, Trace) :-
    question_category(Input, Category),
    recommended_spread(Category, SpreadType),
    element(Sign, Element),
    modality(Sign, Modality),
    spread(SpreadType, Name, _, _),
    Trace = [
        trace_step{
            rule: question_classification(Input, Category),
            result: 'Question classified as category'
        },
        trace_step{
            rule: recommended_spread(Category, SpreadType),
            result: 'Spread recommended for category'
        },
        trace_step{
            rule: element_rule(Sign, Element),
            result: 'Zodiac element identified'
        },
        trace_step{
            rule: modality_rule(Sign, Modality),
            result: 'Zodiac modality identified'
        },
        trace_step{
            rule: spread_selected(SpreadType, Name),
            result: 'Final spread selected'
        }
    ].
