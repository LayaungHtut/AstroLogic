<script lang="ts">
	import { t } from '$lib/i18n';

	const techStack = $derived([
		{ name: 'SvelteKit 5', role: $t('about.stackFrontend'), icon: 'web' },
		{ name: 'TypeScript', role: $t('about.stackTypes'), icon: 'code' },
		{ name: 'Tailwind CSS', role: $t('about.stackStyling'), icon: 'palette' },
		{ name: 'Python FastAPI', role: $t('about.stackApi'), icon: 'dns' },
		{ name: 'SWI-Prolog', role: $t('about.stackReasoning'), icon: 'psychology' },
		{ name: 'OpenRouter', role: $t('about.stackLlm'), icon: 'smart_toy' },
		{ name: 'SQLite', role: $t('about.stackDb'), icon: 'database' },
	]);

	const architecture = $derived([
		{ label: $t('about.layerUi'), desc: $t('about.layerUiDesc'), color: 'text-primary', bg: 'bg-primary/15', border: 'border-primary/40' },
		{ label: $t('about.layerApi'), desc: $t('about.layerApiDesc'), color: 'text-secondary', bg: 'bg-secondary/15', border: 'border-secondary/40' },
		{ label: $t('about.layerLogic'), desc: $t('about.layerLogicDesc'), color: 'text-tertiary', bg: 'bg-tertiary/15', border: 'border-tertiary/40' },
		{ label: $t('about.layerAi'), desc: $t('about.layerAiDesc'), color: 'text-secondary', bg: 'bg-secondary/15', border: 'border-secondary/40' },
		{ label: $t('about.layerDb'), desc: $t('about.layerDbDesc'), color: 'text-primary', bg: 'bg-primary/15', border: 'border-primary/40' },
	]);
</script>

<svelte:head>
	<title>{$t('about.title')} - AstroLogic</title>
</svelte:head>

<div class="page-container">
	<div class="page-header text-center flex flex-col items-center gap-3">
		<span class="font-mono-data text-xs uppercase tracking-widest text-on-surface-variant/80">{$t('about.doc')}</span>
		<div class="flex items-center gap-3">
			<span class="material-symbols-outlined text-primary text-3xl">info</span>
			<h1 class="font-headline text-3xl font-bold text-on-surface">{$t('about.title')}</h1>
		</div>
		<p class="text-on-surface-variant max-w-2xl mx-auto">
			{$t('about.subtitle')}
		</p>
	</div>

	<div class="max-w-4xl mx-auto flex flex-col gap-6">
		<div class="p-6 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl">
			<h2 class="font-headline text-lg font-bold mb-3 gradient-text flex items-center gap-2">
				<span class="material-symbols-outlined text-primary">rocket_launch</span>
				{$t('about.overview')}
			</h2>
			<p class="text-on-surface-variant text-sm leading-relaxed">
				{$t('about.overviewDesc')}
			</p>
			<p class="text-on-surface-variant/70 text-xs mt-3 italic">
				{$t('about.disclaimerText')}
			</p>
		</div>

		<div class="p-6 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl">
			<h2 class="font-headline text-lg font-bold mb-4 gradient-text flex items-center gap-2">
				<span class="material-symbols-outlined text-secondary">layers</span>
				{$t('about.techStack')}
			</h2>
			<div class="grid md:grid-cols-2 gap-3">
				{#each techStack as tech}
					<div class="flex items-center gap-3 p-3 rounded-xl bg-surface-container-high/60">
						<div class="w-9 h-9 rounded-lg bg-surface-container flex items-center justify-center text-primary shrink-0">
							<span class="material-symbols-outlined text-lg">{tech.icon}</span>
						</div>
						<div>
							<div class="text-sm font-bold text-on-surface">{tech.name}</div>
							<div class="font-mono-data text-[11px] text-on-surface-variant/70 uppercase tracking-wide">{tech.role}</div>
						</div>
					</div>
				{/each}
			</div>
		</div>

		<div class="p-6 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl">
			<h2 class="font-headline text-lg font-bold mb-4 gradient-text flex items-center gap-2">
				<span class="material-symbols-outlined text-tertiary">account_tree</span>
				{$t('about.architecture')}
			</h2>
			<div class="flex flex-col gap-3">
				{#each architecture as layer, i}
					<div class="flex items-center gap-4">
						<div class="w-9 h-9 rounded-full {layer.bg} border {layer.border} flex items-center justify-center text-sm font-bold {layer.color} shrink-0">
							{i + 1}
						</div>
						<div class="flex-1 min-w-0 p-3 rounded-xl bg-surface-container-high/60">
							<div class="text-sm font-bold text-on-surface">{layer.label}</div>
							<div class="text-xs text-on-surface-variant">{layer.desc}</div>
						</div>
						{#if i < architecture.length - 1}
							<span class="material-symbols-outlined text-on-surface-variant/40 shrink-0">south</span>
						{/if}
					</div>
				{/each}
			</div>
		</div>

		<div class="p-6 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl">
			<h2 class="font-headline text-lg font-bold mb-3 gradient-text flex items-center gap-2">
				<span class="material-symbols-outlined text-primary">psychology</span>
				{$t('about.prologRole')}
			</h2>
			<p class="text-on-surface-variant text-sm leading-relaxed mb-3">
				{$t('about.roleDesc')}
			</p>
			<ul class="text-on-surface-variant/90 text-sm space-y-2">
				<li class="flex items-center gap-2"><span class="material-symbols-outlined text-secondary text-base">chevron_right</span> {$t('about.role1')}</li>
				<li class="flex items-center gap-2"><span class="material-symbols-outlined text-secondary text-base">chevron_right</span> {$t('about.role2')}</li>
				<li class="flex items-center gap-2"><span class="material-symbols-outlined text-secondary text-base">chevron_right</span> {$t('about.role3')}</li>
				<li class="flex items-center gap-2"><span class="material-symbols-outlined text-secondary text-base">chevron_right</span> {$t('about.role4')}</li>
				<li class="flex items-center gap-2"><span class="material-symbols-outlined text-secondary text-base">chevron_right</span> {$t('about.role5')}</li>
			</ul>
		</div>

		<div class="p-6 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl">
			<h2 class="font-headline text-lg font-bold mb-3 gradient-text flex items-center gap-2">
				<span class="material-symbols-outlined text-error">warning</span>
				{$t('about.disclaimer')}
			</h2>
			<p class="text-on-surface-variant text-sm">
				{$t('about.disclaimerText')}
			</p>
		</div>
	</div>
</div>
