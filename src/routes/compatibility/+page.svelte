<script lang="ts">
	import { analyzeCompatibility, fetchSynastry } from '$lib/utils/api';
	import { ZODIAC_SIGNS, ZODIAC_SYMBOLS } from '$lib/types';
	import type { CompatibilityResult, SynastryResult } from '$lib/types';
	import ZodiacBadge from '$lib/components/ZodiacBadge.svelte';
	import ElementBadge from '$lib/components/ElementBadge.svelte';
	import ReasoningStep from '$lib/components/ReasoningStep.svelte';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import { getApproachTips, type ApproachTips } from '$lib/utils/compatibilityTips';

	let sign1 = $state('aries');
	let sign2 = $state('libra');
	let result = $state<CompatibilityResult | null>(null);
	let loading = $state(false);
	let error = $state('');
	let activeTipTab = $state<'approach' | 'say' | 'dates'>('approach');

	// Feature: Synastry Deep Dive
	let synastry = $state<SynastryResult | null>(null);
	let synastryLoading = $state(false);
	let synastryError = $state('');

	async function loadSynastry() {
		if (!result) return;
		synastryLoading = true;
		synastryError = '';
		synastry = null;
		try {
			const r = await fetchSynastry(result.sign1, result.sign2);
			if ('error' in r) {
				synastryError = String((r as unknown as { error: string }).error);
			} else {
				synastry = r;
			}
		} catch (e) {
			synastryError = e instanceof Error ? e.message : 'Failed to load synastry breakdown';
		} finally {
			synastryLoading = false;
		}
	}

	const tips = $derived(result ? getApproachTips(result.sign1, result.sign2) : null);

	function elementOf(sign: string): string {
		const map: Record<string, string> = {
			aries: 'fire', leo: 'fire', sagittarius: 'fire',
			taurus: 'earth', virgo: 'earth', capricorn: 'earth',
			gemini: 'air', libra: 'air', aquarius: 'air',
			cancer: 'water', scorpio: 'water', pisces: 'water',
		};
		return map[sign] || 'air';
	}

	const levelColors: Record<string, string> = {
		high: 'text-secondary',
		moderate: 'text-tertiary',
		medium: 'text-tertiary',
		low: 'text-error',
	};

	const levelDescriptions: Record<string, string> = {
		high: 'Strong symbolic harmony',
		moderate: 'Balanced potential',
		medium: 'Moderate compatibility',
		low: 'Challenging but growth-oriented',
	};

	async function analyze() {
		if (sign1 === sign2) {
			error = 'Please select two different signs';
			return;
		}
		loading = true;
		error = '';
		synastry = null;
		synastryError = '';
		try {
			result = await analyzeCompatibility(sign1, sign2);
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to analyze compatibility';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Compatibility - AstroLogic</title>
</svelte:head>

<div class="page-container">
	<div class="relative w-full rounded-2xl bg-surface-container-lowest/70 backdrop-blur-xl p-6 lg:p-10 shadow-2xl overflow-hidden mb-8">
		<div class="absolute -top-24 -left-20 w-80 h-80 rounded-full bg-primary-container/20 blur-3xl pointer-events-none"></div>
		<div class="absolute -bottom-24 -right-20 w-80 h-80 rounded-full bg-secondary-container/20 blur-3xl pointer-events-none"></div>

		<div class="relative z-10 mb-6">
			<div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-container-high/90 text-secondary text-[10px] font-semibold uppercase tracking-widest mb-3">
				<span class="w-1.5 h-1.5 rounded-full bg-secondary animate-ping"></span>
				Symbolic Compatibility Engine
			</div>
			<h1 class="font-headline text-2xl sm:text-3xl text-on-surface tracking-tight">
				Zodiac <span class="gradient-text">Compatibility</span> Matrix
			</h1>
			<p class="text-on-surface-variant mt-2 max-w-2xl">
				Evaluate symbolic harmony, elemental resonance, and modality dynamics between two zodiac signs.
			</p>
		</div>

		<div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 items-center gap-6">
			<div class="lg:col-span-5 bg-surface-container/60 hover:bg-surface-container/80 transition-all duration-300 rounded-2xl p-6 relative shadow-lg">
				<div class="absolute top-4 right-4">
					<span class="text-[10px] font-semibold uppercase px-2.5 py-1 rounded-full bg-surface-container-highest text-primary-fixed-dim">Person 1</span>
				</div>
				<div class="flex items-center gap-4 mb-4">
					<ZodiacBadge sign={sign1} size="lg" />
					<div class="min-w-0">
						<label for="sign1" class="block text-xs text-on-surface-variant uppercase tracking-wide mb-1.5">Select Sign</label>
						<select id="sign1" bind:value={sign1} class="input-field capitalize">
							{#each ZODIAC_SIGNS as sign}
								<option value={sign}>{ZODIAC_SYMBOLS[sign]} {sign}</option>
							{/each}
						</select>
					</div>
				</div>
			</div>

			<div class="lg:col-span-2 flex flex-col items-center justify-center text-center px-2 py-2 relative">
				<div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-40">
					<svg class="w-full h-16" fill="none" viewBox="0 0 200 60">
						<path class="text-secondary animate-pulse" d="M 10 30 Q 100 8 190 30" stroke="currentColor" stroke-dasharray="4 4" stroke-width="1.5" />
						<path class="text-primary" d="M 10 30 Q 100 52 190 30" stroke="currentColor" stroke-width="1" />
					</svg>
				</div>
				<div class="relative z-10 w-16 h-16 rounded-full bg-gradient-to-br from-primary-container via-surface-container-lowest to-secondary-container p-1 shadow-[0_0_25px_rgba(76,215,246,0.35)] flex items-center justify-center">
					<span class="material-symbols-outlined text-2xl text-on-surface">favorite</span>
				</div>
				<span class="relative z-10 mt-2 text-[10px] uppercase tracking-widest text-on-surface-variant">Synastry</span>
			</div>

			<div class="lg:col-span-5 bg-surface-container/60 hover:bg-surface-container/80 transition-all duration-300 rounded-2xl p-6 relative shadow-lg">
				<div class="absolute top-4 right-4">
					<span class="text-[10px] font-semibold uppercase px-2.5 py-1 rounded-full bg-surface-container-highest text-secondary-fixed">Person 2</span>
				</div>
				<div class="flex items-center gap-4 mb-4">
					<ZodiacBadge sign={sign2} size="lg" />
					<div class="min-w-0">
						<label for="sign2" class="block text-xs text-on-surface-variant uppercase tracking-wide mb-1.5">Select Sign</label>
						<select id="sign2" bind:value={sign2} class="input-field capitalize">
							{#each ZODIAC_SIGNS as sign}
								<option value={sign}>{ZODIAC_SYMBOLS[sign]} {sign}</option>
							{/each}
						</select>
					</div>
				</div>
			</div>
		</div>

		{#if error}
			<div class="relative z-10 mt-6 p-4 rounded-xl border border-error/30 bg-error-container/20">
				<p class="text-error text-sm">{error}</p>
			</div>
		{/if}

		<div class="relative z-10 mt-6 flex flex-col items-center gap-4">
			<button
				class="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-gradient-to-r from-primary-container to-secondary-container text-on-primary font-headline font-semibold shadow-[0_0_20px_rgba(124,58,237,0.4)] hover:shadow-[0_0_30px_rgba(76,215,246,0.6)] hover:scale-105 active:scale-95 transition-all disabled:opacity-60 disabled:pointer-events-none"
				onclick={analyze}
				disabled={loading}
			>
				<span class="material-symbols-outlined text-lg" class:animate-spin={loading}>autorenew</span>
				<span>{loading ? 'Analyzing...' : 'Analyze Compatibility'}</span>
			</button>

			{#if loading}
				<LoadingSpinner text="Consulting symbolic connections..." />
			{/if}
		</div>
	</div>

	{#if result}
		<div class="flex flex-col gap-6">
			<!-- Classification Status Banner -->
			<div class="w-full rounded-xl bg-surface-container/70 backdrop-blur-md p-4 lg:px-6 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-md">
				<div class="flex items-center gap-3">
					<div class="p-2 rounded-lg bg-primary-container/30 text-primary">
						<span class="material-symbols-outlined text-xl">all_inclusive</span>
					</div>
					<div>
						<p class="text-[10px] uppercase text-on-surface-variant tracking-wider">Classification Status</p>
						<p class="font-headline text-lg {levelColors[result.level] || 'text-on-surface'}">
							{(result.level || 'medium').toUpperCase()} &bull; {levelDescriptions[result.level] || ''}
						</p>
					</div>
				</div>
				<div class="flex items-center gap-3">
					<ZodiacBadge sign={result.sign1} size="sm" />
					<span class="material-symbols-outlined text-on-surface-variant">sync_alt</span>
					<ZodiacBadge sign={result.sign2} size="sm" />
				</div>
			</div>

			<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
				<!-- Left: Element & Modality Matrix -->
				<div class="lg:col-span-5 flex flex-col gap-6">
					<div class="rounded-2xl bg-surface-container/70 backdrop-blur-md p-6 shadow-xl">
						<div class="flex items-center gap-2 mb-4">
							<span class="material-symbols-outlined text-primary text-xl">water_drop</span>
							<h3 class="font-headline text-lg text-on-surface">Element &amp; Modality Matrix</h3>
						</div>

						<div class="grid grid-cols-2 gap-4 mb-6">
							<div class="text-center p-4 rounded-xl bg-surface-container-lowest/60">
								<div class="text-[10px] uppercase text-on-surface-variant mb-2 tracking-wider">Elements</div>
								<div class="flex items-center justify-center gap-2 flex-wrap">
									<ElementBadge element={result.element1} size="sm" />
									<span class="text-on-surface-variant text-xs">&amp;</span>
									<ElementBadge element={result.element2} size="sm" />
								</div>
							</div>
							<div class="text-center p-4 rounded-xl bg-surface-container-lowest/60">
								<div class="text-[10px] uppercase text-on-surface-variant mb-2 tracking-wider">Modalities</div>
								<div class="font-medium capitalize text-on-surface font-mono-data text-sm">
									{result.modality1} &amp; {result.modality2}
								</div>
							</div>
						</div>

						<div class="p-4 rounded-xl bg-surface-container-lowest/60">
							<h4 class="text-sm font-semibold text-primary mb-2">Element Relationship</h4>
							<p class="text-on-surface-variant text-sm leading-relaxed">{result.element_description}</p>
						</div>
					</div>
				</div>

				<!-- Right: Reasoning Trace -->
				<div class="lg:col-span-7 flex flex-col gap-6">
					{#if result.reasoning.length > 0}
						<div class="rounded-2xl bg-surface-container-lowest/90 backdrop-blur-md p-6 shadow-2xl">
							<div class="flex items-center justify-between pb-4">
								<div class="flex items-center gap-2">
									<span class="w-2.5 h-2.5 rounded-full bg-secondary shadow-[0_0_8px_#4cd7f6] animate-pulse"></span>
									<span class="font-mono-data text-xs text-secondary uppercase font-semibold tracking-wider">
										Prolog Symbolic Inference
									</span>
								</div>
							</div>
							<div class="space-y-2">
								{#each result.reasoning as step, i}
									<ReasoningStep {step} index={i} />
								{/each}
							</div>
						</div>
					{/if}

					{#if tips}
						<!-- Crush Tips Section -->
						<div class="rounded-2xl bg-surface-container-lowest/90 backdrop-blur-md p-6 shadow-2xl">
							<div class="flex items-center gap-2 mb-4">
								<span class="material-symbols-outlined text-primary text-xl">favorite</span>
								<h3 class="font-headline text-lg text-on-surface">
									How to Win Over <span class="capitalize">{result.sign2}</span>
								</h3>
							</div>

							<!-- Tab bar -->
							<div class="flex gap-1 p-1 rounded-xl bg-surface-container mb-5">
								<button
									type="button"
									onclick={() => activeTipTab = 'approach'}
									class="flex-1 flex items-center justify-center gap-1.5 rounded-lg px-3 py-2 text-xs font-medium transition-all
										{activeTipTab === 'approach' ? 'bg-primary-container text-primary shadow-sm' : 'text-on-surface-variant hover:bg-surface-container-high'}"
								>
									<span class="material-symbols-outlined text-sm">explore</span>
									Approach
								</button>
								<button
									type="button"
									onclick={() => activeTipTab = 'say'}
									class="flex-1 flex items-center justify-center gap-1.5 rounded-lg px-3 py-2 text-xs font-medium transition-all
										{activeTipTab === 'say' ? 'bg-secondary-container text-secondary shadow-sm' : 'text-on-surface-variant hover:bg-surface-container-high'}"
								>
									<span class="material-symbols-outlined text-sm">chat</span>
									What to Say
								</button>
								<button
									type="button"
									onclick={() => activeTipTab = 'dates'}
									class="flex-1 flex items-center justify-center gap-1.5 rounded-lg px-3 py-2 text-xs font-medium transition-all
										{activeTipTab === 'dates' ? 'bg-tertiary-container text-tertiary shadow-sm' : 'text-on-surface-variant hover:bg-surface-container-high'}"
								>
									<span class="material-symbols-outlined text-sm">event</span>
									Date Ideas
								</button>
							</div>

							<!-- Tab content -->
							{#if activeTipTab === 'approach'}
								<div class="space-y-3">
									<div class="flex items-start gap-3 rounded-xl bg-surface-container-high/60 p-3.5">
										<div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary-container text-primary">
											<span class="material-symbols-outlined text-lg">north_east</span>
										</div>
										<div>
											<span class="text-[10px] uppercase tracking-wider text-on-surface-variant">First Move</span>
											<p class="text-sm text-on-surface mt-0.5">{tips.approach.firstMove}</p>
										</div>
									</div>
									<div class="flex items-start gap-3 rounded-xl bg-surface-container-high/60 p-3.5">
										<div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-secondary-container text-secondary">
											<span class="material-symbols-outlined text-lg">location_on</span>
										</div>
										<div>
											<span class="text-[10px] uppercase tracking-wider text-on-surface-variant">Best Setting</span>
											<p class="text-sm text-on-surface mt-0.5">{tips.approach.setting}</p>
										</div>
									</div>
									<div class="flex items-start gap-3 rounded-xl bg-surface-container-high/60 p-3.5">
										<div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-tertiary-container text-tertiary">
											<span class="material-symbols-outlined text-lg">spa</span>
										</div>
										<div>
											<span class="text-[10px] uppercase tracking-wider text-on-surface-variant">Right Vibe</span>
											<p class="text-sm text-on-surface mt-0.5">{tips.approach.vibe}</p>
										</div>
									</div>
									<div class="flex items-start gap-3 rounded-xl bg-error-container/10 p-3.5">
										<div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-error-container text-error">
											<span class="material-symbols-outlined text-lg">block</span>
										</div>
										<div>
											<span class="text-[10px] uppercase tracking-wider text-error">Avoid</span>
											<p class="text-sm text-on-surface mt-0.5">{tips.approach.avoid}</p>
										</div>
									</div>
									{#if tips.intimacyTip}
										<div class="mt-2 rounded-xl bg-primary-container/10 p-3.5 border border-primary/20">
											<span class="text-[10px] uppercase tracking-wider text-primary font-semibold">Building Trust</span>
											<p class="text-sm text-on-surface mt-1">{tips.intimacyTip}</p>
										</div>
									{/if}
								</div>
							{:else if activeTipTab === 'say'}
								<div class="space-y-3">
									<p class="text-sm text-on-surface-variant mb-3">
										Here are some conversation starters that resonate with <span class="capitalize font-medium text-on-surface">{result.sign2}</span>:
									</p>
									{#each tips.conversationStarters as starter, i}
										<div class="flex items-start gap-3 rounded-xl bg-surface-container-high/60 p-3.5">
											<div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-secondary-container text-secondary font-bold text-sm">
												{i + 1}
											</div>
											<div>
												<p class="text-sm text-on-surface leading-relaxed">"{starter}"</p>
											</div>
										</div>
									{/each}
									<div class="mt-3 rounded-xl bg-surface-container-high/40 p-3.5">
										<span class="text-[10px] uppercase tracking-wider text-on-surface-variant">Pro tip</span>
										<p class="text-sm text-on-surface mt-1">
											{#if elementOf(result.sign2) === 'fire'}
												Ask about their goals and dreams — they light up when talking about their ambitions.
											{:else if elementOf(result.sign2) === 'earth'}
												Show genuine interest in their daily life and routines — they love being appreciated for the little things.
											{:else if elementOf(result.sign2) === 'air'}
												Challenge them intellectually — they fall for minds that keep up with theirs.
											{:else}
												Listen deeply and share something personal — emotional connection is everything to them.
											{/if}
										</p>
									</div>
								</div>
							{:else}
								<div class="space-y-3">
									<p class="text-sm text-on-surface-variant mb-3">
										Ideal date ideas for a connection between <span class="capitalize font-medium text-on-surface">{result.sign1}</span> & <span class="capitalize font-medium text-on-surface">{result.sign2}</span>:
									</p>
									{#each tips.dateIdeas as idea, i}
										<div class="flex items-start gap-3 rounded-xl bg-surface-container-high/60 p-3.5">
											<div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-tertiary-container text-tertiary">
												<span class="material-symbols-outlined text-lg">
													{i === 0 ? 'local_fire_department' : i === 1 ? 'restaurant' : 'celebration'}
												</span>
											</div>
											<p class="text-sm text-on-surface">{idea}</p>
										</div>
									{/each}
									<div class="mt-2 rounded-xl bg-secondary-container/10 p-3.5 border border-secondary/20">
										<span class="text-[10px] uppercase tracking-wider text-secondary font-semibold">Key Takeaway</span>
										<p class="text-sm text-on-surface mt-1">
											{#if elementOf(result.sign1) === elementOf(result.sign2)}
												You share the same element — lean into that natural understanding. Your instincts about each other are likely right.
											{:else}
												Different elements create dynamic tension. Embrace what makes you different — that's where the chemistry lives.
											{/if}
										</p>
									</div>
								</div>
							{/if}
						</div>
					{/if}

					<!-- Feature: Synastry Deep Dive -->
					<div class="rounded-2xl bg-surface-container-lowest/90 backdrop-blur-md p-6 shadow-2xl">
						<div class="flex items-center justify-between mb-4 flex-wrap gap-3">
							<div class="flex items-center gap-2">
								<span class="material-symbols-outlined text-primary text-xl">insights</span>
								<h3 class="font-headline text-lg text-on-surface">Synastry Deep Dive</h3>
							</div>
							{#if !synastry}
								<button
									class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-surface-container-high text-on-surface text-xs font-mono-data uppercase tracking-wider hover:bg-surface-container-highest transition-colors disabled:opacity-60"
									onclick={loadSynastry}
									disabled={synastryLoading}
								>
									<span class="material-symbols-outlined text-base" class:animate-spin={synastryLoading}>autorenew</span>
									{synastryLoading ? 'Loading...' : 'Load Full Breakdown'}
								</button>
							{/if}
						</div>

						{#if synastryError}
							<p class="text-error text-sm">{synastryError}</p>
						{:else if synastry}
							<!-- Score bars -->
							<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
								{#each [
									{ key: 'element', label: 'Element', c: synastry.score_breakdown.element },
									{ key: 'modality', label: 'Modality', c: synastry.score_breakdown.modality },
									{ key: 'traits', label: 'Traits', c: synastry.score_breakdown.traits },
									{ key: 'planetary', label: 'Planetary', c: synastry.score_breakdown.planetary },
								] as row}
									<div class="p-4 rounded-xl bg-surface-container-high/60">
										<div class="flex items-center justify-between mb-1.5">
											<span class="text-xs font-semibold text-on-surface">{row.label}</span>
											<span class="font-mono-data text-[10px] text-on-surface-variant">
												weight {Math.round(row.c.weight * 100)}% &bull; {Math.round(row.c.score)}/100
											</span>
										</div>
										<div class="h-2 rounded-full bg-surface-container-lowest overflow-hidden mb-1.5">
											<div
												class="h-full rounded-full bg-gradient-to-r from-primary-container to-secondary-container"
												style:width="{Math.min(100, Math.max(0, row.c.score))}%"
											></div>
										</div>
										<p class="text-xs text-on-surface-variant">{row.c.description}</p>
									</div>
								{/each}
							</div>

							<div class="text-center mb-6">
								<span class="font-mono-data text-[10px] uppercase text-on-surface-variant tracking-wider">Overall Synastry Score</span>
								<div class="font-headline text-2xl text-primary">{Math.round(synastry.overall_score)} / 100</div>
							</div>

							<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
								<div class="p-4 rounded-xl bg-surface-container-high/60">
									<h4 class="text-sm font-semibold text-secondary mb-1.5 flex items-center gap-1.5">
										<span class="material-symbols-outlined text-base">forum</span>
										Communication Style
									</h4>
									<p class="text-sm text-on-surface-variant">{synastry.communication_theme}</p>
								</div>
								<div class="p-4 rounded-xl bg-surface-container-high/60">
									<h4 class="text-sm font-semibold text-tertiary mb-1.5 flex items-center gap-1.5">
										<span class="material-symbols-outlined text-base">balance</span>
										Balance Theme
									</h4>
									<p class="text-sm text-on-surface-variant">{synastry.balance_theme}</p>
								</div>
							</div>

							<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
								<div class="p-4 rounded-xl bg-primary-container/10">
									<h4 class="text-sm font-semibold text-primary mb-2 flex items-center gap-1.5">
										<span class="material-symbols-outlined text-base">star</span>
										Strengths
									</h4>
									<ul class="space-y-1.5">
										{#each synastry.strengths as s}
											<li class="text-sm text-on-surface flex items-start gap-1.5">
												<span class="material-symbols-outlined text-sm text-primary mt-0.5">check</span>
												{s}
											</li>
										{/each}
									</ul>
								</div>
								<div class="p-4 rounded-xl bg-error-container/10">
									<h4 class="text-sm font-semibold text-error mb-2 flex items-center gap-1.5">
										<span class="material-symbols-outlined text-base">warning</span>
										Growth Areas
									</h4>
									<ul class="space-y-1.5">
										{#each synastry.challenges as c}
											<li class="text-sm text-on-surface flex items-start gap-1.5">
												<span class="material-symbols-outlined text-sm text-error mt-0.5">arrow_forward</span>
												{c}
											</li>
										{/each}
									</ul>
								</div>
							</div>

							{#if synastry.complementary_traits.length > 0}
								<div class="p-4 rounded-xl bg-surface-container-high/40">
									<h4 class="text-sm font-semibold text-on-surface mb-2 flex items-center gap-1.5">
										<span class="material-symbols-outlined text-base">join_inner</span>
										Complementary Traits
									</h4>
									<div class="flex flex-wrap gap-2">
										{#each synastry.complementary_traits as pair}
											<span class="px-3 py-1 rounded-full bg-surface-container text-xs font-mono-data text-on-surface-variant">
												{pair.trait1} <span class="text-primary">&harr;</span> {pair.trait2}
											</span>
										{/each}
									</div>
								</div>
							{/if}
						{:else}
							<p class="text-sm text-on-surface-variant">
								Load the full synastry breakdown for numeric score components, communication style,
								balance themes, and complementary trait pairing.
							</p>
						{/if}
					</div>

					<div class="rounded-xl bg-surface-container/60 p-4 text-center">
						<p class="text-xs text-on-surface-variant italic">
							This compatibility analysis is for entertainment and self-reflection purposes only.
							It does not scientifically predict relationship outcomes.
						</p>
					</div>

					<button class="btn-secondary w-full" onclick={() => { result = null; synastry = null; }}>New Analysis</button>
				</div>
			</div>
		</div>
	{/if}
</div>
