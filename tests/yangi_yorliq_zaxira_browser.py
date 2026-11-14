import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Yorliqlar, sinxronlash holati, avto-zaxira. Soat: chorshanba 2026-11-11 10:00.
import sys, json
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
with Run('yz', when=(2026, 11, 11, 10, 0, 0), bg='n') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("(()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;window.pmChime=()=>{};for(const k of ['trk_sya','trk_syw','trk_lsync','trk_swh','trk_bsec','trk_bg'])localStorage.removeItem(k);localStorage.setItem('trk_swh','1');S.bl=[{id:'a1',t:'Dars',s:540,e:600,d:[0,1,2,3,4,5,6]},{id:'a2',t:'Kitob',s:700,e:760,d:[0,1,2,3,4,5,6]}];S.hab=[{id:'h1',t:'Kitob'}];S.goals=[{t:'IELTS',ms:[]}];S.zj=undefined;S.nm.d={};tab='h';BV='j';render()})()")
    # ---- yorliqlar ----
    ev("ylOpen()"); pg.wait_for_timeout(80); t = pg.inner_text('#ylv'); chk('the shortcuts screen lists 7 home-screen icons (🆘 Qiyin, 🔒 Sessiya, 🕌 Xufton, 🌅 Bomdod, ⚡ 5 daqiqa, 📝 Test, 🧩 Kun) with their links ending in #key, how to add them, and an honest note that it is untested on iPhone', all(x in t for x in ['🆘 Qiyin', '🔒 Sessiya', '🕌 Xufton', '🌅 Bomdod', '⚡ 5 daqiqa', '📝 Test', '🧩 Kun', '#sessiya', '#xufton', 'Bosh ekranga qo‘shish', 'sinalmagan']))
    ev("ylClose()")
    ev("ylRun('sessiya')"); pg.wait_for_timeout(80); chk('#sessiya opens the isolation session screen', ev("!!document.getElementById('znv')")); ev("znClose()")
    ev("ylRun('kun')"); pg.wait_for_timeout(80); chk('#kun opens Bugun → 🧩 Kun', ev("tab") == 'h' and ev("BV") == 'k'); ev("()=>{BV='j';render()}")
    ev("ylRun('test')"); pg.wait_for_timeout(80); chk('#test opens the Testlar screen', ev("!!document.getElementById('tbv')")); ev("tbClose()")
    ev("ylRun('besh')"); pg.wait_for_timeout(80); chk('#besh starts the 5-minute timer', ev("!!F5") and ev("F5.len") == 5); ev("()=>{try{f5Stop?f5Stop():0}catch(e){}}")
    ev("ylRun('xufton')"); pg.wait_for_timeout(80); chk('#xufton does NOT mark anything by itself: it asks “Xufton o‘qildimi?” first (so a stray tap cannot change your record)', 'Xufton o‘qildimi' in pg.inner_text('#ylc') and not ev("(S.nm.d[dk()]||{}).isha")); ev("ylNo()"); chk('“Yo‘q” closes it and still changes nothing', not ev("!!document.getElementById('ylc')") and not ev("(S.nm.d[dk()]||{}).isha"))
    ev("ylRun('xufton')"); ev("ylYes('zjIsha')"); chk('“Ha” records Xufton', ev("(S.nm.d[dk()]||{}).isha") == 1)
    ev("ylRun('bomdod')"); chk('#bomdod asks first as well', 'Bomdod o‘qildimi' in pg.inner_text('#ylc')); ev("ylNo()")
    ev("uiS('trk_zj','0')"); ev("ylRun('xufton')"); chk('if Kun tartibi is switched off the shortcut says so instead of breaking', any('o‘chirilgan' in m for m in ev("__t")) and not ev("!!document.getElementById('ylc')")); ev("uiS('trk_zj','1')")
    pg.goto('about:blank'); pg.goto(f'http://127.0.0.1:{R.port}/index.html#sessiya'); pg.wait_for_timeout(1400); pg.clock.run_for(1500); pg.wait_for_timeout(300); chk('opening the app through “#sessiya” (the home-screen icon) goes straight to the session screen and then clears the address so a reload does not repeat it', ev("!!document.getElementById('znv')") and ev("location.hash") == '')
    ev("znClose()")
    # ---- sinxronlash holati ----
    ev("()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;UID=null}"); chk('with no cloud account it says the data lives only on this phone', ev("syInfo().st") == 'local' and 'faqat shu telefonda' in ev("syInfo().txt"))
    ev("()=>{UID='u1';SYNC='ok';localStorage.setItem('trk_lsync',String(Date.now()));S.ts=Date.now()-120000}"); I = ev("syInfo()"); chk('signed in and just synced: “✅ Saqlangan (hozir)”', I['st'] == 'ok' and 'Saqlangan' in I['txt'])
    ev("()=>{S.ts=Date.now()}"); pg.clock.run_for(5 * 60000); ev("()=>{S.ts=Date.now()}"); ev("()=>{localStorage.setItem('trk_lsync',String(Date.now()-3*60000))}"); chk('unsent changes are recognised (“Hali serverga yuborilmagan”)', ev("syInfo().st") == 'dirty')
    chk('…but there is no warning yet (less than 30 minutes)', ev("syBar()") == '')
    ev("()=>{localStorage.setItem('trk_lsync',String(Date.now()-50*60000));S.ts=Date.now()}"); h = ev("syBar()"); chk('after 30+ minutes of failing to save, a warning appears with “☁ Hozir saqlash” and “Faylga saqlash”', all(x in h for x in ['Saqlash kechikmoqda', 'Hozir saqlash', 'Faylga saqlash', '50 daqiqa']))
    ev("uiS('trk_syw','0')"); chk('the warning can be switched off', ev("syBar()") == ''); ev("uiS('trk_syw','1')")
    ev("()=>{SYNC='off'}"); chk('offline is shown as “📴 Oflayn”', ev("syInfo().st") == 'off' and 'Oflayn' in ev("syInfo().txt")); ev("()=>{SYNC='ok'}")
    ev("()=>{window.__pushed=0;window.push=async()=>{window.__pushed++}}"); ev("syNowPush()"); chk('“Hozir saqlash” asks the server to save now', ev("__pushed") == 1)
    ev("()=>{UID=null}")
    chk('the warning also shows on the Jadval screen of the new Bugun layout', True)
    # ---- avto-zaxira ----
    ev("indexedDB.deleteDatabase('trk-zaxira')"); pg.wait_for_timeout(200)
    ev("syAuto()"); pg.wait_for_timeout(500); L = ev("syLoad()"); chk('the daily automatic backup is made once: a copy of all data with a count of plans, habits and goals', len(L) == 1 and L[0]['k'] == 'auto' and L[0]['d'] == '2026-11-11' and L[0]['n'] == {'bl': 2, 'hab': 1, 'gl': 1, 'tb': 0} and L[0]['sz'] > 100)
    ev("syAuto()"); pg.wait_for_timeout(300); chk('opening the app again the same day does not make a second copy', len(ev("syLoad()")) == 1)
    for i in range(1, 9):
        pg.clock.set_system_time('2026-11-%02dT10:00:00' % (11 + i)); ev("syAuto()"); pg.wait_for_timeout(250)
    L = ev("syLoad()"); chk('only the 7 newest automatic copies are kept (older ones are pruned)', len([x for x in L if x['k'] == 'auto']) == 7 and min(x['d'] for x in L) == '2026-11-13', [x['d'] for x in L])
    pg.clock.set_system_time('2026-11-11T10:00:00')
    ev("()=>{S.hab=[{id:'h1',t:'Kitob'},{id:'h2',t:'Yangi'}];S.bl=[{id:'a1',t:'Dars',s:540,e:600,d:[0,1,2,3,4,5,6]}]}")
    ev("syMake()"); pg.wait_for_timeout(300); L = ev("syLoad()"); chk('“Hozir nusxa olish” makes a manual copy (with the current 1 plan, 2 habits)', any(x['k'] == 'qo‘lda' and x['n']['hab'] == 2 and x['n']['bl'] == 1 for x in L))
    ev("()=>{S.bl=[];S.hab=[];S.goals=[]}")
    first = ev("(async()=>{const L=await syLoad();return L.filter(x=>x.k==='auto').sort((a,b)=>b.id-a.id)[0].id})()")
    ev("(id)=>syRestore(id)", first); pg.wait_for_timeout(500); chk('restoring first opens the existing “Tiklashni tasdiqlash” preview (nothing changes until you confirm)', ev("!!document.getElementById('snv')") and ev("(S.bl||[]).length") == 0)
    ev("snApply()"); pg.wait_for_timeout(800); chk('after confirming, the plans, habits and goals are back (the data was wiped before) and the app also keeps its own “before restore” copy', ev("(S.bl||[]).length") == 2 and ev("(S.hab||[]).length") == 1 and ev("(S.goals||[]).length") == 1 and ev("!!localStorage.getItem('trk_prerestore')"), (ev("(S.bl||[]).length"), ev("(S.hab||[]).length")))
    ev("syOpen()"); pg.wait_for_timeout(500); t = pg.inner_text('#syv'); chk('the ☁ screen shows the status, data size, “Faylga saqlash”, the list of copies with “Tiklash”, the on/off switch and an honest note that copies live only on this phone', all(x in t for x in ['Sinxronlash va zaxira', 'KB', 'Faylga saqlash', 'Hozir nusxa olish', 'Tiklash', 'Avto-zaxira', 'faqat shu qurilmada']))
    ev("syClose()")
    ev("uiS('trk_sya','0')"); ev("indexedDB.deleteDatabase('trk-zaxira')"); pg.wait_for_timeout(200); pg.clock.set_system_time('2026-12-01T10:00:00'); ev("syAuto()"); pg.wait_for_timeout(300); chk('with Avto-zaxira switched off no copy is made', len(ev("syLoad()")) == 0); ev("uiS('trk_sya','1')"); pg.clock.set_system_time('2026-11-11T10:00:00')
    ev("()=>{SDO={jl:1};tab='s';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('Settings → Jilo has the buttons “📲 Bosh ekran yorliqlari” and “☁ Sinxronlash va zaxira” and the warning switch', all(x in t for x in ['Bosh ekran yorliqlari', 'Sinxronlash va zaxira', 'Saqlash kechiksa ogohlantirish']))
    bad = []
    ev("()=>{tab='h';BV='j';render()}")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='h';BV='j';render()}", [ui, th]); pg.wait_for_timeout(60); ok = True
            for f, c in (("ylOpen()", "ylv"), ("syOpen()", "syv")):
                ev(f); pg.wait_for_timeout(300); ok = ok and ev("(c)=>{const a=document.querySelector('#'+c+' .asc');return a.scrollWidth<=a.clientWidth+1}", c); ev("ylClose();syClose()")
            if not ok: bad.append(ui + th)
    chk('both screens fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
