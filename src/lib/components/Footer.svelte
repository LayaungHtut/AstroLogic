<script lang="ts">
	import { t } from '$lib/i18n';
</script>

<footer class="relative z-10 w-full bg-surface-container-lowest/90 backdrop-blur-xl border-t border-outline-variant/20 py-12 mt-16">
	<div class="max-w-7xl mx-auto px-6 lg:px-12 flex flex-col md:flex-row items-center justify-between gap-6">
		<div class="flex items-center gap-4">
			<div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-container-high/80 border border-secondary/30 font-mono-data text-[10px] uppercase text-secondary tracking-widest">
				<span class="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse shadow-[0_0_6px_#4cd7f6]"></span>
				<span>{$t('footer.engineActive')}</span>
			</div>
			<span class="text-on-surface-variant text-sm">{$t('footer.copyright')}</span>
		</div>
		<nav class="flex flex-wrap items-center justify-center gap-6 text-sm">
			<a class="text-on-surface-variant hover:text-on-surface transition-colors" href="/birth-chart">{$t('footer.ephemeris')}</a>
			<a class="text-on-surface-variant hover:text-on-surface transition-colors" href="/tarot">{$t('footer.arcana')}</a>
			<a class="text-on-surface-variant hover:text-on-surface transition-colors" href="/chat">{$t('footer.oracleDocs')}</a>
			<a class="text-on-surface-variant hover:text-on-surface transition-colors" href="/about">{$t('footer.about')}</a>
		</nav>
		<p class="text-on-surface-variant/70 text-sm text-center md:text-right max-w-xs">
			{$t('footer.disclaimer')}
		</p>
	</div>
</footer>
