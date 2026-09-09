<script lang="ts">
	import { locale, formatPlanet } from '$lib/i18n';
	import type { PlanetPosition } from '$lib/types';

	interface BirthChartData {
		sun_sign: string;
		moon_sign: string;
		rising_sign: string;
		sun_degree?: number;
		moon_degree?: number;
		rising_degree?: number;
		planets?: PlanetPosition[];
		timezone?: string;
	}

	let {
		chart,
		birthInfo
	}: {
		chart: BirthChartData;
		birthInfo?: {
			year: number;
			month: number;
			day: number;
			hour: number;
			minute: number;
			latitude?: number | null;
			longitude?: number | null;
		};
	} = $props();

	// ZODIAC SIGNS REFERENCE (0° to 360°)
	const ZODIAC_SIGNS = [
		{
			id: 'aries',
			symbol: '♈',
			nameEn: 'Aries',
			nameMy: 'မိဿ',
			startDeg: 0,
			element: 'fire',
			modality: 'cardinal',
			color: '#ef4444'
		},
		{
			id: 'taurus',
			symbol: '♉',
			nameEn: 'Taurus',
			nameMy: 'ပြိဿ',
			startDeg: 30,
			element: 'earth',
			modality: 'fixed',
			color: '#10b981'
		},
		{
			id: 'gemini',
			symbol: '♊',
			nameEn: 'Gemini',
			nameMy: 'မေထုန်',
			startDeg: 60,
			element: 'air',
			modality: 'mutable',
			color: '#f59e0b'
		},
		{
			id: 'cancer',
			symbol: '♋',
			nameEn: 'Cancer',
			nameMy: 'ကရကဋ်',
			startDeg: 90,
			element: 'water',
			modality: 'cardinal',
			color: '#3b82f6'
		},
		{
			id: 'leo',
			symbol: '♌',
			nameEn: 'Leo',
			nameMy: 'သိဟ်',
			startDeg: 120,
			element: 'fire',
			modality: 'fixed',
			color: '#ef4444'
		},
		{
			id: 'virgo',
			symbol: '♍',
			nameEn: 'Virgo',
			nameMy: 'ကန်',
			startDeg: 150,
			element: 'earth',
			modality: 'mutable',
			color: '#10b981'
		},
		{
			id: 'libra',
			symbol: '♎',
			nameEn: 'Libra',
			nameMy: 'တူ',
			startDeg: 180,
			element: 'air',
			modality: 'cardinal',
			color: '#f59e0b'
		},
		{
			id: 'scorpio',
			symbol: '♏',
			nameEn: 'Scorpio',
			nameMy: 'ဗြိစ္ဆာ',
			startDeg: 210,
			element: 'water',
			modality: 'fixed',
			color: '#3b82f6'
		},
		{
			id: 'sagittarius',
			symbol: '♐',
			nameEn: 'Sagittarius',
			nameMy: 'ဓနု',
			startDeg: 240,
			element: 'fire',
			modality: 'mutable',
			color: '#ef4444'
		},
		{
			id: 'capricorn',
			symbol: '♑',
			nameEn: 'Capricorn',
			nameMy: 'မကာရ',
			startDeg: 270,
			element: 'earth',
			modality: 'cardinal',
			color: '#10b981'
		},
		{
			id: 'aquarius',
			symbol: '♒',
			nameEn: 'Aquarius',
			nameMy: 'ကုမ်',
			startDeg: 300,
			element: 'air',
			modality: 'fixed',
			color: '#f59e0b'
		},
		{
			id: 'pisces',
			symbol: '♓',
			nameEn: 'Pisces',
			nameMy: 'မိန်',
			startDeg: 330,
			element: 'water',
			modality: 'mutable',
			color: '#3b82f6'
		}
	] as const;

	interface ChartBody {
		id: string;
		name: string;
		symbol: string;
		sign: string;
		eclipticDeg: number;
		signDeg: number;
		signMin: number;
		retrograde: boolean;
		element: 'fire' | 'earth' | 'air' | 'water';
		modality: 'cardinal' | 'fixed' | 'mutable';
	}

	function range(length: number): number[] {
		return Array.from({ length }, (_, i) => i);
	}

	function signIndex(signName: string): number {
		const lower = (signName || '').toLowerCase();
		const idx = ZODIAC_SIGNS.findIndex((z) => z.id === lower || z.nameEn.toLowerCase() === lower);
		return idx >= 0 ? idx : 0;
	}

	const allBodies = $derived.by<ChartBody[]>(() => {
		const list: ChartBody[] = [];

		// 1. Sun
		const sunSignIdx = signIndex(chart.sun_sign);
		const sunEcliptic = chart.sun_degree !== undefined ? chart.sun_degree : sunSignIdx * 30 + 15;
		const sunSignDeg = sunEcliptic % 30;
		const sunSignInfo = ZODIAC_SIGNS[sunSignIdx];
		list.push({
			id: 'sun',
			name: 'Sun',
			symbol: '☉',
			sign: chart.sun_sign,
			eclipticDeg: sunEcliptic,
			signDeg: Math.floor(sunSignDeg),
			signMin: Math.floor((sunSignDeg % 1) * 60),
			retrograde: false,
			element: sunSignInfo.element,
			modality: sunSignInfo.modality
		});

		// 2. Moon
		const moonSignIdx = signIndex(chart.moon_sign);
		const moonEcliptic =
			chart.moon_degree !== undefined ? chart.moon_degree : moonSignIdx * 30 + 12;
		const moonSignDeg = moonEcliptic % 30;
		const moonSignInfo = ZODIAC_SIGNS[moonSignIdx];
		list.push({
			id: 'moon',
			name: 'Moon',
			symbol: '☽',
			sign: chart.moon_sign,
			eclipticDeg: moonEcliptic,
			signDeg: Math.floor(moonSignDeg),
			signMin: Math.floor((moonSignDeg % 1) * 60),
			retrograde: false,
			element: moonSignInfo.element,
			modality: moonSignInfo.modality
		});

		// 3. Other planets & celestial points
		const planetMeta: Record<string, { symbol: string; name: string }> = {
			mercury: { symbol: '☿', name: 'Mercury' },
			venus: { symbol: '♀', name: 'Venus' },
			mars: { symbol: '♂', name: 'Mars' },
			jupiter: { symbol: '♃', name: 'Jupiter' },
			saturn: { symbol: '♄', name: 'Saturn' },
			uranus: { symbol: '♅', name: 'Uranus' },
			neptune: { symbol: '♆', name: 'Neptune' },
			pluto: { symbol: '♇', name: 'Pluto' },
			node: { symbol: '☊', name: 'Node' },
			lilith: { symbol: '⚸', name: 'Lilith' },
			chiron: { symbol: '⚷', name: 'Chiron' }
		};

		if (chart.planets && chart.planets.length > 0) {
			for (const p of chart.planets) {
				const pId = p.name.toLowerCase();
				const pMeta = planetMeta[pId] || { symbol: p.symbol || '✧', name: p.name };
				const sIdx = signIndex(p.sign);
				const sInfo = ZODIAC_SIGNS[sIdx];
				const pEcliptic = p.degree !== undefined ? p.degree : sIdx * 30 + 10;
				const pSignDeg = pEcliptic % 30;

				list.push({
					id: pId,
					name: pMeta.name,
					symbol: pMeta.symbol,
					sign: p.sign,
					eclipticDeg: pEcliptic,
					signDeg: Math.floor(pSignDeg),
					signMin: Math.floor((pSignDeg % 1) * 60),
					retrograde: Boolean(p.retrograde),
					element: sInfo.element,
					modality: sInfo.modality
				});
			}
		}

		return list;
	});

	// Wheel Rotation Base: Ascendant (or 0 if not provided)
	const ascendantDegree = $derived(chart.rising_degree ?? signIndex(chart.rising_sign) * 30 + 15);

	// Convert Ecliptic Degree (0-360) to Canvas Angle (in degrees)
	// In Astro-Seek: Ascendant is on the left horizontal axis (180°), signs run counter-clockwise
	function eclipticToAngle(eclipticDeg: number): number {
		// Ascendant placed at 180°
		const relative = (eclipticDeg - ascendantDegree + 360) % 360;
		return (180 - relative + 360) % 360;
	}

	function polarToCartesian(
		centerX: number,
		centerY: number,
		radius: number,
		angleInDegrees: number
	) {
		const rad = (angleInDegrees * Math.PI) / 180;
		return {
			x: centerX + radius * Math.cos(rad),
			y: centerY - radius * Math.sin(rad)
		};
	}

	// ASPECTS COMPUTATION
	interface Aspect {
		body1: ChartBody;
		body2: ChartBody;
		index1: number;
		index2: number;
		type: 'conjunction' | 'sextile' | 'square' | 'trine' | 'opposition';
		symbol: string;
		color: string;
		orb: number;
		orbStr: string;
		isHarmonious: boolean;
	}

	const aspects = $derived.by<Aspect[]>(() => {
		const res: Aspect[] = [];
		const bodies = allBodies;

		for (let i = 0; i < bodies.length; i++) {
			for (let j = i + 1; j < bodies.length; j++) {
				const b1 = bodies[i];
				const b2 = bodies[j];
				let diff = Math.abs(b1.eclipticDeg - b2.eclipticDeg) % 360;
				if (diff > 180) diff = 360 - diff;

				let aspType: Aspect['type'] | null = null;
				let symbol = '';
				let color = '';
				let targetAngle = 0;
				let isHarmonious = true;

				if (diff <= 8) {
					aspType = 'conjunction';
					symbol = '☌';
					color = '#eab308'; // Amber
					targetAngle = 0;
				} else if (Math.abs(diff - 60) <= 6) {
					aspType = 'sextile';
					symbol = '✱';
					color = '#3b82f6'; // Blue
					targetAngle = 60;
				} else if (Math.abs(diff - 90) <= 8) {
					aspType = 'square';
					symbol = '□';
					color = '#ef4444'; // Red
					targetAngle = 90;
					isHarmonious = false;
				} else if (Math.abs(diff - 120) <= 8) {
					aspType = 'trine';
					symbol = '△';
					color = '#2563eb'; // Deep Blue
					targetAngle = 120;
				} else if (Math.abs(diff - 180) <= 8) {
					aspType = 'opposition';
					symbol = '☍';
					color = '#dc2626'; // Deep Red
					targetAngle = 180;
					isHarmonious = false;
				}

				if (aspType) {
					const orb = Math.abs(diff - targetAngle);
					const signDiff = diff - targetAngle;
					const orbInt = Math.floor(orb);
					const orbSuffix = signDiff >= 0 ? 'a' : 's';
					res.push({
						body1: b1,
						body2: b2,
						index1: i,
						index2: j,
						type: aspType,
						symbol,
						color,
						orb,
						orbStr: `${orbInt}°${orbSuffix}`,
						isHarmonious
					});
				}
			}
		}

		return res;
	});

	// ELEMENT X MODALITY TOTALS
	const elementModalityMatrix = $derived.by(() => {
		const matrix: Record<
			'fire' | 'earth' | 'air' | 'water',
			Record<'cardinal' | 'fixed' | 'mutable', ChartBody[]>
		> = {
			fire: { cardinal: [], fixed: [], mutable: [] },
			earth: { cardinal: [], fixed: [], mutable: [] },
			air: { cardinal: [], fixed: [], mutable: [] },
			water: { cardinal: [], fixed: [], mutable: [] }
		};

		for (const b of allBodies) {
			if (matrix[b.element] && matrix[b.element][b.modality]) {
				matrix[b.element][b.modality].push(b);
			}
		}

		const rowTotals = {
			fire: matrix.fire.cardinal.length + matrix.fire.fixed.length + matrix.fire.mutable.length,
			earth: matrix.earth.cardinal.length + matrix.earth.fixed.length + matrix.earth.mutable.length,
			air: matrix.air.cardinal.length + matrix.air.fixed.length + matrix.air.mutable.length,
			water: matrix.water.cardinal.length + matrix.water.fixed.length + matrix.water.mutable.length
		};

		const colTotals = {
			cardinal:
				matrix.fire.cardinal.length +
				matrix.earth.cardinal.length +
				matrix.air.cardinal.length +
				matrix.water.cardinal.length,
			fixed:
				matrix.fire.fixed.length +
				matrix.earth.fixed.length +
				matrix.air.fixed.length +
				matrix.water.fixed.length,
			mutable:
				matrix.fire.mutable.length +
				matrix.earth.mutable.length +
				matrix.air.mutable.length +
				matrix.water.mutable.length
		};

		return { matrix, rowTotals, colTotals };
	});

	// SVG Dimensions
	const CX = 270;
	const CY = 270;
	const R_OUTER = 256;
	const R_ZODIAC_INNER = 214;
	const R_PLANETS = 175;
	const R_INNER_WEB = 135;

	const ascLeft = $derived(polarToCartesian(CX, CY, R_OUTER, 180));
	const dscRight = $derived(polarToCartesian(CX, CY, R_OUTER, 0));
	const mcTop = $derived(polarToCartesian(CX, CY, R_OUTER, 90));
	const icBottom = $derived(polarToCartesian(CX, CY, R_OUTER, 270));
</script>

<div
	class="flex flex-col gap-8 rounded-3xl border border-white/10 bg-surface-container-lowest/90 p-4 shadow-2xl backdrop-blur-xl sm:p-8"
>
	<!-- HEADER: Telemetry & Chart Title -->
	<div class="flex flex-wrap items-center justify-between gap-4 border-b border-white/10 pb-4">
		<div>
			<div class="flex items-center gap-2">
				<span class="inline-block h-2.5 w-2.5 animate-pulse rounded-full bg-primary"></span>
				<h3 class="font-headline text-lg font-bold tracking-tight text-on-surface sm:text-xl">
					{$locale === 'my'
						? 'နက္ခတ်ကြယ်တာရာ မွေးဖွားမှုစက်ဝန်း (Astro-Seek Wheel)'
						: 'Natal Birth Chart Wheel'}
				</h3>
			</div>
			<p class="font-mono-data mt-0.5 text-xs text-on-surface-variant">
				{#if birthInfo}
					{birthInfo.day}
					{birthInfo.month}/{birthInfo.year} &middot; {String(birthInfo.hour).padStart(
						2,
						'0'
					)}:{String(birthInfo.minute).padStart(2, '0')}
					{#if chart.timezone}&middot; {chart.timezone}{/if}
				{:else}
					360° Geocentric Ecliptic Longitudes
				{/if}
			</p>
		</div>

		<div class="font-mono-data flex items-center gap-2 text-xs">
			<span class="rounded-full bg-surface-container px-3 py-1 text-on-surface-variant">
				{$locale === 'my' ? 'လတ္တီတွဒ်/လောင်ဂျီတွဒ် တွက်ချက်ပြီး' : 'Planetary Ephemeris Active'}
			</span>
		</div>
	</div>

	<!-- MAIN CHART SVG WHEEL -->
	<div class="flex items-center justify-center py-2">
		<svg
			viewBox="0 0 540 540"
			class="aspect-square w-full max-w-[540px] drop-shadow-[0_8px_30px_rgba(0,0,0,0.5)] filter select-none"
		>
			<defs>
				<!-- Subtle central gradient -->
				<radialGradient id="centerGradient" cx="50%" cy="50%" r="50%">
					<stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.6" />
					<stop offset="100%" stop-color="#0f172a" stop-opacity="0.95" />
				</radialGradient>
				<radialGradient id="ringGradient" cx="50%" cy="50%" r="50%">
					<stop offset="70%" stop-color="#090d16" stop-opacity="0.9" />
					<stop offset="100%" stop-color="#1e293b" stop-opacity="0.95" />
				</radialGradient>
			</defs>

			<!-- Background Circles -->
			<circle
				cx={CX}
				cy={CY}
				r={R_OUTER}
				fill="url(#ringGradient)"
				stroke="#475569"
				stroke-width="1.5"
			/>
			<circle
				cx={CX}
				cy={CY}
				r={R_ZODIAC_INNER}
				fill="#090d16"
				stroke="#475569"
				stroke-width="1.2"
			/>
			<circle
				cx={CX}
				cy={CY}
				r={R_INNER_WEB}
				fill="url(#centerGradient)"
				stroke="#334155"
				stroke-width="1.2"
			/>

			<!-- 12 ZODIAC SECTORS & DEGREE TICK MARKS -->
			{#each ZODIAC_SIGNS as sign (sign.id)}
				{@const signStartAngle = eclipticToAngle(sign.startDeg)}
				{@const signMidAngle = eclipticToAngle(sign.startDeg + 15)}
				{@const glyphPos = polarToCartesian(CX, CY, (R_OUTER + R_ZODIAC_INNER) / 2, signMidAngle)}

				<!-- Sector separator radial line -->
				{@const radStart = polarToCartesian(CX, CY, R_ZODIAC_INNER, signStartAngle)}
				{@const radEnd = polarToCartesian(CX, CY, R_OUTER, signStartAngle)}
				<line
					x1={radStart.x}
					y1={radStart.y}
					x2={radEnd.x}
					y2={radEnd.y}
					stroke="#475569"
					stroke-width="1.5"
				/>

				<!-- 30 Degree Ticks inside this sign -->
				{#each range(30) as deg (deg)}
					{@const tickEcliptic = sign.startDeg + deg}
					{@const tickAngle = eclipticToAngle(tickEcliptic)}
					{@const isMajor = deg % 5 === 0}
					{@const tickR1 = isMajor ? R_OUTER - 10 : R_OUTER - 5}
					{@const p1 = polarToCartesian(CX, CY, tickR1, tickAngle)}
					{@const p2 = polarToCartesian(CX, CY, R_OUTER, tickAngle)}
					<line
						x1={p1.x}
						y1={p1.y}
						x2={p2.x}
						y2={p2.y}
						stroke={isMajor ? '#94a3b8' : '#475569'}
						stroke-width={isMajor ? 1 : 0.6}
					/>
				{/each}

				<!-- Zodiac Sign Glyph -->
				<text
					x={glyphPos.x}
					y={glyphPos.y + 6}
					text-anchor="middle"
					font-size="18"
					font-weight="bold"
					fill={sign.color}
					class="font-mono-data pointer-events-none drop-shadow"
				>
					{sign.symbol}
				</text>
			{/each}

			<!-- CENTRAL ASPECT WEB: Connecting Lines -->
			{#each aspects as asp (asp.body1.id + asp.body2.id + asp.type)}
				{@const a1 = eclipticToAngle(asp.body1.eclipticDeg)}
				{@const a2 = eclipticToAngle(asp.body2.eclipticDeg)}
				{@const p1 = polarToCartesian(CX, CY, R_INNER_WEB, a1)}
				{@const p2 = polarToCartesian(CX, CY, R_INNER_WEB, a2)}
				<line
					x1={p1.x}
					y1={p1.y}
					x2={p2.x}
					y2={p2.y}
					stroke={asp.color}
					stroke-width={asp.type === 'conjunction' ||
					asp.type === 'opposition' ||
					asp.type === 'trine'
						? 1.4
						: 1}
					stroke-opacity={0.8}
					stroke-dasharray={asp.type === 'sextile' ? '3,2' : undefined}
				/>
			{/each}

			<!-- ASCENDANT / DESCENDANT & IC / MC AXES -->
			<line
				x1={ascLeft.x}
				y1={ascLeft.y}
				x2={dscRight.x}
				y2={dscRight.y}
				stroke="#f43f5e"
				stroke-width="1.8"
			/>
			<!-- Ascendant Arrow -->
			<polygon
				points="{ascLeft.x},{ascLeft.y} {ascLeft.x + 10},{ascLeft.y - 4} {ascLeft.x +
					10},{ascLeft.y + 4}"
				fill="#f43f5e"
			/>
			<text
				x={ascLeft.x + 16}
				y={ascLeft.y - 6}
				font-size="10"
				font-weight="bold"
				fill="#f43f5e"
				class="font-mono-data"
			>
				AC
			</text>
			<text
				x={dscRight.x - 22}
				y={dscRight.y - 6}
				font-size="10"
				font-weight="bold"
				fill="#f43f5e"
				class="font-mono-data"
			>
				DC
			</text>

			<!-- MC / IC Axis (Vertical) -->
			<line
				x1={mcTop.x}
				y1={mcTop.y}
				x2={icBottom.x}
				y2={icBottom.y}
				stroke="#38bdf8"
				stroke-width="1.4"
				stroke-dasharray="4,2"
			/>
			<text
				x={mcTop.x + 4}
				y={mcTop.y + 14}
				font-size="10"
				font-weight="bold"
				fill="#38bdf8"
				class="font-mono-data"
			>
				MC
			</text>
			<text
				x={icBottom.x + 4}
				y={icBottom.y - 8}
				font-size="10"
				font-weight="bold"
				fill="#38bdf8"
				class="font-mono-data"
			>
				IC
			</text>

			<!-- PLANETARY GLYPHS & DEGREES IN THE PLANETARY TRACK -->
			{#each allBodies as body (body.id)}
				{@const angle = eclipticToAngle(body.eclipticDeg)}
				{@const posGlyph = polarToCartesian(CX, CY, R_PLANETS, angle)}
				{@const tickRim = polarToCartesian(CX, CY, R_ZODIAC_INNER, angle)}
				{@const tickTrack = polarToCartesian(CX, CY, R_INNER_WEB, angle)}
				{@const labelPos = polarToCartesian(CX, CY, R_PLANETS - 21, angle)}

				<!-- Subtle radial line indicating exact degree position -->
				<line
					x1={tickTrack.x}
					y1={tickTrack.y}
					x2={tickRim.x}
					y2={tickRim.y}
					stroke="#64748b"
					stroke-width="0.8"
					stroke-dasharray="2,2"
					opacity="0.6"
				/>

				<!-- Outer tick on zodiac inner rim -->
				<line
					x1={tickRim.x}
					y1={tickRim.y}
					x2={polarToCartesian(CX, CY, R_ZODIAC_INNER + 6, angle).x}
					y2={polarToCartesian(CX, CY, R_ZODIAC_INNER + 6, angle).y}
					stroke="#cbd5e1"
					stroke-width="1.5"
				/>

				<!-- Body Glyph Group -->
				<g class="cursor-pointer transition-transform hover:scale-125">
					<!-- Circle backdrop -->
					<circle
						cx={posGlyph.x}
						cy={posGlyph.y}
						r="11"
						fill="#0f172a"
						stroke="#64748b"
						stroke-width="1"
					/>
					<!-- Planet Glyph Symbol -->
					<text
						x={posGlyph.x}
						y={posGlyph.y + 4.5}
						text-anchor="middle"
						font-size="13"
						font-weight="bold"
						fill="#f8fafc"
						class="font-mono-data"
					>
						{body.symbol}
					</text>

					<!-- Retrograde badge (R) -->
					{#if body.retrograde}
						<text
							x={posGlyph.x + 8}
							y={posGlyph.y + 8}
							font-size="8"
							font-weight="bold"
							fill="#ef4444"
							class="font-mono-data"
						>
							R
						</text>
					{/if}

					<!-- Degree & Minute Label -->
					<text
						x={labelPos.x}
						y={labelPos.y + 3}
						text-anchor="middle"
						font-size="8.5"
						font-weight="semibold"
						fill="#94a3b8"
						class="font-mono-data tracking-tighter"
					>
						{body.signDeg}°{body.signMin}'
					</text>
				</g>
			{/each}
		</svg>
	</div>

	<!-- LOWER SECTION: 2 COLUMNS (ASPECT MATRIX & ELEMENT X MODALITY) -->
	<div class="grid grid-cols-1 items-start gap-6 lg:grid-cols-12">
		<!-- LEFT: PLANETARY POSITION TABLE & TRIANGULAR ASPECT MATRIX -->
		<div class="flex flex-col gap-3 overflow-x-auto lg:col-span-8">
			<div class="flex items-center gap-2">
				<span class="material-symbols-outlined text-sm text-primary">grid_view</span>
				<h4 class="font-headline text-sm font-semibold text-on-surface">
					{$locale === 'my'
						? 'ဂြိုဟ်များတည်နေရာနှင့် ထောင့်ချိတ်ဆက်မှုဇယား'
						: 'Planets & Triangular Aspect Grid'}
				</h4>
			</div>

			<div
				class="overflow-x-auto rounded-2xl border border-white/10 bg-surface-container-high/30 p-3"
			>
				<table class="font-mono-data w-full border-collapse text-xs">
					<tbody>
						{#each allBodies as body, rowIdx (body.id)}
							{@const sIdx = signIndex(body.sign)}
							{@const sInfo = ZODIAC_SIGNS[sIdx]}
							<tr class="border-b border-white/5 transition-colors hover:bg-white/5">
								<!-- Planet Glyph -->
								<td class="w-7 p-1.5 text-center text-sm font-bold text-white">
									{body.symbol}
								</td>
								<!-- Planet Name -->
								<td class="p-1.5 pr-2 font-medium whitespace-nowrap text-on-surface">
									{$locale === 'my' ? formatPlanet(body.id, 'my') || body.name : body.name}
								</td>
								<!-- Degrees & Minutes in Sign -->
								<td class="p-1.5 font-mono whitespace-nowrap text-on-surface-variant">
									{String(body.signDeg).padStart(2, '0')}°
									<span style:color={sInfo.color} class="px-0.5 font-bold">{sInfo.symbol}</span>
									{String(body.signMin).padStart(2, '0')}'
								</td>
								<!-- Retrograde Flag -->
								<td class="w-5 p-1 text-center">
									{#if body.retrograde}
										<span class="text-[10px] font-bold text-error">R</span>
									{:else}
										<span class="text-[10px] text-outline">-</span>
									{/if}
								</td>

								<!-- Triangular Aspect Grid Cells (Cols 0 to rowIdx - 1) -->
								{#each range(rowIdx) as colIdx (colIdx)}
									{@const cellAspect = aspects.find(
										(a) =>
											(a.index1 === colIdx && a.index2 === rowIdx) ||
											(a.index1 === rowIdx && a.index2 === colIdx)
									)}
									<td
										class="h-8 w-8 border border-white/10 p-1 text-center select-none"
										style:background-color={cellAspect ? `${cellAspect.color}15` : 'transparent'}
									>
										{#if cellAspect}
											<div class="flex flex-col items-center justify-center leading-tight">
												<span class="text-xs font-bold" style:color={cellAspect.color}>
													{cellAspect.symbol}
												</span>
												<span
													class="font-mono text-[8px] opacity-75"
													style:color={cellAspect.color}
												>
													{cellAspect.orbStr}
												</span>
											</div>
										{/if}
									</td>
								{/each}
								<!-- Self Diagonal Cell -->
								<td class="h-8 w-8 border border-white/15 bg-white/5 p-1 text-center">
									<span class="text-xs font-bold text-white">{body.symbol}</span>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>

		<!-- RIGHT: ELEMENT X MODALITY GRID (CAR, FIX, MUT X FIR, EAR, AIR, WAT) -->
		<div class="flex flex-col gap-3 lg:col-span-4">
			<div class="flex items-center gap-2">
				<span class="material-symbols-outlined text-sm text-secondary">category</span>
				<h4 class="font-headline text-sm font-semibold text-on-surface">
					{$locale === 'my' ? 'ဓာတ်သဘောနှင့် စရိုက်လက္ခဏာခွဲခြမ်းမှု' : 'Elements & Modalities'}
				</h4>
			</div>

			<div class="rounded-2xl border border-white/10 bg-surface-container-high/30 p-4">
				<table class="font-mono-data w-full border-collapse text-xs">
					<thead>
						<tr class="border-b border-white/10 text-[11px] text-on-surface-variant">
							<th class="p-2 text-left"></th>
							<th class="p-2 text-center">
								CAR <span class="font-bold text-primary"
									>({elementModalityMatrix.colTotals.cardinal})</span
								>
							</th>
							<th class="p-2 text-center">
								FIX <span class="font-bold text-primary"
									>({elementModalityMatrix.colTotals.fixed})</span
								>
							</th>
							<th class="p-2 text-center">
								MUT <span class="font-bold text-primary"
									>({elementModalityMatrix.colTotals.mutable})</span
								>
							</th>
						</tr>
					</thead>
					<tbody>
						<!-- FIRE -->
						<tr class="border-b border-white/5">
							<td class="p-2 font-bold text-red-400">
								FIR <span class="text-[10px] font-normal text-on-surface-variant"
									>({elementModalityMatrix.rowTotals.fire})</span
								>
							</td>
							<td class="border-l border-white/5 p-2 text-center text-sm">
								{elementModalityMatrix.matrix.fire.cardinal.map((b) => b.symbol).join(' ')}
							</td>
							<td class="border-l border-white/5 p-2 text-center text-sm">
								{elementModalityMatrix.matrix.fire.fixed.map((b) => b.symbol).join(' ')}
							</td>
							<td class="border-l border-white/5 p-2 text-center text-sm">
								{elementModalityMatrix.matrix.fire.mutable.map((b) => b.symbol).join(' ')}
							</td>
						</tr>
						<!-- EARTH -->
						<tr class="border-b border-white/5">
							<td class="p-2 font-bold text-emerald-400">
								EAR <span class="text-[10px] font-normal text-on-surface-variant"
									>({elementModalityMatrix.rowTotals.earth})</span
								>
							</td>
							<td class="border-l border-white/5 p-2 text-center text-sm">
								{elementModalityMatrix.matrix.earth.cardinal.map((b) => b.symbol).join(' ')}
							</td>
							<td class="border-l border-white/5 p-2 text-center text-sm">
								{elementModalityMatrix.matrix.earth.fixed.map((b) => b.symbol).join(' ')}
							</td>
							<td class="border-l border-white/5 p-2 text-center text-sm">
								{elementModalityMatrix.matrix.earth.mutable.map((b) => b.symbol).join(' ')}
							</td>
						</tr>
						<!-- AIR -->
						<tr class="border-b border-white/5">
							<td class="p-2 font-bold text-amber-400">
								AIR <span class="text-[10px] font-normal text-on-surface-variant"
									>({elementModalityMatrix.rowTotals.air})</span
								>
							</td>
							<td class="border-l border-white/5 p-2 text-center text-sm">
								{elementModalityMatrix.matrix.air.cardinal.map((b) => b.symbol).join(' ')}
							</td>
							<td class="border-l border-white/5 p-2 text-center text-sm">
								{elementModalityMatrix.matrix.air.fixed.map((b) => b.symbol).join(' ')}
							</td>
							<td class="border-l border-white/5 p-2 text-center text-sm">
								{elementModalityMatrix.matrix.air.mutable.map((b) => b.symbol).join(' ')}
							</td>
						</tr>
						<!-- WATER -->
						<tr>
							<td class="p-2 font-bold text-blue-400">
								WAT <span class="text-[10px] font-normal text-on-surface-variant"
									>({elementModalityMatrix.rowTotals.water})</span
								>
							</td>
							<td class="border-l border-white/5 p-2 text-center text-sm">
								{elementModalityMatrix.matrix.water.cardinal.map((b) => b.symbol).join(' ')}
							</td>
							<td class="border-l border-white/5 p-2 text-center text-sm">
								{elementModalityMatrix.matrix.water.fixed.map((b) => b.symbol).join(' ')}
							</td>
							<td class="border-l border-white/5 p-2 text-center text-sm">
								{elementModalityMatrix.matrix.water.mutable.map((b) => b.symbol).join(' ')}
							</td>
						</tr>
					</tbody>
				</table>
			</div>

			<!-- LEGEND OF ASPECTS -->
			<div
				class="font-mono-data flex flex-col gap-1.5 rounded-2xl border border-white/10 bg-surface-container-high/20 p-3 text-[11px]"
			>
				<span class="font-semibold text-on-surface-variant">
					{$locale === 'my' ? 'ထောင့်ချိတ်ဆက်မှုသင်္ကေတများ (Aspects)' : 'Major Aspects Legend'}
				</span>
				<div class="grid grid-cols-2 gap-1.5 text-[10px]">
					<div class="flex items-center gap-1.5 text-blue-400">
						<span class="text-sm font-bold">△</span>
						<span>Trine (120°)</span>
					</div>
					<div class="flex items-center gap-1.5 text-red-400">
						<span class="text-sm font-bold">□</span>
						<span>Square (90°)</span>
					</div>
					<div class="flex items-center gap-1.5 text-sky-400">
						<span class="text-sm font-bold">✱</span>
						<span>Sextile (60°)</span>
					</div>
					<div class="flex items-center gap-1.5 text-rose-500">
						<span class="text-sm font-bold">☍</span>
						<span>Opposition (180°)</span>
					</div>
					<div class="col-span-2 flex items-center gap-1.5 text-amber-400">
						<span class="text-sm font-bold">☌</span>
						<span>Conjunction (0°)</span>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- 0° TO 30° IN-SIGN DEGREE DISTRIBUTION RULER (BOTTOM OF PHOTO 5) -->
	<div class="flex flex-col gap-2 border-t border-white/10 pt-4">
		<div class="font-mono-data flex items-center justify-between text-xs text-on-surface-variant">
			<span
				>{$locale === 'my'
					? 'ရာသီခွင်အတွင်း ဒီဂရီပြန့်ကျဲမှု (0° - 30° Ruler)'
					: 'In-Sign Planetary Degree Distribution (0° - 30°)'}</span
			>
			<span>0° &rarr; 30°</span>
		</div>

		<div class="relative h-20 w-full px-4 select-none">
			<!-- Horizontal Axis line -->
			<div class="absolute right-4 bottom-2 left-4 h-0.5 bg-slate-600"></div>

			<!-- Major Tick marks 0, 5, 10, 15, 20, 25, 30 -->
			{#each [0, 5, 10, 15, 20, 25, 30] as deg (deg)}
				{@const pct = (deg / 30) * 100}
				<div
					class="absolute bottom-0 flex flex-col items-center"
					style:left="calc(1rem + {pct}% * 0.88)"
				>
					<div class="h-3 w-0.5 bg-slate-400"></div>
					<span class="font-mono-data mt-0.5 text-[9px] text-slate-400">{deg}°</span>
				</div>
			{/each}

			<!-- Plotted Bodies on the Ruler -->
			{#each allBodies as body (body.id)}
				{@const pct = ((body.signDeg + body.signMin / 60) / 30) * 100}
				<div
					class="group absolute bottom-5 flex -translate-x-1/2 cursor-pointer flex-col items-center transition-transform hover:z-20 hover:scale-125"
					style:left="calc(1rem + {pct}% * 0.88)"
					title="{body.name}: {body.signDeg}°{body.signMin}' ({body.sign})"
				>
					<span class="font-mono-data mb-0.5 text-[9px] font-semibold text-slate-300"
						>{body.signDeg}°</span
					>
					<span class="text-sm font-bold text-white drop-shadow">{body.symbol}</span>
					<div class="mt-0.5 h-2 w-px border-l border-dashed border-slate-500"></div>
				</div>
			{/each}
		</div>
	</div>
</div>
