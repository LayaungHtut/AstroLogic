/**
 * Route a remote tarot card image through wsrv.nl's resizing/caching proxy
 * instead of loading it straight from the source API.
 *
 * The tarot card API (sixseeds.github.io) serves every card as a
 * full-resolution scan — roughly 1150x1900px, ~1-1.2MB per JPEG — even
 * though the UI only ever displays them as small thumbnails or card faces.
 * That's the actual reason card images sometimes fail to show up on a
 * different wifi: on a slow, congested, or metered connection a 1MB+
 * request per card can stall or time out before it finishes, and some
 * network-level content filters drop large media downloads outright. A
 * broken/blocked *.github.io host on a particular network has the same
 * symptom, and routing through a different domain incidentally works
 * around that too.
 *
 * wsrv.nl fetches the source image once, resizes and re-encodes it as
 * WebP, and edge-caches the result — a 300px-wide thumbnail comes back at
 * roughly 40-50KB instead of 1.1MB+, which is both faster and far less
 * likely to be interrupted by a weak connection.
 */
export function cardImage(url: string | undefined | null, width: number): string | undefined {
	if (!url) return undefined;
	if (!url.startsWith('http')) return url;
	const bare = url.replace(/^https?:\/\//, '');
	return `https://wsrv.nl/?url=${encodeURIComponent(bare)}&w=${width}&output=webp&q=82`;
}
