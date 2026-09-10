import asyncio

from app.services.prolog_service import PrologService


class HoroscopeService:
    @staticmethod
    async def generate_horoscope(zodiac_sign: str, mood: str, locale: str = "en") -> dict | None:
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
            locale=locale,
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
            if locale == "my":
                burmese_signs = {
                    "aries": "မိဿရာသီ", "taurus": "ပြိဿရာသီ", "gemini": "မေထုန်ရာသီ", "cancer": "ကရကဋ်ရာသီ",
                    "leo": "သိဟ်ရာသီ", "virgo": "ကန်ရာသီ", "libra": "တူရာသီ", "scorpio": "ဗြိစ္ဆာရာသီ",
                    "sagittarius": "ဓနုရာသီ", "capricorn": "မကာရရာသီ", "aquarius": "ကုမ်ရာသီ", "pisces": "မိန်ရာသီ"
                }
                sign_my = burmese_signs.get(zodiac_sign.lower(), zodiac_sign)
                return {
                    "zodiac_sign": zodiac_sign,
                    "element": guidance["element"],
                    "theme": guidance["theme"],
                    "mood": mood,
                    "guidance": f"ယနေ့သည် {sign_my} ဖွားများအတွက် အဓိကဆောင်ပုဒ်ဖြစ်သော စွမ်းအင်များကို အထူးအလေးထားရမည့် နေ့တစ်နေ့ဖြစ်ပါသည်။ သင်၏ စိတ်ခံစားချက်နှင့် သဘာဝစွမ်းအင်များကို သဟဇာတဖြစ်အောင် ညှိယူပြီး တစ်နေ့တာ လုပ်ငန်းဆောင်တာများကို အေးချမ်းတည်ငြိမ်စွာ ဖြတ်သန်းပါ။",
                    "reflection": "ယနေ့တွင် ကြုံတွေ့ရသော အခြေအနေများအပေါ် မိမိ၏ နေ့စဉ်ဘဝတွင် မည်သို့ လက်တွေ့ကျင့်သုံး နားလည်နိုင်မည်ကို ပြန်လည်ဆင်ခြင်သုံးသပ်ကြည့်ပါ။",
                    "opportunity": "စိတ်ခံစားချက်နှင့် ထပ်တူကျသော အခွင့်အလမ်းကောင်းများသည် ယနေ့တွင် သင့်ထံသို့ ရောက်ရှိလာနိုင်ပါသည်။ အာရုံစူးစိုက်မှုကို မြှင့်တင်ထားပါ။",
                    "caution": "အလွန်အမင်း စိတ်လောကြီးခြင်း သို့မဟုတ် စိတ်ဖိစီးမှုများ မဖြစ်စေရန် သတိပြုထိန်းကျောင်းပါ။",
                }
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
