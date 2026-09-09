<script lang="ts">
	import { profile } from '$lib/stores';
	import { sendChatMessage } from '$lib/utils/api';
	import type { ChatMessage } from '$lib/types';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import MarkdownText from '$lib/components/MarkdownText.svelte';
	import { locale, t } from '$lib/i18n';

	let messages = $state<ChatMessage[]>([]);
	let input = $state('');
	let loading = $state(false);

	const currentProfile = $derived($profile);

	const suggestions = $derived([
		$t('chat.suggestion1'),
		$t('chat.suggestion2'),
		$t('chat.suggestion3')
	]);

	async function sendMessage() {
		if (!input.trim() || loading) return;

		const userMsg: ChatMessage = { role: 'user', content: input };
		messages = [...messages, userMsg];
		const question = input;
		input = '';
		loading = true;

		try {
			const res = await sendChatMessage(question, currentProfile.zodiac_sign, undefined, $locale);
			messages = [...messages, { role: 'assistant', content: res.response }];
		} catch {
			messages = [
				...messages,
				{
					role: 'assistant',
					content:
						$locale === 'my'
							? 'နက္ခတ်ဗေဒင် အရင်းအမြစ်များနှင့် ချိတ်ဆက်ရာတွင် အခက်အခဲရှိနေပါသည်။ ကျေးဇူးပြု၍ နောက်တစ်ကြိမ် ထပ်မံကြိုးစားပါ။'
							: "I'm having trouble connecting to my mystical sources. Please try again."
				}
			];
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
	<title>{$t('chat.title')} - {$t('brand.name')}</title>
</svelte:head>

<div class="mx-auto flex h-[calc(100vh-4rem)] max-w-6xl flex-col px-4 pt-24 pb-6 sm:px-6 lg:px-8">
	<!-- Oracle Status Ribbon -->
	<div
		class="relative z-10 flex shrink-0 flex-wrap items-center justify-between gap-4 rounded-t-2xl border border-b-0 border-outline-variant/20 bg-surface-container/60 px-5 py-4 backdrop-blur-md"
	>
		<div class="flex min-w-0 items-center gap-3">
			<div
				class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary-container/30 text-primary shadow-sm"
			>
				<span class="material-symbols-outlined text-2xl" style="font-variation-settings: 'FILL' 1;"
					>psychology_alt</span
				>
			</div>
			<div class="min-w-0">
				<div class="flex flex-wrap items-center gap-2">
					<h1 class="font-headline text-lg font-semibold tracking-tight text-on-surface">
						{$t('chat.title')}
					</h1>
					<span
						class="font-mono-data rounded-full bg-secondary-container/20 px-2 py-0.5 text-[10px] tracking-wider text-secondary uppercase"
						>v4.8</span
					>
				</div>
				<p class="truncate text-sm text-on-surface-variant">{$t('chat.subtitle2')}</p>
			</div>
		</div>
		<div
			class="flex shrink-0 items-center gap-2 rounded-full bg-surface-container-high/80 px-3 py-1.5 backdrop-blur-sm"
		>
			<span class="h-2 w-2 animate-pulse rounded-full bg-secondary shadow-sm"></span>
			<span class="font-mono-data text-xs text-on-surface">{$t('chat.logicOnline')}</span>
		</div>
	</div>

	<div class="glass-card flex flex-1 flex-col overflow-hidden rounded-t-none border-t-0">
		<div class="flex-1 space-y-6 overflow-y-auto p-4 md:p-6">
			{#if messages.length === 0}
				<div class="flex h-full flex-col items-center justify-center py-12 text-center">
					<div
						class="mb-4 flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-tr from-primary-container to-secondary-container text-on-primary shadow-lg"
					>
						<span class="material-symbols-outlined text-3xl">auto_awesome</span>
					</div>
					<h2 class="font-headline mb-2 text-lg font-semibold text-on-surface">
						{$t('chat.welcome')}
					</h2>
					<p class="mb-6 max-w-md text-sm text-on-surface-variant">
						{$t('chat.welcomeDesc')}
					</p>
					<div class="flex flex-wrap justify-center gap-2">
						{#each suggestions as suggestion}
							<button
								class="rounded-full border border-outline-variant/30 bg-surface-container-high/70 px-3 py-1.5 text-xs text-on-surface-variant transition-all hover:bg-surface-container-highest hover:text-on-surface"
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
							<div
								class="max-w-[85%] rounded-2xl rounded-tr-none bg-gradient-to-br from-primary-container to-surface-container-highest p-4 text-on-primary-container shadow-xl md:max-w-2xl"
							>
								<div class="mb-1.5 flex items-center gap-2">
									<span
										class="font-mono-data flex h-5 w-5 items-center justify-center rounded-full bg-surface-container-lowest/40 text-[9px] text-primary-fixed"
										>{$t('chat.you')}</span
									>
								</div>
								<p class="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
							</div>
						{:else}
							<div
								class="relative w-full max-w-[85%] rounded-2xl rounded-tl-none bg-surface-container/80 p-4 text-on-surface shadow-2xl backdrop-blur-2xl sm:w-auto md:max-w-2xl"
							>
								<div
									class="pointer-events-none absolute -inset-0.5 -z-10 rounded-2xl bg-gradient-to-r from-secondary/20 via-primary/10 to-transparent blur-sm"
								></div>
								<div class="mb-2 flex items-center gap-2">
									<div
										class="flex h-6 w-6 shrink-0 items-center justify-center rounded-lg bg-gradient-to-tr from-primary-container to-secondary-container text-on-primary"
									>
										<span class="material-symbols-outlined text-sm">psychology</span>
									</div>
									<span class="font-mono-data text-xs tracking-wider text-secondary uppercase"
										>{$t('chat.aiGuide')}</span
									>
								</div>
								<MarkdownText
									content={msg.content}
									class="text-sm leading-relaxed text-on-surface"
								/>
							</div>
						{/if}
					</div>
				{/each}

				{#if loading}
					<div class="flex justify-start">
						<div
							class="rounded-2xl rounded-tl-none bg-surface-container/80 px-6 shadow-2xl backdrop-blur-2xl"
						>
							<LoadingSpinner text={$t('chat.consulting')} />
						</div>
					</div>
				{/if}
			{/if}
		</div>

		<!-- Cosmic Query Input Cockpit -->
		<div
			class="shrink-0 border-t border-outline-variant/20 bg-surface-container-low/90 p-4 backdrop-blur-2xl md:p-5"
		>
			<div class="relative rounded-2xl bg-surface-container-lowest/90 p-2.5 shadow-xl">
				<div class="flex items-end gap-2">
					<input
						type="text"
						id="chat-message"
						name="chat-message"
						bind:value={input}
						onkeydown={handleKeydown}
						class="flex-1 bg-transparent px-2 py-2 text-sm text-on-surface placeholder:text-outline focus:outline-none"
						placeholder={$t('chat.placeholder')}
						disabled={loading}
					/>
					<button
						class="inline-flex shrink-0 items-center gap-2 rounded-full bg-gradient-to-r from-primary-container to-secondary-container px-5 py-2.5 text-sm font-semibold text-on-primary shadow-lg transition-all hover:scale-[1.02] hover:shadow-secondary/25 active:scale-[0.98] disabled:pointer-events-none disabled:opacity-40"
						onclick={sendMessage}
						disabled={!input.trim() || loading}
					>
						<span>{$t('chat.send')}</span>
						<span class="material-symbols-outlined text-base">send</span>
					</button>
				</div>
			</div>
			<div class="mt-2 flex items-center justify-between px-2 text-outline">
				<span class="font-mono-data flex items-center gap-1.5 text-[11px]">
					<span class="material-symbols-outlined text-xs text-secondary">verified_user</span>
					{$locale === 'my'
						? 'သင်္ကေတအရ ဆင်ခြင်သုံးသပ်ရန်အတွက်သာ ဖြစ်သည်'
						: 'Symbolic interpretations only, not professional advice'}
				</span>
				<span class="font-mono-data hidden text-[11px] sm:inline"
					>{$locale === 'my'
						? 'စာကြောင်းအသစ်အတွက် Shift + Enter နှိပ်ပါ'
						: 'Shift + Enter for multi-line'}</span
				>
			</div>
		</div>
	</div>
</div>
