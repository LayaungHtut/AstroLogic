<script lang="ts">
	import type { ReasoningStep } from '$lib/types';
	import { locale, formatTraceResult } from '$lib/i18n';

	let { step, index = 0 }: { step: ReasoningStep; index?: number } = $props();
</script>

<div
	class="reasoning-step flex items-start gap-3 rounded-lg border border-white/10 bg-surface-container-low/70 p-3 transition-all hover:bg-surface-container-high/70"
	style:animation-delay="{index * 100}ms"
>
	<div
		class="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full border border-secondary/40 bg-secondary/15 text-xs font-bold text-secondary"
	>
		✓
	</div>
	<div class="min-w-0 flex-1">
		<div class="font-mono-data truncate text-xs text-secondary">{step.rule}</div>
		<div class="mt-0.5 text-sm text-on-surface/90">{formatTraceResult(step.result, $locale)}</div>
	</div>
</div>
