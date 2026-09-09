<script lang="ts">
	import type { DrawnCard } from '$lib/types';
	import { cardImage } from '$lib/utils/image';
	import { locale, t, getCardTranslation, translatePosition, translateKeyword } from '$lib/i18n';

	let { card, index = 0, revealed = true }: { card: DrawnCard; index?: number; revealed?: boolean } = $props();
	let isFlipped = $state(false);
	let imageFailed = $state(false);

	const CARD_BACK_URL = cardImage('https://sixseeds.github.io/tarot-api/cards/back.jpg', 320);

	$effect(() => {
		isFlipped = !revealed;
	});

	function toggleFlip() {
		isFlipped = !isFlipped;
	}

	const majorArcana = [
		'the_fool', 'the_magician', 'the_high_priestess', 'the_empress',
		'the_emperor', 'the_hierophant', 'the_lovers', 'the_chariot',
		'strength', 'the_hermit', 'wheel_of_fortune', 'justice',
		'the_hanged_man', 'death', 'temperance', 'the_devil',
		'the_tower', 'the_star', 'the_moon', 'the_sun',
		'judgement', 'the_world'
	];

	const isMajor = $derived(majorArcana.includes(card.card));
	const suitColor = $derived(
		card.card.includes('wands') ? 'from-orange-500 to-red-600' :
		card.card.includes('cups') ? 'from-blue-400 to-cyan-600' :
		card.card.includes('swords') ? 'from-slate-400 to-indigo-600' :
		card.card.includes('pentacles') ? 'from-amber-500 to-yellow-700' :
		'from-purple-500 to-indigo-700'
	);

	const cardInfo = $derived(getCardTranslation(card.name || card.card, $locale));
	const localizedName = $derived(cardInfo.name || card.name);
	const localizedPosition = $derived(translatePosition(card.position, $locale));
	const localizedKeywords = $derived(
		card.keywords && card.keywords.length > 0
			? card.keywords.slice(0, 3).map(kw => translateKeyword(kw, $locale))
			: cardInfo.keywords.slice(0, 3)
	);
</script>

<button
	type="button"
	class="tarot-card group relative block w-full cursor-pointer text-left"
	style:animation-delay="{index * 150}ms"
	onclick={toggleFlip}
	aria-pressed={isFlipped}
	aria-label={`${isFlipped ? 'Reveal' : 'Hide'} ${localizedName}`}
>
	<div class:flipped={isFlipped} class="tarot-card__inner">
		<div class="card-face card-back w-full aspect-2/3 rounded-xl overflow-hidden border border-purple-500/30 shadow-lg shadow-purple-500/20">
			<img src={CARD_BACK_URL} alt="Tarot card back" class="h-full w-full object-cover" loading="lazy" />
		</div>
		<div class="card-face card-front relative w-full aspect-2/3 rounded-xl overflow-hidden border border-white/20 shadow-lg group-hover:shadow-xl {imageFailed || !card.image ? `bg-linear-to-br ${suitColor}` : 'bg-black'}">
			{#if card.image && !imageFailed}
				<img
					src={cardImage(card.image, 400)}
					alt={localizedName}
					class="absolute inset-0 h-full w-full object-cover {card.is_reversed ? 'rotate-180' : ''}"
					loading="lazy"
					onerror={() => (imageFailed = true)}
				/>
				<div class="absolute inset-x-0 bottom-0 bg-linear-to-t from-black/90 via-black/60 to-transparent px-2 pb-2 pt-6">
					<div class="text-[11px] font-semibold text-white text-center truncate mb-1 drop-shadow-md">
						{localizedName}
					</div>
					<div class="flex flex-wrap gap-1 justify-center">
						{#each localizedKeywords as keyword}
							<span class="text-[9px] bg-white/20 rounded px-1.5 py-0.5 backdrop-blur-sm text-white/95">{keyword}</span>
						{/each}
					</div>
				</div>
				{#if localizedPosition}
					<div class="absolute top-1.5 left-1.5 right-1.5 text-[10px] font-medium text-white/90 uppercase tracking-wider text-center drop-shadow">{localizedPosition}</div>
				{/if}
			{:else}
				<div class="flex h-full w-full flex-col items-center justify-between p-4">
					<div class={card.is_reversed ? 'rotate-180 flex h-full w-full flex-col items-center justify-between' : 'flex h-full w-full flex-col items-center justify-between'}>
						<div class="text-xs font-medium opacity-70 uppercase tracking-wider">{localizedPosition}</div>
						<div class="text-center">
							<div class="text-3xl mb-2">
								{#if isMajor}⭐{:else if card.card.includes('wands')}🔥{:else if card.card.includes('cups')}🏆{:else if card.card.includes('swords')}⚔️{:else}💰{/if}
							</div>
							<div class="font-bold text-sm text-white drop-shadow-lg">{localizedName}</div>
						</div>
						<div class="flex flex-wrap gap-1 justify-center">
							{#each localizedKeywords as keyword}
								<span class="text-[9px] bg-white/20 rounded px-1.5 py-0.5 backdrop-blur-sm">{keyword}</span>
							{/each}
						</div>
					</div>
				</div>
			{/if}
			{#if card.is_reversed}
				<div class="absolute top-2 right-2 text-[10px] bg-red-500/85 backdrop-blur-sm rounded px-1.5 py-0.5 font-bold text-white z-10 shadow-sm">
					{$t('common.reversed')}
				</div>
			{/if}
		</div>
	</div>
</button>

<style>
	.tarot-card {
		perspective: 1000px;
		animation: cardAppear 0.5s ease-out both;
	}

	.tarot-card__inner {
		display: grid;
		transform-style: preserve-3d;
		transition: transform 600ms cubic-bezier(0.22, 1, 0.36, 1);
	}

	.tarot-card__inner.flipped {
		transform: rotateY(180deg);
	}

	.card-face {
		grid-area: 1 / 1;
		backface-visibility: hidden;
		-webkit-backface-visibility: hidden;
	}

	.card-back {
		transform: rotateY(180deg);
	}

	.tarot-card:focus-visible {
		outline: 2px solid rgb(216 180 254);
		outline-offset: 4px;
	}

	@keyframes cardAppear {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.tarot-card,
		.tarot-card__inner {
			animation: none;
			transition-duration: 1ms;
		}
	}
</style>
