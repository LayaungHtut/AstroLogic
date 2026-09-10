<script lang="ts">
	import '../routes/layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import StarField from '$lib/components/StarField.svelte';
	import Navigation from '$lib/components/Navigation.svelte';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import Footer from '$lib/components/Footer.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>AstroLogic - AI Zodiac & Tarot Reasoning</title>
	<meta
		name="description"
		content="An AI-powered Zodiac, Tarot, and Horoscope application with symbolic reasoning"
	/>
</svelte:head>

<div class="cosmic-stars pointer-events-none fixed inset-0 z-0 opacity-40"></div>
<StarField />
<Navigation />
<Sidebar />
<div class="lg:pl-64">
	<main class="relative z-10">
		{@render children()}
	</main>
	<Footer />
</div>
