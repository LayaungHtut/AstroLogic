import asyncio

from app.services.prolog_service import PrologService


class HoroscopeService:
    @staticmethod
    async def generate_horoscope(zodiac_sign: str, mood: str) -> dict | None:
        # PrologService calls are synchronous, blocking pyswip queries — run
        # off the event loop so one slow query doesn't stall other requests.
        guidance = await asyncio.to_thread(
            PrologService.get_horoscope_guidance, zodiac_sign, mood
        )
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
    async def classify_mood(text: str) -> str:
        """Classify free-text mood into one of the fixed moods known to horoscope_rules.pl.

        Delegates to classify_mood/2 in Prolog (mood_keyword/2 facts + a
        scoring rule) — this is a plain keyword match, not an LLM call, and
        the mood vocabulary now lives in one place instead of being
        duplicated as a Python dict.
        """
        return await asyncio.to_thread(PrologService.classify_mood, text)
