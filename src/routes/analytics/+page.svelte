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
		return Math.max(...items.map(i => i.count), 1);
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
		<span class="font-mono-data text-xs uppercase tracking-widest text-on-surface-variant/80">{$t('analytics.telemetryDigest')}</span>
		<div class="flex items-center gap-3">
			<span class="material-symbols-outlined text-secondary text-3xl">monitoring</span>
			<h1 class="font-headline text-3xl font-bold text-on-surface">{$t('analytics.title')}</h1>
		</div>
		<p class="text-on-surface-variant">{$t('analytics.subtitle')}</p>
	</div>

	{#if loading}
		<LoadingSpinner text={$t('common.loading')} />
	{:else if !data || data.total_readings === 0}
		<div class="rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl p-12 text-center">
			<span class="material-symbols-outlined text-5xl text-on-surface-variant/60 mb-4">bar_chart</span>
			<h2 class="font-headline text-lg font-bold mb-2 text-on-surface">{$t('analytics.noData')}</h2>
			<p class="text-on-surface-variant mb-4">{$t('analytics.noDataDesc')}</p>
			<a href="/reading" class="btn-primary inline-block">{$t('history.startReading')}</a>
		</div>
	{:else}
		<!-- Top Stat Tiles -->
		<div class="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
			<div class="p-5 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl flex flex-col items-center text-center gap-2">
				<span class="material-symbols-outlined text-primary text-2xl">auto_stories</span>
				<div class="font-headline text-3xl font-extrabold gradient-text">{data.total_readings}</div>
				<div class="font-mono-data text-[11px] text-on-surface-variant/70 uppercase tracking-wider">{$t('analytics.totalReadings')}</div>
			</div>
			<div class="p-5 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl flex flex-col items-center text-center gap-2">
				<span class="material-symbols-outlined text-secondary text-2xl">style</span>
				<div class="font-headline text-lg font-bold text-on-surface capitalize">{data.most_common_suit}</div>
				<div class="font-mono-data text-[11px] text-on-surface-variant/70 uppercase tracking-wider">{$t('analytics.commonSuit')}</div>
			</div>
			<div class="p-5 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl flex flex-col items-center text-center gap-2">
				<span class="material-symbols-outlined text-tertiary text-2xl">insights</span>
				<div class="font-headline text-lg font-bold text-on-surface">{data.major_vs_minor.major} / {data.major_vs_minor.minor}</div>
				<div class="font-mono-data text-[11px] text-on-surface-variant/70 uppercase tracking-wider">{$t('analytics.arcanaRatio')}</div>
			</div>
			<div class="p-5 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl flex flex-col items-center text-center gap-2">
				<span class="material-symbols-outlined text-secondary text-2xl">sync_alt</span>
				<div class="font-headline text-lg font-bold text-on-surface">{data.upright_vs_reversed.upright} / {data.upright_vs_reversed.reversed}</div>
				<div class="font-mono-data text-[11px] text-on-surface-variant/70 uppercase tracking-wider">{$t('analytics.reversalRatio')}</div>
			</div>
		</div>

		<!-- Distribution Bars: Major vs Minor, Upright vs Reversed -->
		<div class="grid md:grid-cols-2 gap-4 mb-6">
			<div class="p-6 rounded-2xl bg-surface-container-low shadow-lg flex flex-col gap-3">
				<div class="flex items-center justify-between font-mono-data text-xs">
					<span class="text-on-surface-variant uppercase tracking-wider flex items-center gap-1.5">
						<span class="material-symbols-outlined text-sm">pie_chart</span>
						{$t('analytics.arcanaBalance')}
					</span>
					<span class="text-primary font-medium">{$locale === 'my' ? 'အဓိကကတ်' : 'Major'} {pct(data.major_vs_minor.major, data.major_vs_minor.major + data.major_vs_minor.minor)}%</span>
				</div>
				<div class="w-full h-3 rounded-full bg-surface-container-highest overflow-hidden flex shadow-inner">
					<div class="h-full bg-primary" style:width="{pct(data.major_vs_minor.major, data.major_vs_minor.major + data.major_vs_minor.minor)}%" title="Major: {data.major_vs_minor.major}"></div>
					<div class="h-full bg-tertiary" style:width="{pct(data.major_vs_minor.minor, data.major_vs_minor.major + data.major_vs_minor.minor)}%" title="Minor: {data.major_vs_minor.minor}"></div>
				</div>
				<div class="flex items-center justify-between text-on-surface-variant font-mono-data text-[11px] uppercase">
					<span class="flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-primary"></span> {$locale === 'my' ? 'အဓိကကတ်' : 'Major'} {data.major_vs_minor.major}</span>
					<span class="flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-tertiary"></span> {$locale === 'my' ? 'သာမန်ကတ်' : 'Minor'} {data.major_vs_minor.minor}</span>
				</div>
			</div>

			<div class="p-6 rounded-2xl bg-surface-container-low shadow-lg flex flex-col gap-3">
				<div class="flex items-center justify-between font-mono-data text-xs">
					<span class="text-on-surface-variant uppercase tracking-wider flex items-center gap-1.5">
						<span class="material-symbols-outlined text-sm">swap_vert</span>
						{$t('analytics.orientationBalance')}
					</span>
					<span class="text-secondary font-medium">{$locale === 'my' ? 'ပုံမှန်' : 'Upright'} {pct(data.upright_vs_reversed.upright, data.upright_vs_reversed.upright + data.upright_vs_reversed.reversed)}%</span>
				</div>
				<div class="w-full h-3 rounded-full bg-surface-container-highest overflow-hidden flex shadow-inner">
					<div class="h-full bg-secondary-container" style:width="{pct(data.upright_vs_reversed.upright, data.upright_vs_reversed.upright + data.upright_vs_reversed.reversed)}%" title="Upright: {data.upright_vs_reversed.upright}"></div>
					<div class="h-full bg-outline" style:width="{pct(data.upright_vs_reversed.reversed, data.upright_vs_reversed.upright + data.upright_vs_reversed.reversed)}%" title="Reversed: {data.upright_vs_reversed.reversed}"></div>
				</div>
				<div class="flex items-center justify-between text-on-surface-variant font-mono-data text-[11px] uppercase">
					<span class="flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-secondary-container"></span> {$locale === 'my' ? 'ပုံမှန်' : 'Upright'} {data.upright_vs_reversed.upright}</span>
					<span class="flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-outline"></span> {$locale === 'my' ? 'ဇောက်ထိုး' : 'Reversed'} {data.upright_vs_reversed.reversed}</span>
				</div>
			</div>
		</div>

		{#if data.insights && data.insights.length > 0}
			<div class="p-6 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl mb-6 border border-primary/20">
				<h3 class="font-mono-data text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-4 flex items-center gap-2">
					<span class="material-symbols-outlined text-base text-primary">psychology</span>
					{$t('analytics.patternInsights')}
				</h3>
				<div class="flex flex-col gap-3">
					{#each data.insights as insight}
						<div class="flex items-start gap-3 text-sm">
							<span class="material-symbols-outlined text-base text-tertiary mt-0.5">auto_awesome</span>
							<div>
								<p class="text-on-surface">{insightText(insight)}</p>
								<p class="font-mono-data text-[10px] text-on-surface-variant/60 mt-0.5">{insight.rule}</p>
							</div>
						</div>
					{/each}
				</div>
			</div>
		{/if}

		{#if data.most_drawn_cards.length > 0}
			<div class="p-6 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl mb-6">
				<h3 class="font-mono-data text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-4 flex items-center gap-2">
					<span class="material-symbols-outlined text-base text-primary">style</span>
					{$t('analytics.mostDrawnCards')}
				</h3>
				<div class="flex flex-col gap-3">
					{#each data.most_drawn_cards as item}
						<div class="flex items-center gap-3">
							<div class="text-sm text-on-surface-variant w-40 truncate capitalize">{getCardTranslation(item.card, $locale).name || item.card.replace(/_/g, ' ')}</div>
							<div class="flex-1 h-3 rounded-full bg-surface-container-highest overflow-hidden">
								<div
									class="h-full bg-gradient-to-r from-primary to-secondary rounded-full transition-all"
									style:width="{(item.count / maxVal(data.most_drawn_cards)) * 100}%"
								></div>
							</div>
							<div class="font-mono-data text-xs text-on-surface-variant w-8 text-right">{item.count}</div>
						</div>
					{/each}
				</div>
			</div>
		{/if}

		<div class="grid md:grid-cols-2 gap-6">
			{#if data.most_common_themes.length > 0}
				<div class="p-6 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl">
					<h3 class="font-mono-data text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-4 flex items-center gap-2">
						<span class="material-symbols-outlined text-base text-tertiary">token</span>
						{$t('analytics.mostCommonThemes')}
					</h3>
					<div class="flex flex-wrap gap-2">
						{#each data.most_common_themes as item}
							<span class="text-sm px-3 py-1 rounded-full bg-surface-container-high text-tertiary border border-tertiary/30">
								{item.theme.replace(/_/g, ' ')} <span class="font-mono-data text-on-surface-variant/70">({item.count})</span>
							</span>
						{/each}
					</div>
				</div>
			{/if}

			{#if data.most_common_categories.length > 0}
				<div class="p-6 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl">
					<h3 class="font-mono-data text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-4 flex items-center gap-2">
						<span class="material-symbols-outlined text-base text-secondary">category</span>
						{$t('analytics.questionCategories')}
					</h3>
					<div class="flex flex-col gap-3">
						{#each data.most_common_categories as item}
							<div class="flex items-center gap-3">
								<div class="text-sm text-on-surface-variant w-32 capitalize">{translateTopic(item.category, $locale)}</div>
								<div class="flex-1 h-3 rounded-full bg-surface-container-highest overflow-hidden">
									<div
										class="h-full bg-gradient-to-r from-secondary to-tertiary rounded-full transition-all"
										style:width="{(item.count / maxVal(data.most_common_categories)) * 100}%"
									></div>
								</div>
								<div class="font-mono-data text-xs text-on-surface-variant w-8 text-right">{item.count}</div>
							</div>
						{/each}
					</div>
				</div>
			{/if}
		</div>
	{/if}
</div>
