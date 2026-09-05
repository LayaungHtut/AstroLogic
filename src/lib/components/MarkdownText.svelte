<script lang="ts">
	let { content, class: className = '' }: { content: string; class?: string } = $props();

	function escapeHtml(value: string) {
		return value
			.replace(/&/g, '&amp;')
			.replace(/</g, '&lt;')
			.replace(/>/g, '&gt;')
			.replace(/"/g, '&quot;')
			.replace(/'/g, '&#039;');
	}

	function formatInline(value: string) {
		return value
			.replace(/\\([*_`])/g, '$1')
			.replace(
				/`([^`]+)`/g,
				'<code class="rounded bg-surface-container-high px-1 py-0.5 font-mono-data text-xs">$1</code>'
			)
			.replace(/\*\*([^*]+)\*\*/g, '<strong class="font-semibold text-on-surface">$1</strong>')
			.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>')
			.replace(/[\*_`]+/g, '');
	}

	function renderMarkdown(value: string) {
		const lines = escapeHtml(value).replace(/\r\n?/g, '\n').split('\n');
		const html = lines.map((line) => {
			if (!line.trim()) return '';
			if (line.startsWith('### '))
				return `<h4 class="mt-5 mb-2 font-headline text-base font-semibold text-on-surface">${formatInline(line.slice(4))}</h4>`;
			if (line.startsWith('## '))
				return `<h3 class="mt-5 mb-2 font-headline text-lg font-semibold text-on-surface">${formatInline(line.slice(3))}</h3>`;
			if (line.startsWith('# '))
				return `<h2 class="mt-5 mb-2 font-headline text-xl font-bold text-on-surface">${formatInline(line.slice(2))}</h2>`;
			if (/^[-*] /.test(line)) return `<li>${formatInline(line.slice(2))}</li>`;
			return `<p class="mb-3">${formatInline(line)}</p>`;
		});

		return html
			.join('\n')
			.replace(
				/(?:<li>.*?<\/li>\n?)+/g,
				(items) => `<ul class="mb-3 list-disc space-y-1 pl-5">${items}</ul>`
			);
	}

	let html = $derived(renderMarkdown(content));
</script>

<div class={`markdown-text leading-relaxed text-on-surface ${className}`}>{@html html}</div>
