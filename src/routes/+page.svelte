<script lang="ts">
	import { ZODIAC_SYMBOLS } from '$lib/types';

	const features = [
		{
			icon: 'auto_awesome',
			eyebrow: 'Neural Synthesis',
			title: 'AI-Powered Readings',
			desc: 'Deep narrative synthesis powered by AI, conditioned on tarot symbolism and classical astrological texts.',
			meta: 'Spread Depth: Variable',
			cta: 'Launch',
			href: '/reading',
			accent: 'text-primary bg-primary-container/20'
		},
		{
			icon: 'account_tree',
			eyebrow: 'Formal Verification',
			title: 'Symbolic Reasoning',
			desc: 'A Prolog deductive engine checks decan alignments, elemental dignities, and card relationships without hallucination.',
			meta: 'Engine: Prolog Core',
			cta: 'Inspect',
			href: '/chat',
			accent: 'text-secondary bg-secondary-container/20'
		},
		{
			icon: 'public',
			eyebrow: 'Ephemeris Precision',
			title: 'Birth Chart Analysis',
			desc: 'Planetary computations for Sun, Moon, Rising, and house placements mapped against your exact birth data.',
			meta: 'Precision: Arcminute',
			cta: 'Calculate',
			href: '/birth-chart',
			accent: 'text-tertiary bg-tertiary-container/20'
		},
		{
			icon: 'join_inner',
			eyebrow: 'Synastry Modeling',
			title: 'Zodiac Compatibility',
			desc: 'Explore elemental and planetary resonance between two signs across emotional, intellectual, and physical wavelengths.',
			meta: 'Matrix: Dual Sign',
			cta: 'Compare',
			href: '/compatibility',
			accent: 'text-secondary bg-surface-container-high'
		},
		{
			icon: 'document_scanner',
			eyebrow: 'Vision Telemetry',
			title: 'Card Scanner',
			desc: 'Snap a photo of a physical tarot draw and let computer vision identify the card for an instant reading.',
			meta: 'Input: Camera / Upload',
			cta: 'Scan Deck',
			href: '/scan',
			accent: 'text-primary bg-surface-container-high'
		},
		{
			icon: 'psychology_alt',
			eyebrow: 'Socratic Tutor',
			title: 'AI Mystic Guide',
			desc: 'Chat with a tarot and astrology-themed AI assistant that clarifies archetypal lessons behind your readings.',
			meta: 'Mode: Continuous Dialogue',
			cta: 'Consult',
			href: '/chat',
			accent: 'text-tertiary bg-primary-container/20'
		}
	];

	const steps = [
		{
			num: 1,
			icon: 'psychology',
			eyebrow: 'Phase Alpha',
			title: 'Ask Your Question',
			desc: 'Pose a question or pick a focus area. We translate it into the symbolic inputs the reasoning engine understands.',
			tag: 'Intent Captured'
		},
		{
			num: 2,
			icon: 'memory',
			eyebrow: 'Phase Beta',
			title: 'Prolog Reasons Symbolically',
			desc: 'The Prolog inference engine checks planetary dignities, elemental relationships, and card meanings against its rule base.',
			tag: 'Logic Confirmed'
		},
		{
			num: 3,
			icon: 'auto_stories',
			eyebrow: 'Phase Gamma',
			title: 'Cards Are Drawn',
			desc: 'A spread is drawn (or scanned) and paired with the verified symbolic groundwork from the reasoning core.',
			tag: 'Spread Formed'
		},
		{
			num: 4,
			icon: 'checklist_rtl',
			eyebrow: 'Phase Delta',
			title: 'AI Interprets Meaningfully',
			desc: 'An AI model weaves the deterministic symbolic proof into a nuanced, personalized reading you can revisit anytime.',
			tag: 'Saved to History'
		}
	];

	const elementInfo: Record<string, { color: string; label: string; modality: string; ruler: string; degrees: string }> = {
		aries: { color: 'text-fire', label: 'Fire', modality: 'Cardinal', ruler: 'Mars', degrees: '0°-30°' },
		taurus: { color: 'text-earth', label: 'Earth', modality: 'Fixed', ruler: 'Venus', degrees: '30°-60°' },
		gemini: { color: 'text-air', label: 'Air', modality: 'Mutable', ruler: 'Mercury', degrees: '60°-90°' },
		cancer: { color: 'text-water', label: 'Water', modality: 'Cardinal', ruler: 'Moon', degrees: '90°-120°' },
		leo: { color: 'text-fire', label: 'Fire', modality: 'Fixed', ruler: 'Sun', degrees: '120°-150°' },
		virgo: { color: 'text-earth', label: 'Earth', modality: 'Mutable', ruler: 'Mercury', degrees: '150°-180°' },
		libra: { color: 'text-air', label: 'Air', modality: 'Cardinal', ruler: 'Venus', degrees: '180°-210°' },
		scorpio: { color: 'text-water', label: 'Water', modality: 'Fixed', ruler: 'Pluto / Mars', degrees: '210°-240°' },
		sagittarius: { color: 'text-fire', label: 'Fire', modality: 'Mutable', ruler: 'Jupiter', degrees: '240°-270°' },
		capricorn: { color: 'text-earth', label: 'Earth', modality: 'Cardinal', ruler: 'Saturn', degrees: '270°-300°' },
		aquarius: { color: 'text-air', label: 'Air', modality: 'Fixed', ruler: 'Uranus', degrees: '300°-330°' },
		pisces: { color: 'text-water', label: 'Water', modality: 'Mutable', ruler: 'Neptune', degrees: '330°-360°' }
	};

	const signs = Object.entries(ZODIAC_SYMBOLS);
</script>

<svelte:head>
	<title>AstroLogic - AI Zodiac & Tarot Reasoning</title>
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
						Reasoning Engine Online
					</span>
					<span class="w-1 h-1 rounded-full bg-outline-variant"></span>
					<span class="text-on-surface-variant font-mono-data text-xs">Prolog Logic Core Synchronized</span>
				</div>

				<h1 class="font-headline text-4xl md:text-6xl lg:text-[64px] lg:leading-[72px] font-semibold tracking-tight bg-gradient-to-b from-white via-primary to-secondary bg-clip-text text-transparent drop-shadow-[0_0_35px_rgba(210,187,255,0.4)] mb-6">
					Where Ancient Celestial Wisdom Meets Symbolic AI
				</h1>
				<p class="text-base md:text-lg text-on-surface-variant max-w-2xl mx-auto mb-4 leading-relaxed">
					AstroLogic combines symbolic Prolog reasoning with AI interpretation to produce meaningful tarot readings, horoscopes, and birth chart insights.
				</p>
				<p class="text-sm text-on-surface-variant/70 max-w-xl mx-auto mb-10">
					For entertainment and self-reflection.
				</p>

				<div class="flex flex-wrap items-center justify-center gap-4 mb-12">
					<a
						href="/reading"
						class="group inline-flex items-center gap-3 px-8 py-4 rounded-full bg-gradient-to-r from-primary-container to-secondary-container text-white font-headline text-base font-semibold shadow-[0_0_28px_rgba(124,58,237,0.4)] hover:shadow-[0_0_40px_rgba(76,215,246,0.6)] hover:scale-105 transition-all duration-300"
					>
						<span class="material-symbols-outlined text-xl transition-transform group-hover:rotate-45">auto_awesome</span>
						<span>Start a Reading</span>
					</a>
					<a
						href="/dashboard"
						class="inline-flex items-center gap-3 px-8 py-4 rounded-full bg-surface-container-high/60 hover:bg-surface-container-high text-on-surface font-headline text-base font-semibold backdrop-blur-md shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
					>
						<span class="material-symbols-outlined text-xl text-secondary">orbit</span>
						<span>Explore Dashboard</span>
					</a>
				</div>

				<div class="w-full max-w-3xl grid grid-cols-1 md:grid-cols-3 gap-3 p-4 rounded-2xl bg-surface-container-high/40 backdrop-blur-md shadow-inner">
					<div class="flex flex-col items-center justify-center py-2 px-4">
						<div class="flex items-center gap-1.5 text-primary font-headline text-xl font-medium">
							<span>78</span>
							<span class="text-secondary text-xs">/ 78</span>
						</div>
						<span class="text-on-surface-variant font-mono-data text-[11px] uppercase tracking-wider">Arcana Mapped</span>
					</div>
					<div class="flex flex-col items-center justify-center py-2 px-4">
						<div class="text-secondary font-headline text-xl font-medium">12 Signs</div>
						<span class="text-on-surface-variant font-mono-data text-[11px] uppercase tracking-wider">Zodiac Wheel Covered</span>
					</div>
					<div class="flex flex-col items-center justify-center py-2 px-4">
						<div class="flex items-center gap-2 text-tertiary font-headline text-xl font-medium">
							<span class="w-2 h-2 rounded-full bg-secondary shadow-[0_0_8px_#4cd7f6]"></span>
							<span>Deterministic</span>
						</div>
						<span class="text-on-surface-variant font-mono-data text-[11px] uppercase tracking-wider">Symbolic Prolog Engine</span>
					</div>
				</div>
			</div>
		</section>

		<!-- Zodiac Wheel -->
		<section class="w-full mb-20">
			<div class="flex flex-col items-center text-center max-w-2xl mx-auto mb-10">
				<div class="inline-flex items-center gap-2 text-primary font-mono-data text-[10px] font-semibold uppercase tracking-widest mb-2">
					<span class="material-symbols-outlined text-sm">cyclone</span>
					The Celestial Wheel
				</div>
				<h2 class="font-headline text-2xl md:text-3xl font-medium text-on-surface mb-3">Twelve Archetypal Modalities</h2>
				<p class="text-on-surface-variant text-sm md:text-base">
					Explore all 12 signs. Each is mapped to its element, ruling planet, and degree range on the zodiac wheel.
				</p>
				<div class="flex flex-wrap items-center justify-center gap-3 mt-6">
					<div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-high text-fire font-mono-data text-[10px] font-semibold uppercase tracking-wider shadow-sm">
						<span class="w-2 h-2 rounded-full bg-fire"></span> Fire
					</div>
					<div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-high text-earth font-mono-data text-[10px] font-semibold uppercase tracking-wider shadow-sm">
						<span class="w-2 h-2 rounded-full bg-earth"></span> Earth
					</div>
					<div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-high text-air font-mono-data text-[10px] font-semibold uppercase tracking-wider shadow-sm">
						<span class="w-2 h-2 rounded-full bg-air"></span> Air
					</div>
					<div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-high text-water font-mono-data text-[10px] font-semibold uppercase tracking-wider shadow-sm">
						<span class="w-2 h-2 rounded-full bg-water"></span> Water
					</div>
				</div>
			</div>

			<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
				{#each signs as [sign, symbol]}
					{@const info = elementInfo[sign]}
					<a
						href="/zodiac?sign={sign}"
						class="group relative rounded-2xl bg-surface-container/70 backdrop-blur-md p-5 flex flex-col items-center text-center shadow-lg hover:-translate-y-1 transition-all duration-300"
					>
						<div class="w-14 h-14 rounded-full bg-surface-container-high flex items-center justify-center mb-3 shadow-inner group-hover:scale-110 transition-transform">
							<span class="text-2xl {info.color}">{symbol}</span>
						</div>
						<span class="font-headline text-sm font-semibold text-on-surface mb-1 capitalize">{sign}</span>
						<span class="{info.color} font-mono-data text-[10px] font-semibold uppercase tracking-wider">{info.label} • {info.modality}</span>
						<span class="text-on-surface-variant font-mono-data text-[11px] mt-2">{info.ruler} • {info.degrees}</span>
					</a>
				{/each}
			</div>
		</section>

		<!-- Features -->
		<section class="w-full mb-20">
			<div class="flex flex-col items-start max-w-2xl mb-12">
				<div class="inline-flex items-center gap-2 text-secondary font-mono-data text-[10px] font-semibold uppercase tracking-widest mb-2">
					<span class="material-symbols-outlined text-sm">science</span>
					Core Capabilities
				</div>
				<h2 class="font-headline text-2xl md:text-3xl font-medium text-on-surface mb-3">High-Order Celestial Instruments</h2>
				<p class="text-on-surface-variant text-sm md:text-base">
					Built for seekers and the symbolically curious alike. Deterministic reasoning meets AI-crafted narrative.
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
							<a href={feature.href} class="text-secondary hover:text-white flex items-center gap-1 transition-colors">
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
					The Divination Protocol
				</div>
				<h2 class="font-headline text-2xl md:text-3xl font-medium text-on-surface mb-3">How AstroLogic Works</h2>
				<p class="text-on-surface-variant text-sm md:text-base">
					From your question to a verified symbolic proof to a personalized, AI-written reading.
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
						Open Observatory Access
					</span>
					<h2 class="font-headline text-2xl md:text-3xl font-medium text-on-surface mb-3">Begin Your First Reading</h2>
					<p class="text-on-surface-variant text-sm md:text-base leading-relaxed">
						Draw a tarot spread or compute your birth chart, backed by the Prolog reasoning core, in seconds.
					</p>
				</div>
				<div class="flex flex-col sm:flex-row items-center gap-4 shrink-0">
					<a
						href="/reading"
						class="w-full sm:w-auto px-8 py-4 rounded-full bg-gradient-to-r from-primary-container to-secondary-container text-white font-headline text-base font-semibold text-center shadow-[0_0_24px_rgba(124,58,237,0.4)] hover:shadow-[0_0_35px_rgba(76,215,246,0.6)] hover:scale-105 transition-all duration-300"
					>
						Draw Cards Now
					</a>
					<a
						href="/birth-chart"
						class="w-full sm:w-auto px-8 py-4 rounded-full bg-surface-container text-on-surface hover:bg-surface-container-high font-headline text-base font-semibold text-center backdrop-blur-md shadow-md hover:scale-105 transition-all duration-300"
					>
						Compute Birth Chart
					</a>
				</div>
			</div>
		</section>
	</div>
</div>
