<script lang="ts">
	import { profile } from '$lib/stores';
	import { ZODIAC_SIGNS, ZODIAC_SYMBOLS, ELEMENT_COLORS } from '$lib/types';

	let { open = $bindable(false) }: { open: boolean } = $props();

	const currentProfile = $derived($profile);
	const signElements: Record<string, string> = {
		aries: 'fire', taurus: 'earth', gemini: 'air', cancer: 'water',
		leo: 'fire', virgo: 'earth', libra: 'air', scorpio: 'water',
		sagittarius: 'fire', capricorn: 'earth', aquarius: 'air', pisces: 'water'
	};

	let selectedSign = $state(currentProfile.zodiac_sign);
	let nickname = $state(currentProfile.nickname);

	function save() {
		profile.setProfile({ zodiac_sign: selectedSign, nickname });
		open = false;
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') open = false;
	}
</script>

<svelte:window on:keydown={handleKeydown} />

{#if open}
	<div class="fixed inset-0 z-50 flex items-center justify-center p-4">
		<div class="absolute inset-0 bg-black/60 backdrop-blur-sm" role="presentation" onclick={() => open = false}></div>

		<div class="relative z-10 flex w-full max-w-lg flex-col gap-6 rounded-2xl bg-surface-container-lowest p-6 shadow-2xl max-h-[85vh] overflow-y-auto">
			<div class="flex items-center justify-between">
				<div class="flex items-center gap-3">
					<div class="flex h-10 w-10 items-center justify-center rounded-xl bg-primary-container text-primary">
						<span class="material-symbols-outlined text-xl">person</span>
					</div>
					<h2 class="font-headline text-xl font-bold text-on-surface">Edit Profile</h2>
				</div>
				<button type="button" onclick={() => open = false} class="flex h-8 w-8 items-center justify-center rounded-full text-on-surface-variant transition-colors hover:bg-surface-container-high">
					<span class="material-symbols-outlined text-xl">close</span>
				</button>
			</div>

			<div class="flex flex-col gap-2">
				<label for="nickname" class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase">Nickname</label>
				<input
					id="nickname"
					type="text"
					bind:value={nickname}
					placeholder="Explorer"
					class="rounded-xl bg-surface-container-high px-4 py-2.5 text-sm text-on-surface placeholder:text-on-surface-variant/50 focus:ring-1 focus:ring-primary focus:outline-none"
				/>
			</div>

			<div class="flex flex-col gap-3">
				<span class="font-mono-data text-[11px] tracking-wider text-on-surface-variant uppercase">Zodiac Sign</span>
				<div class="grid grid-cols-4 gap-2">
					{#each ZODIAC_SIGNS as sign}
						{@const elem = signElements[sign]}
						{@const color = ELEMENT_COLORS[elem]}
						<button
							type="button"
							onclick={() => selectedSign = sign}
							class="flex flex-col items-center gap-1.5 rounded-xl p-3 text-center transition-all {selectedSign === sign ? 'ring-2 ring-primary bg-primary-container/20 shadow-md' : 'bg-surface-container-high hover:bg-surface-container'}"
						>
							<span class="text-2xl" style:color={selectedSign === sign ? color : 'var(--color-on-surface-variant)'}>{ZODIAC_SYMBOLS[sign]}</span>
							<span class="font-mono-data text-[10px] font-medium capitalize text-on-surface">{sign}</span>
						</button>
					{/each}
				</div>
			</div>

			<div class="flex justify-end gap-3 pt-2">
				<button type="button" onclick={() => open = false} class="rounded-xl px-4 py-2 text-sm font-medium text-on-surface-variant transition-colors hover:bg-surface-container-high">
					Cancel
				</button>
				<button
					type="button"
					onclick={save}
					disabled={!selectedSign}
					class="rounded-xl bg-primary px-5 py-2 text-sm font-medium text-on-primary shadow-md transition-all hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
				>
					Save Profile
				</button>
			</div>
		</div>
	</div>
{/if}
