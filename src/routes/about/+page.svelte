<script lang="ts">
	const techStack = [
		{ name: 'SvelteKit 5', role: 'Frontend Framework', icon: 'web' },
		{ name: 'TypeScript', role: 'Type Safety', icon: 'code' },
		{ name: 'Tailwind CSS', role: 'UI Styling', icon: 'palette' },
		{ name: 'Python FastAPI', role: 'Backend API', icon: 'dns' },
		{ name: 'SWI-Prolog', role: 'Symbolic Reasoning', icon: 'psychology' },
		{ name: 'OpenRouter', role: 'LLM Integration', icon: 'smart_toy' },
		{ name: 'SQLite', role: 'Local Persistence', icon: 'database' },
	];

	const architecture = [
		{ label: 'User Interface', desc: 'SvelteKit 5 frontend with Tailwind CSS', color: 'text-primary', bg: 'bg-primary/15', border: 'border-primary/40' },
		{ label: 'API Layer', desc: 'Python FastAPI REST endpoints', color: 'text-secondary', bg: 'bg-secondary/15', border: 'border-secondary/40' },
		{ label: 'Symbolic Reasoning', desc: 'SWI-Prolog knowledge base and inference', color: 'text-tertiary', bg: 'bg-tertiary/15', border: 'border-tertiary/40' },
		{ label: 'AI Interpretation', desc: 'OpenRouter LLM for natural language', color: 'text-secondary', bg: 'bg-secondary/15', border: 'border-secondary/40' },
		{ label: 'Persistence', desc: 'SQLite local database', color: 'text-primary', bg: 'bg-primary/15', border: 'border-primary/40' },
	];
</script>

<svelte:head>
	<title>About - AstroLogic</title>
</svelte:head>

<div class="page-container">
	<div class="page-header text-center flex flex-col items-center gap-3">
		<span class="font-mono-data text-xs uppercase tracking-widest text-on-surface-variant/80">Observatory Documentation</span>
		<div class="flex items-center gap-3">
			<span class="material-symbols-outlined text-primary text-3xl">info</span>
			<h1 class="font-headline text-3xl font-bold text-on-surface">About <span class="gradient-text">AstroLogic</span></h1>
		</div>
		<p class="text-on-surface-variant max-w-2xl mx-auto">
			An AI-powered Zodiac, Tarot, and Horoscope application combining symbolic Prolog reasoning with modern web technologies.
		</p>
	</div>

	<div class="max-w-4xl mx-auto flex flex-col gap-6">
		<div class="p-6 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl">
			<h2 class="font-headline text-lg font-bold mb-3 gradient-text flex items-center gap-2">
				<span class="material-symbols-outlined text-primary">rocket_launch</span>
				Project Overview
			</h2>
			<p class="text-on-surface-variant text-sm leading-relaxed">
				AstroLogic is an entertainment and self-reflection application that demonstrates the integration of
				symbolic AI reasoning (Prolog) with natural language AI (LLM) in a modern web application. It provides
				tarot readings, horoscope generation, zodiac compatibility analysis, and an AI conversational assistant.
			</p>
			<p class="text-on-surface-variant/70 text-xs mt-3 italic">
				This application is for entertainment purposes only. Astrology and tarot do not scientifically predict
				the future or diagnose conditions.
			</p>
		</div>

		<div class="p-6 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl">
			<h2 class="font-headline text-lg font-bold mb-4 gradient-text flex items-center gap-2">
				<span class="material-symbols-outlined text-secondary">layers</span>
				Technology Stack
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
				Architecture
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
				The Role of Prolog
			</h2>
			<p class="text-on-surface-variant text-sm leading-relaxed mb-3">
				SWI-Prolog is used as the symbolic reasoning engine. It maintains a knowledge base of zodiac signs,
				tarot cards, elements, modalities, and ruling planets. Prolog inference rules determine:
			</p>
			<ul class="text-on-surface-variant/90 text-sm space-y-2">
				<li class="flex items-center gap-2"><span class="material-symbols-outlined text-secondary text-base">chevron_right</span> Question classification and category matching</li>
				<li class="flex items-center gap-2"><span class="material-symbols-outlined text-secondary text-base">chevron_right</span> Tarot spread recommendation based on question type</li>
				<li class="flex items-center gap-2"><span class="material-symbols-outlined text-secondary text-base">chevron_right</span> Zodiac compatibility evaluation</li>
				<li class="flex items-center gap-2"><span class="material-symbols-outlined text-secondary text-base">chevron_right</span> Card interpretation and thematic extraction</li>
				<li class="flex items-center gap-2"><span class="material-symbols-outlined text-secondary text-base">chevron_right</span> Complete reasoning traces for explainability</li>
			</ul>
		</div>

		<div class="p-6 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-md shadow-xl">
			<h2 class="font-headline text-lg font-bold mb-3 gradient-text flex items-center gap-2">
				<span class="material-symbols-outlined text-error">warning</span>
				Disclaimer
			</h2>
			<p class="text-on-surface-variant text-sm">
				AstroLogic is designed for entertainment and personal reflection. It does not claim that astrology
				or tarot scientifically predicts the future, diagnoses personality traits, or provides medical,
				health, or relationship advice. All readings should be considered symbolic and reflective in nature.
			</p>
		</div>
	</div>
</div>
