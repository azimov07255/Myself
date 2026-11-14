import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Kunlik natija kartasi, tezlik trenajyori (RSVP), xotira saroyi. Soat: 2026-11-05 10:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
BODY = '## Heading line\n\n' + ' '.join('w%d' % i for i in range(100)) + '.'
with Run('karta', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""(B)=>{window.__t=[];window.toast=m=>window.__t.push(m);window.aiOk=()=>true;window.__xp={};window.dayPts=k=>({t:window.__xp[k]||0});window.rwStreak=()=>6;
      window.__ft=[];const of=CanvasRenderingContext2D.prototype.fillText;CanvasRenderingContext2D.prototype.fillText=function(t,x,y){window.__ft.push(String(t));return of.call(this,t,x,y)};
      window.__req=[];window.__ret=null;window.__fail='';window.fnAI=async b=>{__req.push(b);if(window.__fail)throw new Error(window.__fail);return {text:window.__ret!==null?window.__ret:JSON.stringify({items:(b.words||[]).map(x=>({w:x.w,h:'Eslab qol: '+x.w+' — tovushga o‘xshash obraz.'}))})}};
      localStorage.removeItem('trk_sc');S.hab=[{id:'h1',t:'A'},{id:'h2',t:'B'},{id:'h3',t:'C'}];S.hb={};S.hb[dk()]={h1:true,h2:true};S.fl=[{d:dk(),a:'IELTS',m:50}];S.ie.rmd={};S.ie.rmd[dk()]=12;window.__xp[dk()]=140;S.bs=undefined;S.rw={};rwReset();
      S.ie.mat=[{id:1,t:'Speed text',k:'a',x:B,c:[],au:0,d:dk(),an:null},{id:2,t:'Short',k:'a',x:'too short text here',c:[],au:0,d:dk(),an:null}];S.ie.rsv=undefined;S.ie.mn={};S.ie.words=[];tab='m';MQV='b';render()}""", BODY)
    pg.wait_for_timeout(200)
    chk('the Goals screen has the "📤 Kunlik natija kartasi" with a 1080×1350 canvas preview, 3 styles, show/hide chips and share/download/copy buttons', '📤 Kunlik natija kartasi' in pg.inner_text('#app') and ev("document.getElementById('scv').width") == 1080 and ev("document.getElementById('scv').height") == 1350 and all(x in pg.inner_text('#app') for x in ['Uslub 1', 'Uslub 3', 'Ulashish', 'Rasm']))
    ft = ev("__ft")
    chk('the card is drawn with today\u2019s real numbers: 140 XP, 6-day streak, 50 focus minutes, 12 new words, 2/3 habits, the boss, a motivational line and the date', all(x in ft for x in ['Kunlik tizim', '2026-11-05', '140', 'XP bugun', '🔥 6 kun seriya', '🍅 50 daq fokus', '📘 12 yangi so‘z', '✅ 2/3 odat']) and any(x.startswith(ev("bsState().b.e")) and ev("bsState().b.n") in x for x in ft), ft[:14])
    px = ev("(()=>{const c=document.getElementById('scv').getContext('2d'),s=new Set();for(const [x,y] of [[5,5],[540,5],[1070,5],[540,400],[540,700],[300,1000],[1070,1340],[5,1340]]){const d=c.getImageData(x,y,1,1).data;s.add(d.join())}return s.size})()")
    chk('the canvas is really painted (a gradient and shapes, not a blank page)', px >= 4, px)
    ev("scTog('streak')"); pg.wait_for_timeout(120); ft = ev("(()=>{__ft.length=0;scPaint();return __ft})()")
    chk('hiding "Seriya" removes it from the picture (and the choice is remembered on the device)', not any('kun seriya' in x for x in ft) and ev("JSON.parse(localStorage.getItem('trk_sc')).hide.streak") is True and ev("document.querySelector('.goal[aria-label=\"Kunlik natija kartasi\"] .chip[aria-pressed=false]').textContent") == 'Seriya')
    ev("(()=>{scTog('xp');scTog('boss');scTog('hab')})()"); pg.wait_for_timeout(120); ft = ev("(()=>{__ft.length=0;scPaint();return __ft})()")
    chk('hiding XP, Boss and Odat removes those lines; the rest stays', 'XP bugun' not in ft and '140' not in ft and not any(x.startswith('✅') for x in ft) and not any(ev("bsState().b.n") in x for x in ft) and '🍅 50 daq fokus' in ft)
    ev("(()=>{scTog('xp');scTog('boss');scTog('hab');scTog('streak')})()")
    cols = []
    for i in (0, 1, 2):
        ev("scTh(%d)" % i); pg.wait_for_timeout(120); cols.append(ev("document.getElementById('scv').getContext('2d').getImageData(3,3,1,1).data.join()"))
    chk('the three styles use different backgrounds', len(set(cols)) == 3, cols)
    txt = ev("scText()"); chk('the text version carries the same numbers for chats', '📊 Kunlik tizim — 2026-11-05' in txt and '⭐ 140 XP' in txt and '🔥 6 kun seriya' in txt and '✅ 2/3 odat' in txt and 'HP' in txt)
    ev("""()=>{window.__sh=null;Object.defineProperty(navigator,'canShare',{value:()=>true,configurable:true});Object.defineProperty(navigator,'share',{value:async d=>{window.__sh=d},configurable:true})}""")
    ev("()=>{scShare();return 1}"); pg.wait_for_timeout(500); sh = ev("__sh&&{n:__sh.files[0].name,t:__sh.files[0].type,s:__sh.files[0].size,x:__sh.text}")
    chk('"📲 Ulashish" shares a real PNG file (kunlik-natija-2026-11-05.png) plus the text through the phone\u2019s share sheet (Telegram, Instagram…)', sh and sh['n'] == 'kunlik-natija-2026-11-05.png' and sh['t'] == 'image/png' and sh['s'] > 5000 and 'Kunlik tizim' in sh['x'], sh)
    ev("()=>{window.__sh=null;Object.defineProperty(navigator,'canShare',{value:()=>false,configurable:true})}"); ev("()=>{scShare();return 1}"); pg.wait_for_timeout(400); chk('if files cannot be shared the text is shared', ev("__sh&&__sh.files===undefined&&__sh.text.includes('Kunlik tizim')"))
    ev("""()=>{window.__dl=[];Object.defineProperty(navigator,'share',{value:undefined,configurable:true});const oc=HTMLAnchorElement.prototype.click;HTMLAnchorElement.prototype.click=function(){if(this.download)window.__dl.push([this.download,this.href.slice(0,5)]);else oc.call(this)}}""")
    ev("()=>{scShare();return 1}"); pg.wait_for_timeout(500); chk('without any share support the picture is downloaded instead', ev("__dl")[0] == ['kunlik-natija-2026-11-05.png', 'blob:'] if ev("__dl.length") else False)
    ev("()=>{window.__dl.length=0;scDownload();return 1}"); pg.wait_for_timeout(400); chk('"⬇ Rasm" downloads kunlik-natija-<date>.png', ev("__dl.length") == 1 and ev("__dl[0][0]") == 'kunlik-natija-2026-11-05.png')
    ev("""()=>{window.__cp='';Object.defineProperty(navigator,'clipboard',{value:{writeText:async t=>{window.__cp=t}},configurable:true});scCopy()}"""); chk('"📋" copies the text', ev("__cp").startswith('📊 Kunlik tizim'))
    ev("""()=>{Object.defineProperty(navigator,'canShare',{value:()=>true,configurable:true});Object.defineProperty(navigator,'share',{value:async()=>{const e=new Error('x');e.name='AbortError';throw e},configurable:true});__t=[];scShare()}"""); pg.wait_for_timeout(300); chk('closing the share sheet (AbortError) is not an error', ev("__t.length") == 0)
    ev("""()=>{Object.defineProperty(navigator,'share',{value:async()=>{throw new Error('boom')},configurable:true});__t=[];scShare()}"""); pg.wait_for_timeout(300); chk('a real sharing failure tells the user to download the picture', any('yuklab oling' in m for m in ev("__t")))
    # ---------- tezlik ----------
    ev("()=>{IVW='a';tab='e';EV='i';render();ieMatOpen(1)}"); pg.wait_for_timeout(300); chk('the reading screen has a "⚡ Tezlik" chip', '⚡ Tezlik' in pg.inner_text('#iem'))
    ev("[...document.querySelectorAll('#iem .chip')].find(c=>c.textContent.includes('Tezlik')).click()"); pg.wait_for_timeout(120); t = pg.inner_text('#rvo')
    chk('it opens the trainer with the title, a counter, the speed (250 words/min) and controls; heading marks are not words (101 words: heading 2 + 100)', 'Speed text' in t and '250 so‘z/daq' in t and '1 / 102' in t and ev("RV.w[0]") == 'Heading' and ev("RV.w.every(w=>!w.startsWith('#'))"), (t[:80], ev("RV.w.length")))
    o = lambda w: ev("(w)=>{const d=document.createElement('div');d.innerHTML=rvWord([w]);return [d.querySelector('.rvl').textContent,d.querySelector('.rvx').textContent,d.querySelector('.rvr').textContent]}", w)
    chk('each word is shown with its red focus letter in a fixed centre (optimal recognition point): reading → re|a|ding, a → |a|, “Hello, → “He|l|lo,', o('reading') == ['re', 'a', 'ding'] and o('a') == ['', 'a', ''] and o('“Hello,') == ['“H', 'e', 'llo,'] and o('extraordinary') == ['ext', 'r', 'aordinary'], [o('reading'), o('a'), o('“Hello,')])
    ev("RV.wpm=300"); d = lambda a: ev("(a)=>rvDelay(a)", a)
    chk('timing at 300 words/min: a plain word 200 ms, after a comma 260, after a full stop 360, a long word (9+ letters) ×1.2 = 240, a 2-word chunk 400', d(['word']) == 200 and d(['word,']) == 260 and d(['word.']) == 360 and d(['beautifully']) == 240 and d(['a', 'b']) == 400)
    ev("(()=>{RV.wpm=600;rvDraw()})()"); ev("[...document.querySelectorAll('#rvo button')].find(b=>b.textContent.includes('Boshlash')).click()"); pg.clock.run_for(1050); pg.wait_for_timeout(60); i1 = ev("RV.i")
    chk('"▶ Boshlash" shows the words one by one at the chosen speed (600/min = 100 ms each: ~10 words in a second); the counter and progress bar move without redrawing the screen', 8 <= i1 <= 12 and ev("document.querySelector('#rvo .rvc').textContent").startswith(f'{i1 + 1} / ') and ev("parseInt(document.querySelector('#rvo .rvp i').style.width)") > 5, i1)
    ev("[...document.querySelectorAll('#rvo button')].find(b=>b.textContent.includes('Pauza')).click()"); pg.wait_for_timeout(40); i2 = ev("RV.i"); pg.clock.run_for(3000); pg.wait_for_timeout(40); chk('⏸ Pauza stops at once and nothing advances while paused', ev("RV.i") == i2 and ev("RV.pl") == 0)
    ev("document.querySelector('#rvo [aria-label=\"10 so‘z oldinga\"]').click()"); pg.wait_for_timeout(40); chk('⏩ / ⏪ jump 10 words (never past the ends)', ev("RV.i") == i2 + 10); ev("rvSeek(-500)"); chk('...clamped at the start', ev("RV.i") == 0); ev("rvSeek(5000)"); chk('...and at the end', ev("RV.i") == 101); ev("RV.i=0")
    ev("rvWpm(-1000)"); chk('speed is limited to 100–800 words/min (steps of 25)', ev("RV.wpm") == 100); ev("rvWpm(5000)"); chk('...upper limit 800', ev("RV.wpm") == 800); ev("RV.wpm=600")
    ev("rvCh(2)"); ev("RV.i=0"); ev("rvPlay()"); pg.clock.run_for(450); pg.wait_for_timeout(40); i3 = ev("RV.i"); chk('2-word chunks advance two words per step (200 ms per chunk at 600/min: 4 words after 450 ms) and show both words together', i3 == 4 and ev("!!document.querySelector('#rvo .rvm')"), i3); ev("rvPause();rvCh(1)")
    # tugatish
    ev("()=>{RV.i=0;RV.ms=0;RV.wpm=600;RV.ch=1}"); ev("rvPlay()"); pg.clock.run_for(12500); pg.wait_for_timeout(100); t = pg.inner_text('#rvo'); L = ev("S.ie.rsv.log")
    chk('at the end the result shows your real speed in words/min (102 words in ~11 s ≈ 560–620), the time, and the tip about comprehension (“Savollar”)', 'so‘z/daq' in t and ev("RV.end") == 1 and 540 <= ev("RV.ew") <= 640 and 'Savollar' in t and '102 so‘z' in t, (t[:120], ev("RV.ew")))
    chk('the run is saved (date, material, words, set speed, real speed) and becomes the best (it is at least 80 words)', len(L) == 1 and L[0]['d'] == '2026-11-05' and L[0]['id'] == 1 and L[0]['n'] == 102 and L[0]['wpm'] == 600 and ev("S.ie.rsv.best") == L[0]['ew'] and '🏆 yangi rekord' in t, L)
    ev("()=>{S.ie.rsv.log=Array.from({length:40},(_,i)=>({d:'2026-10-01',id:1,n:100,wpm:200,ew:200}));S.ie.rsv.best=999;RV.i=0;RV.ms=0;RV.end=0;RV.pl=0;rvPlay()}"); pg.clock.run_for(12500); pg.wait_for_timeout(100)
    chk('only the last 30 runs are kept and a slower run does not replace the best', len(ev("S.ie.rsv.log")) == 30 and ev("S.ie.rsv.best") == 999 and '🏆' not in pg.inner_text('#rvo'))
    ev("rvClose()"); chk('closing removes the screen and stops the timer', ev("!document.getElementById('rvo')") and ev("RV") is None)
    ev("()=>{window.__t=[];rvOpen(2)}"); chk('a very short text cannot be trained (clear message)', any('juda qisqa' in m for m in ev("__t")) and ev("RV") is None)
    ev("()=>{rvOpen(1)}"); ev("rvClose()"); ev("()=>{rvOpen(1)}"); chk('the next session starts at the speed of your last run (600)', ev("RV.wpm") == 600); ev("rvClose()")
    # ---------- xotira saroyi ----------
    ev("""()=>{const T=dk(),mk=(w,m,box,t,fl,u)=>({id:Math.random(),w,m,u,box,due:T,t,fl:fl||0});S.ie.mn={};S.ie.words=[mk('mitigate','yumshatmoq',0,5,3),mk('scarce','kam',1,5,1),mk('ubiquitous','',0,5,2),mk('novel','yangi',4,5,0),mk('ephemeral','vaqtinchalik',0,0,0),mk('stable','barqaror',1,7,0),mk('abundant','',0,5,2,'ko‘p'),mk('known','bor',0,9,5)];S.ie.mn.known={h:'bor',t:1};EV='i';IVW='l';tab='e';render()}""")
    pk = ev("mnPick().map(w=>w.w)")
    chk('the hardest words are chosen: those you failed (most failures first), then low-box reviewed ones; no meaning → skipped; unreviewed (never seen) → skipped; already has a story → skipped', pk == ['mitigate', 'abundant', 'scarce', 'stable'], pk)
    pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('the vocabulary screen shows "🏰 Xotira saroyi" with the hard words and the button (1 AI)', '🏰 Xotira saroyi' in t and 'mitigate' in t and 'Hikoyalarni yaratish (1 AI)' in t and 'AI, 4 qiyin so‘z' in t)
    ev("[...document.querySelectorAll('#app button')].find(b=>b.textContent.includes('Hikoyalarni yaratish')).click()"); pg.wait_for_timeout(300); rq = ev("__req[0]")
    chk('ONE request (mnemo) with the words and their Uzbek meaning (user meaning preferred): mitigate=yumshatmoq, abundant=ko‘p', rq['kind'] == 'mnemo' and [(x['w'], x['m']) for x in rq['words']] == [('mitigate', 'yumshatmoq'), ('abundant', 'ko‘p'), ('scarce', 'kam'), ('stable', 'barqaror')], rq['words'])
    M = ev("S.ie.mn"); chk('the stories are stored under the lower-case word and appear in the saved list', all(k in M for k in ('mitigate', 'abundant', 'scarce', 'stable')) and 'Eslab qol: mitigate' in M['mitigate']['h'] and ev("mnPick().length") == 0)
    ev("()=>{const w=S.ie.words[0];w.fl=1;S.ie.mn={};window.__ret=JSON.stringify({items:[{w:'mitigate',h:'x'.repeat(400)},{w:'unknown',h:'Bu so‘z so‘ralmagan'},{w:'scarce',h:''}]});mnGo()}"); pg.wait_for_timeout(300); M = ev("S.ie.mn")
    chk('only requested words are accepted, empty stories are dropped and long ones cut to 170 characters', list(M.keys()) == ['mitigate'] and len(M['mitigate']['h']) == 170)
    ev("()=>{S.ie.mn={};window.__ret='yaroqsiz';MNE='';mnGo()}"); pg.wait_for_timeout(300); chk('an unusable AI answer shows a clear message', ('tushunarsiz' in pg.inner_text('#app') or 'hikoya yozmadi' in pg.inner_text('#app')) and not ev("Object.keys(S.ie.mn).length")); ev("window.__ret=null")
    ev("()=>{window.__fail='Bugungi limit tugadi (40 ta so‘rov).';mnGo()}"); pg.wait_for_timeout(300); chk('an AI failure (limit) shows the reason on the card', 'Bugungi limit tugadi' in pg.inner_text('#app')); ev("window.__fail=''")
    ev("()=>{S.ie.mn={};mnGo();return 1}"); pg.wait_for_timeout(300)
    t = ev("(()=>{IR=1;return ieCard(S.ie.words[0])})()"); chk('the story is shown on the flashcard (answer side) under the meaning', '🏰' in t and 'Eslab qol: mitigate' in t and 'class="mnl"' in t)
    ev("()=>{S.ie.mn.mitigate.h='<img src=x onerror=alert(1)>';render()}"); pg.wait_for_timeout(80); chk('story text is never executed as HTML', ev("document.querySelectorAll('#app img[src=x]').length") == 0 and '&lt;img' in ev("(()=>{IR=1;return ieCard(S.ie.words[0])})()"))
    ev("mnDel('mitigate')"); chk('a story can be deleted', ev("!S.ie.mn.mitigate"))
    ev("()=>{S.ie.words.forEach(w=>{w.box=0;w.due=dk();w.t=5;w.fl=0});const w=wDue()[0];window.__w0=w.id;iAns(0)}"); chk('answering "Bilmadim" counts a failure on the word; "Bildim" does not', ev("S.ie.words.find(w=>w.id===__w0).fl") == 1)
    ev("()=>{const w=S.ie.words.find(x=>x.id===__w0);w.due=dk();iAns(1)}"); chk('...(correct answer leaves the failure count unchanged)', ev("S.ie.words.find(w=>w.id===__w0).fl") == 1)
    ev("()=>{S.ie.mn={};for(let i=0;i<310;i++)S.ie.mn['w'+i]={h:'x',t:i};S.ie.words=[{id:1,w:'zzz',m:'q',box:0,due:dk(),t:5,fl:1}];mnGo()}"); pg.wait_for_timeout(300); chk('at most 300 stories are kept (the oldest go first)', len(ev("Object.keys(S.ie.mn)")) <= 300 and 'zzz' in ev("S.ie.mn"))
    bad = []
    ev("()=>{S.ie.mn={abundant:{h:'Uzun hikoya matni '.repeat(8),t:2}};S.ie.words=[{id:1,w:'mitigate',m:'yumshatmoq',box:0,due:dk(),t:5,fl:2}];S.ie.rsv=undefined;S.hab=[{id:'h1',t:'A'}]}")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='m';MQV='b';render()}", [ui, th]); pg.wait_for_timeout(120)
            ok1 = ev("document.documentElement.scrollWidth<=window.innerWidth+1")
            ev("()=>{tab='e';EV='i';IVW='l';render()}"); pg.wait_for_timeout(80); ok2 = ev("document.documentElement.scrollWidth<=window.innerWidth+1")
            ev("()=>{rvOpen(1)}"); pg.wait_for_timeout(60); ok3 = ev("document.querySelector('#rvo .rvb').scrollWidth<=document.querySelector('#rvo .rvb').clientWidth+1"); ev("rvClose()")
            if not (ok1 and ok2 and ok3): bad.append(ui + th)
    chk('the result card, memory palace and speed trainer fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
