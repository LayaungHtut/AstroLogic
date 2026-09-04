% ============================================================
% Card Selection & Filtering Functions - AstroLogic
% Module 2: Card Selection & Spread Filtering
%
% Controls which tarot cards and spreads are appropriate
% for a reading based on question, zodiac, and context.
% ============================================================

:- use_module(zodiac).
:- use_module(tarot).
:- use_module(zodiac_profile).

% ============================================================
% SECTION 1: Card Theme Classification
% ============================================================
% Every card is classified into thematic categories.
% This drives filtering and recommendation logic.

card_theme(the_fool, new_beginnings).
card_theme(the_fool, spontaneity).
card_theme(the_fool, adventure).

card_theme(the_magician, manifestation).
card_theme(the_magician, willpower).
card_theme(the_magician, creativity).
card_theme(the_magician, action).

card_theme(the_high_priestess, intuition).
card_theme(the_high_priestess, mystery).
card_theme(the_high_priestess, inner_wisdom).
card_theme(the_high_priestess, patience).

card_theme(the_empress, nurturing).
card_theme(the_empress, abundance).
card_theme(the_empress, beauty).
card_theme(the_empress, creativity).

card_theme(the_emperor, authority).
card_theme(the_emperor, structure).
card_theme(the_emperor, stability).
card_theme(the_emperor, discipline).

card_theme(the_hierophant, tradition).
card_theme(the_hierophant, guidance).
card_theme(the_hierophant, spirituality).
card_theme(the_hierophant, learning).

card_theme(the_lovers, love).
card_theme(the_lovers, choice).
card_theme(the_lovers, harmony).
card_theme(the_lovers, relationships).

card_theme(the_chariot, determination).
card_theme(the_chariot, willpower).
card_theme(the_chariot, action).
card_theme(the_chariot, victory).

card_theme(strength, courage).
card_theme(strength, patience).
card_theme(strength, inner_power).
card_theme(strength, compassion).

card_theme(the_hermit, reflection).
card_theme(the_hermit, solitude).
card_theme(the_hermit, introspection).
card_theme(the_hermit, guidance).

card_theme(wheel_of_fortune, change).
card_theme(wheel_of_fortune, cycles).
card_theme(wheel_of_fortune, destiny).
card_theme(wheel_of_fortune, luck).

card_theme(justice, fairness).
card_theme(justice, truth).
card_theme(justice, balance).
card_theme(justice, accountability).

card_theme(the_hanged_man, surrender).
card_theme(the_hanged_man, new_perspective).
card_theme(the_hanged_man, patience).
card_theme(the_hanged_man, sacrifice).

card_theme(death, transformation).
card_theme(death, endings).
card_theme(death, rebirth).
card_theme(death, letting_go).

card_theme(temperance, balance).
card_theme(temperance, moderation).
card_theme(temperance, harmony).
card_theme(temperance, patience).

card_theme(the_devil, shadow_self).
card_theme(the_devil, attachment).
card_theme(the_devil, freedom_needed).
card_theme(the_devil, materialism).

card_theme(the_tower, upheaval).
card_theme(the_tower, revelation).
card_theme(the_tower, awakening).
card_theme(the_tower, sudden_change).

card_theme(the_star, hope).
card_theme(the_star, inspiration).
card_theme(the_star, renewal).
card_theme(the_star, spirituality).

card_theme(the_moon, illusion).
card_theme(the_moon, intuition).
card_theme(the_moon, subconscious).
card_theme(the_moon, fear).

card_theme(the_sun, joy).
card_theme(the_sun, success).
card_theme(the_sun, vitality).
card_theme(the_sun, confidence).

card_theme(judgement, reflection).
card_theme(judgement, reckoning).
card_theme(judgement, inner_calling).
card_theme(judgement, absolution).

card_theme(the_world, completion).
card_theme(the_world, accomplishment).
card_theme(the_world, integration).
card_theme(the_world, wholeness).

% Minor arcana - Wands (fire: action, creativity, passion)
card_theme(ace_of_wands, action).
card_theme(ace_of_wands, new_beginnings).
card_theme(two_of_wands, planning).
card_theme(two_of_wands, decision).
card_theme(three_of_wands, expansion).
card_theme(three_of_wands, foresight).
card_theme(four_of_wands, celebration).
card_theme(four_of_wands, harmony).
card_theme(five_of_wands, conflict).
card_theme(five_of_wands, competition).
card_theme(six_of_wands, success).
card_theme(six_of_wands, recognition).
card_theme(seven_of_wands, perseverance).
card_theme(seven_of_wands, challenge).
card_theme(eight_of_wands, speed).
card_theme(eight_of_wands, movement).
card_theme(nine_of_wands, resilience).
card_theme(nine_of_wands, persistence).
card_theme(ten_of_wands, burden).
card_theme(ten_of_wands, responsibility).
card_theme(page_of_wands, exploration).
card_theme(page_of_wands, enthusiasm).
card_theme(knight_of_wands, adventure).
card_theme(knight_of_wands, energy).
card_theme(queen_of_wands, confidence).
card_theme(queen_of_wands, warmth).
card_theme(king_of_wands, leadership).
card_theme(king_of_wands, vision).

% Minor arcana - Cups (water: emotion, relationships, intuition)
card_theme(ace_of_cups, love).
card_theme(ace_of_cups, new_feelings).
card_theme(two_of_cups, partnership).
card_theme(two_of_cups, connection).
card_theme(three_of_cups, celebration).
card_theme(three_of_cups, friendship).
card_theme(four_of_cups, contemplation).
card_theme(four_of_cups, apathy).
card_theme(five_of_cups, loss).
card_theme(five_of_cups, regret).
card_theme(six_of_cups, nostalgia).
card_theme(six_of_cups, innocence).
card_theme(seven_of_cups, fantasy).
card_theme(seven_of_cups, choices).
card_theme(eight_of_cups, walking_away).
card_theme(eight_of_cups, seeking_truth).
card_theme(nine_of_cups, satisfaction).
card_theme(nine_of_cups, wish_fulfillment).
card_theme(ten_of_cups, happiness).
card_theme(ten_of_cups, family_harmony).
card_theme(page_of_cups, curiosity).
card_theme(page_of_cups, intuition).
card_theme(knight_of_cups, romance).
card_theme(knight_of_cups, following_heart).
card_theme(queen_of_cups, compassion).
card_theme(queen_of_cups, emotional_stability).
card_theme(king_of_cups, emotional_balance).
card_theme(king_of_cups, diplomacy).

% Minor arcana - Swords (air: thought, communication, conflict)
card_theme(ace_of_swords, clarity).
card_theme(ace_of_swords, breakthrough).
card_theme(two_of_swords, indecision).
card_theme(two_of_swords, stalemate).
card_theme(three_of_swords, heartbreak).
card_theme(three_of_swords, grief).
card_theme(four_of_swords, rest).
card_theme(four_of_swords, recovery).
card_theme(five_of_swords, conflict).
card_theme(five_of_swords, defeat).
card_theme(six_of_swords, transition).
card_theme(six_of_swords, moving_on).
card_theme(seven_of_swords, strategy).
card_theme(seven_of_swords, resourcefulness).
card_theme(eight_of_swords, restriction).
card_theme(eight_of_swords, powerlessness).
card_theme(nine_of_swords, anxiety).
card_theme(nine_of_swords, worry).
card_theme(ten_of_swords, crisis).
card_theme(ten_of_swords, painful_end).
card_theme(page_of_swords, curiosity).
card_theme(page_of_swords, new_ideas).
card_theme(knight_of_swords, ambition).
card_theme(knight_of_swords, determination).
card_theme(queen_of_swords, independence).
card_theme(queen_of_swords, clarity).
card_theme(king_of_swords, intellectual_authority).
card_theme(king_of_swords, fairness).

% Minor arcana - Pentacles (earth: material, practical, financial)
card_theme(ace_of_pentacles, opportunity).
card_theme(ace_of_pentacles, prosperity).
card_theme(two_of_pentacles, balance).
card_theme(two_of_pentacles, adaptability).
card_theme(three_of_pentacles, teamwork).
card_theme(three_of_pentacles, collaboration).
card_theme(four_of_pentacles, security).
card_theme(four_of_pentacles, conservation).
card_theme(five_of_pentacles, hardship).
card_theme(five_of_pentacles, isolation).
card_theme(six_of_pentacles, generosity).
card_theme(six_of_pentacles, sharing).
card_theme(seven_of_pentacles, patience).
card_theme(seven_of_pentacles, investment).
card_theme(eight_of_pentacles, mastery).
card_theme(eight_of_pentacles, skill_development).
card_theme(nine_of_pentacles, independence).
card_theme(nine_of_pentacles, luxury).
card_theme(ten_of_pentacles, wealth).
card_theme(ten_of_pentacles, legacy).
card_theme(page_of_pentacles, diligence).
card_theme(page_of_pentacles, new_skills).
card_theme(knight_of_pentacles, reliability).
card_theme(knight_of_pentacles, hard_work).
card_theme(queen_of_pentacles, nurturing).
card_theme(queen_of_pentacles, practical_abundance).
card_theme(king_of_pentacles, business_acumen).
card_theme(king_of_pentacles, discipline).

% ============================================================
% SECTION 1B: Tarot Topic Categories
% ============================================================
% Structured topic categories for tarot readings.

tarot_topic(love).
tarot_topic(career).
tarot_topic(finance).
tarot_topic(personal_growth).
tarot_topic(communication).
tarot_topic(general).

% --- Topic description ---
topic_description(love, 'Matters of the heart, romantic relationships, self-love, and emotional connections.').
topic_description(career, 'Professional life, work goals, job changes, leadership, and vocational path.').
topic_description(finance, 'Financial matters, abundance, investments, material security, and prosperity.').
topic_description(personal_growth, 'Self-development, inner work, healing, transformation, and life purpose.').
topic_description(communication, 'Expression, dialogue, social connections, truth-telling, and understanding others.').
topic_description(general, 'Broad life overview, daily guidance, and general reflections.').

% --- Topic to category mapping ---
topic_category(love, relationship).
topic_category(career, career).
topic_category(finance, career).
topic_category(personal_growth, self_reflection).
topic_category(communication, general).
topic_category(general, general).

% --- Topic element affinity ---
topic_element(love, water).
topic_element(career, earth).
topic_element(finance, earth).
topic_element(personal_growth, water).
topic_element(communication, air).
topic_element(general, air).

% --- Topic card themes ---
topic_relevant_theme(love, love).
topic_relevant_theme(love, partnership).
topic_relevant_theme(love, connection).
topic_relevant_theme(love, harmony).
topic_relevant_theme(love, nurturing).
topic_relevant_theme(love, emotion).
topic_relevant_theme(love, compassion).

topic_relevant_theme(career, action).
topic_relevant_theme(career, discipline).
topic_relevant_theme(career, ambition).
topic_relevant_theme(career, mastery).
topic_relevant_theme(career, success).
topic_relevant_theme(career, leadership).
topic_relevant_theme(career, responsibility).

topic_relevant_theme(finance, abundance).
topic_relevant_theme(finance, security).
topic_relevant_theme(finance, investment).
topic_relevant_theme(finance, prosperity).
topic_relevant_theme(finance, practicality).
topic_relevant_theme(finance, stability).

topic_relevant_theme(personal_growth, reflection).
topic_relevant_theme(personal_growth, transformation).
topic_relevant_theme(personal_growth, inner_wisdom).
topic_relevant_theme(personal_growth, introspection).
topic_relevant_theme(personal_growth, surrender).
topic_relevant_theme(personal_growth, patience).
topic_relevant_theme(personal_growth, spirituality).

topic_relevant_theme(communication, communication).
topic_relevant_theme(communication, clarity).
topic_relevant_theme(communication, truth).
topic_relevant_theme(communication, ideas).
topic_relevant_theme(communication, diplomacy).
topic_relevant_theme(communication, curiosity).

topic_relevant_theme(general, balance).
topic_relevant_theme(general, change).
topic_relevant_theme(general, guidance).
topic_relevant_theme(general, hope).
topic_relevant_theme(general, cycles).

% --- Topic spread recommendation ---
topic_spread(love, relationship).
topic_spread(career, career).
topic_spread(finance, decision).
topic_spread(personal_growth, self_reflection).
topic_spread(communication, three_card).
topic_spread(general, three_card).

% --- classify_topic/2 ---
% Classify a question into a tarot topic.

classify_topic(Input, Topic) :-
    (   sub_string(Input, _, _, _, 'love') ; sub_string(Input, _, _, _, 'romantic') ;
        sub_string(Input, _, _, _, 'partner') ; sub_string(Input, _, _, _, 'relationship') ;
        sub_string(Input, _, _, _, 'heart') ; sub_string(Input, _, _, _, 'crush') ;
        sub_string(Input, _, _, _, 'date') ; sub_string(Input, _, _, _, 'marriage') ;
        sub_string(Input, _, _, _, 'soulmate') ; sub_string(Input, _, _, _, 'attract')
    ->  Topic = love, !
    ;   sub_string(Input, _, _, _, 'career') ; sub_string(Input, _, _, _, 'job') ;
        sub_string(Input, _, _, _, 'work') ; sub_string(Input, _, _, _, 'promotion') ;
        sub_string(Input, _, _, _, 'boss') ; sub_string(Input, _, _, _, 'colleague') ;
        sub_string(Input, _, _, _, 'business') ; sub_string(Input, _, _, _, 'professional')
    ->  Topic = career, !
    ;   sub_string(Input, _, _, _, 'money') ; sub_string(Input, _, _, _, 'financ') ;
        sub_string(Input, _, _, _, 'invest') ; sub_string(Input, _, _, _, 'wealth') ;
        sub_string(Input, _, _, _, 'salary') ; sub_string(Input, _, _, _, 'budget') ;
        sub_string(Input, _, _, _, 'spend') ; sub_string(Input, _, _, _, 'saving')
    ->  Topic = finance, !
    ;   sub_string(Input, _, _, _, 'grow') ; sub_string(Input, _, _, _, 'improve') ;
        sub_string(Input, _, _, _, 'heal') ; sub_string(Input, _, _, _, 'transform') ;
        sub_string(Input, _, _, _, 'purpose') ; sub_string(Input, _, _, _, 'meaning') ;
        sub_string(Input, _, _, _, 'develop') ; sub_string(Input, _, _, _, 'become') ;
        sub_string(Input, _, _, _, 'myself') ; sub_string(Input, _, _, _, 'inner')
    ->  Topic = personal_growth, !
    ;   sub_string(Input, _, _, _, 'communicat') ; sub_string(Input, _, _, _, 'explain') ;
        sub_string(Input, _, _, _, 'tell') ; sub_string(Input, _, _, _, 'say') ;
        sub_string(Input, _, _, _, 'listen') ; sub_string(Input, _, _, _, 'understand') ;
        sub_string(Input, _, _, _, 'express') ; sub_string(Input, _, _, _, 'speak')
    ->  Topic = communication, !
    ;   Topic = general
    ).

% --- topic_to_category/2 ---
% Map topic to the internal question category.

topic_to_category(Topic, Category) :-
    topic_category(Topic, Category).

% --- topic_eligible_card/2 ---
% Is a card eligible for a given topic?

topic_eligible_card(Card, Topic) :-
    tarot_card(Card, _, _),
    topic_relevant_theme(Topic, Theme),
    card_theme(Card, Theme).

topic_eligible_card(Card, _) :-
    tarot_card(Card, major_arcana, _), !.

% --- select_cards_for_topic/3 ---
% Select eligible cards for a specific topic.

select_cards_for_topic(Sign, Topic, Selection) :-
    topic_spread(Topic, SpreadType),
    spread_positions(SpreadType, Positions),
    element(Sign, Element),
    findall(
        Card,
        (
            topic_eligible_card(Card, Topic)
            ;
            card_matches_element(Card, Element)
        ),
        Eligible
    ),
    sort(Eligible, UniqueEligible),
    Selection = topic_selection{
        topic: Topic,
        spread: SpreadType,
        positions: Positions,
        eligible_cards: UniqueEligible,
        sign: Sign,
        element: Element
    }.

% ============================================================
% SECTION 2: Card-Question Matching
% ============================================================
% Maps question categories to relevant themes.

category_relevant_theme(career, action).
category_relevant_theme(career, discipline).
category_relevant_theme(career, ambition).
category_relevant_theme(career, mastery).
category_relevant_theme(career, success).
category_relevant_theme(career, leadership).
category_relevant_theme(career, responsibility).

category_relevant_theme(education, learning).
category_relevant_theme(education, curiosity).
category_relevant_theme(education, clarity).
category_relevant_theme(education, new_ideas).
category_relevant_theme(education, skill_development).
category_relevant_theme(education, reflection).

category_relevant_theme(relationship, love).
category_relevant_theme(relationship, partnership).
category_relevant_theme(relationship, harmony).
category_relevant_theme(relationship, connection).
category_relevant_theme(relationship, compassion).
category_relevant_theme(relationship, celebration).

category_relevant_theme(decision, choice).
category_relevant_theme(decision, balance).
category_relevant_theme(decision, fairness).
category_relevant_theme(decision, planning).
category_relevant_theme(decision, new_perspective).
category_relevant_theme(decision, clarity).

category_relevant_theme(self_reflection, reflection).
category_relevant_theme(self_reflection, introspection).
category_relevant_theme(self_reflection, inner_wisdom).
category_relevant_theme(self_reflection, solitude).
category_relevant_theme(self_reflection, intuition).
category_relevant_theme(self_reflection, meditation).

category_relevant_theme(friendship, friendship).
category_relevant_theme(friendship, celebration).
category_relevant_theme(friendship, connection).
category_relevant_theme(friendship, generosity).

category_relevant_theme(creativity, creativity).
category_relevant_theme(creativity, new_beginnings).
category_relevant_theme(creativity, imagination).
category_relevant_theme(creativity, expression).
category_relevant_theme(creativity, inspiration).

category_relevant_theme(future_planning, planning).
category_relevant_theme(future_planning, foresight).
category_relevant_theme(future_planning, expansion).
category_relevant_theme(future_planning, destiny).
category_relevant_theme(future_planning, change).

category_relevant_theme(general, balance).
category_relevant_theme(general, harmony).
category_relevant_theme(general, change).
category_relevant_theme(general, reflection).
category_relevant_theme(general, guidance).

% ============================================================
% SECTION 3: Card Filtering Rules
% ============================================================

% --- card_matches_theme/2 ---
% Does a card carry a specific theme?
card_matches_theme(Card, Theme) :-
    tarot_card(Card, _, _),
    card_theme(Card, Theme).

% --- card_matches_question/2 ---
% Does a card have themes relevant to a question category?
card_matches_question(Card, Category) :-
    tarot_card(Card, _, _),
    category_relevant_theme(Category, Theme),
    card_theme(Card, Theme).

% --- card_matches_element/2 ---
% Does a card match a zodiac element?
card_matches_element(Card, fire) :-
    tarot_card(Card, minor_arcana, wands), !.
card_matches_element(Card, water) :-
    tarot_card(Card, minor_arcana, cups), !.
card_matches_element(Card, air) :-
    tarot_card(Card, minor_arcana, swords), !.
card_matches_element(Card, earth) :-
    tarot_card(Card, minor_arcana, pentacles), !.
card_matches_element(Card, _) :-
    tarot_card(Card, major_arcana, _), !.

% --- card_matches_sign/2 ---
% Is a card symbolically associated with a zodiac sign?
card_matches_sign(Card, Sign) :-
    tarot_card(Card, _, _),
    zodiac_card(Sign, Card), !.
card_matches_sign(Card, Sign) :-
    tarot_card(Card, _, _),
    element(Sign, Element),
    card_matches_element(Card, Element), !.

% --- card_eligible/2 ---
% Master eligibility predicate.
% A card is eligible if it matches the context.
% Context is a structure: context(Category, Sign, Element, Themes)

card_eligible(Card, context(Category, Sign, Element, RequiredThemes)) :-
    tarot_card(Card, _, _),
    card_matches_element(Card, Element),
    (   card_matches_question(Card, Category)
    ;   card_matches_sign(Card, Sign)
    ;   member(Theme, RequiredThemes), card_theme(Card, Theme)
    ).

% Fallback: all major arcana are always eligible.
card_eligible(Card, _) :-
    tarot_card(Card, major_arcana, _), !.

% ============================================================
% SECTION 4: Eligible Card Set Generation
% ============================================================

% --- select_eligible_cards/3 ---
% Generate the set of eligible cards for a context.
% Returns all cards matching the filtering criteria.

select_eligible_cards(Context, AllEligible, Filtered) :-
    findall(Card, card_eligible(Card, Context), AllEligible),
    sort(AllEligible, Filtered).

% --- card_priority/3 ---
% Assign priority to a card for ranking.
% Higher priority = more relevant.

card_priority(Card, context(Category, Sign, Element, _), Priority) :-
    (   zodiac_card(Sign, Card)
    ->  P1 = 3
    ;   P1 = 0
    ),
    (   card_matches_question(Card, Category)
    ->  P2 = 2
    ;   P2 = 0
    ),
    (   card_matches_element(Card, Element)
    ->  P3 = 1
    ;   P3 = 0
    ),
    Priority is P1 + P2 + P3.

% --- rank_cards/3 ---
% Rank eligible cards by relevance priority.

rank_cards(Cards, Context, Ranked) :-
    findall(
        priority(Priority, Card),
        (
            member(Card, Cards),
            card_priority(Card, Context, Priority)
        ),
        PriorityPairs
    ),
    sort(PriorityPairs, SortedPairs),
    reverse(SortedPairs, ReversedPairs),
    findall(Card, member(priority(_, Card), ReversedPairs), Ranked).

% ============================================================
% SECTION 5: Spread Functions
% ============================================================

% --- available_spread/1 ---
available_spread(one_card).
available_spread(three_card).
available_spread(decision).
available_spread(self_reflection).
available_spread(relationship).
available_spread(career).

% --- spread_category/2 ---
spread_category(one_card, general).
spread_category(three_card, general).
spread_category(decision, decision).
spread_category(self_reflection, self_reflection).
spread_category(relationship, relationship).
spread_category(career, career).

% --- spread_positions/2 ---
spread_positions(one_card, [guidance]).
spread_positions(three_card, [past, present, future]).
spread_positions(decision, [current_situation, path_a, path_b, advice]).
spread_positions(self_reflection, [current_self, hidden_influence, what_to_understand, guidance]).
spread_positions(relationship, [you, other_person, connection, challenge, guidance]).
spread_positions(career, [current_position, strength, challenge, opportunity, advice]).

% --- spread_card_count/2 ---
spread_card_count(one_card, 1).
spread_card_count(three_card, 3).
spread_card_count(decision, 4).
spread_card_count(self_reflection, 4).
spread_card_count(relationship, 5).
spread_card_count(career, 5).

% --- spread_description/2 ---
spread_description(one_card, 'Simple daily guidance or single-question insight.').
spread_description(three_card, 'Past, Present, Future - a classic timeline reading.').
spread_description(decision, 'Compare two paths and receive advice for a specific decision.').
spread_description(self_reflection, 'Explore your inner world and hidden influences.').
spread_description(relationship, 'Analyze the dynamics between two people.').
spread_description(career, 'Professional guidance covering position, strengths, and opportunities.').

% ============================================================
% SECTION 6: Spread Recommendation
% ============================================================

% --- recommended_spread/2 ---
% Recommend a spread based on question category.

recommended_spread(career, career).
recommended_spread(education, career).
recommended_spread(relationship, relationship).
recommended_spread(friendship, relationship).
recommended_spread(decision, decision).
recommended_spread(future_planning, decision).
recommended_spread(self_reflection, self_reflection).
recommended_spread(personal_growth, self_reflection).
recommended_spread(creativity, self_reflection).
recommended_spread(general, three_card).

% ============================================================
% SECTION 7: Spread Filtering
% ============================================================

% --- filter_spreads/2 ---
% Filter spreads based on context.
% Context = context(Category, Sign, Element)

filter_spreads(context(Category, _, _), Spreads) :-
    findall(
        Spread,
        (
            recommended_spread(Category, Spread)
        ),
        Spreads
    ).

% If no specific recommendation, fall back to general spreads.
filter_spreads(_, [three_card]).

% --- filter_spreads_detailed/2 ---
% Returns spread options with descriptions.

filter_spreads_detailed(Context, Detailed) :-
    filter_spreads(Context, Spreads),
    findall(
        spread_option{
            id: Spread,
            positions: Positions,
            card_count: Count,
            description: Desc
        },
        (
            member(Spread, Spreads),
            spread_positions(Spread, Positions),
            spread_card_count(Spread, Count),
            spread_description(Spread, Desc)
        ),
        Detailed
    ).

% ============================================================
% SECTION 8: Card Orientation
% ============================================================

% --- card_orientation/2 ---
% Note: actual orientation is determined at draw time by Python.
% This predicate provides the possible states.

card_orientation(Card, upright) :- tarot_card(Card, _, _).
card_orientation(Card, reversed) :- tarot_card(Card, _, _).

% --- card_meaning/3 ---
% Get the meaning of a card based on orientation.

card_meaning(Card, upright, Meaning) :-
    tarot_card(Card, _, _),
    tarot_upright(Card, Meaning).

card_meaning(Card, reversed, Meaning) :-
    tarot_card(Card, _, _),
    tarot_reversed(Card, Meaning).

% --- card_keywords_orientation/3 ---
% Get keywords adjusted by orientation.

card_keywords_orientation(Card, upright, Keywords) :-
    tarot_keywords(Card, Keywords).

card_keywords_orientation(Card, reversed, Keywords) :-
    tarot_keywords(Card, RawKeywords),
    findall(
        Modified,
        (
            member(K, RawKeywords),
            modify_keyword_reversed(K, Modified)
        ),
        Keywords
    ).

% Reverse modifiers for keywords.
modify_keyword_reversed(K, blocked_K) :-
    atom_concat(blocked_, K, Blocked), !, Blocked = blocked_K.
modify_keyword_reversed(K, reversed_K) :-
    atom_concat(reversed_, K, Reversed), !, Reversed = reversed_K.
modify_keyword_reversed(K, need_K) :-
    atom_concat(need_, K, Need), !, Need = need_K.
modify_keyword_reversed(K, K).  % Fallback: keep original.

% ============================================================
% SECTION 9: Card Selection for Reading
% ============================================================

% --- select_cards/3 ---
% Select cards for a spread.
% Prolog determines which cards are eligible.
% Python handles the actual random selection from the eligible set.
%
% This predicate returns the eligible card pool and positions.

select_cards(Sign, Category, Selection) :-
    element(Sign, Element),
    zodiac_traits(Sign, Traits),
    context(Category, Sign, Element, Traits),
    spread_positions(Spread, Positions),
    recommended_spread(Category, Spread),
    findall(Card, card_eligible(Card, context(Category, Sign, Element, Traits)), Eligible),
    sort(Eligible, UniqueEligible),
    Selection = card_selection{
        spread: Spread,
        positions: Positions,
        eligible_cards: UniqueEligible,
        category: Category,
        sign: Sign,
        element: Element
    }.

% --- select_cards_reasoning/4 ---
% Generate reasoning trace for card selection.

select_cards_reasoning(Sign, Category, Trace) :-
    element(Sign, Element),
    zodiac_traits(Sign, Traits),
    recommended_spread(Category, Spread),
    spread_positions(Spread, Positions),
    Trace = [
        reasoning_step{
            rule: format('element(~w, ~w)', [Sign, Element]),
            input: Sign,
            result: format('~w element identified', [Element]),
            explanation: 'Element determines card suit affinity'
        },
        reasoning_step{
            rule: format('recommended_spread(~w, ~w)', [Category, Spread]),
            input: Category,
            result: format('~w spread selected for ~w question', [Spread, Category]),
            explanation: 'Spread is chosen based on question category'
        },
        reasoning_step{
            rule: format('spread_positions(~w, ~w)', [Spread, Positions]),
            input: Spread,
            result: format('~w positions in spread', [length(Positions)]),
            explanation: 'Each position has a specific interpretive role'
        },
        reasoning_step{
            rule: format('card_eligible filter for ~w element and ~w category', [Element, Category]),
            input: format('~w, ~w', [Element, Category]),
            result: 'Card pool filtered by element and category relevance',
            explanation: 'Prolog filtering ensures cards are symbolically appropriate'
        }
    ].
