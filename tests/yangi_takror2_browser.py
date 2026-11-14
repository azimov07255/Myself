import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Takror 2: maqsad, qo'shish (ayat/bet/pora), trekker, aylanish, pora yangiligi, integratsiya. Soat: 2026-11-09 (dushanba) 10:00.
import sys, json
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
GC = "document.querySelector('#app section[aria-label=\"Takror maqsadi\"]').innerText"
VP = json.load(open((ROOT + '/data/quran-mushaf.json'), encoding='utf-8'))['vp']
with Run('tq', when=(2026, 11, 9, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;const q=S.q;q.tk=undefined;q.cr={};q.rd={};q.m=q.m||[];for(let i=0;i<114;i++)q.m[i]=0;q.rs={};q.jz=undefined;q.jd={};q.cur=1;TQF={m:'a',s:-1,a:1,b:0,pa:1,pb:1,j:[],d:''};TQSEL='';TQJ=0;tab='q';QT='t';QG=false;TKV='k';render()}""")
    pg.wait_for_timeout(150)
    # ---------- xarita
    pages = ev("[...Array(6236).keys()].map(tqPage)")
    chk('the embedded ayah-to-page table is EXACT: all 6236 ayahs map to the same Mushaf page as the full 1.8 MB data file', pages == VP, sum(1 for a, b in zip(pages, VP) if a != b))
    chk('spot checks: Fotiha 1:1 → page 1; Baqara 2:1 → 2; 2:286 → 49; Oli Imron 3:1 → 50; An-Nas 114:6 → 604', [ev("tqPage(tqIdx(0,1))"), ev("tqPage(tqIdx(1,1))"), ev("tqPage(tqIdx(1,286))"), ev("tqPage(tqIdx(2,1))"), ev("tqPage(tqIdx(113,6))")] == [1, 2, 49, 50, 604])
    r = ev("tqPg(0,1,7)"); chk('the whole Fotiha is one page (≈ 1,0 bet)', r['pa'] == 1 and r['pb'] == 1 and r['pg'] == 1)
    r = ev("tqPg(1,1,3)"); chk('3 of the 5 ayahs that begin on page 2 → about 0,6 bet', r['pa'] == 2 and r['pb'] == 2 and abs(r['pg'] - 0.6) < 0.01, r)
    r = ev("tqPg(1,1,286)"); chk('the whole Baqara spans pages 2–49 and counts about 48 pages', r['pa'] == 2 and r['pb'] == 49 and 47.5 <= r['pg'] <= 48.5, r)
    r = ev("tqPg(113,6,6)"); chk('a single ayah never counts less than 0,1 bet', r['pg'] >= 0.1)
    chk('the juz table is in place: 30 juz, juz 1 = pages 1–21', ev("J[0]") == 1 and ev("J[1]") == 22 and ev("J[30]") == 605)
    # ---------- maqsad
    t = pg.inner_text('#app'); chk('the Takror tab opens on the new “📖 Bugun” view by default, with the goal card, add form, cycle, tracker and freshness map; the old Sabqi–Manzil and Sura qutilari tabs are still there', '📖 Bugungi takror' in t and '➕ Takrorlaganimni qo‘shish' in t and '🔄 Takror aylanishi' in t and '📈 Takror trekeri' in t and '🌡 Pora yangiligi' in t and 'Sabqi · Manzil' in t and 'Sura qutilari' in t and ev("TKV") == 'k')
    chk('with no goal set the card says “—” and offers “Maqsadsiz”; nothing is logged yet', '—' in ev(GC) and 'Bugun hali takror qo‘shilmagan' in pg.inner_text('#app'))
    ev("tqGoal('bet',5)"); pg.wait_for_timeout(60); chk('goal 5 bet: the ring and text show 0 / 5 bet and 0 / 0,3 pora (1 pora ≈ 20 bet)', ev("tqGoalPg()") == 5 and '0 / 5' in ev(GC) and '0 / 0,3' in ev(GC).replace('\n', ' '))
    ev("tqGoal('pora',1)"); chk('goal 1 pora = 20 bet', ev("tqGoalPg()") == 20 and ev("tqS().g.u") == 'pora')
    ev("tqUnit('bet')"); chk('switching the unit converts the goal (1 pora → 20 bet)', ev("tqS().g.u") == 'bet' and ev("tqS().g.n") == 20); ev("tqUnit('pora')"); chk('…and back (20 bet → 1 pora)', ev("tqS().g.n") == 1)
    ev("tqGoal('pora',99)"); chk('limits: pora up to 10, bet up to 200', ev("tqS().g.n") == 10); ev("tqGoal('bet',999)"); chk('…bet 200', ev("tqS().g.n") == 200); ev("tqGoal('bet',0)"); chk('0 means no goal', ev("tqGoalPg()") == 0); ev("tqGoal('bet',5)")
    # ---------- qo'shish
    rd0 = ev("JSON.stringify(S.q.rd)")
    ev("()=>{tqSet('s',1)}"); chk('choosing Baqara resets the range to 1–286', ev("TQF.a") == 1 and ev("TQF.b") == 286)
    ev("()=>{TQF.a=1;TQF.b=50;render()}"); pg.wait_for_timeout(60); t = pg.inner_text('#app'); P = ev("tqPrev()"); chk('the preview shows the ayah range, the page span and “≈ x bet · y pora” (Baqara 1–50)', 'Baqara 1–50-oyat' in t and P['pa'] == 2 and 'bet ·' in t and 'pora' in t, t[t.find('Baqara 1–50'):][:120])
    ev("tqAdd()"); pg.wait_for_timeout(80); e = ev("tqList(dk())[0]"); chk('adding stores the entry: type, sura, ayahs, page span, pages and a label; a toast shows the total', e['m'] == 'a' and e['s'] == 1 and e['a'] == 1 and e['b'] == 50 and e['pa'] == 2 and e['pg'] > 5 and e['t'] == 'Baqara 1–50-oyat' and any('Qo‘shildi: Baqara 1–50-oyat' in m for m in ev("__t")), e)
    chk('takror is counted SEPARATELY: the reading/hatm pages (q.rd) are untouched', ev("JSON.stringify(S.q.rd)") == rd0)
    pg.wait_for_timeout(60); chk('the goal card now lists the entry and the progress moved (the ring is above 0%)', 'Baqara 1–50-oyat' in ev(GC) and ev("tqPages(dk())") == e['pg'])
    ev("()=>{TQF.a=60;TQF.b=20;render()}"); P = ev("tqPrev()"); chk('a reversed range is fixed (from 60 to 20 → 60–60) and values are clamped to the sura (1–286)', P['items'][0]['a'] == 60 and P['items'][0]['b'] == 60); ev("()=>{TQF.a=0;TQF.b=9999;render()}"); P = ev("tqPrev()"); chk('…out-of-range numbers clamp to 1–286', P['items'][0]['a'] == 1 and P['items'][0]['b'] == 286)
    ev("tqSet('s',112)"); ev("tqAdd()"); chk('a short sura works (Ixlos, 4 ayahs, a fraction of one page)', any(x['s'] == 112 and 0.1 <= x['pg'] <= 1 for x in ev("tqList(dk())")))
    Y = '2026-11-08'; ev("(y)=>tqDate(y)", Y); ev("()=>{tqMode('b');TQF.pa=100;TQF.pb=104;render()}"); ev("tqAdd()"); y = ev("tqList('2026-11-08')"); chk('bet mode with “Kecha” as the date logs 5 pages (100–104) on yesterday, not today', len(y) == 1 and y[0]['pg'] == 5 and y[0]['pa'] == 100 and y[0]['pb'] == 104 and y[0]['t'] == 'Mushaf 100–104-betlar' and not any(x['pa'] == 100 for x in ev("tqList(dk())")))
    ev("()=>{__t=[];tqDate('2026-11-12');}"); chk('a future date is not accepted (falls back to today)', ev("TQF.d") == ''); ev("()=>{TQF.d='2026-11-12';tqAdd()}"); chk('…and adding for a future date is refused', any('Kelajak sana' in m for m in ev("__t")))
    ev("()=>{tqDate('2026-11-05');tqMode('p');TQF.j=[];tqJ(2);tqJ(3);}"); P = ev("tqPrev()"); chk('juz mode: choosing juz 2 and 3 previews both with their real page counts (20 + 20 = 40) and labels', P['pg'] == (ev("J[2]-J[1]") + ev("J[3]-J[2]")) and P['t'] == '2-pora, 3-pora'); ev("tqAdd()"); chk('adding writes one entry per juz on the chosen date and clears the selection', len(ev("tqList('2026-11-05')")) == 2 and ev("TQF.j.length") == 0)
    ev("()=>{__t=[];tqAdd()}"); chk('adding with nothing selected asks you to choose', any('nimani takrorlaganingni' in m for m in ev("__t")))
    ev("()=>{TQF.d='';TQF.m='a'}"); id0 = ev("tqList(dk())[0].id"); ev("(id)=>tqDel(dk(),id)", id0); chk('an entry can be deleted', not ev("tqList(dk()).some(x=>x.id===%s)" % json.dumps(id0)))
    # ---------- eski yozuvlar va avtomatik yozish
    ev("()=>{const q=S.q;q.tk=undefined;q.cr={'2026-11-01':[{s:3,a:77,b:80,x:1},{s:3,a:81,b:82,x:0}]};tqMig();tqMig()}"); L = ev("tqList('2026-11-01')"); chk('old “o‘zim tanlagan takror” entries are carried over once (only the ones you had ticked) and marked as old', len(L) == 1 and L[0]['pg'] == 4 and L[0]['src'] == 'old' and L[0]['t'].startswith('Niso'))
    ev("()=>{const q=S.q;q.tk=undefined;q.m[1]=10;q.m[0]=1;q.rs={};q.rd={};rate(1,2)}"); L = ev("tqList(dk())"); chk('a Sabqi/Manzil rating (“Yaxshi”) is also recorded as takror (10 pages of Baqara, source “Sabqi/Manzil”) and, by the new default rule, is NOT added to the reading counter', len(L) == 1 and L[0]['src'] == 'rate' and L[0]['pg'] == 10 and L[0]['s'] == 1 and (ev("S.q.rd[dk()]") or 0) == 0)
    ev("()=>{const q=S.q;q.tk=undefined;q.rd={};q.jz={sel:[1,2],per:1,ptr:0};jzDone()}"); L = ev("tqList(dk())"); chk('finishing a juz round records that juz as takror (juz 1 → 21 pages, source “jz”)', len(L) == 1 and L[0]['src'] == 'jz' and L[0]['j'] == 1 and L[0]['pg'] == 21)
    ev("()=>{jzDone()}"); chk('the next round records juz 2 (20 pages)', ev("tqList(dk()).slice(-1)[0].j") == 2 and ev("tqList(dk()).slice(-1)[0].pg") == 20)
    # ---------- trekker
    ev("""()=>{const q=S.q;q.tk=undefined;q.cr={};q.jz=undefined;q.rd={};const A=(k,p)=>tqLog({m:'b',pa:1,pb:1,pg:p,t:'x'},k);A('2026-11-09',5);A('2026-11-08',6);A('2026-11-07',5);A('2026-11-05',7);A('2026-11-04',7);A('2026-10-01',604);tqGoal('bet',5);TQSEL='';TQO.t=1;render()}""")
    St = ev("tqStats()"); chk('streaks: current 3 days (9, 8, 7 Nov), best 3; the last 30 days hit the goal on 5 days (17%); the month holds 30 bet (1,5 pora)', St['cur'] == 3 and St['best'] == 3 and St['pc30'] == 17 and St['mp'] == 30, St)
    chk('all-time total is 634 bet = 1,05 Qur‘on (604 pages per full Qur‘on)', St['tot'] == 634 and abs(St['turns'] - 1.05) < 0.06 and St['act'] == 6, St)
    ev("tqLog({m:'b',pa:1,pb:1,pg:5,t:'y'},'2026-11-06')"); St = ev("tqStats()"); chk('adding the missing day (6 Nov) joins the runs: current streak 6 days (4…9 Nov)', St['cur'] == 6 and St['best'] == 6, St)
    ev("tqDel('2026-11-09',tqList('2026-11-09')[0].id)"); St = ev("tqStats()"); chk('if today is not done yet the streak is counted up to yesterday (5 days) instead of showing 0', St['cur'] == 5, St)
    ev("()=>{tqLog({m:'b',pa:1,pb:1,pg:5,t:'x'},'2026-11-09');render()}"); pg.wait_for_timeout(80)
    chk('the heat map has 84 day cells (12 weeks) coloured by progress against the goal: 4 = goal met, 3 = half, 2 = some, 1 = none', ev("document.querySelectorAll('#app .eyc').length") == 84 and ev("document.querySelector('#app .eyc[data-d=\"2026-11-09\"]').dataset.l") == '4' and ev("document.querySelector('#app .eyc[data-d=\"2026-11-03\"]').dataset.l") == '1' and ev("tqLevel(2.5,5)") == '3' and ev("tqLevel(1,5)") == '2' and ev("tqLevel(0,5)") == '1')
    ev("tqSel('2026-11-08')"); pg.wait_for_timeout(60); chk('tapping a day lists its entries with the total against the goal and lets you delete', '8-noyabr · 6 bet / 5' in pg.inner_text('#app') and ev("document.querySelectorAll('#app .goal .x').length") >= 1); ev("tqSel('2026-11-08')"); chk('tapping again closes it', ev("TQSEL") == '')
    St = ev("tqStats()"); chk('weekly totals cover 8 weeks, the last being this week (Mon 9 Nov = 5)', len(St['wk']) == 8 and St['wk'][-1]['p'] == 5 and St['wk'][-1]['k'] == '2026-11-09', St['wk'])
    ev("tqGoal('bet',0)"); ev("render()"); chk('without a goal, levels are by pages (≥10 high, ≥5 mid, >0 low) and a streak counts any day with takror', ev("tqLevel(12,0)") == '4' and ev("tqLevel(6,0)") == '3' and ev("tqLevel(1,0)") == '2' and ev("tqStats().cur") >= 1); ev("tqGoal('bet',5)")
    # ---------- aylanish
    ev("()=>{const q=S.q;q.tk=undefined;for(let i=0;i<114;i++)q.m[i]=0;tqGoal('bet',5);render()}"); pg.wait_for_timeout(60); chk('with nothing memorised the cycle card explains what to do first', 'Avval Yodlash bo‘limida' in pg.inner_text('#app'))
    ev("()=>{const q=S.q;q.m[0]=1;q.m[1]=10;q.m[113]=0.5;render()}"); pg.wait_for_timeout(60); P = ev("tqCy()"); chk('memorised parts are summed (Fotiha 1 + Baqara first 10 + the whole An-Nas, now 0,4 bet = 11,4 bet)', P['tot'] == 11.4 and ev("tqSegs().length") == 3, P)
    chk('before starting, the card offers 15/20/30/45/60 days and shows the daily share', '30 kun' in pg.inner_text('#app') and 'kuniga ≈ 0,4 bet' in pg.inner_text('#app'))
    ev("tqCyStart(30)"); pg.wait_for_timeout(60); P = ev("tqCy()"); chk('started: day 1 of 30; today’s share is half a page from the beginning (Fotiha, page 1)', ev("tqS().cy.on") == 1 and P['port'] == 0.5 and P['items'][0]['s'] == 0 and P['items'][0]['pa'] == 1 and P['items'][0]['pg'] == 0.5 and '1-kun / 30' in pg.inner_text('#app'), P)
    ev("tqCyDone()"); pg.wait_for_timeout(60); c = ev("tqS().cy"); chk('“Bugungi ulushni bajardim” logs the share as takror (source “cy”) and moves the pointer; it cannot be pressed twice the same day', c['p'] == 0.5 and c['last'] == '2026-11-09' and any(e['src'] == 'cy' for e in ev("tqList(dk())"))); n0 = len(ev("tqList(dk())")); ev("tqCyDone()"); chk('…second press does nothing', len(ev("tqList(dk())")) == n0 and '✅ Bugungi ulush bajarildi' in pg.inner_text('#app'))
    ev("()=>{const c=tqS().cy;c.start='2026-10-20';c.p=0;c.last='';render()}"); P = ev("tqCy()"); chk('if you fall behind (day 21 of 30 with nothing done) the remaining pages are spread over the remaining 9–10 days: the daily share grows to about 1 page', P['el'] == 20 and P['left'] == 10 and P['port'] == 1 and P['items'][0]['pg'] == 1, P)
    ev("()=>{const c=tqS().cy;c.start='2026-10-01';c.p=2;render()}"); P = ev("tqCy()"); chk('past the deadline with pages remaining → “Muddat o‘tdi” and a +7 days button', P['over'] and 'Muddat o‘tdi' in pg.inner_text('#app')); ev("tqCyExt()"); chk('+7 days extends the cycle', ev("tqS().cy.days") == 37)
    ev("()=>{const c=tqS().cy;c.days=30;c.start='2026-11-08';c.p=11.0;c.last='';render()}"); ev("tqCyDone()"); chk('finishing the last pages ends the cycle, counts it (1 time) and congratulates', ev("tqS().cy.on") == 0 and ev("tqS().cy.n") == 1 and any('Aylanish tugadi' in m for m in ev("__t")))
    ev("tqCyStart(20)"); ev("tqCyStop()"); chk('the cycle can be stopped', ev("tqS().cy.on") == 0)
    # ---------- pora yangiligi
    ev("""()=>{const q=S.q;q.tk=undefined;q.cr={};q.m[113]=0;q.m[1]=10;q.m[0]=1;const A=(k,pa,pb)=>tqLog({m:'b',pa,pb,pg:pb-pa+1,t:'x'},k);A('2026-11-06',5,10);A('2026-10-20',22,60);A('2026-11-02',100,110);TQJ=0;render()}""")
    F = {x['n']: x for x in ev("tqFresh()")}; chk('each of the 30 juz gets the date of its latest takror from the page ranges: juz 1 → 3 days ago (green), juz 2 and 3 → 20 days ago (yellow), juz 6 → 7 days (green), the rest never (grey)', F[1]['age'] == 3 and F[1]['c'] == 'a' and F[2]['age'] == 20 and F[2]['c'] == 'c' and F[3]['age'] == 20 and F[6]['age'] == 7 and F[6]['c'] == 'a' and F[10]['c'] == 'n' and len(F) == 30, {k: (v['age'], v['c']) for k, v in F.items() if k in (1, 2, 3, 6, 10)})
    chk('colour boundaries: 7 days green, 8 light green, 14 light green, 15 yellow, 30 yellow, 31 red', all(ev("(a)=>{const T=dk();tqS().d={};tqLog({m:'b',pa:1,pb:1,pg:1,t:'x'},rwAdd(T,-a));return tqFresh()[0].c}", a) == c for a, c in ((7, 'a'), (8, 'b'), (14, 'b'), (15, 'c'), (30, 'c'), (31, 'd'))))
    ev("""()=>{const q=S.q;q.tk=undefined;q.cr={};q.m[113]=0;const A=(k,pa,pb)=>tqLog({m:'b',pa,pb,pg:pb-pa+1,t:'x'},k);A('2026-11-06',5,10);A('2026-10-20',22,60);TQJ=0;render()}""")
    F = ev("tqFresh().filter(x=>x.mem).map(x=>x.n)"); chk('memorised juz are marked (ringed): only juz 1 has memorised pages here', F == [1], F)
    pg.wait_for_timeout(60); t = pg.inner_text('#app'); chk('the card names the memorised juz that has waited longest (juz 1: 3 days, the only one memorised)', 'Eng uzoq takrorlanmagan yodlangan pora: 1-pora' in t and '(3 kun)' in t)
    ev("tqJz(2)"); pg.wait_for_timeout(60); chk('tapping a juz shows its details (last takror date and how long ago)', '2-pora · oxirgi takror 20 kun oldin (20-oktyabr)' in pg.inner_text('#app')); ev("tqJz(2)")
    ev("tqJz(9)"); chk('a juz that was never repeated says so', 'takror yozilmagan' in pg.inner_text('#app')); ev("tqJz(9)")
    # ---------- integratsiya
    ev("()=>{const q=S.q;q.tk=undefined;tqGoal('bet',5);tqLog({m:'b',pa:1,pb:1,pg:3,t:'x'},dk());tab='h';BV='j';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('Bugun shows a “📖 Takror: 3 / 5 bet · 0,2 / 0,3 pora” row once a goal or takror exists', '📖' in t and 'Takror: 3 / 5 bet' in t)
    ev("()=>{[...document.querySelectorAll('#app button.row')].find(b=>b.textContent.includes('Takror:')).click()}"); pg.wait_for_timeout(100); chk('tapping it opens Qur‘on → Takror → Bugun', ev("tab") == 'q' and ev("QT") == 't' and ev("TKV") == 'k')
    ev("()=>{S.q.tk=undefined;tab='h';render()}"); pg.wait_for_timeout(60); chk('with no goal and nothing logged the Bugun row is not shown', not ev("[...document.querySelectorAll('#app button.row')].some(b=>b.textContent.includes('Takror:'))"))
    ev("()=>{tqGoal('bet',5);tqLog({m:'b',pa:1,pb:1,pg:5,t:'x'},dk())}"); chk('a takror contract metric exists in the Nafs shartnoma (📖 Qur‘on takrori, bet) and reads today’s pages', ev("NKM.tq[2](dk())") == 5 and ev("nkAdd('tq',3,10000,[])") is True)
    ev("kcOpen()"); pg.wait_for_timeout(100); chk('“Kunni yopish” shows today’s takror in the summary (📖 5/5 bet)', '📖 5/5 bet' in pg.inner_text('#kcv')); ev("kcClose()")
    bad = []
    ev("""()=>{const q=S.q;q.tk=undefined;q.m[0]=1;q.m[1]=10;q.m[113]=.5;tqGoal('pora',1.5);for(let i=0;i<40;i++)tqLog({m:'a',s:1,a:1,b:50,pa:2,pb:6,pg:5+(i%4),t:'Baqara juda uzun nomli yozuv 1–50-oyat'},rwAdd(dk(),-i));tqCyStart(30);TQO.t=1;TQSEL='2026-11-08'}""")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='q';QT='t';TKV='k';QG=false;render()}", [ui, th]); pg.wait_for_timeout(80)
            ok1 = ev("document.documentElement.scrollWidth<=window.innerWidth+1"); ev("()=>{tqMode('b');render()}"); ok2 = ev("document.documentElement.scrollWidth<=window.innerWidth+1"); ev("()=>{tqMode('p');tqJ(7);render()}"); ok3 = ev("document.documentElement.scrollWidth<=window.innerWidth+1"); ev("()=>{tqMode('a');render()}")
            if not (ok1 and ok2 and ok3): bad.append(ui + th)
    chk('the whole Takror view (goal, three add modes, cycle, tracker, freshness) fits the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
