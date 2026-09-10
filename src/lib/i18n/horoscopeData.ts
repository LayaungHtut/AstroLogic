import type { SupportedLocale } from './types';
import { getZodiacTranslation } from './zodiacData';

export const HOROSCOPE_THEMES_MY: Record<string, string> = {
	// Daily themes
	action: 'တက်ကြွသော လှုပ်ရှားမှု',
	courage: 'ရဲရင့်သော သတ္တိ',
	new_beginnings: 'အစပျိုးခြင်း အသစ်များ',
	leadership: 'ဦးဆောင်မှု စွမ်းရည်',
	independence: 'လွတ်လပ်သော ကိုယ်ပိုင်ရပ်တည်မှု',
	stability: 'တည်ငြိမ်ခိုင်မာမှု',
	patience: 'စိတ်ရှည်သည်းခံမှု',
	enjoyment: 'ဘဝ၏ ပျော်ရွှင်ကြည်နူးဖွယ်ရာများ',
	building: 'တည်ဆောက်ဖန်တီးမှု',
	sensuality: 'သဘာဝအလှအပ ခံစားမှု',
	communication: 'ပြောဆိုဆက်ဆံရေး',
	curiosity: 'စူးစမ်းရှာဖွေလိုစိတ်',
	learning: 'ပညာသင်ယူလေ့လာခြင်း',
	socializing: 'မိတ်ဆွေဖွဲ့စည်းခြင်း',
	versatility: 'ဘက်စုံလိုက်လျောညီထွေရှိမှု',
	nurturing: 'နွေးထွေးစွာ ပြုစုစောင့်ရှောက်ခြင်း',
	home: 'မိသားစုနှင့် အိမ်တွင်းအေးချမ်းမှု',
	emotions: 'အတွင်းစိတ် ခံစားချက်များ',
	intuition: 'အလိုလိုသိမြင်သော ဉာဏ်',
	care: 'ဂရုစိုက်ကြင်နာမှု',
	creativity: 'တီထွင်ဖန်တီးမှု စွမ်းအား',
	joy: 'ကြည်နူးရွှင်လန်းမှု',
	self_expression: 'မိမိကိုယ်ကို ထုတ်ဖော်ပြသမှု',
	warmth: 'နွေးထွေးသော စိတ်စေတနာ',
	generosity: 'ရက်ရောစွန့်ကြဲမှု',
	improvement: 'ပိုမိုကောင်းမွန်အောင် ပြုပြင်ခြင်း',
	health: 'ကျန်းမာကြံ့ခိုင်မှု',
	service: 'ကူညီဖေးမ အကျိုးပြုခြင်း',
	organization: 'စနစ်တကျ စီမံခန့်ခွဲမှု',
	detail: 'အသေးစိတ်ဂရုပြုခြင်း',
	balance: 'မျှတမှုနှင့် သဟဇာတ',
	harmony: 'ညီညွတ်မျှတမှု',
	relationships: 'မေတ္တာနှင့် လူမှုဆက်ဆံရေး',
	beauty: 'အလှအပနှင့် သုခချမ်းသာ',
	fairness: 'တရားမျှတမှု',
	transformation: 'ဘဝအသွင် အသစ်သို့ ပြောင်းလဲခြင်း',
	depth: 'နက်နဲသော အသိဉာဏ်',
	passion: 'ပြင်းပြသော စိတ်အားထက်သန်မှု',
	mystery: 'ဆန်းကြယ်သော အတွင်းသဘော',
	intensity: 'အားမာန်ပြည့်ဝသော စွမ်းအင်',
	adventure: 'စွန့်စားရှာဖွေမှု',
	freedom: 'လွတ်လပ်မှု',
	philosophy: 'ဘဝအတွေးအခေါ်နှင့် အမြင်',
	optimism: 'အကောင်းမြင်စိတ်',
	expansion: 'နယ်ပယ်ချဲ့ထွင် တိုးတက်မှု',
	ambition: 'ကြီးမားသော ရည်မှန်းချက်',
	discipline: 'စည်းကမ်းနှင့် ကိုယ်ကျင့်တရား',
	achievement: 'အောင်မြင်မှု ပန်းတိုင်',
	responsibility: 'တာဝန်ယူမှုနှင့် ယုံကြည်စိတ်ချရမှု',
	structure: 'ကျစ်လျစ်ခိုင်မာသော စနစ်',
	innovation: 'ဆန်းသစ်တီထွင်မှု',
	originality: 'မူရင်းကိုယ်ပိုင်ဟန်',
	humanity: 'လူသားချင်း စာနာထောက်ထားမှု',
	vision: 'အနာဂတ်အမြင်နှင့် မျှော်မှန်းချက်',
	spirituality: 'စိတ်ဝိညာဉ် တည်ငြိမ်မှု',
	compassion: 'ကရုဏာနှင့် ကြင်နာမှု',
	imagination: 'စိတ်ကူးစိတ်သန်း ကွန့်မြူးမှု',
	dreams: 'အိပ်မက်နှင့် မျှော်လင့်ချက်များ',

	// Mood-based themes
	celebration: 'အောင်ပွဲခံ အထိမ်းအမှတ်',
	gratitude: 'ကျေးဇူးတင် ကျေနပ်ရောင့်ရဲမှု',
	sharing: 'မျှဝေခံစားခြင်း',
	reflection: 'မိမိကိုယ်ကို ပြန်လည်ဆင်ခြင်ခြင်း',
	meditation: 'တရားရှုမှတ် တည်ငြိမ်ခြင်း',
	peace: 'ငြိမ်းချမ်းအေးမြမှု',
	guidance: 'လမ်းညွှန်မှု ရယူခြင်း',
	clarity: 'ရှင်းလင်းပြတ်သားမှု',
	inner_wisdom: 'အတွင်းစိတ် ဉာဏ်ပညာ',
	relief: 'စိတ်သက်သာရာ ရရှိခြင်း',
	self_care: 'မိမိကိုယ်ကို ဂရုစိုက်စောင့်ရှောက်ခြင်း',
	boundaries: 'သင့်လျော်သော စည်းကန့်သတ်မှု',
	grounding: 'မြေပြင်တွင် အခြေခိုင်တည်ငြိမ်ခြင်း',
	opportunity: 'အခွင့်အလမ်းသစ်များ',
	growth: 'တိုးတက်ကြီးပွားမှု',
	release: 'စွဲလမ်းမှုများကို လက်လွှတ်ဖြေလျှော့ခြင်း',
	perspective: 'ရှုထောင့်သစ်မှ ကြည့်မြင်ခြင်း',
	acceptance: 'လက်ခံနားလည်ခြင်း',
	new_approach: 'နည်းလမ်းသစ်ဖြင့် ချဉ်းကပ်ခြင်း',
	exploration: 'နယ်ပယ်သစ်များ စူးစမ်းရှာဖွေခြင်း',
	discovery: 'အသစ်အဆန်း တွေ့ရှိခြင်း',
	openness: 'ပွင့်လင်းစွာ လက်ခံခြင်း',
	introspection: 'အတွင်းစိတ်ကို စူးစမ်းခြင်း',
	wisdom: 'ပညာဉာဏ်',
	understanding: 'နားလည်သဘောပေါက်ခြင်း',
	awareness: 'သတိတရားနှင့် အသိဉာဏ်',
	presence: 'ပစ္စုပ္ပန်တွင် စိုက်ကပ်တည်ရှိခြင်း',
	appreciation: 'တန်ဖိုးထား မြတ်နိုးခြင်း'
};

export const HOROSCOPE_FOCUS_MY: Record<string, string> = {
	career_bold_moves: 'အလုပ်အကိုင်တွင် ရဲဝံ့ပြတ်သားသော ခြေလှမ်းသစ်များ စတင်ခြင်း',
	creative_expression: 'မိမိ၏ ဖန်တီးမှုစွမ်းရည်နှင့် စိတ်ကူးများကို ထုတ်ဖော်ပြသခြင်း',
	physical_activity: 'ကိုယ်လက်လှုပ်ရှားမှုနှင့် တက်ကြွသော စွမ်းအင်ထိန်းသိမ်းခြင်း',
	financial_planning: 'ငွေကြေးစီမံခန့်ခွဲမှုနှင့် အနာဂတ်အတွက် စုဆောင်းခြင်း',
	health_routines: 'နေ့စဉ်ကျန်းမာရေး အလေ့အထများကို စနစ်တကျ ဂရုစိုက်ခြင်း',
	practical_matters: 'လက်တွေ့ကျသော ဘဝကိစ္စရပ်များကို စေ့စပ်စွာ ဆောင်ရွက်ခြင်း',
	social_connections: 'မိတ်ဆွေအပေါင်းအသင်းများနှင့် ချိတ်ဆက်ဆက်ဆံရေး ခိုင်မာစေခြင်း',
	learning_new_things: 'ဗဟုသုတနှင့် ပညာရပ်အသစ်များကို လေ့လာဆည်းပူးခြင်း',
	communication: 'ရှင်းလင်းပွင့်လင်းသော စကားပြောဆို ဆက်သွယ်မှုများ ပြုလုပ်ခြင်း',
	emotional_reflection: 'စိတ်ခံစားချက်များကို နားလည်ပြီး ပြန်လည်ဆင်ခြင်သုံးသပ်ခြင်း',
	relationships: 'ချစ်ရသူများနှင့် ရင်းနှီးနွေးထွေးသော ဆက်ဆံရေး တည်ဆောက်ခြင်း',
	spiritual_practice: 'စိတ်ဝိညာဉ် တည်ငြိမ်အေးချမ်းစေမည့် အလေ့အကျင့်များ ပြုလုပ်ခြင်း'
};

export function translateHoroscopeTheme(
	theme: string | undefined | null,
	locale: SupportedLocale
): string {
	if (!theme) return '';
	if (locale !== 'my') {
		return theme.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());
	}
	const clean = theme.toLowerCase().trim().replace(/ /g, '_');
	if (HOROSCOPE_THEMES_MY[clean]) {
		return HOROSCOPE_THEMES_MY[clean];
	}
	const noUnderscore = clean.replace(/_/g, '');
	for (const [k, v] of Object.entries(HOROSCOPE_THEMES_MY)) {
		if (k.replace(/_/g, '') === noUnderscore) return v;
	}
	return theme.replace(/_/g, ' ');
}

export function translateHoroscopeFocus(
	focus: string | undefined | null,
	locale: SupportedLocale
): string {
	if (!focus) return '';
	if (locale !== 'my') return focus.replace(/_/g, ' ');
	const clean = focus.toLowerCase().trim().replace(/ /g, '_');
	return HOROSCOPE_FOCUS_MY[clean] || focus.replace(/_/g, ' ');
}

export function formatHoroscopeGuidance(
	guidance: string | undefined | null,
	sign: string,
	theme: string,
	mood: string,
	locale: SupportedLocale
): string {
	if (!guidance) return '';
	if (locale !== 'my') return guidance;

	if (/[\u1000-\u109F]/.test(guidance)) {
		return guidance;
	}

	const signMy = getZodiacTranslation(sign, 'my').name || sign;
	const themeMy = translateHoroscopeTheme(theme, 'my');

	return `ယနေ့သည် ${signMy} ဖွားများအတွက် ${themeMy} ကို အထူးအလေးထားရမည့် နေ့တစ်နေ့ဖြစ်ပါသည်။ သင်၏ စိတ်ခံစားချက်နှင့် သဘာဝစွမ်းအင်များကို သဟဇာတဖြစ်အောင် ညှိယူပြီး တစ်နေ့တာ လုပ်ငန်းဆောင်တာများကို အေးချမ်းတည်ငြိမ်စွာ ဖြတ်သန်းပါ။`;
}

export function formatHoroscopeReflection(
	reflection: string | undefined | null,
	theme: string,
	locale: SupportedLocale
): string {
	if (!reflection) return '';
	if (locale !== 'my') return reflection;

	if (/[\u1000-\u109F]/.test(reflection)) {
		return reflection;
	}

	const themeMy = translateHoroscopeTheme(theme, 'my');
	return `ယနေ့တွင် ${themeMy} နှင့် ပတ်သက်၍ သင်၏ နေ့စဉ်ဘဝတွင် မည်သို့ လက်တွေ့ကျင့်သုံး နားလည်နိုင်မည်ကို မိမိကိုယ်ကို ပြန်လည်ဆင်ခြင်သုံးသပ်ကြည့်ပါ။`;
}

export function formatHoroscopeOpportunity(
	opportunity: string | undefined | null,
	theme: string,
	locale: SupportedLocale
): string {
	if (!opportunity) return '';
	if (locale !== 'my') return opportunity;

	if (/[\u1000-\u109F]/.test(opportunity)) {
		return opportunity;
	}

	const themeMy = translateHoroscopeTheme(theme, 'my');
	return `${themeMy} စွမ်းအင်များနှင့် ထပ်တူကျသော အခွင့်အလမ်းကောင်းများသည် ယနေ့တွင် သင့်ထံသို့ ရောက်ရှိလာနိုင်ပါသည်။ မိမိ၏ အာရုံစူးစိုက်မှုကို မြှင့်တင်ထားပါ။`;
}

export function formatHoroscopeCaution(
	caution: string | undefined | null,
	theme: string,
	element: string,
	locale: SupportedLocale
): string {
	if (!caution) return '';
	if (locale !== 'my') return caution;

	if (/[\u1000-\u109F]/.test(caution)) {
		return caution;
	}

	const themeMy = translateHoroscopeTheme(theme, 'my');
	return `${themeMy} ကို ဆောင်ရွက်ရာတွင် အလွန်အမင်း စိတ်လောကြီးခြင်း သို့မဟုတ် လျစ်လျူရှုခြင်းတို့ မဖြစ်စေရန် သတိပြုထိန်းကျောင်းပါ။`;
}

export const PROLOG_TRACE_RESULTS_MY: Record<string, string> = {
	'User zodiac sign identified': 'အသုံးပြုသူ၏ ရာသီခွင်ကို သတ်မှတ်ဆန်းစစ်ပြီးဖြစ်သည်',
	'Element association determined': 'ရာသီခွင်နှင့် သက်ဆိုင်သော ဓာတ်သဘော စွမ်းအင်ကို အတည်ပြုပြီးသည်',
	'Modality determined': 'ရာသီခွင်၏ လှုပ်ရှားသဘာဝ (Modality) ကို ဖော်ထုတ်ပြီးသည်',
	'Daily theme selected': 'ယနေ့အတွက် အဓိက စွမ်းအင်ဆောင်ပုဒ်ကို ရွေးချယ်ပြီးသည်',
	'Mood-based theme determined':
		'လက်ရှိစိတ်ခံစားချက်အပေါ် မူတည်သော ဆက်စပ်သဘောတရားကို သတ်မှတ်ပြီးသည်',
	'Focus area identified': 'ယနေ့ အထူးဂရုပြုဆောင်ရွက်ရမည့် နယ်ပယ်ကို သတ်မှတ်ပြီးသည်',
	'Question category matched': 'မေးခွန်း၏ ကဏ္ဍနှင့် သဘောသဘာဝကို ဆန်းစစ်အတည်ပြုပြီးသည်',
	'Recommended spread determined': 'အသင့်တော်ဆုံး တားရော့ကတ်ခင်းကျင်းပုံကို ရွေးချယ်ပြီးသည်',
	'Dominant theme identified':
		'ကတ်များအနက် အဓိကလွှမ်းမိုးနေသော စွမ်းအင်သဘောတရားကို ဖော်ထုတ်ပြီးသည်',
	'Advice generated': 'ရာသီခွင်နှင့် ကတ်များအပေါ် အခြေပြု၍ အကြံပြုချက် ရေးဆွဲပြီးသည်',
	'Compatibility score calculated': 'ရာသီခွင်နှစ်ခုအကြား လိုက်ဖက်ညီမှု ရမှတ်ကို တွက်ချက်ပြီးသည်'
};

export function formatTraceResult(
	result: string | undefined | null,
	locale: SupportedLocale
): string {
	if (!result) return '';
	if (locale !== 'my') return result;
	return PROLOG_TRACE_RESULTS_MY[result] || result;
}
