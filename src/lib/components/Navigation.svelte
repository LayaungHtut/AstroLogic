<script lang="ts">
	import { page } from '$app/state';
	import favicon from '$lib/assets/favicon.svg';
	import { t } from '$lib/i18n';
	import LanguageSwitcher from '$lib/components/LanguageSwitcher.svelte';

	const navGroups = $derived([
		{
			items: [{ href: '/dashboard', label: $t('nav.dashboard'), icon: 'space_dashboard' }]
		},
		{
			items: [
				{ href: '/reading', label: $t('nav.reading'), icon: 'style' },
				{ href: '/tarot', label: $t('nav.deck'), icon: 'auto_stories' },
				{ href: '/scan', label: $t('nav.scan'), icon: 'center_focus_weak' }
			]
		},
		{
			items: [
				{ href: '/birth-chart', label: $t('nav.birthChart'), icon: 'orbit' },
				{ href: '/zodiac', label: $t('nav.zodiac'), icon: 'token' },
				{ href: '/horoscope', label: $t('nav.horoscope'), icon: 'nights_stay' },
				{ href: '/compatibility', label: $t('nav.synastry'), icon: 'all_inclusive' }
			]
		},
		{
			items: [
				{ href: '/chat', label: $t('nav.oracle'), icon: 'psychology' },
				{ href: '/history', label: $t('nav.history'), icon: 'history' },
				{ href: '/analytics', label: $t('nav.analytics'), icon: 'monitoring' }
			]
		}
	]);

	const isActive = (href: string) =>
		page.url.pathname === href || page.url.pathname.startsWith(href + '/');

	let mobileOpen = $state(false);
</script>

<header
	class="fixed top-0 z-50 w-full border-b border-tertiary/20 bg-surface-container-lowest/90 shadow-[0_4px_35px_rgba(0,0,0,0.7)] backdrop-blur-xl"
>
	<div class="pointer-events-none absolute inset-0 overflow-hidden">
		<div class="absolute -top-10 left-1/4 h-20 w-96 rounded-full bg-primary/15 blur-3xl"></div>
		<div class="absolute -top-10 right-1/4 h-20 w-80 rounded-full bg-secondary/15 blur-3xl"></div>
	</div>

	<div class="relative mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 lg:px-8">
		<a href="/" class="flex shrink-0 items-center gap-3">
			<div class="relative flex items-center justify-center">
				<div class="absolute inset-0 animate-pulse rounded-full bg-secondary/25 blur-md"></div>
				<div
					class="relative rounded-xl border border-primary/30 bg-surface-container-low/90 p-1.5 shadow-[0_0_15px_rgba(124,58,237,0.35)]"
				>
					<img alt="AstroLogic Emblem" class="h-7 w-7 object-contain" src={favicon} />
				</div>
			</div>
			<div class="hidden flex-col sm:flex">
				<span
					class="font-headline bg-gradient-to-r from-primary via-tertiary to-secondary bg-clip-text text-lg font-bold tracking-tight text-transparent"
				>
					{$t('brand.name')}
				</span>
				<span
					class="font-mono-data text-[10px] tracking-widest text-on-surface-variant/70 uppercase"
				>
					{$t('brand.subtitle')}
				</span>
			</div>
		</a>

		<nav
			class="hidden items-center gap-1 rounded-full border border-white/10 bg-surface-container-lowest/80 p-1 shadow-inner backdrop-blur-md xl:flex"
		>
			{#each navGroups as group, i}
				<div
					class="flex items-center gap-1 px-1.5 {i < navGroups.length - 1
						? 'border-r border-white/10'
						: ''}"
				>
					{#each group.items as item}
						<a
							href={item.href}
							class="flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium transition-all duration-200 {isActive(
								item.href
							)
								? 'border border-primary/40 bg-gradient-to-r from-primary-container/80 to-secondary-container/60 font-semibold text-white shadow-[0_0_16px_rgba(124,58,237,0.5)]'
								: 'text-on-surface-variant hover:bg-white/5 hover:text-primary'}"
						>
							<span class="material-symbols-outlined text-[16px]">{item.icon}</span>
							<span>{item.label}</span>
						</a>
					{/each}
				</div>
			{/each}
		</nav>

		<div class="flex shrink-0 items-center gap-2 sm:gap-3">
			<!-- Language Toggle -->
			<LanguageSwitcher />

			<a
				href="/reading"
				class="hidden items-center gap-1.5 rounded-full border border-primary/30 bg-gradient-to-r from-primary-container via-purple-600 to-secondary-container px-3 py-1.5 text-xs font-semibold text-white shadow-[0_0_20px_rgba(124,58,237,0.45)] transition-all duration-300 hover:scale-[1.02] hover:shadow-[0_0_28px_rgba(76,215,246,0.6)] active:scale-[0.98] sm:inline-flex sm:gap-2 sm:px-4 sm:py-2 sm:text-sm"
			>
				<span class="material-symbols-outlined animate-pulse text-sm text-secondary sm:text-base"
					>auto_awesome</span
				>
				<span>{$t('nav.newReading')}</span>
			</a>

			<button
				class="rounded-full border border-white/5 bg-surface-container-low/70 p-2 text-on-surface-variant transition-colors hover:bg-surface-container-high hover:text-on-surface xl:hidden"
				onclick={() => (mobileOpen = !mobileOpen)}
				aria-label="Toggle menu"
			>
				<span class="material-symbols-outlined text-xl">{mobileOpen ? 'close' : 'menu'}</span>
			</button>
		</div>
	</div>

	{#if mobileOpen}
		<div
			class="max-h-[calc(100vh-4rem)] overflow-y-auto border-t border-white/10 bg-surface-container-lowest/95 p-2 backdrop-blur-xl xl:hidden"
		>
			<div
				class="mb-2 flex items-center justify-between rounded-xl bg-surface-container-low/70 p-3"
			>
				<span class="text-xs font-medium text-on-surface-variant">Language / ဘာသာစကား</span>
				<LanguageSwitcher />
			</div>

			{#each navGroups as group}
				{#each group.items as item}
					<a
						href={item.href}
						class="flex items-center gap-3 rounded-xl px-4 py-3 text-sm transition-all {isActive(
							item.href
						)
							? 'bg-primary-container/20 font-semibold text-primary'
							: 'text-on-surface-variant hover:bg-white/5 hover:text-on-surface'}"
						onclick={() => (mobileOpen = false)}
					>
						<span class="material-symbols-outlined text-[18px]">{item.icon}</span>
						{item.label}
					</a>
				{/each}
			{/each}
			<a
				href="/about"
				class="flex items-center gap-3 rounded-xl px-4 py-3 text-sm transition-all {isActive(
					'/about'
				)
					? 'bg-primary-container/20 font-semibold text-primary'
					: 'text-on-surface-variant hover:bg-white/5 hover:text-on-surface'}"
				onclick={() => (mobileOpen = false)}
			>
				<span class="material-symbols-outlined text-[18px]">info</span>
				{$t('nav.about')}
			</a>

			<div class="mt-4 p-2">
				<a
					href="/reading"
					class="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary-container to-secondary-container py-3 text-sm font-semibold text-white shadow-lg"
					onclick={() => (mobileOpen = false)}
				>
					<span class="material-symbols-outlined text-base">auto_awesome</span>
					<span>{$t('nav.newReading')}</span>
				</a>
			</div>
		</div>
	{/if}
</header>
