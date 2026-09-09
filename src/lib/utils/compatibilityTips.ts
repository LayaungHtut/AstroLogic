import type { SupportedLocale } from '$lib/i18n';

const APPROACH_TIPS: Record<
	string,
	{ firstMove: string; setting: string; vibe: string; avoid: string }
> = {
	aries: {
		firstMove: 'Be direct and confident — they respect boldness.',
		setting: 'Something active: a sports event, hiking, or a spontaneous adventure.',
		vibe: 'High energy, playful competition.',
		avoid: 'Being passive or overly cautious.'
	},
	taurus: {
		firstMove: 'Take it slow and show genuine interest in their comforts.',
		setting: 'A nice dinner, cozy café, or a scenic walk.',
		vibe: 'Relaxed, sensual, consistent.',
		avoid: 'Rushing them or being unreliable.'
	},
	gemini: {
		firstMove: 'Engage them with witty banter and interesting topics.',
		setting: 'A social gathering, bookstore, or anywhere with variety.',
		vibe: 'Playful, curious, mentally stimulating.',
		avoid: 'Being boring or too serious too soon.'
	},
	cancer: {
		firstMove: 'Show warmth and emotional sincerity.',
		setting: 'A quiet, intimate setting — home-cooked meal or a peaceful park.',
		vibe: 'Nurturing, safe, personal.',
		avoid: 'Being too forward or dismissive of feelings.'
	},
	leo: {
		firstMove: 'Compliment them genuinely and show admiration.',
		setting: 'Somewhere they can shine — a party, art gallery, or concert.',
		vibe: 'Fun, glamorous, enthusiastic.',
		avoid: 'Ignoring them or being low-energy.'
	},
	virgo: {
		firstMove: 'Show thoughtfulness through small, meaningful gestures.',
		setting: 'A bookstore, farmers market, or a well-planned outing.',
		vibe: 'Calm, intelligent, detail-oriented.',
		avoid: 'Being messy, loud, or disorganized.'
	},
	libra: {
		firstMove: 'Be charming, balanced, and show good taste.',
		setting: 'A beautiful restaurant, art exhibit, or cultural event.',
		vibe: 'Elegant, harmonious, social.',
		avoid: 'Being crude or creating conflict.'
	},
	scorpio: {
		firstMove: 'Be mysterious and let them come to you — eye contact is key.',
		setting: 'An intimate, dimly-lit bar or a deep conversation setting.',
		vibe: 'Intense, passionate, authentic.',
		avoid: 'Being superficial or flirting with others.'
	},
	sagittarius: {
		firstMove: 'Suggest an adventure or share an exciting idea.',
		setting: 'Something spontaneous — a road trip, concert, or new restaurant.',
		vibe: 'Free-spirited, fun, philosophical.',
		avoid: 'Being clingy or too controlling.'
	},
	capricorn: {
		firstMove: 'Show ambition and respect for their goals.',
		setting: 'A nice dinner or an activity that shows your driven side.',
		vibe: 'Mature, goal-oriented, reliable.',
		avoid: 'Being frivolous or unreliable.'
	},
	aquarius: {
		firstMove: 'Discuss unique ideas and causes you care about.',
		setting: 'A quirky café, tech event, or community gathering.',
		vibe: 'Intellectual, unconventional, friendly.',
		avoid: 'Being too traditional or emotionally demanding.'
	},
	pisces: {
		firstMove: 'Be gentle, creative, and show emotional depth.',
		setting: 'A quiet beach, art studio, or cozy movie night.',
		vibe: 'Dreamy, romantic, intuitive.',
		avoid: 'Being harsh, loud, or overly logical.'
	}
};

const APPROACH_TIPS_MY: Record<
	string,
	{ firstMove: string; setting: string; vibe: string; avoid: string }
> = {
	aries: {
		firstMove: 'ပွင့်လင်းရဲရင့်စွာ တိုက်ရိုက်ချဉ်းကပ်ပါ — သူတို့သည် သတ္တိရှိသူကို လေးစားတတ်သည်။',
		setting:
			'လှုပ်ရှားမှုရှိသောအရာများ - အားကစားပွဲ၊ တောင်တက်ခြင်း သို့မဟုတ် ရုတ်တရက်စွန့်စားခရီးထွက်ခြင်း။',
		vibe: 'တက်ကြွမှုပြည့်ဝပြီး ရယ်ရယ်မောမော ယှဉ်ပြိုင်လိုစိတ်ရှိသော အငွေ့အသက်။',
		avoid: 'တွေဝေတုံ့ဆိုင်းလွန်းခြင်း သို့မဟုတ် သတိလွန်ကဲနေခြင်း။'
	},
	taurus: {
		firstMove:
			'ဖြည်းဖြည်းချင်း အေးအေးဆေးဆေး စတင်ပြီး သူတို့၏ သက်တောင့်သက်သာရှိမှုကို အလေးထားကြောင်း ပြသပါ။',
		setting:
			'ကောင်းမွန်သော ညစာစားပွဲ၊ အေးချမ်းသော ကော်ဖီဆိုင် သို့မဟုတ် သဘာဝရှုခင်းကြည့် လမ်းလျှောက်ခြင်း။',
		vibe: 'အေးဆေးတည်ငြိမ်ပြီး စိတ်ချယုံကြည်ရသော အငွေ့အသက်။',
		avoid: 'လောဆော်လွန်းခြင်း သို့မဟုတ် ကတိမတည်ခြင်း။'
	},
	gemini: {
		firstMove:
			'ဉာဏ်ရည်ပြောင်မြောက်သော ဟာသများနှင့် စိတ်ဝင်စားဖွယ် ခေါင်းစဉ်များဖြင့် စတင်ဆွေးနွေးပါ။',
		setting: 'လူစုံရာဆုံတွေ့ပွဲ၊ စာအုပ်ဆိုင် သို့မဟုတ် စုံလင်ဆန်းသစ်သော နေရာများ။',
		vibe: 'ရယ်စရာကောင်းပြီး စူးစမ်းရှာဖွေလိုသော အငွေ့အသက်။',
		avoid: 'ပျင်းစရာကောင်းလွန်းခြင်း သို့မဟုတ် အစောတလျဉ်း အလေးအနက်ထားလွန်းခြင်း။'
	},
	cancer: {
		firstMove: 'နွေးထွေးမှုနှင့် ရိုးသားဖြူစင်သော စိတ်ခံစားချက်ကို ဖော်ပြပါ။',
		setting:
			'တိတ်ဆိတ်နွေးထွေးသော နေရာ - ကိုယ်တိုင်ချက်ပြုတ်ကျွေးမွေးခြင်း သို့မဟုတ် အေးချမ်းသော ပန်းခြံ။',
		vibe: 'ဂရုစိုက်ယုယမှု၊ လုံခြုံမှုနှင့် သီးသန့်ဆန်မှုရှိသော အငွေ့အသက်။',
		avoid: 'ရုတ်တရက် အလွန်ရင်းနှီးလွန်းအောင်ပြုမူခြင်း သို့မဟုတ် စိတ်ခံစားချက်ကို လျစ်လျူရှုခြင်း။'
	},
	leo: {
		firstMove: 'စိတ်ရင်းအမှန်ဖြင့် ချီးကျူးစကားဆိုပြီး လေးစားတန်ဖိုးထားမှုကို ပြသပါ။',
		setting: 'သူတို့တောက်ပနိုင်မည့် နေရာ - ပါတီပွဲ၊ အနုပညာပြခန်း သို့မဟုတ် တေးဂီတဖျော်ဖြေပွဲ။',
		vibe: 'ပျော်ရွှင်ဖွယ်ကောင်းပြီး ခမ်းနားတက်ကြွသော အငွေ့အသက်။',
		avoid: 'လျစ်လျူရှုထားခြင်း သို့မဟုတ် တက်ကြွမှုမရှိ စိတ်မပါသလို ပြုမူခြင်း။'
	},
	virgo: {
		firstMove: 'အသေးစိတ်ဂရုစိုက်မှုနှင့် အဓိပ္ပာယ်ရှိသော အပြုအမူလေးများဖြင့် ဖော်ပြပါ။',
		setting: 'စာအုပ်ဆိုင်၊ သဘာဝစိုက်ပျိုးရေးဈေး သို့မဟုတ် စနစ်တကျစီစဉ်ထားသော အပြင်ထွက်လည်ပတ်မှု။',
		vibe: 'တည်ငြိမ်မှု၊ ဉာဏ်ရည်ထက်မြက်မှုနှင့် အသေးစိတ်ကျနမှုရှိသော အငွေ့အသက်။',
		avoid: 'ရှုပ်ပွပေရေခြင်း၊ ဆူညံအော်ဟစ်ခြင်း သို့မဟုတ် အစီအစဉ်မရှိခြင်း။'
	},
	libra: {
		firstMove: 'ဆွဲဆောင်မှုရှိစွာ၊ မျှမျှတတနှင့် အနုပညာအမြင်ကောင်းမွန်ကြောင်း ဖော်ပြပါ။',
		setting: 'လှပသောအလှပြင်ဆင်ထားသော စားသောက်ဆိုင်၊ ပန်းချီပြပွဲ သို့မဟုတ် ယဉ်ကျေးမှုပွဲတော်။',
		vibe: 'ယဉ်ကျေးသိမ်မွေ့ပြီး သဟဇာတဖြစ်ကာ ဆက်ဆံရေးကောင်းမွန်သော အငွေ့အသက်။',
		avoid: 'ကြမ်းတမ်းရိုင်းစိုင်းခြင်း သို့မဟုတ် အငြင်းပွားမှုများ ဖန်တီးခြင်း။'
	},
	scorpio: {
		firstMove:
			'ဆန်းကြယ်မှုရှိပါစေ၊ သူတို့ကိုယ်တိုင် ချဉ်းကပ်လာပါစေ — မျက်လုံးချင်းဆုံကြည့်ခြင်းသည် အဓိကဖြစ်ပါသည်။',
		setting: 'မီးမှိန်မှိန် အေးဆေးသော ဘား သို့မဟုတ် နက်နက်နဲနဲ စကားပြောဆိုနိုင်သော နေရာ။',
		vibe: 'နက်ရှိုင်းစူးရှပြီး စိတ်အားထက်သန်ကာ စစ်မှန်မှုရှိသော အငွေ့အသက်။',
		avoid: 'ဟန်ဆောင်လွန်းခြင်း သို့မဟုတ် အခြားသူများနှင့် ပရောပရည်လုပ်ခြင်း။'
	},
	sagittarius: {
		firstMove: 'စိတ်လှုပ်ရှားဖွယ် ခရီးစဉ် သို့မဟုတ် ဆန်းသစ်သော အကြံအစည်တစ်ခုကို မျှဝေဆွေးနွေးပါ။',
		setting:
			'ရုတ်တရက်စီစဉ်သည့် အရာ - မော်တော်ကားခရီးရှည်ထွက်ခြင်း၊ ဖျော်ဖြေပွဲ သို့မဟုတ် ဆိုင်အသစ်များသို့ သွားခြင်း။',
		vibe: 'လွတ်လပ်ပေါ့ပါးပြီး ပျော်စရာကောင်းကာ ဒဿနဆန်သော အငွေ့အသက်။',
		avoid: 'တွယ်ကပ်လွန်းခြင်း သို့မဟုတ် ချုပ်ချယ်လွန်းခြင်း။'
	},
	capricorn: {
		firstMove:
			'ရည်မှန်းချက်ကြီးမားမှုနှင့် သူတို့၏ ရည်မှန်းချက်များကို လေးစားတန်ဖိုးထားကြောင်း ပြသပါ။',
		setting: 'အဆင့်မီညစာစားပွဲ သို့မဟုတ် မိမိ၏ ကြိုးစားအားထုတ်မှုကို ပြသနိုင်သော နေရာ။',
		vibe: 'ရင့်ကျက်ပြီး ရည်မှန်းချက်တိကျကာ အားကိုးထိုက်သော အငွေ့အသက်။',
		avoid: 'ပေါ့ပေါ့ဆဆနေခြင်း သို့မဟုတ် မခိုင်လုံမတည်ကြည်ခြင်း။'
	},
	aquarius: {
		firstMove:
			'ထူးခြားဆန်းသစ်သော အတွေးအမြင်များနှင့် မိမိစိတ်ဝင်စားသော လူမှုအကျိုးပြုအကြောင်းအရာများကို ပြောဆိုပါ။',
		setting: 'ဆန်းကြယ်သော ကော်ဖီဆိုင်၊ နည်းပညာပွဲ သို့မဟုတ် အများပြည်သူဆိုင်ရာ ဆုံဆည်းပွဲ။',
		vibe: 'ဉာဏ်ရည်ဆန်ပြီး ရိုးရာမဆန်သော ခင်မင်ရင်းနှီးမှု အငွေ့အသက်။',
		avoid: 'ရိုးရာဓလေ့ကို အလွန်အမင်းဖက်တွယ်ခြင်း သို့မဟုတ် စိတ်ခံစားမှုအရ ဖိအားပေးတောင်းဆိုခြင်း။'
	},
	pisces: {
		firstMove:
			'နူးညံ့သိမ်မွေ့စွာ၊ တီထွင်ဖန်တီးမှုရှိစွာနှင့် နက်ရှိုင်းသော စိတ်ခံစားချက်ကို ဖော်ပြပါ။',
		setting: 'တိတ်ဆိတ်သော ကမ်းခြေ၊ အနုပညာစတူဒီယို သို့မဟုတ် အေးဆေးစွာ ရုပ်ရှင်ကြည့်ခြင်း။',
		vibe: 'စိတ်ကူးယဉ်ဆန်ပြီး အချစ်ရေးကြည်နူးဖွယ်ကောင်းကာ အလိုလိုသိစိတ်လွှမ်းမိုးသော အငွေ့အသက်။',
		avoid: 'ရုန့်ရင်းကြမ်းတမ်းခြင်း၊ ဆူညံခြင်း သို့မဟုတ် ယုတ္တိဗေဒလွန်ကဲလွန်းခြင်း။'
	}
};

const CONVERSATION_STARTERS: Record<string, string[]> = {
	aries: [
		'What adventure are you planning next?',
		"What's the boldest thing you've ever done?",
		'Pick a superpower — what do you choose?'
	],
	taurus: [
		'What comfort food can you never resist?',
		'Where is your dream vacation spot?',
		'What song always puts you in a good mood?'
	],
	gemini: [
		'What topic could you talk about for hours?',
		'Have you read or watched anything amazing lately?',
		'If you could learn any skill instantly, what would it be?'
	],
	cancer: [
		'What does home mean to you?',
		'Do you have a favorite family tradition?',
		'What makes you feel most at peace?'
	],
	leo: [
		'What are you most proud of?',
		'What makes you light up when you talk about it?',
		'If you could perform anywhere, where would it be?'
	],
	virgo: [
		'What project are you currently working on?',
		'What little thing always makes your day better?',
		'How do you unwind after a long week?'
	],
	libra: [
		'What does balance mean to you?',
		'What aesthetic or style inspires you?',
		'What cause are you passionate about?'
	],
	scorpio: [
		"What is something most people don't know about you?",
		'What drives you on a deep level?',
		"What's a passion you rarely talk about?"
	],
	sagittarius: [
		"What's on your bucket list?",
		"What's the best trip you've ever taken?",
		'What philosophy do you live by?'
	],
	capricorn: [
		'What goal are you working toward right now?',
		'Where do you see yourself in five years?',
		'What achievement are you most proud of?'
	],
	aquarius: [
		'What cause or idea are you most passionate about?',
		'What unique hobby or interest do you have?',
		'If you could change one thing about the world, what would it be?'
	],
	pisces: [
		'What inspires your creativity?',
		'Do you ever have dreams that feel like messages?',
		'What makes you feel most connected to something bigger?'
	]
};

const CONVERSATION_STARTERS_MY: Record<string, string[]> = {
	aries: [
		'နောက်ထပ် ဘယ်လို စွန့်စားခန်းတွေ စီစဉ်ထားလဲ?',
		'ဘဝမှာ အသတ္တိဆုံး လုပ်ခဲ့ဖူးတဲ့ အရာက ဘာလဲ?',
		'စူပါပါဝါ စွမ်းအားတစ်ခုခု ရွေးရမယ်ဆိုရင် ဘာကို ရွေးမလဲ?'
	],
	taurus: [
		'ဘယ်တော့မှ မငြင်းဆန်နိုင်တဲ့ အကြိုက်ဆုံး အစားအစာက ဘာလဲ?',
		'အိပ်မက်ထဲက အလည်အပတ် ခရီးစဉ်နေရာက ဘယ်နေရာလဲ?',
		'စိတ်ကြည်နူးပျော်ရွှင်စေတဲ့ အကြိုက်ဆုံး သီချင်းက ဘာလဲ?'
	],
	gemini: [
		'နာရီပေါင်းများစွာ မရပ်မနား ပြောနိုင်တဲ့ အကြောင်းအရာက ဘာလဲ?',
		'မကြာသေးမီက စိတ်ဝင်စားဖို့ကောင်းတဲ့ စာအုပ် (သို့) ရုပ်ရှင် ကြည့်ဖူးသလား?',
		'ချက်ချင်း တတ်မြောက်နိုင်တဲ့ စွမ်းရည်တစ်ခု ရွေးရမယ်ဆိုရင် ဘာကို ရွေးမလဲ?'
	],
	cancer: [
		'သင့်အတွက် "အိမ်" ဆိုတာ ဘာအဓိပ္ပာယ်ဆောင်သလဲ?',
		'အမြတ်နိုးဆုံး မိသားစု ဓလေ့ထုံးတမ်းလေးတွေ ရှိလား?',
		'စိတ်ကို အအေးချမ်းဆုံး ဖြစ်စေတဲ့ အရာက ဘာလဲ?'
	],
	leo: [
		'ကိုယ့်ကိုယ်ကိုယ် အဂုဏ်ယူရဆုံး အရာက ဘာလဲ?',
		'ပြောလိုက်ရင် မျက်နှာမှာ အပြုံးဝေဆာသွားစေတဲ့ အကြောင်းအရာက ဘာလဲ?',
		'စင်မြင့်တစ်ခုပေါ်မှာ ဖျော်ဖြေခွင့်ရမယ်ဆိုရင် ဘယ်နေရာကို ရွေးမလဲ?'
	],
	virgo: [
		'အခု လက်ရှိ လုပ်ဆောင်နေတဲ့ ပရောဂျက်က ဘာလဲ?',
		'နေ့စဉ်ဘဝကို ပိုမိုလှပစေတဲ့ အသေးအမွှားလေးတွေက ဘာလဲ?',
		'ပင်ပန်းတဲ့ သီတင်းပတ်အပြီးမှာ စိတ်လက်ဘယ်လို အနားယူတတ်လဲ?'
	],
	libra: [
		'သင့်အတွက် "မျှတမှု" ဆိုတာ ဘာလဲ?',
		'စိတ်ကူးဉာဏ်ကို လှုံ့ဆော်ပေးတဲ့ အနုပညာ (သို့) ဖက်ရှင်ပုံစံက ဘာလဲ?',
		'စိတ်အားထက်သန်စွာ ပါဝင်လိုတဲ့ လူမှုရေးကိစ္စက ဘာလဲ?'
	],
	scorpio: [
		'လူအများစု မသိသေးတဲ့ သင့်ရဲ့ လျှို့ဝှက်ချက်လေးက ဘာလဲ?',
		'သင့်ကို ရှေ့ဆက်လှုံ့ဆော်ပေးနေတဲ့ အတွင်းစိတ် စွမ်းအားက ဘာလဲ?',
		'သိပ်မပြောပြဖြစ်ပေမယ့် တကယ်ဝါသနာပါတဲ့ အရာက ဘာလဲ?'
	],
	sagittarius: [
		'ဘဝမှာ သေချာပေါက် လုပ်ကြည့်ချင်တဲ့ ဆန္ဒစာရင်းမှာ ဘာတွေပါလဲ?',
		'သွားခဲ့ဖူးသမျှထဲမှာ အကောင်းဆုံး ခရီးစဉ်က ဘယ်ခရီးလဲ?',
		'ဘဝမှာ လက်ကိုင်ထားတဲ့ ဒဿနက ဘာလဲ?'
	],
	capricorn: [
		'အခု လက်ရှိ အရောက်လှမ်းနေတဲ့ ပန်းတိုင်က ဘာလဲ?',
		'နောက် ၅ နှစ်အတွင်း ကိုယ့်ကိုယ်ကိုယ် ဘယ်နေရာမှာ မြင်ချင်သလဲ?',
		'အမှတ်ရဆုံး အောင်မြင်မှုတစ်ခုက ဘာလဲ?'
	],
	aquarius: [
		'စိတ်အားအထက်သန်ဆုံး အတွေးအခေါ်က ဘာလဲ?',
		'တခြားသူတွေနဲ့ မတူတဲ့ ထူးခြားတဲ့ ဝါသနာလေးတွေ ရှိလား?',
		'ကမ္ဘာကြီးရဲ့ အရာတစ်ခုကို ပြောင်းလဲခွင့်ရရင် ဘာကို ပြောင်းလဲမလဲ?'
	],
	pisces: [
		'သင့်ရဲ့ တီထွင်ဖန်တီးမှုကို ဘာက အားပေးလှုံ့ဆော်သလဲ?',
		'အနာဂတ်နိမိတ်ပြသလို ခံစားရတဲ့ အိပ်မက်တွေ မက်ဖူးလား?',
		'သင့်ထက် ပိုမိုကြီးမြတ်တဲ့အရာတစ်ခုနဲ့ ဆက်သွယ်မိတယ်လို့ ခံစားရစေတဲ့ အရာက ဘာလဲ?'
	]
};

const ELEMENT_INTIMACY_TIPS: Record<string, string> = {
	fire: 'Build trust through shared excitement and honest, direct communication.',
	earth: 'Show reliability and patience — they value consistency over grand gestures.',
	air: 'Keep things mentally stimulating and give them space to think and breathe.',
	water: 'Be emotionally available and create a safe, nurturing space for vulnerability.'
};

const ELEMENT_INTIMACY_TIPS_MY: Record<string, string> = {
	fire: 'စိတ်လှုပ်ရှားဖွယ် အခိုက်အတန့်များကို အတူမျှဝေပြီး ရိုးသားပွင့်လင်းစွာ တိုက်ရိုက်ပြောဆိုခြင်းဖြင့် ယုံကြည်မှု တည်ဆောက်ပါ။',
	earth:
		'အားကိုးထိုက်မှုနှင့် စိတ်ရှည်သည်းခံမှုကို ပြသပါ — သူတို့သည် ဟန်ပြထက် တည်ငြိမ်ခိုင်မြဲမှုကို ပို၍ တန်ဖိုးထားကြသည်။',
	air: 'ဉာဏ်ရည်ဉာဏ်သွေး နိုးကြားစေမည့် အကြောင်းအရာများကို ပြောဆိုပြီး သူတို့အတွက် လွတ်လပ်စွာ တွေးတောနိုင်မည့် နေရာလပ်ပေးပါ။',
	water:
		'စိတ်ခံစားချက်များကို နားထောင်ဖေးမပေးပြီး မိမိ၏ အားနည်းချက်များကို လုံခြုံစိတ်ချစွာ ဖွင့်ဟနိုင်မည့် ပတ်ဝန်းကျင်ကို ဖန်တီးပေးပါ။'
};

const SIGN_DATE_IDEAS: Record<string, string[]> = {
	aries: [
		'High-octane go-kart racing or laser tag',
		'Spontaneous scenic mountain hike with a summit sprint',
		'Axe throwing or energetic retro arcade challenge'
	],
	taurus: [
		'Gourmet farm-to-table wine tasting dinner',
		'Artisanal pastry & espresso tasting at a boutique bakery',
		'Serene botanical garden picnic with decadent desserts'
	],
	gemini: [
		'Interactive escape room challenge or science center',
		'Indie bookstore crawl hopping between lively cafés',
		'Vibrant rooftop cocktail lounge with pub trivia games'
	],
	cancer: [
		'Cozy candlelit home-cooked dinner featuring family recipes',
		'Twilight walk along a peaceful shoreline or tranquil lake',
		'Pottery wheel-throwing masterclass for two'
	],
	leo: [
		'VIP front-row concert or Broadway theater performance',
		'Glamorous rooftop sunset dinner dressed to the nines',
		'Private karaoke suite singing favorite anthems together'
	],
	virgo: [
		'Weekend farmers market followed by making artisanal brunch',
		'Mindful craft workshop, pottery, or terrarium building',
		'Scenic nature trail with a curated photography walk'
	],
	libra: [
		'Contemporary art gallery opening followed by high tea',
		'Chic candlelit jazz club with signature craft cocktails',
		'Scenic stroll through historic architecture and sculpture gardens'
	],
	scorpio: [
		'Hidden speakeasy behind an unmarked door for deep talks',
		'Late-night stargazing at an isolated dark-sky viewpoint',
		'Intriguing immersive theater experience or private tarot salon'
	],
	sagittarius: [
		'Impromptu road trip exploring an unfamiliar historic town',
		'International food festival tasting exotic street delicacies',
		'Outdoor camping under the open sky with fireside stories'
	],
	capricorn: [
		'Architectural landmark walking tour and heritage dining',
		'Private wine and artisan cheese cellar tasting',
		'Symphony orchestra gala or historical museum evening'
	],
	aquarius: [
		'Interactive science or futuristic technology expo',
		'Vintage thrift hunting followed by an unconventional cafe',
		'Indie documentary film screening followed by lively debate'
	],
	pisces: [
		'Bioluminescent evening beach walk or aquarium night tour',
		'Cozy indie cinema screening poetic films with plush seating',
		'Seaside watercolor painting session listening to acoustic melodies'
	]
};

const SIGN_DATE_IDEAS_MY: Record<string, string[]> = {
	aries: [
		'အရှိန်အဟုန်ပြင်းသော ဂိုကတ် (Go-kart) မောင်းပြိုင်ခြင်း',
		'စိတ်လှုပ်ရှားဖွယ် တောင်တက်ခရီးကြမ်း ထွက်ခြင်း',
		'သွက်လက်တက်ကြွသော အာကိတ်ဂိမ်းများ အတူကစားခြင်း'
	],
	taurus: [
		'အရည်အသွေးမြင့် စပျစ်ရည်နှင့် အရသာရှိသော ညစာစားပွဲ',
		'ထင်ရှားသော ကော်ဖီနှင့် မုန့်ဆိုင်လေးတွင် အေးဆေးစကားပြောဆိုခြင်း',
		'ရုက္ခဗေဒဥယျာဉ်တွင် သက်တောင့်သက်သာ ပျော်ပွဲစားထွက်ခြင်း'
	],
	gemini: [
		'ဉာဏ်စမ်း ပဟေဠိအခန်း (Escape room) စိန်ခေါ်ကစားခြင်း',
		'ဆန်းပြားသော စာအုပ်ဆိုင်များနှင့် ကော်ဖီဆိုင်များ လှည့်လည်လည်ပတ်ခြင်း',
		'ခေါင်မိုးပေါ် ဘားတွင် ဉာဏ်စမ်းဂိမ်းကစားရင်း စကားစမြည်ပြောခြင်း'
	],
	cancer: [
		'အိမ်မှာ ဖယောင်းတိုင်မီးထွန်းပြီး ကိုယ်တိုင်ချက်ပြုတ်ကျွေးမွေးသည့် နွေးထွေးသောညစာ',
		'ညနေဆည်းဆာ ကမ်းခြေ သို့မဟုတ် ရေကန်စပ်တွင် အေးချမ်းစွာ လမ်းလျှောက်ခြင်း',
		'နှစ်ယောက်အတူ အိုးလုပ်နည်း လက်တွေ့သင်တန်းတက်ခြင်း'
	],
	leo: [
		'စင်မြင့်ရှေ့ဆုံးတန်းမှ တေးဂီတဖျော်ဖြေပွဲ သို့မဟုတ် ပြဇာတ်ကြည့်ရှုခြင်း',
		'ခမ်းနားထည်ဝါသော ဝတ်စုံဖြင့် ခေါင်မိုးပေါ်တွင် နေဝင်ဆည်းဆာ ညစာစားခြင်း',
		'သီးသန့် ကာရာအိုကေခန်းတွင် စိတ်ကြိုက်သီချင်းဆိုခြင်း'
	],
	virgo: [
		'မနက်ခင်း သဘာဝလတ်ဆတ်သော ဈေးတန်းတွင် ဈေးဝယ်ပြီး အရသာရှိသော နံနက်စာအတူချက်ပြုတ်ခြင်း',
		'သစ်ပင်စိုက်ပျိုးနည်း သို့မဟုတ် လက်မှုပညာ အလုပ်ရုံဆွေးနွေးပွဲတက်ခြင်း',
		'သဘာဝရှုခင်းဓာတ်ပုံရိုက်ရင်း လမ်းလျှောက်ခြင်း'
	],
	libra: [
		'ခေတ်ပေါ်အနုပညာပြပွဲ သွားရောက်ကြည့်ရှုပြီး လက်ဖက်ရည်ဝိုင်းဖွဲ့ခြင်း',
		'ဖယောင်းတိုင်မီးအောက်တွင် ဂျက်ဇ် (Jazz) တေးဂီတနားဆင်ရင်း ကော့တေးသောက်ခြင်း',
		'သမိုင်းဝင် ဗိသုကာလက်ရာများနှင့် ပန်းခြံများတွင် လမ်းလျှောက်ခြင်း'
	],
	scorpio: [
		'လျှို့ဝှက်ဆန်းကြယ်သော တံခါးဝှက်ဘားတွင် နက်နဲသော စကားဝိုင်းဖွဲ့ခြင်း',
		'ညဉ့်နက်ချိန် တိတ်ဆိတ်သော တောင်ကုန်းပေါ်မှ ကြယ်တာရာများ ကြည့်ရှုခြင်း',
		'ဆန်းကြယ်သော တားရော့ဗေဒင်နှင့် စိတ်ပညာဆွေးနွေးပွဲ သွားရောက်ခြင်း'
	],
	sagittarius: [
		'မရောက်ဖူးသေးသော မြို့လေးဆီသို့ ရုတ်တရက် မော်တော်ကားဖြင့် ခရီးထွက်ခြင်း',
		'နိုင်ငံတကာ လမ်းဘေးအစားအစာ စုံလင်စွာ မြည်းစမ်းသည့် ပွဲတော်သွားခြင်း',
		'တောတွင်း တဲထိုးအိပ်ပြီး မီးပုံပွဲလုပ်ရင်း စကားပြောခြင်း'
	],
	capricorn: [
		'သမိုင်းဝင် အထင်ကရနေရာများသို့ သွားရောက်လေ့လာပြီး နာမည်ကြီးစားသောက်ဆိုင်တွင် ညစာစားခြင်း',
		'ဗိသုကာလက်ရာပြတိုက်ကြီးများသို့ သွားရောက်ခြင်း',
		'အရည်အသွေးမြင့် စပျစ်ရည်နှင့် ဒိန်ခဲ မြည်းစမ်းပွဲသို့ သွားခြင်း'
	],
	aquarius: [
		'အပြန်အလှန်တုံ့ပြန်နိုင်သော နည်းပညာနှင့် သိပ္ပံပြပွဲသို့ သွားရောက်ခြင်း',
		'ထူးခြားဆန်းပြားသော ရှေးဟောင်းပစ္စည်းများ ရှာဖွေဝယ်ယူပြီး ဆန်းသစ်သော ကော်ဖီဆိုင်သို့ သွားခြင်း',
		'သီးသန့်ရုပ်ရှင်ပွဲ ကြည့်ရှုပြီး အမြင်ချင်းဖလှယ်ဆွေးနွေးခြင်း'
	],
	pisces: [
		'ညဘက် ရေနေသတ္တဝါပြတိုက် သို့မဟုတ် လရောင်အောက် ကမ်းခြေလမ်းလျှောက်ခြင်း',
		'သက်တောင့်သက်သာ အနားယူနိုင်သော ရုပ်ရှင်ရုံတွင် စိတ်ကူးယဉ်ရုပ်ရှင် အတူကြည့်ခြင်း',
		'ကမ်းနားတွင် တေးဂီတနားဆင်ရင်း ရေဆေးပန်းချီ အတူဆွဲခြင်း'
	]
};

function elementOf(sign: string): string {
	const map: Record<string, string> = {
		aries: 'fire',
		leo: 'fire',
		sagittarius: 'fire',
		taurus: 'earth',
		virgo: 'earth',
		capricorn: 'earth',
		gemini: 'air',
		libra: 'air',
		aquarius: 'air',
		cancer: 'water',
		scorpio: 'water',
		pisces: 'water'
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

export function getApproachTips(
	sign1: string,
	sign2: string,
	locale: SupportedLocale = 'en'
): ApproachTips {
	const targetSign = (sign2 || 'aries').toLowerCase().trim();
	const targetElement = elementOf(targetSign);

	if (locale === 'my') {
		const tips = APPROACH_TIPS_MY[targetSign] || APPROACH_TIPS_MY.aries;
		const starters = CONVERSATION_STARTERS_MY[targetSign] || CONVERSATION_STARTERS_MY.aries;
		const sharedIdeas = SIGN_DATE_IDEAS_MY[targetSign] || SIGN_DATE_IDEAS_MY.aries;
		return {
			approach: tips,
			conversationStarters: starters,
			dateIdeas: sharedIdeas,
			intimacyTip: ELEMENT_INTIMACY_TIPS_MY[targetElement] || ''
		};
	}

	const tips = APPROACH_TIPS[targetSign] || APPROACH_TIPS.aries;
	const starters = CONVERSATION_STARTERS[targetSign] || CONVERSATION_STARTERS.aries;
	const sharedIdeas = SIGN_DATE_IDEAS[targetSign] || SIGN_DATE_IDEAS.aries;

	return {
		approach: tips,
		conversationStarters: starters,
		dateIdeas: sharedIdeas,
		intimacyTip: ELEMENT_INTIMACY_TIPS[targetElement] || ''
	};
}
