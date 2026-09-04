<script lang="ts">
	import { profile } from '$lib/stores';
	import { generateHoroscope } from '$lib/utils/api';
	import type { HoroscopeResult } from '$lib/types';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import ZodiacBadge from '$lib/components/ZodiacBadge.svelte';
	import ElementBadge from '$lib/components/ElementBadge.svelte';
	import ReasoningStep from '$lib/components/ReasoningStep.svelte';
	import ProfileSettingsModal from '$lib/components/ProfileSettingsModal.svelte';

	const moods = [
		{ id: 'happy', label: 'Happy', icon: '😄' },
		{ id: 'calm', label: 'Calm', icon: '😌' },
		{ id: 'excited', label: 'Excited', icon: '🤩' },
		{ id: 'uncertain', label: 'Uncertain', icon: '😕' },
		{ id: 'stressed', label: 'Stressed', icon: '😓' },
		{ id: 'reflective', label: 'Reflective', icon: '🧘' },
		{ id: 'curious', label: 'Curious', icon: '🤔' },
		{ id: 'neutral', label: 'Neutral', icon: '😐' },
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
			result = await generateHoroscope(currentProfile.zodiac_sign, selectedMood);
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to generate horoscope';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Horoscope - AstroLogic</title>
</svelte:head>

<div class="page-container">
	<div class="page-header flex flex-col gap-2">
		<div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-container-high/80 text-secondary font-mono-data text-[10px] uppercase tracking-widest w-fit">
			<span class="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
			Telemetry Stream Active
		</div>
		<h1 class="text-3xl font-extrabold font-headline">Daily <span class="gradient-text">Horoscope</span></h1>
		<p class="text-on-surface-variant">Personalized horoscope for {hasSign ? currentProfile.zodiac_sign : 'your sign'}</p>
	</div>

	{#if !result}
		<div class="max-w-2xl mx-auto">
			{#if !hasSign}
				<div class="glass-card p-6 mb-6 text-center flex flex-col items-center gap-3">
					<span class="text-4xl">✦</span>
					<h2 class="text-xl font-bold font-headline">Set Your Zodiac Sign</h2>
					<p class="text-on-surface-variant text-sm">Select your zodiac sign to receive personalized horoscopes.</p>
					<button
						type="button"
						onclick={() => showProfileSettings = true}
						class="btn-primary mt-2"
					>
						<span class="material-symbols-outlined text-[18px]">edit</span>
						Edit Profile
					</button>
				</div>
			{:else}
				<div class="glass-card p-6 mb-6 text-center flex flex-col items-center gap-3">
					<ZodiacBadge sign={currentProfile.zodiac_sign} size="lg" />
					<h2 class="text-xl font-bold capitalize font-headline">{currentProfile.zodiac_sign}</h2>
					<p class="text-on-surface-variant text-sm">How are you feeling today?</p>
				</div>

				<div class="glass-card p-6 mb-6">
					<label for="mood" class="flex items-center gap-1.5 text-xs font-mono-data uppercase tracking-widest text-on-surface-variant mb-4">
						<span class="material-symbols-outlined text-[16px]">neurology</span>
						Select Your Mood
					</label>
					<div id="mood" class="grid grid-cols-4 gap-3">
						{#each moods as mood}
							<button
								class="p-3 rounded-lg text-center transition-all border
									{selectedMood === mood.id
										? 'bg-secondary/15 border-secondary/40 text-secondary shadow-lg shadow-secondary/20 scale-105'
										: 'bg-surface-container-high/60 border-transparent text-on-surface-variant hover:bg-surface-bright'}"
								onclick={() => selectedMood = mood.id}
							>
								<div class="text-2xl mb-1">{mood.icon}</div>
								<div class="text-xs">{mood.label}</div>
							</button>
						{/each}
					</div>
				</div>

				{#if error}
					<div class="glass-card p-4 mb-6 border-error/30 bg-error/10">
						<p class="text-error text-sm">{error}</p>
					</div>
				{/if}

				<button class="btn-primary w-full text-lg py-4 flex items-center justify-center gap-2" onclick={getHoroscope} disabled={loading}>
					<span class="material-symbols-outlined text-[20px]">{loading ? 'autorenew' : 'satellite_alt'}</span>
					{loading ? 'Consulting the stars...' : 'Generate Horoscope'}
				</button>

				{#if loading}
					<LoadingSpinner text="Reading the cosmic influences..." />
				{/if}
			{/if}
		</div>
	{:else}
		<div class="max-w-3xl mx-auto space-y-6">
			<!-- Sign summary -->
			<div class="glass-card p-6 text-center flex flex-col items-center gap-3">
				<ZodiacBadge sign={result.zodiac_sign} element={result.element} size="lg" />
				<h2 class="text-xl font-bold capitalize font-headline">{result.zodiac_sign}</h2>
				<div class="flex items-center gap-2 flex-wrap justify-center">
					<ElementBadge element={result.element} />
					<span class="px-3 py-1 rounded-full bg-surface-container-high text-on-surface-variant text-xs font-mono-data uppercase tracking-wider">{result.mood} mood</span>
				</div>
			</div>

			<!-- Today's Theme (hero axiom card) -->
			<div class="relative overflow-hidden glass-card p-6 sm:p-8">
				<div class="absolute top-0 right-0 p-6 text-white/5 pointer-events-none select-none">
					<span class="material-symbols-outlined text-8xl">cyclone</span>
				</div>
				<div class="relative z-10 space-y-3">
					<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary-container/30 text-primary font-mono-data text-[10px] uppercase tracking-widest">
						<span class="material-symbols-outlined text-[14px]">auto_awesome</span>
						Today's Theme
					</span>
					<p class="text-xl sm:text-2xl font-bold gradient-text font-headline leading-snug">{result.theme}</p>
				</div>
			</div>

			<!-- Pillar cards -->
			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<div class="glass-card glass-card-hover p-5 flex flex-col gap-3">
					<div class="flex items-center gap-2">
						<span class="w-8 h-8 rounded-lg bg-primary-container/30 text-primary flex items-center justify-center">
							<span class="material-symbols-outlined text-[18px]">bolt</span>
						</span>
						<h3 class="text-sm font-semibold text-primary font-headline">Guidance</h3>
					</div>
					<p class="text-on-surface/80 text-sm">{result.guidance}</p>
				</div>

				<div class="glass-card glass-card-hover p-5 flex flex-col gap-3">
					<div class="flex items-center gap-2">
						<span class="w-8 h-8 rounded-lg bg-secondary-container/30 text-secondary flex items-center justify-center">
							<span class="material-symbols-outlined text-[18px]">dark_mode</span>
						</span>
						<h3 class="text-sm font-semibold text-secondary font-headline">Reflection</h3>
					</div>
					<p class="text-on-surface/80 text-sm italic">{result.reflection}</p>
				</div>

				<div class="glass-card glass-card-hover p-5 flex flex-col gap-3">
					<div class="flex items-center gap-2">
						<span class="w-8 h-8 rounded-lg bg-tertiary-container/30 text-tertiary flex items-center justify-center">
							<span class="material-symbols-outlined text-[18px]">auto_awesome</span>
						</span>
						<h3 class="text-sm font-semibold text-tertiary font-headline">Opportunity</h3>
					</div>
					<p class="text-on-surface/80 text-sm">{result.opportunity}</p>
				</div>

				<div class="glass-card glass-card-hover p-5 flex flex-col gap-3">
					<div class="flex items-center gap-2">
						<span class="w-8 h-8 rounded-lg bg-error-container/30 text-error flex items-center justify-center">
							<span class="material-symbols-outlined text-[18px]">shield</span>
						</span>
						<h3 class="text-sm font-semibold text-error font-headline">Caution</h3>
					</div>
					<p class="text-on-surface/80 text-sm">{result.caution}</p>
				</div>
			</div>

			<!-- Prolog reasoning trace -->
			{#if result.reasoning?.length}
				<div class="glass-card p-6 space-y-4">
					<div class="flex items-center gap-3">
						<span class="w-2.5 h-2.5 rounded-full bg-secondary animate-pulse shadow-[0_0_10px_#4cd7f6]"></span>
						<h3 class="text-sm font-semibold text-on-surface font-headline">Prolog Reasoning Trace</h3>
					</div>
					<div class="space-y-2 font-mono-data">
						{#each result.reasoning as step, i}
							<ReasoningStep {step} index={i} />
						{/each}
					</div>
				</div>
			{/if}

			<button class="btn-secondary w-full flex items-center justify-center gap-2" onclick={() => result = null}>
				<span class="material-symbols-outlined text-[18px]">refresh</span>
				New Horoscope
			</button>
		</div>
	{/if}
</div>

<ProfileSettingsModal bind:open={showProfileSettings} />
