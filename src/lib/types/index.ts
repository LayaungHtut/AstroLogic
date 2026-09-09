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
	suit?: string;
	keywords: string[];
	upright?: string[];
	reversed?: string[];
	themes?: string[];
	is_reversed: boolean;
	image?: string;
}

export interface ZodiacAffinity {
	zodiac: string;
	sign?: string;
	element: string;
	element_theme: string;
	card: string;
	card_theme: string;
	theme?: string;
	combined: string;
}

export interface CardRanking {
	rank: number;
	eligible_pool_size: number;
	priority: number;
	zodiac_affinity_match: boolean;
	category_match: boolean;
	element_match: boolean;
}

export interface DrawnCard {
	card: string;
	name: string;
	position: string;
	is_reversed: boolean;
	keywords: string[];
	image?: string;
	zodiac_affinity?: ZodiacAffinity | null;
	ranking?: CardRanking | null;
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

export interface ThemeConflict {
	card1_position: string | null;
	card1_name: string;
	theme1: string;
	card2_position: string | null;
	card2_name: string;
	theme2: string;
	title: string;
	description: string;
}

export interface TopicInfo {
	topic: string;
	description: string;
	spread: string;
	element: string;
}

export interface ReadingResult {
	id?: number;
	question: string;
	category: string;
	topic?: string;
	topic_info?: TopicInfo | null;
	spread_rationale?: string;
	zodiac_sign: string;
	spread_type: string;
	spread_name?: string;
	cards: DrawnCard[];
	themes: string[];
	dominant_theme?: string | null;
	direction?: string;
	advice?: { category_advice: string; theme_advice: string };
	conflicts?: ThemeConflict[];
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

export interface SynastryScoreComponent {
	name: string;
	score: number;
	weight: number;
	description: string;
}

export interface SynastryResult {
	sign1: string;
	sign2: string;
	overall_level: string;
	overall_score: number;
	score_breakdown: {
		element: SynastryScoreComponent;
		modality: SynastryScoreComponent;
		traits: SynastryScoreComponent;
		planetary: SynastryScoreComponent;
		overall: number;
	};
	communication_theme: string;
	balance_theme: string;
	strengths: string[];
	challenges: string[];
	complementary_traits: { trait1: string; trait2: string }[];
	reasoning: ReasoningStep[];
}

export interface ZodiacProfileResult {
	profile: {
		sign: string;
		element: string;
		modality: string;
		ruling_planet: string;
		traits: string[];
		personality_style: string;
		approach_to_life: string;
		planetary_influence: string;
	};
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

export interface AnalyticsInsight {
	type: 'recurring_theme' | 'suit_bias' | 'reversal_bias' | 'category_suit_bias';
	rule: string;
	theme?: string;
	count?: number;
	suit?: string;
	element?: string;
	proportion?: number;
	bias?: string;
	category?: string;
}

export interface AnalyticsData {
	total_readings: number;
	most_drawn_cards: { card: string; count: number }[];
	most_common_suit: string;
	major_vs_minor: { major: number; minor: number };
	most_common_themes: { theme: string; count: number }[];
	most_common_categories: { category: string; count: number }[];
	upright_vs_reversed: { upright: number; reversed: number };
	insights: AnalyticsInsight[];
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

export interface PlanetPosition {
	name: string;
	sign: string;
	symbol: string;
	element: string;
	modality: string;
	influence: string;
	degree?: number;
	retrograde?: boolean;
}

export const PLANET_SYMBOLS: Record<string, string> = {
	sun: '☉', moon: '☽', mercury: '☿', venus: '♀',
	mars: '♂', jupiter: '♃', saturn: '♄',
	uranus: '♅', neptune: '♆', pluto: '♇'
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
	{ id: 'career', name: 'Career', description: 'Professional guidance', count: 5 },
	// count: 0 is a sentinel for "variable" — a custom draw's actual card
	// count (1-10) is chosen separately in the UI and sent as card_count.
	{ id: 'custom', name: 'Custom Draw', description: 'Pick your own card count', count: 0 }
] as const;

export const CUSTOM_DRAW_MIN = 1;
export const CUSTOM_DRAW_MAX = 10;

export interface BirthChartAspect {
	body1: string;
	body2: string;
	body1_name: string;
	body2_name: string;
	body1_name_my: string;
	body2_name_my: string;
	aspect: string;
	aspect_my: string;
	angle: number;
	orb: number;
	type: string;
	description: string;
}

export interface BirthChartExplanationData {
	archetype_title: string;
	core_identity: {
		title: string;
		sun: {
			sign: string;
			name: string;
			symbol: string;
			sign_display: string;
			essence: string;
			strengths: string[];
			growth_lesson: string;
		};
		moon: {
			sign: string;
			name: string;
			symbol: string;
			sign_display: string;
			essence: string;
			need: string;
		};
		rising: {
			sign: string;
			name: string;
			symbol: string;
			sign_display: string;
			essence: string;
			vibe: string;
		};
		triad_synthesis: string;
	};
	aspects: BirthChartAspect[];
	planetary_breakdown: {
		name: string;
		display_name: string;
		symbol: string;
		sign: string;
		sign_display: string;
		degree?: number;
		retrograde?: boolean;
		domain: string;
		interpretation: string;
	}[];
	elemental_constitution: {
		dominant: string;
		percentages: Record<string, number>;
		analysis: string;
	};
	guidance: string;
}
