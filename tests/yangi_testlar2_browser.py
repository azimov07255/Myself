import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Testlar kengaytmasi: ochiq rejim, takrorlash jadvali, oraliq reja, Bugun kartasi. Soat: chorshanba 2026-11-11 10:00.
import sys, json
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
def bank():
    mk = lambda sid, tid, n: {'id': tid, 'name': 'Mavzu ' + tid, 'src': 's', 'q': [{'id': '%s.%d' % (tid, i), 'q': 'Savol %s %d' % (tid, i), 'o': ['a', 'b', 'c', 'd'], 'a': i % 4, 'e': 'izoh %d' % i, 'r': '%d-slayd' % i} for i in range(1, n + 1)]}
    return json.dumps({'v': 1, 'subjects': [{'id': 'x1', 'name': 'Tilshunoslik', 'topics': [mk('x1', 'x11', 6), mk('x1', 'x12', 4)]}, {'id': 'x2', 'name': 'Axborot', 'topics': [mk('x2', 'x21', 5)]}]}, ensure_ascii=False)
with Run('tx', when=(2026, 11, 11, 10, 0, 0), bg='n') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;for(const k of ['trk_tb','trk_tbsh','trk_tbsec','trk_txc','trk_swh','trk_bg'])localStorage.removeItem(k);localStorage.setItem('trk_swh','1');S.tb=undefined;TB=null;TBX={};TBO=false;TBQ=null;TBR=null;window.__cbUid=undefined;window.__cbStore=undefined;tab='h';BV='j';render()}""")
    ev("(async()=>{try{await tbIdbDel()}catch(e){}})()"); pg.wait_for_timeout(100)
    ok = ev("(async(t)=>await tbImportText(t,false))", bank()); pg.wait_for_timeout(300)
    chk('(setup) a test bank with 2 subjects and 15 questions is loaded', ev("tbCount()") == 15, ok)
    ev("tbOpen('h')"); pg.wait_for_timeout(120); t = pg.inner_text('#tbv'); chk('the Testlar home has the new extras: “🔁 Bugun takrorlash (0)” (nothing to repeat yet) and “🧠 Ochiq rejim”', '🔁 Bugun takrorlash (0)' in t and '🧠 Ochiq rejim' in t and ev("[...document.querySelectorAll('#tbv button')].find(b=>b.textContent.includes('Bugun takrorlash')).disabled") is True)
    ev("tbSetN(5)"); ev("txStartOpen('a','','Hamma fanlar')"); pg.wait_for_timeout(100); t = pg.inner_text('#tbv'); chk('open mode shows only the question (no A/B/C/D options) and a “👁 Javobni ko‘rish” button; moving on is blocked until you rate yourself', 'Savol' in t and '👁 Javobni ko‘rish' in t and ev("document.querySelectorAll('#tbv .tbo').length") == 0 and ev("[...document.querySelectorAll('#tbv button')].find(b=>b.textContent.includes('Keyingisi')).disabled") is True and '🧠 ochiq' in t)
    ev("txRev()"); pg.wait_for_timeout(80); t = pg.inner_text('#tbv'); chk('“Javobni ko‘rish” reveals the right answer with the explanation and the source, then asks “Qanchalik bilding?” with ✅ Bildim / 🟡 Qisman / ❌ Bilmadim', all(x in t for x in ['To‘g‘ri javob:', 'izoh', 'Manba:', 'slayd', 'Qanchalik bilding', '✅ Bildim', '🟡 Qisman', '❌ Bilmadim']))
    ids = ev("TBQ.ids"); rates = ['y', 'y', 'p', 'n', 'y']
    for i, r in enumerate(rates):
        if i: ev("txRev()")
        ev("(r)=>txRate(r)", r); pg.wait_for_timeout(40)
        if i == 0: chk('after rating, “Keyingisi ›” becomes active', ev("[...document.querySelectorAll('#tbv button')].find(b=>b.textContent.includes('Keyingisi')).disabled") is False)
        if i < 4: ev("tbGo(1)")
    chk('the ratings are stored: Bildim = correct answer, Qisman and Bilmadim = counted as not known (the answer is not pretended to be a wrong option)', ev("TBQ.sf") == {ids[0]: 'y', ids[1]: 'y', ids[2]: 'p', ids[3]: 'n', ids[4]: 'y'} and ev("TBQ.ans[TBQ.ids[2]]") == -1 and ev("TBQ.ans[TBQ.ids[0]] === TBX[TBQ.ids[0]].q.a"))
    ev("tbFinish()"); pg.wait_for_timeout(120); t = pg.inner_text('#tbv'); chk('the result is 3 / 5 = 60%, and the not-known ones are listed with “O‘zing baholading” instead of a made-up wrong choice', '60%' in t and '3 / 5' in t and ev("document.getElementById('tbv').innerHTML").count('O‘zing baholading') == 2 and 'Sen:' not in ev("document.getElementById('tbv').innerHTML"))
    A = ev("S.tb"); chk('all 5 answered questions are marked as seen today, and the 2 not-known ones go to the mistakes bank to repeat TOMORROW (2026-11-12)', len(A['sn']) == 5 and all(v == '2026-11-11' for v in A['sn'].values()) and sorted(A['m'].keys()) == sorted([ids[2], ids[3]]) and all(A['m'][k]['nx'] == '2026-11-12' for k in A['m']), A['m'])
    ev("tbClose()"); chk('nothing is due today (they are scheduled for tomorrow)', ev("txDue().length") == 0)
    pg.clock.set_system_time('2026-11-12T10:00:00'); ev("render()"); chk('tomorrow both are due', sorted(ev("txDue()")) == sorted([ids[2], ids[3]]))
    ev("tbOpen('h')"); pg.wait_for_timeout(100); chk('and the button reads “🔁 Bugun takrorlash (2)”', '🔁 Bugun takrorlash (2)' in pg.inner_text('#tbv'))
    ev("txStartDue()"); pg.wait_for_timeout(100); chk('it starts a practice with exactly those two questions (explanations after each answer)', ev("TBQ.kind") == 'd' and sorted(ev("TBQ.ids")) == sorted([ids[2], ids[3]]) and ev("TBQ.mo") == 'm')
    ev("(()=>{for(let i=0;i<TBQ.ids.length;i++){const id=TBQ.ids[i],x=TBX[id],ord=TBQ.ord[i];const k=ord.indexOf(x.q.a);TBQ.i=i;tbAns(k)}})()"); ev("tbFinish()"); pg.wait_for_timeout(100)
    A = ev("S.tb"); chk('answering both correctly moves their next repetition 3 days ahead (2026-11-15) — they are still in the bank until they are right twice in a row', all(A['m'][k]['nx'] == '2026-11-15' and A['m'][k]['s'] == 1 for k in [ids[2], ids[3]]), A['m'])
    ev("tbClose()"); chk('so nothing is due on the 12th any more', ev("txDue().length") == 0)
    pg.clock.set_system_time('2026-11-15T10:00:00'); ev("txStartDue()"); ev("(()=>{for(let i=0;i<TBQ.ids.length;i++){const id=TBQ.ids[i],x=TBX[id],ord=TBQ.ord[i];TBQ.i=i;tbAns(ord.indexOf(x.q.a))}})()"); ev("tbFinish()"); chk('on the 15th a second correct answer in a row removes them from the mistakes bank', ev("Object.keys(S.tb.m).length") == 0); ev("tbClose()"); pg.clock.set_system_time('2026-11-12T10:00:00')
    # oraliq reja
    ev("txExSet('x1','2026-11-14')"); p = ev("txPlan('x1')"); chk('with an exam date in 2 days for the 10-question subject (5 already seen): 2 days left, 5 left to see, so 3 a day', p['left'] == 2 and p['total'] == 10 and p['rem'] == 10 - ev("txSubQ('x1').filter(i=>S.tb.sn[i]).length") and p['quota'] == -(-p['rem'] // 2), p)
    ev("tbOpen('h')"); pg.wait_for_timeout(100); t = pg.inner_text('#tbv'); chk('the home shows the plan: “Oraliq tayyorgarlik”, the days left, how many are seen and “▶ Bugungi N ta savol”', all(x in t for x in ['Oraliq tayyorgarlik', 'Tilshunoslik', '2 kun', 'Ko‘rilgan', 'kuniga', '▶ Bugungi']))
    ev("txToday('x1')"); pg.wait_for_timeout(100); seen0 = ev("txSubQ('x1').filter(i=>S.tb.sn[i]).length"); chk('“Bugungi N ta savol” takes exactly N questions and prefers ones you have not seen yet', ev("TBQ.ids.length") == p['quota'] and all(not ev("(i)=>!!S.tb.sn[i]", i) for i in ev("TBQ.ids")), ev("TBQ.ids"))
    ev("(()=>{for(let i=0;i<TBQ.ids.length;i++){const id=TBQ.ids[i],x=TBX[id],ord=TBQ.ord[i];TBQ.i=i;tbAns(ord.indexOf(x.q.a))}})()"); ev("tbFinish()"); ev("tbClose()"); p2 = ev("txPlan('x1')"); chk('after finishing, the seen count grows by that many and the remaining shrinks', p2['seen'] == seen0 + p['quota'] and p2['rem'] == p['rem'] - p['quota'])
    ev("txExSet('x1','2026-11-10')"); ev("tbOpen('h')"); pg.wait_for_timeout(100); chk('an exam date in the past says “Sana o‘tgan” and offers to set a new date', 'Sana o‘tgan' in pg.inner_text('#tbv')); ev("tbClose()")
    ev("txExSet('x1','')"); chk('clearing the date removes the plan', ev("txPlan('x1')") is None)
    ev("tbOpen('s')"); pg.wait_for_timeout(100); ev("tbV('set')"); pg.wait_for_timeout(100); t = pg.inner_text('#tbv'); chk('⚙️ has a date field per subject under “Oraliq imtihon sanalari”', 'Oraliq imtihon sanalari' in t and ev("document.querySelectorAll('#tbv input[type=date]').length") == 2); ev("tbClose()")
    # Bugun kartasi
    ev("txExSet('x2','2026-11-20')"); ev("()=>{S.tb.m={'x11.1':{w:1,s:0,l:'2026-11-11',nx:'2026-11-12'}}}"); pg.clock.set_system_time('2026-11-12T10:00:00'); h = ev("txCard()"); chk('the Bugun card summarises today’s test work: “🔁 Takrorlash: 1 ta savol” and the exam countdown with how many questions to do today', all(x in h for x in ['📝 Testlar', '🔁 Takrorlash: <b>1 ta</b>', 'Axborot', '8 kun', 'bugun']))
    ev("()=>{tab='h';BV='k';render()}"); pg.wait_for_timeout(120); sm = ev("[...document.querySelectorAll('#app details.bgs')].map(d=>d.querySelector('summary').textContent.trim()+'|'+d.innerText.includes('Takrorlash'))"); chk('on the 🧩 Kun screen the card is inside the “📚 O‘rganish” group', any(x.startswith('📚 O‘rganish') and x.endswith('|true') for x in sm), sm)
    ev("uiS('trk_txc','0')"); chk('the card can be switched off', ev("txCard()") == ''); ev("uiS('trk_txc','1')")
    ev("()=>{S.tb.m={};S.tb.ex={}}"); chk('with nothing to repeat and no exam date the card is not shown', ev("txCard()") == '')
    ev("()=>{BV='j';render()}"); ev("()=>{SDO={jl:1};tab='s';render()}"); pg.wait_for_timeout(100); chk('Settings → Jilo has the switch for the Testlar plan card', 'Testlar rejasi kartasi' in pg.inner_text('#app'))
    bad = []
    ev("()=>{tab='h';BV='j';render()}")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='h';BV='j';render()}", [ui, th]); pg.wait_for_timeout(60)
            ev("txExSet('x1','2026-11-20')"); ev("tbOpen('h')"); pg.wait_for_timeout(150); ok = ev("(()=>{const a=document.querySelector('#tbv .asc');return a.scrollWidth<=a.clientWidth+1})()")
            ev("txStartOpen('a','','Hamma fanlar')"); ev("txRev()"); pg.wait_for_timeout(100); ok = ok and ev("(()=>{const a=document.querySelector('#tbv .asc');return a.scrollWidth<=a.clientWidth+1})()"); ev("tbClose()"); ev("txExSet('x1','')")
            if not ok: bad.append(ui + th)
    chk('the Testlar home (with the plan) and the open-mode screen fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
