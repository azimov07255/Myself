import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Sabaq - Sabqi - Manzil: yodlash jurnali, sabqi/manzil hisobi, baholash, bekor qilish, ekran. Soat qotirilgan: 2026-10-31 (shanba) 10:00.
import sys, datetime, http.server, threading, socketserver, os, shutil, functools
from playwright.sync_api import sync_playwright
OUT = ROOT; SITE = '/tmp/site_hf'
shutil.rmtree(SITE, ignore_errors=True); os.makedirs(SITE)
[shutil.copy(os.path.join(OUT, 'tracker', f), SITE) for f in os.listdir(OUT + '/tracker') if os.path.isfile(os.path.join(OUT, 'tracker', f))]
shutil.copytree(OUT + '/data', SITE + '/data'); shutil.copytree(OUT + '/fonts', SITE + '/fonts')
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def handle(self):
        try: super().handle()
        except (BrokenPipeError, ConnectionResetError): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(H, directory=SITE)); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
ok = bad = 0
def chk(name, cond, extra=''):
    global ok, bad
    if cond: ok += 1; print('PASS', name)
    else: bad += 1; print('FAIL', name, extra)
RESET = "()=>{S.ob=1;S.ts=1;const q=S.q;q.m={};q.ord=[];q.rs={};q.rd={};q.ny={};q.ty={};q.lg=[];q.sqd={};q.mzd={};q.mzp=null;q.mz=0;q.sd=7;q.mc=30;q.ppd=3;q.cur=0;S.rw=undefined;rwReset()}"
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o');if(localStorage.getItem('trk_sgr')===null)localStorage.setItem('trk_sgr','a');if(localStorage.getItem('trk_ptb')===null)localStorage.setItem('trk_ptb','a');localStorage.setItem('trk_tqrd','q')}catch(e){}"); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.clock.install(time=datetime.datetime(2026, 10, 31, 10, 0, 0))
    pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') or r.request.url.startswith('data:') else r.abort())
    pg.goto(f'http://127.0.0.1:{PORT}/index.html'); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())")
    ev = pg.evaluate
    sp = ev("SP"); SL = ev("SN.map((_,i)=>SL(i))")
    # ---------- 1. the memorisation log ----------
    ev(RESET); ev("setM(1,5)"); chk('setM logs a dated interval (Baqara pages 0-5)', ev("S.q.lg.length") == 1 and ev("S.q.lg[0].i") == 1 and ev("S.q.lg[0].a") == 0 and ev("S.q.lg[0].b") == 5 and ev("S.q.lg[0].d") == '2026-10-31' and ev("S.q.lg[0].t") == 'n')
    ev("setM(1,8)"); chk('more pages the same day extend the same interval (0-8)', ev("S.q.lg.length") == 1 and ev("S.q.lg[0].b") == 8)
    ev("setM(1,6)"); chk('un-marking pages trims the log (0-6)', ev("S.q.lg[0].b") == 6)
    ev("setM(1,0)"); chk('removing everything removes the interval', ev("S.q.lg.length") == 0)
    ev(RESET); ev("S.q.cur=0;addP(3)")
    lg = ev("S.q.lg.map(e=>[e.i,e.a,e.b])"); tot = sum(e[2] - e[1] for e in lg)
    chk('addP(3) is logged across suras (Fotiha then Baqara), 3 pages in total', abs(tot - 3) < 1e-6 and lg[0][0] == 0 and any(e[0] == 1 for e in lg), lg)
    # ---------- 2. sabqi window ----------
    ev(RESET)
    ev("()=>{const q=S.q;q.m={1:20};q.ord=[1];q.lg=[{id:1,d:dAgo(9),i:1,a:0,b:3,t:'n'},{id:2,d:dAgo(7),i:1,a:3,b:6,t:'n'},{id:3,d:dAgo(3),i:1,a:6,b:9,t:'n'},{id:4,d:dAgo(1),i:1,a:9,b:12,t:'n'},{id:5,d:dk(),i:1,a:12,b:15,t:'n'}];rwReset()}")
    w = ev("ssWin()"); s2 = sp[1]
    chk('sabqi = last 7 days before today (days 7,3,1 ago -> pages 3-12), today and 9 days ago are not in it', w['sab'] == [[s2 + 3, s2 + 12]], w)
    chk('window incl. today (used to keep new pages out of manzil) = pages 3-15', w['inc'] == [[s2 + 3, s2 + 15]], w)
    ev("S.q.sd=3;rwReset()"); chk('window length is adjustable (3 days: only 3 and 1 days ago -> 6-12)', ev("ssWin().sab") == [[s2 + 6, s2 + 12]])
    ev("S.q.sd=7;rwReset()")
    info = ev("ssInfo()"); chk('old (manzil source) = memorised minus window: pages 0-3 and 15-20', info['old'] == [[s2, s2 + 3], [s2 + 15, s2 + 20]] and abs(info['tot'] - 8) < 1e-6, info)
    chk('manzil quota = ceil(8 pages / 30 days) = 1 page a day', info['Q'] == 1)
    ev("S.q.mc=7;rwReset()"); chk('7-day cycle -> 2 pages a day', ev("ssInfo().Q") == 2); ev("S.q.mc=30;rwReset()")
    # ---------- 3. manzil pointer ----------
    ev("S.q.mzp=null;S.q.mz=0"); m1 = ev("ssManzil()")
    chk('first manzil: 1 page from the start of the old part', m1['r'] == [[s2, s2 + 1]] and abs(m1['p'] - 1) < 1e-6, m1)
    chk('the plan is frozen for the day', ev("S.q.lg.push({id:99,d:dk(),i:1,a:15,b:16,t:'n'});rwReset();JSON.stringify(ssManzil().r)") == '[[%d,%d]]' % (s2, s2 + 1)); ev("S.q.lg=S.q.lg.filter(e=>e.id!==99);rwReset()")
    ev("ssSet('m','g')"); chk('marking manzil done moves the pointer to the end of the range and adds 1 page of review (XP)', abs(ev("S.q.mz") - (s2 + 1)) < 1e-6 and abs(ev("S.q.rd[dk()]") - 1) < 1e-6 and ev("S.q.mzd[dk()].q") == 'g')
    chk('after done, the card still shows today\u2019s range (not tomorrow\u2019s)', ev("JSON.stringify(ssParts().find(p=>p.k==='m').r)") == '[[%d,%d]]' % (s2, s2 + 1))
    ev("ssUndo('m')"); chk('undo restores the pointer and the review pages', abs(ev("S.q.mz")) < 1e-6 and abs(ev("S.q.rd[dk()]||0")) < 1e-6 and ev("!S.q.mzd[dk()]"))
    ev("ssSet('m','g')")
    # next day: advance the clock
    pg.clock.set_system_time(datetime.datetime(2026, 11, 1, 10, 0, 0)); ev("rwReset()")
    m2 = ev("ssManzil()"); chk('next day continues where it stopped (pages 1-2 of the old part)', m2['r'] == [[s2 + 1, s2 + 2]], m2)
    ev("S.q.mz=%f;S.q.mzp=null;rwReset()" % (s2 + 2.5)); m3 = ev("ssManzil()")
    chk('range may jump across an interval boundary (2.5 -> 3, then continues in 15-..): wraps to the next old interval', m3['r'] and abs(m3['p'] - 1) < 1e-6 and m3['r'][0][0] >= s2 + 2.5 - 1e-6, m3)
    ev("S.q.mz=%f;S.q.mzp=null;rwReset()" % (s2 + 19.5)); m4 = ev("ssManzil()")
    chk('at the end of the memorised part the pointer wraps around to the beginning', len(m4['r']) == 2 and abs(m4['r'][0][0] - (s2 + 19.5)) < 1e-6 and abs(m4['r'][1][0] - s2) < 1e-6, m4)
    pg.clock.set_system_time(datetime.datetime(2026, 10, 31, 10, 0, 0))
    # ---------- 4. sabqi rating ----------
    ev(RESET)
    ev("()=>{const q=S.q;q.m={1:20,2:6};q.ord=[1,2];q.rs={};initRs(1);initRs(2);q.lg=[{id:1,d:dAgo(2),i:1,a:3,b:6,t:'n'},{id:2,d:dAgo(1),i:2,a:0,b:2,t:'n'}];rwReset()}")
    sab = ev("ssParts().find(p=>p.k==='q')"); chk('sabqi lists both ranges (Baqara 3-6 and Oli Imron 0-2) = 5 pages', abs(sab['p'] - 5) < 1e-6 and len(sab['r']) == 2, sab)
    ev("ssSet('q','g')"); chk('"Yaxshi" on sabqi: +5 review pages, no relearn entries, not weak', abs(ev("S.q.rd[dk()]") - 5) < 1e-6 and ev("S.q.lg.filter(e=>e.t==='r').length") == 0 and ev("!S.q.rs[1].weak"))
    ev("ssSet('q','w')"); chk('re-rating to "Zaif" replaces the rating (still 5 pages, not 10), adds today\u2019s relearn entries and flags the suras weak', abs(ev("S.q.rd[dk()]") - 5) < 1e-6 and ev("S.q.lg.filter(e=>e.t==='r').length") == 2 and ev("S.q.rs[1].weak") is True and ev("S.q.rs[2].weak") is True)
    pg.clock.set_system_time(datetime.datetime(2026, 11, 1, 10, 0, 0)); ev("rwReset()")
    sab2 = ev("ssParts().find(p=>p.k==='q').r"); chk('the weak pages come back in tomorrow\u2019s sabqi (relearn entries are dated yesterday)', any(abs(x[0] - (sp[1] + 3)) < 1e-6 for x in sab2), sab2)
    pg.clock.set_system_time(datetime.datetime(2026, 10, 31, 10, 0, 0)); ev("rwReset()")
    ev("ssUndo('q')"); chk('undo removes the relearn entries and the review pages', ev("S.q.lg.filter(e=>e.t==='r').length") == 0 and abs(ev("S.q.rd[dk()]||0")) < 1e-6)
    # ---------- 5. quest + XP ----------
    ev("S.q.ppd=3;S.q.cur=3;rwReset()"); q = ev("RWQ.find(q=>q.id==='rev')")
    chk('the review quest follows the new plan: 1 part not done yet -> 0/1 .. 2 parts (sabqi + manzil)', ev("RWQ.find(q=>q.id==='rev').g()") == ev("ssParts().length") and ev("RWQ.find(q=>q.id==='rev').n()") == 0)
    ev("ssSet('q','g')"); chk('finishing a part counts for the quest', ev("RWQ.find(q=>q.id==='rev').n()") == 1)
    chk('review pages feed XP (3 per page, up to 15 pages)', ev("dayPts(dk()).p.find(x=>x[0]==='Takror')[1]") == 15)
    # ---------- 6. screen ----------
    ev(RESET)
    ev("()=>{const q=S.q;q.m={1:20,2:6};q.ord=[1,2];q.cur=3;q.lg=[{id:1,d:dAgo(2),i:1,a:3,b:6,t:'n'},{id:2,d:dAgo(1),i:2,a:0,b:2,t:'n'}];tab='q';QT='t';TKV='s';rwReset();render()}"); pg.wait_for_timeout(200)
    t = pg.inner_text('#app')
    chk('Takror opens on Sabqi · Manzil with the three steps', 'Bugungi hifz tartibi' in t and '① Sabaq' in t and '② Sabqi' in t and '③ Manzil' in t and 'Oxirgi 7 kun' in t and 'Sozlama' in t, t[:300])
    chk('sabqi card names the pages (Baqara 3..)', 'Baqara' in t and 'Oli Imron' in t)
    pg.evaluate("document.querySelectorAll('canvas').forEach(c=>c.remove());window.scrollTo(0,0)"); pg.screenshot(path='/tmp/hf_top.png')
    pg.click('#app .ssc:nth-of-type(2) >> text=Yaxshi') if False else pg.evaluate("document.querySelectorAll('#app .ssc')[1].querySelector('.btn:not(.s)').click()"); pg.wait_for_timeout(200)
    chk('tapping "Yaxshi" marks the part done on the screen with an undo button', '✓ Bajarildi (yaxshi)' in pg.inner_text('#app') and pg.evaluate("!!document.querySelector('#app button[aria-label=\"Bekor qilish\"]')"))
    pg.evaluate("document.querySelector('#app button[aria-label=\"Bekor qilish\"]').click()"); pg.wait_for_timeout(150)
    chk('undo from the screen works', '✓ Bajarildi' not in pg.inner_text('#app'))
    pg.evaluate("document.querySelectorAll('#app .ssc')[1].querySelectorAll('.btn.s')[0].click()") ; pg.wait_for_timeout(300)
    chk('"Mushafda" opens the reader at the first page of the sabqi range', pg.evaluate("MFO") is True and pg.evaluate("MFPG") == sp[1] + 3, pg.evaluate("MFPG"))
    pg.evaluate("mfClose()"); pg.wait_for_timeout(150); pg.evaluate("()=>{tab='q';QT='t';render()}"); pg.wait_for_timeout(100)
    pg.evaluate("document.querySelectorAll('#app .ssc')[1].querySelectorAll('.btn.s')[1].click()"); pg.wait_for_timeout(350)
    chk('"Sinash" opens the same page in test mode', pg.evaluate("MFPG") == sp[1] + 3 and pg.evaluate("!!(MFT&&MFT.on)") and pg.evaluate("document.querySelectorAll('#mfpg .xh').length") > 3)
    pg.evaluate("mfClose()"); pg.wait_for_timeout(150); pg.evaluate("()=>{tab='q';QT='t';render()}"); pg.wait_for_timeout(100)
    pg.evaluate("document.querySelector('#app .ssst .btn:last-child').click()"); pg.wait_for_timeout(100)
    chk('stepper: sabqi window 7 -> 8 days, saved', ev("S.q.sd") == 8)
    pg.click('#app .seg button >> text=Sura qutilari'); pg.wait_for_timeout(150)
    chk('the old per-sura boxes are still available under "Sura qutilari"', 'Bugungi takror' in pg.inner_text('#app') or 'Sura' in pg.inner_text('#app'))
    pg.click('#app .seg button >> text=Sabqi · Manzil'); pg.wait_for_timeout(100)
    ev(RESET); ev("()=>{tab='q';QT='t';TKV='s';render()}"); pg.wait_for_timeout(150)
    chk('with nothing memorised the screen explains what to do (no crash)', 'Hali yodlangan sahifa yo‘q' in pg.inner_text('#app') and 'Kechirasan' not in pg.inner_text('#app'))
    ev("()=>{S.q.m={1:2};S.q.ord=[1];S.q.lg=[{id:1,d:dk(),i:1,a:0,b:2,t:'n'}];rwReset();render()}"); pg.wait_for_timeout(100)
    chk('only today\u2019s new pages -> nothing to review yet (they are sabaq), explained', 'ertadan sabqi boshlanadi' in pg.inner_text('#app'))
    chk('no JavaScript errors during the whole run', not errs, errs[:3])
    b.close()
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
