<script lang="ts">
	import type { BirthChartExplanationData, BirthChartAspect } from '$lib/types';
	import { locale, t, formatElement, formatModality, formatPlanet } from '$lib/i18n';
	import { ELEMENT_COLORS, ZODIAC_SYMBOLS } from '$lib/types';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';

	interface Props {
		chart: any;
		birthInfo?: {
			year?: number;
			month?: number;
			day?: number;
			hour?: number;
			minute?: number;
			latitude?: number | null;
			longitude?: number | null;
		};
	}

	let { chart, birthInfo }: Props = $props();

	let explanation = $state<BirthChartExplanationData | null>(null);
	let loading = $state(false);
	let error = $state('');
	let isOpen = $state(false);
	let activeTab = $state<'triad' | 'planets' | 'aspects' | 'elements'>('triad');

	async function fetchExplanation() {
		if (!chart) return;
		loading = true;
		error = '';

		try {
			const res = await fetch('http://localhost:8000/api/birth-chart/explain', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					chart,
					locale: $locale,
					birth_info: birthInfo
				}),
			});

			const data = await res.json();
			if (data.error) {
				error = data.error;
			} else if (data.explanation) {
				explanation = data.explanation;
				isOpen = true;
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to generate birth chart explanation';
		} finally {
			loading = false;
		}
	}

	// Re-fetch explanation automatically if user changes language while explanation is visible
	$effect(() => {
		const currentLocale = $locale;
		if (isOpen && chart && explanation) {
			fetchExplanation();
		}
	});

	function getElementColor(element: string): string {
		return ELEMENT_COLORS[element] || '#9333ea';
	}

	function getAspectBadgeColor(type: string): string {
		switch (type) {
			case 'harmonious':
				return 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30';
			case 'dynamic':
				return 'bg-amber-500/15 text-amber-400 border-amber-500/30';
			case 'polarity':
				return 'bg-rose-500/15 text-rose-400 border-rose-500/30';
			default:
				return 'bg-sky-500/15 text-sky-400 border-sky-500/30';
		}
	}

	function getAspectTypeLabel(type: string, isMy: boolean): string {
		if (isMy) {
			switch (type) {
				case 'harmonious': return 'သဟဇာတဖြစ် (Harmonious)';
				case 'dynamic': return 'စိန်ခေါ်မှု/တိုးတက်မှု (Dynamic)';
				case 'polarity': return 'ချိန်ခွင်လျှာ (Polarity)';
				default: return 'ပေါင်းစပ်မှု (Unified)';
			}
		} else {
			switch (type) {
				case 'harmonious': return 'Harmonious Flow';
				case 'dynamic': return 'Evolutionary Tension';
				case 'polarity': return 'Complementary Polarity';
				default: return 'Unified Synthesis';
			}
		}
	}
</script>

<div class="w-full my-8">
	<!-- Trigger Section -->
	{#if !isOpen}
		<div class="glass-card relative overflow-hidden p-6 sm:p-8 border border-primary/20 bg-gradient-to-br from-surface-container-high/80 via-surface-container/60 to-surface-container-lowest/90 text-center flex flex-col items-center gap-4">
			<div class="absolute -top-20 -left-20 w-48 h-48 rounded-full bg-primary/10 blur-3xl pointer-events-none"></div>
			<div class="absolute -bottom-20 -right-20 w-48 h-48 rounded-full bg-secondary/10 blur-3xl pointer-events-none"></div>

			<div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-primary/20 via-purple-500/20 to-secondary/20 flex items-center justify-center text-primary shadow-lg border border-primary/30">
				<span class="material-symbols-outlined text-2xl">psychology_alt</span>
			</div>

			<div class="max-w-xl">
				<h3 class="font-headline text-xl sm:text-2xl text-on-surface font-semibold mb-2">
					{$locale === 'my' ? 'မွေးဖွားမှုဇာတာ အသေးစိတ် ရှင်းလင်းချက် ရယူမည်' : 'Want an In-Depth Explanation of Your Birth Chart?'}
				</h3>
				<p class="text-sm text-on-surface-variant leading-relaxed">
					{$locale === 'my'
						? 'သင့်နေမင်း၊ လမင်း၊ စန်းလဂ်နှင့် ဂြိုဟ် ၁၁ လုံး၏ အတွင်းစိတ်လွှမ်းမိုးမှု၊ အဓိက ထောင့်ချိတ်ဆက်မှုများ (Aspects) နှင့် ဓာတ်သဘောမျှတမှုကို အသေးစိတ် ဖတ်ရှုလေ့လာပါ။'
						: 'Unpack the psychological blueprint of your Big Three, 11 celestial archetypes, major angular aspects, and elemental constitution with comprehensive cosmic analysis.'}
				</p>
			</div>

			{#if error}
				<p class="text-error text-xs flex items-center gap-1.5">
					<span class="material-symbols-outlined text-sm">error</span>
					{error}
				</p>
			{/if}

			<button
				type="button"
				onclick={fetchExplanation}
				disabled={loading}
				class="mt-2 inline-flex items-center gap-3 px-8 py-3.5 rounded-full bg-gradient-to-r from-primary via-purple-600 to-secondary text-on-primary font-headline text-sm font-semibold shadow-lg shadow-primary/25 hover:shadow-primary/40 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-60 cursor-pointer"
			>
				<span class="material-symbols-outlined text-lg {loading ? 'animate-spin' : ''}">
					{loading ? 'progress_activity' : 'auto_awesome'}
				</span>
				<span>
					{loading
						? ($locale === 'my' ? 'ရှင်းလင်းချက် ပြုစုနေပါသည်...' : 'Analyzing Birth Chart...')
						: ($locale === 'my' ? '✨ မွေးဖွားမှုဇာတာ အပြည့်အစုံ ရှင်းလင်းချက် ဖတ်မည်' : '✨ Explain My Birth Chart')}
				</span>
			</button>
		</div>
	{:else if explanation}
		<!-- Main Deep-Dive Explanation Panel -->
		<div class="glass-card relative overflow-hidden border border-primary/30 p-6 lg:p-8 rounded-2xl shadow-2xl bg-surface-container-lowest/90 backdrop-blur-xl">
			<!-- Header with Close & Toggle -->
			<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-surface-container-highest">
				<div>
					<div class="flex items-center gap-2 mb-1">
						<span class="w-2 h-2 rounded-full bg-secondary animate-ping"></span>
						<span class="font-mono-data text-xs text-secondary tracking-widest uppercase">
							{$locale === 'my' ? 'ဇာတာရှင်၏ စိတ်ပညာနှင့် နက္ခတ်ဗေဒ အနုစိတ်ဆန်းစစ်ချက်' : 'Cosmic Blueprint & Psychological Profile'}
						</span>
					</div>
					<h2 class="font-headline text-2xl sm:text-3xl text-on-surface font-bold">
						{explanation.archetype_title}
					</h2>
				</div>

				<div class="flex items-center gap-2 self-end sm:self-auto">
					<button
						type="button"
						onclick={() => (isOpen = false)}
						class="px-3.5 py-1.5 rounded-lg bg-surface-container-highest hover:bg-surface-bright text-on-surface-variant hover:text-on-surface text-xs font-medium transition-colors flex items-center gap-1.5"
					>
						<span class="material-symbols-outlined text-sm">close</span>
						<span>{$locale === 'my' ? 'ပိတ်မည်' : 'Collapse'}</span>
					</button>
				</div>
			</div>

			<!-- Navigation Tabs -->
			<div class="flex flex-wrap gap-2 my-6 p-1.5 rounded-xl bg-surface-container-highest/60 border border-white/5">
				<button
					type="button"
					onclick={() => (activeTab = 'triad')}
					class="flex-1 min-w-[130px] py-2.5 px-3 rounded-lg text-xs font-headline font-semibold transition-all flex items-center justify-center gap-2 {activeTab === 'triad' ? 'bg-primary text-on-primary shadow-md' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-bright/40'}"
				>
					<span class="material-symbols-outlined text-base">diversity_3</span>
					<span>{$locale === 'my' ? 'အဓိကမဏ္ဍိုင် ၃ မျိုး' : 'The Big Three'}</span>
				</button>

				<button
					type="button"
					onclick={() => (activeTab = 'planets')}
					class="flex-1 min-w-[130px] py-2.5 px-3 rounded-lg text-xs font-headline font-semibold transition-all flex items-center justify-center gap-2 {activeTab === 'planets' ? 'bg-primary text-on-primary shadow-md' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-bright/40'}"
				>
					<span class="material-symbols-outlined text-base">scatter_plot</span>
					<span>{$locale === 'my' ? 'ဂြိုဟ် ၁၁ လုံး အနေအထား' : 'Planetary Dimensions'}</span>
				</button>

				<button
					type="button"
					onclick={() => (activeTab = 'aspects')}
					class="flex-1 min-w-[130px] py-2.5 px-3 rounded-lg text-xs font-headline font-semibold transition-all flex items-center justify-center gap-2 {activeTab === 'aspects' ? 'bg-primary text-on-primary shadow-md' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-bright/40'}"
				>
					<span class="material-symbols-outlined text-base">hub</span>
					<span>{$locale === 'my' ? 'ထောင့်ချိတ်ဆက်မှုများ' : 'Harmonic Aspects'}</span>
					{#if explanation.aspects?.length}
						<span class="text-[10px] px-1.5 py-0.5 rounded-full bg-white/20">{explanation.aspects.length}</span>
					{/if}
				</button>

				<button
					type="button"
					onclick={() => (activeTab = 'elements')}
					class="flex-1 min-w-[130px] py-2.5 px-3 rounded-lg text-xs font-headline font-semibold transition-all flex items-center justify-center gap-2 {activeTab === 'elements' ? 'bg-primary text-on-primary shadow-md' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-bright/40'}"
				>
					<span class="material-symbols-outlined text-base">water_drop</span>
					<span>{$locale === 'my' ? 'ဓာတ်သဘောနှင့် လမ်းညွှန်ချက်' : 'Elements & Guidance'}</span>
				</button>
			</div>

			<!-- TAB 1: THE BIG THREE (CORE IDENTITY) -->
			{#if activeTab === 'triad'}
				<div class="space-y-6">
					<div class="grid grid-cols-1 md:grid-cols-3 gap-5">
						<!-- Sun Sign Deep Dive -->
						<div class="glass-card p-5 border border-primary/20 bg-surface-container-high/40 rounded-xl flex flex-col justify-between">
							<div>
								<div class="flex items-center justify-between mb-3">
									<span class="font-mono-data text-[11px] text-primary uppercase font-bold tracking-wider flex items-center gap-1.5">
										<span class="text-base">☉</span>
										{explanation.core_identity.sun.name}
									</span>
									<span class="text-2xl text-primary font-serif">
										{ZODIAC_SYMBOLS[explanation.core_identity.sun.sign] || '☉'}
									</span>
								</div>
								<h4 class="font-headline text-lg font-bold text-on-surface mb-2">
									{explanation.core_identity.sun.sign_display}
								</h4>
								<p class="text-xs text-on-surface/90 leading-relaxed mb-4">
									{explanation.core_identity.sun.essence}
								</p>
							</div>

							<div>
								<div class="mb-3">
									<div class="text-[11px] font-mono-data text-on-surface-variant uppercase mb-1.5">
										{$locale === 'my' ? 'အဓိက အားသာချက်များ' : 'Key Strengths'}
									</div>
									<div class="flex flex-wrap gap-1.5">
										{#each explanation.core_identity.sun.strengths as strength}
											<span class="text-[11px] px-2 py-0.5 rounded-md bg-primary/10 text-primary border border-primary/20">
												{strength}
											</span>
										{/each}
									</div>
								</div>
								<div class="pt-3 border-t border-white/5">
									<div class="text-[11px] font-mono-data text-secondary uppercase mb-1">
										{$locale === 'my' ? 'ဘဝသင်ခန်းစာ' : 'Growth Lesson'}
									</div>
									<p class="text-xs text-on-surface-variant leading-relaxed">
										{explanation.core_identity.sun.growth_lesson}
									</p>
								</div>
							</div>
						</div>

						<!-- Moon Sign Deep Dive -->
						<div class="glass-card p-5 border border-secondary/20 bg-surface-container-high/40 rounded-xl flex flex-col justify-between">
							<div>
								<div class="flex items-center justify-between mb-3">
									<span class="font-mono-data text-[11px] text-secondary uppercase font-bold tracking-wider flex items-center gap-1.5">
										<span class="text-base">☽</span>
										{explanation.core_identity.moon.name}
									</span>
									<span class="text-2xl text-secondary font-serif">
										{ZODIAC_SYMBOLS[explanation.core_identity.moon.sign] || '☽'}
									</span>
								</div>
								<h4 class="font-headline text-lg font-bold text-on-surface mb-2">
									{explanation.core_identity.moon.sign_display}
								</h4>
								<p class="text-xs text-on-surface/90 leading-relaxed mb-4">
									{explanation.core_identity.moon.essence}
								</p>
							</div>

							<div class="pt-3 border-t border-white/5">
								<div class="text-[11px] font-mono-data text-secondary uppercase mb-1">
									{$locale === 'my' ? 'အတွင်းစိတ် လုံခြုံမှု လိုအပ်ချက်' : 'Subconscious Core Need'}
								</div>
								<p class="text-xs text-on-surface-variant leading-relaxed">
									{explanation.core_identity.moon.need}
								</p>
							</div>
						</div>

						<!-- Rising Sign Deep Dive -->
						<div class="glass-card p-5 border border-tertiary/20 bg-surface-container-high/40 rounded-xl flex flex-col justify-between">
							<div>
								<div class="flex items-center justify-between mb-3">
									<span class="font-mono-data text-[11px] text-tertiary uppercase font-bold tracking-wider flex items-center gap-1.5">
										<span class="text-base">AC</span>
										{explanation.core_identity.rising.name}
									</span>
									<span class="text-2xl text-tertiary font-serif">
										{ZODIAC_SYMBOLS[explanation.core_identity.rising.sign] || 'AC'}
									</span>
								</div>
								<h4 class="font-headline text-lg font-bold text-on-surface mb-2">
									{explanation.core_identity.rising.sign_display}
								</h4>
								<p class="text-xs text-on-surface/90 leading-relaxed mb-4">
									{explanation.core_identity.rising.essence}
								</p>
							</div>

							<div class="pt-3 border-t border-white/5">
								<div class="text-[11px] font-mono-data text-tertiary uppercase mb-1">
									{$locale === 'my' ? 'ပထမဆုံးတွေ့ဆုံမှု အရှိန်အဝါ' : 'First Impression & Vibe'}
								</div>
								<p class="text-xs text-on-surface-variant leading-relaxed">
									{explanation.core_identity.rising.vibe}
								</p>
							</div>
						</div>
					</div>

					<!-- Triad Synthesis Narrative Box -->
					<div class="p-6 rounded-xl bg-gradient-to-r from-primary/10 via-purple-500/10 to-secondary/10 border border-primary/20">
						<div class="flex items-center gap-2 mb-3">
							<span class="material-symbols-outlined text-primary text-xl">merge</span>
							<h4 class="font-headline text-base text-on-surface font-semibold">
								{$locale === 'my' ? 'စွမ်းအင် ၃ ခု ပေါင်းစပ်လှုပ်ရှားမှု (Triad Alchemy)' : 'Triad Dynamic Synthesis'}
							</h4>
						</div>
						<p class="text-sm text-on-surface/95 leading-relaxed">
							{explanation.core_identity.triad_synthesis}
						</p>
					</div>
				</div>
			{/if}

			<!-- TAB 2: PLANETARY DIMENSIONS -->
			{#if activeTab === 'planets'}
				<div class="space-y-4">
					<p class="text-xs text-on-surface-variant mb-3">
						{$locale === 'my'
							? 'ဂြိုဟ်တစ်ခုစီသည် သင့်စိတ်နှင့် ဘဝ၏ သီးခြားကဏ္ဍတစ်ခုစီကို ကိုယ်စားပြုသည်။ အောက်ပါဇယားတွင် ဂြိုဟ် ၁၁ လုံး၏ အနေအထားနှင့် လွှမ်းမိုးမှုများကို လေ့လာပါ။'
							: 'Each celestial body governs a distinct cognitive and life dimension. Here is the complete evolutionary profile of your 11 planetary placements.'}
					</p>

					<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
						{#each explanation.planetary_breakdown as p}
							<div class="glass-card p-4 rounded-xl border border-white/5 hover:border-primary/30 transition-all flex flex-col justify-between">
								<div>
									<div class="flex items-center justify-between mb-2">
										<div class="flex items-center gap-2">
											<span class="text-lg font-serif text-primary">{p.symbol}</span>
											<span class="font-headline text-sm font-semibold text-on-surface">{p.display_name}</span>
										</div>
										{#if p.retrograde}
											<span class="px-2 py-0.5 rounded-full bg-rose-500/15 text-rose-400 border border-rose-500/30 text-[10px] font-mono font-semibold" title="Retrograde">
												℞ Retrograde
											</span>
										{/if}
									</div>

									<div class="flex items-center gap-2 mb-2 text-xs font-mono-data text-secondary">
										<span>{p.sign_display}</span>
										{#if p.degree !== undefined}
											<span class="text-on-surface-variant">({Math.floor(p.degree % 30)}° {Math.floor(((p.degree % 30) - Math.floor(p.degree % 30)) * 60)}')</span>
										{/if}
									</div>

									<p class="text-xs text-on-surface/90 leading-relaxed mb-3">
										{p.interpretation}
									</p>
								</div>

								<div class="pt-2 border-t border-white/5 flex items-center justify-between text-[11px] text-on-surface-variant font-mono-data">
									<span>{p.domain}</span>
								</div>
							</div>
						{/each}
					</div>
				</div>
			{/if}

			<!-- TAB 3: HARMONIC ASPECTS -->
			{#if activeTab === 'aspects'}
				<div class="space-y-4">
					<p class="text-xs text-on-surface-variant mb-3">
						{$locale === 'my'
							? 'ဂြိုဟ်အချင်းချင်း ချိတ်ဆက်နေသော ထောင့်များသည် သင့်မွေးရာပါ စွမ်းရည်များနှင့် အတွင်းစိတ် သင်ခန်းစာများကို ဖော်ပြသည်။'
							: 'Angular aspects reveal how planetary energies dialogue with one another—flowing harmonies provide natural gifts, while dynamic tensions fuel growth.'}
					</p>

					{#if explanation.aspects && explanation.aspects.length > 0}
						<div class="space-y-3">
							{#each explanation.aspects as asp}
								<div class="p-4 rounded-xl bg-surface-container-high/40 border border-white/5 hover:border-primary/20 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4">
									<div class="flex-1">
										<div class="flex flex-wrap items-center gap-2 mb-1.5">
											<span class="font-headline text-sm font-semibold text-on-surface">
												{$locale === 'my' ? `${asp.body1_name_my} နှင့် ${asp.body2_name_my}` : `${asp.body1_name} & ${asp.body2_name}`}
											</span>
											<span class="px-2 py-0.5 rounded-full border text-[11px] font-mono font-medium {getAspectBadgeColor(asp.type)}">
												{$locale === 'my' ? asp.aspect_my : `${asp.aspect} (${asp.angle}°)`}
											</span>
											<span class="text-[10px] text-on-surface-variant font-mono-data">
												Orb: {asp.orb}°
											</span>
										</div>
										<p class="text-xs text-on-surface/90 leading-relaxed">
											{asp.description}
										</p>
									</div>

									<div class="self-start sm:self-center shrink-0">
										<span class="text-[10px] uppercase font-mono px-2 py-1 rounded bg-surface-container-highest text-on-surface-variant">
											{getAspectTypeLabel(asp.type, $locale === 'my')}
										</span>
									</div>
								</div>
							{/each}
						</div>
					{:else}
						<p class="text-sm text-on-surface-variant italic py-6 text-center">
							{$locale === 'my' ? 'ထင်ရှားသော ထောင့်ချိတ်ဆက်မှုများ မတွေ့ရှိပါ။' : 'No major close aspects detected within 8° orbs.'}
						</p>
					{/if}
				</div>
			{/if}

			<!-- TAB 4: ELEMENTS & COSMIC GUIDANCE -->
			{#if activeTab === 'elements'}
				<div class="space-y-6">
					<!-- Elemental Distribution Bars -->
					<div class="glass-card p-6 rounded-xl border border-white/5 bg-surface-container-high/40">
						<h4 class="font-headline text-base text-on-surface font-semibold mb-4">
							{$locale === 'my' ? 'ဓာတ်ကြီး ၄ ပါး မျှတမှုအချိုးအစား (Elemental Balance)' : 'Elemental Constitution Breakdown'}
						</h4>

						<div class="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-6">
							{#each ['fire', 'earth', 'air', 'water'] as elem}
								{@const pct = explanation.elemental_constitution.percentages[elem] || 0}
								<div class="flex flex-col gap-1.5 p-3 rounded-lg bg-surface-container-highest/40 border border-white/5">
									<div class="flex items-center justify-between text-xs">
										<span class="font-mono-data capitalize" style:color={getElementColor(elem)}>
											{formatElement(elem, $locale)}
										</span>
										<span class="font-mono font-bold text-on-surface">{pct}%</span>
									</div>
									<div class="w-full h-2 rounded-full bg-surface-container-lowest overflow-hidden">
										<div
											class="h-full rounded-full transition-all duration-500"
											style:width="{pct}%"
											style:background-color={getElementColor(elem)}
										></div>
									</div>
								</div>
							{/each}
						</div>

						<p class="text-xs text-on-surface/90 leading-relaxed">
							{explanation.elemental_constitution.analysis}
						</p>
					</div>

					<!-- Cosmic Evolutionary Guidance -->
					<div class="p-6 rounded-xl bg-gradient-to-r from-purple-900/30 via-indigo-900/20 to-slate-900/40 border border-secondary/30">
						<div class="flex items-center gap-2 mb-3">
							<span class="material-symbols-outlined text-secondary text-2xl">stars</span>
							<h4 class="font-headline text-base text-on-surface font-semibold">
								{$locale === 'my' ? 'ဝိညာဉ်ရေးရာ ဘဝလမ်းညွှန်ချက် (Cosmic Guidance)' : 'Evolutionary Soul Guidance'}
							</h4>
						</div>
						<p class="text-sm text-on-surface/95 leading-relaxed italic">
							"{explanation.guidance}"
						</p>
					</div>
				</div>
			{/if}
		</div>
	{/if}
</div>
