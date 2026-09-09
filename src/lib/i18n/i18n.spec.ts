import { describe, it, expect } from 'vitest';
import {
	locale,
	translate,
	getCardTranslation,
	translatePosition,
	translateSpreadType,
	translateTopic,
	getZodiacTranslation,
	formatElement,
	formatModality,
	formatPlanet,
	TAROT_CARDS_DATA,
	ZODIAC_SIGNS_DATA,
	translateHoroscopeTheme,
	formatHoroscopeGuidance,
	translateTheme,
	formatReadingSynthesis
} from './index';
import { getApproachTips } from '../utils/compatibilityTips';

describe('i18n translation engine', () => {
	it('translates known keys for English and Myanmar', () => {
		expect(translate('brand.name', 'en')).toBe('AstroLogic');
		expect(translate('brand.name', 'my')).toBe('AstroLogic');
		expect(translate('reading.title', 'en')).toBe('Tarot Divination');
		expect(translate('reading.title', 'my')).toBe('တားရော့ဗေဒင် ဟောကိန်း');
	});

	it('interpolates parameters correctly', () => {
		const result = translate('deck.totalCards', 'en');
		expect(result).toBe('Cards Displayed');

		// Parameter substitution
		const custom = translate('Custom {val}', 'en', { val: '42' });
		expect(custom).toBe('Custom 42');
	});

	it('falls back gracefully to English when key is missing in Myanmar', () => {
		const fallback = translate('non_existent_key_xyz', 'my');
		expect(fallback).toBe('non_existent_key_xyz');
	});
});

describe('Locale store', () => {
	it('supports toggling and setting locale', () => {
		locale.setLocale('en');
		let currentVal = '';
		const unsub = locale.subscribe((v) => (currentVal = v));
		expect(currentVal).toBe('en');

		locale.setLocale('my');
		expect(currentVal).toBe('my');

		locale.toggle();
		expect(currentVal).toBe('en');

		unsub();
	});
});

describe('Tarot translations (Full 78-card deck)', () => {
	it('contains exactly 78 tarot cards in the dataset', () => {
		const cardKeys = Object.keys(TAROT_CARDS_DATA);
		expect(cardKeys.length).toBe(78);
	});

	it('translates major arcana cards in both languages', () => {
		const foolEn = getCardTranslation('The Fool', 'en');
		const foolMy = getCardTranslation('The Fool', 'my');

		expect(foolEn.name).toBe('The Fool');
		expect(foolMy.name).toBe('လူမိုက် (သို့) အစပြုသူ');
		expect(foolEn.arcana).toBe('Major Arcana');
		expect(foolMy.arcana).toBe('မေဂျာအာခါနာ (အဓိကနက်နဲသောအရာ)');
		expect(foolEn.element).toBe('Air');
		expect(foolMy.element).toBe('လေဓာတ်');
		expect(foolEn.keywords.length).toBeGreaterThan(0);
		expect(foolMy.keywords.length).toBeGreaterThan(0);
	});

	it('translates minor arcana cards across all four suits', () => {
		const aceWandsMy = getCardTranslation('Ace of Wands', 'my');
		const aceCupsMy = getCardTranslation('Ace of Cups', 'my');
		const aceSwordsMy = getCardTranslation('Ace of Swords', 'my');
		const acePentsMy = getCardTranslation('Ace of Pentacles', 'my');

		expect(aceWandsMy.suit).toBe('တုတ်ချောင်း (မီးဓာတ်)');
		expect(aceCupsMy.suit).toBe('ခွက် (ရေဓာတ်)');
		expect(aceSwordsMy.suit).toBe('ဓား (လေဓာတ်)');
		expect(acePentsMy.suit).toBe('ဒင်္ဂါး (မြေဓာတ်)');
	});

	it('handles snake_case and case insensitive card name lookups', () => {
		const card = getCardTranslation('the_magician', 'my');
		expect(card.name).toBe('မှော်ဆရာ');
	});

	it('translates spread positions and keywords', () => {
		expect(translatePosition('past', 'en')).toBe('past');
		expect(translatePosition('past', 'my')).toBe('အတိတ်');
		expect(translatePosition('future', 'my')).toBe('အနာဂတ်');

		expect(translateSpreadType('decision', 'my')).toBe('လမ်းခွဲရွေးချယ်မှု စနစ်');
		expect(translateSpreadType('decision', 'en')).toBe('Decision Spread');

		expect(translateTopic('love', 'my')).toBe('အချစ်ရေးနှင့် အိမ်ထောင်ရေး');
		expect(translateTopic('career', 'en')).toBe('Career & Work');
	});
});

describe('Zodiac translations (12 signs & Astrological Attributes)', () => {
	it('contains all 12 zodiac signs with full metadata', () => {
		const signs = Object.keys(ZODIAC_SIGNS_DATA);
		expect(signs.length).toBe(12);
	});

	it('translates signs into English and authentic Myanmar designations', () => {
		const ariesEn = getZodiacTranslation('Aries', 'en');
		const ariesMy = getZodiacTranslation('Aries', 'my');

		expect(ariesEn.name).toBe('Aries');
		expect(ariesMy.name).toBe('မိဿရာသီ');
		expect(ariesEn.element).toBe('Fire');
		expect(ariesMy.element).toBe('မီးဓာတ်');

		const scorpioMy = getZodiacTranslation('Scorpio', 'my');
		expect(scorpioMy.name).toBe('ဗြိစ္ဆာရာသီ');
		expect(scorpioMy.element).toBe('ရေဓာတ်');
	});

	it('translates astrological elements, modalities, and ruling planets', () => {
		expect(formatElement('fire', 'en')).toBe('Fire');
		expect(formatElement('fire', 'my')).toBe('မီးဓာတ်');

		expect(formatModality('cardinal', 'en')).toBe('Cardinal');
		expect(formatModality('cardinal', 'my')).toBe('အစပျိုး (Cardinal)');

		expect(formatPlanet('Mars', 'en')).toBe('Mars');
		expect(formatPlanet('Mars', 'my')).toBe('အင်္ဂါဂြိုဟ်');
	});
});

describe('Bilingual Compatibility Tips Generator', () => {
	it('generates tips in English and Myanmar', () => {
		const enTips = getApproachTips('Aries', 'Leo', 'en');
		const myTips = getApproachTips('Aries', 'Leo', 'my');

		expect(enTips.approach.firstMove).toBeTruthy();
		expect(myTips.approach.firstMove).toBeTruthy();
		expect(enTips.conversationStarters.length).toBeGreaterThan(0);
		expect(myTips.conversationStarters.length).toBeGreaterThan(0);
		expect(enTips.dateIdeas.length).toBeGreaterThan(0);
		expect(myTips.dateIdeas.length).toBeGreaterThan(0);
		expect(enTips.intimacyTip).toBeTruthy();
		expect(myTips.intimacyTip).toBeTruthy();
	});
});

describe('Horoscope localization & formatters', () => {
	it('translates daily horoscope themes into fluent Myanmar', () => {
		expect(translateHoroscopeTheme('nurturing', 'my')).toBe('နွေးထွေးစွာ ပြုစုစောင့်ရှောက်ခြင်း');
		expect(translateHoroscopeTheme('courage', 'my')).toBe('ရဲရင့်သော သတ္တိ');
		expect(translateHoroscopeTheme('nurturing', 'en')).toBe('Nurturing');

		const guidanceMy = formatHoroscopeGuidance(
			'Today emphasizes nurturing for cancer.',
			'cancer',
			'nurturing',
			'calm',
			'my'
		);
		expect(guidanceMy).toContain('ကရကဋ်');
		expect(guidanceMy).toContain('နွေးထွေးစွာ ပြုစုစောင့်ရှောက်ခြင်း');
	});
});

describe('Tarot reading question-focused synthesis & theme localization', () => {
	it('translates previously missing Prolog themes without leaking raw English tokens', () => {
		expect(translateTheme('ambition', 'my')).toBe('ကြီးမားသော ရည်မှန်းချက်');
		expect(translateTheme('following_heart', 'my')).toBe('နှလုံးသားဆန္ဒအတိုင်း လိုက်နာခြင်း');
		expect(translateTheme('followingheart', 'my')).toBe('နှလုံးသားဆန္ဒအတိုင်း လိုက်နာခြင်း');
		expect(translateTheme('new_skills', 'my')).toBe('ကျွမ်းကျင်မှုအသစ်များ သင်ယူခြင်း');
		expect(translateTheme('newskills', 'my')).toBe('ကျွမ်းကျင်မှုအသစ်များ သင်ယူခြင်း');
	});

	it('produces question-aware Burmese reading synthesis for exam inquiries', () => {
		const mockReading = {
			question: 'စာမေးပွဲအောင်မှာလား',
			category: 'education',
			topic: 'education',
			zodiac_sign: 'cancer',
			cards: [
				{ name: 'Knight of Wands', position: 'Past', is_reversed: false },
				{ name: 'Knight of Cups', position: 'Present', is_reversed: false },
				{ name: 'Knight of Swords', position: 'Future', is_reversed: false }
			],
			themes: ['ambition', 'following_heart', 'new_skills']
		};

		const synthesis = formatReadingSynthesis(
			'Your reading draws Knight of Wands, Knight of Cups...',
			mockReading,
			'my'
		);

		expect(synthesis).toContain('စာမေးပွဲအောင်မှာလား');
		expect(synthesis).toContain('စာမေးပွဲနှင့် ပညာရေးအောင်မြင်မှု');
		expect(synthesis).toContain('တုတ်ကိုင်မြင်းစီးသူရဲကောင်း');
		expect(synthesis).toContain('ကြီးမားသော ရည်မှန်းချက်');
		expect(synthesis).not.toContain('followingheart');
		expect(synthesis).not.toContain('newskills');
	});

	it('should format relationship reading for boyfriend timing question properly', () => {
		const mockReading = {
			question: 'ချစ်သူကောင်လေးရဖို့ကြာဦးမှာလား',
			category: 'relationship',
			topic: 'relationship',
			zodiac_sign: 'cancer',
			cards: [
				{ name: 'Knight of Pentacles', position: 'You', is_reversed: false },
				{ name: 'Knight of Swords', position: 'Other Person', is_reversed: true },
				{ name: 'Nine of Wands', position: 'Connection', is_reversed: false },
				{ name: 'The Lovers', position: 'Challenge', is_reversed: false },
				{ name: 'Two of Cups', position: 'Guidance', is_reversed: false }
			],
			themes: ['hard_work', 'perseverance', 'resilience']
		};

		const synthesis = formatReadingSynthesis('', mockReading, 'my');

		expect(synthesis).toContain('ချစ်သူကောင်လေးရဖို့ကြာဦးမှာလား');
		expect(synthesis).toContain('အချစ်သစ် ပေါ်ပေါက်လာနိုင်မှုနှင့် အချိန်ကာလ');
		expect(synthesis).toContain('ဒင်္ဂါးကိုင်မြင်းစီးသူရဲကောင်း');
		expect(synthesis).toContain('ဓားကိုင်မြင်းစီးသူရဲကောင်း');
		expect(synthesis).toContain('တုတ် ၉ ချောင်း');
		expect(synthesis).toContain('တစ်ဖက်လူ / လက်တွဲဖော်');
		expect(synthesis).toContain('နှစ်ဦးဆက်နွယ်မှု / သံယောဇဉ်');
		expect(synthesis).toContain('ကရကဋ်ရာသီဖွား (ရေဓာတ်) အနေဖြင့်');
		expect(synthesis).toContain('အလင်းဘက်ခြမ်း');
		expect(synthesis).toContain('သတိပြုဖွယ်');
		expect(synthesis).not.toContain('undefined');
	});

	it('should provide customized advice for different zodiac signs and decision question', () => {
		const mockReadingAries = {
			question: 'ဒီအလုပ်ကို ပြောင်းသင့်သလား',
			category: 'decision',
			topic: 'career',
			zodiac_sign: 'aries',
			cards: [
				{ name: 'The Chariot', position: 'Situation', is_reversed: false },
				{ name: 'Two of Wands', position: 'Path A', is_reversed: false },
				{ name: 'Four of Swords', position: 'Path B', is_reversed: false }
			],
			themes: ['determination', 'direction']
		};

		const synthesisAries = formatReadingSynthesis('', mockReadingAries, 'my');
		expect(synthesisAries).toContain('မိဿရာသီဖွား (မီးဓာတ်) အနေဖြင့်');
		expect(synthesisAries).toContain('အလုပ်အကိုင်နှင့် စီးပွားရေး');
		expect(synthesisAries).toContain('စစ်ရထား');

		const mockReadingDecision = {
			question: 'လမ်းခွဲ A နဲ့ B ဘယ်လမ်းကို ရွေးသင့်သလဲ',
			category: 'decision',
			topic: 'decision',
			zodiac_sign: 'libra',
			cards: [
				{ name: 'Justice', position: 'Situation', is_reversed: false }
			]
		};
		const synthesisLibra = formatReadingSynthesis('', mockReadingDecision, 'my');
		expect(synthesisLibra).toContain('တူရာသီဖွား (လေဓာတ်) အနေဖြင့်');
		expect(synthesisLibra).toContain('ရွေးချယ်မှုနှင့် စွမ်းအင်စီးဆင်းမှု');
		expect(synthesisLibra).toContain('တရားမျှတမှု');
	});
});
