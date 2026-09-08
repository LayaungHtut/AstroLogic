% ============================================================
% Reading Analysis & Interpretation Rules - AstroLogic
% Module 3: Reading Analysis & Interpretation
%
% Analyzes entire tarot readings rather than individual cards.
% Detects themes, conflicts, and provides holistic analysis.
% ============================================================

% Dependencies loaded via prolog_service.py before this file

% ============================================================
% SECTION 1: Individual Card Analysis
% ============================================================

% --- analyze_card/3 ---
% Analyze a single card with its orientation.
% Returns keywords, themes, meaning, and aspects.

analyze_card(Card, Orientation, Analysis) :-
    tarot_card(Card, Arcana, Extra),
    card_name(Card, Name),
    card_keywords_orientation(Card, Orientation, Keywords),
    card_meaning(Card, Orientation, Meaning),
    findall(Theme, card_theme(Card, Theme), Themes),
    % Extract positive and challenging aspects
    (   Orientation = upright
    ->  tarot_upright(Card, Positive),
        tarot_reversed(Card, Challenging)
    ;   tarot_reversed(Card, Positive),
        tarot_upright(Card, Challenging)
    ),
    Analysis = card_analysis{
        card: Card,
        name: Name,
        arcana: Arcana,
        orientation: Orientation,
        keywords: Keywords,
        themes: Themes,
        meaning: Meaning,
        positive_aspects: Positive,
        challenging_aspects: Challenging
    }.

% ============================================================
% SECTION 2: Position-Aware Interpretation
% ============================================================
% A card in a different position has different emphasis.

% --- position_meaning_modifier/3 ---
% Each position has an interpretive lens.

position_meaning_modifier(guidance, 'This card highlights what you should focus on for guidance.').
position_meaning_modifier(past, 'This card represents energies from your recent past.').
position_meaning_modifier(present, 'This card reflects your current situation and energy.').
position_meaning_modifier(future, 'This card points toward emerging energies ahead.').
position_meaning_modifier(current_situation, 'This card describes your current situation.').
position_meaning_modifier(path_a, 'This card represents the likely outcome of Path A.').
position_meaning_modifier(path_b, 'This card represents the likely outcome of Path B.').
position_meaning_modifier(advice, 'This card offers specific advice for your decision.').
position_meaning_modifier(current_self, 'This card reflects who you are right now.').
position_meaning_modifier(hidden_influence, 'This card reveals unseen forces at work.').
position_meaning_modifier(what_to_understand, 'This card highlights what you need to understand.').
position_meaning_modifier(you, 'This card represents you in this relationship.').
position_meaning_modifier(other_person, 'This card represents the other person.').
position_meaning_modifier(connection, 'This card describes the connection between you.').
position_meaning_modifier(challenge, 'This card identifies the main challenge.').
position_meaning_modifier(current_position, 'This card reflects your current professional position.').
position_meaning_modifier(strength, 'This card highlights your professional strength.').
position_meaning_modifier(challenge, 'This card identifies the professional challenge.').
position_meaning_modifier(opportunity, 'This card reveals an emerging opportunity.').
position_meaning_modifier(advice, 'This card offers career guidance.').
% Catch-all: without this, a position label that isn't one of the fixed
% spreads above (e.g. "Card 1".."Card 10" from an open/custom draw) makes
% once(position_meaning_modifier(...)) fail, which silently drops that card
% out of card_interpretations in analyze_reading_oriented/4 via findall/3 -
% the card is still drawn and shown in the UI, but gets no per-card
% interpretation. Any custom/free-form spread depends on this fallback to
% read every drawn card, not just the ones matching a known position name.
position_meaning_modifier(_, 'This card speaks to its own place in the story you are drawing.').

% --- position_theme_emphasis/3 ---
% Each position emphasizes certain theme categories.

position_theme_emphasis(guidance, reflective).
position_theme_emphasis(past, historical).
position_theme_emphasis(present, current).
position_theme_emphasis(future, emerging).
position_theme_emphasis(challenge, challenging).
position_theme_emphasis(strength, positive).
position_theme_emphasis(advice, advisory).
position_theme_emphasis(connection, relational).
position_theme_emphasis(hidden_influence, hidden).
position_theme_emphasis(what_to_understand, educational).
% NOTE: these eight positions (used by the decision, self_reflection, career,
% and relationship spreads — see spread_rules.pl) had no entry at all here,
% so interpret_card_position/4 failed outright for them with no fallback,
% silently dropping every card in those four spread types from
% card_interpretations (and therefore from reading_direction/2 too).
position_theme_emphasis(current_situation, current).
position_theme_emphasis(path_a, neutral).
position_theme_emphasis(path_b, neutral).
position_theme_emphasis(current_self, current).
position_theme_emphasis(you, neutral).
position_theme_emphasis(other_person, relational).
position_theme_emphasis(current_position, current).
position_theme_emphasis(opportunity, positive).
% Catch-all so an unrecognized position (e.g. a future spread type) still
% resolves instead of making interpret_card_position/4 fail outright.
position_theme_emphasis(_, neutral).

% --- interpret_card_position/4 ---
% Combine card analysis with position interpretation.

interpret_card_position(Card, Position, Orientation, Interpretation) :-
    analyze_card(Card, Orientation, CardAnalysis),
    % once/1 on both of these: position_meaning_modifier/2 has two separate
    % facts each for 'challenge' (used by both the relationship and career
    % spreads, worded differently for each) and 'advice' (decision vs.
    % career spreads) — and position_theme_emphasis/2 ends in a catch-all
    % fact (`_`), so a *known* position still has a second solution via the
    % catch-all on backtracking. Without once/1 on both, the findall/3 in
    % analyze_reading_oriented/4 would collect a duplicate
    % card_position_interpretation per card for any position name reused
    % across more than one spread type.
    once(position_meaning_modifier(Position, PositionContext)),
    once(position_theme_emphasis(Position, Emphasis)),
    % Adjust interpretation based on position
    (   Emphasis = challenging
    ->  InterpretationAspect = CardAnalysis.challenging_aspects
    ;   Emphasis = positive
    ->  InterpretationAspect = CardAnalysis.positive_aspects
    ;   InterpretationAspect = CardAnalysis.meaning
    ),
    Interpretation = card_position_interpretation{
        card: Card,
        name: CardAnalysis.name,
        position: Position,
        orientation: Orientation,
        keywords: CardAnalysis.keywords,
        themes: CardAnalysis.themes,
        position_context: PositionContext,
        emphasis: Emphasis,
        aspect: InterpretationAspect,
        full_interpretation: format('~w ~w', [CardAnalysis.name, PositionContext])
    }.

% ============================================================
% SECTION 3: Multi-Card Reading Analysis
% ============================================================

% --- analyze_reading/3 ---
% Analyze a complete reading with cards and positions.

analyze_reading(Cards, Positions, Analysis) :-
    analyze_reading_oriented(Cards, Positions, _, Analysis).

% --- analyze_reading_oriented/4 ---
% Analyze with orientations provided.

analyze_reading_oriented(Cards, Positions, Orientations, Analysis) :-
    length(Cards, CardCount),
    length(Positions, PosCount),
    % Analyze each card in its position
    findall(
        CardInterp,
        (
            nth0(Index, Cards, Card),
            nth0(Index, Positions, Position),
            nth0(Index, Orientations, Orientation),
            interpret_card_position(Card, Position, Orientation, CardInterp)
        ),
        CardInterpretations
    ),
    % Detect themes
    reading_themes(Cards, AllThemes),
    sort(AllThemes, Themes),
    % Detect dominant theme
    dominant_theme(Cards, Dominant),
    % Detect conflicts
    reading_conflicts(Cards, Conflicts),
    % Detect suit balance
    suit_distribution(Cards, SuitDist),
    % Detect major/minor balance
    arcana_distribution(Cards, ArcanaDist),
    % Detect dominant element
    dominant_element(Cards, DominantElement),
    % Detect overall direction
    reading_direction(CardInterpretations, Direction),
    Analysis = reading_analysis{
        card_count: CardCount,
        position_count: PosCount,
        card_interpretations: CardInterpretations,
        themes: Themes,
        dominant_theme: Dominant,
        conflicts: Conflicts,
        suit_distribution: SuitDist,
        arcana_distribution: ArcanaDist,
        dominant_element: DominantElement,
        direction: Direction
    }.

% ============================================================
% SECTION 4: Theme Detection
% ============================================================

% --- reading_themes/2 ---
% Extract all themes from a set of cards.

reading_themes(Cards, Themes) :-
    findall(
        Theme,
        (
            member(Card, Cards),
            card_theme(Card, Theme)
        ),
        Themes
    ).

% --- dominant_theme/2 ---
% Find the most frequently occurring theme.

dominant_theme(Cards, Theme) :-
    reading_themes(Cards, AllThemes),
    count_themes(AllThemes, ThemeCounts),
    sort(ThemeCounts, Sorted),
    last(Sorted, count(_, Theme)).

% --- count_themes/2 ---
% Count occurrences of each theme.

count_themes([], []).
count_themes([Theme|Rest], [count(Count, Theme)|RestCounts]) :-
    include(=(Theme), Rest, Same),
    length(Same, RestCount),
    Count is RestCount + 1,
    exclude(=(Theme), Rest, Remaining),
    count_themes(Remaining, RestCounts).

% --- theme_category/2 ---
% Classify themes into broader categories.

theme_category(change, transformation).
theme_category(endings, transformation).
theme_category(rebirth, transformation).
theme_category(sudden_change, transformation).
theme_category(awakening, transformation).

theme_category(reflection, introspection).
theme_category(introspection, introspection).
theme_category(solitude, introspection).
theme_category(inner_wisdom, introspection).
theme_category(meditation, introspection).

theme_category(choice, decision).
theme_category(planning, decision).
theme_category(decision, decision).
theme_category(new_perspective, decision).
theme_category(fairness, decision).

theme_category(growth, development).
theme_category(expansion, development).
theme_category(mastery, development).
theme_category(skill_development, development).
theme_category(new_beginnings, development).

theme_category(communication, expression).
theme_category(new_ideas, expression).
theme_category(creativity, expression).
theme_category(curiosity, expression).

theme_category(discipline, structure).
theme_category(responsibility, structure).
theme_category(structure, structure).
theme_category(security, structure).
theme_category(ambition, structure).

theme_category(balance, harmony).
theme_category(harmony, harmony).
theme_category(moderation, harmony).
theme_category(patience, harmony).

theme_category(confidence, empowerment).
theme_category(leadership, empowerment).
theme_category(courage, empowerment).
theme_category(action, empowerment).
theme_category(victory, empowerment).

theme_category(intuition, inner_world).
theme_category(mystery, inner_world).
theme_category(subconscious, inner_world).
theme_category(illusion, inner_world).
theme_category(fear, inner_world).

theme_category(love, relationship).
theme_category(partnership, relationship).
theme_category(connection, relationship).
theme_category(friendship, relationship).
theme_category(nurturing, relationship).

theme_category(hope, spiritual).
theme_category(inspiration, spiritual).
theme_category(spirituality, spiritual).
theme_category(renewal, spiritual).
theme_category(destiny, spiritual).

theme_category(loss, challenge).
theme_category(conflict, challenge).
theme_category(burden, challenge).
theme_category(restriction, challenge).
theme_category(hardship, challenge).

theme_category(joy, celebration).
theme_category(celebration, celebration).
theme_category(success, celebration).
theme_category(abundance, celebration).
theme_category(satisfaction, celebration).

% ============================================================
% SECTION 5: Conflicting Themes
% ============================================================

% --- theme_conflict/3 ---
% Identify symbolic tension between themes.

theme_conflict(action, patience, tension('Action vs Patience', 'The reading emphasizes both taking decisive action and exercising patience. Consider when each approach is most appropriate.')).
theme_conflict(patience, action, tension('Patience vs Action', 'The reading emphasizes both taking decisive action and exercising patience. Consider when each approach is most appropriate.')).

theme_conflict(independence, partnership, tension('Independence vs Partnership', 'The reading highlights both self-reliance and collaboration. Balance personal autonomy with cooperative engagement.')).
theme_conflict(partnership, independence, tension('Partnership vs Independence', 'The reading highlights both self-reliance and collaboration. Balance personal autonomy with cooperative engagement.')).

theme_conflict(change, stability, tension('Change vs Stability', 'The reading pulls between transformation and maintaining the status quo. Embrace necessary change while preserving what matters.')).
theme_conflict(stability, change, tension('Stability vs Change', 'The reading pulls between transformation and maintaining the status quo. Embrace necessary change while preserving what matters.')).

theme_conflict(logic, emotion, tension('Logic vs Emotion', 'The reading balances rational thinking with emotional wisdom. Both perspectives offer valuable insight.')).
theme_conflict(emotion, logic, tension('Emotion vs Logic', 'The reading balances rational thinking with emotional wisdom. Both perspectives offer valuable insight.')).

theme_conflict(confidence, reflection, tension('Confidence vs Reflection', 'The reading combines bold self-assurance with thoughtful introspection. Act with confidence but check in with yourself.')).
theme_conflict(reflection, confidence, tension('Reflection vs Confidence', 'The reading combines bold self-assurance with thoughtful introspection. Act with confidence but check in with yourself.')).

theme_conflict(action, reflection, tension('Action vs Reflection', 'The reading emphasizes balancing initiative with careful consideration. Neither alone leads to the best outcome.')).
theme_conflict(reflection, action, tension('Reflection vs Action', 'The reading emphasizes balancing initiative with careful consideration. Neither alone leads to the best outcome.')).

theme_conflict(freedom, discipline, tension('Freedom vs Discipline', 'The reading highlights tension between personal freedom and structured approach. Find creative discipline.')).
theme_conflict(discipline, freedom, tension('Discipline vs Freedom', 'The reading highlights tension between personal freedom and structured approach. Find creative discipline.')).

theme_conflict(new_beginnings, endings, tension('New Beginnings vs Endings', 'The reading signals both closure and fresh starts. Release the old to make space for the new.')).
theme_conflict(endings, new_beginnings, tension('Endings vs New Beginnings', 'The reading signals both closure and fresh starts. Release the old to make space for the new.')).

theme_conflict(courage, surrender, tension('Courage vs Surrender', 'The reading balances bold action with letting go. Know when to push forward and when to yield.')).
theme_conflict(surrender, courage, tension('Surrender vs Courage', 'The reading balances bold action with letting go. Know when to push forward and when to yield.')).

theme_conflict(abundance, simplicity, tension('Abundance vs Simplicity', 'The reading highlights both material richness and essential simplicity. Value what you have while staying grounded.')).
theme_conflict(simplicity, abundance, tension('Simplicity vs Abundance', 'The reading highlights both material richness and essential simplicity. Value what you have while staying grounded.')).

% ============================================================
% SECTION 6: Reading Conflicts Detection
% ============================================================

% --- reading_conflicts/2 ---
% Detect all conflicts present in a reading.

reading_conflicts(Cards, Conflicts) :-
    reading_themes(Cards, Themes),
    sort(Themes, UniqueThemes),
    findall(
        Conflict,
        (
            member(T1, UniqueThemes),
            member(T2, UniqueThemes),
            T1 @< T2,
            theme_conflict(T1, T2, Conflict)
        ),
        Conflicts
    ).

% ============================================================
% SECTION 7: Suit & Arcana Distribution
% ============================================================

% --- suit_distribution/2 ---
% Count cards per suit.

suit_distribution(Cards, Distribution) :-
    findall(Card, (member(Card, Cards), tarot_card(Card, minor_arcana, wands)), Wands),
    findall(Card, (member(Card, Cards), tarot_card(Card, minor_arcana, cups)), Cups),
    findall(Card, (member(Card, Cards), tarot_card(Card, minor_arcana, swords)), Swords),
    findall(Card, (member(Card, Cards), tarot_card(Card, minor_arcana, pentacles)), Pentacles),
    length(Wands, WandsCount),
    length(Cups, CupsCount),
    length(Swords, SwordsCount),
    length(Pentacles, PentaclesCount),
    Distribution = suit_distribution{
        wands: WandsCount,
        cups: CupsCount,
        swords: SwordsCount,
        pentacles: PentaclesCount
    }.

% --- arcana_distribution/2 ---
% Count major vs minor arcana.

arcana_distribution(Cards, Distribution) :-
    findall(Card, (member(Card, Cards), tarot_card(Card, major_arcana, _)), Major),
    findall(Card, (member(Card, Cards), tarot_card(Card, minor_arcana, _)), Minor),
    length(Major, MajorCount),
    length(Minor, MinorCount),
    Distribution = arcana_distribution{
        major: MajorCount,
        minor: MinorCount,
        total: Total
    },
    Total is MajorCount + MinorCount.

% --- dominant_element/2 ---
% Find the most common element in the reading.

dominant_element(Cards, Element) :-
    findall(
        Element,
        (
            member(Card, Cards),
            (   tarot_card(Card, minor_arcana, Suit)
            ->  suit_element(Suit, Element)
            ;   tarot_card(Card, major_arcana, _),
                Element = universal
            )
        ),
        Elements
    ),
    count_elements(Elements, ElementCounts),
    sort(ElementCounts, Sorted),
    last(Sorted, count(_, Element)).

% --- count_elements/2 ---
count_elements([], []).
count_elements([E|Rest], [count(Count, E)|RestCounts]) :-
    include(=(E), Rest, Same),
    length(Same, RestCount),
    Count is RestCount + 1,
    exclude(=(E), Rest, Remaining),
    count_elements(Remaining, RestCounts).

% --- element_to_theme/2 ---
element_to_theme(fire, action).
element_to_theme(fire, passion).
element_to_theme(fire, creativity).
element_to_theme(earth, practicality).
element_to_theme(earth, stability).
element_to_theme(earth, grounding).
element_to_theme(air, communication).
element_to_theme(air, ideas).
element_to_theme(air, clarity).
element_to_theme(water, emotion).
element_to_theme(water, intuition).
element_to_theme(water, depth).

% ============================================================
% SECTION 8: Reading Direction
% ============================================================

% --- reading_direction/2 ---
% Determine the overall directional flow of a reading.

% --- emphasis_bucket/2 ---
% position_theme_emphasis/2 emits a fairly fine-grained vocabulary
% (historical, current, emerging, advisory, relational, educational, ...)
% for use elsewhere (interpret_card_position/4 uses 'positive'/'challenging'
% specifically to pick which of a card's aspects to surface). reading_direction/2
% only ever needs the coarser positive/challenging/hidden/neutral split, and
% used to check membership in exactly those three atoms directly — meaning
% every emphasis value the position facts can actually produce OTHER than
% those three literals (historical, current, emerging, advisory, relational,
% educational — i.e. every position in a three_card, decision, career, or
% relationship spread) fell into none of the three buckets, so direction
% degenerated to 'balanced' for nearly every real reading regardless of
% the cards drawn.
emphasis_bucket(positive, positive).
emphasis_bucket(challenging, challenging).
emphasis_bucket(hidden, hidden).
emphasis_bucket(historical, neutral).
emphasis_bucket(current, neutral).
emphasis_bucket(emerging, neutral).
emphasis_bucket(advisory, neutral).
emphasis_bucket(relational, neutral).
emphasis_bucket(educational, neutral).
emphasis_bucket(reflective, neutral).
emphasis_bucket(neutral, neutral).
emphasis_bucket(_, neutral).

reading_direction(Interpretations, Direction) :-
    findall(
        Bucket,
        (
            member(I, Interpretations),
            Emphasis = I.emphasis,
            once(emphasis_bucket(Emphasis, Bucket))
        ),
        Buckets
    ),
    include(=(positive), Buckets, Positives),
    include(=(challenging), Buckets, Challengings),
    include(=(hidden), Buckets, Hiddens),
    length(Positives, PosCount),
    length(Challengings, ChalCount),
    length(Hiddens, HiddenCount),
    (   PosCount > ChalCount, PosCount > HiddenCount
    ->  Direction = optimistic
    ;   ChalCount > PosCount, ChalCount > HiddenCount
    ->  Direction = challenging
    ;   HiddenCount > 0
    ->  Direction = reflective
    ;   Direction = balanced
    ).

% ============================================================
% SECTION 9: Reading Summary
% ============================================================

% --- reading_summary/2 ---
% Generate a structured summary from analyzed themes.

reading_summary(Cards, Summary) :-
    reading_themes(Cards, AllThemes),
    sort(AllThemes, Themes),
    dominant_theme(Cards, Dominant),
    reading_conflicts(Cards, Conflicts),
    length(Conflicts, ConflictCount),
    length(Cards, CardCount),
    (   Conflicts = []
    ->  ConflictNote = 'The reading shows harmonious energy with no significant symbolic tension.'
    ;   format(atom(ConflictNote), 'The reading contains ~w symbolic tension(s) worth reflecting on.', [ConflictCount])
    ),
    Summary = reading_summary{
        themes: Themes,
        dominant_theme: Dominant,
        conflict_count: ConflictCount,
        conflict_note: ConflictNote,
        card_count: CardCount
    }.

% ============================================================
% SECTION 10: Reading Advice Rules
% ============================================================

% --- reading_advice/2 ---
% Generate advice based on context and detected themes.

reading_advice(context(decision, _, _), 'Consider both paths carefully. The cards suggest weighing your options with both logic and intuition before committing to a direction.').
reading_advice(context(relationship, _, _), 'Focus on open communication and emotional honesty. The cards highlight the importance of understanding both your own needs and those of others.').
reading_advice(context(career, _, _), 'Trust your professional instincts while staying grounded. The cards suggest leveraging your strengths while remaining open to new approaches.').
reading_advice(context(self_reflection, _, _), 'Take time for honest self-assessment. The cards encourage looking beneath the surface to understand your true motivations and desires.').
reading_advice(context(friendship, _, _), 'Nurture your connections through genuine presence. The cards suggest that authentic engagement strengthens bonds more than grand gestures.').
reading_advice(context(creativity, _, _), 'Follow your creative impulses without overthinking. The cards encourage experimentation and trusting the creative process.').
reading_advice(context(education, _, _), 'Approach learning with both curiosity and discipline. The cards suggest that consistent effort combined with genuine interest leads to the deepest understanding.').
reading_advice(context(future_planning, _, _), 'Balance ambition with realistic assessment. The cards encourage planning while remaining flexible to unexpected opportunities.').
reading_advice(context(general, _, _), 'Stay present and aware of the energies around you. The cards invite you to notice patterns and trust your intuition in daily interactions.').

% --- theme_based_advice/2 ---
% Advice derived from detected themes.

theme_based_advice(action, 'Take a concrete step today. Even small actions build momentum.').
theme_based_advice(patience, 'Allow things to unfold at their natural pace. Rushing may create unnecessary friction.').
theme_based_advice(reflection, 'Set aside quiet time for honest self-examination. Journaling may help clarify your thoughts.').
theme_based_advice(balance, 'Look for areas of your life that may need rebalancing. Give attention to what has been neglected.').
theme_based_advice(change, 'Embrace transformation. Something is ending to make room for something new.').
theme_based_advice(confidence, 'Trust in your abilities. The cards affirm your capacity to handle what comes.').
theme_based_advice(intuition, 'Pay attention to your inner voice. Your gut feelings are particularly reliable right now.').
theme_based_advice(communication, 'Express yourself honestly but kindly. Clear communication resolves many uncertainties.').
theme_based_advice(creativity, 'Allow yourself to play and experiment. Creativity thrives when you release perfectionism.').
theme_based_advice(discipline, 'Establish or return to a consistent routine. Structure supports your goals.').
theme_based_advice(love, 'Open your heart to give and receive love. Vulnerability is strength, not weakness.').
theme_based_advice(hope, 'Maintain optimism even in challenging times. The cards point toward positive potential.').
theme_based_advice(transformation, 'Release what no longer serves you. Transformation requires letting go.').
theme_based_advice(spirituality, 'Connect with something larger than yourself. Spiritual practice deepens self-understanding.').

% ============================================================
% SECTION 11: Zodiac + Tarot Interaction Rules
% ============================================================

% --- zodiac_tarot_theme/3 ---
% Combine zodiac element with card theme for deeper meaning.

zodiac_tarot_theme(Sign, Card, CombinedTheme) :-
    element(Sign, Element),
    card_theme(Card, Theme),
    element_to_theme(Element, ElementTheme),
    format(atom(CombinedStr), 'Your ~w ~w amplifies this card''s ~w energy', [Sign, Element, Theme]),
    CombinedTheme = combined_theme{
        zodiac: Sign,
        element: Element,
        element_theme: ElementTheme,
        card: Card,
        card_theme: Theme,
        combined: CombinedStr
    }.

% --- profile_reading_theme/3 ---
% Combine zodiac profile traits with reading themes.

profile_reading_theme(Sign, Cards, Analysis) :-
    zodiac_traits(Sign, Traits),
    reading_themes(Cards, CardThemes),
    sort(CardThemes, UniqueCardThemes),
    findall(
        intersection(Theme, Trait),
        (
            member(Theme, UniqueCardThemes),
            member(Trait, Traits),
            symbolic_overlap(Theme, Trait)
        ),
        Overlaps
    ),
    Analysis = profile_reading_analysis(Sign, Traits, UniqueCardThemes, Overlaps, 'The alignment between your zodiac traits and reading themes suggests particular relevance to your personal journey.').

% --- symbolic_overlap/2 ---
% Detect symbolic overlap between a theme and a trait.

symbolic_overlap(action, initiative).
symbolic_overlap(action, courage).
symbolic_overlap(action, leadership).
symbolic_overlap(reflection, introspection).
symbolic_overlap(reflection, intuition).
symbolic_overlap(confidence, courage).
symbolic_overlap(confidence, leadership).
symbolic_overlap(balance, adaptability).
symbolic_overlap(balance, diplomacy).
symbolic_overlap(change, adaptability).
symbolic_overlap(change, independence).
symbolic_overlap(love, nurturing).
symbolic_overlap(love, sensitivity).
symbolic_overlap(love, warmth).
symbolic_overlap(creativity, imagination).
symbolic_overlap(creativity, curiosity).
symbolic_overlap(discipline, determination).
symbolic_overlap(discipline, reliability).
symbolic_overlap(patience, reliability).
symbolic_overlap(patience, determination).
symbolic_overlap(intuition, sensitivity).
symbolic_overlap(intuition, imagination).
symbolic_overlap(hope, optimism).
symbolic_overlap(communication, curiosity).
symbolic_overlap(communication, adaptability).
symbolic_overlap(leadership, initiative).
symbolic_overlap(leadership, confidence).
symbolic_overlap(transformation, independence).
symbolic_overlap(transformation, courage).
symbolic_overlap(mastery, determination).
symbolic_overlap(mastery, discipline).

% --- profile_reading_theme_dict/3 ---
% Dict-shaped wrapper around profile_reading_theme/3 for the API layer
% (the underlying predicate returns a positional compound term, which
% pyswip cannot marshal as named fields).

profile_reading_theme_dict(Sign, Cards, Analysis) :-
    profile_reading_theme(Sign, Cards, profile_reading_analysis(Sign, Traits, CardThemes, Overlaps, Desc)),
    findall(
        overlap{theme: Theme, trait: Trait},
        member(intersection(Theme, Trait), Overlaps),
        OverlapDicts
    ),
    Analysis = profile_theme_analysis{
        sign: Sign,
        traits: Traits,
        card_themes: CardThemes,
        overlaps: OverlapDicts,
        description: Desc
    }.

% ============================================================
% SECTION 5B: Card-Level Conflict Detection (Theme Conflict Detector)
% ============================================================

% --- reading_card_conflicts/2 ---
% Like reading_conflicts/2, but reports which specific cards (by position
% index) produced each conflicting theme pair, so the UI can say e.g.
% "Card 1 urges action while Card 3 counsels patience" instead of just
% naming the two themes.

reading_card_conflicts(Cards, Conflicts) :-
    findall(
        card_conflict{
            card1_index: I, card1: Card1, theme1: Theme1,
            card2_index: J, card2: Card2, theme2: Theme2,
            title: Title, description: Desc
        },
        (
            nth0(I, Cards, Card1),
            nth0(J, Cards, Card2),
            I < J,
            card_theme(Card1, Theme1),
            card_theme(Card2, Theme2),
            theme_conflict(Theme1, Theme2, tension(Title, Desc))
        ),
        Conflicts
    ).

% ============================================================
% SECTION 12: Reasoning Trace for Reading Analysis
% ============================================================

% --- reading_analysis_trace/3 ---
% Generate reasoning trace for full reading analysis.

reading_analysis_trace(Cards, Positions, Trace) :-
    reading_themes(Cards, Themes),
    sort(Themes, UniqueThemes),
    dominant_theme(Cards, Dominant),
    reading_conflicts(Cards, Conflicts),
    suit_distribution(Cards, SuitDist),
    arcana_distribution(Cards, ArcanaDist),
    reading_summary(Cards, Summary),
    % NOTE: length(Cards) etc. used to be passed directly as format/2 args
    % without ever being evaluated via length(List, N) first — the dict
    % field ended up holding the literal, un-rendered compound term
    % "length([...])" instead of a card count.
    length(Cards, CardCount),
    length(UniqueThemes, ThemeCount),
    length(Conflicts, ConflictCount),
    Trace = [
        reasoning_step{
            rule: format('analyze_cards(~w)', [Cards]),
            input: 'Card list',
            result: format('~w cards analyzed', [CardCount]),
            explanation: 'Each card is analyzed individually with its position and orientation'
        },
        reasoning_step{
            rule: format('reading_themes(~w)', [UniqueThemes]),
            input: 'All card themes',
            result: format('~w themes detected: ~w', [ThemeCount, UniqueThemes]),
            explanation: 'Themes are extracted from all cards and deduplicated'
        },
        reasoning_step{
            rule: format('dominant_theme(~w, ~w)', [Cards, Dominant]),
            input: 'Theme frequency',
            result: format('Dominant theme: ~w', [Dominant]),
            explanation: 'The most frequently occurring theme is identified'
        },
        reasoning_step{
            rule: format('reading_conflicts(~w)', [ConflictCount]),
            input: 'Theme pairs',
            result: format('~w symbolic tension(s) detected', [ConflictCount]),
            explanation: 'Conflicting themes indicate areas requiring balance'
        },
        reasoning_step{
            rule: format('suit_distribution(~w)', [SuitDist]),
            input: 'Card suits',
            result: 'Suit balance analyzed',
            explanation: 'Dominant suit reveals the reading primary energy type'
        }
    ].
