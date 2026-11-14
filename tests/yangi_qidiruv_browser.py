import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Lug'at qidiruvi: UK/US IPA + ovoz, AI boyitish, kesh, tarix, imlo tuzatish, ibora, lug'atga qo'shish, kartochkada IPA. Soat: 2026-11-03 10:00.
import sys, json
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
with Run('qidiruv', when=(2026, 11, 3, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);window.aiOk=()=>true;window.__fp=[];window.__ai=[];window.__au=[];window.__tts=[];
      window.Audio=function(u){this.u=u;__au.push(u);this.play=()=>Promise.resolve();this.pause=()=>{}};window.dqTts=(w,a)=>__tts.push([w,a]);
      const SUP={w:'support',ipaUK:'/səˈpɔːt/',ipaUS:'/səˈpɔɹt/',ipa:'/səˈpɔːt/',auUK:'https://api.dictionaryapi.dev/media/pronunciations/en/support-uk.mp3',auUS:'https://api.dictionaryapi.dev/media/pronunciations/en/support-us.mp3',meanings:[{pos:'verb',defs:[{d:'To help someone or something.',ex:'We support the plan.'}],syn:['back','help'],ant:['oppose']},{pos:'noun',defs:[{d:'Help given.',ex:''}],syn:[],ant:[]}],src:'https://en.wiktionary.org/wiki/support'};
      window.fnPost=async(b)=>{__fp.push(b);if(b.action==='dict'){if(window.__down)throw new Error('Lug‘atga ulanib bo‘lmadi.');if(b.word==='support')return SUP;if(b.word==='noipa')return {w:'noipa',ipa:'',meanings:[{pos:'noun',defs:[{d:'Something.',ex:''}],syn:[],ant:[]}]};return {nf:true}}return {}};
      window.fnAI=async(b)=>{__ai.push(b);if(b.action==='iex'&&b.kind==='dict'){if(window.__aifail)throw new Error('Bugungi limit tugadi (40 ta so‘rov).');const w=b.word;
        if(w==='support')return {text:JSON.stringify({w:'support',fix:'',lv:'B1',reg:'neutral',pos:['verb','noun'],ipaUK:'/ˈaiuk/',ipaUS:'/ˈaius/',uz:['qo‘llab-quvvatlamoq','yordam'],defs:[{pos:'verb',d:'to help someone by giving encouragement',uz:'qo‘llab-quvvatlamoq',ex:['Many people support the policy.','She supports her family.']}],col:['strongly support','support a claim'],syn:['back','assist'],ant:['oppose'],fam:[['supporter','n'],['supportive','adj']],tip:'Writing’da “agree with” o‘rniga “back” yoki “endorse” ishlating.',err:''})};
        if(w==='neccessary')return {text:JSON.stringify({w:'',fix:'necessary',err:'Imlo xato'})};
        if(w==='take for granted')return {text:JSON.stringify({w:'take for granted',lv:'C1',reg:'neutral',pos:['phrase'],ipaUK:'/teɪk fə ˈɡrɑːntɪd/',ipaUS:'/teɪk fɔːr ˈɡræntɪd/',uz:['qadrlamaslik'],defs:[{pos:'phrase',d:'to not value something enough',uz:'qadriga yetmaslik',ex:['Never take your health for granted.']}],col:[],syn:[],ant:[],fam:[],tip:'',err:''})};
        if(w==='noipa')return {text:JSON.stringify({w:'noipa',lv:'C2',ipaUK:'/ˈnɔɪpə/',ipaUS:'bad ipa',uz:['x'],defs:[],col:[],syn:[],ant:[],fam:[],tip:'',err:''})};
        return {text:JSON.stringify({w:w,lv:'C1',reg:'formal',pos:['noun'],ipaUK:'/ˈzɪk/',ipaUS:'/ˈzɪk/',uz:['sinov'],defs:[{pos:'noun',d:'a test word',uz:'sinov',ex:['A test.']}],col:[],syn:[],ant:[],fam:[],tip:'',err:''})}}return {text:'{}'}};
      localStorage.removeItem('trk_dqh');DQC=null;try{idbSet('dqc',{})}catch(e){}S.ie.words=[];tab='e';EV='i';IVW='l';render()}""")
    t = pg.inner_text('#app'); chk('the Lug‘at screen starts with the "🔎 Lug‘atdan qidirish" search card (above the cards and quiz)', '🔎 Lug‘atdan qidirish' in t and ev("!!document.getElementById('dqi')") and ev("document.querySelector('#app .goal b').textContent") == '🔎 Lug‘atdan qidirish')
    srch = lambda w: (pg.fill('#dqi', w), pg.click('#app .goal .in .btn'), pg.wait_for_timeout(400))
    srch('Support!'); fp = ev("__fp"); t = pg.inner_text('#app')
    chk('searching sends ONE free dictionary request with the cleaned word (lower case, punctuation removed)', len(fp) == 1 and fp[0] == {'action': 'dict', 'word': 'support'} and len(ev("__ai")) == 0, fp)
    chk('the card shows UK and US pronunciation on separate rows, in the Cambridge style: UK /səˈpɔːt/ 🔊 and US /səˈpɔɹt/ 🔊', 'UK\n/səˈpɔːt/' in t.replace('\n\n', '\n') or ('UK' in t and '/səˈpɔːt/' in t) and ev("document.querySelectorAll('#app .dqph').length") == 2 and '/səˈpɔɹt/' in t, t[:300])
    chk('real recorded audio is available: two speaker buttons (UK and US)', ev("document.querySelectorAll('#app .dqph .dqs').length") == 2)
    chk('English definitions with an example and the parts of speech are shown straight away (no AI used)', 'To help someone or something.' in t and 'We support the plan.' in t and 'verb' in t and 'noun' in t and 'back' in t and 'oppose' in t)
    ln = ev("[...document.querySelectorAll('#app .dqc a')].map(a=>[a.href,a.target,a.rel])")
    chk('"Cambridge ↗" and "Wiktionary ↗" links open the word on their own sites in a new tab', ['https://dictionary.cambridge.org/dictionary/english/support', '_blank', 'noopener'] in ln and ['https://en.wiktionary.org/wiki/support', '_blank', 'noopener'] in ln, ln)
    chk('the source (Wiktionary, CC BY-SA 3.0) is credited on the card', 'Wiktionary (CC BY-SA 3.0)' in t)
    pg.click('#app .dqph >> nth=0 >> .dqs'); pg.click('#app .dqph >> nth=1 >> .dqs'); au = ev("__au")
    chk('UK 🔊 plays the UK recording and US 🔊 the US recording', au == ['https://api.dictionaryapi.dev/media/pronunciations/en/support-uk.mp3', 'https://api.dictionaryapi.dev/media/pronunciations/en/support-us.mp3'], au)
    ev("()=>{DQ.e.au={uk:'',us:''};dqSay('uk')}"); chk('without a recording the device voice is used with the right accent (en-GB for UK)', ev("__tts") == [['support', 'uk']]); ev("()=>{DQ.e.au={uk:'x',us:''};window.Audio=function(){throw new Error('x')};__tts=[];dqSay('uk')}"); chk('a broken audio file falls back to the device voice too', len(ev("__tts")) == 1)
    ev("()=>{window.Audio=function(u){this.u=u;__au.push(u);this.play=()=>Promise.resolve();this.pause=()=>{}}}")
    ev("()=>{DQ.e.au={uk:'https://api.dictionaryapi.dev/media/pronunciations/en/support-uk.mp3',us:'https://api.dictionaryapi.dev/media/pronunciations/en/support-us.mp3'}}")
    # ---------- AI boyitish ----------
    pg.click('#app .dqc >> text=O‘zbekcha ma‘no, misollar va 8+ maslahat'); pg.wait_for_timeout(400); ai = ev("__ai"); t = pg.inner_text('#app')
    chk('the AI button sends ONE entry request carrying the free definitions as a hint', len(ai) == 1 and ai[0]['kind'] == 'dict' and ai[0]['word'] == 'support' and 'To help someone or something' in ai[0]['hint'], ai)
    chk('the card then shows the Uzbek meanings, definitions with Uzbek and 2 examples, collocations, word family and the IELTS 8+ tip; the level B1 chip', 'qo‘llab-quvvatlamoq · yordam' in t and 'Many people support the policy.' in t and 'strongly support' in t and 'supporter (n)' in t and '🎯 IELTS 8+ maslahat' in t and 'endorse' in t and 'B1' in t and 'formal' not in t)
    phr = lambda: ev("[...document.querySelectorAll('#app .dqph')].map(e=>e.textContent.replace(/\\s+/g,' ').trim())")
    chk('the recorded IPA is kept: the AI\u2019s own IPA never replaces dictionary data (UK stays /səˈpɔːt/)', len(phr()) == 2 and '/səˈpɔːt/' in phr()[0] and '/səˈpɔɹt/' in phr()[1] and not any('AI taxmini' in x or 'ˈaiuk' in x for x in phr()), phr())
    chk('the AI button is gone once the entry is complete', ev("![...document.querySelectorAll('#app .dqc button')].some(b=>b.textContent.includes('(AI)'))"))
    # ---------- kesh ----------
    ev("()=>{__fp=[];__ai=[];DQ.e=null;DQ.q='';render()}"); srch('support'); chk('searching the same word again needs NO request at all (cached, with the AI part too)', len(ev("__fp")) == 0 and len(ev("__ai")) == 0 and 'Many people support the policy.' in pg.inner_text('#app'))
    ev("()=>{DQC=null;DQ.e=null;__fp=[];__ai=[];render()}"); srch('support'); chk('the cache survives an app restart (it is kept in the device storage)', len(ev("__fp")) == 0 and 'strongly support' in pg.inner_text('#app'))
    ev("()=>{DQ.e=null;render()}"); h = ev("[...document.querySelectorAll('#app .goal .rwch .chip')].map(c=>c.textContent)"); chk('recent searches appear as chips', 'support' in h, h)
    pg.click('#app .goal .rwch .chip >> text=support'); pg.wait_for_timeout(200); chk('tapping a recent chip opens the word without any request', len(ev("__fp")) == 0 and ev("DQ.e&&DQ.e.w") == 'support')
    # ---------- ochiq lug'atda yo'q so'z ----------
    ev("()=>{DQ.e=null;__fp=[];__ai=[];render()}"); srch('zzzxq'); t = pg.inner_text('#app')
    chk('a word missing from the free dictionary automatically gets a full AI entry, and its IPA is honestly labelled "AI taxmini"', len(ev("__fp")) == 1 and len(ev("__ai")) == 1 and 'sinov' in t and len(phr()) == 2 and all('/ˈzɪk/' in x and 'AI taxmini' in x for x in phr()) and 'C1' in t, phr())
    ev("()=>{DQ.e=null;__fp=[];__ai=[];render()}"); srch('noipa'); chk('a word with no IPA in the free dictionary shows the UK/US buttons and "IPA topilmadi"', 'IPA topilmadi' in pg.inner_text('#app') and len(phr()) == 1)
    ev("dqAi()"); pg.wait_for_timeout(400); chk('then AI adds the valid IPA only (the invalid one "bad ipa" is dropped) and labels it', len(phr()) == 1 and '/ˈnɔɪpə/' in phr()[0] and 'AI taxmini' in phr()[0] and 'bad ipa' not in pg.inner_text('#app'), phr())
    ev("()=>{DQ.e=null;__fp=[];__ai=[];render()}"); srch('neccessary'); t = pg.inner_text('#app')
    chk('a misspelling: the AI answer becomes a suggestion "Siz necessary demoqchimisiz?"', 'Siz necessary demoqchimisiz?' in t, t[:200])
    pg.click('#app .goal >> button >> text=necessary'); pg.wait_for_timeout(400); chk('tapping the suggestion searches the corrected word', ev("DQ.q") == 'necessary')
    ev("()=>{DQ.e=null;DQ.sug='';__fp=[];__ai=[];render()}"); srch('take for granted'); t = pg.inner_text('#app')
    chk('a phrase skips the single-word dictionary and gets an AI entry (IPA, Uzbek, example)', len([f for f in ev("__fp")]) == 0 and 'qadrlamaslik' in t and 'Never take your health for granted.' in t and '/teɪk fə ˈɡrɑːntɪd/' in t)
    # ---------- kiritish tekshiruvi va xatolar ----------
    ev("()=>{DQ.e=null;__fp=[];__ai=[];render()}"); srch('12345'); chk('numbers are refused locally with a clear message (no request)', 'Faqat inglizcha' in pg.inner_text('#app') and len(ev("__fp")) == 0)
    pg.fill('#dqi', ''); pg.click('#app .goal .in .btn'); pg.wait_for_timeout(100); chk('an empty search asks to type a word', 'So‘z yoki ibora yozing' in pg.inner_text('#app'))
    ev("window.aiOk=()=>false"); srch('hello'); chk('not signed in: a clear message and no request', 'hisobga kirish' in pg.inner_text('#app') and len(ev("__fp")) == 0); ev("window.aiOk=()=>true")
    ev("()=>{DQ.e=null;DQ.err='';DQC={};__fp=[];__ai=[];window.__down=1;render()}"); srch('hello'); chk('if the dictionary service is down the error is shown and nothing breaks', 'ulanib bo‘lmadi' in pg.inner_text('#app') and ev("DQ.busy") == 0); ev("window.__down=0")
    ev("()=>{DQ.e=null;DQ.err='';DQC={};window.__aifail=1;render()}"); srch('support'); ev("dqAi()"); pg.wait_for_timeout(300)
    chk('if the AI fails (daily limit) the free card stays and the reason is shown', 'Bugungi limit tugadi' in pg.inner_text('#app') and 'To help someone or something.' in pg.inner_text('#app') and ev("DQ.ai") == 0); ev("window.__aifail=0")
    # ---------- lug'atga qo'shish ----------
    ev("()=>{DQ.e=null;DQ.err='';DQC={};__fp=[];__ai=[];S.ie.words=[];render()}"); srch('support'); ev("dqAi()"); pg.wait_for_timeout(400); pg.click('#app .dqc >> text=Lug‘atga qo‘shish'); pg.wait_for_timeout(200); w = ev("S.ie.words[S.ie.words.length-1]")
    chk('"➕ Lug‘atga qo‘shish" saves the word with Uzbek meaning, definition, example, level, part of speech and BOTH IPAs', w['w'] == 'support' and 'qo‘llab-quvvatlamoq' in w['u'] and w['lv'] == 'B1' and w['pos'] == 'ver'[:3] or (w['w'] == 'support' and w['pu'] == '/səˈpɔːt/' and w['ps'] == '/səˈpɔɹt/' and w['d'] and w['e'] and w['lv'] == 'B1'), w)
    chk('IPA and level are stored on the word', w['pu'] == '/səˈpɔːt/' and w['ps'] == '/səˈpɔɹt/' and w['lv'] == 'B1')
    chk('the button turns into "✓ Lug‘atda bor" and a second add is impossible', '✓ Lug‘atda bor' in pg.inner_text('#app') and ev("S.ie.words.filter(x=>x.w==='support').length") == 1)
    ev("()=>{IR=0;render()}"); pg.wait_for_timeout(60); ev("()=>{IR=1;render()}"); pg.wait_for_timeout(100); chk('the flashcard of that word shows "UK /…/ · US /…/" on its back', 'UK /səˈpɔːt/ · US /səˈpɔɹt/' in pg.inner_text('#app'))
    ev("()=>{DQ.e=null;DQC={};__fp=[];__ai=[];render()}"); srch('take for granted'); pg.click('#app .dqc >> text=Lug‘atga qo‘shish'); pg.wait_for_timeout(200); chk('a phrase is saved as a chunk (k = c)', ev("S.ie.words.find(x=>x.w==='take for granted').k") == 'c')
    # ---------- tekshiruvchi va kesh chegarasi ----------
    cl = ev("(()=>{const r=dqClean({w:'x',lv:'Z9',reg:'weird',ipaUK:'nope',ipaUS:'/ok/',uz:['a','b','c','d','e','f'],col:Array(20).fill('c'),defs:[{d:'d',ex:['1','2','3','4']}],fam:[['a','n'],'bad']});return [r.lv,r.reg,r.ipaUK,r.ipaUS,r.uz.length,r.col.length,r.defs[0].ex.length,r.fam.length]})()")
    chk('the AI answer is cleaned: bad level/register/IPA dropped; lists capped (4 meanings, 6 collocations, 2 examples)', cl == ['', '', '', '/ok/', 4, 6, 2, 1], cl)
    ev("()=>{DQC={};for(let i=0;i<330;i++)DQC['w'+i]={w:'w'+i,ts:i};dqSaveC()}"); chk('the on-device cache is limited to 300 words (oldest are dropped)', ev("Object.keys(DQC).length") == 300 and ev("!DQC.w0&&!!DQC.w329"))
    # ---------- ikkala uslubda to'g'ri ko'rinadi ----------
    ev("()=>{DQ.e=null;DQC={};__fp=[];__ai=[];render()}"); srch('support'); ev("dqAi()"); pg.wait_for_timeout(300)
    bad = []
    for ui in ('1', '2'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1]}", [ui, th]); pg.wait_for_timeout(80)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('the full card does not overflow the phone screen in Klassik and Yangi, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
