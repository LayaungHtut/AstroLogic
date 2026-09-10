<script lang="ts">
	import { locale } from '$lib/i18n';

	let { class: className = '' }: { class?: string } = $props();

	function select(lang: 'en' | 'my') {
		locale.setLocale(lang);
	}
</script>

<div
	class="inline-flex items-center rounded-full border border-white/10 bg-surface-container-high/80 p-0.5 shadow-inner backdrop-blur-md transition-all {className}"
	role="group"
	aria-label="Language Selector"
>
	<button
		type="button"
		onclick={() => select('en')}
		class="flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-medium transition-all duration-200 {$locale ===
		'en'
			? 'bg-gradient-to-r from-primary to-secondary font-semibold text-white shadow-[0_0_12px_rgba(76,215,246,0.4)]'
			: 'text-on-surface-variant hover:bg-white/5 hover:text-on-surface'}"
		aria-pressed={$locale === 'en'}
	>
		<span>EN</span>
	</button>
	<button
		type="button"
		onclick={() => select('my')}
		class="flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-medium transition-all duration-200 {$locale ===
		'my'
			? 'bg-gradient-to-r from-primary to-secondary font-semibold text-white shadow-[0_0_12px_rgba(76,215,246,0.4)]'
			: 'text-on-surface-variant hover:bg-white/5 hover:text-on-surface'}"
		aria-pressed={$locale === 'my'}
	>
		<span>မြန်မာ</span>
	</button>
</div>
