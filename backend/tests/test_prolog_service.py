"""Tests for the Prolog query-building/decoding helpers and a handful of
representative PrologService queries.

These exist mainly to lock in two bugs fixed in this pass:
  1. Query injection via unescaped/unquoted string interpolation into
     Prolog query strings (see `_quote_atom`).
  2. Stringified, unevaluated `format(Template, Args)` terms leaking into
     reasoning-trace fields instead of being rendered (see
     `_decode_format_term`).
"""

from app.services.prolog_service import PrologService, _decode_format_term, _quote_atom


class TestQuoteAtom:
    def test_plain_atom_round_trips(self):
        assert _quote_atom("aries") == "'aries'"

    def test_escapes_single_quotes(self):
        assert _quote_atom("it's") == "'it\\'s'"

    def test_escapes_backslashes_before_quotes(self):
        # A value ending in backslash-then-quote must not be able to smuggle
        # an unescaped quote into the surrounding Prolog atom.
        assert _quote_atom("foo\\") == "'foo\\\\'"
        quoted = _quote_atom("foo\\'bar")
        # The quoted form must contain no unescaped `'` other than the two
        # delimiters, whatever the input looked like.
        interior = quoted[1:-1]
        i = 0
        while i < len(interior):
            if interior[i] == "\\":
                i += 2
                continue
            assert interior[i] != "'"
            i += 1


class TestQueryInjectionRegression:
    """Attempted breakouts must fail to match rather than corrupt the query
    or execute unintended goals — never raise, and never behave as if the
    injected goal succeeded."""

    def test_classify_question_survives_quote_breakout_attempt(self):
        result = PrologService.classify_question("test' , true, fail('X")
        assert result == "general"

    def test_get_zodiac_info_rejects_paren_breakout_attempt(self):
        # Previously this parameter was interpolated completely unquoted;
        # a value like this could append arbitrary extra goals to the query.
        result = PrologService.get_zodiac_info("aries), true, X = 1, zodiac_info(taurus")
        assert result is None

    def test_analyze_compatibility_rejects_backslash_quote_breakout(self):
        result = PrologService.analyze_compatibility("aries\\'), true, evil('X", "leo")
        assert result is None

    def test_normal_signs_still_work_after_hardening(self):
        # The fix must not break legitimate atom values.
        assert PrologService.get_zodiac_info("aries") is not None
        assert PrologService.analyze_compatibility("aries", "leo") is not None


class TestDecodeFormatTerm:
    def test_passes_through_plain_strings(self):
        assert _decode_format_term("Sun sign: gemini") == "Sun sign: gemini"
        assert _decode_format_term("swisseph.calc_ut(jd, SUN, FLG_MOSEPH)") == (
            "swisseph.calc_ut(jd, SUN, FLG_MOSEPH)"
        )

    def test_renders_simple_format_term(self):
        assert _decode_format_term("format(Sun sign: ~w, ['gemini'])") == "Sun sign: gemini"

    def test_renders_format_term_with_multiple_args(self):
        assert (
            _decode_format_term("format(zodiac_from_date(~w, ~w, ~w), [6, 15, 'gemini'])")
            == "zodiac_from_date(6, 15, gemini)"
        )

    def test_renders_format_term_with_a_nested_list_argument(self):
        # Regression: a naive greedy-regex split breaks here because it
        # finds the *last* top-level ", [" instead of the true outer one.
        value = (
            "format(~w symbolic traits: ~w, "
            "['aries', ['courage', 'initiative', 'leadership']])"
        )
        assert _decode_format_term(value) == (
            "aries symbolic traits: ['courage', 'initiative', 'leadership']"
        )

    def test_leaves_unparseable_format_term_unchanged(self):
        # A nested unevaluated format(...) term as an arg isn't valid Python
        # literal syntax — must fail safe (return input) rather than raise.
        value = "format(~w falls within ~w, [format('~w/~w', [6, 15]), gemini])"
        assert _decode_format_term(value) == value


class TestReasoningTraceEndToEnd:
    """The reasoning-trace predicates should never leak raw format(...) text."""

    def test_precise_birth_chart_trace_has_no_leaked_format_terms(self):
        trace = PrologService.get_birth_chart_reasoning_precise(
            "gemini", "capricorn", "leo", 84.0317, 298.5437, 145.9785
        )
        assert trace
        for step in trace:
            for field in ("rule", "result", "input", "explanation"):
                assert not step[field].startswith("format(")
