<script lang="ts">
	import { ZODIAC_SYMBOLS, ELEMENT_COLORS } from '$lib/types';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import ReasoningStep from '$lib/components/ReasoningStep.svelte';
	import ElementBadge from '$lib/components/ElementBadge.svelte';
	import type { ReasoningStep as ReasoningStepType, PlanetPosition } from '$lib/types';

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
			locationNote = 'Geolocation is not available in this browser.';
			return;
		}
		locating = true;
		locationNote = '';
		navigator.geolocation.getCurrentPosition(
			(pos) => {
				latitude = Math.round(pos.coords.latitude * 10000) / 10000;
				longitude = Math.round(pos.coords.longitude * 10000) / 10000;
				locating = false;
				locationNote = 'Using your current location. If you weren\'t born here, replace it with your birth coordinates.';
			},
			() => {
				locating = false;
				locationNote = 'Could not access location — enter coordinates manually.';
			}
		);
	}

	const months = [
		{ value: 1, label: 'January' }, { value: 2, label: 'February' },
		{ value: 3, label: 'March' }, { value: 4, label: 'April' },
		{ value: 5, label: 'May' }, { value: 6, label: 'June' },
		{ value: 7, label: 'July' }, { value: 8, label: 'August' },
		{ value: 9, label: 'September' }, { value: 10, label: 'October' },
		{ value: 11, label: 'November' }, { value: 12, label: 'December' },
	];

	const hours = Array.from({ length: 24 }, (_, i) => ({
		value: i,
		label: `${i.toString().padStart(2, '0')}:00`
	}));

	// Fallback angles for the schematic wheel when no precise ecliptic degrees
	// are available (approximate mode) — purely decorative in that case.
	const WHEEL_ANGLES = { sun: -90, moon: 30, rising: 150 };

	// Ecliptic longitude (0-360, 0 = Aries point) to SVG angle. The wheel's
	// "up" (-90 deg in SVG terms) is aligned to the Ascendant so the rising
	// sign always appears at the same on-screen position (as on a real chart).
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
	<title>Birth Chart - AstroLogic</title>
</svelte:head>

<div class="page-container">
	<!-- Header -->
	<div class="flex flex-col gap-3 mb-10">
		<div class="inline-flex items-center gap-2 self-start px-3 py-1 rounded-full bg-surface-container-high text-secondary font-mono-data text-[11px] uppercase tracking-widest">
			<span class="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
			<span>Natal Chart Calculation</span>
		</div>
		<h1 class="font-headline text-3xl md:text-4xl font-bold tracking-tight gradient-text">
			Natal Ephemeris &amp; Signs
		</h1>
		<p class="text-on-surface-variant max-w-2xl">
			Calculate your Sun, Moon, Rising, and full planetary lineup (Mercury through Pluto) from your
			birth date, time, and location using deterministic symbolic reasoning.
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
				<span class="font-headline text-lg text-on-surface">Precision Birth Inputs</span>
			</div>

			<div class="relative grid grid-cols-2 sm:grid-cols-4 gap-5">
				<div class="flex flex-col gap-2">
					<label for="month" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">Birth Month</label>
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
					<label for="day" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">Birth Day</label>
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
					<label for="year" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">Birth Year</label>
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
					<label for="hour" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">Birth Hour</label>
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
					<label for="minute" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">Birth Minute</label>
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
					<label for="latitude" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">Birth Latitude</label>
					<input
						id="latitude"
						type="number"
						step="0.0001"
						placeholder="e.g. 40.7128"
						value={latitude ?? ''}
						oninput={(e) => (latitude = e.currentTarget.value === '' ? null : Number(e.currentTarget.value))}
						min="-90"
						max="90"
						class="w-full bg-surface-container-highest text-on-surface rounded-lg px-4 py-3 focus:bg-surface-bright transition-colors outline-none"
					/>
				</div>

				<div class="flex flex-col gap-2">
					<label for="longitude" class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">Birth Longitude</label>
					<input
						id="longitude"
						type="number"
						step="0.0001"
						placeholder="e.g. -74.0060"
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
						<span class="text-sm">Use my location</span>
					</button>
				</div>
			</div>

			{#if locationNote}
				<p class="relative flex items-center gap-2 text-xs text-tertiary mt-3">
					<span class="material-symbols-outlined text-sm">info</span>
					{locationNote}
				</p>
			{/if}

			<p class="relative flex items-center gap-2 text-xs text-on-surface-variant/70 mt-4">
				<span class="material-symbols-outlined text-sm text-primary">info</span>
				{#if latitude !== null && longitude !== null}
					Sun, Moon, Rising &amp; all eight planets (Mercury–Pluto) will be computed from real ecliptic positions (Swiss Ephemeris) using your birth date, time, and location.
				{:else}
					Add your birth year and coordinates above for a precise chart with the full planetary lineup. Without them, only Sun/Moon/Rising are calculated, with Moon and Rising falling back to a rough approximation.
				{/if}
			</p>

			<button
				class="relative mt-6 w-full inline-flex items-center justify-center gap-3 px-8 py-3.5 rounded-full bg-gradient-to-r from-primary-container via-inverse-primary to-secondary-container text-on-primary font-headline text-base font-semibold shadow-xl hover:shadow-[0_0_24px_rgba(76,215,246,0.45)] transition-all disabled:opacity-60 disabled:cursor-not-allowed"
				onclick={calculateChart}
				disabled={loading}
			>
				<span class="material-symbols-outlined text-xl {loading ? 'animate-spin' : ''}">
					{loading ? 'progress_activity' : 'radar'}
				</span>
				<span>{loading ? 'Calculating...' : 'Calculate Birth Chart'}</span>
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
			<LoadingSpinner text="Calculating your birth chart..." />
		{/if}

		{#if chart}
			<!-- Schematic wheel -->
			<div class="mb-10">
				<div class="flex items-center gap-4 mb-4">
					<h2 class="font-headline text-xl text-on-surface">Celestial Wheel</h2>
					<div class="h-px flex-1 bg-surface-container-highest"></div>
					<span class="font-mono-data text-[11px] text-on-surface-variant uppercase">Schematic</span>
				</div>
				<div class="glass-card p-6 lg:p-8 flex flex-col items-center gap-4">
					<svg viewBox="0 0 200 200" class="w-56 h-56 sm:w-64 sm:h-64">
						<circle cx="100" cy="100" r="92" fill="none" stroke="var(--color-outline-variant)" stroke-width="1" opacity="0.4" />
						<circle cx="100" cy="100" r="70" fill="none" stroke="var(--color-outline-variant)" stroke-width="1" opacity="0.3" />
						{#each Array.from({ length: 12 }) as _, i}
							{@const a = (i * 30 * Math.PI) / 180}
							<line
								x1={100 + 70 * Math.cos(a)} y1={100 + 70 * Math.sin(a)}
								x2={100 + 92 * Math.cos(a)} y2={100 + 92 * Math.sin(a)}
								stroke="var(--color-outline-variant)" stroke-width="1" opacity="0.4"
							/>
						{/each}

						{#each [
							{
								key: 'sun', sign: chart.sun_sign, element: chart.element,
								angle: chart.precise && chart.sun_degree !== undefined && chart.rising_degree !== undefined
									? eclipticToWheelAngle(chart.sun_degree, chart.rising_degree)
									: WHEEL_ANGLES.sun
							},
							{
								key: 'moon', sign: chart.moon_sign, element: chart.moon_element,
								angle: chart.precise && chart.moon_degree !== undefined && chart.rising_degree !== undefined
									? eclipticToWheelAngle(chart.moon_degree, chart.rising_degree)
									: WHEEL_ANGLES.moon
							},
							{
								key: 'rising', sign: chart.rising_sign, element: chart.rising_element,
								angle: chart.precise ? -90 : WHEEL_ANGLES.rising
							}
						] as point}
							{@const p = wheelPoint(point.angle, 70)}
							{@const color = getElementColor(point.element)}
							<circle cx={p.x} cy={p.y} r="7" fill={color} fill-opacity="0.2" stroke={color} stroke-width="2" />
							<text x={p.x} y={p.y + 3.5} text-anchor="middle" font-size="8" fill={color}>{getSignSymbol(point.sign)}</text>
						{/each}

						<!-- Mercury..Pluto, plotted at their real ecliptic degrees on an
						     inner ring (precise mode only — no approximate fallback for these). -->
						{#if chart.precise && chart.planets && chart.rising_degree !== undefined}
							{#each chart.planets as planet}
								{#if planet.degree !== undefined}
									{@const p = wheelPoint(eclipticToWheelAngle(planet.degree, chart.rising_degree), 48)}
									{@const color = getElementColor(planet.element)}
									<circle cx={p.x} cy={p.y} r="5.5" fill={color} fill-opacity="0.15" stroke={color} stroke-width="1.5" />
									<text x={p.x} y={p.y + 2.8} text-anchor="middle" font-size="6.5" fill={color}>{planet.symbol}</text>
								{/if}
							{/each}
						{/if}

						<circle cx="100" cy="100" r="3" fill="var(--color-secondary)" />
					</svg>
					<p class="font-mono-data text-[11px] text-on-surface-variant/70 text-center max-w-sm">
						{#if chart.precise}
							Plotted from your real Sun, Moon &amp; Ascendant ecliptic longitudes (Swiss Ephemeris).
						{:else}
							Schematic placement of your Sun, Moon &amp; Rising signs — a stylized representation, not exact ecliptic degrees.
						{/if}
					</p>
				</div>
			</div>

			<!-- Natal Core Triad -->
			<div class="flex items-center gap-4 mb-4">
				<h2 class="font-headline text-xl text-on-surface">Natal Core Triad</h2>
				<div class="h-px flex-1 bg-surface-container-highest"></div>
				<span class="font-mono-data text-[11px] text-on-surface-variant uppercase">Identity Pillars</span>
			</div>
			<div class="grid grid-cols-1 sm:grid-cols-3 gap-5 mb-10">
				<div class="glass-card glass-card-hover relative p-6 flex flex-col overflow-hidden">
					<div class="absolute -top-16 -right-16 w-36 h-36 rounded-full blur-2xl pointer-events-none" style:background-color="{getElementColor(chart.element)}20"></div>
					<div class="relative flex items-center justify-between gap-2 mb-4">
						<span class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider flex items-center gap-1.5">
							<span class="material-symbols-outlined text-sm text-primary">wb_sunny</span>
							Sun Sign
						</span>
						<ElementBadge element={chart.element} size="sm" />
					</div>
					<div class="relative text-5xl mb-2" style:color="{getElementColor(chart.element)}">
						{getSignSymbol(chart.sun_sign)}
					</div>
					<h3 class="relative font-headline text-xl text-on-surface font-semibold capitalize">{chart.sun_sign}</h3>
					<p class="relative text-xs text-on-surface-variant mt-1">Core will &amp; identity</p>
				</div>

				<div class="glass-card glass-card-hover relative p-6 flex flex-col overflow-hidden">
					<div class="absolute -top-16 -right-16 w-36 h-36 rounded-full blur-2xl pointer-events-none" style:background-color="{getElementColor(chart.moon_element)}20"></div>
					<div class="relative flex items-center justify-between gap-2 mb-4">
						<span class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider flex items-center gap-1.5">
							<span class="material-symbols-outlined text-sm text-secondary">bedtime</span>
							Moon Sign
						</span>
						<ElementBadge element={chart.moon_element} size="sm" />
					</div>
					<div class="relative text-5xl mb-2" style:color="{getElementColor(chart.moon_element)}">
						{getSignSymbol(chart.moon_sign)}
					</div>
					<h3 class="relative font-headline text-xl text-on-surface font-semibold capitalize">{chart.moon_sign}</h3>
					<p class="relative text-xs text-on-surface-variant mt-1">Subconscious &amp; emotion</p>
				</div>

				<div class="glass-card glass-card-hover relative p-6 flex flex-col overflow-hidden">
					<div class="absolute -top-16 -right-16 w-36 h-36 rounded-full blur-2xl pointer-events-none" style:background-color="{getElementColor(chart.rising_element)}20"></div>
					<div class="relative flex items-center justify-between gap-2 mb-4">
						<span class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider flex items-center gap-1.5">
							<span class="material-symbols-outlined text-sm text-tertiary">north_east</span>
							Rising Sign
						</span>
						<ElementBadge element={chart.rising_element} size="sm" />
					</div>
					<div class="relative text-5xl mb-2" style:color="{getElementColor(chart.rising_element)}">
						{getSignSymbol(chart.rising_sign)}
					</div>
					<h3 class="relative font-headline text-xl text-on-surface font-semibold capitalize">{chart.rising_sign}</h3>
					<p class="relative text-xs text-on-surface-variant mt-1">Ascendant mask</p>
				</div>
			</div>

			<!-- Full Planetary Lineup -->
			{#if chart.planets && chart.planets.length > 0}
				<div class="flex items-center gap-4 mb-4">
					<h2 class="font-headline text-xl text-on-surface">Full Planetary Lineup</h2>
					<div class="h-px flex-1 bg-surface-container-highest"></div>
					<span class="font-mono-data text-[11px] text-on-surface-variant uppercase">Mercury – Pluto</span>
				</div>
				<div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-10">
					{#each chart.planets as planet}
						<div class="glass-card glass-card-hover relative p-4 flex flex-col overflow-hidden">
							<div class="absolute -top-10 -right-10 w-24 h-24 rounded-full blur-2xl pointer-events-none" style:background-color="{getElementColor(planet.element)}20"></div>
							<div class="relative flex items-center justify-between gap-2 mb-2">
								<span class="font-mono-data text-[10px] text-on-surface-variant uppercase tracking-wider capitalize">{planet.name}</span>
								{#if planet.retrograde}
									<span class="font-mono-data text-[9px] text-tertiary" title="Retrograde">℞</span>
								{/if}
							</div>
							<div class="relative text-3xl mb-1" style:color="{getElementColor(planet.element)}">
								{getSignSymbol(planet.sign)}
							</div>
							<h4 class="relative font-headline text-sm text-on-surface font-semibold capitalize">{planet.sign}</h4>
							<p class="relative text-[11px] text-on-surface-variant/80 mt-1 capitalize">{planet.element} · {planet.modality}</p>
						</div>
					{/each}
				</div>
			{/if}

			<!-- Profile Details -->
			<div class="glass-card p-6 lg:p-8 mb-8">
				<h3 class="font-headline text-lg text-on-surface mb-5">Your Profile</h3>

				<div class="grid grid-cols-2 gap-3 mb-5 bg-surface-container-lowest/60 p-4 rounded-xl">
					<div class="flex flex-col">
						<span class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">Modality</span>
						<span class="text-on-surface font-medium capitalize">{chart.modality}</span>
					</div>
					<div class="flex flex-col">
						<span class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider">Ruling Planet</span>
						<span class="text-on-surface font-medium capitalize">{chart.ruling_planet}</span>
					</div>
				</div>

				{#if chart.personality_style}
					<div class="mb-4 border-b border-white/5 pb-4">
						<div class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider mb-1">Personality Style</div>
						<div class="text-sm text-on-surface/90">{chart.personality_style}</div>
					</div>
				{/if}

				{#if chart.approach_to_life}
					<div class="mb-4 border-b border-white/5 pb-4">
						<div class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider mb-1">Approach to Life</div>
						<div class="text-sm text-on-surface/90">{chart.approach_to_life}</div>
					</div>
				{/if}

				{#if chart.planetary_influence}
					<div>
						<div class="font-mono-data text-[11px] text-on-surface-variant uppercase tracking-wider mb-1">Planetary Influence</div>
						<div class="text-sm text-on-surface/90">{chart.planetary_influence}</div>
					</div>
				{/if}
			</div>

			{#if chart.traits && chart.traits.length > 0}
				<div class="glass-card p-6 lg:p-8 mb-8">
					<h3 class="font-mono-data text-xs text-on-surface-variant uppercase tracking-wider mb-4">Symbolic Traits</h3>
					<div class="flex flex-wrap gap-2">
						{#each chart.traits as trait}
							<span class="px-3 py-1 rounded-md bg-surface-container text-on-surface-variant font-mono-data text-xs capitalize">
								{String(trait).replace(/_/g, ' ')}
							</span>
						{/each}
					</div>
				</div>
			{/if}

			{#if chart.note}
				<div class="glass-card p-4 mb-8 border-tertiary/30 bg-tertiary-container/10">
					<p class="text-tertiary text-xs flex items-start gap-2">
						<span class="material-symbols-outlined text-base">warning</span>
						{chart.note}
					</p>
				</div>
			{/if}

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
