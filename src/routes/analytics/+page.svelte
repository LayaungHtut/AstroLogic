<script lang="ts">
	import { onMount } from 'svelte';
	import { fetchAnalytics } from '$lib/utils/api';
	import type { AnalyticsData } from '$lib/types';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import { locale, t, getCardTranslation, formatElement, translateTopic } from '$lib/i18n';

	let data = $state<AnalyticsData | null>(null);
	let loading = $state(true);

	onMount(async () => {
		try {
			data = await fetchAnalytics();
		} catch {
			// API may not be running
		} finally {
			loading = false;
		}
	});

	function maxVal(items: { count: number }[]): number {
		if (items.length === 0) return 1;
		return Math.max(...items.map((i) => i.count), 1);
	}

	function pct(part: number, total: number): number {
		if (total <= 0) return 0;
		return Math.round((part / total) * 100);
	}

	function humanize(text: string | undefined): string {
		return (text ?? '').replace(/_/g, ' ');
	}

	function insightText(insight: import('$lib/types').AnalyticsInsight): string {
		if ($locale === 'my') {
			switch (insight.type) {
				case 'recurring_theme':
					return `"${humanize(insight.theme)}" ဟူသော သဘောတရားသည် ဗေဒင် ${insight.count} ကြိမ်တွင် ကျရောက်ခဲ့သည်။`;
				case 'suit_bias':
					return `သင့်ကတ်များ၏ ${Math.round((insight.proportion ?? 0) * 100)}% သည် ${humanize(insight.suit)} အုပ်စုဖြစ်ပြီး ${formatElement(insight.element, $locale)} အားကောင်းသော သင်္ကေတဖြစ်သည်။`;
				case 'reversal_bias':
					return insight.bias === 'mostly_reversed'
						? 'မကြာသေးမီက ကျရောက်သော ကတ်အများစုသည် ဇောက်ထိုး (Reversed) ဖြစ်နေသည် — စွမ်းအင်များ ပိတ်ဆို့နေခြင်း သို့မဟုတ် အတွင်းစိတ်သို့ လှည့်နေခြင်း ဖြစ်နိုင်သည်။'
						: 'မကြာသေးမီက ကျရောက်သော ကတ်အများစုသည် ပုံမှန် (Upright) ဖြစ်နေသည် — စွမ်းအင်များ လွတ်လပ်စွာ စီးဆင်းနေသည်။';
				case 'category_suit_bias':
					return `သင့်၏ "${translateTopic(insight.category, $locale)}" ဗေဒင်များတွင် ${humanize(insight.suit)} ကတ်များ မကြာခဏ ကျရောက်နေပြီး သတိပြုဖွယ် ${formatElement(insight.element, $locale)} လက္ခဏာတစ်ခု ဖြစ်သည်။`;
				default:
					return insight.rule;
			}
		}
		switch (insight.type) {
			case 'recurring_theme':
				return `The theme "${humanize(insight.theme)}" has come up in ${insight.count} readings.`;
			case 'suit_bias':
				return `${Math.round((insight.proportion ?? 0) * 100)}% of your cards have been ${humanize(insight.suit)} — a strong ${humanize(insight.element)} leaning.`;
			case 'reversal_bias':
				return insight.bias === 'mostly_reversed'
					? 'Most of your recent cards have landed reversed — energy may feel blocked or turned inward.'
					: 'Most of your recent cards have landed upright — energy has been flowing freely.';
			case 'category_suit_bias':
				return `Your "${humanize(insight.category)}" readings keep drawing ${humanize(insight.suit)} — a ${humanize(insight.element)} pattern worth noticing.`;
			default:
				return insight.rule;
		}
	}
</script>

<svelte:head>
	<title>{$t('analytics.title')} - {$t('brand.name')}</title>
</svelte:head>

<div class="page-container">
	<div class="page-header flex flex-col gap-2">
		<span class="font-mono-data text-xs tracking-widest text-on-surface-variant/80 uppercase"
			>{$t('analytics.telemetryDigest')}</span
		>
		<div class="flex items-center gap-3">
			<span class="material-symbols-outlined text-3xl text-secondary">monitoring</span>
			<h1 class="font-headline text-3xl font-bold text-on-surface">{$t('analytics.title')}</h1>
		</div>
		<p class="text-on-surface-variant">{$t('analytics.subtitle')}</p>
	</div>

	{#if loading}
		<LoadingSpinner text={$t('common.loading')} />
	{:else if !data || data.total_readings === 0}
		<div
			class="rounded-2xl bg-surface-container-lowest/80 p-12 text-center shadow-xl backdrop-blur-md"
		>
			<span class="material-symbols-outlined mb-4 text-5xl text-on-surface-variant/60"
				>bar_chart</span
			>
			<h2 class="font-headline mb-2 text-lg font-bold text-on-surface">{$t('analytics.noData')}</h2>
			<p class="mb-4 text-on-surface-variant">{$t('analytics.noDataDesc')}</p>
			<a href="/reading" class="btn-primary inline-block">{$t('history.startReading')}</a>
		</div>
	{:else}
		<!-- Top Stat Tiles -->
		<div class="mb-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
			<div
				class="flex flex-col items-center gap-2 rounded-2xl bg-surface-container-lowest/80 p-5 text-center shadow-xl backdrop-blur-md"
			>
				<span class="material-symbols-outlined text-2xl text-primary">auto_stories</span>
				<div class="font-headline gradient-text text-3xl font-extrabold">{data.total_readings}</div>
				<div class="font-mono-data text-[11px] tracking-wider text-on-surface-variant/70 uppercase">
					{$t('analytics.totalReadings')}
				</div>
			</div>
			<div
				class="flex flex-col items-center gap-2 rounded-2xl bg-surface-container-lowest/80 p-5 text-center shadow-xl backdrop-blur-md"
			>
				<span class="material-symbols-outlined text-2xl text-secondary">style</span>
				<div class="font-headline text-lg font-bold text-on-surface capitalize">
					{data.most_common_suit}
				</div>
				<div class="font-mono-data text-[11px] tracking-wider text-on-surface-variant/70 uppercase">
					{$t('analytics.commonSuit')}
				</div>
			</div>
			<div
				class="flex flex-col items-center gap-2 rounded-2xl bg-surface-container-lowest/80 p-5 text-center shadow-xl backdrop-blur-md"
			>
				<span class="material-symbols-outlined text-2xl text-tertiary">insights</span>
				<div class="font-headline text-lg font-bold text-on-surface">
					{data.major_vs_minor.major} / {data.major_vs_minor.minor}
				</div>
				<div class="font-mono-data text-[11px] tracking-wider text-on-surface-variant/70 uppercase">
					{$t('analytics.arcanaRatio')}
				</div>
			</div>
			<div
				class="flex flex-col items-center gap-2 rounded-2xl bg-surface-container-lowest/80 p-5 text-center shadow-xl backdrop-blur-md"
			>
				<span class="material-symbols-outlined text-2xl text-secondary">sync_alt</span>
				<div class="font-headline text-lg font-bold text-on-surface">
					{data.upright_vs_reversed.upright} / {data.upright_vs_reversed.reversed}
				</div>
				<div class="font-mono-data text-[11px] tracking-wider text-on-surface-variant/70 uppercase">
					{$t('analytics.reversalRatio')}
				</div>
			</div>
		</div>

		<!-- Distribution Bars: Major vs Minor, Upright vs Reversed -->
		<div class="mb-6 grid gap-4 md:grid-cols-2">
			<div class="flex flex-col gap-3 rounded-2xl bg-surface-container-low p-6 shadow-lg">
				<div class="font-mono-data flex items-center justify-between text-xs">
					<span class="flex items-center gap-1.5 tracking-wider text-on-surface-variant uppercase">
						<span class="material-symbols-outlined text-sm">pie_chart</span>
						{$t('analytics.arcanaBalance')}
					</span>
					<span class="font-medium text-primary"
						>{$locale === 'my' ? 'အဓိကကတ်' : 'Major'}
						{pct(
							data.major_vs_minor.major,
							data.major_vs_minor.major + data.major_vs_minor.minor
						)}%</span
					>
				</div>
				<div
					class="flex h-3 w-full overflow-hidden rounded-full bg-surface-container-highest shadow-inner"
				>
					<div
						class="h-full bg-primary"
						style:width="{pct(
							data.major_vs_minor.major,
							data.major_vs_minor.major + data.major_vs_minor.minor
						)}%"
						title="Major: {data.major_vs_minor.major}"
					></div>
					<div
						class="h-full bg-tertiary"
						style:width="{pct(
							data.major_vs_minor.minor,
							data.major_vs_minor.major + data.major_vs_minor.minor
						)}%"
						title="Minor: {data.major_vs_minor.minor}"
					></div>
				</div>
				<div
					class="font-mono-data flex items-center justify-between text-[11px] text-on-surface-variant uppercase"
				>
					<span class="flex items-center gap-1"
						><span class="h-1.5 w-1.5 rounded-full bg-primary"></span>
						{$locale === 'my' ? 'အဓိကကတ်' : 'Major'}
						{data.major_vs_minor.major}</span
					>
					<span class="flex items-center gap-1"
						><span class="h-1.5 w-1.5 rounded-full bg-tertiary"></span>
						{$locale === 'my' ? 'သာမန်ကတ်' : 'Minor'}
						{data.major_vs_minor.minor}</span
					>
				</div>
			</div>

			<div class="flex flex-col gap-3 rounded-2xl bg-surface-container-low p-6 shadow-lg">
				<div class="font-mono-data flex items-center justify-between text-xs">
					<span class="flex items-center gap-1.5 tracking-wider text-on-surface-variant uppercase">
						<span class="material-symbols-outlined text-sm">swap_vert</span>
						{$t('analytics.orientationBalance')}
					</span>
					<span class="font-medium text-secondary"
						>{$locale === 'my' ? 'ပုံမှန်' : 'Upright'}
						{pct(
							data.upright_vs_reversed.upright,
							data.upright_vs_reversed.upright + data.upright_vs_reversed.reversed
						)}%</span
					>
				</div>
				<div
					class="flex h-3 w-full overflow-hidden rounded-full bg-surface-container-highest shadow-inner"
				>
					<div
						class="h-full bg-secondary-container"
						style:width="{pct(
							data.upright_vs_reversed.upright,
							data.upright_vs_reversed.upright + data.upright_vs_reversed.reversed
						)}%"
						title="Upright: {data.upright_vs_reversed.upright}"
					></div>
					<div
						class="h-full bg-outline"
						style:width="{pct(
							data.upright_vs_reversed.reversed,
							data.upright_vs_reversed.upright + data.upright_vs_reversed.reversed
						)}%"
						title="Reversed: {data.upright_vs_reversed.reversed}"
					></div>
				</div>
				<div
					class="font-mono-data flex items-center justify-between text-[11px] text-on-surface-variant uppercase"
				>
					<span class="flex items-center gap-1"
						><span class="h-1.5 w-1.5 rounded-full bg-secondary-container"></span>
						{$locale === 'my' ? 'ပုံမှန်' : 'Upright'}
						{data.upright_vs_reversed.upright}</span
					>
					<span class="flex items-center gap-1"
						><span class="h-1.5 w-1.5 rounded-full bg-outline"></span>
						{$locale === 'my' ? 'ဇောက်ထိုး' : 'Reversed'}
						{data.upright_vs_reversed.reversed}</span
					>
				</div>
			</div>
		</div>

		{#if data.insights && data.insights.length > 0}
			<div
				class="mb-6 rounded-2xl border border-primary/20 bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md"
			>
				<h3
					class="font-mono-data mb-4 flex items-center gap-2 text-xs font-semibold tracking-wider text-on-surface-variant uppercase"
				>
					<span class="material-symbols-outlined text-base text-primary">psychology</span>
					{$t('analytics.patternInsights')}
				</h3>
				<div class="flex flex-col gap-3">
					{#each data.insights as insight}
						<div class="flex items-start gap-3 text-sm">
							<span class="material-symbols-outlined mt-0.5 text-base text-tertiary"
								>auto_awesome</span
							>
							<div>
								<p class="text-on-surface">{insightText(insight)}</p>
								<p class="font-mono-data mt-0.5 text-[10px] text-on-surface-variant/60">
									{insight.rule}
								</p>
							</div>
						</div>
					{/each}
				</div>
			</div>
		{/if}

		{#if data.most_drawn_cards.length > 0}
			<div class="mb-6 rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md">
				<h3
					class="font-mono-data mb-4 flex items-center gap-2 text-xs font-semibold tracking-wider text-on-surface-variant uppercase"
				>
					<span class="material-symbols-outlined text-base text-primary">style</span>
					{$t('analytics.mostDrawnCards')}
				</h3>
				<div class="flex flex-col gap-3">
					{#each data.most_drawn_cards as item}
						<div class="flex items-center gap-3">
							<div class="w-40 truncate text-sm text-on-surface-variant capitalize">
								{getCardTranslation(item.card, $locale).name || item.card.replace(/_/g, ' ')}
							</div>
							<div class="h-3 flex-1 overflow-hidden rounded-full bg-surface-container-highest">
								<div
									class="h-full rounded-full bg-gradient-to-r from-primary to-secondary transition-all"
									style:width="{(item.count / maxVal(data.most_drawn_cards)) * 100}%"
								></div>
							</div>
							<div class="font-mono-data w-8 text-right text-xs text-on-surface-variant">
								{item.count}
							</div>
						</div>
					{/each}
				</div>
			</div>
		{/if}

		<div class="grid gap-6 md:grid-cols-2">
			{#if data.most_common_themes.length > 0}
				<div class="rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md">
					<h3
						class="font-mono-data mb-4 flex items-center gap-2 text-xs font-semibold tracking-wider text-on-surface-variant uppercase"
					>
						<span class="material-symbols-outlined text-base text-tertiary">token</span>
						{$t('analytics.mostCommonThemes')}
					</h3>
					<div class="flex flex-wrap gap-2">
						{#each data.most_common_themes as item}
							<span
								class="rounded-full border border-tertiary/30 bg-surface-container-high px-3 py-1 text-sm text-tertiary"
							>
								{item.theme.replace(/_/g, ' ')}
								<span class="font-mono-data text-on-surface-variant/70">({item.count})</span>
							</span>
						{/each}
					</div>
				</div>
			{/if}

			{#if data.most_common_categories.length > 0}
				<div class="rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md">
					<h3
						class="font-mono-data mb-4 flex items-center gap-2 text-xs font-semibold tracking-wider text-on-surface-variant uppercase"
					>
						<span class="material-symbols-outlined text-base text-secondary">category</span>
						{$t('analytics.questionCategories')}
					</h3>
					<div class="flex flex-col gap-3">
						{#each data.most_common_categories as item}
							<div class="flex items-center gap-3">
								<div class="w-32 text-sm text-on-surface-variant capitalize">
									{translateTopic(item.category, $locale)}
								</div>
								<div class="h-3 flex-1 overflow-hidden rounded-full bg-surface-container-highest">
									<div
										class="h-full rounded-full bg-gradient-to-r from-secondary to-tertiary transition-all"
										style:width="{(item.count / maxVal(data.most_common_categories)) * 100}%"
									></div>
								</div>
								<div class="font-mono-data w-8 text-right text-xs text-on-surface-variant">
									{item.count}
								</div>
							</div>
						{/each}
					</div>
				</div>
			{/if}
		</div>
	{/if}
</div>
