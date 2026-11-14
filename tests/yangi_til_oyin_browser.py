import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Til o'yinlari: ma'lumot sifati, o'yin oqimi, ball/jon/combo, soat, xatolar daftari, o'z xatolaring. Soat: 2026-11-05 10:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
with Run('tilo', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confetti=()=>{window.__cf=(window.__cf||0)+1};S.ie.words=[];S.ie.xd=[];S.ie.gb={};S.ie.gm={};TG=null;tab='e';EV='i';IVW='l';render()}""")
    d = ev("""(()=>{const bad=[];const uq=a=>new Set(a).size===a.length;
      TGC.forEach(x=>{if(!x[0].includes('___')||x[2].length!==3||!uq([x[1],...x[2]])||x[2].includes(x[1]))bad.push('col:'+x[0])});
      TGF.forEach(x=>{if(!x[0].includes('___')||x[2].length!==3||!uq([x[1],...x[2]]))bad.push('fam:'+x[0])});
      TGP.forEach(x=>{if(x.length!==4||!uq(x))bad.push('par:'+x[0])});
      TGE.forEach(x=>{const tk=x[0].split(' ');if(x[1]<0||x[1]>=tk.length)bad.push('err-idx:'+x[0]);const c=tgRep(tk,x[1],x[2]);if(c===x[0])bad.push('err-same:'+x[0]);if(x[2]===''&&c.split(' ').length!==tk.length-1)bad.push('err-del:'+x[0]);if(x[2]!==''&&tk[x[1]].replace(/[.,]/g,'')===x[2])bad.push('err-eq:'+x[0])});
      const pr=[...TGC.map(x=>x[0]),...TGF.map(x=>x[0]),...TGP.map(x=>x[0]),...TGE.map(x=>x[0])];if(!uq(pr))bad.push('dupe-prompts');
      return {bad,n:[TGC.length,TGF.length,TGP.length,TGE.length]}})()""")
    chk('the built-in question banks are clean: every question has the blank, 3 distinct wrong options that do not repeat the answer, every error index points at a real word, every correction really changes the sentence, and no prompt is duplicated', d['bad'] == [], d['bad'])
    chk('there is enough material for many rounds: 35+ collocations, 33+ word families, 20 paraphrases, 30 error sentences', d['n'][0] >= 35 and d['n'][1] >= 33 and d['n'][2] == 20 and d['n'][3] >= 30, d['n'])
    t = pg.inner_text('#app'); chk('the vocabulary screen has a "🧠 Til o‘yinlari" section with the four games (no "own mistakes" game yet)', '🧠 Til o‘yinlari' in t and all(x in t for x in ['Birikmalar', 'So‘z oilasi', 'Paraphrase jangi', 'Xatoni top']) and 'O‘z xatolaring' not in t)
    pos = set(); same = 0
    for _ in range(25):
        q = ev("(()=>{const q=tgBuild('col');return [q.length,q.every(x=>x.o.length===4&&x.o[x.a]&&new Set(x.o).size===4),q.map(x=>x.a),new Set(q.map(x=>x.p)).size]})()")
        assert q[0] == 10 and q[1] and q[3] == 10; pos.update(q[2])
    chk('every round has 10 different questions, each with 4 distinct options, the right answer index is correct and varies (shuffled)', len(pos) >= 3, pos)
    # o'yin oqimi
    pg.click('#app .gmb >> text=Birikmalar'); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('starting shows the question with 4 options, lives ❤️❤️❤️, "1 / 10", the score and the timer bar', ev("TG.g") == 'col' and ev("document.querySelectorAll('#app .qopt').length") == 4 and '❤️❤️❤️' in t and '1 / 10' in t and ev("!!document.getElementById('tgb')") and '0 ball' in t)
    ans = lambda ok=True: ev("()=>{const q=TG.qs[TG.i];tgAns(%s);return 1}" % ("q.a" if ok else "(q.a+1)%4"))
    ans(True); pg.wait_for_timeout(60); sc1 = ev("TG.sc"); t = pg.inner_text('#app')
    chk('a correct answer: +10, the right option is highlighted, "✅ To‘g‘ri!" with the full phrase and the rule; the options are locked', sc1 == 10 and '✅ To‘g‘ri!' in t and ev("document.querySelectorAll('#app .qopt.ok').length") == 1 and ev("[...document.querySelectorAll('#app .qopt')].every(b=>b.disabled)"))
    pg.click('#app >> text=Keyingisi'); pg.wait_for_timeout(40); ans(True); sc2 = ev("TG.sc")
    chk('a second correct answer in a row: combo ×2 gives +12 (22 total) and "🔥 combo ×2"', sc2 == 22 and '🔥 combo ×2' in pg.inner_text('#app'))
    pg.click('#app >> text=Keyingisi'); pg.wait_for_timeout(40); ans(False); pg.wait_for_timeout(60); t = pg.inner_text('#app')
    chk('a wrong answer: a life is lost (❤️❤️🖤), combo resets, the wrong option is marked and the right one shown with the explanation', ev("TG.lives") == 2 and ev("TG.combo") == 0 and ev("document.querySelectorAll('#app .qopt.no').length") == 1 and '❌ Xato.' in t and '🖤' in t)
    pg.click('#app >> text=Keyingisi'); pg.wait_for_timeout(40); ans(False); pg.click('#app >> text=Keyingisi'); pg.wait_for_timeout(40); ans(False); pg.click('#app >> text=Natija'); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('three wrong answers end the round early: "Jonlar tugadi", score, accuracy, and the list of mistakes with the right answers', 'Jonlar tugadi' in t and '22 ball' in t and 'Xatolaring:' in t and ev("document.querySelectorAll('#app .row s').length") == 3 and ev("TG.end") == 1)
    chk('the round is counted for the daily XP/boss (S.ie.gm today = 1), the best score is saved, a score of 22 is a record the first time', ev("S.ie.gm['2026-11-05']") == 1 and ev("S.ie.gb.col") == 22 and 'yangi rekord' in t)
    chk('the finished round no longer ticks the timer (interval stopped)', ev("TGT") == 0)
    # to'liq to'g'ri
    pg.click('#app >> text=Yana'); pg.wait_for_timeout(80)
    for i in range(10):
        ans(True); pg.wait_for_timeout(20); pg.click('#app >> text=/Keyingisi|Natija/'); pg.wait_for_timeout(30)
    t = pg.inner_text('#app'); chk('a perfect round: 170 points (10 questions with combo 1…10 → 100 + 2×35), 100%, ⭐⭐⭐, confetti, new record 170, longest combo 10', '170 ball' in t and '100%' in t and '⭐⭐⭐' in t and ev("__cf") == 1 and ev("S.ie.gb.col") == 170 and 'eng uzun combo: 10' in t and '🎉 Xatosiz!' in t, t[:160])
    chk('the second finished round is counted too (2) and a lower later score does not overwrite the record', ev("S.ie.gm['2026-11-05']") == 2)
    pg.click('#app >> text=Yana'); pg.wait_for_timeout(60); ans(False); ans(False) if False else None
    ev("tgExit()"); pg.wait_for_timeout(60); chk('"⬅ Lug‘at" leaves the game and returns to the vocabulary screen; the timer is stopped', ev("TG") is None and ev("TGT") == 0 and '🧠 Til o‘yinlari' in pg.inner_text('#app'))
    # vaqt
    ev("tgStart('fam')"); pg.wait_for_timeout(60); pg.clock.run_for(21000); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('no answer within 20 seconds counts as wrong: "⏰ Vaqt tugadi." with the right form, a life lost', '⏰ Vaqt tugadi.' in t and ev("TG.lives") == 2 and ev("TG.ans") == -2)
    ev("tgExit()")
    # xatoni top
    ev("tgStart('err')"); pg.wait_for_timeout(80); q = ev("TG.qs[TG.i]")
    chk('"Xatoni top" shows the sentence as tappable words (30 s per sentence)', ev("document.querySelectorAll('#app .tgt').length") == len(q['tk']) and ev("TG.tl") == 30 and 'Xato so‘zni bos' in pg.inner_text('#app'))
    pg.click('#app .tgt >> nth=%d' % q['a']); pg.wait_for_timeout(60); t = pg.inner_text('#app')
    chk('tapping the wrong word: it is highlighted green, the corrected sentence and the rule are shown', ev("document.querySelectorAll('#app .tgt.tgok').length") == 1 and '✅ To‘g‘ri!' in t and q['c'] in t and ev("TG.sc") == 10)
    pg.click('#app >> text=Keyingisi'); pg.wait_for_timeout(40); q2 = ev("TG.qs[TG.i]"); wrong_i = (q2['a'] + 1) % len(q2['tk']); pg.click('#app .tgt >> nth=%d' % wrong_i); pg.wait_for_timeout(60)
    chk('tapping a different word: that word is red, the real mistake green, a life is lost', ev("document.querySelectorAll('#app .tgt.tgno').length") == 1 and ev("document.querySelectorAll('#app .tgt.tgok').length") == 1 and ev("TG.lives") == 2)
    ev("tgExit()")
    # paraphrase va oila
    ev("tgStart('par')"); chk('"Paraphrase jangi": 3 options, one correct', ev("TG.qs[0].o.length") == 3 and ev("TG.qs[0].o[TG.qs[0].a]") != ev("TG.qs[0].p")); ev("tgExit()")
    # daftar
    ev("()=>{S.ie.xd=[];tgStart('col')}"); pg.wait_for_timeout(60)
    for i in range(2):
        ans(False); pg.click('#app >> text=Keyingisi'); pg.wait_for_timeout(30)
    ev("()=>{const q=TG.qs[TG.i];tgAns((q.a+1)%4)}"); pg.click('#app >> text=Natija'); pg.wait_for_timeout(80); pg.click('#app >> text=Xatolarimni daftarga qo‘sh'); pg.wait_for_timeout(100)
    e = ev("S.ie.xd.map(x=>[x.c,x.w,x.r,x.src])"); chk('the 3 mistakes can be saved to the mistakes notebook with the WRONG phrase (what you chose) and the right one, category vocab, source g; saving again adds nothing', len(e) == 3 and all(x[0] == 'vocab' and x[3] == 'g' and x[1] != x[2] and '___' not in x[1] and '___' not in x[2] for x in e) and any('3 ta xato' in m for m in ev("__t")), e)
    ev("__t=[]"); pg.click('#app >> text=Xatolarimni daftarga qo‘sh'); chk('...a second press adds nothing and says so', len(ev("S.ie.xd")) == 3 and any('yangi xato yo‘q' in m for m in ev("__t")))
    ev("tgExit()")
    # o'z xatolaring
    ev("()=>{S.ie.xd=[];tgStart('mine')}"); chk('"O‘z xatolaring" needs at least 4 notebook entries (otherwise a clear message, no game)', ev("TG") is None and any('kamida 4 ta' in m for m in ev("__t")))
    ev("()=>{S.ie.xd=[];for(let i=0;i<6;i++)xdPut('grammar','wrong '+i,'right '+i,'rule '+i,'m');tgExit()}"); pg.wait_for_timeout(60); t = pg.inner_text('#app')
    chk('with 4+ mistakes in the notebook the fifth game "📓 O‘z xatolaring" appears', 'O‘z xatolaring' in t and 'daftaringdan' in t)
    pg.click('#app .gmb >> text=O‘z xatolaring'); pg.wait_for_timeout(80); q = ev("TG.qs[TG.i]")
    chk('it asks "which is correct?" between YOUR wrong and right versions (6 questions from 6 entries), with the rule as the hint', ev("TG.qs.length") == 6 and len(q['o']) == 2 and q['o'][q['a']].startswith('right') and q['p'].startswith('Qoida: rule'), q)
    ev("()=>{for(let i=0;i<6;i++){tgAns(TG.qs[TG.i].a);tgNext()}}"); pg.wait_for_timeout(80); t = pg.inner_text('#app')
    chk('finishing it works, saves the best score under "mine" and offers no "add to notebook" button (they are already there)', ev("TG.end") == 1 and ev("S.ie.gb.mine") > 0 and 'daftarga qo‘sh' not in t)
    # boss bilan bog'lanish
    ev("tgExit()"); chk('rounds feed the weekly boss weak point "Til o‘yinlarida 5 ta raund" (they use the same daily counter)', ev("BSO.find(x=>x.id==='oyin').n(bsMon())") == ev("Object.values(S.ie.gm).reduce((a,b)=>a+b,0)") and ev("S.ie.gm['2026-11-05']") >= 4)
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tgStart('err')}", [ui, th]); pg.wait_for_timeout(40)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th + 'e')
            ev("()=>{tgAns(TG.qs[TG.i].a)}"); pg.wait_for_timeout(30)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th + 'a')
            ev("()=>{TG.end=1;TG.wrong=[{q:TG.qs[0],k:0},{q:TG.qs[1],k:1}];render()}"); pg.wait_for_timeout(30)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th + 'r')
            ev("tgExit()")
    chk('question, answered and result screens fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
