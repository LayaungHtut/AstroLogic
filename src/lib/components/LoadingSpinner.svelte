<script lang="ts">
	let { text = 'Loading...' }: { text?: string } = $props();
</script>

<div class="loading-spinner flex flex-col items-center justify-center gap-3 py-8">
	<div class="relative w-12 h-12">
		<div class="absolute inset-0 rounded-full border-2 border-primary-container/20"></div>
		<div class="absolute inset-0 rounded-full border-2 border-transparent border-t-primary animate-spin"></div>
		<div class="absolute inset-1 rounded-full border border-transparent border-t-secondary animate-spin" style:animation-duration="1.5s"></div>
	</div>
	<p class="text-sm text-on-surface-variant animate-pulse font-mono-data">{text}</p>
</div>
