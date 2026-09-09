<script lang="ts">
	import { locale } from '$lib/i18n';

	let { class: className = '' }: { class?: string } = $props();

	function select(lang: 'en' | 'my') {
		locale.setLocale(lang);
	}
</script>

<div
	class="inline-flex items-center p-0.5 rounded-full bg-surface-container-high/80 border border-white/10 shadow-inner backdrop-blur-md transition-all {className}"
	role="group"
	aria-label="Language Selector"
>
	<button
		type="button"
		onclick={() => select('en')}
		class="px-2.5 py-1 rounded-full text-xs font-medium transition-all duration-200 flex items-center gap-1 {$locale === 'en'
			? 'bg-gradient-to-r from-primary to-secondary text-white font-semibold shadow-[0_0_12px_rgba(76,215,246,0.4)]'
			: 'text-on-surface-variant hover:text-on-surface hover:bg-white/5'}"
		aria-pressed={$locale === 'en'}
	>
		<span>EN</span>
	</button>
	<button
		type="button"
		onclick={() => select('my')}
		class="px-2.5 py-1 rounded-full text-xs font-medium transition-all duration-200 flex items-center gap-1 {$locale === 'my'
			? 'bg-gradient-to-r from-primary to-secondary text-white font-semibold shadow-[0_0_12px_rgba(76,215,246,0.4)]'
			: 'text-on-surface-variant hover:text-on-surface hover:bg-white/5'}"
		aria-pressed={$locale === 'my'}
	>
		<span>မြန်မာ</span>
	</button>
</div>
