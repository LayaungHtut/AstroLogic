<script lang="ts">
	import { profile } from '$lib/stores';
	import { sendChatMessage } from '$lib/utils/api';
	import type { ChatMessage } from '$lib/types';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';

	let messages = $state<ChatMessage[]>([]);
	let input = $state('');
	let loading = $state(false);

	const currentProfile = $derived($profile);

	const suggestions = [
		'What does The Hermit mean?',
		'Tell me about Aries',
		'How do tarot readings work?'
	];

	async function sendMessage() {
		if (!input.trim() || loading) return;

		const userMsg: ChatMessage = { role: 'user', content: input };
		messages = [...messages, userMsg];
		const question = input;
		input = '';
		loading = true;

		try {
			const res = await sendChatMessage(question, currentProfile.zodiac_sign);
			messages = [...messages, { role: 'assistant', content: res.response }];
		} catch {
			messages = [...messages, {
				role: 'assistant',
				content: "I'm having trouble connecting to my mystical sources. Please try again."
			}];
		} finally {
			loading = false;
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			sendMessage();
		}
	}

	function useSuggestion(suggestion: string) {
		input = suggestion;
		sendMessage();
	}
</script>

<svelte:head>
	<title>AI Guide - AstroLogic</title>
</svelte:head>

<div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-6 flex flex-col h-[calc(100vh-4rem)]">
	<!-- Oracle Status Ribbon -->
	<div class="relative z-10 px-5 py-4 rounded-t-2xl bg-surface-container/60 backdrop-blur-md border border-b-0 border-outline-variant/20 flex flex-wrap items-center justify-between gap-4 shrink-0">
		<div class="flex items-center gap-3 min-w-0">
			<div class="w-10 h-10 rounded-xl bg-primary-container/30 flex items-center justify-center text-primary shadow-sm shrink-0">
				<span class="material-symbols-outlined text-2xl" style="font-variation-settings: 'FILL' 1;">psychology_alt</span>
			</div>
			<div class="min-w-0">
				<div class="flex items-center gap-2 flex-wrap">
					<h1 class="font-headline text-lg font-semibold text-on-surface tracking-tight">Socratic AI Oracle</h1>
					<span class="px-2 py-0.5 rounded-full bg-secondary-container/20 text-secondary text-[10px] font-mono-data uppercase tracking-wider">v4.8</span>
				</div>
				<p class="text-sm text-on-surface-variant truncate">Chat with your tarot and astrology guide</p>
			</div>
		</div>
		<div class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-container-high/80 backdrop-blur-sm shrink-0">
			<span class="w-2 h-2 rounded-full bg-secondary animate-pulse shadow-sm"></span>
			<span class="font-mono-data text-xs text-on-surface">Logic Core Online</span>
		</div>
	</div>

	<div class="flex-1 flex flex-col glass-card rounded-t-none border-t-0 overflow-hidden">
		<div class="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
			{#if messages.length === 0}
				<div class="flex flex-col items-center justify-center h-full text-center py-12">
					<div class="w-14 h-14 rounded-xl bg-gradient-to-tr from-primary-container to-secondary-container flex items-center justify-center text-on-primary shadow-lg mb-4">
						<span class="material-symbols-outlined text-3xl">auto_awesome</span>
					</div>
					<h2 class="font-headline text-lg font-semibold text-on-surface mb-2">Welcome to your AI Guide</h2>
					<p class="text-sm text-on-surface-variant max-w-md mb-6">
						Ask questions about tarot readings, zodiac signs, or request guidance.
						I'll do my best to provide thoughtful, symbolic interpretations.
					</p>
					<div class="flex flex-wrap gap-2 justify-center">
						{#each suggestions as suggestion}
							<button
								class="text-xs px-3 py-1.5 rounded-full bg-surface-container-high/70 border border-outline-variant/30 text-on-surface-variant hover:text-on-surface hover:bg-surface-container-highest transition-all"
								onclick={() => useSuggestion(suggestion)}
							>
								{suggestion}
							</button>
						{/each}
					</div>
				</div>
			{:else}
				{#each messages as msg}
					<div class="flex {msg.role === 'user' ? 'justify-end' : 'justify-start'}">
						{#if msg.role === 'user'}
							<div class="max-w-[85%] md:max-w-2xl bg-gradient-to-br from-primary-container to-surface-container-highest text-on-primary-container p-4 rounded-2xl rounded-tr-none shadow-xl">
								<div class="flex items-center gap-2 mb-1.5">
									<span class="w-5 h-5 rounded-full bg-surface-container-lowest/40 flex items-center justify-center text-[9px] font-mono-data text-primary-fixed">YOU</span>
								</div>
								<p class="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
							</div>
						{:else}
							<div class="max-w-[85%] md:max-w-2xl w-full sm:w-auto bg-surface-container/80 backdrop-blur-2xl text-on-surface p-4 rounded-2xl rounded-tl-none shadow-2xl relative">
								<div class="absolute -inset-0.5 rounded-2xl bg-gradient-to-r from-secondary/20 via-primary/10 to-transparent -z-10 blur-sm pointer-events-none"></div>
								<div class="flex items-center gap-2 mb-2">
									<div class="w-6 h-6 rounded-lg bg-gradient-to-tr from-primary-container to-secondary-container flex items-center justify-center text-on-primary shrink-0">
										<span class="material-symbols-outlined text-sm">psychology</span>
									</div>
									<span class="text-xs font-mono-data text-secondary uppercase tracking-wider">AI Guide</span>
								</div>
								<p class="text-sm leading-relaxed whitespace-pre-wrap text-on-surface">{msg.content}</p>
							</div>
						{/if}
					</div>
				{/each}

				{#if loading}
					<div class="flex justify-start">
						<div class="bg-surface-container/80 backdrop-blur-2xl rounded-2xl rounded-tl-none px-6 shadow-2xl">
							<LoadingSpinner text="The Oracle is consulting the stars..." />
						</div>
					</div>
				{/if}
			{/if}
		</div>

		<!-- Cosmic Query Input Cockpit -->
		<div class="p-4 md:p-5 bg-surface-container-low/90 backdrop-blur-2xl border-t border-outline-variant/20 shrink-0">
			<div class="relative bg-surface-container-lowest/90 rounded-2xl p-2.5 shadow-xl">
				<div class="flex items-end gap-2">
					<input
						type="text"
						bind:value={input}
						onkeydown={handleKeydown}
						class="flex-1 bg-transparent text-on-surface placeholder:text-outline text-sm focus:outline-none px-2 py-2"
						placeholder="Ask about your reading, zodiac, or anything mystical..."
						disabled={loading}
					/>
					<button
						class="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-gradient-to-r from-primary-container to-secondary-container text-on-primary text-sm font-semibold shadow-lg hover:shadow-secondary/25 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-40 disabled:pointer-events-none shrink-0"
						onclick={sendMessage}
						disabled={!input.trim() || loading}
					>
						<span>Send</span>
						<span class="material-symbols-outlined text-base">send</span>
					</button>
				</div>
			</div>
			<div class="flex items-center justify-between mt-2 px-2 text-outline">
				<span class="text-[11px] font-mono-data flex items-center gap-1.5">
					<span class="material-symbols-outlined text-xs text-secondary">verified_user</span>
					Symbolic interpretations only, not professional advice
				</span>
				<span class="text-[11px] font-mono-data hidden sm:inline">Shift + Enter for multi-line</span>
			</div>
		</div>
	</div>
</div>
