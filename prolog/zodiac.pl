% ============================================================
% Zodiac Knowledge Base - AstroLogic
% Complete representation of all 12 zodiac signs
% ============================================================

% --- Zodiac Signs ---
zodiac(aries).
zodiac(taurus).
zodiac(gemini).
zodiac(cancer).
zodiac(leo).
zodiac(virgo).
zodiac(libra).
zodiac(scorpio).
zodiac(sagittarius).
zodiac(capricorn).
zodiac(aquarius).
zodiac(pisces).

% --- Elements ---
element(aries, fire).
element(taurus, earth).
element(gemini, air).
element(cancer, water).
element(leo, fire).
element(virgo, earth).
element(libra, air).
element(scorpio, water).
element(sagittarius, fire).
element(capricorn, earth).
element(aquarius, air).
element(pisces, water).

% --- Modalities ---
modality(aries, cardinal).
modality(taurus, fixed).
modality(gemini, mutable).
modality(cancer, cardinal).
modality(leo, fixed).
modality(virgo, mutable).
modality(libra, cardinal).
modality(scorpio, fixed).
modality(sagittarius, mutable).
modality(capricorn, cardinal).
modality(aquarius, fixed).
modality(pisces, mutable).

% --- Ruling Planets ---
ruling_planet(aries, mars).
ruling_planet(taurus, venus).
ruling_planet(gemini, mercury).
ruling_planet(cancer, moon).
ruling_planet(leo, sun).
ruling_planet(virgo, mercury).
ruling_planet(libra, venus).
ruling_planet(scorpio, pluto).
ruling_planet(sagittarius, jupiter).
ruling_planet(capricorn, saturn).
ruling_planet(aquarius, uranus).
ruling_planet(pisces, neptune).

% --- Symbolic Traits ---
zodiac_traits(aries, [courage, initiative, independence, impulsiveness, leadership]).
zodiac_traits(taurus, [patience, reliability, sensuality, stubbornness, determination]).
zodiac_traits(gemini, [curiosity, adaptability, communication, restlessness, versatility]).
zodiac_traits(cancer, [intuition, nurturing, sensitivity, moodiness, loyalty]).
zodiac_traits(leo, [creativity, generosity, confidence, pride, warmth]).
zodiac_traits(virgo, [analytical, practical, modesty, perfectionism, helpfulness]).
zodiac_traits(libra, [diplomacy, fairness, charm, indecisiveness, harmony]).
zodiac_traits(scorpio, [intensity, resourcefulness, passion, secrecy, depth]).
zodiac_traits(sagittarius, [adventure, optimism, freedom, restlessness, philosophical]).
zodiac_traits(capricorn, [ambition, discipline, responsibility, pessimism, practicality]).
zodiac_traits(aquarius, [originality, humanitarianism, detachment, rebellion, innovation]).
zodiac_traits(pisces, [compassion, imagination, spirituality, escapism, empathy]).

% --- Date Ranges ---
zodiac_date_range(aries, 'Mar 21 - Apr 19').
zodiac_date_range(taurus, 'Apr 20 - May 20').
zodiac_date_range(gemini, 'May 21 - Jun 20').
zodiac_date_range(cancer, 'Jun 21 - Jul 22').
zodiac_date_range(leo, 'Jul 23 - Aug 22').
zodiac_date_range(virgo, 'Aug 23 - Sep 22').
zodiac_date_range(libra, 'Sep 23 - Oct 22').
zodiac_date_range(scorpio, 'Oct 23 - Nov 21').
zodiac_date_range(sagittarius, 'Nov 22 - Dec 21').
zodiac_date_range(capricorn, 'Dec 22 - Jan 19').
zodiac_date_range(aquarius, 'Jan 20 - Feb 18').
zodiac_date_range(pisces, 'Feb 19 - Mar 20').

% --- Zodiac Symbol Unicode ---
zodiac_symbol(aries, '\u2648').
zodiac_symbol(taurus, '\u2649').
zodiac_symbol(gemini, '\u264A').
zodiac_symbol(cancer, '\u264B').
zodiac_symbol(leo, '\u264C').
zodiac_symbol(virgo, '\u264D').
zodiac_symbol(libra, '\u264E').
zodiac_symbol(scorpio, '\u264F').
zodiac_symbol(sagittarius, '\u2650').
zodiac_symbol(capricorn, '\u2651').
zodiac_symbol(aquarius, '\u2652').
zodiac_symbol(pisces, '\u2653').

% --- Helper: Get all signs of a given element ---
signs_of_element(Element, Signs) :-
    findall(Sign, element(Sign, Element), Signs).

% --- Helper: Get all signs of a given modality ---
signs_of_modality(Modality, Signs) :-
    findall(Sign, modality(Sign, Modality), Signs).
