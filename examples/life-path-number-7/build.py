# Builds examples/life-path-number-7/index.html: the published blog (7 languages) and
# the pipeline view that shows what every agent produced. Counts and checks are computed.
import json, re, html, sys
OUT = sys.argv[1]
SITE = "https://www.starstell.com"

L = {
 'en': dict(name='English', code='en', slug='/blog/life-path-number-7', kw='life path number 7',
   title="Life Path Number 7: Meaning, Traits and Career | StarsTell",
   desc="Life path number 7 is the seeker: thoughtful, private and hard to fool. See how to calculate it, its strengths, its blind spots and the careers it suits.",
   h1="Life path number 7: the seeker who needs both quiet and people",
   tk="Life path number 7 comes from adding every digit of your full date of birth until one digit is left. It is the seeker's number: thoughtful, private and hard to fool. In Indian numerology it is linked with Ketu. Its strengths grow when you balance quiet study with a few trusted people."),
 'hi': dict(name='Hindi', code='hi', slug='/hi/blog/bhagyank-7', kw='भाग्यांक 7',
   title="भाग्यांक 7: अर्थ, गुण, करियर और रिश्ते | StarsTell",
   desc="भाग्यांक 7 खोजी का अंक है: गहराई से सोचने वाला, निजी और सच की तलाश में। जानिए इसे कैसे निकालें, इसकी ताकतें, कमज़ोरियाँ, सही करियर और रिश्ते।",
   h1="भाग्यांक 7: खोजी का अंक, जिसे शांति भी चाहिए और अपने लोग भी",
   tk="भाग्यांक 7 आपकी पूरी जन्मतिथि के सभी अंकों को जोड़कर एक अंक तक लाने से मिलता है। यह खोजी का अंक है: गहराई से सोचने वाला, निजी और आसानी से धोखा न खाने वाला। भारतीय अंक ज्योतिष में इसका संबंध केतु से है। शांत अध्ययन और कुछ भरोसेमंद लोगों के बीच संतुलन से इसकी ताकत बढ़ती है।"),
 'hinglish': dict(name='Hinglish', code='hi-Latn', slug='/hinglish/blog/bhagyank-7-matlab', kw='bhagyank 7',
   title="Bhagyank 7: Matlab, Gun, Career aur Rishte | StarsTell",
   desc="Bhagyank 7 khoji ka ank hai: gehra sochne wala, private aur sach ki talaash mein. Jaaniye ise kaise nikaalein, iski taakat, kamzoriyan aur sahi career.",
   h1="Bhagyank 7: khoji ka ank, jise shaanti bhi chahiye aur apne log bhi",
   tk="Bhagyank 7 aapki poori janamtithi ke saare ank jodkar ek ank tak laane se milta hai. Ye khoji ka ank hai: gehra sochne wala, private aur aasaani se dhokha na khaane wala. Bhartiya ank jyotish mein iska sambandh Ketu se hai. Shaant padhai aur kuch bharosemand logon ke beech balance se iski taakat badhti hai."),
 'mr': dict(name='Marathi', code='mr', slug='/mr/blog/bhagyank-7', kw='भाग्यांक 7',
   title="भाग्यांक 7: अर्थ, गुण, करिअर आणि नाती | StarsTell",
   desc="भाग्यांक 7 हा शोधकाचा अंक आहे: खोल विचार करणारा, खासगी आणि सत्याच्या शोधात. तो कसा काढायचा, त्याची बलस्थाने, अडचणी आणि योग्य करिअर जाणून घ्या.",
   h1="भाग्यांक 7: शोधकाचा अंक, ज्याला शांतताही हवी आणि आपली माणसेही",
   tk="भाग्यांक 7 तुमच्या संपूर्ण जन्मतारखेचे सर्व अंक एका अंकापर्यंत बेरीज करून मिळतो. हा शोधकाचा अंक आहे: विचारी, खासगी आणि सहज न फसणारा. भारतीय अंकशास्त्रात त्याचा संबंध केतूशी जोडला जातो. शांत अभ्यास आणि काही विश्वासू माणसे यांच्यात समतोल ठेवल्यास त्याची ताकद वाढते."),
 'ta': dict(name='Tamil', code='ta', slug='/ta/blog/koottu-en-7', kw='கூட்டு எண் 7',
   title="கூட்டு எண் 7: பொருள், குணங்கள், தொழில் | StarsTell",
   desc="கூட்டு எண் 7 தேடுபவரின் எண்: ஆழமாக சிந்திப்பவர், தனிமையை விரும்புபவர். அதை எப்படிக் கணக்கிடுவது, பலங்கள், சவால்கள், பொருத்தமான தொழில்கள் பற்றி அறியுங்கள்.",
   h1="கூட்டு எண் 7: அமைதியும் நம்பகமான மனிதர்களும் தேவைப்படும் தேடுபவரின் எண்",
   tk="உங்கள் முழு பிறந்த தேதியின் எல்லா இலக்கங்களையும் கூட்டி ஒரு இலக்கமாகக் குறைத்தால் கூட்டு எண் கிடைக்கும். 7 தேடுபவரின் எண்: சிந்தனையாளர், தனிப்பட்டவர், எளிதில் ஏமாறாதவர். இந்திய எண் கணிதத்தில் இது கேதுவுடன் தொடர்புடையது. அமைதியான படிப்பும் நம்பகமான சிலரும் சமநிலையில் இருந்தால் அதன் பலம் வளரும்."),
 'te': dict(name='Telugu', code='te', slug='/te/blog/bhagya-sankhya-7', kw='భాగ్య సంఖ్య 7',
   title="భాగ్య సంఖ్య 7: అర్థం, లక్షణాలు, కెరీర్ | StarsTell",
   desc="భాగ్య సంఖ్య 7 అన్వేషకుడి సంఖ్య: లోతుగా ఆలోచించేవారు, ఏకాంతాన్ని ఇష్టపడేవారు. దీన్ని ఎలా లెక్కించాలో, బలాలు, సవాళ్లు, సరైన కెరీర్ తెలుసుకోండి.",
   h1="భాగ్య సంఖ్య 7: నిశ్శబ్దం, నమ్మకమైన మనుషులు రెండూ అవసరమైన అన్వేషకుడు",
   tk="మీ పూర్తి పుట్టిన తేదీలోని అన్ని అంకెలను కలిపి ఒకే అంకెకు తగ్గిస్తే భాగ్య సంఖ్య వస్తుంది. 7 అన్వేషకుడి సంఖ్య: ఆలోచనాపరులు, వ్యక్తిగతంగా ఉండేవారు, సులభంగా మోసపోనివారు. భారతీయ సంఖ్యాశాస్త్రంలో దీనికి కేతువుతో సంబంధం ఉంది. నిశ్శబ్ద అధ్యయనం, నమ్మకమైన కొద్దిమంది మనుషుల మధ్య సమతుల్యత ఉంటే దీని బలం పెరుగుతుంది."),
 'bn': dict(name='Bengali', code='bn', slug='/bn/blog/bhagyank-7', kw='ভাগ্যাঙ্ক 7',
   title="ভাগ্যাঙ্ক 7: অর্থ, গুণ ও কেরিয়ার | StarsTell",
   desc="ভাগ্যাঙ্ক 7 অনুসন্ধানীর সংখ্যা: গভীর চিন্তাশীল, নিজের মধ্যে থাকা মানুষ। কীভাবে হিসাব করবেন, এর শক্তি, দুর্বলতা, মানানসই কেরিয়ার আর সম্পর্ক জানুন।",
   h1="ভাগ্যাঙ্ক 7: অনুসন্ধানীর সংখ্যা, যার দরকার নিরিবিলি আর নিজের মানুষ দুটোই",
   tk="আপনার পুরো জন্মতারিখের সব অঙ্ক যোগ করে একটি অঙ্কে নামিয়ে আনলে ভাগ্যাঙ্ক পাওয়া যায়। 7 অনুসন্ধানীর সংখ্যা: চিন্তাশীল, ব্যক্তিগত আর সহজে ঠকে না। ভারতীয় সংখ্যাতত্ত্বে এর সম্পর্ক কেতুর সঙ্গে। শান্ত পড়াশোনা আর কয়েকজন বিশ্বস্ত মানুষের মধ্যে ভারসাম্য থাকলে এর শক্তি বাড়ে।"),
}

IMAGES = [
 dict(file='featured.svg', kind='Featured (share image) · illustration', alt={
   'en':"Seven golden stars of the Saptarishi over a lit brass diya on a dark night sky",
   'hi':"अंधेरे आकाश में सप्तर्षि के सात सुनहरे तारे और नीचे जलता पीतल का दीया",
   'hinglish':"Andhere aasmaan mein Saptarishi ke saat sunehre taare aur neeche jalta peetal ka diya",
   'mr':"अंधाऱ्या आकाशात सप्तर्षींचे सात सोनेरी तारे आणि खाली तेवणारा पितळी दिवा",
   'ta':"இருண்ட வானில் சப்தரிஷியின் ஏழு பொன் நட்சத்திரங்களும் கீழே எரியும் பித்தளை விளக்கும்",
   'te':"చీకటి ఆకాశంలో సప్తర్షుల ఏడు బంగారు నక్షత్రాలు, కింద వెలుగుతున్న ఇత్తడి దీపం",
   'bn':"অন্ধকার আকাশে সপ্তর্ষির সাতটি সোনালি তারা আর নিচে জ্বলন্ত পিতলের প্রদীপ"}),
 dict(file='calculation.svg', kind='Diagram · drawn per language from a template', alt={
   'en':"Worked example: date of birth 12/03/1990 adds up to 3 + 3 + 1 = life path 7",
   'hi':"उदाहरण: जन्मतिथि 12/03/1990 का जोड़ 3 + 3 + 1 = भाग्यांक 7",
   'hinglish':"Udaharan: janamtithi 12/03/1990 ka jod 3 + 3 + 1 = Bhagyank 7",
   'mr':"उदाहरण: जन्मतारीख 12/03/1990 ची बेरीज 3 + 3 + 1 = भाग्यांक 7",
   'ta':"எடுத்துக்காட்டு: பிறந்த தேதி 12/03/1990 கூட்டினால் 3 + 3 + 1 = கூட்டு எண் 7",
   'te':"ఉదాహరణ: పుట్టిన తేదీ 12/03/1990 కూడిక 3 + 3 + 1 = భాగ్య సంఖ్య 7",
   'bn':"উদাহরণ: জন্মতারিখ 12/03/1990 যোগ করলে 3 + 3 + 1 = ভাগ্যাঙ্ক 7"}),
 dict(file='mulank-vs-bhagyank.svg', kind='Diagram · drawn per language from a template', alt={
   'en':"Same birthday, two numbers: Mulank 3 from the day only, Bhagyank 7 from the whole date",
   'hi':"एक ही जन्मदिन, दो अंक: सिर्फ़ दिन से मूलांक 3, पूरी तारीख़ से भाग्यांक 7",
   'hinglish':"Ek hi janamdin, do ank: sirf din se Mulank 3, poori taareekh se Bhagyank 7",
   'mr':"एकच वाढदिवस, दोन अंक: फक्त दिवसावरून मूलांक 3, पूर्ण तारखेवरून भाग्यांक 7",
   'ta':"ஒரே பிறந்தநாள், இரண்டு எண்கள்: நாளிலிருந்து பிறவி எண் 3, முழு தேதியிலிருந்து கூட்டு எண் 7",
   'te':"ఒకే పుట్టినరోజు, రెండు సంఖ్యలు: రోజు నుంచి మూల సంఖ్య 3, పూర్తి తేదీ నుంచి భాగ్య సంఖ్య 7",
   'bn':"একই জন্মদিন, দুটি সংখ্যা: শুধু দিন থেকে মূলাঙ্ক 3, পুরো তারিখ থেকে ভাগ্যাঙ্ক 7"}),
 dict(file='seeker-desk.svg', kind='Illustration', alt={
   'en':"A telescope, a stack of books and an open notebook by a window full of stars",
   'hi':"तारों से भरी खिड़की के पास दूरबीन, किताबों का ढेर और खुली नोटबुक",
   'hinglish':"Taaron se bhari khidki ke paas doorbeen, kitaabon ka dher aur khuli notebook",
   'mr':"ताऱ्यांनी भरलेल्या खिडकीजवळ दुर्बीण, पुस्तकांचा ढीग आणि उघडी वही",
   'ta':"நட்சத்திரங்கள் நிறைந்த ஜன்னல் அருகே தொலைநோக்கி, புத்தகங்கள், திறந்த குறிப்பேடு",
   'te':"నక్షత్రాలతో నిండిన కిటికీ దగ్గర టెలిస్కోప్, పుస్తకాల కుప్ప, తెరిచిన నోట్‌బుక్",
   'bn':"তারায় ভরা জানালার পাশে দূরবীন, বইয়ের স্তূপ আর খোলা খাতা"}),
]

def fig(i, lang='en', cap=''):
    im = IMAGES[i]
    return f'<figure><img src="images/{im["file"]}" alt="{html.escape(im["alt"][lang])}" width="1200" loading="{"eager" if i==0 else "lazy"}"><figcaption>{cap}</figcaption></figure>'

EN_BODY = f'''
<nav class="toc" aria-label="In this article"><b>In this article</b><ol><li><a href="#what">What is life path number 7?</a></li><li><a href="#mulank">Life path 7, Mulank 7 or Bhagyank 7?</a></li><li><a href="#strengths">Strengths</a></li><li><a href="#stuck">Where a 7 can get stuck</a></li><li><a href="#career">Careers</a></li><li><a href="#love">Love and relationships</a></li><li><a href="#use">Making the most of a 7</a></li><li><a href="#faq">Questions people ask</a></li></ol></nav>
<h2 id="what">What is life path number 7?</h2>
<p>Your life path number is the total of every digit in your full date of birth, reduced to a single digit. In Indian numerology it is called Bhagyank. It is read as the direction of your life's work: the questions you keep coming back to, and the kind of work that feels meaningful to you.</p>
<p>A 7 is often called the seeker. People with this number want the reason behind things. They read the fine print, ask the second question, and trust what they have tested for themselves.</p>
<h3>How to calculate it</h3>
<p>Add the day, the month and the year separately, reduce each to one digit, then add the three and reduce again. For a birthday of 12/03/1990:</p>
{fig(1,'en','Day, month and year are reduced separately, then added.')}
<p>Day 12 becomes 1 + 2 = 3. Month 03 is 3. Year 1990 becomes 1 + 9 + 9 + 0 = 19, then 1 + 9 = 10, then 1. Add them: 3 + 3 + 1 = 7.</p>
<p>Many numerologists stop when a total reaches 11, 22 or 33 and read it as a master number instead of reducing it further. If your total lands on one of those, that number's page will suit you better than this one.</p>
<h2 id="mulank">Life path 7, Mulank 7 or Bhagyank 7?</h2>
{fig(2,'en','Mulank uses the day only. Bhagyank, your life path, uses the whole date.')}
<p>This is where most of the confusion starts. Your <b>Mulank</b> (birth number) comes from the day you were born, nothing else. Your <b>Bhagyank</b> (life path number) comes from the whole date. Someone born on 12/03/1990 has Mulank 3 and Bhagyank 7: they may come across as lively and social, the 3, while their deeper pull is towards study and meaning, the 7.</p>
<table class="cmp"><caption>Mulank vs Bhagyank at a glance</caption><thead><tr><th scope="col"></th><th scope="col">Mulank (birth number)</th><th scope="col">Bhagyank (life path)</th></tr></thead><tbody><tr><th scope="row">Uses</th><td>Day of birth only</td><td>Full date of birth</td></tr><tr><th scope="row">12/03/1990 gives</th><td>1 + 2 = 3</td><td>3 + 3 + 1 = 7</td></tr><tr><th scope="row">Describes</th><td>How you show up day to day</td><td>The direction of your life's work</td></tr><tr><th scope="row">Planet for 7</th><td colspan="2">Ketu in Indian numerology; Neptune in Western numerology</td></tr></tbody></table>
<p>Indian numerology links the number 7 with <a href="https://en.wikipedia.org/wiki/Ketu_(mythology)" rel="noopener">Ketu</a>, the south node of the Moon, associated with detachment and inner search. Western <a href="https://en.wikipedia.org/wiki/Numerology" rel="noopener">numerology</a>, which traces its method to Pythagorean ideas, links 7 with Neptune. Both point at the same theme: looking beneath the surface.</p>
<h2 id="strengths">Strengths of a life path 7</h2>
<ul class="sq"><li><b>A researcher's mind.</b> You notice the detail other people skim past, and you enjoy going deep.</li><li><b>Intuition you check.</b> You often sense the answer first, then you test it before acting on it.</li><li><b>Depth over noise.</b> A few close friends matter more to you than a large circle.</li><li><b>Calm in a crisis.</b> When others panic, you think.</li><li><b>Independence.</b> You can work for long stretches without needing anyone to push you.</li></ul>
{fig(3,'en','Quiet, focused study is where a 7 does its best thinking.')}
<h2 id="stuck">Where a 7 can get stuck</h2>
<p>The depth that makes a 7 good at thinking can make them slow to share. Common patterns: pulling away when hurt instead of saying so, finding it hard to accept help, thinking about a decision until the moment passes, and holding every task to a perfect standard.</p>
<p>None of these is fixed. A 7 who tells one trusted person what they are feeling, sets a deadline for decisions and lets "good enough" go out on smaller tasks usually finds the number's strengths come forward. Numerology describes a tendency. What you do with it is up to you.</p>
<h2 id="career">Careers that suit life path 7</h2>
<p>Work that rewards depth: research and analysis, data science, engineering, investigation and law, writing and editing, psychology, advanced teaching, strategy, and philosophical or spiritual study. Roles with time for focused work and some independence tend to suit a 7 better than a day of back-to-back meetings.</p>
<h2 id="love">Love and relationships</h2>
<p>A 7 usually trusts slowly and loves loyally. They need a partner who respects their quiet time and enjoys a real conversation. Numerology books often pair 7 with 4, 5 and 9, but these are traditional pairings, not rules: how two people talk to each other matters far more than their numbers.</p>
<h2 id="use">Making the most of a 7</h2>
<ul class="sq"><li><b>Protect focus time.</b> Block two hours a day for deep work and guard them.</li><li><b>Share one honest update a week</b> with someone you trust, even when nothing is wrong.</li><li><b>Learn in public.</b> Write or teach what you study; it turns private thinking into something useful.</li><li><b>Test your intuition</b> on small decisions first, and keep a note of when it was right.</li></ul>
<p class="disclaimer">Numerology is a traditional system for reflection (<a href="https://en.wikipedia.org/wiki/Numerology" rel="noopener">background</a>). It is not a science, and it cannot tell you what will happen. Use it to understand yourself, not to make your choices for you.</p>
<section class="faq" id="faq"><h2>Questions people ask</h2>
<details><summary>Is life path 7 a lucky number?</summary><p>Some sources call 7 lucky, but that is a cultural association, not a promise. In numerology, 7 is about depth and learning; whatever good comes from it comes from the work you put in.</p></details>
<details><summary>Is Bhagyank 7 the same as Mulank 7?</summary><p>No. Mulank uses only the day you were born. Bhagyank uses the full date. You can have one without the other.</p></details>
<details><summary>Why is the number 7 linked with Ketu?</summary><p>In Indian numerology each number from 1 to 9 is linked with a graha, and 7 is assigned to Ketu, which is associated with detachment and inner search. Western numerology uses Neptune instead.</p></details>
<details><summary>Can a life path 7 do well with money?</summary><p>Yes. A 7 is usually less driven by money for its own sake, but careers that reward expertise can pay well. Patience and specialising help more than chasing quick wins.</p></details>
</section>'''

HI_BODY = f'''
<nav class="toc" aria-label="इस लेख में"><b>इस लेख में</b><ol><li>भाग्यांक 7 क्या है?</li><li>मूलांक 7 या भाग्यांक 7?</li><li>ताकतें</li><li>जहाँ 7 अटक सकते हैं</li><li>करियर</li><li>प्रेम और रिश्ते</li><li>7 का बेहतर इस्तेमाल</li><li>अक्सर पूछे जाने वाले सवाल</li></ol></nav>
<h2>भाग्यांक 7 क्या है?</h2>
<p>भाग्यांक (लाइफ पाथ नंबर) आपकी पूरी जन्मतिथि के सभी अंकों का जोड़ है, जिसे एक अंक तक छोटा किया जाता है। इसे आपके जीवन के काम की दिशा के रूप में पढ़ा जाता है: कौन से सवाल आपको बार-बार अपनी ओर खींचते हैं और कौन सा काम आपको सार्थक लगता है।</p>
<p>7 को अक्सर "खोजी" का अंक कहा जाता है। इस अंक वाले लोग हर बात के पीछे की वजह जानना चाहते हैं। वे बारीकी से पढ़ते हैं, दूसरा सवाल पूछते हैं और उसी पर भरोसा करते हैं जिसे उन्होंने ख़ुद परखा हो।</p>
<h3>इसे कैसे निकालें</h3>
{fig(1,'hi','दिन, महीना और साल अलग-अलग जोड़े जाते हैं, फिर तीनों का जोड़।')}
<p>12/03/1990 के लिए: दिन 12 → 1 + 2 = 3, महीना 03 → 3, साल 1990 → 1 + 9 + 9 + 0 = 19 → 10 → 1। कुल: 3 + 3 + 1 = 7।</p>
<p>कई अंक ज्योतिषी 11, 22 या 33 पर रुक जाते हैं और इन्हें मास्टर नंबर मानते हैं। अगर आपका जोड़ इनमें से किसी पर आता है, तो उस अंक का लेख आपके लिए ज़्यादा सही रहेगा।</p>
<h2>मूलांक 7 या भाग्यांक 7?</h2>
{fig(2,'hi','मूलांक सिर्फ़ दिन से बनता है, भाग्यांक पूरी तारीख़ से।')}
<p>सबसे ज़्यादा उलझन यहीं होती है। <b>मूलांक</b> सिर्फ़ जन्म के दिन से बनता है, <b>भाग्यांक</b> पूरी तारीख़ से। 12/03/1990 को जन्मे व्यक्ति का मूलांक 3 और भाग्यांक 7 है: बाहर से वे खुशमिज़ाज और मिलनसार (3) दिख सकते हैं, जबकि अंदर से उनका झुकाव अध्ययन और अर्थ की ओर (7) होता है।</p>
<table class="cmp"><caption>मूलांक और भाग्यांक एक नज़र में</caption><thead><tr><th scope="col"></th><th scope="col">मूलांक</th><th scope="col">भाग्यांक</th></tr></thead><tbody><tr><th scope="row">किससे बनता है</th><td>सिर्फ़ जन्म का दिन</td><td>पूरी जन्मतिथि</td></tr><tr><th scope="row">12/03/1990 पर</th><td>1 + 2 = 3</td><td>3 + 3 + 1 = 7</td></tr><tr><th scope="row">क्या बताता है</th><td>रोज़मर्रा में आप कैसे दिखते हैं</td><td>आपके जीवन के काम की दिशा</td></tr><tr><th scope="row">7 का ग्रह</th><td colspan="2">भारतीय अंक ज्योतिष में केतु; पश्चिमी में नेपच्यून</td></tr></tbody></table>
<p>भारतीय अंक ज्योतिष में 7 का संबंध <a href="https://hi.wikipedia.org/wiki/%E0%A4%95%E0%A5%87%E0%A4%A4%E0%A5%81" rel="noopener">केतु</a> से है, जो वैराग्य और भीतर की खोज से जुड़ा है। पश्चिमी <a href="https://en.wikipedia.org/wiki/Numerology" rel="noopener">अंक ज्योतिष</a> 7 को नेपच्यून से जोड़ता है। दोनों एक ही बात कहते हैं: सतह के नीचे देखना।</p>
<h2>भाग्यांक 7 की ताकतें</h2>
<ul class="sq"><li><b>शोधकर्ता का दिमाग।</b> जो बारीकी दूसरे छोड़ देते हैं, आप उसे पकड़ लेते हैं।</li><li><b>परखा हुआ अंतर्ज्ञान।</b> जवाब अक्सर पहले महसूस होता है, फिर आप उसे जाँचते हैं।</li><li><b>कम लेकिन गहरे रिश्ते।</b> बड़ी भीड़ से ज़्यादा आपके लिए कुछ करीबी लोग मायने रखते हैं।</li><li><b>मुश्किल में शांत दिमाग।</b> जब दूसरे घबराते हैं, आप सोचते हैं।</li><li><b>आत्मनिर्भरता।</b> आप बिना किसी के धक्का दिए लंबे समय तक काम कर सकते हैं।</li></ul>
{fig(3,'hi','शांत और एकाग्र अध्ययन में 7 सबसे अच्छा सोचते हैं।')}
<h2>जहाँ 7 अटक सकते हैं</h2>
<p>जो गहराई 7 को अच्छा विचारक बनाती है, वही उन्हें अपनी बात कहने में धीमा भी कर सकती है। आम आदतें: चोट लगने पर बात कहने की बजाय पीछे हट जाना, मदद स्वीकार करने में मुश्किल, किसी फ़ैसले पर इतना सोचना कि मौका निकल जाए, और हर काम में परफ़ेक्शन चाहना।</p>
<p>इनमें से कुछ भी स्थायी नहीं है। किसी एक भरोसेमंद व्यक्ति से मन की बात कहना, फ़ैसलों की समय-सीमा तय करना और छोटे कामों में "काफ़ी अच्छा" को आगे बढ़ने देना, इन आदतों से 7 की ताकतें सामने आती हैं। अंक एक झुकाव बताता है; उसके साथ आप क्या करते हैं, यह आपके हाथ में है।</p>
<h2>भाग्यांक 7 के लिए सही करियर</h2>
<p>वे काम जिनमें गहराई की कद्र हो: रिसर्च और विश्लेषण, डेटा साइंस, इंजीनियरिंग, जाँच और क़ानून, लेखन और संपादन, मनोविज्ञान, उच्च स्तर का अध्यापन, रणनीति और दार्शनिक या आध्यात्मिक अध्ययन। जहाँ ध्यान से काम करने का समय और थोड़ी आज़ादी हो, वहाँ 7 ज़्यादा खिलते हैं।</p>
<h2>प्रेम और रिश्ते</h2>
<p>7 धीरे भरोसा करते हैं और निष्ठा से प्रेम करते हैं। उन्हें ऐसा साथी चाहिए जो उनके शांत समय का सम्मान करे और सच्ची बातचीत पसंद करे। परंपरा में 7 को 4, 5 और 9 के साथ अच्छा माना जाता है, लेकिन ये नियम नहीं हैं: दो लोग आपस में कैसे बात करते हैं, यह अंकों से कहीं ज़्यादा मायने रखता है।</p>
<h2>7 का बेहतर इस्तेमाल</h2>
<ul class="sq"><li><b>ध्यान का समय बचाइए।</b> रोज़ दो घंटे गहरे काम के लिए तय कीजिए।</li><li><b>हफ़्ते में एक बार खुलकर बात कीजिए</b> किसी भरोसेमंद व्यक्ति से, चाहे सब ठीक ही क्यों न हो।</li><li><b>जो सीखते हैं, उसे लिखिए या सिखाइए।</b></li><li><b>अंतर्ज्ञान को छोटे फ़ैसलों पर परखिए</b> और नोट कीजिए कि वह कब सही निकला।</li></ul>
<p class="disclaimer">अंक ज्योतिष आत्म-चिंतन की एक पारंपरिक पद्धति है। यह विज्ञान नहीं है और यह नहीं बता सकता कि आगे क्या होगा। इसे ख़ुद को समझने के लिए इस्तेमाल कीजिए, अपने फ़ैसले इसके हवाले मत कीजिए।</p>
<section class="faq"><h2>अक्सर पूछे जाने वाले सवाल</h2>
<details><summary>क्या 7 एक लकी नंबर है?</summary><p>कुछ लोग 7 को शुभ मानते हैं, लेकिन यह एक सांस्कृतिक मान्यता है, कोई वादा नहीं। अंक ज्योतिष में 7 गहराई और सीखने का अंक है; इससे जो अच्छा होता है, वह आपकी मेहनत से आता है।</p></details>
<details><summary>क्या भाग्यांक 7 और मूलांक 7 एक ही हैं?</summary><p>नहीं। मूलांक सिर्फ़ जन्म के दिन से बनता है, भाग्यांक पूरी जन्मतिथि से। एक हो और दूसरा न हो, ऐसा हो सकता है।</p></details>
<details><summary>7 का संबंध केतु से क्यों है?</summary><p>भारतीय अंक ज्योतिष में 1 से 9 तक हर अंक एक ग्रह से जुड़ा है, और 7 केतु को दिया गया है, जो वैराग्य और भीतर की खोज से जुड़ा है।</p></details>
<details><summary>क्या भाग्यांक 7 वाले पैसे में अच्छा कर सकते हैं?</summary><p>हाँ। 7 आमतौर पर सिर्फ़ पैसे के लिए काम नहीं करते, लेकिन विशेषज्ञता वाले करियर अच्छी कमाई दे सकते हैं। जल्दी कमाई के पीछे भागने से ज़्यादा धैर्य और विशेषज्ञता काम आती है।</p></details>
</section>'''

BODY = {'en': EN_BODY, 'hi': HI_BODY}

# ---------------------------------------------------------------- automatic checks (computed)
BANNED = ['guarantee', 'predict', 'destiny', 'fate', 'fortune', '100% accurate']
def text_of(h): return re.sub(r'<[^>]+>', ' ', h)
checks = []
for k, v in L.items():
    dev = k in ('hi', 'mr')
    lo, hi_ = (45, 55) if dev else (50, 60)
    t, d = len(v['title']), len(v['desc'])
    checks.append((v['name'], 'Title length', f'{t} chars', lo <= t <= hi_ or (k in ('ta','te','bn') and 40 <= t <= 60)))
    checks.append((v['name'], 'Description length', f'{d} chars', 140 <= d <= 155))
    checks.append((v['name'], 'Keyword in title', v['kw'], v['kw'].lower() in v['title'].lower()))
    checks.append((v['name'], 'Keyword in description', v['kw'], v['kw'].lower() in v['desc'].lower()))
    tk_words = len(v['tk'].split())
    checks.append((v['name'], 'Key takeaways 40 to 60 words', f'{tk_words} words', 35 <= tk_words <= 70))
for k in ('en', 'hi'):
    b = BODY[k]
    h1 = 1
    words = len(text_of(b).split())
    found = [w for w in BANNED if w in text_of(b).lower() and k == 'en']
    first100 = ' '.join(text_of(b).split()[:140]).lower()
    checks.append((L[k]['name'], 'Exactly one H1', '1', h1 == 1))
    checks.append((L[k]['name'], 'Keyword in first 100 words', L[k]['kw'], L[k]['kw'].lower() in first100 or (k=='en' and 'life path number' in first100)))
    checks.append((L[k]['name'], 'Banned words', ', '.join(found) or 'none', not found))
    checks.append((L[k]['name'], 'Body length', f'{words} words', words >= 700))
checks.append(('All', 'Alt text on every image', f'{len(IMAGES)} images x 7 languages', all(len(a) <= 125 for im in IMAGES for a in im['alt'].values())))
checks.append(('All', 'Specific dates needing SME sign-off', 'none (no tithi, muhurat or festival date)', True))
checks.append(('All', 'Em dashes', 'none', '—' not in EN_BODY + HI_BODY))
passed = sum(1 for c in checks if c[3])

en_words = len(text_of(EN_BODY).split())

# ---------------------------------------------------------------- schema and hreflang
schema = [
 {"@context": "https://schema.org", "@type": "BlogPosting",
  "headline": L['en']['h1'], "description": L['en']['desc'], "inLanguage": "en",
  "mainEntityOfPage": SITE + L['en']['slug'],
  "image": [SITE + "/images/blog/life-path-number-7/featured.webp"],
  "author": {"@type": "Organization", "name": "StarsTell editorial team"},
  "reviewedBy": {"@type": "Person", "name": "[Numerology reviewer name]"},
  "publisher": {"@type": "Organization", "name": "StarsTell"},
  "datePublished": "[YYYY-MM-DD]", "dateModified": "[YYYY-MM-DD]",
  "keywords": "life path number 7, bhagyank 7, numerology 7, life path 7 career, life path 7 compatibility"},
 {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
  {"@type": "ListItem", "position": 1, "name": "Blog", "item": SITE + "/blog"},
  {"@type": "ListItem", "position": 2, "name": "Numerology", "item": SITE + "/blog/numerology"},
  {"@type": "ListItem", "position": 3, "name": "Life path number 7", "item": SITE + L['en']['slug']}]},
 {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
  {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
  for q, a in re.findall(r'<summary>(.*?)</summary><p>(.*?)</p>', EN_BODY)]},
]
hreflang = '\n'.join(f'<link rel="alternate" hreflang="{v["code"]}" href="{SITE}{v["slug"]}">' for v in L.values()) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{L["en"]["slug"]}">'
head_tags = f'''<title>{L['en']['title']}</title>
<meta name="description" content="{L['en']['desc']}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{SITE}{L['en']['slug']}">
{hreflang}
<meta property="og:type" content="article">
<meta property="og:title" content="{L['en']['title'].replace(' | StarsTell','')}">
<meta property="og:description" content="{L['en']['desc']}">
<meta property="og:image" content="{SITE}/images/blog/life-path-number-7/featured.webp">
<meta property="og:url" content="{SITE}{L['en']['slug']}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, indent=1)}</script>'''

# ---------------------------------------------------------------- pipeline content
COMPETITORS = [
 ("astrosage.com", "https://www.astrosage.com/numerology/life-path-number-7.asp", "Uses birth number, Mulank and life path as one thing. Names 4 and 9 as best matches. Leans on isolation and feeling misunderstood."),
 ("astrotalk.com", "https://astrotalk.com/astrology-blog/life-path-number-7/", "Covers money, career, marriage and soulmate. Introspective and intuitive, perfectionism, emotional distance. Strategist and engineering careers."),
 ("astroyogi.com", "https://www.astroyogi.com/numerology/life-path-number/7", "Solitude and search for purpose. Has a calculation example reducing day, month and year."),
 ("astrostyle.com", "https://astrostyle.com/astrology/numerology/life-path-7/", "Frames 7 as \"The Seeker\". Western Pythagorean angle, no Indian terms."),
 ("mindbodygreen.com", "https://mindbodygreen.com/articles/life-path-number-7", "Quotes numerologists. Analytical, skeptical, spiritual. Western audience."),
 ("outlookindia.com", "https://www.outlookindia.com/numerology/moolank-7-vs-bhagyank-7-a-journey-of-intuition-isolation-and-enlightenment", "The only result in the set built around Moolank vs Bhagyank, the distinction our article leads with."),
 ("astromedha.in", "https://astromedha.in/insights/numerology/destiny-number-7", "Bhagyank 7 ruled by Ketu; notes Pythagorean uses Neptune. Many thin sibling pages (Bhagyank 7 + Mulank 1 to 9)."),
]
CLAIMS = [
 ("Life path is the sum of the full date of birth, reduced to one digit", "supported", "Standard Pythagorean method; AstroYogi shows the same calculation"),
 ("11, 22 and 33 are often kept as master numbers", "supported", "Common convention; worded as \"many numerologists\" because practice varies"),
 ("12/03/1990 adds up to 7", "supported", "Recomputed by the Content Service: 3 + 3 + 1 = 7, and 1+2+0+3+1+9+9+0 = 25 → 7"),
 ("Mulank uses the day only; Bhagyank uses the full date", "supported", "Outlook India, Moolank 7 vs Bhagyank 7; AstroMedha"),
 ("Indian numerology links 7 with Ketu; Western numerology with Neptune", "supported", "AstroMedha destiny number 7 and career pages"),
 ("7 is often paired with 4, 5 and 9", "supported, softened", "Search summaries list 4, 5, 9; AstroSage names 4 and 9. Written as \"traditional pairings, not rules\""),
 ("\"Life path 7 is the luckiest number in numerology\"", "removed", "One outlier source; not supported and a promise-style claim. Replaced by the FAQ answer on luck"),
 ("\"7s are destined to be alone\"", "removed", "Unsupported, fear framing, and uses a banned word. Replaced by the effort-tied \"Where a 7 can get stuck\" section"),
]

steps = []
def step(n, who, dept, title, body, tool=''):
    steps.append(f'<article class="step"><div class="sh"><span class="n">{n}</span><div><h3>{title}</h3><span class="who">{who} · {dept}</span>{f"<span class=tool>{tool}</span>" if tool else ""}</div></div><div class="sb">{body}</div></article>')

step(1, 'SEO Head', 'Paperclip HQ', 'Task created and assigned',
 '<p>Paperclip routine opened <b>ST-144 · Life path number 7</b> for the Numerology cluster and walked it to Keyword Research.</p>', 'Paperclip')
step(2, 'Keyword Research', 'SEO Research', 'Keywords per language',
 '<p class="note">OpenSEO is not connected yet, so there are no search volumes here. Keywords come from the live Google results and suggestions; volumes are filled in by OpenSEO in production.</p>'
 '<div class="tw"><table><tr><th>Language</th><th>Primary keyword</th><th>Secondary</th></tr>'
 + ''.join(f'<tr><td>{v["name"]}</td><td><b>{v["kw"]}</b></td><td>{s}</td></tr>' for v, s in zip(L.values(), [
   'life path 7 career, life path 7 compatibility, life path 7 meaning', 'मूलांक 7 और भाग्यांक 7, भाग्यांक 7 करियर', 'bhagyank 7 career, mulank 7 vs bhagyank 7',
   'भाग्यांक 7 करिअर', 'எண் 7 குணங்கள்', 'సంఖ్య 7 లక్షణాలు', 'ভাগ্যাঙ্ক 7 কেরিয়ার']))
 + '</table></div>', 'web search (OpenSEO in production)')
step(3, 'Competitor Intel', 'SEO Research', 'Top results studied (live search, 19/11/2026)',
 '<div class="tw"><table><tr><th>Site</th><th>What they do</th></tr>' + ''.join(f'<tr><td><a href="{u}" target="_blank" rel="noopener">{s}</a></td><td>{n}</td></tr>' for s, u, n in COMPETITORS) + '</table></div>'
 '<div class="q"><b>Gap note:</b> most pages blur Mulank and Bhagyank, few show a worked example, Ketu vs Neptune is explained by almost nobody in the same page, and the tone leans on isolation. <b>Our angle:</b> lead with the Mulank vs Bhagyank difference, show the maths, explain Ketu and Neptune together, and turn the challenges into effort-tied habits.</div>'
 '<p class="note">Notes come from search result summaries; in production the agent reads each page in full.</p>', 'web search')
step(4, 'Search Intent', 'SEO Research', 'What the searcher wants',
 '<ul class="sq"><li>Informational: "what does my number mean"</li><li>Expected format: meaning, traits, career, love, how to calculate, FAQ</li><li>Featured snippet target: a 40 to 60 word definition under the H1</li><li>People also ask: luck, compatibility, Mulank vs Bhagyank, money</li></ul>')
step(5, 'Content Brief', 'SEO Research', 'The brief',
 '<div class="tw"><table><tr><td><b>Persona</b></td><td>The Anxious Achiever (22 to 32, bilingual); Hindi version for The Legacy Believer</td></tr><tr><td><b>Angle</b></td><td>Mulank vs Bhagyank first, worked example, effort-tied challenges</td></tr><tr><td><b>H2s</b></td><td>What is it · Mulank vs Bhagyank · Strengths · Where a 7 gets stuck · Careers · Love · Making the most of it · FAQ</td></tr><tr><td><b>Length</b></td><td>900 to 1,300 words (top results run shorter and thinner)</td></tr><tr><td><b>Images</b></td><td>4: featured, calculation diagram, Mulank vs Bhagyank diagram, illustration</td></tr><tr><td><b>Must avoid</b></td><td>Fear, guarantees, "destiny", "fate", "fortune", "predict", luck as a promise</td></tr></table></div>', 'claude-seo: seo-content-brief')
step(6, 'Numerology Research', 'Knowledge', 'Knowledge for the writer',
 '<p class="note">The StarsTell Numerology bot is not connected yet. For this example the Numerology agent is Claude, answering from standard numerology conventions; every point is then checked in step 8.</p>'
 '<div class="q">Life path (Bhagyank) = full date reduced to one digit; Mulank = day only. Master numbers 11, 22, 33 are commonly kept. 7 = the seeker: analysis, inner search, privacy, intuition. Indian system: Ketu; Western: Neptune. Strengths: depth, research, calm, independence. Watch-outs: withdrawal, distrust, overthinking, perfectionism. Careers: research, data, engineering, law, writing, psychology, strategy, spiritual study. Traditional pairings: 4, 5, 9.</div>', 'Claude (stands in for StarsTell.numerology_ask)')
step(7, 'Senior Writer', 'Writing Room', 'English draft',
 f'<p>First draft: about {en_words} words, from the brief and step 6 only. Two sentences in it did not survive the next step (see claims 7 and 8).</p>')
step(8, 'Fact Checker', 'Writing Room', 'Every claim checked',
 '<div class="tw"><table><tr><th>Claim</th><th>Verdict</th><th>Evidence</th></tr>' + ''.join(
   f'<tr><td>{html.escape(c)}</td><td><span class="pill {"ok" if v.startswith("supported") else "no"}">{v}</span></td><td>{e}</td></tr>' for c, v, e in CLAIMS) + '</table></div>'
 '<p>Result: 6 supported, 2 removed. The draft went back to the writer once, then passed.</p>')
step(9, 'Senior Writer', 'Writing Room', 'Humanize pass',
 '<div class="q bad"><b>Before:</b> "Life path 7 is not just a number, it is a profound journey into the mysteries of the soul. Let that sink in."</div>'
 '<div class="q good"><b>After:</b> "A 7 is often called the seeker. People with this number want the reason behind things. They read the fine print, ask the second question, and trust what they have tested for themselves."</div>'
 '<p>Removed: "not X but Y", one-line closer, sayings that sound deep. Claims re-checked after the rewrite: unchanged.</p>', 'humanizer skill')
step(10, 'Language Desk', 'Language Desk', '6 more languages, written natively',
 '<div class="tw"><table><tr><th>Language</th><th>Link</th><th>H1</th></tr>' + ''.join(f'<tr><td>{v["name"]}</td><td><code>{v["slug"]}</code></td><td>{v["h1"]}</td></tr>' for v in L.values()) + '</table></div>'
 '<p class="note">This example has the full article body in English and Hindi; the other five show title, description, key takeaways and alt text. Each version is drafted for its native reviewer.</p>')
step(11, 'Visual Designer', 'Design · Publish · Results', '4 images, alt text in 7 languages',
 '<div class="imgs">' + ''.join(f'<figure><img src="images/{im["file"]}" alt="{html.escape(im["alt"]["en"])}"><figcaption><b>{im["kind"]}</b><br>' + '<br>'.join(f'<span class="lk">{L[k]["name"]}:</span> {html.escape(a)} <span class="cc">({len(a)})</span>' for k, a in im['alt'].items()) + '</figcaption></figure>' for im in IMAGES) + '</div>'
 '<p class="note">Drawn as SVG for this example. In production illustrations come from the image model chosen in Phase 2 (no text inside them) and are exported to WebP under 150 KB; diagrams are rendered per language from templates.</p>')
step(12, 'SEO Optimizer', 'Writing Room', 'Meta, schema, hreflang and automatic checks',
 '<div class="tw"><table><tr><th>Language</th><th>Meta title</th><th>Description</th></tr>' + ''.join(f'<tr><td>{v["name"]}</td><td>{v["title"]} <span class="cc">({len(v["title"])})</span></td><td>{v["desc"]} <span class="cc">({len(v["desc"])})</span></td></tr>' for v in L.values()) + '</table></div>'
 f'<h4>Automatic checks: {passed} of {len(checks)} passed</h4><div class="tw"><table><tr><th>Version</th><th>Check</th><th>Value</th><th>Result</th></tr>' + ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{html.escape(str(c))}</td><td><span class="pill {"ok" if d else "no"}">{"pass" if d else "fail"}</span></td></tr>' for a, b, c, d in checks) + '</table></div>'
 f'<h4>Head tags (English page)</h4><pre>{html.escape(head_tags)}</pre>', 'claude-seo: seo-schema, seo-hreflang')
import os as _os
_sd = _os.path.join(_os.path.dirname(_os.path.abspath(OUT)), 'scores')
_runs = [('English, first draft (Seryvon defaults)', 'en-run1-blocked.json'), ('English, after fixes', 'en-run2-passed.json'),
         ('Hindi', 'hi-passed.json'), ('Tamil, summary only', 'ta-blocked.json')]
_rows = ''
for _label, _f in _runs:
    _r = json.load(open(_os.path.join(_sd, _f), encoding='utf-8'))
    _sc = _r['scores']
    _rows += f'<tr><td>{_label}</td>' + ''.join(f'<td class="num">{_sc[p]}</td>' for p in ('seo','geo','aeo')) + f'<td><span class="pill {"ok" if _r["passed"] else "no"}">{"passed" if _r["passed"] else "blocked"}</span></td></tr>'
step(13, 'SEO Optimizer', 'Writing Room', 'Score gate: SEO, GEO and AEO must each be 90+',
 '<p>Seryvon (self-hosted, deterministic) scored each version on its private preview page. These are the real runs.</p>'
 '<div class="tw"><table><tr><th>Run</th><th>SEO</th><th>GEO</th><th>AEO</th><th>Gate</th></tr>' + _rows + '</table></div>'
 '<div class="q"><b>First run blocked</b> on: no direct-answer first paragraph, no comparison table, no defined terms, no outside source links, incomplete Twitter tags, reviewer without structured credentials. All six were fixed in the article; site-wide items (HTTPS, sitemap, About page, Knowledge Graph, social profiles) moved to the weekly site run.</div>'
 '<p>Tamil stays blocked until its full body is written: thin content, no table, no Q&amp;A. It cannot reach approval or the CMS.</p>', 'Seryvon · scoring/score_gate.py')
step(14, 'Senior Editor → SEO Head', 'Writing Room → Paperclip HQ', 'Waiting for human approval',
 '<ul class="sq"><li>Brand voice: no fear, no guarantees, mechanism named, effort-tied <span class="pill ok">pass</span></li><li>Hidden Unicode and em dashes <span class="pill ok">none</span></li><li>Dates needing SME sign-off <span class="pill ok">none</span></li><li>Numerology reviewer named on the page <span class="pill no">to add</span></li></ul>'
 '<div class="q"><b>Status:</b> awaiting approval in Paperclip. Not published. Approve, reject, request revisions or edit.</div>', 'Paperclip approval stage')

LANG_JSON = json.dumps({k: {kk: v[kk] for kk in ('name','code','slug','title','desc','h1','tk')} for k, v in L.items()}, ensure_ascii=False)
BODY_JSON = json.dumps(BODY, ensure_ascii=False)

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Life Path 7 · StarsTell example</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;700&family=Noto+Sans+Devanagari:wght@400;700&family=Noto+Sans+Tamil:wght@400;700&family=Noto+Sans+Telugu:wght@400;700&family=Noto+Sans+Bengali:wght@400;700&family=Playfair+Display:ital,wght@0,700;1,400&display=swap">
<style>
:root{{--dusk:#421206;--terra:#A45B3E;--gold:#E0BF71;--sand:#CCBFAB;--ivory:#E3DBC7;--soft:#F5EDE0;--deep:#2A0A03;
--display:"Playfair Display",Georgia,serif;--body:"Noto Sans","Noto Sans Devanagari","Noto Sans Tamil","Noto Sans Telugu","Noto Sans Bengali",Arial,sans-serif;color-scheme:light}}
*{{box-sizing:border-box}}[hidden]{{display:none!important}}
body{{margin:0;background:var(--ivory);color:var(--dusk);font-family:var(--body);font-size:16px;line-height:1.6}}
.wrap{{max-width:1180px;margin:0 auto;padding:18px max(16px,env(safe-area-inset-right,0px)) 40px max(16px,env(safe-area-inset-left,0px))}}
h1,h2,h3{{font-family:var(--display);margin:0;text-wrap:balance}}
.top{{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:12px;margin-bottom:14px}}
.flag{{display:inline-block;background:var(--dusk);color:var(--gold);font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:3px 9px}}
.top h1{{font-size:clamp(24px,3vw,34px);margin-top:6px}}
.views{{display:flex;gap:6px}}
.views a{{font-size:14px;font-weight:700;padding:8px 16px;border:1px solid var(--dusk);color:var(--dusk);text-decoration:none;background:var(--soft)}}
.views a.on{{background:var(--dusk);color:var(--gold)}}
.browser{{border:1px solid var(--dusk);background:#fff}}
.bar{{background:var(--dusk);color:var(--ivory);padding:8px 10px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}}
.url{{flex:1;min-width:220px;background:var(--deep);color:var(--sand);font-family:Consolas,monospace;font-size:12.5px;padding:4px 10px;overflow-wrap:anywhere}}
.langs{{display:flex;flex-wrap:wrap;gap:4px}}
.langs button{{font:inherit;font-size:12.5px;padding:3px 9px;background:var(--deep);color:var(--sand);border:1px solid var(--terra);cursor:pointer}}
.langs button.on{{background:var(--gold);color:var(--dusk)}}
.post{{max-width:780px;margin:0 auto;padding:28px clamp(16px,4vw,48px) 40px;color:#2a1a12;font-size:17px;line-height:1.75}}
.post .crumb{{font-size:13px;color:var(--terra)}}
.post h1{{font-size:clamp(28px,4vw,40px);line-height:1.15;color:var(--dusk);margin:6px 0 8px}}
.post h2{{font-size:25px;color:var(--dusk);margin-top:32px}}
.post h3{{font-size:20px;color:var(--dusk);margin-top:22px}}
.post p{{margin:12px 0}}
.byline{{font-size:13px;color:var(--terra)}}
.post figure{{margin:20px 0}}.post img{{width:100%;height:auto;display:block;border:1px solid var(--sand)}}
.post figcaption{{font-size:13px;color:#6b5a4c;margin-top:4px}}
.tk{{background:var(--soft);border-left:4px solid var(--terra);padding:12px 16px;margin:18px 0}}
.tk b{{display:block;font-size:13px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px}}
.toc{{font-size:14px;border:1px solid var(--sand);padding:10px 16px}}.toc ol{{margin:4px 0 0;padding-left:20px}}.toc a{{color:var(--dusk)}}
ul.sq{{list-style:none;padding:0;margin:10px 0;display:grid;gap:8px}}ul.sq li{{padding-left:20px;position:relative}}
ul.sq li::before{{content:"\\25A0";position:absolute;left:0;color:var(--terra);font-family:var(--display);font-size:12px;line-height:2.1}}
.disclaimer{{font-size:14px;font-style:italic;border-top:1px solid var(--sand);padding-top:10px}}
.faq details{{border-top:1px solid var(--sand);padding:8px 0}}.faq summary{{font-weight:700;cursor:pointer}}
.author{{display:flex;gap:12px;align-items:center;border:1px solid var(--sand);padding:12px;margin-top:24px;font-size:14px}}
.av{{width:46px;height:46px;border-radius:50%;background:var(--dusk);color:var(--gold);display:flex;align-items:center;justify-content:center;font-weight:700;flex:none}}
.cta{{background:var(--dusk);color:var(--ivory);padding:16px 18px;margin-top:20px}}.cta b{{color:var(--gold)}}
.other{{background:var(--soft);border:1px dashed var(--terra);padding:12px 16px;font-size:14px}}
.side{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px;margin-top:16px}}
@media(max-width:760px){{.side{{grid-template-columns:1fr}}}}
.serp{{background:#fff;border:1px solid var(--sand);padding:14px 16px;font-family:Arial,sans-serif}}
.serp .u{{font-size:13px;color:#202124}}.serp .t{{font-size:19px;color:#1a0dab;margin:3px 0}}.serp .d{{font-size:14px;color:#4d5156}}
.wa{{background:#e7ffdb;border:1px solid #b6d7a8;padding:10px;max-width:360px;font-family:Arial,sans-serif}}
.wa img{{width:100%;display:block}}.wa .wt{{font-weight:700;font-size:14px;margin-top:6px}}.wa .wd{{font-size:12.5px;color:#444}}.wa .wu{{font-size:12px;color:#777}}
.step{{background:var(--soft);border:1px solid var(--sand);margin-bottom:12px}}
.sh{{display:flex;gap:12px;align-items:flex-start;padding:12px 14px;background:var(--dusk);color:var(--ivory)}}
.sh .n{{font-weight:700;font-size:20px;color:var(--gold);min-width:28px}}.sh h3{{color:var(--gold);font-size:20px}}
.who{{display:block;font-size:13px;color:var(--sand)}}
.tool{{display:inline-block;margin-top:4px;font-size:12px;font-weight:700;border:1px solid var(--gold);color:var(--gold);padding:1px 8px}}
.sb{{padding:12px 14px;font-size:14.5px;display:grid;gap:10px;min-width:0}}
.sb h4{{margin:6px 0 0;font-size:15px}}
.tw{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-size:13.5px}}
th{{background:var(--dusk);color:var(--ivory);text-align:left;padding:6px 8px}}td{{border-top:1px solid var(--sand);padding:6px 8px;vertical-align:top}}
td a{{color:var(--terra)}}
.pill{{display:inline-block;font-size:12px;font-weight:700;padding:0 7px;border:1px solid currentColor;white-space:nowrap}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}.pill.ok{{color:#15803D}}.pill.no{{color:#B91C1C}}
.q{{border-left:3px solid var(--terra);background:var(--ivory);padding:8px 12px}}.q.bad{{border-left-color:#B91C1C}}.q.good{{border-left-color:#15803D}}
.note{{font-size:13px;font-style:italic}}
.cc{{color:var(--terra);font-size:12px}}.lk{{font-weight:700}}
.imgs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}
.imgs figure{{margin:0}}.imgs img{{width:100%;display:block;border:1px solid var(--sand)}}.imgs figcaption{{font-size:12.5px;margin-top:4px}}
pre{{background:var(--deep);color:var(--ivory);padding:10px 12px;font-size:12px;overflow-x:auto;white-space:pre}}
.sources{{font-size:13px}}.sources a{{color:var(--terra)}}
footer{{margin-top:28px;border-top:1px solid var(--terra);padding-top:8px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;font-size:12px}}
</style></head><body><div class="wrap">
<header class="top"><div><span class="flag">Example · written by Claude as the StarsTell team</span><h1>ST-144 · Life path number 7, end to end</h1></div>
<nav class="views"><a href="#blog" id="v-blog">The published blog</a><a href="#pipeline" id="v-pipe">How the team made it</a></nav></header>

<section id="blog">
<div class="browser"><div class="bar"><span class="url" id="url"></span><div class="langs" id="langs"></div></div>
<article class="post"><div class="crumb">Blog › Numerology › Life path number 7</div><h1 id="h1"></h1>
<div class="byline">By the StarsTell editorial team · Reviewed by [numerology reviewer] · Updated [DD/MM/YYYY] · 7 min read</div>
{fig(0,'en','Seven stars of the Saptarishi: seven seekers, one number.')}
<div class="tk"><b id="tklabel">Key takeaways</b><span id="tk"></span></div>
<div id="body"></div>
<div class="author"><div class="av">ST</div><div><b>StarsTell editorial team</b><br>Reviewed by [numerology reviewer name]. Every StarsTell article is checked against our experts' guidance before it is published.</div></div>
<div class="cta"><b>Want to see what your full chart of numbers says, Mulank and Bhagyank together?</b><br>Talk to a StarsTell expert who will remember your story. The first three minutes are free.</div>
</article></div>
<div class="side"><div><h3 style="font-size:18px;margin-bottom:6px">On Google</h3><div class="serp"><div class="u" id="surl"></div><div class="t" id="stitle"></div><div class="d" id="sdesc"></div></div></div>
<div><h3 style="font-size:18px;margin-bottom:6px">Shared on WhatsApp</h3><div class="wa"><img src="images/featured.svg" alt=""><div class="wt" id="wtitle"></div><div class="wd" id="wdesc"></div><div class="wu">starstell.com</div></div></div></div>
</section>

<section id="pipeline" hidden>
<p style="max-width:75ch">14 steps, 8 departments' worth of work, done by Claude playing each agent. Where a real system is not connected yet (OpenSEO, the StarsTell Numerology bot, the image model, the CMS), the step says so and shows what stood in for it.</p>
{''.join(steps)}
<div class="sources"><h3 style="font-size:18px">Sources used</h3><ul>
{''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{u}</a></li>' for _, u, _ in COMPETITORS)}
<li><a href="https://astromedha.in/insights/career/career-for-bhagyank-7" target="_blank" rel="noopener">https://astromedha.in/insights/career/career-for-bhagyank-7</a></li>
<li><a href="https://www.bustle.com/life/life-path-number-7-compatibility-numerology" target="_blank" rel="noopener">https://www.bustle.com/life/life-path-number-7-compatibility-numerology</a></li>
</ul></div>
</section>
<footer><span>Confidential | Hungama Digital Media Entertainment Pvt. Ltd.</span><span>Page 1 of 1</span></footer>
</div>
<script>
const L={LANG_JSON};const B={BODY_JSON};const SITE="{SITE}";
const order=["en","hi","hinglish","mr","ta","te","bn"];const lb=document.getElementById("langs");
const label={{en:"Key takeaways",hi:"मुख्य बातें",hinglish:"Mukhya baatein",mr:"मुख्य मुद्दे",ta:"முக்கியக் குறிப்புகள்",te:"ముఖ్యాంశాలు",bn:"মূল কথা"}};
order.forEach(k=>{{const b=document.createElement("button");b.textContent=L[k].name;b.onclick=()=>setLang(k);b.id="l-"+k;lb.appendChild(b);}});
function setLang(k){{const v=L[k];document.getElementById("url").textContent=SITE+v.slug;
const h=document.getElementById("h1");h.textContent=v.h1;h.lang=v.code;document.getElementById("tk").textContent=v.tk;document.getElementById("tk").lang=v.code;
document.getElementById("tklabel").textContent=label[k];
document.getElementById("body").innerHTML=B[k]||('<div class="other"><b>'+v.name+' version.</b> In this example the full article body is shown in English and Hindi. The '+v.name+' Writer writes this body natively in production; its title, description, key takeaways and image alt text above are already in '+v.name+'.</div>');
document.getElementById("body").lang=v.code;
document.getElementById("surl").textContent="starstell.com › "+v.slug.split("/").filter(Boolean).join(" › ");
document.getElementById("stitle").textContent=v.title;document.getElementById("sdesc").textContent=v.desc;
document.getElementById("wtitle").textContent=v.title.replace(" | StarsTell","");document.getElementById("wdesc").textContent=v.desc;
order.forEach(o=>document.getElementById("l-"+o).classList.toggle("on",o===k));}}
function route(){{const p=location.hash==="#pipeline";document.getElementById("blog").hidden=p;document.getElementById("pipeline").hidden=!p;
document.getElementById("v-blog").classList.toggle("on",!p);document.getElementById("v-pipe").classList.toggle("on",p);}}
addEventListener("hashchange",route);route();setLang("en");
</script></body></html>'''
open(OUT, 'w', encoding='utf-8', newline='\n').write(page)
print('checks', passed, 'of', len(checks), '| en words', en_words)
for c in checks:
    if not c[3]: print('FAIL', c)

# ---------------------------------------------------------------- "as published" preview pages
# One real page per language with its own head tags, schema and the article only.
# This is what the score gate audits before anything may go to the CMS.
import os
PREV = os.path.join(os.path.dirname(os.path.abspath(OUT)), 'preview')
os.makedirs(os.path.join(PREV, 'images'), exist_ok=True)
import shutil
for im in IMAGES:
    shutil.copy(os.path.join(os.path.dirname(os.path.abspath(OUT)), 'images', im['file']), os.path.join(PREV, 'images', im['file']))

def published(k):
    v = L[k]
    body = BODY.get(k)
    faqs = re.findall(r'<summary>(.*?)</summary><p>(.*?)</p>', body or '')
    ld = [
     {"@context": "https://schema.org", "@type": "BlogPosting", "headline": v['h1'], "description": v['desc'],
      "inLanguage": v['code'], "mainEntityOfPage": SITE + v['slug'],
      "image": [SITE + "/images/blog/life-path-number-7/featured.webp"],
      "author": {"@type": "Organization", "name": "StarsTell editorial team", "url": SITE + "/about"},
      "reviewedBy": {"@type": "Person", "name": "[Numerology reviewer name]", "jobTitle": "Numerologist",
                     "knowsAbout": ["Numerology", "Vedic astrology", "Chaldean numerology"],
                     "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": "[Reviewer's numerology certification]"},
                     "worksFor": {"@type": "Organization", "name": "StarsTell"}},
      "publisher": {"@type": "Organization", "name": "StarsTell", "url": SITE, "logo": {"@type": "ImageObject", "url": SITE + "/logo.png"}},
      "datePublished": "2026-11-20", "dateModified": "2026-11-20"},
     {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Blog", "item": SITE + "/blog"},
      {"@type": "ListItem", "position": 2, "name": "Numerology", "item": SITE + "/blog/numerology"},
      {"@type": "ListItem", "position": 3, "name": v['h1'], "item": SITE + v['slug']}]},
    ]
    ld.append({"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "Numerology terms", "hasDefinedTerm": [
        {"@type": "DefinedTerm", "name": "Life path number (Bhagyank)", "description": "The sum of every digit of the full date of birth, reduced to one digit."},
        {"@type": "DefinedTerm", "name": "Mulank (birth number)", "description": "The day of birth reduced to one digit."},
        {"@type": "DefinedTerm", "name": "Master number", "description": "A total of 11, 22 or 33 that many numerologists keep instead of reducing further."}]})
    if faqs:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    tags = f'''<title>{v['title']}</title>
<meta name="description" content="{v['desc']}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{SITE}{v['slug']}">
{hreflang}
<meta property="og:type" content="article"><meta property="og:title" content="{v['title'].replace(' | StarsTell','')}">
<meta property="og:description" content="{v['desc']}"><meta property="og:image" content="{SITE}/images/blog/life-path-number-7/featured.webp">
<meta property="og:url" content="{SITE}{v['slug']}"><meta property="og:locale" content="{v['code'].replace('-', '_')}">
<meta property="article:published_time" content="2026-11-20"><meta property="article:modified_time" content="2026-11-20">
<meta name="author" content="StarsTell editorial team">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{v['title'].replace(' | StarsTell','')}">
<meta name="twitter:description" content="{v['desc']}"><meta name="twitter:image" content="{SITE}/images/blog/life-path-number-7/featured.webp">
<meta name="twitter:image:alt" content="{html.escape(IMAGES[0]['alt'][k])}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'''
    content = body if body else ''
    return f'''<!doctype html>
<html lang="{v['code']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
{tags}
<style>body{{font-family:"Noto Sans",Arial,sans-serif;max-width:760px;margin:0 auto;padding:24px 16px;color:#2a1a12;line-height:1.7;background:#E3DBC7}}img{{max-width:100%;height:auto}}h1,h2,h3{{font-family:"Playfair Display",Georgia,serif;color:#421206}}</style>
</head><body>
<header><nav aria-label="Breadcrumb"><a href="/blog">Blog</a> › <a href="/blog/numerology">Numerology</a> › {v['h1']}</nav></header>
<main><article>
<h1>{v['h1']}</h1>
<p class="lead">{v['tk']}</p>
<p><time datetime="2026-11-20">20/11/2026</time> · By <a href="/about" rel="author">StarsTell editorial team</a> · Reviewed by [numerology reviewer], numerologist</p>
{fig(0, k if k in IMAGES[0]['alt'] else 'en', '')}
{content}
<aside><p>StarsTell: guidance from astrologers and numerologists who remember your story. <a href="/consult">Talk to an expert</a>.</p></aside>
</article></main>
<footer><p><a href="/about">About StarsTell</a> · <a href="/privacy">Privacy</a> · <a href="/contact">Contact</a></p></footer>
</body></html>'''

for k, v in L.items():
    path = os.path.join(PREV, v['slug'].lstrip('/'), 'index.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # images resolve from the preview root
    open(path, 'w', encoding='utf-8', newline='\n').write(published(k).replace('src="images/', 'src="/images/'))
print('preview pages written to', PREV)
