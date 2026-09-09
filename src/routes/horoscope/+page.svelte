<script lang="ts">
	import { profile } from '$lib/stores';
	import { generateHoroscope } from '$lib/utils/api';
	import type { HoroscopeResult } from '$lib/types';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import ZodiacBadge from '$lib/components/ZodiacBadge.svelte';
	import ElementBadge from '$lib/components/ElementBadge.svelte';
	import ReasoningStep from '$lib/components/ReasoningStep.svelte';
	import ProfileSettingsModal from '$lib/components/ProfileSettingsModal.svelte';
	import MarkdownText from '$lib/components/MarkdownText.svelte';
	import {
		locale,
		t,
		getZodiacTranslation,
		translateHoroscopeTheme,
		formatHoroscopeGuidance,
		formatHoroscopeReflection,
		formatHoroscopeOpportunity,
		formatHoroscopeCaution
	} from '$lib/i18n';

	const moods = [
		{ id: 'happy', key: 'horoscope.mood.happy', icon: '😄' },
		{ id: 'calm', key: 'horoscope.mood.calm', icon: '😌' },
		{ id: 'excited', key: 'horoscope.mood.excited', icon: '🤩' },
		{ id: 'uncertain', key: 'horoscope.mood.uncertain', icon: '😕' },
		{ id: 'stressed', key: 'horoscope.mood.stressed', icon: '😓' },
		{ id: 'reflective', key: 'horoscope.mood.reflective', icon: '🧘' },
		{ id: 'curious', key: 'horoscope.mood.curious', icon: '🤔' },
		{ id: 'neutral', key: 'horoscope.mood.neutral', icon: '😐' }
	];

	let selectedMood = $state('neutral');
	let result = $state<HoroscopeResult | null>(null);
	let loading = $state(false);
	let error = $state('');
	let showProfileSettings = $state(false);

	const currentProfile = $derived($profile);
	const hasSign = $derived(!!currentProfile.zodiac_sign);

	async function getHoroscope() {
		loading = true;
		error = '';
		try {
			result = await generateHoroscope(currentProfile.zodiac_sign, selectedMood, $locale);
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to generate horoscope';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>{$t('horoscope.title')} - {$t('brand.name')}</title>
</svelte:head>

<div class="page-container">
	<div class="page-header flex flex-col gap-2">
		<div
			class="font-mono-data inline-flex w-fit items-center gap-2 rounded-full bg-surface-container-high/80 px-3 py-1 text-[10px] tracking-widest text-secondary uppercase"
		>
			<span class="h-1.5 w-1.5 animate-pulse rounded-full bg-secondary"></span>
			{$t('dashboard.telemetryActive')}
		</div>
		<h1 class="font-headline text-3xl font-extrabold">
			{$t('horoscope.title')}
		</h1>
		<p class="text-on-surface-variant">
			{$t('horoscope.subtitle')}
		</p>
	</div>

	{#if !result}
		<div class="mx-auto max-w-2xl">
			{#if !hasSign}
				<div class="glass-card mb-6 flex flex-col items-center gap-3 p-6 text-center">
					<span class="text-4xl">✦</span>
					<h2 class="font-headline text-xl font-bold">{$t('dashboard.setSign')}</h2>
					<p class="text-sm text-on-surface-variant">
						{$t('dashboard.setSignPrompt')}
					</p>
					<button
						type="button"
						onclick={() => (showProfileSettings = true)}
						class="btn-primary mt-2"
					>
						<span class="material-symbols-outlined text-[18px]">edit</span>
						{$t('dashboard.editProfile')}
					</button>
				</div>
			{:else}
				<div class="glass-card mb-6 flex flex-col items-center gap-3 p-6 text-center">
					<ZodiacBadge sign={currentProfile.zodiac_sign} size="lg" />
					<h2 class="font-headline text-xl font-bold capitalize">
						{getZodiacTranslation(currentProfile.zodiac_sign, $locale).name || currentProfile.zodiac_sign}
					</h2>
					<p class="text-sm text-on-surface-variant">{$t('horoscope.howFeeling')}</p>
				</div>

				<div class="glass-card mb-6 p-6">
					<label
						for="mood"
						class="font-mono-data mb-4 flex items-center gap-1.5 text-xs tracking-widest text-on-surface-variant uppercase"
					>
						<span class="material-symbols-outlined text-[16px]">neurology</span>
						{$t('horoscope.selectMood')}
					</label>
					<div id="mood" class="grid grid-cols-2 gap-3 sm:grid-cols-4">
						{#each moods as mood}
							<button
								class="rounded-lg border p-3 text-center transition-all
									{selectedMood === mood.id
									? 'scale-105 border-secondary/40 bg-secondary/15 text-secondary shadow-lg shadow-secondary/20'
									: 'border-transparent bg-surface-container-high/60 text-on-surface-variant hover:bg-surface-bright'}"
								onclick={() => (selectedMood = mood.id)}
							>
								<div class="mb-1 text-2xl">{mood.icon}</div>
								<div class="text-xs">{$t(mood.key)}</div>
							</button>
						{/each}
					</div>
				</div>

				{#if error}
					<div class="glass-card mb-6 border-error/30 bg-error/10 p-4">
						<p class="text-sm text-error">{error}</p>
					</div>
				{/if}

				<button
					class="btn-primary flex w-full items-center justify-center gap-2 py-4 text-lg"
					onclick={getHoroscope}
					disabled={loading}
				>
					<span class="material-symbols-outlined text-[20px]"
						>{loading ? 'autorenew' : 'satellite_alt'}</span
					>
					{loading ? $t('horoscope.consulting') : $t('horoscope.generate')}
				</button>

				{#if loading}
					<LoadingSpinner text={$t('horoscope.readingInfluences')} />
				{/if}
			{/if}
		</div>
	{:else}
		<div class="mx-auto max-w-3xl space-y-6">
			<!-- Sign summary -->
			<div class="glass-card flex flex-col items-center gap-3 p-6 text-center">
				<ZodiacBadge sign={result.zodiac_sign} element={result.element} size="lg" />
				<h2 class="font-headline text-xl font-bold capitalize">
					{getZodiacTranslation(result.zodiac_sign, $locale).name || result.zodiac_sign}
				</h2>
				<div class="flex flex-wrap items-center justify-center gap-2">
					<ElementBadge element={result.element} />
					<span
						class="font-mono-data rounded-full bg-surface-container-high px-3 py-1 text-xs tracking-wider text-on-surface-variant uppercase"
						>{$t(`horoscope.mood.${result.mood}`) || result.mood}</span
					>
				</div>
			</div>

			<!-- Today's Theme (hero axiom card) -->
			<div class="glass-card relative overflow-hidden p-6 sm:p-8">
				<div class="pointer-events-none absolute top-0 right-0 p-6 text-white/5 select-none">
					<span class="material-symbols-outlined text-8xl">cyclone</span>
				</div>
				<div class="relative z-10 space-y-3">
					<span
						class="font-mono-data inline-flex items-center gap-1.5 rounded-full bg-primary-container/30 px-3 py-1 text-[10px] tracking-widest text-primary uppercase"
					>
						<span class="material-symbols-outlined text-[14px]">auto_awesome</span>
						{$t('horoscope.theme')}
					</span>
					<p class="gradient-text font-headline text-xl leading-snug font-bold sm:text-2xl">
						{translateHoroscopeTheme(result.theme, $locale)}
					</p>
				</div>
			</div>

			<!-- Pillar cards -->
			<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
				<div class="glass-card glass-card-hover flex flex-col gap-3 p-5">
					<div class="flex items-center gap-2">
						<span
							class="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-container/30 text-primary"
						>
							<span class="material-symbols-outlined text-[18px]">bolt</span>
						</span>
						<h3 class="font-headline text-sm font-semibold text-primary">{$t('horoscope.guidance')}</h3>
					</div>
					<MarkdownText content={formatHoroscopeGuidance(result.guidance, result.zodiac_sign, result.theme, result.mood, $locale)} class="text-sm text-on-surface/80" />
				</div>

				<div class="glass-card glass-card-hover flex flex-col gap-3 p-5">
					<div class="flex items-center gap-2">
						<span
							class="flex h-8 w-8 items-center justify-center rounded-lg bg-secondary-container/30 text-secondary"
						>
							<span class="material-symbols-outlined text-[18px]">dark_mode</span>
						</span>
						<h3 class="font-headline text-sm font-semibold text-secondary">{$t('horoscope.reflection')}</h3>
					</div>
					<MarkdownText content={formatHoroscopeReflection(result.reflection, result.theme, $locale)} class="text-sm text-on-surface/80 italic" />
				</div>

				<div class="glass-card glass-card-hover flex flex-col gap-3 p-5">
					<div class="flex items-center gap-2">
						<span
							class="flex h-8 w-8 items-center justify-center rounded-lg bg-tertiary-container/30 text-tertiary"
						>
							<span class="material-symbols-outlined text-[18px]">auto_awesome</span>
						</span>
						<h3 class="font-headline text-sm font-semibold text-tertiary">{$t('horoscope.opportunity')}</h3>
					</div>
					<MarkdownText content={formatHoroscopeOpportunity(result.opportunity, result.theme, $locale)} class="text-sm text-on-surface/80" />
				</div>

				<div class="glass-card glass-card-hover flex flex-col gap-3 p-5">
					<div class="flex items-center gap-2">
						<span
							class="flex h-8 w-8 items-center justify-center rounded-lg bg-error-container/30 text-error"
						>
							<span class="material-symbols-outlined text-[18px]">shield</span>
						</span>
						<h3 class="font-headline text-sm font-semibold text-error">{$t('horoscope.caution')}</h3>
					</div>
					<MarkdownText content={formatHoroscopeCaution(result.caution, result.theme, result.element, $locale)} class="text-sm text-on-surface/80" />
				</div>
			</div>

			<!-- Prolog reasoning trace -->
			{#if result.reasoning?.length}
				<div class="glass-card space-y-4 p-6">
					<div class="flex items-center gap-3">
						<span
							class="h-2.5 w-2.5 animate-pulse rounded-full bg-secondary shadow-[0_0_10px_#4cd7f6]"
						></span>
						<h3 class="font-headline text-sm font-semibold text-on-surface">
							{$t('horoscope.prologTrace')}
						</h3>
					</div>
					<div class="font-mono-data space-y-2">
						{#each result.reasoning as step, i}
							<ReasoningStep {step} index={i} />
						{/each}
					</div>
				</div>
			{/if}

			<button
				class="btn-secondary flex w-full items-center justify-center gap-2"
				onclick={() => (result = null)}
			>
				<span class="material-symbols-outlined text-[18px]">refresh</span>
				{$t('horoscope.newHoroscope')}
			</button>
		</div>
	{/if}
</div>

<ProfileSettingsModal bind:open={showProfileSettings} />
