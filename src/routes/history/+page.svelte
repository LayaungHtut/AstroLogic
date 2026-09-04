<script lang="ts">
	import { onMount } from 'svelte';
	import { fetchHistory, deleteReading } from '$lib/utils/api';
	import type { HistoryItem } from '$lib/types';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import MarkdownText from '$lib/components/MarkdownText.svelte';

	let items = $state<HistoryItem[]>([]);
	let loading = $state(true);
	let expandedId = $state<number | null>(null);

	onMount(async () => {
		try {
			items = await fetchHistory();
		} catch {
			// API may not be running
		} finally {
			loading = false;
		}
	});

	async function handleDelete(id: number) {
		try {
			await deleteReading(id);
			items = items.filter((i) => i.id !== id);
		} catch {
			// ignore
		}
	}

	function toggleExpand(id: number) {
		expandedId = expandedId === id ? null : id;
	}
</script>

<svelte:head>
	<title>Reading History - AstroLogic</title>
</svelte:head>

<div class="page-container">
	<div class="page-header flex flex-col gap-2">
		<span class="font-mono-data text-xs tracking-widest text-on-surface-variant/80 uppercase"
			>Archival Log • Chronological Record</span
		>
		<div class="flex items-center gap-3">
			<span class="material-symbols-outlined text-3xl text-primary">history</span>
			<h1 class="font-headline text-3xl font-bold text-on-surface">
				Reading <span class="gradient-text">History</span>
			</h1>
		</div>
		<p class="text-on-surface-variant">
			Review your past tarot readings and revisit their symbolic insights.
		</p>
	</div>

	{#if loading}
		<LoadingSpinner text="Loading history..." />
	{:else if items.length === 0}
		<div
			class="rounded-2xl bg-surface-container-lowest/80 p-12 text-center shadow-xl backdrop-blur-md"
		>
			<span class="material-symbols-outlined mb-4 text-5xl text-on-surface-variant/60"
				>inventory_2</span
			>
			<h2 class="font-headline mb-2 text-lg font-bold text-on-surface">No Readings Yet</h2>
			<p class="mb-4 text-on-surface-variant">Your reading history will appear here.</p>
			<a href="/reading" class="btn-primary inline-block">Start a Reading</a>
		</div>
	{:else}
		<div class="relative">
			<div
				class="absolute top-2 bottom-2 left-5 hidden w-px bg-gradient-to-b from-primary/40 via-secondary/20 to-transparent sm:block"
			></div>
			<div class="flex flex-col gap-3">
				{#each items as item (item.id)}
					<div class="relative sm:pl-12">
						<div
							class="absolute top-6 left-[13px] hidden h-3 w-3 rounded-full bg-secondary shadow-[0_0_10px_rgba(76,215,246,0.6)] sm:block"
						></div>
						<div
							class="overflow-hidden rounded-2xl bg-surface-container-lowest/80 shadow-xl backdrop-blur-md transition-all"
						>
							<button
								class="flex w-full items-center justify-between gap-4 p-4 text-left transition-colors hover:bg-surface-container-high/40 sm:p-5"
								onclick={() => toggleExpand(item.id)}
							>
								<div class="min-w-0 flex-1">
									<div class="truncate font-medium text-on-surface">
										{item.question || 'Tarot Reading'}
									</div>
									<div class="mt-2 flex flex-wrap items-center gap-2">
										<span
											class="font-mono-data inline-flex items-center gap-1 rounded-full bg-surface-container-high px-2.5 py-1 text-[11px] tracking-wider text-primary uppercase"
										>
											{item.zodiac_sign}
										</span>
										<span
											class="font-mono-data inline-flex items-center gap-1 rounded-full bg-surface-container-high px-2.5 py-1 text-[11px] tracking-wider text-secondary uppercase"
										>
											{item.category}
										</span>
										<span
											class="font-mono-data inline-flex items-center gap-1 rounded-full bg-surface-container-high px-2.5 py-1 text-[11px] tracking-wider text-tertiary uppercase"
										>
											{item.spread_type}
										</span>
										<span
											class="font-mono-data ml-auto text-[11px] text-on-surface-variant/70 sm:ml-0"
										>
											{item.created_at}
										</span>
									</div>
								</div>
								<span
									class="material-symbols-outlined shrink-0 text-on-surface-variant/60 transition-transform {expandedId ===
									item.id
										? 'rotate-90'
										: ''}">chevron_right</span
								>
							</button>

							{#if expandedId === item.id}
								<div class="border-t border-outline-variant/20 p-4 sm:p-5">
									<div class="flex flex-col gap-2 rounded-xl bg-surface-container-low p-4">
										<div class="flex items-center gap-2 text-secondary">
											<span class="material-symbols-outlined text-base">auto_awesome</span>
											<span
												class="font-mono-data text-[11px] font-semibold tracking-wider uppercase"
												>AI Interpretation</span
											>
										</div>
										<MarkdownText
											content={item.ai_interpretation}
											class="text-sm text-on-surface/90"
										/>
									</div>
									<div class="mt-4 flex justify-end gap-3">
										<a
											href="/reasoning/{item.id}"
											class="font-body-sm inline-flex items-center gap-1.5 rounded-full bg-surface-container px-3 py-1.5 text-sm text-on-surface transition-colors hover:bg-surface-container-high"
										>
											<span class="material-symbols-outlined text-base">psychology</span>
											View Reasoning
										</a>
										<button
											class="font-body-sm inline-flex items-center gap-1.5 rounded-full bg-error-container/30 px-3 py-1.5 text-sm text-error transition-colors hover:bg-error-container/50"
											onclick={() => handleDelete(item.id)}
										>
											<span class="material-symbols-outlined text-base">delete</span>
											Delete
										</button>
									</div>
								</div>
							{/if}
						</div>
					</div>
				{/each}
			</div>
		</div>
	{/if}
</div>
