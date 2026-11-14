# Namoz-markazli kun: bloklarni namoz vaqtiga bog'lash. Soat: chorshanba 2026-11-11 10:00.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
BL = "[{id:'uyqu1',t:'Uxlash',s:1380,e:1740,d:[0,1,2,3,4,5,6],ty:'uyqu'},{id:'b1',t:'Peshin namozi va tushlik',s:760,e:870,d:[0,1,2,3,4,5,6],ty:'ibodat',fx:1},{id:'b2',t:'Asr namozi',s:900,e:920,d:[0,1,2,3,4,5,6],ty:'ibodat',fx:1},{id:'b3',t:'Kitob',s:540,e:600,d:[0,1,2,3,4,5,6],ty:'oqish',fx:0}]"
with Run('nmk', when=(2026, 11, 11, 10, 0, 0), bg='n') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("(()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;window.__PT={Fajr:345,Sunrise:430,Dhuhr:735,Asr:900,Maghrib:1070,Isha:1140};window.ptTimes=()=>window.__PT;for(const k of ['trk_nmk','trk_swh','trk_bg'])localStorage.removeItem(k);localStorage.setItem('trk_swh','1');S.bl=" + BL + ";S.ov=undefined;NMKSIG='';tab='h';BV='j';render()})()")
    pg.wait_for_timeout(100)
    ev("nmkOpen()"); pg.wait_for_timeout(80); t = pg.inner_text('#nmkv'); chk('the screen shows today’s prayer times, the plan blocks (not the sleep one) with “qat‘iy vaqt”, and the buttons “🕌 5 vaqt namoz bloklari” and “🪄 Nomiga qarab bog‘lash”', all(x in t for x in ['Namoz-markazli kun', 'Bomdod 05:45', 'Peshin 12:15', 'Xufton 19:00', 'Peshin namozi va tushlik', 'Asr namozi', 'Kitob', 'qat‘iy vaqt', '5 vaqt namoz bloklari', 'Nomiga qarab bog‘lash']) and 'Uxlash' not in t.split('Reja bloklari')[1])
    ev("nmkEdit('b1')"); pg.wait_for_timeout(60); t = pg.inner_text('#nmkv'); chk('tapping “Bog‘lash” opens the editor: six prayers, offsets (−30 … +60) and durations (10 … 90)', all(x in t for x in ['Bomdod', 'Quyosh', 'Peshin', 'Asr', 'Shom', 'Xufton', '-30', '+15', '+60', '10', '90']))
    ev("nmkAttach('b1','Dhuhr',15,60)"); b = ev("S.bl.find(b=>b.id==='b1')"); chk('attaching “Peshin (12:15) + 15 daqiqa, 60 daqiqa” moves the block to 12:30–13:30 and keeps the link', b['s'] == 750 and b['e'] == 810 and b['an'] == {'p': 'Dhuhr', 'o': 15, 'dur': 60}, b)
    chk('the rest of the app sees the new time (the day plan used by Hozir and reminders)', ev("rjDay(dk()).find(b=>b.id==='b1').s") == 750 and ev("rjDay(dk()).find(b=>b.id==='b1').e") == 810)
    ev("window.__PT.Dhuhr=740"); ev("render()"); chk('when the prayer time changes (12:20) the block follows by itself: 12:35–13:35', ev("S.bl.find(b=>b.id==='b1').s") == 755 and ev("S.bl.find(b=>b.id==='b1').e") == 815)
    pg.clock.set_system_time('2026-11-12T10:00:00'); ev("window.__PT.Dhuhr=738"); ev("render()"); chk('the next day, with that day’s prayer time (12:18), it is shifted again to 12:33', ev("S.bl.find(b=>b.id==='b1').s") == 753)
    chk('a second synchronisation changes nothing (no loop, nothing re-saved)', ev("nmkSync()") == 0)
    pg.clock.set_system_time('2026-11-11T10:00:00'); ev("window.__PT.Dhuhr=735"); ev("render()")
    ev("nmkDetach('b1')"); b = ev("S.bl.find(b=>b.id==='b1')"); chk('“Qat‘iy vaqt” removes the link and the block keeps its last time', 'an' not in b and b['s'] in (750, 753, 755)); ev("window.__PT.Dhuhr=700"); ev("render()"); chk('after detaching, prayer changes no longer move it', ev("S.bl.find(b=>b.id==='b1').s") == b['s']); ev("window.__PT.Dhuhr=735"); ev("render()")
    ev("nmkAuto()"); b1 = ev("S.bl.find(b=>b.id==='b1')"); b2 = ev("S.bl.find(b=>b.id==='b2')"); b3 = ev("S.bl.find(b=>b.id==='b3')")
    chk('“Nomiga qarab bog‘lash” links the blocks that name a prayer (Peshin → Dhuhr, Asr → Asr) with offset 0 and the block’s current length (60 minutes after the earlier edit), and leaves “Kitob” alone', b1['an']['p'] == 'Dhuhr' and b1['an']['o'] == 0 and b1['an']['dur'] == 60 and b1['s'] == 735 and b1['e'] == 795 and b2['an']['p'] == 'Asr' and b2['s'] == 900 and b2['e'] == 920 and 'an' not in b3 and b3['s'] == 540, (b1, b2))
    n0 = len(ev("S.bl")); ev("nmkAdd5()"); L = ev("S.bl.filter(b=>b.an)"); chk('“5 vaqt namoz bloklari” adds the missing prayer blocks (Bomdod, Shom, Xufton; Peshin and Asr already exist at +0): each 20 minutes, linked, fixed', len(ev("S.bl")) - n0 == 3 and sorted(b['an']['p'] for b in L) == ['Asr', 'Dhuhr', 'Fajr', 'Isha', 'Maghrib'] and all(b['fx'] == 1 for b in L if b['id'].startswith('nmk')), [(b['t'], b['s']) for b in L])
    f = ev("S.bl.find(b=>b.an&&b.an.p==='Fajr')"); chk('the Bomdod block sits exactly at the Bomdod time (05:45–06:05)', f['s'] == 345 and f['e'] == 365); n1 = len(ev("S.bl")); ev("nmkAdd5()"); chk('pressing it again adds nothing', len(ev("S.bl")) == n1 and any('allaqachon' in m for m in ev("__t")))
    ev("window.__PT.Isha=1430"); ev("render()"); i = ev("S.bl.find(b=>b.an&&b.an.p==='Isha')"); chk('a block that would run past midnight is kept inside the day (clamped to 24:00)', i['e'] == 1440 and i['s'] == 1420, i); ev("window.__PT.Isha=1140"); ev("render()")
    ev("uiS('trk_nmk','0')"); ev("window.__PT.Asr=950"); ev("render()"); chk('switched off in Settings: bound blocks stay where they are (no shifting)', ev("S.bl.find(b=>b.id==='b2').s") == 900 and ev("nmkSync()") == 0); ev("uiS('trk_nmk','1')"); ev("render()"); chk('switched on again, they catch up', ev("S.bl.find(b=>b.id==='b2').s") == 950); ev("window.__PT.Asr=900"); ev("render()")
    ev("window.ptTimes=()=>null"); s0 = ev("S.bl.find(b=>b.id==='b2').s"); ev("render()"); chk('if prayer times are not set nothing moves and the screen says so', ev("nmkSync()") == 0 and ev("S.bl.find(b=>b.id==='b2').s") == s0 and '⚠️ Namoz vaqtlari sozlanmagan' in ev("(()=>{nmkDraw();return document.getElementById('nmkv').innerText})()")); ev("window.ptTimes=()=>window.__PT")
    ev("nmkClose()"); ev("()=>{SDO={jl:1};tab='s';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('Settings → Jilo has the switch (“Yoqilgan / O‘chirilgan (qat‘iy vaqt)”) and the “Bloklarni namozga bog‘lash” button', all(x in t for x in ['Namoz-markazli kun', 'Yoqilgan (bog‘langan bloklar siljiydi)', 'qat‘iy vaqt', 'Bloklarni namozga bog‘lash']))
    bad = []
    ev("()=>{tab='h';BV='j';render()}")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='h';BV='j';render()}", [ui, th]); pg.wait_for_timeout(60)
            ev("nmkOpen()"); ev("nmkEdit('b3')"); pg.wait_for_timeout(200); ok = ev("(()=>{const a=document.querySelector('#nmkv .asc');return a.scrollWidth<=a.clientWidth+1})()"); ev("nmkClose()")
            if not ok: bad.append(ui + th)
    chk('the screen (with the editor open) fits the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
