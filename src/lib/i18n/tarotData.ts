import type { TarotCardTranslation, SupportedLocale } from './types';
import { getZodiacTranslation, formatElement } from './zodiacData';

export const TAROT_CARDS_DATA: Record<string, TarotCardTranslation> = {
	// 22 MAJOR ARCANA
	'The Fool': {
		nameEn: 'The Fool',
		nameMy: 'လူမိုက် (သို့) အစပြုသူ',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ (အဓိကနက်နဲသောအရာ)',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Beginnings', 'Innocence', 'Spontaneity', 'Free spirit'],
		keywordsMy: ['အစပြုခြင်း', 'အပြစ်ကင်းစင်မှု', 'အလိုက်သင့်ဖြစ်တည်မှု', 'လွတ်လပ်သောစိတ်'],
		meaningUprightEn:
			'New beginnings, innocence, spontaneity, leap of faith, following one’s heart.',
		meaningUprightMy:
			'ခရီးသစ်စတင်ခြင်း၊ မကြောက်မရွံ့ယုံကြည်စွာရှေ့ဆက်ခြင်း၊ လွတ်လပ်မှုနှင့် ဖြစ်တည်မှုအသစ်။',
		meaningReversedEn: 'Recklessness, risk-taking, holding back, naive mistakes.',
		meaningReversedMy:
			'မဆင်မခြင်စွန့်စားလွန်းခြင်း၊ သတိလက်လွတ်ဖြစ်ခြင်း၊ အသစ်စတင်ရန် တွန့်ဆုတ်နေခြင်း။'
	},
	'The Magician': {
		nameEn: 'The Magician',
		nameMy: 'မှော်ဆရာ',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Manifestation', 'Resourcefulness', 'Power', 'Inspired action'],
		keywordsMy: [
			'လက်တွေ့ဖန်တီးနိုင်မှု',
			'အရင်းအမြစ်ကြွယ်ဝမှု',
			'စွမ်းအား',
			'လှုံ့ဆော်မှုရှိသောလှုပ်ရှားမှု'
		],
		meaningUprightEn:
			'Desire turned into reality, resourcefulness, willpower, manifestation power.',
		meaningUprightMy:
			'ရည်မှန်းချက်များကို လက်တွေ့အကောင်အထည်ဖော်နိုင်ခြင်း၊ စိတ်စွမ်းအားနှင့် ကျွမ်းကျင်မှုအပြည့်ရှိခြင်း။',
		meaningReversedEn: 'Manipulation, poor planning, untapped talents, wasted energy.',
		meaningReversedMy: 'လိမ်လည်လှည့်ဖြားမှု၊ အစီအစဉ်မကျနမှု၊ မိမိစွမ်းရည်ကို အလဟဿဖြစ်စေခြင်း။'
	},
	'The High Priestess': {
		nameEn: 'The High Priestess',
		nameMy: 'မဟာယဇ်ပုရောဟိတ်မ',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Intuition', 'Sacred knowledge', 'Divine feminine', 'Subconscious'],
		keywordsMy: ['အတွင်းစိတ်အာရုံ', 'နက်နဲသောအသိပညာ', 'အမျိုးသမီးစွမ်းအင်', 'မသိစိတ်'],
		meaningUprightEn: 'Intuition, mystery, subconscious insight, inner spiritual wisdom.',
		meaningUprightMy:
			'ဆဋ္ဌမအာရုံ အလွန်အားကောင်းခြင်း၊ လျှို့ဝှက်နက်နဲသောအသိ၊ အတွင်းစိတ်၏လမ်းပြမှုကို ယုံကြည်ရန်လိုအပ်ခြင်း။',
		meaningReversedEn: 'Secrets, withdrawal, silence, ignored intuition, hidden agendas.',
		meaningReversedMy:
			'အတွင်းစိတ်အသံကို လျစ်လျူရှုမိခြင်း၊ လျှို့ဝှက်ချက်များ၊ စိတ်ခံစားမှုနောက်ဆုတ်နေခြင်း။'
	},
	'The Empress': {
		nameEn: 'The Empress',
		nameMy: 'ဧကရီဘုရင်မ',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Femininity', 'Beauty', 'Nature', 'Abundance', 'Nurturing'],
		keywordsMy: ['နွေးထွေးယုယမှု', 'လှပတင့်တယ်ခြင်း', 'သဘာဝတရား', 'ပေါများကြွယ်ဝခြင်း', 'မေတ္တာ'],
		meaningUprightEn: 'Abundance, fertility, creativity, nurturing love, luxury and harmony.',
		meaningUprightMy:
			'ကြွယ်ဝချမ်းသာခြင်း၊ အောင်မြင်ဖြစ်ထွန်းခြင်း၊ နွေးထွေးသောချစ်ခြင်းနှင့် ဖန်တီးနိုင်စွမ်း။',
		meaningReversedEn: 'Creative block, dependence, smothering, disharmony.',
		meaningReversedMy:
			'ဖန်တီးမှုအားနည်းခြင်း၊ သူတစ်ပါးအပေါ် မှီခိုလွန်းခြင်း၊ မိမိကိုယ်ကို ဂရုမစိုက်မိခြင်း။'
	},
	'The Emperor': {
		nameEn: 'The Emperor',
		nameMy: 'ဧကရာဇ်မင်း',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Authority', 'Structure', 'Control', 'Father figure', 'Leadership'],
		keywordsMy: ['ဩဇာအာဏာ', 'စနစ်တကျစည်းကမ်း', 'ထိန်းချုပ်နိုင်စွမ်း', 'ခေါင်းဆောင်မှု'],
		meaningUprightEn: 'Stability, structure, leadership, authority, disciplined focus.',
		meaningUprightMy:
			'ခိုင်မာသောတည်ငြိမ်မှု၊ စည်းကမ်းသေဝပ်မှု၊ ဩဇာတိက္ကမနှင့် ခေါင်းဆောင်မှုအရည်အသွေး။',
		meaningReversedEn: 'Tyranny, rigidity, loss of control, abuse of power.',
		meaningReversedMy: 'တင်းကျပ်လွန်းခြင်း၊ အာဏာအလွဲသုံးစားလုပ်ခြင်း၊ ထိန်းချုပ်မှုကင်းမဲ့ခြင်း။'
	},
	'The Hierophant': {
		nameEn: 'The Hierophant',
		nameMy: 'ဘာသာရေးဆရာကြီး',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Spiritual wisdom', 'Tradition', 'Belief systems', 'Institutions'],
		keywordsMy: ['ဓလေ့ထုံးတမ်း', 'ဝိညာဉ်ရေးရာအသိ', 'ယုံကြည်မှုစနစ်', 'ဆရာသမား'],
		meaningUprightEn: 'Spiritual guidance, tradition, conforming to higher wisdom, education.',
		meaningUprightMy:
			'ရိုးရာဓလေ့နှင့် စည်းမျဉ်းများ၊ ပညာသင်ကြားခြင်း၊ လေးစားရသောဆရာသမား၏ လမ်းညွှန်မှု။',
		meaningReversedEn: 'Rebellion, unconventional beliefs, new approaches, dogmatism.',
		meaningReversedMy:
			'ထုံးတမ်းစဉ်လာကို ဆန့်ကျင်ခြင်း၊ ကိုယ်ပိုင်လမ်းစဉ်သစ်ရှာဖွေခြင်း၊ အယူသီးလွန်းခြင်း။'
	},
	'The Lovers': {
		nameEn: 'The Lovers',
		nameMy: 'ချစ်သူများ',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Love', 'Harmony', 'Relationships', 'Values alignment', 'Choices'],
		keywordsMy: ['အချစ်ရေး', 'သဟဇာတဖြစ်မှု', 'ဆက်ဆံရေး', 'တန်ဖိုးထားမှုတူညီခြင်း', 'ရွေးချယ်မှု'],
		meaningUprightEn: 'True love, soul alignment, union, vital choices guided by value.',
		meaningUprightMy:
			'နက်ရှိုင်းသောချစ်ခြင်းမေတ္တာ၊ အရေးကြီးသောဘဝရွေးချယ်မှု၊ အတွေးအခေါ်တန်ဖိုးချင်း ကိုက်ညီမှု။',
		meaningReversedEn: 'Disharmony, misalignment of values, indecision, broken trust.',
		meaningReversedMy: 'သဘောထားကွဲလွဲခြင်း၊ ဆက်ဆံရေးအဆင်မပြေမှု၊ အဆုံးအဖြတ်မချနိုင်ခြင်း။'
	},
	'The Chariot': {
		nameEn: 'The Chariot',
		nameMy: 'စစ်ရထား',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Control', 'Willpower', 'Success', 'Determination', 'Action'],
		keywordsMy: ['ထိန်းချုပ်နိုင်စွမ်း', 'ဇွဲလုံ့လ', 'အောင်မြင်မှု', 'ပြတ်သားသောဆန္ဒ'],
		meaningUprightEn: 'Triumph over adversity, momentum, willpower, overcoming opposing forces.',
		meaningUprightMy:
			'အခက်အခဲများကို ကျော်လွှားနိုင်ခြင်း၊ အောင်မြင်မှုဆီသို့ အရှိန်အဟုန်ဖြင့် ချီတက်ခြင်း၊ ခိုင်မာသောဇွဲ။',
		meaningReversedEn: 'Lack of direction, aggression, feeling powerless, obstacles.',
		meaningReversedMy:
			'ဦးတည်ချက်ပျောက်ဆုံးခြင်း၊ ထိန်းမနိုင်သိမ်းမရဖြစ်ခြင်း၊ အတားအဆီးများ ကြုံတွေ့ရခြင်း။'
	},
	Strength: {
		nameEn: 'Strength',
		nameMy: 'ခွန်အားနှင့် သည်းခံခြင်း',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Courage', 'Patience', 'Compassion', 'Inner strength', 'Gentle power'],
		keywordsMy: ['သတ္တိ', 'သည်းခံခြင်း', 'ကရုဏာ', 'အတွင်းစိတ်ခွန်အား', 'နူးညံ့သောစွမ်းအား'],
		meaningUprightEn:
			'Mastering inner impulses through compassion, quiet bravery, emotional endurance.',
		meaningUprightMy:
			'နူးညံ့မှုဖြင့် အောင်နိုင်ခြင်း၊ စိတ်ရှည်သည်းခံနိုင်စွမ်း၊ အတွင်းစိတ်၏ မယိမ်းယိုင်သောသတ္တိ။',
		meaningReversedEn: 'Self-doubt, weakness, insecurity, raw aggression, exhaustion.',
		meaningReversedMy:
			'မိမိကိုယ်ကို သံသယဝင်ခြင်း၊ အားငယ်ခြင်း၊ စိတ်မထိန်းနိုင်ဘဲ ဒေါသထွက်လွယ်ခြင်း။'
	},
	'The Hermit': {
		nameEn: 'The Hermit',
		nameMy: 'ရသေ့ (သို့) ဆင်ခြင်တွေးတောသူ',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Soul-searching', 'Introspection', 'Solitude', 'Inner guidance'],
		keywordsMy: [
			'မိမိကိုယ်ကိုဆန်းစစ်ခြင်း',
			'ဆင်ခြင်တွေးတောမှု',
			'တိတ်ဆိတ်ငြိမ်သက်ခြင်း',
			'အတွင်းလမ်းပြ'
		],
		meaningUprightEn: 'Seeking inner truth, spiritual retreat, reflective solitude, mentorship.',
		meaningUprightMy:
			'အတွင်းစိတ်အမှန်တရားကို ရှာဖွေခြင်း၊ ဆိတ်ငြိမ်ရာတွင် အဖြေရှာခြင်း၊ ဉာဏ်အလင်းပွင့်လန်းခြင်း။',
		meaningReversedEn: 'Isolation, loneliness, anti-social withdrawal, lost in thoughts.',
		meaningReversedMy:
			'တစ်ကိုယ်တည်းအထီးကျန်ဆန်လွန်းခြင်း၊ ပတ်ဝန်းကျင်နှင့် အဆက်အသွယ်ပြတ်တောက်ခြင်း။'
	},
	'Wheel of Fortune': {
		nameEn: 'Wheel of Fortune',
		nameMy: 'ကံကြမ္မာစက်ဘီး',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Good luck', 'Karma', 'Life cycles', 'Destiny', 'Turning point'],
		keywordsMy: ['ကံကောင်းခြင်း', 'ကံကြမ္မာ', 'ဘဝစက်ဝန်း', 'ကံအလှည့်အပြောင်း', 'အပြောင်းအလဲကြီး'],
		meaningUprightEn:
			'Fortuitous turn of events, positive destiny, cycles of progress, adaptability.',
		meaningUprightMy:
			'ဘဝ၏ အလှည့်အပြောင်းကောင်းများရောက်ရှိလာခြင်း၊ ကံတရား၏ အကူအညီရရှိခြင်း၊ သံသရာစက်ဝန်း။',
		meaningReversedEn:
			'Bad luck, resistance to change, unexpected disruptions, breaking negative cycles.',
		meaningReversedMy: 'ကံအခွင့်အရေးလွဲချော်ခြင်း၊ အပြောင်းအလဲကို လက်မခံနိုင်ခြင်း၊ အခက်အခဲကာလ။'
	},
	Justice: {
		nameEn: 'Justice',
		nameMy: 'တရားမျှတမှု',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Fairness', 'Truth', 'Cause and effect', 'Law', 'Accountability'],
		keywordsMy: ['တရားမျှတခြင်း', 'အမှန်တရား', 'အကြောင်းနှင့်အကျိုး', 'ဥပဒေ', 'တာဝန်ယူမှု'],
		meaningUprightEn: 'Truth, balance, moral integrity, legal success, balanced karma.',
		meaningUprightMy:
			'အမှန်တရားနှင့် တရားမျှတမှု၊ မိမိလုပ်ရပ်အတွက် တာဝန်ယူနိုင်ခြင်း၊ မျှတသောဆုံးဖြတ်ချက်။',
		meaningReversedEn: 'Dishonesty, unfair treatment, unaccountability, legal complications.',
		meaningReversedMy: 'မမျှတမှုကြုံရခြင်း၊ အမှန်တရားကို ဖုံးကွယ်ထားခြင်း၊ တာဝန်မဲ့မှု။'
	},
	'The Hanged Man': {
		nameEn: 'The Hanged Man',
		nameMy: 'ဇောက်ထိုးဆွဲထားသူ (စွန့်လွှတ်ခြင်း)',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Surrender', 'Letting go', 'New perspectives', 'Sacrifice', 'Pause'],
		keywordsMy: ['အလျော့ပေးခြင်း', 'လက်လွှတ်စွန့်လွှတ်ခြင်း', 'အမြင်သစ်ရရှိခြင်း', 'ခဏရပ်နားခြင်း'],
		meaningUprightEn: 'Gaining higher perspective through stillness, willing surrender, patience.',
		meaningUprightMy:
			'အခြေအနေကို အမြင်သစ်ဖြင့် ကြည့်မြင်ခြင်း၊ ခေတ္တရပ်နား၍ အချိန်ပေးဆင်ခြင်ခြင်း၊ စွန့်လွှတ်အနစ်နာခံခြင်း။',
		meaningReversedEn: 'Stalling, needless martyrdom, resistance to insight, stagnation.',
		meaningReversedMy:
			'အချည်းနှီးအနစ်နာခံမိခြင်း၊ ကြန့်ကြာမှုများပြားခြင်း၊ အပြောင်းအလဲကို ငြင်းဆန်ခြင်း။'
	},
	Death: {
		nameEn: 'Death',
		nameMy: 'အဆုံးသတ်နှင့် အသစ်ဖြစ်တည်ခြင်း',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Endings', 'Change', 'Transformation', 'Transition', 'Rebirth'],
		keywordsMy: [
			'အဆုံးသတ်ခြင်း',
			'အသွင်ပြောင်းလဲခြင်း',
			'အသစ်ပြန်လည်မွေးဖွားခြင်း',
			'ဘဝအလှည့်အပြောင်း'
		],
		meaningUprightEn:
			'End of an era, profound transformation, letting go of the old to welcome the new.',
		meaningUprightMy:
			'ဟောင်းနွမ်းသောအရာများ အဆုံးသတ်ပြီး အသစ်စတင်ရန် အခွင့်အလမ်းရောက်လာခြင်း၊ အကြီးအကျယ်ပြောင်းလဲခြင်း။',
		meaningReversedEn: 'Resistance to change, lingering attachments, stagnant inertia.',
		meaningReversedMy:
			'အဟောင်းကို တွယ်ကပ်နေမိခြင်း၊ အပြောင်းအလဲကို ကြောက်ရွံ့ခြင်း၊ တိုးတက်မှုရပ်တန့်နေခြင်း။'
	},
	Temperance: {
		nameEn: 'Temperance',
		nameMy: 'မျှတခြင်းနှင့် သဟဇာတ',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Balance', 'Moderation', 'Patience', 'Purpose', 'Healing'],
		keywordsMy: ['မျှတမှု', 'အလယ်အလတ်လမ်းစဉ်', 'သည်းခံခြင်း', 'ရည်ရွယ်ချက်', 'ကုစားခြင်း'],
		meaningUprightEn: 'Harmony, emotional calm, moderation, blending opposing elements smoothly.',
		meaningUprightMy:
			'မျှတသော အလယ်အလတ်လမ်းစဉ်၊ စိတ်အေးချမ်းမှု၊ စိတ်ရှည်မှုဖြင့် အောင်မြင်ခြင်း၊ ကုစားခြင်း။',
		meaningReversedEn: 'Imbalance, excess, clashing, impatience, hasty decisions.',
		meaningReversedMy: 'အစွန်းရောက်လွန်းခြင်း၊ သဟဇာတမဖြစ်ခြင်း၊ စိတ်မရှည်ဘဲ အလျင်စလိုလုပ်မိခြင်း။'
	},
	'The Devil': {
		nameEn: 'The Devil',
		nameMy: 'မာရ်နတ် (နှောင်ကြိုးနှင့် စွဲလမ်းမှု)',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Shadow self', 'Attachment', 'Addiction', 'Restriction', 'Illusion'],
		keywordsMy: [
			'စွဲလမ်းမှု',
			'နှောင်ကြိုး',
			'စိတ်အလိုလိုက်ခြင်း',
			'ကန့်သတ်ချုပ်ချယ်မှု',
			'ထောင်ချောက်'
		],
		meaningUprightEn:
			'Unhealthy attachments, material illusion, hidden shadows needing acknowledgment.',
		meaningUprightMy:
			'မကောင်းသော စွဲလမ်းမှုနှင့် နှောင်ကြိုးများ၊ ရုပ်ဝတ္ထုအပေါ် သာယာမိခြင်း၊ မိမိကိုယ်ကို ချုပ်နှောင်ထားခြင်း။',
		meaningReversedEn: 'Breaking free, release of toxic habits, reclaiming independence.',
		meaningReversedMy:
			'မကောင်းသော နှောင်ကြိုးများမှ လွတ်မြောက်ခြင်း၊ အကျင့်ဆိုးများကို စွန့်လွှတ်နိုင်ခြင်း။'
	},
	'The Tower': {
		nameEn: 'The Tower',
		nameMy: 'မျှော်စင်ပြိုကျခြင်း (ရုတ်တရက်ပြောင်းလဲမှု)',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Sudden change', 'Upheaval', 'Chaos', 'Revelation', 'Awakening'],
		keywordsMy: [
			'ရုတ်တရက်ပြိုလဲမှု',
			'မမျှော်လင့်သောအပြောင်းအလဲ',
			'အမှန်တရားပေါ်ပေါက်ခြင်း',
			'နိုးထခြင်း'
		],
		meaningUprightEn:
			'Shattering illusions, sudden revelations, foundation rebuilt on authentic truth.',
		meaningUprightMy:
			'မမျှော်လင့်ဘဲ အခြေခံအုတ်မြစ်များ ပြိုလဲပျက်စီးခြင်း၊ အမှန်တရားပေါ်ပေါက်ပြီး အသစ်ပြန်တည်ဆောက်ရခြင်း။',
		meaningReversedEn: 'Averting disaster, delayed inevitable change, fear of suffering.',
		meaningReversedMy:
			'ဘေးဒုက္ခမှ သီသီလေးလွတ်မြောက်ခြင်း၊ ရှောင်လွှဲမရသော အပြောင်းအလဲကို ရွှေ့ဆိုင်းနေခြင်း။'
	},
	'The Star': {
		nameEn: 'The Star',
		nameMy: 'ကြယ်တာရာ (မျှော်လင့်ချက်)',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Hope', 'Faith', 'Purpose', 'Renewal', 'Spirituality', 'Inspiration'],
		keywordsMy: [
			'မျှော်လင့်ချက်',
			'ယုံကြည်မှု',
			'ပြန်လည်နိုးထခြင်း',
			'စိတ်ဓာတ်ခွန်အား',
			'အေးချမ်းမှု'
		],
		meaningUprightEn: 'Renewed hope, inspiration, serene clarity, peaceful healing after storms.',
		meaningUprightMy:
			'မျှော်လင့်ချက်ရောင်ခြည်သစ် သန်းလာခြင်း၊ စိတ်နှလုံးချမ်းမြေ့ခြင်း၊ အနာဂတ်အတွက် ယုံကြည်မှုအပြည့်ရှိခြင်း။',
		meaningReversedEn: 'Despair, loss of faith, discouragement, feeling disconnected.',
		meaningReversedMy:
			'မျှော်လင့်ချက်မဲ့သလို ခံစားရခြင်း၊ ယုံကြည်မှုအားနည်းခြင်း၊ အဆိုးမြင်စိတ်ဝင်ခြင်း။'
	},
	'The Moon': {
		nameEn: 'The Moon',
		nameMy: 'လမင်း (စိတ်ကူးယဉ်နှင့် မရေရာမှု)',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Illusion', 'Fear', 'Anxiety', 'Subconscious', 'Intuition'],
		keywordsMy: ['စိတ်ကူးယဉ်မှု', 'စိုးရိမ်ပူပန်မှု', 'မရေရာမှု', 'မျက်လှည့်နှင့်ထင်ယောင်ထင်မှား'],
		meaningUprightEn:
			'Navigating shadows, trusting intuition despite foggy clarity, dreams unveiling truth.',
		meaningUprightMy:
			'မရေရာမှုနှင့် စိုးရိမ်စိတ်များ ရှိနေခြင်း၊ အရာအားလုံး မထင်ရှားသေးခြင်း၊ မိမိအတွင်းစိတ်အာရုံကို သတိထားရမည့်အချိန်။',
		meaningReversedEn: 'Release of fear, clarity dawning, dispelling deception.',
		meaningReversedMy:
			'မရေရာမှုများ ပျောက်ကွယ်သွားခြင်း၊ အမှန်တရားပေါ်လွင်လာခြင်း၊ စိုးရိမ်စိတ် လျော့ပါးသွားခြင်း။'
	},
	'The Sun': {
		nameEn: 'The Sun',
		nameMy: 'နေမင်း (အောင်မြင်မှုနှင့် ပျော်ရွှင်မှု)',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Positivity', 'Joy', 'Success', 'Warmth', 'Vitality', 'Celebration'],
		keywordsMy: [
			'အပြုသဘောဆောင်မှု',
			'ပျော်ရွှင်ချမ်းမြေ့ခြင်း',
			'အောင်မြင်မှု',
			'တောက်ပမှု',
			'ခွန်အား'
		],
		meaningUprightEn: 'Radiant success, vitality, pure joy, confidence, warmth and abundance.',
		meaningUprightMy:
			'အလွန်တောက်ပသော အောင်မြင်မှုနှင့် ပျော်ရွှင်မှု၊ စိတ်ကြည်လင်လန်းဆန်းခြင်း၊ ကံကောင်းခြင်းအပြည့်ရှိခြင်း။',
		meaningReversedEn: 'Temporary sadness, missed optimism, clouded happiness.',
		meaningReversedMy:
			'ယာယီအားလျော့ခြင်း၊ အလွန်အကျွံအကောင်းမြင်လွန်းခြင်း၊ ပျော်ရွှင်မှုခေတ္တမှေးမှိန်ခြင်း။'
	},
	Judgement: {
		nameEn: 'Judgement',
		nameMy: 'တရားစီရင်ခြင်း (နိုးကြားတန်ဖိုးထားမှု)',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Rebirth', 'Inner calling', 'Absolution', 'Awakening', 'Clarity'],
		keywordsMy: ['ပြန်လည်ရှင်သန်ခြင်း', 'ဘဝခေါ်သံ', 'ဆင်ခြင်တုံတရား', 'အသိအမြင်သစ်ရရှိခြင်း'],
		meaningUprightEn: 'Spiritual awakening, reckoning, hearing your true calling, life evaluation.',
		meaningUprightMy:
			'ဘဝ၏ အရေးပါသောခေါ်သံကို ကြားသိရခြင်း၊ အတိတ်ကို သင်ခန်းစာယူ၍ အသစ်ပြန်စတင်ခြင်း၊ ဉာဏ်အလင်းရခြင်း။',
		meaningReversedEn: 'Self-doubt, harsh self-judgment, ignoring life’s calling, regret.',
		meaningReversedMy:
			'မိမိကိုယ်ကို အပြစ်တင်လွန်းခြင်း၊ အဆုံးအဖြတ်ချရန် မဝံ့မရဲဖြစ်ခြင်း၊ အခွင့်အရေးကို လျစ်လျူရှုမိခြင်း။'
	},
	'The World': {
		nameEn: 'The World',
		nameMy: 'ကမ္ဘာလောက (ပြည့်စုံခြင်း)',
		arcanaEn: 'Major Arcana',
		arcanaMy: 'မေဂျာအာခါနာ',
		suitEn: 'Major',
		suitMy: 'မေဂျာ',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Completion', 'Integration', 'Accomplishment', 'Travel', 'Wholeness'],
		keywordsMy: [
			'ပြည့်စုံပြီးမြောက်ခြင်း',
			'အောင်မြင်မှုအထွတ်အထိပ်',
			'ခရီးသွားလာခြင်း',
			'လုံးစုံပြည့်စုံမှု'
		],
		meaningUprightEn:
			'Fulfillment of a cycle, ultimate victory, holistic integration, global expansion.',
		meaningUprightMy:
			'ရည်မှန်းချက်များ ပြီးမြောက်အောင်မြင်ခြင်း၊ ဘဝအဆင့်သစ်သို့ ကူးပြောင်းခြင်း၊ စိတ်ချမ်းသာပြည့်စုံမှု။',
		meaningReversedEn: 'Incompletion, lingering loose ends, short of the finish line.',
		meaningReversedMy:
			'ပြီးပြည့်စုံရန် အနည်းငယ်ကျန်ရှိနေခြင်း၊ မပြီးပြတ်သေးသောကိစ္စများ၊ ပိတ်မိနေသလိုခံစားရခြင်း။'
	},

	// 14 WANDS (FIRE) - တုတ်ချောင်းများ
	'Ace of Wands': {
		nameEn: 'Ace of Wands',
		nameMy: 'တုတ် ၁ ချောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Inspiration', 'Creative spark', 'New passion', 'Enthusiasm'],
		keywordsMy: ['စိတ်ကူးစိတ်သန်းသစ်', 'တီထွင်ဖန်တီးမှုမီးပွား', 'စိတ်အားထက်သန်မှု', 'အစပြုမှု'],
		meaningUprightEn: 'A sudden burst of creative inspiration, fresh passion, dynamic ambition.',
		meaningUprightMy:
			'တီထွင်ဖန်တီးမှုနှင့် စိတ်အားထက်သန်မှုအသစ်များ ရုတ်တရက်ပေါ်ပေါက်လာခြင်း၊ စတင်လှုပ်ရှားရန် အခွင့်ကောင်း။',
		meaningReversedEn: 'Delays, lack of motivation, creative blockage, hesitation.',
		meaningReversedMy:
			'စိတ်အားထက်သန်မှု လျော့နည်းခြင်း၊ ဖန်တီးမှုပိတ်ဆို့နေခြင်း၊ စတင်ရန် တွန့်ဆုတ်နေခြင်း။'
	},
	'Two of Wands': {
		nameEn: 'Two of Wands',
		nameMy: 'တုတ် ၂ ချောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Planning', 'Future focus', 'Decisions', 'Discovery'],
		keywordsMy: [
			'အနာဂတ်အစီအစဉ်',
			'ရှေ့ရေးမျှော်တွေးခြင်း',
			'ရွေးချယ်ဆုံးဖြတ်မှု',
			'လေ့လာစူးစမ်းခြင်း'
		],
		meaningUprightEn:
			'Making plans for the future, weighing options, looking out at vast horizons.',
		meaningUprightMy:
			'ရှေ့ဆက်ရမည့် အစီအစဉ်များကို ရေးဆွဲခြင်း၊ အခွင့်အလမ်းများကို ချိန်ဆသုံးသပ်ခြင်း။',
		meaningReversedEn: 'Fear of unknown, poor planning, hesitation to take risks.',
		meaningReversedMy:
			'မသေချာမှုကို ကြောက်ရွံ့ခြင်း၊ အစီအစဉ်ချွတ်ချော်ခြင်း၊ မဆုံးဖြတ်နိုင်ဖြစ်ခြင်း။'
	},
	'Three of Wands': {
		nameEn: 'Three of Wands',
		nameMy: 'တုတ် ၃ ချောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Expansion', 'Foresight', 'Overseas opportunities', 'Confidence'],
		keywordsMy: ['တိုးချဲ့ခြင်း', 'အမြော်အမြင်', 'ခရီးဝေးအခွင့်အလမ်း', 'ယုံကြည်မှု'],
		meaningUprightEn:
			'Seeing initial plans bear fruit, expanding operations, looking outward with confidence.',
		meaningUprightMy:
			'လုပ်ငန်းများ တိုးချဲ့ခွင့်ရခြင်း၊ ကြိုးစားမှုများ၏ အကျိုးရလဒ် စတင်မြင်တွေ့ရခြင်း၊ ခရီးရှည်အလားအလာကောင်းခြင်း။',
		meaningReversedEn: 'Obstacles to expansion, delays, unmet expectations.',
		meaningReversedMy: 'တိုးချဲ့ရာတွင် အခက်အခဲကြုံခြင်း၊ မျှော်လင့်သလောက် မခရီးရောက်ခြင်း။'
	},
	'Four of Wands': {
		nameEn: 'Four of Wands',
		nameMy: 'တုတ် ၄ ချောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Celebration', 'Harmony', 'Homecoming', 'Milestone', 'Joy'],
		keywordsMy: ['အောင်ပွဲခံခြင်း', 'သဟဇာတဖြစ်မှု', 'မိသားစုနွေးထွေးမှု', 'မှတ်တိုင်သစ်'],
		meaningUprightEn: 'Celebrating milestones, community harmony, peaceful domestic foundation.',
		meaningUprightMy:
			'အောင်မြင်မှုမှတ်တိုင်ကို အတူတကွ ပျော်ရွှင်စွာကျင်းပခြင်း၊ အိမ်တွင်းအေးချမ်းသာယာခြင်း။',
		meaningReversedEn: 'Family tension, cancelled celebration, transient instability.',
		meaningReversedMy: 'အိမ်တွင်းသဘောထားကွဲလွဲမှု၊ အစီအစဉ်ပျက်ပြယ်ခြင်း၊ စိတ်မသက်မသာဖြစ်ခြင်း။'
	},
	'Five of Wands': {
		nameEn: 'Five of Wands',
		nameMy: 'တုတ် ၅ ချောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Conflict', 'Competition', 'Disagreements', 'Rivalry'],
		keywordsMy: ['ပဋိပက္ခ', 'ပြိုင်ဆိုင်မှု', 'သဘောထားကွဲလွဲခြင်း', 'စိန်ခေါ်မှုများ'],
		meaningUprightEn: 'Healthy or chaotic competition, creative tension, conflicting perspectives.',
		meaningUprightMy:
			'ပြိုင်ဆိုင်မှုပြင်းထန်ခြင်း၊ အမြင်မတူဘဲ ငြင်းခုံရခြင်း၊ စိတ်ရှုပ်ထွေးဖွယ်စိန်ခေါ်မှုများ။',
		meaningReversedEn: 'Avoiding conflict, resolving friction, exhaustion from competition.',
		meaningReversedMy:
			'ပဋိပက္ခများကို အဆုံးသတ်နိုင်ခြင်း၊ အလျှော့ပေးညှိနှိုင်းခြင်း၊ ပြိုင်ဆိုင်မှုမှ နားယူခြင်း။'
	},
	'Six of Wands': {
		nameEn: 'Six of Wands',
		nameMy: 'တုတ် ၆ ချောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Success', 'Public recognition', 'Victory', 'Pride', 'Acclaim'],
		keywordsMy: ['အောင်ပွဲ', 'အသိအမှတ်ပြုခံရခြင်း', 'ဂုဏ်ယူဖွယ်အောင်မြင်မှု', 'ချီးကျူးခံရခြင်း'],
		meaningUprightEn:
			'Public triumph, celebrated accomplishment, rising confidence and validation.',
		meaningUprightMy:
			'လူအများ၏ အသိအမှတ်ပြုချီးကျူးမှုကို ရရှိခြင်း၊ ပြိုင်ဘက်ကင်း အောင်မြင်မှုရရှိခြင်း။',
		meaningReversedEn: 'Ego clash, fall from grace, lack of recognition.',
		meaningReversedMy: 'မာနထောင်လွှားမိခြင်း၊ ကြိုးစားသလောက် အသိအမှတ်မပြုခံရခြင်း။'
	},
	'Seven of Wands': {
		nameEn: 'Seven of Wands',
		nameMy: 'တုတ် ၇ ချောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Defensiveness', 'Perseverance', 'Holding ground', 'Courage'],
		keywordsMy: ['မိမိရပ်တည်ချက်ကို ကာကွယ်ခြင်း', 'ဇွဲရှိခြင်း', 'အခက်အခဲကို တွန်းလှန်ခြင်း'],
		meaningUprightEn:
			'Standing your ground against opposition, fierce persistence, moral conviction.',
		meaningUprightMy:
			'ဝိုင်းဝန်းတိုက်ခိုက်မှုများကို ကြံ့ကြံ့ခံရပ်တည်ခြင်း၊ မိမိယုံကြည်ချက်ကို သတ္တိရှိရှိကာကွယ်ခြင်း။',
		meaningReversedEn: 'Giving up, overwhelmed by critics, surrender.',
		meaningReversedMy: 'ဖိအားများလွန်း၍ လက်မြှောက်အရှုံးပေးချင်စိတ်ပေါက်ခြင်း၊ အားလျော့ခြင်း။'
	},
	'Eight of Wands': {
		nameEn: 'Eight of Wands',
		nameMy: 'တုတ် ၈ ချောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Swift action', 'Speed', 'Movement', 'Quick news', 'Momentum'],
		keywordsMy: [
			'လျင်မြန်သောလှုပ်ရှားမှု',
			'အရှိန်အဟုန်',
			'သတင်းစကားရောက်ရှိခြင်း',
			'တိုးတက်မှုမြန်ဆန်ခြင်း'
		],
		meaningUprightEn: 'Rapid developments, incoming messages, travel, accelerated momentum.',
		meaningUprightMy:
			'ကိစ္စရပ်များ အလွန်လျင်မြန်စွာ ဖြစ်ပျက်တိုးတက်လာခြင်း၊ သတင်းကောင်းများ အမြန်ရောက်လာခြင်း။',
		meaningReversedEn: 'Delays, missed messages, panicked rushing, frustrating slowness.',
		meaningReversedMy: 'ကြန့်ကြာနှောင့်နှေးမှုများကြုံရခြင်း၊ အလျင်စလိုလုပ်၍ မှားယွင်းခြင်း။'
	},
	'Nine of Wands': {
		nameEn: 'Nine of Wands',
		nameMy: 'တုတ် ၉ ချောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Resilience', 'Courage', 'Persistence', 'Final stretch', 'Vigilance'],
		keywordsMy: ['ခံနိုင်ရည်ရှိမှု', 'သတိရှိခြင်း', 'နောက်ဆုံးအဆင့်ဇွဲ', 'အလျော့မပေးခြင်း'],
		meaningUprightEn:
			'Battle-weary yet unbroken, guarding your accomplishments, enduring resilience.',
		meaningUprightMy:
			'ပင်ပန်းနွမ်းနယ်နေသော်လည်း အလျှော့မပေးဘဲ ဆက်လက်ကြံ့ကြံ့ခံနိုင်ခြင်း၊ အောင်မြင်ခါနီးအချိန်။',
		meaningReversedEn: 'Exhaustion, giving in right before the finish, paranoia.',
		meaningReversedMy:
			'အလွန်အမင်းပင်ပန်းနွမ်းနယ်ခြင်း၊ စိတ်ဒဏ်ရာကြောင့် အရာရာကို သံသယလွန်ကဲနေခြင်း။'
	},
	'Ten of Wands': {
		nameEn: 'Ten of Wands',
		nameMy: 'တုတ် ၁၀ ချောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Burden', 'Overwork', 'Responsibility', 'Stress', 'Hard labor'],
		keywordsMy: ['ဝန်ထုပ်ဝန်ပိုး', 'တာဝန်လွန်ကဲခြင်း', 'ပင်ပန်းဆင်းရဲမှု', 'စိတ်ဖိစီးမှု'],
		meaningUprightEn:
			'Carrying heavy responsibilities, near the summit of hard labor, burnout risk.',
		meaningUprightMy:
			'တာဝန်ဝတ္တရားများ အလွန်များပြားနေခြင်း၊ ဝန်ထုပ်ဝန်ပိုးကို တစ်ဦးတည်းထမ်းထားရခြင်း။',
		meaningReversedEn: 'Releasing burdens, delegating duties, inevitable collapse if not rested.',
		meaningReversedMy: 'တာဝန်များကို ခွဲဝေပေးအပ်ခြင်း၊ ဝန်ထုပ်ဝန်ပိုးမှ သက်သာရာရခြင်း။'
	},
	'Page of Wands': {
		nameEn: 'Page of Wands',
		nameMy: 'တုတ်ကိုင်လူငယ်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Enthusiasm', 'Exploration', 'New ideas', 'Free thinker'],
		keywordsMy: ['စိတ်အားထက်သန်သောလူငယ်', 'စူးစမ်းလိုစိတ်', 'စိတ်ကူးသစ်များ', 'သတင်းစကား'],
		meaningUprightEn: 'Youthful enthusiasm, exciting ideas, desire to explore new horizons.',
		meaningUprightMy:
			'စိတ်အားထက်သန်စွာ စတင်လေ့လာစူးစမ်းခြင်း၊ စိတ်လှုပ်ရှားဖွယ် သတင်းစကားရရှိခြင်း။',
		meaningReversedEn: 'Lack of follow-through, childish tantrum, procrastination.',
		meaningReversedMy: 'စိတ်ကူးသာရှိပြီး လက်တွေ့မပါခြင်း၊ စိတ်မတည်မငြိမ်ဖြစ်ခြင်း။'
	},
	'Knight of Wands': {
		nameEn: 'Knight of Wands',
		nameMy: 'တုတ်ကိုင်မြင်းစီးသူရဲကောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Energy', 'Passion', 'Adventure', 'Impulsiveness', 'Daring'],
		keywordsMy: ['ရဲရင့်စွန့်စားမှု', 'တက်ကြွလှုပ်ရှားမှု', 'စိတ်မြန်လက်မြန်', 'အရှိန်အဟုန်'],
		meaningUprightEn: 'Daring heroics, passionate pursuit of adventure, infectious energy.',
		meaningUprightMy:
			'ရဲရဲဝံ့ဝံ့ ရှေ့တိုးဆောင်ရွက်ခြင်း၊ စွန့်စားရဲသောစိတ်ဓာတ်၊ အရှိန်အဟုန်ပြင်းစွာ လုပ်ဆောင်ခြင်း။',
		meaningReversedEn: 'Reckless impulsivity, short-tempered frustration, scattered focus.',
		meaningReversedMy:
			'စိတ်လိုက်မာန်ပါလုပ်မိခြင်း၊ စိတ်မရှည်ဒေါသထွက်လွယ်ခြင်း၊ မဆင်မခြင်စွန့်စားခြင်း။'
	},
	'Queen of Wands': {
		nameEn: 'Queen of Wands',
		nameMy: 'တုတ်မိဖုရား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Confidence', 'Independence', 'Vibrancy', 'Charisma', 'Warmth'],
		keywordsMy: [
			'ကိုယ့်ကိုယ်ကိုယုံကြည်မှု',
			'လွတ်လပ်သောစိတ်',
			'ဆွဲဆောင်မှုရှိခြင်း',
			'နွေးထွေးတက်ကြွမှု'
		],
		meaningUprightEn: 'Magnetic confidence, vibrant creative leadership, cheerful independence.',
		meaningUprightMy:
			'ဆွဲဆောင်မှုရှိသော ခေါင်းဆောင်မှု၊ ကိုယ့်ကိုယ်ကို ယုံကြည်မှုအပြည့်ရှိခြင်း၊ တက်ကြွနွေးထွေးသော စိတ်ထား။',
		meaningReversedEn: 'Insecurity, jealousy, demanding nature, burnout.',
		meaningReversedMy: 'မနာလိုဝန်တိုစိတ်ဝင်ခြင်း၊ လွှမ်းမိုးချုပ်ချယ်လိုခြင်း၊ စိတ်ဓာတ်ကျဆင်းခြင်း။'
	},
	'King of Wands': {
		nameEn: 'King of Wands',
		nameMy: 'တုတ်ဘုရင်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Wands',
		suitMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်',
		keywordsEn: ['Visionary', 'Leadership', 'Honor', 'Inspiration', 'Bold execution'],
		keywordsMy: [
			'အမြော်အမြင်ကြီးသောခေါင်းဆောင်',
			'ရဲရင့်သောဆုံးဖြတ်ချက်',
			'စံပြပုဂ္ဂိုလ်',
			'ဩဇာရှိခြင်း'
		],
		meaningUprightEn: 'Bold visionary leadership, inspiring action, commanding authority.',
		meaningUprightMy:
			'အမြော်အမြင်ကြီးမားသော ခေါင်းဆောင်၊ ကြီးမားသောရည်မှန်းချက်များကို ဦးဆောင်အကောင်အထည်ဖော်သူ။',
		meaningReversedEn: 'Autocratic arrogance, unrealistic expectations, domineering temper.',
		meaningReversedMy:
			'အာဏာရှင်ဆန်လွန်းခြင်း၊ စိတ်ကြီးဝင်ခြင်း၊ အခြားသူများ၏ အကြံဉာဏ်ကို လျစ်လျူရှုခြင်း။'
	},

	// 14 CUPS (WATER) - ခွက်များ (ရေဓာတ်)
	'Ace of Cups': {
		nameEn: 'Ace of Cups',
		nameMy: 'ခွက် ၁ ခွက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Love', 'New feelings', 'Intuition', 'Compassion', 'Spiritual abundance'],
		keywordsMy: ['ချစ်ခြင်းမေတ္တာအသစ်', 'စိတ်ခံစားမှုနိုးထခြင်း', 'ကရုဏာ', 'စိတ်ချမ်းသာမှု'],
		meaningUprightEn: 'Overflowing love, emotional awakening, spiritual grace, new relationships.',
		meaningUprightMy:
			'မေတ္တာတရားအပြည့်အဝ စီးဆင်းလာခြင်း၊ စိတ်ခံစားမှုနွေးထွေးခြင်း၊ ဆက်ဆံရေးသစ်စတင်ခြင်း။',
		meaningReversedEn: 'Blocked feelings, emotional drain, repressed sorrow.',
		meaningReversedMy:
			'စိတ်ခံစားချက်ကို မျိုသိပ်ထားရခြင်း၊ စိတ်ဆင်းရဲစရာကြုံရခြင်း၊ စိတ်အားငယ်ခြင်း။'
	},
	'Two of Cups': {
		nameEn: 'Two of Cups',
		nameMy: 'ခွက် ၂ ခွက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Partnership', 'Mutual attraction', 'Connection', 'Harmony'],
		keywordsMy: [
			'လက်တွဲဖော်',
			'နှစ်ဦးသဘောတူချစ်ကြည်မှု',
			'ရင်းနှီးကျွမ်းဝင်မှု',
			'မျှတသောဆက်ဆံရေး'
		],
		meaningUprightEn: 'Deep mutual connection, harmonious partnership, heartfelt reconciliation.',
		meaningUprightMy:
			'စိတ်သဘောထားချင်း အလွန်ကိုက်ညီသော မိတ်ဖက် (သို့) ချစ်သူရရှိခြင်း၊ သဟဇာတဖြစ်သော ဆက်ဆံရေး။',
		meaningReversedEn: 'Imbalance in love, misunderstandings, broken harmony.',
		meaningReversedMy: 'နားလည်မှုလွဲမှားခြင်း၊ ဆက်ဆံရေးမညီမျှခြင်း၊ ကွဲလွဲမှုဖြစ်ပေါ်ခြင်း။'
	},
	'Three of Cups': {
		nameEn: 'Three of Cups',
		nameMy: 'ခွက် ၃ ခွက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Celebration', 'Friendship', 'Community', 'Gathering', 'Joy'],
		keywordsMy: [
			'မိတ်ဆွေများနှင့်ဆုံဆည်းခြင်း',
			'ပျော်ပွဲရွှင်ပွဲ',
			'ခင်မင်ရင်းနှီးမှု',
			'ပျော်ရွှင်ချမ်းမြေ့ခြင်း'
		],
		meaningUprightEn:
			'Joyful gatherings with cherished friends, mutual support, heartfelt celebrations.',
		meaningUprightMy:
			'မိတ်ဆွေသူငယ်ချင်းများနှင့် ပျော်ရွှင်စွာ ဆုံဆည်းရခြင်း၊ ပွဲလမ်းသဘင်များတွင် ပျော်ရွှင်ရခြင်း။',
		meaningReversedEn: 'Gossip, isolation from friends, overindulgence, exclusion.',
		meaningReversedMy:
			'သူငယ်ချင်းများအကြား သွေးခွဲစကားများရှိခြင်း၊ ပျော်ပါးလွန်းခြင်း၊ အထီးကျန်သလိုခံစားရခြင်း။'
	},
	'Four of Cups': {
		nameEn: 'Four of Cups',
		nameMy: 'ခွက် ၄ ခွက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Apathy', 'Contemplation', 'Discontent', 'Re-evaluation', 'Boredom'],
		keywordsMy: [
			'စိတ်မပါလက်မပါဖြစ်ခြင်း',
			'ငြီးငွေ့မှု',
			'ဆင်ခြင်တွေးတောခြင်း',
			'အခွင့်အရေးလွဲချော်ခြင်း'
		],
		meaningUprightEn:
			'Looking inward, emotional boredom, missing an offered opportunity right in front of you.',
		meaningUprightMy:
			'လက်ရှိအခြေအနေကို ငြီးငွေ့နေခြင်း၊ မျက်စိရှေ့ရှိ အခွင့်အလမ်းကောင်းကို သတိမထားမိဘဲ လျစ်လျူရှုမိခြင်း။',
		meaningReversedEn: 'Sudden awakening, seizing missed chances, renewed interest in life.',
		meaningReversedMy:
			'စိတ်ဓာတ်ပြန်လည်တက်ကြွလာခြင်း၊ အခွင့်အရေးသစ်များကို ပြန်လည်မြင်တွေ့နိုးထလာခြင်း။'
	},
	'Five of Cups': {
		nameEn: 'Five of Cups',
		nameMy: 'ခွက် ၅ ခွက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Loss', 'Grief', 'Regret', 'Disappointment', 'Lingering sorrow'],
		keywordsMy: ['ဆုံးရှုံးမှု', 'ဝမ်းနည်းပူဆွေးခြင်း', 'နောင်တ', 'စိတ်ပျက်လက်ပျက်ဖြစ်ခြင်း'],
		meaningUprightEn:
			'Grieving over spilled cups, dwelling on past mistakes while two cups still stand.',
		meaningUprightMy:
			'ဆုံးရှုံးသွားသောအရာများကိုသာ ကြည့်ပြီး နောင်တရဝမ်းနည်းနေခြင်း၊ ကျန်ရှိနေသေးသော ကောင်းကွက်များကို မမြင်နိုင်ခြင်း။',
		meaningReversedEn: 'Acceptance, healing from sorrow, moving forward, forgiveness.',
		meaningReversedMy:
			'အမှန်တရားကို လက်ခံပြီး ရှေ့ဆက်နိုင်ခြင်း၊ စိတ်ဒဏ်ရာမှ သက်သာပျောက်ကင်းလာခြင်း။'
	},
	'Six of Cups': {
		nameEn: 'Six of Cups',
		nameMy: 'ခွက် ၆ ခွက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Nostalgia', 'Childhood memories', 'Innocence', 'Reunion', 'Kindness'],
		keywordsMy: ['လွမ်းဆွတ်ဖွယ်အတိတ်', 'ကလေးဘဝအမှတ်တရ', 'အပြစ်ကင်းစင်မှု', 'ပြန်လည်ဆုံစည်းခြင်း'],
		meaningUprightEn:
			'Warm nostalgia, innocent generosity, meeting people from your past, sweet memories.',
		meaningUprightMy:
			'အတိတ်က အမှတ်တရကောင်းများ ပြန်လည်သတိရခြင်း၊ ငယ်သူငယ်ချင်းများနှင့် ပြန်ဆုံခြင်း၊ နွေးထွေးသောစေတနာ။',
		meaningReversedEn:
			'Living in the past, stuck in childhood wounds, clinging to outdated nostalgia.',
		meaningReversedMy: 'အတိတ်တွင်သာ ပိတ်မိနေပြီး ရှေ့မဆက်နိုင်ခြင်း၊ ကလေးဆန်သောစိတ်။'
	},
	'Seven of Cups': {
		nameEn: 'Seven of Cups',
		nameMy: 'ခွက် ၇ ခွက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Choices', 'Fantasy', 'Illusion', 'Daydreaming', 'Multiple options'],
		keywordsMy: [
			'ရွေးချယ်စရာများပြားခြင်း',
			'စိတ်ကူးယဉ်အိပ်မက်',
			'ထင်ယောင်ထင်မှား',
			'စိတ်ကူးမယဉ်ဘဲ လက်တွေ့ကျရန်လိုခြင်း'
		],
		meaningUprightEn:
			'Too many possibilities, tempting illusions, need to separate fantasy from reality.',
		meaningUprightMy:
			'ရွေးချယ်စရာတွေ များပြားပြီး စိတ်ကူးယဉ်ဆန်နေခြင်း၊ လက်တွေ့မကျသော ထင်ယောင်ထင်မှားများကို သတိထားရန်လိုအပ်ခြင်း။',
		meaningReversedEn: 'Clarity, realistic choices, cutting through illusions.',
		meaningReversedMy:
			'စိတ်ရှုပ်ထွေးမှုများ ကင်းစင်သွားပြီး လက်တွေ့ကျသော ရွေးချယ်မှုပြုလုပ်နိုင်ခြင်း။'
	},
	'Eight of Cups': {
		nameEn: 'Eight of Cups',
		nameMy: 'ခွက် ၈ ခွက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Walking away', 'Disillusionment', 'Higher quest', 'Leaving behind'],
		keywordsMy: [
			'ကျောခိုင်းထွက်ခွာခြင်း',
			'စိတ်ကုန်ခမ်းခြင်း',
			'မြင့်မြတ်သောအရာကိုရှာဖွေခြင်း',
			'စွန့်ခွာခြင်း'
		],
		meaningUprightEn: 'Walking away from unfulfilling situations to pursue deeper spiritual truth.',
		meaningUprightMy:
			'စိတ်ကျေနပ်မှု မပေးနိုင်တော့သောအရာများကို ကျောခိုင်းစွန့်ခွာခြင်း၊ ပိုမိုအဓိပ္ပာယ်ရှိသော ဘဝကို ရှာဖွေခြင်း။',
		meaningReversedEn: 'Fear of leaving, remaining in stagnant comfort, avoidance.',
		meaningReversedMy:
			'စွန့်ခွာထွက်ပြေးရန် မဝံ့မရဲဖြစ်ခြင်း၊ အဆင်မပြေသောအခြေအနေတွင် အောင့်အီးနေထိုင်ခြင်း။'
	},
	'Nine of Cups': {
		nameEn: 'Nine of Cups',
		nameMy: 'ခွက် ၉ ခွက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Wish fulfillment', 'Satisfaction', 'Contentment', 'Gratitude', 'Comfort'],
		keywordsMy: ['ဆန္ဒပြည့်ဝခြင်း', 'စိတ်ကျေနပ်မှု', 'လုံလောက်ပြည့်စုံခြင်း', 'ကံကောင်းခြင်း'],
		meaningUprightEn:
			'Wishes fulfilled, emotional contentment, abundant enjoyment of life pleasures.',
		meaningUprightMy:
			'ဆုတောင်းများ ပြည့်ဝခြင်း၊ စိတ်ချမ်းသာကိုယ်ကျန်းမာနှင့် စိတ်တိုင်းကျပျော်ရွှင်ရခြင်း၊ ကံကောင်းခြင်း။',
		meaningReversedEn: 'Smugness, overindulgence, superficial happiness, unfulfilled expectations.',
		meaningReversedMy:
			'အလိုမပြည့်နိုင်ခြင်း၊ စိတ်တိုင်းမကျဖြစ်ခြင်း၊ ရုပ်ဝတ္ထုအပေါ် သာယာလွန်ကဲခြင်း။'
	},
	'Ten of Cups': {
		nameEn: 'Ten of Cups',
		nameMy: 'ခွက် ၁၀ ခွက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Divine harmony', 'Family bliss', 'Happy home', 'Fulfillment', 'Peace'],
		keywordsMy: [
			'မိသားစုချမ်းမြေ့ခြင်း',
			'ပြီးပြည့်စုံသောချစ်ခြင်း',
			'အေးချမ်းသာယာမှု',
			'ဘဝရည်မှန်းချက်ပြည့်ဝခြင်း'
		],
		meaningUprightEn: 'Ultimate family harmony, true emotional abundance, lasting domestic joy.',
		meaningUprightMy:
			'မိသားစုတစ်ခုလုံး အေးချမ်းသာယာပျော်ရွှင်ခြင်း၊ နွေးထွေးသောမေတ္တာနှင့် ပြည့်စုံသောဘဝ။',
		meaningReversedEn: 'Domestic discord, broken family ties, shattered idyllic dream.',
		meaningReversedMy: 'အိမ်တွင်းရေး အဆင်မပြေခြင်း၊ သဘောထားကွဲလွဲမှုများပြားခြင်း။'
	},
	'Page of Cups': {
		nameEn: 'Page of Cups',
		nameMy: 'ခွက်ကိုင်လူငယ်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Creative messenger', 'Intuition', 'Sweet curiosity', 'Gentle heart'],
		keywordsMy: ['နူးညံ့သောစိတ်ထား', 'အတွင်းစိတ်အာရုံ', 'တီထွင်ဖန်တီးမှု', 'ချစ်ခြင်းမေတ္တာသတင်း'],
		meaningUprightEn: 'Sweet unexpected news, creative poetic inspiration, sensitive curiosity.',
		meaningUprightMy:
			'မေတ္တာနှင့်ဆိုင်သော သတင်းကောင်းကြားရခြင်း၊ နူးညံ့သိမ်မွေ့သော စိတ်ကူးသစ်များရရှိခြင်း။',
		meaningReversedEn: 'Emotional immaturity, broken promises, hurt feelings.',
		meaningReversedMy: 'ကလေးဆန်သော စိတ်ခံစားမှု၊ စိတ်မထိန်းနိုင်ခြင်း၊ ကတိမတည်ခြင်း။'
	},
	'Knight of Cups': {
		nameEn: 'Knight of Cups',
		nameMy: 'ခွက်ကိုင်မြင်းစီးသူရဲကောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Romance', 'Charm', 'Idealism', 'Poetic soul', 'Heart’s invitation'],
		keywordsMy: ['ရိုမန်းတစ်ဆန်မှု', 'ဆွဲဆောင်မှုရှိခြင်း', 'စိတ်ကူးယဉ်အချစ်', 'မေတ္တာလက်ကမ်းမှု'],
		meaningUprightEn:
			'Romantic overtures, following the heart’s ideals, graceful artistic pursuit.',
		meaningUprightMy:
			'အချစ်ရေးကမ်းလှမ်းမှုများရရှိခြင်း၊ နှလုံးသားဆန္ဒအတိုင်း လိုက်လျှောက်ခြင်း၊ စိတ်ကူးယဉ်အချစ်။',
		meaningReversedEn: 'Moodiness, deceptive charm, unrealistic fantasy, fickle affections.',
		meaningReversedMy: 'စိတ်ပြောင်းလွယ်ခြင်း၊ နှုတ်ချိုသော်လည်း လက်တွေ့မပါခြင်း၊ စိတ်မချရခြင်း။'
	},
	'Queen of Cups': {
		nameEn: 'Queen of Cups',
		nameMy: 'ခွက်မိဖုရား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Compassion', 'Deep empathy', 'Intuitive wisdom', 'Loving presence'],
		keywordsMy: ['စာနာနားလည်မှု', 'နက်ရှိုင်းသောမေတ္တာ', 'အတွင်းစိတ်ဉာဏ်', 'နွေးထွေးယုယမှု'],
		meaningUprightEn:
			'Deep emotional empathy, psychic sensitivity, caring sanctuary for troubled hearts.',
		meaningUprightMy:
			'စာနာနားလည်မှုအပြည့်ရှိသော မေတ္တာရှင်၊ စိတ်ခံစားချက်များကို ကောင်းစွာထိန်းသိမ်းနားလည်နိုင်သူ။',
		meaningReversedEn: 'Codependency, emotional overwhelm, brooding vulnerability.',
		meaningReversedMy:
			'စိတ်ခံစားမှုလွန်ကဲခြင်း၊ အလွန်အမင်းထိခိုက်လွယ်ခြင်း၊ စိတ်ဓာတ်မတည်ငြိမ်ခြင်း။'
	},
	'King of Cups': {
		nameEn: 'King of Cups',
		nameMy: 'ခွက်ဘုရင်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Cups',
		suitMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်',
		keywordsEn: ['Emotional balance', 'Diplomacy', 'Wise counsel', 'Calm dignity'],
		keywordsMy: [
			'စိတ်ခံစားမှုတည်ငြိမ်ခြင်း',
			'လိမ္မာပါးနပ်မှု',
			'ပညာရှိသောအကြံဉာဏ်',
			'မေတ္တာခေါင်းဆောင်'
		],
		meaningUprightEn: 'Mastery over feelings, emotional wisdom, compassionate and calm leadership.',
		meaningUprightMy:
			'မုန်တိုင်းထန်သော အခြေအနေတွင်ပင် စိတ်ကို အေးဆေးစွာထိန်းချုပ်နိုင်သော ပညာရှိခေါင်းဆောင်။',
		meaningReversedEn: 'Emotional manipulation, mood swings, cold aloofness, hidden malice.',
		meaningReversedMy:
			'စိတ်မတည်ငြိမ်ခြင်း၊ စိတ်ခံစားချက်ဖြင့် အခြားသူများကို လှည့်စားခြယ်လှယ်ခြင်း။'
	},

	// 14 SWORDS (AIR) - ဓားများ (လေဓာတ်)
	'Ace of Swords': {
		nameEn: 'Ace of Swords',
		nameMy: 'ဓား ၁ လက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Clarity', 'Breakthrough', 'Truth', 'Mental power', 'Sharp intellect'],
		keywordsMy: [
			'ရှင်းလင်းပြတ်သားမှု',
			'အမှန်တရား',
			'အသိဉာဏ်ထိုးထွင်းသိမြင်မှု',
			'အောင်မြင်ကျော်လွှားခြင်း'
		],
		meaningUprightEn:
			'Cutting through illusions with absolute truth, mental breakthrough, crystal clear vision.',
		meaningUprightMy:
			'အမှန်တရားကို ရှင်းရှင်းလင်းလင်း သိမြင်လာခြင်း၊ ဉာဏ်အလင်းပွင့်လန်းခြင်း၊ အောင်မြင်သောဆုံးဖြတ်ချက်။',
		meaningReversedEn: 'Confusion, harsh tongue, clouded judgment, hostility.',
		meaningReversedMy: 'တွေဝေဒွိဟဖြစ်ခြင်း၊ စကားကြမ်းတမ်းလွန်းခြင်း၊ မှားယွင်းသောဆုံးဖြတ်ချက်။'
	},
	'Two of Swords': {
		nameEn: 'Two of Swords',
		nameMy: 'ဓား ၂ လက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Stalemate', 'Difficult choices', 'Blindfolded doubt', 'Truce'],
		keywordsMy: [
			'ဆုံးဖြတ်ရခက်ခြင်း',
			'မျက်စိမှိတ်ငြင်းဆန်မှု',
			'နှစ်ခွဖြစ်နေခြင်း',
			'ယာယီငြိမ်သက်မှု'
		],
		meaningUprightEn:
			'A tough impasse, balancing opposing viewpoints, needing courage to face facts.',
		meaningUprightMy:
			'ဆုံးဖြတ်ချက်တစ်ခုကို ချရန် ခက်ခဲနေခြင်း၊ အမှန်တရားကို မျက်ကွယ်ပြုထားမိခြင်း။',
		meaningReversedEn: 'Information overload, forced painful choice, broken deadlock.',
		meaningReversedMy: 'မဖြစ်မနေ ရွေးချယ်ရမည့်အချိန်ရောက်လာခြင်း၊ အမှန်တရားကို ရင်ဆိုင်ရခြင်း။'
	},
	'Three of Swords': {
		nameEn: 'Three of Swords',
		nameMy: 'ဓား ၃ လက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Heartbreak', 'Emotional pain', 'Sorrow', 'Betrayal', 'Healing wound'],
		keywordsMy: ['နှလုံးကြေကွဲခြင်း', 'စိတ်ဒဏ်ရာ', 'သစ္စာဖောက်ခံရခြင်း', 'ဝမ်းနည်းမှု'],
		meaningUprightEn:
			'Piercing emotional pain, grief, painful truth that ultimately frees the spirit.',
		meaningUprightMy:
			'နှလုံးသားကြေကွဲဝမ်းနည်းရခြင်း၊ မေတ္တာရေးတွင် နာကျင်ရခြင်း၊ ခံစားချက်ဒဏ်ရာရခြင်း။',
		meaningReversedEn: 'Recovery from grief, releasing pain, forgiveness, healing.',
		meaningReversedMy:
			'စိတ်ဒဏ်ရာမှ သက်သာပျောက်ကင်းလာခြင်း၊ ခွင့်လွှတ်ခြင်း၊ နာကျင်မှုကို ကျော်လွှားနိုင်ခြင်း။'
	},
	'Four of Swords': {
		nameEn: 'Four of Swords',
		nameMy: 'ဓား ၄ လက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Rest', 'Recovery', 'Sanctuary', 'Meditation', 'Quiet pause'],
		keywordsMy: [
			'အနားယူခြင်း',
			'စိတ်အေးငြိမ်းရာရှာခြင်း',
			'တရားမှတ်ဆင်ခြင်ခြင်း',
			'ပြန်လည်အားဖြည့်ခြင်း'
		],
		meaningUprightEn:
			'Recuperation after mental battles, peaceful retreat, meditation to recharge.',
		meaningUprightMy:
			'စိတ်ရောကိုယ်ပါ အနားယူသင့်သောအချိန်၊ တိတ်ဆိတ်ငြိမ်သက်စွာ စွမ်းအင်ပြန်လည်ဖြည့်တင်းခြင်း။',
		meaningReversedEn: 'Burnout from refusing rest, forced isolation, restless awakening.',
		meaningReversedMy:
			'မနားမနေ အလုပ်လုပ်လွန်း၍ ပင်ပန်းနွမ်းနယ်ခြင်း၊ ပြန်လည်လှုပ်ရှားရန် အဆင်သင့်ဖြစ်ခြင်း။'
	},
	'Five of Swords': {
		nameEn: 'Five of Swords',
		nameMy: 'ဓား ၅ လက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Hollow victory', 'Conflict', 'Ego defeat', 'Bitter dispute'],
		keywordsMy: [
			'တန်ဖိုးမဲ့သောအနိုင်ရမှု',
			'အငြင်းပွားမှု',
			'မာနတိုက်ပွဲ',
			'ဆုံးရှုံးမှုကြီးသောအောင်ပွဲ'
		],
		meaningUprightEn:
			'Winning at too high a cost, selfish victory, bitter conflict leaving all wounded.',
		meaningUprightMy:
			'အနိုင်ရသော်လည်း မိတ်ဆွေများဆုံးရှုံးရခြင်း၊ မာနကြောင့် အားလုံးနာကျင်ရသော ရလဒ်။',
		meaningReversedEn: 'Reconciliation, walking away from toxic arguments, remorse.',
		meaningReversedMy: 'အငြင်းပွားမှုများကို ရပ်တန့်ခြင်း၊ ပြန်လည်သင့်မြတ်ခြင်း၊ နောင်တရခြင်း။'
	},
	'Six of Swords': {
		nameEn: 'Six of Swords',
		nameMy: 'ဓား ၆ လက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Transition', 'Calmer waters', 'Moving forward', 'Leaving turbulence'],
		keywordsMy: [
			'ကူးပြောင်းခြင်း',
			'လှိုင်းလေငြိမ်သက်ရာဆီသို့',
			'ခရီးထွက်ခွာခြင်း',
			'စိတ်သက်သာရာရခြင်း'
		],
		meaningUprightEn: 'Sailing away from rough seas toward peaceful shores, gradual healing.',
		meaningUprightMy:
			'မုန်တိုင်းထန်သော အခက်အခဲများမှ လွတ်မြောက်ပြီး အေးချမ်းသော အခြေအနေသစ်သို့ ကူးပြောင်းခြင်း။',
		meaningReversedEn: 'Stuck in turbulence, carrying baggage, trapped by past sorrow.',
		meaningReversedMy:
			'အတိတ်ဒဏ်ရာများကို သယ်ဆောင်နေဆဲဖြစ်ခြင်း၊ အခက်အခဲမှ မလွတ်မြောက်နိုင်သေးခြင်း။'
	},
	'Seven of Swords': {
		nameEn: 'Seven of Swords',
		nameMy: 'ဓား ၇ လက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Stealth', 'Strategy', 'Secret actions', 'Deception', 'Clever escape'],
		keywordsMy: ['လျှို့ဝှက်လှုပ်ရှားမှု', 'ဉာဏ်နီဉာဏ်နက်', 'သတိထားရမည့်လိမ်လည်မှု', 'ဗျူဟာ'],
		meaningUprightEn:
			'Strategic circumvention, careful secret steps, beware of deceit or cutting corners.',
		meaningUprightMy:
			'ဉာဏ်နီဉာဏ်နက်သုံး၍ ရှောင်တိမ်းခြင်း၊ လျှို့ဝှက်ကြံစည်မှုများ၊ သစ္စာမရှိသူများကို သတိထားရခြင်း။',
		meaningReversedEn: 'Confession, truth exposed, conscience clearing, foiled plans.',
		meaningReversedMy:
			'လျှို့ဝှက်ချက်များ ပေါ်ပေါက်သွားခြင်း၊ ဝန်ခံခြင်း၊ အမှန်အတိုင်း ပြန်လည်ရင်ဆိုင်ခြင်း။'
	},
	'Eight of Swords': {
		nameEn: 'Eight of Swords',
		nameMy: 'ဓား ၈ လက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Trapped feeling', 'Self-imposed restriction', 'Victim mindset', 'Helplessness'],
		keywordsMy: [
			'ပိတ်မိနေသလိုခံစားရခြင်း',
			'မိမိကိုယ်ကိုကန့်သတ်ထားခြင်း',
			'ကြောက်ရွံ့မှု',
			'အမြင်ကျဉ်းမြောင်းခြင်း'
		],
		meaningUprightEn:
			'Feeling trapped by self-limiting beliefs, illusions of helplessness; the ropes are loose.',
		meaningUprightMy:
			'မိမိအတွေးဖြင့် မိမိကိုယ်ကို ထောင်ချောက်ဆင်ပိတ်မိနေခြင်း၊ သတ္တိရှိရှိ မျက်စိဖွင့်ကြည့်ပါက လွတ်မြောက်နိုင်ခြင်း။',
		meaningReversedEn: 'Breaking free, seeing reality, mental release, taking empowerment.',
		meaningReversedMy:
			'ကြောက်ရွံ့မှုများမှ လွတ်မြောက်ခြင်း၊ အသိဉာဏ်ပွင့်လင်းပြီး လွတ်လပ်မှုရရှိခြင်း။'
	},
	'Nine of Swords': {
		nameEn: 'Nine of Swords',
		nameMy: 'ဓား ၉ လက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Anxiety', 'Insomnia', 'Nightmares', 'Deep worry', 'Guilt'],
		keywordsMy: ['သောကဗျာပါဒ', 'အိပ်မပျော်ခြင်း', 'စိတ်ပူပန်လွန်ကဲခြင်း', 'အကြောက်တရား'],
		meaningUprightEn:
			'Awake in the dark with looping anxiety, exaggerated mental anguish, need for soothing.',
		meaningUprightMy:
			'ညဘက်အိပ်မပျော်အောင် စိုးရိမ်ပူပန်မှုများခြင်း၊ စိတ်ဖိစီးမှုလွန်ကဲခြင်း၊ အခြေအနေထက် စိတ်က ပိုဆိုးနေခြင်း။',
		meaningReversedEn: 'Light at dawn, relief from anxiety, finding solace, speaking up.',
		meaningReversedMy: 'စိတ်သက်သာရာရလာခြင်း၊ စိုးရိမ်မှုများ လျော့ပါးသွားခြင်း၊ အကူအညီရရှိခြင်း။'
	},
	'Ten of Swords': {
		nameEn: 'Ten of Swords',
		nameMy: 'ဓား ၁၀ လက်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Rock bottom', 'Painful ending', 'Betrayal', 'New dawn ahead'],
		keywordsMy: ['အဆိုးဆုံးအခြေအနေရောက်ခြင်း', 'နာကျင်စရာအဆုံးသတ်', 'အရုဏ်ဦးသစ်စတင်ခြင်း'],
		meaningUprightEn:
			'The absolute bottom; the worst is officially over and dawn begins on the horizon.',
		meaningUprightMy:
			'အဆိုးဝါးဆုံး အခြေအနေသို့ ရောက်ရှိပြီးဆုံးသွားခြင်း၊ နာကျင်မှုများ ပြီးဆုံးပြီဖြစ်၍ အသစ်ပြန်စတင်ရတော့မည်။',
		meaningReversedEn: 'Recovery, rising from defeat, surviving the worst, rebuilding.',
		meaningReversedMy: 'ကျရှုံးမှုမှ ပြန်လည်ထူထောင်လာခြင်း၊ အသက်ရှူပေါက်ပြန်ရခြင်း။'
	},
	'Page of Swords': {
		nameEn: 'Page of Swords',
		nameMy: 'ဓားကိုင်လူငယ်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Curiosity', 'Mental agility', 'Truth seeker', 'Observant'],
		keywordsMy: [
			'စူးစမ်းလိုစိတ်ပြင်းပြခြင်း',
			'ဉာဏ်ထက်မြက်ခြင်း',
			'အမှန်တရားရှာဖွေသူ',
			'သတိရှိခြင်း'
		],
		meaningUprightEn:
			'Sharp curiosity, vibrant intellectual thirst, candid and vigilant communication.',
		meaningUprightMy:
			'ဉာဏ်ရည်ထက်မြက်ပြီး အရာရာကို စူးစမ်းလေ့လာလိုစိတ်ရှိခြင်း၊ သတင်းအချက်အလက် စုဆောင်းခြင်း။',
		meaningReversedEn: 'Gossip, defensive chatter, spying, cynical skepticism.',
		meaningReversedMy: 'စကားအတင်းပြောလွန်းခြင်း၊ အဆိုးမြင်ဝါဒ၊ စိတ်ဆတ်ခြင်း။'
	},
	'Knight of Swords': {
		nameEn: 'Knight of Swords',
		nameMy: 'ဓားကိုင်မြင်းစီးသူရဲကောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Directness', 'Fierce intellect', 'Action-oriented', 'Ambitious drive'],
		keywordsMy: [
			'ပြတ်သားတိုက်ခိုက်ခြင်း',
			'ရည်မှန်းချက်ကြီးခြင်း',
			'ထိုးထွင်းဉာဏ်',
			'အရှိန်ပြင်းသောလုပ်ဆောင်မှု'
		],
		meaningUprightEn:
			'Charging forward with razor-sharp ambition, fearless directness, decisive action.',
		meaningUprightMy:
			'ရည်မှန်းချက်ဆီသို့ မဆုတ်မနစ် အရှိန်အဟုန်ဖြင့် ရှေ့တိုးဆောင်ရွက်ခြင်း၊ ပြတ်သားသော စိတ်ဓာတ်။',
		meaningReversedEn: 'Tactless cruelty, blindly impulsive, aggressive burnout.',
		meaningReversedMy: 'စကားကြမ်းတမ်းရိုင်းပြခြင်း၊ အလျင်စလိုဆုံးဖြတ်မိ၍ ထိခိုက်နစ်နာခြင်း။'
	},
	'Queen of Swords': {
		nameEn: 'Queen of Swords',
		nameMy: 'ဓားမိဖုရား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Perceptive clarity', 'Honesty', 'Independence', 'Clear boundaries'],
		keywordsMy: [
			'ထက်မြက်သောဆုံးဖြတ်ချက်',
			'ရိုးသားဖြောင့်မတ်မှု',
			'လွတ်လပ်သောဉာဏ်',
			'စည်းကမ်းပြတ်သားမှု'
		],
		meaningUprightEn:
			'Unfiltered clarity, wisdom earned through hardships, healthy firm boundaries.',
		meaningUprightMy:
			'အမှန်တရားကို မျက်နှာမလိုက်ဘဲ ကြည့်မြင်နိုင်သော ဉာဏ်ပညာ၊ လွတ်လပ်ပြီး ပြတ်သားသော ခေါင်းဆောင်မှု။',
		meaningReversedEn: 'Cold cynicism, bitter tongue, unyielding rigidity.',
		meaningReversedMy: 'အေးစက်ခက်ထန်လွန်းခြင်း၊ ခွင့်မလွှတ်နိုင်သော အငြိုးအတေးထားခြင်း။'
	},
	'King of Swords': {
		nameEn: 'King of Swords',
		nameMy: 'ဓားဘုရင်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Swords',
		suitMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်',
		keywordsEn: ['Intellectual mastery', 'Ethical truth', 'Impartial justice', 'Strategic genius'],
		keywordsMy: [
			'ဉာဏ်ပညာကြီးမားသောခေါင်းဆောင်',
			'တရားမျှတသောဆုံးဖြတ်ချက်',
			'ဗျူဟာကျကျစီမံမှု',
			'ဩဇာအာဏာ'
		],
		meaningUprightEn:
			'Commanding intellectual authority, fair judgment, analytical mastery, strategic leader.',
		meaningUprightMy:
			'အထွတ်အထိပ် ဉာဏ်ပညာနှင့် ဗျူဟာကျသော ခေါင်းဆောင်မှု၊ တရားမျှတစွာ ဆုံးဖြတ်စီရင်နိုင်သူ။',
		meaningReversedEn: 'Tyrannical dogmatism, cold cruelty, manipulating rules.',
		meaningReversedMy: 'ဉာဏ်ဆင်၍ အနိုင်ကျင့်ခြင်း၊ စာနာမှုကင်းမဲ့စွာ အမိန့်ပေးခြင်း။'
	},

	// 14 PENTACLES (EARTH) - ဒင်္ဂါးများ (မြေဓာတ်)
	'Ace of Pentacles': {
		nameEn: 'Ace of Pentacles',
		nameMy: 'ဒင်္ဂါး ၁ ပြား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Material opportunity', 'Prosperity', 'New venture', 'Solid foundation'],
		keywordsMy: ['ငွေကြေးအခွင့်အလမ်းသစ်', 'ကြွယ်ဝချမ်းသာခြင်း', 'ခိုင်မာသောအခြေခံ', 'စီးပွားရေးအစ'],
		meaningUprightEn:
			'Tangible seed of wealth, a real-world investment or practical opportunity manifesting.',
		meaningUprightMy:
			'ငွေကြေးဥစ္စာနှင့် စီးပွားရေးအခွင့်အလမ်းသစ် ပေါ်ပေါက်လာခြင်း၊ ခိုင်မာသော ဘဝအုတ်မြစ်။',
		meaningReversedEn: 'Missed investment, poor planning, financial stinginess or waste.',
		meaningReversedMy: 'ငွေကြေးအခွင့်အလမ်း လွဲချော်ခြင်း၊ အသုံးစရိတ်မထိန်းနိုင်ခြင်း။'
	},
	'Two of Pentacles': {
		nameEn: 'Two of Pentacles',
		nameMy: 'ဒင်္ဂါး ၂ ပြား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Balance', 'Adaptability', 'Juggling priorities', 'Resourcefulness'],
		keywordsMy: [
			'မျှတအောင်ထိန်းညှိခြင်း',
			'လိုက်လျောညီထွေရှိမှု',
			'တာဝန်မျိုးစုံကို စီမံနိုင်ခြင်း'
		],
		meaningUprightEn:
			'Skillful multitasking, adapting to financial ebb and flow, maintaining equilibrium.',
		meaningUprightMy:
			'ဝင်ငွေထွက်ငွေနှင့် တာဝန်များကို မျှတအောင် ချိန်ဆထိန်းသိမ်းနိုင်ခြင်း၊ ပြောင်းလဲမှုကို လိုက်လျောညီထွေဖြစ်အောင် နေနိုင်ခြင်း။',
		meaningReversedEn: 'Overwhelmed by chores, financial disarray, dropping balls.',
		meaningReversedMy: 'တာဝန်များပြားလွန်း၍ စိတ်ဖိစီးခြင်း၊ ငွေကြေးစီမံခန့်ခွဲမှု လွဲချော်ခြင်း။'
	},
	'Three of Pentacles': {
		nameEn: 'Three of Pentacles',
		nameMy: 'ဒင်္ဂါး ၃ ပြား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Teamwork', 'Craftsmanship', 'Collaboration', 'Mastery', 'Recognition'],
		keywordsMy: [
			'ပူးပေါင်းဆောင်ရွက်မှု',
			'လက်ရာမြောက်ကျွမ်းကျင်မှု',
			'အဖွဲ့လိုက်လုပ်ဆောင်ခြင်း',
			'အသိအမှတ်ပြုခံရမှု'
		],
		meaningUprightEn:
			'Successful collaboration, expert craftsmanship recognized, laying great work together.',
		meaningUprightMy:
			'အဖွဲ့အစည်းနှင့် လက်တွဲညီညီ အောင်မြင်စွာလုပ်ဆောင်နိုင်ခြင်း၊ ကျွမ်းကျင်မှုအတွက် ချီးကျူးခံရခြင်း။',
		meaningReversedEn: 'Friction in team, shoddy work, lack of cohesive vision.',
		meaningReversedMy: 'အဖွဲ့တွင်း စည်းလုံးမှုမရှိခြင်း၊ လုပ်ငန်းအရည်အသွေး ညံ့ဖျင်းခြင်း။'
	},
	'Four of Pentacles': {
		nameEn: 'Four of Pentacles',
		nameMy: 'ဒင်္ဂါး ၄ ပြား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Frugality', 'Security', 'Hoarding', 'Holding tightly', 'Stability'],
		keywordsMy: [
			'ချွေတာစုဆောင်းခြင်း',
			'လုံခြုံစိတ်ချမှု',
			'တွန့်တိုလွန်းခြင်း',
			'ပိုင်ဆိုင်မှုကို တင်းတင်းဆုပ်ကိုင်ထားခြင်း'
		],
		meaningUprightEn:
			'Financial stability and security, but guard against hoarding or fear of poverty.',
		meaningUprightMy:
			'ငွေကြေးလုံခြုံမှုရှိသော်လည်း တွန့်တိုလွန်းပြီး စွန့်လွှတ်ရမည်ကို ကြောက်ရွံ့နေခြင်း။',
		meaningReversedEn: 'Reckless spending, opening up generosity, letting go of fear.',
		meaningReversedMy:
			'ငွေကြေးဖြုန်းတီးမိခြင်း (သို့) ပေးကမ်းစွန့်ကြဲရန် စိတ်ထားဖွင့်ပေးနိုင်လာခြင်း။'
	},
	'Five of Pentacles': {
		nameEn: 'Five of Pentacles',
		nameMy: 'ဒင်္ဂါး ၅ ပြား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Hardship', 'Financial worry', 'Isolation', 'Out in the cold', 'Scarcity'],
		keywordsMy: [
			'အခက်အခဲကြုံရခြင်း',
			'ငွေကြေးကျပ်တည်းမှု',
			'အထီးကျန်ဆန်ခြင်း',
			'အကူအညီလိုအပ်ခြင်း'
		],
		meaningUprightEn:
			'Temporary material hardship, feeling left out in the snow, shelter is nearby if you look.',
		meaningUprightMy:
			'ငွေကြေးနှင့် ဘဝအခက်အခဲများ ကြုံတွေ့ရချိန်၊ အကူအညီရယူရန် သတိမထားမိဘဲ အထီးကျန်နေခြင်း။',
		meaningReversedEn: 'Recovery from financial loss, finding warm shelter, returning prosperity.',
		meaningReversedMy:
			'အခက်အခဲကာလမှ လွတ်မြောက်လာခြင်း၊ အကူအညီနှင့် မျှော်လင့်ချက် ပြန်လည်ရရှိခြင်း။'
	},
	'Six of Pentacles': {
		nameEn: 'Six of Pentacles',
		nameMy: 'ဒင်္ဂါး ၆ ပြား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Generosity', 'Charity', 'Fair sharing', 'Receiving support', 'Balance'],
		keywordsMy: ['ရက်ရောမှု', 'လှူဒါန်းပေးကမ်းခြင်း', 'မျှတစွာဝေမျှမှု', 'အကူအညီရရှိခြင်း'],
		meaningUprightEn:
			'Generosity of resources, fair reciprocity, giving and receiving in noble equilibrium.',
		meaningUprightMy:
			'ရက်ရက်ရောရော ကူညီပေးကမ်းနိုင်ခြင်း (သို့) မိမိလိုအပ်သော အကူအညီကို ကောင်းမွန်စွာ ရရှိခြင်း။',
		meaningReversedEn: 'Strings attached to gifts, abuse of charity, financial exploitation.',
		meaningReversedMy: 'ကောက်ကျစ်သော ရည်ရွယ်ချက်ဖြင့် ကူညီခြင်း၊ မမျှတသော ဝေမျှမှု။'
	},
	'Seven of Pentacles': {
		nameEn: 'Seven of Pentacles',
		nameMy: 'ဒင်္ဂါး ၇ ပြား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Patience', 'Long-term investment', 'Harvest pause', 'Evaluating crops'],
		keywordsMy: [
			'စိတ်ရှည်သည်းခံခြင်း',
			'ရေရှည်ရင်းနှီးမြှုပ်နှံမှု',
			'အသီးအပွင့်ကို စောင့်ဆိုင်းခြင်း',
			'သုံးသပ်ခြင်း'
		],
		meaningUprightEn:
			'Patiently tending to long-term growth, taking stock of hard work, waiting for harvest.',
		meaningUprightMy:
			'စိုက်ထုတ်ထားသော ကြိုးစားအားထုတ်မှုများ အသီးအပွင့်ဝေဆာရန် စိတ်ရှည်စွာ စောင့်ဆိုင်းရမည့်အချိန်။',
		meaningReversedEn: 'Impatience, lack of reward, abandoned labor, poor results.',
		meaningReversedMy: 'စိတ်မရှည်ဘဲ စောစီးစွာ လက်လျှော့မိခြင်း၊ ရလဒ်မကောင်းခြင်း။'
	},
	'Eight of Pentacles': {
		nameEn: 'Eight of Pentacles',
		nameMy: 'ဒင်္ဂါး ၈ ပြား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Apprenticeship', 'Dedication', 'Craftsmanship', 'Skill development', 'Focus'],
		keywordsMy: [
			'ကြိုးစားအားထုတ်မှု',
			'ပညာဆည်းပူးခြင်း',
			'ကျွမ်းကျင်မှုလေ့ကျင့်ခြင်း',
			'အာရုံစူးစိုက်မှု'
		],
		meaningUprightEn:
			'Mastering a craft through diligent practice, proud work ethic, honing skills meticulously.',
		meaningUprightMy:
			'မိမိလုပ်ငန်းနှင့် ကျွမ်းကျင်မှုတွင် အာရုံစူးစိုက်၍ ကြိုးစားလေ့ကျင့်နေခြင်း၊ အောင်မြင်မည့် အလေ့အကျင့်ကောင်း။',
		meaningReversedEn: 'Careless work, repetitive monotony, perfectionism paralysis.',
		meaningReversedMy: 'ပေါ့ဆစွာလုပ်ကိုင်မိခြင်း၊ ပင်ပန်းငြီးငွေ့ဖွယ် အလုပ်များတွင် ပိတ်မိခြင်း။'
	},
	'Nine of Pentacles': {
		nameEn: 'Nine of Pentacles',
		nameMy: 'ဒင်္ဂါး ၉ ပြား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Self-reliance', 'Luxury', 'Refinement', 'Abundance', 'Solitary reward'],
		keywordsMy: [
			'ကိုယ့်အားကိုယ်ကိုးနိုင်ခြင်း',
			'ဇိမ်ခံချမ်းသာမှု',
			'ဂုဏ်သရေရှိခြင်း',
			'ကြွယ်ဝအေးချမ်းမှု'
		],
		meaningUprightEn:
			'Financial independence earned through hard work, savoring luxurious peace, self-worth.',
		meaningUprightMy:
			'မိမိကိုယ်ပိုင်ကြိုးစားမှုဖြင့် ဘဝကို ပြည့်စုံလွတ်လပ်စွာ တည်ဆောက်နိုင်ခြင်း၊ ဂုဏ်သိက္ခာရှိသော ဇိမ်ခံဘဝ။',
		meaningReversedEn: 'Overspending, material obsession, loneliness in wealth.',
		meaningReversedMy: 'ငွေကြေးဖြုန်းတီးလွန်းခြင်း၊ ပစ္စည်းဥစ္စာကြွယ်ဝသော်လည်း စိတ်မချမ်းသာခြင်း။'
	},
	'Ten of Pentacles': {
		nameEn: 'Ten of Pentacles',
		nameMy: 'ဒင်္ဂါး ၁၀ ပြား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Wealth', 'Legacy', 'Generational stability', 'Tradition', 'Family empire'],
		keywordsMy: [
			'မျိုးရိုးစဉ်ဆက်ကြွယ်ဝမှု',
			'အမွေအနှစ်',
			'ရေရှည်ခိုင်မာသောချမ်းသာမှု',
			'မိသားစုအောင်မြင်မှု'
		],
		meaningUprightEn:
			'Generational wealth, enduring family security, leaving a proud foundation for descendants.',
		meaningUprightMy:
			'မျိုးဆက်အလိုက် ခိုင်မာသော စည်းစိမ်ချမ်းသာနှင့် အမွေအနှစ်၊ အေးချမ်းတည်ငြိမ်သော မိသားစုဘဝ။',
		meaningReversedEn: 'Inheritance disputes, financial collapse, tradition broken in anger.',
		meaningReversedMy: 'အမွေကိစ္စ အငြင်းပွားရခြင်း၊ ငွေကြေးဆုံးရှုံးမှုကြုံရခြင်း။'
	},
	'Page of Pentacles': {
		nameEn: 'Page of Pentacles',
		nameMy: 'ဒင်္ဂါးကိုင်လူငယ်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Ambitious student', 'Practical idea', 'Grounding', 'Loyal learner'],
		keywordsMy: [
			'ကြိုးစားသောကျောင်းသား',
			'လက်တွေ့ကျသောအကြံဉာဏ်',
			'စီးပွားရေးအစ',
			'စိတ်ချရသောလေ့လာသူ'
		],
		meaningUprightEn:
			'Studious thirst for real-world mastery, promising financial idea, eager beginner.',
		meaningUprightMy:
			'လက်တွေ့ကျသော ပညာနှင့် စီးပွားရေးအခွင့်အလမ်းကို သဲကြီးမဲကြီး လေ့လာဆည်းပူးနေခြင်း။',
		meaningReversedEn: 'Lack of follow-through, procrastination, short-sighted laziness.',
		meaningReversedMy: 'အပျင်းထူခြင်း၊ အစီအစဉ်မရှိဘဲ အချိန်ဖြုန်းနေမိခြင်း။'
	},
	'Knight of Pentacles': {
		nameEn: 'Knight of Pentacles',
		nameMy: 'ဒင်္ဂါးကိုင်မြင်းစီးသူရဲကောင်း',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Reliability', 'Work ethic', 'Patience', 'Routine', 'Methodical progress'],
		keywordsMy: ['စိတ်ချရမှု', 'တာဝန်ကျေပွန်ခြင်း', 'စနစ်တကျရှေ့တိုးခြင်း', 'ခိုင်မာသောဇွဲ'],
		meaningUprightEn:
			'Unshakable work ethic, steady methodical duty, dependable honor and execution.',
		meaningUprightMy:
			'အလွန်စိတ်ချရသော လုပ်ဆောင်မှု၊ ဖြည်းဖြည်းနှင့်မှန်မှန် ခိုင်မာစွာ အောင်မြင်မှုဆီသို့ လျှောက်လှမ်းခြင်း။',
		meaningReversedEn: 'Stubborn rut, boring perfectionism, uninspired drudgery.',
		meaningReversedMy:
			'ခေါင်းမာလွန်းခြင်း၊ အပြောင်းအလဲကို မလုပ်ချင်ဘဲ ငြီးငွေ့ဖွယ် အလုပ်များတွင် ပိတ်မိခြင်း။'
	},
	'Queen of Pentacles': {
		nameEn: 'Queen of Pentacles',
		nameMy: 'ဒင်္ဂါးမိဖုရား',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Nurturing abundance', 'Practical care', 'Resourcefulness', 'Down-to-earth'],
		keywordsMy: [
			'နွေးထွေးသောကြွယ်ဝမှု',
			'လက်တွေ့ကျကျစောင့်ရှောက်ခြင်း',
			'အရင်းအမြစ်ပိုင်နိုင်မှု',
			'ချမ်းသာငြိမ်းချမ်းမှု'
		],
		meaningUprightEn:
			'Generous matriarch, thriving home and garden, sensible financial caregiving.',
		meaningUprightMy:
			'မိသားစုနှင့် အနီးနားရှိသူများကို နွေးထွေးစွာ ဂရုစိုက်စောင့်ရှောက်နိုင်သော လက်တွေ့ကျသော ချမ်းသာရှင်။',
		meaningReversedEn: 'Work-life imbalance, smothered by possessions, anxiety over wealth.',
		meaningReversedMy:
			'ငွေကြေးနှင့် ပိုင်ဆိုင်မှုများအတွက် စိုးရိမ်လွန်ကဲခြင်း၊ အလုပ်နှင့် ဘဝ မမျှတခြင်း။'
	},
	'King of Pentacles': {
		nameEn: 'King of Pentacles',
		nameMy: 'ဒင်္ဂါးဘုရင်',
		arcanaEn: 'Minor Arcana',
		arcanaMy: 'မိုင်နာအာခါနာ',
		suitEn: 'Pentacles',
		suitMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်',
		keywordsEn: ['Financial mastery', 'Abundance', 'Empire builder', 'Generosity', 'Security'],
		keywordsMy: [
			'ငွေကြေးနှင့်စီးပွားရေးအရှင်သခင်',
			'ကြွယ်ဝချမ်းသာမှုအထွတ်အထိပ်',
			'ခိုင်မာသောဩဇာ',
			'အောင်မြင်သူ'
		],
		meaningUprightEn:
			'Pinnacle of business mastery, enterprise builder, providing security to all under his care.',
		meaningUprightMy:
			'စီးပွားရေးနှင့် ငွေကြေးဆိုင်ရာ အထွတ်အထိပ် အောင်မြင်သူ၊ အားလုံးကို လုံခြုံစွာ စောင့်ရှောက်နိုင်သော ခေါင်းဆောင်။',
		meaningReversedEn: 'Greed, financial corruption, stubborn materialism, bankruptcy.',
		meaningReversedMy:
			'လောဘကြီးလွန်းခြင်း၊ ပစ္စည်းဥစ္စာနောက်သာ လိုက်လွန်း၍ လူသားဆန်မှု ကင်းမဲ့ခြင်း။'
	}
};

// SPREAD POSITIONS TRANSLATIONS
export const SPREAD_POSITIONS_DATA: Record<string, { en: string; my: string }> = {
	past: { en: 'Past', my: 'အတိတ်' },
	present: { en: 'Present', my: 'ပစ္စုပ္ပန် (လက်ရှိ)' },
	future: { en: 'Future', my: 'အနာဂတ်' },
	situation: { en: 'Situation', my: 'လက်ရှိအခြေအနေ' },
	current_position: { en: 'Current Position', my: 'လက်ရှိရပ်တည်ချက်' },
	obstacle: { en: 'Obstacle / Challenge', my: 'အခက်အခဲ / စိန်ခေါ်မှု' },
	challenge: { en: 'Challenge', my: 'စိန်ခေါ်မှု' },
	advice: { en: 'Advice', my: 'အကြံပြုချက်' },
	guidance: { en: 'Guidance', my: 'လမ်းညွှန်ချက်' },
	outcome: { en: 'Outcome', my: 'နောက်ဆုံးရလဒ်' },
	you: { en: 'You', my: 'သင်၏ရပ်တည်ချက်' },
	other_person: { en: 'Other Person', my: 'တစ်ဖက်လူ / လက်တွဲဖော်' },
	connection: { en: 'Connection', my: 'နှစ်ဦးဆက်နွယ်မှု / သံယောဇဉ်' },
	partner: { en: 'Partner / Other', my: 'လက်တွဲဖော် / အခြားသူ' },
	dynamics: { en: 'Dynamics / Connection', my: 'ဆက်ဆံရေးအခြေအနေ' },
	relationship_dynamics: { en: 'Relationship Dynamics', my: 'ဆက်ဆံရေးအခြေအနေ' },
	current_situation: { en: 'Current Situation', my: 'လက်ရှိအခြေအနေ' },
	outcome_a: { en: 'Outcome A', my: 'လမ်းကြောင်း (က) ၏ ရလဒ်' },
	outcome_b: { en: 'Outcome B', my: 'လမ်းကြောင်း (ခ) ၏ ရလဒ်' },
	core_self: { en: 'Core Self', my: 'မိမိ၏ ပင်ကိုစိတ်' },
	subconscious: { en: 'Subconscious', my: 'မသိစိတ်၏ လှုံ့ဆော်မှု' },
	growth_path: { en: 'Growth Path', my: 'တိုးတက်ရာ လမ်းကြောင်း' },
	strength: { en: 'Strength', my: 'အားသာချက်နှင့် စွမ်းဆောင်ရည်' },
	opportunity: { en: 'Opportunity', my: 'အခွင့်အလမ်းသစ်' },
	present_situation: { en: 'Present Situation', my: 'လက်ရှိဖြစ်တည်မှု' },
	immediate_challenge: { en: 'Immediate Challenge', my: 'ရင်ဆိုင်နေရသော စိန်ခေါ်မှု' },
	distant_past: { en: 'Distant Past', my: 'ဝေးကွာသော အတိတ်အကြောင်း' },
	recent_past: { en: 'Recent Past', my: 'လတ်တလော အတိတ်' },
	best_outcome: { en: 'Best Outcome', my: 'အကောင်းဆုံး အလားအလာ' },
	immediate_future: { en: 'Immediate Future', my: 'မကြာမီကာလ အနာဂတ်' },
	factors_affecting: { en: 'Factors Affecting', my: 'သက်ရောက်နေသော အကြောင်းအရာများ' },
	final_outcome: { en: 'Final Outcome', my: 'နောက်ဆုံးရလဒ်' },
	path_a: { en: 'Path A', my: 'ရွေးချယ်မှု လမ်းကြောင်း (က)' },
	path_b: { en: 'Path B', my: 'ရွေးချယ်မှု လမ်းကြောင်း (ခ)' },
	what_to_understand: { en: 'What to Understand', my: 'နားလည်သဘောပေါက်ရမည့်အရာ' },
	what_to_release: { en: 'What to Release', my: 'လက်လွှတ်စွန့်လွှတ်ရမည့်အရာ' },
	inner_truth: { en: 'Inner Truth', my: 'အတွင်းစိတ်အမှန်တရား' },
	external_influences: { en: 'External Influences', my: 'ပြင်ပလွှမ်းမိုးမှုများ' },
	hopes_and_fears: { en: 'Hopes & Fears', my: 'မျှော်လင့်ချက်နှင့် စိုးရိမ်မှုများ' },
	foundation: { en: 'Foundation', my: 'အခြေခံအကြောင်းရင်း' }
};

// SPREAD TYPES TRANSLATIONS
export const SPREAD_TYPES_DATA: Record<
	string,
	{ nameEn: string; nameMy: string; descEn: string; descMy: string }
> = {
	one_card: {
		nameEn: 'One Card',
		nameMy: 'တစ်ကတ်ဆွဲ စနစ်',
		descEn: 'Simple daily guidance and quick clarity',
		descMy: 'နေ့စဉ်လမ်းညွှန်ချက်နှင့် အမြန်အဖြေရှာဖွေရန်'
	},
	three_card: {
		nameEn: 'Three Card',
		nameMy: 'သုံးကတ်ဆွဲ စနစ် (အတိတ်၊ ပစ္စုပ္ပန်၊ အနာဂတ်)',
		descEn: 'Past, Present, Future or Mind, Body, Spirit',
		descMy: 'အတိတ်၊ ပစ္စုပ္ပန်၊ အနာဂတ် သို့မဟုတ် စိတ်၊ ကိုယ်၊ ဝိညာဉ် ဆန်းစစ်ခြင်း'
	},
	decision: {
		nameEn: 'Decision Spread',
		nameMy: 'လမ်းခွဲရွေးချယ်မှု စနစ်',
		descEn: 'Compare two alternative paths and choices',
		descMy: 'လမ်းကြောင်းနှစ်ခုကို နှိုင်းယှဉ်ဆုံးဖြတ်ရန်'
	},
	self_reflection: {
		nameEn: 'Self Reflection',
		nameMy: 'မိမိကိုယ်ကိုဆန်းစစ်ခြင်း စနစ်',
		descEn: 'Inner exploration, subconscious blocks, and personal growth',
		descMy: 'အတွင်းစိတ်စူးစမ်းခြင်းနှင့် ကိုယ်ပိုင်တိုးတက်မှု'
	},
	relationship: {
		nameEn: 'Relationship Spread',
		nameMy: 'အချစ်ရေးနှင့် မိတ်ဖက်ဆက်ဆံရေး စနစ်',
		descEn: 'Analyze connection, harmony, and partner dynamic',
		descMy: 'နှစ်ဦးနှစ်ဖက် သဟဇာတဖြစ်မှုနှင့် ဆက်ဆံရေးဆန်းစစ်ရန်'
	},
	career: {
		nameEn: 'Career Guidance',
		nameMy: 'အလုပ်အကိုင်နှင့် စီးပွားရေးလမ်းညွှန် စနစ်',
		descEn: 'Professional aspirations, obstacles, and opportunities',
		descMy: 'လုပ်ငန်းခွင်အခွင့်အလမ်းများနှင့် စိန်ခေါ်မှုများ'
	},
	custom: {
		nameEn: 'Custom Draw',
		nameMy: 'စိတ်ကြိုက်ကတ်အရေအတွက်ဆွဲခြင်း',
		descEn: 'Pick your own card count from 1 to 10',
		descMy: '၁ ကတ်မှ ၁၀ ကတ်အထိ မိမိစိတ်ကြိုက် ရွေးချယ်ဆွဲယူခြင်း'
	}
};

// READING TOPICS TRANSLATIONS
export const TOPICS_DATA: Record<string, { labelEn: string; labelMy: string }> = {
	love: { labelEn: 'Love & Romance', labelMy: 'အချစ်ရေးနှင့် အိမ်ထောင်ရေး' },
	career: { labelEn: 'Career & Work', labelMy: 'အလုပ်အကိုင်နှင့် ရာထူး' },
	finance: { labelEn: 'Finance & Wealth', labelMy: 'ငွေကြေးနှင့် စီးပွားဥစ္စာ' },
	personal_growth: { labelEn: 'Personal Growth', labelMy: 'ကိုယ်ပိုင်တိုးတက်မှု' },
	communication: { labelEn: 'Communication', labelMy: 'ဆက်ဆံရေးနှင့် ပြောဆိုမှု' },
	education: { labelEn: 'Education & Studies', labelMy: 'ပညာရေးနှင့် သင်ယူလေ့လာမှု' },
	general: { labelEn: 'General Guidance', labelMy: 'အထွေထွေဘဝလမ်းညွှန်' }
};

// SUITS TRANSLATIONS
export const SUITS_DATA: Record<
	string,
	{ labelEn: string; labelMy: string; elementEn: string; elementMy: string }
> = {
	all: {
		labelEn: 'All Cards',
		labelMy: 'ကတ်အားလုံး (၇၈ ကတ်)',
		elementEn: 'All',
		elementMy: 'အားလုံး'
	},
	major: {
		labelEn: 'Major Arcana',
		labelMy: 'မေဂျာအာခါနာ (အဓိကကတ် ၂၂ ကတ်)',
		elementEn: 'Spirit',
		elementMy: 'ဝိညာဉ်ဓာတ်'
	},
	wands: {
		labelEn: 'Wands (Fire)',
		labelMy: 'တုတ်ချောင်း (မီးဓာတ်)',
		elementEn: 'Fire',
		elementMy: 'မီးဓာတ်'
	},
	cups: {
		labelEn: 'Cups (Water)',
		labelMy: 'ခွက် (ရေဓာတ်)',
		elementEn: 'Water',
		elementMy: 'ရေဓာတ်'
	},
	swords: {
		labelEn: 'Swords (Air)',
		labelMy: 'ဓား (လေဓာတ်)',
		elementEn: 'Air',
		elementMy: 'လေဓာတ်'
	},
	pentacles: {
		labelEn: 'Pentacles (Earth)',
		labelMy: 'ဒင်္ဂါး (မြေဓာတ်)',
		elementEn: 'Earth',
		elementMy: 'မြေဓာတ်'
	}
};

// HELPER FUNCTIONS
export function normalizeCardKey(nameOrCard: string): string {
	if (!nameOrCard) return '';
	// Match against standard keys
	const lower = nameOrCard.toLowerCase().trim();
	for (const key of Object.keys(TAROT_CARDS_DATA)) {
		if (key.toLowerCase() === lower) return key;
		const snake = key.toLowerCase().replace(/[']/g, '').replace(/ /g, '_');
		if (snake === lower) return key;
	}
	return nameOrCard;
}

export function getCardTranslation(
	cardNameOrId: string,
	locale: SupportedLocale
): {
	name: string;
	arcana: string;
	suit: string;
	element: string;
	keywords: string[];
	meaningUpright: string;
	meaningReversed: string;
} {
	const key = normalizeCardKey(cardNameOrId);
	const data = TAROT_CARDS_DATA[key];
	if (!data) {
		return {
			name: cardNameOrId,
			arcana: 'Tarot',
			suit: 'Tarot',
			element: 'Arcana',
			keywords: [],
			meaningUpright: '',
			meaningReversed: ''
		};
	}

	if (locale === 'my') {
		return {
			name: data.nameMy,
			arcana: data.arcanaMy,
			suit: data.suitMy,
			element: data.elementMy,
			keywords: data.keywordsMy,
			meaningUpright: data.meaningUprightMy,
			meaningReversed: data.meaningReversedMy
		};
	}

	return {
		name: data.nameEn,
		arcana: data.arcanaEn,
		suit: data.suitEn,
		element: data.elementEn,
		keywords: data.keywordsEn,
		meaningUpright: data.meaningUprightEn,
		meaningReversed: data.meaningReversedEn
	};
}

export function translatePosition(pos: string | undefined | null, locale: SupportedLocale): string {
	if (!pos) return '';
	if (locale === 'en') return pos;
	const key = pos
		.toLowerCase()
		.trim()
		.replace(/[^a-z0-9]+/g, '_');
	return SPREAD_POSITIONS_DATA[key]?.my || pos;
}

export function translateKeyword(kw: string, locale: SupportedLocale): string {
	if (!kw || locale === 'en') return kw;
	// Search in TAROT_CARDS_DATA for matching keyword
	for (const card of Object.values(TAROT_CARDS_DATA)) {
		const idx = card.keywordsEn.findIndex((k) => k.toLowerCase() === kw.toLowerCase());
		if (idx >= 0 && card.keywordsMy[idx]) {
			return card.keywordsMy[idx];
		}
	}
	return kw;
}

export function translateSpreadType(
	spreadType: string | undefined | null,
	locale: SupportedLocale
): string {
	if (!spreadType) return '';
	const key = spreadType
		.toLowerCase()
		.trim()
		.replace(/[^a-z0-9]+/g, '_');
	const data = SPREAD_TYPES_DATA[key];
	if (!data) return spreadType;
	return locale === 'my' ? data.nameMy : data.nameEn;
}

export function translateTopic(topic: string | undefined | null, locale: SupportedLocale): string {
	if (!topic) return '';
	const key = topic
		.toLowerCase()
		.trim()
		.replace(/[^a-z0-9]+/g, '_');
	const data = TOPICS_DATA[key];
	if (!data) return topic;
	return locale === 'my' ? data.labelMy : data.labelEn;
}

export const THEMES_DATA_MY: Record<string, string> = {
	awakening: 'နိုးထခြင်း',
	choice: 'ရွေးချယ်မှု',
	grief: 'ဝမ်းနည်းပူဆွေးမှု',
	harmony: 'သဟဇာတဖြစ်မှု',
	heartbreak: 'စိတ်နှလုံးကြေကွဲမှု',
	love: 'ချစ်ခြင်းမေတ္တာ',
	moving_on: 'ရှေ့ဆက်လှမ်းခြင်း',
	'moving on': 'ရှေ့ဆက်လှမ်းခြင်း',
	movingon: 'ရှေ့ဆက်လှမ်းခြင်း',
	new_perspective: 'အမြင်သစ်ရရှိခြင်း',
	'new perspective': 'အမြင်သစ်ရရှိခြင်း',
	newperspective: 'အမြင်သစ်ရရှိခြင်း',
	patience: 'စိတ်ရှည်သည်းခံမှု',
	relationships: 'လူမှုဆက်ဆံရေး',
	revelation: 'အမှန်တရားဖော်ထုတ်တွေ့ရှိခြင်း',
	sacrifice: 'စွန့်လွှတ်အနစ်နာခံမှု',
	sudden_change: 'ရုတ်တရက်ပြောင်းလဲမှု',
	'sudden change': 'ရုတ်တရက်ပြောင်းလဲမှု',
	suddenchange: 'ရုတ်တရက်ပြောင်းလဲမှု',
	surrender: 'လက်ခံအရှုံးပေးခြင်း',
	transition: 'ကူးပြောင်းခြင်း',
	upheaval: 'ကြီးမားသောလှုပ်ခတ်မှု',
	reflection: 'ဆင်ခြင်သုံးသပ်ခြင်း',
	balance: 'မျှတမှု',
	courage: 'ရဲရင့်သတ္တိ',
	wisdom: 'ဉာဏ်ပညာ',
	growth: 'တိုးတက်ဖွံ့ဖြိုးမှု',
	opportunity: 'အခွင့်အလမ်း',
	clarity: 'ရှင်းလင်းပြတ်သားမှု',
	healing: 'ကုစားသက်သာမှု',
	inner_strength: 'အတွင်းစိတ်ခွန်အား',
	'inner strength': 'အတွင်းစိတ်ခွန်အား',
	passion: 'စိတ်အားထက်သန်မှု',
	success: 'အောင်မြင်မှု',
	abundance: 'ကြွယ်ဝပြည့်စုံမှု',
	intuition: 'အလိုလိုသိစိတ်',
	transformation: 'ဘဝအသွင်ပြောင်းလဲမှု',
	conflict: 'ပဋိပက္ခစိန်ခေါ်မှု',
	illusion: 'ထင်ယောင်ထင်မှားဖြစ်မှု',
	hope: 'မျှော်လင့်ချက်ရောင်ခြည်',
	renewal: 'ပြန်လည်နိုးထဆန်းသစ်မှု',
	completion: 'ပြည့်စုံပြီးမြောက်မှု',
	rest: 'အနားယူဆင်ခြင်ခြင်း',
	action: 'လက်တွေ့လုပ်ဆောင်မှု',
	willpower: 'စိတ်ပိုင်းဖြတ်မှုစွမ်းအား',

	// Newly added themes from Prolog rule base
	ambition: 'ကြီးမားသော ရည်မှန်းချက်',
	following_heart: 'နှလုံးသားဆန္ဒအတိုင်း လိုက်နာခြင်း',
	followingheart: 'နှလုံးသားဆန္ဒအတိုင်း လိုက်နာခြင်း',
	'following heart': 'နှလုံးသားဆန္ဒအတိုင်း လိုက်နာခြင်း',
	new_skills: 'ကျွမ်းကျင်မှုအသစ်များ သင်ယူခြင်း',
	newskills: 'ကျွမ်းကျင်မှုအသစ်များ သင်ယူခြင်း',
	'new skills': 'ကျွမ်းကျင်မှုအသစ်များ သင်ယူခြင်း',
	diligence: 'ဇွဲလုံ့လ စိုက်ထုတ်ခြင်း',
	adventure: 'စွန့်စားရှာဖွေခြင်း',
	spontaneity: 'လွတ်လပ်ပေါ့ပါးမှု',
	new_beginnings: 'အစပျိုးခြင်းသစ်များ',
	'new beginnings': 'အစပျိုးခြင်းသစ်များ',
	newbeginnings: 'အစပျိုးခြင်းသစ်များ',
	manifestation: 'လက်တွေ့ဖော်ဆောင်မှု',
	mystery: 'ဆန်းကြယ်နက်နဲမှု',
	inner_wisdom: 'အတွင်းစိတ်ဉာဏ်ပညာ',
	'inner wisdom': 'အတွင်းစိတ်ဉာဏ်ပညာ',
	innerwisdom: 'အတွင်းစိတ်ဉာဏ်ပညာ',
	nurturing: 'နွေးထွေးစွာ ပြုစုစောင့်ရှောက်ခြင်း',
	authority: 'ဩဇာအာဏာနှင့် ခေါင်းဆောင်မှု',
	structure: 'စနစ်ကျခိုင်မာမှု',
	stability: 'တည်ငြိမ်ခိုင်မြဲမှု',
	discipline: 'စည်းကမ်းနှင့် ကိုယ်ကျင့်တရား',
	tradition: 'ရိုးရာဓလေ့နှင့် လမ်းညွှန်မှု',
	spirituality: 'စိတ်ဝိညာဉ်နိုးထမှု',
	learning: 'ပညာရပ်များ သင်ယူလေ့လာခြင်း',
	determination: 'ပြတ်သားသော ဆုံးဖြတ်ချက်',
	victory: 'အောင်ပွဲနှင့် ပြီးမြောက်မှု',
	compassion: 'စာနာကြင်နာမှု',
	solitude: 'တစ်ကိုယ်တည်း တည်ငြိမ်စွာ ဆင်ခြင်ခြင်း',
	introspection: 'မိမိစိတ်ကို ပြန်လည်စူးစမ်းခြင်း',
	change: 'အပြောင်းအလဲ',
	cycles: 'ဘဝသံသရာ လည်ပတ်မှု',
	destiny: 'ကံကြမ္မာ',
	luck: 'ကံကောင်းခြင်း',
	fairness: 'တရားမျှတမှု',
	truth: 'အမှန်တရား',
	accountability: 'တာဝန်ယူမှု',
	vitality: 'တက်ကြွသော စွမ်းအင်',
	leadership: 'ခေါင်းဆောင်မှုအရည်အသွေး',
	generosity: 'ရက်ရောစွန့်ကြဲမှု',
	mastery: 'ကျွမ်းကျင်ပိုင်နိုင်မှု',
	focus: 'အာရုံစူးစိုက်မှု',
	education: 'ပညာရေးနှင့် သင်ယူမှု',
	intellect: 'ထက်မြက်သော ဉာဏ်ရည်',
	curiosity: 'စူးစမ်းလေ့လာလိုစိတ်',
	connection: 'စိတ်ချင်းဆက်နွယ်မှု',
	partnership: 'လက်တွဲဖော် သဟဇာတ',
	practicality: 'လက်တွေ့ကျကျ ဆောင်ရွက်ခြင်း',
	security: 'လုံခြုံစိတ်ချရမှု',
	prosperity: 'စီးပွားဖွံ့ဖြိုးကြွယ်ဝမှု',
	investment: 'အနာဂတ်အတွက် ရင်းနှီးမြှုပ်နှံမှု',
	ideas: 'အတွေးအခေါ်သစ်များ',
	diplomacy: 'လိမ္မာပါးနပ်စွာ ဆက်ဆံမှု',
	hard_work: 'ကြိုးစားအားထုတ်မှု',
	hardwork: 'ကြိုးစားအားထုတ်မှု',
	'hard work': 'ကြိုးစားအားထုတ်မှု',
	perseverance: 'ဇွဲသတ္တိဖြင့် ကြံ့ကြံ့ခံမှု',
	resilience: 'ခံနိုင်ရည်ရှိမှု',
	illumination: 'ဉာဏ်အလင်းပွင့်မှု',
	rebirth: 'ပြန်လည်နိုးထရှင်သန်ခြင်း',
	relationship: 'ဆက်ဆံရေးနှင့် သံယောဇဉ်',
	release: 'လက်လွှတ်စွန့်လွှတ်ခြင်း',
	burden: 'ဝန်ထုပ်ဝန်ပိုး',
	responsibility: 'တာဝန်ယူမှု',
	productivity: 'အကျိုးဖြစ်ထွန်းမှု',
	routine: 'ပုံမှန်ဆောင်ရွက်မှု',
	conservatism: 'သတိကြီးစွာ ထိန်းသိမ်းမှု',
	extra_responsibility: 'တာဝန်အပိုများ ထမ်းဆောင်ခြင်း'
};

export function translateTheme(theme: string | undefined | null, locale: SupportedLocale): string {
	if (!theme) return '';
	if (locale !== 'my') return theme.replace(/_/g, ' ');
	const normalized = theme.toLowerCase().trim();
	const clean = normalized.replace(/_/g, '').replace(/ /g, '');
	for (const [k, v] of Object.entries(THEMES_DATA_MY)) {
		if (k.replace(/_/g, '').replace(/ /g, '') === clean) {
			return v;
		}
	}
	return translateKeyword(theme, 'my') || theme.replace(/_/g, ' ');
}

export function formatReadingSynthesis(
	aiInterpretation: string,
	reading: {
		question?: string;
		cards?: Array<{ name: string; position?: string; is_reversed?: boolean; keywords?: string[] }>;
		themes?: string[];
		zodiac_sign?: string;
		category?: string;
		topic?: string;
	},
	locale: SupportedLocale
): string {
	if (!aiInterpretation && (!reading.cards || reading.cards.length === 0)) return '';
	if (locale !== 'my') return aiInterpretation;

	const isBackendFallback =
		aiInterpretation &&
		(aiInterpretation.includes('သင်၏ မေးခွန်းဖြစ်သော') ||
			aiInterpretation.includes(
				'ဤမေးခွန်းအတွက် ကတ်များသည် စိတ်ရှည်တည်ငြိမ်စွာ စူးစိုက်ဆင်ခြင်ရန်'
			));

	// If genuine AI interpretation exists (from LLM), return it!
	if (
		aiInterpretation &&
		!isBackendFallback &&
		/[\u1000-\u109F]/.test(aiInterpretation) &&
		aiInterpretation.length > 200
	) {
		return aiInterpretation;
	}

	const question = (reading.question || '').trim();
	const cards = reading.cards || [];
	const cardNamesMy = cards
		.map((c) => `${getCardTranslation(c.name, 'my').name} (${c.name})`)
		.join('၊ ');
	const themes = reading.themes || [];
	const themesMy = themes
		.map((t) => translateTheme(t, 'my'))
		.filter(Boolean)
		.join('၊ ');
	const categoryMy = translateTopic(reading.category || reading.topic, 'my') || 'အထွေထွေဘဝကဏ္ဍ';

	const qLower = question.toLowerCase();

	const isLoveTiming =
		/ကြာဦးမှာလား|ရဖို့|ရမှာလား|တွေ့မလား|တွေ့ရမှာလား|ဘယ်တော့|အချိန်|when|soon|boyfriend|girlfriend|ကောင်လေး|ကောင်မလေး/.test(
			qLower
		) &&
		(/ချစ်သူ|ရည်းစား|အချစ်|ကောင်လေး|ကောင်မလေး|လက်တွဲဖော်|love|crush|partner/.test(qLower) ||
			reading.category === 'relationship' ||
			reading.topic === 'love');

	const isLoveGeneral =
		/အချစ်|ချစ်သူ|ရည်းစား|အိမ်ထောင်|မင်္ဂလာ|ကြိုက်|တွဲ|သဘောကျ|crush|လက်ထပ်|love|dating|partner|marriage/.test(
			qLower
		) ||
		reading.category === 'relationship' ||
		reading.topic === 'love';

	const isEducation =
		/စာမေးပွဲ|အောင်|ကျောင်း|တက္ကသိုလ်|ပညာရေး|ဘွဲ့|သင်တန်း|စာသင်|exam|test|study|pass|fail|education|grade/.test(
			qLower
		) ||
		reading.category === 'education' ||
		reading.topic === 'education';

	const isCareer =
		/အလုပ်|ရာထူး|စီးပွားရေး|ကုမ္ပဏီ|အင်တာဗျူး|လုပ်ငန်း|career|job|work|promotion|business/.test(
			qLower
		) ||
		reading.category === 'career' ||
		reading.topic === 'career';

	const isFinance =
		/ငွေ|ပိုက်ဆံ|ကြွေး|ချမ်းသာ|လစာ|ရင်းနှီးမြှုပ်နှံ|ဓန|finance|money|wealth|salary|invest/.test(
			qLower
		) ||
		reading.category === 'finance' ||
		reading.topic === 'finance';

	const isDecisionOrYesNo =
		/ရမလား|ဖြစ်မလား|သင့်သလား|ကောင်းမလား|ဖြစ်နိုင်မလား|ရနိုင်မလား|မလား|လား|will|should|can|could|would|decision|choice|opt/.test(
			qLower
		) ||
		reading.category === 'decision' ||
		reading.topic === 'decision';

	// SECTION 1: QUESTION-SPECIFIC DIRECT ANSWER
	let section1: string;
	if (isLoveTiming) {
		section1 =
			`**၁။ မေးခွန်းနှင့် ပတ်သက်သော တိုက်ရိုက်ဆန်းစစ်ချက် (အချစ်သစ် ပေါ်ပေါက်လာနိုင်မှုနှင့် အချိန်ကာလ)**\n` +
			`${question ? `သင်၏ မေးခွန်းဖြစ်သော "${question}" နှင့် စပ်လျဉ်း၍ ဆန်းစစ်ရလျှင် -\n\n` : ''}` +
			`ကျရောက်သော တားရော့ကတ်များအနက် ${cardNamesMy || 'ရွေးချယ်ထားသော ကတ်များ'} တို့၏ ညွှန်ပြချက်အရ၊ သင့်ဘဝထဲသို့ စစ်မှန်သော လက်တွဲဖော် သို့မဟုတ် ချစ်သူ ရောက်ရှိလာရန်အတွက် လောလောဆယ်တွင် အချို့သော အတွင်းစိတ်ပြင်ဆင်မှုများနှင့် အချိန်ကာလတစ်ခု လိုအပ်နေသေးကြောင်း ဖော်ပြနေပါသည်။\n\n` +
			`ကတ်များက သင့်အား အလျင်စလို မရှာဖွေဘဲ မိမိကိုယ်ကို ချစ်ခင်တန်ဖိုးထားမှု၊ စိတ်ပိုင်းဆိုင်ရာ တည်ငြိမ်မှုနှင့် ကိုယ်ပိုင်ရပ်တည်မှုကို အရင်ခိုင်မာအောင် ပြင်ဆင်ထားရန် အကြံပြုထားပါသည်။ အတိတ်မှ စိတ်ဒဏ်ရာဟောင်းများ သို့မဟုတ် သံသယများကို လက်လွှတ်လိုက်ပြီး မိမိဘက်မှ အဆင်သင့်ဖြစ်ချိန်တွင် သင့်အတွက် အသင့်တော်ဆုံး စစ်မှန်သော မေတ္တာရှင်သည် မမျှော်လင့်ဘဲ ဆုံဆည်းလာပါလိမ့်မည်။`;
	} else if (isLoveGeneral) {
		section1 =
			`**၁။ မေးခွန်းနှင့် ပတ်သက်သော တိုက်ရိုက်ဆန်းစစ်ချက် (အချစ်ရေးနှင့် သံယောဇဉ်)**\n` +
			`${question ? `သင်၏ မေးခွန်းဖြစ်သော "${question}" နှင့် စပ်လျဉ်း၍ -\n\n` : ''}` +
			`တားရော့ကတ်များအနက် ${cardNamesMy || 'ရွေးချယ်ထားသော ကတ်များ'} ကျရောက်ခဲ့ပြီး ${themesMy ? themesMy + ' ဆိုင်ရာ' : ''} စွမ်းအင်များကို ထင်ဟပ်စေပါသည်။\n\n` +
			`ဤကတ်များသည် နှစ်ဦးနှစ်ဖက်အကြား နားလည်မှု၊ ပွင့်လင်းစွာ ဆက်ဆံပြောဆိုမှုနှင့် အတွင်းစိတ်ခံစားချက်များကို အလေးထားသင့်ကြောင်း ညွှန်ပြနေပါသည်။ အထင်အမြင်လွဲမှားမှုများကို ရှောင်ရှားပြီး ရိုးသားနွေးထွေးသော စေတနာဖြင့် ချဉ်းကပ်ရန် အချိန်အခါကောင်း ဖြစ်ပါသည်။`;
	} else if (isEducation) {
		section1 =
			`**၁။ မေးခွန်းနှင့် ပတ်သက်သော တိုက်ရိုက်ဆန်းစစ်ချက် (စာမေးပွဲနှင့် ပညာရေးအောင်မြင်မှု)**\n` +
			`${question ? `သင်၏ မေးခွန်းဖြစ်သော "${question}" နှင့် စပ်လျဉ်း၍ -\n\n` : ''}` +
			`တားရော့ဗေဒင်မေးမြန်းမှုတွင် ${cardNamesMy || 'ရွေးချယ်ထားသော ကတ်များ'} ကျရောက်ခဲ့ပြီး ${themesMy ? themesMy + ' စသည့်' : ''} စွမ်းအင်များကို ပေါ်လွင်စေပါသည်။\n\n` +
			`ကျရောက်သော ကတ်များသည် သင်၏ ကြိုးစားအားထုတ်မှု၊ စိတ်အားထက်သန်သော အရှိန်အဟုန်နှင့် စူးစိုက်မှုတို့သည် အမြင့်မားဆုံး အဆင့်သို့ ရောက်ရှိနေကြောင်း ပြသနေပါသည်။ စာမေးပွဲအောင်မြင်ရန်အတွက် လုံလောက်သော ဉာဏ်ရည်နှင့် ကြိုးပမ်းလိုစိတ် အပြည့်အဝရှိသော်လည်း၊ အလျင်စလို ဖြေဆိုခြင်းနှင့် စိတ်လှုပ်ရှားလွန်ကဲခြင်းတို့ကို အထူးသတိပြု ထိန်းချုပ်ရန် လိုအပ်ပါသည်။`;
	} else if (isCareer) {
		section1 =
			`**၁။ မေးခွန်းနှင့် ပတ်သက်သော တိုက်ရိုက်ဆန်းစစ်ချက် (အလုပ်အကိုင်နှင့် စီးပွားရေး)**\n` +
			`${question ? `သင်၏ မေးခွန်းဖြစ်သော "${question}" နှင့် စပ်လျဉ်း၍ -\n\n` : ''}` +
			`တားရော့ဗေဒင်တွင် ${cardNamesMy || 'ရွေးချယ်ထားသော ကတ်များ'} ကျရောက်ခဲ့ပြီး လုပ်ငန်းခွင်ဆိုင်ရာ အခွင့်အလမ်းသစ်များနှင့် အပြောင်းအလဲများကို ညွှန်ပြနေပါသည်။\n\n` +
			`မိမိ၏ အတွေ့အကြုံနှင့် စွမ်းဆောင်ရည်ကို ယုံကြည်စိတ်ချစွာ အသုံးချရန်နှင့် မိတ်ဖက်များနှင့် ဆက်ဆံရေးကောင်းမွန်အောင် ထိန်းသိမ်းရန် အကြံပြုထားပါသည်။`;
	} else if (isFinance) {
		section1 =
			`**၁။ မေးခွန်းနှင့် ပတ်သက်သော တိုက်ရိုက်ဆန်းစစ်ချက် (ငွေကြေးနှင့် ဓနဥစ္စာ)**\n` +
			`${question ? `သင်၏ မေးခွန်းဖြစ်သော "${question}" နှင့် စပ်လျဉ်း၍ -\n\n` : ''}` +
			`တားရော့ကတ်များအနက် ${cardNamesMy || 'ရွေးချယ်ထားသော ကတ်များ'} ကျရောက်ခဲ့ပြီး ငွေကြေးဆိုင်ရာ အခြေအနေကို စနစ်တကျ စီမံခန့်ခွဲရန် လိုအပ်ကြောင်း ပြသနေပါသည်။\n\n` +
			`မလိုအပ်သော ကုန်ကျစရိတ်များကို ထိန်းသိမ်းပြီး ရေရှည်တည်ငြိမ်မှုရှိစေမည့် အစီအစဉ်များကို ဦးစားပေးသင့်ပါသည်။`;
	} else if (isDecisionOrYesNo) {
		section1 =
			`**၁။ မေးခွန်းနှင့် ပတ်သက်သော တိုက်ရိုက်ဆန်းစစ်ချက် (ရွေးချယ်မှုနှင့် စွမ်းအင်စီးဆင်းမှု)**\n` +
			`${question ? `သင်၏ မေးခွန်းဖြစ်သော "${question}" နှင့် စပ်လျဉ်း၍ -\n\n` : ''}` +
			`တားရော့ကတ်များဖြစ်သည့် ${cardNamesMy || 'ရွေးချယ်ထားသော ကတ်များ'} တို့သည် တရားသေ "ဟုတ်/မဟုတ်" ထက်မက လက်ရှိစွမ်းအင်စီးဆင်းမှု၊ အခွင့်အလမ်းများနှင့် သတိပြုဖွယ် အချက်များကို ညွှန်ပြနေပါသည်။\n\n` +
			`လက်ရှိအခြေအနေတွင် အလားအလာကောင်းများ ရှိနေသော်လည်း၊ အလျင်စလို မဆုံးဖြတ်ဘဲ အချက်အလက်များကို သေချာစွာ ချိန်ဆရန်နှင့် မိမိ၏ အလိုလိုသိစိတ်ကို နားထောင်ပြီးမှသာ ရွေးချယ်မှုတစ်ခုကို အတည်ပြုရန် အကြံပြုထားပါသည်။`;
	} else {
		section1 =
			`**၁။ မေးခွန်းနှင့် ပတ်သက်သော တိုက်ရိုက်ဆန်းစစ်ချက် (${categoryMy})**\n` +
			`${question ? `သင်၏ မေးခွန်းဖြစ်သော "${question}" နှင့် စပ်လျဉ်း၍ -\n\n` : ''}` +
			`တားရော့ဗေဒင်တွင် ${cardNamesMy || 'ရွေးချယ်ထားသော ကတ်များ'} ကျရောက်ခဲ့ပြီး ${themesMy ? themesMy + ' စသည့်' : ''} သင်္ကေတအဓိပ္ပာယ်များကို ပေါ်လွင်စေပါသည်။\n\n` +
			`ကျရောက်သော ကတ်များ၏ လမ်းညွှန်ချက်အရ ${categoryMy} နှင့် သက်ဆိုင်သော ကိစ္စရပ်များတွင် အလေးအနက်ထား စဉ်းစားဆင်ခြင်ရန်နှင့် လက်တွေ့ကျသော ခြေလှမ်းများကို စတင်လှမ်းရန် သင့်တော်သော အချိန်အခါဖြစ်ကြောင်း ညွှန်ပြနေပါသည်။`;
	}

	// SECTION 2: CARD-BY-CARD DETAILED BREAKDOWN WITH LIGHT & SHADOW
	const section2 =
		`**၂။ ကျရောက်သော ကတ်တစ်ခုချင်းစီ၏ အသေးစိတ်အနက်ဖွင့်ဆိုချက်**\n` +
		cards
			.map((c, i) => {
				const cTrans = getCardTranslation(c.name, 'my');
				const orient = c.is_reversed ? ' (ပြောင်းပြန် - Reversed)' : ' (မူမှန် - Upright)';
				const pos = translatePosition(c.position, 'my') || c.position || `ကတ် ${i + 1}`;

				let dynamicInsight: string;
				let lightAspect: string;
				let shadowAspect: string;

				if (isLoveTiming || isLoveGeneral) {
					if (c.name.includes('Cups')) {
						dynamicInsight =
							'ဤကတ်သည် နှလုံးသားခံစားချက်၊ သံယောဇဉ်နှင့် မေတ္တာတရား စီးဆင်းမှုကို အဓိကဖော်ပြပြီး မေးခွန်းနှင့် ပတ်သက်၍ နွေးထွေးသော နားလည်မှုနှင့် စိတ်ချင်းဆက်နွယ်မှု ဖြစ်ထွန်းလာနိုင်ကြောင်း ပြသနေပါသည်။';
						lightAspect = c.is_reversed
							? 'မိမိကိုယ်ကို အရင်ဆုံး ပြန်လည်ကုစားခွင့်ရရှိခြင်း'
							: 'စစ်မှန်သော နှလုံးသားချင်း ထပ်တူကျမှုနှင့် မေတ္တာသစ် ဆုံဆည်းနိုင်မှု';
						shadowAspect = c.is_reversed
							? 'ခံစားချက်လွန်ကဲခြင်း သို့မဟုတ် အထင်အမြင်လွဲမှားမှုများ ဖြစ်ပေါ်နိုင်ခြင်း'
							: 'မျှော်လင့်ချက်လွန်ကဲပြီး အခြေအနေမှန်ကို မျက်ကွယ်ပြုမိခြင်း';
					} else if (c.name.includes('Pentacles')) {
						dynamicInsight =
							'ဤကတ်သည် အချစ်ရေးတွင် ရေရှည်တည်ငြိမ်မှု၊ စိတ်ချယုံကြည်ရမှုနှင့် လက်တွေ့ကျသော ရပ်တည်ချက်ကို ဖော်ပြပြီး အလျင်မလိုဘဲ အချိန်ယူ တည်ဆောက်သင့်ကြောင်း ညွှန်ပြပါသည်။';
						lightAspect = c.is_reversed
							? 'လက်တွေ့မကျသော မျှော်လင့်ချက်များကို သိမြင်ပြင်ဆင်နိုင်ခြင်း'
							: 'ခိုင်မာသော သစ္စာတရားနှင့် ရေရှည်တည်မြဲမည့် သဟဇာတဆက်ဆံရေး';
						shadowAspect = c.is_reversed
							? 'လုံခြုံမှုမရှိဟု ခံစားရခြင်း သို့မဟုတ် တာဝန်ဝတ္တရားများ လေးလံနေခြင်း'
							: 'စည်းစနစ်လွန်းပြီး စိတ်ခံစားချက်ပိုင်းတွင် အေးစက်သွားနိုင်ခြင်း';
					} else if (c.name.includes('Swords')) {
						dynamicInsight =
							'ဤကတ်သည် စိတ်ပိုင်းဆိုင်ရာ ရှင်းလင်းပြတ်သားမှု၊ ဆက်သွယ်ပြောဆိုမှုနှင့် အတွေးသံသယများကို ညွှန်ပြပြီး၊ အတိတ်မှ စိတ်ဒဏ်ရာများကို ဉာဏ်ပညာဖြင့် ဖြေဖျောက်ရန် လိုအပ်ကြောင်း ဖော်ပြပါသည်။';
						lightAspect = c.is_reversed
							? 'စိတ်ဒဏ်ရာဟောင်းများနှင့် သံသယများကို လက်လွှတ်စွန့်လွှတ်နိုင်ခြင်း'
							: 'ပွင့်လင်းရိုးသားစွာ ဆွေးနွေးတိုင်ပင်နိုင်မှုနှင့် အမှန်တရားကို ရင်ဆိုင်နိုင်စွမ်း';
						shadowAspect = c.is_reversed
							? 'စကားအပြောအဆို ကြမ်းတမ်းမိခြင်း သို့မဟုတ် စိုးရိမ်လွန်ကဲခြင်း'
							: 'အတွေးများလွန်းပြီး နှလုံးသားထက် အပြစ်ရှာလိုစိတ် ရှေ့တန်းရောက်ခြင်း';
					} else if (c.name.includes('Wands')) {
						dynamicInsight =
							'ဤကတ်သည် စိတ်အားထက်သန်မှု၊ ဆွဲဆောင်မှုနှင့် တက်ကြွသော စွမ်းအင်စီးဆင်းမှုကို ဖော်ညွှန်းပြီး၊ လူမှုဆက်ဆံရေး အသိုင်းအဝိုင်းသစ်များတွင် ရင်ခုန်ဖွယ် အခွင့်အလမ်းများ ပေါ်ပေါက်စေပါမည်။';
						lightAspect = c.is_reversed
							? 'အရှိန်အဟုန်ကို ပြန်လည်ထိန်းညှိပြီး စိတ်တည်ငြိမ်မှု ရှာဖွေနိုင်ခြင်း'
							: 'တက်ကြွသော စိတ်ဓာတ်ခွန်အားနှင့် ဆွဲဆောင်မှုရှိသော ချဉ်းကပ်နိုင်စွမ်း';
						shadowAspect = c.is_reversed
							? 'စိတ်မရှည်ခြင်း သို့မဟုတ် အားအင်ကုန်ခမ်းနွမ်းနယ်နေခြင်း'
							: 'အလျင်စလို ဆုံးဖြတ်မိပြီး နားလည်မှုလွဲမှားနိုင်ခြင်း';
					} else {
						dynamicInsight =
							'ဤမဟာအာကာနာ (Major Arcana) ကတ်သည် သင့်ဘဝ၏ အရေးပါသော ကံကြမ္မာသင်ခန်းစာနှင့် မေတ္တာရေးရာ အပြောင်းအလဲကြီးတစ်ခု ဖြစ်ပေါ်လာမည့် အလားအလာကို လေးနက်စွာ ညွှန်ပြနေပါသည်။';
						lightAspect = c.is_reversed
							? 'အတွင်းစိတ် အမှန်တရားကို နက်ရှိုင်းစွာ ပြန်လည်သိမြင်ခွင့်ရခြင်း'
							: 'ဘဝလက်တွဲဖော်ဆိုင်ရာ ကံကြမ္မာဆုံဆည်းမှုနှင့် ဝိညာဉ်ရေးရာ နိုးထမှု';
						shadowAspect = c.is_reversed
							? 'ပြောင်းလဲမှုကို ကြောက်ရွံ့ပြီး လက်ဟောင်းကို ဖက်တွယ်ထားမိခြင်း'
							: 'ကံကြမ္မာအပေါ် အလိုအလျောက် ပုံချပြီး မိမိကိုယ်တိုင် ကြိုးစားမှုကို မေ့လျော့ခြင်း';
					}
				} else if (isCareer || isFinance) {
					if (c.name.includes('Pentacles')) {
						dynamicInsight =
							'ဤကတ်သည် ပစ္စည်းဥစ္စာ၊ ရင်းနှီးမြှုပ်နှံမှု၊ လုပ်ငန်းခွင် ရလဒ်များနှင့် ရေရှည်ဓနဥစ္စာ တည်ငြိမ်မှုကို တိုက်ရိုက်ထင်ဟပ်နေပါသည်။';
						lightAspect = c.is_reversed
							? 'ငွေကြေးစီမံခန့်ခွဲမှု အမှားအယွင်းများကို ပြန်လည်ထိန်းကျောင်းနိုင်ခြင်း'
							: 'ခိုင်မာသော စီးပွားရေးအခွင့်အလမ်းနှင့် ကြိုးစားမှုအသီးအပွင့်များ ရရှိခြင်း';
						shadowAspect = c.is_reversed
							? 'ငွေကြေးသုံးစွဲမှု မဆင်ခြင်မိခြင်း သို့မဟုတ် ဝင်ငွေမတည်ငြိမ်ခြင်း'
							: 'ပစ္စည်းဥစ္စာအပေါ် စွဲလမ်းလွန်းပြီး စိတ်ဖိစီးမှုများပြားခြင်း';
					} else if (c.name.includes('Wands')) {
						dynamicInsight =
							'ဤကတ်သည် လုပ်ငန်းခွင် ရည်မှန်းချက်၊ စီမံကိန်းအသစ်များ အကောင်အထည်ဖော်မှုနှင့် ခေါင်းဆောင်မှု အရည်အသွေးတို့ကို ပေါ်လွင်စေပါသည်။';
						lightAspect = c.is_reversed
							? 'အလုပ်ဖိစီးမှုများကို လျှော့ချပြီး အစီအစဉ်သစ် ပြန်လည်ရေးဆွဲနိုင်ခြင်း'
							: 'တီထွင်ဆန်းသစ်မှု၊ စိတ်အားထက်သန်သော အရှိန်အဟုန်နှင့် အောင်မြင်မှု';
						shadowAspect = c.is_reversed
							? 'ဦးတည်ချက်ပျောက်ဆုံးခြင်း သို့မဟုတ် အစီအစဉ်မရှိဘဲ လှုပ်ရှားမိခြင်း'
							: 'တာဝန်အလွန်အကျွံယူမိပြီး ပင်ပန်းနွမ်းနယ်ခြင်း';
					} else if (c.name.includes('Swords')) {
						dynamicInsight =
							'ဤကတ်သည် မဟာဗျူဟာမြောက် စဉ်းစားတွေးခေါ်မှု၊ ညှိနှိုင်းဆွေးနွေးမှုများနှင့် စာချုပ်စာတမ်းဆိုင်ရာ ဆုံးဖြတ်ချက်များကို ဖော်ပြပါသည်။';
						lightAspect = c.is_reversed
							? 'ရှုပ်ထွေးနေသော ပြဿနာများကို ဉာဏ်ဖြင့် ရှင်းထုတ်နိုင်ခြင်း'
							: 'ထက်မြက်သော မဟာဗျူဟာအမြင်နှင့် ပြတ်သားသော ဆုံးဖြတ်ချက်များ ချမှတ်နိုင်စွမ်း';
						shadowAspect = c.is_reversed
							? 'သတင်းမှားများကြောင့် ဆုံးဖြတ်ချက် မှားယွင်းနိုင်ခြင်း'
							: 'လုပ်ဖော်ကိုင်ဖက်များနှင့် အငြင်းပွားမှု သို့မဟုတ် တင်းမာမှုများ ဖြစ်ပေါ်နိုင်ခြင်း';
					} else if (c.name.includes('Cups')) {
						dynamicInsight =
							'ဤကတ်သည် လုပ်ငန်းခွင်အတွင်း လူမှုဆက်ဆံရေး၊ ဖောက်သည်များနှင့် သဟဇာတဖြစ်မှုနှင့် မိမိနှစ်သက်သော အလုပ်ကို ဖန်တီးနိုင်စွမ်းကို ပြသပါသည်။';
						lightAspect = c.is_reversed
							? 'စိတ်ဖိစီးမှုများကို ဖယ်ရှားပြီး စိတ်ကျေနပ်မှုကို ရှာဖွေနိုင်ခြင်း'
							: 'လုပ်ဖော်ကိုင်ဖက်များနှင့် ချစ်ခင်ရင်းနှီးမှုနှင့် ပူးပေါင်းဆောင်ရွက်မှု အောင်မြင်ခြင်း';
						shadowAspect = c.is_reversed
							? 'လုပ်ငန်းခွင်တွင် စိတ်ခံစားချက် ရှေ့တန်းတင်မိခြင်း'
							: 'လက်တွေ့အလုပ်ထက် စိတ်ကူးယဉ်မှုများပြားနေခြင်း';
					} else {
						dynamicInsight =
							'ဤကတ်သည် အလုပ်အကိုင်နှင့် စီးပွားရေးခရီးလမ်းတွင် အရေးပါသော လှည့်ကွက်နှင့် ကြီးမားသော အဆင့်အတန်းတက်လှမ်းမှုတို့ကို ညွှန်ပြနေပါသည်။';
						lightAspect = c.is_reversed
							? 'အတားအဆီးများအကြားမှ သင်ခန်းစာသစ် ထုတ်ယူနိုင်ခြင်း'
							: 'ဂုဏ်သိက္ခာတက်လှမ်းမှုနှင့် ရေရှည်တည်မြဲမည့် အောင်မြင်မှုမှတ်တိုင် စိုက်ထူနိုင်ခြင်း';
						shadowAspect = c.is_reversed
							? 'အခွင့်အလမ်းကောင်းများကို လက်လွတ်မခံမိစေရန် သတိပြုရခြင်း'
							: 'ရရှိထားသော အောင်မြင်မှုအပေါ် မောက်မာမိပါက ဆုံးရှုံးနိုင်ခြင်း';
					}
				} else if (isEducation) {
					dynamicInsight =
						'ဤကတ်သည် ပညာသင်ယူမှု၊ စာမေးပွဲဖြေဆိုမှုနှင့် စိတ်ပိုင်းဆိုင်ရာ အာရုံစူးစိုက်မှု အခြေအနေများကို အနီးကပ်ထင်ဟပ်စေပါသည်။';
					lightAspect = c.is_reversed
						? 'အားနည်းချက်များကို သိမြင်ပြီး စာလေ့လာမှုပုံစံ ပြင်ဆင်နိုင်ခြင်း'
						: 'မှတ်ဉာဏ်ကောင်းမွန်မှု၊ စူးစိုက်မှုနှင့် စာမေးပွဲအောင်မြင်နိုင်ခြေ အားကောင်းခြင်း';
					shadowAspect = c.is_reversed
						? 'စာမေးပွဲနီးမှ ကမန်းကတန်းလုပ်မိခြင်း သို့မဟုတ် စိတ်လှုပ်ရှားလွန်ခြင်း'
						: 'ကိုယ့်ကိုယ်ကို ယုံကြည်မှုလွန်ကဲပြီး ပေါ့ဆမိနိုင်ခြင်း';
				} else if (isDecisionOrYesNo) {
					dynamicInsight =
						'ဤကတ်သည် မေးမြန်းထားသော ကိစ္စရပ်နှင့် စပ်လျဉ်း၍ ဖြစ်ပေါ်နေသော စွမ်းအင်စီးဆင်းမှုနှင့် နောက်ဆက်တွဲ ရလဒ်အလားအလာကို ပေါ်လွင်စေပါသည်။';
					lightAspect = c.is_reversed
						? 'မမြင်နိုင်သော အခက်အခဲများကို ကြိုတင်ကာကွယ်ပြင်ဆင်ခွင့်ရခြင်း'
						: 'အပြုသဘောဆောင်သော အလားအလာနှင့် လိုလားချက်များ အောင်မြင်နိုင်ခြေမြင့်မားခြင်း';
					shadowAspect = c.is_reversed
						? 'သံသယများနှင့် မသေချာမှုများကို သေချာစွာ မစစ်ဆေးဘဲ ခုန်ဆင်းမိနိုင်ခြင်း'
						: 'မျှော်လင့်ချက်လွန်ကဲပြီး အရေးပါသောအချက်များကို လျစ်လျူရှုမိခြင်း';
				} else {
					dynamicInsight =
						'ဤကတ်သည် ဘဝ၏ လက်ရှိအခိုက်အတန့်တွင် သင်ရင်ဆိုင်ကြုံတွေ့နေရသော အခြေအနေကို ဉာဏ်ပညာဖြင့် ဆင်ခြင်သုံးသပ်ရန် လမ်းညွှန်ပေးပါသည်။';
					lightAspect = c.is_reversed
						? 'အတွင်းစိတ်ပြန်လည်ဆန်းစစ်မှုနှင့် အတွေ့အကြုံမှ ရင့်ကျက်လာခြင်း'
						: 'ရှင်းလင်းပြတ်သားသော ရည်မှန်းချက်နှင့် ရှေ့ဆက်လှမ်းနိုင်မည့် ခွန်အား';
					shadowAspect = c.is_reversed
						? 'တုံ့ဆိုင်းနေခြင်း သို့မဟုတ် သံသယစိတ်များ လွှမ်းမိုးနေခြင်း'
						: 'အပြောင်းအလဲကို လက်ခံရန် တွန့်ဆုတ်နေခြင်း';
				}

				return (
					`* **${cTrans.name} (${c.name})**${orient}\n` +
					`  * **တည်နေရာ**: ${pos}\n` +
					`  * **စွမ်းအင်နှင့် ဆန်းစစ်ချက်**: ${dynamicInsight}\n` +
					`  * **အလင်းဘက်ခြမ်း (အခွင့်အလမ်း)**: ${lightAspect}\n` +
					`  * **သတိပြုဖွယ် (အရိပ်ဘက်ခြမ်း)**: ${shadowAspect}`
				);
			})
			.join('\n\n');

	// SECTION 3: ACTIONABLE GUIDANCE & CONCLUSION (TAILORED TO ALL 12 ZODIAC SIGNS)
	const signGuidance = getZodiacAdvice(reading.zodiac_sign);
	let section3 = `**၃။ လက်တွေ့ကျင့်သုံးရန် လမ်းညွှန်ချက်နှင့် အကြံပြုချက်**\n${signGuidance}\n\n`;

	if (isLoveTiming) {
		section3 +=
			'ချစ်သူရဖို့ အချိန်ကာလကို လောလောလောလော မတွက်ချက်ဘဲ၊ နေ့စဉ်ဘဝတွင် မိမိကိုယ်ကို ပျော်ရွှင်အောင် နေထိုင်ပါ။ ကိုယ်တိုင် ပြည့်စုံပျော်ရွှင်နေသူထံသို့ အချစ်စစ်သည် အလိုအလျောက် ဆွဲဆောင်ရောက်ရှိလာစမြဲ ဖြစ်ပါသည်။';
	} else if (isLoveGeneral) {
		section3 +=
			'မိမိ၏ စိတ်ခံစားချက်များကို အလိုလိုသိစိတ်ဖြင့် ဆင်ခြင်ပြီး လက်တွဲဖော်အပေါ် စာနာနားလည်မှု၊ ပွင့်လင်းရိုးသားမှုတို့ဖြင့် ဆက်ဆံပါ။ စစ်မှန်သော ချစ်ခြင်းမေတ္တာသည် အပြန်အလှန် လေးစားမှုပေါ်တွင် တည်ဆောက်ထားပါသည်။';
	} else if (isEducation) {
		section3 +=
			'စာမေးပွဲဖြေဆိုချိန်တွင် မေးခွန်းများကို အလျင်စလို မဖြေဆိုမီ သေချာစွာ ဖတ်ရှုဆင်ခြင်ပါ။ စိတ်တည်ငြိမ်အေးဆေးမှုသည် အောင်မြင်ခြင်း၏ အဓိကသော့ချက်ဖြစ်ပြီး၊ ဇွဲလုံ့လ စိုက်ထုတ်မှုကို ဆက်လက်ထိန်းသိမ်းထားပါက စာမေးပွဲအောင်မြင်မှု ရလဒ်ကောင်းကို ပိုင်ဆိုင်နိုင်ပါလိမ့်မည်။';
	} else if (isCareer || isFinance) {
		section3 +=
			'လက်ရှိလုပ်ငန်းခွင်နှင့် ငွေကြေးကိစ္စရပ်များတွင် အစီအစဉ်တကျ ခြေလှမ်းမှန်မှန် လှမ်းပါ။ သင့်၏ ပင်ကိုအရည်အချင်းနှင့် စွမ်းဆောင်ရည်ကို ယုံကြည်စိတ်ချစွာ အသုံးချခြင်းဖြင့် အောင်မြင်မှုမှတ်တိုင်များကို အရောက်လှမ်းနိုင်ပါလိမ့်မည်။';
	} else if (isDecisionOrYesNo) {
		section3 +=
			'မည်သည့်လမ်းကြောင်းကို ရွေးချယ်သည်ဖြစ်စေ၊ နှလုံးသား၏ ခံစားချက်နှင့် ဦးနှောက်၏ ယုတ္တိကျသော သုံးသပ်ချက် နှစ်ခုစလုံးကို ဟန်ချက်ညီစေရန် အထူးအရေးကြီးပါသည်။ မိမိ၏ ရွေးချယ်မှုအပေါ် ယုံကြည်စိတ်ချစွာဖြင့် ရှေ့ဆက်ပါ။';
	} else {
		section3 +=
			'ဤဟောကိန်းသည် အနာဂတ်ကို ကန့်သတ်ဟောကိန်းထုတ်ခြင်း မဟုတ်ဘဲ မိမိကိုယ်ကို ဆင်ခြင်သုံးသပ်ရန်အတွက် သင်္ကေတသဘော လမ်းညွှန်ချက်တစ်ခုသာ ဖြစ်ပါသည်။ လက်ရှိကြုံတွေ့နေရသော အခြေအနေများနှင့် ဆက်စပ်ဆင်ခြင်၍ အကျိုးရှိစွာ အသုံးချပါ။';
	}

	return `${section1}\n\n---\n\n${section2}\n\n---\n\n${section3}`;
}

export function getZodiacAdvice(sign: string | undefined): string {
	const s = (sign || '').toLowerCase().trim();
	if (s.includes('aries') || s.includes('မိဿ')) {
		return 'မိဿရာသီဖွား (မီးဓာတ်) အနေဖြင့် သင်၏ ပင်ကိုရဲရင့်ပြတ်သားမှုနှင့် ရှေ့ဆောင်ဦးဆောင်လိုစိတ်ကို အပြုသဘောဆောင် အသုံးချပါ။ အလျင်စလို ဆုံးဖြတ်ခြင်းကို ရှောင်ရှားပြီး ရေရှည်မျှော်တွေးကာ အဆင့်ဆင့် လျှောက်လှမ်းပါ။';
	} else if (s.includes('taurus') || s.includes('ပြိဿ')) {
		return 'ပြိဿရာသီဖွား (မြေဓာတ်) အနေဖြင့် သင်၏ စိတ်ရှည်သည်းခံမှု၊ တည်ငြိမ်ခိုင်မာမှုနှင့် လက်တွေ့ကျသော အခြေခံများကို အားပြုပါ။ စိတ်လောကြီးခြင်းမရှိဘဲ ဖြည်းဖြည်းနှင့်မှန်မှန် ခိုင်မာစွာ တည်ဆောက်သွားပါ။';
	} else if (s.includes('gemini') || s.includes('မေထုန်')) {
		return 'မေထုန်ရာသီဖွား (လေဓာတ်) အနေဖြင့် သင်၏ ထက်မြက်သော ဉာဏ်ပညာ၊ စူးစမ်းရှာဖွေလိုစိတ်နှင့် ပွင့်လင်းစွာ ပြောဆိုဆက်ဆံနိုင်စွမ်းကို အသုံးချပါ။ စိတ်ဒွိဟဖြစ်မှုများကို ရှင်းလင်းပြတ်သားသော သတင်းအချက်အလက်များဖြင့် ဖြေရှင်းပါ။';
	} else if (s.includes('cancer') || s.includes('ကရကဋ်')) {
		return 'ကရကဋ်ရာသီဖွား (ရေဓာတ်) အနေဖြင့် သင်၏ နက်ရှိုင်းသော အလိုလိုသိစိတ်၊ နွေးထွေးသော စာနာနားလည်မှုနှင့် အတွင်းစိတ်ခွန်အားကို အပြည့်အဝ ယုံကြည်ပါ။ စိတ်ခံစားချက်များကို လုံခြုံစွာ ထိန်းသိမ်းပြီး အဆင်သင့်ဖြစ်ချိန်တွင် သဘာဝကျကျ ရှေ့ဆက်ပါ။';
	} else if (s.includes('leo') || s.includes('သိဟ်')) {
		return 'သိဟ်ရာသီဖွား (မီးဓာတ်) အနေဖြင့် သင်၏ မွန်မြတ်သော စေတနာ၊ နှလုံးသားခွန်အားနှင့် မိမိကိုယ်ကို ယုံကြည်မှုကို မဏ္ဍိုင်ပြုပါ။ မာနထက် နားလည်မှုကို ဦးစားပေးပြီး သင်၏ တောက်ပသော စွမ်းအင်ဖြင့် အောင်မြင်မှုကို အရယူပါ။';
	} else if (s.includes('virgo') || s.includes('ကန်')) {
		return 'ကန်ရာသီဖွား (မြေဓာတ်) အနေဖြင့် သင်၏ စေ့စပ်သေချာမှု၊ စနစ်တကျ ပြင်ဆင်နိုင်မှုနှင့် လက်တွေ့ကျကျ ဆန်းစစ်နိုင်စွမ်းကို အားပြုပါ။ အသေးစိတ်အချက်အလက်များကို အလေးထားသော်လည်း အရာရာ ပြီးပြည့်စုံလွန်းရမည်ဟူသော စိုးရိမ်စိတ်ကို လျှော့ချပါ။';
	} else if (s.includes('libra') || s.includes('တူ')) {
		return 'တူရာသီဖွား (လေဓာတ်) အနေဖြင့် သင်၏ မျှတစွာ ချိန်ဆနိုင်မှု၊ သဟဇာတဖြစ်လိုစိတ်နှင့် လိမ္မာပါးနပ်သော သံတမန်ဆက်ဆံရေးကို အသုံးချပါ။ လမ်းကြောင်းနှစ်ခုကြား ဝေခွဲမရဖြစ်မနေဘဲ မိမိ၏ အတွင်းစိတ်အမှန်တရားအတိုင်း သတ္တိရှိရှိ ရွေးချယ်ပါ။';
	} else if (s.includes('scorpio') || s.includes('ဗြိစ္ဆာ')) {
		return 'ဗြိစ္ဆာရာသီဖွား (ရေဓာတ်) အနေဖြင့် သင်၏ စူးရှထက်မြက်သော ထိုးထွင်းအမြင်၊ စိတ်ပိုင်းဖြတ်မှုနှင့် ဘဝကို အသွင်ပြောင်းလဲနိုင်သော စွမ်းအားကို ယုံကြည်ပါ။ အတိတ်ဟောင်းများကို လက်လွှတ်စွန့်လွှတ်ပြီး အသစ်တဖန် ပြန်လည်မွေးဖွားသည့်သဖွယ် အားသစ်မွေးပါ။';
	} else if (s.includes('sagittarius') || s.includes('ဓနု')) {
		return 'ဓနုရာသီဖွား (မီးဓာတ်) အနေဖြင့် သင်၏ အကောင်းမြင်စိတ်၊ အမြင်ကျယ်မှုနှင့် အမှန်တရားရှာဖွေလိုစိတ်ကို အားဖြည့်ပါ။ ပန်းတိုင်ကို ရှင်းလင်းစွာ မြင်ယောင်ပြီး စိတ်အားထက်သန်စွာဖြင့် ဇွဲမလျှော့ဘဲ ဆက်လက်လျှောက်လှမ်းပါ။';
	} else if (s.includes('capricorn') || s.includes('မကာရ')) {
		return 'မကာရရာသီဖွား (မြေဓာတ်) အနေဖြင့် သင်၏ စည်းကမ်းခိုင်မာမှု၊ မဆုတ်မနစ်သော ဇွဲလုံ့လနှင့် ရေရှည်ရည်မှန်းချက်ကြီးမားမှုကို အခြေပြုပါ။ အချိန်ယူတည်ဆောက်ရသောအရာများသည် ခိုင်ခံ့မြဲမြံစမြဲဖြစ်ကြောင်း သတိပြုကာ စိတ်ရှည်စွာ ရှေ့ဆက်ပါ။';
	} else if (s.includes('aquarius') || s.includes('ကုမ်')) {
		return 'ကုမ်ရာသီဖွား (လေဓာတ်) အနေဖြင့် သင်၏ ထူးခြားဆန်းသစ်သော အတွေးအခေါ်၊ လွတ်လပ်မှုနှင့် ရှေ့ပြေးအမြင်များကို လက်ကိုင်ထားပါ။ သမားရိုးကျ ဘောင်များမှ ခွဲထွက်ပြီး သင့်ကိုယ်ပိုင် နည်းလမ်းသစ်ဖြင့် ဖန်တီးတီထွင်ပါ။';
	} else if (s.includes('pisces') || s.includes('မိန်')) {
		return 'မိန်ရာသီဖွား (ရေဓာတ်) အနေဖြင့် သင်၏ နူးညံ့သိမ်မွေ့သော မေတ္တာ၊ အလိုလိုသိမြင်နိုင်သော စိတ်ဝိညာဉ်စွမ်းအားနှင့် အနုပညာဆန်သော စိတ်ကူးဉာဏ်ကို အသုံးချပါ။ စိတ်ကူးယဉ်မှုနှင့် လက်တွေ့ဘဝကို ဟန်ချက်ညီစေပြီး မိမိ၏ နှလုံးသားအသံကို နားထောင်ပါ။';
	}
	return 'သင်၏ ပင်ကိုစွမ်းအင်နှင့် ဆင်ခြင်တွေးခေါ်မှုများကို သဟဇာတဖြစ်အောင် ညှိယူပါ။ ဤဟောကိန်းသည် အနာဂတ်ကို ကန့်သတ်ဟောကိန်းထုတ်ခြင်း မဟုတ်ဘဲ မိမိကိုယ်ကို ဆင်ခြင်သုံးသပ်ရန်အတွက် သင်္ကေတသဘော လမ်းညွှန်ချက်တစ်ခုသာ ဖြစ်ပါသည်။ လက်ရှိကြုံတွေ့နေရသော အခြေအနေများနှင့် ဆက်စပ်ဆင်ခြင်၍ အကျိုးရှိစွာ အသုံးချပါ။';
}

export function formatAdviceText(
	adviceText: string | undefined | null,
	locale: SupportedLocale
): string {
	if (!adviceText) return '';
	if (locale !== 'my') return adviceText;

	const lower = adviceText.toLowerCase().trim();

	// Context Advice Translations
	if (
		lower.includes('focus on open communication and emotional honesty') ||
		lower.includes('open communication')
	) {
		return 'ပွင့်လင်းရိုးသားစွာ ဆက်သွယ်ပြောဆိုခြင်းနှင့် စိတ်ခံစားချက်များကို အပြန်အလှန် မျှဝေနားလည်ခြင်းအပေါ် အဓိကအာရုံစိုက်ပါ။ မိမိ၏ လိုလားချက်များနှင့် တစ်ဖက်သား၏ လိုအပ်ချက်များကို မျှတစွာ နားလည်သဘောပေါက်ရန် ကတ်များက အလေးပေး ညွှန်ပြနေပါသည်။';
	}
	if (lower.includes('consider both paths carefully') || lower.includes('both paths')) {
		return 'လမ်းကြောင်းနှစ်ခုလုံးကို သေချာစွာ ချိန်ဆစဉ်းစားပါ။ လမ်းကြောင်းတစ်ခုကို မရွေးချယ်မီ ယုတ္တိကျသော အချက်အလက်များနှင့် မိမိ၏ အလိုလိုသိစိတ် နှစ်ခုလုံးကို အသုံးပြု၍ သုံးသပ်ရန် ကတ်များက အကြံပြုထားပါသည်။';
	}
	if (lower.includes('trust your professional instincts') || lower.includes('staying grounded')) {
		return 'လက်တွေ့ကျသော ရပ်တည်ချက်ကို ထိန်းသိမ်းရင်း မိမိ၏ လုပ်ငန်းခွင်ဆိုင်ရာ ဗီဇဉာဏ်ကို ယုံကြည်ပါ။ မိမိ၏ အားသာချက်များကို အသုံးချပြီး နည်းလမ်းသစ်များကို လက်ခံကျင့်သုံးရန် ကတ်များက ညွှန်ပြနေပါသည်။';
	}
	if (lower.includes('honest self-assessment') || lower.includes('beneath the surface')) {
		return 'မိမိကိုယ်ကို ရိုးသားစွာ ပြန်လည်ဆန်းစစ်ရန် အချိန်ယူပါ။ မိမိ၏ စစ်မှန်သော ရည်မှန်းချက်များနှင့် ဆန္ဒများကို နားလည်နိုင်ရန် အတွင်းစိတ်သဘောကို လေ့လာဆင်ခြင်ရန် ကတ်များက တိုက်တွန်းထားပါသည်။';
	}
	if (
		lower.includes('nurture your connections through genuine presence') ||
		lower.includes('genuine presence')
	) {
		return 'စိတ်ရင်းမှန်ဖြင့် အတူရှိပေးခြင်းဖြင့် ဆက်ဆံရေးများကို ခိုင်မြဲစေပါ။ ကြီးကျယ်သော လုပ်ဆောင်မှုများထက် စစ်မှန်သော စေတနာထားရှိမှုက သံယောဇဉ်ကို ပိုမိုခိုင်မာစေကြောင်း ကတ်များက ဖော်ပြပါသည်။';
	}
	if (lower.includes('follow your creative impulses') || lower.includes('creative impulses')) {
		return 'အတွေးများလွန်မနေဘဲ မိမိ၏ ဖန်တီးမှုစိတ်ကူးများကို လက်တွေ့ဖော်ဆောင်ပါ။ စမ်းသပ်တီထွင်မှုများ ပြုလုပ်ရန်နှင့် ဖန်တီးမှုလုပ်ငန်းစဉ်ကို ယုံကြည်စိတ်ချရန် ကတ်များက လမ်းညွှန်ထားပါသည်။';
	}
	if (
		lower.includes('approach learning with both curiosity and discipline') ||
		lower.includes('curiosity and discipline')
	) {
		return 'စူးစမ်းလိုစိတ်နှင့် စည်းကမ်းရှိမှု နှစ်ရပ်လုံးဖြင့် ပညာရပ်များကို ဆည်းပူးပါ။ စိတ်ပါဝင်စားမှုနှင့်အတူ စဉ်ဆက်မပြတ် ဇွဲလုံ့လ စိုက်ထုတ်ခြင်းက အလေးနက်ဆုံး အောင်မြင်မှုကို ဖြစ်ထွန်းစေကြောင်း ကတ်များက အကြံပြုထားပါသည်။';
	}
	if (
		lower.includes('balance ambition with realistic assessment') ||
		lower.includes('balance ambition')
	) {
		return 'ရည်မှန်းချက်ကြီးမားမှုနှင့် လက်တွေ့ကျသော ချိန်ဆချက်တို့ကို မျှတအောင် ညှိယူပါ။ အစီအစဉ်များ ရေးဆွဲထားသော်လည်း မမျှော်လင့်ဘဲ ပေါ်ပေါက်လာမည့် အခွင့်အလမ်းများအတွက် ပြောင်းလွယ်ပြင်လွယ် ရှိနေရန် ကတ်များက အကြံပြုထားပါသည်။';
	}
	if (lower.includes('stay present and aware') || lower.includes('daily interactions')) {
		return 'လက်ရှိပစ္စုပ္ပန်တည့်တည့်တွင် စိတ်ကို စိုက်ကပ်ထားပြီး ပတ်ဝန်းကျင်မှ စွမ်းအင်များကို သတိပြုဆင်ခြင်ပါ။ နေ့စဉ်လူမှုဆက်ဆံရေးများတွင် မိမိ၏ အလိုလိုသိစိတ်ကို ယုံကြည်ပြီး အခြေအနေအရပ်ရပ်ကို မျှတစွာ လေ့လာပါ။';
	}

	// Theme-based Advice Translations
	if (lower.includes('take a concrete step today') || lower.includes('concrete step')) {
		return 'ယနေ့တွင် လက်တွေ့ကျသော ခြေလှမ်းတစ်ခုကို စတင်လှမ်းပါ။ သေးငယ်သော လုပ်ဆောင်မှုများသည်ပင် အရှိန်အဟုန်ကောင်းကို တည်ဆောက်ပေးပါသည်။';
	}
	if (
		lower.includes('natural pace') ||
		lower.includes('unnecessary friction') ||
		lower.includes('patience')
	) {
		return 'အရာရာကို သဘာဝအလျောက် အချိန်ယူဖြစ်ထွန်းစေပါ။ လောလောလောလော ပြုမူခြင်းသည် မလိုအပ်သော ပွတ်တိုက်မှုများကို ဖြစ်ပေါ်စေနိုင်ပါသည်။';
	}
	if (
		lower.includes('honest self-examination') ||
		lower.includes('journaling') ||
		lower.includes('quiet time')
	) {
		return 'မိမိကိုယ်ကို ရိုးသားစွာ ပြန်လည်သုံးသပ်ရန် တိတ်ဆိတ်အေးချမ်းသော အချိန်တစ်ခု သီးသန့်ထားရှိပါ။ မိမိအတွေးများကို သေချာစွာ ရှင်းလင်းဆင်ခြင်ပါ။';
	}
	if (lower.includes('rebalancing') || lower.includes('neglected')) {
		return 'သင့်ဘဝတွင် ပြန်လည်ညှိယူရန် လိုအပ်နေသော နေရာများကို ရှာဖွေပါ။ လျစ်လျူရှုထားမိသော အရာများကို အထူးဂရုစိုက်ပေးပါ။';
	}
	if (lower.includes('embrace transformation') || lower.includes('something is ending')) {
		return 'ဘဝ၏ အပြောင်းအလဲများကို ဝမ်းမြောက်စွာ ကြိုဆိုပါ။ အသစ်သောအရာများ ဝင်ရောက်လာနိုင်ရန်အတွက် အဟောင်းတစ်ခုသည် ပြီးဆုံးရစမြဲ ဖြစ်ပါသည်။';
	}
	if (lower.includes('trust in your abilities') || lower.includes('handle what comes')) {
		return 'မိမိ၏ စွမ်းဆောင်ရည်နှင့် အရည်အချင်းကို အပြည့်အဝ ယုံကြည်ပါ။ ကြုံတွေ့လာမည့် အခြေအနေတိုင်းကို ကောင်းမွန်စွာ ကိုင်တွယ်ဖြေရှင်းနိုင်ကြောင်း ကတ်များက အတည်ပြုဖော်ပြနေပါသည်။';
	}
	if (lower.includes('inner voice') || lower.includes('gut feelings')) {
		return 'သင့်အတွင်းစိတ်၏ အသံကို အထူးအာရုံစိုက်ပါ။ လောလောဆယ်တွင် သင့်၏ ပင်ကိုဗီဇသိစိတ်သည် အထူးပင် မှန်ကန်တိကျနေပါသည်။';
	}
	if (
		lower.includes('express yourself honestly') ||
		lower.includes('resolves many uncertainties')
	) {
		return 'မိမိခံစားချက်ကို ရိုးသားသော်လည်း ယဉ်ကျေးသိမ်မွေ့စွာ ထုတ်ဖော်ပြောဆိုပါ။ ရှင်းလင်းပြတ်သားစွာ ပြောဆိုဆက်ဆံခြင်းသည် မသေချာမရေရာမှု အများအပြားကို ပြေလည်စေပါသည်။';
	}
	if (lower.includes('play and experiment') || lower.includes('release perfectionism')) {
		return 'မိမိကိုယ်ကို ပေါ့ပါးစွာ စမ်းသပ်တီထွင်ခွင့်ပြုပါ။ အရာရာ အပြစ်ကင်းစင်လိုစိတ်ကို လျှော့ချလိုက်သောအခါ တီထွင်ဖန်တီးနိုင်စွမ်းသည် အထွန်းကားဆုံး ဖြစ်လာပါသည်။';
	}
	if (lower.includes('consistent routine') || lower.includes('structure supports')) {
		return 'စနစ်တကျ ညီညွတ်သော နေ့စဉ်လုပ်ရိုးလုပ်စဉ်တစ်ခုကို တည်ဆောက်ကျင့်သုံးပါ။ စည်းစနစ်ကျနမှုသည် သင့်ပန်းတိုင်များကို များစွာ အထောက်အကူပြုပါသည်။';
	}
	if (lower.includes('give and receive love') || lower.includes('vulnerability is strength')) {
		return 'မေတ္တာတရားကို ပေးဝေရန်နှင့် လက်ခံရယူရန် သင့်နှလုံးသားကို ဖွင့်လှစ်ထားပါ။ စိတ်ခံစားချက်ကို ရိုးသားစွာ ဖော်ထုတ်ခြင်းသည် အားနည်းချက်မဟုတ်ဘဲ ခွန်အားတစ်ခု ဖြစ်ပါသည်။';
	}
	if (lower.includes('maintain optimism') || lower.includes('positive potential')) {
		return 'အခက်အခဲများနှင့် ရင်ဆိုင်ရချိန်တွင်ပင် အကောင်းမြင်စိတ်ကို ဆက်လက်ထိန်းသိမ်းပါ။ အနာဂတ်တွင် ကောင်းမွန်သော အလားအလာများ ရှိနေကြောင်း ကတ်များက ညွှန်ပြနေပါသည်။';
	}
	if (lower.includes('no longer serves you') || lower.includes('letting go')) {
		return 'သင့်ဘဝအတွက် အကျိုးမပြုတော့သော အရာဟောင်းများကို လက်လွှတ်စွန့်လွှတ်လိုက်ပါ။ အသစ်သောအသွင်သို့ ကူးပြောင်းရန်အတွက် လက်လွှတ်တတ်ရန် လိုအပ်ပါသည်။';
	}
	if (lower.includes('larger than yourself') || lower.includes('spiritual practice')) {
		return 'မိမိထက် ကြီးမြတ်သော သဘာဝတရား သို့မဟုတ် စိတ်ဝိညာဉ်စွမ်းအင်နှင့် ချိတ်ဆက်ပါ။ စိတ်ပိုင်းဆိုင်ရာ လေ့ကျင့်မှုများသည် မိမိကိုယ်ကို ပိုမိုနက်ရှိုင်းစွာ နားလည်စေပါသည်။';
	}

	return adviceText;
}

export function formatResonanceNote(
	zodiac: string,
	element: string,
	theme: string,
	locale: SupportedLocale
): string {
	if (locale !== 'my') {
		return `Your ${zodiac} ${element} amplifies this card's ${theme} energy`;
	}
	const zMy = getZodiacTranslation(zodiac, 'my').name || zodiac;
	const eMy = formatElement(element, 'my') || element;
	const tMy = translateTheme(theme, 'my') || theme;
	return `သင်၏ ${zMy} (${eMy}) သည် ဤကတ်၏ ${tMy} စွမ်းအင်ကို ပိုမိုအားကောင်းစေပါသည်`;
}
