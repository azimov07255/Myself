# Cambridge so'zlari: shaxsiy fayl import, bulut (soxta xotira), maqola birlashmasi, matn bo'yicha moslik, takrorlash. Soat: 2026-11-09 10:00.
import sys, json, re, os
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
def W(pi, test, no, w, pos, d, u, e): return [pi, test, no, w, pos, d, u, e]
rows = []
n = 0
def add(pi, test, words):
    global n
    for i, (w, pos) in enumerate(words, 1):
        rows.append(W(pi, test, i, w, pos, 'definition of ' + w, 'tarjima ' + w, 'Example with ' + w + '.'))
add(1, 1, [('aquatic', 'adjective'), ('mammal', 'noun'), ('belong to', 'phrase'), ('flipper', 'noun'), ('forelimb', 'noun'), ('whereas', ''), ('species', 'noun'), ('evolve', 'verb')])
add(1, 21, [('propulsion', 'noun'), ('buoyancy', 'noun'), ('graze', 'verb'), ('vegetation', 'noun'), ('endangered', 'adjective'), ('mitigate', 'verb'), ('run out of', 'phrase'), ('catch someone’s attention', 'phrase'), ('species', 'noun')])
add(2, 2, [('preserve', 'verb'), ('evidence', 'noun'), ('inhabitant', 'noun'), ('unique', 'adjective'), ('means', 'noun'), ('conserve', 'verb')])
add(3, 43, [('guard dog', 'noun'), ('livestock', 'noun'), ('predator', 'noun'), ('herd', 'noun'), ('shepherd', 'noun'), ('flock', 'noun')])
add(4, 9, [('tiny', 'adjective'), ('minute', 'adjective')])
DATA = {'v': 1, 'src': 'test', 'p': [{'i': 1, 't': 'Manatees', 's': 'Cambridge IELTS Academic 20', 'ts': [1, 21]}, {'i': 2, 't': 'Frozen Food', 's': 'Cambridge IELTS Academic 19', 'ts': [2]}, {'i': 3, 't': 'Livestock guard dogs', 's': 'Cambridge IELTS Academic 20', 'ts': [43, 77]}, {'i': 4, 't': 'Tiny passage', 's': 'Cambridge IELTS Academic 19', 'ts': [9]}], 'x': {'77': 43}, 'w': rows}
TXT = json.dumps(DATA, ensure_ascii=False, separators=(',', ':'))
TEXT = ('Manatees are aquatic mammals that belong to a group of animals. Their flippers help steering, whereas the tail gives propulsion. '
        'The animals graze on vegetation, and endangered species such as these need protection to mitigate the harm. They often run out of food and catch the attention of scientists. '
        'The study of these animals evolved over many decades, and researchers keep grazing sites under observation to protect the forelimbs of the young. ' * 2)
with Run('cb', when=(2026, 11, 9, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;for(const k of ['trk_cb','trk_bso','trk_swh'])localStorage.removeItem(k);localStorage.setItem('trk_swh','1');S.cb=undefined;CB=null;CBO=false;CBS={v:'p',q:'',bk:'',pi:0,sel:{},txt:'',an:null,lim:40,f:'all',st:'',cl:''};CBR=null;window.__cbUid=undefined;window.__cbStore=undefined;tab='h';BV='j';render()}""")
    pg.wait_for_timeout(100)
    # ---------- fayl
    chk('without a file the section says so and offers to pick the file (and nothing is stored in the app code)', ev("(async()=>{await cbLoad();cbOpen();return CB===null})()") and 'So‘zlar fayli hali yuklanmagan' in pg.inner_text('#cbv') and '📥 Faylni tanlash' in pg.inner_text('#cbv')); ev("cbClose()")
    ok = ev("(t)=>cbImportText(t,false)", TXT); chk('importing the file works: validated, indexed and the status shows “✅ N so‘z, 4 maqola yuklandi”', ok is True and ev("CB.d.w.length") == len(rows) and 'maqola yuklandi' in ev("CBS.st"))
    chk('garbage is refused without touching what is already loaded: not JSON, wrong structure, row of the wrong length', ev("(async()=>{const a=await cbImportText('xx',false),b=await cbImportText('{\"v\":2,\"p\":[],\"w\":[]}',false),c=await cbImportText(JSON.stringify({v:1,p:[{i:1,t:'a',ts:[1]}],w:[[1,1,1]]}),false);return [a,b,c,CB.d.w.length]})()") == [False, False, False, len(rows)])
    ev("CB=null"); chk('the file survives closing the app: it is kept in the phone’s own storage and loaded again', ev("cbLoad()") is True and ev("CB.d.p.length") == 4)
    # indeks
    chk('a full passage = ALL its tests together: Manatees (tests 1 and 21) has 16 unique words (the word “species” in both tests counts once)', ev("CB.byP[1].length") == 16 and len(set(ev("CB.byP[1].map(i=>CB.d.w[i][3])"))) == 16)
    chk('a test that is “the same as test 43” (77) adds nothing of its own but the passage still gets test 43’s words through the alias', ev("CB.byP[3].length") == 6 and ev("CB.byT[77]") is None)
    # korinish
    ev("cbOpen()"); pg.wait_for_timeout(100); t = pg.inner_text('#cbv'); chk('the sections: 📚 Maqolalar, 📋 Matn, 🔁 Takror, ℹ️; the passage list shows title, book, tests and the word count', all(x in t for x in ['📚 Maqolalar', '📋 Matn', '🔁 Takror']) and 'Manatees' in t and 'Cambridge IELTS Academic 20 · 2 ta test' in t and '16 so‘z' in t and '4 ta maqola' in t or '3 ta maqola' in t)
    chk('passages with too few words (Tiny passage, 2 words) still list but cannot match a text; search narrows the list (“frozen”)', ev("(()=>{cbSearch('frozen');return document.querySelectorAll('#cbv .row').length})()") == 1); ev("cbSearch('')")
    ev("cbBook('Cambridge IELTS Academic 19')"); chk('the book filter works (Academic 19 → 2 passages)', ev("document.querySelectorAll('#cbv .row').length") == 2); ev("cbBook('')")
    ev("()=>{CBS.lim=1;cbDraw()}"); chk('long lists show 40 at a time with “Yana ko‘rsat”', 'Yana ko‘rsat' in pg.inner_text('#cbv')); ev("()=>{CBS.lim=40;cbDraw()}")
    ev("cbPass(1)"); pg.wait_for_timeout(80); t = pg.inner_text('#cbv'); chk('opening a passage lists its 16 words with Uzbek translation (definition and example in a fold-out) and a counter button', 'Manatees' in t and 'testlar: 1, 21' in t and 'tarjima aquatic' in t and 'tarjima propulsion' in t and '＋ Tanlanganlarni qo‘sh (0)' in t)
    ev("()=>{cbSel(0);cbSel(1);cbSel(2)}"); chk('ticking words updates the button (3)', '(3)' in pg.inner_text('#cbv'))
    ev("cbAddSel()"); A = ev("S.cb"); chk('adding puts the words into the SEPARATE Cambridge deck: only keys (test:number) and the review state are saved — no words, translations or definitions in the app data', sorted(A['w'].keys()) == ['1:1', '1:2', '1:3'] and all(set(v.keys()) <= {'b', 'due', 'a', 'l'} for v in A['w'].values()) and 'aquatic' not in json.dumps(A) and 'tarjima' not in json.dumps(A) and A['dd']['2026-11-09'] == 3, A)
    chk('the existing vocabulary deck (Lug‘at) is untouched', ev("(S.ie.words||[]).length") == 0 or ev("!(S.ie.words||[]).some(w=>w.src==='cam')"))
    ev("cbDraw()"); t = pg.inner_text('#cbv'); chk('added words show “✅ to‘plamda” and cannot be ticked again; the filter “Qo‘shilmaganlar” hides them', '✅ to‘plamda' in t and ev("document.querySelectorAll('#cbv input[type=checkbox][disabled]').length") == 3); ev("()=>{CBS.f='new';cbDraw()}"); chk('…', ev("document.querySelectorAll('#cbv input[type=checkbox]').length") == 13); ev("()=>{CBS.f='all';cbDraw()}")
    ev("()=>{cbS().lim=2;window.__cm='';window.confirm=m=>{window.__cm=m;return false}}"); ev("()=>{cbSel(3);cbSel(4);cbAddSel()}"); chk('the daily limit: beyond it the app asks first (“Bugungi chegara 2 ta…”); answering no adds nothing', 'Bugungi chegara 2 ta' in ev("__cm") and ev("Object.keys(S.cb.w).length") == 3)
    ev("()=>{window.confirm=()=>true;cbAddSel()}"); chk('answering yes adds them anyway (5 words in the deck)', ev("Object.keys(S.cb.w).length") == 5); ev("cbS().lim=20")
    ev("cbRemove('1:1')"); chk('a word can be removed from the deck, with ↩︎ Bekor qilish', ev("!S.cb.w['1:1']") and 'to‘plamdan olib tashlandi' in pg.inner_text('#udb')); ev("udDo()"); chk('…and restored', ev("!!S.cb.w['1:1']"))
    # moslik
    chk('word forms are matched by a simple stem: mitigating = mitigate, studies = study, running = run, flippers = flipper, belongs to = belong to', ev("cbStem('mitigating')") == ev("cbStem('mitigate')") and ev("cbStem('mitigated')") == ev("cbStem('mitigate')") and ev("cbStem('studies')") == ev("cbStem('study')") and ev("cbStem('running')") == ev("cbStem('run')") and ev("cbStem('flippers')") == ev("cbStem('flipper')"))
    ev("(t)=>{CBS.txt=t;cbV('t')}", TEXT); ev("cbRun()"); pg.wait_for_timeout(100); an = ev("(()=>{const a=CBS.an;return {top:a.sc[0],n:a.sc.length,nt:a.nt}})()")
    chk('pasting a full passage finds the right one: Manatees first, with words from BOTH of its tests counted together', an['top']['pi'] == 1 and an['top']['f'] >= 11 and an['top']['n'] == 16, an)
    f = ev("CB.byP[1].filter(i=>CBS.an.F[i]).map(i=>CB.d.w[i][1]+':'+CB.d.w[i][3])"); chk('…words from test 1 (aquatic, belong to, flipper, whereas) and from test 21 (propulsion, graze, vegetation, mitigate, run out of, catch someone’s attention) are both found; the gap word “someone’s” matches “the”', all(x in f for x in ['1:aquatic', '1:belong to', '1:flipper', '1:whereas', '21:propulsion', '21:graze', '21:vegetation', '21:mitigate', '21:run out of', '21:catch someone’s attention']), f)
    t = pg.inner_text('#cbv'); chk('the result lists the best passages with “found/total · %”, the words marked “matnda bor”, and the missing ones under “Matnda topilmaganlar (N)”', 'Manatees' in t and '%' in t and 'matnda bor' in t and 'Matnda topilmaganlar' in t)
    chk('the pasted text is highlighted (found words in <mark>) and any HTML in it is shown as plain text', ev("(()=>{const h=cbHl(cbAnalyze('<img src=x onerror=1> aquatic mammals belong to flippers. '+'x '.repeat(5)),'<img src=x onerror=1> aquatic mammals belong to flippers. '+'x '.repeat(5));return h.includes('<mark>aquatic</mark>')&&!h.includes('<img')})()"))
    ev("()=>{const i=CB.byP[1].filter(i=>CBS.an.F[i]);cbSelAll(i)}"); ev("cbDraw()"); chk('“Topilganlarni tanla” ticks every found word that is not yet in the deck', ev("Object.keys(CBS.sel).length") >= 8)
    chk('the pasted text is NOT saved anywhere (not in the app data, not after closing)', 'Manatees are aquatic' not in ev("JSON.stringify(S)") and (ev("(()=>{cbClose();return CBS.txt})()") == '') and ev("CBS.an") is None)
    ev("cbOpen('t')"); ev("(t)=>{CBS.txt=t;cbDraw();cbRun()}", 'too short'); chk('a short text is refused with a hint to paste the whole passage', 'Butun maqolani joylang' in ev("CBS.st") or 'juda qisqa' in ev("CBS.st"))
    ev("(t)=>{CBS.txt=t;cbDraw();cbRun()}", 'The weather is nice today and we walk in the park near the lake with friends and family on a sunny afternoon. ' * 3); chk('a text unlike any passage says that no passage matched', ev("CBS.an.sc.length") == 0 and 'Mos maqola topilmadi' in pg.inner_text('#cbv')); ev("cbClose()")
    # takrorlash
    ev("()=>{S.cb.w={'1:1':{b:0,due:'2026-11-09',a:'2026-11-09'},'1:2':{b:0,due:'2026-11-09',a:'2026-11-09'},'1:3':{b:2,due:'2026-11-12',a:'2026-11-09'}}}"); chk('words due today are counted (2 of 3; the third is due on the 12th)', ev("cbDue()") == ['1:1', '1:2'])
    ev("()=>{tab='h';BV='j';render()}"); pg.wait_for_timeout(100); chk('Bugun shows “📚 Cambridge takror: 2 ta so‘z” and opens the review', 'Cambridge takror: 2 ta so‘z' in pg.inner_text('#app')); ev("()=>{[...document.querySelectorAll('#app button.row')].find(b=>b.textContent.includes('Cambridge takror')).click()}"); pg.wait_for_timeout(150); chk('…which starts on the review tab', ev("CBS.v") == 'r' and ev("!!document.getElementById('cbv')"))
    ev("cbRStart()"); pg.wait_for_timeout(80); t = pg.inner_text('#cbv'); chk('the card shows only the word first (1 / 2); “Ko‘rsatish” reveals the translation, definition and example with three answer buttons', '1 / 2' in t and 'aquatic' in t and 'tarjima aquatic' not in t); ev("cbRShow()"); t = pg.inner_text('#cbv'); chk('…revealed', 'tarjima aquatic' in t and 'definition of aquatic' in t and '❌ Bilmayman' in t and '🟡 Qiyin' in t and '✅ Bilaman' in t)
    ev("cbRAns('g')"); e1 = ev("S.cb.w['1:1']"); chk('“Bilaman” moves the word up one box and schedules it later (box 1 → due in 2 days: 11 Nov)', e1['b'] == 1 and e1['due'] == '2026-11-11' and e1['l'] == '2026-11-09')
    ev("cbRShow()"); ev("cbRAns('x')"); e2 = ev("S.cb.w['1:2']"); chk('“Bilmayman” resets the box and brings it back tomorrow', e2['b'] == 0 and e2['due'] == '2026-11-10'); t = pg.inner_text('#cbv'); chk('the session ends with a summary', '🎉 Tugadi' in t and 'Bilaman: 1' in t and 'Bilmayman: 1' in t)
    ev("()=>{S.cb.w['1:3'].b=2;S.cb.w['1:3'].due='2026-11-09'}"); ev("()=>{CBR=null;cbRStart()}"); ev("cbRShow()"); ev("cbRAns('q')"); chk('“Qiyin” goes one box down and returns in 2 days (box 2 → 1)', ev("S.cb.w['1:3'].b") == 1 and ev("S.cb.w['1:3'].due") == '2026-11-11')
    ev("()=>{for(let i=0;i<6;i++){S.cb.w['1:3'].due='2026-11-09';cbAns('1:3','g')}}"); chk('the box never goes above 6 (mastered words come back every 60 days)', ev("S.cb.w['1:3'].b") == 6 and ev("S.cb.w['1:3'].due") == '2027-01-08')
    ev("()=>{cbClose();uiS('trk_cb','0');S.cb.w={'1:1':{b:0,due:'2026-11-09',a:'2026-11-09'}};tab='h';render()}"); pg.wait_for_timeout(80); chk('the whole section can be switched off in Settings (no Bugun row, no card)', 'Cambridge takror' not in pg.inner_text('#app') and ev("cbEntry()") == '' and ev("cbRow()") == ''); ev("uiS('trk_cb','1')")
    # IELTS lug'at
    ev("()=>{tab='e';IVW='l';render()}"); pg.wait_for_timeout(100); chk('IELTS → Lug‘at starts with the “📚 Cambridge so‘zlari” card (count and “Ochish”)', '📚 Cambridge so‘zlari' in pg.inner_text('#app') and 'Ochish' in pg.inner_text('#app'))
    # bulut
    ev("""()=>{window.__cbUid='user-1';window.__cbLog=[];window.__cbBlob=null;window.__cbFail='';window.__cbStore={from:b=>({upload:async(p,blob,o)=>{window.__cbLog.push([b,p,o&&o.upsert]);if(window.__cbFail)return{error:{message:window.__cbFail}};window.__cbBlob=await blob.text();return{error:null}},download:async p=>{window.__cbLog.push(['dl',b,p]);if(!window.__cbBlob)return{data:null,error:{message:'Object not found'}};return{data:new Blob([window.__cbBlob]),error:null}}})}}""")
    ev("(t)=>cbImportText(t)", TXT); pg.wait_for_timeout(100); lg = ev("__cbLog")
    chk('importing also uploads to the private cloud bucket “cambridge” at <your user id>/sozlar.json (upsert), and says so', lg[0][0] == 'cambridge' and lg[0][1] == 'user-1/sozlar.json' and lg[0][2] is True and 'Bulutda saqlandi' in ev("CBS.cl") and len(ev("__cbBlob")) == len(TXT))
    ev("CB=null;cbIdbDel()"); pg.wait_for_timeout(150); ev("cbOpen()"); pg.wait_for_timeout(400); chk('on another device (nothing stored locally) opening the section downloads the file from the cloud automatically', ev("!!CB") and ev("CB.d.w.length") == len(rows) and 'Bulutdan yuklandi' in ev("CBS.cl"), ev("CBS.cl")); ev("cbClose()")
    ev("()=>{CB=null;window.__cbBlob=null;window.__cbFail=''}"); ev("cbIdbDel()"); pg.wait_for_timeout(100); ev("cbDown()"); pg.wait_for_timeout(200); chk('a missing cloud file gives a clear message (not a crash)', 'Bulutdan olinmadi' in ev("CBS.cl") and 'topilmadi' in ev("CBS.cl").lower() or 'not found' in ev("CBS.cl").lower())
    ev("window.__cbFail='Bucket not found'"); ev("(t)=>cbImportText(t)", TXT); pg.wait_for_timeout(200); chk('if the cloud step fails (SQL not run yet) the file is still usable on this phone and the message points to the SQL', ev("!!CB") and 'Bulutga yuklanmadi' in ev("CBS.cl") and 'SQL' in ev("CBS.cl") and 'Bucket not found' in ev("CBS.cl"))
    ev("()=>{window.__cbUid=undefined}"); ev("cbUp()"); pg.wait_for_timeout(100); chk('without a signed-in account the cloud step explains that', 'Hisobga kirilmagan' in ev("CBS.cl")); ev("cbClose()")
    ev("cbOpen('s')"); pg.wait_for_timeout(100); chk('the ℹ️ tab shows the deck statistics, the daily limit choices, the file status and the privacy note', all(x in pg.inner_text('#cbv') for x in ['To‘plamda', 'Kuniga qo‘shish chegarasi', 'Qurilmada: ', 'Maxfiylik va bulut sozlash'])); ev("(async()=>{await cbDelLocal()})()"); pg.wait_for_timeout(200); chk('“Qurilmadagi nusxani o‘chirish” removes only the local file; your deck stays', ev("!CB") and ev("Object.keys(S.cb.w).length") >= 0); ev("cbClose()")
    # maxfiylik
    html = open('/mnt/user-data/outputs/tracker/index.html', encoding='utf-8').read(); real = json.load(open('/mnt/user-data/outputs/cambridge-sozlar.json', encoding='utf-8'))
    longs = [w[i] for w in real['w'] for i in (5, 6, 7) if len(w[i]) > 25]
    chk('PRIVACY: none of the file’s definitions, Uzbek translations or example sentences (%d long strings from all 7,569 entries) is inside the built app (at most 3 generic sentences may coincide with the app’s own texts)' % len(longs), len([x for x in longs if x in html]) <= 3, [x for x in longs if x in html][:3])
    chk('…and the data file is not in the app package list (friends version / GitHub files)', 'cambridge' not in open('/mnt/user-data/outputs/tools/make_zips.py', encoding='utf-8').read().lower() and not os.path.exists('/mnt/user-data/outputs/tracker/cambridge-sozlar.json'))
    sql = open('/mnt/user-data/outputs/server-setup/cambridge-storage.sql', encoding='utf-8').read(); chk('the SQL creates a PRIVATE bucket and four policies that restrict every operation to the user’s own folder', "'cambridge', 'cambridge', false" in sql and sql.count('create policy') == 4 and sql.count('auth.uid()::text') >= 5)
    # haqiqiy fayl
    ok = ev("(t)=>{const d=JSON.parse(t);const s=performance.now();const ok=cbSetData(d);return [ok,CB.d.p.length,CB.byP[Object.values(CB.P).find(p=>p.t==='Manatees').i].length,Math.round(performance.now()-s)]}", open('/mnt/user-data/outputs/cambridge-sozlar.json', encoding='utf-8').read())
    chk('YOUR REAL FILE loads and indexes: 144 passages, Manatees (tests 1 + 21) = 94 unique words, and it takes well under 2 seconds', ok[0] and ok[1] == 144 and ok[2] == 94 and ok[3] < 2000, ok)
    sample = ' '.join(r[7] for r in real['w'] if r[1] in (1, 21)) * 1
    r2 = ev("(t)=>{const s=performance.now();const a=cbAnalyze(t);return {top:a.sc[0]&&CB.P[a.sc[0].pi].t,f:a.sc[0]&&a.sc[0].f,n:a.sc[0]&&a.sc[0].n,ms:Math.round(performance.now()-s),nt:a.nt}}", sample + ' ' + sample)
    chk('a long text made from the Manatees examples is recognised as “Manatees” by the real file in well under 3 seconds', r2['top'] == 'Manatees' and r2['f'] >= 60 and r2['ms'] < 3000, r2)
    bad = []
    ev("(t)=>{cbSetData(JSON.parse(t));S.cb.w={'1:1':{b:0,due:'2026-11-09',a:'2026-11-09'}}}", TXT)
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];CBS={v:'p',q:'',bk:'',pi:1,sel:{},txt:'',an:null,lim:40,f:'all',st:'Uzun holat xabari '.repeat(4),cl:''};CBO=true;cbDraw()}", [ui, th]); pg.wait_for_timeout(60); o1 = ev("document.querySelector('#cbv .asc').scrollWidth<=document.querySelector('#cbv .asc').clientWidth+1")
            ev("cbPass(1)"); o2 = ev("document.querySelector('#cbv .asc').scrollWidth<=document.querySelector('#cbv .asc').clientWidth+1"); ev("(t)=>{CBS.txt=t;cbV('t');cbRun()}", TEXT); o3 = ev("document.querySelector('#cbv .asc').scrollWidth<=document.querySelector('#cbv .asc').clientWidth+1"); ev("()=>{CBR=null;cbV('r')}"); o4 = ev("document.querySelector('#cbv .asc').scrollWidth<=document.querySelector('#cbv .asc').clientWidth+1"); ev("cbClose()")
            if not (o1 and o2 and o3 and o4): bad.append(ui + th)
    chk('the passage list, word list, text analysis and review fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
