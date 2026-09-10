<script lang="ts">
	import type { BirthChartExplanationData } from '$lib/types';
	import { locale, formatElement } from '$lib/i18n';
	import { ELEMENT_COLORS, ZODIAC_SYMBOLS } from '$lib/types';

	interface Props {
		chart: unknown;
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
				})
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
		void $locale;
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
				case 'harmonious':
					return 'သဟဇာတဖြစ် (Harmonious)';
				case 'dynamic':
					return 'စိန်ခေါ်မှု/တိုးတက်မှု (Dynamic)';
				case 'polarity':
					return 'ချိန်ခွင်လျှာ (Polarity)';
				default:
					return 'ပေါင်းစပ်မှု (Unified)';
			}
		} else {
			switch (type) {
				case 'harmonious':
					return 'Harmonious Flow';
				case 'dynamic':
					return 'Evolutionary Tension';
				case 'polarity':
					return 'Complementary Polarity';
				default:
					return 'Unified Synthesis';
			}
		}
	}
</script>

<div class="my-8 w-full">
	<!-- Trigger Section -->
	{#if !isOpen}
		<div
			class="glass-card relative flex flex-col items-center gap-4 overflow-hidden border border-primary/20 bg-gradient-to-br from-surface-container-high/80 via-surface-container/60 to-surface-container-lowest/90 p-6 text-center sm:p-8"
		>
			<div
				class="pointer-events-none absolute -top-20 -left-20 h-48 w-48 rounded-full bg-primary/10 blur-3xl"
			></div>
			<div
				class="pointer-events-none absolute -right-20 -bottom-20 h-48 w-48 rounded-full bg-secondary/10 blur-3xl"
			></div>

			<div
				class="flex h-12 w-12 items-center justify-center rounded-2xl border border-primary/30 bg-gradient-to-tr from-primary/20 via-purple-500/20 to-secondary/20 text-primary shadow-lg"
			>
				<span class="material-symbols-outlined text-2xl">psychology_alt</span>
			</div>

			<div class="max-w-xl">
				<h3 class="font-headline mb-2 text-xl font-semibold text-on-surface sm:text-2xl">
					{$locale === 'my'
						? 'မွေးဖွားမှုဇာတာ အသေးစိတ် ရှင်းလင်းချက် ရယူမည်'
						: 'Want an In-Depth Explanation of Your Birth Chart?'}
				</h3>
				<p class="text-sm leading-relaxed text-on-surface-variant">
					{$locale === 'my'
						? 'သင့်နေမင်း၊ လမင်း၊ စန်းလဂ်နှင့် ဂြိုဟ် ၁၁ လုံး၏ အတွင်းစိတ်လွှမ်းမိုးမှု၊ အဓိက ထောင့်ချိတ်ဆက်မှုများ (Aspects) နှင့် ဓာတ်သဘောမျှတမှုကို အသေးစိတ် ဖတ်ရှုလေ့လာပါ။'
						: 'Unpack the psychological blueprint of your Big Three, 11 celestial archetypes, major angular aspects, and elemental constitution with comprehensive cosmic analysis.'}
				</p>
			</div>

			{#if error}
				<p class="flex items-center gap-1.5 text-xs text-error">
					<span class="material-symbols-outlined text-sm">error</span>
					{error}
				</p>
			{/if}

			<button
				type="button"
				onclick={fetchExplanation}
				disabled={loading}
				class="font-headline mt-2 inline-flex cursor-pointer items-center gap-3 rounded-full bg-gradient-to-r from-primary via-purple-600 to-secondary px-8 py-3.5 text-sm font-semibold text-on-primary shadow-lg shadow-primary/25 transition-all hover:scale-[1.02] hover:shadow-primary/40 active:scale-[0.98] disabled:opacity-60"
			>
				<span class="material-symbols-outlined text-lg {loading ? 'animate-spin' : ''}">
					{loading ? 'progress_activity' : 'auto_awesome'}
				</span>
				<span>
					{loading
						? $locale === 'my'
							? 'ရှင်းလင်းချက် ပြုစုနေပါသည်...'
							: 'Analyzing Birth Chart...'
						: $locale === 'my'
							? '✨ မွေးဖွားမှုဇာတာ အပြည့်အစုံ ရှင်းလင်းချက် ဖတ်မည်'
							: '✨ Explain My Birth Chart'}
				</span>
			</button>
		</div>
	{:else if explanation}
		<!-- Main Deep-Dive Explanation Panel -->
		<div
			class="glass-card relative overflow-hidden rounded-2xl border border-primary/30 bg-surface-container-lowest/90 p-6 shadow-2xl backdrop-blur-xl lg:p-8"
		>
			<!-- Header with Close & Toggle -->
			<div
				class="flex flex-col justify-between gap-4 border-b border-surface-container-highest pb-6 sm:flex-row sm:items-center"
			>
				<div>
					<div class="mb-1 flex items-center gap-2">
						<span class="h-2 w-2 animate-ping rounded-full bg-secondary"></span>
						<span class="font-mono-data text-xs tracking-widest text-secondary uppercase">
							{$locale === 'my'
								? 'ဇာတာရှင်၏ စိတ်ပညာနှင့် နက္ခတ်ဗေဒ အနုစိတ်ဆန်းစစ်ချက်'
								: 'Cosmic Blueprint & Psychological Profile'}
						</span>
					</div>
					<h2 class="font-headline text-2xl font-bold text-on-surface sm:text-3xl">
						{explanation.archetype_title}
					</h2>
				</div>

				<div class="flex items-center gap-2 self-end sm:self-auto">
					<button
						type="button"
						onclick={() => (isOpen = false)}
						class="flex items-center gap-1.5 rounded-lg bg-surface-container-highest px-3.5 py-1.5 text-xs font-medium text-on-surface-variant transition-colors hover:bg-surface-bright hover:text-on-surface"
					>
						<span class="material-symbols-outlined text-sm">close</span>
						<span>{$locale === 'my' ? 'ပိတ်မည်' : 'Collapse'}</span>
					</button>
				</div>
			</div>

			<!-- Navigation Tabs -->
			<div
				class="my-6 flex flex-wrap gap-2 rounded-xl border border-white/5 bg-surface-container-highest/60 p-1.5"
			>
				<button
					type="button"
					onclick={() => (activeTab = 'triad')}
					class="font-headline flex min-w-[130px] flex-1 items-center justify-center gap-2 rounded-lg px-3 py-2.5 text-xs font-semibold transition-all {activeTab ===
					'triad'
						? 'bg-primary text-on-primary shadow-md'
						: 'text-on-surface-variant hover:bg-surface-bright/40 hover:text-on-surface'}"
				>
					<span class="material-symbols-outlined text-base">diversity_3</span>
					<span>{$locale === 'my' ? 'အဓိကမဏ္ဍိုင် ၃ မျိုး' : 'The Big Three'}</span>
				</button>

				<button
					type="button"
					onclick={() => (activeTab = 'planets')}
					class="font-headline flex min-w-[130px] flex-1 items-center justify-center gap-2 rounded-lg px-3 py-2.5 text-xs font-semibold transition-all {activeTab ===
					'planets'
						? 'bg-primary text-on-primary shadow-md'
						: 'text-on-surface-variant hover:bg-surface-bright/40 hover:text-on-surface'}"
				>
					<span class="material-symbols-outlined text-base">scatter_plot</span>
					<span>{$locale === 'my' ? 'ဂြိုဟ် ၁၁ လုံး အနေအထား' : 'Planetary Dimensions'}</span>
				</button>

				<button
					type="button"
					onclick={() => (activeTab = 'aspects')}
					class="font-headline flex min-w-[130px] flex-1 items-center justify-center gap-2 rounded-lg px-3 py-2.5 text-xs font-semibold transition-all {activeTab ===
					'aspects'
						? 'bg-primary text-on-primary shadow-md'
						: 'text-on-surface-variant hover:bg-surface-bright/40 hover:text-on-surface'}"
				>
					<span class="material-symbols-outlined text-base">hub</span>
					<span>{$locale === 'my' ? 'ထောင့်ချိတ်ဆက်မှုများ' : 'Harmonic Aspects'}</span>
					{#if explanation.aspects?.length}
						<span class="rounded-full bg-white/20 px-1.5 py-0.5 text-[10px]"
							>{explanation.aspects.length}</span
						>
					{/if}
				</button>

				<button
					type="button"
					onclick={() => (activeTab = 'elements')}
					class="font-headline flex min-w-[130px] flex-1 items-center justify-center gap-2 rounded-lg px-3 py-2.5 text-xs font-semibold transition-all {activeTab ===
					'elements'
						? 'bg-primary text-on-primary shadow-md'
						: 'text-on-surface-variant hover:bg-surface-bright/40 hover:text-on-surface'}"
				>
					<span class="material-symbols-outlined text-base">water_drop</span>
					<span>{$locale === 'my' ? 'ဓာတ်သဘောနှင့် လမ်းညွှန်ချက်' : 'Elements & Guidance'}</span>
				</button>
			</div>

			<!-- TAB 1: THE BIG THREE (CORE IDENTITY) -->
			{#if activeTab === 'triad'}
				<div class="space-y-6">
					<div class="grid grid-cols-1 gap-5 md:grid-cols-3">
						<!-- Sun Sign Deep Dive -->
						<div
							class="glass-card flex flex-col justify-between rounded-xl border border-primary/20 bg-surface-container-high/40 p-5"
						>
							<div>
								<div class="mb-3 flex items-center justify-between">
									<span
										class="font-mono-data flex items-center gap-1.5 text-[11px] font-bold tracking-wider text-primary uppercase"
									>
										<span class="text-base">☉</span>
										{explanation.core_identity.sun.name}
									</span>
									<span class="font-serif text-2xl text-primary">
										{ZODIAC_SYMBOLS[explanation.core_identity.sun.sign] || '☉'}
									</span>
								</div>
								<h4 class="font-headline mb-2 text-lg font-bold text-on-surface">
									{explanation.core_identity.sun.sign_display}
								</h4>
								<p class="mb-4 text-xs leading-relaxed text-on-surface/90">
									{explanation.core_identity.sun.essence}
								</p>
							</div>

							<div>
								<div class="mb-3">
									<div class="font-mono-data mb-1.5 text-[11px] text-on-surface-variant uppercase">
										{$locale === 'my' ? 'အဓိက အားသာချက်များ' : 'Key Strengths'}
									</div>
									<div class="flex flex-wrap gap-1.5">
										{#each explanation.core_identity.sun.strengths as strength (strength)}
											<span
												class="rounded-md border border-primary/20 bg-primary/10 px-2 py-0.5 text-[11px] text-primary"
											>
												{strength}
											</span>
										{/each}
									</div>
								</div>
								<div class="border-t border-white/5 pt-3">
									<div class="font-mono-data mb-1 text-[11px] text-secondary uppercase">
										{$locale === 'my' ? 'ဘဝသင်ခန်းစာ' : 'Growth Lesson'}
									</div>
									<p class="text-xs leading-relaxed text-on-surface-variant">
										{explanation.core_identity.sun.growth_lesson}
									</p>
								</div>
							</div>
						</div>

						<!-- Moon Sign Deep Dive -->
						<div
							class="glass-card flex flex-col justify-between rounded-xl border border-secondary/20 bg-surface-container-high/40 p-5"
						>
							<div>
								<div class="mb-3 flex items-center justify-between">
									<span
										class="font-mono-data flex items-center gap-1.5 text-[11px] font-bold tracking-wider text-secondary uppercase"
									>
										<span class="text-base">☽</span>
										{explanation.core_identity.moon.name}
									</span>
									<span class="font-serif text-2xl text-secondary">
										{ZODIAC_SYMBOLS[explanation.core_identity.moon.sign] || '☽'}
									</span>
								</div>
								<h4 class="font-headline mb-2 text-lg font-bold text-on-surface">
									{explanation.core_identity.moon.sign_display}
								</h4>
								<p class="mb-4 text-xs leading-relaxed text-on-surface/90">
									{explanation.core_identity.moon.essence}
								</p>
							</div>

							<div class="border-t border-white/5 pt-3">
								<div class="font-mono-data mb-1 text-[11px] text-secondary uppercase">
									{$locale === 'my' ? 'အတွင်းစိတ် လုံခြုံမှု လိုအပ်ချက်' : 'Subconscious Core Need'}
								</div>
								<p class="text-xs leading-relaxed text-on-surface-variant">
									{explanation.core_identity.moon.need}
								</p>
							</div>
						</div>

						<!-- Rising Sign Deep Dive -->
						<div
							class="glass-card flex flex-col justify-between rounded-xl border border-tertiary/20 bg-surface-container-high/40 p-5"
						>
							<div>
								<div class="mb-3 flex items-center justify-between">
									<span
										class="font-mono-data flex items-center gap-1.5 text-[11px] font-bold tracking-wider text-tertiary uppercase"
									>
										<span class="text-base">AC</span>
										{explanation.core_identity.rising.name}
									</span>
									<span class="font-serif text-2xl text-tertiary">
										{ZODIAC_SYMBOLS[explanation.core_identity.rising.sign] || 'AC'}
									</span>
								</div>
								<h4 class="font-headline mb-2 text-lg font-bold text-on-surface">
									{explanation.core_identity.rising.sign_display}
								</h4>
								<p class="mb-4 text-xs leading-relaxed text-on-surface/90">
									{explanation.core_identity.rising.essence}
								</p>
							</div>

							<div class="border-t border-white/5 pt-3">
								<div class="font-mono-data mb-1 text-[11px] text-tertiary uppercase">
									{$locale === 'my' ? 'ပထမဆုံးတွေ့ဆုံမှု အရှိန်အဝါ' : 'First Impression & Vibe'}
								</div>
								<p class="text-xs leading-relaxed text-on-surface-variant">
									{explanation.core_identity.rising.vibe}
								</p>
							</div>
						</div>
					</div>

					<!-- Triad Synthesis Narrative Box -->
					<div
						class="rounded-xl border border-primary/20 bg-gradient-to-r from-primary/10 via-purple-500/10 to-secondary/10 p-6"
					>
						<div class="mb-3 flex items-center gap-2">
							<span class="material-symbols-outlined text-xl text-primary">merge</span>
							<h4 class="font-headline text-base font-semibold text-on-surface">
								{$locale === 'my'
									? 'စွမ်းအင် ၃ ခု ပေါင်းစပ်လှုပ်ရှားမှု (Triad Alchemy)'
									: 'Triad Dynamic Synthesis'}
							</h4>
						</div>
						<p class="text-sm leading-relaxed text-on-surface/95">
							{explanation.core_identity.triad_synthesis}
						</p>
					</div>
				</div>
			{/if}

			<!-- TAB 2: PLANETARY DIMENSIONS -->
			{#if activeTab === 'planets'}
				<div class="space-y-4">
					<p class="mb-3 text-xs text-on-surface-variant">
						{$locale === 'my'
							? 'ဂြိုဟ်တစ်ခုစီသည် သင့်စိတ်နှင့် ဘဝ၏ သီးခြားကဏ္ဍတစ်ခုစီကို ကိုယ်စားပြုသည်။ အောက်ပါဇယားတွင် ဂြိုဟ် ၁၁ လုံး၏ အနေအထားနှင့် လွှမ်းမိုးမှုများကို လေ့လာပါ။'
							: 'Each celestial body governs a distinct cognitive and life dimension. Here is the complete evolutionary profile of your 11 planetary placements.'}
					</p>

					<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
						{#each explanation.planetary_breakdown as p (p.display_name)}
							<div
								class="glass-card flex flex-col justify-between rounded-xl border border-white/5 p-4 transition-all hover:border-primary/30"
							>
								<div>
									<div class="mb-2 flex items-center justify-between">
										<div class="flex items-center gap-2">
											<span class="font-serif text-lg text-primary">{p.symbol}</span>
											<span class="font-headline text-sm font-semibold text-on-surface"
												>{p.display_name}</span
											>
										</div>
										{#if p.retrograde}
											<span
												class="rounded-full border border-rose-500/30 bg-rose-500/15 px-2 py-0.5 font-mono text-[10px] font-semibold text-rose-400"
												title="Retrograde"
											>
												℞ Retrograde
											</span>
										{/if}
									</div>

									<div class="font-mono-data mb-2 flex items-center gap-2 text-xs text-secondary">
										<span>{p.sign_display}</span>
										{#if p.degree !== undefined}
											<span class="text-on-surface-variant"
												>({Math.floor(p.degree % 30)}° {Math.floor(
													((p.degree % 30) - Math.floor(p.degree % 30)) * 60
												)}')</span
											>
										{/if}
									</div>

									<p class="mb-3 text-xs leading-relaxed text-on-surface/90">
										{p.interpretation}
									</p>
								</div>

								<div
									class="font-mono-data flex items-center justify-between border-t border-white/5 pt-2 text-[11px] text-on-surface-variant"
								>
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
					<p class="mb-3 text-xs text-on-surface-variant">
						{$locale === 'my'
							? 'ဂြိုဟ်အချင်းချင်း ချိတ်ဆက်နေသော ထောင့်များသည် သင့်မွေးရာပါ စွမ်းရည်များနှင့် အတွင်းစိတ် သင်ခန်းစာများကို ဖော်ပြသည်။'
							: 'Angular aspects reveal how planetary energies dialogue with one another—flowing harmonies provide natural gifts, while dynamic tensions fuel growth.'}
					</p>

					{#if explanation.aspects && explanation.aspects.length > 0}
						<div class="space-y-3">
							{#each explanation.aspects as asp (asp.body1_name + asp.body2_name + asp.type)}
								<div
									class="flex flex-col justify-between gap-4 rounded-xl border border-white/5 bg-surface-container-high/40 p-4 transition-all hover:border-primary/20 sm:flex-row sm:items-center"
								>
									<div class="flex-1">
										<div class="mb-1.5 flex flex-wrap items-center gap-2">
											<span class="font-headline text-sm font-semibold text-on-surface">
												{$locale === 'my'
													? `${asp.body1_name_my} နှင့် ${asp.body2_name_my}`
													: `${asp.body1_name} & ${asp.body2_name}`}
											</span>
											<span
												class="rounded-full border px-2 py-0.5 font-mono text-[11px] font-medium {getAspectBadgeColor(
													asp.type
												)}"
											>
												{$locale === 'my' ? asp.aspect_my : `${asp.aspect} (${asp.angle}°)`}
											</span>
											<span class="font-mono-data text-[10px] text-on-surface-variant">
												Orb: {asp.orb}°
											</span>
										</div>
										<p class="text-xs leading-relaxed text-on-surface/90">
											{asp.description}
										</p>
									</div>

									<div class="shrink-0 self-start sm:self-center">
										<span
											class="rounded bg-surface-container-highest px-2 py-1 font-mono text-[10px] text-on-surface-variant uppercase"
										>
											{getAspectTypeLabel(asp.type, $locale === 'my')}
										</span>
									</div>
								</div>
							{/each}
						</div>
					{:else}
						<p class="py-6 text-center text-sm text-on-surface-variant italic">
							{$locale === 'my'
								? 'ထင်ရှားသော ထောင့်ချိတ်ဆက်မှုများ မတွေ့ရှိပါ။'
								: 'No major close aspects detected within 8° orbs.'}
						</p>
					{/if}
				</div>
			{/if}

			<!-- TAB 4: ELEMENTS & COSMIC GUIDANCE -->
			{#if activeTab === 'elements'}
				<div class="space-y-6">
					<!-- Elemental Distribution Bars -->
					<div class="glass-card rounded-xl border border-white/5 bg-surface-container-high/40 p-6">
						<h4 class="font-headline mb-4 text-base font-semibold text-on-surface">
							{$locale === 'my'
								? 'ဓာတ်ကြီး ၄ ပါး မျှတမှုအချိုးအစား (Elemental Balance)'
								: 'Elemental Constitution Breakdown'}
						</h4>

						<div class="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-4">
							{#each ['fire', 'earth', 'air', 'water'] as elem (elem)}
								{@const pct = explanation.elemental_constitution.percentages[elem] || 0}
								<div
									class="flex flex-col gap-1.5 rounded-lg border border-white/5 bg-surface-container-highest/40 p-3"
								>
									<div class="flex items-center justify-between text-xs">
										<span class="font-mono-data capitalize" style:color={getElementColor(elem)}>
											{formatElement(elem, $locale)}
										</span>
										<span class="font-mono font-bold text-on-surface">{pct}%</span>
									</div>
									<div class="h-2 w-full overflow-hidden rounded-full bg-surface-container-lowest">
										<div
											class="h-full rounded-full transition-all duration-500"
											style:width="{pct}%"
											style:background-color={getElementColor(elem)}
										></div>
									</div>
								</div>
							{/each}
						</div>

						<p class="text-xs leading-relaxed text-on-surface/90">
							{explanation.elemental_constitution.analysis}
						</p>
					</div>

					<!-- Cosmic Evolutionary Guidance -->
					<div
						class="rounded-xl border border-secondary/30 bg-gradient-to-r from-purple-900/30 via-indigo-900/20 to-slate-900/40 p-6"
					>
						<div class="mb-3 flex items-center gap-2">
							<span class="material-symbols-outlined text-2xl text-secondary">stars</span>
							<h4 class="font-headline text-base font-semibold text-on-surface">
								{$locale === 'my'
									? 'ဝိညာဉ်ရေးရာ ဘဝလမ်းညွှန်ချက် (Cosmic Guidance)'
									: 'Evolutionary Soul Guidance'}
							</h4>
						</div>
						<p class="text-sm leading-relaxed text-on-surface/95 italic">
							"{explanation.guidance}"
						</p>
					</div>
				</div>
			{/if}
		</div>
	{/if}
</div>
