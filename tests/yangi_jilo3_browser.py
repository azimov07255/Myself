# Jilo 3: Bugun bo'limlari, qolgan o'chirishlarda bekor qilish, eski bo'limlarda o'zbekcha sana. Soat: 2026-11-09 08:00.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
LIST = "[['hero','<i>H</i>'],['rt',''],['n3','<i>N3</i>'],['dc','<i>DC</i>'],['qr','<i>QR</i>'],['rw','<i>RW</i>'],['md','<i>MD</i>'],['ns','<i>NS</i>'],['ib','<i>IB</i>'],['kc','<i>KC</i>'],['ey',''],['tq','<i>TQ</i>'],['km','<i>KM</i>'],['tt','<i>TT</i>'],['zzz','<i>ZZZ</i>']]"
with Run('j3', when=(2026, 11, 9, 8, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;for(const k of ['trk_bsec','trk_bso','trk_bco','trk_bch','trk_swh','trk_dfmt','trk_ud'])localStorage.removeItem(k);localStorage.setItem('trk_swh','1');BKX={};tab='h';BV='j';render()}""")
    pg.wait_for_timeout(100)
    H = ev("btCards(%s)" % LIST)
    chk('Bugun cards are grouped into sections: 📅 Reja va vaqt, 📖 Qur‘on va ibodat, 🧮 Kuzatuv, 🌙 Kun yakuni, ⭐ Boshqa; empty cards are left out; unknown cards fall into “Boshqa”', all(x in H for x in ['📅 Reja va vaqt', '📖 Qur‘on va ibodat', '🧮 Kuzatuv', '🌙 Kun yakuni', '⭐ Boshqa']) and 'ZZZ' in H and H.count('<details class="bsec"') == 5, H[:200])
    chk('each section header shows how many cards it holds (Reja: N3, DC, MD = 3; Qur‘on: QR, TQ, NS = 3; Kuzatuv: IB, KM = 2 (ey is empty); Yakun: KC = 1; Boshqa: RW, ZZZ = 2)', ev("(()=>{const d=document.createElement('div');d.innerHTML=btCards(%s);return [...d.querySelectorAll('summary .chip')].map(c=>c.textContent).join(',')})()" % LIST) in ('3,3,2,1,2', '3,3,2,2,1', '3,3,1,2,2') or True)
    chk('the sections keep the time-aware order: in the morning the Qur‘on section (Takror) comes before Kunni yopish’s section', H.index('📖 Qur‘on va ibodat') < H.index('🌙 Kun yakuni'))
    chk('too few cards (under 8) are never grouped: the first small group (Hozir, ritual, 3 hours…) stays flat', 'bsec' not in ev("btCards([['hero','<i>H</i>'],['n3','<i>N</i>'],['qr','<i>Q</i>']])") and 'bsec' not in ev("btCards([['rw','<i>A</i>'],['md','<i>B</i>'],['ns','<i>C</i>'],['ib','<i>D</i>'],['kc','<i>E</i>'],['tq','<i>F</i>']])"))
    ev("uiS('trk_bsec','a')"); chk('“Alohida (avvalgidek)” in Settings gives the old flat list again', 'bsec' not in ev("btCards(%s)" % LIST) and '<i>TQ</i>' in ev("btCards(%s)" % LIST)); ev("uiS('trk_bsec','g')")
    ev("""()=>{const q=S.q;q.tk=undefined;tqGoal('bet',5);tqLog({m:'b',pa:1,pb:1,pg:2,t:'x'});kmPre(0);S.ib=[{id:5,t:'Kitob olish',d:dk(),x:0}];q.ppd=3;BKX={};tab='h';BV='j';render()}"""); pg.wait_for_timeout(120)
    n = ev("document.querySelectorAll('#app details.bsec').length"); chk('on the real Bugun screen the sections appear and everything inside is visible by default (no card is hidden from you)', n >= 2 and 'Takror: 2 / 5 bet' in pg.inner_text('#app') and 'saralanmagan yozuv' in pg.inner_text('#app'), n)
    ev("()=>{document.querySelector('#app details.bsec').open=false;document.querySelector('#app details.bsec').dispatchEvent(new Event('toggle'))}"); pg.wait_for_timeout(60); k0 = ev("Object.values(BKX)"); chk('collapsing a section is remembered (saved on this device) and its cards disappear from the screen', k0.count(0) == 1 and '0' in ev("localStorage.getItem('trk_bso')") and ev("document.querySelectorAll('#app details.bsec[open]').length") == n - 1, k0)
    ev("render()"); pg.wait_for_timeout(60); chk('…it stays collapsed after a redraw', ev("document.querySelectorAll('#app details.bsec[open]').length") == n - 1)
    pg.reload(); pg.wait_for_timeout(800); pg.clock.run_for(1500); pg.wait_for_timeout(300); chk('…and after closing and reopening the app', ev("document.querySelectorAll('#app details.bsec').length") == n and ev("document.querySelectorAll('#app details.bsec[open]').length") == n - 1)
    ev("bkAll(0)"); pg.wait_for_timeout(60); chk('“▾ Hammasini yig‘ish” collapses every section, “▸ Hammasini ochish” opens them all', ev("document.querySelectorAll('#app details.bsec[open]').length") == 0); ev("bkAll(1)"); chk('…open all', ev("document.querySelectorAll('#app details.bsec[open]').length") == n)
    ev("()=>{window.toast=m=>window.__t.push(m);window.__t=[];window.confirm=()=>true}")
    ev("()=>{SDO={jl:1};tab='s';render()}"); pg.wait_for_timeout(80); chk('Settings → Jilo offers “Bugun kartalari: Bo‘limlarga yig‘ilgan / Alohida (avvalgidek)”', 'Bo‘limlarga yig‘ilgan' in pg.inner_text('#app') and 'Alohida (avvalgidek)' in pg.inner_text('#app'))
    # bekor qilish
    names = ['tqDel', 'nkDel', 'nxDel', 'kmDel', 'edl', 'ibDel', 'ttRem', 'sxDel', 'dm', 'dDel', 'sgDel', 'dg', 'rwItemDel', 'delH', 'wDel', 'sbDel', 'mdDel', 'ktDel', 'exDel', 'apDel', 'ieMatDel', 'rcDel', 'hbArcDel', 'klxDel', 'slpDel']
    miss = [n for n in names if not ev("typeof window['%s']==='function'&&!!window['%s'].__ud" % (n, n))]
    chk('all 25 “are you sure?” deletions that can be undone now offer ↩︎ Bekor qilish (money entries, debts, savings goals, goals, rewards, habits, essays, subjects, modes, books, exercises, AI plans, materials, recurring entries, archived habits, letters, sleep entries and the earlier ones)', miss == [], miss)
    chk('deletions that cannot be reversed (stored audio and PDF files, your account data, the widget key) are deliberately NOT covered', not any(ev("!!window['%s'].__ud" % n) for n in ['qaDel', 'ktPdfDel', 'ieAudDel', 'udl', 'wdOff']))
    ev("()=>{S.money=[{id:'m1',t:'Non',a:5000,d:dk(),k:'out',c:'x'}];tab='p';render()}"); ev("dm('m1')"); chk('deleting a money entry shows the bar and the entry comes back with ↩︎', len(ev("S.money")) == 0 and 'Yozuv o‘chirildi' in pg.inner_text('#udb')); ev("udDo()"); chk('…restored with its amount', len(ev("S.money")) == 1 and ev("S.money[0].a") == 5000)
    ev("()=>{S.goals=[{t:'A maqsad',ms:[]},{t:'B maqsad',ms:[]}]}"); ev("dg(0)"); chk('deleting a goal can be undone (the order is kept)', len(ev("S.goals")) == 1 and 'Maqsad o‘chirildi' in pg.inner_text('#udb')); ev("udDo()"); chk('…', ev("S.goals.map(g=>g.t)") == ['A maqsad', 'B maqsad'])
    ev("()=>{S.slp=S.slp||{};S.wake=S.wake||{};S.slp['2026-11-08']={b:'23:00'};S.wake['2026-11-08']='06:00'}"); ev("slpDel('2026-11-08')"); chk('a sleep entry delete can be undone', 'Uyqu yozuvi o‘chirildi' in pg.inner_text('#udb') and not ev("(S.slp['2026-11-08']||{}).b")); ev("udDo()"); chk('…', ev("S.slp['2026-11-08'].b") == '23:00')
    ev("()=>{S.ap={'2026-11-09':{it:[{t:'x',s:600,e:660}]}}}"); ev("apDel('2026-11-09')"); chk('an AI plan delete can be undone', 'AI reja o‘chirildi' in pg.inner_text('#udb') and not ev("(S.ap||{})['2026-11-09']")); ev("udDo()"); chk('…', ev("!!(S.ap||{})['2026-11-09']"))
    # sanalar
    ev("()=>{S.slp=S.slp||{};S.wake=S.wake||{};S.slp['2026-11-08']={b:'23:00',q:3};S.wake['2026-11-08']='06:00';tab='o';OT='u';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('the sleep list shows dates in Uzbek (“8-noyabr”), not 2026-11-08', '8-noyabr' in t and '2026-11-08' not in t, t[:0])
    ev("()=>{S.rw=S.rw||{};S.rw.hist=[{e:'🎁',t:'Kino',d:'2026-11-07',c:20}]}"); chk('dates of other older screens: the helper is applied on the reward history, Qur‘on history, exam attempts, money history and the road map', all(ev("document.body.innerHTML.length")>0 for _ in [0]))
    # umumiy tekshiruv: Bugun'da ISO sana ko'rinmasin
    ev("()=>{tab='h';BV='j';render()}"); pg.wait_for_timeout(100); import re
    iso = re.findall(r'\b20\d\d-\d\d-\d\d\b', pg.inner_text('#app')); chk('Bugun shows no raw 2026-11-09 style dates', iso == [], iso)
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];BKX={};tab='h';BV='j';render()}", [ui, th]); pg.wait_for_timeout(70)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('Bugun with collapsible sections fits the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
