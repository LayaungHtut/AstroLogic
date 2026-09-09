<script lang="ts">
	import { ELEMENT_COLORS, ELEMENT_ICONS } from '$lib/types';
	import { locale, formatElement } from '$lib/i18n';

	let { element, size = 'md' }: { element: string; size?: 'sm' | 'md' | 'lg' } = $props();

	const color = $derived(ELEMENT_COLORS[element] || '#9333ea');
	const icon = $derived(ELEMENT_ICONS[element] || '\u2728');
	const sizeClass = $derived(
		size === 'sm'
			? 'text-xs px-2 py-0.5'
			: size === 'lg'
				? 'text-base px-4 py-2'
				: 'text-sm px-3 py-1'
	);
	const localizedElement = $derived(formatElement(element, $locale));
</script>

<span
	class="element-badge {sizeClass} inline-flex items-center gap-1.5 rounded-full border font-medium capitalize"
	style:background-color="{color}15"
	style:border-color="{color}40"
	style:color
>
	<span>{icon}</span>
	<span>{localizedElement}</span>
</span>
