<script lang="ts">
	import { onMount } from 'svelte';
	import { profile } from '$lib/stores';
	import { ZODIAC_SYMBOLS, ELEMENT_COLORS, ELEMENT_ICONS } from '$lib/types';
	import { fetchHistory } from '$lib/utils/api';
	import type { DrawnCard, HistoryItem } from '$lib/types';
	import ZodiacBadge from '$lib/components/ZodiacBadge.svelte';
	import ElementBadge from '$lib/components/ElementBadge.svelte';
	import TarotCard from '$lib/components/TarotCard.svelte';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import ProfileSettingsModal from '$lib/components/ProfileSettingsModal.svelte';
	import MarkdownText from '$lib/components/MarkdownText.svelte';

	let recentReadings = $state<HistoryItem[]>([]);
	let loading = $state(true);
	let refreshing = $state(false);

	onMount(async () => {
		try {
			recentReadings = await fetchHistory();
		} catch {
			// API may not be running
		} finally {
			loading = false;
		}
	});

	async function refresh() {
		refreshing = true;
		try {
			recentReadings = await fetchHistory();
		} catch {
			// API may not be running
		} finally {
			refreshing = false;
		}
	}

	const currentProfile = $derived($profile);
	const hasSign = $derived(!!currentProfile.zodiac_sign);
	const symbol = $derived(hasSign ? ZODIAC_SYMBOLS[currentProfile.zodiac_sign] : '✦');
	const element = $derived(
		currentProfile.zodiac_sign === 'aries' ||
			currentProfile.zodiac_sign === 'leo' ||
			currentProfile.zodiac_sign === 'sagittarius'
			? 'fire'
			: currentProfile.zodiac_sign === 'taurus' ||
				  currentProfile.zodiac_sign === 'virgo' ||
				  currentProfile.zodiac_sign === 'capricorn'
				? 'earth'
				: currentProfile.zodiac_sign === 'gemini' ||
					  currentProfile.zodiac_sign === 'libra' ||
					  currentProfile.zodiac_sign === 'aquarius'
					? 'air'
					: 'water'
	);

	const greeting = $derived(() => {
		const hour = new Date().getHours();
		if (hour < 12) return 'Good morning';
		if (hour < 18) return 'Good afternoon';
		return 'Good evening';
	});

	type Tint = 'primary' | 'secondary' | 'tertiary';

	const tintStyles: Record<
		Tint,
		{
			icon: string;
			iconBg: string;
			badge: string;
			button: string;
			blob: string;
			titleHover: string;
		}
	> = {
		primary: {
			icon: 'text-primary',
			iconBg: 'from-primary-container to-surface-container-high',
			badge: 'bg-primary/10 text-primary',
			button: 'bg-primary-container text-on-primary hover:bg-primary',
			blob: 'bg-primary-container/20 group-hover:bg-primary-container/35',
			titleHover: 'group-hover:text-primary'
		},
		secondary: {
			icon: 'text-secondary',
			iconBg: 'from-secondary-container to-surface-container-high',
			badge: 'bg-secondary/10 text-secondary',
			button: 'bg-surface-container text-on-surface hover:bg-surface-container-high',
			blob: 'bg-secondary-container/20 group-hover:bg-secondary-container/35',
			titleHover: 'group-hover:text-secondary'
		},
		tertiary: {
			icon: 'text-tertiary',
			iconBg: 'from-tertiary-container to-surface-container-high',
			badge: 'bg-tertiary/10 text-tertiary',
			button: 'bg-surface-container text-on-surface hover:bg-surface-container-high',
			blob: 'bg-tertiary-container/25 group-hover:bg-tertiary-container/40',
			titleHover: 'group-hover:text-tertiary'
		}
	};

	const quickActions: Array<{
		href: string;
		icon: string;
		label: string;
		badge: string;
		description: string;
		cta: string;
		ctaIcon: string;
		tint: Tint;
	}> = [
		{
			href: '/reading',
			icon: 'style',
			label: 'Tarot Reading',
			badge: 'Daily Draw',
			description: "Shuffle the deck of symbolic archetypes to unveil today's currents.",
			cta: 'Draw Cards',
			ctaIcon: 'arrow_forward',
			tint: 'primary'
		},
		{
			href: '/horoscope',
			icon: 'explore',
			label: 'Horoscope',
			badge: 'Daily Guidance',
			description: 'Personalized celestial guidance mapped to your sign, refreshed daily.',
			cta: 'View Horoscope',
			ctaIcon: 'north_east',
			tint: 'secondary'
		},
		{
			href: '/compatibility',
			icon: 'all_inclusive',
			label: 'Compatibility',
			badge: 'Elemental Match',
			description: 'Evaluate elemental harmony and compatibility between two signs.',
			cta: 'Analyze Bond',
			ctaIcon: 'fingerprint',
			tint: 'tertiary'
		},
		{
			href: '/chat',
			icon: 'psychology',
			label: 'AI Guide',
			badge: 'Online',
			description: 'Ask the Prolog-backed reasoning engine for deterministic insight.',
			cta: 'Ask the Oracle',
			ctaIcon: 'chat_bubble',
			tint: 'secondary'
		}
	];

	const latestReading = $derived(recentReadings[0]);

	const latestCards = $derived.by<DrawnCard[]>(() => {
		if (!latestReading) return [];
		try {
			const parsed = JSON.parse(latestReading.cards_json);
			return Array.isArray(parsed) ? parsed.slice(0, 3) : [];
		} catch {
			return [];
		}
	});

	const latestThemes = $derived.by<string[]>(() => {
		if (!latestReading) return [];
		try {
			const parsed = JSON.parse(latestReading.themes_json);
			return Array.isArray(parsed) ? parsed.slice(0, 4) : [];
		} catch {
			return [];
		}
	});

	let showReadingDetails = $state(false);
	let showProfileSettings = $state(false);

	// Local-only journal note widget -- not persisted to any backend/API.
	let journalNote = $state('');
	let journalSaved = $state(false);
	function saveJournalNote() {
		if (!journalNote.trim()) return;
		journalSaved = true;
		journalNote = '';
		setTimeout(() => {
			journalSaved = false;
		}, 2400);
	}
</script>

<svelte:head>
	<title>Dashboard - AstroLogic</title>
</svelte:head>

<div class="page-container relative">
	<!-- Ambient glow blobs -->
	<div
		class="pointer-events-none absolute -top-4 left-1/4 h-96 w-96 rounded-full bg-primary-container/15 blur-[120px]"
	></div>
	<div
		class="pointer-events-none absolute top-8 right-1/4 h-80 w-80 rounded-full bg-secondary-container/10 blur-[100px]"
	></div>

	<div class="relative z-10 flex flex-col gap-8">
		<!-- Header: Personalized greeting -->
		<section class="flex flex-col gap-6 pb-2 lg:flex-row lg:items-end lg:justify-between">
			<div class="flex max-w-2xl flex-col gap-3">
				<div class="flex flex-wrap items-center gap-2">
					{#if hasSign}
						<span
							class="font-mono-data inline-flex items-center gap-1.5 rounded-full bg-surface-container-high px-3 py-1 text-[10px] font-semibold tracking-wider text-primary uppercase"
						>
							<span class="text-sm">{symbol}</span>
							{currentProfile.zodiac_sign}
						</span>
						<span
							class="font-mono-data inline-flex items-center gap-1.5 rounded-full bg-surface-container-high px-3 py-1 text-[10px] font-semibold tracking-wider text-secondary uppercase"
						>
							<span class="h-1.5 w-1.5 rounded-full bg-secondary"></span>
							{element} Dominant
						</span>
					{:else}
						<button
							type="button"
							onclick={() => (showProfileSettings = true)}
							class="font-mono-data inline-flex items-center gap-1.5 rounded-full bg-primary/10 px-3 py-1 text-[10px] font-semibold tracking-wider text-primary uppercase transition-colors hover:bg-primary/20"
						>
							<span class="text-sm">✦</span> Set Your Zodiac Sign
						</button>
					{/if}
					{#if currentProfile.preferred_style}
						<span
							class="font-mono-data inline-flex items-center gap-1.5 rounded-full bg-surface-container-high px-3 py-1 text-[10px] font-semibold tracking-wider text-tertiary uppercase"
						>
							{currentProfile.preferred_style} Style
						</span>
					{/if}
				</div>
				<div class="flex flex-col">
					<span
						class="font-mono-data text-[11px] tracking-widest text-on-surface-variant/70 uppercase"
						>Cosmic Dashboard &bull; Reflection Mode</span
					>
					<h1
						class="font-headline mt-1 text-3xl font-bold tracking-tight text-on-surface md:text-4xl"
					>
						{greeting()}, <span class="gradient-text">{currentProfile.nickname}</span>
					</h1>
					<p class="mt-1 text-on-surface-variant">Welcome to your cosmic dashboard.</p>
				</div>
			</div>

			<!-- Telemetry strip -->
			<div class="flex flex-col items-start gap-3 sm:flex-row sm:items-center lg:self-end">
				<div
					class="flex items-center gap-3 rounded-xl bg-surface-container-low px-4 py-2.5 shadow-md"
				>
					<div class="h-2.5 w-2.5 rounded-full bg-secondary shadow-lg"></div>
					<div class="flex flex-col">
						<span
							class="font-mono-data text-[10px] tracking-wider text-on-surface-variant uppercase"
							>Reading Archive</span
						>
						<span class="font-mono-data text-sm font-semibold text-on-surface">
							{recentReadings.length}
							{recentReadings.length === 1 ? 'Reading' : 'Readings'} Logged
						</span>
					</div>
				</div>
				<button
					type="button"
					onclick={refresh}
					title="Refresh reading history"
					class="inline-flex items-center justify-center rounded-xl bg-surface-container p-2.5 text-on-surface-variant shadow-sm transition-all duration-300 hover:bg-surface-container-high hover:text-on-surface"
				>
					<span class="material-symbols-outlined text-xl {refreshing ? 'animate-spin' : ''}"
						>sync</span
					>
				</button>
			</div>
		</section>

		<!-- Quick Action Portals -->
		<section class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
			{#each quickActions as action}
				<a
					href={action.href}
					class="group relative flex flex-col justify-between overflow-hidden rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl"
				>
					<div
						class="absolute -top-12 -right-12 h-32 w-32 rounded-full {tintStyles[action.tint]
							.blob} blur-2xl transition-all"
					></div>
					<div class="relative z-10 flex flex-col gap-4">
						<div class="flex items-center justify-between">
							<div
								class="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br {tintStyles[
									action.tint
								].iconBg} {tintStyles[action.tint].icon} shadow-lg"
							>
								<span class="material-symbols-outlined text-2xl">{action.icon}</span>
							</div>
							<span
								class="font-mono-data inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[10px] tracking-wider uppercase {tintStyles[
									action.tint
								].badge}"
							>
								{#if action.badge === 'Online'}
									<span class="h-1.5 w-1.5 animate-ping rounded-full bg-secondary"></span>
								{/if}
								{action.badge}
							</span>
						</div>
						<div>
							<h3
								class="font-headline text-lg font-semibold text-on-surface transition-colors {tintStyles[
									action.tint
								].titleHover}"
							>
								{action.label}
							</h3>
							<p class="mt-1.5 text-sm text-on-surface-variant">{action.description}</p>
						</div>
					</div>
					<div class="relative z-10 mt-6 pt-6">
						<span
							class="flex w-full items-center justify-between rounded-xl px-4 py-2.5 text-sm font-medium shadow-md transition-all {tintStyles[
								action.tint
							].button}"
						>
							{action.cta}
							<span
								class="material-symbols-outlined text-lg transition-transform group-hover:translate-x-1"
								>{action.ctaIcon}</span
							>
						</span>
					</div>
				</a>
			{/each}
		</section>

		<!-- Bento grid: Profile snapshot + Recent Reading spotlight -->
		<section class="grid grid-cols-1 items-start gap-8 lg:grid-cols-12">
			<!-- Left: Your Cosmic Profile -->
			<div class="flex flex-col gap-6 lg:col-span-5">
				<div
					class="flex flex-col gap-6 rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md"
				>
					<div class="flex items-center gap-2.5">
						<span class="material-symbols-outlined text-xl text-secondary">satellite_alt</span>
						<h2 class="font-headline text-lg font-semibold text-on-surface">Your Cosmic Profile</h2>
						<button
							type="button"
							onclick={() => (showProfileSettings = true)}
							class="ml-auto inline-flex items-center gap-1.5 rounded-full bg-surface-container px-3 py-1 text-xs font-medium text-on-surface-variant transition-colors hover:bg-surface-container-high"
						>
							<span class="material-symbols-outlined text-sm">edit</span>
							Edit
						</button>
					</div>

					<div class="flex items-center gap-4 rounded-xl bg-surface-container-low p-5">
						<ZodiacBadge sign={currentProfile.zodiac_sign} {element} size="lg" />
						<div class="flex flex-col">
							<span class="font-mono-data text-[10px] tracking-wider text-secondary uppercase"
								>Sun Sign</span
							>
							<h4 class="font-headline text-lg font-semibold text-on-surface capitalize">
								{currentProfile.zodiac_sign}
							</h4>
							<p class="text-sm text-on-surface-variant">Ruled by the element of {element}</p>
						</div>
					</div>

					<div class="flex flex-col gap-3">
						<div
							class="flex items-center justify-between rounded-xl bg-surface-container-high/60 p-3.5"
						>
							<div class="flex items-center gap-3">
								<div
									class="flex h-8 w-8 items-center justify-center rounded-lg bg-surface-container text-lg"
									style:color={ELEMENT_COLORS[element]}
								>
									{ELEMENT_ICONS[element]}
								</div>
								<div class="flex flex-col">
									<span class="text-sm font-medium text-on-surface">Elemental Affinity</span>
									<span class="text-xs text-on-surface-variant">Your dominant elemental energy</span
									>
								</div>
							</div>
							<ElementBadge {element} size="sm" />
						</div>

						{#if currentProfile.birth_date}
							<div
								class="flex items-center justify-between rounded-xl bg-surface-container-high/60 p-3.5"
							>
								<div class="flex items-center gap-3">
									<div
										class="flex h-8 w-8 items-center justify-center rounded-lg bg-surface-container text-primary"
									>
										<span class="material-symbols-outlined text-lg">cake</span>
									</div>
									<div class="flex flex-col">
										<span class="text-sm font-medium text-on-surface">Birth Date</span>
										<span class="text-xs text-on-surface-variant">Used to determine your sign</span>
									</div>
								</div>
								<span class="font-mono-data text-xs text-on-surface-variant"
									>{currentProfile.birth_date}</span
								>
							</div>
						{/if}

						<div
							class="flex items-center justify-between rounded-xl bg-surface-container-high/60 p-3.5"
						>
							<div class="flex items-center gap-3">
								<div
									class="flex h-8 w-8 items-center justify-center rounded-lg bg-surface-container text-tertiary"
								>
									<span class="material-symbols-outlined text-lg">style</span>
								</div>
								<div class="flex flex-col">
									<span class="text-sm font-medium text-on-surface">Preferred Style</span>
									<span class="text-xs text-on-surface-variant">How your readings are phrased</span>
								</div>
							</div>
							<span class="font-mono-data text-xs text-tertiary capitalize"
								>{currentProfile.preferred_style || 'balanced'}</span
							>
						</div>
					</div>

					<!-- Decorative ambient panel (illustrative only, no live data) -->
					<div
						class="relative flex h-28 w-full items-end overflow-hidden rounded-xl bg-gradient-to-br from-primary-container/30 via-surface-container-low to-secondary-container/20 shadow-inner"
					>
						<div class="cosmic-stars absolute inset-0 opacity-50"></div>
						<span
							class="font-mono-data relative z-10 flex items-center gap-2 p-3.5 text-[11px] text-primary"
						>
							<span class="material-symbols-outlined text-base">lens_blur</span>
							Every reading unfolds within the greater celestial rhythm.
						</span>
					</div>
				</div>
			</div>

			<!-- Right: Recent Reading Spotlight -->
			<div class="flex flex-col gap-6 lg:col-span-7">
				<div
					class="flex flex-col gap-6 rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md sm:p-8"
				>
					{#if loading}
						<LoadingSpinner text="Consulting the archive..." />
					{:else if latestReading}
						<div class="flex flex-wrap items-center justify-between gap-4">
							<div class="flex flex-col">
								<div class="flex items-center gap-2">
									<span class="font-mono-data text-[10px] tracking-wider text-primary uppercase"
										>Archival Spotlight</span
									>
									<span class="text-on-surface-variant">&bull;</span>
									<span class="text-sm text-on-surface-variant">{latestReading.created_at}</span>
								</div>
								<h2 class="font-headline mt-1 text-xl font-semibold text-on-surface">
									{latestReading.question || 'Tarot Reading'}
								</h2>
							</div>
							<a
								href="/history"
								class="inline-flex items-center gap-1.5 rounded-full bg-surface-container px-3 py-1.5 text-sm text-on-surface transition-colors hover:bg-surface-container-high"
							>
								Full Spread
								<span class="material-symbols-outlined text-base">open_in_new</span>
							</a>
						</div>

						{#if latestCards.length > 0}
							<div class="grid grid-cols-3 gap-4">
								{#each latestCards as card, i (card.position + i)}
									<div
										class="flex flex-col gap-2 rounded-xl bg-surface-container-low p-3 shadow-md"
									>
										<TarotCard {card} index={i} revealed={true} />
										<span class="truncate text-center text-xs font-medium text-on-surface-variant"
											>{card.position}</span
										>
									</div>
								{/each}
							</div>
						{/if}

						{#if latestThemes.length > 0}
							<div class="flex flex-wrap gap-2">
								{#each latestThemes as theme}
									<span
										class="font-mono-data inline-flex items-center rounded-full bg-surface-container px-2.5 py-1 text-[10px] tracking-wider text-secondary uppercase"
										>{theme}</span
									>
								{/each}
							</div>
						{/if}

						<!-- AI interpretation -->
						<div class="flex flex-col gap-3 rounded-xl bg-surface-container-low p-5">
							<div class="flex items-center gap-2 text-secondary">
								<span class="material-symbols-outlined text-lg">auto_awesome</span>
								<span class="font-mono-data text-[11px] font-semibold tracking-wider uppercase"
									>AI Interpretation</span
								>
							</div>
							<MarkdownText content={latestReading.ai_interpretation} />

							<div class="flex flex-col gap-2 pt-2">
								<button
									type="button"
									onclick={() => (showReadingDetails = !showReadingDetails)}
									class="font-mono-data inline-flex w-fit items-center gap-2 rounded-full bg-surface-container-high px-3 py-1.5 text-[11px] text-secondary shadow-sm transition-all hover:bg-surface-bright"
								>
									<span class="h-2 w-2 rounded-full bg-secondary"></span>
									Reading Details
									<span class="material-symbols-outlined text-sm"
										>{showReadingDetails ? 'unfold_less' : 'unfold_more'}</span
									>
								</button>
								{#if showReadingDetails}
									<div
										class="font-mono-data flex flex-col gap-1.5 rounded-xl bg-surface-container-lowest p-4 text-[11px] text-on-surface-variant shadow-inner"
									>
										<div>
											category: <span class="text-secondary">{latestReading.category}</span>
										</div>
										<div>
											spread_type: <span class="text-secondary">{latestReading.spread_type}</span>
										</div>
										<div>
											zodiac_sign: <span class="text-secondary">{latestReading.zodiac_sign}</span>
										</div>
									</div>
								{/if}
							</div>
						</div>
					{:else}
						<div class="flex flex-col items-center gap-3 py-8 text-center">
							<span class="material-symbols-outlined text-4xl text-on-surface-variant/60"
								>auto_stories</span
							>
							<p class="text-on-surface-variant">No readings yet. Start your first reading!</p>
							<a href="/reading" class="btn-primary mt-2 inline-block">Begin Reading</a>
						</div>
					{/if}
				</div>
			</div>
		</section>

		<!-- Journal micro-widget (local only, not persisted) -->
		<section
			class="flex flex-col items-start justify-between gap-4 rounded-2xl bg-surface-container-lowest/80 p-6 shadow-lg backdrop-blur-md md:flex-row md:items-center"
		>
			<div class="flex items-center gap-4">
				<div
					class="flex h-10 w-10 items-center justify-center rounded-xl bg-surface-container text-primary"
				>
					<span class="material-symbols-outlined text-xl">edit_note</span>
				</div>
				<div class="flex flex-col">
					<span class="font-headline text-base font-semibold text-on-surface"
						>Quick Reflection Journal</span
					>
					<span class="text-sm text-on-surface-variant"
						>Jot down a thought before it drifts away.</span
					>
				</div>
			</div>
			<div class="flex w-full items-center gap-3 md:w-auto">
				<input
					type="text"
					bind:value={journalNote}
					placeholder="Record intuitive insight..."
					class="w-full rounded-xl bg-surface-container-low px-4 py-2 text-sm text-on-surface placeholder:text-on-surface-variant/50 focus:ring-1 focus:ring-secondary focus:outline-none md:w-80"
				/>
				<button
					type="button"
					onclick={saveJournalNote}
					class="shrink-0 rounded-xl px-4 py-2 text-sm font-medium shadow-md transition-all {journalSaved
						? 'bg-primary text-on-primary'
						: 'bg-secondary-container text-on-secondary hover:bg-secondary'}"
				>
					{journalSaved ? 'Saved ✓' : 'Save Note'}
				</button>
			</div>
		</section>
	</div>
</div>

<ProfileSettingsModal bind:open={showProfileSettings} />
