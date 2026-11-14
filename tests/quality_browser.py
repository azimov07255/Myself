# Sifat: yangi versiya xabari (version.json, Yangilash, himoyalar) va egasi uchun xatolar paneli. HTTP serverda (version.json uchun).
import sys, os, shutil, json, http.server, threading, socketserver, functools
from playwright.sync_api import sync_playwright
OUT = '/mnt/user-data/outputs'; SITE = '/tmp/site_q'
shutil.rmtree(SITE, ignore_errors=True); os.makedirs(SITE)
[shutil.copy(os.path.join(OUT, 'tracker', f), SITE) for f in os.listdir(OUT + '/tracker') if os.path.isfile(os.path.join(OUT, 'tracker', f))]
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def handle(self):
        try: super().handle()
        except (BrokenPipeError, ConnectionResetError): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(H, directory=SITE)); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
LOCAL = json.load(open(SITE + '/version.json'))
def remote(v, b): open(SITE + '/version.json', 'w').write(json.dumps({'v': v, 'b': b}))
ok = bad = 0
def chk(name, cond, extra=''):
    global ok, bad
    if cond: ok += 1; print('PASS', name)
    else: bad += 1; print('FAIL', name, extra)
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o')}catch(e){}"); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') or r.request.url.startswith('data:') else r.abort())
    pg.goto(f'http://127.0.0.1:{PORT}/index.html'); pg.wait_for_timeout(600)
    pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())"); ev = pg.evaluate; ev("()=>{S.ob=1;S.ts=1;render()}")
    # ---------- A. version compare ----------
    vc = ev("[['2026.10.29-2','2026.10.29-1'],['2026.10.29-1','2026.10.29-1'],['2026.10.30-1','2026.10.29-9'],['2026.10.29-10','2026.10.29-9'],['2026.10.28-1','2026.10.29-1'],['2027.01.01-1','2026.12.31-5']].map(x=>verCmp(x[0],x[1]))")
    chk('version comparison is numeric (…-10 is newer than …-9, month/year roll over)', vc == [1, 0, 1, 1, -1, 1], vc)
    chk('the running app knows its version and build', ev("APP_VER") == LOCAL['v'] and ev("APP_BUILD") == LOCAL['b'])
    # ---------- B. update checks ----------
    ev("updCheck()"); pg.wait_for_timeout(500); chk('same version + same build -> no banner', not ev("!!document.getElementById('updb')") and ev("UPD") is None)
    remote('2099.01.01-1', 'zzzzzzzzzz'); ev("updCheck()"); pg.wait_for_timeout(500)
    chk('a newer version on the server shows the banner with the version number', ev("!!document.getElementById('updb')") and 'Yangi versiya tayyor (v2099.01.01-1)' in pg.inner_text('#updb') and 'Yangilash' in pg.inner_text('#updb'))
    pg.evaluate("document.querySelectorAll('canvas').forEach(c=>c.remove())"); pg.screenshot(path='/tmp/q_banner.png')
    remote(LOCAL['v'], 'aaaaaaaaaa'); ev("updCheck()"); pg.wait_for_timeout(500)
    chk('same version but a different build (hot-fix without a version bump) also counts as an update', ev("!!document.getElementById('updb')") and ev("UPD.b") == 'aaaaaaaaaa')
    remote('2000.01.01-1', 'bbbbbbbbbb'); ev("updCheck()"); pg.wait_for_timeout(500)
    chk('an OLDER version on the server (rollback / slow CDN) is ignored and removes the banner', not ev("!!document.getElementById('updb')") and ev("UPD") is None)
    remote(LOCAL['v'], LOCAL['b']); ev("updCheck()"); pg.wait_for_timeout(300); chk('back to equal -> no banner', not ev("!!document.getElementById('updb')"))
    # ---------- C. dismiss ----------
    remote('2099.01.01-1', 'zzzzzzzzzz'); ev("updCheck()"); pg.wait_for_timeout(400); pg.click('#updb .x'); pg.wait_for_timeout(100)
    chk('"✕" hides the banner', not ev("!!document.getElementById('updb')"))
    ev("updCheck()"); pg.wait_for_timeout(400); chk('and it stays hidden for the same version on the next check', not ev("!!document.getElementById('updb')"))
    remote('2099.01.02-1', 'yyyyyyyyyy'); ev("updCheck()"); pg.wait_for_timeout(400); chk('but a newer release shows it again', ev("!!document.getElementById('updb')"))
    # ---------- D. updating ----------
    ev("""async()=>{window.__rl=0;window.__pushed=0;window.updReload=()=>{window.__rl++};window.push=async()=>{window.__pushed++};
        const c=await caches.open('trk-v2');await c.put('/index.html',new Response('old'));await c.put('/sw.js',new Response('old'));await c.put('/fonts/x.ttf',new Response('f'));await c.put('/data/q.json',new Response('d'));sessionStorage.removeItem('trk_updtry')}""")
    pg.click('#updb .btn'); pg.wait_for_timeout(1200)
    keys = ev("(async()=>{const c=await caches.open('trk-v2');return (await c.keys()).map(r=>new URL(r.url).pathname)})()")
    chk('"Yangilash" first sends the data to the server, then reloads', ev("__pushed") == 1 and ev("__rl") == 1)
    chk('it clears the app files from the cache but keeps the big Quran data and fonts', '/index.html' not in keys and '/sw.js' not in keys and '/fonts/x.ttf' in keys and '/data/q.json' in keys, keys)
    ev("window.__rl=0;window.__pushed=0;document.getElementById('updb')&&0"); ev("updShow()")
    ev("updGo()"); pg.wait_for_timeout(300)
    chk('pressing it again within 2 minutes does not reload again (no reload loop when the server still serves the old file)', ev("__rl") == 0 and ev("__pushed") == 0)
    ev("sessionStorage.removeItem('trk_updtry')"); remote(LOCAL['v'], LOCAL['b']); ev("updCheck()"); pg.wait_for_timeout(300)
    chk('once the app is up to date the loop guard is cleared', ev("sessionStorage.getItem('trk_updtry')") is None)
    ev("""async()=>{window.push=async()=>{await new Promise(r=>setTimeout(r,10000))};}"""); remote('2099.01.03-1', 'qqqqqqqqqq'); ev("updCheck()"); pg.wait_for_timeout(400)
    el = ev("(async()=>{window.__rl=0;const t=Date.now();await updGo();return Date.now()-t})()")
    chk('a hanging upload cannot block the update for more than ~3.5 seconds (local data is already saved) [%d ms]' % el, ev("__rl") == 1 and 3000 <= el < 5500, el)
    # ---------- E. manual check in Diagnostika ----------
    remote(LOCAL['v'], LOCAL['b']); ev("window.push=undefined;delete window.push;UPDX=''")
    ev("updCheck(true)"); pg.wait_for_timeout(500); chk('manual check: up to date message', 'Eng so‘nggi versiya o‘rnatilgan' in ev("UPDMSG"), ev("UPDMSG"))
    remote('2099.02.02-1', 'mmmmmmmmmm'); ev("updCheck(true)"); pg.wait_for_timeout(500); chk('manual check: says a new version exists', 'Yangi versiya bor: v2099.02.02-1' in ev("UPDMSG"))
    ev("()=>{const f=window.fetch;window.fetch=()=>Promise.reject(new Error('offline'));window.__f=f}"); ev("updCheck(true)"); pg.wait_for_timeout(300)
    chk('manual check while offline: clear message, no banner change, no crash', 'Tekshirib bo‘lmadi' in ev("UPDMSG")); ev("window.fetch=window.__f")
    chk('Diagnostika shows version with build id and the check button', ev("diagText()").split('\n')[0] == 'Versiya: %s (%s)' % (LOCAL['v'], LOCAL['b']) and 'Yangilanishni tekshirish' in ev("diagCard()"))
    remote(LOCAL['v'], LOCAL['b']); ev("updCheck()"); pg.wait_for_timeout(300)
    # ---------- F. owner error panel ----------
    ev("""()=>{UID='owner1';OW=[];lsSet('trk_errseen_owner1','');const d=(n,h)=>new Date(Date.now()-n*36e5*h).toISOString();
      ERRL=[{id:1,user_id:'a',ver:'2026.10.20-1',tab:'h',msg:'Timeout after 5000 ms',stack:'at f (app.js:1)',standalone:true,created_at:d(1,24)},
            {id:2,user_id:'b',ver:'2026.10.20-1',tab:'q:y',msg:'Timeout after 7000 ms',stack:'',standalone:false,created_at:d(2,24)},
            {id:3,user_id:'a',ver:'2026.10.20-1',tab:'h',msg:'Timeout after 91 ms',stack:'',standalone:true,created_at:d(3,24)},
            {id:4,user_id:'c',ver:APP_VER,tab:'e:i',msg:'Cannot read properties of undefined (reading "x1")',stack:'at g (app.js:9)',standalone:true,created_at:d(1,2)},
            {id:5,user_id:'c',ver:APP_VER,tab:'e:i',msg:'Cannot read properties of undefined (reading "x1")',stack:'',standalone:true,created_at:d(1,3)},
            {id:6,user_id:'d',ver:'2026.09.01-1',tab:'o',msg:'<img src=x onerror=alert(1)> broke',stack:'',standalone:false,created_at:d(1,24*20)}];render()}""")
    G = ev("errGroups(ERRL,'',APP_VER).map(x=>({sig:x.sig,n:x.n,u:x.u,old:x.old,isNew:x.isNew}))")
    chk('similar messages are merged into one group (5000/7000/91 ms -> one "Timeout after # ms")', any(g['sig'] == 'Timeout after # ms' and g['n'] == 3 and g['u'] == 2 for g in G), G)
    chk('groups count users and versions', any(g['sig'].startswith('Cannot read') and g['n'] == 2 and g['u'] == 1 for g in G))
    chk('a group seen only in OLD versions is marked as probably fixed; one seen in the current version is not', next(g for g in G if g['sig'] == 'Timeout after # ms')['old'] is True and next(g for g in G if g['sig'].startswith('Cannot'))['old'] is False)
    chk('with nothing marked as seen, every group is "new"', all(g['isNew'] for g in G))
    card = ev("errCard()")
    chk('the card shows counts, users, versions, device split and the stack on demand', '3 marta · 2 kishi' in card and 'v2026.10.20-1×3' in card and '<details>' in card and 'ilova /' in card and 'yangi' in card, card[:300])
    chk('hostile text in an error message is escaped (no HTML injection into the owner panel)', '<img src=x' not in card and '&lt;img' in card)
    dg = ev("errDigest()")
    chk('the digest is a ready-to-share summary (7 days: 5 errors, 4... users, groups, current version)', 'Xatolar xulosasi' in dg and 'Jami: 5 ta xato' in dg and '3 foydalanuvchi' in dg and 'Joriy versiya: v' + LOCAL['v'] in dg and '1) ' in dg, dg)
    chk('the group title shows how many are new', ev("errBadge()") == ' (3 yangi)', ev("errBadge()"))
    ev("errSeenAll()"); pg.wait_for_timeout(100)
    chk('"Ko‘rildi" remembers the time: nothing is "new" afterwards, the badge disappears', ev("errBadge()") == '' and 'class="erb new"' not in ev("errCard()") and ev("lsGet('trk_errseen_owner1')") != '')
    ev("""()=>{ERRL.push({id:9,user_id:'z',ver:APP_VER,tab:'p',msg:'Brand new failure 42',stack:'',standalone:true,created_at:new Date(Date.now()+60000).toISOString()});render()}""")
    chk('a failure that first appears after the last "Ko‘rildi" is marked new again', ev("errBadge()") == ' (1 yangi)', ev("errBadge()"))
    ev("OW=null"); chk('a normal user (not the owner) sees nothing of this', ev("errCard()") == '' and ev("errBadge()") == '')
    ev("""()=>{OW=[];ERRL=null;window.__le=0;window.loadErrs=async()=>{window.__le++;ERRL=[]};window.fn=async()=>({users:[],stats:{}})}""")
    ev("loadOw()"); pg.wait_for_timeout(300); chk('errors are loaded automatically once when the owner data arrives', ev("__le") == 1)
    ev("loadOw()"); pg.wait_for_timeout(300); chk('...and not again on every refresh', ev("__le") == 1)
    chk('no JavaScript errors during the whole run', not errs, errs[:3])
    b.close()
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
