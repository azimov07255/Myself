import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# "Nima yangilandi?": versiyalangan yangiliklar, yangilangandan keyin chiqadigan oyna, yangilash tugmasi ustidagi izoh. Soat: 2026-11-05 10:00.
import sys, json
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
VJ = json.load(open((ROOT + '/tracker/version.json'), encoding='utf-8'))
with Run('yangilik', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("()=>{window.__t=[];window.toast=m=>window.__t.push(m);localStorage.removeItem('trk_seenv');tab='s';render()}")
    ok_list = ev("(()=>{const L=NEWSV;if(!L.length||L[0].v!==APP_VER)return false;for(let i=1;i<L.length;i++)if(verCmp(L[i-1].v,L[i].v)<=0)return false;return L.every(x=>x.t&&x.items.length&&x.items.every(y=>y[0]&&y[1]))})()")
    chk('the news list is valid: the newest entry equals the app version, entries are strictly newest-first, each has a summary and items with text and "where to find"', ok_list is True)
    chk('version.json carries the version and the short summary for the update banner (written by the build, equal to the newest entry)', VJ['v'] == ev("APP_VER") and VJ['n'] == ev("NEWSV[0].t"), VJ)
    ev("nvCheck()"); chk('under browser automation the popup never appears by itself (so it cannot disturb tests); real browsers do show it', ev("!document.getElementById('nvbd')") and ev("navigator.webdriver") is True)
    # ---------- birinchi marta ----------
    ev("()=>{window.__nvForce=1;localStorage.removeItem('trk_seenv');nvCheck()}"); pg.wait_for_timeout(100); t = pg.inner_text('#nvbd')
    chk('first time (nothing seen yet) the popup shows only the NEWEST version with its items and where to find them', '🆕 Nima yangilandi?' in t and 'v' + VJ['v'] in t and ev("NEWSV[0].items[0][0].slice(0,30)") in t and ev("NEWSV[0].items[0][1].slice(0,18)") in t and ev("'v'+NEWSV[1].v") not in t, t[:200])
    chk('it is an accessible dialog and the "Tushundim" button has focus', ev("document.querySelector('#nvbd .nvs').getAttribute('role')") == 'dialog' and ev("document.querySelector('#nvbd .nvs').getAttribute('aria-modal')") == 'true' and ev("document.activeElement.id") == 'nvok')
    chk('calling the check again does not open a second popup', (ev("nvCheck()"), ev("document.querySelectorAll('#nvbd').length"))[1] == 1)
    pg.click('#nvok'); pg.wait_for_timeout(60)
    chk('"Tushundim" closes it and remembers this version on the device', ev("!document.getElementById('nvbd')") and ev("localStorage.getItem('trk_seenv')") == VJ['v'])
    ev("nvCheck()"); chk('and it does not appear again for the same version', ev("!document.getElementById('nvbd')"))
    # ---------- bir necha versiya o'tkazib yuborilgan ----------
    NV = ev("NEWSV.slice(0,5).map(x=>x.v)"); ev("(v)=>{localStorage.setItem('trk_seenv',v);nvCheck()}", NV[3]); pg.wait_for_timeout(60); t = pg.inner_text('#nvbd')
    chk('after skipping versions it lists everything newer than the last seen one (the three newest), newest first, and not the one already seen', t.index('v' + NV[0]) < t.index('v' + NV[1]) < t.index('v' + NV[2]) and ('v' + NV[3]) not in t and ('v' + NV[4]) not in t)
    ev("document.getElementById('nvbd').remove()")
    ev("()=>{localStorage.setItem('trk_seenv','2026.11.01-1');nvCheck()}"); pg.wait_for_timeout(60); chk('a long absence shows at most the last 4 versions (no endless list)', ev("document.querySelectorAll('#nvbd .nvs p b').length") == 4); ev("document.getElementById('nvbd').remove()")
    ev("()=>{localStorage.setItem('trk_seenv','2099.01.01-1');nvCheck()}"); chk('a "seen" mark from a newer version shows nothing and is reset to the current one', ev("!document.getElementById('nvbd')") and ev("localStorage.getItem('trk_seenv')") == VJ['v'])
    # Esc va Hammasi
    ev("()=>{localStorage.removeItem('trk_seenv');nvCheck()}"); pg.keyboard.press('Escape'); pg.wait_for_timeout(60); chk('Escape closes it and marks the version as seen', ev("!document.getElementById('nvbd')") and ev("localStorage.getItem('trk_seenv')") == VJ['v'])
    ev("()=>{localStorage.removeItem('trk_seenv');tab='h';render();nvCheck()}"); pg.click('#nvbd >> text=Hammasi'); pg.wait_for_timeout(120)
    chk('"Hammasi" closes the popup and opens Settings with the news section expanded', ev("!document.getElementById('nvbd')") and ev("tab") == 's' and ev("[...document.querySelectorAll('#app details')].some(d=>d.open&&d.textContent.includes('Yangiliklar va qo‘llanma'))"))
    t = pg.inner_text('#app'); ds = ev("[...document.querySelectorAll('#app details.sd')].filter(d=>d.querySelector('summary').textContent.startsWith('🆕 v')).map(d=>[d.open,d.querySelector('summary').textContent])")
    chk('Settings → Yangiliklar lists the latest versions (the newest expanded) and still has the older by-section lists below', len(ds) == 5 and ds[0][0] is True and ds[1][0] is False and ds[0][1].startswith('🆕 v' + VJ['v']) and 'Bo‘limlar bo‘yicha' in t and 'Pul nazorati' in t)
    # ---------- yangilash tugmasi ustidagi izoh ----------
    ev("""()=>{const of=window.fetch;window.fetch=async(u,o)=>{if(String(u).startsWith('version.json'))return new Response(JSON.stringify(window.__vj),{status:200});return of(u,o)};window.__vj={v:'2099.01.01-1',b:'zz',n:'Yangi imkoniyat: test izohi'};UPDX='';UPD=null}""")
    ev("updCheck()"); pg.wait_for_timeout(200); u = ev("document.getElementById('updb')&&document.getElementById('updb').innerText")
    chk('the update banner shows the new version AND a short note about what is new, before you press "Yangilash"', u and 'v2099.01.01-1' in u and 'Yangi imkoniyat: test izohi' in u and 'Yangilash' in u, u)
    ev("()=>{window.__vj={v:'2099.01.02-1',b:'zy'};UPDX='';UPD=null;updCheck()}"); pg.wait_for_timeout(200); chk('without a note the banner is as before', ev("document.querySelectorAll('#updb small').length") == 0 and 'v2099.01.02-1' in ev("document.getElementById('updb').innerText"))
    ev("()=>{window.__vj={v:'2099.01.03-1',b:'zx',n:'<img src=x onerror=alert(1)> Xavfsiz matn'};UPDX='';UPD=null;updCheck()}"); pg.wait_for_timeout(200); chk('a note is shown as plain text (no HTML is ever executed from it)', ev("document.querySelectorAll('#updb img').length") == 0 and 'Xavfsiz matn' in ev("document.getElementById('updb').innerText"))
    ev("()=>{const b=document.getElementById('updb');if(b)b.remove();UPD=null}")
    # ---------- ko'rinish ----------
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1]}", [ui, th]); ev("()=>{localStorage.setItem('trk_seenv','2026.11.01-1');const e=document.getElementById('nvbd');if(e)e.remove();nvCheck()}"); pg.wait_for_timeout(60)
            r = ev("(()=>{const s=document.querySelector('#nvbd .nvs').getBoundingClientRect();return [s.left>=0,s.right<=innerWidth+1,s.bottom<=innerHeight+1,document.documentElement.scrollWidth<=innerWidth+1]})()")
            if not all(r): bad.append((ui, th, r))
    chk('the popup fits the phone screen in Klassik, Yangi and Liquid Glass, light and dark (with 4 versions listed)', not bad, bad)
    ev("()=>{const e=document.getElementById('nvbd');if(e)e.remove();uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
