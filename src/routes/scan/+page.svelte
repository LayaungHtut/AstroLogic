<script lang="ts">
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import { locale, t, getCardTranslation, translateKeyword } from '$lib/i18n';

	interface ScanResult {
		card_name: string;
		orientation: string;
		confidence: string;
		keywords: string[];
		brief_interpretation: string;
		upright_meaning: string;
		reversed_meaning: string;
		error?: string;
	}

	let file = $state<File | null>(null);
	let preview = $state('');
	let result = $state<ScanResult | null>(null);
	let loading = $state(false);
	let error = $state('');
	let explaining = $state(false);
	let explanation = $state('');
	let dragActive = $state(false);

	function handleFileSelect(e: Event) {
		const input = e.target as HTMLInputElement;
		if (input.files && input.files[0]) {
			file = input.files[0];
			preview = URL.createObjectURL(file);
			result = null;
			error = '';
			explanation = '';
		}
	}

	function handleDrop(e: DragEvent) {
		e.preventDefault();
		dragActive = false;
		if (e.dataTransfer?.files && e.dataTransfer.files[0]) {
			file = e.dataTransfer.files[0];
			preview = URL.createObjectURL(file);
			result = null;
			error = '';
			explanation = '';
		}
	}

	function handleDragOver(e: DragEvent) {
		e.preventDefault();
		dragActive = true;
	}

	function handleDragLeave(e: DragEvent) {
		e.preventDefault();
		dragActive = false;
	}

	async function scanCard() {
		if (!file) return;
		loading = true;
		error = '';
		result = null;
		explanation = '';

		try {
			const formData = new FormData();
			formData.append('file', file);

			const res = await fetch('http://localhost:8000/api/tarot-scan/identify', {
				method: 'POST',
				body: formData
			});
			const data = await res.json();
			result = data as ScanResult;

			if (result && result.error) {
				error = result.error;
				result = null;
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to scan image';
		} finally {
			loading = false;
		}
	}

	async function getExplanation() {
		if (!result || !result.card_name) return;
		explaining = true;
		try {
			const res = await fetch('http://localhost:8000/api/tarot-scan/explain', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					card_name: result.card_name,
					orientation: result.orientation || 'upright'
				})
			});
			const data = await res.json();
			explanation = data.explanation || '';
		} catch {
			explanation = 'Could not generate explanation.';
		} finally {
			explaining = false;
		}
	}

	function reset() {
		file = null;
		preview = '';
		result = null;
		error = '';
		explanation = '';
	}
</script>

<svelte:head>
	<title>{$t('scan.title')} - {$t('brand.name')}</title>
</svelte:head>

<div class="page-container">
	<!-- Atmospheric glow orbs -->
	<div
		class="pointer-events-none absolute -top-10 left-0 h-96 w-96 rounded-full bg-primary-container/20 blur-[120px]"
	></div>
	<div
		class="pointer-events-none absolute top-1/3 right-0 h-80 w-80 rounded-full bg-secondary-container/15 blur-[110px]"
	></div>

	<div class="page-header relative">
		<div
			class="mb-3 inline-flex items-center gap-2 rounded-full bg-surface-container-high/60 px-3 py-1 backdrop-blur-md"
		>
			<span class="h-1.5 w-1.5 animate-ping rounded-full bg-secondary"></span>
			<span class="font-mono-data text-[11px] tracking-widest text-secondary uppercase">
				{$locale === 'my'
					? 'ကင်မရာ အမြင်အာရုံ စနစ် အသင့်ရှိသည်'
					: 'Optical Telemetry • Vision Array Active'}
			</span>
		</div>
		<h1 class="font-headline text-3xl font-extrabold">{$t('scan.title')}</h1>
		<p class="text-on-surface-variant">{$t('scan.subtitle')}</p>
	</div>

	<div class="relative mx-auto max-w-2xl">
		{#if !preview}
			<!-- Scanner Aperture Drop Zone -->
			<div class="glass-card p-6 shadow-xl">
				<div class="mb-4 flex items-center justify-between">
					<div class="flex items-center gap-2">
						<span class="material-symbols-outlined text-[18px] text-secondary"
							>filter_center_focus</span
						>
						<span class="font-mono-data text-xs tracking-wider text-secondary uppercase"
							>Optical Aperture</span
						>
					</div>
					<div class="font-mono-data flex items-center gap-1.5 text-xs text-on-surface-variant">
						<span class="inline-block h-2 w-2 rounded-full bg-secondary"></span>
						<span>READY</span>
					</div>
				</div>

				<div
					class="relative flex min-h-[320px] cursor-pointer flex-col items-center justify-center overflow-hidden rounded-lg border-2 border-dashed p-8 text-center transition-colors duration-300 {dragActive
						? 'border-secondary bg-surface-container-high/40'
						: 'border-outline-variant bg-surface-container-lowest/80 hover:border-primary/50'}"
					ondrop={handleDrop}
					ondragover={handleDragOver}
					ondragleave={handleDragLeave}
					role="button"
					tabindex="0"
				>
					<!-- Corner brackets -->
					<span
						class="pointer-events-none absolute top-3 left-3 h-4 w-4 border-t-2 border-l-2 border-secondary/60"
					></span>
					<span
						class="pointer-events-none absolute top-3 right-3 h-4 w-4 border-t-2 border-r-2 border-secondary/60"
					></span>
					<span
						class="pointer-events-none absolute bottom-3 left-3 h-4 w-4 border-b-2 border-l-2 border-secondary/60"
					></span>
					<span
						class="pointer-events-none absolute right-3 bottom-3 h-4 w-4 border-r-2 border-b-2 border-secondary/60"
					></span>

					<div class="relative z-10 flex flex-col items-center gap-3">
						<div
							class="relative flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-tr from-primary-container/40 to-secondary-container/40 text-secondary shadow-lg"
						>
							<span class="material-symbols-outlined text-3xl">add_a_photo</span>
							<span class="absolute -inset-1 animate-ping rounded-full bg-secondary/15"></span>
						</div>
						<div class="mt-1 space-y-1">
							<p class="font-headline text-lg font-bold text-on-surface">
								{$t('scan.dropzoneTitle')}
							</p>
							<p class="max-w-xs text-sm text-on-surface-variant">{$t('scan.dropzoneHint')}</p>
							<p class="text-xs text-on-surface-variant/70">JPG, PNG, WebP (Max 10MB)</p>
						</div>
						<div class="mt-2 flex items-center gap-2">
							<span
								class="font-mono-data rounded bg-surface-container px-2.5 py-1 text-[11px] text-on-surface-variant"
								>JPG</span
							>
							<span
								class="font-mono-data rounded bg-surface-container px-2.5 py-1 text-[11px] text-on-surface-variant"
								>PNG</span
							>
							<span
								class="font-mono-data rounded bg-surface-container px-2.5 py-1 text-[11px] text-on-surface-variant"
								>WEBP</span
							>
						</div>
						<input
							type="file"
							accept="image/*"
							class="hidden"
							id="file-input"
							onchange={handleFileSelect}
						/>
						<label for="file-input" class="btn-primary mt-2 inline-block cursor-pointer">
							{$locale === 'my' ? 'ဓာတ်ပုံရွေးချယ်မည်' : 'Choose Image'}
						</label>
					</div>
				</div>
			</div>
		{:else}
			<div class="glass-card mb-6 p-6">
				<div class="mb-4 flex items-center justify-between">
					<h2 class="font-headline text-lg font-bold">
						{$locale === 'my' ? 'ထည့်သွင်းထားသော ဓာတ်ပုံ' : 'Uploaded Image'}
					</h2>
					<button class="text-sm text-on-surface-variant hover:text-on-surface" onclick={reset}>
						{$locale === 'my' ? 'ရှင်းလင်းမည်' : 'Clear'}
					</button>
				</div>
				<div class="flex justify-center">
					<img src={preview} alt="Tarot card" class="max-h-80 rounded-lg object-contain" />
				</div>
			</div>

			{#if !result && !loading}
				<button class="btn-primary w-full py-4 text-lg" onclick={scanCard}>
					{$t('scan.scanButton')}
				</button>
			{/if}

			{#if loading}
				<div class="glass-card p-4">
					<LoadingSpinner text={$t('scan.scanning')} />
				</div>
			{/if}

			{#if error}
				<div class="glass-card mb-6 border-error/30 bg-error-container/10 p-6">
					<p class="text-error">{error}</p>
					<button class="btn-secondary mt-3 text-sm" onclick={reset}>{$t('common.retry')}</button>
				</div>
			{/if}

			{#if result && !result.error}
				{@const cardTrans = getCardTranslation(result.card_name, $locale)}
				<div class="glass-card mb-6 overflow-hidden p-6">
					<div class="mb-4 flex items-center gap-3">
						<div
							class="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-primary-container to-secondary-container text-on-primary shadow-lg"
						>
							<span class="material-symbols-outlined text-2xl">
								{#if result.orientation === 'reversed'}swap_vert{:else}vertical_align_top{/if}
							</span>
						</div>
						<div>
							<h2 class="font-headline text-xl font-bold text-on-surface">
								{cardTrans.name || result.card_name}
							</h2>
							<p class="font-mono-data text-xs text-on-surface-variant capitalize">
								{result.orientation === 'reversed' ? $t('common.reversed') : $t('common.upright')} &bull;
								{$t('scan.confidence')}: {result.confidence}
							</p>
						</div>
					</div>

					{#if result.keywords && result.keywords.length > 0}
						<div class="mb-4">
							<h3
								class="font-mono-data mb-2 text-xs tracking-wider text-on-surface-variant uppercase"
							>
								{$t('deck.uprightKeywords')}
							</h3>
							<div class="flex flex-wrap gap-2">
								{#each result.keywords as keyword}
									<span
										class="font-mono-data rounded-full border border-primary/30 bg-primary-container/20 px-2.5 py-1 text-xs text-primary"
									>
										{translateKeyword(keyword, $locale)}
									</span>
								{/each}
							</div>
						</div>
					{/if}

					{#if result.brief_interpretation}
						<div class="mb-4 rounded-lg bg-surface-container-high/50 p-4">
							<h3 class="mb-2 text-sm font-semibold text-secondary">{$t('reading.aiSynthesis')}</h3>
							<p class="text-sm text-on-surface-variant">{result.brief_interpretation}</p>
						</div>
					{/if}

					{#if result.upright_meaning || cardTrans.meaningUpright}
						<div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
							<div
								class="relative overflow-hidden rounded-lg border border-secondary/20 bg-secondary/10 p-3 pl-4"
							>
								<span
									class="absolute top-0 bottom-0 left-0 w-1 bg-secondary shadow-[0_0_8px_var(--color-secondary)]"
								></span>
								<div class="mb-1 flex items-center gap-1.5 text-xs font-semibold text-secondary">
									<span class="material-symbols-outlined text-sm">check_circle</span>
									{$t('common.upright')}
								</div>
								<p class="text-xs text-on-surface-variant">
									{cardTrans.meaningUpright || result.upright_meaning}
								</p>
							</div>
							<div
								class="rounded-lg border border-outline-variant/40 bg-surface-container-lowest/60 p-3 opacity-80 transition-opacity hover:opacity-100"
							>
								<div
									class="mb-1 flex items-center gap-1.5 text-xs font-semibold text-on-surface-variant"
								>
									<span class="material-symbols-outlined text-sm">swap_vert</span>
									{$t('common.reversed')}
								</div>
								<p class="text-xs text-on-surface-variant">
									{cardTrans.meaningReversed || result.reversed_meaning}
								</p>
							</div>
						</div>
					{/if}
				</div>

				{#if !explanation && !explaining}
					<button class="btn-secondary w-full" onclick={getExplanation}>
						{$t('scan.explainButton')}
					</button>
				{/if}

				{#if explaining}
					<div class="glass-card p-2">
						<LoadingSpinner text={$t('common.loading')} />
					</div>
				{/if}

				{#if explanation}
					<div class="glass-card p-6">
						<h3
							class="font-mono-data mb-3 text-xs tracking-wider text-on-surface-variant uppercase"
						>
							{$t('scan.explanation')}
						</h3>
						<div class="text-sm whitespace-pre-wrap text-on-surface-variant">{explanation}</div>
					</div>
				{/if}
			{/if}
		{/if}
	</div>
</div>
