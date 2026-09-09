<script lang="ts">
	import { ZODIAC_SYMBOLS } from '$lib/types';
	import { locale, t, getZodiacTranslation, formatElement, formatModality } from '$lib/i18n';

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
	<div class="max-w-7xl mx-auto px-6 lg:px-12 flex flex-col">
		<!-- Hero -->
		<section class="relative w-full overflow-hidden rounded-3xl bg-surface-container-lowest/70 backdrop-blur-2xl p-8 lg:p-16 mb-16 shadow-2xl">
			<div class="absolute -top-32 -left-32 w-96 h-96 rounded-full bg-primary-container/20 blur-3xl pointer-events-none"></div>
			<div class="absolute -bottom-32 -right-32 w-96 h-96 rounded-full bg-secondary-container/20 blur-3xl pointer-events-none"></div>
			<div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-3/4 h-64 bg-tertiary-container/10 blur-3xl pointer-events-none"></div>

			<div class="relative z-10 flex flex-col items-center text-center max-w-4xl mx-auto">
				<div class="inline-flex items-center gap-3 px-4 py-1.5 rounded-full bg-surface-container-high/90 shadow-md mb-8">
					<span class="inline-flex items-center gap-1.5 text-secondary font-mono-data text-[10px] font-semibold tracking-wider uppercase">
						<span class="w-2 h-2 rounded-full bg-secondary animate-ping"></span>
						{$t('landing.engineOnline')}
					</span>
					<span class="w-1 h-1 rounded-full bg-outline-variant"></span>
					<span class="text-on-surface-variant font-mono-data text-xs">{$t('landing.logicCoreSync')}</span>
				</div>

				<h1 class="font-headline text-3xl md:text-5xl lg:text-[56px] lg:leading-[68px] font-semibold tracking-tight bg-gradient-to-b from-white via-primary to-secondary bg-clip-text text-transparent drop-shadow-[0_0_35px_rgba(210,187,255,0.4)] mb-6">
					{$t('landing.heroTitle')}
				</h1>
				<p class="text-base md:text-lg text-on-surface-variant max-w-2xl mx-auto mb-4 leading-relaxed">
					{$t('landing.heroSubtitle')}
				</p>
				<p class="text-sm text-on-surface-variant/70 max-w-xl mx-auto mb-10">
					{$t('landing.entertainmentNotice')}
				</p>

				<div class="flex flex-wrap items-center justify-center gap-4 mb-12">
					<a
						href="/reading"
						class="group inline-flex items-center gap-3 px-8 py-4 rounded-full bg-gradient-to-r from-primary-container to-secondary-container text-white font-headline text-base font-semibold shadow-[0_0_28px_rgba(124,58,237,0.4)] hover:shadow-[0_0_40px_rgba(76,215,246,0.6)] hover:scale-105 transition-all duration-300"
					>
						<span class="material-symbols-outlined text-xl transition-transform group-hover:rotate-45">auto_awesome</span>
						<span>{$t('landing.startReading')}</span>
					</a>
					<a
						href="/dashboard"
						class="inline-flex items-center gap-3 px-8 py-4 rounded-full bg-surface-container-high/60 hover:bg-surface-container-high text-on-surface font-headline text-base font-semibold backdrop-blur-md shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
					>
						<span class="material-symbols-outlined text-xl text-secondary">orbit</span>
						<span>{$t('landing.exploreDashboard')}</span>
					</a>
				</div>

				<div class="w-full max-w-3xl grid grid-cols-1 md:grid-cols-3 gap-3 p-4 rounded-2xl bg-surface-container-high/40 backdrop-blur-md shadow-inner">
					<div class="flex flex-col items-center justify-center py-2 px-4">
						<div class="flex items-center gap-1.5 text-primary font-headline text-xl font-medium">
							<span>78</span>
							<span class="text-secondary text-xs">/ 78</span>
						</div>
						<span class="text-on-surface-variant font-mono-data text-[11px] uppercase tracking-wider">{$t('landing.statArcanaMapped')}</span>
					</div>
					<div class="flex flex-col items-center justify-center py-2 px-4">
						<div class="text-secondary font-headline text-xl font-medium">12 Signs</div>
						<span class="text-on-surface-variant font-mono-data text-[11px] uppercase tracking-wider">{$t('landing.statZodiacCovered')}</span>
					</div>
					<div class="flex flex-col items-center justify-center py-2 px-4">
						<div class="flex items-center gap-2 text-tertiary font-headline text-xl font-medium">
							<span class="w-2 h-2 rounded-full bg-secondary shadow-[0_0_8px_#4cd7f6]"></span>
							<span>{$t('landing.statDeterministic')}</span>
						</div>
						<span class="text-on-surface-variant font-mono-data text-[11px] uppercase tracking-wider">{$t('landing.statPrologEngine')}</span>
					</div>
				</div>
			</div>
		</section>

		<!-- Zodiac Wheel -->
		<section class="w-full mb-20">
			<div class="flex flex-col items-center text-center max-w-2xl mx-auto mb-10">
				<div class="inline-flex items-center gap-2 text-primary font-mono-data text-[10px] font-semibold uppercase tracking-widest mb-2">
					<span class="material-symbols-outlined text-sm">cyclone</span>
					{$t('landing.celestialWheel')}
				</div>
				<h2 class="font-headline text-2xl md:text-3xl font-medium text-on-surface mb-3">{$t('landing.twelveModalities')}</h2>
				<p class="text-on-surface-variant text-sm md:text-base">
					{$t('landing.wheelDesc')}
				</p>
				<div class="flex flex-wrap items-center justify-center gap-3 mt-6">
					<div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-high text-fire font-mono-data text-[10px] font-semibold uppercase tracking-wider shadow-sm">
						<span class="w-2 h-2 rounded-full bg-fire"></span> {formatElement('fire', $locale)}
					</div>
					<div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-high text-earth font-mono-data text-[10px] font-semibold uppercase tracking-wider shadow-sm">
						<span class="w-2 h-2 rounded-full bg-earth"></span> {formatElement('earth', $locale)}
					</div>
					<div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-high text-air font-mono-data text-[10px] font-semibold uppercase tracking-wider shadow-sm">
						<span class="w-2 h-2 rounded-full bg-air"></span> {formatElement('air', $locale)}
					</div>
					<div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-high text-water font-mono-data text-[10px] font-semibold uppercase tracking-wider shadow-sm">
						<span class="w-2 h-2 rounded-full bg-water"></span> {formatElement('water', $locale)}
					</div>
				</div>
			</div>

			<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
				{#each signs as [sign, symbol]}
					{@const info = elementInfo[sign]}
					{@const zData = getZodiacTranslation(sign, $locale)}
					<a
						href="/zodiac?sign={sign}"
						class="group relative rounded-2xl bg-surface-container/70 backdrop-blur-md p-5 flex flex-col items-center text-center shadow-lg hover:-translate-y-1 transition-all duration-300"
					>
						<div class="w-14 h-14 rounded-full bg-surface-container-high flex items-center justify-center mb-3 shadow-inner group-hover:scale-110 transition-transform">
							<span class="text-2xl {info.color}">{symbol}</span>
						</div>
						<span class="font-headline text-sm font-semibold text-on-surface mb-1 truncate max-w-full">{zData.name}</span>
						<span class="{info.color} font-mono-data text-[10px] font-semibold uppercase tracking-wider">{zData.element} • {zData.modality}</span>
						<span class="text-on-surface-variant font-mono-data text-[11px] mt-2">{zData.ruler} • {info.degrees}</span>
					</a>
				{/each}
			</div>
		</section>

		<!-- Features -->
		<section class="w-full mb-20">
			<div class="flex flex-col items-start max-w-2xl mb-12">
				<div class="inline-flex items-center gap-2 text-secondary font-mono-data text-[10px] font-semibold uppercase tracking-widest mb-2">
					<span class="material-symbols-outlined text-sm">science</span>
					{$t('landing.coreCapabilities')}
				</div>
				<h2 class="font-headline text-2xl md:text-3xl font-medium text-on-surface mb-3">{$t('landing.highOrderInstruments')}</h2>
				<p class="text-on-surface-variant text-sm md:text-base">
					{$t('landing.capabilitiesDesc')}
				</p>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
				{#each features as feature}
					<div class="group relative rounded-2xl bg-surface-container/70 backdrop-blur-xl p-8 shadow-xl hover:-translate-y-1 transition-all duration-300 flex flex-col justify-between">
						<div>
							<div class="w-12 h-12 rounded-xl {feature.accent} flex items-center justify-center mb-6 shadow-md group-hover:scale-110 transition-transform">
								<span class="material-symbols-outlined text-2xl">{feature.icon}</span>
							</div>
							<span class="text-secondary font-mono-data text-[10px] font-semibold uppercase tracking-widest">{feature.eyebrow}</span>
							<h3 class="font-headline text-lg font-medium text-on-surface mt-1 mb-3">{feature.title}</h3>
							<p class="text-on-surface-variant text-sm leading-relaxed">{feature.desc}</p>
						</div>
						<div class="mt-6 pt-4 flex items-center justify-between text-on-surface-variant font-mono-data text-[11px]">
							<span>{feature.meta}</span>
							<a href={feature.href} class="text-secondary hover:text-white flex items-center gap-1 transition-colors font-medium">
								{feature.cta} <span class="material-symbols-outlined text-sm">arrow_forward</span>
							</a>
						</div>
					</div>
				{/each}
			</div>
		</section>

		<!-- How It Works -->
		<section class="w-full mb-20">
			<div class="flex flex-col items-center text-center max-w-2xl mx-auto mb-14">
				<div class="inline-flex items-center gap-2 text-primary font-mono-data text-[10px] font-semibold uppercase tracking-widest mb-2">
					<span class="material-symbols-outlined text-sm">route</span>
					{$t('landing.divinationProtocol')}
				</div>
				<h2 class="font-headline text-2xl md:text-3xl font-medium text-on-surface mb-3">{$t('landing.howItWorks')}</h2>
				<p class="text-on-surface-variant text-sm md:text-base">
					{$t('landing.howItWorksDesc')}
				</p>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
				{#each steps as step}
					<div class="relative rounded-2xl bg-surface-container/70 backdrop-blur-xl p-6 shadow-lg flex flex-col justify-between">
						<div>
							<div class="flex items-center justify-between mb-4">
								<span class="w-8 h-8 rounded-full bg-primary-container text-white font-headline text-sm font-semibold flex items-center justify-center shadow-md">{step.num}</span>
								<span class="material-symbols-outlined text-secondary text-xl">{step.icon}</span>
							</div>
							<span class="text-primary font-mono-data text-[10px] font-semibold uppercase tracking-widest">{step.eyebrow}</span>
							<h4 class="font-headline text-base font-semibold text-on-surface mt-1 mb-2">{step.title}</h4>
							<p class="text-on-surface-variant text-sm leading-relaxed">{step.desc}</p>
						</div>
						<div class="mt-6 pt-3 flex items-center gap-2 text-secondary font-mono-data text-[11px]">
							<span class="material-symbols-outlined text-sm">keyboard_double_arrow_right</span>
							<span>{step.tag}</span>
						</div>
					</div>
				{/each}
			</div>
		</section>

		<!-- Closing CTA -->
		<section class="relative w-full rounded-3xl bg-gradient-to-r from-surface-container-high via-surface-container-low to-surface-container-lowest p-8 lg:p-14 overflow-hidden shadow-2xl">
			<div class="absolute top-0 right-0 w-80 h-80 rounded-full bg-secondary-container/10 blur-3xl pointer-events-none"></div>
			<div class="absolute bottom-0 left-10 w-72 h-72 rounded-full bg-primary-container/15 blur-3xl pointer-events-none"></div>

			<div class="relative z-10 flex flex-col lg:flex-row items-center justify-between gap-8">
				<div class="max-w-xl text-center lg:text-left">
					<span class="px-3 py-1 rounded-full bg-surface-container-highest text-secondary font-mono-data text-[10px] font-semibold uppercase tracking-wider mb-4 inline-block">
						{$t('landing.ctaTag')}
					</span>
					<h2 class="font-headline text-2xl md:text-3xl font-medium text-on-surface mb-3">{$t('landing.ctaTitle')}</h2>
					<p class="text-on-surface-variant text-sm md:text-base leading-relaxed">
						{$t('landing.ctaDesc')}
					</p>
				</div>
				<div class="flex flex-col sm:flex-row items-center gap-4 shrink-0">
					<a
						href="/reading"
						class="w-full sm:w-auto px-8 py-4 rounded-full bg-gradient-to-r from-primary-container to-secondary-container text-white font-headline text-base font-semibold text-center shadow-[0_0_24px_rgba(124,58,237,0.4)] hover:shadow-[0_0_35px_rgba(76,215,246,0.6)] hover:scale-105 transition-all duration-300"
					>
						{$t('landing.ctaDraw')}
					</a>
					<a
						href="/birth-chart"
						class="w-full sm:w-auto px-8 py-4 rounded-full bg-surface-container text-on-surface hover:bg-surface-container-high font-headline text-base font-semibold text-center backdrop-blur-md shadow-md hover:scale-105 transition-all duration-300"
					>
						{$t('landing.ctaChart')}
					</a>
				</div>
			</div>
		</section>
	</div>
</div>
