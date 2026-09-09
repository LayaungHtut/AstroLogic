import { writable } from 'svelte/store';
import type { ZodiacInfo, ReadingResult, UserProfile, ChatMessage } from '$lib/types';

function createProfileStore() {
	const STORAGE_KEY = 'astrologic_profile';
	const defaults: UserProfile = {
		nickname: 'Explorer',
		zodiac_sign: '',
		birth_date: '',
		preferred_style: 'balanced'
	};

	function load(): UserProfile {
		if (typeof window === 'undefined') return { ...defaults };
		try {
			const raw = localStorage.getItem(STORAGE_KEY);
			return raw ? { ...defaults, ...JSON.parse(raw) } : { ...defaults };
		} catch {
			return { ...defaults };
		}
	}

	function save(profile: UserProfile) {
		if (typeof window === 'undefined') return;
		localStorage.setItem(STORAGE_KEY, JSON.stringify(profile));
	}

	const { subscribe, set, update } = writable<UserProfile>(load());

	return {
		subscribe,
		setProfile: (partial: Partial<UserProfile>) =>
			update((p) => {
				const next = { ...p, ...partial };
				save(next);
				return next;
			}),
		reset: () => {
			set({ ...defaults });
			if (typeof window !== 'undefined') localStorage.removeItem(STORAGE_KEY);
		}
	};
}

function createReadingStore() {
	const { subscribe, set, update } = writable<ReadingResult | null>(null);

	return {
		subscribe,
		setReading: (reading: ReadingResult) => set(reading),
		clearReading: () => set(null),
		updateReading: (partial: Partial<ReadingResult>) =>
			update((r) => (r ? { ...r, ...partial } : null))
	};
}

function createChatStore() {
	const { subscribe, set, update } = writable<ChatMessage[]>([]);

	return {
		subscribe,
		addMessage: (msg: ChatMessage) => update((msgs) => [...msgs, msg]),
		setMessages: (msgs: ChatMessage[]) => set(msgs),
		clearMessages: () => set([])
	};
}

function createLoadingStore() {
	const { subscribe, set, update } = writable<Record<string, boolean>>({});

	return {
		subscribe,
		setLoading: (key: string, value: boolean) =>
			update((s: Record<string, boolean>) => ({ ...s, [key]: value })),
		isLoading: (key: string) => false
	};
}

export const profile = createProfileStore();
export const currentReading = createReadingStore();
export const chatMessages = createChatStore();
export const loading = createLoadingStore();
