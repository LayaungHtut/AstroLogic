<script lang="ts">
	import { t } from '$lib/i18n';

	const techStack = $derived([
		{ name: 'SvelteKit 5', role: $t('about.stackFrontend'), icon: 'web' },
		{ name: 'TypeScript', role: $t('about.stackTypes'), icon: 'code' },
		{ name: 'Tailwind CSS', role: $t('about.stackStyling'), icon: 'palette' },
		{ name: 'Python FastAPI', role: $t('about.stackApi'), icon: 'dns' },
		{ name: 'SWI-Prolog', role: $t('about.stackReasoning'), icon: 'psychology' },
		{ name: 'OpenRouter', role: $t('about.stackLlm'), icon: 'smart_toy' },
		{ name: 'SQLite', role: $t('about.stackDb'), icon: 'database' }
	]);

	const architecture = $derived([
		{
			label: $t('about.layerUi'),
			desc: $t('about.layerUiDesc'),
			color: 'text-primary',
			bg: 'bg-primary/15',
			border: 'border-primary/40'
		},
		{
			label: $t('about.layerApi'),
			desc: $t('about.layerApiDesc'),
			color: 'text-secondary',
			bg: 'bg-secondary/15',
			border: 'border-secondary/40'
		},
		{
			label: $t('about.layerLogic'),
			desc: $t('about.layerLogicDesc'),
			color: 'text-tertiary',
			bg: 'bg-tertiary/15',
			border: 'border-tertiary/40'
		},
		{
			label: $t('about.layerAi'),
			desc: $t('about.layerAiDesc'),
			color: 'text-secondary',
			bg: 'bg-secondary/15',
			border: 'border-secondary/40'
		},
		{
			label: $t('about.layerDb'),
			desc: $t('about.layerDbDesc'),
			color: 'text-primary',
			bg: 'bg-primary/15',
			border: 'border-primary/40'
		}
	]);
</script>

<svelte:head>
	<title>{$t('about.title')} - AstroLogic</title>
</svelte:head>

<div class="page-container">
	<div class="page-header flex flex-col items-center gap-3 text-center">
		<span class="font-mono-data text-xs tracking-widest text-on-surface-variant/80 uppercase"
			>{$t('about.doc')}</span
		>
		<div class="flex items-center gap-3">
			<span class="material-symbols-outlined text-3xl text-primary">info</span>
			<h1 class="font-headline text-3xl font-bold text-on-surface">{$t('about.title')}</h1>
		</div>
		<p class="mx-auto max-w-2xl text-on-surface-variant">
			{$t('about.subtitle')}
		</p>
	</div>

	<div class="mx-auto flex max-w-4xl flex-col gap-6">
		<div class="rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md">
			<h2 class="font-headline gradient-text mb-3 flex items-center gap-2 text-lg font-bold">
				<span class="material-symbols-outlined text-primary">rocket_launch</span>
				{$t('about.overview')}
			</h2>
			<p class="text-sm leading-relaxed text-on-surface-variant">
				{$t('about.overviewDesc')}
			</p>
			<p class="mt-3 text-xs text-on-surface-variant/70 italic">
				{$t('about.disclaimerText')}
			</p>
		</div>

		<div class="rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md">
			<h2 class="font-headline gradient-text mb-4 flex items-center gap-2 text-lg font-bold">
				<span class="material-symbols-outlined text-secondary">layers</span>
				{$t('about.techStack')}
			</h2>
			<div class="grid gap-3 md:grid-cols-2">
				{#each techStack as tech}
					<div class="flex items-center gap-3 rounded-xl bg-surface-container-high/60 p-3">
						<div
							class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-surface-container text-primary"
						>
							<span class="material-symbols-outlined text-lg">{tech.icon}</span>
						</div>
						<div>
							<div class="text-sm font-bold text-on-surface">{tech.name}</div>
							<div
								class="font-mono-data text-[11px] tracking-wide text-on-surface-variant/70 uppercase"
							>
								{tech.role}
							</div>
						</div>
					</div>
				{/each}
			</div>
		</div>

		<div class="rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md">
			<h2 class="font-headline gradient-text mb-4 flex items-center gap-2 text-lg font-bold">
				<span class="material-symbols-outlined text-tertiary">account_tree</span>
				{$t('about.architecture')}
			</h2>
			<div class="flex flex-col gap-3">
				{#each architecture as layer, i}
					<div class="flex items-center gap-4">
						<div
							class="h-9 w-9 rounded-full {layer.bg} border {layer.border} flex items-center justify-center text-sm font-bold {layer.color} shrink-0"
						>
							{i + 1}
						</div>
						<div class="min-w-0 flex-1 rounded-xl bg-surface-container-high/60 p-3">
							<div class="text-sm font-bold text-on-surface">{layer.label}</div>
							<div class="text-xs text-on-surface-variant">{layer.desc}</div>
						</div>
						{#if i < architecture.length - 1}
							<span class="material-symbols-outlined shrink-0 text-on-surface-variant/40"
								>south</span
							>
						{/if}
					</div>
				{/each}
			</div>
		</div>

		<div class="rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md">
			<h2 class="font-headline gradient-text mb-3 flex items-center gap-2 text-lg font-bold">
				<span class="material-symbols-outlined text-primary">psychology</span>
				{$t('about.prologRole')}
			</h2>
			<p class="mb-3 text-sm leading-relaxed text-on-surface-variant">
				{$t('about.roleDesc')}
			</p>
			<ul class="space-y-2 text-sm text-on-surface-variant/90">
				<li class="flex items-center gap-2">
					<span class="material-symbols-outlined text-base text-secondary">chevron_right</span>
					{$t('about.role1')}
				</li>
				<li class="flex items-center gap-2">
					<span class="material-symbols-outlined text-base text-secondary">chevron_right</span>
					{$t('about.role2')}
				</li>
				<li class="flex items-center gap-2">
					<span class="material-symbols-outlined text-base text-secondary">chevron_right</span>
					{$t('about.role3')}
				</li>
				<li class="flex items-center gap-2">
					<span class="material-symbols-outlined text-base text-secondary">chevron_right</span>
					{$t('about.role4')}
				</li>
				<li class="flex items-center gap-2">
					<span class="material-symbols-outlined text-base text-secondary">chevron_right</span>
					{$t('about.role5')}
				</li>
			</ul>
		</div>

		<div class="rounded-2xl bg-surface-container-lowest/80 p-6 shadow-xl backdrop-blur-md">
			<h2 class="font-headline gradient-text mb-3 flex items-center gap-2 text-lg font-bold">
				<span class="material-symbols-outlined text-error">warning</span>
				{$t('about.disclaimer')}
			</h2>
			<p class="text-sm text-on-surface-variant">
				{$t('about.disclaimerText')}
			</p>
		</div>
	</div>
</div>
