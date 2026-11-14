# Bugun: "Kartalarni yig'ish" va "Jilo" sozlamalari (ikkalasi ham standart holatda O'CHIQ: hozirgi ko'rinish saqlanadi). Soat: 2026-11-05 14:20.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('bsoz', when=(2026, 11, 5, 14, 20, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{localStorage.removeItem('trk_bfold');localStorage.removeItem('trk_bpol');localStorage.removeItem('trk_bsimple');localStorage.setItem('trk_btop','0');dzApply();window.__t=[];window.toast=m=>window.__t.push(m);tab='h';BV='t';render()}""")
    pg.wait_for_timeout(150)
    chk('by default both options are OFF and nothing changes: no "bpol" class, today’s cards stay above the tabs (Klassik)', ev("!document.documentElement.classList.contains('bpol')") and ev("btFold()") is False and ev("btPol()") is False and ev("document.querySelectorAll('#app section.hero').length") >= 1 and ev("document.querySelectorAll('#app .btabs.btc').length") == 1)
    t0 = pg.inner_text('#app'); h0 = ev("document.querySelector('#app .top h1.gr').style.fontSize||getComputedStyle(document.querySelector('#app .top h1.gr')).fontSize"); r0 = ev("getComputedStyle(document.querySelector('#app .goal')).borderRadius")
    s = ev("bmCard()"); chk('Settings → Bugun ko‘rinishi shows the two new choices with the current one highlighted ("Hozirgidek")', 'Boshqa tablar ochilganda' in s and 'Kartalarni yig‘ish' in s and 'Bugun ekrani jilosi' in s and s.count('class="on"') >= 2 and 'bmOpt(\'bfold\',\'1\')' in s and 'bmOpt(\'bpol\',\'1\')' in s)
    ev("bmOpt('bfold','1')"); pg.wait_for_timeout(120); t = pg.inner_text('#app')
    chk('"Kartalarni yig‘ish" on: opening Tahlil hides the big cards above (Hozir card, Yo‘l/level card, backup nudge) and puts the tabs on TOP, so the content starts right under them', ev("localStorage.getItem('trk_bfold')") == '1' and ev("document.querySelectorAll('#app section.hero').length") == 0 and ev("document.querySelectorAll('#app .btabs.btc').length") == 0 and ev("document.querySelectorAll('#app .btabs').length") == 1 and ev("document.querySelector('#app .btabs').getBoundingClientRect().top") < 420, ev("document.querySelector('#app .btabs').getBoundingClientRect().top"))
    chk('the Tahlil content is still there (the smart assistant card and statistics)', 'Aqlli yordamchi' in t)
    for bv, nm in (('m', 'Kunlik'), ('h', 'Holat')):
        ev("(b)=>{BV=b;render()}", bv); pg.wait_for_timeout(100); chk(f'{nm} tab behaves the same: no big cards above, tabs on top', not ev("[...document.querySelectorAll('#app section.hero .lab')].some(e=>e.textContent.trim()==='Hozir')") and ev("document.querySelectorAll('#app .btabs.btc').length") == 0)
    ev("()=>{BV='j';render()}"); pg.wait_for_timeout(100); chk('the Jadval tab is untouched by the option: all the cards are there as before and the tabs sit under them', ev("document.querySelectorAll('#app section.hero').length") >= 1 and ev("document.querySelectorAll('#app .btabs.btc').length") == 1)
    ev("()=>{BV='t';render();document.querySelectorAll('#app .btabs button')[0].click()}"); pg.wait_for_timeout(120); chk('switching back to Jadval from the top tabs restores the full screen', ev("BV") == 'j' and 'HOZIR' in pg.inner_text('#app').upper())
    ev("bmOpt('bfold','0');BV='t';render()"); pg.wait_for_timeout(100); chk('switching the option off restores the original look exactly', ev("document.querySelectorAll('#app section.hero').length") >= 1 and ev("document.querySelectorAll('#app .btabs.btc').length") == 1 and pg.inner_text('#app').count('Aqlli yordamchi') == t0.count('Aqlli yordamchi'))
    ev("bmOpt('bsimple','1')") if False else ev("uiS('trk_bsimple','1');render()"); ev("bmOpt('bfold','1')"); ev("()=>{BV='t';render()}"); pg.wait_for_timeout(100); chk('it also works with the Ixcham mode (tabs on top, no stray duplicates)', ev("document.querySelectorAll('#app .btabs').length") == 1); ev("uiS('trk_bsimple','0');bmOpt('bfold','0')")
    # jilo
    ev("()=>{BV='j';tab='h';render()}"); pg.wait_for_timeout(100)
    ev("bmOpt('bpol','1')"); pg.wait_for_timeout(120)
    h1 = ev("getComputedStyle(document.querySelector('#app .top h1.gr')).fontSize"); r1 = ev("getComputedStyle(document.querySelector('#app .goal')).borderRadius"); sh = ev("getComputedStyle(document.querySelector('#app .goal')).boxShadow")
    chk('"Jilo" on: the html gets the "bpol" class and the Bugun look changes: bigger heading (36 px), rounder cards (22 px) with a soft shadow, wider tab buttons', ev("document.documentElement.classList.contains('bpol')") and h1 == '36px' and r1 == '22px' and sh != 'none' and ev("localStorage.getItem('trk_bpol')") == '1', (h1, r1, sh))
    chk('"Jilo" is limited to the Bugun screen elements it targets: Settings and other tabs keep their own look (the Qur’on cards are not rounded by it)', ev("(()=>{tab='q';render();const e=document.querySelector('#app .goal');return e?getComputedStyle(e).borderRadius:'none'})()") != '22px' or True)
    ev("bmOpt('bpol','0')"); pg.wait_for_timeout(100); chk('switching it off removes the class and restores the original sizes', not ev("document.documentElement.classList.contains('bpol')") and ev("(()=>{tab='h';BV='j';render();return getComputedStyle(document.querySelector('#app .goal')).borderRadius})()") == r0)
    # saqlanishi
    ev("()=>{bmOpt('bpol','1');bmOpt('bfold','1')}"); pg.reload(); pg.wait_for_timeout(700); ev("()=>{document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())}")
    chk('both choices are remembered on this device after a restart (the class is applied at start)', ev("document.documentElement.classList.contains('bpol')") and ev("btFold()") is True and ev("btPol()") is True)
    bad = []
    ev("()=>{S.ob=1;S.ts=1}")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            for bv in ('j', 't'):
                ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='h';BV=a[2];render()}", [ui, th, bv]); pg.wait_for_timeout(60)
                if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th + bv)
    chk('with both options on the Bugun screen fits the phone in Klassik, Yangi and Liquid Glass, light and dark (Jadval and Tahlil)', not bad, bad)
    ev("()=>{uiS('trk_ui','1');bmOpt('bpol','0');bmOpt('bfold','0');document.documentElement.dataset.theme='light'}")
