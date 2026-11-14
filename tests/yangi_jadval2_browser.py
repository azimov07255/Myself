# Bugun jadvali: keyingi reja uyqu paytida va yarim tundan keyin ham ko'rinadi. Soat: seshanba 2026-11-10 01:42.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
BL = "[{id:'uyqu1',t:'Uxlash',s:0,e:300,d:[0,1,2,3,4,5,6]},{id:'uyqu2',t:'Uygonish',s:300,e:360,d:[0,1,2,3,4,5,6]},{id:'q1',t:'Quron',s:360,e:540,d:[0,1,2,3,4,5,6],ty:'quron',fx:0},{id:'k1',t:'Kitob',s:735,e:760,d:[0,1,2,3,4,5,6],ty:'oqish',fx:0},{id:'u1',t:'Univer',s:1080,e:1170,d:[0,1,2,3,4,5,6],ty:'ish',fx:1}]"
def setup(ev):
    ev("(()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;for(const k of ['trk_jdm','trk_jdw','trk_jdn','trk_jdx','trk_hzc','trk_hzb','trk_swh','trk_jds','trk_bsec','trk_jdl'])localStorage.removeItem(k);localStorage.setItem('trk_jdx','1');localStorage.setItem('trk_swh','1');localStorage.setItem('trk_bsec','a');S.bl=" + BL + ";S.ov=undefined;S.done={};tab='h';BV='j';render()})()")
BAR = "(()=>{window.scrollTo(0,3000);hzUpdate();const b=document.getElementById('hzb');return b?b.innerText:null})()"
with Run('jd2', when=(2026, 11, 10, 1, 42, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    setup(ev); pg.wait_for_timeout(150)
    chk('at night the current block is “Uxlash” (a sleep block), yet the bottom bar still shows the next real plan: “⏭ Keyingi: Quron · 06:00 — 4 soat 18 daqiqadan keyin”', ev("nowInfo().b.id") == 'uyqu1' and (lambda t: t and 'Keyingi: Quron' in t and '06:00' in t and '4 soat 18' in t and 'dan keyin' in t)(ev(BAR)), ev(BAR))
    chk('the wake-up block (Uyg‘onish 05:00) is skipped: the bar names the first real plan, not the sleep ones', 'Uygonish' not in (ev(BAR) or ''))
    ev("window.scrollTo(0,0)"); ev("hzUpdate()"); chk('with the Hozir card still in view the bar stays hidden (as before)', ev("!document.getElementById('hzb')"))
    ev("uiS('trk_hzc','1')"); chk('folded into a pill it shows just “⏭ 06:00” and opens again on tap', (ev(BAR) or '').startswith('⏭ 06:00') and ev("document.getElementById('hzb').hasAttribute('data-c')")); ev("document.querySelector('#hzb .hzm').click()"); chk('…', ev("localStorage.getItem('trk_hzc')") == '0' and ev("!!document.querySelector('#hzb .hzt')"))
    # chiziq
    ev("window.scrollTo(0,0)"); ev("render()"); pg.wait_for_timeout(80); t = ev("document.querySelector('#app .n3').innerText")
    chk('the “Keyingi 3 soat” strip no longer just says “Reja yo‘q”: it adds the next plan after the window (“Keyingisi: Quron — 06:00 · 4 soat 18 daqiqadan keyin”)', 'Reja yo‘q: bo‘sh vaqt' in t and 'Keyingisi: Quron' in t and '06:00' in t and '4 soat 18' in t, t)
    ev("uiS('trk_jdx','0')"); ev("render()"); t = ev("document.querySelector('#app .n3').innerText"); chk('with that setting off it is exactly as before (only “Reja yo‘q: bo‘sh vaqt”)', 'Reja yo‘q: bo‘sh vaqt' in t and 'Keyingisi' not in t); ev("uiS('trk_jdx','1')")
    ev("uiS('trk_jdn','0')"); chk('“Bo‘sh vaqtda va uyqu paytida…” off → no bar at night (the old behaviour)', ev(BAR) is None); ev("uiS('trk_jdn','1')")
    ev("uiS('trk_jdm','o')"); ev("render()"); t = ev("document.querySelector('#app .n3').innerText"); chk('the old schedule mode keeps both exactly as they were (no bar at night, strip without the extra plan)', ev(BAR) is None and 'Keyingisi' not in t); ev("uiS('trk_jdm','n')")
    # ertaga
    pg.clock.set_system_time('2026-11-10T23:50:00'); setup(ev); pg.wait_for_timeout(100); b = ev(BAR)
    chk('late in the evening with nothing left today the bar points to tomorrow: “⏭ Ertaga: Quron · 06:00 — 6 soat 10 daqiqadan keyin”', b and 'Ertaga: Quron' in b and '06:00' in b and '6 soat 10' in b, b)
    ev("window.scrollTo(0,0)"); ev("render()"); t = ev("document.querySelector('#app .n3').innerText"); chk('…and so does the strip (“Ertaga: Quron”)', 'Ertaga: Quron' in t, t)
    # hozirgi blok bor
    pg.clock.set_system_time('2026-11-10T06:30:00'); setup(ev); pg.wait_for_timeout(100); b = ev(BAR); chk('while a real block is running the bar is as before: its name, time left and the next plan (Quron · 2 soat 30 daqiqa qoldi; Keyingi: Kitob, 12:15)', b and 'Quron' in b and '2 soat 30' in b and 'Keyingi: Kitob, 12:15' in b, b)
    pg.clock.set_system_time('2026-11-10T01:42:00'); setup(ev); ev("()=>{SDO={jl:1};tab='s';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('Settings → Jilo explains both switches', 'Bo‘sh vaqtda va uyqu paytida pastdagi chiziq' in t and 'Keyingi 3 soat” chizig‘ida reja bo‘lmasa' in t)
