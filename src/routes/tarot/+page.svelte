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
		(filter === 'all' ? cards : cards.filter((c) => cardSuit(c) === filter)).filter((c) => {
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
		{ id: 'pentacles', label: $locale === 'my' ? 'ဒင်္ဂါး (မြေဓာတ်)' : 'Pentacles (Earth)' }
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
		major: { label: 'Spirit', icon: 'auto_awesome', text: 'text-secondary', bg: 'bg-secondary/15' }
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
	<div class="mb-8 flex flex-col items-start justify-between gap-6 lg:flex-row lg:items-end">
		<div class="flex max-w-2xl flex-col gap-2">
			<div class="flex items-center gap-2">
				<span
					class="font-mono-data inline-flex items-center gap-1.5 rounded-full bg-surface-container-high px-3 py-0.5 text-[10px] tracking-wider text-secondary uppercase"
				>
					<span class="h-1.5 w-1.5 animate-pulse rounded-full bg-secondary"></span>
					{$locale === 'my' ? 'တားရော့ကတ် ၇၈ ကတ် စာကြည့်တိုက်' : '78-Card Archive'}
				</span>
				<span class="font-mono-data text-xs text-outline"
					>{cards.length || 78} {$locale === 'my' ? 'ကတ် ပါဝင်သည်' : 'cards indexed'}</span
				>
			</div>
			<h1 class="font-headline text-3xl font-semibold tracking-tight text-on-surface md:text-4xl">
				{$t('deck.title')}
			</h1>
			<p class="text-on-surface-variant">
				{$t('deck.subtitle')}
			</p>
		</div>
		<div class="flex w-full items-center gap-3 lg:w-auto">
			<div class="relative flex-1 lg:w-72">
				<span
					class="material-symbols-outlined pointer-events-none absolute top-2.5 left-3 text-lg text-outline"
					>search</span
				>
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

	<div class="mb-8 flex items-center gap-2 overflow-x-auto pb-2">
		{#each suits as suit}
			<button
				type="button"
				class="font-mono-data rounded-full px-4 py-2 text-sm whitespace-nowrap transition-all
					{filter === suit.id
					? 'bg-primary-container font-semibold text-on-primary-container shadow-[0_0_15px_rgba(124,58,237,0.4)]'
					: 'bg-surface-container-high text-on-surface-variant hover:bg-surface-container-highest hover:text-on-surface'}"
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
			<div class="mb-12 grid grid-cols-1 items-stretch gap-6 xl:grid-cols-12">
				<div
					class="relative flex flex-col items-center justify-center overflow-hidden rounded-xl bg-surface-container-lowest/70 p-8 shadow-2xl xl:col-span-4"
				>
					<div
						class="pointer-events-none absolute -top-16 -left-16 h-56 w-56 rounded-full bg-primary-container/20 blur-3xl"
					></div>
					<div
						class="pointer-events-none absolute -right-16 -bottom-16 h-56 w-56 rounded-full bg-secondary/20 blur-3xl"
					></div>
					<div class="relative w-56">
						<TarotCard card={{ ...selectedCard, position: '' }} revealed={true} />
					</div>
				</div>

				<div
					class="flex flex-col justify-between gap-6 rounded-xl bg-surface-container-low/70 p-8 shadow-xl xl:col-span-8"
				>
					<div class="flex flex-col gap-6">
						<div class="flex flex-wrap items-center justify-between gap-4">
							<span class="font-mono-data text-xs tracking-widest text-secondary uppercase"
								>{cardBadge(selectedCard)}</span
							>
							<span
								class="inline-flex items-center gap-1.5 rounded-full px-3 py-0.5 {el.bg} {el.text} font-mono-data text-[10px] uppercase"
							>
								<span class="material-symbols-outlined text-xs">{el.icon}</span>
								{el.localizedLabel}
							</span>
						</div>
						<div class="flex flex-col gap-2">
							<h2 class="font-headline text-2xl text-on-surface md:text-3xl">
								{selTrans.name || selectedCard.name}
							</h2>
							{#if $locale === 'my' && selTrans.name !== selectedCard.name}
								<p class="font-mono-data text-xs text-on-surface-variant/80 italic">
									{selectedCard.name}
								</p>
							{/if}
						</div>

						<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
							<div class="flex flex-col gap-3 rounded-lg bg-surface-container-lowest/60 p-4">
								<div
									class="font-mono-data flex items-center gap-2 text-xs font-semibold tracking-wider text-secondary uppercase"
								>
									<span class="material-symbols-outlined text-sm">north</span>
									{$t('deck.uprightKeywords')}
								</div>
								<div class="flex flex-wrap gap-1.5">
									{#each selTrans.keywords.length ? selTrans.keywords : selectedCard.upright?.length ? selectedCard.upright : selectedCard.keywords as kw}
										<span
											class="rounded-full bg-surface-container px-2.5 py-1 text-xs text-on-surface"
											>{translateKeyword(kw, $locale)}</span
										>
									{/each}
								</div>
								{#if selTrans.meaningUpright}
									<p
										class="border-t border-white/5 pt-2 text-xs leading-relaxed text-on-surface-variant/90"
									>
										{selTrans.meaningUpright}
									</p>
								{/if}
							</div>
							<div class="flex flex-col gap-3 rounded-lg bg-surface-container-lowest/60 p-4">
								<div
									class="font-mono-data flex items-center gap-2 text-xs font-semibold tracking-wider text-error uppercase"
								>
									<span class="material-symbols-outlined text-sm">south</span>
									{$t('deck.reversedKeywords')}
								</div>
								<div class="flex flex-wrap gap-1.5">
									{#each selectedCard.reversed?.length ? selectedCard.reversed : selTrans.keywords.length ? selTrans.keywords : selectedCard.keywords as kw}
										<span
											class="rounded-full bg-surface-container px-2.5 py-1 text-xs text-on-surface"
											>{translateKeyword(kw, $locale)}</span
										>
									{/each}
								</div>
								{#if selTrans.meaningReversed}
									<p
										class="border-t border-white/5 pt-2 text-xs leading-relaxed text-on-surface-variant/90"
									>
										{selTrans.meaningReversed}
									</p>
								{/if}
							</div>
						</div>
					</div>

					<div class="flex items-center justify-between border-t border-outline-variant/30 pt-6">
						<div class="flex items-center gap-2">
							<span class="h-2 w-2 animate-ping rounded-full bg-secondary"></span>
							<span class="font-mono-data text-xs text-outline">
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

		<div class="mb-6 flex items-center justify-between">
			<div class="flex items-center gap-3">
				<h3 class="font-headline text-lg text-on-surface">
					{$locale === 'my' ? 'တားရော့ကတ်များ စုစည်းမှု' : 'Card Gallery'}
				</h3>
				<span
					class="font-mono-data rounded-full bg-surface-container-high px-2.5 py-0.5 text-[10px] text-on-surface-variant"
				>
					{$locale === 'my'
						? `ကတ်ပေါင်း ${filtered.length} ကတ် ပြသထားသည်`
						: `Displaying ${filtered.length} cards`}
				</span>
			</div>
			<span class="font-mono-data hidden text-xs text-outline sm:block">
				{$locale === 'my' ? 'အသေးစိတ်ကြည့်ရန် ကတ်ကိုနှိပ်ပါ' : 'Select a card to inspect'}
			</span>
		</div>

		<div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
			{#each filtered as card (card.card)}
				{@const el = elementOf(card)}
				{@const cardTrans = getCardTranslation(card.name, $locale)}
				<button
					type="button"
					onclick={() => selectCard(card)}
					class="group relative flex flex-col rounded-xl p-3 text-left transition-all duration-300 hover:-translate-y-1.5
						{selectedCard === card
						? 'bg-surface-container-high shadow-[0_12px_32px_rgba(124,58,237,0.3)]'
						: 'bg-surface-container-lowest/80 hover:shadow-[0_12px_32px_rgba(124,58,237,0.2)]'}"
				>
					<div
						class="relative mb-3 flex aspect-2/3 w-full items-center justify-center overflow-hidden rounded-lg bg-linear-to-br from-surface-container-high to-surface-container"
					>
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
						<span
							class="font-mono-data absolute top-2 left-2 rounded bg-surface-container-lowest/90 px-2 py-0.5 text-[9px] tracking-wider text-secondary uppercase"
						>
							{cardBadge(card)}
						</span>
						<span
							class="absolute top-2 right-2 rounded px-2 py-0.5 {el.bg} {el.text} font-mono-data text-[9px]"
						>
							{el.localizedLabel}
						</span>
					</div>
					<div class="flex grow flex-col justify-between">
						<h4
							class="font-headline line-clamp-1 text-sm text-on-surface transition-colors group-hover:text-primary"
						>
							{cardTrans.name || card.name}
						</h4>
						<p class="mb-2 text-[11px] text-on-surface-variant capitalize">
							{cardTrans.arcana || card.arcana}
						</p>
						<div class="flex items-center justify-between pt-1">
							<span class="font-mono-data max-w-[90px] truncate text-[10px] text-outline">
								{cardTrans.keywords?.[0] || card.keywords?.[0] || ''}
							</span>
							<span
								class="font-mono-data flex items-center gap-1 text-[10px] text-secondary transition-colors group-hover:text-primary"
							>
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
