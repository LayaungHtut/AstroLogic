<script lang="ts">
	import { t } from '$lib/i18n';
</script>

<footer
	class="relative z-10 mt-16 w-full border-t border-outline-variant/20 bg-surface-container-lowest/90 py-12 backdrop-blur-xl"
>
	<div
		class="mx-auto flex max-w-7xl flex-col items-center justify-between gap-6 px-6 md:flex-row lg:px-12"
	>
		<div class="flex items-center gap-4">
			<div
				class="font-mono-data inline-flex items-center gap-2 rounded-full border border-secondary/30 bg-surface-container-high/80 px-3 py-1 text-[10px] tracking-widest text-secondary uppercase"
			>
				<span class="h-1.5 w-1.5 animate-pulse rounded-full bg-secondary shadow-[0_0_6px_#4cd7f6]"
				></span>
				<span>{$t('footer.engineActive')}</span>
			</div>
			<span class="text-sm text-on-surface-variant">{$t('footer.copyright')}</span>
		</div>
		<nav class="flex flex-wrap items-center justify-center gap-6 text-sm">
			<a class="text-on-surface-variant transition-colors hover:text-on-surface" href="/birth-chart"
				>{$t('footer.ephemeris')}</a
			>
			<a class="text-on-surface-variant transition-colors hover:text-on-surface" href="/tarot"
				>{$t('footer.arcana')}</a
			>
			<a class="text-on-surface-variant transition-colors hover:text-on-surface" href="/chat"
				>{$t('footer.oracleDocs')}</a
			>
			<a class="text-on-surface-variant transition-colors hover:text-on-surface" href="/about"
				>{$t('footer.about')}</a
			>
		</nav>
		<p class="max-w-xs text-center text-sm text-on-surface-variant/70 md:text-right">
			{$t('footer.disclaimer')}
		</p>
	</div>
</footer>
