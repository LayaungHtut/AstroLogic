import re
import random
import logging
from typing import Optional
from app.services.openrouter_service import chat_with_assistant
from app.services.tarot_api_client import BUILTIN_CARDS

logger = logging.getLogger(__name__)

# Zodiac sign database with bilingual details
ZODIAC_DATA = {
    "aries": {
        "en": "Aries", "my": "မိဿရာသီ", "element_en": "Fire", "element_my": "မီးဓာတ်",
        "modality_en": "Cardinal", "modality_my": "အစပျိုး (Cardinal)",
        "ruler_en": "Mars", "ruler_my": "အင်္ဂါဂြိုဟ်",
        "dates_my": "မတ် ၂၁ - ဧပြီ ၁၉",
        "traits_my": ["ရဲရင့်ပြတ်သားသူ", "ရည်မှန်းချက်ကြီးသူ", "ရှေ့ဆောင်လမ်းပြ", "စိတ်အားထက်သန်သူ", "ပွင့်လင်းရိုးသားသူ"],
        "traits_en": ["Bold", "Ambitious", "Pioneering", "Passionate", "Direct"],
        "summary_my": "မီးဓာတ်စွမ်းအင်ရှင် မိဿရာသီဖွားများသည် ရဲရင့်ပြတ်သားပြီး ရှေ့ဆောင်လမ်းပြ အစပြုလိုစိတ် ပြင်းပြသူများ ဖြစ်ကြသည်။ အခက်အခဲများကို မကြောက်မရွံ့ ရင်ဆိုင်နိုင်စွမ်းရှိပြီး လုပ်ဆောင်ချက်များကို ချက်ချင်းလက်ငင်း အကောင်အထည်ဖော်လိုကြသည်။",
        "career_my": "ခေါင်းဆောင်မှု၊ စွန့်ဦးတီထွင်မှုနှင့် စိန်ခေါ်မှုများသော လုပ်ငန်းခွင်များတွင် အလွန်ထူးချွန်ပါသည်။ အစီအစဉ်သစ်များကို စတင်ဦးဆောင်ရာတွင် အကောင်းဆုံး စွမ်းဆောင်ရည်ကို ပြသနိုင်ပါသည်။",
        "love_my": "ချစ်ခြင်းမေတ္တာတွင် စိတ်အားထက်သန်ပြီး ပွင့်လင်းရိုးသားစွာ ချစ်တတ်ကြသည်။ သို့သော် တစ်ဖက်လူ၏ ခံစားချက်ကို စိတ်ရှည်စွာ နားထောင်ပေးရန်နှင့် အလျင်စလို ဆုံးဖြတ်ခြင်းကို လျှော့ချရန် လိုအပ်ပါသည်။",
        "advice_my": "အလျင်စလို ဆုံးဖြတ်ခြင်းကို ရှောင်ရှားပြီး ရေရှည်မျှော်တွေးကာ အဆင့်ဆင့် လျှောက်လှမ်းပါ။"
    },
    "taurus": {
        "en": "Taurus", "my": "ပြိဿရာသီ", "element_en": "Earth", "element_my": "မြေဓာတ်",
        "modality_en": "Fixed", "modality_my": "တည်ငြိမ် (Fixed)",
        "ruler_en": "Venus", "ruler_my": "သောကြာဂြိုဟ်",
        "dates_my": "ဧပြီ ၂၀ - မေ ၂၀",
        "traits_my": ["တည်ငြိမ်အေးဆေးသူ", "စိတ်ရှည်သည်းခံသူ", "ယုံကြည်အားထားရသူ", "သစ္စာရှိသူ", "ဇွဲရှိသူ"],
        "traits_en": ["Grounded", "Patient", "Reliable", "Loyal", "Determined"],
        "summary_my": "မြေဓာတ်စွမ်းအင်ရှင် ပြိဿရာသီဖွားများသည် စိတ်ရှည်တည်ငြိမ်ပြီး သစ္စာရှိကာ အလှအပနှင့် လုံခြုံစိတ်ချရမှုကို မြတ်နိုးကြသည်။ ခိုင်မာသော အခြေခံကောင်းများကို တည်ဆောက်ရာတွင် အလွန်စိတ်ချရသူများ ဖြစ်ကြသည်။",
        "career_my": "ဘဏ္ဍာရေး၊ စီမံခန့်ခွဲမှု၊ စိုက်ပျိုးရေးနှင့် အနုပညာဆိုင်ရာ လုပ်ငန်းများတွင် ထူးချွန်ပါသည်။ အရာရာကို အချိန်ယူ၍ စေ့စပ်သေချာစွာ ပြီးမြောက်အောင် ဆောင်ရွက်တတ်ကြသည်။",
        "love_my": "ချစ်သူအပေါ် အလွန်သစ္စာစောင့်သိပြီး ရေရှည်တည်မြဲသော ဆက်ဆံရေးကို တန်ဖိုးထားသည်။ တစ်ခါတစ်ရံ ခေါင်းမာတတ်မှုကို လျှော့ချပြီး လိုက်လျောညီထွေရှိရန် လိုအပ်ပါသည်။",
        "advice_my": "စိတ်လောကြီးခြင်းမရှိဘဲ ဖြည်းဖြည်းနှင့်မှန်မှန် ခိုင်မာစွာ တည်ဆောက်သွားပါ။"
    },
    "gemini": {
        "en": "Gemini", "my": "မေထုန်ရာသီ", "element_en": "Air", "element_my": "လေဓာတ်",
        "modality_en": "Mutable", "modality_my": "ပြောင်းလဲလွယ် (Mutable)",
        "ruler_en": "Mercury", "ruler_my": "ဗုဒ္ဓဟူးဂြိုဟ်",
        "dates_my": "မေ ၂၁ - ဇွန် ၂၀",
        "traits_my": ["စူးစမ်းလိုစိတ်ရှိသူ", "လိုက်လျောညီထွေနေတတ်သူ", "ဉာဏ်ရည်ထက်မြက်သူ", "ပြောဆိုဆက်ဆံရေးကောင်းသူ", "ဗဟုသုတကြွယ်ဝသူ"],
        "traits_en": ["Curious", "Adaptable", "Witty", "Expressive", "Versatile"],
        "summary_my": "လေဓာတ်စွမ်းအင်ရှင် မေထုန်ရာသီဖွားများသည် ဉာဏ်ရည်ထက်မြက်ပြီး လိုက်လျောညီထွေရှိကာ စူးစမ်းရှာဖွေလိုစိတ် ပြင်းပြကြသည်။ အတွေးအခေါ်သစ်များကို အမြဲလေ့လာသင်ယူလိုပြီး ဆက်ဆံရေးနယ်ပယ် ကျယ်ပြန့်သည်။",
        "career_my": "မီဒီယာ၊ စာပေ၊ နည်းပညာ၊ ဆက်သွယ်ရေးနှင့် အရောင်းဆိုင်ရာ ကဏ္ဍများတွင် အထူးအောင်မြင်နိုင်ပါသည်။",
        "love_my": "ဉာဏ်ရည်ချင်း စကားပြောဆိုဆက်သွယ်နိုင်သော မိတ်ဖက်ကို သဘောကျသည်။ စိတ်နှစ်ခွဖြစ်တတ်မှုကို သတိပြုပြီး တည်ငြိမ်သော သံယောဇဉ်ကို တည်ဆောက်သင့်သည်။",
        "advice_my": "စိတ်ဒွိဟဖြစ်မှုများကို ရှင်းလင်းပြတ်သားသော သတင်းအချက်အလက်များဖြင့် ဖြေရှင်းပါ။"
    },
    "cancer": {
        "en": "Cancer", "my": "ကရကဋ်ရာသီ", "element_en": "Water", "element_my": "ရေဓာတ်",
        "modality_en": "Cardinal", "modality_my": "အစပျိုး (Cardinal)",
        "ruler_en": "Moon", "ruler_my": "လမင်း",
        "dates_my": "ဇွန် ၂၁ - ဇူလိုင် ၂၂",
        "traits_my": ["နွေးထွေးကြင်နာသူ", "စာနာနားလည်တတ်သူ", "အလိုလိုသိစိတ်ထက်မြက်သူ", "မိသားစုကိုချစ်မြတ်နိုးသူ", "ကာကွယ်စောင့်ရှောက်လိုသူ"],
        "traits_en": ["Intuitive", "Nurturing", "Empathetic", "Protective", "Loyal"],
        "summary_my": "ရေဓာတ်စွမ်းအင်ရှင် ကရကဋ်ရာသီဖွားများသည် နက်ရှိုင်းသော စိတ်ခံစားချက်၊ ထက်မြက်သော အလိုလိုသိစိတ်နှင့် နွေးထွေးသော မေတ္တာတရားတို့ကို ပိုင်ဆိုင်ထားကြသည်။ ချစ်ခင်ရသူများကို အနစ်နာခံကာကွယ်စောင့်ရှောက်တတ်ကြသည်။",
        "career_my": "ကျန်းမာရေး၊ ပညာရေး၊ စိတ်ပညာ၊ အိမ်ခြံမြေနှင့် လူမှုဖူလုံရေး လုပ်ငန်းများတွင် စိတ်စေတနာထက်သန်စွာ စွမ်းဆောင်နိုင်ပါသည်။",
        "love_my": "အလွန်နက်ရှိုင်းသော သံယောဇဉ်ဖြင့် ချစ်တတ်သည်။ အတိတ်မှ စိတ်ဒဏ်ရာများကို လက်လွှတ်ပြီး မိမိကိုယ်ကို ချစ်ခင်တန်ဖိုးထားရန် အထူးအရေးကြီးပါသည်။",
        "advice_my": "သင့်၏ နက်ရှိုင်းသော အလိုလိုသိစိတ်နှင့် အတွင်းစိတ်ခွန်အားကို ယုံကြည်ပါ။ စိတ်ခံစားချက်များကို လုံခြုံစွာ ထိန်းသိမ်းပြီး ရှေ့ဆက်ပါ။"
    },
    "leo": {
        "en": "Leo", "my": "သိဟ်ရာသီ", "element_en": "Fire", "element_my": "မီးဓာတ်",
        "modality_en": "Fixed", "modality_my": "တည်ငြိမ် (Fixed)",
        "ruler_en": "Sun", "ruler_my": "နေမင်း",
        "dates_my": "ဇူလိုင် ၂၃ - သြဂုတ် ၂၂",
        "traits_my": ["ယုံကြည်မှုပြည့်ဝသူ", "ရက်ရောစွန့်ကြဲသူ", "ခေါင်းဆောင်ကောင်း", "စိတ်အားထက်သန်သူ", "သစ္စာရှိသူ"],
        "traits_en": ["Confident", "Generous", "Charismatic", "Warm-hearted", "Proud"],
        "summary_my": "မီးဓာတ်စွမ်းအင်ရှင် သိဟ်ရာသီဖွားများသည် နေမင်းကဲ့သို့ တောက်ပသော စွမ်းအင်၊ မွန်မြတ်သော စေတနာနှင့် ခေါင်းဆောင်မှု သဘာဝကို ပိုင်ဆိုင်ထားကြသည်။ ရက်ရောကြင်နာပြီး ချစ်ခင်လေးစားမှုကို ရရှိတတ်သည်။",
        "career_my": "အနုပညာ၊ စီမံအုပ်ချုပ်မှု၊ ဖျော်ဖြေရေးနှင့် ပြည်သူ့ဆက်ဆံရေး ကဏ္ဍများတွင် ထူးချွန်ထင်ရှားကြသည်။",
        "love_my": "ချစ်သူအပေါ် အလွန်ရက်ရောပြီး နွေးထွေးစွာ ကာကွယ်စောင့်ရှောက်တတ်သည်။ မာနထက် နားလည်မှုကို ဦးစားပေးသင့်သည်။",
        "advice_my": "မာနထက် နားလည်မှုကို ဦးစားပေးပြီး သင်၏ တောက်ပသော စွမ်းအင်ဖြင့် အောင်မြင်မှုကို အရယူပါ။"
    },
    "virgo": {
        "en": "Virgo", "my": "ကန်ရာသီ", "element_en": "Earth", "element_my": "မြေဓာတ်",
        "modality_en": "Mutable", "modality_my": "ပြောင်းလဲလွယ် (Mutable)",
        "ruler_en": "Mercury", "ruler_my": "ဗုဒ္ဓဟူးဂြိုဟ်",
        "dates_my": "သြဂုတ် ၂၃ - စက်တင်ဘာ ၂၂",
        "traits_my": ["စေ့စပ်သေချာသူ", "လက်တွေ့ကျသူ", "ကူညီတတ်သူ", "စနစ်ကျသူ", "ဉာဏ်ထက်သူ"],
        "traits_en": ["Analytical", "Meticulous", "Helpful", "Practical", "Hardworking"],
        "summary_my": "မြေဓာတ်စွမ်းအင်ရှင် ကန်ရာသီဖွားများသည် စေ့စပ်သေချာပြီး စနစ်တကျ ပြင်ဆင်နိုင်စွမ်းရှိကာ အခြားသူများကို ကူညီဖေးမလိုစိတ် ပြင်းပြကြသည်။",
        "career_my": "သုတေသန၊ အချက်အလက်ဆန်းစစ်မှု၊ ကျန်းမာရေးစောင့်ရှောက်မှုနှင့် အရည်အသွေးထိန်းသိမ်းရေး လုပ်ငန်းများတွင် အထူးတော်ကြသည်။",
        "love_my": "အသေးစိတ်အချက်အလက်လေးတွေအထိ ဂရုတစိုက် ချစ်တတ်သည်။ အရာရာ ပြီးပြည့်စုံလွန်းရမည်ဟူသော အတွေးကို လျှော့ချသင့်သည်။",
        "advice_my": "အသေးစိတ်ကို အလေးထားသော်လည်း အရာရာ ပြီးပြည့်စုံလွန်းရမည်ဟူသော စိုးရိမ်စိတ်ကို လျှော့ချပါ။"
    },
    "libra": {
        "en": "Libra", "my": "တူရာသီ", "element_en": "Air", "element_my": "လေဓာတ်",
        "modality_en": "Cardinal", "modality_my": "အစပျိုး (Cardinal)",
        "ruler_en": "Venus", "ruler_my": "သောကြာဂြိုဟ်",
        "dates_my": "စက်တင်ဘာ ၂၃ - အောက်တိုဘာ ၂၂",
        "traits_my": ["တရားမျှတသူ", "သဟဇာတဖြစ်လိုသူ", "သံတမန်ဆန်သူ", "အလှအပမြတ်နိုးသူ", "ယဉ်ကျေးသိမ်မွေ့သူ"],
        "traits_en": ["Diplomatic", "Fair-minded", "Harmonious", "Charming", "Social"],
        "summary_my": "လေဓာတ်စွမ်းအင်ရှင် တူရာသီဖွားများသည် မျှတမှု၊ ငြိမ်းချမ်းရေးနှင့် သဟဇာတဖြစ်မှုကို တန်ဖိုးထားကြသည်။ လူမှုဆက်ဆံရေး ပြေပြစ်ပြီး သံတမန်ဆန်စွာ ဆွေးနွေးဖြေရှင်းတတ်ကြသည်။",
        "career_my": "ဥပဒေရေးရာ၊ သံတမန်ဆက်ဆံရေး၊ ဒီဇိုင်း၊ အနုပညာနှင့် ညှိနှိုင်းရေးလုပ်ငန်းများတွင် ထူးချွန်ကြသည်။",
        "love_my": "လက်တွဲဖော်နှင့် ညီမျှသော သဟဇာတဖြစ်မှုကို လိုလားသည်။ ဆုံးဖြတ်ရခက်သော ဒွိဟစိတ်ကို လျှော့ချပြီး ရဲရင့်စွာ ရွေးချယ်သင့်သည်။",
        "advice_my": "လမ်းကြောင်းနှစ်ခုကြား ဝေခွဲမရဖြစ်မနေဘဲ မိမိ၏ အတွင်းစိတ်အမှန်တရားအတိုင်း သတ္တိရှိရှိ ရွေးချယ်ပါ။"
    },
    "scorpio": {
        "en": "Scorpio", "my": "ဗြိစ္ဆာရာသီ", "element_en": "Water", "element_my": "ရေဓာတ်",
        "modality_en": "Fixed", "modality_my": "တည်ငြိမ် (Fixed)",
        "ruler_en": "Pluto / Mars", "ruler_my": "ပလူတိုဂြိုဟ် / အင်္ဂါဂြိုဟ်",
        "dates_my": "အောက်တိုဘာ ၂၃ - နိုဝင်ဘာ ၂၁",
        "traits_my": ["ထိုးထွင်းသိမြင်သူ", "စိတ်ပိုင်းဖြတ်မှုခိုင်မာသူ", "သစ္စာနက်ရှိုင်းသူ", "လျှို့ဝှက်ချက်ထိန်းနိုင်သူ", "သတ္တိရှိသူ"],
        "traits_en": ["Intuitive", "Passionate", "Determined", "Transformative", "Loyal"],
        "summary_my": "ရေဓာတ်စွမ်းအင်ရှင် ဗြိစ္ဆာရာသီဖွားများသည် စူးရှသော ထိုးထွင်းအမြင်၊ ခိုင်မာသော စိတ်ပိုင်းဖြတ်မှုနှင့် ဘဝကို အသွင်ပြောင်းလဲနိုင်သော စွမ်းအားကို ပိုင်ဆိုင်ထားကြသည်။",
        "career_my": "စုံစမ်းထောက်လှမ်းရေး၊ စိတ်ပညာ၊ ဆေးပညာ၊ ဘဏ္ဍာရေးရင်းနှီးမြှုပ်နှံမှုနှင့် သုတေသနများတွင် အလွန်ထူးချွန်ပါသည်။",
        "love_my": "အလွန်နက်ရှိုင်းစွာ ချစ်တတ်ပြီး သစ္စာတရားကို အသက်တမျှ တန်ဖိုးထားသည်။ သံသယစိတ်ကို လျှော့ချပြီး ယုံကြည်မှု တည်ဆောက်သင့်သည်။",
        "advice_my": "အတိတ်ဟောင်းများကို လက်လွှတ်စွန့်လွှတ်ပြီး အသစ်တဖန် ပြန်လည်မွေးဖွားသည့်သဖွယ် အားသစ်မွေးပါ။"
    },
    "sagittarius": {
        "en": "Sagittarius", "my": "ဓနုရာသီ", "element_en": "Fire", "element_my": "မီးဓာတ်",
        "modality_en": "Mutable", "modality_my": "ပြောင်းလဲလွယ် (Mutable)",
        "ruler_en": "Jupiter", "ruler_my": "ကြာသပတေးဂြိုဟ်",
        "dates_my": "နိုဝင်ဘာ ၂၂ - ဒီဇင်ဘာ ၂၁",
        "traits_my": ["အကောင်းမြင်စိတ်ရှိသူ", "လွတ်လပ်မှုကိုမြတ်နိုးသူ", "အမြင်ကျယ်သူ", "ရိုးသားပွင့်လင်းသူ", "စွန့်စားလိုသူ"],
        "traits_en": ["Optimistic", "Adventurous", "Philosophical", "Honest", "Freedom-loving"],
        "summary_my": "မီးဓာတ်စွမ်းအင်ရှင် ဓနုရာသီဖွားများသည် အကောင်းမြင်စိတ်ပြည့်ဝပြီး လွတ်လပ်မှုကို မြတ်နိုးကာ ဘဝ၏ အမှန်တရားနှင့် အသိပညာသစ်များကို စဉ်ဆက်မပြတ် ရှာဖွေလိုကြသည်။",
        "career_my": "ခရီးသွားလာရေး၊ ဒဿနိကဗေဒ၊ ပညာရေး၊ ဥပဒေနှင့် နိုင်ငံတကာဆက်ဆံရေးများတွင် အောင်မြင်နိုင်ပါသည်။",
        "love_my": "လွတ်လပ်မှုကို အပြန်အလှန် လေးစားသော ဆက်ဆံရေးကို နှစ်သက်သည်။ စိတ်ရှည်မှု ထားရှိရန် လိုအပ်သည်။",
        "advice_my": "ပန်းတိုင်ကို ရှင်းလင်းစွာ မြင်ယောင်ပြီး စိတ်အားထက်သန်စွာဖြင့် ဇွဲမလျှော့ဘဲ ဆက်လက်လျှောက်လှမ်းပါ။"
    },
    "capricorn": {
        "en": "Capricorn", "my": "မကာရရာသီ", "element_en": "Earth", "element_my": "မြေဓာတ်",
        "modality_en": "Cardinal", "modality_my": "အစပျိုး (Cardinal)",
        "ruler_en": "Saturn", "ruler_my": "စနေဂြိုဟ်",
        "dates_my": "ဒီဇင်ဘာ ၂၂ - ဇန်နဝါရီ ၁၉",
        "traits_my": ["စည်းကမ်းရှိသူ", "ဇွဲလုံ့လကြီးမားသူ", "ရည်မှန်းချက်မြင့်သူ", "တာဝန်ယူမှုရှိသူ", "လက်တွေ့ကျသူ"],
        "traits_en": ["Disciplined", "Ambitious", "Patient", "Responsible", "Resourceful"],
        "summary_my": "မြေဓာတ်စွမ်းအင်ရှင် မကာရရာသီဖွားများသည် စည်းကမ်းခိုင်မာပြီး မဆုတ်မနစ်သော ဇွဲလုံ့လဖြင့် ရေရှည်ရည်မှန်းချက်များကို အဆင့်ဆင့် အောင်မြင်အောင် တည်ဆောက်နိုင်ကြသည်။",
        "career_my": "စီးပွားရေးစီမံခန့်ခွဲမှု၊ အုပ်ချုပ်ရေး၊ အင်ဂျင်နီယာနှင့် အစိုးရပိုင်းဆိုင်ရာ တာဝန်ကြီးမားသော နေရာများတွင် ထူးချွန်ကြသည်။",
        "love_my": "သစ္စာရှိပြီး တည်ငြိမ်သော မိသားစုဘဝကို တန်ဖိုးထားသည်။ စိတ်ခံစားချက်များကို ပိုမိုပွင့်လင်းစွာ ထုတ်ဖော်ပြသသင့်သည်။",
        "advice_my": "အချိန်ယူတည်ဆောက်ရသောအရာများသည် ခိုင်ခံ့မြဲမြံစမြဲဖြစ်ကြောင်း သတိပြုကာ စိတ်ရှည်စွာ ရှေ့ဆက်ပါ။"
    },
    "aquarius": {
        "en": "Aquarius", "my": "ကုမ်ရာသီ", "element_en": "Air", "element_my": "လေဓာတ်",
        "modality_en": "Fixed", "modality_my": "တည်ငြိမ် (Fixed)",
        "ruler_en": "Uranus / Saturn", "ruler_my": "ယူရေးနပ်စ်ဂြိုဟ် / စနေဂြိုဟ်",
        "dates_my": "ဇန်နဝါရီ ၂၀ - ဖေဖော်ဝါရီ ၁၈",
        "traits_my": ["တီထွင်ဆန်းသစ်သူ", "လွတ်လပ်သူ", "ရှေ့ပြေးအမြင်ရှိသူ", "လူသားဝါဒီ", "မူပိုင်အတွေးအခေါ်ရှိသူ"],
        "traits_en": ["Innovative", "Independent", "Visionary", "Humanitarian", "Original"],
        "summary_my": "လေဓာတ်စွမ်းအင်ရှင် ကုမ်ရာသီဖွားများသည် သမားရိုးကျ ဘောင်များမှ ခွဲထွက်၍ ထူးခြားဆန်းသစ်သော ရှေ့ပြေးအမြင်နှင့် လူသားအားလုံး အကျိုးပြုစိတ်ကူးများကို ဖော်ဆောင်တတ်ကြသည်။",
        "career_my": "သိပ္ပံ၊ နည်းပညာ၊ လူမှုရေးလှုပ်ရှားမှု၊ တီထွင်ဖန်တီးမှုနှင့် အနာဂတ်စီမံကိန်းများတွင် ထူးချွန်ကြသည်။",
        "love_my": "စိတ်ချင်းဆက်သွယ်နိုင်သော မိတ်ဆွေသဖွယ် လက်တွဲဖော်ကို သဘောကျသည်။ စိတ်ခံစားချက်ကို အဝေးကမကြည့်ဘဲ နီးကပ်စွာ ထိတွေ့သင့်သည်။",
        "advice_my": "သမားရိုးကျ ဘောင်များမှ ခွဲထွက်ပြီး သင့်ကိုယ်ပိုင် နည်းလမ်းသစ်ဖြင့် ဖန်တီးတီထွင်ပါ။"
    },
    "pisces": {
        "en": "Pisces", "my": "မိန်ရာသီ", "element_en": "Water", "element_my": "ရေဓာတ်",
        "modality_en": "Mutable", "modality_my": "ပြောင်းလဲလွယ် (Mutable)",
        "ruler_en": "Neptune / Jupiter", "ruler_my": "နက်ပကျွန်းဂြိုဟ် / ကြာသပတေးဂြိုဟ်",
        "dates_my": "ဖေဖော်ဝါရီ ၁၉ - မတ် ၂၀",
        "traits_my": ["စာနာကြင်နာသူ", "အနုပညာမြတ်နိုးသူ", "အလိုလိုသိစိတ်အားကောင်းသူ", "စိတ်ကူးဉာဏ်ကြွယ်သူ", "မေတ္တာကြီးမားသူ"],
        "traits_en": ["Compassionate", "Artistic", "Intuitive", "Gentle", "Spiritual"],
        "summary_my": "ရေဓာတ်စွမ်းအင်ရှင် မိန်ရာသီဖွားများသည် နူးညံ့သိမ်မွေ့သော မေတ္တာ၊ အလိုလိုသိမြင်နိုင်သော စိတ်ဝိညာဉ်စွမ်းအားနှင့် အနုပညာဆန်သော စိတ်ကူးဉာဏ်ကို ပိုင်ဆိုင်ထားကြသည်။",
        "career_my": "ဂီတ၊ အနုပညာ၊ စာပေ၊ ကုသစောင့်ရှောက်ရေး၊ ဝိညာဉ်ရေးရာနှင့် ဖန်တီးမှုလုပ်ငန်းများတွင် အလွန်ထူးချွန်ပါသည်။",
        "love_my": "အချစ်ကို အလွန်နက်ရှိုင်းစွာ မြတ်နိုးတန်ဖိုးထားသည်။ စိတ်ကူးယဉ်မှုနှင့် လက်တွေ့ဘဝကို ဟန်ချက်ညီစေရန် လိုအပ်ပါသည်။",
        "advice_my": "စိတ်ကူးယဉ်မှုနှင့် လက်တွေ့ဘဝကို ဟန်ချက်ညီစေပြီး မိမိ၏ နှလုံးသားအသံကို နားထောင်ပါ။"
    }
}

# Burmese card aliases for major cards
BURMESE_CARD_MAP = {
    "the hermit": "The Hermit", "ရသေ့": "The Hermit", "ရသေ့ကတ်": "The Hermit", "hermit": "The Hermit",
    "the fool": "The Fool", "လူမိုက်": "The Fool", "fool": "The Fool",
    "the magician": "The Magician", "မျက်လှည့်": "The Magician", "magician": "The Magician",
    "the high priestess": "The High Priestess", "နတ်ဆရာမ": "The High Priestess", "priestess": "The High Priestess",
    "the empress": "The Empress", "မိဖုရား": "The Empress", "empress": "The Empress",
    "the emperor": "The Emperor", "ဧကရာဇ်": "The Emperor", "emperor": "The Emperor",
    "the hierophant": "The Hierophant", "ဆရာတော်": "The Hierophant", "hierophant": "The Hierophant",
    "the lovers": "The Lovers", "ချစ်သူများ": "The Lovers", "lovers": "The Lovers",
    "the chariot": "The Chariot", "စစ်ရထား": "The Chariot", "chariot": "The Chariot",
    "strength": "Strength", "ခွန်အား": "Strength",
    "wheel of fortune": "Wheel of Fortune", "ကံကြမ္မာဘီး": "Wheel of Fortune", "ဘီး": "Wheel of Fortune",
    "justice": "Justice", "တရားမျှတမှု": "Justice",
    "the hanged man": "The Hanged Man", "တွဲလောင်း": "The Hanged Man", "hanged man": "The Hanged Man",
    "death": "Death", "သေခြင်း": "Death", "သေခြင်းတရား": "Death",
    "temperance": "Temperance", "မျှတမှု": "Temperance",
    "the devil": "The Devil", "မိစ္ဆာ": "The Devil", "devil": "The Devil",
    "the tower": "The Tower", "မျှော်စင်": "The Tower", "tower": "The Tower",
    "the star": "The Star", "ကြယ်": "The Star", "star": "The Star",
    "the moon": "The Moon", "လမင်း": "The Moon", "moon": "The Moon",
    "the sun": "The Sun", "နေမင်း": "The Sun", "sun": "The Sun",
    "judgement": "Judgement", "တရားစီရင်ခြင်း": "Judgement",
    "the world": "The World", "ကမ္ဘာလောက": "The World", "world": "The World"
}


class ChatService:
    @staticmethod
    async def chat(
        message: str,
        zodiac_sign: Optional[str] = None,
        current_reading: Optional[dict] = None,
        chat_history: Optional[list[dict]] = None,
        locale: str = "en"
    ) -> str:
        # First attempt OpenRouter if API key is present
        try:
            response = await chat_with_assistant(
                message=message,
                zodiac_sign=zodiac_sign,
                current_reading=current_reading,
                chat_history=chat_history,
            )
            if response and len(response.strip()) > 0:
                return response
        except Exception as e:
            logger.warning(f"OpenRouter chat failed or unconfigured, using AstroLogic Oracle: {e}")

        # Fallback to local intelligent knowledge-based conversation
        return ChatService.generate_fallback(
            message=message,
            zodiac_sign=zodiac_sign,
            current_reading=current_reading,
            locale=locale
        )

    @staticmethod
    def generate_fallback(
        message: str,
        zodiac_sign: Optional[str] = None,
        current_reading: Optional[dict] = None,
        locale: str = "en"
    ) -> str:
        msg = message.strip()
        msg_lower = msg.lower()
        is_myanmar = (locale == "my") or bool(re.search(r"[က-႟]", msg))

        # 1. Check if user is asking about a specific Tarot card
        card_response = ChatService._handle_tarot_card_query(msg_lower, is_myanmar)
        if card_response:
            return card_response

        # 2. Check if user is asking about element interactions / compatibility
        element_response = ChatService._handle_element_query(msg_lower, is_myanmar)
        if element_response:
            return element_response

        # 3. Check if user is asking how tarot readings or AstroLogic works
        how_it_works_response = ChatService._handle_how_it_works_query(msg_lower, is_myanmar)
        if how_it_works_response:
            return how_it_works_response

        # 4. Check if user is asking about Zodiac signs (their own or a mentioned sign)
        zodiac_response = ChatService._handle_zodiac_query(msg_lower, zodiac_sign, is_myanmar)
        if zodiac_response:
            return zodiac_response

        # 5. Check if user is asking about Love / Partner timing
        love_response = ChatService._handle_love_query(msg_lower, zodiac_sign, current_reading, is_myanmar)
        if love_response:
            return love_response

        # 6. Check if user is asking about Career / Job / Money
        career_response = ChatService._handle_career_query(msg_lower, zodiac_sign, current_reading, is_myanmar)
        if career_response:
            return career_response

        # 7. Check if user is asking a decision / yes-no query
        decision_response = ChatService._handle_decision_query(msg_lower, zodiac_sign, current_reading, is_myanmar)
        if decision_response:
            return decision_response

        # 8. Greetings & identity
        greeting_response = ChatService._handle_greeting_query(msg_lower, is_myanmar)
        if greeting_response:
            return greeting_response

        # 9. General supportive astrological fallback
        return ChatService._handle_general_query(msg, zodiac_sign, current_reading, is_myanmar)

    @staticmethod
    def _handle_tarot_card_query(msg_lower: str, is_myanmar: bool) -> Optional[str]:
        matched_card_name = None
        for alias, card_name in BURMESE_CARD_MAP.items():
            if alias in msg_lower:
                matched_card_name = card_name
                break

        if not matched_card_name:
            for c in BUILTIN_CARDS:
                if c["name"].lower() in msg_lower:
                    matched_card_name = c["name"]
                    break

        if not matched_card_name:
            return None

        card_info = next((c for c in BUILTIN_CARDS if c["name"] == matched_card_name), None)
        if not card_info:
            return None

        name = card_info["name"]
        meaning_up = card_info.get("meaning_up", "")
        meaning_rev = card_info.get("meaning_rev", "")

        if is_myanmar:
            return f"""### 🔮 **{name} တားရော့ကတ် အနက်ဖွင့်ဆိုချက်**

**{name}** သည် တားရော့ဗေဒင်တွင် အလွန်လေးနက်ပြီး အဓိပ္ပာယ်ပြည့်ဝသော သင်္ကေတတစ်ခု ဖြစ်ပါသည်။

* **အလင်းဘက်ခြမ်း (Upright Energy)**: {meaning_up}
  * ဤကတ်သည် သင့်ဘဝတွင် အတွင်းစိတ်ဉာဏ်ပညာ၊ တည်ငြိမ်မှုနှင့် သစ္စာတရားကို အခြေပြု၍ အဖြေရှာရန် လမ်းပြပေးနေပါသည်။ ပြင်ပလောက၏ ဆူညံမှုများမှ ခေတ္တခွာပြီး မိမိကိုယ်ကို ပြန်လည်ဆန်းစစ်ရန် သင့်တော်သော အခိုက်အတန့်ဖြစ်ပါသည်။
* **သတိပြုဖွယ် / အရိပ်ဘက်ခြမ်း (Reversed Energy)**: {meaning_rev}
  * ပြောင်းပြန်အနေအထားတွင်မူ အထီးကျန်ဆန်လွန်းခြင်း၊ ပတ်ဝန်းကျင်နှင့် အဆက်အသွယ်ဖြတ်တောက်မိခြင်း သို့မဟုတ် အတွင်းစိတ်အမှန်တရားကို ရင်မဆိုင်လိုဘဲ ရှောင်လွှဲနေခြင်းတို့ကို သတိပြုဆင်ခြင်ရန် ညွှန်ပြပါသည်။

**လက်တွေ့ကျင့်သုံးရန် လမ်းညွှန်ချက်**:
စိတ်အေးချမ်းမှုရှိသော နေရာတစ်ခုတွင် တိတ်ဆိတ်စွာ အနားယူပြီး သင်၏ အလိုလိုသိစိတ် (Intuition) ကို နားထောင်ပါ။ အဖြေမှန်သည် သင့်အတွင်းစိတ်ထဲတွင် ရှိပြီးသား ဖြစ်ပါသည်။"""
        else:
            return f"""### 🔮 **Tarot Archetype: {name}**

**{name}** is a profoundly symbolic archetype in the Tarot journey.

* **Upright Energy (Light & Empowerment)**: {meaning_up}
  * When upright, this card encourages introspective wisdom, looking inward for light, and relying on soul guidance rather than external noise.
* **Reversed Energy (Shadow & Caution)**: {meaning_rev}
  * In reverse, it cautions against excessive isolation, resisting inner truths, or feeling disconnected from supportive relationships.

**Guidance for Your Path**:
Take a quiet moment to listen to your inner guidance. The clarity you seek is already unfolding within your intuitive awareness."""

    @staticmethod
    def _handle_element_query(msg_lower: str, is_myanmar: bool) -> Optional[str]:
        has_fire = any(k in msg_lower for k in ["fire", "မီး"])
        has_water = any(k in msg_lower for k in ["water", "ရေ"])
        has_earth = any(k in msg_lower for k in ["earth", "မြေ"])
        has_air = any(k in msg_lower for k in ["air", "လေ"])

        if has_fire and has_water:
            if is_myanmar:
                return """### 🌌 **မီးဓာတ် (Fire) နှင့် ရေဓာတ် (Water) ရာသီခွင်များ၏ ဆက်နွယ်မှု**

မီးဓာတ် (Aries, Leo, Sagittarius) နှင့် ရေဓာတ် (Cancer, Scorpio, Pisces) တို့၏ ပေါင်းစပ်မှုသည် **စိတ်အားထက်သန်မှုနှင့် နက်ရှိုင်းသော ခံစားချက်များ** ရောယှက်နေသည့် စိတ်ဝင်စားဖွယ် သဘာဝတစ်ခု ဖြစ်ပါသည်။

* **အားသာချက် (Harmony & Growth)**:
  * မီး၏ ရဲရင့်တက်ကြွမှုသည် ရေ၏ နူးညံ့သိမ်မွေ့မှုကို နွေးထွေးရှင်သန်စေပြီး ယုံကြည်မှု တိုးပွားစေပါသည်။
  * ရေ၏ စာနာနားလည်မှုနှင့် အလိုလိုသိစိတ်သည် မီး၏ စိတ်လောကြီးမှုနှင့် အရှိန်လွန်ကဲမှုကို အေးငြိမ်းတည်ငြိမ်စေပါသည်။
* **သတိပြုဖွယ် (Dynamic Friction)**:
  * ရေက မီးကို ငြှိမ်းသတ်မိသလို မဖြစ်စေရန် (ရေဓာတ်ရှင်များအနေဖြင့် မီးဓာတ်ရှင်၏ လွတ်လပ်မှုကို အလွန်အကျွံ မချုပ်ချယ်ရန်) လိုအပ်ပါသည်။
  * မီးက ရေကို ဆူပွက်ခမ်းခြောက်စေသလို မဖြစ်စေရန် (မီးဓာတ်ရှင်များအနေဖြင့် စကားအပြောအဆို ကြမ်းတမ်းခြင်းကို ထိန်းသိမ်းရန်) လိုအပ်ပါသည်။

**ဆက်ဆံရေး အကြံပြုချက်**: 
ပွင့်လင်းစွာ စကားပြောဆိုပြီး နှစ်ဦးနှစ်ဖက်၏ မတူကွဲပြားသော စွမ်းအင်များကို လေးစားတန်ဖိုးထားပါက မေတ္တာနက်ရှိုင်းသော စုံတွဲတစ်တွဲ ဖြစ်လာနိုင်ပါသည်။"""
            else:
                return """### 🌌 **Elemental Alchemy: Fire & Water Signs**

The connection between Fire signs (Aries, Leo, Sagittarius) and Water signs (Cancer, Scorpio, Pisces) is an intense blend of **passion, vulnerability, and transformation**.

* **Harmonious Flow**: Fire inspires Water with confidence, warmth, and action, while Water nurtures Fire with deep empathy and emotional depth.
* **Potential Friction**: Fire can overwhelm sensitive Water with directness, while Water's moodiness can occasionally dampen Fire's enthusiasm.
* **Wisdom for Growth**: Balance passionate initiative with empathetic listening. When both partners respect their differing emotional languages, this creates an unbreakable bond."""

        if (has_fire and has_air) or (has_earth and has_water):
            if is_myanmar:
                return """### 🌌 **သဘာဝချင်း လိုက်လျောညီထွေရှိသော ဓာတ်ကြီးများ ဆက်နွယ်မှု**

နက္ခတ်ဗေဒင်တွင် **မီး နှင့် လေ**၊ **မြေ နှင့် ရေ** တို့သည် တစ်ခုကိုတစ်ခု သဘာဝအလျောက် အားဖြည့်ပေးသော သဟဇာတဓာတ်များ ဖြစ်ကြပါသည်။

* **မြေ နှင့် ရေ**: မြေက ရေကို လုံခြုံတည်ငြိမ်သော ခံယူချက် ပေးစွမ်းနိုင်ပြီး၊ ရေက မြေကို စိုစွတ်ရှင်သန်စေသောကြောင့် အလွန်တည်မြဲခိုင်မာသော လက်တွဲဖော်များ ဖြစ်စေပါသည်။
* **မီး နှင့် လေ**: လေက မီးကို ပိုမိုတောက်ပစေပြီး၊ မီးက လေကို စိတ်အားထက်သန်သော အရှိန်အဟုန် ရရှိစေသောကြောင့် စိတ်ကူးသစ်များနှင့် အောင်မြင်မှုများ အတူတကွ ဖော်ဆောင်နိုင်ပါသည်။"""
            else:
                return """### 🌌 **Elemental Harmony: Complementary Elements**

In astrology, **Fire & Air** and **Earth & Water** are naturally complementary element pairings.

* **Earth & Water**: Earth provides safe containment, loyalty, and practical grounding, while Water enriches Earth with emotional warmth and intuitive life.
* **Fire & Air**: Air feeds Fire with ideas, mental clarity, and communication, while Fire ignites Air with purpose, creativity, and vibrant passion."""

        return None

    @staticmethod
    def _handle_how_it_works_query(msg_lower: str, is_myanmar: bool) -> Optional[str]:
        if any(k in msg_lower for k in ["how do tarot", "how tarot work", "how does tarot work", "မည်သို့ အလုပ်လုပ်", "ဘယ်လိုအလုပ်လုပ်", "ဗေဒင် အလုပ်လုပ်"]):
            if is_myanmar:
                return """### 🌟 **တားရော့ဗေဒင် မည်သို့ အလုပ်လုပ်သနည်း?**

တားရော့ဗေဒင်သည် အနာဂတ်ကို တရားသေ ကြိုတင်သတ်မှတ်ထားသော ကံကြမ္မာအဖြစ် ဟောကိန်းထုတ်ခြင်း **မဟုတ်ပါ**။

* **မသိစိတ်၏ ကြေးမုံပြင် (Mirror of the Subconscious)**:
  * လူသားတို့၏ နေ့စဉ်ဘဝတွင် ရင်ဆိုင်နေရသော အတွေးများ၊ စိတ်ခံစားချက်များနှင့် စွမ်းအင်စီးဆင်းမှုများကို ၇၈ ကတ်သော စကြာဝဠာသင်္ကေတ (Archetypes) များဖြင့် ထင်ဟပ်ဖော်ပြပေးခြင်း ဖြစ်ပါသည်။
* **သတိပြုဆင်ခြင်နိုင်စွမ်း (Mindful Awareness)**:
  * ကျရောက်လာသော ကတ်များသည် လက်ရှိအခြေအနေ၊ သင့်အတွင်းစိတ်ခွန်အားနှင့် ကြိုတင်သတိပြုရမည့် စိန်ခေါ်မှုများကို ရှင်းလင်းစွာ မြင်သာစေပါသည်။
* **မိမိကိုယ်တိုင် ရွေးချယ်ဖန်တီးနိုင်မှု (Empowered Choice)**:
  * တားရော့သည် အနာဂတ်ကို ချည်နှောင်ထားခြင်းမရှိဘဲ၊ ပိုမိုမှန်ကန်ကောင်းမွန်သော ဆုံးဖြတ်ချက်များကို သတ္တိရှိရှိ ချမှတ်နိုင်စေရန် အလင်းပြပေးသော လမ်းညွှန်ကြယ်စင် ဖြစ်ပါသည်။"""
            else:
                return """### 🌟 **How Does Tarot Work in AstroLogic?**

Tarot is **not** deterministic fortune-telling. Rather, it serves as an intuitive mirror for conscious self-reflection.

* **Mirror of the Subconscious**: The 78 archetypal cards reflect the subtle psychological currents, emotional dynamics, and intuitive signals active in your current reality.
* **Synchronicity & Symbolic Language**: The cards drawn resonate with your present energetic focus, highlighting hidden opportunities and shadow blindspots.
* **Empowered Decision-Making**: Tarot never limits your destiny; it empowers you with clarity so you can shape your future with conscious intention."""
        return None

    @staticmethod
    def _handle_zodiac_query(msg_lower: str, zodiac_sign: Optional[str], is_myanmar: bool) -> Optional[str]:
        target_sign = None
        for key, data in ZODIAC_DATA.items():
            if key in msg_lower or data["my"] in msg_lower or data["en"].lower() in msg_lower:
                target_sign = key
                break

        if not target_sign and zodiac_sign:
            z_clean = zodiac_sign.lower().strip()
            if z_clean in ZODIAC_DATA and any(k in msg_lower for k in ["my sign", "zodiac", "ရာသီခွင်", "ကျွန်ုပ်၏", "ကျွန်တော့်", "ငါ့"]):
                target_sign = z_clean

        if not target_sign:
            return None

        z = ZODIAC_DATA[target_sign]
        is_career = any(k in msg_lower for k in ["career", "job", "work", "အလုပ်", "စီးပွား"])
        is_love = any(k in msg_lower for k in ["love", "relationship", "partner", "အချစ်", "ချစ်သူ"])

        if is_myanmar:
            extra = ""
            if is_career:
                extra = f"\n\n💼 **အလုပ်အကိုင်ဆိုင်ရာ လမ်းညွှန်ချက်**: {z['career_my']}"
            elif is_love:
                extra = f"\n\n💖 **အချစ်ရေးနှင့် သံယောဇဉ်**: {z['love_my']}"

            return f"""### ♈ **{z['my']} ({z['en']}) ဆိုင်ရာ နက္ခတ်ဗေဒင် လက္ခဏာရပ်များ**

* **ဓာတ်သဘာဝ**: {z['element_my']}
* **အုပ်စိုးသော ဂြိုဟ်**: {z['ruler_my']}
* **လက္ခဏာ အချိန်ကာလ**: {z['dates_my']}
* **ထူးခြားသော အားသာချက်များ**: {', '.join(z['traits_my'])}

**ပင်ကိုစရိုက် သဘောတရား**:
{z['summary_my']}{extra}

🌱 **ဘဝခရီးလမ်း အကြံပြုချက်**:
{z['advice_my']}"""
        else:
            extra = ""
            if is_career:
                extra = f"\n\n💼 **Career Profile**: {z['career_my']}"
            elif is_love:
                extra = f"\n\n💖 **Romantic Profile**: {z['love_my']}"

            return f"""### ♈ **Zodiac Profile: {z['en']}**

* **Element**: {z['element_en']}
* **Ruling Planet**: {z['ruler_en']}
* **Core Traits**: {', '.join(z['traits_en'])}

**Essence & Expression**:
{z['summary_my']}{extra}

🌱 **Wisdom for Your Sign**:
{z['advice_my']}"""

    @staticmethod
    def _handle_love_query(
        msg_lower: str,
        zodiac_sign: Optional[str],
        current_reading: Optional[dict],
        is_myanmar: bool
    ) -> Optional[str]:
        if not any(k in msg_lower for k in ["ချစ်သူ", "အချစ်", "ရည်းစား", "ကြာဦးမှာလား", "love", "boyfriend", "girlfriend", "crush", "marriage"]):
            return None

        sign_text = ""
        if zodiac_sign and zodiac_sign.lower().strip() in ZODIAC_DATA:
            z = ZODIAC_DATA[zodiac_sign.lower().strip()]
            sign_text = f"{z['my']} ဖွားတစ်ဦးအနေဖြင့် " if is_myanmar else f"As a {z['en']}, "

        if is_myanmar:
            return f"""### 💖 **အချစ်ရေးနှင့် လက်တွဲဖော်ဆိုင်ရာ တားရော့လမ်းညွှန်ချက်**

သင်၏ မေးခွန်းနှင့် စပ်လျဉ်း၍ တားရော့စွမ်းအင်များကို နက်ရှိုင်းစွာ ဆန်းစစ်ရလျှင် -

{sign_text}စစ်မှန်သော ချစ်ခြင်းမေတ္တာသည် အချိန်ကာလကို လောလောလောလော တွက်ချက်ရှာဖွေခြင်းထက် **မိမိကိုယ်တိုင် ပြည့်စုံပျော်ရွှင်နေချိန်** တွင် အလိုအလျောက် ဆုံဆည်းလာတတ်သော သဘာဝရှိပါသည်။

* **လက်ရှိ အရေးကြီးသော အဆင့်**:
  * အတိတ်မှ စိတ်ဒဏ်ရာများ သို့မဟုတ် မလုံခြုံသော သံသယများကို အရင်ဆုံး လက်လွှတ်ကုစားပါ။
  * နေ့စဉ်ဘဝတွင် မိမိကိုယ်ကို တန်ဖိုးထားချစ်ခင်ပြီး စိတ်ပိုင်းဆိုင်ရာ တည်ငြိမ်မှုကို အရင်ခိုင်မာအောင် တည်ဆောက်ပါ။
* **အချိန်ကာလနှင့် စွမ်းအင်စီးဆင်းမှု**:
  * ကတ်များ၏ ညွှန်ပြချက်အရ လောလောဆယ်တွင် အလျင်စလို မရှာဖွေဘဲ လူမှုဆက်ဆံရေးနယ်ပယ်သစ်များသို့ ပေါ့ပါးစွာ ထိတွေ့နေထိုင်ရန် အကြံပြုထားပါသည်။ မိမိဘက်မှ အဆင်သင့်ဖြစ်ချိန်တွင် သင့်အတွက် အသင့်တော်ဆုံး စစ်မှန်သော မေတ္တာရှင်သည် မမျှော်လင့်ဘဲ ရောက်ရှိလာပါလိမ့်မည်။

**နွေးထွေးသော စကားလက်ဆောင်**: စိတ်ချမ်းသာစွာဖြင့် နေ့စဉ်ဘဝကို ပျော်ရွှင်အောင် နေထိုင်ပါ။ အချစ်စစ်သည် သင့်ဆီသို့ လျှောက်လှမ်းနေဆဲ ဖြစ်ပါသည်။"""
        else:
            return f"""### 💖 **Love & Relationship Intuitive Insight**

{sign_text}Tarot reminds us that authentic love is drawn to an open, wholehearted spirit.

* **Present Energy**: Focus on emotional self-worth and releasing lingering past heartbreaks.
* **Timing & Flow**: Rather than worrying about a deadline, create space for genuine connection. When your internal emotional home is peaceful, the right partner naturally finds their way to you."""

    @staticmethod
    def _handle_career_query(
        msg_lower: str,
        zodiac_sign: Optional[str],
        current_reading: Optional[dict],
        is_myanmar: bool
    ) -> Optional[str]:
        if not any(k in msg_lower for k in ["အလုပ်", "ရာထူး", "စီးပွား", "career", "job", "work", "promotion"]):
            return None

        sign_text = ""
        if zodiac_sign and zodiac_sign.lower().strip() in ZODIAC_DATA:
            z = ZODIAC_DATA[zodiac_sign.lower().strip()]
            sign_text = f"{z['my']} ဖွားတစ်ဦးအနေဖြင့် " if is_myanmar else f"As a {z['en']}, "

        if is_myanmar:
            return f"""### 💼 **အလုပ်အကိုင်နှင့် စီးပွားရေးဆိုင်ရာ တားရော့လမ်းညွှန်ချက်**

{sign_text}လက်ရှိလုပ်ငန်းခွင် အခြေအနေနှင့် စပ်လျဉ်း၍ တားရော့စွမ်းအင်များက အောက်ပါအတိုင်း အကြံပြုထားပါသည် -

* **အခွင့်အလမ်းနှင့် စွမ်းဆောင်ရည်**:
  * သင့်တွင် ရှိပြီးသား ကျွမ်းကျင်မှုနှင့် ကြိုးစားအားထုတ်လိုစိတ်သည် အောင်မြင်မှုအတွက် ခိုင်မာသော အခြေခံကောင်း ဖြစ်နေပါသည်။
  * အသစ်သော ပညာရပ်များ သင်ယူခြင်းနှင့် လုပ်ငန်းခွင် ဆက်ဆံရေးကောင်းမွန်အောင် ထိန်းသိမ်းခြင်းတို့က တိုးတက်မှုကို အရှိန်မြှင့်ပေးပါလိမ့်မည်။
* **သတိပြုဖွယ် အချက်**:
  * အလုပ်ပြောင်းလဲရန် သို့မဟုတ် စီမံကိန်းအသစ် စတင်ရန် စဉ်းစားနေပါက၊ အလျင်စလို မဆုံးဖြတ်ဘဲ အချက်အလက်နှင့် အစီအစဉ်များကို စနစ်တကျ ပြင်ဆင်ပြီးမှသာ ခြေလှမ်းလှမ်းပါ။

**အကြံပြုချက်**: မိမိ၏ အရည်အချင်းကို ယုံကြည်စိတ်ချစွာ အသုံးချပါ။ ဇွဲလုံ့လဖြင့် ကြိုးစားမှုသည် ထိုက်တန်သော ရလဒ်ကောင်းကို ပေးစွမ်းပါလိမ့်မည်။"""
        else:
            return f"""### 💼 **Career & Strategic Guidance**

{sign_text}the cards highlight positive momentum grounded in patience and clarity.

* **Strategic Focus**: Lean into your natural strengths and maintain high standards of integrity.
* **Timing**: If considering a major transition, ensure your foundation is solid before making the leap. Trust your skills and move with purposeful deliberation."""

    @staticmethod
    def _handle_decision_query(
        msg_lower: str,
        zodiac_sign: Optional[str],
        current_reading: Optional[dict],
        is_myanmar: bool
    ) -> Optional[str]:
        if not any(k in msg_lower for k in ["သင့်သလား", "ရမလား", "ဖြစ်မလား", "ကောင်းမလား", "should i", "will i", "can i", "decision", "choice"]):
            return None

        if is_myanmar:
            return """### ⚖️ **ရွေးချယ်ဆုံးဖြတ်မှုဆိုင်ရာ တားရော့စွမ်းအင် ဆန်းစစ်ချက်**

တားရော့သည် တရားသေ "ဟုတ်/မဟုတ်" အဖြေပေးခြင်းထက်၊ သင်၏ ဆုံးဖြတ်ချက်နောက်ကွယ်ရှိ **စွမ်းအင်အလားအလာနှင့် သတိပြုဖွယ်ရာများ** ကို အောက်ပါအတိုင်း ညွှန်ပြနေပါသည် -

* **အပြုသဘောဆောင်သော အလားအလာ**:
  * သင် ရွေးချယ်လိုသော လမ်းကြောင်းတွင် အောင်မြင်နိုင်ခြေနှင့် တိုးတက်မှုအခွင့်အလမ်းများ ရှိနေပါသည်။
* **ချိန်ဆရမည့် အချက်**:
  * နှလုံးသား၏ ခံစားချက်တစ်ခုတည်းဖြင့် မဆုံးဖြတ်ဘဲ၊ ဦးနှောက်၏ လက်တွေ့ကျသော အချက်အလက်များနှင့် ချိန်ဆပါ။
  * အရေးကြီးသော ဆုံးဖြတ်ချက်မချမီ စိတ်တည်ငြိမ်အေးဆေးသော အချိန်ကို ရွေးချယ်ပါ။

**လမ်းညွှန်ချက်**: မည်သည့်လမ်းကြောင်းကို ရွေးချယ်သည်ဖြစ်စေ၊ သင့်ကိုယ်သင် ယုံကြည်မှုအပြည့်ဖြင့် တာဝန်ယူဆောင်ရွက်ပါက အကောင်းဆုံး ရလဒ်ဆီသို့ ရောက်ရှိနိုင်ပါလိမ့်မည်။"""
        else:
            return """### ⚖️ **Decision-Making & Energetic Alignment**

Rather than a rigid yes or no, the Tarot reveals the energetic forces surrounding your choice:

* **Momentum**: The potential for a rewarding outcome is favorable if aligned with your core values.
* **Balance**: Balance intellectual reasoning with emotional clarity. Trust your inner knowing and take ownership of whichever path you choose."""

    @staticmethod
    def _handle_greeting_query(msg_lower: str, is_myanmar: bool) -> Optional[str]:
        if any(k in msg_lower for k in ["မင်္ဂလာပါ", "ဟဲလို", "နေကောင်းလား", "hello", "hi", "hey", "who are you", "ကျေးဇူး", "thank"]):
            if "ကျေးဇူး" in msg_lower or "thank" in msg_lower:
                return "မင်္ဂလာပါရှင်။ အမြဲကူညီလျက် ရှိပါသည်။ စိတ်နှလုံး အေးချမ်းပျော်ရွှင်ပါစေရှင်။" if is_myanmar else "You are most welcome! May peace and clarity accompany your path."

            if is_myanmar:
                return """### ✨ **မင်္ဂလာပါရှင်! AstroLogic Oracle မှ နွေးထွေးစွာ ကြိုဆိုပါသည်**

ကျွန်ုပ်သည် နက္ခတ်ဗေဒင်နှင့် တားရော့ဗေဒင် အကြံပေး AI ဖြစ်ပါသည်။

အောက်ပါ ကိစ္စရပ်များနှင့် ပတ်သက်၍ စိတ်ကြိုက် ဆွေးနွေးမေးမြန်းနိုင်ပါသည် -
* **တားရော့ကတ်များ၏ သင်္ကေတအဓိပ္ပာယ်** (ဥပမာ - *The Hermit, The Lovers*)
* **ရာသီခွင် ၁၂ မျိုး၏ စရိုက်နှင့် အားသာချက်များ** (ဥပမာ - *မိဿ၊ ကရကဋ်*)
* **ဓာတ်သဘာဝ လိုက်ဖက်ညီမှု** (ဥပမာ - *မီးဓာတ်နှင့် ရေဓာတ် ပေါင်းစပ်မှု*)
* **အချစ်ရေး၊ အလုပ်အကိုင်နှင့် ဘဝလမ်းခွဲ ရွေးချယ်မှုများ**

ယနေ့ သင့်စိတ်ထဲတွင် သိရှိလိုသည်များကို လွတ်လပ်စွာ မျှဝေမေးမြန်းနိုင်ပါသည်ရှင်။"""
            else:
                return """### ✨ **Greetings from the AstroLogic Oracle!**

I am your intuitive astrology and tarot companion. You can explore:
* **Tarot Card Archetypes & Meanings** (e.g., *The Hermit*, *The High Priestess*)
* **Zodiac Personality & Astrological Profiles**
* **Elemental Compatibility & Synergy**
* **Contextual Guidance for Love, Career, and Life Decisions**

What mystical curiosity or question is in your heart today?"""
        return None

    @staticmethod
    def _handle_general_query(
        msg: str,
        zodiac_sign: Optional[str],
        current_reading: Optional[dict],
        is_myanmar: bool
    ) -> str:
        sign_info = ""
        if zodiac_sign and zodiac_sign.lower().strip() in ZODIAC_DATA:
            z = ZODIAC_DATA[zodiac_sign.lower().strip()]
            sign_info = f"\n\nသင်၏ ရာသီခွင်ဖြစ်သော **{z['my']}** ၏ ပင်ကိုဓာတ်စွမ်းအင်အရ: {z['advice_my']}" if is_myanmar else f"\n\nFrom the perspective of your sun sign **{z['en']}**: {z['advice_my']}"

        if is_myanmar:
            return f"""သင်၏ မေးမြန်းချက်ဖြစ်သော *"{msg}"* နှင့် စပ်လျဉ်း၍ တားရော့နှင့် နက္ခတ်ဗေဒင် အမြင်အရ ဆင်ခြင်ရလျှင် -

ဘဝ၏ အပြောင်းအလဲများနှင့် စိန်ခေါ်မှုတိုင်းသည် မိမိကိုယ်ကို ပိုမိုနားလည်သိမြင်လာစေရန် လေ့ကျင့်ပေးသော သင်ခန်းစာများ ဖြစ်ကြပါသည်။ လက်ရှိရင်ဆိုင်နေရသော အခြေအနေကို စိတ်ရှည်တည်ငြိမ်စွာ သုံးသပ်ပြီး၊ အလျင်စလို မဟုတ်ဘဲ အဆင့်ဆင့် ရင်ဆိုင်ကျော်ဖြတ်ရန် ကတ်များက တိုက်တွန်းထားပါသည်။{sign_info}

ထပ်မံ၍ တားရော့ကတ် သို့မဟုတ် ရာသီခွင်ဆိုင်ရာ အသေးစိတ် အချက်အလက်များ သိလိုပါက မေးမြန်းနိုင်ပါသည်ရှင်။"""
        else:
            return f"""Reflecting on your query *"{msg}"* through the symbolic lens of astrology and tarot:

Every moment of questioning brings an opportunity for deeper alignment. The cosmic symbols suggest stepping back to gain perspective, honoring your intuitive feelings, and moving forward with grounded courage.{sign_info}

Feel free to ask about specific tarot cards, zodiac energies, or spreads!"""
