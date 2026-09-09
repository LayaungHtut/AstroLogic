<script lang="ts">
	import { onMount } from 'svelte';
	import { fetchAllTarotCards } from '$lib/utils/api';
	import { cardImage } from '$lib/utils/image';
	import type { TarotCardInfo } from '$lib/types';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import { locale, t, getCardTranslation } from '$lib/i18n';

	let {
		selected = $bindable([]),
		max,
	}: { selected: { name: string; is_reversed: boolean }[]; max: number } = $props();

	let allCards = $state<TarotCardInfo[]>([]);
	let loading = $state(true);
	let loadError = $state('');
	let mode = $state<'mystery' | 'browse'>('mystery');

	interface MysterySlot {
		id: number;
		card: TarotCardInfo;
		revealed: boolean;
		is_reversed: boolean;
	}

	let mysterySlots = $state<MysterySlot[]>([]);
	let search = $state('');
	let suitFilter = $state('all');

	const CARD_BACK_URL = cardImage('https://sixseeds.github.io/tarot-api/cards/back.jpg', 320);

	function shuffleArray<T>(array: T[]): T[] {
		const arr = [...array];
		for (let i = arr.length - 1; i > 0; i--) {
			const j = Math.floor(Math.random() * (i + 1));
			[arr[i], arr[j]] = [arr[j], arr[i]];
		}
		return arr;
	}

	function dealMysteryCards(source: TarotCardInfo[]) {
		if (!source.length) return;
		const shuffled = shuffleArray(source);
		// Deal 15 face-down cards
		const pool = shuffled.slice(0, 15);
		mysterySlots = pool.map((c, idx) => {
			const isAlreadySelected = selected.some((s) => s.name === c.name);
			const selItem = selected.find((s) => s.name === c.name);
			return {
				id: idx + 1,
				card: c,
				revealed: isAlreadySelected,
				is_reversed: selItem ? selItem.is_reversed : Math.random() < 0.2
			};
		});
	}

	onMount(async () => {
		try {
			allCards = await fetchAllTarotCards();
			dealMysteryCards(allCards);
		} catch (e) {
			loadError = e instanceof Error ? e.message : "Couldn't reach the tarot API.";
		} finally {
			loading = false;
		}
	});

	function reshuffle() {
		dealMysteryCards(allCards);
	}

	const suits = $derived([
		{ id: 'all', label: $t('common.all') },
		{ id: 'major', label: $locale === 'my' ? 'မေဂျာ' : 'Major' },
		{ id: 'wands', label: $locale === 'my' ? 'တုတ်ချောင်း' : 'Wands' },
		{ id: 'cups', label: $locale === 'my' ? 'ခွက်' : 'Cups' },
		{ id: 'swords', label: $locale === 'my' ? 'ဓား' : 'Swords' },
		{ id: 'pentacles', label: $locale === 'my' ? 'ဒင်္ဂါး' : 'Pentacles' },
	]);

	function cardSuit(card: TarotCardInfo): string {
		if (card.arcana === 'major' || card.arcana === 'major_arcana') return 'major';
		if (card.suit) return card.suit.toLowerCase();
		for (const s of ['wands', 'cups', 'swords', 'pentacles']) {
			if (card.card.toLowerCase().includes(s)) return s;
		}
		return 'major';
	}

	const filteredBrowseCards = $derived(
		(suitFilter === 'all' ? allCards : allCards.filter((c) => cardSuit(c) === suitFilter)).filter(
			(c) => {
				if (!search) return true;
				const q = search.toLowerCase();
				const trans = getCardTranslation(c.name, $locale);
				return (
					c.name.toLowerCase().includes(q) ||
					trans.name.toLowerCase().includes(q)
				);
			}
		),
	);

	function isSelected(name: string): boolean {
		return selected.some((s) => s.name === name);
	}

	function onMysteryCardClick(slotIndex: number) {
		const slot = mysterySlots[slotIndex];
		if (!slot) return;

		const selectedIndex = selected.findIndex((s) => s.name === slot.card.name);

		if (selectedIndex >= 0) {
			// Deselect card
			selected = selected.filter((_, i) => i !== selectedIndex);
			slot.revealed = false;
		} else {
			// Check if maximum cards reached
			if (selected.length >= max) return;
			// Reveal and select
			slot.revealed = true;
			selected = [...selected, { name: slot.card.name, is_reversed: slot.is_reversed }];
		}
	}

	function toggleBrowseCard(card: TarotCardInfo) {
		const idx = selected.findIndex((s) => s.name === card.name);
		if (idx >= 0) {
			selected = selected.filter((_, i) => i !== idx);
			const slot = mysterySlots.find((s) => s.card.name === card.name);
			if (slot) slot.revealed = false;
		} else if (selected.length < max) {
			selected = [...selected, { name: card.name, is_reversed: false }];
			const slot = mysterySlots.find((s) => s.card.name === card.name);
			if (slot) slot.revealed = true;
		}
	}

	function removeAt(idx: number) {
		const removed = selected[idx];
		selected = selected.filter((_, i) => i !== idx);
		if (removed) {
			const slot = mysterySlots.find((s) => s.card.name === removed.name);
			if (slot) slot.revealed = false;
		}
	}

	function toggleReversed(idx: number) {
		selected = selected.map((s, i) => {
			if (i === idx) {
				const nextRev = !s.is_reversed;
				const slot = mysterySlots.find((m) => m.card.name === s.name);
				if (slot) slot.is_reversed = nextRev;
				return { ...s, is_reversed: nextRev };
			}
			return s;
		});
	}

	function moveUp(idx: number) {
		if (idx === 0) return;
		const next = [...selected];
		[next[idx - 1], next[idx]] = [next[idx], next[idx - 1]];
		selected = next;
	}

	function moveDown(idx: number) {
		if (idx === selected.length - 1) return;
		const next = [...selected];
		[next[idx + 1], next[idx]] = [next[idx], next[idx + 1]];
		selected = next;
	}

	const atMax = $derived(selected.length >= max);
</script>

<div class="flex flex-col gap-4">
	<!-- SELECTED CARDS TRAY -->
	<div class="rounded-xl border border-primary/20 bg-surface-container-high/40 p-4 backdrop-blur-md">
		<div class="mb-3 flex items-center justify-between">
			<div class="flex items-center gap-2">
				<span class="material-symbols-outlined text-base text-primary">auto_fix_high</span>
				<span class="text-sm font-semibold text-on-surface">
					{$locale === 'my' ? 'သင်ရွေးချယ်ထားသော ကတ်များ' : 'Your Drawn Selection'}
				</span>
			</div>
			<span
				class="font-mono-data text-xs font-bold px-2 py-0.5 rounded-full {atMax ? 'bg-secondary/20 text-secondary' : 'bg-surface-container text-primary'}"
			>
				{selected.length} / {max}
			</span>
		</div>

		{#if !selected.length}
			<p class="text-xs text-on-surface-variant flex items-center gap-1.5">
				<span class="material-symbols-outlined text-sm text-secondary">touch_app</span>
				{$locale === 'my'
					? 'အောက်ပါ မျက်နှာဖုံးကတ် ၁၅ ကတ်ထဲမှ သင်နှစ်သက်ရာကို လျှို့ဝှက်ဆွဲယူပါ (ကတ်ကို နှိပ်ပါက လှန်ပြပါမည်)'
					: 'Select from the 15 mystery face-down cards below. Click a card to draw and reveal its wisdom.'}
			</p>
		{:else}
			<div class="flex flex-col gap-1.5">
				{#each selected as sel, i (sel.name)}
					{@const cardTrans = getCardTranslation(sel.name, $locale)}
					<div class="flex items-center gap-2 rounded-lg bg-surface-container-lowest/80 px-3 py-2 border border-white/5 shadow-sm">
						<span
							class="font-mono-data flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/20 text-[10px] font-semibold text-primary"
							>{i + 1}</span
						>
						<span class="flex-1 truncate text-sm font-medium text-on-surface">{cardTrans.name || sel.name}</span>
						<button
							type="button"
							class="font-mono-data rounded-full px-2 py-0.5 text-[10px] uppercase tracking-wider transition-colors
								{sel.is_reversed
								? 'bg-error-container/40 text-error'
								: 'bg-surface-container text-on-surface-variant hover:bg-surface-container-highest'}"
							onclick={() => toggleReversed(i)}
						>
							{sel.is_reversed ? $t('common.reversed') : $t('common.upright')}
						</button>
						<button
							type="button"
							class="flex h-6 w-6 items-center justify-center rounded-full text-on-surface-variant transition-colors hover:bg-surface-container-highest disabled:opacity-30"
							disabled={i === 0}
							onclick={() => moveUp(i)}
							aria-label="Move up"
						>
							<span class="material-symbols-outlined text-sm">arrow_upward</span>
						</button>
						<button
							type="button"
							class="flex h-6 w-6 items-center justify-center rounded-full text-on-surface-variant transition-colors hover:bg-surface-container-highest disabled:opacity-30"
							disabled={i === selected.length - 1}
							onclick={() => moveDown(i)}
							aria-label="Move down"
						>
							<span class="material-symbols-outlined text-sm">arrow_downward</span>
						</button>
						<button
							type="button"
							class="flex h-6 w-6 items-center justify-center rounded-full text-error transition-colors hover:bg-error-container/30"
							onclick={() => removeAt(i)}
							aria-label="Remove {cardTrans.name || sel.name}"
						>
							<span class="material-symbols-outlined text-sm">close</span>
						</button>
					</div>
				{/each}
			</div>
		{/if}
	</div>

	<!-- DRAW MODE SELECTOR & ACTIONS -->
	<div class="flex flex-wrap items-center justify-between gap-2">
		<div class="flex items-center gap-1 rounded-full bg-surface-container-high/60 p-1 border border-white/5">
			<button
				type="button"
				class="font-mono-data text-xs px-3 py-1 rounded-full transition-all flex items-center gap-1.5 {mode === 'mystery' ? 'bg-primary text-on-primary shadow-sm font-semibold' : 'text-on-surface-variant hover:text-on-surface'}"
				onclick={() => (mode = 'mystery')}
			>
				<span class="material-symbols-outlined text-sm">style</span>
				{$locale === 'my' ? 'မျက်နှာဖုံးကတ်များ (၁၅ ကတ်)' : 'Mystery Spread (15 Cards)'}
			</button>
			<button
				type="button"
				class="font-mono-data text-xs px-3 py-1 rounded-full transition-all flex items-center gap-1.5 {mode === 'browse' ? 'bg-primary text-on-primary shadow-sm font-semibold' : 'text-on-surface-variant hover:text-on-surface'}"
				onclick={() => (mode = 'browse')}
			>
				<span class="material-symbols-outlined text-sm">manage_search</span>
				{$locale === 'my' ? 'ကတ် ၇၈ ကတ် ရှာဖွေမည်' : 'Full Deck Browser'}
			</button>
		</div>

		{#if mode === 'mystery'}
			<button
				type="button"
				class="font-mono-data text-xs px-3 py-1 rounded-full bg-secondary/15 hover:bg-secondary/25 text-secondary border border-secondary/30 transition-all flex items-center gap-1.5 active:scale-95"
				onclick={reshuffle}
				title={$locale === 'my' ? 'ကတ်များကို အသစ်ပြန်မွှေမည်' : 'Shuffle a new set of 15 cards'}
			>
				<span class="material-symbols-outlined text-sm">shuffle</span>
				{$locale === 'my' ? 'ကတ်များ ပြန်လည်မွှေမည်' : 'Reshuffle Deck'}
			</button>
		{/if}
	</div>

	{#if loading}
		<LoadingSpinner text={$t('common.loading')} />
	{:else if loadError}
		<div class="glass-card p-6 text-center text-sm text-error">{loadError}</div>
	{:else if mode === 'mystery'}
		<!-- 15 FACE-DOWN MYSTERY SPREAD -->
		<div class="flex flex-col gap-2">
			<p class="text-[11px] text-on-surface-variant/80 italic text-center">
				{$locale === 'my'
					? 'ကတ်များ၏ နောက်ကျောကိုသာ မြင်တွေ့ရမည်ဖြစ်ပြီး စိတ်ကြိုက်ကတ်ကို နှိပ်လိုက်ပါက ကတ်ပက်လက်လှန်၍ ရွေးချယ်သွားပါမည်။'
					: 'Cards are dealt face down. Trust your intuition and tap to draw and reveal.'}
			</p>

			<div class="grid grid-cols-3 gap-2.5 sm:grid-cols-5 perspective-[1000px] max-h-120 overflow-y-auto p-1">
				{#each mysterySlots as slot, idx (slot.card.card + idx)}
					{@const picked = isSelected(slot.card.name)}
					{@const cardTrans = getCardTranslation(slot.card.name, $locale)}
					<button
						type="button"
						class="group relative flex flex-col items-center cursor-pointer select-none transition-transform duration-300 hover:scale-105 active:scale-95 disabled:cursor-not-allowed"
						onclick={() => onMysteryCardClick(idx)}
						disabled={!picked && atMax}
						aria-label={slot.revealed ? cardTrans.name || slot.card.name : `Mystery Card #${slot.id}`}
					>
						<div
							class="relative aspect-2/3 w-full rounded-xl overflow-hidden shadow-md transition-all duration-500 border {picked ? 'ring-2 ring-primary shadow-primary/30' : 'border-white/10 hover:border-secondary/40'}"
						>
							{#if slot.revealed}
								<!-- FACE UP REVEALED CARD -->
								<div class="absolute inset-0 bg-surface-container-highest flex flex-col">
									{#if slot.card.image}
										<img
											src={cardImage(slot.card.image, 200)}
											alt={cardTrans.name || slot.card.name}
											class="h-full w-full object-cover {slot.is_reversed ? 'rotate-180' : ''}"
											loading="lazy"
											onerror={(e) => ((e.currentTarget as HTMLImageElement).style.display = 'none')}
										/>
									{:else}
										<div class="h-full w-full flex items-center justify-center bg-gradient-to-br from-purple-900 to-indigo-950 p-2 text-center text-[10px] text-purple-200">
											{cardTrans.name || slot.card.name}
										</div>
									{/if}
									{#if picked}
										<div class="absolute inset-0 bg-primary/20 flex items-center justify-center backdrop-blur-[0.5px]">
											<span class="material-symbols-outlined text-2xl text-white drop-shadow">check_circle</span>
										</div>
									{/if}
								</div>
							{:else}
								<!-- FACE DOWN MYSTERY CARD BACK -->
								<div class="absolute inset-0 bg-gradient-to-b from-indigo-950 via-purple-950 to-slate-950 flex flex-col items-center justify-center p-2 border-2 border-amber-400/30 rounded-xl overflow-hidden">
									<!-- Background ornate image with gradient fallback -->
									<img
										src={CARD_BACK_URL}
										alt="Card back"
										class="absolute inset-0 h-full w-full object-cover opacity-75 group-hover:opacity-90 transition-opacity"
										loading="lazy"
										onerror={(e) => ((e.currentTarget as HTMLImageElement).style.display = 'none')}
									/>

									<!-- Cosmic Card Centerpiece -->
									<div class="relative z-10 flex flex-col items-center justify-center gap-1 rounded-full bg-black/50 p-2.5 backdrop-blur-sm border border-amber-300/30 group-hover:scale-110 transition-transform">
										<span class="material-symbols-outlined text-xl text-amber-300">sparkles</span>
										<span class="font-mono-data text-[10px] font-bold text-amber-200">#{slot.id}</span>
									</div>

									<!-- Top/bottom celestial badges -->
									<div class="pointer-events-none absolute top-1.5 text-[10px] text-amber-300/60">✦</div>
									<div class="pointer-events-none absolute bottom-1.5 text-[10px] text-amber-300/60">✦</div>
								</div>
							{/if}
						</div>

						<span class="mt-1 line-clamp-1 text-[11px] font-medium text-center {slot.revealed ? 'text-primary' : 'text-on-surface-variant'}">
							{slot.revealed ? (cardTrans.name || slot.card.name) : `${$locale === 'my' ? 'ကတ် ' : 'Card '}${slot.id}`}
						</span>
					</button>
				{/each}
			</div>
		</div>
	{:else}
		<!-- FULL 78 CARDS BROWSER MODE -->
		<div class="flex flex-col gap-3">
			<div class="flex flex-wrap items-center gap-2">
				<input
					class="input-field min-w-0 flex-1 text-sm"
					placeholder={$t('common.search')}
					type="text"
					bind:value={search}
				/>
				<div class="flex items-center gap-1.5 overflow-x-auto">
					{#each suits as s}
						<button
							type="button"
							class="font-mono-data shrink-0 rounded-full px-2.5 py-1 text-[10px] uppercase tracking-wider transition-all
								{suitFilter === s.id
								? 'bg-primary-container text-on-primary-container font-semibold'
								: 'bg-surface-container text-on-surface-variant hover:bg-surface-container-high'}"
							onclick={() => (suitFilter = s.id)}
						>
							{s.label}
						</button>
					{/each}
				</div>
			</div>

			{#if !filteredBrowseCards.length}
				<div class="glass-card p-6 text-center text-sm text-on-surface-variant">
					{$locale === 'my' ? 'မည်သည့်ကတ်မှ မတွေ့ရှိပါ' : 'No cards match this filter.'}
				</div>
			{:else}
				<div class="grid max-h-96 grid-cols-3 gap-2 overflow-y-auto pr-1 sm:grid-cols-4 md:grid-cols-6">
					{#each filteredBrowseCards as card (card.card)}
						{@const picked = isSelected(card.name)}
						{@const cardTrans = getCardTranslation(card.name, $locale)}
						<button
							type="button"
							class="group relative flex flex-col items-center gap-1 rounded-lg p-2 text-center transition-all
								{picked
								? 'bg-primary-container/30 shadow-[0_0_0_1.5px_var(--color-primary)]'
								: atMax
									? 'cursor-not-allowed opacity-40'
									: 'bg-surface-container-lowest/60 hover:bg-surface-container-high'}"
							onclick={() => toggleBrowseCard(card)}
							disabled={!picked && atMax}
						>
							<div
								class="relative flex aspect-2/3 w-full items-center justify-center overflow-hidden rounded-md bg-linear-to-br from-surface-container-high to-surface-container"
							>
								{#if card.image}
									<img
										src={cardImage(card.image, 160)}
										alt={cardTrans.name || card.name}
										class="absolute inset-0 h-full w-full object-cover"
										loading="lazy"
										onerror={(e) => ((e.currentTarget as HTMLImageElement).style.display = 'none')}
									/>
								{:else}
									<span class="material-symbols-outlined text-2xl text-on-surface-variant"
										>auto_awesome</span
									>
								{/if}
								{#if picked}
									<div
										class="absolute inset-0 flex items-center justify-center bg-primary/30 backdrop-blur-[1px]"
									>
										<span class="material-symbols-outlined text-2xl text-white drop-shadow">check_circle</span>
									</div>
								{/if}
							</div>
							<span class="line-clamp-1 text-[10px] text-on-surface-variant">{cardTrans.name || card.name}</span>
						</button>
					{/each}
				</div>
			{/if}
		</div>
	{/if}
</div>
