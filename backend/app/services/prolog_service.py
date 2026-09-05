from pyswip import Prolog
from pathlib import Path
from app.config import PROLOG_DIR
import ast
import logging
import re

logger = logging.getLogger(__name__)

prolog = Prolog()


def _load_prolog_files():
    pl_files = [
        "zodiac.pl",
        "tarot.pl",
        "zodiac_profile.pl",
        "card_selection.pl",
        "reading_analysis.pl",
        "compatibility.pl",
        "synastry.pl",
        "horoscope_rules.pl",
        "spread_rules.pl",
        "recommendation_rules.pl",
        "reasoning.pl",
        "main.pl",
    ]
    for f in pl_files:
        path = PROLOG_DIR / f
        if path.exists():
            try:
                posix_path = path.as_posix()
                list(prolog.query(f"consult('{posix_path}')"))
                logger.info(f"Loaded Prolog file: {f}")
            except Exception as e:
                logger.error(f"Failed to load {f}: {e}")
        else:
            logger.warning(f"Prolog file not found: {path}")


_load_prolog_files()


def _quote_atom_list(items: list[str]) -> str:
    """Build a Prolog list literal from user-derived strings, each safely quoted."""
    return "[" + ",".join(_quote_atom(item) for item in items) + "]"


def _quote_atom(text: str) -> str:
    """Safely embed arbitrary user text as a single-quoted Prolog atom.

    Backslashes must be escaped *before* quotes, or a value ending in a
    backslash immediately followed by a quote (e.g. "foo\\'") can escape
    the quoting and inject additional Prolog syntax into the query string
    built around it. Escaping only quotes (the old behavior) is not safe.
    """
    escaped = text.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{escaped}'"


def _safe_query(query_str: str) -> list[dict]:
    try:
        results = list(prolog.query(query_str))
        return results
    except Exception as e:
        logger.error(f"Prolog query failed: {query_str} - {e}")
        return []


def _first_result(query_str: str) -> dict | None:
    results = _safe_query(query_str)
    return results[0] if results else None


def _decode_format_term(value: str) -> str:
    """Render a stringified, unevaluated `format(Template, Args)` term.

    Some Prolog trace predicates build dict fields like
    `rule: format('~w foo', [X])` directly, instead of binding the result
    to an atom first (`format(atom(R), '~w foo', [X]), rule: R`). SWI never
    evaluates the format call in that position, so pyswip hands back the
    compound term's own string form — e.g. "format(~w foo, [bar])" — which
    would otherwise leak into the UI verbatim. Detect that shape and render
    it in Python instead. Returns `value` unchanged if it doesn't match.

    The args list is found by matching brackets from the end rather than a
    greedy regex, since a naive `(.*), (\\[.*\\])` split picks the *last*
    top-level ", [" it can find — which is wrong whenever an arg is itself
    a list (e.g. `format('~w: ~w', [sign, [trait1, trait2]])` would get
    split inside the nested list instead of before the outer one).
    """
    if not isinstance(value, str):
        return value
    if not (value.startswith("format(") and value.endswith(")") and value.endswith("])")):
        return value
    inner = value[len("format("):-1]

    depth = 0
    start = None
    for i in range(len(inner) - 1, -1, -1):
        ch = inner[i]
        if ch == "]":
            depth += 1
        elif ch == "[":
            depth -= 1
            if depth == 0:
                start = i
                break
    if start is None or not inner[:start].endswith(", "):
        return value

    template, args_repr = inner[: start - 2], inner[start:]
    try:
        args = ast.literal_eval(args_repr)
    except (ValueError, SyntaxError):
        return value
    it = iter(args)
    try:
        return re.sub("~w", lambda _: str(next(it)), template)
    except StopIteration:
        return value


def _extract_trace(trace_list: list) -> list[dict]:
    """Extract reasoning trace from Prolog result list."""
    steps = []
    for step in trace_list:
        steps.append({
            "rule": _decode_format_term(str(step.get("rule", ""))),
            "result": _decode_format_term(str(step.get("result", ""))),
            "input": _decode_format_term(str(step.get("input", ""))) if "input" in step else "",
            "explanation": _decode_format_term(str(step.get("explanation", ""))) if "explanation" in step else "",
        })
    return steps


class PrologService:
    # ============================================================
    # Module 1: Zodiac & Chart Profile Functions
    # ============================================================

    @staticmethod
    def get_zodiac_profile(sign: str) -> dict | None:
        """Full zodiac profile via zodiac_profile/2."""
        result = _first_result(f"zodiac_profile({_quote_atom(sign)}, Profile)")
        if result:
            p = result["Profile"]
            return {
                "sign": str(p["sign"]),
                "element": str(p["element"]),
                "modality": str(p["modality"]),
                "ruling_planet": str(p["ruling_planet"]),
                "traits": [str(t) for t in p["traits"]],
                "strengths": [str(s) for s in p["strengths"]],
                "challenges": [str(c) for c in p["challenges"]],
                "date_range": str(p["date_range"]),
            }
        return None

    @staticmethod
    def generate_profile(sign: str) -> dict | None:
        """Extended profile via generate_profile/2."""
        result = _first_result(f"generate_profile({_quote_atom(sign)}, Profile)")
        if result:
            p = result["Profile"]
            base = p.get("base_profile", {})
            return {
                "sign": str(p["sign"]),
                "element": str(base.get("element", "")) if base else "",
                "modality": str(base.get("modality", "")) if base else "",
                "ruling_planet": str(base.get("ruling_planet", "")) if base else "",
                "traits": [str(t) for t in base["traits"]] if base and "traits" in base else [],
                "personality_style": str(p.get("personality_style", "")),
                "approach_to_life": str(p.get("approach_to_life", "")),
                "planetary_influence": str(p.get("planetary_influence", "")),
            }
        return None

    @staticmethod
    def get_full_birth_chart(month: int, day: int, hour: int) -> dict | None:
        """Calculate full birth chart from date and time."""
        result = _first_result(
            f"full_birth_chart({month}, {day}, {hour}, SunSign, Chart)"
        )
        if result:
            c = result["Chart"]
            return {
                "sun_sign": str(c["sun_sign"]),
                "moon_sign": str(c["moon_sign"]),
                "rising_sign": str(c["rising_sign"]),
                "element": str(c["element"]),
                "modality": str(c["modality"]),
                "ruling_planet": str(c["ruling_planet"]),
                "traits": [str(t) for t in c["traits"]],
                "personality_style": str(c["personality_style"]),
                "approach_to_life": str(c["approach_to_life"]),
                "planetary_influence": str(c["planetary_influence"]),
                "moon_element": str(c["moon_element"]),
                "rising_element": str(c["rising_element"]),
                "note": str(c["note"]),
            }
        return None

    @staticmethod
    def get_birth_chart_reasoning(month: int, day: int, hour: int) -> list[dict]:
        result = _first_result(
            f"birth_chart_reasoning_trace({month}, {day}, {hour}, Trace)"
        )
        return _extract_trace(result["Trace"]) if result else []

    @staticmethod
    def get_full_birth_chart_precise(
        sun_sign: str, moon_sign: str, rising_sign: str
    ) -> dict | None:
        """Build the symbolic chart from Sun/Moon/Rising signs already computed
        from real ecliptic positions (see app.services.ephemeris_service)."""
        result = _first_result(
            f"full_birth_chart_precise({_quote_atom(sun_sign)}, {_quote_atom(moon_sign)}, "
            f"{_quote_atom(rising_sign)}, Chart)"
        )
        if result:
            c = result["Chart"]
            return {
                "sun_sign": str(c["sun_sign"]),
                "moon_sign": str(c["moon_sign"]),
                "rising_sign": str(c["rising_sign"]),
                "element": str(c["element"]),
                "modality": str(c["modality"]),
                "ruling_planet": str(c["ruling_planet"]),
                "traits": [str(t) for t in c["traits"]],
                "personality_style": str(c["personality_style"]),
                "approach_to_life": str(c["approach_to_life"]),
                "planetary_influence": str(c["planetary_influence"]),
                "moon_element": str(c["moon_element"]),
                "rising_element": str(c["rising_element"]),
                "note": str(c["note"]),
            }
        return None

    @staticmethod
    def get_birth_chart_reasoning_precise(
        sun_sign: str,
        moon_sign: str,
        rising_sign: str,
        sun_degree: float,
        moon_degree: float,
        rising_degree: float,
    ) -> list[dict]:
        result = _first_result(
            f"birth_chart_reasoning_trace_precise({_quote_atom(sun_sign)}, {_quote_atom(moon_sign)}, "
            f"{_quote_atom(rising_sign)}, {sun_degree}, {moon_degree}, {rising_degree}, Trace)"
        )
        return _extract_trace(result["Trace"]) if result else []

    @staticmethod
    def get_zodiac_info(sign: str) -> dict | None:
        result = _first_result(f"zodiac_info({_quote_atom(sign)}, Info)")
        if result:
            info = result["Info"]
            return {
                "sign": str(info["sign"]),
                "element": str(info["element"]),
                "modality": str(info["modality"]),
                "ruling_planet": str(info["ruling_planet"]),
                "traits": [str(t) for t in info["traits"]],
                "date_range": str(info["date_range"]),
                "symbol": str(info["symbol"]),
            }
        return None

    @staticmethod
    def get_all_zodiac_signs() -> list[dict]:
        signs = []
        results = _safe_query("zodiac(Sign)")
        for r in results:
            info = PrologService.get_zodiac_info(str(r["Sign"]))
            if info:
                signs.append(info)
        return signs

    @staticmethod
    def get_element(sign: str) -> str:
        result = _first_result(f"get_element({_quote_atom(sign)}, Element)")
        return str(result["Element"]) if result else "fire"

    @staticmethod
    def get_modality(sign: str) -> str:
        result = _first_result(f"get_modality({_quote_atom(sign)}, Modality)")
        return str(result["Modality"]) if result else "cardinal"

    @staticmethod
    def get_ruling_planet(sign: str) -> str:
        result = _first_result(f"get_ruling_planet({_quote_atom(sign)}, Planet)")
        return str(result["Planet"]) if result else "sun"

    @staticmethod
    def get_zodiac_traits(sign: str) -> list[str]:
        result = _first_result(f"zodiac_traits_of({_quote_atom(sign)}, Traits)")
        if result:
            return [str(t) for t in result["Traits"]]
        return []

    @staticmethod
    def get_zodiac_strengths(sign: str) -> list[str]:
        result = _first_result(f"zodiac_strengths({_quote_atom(sign)}, Strengths)")
        if result:
            return [str(s) for s in result["Strengths"]]
        return []

    @staticmethod
    def get_zodiac_challenges(sign: str) -> list[str]:
        result = _first_result(f"zodiac_challenges({_quote_atom(sign)}, Challenges)")
        if result:
            return [str(c) for c in result["Challenges"]]
        return []

    @staticmethod
    def zodiac_from_date(month: int, day: int) -> str | None:
        result = _first_result(f"zodiac_from_date({month}, {day}, Sign)")
        return str(result["Sign"]) if result else None

    @staticmethod
    def get_chart_profile(sign: str, birth_time: str = "unknown", birth_location: str = "unknown") -> dict | None:
        result = _first_result(
            f"chart_profile({_quote_atom(sign)}, {_quote_atom(birth_time)}, "
            f"{_quote_atom(birth_location)}, Chart)"
        )
        if result:
            c = result["Chart"]
            return {
                "sun_sign": str(c["sun_sign"]),
                "element": str(c["element"]),
                "modality": str(c["modality"]),
                "ruling_planet": str(c["ruling_planet"]),
                "traits": [str(t) for t in c["traits"]],
                "moon_sign": str(c["moon_sign"]),
                "rising_sign": str(c["rising_sign"]),
                "available_data": [str(d) for d in c["available_data"]],
                "note": str(c["note"]),
            }
        return None

    @staticmethod
    def get_element_compatibility(e1: str, e2: str) -> str:
        result = _first_result(f"element_compatibility({_quote_atom(e1)}, {_quote_atom(e2)}, Level)")
        return str(result["Level"]) if result else "moderate"

    @staticmethod
    def get_modality_compatibility(m1: str, m2: str) -> str:
        result = _first_result(f"modality_compatibility({_quote_atom(m1)}, {_quote_atom(m2)}, Level)")
        return str(result["Level"]) if result else "moderate"

    @staticmethod
    def get_profile_reasoning_trace(sign: str) -> list[dict]:
        result = _first_result(f"profile_reasoning_trace({_quote_atom(sign)}, Trace)")
        return _extract_trace(result["Trace"]) if result else []

    @staticmethod
    def get_date_reasoning_trace(month: int, day: int) -> list[dict]:
        result = _first_result(f"date_reasoning_trace({month}, {day}, Trace)")
        return _extract_trace(result["Trace"]) if result else []

    # ============================================================
    # Module 2: Card Selection & Spread Filtering
    # ============================================================

    @staticmethod
    def classify_question(question: str) -> str:
        safe_q = _quote_atom(question)
        result = _first_result(f"question_category({safe_q}, Category)")
        if result:
            return str(result["Category"])
        return "general"

    @staticmethod
    def classify_topic(question: str) -> str:
        """Classify a question into a tarot topic."""
        safe_q = _quote_atom(question)
        result = _first_result(f"classify_topic({safe_q}, Topic)")
        if result:
            return str(result["Topic"])
        return "general"

    @staticmethod
    def get_topic_info(topic: str) -> dict | None:
        """Get topic description and related info."""
        topic_q = _quote_atom(topic)
        desc_result = _first_result(f"topic_description({topic_q}, Desc)")
        spread_result = _first_result(f"topic_spread({topic_q}, Spread)")
        element_result = _first_result(f"topic_element({topic_q}, Element)")
        if desc_result:
            return {
                "topic": topic,
                "description": str(desc_result["Desc"]),
                "spread": str(spread_result["Spread"]) if spread_result else "three_card",
                "element": str(element_result["Element"]) if element_result else "air",
            }
        return None

    @staticmethod
    def get_all_topics() -> list[dict]:
        """Get all available tarot topics."""
        results = _safe_query("tarot_topic(Topic)")
        topics = []
        for r in results:
            info = PrologService.get_topic_info(str(r["Topic"]))
            if info:
                topics.append(info)
        return topics

    @staticmethod
    def select_eligible_cards(sign: str, category: str) -> dict | None:
        """Use Prolog to select eligible cards for a context."""
        result = _first_result(
            f"select_cards({_quote_atom(sign)}, {_quote_atom(category)}, Selection)"
        )
        if result:
            s = result["Selection"]
            return {
                "spread": str(s["spread"]),
                "positions": [str(p) for p in s["positions"]],
                "eligible_cards": [str(c) for c in s["eligible_cards"]],
                "category": str(s["category"]),
                "sign": str(s["sign"]),
                "element": str(s["element"]),
            }
        return None

    @staticmethod
    def filter_spreads(sign: str, category: str) -> list[dict]:
        """Filter spreads based on context using Prolog."""
        element = PrologService.get_element(sign)
        results = _safe_query(
            f"filter_spreads_detailed(context({_quote_atom(category)}, {_quote_atom(sign)}, "
            f"{_quote_atom(element)}), Spreads)"
        )
        if results:
            return [
                {
                    "id": str(s["id"]),
                    "positions": [str(p) for p in s["positions"]],
                    "card_count": int(s["card_count"]),
                    "description": str(s["description"]),
                }
                for s in results[0]["Spreads"]
            ]
        return []

    @staticmethod
    def recommend_spread(question: str, sign: str) -> dict | None:
        safe_q = _quote_atom(question)
        result = _first_result(
            f"spread_recommendation({safe_q}, {_quote_atom(sign)}, Rec)"
        )
        if result:
            rec = result["Rec"]
            return {
                "category": str(rec["category"]),
                "spread_type": str(rec["spread_type"]),
                "name": str(rec["name"]),
                "description": str(rec["description"]),
                "card_count": int(rec["card_count"]),
                "positions": [str(p) for p in rec["positions"]],
                "element": str(rec["element"]),
                "modality": str(rec["modality"]),
                "emphasis": str(rec["emphasis"]),
            }
        return None

    @staticmethod
    def get_available_spreads() -> list[dict]:
        results = _safe_query("available_spread(Spread)")
        spreads = []
        for r in results:
            s = str(r["Spread"])
            s_q = _quote_atom(s)
            pos_result = _first_result(f"spread_positions({s_q}, Positions)")
            desc_result = _first_result(f"spread_description({s_q}, Desc)")
            count_result = _first_result(f"spread_card_count({s_q}, Count)")
            spreads.append({
                "id": s,
                "positions": [str(p) for p in pos_result["Positions"]] if pos_result else [],
                "description": str(desc_result["Desc"]) if desc_result else "",
                "card_count": int(count_result["Count"]) if count_result else 0,
            })
        return spreads

    @staticmethod
    def get_card_orientation_meaning(card: str, orientation: str) -> list[str]:
        result = _first_result(f"card_meaning({_quote_atom(card)}, {_quote_atom(orientation)}, Meaning)")
        if result:
            return [str(m) for m in result["Meaning"]]
        return []

    @staticmethod
    def get_card_themes(card: str) -> list[str]:
        results = _safe_query(f"card_theme({_quote_atom(card)}, Theme)")
        return [str(r["Theme"]) for r in results]

    @staticmethod
    def get_select_cards_reasoning(sign: str, category: str) -> list[dict]:
        result = _first_result(
            f"select_cards_reasoning({_quote_atom(sign)}, {_quote_atom(category)}, Trace)"
        )
        return _extract_trace(result["Trace"]) if result else []

    # ============================================================
    # Module 3: Reading Analysis & Interpretation
    # ============================================================

    @staticmethod
    def analyze_card(card: str, orientation: str) -> dict | None:
        result = _first_result(
            f"analyze_card({_quote_atom(card)}, {_quote_atom(orientation)}, Analysis)"
        )
        if result:
            a = result["Analysis"]
            return {
                "card": str(a["card"]),
                "name": str(a["name"]),
                "arcana": str(a["arcana"]),
                "orientation": str(a["orientation"]),
                "keywords": [str(k) for k in a["keywords"]],
                "themes": [str(t) for t in a["themes"]],
                "meaning": [str(m) for m in a["meaning"]],
                "positive_aspects": [str(p) for p in a["positive_aspects"]],
                "challenging_aspects": [str(c) for c in a["challenging_aspects"]],
            }
        return None

    @staticmethod
    def interpret_card_position(card: str, position: str, orientation: str) -> dict | None:
        result = _first_result(
            f"interpret_card_position({_quote_atom(card)}, {_quote_atom(position)}, "
            f"{_quote_atom(orientation)}, Interp)"
        )
        if result:
            i = result["Interp"]
            return {
                "card": str(i["card"]),
                "name": str(i["name"]),
                "position": str(i["position"]),
                "orientation": str(i["orientation"]),
                "keywords": [str(k) for k in i["keywords"]],
                "themes": [str(t) for t in i["themes"]],
                "position_context": str(i["position_context"]),
                "emphasis": str(i["emphasis"]),
            }
        return None

    @staticmethod
    def analyze_reading(cards: list[str], positions: list[str], orientations: list[str]) -> dict | None:
        cards_str = _quote_atom_list(cards)
        positions_str = _quote_atom_list(positions)
        orientations_str = _quote_atom_list(orientations)
        result = _first_result(
            f"analyze_reading_oriented({cards_str}, {positions_str}, {orientations_str}, Analysis)"
        )
        if result:
            a = result["Analysis"]
            return {
                "card_count": int(a["card_count"]),
                "themes": [str(t) for t in a["themes"]],
                "dominant_theme": str(a["dominant_theme"]),
                "conflicts": [str(c) for c in a["conflicts"]],
                "direction": str(a["direction"]),
                "dominant_element": str(a["dominant_element"]),
            }
        return None

    @staticmethod
    def get_reading_themes(cards: list[str]) -> list[str]:
        cards_str = _quote_atom_list(cards)
        result = _first_result(f"reading_themes({cards_str}, Themes)")
        if result:
            return [str(t) for t in result["Themes"]]
        return []

    @staticmethod
    def get_dominant_theme(cards: list[str]) -> str:
        cards_str = _quote_atom_list(cards)
        result = _first_result(f"dominant_theme({cards_str}, Theme)")
        return str(result["Theme"]) if result else "balance"

    @staticmethod
    def get_reading_conflicts(cards: list[str]) -> list[str]:
        cards_str = _quote_atom_list(cards)
        result = _first_result(f"reading_conflicts({cards_str}, Conflicts)")
        if result:
            return [str(c) for c in result["Conflicts"]]
        return []

    @staticmethod
    def get_reading_summary(cards: list[str]) -> dict | None:
        cards_str = _quote_atom_list(cards)
        result = _first_result(f"reading_summary({cards_str}, Summary)")
        if result:
            s = result["Summary"]
            return {
                "themes": [str(t) for t in s["themes"]],
                "dominant_theme": str(s["dominant_theme"]),
                "conflict_count": int(s["conflict_count"]),
                "conflict_note": str(s["conflict_note"]),
                "card_count": int(s["card_count"]),
            }
        return None

    @staticmethod
    def get_reading_advice(category: str, sign: str) -> str:
        result = _first_result(
            f"reading_advice(context({_quote_atom(category)}, _, {_quote_atom(sign)}), Advice)"
        )
        return str(result["Advice"]) if result else "Trust your intuition and stay present."

    @staticmethod
    def get_theme_based_advice(theme: str) -> str:
        result = _first_result(f"theme_based_advice({_quote_atom(theme)}, Advice)")
        return str(result["Advice"]) if result else ""

    @staticmethod
    def get_zodiac_tarot_theme(sign: str, card: str) -> dict | None:
        result = _first_result(
            f"zodiac_tarot_theme({_quote_atom(sign)}, {_quote_atom(card)}, Theme)"
        )
        if result:
            t = result["Theme"]
            return {
                "zodiac": str(t["zodiac"]),
                "element": str(t["element"]),
                "element_theme": str(t["element_theme"]),
                "card": str(t["card"]),
                "card_theme": str(t["card_theme"]),
                "combined": str(t["combined"]),
            }
        return None

    @staticmethod
    def get_profile_reading_theme(sign: str, cards: list[str]) -> dict | None:
        """Overlap between a sign's traits and the themes present in a reading."""
        cards_str = _quote_atom_list(cards)
        result = _first_result(
            f"profile_reading_theme_dict({_quote_atom(sign)}, {cards_str}, Analysis)"
        )
        if result:
            a = result["Analysis"]
            return {
                "sign": str(a["sign"]),
                "traits": [str(t) for t in a["traits"]],
                "card_themes": [str(t) for t in a["card_themes"]],
                "overlaps": [
                    {"theme": str(o["theme"]), "trait": str(o["trait"])} for o in a["overlaps"]
                ],
                "description": str(a["description"]),
            }
        return None

    @staticmethod
    def get_reading_card_conflicts(cards: list[str]) -> list[dict]:
        """Card-level theme tensions within a reading (which two cards, which
        two themes, and why), unlike get_reading_conflicts which only names
        the conflicting themes without saying which cards produced them."""
        cards_str = _quote_atom_list(cards)
        result = _first_result(f"reading_card_conflicts({cards_str}, Conflicts)")
        if not result:
            return []
        return [
            {
                "card1_index": int(c["card1_index"]),
                "card1": str(c["card1"]),
                "theme1": str(c["theme1"]),
                "card2_index": int(c["card2_index"]),
                "card2": str(c["card2"]),
                "theme2": str(c["theme2"]),
                "title": str(c["title"]),
                "description": str(c["description"]),
            }
            for c in result["Conflicts"]
        ]

    @staticmethod
    def get_synastry_trait_pairs(sign1: str, sign2: str) -> list[dict]:
        """Complementary trait pairs between two signs (e.g. initiative <-> patience)."""
        result = _first_result(
            f"synastry_trait_pairs({_quote_atom(sign1)}, {_quote_atom(sign2)}, Pairs)"
        )
        if not result:
            return []
        return [
            {"trait1": str(p["trait1"]), "trait2": str(p["trait2"])} for p in result["Pairs"]
        ]

    @staticmethod
    def get_card_priority_breakdown(card: str, category: str, sign: str, element: str) -> dict:
        """Priority score (0-6) for one card in a context, plus which of the
        three scoring criteria it matched — the "why" behind the score."""
        context = (
            f"context({_quote_atom(category)}, {_quote_atom(sign)}, {_quote_atom(element)}, _)"
        )
        priority_result = _first_result(f"card_priority({_quote_atom(card)}, {context}, Priority)")
        priority = int(priority_result["Priority"]) if priority_result else 0
        zodiac_match = _first_result(f"zodiac_card({_quote_atom(sign)}, {_quote_atom(card)})") is not None
        category_match = _first_result(
            f"card_matches_question({_quote_atom(card)}, {_quote_atom(category)})"
        ) is not None
        element_match = _first_result(
            f"card_matches_element({_quote_atom(card)}, {_quote_atom(element)})"
        ) is not None
        return {
            "card": card,
            "priority": priority,
            "zodiac_affinity_match": zodiac_match,
            "category_match": category_match,
            "element_match": element_match,
        }

    @staticmethod
    def get_ranked_eligible_cards(category: str, sign: str) -> list[dict]:
        """All Prolog-eligible cards for this context, scored and ranked by
        card_priority/3 (zodiac affinity +3, category match +2, element
        match +1). Highest priority first; ties keep Prolog's own ordering."""
        element = PrologService.get_element(sign)
        selection = PrologService.select_eligible_cards(sign, category)
        eligible = selection["eligible_cards"] if selection else []
        scored = [
            PrologService.get_card_priority_breakdown(card, category, sign, element)
            for card in eligible
        ]
        scored.sort(key=lambda s: s["priority"], reverse=True)
        for i, s in enumerate(scored, start=1):
            s["rank"] = i
        return scored

    @staticmethod
    def get_reading_analysis_trace(cards: list[str], positions: list[str]) -> list[dict]:
        cards_str = _quote_atom_list(cards)
        positions_str = _quote_atom_list(positions)
        result = _first_result(
            f"reading_analysis_trace({cards_str}, {positions_str}, Trace)"
        )
        return _extract_trace(result["Trace"]) if result else []

    @staticmethod
    def interpret_cards(cards: list[str], sign: str, category: str) -> dict | None:
        """Legacy wrapper for card interpretation."""
        cards_str = _quote_atom_list(cards)
        result = _first_result(
            f"analyze_reading({cards_str}, {_quote_atom(sign)}, {_quote_atom(category)}, Analysis)"
        )
        if result:
            a = result["Analysis"]
            return {
                "cards": [str(c) for c in a["cards"]] if "cards" in a else cards,
                "themes": [str(t) for t in a["themes"]],
                "major_arcana_count": int(a.get("major_arcana_count", 0)),
                "total_cards": int(a.get("total_cards", len(cards))),
            }
        return None

    # ============================================================
    # Module 4: Compatibility & Synastry
    # ============================================================

    @staticmethod
    def analyze_compatibility(sign1: str, sign2: str) -> dict | None:
        result = _first_result(
            f"zodiac_compatibility({_quote_atom(sign1)}, {_quote_atom(sign2)}, Result)"
        )
        if result:
            r = result["Result"]
            return {
                "sign1": str(r["sign1"]),
                "sign2": str(r["sign2"]),
                "level": str(r["level"]),
                "score": float(r["score"]),
                "element_score": float(r["element_score"]),
                "modality_score": float(r["modality_score"]),
                "trait_score": float(r["trait_score"]),
                "planetary_score": float(r["planetary_score"]),
            }
        return None

    @staticmethod
    def analyze_synastry(sign1: str, sign2: str) -> dict | None:
        result = _first_result(
            f"synastry({_quote_atom(sign1)}, {_quote_atom(sign2)}, Analysis)"
        )
        if result:
            a = result["Analysis"]
            return {
                "sign1": str(a["sign1"]),
                "sign2": str(a["sign2"]),
                "element1": str(a["element1"]),
                "element2": str(a["element2"]),
                "modality1": str(a["modality1"]),
                "modality2": str(a["modality2"]),
                "planet1": str(a["planet1"]),
                "planet2": str(a["planet2"]),
                "element_level": str(a["element_level"]),
                "element_description": str(a["element_description"]),
                "modality_level": str(a["modality_level"]),
                "overall_level": str(a["overall_level"]),
                "overall_score": float(a["overall_score"]),
                "strengths": [str(s) for s in a["strengths"]],
                "challenges": [str(c) for c in a["challenges"]],
                "communication_theme": str(a["communication_theme"]),
                "balance_theme": str(a["balance_theme"]),
            }
        return None

    @staticmethod
    def get_compatibility_explanation(sign1: str, sign2: str) -> dict | None:
        result = _first_result(
            f"compatibility_explanation({_quote_atom(sign1)}, {_quote_atom(sign2)}, Explanation)"
        )
        if result:
            e = result["Explanation"]
            return {
                "element_analysis": {
                    "input": str(e["element_analysis"]["input"]),
                    "result": str(e["element_analysis"]["result"]),
                    "description": str(e["element_analysis"]["description"]),
                },
                "modality_analysis": {
                    "input": str(e["modality_analysis"]["input"]),
                    "result": str(e["modality_analysis"]["result"]),
                    "description": str(e["modality_analysis"]["description"]),
                },
                "trait_analysis": {
                    "input": str(e["trait_analysis"]["input"]),
                    "result": str(e["trait_analysis"]["result"]),
                    "description": str(e["trait_analysis"]["description"]),
                },
                "planetary_analysis": {
                    "input": str(e["planetary_analysis"]["input"]),
                    "result": str(e["planetary_analysis"]["result"]),
                    "description": str(e["planetary_analysis"]["description"]),
                },
                "overall": {
                    "input": str(e["overall"]["input"]),
                    "result": str(e["overall"]["result"]),
                    "description": str(e["overall"]["description"]),
                },
            }
        return None

    @staticmethod
    def get_compatibility_score_breakdown(sign1: str, sign2: str) -> dict | None:
        result = _first_result(
            f"compatibility_score_breakdown({_quote_atom(sign1)}, {_quote_atom(sign2)}, Breakdown)"
        )
        if result:
            b = result["Breakdown"]
            return {
                "element": {"name": str(b["element"]["name"]), "score": float(b["element"]["score"]), "weight": float(b["element"]["weight"]), "description": _decode_format_term(str(b["element"]["description"]))},
                "modality": {"name": str(b["modality"]["name"]), "score": float(b["modality"]["score"]), "weight": float(b["modality"]["weight"]), "description": _decode_format_term(str(b["modality"]["description"]))},
                "traits": {"name": str(b["traits"]["name"]), "score": float(b["traits"]["score"]), "weight": float(b["traits"]["weight"]), "description": _decode_format_term(str(b["traits"]["description"]))},
                "planetary": {"name": str(b["planetary"]["name"]), "score": float(b["planetary"]["score"]), "weight": float(b["planetary"]["weight"]), "description": _decode_format_term(str(b["planetary"]["description"]))},
                "overall": float(b["overall"]),
            }
        return None

    @staticmethod
    def get_synastry_reasoning_trace(sign1: str, sign2: str) -> list[dict]:
        result = _first_result(
            f"synastry_reasoning_trace({_quote_atom(sign1)}, {_quote_atom(sign2)}, Trace)"
        )
        return _extract_trace(result["Trace"]) if result else []

    @staticmethod
    def get_compatibility_level(sign1: str, sign2: str) -> str:
        result = _first_result(
            f"zodiac_compatibility({_quote_atom(sign1)}, {_quote_atom(sign2)}, Result)"
        )
        return str(result["Result"]["level"]) if result else "moderate"

    # ============================================================
    # Shared: Horoscope & Reasoning
    # ============================================================

    @staticmethod
    def get_horoscope_guidance(sign: str, mood: str) -> dict | None:
        result = _first_result(
            f"horoscope_guidance({_quote_atom(sign)}, {_quote_atom(mood)}, Guidance)"
        )
        if result:
            g = result["Guidance"]
            return {
                "sign": str(g["sign"]),
                "element": str(g["element"]),
                "modality": str(g["modality"]),
                "theme": str(g["theme"]),
                "mood": str(g["mood"]),
                "mood_theme": str(g["mood_theme"]),
                "focus": str(g["focus"]),
            }
        return None

    @staticmethod
    def get_relevant_facts(sign: str, category: str) -> dict | None:
        result = _first_result(
            f"get_relevant_facts({_quote_atom(sign)}, {_quote_atom(category)}, Facts)"
        )
        if result:
            f = result["Facts"]
            return {
                "zodiac": str(f["zodiac"]),
                "element": str(f["element"]),
                "modality": str(f["modality"]),
                "ruling_planet": str(f["ruling_planet"]),
                "traits": [str(t) for t in f["traits"]],
                "category": str(f["category"]),
                "spread_type": str(f["spread_type"]),
                "card_count": int(f["card_count"]),
            }
        return None

    @staticmethod
    def get_zodiac_card_affinity(sign: str) -> list[str]:
        results = _safe_query(f"zodiac_card({_quote_atom(sign)}, Card)")
        return [str(r["Card"]) for r in results]

    @staticmethod
    def get_element_card_affinity(element: str) -> list[str]:
        results = _safe_query(f"element_card_affinity({_quote_atom(element)}, Card)")
        return [str(r["Card"]) for r in results]

    @staticmethod
    def generate_reading_trace(question: str, sign: str) -> list[dict]:
        safe_q = _quote_atom(question)
        result = _first_result(
            f"generate_full_trace({safe_q}, {_quote_atom(sign)}, Trace)"
        )
        return _extract_trace(result["Trace"]) if result else []

    @staticmethod
    def generate_compatibility_trace(sign1: str, sign2: str) -> list[dict]:
        result = _first_result(
            f"generate_compatibility_trace({_quote_atom(sign1)}, {_quote_atom(sign2)}, Trace)"
        )
        return _extract_trace(result["Trace"]) if result else []

    @staticmethod
    def generate_horoscope_trace(sign: str, mood: str) -> list[dict]:
        result = _first_result(
            f"generate_horoscope_trace({_quote_atom(sign)}, {_quote_atom(mood)}, Trace)"
        )
        return _extract_trace(result["Trace"]) if result else []
