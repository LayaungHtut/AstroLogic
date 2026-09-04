from app.services.prolog_service import PrologService

MOOD_KEYWORDS = {
    "happy": ["happy", "joy", "great", "wonderful", "amazing", "good"],
    "excited": ["excited", "thrilled", "eager", "looking forward", "can't wait"],
    "stressed": ["stressed", "overwhelmed", "pressure", "too much", "anxious"],
    "uncertain": ["unsure", "confused", "lost", "don't know", "uncertain"],
    "calm": ["calm", "peaceful", "relaxed", "serene", "content"],
    "frustrated": ["frustrated", "annoyed", "stuck", "angry", "irritated"],
    "curious": ["curious", "wondering", "interested", "want to know", "exploring"],
    "reflective": ["thinking", "reflecting", "contemplating", "pondering", "meditating"],
}


class HoroscopeService:
    @staticmethod
    async def generate_horoscope(zodiac_sign: str, mood: str) -> dict | None:
        guidance = PrologService.get_horoscope_guidance(zodiac_sign, mood)
        if not guidance:
            return None

        from app.services.openrouter_service import generate_horoscope as ai_generate

        ai_result = await ai_generate(
            zodiac_sign=zodiac_sign,
            element=guidance["element"],
            modality=guidance["modality"],
            theme=guidance["theme"],
            mood=guidance["mood"],
            mood_theme=guidance["mood_theme"],
            focus=guidance["focus"],
        )

        if ai_result:
            return {
                "zodiac_sign": zodiac_sign,
                "element": guidance["element"],
                "theme": guidance["theme"],
                "mood": mood,
                "guidance": ai_result.get("guidance", ""),
                "reflection": ai_result.get("reflection", ""),
                "opportunity": ai_result.get("opportunity", ""),
                "caution": ai_result.get("caution", ""),
            }
        else:
            return {
                "zodiac_sign": zodiac_sign,
                "element": guidance["element"],
                "theme": guidance["theme"],
                "mood": mood,
                "guidance": f"Today emphasizes {guidance['theme']} for {zodiac_sign}. Focus on your {guidance['focus']}.",
                "reflection": f"How can you embrace {guidance['theme']} in your daily life today?",
                "opportunity": f"A day aligned with {guidance['mood_theme']} energy. Look for moments of {guidance['theme']}.",
                "caution": f"Be mindful of overthinking. Sometimes the best approach is to trust your {guidance['element']} nature.",
            }

    @staticmethod
    def classify_mood(text: str) -> str:
        """Classify free-text mood into one of the fixed moods known to horoscope_rules.pl.

        This is a plain keyword match, not an LLM call — the Prolog rules only
        recognize this fixed vocabulary, so there's nothing for a model to add.
        """
        text_lower = text.lower()
        scores = {
            mood: sum(1 for kw in keywords if kw in text_lower)
            for mood, keywords in MOOD_KEYWORDS.items()
        }
        scores = {mood: score for mood, score in scores.items() if score > 0}
        if scores:
            return max(scores, key=scores.get)
        return "neutral"
