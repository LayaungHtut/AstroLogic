<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { fetchAllZodiac, fetchZodiac, fetchZodiacProfile } from '$lib/utils/api';
	import { ZODIAC_SYMBOLS, ELEMENT_COLORS, ELEMENT_ICONS } from '$lib/types';
	import type { ZodiacInfo, ZodiacProfileResult } from '$lib/types';
	import ZodiacBadge from '$lib/components/ZodiacBadge.svelte';
	import ElementBadge from '$lib/components/ElementBadge.svelte';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import ReasoningStep from '$lib/components/ReasoningStep.svelte';
	import {
		locale,
		t,
		getZodiacTranslation,
		formatElement,
		formatModality,
		formatPlanet,
		formatPersonalityStyle,
		formatApproachToLife,
		formatPlanetaryInfluence
	} from '$lib/i18n';

	let signs = $state<ZodiacInfo[]>([]);
	let selected = $state<string>('');
	let selectedInfo = $state<ZodiacInfo | null>(null);
	let loading = $state(true);
	let elementFilter = $state<string>('all');

	// Feature: Profile Reasoning Trace ("Why am I like this?")
	let profileResult = $state<ZodiacProfileResult | null>(null);
	let profileLoading = $state(false);
	let profileError = $state('');
	let profileOpen = $state(false);

	async function loadProfile(sign: string) {
		profileOpen = true;
		profileLoading = true;
		profileError = '';
		profileResult = null;
		try {
			const result = await fetchZodiacProfile(sign);
			if ('error' in result) {
				profileError = String((result as unknown as { error: string }).error);
			} else {
				profileResult = result;
			}
		} catch (e) {
			profileError = e instanceof Error ? e.message : 'Failed to load profile reasoning';
		} finally {
			profileLoading = false;
		}
	}

	const ELEMENTS = ['fire', 'earth', 'air', 'water'];

	const filteredSigns = $derived(
		elementFilter === 'all' ? signs : signs.filter((s) => s.element === elementFilter)
	);

	function elementCount(el: string) {
		return signs.filter((s) => s.element === el).length;
	}

	onMount(async () => {
		const signParam = page.url.searchParams.get('sign');
		if (signParam) selected = signParam;

		try {
			signs = await fetchAllZodiac();
			if (selected) {
				selectedInfo = await fetchZodiac(selected);
			} else if (signs.length > 0) {
				selected = signs[0].sign;
				selectedInfo = signs[0];
			}
		} catch {
			// API may not be running
		} finally {
			loading = false;
		}
	});

	async function selectSign(sign: string) {
		selected = sign;
		profileOpen = false;
		profileResult = null;
		try {
			selectedInfo = await fetchZodiac(sign);
		} catch {
			selectedInfo = null;
		}
	}
</script>

<svelte:head>
	<title>{$t('zodiac.title')} - {$t('brand.name')}</title>
</svelte:head>

<div class="page-container">
	<!-- Observatory Header / Atmosphere Lead -->
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
				<span class="h-1.5 w-1.5 rounded-full bg-secondary shadow-[0_0_8px_#4cd7f6]"></span>
				<span>{$t('landing.statZodiacCovered')} • Ephemeris Matrix 360°</span>
			</div>
			<h1
				class="font-headline mb-3 bg-gradient-to-r from-primary via-tertiary to-secondary bg-clip-text text-3xl font-bold tracking-tight text-transparent md:text-4xl"
			>
				{$t('zodiac.title')}
			</h1>
			<p class="max-w-2xl leading-relaxed text-on-surface-variant">
				{$t('zodiac.subtitle')}
			</p>
		</div>

		<!-- Filter & Modality Segmentation Controls -->
		<div class="mt-8 flex flex-wrap items-center gap-2 border-t border-outline-variant/20 pt-6">
			<button
				class="font-mono-data rounded-full px-4 py-2 text-xs transition-all {elementFilter === 'all'
					? 'bg-primary-container text-on-primary-container shadow-[0_0_15px_rgba(124,58,237,0.4)]'
					: 'bg-surface-container-high/60 text-on-surface-variant hover:bg-surface-container-highest hover:text-on-surface'}"
				onclick={() => (elementFilter = 'all')}
			>
				{$t('common.all')} ({signs.length})
			</button>
			{#each ELEMENTS as el}
				<button
					class="font-mono-data flex items-center gap-1.5 rounded-full px-4 py-2 text-xs capitalize transition-all {elementFilter ===
					el
						? 'bg-primary-container text-on-primary-container shadow-[0_0_15px_rgba(124,58,237,0.4)]'
						: 'bg-surface-container-high/60 text-on-surface-variant hover:bg-surface-container-highest hover:text-on-surface'}"
					onclick={() => (elementFilter = el)}
				>
					<span class="h-2 w-2 rounded-full" style:background-color={ELEMENT_COLORS[el]}></span>
					{formatElement(el, $locale)} ({elementCount(el)})
				</button>
			{/each}
		</div>
	</div>

	{#if loading}
		<LoadingSpinner text={$t('common.loading')} />
	{:else}
		<!-- Selected Sign Focal Module -->
		{#if selectedInfo}
			{@const zData = getZodiacTranslation(selectedInfo.sign, $locale)}
			{@const accent = ELEMENT_COLORS[selectedInfo.element] || '#9333ea'}
			<section
				class="group relative mb-12 w-full overflow-hidden rounded-2xl bg-surface-container-lowest/90 shadow-2xl backdrop-blur-2xl"
			>
				<div
					class="pointer-events-none absolute -top-24 -right-24 h-[500px] w-[500px] rounded-full bg-gradient-to-bl from-primary-container/25 via-secondary-container/15 to-transparent blur-3xl"
				></div>
				<div
					class="pointer-events-none absolute bottom-0 left-1/3 h-80 w-80 rounded-full blur-2xl"
					style:background-color="{accent}15"
				></div>

				<div class="relative z-10 grid grid-cols-1 items-center gap-8 p-6 lg:grid-cols-12 lg:p-10">
					<!-- Left Graphic -->
					<div class="relative flex flex-col items-center text-center lg:col-span-4">
						<div class="relative flex h-48 w-48 items-center justify-center sm:h-56 sm:w-56">
							<svg
								class="absolute inset-0 h-full w-full animate-[spin_60s_linear_infinite]"
								fill="none"
								viewBox="0 0 200 200"
							>
								<circle
									class="text-primary/30"
									cx="100"
									cy="100"
									r="92"
									stroke="currentColor"
									stroke-dasharray="3 6"
									stroke-width="0.75"
								/>
								<circle
									class="text-secondary/20"
									cx="100"
									cy="100"
									r="76"
									stroke="currentColor"
									stroke-width="1"
								/>
								<circle
									class="text-outline-variant/40"
									cx="100"
									cy="100"
									r="60"
									stroke="currentColor"
									stroke-dasharray="1 4"
									stroke-width="0.75"
								/>
								<path
									class="text-primary/20"
									d="M100,8 L100,192 M8,100 L192,100"
									stroke="currentColor"
									stroke-width="0.5"
								/>
							</svg>
							<ZodiacBadge sign={selectedInfo.sign} element={selectedInfo.element} size="lg" />
						</div>
						<div class="font-mono-data mt-4 flex items-center gap-2 text-xs text-secondary">
							<span class="material-symbols-outlined text-[16px]">explore</span>
							<span>{zData.dateRange || selectedInfo.date_range}</span>
						</div>
					</div>

					<!-- Right Narrative -->
					<div class="flex flex-col gap-6 lg:col-span-8">
						<div class="flex flex-wrap items-center justify-between gap-4">
							<div class="flex items-center gap-3">
								<ElementBadge element={selectedInfo.element} />
								<span
									class="font-mono-data rounded-full bg-surface-container-high px-3 py-1 text-[10px] tracking-widest text-tertiary capitalize uppercase"
								>
									{formatModality(selectedInfo.modality, $locale)}
								</span>
							</div>
							<div class="font-mono-data flex items-center gap-1.5 text-xs text-on-surface-variant">
								<span class="material-symbols-outlined text-[16px] text-secondary"
									>calendar_today</span
								>
								<span>{zData.dateRange || selectedInfo.date_range}</span>
							</div>
						</div>

						<div>
							<div class="font-mono-data mb-1 text-[10px] tracking-widest text-secondary uppercase">
								{$t('zodiac.activeStation')}
							</div>
							<h2
								class="font-headline text-2xl tracking-tight text-on-surface capitalize md:text-3xl"
							>
								{zData.name}
							</h2>
						</div>

						<!-- Metric Cards -->
						<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
							<div class="rounded-xl bg-surface-container-high/60 p-4 backdrop-blur-md">
								<div class="font-mono-data text-[11px] text-on-surface-variant">
									{$t('zodiac.ruler')}
								</div>
								<div
									class="font-headline mt-1 flex items-center gap-1.5 text-lg text-primary capitalize"
								>
									<span class="material-symbols-outlined text-[18px]">shield</span>
									<span>{formatPlanet(selectedInfo.ruling_planet, $locale)}</span>
								</div>
							</div>
							<div class="rounded-xl bg-surface-container-high/60 p-4 backdrop-blur-md">
								<div class="font-mono-data text-[11px] text-on-surface-variant">
									{$t('zodiac.element')}
								</div>
								<div
									class="font-headline mt-1 flex items-center gap-1.5 text-lg text-secondary capitalize"
								>
									<span>{ELEMENT_ICONS[selectedInfo.element]}</span>
									<span>{formatElement(selectedInfo.element, $locale)}</span>
								</div>
							</div>
						</div>

						<!-- Traits -->
						<div class="flex flex-wrap items-center gap-2 pt-2">
							{#each zData.traits.length > 0 ? zData.traits : selectedInfo.traits as trait}
								<span
									class="font-mono-data rounded-full bg-surface-container px-3 py-1 text-[10px] tracking-wider text-on-surface uppercase"
								>
									{trait.replace(/_/g, ' ')}
								</span>
							{/each}
						</div>

						<div class="flex flex-wrap gap-3 pt-2">
							<button
								type="button"
								class="btn-primary inline-flex items-center gap-2.5"
								onclick={() =>
									profileOpen && profileResult
										? (profileOpen = false)
										: loadProfile(selectedInfo!.sign)}
							>
								<span class="material-symbols-outlined text-[18px]">psychology</span>
								<span
									>{profileOpen && profileResult
										? $t('zodiac.hideReasoning')
										: $t('zodiac.whyAmILikeThis')}</span
								>
							</button>
						</div>
					</div>
				</div>

				{#if profileOpen}
					<div class="relative z-10 -mt-2 px-6 pb-8 lg:px-10">
						{#if profileLoading}
							<LoadingSpinner
								text={$locale === 'my'
									? 'ကျိုးကြောင်းဆင်ခြင်မှု အဆင့်ဆင့်ကို တွက်ချက်နေသည်...'
									: 'Tracing the reasoning chain...'}
							/>
						{:else if profileError}
							<div class="rounded-xl bg-error-container/10 p-4 text-sm text-error">
								{profileError}
							</div>
						{:else if profileResult}
							<div
								class="rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md lg:p-8"
							>
								<h3 class="font-headline mb-4 flex items-center gap-2 text-lg text-on-surface">
									<span class="material-symbols-outlined text-primary">psychology</span>
									{$locale === 'my'
										? `${zData.name} ${$t('zodiac.whyYouAre')}`
										: `${$t('zodiac.whyYouAre')} ${zData.name}`}
								</h3>
								<div class="mb-6 grid grid-cols-1 gap-4 md:grid-cols-3">
									<div class="rounded-xl bg-surface-container-high/60 p-4">
										<div
											class="font-mono-data mb-1 text-[11px] tracking-wider text-secondary uppercase"
										>
											{$t('zodiac.personalityStyle')}
										</div>
										<p class="text-sm text-on-surface/90">
											{formatPersonalityStyle(
												profileResult.profile.personality_style,
												selectedInfo.element,
												$locale
											)}
										</p>
									</div>
									<div class="rounded-xl bg-surface-container-high/60 p-4">
										<div
											class="font-mono-data mb-1 text-[11px] tracking-wider text-secondary uppercase"
										>
											{$t('zodiac.approachToLife')}
										</div>
										<p class="text-sm text-on-surface/90">
											{formatApproachToLife(
												profileResult.profile.approach_to_life,
												selectedInfo.modality,
												$locale
											)}
										</p>
									</div>
									<div class="rounded-xl bg-surface-container-high/60 p-4">
										<div
											class="font-mono-data mb-1 text-[11px] tracking-wider text-secondary uppercase"
										>
											{$t('zodiac.planetaryInfluence')}
										</div>
										<p class="text-sm text-on-surface/90">
											{formatPlanetaryInfluence(
												profileResult.profile.planetary_influence,
												selectedInfo.ruling_planet,
												$locale
											)}
										</p>
									</div>
								</div>
								<div class="mb-3 flex items-center gap-2.5 border-b border-outline-variant/20 pb-3">
									<span
										class="h-2 w-2 animate-pulse rounded-full bg-secondary shadow-[0_0_8px_#4cd7f6]"
									></span>
									<span class="font-mono-data text-xs tracking-widest text-secondary uppercase"
										>{$t('zodiac.prologChain')}</span
									>
								</div>
								<div class="space-y-2">
									{#each profileResult.reasoning as step, i}
										<ReasoningStep {step} index={i} />
									{/each}
								</div>
							</div>
						{/if}
					</div>
				{/if}
			</section>
		{/if}

		<!-- Section Header -->
		<div class="mb-6 flex items-center justify-between">
			<div>
				<div class="font-mono-data mb-1 text-[10px] tracking-widest text-secondary uppercase">
					{$t('landing.twelveModalities')}
				</div>
				<h2 class="font-headline text-xl tracking-tight text-on-surface md:text-2xl">
					{$t('zodiac.spheres')}
				</h2>
			</div>
			<div
				class="font-mono-data hidden items-center gap-2 rounded-full bg-surface-container-high px-3 py-1.5 text-xs text-on-surface-variant sm:flex"
			>
				<span class="material-symbols-outlined text-[16px] text-secondary">tune</span>
				<span
					>{$locale === 'my'
						? `ရာသီခွင် ${signs.length} ခုအနက် ${filteredSigns.length} ခု ပြသနေသည်`
						: `${$t('zodiac.showing')} ${filteredSigns.length} ${$t('zodiac.of')} ${signs.length} ${$t('zodiac.archetypes')}`}</span
				>
			</div>
		</div>

		<!-- Zodiac Grid -->
		<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
			{#each filteredSigns as sign, i}
				{@const cardZData = getZodiacTranslation(sign.sign, $locale)}
				{@const accent = ELEMENT_COLORS[sign.element] || '#9333ea'}
				{@const isSelected = selected === sign.sign}
				<button
					class="group relative flex flex-col justify-between rounded-2xl p-6 text-left backdrop-blur-xl transition-all duration-300 hover:-translate-y-1 {isSelected
						? 'bg-surface-container/90 shadow-[0_12px_40px_rgba(124,58,237,0.25)] ring-1 ring-primary/40'
						: 'bg-surface-container-low/90 hover:bg-surface-container-high/80'}"
					onclick={() => selectSign(sign.sign)}
				>
					<div
						class="font-headline pointer-events-none absolute top-0 right-0 p-4 text-2xl transition-colors select-none {isSelected
							? 'text-primary/20'
							: 'text-on-surface-variant/10 group-hover:text-primary/20'}"
					>
						{String(i + 1).padStart(2, '0')}
					</div>
					<div>
						<div class="mb-4 flex items-center justify-between">
							<div
								class="flex h-12 w-12 items-center justify-center rounded-xl bg-surface-container-high text-2xl transition-transform group-hover:scale-110"
								style:color={accent}
							>
								{ZODIAC_SYMBOLS[sign.sign]}
							</div>
							<div class="flex items-center gap-2">
								<span
									class="font-mono-data rounded-full px-2.5 py-0.5 text-[10px] capitalize uppercase"
									style:background-color="{accent}20"
									style:color={accent}
								>
									{formatElement(sign.element, $locale)}
								</span>
								<span
									class="font-mono-data rounded-full bg-surface-container-highest px-2.5 py-0.5 text-[10px] text-on-surface-variant capitalize uppercase"
								>
									{formatModality(sign.modality, $locale)}
								</span>
							</div>
						</div>
						<div class="mb-3">
							<h3
								class="font-headline text-lg text-on-surface capitalize transition-colors group-hover:text-primary {isSelected
									? 'font-semibold text-primary'
									: ''}"
							>
								{cardZData.name}
							</h3>
							<div class="font-mono-data mt-1 text-xs text-secondary">
								{cardZData.dateRange || sign.date_range}
							</div>
						</div>
					</div>
					<div
						class="font-mono-data flex flex-col gap-2 border-t border-outline-variant/20 pt-4 text-xs"
					>
						<div class="flex items-center justify-between text-on-surface-variant">
							<span>{$t('zodiac.rulerLabel')}</span>
							<span class="font-medium text-on-surface capitalize"
								>{formatPlanet(sign.ruling_planet, $locale)}</span
							>
						</div>
					</div>
				</button>
			{/each}
		</div>
	{/if}
</div>
