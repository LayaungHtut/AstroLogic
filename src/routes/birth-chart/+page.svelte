<script lang="ts">
	import { ZODIAC_SYMBOLS, ELEMENT_COLORS } from '$lib/types';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import ReasoningStep from '$lib/components/ReasoningStep.svelte';
	import ElementBadge from '$lib/components/ElementBadge.svelte';
	import NatalChartWheel from '$lib/components/NatalChartWheel.svelte';
	import BirthChartExplanation from '$lib/components/BirthChartExplanation.svelte';
	import type { ReasoningStep as ReasoningStepType, PlanetPosition } from '$lib/types';
	import {
		locale,
		t,
		getZodiacTranslation,
		formatElement,
		formatModality,
		formatPlanet
	} from '$lib/i18n';

	interface BirthChart {
		sun_sign: string;
		moon_sign: string;
		rising_sign: string;
		element: string;
		moon_element: string;
		rising_element: string;
		modality: string;
		ruling_planet: string;
		traits: string[];
		personality_style: string;
		approach_to_life: string;
		planetary_influence: string;
		note: string;
		precise?: boolean;
		sun_degree?: number;
		moon_degree?: number;
		rising_degree?: number;
		timezone?: string;
		planets?: PlanetPosition[];
	}

	const currentYear = new Date().getFullYear();
	let month = $state(new Date().getMonth() + 1);
	let day = $state(new Date().getDate());
	let year = $state(currentYear - 25);
	let hour = $state(12);
	let minute = $state(0);
	let latitude = $state<number | null>(null);
	let longitude = $state<number | null>(null);
	let chart = $state<BirthChart | null>(null);
	let reasoning = $state<ReasoningStepType[]>([]);
	let loading = $state(false);
	let error = $state('');
	let locating = $state(false);
	let locationNote = $state('');

	function useBrowserLocation() {
		if (!navigator.geolocation) {
			locationNote =
				$locale === 'my'
					? 'ဤဘရောက်ဆာတွင် တည်နေရာရယူခြင်းကို အထောက်အပံ့မပေးပါ။'
					: 'Geolocation is not available in this browser.';
			return;
		}
		locating = true;
		locationNote = '';
		navigator.geolocation.getCurrentPosition(
			(pos) => {
				latitude = Math.round(pos.coords.latitude * 10000) / 10000;
				longitude = Math.round(pos.coords.longitude * 10000) / 10000;
				locating = false;
				locationNote =
					$locale === 'my'
						? 'သင့်လက်ရှိတည်နေရာကို အသုံးပြုထားပါသည်။ အကယ်၍ ဤနေရာတွင် မမွေးဖွားခဲ့ပါက သင့်မွေးရပ်မြေတည်နေရာကို ထည့်သွင်းပါ။'
						: "Using your current location. If you weren't born here, replace it with your birth coordinates.";
			},
			() => {
				locating = false;
				locationNote =
					$locale === 'my'
						? 'တည်နေရာကို ရယူ၍မရပါ — တည်နေရာကို ကိုယ်တိုင်ထည့်သွင်းပေးပါ။'
						: 'Could not access location — enter coordinates manually.';
			}
		);
	}

	const months = $derived([
		{ value: 1, label: $locale === 'my' ? 'ဇန်နဝါရီ' : 'January' },
		{ value: 2, label: $locale === 'my' ? 'ဖေဖော်ဝါရီ' : 'February' },
		{ value: 3, label: $locale === 'my' ? 'မတ်' : 'March' },
		{ value: 4, label: $locale === 'my' ? 'ဧပြီ' : 'April' },
		{ value: 5, label: $locale === 'my' ? 'မေ' : 'May' },
		{ value: 6, label: $locale === 'my' ? 'ဇွန်' : 'June' },
		{ value: 7, label: $locale === 'my' ? 'ဇူလိုင်' : 'July' },
		{ value: 8, label: $locale === 'my' ? 'ဩဂုတ်' : 'August' },
		{ value: 9, label: $locale === 'my' ? 'စက်တင်ဘာ' : 'September' },
		{ value: 10, label: $locale === 'my' ? 'အောက်တိုဘာ' : 'October' },
		{ value: 11, label: $locale === 'my' ? 'နိုဝင်ဘာ' : 'November' },
		{ value: 12, label: $locale === 'my' ? 'ဒီဇင်ဘာ' : 'December' }
	]);

	const hours = Array.from({ length: 24 }, (_, i) => ({
		value: i,
		label: `${i.toString().padStart(2, '0')}:00`
	}));

	const WHEEL_ANGLES = { sun: -90, moon: 30, rising: 150 };

	function eclipticToWheelAngle(degree: number, risingDegree: number): number {
		return degree - risingDegree - 90;
	}

	async function calculateChart() {
		loading = true;
		error = '';
		chart = null;
		reasoning = [];

		const body: Record<string, number> = { month, day, hour, minute, year };
		if (latitude !== null && longitude !== null) {
			body.latitude = latitude;
			body.longitude = longitude;
		}

		try {
			const res = await fetch('http://localhost:8000/api/birth-chart/calculate', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(body)
			});
			const data = await res.json();
			if (data.error) {
				error = data.error;
			} else {
				chart = data.chart as BirthChart;
				reasoning = (data.reasoning || []) as ReasoningStepType[];
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to calculate chart';
		} finally {
			loading = false;
		}
	}

	function getSignSymbol(sign: string): string {
		return ZODIAC_SYMBOLS[sign] || '☆';
	}

	function getElementColor(element: string): string {
		return ELEMENT_COLORS[element] || '#9333ea';
	}

	function wheelPoint(angleDeg: number, radius: number) {
		const rad = (angleDeg * Math.PI) / 180;
		return { x: 100 + radius * Math.cos(rad), y: 100 + radius * Math.sin(rad) };
	}
</script>

<svelte:head>
	<title>{$t('chart.title')} - {$t('brand.name')}</title>
</svelte:head>

<div class="page-container">
	<!-- Header -->
	<div class="mb-10 flex flex-col gap-3">
		<div
			class="font-mono-data inline-flex items-center gap-2 self-start rounded-full bg-surface-container-high px-3 py-1 text-[11px] tracking-widest text-secondary uppercase"
		>
			<span class="h-1.5 w-1.5 animate-pulse rounded-full bg-secondary"></span>
			<span>{$locale === 'my' ? 'ဇာတာခွင် တွက်ချက်မှု' : 'Natal Chart Calculation'}</span>
		</div>
		<h1 class="font-headline gradient-text text-3xl font-bold tracking-tight md:text-4xl">
			{$t('chart.title')}
		</h1>
		<p class="max-w-2xl text-on-surface-variant">
			{$t('chart.subtitle')}
		</p>
	</div>

	<div class="mx-auto max-w-3xl">
		<!-- Input Panel -->
		<div class="glass-card relative mb-8 overflow-hidden p-6 lg:p-8">
			<div
				class="pointer-events-none absolute -top-10 right-10 h-72 w-72 rounded-full bg-primary-container/10 blur-3xl"
			></div>

			<div class="relative mb-6 flex items-center gap-3">
				<div
					class="flex h-8 w-8 items-center justify-center rounded-full bg-primary-container/30 text-primary"
				>
					<span class="material-symbols-outlined text-base">tune</span>
				</div>
				<span class="font-headline text-lg text-on-surface">
					{$locale === 'my' ? 'မွေးဖွားချိန် အချက်အလက်များ' : 'Precision Birth Inputs'}
				</span>
			</div>

			<div class="relative grid grid-cols-2 gap-5 sm:grid-cols-4">
				<div class="flex flex-col gap-2">
					<label
						for="month"
						class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase"
					>
						{$locale === 'my' ? 'မွေးဖွားသည့်လ' : 'Birth Month'}
					</label>
					<div class="relative">
						<select
							id="month"
							bind:value={month}
							class="w-full cursor-pointer appearance-none rounded-lg bg-surface-container-highest px-4 py-3 text-on-surface transition-colors outline-none focus:bg-surface-bright"
						>
							{#each months as m}
								<option value={m.value}>{m.label}</option>
							{/each}
						</select>
						<span
							class="material-symbols-outlined pointer-events-none absolute top-3.5 right-3 text-lg text-on-surface-variant"
							>expand_more</span
						>
					</div>
				</div>

				<div class="flex flex-col gap-2">
					<label
						for="day"
						class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase"
					>
						{$locale === 'my' ? 'မွေးဖွားသည့်ရက်' : 'Birth Day'}
					</label>
					<input
						id="day"
						type="number"
						bind:value={day}
						min="1"
						max="31"
						class="w-full rounded-lg bg-surface-container-highest px-4 py-3 text-on-surface transition-colors outline-none focus:bg-surface-bright"
					/>
				</div>

				<div class="flex flex-col gap-2">
					<label
						for="year"
						class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase"
					>
						{$locale === 'my' ? 'မွေးဖွားသည့်ခုနှစ်' : 'Birth Year'}
					</label>
					<input
						id="year"
						type="number"
						bind:value={year}
						min="1900"
						max={currentYear}
						class="w-full rounded-lg bg-surface-container-highest px-4 py-3 text-on-surface transition-colors outline-none focus:bg-surface-bright"
					/>
				</div>

				<div class="flex flex-col gap-2">
					<label
						for="hour"
						class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase"
					>
						{$locale === 'my' ? 'မွေးဖွားသည့်နာရီ' : 'Birth Hour'}
					</label>
					<div class="relative">
						<select
							id="hour"
							bind:value={hour}
							class="w-full cursor-pointer appearance-none rounded-lg bg-surface-container-highest px-4 py-3 text-on-surface transition-colors outline-none focus:bg-surface-bright"
						>
							{#each hours as h}
								<option value={h.value}>{h.label}</option>
							{/each}
						</select>
						<span
							class="material-symbols-outlined pointer-events-none absolute top-3.5 right-3 text-lg text-on-surface-variant"
							>schedule</span
						>
					</div>
				</div>

				<div class="flex flex-col gap-2">
					<label
						for="minute"
						class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase"
					>
						{$locale === 'my' ? 'မွေးဖွားသည့်မိနစ်' : 'Birth Minute'}
					</label>
					<input
						id="minute"
						type="number"
						bind:value={minute}
						min="0"
						max="59"
						class="w-full rounded-lg bg-surface-container-highest px-4 py-3 text-on-surface transition-colors outline-none focus:bg-surface-bright"
					/>
				</div>

				<div class="flex flex-col gap-2">
					<label
						for="latitude"
						class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase"
					>
						{$t('chart.latitude')}
					</label>
					<input
						id="latitude"
						type="number"
						step="0.0001"
						placeholder="e.g. 16.8409"
						value={latitude ?? ''}
						oninput={(e) =>
							(latitude = e.currentTarget.value === '' ? null : Number(e.currentTarget.value))}
						min="-90"
						max="90"
						class="w-full rounded-lg bg-surface-container-highest px-4 py-3 text-on-surface transition-colors outline-none focus:bg-surface-bright"
					/>
				</div>

				<div class="flex flex-col gap-2">
					<label
						for="longitude"
						class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase"
					>
						{$t('chart.longitude')}
					</label>
					<input
						id="longitude"
						type="number"
						step="0.0001"
						placeholder="e.g. 96.1735"
						value={longitude ?? ''}
						oninput={(e) =>
							(longitude = e.currentTarget.value === '' ? null : Number(e.currentTarget.value))}
						min="-180"
						max="180"
						class="w-full rounded-lg bg-surface-container-highest px-4 py-3 text-on-surface transition-colors outline-none focus:bg-surface-bright"
					/>
				</div>

				<div class="flex flex-col justify-end gap-2">
					<button
						type="button"
						onclick={useBrowserLocation}
						disabled={locating}
						class="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-surface-container-highest px-4 py-3 text-on-surface transition-colors hover:bg-surface-bright disabled:opacity-60"
					>
						<span class="material-symbols-outlined text-lg {locating ? 'animate-spin' : ''}"
							>{locating ? 'progress_activity' : 'my_location'}</span
						>
						<span class="text-sm">{$t('chart.useLocation')}</span>
					</button>
				</div>
			</div>

			{#if locationNote}
				<p class="relative mt-3 flex items-center gap-2 text-xs text-tertiary">
					<span class="material-symbols-outlined text-sm">info</span>
					{locationNote}
				</p>
			{/if}

			<button
				class="font-headline relative mt-6 inline-flex w-full items-center justify-center gap-3 rounded-full bg-gradient-to-r from-primary-container via-purple-600 to-secondary-container px-8 py-3.5 text-base font-semibold text-white shadow-xl transition-all hover:shadow-[0_0_24px_rgba(76,215,246,0.45)] disabled:cursor-not-allowed disabled:opacity-60"
				onclick={calculateChart}
				disabled={loading}
			>
				<span class="material-symbols-outlined text-xl {loading ? 'animate-spin' : ''}">
					{loading ? 'progress_activity' : 'radar'}
				</span>
				<span>{loading ? $t('common.loading') : $t('chart.calculate')}</span>
			</button>
		</div>

		{#if error}
			<div class="glass-card mb-8 border-error/30 bg-error-container/10 p-4">
				<p class="flex items-center gap-2 text-sm text-error">
					<span class="material-symbols-outlined text-base">error</span>
					{error}
				</p>
			</div>
		{/if}

		{#if loading}
			<LoadingSpinner text={$t('common.loading')} />
		{/if}

		{#if chart}
			<!-- Astro-Seek Style Natal Celestial Wheel -->
			<div class="mb-8">
				<NatalChartWheel
					{chart}
					birthInfo={{ year, month, day, hour, minute, latitude, longitude }}
				/>
			</div>

			<!-- Comprehensive Psychological & Astrological Explanation -->
			<BirthChartExplanation
				{chart}
				birthInfo={{ year, month, day, hour, minute, latitude, longitude }}
			/>

			<!-- Natal Core Triad -->
			<div class="mb-4 flex items-center gap-4">
				<h2 class="font-headline text-xl text-on-surface">
					{$locale === 'my' ? 'အဓိက အရေးပါသော ရာသီခွင် ၃ မျိုး' : 'Natal Core Triad'}
				</h2>
				<div class="h-px flex-1 bg-surface-container-highest"></div>
				<span class="font-mono-data text-[11px] text-on-surface-variant uppercase">
					{$locale === 'my' ? 'ပင်မမဏ္ဍိုင်များ' : 'Identity Pillars'}
				</span>
			</div>
			<div class="mb-10 grid grid-cols-1 gap-5 sm:grid-cols-3">
				<div class="glass-card glass-card-hover relative flex flex-col overflow-hidden p-6">
					<div
						class="pointer-events-none absolute -top-16 -right-16 h-36 w-36 rounded-full blur-2xl"
						style:background-color="{getElementColor(chart.element)}20"
					></div>
					<div class="relative mb-4 flex items-center justify-between gap-2">
						<span
							class="font-mono-data flex items-center gap-1.5 text-[11px] tracking-wider text-on-surface-variant uppercase"
						>
							<span class="material-symbols-outlined text-sm text-primary">wb_sunny</span>
							{$t('chart.sunSign')}
						</span>
						<ElementBadge element={chart.element} size="sm" />
					</div>
					<div class="relative mb-2 text-5xl" style:color={getElementColor(chart.element)}>
						{getSignSymbol(chart.sun_sign)}
					</div>
					<h3 class="font-headline relative text-xl font-semibold text-on-surface">
						{getZodiacTranslation(chart.sun_sign, $locale).name || chart.sun_sign}
					</h3>
					<p class="relative mt-1 text-xs text-on-surface-variant">
						{$locale === 'my' ? 'ပင်ကိုစရိုက်နှင့် စိတ်စွမ်းအား' : 'Core will & identity'}
					</p>
				</div>

				<div class="glass-card glass-card-hover relative flex flex-col overflow-hidden p-6">
					<div
						class="pointer-events-none absolute -top-16 -right-16 h-36 w-36 rounded-full blur-2xl"
						style:background-color="{getElementColor(chart.moon_element)}20"
					></div>
					<div class="relative mb-4 flex items-center justify-between gap-2">
						<span
							class="font-mono-data flex items-center gap-1.5 text-[11px] tracking-wider text-on-surface-variant uppercase"
						>
							<span class="material-symbols-outlined text-sm text-secondary">bedtime</span>
							{$t('chart.moonSign')}
						</span>
						<ElementBadge element={chart.moon_element} size="sm" />
					</div>
					<div class="relative mb-2 text-5xl" style:color={getElementColor(chart.moon_element)}>
						{getSignSymbol(chart.moon_sign)}
					</div>
					<h3 class="font-headline relative text-xl font-semibold text-on-surface">
						{getZodiacTranslation(chart.moon_sign, $locale).name || chart.moon_sign}
					</h3>
					<p class="relative mt-1 text-xs text-on-surface-variant">
						{$locale === 'my' ? 'မသိစိတ်နှင့် စိတ်ခံစားမှု' : 'Subconscious & emotion'}
					</p>
				</div>

				<div class="glass-card glass-card-hover relative flex flex-col overflow-hidden p-6">
					<div
						class="pointer-events-none absolute -top-16 -right-16 h-36 w-36 rounded-full blur-2xl"
						style:background-color="{getElementColor(chart.rising_element)}20"
					></div>
					<div class="relative mb-4 flex items-center justify-between gap-2">
						<span
							class="font-mono-data flex items-center gap-1.5 text-[11px] tracking-wider text-on-surface-variant uppercase"
						>
							<span class="material-symbols-outlined text-sm text-tertiary">north_east</span>
							{$t('chart.risingSign')}
						</span>
						<ElementBadge element={chart.rising_element} size="sm" />
					</div>
					<div class="relative mb-2 text-5xl" style:color={getElementColor(chart.rising_element)}>
						{getSignSymbol(chart.rising_sign)}
					</div>
					<h3 class="font-headline relative text-xl font-semibold text-on-surface">
						{getZodiacTranslation(chart.rising_sign, $locale).name || chart.rising_sign}
					</h3>
					<p class="relative mt-1 text-xs text-on-surface-variant">
						{$locale === 'my' ? 'အပြင်ပန်းပုံရိပ်နှင့် မျက်နှာဖုံး' : 'Ascendant mask'}
					</p>
				</div>
			</div>

			<!-- Full Planetary Lineup -->
			{#if chart.planets && chart.planets.length > 0}
				<div class="mb-4 flex items-center gap-4">
					<h2 class="font-headline text-xl text-on-surface">{$t('chart.placements')}</h2>
					<div class="h-px flex-1 bg-surface-container-highest"></div>
					<span class="font-mono-data text-[11px] text-on-surface-variant uppercase">
						{$locale === 'my' ? 'ဂြိုဟ် ၁၀ လုံး အနေအထား' : 'Planetary Lineup'}
					</span>
				</div>
				<div class="mb-10 grid grid-cols-2 gap-4 sm:grid-cols-4">
					{#each chart.planets as planet}
						{@const pSignTrans = getZodiacTranslation(planet.sign, $locale)}
						<div class="glass-card glass-card-hover relative flex flex-col overflow-hidden p-4">
							<div
								class="pointer-events-none absolute -top-10 -right-10 h-24 w-24 rounded-full blur-2xl"
								style:background-color="{getElementColor(planet.element)}20"
							></div>
							<div class="relative mb-2 flex items-center justify-between gap-2">
								<span
									class="font-mono-data text-[10px] font-semibold tracking-wider text-on-surface-variant uppercase"
								>
									{formatPlanet(planet.name, $locale)}
								</span>
								{#if planet.retrograde}
									<span class="font-mono-data text-[9px] text-tertiary" title="Retrograde">℞</span>
								{/if}
							</div>
							<div class="relative mb-1 text-3xl" style:color={getElementColor(planet.element)}>
								{getSignSymbol(planet.sign)}
							</div>
							<h4 class="font-headline relative text-sm font-semibold text-on-surface">
								{pSignTrans.name || planet.sign}
							</h4>
							<p class="relative mt-1 text-[11px] text-on-surface-variant/80">
								{formatElement(planet.element, $locale)} · {formatModality(
									planet.modality,
									$locale
								)}
							</p>
						</div>
					{/each}
				</div>
			{/if}

			<!-- Profile Details -->
			<div class="glass-card mb-8 p-6 lg:p-8">
				<h3 class="font-headline mb-5 text-lg text-on-surface">
					{$locale === 'my' ? 'သင့်ရာသီခွင် အသေးစိတ်အချက်အလက်များ' : 'Your Profile'}
				</h3>

				<div class="mb-5 grid grid-cols-2 gap-3 rounded-xl bg-surface-container-lowest/60 p-4">
					<div class="flex flex-col">
						<span
							class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase"
						>
							{$t('zodiac.modality')}
						</span>
						<span class="font-medium text-on-surface capitalize"
							>{formatModality(chart.modality, $locale)}</span
						>
					</div>
					<div class="flex flex-col">
						<span
							class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase"
						>
							{$t('zodiac.ruler')}
						</span>
						<span class="font-medium text-on-surface capitalize"
							>{formatPlanet(chart.ruling_planet, $locale)}</span
						>
					</div>
				</div>

				{#if chart.personality_style}
					<div class="mb-4 border-b border-white/5 pb-4">
						<div
							class="font-mono-data mb-1 text-[11px] tracking-wider text-on-surface-variant uppercase"
						>
							{$locale === 'my' ? 'ကိုယ်ရည်ကိုယ်သွေးဟန်' : 'Personality Style'}
						</div>
						<div class="text-sm text-on-surface/90">{chart.personality_style}</div>
					</div>
				{/if}

				{#if chart.approach_to_life}
					<div class="mb-4 border-b border-white/5 pb-4">
						<div
							class="font-mono-data mb-1 text-[11px] tracking-wider text-on-surface-variant uppercase"
						>
							{$locale === 'my' ? 'ဘဝကို ချဉ်းကပ်ပုံ' : 'Approach to Life'}
						</div>
						<div class="text-sm text-on-surface/90">{chart.approach_to_life}</div>
					</div>
				{/if}

				{#if chart.planetary_influence}
					<div>
						<div
							class="font-mono-data mb-1 text-[11px] tracking-wider text-on-surface-variant uppercase"
						>
							{$locale === 'my' ? 'ဂြိုဟ်လွှမ်းမိုးမှုစွမ်းအား' : 'Planetary Influence'}
						</div>
						<div class="text-sm text-on-surface/90">{chart.planetary_influence}</div>
					</div>
				{/if}
			</div>

			{#if reasoning.length > 0}
				<div class="rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl lg:p-8">
					<div
						class="mb-4 flex items-center justify-between border-b border-surface-container-highest pb-4"
					>
						<div class="flex items-center gap-2.5">
							<span
								class="h-2.5 w-2.5 animate-pulse rounded-full bg-secondary shadow-[0_0_8px_#4cd7f6]"
							></span>
							<span class="font-headline text-lg text-on-surface"
								>Prolog Symbolic Reasoning Engine</span
							>
						</div>
						<span
							class="font-mono-data hidden text-[11px] tracking-widest text-secondary uppercase sm:inline"
							>Verified Trace</span
						>
					</div>
					<div class="space-y-2">
						{#each reasoning as step, i}
							<ReasoningStep {step} index={i} />
						{/each}
					</div>
				</div>
			{/if}
		{/if}
	</div>
</div>
