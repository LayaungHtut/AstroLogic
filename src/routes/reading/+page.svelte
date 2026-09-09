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
	import {
		locale,
		t,
		translatePosition,
		SPREAD_TYPES_DATA,
		TOPICS_DATA,
		translateTheme,
		translateTopic,
		formatReadingSynthesis,
		formatAdviceText,
		formatResonanceNote
	} from '$lib/i18n';

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

	const topics = $derived([
		{ id: 'love', label: TOPICS_DATA.love ? ($locale === 'my' ? TOPICS_DATA.love.labelMy : TOPICS_DATA.love.labelEn) : 'Love', icon: '❤️' },
		{ id: 'career', label: TOPICS_DATA.career ? ($locale === 'my' ? TOPICS_DATA.career.labelMy : TOPICS_DATA.career.labelEn) : 'Career', icon: '💼' },
		{ id: 'education', label: TOPICS_DATA.education ? ($locale === 'my' ? TOPICS_DATA.education.labelMy : TOPICS_DATA.education.labelEn) : 'Education', icon: '🎓' },
		{ id: 'finance', label: TOPICS_DATA.finance ? ($locale === 'my' ? TOPICS_DATA.finance.labelMy : TOPICS_DATA.finance.labelEn) : 'Finance', icon: '💰' },
		{ id: 'personal_growth', label: TOPICS_DATA.personal_growth ? ($locale === 'my' ? TOPICS_DATA.personal_growth.labelMy : TOPICS_DATA.personal_growth.labelEn) : 'Growth', icon: '🌱' },
		{ id: 'communication', label: TOPICS_DATA.communication ? ($locale === 'my' ? TOPICS_DATA.communication.labelMy : TOPICS_DATA.communication.labelEn) : 'Communication', icon: '🗣️' },
		{ id: 'general', label: TOPICS_DATA.general ? ($locale === 'my' ? TOPICS_DATA.general.labelMy : TOPICS_DATA.general.labelEn) : 'General', icon: '✨' }
	]);

	const topicSpreadMap: Record<string, string> = {
		love: 'relationship',
		career: 'career',
		education: 'three_card',
		finance: 'decision',
		personal_growth: 'self_reflection',
		communication: 'three_card',
		general: 'three_card'
	};

	let userExplicitlyPickedSpread = $state(false);

	function selectTopic(topicId: string) {
		selectedTopic = topicId;
		if (!userExplicitlyPickedSpread) {
			selectedSpread = topicSpreadMap[topicId] || 'three_card';
		}
	}

	const canBeginReading = $derived(
		Boolean(question.trim()) && (drawMethod === 'random' || manualSelection.length > 0)
	);

	const loadingSteps = $derived(
		$locale === 'my'
			? [
					'သင်၏မေးခွန်းကို ဆန်းစစ်နေပါသည်...',
					'Prolog သင်္ကေတယုတ္တိဗေဒကို စစ်ဆေးနေပါသည်...',
					'တားရော့ကတ်များကို ဖတ်ရှုနေပါသည်...',
					'သင့်အတွက် ဟောကိန်းကို ပြင်ဆင်နေပါသည်...'
				]
			: [
					'Analyzing your question...',
					'Consulting symbolic knowledge...',
					'Reading your chosen cards...',
					'Preparing your interpretation...'
				]
	);

	async function startReading() {
		if (!canBeginReading) return;

		loading = true;
		error = '';
		reading = null;
		showReasoning = false;

		const steps = loadingSteps;
		let step = 0;
		loadingText = steps[0];
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
					$locale
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
					$locale
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
		manualSelection = [];
	}

	function getSpreadMeta(spreadId: string) {
		const s = SPREAD_TYPES_DATA[spreadId];
		if (!s) {
			const found = SPREAD_TYPES.find((x) => x.id === spreadId);
			return { name: found?.name || spreadId, desc: found?.description || '' };
		}
		return {
			name: $locale === 'my' ? s.nameMy : s.nameEn,
			desc: $locale === 'my' ? s.descMy : s.descEn
		};
	}
</script>

<svelte:head>
	<title>{$t('reading.title')} - {$t('brand.name')}</title>
</svelte:head>

<div class="page-container">
	<!-- Atmospheric Observatory lead -->
	<div class="relative mb-10 w-full">
		<div
			class="pointer-events-none absolute -top-10 left-1/4 h-96 w-96 rounded-full bg-primary-container/15 blur-[120px]"
		></div>
		<div
			class="pointer-events-none absolute -top-12 right-1/4 h-96 w-96 rounded-full bg-secondary-container/10 blur-[140px]"
		></div>

		<div class="relative z-10">
			<div
				class="font-mono-data mb-4 inline-flex items-center gap-2 rounded-full bg-surface-container-high/80 px-3 py-1 text-[10px] tracking-widest text-secondary uppercase"
			>
				<span class="h-1.5 w-1.5 animate-pulse rounded-full bg-secondary"></span>
				{$t('landing.engineOnline')}
			</div>
			<h1 class="font-headline text-3xl font-extrabold tracking-tight text-on-surface sm:text-4xl">
				{$t('reading.title')}
			</h1>
			<p class="mt-2 max-w-2xl text-on-surface-variant">
				{$t('reading.subtitle')}
			</p>
		</div>
	</div>

	<!-- Two-column workspace -->
	<div class="relative z-10 flex flex-col gap-8">
		{#if !reading}
			<div class="grid grid-cols-1 items-start gap-8 xl:grid-cols-12">
				<!-- LEFT COLUMN: Input Configuration Station -->
				<div class="flex flex-col gap-6 xl:col-span-5">
					<div
						class="flex flex-col gap-6 rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-xl sm:p-8"
					>
						<!-- STEP 1: Question Input -->
						<div class="flex flex-col gap-3">
							<div class="flex items-center justify-between">
								<div class="flex items-center gap-2">
									<span
										class="font-mono-data flex h-5 w-5 items-center justify-center rounded-full bg-primary/20 text-[11px] font-semibold text-primary"
										>1</span
									>
									<label
										class="font-headline text-base font-semibold text-on-surface"
										for="cosmic-query"
									>
										{$t('reading.questionLabel')}
									</label>
								</div>
								<span
									class="font-mono-data text-[11px] font-medium tracking-tight {question.length >= 480
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
									placeholder={$t('reading.questionPlaceholder')}
								></textarea>
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
									<span class="font-headline text-base font-semibold text-on-surface">
										{$t('reading.selectTopic')}
									</span>
								</div>
							</div>
							<div class="flex flex-wrap gap-2" role="radiogroup" aria-label="Reading topic">
								{#each topics as topic}
									<button
										type="button"
										class="font-mono-data flex items-center gap-1.5 rounded-full px-3 py-1.5 text-[11px] font-medium transition-all
											{selectedTopic === topic.id
											? 'bg-primary-container text-on-primary-container shadow-sm font-semibold'
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
								<span class="font-headline text-base font-semibold text-on-surface">
									{$t('reading.drawMethod')}
								</span>
							</div>
							<div class="grid grid-cols-2 gap-2.5" role="radiogroup" aria-label="Card draw method">
								<button
									type="button"
									class="flex flex-col items-start gap-1 rounded-xl p-3 text-left transition-all
										{drawMethod === 'random'
										? 'bg-primary-container/20 text-on-surface shadow-md border border-primary/40'
										: 'bg-surface-container/60 text-on-surface-variant hover:bg-surface-container-high'}"
									onclick={() => (drawMethod = 'random')}
								>
									<span class="flex items-center gap-1.5 text-sm font-semibold text-on-surface">
										<span class="material-symbols-outlined text-base">cyclone</span>
										{$t('reading.drawRandom')}
									</span>
									<span class="text-xs {drawMethod === 'random' ? 'text-primary' : 'text-on-surface-variant'}">
										{$locale === 'my' ? 'စနစ်က ကတ်များကို မွှေနှောက်ဆွဲယူမည်' : 'Let the array choose your spread'}
									</span>
								</button>
								<button
									type="button"
									class="flex flex-col items-start gap-1 rounded-xl p-3 text-left transition-all
										{drawMethod === 'manual'
										? 'bg-primary-container/20 text-on-surface shadow-md border border-primary/40'
										: 'bg-surface-container/60 text-on-surface-variant hover:bg-surface-container-high'}"
									onclick={() => (drawMethod = 'manual')}
								>
									<span class="flex items-center gap-1.5 text-sm font-semibold text-on-surface">
										<span class="material-symbols-outlined text-base">touch_app</span>
										{$t('reading.drawManual')}
									</span>
									<span class="text-xs {drawMethod === 'manual' ? 'text-primary' : 'text-on-surface-variant'}">
										{$locale === 'my' ? 'ကတ် ၇၈ ကတ်ထဲမှ စိတ်ကြိုက်ရွေးမည်' : 'Choose cards straight from the deck'}
									</span>
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
										<span class="font-headline text-base font-semibold text-on-surface">
											{$t('reading.selectSpread')}
										</span>
									</div>
									<span class="font-mono-data text-[10px] tracking-wider text-secondary uppercase">
										{#if selectedSpread === 'custom'}
											{customCardCount} {$locale === 'my' ? 'ကတ်' : `card${customCardCount === 1 ? '' : 's'}`}
										{:else}
											{SPREAD_TYPES.find((s) => s.id === selectedSpread)?.count ?? ''} {$locale === 'my' ? 'ကတ်' : 'cards'}
										{/if}
									</span>
								</div>
								<div id="spread" class="grid grid-cols-1 gap-2.5 sm:grid-cols-2">
									{#each SPREAD_TYPES as spread}
										{@const meta = getSpreadMeta(spread.id)}
										<button
											type="button"
											class="relative flex cursor-pointer flex-col justify-between overflow-hidden rounded-xl p-3 text-left transition-all
												{selectedSpread === spread.id
												? 'bg-primary-container/20 text-on-surface shadow-md border border-primary/40'
												: 'bg-surface-container/60 text-on-surface-variant hover:bg-surface-container-high'}"
											onclick={() => {
												selectedSpread = spread.id;
												userExplicitlyPickedSpread = true;
											}}
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
													<span class="text-sm font-semibold text-on-surface">{meta.name}</span>
												</div>
												<span class="font-mono-data shrink-0 text-[10px] text-outline"
													>{spread.id === 'custom' ? `1-${CUSTOM_DRAW_MAX}` : spread.count}</span
												>
											</div>
											<span
												class="relative z-10 text-xs {selectedSpread === spread.id
													? 'text-primary'
													: 'text-on-surface-variant'}">{meta.desc}</span
											>
										</button>
									{/each}
								</div>

								{#if selectedSpread === 'custom'}
									<div class="flex flex-col gap-2 rounded-xl bg-surface-container-high/40 p-4">
										<div class="flex items-center justify-between">
											<span class="text-sm font-medium text-on-surface">{$t('reading.customCardCount')}</span>
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
									<span class="font-headline text-base font-semibold text-on-surface">
										{$t('picker.title')}
									</span>
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
							class="font-headline group flex w-full items-center justify-center gap-2 rounded-full bg-gradient-to-r from-primary-container via-purple-600 to-secondary-container px-6 py-3.5 text-base font-semibold tracking-wide text-white shadow-lg transition-all hover:scale-[1.02] active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-50"
							onclick={startReading}
							disabled={!canBeginReading || loading}
						>
							<span
								class="material-symbols-outlined transition-transform duration-500 group-hover:rotate-180"
								>cyclone</span
							>
							<span>{loading ? loadingText || $t('common.loading') : $t('reading.beginButton')}</span>
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
								{loadingText || $t('reading.analyzing')}
							</p>
							<p class="max-w-sm text-sm text-on-surface-variant">
								{$locale === 'my' ? 'Prolog ယုတ္တိဗေဒစနစ်သည် သင်၏မေးခွန်းအတွက် ဓာတ်သဘောနှင့် သင်္ကေတများကို တွက်ချက်စစ်ဆေးနေပါသည်။' : 'The Prolog inference engine is evaluating elemental dignities and archetypal harmonics for your query.'}
							</p>
						{:else}
							<span class="material-symbols-outlined text-5xl text-outline">auto_awesome</span>
							<p class="font-headline text-lg text-on-surface">
								{$locale === 'my' ? 'လမ်းညွှန်ချက်ရယူရန် အသင့်ရှိသည်' : 'Awaiting Transmission'}
							</p>
							<p class="max-w-sm text-sm text-on-surface-variant">
								{$locale === 'my' ? 'မေးခွန်းကို ရေးသားပြီး ကဏ္ဍနှင့် ကတ်ခင်းကျင်းမှုစနစ်ကို ရွေးချယ်ကာ ဗေဒင်စတင်မေးမြန်းနိုင်ပါပြီ။' : 'Compose your query, choose a topic and a spread configuration, then begin your reading to reveal the drawn cards here.'}
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
							<h2 class="font-headline text-lg font-semibold text-on-surface">
								{$locale === 'my' ? 'သင်၏ တားရော့ဗေဒင် ရလဒ်' : 'Your Reading'}
							</h2>
							<p class="text-sm text-on-surface-variant">
								{(SPREAD_TYPES_DATA[reading.spread_type] ? ($locale === 'my' ? SPREAD_TYPES_DATA[reading.spread_type].nameMy : SPREAD_TYPES_DATA[reading.spread_type].nameEn) : getSpreadMeta(reading.spread_type).name)} &middot; {translateTopic(reading.category, $locale) || reading.category}
								{#if reading.topic}&middot; {translateTopic(reading.topic, $locale) || reading.topic}{/if}
							</p>
						</div>
						<button type="button" class="btn-secondary text-sm" onclick={resetReading}>
							{$t('reading.newReadingButton')}
						</button>
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
							<h2 class="font-headline text-xl font-semibold text-on-surface">
								{$locale === 'my' ? 'ဆွဲယူရရှိသော တားရော့ကတ်များ' : 'Active Spread'}
							</h2>
						</div>
						<span class="font-mono-data text-[11px] text-on-surface-variant"
							>{reading.cards.length} {$locale === 'my' ? 'ကတ် ဆွဲယူထားသည်' : 'CARDS DRAWN'}</span
						>
					</div>
					<div class="grid grid-cols-2 gap-4 perspective-[1000px] md:grid-cols-4">
						{#each reading.cards as card, i (card.card + i)}
							<div class="flex flex-col gap-2">
								<TarotCard {card} index={i} />
								<div class="text-center">
									<div class="font-mono-data text-xs font-medium tracking-wider text-primary">
										{translatePosition(card.position, $locale)}
									</div>
								</div>
								{#if card.zodiac_affinity}
									<p class="text-center text-[11px] leading-snug text-on-surface-variant italic px-1">
										{$locale === 'my' ? formatResonanceNote(card.zodiac_affinity.zodiac || currentProfile.zodiac_sign, card.zodiac_affinity.element || '', card.zodiac_affinity.card_theme || '', $locale) : card.zodiac_affinity.combined}
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
									{$t('reading.aiSynthesis')}
								</h3>
								<span class="font-mono-data text-[11px] text-on-surface-variant"
									>{$locale === 'my' ? 'သင်္ကေတသဟဇာတဖြစ်မှု ဆန်းစစ်ချက်' : 'Harmonic Convergence Analysis'}</span
								>
							</div>
						</div>
						{#if reading.themes.length > 0}
							<div class="flex flex-wrap items-center gap-2">
								{#each reading.themes as theme}
									<span
										class="font-mono-data rounded-full bg-primary-container px-3 py-1 text-[10px] tracking-wider text-on-primary-container uppercase"
									>
										{translateTheme(theme, $locale)}
									</span>
								{/each}
							</div>
						{/if}
					</div>

					<div class="relative z-10 rounded-xl bg-surface-container-lowest/60 p-5">
						<MarkdownText content={formatReadingSynthesis(reading.ai_interpretation, reading, $locale)} />
					</div>

					<!-- READING DIRECTION & ADVICE -->
					{#if reading.direction || reading.advice}
						<div class="relative z-10 grid grid-cols-1 gap-4 sm:grid-cols-2">
							{#if reading.direction}
								{@const directionMeta = {
									optimistic: { icon: 'trending_up', color: 'text-primary', label: $locale === 'my' ? 'အကောင်းမြင်ဖွယ် အလားအလာ' : 'Optimistic' },
									challenging: { icon: 'warning', color: 'text-error', label: $locale === 'my' ? 'စိန်ခေါ်မှုများသော အခြေအနေ' : 'Challenging' },
									reflective: { icon: 'nights_stay', color: 'text-secondary', label: $locale === 'my' ? 'ဆင်ခြင်သုံးသပ်ရမည့် အခြေအနေ' : 'Reflective' },
									balanced: { icon: 'balance', color: 'text-tertiary', label: $locale === 'my' ? 'မျှတသော အခြေအနေ' : 'Balanced' },
								}[reading.direction] ?? { icon: 'auto_awesome', color: 'text-secondary', label: reading.direction }}
								<div class="rounded-xl bg-surface-container-lowest/60 p-5 flex flex-col gap-1.5">
									<div class="flex items-center gap-2">
										<span class="material-symbols-outlined {directionMeta.color}">{directionMeta.icon}</span>
										<span class="font-mono-data text-[11px] uppercase tracking-wider text-on-surface-variant">
											{$locale === 'my' ? 'ကံကြမ္မာဦးတည်ချက်' : 'Reading Direction'}
										</span>
									</div>
									<span class="font-headline text-lg {directionMeta.color}">{directionMeta.label}</span>
								</div>
							{/if}
							{#if reading.advice}
								<div class="rounded-xl bg-surface-container-lowest/60 p-5 flex flex-col gap-2">
									<div class="flex items-center gap-2">
										<span class="material-symbols-outlined text-primary">tips_and_updates</span>
										<span class="font-mono-data text-[11px] uppercase tracking-wider text-on-surface-variant">
											{$t('reading.advice')}
										</span>
									</div>
									{#if reading.advice.category_advice}
										<p class="text-sm text-on-surface">{formatAdviceText(reading.advice.category_advice, $locale)}</p>
									{/if}
									{#if reading.advice.theme_advice}
										<p class="text-sm text-on-surface-variant italic">{formatAdviceText(reading.advice.theme_advice, $locale)}</p>
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
									{$t('reading.conflicts')}
								</span>
							</div>
							{#each reading.conflicts as conflict}
								<div class="rounded-lg bg-surface-container-high/40 p-3.5">
									<p class="text-sm font-semibold text-on-surface mb-1">{conflict.title}</p>
									<p class="text-xs text-on-surface-variant mb-2">
										<span class="text-primary font-medium">{conflict.card1_name}</span>
										{#if conflict.card1_position}({translatePosition(conflict.card1_position, $locale)}){/if}
										&harr;
										<span class="text-secondary font-medium">{conflict.card2_name}</span>
										{#if conflict.card2_position}({translatePosition(conflict.card2_position, $locale)}){/if}
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
									>{$t('reading.reasoningTrace')}</span
								>
								<span
									class="font-mono-data rounded bg-surface-container px-2 py-0.5 text-[10px] text-outline"
									>Prolog Engine</span
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
