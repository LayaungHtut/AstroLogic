<script lang="ts">
	import type { ReasoningStep } from '$lib/types';

	let { step, index = 0 }: { step: ReasoningStep; index?: number } = $props();
</script>

<div class="reasoning-step flex items-start gap-3 p-3 rounded-lg bg-surface-container-low/70 border border-white/10 transition-all hover:bg-surface-container-high/70" style:animation-delay="{index * 100}ms">
	<div class="flex-shrink-0 w-6 h-6 rounded-full bg-secondary/15 border border-secondary/40 flex items-center justify-center text-secondary text-xs font-bold">
		✓
	</div>
	<div class="flex-1 min-w-0">
		<div class="text-xs text-secondary font-mono-data truncate">{step.rule}</div>
		<div class="text-sm text-on-surface/90 mt-0.5">{step.result}</div>
	</div>
</div>
