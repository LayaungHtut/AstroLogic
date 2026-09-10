<script lang="ts">
	import { page } from '$app/state';
	import { t } from '$lib/i18n';

	const navGroups = $derived([
		{
			items: [{ href: '/dashboard', label: $t('nav.dashboard'), icon: 'space_dashboard' }]
		},
		{
			label: $t('nav.reading'),
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
</script>

<aside
	class="fixed top-16 left-0 z-40 hidden h-[calc(100vh-4rem)] w-64 flex-col overflow-hidden px-3 py-3 border-r border-white/10 bg-surface-container-lowest/90 backdrop-blur-xl lg:flex"
>
	<a
		href="/reading"
		class="mb-3 flex shrink-0 items-center justify-center gap-2 rounded-xl border border-primary/30 bg-gradient-to-r from-primary-container via-purple-600 to-secondary-container px-4 py-2 text-sm font-semibold text-white shadow-[0_0_20px_rgba(124,58,237,0.45)] transition-all duration-300 hover:scale-[1.02] hover:shadow-[0_0_28px_rgba(76,215,246,0.6)] active:scale-[0.98]"
	>
		<span class="material-symbols-outlined animate-pulse text-base text-secondary"
			>auto_awesome</span
		>
		<span>{$t('nav.newReading')}</span>
	</a>

	<nav class="flex min-h-0 flex-1 flex-col justify-between gap-1">
		<div class="flex flex-col gap-1.5">
			{#each navGroups as group, i}
				<div
					class="flex flex-col gap-0.5 {i < navGroups.length - 1
						? 'border-b border-white/10 pb-1.5'
						: ''}"
				>
					{#each group.items as item}
						<a
							href={item.href}
							class="flex items-center gap-3 rounded-lg px-3 py-1.5 text-sm font-medium transition-all duration-200 {isActive(
								item.href
							)
								? 'border border-primary/40 bg-gradient-to-r from-primary-container/80 to-secondary-container/60 font-semibold text-white shadow-[0_0_16px_rgba(124,58,237,0.5)]'
								: 'text-on-surface-variant hover:bg-white/5 hover:text-primary'}"
						>
							<span class="material-symbols-outlined text-[18px]">{item.icon}</span>
							<span>{item.label}</span>
						</a>
					{/each}
				</div>
			{/each}
		</div>

		<a
			href="/about"
			class="flex shrink-0 items-center gap-3 rounded-lg px-3 py-1.5 text-sm font-medium transition-all duration-200 {isActive(
				'/about'
			)
				? 'bg-primary-container/20 font-semibold text-primary'
				: 'text-on-surface-variant hover:bg-white/5 hover:text-on-surface'}"
		>
			<span class="material-symbols-outlined text-[18px]">info</span>
			<span>{$t('nav.about')}</span>
		</a>
	</nav>
</aside>
