<script lang="ts">
	import { onMount } from 'svelte';
	import { fetchAllTarotCards } from '$lib/utils/api';
	import type { TarotCardInfo } from '$lib/types';
	import TarotCard from '$lib/components/TarotCard.svelte';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';

	let cards = $state<TarotCardInfo[]>([]);
	let filter = $state('all');
	let search = $state('');
	let loading = $state(true);
	let selectedCard = $state<TarotCardInfo | null>(null);

	onMount(async () => {
		try {
			cards = await fetchAllTarotCards();
		} catch {
			// API may not be running
		} finally {
			loading = false;
		}
	});

	const filtered = $derived(
		(filter === 'all'
			? cards
			: filter === 'major'
				? cards.filter((c) => c.arcana === 'major_arcana')
				: cards.filter((c) => c.card.includes(filter))
		).filter((c) => !search || c.name.toLowerCase().includes(search.toLowerCase()))
	);

	$effect(() => {
		if (filtered.length && (!selectedCard || !filtered.includes(selectedCard))) {
			selectedCard = filtered[0];
		} else if (!filtered.length) {
			selectedCard = null;
		}
	});

	function selectCard(card: TarotCardInfo) {
		selectedCard = card;
	}

	const suits = [
		{ id: 'all', label: 'All Cards' },
		{ id: 'major', label: 'Major Arcana' },
		{ id: 'wands', label: 'Wands (Fire)' },
		{ id: 'cups', label: 'Cups (Water)' },
		{ id: 'swords', label: 'Swords (Air)' },
		{ id: 'pentacles', label: 'Pentacles (Earth)' },
	];

	const MAJOR_ARCANA = [
		'the_fool', 'the_magician', 'the_high_priestess', 'the_empress',
		'the_emperor', 'the_hierophant', 'the_lovers', 'the_chariot',
		'strength', 'the_hermit', 'wheel_of_fortune', 'justice',
		'the_hanged_man', 'death', 'temperance', 'the_devil',
		'the_tower', 'the_star', 'the_moon', 'the_sun',
		'judgement', 'the_world',
	];
	const ROMAN = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI'];

	function capitalize(s: string) {
		return s.charAt(0).toUpperCase() + s.slice(1);
	}

	function cardSuit(card: TarotCardInfo): 'wands' | 'cups' | 'swords' | 'pentacles' | 'major' {
		if (card.arcana === 'major_arcana') return 'major';
		for (const s of ['wands', 'cups', 'swords', 'pentacles'] as const) {
			if (card.card.includes(s)) return s;
		}
		return 'major';
	}

	function cardBadge(card: TarotCardInfo): string {
		if (card.arcana === 'major_arcana') {
			const idx = MAJOR_ARCANA.indexOf(card.card);
			return `${idx >= 0 ? ROMAN[idx] : ''} • Major`.trim();
		}
		const parts = card.card.split('_of_');
		if (parts.length === 2) return `${capitalize(parts[0])} • ${capitalize(parts[1])}`;
		return card.name;
	}

	const SUIT_ELEMENT: Record<string, { label: string; icon: string; text: string; bg: string }> = {
		wands: { label: 'Fire', icon: 'local_fire_department', text: 'text-fire', bg: 'bg-fire/15' },
		cups: { label: 'Water', icon: 'water_drop', text: 'text-water', bg: 'bg-water/15' },
		swords: { label: 'Air', icon: 'air', text: 'text-air', bg: 'bg-air/15' },
		pentacles: { label: 'Earth', icon: 'public', text: 'text-earth', bg: 'bg-earth/15' },
		major: { label: 'Spirit', icon: 'auto_awesome', text: 'text-secondary', bg: 'bg-secondary/15' },
	};

	function elementOf(card: TarotCardInfo) {
		return SUIT_ELEMENT[cardSuit(card)];
	}
</script>

<svelte:head>
	<title>Tarot Deck - AstroLogic</title>
</svelte:head>

<div class="page-container pt-24">
	<div class="flex flex-col lg:flex-row items-start lg:items-end justify-between gap-6 mb-8">
		<div class="flex flex-col gap-2 max-w-2xl">
			<div class="flex items-center gap-2">
				<span class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-surface-container-high text-secondary text-[10px] font-mono-data tracking-wider uppercase">
					<span class="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
					78-Card Archive
				</span>
				<span class="font-mono-data text-xs text-outline">{cards.length || 78} cards indexed</span>
			</div>
			<h1 class="font-headline text-3xl md:text-4xl font-semibold text-on-surface tracking-tight">
				The Tarot <span class="gradient-text">Deck</span>
			</h1>
			<p class="text-on-surface-variant">
				Explore the complete 78-card tarot deck with upright and reversed meanings, elemental
				dignities, and keyword archetypes.
			</p>
		</div>
		<div class="flex items-center gap-3 w-full lg:w-auto">
			<div class="relative flex-1 lg:w-72">
				<span class="material-symbols-outlined absolute left-3 top-2.5 text-outline text-lg pointer-events-none">search</span>
				<input
					class="input-field w-full pl-9"
					placeholder="Filter by card name..."
					type="text"
					bind:value={search}
				/>
			</div>
		</div>
	</div>

	<div class="flex items-center gap-2 overflow-x-auto pb-2 mb-8">
		{#each suits as suit}
			<button
				type="button"
				class="px-4 py-2 rounded-full text-sm font-mono-data whitespace-nowrap transition-all
					{filter === suit.id
						? 'bg-primary-container text-on-primary-container shadow-[0_0_15px_rgba(124,58,237,0.4)]'
						: 'bg-surface-container-high text-on-surface-variant hover:text-on-surface hover:bg-surface-container-highest'}"
				onclick={() => (filter = suit.id)}
			>
				{suit.label}
			</button>
		{/each}
	</div>

	{#if loading}
		<LoadingSpinner text="Loading tarot deck..." />
	{:else if !filtered.length}
		<div class="glass-card p-10 text-center text-on-surface-variant">No cards match this filter.</div>
	{:else}
		{#if selectedCard}
			{@const el = elementOf(selectedCard)}
			<div class="grid grid-cols-1 xl:grid-cols-12 gap-6 mb-12 items-stretch">
				<div class="xl:col-span-4 flex flex-col items-center justify-center p-8 rounded-xl bg-surface-container-lowest/70 relative overflow-hidden shadow-2xl">
					<div class="absolute -top-16 -left-16 w-56 h-56 rounded-full bg-primary-container/20 blur-3xl pointer-events-none"></div>
					<div class="absolute -bottom-16 -right-16 w-56 h-56 rounded-full bg-secondary/20 blur-3xl pointer-events-none"></div>
					<div class="relative w-56">
						<TarotCard card={{ ...selectedCard, position: '' }} revealed={true} />
					</div>
				</div>

				<div class="xl:col-span-8 flex flex-col justify-between gap-6 p-8 rounded-xl bg-surface-container-low/70 shadow-xl">
					<div class="flex flex-col gap-6">
						<div class="flex flex-wrap items-center justify-between gap-4">
							<span class="font-mono-data text-xs text-secondary tracking-widest uppercase">{cardBadge(selectedCard)} Arcana</span>
							<span class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full {el.bg} {el.text} text-[10px] font-mono-data uppercase">
								<span class="material-symbols-outlined text-xs">{el.icon}</span>
								{el.label} Dignity
							</span>
						</div>
						<div class="flex flex-col gap-2">
							<h2 class="font-headline text-2xl md:text-3xl text-on-surface">{selectedCard.name}</h2>
							{#if selectedCard.themes?.length}
								<p class="font-mono-data text-sm text-secondary">{selectedCard.themes.join(' • ')}</p>
							{/if}
						</div>

						<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
							<div class="p-4 rounded-lg bg-surface-container-lowest/60">
								<div class="flex items-center gap-2 text-secondary mb-2 text-xs font-mono-data uppercase tracking-wider">
									<span class="material-symbols-outlined text-sm">north</span> Upright
								</div>
								<div class="flex flex-wrap gap-1.5">
									{#each (selectedCard.upright?.length ? selectedCard.upright : selectedCard.keywords) as kw}
										<span class="px-2.5 py-1 rounded-full bg-surface-container text-on-surface text-xs">{kw}</span>
									{/each}
								</div>
							</div>
							<div class="p-4 rounded-lg bg-surface-container-lowest/60">
								<div class="flex items-center gap-2 text-error mb-2 text-xs font-mono-data uppercase tracking-wider">
									<span class="material-symbols-outlined text-sm">south</span> Reversed
								</div>
								<div class="flex flex-wrap gap-1.5">
									{#each (selectedCard.reversed?.length ? selectedCard.reversed : selectedCard.keywords) as kw}
										<span class="px-2.5 py-1 rounded-full bg-surface-container text-on-surface text-xs">{kw}</span>
									{/each}
								</div>
							</div>
						</div>
					</div>

					<div class="flex items-center justify-between pt-6 border-t border-outline-variant/30">
						<div class="flex items-center gap-2">
							<span class="w-2 h-2 rounded-full bg-secondary animate-ping"></span>
							<span class="text-xs font-mono-data text-outline">Card detail synced</span>
						</div>
						<a href="/reading" class="btn-primary inline-flex items-center gap-2">
							<span class="material-symbols-outlined text-sm">auto_awesome</span>
							Use in a Reading
						</a>
					</div>
				</div>
			</div>
		{/if}

		<div class="flex items-center justify-between mb-6">
			<div class="flex items-center gap-3">
				<h3 class="font-headline text-lg text-on-surface">Card Gallery</h3>
				<span class="px-2.5 py-0.5 rounded-full bg-surface-container-high text-on-surface-variant text-[10px] font-mono-data">
					Displaying {filtered.length} {filtered.length === 1 ? 'card' : 'cards'}
				</span>
			</div>
			<span class="text-xs font-mono-data text-outline hidden sm:block">Select a card to inspect</span>
		</div>

		<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
			{#each filtered as card (card.card)}
				{@const el = elementOf(card)}
				<button
					type="button"
					onclick={() => selectCard(card)}
					class="group relative flex flex-col p-3 rounded-xl text-left transition-all duration-300 hover:-translate-y-1.5
						{selectedCard === card
							? 'bg-surface-container-high shadow-[0_12px_32px_rgba(124,58,237,0.3)]'
							: 'bg-surface-container-lowest/80 hover:shadow-[0_12px_32px_rgba(124,58,237,0.2)]'}"
				>
					<div class="relative w-full aspect-[2/3] rounded-lg overflow-hidden mb-3 bg-gradient-to-br from-surface-container-high to-surface-container flex items-center justify-center">
						{#if card.image}
							<img
								src={card.image}
								alt={card.name}
								class="absolute inset-0 h-full w-full object-cover"
								loading="lazy"
								onerror={(e) => ((e.currentTarget as HTMLImageElement).style.display = 'none')}
							/>
						{:else}
							<span class="material-symbols-outlined text-4xl {el.text} opacity-80">{el.icon}</span>
						{/if}
						<span class="absolute top-2 left-2 px-2 py-0.5 rounded bg-surface-container-lowest/90 text-secondary text-[9px] font-mono-data uppercase tracking-wider">
							{cardBadge(card)}
						</span>
						<span class="absolute top-2 right-2 px-2 py-0.5 rounded {el.bg} {el.text} text-[9px] font-mono-data">
							{el.label}
						</span>
					</div>
					<div class="flex flex-col flex-grow justify-between">
						<h4 class="font-headline text-sm text-on-surface group-hover:text-primary transition-colors line-clamp-1">
							{card.name}
						</h4>
						<p class="text-[11px] text-on-surface-variant capitalize mb-2">{card.arcana?.replace('_', ' ')}</p>
						<div class="pt-1 flex items-center justify-between">
							<span class="text-[10px] font-mono-data text-outline">{card.keywords?.[0] ?? ''}</span>
							<span class="flex items-center gap-1 text-secondary group-hover:text-primary text-[10px] font-mono-data transition-colors">
								Inspect
								<span class="material-symbols-outlined text-xs">arrow_forward</span>
							</span>
						</div>
					</div>
				</button>
			{/each}
		</div>
	{/if}
</div>
