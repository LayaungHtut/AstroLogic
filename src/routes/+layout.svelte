<script lang="ts">
	import '../routes/layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import StarField from '$lib/components/StarField.svelte';
	import Navigation from '$lib/components/Navigation.svelte';
	import Footer from '$lib/components/Footer.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>AstroLogic - AI Zodiac & Tarot Reasoning</title>
	<meta name="description" content="An AI-powered Zodiac, Tarot, and Horoscope application with symbolic reasoning" />
</svelte:head>

<div class="fixed inset-0 pointer-events-none cosmic-stars opacity-40 z-0"></div>
<StarField />
<Navigation />
<main class="relative z-10">
	{@render children()}
</main>
<Footer />
