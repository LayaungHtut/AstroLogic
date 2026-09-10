<script lang="ts">
	import { ZODIAC_SYMBOLS } from '$lib/types';
	import { locale, t, getZodiacTranslation, formatElement } from '$lib/i18n';

	const features = $derived([
		{
			icon: 'auto_awesome',
			eyebrow: $locale === 'my' ? 'ဉာဏ်ရည်တု ပေါင်းစပ်မှု' : 'Neural Synthesis',
			title: $t('feat.readings.title'),
			desc: $t('feat.readings.desc'),
			meta: $t('feat.readings.meta'),
			cta: $t('feat.readings.cta'),
			href: '/reading',
			accent: 'text-primary bg-primary-container/20'
		},
		{
			icon: 'account_tree',
			eyebrow: $locale === 'my' ? 'ယုတ္တိဗေဒ သက်သေပြချက်' : 'Formal Verification',
			title: $t('feat.prolog.title'),
			desc: $t('feat.prolog.desc'),
			meta: $t('feat.prolog.meta'),
			cta: $t('feat.prolog.cta'),
			href: '/chat',
			accent: 'text-secondary bg-secondary-container/20'
		},
		{
			icon: 'public',
			eyebrow: $locale === 'my' ? 'နက္ခတ်တွက်ချက်မှု တိကျခြင်း' : 'Ephemeris Precision',
			title: $t('feat.chart.title'),
			desc: $t('feat.chart.desc'),
			meta: $t('feat.chart.meta'),
			cta: $t('feat.chart.cta'),
			href: '/birth-chart',
			accent: 'text-tertiary bg-tertiary-container/20'
		},
		{
			icon: 'join_inner',
			eyebrow: $locale === 'my' ? 'ရာသီခွင် ပေါင်းစပ်မှု' : 'Synastry Modeling',
			title: $t('feat.synastry.title'),
			desc: $t('feat.synastry.desc'),
			meta: $t('feat.synastry.meta'),
			cta: $t('feat.synastry.cta'),
			href: '/compatibility',
			accent: 'text-secondary bg-surface-container-high'
		},
		{
			icon: 'document_scanner',
			eyebrow: $locale === 'my' ? 'ကင်မရာပုံရိပ် ခွဲခြမ်းမှု' : 'Vision Telemetry',
			title: $t('feat.scan.title'),
			desc: $t('feat.scan.desc'),
			meta: $t('feat.scan.meta'),
			cta: $t('feat.scan.cta'),
			href: '/scan',
			accent: 'text-primary bg-surface-container-high'
		},
		{
			icon: 'psychology_alt',
			eyebrow: $locale === 'my' ? 'ဆိုကရေးတီးဆန်သော AI လမ်းပြ' : 'Socratic Tutor',
			title: $t('feat.guide.title'),
			desc: $t('feat.guide.desc'),
			meta: $t('feat.guide.meta'),
			cta: $t('feat.guide.cta'),
			href: '/chat',
			accent: 'text-tertiary bg-primary-container/20'
		}
	]);

	const steps = $derived([
		{
			num: 1,
			icon: 'psychology',
			eyebrow: $locale === 'my' ? 'ပထမအဆင့်' : 'Phase Alpha',
			title: $t('landing.step1Title'),
			desc: $t('landing.step1Desc'),
			tag: $t('landing.step1Tag')
		},
		{
			num: 2,
			icon: 'memory',
			eyebrow: $locale === 'my' ? 'ဒုတိယအဆင့်' : 'Phase Beta',
			title: $t('landing.step2Title'),
			desc: $t('landing.step2Desc'),
			tag: $t('landing.step2Tag')
		},
		{
			num: 3,
			icon: 'auto_stories',
			eyebrow: $locale === 'my' ? 'တတိယအဆင့်' : 'Phase Gamma',
			title: $t('landing.step3Title'),
			desc: $t('landing.step3Desc'),
			tag: $t('landing.step3Tag')
		},
		{
			num: 4,
			icon: 'checklist_rtl',
			eyebrow: $locale === 'my' ? 'စတုတ္ထအဆင့်' : 'Phase Delta',
			title: $t('landing.step4Title'),
			desc: $t('landing.step4Desc'),
			tag: $t('landing.step4Tag')
		}
	]);

	const elementInfo: Record<string, { color: string; degrees: string }> = {
		aries: { color: 'text-fire', degrees: '0°-30°' },
		taurus: { color: 'text-earth', degrees: '30°-60°' },
		gemini: { color: 'text-air', degrees: '60°-90°' },
		cancer: { color: 'text-water', degrees: '90°-120°' },
		leo: { color: 'text-fire', degrees: '120°-150°' },
		virgo: { color: 'text-earth', degrees: '150°-180°' },
		libra: { color: 'text-air', degrees: '180°-210°' },
		scorpio: { color: 'text-water', degrees: '210°-240°' },
		sagittarius: { color: 'text-fire', degrees: '240°-270°' },
		capricorn: { color: 'text-earth', degrees: '270°-300°' },
		aquarius: { color: 'text-air', degrees: '300°-330°' },
		pisces: { color: 'text-water', degrees: '330°-360°' }
	};

	const signs = Object.entries(ZODIAC_SYMBOLS);
</script>

<svelte:head>
	<title>{$t('brand.name')} - {$t('brand.tagline')}</title>
</svelte:head>

<div class="w-full pt-24 pb-20">
	<div class="mx-auto flex max-w-7xl flex-col px-6 lg:px-12">
		<!-- Hero -->
		<section
			class="relative mb-16 w-full overflow-hidden rounded-3xl bg-surface-container-lowest/70 p-8 shadow-2xl backdrop-blur-2xl lg:p-16"
		>
			<div
				class="pointer-events-none absolute -top-32 -left-32 h-96 w-96 rounded-full bg-primary-container/20 blur-3xl"
			></div>
			<div
				class="pointer-events-none absolute -right-32 -bottom-32 h-96 w-96 rounded-full bg-secondary-container/20 blur-3xl"
			></div>
			<div
				class="pointer-events-none absolute top-1/2 left-1/2 h-64 w-3/4 -translate-x-1/2 -translate-y-1/2 bg-tertiary-container/10 blur-3xl"
			></div>

			<div class="relative z-10 mx-auto flex max-w-4xl flex-col items-center text-center">
				<div
					class="mb-8 inline-flex items-center gap-3 rounded-full bg-surface-container-high/90 px-4 py-1.5 shadow-md"
				>
					<span
						class="font-mono-data inline-flex items-center gap-1.5 text-[10px] font-semibold tracking-wider text-secondary uppercase"
					>
						<span class="h-2 w-2 animate-ping rounded-full bg-secondary"></span>
						{$t('landing.engineOnline')}
					</span>
					<span class="h-1 w-1 rounded-full bg-outline-variant"></span>
					<span class="font-mono-data text-xs text-on-surface-variant"
						>{$t('landing.logicCoreSync')}</span
					>
				</div>

				<h1
					class="font-headline mb-6 bg-gradient-to-b from-white via-primary to-secondary bg-clip-text text-3xl font-semibold tracking-tight text-transparent drop-shadow-[0_0_35px_rgba(210,187,255,0.4)] md:text-5xl lg:text-[56px] lg:leading-[68px]"
				>
					{$t('landing.heroTitle')}
				</h1>
				<p
					class="mx-auto mb-4 max-w-2xl text-base leading-relaxed text-on-surface-variant md:text-lg"
				>
					{$t('landing.heroSubtitle')}
				</p>
				<p class="mx-auto mb-10 max-w-xl text-sm text-on-surface-variant/70">
					{$t('landing.entertainmentNotice')}
				</p>

				<div class="mb-12 flex flex-wrap items-center justify-center gap-4">
					<a
						href="/reading"
						class="group font-headline inline-flex items-center gap-3 rounded-full bg-gradient-to-r from-primary-container to-secondary-container px-8 py-4 text-base font-semibold text-white shadow-[0_0_28px_rgba(124,58,237,0.4)] transition-all duration-300 hover:scale-105 hover:shadow-[0_0_40px_rgba(76,215,246,0.6)]"
					>
						<span
							class="material-symbols-outlined text-xl transition-transform group-hover:rotate-45"
							>auto_awesome</span
						>
						<span>{$t('landing.startReading')}</span>
					</a>
					<a
						href="/dashboard"
						class="font-headline inline-flex items-center gap-3 rounded-full bg-surface-container-high/60 px-8 py-4 text-base font-semibold text-on-surface shadow-lg backdrop-blur-md transition-all duration-300 hover:scale-105 hover:bg-surface-container-high hover:shadow-xl"
					>
						<span class="material-symbols-outlined text-xl text-secondary">orbit</span>
						<span>{$t('landing.exploreDashboard')}</span>
					</a>
				</div>

				<div
					class="grid w-full max-w-3xl grid-cols-1 gap-3 rounded-2xl bg-surface-container-high/40 p-4 shadow-inner backdrop-blur-md md:grid-cols-3"
				>
					<div class="flex flex-col items-center justify-center px-4 py-2">
						<div class="font-headline flex items-center gap-1.5 text-xl font-medium text-primary">
							<span>78</span>
							<span class="text-xs text-secondary">/ 78</span>
						</div>
						<span
							class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase"
							>{$t('landing.statArcanaMapped')}</span
						>
					</div>
					<div class="flex flex-col items-center justify-center px-4 py-2">
						<div class="font-headline text-xl font-medium text-secondary">12 Signs</div>
						<span
							class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase"
							>{$t('landing.statZodiacCovered')}</span
						>
					</div>
					<div class="flex flex-col items-center justify-center px-4 py-2">
						<div class="font-headline flex items-center gap-2 text-xl font-medium text-tertiary">
							<span class="h-2 w-2 rounded-full bg-secondary shadow-[0_0_8px_#4cd7f6]"></span>
							<span>{$t('landing.statDeterministic')}</span>
						</div>
						<span
							class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase"
							>{$t('landing.statPrologEngine')}</span
						>
					</div>
				</div>
			</div>
		</section>

		<!-- Zodiac Wheel -->
		<section class="mb-20 w-full">
			<div class="mx-auto mb-10 flex max-w-2xl flex-col items-center text-center">
				<div
					class="font-mono-data mb-2 inline-flex items-center gap-2 text-[10px] font-semibold tracking-widest text-primary uppercase"
				>
					<span class="material-symbols-outlined text-sm">cyclone</span>
					{$t('landing.celestialWheel')}
				</div>
				<h2 class="font-headline mb-3 text-2xl font-medium text-on-surface md:text-3xl">
					{$t('landing.twelveModalities')}
				</h2>
				<p class="text-sm text-on-surface-variant md:text-base">
					{$t('landing.wheelDesc')}
				</p>
				<div class="mt-6 flex flex-wrap items-center justify-center gap-3">
					<div
						class="font-mono-data inline-flex items-center gap-1.5 rounded-full bg-surface-container-high px-3 py-1 text-[10px] font-semibold tracking-wider text-fire uppercase shadow-sm"
					>
						<span class="h-2 w-2 rounded-full bg-fire"></span>
						{formatElement('fire', $locale)}
					</div>
					<div
						class="font-mono-data inline-flex items-center gap-1.5 rounded-full bg-surface-container-high px-3 py-1 text-[10px] font-semibold tracking-wider text-earth uppercase shadow-sm"
					>
						<span class="h-2 w-2 rounded-full bg-earth"></span>
						{formatElement('earth', $locale)}
					</div>
					<div
						class="font-mono-data inline-flex items-center gap-1.5 rounded-full bg-surface-container-high px-3 py-1 text-[10px] font-semibold tracking-wider text-air uppercase shadow-sm"
					>
						<span class="h-2 w-2 rounded-full bg-air"></span>
						{formatElement('air', $locale)}
					</div>
					<div
						class="font-mono-data inline-flex items-center gap-1.5 rounded-full bg-surface-container-high px-3 py-1 text-[10px] font-semibold tracking-wider text-water uppercase shadow-sm"
					>
						<span class="h-2 w-2 rounded-full bg-water"></span>
						{formatElement('water', $locale)}
					</div>
				</div>
			</div>

			<div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
				{#each signs as [sign, symbol]}
					{@const info = elementInfo[sign]}
					{@const zData = getZodiacTranslation(sign, $locale)}
					<a
						href="/zodiac?sign={sign}"
						class="group relative flex flex-col items-center rounded-2xl bg-surface-container/70 p-5 text-center shadow-lg backdrop-blur-md transition-all duration-300 hover:-translate-y-1"
					>
						<div
							class="mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-surface-container-high shadow-inner transition-transform group-hover:scale-110"
						>
							<span class="text-2xl {info.color}">{symbol}</span>
						</div>
						<span
							class="font-headline mb-1 max-w-full truncate text-sm font-semibold text-on-surface"
							>{zData.name}</span
						>
						<span
							class="{info.color} font-mono-data text-[10px] font-semibold tracking-wider uppercase"
							>{zData.element} • {zData.modality}</span
						>
						<span class="font-mono-data mt-2 text-[11px] text-on-surface-variant"
							>{zData.ruler} • {info.degrees}</span
						>
					</a>
				{/each}
			</div>
		</section>

		<!-- Features -->
		<section class="mb-20 w-full">
			<div class="mb-12 flex max-w-2xl flex-col items-start">
				<div
					class="font-mono-data mb-2 inline-flex items-center gap-2 text-[10px] font-semibold tracking-widest text-secondary uppercase"
				>
					<span class="material-symbols-outlined text-sm">science</span>
					{$t('landing.coreCapabilities')}
				</div>
				<h2 class="font-headline mb-3 text-2xl font-medium text-on-surface md:text-3xl">
					{$t('landing.highOrderInstruments')}
				</h2>
				<p class="text-sm text-on-surface-variant md:text-base">
					{$t('landing.capabilitiesDesc')}
				</p>
			</div>

			<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
				{#each features as feature}
					<div
						class="group relative flex flex-col justify-between rounded-2xl bg-surface-container/70 p-8 shadow-xl backdrop-blur-xl transition-all duration-300 hover:-translate-y-1"
					>
						<div>
							<div
								class="h-12 w-12 rounded-xl {feature.accent} mb-6 flex items-center justify-center shadow-md transition-transform group-hover:scale-110"
							>
								<span class="material-symbols-outlined text-2xl">{feature.icon}</span>
							</div>
							<span
								class="font-mono-data text-[10px] font-semibold tracking-widest text-secondary uppercase"
								>{feature.eyebrow}</span
							>
							<h3 class="font-headline mt-1 mb-3 text-lg font-medium text-on-surface">
								{feature.title}
							</h3>
							<p class="text-sm leading-relaxed text-on-surface-variant">{feature.desc}</p>
						</div>
						<div
							class="font-mono-data mt-6 flex items-center justify-between pt-4 text-[11px] text-on-surface-variant"
						>
							<span>{feature.meta}</span>
							<a
								href={feature.href}
								class="flex items-center gap-1 font-medium text-secondary transition-colors hover:text-white"
							>
								{feature.cta} <span class="material-symbols-outlined text-sm">arrow_forward</span>
							</a>
						</div>
					</div>
				{/each}
			</div>
		</section>

		<!-- How It Works -->
		<section class="mb-20 w-full">
			<div class="mx-auto mb-14 flex max-w-2xl flex-col items-center text-center">
				<div
					class="font-mono-data mb-2 inline-flex items-center gap-2 text-[10px] font-semibold tracking-widest text-primary uppercase"
				>
					<span class="material-symbols-outlined text-sm">route</span>
					{$t('landing.divinationProtocol')}
				</div>
				<h2 class="font-headline mb-3 text-2xl font-medium text-on-surface md:text-3xl">
					{$t('landing.howItWorks')}
				</h2>
				<p class="text-sm text-on-surface-variant md:text-base">
					{$t('landing.howItWorksDesc')}
				</p>
			</div>

			<div class="grid grid-cols-1 gap-4 md:grid-cols-4">
				{#each steps as step}
					<div
						class="relative flex flex-col justify-between rounded-2xl bg-surface-container/70 p-6 shadow-lg backdrop-blur-xl"
					>
						<div>
							<div class="mb-4 flex items-center justify-between">
								<span
									class="font-headline flex h-8 w-8 items-center justify-center rounded-full bg-primary-container text-sm font-semibold text-white shadow-md"
									>{step.num}</span
								>
								<span class="material-symbols-outlined text-xl text-secondary">{step.icon}</span>
							</div>
							<span
								class="font-mono-data text-[10px] font-semibold tracking-widest text-primary uppercase"
								>{step.eyebrow}</span
							>
							<h4 class="font-headline mt-1 mb-2 text-base font-semibold text-on-surface">
								{step.title}
							</h4>
							<p class="text-sm leading-relaxed text-on-surface-variant">{step.desc}</p>
						</div>
						<div
							class="font-mono-data mt-6 flex items-center gap-2 pt-3 text-[11px] text-secondary"
						>
							<span class="material-symbols-outlined text-sm">keyboard_double_arrow_right</span>
							<span>{step.tag}</span>
						</div>
					</div>
				{/each}
			</div>
		</section>

		<!-- Closing CTA -->
		<section
			class="relative w-full overflow-hidden rounded-3xl bg-gradient-to-r from-surface-container-high via-surface-container-low to-surface-container-lowest p-8 shadow-2xl lg:p-14"
		>
			<div
				class="pointer-events-none absolute top-0 right-0 h-80 w-80 rounded-full bg-secondary-container/10 blur-3xl"
			></div>
			<div
				class="pointer-events-none absolute bottom-0 left-10 h-72 w-72 rounded-full bg-primary-container/15 blur-3xl"
			></div>

			<div class="relative z-10 flex flex-col items-center justify-between gap-8 lg:flex-row">
				<div class="max-w-xl text-center lg:text-left">
					<span
						class="font-mono-data mb-4 inline-block rounded-full bg-surface-container-highest px-3 py-1 text-[10px] font-semibold tracking-wider text-secondary uppercase"
					>
						{$t('landing.ctaTag')}
					</span>
					<h2 class="font-headline mb-3 text-2xl font-medium text-on-surface md:text-3xl">
						{$t('landing.ctaTitle')}
					</h2>
					<p class="text-sm leading-relaxed text-on-surface-variant md:text-base">
						{$t('landing.ctaDesc')}
					</p>
				</div>
				<div class="flex shrink-0 flex-col items-center gap-4 sm:flex-row">
					<a
						href="/reading"
						class="font-headline w-full rounded-full bg-gradient-to-r from-primary-container to-secondary-container px-8 py-4 text-center text-base font-semibold text-white shadow-[0_0_24px_rgba(124,58,237,0.4)] transition-all duration-300 hover:scale-105 hover:shadow-[0_0_35px_rgba(76,215,246,0.6)] sm:w-auto"
					>
						{$t('landing.ctaDraw')}
					</a>
					<a
						href="/birth-chart"
						class="font-headline w-full rounded-full bg-surface-container px-8 py-4 text-center text-base font-semibold text-on-surface shadow-md backdrop-blur-md transition-all duration-300 hover:scale-105 hover:bg-surface-container-high sm:w-auto"
					>
						{$t('landing.ctaChart')}
					</a>
				</div>
			</div>
		</section>
	</div>
</div>
