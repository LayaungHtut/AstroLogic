<script lang="ts">
	import { ZODIAC_SYMBOLS, ELEMENT_COLORS } from '$lib/types';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import ReasoningStep from '$lib/components/ReasoningStep.svelte';
	import ElementBadge from '$lib/components/ElementBadge.svelte';
	import NatalChartWheel from '$lib/components/NatalChartWheel.svelte';
	import BirthChartExplanation from '$lib/components/BirthChartExplanation.svelte';
	import type { ReasoningStep as ReasoningStepType, PlanetPosition } from '$lib/types';
	import { locale, t, getZodiacTranslation, formatElement, formatModality, formatPlanet } from '$lib/i18n';

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
			locationNote = $locale === 'my' ? 'ဤဘရောက်ဆာတွင် တည်နေရာရယူခြင်းကို အထောက်အပံ့မပေးပါ။' : 'Geolocation is not available in this browser.';
			return;
		}
		locating = true;
		locationNote = '';
		navigator.geolocation.getCurrentPosition(
			(pos) => {
				latitude = Math.round(pos.coords.latitude * 10000) / 10000;
				longitude = Math.round(pos.coords.longitude * 10000) / 10000;
				locating = false;
				locationNote = $locale === 'my'
					? 'သင့်လက်ရှိတည်နေရာကို အသုံးပြုထားပါသည်။ အကယ်၍ ဤနေရာတွင် မမွေးဖွားခဲ့ပါက သင့်မွေးရပ်မြေတည်နေရာကို ထည့်သွင်းပါ။'
					: 'Using your current location. If you weren\'t born here, replace it with your birth coordinates.';
			},
			() => {
				locating = false;
				locationNote = $locale === 'my' ? 'တည်နေရာကို ရယူ၍မရပါ — တည်နေရာကို ကိုယ်တိုင်ထည့်သွင်းပေးပါ။' : 'Could not access location — enter coordinates manually.';
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
		{ value: 12, label: $locale === 'my' ? 'ဒီဇင်ဘာ' : 'December' },
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
				body: JSON.stringify(body),
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
	<div class="flex flex-col gap-3 mb-10">
		<div class="inline-flex items-center gap-2 self-start px-3 py-1 rounded-full bg-surface-container-high text-secondary font-mono-data text-[11px] uppercase tracking-widest">
			<span class="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
			<span>{$locale === 'my' ? 'ဇာတာခွင် တွက်ချက်မှု' : 'Natal Chart Calculation'}</span>
		</div>
		<h1 class="font-headline text-3xl md:text-4xl font-bold tracking-tight gradient-text">
			{$t('chart.title')}
		</h1>
		<p class="text-on-surface-variant max-w-2xl">
			{$t('chart.subtitle')}
		</p>
	</div>

	<div class="max-w-3xl mx-auto">
		<!-- Input Panel -->
		<div class="glass-card p-6 lg:p-8 mb-8 relative overflow-hidden">
			<div class="absolute -top-10 right-10 w-72 h-72 bg-primary-container/10 rounded-full blur-3xl pointer-events-none"></div>

			<div class="relative flex items-center gap-3 mb-6">
				<div class="w-8 h-8 rounded-full bg-primary-container/30 text-primary flex items-center justify-center">
					<span class="material-symbols-outlined text-base">tune</span>
				</div>
				<span class="font-headline text-lg text-on-surface">
					{$locale === 'my' ? 'မွေးဖွားချိန် အချက်အလက်များ' : 'Precision Birth Inputs'}
				</span>
			</div>

			<div class="relative grid grid-cols-2 sm:grid-cols-4 gap-5">
				<div class="flex flex-col gap-2">
					<label for="month" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">
						{$locale === 'my' ? 'မွေးဖွားသည့်လ' : 'Birth Month'}
					</label>
					<div class="relative">
						<select
							id="month"
							bind:value={month}
							class="w-full bg-surface-container-highest text-on-surface rounded-lg px-4 py-3 appearance-none focus:bg-surface-bright transition-colors outline-none cursor-pointer"
						>
							{#each months as m}
								<option value={m.value}>{m.label}</option>
							{/each}
						</select>
						<span class="material-symbols-outlined absolute right-3 top-3.5 text-on-surface-variant pointer-events-none text-lg">expand_more</span>
					</div>
				</div>

				<div class="flex flex-col gap-2">
					<label for="day" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">
						{$locale === 'my' ? 'မွေးဖွားသည့်ရက်' : 'Birth Day'}
					</label>
					<input
						id="day"
						type="number"
						bind:value={day}
						min="1"
						max="31"
						class="w-full bg-surface-container-highest text-on-surface rounded-lg px-4 py-3 focus:bg-surface-bright transition-colors outline-none"
					/>
				</div>

				<div class="flex flex-col gap-2">
					<label for="year" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">
						{$locale === 'my' ? 'မွေးဖွားသည့်ခုနှစ်' : 'Birth Year'}
					</label>
					<input
						id="year"
						type="number"
						bind:value={year}
						min="1900"
						max={currentYear}
						class="w-full bg-surface-container-highest text-on-surface rounded-lg px-4 py-3 focus:bg-surface-bright transition-colors outline-none"
					/>
				</div>

				<div class="flex flex-col gap-2">
					<label for="hour" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">
						{$locale === 'my' ? 'မွေးဖွားသည့်နာရီ' : 'Birth Hour'}
					</label>
					<div class="relative">
						<select
							id="hour"
							bind:value={hour}
							class="w-full bg-surface-container-highest text-on-surface rounded-lg px-4 py-3 appearance-none focus:bg-surface-bright transition-colors outline-none cursor-pointer"
						>
							{#each hours as h}
								<option value={h.value}>{h.label}</option>
							{/each}
						</select>
						<span class="material-symbols-outlined absolute right-3 top-3.5 text-on-surface-variant pointer-events-none text-lg">schedule</span>
					</div>
				</div>

				<div class="flex flex-col gap-2">
					<label for="minute" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">
						{$locale === 'my' ? 'မွေးဖွားသည့်မိနစ်' : 'Birth Minute'}
					</label>
					<input
						id="minute"
						type="number"
						bind:value={minute}
						min="0"
						max="59"
						class="w-full bg-surface-container-highest text-on-surface rounded-lg px-4 py-3 focus:bg-surface-bright transition-colors outline-none"
					/>
				</div>

				<div class="flex flex-col gap-2">
					<label for="latitude" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">
						{$t('chart.latitude')}
					</label>
					<input
						id="latitude"
						type="number"
						step="0.0001"
						placeholder="e.g. 16.8409"
						value={latitude ?? ''}
						oninput={(e) => (latitude = e.currentTarget.value === '' ? null : Number(e.currentTarget.value))}
						min="-90"
						max="90"
						class="w-full bg-surface-container-highest text-on-surface rounded-lg px-4 py-3 focus:bg-surface-bright transition-colors outline-none"
					/>
				</div>

				<div class="flex flex-col gap-2">
					<label for="longitude" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">
						{$t('chart.longitude')}
					</label>
					<input
						id="longitude"
						type="number"
						step="0.0001"
						placeholder="e.g. 96.1735"
						value={longitude ?? ''}
						oninput={(e) => (longitude = e.currentTarget.value === '' ? null : Number(e.currentTarget.value))}
						min="-180"
						max="180"
						class="w-full bg-surface-container-highest text-on-surface rounded-lg px-4 py-3 focus:bg-surface-bright transition-colors outline-none"
					/>
				</div>

				<div class="flex flex-col gap-2 justify-end">
					<button
						type="button"
						onclick={useBrowserLocation}
						disabled={locating}
						class="w-full inline-flex items-center justify-center gap-2 bg-surface-container-highest hover:bg-surface-bright text-on-surface rounded-lg px-4 py-3 transition-colors disabled:opacity-60"
					>
						<span class="material-symbols-outlined text-lg {locating ? 'animate-spin' : ''}">{locating ? 'progress_activity' : 'my_location'}</span>
						<span class="text-sm">{$t('chart.useLocation')}</span>
					</button>
				</div>
			</div>

			{#if locationNote}
				<p class="relative flex items-center gap-2 text-xs text-tertiary mt-3">
					<span class="material-symbols-outlined text-sm">info</span>
					{locationNote}
				</p>
			{/if}

			<button
				class="relative mt-6 w-full inline-flex items-center justify-center gap-3 px-8 py-3.5 rounded-full bg-gradient-to-r from-primary-container via-purple-600 to-secondary-container text-white font-headline text-base font-semibold shadow-xl hover:shadow-[0_0_24px_rgba(76,215,246,0.45)] transition-all disabled:opacity-60 disabled:cursor-not-allowed"
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
			<div class="glass-card p-4 mb-8 border-error/30 bg-error-container/10">
				<p class="text-error text-sm flex items-center gap-2">
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
			<div class="flex items-center gap-4 mb-4">
				<h2 class="font-headline text-xl text-on-surface">
					{$locale === 'my' ? 'အဓိက အရေးပါသော ရာသီခွင် ၃ မျိုး' : 'Natal Core Triad'}
				</h2>
				<div class="h-px flex-1 bg-surface-container-highest"></div>
				<span class="font-mono-data text-[11px] text-on-surface-variant uppercase">
					{$locale === 'my' ? 'ပင်မမဏ္ဍိုင်များ' : 'Identity Pillars'}
				</span>
			</div>
			<div class="grid grid-cols-1 sm:grid-cols-3 gap-5 mb-10">
				<div class="glass-card glass-card-hover relative p-6 flex flex-col overflow-hidden">
					<div class="absolute -top-16 -right-16 w-36 h-36 rounded-full blur-2xl pointer-events-none" style:background-color="{getElementColor(chart.element)}20"></div>
					<div class="relative flex items-center justify-between gap-2 mb-4">
						<span class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider flex items-center gap-1.5">
							<span class="material-symbols-outlined text-sm text-primary">wb_sunny</span>
							{$t('chart.sunSign')}
						</span>
						<ElementBadge element={chart.element} size="sm" />
					</div>
					<div class="relative text-5xl mb-2" style:color="{getElementColor(chart.element)}">
						{getSignSymbol(chart.sun_sign)}
					</div>
					<h3 class="relative font-headline text-xl text-on-surface font-semibold">{getZodiacTranslation(chart.sun_sign, $locale).name || chart.sun_sign}</h3>
					<p class="relative text-xs text-on-surface-variant mt-1">
						{$locale === 'my' ? 'ပင်ကိုစရိုက်နှင့် စိတ်စွမ်းအား' : 'Core will & identity'}
					</p>
				</div>

				<div class="glass-card glass-card-hover relative p-6 flex flex-col overflow-hidden">
					<div class="absolute -top-16 -right-16 w-36 h-36 rounded-full blur-2xl pointer-events-none" style:background-color="{getElementColor(chart.moon_element)}20"></div>
					<div class="relative flex items-center justify-between gap-2 mb-4">
						<span class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider flex items-center gap-1.5">
							<span class="material-symbols-outlined text-sm text-secondary">bedtime</span>
							{$t('chart.moonSign')}
						</span>
						<ElementBadge element={chart.moon_element} size="sm" />
					</div>
					<div class="relative text-5xl mb-2" style:color="{getElementColor(chart.moon_element)}">
						{getSignSymbol(chart.moon_sign)}
					</div>
					<h3 class="relative font-headline text-xl text-on-surface font-semibold">{getZodiacTranslation(chart.moon_sign, $locale).name || chart.moon_sign}</h3>
					<p class="relative text-xs text-on-surface-variant mt-1">
						{$locale === 'my' ? 'မသိစိတ်နှင့် စိတ်ခံစားမှု' : 'Subconscious & emotion'}
					</p>
				</div>

				<div class="glass-card glass-card-hover relative p-6 flex flex-col overflow-hidden">
					<div class="absolute -top-16 -right-16 w-36 h-36 rounded-full blur-2xl pointer-events-none" style:background-color="{getElementColor(chart.rising_element)}20"></div>
					<div class="relative flex items-center justify-between gap-2 mb-4">
						<span class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider flex items-center gap-1.5">
							<span class="material-symbols-outlined text-sm text-tertiary">north_east</span>
							{$t('chart.risingSign')}
						</span>
						<ElementBadge element={chart.rising_element} size="sm" />
					</div>
					<div class="relative text-5xl mb-2" style:color="{getElementColor(chart.rising_element)}">
						{getSignSymbol(chart.rising_sign)}
					</div>
					<h3 class="relative font-headline text-xl text-on-surface font-semibold">{getZodiacTranslation(chart.rising_sign, $locale).name || chart.rising_sign}</h3>
					<p class="relative text-xs text-on-surface-variant mt-1">
						{$locale === 'my' ? 'အပြင်ပန်းပုံရိပ်နှင့် မျက်နှာဖုံး' : 'Ascendant mask'}
					</p>
				</div>
			</div>

			<!-- Full Planetary Lineup -->
			{#if chart.planets && chart.planets.length > 0}
				<div class="flex items-center gap-4 mb-4">
					<h2 class="font-headline text-xl text-on-surface">{$t('chart.placements')}</h2>
					<div class="h-px flex-1 bg-surface-container-highest"></div>
					<span class="font-mono-data text-[11px] text-on-surface-variant uppercase">
						{$locale === 'my' ? 'ဂြိုဟ် ၁၀ လုံး အနေအထား' : 'Planetary Lineup'}
					</span>
				</div>
				<div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-10">
					{#each chart.planets as planet}
						{@const pSignTrans = getZodiacTranslation(planet.sign, $locale)}
						<div class="glass-card glass-card-hover relative p-4 flex flex-col overflow-hidden">
							<div class="absolute -top-10 -right-10 w-24 h-24 rounded-full blur-2xl pointer-events-none" style:background-color="{getElementColor(planet.element)}20"></div>
							<div class="relative flex items-center justify-between gap-2 mb-2">
								<span class="font-mono-data text-[10px] text-on-surface-variant uppercase tracking-wider font-semibold">
									{formatPlanet(planet.name, $locale)}
								</span>
								{#if planet.retrograde}
									<span class="font-mono-data text-[9px] text-tertiary" title="Retrograde">℞</span>
								{/if}
							</div>
							<div class="relative text-3xl mb-1" style:color="{getElementColor(planet.element)}">
								{getSignSymbol(planet.sign)}
							</div>
							<h4 class="relative font-headline text-sm text-on-surface font-semibold">{pSignTrans.name || planet.sign}</h4>
							<p class="relative text-[11px] text-on-surface-variant/80 mt-1">{formatElement(planet.element, $locale)} · {formatModality(planet.modality, $locale)}</p>
						</div>
					{/each}
				</div>
			{/if}

			<!-- Profile Details -->
			<div class="glass-card p-6 lg:p-8 mb-8">
				<h3 class="font-headline text-lg text-on-surface mb-5">
					{$locale === 'my' ? 'သင့်ရာသီခွင် အသေးစိတ်အချက်အလက်များ' : 'Your Profile'}
				</h3>

				<div class="grid grid-cols-2 gap-3 mb-5 bg-surface-container-lowest/60 p-4 rounded-xl">
					<div class="flex flex-col">
						<span class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">
							{$t('zodiac.modality')}
						</span>
						<span class="text-on-surface font-medium capitalize">{formatModality(chart.modality, $locale)}</span>
					</div>
					<div class="flex flex-col">
						<span class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">
							{$t('zodiac.ruler')}
						</span>
						<span class="text-on-surface font-medium capitalize">{formatPlanet(chart.ruling_planet, $locale)}</span>
					</div>
				</div>

				{#if chart.personality_style}
					<div class="mb-4 border-b border-white/5 pb-4">
						<div class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider mb-1">
							{$locale === 'my' ? 'ကိုယ်ရည်ကိုယ်သွေးဟန်' : 'Personality Style'}
						</div>
						<div class="text-sm text-on-surface/90">{chart.personality_style}</div>
					</div>
				{/if}

				{#if chart.approach_to_life}
					<div class="mb-4 border-b border-white/5 pb-4">
						<div class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider mb-1">
							{$locale === 'my' ? 'ဘဝကို ချဉ်းကပ်ပုံ' : 'Approach to Life'}
						</div>
						<div class="text-sm text-on-surface/90">{chart.approach_to_life}</div>
					</div>
				{/if}

				{#if chart.planetary_influence}
					<div>
						<div class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider mb-1">
							{$locale === 'my' ? 'ဂြိုဟ်လွှမ်းမိုးမှုစွမ်းအား' : 'Planetary Influence'}
						</div>
						<div class="text-sm text-on-surface/90">{chart.planetary_influence}</div>
					</div>
				{/if}
			</div>

			{#if reasoning.length > 0}
				<div class="bg-surface-container-lowest/80 rounded-2xl p-6 lg:p-8 shadow-xl">
					<div class="flex items-center justify-between pb-4 mb-4 border-b border-surface-container-highest">
						<div class="flex items-center gap-2.5">
							<span class="w-2.5 h-2.5 rounded-full bg-secondary shadow-[0_0_8px_#4cd7f6] animate-pulse"></span>
							<span class="font-headline text-lg text-on-surface">Prolog Symbolic Reasoning Engine</span>
						</div>
						<span class="font-mono-data text-[11px] text-secondary tracking-widest uppercase hidden sm:inline">Verified Trace</span>
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
