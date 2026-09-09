"""Comprehensive bilingual Birth Chart Explanation Service (English and Myanmar).

Analyzes calculated birth chart data (Sun, Moon, Rising, planets, houses, and degrees)
to generate rich, structured psychological and evolutionary astrological explanations.
Computes major aspects (Conjunctions, Trines, Squares, Oppositions, Sextiles) and provides
in-depth interpretations in both English and authentic Burmese.
"""

import math
from typing import Any

ZODIAC_META = {
    "aries": {"en": "Aries", "my": "မိဿ (Aries)", "symbol": "♈", "element": "fire", "modality": "cardinal"},
    "taurus": {"en": "Taurus", "my": "ပြိဿ (Taurus)", "symbol": "♉", "element": "earth", "modality": "fixed"},
    "gemini": {"en": "Gemini", "my": "မေထုန် (Gemini)", "symbol": "♊", "element": "air", "modality": "mutable"},
    "cancer": {"en": "Cancer", "my": "ကရကဋ် (Cancer)", "symbol": "♋", "element": "water", "modality": "cardinal"},
    "leo": {"en": "Leo", "my": "သိဟ် (Leo)", "symbol": "♌", "element": "fire", "modality": "fixed"},
    "virgo": {"en": "Virgo", "my": "ကန် (Virgo)", "symbol": "♍", "element": "earth", "modality": "mutable"},
    "libra": {"en": "Libra", "my": "တူ (Libra)", "symbol": "♎", "element": "air", "modality": "cardinal"},
    "scorpio": {"en": "Scorpio", "my": "ဗြိစ္ဆာ (Scorpio)", "symbol": "♏", "element": "water", "modality": "fixed"},
    "sagittarius": {"en": "Sagittarius", "my": "ဓနု (Sagittarius)", "symbol": "♐", "element": "fire", "modality": "mutable"},
    "capricorn": {"en": "Capricorn", "my": "မကာရ (Capricorn)", "symbol": "♑", "element": "earth", "modality": "cardinal"},
    "aquarius": {"en": "Aquarius", "my": "ကုမ် (Aquarius)", "symbol": "♒", "element": "air", "modality": "fixed"},
    "pisces": {"en": "Pisces", "my": "မိန် (Pisces)", "symbol": "♓", "element": "water", "modality": "mutable"},
}

PLANET_NAMES = {
    "sun": {"en": "Sun", "my": "နေမင်း (Sun)", "symbol": "☉", "domain_en": "Core Identity & Vital Purpose", "domain_my": "ပင်ကိုစရိုက်နှင့် ဘဝရည်မှန်းချက်"},
    "moon": {"en": "Moon", "my": "လမင်း (Moon)", "symbol": "☽", "domain_en": "Emotions, Needs & Subconscious", "domain_my": "စိတ်ခံစားမှု၊ အတွင်းစိတ်နှင့် လိုအပ်ချက်များ"},
    "rising": {"en": "Rising / Ascendant", "my": "စန်းလဂ် (Ascendant)", "symbol": "AC", "domain_en": "Outer Persona & First Impression", "domain_my": "အပြင်ပန်းပုံရိပ်နှင့် ပထမဆုံးတွေ့ဆုံမှုဟန်"},
    "mercury": {"en": "Mercury", "my": "ဗုဒ္ဓဟူး (Mercury)", "symbol": "☿", "domain_en": "Mind, Intellect & Communication", "domain_my": "ဉာဏ်ပညာ၊ တွေးခေါ်မှုနှင့် ဆက်ဆံရေး"},
    "venus": {"en": "Venus", "my": "သောကြာ (Venus)", "symbol": "♀", "domain_en": "Love, Harmony & Values", "domain_my": "အချစ်ရေး၊ တန်ဖိုးထားမှုနှင့် အလှတရား"},
    "mars": {"en": "Mars", "my": "အင်္ဂါ (Mars)", "symbol": "♂", "domain_en": "Drive, Willpower & Passion", "domain_my": "စွမ်းအင်၊ ရည်မှန်းချက်နှင့် လှုပ်ရှားစွမ်းအား"},
    "jupiter": {"en": "Jupiter", "my": "ကြာသပတေး (Jupiter)", "symbol": "♃", "domain_en": "Luck, Expansion & Wisdom", "domain_my": "ကံကြမ္မာ၊ အခွင့်အလမ်းနှင့် ကြီးထွားချဲ့ထွင်မှု"},
    "saturn": {"en": "Saturn", "my": "စနေ (Saturn)", "symbol": "♄", "domain_en": "Discipline, Mastery & Karma", "domain_my": "စည်းကမ်း၊ ကံကြမ္မာသင်ခန်းစာနှင့် ရင့်ကျက်မှု"},
    "uranus": {"en": "Uranus", "my": "ယူရေးနပ်စ် (Uranus)", "symbol": "♅", "domain_en": "Innovation, Breakthroughs & Freedom", "domain_my": "ဆန်းသစ်တီထွင်မှု၊ လွတ်လပ်ခွင့်နှင့် အပြောင်းအလဲ"},
    "neptune": {"en": "Neptune", "my": "နက်ပကျွန်း (Neptune)", "symbol": "♆", "domain_en": "Dreams, Intuition & Mysticism", "domain_my": "စိတ်ကူးယဉ်အနုပညာ၊ မသိစိတ်နှင့် ဝိညာဉ်ရေးရာ"},
    "pluto": {"en": "Pluto", "my": "ပလူတို (Pluto)", "symbol": "♇", "domain_en": "Rebirth, Power & Transformation", "domain_my": "အသွင်ပြောင်းလဲခြင်း၊ စိတ်စွမ်းအားနှင့် ပြန်လည်ရှင်သန်မှု"},
    "node": {"en": "North Node", "my": "ရာဟု / နဂါးခေါင်း (North Node)", "symbol": "☊", "domain_en": "Soul Destiny & Growth Path", "domain_my": "ဝိညာဉ်ရေးရာ ဆင့်ကဲတိုးတက်မှု ပန်းတိုင်"},
    "lilith": {"en": "Lilith", "my": "လမင်းအမှောင်ခြမ်း (Lilith)", "symbol": "⚸", "domain_en": "Primal Instincts & Untamed Truth", "domain_my": "မသိစိတ်၏ စစ်မှန်သော ရိုင်းစိုင်းအလှ"},
    "chiron": {"en": "Chiron", "my": "ခိုင်ရွန် (Chiron)", "symbol": "⚷", "domain_en": "Wounded Healer & Soul Wisdom", "domain_my": "အတွင်းဒဏ်ရာကို ကုသပေးသော ဝိညာဉ်ဆေးဆရာ"},
}

SUN_PROFILES = {
    "aries": {
        "en": "Your Sun in Aries gives you bold initiative, pioneering vitality, and an instinctive drive to blaze new trails. You thrive when leading with authentic courage and breaking through stagnant boundaries.",
        "my": "မိဿရာသီဖွား နေမင်းပိုင်ရှင်ဖြစ်၍ ရဲရင့်သော ဦးဆောင်မှု၊ ရှေ့ပြေးလမ်းဖောက်လိုစိတ်နှင့် မဆုတ်မနစ်သော စွမ်းအင်အပြည့်ရှိသည်။ အတားအဆီးများကို ရဲဝံ့စွာ ထိုးဖောက်ကျော်လွှားရာတွင် အထူးထူးချွန်သည်။",
        "strengths_en": ["Bold courage", "Pioneering drive", "Decisive leadership", "High physical energy"],
        "strengths_my": ["ရဲရင့်ပြတ်သားမှု", "ရှေ့ဆောင်စတင်နိုင်စွမ်း", "ခေါင်းဆောင်မှုအရည်အသွေး", "တက်ကြွသော စွမ်းအင်"],
        "lesson_en": "Cultivate patient endurance and listen to others before taking swift leaps.",
        "lesson_my": "လျင်မြန်စွာ မဆုံးဖြတ်မီ အခြားသူများ၏ အမြင်ကို နားထောင်၍ စိတ်ရှည်သည်းခံမှုကို လေ့ကျင့်ပါ။",
    },
    "taurus": {
        "en": "Your Sun in Taurus anchors you with steadfast determination, sensory appreciation, and patience. You build lasting value and tangible security through persistent, methodical focus.",
        "my": "ပြိဿရာသီဖွား နေမင်းပိုင်ရှင်ဖြစ်၍ တည်ငြိမ်ခိုင်မာမှု၊ စိတ်ရှည်သည်းခံနိုင်စွမ်းနှင့် လက်တွေ့ကျသော တန်ဖိုးဖန်တီးမှုများတွင် အထူးအားကောင်းသည်။ ခိုင်မာသော အနာဂတ်ကို စနစ်တကျ တည်ဆောက်နိုင်သည်။",
        "strengths_en": ["Rock-solid loyalty", "Financial acumen", "Patience and stamina", "Aesthetic appreciation"],
        "strengths_my": ["သစ္စာခိုင်မြဲမှု", "စီးပွားရေးနှင့် ငွေကြေးစီမံနိုင်စွမ်း", "စိတ်ရှည်ဇွဲကောင်းမှု", "အလှတရားကို တန်ဖိုးထားတတ်မှု"],
        "lesson_en": "Embrace change and avoid holding on to comfort zones when life calls for transformation.",
        "lesson_my": "အပြောင်းအလဲများကို မကြောက်ဘဲ သက်တောင့်သက်သာဇုန်မှ ရုန်းထွက်၍ အသစ်များကို လက်ခံပါ။",
    },
    "gemini": {
        "en": "Your Sun in Gemini brings sharp curiosity, versatile communication, and quick wit. You bridge diverse concepts effortlessly and thrive on intellectual variety and social exchange.",
        "my": "မေထုန်ရာသီဖွား နေမင်းပိုင်ရှင်ဖြစ်၍ ထက်မြက်သော ဉာဏ်ရည်၊ လျင်မြန်သော ဆက်သွယ်ပြောဆိုနိုင်စွမ်းနှင့် စူးစမ်းလိုစိတ် ကြွယ်ဝသည်။ အကြောင်းအရာမျိုးစုံကို အလွယ်တကူ ချိတ်ဆက်နားလည်နိုင်သည်။",
        "strengths_en": ["Mental agility", "Eloquent articulation", "Adaptability", "Multi-disciplinary curiosity"],
        "strengths_my": ["လျင်မြန်သော အတွေးအခေါ်", "စကားပြောကျွမ်းကျင်မှု", "လိုက်လျောညီထွေရှိမှု", "ဗဟုသုတစုံလင်မှု"],
        "lesson_en": "Focus your versatile mind on deep mastery rather than scattering energy across too many pursuits.",
        "lesson_my": "အရာရာကို စိတ်မပြန့်လွင့်စေဘဲ အရေးကြီးသောအရာတစ်ခုတွင် အဆုံးထိ အာရုံစူးစိုက်ပါ။",
    },
    "cancer": {
        "en": "Your Sun in Cancer radiates deep emotional intelligence, nurturing protective instincts, and profound empathy. Your heart is an intuitive sanctuary that creates profound bonds with family and tribe.",
        "my": "ကရကဋ်ရာသီဖွား နေမင်းပိုင်ရှင်ဖြစ်၍ နက်ရှိုင်းသော စိတ်ခံစားမှုဉာဏ်ရည်၊ နွေးထွေးသော စောင့်ရှောက်ကာကွယ်လိုစိတ်နှင့် အလိုလိုသိမြင်နိုင်စွမ်း (Intuition) အလွန်မြင့်မားသည်။ မိသားစုနှင့် ချစ်ခင်ရသူများကို နွေးထွေးစွာ ကာကွယ်သည်။",
        "strengths_en": ["Intuitive perception", "Deep empathy", "Protective loyalty", "Emotional resilience"],
        "strengths_my": ["အလိုလိုသိမြင်နိုင်စွမ်း", "စာနာထောက်ထားမှု", "ကာကွယ်စောင့်ရှောက်လိုစိတ်", "စိတ်ပိုင်းဆိုင်ရာ ကြံ့ခိုင်မှု"],
        "lesson_en": "Establish healthy emotional boundaries so you do not absorb other people's emotional baggage.",
        "lesson_my": "မိမိကိုယ်ကို မပင်ပန်းစေရန် အခြားသူများ၏ စိတ်ဒုက္ခများကို လိုအပ်သလို အကန့်အသတ်ထား၍ ကာကွယ်ပါ။",
    },
    "leo": {
        "en": "Your Sun in Leo bestows radiant confidence, creative leadership, and generous warmth. You inspire others when sharing your authentic creative light and leading with a noble heart.",
        "my": "သိဟ်ရာသီဖွား နေမင်းပိုင်ရှင်ဖြစ်၍ ထင်ပေါ်သော ကိုယ်ရည်ကိုယ်သွေး၊ ဖန်တီးနိုင်စွမ်းနှင့် ရက်ရောနွေးထွေးသော စိတ်နှလုံးရှိသည်။ အခြားသူများကို လှုံ့ဆော်ဦးဆောင်နိုင်သော မွေးရာပါ ခေါင်းဆောင်ဖြစ်သည်။",
        "strengths_en": ["Magnetic charisma", "Artistic flair", "Generous nobility", "Uplifting warmth"],
        "strengths_my": ["ဆွဲဆောင်မှုရှိသော အရှိန်အဝါ", "အနုပညာဖန်တီးနိုင်စွမ်း", "ရက်ရောသော စိတ်ထား", "နွေးထွေးသော ခေါင်းဆောင်မှု"],
        "lesson_en": "Find validation from within your own soul rather than relying solely on applause from the outside world.",
        "lesson_my": "အပြင်ပန်း ချီးမွမ်းသံများထက် မိမိ၏ အတွင်းစိတ် အမှန်တရားနှင့် တန်ဖိုးကို ပိုမိုအလေးထားပါ။",
    },
    "virgo": {
        "en": "Your Sun in Virgo grants discerning analysis, methodical craftsmanship, and a devotion to purposeful refinement. You bring order, health, and clarity to complexity.",
        "my": "ကန်ရာသီဖွား နေမင်းပိုင်ရှင်ဖြစ်၍ အသေးစိတ်စိစစ်နိုင်စွမ်း၊ စနစ်တကျ လုပ်ဆောင်နိုင်မှုနှင့် ပြီးပြည့်စုံအောင် သန့်စင်ပြုပြင်လိုစိတ် အားကောင်းသည်။ အရာရာကို လက်တွေ့ကျကျ စီစဉ်ဖြေရှင်းပေးနိုင်သည်။",
        "strengths_en": ["Analytical precision", "Practical helpfulness", "Quality craftsmanship", "Systemic thinking"],
        "strengths_my": ["တိကျသော စိစစ်နိုင်စွမ်း", "လက်တွေ့ကူညီမှု", "အရည်အသွေးမြင့်မားမှု", "စနစ်တကျ တွေးခေါ်မှု"],
        "lesson_en": "Release harsh self-criticism and understand that beauty often thrives in organic imperfection.",
        "lesson_my": "မိမိကိုယ်ကို အပြစ်တင်လွန်းခြင်းကို လျှော့ချပြီး မပြည့်စုံမှုများကြားမှ အလှတရားကို လက်ခံတတ်ပါစေ။",
    },
    "libra": {
        "en": "Your Sun in Libra seeks harmony, elevated aesthetic elegance, and social equilibrium. You understand balance, justice, and excel at bridging polarized perspectives with diplomatic grace.",
        "my": "တူရာသီဖွား နေမင်းပိုင်ရှင်ဖြစ်၍ မျှတညီညွတ်မှု၊ အလှတရားနှင့် သံတမန်ဆန်သော ဆက်ဆံရေးတွင် ထူးချွန်သည်။ မတူကွဲပြားသော အမြင်များကို ညှိနှိုင်းပေါင်းစည်းပေးနိုင်သော တရားမျှတသူဖြစ်သည်။",
        "strengths_en": ["Diplomatic tact", "Aesthetic taste", "Fair-minded mediation", "Relational charm"],
        "strengths_my": ["သံတမန်ဆန်သော နည်းပရိယာယ်", "အနုပညာအမြင်", "မျှတသော ဖျန်ဖြေနိုင်မှု", "ဆွဲဆောင်မှုရှိသော ဆက်ဆံရေး"],
        "lesson_en": "Trust your own inner truth and make clear decisions without fearing disagreement from others.",
        "lesson_my": "အခြားသူများ မကြိုက်မည်ကို စိုးရိမ်မနေဘဲ မိမိ၏ ဆုံးဖြတ်ချက်ကို ခိုင်မာစွာ ချမှတ်ပါ။",
    },
    "scorpio": {
        "en": "Your Sun in Scorpio drives intense psychological depth, transformative power, and emotional resilience. You uncover hidden truth beneath appearances and possess profound regenerative capabilities.",
        "my": "ဗြိစ္ဆာရာသီဖွား နေမင်းပိုင်ရှင်ဖြစ်၍ နက်နဲသော စိတ်ပိုင်းဆိုင်ရာ စွမ်းအား၊ အသွင်ပြောင်းလဲနိုင်စွမ်းနှင့် မလျှော့သော ဇွဲလုံ့လရှိသည်။ လျှို့ဝှက်ချက်များနှင့် အမှန်တရားကို ထိုးထွင်းသိမြင်နိုင်စွမ်း အလွန်ထက်မြက်သည်။",
        "strengths_en": ["Unshakable resilience", "Psychological penetration", "Unwavering loyalty", "Transformative power"],
        "strengths_my": ["မယိမ်းယိုင်သော ကြံ့ခိုင်မှု", "စိတ်ပိုင်းထိုးထွင်းသိမြင်မှု", "သစ္စာစောင့်သိမှု", "အသွင်ပြောင်းလဲနိုင်သော စွမ်းရည်"],
        "lesson_en": "Practice forgiveness and surrender the need to control life's unpredictable currents.",
        "lesson_my": "ခွင့်လွှတ်ခြင်းကို ကျင့်သုံးပြီး အရာရာကို ထိန်းချုပ်လိုသည့် စိတ်အား ဖြေလျှော့ပေးပါ။",
    },
    "sagittarius": {
        "en": "Your Sun in Sagittarius inspires expansive philosophical optimism, a boundless quest for truth, and love of adventure. You seek big-picture meaning across intellectual and physical horizons.",
        "my": "ဓနုရာသီဖွား နေမင်းပိုင်ရှင်ဖြစ်၍ ကျယ်ပြန့်သော အတွေးအခေါ်၊ အမှန်တရားကို ရှာဖွေလိုစိတ်နှင့် စွန့်စားလိုသော အကောင်းမြင်ဝါဒ အပြည့်ရှိသည်။ ဘဝ၏ နက်နဲသော အဓိပ္ပာယ်ကို စူးစမ်းရှာဖွေသည်။",
        "strengths_en": ["Philosophical vision", "Generous honesty", "Infectious optimism", "Global curiosity"],
        "strengths_my": ["ကျယ်ပြန့်သော မျှော်မှန်းချက်", "ရိုးသားပွင့်လင်းမှု", "အကောင်းမြင်သော စိတ်ဓာတ်", "စူးစမ်းလေ့လာလိုစိတ်"],
        "lesson_en": "Anchor your grand visions with meticulous follow-through on the ground.",
        "lesson_my": "ကြီးမားသော စိတ်ကူးများကို လက်တွေ့ကျသော ခြေလှမ်းများဖြင့် အဆုံးထိ အကောင်အထည်ဖော်ပါ။",
    },
    "capricorn": {
        "en": "Your Sun in Capricorn bestows strategic ambition, grounded perseverance, and disciplined mastery. You ascend life's highest mountains with steady purpose and enduring responsibility.",
        "my": "မကာရရာသီဖွား နေမင်းပိုင်ရှင်ဖြစ်၍ မဟာဗျူဟာမြောက် ရည်မှန်းချက်၊ စည်းကမ်းနှင့် မယိမ်းယိုင်သော ဇွဲရှိသည်။ အချိန်ယူ၍ ခိုင်ခံ့သော အောင်မြင်မှုကို စနစ်တကျ တည်ဆောက်နိုင်သူဖြစ်သည်။",
        "strengths_en": ["Executive leadership", "Patience and tenacity", "Strategic foresight", "Reliable accountability"],
        "strengths_my": ["ခေါင်းဆောင်မှု အရည်အချင်း", "ဇွဲနှင့် စိတ်ရှည်မှု", "အမြော်အမြင်ရှိမှု", "တာဝန်ယူမှု အပြည့်ရှိခြင်း"],
        "lesson_en": "Remember that life is not just work and duty; allow yourself joy, leisure, and spontaneous rest.",
        "lesson_my": "ဘဝသည် အလုပ်တစ်ခုတည်း မဟုတ်ကြောင်း သတိရပြီး ပျော်ရွှင်မှုနှင့် အနားယူခြင်းကိုလည်း အချိန်ပေးပါ။",
    },
    "aquarius": {
        "en": "Your Sun in Aquarius pulses with visionary innovation, egalitarian humanitarianism, and independent intellect. You question dogma and envision a more liberated future for all.",
        "my": "ကုမ်ရာသီဖွား နေမင်းပိုင်ရှင်ဖြစ်၍ ဆန်းသစ်သော တွေးခေါ်မှု၊ လွတ်လပ်မှုကို တန်ဖိုးထားခြင်းနှင့် လူသားဆန်သော အနာဂတ်မျှော်မှန်းချက်များ ပြည့်နှက်နေသည်။ စည်းမျဉ်းဟောင်းများကို ကျော်လွန်တွေးခေါ်နိုင်သည်။",
        "strengths_en": ["Visionary originality", "Humanitarian compassion", "Objective detachment", "Inventive intellect"],
        "strengths_my": ["ဆန်းသစ်တီထွင်နိုင်စွမ်း", "လူသားချင်းစာနာမှု", "ဘက်မလိုက်သော အမြင်", "ထူးချွန်သော ဉာဏ်ရည်"],
        "lesson_en": "Connect with individual, warm human hearts alongside your grand ideas for humanity.",
        "lesson_my": "ကြီးမားသော စိတ်ကူးများအပြင် နီးစပ်ရာ လူတစ်ဦးချင်းစီ၏ နွေးထွေးသော စိတ်ခံစားချက်ကို ဂရုပြုပါ။",
    },
    "pisces": {
        "en": "Your Sun in Pisces immerses in boundless spiritual imagination, compassionate empathy, and mystical artistic sensibility. You sense the unseen interconnected tapestry of existence.",
        "my": "မိန်ရာသီဖွား နေမင်းပိုင်ရှင်ဖြစ်၍ ကျယ်ပြောသော စိတ်ကူးယဉ်အနုပညာဉာဏ်၊ ကြီးမားသော စာနာထောက်ထားမှုနှင့် ဝိညာဉ်ရေးရာ ဆက်နွှယ်မှု နက်ရှိုင်းသည်။ အရာခပ်သိမ်းကို ချစ်ခြင်းမေတ္တာဖြင့် နားလည်ပေးနိုင်သည်။",
        "strengths_en": ["Spiritual empathy", "Artistic vision", "Intuitive wisdom", "Unconditional compassion"],
        "strengths_my": ["ဝိညာဉ်ရေးရာ စာနာမှု", "အနုပညာအမြင်", "အလိုလိုသိဉာဏ်", "အကြွင်းမဲ့ မေတ္တာတရား"],
        "lesson_en": "Ground your spiritual visions into tangible reality and protect your emotional space.",
        "lesson_my": "စိတ်ကူးယဉ်မှုများကို လက်တွေ့ဘဝတွင် အခြေတည်ပြီး မိမိ၏ စိတ်လုံခြုံမှုကို ကာကွယ်ပါ။",
    },
}

MOON_PROFILES = {
    "aries": {
        "en": "Your Moon in Aries feels emotions with fiery immediacy and spontaneous passion. You need autonomy, physical expression, and honest directness to feel emotionally secure.",
        "my": "မိဿရာသီ လမင်းပိုင်ရှင်ဖြစ်၍ စိတ်ခံစားမှုများ လျင်မြန်ပြင်းထန်ပြီး ချက်ချင်းတုံ့ပြန်တတ်သည်။ လွတ်လပ်ခွင့်၊ ရိုးသားပွင့်လင်းမှုနှင့် တက်ကြွစွာ လှုပ်ရှားခြင်းဖြင့် အတွင်းစိတ် အေးချမ်းမှုကို ရရှိသည်။",
        "need_en": "Freedom to act without micromanagement",
        "need_my": "ချုပ်ချယ်မှုမရှိဘဲ လွတ်လပ်စွာ လုပ်ဆောင်ခွင့်",
    },
    "taurus": {
        "en": "Your Moon in Taurus (exalted) finds emotional security in tactile comfort, serene stability, and predictable loyalty. Your inner world is calm, grounded, and deeply restorative.",
        "my": "ပြိဿရာသီ လမင်းပိုင်ရှင်ဖြစ်၍ (လမင်း အမြင့်ဆုံးစွမ်းအင်ရှိသည့် နေရာဖြစ်သောကြောင့်) တည်ငြိမ်အေးချမ်းမှု၊ သစ္စာရှိမှုနှင့် လုံခြုံစိတ်ချရသော ပတ်ဝန်းကျင်တွင် စိတ်ခံစားမှု အထူးတည်ငြိမ်အေးချမ်းစေသည်။",
        "need_en": "Financial stability and emotional consistency",
        "need_my": "ငွေကြေးခိုင်မာမှုနှင့် စိတ်ခံစားမှု တည်ငြိမ်မှု",
    },
    "gemini": {
        "en": "Your Moon in Gemini processes emotional states through mental articulation, conversation, and reading. Verbal connection and intellectual stimulation are your emotional medicine.",
        "my": "မေထုန်ရာသီ လမင်းပိုင်ရှင်ဖြစ်၍ စိတ်ခံစားချက်များကို စကားပြောဆိုဆွေးနွေးခြင်း၊ အတွေးဖလှယ်ခြင်းနှင့် စာဖတ်လေ့လာခြင်းတို့ဖြင့် ဖြေရှင်းလေ့ရှိသည်။ ဆက်သွယ်ပြောဆိုခွင့်ရမှသာ စိတ်သက်သာရာ ရသည်။",
        "need_en": "Open communication and variety of interests",
        "need_my": "ပွင့်လင်းစွာ ဆွေးနွေးခွင့်နှင့် စိတ်ဝင်စားစရာ အသစ်အဆန်းများ",
    },
    "cancer": {
        "en": "Your Moon in Cancer (domicile) possesses profound psychic intuition, deep devotion, and tender vulnerability. You nurture deeply and find safety in your sacred home sanctuary.",
        "my": "ကရကဋ်ရာသီ လမင်းပိုင်ရှင်ဖြစ်၍ (လမင်း၏ မူရင်းအိမ်ဖြစ်သောကြောင့်) မိခင်ဆန်သော စောင့်ရှောက်မှု၊ နက်နဲသော စိတ်ခံစားမှုနှင့် အလိုလိုကြိုတင်သိမြင်နိုင်စွမ်း အထွတ်အထိပ်သို့ ရောက်ရှိသည်။ အိမ်ဂေဟာတွင် အနားယူခြင်းက အားပြည့်စေသည်။",
        "need_en": "Emotional safety and loving roots",
        "need_my": "စိတ်ပိုင်းဆိုင်ရာ လုံခြုံမှုနှင့် နွေးထွေးသော အသိုက်အဝန်း",
    },
    "leo": {
        "en": "Your Moon in Leo needs genuine appreciation, creative self-expression, and romantic loyalty to feel secure. Your inner heart is noble, generous, and proud.",
        "my": "သိဟ်ရာသီ လမင်းပိုင်ရှင်ဖြစ်၍ အသိအမှတ်ပြုခံရခြင်း၊ ချစ်ခင်မြတ်နိုးခံရခြင်းနှင့် ဖန်တီးမှုလုပ်ဆောင်ခြင်းတို့ဖြင့် အတွင်းစိတ် လုံခြုံနွေးထွေးမှု ရရှိသည်။ စိတ်ထားမြင့်မြတ်ပြီး ရက်ရောသည်။",
        "need_en": "Heartfelt appreciation and creative joy",
        "need_my": "လှိုက်လှဲစွာ အသိအမှတ်ပြုခံရမှုနှင့် ပျော်ရွှင်သော ဖန်တီးမှုများ",
    },
    "virgo": {
        "en": "Your Moon in Virgo achieves inner calm through helpful service, organized daily routines, and practical problem-solving. You demonstrate care through tangible acts of assistance.",
        "my": "ကန်ရာသီ လမင်းပိုင်ရှင်ဖြစ်၍ အခြားသူများကို လက်တွေ့ကူညီခြင်း၊ စနစ်တကျ စီစဉ်နေထိုင်ခြင်းနှင့် ပြဿနာများကို ဖြေရှင်းပေးခြင်းဖြင့် စိတ်အေးချမ်းမှု ရရှိသည်။ ဂရုစိုက်မှုကို လက်တွေ့လုပ်ရပ်ဖြင့် ပြသသည်။",
        "need_en": "Order, functional cleanliness, and helpful purpose",
        "need_my": "သပ်ရပ်ကျနမှုနှင့် လက်တွေ့အသုံးဝင်သော ရည်ရွယ်ချက်ရှိခြင်း",
    },
    "libra": {
        "en": "Your Moon in Libra craves harmonious dialogue, peaceful surroundings, and reciprocal partnerships. Conflict and chaotic environments drain your inner reserves.",
        "my": "တူရာသီ လမင်းပိုင်ရှင်ဖြစ်၍ သာယာငြိမ်းချမ်းသော ပတ်ဝန်းကျင်နှင့် အပြန်အလှန်နားလည်သော ဆက်ဆံရေးများရှိမှသာ စိတ်နှလုံး သက်တောင့်သက်သာ ရှိနိုင်သည်။ ပဋိပက္ခများက စိတ်စွမ်းအင်ကို ကုန်ခမ်းစေသည်။",
        "need_en": "Relational harmony and aesthetic grace",
        "need_my": "ဆက်ဆံရေး သဟဇာတဖြစ်မှုနှင့် အေးချမ်းသော အလှတရား",
    },
    "scorpio": {
        "en": "Your Moon in Scorpio experiences emotional depths of immense power. You crave absolute authenticity and loyalty, with the capacity to heal through emotional rebirth.",
        "my": "ဗြိစ္ဆာရာသီ လမင်းပိုင်ရှင်ဖြစ်၍ စိတ်ခံစားမှု အလွန်နက်ရှိုင်းပြင်းထန်ပြီး အပေါ်ယံမဟုတ်သော စစ်မှန်သော သစ္စာတရားကိုသာ လိုလားသည်။ ဝေဒနာများကို ရင်ဆိုင်ကျော်လွှားပြီး စိတ်စွမ်းအားကို ပြန်လည်မွေးဖွားနိုင်သည်။",
        "need_en": "Absolute emotional truth and privacy",
        "need_my": "စစ်မှန်သော သစ္စာတရားနှင့် ကိုယ်ပိုင်လွတ်လပ်ခွင့်",
    },
    "sagittarius": {
        "en": "Your Moon in Sagittarius needs freedom, laughter, and open mental horizons. You process emotional challenges through philosophical perspective and questing for optimism.",
        "my": "ဓနုရာသီ လမင်းပိုင်ရှင်ဖြစ်၍ လွတ်လပ်ခွင့်၊ ပျော်ရွှင်မှုနှင့် ဘဝကို အကောင်းမြင်သည့် သဘောထားရှိမှသာ စိတ်လွတ်လပ်ပေါ့ပါးနိုင်သည်။ ခံစားချက်များကို ဒဿနအမြင်ဖြင့် ဖြေဖျောက်သည်။",
        "need_en": "Spiritual freedom, travel, and optimism",
        "need_my": "ဝိညာဉ်ရေးရာ လွတ်လပ်မှု၊ ခရီးသွားခြင်းနှင့် အကောင်းမြင်စိတ်",
    },
    "capricorn": {
        "en": "Your Moon in Capricorn channels emotional currents into self-reliance, quiet dignity, and practical perseverance. You take emotional responsibilities with supreme seriousness.",
        "my": "မကာရရာသီ လမင်းပိုင်ရှင်ဖြစ်၍ စိတ်ခံစားချက်များကို ထိန်းချုပ်နိုင်စွမ်းရှိပြီး မိမိကိုယ်ကို အားကိုးလိုစိတ်၊ တည်ကြည်ခန့်ညားမှုတို့ဖြင့် အတွင်းစိတ်ကို ထိန်းသိမ်းသည်။ တာဝန်ယူမှုကို အလေးထားသည်။",
        "need_en": "Respect, self-sufficiency, and long-term security",
        "need_my": "လေးစားခံရမှု၊ ကိုယ်တိုင်ရပ်တည်နိုင်မှုနှင့် ရေရှည်လုံခြုံမှု",
    },
    "aquarius": {
        "en": "Your Moon in Aquarius analyzes feelings with objective clarity, emotional independence, and humanitarian friendship. You require autonomy to maintain inner peace.",
        "my": "ကုမ်ရာသီ လမင်းပိုင်ရှင်ဖြစ်၍ စိတ်ခံစားချက်များကို သမာသမတ်ကျကျ သုံးသပ်တတ်ပြီး လွတ်လပ်သော အတွေးအခေါ်နှင့် မိတ်ဆွေသစ္စာဖြင့် စိတ်ချမ်းသာမှု ရှာဖွေသည်။ ချုပ်ချယ်ခံရခြင်းကို မနှစ်သက်ပါ။",
        "need_en": "Personal space and intellectual camaraderie",
        "need_my": "ကိုယ်ပိုင်နေရာလွတ်နှင့် အတွေးတူမိတ်ဆွေများ",
    },
    "pisces": {
        "en": "Your Moon in Pisces dissolves personal boundaries with mystic empathy, poetic sensitivity, and oceanic intuition. You feel the emotional currents of the entire world.",
        "my": "မိန်ရာသီ လမင်းပိုင်ရှင်ဖြစ်၍ မေတ္တာကရုဏာကြီးမားပြီး ပတ်ဝန်းကျင်၏ စိတ်ခံစားချက်များကို ရေမြှုပ်ကဲ့သို့ အလွယ်တကူ စုပ်ယူခံစားမိလေ့ရှိသည်။ အနုပညာနှင့် ဝိညာဉ်ရေးရာတို့က စိတ်ကို ကုသပေးသည်။",
        "need_en": "Spiritual retreat, music, and boundless compassion",
        "need_my": "စိတ်အေးချမ်းရာ ဝိညာဉ်အနားယူခွင့်၊ ဂီတနှင့် စာနာမေတ္တာတရား",
    },
}

RISING_PROFILES = {
    "aries": {
        "en": "Aries Rising enters the world with dynamic vitality, candid courage, and an energetic physical presence. You tackle challenges head-on without hesitating.",
        "my": "မိဿစန်းလဂ်ဖြစ်၍ ရဲရင့်ပြတ်သားသော အသွင်အပြင်၊ တက်ကြွမှုနှင့် တိုက်ရိုက်ပြောဆိုဆက်ဆံတတ်သော ဟန်ပန်ရှိသည်။ အခက်အခဲများကို မဆိုင်းမတွ ရင်ဆိုင်ဖြေရှင်းတတ်သည်။",
        "vibe_en": "Direct, fearless, pioneering",
        "vibe_my": "တိုက်ရိုက်ကျသော၊ ရဲရင့်သော၊ ရှေ့ဆောင်စတင်သူ",
    },
    "taurus": {
        "en": "Taurus Rising projects calming serenity, grounded elegance, and reassuring stability. Your presence naturally soothes others and commands quiet respect.",
        "my": "ပြိဿစန်းလဂ်ဖြစ်၍ တည်ငြိမ်အေးဆေးသော အရှိန်အဝါ၊ ခိုင်မာမှုနှင့် ယုံကြည်အားထားရသော အသွင်အပြင်ကို ပေးစွမ်းသည်။ အခြားသူများကို စိတ်အေးချမ်းစေသည်။",
        "vibe_en": "Patient, sensual, grounded",
        "vibe_my": "စိတ်ရှည်သော၊ အလှတရားကြိုက်သော၊ ခိုင်ခံ့သော",
    },
    "gemini": {
        "en": "Gemini Rising projects witty charm, expressive curiosity, and lively approachability. People are immediately drawn to your conversational sparkle and animated eyes.",
        "my": "မေထုန်စန်းလဂ်ဖြစ်၍ သွက်လက်ဖော်ရွေသော အမူအရာ၊ စူးစမ်းတတ်သော မျက်ဝန်းနှင့် စကားပြောချိုသာဆွဲဆောင်မှုရှိသော ဟန်ပန်ရှိသည်။ လူအများကြားတွင် အလွယ်တကူ ရင်းနှီးနိုင်သည်။",
        "vibe_en": "Inquisitive, animated, social",
        "vibe_my": "စူးစမ်းလိုသော၊ သွက်လက်သော၊ ပေါင်းသင်းဆက်ဆံရေးကောင်းသော",
    },
    "cancer": {
        "en": "Cancer Rising emanates gentle warmth, protective empathy, and approachable intuition. People instinctively feel safe and cared for in your presence.",
        "my": "ကရကဋ်စန်းလဂ်ဖြစ်၍ နူးညံ့သိမ်မွေ့သော မေတ္တာရိပ်၊ နွေးထွေးမှုနှင့် အခြားသူများအား လုံခြုံအေးချမ်းစေသော အရှိန်အဝါရှိသည်။ လူအများက လွယ်ကူစွာ ယုံကြည်ရင်ဖွင့်တတ်သည်။",
        "vibe_en": "Nurturing, intuitive, protective",
        "vibe_my": "နွေးထွေးကြင်နာသော၊ အလိုလိုသိတတ်သော၊ စောင့်ရှောက်တတ်သော",
    },
    "leo": {
        "en": "Leo Rising commands presence with dignified charisma, radiant posture, and a magnificent aura. You naturally become the sun of every room you enter.",
        "my": "သိဟ်စန်းလဂ်ဖြစ်၍ ခန့်ညားထည်ဝါသော ကိုယ်ဟန်၊ ဆွဲဆောင်မှုရှိသော အပြုံးနှင့် အလိုလိုထင်ပေါ်စေသော ခေါင်းဆောင်အရှိန်အဝါရှိသည်။ မည်သည့်နေရာမဆို ထင်ရှားစေသည်။",
        "vibe_en": "Radiant, regal, magnetic",
        "vibe_my": "တောက်ပသော၊ ခန့်ညားသော၊ ဆွဲဆောင်မှုရှိသော",
    },
    "virgo": {
        "en": "Virgo Rising appears observant, impeccably composed, and thoughtfully intelligent. Your attentive demeanor exudes quiet competence and reliability.",
        "my": "ကန်စန်းလဂ်ဖြစ်၍ အကဲခတ်ကောင်းသော အမူအရာ၊ သပ်ရပ်ကျနမှုနှင့် ကျိုးနွံပြီး ဉာဏ်ပညာထက်မြက်သော ဟန်ပန်ကို မြင်တွေ့ရသည်။ အားကိုးထိုက်သော အရည်အသွေးကို ပြသသည်။",
        "vibe_en": "Discerning, articulate, modest",
        "vibe_my": "အကဲခတ်ကောင်းသော၊ သပ်ရပ်ကျနသော၊ ဉာဏ်ရည်ထက်သော",
    },
    "libra": {
        "en": "Libra Rising radiates harmonious grace, balanced symmetry, and refined sociability. You possess an innate aesthetic gift that puts everyone at ease.",
        "my": "တူစန်းလဂ်ဖြစ်၍ ကျက်သရေရှိသော အလှ၊ ယဉ်ကျေးသိမ်မွေ့သော အမူအရာနှင့် အများကြားတွင် ညှိနှိုင်းသင့်မြတ်အောင် ဖန်တီးပေးနိုင်စွမ်းရှိသည်။ ပေါင်းသင်းဆက်ဆံရေး အထူးပြေပြစ်သည်။",
        "vibe_en": "Charming, elegant, diplomatic",
        "vibe_my": "ယဉ်ကျေးသိမ်မွေ့သော၊ ကျက်သရေရှိသော၊ သံတမန်ဆန်သော",
    },
    "scorpio": {
        "en": "Scorpio Rising projects magnetic intensity, penetrating focus, and an unmistakable aura of mystery. People instinctively sense your profound strength.",
        "my": "ဗြိစ္ဆာစန်းလဂ်ဖြစ်၍ ဆွဲဆောင်မှုပြင်းထန်ပြီး လျှို့ဝှက်နက်နဲသော အရှိန်အဝါ၊ ထိုးထွင်းစူးစိုက်ကြည့်တတ်သော မျက်ဝန်းတို့ဖြင့် လေးစားခန့်ညားမှုကို ရရှိစေသည်။",
        "vibe_en": "Intense, magnetic, enigmatic",
        "vibe_my": "နက်နဲပြင်းထန်သော၊ ဆွဲဆောင်မှုရှိသော၊ လျှို့ဝှက်ဆန်းကြယ်သော",
    },
    "sagittarius": {
        "en": "Sagittarius Rising enters with enthusiastic warmth, broad strides, and philosophical openness. Your infectious optimism invites adventurous camaraderie.",
        "my": "ဓနုစန်းလဂ်ဖြစ်၍ ရွှင်လန်းတက်ကြွသော အမူအရာ၊ ပွင့်လင်းသော စိတ်ထားနှင့် စွန့်စားလိုသော အကောင်းမြင်ဟန်ပန်ကို အများက နှစ်သက်ကြည်နူးကြသည်။",
        "vibe_en": "Expansive, jovial, adventurous",
        "vibe_my": "ရွှင်လန်းသော၊ ပွင့်လင်းသော၊ စွန့်စားလိုသော",
    },
    "capricorn": {
        "en": "Capricorn Rising projects poised maturity, architectural discipline, and capable authority. People immediately respect your composed, grounded competence.",
        "my": "မကာရစန်းလဂ်ဖြစ်၍ ရင့်ကျက်တည်ကြည်သော အသွင်၊ စည်းစနစ်ကျနမှုနှင့် တာဝန်ယူနိုင်သော ခေါင်းဆောင်ဟန်ပန်ဖြင့် ယုံကြည်လေးစားမှုကို တည်ဆောက်သည်။",
        "vibe_en": "Authoritative, dignified, resilient",
        "vibe_my": "တည်ကြည်ခန့်ညားသော၊ စည်းကမ်းရှိသော၊ တာဝန်ယူနိုင်သော",
    },
    "aquarius": {
        "en": "Aquarius Rising projects unique individuality, authentic originality, and visionary coolness. You stand comfortably in your distinctive uniqueness.",
        "my": "ကုမ်စန်းလဂ်ဖြစ်၍ ထူးခြားဆန်းသစ်သော ကိုယ်ရည်ကိုယ်သွေး၊ လွတ်လပ်သော အမူအရာနှင့် ခေတ်ရှေ့ပြေးသော စတိုင်လ်ကို ပိုင်ဆိုင်ထားသည်။ မိမိကိုယ်ပိုင်စတိုင်လ်အတိုင်း လျှောက်လှမ်းသည်။",
        "vibe_en": "Original, avant-garde, friendly",
        "vibe_my": "ထူးခြားဆန်းသစ်သော၊ ခေတ်ရှေ့ပြေးသော၊ ဖော်ရွေသော",
    },
    "pisces": {
        "en": "Pisces Rising emanates dreamy poetic grace, compassionate gentleness, and an aura of ethereal enchantment. You move with subtle, artistic intuition.",
        "my": "မိန်စန်းလဂ်ဖြစ်၍ အိပ်မက်ဆန်ဆန် နူးညံ့သောအလှ၊ ကရုဏာပြည့်ဝသော အကြည့်နှင့် အနုပညာဆန်သော ဝိညာဉ်အရှိန်အဝါကို ပေးစွမ်းသည်။ နူးညံ့စွာ သဘောထားကြီးသည်။",
        "vibe_en": "Ethereal, gentle, poetic",
        "vibe_my": "နူးညံ့သိမ်မွေ့သော၊ အနုပညာဆန်သော၊ မေတ္တာပြည့်ဝသော",
    },
}

ASPECT_TYPES = [
    {"name": "Conjunction", "name_my": "ပူးယှဉ်ထောင့် (၀°)", "angle": 0, "orb": 8.0, "type": "unified"},
    {"name": "Sextile", "name_my": "၆၀ ဒီဂရီ မိတ်ဖက်ထောင့်", "angle": 60, "orb": 6.0, "type": "harmonious"},
    {"name": "Square", "name_my": "၉၀ ဒီဂရီ စိန်ခေါ်မှုထောင့်", "angle": 90, "orb": 7.0, "type": "dynamic"},
    {"name": "Trine", "name_my": "၁၂၀ ဒီဂရီ သဟဇာတထောင့်", "angle": 120, "orb": 8.0, "type": "harmonious"},
    {"name": "Opposition", "name_my": "၁၈၀ ဒီဂရီ မျက်နှာချင်းဆိုင်ထောင့်", "angle": 180, "orb": 8.0, "type": "polarity"},
]


def _angular_distance(deg1: float, deg2: float) -> float:
    """Calculate shortest angular distance between two degrees (0-180)."""
    diff = abs(deg1 - deg2) % 360
    return 360 - diff if diff > 180 else diff


def detect_aspects(body_degrees: dict[str, float]) -> list[dict[str, Any]]:
    """Detect all major geometric aspects between planets and points."""
    aspects = []
    keys = list(body_degrees.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            k1, k2 = keys[i], keys[j]
            deg1 = body_degrees[k1]
            deg2 = body_degrees[k2]
            dist = _angular_distance(deg1, deg2)

            for asp in ASPECT_TYPES:
                target = asp["angle"]
                max_orb = asp["orb"]
                actual_orb = abs(dist - target)
                if actual_orb <= max_orb:
                    aspects.append({
                        "body1": k1,
                        "body2": k2,
                        "body1_name": PLANET_NAMES.get(k1, {}).get("en", k1.capitalize()),
                        "body2_name": PLANET_NAMES.get(k2, {}).get("en", k2.capitalize()),
                        "body1_name_my": PLANET_NAMES.get(k1, {}).get("my", k1),
                        "body2_name_my": PLANET_NAMES.get(k2, {}).get("my", k2),
                        "aspect": asp["name"],
                        "aspect_my": asp["name_my"],
                        "angle": target,
                        "orb": round(actual_orb, 2),
                        "type": asp["type"],
                    })
    # Sort by closest orb (most potent aspects first)
    aspects.sort(key=lambda a: a["orb"])
    return aspects


def _generate_aspect_description(asp: dict, locale: str) -> str:
    """Generate meaningful interpretation for a detected aspect."""
    b1 = asp["body1"]
    b2 = asp["body2"]
    atype = asp["aspect"]
    is_my = locale == "my"

    pair = tuple(sorted([b1, b2]))
    
    # Specific aspect meanings
    interpretations = {
        ("moon", "sun"): {
            "Conjunction": (
                "New Moon Soul: Intensely focused unity between your conscious ego and unconscious emotions.",
                "လဆန်းစ ဝိညာဉ်စွမ်းအင် - နေမင်းနှင့် လမင်း ပူးယှဉ်နေသဖြင့် သင့်အသိစိတ်နှင့် မသိစိတ်တို့ တစ်သားတည်းကျကာ ပြင်းထန်သော ရည်ရွယ်ချက်ရှိသည်။",
            ),
            "Opposition": (
                "Full Moon Illumination: Dynamic polarity between emotional needs and conscious identity, creating deep relationship awareness.",
                "လပြည့်ဝန်း အလင်းရောင် - နေမင်းနှင့် လမင်း မျက်နှာချင်းဆိုင်နေသဖြင့် အတွင်းစိတ်ခံစားမှုနှင့် အပြင်ပန်းရည်မှန်းချက်ကြား ချိန်ခွင်လျှာညှိရန် သင်ခန်းစာရှိသည်။",
            ),
            "Trine": (
                "Inner Harmony: Flowing peace between conscious willpower and inner emotional security.",
                "အတွင်းစိတ် သဟဇာတဖြစ်မှု - နေမင်းနှင့် လမင်း ထောင့်ပေါင်းစုံညီ ၁၂၀ ဒီဂရီ ချိတ်ဆက်နေသဖြင့် စိတ်ခံစားမှုနှင့် ဘဝရည်မှန်းချက်တို့ သဘာဝကျကျ သဟဇာတဖြစ်သည်။",
            ),
            "Square": (
                "Growth Friction: Productive tension between past conditioning and future soul purpose.",
                "တိုးတက်မှု စိန်ခေါ်ချက် - နေမင်းနှင့် လမင်း ထောင့်မတ် ၉၀ ဒီဂရီဖြစ်နေသဖြင့် အတိတ်အလေ့အကျင့်ဟောင်းများနှင့် အနာဂတ်ရည်မှန်းချက်ကြား စိန်ခေါ်မှုကို ကျော်လွှားရမည်။",
            ),
        },
        ("mars", "venus"): {
            "Conjunction": (
                "Passionate Magnetism: Fusion of romantic attraction and sexual willpower, yielding irresistible charismatic presence.",
                "ဆွဲဆောင်မှု စွမ်းအား - သောကြာနှင့် အင်္ဂါ ပူးယှဉ်နေသဖြင့် အချစ်ရေး၊ ဆွဲဆောင်မှုနှင့် တက်ကြွသော စွမ်းအင်တို့ ပေါင်းစပ်ကာ ဆွဲဆောင်မှု အလွန်မြင့်မားသည်။",
            ),
            "Trine": (
                "Romantic Grace: Harmonious balance between receiving love and actively pursuing desire.",
                "အချစ်ရေး သဟဇာတ - သောကြာနှင့် အင်္ဂါ သဟဇာတဖြစ်နေသဖြင့် အချစ်ရေးနှင့် ဆက်ဆံရေးများတွင် သဘာဝကျကျ အဆင်ပြေချောမွေ့စေသည်။",
            ),
            "Square": (
                "Creative Tension: High erotic energy and passionate sparks that demand conscious communication to avoid unnecessary drama.",
                "ပြင်းထန်သော ဆွဲဆောင်မှု - သောကြာနှင့် အင်္ဂါ ထောင့်မတ်ကျနေသဖြင့် ဆက်ဆံရေးများတွင် စိတ်လှုပ်ရှားဖွယ် ပြင်းထန်သော်လည်း နားလည်မှု ပိုမိုတည်ဆောက်ရန် လိုအပ်သည်။",
            ),
        },
        ("mercury", "sun"): {
            "Conjunction": (
                "Cazimi / Sun-Mercury Alignment: Sharp, laser-focused mind where your identity is deeply tied to ideas and articulate communication.",
                "နေမင်းနှင့် ဗုဒ္ဓဟူး ပူးယှဉ်မှု - ဉာဏ်ရည်ထက်မြက်ပြီး မိမိ၏ အတွေးအခေါ်နှင့် ဆက်သွယ်ပြောဆိုမှုများတွင် ထူးချွန်ထင်ရှားသည်။",
            ),
        },
    }

    if pair in interpretations and atype in interpretations[pair]:
        en_desc, my_desc = interpretations[pair][atype]
        return my_desc if is_my else en_desc

    # General aspect templates
    if atype == "Trine":
        return (
            f"{asp['body1_name_my']} နှင့် {asp['body2_name_my']} တို့ ၁၂၀ ဒီဂရီ သဟဇာတဖြစ်နေသဖြင့် ဤဂြိုဟ်နှစ်ခု၏ စွမ်းအင်များသည် မွေးရာပါ အရည်အချင်းအဖြစ် လွယ်ကူချောမွေ့စွာ စီးဆင်းနေသည်။"
            if is_my else
            f"Trine between {asp['body1_name']} and {asp['body2_name']} represents a natural gift and effortless harmonic flow of energy."
        )
    elif atype == "Square":
        return (
            f"{asp['body1_name_my']} နှင့် {asp['body2_name_my']} တို့ ၉၀ ဒီဂရီ ထောင့်မတ်ကျနေသဖြင့် အတွင်းစိတ်တွန်းအားနှင့် စိန်ခေါ်မှုကို ဖြစ်ပေါ်စေပြီး ကြီးမားသော အောင်မြင်မှုအတွက် တွန်းအားပေးသည်။"
            if is_my else
            f"Square between {asp['body1_name']} and {asp['body2_name']} creates evolutionary tension that catalyzes powerful personal breakthroughs."
        )
    elif atype == "Opposition":
        return (
            f"{asp['body1_name_my']} နှင့် {asp['body2_name_my']} တို့ ၁၈၀ ဒီဂရီ ဆန့်ကျင်ဘက်ဖြစ်နေသဖြင့် ဘဝ၏ ဤကဏ္ဍနှစ်ခုကြားတွင် မျှတမှုကို ရှာဖွေတည်ဆောက်ရန် သင်ခန်းစာပေးသည်။"
            if is_my else
            f"Opposition between {asp['body1_name']} and {asp['body2_name']} invites conscious integration of complementary life polarities."
        )
    elif atype == "Conjunction":
        return (
            f"{asp['body1_name_my']} နှင့် {asp['body2_name_my']} တို့ ပူးယှဉ်ပေါင်းစပ်နေသဖြင့် အလွန်ပြင်းထန်သော စွမ်းအင်ဗဟိုချက်ကို ဖန်တီးပေးသည်။"
            if is_my else
            f"Conjunction blends the powers of {asp['body1_name']} and {asp['body2_name']} into an intense, focused engine of action."
        )
    else:  # Sextile
        return (
            f"{asp['body1_name_my']} နှင့် {asp['body2_name_my']} တို့ ၆၀ ဒီဂရီ မိတ်ဖက်ထောင့်ကျနေသဖြင့် အခွင့်အလမ်းကောင်းများနှင့် ပူးပေါင်းလုပ်ဆောင်မှုများကို အကျိုးပြုစေသည်။"
            if is_my else
            f"Sextile between {asp['body1_name']} and {asp['body2_name']} stimulates supportive opportunities and creative collaboration."
        )


def _synthesize_triad(sun: str, moon: str, rising: str, locale: str) -> str:
    """Synthesize the Big Three dynamic interaction."""
    sun_elem = ZODIAC_META.get(sun, {}).get("element", "fire")
    moon_elem = ZODIAC_META.get(moon, {}).get("element", "water")
    rising_elem = ZODIAC_META.get(rising, {}).get("element", "earth")

    is_my = locale == "my"

    if is_my:
        return (
            f"သင့်ဇာတာတွင် နေမင်း ({ZODIAC_META[sun]['my']}) ၏ ဘဝရည်မှန်းချက်၊ "
            f"လမင်း ({ZODIAC_META[moon]['my']}) ၏ အတွင်းစိတ်ခံစားမှုနှင့် "
            f"စန်းလဂ် ({ZODIAC_META[rising]['my']}) ၏ အပြင်ပန်းပုံရိပ်တို့ စုပေါင်းလှုပ်ရှားနေပါသည်။ "
            f"နေမင်းသည် {sun_elem.upper()} ဓာတ်ဖြစ်ပြီး လမင်းသည် {moon_elem.upper()} ဓာတ်၊ စန်းလဂ်သည် {rising_elem.upper()} ဓာတ်ဖြစ်သဖြင့် "
            f"အတွင်းစိတ်၏ နက်ရှိုင်းမှုနှင့် အပြင်ပန်း လှုပ်ရှားဆောင်ရွက်မှုများကြားတွင် စိတ်ဝင်စားဖွယ် သဟဇာတဖြစ်မှုကို ဖြစ်ပေါ်စေသည်။ "
            f"အခြားသူများက သင့်အား စန်းလဂ်၏ အရှိန်အဝါဖြင့် ပထမဆုံး မြင်တွေ့ရသော်လည်း သင့်အတွင်းစိတ်အမှန်မှာ နေမင်းနှင့် လမင်း၏ နက်နဲသော စွမ်းအားဖြင့် မောင်းနှင်နေပါသည်။"
        )
    else:
        return (
            f"Your Big Three creates an intricate alchemy: a {ZODIAC_META[sun]['en']} Sun ({sun_elem} element), "
            f"a {ZODIAC_META[moon]['en']} Moon ({moon_elem} element), and a {ZODIAC_META[rising]['en']} Rising ({rising_elem} element). "
            f"While the world first experiences your {ZODIAC_META[rising]['en']} Rising lens, your core choices are energized by the "
            f"radiance of your {ZODIAC_META[sun]['en']} Sun, and your deepest private sanctuary is nourished by your {ZODIAC_META[moon]['en']} Moon. "
            f"Integrating these three elements allows your authentic purpose to shine without friction."
        )


def _compute_element_distribution(chart: dict) -> dict[str, Any]:
    """Calculate Fire, Earth, Air, Water distribution from chart planets."""
    counts = {"fire": 0, "earth": 0, "air": 0, "water": 0}
    total = 0

    # Sun, Moon, Rising
    for sign_key in [chart.get("sun_sign"), chart.get("moon_sign"), chart.get("rising_sign")]:
        if sign_key in ZODIAC_META:
            counts[ZODIAC_META[sign_key]["element"]] += 2  # Double weight for big three
            total += 2

    # Planets
    for p in chart.get("planets", []):
        sign = p.get("sign")
        if sign in ZODIAC_META:
            counts[ZODIAC_META[sign]["element"]] += 1
            total += 1

    percentages = {}
    dominant = "fire"
    max_count = -1
    for elem, count in counts.items():
        pct = round((count / max(total, 1)) * 100)
        percentages[elem] = pct
        if count > max_count:
            max_count = count
            dominant = elem

    return {
        "counts": counts,
        "percentages": percentages,
        "dominant": dominant,
        "total": total,
    }


def generate_birth_chart_explanation(chart: dict, locale: str = "en") -> dict[str, Any]:
    """Generate comprehensive, in-depth bilingual Birth Chart interpretation."""
    is_my = locale == "my"

    sun_sign = chart.get("sun_sign", "aries")
    moon_sign = chart.get("moon_sign", "taurus")
    rising_sign = chart.get("rising_sign", "gemini")

    sun_prof = SUN_PROFILES.get(sun_sign, SUN_PROFILES["aries"])
    moon_prof = MOON_PROFILES.get(moon_sign, MOON_PROFILES["taurus"])
    rising_prof = RISING_PROFILES.get(rising_sign, RISING_PROFILES["gemini"])

    # Collect degrees for aspect calculations
    body_degrees = {}
    if chart.get("sun_degree") is not None:
        body_degrees["sun"] = float(chart["sun_degree"])
    if chart.get("moon_degree") is not None:
        body_degrees["moon"] = float(chart["moon_degree"])
    if chart.get("rising_degree") is not None:
        body_degrees["rising"] = float(chart["rising_degree"])

    planets_list = chart.get("planets", [])
    for p in planets_list:
        name = p.get("name")
        deg = p.get("degree")
        if name and deg is not None:
            body_degrees[name] = float(deg)

    # Detect major aspects
    raw_aspects = detect_aspects(body_degrees)
    aspects = []
    for asp in raw_aspects[:10]:  # Top 10 most exact aspects
        desc = _generate_aspect_description(asp, locale)
        aspects.append({
            **asp,
            "description": desc,
        })

    # Elemental breakdown
    elements = _compute_element_distribution(chart)

    # Archetype titles
    archetype_en = f"The {ZODIAC_META.get(sun_sign, {}).get('en', '')} Architect of Destiny"
    archetype_my = f"{ZODIAC_META.get(sun_sign, {}).get('my', '')} ၏ ကံကြမ္မာဗိသုကာရှင်"

    # Core Identity Section
    core_identity = {
        "title": "ပင်မမဏ္ဍိုင် ၃ မျိုး (The Big Three Core Identity)" if is_my else "The Big Three (Core Identity)",
        "sun": {
            "sign": sun_sign,
            "name": PLANET_NAMES["sun"]["my"] if is_my else PLANET_NAMES["sun"]["en"],
            "symbol": PLANET_NAMES["sun"]["symbol"],
            "sign_display": ZODIAC_META.get(sun_sign, {}).get("my" if is_my else "en", sun_sign),
            "essence": sun_prof["my" if is_my else "en"],
            "strengths": sun_prof["strengths_my" if is_my else "strengths_en"],
            "growth_lesson": sun_prof["lesson_my" if is_my else "lesson_en"],
        },
        "moon": {
            "sign": moon_sign,
            "name": PLANET_NAMES["moon"]["my"] if is_my else PLANET_NAMES["moon"]["en"],
            "symbol": PLANET_NAMES["moon"]["symbol"],
            "sign_display": ZODIAC_META.get(moon_sign, {}).get("my" if is_my else "en", moon_sign),
            "essence": moon_prof["my" if is_my else "en"],
            "need": moon_prof["need_my" if is_my else "need_en"],
        },
        "rising": {
            "sign": rising_sign,
            "name": PLANET_NAMES["rising"]["my"] if is_my else PLANET_NAMES["rising"]["en"],
            "symbol": PLANET_NAMES["rising"]["symbol"],
            "sign_display": ZODIAC_META.get(rising_sign, {}).get("my" if is_my else "en", rising_sign),
            "essence": rising_prof["my" if is_my else "en"],
            "vibe": rising_prof["vibe_my" if is_my else "vibe_en"],
        },
        "triad_synthesis": _synthesize_triad(sun_sign, moon_sign, rising_sign, locale),
    }

    # Planetary interpretations
    planetary_breakdown = []
    for p in planets_list:
        p_name = p.get("name", "")
        p_sign = p.get("sign", "")
        p_deg = p.get("degree")
        p_rx = p.get("retrograde", False)

        meta = PLANET_NAMES.get(p_name, {"en": p_name.capitalize(), "my": p_name, "symbol": "✦"})
        sign_meta = ZODIAC_META.get(p_sign, {"en": p_sign, "my": p_sign, "element": "", "modality": ""})

        # Generate descriptive interpretation
        if is_my:
            rx_text = " (သွားလမ်းနောက်ပြန် - Retrograde ℞)" if p_rx else ""
            interp = (
                f"{meta['my']} သည် {sign_meta['my']} တွင် တည်ရှိပါသည်{rx_text}။ "
                f"ဤအနေအထားသည် သင့်ဘဝ၏ {meta.get('domain_my', 'ကဏ္ဍ')} တွင် "
                f"{sign_meta['en']} ၏ စွမ်းအင်များကို ထင်ရှားစေပါသည်။"
            )
        else:
            rx_text = " (Retrograde ℞)" if p_rx else ""
            interp = (
                f"{meta['en']} in {sign_meta['en']}{rx_text}: "
                f"Expresses its influence through {sign_meta['en']}'s archetype, "
                f"shaping your {meta.get('domain_en', 'life dimension')}."
            )

        planetary_breakdown.append({
            "name": p_name,
            "display_name": meta["my"] if is_my else meta["en"],
            "symbol": meta.get("symbol", "✦"),
            "sign": p_sign,
            "sign_display": sign_meta["my"] if is_my else sign_meta["en"],
            "degree": p_deg,
            "retrograde": p_rx,
            "domain": meta.get("domain_my" if is_my else "domain_en", ""),
            "interpretation": interp,
        })

    # Guidance summary
    guidance = (
        "သင့်မွေးဖွားမှုဇာတာသည် သင့်အား ကန့်သတ်ထားသော ဘောင်တစ်ခုမဟုတ်ဘဲ "
        "သင့်ဝိညာဉ်၏ အမြင့်မားဆုံး စွမ်းရည်များကို အကောင်အထည်ဖော်ရန် လမ်းညွှန်ပြသပေးသော ကောင်းကင်ဘုံမြေပုံဖြစ်ပါသည်။ "
        "အလင်းရောင်နှင့် အမှောင်ခြမ်း၊ အားသာချက်နှင့် သင်ခန်းစာများကို သဟဇာတဖြစ်အောင် ပေါင်းစပ်အသုံးပြုပါ။"
        if is_my else
        "Your birth chart is not a rigid script, but an evolutionary cosmic map. "
        "Use your natural trines as flowing gifts, your squares as engines of mastery, and "
        "let your Sun, Moon, and Ascendant work together in radiant synergy."
    )

    return {
        "archetype_title": archetype_my if is_my else archetype_en,
        "core_identity": core_identity,
        "aspects": aspects,
        "planetary_breakdown": planetary_breakdown,
        "elemental_constitution": {
            "dominant": elements["dominant"],
            "percentages": elements["percentages"],
            "analysis": (
                f"သင့်ဇာတာတွင် {elements['dominant'].upper()} ဓာတ် အားအကောင်းဆုံးဖြစ်ပြီး စုစုပေါင်း၏ {elements['percentages'][elements['dominant']]}% ပါဝင်ပါသည်။"
                if is_my else
                f"Your chart is predominantly governed by the {elements['dominant'].upper()} element ({elements['percentages'][elements['dominant']]}%)."
            ),
        },
        "guidance": guidance,
    }
