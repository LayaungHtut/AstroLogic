<script lang="ts">
	import { onMount } from 'svelte';
	import { fetchAllTarotCards } from '$lib/utils/api';
	import { cardImage } from '$lib/utils/image';
	import type { TarotCardInfo } from '$lib/types';
	import TarotCard from '$lib/components/TarotCard.svelte';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import { locale, t, getCardTranslation, translateKeyword, formatElement } from '$lib/i18n';

	let cards = $state<TarotCardInfo[]>([]);
	let filter = $state('all');
	let search = $state('');
	let loading = $state(true);
	let selectedCard = $state<TarotCardInfo | null>(null);
	let loadError = $state('');

	onMount(async () => {
		try {
			cards = await fetchAllTarotCards();
		} catch (e) {
			loadError =
				e instanceof Error
					? `Couldn't reach the tarot API: ${e.message}`
					: "Couldn't reach the tarot API.";
		} finally {
			loading = false;
		}
	});

	function cardSuit(card: TarotCardInfo): 'wands' | 'cups' | 'swords' | 'pentacles' | 'major' {
		if (card.arcana === 'major' || card.arcana === 'major_arcana') return 'major';
		if (card.suit) {
			const s = card.suit.toLowerCase();
			if (s === 'wands' || s === 'cups' || s === 'swords' || s === 'pentacles') return s;
		}
		const nameLower = card.name.toLowerCase();
		if (nameLower.includes('wand')) return 'wands';
		if (nameLower.includes('cup')) return 'cups';
		if (nameLower.includes('sword')) return 'swords';
		if (nameLower.includes('pentacle') || nameLower.includes('coin')) return 'pentacles';
		const code = (card.card || '').toLowerCase();
		if (code.startsWith('ar')) return 'major';
		if (code.startsWith('wa')) return 'wands';
		if (code.startsWith('cu')) return 'cups';
		if (code.startsWith('sw')) return 'swords';
		if (code.startsWith('pe')) return 'pentacles';
		return 'major';
	}

	const filtered = $derived(
		(filter === 'all'
			? cards
			: cards.filter((c) => cardSuit(c) === filter)
		).filter((c) => {
			if (!search) return true;
			const q = search.toLowerCase();
			const trans = getCardTranslation(c.name, $locale);
			return (
				c.name.toLowerCase().includes(q) ||
				trans.name.toLowerCase().includes(q) ||
				(c.keywords && c.keywords.some((k) => k.toLowerCase().includes(q)))
			);
		})
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

	const suits = $derived([
		{ id: 'all', label: $locale === 'my' ? 'ကတ်အားလုံး (၇၈ ကတ်)' : 'All Cards' },
		{ id: 'major', label: $locale === 'my' ? 'မေဂျာအာခါနာ (၂၂ ကတ်)' : 'Major Arcana' },
		{ id: 'wands', label: $locale === 'my' ? 'တုတ်ချောင်း (မီးဓာတ်)' : 'Wands (Fire)' },
		{ id: 'cups', label: $locale === 'my' ? 'ခွက် (ရေဓာတ်)' : 'Cups (Water)' },
		{ id: 'swords', label: $locale === 'my' ? 'ဓား (လေဓာတ်)' : 'Swords (Air)' },
		{ id: 'pentacles', label: $locale === 'my' ? 'ဒင်္ဂါး (မြေဓာတ်)' : 'Pentacles (Earth)' },
	]);

	function capitalize(s: string) {
		return s.charAt(0).toUpperCase() + s.slice(1);
	}

	function cardBadge(card: TarotCardInfo): string {
		const suit = cardSuit(card);
		if (suit === 'major') {
			const trans = getCardTranslation(card.name, $locale);
			return trans.arcana || ($locale === 'my' ? 'မေဂျာအာခါနာ' : 'Major Arcana');
		}
		const trans = getCardTranslation(card.name, $locale);
		return trans.suit || capitalize(suit);
	}

	const SUIT_ELEMENT: Record<string, { label: string; icon: string; text: string; bg: string }> = {
		wands: { label: 'Fire', icon: 'local_fire_department', text: 'text-fire', bg: 'bg-fire/15' },
		cups: { label: 'Water', icon: 'water_drop', text: 'text-water', bg: 'bg-water/15' },
		swords: { label: 'Air', icon: 'air', text: 'text-air', bg: 'bg-air/15' },
		pentacles: { label: 'Earth', icon: 'public', text: 'text-earth', bg: 'bg-earth/15' },
		major: { label: 'Spirit', icon: 'auto_awesome', text: 'text-secondary', bg: 'bg-secondary/15' },
	};

	function elementOf(card: TarotCardInfo) {
		const base = SUIT_ELEMENT[cardSuit(card)];
		return {
			...base,
			localizedLabel: formatElement(base.label.toLowerCase(), $locale)
		};
	}
</script>

<svelte:head>
	<title>{$t('deck.title')} - {$t('brand.name')}</title>
</svelte:head>

<div class="page-container pt-24">
	<div class="flex flex-col lg:flex-row items-start lg:items-end justify-between gap-6 mb-8">
		<div class="flex flex-col gap-2 max-w-2xl">
			<div class="flex items-center gap-2">
				<span class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-surface-container-high text-secondary text-[10px] font-mono-data tracking-wider uppercase">
					<span class="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
					{$locale === 'my' ? 'တားရော့ကတ် ၇၈ ကတ် စာကြည့်တိုက်' : '78-Card Archive'}
				</span>
				<span class="font-mono-data text-xs text-outline">{cards.length || 78} {$locale === 'my' ? 'ကတ် ပါဝင်သည်' : 'cards indexed'}</span>
			</div>
			<h1 class="font-headline text-3xl md:text-4xl font-semibold text-on-surface tracking-tight">
				{$t('deck.title')}
			</h1>
			<p class="text-on-surface-variant">
				{$t('deck.subtitle')}
			</p>
		</div>
		<div class="flex items-center gap-3 w-full lg:w-auto">
			<div class="relative flex-1 lg:w-72">
				<span class="material-symbols-outlined absolute left-3 top-2.5 text-outline text-lg pointer-events-none">search</span>
				<input
					id="tarot-search"
					name="tarot-search"
					class="input-field w-full pl-9"
					placeholder={$t('deck.searchPlaceholder')}
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
						? 'bg-primary-container text-on-primary-container shadow-[0_0_15px_rgba(124,58,237,0.4)] font-semibold'
						: 'bg-surface-container-high text-on-surface-variant hover:text-on-surface hover:bg-surface-container-highest'}"
				onclick={() => (filter = suit.id)}
			>
				{suit.label}
			</button>
		{/each}
	</div>

	{#if loading}
		<LoadingSpinner text={$t('common.loading')} />
	{:else if loadError}
		<div class="glass-card p-10 text-center text-error">{loadError}</div>
	{:else if !filtered.length}
		<div class="glass-card p-10 text-center text-on-surface-variant">
			{$locale === 'my' ? 'မည်သည့်ကတ်မှ မတွေ့ရှိပါ' : 'No cards match this filter.'}
		</div>
	{:else}
		{#if selectedCard}
			{@const el = elementOf(selectedCard)}
			{@const selTrans = getCardTranslation(selectedCard.name, $locale)}
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
							<span class="font-mono-data text-xs text-secondary tracking-widest uppercase">{cardBadge(selectedCard)}</span>
							<span class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full {el.bg} {el.text} text-[10px] font-mono-data uppercase">
								<span class="material-symbols-outlined text-xs">{el.icon}</span>
								{el.localizedLabel}
							</span>
						</div>
						<div class="flex flex-col gap-2">
							<h2 class="font-headline text-2xl md:text-3xl text-on-surface">
								{selTrans.name || selectedCard.name}
							</h2>
							{#if $locale === 'my' && selTrans.name !== selectedCard.name}
								<p class="font-mono-data text-xs text-on-surface-variant/80 italic">{selectedCard.name}</p>
							{/if}
						</div>

						<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
							<div class="p-4 rounded-lg bg-surface-container-lowest/60 flex flex-col gap-3">
								<div class="flex items-center gap-2 text-secondary text-xs font-mono-data uppercase tracking-wider font-semibold">
									<span class="material-symbols-outlined text-sm">north</span> {$t('deck.uprightKeywords')}
								</div>
								<div class="flex flex-wrap gap-1.5">
									{#each (selTrans.keywords.length ? selTrans.keywords : (selectedCard.upright?.length ? selectedCard.upright : selectedCard.keywords)) as kw}
										<span class="px-2.5 py-1 rounded-full bg-surface-container text-on-surface text-xs">{translateKeyword(kw, $locale)}</span>
									{/each}
								</div>
								{#if selTrans.meaningUpright}
									<p class="text-xs text-on-surface-variant/90 leading-relaxed border-t border-white/5 pt-2">
										{selTrans.meaningUpright}
									</p>
								{/if}
							</div>
							<div class="p-4 rounded-lg bg-surface-container-lowest/60 flex flex-col gap-3">
								<div class="flex items-center gap-2 text-error text-xs font-mono-data uppercase tracking-wider font-semibold">
									<span class="material-symbols-outlined text-sm">south</span> {$t('deck.reversedKeywords')}
								</div>
								<div class="flex flex-wrap gap-1.5">
									{#each (selectedCard.reversed?.length ? selectedCard.reversed : (selTrans.keywords.length ? selTrans.keywords : selectedCard.keywords)) as kw}
										<span class="px-2.5 py-1 rounded-full bg-surface-container text-on-surface text-xs">{translateKeyword(kw, $locale)}</span>
									{/each}
								</div>
								{#if selTrans.meaningReversed}
									<p class="text-xs text-on-surface-variant/90 leading-relaxed border-t border-white/5 pt-2">
										{selTrans.meaningReversed}
									</p>
								{/if}
							</div>
						</div>
					</div>

					<div class="flex items-center justify-between pt-6 border-t border-outline-variant/30">
						<div class="flex items-center gap-2">
							<span class="w-2 h-2 rounded-full bg-secondary animate-ping"></span>
							<span class="text-xs font-mono-data text-outline">
								{$locale === 'my' ? 'ကတ်အချက်အလက် စစ်ဆေးပြီး' : 'Card detail synced'}
							</span>
						</div>
						<a href="/reading" class="btn-primary inline-flex items-center gap-2">
							<span class="material-symbols-outlined text-sm">auto_awesome</span>
							{$locale === 'my' ? 'ဗေဒင်မေးရာတွင် အသုံးပြုမည်' : 'Use in a Reading'}
						</a>
					</div>
				</div>
			</div>
		{/if}

		<div class="flex items-center justify-between mb-6">
			<div class="flex items-center gap-3">
				<h3 class="font-headline text-lg text-on-surface">
					{$locale === 'my' ? 'တားရော့ကတ်များ စုစည်းမှု' : 'Card Gallery'}
				</h3>
				<span class="px-2.5 py-0.5 rounded-full bg-surface-container-high text-on-surface-variant text-[10px] font-mono-data">
					{$locale === 'my' ? `ကတ်ပေါင်း ${filtered.length} ကတ် ပြသထားသည်` : `Displaying ${filtered.length} cards`}
				</span>
			</div>
			<span class="text-xs font-mono-data text-outline hidden sm:block">
				{$locale === 'my' ? 'အသေးစိတ်ကြည့်ရန် ကတ်ကိုနှိပ်ပါ' : 'Select a card to inspect'}
			</span>
		</div>

		<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
			{#each filtered as card (card.card)}
				{@const el = elementOf(card)}
				{@const cardTrans = getCardTranslation(card.name, $locale)}
				<button
					type="button"
					onclick={() => selectCard(card)}
					class="group relative flex flex-col p-3 rounded-xl text-left transition-all duration-300 hover:-translate-y-1.5
						{selectedCard === card
							? 'bg-surface-container-high shadow-[0_12px_32px_rgba(124,58,237,0.3)]'
							: 'bg-surface-container-lowest/80 hover:shadow-[0_12px_32px_rgba(124,58,237,0.2)]'}"
				>
					<div class="relative w-full aspect-2/3 rounded-lg overflow-hidden mb-3 bg-linear-to-br from-surface-container-high to-surface-container flex items-center justify-center">
						{#if card.image}
							<img
								src={cardImage(card.image, 220)}
								alt={cardTrans.name || card.name}
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
							{el.localizedLabel}
						</span>
					</div>
					<div class="flex flex-col grow justify-between">
						<h4 class="font-headline text-sm text-on-surface group-hover:text-primary transition-colors line-clamp-1">
							{cardTrans.name || card.name}
						</h4>
						<p class="text-[11px] text-on-surface-variant capitalize mb-2">{cardTrans.arcana || card.arcana}</p>
						<div class="pt-1 flex items-center justify-between">
							<span class="text-[10px] font-mono-data text-outline truncate max-w-[90px]">
								{cardTrans.keywords?.[0] || card.keywords?.[0] || ''}
							</span>
							<span class="flex items-center gap-1 text-secondary group-hover:text-primary text-[10px] font-mono-data transition-colors">
								{$locale === 'my' ? 'ကြည့်မည်' : 'Inspect'}
								<span class="material-symbols-outlined text-xs">arrow_forward</span>
							</span>
						</div>
					</div>
				</button>
			{/each}
		</div>
	{/if}
</div>
