import type { ZodiacSignTranslation, SupportedLocale } from './types';

export const ZODIAC_SIGNS_DATA: Record<string, ZodiacSignTranslation> = {
	aries: {
		signEn: 'Aries',
		signMy: 'မိဿရာသီ',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		modalityEn: 'Cardinal',
		modalityMy: 'အစပျိုး (Cardinal)',
		rulerEn: 'Mars',
		rulerMy: 'အင်္ဂါဂြိုဟ်',
		traitsEn: ['Bold', 'Ambitious', 'Pioneering', 'Energetic', 'Passionate', 'Direct'],
		traitsMy: [
			'ရဲရင့်ပြတ်သားသူ',
			'ရည်မှန်းချက်ကြီးသူ',
			'ရှေ့ဆောင်လမ်းပြ',
			'တက်ကြွဖျတ်လတ်သူ',
			'စိတ်အားထက်သန်သူ',
			'ပွင့်လင်းရိုးသားသူ'
		],
		dateRangeEn: 'March 21 - April 19',
		dateRangeMy: 'မတ် ၂၁ - ဧပြီ ၁၉',
		summaryEn:
			'Pioneering fire sign driven by passion, direct courage, and an unstoppable desire to initiate new adventures.',
		summaryMy:
			'မီးဓာတ်စွမ်းအင်ရှင် မိဿရာသီဖွားများသည် ရဲရင့်ပြတ်သားပြီး ရှေ့ဆောင်လမ်းပြအစပြုလိုစိတ် ပြင်းပြသူများဖြစ်ကြသည်။'
	},
	taurus: {
		signEn: 'Taurus',
		signMy: 'ပြိဿရာသီ',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		modalityEn: 'Fixed',
		modalityMy: 'တည်ငြိမ် (Fixed)',
		rulerEn: 'Venus',
		rulerMy: 'သောကြာဂြိုဟ်',
		traitsEn: ['Grounded', 'Patient', 'Reliable', 'Sensual', 'Devoted', 'Determined'],
		traitsMy: [
			'တည်ငြိမ်အေးဆေးသူ',
			'စိတ်ရှည်သည်းခံသူ',
			'ယုံကြည်အားထားရသူ',
			'အလှအပနှင့်ဇိမ်ခံမှုကိုမြတ်နိုးသူ',
			'သစ္စာရှိသူ',
			'ဇွဲရှိသူ'
		],
		dateRangeEn: 'April 20 - May 20',
		dateRangeMy: 'ဧပြီ ၂၀ - မေ ၂၀',
		summaryEn:
			'Grounded earth sign embodying patience, exquisite taste, practical loyalty, and enduring stability.',
		summaryMy:
			'မြေဓာတ်စွမ်းအင်ရှင် ပြိဿရာသီဖွားများသည် စိတ်ရှည်တည်ငြိမ်ပြီး သစ္စာရှိကာ အလှအပနှင့် လုံခြုံစိတ်ချရမှုကို မြတ်နိုးကြသည်။'
	},
	gemini: {
		signEn: 'Gemini',
		signMy: 'မေထုန်ရာသီ',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		modalityEn: 'Mutable',
		modalityMy: 'ပြောင်းလဲလွယ် (Mutable)',
		rulerEn: 'Mercury',
		rulerMy: 'ဗုဒ္ဓဟူးဂြိုဟ်',
		traitsEn: ['Curious', 'Adaptable', 'Witty', 'Expressive', 'Versatile', 'Intellectual'],
		traitsMy: [
			'စူးစမ်းလိုစိတ်ရှိသူ',
			'လိုက်လျောညီထွေနေတတ်သူ',
			'ဉာဏ်ရည်ထက်မြက်သူ',
			'ပြောဆိုဆက်ဆံရေးကောင်းသူ',
			'ဗဟုသုတကြွယ်ဝသူ'
		],
		dateRangeEn: 'May 21 - June 20',
		dateRangeMy: 'မေ ၂၁ - ဇွန် ၂၀',
		summaryEn:
			'Versatile air sign governed by intellect, lively wit, endless curiosity, and multifaceted storytelling.',
		summaryMy:
			'လေဓာတ်စွမ်းအင်ရှင် မေထုန်ရာသီဖွားများသည် ဉာဏ်ရည်ထက်မြက်ပြီး လိုက်လျောညီထွေရှိကာ စူးစမ်းရှာဖွေလိုစိတ် ပြင်းပြကြသည်။'
	},
	cancer: {
		signEn: 'Cancer',
		signMy: 'ကရကဋ်ရာသီ',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		modalityEn: 'Cardinal',
		modalityMy: 'အစပျိုး (Cardinal)',
		rulerEn: 'Moon',
		rulerMy: 'လမင်း',
		traitsEn: ['Intuitive', 'Nurturing', 'Protective', 'Empathetic', 'Loyal', 'Sentimental'],
		traitsMy: [
			'အတွင်းစိတ်အာရုံသိသူ',
			'နွေးထွေးဂရုစိုက်တတ်သူ',
			'ကာကွယ်စောင့်ရှောက်သူ',
			'စာနာနားလည်တတ်သူ',
			'မေတ္တာကြီးမားသူ'
		],
		dateRangeEn: 'June 21 - July 22',
		dateRangeMy: 'ဇွန် ၂၁ - ဇူလိုင် ၂၂',
		summaryEn:
			'Nurturing water sign with profound intuition, protective domestic warmth, and a loyal, sensitive heart.',
		summaryMy:
			'ရေဓာတ်စွမ်းအင်ရှင် ကရကဋ်ရာသီဖွားများသည် နူးညံ့သိမ်မွေ့သော မေတ္တာရှင်များဖြစ်ပြီး မိသားစုနှင့် ချစ်ရသူများကို အလွန်ကာကွယ်စောင့်ရှောက်တတ်ကြသည်။'
	},
	leo: {
		signEn: 'Leo',
		signMy: 'သိဟ်ရာသီ',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		modalityEn: 'Fixed',
		modalityMy: 'တည်ငြိမ် (Fixed)',
		rulerEn: 'Sun',
		rulerMy: 'နေမင်း',
		traitsEn: ['Radiant', 'Generous', 'Charismatic', 'Confident', 'Warm-hearted', 'Leader'],
		traitsMy: [
			'တောက်ပသောဩဇာရှိသူ',
			'ရက်ရောစွန့်ကြဲသူ',
			'ဆွဲဆောင်မှုရှိသူ',
			'ကိုယ့်ကိုယ်ကိုယုံကြည်မှုပြည့်ဝသူ',
			'ခေါင်းဆောင်မွေးရာပါ'
		],
		dateRangeEn: 'July 23 - August 22',
		dateRangeMy: 'ဇူလိုင် ၂၃ - ဩဂုတ် ၂၂',
		summaryEn:
			'Radiant fire sign shining with natural majesty, generous warmth, dramatic flair, and loyal leadership.',
		summaryMy:
			'မီးဓာတ်စွမ်းအင်ရှင် သိဟ်ရာသီဖွားများသည် မွေးရာပါခေါင်းဆောင်အရည်အသွေးရှိပြီး ရက်ရောသော စိတ်ထားနှင့် တောက်ပသော ဩဇာတိက္ကမကို ပိုင်ဆိုင်ကြသည်။'
	},
	virgo: {
		signEn: 'Virgo',
		signMy: 'ကန်ရာသီ',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		modalityEn: 'Mutable',
		modalityMy: 'ပြောင်းလဲလွယ် (Mutable)',
		rulerEn: 'Mercury',
		rulerMy: 'ဗုဒ္ဓဟူးဂြိုဟ်',
		traitsEn: ['Analytical', 'Meticulous', 'Helpful', 'Practical', 'Refined', 'Discerning'],
		traitsMy: [
			'စနစ်တကျဆန်းစစ်တတ်သူ',
			'အသေးစိတ်ဂရုပြုသူ',
			'ကူညီလိုစိတ်ပြည့်ဝသူ',
			'လက်တွေ့ကျသူ',
			'စေ့စပ်သေချာသူ'
		],
		dateRangeEn: 'August 23 - September 22',
		dateRangeMy: 'ဩဂုတ် ၂၃ - စက်တင်ဘာ ၂၂',
		summaryEn:
			'Meticulous earth sign dedicated to service, elegant refinement, analytical clarity, and healing craftsmanship.',
		summaryMy:
			'မြေဓာတ်စွမ်းအင်ရှင် ကန်ရာသီဖွားများသည် စနစ်တကျ အသေးစိတ်ကျနစွာ တွေးခေါ်လုပ်ကိုင်တတ်ပြီး အခြားသူများကို ကူညီဖေးမလိုစိတ် မြင့်မားကြသည်။'
	},
	libra: {
		signEn: 'Libra',
		signMy: 'တူရာသီ',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		modalityEn: 'Cardinal',
		modalityMy: 'အစပျိုး (Cardinal)',
		rulerEn: 'Venus',
		rulerMy: 'သောကြာဂြိုဟ်',
		traitsEn: ['Diplomatic', 'Charming', 'Fair-minded', 'Harmonious', 'Artistic', 'Social'],
		traitsMy: [
			'လိမ္မာပါးနပ်သောသံတမန်',
			'ဆွဲဆောင်မှုရှိသူ',
			'တရားမျှတသူ',
			'သဟဇာတဖြစ်မှုကိုမြတ်နိုးသူ',
			'အနုပညာစိတ်ရှိသူ'
		],
		dateRangeEn: 'September 23 - October 22',
		dateRangeMy: 'စက်တင်ဘာ ၂၃ - အောက်တိုဘာ ၂၂',
		summaryEn:
			'Harmonious air sign dedicated to aesthetic balance, graceful diplomacy, partnership, and fair justice.',
		summaryMy:
			'လေဓာတ်စွမ်းအင်ရှင် တူရာသီဖွားများသည် သဟဇာတဖြစ်မှုနှင့် တရားမျှတမှုကို တန်ဖိုးထားပြီး ဆွဲဆောင်မှုရှိသော ဆက်ဆံရေးပညာရှင်များ ဖြစ်ကြသည်။'
	},
	scorpio: {
		signEn: 'Scorpio',
		signMy: 'ဗြိစ္ဆာရာသီ',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		modalityEn: 'Fixed',
		modalityMy: 'တည်ငြိမ် (Fixed)',
		rulerEn: 'Pluto / Mars',
		rulerMy: 'ပလူတိုနှင့် အင်္ဂါဂြိုဟ်',
		traitsEn: ['Intense', 'Passionate', 'Intuitive', 'Magnetic', 'Transformative', 'Strategic'],
		traitsMy: [
			'နက်နဲခိုင်မာသူ',
			'စိတ်ထက်သန်သူ',
			'ဆဋ္ဌမအာရုံထက်မြက်သူ',
			'သံလိုက်ဓာတ်ကဲ့သို့ဆွဲဆောင်မှုရှိသူ',
			'လျှို့ဝှက်ချက်ထိန်းနိုင်သူ'
		],
		dateRangeEn: 'October 23 - November 21',
		dateRangeMy: 'အောက်တိုဘာ ၂၃ - နိုဝင်ဘာ ၂၁',
		summaryEn:
			'Intensely perceptive water sign wielding transformative depth, psychological insight, and unshakable willpower.',
		summaryMy:
			'ရေဓာတ်စွမ်းအင်ရှင် ဗြိစ္ဆာရာသီဖွားများသည် အလွန်နက်နဲပြီး ထိုးထွင်းသိမြင်နိုင်စွမ်းနှင့် စိတ်ဓာတ်ကြံ့ခိုင်မှု အပြည့်ရှိကြသည်။'
	},
	sagittarius: {
		signEn: 'Sagittarius',
		signMy: 'ဓနုရာသီ',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		modalityEn: 'Mutable',
		modalityMy: 'ပြောင်းလဲလွယ် (Mutable)',
		rulerEn: 'Jupiter',
		rulerMy: 'ကြာသပတေးဂြိုဟ်',
		traitsEn: ['Adventurous', 'Philosophical', 'Optimistic', 'Free-spirited', 'Generous', 'Direct'],
		traitsMy: [
			'စွန့်စားခရီးသွားမြတ်နိုးသူ',
			'ဒဿနအမြင်ရှိသူ',
			'အကောင်းမြင်ဝါဒီ',
			'လွတ်လပ်မှုကိုတန်ဖိုးထားသူ',
			'ရက်ရောဖြောင့်မတ်သူ'
		],
		dateRangeEn: 'November 22 - December 21',
		dateRangeMy: 'နိုဝင်ဘာ ၂၂ - ဒီဇင်ဘာ ၂၁',
		summaryEn:
			'Adventurous fire sign questing for truth, expansive knowledge, philosophical humor, and boundless horizons.',
		summaryMy:
			'မီးဓာတ်စွမ်းအင်ရှင် ဓနုရာသီဖွားများသည် လွတ်လပ်မှုနှင့် အမှန်တရားကို ရှာဖွေသူများဖြစ်ပြီး ဘဝကို အကောင်းမြင်စိတ်ဖြင့် စွန့်စားဖြတ်သန်းကြသည်။'
	},
	capricorn: {
		signEn: 'Capricorn',
		signMy: 'မကာရရာသီ',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		modalityEn: 'Cardinal',
		modalityMy: 'အစပျိုး (Cardinal)',
		rulerEn: 'Saturn',
		rulerMy: 'စနေဂြိုဟ်',
		traitsEn: ['Disciplined', 'Ambitious', 'Strategic', 'Persistent', 'Responsible', 'Patient'],
		traitsMy: [
			'စည်းကမ်းပြည့်ဝသူ',
			'ရည်မှန်းချက်ကြီးမားသူ',
			'ဗျူဟာကျကျစီမံသူ',
			'ဇွဲလုံ့လကြီးမားသူ',
			'တာဝန်သိတတ်သူ'
		],
		dateRangeEn: 'December 22 - January 19',
		dateRangeMy: 'ဒီဇင်ဘာ ၂၂ - ဇန်နဝါရီ ၁၉',
		summaryEn:
			'Disciplined earth sign climbing steadily toward mastery, enduring legacy, pragmatic leadership, and duty.',
		summaryMy:
			'မြေဓာတ်စွမ်းအင်ရှင် မကာရရာသီဖွားများသည် စည်းကမ်းကြီးမားပြီး ဇွဲရှိကာ ရည်မှန်းချက်ပန်းတိုင်ကို မရောက်မချင်း မဆုတ်မနစ် ကြိုးစားတတ်ကြသည်။'
	},
	aquarius: {
		signEn: 'Aquarius',
		signMy: 'ကုမ်ရာသီ',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		modalityEn: 'Fixed',
		modalityMy: 'တည်ငြိမ် (Fixed)',
		rulerEn: 'Uranus / Saturn',
		rulerMy: 'ယူရေးနပ်စ်နှင့် စနေဂြိုဟ်',
		traitsEn: [
			'Visionary',
			'Original',
			'Humanitarian',
			'Independent',
			'Inventive',
			'Unconventional'
		],
		traitsMy: [
			'အမြော်အမြင်ကြီးမားသူ',
			'ထူးခြားဆန်းသစ်သူ',
			'လူသားချင်းစာနာသူ',
			'လွတ်လပ်စွာတွေးခေါ်သူ',
			'တီထွင်ဆန်းသစ်သူ'
		],
		dateRangeEn: 'January 20 - February 18',
		dateRangeMy: 'ဇန်နဝါရီ ၂၀ - ဖေဖော်ဝါရီ ၁၈',
		summaryEn:
			'Visionary air sign pioneering humanitarian progress, unconventional innovation, and egalitarian brotherhood.',
		summaryMy:
			'လေဓာတ်စွမ်းအင်ရှင် ကုမ်ရာသီဖွားများသည် ခေတ်ရှေ့ပြေးသော အတွေးအခေါ်ပိုင်ရှင်များဖြစ်ပြီး လူသားအားလုံးကောင်းကျိုးအတွက် ဆန်းသစ်တီထွင်လိုကြသည်။'
	},
	pisces: {
		signEn: 'Pisces',
		signMy: 'မိန်ရာသီ',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		modalityEn: 'Mutable',
		modalityMy: 'ပြောင်းလဲလွယ် (Mutable)',
		rulerEn: 'Neptune / Jupiter',
		rulerMy: 'နက်ပကျွန်းနှင့် ကြာသပတေးဂြိုဟ်',
		traitsEn: ['Imaginative', 'Compassionate', 'Spiritual', 'Artistic', 'Empathetic', 'Dreamy'],
		traitsMy: [
			'စိတ်ကူးဉာဏ်ကြွယ်ဝသူ',
			'ကရုဏာကြီးမားသူ',
			'ဝိညာဉ်ရေးရာနက်နဲသူ',
			'အနုပညာပါရမီပါသူ',
			'နူးညံ့သိမ်မွေ့သူ'
		],
		dateRangeEn: 'February 19 - March 20',
		dateRangeMy: 'ဖေဖော်ဝါရီ ၁၉ - မတ် ၂၀',
		summaryEn:
			'Mystical water sign swimming between physical reality and spiritual ocean, abundant with creative empathy.',
		summaryMy:
			'ရေဓာတ်စွမ်းအင်ရှင် မိန်ရာသီဖွားများသည် အလွန်နူးညံ့သိမ်မွေ့ပြီး အနုပညာနှင့် ဝိညာဉ်ရေးရာတွင် ထူးချွန်ကာ ကရုဏာစိတ် အလွန်ကြီးမားကြသည်။'
	}
};

export const ELEMENTS_DATA: Record<string, { en: string; my: string }> = {
	fire: { en: 'Fire', my: 'မီးဓာတ်' },
	earth: { en: 'Earth', my: 'မြေဓာတ်' },
	air: { en: 'Air', my: 'လေဓာတ်' },
	water: { en: 'Water', my: 'ရေဓာတ်' },
	spirit: { en: 'Spirit', my: 'ဝိညာဉ်ဓာတ်' }
};

export const MODALITIES_DATA: Record<string, { en: string; my: string }> = {
	cardinal: { en: 'Cardinal', my: 'အစပျိုး (Cardinal)' },
	fixed: { en: 'Fixed', my: 'တည်ငြိမ် (Fixed)' },
	mutable: { en: 'Mutable', my: 'ပြောင်းလဲလွယ် (Mutable)' }
};

export const PLANETS_DATA: Record<string, { en: string; my: string }> = {
	sun: { en: 'Sun', my: 'နေမင်း' },
	moon: { en: 'Moon', my: 'လမင်း' },
	mercury: { en: 'Mercury', my: 'ဗုဒ္ဓဟူးဂြိုဟ်' },
	venus: { en: 'Venus', my: 'သောကြာဂြိုဟ်' },
	mars: { en: 'Mars', my: 'အင်္ဂါဂြိုဟ်' },
	jupiter: { en: 'Jupiter', my: 'ကြာသပတေးဂြိုဟ်' },
	saturn: { en: 'Saturn', my: 'စနေဂြိုဟ်' },
	uranus: { en: 'Uranus', my: 'ယူရေးနပ်စ်ဂြိုဟ်' },
	neptune: { en: 'Neptune', my: 'နက်ပကျွန်းဂြိုဟ်' },
	pluto: { en: 'Pluto', my: 'ပလူတိုဂြိုဟ်' }
};

export function getZodiacTranslation(
	sign: string,
	locale: SupportedLocale
): {
	name: string;
	element: string;
	modality: string;
	ruler: string;
	traits: string[];
	dateRange: string;
	summary: string;
} {
	const key = (sign || '').toLowerCase().trim();
	const data = ZODIAC_SIGNS_DATA[key];
	if (!data) {
		return {
			name: sign,
			element: '',
			modality: '',
			ruler: '',
			traits: [],
			dateRange: '',
			summary: ''
		};
	}

	if (locale === 'my') {
		return {
			name: data.signMy,
			element: data.elementMy,
			modality: data.modalityMy,
			ruler: data.rulerMy,
			traits: data.traitsMy,
			dateRange: data.dateRangeMy,
			summary: data.summaryMy
		};
	}

	return {
		name: data.signEn,
		element: data.elementEn,
		modality: data.modalityEn,
		ruler: data.rulerEn,
		traits: data.traitsEn,
		dateRange: data.dateRangeEn,
		summary: data.summaryEn
	};
}

export function formatElement(element: string | undefined | null, locale: SupportedLocale): string {
	if (!element) return '';
	const key = element.toLowerCase().trim();
	return (locale === 'my' ? ELEMENTS_DATA[key]?.my : ELEMENTS_DATA[key]?.en) || element;
}

export function formatModality(
	modality: string | undefined | null,
	locale: SupportedLocale
): string {
	if (!modality) return '';
	const key = modality.toLowerCase().trim();
	return (locale === 'my' ? MODALITIES_DATA[key]?.my : MODALITIES_DATA[key]?.en) || modality;
}

export function formatPlanet(planet: string | undefined | null, locale: SupportedLocale): string {
	if (!planet) return '';
	const key = planet.toLowerCase().trim();
	return (locale === 'my' ? PLANETS_DATA[key]?.my : PLANETS_DATA[key]?.en) || planet;
}

export const ELEMENT_PERSONALITIES_MY: Record<string, string> = {
	fire: 'စိတ်အားထက်သန်ခြင်း၊ တက်ကြွလှုပ်ရှားခြင်းနှင့် ပင်ကိုဗီဇအရ ဦးဆောင်နိုင်စွမ်းရှိခြင်း။ မီးဓာတ်စွမ်းအင်ရှင်များသည် စိတ်အားထက်သန်မှုနှင့် ရဲရင့်ပြတ်သားမှုတို့ဖြင့် ဆုံးဖြတ်လှုပ်ရှားတတ်ကြသည်။',
	earth:
		'တည်ကြည်ခိုင်မြဲခြင်း၊ လက်တွေ့ကျခြင်းနှင့် အားကိုးထိုက်ခြင်း။ မြေဓာတ်စွမ်းအင်ရှင်များသည် တည်ငြိမ်မှု၊ လုံခြုံမှုနှင့် မြင်သာထင်သာရှိသော ရလဒ်များကို အဓိကထား၍ စိတ်ရှည်ဇွဲရှိစွာ ကြိုးပမ်းလေ့ရှိကြသည်။',
	air: 'ဉာဏ်ရည်ဉာဏ်သွေး ထက်မြက်ခြင်း၊ ဆက်ဆံရေးကောင်းမွန်ခြင်းနှင့် ပေါင်းသင်းဆက်ဆံမှုလွယ်ကူခြင်း။ လေဓာတ်စွမ်းအင်ရှင်များသည် အတွေးအခေါ်သစ်များ၊ စူးစမ်းရှာဖွေမှုများနှင့် အသိပညာဖလှယ်ခြင်းကို နှစ်သက်ကြသည်။',
	water:
		'အလိုလိုသိစိတ်စူးရှခြင်း၊ စိတ်ခံစားမှုနက်နဲခြင်းနှင့် ကရုဏာကြီးမားခြင်း။ ရေဓာတ်စွမ်းအင်ရှင်များသည် စာနာနားလည်နိုင်စွမ်း မြင့်မားပြီး မိမိတို့၏ အတွင်းစိတ်ခံစားချက်နှင့် စိတ်ကူးဉာဏ်ဖြင့် ဘဝကို ဖြတ်သန်းကြသည်။'
};

export const MODALITY_APPROACHES_MY: Record<string, string> = {
	cardinal:
		'အစပျိုးဦးဆောင်ခြင်းနှင့် လမ်းသစ်ဖောက်ခြင်း။ အစပျိုး (Cardinal) ရာသီဖွားများသည် လုပ်ငန်းသစ်များနှင့် အခွင့်အလမ်းများကို စတင်အကောင်အထည်ဖော်တတ်သော ပင်ကိုခေါင်းဆောင်များ ဖြစ်ကြသည်။',
	fixed:
		'တည်ငြိမ်ခိုင်ခံ့စေခြင်းနှင့် ထိန်းသိမ်းစောင့်ရှောက်ခြင်း။ တည်ငြိမ် (Fixed) ရာသီဖွားများသည် ခိုင်မာသော သန္နိဋ္ဌာန်၊ ဇွဲလုံ့လတို့ဖြင့် စတင်ထားသောအရာများကို အောင်မြင်စွာ တည်ဆောက်ထိန်းသိမ်းလေ့ရှိကြသည်။',
	mutable:
		'အခြေအနေနှင့်အညီ လိုက်လျောညီထွေ ပြောင်းလဲနိုင်ခြင်း။ ပြောင်းလဲလွယ် (Mutable) ရာသီဖွားများသည် ပျော့ပျောင်းညင်သာပြီး ပြောင်းလဲမှုများကို အဆင်ပြေစွာ လက်ခံကာ အဆင့်ဆင့်ကူးပြောင်းမှုကို ချောမွေ့စေသည်။'
};

export const PLANETARY_INFLUENCES_MY: Record<string, string> = {
	mars: 'အင်္ဂါဂြိုဟ်သည် စွမ်းအင်၊ ရဲရင့်ပြတ်သားမှုနှင့် တိုက်ခိုက်လိုစိတ်တို့ကို ဆောင်ကြဉ်းပေးသည်။ ရဲရင့်သော စစ်သည်တော်စိတ်ဓာတ်ကို ပေးစွမ်းသော်လည်း စိတ်မြန်လက်မြန်ဖြစ်မှုကို သတိပြုသင့်သည်။',
	venus:
		'သောကြာဂြိုဟ်သည် ချစ်ခြင်းမေတ္တာ၊ အလှအပနှင့် သဟဇာတဖြစ်မှုကို ယူဆောင်ပေးသည်။ ဆွဲဆောင်မှုရှိခြင်းနှင့် အနုပညာအမြင်ကို ပေးစွမ်းသော်လည်း အလိုလိုက်လွန်းမှုကို ဆင်ခြင်သင့်သည်။',
	mercury:
		'ဗုဒ္ဓဟူးဂြိုဟ်သည် ဆက်သွယ်ပြောဆိုမှု၊ ထက်မြက်သော ဉာဏ်ရည်နှင့် လျင်မြန်စွာ လိုက်လျောညီထွေဖြစ်မှုကို ပေးသည်။ စူးစမ်းလိုစိတ်နှင့် လျင်မြန်စွာ စဉ်းစားနိုင်စွမ်းကို ဖြစ်ပေါ်စေသည်။',
	moon: 'လမင်းသည် အလိုလိုသိစိတ်၊ နက်နဲသော စိတ်ခံစားချက်နှင့် ကြင်နာယုယမှုကို ယူဆောင်ပေးသည်။ စာနာနားလည်နိုင်စွမ်းနှင့် နူးညံ့သိမ်မွေ့မှုကို တိုးပွားစေသော်လည်း စိတ်အပြောင်းအလဲမြန်မှုကို သတိပြုရမည်။',
	sun: 'နေမင်းသည် အသက်စွမ်းအား၊ ကိုယ့်ကိုယ်ကိုယ်ယုံကြည်မှုနှင့် ခေါင်းဆောင်မှုစွမ်းရည်ကို ပေးစွမ်းသည်။ နွေးထွေးမှုနှင့် တီထွင်ဖန်တီးမှုကို ဖြစ်ထွန်းစေသည်။',
	pluto:
		'ပလူတိုဂြိုဟ်သည် ဘဝအသွင်ပြောင်းလဲခြင်း၊ နက်ရှိုင်းသော စွမ်းအားနှင့် လျှို့ဝှက်ဆန်းကြယ်မှုကို ဆောင်ကြဉ်းပေးသည်။ စိတ်ပိုင်းဖြတ်မှုနှင့် ခံနိုင်ရည်စွမ်းအားကို မြှင့်တင်ပေးသည်။',
	jupiter:
		'ကြာသပတေးဂြိုဟ်သည် တိုးတက်ကြီးပွားခြင်း၊ အကောင်းမြင်ဝါဒနှင့် ဉာဏ်ပညာတို့ကို ဖြည့်ဆည်းပေးသည်။ ရက်ရောမှုနှင့် ဒဿနဆန်သော အမြင်ကျယ်မှုကို ဖြစ်ထွန်းစေသည်။',
	saturn:
		'စနေဂြိုဟ်သည် စည်းကမ်းရှိမှု၊ တည်ဆောက်ဖွဲ့စည်းမှုနှင့် တာဝန်ယူစိတ်တို့ကို သွန်သင်ပေးသည်။ ရင့်ကျက်မှုနှင့် ခိုင်မာသော ရည်မှန်းချက်ပန်းတိုင်ကို ဦးတည်စေသည်။',
	uranus:
		'ယူရေးနပ်စ်ဂြိုဟ်သည် ဆန်းသစ်တီထွင်မှု၊ လွတ်လပ်မှုနှင့် ရိုးရာမဆန်သော အတွေးအမြင်များကို လှုံ့ဆော်ပေးသည်။ မူပိုင်ဆန်းသစ်သော ပါရမီကို ထင်ရှားစေသည်။',
	neptune:
		'နက်ပကျွန်းဂြိုဟ်သည် စိတ်ကူးဉာဏ်ကွန့်မြူးမှု၊ အနုပညာခံစားမှုနှင့် ဝိညာဉ်ရေးရာနက်နဲမှုကို ဆောင်ကြဉ်းပေးသည်။ အိပ်မက်များနှင့် ကရုဏာတရားကို အလင်းပေးသည်။'
};

export function formatPersonalityStyle(
	style: string | undefined | null,
	element: string | undefined | null,
	locale: SupportedLocale
): string {
	if (locale !== 'my') return style || '';
	const elKey = (element || '').toLowerCase().trim();
	return ELEMENT_PERSONALITIES_MY[elKey] || style || '';
}

export function formatApproachToLife(
	approach: string | undefined | null,
	modality: string | undefined | null,
	locale: SupportedLocale
): string {
	if (locale !== 'my') return approach || '';
	const modKey = (modality || '').toLowerCase().trim();
	return MODALITY_APPROACHES_MY[modKey] || approach || '';
}

export function formatPlanetaryInfluence(
	influence: string | undefined | null,
	planet: string | undefined | null,
	locale: SupportedLocale
): string {
	if (locale !== 'my') return influence || '';
	const pKey = (planet || '').toLowerCase().trim();
	return PLANETARY_INFLUENCES_MY[pKey] || influence || '';
}
