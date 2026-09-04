<script lang="ts">
	let { count = 50 }: { count?: number } = $props();

	const stars = $derived(
		Array.from({ length: count }, (_, i) => ({
			id: i,
			x: Math.random() * 100,
			y: Math.random() * 100,
			size: Math.random() * 2 + 0.5,
			opacity: Math.random() * 0.8 + 0.2,
			duration: Math.random() * 3 + 2
		}))
	);
</script>

<div class="star-field fixed inset-0 pointer-events-none overflow-hidden z-0">
	{#each stars as star (star.id)}
		<div
			class="absolute rounded-full bg-white"
			style:left="{star.x}%"
			style:top="{star.y}%"
			style:width="{star.size}px"
			style:height="{star.size}px"
			style:opacity="{star.opacity}"
			style:animation="twinkle {star.duration}s ease-in-out infinite"
		></div>
	{/each}
</div>

<style>
	@keyframes twinkle {
		0%, 100% { opacity: 0.2; }
		50% { opacity: 1; }
	}
</style>
