# Testlar bo'limi: savol banki import, mashq/imtihon, xatolar banki, statistika, bulut. Soat: 2026-11-11 10:00.
import sys, json, re, os
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
BANK = open('/mnt/user-data/outputs/testlar-banki.json', encoding='utf-8').read()
D = json.loads(BANK)
SMALL = json.dumps({'v': 1, 'subjects': [{'id': 'x1', 'name': 'Tarix <b>X</b>', 'topics': [{'id': 'x11', 'name': 'Qadimgi davr', 'src': 's', 'q': [{'id': 'x11.%d' % i, 'q': 'Savol %d <img src=x onerror=1>' % i, 'o': ['a', 'b', 'c', 'd'], 'a': i % 4, 'e': 'izoh', 'r': '1-slayd'} for i in range(1, 6)]}]}]}, ensure_ascii=False)
ANS = lambda ok: "(()=>{const id=TBQ.ids[TBQ.i],x=TBX[id],ord=TBQ.ord[TBQ.i];let k=ord.indexOf(x.q.a);if(!%s)k=(k+1)%%4;tbAns(k)})()" % ('true' if ok else 'false')
with Run('tb', when=(2026, 11, 11, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;for(const k of ['trk_tb','trk_tbsh','trk_tbsec','trk_swh'])localStorage.removeItem(k);localStorage.setItem('trk_swh','1');S.tb=undefined;TB=null;TBX={};TBO=false;TBQ=null;TBR=null;window.__cbUid=undefined;window.__cbStore=undefined;tab='h';render()}""")
    ev("(async()=>{try{await tbIdbDel()}catch(e){}})()"); pg.wait_for_timeout(120)
    chk('the Univer screen starts with a “📝 Testlar” card with an “Ochish” button', '📝 Testlar' in ev("univer()") and 'Testlarni ochish' in ev("univer()"))
    ev("tbOpen()"); pg.wait_for_timeout(150); chk('without a bank the section says it is not loaded yet and offers to pick the file', 'Savol banki hali yuklanmagan' in pg.inner_text('#tbv') and '📥 Faylni tanlash' in pg.inner_text('#tbv')); ev("tbClose()")
    # bank sifati
    allq = [q for s in D['subjects'] for t in s['topics'] for q in t['q']]
    chk('YOUR BANK FILE: 2 subjects, 9 topics, %d questions; every question has 4 different options, a valid answer, an explanation and a source; ids are unique' % len(allq), len(D['subjects']) == 2 and sum(len(s['topics']) for s in D['subjects']) == 9 and len(allq) >= 230 and all(len(set(q['o'])) == 4 and 0 <= q['a'] < 4 and q['e'] and q['r'] for q in allq) and len({q['id'] for q in allq}) == len(allq))
    pos = [sum(1 for q in allq if q['a'] == k) / len(allq) for k in range(4)]
    chk('the right answer is spread over A, B, C and D (each between 15% and 35%), not always in the same place', all(.15 <= p <= .35 for p in pos), pos)
    chk('every topic has at least 20 questions', all(len(t['q']) >= 20 for s in D['subjects'] for t in s['topics']))
    # import
    chk('garbage is refused: not JSON, a question with 3 options, a wrong answer index', ev("(async()=>[await tbImportText('xx',false),await tbImportText(JSON.stringify({v:1,subjects:[{id:'a',name:'a',topics:[{id:'b',name:'b',q:[{id:'1',q:'q',o:['a','b','c'],a:0}]}]}]}),false),await tbImportText(JSON.stringify({v:1,subjects:[{id:'a',name:'a',topics:[{id:'b',name:'b',q:[{id:'1',q:'q',o:['a','b','c','d'],a:7}]}]}]}),false)])()") == [False, False, False] and ev("TB") is None)
    chk('importing your file works and says “✅ N ta savol, 9 ta mavzu yuklandi”', ev("(t)=>tbImportText(t,false)", BANK) is True and ev("tbCount()") == len(allq) and '9 ta mavzu yuklandi' in ev("TBS.st"))
    ev("TB=null;TBX={}"); chk('the bank survives closing the app (kept in the phone’s own storage)', ev("tbLoad()") is True and ev("tbCount()") == len(allq))
    chk('importing a second file ADDS its subject and keeps the others; importing the same topic again replaces it (no duplicates)', ev("(t)=>tbImportText(t,false)", SMALL) is True and ev("TB.subjects.length") == 3 and ev("tbCount()") == len(allq) + 5 and ev("(t)=>tbImportText(t,false)", SMALL) is True and ev("tbCount()") == len(allq) + 5)
    # bosh ekran
    ev("tbOpen()"); pg.wait_for_timeout(150); t = pg.inner_text('#tbv'); chk('the home screen lists subjects and topics with question counts; it has “🎲 Umumiy test”, “❗ Xatolar”, question-count choices and Mashq / Imtihon modes', all(x in t for x in ['Tilshunoslikka kirish', 'Fonetika', 'Axborot texnologiyalari', 'Tarix <b>X</b>', '🎲 Umumiy test', '❗ Xatolar (0)', '✍️ Mashq', '⏱ Imtihon']) and '28 savol' in t)
    chk('HTML inside a bank (a subject name and a question with <img onerror>) is shown as plain text, never executed', '<b>X</b>' in t and ev("document.querySelectorAll('#tbv img, #tbv b').length>=0") and not ev("!!document.querySelector('#tbv img')"))
    # mashq
    ev("uiS('trk_tbsh','0')"); ev("tbBegin('t','ts5',10,'m','Fonetika')"); pg.wait_for_timeout(100); Q = ev("TBQ"); chk('a practice test on Fonetika takes 10 different questions from that topic; with “Faylda berilgandek” the options keep the file order', len(Q['ids']) == 10 and len(set(Q['ids'])) == 10 and all(i.startswith('ts5.') for i in Q['ids']) and all(o == [0, 1, 2, 3] for o in Q['ord']))
    ev("uiS('trk_tbsh','1')"); ev("tbBegin('t','ts5',10,'m','Fonetika')"); Q = ev("TBQ"); chk('with the default setting the options are shuffled for every question (each is still a permutation of A–D)', all(sorted(o) == [0, 1, 2, 3] for o in Q['ord']) and any(o != [0, 1, 2, 3] for o in Q['ord']))
    t = pg.inner_text('#tbv'); chk('the question screen shows “1 / 10”, the question, four lettered options and a progress bar', '1 / 10' in t and re.search(r'\nA\n', t) and ev("document.querySelectorAll('#tbv .tbo').length") == 4 and ev("!!document.querySelector('#tbv .ttbr')"))
    ev(ANS(False)); pg.wait_for_timeout(80); chk('a wrong answer is marked red, the right one green, with “❌ Noto‘g‘ri”, the correct answer, the explanation and the source slide; options lock', ev("document.querySelectorAll('#tbv .tbo[class~=bad]').length") == 1 and ev("document.querySelectorAll('#tbv .tbo.ok').length") == 1 and '❌ Noto‘g‘ri' in pg.inner_text('#tbv') and 'Manba: Fonetika' in pg.inner_text('#tbv') and ev("[...document.querySelectorAll('#tbv .tbo')].every(b=>b.disabled)"))
    ev("tbGo(1)"); ev(ANS(True)); chk('a right answer shows “✅ To‘g‘ri” in green', '✅ To‘g‘ri' in pg.inner_text('#tbv') and ev("document.querySelectorAll('#tbv .tbo.ok').length") == 1)
    ev("()=>{window.tbQ1=TBQ.ids[0]}"); ev("tbFlag(TBQ.ids[TBQ.i])"); chk('“🏳️ Shubhali” flags the current question (🚩), and tapping again removes the flag', len(ev("Object.keys(S.tb.f)")) == 1 and '🚩 Belgilangan' in pg.inner_text('#tbv')); ev("tbFlag(TBQ.ids[TBQ.i])"); chk('…', len(ev("Object.keys(S.tb.f)")) == 0)
    for i in range(2, 10): ev("tbGo(1)"); ev(ANS(i % 3 != 0))
    ev("tbFinish()"); pg.wait_for_timeout(100); R_ = ev("TBR"); n_wrong = R_['rec']['n'] - R_['rec']['ok']
    chk('finishing shows the result (percent, X / 10, a grade), saves it in the history and puts the wrong answers into the mistakes bank', R_['rec']['n'] == 10 and 1 <= n_wrong <= 5 and len(ev("S.tb.h")) == 1 and len(ev("Object.keys(S.tb.m)")) == n_wrong and ev("TBS.v") == 'r' and '%' in pg.inner_text('#tbv'), (R_['rec'], n_wrong))
    t = pg.inner_text('#tbv'); chk('the result lists the wrong questions (fold-out with the correct answer and the explanation) and offers “🔁 Qayta”, “❗ Xatolarni mashq qil” and “Mavzular”', 'Xato javoblar (%d)' % n_wrong in t and '🔁 Qayta' in t and '❗ Xatolarni mashq qil' in t)
    # xatolar banki
    ev("tbV('h')"); pg.wait_for_timeout(60); chk('the home screen counts the mistakes (“❗ Xatolar (N)”)', '❗ Xatolar (%d)' % n_wrong in pg.inner_text('#tbv'))
    ev("tbGo2('m','','Xatolar banki')"); Q = ev("TBQ"); chk('the mistakes bank practises exactly those questions', sorted(Q['ids']) == sorted(ev("Object.keys(S.tb.m)")) and Q['mo'] == 'm')
    for _ in Q['ids']: ev(ANS(True)); ev("tbGo(1)")
    ev("tbFinish()"); chk('answering them right once keeps them (streak 1), …', len(ev("Object.keys(S.tb.m)")) == n_wrong and all(v['s'] == 1 for v in ev("Object.values(S.tb.m)")))
    ev("tbGo2('m','','Xatolar banki')")
    for _ in ev("TBQ.ids"): ev(ANS(True)); ev("tbGo(1)")
    ev("tbFinish()"); chk('…and a second right answer in a row clears them from the mistakes bank', ev("Object.keys(S.tb.m).length") == 0)
    # imtihon
    ev("tbBegin('t','ts5',10,'m','Fonetika')"); pg.wait_for_timeout(60); chk('in practice mode the next button stays disabled until the question is answered (so the explanation is read)', ev("[...document.querySelectorAll('#tbv .big')].find(b=>b.textContent.includes('Keyingisi')).disabled") is True and ev("!document.getElementById('tbt')")); ev("tbQuit()")
    ev("tbBegin('t','ts5',10,'e','Fonetika')"); pg.wait_for_timeout(80); chk('exam mode shows a countdown (10 questions × 45 s = 7:30) that follows the clock', ev("document.getElementById('tbt').textContent") == '7:30'); pg.clock.run_for(61000); pg.wait_for_timeout(60); chk('…after one minute it reads 6:29–6:30', ev("document.getElementById('tbt').textContent") in ('6:30', '6:29'))
    ev(ANS(True)); chk('in exam mode there is NO feedback after answering (the option is only highlighted)', ev("document.querySelectorAll('#tbv .tbo.ok').length") == 0 and ev("document.querySelectorAll('#tbv .tbo.sel').length") == 1 and 'Noto‘g‘ri' not in pg.inner_text('#tbv'))
    ev("tbGo(1)"); chk('in exam mode questions can be skipped (the next button works, a number grid shows which are answered ✓) and finishing warns about unanswered ones', ev("[...document.querySelectorAll('#tbv .big')].find(b=>b.textContent.includes('Keyingisi')).disabled") is False and '✓' in pg.inner_text('#tbv') and ev("document.querySelectorAll('#tbv .chip').length") >= 10); ev("tbGo(-1)"); chk('going back keeps the earlier answer', ev("TBQ.ans[TBQ.ids[0]]") is not None)
    pg.clock.run_for(460000); pg.wait_for_timeout(150); chk('when the time runs out the test finishes by itself (“Vaqt tugadi”) with the unanswered questions counted as wrong', ev("TBQ.fin") is True and any('Vaqt tugadi' in m for m in ev("__t")) and ev("TBR.un") == 9 and ev("TBR.rec.ok") in (0, 1) and ev("TBS.v") == 'r')
    ev("uiS('trk_tbsec','30')"); ev("tbBegin('t','ts5',10,'e','F')"); chk('Settings choose the time per question (30 s → 5:00 for 10 questions)', ev("document.getElementById('tbt').textContent") == '5:00'); ev("tbQuit()"); ev("uiS('trk_tbsec','45')")
    # umumiy
    ev("tbBegin('s','ts',30,'m','Tilshunoslik')"); Q = ev("TBQ"); tops = {i.split('.')[0] for i in Q['ids']}; chk('the subject-wide test mixes topics of that subject only (30 questions from several of the 6 linguistics topics)', len(Q['ids']) == 30 and len(tops) >= 4 and all(t.startswith('ts') for t in tops), tops)
    ev("tbBegin('a','',0,'m','Hamma')"); chk('the all-subjects test with “hammasi” takes the whole bank', len(ev("TBQ.ids")) == len(allq) + 5)
    ev("tbQuit()"); ev("tbV('h')")
    # statistika
    ev("tbV('s')"); pg.wait_for_timeout(80); t = pg.inner_text('#tbv'); chk('Statistika: tests done, answered questions, overall percent, mistakes in the bank, and the topics from weakest to strongest', all(x in t for x in ['Yechilgan testlar', 'Javob berilgan savollar', 'Umumiy to‘g‘ri', 'Xatolar bankida', 'Fonetika']) and ev("S.tb.h.length") >= 4)
    # sozlamalar
    ev("tbV('g')"); t = pg.inner_text('#tbv'); chk('the ⚙️ tab shows the bank status, file / cloud buttons, option shuffling and exam seconds', all(x in t for x in ['Qurilmada:', '📥 Fayl qo‘shish', 'Har safar aralashtirilsin', 'Faylda berilgandek', '30 s', '90 s']))
    ev("tbClose()"); ev("()=>{SDO={jl:1};tab='s';render()}"); pg.wait_for_timeout(100); chk('Settings → Jilo can switch the Testlar section on/off and has the shuffle and exam-time choices', all(x in pg.inner_text('#app') for x in ['Testlar bo‘limi', 'Test variantlari tartibi', 'Imtihon rejimida bitta savolga vaqt']))
    ev("uiS('trk_tb','0')"); chk('switched off: no card and nothing opens', ev("univer()").find('📝 Testlar') == -1 and ev("(()=>{tbOpen();return !!document.getElementById('tbv')})()") is False); ev("uiS('trk_tb','1')")
    # bulut
    ev("""()=>{window.__cbUid='user-1';window.__cbLog=[];window.__cbBlob=null;window.__cbStore={from:b=>({upload:async(p,blob,o)=>{window.__cbLog.push([b,p,o&&o.upsert]);window.__cbBlob=await blob.text();return{error:null}},download:async p=>{window.__cbLog.push(['dl',b,p]);if(!window.__cbBlob)return{data:null,error:{message:'Object not found'}};return{data:new Blob([window.__cbBlob]),error:null}}})}}""")
    ev("TB=null;TBX={}"); ev("(t)=>tbImportText(t)", BANK); pg.wait_for_timeout(150); lg = ev("__cbLog")
    chk('importing also uploads to your private bucket at <your id>/testlar.json (same bucket, no extra SQL) and says so', lg[0][0] == 'cambridge' and lg[0][1] == 'user-1/testlar.json' and lg[0][2] is True and 'Bulutda saqlandi' in ev("TBS.cl"))
    ev("TB=null;TBX={};tbIdbDel()"); pg.wait_for_timeout(120); ev("tbOpen()"); pg.wait_for_timeout(450); chk('on another device (nothing stored locally) opening the section downloads the bank from the cloud by itself', ev("tbCount()") == len(allq) and 'Bulutdan yuklandi' in ev("TBS.cl")); ev("tbClose()")
    # maxfiylik
    html = open('/mnt/user-data/outputs/tracker/index.html', encoding='utf-8').read()
    chk('PRIVACY: none of the bank’s questions or explanations is inside the built app (the file is only imported), and the bank is not in the deploy package', not any(q['q'] in html or q['e'] in html for q in allq[:150]) and 'testlar-banki' not in open('/mnt/user-data/outputs/tools/make_zips.py', encoding='utf-8').read() and not os.path.exists('/mnt/user-data/outputs/tracker/testlar-banki.json'))
    bad = []
    ev("(t)=>{TB=null;return tbImportText(t,false)}", BANK); ev("uiS('trk_tbsh','1')")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];TBO=true;TBS.st='';TBS.v='h';tbDraw()}", [ui, th]); w = lambda: ev("document.querySelector('#tbv .asc').scrollWidth<=document.querySelector('#tbv .asc').clientWidth+1"); o1 = w()
            ev("tbBegin('t','ts1',10,'m','Tarix')"); ev(ANS(False)); o2 = w(); ev("tbFinish()"); o3 = w(); ev("tbV('s')"); o4 = w(); ev("tbV('g')"); o5 = w(); ev("tbClose()")
            if not (o1 and o2 and o3 and o4 and o5): bad.append(ui + th)
    chk('home, question (with feedback), result, statistics and settings fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
