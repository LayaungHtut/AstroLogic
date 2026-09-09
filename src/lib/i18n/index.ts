import { writable, derived } from 'svelte/store';
import type { SupportedLocale } from './types';
import { TRANSLATIONS_EN, TRANSLATIONS_MY } from './translations';

const STORAGE_KEY = 'astrologic_locale';

function createLocaleStore() {
	function getInitialLocale(): SupportedLocale {
		if (typeof window === 'undefined') return 'en';
		try {
			const saved = localStorage.getItem(STORAGE_KEY);
			if (saved === 'my' || saved === 'en') return saved;
		} catch {
			// ignore
		}
		return 'en';
	}

	const { subscribe, set } = writable<SupportedLocale>(getInitialLocale());

	return {
		subscribe,
		setLocale: (next: SupportedLocale) => {
			set(next);
			if (typeof window !== 'undefined') {
				try {
					localStorage.setItem(STORAGE_KEY, next);
					document.documentElement.lang = next === 'my' ? 'my' : 'en';
				} catch {
					// ignore
				}
			}
		},
		toggle: () => {
			let current: SupportedLocale = 'en';
			const unsubscribe = subscribe((val) => (current = val));
			unsubscribe();
			const next: SupportedLocale = current === 'en' ? 'my' : 'en';
			if (typeof window !== 'undefined') {
				try {
					localStorage.setItem(STORAGE_KEY, next);
					document.documentElement.lang = next === 'my' ? 'my' : 'en';
				} catch {
					// ignore
				}
			}
			set(next);
		}
	};
}

export const locale = createLocaleStore();

export function translate(
	key: string,
	currentLocale: SupportedLocale,
	params?: Record<string, string | number>
): string {
	const dict = currentLocale === 'my' ? TRANSLATIONS_MY : TRANSLATIONS_EN;
	let text = dict[key] || TRANSLATIONS_EN[key] || key;

	if (params) {
		for (const [paramKey, paramVal] of Object.entries(params)) {
			text = text.replace(new RegExp(`{${paramKey}}`, 'g'), String(paramVal));
		}
	}
	return text;
}

export const t = derived(
	locale,
	($loc) => (key: string, params?: Record<string, string | number>) => {
		return translate(key, $loc, params);
	}
);

// Re-export all domain data and translation helpers
export * from './types';
export * from './tarotData';
export * from './zodiacData';
export * from './horoscopeData';
