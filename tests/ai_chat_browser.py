# AI suhbat (klient): shlyuz xatosida qayta urinish, xabarlar, "Qayta yuborish" tugmasi, hisobot qatori. Tarmoq soxta fetch bilan almashtiriladi.
import sys
from playwright.sync_api import sync_playwright
ok = bad = 0
def chk(name, cond, extra=''):
    global ok, bad
    if cond: ok += 1; print('PASS', name)
    else: bad += 1; print('FAIL', name, extra)
STUB = """()=>{window.__calls=0;window.__seq=[];window.__retry=0;window.aiSession=async()=>({access_token:'t'});
  window.fetch=async(u,o)=>{window.__calls++;const s=window.__seq.shift()||{st:200,body:'Salom!'};if(s.delay)await new Promise(r=>setTimeout(r,s.delay));
    return new Response(s.body,{status:s.st,headers:{'content-type':s.json?'application/json':'text/plain','x-timing':s.tm||''}})}}"""
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o')}catch(e){}"); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route('**/*', lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
    pg.goto('file:///mnt/user-data/outputs/tracker/index.html'); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())")
    ev = pg.evaluate; ev("()=>{S.ob=1;S.ts=1}"); ev(STUB)
    run = lambda: ev("()=>aiStream([{r:'user',t:'salom'}],'',t=>{window.__txt=t},null,{onRetry:()=>{window.__retry++}}).then(r=>({ok:1,r}),e=>({ok:0,m:e.message}))")
    # 1. gateway 502 with an empty body, then success
    ev("window.__seq=[{st:502,body:''}]"); r = run()
    chk('502 with an empty body is retried once automatically and the answer arrives', r['ok'] == 1 and r['r'] == 'Salom!' and ev("__calls") == 2 and ev("__retry") == 1, r)
    # 2. 502 twice
    ev(STUB); ev("window.__seq=[{st:502,body:''},{st:502,body:''}]"); r = run()
    chk('two gateway errors in a row -> a friendly message (not the bare "Server xatosi"), exactly 2 requests', r['ok'] == 0 and 'AI serveri vaqtincha javob bermadi (502)' in r['m'] and ev("__calls") == 2, r)
    # 3. 503 with an HTML body
    ev(STUB); ev("window.__seq=[{st:503,body:'<html><body><h1>Bad Gateway</h1></body></html>'},{st:503,body:'<h1>Bad Gateway</h1>'}]"); r = run()
    chk('an HTML error page is shown as plain text (tags removed)', r['ok'] == 0 and 'Bad Gateway' in r['m'] and '<' not in r['m'], r)
    # 4. real JSON errors are not retried
    ev(STUB); ev("window.__seq=[{st:429,json:1,body:JSON.stringify({error:'Bugungi limit tugadi (40 ta so‘rov).'})}]"); r = run()
    chk('a JSON error from our server (limit) is shown as is and NOT retried', r['ok'] == 0 and 'Bugungi limit tugadi' in r['m'] and ev("__calls") == 1 and ev("__retry") == 0, r)
    ev(STUB); ev("window.__seq=[{st:502,json:1,body:JSON.stringify({error:'AI javob bera olmadi: x [a:http503; b:timeout9000]'})}]"); r = run()
    chk('a 502 that carries our own message is shown and not retried', r['ok'] == 0 and 'urinishlar' not in r['m'] and 'AI javob bera olmadi' in r['m'] and ev("__calls") == 1, r)
    # 5. timing line
    meta = 'auth=300,db=2000,gemini=1000,model=gemini-3.8-flash,think=minimal,att=3.8-flash-lite:timeout9000|3.8-flash:ok1000'
    tl = ev(f"aiTimingLine('{meta}',29700,31500)")
    chk('timing line reproduces the screenshot case and now explains it: retries + ~26 s of waiting outside the server', 'urinishlar: 3.8-flash-lite:timeout9000 → 3.8-flash:ok1000' in tl and 'tarmoq/kutish: 26.4 s' in tl and 'server 2.3 s' in tl and 'Gemini 1.0 s' in tl, tl)
    tl = ev("aiTimingLine('auth=100,db=200,gemini=900,model=gemini-3.8-flash,think=minimal,att=3.8-flash:ok900',1800,2300)")
    chk('a healthy request shows no retry or waiting notes', 'urinishlar' not in tl and 'tarmoq' not in tl and 'birinchi so‘z 1.8 s' in tl, tl)
    # 6. full chat flow with the retry button
    ev(STUB); ev("()=>{aiS().chat=[];aiBuild();aiRender();window.__seq=[{st:502,body:''},{st:502,body:''}];aiSend('Rejamni tuzib ber')}")
    pg.wait_for_timeout(300); txt = pg.inner_text('#aic')
    chk('while retrying, the waiting bubble says so', 'qayta urinyapman' in txt, txt[-120:])
    pg.wait_for_timeout(2600); txt = pg.inner_text('#aic')
    chk('after the failure: the friendly error and a "Qayta yuborish" button are shown', 'AI serveri vaqtincha javob bermadi' in txt and 'Qayta yuborish' in txt, txt[-200:])
    ev("window.__seq=[{st:200,body:'Mana rejang: 1) Bomdod...',tm:'auth=100,db=100,gemini=800,model=gemini-3.8-flash,think=minimal,att=3.8-flash:ok800'}]")
    pg.click('#aic >> text=Qayta yuborish'); pg.wait_for_timeout(700); txt = pg.inner_text('#aic')
    chk('clicking it resends the same question once and the answer replaces the error', 'Mana rejang' in txt and 'Qayta yuborish' not in txt and 'vaqtincha' not in txt and txt.count('Rejamni tuzib ber') == 1, txt[-300:])
    chk('the chat history has exactly one user message and one answer (no duplicates)', ev("aiS().chat.map(m=>m.r)") == ['user', 'model'], ev("aiS().chat.map(m=>m.r)"))
    chk('the answer carries the new timing note', 'birinchi so‘z' in pg.inner_text('#aic'))
    ev("()=>{aiS().chat=[{r:'user',t:'a'},{r:'err',t:'xato'},{r:'user',t:'b'},{r:'err',t:'xato2'}];aiRender()}")
    chk('only the LAST error has a retry button', pg.evaluate("document.querySelectorAll('#aic button[onclick=\"aiRetry()\"]').length") == 1)
    chk('no JavaScript errors during the whole run', not errs, errs[:3])
    b.close()
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
