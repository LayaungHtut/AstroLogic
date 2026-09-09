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
	<div class="relative w-full mb-10">
		<div
			class="absolute -top-10 left-1/4 w-96 h-96 rounded-full bg-primary-container/15 blur-[120px] pointer-events-none"
		></div>
		<div
			class="absolute -top-12 right-1/4 w-96 h-96 rounded-full bg-secondary-container/10 blur-[140px] pointer-events-none"
		></div>
		<div class="relative z-10">
			<div
				class="inline-flex items-center gap-2 px-3 py-1 mb-4 rounded-full bg-surface-container-high/80 text-secondary font-mono-data text-[10px] tracking-widest uppercase"
			>
				<span class="w-1.5 h-1.5 rounded-full bg-secondary shadow-[0_0_8px_#4cd7f6]"></span>
				<span>{$t('landing.statZodiacCovered')} • Ephemeris Matrix 360°</span>
			</div>
			<h1
				class="font-headline text-3xl md:text-4xl font-bold tracking-tight bg-gradient-to-r from-primary via-tertiary to-secondary bg-clip-text text-transparent mb-3"
			>
				{$t('zodiac.title')}
			</h1>
			<p class="text-on-surface-variant max-w-2xl leading-relaxed">
				{$t('zodiac.subtitle')}
			</p>
		</div>

		<!-- Filter & Modality Segmentation Controls -->
		<div class="flex flex-wrap items-center gap-2 mt-8 pt-6 border-t border-outline-variant/20">
			<button
				class="px-4 py-2 rounded-full font-mono-data text-xs transition-all {elementFilter === 'all'
					? 'bg-primary-container text-on-primary-container shadow-[0_0_15px_rgba(124,58,237,0.4)]'
					: 'bg-surface-container-high/60 text-on-surface-variant hover:text-on-surface hover:bg-surface-container-highest'}"
				onclick={() => (elementFilter = 'all')}
			>
				{$t('common.all')} ({signs.length})
			</button>
			{#each ELEMENTS as el}
				<button
					class="px-4 py-2 rounded-full font-mono-data text-xs transition-all flex items-center gap-1.5 capitalize {elementFilter === el
						? 'bg-primary-container text-on-primary-container shadow-[0_0_15px_rgba(124,58,237,0.4)]'
						: 'bg-surface-container-high/60 text-on-surface-variant hover:text-on-surface hover:bg-surface-container-highest'}"
					onclick={() => (elementFilter = el)}
				>
					<span class="w-2 h-2 rounded-full" style:background-color={ELEMENT_COLORS[el]}></span>
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
				class="relative w-full rounded-2xl overflow-hidden bg-surface-container-lowest/90 backdrop-blur-2xl shadow-2xl mb-12 group"
			>
				<div
					class="absolute -top-24 -right-24 w-[500px] h-[500px] bg-gradient-to-bl from-primary-container/25 via-secondary-container/15 to-transparent rounded-full blur-3xl pointer-events-none"
				></div>
				<div
					class="absolute bottom-0 left-1/3 w-80 h-80 rounded-full blur-2xl pointer-events-none"
					style:background-color="{accent}15"
				></div>

				<div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 p-6 lg:p-10 items-center">
					<!-- Left Graphic -->
					<div class="lg:col-span-4 flex flex-col items-center text-center relative">
						<div class="relative w-48 h-48 sm:w-56 sm:h-56 flex items-center justify-center">
							<svg
								class="absolute inset-0 w-full h-full animate-[spin_60s_linear_infinite]"
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
								<circle class="text-secondary/20" cx="100" cy="100" r="76" stroke="currentColor" stroke-width="1" />
								<circle
									class="text-outline-variant/40"
									cx="100"
									cy="100"
									r="60"
									stroke="currentColor"
									stroke-dasharray="1 4"
									stroke-width="0.75"
								/>
								<path class="text-primary/20" d="M100,8 L100,192 M8,100 L192,100" stroke="currentColor" stroke-width="0.5" />
							</svg>
							<ZodiacBadge sign={selectedInfo.sign} element={selectedInfo.element} size="lg" />
						</div>
						<div class="mt-4 flex items-center gap-2 font-mono-data text-xs text-secondary">
							<span class="material-symbols-outlined text-[16px]">explore</span>
							<span>{zData.dateRange || selectedInfo.date_range}</span>
						</div>
					</div>

					<!-- Right Narrative -->
					<div class="lg:col-span-8 flex flex-col gap-6">
						<div class="flex flex-wrap items-center justify-between gap-4">
							<div class="flex items-center gap-3">
								<ElementBadge element={selectedInfo.element} />
								<span
									class="px-3 py-1 rounded-full font-mono-data text-[10px] uppercase tracking-widest bg-surface-container-high text-tertiary capitalize"
								>
									{formatModality(selectedInfo.modality, $locale)}
								</span>
							</div>
							<div class="font-mono-data text-xs text-on-surface-variant flex items-center gap-1.5">
								<span class="material-symbols-outlined text-[16px] text-secondary">calendar_today</span>
								<span>{zData.dateRange || selectedInfo.date_range}</span>
							</div>
						</div>

						<div>
							<div class="font-mono-data text-[10px] tracking-widest uppercase text-secondary mb-1">
								{$t('zodiac.activeStation')}
							</div>
							<h2 class="font-headline text-2xl md:text-3xl text-on-surface tracking-tight capitalize">
								{zData.name}
							</h2>
						</div>

						<!-- Metric Cards -->
						<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
							<div class="p-4 rounded-xl bg-surface-container-high/60 backdrop-blur-md">
								<div class="font-mono-data text-[11px] text-on-surface-variant">{$t('zodiac.ruler')}</div>
								<div class="text-lg font-headline text-primary mt-1 flex items-center gap-1.5 capitalize">
									<span class="material-symbols-outlined text-[18px]">shield</span>
									<span>{formatPlanet(selectedInfo.ruling_planet, $locale)}</span>
								</div>
							</div>
							<div class="p-4 rounded-xl bg-surface-container-high/60 backdrop-blur-md">
								<div class="font-mono-data text-[11px] text-on-surface-variant">{$t('zodiac.element')}</div>
								<div class="text-lg font-headline text-secondary mt-1 flex items-center gap-1.5 capitalize">
									<span>{ELEMENT_ICONS[selectedInfo.element]}</span>
									<span>{formatElement(selectedInfo.element, $locale)}</span>
								</div>
							</div>
						</div>

						<!-- Traits -->
						<div class="flex flex-wrap items-center gap-2 pt-2">
							{#each (zData.traits.length > 0 ? zData.traits : selectedInfo.traits) as trait}
								<span
									class="px-3 py-1 rounded-full font-mono-data text-[10px] uppercase tracking-wider bg-surface-container text-on-surface"
								>
									{trait.replace(/_/g, ' ')}
								</span>
							{/each}
						</div>

						<div class="pt-2 flex flex-wrap gap-3">
							<button
								type="button"
								class="btn-primary inline-flex items-center gap-2.5"
								onclick={() => (profileOpen && profileResult ? (profileOpen = false) : loadProfile(selectedInfo!.sign))}
							>
								<span class="material-symbols-outlined text-[18px]">psychology</span>
								<span>{profileOpen && profileResult ? $t('zodiac.hideReasoning') : $t('zodiac.whyAmILikeThis')}</span>
							</button>
						</div>
					</div>
				</div>

				{#if profileOpen}
					<div class="relative z-10 px-6 lg:px-10 pb-8 -mt-2">
						{#if profileLoading}
							<LoadingSpinner text={$locale === 'my' ? 'ကျိုးကြောင်းဆင်ခြင်မှု အဆင့်ဆင့်ကို တွက်ချက်နေသည်...' : 'Tracing the reasoning chain...'} />
						{:else if profileError}
							<div class="p-4 rounded-xl bg-error-container/10 text-error text-sm">{profileError}</div>
						{:else if profileResult}
							<div class="rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl p-6 lg:p-8">
								<h3 class="font-headline text-lg text-on-surface mb-4 flex items-center gap-2">
									<span class="material-symbols-outlined text-primary">psychology</span>
									{$locale === 'my' ? `${zData.name} ${$t('zodiac.whyYouAre')}` : `${$t('zodiac.whyYouAre')} ${zData.name}`}
								</h3>
								<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
									<div class="p-4 rounded-xl bg-surface-container-high/60">
										<div class="font-mono-data text-[11px] text-secondary uppercase tracking-wider mb-1">{$t('zodiac.personalityStyle')}</div>
										<p class="text-sm text-on-surface/90">{formatPersonalityStyle(profileResult.profile.personality_style, selectedInfo.element, $locale)}</p>
									</div>
									<div class="p-4 rounded-xl bg-surface-container-high/60">
										<div class="font-mono-data text-[11px] text-secondary uppercase tracking-wider mb-1">{$t('zodiac.approachToLife')}</div>
										<p class="text-sm text-on-surface/90">{formatApproachToLife(profileResult.profile.approach_to_life, selectedInfo.modality, $locale)}</p>
									</div>
									<div class="p-4 rounded-xl bg-surface-container-high/60">
										<div class="font-mono-data text-[11px] text-secondary uppercase tracking-wider mb-1">{$t('zodiac.planetaryInfluence')}</div>
										<p class="text-sm text-on-surface/90">{formatPlanetaryInfluence(profileResult.profile.planetary_influence, selectedInfo.ruling_planet, $locale)}</p>
									</div>
								</div>
								<div class="flex items-center gap-2.5 pb-3 mb-3 border-b border-outline-variant/20">
									<span class="w-2 h-2 rounded-full bg-secondary shadow-[0_0_8px_#4cd7f6] animate-pulse"></span>
									<span class="font-mono-data text-xs text-secondary tracking-widest uppercase">{$t('zodiac.prologChain')}</span>
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
		<div class="flex items-center justify-between mb-6">
			<div>
				<div class="font-mono-data text-[10px] uppercase text-secondary tracking-widest mb-1">
					{$t('landing.twelveModalities')}
				</div>
				<h2 class="font-headline text-xl md:text-2xl text-on-surface tracking-tight">
					{$t('zodiac.spheres')}
				</h2>
			</div>
			<div
				class="hidden sm:flex items-center gap-2 font-mono-data text-xs text-on-surface-variant bg-surface-container-high px-3 py-1.5 rounded-full"
			>
				<span class="material-symbols-outlined text-[16px] text-secondary">tune</span>
				<span>{$locale === 'my' ? `ရာသီခွင် ${signs.length} ခုအနက် ${filteredSigns.length} ခု ပြသနေသည်` : `${$t('zodiac.showing')} ${filteredSigns.length} ${$t('zodiac.of')} ${signs.length} ${$t('zodiac.archetypes')}`}</span>
			</div>
		</div>

		<!-- Zodiac Grid -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
			{#each filteredSigns as sign, i}
				{@const cardZData = getZodiacTranslation(sign.sign, $locale)}
				{@const accent = ELEMENT_COLORS[sign.element] || '#9333ea'}
				{@const isSelected = selected === sign.sign}
				<button
					class="group relative p-6 rounded-2xl backdrop-blur-xl transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between text-left {isSelected
						? 'bg-surface-container/90 ring-1 ring-primary/40 shadow-[0_12px_40px_rgba(124,58,237,0.25)]'
						: 'bg-surface-container-low/90 hover:bg-surface-container-high/80'}"
					onclick={() => selectSign(sign.sign)}
				>
					<div
						class="absolute top-0 right-0 p-4 font-headline text-2xl select-none pointer-events-none transition-colors {isSelected
							? 'text-primary/20'
							: 'text-on-surface-variant/10 group-hover:text-primary/20'}"
					>
						{String(i + 1).padStart(2, '0')}
					</div>
					<div>
						<div class="flex items-center justify-between mb-4">
							<div
								class="w-12 h-12 rounded-xl bg-surface-container-high flex items-center justify-center text-2xl group-hover:scale-110 transition-transform"
								style:color={accent}
							>
								{ZODIAC_SYMBOLS[sign.sign]}
							</div>
							<div class="flex items-center gap-2">
								<span
									class="px-2.5 py-0.5 rounded-full font-mono-data text-[10px] uppercase capitalize"
									style:background-color="{accent}20"
									style:color={accent}
								>
									{formatElement(sign.element, $locale)}
								</span>
								<span
									class="px-2.5 py-0.5 rounded-full font-mono-data text-[10px] uppercase bg-surface-container-highest text-on-surface-variant capitalize"
								>
									{formatModality(sign.modality, $locale)}
								</span>
							</div>
						</div>
						<div class="mb-3">
							<h3
								class="font-headline text-lg text-on-surface group-hover:text-primary transition-colors capitalize {isSelected
									? 'text-primary font-semibold'
									: ''}"
							>
								{cardZData.name}
							</h3>
							<div class="font-mono-data text-xs text-secondary mt-1">{cardZData.dateRange || sign.date_range}</div>
						</div>
					</div>
					<div class="pt-4 border-t border-outline-variant/20 flex flex-col gap-2 font-mono-data text-xs">
						<div class="flex justify-between items-center text-on-surface-variant">
							<span>{$t('zodiac.rulerLabel')}</span>
							<span class="text-on-surface font-medium capitalize">{formatPlanet(sign.ruling_planet, $locale)}</span>
						</div>
					</div>
				</button>
			{/each}
		</div>
	{/if}
</div>
