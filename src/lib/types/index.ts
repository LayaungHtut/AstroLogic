export interface ZodiacInfo {
	sign: string;
	element: string;
	modality: string;
	ruling_planet: string;
	traits: string[];
	date_range: string;
	symbol: string;
}

export interface TarotCardInfo {
	card: string;
	name: string;
	arcana?: string;
	keywords: string[];
	upright?: string[];
	reversed?: string[];
	themes?: string[];
	is_reversed: boolean;
	image?: string;
}

export interface DrawnCard {
	card: string;
	name: string;
	position: string;
	is_reversed: boolean;
	keywords: string[];
	image?: string;
}

export interface DrawResponse {
	cards: DrawnCard[];
	spread_type: string;
	positions: string[];
}

export interface ReasoningStep {
	rule: string;
	result: string;
}

export interface ReadingResult {
	id?: number;
	question: string;
	category: string;
	zodiac_sign: string;
	spread_type: string;
	spread_name?: string;
	cards: DrawnCard[];
	themes: string[];
	reasoning: ReasoningStep[];
	ai_interpretation: string;
	facts?: Record<string, unknown>;
	created_at?: string;
}

export interface HoroscopeResult {
	zodiac_sign: string;
	element: string;
	theme: string;
	mood: string;
	guidance: string;
	reflection: string;
	opportunity: string;
	caution: string;
	reasoning: ReasoningStep[];
}

export interface CompatibilityResult {
	sign1: string;
	sign2: string;
	element1: string;
	element2: string;
	modality1: string;
	modality2: string;
	level: string;
	element_description: string;
	reasoning: ReasoningStep[];
}

export interface ChatMessage {
	role: 'user' | 'assistant';
	content: string;
}

export interface HistoryItem {
	id: number;
	question: string;
	category: string;
	zodiac_sign: string;
	spread_type: string;
	cards_json: string;
	themes_json: string;
	ai_interpretation: string;
	created_at: string;
}

export interface AnalyticsData {
	total_readings: number;
	most_drawn_cards: { card: string; count: number }[];
	most_common_suit: string;
	major_vs_minor: { major: number; minor: number };
	most_common_themes: { theme: string; count: number }[];
	most_common_categories: { category: string; count: number }[];
	upright_vs_reversed: { upright: number; reversed: number };
}

export interface UserProfile {
	nickname: string;
	zodiac_sign: string;
	birth_date: string;
	preferred_style: string;
}

export const ZODIAC_SIGNS = [
	'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
	'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
] as const;

export const ZODIAC_SYMBOLS: Record<string, string> = {
	aries: '\u2648', taurus: '\u2649', gemini: '\u264A', cancer: '\u264B',
	leo: '\u264C', virgo: '\u264D', libra: '\u264E', scorpio: '\u264F',
	sagittarius: '\u2650', capricorn: '\u2651', aquarius: '\u2652', pisces: '\u2653'
};

export const ELEMENT_COLORS: Record<string, string> = {
	fire: '#FF6B35',
	earth: '#8B7355',
	air: '#87CEEB',
	water: '#4169E1'
};

export const ELEMENT_ICONS: Record<string, string> = {
	fire: '\uD83D\uDD25',
	earth: '\uD83C\uDF31',
	air: '\uD83C\uDF2C\uFE0F',
	water: '\uD83D\uDCA7'
};

export const SPREAD_TYPES = [
	{ id: 'one_card', name: 'One Card', description: 'Simple daily guidance', count: 1 },
	{ id: 'three_card', name: 'Three Card', description: 'Past, Present, Future', count: 3 },
	{ id: 'decision', name: 'Decision', description: 'Compare paths', count: 4 },
	{ id: 'self_reflection', name: 'Self Reflection', description: 'Inner exploration', count: 4 },
	{ id: 'relationship', name: 'Relationship', description: 'Connection analysis', count: 5 },
	{ id: 'career', name: 'Career', description: 'Professional guidance', count: 5 }
] as const;
