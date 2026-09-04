<script lang="ts">
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { fetchReading } from '$lib/utils/api';
	import type { ReadingResult } from '$lib/types';
	import ReasoningStep from '$lib/components/ReasoningStep.svelte';
	import MarkdownText from '$lib/components/MarkdownText.svelte';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';

	let reading = $state<ReadingResult | null>(null);
	let loading = $state(true);

	onMount(async () => {
		const id = page.params.id;
		if (id) {
			try {
				reading = await fetchReading(parseInt(id));
			} catch {
				// API may not be running
			} finally {
				loading = false;
			}
		} else {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>Reasoning - AstroLogic</title>
</svelte:head>

<div class="page-container">
	<div class="page-header flex flex-col gap-2">
		<span class="font-mono-data text-xs tracking-widest text-on-surface-variant/80 uppercase"
			>Inspection Focus • Symbolic Trace Viewer</span
		>
		<div class="flex items-center gap-3">
			<span class="material-symbols-outlined text-3xl text-secondary">psychology</span>
			<h1 class="font-headline text-3xl font-bold text-on-surface">
				Prolog <span class="gradient-text">Reasoning</span>
			</h1>
		</div>
		<p class="text-on-surface-variant">How did AstroLogic reach this result?</p>
	</div>

	{#if loading}
		<LoadingSpinner text="Loading reasoning..." />
	{:else if !reading}
		<div
			class="rounded-2xl bg-surface-container-lowest/80 p-12 text-center shadow-xl backdrop-blur-md"
		>
			<span class="material-symbols-outlined mb-4 text-5xl text-on-surface-variant/60"
				>psychology_alt</span
			>
			<h2 class="font-headline mb-2 text-lg font-bold text-on-surface">No Reading Found</h2>
			<p class="mb-4 text-on-surface-variant">Complete a reading to see its reasoning process.</p>
			<a href="/reading" class="btn-primary inline-block">Start a Reading</a>
		</div>
	{:else}
		<div class="mx-auto flex max-w-3xl flex-col gap-6">
			<div class="rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md">
				<h2 class="font-headline mb-2 flex items-center gap-2 text-lg font-bold text-on-surface">
					<span class="material-symbols-outlined text-xl text-primary">summarize</span>
					Reading Summary
				</h2>
				<div class="mb-3 text-sm text-on-surface-variant italic">"{reading.question}"</div>
				<div class="flex flex-wrap gap-2">
					<span
						class="font-mono-data inline-flex items-center gap-1 rounded-full bg-surface-container-high px-2.5 py-1 text-[11px] tracking-wider text-primary uppercase"
						>{reading.zodiac_sign}</span
					>
					<span
						class="font-mono-data inline-flex items-center gap-1 rounded-full bg-surface-container-high px-2.5 py-1 text-[11px] tracking-wider text-secondary uppercase"
						>{reading.spread_type}</span
					>
					<span
						class="font-mono-data inline-flex items-center gap-1 rounded-full bg-surface-container-high px-2.5 py-1 text-[11px] tracking-wider text-tertiary uppercase"
						>{reading.category}</span
					>
				</div>
			</div>

			{#if reading.cards.length > 0}
				<div class="rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md">
					<h3
						class="font-mono-data mb-3 flex items-center gap-2 text-xs font-semibold tracking-wider text-on-surface-variant uppercase"
					>
						<span class="material-symbols-outlined text-base text-primary">style</span>
						Cards Drawn
					</h3>
					<div class="grid grid-cols-2 gap-3 md:grid-cols-4">
						{#each reading.cards as card}
							<div class="rounded-xl bg-surface-container-high/60 p-3 text-center">
								<div class="text-sm font-bold text-on-surface">{card.name}</div>
								<div class="mt-0.5 text-xs text-secondary">{card.position}</div>
								<div
									class="font-mono-data mt-1 text-[11px] tracking-wide text-on-surface-variant/70 uppercase"
								>
									{card.is_reversed ? 'Reversed' : 'Upright'}
								</div>
							</div>
						{/each}
					</div>
				</div>
			{/if}

			{#if reading.themes.length > 0}
				<div class="rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md">
					<h3
						class="font-mono-data mb-3 flex items-center gap-2 text-xs font-semibold tracking-wider text-on-surface-variant uppercase"
					>
						<span class="material-symbols-outlined text-base text-tertiary">token</span>
						Extracted Themes
					</h3>
					<div class="flex flex-wrap gap-2">
						{#each reading.themes as theme}
							<span
								class="rounded-full border border-tertiary/30 bg-surface-container-high px-3 py-1 text-sm text-tertiary"
							>
								{theme.replace(/_/g, ' ')}
							</span>
						{/each}
					</div>
				</div>
			{/if}

			{#if reading.ai_interpretation}
				<div class="flex flex-col gap-3 rounded-xl bg-surface-container-low p-5">
					<div class="flex items-center gap-2 text-secondary">
						<span class="material-symbols-outlined text-lg">auto_awesome</span>
						<span class="font-mono-data text-xs font-semibold tracking-wider uppercase"
							>AI Socratic Synthesis</span
						>
					</div>
					<MarkdownText content={reading.ai_interpretation} class="text-sm" />
				</div>
			{/if}

			{#if reading.reasoning.length > 0}
				<div class="rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md">
					<h3
						class="font-mono-data mb-4 flex items-center gap-2 text-xs font-semibold tracking-wider text-on-surface-variant uppercase"
					>
						<span class="material-symbols-outlined text-base text-secondary">account_tree</span>
						Reasoning Trace
					</h3>
					<div class="relative">
						<div
							class="absolute top-0 bottom-0 left-5 w-px bg-gradient-to-b from-primary/50 to-transparent"
						></div>
						<div class="flex flex-col gap-3">
							{#each reading.reasoning as step, i}
								<ReasoningStep {step} index={i} />
							{/each}
						</div>
					</div>
				</div>
			{/if}
		</div>
	{/if}
</div>
