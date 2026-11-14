import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Mushaf o'quvchisi: haqiqiy Chromium (telefon o'lchami) + lokal server. Hamma 604 sahifa, uzoq bosish, rang/izoh, varaqlash, sinov.
import http.server, threading, socketserver, os, shutil, json, sys, functools, time
from playwright.sync_api import sync_playwright
OUT = ROOT; SITE = '/tmp/site_mf'
shutil.rmtree(SITE, ignore_errors=True); os.makedirs(SITE)
[shutil.copy(os.path.join(OUT, 'tracker', f), SITE) for f in os.listdir(OUT + '/tracker') if os.path.isfile(os.path.join(OUT, 'tracker', f))]; shutil.copytree(OUT + '/data', SITE + '/data'); shutil.copytree(OUT + '/fonts', SITE + '/fonts')
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def handle(self):
        try: super().handle()
        except (BrokenPipeError, ConnectionResetError): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(H, directory=SITE)); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
D = json.load(open(OUT + '/data/quran-mushaf.json', encoding='utf-8'))
ok = bad = 0
def chk(name, cond, extra=''):
    global ok, bad
    if cond: ok += 1; print('PASS', name)
    else: bad += 1; print('FAIL', name, extra)
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o');if(localStorage.getItem('trk_sgr')===null)localStorage.setItem('trk_sgr','a');if(localStorage.getItem('trk_ptb')===null)localStorage.setItem('trk_ptb','a')}catch(e){}"); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append('console: ' + m.text) if m.type == 'error' and not any(x in m.text for x in ('favicon', 'net::ERR_FAILED', 'ERR_BLOCKED')) else None)
    pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') or r.request.url.startswith('data:') else r.abort())
    pg.goto(f'http://127.0.0.1:{PORT}/index.html'); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())")
    pg.evaluate("()=>{S.ob=1;S.ts=1;S.q.m[1]=2;S.q.ord=[1];tab='q';QT='u';render()}"); pg.wait_for_timeout(150)
    chk('Mushaf tab renders without crash', 'Kechirasan' not in pg.inner_text('#app') and 'DAVOM ETISH' in pg.inner_text('#app'))
    chk('surah list has 114 rows', pg.evaluate("document.querySelectorAll('#mfl .row').length") == 114)
    pg.fill('.mfq', 'baq'); chk('search "baq" finds only Baqara', pg.evaluate("document.querySelectorAll('#mfl .row').length") == 1 and 'Baqara' in pg.inner_text('#mfl'))
    pg.evaluate("()=>{MV='j';render()}"); chk('juz list has 30 rows', pg.evaluate("document.querySelectorAll('#app .row').length") == 30)
    chk('app SP table = surah start pages of the data', pg.evaluate("SP") == D['sp'] and pg.evaluate("J.slice(0,30)") == D['jp'])
    # ---- open page 3 ----
    pg.evaluate("()=>{MV='s';mfOpen(3)}"); pg.wait_for_function("document.querySelectorAll('#mfpg .mx').length>0", timeout=8000); pg.wait_for_timeout(500)
    pg.evaluate("document.fonts.load('20px QPC','\\u0627')"); pg.wait_for_timeout(300)
    info = pg.evaluate("()=>{const g=document.getElementById('mfpg');const rows=[...g.querySelectorAll('.mx')];return {n:rows.length,fs:parseFloat(g.dataset.fs),over:rows.filter(r=>r.scrollWidth>r.clientWidth+1).length,font:document.fonts.check('20px QPC'),title:document.getElementById('mfn').textContent,sub:document.getElementById('mfj').textContent,first:rows[0].innerText.slice(0,30),W:g.clientWidth,docW:document.documentElement.scrollWidth}}")
    chk('page 3: 15 text rows, nothing wider than the page, font loaded', info['n'] == 15 and info['over'] == 0 and info['font'], info)
    chk('page 3 header shows the surah and juz', 'البقرة' in info['title'] and "Juz’ 1" in info['sub'] and '3-bet' in info['sub'], info)
    chk('page does not scroll sideways', info['docW'] <= 392, info)
    chk('rounded-zero marks are drawn with the font\'s own glyph (no U+06DF on screen)', pg.evaluate("!document.getElementById('mfpg').innerText.includes('\\u06DF')"))
    pg.screenshot(path='/tmp/shot_p3.png')
    # ---- all 604 pages ----
    res = pg.evaluate("""()=>{const bad=[];let minfs=99,maxfs=0;const t0=performance.now();
      for(let n=1;n<=604;n++){MFPG=n;mfDraw();const g=document.getElementById('mfpg');const rows=[...g.querySelectorAll('.mx')];
        const exp=MF.p[n].r.filter(r=>r[0]==='x').length;const fs=parseFloat(g.dataset.fs);minfs=Math.min(minfs,fs);maxfs=Math.max(maxfs,fs);
        const over=rows.filter(r=>r.scrollWidth>r.clientWidth+1).length;const wcount=rows.reduce((a,r)=>a+r.children.length,0);
        const expw=MF.p[n].r.filter(r=>r[0]==='x').reduce((a,r)=>a+r[1].length,0);
        if(rows.length!==exp||over||wcount!==expw||!(fs>=11))bad.push([n,rows.length,exp,over,wcount,expw,fs])}
      return {bad:bad.slice(0,8),nbad:bad.length,minfs,maxfs,ms:Math.round(performance.now()-t0)}}""")
    chk('ALL 604 pages: row count, word count, no overflow, readable font size', res['nbad'] == 0, res)
    print('   font size range over all pages: %.1f - %.1f px (390px wide phone), %d ms for 604 draws' % (res['minfs'], res['maxfs'], res['ms']))
    # screenshots of special pages
    for n in (1, 2, 12, 52, 77, 586, 604):
        pg.evaluate(f"()=>{{MFPG={n};mfDraw()}}"); pg.wait_for_timeout(350); pg.evaluate("mfFit()"); pg.screenshot(path=f'/tmp/shot_p{n}.png')
    pg.evaluate("()=>{MFPG=3;mfDraw()}"); pg.wait_for_timeout(200)
    # ---- long press -> sheet -> colour ----
    box = pg.evaluate("()=>{const e=document.querySelector('#mfpg .mw[data-v=\"2008\"]');const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}")
    pg.mouse.move(*box); pg.mouse.down(); pg.wait_for_timeout(650)
    chk('long press opens the verse sheet', pg.evaluate("!!document.getElementById('mfs')") and 'Baqara 2:8' in pg.inner_text('#mfs'))
    pg.mouse.up(); pg.click('#mfs .mfd:nth-child(2)'); pg.wait_for_timeout(200)
    chk('colour 2 saved for verse 2:8 and painted on all its words', pg.evaluate("S.mq.hl['2008'].c") == 2 and pg.evaluate("document.querySelectorAll('#mfpg .mw.h2[data-v=\"2008\"]').length") >= 3)
    # note
    pg.mouse.move(*box); pg.mouse.down(); pg.wait_for_timeout(650); pg.mouse.up(); pg.click('#mfs >> text=Izoh'); pg.fill('#mfnt', 'Munofiqlar haqida'); pg.click('#mfs >> text=Saqlash'); pg.wait_for_timeout(150)
    chk('note saved and marked on the verse number', pg.evaluate("S.mq.hl['2008'].n") == 'Munofiqlar haqida' and pg.evaluate("document.querySelectorAll('#mfpg .mk.hn[data-v=\"2008\"]').length") == 1)
    # remove colour but keep note
    pg.mouse.move(*box); pg.mouse.down(); pg.wait_for_timeout(650); pg.mouse.up(); pg.click('#mfs .mfd.x0'); pg.wait_for_timeout(120)
    chk('removing the colour keeps the note', pg.evaluate("S.mq.hl['2008'].c") == 0 and pg.evaluate("S.mq.hl['2008'].n") != '')
    # weak mark
    pg.mouse.move(*box); pg.mouse.down(); pg.wait_for_timeout(650); pg.mouse.up(); pg.click('#mfs >> text=Zaif oyat'); pg.wait_for_timeout(120)
    chk('weak mark saved, verse number turns red, linked to Takror (Baqara is in the memorization list)', pg.evaluate("S.mq.wk['2008'].s") == 0 and pg.evaluate("!!document.querySelector('#mfpg .mk.wkm[data-v=\"2008\"]')") and pg.evaluate("S.q.rs[1].weak===true&&S.q.rs[1].box===0"))
    # ---- swipe (synthetic touches) ----
    def swipe(dx):
        pg.evaluate("""(dx)=>{const el=document.querySelector('#mfpg .mx');const r=el.getBoundingClientRect();const x=r.x+r.width/2,y=r.y+r.height/2;
          const mk=(t,cx)=>new Touch({identifier:1,target:el,clientX:cx,clientY:y});
          el.dispatchEvent(new TouchEvent('touchstart',{touches:[mk(el,x)],changedTouches:[mk(el,x)],bubbles:true}));
          el.dispatchEvent(new TouchEvent('touchmove',{touches:[mk(el,x+dx/2)],changedTouches:[mk(el,x+dx/2)],bubbles:true}));
          el.dispatchEvent(new TouchEvent('touchend',{touches:[],changedTouches:[mk(el,x+dx)],bubbles:true}))}""", dx); pg.wait_for_timeout(250)
    swipe(140); chk('swipe right = next page (RTL book): 3 -> 4', pg.evaluate("MFPG") == 4)
    swipe(-140); chk('swipe left = previous page: 4 -> 3', pg.evaluate("MFPG") == 3)
    swipe(30); chk('a short drag does not turn the page', pg.evaluate("MFPG") == 3)
    pg.click('.mfnv .btn >> text=Keyingi'); pg.wait_for_timeout(200); chk('"Keyingi" button -> page 4', pg.evaluate("MFPG") == 4)
    pg.fill('#mfi', '300'); pg.dispatch_event('#mfi', 'change'); pg.wait_for_timeout(200); chk('typing a page number jumps there', pg.evaluate("MFPG") == 300)
    pg.fill('#mfi', '9999'); pg.dispatch_event('#mfi', 'change'); pg.wait_for_timeout(200); chk('page number is clamped to 604', pg.evaluate("MFPG") == 604)
    pg.evaluate("mfShow(0)"); pg.wait_for_timeout(200); chk('page number is clamped to 1', pg.evaluate("MFPG") == 1)
    # ---- bookmarks and recents ----
    pg.evaluate("mfShow(50)"); pg.wait_for_timeout(150); pg.click('#mfb'); chk('bookmark toggles on (star filled, saved)', pg.evaluate("S.mq.bm.includes(50)") and pg.inner_text('#mfb') == '★')
    pg.click('#mfb'); chk('bookmark toggles off', not pg.evaluate("S.mq.bm.includes(50)") and pg.inner_text('#mfb') == '☆')
    chk('last page and recents are remembered', pg.evaluate("S.mq.last") == 50 and pg.evaluate("S.mq.rec[0].p") == 50 and pg.evaluate("S.mq.rec.length") <= 10)
    # ---- recall test ----
    pg.evaluate("mfShow(3)"); pg.wait_for_timeout(200)
    pg.evaluate("mfTestStart('b')"); pg.wait_for_timeout(200)
    st = pg.evaluate("()=>{const out={};document.querySelectorAll('#mfpg .mw:not(.mk)').forEach(e=>{const k=e.dataset.v;(out[k]=out[k]||[]).push(e.classList.contains('xh'))});return out}")
    starts_ok = all((len(v) <= 2 and not any(v)) or (not v[0] and not v[1] and all(v[2:])) for k, v in st.items() if k not in ('2006',))
    chk('hidden = every word after the 2nd of verses that begin on this page', starts_ok, {k: v for k, v in list(st.items())[:3]})
    chk('verse numbers stay visible in test mode', pg.evaluate("[...document.querySelectorAll('#mfpg .mk')].every(e=>!e.classList.contains('xh'))"))
    chk('status strip shows the test', 'Sinov' in pg.inner_text('#mfst'))
    pg.screenshot(path='/tmp/shot_test_b.png')
    box2 = pg.evaluate("()=>{const e=document.querySelector('#mfpg .mw.xh[data-v=\"2010\"]');const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}")
    pg.mouse.click(*box2); pg.wait_for_timeout(250)
    chk('tapping a hidden verse reveals it and shows the grade bar', pg.evaluate("document.querySelectorAll('#mfpg .mw.xh[data-v=\"2010\"]').length") == 0 and pg.is_visible('#mfg') and '2:10' in pg.inner_text('#mfg'))
    pg.click('#mfg >> text=Qisman'); pg.wait_for_timeout(200)
    chk('grading "Qisman" saves weak mark (s=1), counts it and hides the bar', pg.evaluate("S.mq.wk['2010'].s") == 1 and pg.evaluate("MFT.st") == [0, 1, 0] and not pg.is_visible('#mfg'))
    box3 = pg.evaluate("()=>{const e=document.querySelector('#mfpg .mw.xh[data-v=\"2011\"]');const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}")
    pg.mouse.click(*box3); pg.wait_for_timeout(200); pg.click('#mfg >> text=Bildim'); pg.wait_for_timeout(200)
    chk('grading "Bildim" saves s=2 (not weak)', pg.evaluate("S.mq.wk['2011'].s") == 2 and not pg.evaluate("!!document.querySelector('#mfpg .mk.wkm[data-v=\"2011\"]')"))
    pg.evaluate("mfTestStart('r')"); pg.wait_for_timeout(200)
    chk('test mode "faqat raqam": ALL words hidden, numbers visible', pg.evaluate("[...document.querySelectorAll('#mfpg .mw:not(.mk)')].every(e=>e.classList.contains('xh'))") and pg.evaluate("document.querySelectorAll('#mfpg .mk').length") > 5)
    pg.screenshot(path='/tmp/shot_test_r.png')
    pg.evaluate("mfTestEnd()"); pg.wait_for_timeout(150)
    chk('ending the test shows the text again', pg.evaluate("document.querySelectorAll('#mfpg .xh').length") == 0 and pg.evaluate("MFT") is None)
    # ---- lists reflect the marks ----
    pg.evaluate("mfClose()"); pg.wait_for_timeout(200)
    chk('closing returns to the app and unlocks the page', not pg.evaluate("!!document.getElementById('mf')") and not pg.evaluate("document.documentElement.classList.contains('ovl')"))
    pg.evaluate("()=>{MV='n';render()}"); chk('"Izohlar" list shows the noted verse', 'Baqara 2:8' in pg.inner_text('#app') and 'Munofiqlar' in pg.inner_text('#app'))
    pg.evaluate("()=>{MV='w';render()}"); t = pg.inner_text('#app'); chk('"Zaif" list shows 2:8 (Bilmadim) and 2:10 (Qisman) but not 2:11', 'Baqara 2:8' in t and 'Baqara 2:10' in t and '2:11' not in t, t[:300])
    pg.evaluate("()=>{MV='b';render()}"); chk('"Xatcho\'p" tab renders', 'Kechirasan' not in pg.inner_text('#app'))
    # offline cache: data comes from IndexedDB on the next open
    pg.evaluate("()=>{MF=null;MFP=null}"); got = []; pg.on('request', lambda r: got.append(r.url) if 'quran-mushaf' in r.url else None)
    pg.evaluate("mfOpen(10)"); pg.wait_for_timeout(1200)
    chk('second open reads the Quran from IndexedDB (no new download)', not got and pg.evaluate("MFPG") == 10, got)
    pg.evaluate("mfClose()")
    # ---- link with memorization (Yodlash / Takror) ----
    pg.evaluate("()=>{S.q.cur=1;S.q.m[1]=2;S.q.ord=[1];S.q.ty={};S.q.rs={1:{box:0,due:dk(),weak:false,last:''}};tab='q';QT='y';render()}"); pg.wait_for_timeout(150)
    chk('Yodlash shows "Mushafda ochish" with today\u2019s page (Baqara starts on page 2, 2 pages learned -> 4)', 'Mushafda ochish (4-bet)' in pg.inner_text('#app'))
    pg.click('#app >> text=Mushafda ochish (4-bet)'); pg.wait_for_function("MFO&&document.querySelectorAll('#mfpg .mx').length>0", timeout=8000); pg.wait_for_timeout(300)
    chk('... and it opens the reader on page 4', pg.evaluate("MFPG") == 4)
    pg.evaluate("mfShow(3)"); pg.wait_for_timeout(300)
    def holdv(v):
        bx = pg.evaluate("(v)=>{const e=document.querySelector('#mfpg .mw[data-v=\"'+v+'\"]');const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}", v)
        pg.mouse.move(*bx); pg.mouse.down(); pg.wait_for_timeout(650); pg.mouse.up()
    holdv('2008'); pg.click('#mfs >> text=Bugungi yodlashga'); pg.wait_for_timeout(150)
    chk('verse sheet: "Bugungi yodlashga" adds 2:8 to today\u2019s picks', pg.evaluate("JSON.stringify(S.q.ty[dk()])") == '[{"s":1,"a":8,"b":8,"x":0}]', pg.evaluate("JSON.stringify(S.q.ty)"))
    holdv('2009'); pg.click('#mfs >> text=Bugungi yodlashga'); pg.wait_for_timeout(150)
    chk('the next verse (2:9) is merged into the same range 8-9', pg.evaluate("JSON.stringify(S.q.ty[dk()])") == '[{"s":1,"a":8,"b":9,"x":0}]')
    holdv('2008'); pg.click('#mfs >> text=Bugungi yodlashga'); pg.wait_for_timeout(150)
    chk('adding a verse that is already there changes nothing', pg.evaluate("S.q.ty[dk()].length") == 1 and pg.evaluate("S.q.ty[dk()][0].b") == 9)
    holdv('2012'); pg.click('#mfs >> text=Bugungi yodlashga'); pg.wait_for_timeout(150)
    chk('a non-adjacent verse (2:12) starts a new range', pg.evaluate("S.q.ty[dk()].length") == 2)
    pg.evaluate("mfClose()"); pg.wait_for_timeout(200)
    pg.evaluate("()=>{tab='q';QT='y';render()}"); pg.wait_for_timeout(150)
    chk('Yodlash lists the ranges picked in the Mushaf', 'Baqara, 8' in pg.inner_text('#app') and '9-oyatlar' in pg.inner_text('#app'))
    pg.click('#app .row >> nth=0 >> button[aria-label="Mushafda ochish"]') if False else pg.evaluate("document.querySelector('#app button[aria-label=\"Mushafda ochish\"]').click()")
    pg.wait_for_function("MFO&&document.querySelectorAll('#mfpg .mx').length>0", timeout=8000); pg.wait_for_timeout(300)
    chk('the 📖 button next to a range opens the page that contains it (2:8 is on page 3)', pg.evaluate("MFPG") == 3)
    pg.evaluate("mfClose()"); pg.wait_for_timeout(200)
    pg.evaluate("()=>{tab='q';QT='t';TKV='b';render()}"); pg.wait_for_timeout(150)
    chk('Takror card (Sura qutilari) has "Mushafda sinab ko\u2018r"', 'Mushafda sinab ko‘r' in pg.inner_text('#app'))
    pg.click('#app >> text=Mushafda sinab ko‘r'); pg.wait_for_function("MFO&&document.querySelectorAll('#mfpg .mx').length>0", timeout=8000); pg.wait_for_timeout(300)
    chk('it opens the sura\u2019s first page already in test mode', pg.evaluate("MFPG") == 2 and pg.evaluate("!!(MFT&&MFT.on)") and 'Sinov' in pg.inner_text('#mfst') and pg.evaluate("document.querySelectorAll('#mfpg .xh').length") > 5)
    pg.evaluate("mfClose()"); pg.wait_for_timeout(200)
    # ---- in-app switch ----
    pg.evaluate("()=>{tab='q';QT='u';render()}")
    pg.evaluate("()=>{tab='s';render()}"); pg.wait_for_timeout(100)
    chk('Settings has the "Mushaf bo\u2018limi" group with an off button', 'Mushaf bo\u2018limi' in pg.inner_text('#app') and pg.evaluate("mfSet().includes('Mushaf\u2019ni o\u2018chirish')"))
    pg.evaluate("()=>{tab='q';QT='u';mfToggle()}"); pg.wait_for_timeout(120)
    chk('turning it off: flag saved, tab removed, page falls back to Yodlash', pg.evaluate("S.nomf") == 1 and pg.evaluate("QT") == 'y' and 'Mushaf' not in pg.inner_text('.seg.sc'))
    pg.evaluate("mfOpen(3)"); pg.wait_for_timeout(150); chk('while hidden, the reader cannot be opened', not pg.evaluate("!!document.getElementById('mf')"))
    chk('the saved marks survive hiding', pg.evaluate("Object.keys(S.mq.hl).length") >= 1 and pg.evaluate("Object.keys(S.mq.wk).length") >= 2)
    pg.evaluate("mfToggle()"); pg.wait_for_timeout(120); chk('turning it back on restores the tab', pg.evaluate("S.nomf") == 0 and 'Mushaf' in pg.inner_text('.seg.sc'))
    chk('no JavaScript errors during the whole run', not errs, errs[:3])
    b.close()
    # ---- friends build: MUSHAF_MODE='off' ----
    OFF = '/tmp/site_mf_off'; shutil.rmtree(OFF, ignore_errors=True); shutil.copytree(SITE, OFF)
    src = open(OFF + '/index.html', encoding='utf-8').read(); assert "const MUSHAF_MODE='all';" in src
    open(OFF + '/index.html', 'w', encoding='utf-8').write(src.replace("const MUSHAF_MODE='all';", "const MUSHAF_MODE='off';"))
    srv2 = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(H, directory=OFF)); P2 = srv2.server_address[1]; threading.Thread(target=srv2.serve_forever, daemon=True).start()
    b2 = p.chromium.launch(); c2 = b2.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True); q = c2.new_page(); e2 = []; reqs = []
    q.on('pageerror', lambda e: e2.append(str(e))); q.on('request', lambda r: reqs.append(r.url))
    q.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') else r.abort())
    q.goto(f'http://127.0.0.1:{P2}/index.html'); q.wait_for_timeout(500); q.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())")
    q.evaluate("()=>{S.ob=1;S.ts=1;tab='q';QT='u';render()}"); q.wait_for_timeout(150)
    chk("friends build: no Mushaf tab, page shows Yodlash instead of crashing", 'Mushaf' not in q.inner_text('.seg.sc') and q.evaluate("QT") == 'y' and 'Kechirasan' not in q.inner_text('#app'))
    q.evaluate("()=>{tab='s';render()}"); q.wait_for_timeout(100); chk('friends build: no Mushaf group in Settings', 'Mushaf' not in q.inner_text('#app'))
    q.evaluate("mfOpen(3)"); q.wait_for_timeout(400); chk('friends build: reader cannot be opened', not q.evaluate("!!document.getElementById('mf')"))
    chk('friends build downloads neither the Quran data nor the fonts', not any(('quran-mushaf' in u or '/fonts/' in u) for u in reqs), [u for u in reqs if 'quran' in u or 'fonts' in u])
    chk('friends build: no JavaScript errors', not e2, e2[:3]); b2.close()
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
