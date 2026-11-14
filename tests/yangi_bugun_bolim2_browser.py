import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Bugun: 📅 Jadval + 🧩 Kun, Intizom kartasi, o'tgan rejalar joyi. Soat: chorshanba 2026-11-11 13:01.
import sys, re
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
BL = "[{id:'uyqu1',t:'Uxlash',s:1440,e:1740,d:[0,1,2,3,4,5,6]},{id:'u2',t:'Uygonish',s:300,e:360,d:[0,1,2,3,4,5,6],ty:'uyqu',fx:1},{id:'q1',t:'Quron',s:360,e:540,d:[0,1,2,3,4,5,6],ty:'quron',fx:0},{id:'k1',t:'Kitob oqish',s:735,e:760,d:[0,1,2,3,4,5,6],ty:'oqish',fx:0},{id:'p1',t:'Peshin namozi',s:760,e:870,d:[0,1,2,3,4,5,6],ty:'ibodat',fx:1},{id:'t1',t:'Univer tasks',s:870,e:960,d:[0,1,2,3,4,5,6],ty:'oqish',fx:1},{id:'f1',t:'Univer',s:1080,e:1170,d:[0,1,2,3,4,5,6],ty:'ish',fx:1},{id:'d1',t:'Quron yodlash',s:1200,e:1260,d:[0,1,2,3,4,5,6],ty:'quron',fx:0}]"
def setup(ev, extra=""):
    ev("(()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;for(const k of ['trk_bg','trk_jdp','trk_bgi','trk_bgq','trk_bgd','trk_bgt','trk_bgo','trk_jdm','trk_jdw','trk_jds','trk_jdo','trk_swh','trk_bsec','trk_hzb','trk_bfold','trk_btop','trk_bsimple'])localStorage.removeItem(k);localStorage.setItem('trk_swh','1');localStorage.setItem('trk_jdw','e');S.bl=" + BL + ";S.ov=undefined;S.done={};S.ml=undefined;BGO={};BGL=[];ALLV=false;BV='j';tab='h';render()})()")
with Run('bg', when=(2026, 11, 11, 13, 1, 0), bg='n') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    setup(ev); pg.wait_for_timeout(150)
    t = pg.inner_text('#app'); tabs = ev("[...document.querySelectorAll('#app .btabs button')].map(b=>b.textContent.trim())")
    chk('Bugun opens on 📅 Jadval and there is a new tab “🧩 Kun” next to Jadval, Kunlik, Holat, Tahlil', ev("BV") == 'j' and any('Kun' in x and '🧩' in x for x in tabs) and any('Jadval' in x for x in tabs) and any('Tahlil' in x for x in tabs), tabs)
    chk('the Jadval tab is clean: the Hozir card, the “Keyingi 3 soat” strip, the schedule rows — and NONE of the other cards (no Mulk, Himoya, Rejim, Kun tartibi, Qur‘on rejasi)', ev("!!document.querySelector('#app section.hero')") and 'Keyingi' in t and ev("document.querySelectorAll('#app .tl').length") >= 6 and all(x not in t for x in ['Mulk surasi', '🛡 Himoya', '🧭 Rejim', 'Kun tartibi', 'Bugungi Qur‘on rejasi']), t[:200])
    chk('under the Hozir card there is a quick row: “🆘 Qiyin”, “🔒 Sessiya”, “🧩 Kun”', all(x in t for x in ['🆘 Qiyin', '🔒 Sessiya', '🧩 Kun']))
    ev("uiS('trk_bgq','0')"); ev("render()"); chk('the quick row can be switched off in Settings', '🆘 Qiyin' not in pg.inner_text('#app')); ev("uiS('trk_bgq','1')"); ev("render()")
    ev("[...document.querySelectorAll('#app .bgq button')].find(b=>b.textContent.includes('Kun')).click()"); pg.wait_for_timeout(120); t = pg.inner_text('#app'); chk('the quick “🧩 Kun” button opens the Kun tab', ev("BV") == 'k')
    sm = ev("[...document.querySelectorAll('#app details.bgs > summary')].map(s=>s.textContent.replace(/\\s+/g,' ').trim())")
    chk('the Kun tab holds the other cards in themed groups: 🕌 Ibodat va nafs, 🎯 Intizom va fokus (and the others that have cards), each with a count', any('🕌 Ibodat va nafs' in x for x in sm) and any('🎯 Intizom va fokus' in x for x in sm), sm)
    chk('Mulk, the Qur‘on plan and the Nafs help are in the worship group; the discipline group has the combined “🧭 Intizom” card', all(x in t for x in ['Mulk surasi']) and 'Intizom' in t and ev("document.querySelectorAll('#app section.bgint').length") == 1)
    chk('the Hozir card and the next-3-hours strip are NOT repeated in the Kun tab (they live on Jadval)', ev("!document.querySelector('#app section.hero')") and 'Keyingi 3 soat' not in t and ev("document.querySelectorAll('#app .tl').length") == 0)
    ni = ev("document.querySelector('#app section.bgint').innerText"); chk('the combined Intizom card contains the three parts in one block: Rejim (with the index), Himoya / 🆘 and the Kun tartibi section', all(x in ni for x in ['Intizom', 'Rejim', 'Himoya', 'Kun tartibi']) or all(x in ni for x in ['Rejim', '🆘', 'Til']), ni[:300])
    ev("uiS('trk_bgi','a')"); ev("render()"); chk('“Alohida kartalar (avvalgidek)” gives the three separate cards again (Rejim, Himoya, Kun tartibi) and no combined card', ev("document.querySelectorAll('#app section.bgint').length") == 0 and ev("!!document.querySelector('#app .znc')") and ev("!!document.querySelector('#app .sosc')") and ev("!!document.querySelector('#app .zjc')")); ev("uiS('trk_bgi','b')")
    ev("()=>{const d=[...document.querySelectorAll('#app details.bgs')][0];d.open=false;d.dispatchEvent(new Event('toggle'))}"); ev("render()"); chk('folding a group is remembered after a redraw', ev("document.querySelectorAll('#app details.bgs')[0].open") is False)
    # eski
    ev("uiS('trk_bg','o')"); ev("()=>{BV='j';render()}"); pg.wait_for_timeout(120); t = pg.inner_text('#app'); tabs = ev("[...document.querySelectorAll('#app .btabs button')].map(b=>b.textContent.trim())")
    chk('“Hammasi bir ekranda (avvalgidek)”: no Kun tab, and the cards are on the Jadval screen again exactly as before', not any('🧩' in x for x in tabs) and 'Mulk surasi' in t and ev("!!document.querySelector('#app section.hero')") and ev("document.querySelectorAll('#app .tl').length") >= 6)
    ev("()=>{BV='k';render()}"); chk('even if the app was left on the Kun tab, switching back to the old layout lands on Jadval', ev("BV") == 'j'); ev("uiS('trk_bg','n')"); ev("()=>{BV='j';render()}")
    # o'tgan rejalar
    ev("uiS('trk_jdp','g')"); ev("render()"); pg.wait_for_timeout(80); t = pg.inner_text('#app'); g = ev("[...document.querySelectorAll('#app .tl')].map(e=>[e.dataset.bid,e.closest('details.jdg')?e.closest('details.jdg').querySelector('summary').textContent.trim().slice(0,5):'A'])"); gd = dict(g)
    chk('default: passed plans are in the folded “✅ O‘tgan” group at the bottom (Uygonish, Quron, Kitob oqish), the running block is on top', gd['u2'].startswith('✅') and gd['q1'].startswith('✅') and gd['k1'].startswith('✅') and gd['p1'] == 'A' and re.search(r'✅ O‘tgan · \d ta o‘tkazildi', t), gd)
    ev("jdPast()"); pg.wait_for_timeout(80); t = pg.inner_text('#app'); g = ev("[...document.querySelectorAll('#app .tl')].map(e=>e.dataset.bid)")
    chk('“Joyida, vaqt tartibida” (the one-tap chip): all plans in time order — Uygonish 05:00, Quron 06:00, Kitob 12:15 (missed, red), Peshin 12:40 …; no O‘tgan group; the title says “Kun rejalari (vaqt tartibida)”', g[:5] == ['u2', 'q1', 'k1', 'p1', 't1'] and ev("document.querySelectorAll('#app details.jdg').length") == 0 or ('O‘tgan' not in t and g[:4] == ['u2', 'q1', 'k1', 'p1']), g)
    chk('…and the missed one is still marked “O‘tkazib yuborilgan”, the running one still stands out', 'Kun rejalari (vaqt tartibida)' in t and 'O‘tkazib yuborilgan' in t and ev("!!document.querySelector('#app .tl.now')"))
    pg.clock.set_system_time('2026-11-11T11:30:00'); ev("render()"); pg.wait_for_timeout(80); chk('with nothing running (11:30) a “now” line is drawn between the passed and the upcoming plans', ev("!!document.querySelector('#app .nowl')") and ev("[...document.querySelectorAll('#app .tl, #app .nowl')].map(e=>e.classList.contains('nowl')?'N':'T').join('').indexOf('N')") > 0)
    pg.clock.set_system_time('2026-11-11T13:01:00'); ev("jdPast()"); chk('the chip switches back to the grouped view', ev("uiG('trk_jdp')") == 'g'); ev("uiS('trk_jdp','g')")
    # ochilish
    ev("uiS('trk_bgd','k')"); pg.reload(); pg.wait_for_timeout(800); pg.clock.run_for(1500); pg.wait_for_timeout(250); chk('“Bugun ochilganda: 🧩 Kun” opens the app on the Kun tab', ev("BV") == 'k')
    ev("uiS('trk_bgd','l')"); ev("()=>{BV='m';render()}"); pg.reload(); pg.wait_for_timeout(800); pg.clock.run_for(1500); pg.wait_for_timeout(250); chk('“Oxirgi ochilgan” returns to the tab you left (Kunlik)', ev("BV") == 'm'); ev("uiS('trk_bgd','j')"); ev("()=>{BV='j';render()}")
    ev("()=>{window.toast=m=>window.__t.push(m)}")
    ev("()=>{SDO={jl:1};tab='s';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('Settings → Jilo has the new choices: Bugun tuzilishi, O‘tgan rejalar, Intizom kartasi, tezkor tugmalar, qaysi bo‘lim ochilsin', all(x in t for x in ['Bugun tuzilishi', 'Alohida bo‘limlar', 'Hammasi bir ekranda (avvalgidek)', 'O‘tgan rejalar', 'Joyida, vaqt tartibida (avvalgidek)', 'Intizom kartasi', 'Bitta birlashgan karta', 'Hozir ostidagi tezkor tugmalar', 'Bugun ochilganda qaysi bo‘lim']))
    bad = []
    ev("()=>{tab='h';BV='j';render()}")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='h';BV='j';render()}", [ui, th]); pg.wait_for_timeout(70); ok = ev("document.documentElement.scrollWidth<=window.innerWidth+1")
            ev("()=>{BV='k';render()}"); pg.wait_for_timeout(60); ok = ok and ev("document.documentElement.scrollWidth<=window.innerWidth+1"); ev("()=>{BV='j';render()}")
            if not ok: bad.append(ui + th)
    chk('the Jadval and Kun screens fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
