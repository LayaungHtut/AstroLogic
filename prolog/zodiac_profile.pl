% ============================================================
% Zodiac Profile Functions - AstroLogic
% Module 1: Zodiac & Chart Profile Functions
%
% Provides predicates for constructing and analyzing
% a user's symbolic zodiac profile.
% ============================================================

:- use_module(zodiac).

% ============================================================
% SECTION 1: Core Profile Accessors
% ============================================================

% --- get_element/2 ---
% Retrieve the element for a zodiac sign.
get_element(Sign, Element) :-
    zodiac(Sign),
    element(Sign, Element).

% --- get_modality/2 ---
% Retrieve the modality for a zodiac sign.
get_modality(Sign, Modality) :-
    zodiac(Sign),
    modality(Sign, Modality).

% --- get_ruling_planet/2 ---
% Retrieve the ruling planet for a zodiac sign.
get_ruling_planet(Sign, Planet) :-
    zodiac(Sign),
    ruling_planet(Sign, Planet).

% --- zodiac_traits/2 ---
% Retrieve symbolic traits for a zodiac sign.
% This is a wrapper for the base zodiac traits.
zodiac_traits_of(Sign, Traits) :-
    zodiac(Sign),
    zodiac_traits(Sign, Traits).

% ============================================================
% SECTION 2: Strengths & Challenges
% ============================================================
% Derived from the dual nature of zodiac traits.
% Each trait has a positive (strength) and challenging aspect.

% --- Trait strength mapping ---
trait_strength(initiative, 'Takes action and leads').
trait_strength(courage, 'Brave in the face of challenge').
trait_strength(independence, 'Self-reliant and autonomous').
trait_strength(leadership, 'Natural ability to guide others').
trait_strength(patience, 'Steady and enduring').
trait_strength(reliability, 'Dependable and trustworthy').
trait_strength(determination, 'Persistent and focused').
trait_strength(sensuality, 'Appreciates beauty and comfort').
trait_strength(curiosity, 'Eager to learn and explore').
trait_strength(adaptability, 'Flexible and versatile').
trait_strength(communication, 'Expressive and articulate').
trait_strength(intuition, 'Deep inner knowing').
trait_strength(nurturing, 'Caring and supportive').
trait_strength(sensitivity, 'Empathetic and perceptive').
trait_strength(creativity, 'Imaginative and artistic').
trait_strength(generosity, 'Giving and warm-hearted').
trait_strength(confidence, 'Self-assured and radiant').
trait_strength(warmth, 'Enthusiastic and magnetic').
trait_strength(analytical, 'Detail-oriented and precise').
trait_strength(practical, 'Grounded and efficient').
trait_strength(helpfulness, 'Service-oriented and kind').
trait_strength(diplomacy, 'Fair-minded and gracious').
trait_strength(fairness, 'Just and balanced').
trait_strength(charm, 'Attractive and gracious').
trait_strength(intensity, 'Deep and focused').
trait_strength(resourcefulness, 'Clever and resilient').
trait_strength(passion, 'Enthusiastic and driven').
trait_strength(adventure, 'Bold and exploratory').
trait_strength(optimism, 'Positive and hopeful').
trait_strength(freedom, 'Independent spirit').
trait_strength(philosophical, 'Thoughtful and wise').
trait_strength(ambition, 'Goal-oriented and driven').
trait_strength(discipline, 'Structured and controlled').
trait_strength(responsibility, 'Dutiful and mature').
trait_strength(practicality, 'Realistic and grounded').
trait_strength(originality, 'Unique and innovative').
trait_strength(humanitarianism, 'Community-minded').
trait_strength(rebellion, 'Challenges the status quo').
trait_strength(innovation, 'Forward-thinking and inventive').
trait_strength(compassion, 'Deeply caring').
trait_strength(imagination, 'Visionary and creative').
trait_strength(spirituality, 'Connected to the transcendent').
trait_strength(empathy, 'Deeply feeling of others').
trait_strength(versatility, 'Multi-talented and nimble').
trait_strength(restlessness, 'Driven to explore').

% --- Trait challenge mapping ---
trait_challenge(initiative, 'May act impulsively without thinking').
trait_challenge(courage, 'Can be reckless or aggressive').
trait_challenge(independence, 'May resist collaboration').
trait_challenge(leadership, 'Can become domineering').
trait_challenge(patience, 'May become too passive or stagnant').
trait_challenge(reliability, 'Can become stubborn or inflexible').
trait_challenge(determination, 'May become obsessive or rigid').
trait_challenge(sensuality, 'Can become overly indulgent').
trait_challenge(curiosity, 'May become scattered or restless').
trait_challenge(adaptability, 'Can lack consistency or depth').
trait_challenge(communication, 'May talk too much or gossip').
trait_challenge(intuition, 'Can become overly suspicious').
trait_challenge(nurturing, 'May become overprotective or controlling').
trait_challenge(sensitivity, 'Can be easily hurt or moody').
trait_challenge(creativity, 'May become impractical or self-absorbed').
trait_challenge(generosity, 'Can be taken advantage of').
trait_challenge(confidence, 'May become arrogant or proud').
trait_challenge(warmth, 'Can be dramatic or attention-seeking').
trait_challenge(analytical, 'May become overly critical').
trait_challenge(practical, 'Can become rigid or materialistic').
trait_challenge(helpfulness, 'May become a perfectionist martyr').
trait_challenge(diplomacy, 'Can be indecisive or passive-aggressive').
trait_challenge(fairness, 'May become self-righteous').
trait_challenge(charm, 'Can be superficial or people-pleasing').
trait_challenge(intensity, 'May become secretive or jealous').
trait_challenge(resourcefulness, 'Can become manipulative').
trait_challenge(passion, 'May become obsessive or volatile').
trait_challenge(adventure, 'Can become restless or irresponsible').
trait_challenge(optimism, 'May become unrealistic or naive').
trait_challenge(freedom, 'Can resist necessary structure').
trait_challenge(philosophical, 'May become preachy or detached').
trait_challenge(ambition, 'Can become ruthless or workaholic').
trait_challenge(discipline, 'May become cold or overly strict').
trait_challenge(responsibility, 'Can become burdened or pessimistic').
trait_challenge(practicality, 'May miss creative or spiritual dimensions').
trait_challenge(originality, 'Can become rebellious for its own sake').
trait_challenge(humanitarianism, 'May become detached from personal life').
trait_challenge(rebellion, 'Can become contrarian or disruptive').
trait_challenge(innovation, 'May neglect tradition or basics').
trait_challenge(compassion, 'Can become escapist or overly selfless').
trait_challenge(imagination, 'May become impractical or delusional').
trait_challenge(spirituality, 'Can become overly mystical or ungrounded').
trait_challenge(empathy, 'May absorb others emotions excessively').
trait_challenge(versatility, 'Can lack focus or commitment').
trait_challenge(restlessness, 'May struggle with commitment or routine').

% --- zodiac_strengths/2 ---
% Return the strengths for a zodiac sign.
zodiac_strengths(Sign, Strengths) :-
    zodiac(Sign),
    zodiac_traits(Sign, Traits),
    findall(
        Strength,
        (
            member(Trait, Traits),
            trait_strength(Trait, Strength)
        ),
        Strengths
    ).

% --- zodiac_challenges/2 ---
% Return the challenges for a zodiac sign.
zodiac_challenges(Sign, Challenges) :-
    zodiac(Sign),
    zodiac_traits(Sign, Traits),
    findall(
        Challenge,
        (
            member(Trait, Traits),
            trait_challenge(Trait, Challenge)
        ),
        Challenges
    ).

% ============================================================
% SECTION 3: Zodiac Profile Generation
% ============================================================

% --- zodiac_profile/2 ---
% Build a complete zodiac profile from a sign.
zodiac_profile(Sign, Profile) :-
    zodiac(Sign),
    element(Sign, Element),
    modality(Sign, Modality),
    ruling_planet(Sign, Planet),
    zodiac_traits(Sign, Traits),
    zodiac_strengths(Sign, Strengths),
    zodiac_challenges(Sign, Challenges),
    zodiac_date_range(Sign, DateRange),
    Profile = zodiac_profile{
        sign: Sign,
        element: Element,
        modality: Modality,
        ruling_planet: Planet,
        traits: Traits,
        strengths: Strengths,
        challenges: Challenges,
        date_range: DateRange
    }.

% --- generate_profile/2 ---
% Higher-level predicate that builds a rich profile
% combining multiple facts and inference rules.
generate_profile(Sign, Profile) :-
    zodiac_profile(Sign, BaseProfile),
    element(Sign, Element),
    modality(Sign, Modality),
    ruling_planet(Sign, Planet),
    % Derive element-based personality style
    element_personality(Element, Personality),
    % Derive modality-based approach
    modality_approach(Modality, Approach),
    % Derive planetary influence
    planetary_influence(Planet, Influence),
    Profile = generated_profile{
        sign: Sign,
        base_profile: BaseProfile,
        personality_style: Personality,
        approach_to_life: Approach,
        planetary_influence: Influence
    }.

% ============================================================
% SECTION 4: Element Personality Derivation
% ============================================================

element_personality(fire, 'Passionate, dynamic, and temperamental. Fire signs tend to be energetic, spontaneous, and natural leaders who act on instinct and enthusiasm.').
element_personality(earth, 'Grounded, practical, and reliable. Earth signs value stability, security, and tangible results. They work steadily toward their goals with patience and determination.').
element_personality(air, 'Intellectual, communicative, and social. Air signs thrive on ideas, connections, and social interaction. They are natural communicators who value mental stimulation.').
element_personality(water, 'Intuitive, emotional, and deep. Water signs are sensitive, empathetic, and connected to their inner world. They navigate life through feelings and intuition.').

% ============================================================
% SECTION 5: Modality Approach Derivation
% ============================================================

modality_approach(cardinal, 'Initiating and pioneering. Cardinal signs start new projects and seasons. They are natural leaders who prefer to begin rather than follow.').
modality_approach(fixed, 'Stabilizing and sustaining. Fixed signs maintain and solidify. They are reliable and determined, providing consistency and structure.').
modality_approach(mutable, 'Adapting and transitioning. Mutable signs are flexible and versatile. They adjust to change easily and serve as bridges between phases.').

% ============================================================
% SECTION 6: Planetary Influence
% ============================================================

planetary_influence(mars, 'Mars brings energy, drive, and assertiveness. The Martian influence adds courage and a warrior spirit, but can also bring impulsiveness and conflict.').
planetary_influence(venus, 'Venus brings beauty, harmony, and love. The Venusian influence adds charm, sensuality, and appreciation for aesthetics, but can also bring indulgence.').
planetary_influence(mercury, 'Mercury brings communication, intellect, and adaptability. The Mercurial influence adds quick thinking and curiosity, but can also bring restlessness.').
planetary_influence(moon, 'The Moon brings intuition, emotion, and nurturing. The Lunar influence adds sensitivity and empathy, but can also bring moodiness.').
planetary_influence(sun, 'The Sun brings vitality, confidence, and leadership. The Solar influence adds warmth and creativity, but can also bring pride.').
planetary_influence(pluto, 'Pluto brings transformation, depth, and power. The Plutonian influence adds intensity and resourcefulness, but can also bring obsession.').
planetary_influence(jupiter, 'Jupiter brings expansion, optimism, and wisdom. The Jovian influence adds generosity and philosophy, but can also bring excess.').
planetary_influence(saturn, 'Saturn brings discipline, structure, and responsibility. The Saturnian influence adds maturity and ambition, but can also bring restriction.').
planetary_influence(uranus, 'Uranus brings innovation, rebellion, and freedom. The Uranian influence adds originality and humanitarianism, but can also bring unpredictability.').
planetary_influence(neptune, 'Neptune brings spirituality, imagination, and compassion. The Neptunian influence adds dreams and empathy, but can also bring escapism.').

% ============================================================
% SECTION 7: Birth Date to Zodiac Sign
% ============================================================

% --- zodiac_from_date/3 ---
% Determine zodiac sign from birth month and day.
% Uses standard Western tropical zodiac date boundaries.

zodiac_from_date(Month, Day, aries) :- Month =:= 3, Day >= 21, !.
zodiac_from_date(Month, Day, aries) :- Month =:= 4, Day =< 19, !.
zodiac_from_date(Month, Day, taurus) :- Month =:= 4, Day >= 20, !.
zodiac_from_date(Month, Day, taurus) :- Month =:= 5, Day =< 20, !.
zodiac_from_date(Month, Day, gemini) :- Month =:= 5, Day >= 21, !.
zodiac_from_date(Month, Day, gemini) :- Month =:= 6, Day =< 20, !.
zodiac_from_date(Month, Day, cancer) :- Month =:= 6, Day >= 21, !.
zodiac_from_date(Month, Day, cancer) :- Month =:= 7, Day =< 22, !.
zodiac_from_date(Month, Day, leo) :- Month =:= 7, Day >= 23, !.
zodiac_from_date(Month, Day, leo) :- Month =:= 8, Day =< 22, !.
zodiac_from_date(Month, Day, virgo) :- Month =:= 8, Day >= 23, !.
zodiac_from_date(Month, Day, virgo) :- Month =:= 9, Day =< 22, !.
zodiac_from_date(Month, Day, libra) :- Month =:= 9, Day >= 23, !.
zodiac_from_date(Month, Day, libra) :- Month =:= 10, Day =< 22, !.
zodiac_from_date(Month, Day, scorpio) :- Month =:= 10, Day >= 23, !.
zodiac_from_date(Month, Day, scorpio) :- Month =:= 11, Day =< 21, !.
zodiac_from_date(Month, Day, sagittarius) :- Month =:= 11, Day >= 22, !.
zodiac_from_date(Month, Day, sagittarius) :- Month =:= 12, Day =< 21, !.
zodiac_from_date(Month, Day, capricorn) :- Month =:= 12, Day >= 22, !.
zodiac_from_date(Month, Day, capricorn) :- Month =:= 1, Day =< 19, !.
zodiac_from_date(Month, Day, aquarius) :- Month =:= 1, Day >= 20, !.
zodiac_from_date(Month, Day, aquarius) :- Month =:= 2, Day =< 18, !.
zodiac_from_date(Month, Day, pisces) :- Month =:= 2, Day >= 19, !.
zodiac_from_date(Month, Day, pisces) :- Month =:= 3, Day =< 20, !.

% ============================================================
% SECTION 8: Extensible Chart Profile
% ============================================================
% The chart profile distinguishes between what is known
% from birth date and what requires birth time/location.
%
% Known from birth date:
%   - Sun sign (zodiac sign)
%   - Element
%   - Modality
%   - Ruling planet
%   - Symbolic traits
%
% Requires birth time/location (NOT calculated in V1):
%   - Moon sign
%   - Rising sign (Ascendant)
%   - House placements
%   - Aspect patterns

% --- chart_profile/3 ---
% Build an extensible chart profile.
% BirthTime = unknown | time(Hour, Minute)
% BirthLocation = unknown | location(Lat, Lon)

chart_profile(Sign, BirthTime, BirthLocation, Chart) :-
    zodiac_profile(Sign, Profile),
    element(Sign, Element),
    modality(Sign, Modality),
    ruling_planet(Sign, Planet),
    % Sun sign is always known from birth date
    Known = [sun_sign, element, modality, ruling_planet, traits],
    % Determine what additional info is available
    (   BirthTime = unknown
    ->  Additional = [],
        MoonSign = unknown,
        RisingSign = unknown,
        Note = 'Moon and Rising signs require birth time. Sun sign and element are derived from birth date.'
    ;   Additional = [moon_sign, rising_sign],
        MoonSign = calculated,
        RisingSign = calculated,
        Note = 'Full chart calculation available with birth time.'
    ),
    append(Known, Additional, Available),
    Chart = chart_profile{
        sun_sign: Sign,
        element: Element,
        modality: Modality,
        ruling_planet: Planet,
        traits: Profile.traits,
        moon_sign: MoonSign,
        rising_sign: RisingSign,
        available_data: Available,
        note: Note
    }.

% ============================================================
% SECTION 9: Element & Modality Compatibility
% ============================================================

% --- element_compatibility/3 ---
% Score element pair compatibility on a symbolic scale.

element_compatibility(fire, fire, supportive) :- !.
element_compatibility(fire, air, supportive) :- !.
element_compatibility(air, fire, supportive) :- !.
element_compatibility(air, air, supportive) :- !.
element_compatibility(earth, earth, supportive) :- !.
element_compatibility(earth, water, supportive) :- !.
element_compatibility(water, earth, supportive) :- !.
element_compatibility(water, water, supportive) :- !.
element_compatibility(fire, earth, moderate) :- !.
element_compatibility(earth, fire, moderate) :- !.
element_compatibility(fire, water, challenging) :- !.
element_compatibility(water, fire, challenging) :- !.
element_compatibility(air, earth, moderate) :- !.
element_compatibility(earth, air, moderate) :- !.
element_compatibility(air, water, moderate) :- !.
element_compatibility(water, air, moderate) :- !.

% --- modality_compatibility/3 ---
% Score modality pair compatibility.

modality_compatibility(cardinal, cardinal, moderate) :- !.
modality_compatibility(cardinal, fixed, supportive) :- !.
modality_compatibility(cardinal, mutable, supportive) :- !.
modality_compatibility(fixed, cardinal, supportive) :- !.
modality_compatibility(fixed, fixed, challenging) :- !.
modality_compatibility(fixed, mutable, moderate) :- !.
modality_compatibility(mutable, cardinal, supportive) :- !.
modality_compatibility(mutable, fixed, moderate) :- !.
modality_compatibility(mutable, mutable, supportive) :- !.

% ============================================================
% SECTION 10: Birth Chart Calculation
% ============================================================
% Calculates Moon sign and Rising sign from birth date and time.
% Uses simplified symbolic ephemeris (approximation for entertainment).

% --- Moon Sign Calculation ---
% The Moon moves approximately 13 degrees per day through the zodiac.
% We use a simplified day-of-year to Moon sign mapping.

% Day ranges for Moon signs (approximate, for symbolic entertainment).
% In reality, Moon position requires astronomical ephemeris.
% This uses a repeating cycle that produces plausible Moon placements.

moon_sign_from_doy(DOY, aries) :- DOY mod 28 =< 2, !.
moon_sign_from_doy(DOY, taurus) :- DOY mod 28 =< 5, DOY mod 28 > 2, !.
moon_sign_from_doy(DOY, gemini) :- DOY mod 28 =< 7, DOY mod 28 > 5, !.
moon_sign_from_doy(DOY, cancer) :- DOY mod 28 =< 9, DOY mod 28 > 7, !.
moon_sign_from_doy(DOY, leo) :- DOY mod 28 =< 11, DOY mod 28 > 9, !.
moon_sign_from_doy(DOY, virgo) :- DOY mod 28 =< 13, DOY mod 28 > 11, !.
moon_sign_from_doy(DOY, libra) :- DOY mod 28 =< 15, DOY mod 28 > 13, !.
moon_sign_from_doy(DOY, scorpio) :- DOY mod 28 =< 17, DOY mod 28 > 15, !.
moon_sign_from_doy(DOY, sagittarius) :- DOY mod 28 =< 19, DOY mod 28 > 17, !.
moon_sign_from_doy(DOY, capricorn) :- DOY mod 28 =< 21, DOY mod 28 > 19, !.
moon_sign_from_doy(DOY, aquarius) :- DOY mod 28 =< 24, DOY mod 28 > 21, !.
moon_sign_from_doy(DOY, pisces) :- DOY mod 28 > 24, !.

% --- Day of Year Calculation ---
day_of_year(Month, Day, DOY) :-
    Month =:= 1, DOY = Day, ! ;
    Month =:= 2, DOY is 31 + Day, ! ;
    Month =:= 3, DOY is 59 + Day, ! ;
    Month =:= 4, DOY is 90 + Day, ! ;
    Month =:= 5, DOY is 120 + Day, ! ;
    Month =:= 6, DOY is 151 + Day, ! ;
    Month =:= 7, DOY is 181 + Day, ! ;
    Month =:= 8, DOY is 212 + Day, ! ;
    Month =:= 9, DOY is 243 + Day, ! ;
    Month =:= 10, DOY is 273 + Day, ! ;
    Month =:= 11, DOY is 304 + Day, ! ;
    Month =:= 12, DOY is 334 + Day, !.

% --- Rising Sign Calculation ---
% Rising sign changes approximately every 2 hours.
% We use birth hour to approximate the Ascendant sign.
% Hour 0-1 = same as hour 2, etc.

% NOTE: this used to special-case H < 2 by recursing into rising_from_hour(2, _),
% which gave aries a 4-hour slot (0-3) while every other sign got 2 hours,
% and the final catch-all (aquarius) silently absorbed hours 22-23 that
% should belong to the 12th sign — pisces was never reachable for any hour.
% Rewritten as 12 clean, non-overlapping 2-hour slots covering all of 0-23.
rising_from_hour(Hour, Sign) :-
    H is Hour mod 24,
    Slot is H // 2,
    rising_slot(Slot, Sign).

rising_slot(0, aries).
rising_slot(1, taurus).
rising_slot(2, gemini).
rising_slot(3, cancer).
rising_slot(4, leo).
rising_slot(5, virgo).
rising_slot(6, libra).
rising_slot(7, scorpio).
rising_slot(8, sagittarius).
rising_slot(9, capricorn).
rising_slot(10, aquarius).
rising_slot(11, pisces).

% --- calculate_moon_sign/3 ---
% Calculate Moon sign from birth month and day.

calculate_moon_sign(Month, Day, MoonSign) :-
    day_of_year(Month, Day, DOY),
    moon_sign_from_doy(DOY, MoonSign).

% --- calculate_rising_sign/2 ---
% Calculate Rising sign from birth hour (24h format).

calculate_rising_sign(Hour, RisingSign) :-
    rising_from_hour(Hour, RisingSign).

% --- full_birth_chart/5 ---
% Complete birth chart calculation.
% Requires: Month, Day, Hour (24h format)
% Returns: Sun sign, Moon sign, Rising sign, element, modality

full_birth_chart(Month, Day, Hour, SunSign, Chart) :-
    zodiac_from_date(Month, Day, SunSign),
    calculate_moon_sign(Month, Day, MoonSign),
    calculate_rising_sign(Hour, RisingSign),
    element(SunSign, Element),
    modality(SunSign, Modality),
    ruling_planet(SunSign, Planet),
    zodiac_traits(SunSign, Traits),
    element(SunSign, Elem),
    element_personality(Elem, Personality),
    modality_approach(Modality, Approach),
    planetary_influence(Planet, Influence),
    % Moon element
    element(MoonSign, MoonElem),
    % Rising element
    element(RisingSign, RisingElem),
    Chart = birth_chart{
        sun_sign: SunSign,
        moon_sign: MoonSign,
        rising_sign: RisingSign,
        element: Element,
        modality: Modality,
        ruling_planet: Planet,
        traits: Traits,
        personality_style: Personality,
        approach_to_life: Approach,
        planetary_influence: Influence,
        moon_element: MoonElem,
        rising_element: RisingElem,
        note: 'Moon and Rising signs are approximations for symbolic entertainment. Exact positions require astronomical ephemeris.'
    }.

% --- birth_chart_reasoning_trace/4 ---
% Generate reasoning trace for birth chart calculation.

birth_chart_reasoning_trace(Month, Day, Hour, Trace) :-
    zodiac_from_date(Month, Day, SunSign),
    calculate_moon_sign(Month, Day, MoonSign),
    calculate_rising_sign(Hour, RisingSign),
    element(SunSign, Element),
    element(MoonSign, MoonElem),
    element(RisingSign, RisingElem),
    day_of_year(Month, Day, DOY),
    Trace = [
        reasoning_step{
            rule: format('zodiac_from_date(~w, ~w, ~w)', [Month, Day, SunSign]),
            input: format('~w/~w', [Month, Day]),
            result: format('Sun sign: ~w', [SunSign]),
            explanation: 'Sun sign is derived from birth date using standard zodiac boundaries'
        },
        reasoning_step{
            rule: format('day_of_year(~w, ~w, ~w)', [Month, Day, DOY]),
            input: format('~w/~w', [Month, Day]),
            result: format('Day of year: ~w', [DOY]),
            explanation: 'Day of year is used to approximate Moon position'
        },
        reasoning_step{
            rule: format('calculate_moon_sign(~w, ~w, ~w)', [Month, Day, MoonSign]),
            input: format('~w/~w (DOY ~w)', [Month, Day, DOY]),
            result: format('Moon sign: ~w', [MoonSign]),
            explanation: 'Moon sign is approximated from day-of-year cycle (Moon moves ~13 degrees/day)'
        },
        reasoning_step{
            rule: format('calculate_rising_sign(~w, ~w)', [Hour, RisingSign]),
            input: format('Hour ~w', [Hour]),
            result: format('Rising sign: ~w', [RisingSign]),
            explanation: 'Rising sign is approximated from birth hour (Ascendant changes every ~2 hours)'
        },
        reasoning_step{
            rule: format('element(~w, ~w)', [SunSign, Element]),
            input: SunSign,
            result: format('Sun element: ~w', [Element]),
            explanation: 'Core element from Sun sign'
        },
        reasoning_step{
            rule: format('element(~w, ~w)', [MoonSign, MoonElem]),
            input: MoonSign,
            result: format('Moon element: ~w', [MoonElem]),
            explanation: 'Moon element adds emotional layer'
        },
        reasoning_step{
            rule: format('element(~w, ~w)', [RisingSign, RisingElem]),
            input: RisingSign,
            result: format('Rising element: ~w', [RisingElem]),
            explanation: 'Rising element shows outward presentation'
        }
    ].

% --- full_birth_chart_precise/4 ---
% Complete birth chart built from Sun/Moon/Rising signs that were already
% computed from real ecliptic longitudes (Swiss Ephemeris, in Python) —
% unlike full_birth_chart/5, this predicate does no date/hour approximation
% of its own, it only derives the symbolic layer (element, traits, etc.)
% from the given signs.

full_birth_chart_precise(SunSign, MoonSign, RisingSign, Chart) :-
    zodiac(SunSign),
    element(SunSign, Element),
    modality(SunSign, Modality),
    ruling_planet(SunSign, Planet),
    zodiac_traits(SunSign, Traits),
    element_personality(Element, Personality),
    modality_approach(Modality, Approach),
    planetary_influence(Planet, Influence),
    element(MoonSign, MoonElem),
    element(RisingSign, RisingElem),
    Chart = birth_chart{
        sun_sign: SunSign,
        moon_sign: MoonSign,
        rising_sign: RisingSign,
        element: Element,
        modality: Modality,
        ruling_planet: Planet,
        traits: Traits,
        personality_style: Personality,
        approach_to_life: Approach,
        planetary_influence: Influence,
        moon_element: MoonElem,
        rising_element: RisingElem,
        note: 'Sun, Moon, and Rising signs computed from real ecliptic positions via the Swiss Ephemeris (Moshier method).'
    }.

% --- birth_chart_reasoning_trace_precise/7 ---
% Reasoning trace for the ephemeris-backed chart above.

birth_chart_reasoning_trace_precise(SunSign, MoonSign, RisingSign, SunDeg, MoonDeg, RisingDeg, Trace) :-
    element(SunSign, Element),
    element(MoonSign, MoonElem),
    element(RisingSign, RisingElem),
    format(atom(SunInput), 'ecliptic longitude ~w degrees', [SunDeg]),
    format(atom(SunResult), 'Sun sign: ~w', [SunSign]),
    format(atom(MoonInput), 'ecliptic longitude ~w degrees', [MoonDeg]),
    format(atom(MoonResult), 'Moon sign: ~w', [MoonSign]),
    format(atom(RisingInput), 'ascendant longitude ~w degrees', [RisingDeg]),
    format(atom(RisingResult), 'Rising sign: ~w', [RisingSign]),
    format(atom(SunElemRule), 'element(~w, ~w)', [SunSign, Element]),
    format(atom(SunElemResult), 'Sun element: ~w', [Element]),
    format(atom(MoonElemRule), 'element(~w, ~w)', [MoonSign, MoonElem]),
    format(atom(MoonElemResult), 'Moon element: ~w', [MoonElem]),
    format(atom(RisingElemRule), 'element(~w, ~w)', [RisingSign, RisingElem]),
    format(atom(RisingElemResult), 'Rising element: ~w', [RisingElem]),
    Trace = [
        reasoning_step{
            rule: 'swisseph.calc_ut(jd, SUN, FLG_MOSEPH)',
            input: SunInput,
            result: SunResult,
            explanation: 'Sun sign from the Sun''s real ecliptic longitude at birth (UTC), 30 degrees per sign'
        },
        reasoning_step{
            rule: 'swisseph.calc_ut(jd, MOON, FLG_MOSEPH)',
            input: MoonInput,
            result: MoonResult,
            explanation: 'Moon sign from the Moon''s real ecliptic longitude at birth (UTC), computed from date, time, and location'
        },
        reasoning_step{
            rule: 'swisseph.houses_ex(jd, latitude, longitude, hsys=Placidus)',
            input: RisingInput,
            result: RisingResult,
            explanation: 'Rising sign is the zodiac sign on the eastern horizon at birth, computed from birth time and geographic coordinates'
        },
        reasoning_step{
            rule: SunElemRule,
            input: SunSign,
            result: SunElemResult,
            explanation: 'Core element from Sun sign'
        },
        reasoning_step{
            rule: MoonElemRule,
            input: MoonSign,
            result: MoonElemResult,
            explanation: 'Moon element adds emotional layer'
        },
        reasoning_step{
            rule: RisingElemRule,
            input: RisingSign,
            result: RisingElemResult,
            explanation: 'Rising element shows outward presentation'
        }
    ].

% ============================================================
% SECTION 11: Reasoning Trace Generation
% ============================================================

% --- profile_reasoning_trace/2 ---
% Generate a reasoning trace for profile generation.

profile_reasoning_trace(Sign, Trace) :-
    zodiac(Sign),
    element(Sign, Element),
    modality(Sign, Modality),
    ruling_planet(Sign, Planet),
    zodiac_traits(Sign, Traits),
    element_personality(Element, Personality),
    modality_approach(Modality, Approach),
    planetary_influence(Planet, Influence),
    Trace = [
        reasoning_step{
            rule: format('zodiac(~w)', [Sign]),
            input: Sign,
            result: 'Zodiac sign identified',
            explanation: format('~w is a valid zodiac sign', [Sign])
        },
        reasoning_step{
            rule: format('element(~w, ~w)', [Sign, Element]),
            input: Sign,
            result: format('~w belongs to ~w element', [Sign, Element]),
            explanation: format('The ~w element defines ~w personality style', [Element, Sign])
        },
        reasoning_step{
            rule: format('modality(~w, ~w)', [Sign, Modality]),
            input: Sign,
            result: format('~w has ~w modality', [Sign, Modality]),
            explanation: format('~w modality means ~w approaches life through initiating energy', [Modality, Sign])
        },
        reasoning_step{
            rule: format('ruling_planet(~w, ~w)', [Sign, Planet]),
            input: Sign,
            result: format('~w is ruled by ~w', [Sign, Planet]),
            explanation: format('~w influence adds specific energy to ~w', [Planet, Sign])
        },
        reasoning_step{
            rule: format('zodiac_traits(~w, ~w)', [Sign, Traits]),
            input: Sign,
            result: format('~w traits: ~w', [Sign, Traits]),
            explanation: 'Symbolic traits define the core personality dimensions'
        }
    ].

% --- date_reasoning_trace/3 ---
% Generate a reasoning trace for birth date to zodiac.

date_reasoning_trace(Month, Day, Trace) :-
    zodiac_from_date(Month, Day, Sign),
    element(Sign, Element),
    Trace = [
        reasoning_step{
            rule: format('zodiac_from_date(~w, ~w, ~w)', [Month, Day, Sign]),
            input: format('~w/~w', [Month, Day]),
            result: format('Birth date maps to ~w', [Sign]),
            explanation: format('~w falls within ~w zodiac range', [format('~w/~w', [Month, Day]), Sign])
        },
        reasoning_step{
            rule: format('element(~w, ~w)', [Sign, Element]),
            input: Sign,
            result: format('~w belongs to ~w element', [Sign, Element]),
            explanation: 'Element is derived from the zodiac sign'
        }
    ].
