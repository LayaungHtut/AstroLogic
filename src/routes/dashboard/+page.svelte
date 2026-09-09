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
	import { locale, t, getZodiacTranslation, formatElement } from '$lib/i18n';

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

	const zodiacTrans = $derived(getZodiacTranslation(currentProfile.zodiac_sign, $locale));
	const localizedElement = $derived(formatElement(element, $locale));

	const greeting = $derived(() => {
		const hour = new Date().getHours();
		if ($locale === 'my') {
			if (hour < 12) return 'မင်္ဂလာနံနက်ခင်းပါ';
			if (hour < 18) return 'မင်္ဂလာနေ့လယ်ခင်းပါ';
			return 'မင်္ဂလာညနေခင်းပါ';
		}
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

	const quickActions = $derived([
		{
			href: '/reading',
			icon: 'style',
			label: $locale === 'my' ? 'တားရော့ဗေဒင်မေးမည်' : 'Tarot Reading',
			badge: $locale === 'my' ? 'နေ့စဉ်ဟောကိန်း' : 'Daily Draw',
			description: $locale === 'my' ? 'သင်္ကေတတားရော့ကတ်များကို မွှေနှောက်ဆွဲယူပြီး ယနေ့အတွက် လမ်းညွှန်ချက်ရယူပါ။' : "Shuffle the deck of symbolic archetypes to unveil today's currents.",
			cta: $locale === 'my' ? 'ကတ်ဆွဲမည်' : 'Draw Cards',
			ctaIcon: 'arrow_forward',
			tint: 'primary' as Tint
		},
		{
			href: '/horoscope',
			icon: 'explore',
			label: $locale === 'my' ? 'နေ့စဉ်ဟောစာတမ်း' : 'Horoscope',
			badge: $locale === 'my' ? 'နေ့စဉ်လမ်းညွှန်' : 'Daily Guidance',
			description: $locale === 'my' ? 'သင့်ရာသီခွင်အတွက် နေ့စဉ်အသစ်ထုတ်ပြန်ပေးသော နက္ခတ်ဟောစာတမ်း။' : 'Personalized celestial guidance mapped to your sign, refreshed daily.',
			cta: $locale === 'my' ? 'ဟောစာတမ်းကြည့်မည်' : 'View Horoscope',
			ctaIcon: 'north_east',
			tint: 'secondary' as Tint
		},
		{
			href: '/compatibility',
			icon: 'all_inclusive',
			label: $locale === 'my' ? 'ရာသီခွင်လိုက်ဖက်ညီမှု' : 'Compatibility',
			badge: $locale === 'my' ? 'ဓာတ်သဟဇာတ' : 'Elemental Match',
			description: $locale === 'my' ? 'ရာသီခွင်နှစ်ခုအကြား ဓာတ်သဘောနှင့် သဟဇာတဖြစ်မှုကို လေ့လာဆန်းစစ်ပါ။' : 'Evaluate elemental harmony and compatibility between two signs.',
			cta: $locale === 'my' ? 'လိုက်ဖက်မှုဆန်းစစ်မည်' : 'Analyze Bond',
			ctaIcon: 'fingerprint',
			tint: 'tertiary' as Tint
		},
		{
			href: '/chat',
			icon: 'psychology',
			label: $locale === 'my' ? 'AI နက္ခတ်လမ်းပြ' : 'AI Guide',
			badge: $locale === 'my' ? 'အွန်လိုင်း' : 'Online',
			description: $locale === 'my' ? 'Prolog ယုတ္တိဗေဒစနစ်ဖြင့် သက်သေပြအဖြေထုတ်ပေးသော AI ကို မေးမြန်းပါ။' : 'Ask the Prolog-backed reasoning engine for deterministic insight.',
			cta: $locale === 'my' ? 'AI ကို မေးမည်' : 'Ask the Oracle',
			ctaIcon: 'chat_bubble',
			tint: 'secondary' as Tint
		}
	]);

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
	<title>{$t('nav.dashboard')} - {$t('brand.name')}</title>
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
							{zodiacTrans.name || currentProfile.zodiac_sign}
						</span>
						<span
							class="font-mono-data inline-flex items-center gap-1.5 rounded-full bg-surface-container-high px-3 py-1 text-[10px] font-semibold tracking-wider text-secondary uppercase"
						>
							<span class="h-1.5 w-1.5 rounded-full bg-secondary"></span>
							{localizedElement}
						</span>
					{:else}
						<button
							type="button"
							onclick={() => (showProfileSettings = true)}
							class="font-mono-data inline-flex items-center gap-1.5 rounded-full bg-primary/10 px-3 py-1 text-[10px] font-semibold tracking-wider text-primary uppercase transition-colors hover:bg-primary/20"
						>
							<span class="text-sm">✦</span> {$t('dashboard.setSign')}
						</button>
					{/if}
					{#if currentProfile.preferred_style}
						<span
							class="font-mono-data inline-flex items-center gap-1.5 rounded-full bg-surface-container-high px-3 py-1 text-[10px] font-semibold tracking-wider text-tertiary uppercase"
						>
							{currentProfile.preferred_style}
						</span>
					{/if}
				</div>
				<div class="flex flex-col">
					<span
						class="font-mono-data text-[11px] tracking-widest text-on-surface-variant/70 uppercase"
						>{$t('dashboard.telemetryActive')}</span
					>
					<h1
						class="font-headline mt-1 text-3xl font-bold tracking-tight text-on-surface md:text-4xl"
					>
						{greeting()}, <span class="gradient-text">{currentProfile.nickname || 'Explorer'}</span>
					</h1>
					<p class="mt-1 text-on-surface-variant">
						{$locale === 'my' ? 'သင်၏ နက္ခတ်ဗေဒင် ဒက်ရှ်ဘုတ်မှ ကြိုဆိုပါသည်။' : 'Welcome to your cosmic dashboard.'}
					</p>
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
							>{$locale === 'my' ? 'ဗေဒင်မှတ်တမ်း အရေအတွက်' : 'Reading Archive'}</span
						>
						<span class="font-mono-data text-sm font-semibold text-on-surface">
							{recentReadings.length}
							{$locale === 'my' ? 'ကြိမ် မေးမြန်းထားသည်' : (recentReadings.length === 1 ? 'Reading Logged' : 'Readings Logged')}
						</span>
					</div>
				</div>
				<button
					type="button"
					onclick={refresh}
					title={$t('dashboard.refresh')}
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
								{#if action.badge === 'Online' || action.badge === 'အွန်လိုင်း'}
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
						<h2 class="font-headline text-lg font-semibold text-on-surface">
							{$locale === 'my' ? 'သင့်ရာသီခွင် ပရိုဖိုင်' : 'Your Cosmic Profile'}
						</h2>
						<button
							type="button"
							onclick={() => (showProfileSettings = true)}
							class="ml-auto inline-flex items-center gap-1.5 rounded-full bg-surface-container px-3 py-1 text-xs font-medium text-on-surface-variant transition-colors hover:bg-surface-container-high"
						>
							<span class="material-symbols-outlined text-sm">edit</span>
							{$locale === 'my' ? 'ပြင်ဆင်ရန်' : 'Edit'}
						</button>
					</div>

					<div class="flex items-center gap-4 rounded-xl bg-surface-container-low p-5">
						<ZodiacBadge sign={currentProfile.zodiac_sign} {element} size="lg" />
						<div class="flex flex-col">
							<span class="font-mono-data text-[10px] tracking-wider text-secondary uppercase"
								>{$t('chart.sunSign')}</span
							>
							<h4 class="font-headline text-lg font-semibold text-on-surface">
								{zodiacTrans.name || currentProfile.zodiac_sign}
							</h4>
							<p class="text-sm text-on-surface-variant">
								{$locale === 'my' ? `${localizedElement} စိုးမိုးသော ရာသီခွင်` : `Ruled by the element of ${element}`}
							</p>
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
									<span class="text-sm font-medium text-on-surface">
										{$locale === 'my' ? 'ဓာတ်သဘာဝ' : 'Elemental Affinity'}
									</span>
									<span class="text-xs text-on-surface-variant">
										{$locale === 'my' ? 'သင့်ပင်မဓာတ်စွမ်းအင်' : 'Your dominant elemental energy'}
									</span>
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
										<span class="text-sm font-medium text-on-surface">
											{$locale === 'my' ? 'မွေးနေ့ရက်စွဲ' : 'Birth Date'}
										</span>
										<span class="text-xs text-on-surface-variant">
											{$locale === 'my' ? 'ရာသီခွင်သတ်မှတ်ချက်' : 'Used to determine your sign'}
										</span>
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
									<span class="text-sm font-medium text-on-surface">
										{$locale === 'my' ? 'ဟောကိန်းပုံစံ' : 'Preferred Style'}
									</span>
									<span class="text-xs text-on-surface-variant">
										{$locale === 'my' ? 'အနက်ဖွင့်ဟောကြားမည့်ဟန်' : 'How your readings are phrased'}
									</span>
								</div>
							</div>
							<span class="font-mono-data text-xs text-tertiary capitalize"
								>{currentProfile.preferred_style || 'balanced'}</span
							>
						</div>
					</div>

					<!-- Decorative ambient panel -->
					<div
						class="relative flex h-28 w-full items-end overflow-hidden rounded-xl bg-gradient-to-br from-primary-container/30 via-surface-container-low to-secondary-container/20 shadow-inner"
					>
						<div class="cosmic-stars absolute inset-0 opacity-50"></div>
						<span
							class="font-mono-data relative z-10 flex items-center gap-2 p-3.5 text-[11px] text-primary"
						>
							<span class="material-symbols-outlined text-base">lens_blur</span>
							{$locale === 'my' ? 'ဗေဒင်မေးမြန်းမှုတိုင်းသည် ကောင်းကင်စကြဝဠာ၏ စည်းချက်အတိုင်း ဖြစ်ပေါ်ပါသည်' : 'Every reading unfolds within the greater celestial rhythm.'}
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
						<LoadingSpinner text={$t('common.loading')} />
					{:else if latestReading}
						<div class="flex flex-wrap items-center justify-between gap-4">
							<div class="flex flex-col">
								<div class="flex items-center gap-2">
									<span class="font-mono-data text-[10px] tracking-wider text-primary uppercase"
										>{$locale === 'my' ? 'နောက်ဆုံးမေးထားသော ဗေဒင်' : 'Archival Spotlight'}</span
									>
									<span class="text-on-surface-variant">&bull;</span>
									<span class="text-sm text-on-surface-variant">{latestReading.created_at}</span>
								</div>
								<h2 class="font-headline mt-1 text-xl font-semibold text-on-surface">
									{latestReading.question || ($locale === 'my' ? 'တားရော့ဗေဒင်' : 'Tarot Reading')}
								</h2>
							</div>
							<a
								href="/history"
								class="inline-flex items-center gap-1.5 rounded-full bg-surface-container px-3 py-1.5 text-sm text-on-surface transition-colors hover:bg-surface-container-high"
							>
								{$locale === 'my' ? 'မှတ်တမ်းအပြည့်အစုံ' : 'Full Spread'}
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
									>{$t('reading.aiSynthesis')}</span
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
									{$locale === 'my' ? 'အသေးစိတ်အချက်များ' : 'Reading Details'}
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
							<p class="text-on-surface-variant">{$t('dashboard.noReadings')}</p>
							<a href="/reading" class="btn-primary mt-2 inline-block">{$t('dashboard.newReading')}</a>
						</div>
					{/if}
				</div>
			</div>
		</section>

		<!-- Journal micro-widget -->
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
					<span class="font-headline text-base font-semibold text-on-surface">
						{$locale === 'my' ? 'အတွေးအမြင် အမြန်မှတ်တမ်း' : 'Quick Reflection Journal'}
					</span>
					<span class="text-sm text-on-surface-variant">
						{$locale === 'my' ? 'စိတ်ထဲပေါ်လာသော အတွေးစများကို ချက်ချင်းမှတ်သားထားပါ။' : 'Jot down a thought before it drifts away.'}
					</span>
				</div>
			</div>
			<div class="flex w-full items-center gap-3 md:w-auto">
				<input
					type="text"
					id="journal-note"
					name="journal-note"
					bind:value={journalNote}
					placeholder={$locale === 'my' ? 'စိတ်ကူးအသိကို မှတ်သားပါ...' : 'Record intuitive insight...'}
					class="w-full rounded-xl bg-surface-container-low px-4 py-2 text-sm text-on-surface placeholder:text-on-surface-variant/50 focus:ring-1 focus:ring-secondary focus:outline-none md:w-80"
				/>
				<button
					type="button"
					onclick={saveJournalNote}
					class="shrink-0 rounded-xl px-4 py-2 text-sm font-medium shadow-md transition-all {journalSaved
						? 'bg-primary text-on-primary'
						: 'bg-secondary-container text-on-secondary hover:bg-secondary'}"
				>
					{journalSaved ? ($locale === 'my' ? 'မှတ်သားပြီး ✓' : 'Saved ✓') : ($locale === 'my' ? 'မှတ်သားမည်' : 'Save Note')}
				</button>
			</div>
		</section>
	</div>
</div>

<ProfileSettingsModal bind:open={showProfileSettings} />
