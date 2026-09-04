<script lang="ts">
	import { ZODIAC_SYMBOLS, ELEMENT_COLORS } from '$lib/types';

	let { sign, element, size = 'md' }: { sign: string; element?: string; size?: 'sm' | 'md' | 'lg' } = $props();

	const symbol = $derived(ZODIAC_SYMBOLS[sign] || '\u2606');
	const elemColor = $derived(element ? ELEMENT_COLORS[element] : '#9333ea');
	const sizeClass = $derived(
		size === 'sm' ? 'w-8 h-8 text-sm' :
		size === 'lg' ? 'w-16 h-16 text-3xl' :
		'w-12 h-12 text-xl'
	);
</script>

<div
	class="zodiac-badge {sizeClass} rounded-full flex items-center justify-center font-bold border-2 transition-all hover:scale-110"
	style:background-color="{elemColor}20"
	style:border-color="{elemColor}60"
	style:color="{elemColor}"
	style:text-shadow="0 0 10px {elemColor}"
>
	{symbol}
</div>
