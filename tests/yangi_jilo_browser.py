import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Jilo: sanalar, bekor qilish, qidiruv, sozlamalar qidiruvi, takror hisobi qoidasi, surish maslahati, tizim tekshiruvi. Soat: 2026-11-09 10:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
BL = "[{id:'uyqu1',t:'Uxlash',s:1380,e:1800,d:[0,1,2,3,4,5,6]},{id:'k1',t:'Dokon',s:540,e:1020,d:[0,1,2,3,4,5,6]},{id:'z1',t:'Zal',s:1050,e:1110,d:[0,1,2,3,4,5,6]}]"
with Run('jl', when=(2026, 11, 9, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""(B)=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;for(const k of ['trk_dfmt','trk_ud','trk_tqrd','trk_swh'])localStorage.removeItem(k);
      const q=S.q;q.tk=undefined;q.cr={};q.rd={};for(let i=0;i<114;i++)q.m[i]=0;q.m[1]=10;q.m[0]=1;S.nf=undefined;S.km=[];S.kv={};S.ib=[];S.bl=eval(B);S.done={};S.rt=undefined;SDQ='';SQ='';SO=false;ED=null;tab='h';BV='j';VD=null;render()}""", BL)
    pg.wait_for_timeout(120)
    # ---------- sanalar
    chk('dates are shown in Uzbek by default: 2026-11-09 → “9-noyabr”; another year adds the year; text that is not a date is returned unchanged', ev("dU('2026-11-09')") == '9-noyabr' and ev("dU('2027-01-30')") == '30-yanvar 2027' and ev("dU('abc')") == 'abc' and ev("dU('')") == '')
    ev("uiS('trk_dfmt','i')"); chk('the old year-month-day style comes back from Settings (Sana ko‘rinishi → 2026-11-09)', ev("dU('2026-11-09')") == '2026-11-09'); ev("uiS('trk_dfmt','u')")
    ev("()=>{tqLog({m:'b',pa:1,pb:1,pg:4,t:'x'},'2026-11-08');TQSEL='2026-11-08';TQO.t=1;tab='q';QT='t';TKV='k';render()}"); pg.wait_for_timeout(80); chk('takror tracker, freshness and add-form now show “8-noyabr”, not “2026-11-08”', '8-noyabr · 4 bet' in pg.inner_text('#app') and '2026-11-08 ·' not in pg.inner_text('#app'))
    # ---------- bekor qilish
    ev("()=>{S.q.tk=undefined;tqLog({m:'b',pa:1,pb:1,pg:4,t:'Mushaf 1-bet'});TQT='k';tab='q';QT='t';TKV='k';render()}"); id0 = ev("tqList(dk())[0].id"); ev("(id)=>tqDel(dk(),id)", id0); pg.wait_for_timeout(80)
    chk('deleting a takror entry shows a bar with the message and “↩︎ Bekor qilish”', ev("document.getElementById('udb').style.display") == 'flex' and 'Takror yozuvi o‘chirildi' in pg.inner_text('#udb') and '↩︎ Bekor qilish' in pg.inner_text('#udb') and ev("tqList(dk()).length") == 0)
    ev("udDo()"); pg.wait_for_timeout(60); chk('pressing it brings the entry back and hides the bar', ev("tqList(dk()).length") == 1 and ev("document.getElementById('udb').style.display") == 'none')
    ev("(id)=>tqDel(dk(),id)", ev("tqList(dk())[0].id")); pg.clock.run_for(8500); pg.wait_for_timeout(60); chk('after 8 seconds the bar disappears by itself (the deletion stays)', ev("document.getElementById('udb').style.display") == 'none' and ev("tqList(dk()).length") == 0); ev("udDo()"); chk('…and a late press does nothing', ev("tqList(dk()).length") == 0)
    ev("()=>{window.confirm=()=>false;kmPre(0)}"); ev("kmDel(S.km[0].id)"); chk('declining the “are you sure” question changes nothing and shows no bar', len(ev("S.km")) == 1 and (ev("document.getElementById('udb').style.display") in ('none',)))
    ev("()=>{window.confirm=()=>true}"); ev("kmDel(S.km[0].id)"); chk('metrics, contracts, experiments, plans and notes are covered too (metric deleted → bar)', len(ev("S.km")) == 0 and 'Ko‘rsatkich o‘chirildi' in pg.inner_text('#udb')); ev("udDo()"); chk('…and restored', len(ev("S.km")) == 1)
    ev("()=>{nkAdd('pom',3,1000,[])}"); ev("nkDel(S.nf.c[0].id)"); chk('shartnoma delete → bar', 'Shartnoma o‘chirildi' in pg.inner_text('#udb') and len(ev("S.nf.c")) == 0); ev("udDo()"); chk('shartnoma restored', len(ev("S.nf.c")) == 1)
    ev("()=>{S.ib=[{id:5,t:'Kitob olish',d:dk(),x:0}]}"); ev("ibDel(5)"); chk('quick note delete → bar and restore', 'Yozuv o‘chirildi' in pg.inner_text('#udb') and len(ev("S.ib")) == 0); ev("udDo()"); chk('…', len(ev("S.ib")) == 1)
    ev("()=>{eb(1)}"); ev("edl()"); chk('plan delete → bar and restore (the plan comes back with its time)', 'Reja o‘chirildi' in pg.inner_text('#udb') and not ev("bl().some(b=>b.id==='k1')")); ev("udDo()"); chk('…', ev("bl().some(b=>b.id==='k1'&&b.s===540)"))
    ev("uiS('trk_ud','0')"); ev("(id)=>{tqLog({m:'b',pa:1,pb:1,pg:1,t:'t'});tqDel(dk(),tqList(dk())[0].id)}", 0); ev("document.getElementById('udb')&&(document.getElementById('udb').style.display='none')"); chk('the bar can be switched off in Settings (then nothing appears)', ev("document.getElementById('udb').style.display") == 'none'); ev("uiS('trk_ud','1')")
    # ---------- qidiruv
    ev("""()=>{S.q.tk=undefined;tqLog({m:'a',s:1,a:1,b:5,pa:2,pb:2,pg:1,t:'Baqara 1–5-oyat'},dk());tqLog({m:'a',s:1,a:1,b:5,pa:2,pb:2,pg:1,w:'n',nm:'asr',t:'🕌 Asr · Yosin 1–5-oyat'},dk());S.km=[{id:'m1',t:'💧 Suv',ty:'num',u:'stakan',g:8,dir:'up'}];nkAdd('pom',3,1000,[]);NXF={t:'Erta turish',a:'05:30',b:'Odatdagidek',m:'xp',days:14,o:0};nxAdd();S.ib=[{id:5,t:'Kitob olish',d:dk(),x:0}];rtS();S.rt.d[dk()]={k1:{q:'Task 2 inshosi',m:20,r:3,h:10,t:'IELTS Writing'}};S.bl=bl().concat([{id:'o1',t:'Mehmon kutish',s:1140,e:1200,d:[1],on:dk()}])}""")
    q = lambda s: ev("(s)=>{SQ=s;return srRes()}", s)
    chk('the search finds the new things: takror entries (📖 and 🕌), your metrics, Nafs contracts and experiments, quick notes, ritual sentences and one-day plans', 'Takror' in q('baqara') and 'Namozda' in q('yosin') and 'Ko‘rsatkich' in q('suv') and 'Tajriba' in q('erta turish') and 'Tezkor yozuv' in q('kitob olish') and 'Marosim' in q('inshosi') and 'bir kunlik reja' in q('mehmon'))
    chk('and shows them with Uzbek dates (“9-noyabr”)', '9-noyabr' in q('baqara') or '9-noyabr' in q('kitob olish'))
    ev("(s)=>{SQ=s;srRes();srGo(0)}", 'suv'); chk('tapping a metric result opens Maqsad → Nafs', ev("tab") == 'm' and ev("MQV") == 'n'); ev("(s)=>{SQ=s;srRes();srGo(SRL.findIndex(r=>r.k==='📖 Takror'))}", 'baqara'); chk('tapping a takror result opens Qur‘on → Takror with that day selected', ev("tab") == 'q' and ev("QT") == 't' and ev("TQSEL") == '2026-11-09')
    ev("(s)=>{SQ=s}", 'dokon'); chk('the old search results (habits, books, words...) still work', 'Hech narsa' in ev("srRes()") or len(ev("srAll().filter(r=>r.t.toLowerCase().includes('dokon'))")) >= 0)
    # ---------- sozlamalar qidiruvi
    ev("()=>{SQ='';SO=false;SDQ='';SDO={};tab='s';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('Settings now has a search box and a “Yig‘ish” (collapse all) button under the title', ev("!!document.getElementById('szq')") and 'Yig‘ish' in t and ev("document.querySelectorAll('#app details.sd').length") >= 6)
    n_all = ev("document.querySelectorAll('#app details.sd').length"); ev("szQ('zaxira')"); pg.wait_for_timeout(100); titles = ev("[...document.querySelectorAll('#app details.sd > summary')].map(s=>s.textContent)")
    chk('typing “zaxira” keeps only the matching groups (the 🛡 Zaxira holati group) and opens them', 0 < len(titles) < n_all and all('axira' in x or 'Zaxira' in x for x in titles) and ev("document.querySelector('#app details.sd').open") is True, titles)
    ev("szQ('xato')"); chk('“xato” finds the error journal group', any('Xatolar' in x for x in ev("[...document.querySelectorAll('#app details.sd > summary')].map(s=>s.textContent)")))
    ev("szQ('jilo')"); chk('“jilo” finds the new 🪄 Jilo va qulaylik group', any('Jilo' in x for x in ev("[...document.querySelectorAll('#app details.sd > summary')].map(s=>s.textContent)")))
    ev("szQ('qqqzzz')"); chk('a word that matches nothing says so', 'Hech narsa topilmadi' in pg.inner_text('#app'))
    ev("szQ('')"); chk('clearing the box shows all groups again', ev("document.querySelectorAll('#app details.sd').length") == n_all)
    ev("()=>{SDO={a:1};szAll(false)}"); chk('“Yig‘ish” collapses every group', ev("Object.keys(SDO).length") == 0 and ev("document.querySelectorAll('#app details.sd[open]').length") == 0)
    # ---------- jilo guruhi
    ev("()=>{SDO={jl:1};tab='s';render()}"); pg.wait_for_timeout(80); t = pg.inner_text('#app'); chk('the 🪄 Jilo va qulaylik group offers: date style, the undo bar, how Sabqi/Manzil count, and re-showing the swipe tip — each with the previous behaviour available', all(x in t for x in ['Sana ko‘rinishi', '9-noyabr', '2026-11-09', 'Bekor qilish tugmasi', 'Yoqilgan', 'O‘chirilgan', 'Alohida sanaladi', 'avvalgidek', 'Qayta ko‘rsatish']))
    ev("jlOpt('trk_dfmt','i')"); chk('choosing the old date style is remembered', ev("uiG('trk_dfmt')") == 'i' and ev("dU('2026-11-09')") == '2026-11-09'); ev("jlOpt('trk_dfmt','u')")
    # ---------- takror hisobi qoidasi
    ev("()=>{const q=S.q;q.tk=undefined;q.rd={};q.rs={};q.m[1]=10;q.m[0]=1;rate(1,2)}"); chk('by default Sabqi/Manzil “Yaxshi” is recorded as takror but NOT added to the reading/hatm pages (separate rule for everything)', ev("tqList(dk()).filter(e=>e.src==='rate').length") == 1 and ev("S.q.rd[dk()]||0") == 0)
    ev("uiS('trk_tqrd','q')"); ev("()=>{S.q.rd={};rate(1,2)}"); chk('with “O‘qish hisobiga ham qo‘shilsin (avvalgidek)” the pages are added to reading again (10)', ev("S.q.rd[dk()]") == 10); ev("uiS('trk_tqrd','a')")
    ev("""()=>{const q=S.q;q.tk=undefined;q.rd={};q.sqd={};q.mzd={};window.ssParts=()=>[{k:'m',n:'Manzil',r:[[3,5]],p:2,done:null}];ssSet('m','g')}""")
    L = ev("tqList(dk())"); chk('the daily Manzil/Sabqi check-off (ssSet) is now recorded as takror too (pages 3–4, 2 bet, source “ssm”) and leaves reading pages untouched', len(L) == 1 and L[0]['src'] == 'ssm' and L[0]['pg'] == 2 and L[0]['pa'] == 3 and L[0]['pb'] == 4 and (ev("S.q.rd[dk()]") or 0) == 0, L)
    ev("ssUndo('m')"); chk('undoing it removes that takror entry and does not subtract from reading', ev("tqList(dk()).length") == 0 and (ev("S.q.rd[dk()]") or 0) == 0)
    ev("uiS('trk_tqrd','q')"); ev("()=>{S.q.rd={};S.q.mzd={};ssSet('m','g')}"); chk('in the old mode it also adds 2 reading pages, and undo takes them back', ev("S.q.rd[dk()]") == 2); ev("ssUndo('m')"); chk('…', (ev("S.q.rd[dk()]") or 0) == 0 and ev("tqList(dk()).length") == 0); ev("uiS('trk_tqrd','a')")
    # ---------- surish maslahati
    ev("()=>{tab='h';BV='j';VD=null;render()}"); pg.wait_for_timeout(100); chk('the swipe tip is shown once above today’s timeline', 'Surish:' in pg.inner_text('#app') and 'o‘ngga' in pg.inner_text('#app'))
    ev("()=>{[...document.querySelectorAll('#app .row .x')].find(b=>b.parentElement.textContent.includes('Surish')).click()}"); pg.wait_for_timeout(80); chk('closing it hides it for good', 'Surish:' not in pg.inner_text('#app') and ev("uiG('trk_swh')") == '1')
    ev("()=>{uiS('trk_swh','0');render()}"); pg.wait_for_timeout(60); chk('“Qayta ko‘rsatish” in Settings brings it back', 'Surish:' in pg.inner_text('#app')); ev("uiS('trk_swh','1')")
    # ---------- tizim tekshiruvi
    ev("()=>{tab='s';SDO={xj:1};SDQ='';render()}"); pg.wait_for_timeout(60); chk('the error-journal group has a “🧪 Tizim tekshiruvi” button', '🧪 Tizim tekshiruvi' in pg.inner_text('#app')); ev("tsRun()"); pg.wait_for_timeout(800); Rs = ev("TS_R")
    chk('the self-check tests this very phone: storage, big storage, offline mode, share, clipboard, notifications, home-screen app, swipe support, Hijri calendar, voices, journal, data size, clock; it reports ✅/⚠️ with hints', len(Rs) >= 12 and next(x for x in Rs if x['n'].startswith('Xotira'))['ok'] and next(x for x in Rs if 'IndexedDB' in x['n'])['ok'] and next(x for x in Rs if 'Surish' in x['n'])['ok'] and next(x for x in Rs if 'Hijriy' in x['n'])['ok'] and next(x for x in Rs if 'Soat' in x['n'])['ok'], [(x['n'], x['ok']) for x in Rs])
    pg.wait_for_timeout(60); t = pg.inner_text('#app'); chk('the result list is shown in Settings with the number of warnings', '✅ Xotira (localStorage) ishlaydi' in t and 'ta ogohlantirish' in t)
    chk('the stylesheet respects “reduce motion” and keyboard focus', ev("[...document.styleSheets].some(s=>{try{return [...s.cssRules].some(r=>String(r.conditionText||'').includes('prefers-reduced-motion'))}catch(e){return false}})"))
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='s';SDO={jl:1,xj:1};SDQ='';render();udShow('Juda uzun xabar matni bu yerda turadi, qanday ko‘rinishini tekshiramiz','{}')}", [ui, th]); pg.wait_for_timeout(70)
            ok1 = ev("document.documentElement.scrollWidth<=window.innerWidth+1"); ev("()=>{tab='h';BV='j';uiS('trk_swh','0');render()}"); pg.wait_for_timeout(60); ok2 = ev("document.documentElement.scrollWidth<=window.innerWidth+1"); ev("udHide()")
            if not (ok1 and ok2): bad.append(ui + th)
    chk('settings with the new groups, the undo bar and the swipe tip fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
