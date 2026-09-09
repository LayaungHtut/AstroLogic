const API_BASE = 'http://localhost:8000/api';

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
	const url = `${API_BASE}${path}`;
	const response = await fetch(url, {
		...options,
		headers: {
			'Content-Type': 'application/json',
			...options?.headers
		}
	});

	if (!response.ok) {
		const error = await response.text();
		throw new Error(`API Error: ${response.status} - ${error}`);
	}

	return response.json();
}

export async function fetchAllZodiac() {
	return apiFetch<import('$lib/types').ZodiacInfo[]>('/zodiac');
}

export async function fetchZodiac(sign: string) {
	return apiFetch<import('$lib/types').ZodiacInfo>(`/zodiac/${sign}`);
}

export async function fetchAllTarotCards() {
	return apiFetch<import('$lib/types').TarotCardInfo[]>('/tarot');
}

export async function drawTarotCards(count: number, spreadType?: string) {
	return apiFetch<import('$lib/types').DrawResponse>('/tarot/draw', {
		method: 'POST',
		body: JSON.stringify({ count, spread_type: spreadType })
	});
}

export async function analyzeReading(
	question: string,
	zodiacSign: string,
	spreadType?: string,
	cardCount?: number,
	locale: string = 'en'
) {
	return apiFetch<import('$lib/types').ReadingResult>('/reading/analyze', {
		method: 'POST',
		body: JSON.stringify({
			question,
			zodiac_sign: zodiacSign,
			spread_type: spreadType,
			// Only meaningful when spreadType === 'custom'; the backend ignores
			// it for fixed spreads, which use their own predetermined count.
			card_count: cardCount,
			locale
		})
	});
}

export async function analyzeSelectedReading(
	question: string,
	zodiacSign: string,
	cards: { name: string; is_reversed: boolean }[],
	locale: string = 'en'
) {
	// The backend reports a bad selection (duplicate or unrecognized card)
	// as a 200 response with an `error` field rather than an HTTP error, so
	// the caller checks `result.error` the same way the other read-only
	// analysis endpoints in this app do.
	return apiFetch<import('$lib/types').ReadingResult & { error?: string }>(
		'/reading/analyze-selected',
		{
			method: 'POST',
			body: JSON.stringify({ question, zodiac_sign: zodiacSign, cards, locale })
		}
	);
}

export async function saveReading(data: Record<string, unknown>) {
	return apiFetch<{ id: number; status: string }>('/reading/generate', {
		method: 'POST',
		body: JSON.stringify(data)
	});
}

export async function generateHoroscope(zodiacSign: string, mood: string, locale: string = 'en') {
	return apiFetch<import('$lib/types').HoroscopeResult>('/horoscope/generate', {
		method: 'POST',
		body: JSON.stringify({ zodiac_sign: zodiacSign, mood, locale })
	});
}

export async function analyzeCompatibility(sign1: string, sign2: string) {
	return apiFetch<import('$lib/types').CompatibilityResult>('/compatibility/analyze', {
		method: 'POST',
		body: JSON.stringify({ sign1, sign2 })
	});
}

export async function fetchSynastry(sign1: string, sign2: string) {
	return apiFetch<import('$lib/types').SynastryResult>('/compatibility/synastry', {
		method: 'POST',
		body: JSON.stringify({ sign1, sign2 })
	});
}

export async function fetchZodiacProfile(sign: string) {
	return apiFetch<import('$lib/types').ZodiacProfileResult>(`/zodiac/${sign}/profile`);
}

export async function sendChatMessage(
	message: string,
	zodiacSign?: string,
	currentReading?: Record<string, unknown>,
	locale?: string
) {
	return apiFetch<{ response: string; context_used: Record<string, unknown> }>('/chat', {
		method: 'POST',
		body: JSON.stringify({
			message,
			zodiac_sign: zodiacSign,
			current_reading: currentReading,
			locale
		})
	});
}

export async function fetchHistory() {
	return apiFetch<import('$lib/types').HistoryItem[]>('/history');
}

export async function fetchReading(id: number) {
	return apiFetch<import('$lib/types').ReadingResult>(`/history/${id}`);
}

export async function deleteReading(id: number) {
	return apiFetch<{ status: string }>(`/history/${id}`, { method: 'DELETE' });
}

export async function fetchAnalytics() {
	return apiFetch<import('$lib/types').AnalyticsData>('/analytics');
}

export async function healthCheck() {
	return apiFetch<{ status: string; service: string }>('/health');
}
