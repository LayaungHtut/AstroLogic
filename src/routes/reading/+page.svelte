<script lang="ts">
	import { profile } from '$lib/stores';
	import { analyzeReading, analyzeSelectedReading, saveReading } from '$lib/utils/api';
	import { SPREAD_TYPES, CUSTOM_DRAW_MIN, CUSTOM_DRAW_MAX } from '$lib/types';
	import type { ReadingResult } from '$lib/types';
	import TarotCard from '$lib/components/TarotCard.svelte';
	import ReasoningStep from '$lib/components/ReasoningStep.svelte';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import MarkdownText from '$lib/components/MarkdownText.svelte';
	import CardPicker from '$lib/components/CardPicker.svelte';

	let question = $state('');
	let drawMethod = $state<'random' | 'manual'>('random');
	let selectedSpread = $state('three_card');
	let customCardCount = $state(7);
	let manualSelection = $state<{ name: string; is_reversed: boolean }[]>([]);
	let selectedTopic = $state('general');
	let reading = $state<ReadingResult | null>(null);
	let loading = $state(false);
	let loadingText = $state('');
	let error = $state('');
	let showReasoning = $state(true);

	const currentProfile = $derived($profile);

	const topics = [
		{ id: 'love', label: 'Love', icon: '❤️', color: 'from-pink-500 to-rose-600' },
		{ id: 'career', label: 'Career', icon: '💼', color: 'from-blue-500 to-indigo-600' },
		{ id: 'finance', label: 'Finance', icon: '💰', color: 'from-green-500 to-emerald-600' },
		{ id: 'personal_growth', label: 'Growth', icon: '🌱', color: 'from-amber-500 to-orange-600' },
		{ id: 'communication', label: 'Communication', icon: '🗣️', color: 'from-cyan-500 to-teal-600' },
		{ id: 'general', label: 'General', icon: '✨', color: 'from-purple-500 to-violet-600' }
	];

	const topicSpreadMap: Record<string, string> = {
		love: 'relationship',
		career: 'career',
		finance: 'decision',
		personal_growth: 'self_reflection',
		communication: 'three_card',
		general: 'three_card'
	};

	function selectTopic(topicId: string) {
		selectedTopic = topicId;
		selectedSpread = topicSpreadMap[topicId] || 'three_card';
	}

	const canBeginReading = $derived(
		Boolean(question.trim()) && (drawMethod === 'random' || manualSelection.length > 0)
	);

	async function startReading() {
		if (!canBeginReading) return;

		loading = true;
		error = '';
		reading = null;
		showReasoning = false;

		const steps =
			drawMethod === 'manual'
				? [
						'Analyzing your question...',
						'Consulting symbolic knowledge...',
						'Reading your chosen cards...',
						'Preparing your interpretation...'
					]
				: [
						'Analyzing your question...',
						'Consulting symbolic knowledge...',
						'Drawing your cards...',
						'Preparing your interpretation...'
					];

		let step = 0;
		const stepInterval = setInterval(() => {
			step = (step + 1) % steps.length;
			loadingText = steps[step];
		}, 2000);

		try {
			if (drawMethod === 'manual') {
				const result = await analyzeSelectedReading(
					question,
					currentProfile.zodiac_sign,
					manualSelection,
				);
				if (result.error) {
					throw new Error(result.error);
				}
				reading = result;
			} else {
				reading = await analyzeReading(
					question,
					currentProfile.zodiac_sign,
					selectedSpread,
					selectedSpread === 'custom' ? customCardCount : undefined,
				);
			}

			await saveReading({
				question: reading.question,
				category: reading.category,
				zodiac_sign: reading.zodiac_sign,
				spread_type: reading.spread_type,
				cards: reading.cards,
				orientations: reading.cards.map((c) => c.is_reversed),
				themes: reading.themes,
				reasoning: reading.reasoning,
				ai_interpretation: reading.ai_interpretation
			});
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to generate reading';
		} finally {
			clearInterval(stepInterval);
			loading = false;
			loadingText = '';
		}
	}

	function resetReading() {
		reading = null;
		question = '';
		error = '';
		showReasoning = true;
		manualSelection = [];
	}
</script>

<svelte:head>
	<title>Tarot Reading - AstroLogic</title>
</svelte:head>

<div class="page-container">
	<div class="relative w-full overflow-hidden">
		<div
			class="pointer-events-none absolute -top-24 left-1/4 -z-10 h-96 w-96 rounded-full bg-primary-container/20 blur-3xl"
		></div>
		<div
			class="pointer-events-none absolute top-1/3 right-10 -z-10 h-80 w-80 rounded-full bg-secondary/10 blur-3xl"
		></div>

		<div class="mb-10 flex flex-col justify-between gap-6 md:flex-row md:items-end">
			<div class="flex flex-col gap-2">
				<div
					class="inline-flex w-max items-center gap-2 rounded-full bg-surface-container-high px-3 py-1"
				>
					<span class="h-1.5 w-1.5 animate-pulse rounded-full bg-secondary"></span>
					<span class="font-mono-data text-[10px] tracking-widest text-secondary uppercase"
						>Autonomous Divination Array</span
					>
				</div>
				<h1 class="font-headline text-3xl font-semibold tracking-tight text-on-surface md:text-4xl">
					Tarot Reading <span class="gradient-text">Matrix</span>
				</h1>
				<p class="max-w-xl text-on-surface-variant">
					Harnessing symbolic logic engines and cosmic archetypal harmonics to synthesize your
					divination.
				</p>
			</div>
			{#if currentProfile?.zodiac_sign}
				<div
					class="flex items-center gap-4 rounded-xl bg-surface-container-low/90 px-4 py-3 shadow-md backdrop-blur-md"
				>
					<div class="flex flex-col">
						<span class="font-mono-data text-[10px] text-on-surface-variant uppercase"
							>Seeker Sign</span
						>
						<span class="font-mono-data text-sm font-medium text-primary"
							>{currentProfile.zodiac_sign}</span
						>
					</div>
					<div class="h-8 w-px bg-surface-variant"></div>
					<div class="flex flex-col">
						<span class="font-mono-data text-[10px] text-on-surface-variant uppercase"
							>Selected Array</span
						>
						<span class="font-mono-data text-sm font-medium text-secondary"
							>{selectedSpread.replace(/_/g, ' ')}</span
						>
					</div>
				</div>
			{/if}
		</div>

		{#if !reading}
			<div class="grid grid-cols-1 items-start gap-8 xl:grid-cols-12">
				<!-- LEFT COLUMN: Workflow controller -->
				<div class="flex flex-col gap-6 xl:col-span-5">
					<div
						class="flex flex-col gap-7 rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-xl sm:p-7"
					>
						<!-- STEP 1: Cosmic Query -->
						<div class="flex flex-col gap-3">
							<div class="flex items-center justify-between">
								<div class="flex items-center gap-2">
									<span
										class="font-mono-data flex h-5 w-5 items-center justify-center rounded-full bg-primary/20 text-[11px] font-semibold text-primary"
										>1</span
									>
									<label
										class="font-headline text-base font-semibold text-on-surface"
										for="cosmic-query">Cosmic Query</label
									>
								</div>
								<span
									class="font-mono-data text-[11px] font-medium tracking-tight {question.length >=
									480
										? 'text-error'
										: 'text-primary'}">{question.length}/500</span
								>
							</div>
							<div class="group relative">
								<textarea
									id="cosmic-query"
									bind:value={question}
									class="min-h-25 w-full resize-none rounded-xl bg-surface-container-high/40 p-4 text-sm text-on-surface transition-all duration-300 placeholder:text-outline/60 focus:ring-2 focus:ring-secondary/40 focus:outline-none"
									maxlength="500"
									placeholder="What celestial guidance do you seek from the arcana?"></textarea>
								<div
									class="pointer-events-none absolute right-3 bottom-3 flex items-center gap-1 opacity-50"
								>
									<span class="material-symbols-outlined text-[16px] text-secondary">tune</span>
								</div>
							</div>
						</div>

						<!-- STEP 2: Topic Selector Pills -->
						<div class="flex flex-col gap-3">
							<div class="flex items-center justify-between">
								<div class="flex items-center gap-2">
									<span
										class="font-mono-data flex h-5 w-5 items-center justify-center rounded-full bg-primary/20 text-[11px] font-semibold text-primary"
										>2</span
									>
									<span class="font-headline text-base font-semibold text-on-surface"
										>Divination Plane</span
									>
								</div>
							</div>
							<div class="flex flex-wrap gap-2" role="radiogroup" aria-label="Reading topic">
								{#each topics as topic}
									<button
										type="button"
										class="font-mono-data flex items-center gap-1.5 rounded-full px-3 py-1.5 text-[11px] font-medium transition-all
											{selectedTopic === topic.id
											? 'bg-primary-container text-on-primary-container shadow-sm'
											: 'bg-surface-container text-on-surface-variant hover:bg-surface-bright hover:text-on-surface'}"
										onclick={() => selectTopic(topic.id)}
									>
										<span>{topic.icon}</span>
										<span>{topic.label}</span>
									</button>
								{/each}
							</div>
						</div>

						<!-- STEP 3: Draw Method -->
						<div class="flex flex-col gap-3">
							<div class="flex items-center gap-2">
								<span
									class="font-mono-data flex h-5 w-5 items-center justify-center rounded-full bg-primary/20 text-[11px] font-semibold text-primary"
									>3</span
								>
								<span class="font-headline text-base font-semibold text-on-surface">Draw Method</span
								>
							</div>
							<div class="grid grid-cols-2 gap-2.5" role="radiogroup" aria-label="Card draw method">
								<button
									type="button"
									class="flex flex-col items-start gap-1 rounded-xl p-3 text-left transition-all
										{drawMethod === 'random'
										? 'bg-primary-container/20 text-on-surface shadow-md'
										: 'bg-surface-container/60 text-on-surface-variant hover:bg-surface-container-high'}"
									onclick={() => (drawMethod = 'random')}
								>
									<span class="flex items-center gap-1.5 text-sm font-semibold text-on-surface">
										<span class="material-symbols-outlined text-base">cyclone</span>
										Random Draw
									</span>
									<span class="text-xs {drawMethod === 'random' ? 'text-primary' : 'text-on-surface-variant'}"
										>Let the array choose your spread</span
									>
								</button>
								<button
									type="button"
									class="flex flex-col items-start gap-1 rounded-xl p-3 text-left transition-all
										{drawMethod === 'manual'
										? 'bg-primary-container/20 text-on-surface shadow-md'
										: 'bg-surface-container/60 text-on-surface-variant hover:bg-surface-container-high'}"
									onclick={() => (drawMethod = 'manual')}
								>
									<span class="flex items-center gap-1.5 text-sm font-semibold text-on-surface">
										<span class="material-symbols-outlined text-base">touch_app</span>
										Pick Your Own
									</span>
									<span class="text-xs {drawMethod === 'manual' ? 'text-primary' : 'text-on-surface-variant'}"
										>Choose cards straight from the deck</span
									>
								</button>
							</div>
						</div>

						{#if drawMethod === 'random'}
							<!-- STEP 4: Spread Type Selector -->
							<div class="flex flex-col gap-3">
								<div class="flex items-center justify-between">
									<div class="flex items-center gap-2">
										<span
											class="font-mono-data flex h-5 w-5 items-center justify-center rounded-full bg-primary/20 text-[11px] font-semibold text-primary"
											>4</span
										>
										<span class="font-headline text-base font-semibold text-on-surface"
											>Geometric Array</span
										>
									</div>
									<span class="font-mono-data text-[10px] tracking-wider text-secondary uppercase">
										{#if selectedSpread === 'custom'}
											{customCardCount} card{customCardCount === 1 ? '' : 's'}
										{:else}
											{SPREAD_TYPES.find((s) => s.id === selectedSpread)?.count ?? ''} card{(SPREAD_TYPES.find(
												(s) => s.id === selectedSpread
											)?.count ?? 0) === 1
												? ''
												: 's'}
										{/if}
									</span>
								</div>
								<div id="spread" class="grid grid-cols-1 gap-2.5 sm:grid-cols-2">
									{#each SPREAD_TYPES as spread}
										<button
											type="button"
											class="relative flex cursor-pointer flex-col justify-between overflow-hidden rounded-xl p-3 text-left transition-all
												{selectedSpread === spread.id
												? 'bg-primary-container/20 text-on-surface shadow-md'
												: 'bg-surface-container/60 text-on-surface-variant hover:bg-surface-container-high'}"
											onclick={() => (selectedSpread = spread.id)}
										>
											{#if selectedSpread === spread.id}
												<div
													class="pointer-events-none absolute -right-6 -bottom-6 h-16 w-16 rounded-full bg-primary/20 blur-xl"
												></div>
											{/if}
											<div class="relative z-10 mb-1 flex items-start justify-between gap-2">
												<div class="flex items-center gap-1.5">
													{#if selectedSpread === spread.id}
														<span class="h-2 w-2 shrink-0 rounded-full bg-secondary shadow-sm"></span>
													{/if}
													<span class="text-sm font-semibold text-on-surface">{spread.name}</span>
												</div>
												<span class="font-mono-data shrink-0 text-[10px] text-outline"
													>{spread.id === 'custom' ? `1-${CUSTOM_DRAW_MAX}` : spread.count}</span
												>
											</div>
											<span
												class="relative z-10 text-xs {selectedSpread === spread.id
													? 'text-primary'
													: 'text-on-surface-variant'}">{spread.description}</span
											>
										</button>
									{/each}
								</div>

								{#if selectedSpread === 'custom'}
									<div class="flex flex-col gap-2 rounded-xl bg-surface-container-high/40 p-4">
										<div class="flex items-center justify-between">
											<span class="text-sm font-medium text-on-surface">Number of cards</span>
											<span class="font-mono-data text-sm font-semibold text-primary"
												>{customCardCount}</span
											>
										</div>
										<div class="flex items-center gap-3">
											<button
												type="button"
												class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-surface-container text-on-surface transition-colors hover:bg-surface-container-highest disabled:cursor-not-allowed disabled:opacity-40"
												disabled={customCardCount <= CUSTOM_DRAW_MIN}
												onclick={() => (customCardCount = Math.max(CUSTOM_DRAW_MIN, customCardCount - 1))}
												aria-label="Fewer cards"
											>
												<span class="material-symbols-outlined text-base">remove</span>
											</button>
											<input
												type="range"
												min={CUSTOM_DRAW_MIN}
												max={CUSTOM_DRAW_MAX}
												step="1"
												bind:value={customCardCount}
												class="w-full accent-primary"
												aria-label="Number of cards to draw"
											/>
											<button
												type="button"
												class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-surface-container text-on-surface transition-colors hover:bg-surface-container-highest disabled:cursor-not-allowed disabled:opacity-40"
												disabled={customCardCount >= CUSTOM_DRAW_MAX}
												onclick={() => (customCardCount = Math.min(CUSTOM_DRAW_MAX, customCardCount + 1))}
												aria-label="More cards"
											>
												<span class="material-symbols-outlined text-base">add</span>
											</button>
										</div>
										<p class="text-xs text-on-surface-variant">
											Draw {CUSTOM_DRAW_MIN}-{CUSTOM_DRAW_MAX} cards for an open reading — each one is still
											read individually by the Prolog engine, in the order you pulled them.
										</p>
									</div>
								{/if}
							</div>
						{:else}
							<!-- STEP 4: Manual Card Picker -->
							<div class="flex flex-col gap-3">
								<div class="flex items-center gap-2">
									<span
										class="font-mono-data flex h-5 w-5 items-center justify-center rounded-full bg-primary/20 text-[11px] font-semibold text-primary"
										>4</span
									>
									<span class="font-headline text-base font-semibold text-on-surface"
										>Choose Your Cards</span
									>
								</div>
								<CardPicker bind:selected={manualSelection} max={CUSTOM_DRAW_MAX} />
							</div>
						{/if}

						{#if error}
							<div class="rounded-xl border border-error/30 bg-error-container/10 p-4">
								<p class="text-sm text-error">{error}</p>
							</div>
						{/if}

						<button
							type="button"
							class="font-headline group flex w-full items-center justify-center gap-2 rounded-full bg-linear-to-r from-primary-container via-tertiary-container to-secondary-container px-6 py-3.5 text-base font-semibold tracking-wide text-on-primary shadow-lg transition-all hover:shadow-primary-container/40 disabled:cursor-not-allowed disabled:opacity-50"
							onclick={startReading}
							disabled={!canBeginReading || loading}
						>
							<span
								class="material-symbols-outlined transition-transform duration-500 group-hover:rotate-180"
								>cyclone</span
							>
							<span>{loading ? loadingText || 'Reading the arcana...' : 'Begin Reading'}</span>
						</button>
					</div>

					{#if loading}
						<div class="rounded-2xl bg-surface-container-low p-5">
							<LoadingSpinner text={loadingText} />
						</div>
					{/if}
				</div>

				<!-- RIGHT COLUMN: Idle / status panel -->
				<div class="flex flex-col gap-6 xl:col-span-7">
					<div
						class="flex min-h-95 flex-col items-center justify-center gap-4 rounded-2xl bg-surface-container-lowest/80 p-8 text-center shadow-xl backdrop-blur-xl sm:p-10"
					>
						{#if loading}
							<span class="h-2.5 w-2.5 animate-ping rounded-full bg-secondary"></span>
							<p class="font-mono-data text-sm tracking-tight text-secondary">
								{loadingText || 'Consulting the arcana...'}
							</p>
							<p class="max-w-sm text-sm text-on-surface-variant">
								The Prolog inference engine is evaluating elemental dignities and archetypal
								harmonics for your query.
							</p>
						{:else}
							<span class="material-symbols-outlined text-5xl text-outline">auto_awesome</span>
							<p class="font-headline text-lg text-on-surface">Awaiting Transmission</p>
							<p class="max-w-sm text-sm text-on-surface-variant">
								Compose your query, choose a topic and a geometric array, then begin your reading to
								reveal the drawn cards here.
							</p>
						{/if}
					</div>
				</div>
			</div>
		{:else}
			<!-- RESULTS -->
			<div class="flex flex-col gap-8">
				<div
					class="flex flex-col gap-4 rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-xl"
				>
					<div class="flex flex-wrap items-center justify-between gap-4">
						<div>
							<h2 class="font-headline text-lg font-semibold text-on-surface">Your Reading</h2>
							<p class="text-sm text-on-surface-variant">
								{reading.spread_name} Spread &middot; Classified as {reading.category?.replace(/_/g, ' ')}
								{#if reading.topic}&middot; Topic: {reading.topic.replace(/_/g, ' ')}{/if}
							</p>
						</div>
						<button type="button" class="btn-secondary text-sm" onclick={resetReading}
							>New Reading</button
						>
					</div>
					<div
						class="rounded-xl bg-surface-container-high/40 p-3 text-sm text-on-surface-variant italic"
					>
						&ldquo;{reading.question}&rdquo;
					</div>
					{#if reading.spread_rationale}
						<div class="flex items-start gap-2 rounded-xl bg-surface-container-high/30 p-3">
							<span class="material-symbols-outlined text-base text-secondary mt-0.5">lightbulb</span>
							<p class="text-xs text-on-surface-variant">{reading.spread_rationale}</p>
						</div>
					{/if}
				</div>

				<!-- ACTIVE DRAWN CARDS -->
				<div class="flex flex-col gap-4">
					<div class="flex items-center justify-between px-1">
						<div class="flex items-center gap-2">
							<span class="material-symbols-outlined text-xl text-primary">view_column</span>
							<h2 class="font-headline text-xl font-semibold text-on-surface">Active Spread</h2>
						</div>
						<span class="font-mono-data text-[11px] text-on-surface-variant"
							>{reading.cards.length} CARDS DRAWN</span
						>
					</div>
					<div class="grid grid-cols-2 gap-4 perspective-[1000px] md:grid-cols-4">
						{#each reading.cards as card, i (card.card + i)}
							<div class="flex flex-col gap-2">
								<TarotCard {card} index={i} />
								<div class="text-center">
									<div class="font-mono-data text-xs font-medium tracking-wider text-primary">
										{card.position}
									</div>
									{#if card.ranking}
										<div
											class="mt-1 inline-flex items-center gap-1 rounded-full bg-surface-container-high px-2 py-0.5 font-mono-data text-[9px] text-on-surface-variant"
											title="Priority {card.ranking.priority}/6 — zodiac affinity: {card.ranking.zodiac_affinity_match}, category match: {card.ranking.category_match}, element match: {card.ranking.element_match}"
										>
											<span class="material-symbols-outlined text-[11px] text-secondary">military_tech</span>
											#{card.ranking.rank} of {card.ranking.eligible_pool_size} eligible
										</div>
									{/if}
								</div>
								{#if card.zodiac_affinity}
									<p class="text-center text-[11px] leading-snug text-on-surface-variant italic px-1">
										{card.zodiac_affinity.combined}
									</p>
								{/if}
							</div>
						{/each}
					</div>
				</div>

				<!-- SYNTHESIS PANEL -->
				<div
					class="relative flex flex-col gap-6 overflow-hidden rounded-2xl bg-surface-container-low/95 p-6 shadow-xl backdrop-blur-xl sm:p-8"
				>
					<div
						class="pointer-events-none absolute top-0 right-0 h-64 w-64 bg-linear-to-bl from-primary/10 via-secondary/5 to-transparent"
					></div>

					<div
						class="relative z-10 flex flex-col justify-between gap-4 sm:flex-row sm:items-center"
					>
						<div class="flex items-center gap-3">
							<div
								class="flex h-10 w-10 items-center justify-center rounded-full bg-primary-container/30 text-primary shadow-sm"
							>
								<span class="material-symbols-outlined">psychology_alt</span>
							</div>
							<div>
								<h3 class="font-headline text-lg font-semibold text-on-surface">
									Synthesized Oracle Interpretation
								</h3>
								<span class="font-mono-data text-[11px] text-on-surface-variant"
									>Harmonic Convergence Analysis</span
								>
							</div>
						</div>
						{#if reading.themes.length > 0}
							<div class="flex flex-wrap items-center gap-2">
								{#each reading.themes as theme}
									<span
										class="font-mono-data rounded-full bg-primary-container px-3 py-1 text-[10px] tracking-wider text-on-primary-container uppercase"
									>
										{theme.replace(/_/g, ' ')}
									</span>
								{/each}
							</div>
						{/if}
					</div>

					<div class="relative z-10 rounded-xl bg-surface-container-lowest/60 p-5">
						<MarkdownText content={reading.ai_interpretation} />
					</div>

					<!-- READING DIRECTION & ADVICE -->
					{#if reading.direction || reading.advice}
						<div class="relative z-10 grid grid-cols-1 gap-4 sm:grid-cols-2">
							{#if reading.direction}
								{@const directionMeta = {
									optimistic: { icon: 'trending_up', color: 'text-primary', label: 'Optimistic' },
									challenging: { icon: 'warning', color: 'text-error', label: 'Challenging' },
									reflective: { icon: 'nights_stay', color: 'text-secondary', label: 'Reflective' },
									balanced: { icon: 'balance', color: 'text-tertiary', label: 'Balanced' },
								}[reading.direction] ?? { icon: 'auto_awesome', color: 'text-secondary', label: reading.direction }}
								<div class="rounded-xl bg-surface-container-lowest/60 p-5 flex flex-col gap-1.5">
									<div class="flex items-center gap-2">
										<span class="material-symbols-outlined {directionMeta.color}">{directionMeta.icon}</span>
										<span class="font-mono-data text-[11px] uppercase tracking-wider text-on-surface-variant">Reading Direction</span>
									</div>
									<span class="font-headline text-lg {directionMeta.color}">{directionMeta.label}</span>
								</div>
							{/if}
							{#if reading.advice}
								<div class="rounded-xl bg-surface-container-lowest/60 p-5 flex flex-col gap-2">
									<div class="flex items-center gap-2">
										<span class="material-symbols-outlined text-primary">tips_and_updates</span>
										<span class="font-mono-data text-[11px] uppercase tracking-wider text-on-surface-variant">Guidance</span>
									</div>
									{#if reading.advice.category_advice}
										<p class="text-sm text-on-surface">{reading.advice.category_advice}</p>
									{/if}
									{#if reading.advice.theme_advice}
										<p class="text-sm text-on-surface-variant italic">{reading.advice.theme_advice}</p>
									{/if}
								</div>
							{/if}
						</div>
					{/if}

					<!-- THEME CONFLICT DETECTOR -->
					{#if reading.conflicts && reading.conflicts.length > 0}
						<div class="relative z-10 rounded-xl bg-surface-container-lowest/60 p-5 flex flex-col gap-3">
							<div class="flex items-center gap-2">
								<span class="material-symbols-outlined text-tertiary">compare_arrows</span>
								<span class="font-mono-data text-[11px] uppercase tracking-wider text-on-surface-variant">
									Symbolic Tension{reading.conflicts.length > 1 ? 's' : ''} Detected
								</span>
							</div>
							{#each reading.conflicts as conflict}
								<div class="rounded-lg bg-surface-container-high/40 p-3.5">
									<p class="text-sm font-semibold text-on-surface mb-1">{conflict.title}</p>
									<p class="text-xs text-on-surface-variant mb-2">
										<span class="text-primary font-medium">{conflict.card1_name}</span>
										{#if conflict.card1_position}({conflict.card1_position}){/if}
										urges <span class="italic">{conflict.theme1.replace(/_/g, ' ')}</span>
										while
										<span class="text-secondary font-medium">{conflict.card2_name}</span>
										{#if conflict.card2_position}({conflict.card2_position}){/if}
										counsels <span class="italic">{conflict.theme2.replace(/_/g, ' ')}</span>.
									</p>
									<p class="text-xs text-on-surface-variant">{conflict.description}</p>
								</div>
							{/each}
						</div>
					{/if}

					<!-- PROLOG SYMBOLIC REASONING TRACE -->
					<div
						class="relative z-10 flex flex-col overflow-hidden rounded-xl bg-surface-container-lowest/80 shadow-inner"
					>
						<button
							type="button"
							class="flex w-full cursor-pointer items-center justify-between bg-surface-container-high/60 px-5 py-3.5 text-left"
							onclick={() => (showReasoning = !showReasoning)}
						>
							<div class="flex items-center gap-2.5">
								<span
									class="h-2 w-2 rounded-full bg-secondary {loading
										? 'animate-ping'
										: 'animate-pulse'}"
								></span>
								<span class="font-mono-data text-sm font-medium tracking-tight text-secondary"
									>PROLOG LOGICAL INFERENCE ENGINE</span
								>
								<span
									class="font-mono-data rounded bg-surface-container px-2 py-0.5 text-[10px] text-outline"
									>DETERMINISTIC</span
								>
							</div>
							<span
								class="material-symbols-outlined text-[18px] text-secondary transition-transform {showReasoning
									? 'rotate-180'
									: ''}">expand_more</span
							>
						</button>

						{#if showReasoning}
							<div class="font-mono-data flex flex-col gap-4 p-5 text-xs">
								{#each reading.reasoning as step, i}
									<ReasoningStep {step} index={i} />
								{/each}
							</div>
						{/if}
					</div>
				</div>
			</div>
		{/if}
	</div>
</div>
