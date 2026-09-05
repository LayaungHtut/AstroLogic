"""Tests for the reading-analysis features added on top of the rule base:
zodiac x tarot affinity, theme conflict detection, reading direction/advice,
topic classification, and card ranking — plus regression coverage for the
bugs found while wiring them up.
"""

from app.services.prolog_service import PrologService
from app.services.tarot_service import TarotService


class TestCardAtomConversion:
    """The Prolog card knowledge base is keyed on snake_case atoms
    (the_hanged_man, ace_of_wands, ...), not the short display codes used
    for images (01, w01, ...). Every drawn card must be converted before
    it's handed to any Prolog predicate, or themes/conflicts/priority all
    silently resolve empty."""

    def test_major_arcana_names_convert(self):
        assert TarotService.to_prolog_card_atom("The Fool") == "the_fool"
        assert TarotService.to_prolog_card_atom("The Hanged Man") == "the_hanged_man"
        assert TarotService.to_prolog_card_atom("Wheel of Fortune") == "wheel_of_fortune"
        assert TarotService.to_prolog_card_atom("Strength") == "strength"

    def test_minor_arcana_names_convert(self):
        assert TarotService.to_prolog_card_atom("Ace of Wands") == "ace_of_wands"
        assert TarotService.to_prolog_card_atom("Ten of Cups") == "ten_of_cups"
        assert TarotService.to_prolog_card_atom("Queen of Swords") == "queen_of_swords"

    def test_converted_atom_actually_matches_the_rule_base(self):
        # The real regression: does the derived atom resolve to real Prolog facts?
        atom = TarotService.to_prolog_card_atom("The Hanged Man")
        assert PrologService.get_card_themes(atom)
        assert PrologService.analyze_card(atom, "upright") is not None


class TestTopicClassifierRegression:
    """classify_topic/2 used `A ; B -> C ; D` without grouping, which parses
    as `A ; (B -> C) ; D` in Prolog — matching keyword A then succeeded the
    whole clause without ever binding Topic, leaving it a dangling unbound
    variable (pyswip printed it as e.g. "_12860")."""

    def test_love_keyword_classifies_correctly(self):
        assert PrologService.classify_topic("Will I find love soon?") == "love"

    def test_career_keyword_classifies_correctly(self):
        assert PrologService.classify_topic("Should I take this job?") == "career"

    def test_result_is_never_a_dangling_variable(self):
        for question in [
            "Will I find love?", "What about my career?", "How is my money?",
            "How can I grow?", "Should I communicate more?", "Random question",
        ]:
            topic = PrologService.classify_topic(question)
            assert not topic.startswith("_"), f"leaked unbound variable for: {question!r}"


class TestCardRankingRegression:
    """select_cards/3 called `context(Category, Sign, Element, Traits)` as a
    bare goal — context/4 is never defined as a predicate, only ever used as
    a data term — so every call raised existence_error and select_cards (and
    everything built on it, including card ranking) always failed."""

    def test_select_eligible_cards_succeeds(self):
        result = PrologService.select_eligible_cards("leo", "relationship")
        assert result is not None
        assert len(result["eligible_cards"]) > 0

    def test_ranked_eligible_cards_are_sorted_descending_by_priority(self):
        ranked = PrologService.get_ranked_eligible_cards("relationship", "leo")
        assert len(ranked) > 0
        priorities = [r["priority"] for r in ranked]
        assert priorities == sorted(priorities, reverse=True)
        assert ranked[0]["rank"] == 1

    def test_a_card_matching_the_signs_affinity_ranks_at_the_top(self):
        # 'strength' is a leo-affine, fire-element, relationship-matching card.
        ranked = PrologService.get_ranked_eligible_cards("relationship", "leo")
        by_card = {r["card"]: r for r in ranked}
        assert "strength" in by_card
        assert by_card["strength"]["priority"] == 6
        assert by_card["strength"]["rank"] == 1


class TestZodiacTarotAffinity:
    def test_returns_a_dict_not_a_leaked_compound_term(self):
        result = PrologService.get_zodiac_tarot_theme("leo", "the_sun")
        assert result is not None
        assert result["zodiac"] == "leo"
        assert result["card"] == "the_sun"
        assert "combined" in result
        assert not result["combined"].startswith("combined_theme(")


class TestThemeConflictDetector:
    def test_detects_a_known_conflicting_pair(self):
        # the_chariot -> action, the_high_priestess -> patience (conflicting).
        conflicts = PrologService.get_reading_card_conflicts(["the_chariot", "the_high_priestess"])
        assert len(conflicts) >= 1
        c = conflicts[0]
        assert c["card1"] == "the_chariot"
        assert c["card2"] == "the_high_priestess"
        assert "title" in c and "description" in c

    def test_no_conflict_returns_empty_list(self):
        conflicts = PrologService.get_reading_card_conflicts(["the_fool"])
        assert conflicts == []


class TestSynastryTraitPairs:
    def test_returns_complementary_pairs(self):
        pairs = PrologService.get_synastry_trait_pairs("aries", "cancer")
        assert {"trait1": "independence", "trait2": "nurturing"} in pairs

    def test_no_result_case_is_a_clean_empty_list_not_an_error(self):
        pairs = PrologService.get_synastry_trait_pairs("aries", "libra")
        assert pairs == []


class TestExplicitSpreadTypeOverridesAutoRecommendation:
    """The reading endpoint always called PrologService.recommend_spread,
    which auto-classifies category from the question text and picks its own
    spread type — any client-chosen spread_type was silently discarded, so
    the UI's spread picker never actually changed anything server-side.
    recommend_spread_for lets the caller pin the spread while still
    classifying the question for category/topic purposes."""

    def test_each_spread_type_is_honored_with_correct_card_count(self):
        expected_counts = {
            "one_card": 1, "three_card": 3, "decision": 4,
            "self_reflection": 4, "relationship": 5, "career": 5,
        }
        for spread_type, count in expected_counts.items():
            rec = PrologService.recommend_spread_for("What should I do?", "leo", spread_type)
            assert rec is not None
            assert rec["spread_type"] == spread_type
            assert rec["card_count"] == count
            assert len(rec["positions"]) == count

    def test_still_classifies_the_question_category(self):
        rec = PrologService.recommend_spread_for("Will I find love?", "leo", "one_card")
        assert rec["category"] == "relationship"
        assert rec["spread_type"] == "one_card"


class TestSynastryScoreBreakdownNoLeakedFormat:
    def test_descriptions_are_rendered_not_raw_format_terms(self):
        breakdown = PrologService.get_compatibility_score_breakdown("aries", "cancer")
        assert breakdown is not None
        for component in ("element", "modality", "traits", "planetary"):
            desc = breakdown[component]["description"]
            assert not desc.startswith("format("), f"{component} leaked a raw format() term"
