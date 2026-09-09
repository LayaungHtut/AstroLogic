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
	class="fixed top-0 w-full z-50 bg-surface-container-lowest/90 backdrop-blur-xl border-b border-tertiary/20 shadow-[0_4px_35px_rgba(0,0,0,0.7)]"
>
	<div class="absolute inset-0 pointer-events-none overflow-hidden">
		<div class="absolute -top-10 left-1/4 w-96 h-20 bg-primary/15 blur-3xl rounded-full"></div>
		<div class="absolute -top-10 right-1/4 w-80 h-20 bg-secondary/15 blur-3xl rounded-full"></div>
	</div>

	<div class="relative max-w-7xl mx-auto px-4 lg:px-8 h-16 flex items-center justify-between gap-4">
		<a href="/" class="flex items-center gap-3 shrink-0">
			<div class="relative flex items-center justify-center">
				<div class="absolute inset-0 rounded-full bg-secondary/25 blur-md animate-pulse"></div>
				<div class="relative p-1.5 rounded-xl bg-surface-container-low/90 border border-primary/30 shadow-[0_0_15px_rgba(124,58,237,0.35)]">
					<img alt="AstroLogic Emblem" class="h-7 w-7 object-contain" src={favicon} />
				</div>
			</div>
			<div class="hidden sm:flex flex-col">
				<span class="font-headline text-lg font-bold tracking-tight bg-gradient-to-r from-primary via-tertiary to-secondary bg-clip-text text-transparent">
					{$t('brand.name')}
				</span>
				<span class="font-mono-data text-[10px] uppercase tracking-widest text-on-surface-variant/70">
					{$t('brand.subtitle')}
				</span>
			</div>
		</a>

		<nav class="hidden xl:flex items-center gap-1 p-1 rounded-full bg-surface-container-lowest/80 border border-white/10 shadow-inner backdrop-blur-md">
			{#each navGroups as group, i}
				<div class="flex items-center gap-1 px-1.5 {i < navGroups.length - 1 ? 'border-r border-white/10' : ''}">
					{#each group.items as item}
						<a
							href={item.href}
							class="px-2.5 py-1 rounded-full text-xs font-medium transition-all duration-200 flex items-center gap-1.5 {isActive(item.href)
								? 'text-white bg-gradient-to-r from-primary-container/80 to-secondary-container/60 shadow-[0_0_16px_rgba(124,58,237,0.5)] border border-primary/40 font-semibold'
								: 'text-on-surface-variant hover:text-primary hover:bg-white/5'}"
						>
							<span class="material-symbols-outlined text-[16px]">{item.icon}</span>
							<span>{item.label}</span>
						</a>
					{/each}
				</div>
			{/each}
		</nav>

		<div class="flex items-center gap-2 sm:gap-3 shrink-0">
			<!-- Language Toggle -->
			<LanguageSwitcher />

			<a
				href="/reading"
				class="hidden sm:inline-flex items-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-1.5 sm:py-2 rounded-full bg-gradient-to-r from-primary-container via-purple-600 to-secondary-container text-white text-xs sm:text-sm font-semibold shadow-[0_0_20px_rgba(124,58,237,0.45)] hover:shadow-[0_0_28px_rgba(76,215,246,0.6)] border border-primary/30 hover:scale-[1.02] active:scale-[0.98] transition-all duration-300"
			>
				<span class="material-symbols-outlined text-sm sm:text-base text-secondary animate-pulse">auto_awesome</span>
				<span>{$t('nav.newReading')}</span>
			</a>

			<button
				class="xl:hidden p-2 rounded-full text-on-surface-variant hover:text-on-surface bg-surface-container-low/70 hover:bg-surface-container-high border border-white/5 transition-colors"
				onclick={() => (mobileOpen = !mobileOpen)}
				aria-label="Toggle menu"
			>
				<span class="material-symbols-outlined text-xl">{mobileOpen ? 'close' : 'menu'}</span>
			</button>
		</div>
	</div>

	{#if mobileOpen}
		<div class="xl:hidden border-t border-white/10 bg-surface-container-lowest/95 backdrop-blur-xl max-h-[calc(100vh-4rem)] overflow-y-auto p-2">
			<div class="p-3 mb-2 flex items-center justify-between bg-surface-container-low/70 rounded-xl">
				<span class="text-xs text-on-surface-variant font-medium">Language / ဘာသာစကား</span>
				<LanguageSwitcher />
			</div>

			{#each navGroups as group}
				{#each group.items as item}
					<a
						href={item.href}
						class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm transition-all {isActive(item.href)
							? 'bg-primary-container/20 text-primary font-semibold'
							: 'text-on-surface-variant hover:text-on-surface hover:bg-white/5'}"
						onclick={() => (mobileOpen = false)}
					>
						<span class="material-symbols-outlined text-[18px]">{item.icon}</span>
						{item.label}
					</a>
				{/each}
			{/each}
			<a
				href="/about"
				class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm transition-all {isActive('/about')
					? 'bg-primary-container/20 text-primary font-semibold'
					: 'text-on-surface-variant hover:text-on-surface hover:bg-white/5'}"
				onclick={() => (mobileOpen = false)}
			>
				<span class="material-symbols-outlined text-[18px]">info</span>
				{$t('nav.about')}
			</a>

			<div class="mt-4 p-2">
				<a
					href="/reading"
					class="w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-gradient-to-r from-primary-container to-secondary-container text-white text-sm font-semibold shadow-lg"
					onclick={() => (mobileOpen = false)}
				>
					<span class="material-symbols-outlined text-base">auto_awesome</span>
					<span>{$t('nav.newReading')}</span>
				</a>
			</div>
		</div>
	{/if}
</header>
