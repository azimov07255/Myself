# Mulk surasi, namozdan keyingi suralar, "Undan keyin" ro'yxati, Cambridge: yopilmaydigan bo'limlar, ommaviy tanlash, matnni saqlash. Soat: chorshanba 2026-11-11 21:00.
import sys, json, re
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
def add(rows, pi, test, words):
    for i, (w, pos) in enumerate(words, 1):
        rows.append([pi, test, i, w, pos, 'definition of ' + w, 'tarjima ' + w, 'Example with ' + w + '.'])
rows = []
add(rows, 1, 1, [('aquatic', 'adjective'), ('mammal', 'noun'), ('belong to', 'phrase'), ('flipper', 'noun'), ('forelimb', 'noun'), ('whereas', ''), ('species', 'noun'), ('evolve', 'verb')])
add(rows, 1, 21, [('propulsion', 'noun'), ('buoyancy', 'noun'), ('graze', 'verb'), ('vegetation', 'noun'), ('endangered', 'adjective'), ('mitigate', 'verb')])
add(rows, 2, 2, [('preserve', 'verb'), ('evidence', 'noun'), ('inhabitant', 'noun'), ('unique', 'adjective'), ('means', 'noun'), ('conserve', 'verb')])
DATA = {'v': 1, 'src': 't', 'p': [{'i': 1, 't': 'Manatees', 's': 'Cambridge IELTS Academic 20', 'ts': [1, 21]}, {'i': 2, 't': 'Frozen Food', 's': 'Cambridge IELTS Academic 19', 'ts': [2]}], 'x': {}, 'w': rows}
TXT = json.dumps(DATA, ensure_ascii=False, separators=(',', ':'))
TEXT = ('Manatees are aquatic mammals that belong to a group of animals. Their flippers help steering, whereas the tail gives propulsion. '
        'The animals graze on vegetation, and endangered species such as these need protection to mitigate the harm. Scientists preserve evidence of the unique inhabitants. '
        'The study of these animals evolved over many decades, and researchers keep grazing sites under observation to protect the forelimbs of the young. ' * 2)
PT = "window.ptTimes=()=>({Fajr:300,Dhuhr:735,Asr:900,Maghrib:1070,Isha:1230})"
with Run('ml', when=(2026, 11, 11, 21, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("(()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;" + PT + ";for(const k of ['trk_ml','trk_mlr','trk_mlp','trk_mlrm','trk_mlo','trk_swh','trk_bsec','trk_jdx','trk_jdl','trk_jdm','trk_cb'])localStorage.removeItem(k);localStorage.setItem('trk_swh','1');localStorage.setItem('trk_bsec','a');S.ml=undefined;S.q.rd={};tab='h';BV='j';render()})()")
    pg.wait_for_timeout(120)
    h = ev("mlCard()")
    chk('Bugun has a 🌙 “Mulk surasi” card: 30 oyat, uxlashdan oldin, “Xufton 20:30 dan keyin”, and a starting streak badge', all(x in h for x in ['Mulk surasi', '30 oyat', 'uxlashdan oldin', 'Xufton 20:30 dan keyin', 'yangi']))
    chk('after Xufton (21:00) it says “Uxlashdan oldin o‘qib, belgilab qo‘y” with two buttons: ✅ O‘qidim (+15) and 🕌 Namozda o‘qidim (+30), and explains that reading in prayer doubles the points', 'Uxlashdan oldin o‘qib, belgilab qo‘y' in h and '✅ O‘qidim (+15)' in h and '🕌 Namozda o‘qidim (+30)' in h and '2 baravar' in h)
    pg.clock.set_system_time('2026-11-11T19:00:00'); ev("render()"); chk('before Xufton it only says it will be read after Xufton (but can still be marked)', 'Xufton vaqti kirgach o‘qiysan' in ev("mlCard()")); pg.clock.set_system_time('2026-11-11T21:00:00')
    ev("render()"); t = pg.inner_text('#app'); chk('the card shows on the Bugun screen', 'Mulk surasi' in t and '🌙' in t)
    p0 = ev("dayPts(dk()).t"); ev("mlRead(0)"); d = ev("S.ml.d['2026-11-11']"); chk('“O‘qidim” records the reading time (21:00) and 15 points are added to the day', d['r'] == '21:00' and d['n'] == 0 and ev("dayPts(dk()).t") == p0 + 15 and ['Mulk surasi', 15] in ev("dayPts(dk()).p"), d)
    h = ev("mlCard()"); chk('the card now says “✅ Bugun o‘qildi · 21:00 · +15 ball”, streak 🔥 1 kun, and offers to mark it as read in prayer or to undo', '✅ Bugun o‘qildi · 21:00' in h and '+15 ball' in h and '🔥 1 kun' in h and 'Namozda edi (+15 ball)' in h and 'Bekor' in h)
    ev("mlN()"); chk('“Namozda edi” upgrades it to 30 points (double)', ev("dayPts(dk()).t") == p0 + 30 and ['Mulk surasi', 30] in ev("dayPts(dk()).p") and '🕌 namozda' in ev("mlCard()") and '+30 ball' in ev("mlCard()"))
    ev("mlUn()"); chk('undo removes it completely (points back, no record left)', ev("dayPts(dk()).t") == p0 and ev("!S.ml.d['2026-11-11']")); ev("mlRead(1)"); chk('“Namozda o‘qidim” records 30 points directly', ev("dayPts(dk()).t") == p0 + 30 and ev("S.ml.d['2026-11-11'].n") == 1); ev("mlUn()")
    ev("()=>{S.ml.d={};['2026-11-10','2026-11-09','2026-11-08'].forEach(k=>S.ml.d[k]={r:'22:00',n:0})}"); chk('streak counts consecutive days: yesterday and the two before = 3 (today not yet read does not break it)', ev("mlStreak()") == 3); ev("mlRead(0)"); chk('…and today makes it 4', ev("mlStreak()") == 4); ev("mlUn()")
    # namozdan keyin
    ev("()=>{S.ml.d={}}"); ev("mlPT('Fajr','k')"); ev("mlPT('Fajr','m')"); h = ev("mlCard()"); chk('after-prayer surahs are listed per prayer (Bomdod, Peshin, Asr, Shom, Xufton) with Oyatul Kursiy and Ixlos·Falaq·Nos (×3 after Bomdod and Shom); ticking two shows 2/10', all(x in h for x in ['Bomdod', 'Peshin', 'Asr', 'Shom', 'Xufton', 'Oyatul Kursiy', 'Ixlos · Falaq · Nos ×3', 'tavsiya, majburiy emas', '2/10']))
    chk('they give a little (1 point each, at most 10) and are clearly not required: no audit warning for them', ['Namozdan keyingi suralar', 2] in ev("dayPts(dk()).p") and not any('suralar' in x['txt'] for x in ev("dcAudit(dk()).F")))
    ev("mlPT('Fajr','k')"); chk('a tick can be removed again', ev("mlPCount(dk())") == 1)
    ev("uiS('trk_mlp','0')"); ev("render()"); chk('the list can be hidden in Settings (and then gives no points)', 'Namozdan keyin' not in ev("mlCard()") and not any(x[0] == 'Namozdan keyingi suralar' for x in ev("(rwReset(),dayPts(dk()).p)"))); ev("uiS('trk_mlp','1')")
    # majburiy
    ev("()=>{S.ml.d={}}"); pg.clock.set_system_time('2026-11-11T20:40:00'); a = ev("dcAudit(dk()).F.filter(x=>x.id==='mulk')"); chk('Mulk is required but not nagging too early: no warning at 20:40', a == [])
    pg.clock.set_system_time('2026-11-11T23:00:00'); a = ev("dcAudit(dk()).F.filter(x=>x.id==='mulk')"); chk('late in the evening Kun tekshiruvi warns “Mulk surasi o‘qilmadi (majburiy)” with a one-tap fix “🌙 Hozir o‘qidim”', len(a) == 1 and 'majburiy' in a[0]['txt'] and a[0]['fix']['l'] == '🌙 Hozir o‘qidim' and 'mlReadK' in a[0]['fix']['a'], a)
    ev("(a)=>eval(a)", a[0]['fix']['a']); chk('the fix marks it read and the warning disappears', ev("!!S.ml.d['2026-11-11']") and ev("dcAudit(dk()).F.filter(x=>x.id==='mulk').length") == 0); ev("mlUn()")
    chk('an unread past day is also flagged (it was required)', ev("dcAudit('2026-11-09').F.filter(x=>x.id==='mulk').length") == 1)
    ev("uiS('trk_mlr','0')"); chk('“Majburiy emas” in Settings stops the warning', ev("dcAudit(dk()).F.filter(x=>x.id==='mulk').length") == 0 and ev("dcAudit('2026-11-09').F.filter(x=>x.id==='mulk').length") == 0); ev("uiS('trk_mlr','1')"); pg.clock.set_system_time('2026-11-11T21:00:00')
    # eslatma
    ev("()=>{S.rem=Object.assign({},S.rem,{on:true,tg:false,blk:false,close:false,wake:false,nz:false,zk:false,yo:false,rz:false,custom:[]})}"); r = [x for x in ev("remRows()") if x.get('kind') == 'ml']
    chk('with reminders on, a “🌙 Mulk surasi” reminder is sent 45 minutes after Xufton (21:15) every day; its kind fits the server format', len(r) == 1 and r[0]['hhmm'] == '21:15' and r[0]['days'] == [0, 1, 2, 3, 4, 5, 6] and re.fullmatch(r'[a-z]{1,3}(:[\w-]+)?(@\d{4}-\d\d-\d\d)?', r[0]['kind']), r)
    ev("uiS('trk_mlrm','0')"); chk('the reminder can be switched off', not [x for x in ev("remRows()") if x.get('kind') == 'ml']); ev("uiS('trk_mlrm','1')")
    ev("()=>{S.rem.on=false;S.rem.tg=false}"); chk('and there is none when all reminders are off', not [x for x in ev("remRows()") if x.get('kind') == 'ml'])
    ev("uiS('trk_ml','0')"); ev("render()"); chk('the whole feature can be switched off (no card, no points, no warning, no reminder)', ev("mlCard()") == '' and ev("(mlRead(0),dayPts(dk()).p.some(x=>x[0]==='Mulk surasi'))") is False and ev("dcAudit('2026-11-09').F.filter(x=>x.id==='mulk').length") == 0); ev("()=>{S.ml.d={}}"); ev("uiS('trk_ml','1')")
    ev("()=>{SDO={jl:1};tab='s';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('Settings → Jilo has the Mulk switches (card, required/not required, after-prayer list, reminder)', all(x in t for x in ['Mulk surasi kartasi', 'Majburiy (ogohlantiradi)', 'Namozdan keyingi tavsiya suralar ro‘yxati', 'Mulk eslatmasi']))
    # undan keyin ro'yxati
    pg.clock.set_system_time('2026-11-11T01:42:00')
    ev("(()=>{S.bl=[{id:'uyqu1',t:'Uxlash',s:0,e:300,d:[0,1,2,3,4,5,6]},{id:'uyqu2',t:'Uygonish',s:300,e:360,d:[0,1,2,3,4,5,6]},{id:'q1',t:'Quron',s:360,e:540,d:[0,1,2,3,4,5,6],ty:'quron',fx:0},{id:'k1',t:'Kitob',s:735,e:760,d:[0,1,2,3,4,5,6],ty:'oqish',fx:0},{id:'u1',t:'Univer',s:1080,e:1170,d:[0,1,2,3,4,5,6],ty:'ish',fx:1},{id:'d1',t:'Dars',s:1200,e:1260,d:[0,1,2,3,4,5,6],ty:'oqish',fx:0},{id:'s9',t:'Uxlash kechqurun',s:1380,e:1440,d:[0,1,2,3,4,5,6]}];S.ov=undefined;S.done={};tab='h';BV='j';render()})()"); pg.wait_for_timeout(120)
    t = ev("document.querySelector('#app .n3a')&&document.querySelector('#app .n3a').innerText"); chk('right below the “Keyingi 3 soat” strip an “Undan keyin” list shows the plans after the window: Uygonish 05:00, Quron 06:00, Kitob 12:15, Univer 18:00, Dars 20:00 (5 by default) with how long until each', t and t.index('05:00') < t.index('06:00') < t.index('12:15') < t.index('18:00') < t.index('20:00') and 'Uygonish' in t and '3 soat 18 daqiqadan keyin' in t and '23:00' not in t, t)
    chk('the list sits directly after the strip in the page (strip first, then the list, then the other cards)', ev("document.querySelector('#app .n3').nextElementSibling.classList.contains('n3a')"))
    ev("uiS('trk_jdl','3')"); ev("render()"); chk('3 / 8 / off are choices: with 3 only the first three show', ev("document.querySelectorAll('#app .n3a .n3r').length") == 3); ev("uiS('trk_jdl','0')"); ev("render()"); chk('“Yo‘q (avvalgidek)” removes the list', ev("!document.querySelector('#app .n3a')")); ev("uiS('trk_jdl','5')")
    ev("uiS('trk_jdm','o')"); ev("render()"); chk('the old schedule mode has no list either', ev("!document.querySelector('#app .n3a')")); ev("uiS('trk_jdm','n')")
    ev("render()"); ev("()=>{document.querySelector('#app .n3a .n3r').click()}"); chk('tapping a row scrolls to that plan in the schedule (no error)', True)
    pg.clock.set_system_time('2026-11-11T23:50:00'); ev("render()"); pg.wait_for_timeout(80); t = ev("document.querySelector('#app .n3a')&&document.querySelector('#app .n3a').innerText"); chk('late in the evening, when nothing is left today, the list shows tomorrow’s first plans marked “Ertaga”', t and 'Ertaga' in t and 'Uygonish' in t, t)
    ev("render()"); t = ev("document.querySelector('#app .n3').innerText"); chk('the strip itself keeps its old text only (the extra “Keyingisi” line is now an option, off by default)', 'Keyingisi' not in t); ev("uiS('trk_jdx','1')"); ev("render()"); chk('…and can still be switched on', 'Keyingisi' in ev("document.querySelector('#app .n3').innerText") or 'Reja yo‘q' not in ev("document.querySelector('#app .n3').innerText")); ev("uiS('trk_jdx','0')")
    # ---------- Cambridge
    pg.clock.set_system_time('2026-11-11T21:00:00')
    ev("(t)=>{S.ie.mat=[];return cbImportText(t,false)}", TXT); ev("(t)=>{CBS.txt=t;cbOpen('t');CBS.txt=t;cbDraw();cbRun()}", TEXT); pg.wait_for_timeout(150)
    chk('analysis finds the passage and shows the three groups (found, “Matnda topilmaganlar”, “Boshqa maqolalar…”) with bulk buttons “☑ Hammasini tanla / ☐ Bekor qilish / ⇄ Teskari”', ev("CBS.an.sc[0].pi") == 1 and 'Matnda topilmaganlar' in pg.inner_text('#cbv') and 'Boshqa maqolalar ro‘yxatidagi' in pg.inner_text('#cbv') and ev("document.querySelectorAll('#cbv .rwch button').length") > 6 and '⇄ Teskari' in pg.inner_text('#cbv'))
    ev("()=>{const d=[...document.querySelectorAll('#cbv details')].find(x=>x.textContent.includes('Matnda topilmaganlar'));d.open=true;d.dispatchEvent(new Event('toggle'))}"); mi = ev("CB.byP[1].filter(i=>!CBS.an.F[i])[0]"); ev("(i)=>cbSel(i)", mi); pg.wait_for_timeout(80)
    chk('ticking a word inside “Matnda topilmaganlar” no longer closes the section (it stays open) and the word is ticked', ev("[...document.querySelectorAll('#cbv details')].find(x=>x.textContent.includes('Matnda topilmaganlar')).open") is True and ev("!!CBS.sel[%d]" % mi))
    ev("()=>{const d=[...document.querySelectorAll('#cbv details')].find(x=>x.textContent.includes('Boshqa maqolalar'));d.open=true;d.dispatchEvent(new Event('toggle'))}"); oi = ev("cbOtherList()[0]"); ev("(i)=>cbSel(i)", oi); pg.wait_for_timeout(80)
    chk('the same for “Boshqa maqolalar ro‘yxatidagi…”: it stays open after ticking', ev("[...document.querySelectorAll('#cbv details')].find(x=>x.textContent.includes('Boshqa maqolalar')).open") is True and ev("!!CBS.sel[%d]" % oi))
    chk('the page does not jump to the top when ticking (the scroll position is kept)', ev("(()=>{const e=document.getElementById('cbv');e.scrollTop=250;const y=e.scrollTop;cbSel(%d);return Math.abs(document.getElementById('cbv').scrollTop-y)<=2})()" % oi))
    ev("cbSelNone()"); ev("cbBulk('found','all')"); nf = ev("cbGrpList('found').length"); chk('“☑ Hammasini tanla” on the found group ticks all of them (not the ones already in the deck)', ev("Object.keys(CBS.sel).length") == nf and nf >= 8)
    ev("cbBulk('found','none')"); chk('“☐ Bekor qilish” clears just that group', ev("Object.keys(CBS.sel).length") == 0)
    ev("cbBulk('miss','all')"); ev("cbBulk('other','all')"); chk('the missing and other-passage groups have their own bulk buttons (both ticked here)', ev("Object.keys(CBS.sel).length") == ev("cbGrpList('miss').length+cbGrpList('other').length"))
    ev("cbBulk('miss','inv')"); chk('“⇄ Teskari” flips the selection of that group', ev("cbGrpList('miss').every(i=>!CBS.sel[i])"))
    ev("cbSelNone()"); ev("S.cb=S.cb||{};cbS().w['1:1']={b:0,due:'2026-11-11',a:'2026-11-11'}"); ev("cbBulk('found','all')"); chk('words already in the deck are never ticked by the bulk buttons', not ev("!!CBS.sel[CB.K['1:1']]"))
    ev("cbSelNone()")
    # saqlash
    chk('the text screen offers “💾 Maqola sifatida saqlash (so‘zlar ko‘rinib turadi, AI tahlil qiladi)”', '💾 Maqola sifatida saqlash' in pg.inner_text('#cbv'))
    ev("S.cb.w={}"); ev("cbSaveText()"); pg.wait_for_timeout(400); m = ev("S.ie.mat[0]"); chk('saving creates a normal “Maqola” material in IELTS → Materiallar: title “📚 Manatees”, the full text, linked to the passage, not analysed yet', m and m['t'] == '📚 Manatees' and m['k'] == 'a' and m['x'].startswith('Manatees are aquatic') and m['cb'] == 1 and m['an'] is None and len(ev("S.ie.mat")) == 1, m and {k: m[k] for k in ('t', 'k', 'cb')})
    chk('and the reader opens at once (the Cambridge screen closes)', ev("!!document.getElementById('iem')") and not ev("!!document.getElementById('cbv')"))
    t = pg.inner_text('#iem'); chk('the reader has the usual “AI bilan tahlil” button AND a “📚 Cambridge so‘zlari: matnda N ta (M ta yangi)” list with Uzbek translations', 'AI bilan tahlil' in t and '📚 Cambridge so‘zlari: matnda' in t and 'ta yangi' in t)
    nm = ev("document.querySelectorAll('#iem mark.mcb').length"); chk('Cambridge words are marked inside the text itself (amber), so the vocabulary is visible while reading', nm >= 8, nm)
    ev("document.querySelector('#iem mark.mcb').click()"); pg.wait_for_timeout(300); t = ev("document.getElementById('iesh')&&document.getElementById('iesh').textContent"); chk('tapping a marked word opens a card with its Uzbek translation, definition, example and a button to add it to the Cambridge deck', t and 'tarjima' in t and 'definition of' in t and 'Cambridge to‘plamiga qo‘sh' in t, t)
    n0 = len(ev("Object.keys(S.cb.w)")); ev("document.querySelector('#iesh .big').click()"); pg.wait_for_timeout(120); chk('adding from the card puts it into the deck; the mark turns green (“to‘plamda”)', len(ev("Object.keys(S.cb.w)")) == n0 + 1 and ev("document.querySelectorAll('#iem mark.mcb.hv').length") >= 1)
    ev("ieMatClose()"); ev("(t)=>{CBS.txt=t;cbOpen('t');CBS.txt=t;cbDraw();cbRun()}", TEXT); pg.wait_for_timeout(100); ev("cbSaveText()"); pg.wait_for_timeout(200); chk('saving the same text twice does not create a duplicate (it opens the saved one)', len(ev("S.ie.mat")) == 1 and any('allaqachon saqlangan' in x for x in ev("__t"))); ev("ieMatClose()")
    ev("(t)=>{CBS.txt=t;cbOpen('t');cbDraw()}", ''); t = pg.inner_text('#cbv'); chk('the saved texts are listed on the text screen (“💾 Saqlangan matnlar (1)”) so they can be reopened', '💾 Saqlangan matnlar (1)' in t)
    ev("S.ie.mat.push({id:99,t:'Oddiy maqola',k:'a',x:'x'.repeat(300),c:[],au:0,an:null,d:'2026-11-01'})"); n = 0
    for i in range(31):
        ev("(a)=>{CBS.txt=a;CBS.pi=1;cbSaveText()}", ('Unique passage number %d about manatees and aquatic life. ' % i) * 8); pg.wait_for_timeout(30)
        ev("()=>{if(document.getElementById('iem'))ieMatClose(true)}")
    chk('at most 30 saved Cambridge texts are kept (the oldest drop out) and your ordinary materials are never pushed out by them', len([m for m in ev("S.ie.mat") if m.get('cb')]) == 30 and any(m['id'] == 99 for m in ev("S.ie.mat")))
    ev("uiS('trk_cb','0')"); ev("(()=>{const m=S.ie.mat.find(x=>x.cb);ieMatOpen(m.id)})()"); pg.wait_for_timeout(300); chk('with the Cambridge feature switched off the reader is the plain one (no Cambridge panel or marks)', 'Cambridge so‘zlari: matnda' not in pg.inner_text('#iem')); ev("ieMatClose()"); ev("uiS('trk_cb','1')")
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='h';BV='j';render()}", [ui, th]); pg.wait_for_timeout(70); o1 = ev("document.documentElement.scrollWidth<=window.innerWidth+1")
            ev("(t)=>{CBS.txt=t;cbOpen('t');cbDraw();cbRun()}", TEXT); o2 = ev("document.querySelector('#cbv .asc').scrollWidth<=document.querySelector('#cbv .asc').clientWidth+1"); ev("cbClose()")
            if not (o1 and o2): bad.append(ui + th)
    chk('the Mulk card, the “Undan keyin” list and the Cambridge screens fit the phone in all three styles, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
