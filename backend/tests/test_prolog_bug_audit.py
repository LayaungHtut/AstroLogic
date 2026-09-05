"""Regression tests for the Prolog logic-bug audit: 11 confirmed bugs found
by systematically re-reading and live-testing the whole rule base, on top of
the bugs already caught earlier in this project. Each test locks in one bug.
"""

from app.services.prolog_service import PrologService, _first_result, _safe_query
from app.services.tarot_service import TarotService


class TestModifyKeywordReversed:
    """Each clause head bound its 2nd arg against a literal atom like
    `blocked_K` (K as plain text, not the variable) instead of the atom
    atom_concat/3 actually built in the body — every call failed, so every
    reversed card's keyword list came back empty."""

    def test_produces_a_real_modified_keyword(self):
        result = _first_result("modify_keyword_reversed(new_beginnings, X)")
        assert result is not None
        assert result["X"] == "reversed_new_beginnings"

    def test_reversed_cards_have_nonempty_keywords(self):
        analysis = PrologService.analyze_card("the_fool", "reversed")
        assert analysis is not None
        assert len(analysis["keywords"]) > 0


class TestSixOfWandsSingletonVariable:
    """`Lack_of_recognition` (capitalized) parsed as an unbound variable, not
    the intended atom — its value leaked into the API as e.g. "_22932"."""

    def test_no_leaked_variable_in_meaning(self):
        analysis = PrologService.analyze_card("six_of_wands", "reversed")
        assert analysis is not None
        for field in ("meaning", "positive_aspects", "challenging_aspects"):
            for value in analysis[field]:
                assert not value.startswith("_"), f"leaked unbound var in {field}: {value!r}"
        assert "lack_of_recognition" in analysis["meaning"]


class TestSpreadPositionNormalization:
    """spread_rules.pl's spread_positions/2 (capitalized: 'Current Position')
    shadows card_selection.pl's own (lowercase) definition of the same
    predicate/arity, but position_meaning_modifier/2 and
    position_theme_emphasis/2 are keyed on the lowercase atoms — so every
    real spread's positions failed to match at all."""

    def test_conversion_matches_every_position_fact(self):
        display_positions = [
            "Guidance", "Past", "Present", "Future",
            "Current Situation", "Path A", "Path B", "Advice",
            "Current Self", "Hidden Influence", "What to Understand",
            "You", "Other Person", "Connection", "Challenge",
            "Current Position", "Strength", "Opportunity",
        ]
        for label in display_positions:
            atom = TarotService.to_prolog_position_atom(label)
            assert _first_result(f"position_meaning_modifier({atom}, _)") is not None, (
                f"{label!r} -> {atom!r} has no position_meaning_modifier fact"
            )

    def test_interpret_card_position_succeeds_for_every_real_spread_position(self):
        for atom in [
            "current_situation", "path_a", "path_b", "current_self", "you",
            "other_person", "current_position", "opportunity",
        ]:
            result = PrologService.interpret_card_position("the_fool", atom, "upright")
            assert result is not None, f"interpret_card_position failed for position {atom!r}"


class TestNoDuplicateCardInterpretations:
    """position_meaning_modifier/2 has two facts each for 'challenge' (career
    vs. relationship spreads) and 'advice' (decision vs. career spreads), and
    position_theme_emphasis/2 ends in a catch-all fact — without once/1 on
    both, backtracking produced two card_position_interpretation dicts per
    card for any reused position name."""

    def test_career_spread_produces_exactly_one_interpretation_per_card(self):
        cards = ["the_fool", "the_magician", "death", "justice", "the_sun"]
        positions = ["current_position", "strength", "challenge", "opportunity", "advice"]
        orientations = ["upright"] * 5
        result = _first_result(
            f"analyze_reading_oriented({cards}, {positions}, {orientations}, A)"
        )
        assert len(result["A"]["card_interpretations"]) == len(cards)

    def test_reused_position_name_yields_single_solution(self):
        for card, position in [("justice", "challenge"), ("the_sun", "advice")]:
            solutions = _safe_query(f"interpret_card_position({card}, {position}, upright, I)")
            assert len(solutions) == 1


class TestReadingDirectionReflectsRealContent:
    """reading_direction/2 only ever bucketed the literal atoms
    positive/challenging/hidden — every other emphasis category
    position_theme_emphasis/2 can actually produce (historical, current,
    emerging, advisory, relational, educational — i.e. every position in a
    three_card, decision, career, or relationship spread) matched none of
    the three buckets, so direction was always 'balanced'."""

    def test_direction_is_optimistic_when_positive_dominates(self):
        cards = ["the_fool", "the_magician", "death", "justice", "the_sun"]
        positions = ["current_position", "strength", "challenge", "opportunity", "advice"]
        result = _first_result(
            f"analyze_reading_oriented({cards}, {positions}, {['upright']*5}, A)"
        )
        assert result["A"]["direction"] == "optimistic"

    def test_direction_is_not_always_balanced(self):
        # A spread with two challenge-emphasis positions and no positive ones.
        cards = ["the_devil", "the_tower"]
        positions = ["challenge", "challenge"]
        result = _first_result(
            f"analyze_reading_oriented({cards}, {positions}, {['upright']*2}, A)"
        )
        assert result["A"]["direction"] == "challenging"


class TestExtractCardThemesCoversMinorArcana:
    """extract_card_themes/2 (recommendation_rules.pl) used to read from
    tarot_themes/2, which is only defined for the 22 major arcana — every
    minor arcana card silently contributed zero themes."""

    def test_minor_arcana_only_reading_has_themes(self):
        result = PrologService.interpret_cards(
            ["ace_of_wands", "two_of_cups", "three_of_swords"], "aries", "career"
        )
        assert result is not None
        assert len(result["themes"]) > 0


class TestWheelOfFortuneAtomTypo:
    """recommendation_rules.pl referred to 'the_wheel_of_fortune' in seven
    places; the real card atom (per tarot.pl) is 'wheel_of_fortune' with no
    'the_' prefix — every zodiac/category/mood affinity check for that card
    silently failed to match."""

    def test_card_exists_under_the_correct_atom(self):
        assert _first_result("tarot_card(wheel_of_fortune, _, _)") is not None

    def test_zodiac_affinity_resolves(self):
        assert _first_result("zodiac_card(gemini, wheel_of_fortune)") is not None

    def test_category_and_mood_affinity_resolve(self):
        assert _first_result("category_card_affinity(decision, wheel_of_fortune)") is not None
        assert _first_result("mood_card(neutral, wheel_of_fortune)") is not None


class TestGenerateCompatibilityTraceNotEmpty:
    """The trace's findall/3 checked `member(step, [step(...), step(...)])`
    — the bare atom `step` against a list of step(_,_) compounds, which can
    never unify — and never bound its RuleStr/ResultStr output variables
    anywhere, so the trace was always []."""

    def test_trace_has_seven_steps(self):
        trace = PrologService.generate_compatibility_trace("aries", "leo")
        assert len(trace) == 7
        for step in trace:
            assert step["rule"]
            assert step["result"]


class TestUnevaluatedLengthCalls:
    """reading_summary/2, reading_analysis_trace/3, and
    select_cards_reasoning/4 all passed `length(List)` directly as a dict
    value or format/2 arg without ever calling length(List, N) — the field
    held the literal unevaluated term instead of a count."""

    def test_reading_summary_counts_are_integers(self):
        summary = PrologService.get_reading_summary(["the_fool", "the_magician", "death"])
        assert summary is not None
        assert summary["card_count"] == 3
        assert isinstance(summary["conflict_count"], int)
        assert "length(" not in summary["conflict_note"]

    def test_reading_analysis_trace_has_no_leaked_length_calls(self):
        trace = PrologService.get_reading_analysis_trace(["the_fool", "the_magician"], ["past", "present"])
        for step in trace:
            for field in ("rule", "result"):
                assert "length(" not in step[field], f"leaked length() in {field}: {step[field]!r}"

    def test_select_cards_reasoning_has_no_leaked_length_calls(self):
        trace = PrologService.get_select_cards_reasoning("leo", "career")
        for step in trace:
            assert "length(" not in step["result"]


class TestRisingSignCoversAllTwelveSigns:
    """rising_from_hour/2 special-cased H < 2 by recursing into hour 2,
    giving aries a 4-hour slot while every other sign got 2 — and the final
    catch-all (aquarius) absorbed the 2 hours that should have gone to the
    never-reachable 12th sign, pisces."""

    def test_all_24_hours_produce_a_valid_sign_and_pisces_is_reachable(self):
        seen = set()
        for hour in range(24):
            result = _first_result(f"rising_from_hour({hour}, S)")
            assert result is not None
            seen.add(result["S"])
        assert seen == {
            "aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra",
            "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
        }

    def test_each_sign_gets_exactly_two_hours(self):
        from collections import Counter
        counts = Counter()
        for hour in range(24):
            result = _first_result(f"rising_from_hour({hour}, S)")
            counts[result["S"]] += 1
        assert all(count == 2 for count in counts.values())
