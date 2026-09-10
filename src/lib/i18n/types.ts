export type SupportedLocale = 'en' | 'my';

export interface TarotCardTranslation {
	nameEn: string;
	nameMy: string;
	arcanaEn: string;
	arcanaMy: string;
	suitEn: string;
	suitMy: string;
	elementEn: string;
	elementMy: string;
	keywordsEn: string[];
	keywordsMy: string[];
	meaningUprightEn: string;
	meaningUprightMy: string;
	meaningReversedEn: string;
	meaningReversedMy: string;
}

export interface ZodiacSignTranslation {
	signEn: string;
	signMy: string;
	elementEn: string;
	elementMy: string;
	modalityEn: string;
	modalityMy: string;
	rulerEn: string;
	rulerMy: string;
	traitsEn: string[];
	traitsMy: string[];
	dateRangeEn: string;
	dateRangeMy: string;
	summaryEn: string;
	summaryMy: string;
}

export type TranslationDictionary = Record<string, string>;
