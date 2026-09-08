<script lang="ts">
	import { onMount } from 'svelte';
	import { fetchAllTarotCards } from '$lib/utils/api';
	import { cardImage } from '$lib/utils/image';
	import type { TarotCardInfo } from '$lib/types';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';

	let {
		selected = $bindable([]),
		max,
	}: { selected: { name: string; is_reversed: boolean }[]; max: number } = $props();

	let cards = $state<TarotCardInfo[]>([]);
	let loading = $state(true);
	let loadError = $state('');
	let search = $state('');
	let suitFilter = $state('all');

	onMount(async () => {
		try {
			cards = await fetchAllTarotCards();
		} catch (e) {
			loadError = e instanceof Error ? e.message : "Couldn't reach the tarot API.";
		} finally {
			loading = false;
		}
	});

	const suits = [
		{ id: 'all', label: 'All' },
		{ id: 'major', label: 'Major' },
		{ id: 'wands', label: 'Wands' },
		{ id: 'cups', label: 'Cups' },
		{ id: 'swords', label: 'Swords' },
		{ id: 'pentacles', label: 'Pentacles' },
	];

	function cardSuit(card: TarotCardInfo): string {
		if (card.arcana === 'major_arcana') return 'major';
		for (const s of ['wands', 'cups', 'swords', 'pentacles']) {
			if (card.card.includes(s)) return s;
		}
		return 'major';
	}

	const filtered = $derived(
		(suitFilter === 'all' ? cards : cards.filter((c) => cardSuit(c) === suitFilter)).filter(
			(c) => !search || c.name.toLowerCase().includes(search.toLowerCase()),
		),
	);

	function isSelected(name: string): boolean {
		return selected.some((s) => s.name === name);
	}

	function toggleCard(card: TarotCardInfo) {
		const idx = selected.findIndex((s) => s.name === card.name);
		if (idx >= 0) {
			selected = selected.filter((_, i) => i !== idx);
		} else if (selected.length < max) {
			selected = [...selected, { name: card.name, is_reversed: false }];
		}
	}

	function removeAt(idx: number) {
		selected = selected.filter((_, i) => i !== idx);
	}

	function toggleReversed(idx: number) {
		selected = selected.map((s, i) => (i === idx ? { ...s, is_reversed: !s.is_reversed } : s));
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
	<!-- SELECTED TRAY -->
	<div class="rounded-xl bg-surface-container-high/40 p-4">
		<div class="mb-3 flex items-center justify-between">
			<span class="text-sm font-medium text-on-surface">Your Selection</span>
			<span
				class="font-mono-data text-xs {atMax ? 'text-secondary' : 'text-on-surface-variant'}"
				>{selected.length} / {max}</span
			>
		</div>
		{#if !selected.length}
			<p class="text-xs text-on-surface-variant">
				Tap cards below to add them here, in the order you want them read.
			</p>
		{:else}
			<div class="flex flex-col gap-1.5">
				{#each selected as sel, i (sel.name)}
					<div class="flex items-center gap-2 rounded-lg bg-surface-container-lowest/70 px-3 py-2">
						<span
							class="font-mono-data flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/20 text-[10px] font-semibold text-primary"
							>{i + 1}</span
						>
						<span class="flex-1 truncate text-sm text-on-surface">{sel.name}</span>
						<button
							type="button"
							class="font-mono-data rounded-full px-2 py-0.5 text-[10px] uppercase tracking-wider transition-colors
								{sel.is_reversed
								? 'bg-error-container/40 text-error'
								: 'bg-surface-container text-on-surface-variant hover:bg-surface-container-highest'}"
							onclick={() => toggleReversed(i)}
						>
							{sel.is_reversed ? 'Reversed' : 'Upright'}
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
							aria-label="Remove {sel.name}"
						>
							<span class="material-symbols-outlined text-sm">close</span>
						</button>
					</div>
				{/each}
			</div>
		{/if}
	</div>

	<!-- DECK BROWSER -->
	<div class="flex flex-col gap-3">
		<div class="flex flex-wrap items-center gap-2">
			<input
				class="input-field min-w-0 flex-1 text-sm"
				placeholder="Search cards..."
				type="text"
				bind:value={search}
			/>
			<div class="flex items-center gap-1.5 overflow-x-auto">
				{#each suits as s}
					<button
						type="button"
						class="font-mono-data shrink-0 rounded-full px-2.5 py-1 text-[10px] uppercase tracking-wider transition-all
							{suitFilter === s.id
							? 'bg-primary-container text-on-primary-container'
							: 'bg-surface-container text-on-surface-variant hover:bg-surface-container-high'}"
						onclick={() => (suitFilter = s.id)}
					>
						{s.label}
					</button>
				{/each}
			</div>
		</div>

		{#if loading}
			<LoadingSpinner text="Loading the deck..." />
		{:else if loadError}
			<div class="glass-card p-6 text-center text-sm text-error">{loadError}</div>
		{:else if !filtered.length}
			<div class="glass-card p-6 text-center text-sm text-on-surface-variant">
				No cards match this filter.
			</div>
		{:else}
			<div class="grid max-h-96 grid-cols-3 gap-2 overflow-y-auto pr-1 sm:grid-cols-4 md:grid-cols-6">
				{#each filtered as card (card.card)}
					{@const picked = isSelected(card.name)}
					<button
						type="button"
						class="group relative flex flex-col items-center gap-1 rounded-lg p-2 text-center transition-all
							{picked
							? 'bg-primary-container/30 shadow-[0_0_0_1.5px_var(--color-primary)]'
							: atMax
								? 'cursor-not-allowed opacity-40'
								: 'bg-surface-container-lowest/60 hover:bg-surface-container-high'}"
						onclick={() => toggleCard(card)}
						disabled={!picked && atMax}
					>
						<div
							class="relative flex aspect-2/3 w-full items-center justify-center overflow-hidden rounded-md bg-linear-to-br from-surface-container-high to-surface-container"
						>
							{#if card.image}
								<img
									src={cardImage(card.image, 160)}
									alt={card.name}
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
						<span class="line-clamp-1 text-[10px] text-on-surface-variant">{card.name}</span>
					</button>
				{/each}
			</div>
		{/if}
	</div>
</div>
