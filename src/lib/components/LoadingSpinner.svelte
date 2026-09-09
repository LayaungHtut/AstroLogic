<script lang="ts">
	let { text = 'Loading...' }: { text?: string } = $props();
</script>

<div class="loading-spinner flex flex-col items-center justify-center gap-3 py-8">
	<div class="relative h-12 w-12">
		<div class="absolute inset-0 rounded-full border-2 border-primary-container/20"></div>
		<div
			class="absolute inset-0 animate-spin rounded-full border-2 border-transparent border-t-primary"
		></div>
		<div
			class="absolute inset-1 animate-spin rounded-full border border-transparent border-t-secondary"
			style:animation-duration="1.5s"
		></div>
	</div>
	<p class="font-mono-data animate-pulse text-sm text-on-surface-variant">{text}</p>
</div>
