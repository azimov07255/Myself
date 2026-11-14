import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# IELTS 8+ yo'l xaritasi: bosqichlar, maqsad, bugungi paket, daraja aniqlash, test. Soat: 2026-11-03 10:00.
import sys, json
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
LISTS = open((ROOT + '/data/ielts-lists-v1.json'), encoding='utf-8').read()
with Run('yol', when=(2026, 11, 3, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""(txt)=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);window.aiOk=()=>true;window.__req=[];window.__omit='';window.__failAt=0;
      const of=window.fetch;window.fetch=async(u,o)=>{if(String(u).includes('ielts-lists-v1.json')){if(window.__nofile)return new Response('',{status:404});return new Response(txt,{status:200})}return of(u,o)};
      window.fnAI=async b=>{__req.push(b);if(b.action==='iex'&&b.kind==='pack'){if(window.__failAt&&__req.filter(x=>x.kind==='pack').length===window.__failAt)throw new Error('Tarmoq xatosi');return {text:JSON.stringify({items:b.words.filter(w=>w!==window.__omit).map(w=>({w,pos:'n',lv:'B2',ipaUK:'/ˈ'+w.replace(/ /g,'')+'/',ipaUS:'/ˈ'+w.replace(/ /g,'')+'ː/',uz:'ma‘no-'+w,def:'definition of '+w,ex:'Example with '+w+'.',col:['col1 '+w,'col2 '+w]}))})}}return {text:'{}'}};
      S.ie.words=[];S.ie.rmk=[];S.ie.rmd={};S.ie.rmp=null;S.ie.rms='auto';S.ie.rmo='';S.ie.rmg=10;S.ie.rmt=null;S.ie.kr=null;YX={ld:0,err:'',data:null,gen:0,err2:'',pl:null,qz:null};KS.sec='l';tab='e';EV='i';IVW='b';render()}""", LISTS)
    top = ev("[...document.querySelectorAll('#app .seg')[1].querySelectorAll('button')].map(b=>b.textContent.trim())")
    chk('IELTS has a fifth tab "🎓 Kurs" next to Lug‘at', len(top) == 5 and top[2].endswith('Kurs'), top)
    ev("()=>{IVW='y';KS.sec='l';render()}"); pg.wait_for_timeout(500); t = pg.inner_text('#app'); n = ev("YX.data.top.length")
    chk('the roadmap opens with the six stages and their sizes: 542, 499, 1000, 800 (NGSL), 947 (NAWL) and the 8+ topic words', all(s in t for s in ['Asos 1', 'Asos 2', 'O‘rta', 'Yuqori', 'Akademik', 'IELTS 8+', '0 / 542', '0 / 499', '0 / 1000', '0 / 800', '0 / 947', '0 / %d' % n]) and 340 <= n <= 360, t[:200])
    chk('the first stage (Asos 1) is the current one and the daily goal starts at 0 / 10', ev("document.querySelector('#app .yxrow.now').textContent").startswith('🌱 Asos 1') and 'Bugungi maqsad: 0 / 10' in t)
    chk('the word-list credit (NGSL/NAWL, CC BY-SA 4.0) is shown', 'CC BY-SA 4.0' in t and 'newgeneralservicelist.com' in t)
    # ---------- statistika ----------
    ev("()=>{S.ie.words=[{id:1,w:'the',m:'x',u:'x',k:'w',box:0,due:dk(),t:0},{id:2,w:'be',m:'x',u:'x',k:'w',box:5,due:dk(),t:0}];S.ie.rmk=['and'];render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('progress counts words in your vocabulary and words marked "Bilaman": 3 / 542, and how many are memorised (box 4+)', '3 / 542' in t and 'yodlangan 1' in t, t[t.index('Asos 1'):t.index('Asos 1') + 120])
    ev("()=>{S.ie.rmk=S.ie.rmk.concat(YX.data.g1.slice(0,500));render()}"); pg.wait_for_timeout(100)
    chk('when a stage is 90% done the automatic stage moves on to the next (Asos 2)', ev("document.querySelector('#app .yxrow.now').textContent").startswith('🌿 Asos 2'))
    pg.click('#app .yxrow >> nth=3'); pg.wait_for_timeout(80); chk('tapping a stage makes it the current one (saved)', ev("S.ie.rms") == 'g4' and ev("document.querySelector('#app .yxrow.now').textContent").startswith('⛰️ Yuqori'))
    pg.click('#app >> text=Avtomatik bosqich'); pg.wait_for_timeout(80); chk('"Avtomatik bosqich" returns to automatic', ev("S.ie.rms") == 'auto')
    # ---------- bugungi paket ----------
    ev("()=>{S.ie.words=[{id:1,w:'the',m:'x',u:'x',k:'w',box:0,due:dk(),t:0}];S.ie.rmk=['and'];S.ie.rms='g1';__req=[];render()}"); pg.wait_for_timeout(100)
    exp = ev("YX.data.g1.filter(w=>w!=='the'&&w!=='and').slice(0,10)"); pg.click('#app >> text=Bugungi 10 ta so‘zni tayyorla'); pg.wait_for_timeout(600); rq = [r for r in ev("__req") if r.get('kind') == 'pack']
    chk('the pack asks for the NEXT 10 words of the stage (skipping words already in the vocabulary or marked known) in ONE request', len(rq) == 1 and rq[0]['words'] == exp, (rq[0]['words'] if rq else None, exp))
    t = pg.inner_text('#app'); w0 = exp[0]
    chk('every word shows UK and US IPA, the Uzbek meaning, the definition, an example and collocations, with level and part of speech', 'UK /ˈ%s/' % w0 in t and 'US /ˈ%sː/' % w0 in t and 'ma‘no-%s' % w0 in t and 'definition of %s' % w0 in t and 'Example with %s.' % w0 in t and 'col1 %s' % w0 in t and 'B2' in t, t[t.index('Bugungi so'):t.index('Bugungi so') + 300])
    pg.click('#app .yxw >> nth=0 >> text=Lug‘atga qo‘shish'); pg.wait_for_timeout(150); w = ev("S.ie.words[S.ie.words.length-1]")
    chk('"➕ Lug‘atga qo‘shish" stores the word with meaning, definition, example, level and both IPAs', w['w'] == w0 and w['u'] == 'ma‘no-' + w0 and w['d'] == 'definition of ' + w0 and w['e'] == 'Example with %s.' % w0 and w['lv'] == 'B2' and w['pu'] == '/ˈ%s/' % w0 and w['ps'] == '/ˈ%sː/' % w0 and w['pos'] == 'n', w)
    t = pg.inner_text('#app'); chk('today\u2019s goal counts it (1 / 10) and the row shows "✓ Lug‘atda"', 'Bugungi maqsad: 1 / 10' in t and ev("document.querySelectorAll('#app .yxw')[0].textContent").count('✓ Lug‘atda') == 1)
    pg.click('#app .yxw >> nth=1 >> text=Bilaman'); pg.wait_for_timeout(120); chk('"Bilaman" skips a word for good (no card created, goal not counted) and shows "✓ Bilaman"', exp[1] in ev("S.ie.rmk") and not any(x['w'] == exp[1] for x in ev("S.ie.words")) and ev("rmDoneToday()" .replace('rm', 'yx')) == 1 and 'Bilaman' in ev("document.querySelectorAll('#app .yxw')[1].textContent"))
    ev("__req=[]"); pg.click('#app >> text=Hammasini qo‘sh'); pg.wait_for_timeout(200)
    chk('"Hammasini qo‘sh" adds the remaining 8 at once', len(ev("S.ie.words")) == 1 + 1 + 8 and ev("yxDoneToday()") == 9 and any('8 ta so‘z' in x for x in ev("__t")))
    t = pg.inner_text('#app'); chk('the finished pack says "🎉 Bugungi paket tugadi!" and offers more words and a test', '🎉 Bugungi paket tugadi!' in t and 'Yana 10 ta so‘z' in t and '🧪 Test' in t)
    pg.click('#app >> text=kuniga 5'); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('the daily goal can be 5, 10, 15 or 20; reaching it shows "✓ bajarildi" and a streak of 1 day', ev("S.ie.rmg") == 5 and 'Bugungi maqsad: 9 / 5' in t and '✓ bajarildi' in t and '🔥 1 kun' in t)
    ev("__req=[]"); ev("()=>{tab='e';IVW='y';KS.sec='l';render()}"); pg.wait_for_timeout(100); chk('re-opening the screen keeps the same pack and asks the AI nothing', len([r for r in ev("__req") if r.get('kind') == 'pack']) == 0 and '🎉 Bugungi paket tugadi!' in pg.inner_text('#app'))
    # ---------- test ----------
    pg.click('#app >> text=🧪 Test'); pg.wait_for_timeout(150); t = pg.inner_text('#app')
    chk('the test is built from today\u2019s added words: 9 questions with 4 meanings each', '🧪 Bugungi so‘zlar testi' in t and ev("YX.qz.q.length") == 9 and all(len(q['opts']) == 4 and q['c'] in q['opts'] for q in ev("YX.qz.q")))
    for i in range(9):
        q = ev("YX.qz.q[YX.qz.i]"); idx = q['opts'].index(q['c']) if i != 0 else (q['opts'].index(q['c']) + 1) % 4
        ev("(i)=>yxQzAns(i)", idx); pg.click('#app .goal >> text=/Keyingisi|Natijani ko‘rish/'); pg.wait_for_timeout(40)
    t = pg.inner_text('#app'); bad = ev("YX.qz.bad")
    chk('the result is 8 / 9; the word answered wrongly goes back to the start of the spaced repetition (box 0, due today)', '8 / 9' in t and len(bad) == 1 and ev("(id)=>{const x=S.ie.words.find(y=>y.id===id);return [x.box,x.due===dk()]}", bad[0]) == [0, True] and 'qayta takrorlashga' in t)
    pg.click('#app >> text=Yopish'); pg.wait_for_timeout(60)
    ev("()=>{S.ie.rmp.added=['x1','x2'];YX.qz=null;render()}"); ev("yxQzStart()"); chk('a test needs at least 4 words added today (otherwise a clear message)', any('kamida 4 ta' in x for x in ev("__t")) and ev("YX.qz") is None)
    # ---------- kunlar o'tishi ----------
    pg.clock.set_system_time('2026-11-04T10:00:00'); ev("()=>{__req=[];render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('next day: yesterday\u2019s pack has expired (a new "Bugungi … tayyorla" button), the goal is 0 / 5 and yesterday\u2019s streak is still alive (1 day)', 'Bugungi maqsad: 0 / 5' in t and 'Bugungi 5 ta so‘zni tayyorla' in t and '🔥 1 kun' in t and '🎉' not in t)
    pg.clock.set_system_time('2026-11-07T10:00:00'); ev("render()"); pg.wait_for_timeout(80); chk('after missing days the streak starts again (no 🔥 badge)', '🔥' not in pg.inner_text('#app'))
    pg.clock.set_system_time('2026-11-03T10:00:00')
    # ---------- AI kamchiliklari ----------
    ev("()=>{S.ie.words=[];S.ie.rmk=[];S.ie.rmd={};S.ie.rmp=null;S.ie.rms='g2';S.ie.rmg=10;window.__omit=YX.data.g2[2];__req=[];render()}"); pg.wait_for_timeout(80); pg.click('#app >> text=Bugungi 10 ta so‘zni tayyorla'); pg.wait_for_timeout(500)
    t = pg.inner_text('#app'); chk('if the AI skips a word, that word says so and can still be added without a meaning', 'AI bu so‘z uchun kartochka yozmadi' in t and 'Ma‘nosiz qo‘shish' in t)
    pg.click('#app .yxw >> text=Ma‘nosiz qo‘shish'); pg.wait_for_timeout(120); chk('adding it works (a word card with no meaning)', len(ev("S.ie.words")) == 1 and ev("S.ie.words[0].u") == '' and ev("S.ie.words[0].w") == ev("YX.data.g2[2]"))
    ev("()=>{S.ie.words=[];S.ie.rmk=[];S.ie.rmd={};S.ie.rmp=null;S.ie.rmg=20;window.__omit='';window.__failAt=2;__req=[];render()}"); pg.wait_for_timeout(80); pg.click('#app >> text=Bugungi 20 ta so‘zni tayyorla'); pg.wait_for_timeout(700)
    chk('a 20-word goal needs 2 requests; if the second fails, the first 10 words are kept and the error is shown', len([r for r in ev("__req") if r.get('kind') == 'pack']) == 2 and ev("S.ie.rmp.words.length") == 10 and 'Tarmoq xatosi' in pg.inner_text('#app'))
    ev("window.__failAt=0")
    # ---------- mavzuli 8+ ----------
    ev("()=>{S.ie.words=[];S.ie.rmk=[];S.ie.rmd={};S.ie.rmp=null;S.ie.rms='top';S.ie.rmo='';S.ie.rmg=10;__req=[];render()}"); pg.wait_for_timeout(80); t = pg.inner_text('#app')
    chk('in the 8+ stage a topic chooser with 18 topics appears', ev("document.querySelectorAll('#app .rwch')[1].querySelectorAll('button').length") == 19 and 'Atrof-muhit' in t and 'Speaking iboralari' in t)
    pg.click('#app .rwch >> nth=1 >> text=Atrof-muhit'); pg.wait_for_timeout(80); pg.click('#app >> text=Bugungi 10 ta so‘zni tayyorla'); pg.wait_for_timeout(500); rq = [r for r in ev("__req") if r.get('kind') == 'pack']
    chk('choosing a topic gives that topic\u2019s own words and phrases', rq and rq[0]['words'][:3] == ['mitigate', 'carbon footprint', 'renewable energy'], rq[0]['words'] if rq else None)
    pg.click('#app .yxw >> nth=1 >> text=Lug‘atga qo‘shish'); pg.wait_for_timeout(120); chk('a phrase is stored as a chunk (k = c)', ev("S.ie.words[0].w") == 'carbon footprint' and ev("S.ie.words[0].k") == 'c')
    # ---------- daraja aniqlash ----------
    ev("()=>{S.ie.words=[];S.ie.rmk=[];S.ie.rmp=null;S.ie.rms='auto';YX.qz=null;render()}"); pg.wait_for_timeout(80); pg.click('#app >> text=Lug‘at darajamni aniqlash'); pg.wait_for_timeout(100)
    its = ev("YX.pl.items"); cnt = {k: len([x for x in its if x['k'] == k]) for k in ['g1', 'g2', 'g3', 'g4', 'aw', 'top']}
    chk('the placement test shows 44 single words: 4 + 8 + 8 + 8 + 8 + 8, all different, none containing spaces', len(its) == 44 and cnt == {'g1': 4, 'g2': 8, 'g3': 8, 'g4': 8, 'aw': 8, 'top': 8} and len(set(x['w'] for x in its)) == 44 and not any(' ' in x['w'] for x in its), cnt)
    for i in range(44): ev("yxPlAns(1)")
    pg.wait_for_timeout(100); t = pg.inner_text('#app'); T = ev("S.ie.rmt")
    chk('answering "Bilaman" to everything: estimate close to the full 3788 words, 100% on each stage, recommendation = the 8+ stage', 3700 <= T['est'] <= 3800 and T['rec'] == 'top' and '100%' in t and 'Taxminiy so‘z boyligi' in t, T)
    pg.click('#app >> text=Bilganlarimni paketlardan chiqar'); pg.wait_for_timeout(100); chk('the known words can be removed from future packs', len(ev("S.ie.rmk")) == 44)
    ev("()=>{YX.pl=null;S.ie.rmk=[];render()}"); pg.click('#app >> text=Lug‘at darajamni aniqlash'); pg.wait_for_timeout(80)
    for i in range(44): ev("yxPlAns(0)")
    T = ev("S.ie.rmt"); chk('answering "Bilmayman" to everything: estimate 0 and the recommendation is the first stage', T['est'] == 0 and T['rec'] == 'g1', T)
    ev("()=>{S.ie.rms='aw'}"); pg.click('#app >> text=Shu bosqichni tanlash'); pg.wait_for_timeout(80); chk('"Shu bosqichni tanlash" applies the recommendation', ev("S.ie.rms") == 'g1' and ev("YX.pl") is None)
    ev("()=>{render()}"); pg.click('#app >> text=Lug‘at darajamni aniqlash'); pg.wait_for_timeout(60); ev("yxPlAns(1)"); pg.click('#app >> text=Bekor qilish'); pg.wait_for_timeout(60); chk('the placement test can be cancelled', ev("YX.pl") is None)
    # ---------- ro'yxatlar ilova ichida ----------
    ev("()=>{YX={ld:0,err:'',data:null,gen:0,err2:'',pl:null,qz:null};window.__lf=0;const of=window.fetch;window.fetch=async(u,o)=>{if(String(u).includes('ielts-lists'))window.__lf++;return of(u,o)};render()}"); pg.wait_for_timeout(200)
    chk('the word lists are built into the app: the roadmap opens at once and never downloads a separate file', 'Asos 1' in pg.inner_text('#app') and ev("__lf") == 0 and ev("YX.data.g1.length") == 542)
    # ---------- ko'rinish ----------
    ev("()=>{S.ie.words=[];S.ie.rmk=[];S.ie.rmd={};S.ie.rmp=null;S.ie.rms='g1';KS.sec='l';render()}"); pg.click('#app >> text=Bugungi 10 ta so‘zni tayyorla'); pg.wait_for_timeout(500)
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1]}", [ui, th]); pg.wait_for_timeout(60)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('the roadmap does not overflow the phone screen in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
