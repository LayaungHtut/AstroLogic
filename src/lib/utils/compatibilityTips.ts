const APPROACH_TIPS: Record<string, { firstMove: string; setting: string; vibe: string; avoid: string }> = {
	aries: { firstMove: 'Be direct and confident — they respect boldness.', setting: 'Something active: a sports event, hiking, or a spontaneous adventure.', vibe: 'High energy, playful competition.', avoid: 'Being passive or overly cautious.' },
	taurus: { firstMove: 'Take it slow and show genuine interest in their comforts.', setting: 'A nice dinner, cozy café, or a scenic walk.', vibe: 'Relaxed, sensual, consistent.', avoid: 'Rushing them or being unreliable.' },
	gemini: { firstMove: 'Engage them with witty banter and interesting topics.', setting: 'A social gathering, bookstore, or anywhere with variety.', vibe: 'Playful, curious, mentally stimulating.', avoid: 'Being boring or too serious too soon.' },
	cancer: { firstMove: 'Show warmth and emotional sincerity.', setting: 'A quiet, intimate setting — home-cooked meal or a peaceful park.', vibe: 'Nurturing, safe, personal.', avoid: 'Being too forward or dismissive of feelings.' },
	leo: { firstMove: 'Compliment them genuinely and show admiration.', setting: 'Somewhere they can shine — a party, art gallery, or concert.', vibe: 'Fun, glamorous, enthusiastic.', avoid: 'Ignoring them or being low-energy.' },
	virgo: { firstMove: 'Show thoughtfulness through small, meaningful gestures.', setting: 'A bookstore, farmers market, or a well-planned outing.', vibe: 'Calm, intelligent, detail-oriented.', avoid: 'Being messy, loud, or disorganized.' },
	libra: { firstMove: 'Be charming, balanced, and show good taste.', setting: 'A beautiful restaurant, art exhibit, or cultural event.', vibe: 'Elegant, harmonious, social.', avoid: 'Being crude or creating conflict.' },
	scorpio: { firstMove: 'Be mysterious and let them come to you — eye contact is key.', setting: 'An intimate, dimly-lit bar or a deep conversation setting.', vibe: 'Intense, passionate, authentic.', avoid: 'Being superficial or flirting with others.' },
	sagittarius: { firstMove: 'Suggest an adventure or share an exciting idea.', setting: 'Something spontaneous — a road trip, concert, or new restaurant.', vibe: 'Free-spirited, fun, philosophical.', avoid: 'Being clingy or too controlling.' },
	capricorn: { firstMove: 'Show ambition and respect for their goals.', setting: 'A nice dinner or an activity that shows your driven side.', vibe: 'Mature, goal-oriented, reliable.', avoid: 'Being frivolous or unreliable.' },
	aquarius: { firstMove: 'Discuss unique ideas and causes you care about.', setting: 'A quirky café, tech event, or community gathering.', vibe: 'Intellectual, unconventional, friendly.', avoid: 'Being too traditional or emotionally demanding.' },
	pisces: { firstMove: 'Be gentle, creative, and show emotional depth.', setting: 'A quiet beach, art studio, or cozy movie night.', vibe: 'Dreamy, romantic, intuitive.', avoid: 'Being harsh, loud, or overly logical.' },
};

const CONVERSATION_STARTERS: Record<string, string[]> = {
	aries: ['What adventure are you planning next?', "What's the boldest thing you've ever done?", 'Pick a superpower — what do you choose?'],
	taurus: ['What comfort food can you never resist?', 'Where is your dream vacation spot?', 'What song always puts you in a good mood?'],
	gemini: ['What topic could you talk about for hours?', 'Have you read or watched anything amazing lately?', 'If you could learn any skill instantly, what would it be?'],
	cancer: ['What does home mean to you?', 'Do you have a favorite family tradition?', 'What makes you feel most at peace?'],
	leo: ['What are you most proud of?', 'What makes you light up when you talk about it?', 'If you could perform anywhere, where would it be?'],
	virgo: ['What project are you currently working on?', 'What little thing always makes your day better?', 'How do you unwind after a long week?'],
	libra: ['What does balance mean to you?', 'What aesthetic or style inspires you?', 'What cause are you passionate about?'],
	scorpio: ['What is something most people don\'t know about you?', 'What drives you on a deep level?', 'What\'s a passion you rarely talk about?'],
	sagittarius: ['What\'s on your bucket list?', 'What\'s the best trip you\'ve ever taken?', 'What philosophy do you live by?'],
	capricorn: ['What goal are you working toward right now?', 'Where do you see yourself in five years?', 'What achievement are you most proud of?'],
	aquarius: ['What cause or idea are you most passionate about?', 'What unique hobby or interest do you have?', 'If you could change one thing about the world, what would it be?'],
	pisces: ['What inspires your creativity?', 'Do you ever have dreams that feel like messages?', 'What makes you feel most connected to something bigger?'],
};

const ELEMENT_INTIMACY_TIPS: Record<string, string> = {
	fire: 'Build trust through shared excitement and honest, direct communication.',
	earth: 'Show reliability and patience — they value consistency over grand gestures.',
	air: 'Keep things mentally stimulating and give them space to think and breathe.',
	water: 'Be emotionally available and create a safe, nurturing space for vulnerability.',
};

const ELEMENT_DATE_IDEAS: Record<string, string[]> = {
	fire: ['Rock climbing or trampoline park', 'A cooking competition at home', 'Live music or a comedy show'],
	earth: ['Wine tasting or a nice restaurant', 'A botanical garden or nature trail', 'A cozy movie marathon at home'],
	air: ['Trivia night or a debate café', 'Museum hopping or a gallery opening', 'A bookshop crawl followed by coffee'],
	water: ['Sunset picnic by the water', 'An art class or pottery workshop', 'A quiet evening stargazing'],
};

function elementOf(sign: string): string {
	const map: Record<string, string> = {
		aries: 'fire', leo: 'fire', sagittarius: 'fire',
		taurus: 'earth', virgo: 'earth', capricorn: 'earth',
		gemini: 'air', libra: 'air', aquarius: 'air',
		cancer: 'water', scorpio: 'water', pisces: 'water',
	};
	return map[sign] || 'air';
}

export interface ApproachTips {
	approach: {
		firstMove: string;
		setting: string;
		vibe: string;
		avoid: string;
	};
	conversationStarters: string[];
	dateIdeas: string[];
	intimacyTip: string;
}

export function getApproachTips(sign1: string, sign2: string): ApproachTips {
	const tips = APPROACH_TIPS[sign2] || APPROACH_TIPS.aries;
	const starters = CONVERSATION_STARTERS[sign2] || CONVERSATION_STARTERS.aries;
	const targetElement = elementOf(sign2);
	const sharedIdeas = (ELEMENT_DATE_IDEAS[targetElement] || ELEMENT_DATE_IDEAS.air);

	return {
		approach: tips,
		conversationStarters: starters,
		dateIdeas: sharedIdeas,
		intimacyTip: ELEMENT_INTIMACY_TIPS[targetElement] || '',
	};
}
