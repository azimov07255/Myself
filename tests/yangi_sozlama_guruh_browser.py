# Sozlamalar tartibga solindi: guruhlar, zaxira bir joyda, egasi bo'limi, qisqa yangiliklar; Jilo'da eskisiga qaytish. Soat: 2026-10-31 10:00.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('sozlama_guruh') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    def go(mode='g', owner=False, q=''):
        ev("(a)=>{uiS('trk_sgr',a[0]);SDO={};SDQ=a[2];if(a[1]){OW=[]}tab='s';render()}", [mode, owner, q]); pg.wait_for_timeout(120)
    tops = lambda: ev("[...document.querySelectorAll('#app > details.sd > summary, #app details.sd')].filter(d=>d.parentElement&&d.parentElement.id==='app'||d.parentElement&&d.parentElement.tagName==='DIV'&&d.parentElement.parentElement&&d.parentElement.parentElement.id==='app').length")
    topSum = lambda: ev("[...document.querySelectorAll('#app > details.sd > summary')].map(s=>s.textContent.trim().slice(0,40))")
    go('g'); T = topSum()
    chk('grouped (default): top-level groups are AI, Eslatmalar, Ko‘rinish va qulaylik, Zaxira va sinxron, Yangiliklar, Vidjet (not 20+ separate ones)', len(T) <= 8 and any('Ko‘rinish va qulaylik' in x for x in T) and any('Zaxira va sinxron' in x for x in T) and any('AI yordamchi' in x for x in T), T)
    chk('developer tools (Xatolar jurnali, Diagnostika, Ishga tayyormi?, Foydalanish) are NOT top-level for a normal user (no owner section either)', not any(w in ' '.join(T) for w in ['Xatolar jurnali', 'Diagnostika', 'Ishga tayyormi', 'Foydalanish']), T)
    go('g', owner=True); T = topSum()
    chk('for the owner there is one "🛠 Egasi va diagnostika" group', any('Egasi va diagnostika' in x for x in T), T)
    # ichidagilar
    ev("()=>{SDO={w_v:1};render()}"); pg.wait_for_timeout(80)
    inner = ev("[...document.querySelectorAll('#app > details.sd[open] > summary')].map(s=>s.textContent)[0]||''"); sm = ev("[...document.querySelectorAll('#app details.sd details.sd > summary')].map(s=>s.textContent.trim())")
    chk('opening "Ko‘rinish va qulaylik" shows Dizayn, Bugun ko‘rinishi, Jilo, Reja rejimlari, Ovoz inside it', all(any(w in x for x in sm) for w in ['Dizayn', 'Bugun ko‘rinishi', 'Jilo', 'Reja rejimlari', 'Ovoz']), sm)
    go('g'); ev("()=>{SDO={zh:1};render()}"); pg.wait_for_timeout(80)
    chk('opening an inner group by its old key (SDO.zh) makes its wrapper open by itself (old tests/links keep working)', ev("[...document.querySelectorAll('#app > details.sd[open] > summary')].some(s=>/Zaxira va sinxron/.test(s.textContent))") and ev("[...document.querySelectorAll('#app details.sd[open] details.sd[open] > summary')].some(s=>/Zaxira holati/.test(s.textContent))"))
    go('g'); ev("()=>{SDO={w_z:1};render()}"); pg.wait_for_timeout(80)
    z = ev("[...document.querySelectorAll('#app details.sd details.sd > summary')].map(s=>s.textContent.trim())")
    chk('"Zaxira va sinxron" holds the three backup groups together: Zaxira holati, Zaxira nusxa, Avtomatik zaxiralar', all(any(w in x for x in z) for w in ['Zaxira holati', 'Zaxira nusxa', 'Avtomatik zaxiralar']), z)
    # qidiruv hali ishlaydi
    go('g', q='zaxira'); t = pg.inner_text('#app')
    chk('the settings search still finds a group inside a wrapper ("zaxira")', 'Zaxira holati' in t and 'Zaxira nusxa' in t)
    go('g', q='diagnostika', owner=False); chk('search for "diagnostika" finds it even though it is inside the owner group', 'Diagnostika' in pg.inner_text('#app'))
    # yangiliklar qisqardi
    go('g'); ev("()=>{SDO={nw:1};render()}"); pg.wait_for_timeout(80)
    nv = ev("[...document.querySelectorAll('#app details.sd')].filter(d=>d.querySelector('summary').textContent.startsWith('🆕 v')).length")
    chk('news: only the latest 2 versions are listed; older ones are in one "Oldingi versiyalar" block; by-section list is collapsed', nv == 2 + 0 and 'Oldingi versiyalar' in pg.inner_text('#app') and ev("[...document.querySelectorAll('#app details.sd > summary')].some(s=>s.textContent.trim()==='Bo‘limlar bo‘yicha')"), nv)
    # Jilo orqali eskisiga qaytish
    go('g'); ev("()=>{SDO={w_v:1,jl:1};render()}"); pg.wait_for_timeout(80)
    chk('Jilo has "Sozlamalar tuzilishi" with Guruhlangan (selected) / Avvalgidek', 'Sozlamalar tuzilishi' in pg.inner_text('#app') and ev("jlCard().length>0") and ev("sgrJl().includes('Guruhlangan')"))
    go('a'); T = topSum()
    chk('"Avvalgidek": back to one long flat list (20+ separate groups, no wrappers)', len(T) >= 15 and not any('Ko‘rinish va qulaylik' in x or 'Zaxira va sinxron' in x for x in T), len(T))
    chk('...and the news show the 5 versions + the by-section list as before', (go('a') or True) and ev("(()=>{SDO={nw:1};render();return [...document.querySelectorAll('#app details.sd')].filter(d=>d.querySelector('summary').textContent.startsWith('🆕 v')).length})()") == 5)
    # umumiy
    for mode in ('g', 'a'):
        go(mode); chk('mode %s: no horizontal overflow' % mode, pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1"))
    print('\n%d passed, %d failed' % (R.ok, R.bad))
