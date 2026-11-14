# IELTS o'qish: grammar ko'rinishi (regressiya), sahifa sakramasligi, audio joyini eslab qolish, belgilangan iboralarni izohlash. Soat: 2026-10-31 10:00.
import sys, os, shutil, json, struct, base64, http.server, threading, socketserver, functools, datetime
from playwright.sync_api import sync_playwright
OUT = '/mnt/user-data/outputs'; SITE = '/tmp/site_ioq'
shutil.rmtree(SITE, ignore_errors=True); os.makedirs(SITE)
[shutil.copy(os.path.join(OUT, 'tracker', f), SITE) for f in os.listdir(OUT + '/tracker') if os.path.isfile(os.path.join(OUT, 'tracker', f))]
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def handle(self):
        try: super().handle()
        except (BrokenPipeError, ConnectionResetError): pass
srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(H, directory=SITE)); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
sr = 8000; n = sr * 8
WAV = b'RIFF' + struct.pack('<I', 36 + n) + b'WAVEfmt ' + struct.pack('<IHHIIHH', 16, 1, 1, sr, sr, 1, 8) + b'data' + struct.pack('<I', n) + bytes([128]) * n
ok = bad = 0
def chk(name, cond, extra=''):
    global ok, bad
    if cond: ok += 1; print('PASS', name)
    else: bad += 1; print('FAIL', name, extra)
TXT = ("If the council had acted earlier, the city would have avoided the worst flooding. The plan mitigated the risk of flooding in low-lying districts, although critics argued that the scheme was far too expensive. "
       "Residents, who had been waiting for years, were reluctant to accept higher taxes.")
P2 = "Experts say the project will significantly reduce long-term damage across the whole region over the next decade."
AN = {'level': 'B2', 'topic': 'floods', 'lv': 'B2', 'n': 1, 'at': '2026-10-31',
      'words': [{'w': 'avoid', 'f': 'avoided', 'pos': 'v', 'lv': 'B2', 'def': 'keep away', 'uz': 'qochmoq', 'ctx': '', 'ex': ''}, {'w': 'scheme', 'f': 'scheme', 'pos': 'n', 'lv': 'B2', 'def': 'plan', 'uz': 'reja', 'ctx': '', 'ex': ''}],
      'chunks': [], 'grammar': [{'p': 'If the council had acted earlier, the city would have avoided', 'g': 'Third conditional', 'lv': 'C1', 'def': 'If + past perfect, would have + V3', 'uz': 'Shart', 'ctx': '', 'ex': 'If I had known, I would have come.'},
                                 {'p': 'who had been waiting for years', 'g': 'Past perfect continuous', 'lv': 'B2', 'def': 'had been + V-ing', 'uz': '', 'ctx': '', 'ex': ''}]}
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o')}catch(e){}"); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.clock.install(time=datetime.datetime(2026, 10, 31, 10, 0, 0))
    pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') or r.request.url.startswith('data:') or r.request.url.startswith('blob:') else r.abort())
    pg.goto(f'http://127.0.0.1:{PORT}/index.html'); pg.wait_for_timeout(600)
    pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())"); ev = pg.evaluate
    ev("""(x)=>{S.ob=1;S.ts=1;S.ie.words=[];window.__spoken=[];window.__voices=[{name:'Samantha',lang:'en-US',localService:true}];window.__tts={getVoices:()=>window.__voices,speak:u=>window.__spoken.push({t:u.text,lang:u.lang,u}),cancel:()=>{}};
      S.ie.mat=[{id:50,t:'Floods',k:'a',x:x[0]+'\\\\n\\\\n'+x[1],c:[],au:0,d:dk(),an:x[2]}];tab='e';EV='i';IVW='a';render();ieMatOpen(50)}""", [TXT, P2, AN]); pg.wait_for_timeout(400)
    # ---------- 1. grammar tint must not break the layout (regression of a real bug) ----------
    st = ev("""()=>{const e=document.querySelector('#iem .iew.gtx'),c=getComputedStyle(e);return {n:document.querySelectorAll('#iem .iew.gtx').length,display:c.display,border:c.borderTopWidth,bg:c.backgroundColor,h:e.getBoundingClientRect().height}}""")
    chk('words inside a grammar structure stay ordinary inline words (not boxed blocks)', st['n'] >= 12 and st['display'] == 'inline' and st['border'] == '0px' and st['h'] < 45, st)
    chk('...with a light purple tint', 'rgba' in st['bg'] and st['bg'] != 'rgba(0, 0, 0, 0)', st['bg'])
    chk('the text still flows as normal lines: the first paragraph is only a few lines tall (not one word per line)', ev("document.querySelector('#iem .iep').getBoundingClientRect().height") < 260, ev("document.querySelector('#iem .iep').getBoundingClientRect().height"))
    pg.evaluate("document.querySelectorAll('canvas').forEach(c=>c.remove())"); pg.screenshot(path='/tmp/ioq_grammar.png')
    # ---------- 2. redrawing must not scroll the page ----------
    cues = [[round(i * 0.4, 2), round(i * 0.4 + 0.4, 2), 'Line number %d of the long podcast transcript goes here for the scrolling test.' % i, None] for i in range(20)]
    ev("(a)=>{S.ie.mat=[{id:60,t:'Pod',k:'p',x:'',c:a[0],au:1,d:dk(),an:a[1]}];ieMatClose();IVW='a';render()}", [cues, AN]); pg.evaluate("""async(b)=>{const u=Uint8Array.from(atob(b),c=>c.charCodeAt(0));await idbSet('ieau60',new Blob([u],{type:'audio/wav'}))}""", base64.b64encode(WAV).decode())
    ev("ieMatOpen(60)"); pg.wait_for_function("document.getElementById('ieau')&&document.getElementById('ieau').readyState>=1", timeout=8000)
    ev("()=>{const a=document.getElementById('ieau');a.currentTime=7;ieTU();IMSEL={_o:1};ieMatDraw()}"); pg.wait_for_timeout(300)
    ev("()=>{document.getElementById('iemb').scrollTop=0}"); pg.wait_for_timeout(100)
    ev("()=>{const b=document.getElementById('iemb');b.scrollTop=260;window.__s0=b.scrollTop}"); s0 = ev("__s0")
    pg.click('#iem >> text=Hammasini belgilash'); pg.wait_for_timeout(500)
    chk('"Hammasini belgilash" does NOT scroll the page (the active subtitle line used to pull it down)', abs(ev("document.getElementById('iemb').scrollTop") - s0) <= 2 and s0 > 100, (s0, ev("document.getElementById('iemb').scrollTop")))
    ev("()=>{document.getElementById('iemb').scrollTop=s0}".replace('s0', str(s0))); pg.click('#iem >> text=Tozalash'); pg.wait_for_timeout(400)
    chk('neither does "Tozalash"', abs(ev("document.getElementById('iemb').scrollTop") - s0) <= 2)
    chk('after the redraw the audio\u2019s current line is still marked (just not scrolled to)', ev("document.querySelectorAll('#iem .iecu.on').length") == 1 and ev("document.querySelector('#iem .iecu.on').id") == 'icu17')
    ev("()=>{document.getElementById('iemb').scrollTop=0}"); pg.wait_for_timeout(100)
    ev("ieCueGo(19)"); pg.wait_for_timeout(1500)
    r = ev("(()=>{const r=document.getElementById('icu19').getBoundingClientRect();return [r.top,r.bottom,innerHeight]})()")
    chk('tapping a subtitle line (an explicit seek) DOES bring that line into view', r[0] >= 0 and r[1] <= r[2], r)
    ev("document.getElementById('ieau').pause()")
    # ---------- 3. the audio remembers where you stopped ----------
    ev("()=>{const a=document.getElementById('ieau');a.currentTime=5;a.dispatchEvent(new Event('pause'))}"); chk('pausing stores the position with the material', ev("S.ie.mat[0].pos") == 5)
    ev("ieMatClose()"); chk('closing the reader also keeps it', ev("S.ie.mat[0].pos") == 5)
    ev("ieMatOpen(60)"); pg.wait_for_function("document.getElementById('ieau')&&document.getElementById('ieau').readyState>=1", timeout=8000); pg.wait_for_timeout(300)
    chk('reopening continues from 0:05 (not from the start) and says so', abs(ev("document.getElementById('ieau').currentTime") - 5) < 0.3 and 'Davom ettirildi: 0:05' in pg.inner_text('body'), ev("document.getElementById('ieau').currentTime"))
    ev("ieMatClose()"); ev("S.ie.mat[0].pos=7.6"); ev("ieMatOpen(60)"); pg.wait_for_function("document.getElementById('ieau')&&document.getElementById('ieau').readyState>=1", timeout=8000); pg.wait_for_timeout(300)
    chk('a saved position within the last 2 seconds is ignored (start from the beginning)', ev("document.getElementById('ieau').currentTime") < 0.3)
    ev("()=>{document.getElementById('ieau').dispatchEvent(new Event('ended'))}"); chk('finishing the audio resets the saved position', ev("S.ie.mat[0].pos") == 0)
    ev("ieMatClose()")
    # ---------- 4. selecting 2-3 words (a phrase) ----------
    ev("""()=>{S.ie.words=[];window.__calls=[];window.fnAI=async(b)=>{window.__calls.push(b);return {text:JSON.stringify({w:'far too expensive',pos:'',lv:'B2',def:'much more costly than is reasonable',uz:'juda qimmat',ex:'The car is far too expensive.'})}};ieSay=t=>window.__spoken.push({t,ph:1});
      window.__sel=(pi,from,to)=>{const p=[...document.querySelectorAll('#iem .iep')][pi],w=document.createTreeWalker(p,NodeFilter.SHOW_TEXT);let nd,c=0,sN,sO,eN,eO;while((nd=w.nextNode())){const l=nd.textContent.length;if(sN===undefined&&from<c+l){sN=nd;sO=from-c}if(to<=c+l){eN=nd;eO=to-c;break}c+=l}const r=document.createRange();r.setStart(sN,sO);r.setEnd(eN,eO);const s=getSelection();s.removeAllRanges();s.addRange(r);ieSelUpdate()};
      S.ie.mat=[{id:70,t:'Floods',k:'a',x:%s,c:[],au:0,d:dk(),an:null}];ieMatOpen(70)}""" % json.dumps(TXT + '\n\n' + P2)); pg.wait_for_timeout(400)
    i0 = TXT.index('far too expensive')
    ev("(a)=>__sel(0,a[0],a[1])", [i0, i0 + len('far too expensive')]); pg.wait_for_timeout(100)
    chk('selecting three words shows a small bar with the phrase and the buttons ✨ Ma’nosi, 🔊, ➕', ev("!!document.getElementById('iesel')") and '“far too expensive”' in pg.inner_text('#iesel') and 'Ma’nosi' in pg.inner_text('#iesel') and ev("document.querySelectorAll('#iesel button').length") == 3, pg.inner_text('#iem')[:200])
    chk('the bar sits above the bottom and does not cover the text start', ev("parseInt(document.getElementById('iesel').style.bottom)") >= 8)
    ev("window.__spoken=[]"); pg.click('#iesel [aria-label="Eshitish"]'); chk('🔊 speaks the selected phrase', ev("__spoken[0].t") == 'far too expensive')
    pg.click('#iesel >> text=Ma’nosi'); pg.wait_for_timeout(400)
    c = ev("__calls"); chk('"Ma’nosi" asks the AI at once (no extra tap): mode define, the phrase and the SENTENCE it comes from', len(c) == 1 and c[0]['mode'] == 'define' and c[0]['word'] == 'far too expensive' and c[0]['ctx'].startswith('The plan mitigated') and c[0]['ctx'].endswith('too expensive.'), c)
    t = pg.inner_text('#iesh'); chk('the card shows the phrase, the Uzbek meaning, the definition and the example', 'far too expensive' in t and 'juda qimmat' in t and 'much more costly' in t and 'The car is far too expensive.' in t and 'Lug‘atga qo‘shish' in t, t)
    chk('the bar and the selection are gone once the card opens', not ev("!!document.getElementById('iesel')") and ev("getSelection().isCollapsed") is True)
    pg.click('#iesh >> text=Lug‘atga qo‘shish'); pg.wait_for_timeout(150)
    w = ev("S.ie.words.find(x=>x.w==='far too expensive')"); chk('a multi-word selection is saved as a CHUNK (k=c) with the meaning, definition, example, sentence and level', w and w['k'] == 'c' and w['u'] == 'juda qimmat' and w['d'].startswith('much more') and w['e'].startswith('The car') and w['c'].endswith('too expensive.') and w['lv'] == 'B2' and w['src'] == 70, w)
    ev("ieSheetClose()")
    j0 = TXT.index('city council') if 'city council' in TXT else TXT.index('the city')
    ev("(a)=>__sel(0,a[0],a[1])", [TXT.index('the council'), TXT.index('the council') + len('the council')]); pg.click('#iesel >> text=➕'); pg.wait_for_timeout(150)
    chk('➕ adds the selected two words at once as a chunk with its sentence (no meaning yet)', ev("S.ie.words.find(x=>x.w==='the council')&&S.ie.words.find(x=>x.w==='the council').k") == 'c' and ev("S.ie.words.find(x=>x.w==='the council').c").startswith('If the council') and not ev("!!document.getElementById('iesel')"))
    ev("(a)=>__sel(0,a[0],a[1])", [TXT.index('the council'), TXT.index('the council') + len('the council')]); pg.click('#iesel >> text=➕'); pg.wait_for_timeout(100)
    chk('adding the same phrase twice is refused with a message', 'Bu lug‘atda bor' in pg.inner_text('body') and len([x for x in ev("S.ie.words") if x['w'] == 'the council']) == 1)
    ev("(a)=>__sel(0,a[0],a[1])", [TXT.index('mitigated'), TXT.index('mitigated') + 9]); pg.click('#iesel >> text=➕'); pg.wait_for_timeout(100)
    chk('one selected word is saved as a normal word (k=w)', ev("S.ie.words.find(x=>x.w==='mitigated').k") == 'w')
    ev("(a)=>__sel(0,a[0],a[1])", [0, len('If the council had acted earlier, the city would')]); pg.wait_for_timeout(50)
    chk('a selection of 9+ words shows no bar (the limit is 8 words)', not ev("!!document.getElementById('iesel')"))
    ev("(a)=>__sel(0,a[0],a[1])", [i0, i0 + 4]); chk('a selection that is a single word still works', ev("!!document.getElementById('iesel')"))
    ev("(a)=>__sel(0,a[0],a[1])", [10, 11]); chk('a 1-character selection is ignored', not ev("!!document.getElementById('iesel')"))
    ev("()=>{const a=[...document.querySelectorAll('#iem .iep')],r=document.createRange();r.setStart(a[0].firstChild||a[0],0);r.setEnd(a[1],2);const s=getSelection();s.removeAllRanges();s.addRange(r);ieSelUpdate()}"); chk('a selection running across two paragraphs is ignored', not ev("!!document.getElementById('iesel')"))
    ev("(a)=>__sel(0,a[0],a[1])", [i0, i0 + 17]); ev("()=>{getSelection().removeAllRanges();ieSelUpdate()}"); chk('clearing the selection removes the bar', not ev("!!document.getElementById('iesel')"))
    ev("(a)=>__sel(0,a[0],a[1])", [i0, i0 + 17])
    ev("()=>{window.__tapped=0;const w=document.querySelector('#iem .iew');const before=!!document.getElementById('iesh');ieTap({target:w});window.__tapped=(!before&&!!document.getElementById('iesh'))?1:0}"); chk('the click that ends a text selection does NOT open the single-word card', ev("__tapped") == 0)
    ev("()=>{getSelection().removeAllRanges();ieSelUpdate()}"); pg.click('#iem .iew >> text="plan"'); pg.wait_for_timeout(100); chk('an ordinary tap on a word (no selection) still opens its card', ev("!!document.getElementById('iesh')")); ev("ieSheetClose()")
    # AI failure
    ev("()=>{window.fnAI=async()=>{throw new Error('Bugungi limit tugadi (40 ta so‘rov).')};S.ie.words=[];S.ie.mat.forEach(m=>{m.gl={}})}")
    ev("(a)=>__sel(0,a[0],a[1])", [i0, i0 + 17]); pg.click('#iesel >> text=Ma’nosi'); pg.wait_for_timeout(300); t = pg.inner_text('#iesh')
    chk('if the AI fails the card says why and still lets the user add the phrase without a meaning', 'Bugungi limit tugadi' in t and 'Faqat so‘zni qo‘sh' in t)
    pg.click('#iesh >> text=Faqat so‘zni qo‘sh'); pg.wait_for_timeout(100); chk('...as a chunk', ev("S.ie.words.find(x=>x.w==='far too expensive').k") == 'c')
    ev("(a)=>__sel(0,a[0],a[1])", [i0, i0 + 17]); ev("ieMatClose()"); chk('closing the reader removes a leftover selection bar', not ev("!!document.getElementById('iesel')"))
    chk('no JavaScript errors during the whole run', not errs, errs[:3])
    b.close()
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
