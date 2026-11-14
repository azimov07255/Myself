# Ayat o'yini: keyingi so'zni top, ayatni tartibga sol. Soat: 2026-11-05 10:00. Haqiqiy Mushaf ma'lumoti bilan.
import sys, json
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
DATA = json.load(open('/mnt/user-data/outputs/data/quran-mushaf.json', encoding='utf-8'))
with Run('ayat', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""(d)=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confetti=()=>{window.__cf=(window.__cf||0)+1};MF=d;MFP=Promise.resolve(d);
      S.nomf=0;S.q.m={};S.q.m[0]=1;S.q.m[1]=3;S.q.m[113]=1;S.q.ord=[0,1,113];S.q.rs={};S.mq=undefined;S.ie.gm={};S.ie.gb={};QG=null;tab='q';QT='t';TKV='b';render()}""", DATA)
    pg.wait_for_timeout(150); t = pg.inner_text('#app')
    chk('the Takror tab shows the "🎯 Ayat o‘yini" card with both games and how many of your suras are used (3 memorized suras)', '🎯 Ayat o‘yini' in t and '3 sura' in t and 'Keyingi so‘zni top' in t and 'Ayatni tartibga sol' in t)
    ev("S.nomf=1;render()"); pg.wait_for_timeout(60); chk('with the Mushaf switched off the card is hidden (the game needs the Mushaf text)', '🎯 Ayat o‘yini' not in pg.inner_text('#app')); ev("S.nomf=0;render()")
    ev("()=>{S.q.ord=[];render()}"); pg.wait_for_timeout(60); t = pg.inner_text('#app'); chk('with no memorized suras it offers practice with Juz Amma suras', 'Juz Amma' in t); ev("()=>{S.q.ord=[0,1,113];render()}")
    # savollar
    nx = ev("""(()=>{const qs=qgBuild('next'),ok=[];qs.forEach(q=>{const w=qgWords(q.k);ok.push([q.o.length===4,new Set(q.o).size===4,q.o[q.a]===q.ans,q.ans===w[q.c],JSON.stringify(q.sh)===JSON.stringify(w.slice(0,q.c)),q.c>=2&&q.c<=w.length-1,w.length>=5,[0,1,113].includes(vkS(q.k)-1),!q.o.filter((x,i)=>i!==q.a).includes(q.ans),vkS(q.k)!==2||MF.vp[mfIdx(q.k)]<SP[1]+3].every(Boolean))});return {n:qs.length,all:ok.every(Boolean),bad:ok.filter(x=>!x).length,uniq:new Set(qs.map(q=>q.k)).size}})()""")
    chk('"next word" questions: 10 different verses from the memorized suras only (and for a partly memorized sura only from the memorized pages); each shows a prefix of the verse and 4 distinct options, one of which is the real next word', nx['n'] == 10 and nx['all'] and nx['uniq'] == 10, nx)
    od = ev("""(()=>{const qs=qgBuild('order'),b=[];qs.forEach(q=>{const w=qgWords(q.k),n=q.ch.length;b.push([q.ch.join(' ')===w.join(' '),w.length>=6&&w.length<=24,n===(w.length<=9?3:w.length<=14?4:5),[...q.ord].sort().join()===[...Array(n).keys()].join(),q.ord.join()!==[...Array(n).keys()].join()||n<2].every(Boolean))});return {n:qs.length,bad:b.filter(x=>!x).length}})()""")
    chk('"order" questions: the chunks put back together are exactly the verse (6–24 words, split into 3, 4 or 5 chunks by length) and are shuffled', od['n'] == 10 and od['bad'] <= 1, od)
    ev("()=>{S.q.ord=[];window.__j=qgBuild('next').map(q=>vkS(q.k)-1)}"); j = ev("__j"); chk('with nothing memorized the verses come from Juz Amma (suras 78–114)', len(j) == 10 and all(77 <= x <= 113 for x in j), j); ev("()=>{S.q.ord=[0,1,113]}")
    # o'yin: keyingi so'z
    pg.click('#app .gmb >> text=Keyingi so‘zni top'); pg.wait_for_timeout(500); t = pg.inner_text('#app')
    chk('starting shows "1 / 10", ❤️❤️❤️, the timer bar, the verse beginning in the Mushaf font and 4 options', ev("QG.mode") == 'next' and '1 / 10' in t and '❤️❤️❤️' in t and ev("!!document.getElementById('qgb')") and ev("document.querySelectorAll('#app .qgo').length") == 4 and 'QPC' in ev("getComputedStyle(document.querySelector('#app .qgw')).fontFamily") and ev("getComputedStyle(document.querySelector('#app .qgl')).direction") == 'rtl')
    ans = lambda ok=True: ev("()=>{const q=QG.qs[QG.i];qgAns(%s);return 1}" % ("q.a" if ok else "(q.a+1)%4"))
    ans(True); pg.wait_for_timeout(60); t = pg.inner_text('#app')
    chk('a correct answer: +10, the right option is green, "✅ To‘g‘ri!" with the verse reference (sura:ayah) and the full verse', ev("QG.sc") == 10 and '✅ To‘g‘ri!' in t and ev("document.querySelectorAll('#app .qgo.qgok').length") == 1 and ev("vkL(QG.qs[0].k)") in t and ev("[...document.querySelectorAll('#app .qgw')].some(x=>x.textContent===QG.qs[0].w.join(' '))"))
    pg.click('#app >> text=Keyingisi'); pg.wait_for_timeout(40); ans(False); pg.wait_for_timeout(60); q = ev("QG.qs[1]"); i = q['i']
    chk('a wrong answer: a life is lost, the wrong option is red, and the SURA goes back to your review (weak, box 0, due today) with the verse marked weak in the Mushaf', ev("QG.lives") == 2 and ev("document.querySelectorAll('#app .qgo.qgno').length") == 1 and ev("(i=>{const r=rsOf(i);return r.weak===true&&r.box===0&&r.due===dk()})(%d)" % i) and ev("mq().wk[%d].s" % q['k']) == 0)
    pg.click('#app >> text=Keyingisi'); pg.wait_for_timeout(40); ans(False); pg.click('#app >> text=Keyingisi'); pg.wait_for_timeout(40); ans(False); pg.click('#app >> text=Natija'); pg.wait_for_timeout(80); t = pg.inner_text('#app')
    chk('three wrong answers end the round: "Jonlar tugadi", the score, and the list "Takrorga qaytgan suralar" with the sura names', 'Jonlar tugadi' in t and '10 ball' in t and 'Takrorga qaytgan suralar' in t and ev("QG.wrong.length") == 3)
    chk('the round counts for the daily XP / boss (S.ie.gm today = 1) and the best score is saved', ev("S.ie.gm['2026-11-05']") == 1 and ev("S.ie.gb.qanext") == 10)
    pg.click('#app >> text=Yana'); pg.wait_for_timeout(500)
    for k in range(10):
        ans(True); pg.wait_for_timeout(20); pg.click('#app >> text=/Keyingisi|Natija/'); pg.wait_for_timeout(30)
    t = pg.inner_text('#app'); chk('a perfect round: 170 points, 100%, ⭐⭐⭐, "Xatosiz", confetti, new record', '170 ball' in t and '100%' in t and '⭐⭐⭐' in t and 'Xatosiz' in t and ev("__cf") == 1 and ev("S.ie.gb.qanext") == 170 and ev("S.ie.gm['2026-11-05']") == 2)
    chk('the finished round also counts towards the boss weak point "O‘yinlarda 5 ta raund" (shared daily counter)', ev("BSO.find(x=>x.id==='oyin').n(bsMon())") >= 2)
    ev("qgExit()"); pg.wait_for_timeout(60)
    # vaqt
    ev("qgStart('next')"); pg.wait_for_timeout(500); pg.clock.run_for(21000); pg.wait_for_timeout(100); chk('no answer within 20 seconds: "⏰ Vaqt tugadi.", a life lost, the sura goes back to review', '⏰ Vaqt tugadi.' in pg.inner_text('#app') and ev("QG.lives") == 2 and ev("QG.ans") == -2); ev("qgExit()")
    # tartib
    pg.click('#app .gmb >> text=Ayatni tartibga sol'); pg.wait_for_timeout(500); q = ev("QG.qs[0]"); n = len(q['ch'])
    chk('"order" shows the shuffled chunks as buttons and an empty line above them; 40 seconds per verse', ev("document.querySelectorAll('#app .qgo').length") == n and ev("QG.tl") == 40 and 'Bo‘laklarni ayat tartibida bos' in pg.inner_text('#app'))
    ev("()=>{const q=QG.qs[0];qgPick(q.ord.find(c=>c!==0))}"); pg.wait_for_timeout(60); t = pg.inner_text('#app')
    chk('pressing a chunk that is not the next one fails the verse: a life lost, "❌ Xato.", the correct full verse and its reference are shown', ev("QG.lives") == 2 and '❌ Xato.' in t and ev("vkL(QG.qs[0].k)") in t)
    pg.click('#app >> text=Keyingisi'); pg.wait_for_timeout(40); q1 = ev("QG.qs[1]"); order = list(range(len(q1['ch'])))
    ev("()=>{const q=QG.qs[1];qgPick(0)}"); pg.wait_for_timeout(50); chk('the correct first chunk is placed: it appears in the line above and its button is disabled', ev("QG.qs[1].pl") == [0] and ev("document.querySelectorAll('#app .qgo.used').length") == 1 and ev("QG.ans") is None)
    ev("qgPick(0)"); chk('pressing an already placed chunk does nothing', ev("QG.qs[1].pl") == [0] and ev("QG.lives") == 2)
    ev("()=>{const q=QG.qs[1];for(let c=1;c<q.ch.length;c++)qgPick(c)}"); pg.wait_for_timeout(60); chk('completing the verse in the right order succeeds: +10, "✅ To‘g‘ri!"', ev("QG.ans") == 1 and ev("QG.sc") == 10 and '✅ To‘g‘ri!' in pg.inner_text('#app'))
    ev("qgExit()")
    # yuklanmasa
    ev("()=>{MF=null;MFP=null;window.fetch=()=>Promise.reject(new Error('x'));__t=[]}"); ev("()=>{qgStart('next');return 1}"); pg.wait_for_timeout(300)
    chk('if the Qur‘an text cannot be loaded: a clear message and no broken screen', ev("QG") is None and any('yuklanmadi' in m for m in ev("__t")))
    ev("(d)=>{MF=d;MFP=Promise.resolve(d)}", DATA)
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];QG=null}", [ui, th]); ev("()=>{qgStart('next');return 1}"); pg.wait_for_timeout(300)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th + 'n')
            ev("()=>{qgAns(QG.qs[QG.i].a)}"); pg.wait_for_timeout(40)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th + 'a')
            ev("qgExit()"); ev("()=>{qgStart('order');return 1}"); pg.wait_for_timeout(300)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th + 'o')
            ev("qgExit()")
    chk('the game screens (with Arabic text) fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
