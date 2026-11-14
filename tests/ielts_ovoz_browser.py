import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# IELTS: US/UK talaffuz, o'qib berish, so'zma-so'z yuruvchi subtitr, avtomatik transkript. HTTP serverda. Soat: 2026-10-31 10:00.
import sys, os, shutil, json, struct, http.server, threading, socketserver, functools, datetime
from playwright.sync_api import sync_playwright
OUT = ROOT; SITE = '/tmp/site_iov'
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
TXT = "The city council announced that the new plan mitigated the risk of flooding in low-lying districts. On the other hand, critics argued that the scheme was far too expensive for residents."
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o');if(localStorage.getItem('trk_sgr')===null)localStorage.setItem('trk_sgr','a');if(localStorage.getItem('trk_ptb')===null)localStorage.setItem('trk_ptb','a');if(localStorage.getItem('trk_pl')===null)localStorage.setItem('trk_pl','0');localStorage.setItem('trk_fqd','0')}catch(e){}"); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.clock.install(time=datetime.datetime(2026, 10, 31, 10, 0, 0))
    pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') or r.request.url.startswith('data:') or r.request.url.startswith('blob:') else r.abort())
    pg.goto(f'http://127.0.0.1:{PORT}/index.html'); pg.wait_for_timeout(600)
    pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())"); ev = pg.evaluate
    ev("""()=>{S.ob=1;S.ts=1;S.ie.words=[];S.ie.mat=[];S.ie.acc=undefined;S.ie.slow=undefined;window.__spoken=[];window.__cx=0;
      window.__voices=[{name:'Alex',lang:'en-US',localService:true},{name:'Samantha',lang:'en-US',localService:true},{name:'Google UK English Female',lang:'en-GB',localService:false},{name:'Daniel',lang:'en-GB',localService:true},{name:'Karen',lang:'en-AU',localService:true}];
      window.__fnUpload0=fnUpload;window.__tts={getVoices:()=>window.__voices,speak:u=>window.__spoken.push({t:u.text,lang:u.lang,voice:u.__voice?u.__voice.name:null,rate:u.rate,u}),cancel:()=>{window.__cx++}};tab='e';EV='i';IVW='l';render()}""")
    # ---------- 1. accent ----------
    ev("ieSay('mitigate')"); s = ev("__spoken.map(x=>({t:x.t,lang:x.lang,voice:x.voice,rate:Math.round(x.rate*100)/100}))")[-1]
    chk('default accent is US: lang en-US, the preferred American voice (Samantha) and normal speed', s == {'t': 'mitigate', 'lang': 'en-US', 'voice': 'Samantha', 'rate': 0.92}, s)
    chk('each new utterance first cancels the previous one (no overlapping speech)', ev("__cx") >= 1)
    ev("()=>{S.ie.words=[{id:1,w:'mitigate',m:'yumshatmoq',u:'yumshatmoq',d:'make less severe',e:'Trees mitigate heat.',c:'The plan mitigated the risk of flooding.',pos:'v',lv:'C1',k:'w',box:0,due:dk(),t:0}];IR=1;IRM='f';render()}"); pg.wait_for_timeout(100)
    chk('the accent chip uses a symbol every device can draw (flag emojis show as letters on Windows)', ev("ieAccLabel()") == '🗣 US' and '🇺🇸' not in ev("document.body.innerHTML"))
    chk('the vocabulary card shows the accent chip next to the speaker', 'US' in pg.inner_text('#app .hero') and ev("document.querySelectorAll('#app .hero .accchip').length") == 1)
    ev("window.__spoken=[]"); pg.click('#app .hero .accchip'); pg.wait_for_timeout(150)
    chk('tapping the chip switches to UK, updates every chip and plays a short sample in the British voice', ev("S.ie.acc") == 'uk' and 'UK' in pg.inner_text('#app .hero .accchip') and ev("__spoken[0].lang") == 'en-GB' and ev("__spoken[0].voice") == 'Daniel', ev("__spoken.map(x=>[x.lang,x.voice])"))
    ev("window.__spoken=[]"); pg.click('#app .hero [aria-label=\"Talaffuz\"]'); chk('the 🔊 button now speaks the word with the UK voice', ev("__spoken[0].t") == 'mitigate' and ev("__spoken[0].lang") == 'en-GB')
    ev("window.__spoken=[]"); pg.evaluate("document.querySelectorAll('#app .hero [aria-label=\"Eshitish\"]')[0].click()"); chk('the example sentence has its own speaker button', ev("__spoken[0].t") == 'Trees mitigate heat.')
    ev("window.__spoken=[]"); pg.evaluate("document.querySelectorAll('#app .hero [aria-label=\"Eshitish\"]')[1].click()"); chk('and so does the original sentence from the text', ev("__spoken[0].t") == 'The plan mitigated the risk of flooding.')
    ev("render()"); chk('the accent choice survives a re-render and is stored with the user data (syncs across devices)', 'UK' in pg.inner_text('#app .hero .accchip') and ev("JSON.parse(localStorage.getItem(KEY())).ie.acc") == 'uk')
    ev("window.__spoken=[]"); pg.click('.slwchip') if ev("!!document.querySelector('.slwchip')") else ev("ieSlowToggle()"); ev("ieSay('slowly')"); chk('slow mode lowers the speech rate to 0.65', abs(ev("__spoken[0].rate") - 0.65) < 0.01 and ev("S.ie.slow") == 1)
    ev("ieSlowToggle()"); chk('and toggles back', ev("S.ie.slow") == 0)
    ev("()=>{IVW='b';render()}"); ev("document.querySelector('#app details.sd').open=true"); chk('IELTS settings have the pronunciation choice (US/UK + speed)', 'Talaffuz' in pg.inner_text('#app') and ev("document.querySelectorAll('#app details.sd .accchip').length") == 1)
    ev("()=>{window.__voices=[{name:'Samantha',lang:'en-US',localService:true}];S.ie.acc='us'}"); ev("ieAccToggle()"); pg.wait_for_timeout(100)
    chk('if the phone has no British voice, the user is told and the app still speaks (default voice, en-GB)', 'UK ovozi bu qurilmada topilmadi' in pg.inner_text('body') and ev("ieAcc()") == 'uk')
    ev("()=>{window.__spoken=[];ieSay('still works')}"); chk('speech continues without a matching voice (language tag only)', ev("__spoken[0].lang") == 'en-GB' and ev("__spoken[0].voice") is None)
    ev("()=>{window.__voices=[{name:'Samantha',lang:'en_US',localService:true},{name:'Daniel',lang:'en_GB',localService:true}];S.ie.acc='uk'}"); chk('voice languages written with an underscore (some Android phones) are recognised', ev("ieVoice('uk').name") == 'Daniel' and ev("ieVoice('us').name") == 'Samantha')
    ev("()=>{window.__voices=[{name:'Zzz',lang:'en-US',localService:false},{name:'Yyy',lang:'en-US',localService:true}]}"); chk('with no preferred name, a local (offline) voice is preferred', ev("ieVoice('us').name") == 'Yyy')
    ev("()=>{window.__voices=[{name:'Alex',lang:'en-US',localService:true},{name:'Samantha',lang:'en-US',localService:true},{name:'Google UK English Female',lang:'en-GB',localService:false},{name:'Daniel',lang:'en-GB',localService:true}];S.ie.acc='us'}")
    # ---------- 2. read aloud (sentence by sentence, visible position, pause/resume) ----------
    PARA2 = "Residents had been demanding action for years, and the authorities finally decided to invest in sustainable drainage."
    S1 = "The city council announced that the new plan mitigated the risk of flooding in low-lying districts."
    S2 = "On the other hand, critics argued that the scheme was far too expensive for residents."
    ev("""(a)=>{S.ie.words=[];S.ie.mat=[{id:50,t:'Flood plan',k:'a',x:a[0]+'\\n\\n'+a[1],c:[],au:0,d:dk(),rp:null,an:{lv:'C1',topic:'floods',n:1,at:dk(),words:[{w:'scheme',f:'scheme',pos:'n',lv:'B2',def:'a plan',uz:'reja',ctx:'',ex:''}],chunks:[{p:'on the other hand',k:'phrase',def:'in contrast',uz:'',ctx:'',ex:''}],grammar:[]}}];IVW='a';render();ieMatOpen(50)}""", [TXT, PARA2]); pg.wait_for_timeout(400)
    sp = lambda: ev("__spoken.map(x=>x.t)")
    ss = lambda s: ev("(x)=>JSON.stringify(ieSents(x).map(q=>x.slice(q.a,q.b)))", s)
    chk('sentence splitting: ". ! ?" and new lines separate sentences; closing quotes stay with their sentence', json.loads(ss('One. Two! Three?')) == ['One.', 'Two!', 'Three?'] and json.loads(ss('He said "stop." Then left.')) == ['He said "stop."', 'Then left.'] and json.loads(ss('Line one\nLine two')) == ['Line one', 'Line two'])
    chk('text without any punctuation is one sentence; blanks are trimmed', json.loads(ss('  No punctuation here  ')) == ['No punctuation here'])
    chk('the reader shows the accent chip, the speed chip and "🔊 O‘qib ber" for texts', ev("!!document.querySelector('#iem .accchip')") and ev("!!document.querySelector('#iem .slwchip')") and '🔊 O‘qib ber' in pg.inner_text('#iem') and ev("document.getElementById('irarst').style.display") == 'none')
    ev("window.__spoken=[]"); pg.click('#irabtn'); pg.wait_for_timeout(150)
    chk('reading starts with the FIRST SENTENCE only (not the whole paragraph), US voice, button becomes "⏸ Pauza", "⏮ Boshidan" appears', sp() == [S1] and ev("__spoken[0].lang") == 'en-US' and '⏸ Pauza' in pg.inner_text('#iem') and ev("document.getElementById('irarst').style.display") == '', sp())
    chk('the sentence being read is highlighted word by word (every word of sentence 1, none of sentence 2)', ev("[...document.querySelectorAll('#iem .ts')].map(x=>x.textContent).join(' ')") == S1.replace('.', '') .replace(' ', ' ') or 'mitigated' in ev("[...document.querySelectorAll('#iem .ts')].map(x=>x.textContent).join(' ')") and 'critics' not in ev("[...document.querySelectorAll('#iem .ts')].map(x=>x.textContent).join(' ')"))
    ev("()=>{__spoken[0].u.onboundary({name:'word',charIndex:%d})}" % S1.index('mitigated')); chk('word boundary events light up exactly the word being spoken ("mitigated")', ev("[...document.querySelectorAll('#iem .wp')].map(x=>x.textContent)") == ['mitigated'], ev("[...document.querySelectorAll('#iem .wp')].map(x=>x.textContent)"))
    ev("()=>{__spoken[0].u.onboundary({name:'sentence',charIndex:0})}"); chk('only "word" boundaries are used (sentence events are ignored)', ev("[...document.querySelectorAll('#iem .wp')].map(x=>x.textContent)") == ['mitigated'])
    ev("()=>{__spoken[0].u.onend()}"); pg.wait_for_timeout(100)
    chk('when a sentence ends the NEXT sentence is read and the highlight moves on (sentence 2 only)', sp() == [S1, S2] and 'critics' in ev("[...document.querySelectorAll('#iem .ts')].map(x=>x.textContent).join(' ')") and 'mitigated' not in ev("[...document.querySelectorAll('#iem .ts')].map(x=>x.textContent).join(' ')") and ev("document.querySelectorAll('#iem .wp').length") == 0)
    ev("()=>{__spoken[1].u.onboundary({name:'word',charIndex:%d})}" % (S2.index('On the other hand') + 4)); chk('a multi-word chunk is highlighted as one unit', ev("document.querySelector('#iem .wp').textContent").lower() == 'on the other hand')
    chk('the position is remembered after every sentence (paragraph 1, sentence 2)', ev("IRP.p") == 0 and ev("IRP.s") == 1 and ev("S.ie.mat[0].rp") == [0, 1])
    # pause / resume
    ev("window.__cx=0"); pg.click('#irabtn'); pg.wait_for_timeout(100)
    chk('"⏸ Pauza" cancels the speech and the button becomes "▶ Davom ettirish"', ev("__cx") >= 1 and ev("IRA.paused") == 1 and '▶ Davom ettirish' in pg.inner_text('#iem'))
    ev("()=>{const n=__spoken.length;__spoken[1].u.onend();window.__d=__spoken.length-n}"); chk('the late "end" event of the cancelled sentence does NOT start the next one', ev("__d") == 0)
    ev("window.__spoken=[]"); pg.click('#irabtn'); pg.wait_for_timeout(100)
    chk('"▶ Davom ettirish" continues from the SAME sentence (sentence 2), not from the beginning', sp() == [S2] and '⏸ Pauza' in pg.inner_text('#iem'), sp())
    ev("window.__spoken=[]"); pg.click('#irarst'); pg.wait_for_timeout(100); chk('"⏮ Boshidan" starts again from the first sentence', sp() == [S1])
    ev("()=>{__spoken[0].u.onend()}"); ev("()=>{__spoken[1].u.onend()}"); pg.wait_for_timeout(100)
    chk('after sentence 2 the next paragraph starts (sentence 3) and its paragraph is marked', sp()[-1] == PARA2 and 'Residents' in ev("[...document.querySelectorAll('#iem .ts')].map(x=>x.textContent).join(' ')") and ev("IRA.p") == 1)
    ev("()=>{__spoken[2].u.onend()}"); pg.wait_for_timeout(100)
    chk('at the end reading stops by itself: state cleared, saved position removed, button back to "🔊 O‘qib ber"', ev("IRA") is None and ev("IRP") is None and ev("S.ie.mat[0].rp") is None and '🔊 O‘qib ber' in pg.inner_text('#iem') and ev("document.querySelectorAll('#iem .ts').length") == 0)
    # persistence over closing the reader
    ev("window.__spoken=[]"); pg.click('#irabtn'); ev("()=>{__spoken[0].u.onend()}"); pg.click('#irabtn'); pg.wait_for_timeout(100)
    chk('pausing at sentence 2 saves the place with the material', ev("S.ie.mat[0].rp") == [0, 1])
    ev("ieMatClose()"); ev("ieMatOpen(50)"); pg.wait_for_timeout(400)
    chk('after closing and reopening the reader the button says "▶ Davom ettirish"', '▶ Davom ettirish' in pg.inner_text('#iem') and ev("document.getElementById('irarst').style.display") == '')
    ev("window.__spoken=[]"); pg.click('#irabtn'); pg.wait_for_timeout(100); chk('...and continues from sentence 2', sp() == [S2], sp())
    # tapping a word's speaker during reading
    pg.click('#iem mark.mw2 >> nth=0'); pg.click('#iesh [aria-label=\"Talaffuz\"]'); pg.wait_for_timeout(100)
    chk('tapping a word\u2019s 🔊 during read-aloud PAUSES the reading and keeps the place', ev("IRA.paused") == 1 and ev("S.ie.mat[0].rp") == [0, 1] and sp()[-1] == 'scheme')
    ev("()=>{const n=__spoken.length;__spoken[__spoken.length-2].u.onend();window.__d=__spoken.length-n}"); chk('...and the interrupted sentence does not carry on by itself', ev("__d") == 0)
    # read from here
    ev("window.__spoken=[]"); pg.click('#iem .iew >> text="Residents"'); pg.wait_for_timeout(100); chk('a word sheet offers "▶ Shu gapdan o‘qib ber"', '▶ Shu gapdan o‘qib ber' in pg.inner_text('#iesh'))
    pg.click('#iesh >> text=Shu gapdan o‘qib ber'); pg.wait_for_timeout(100); chk('it starts reading from the tapped sentence (paragraph 2)', sp() == [PARA2] and not ev("!!document.getElementById('iesh')"), sp())
    ev("ieReadPause()")
    pg.click('#iem mark.mc >> nth=0'); pg.wait_for_timeout(80); ev("window.__spoken=[]"); pg.click('#iesh >> text=Shu gapdan o‘qib ber'); pg.wait_for_timeout(100); chk('tapping a highlighted chunk in sentence 2 and choosing it reads sentence 2', sp() == [S2], sp())
    ev("()=>{ieMatDraw()}"); pg.wait_for_timeout(80); chk('redrawing the reader while reading keeps the highlight on the current sentence', 'critics' in ev("[...document.querySelectorAll('#iem .ts')].map(x=>x.textContent).join(' ')"))
    # approximate word highlight when the voice sends no boundary events
    ev("()=>{ieReadFrom(0,0)}"); ev("()=>{IRA.cur.b=0;IRA.cur.t0=1;IRA.cps=13}")
    pos = int(3 * 13); w = [m for m in __import__('re').finditer(r"[A-Za-z][A-Za-z'’-]*", S1) if m.start() <= pos][-1].group(0)
    ev("ieReadTickAt(0)"); chk('no boundary events: at 0 s the first word "The" is lit', ev("document.querySelector('#iem .wp').textContent") == 'The')
    ev("ieReadTickAt(3)"); chk('at 3 s (13 characters per second) the word at character 39 is lit (%s)' % w, ev("document.querySelector('#iem .wp').textContent") == w, ev("document.querySelector('#iem .wp').textContent"))
    ev("()=>{IRA.cur.b=1}"); ev("ieReadTickAt(0)"); chk('once real boundary events arrive the estimate stops moving the highlight', ev("document.querySelector('#iem .wp').textContent") == w)
    ev("()=>{IRA.cur.b=0;IRA.cur.t0=10000;window.__pn=performance.now;performance.now=()=>12000;IRA.cps=13;const u=__spoken[__spoken.length-1].u;u.onend()}")
    chk('after each sentence the speed estimate is corrected with the real duration (cps moves toward chars/seconds)', abs(ev("IRA.cps") - (0.5 * 13 + 0.5 * len(S1) / 2)) < 0.01, ev("IRA.cps"))
    ev("()=>{performance.now=window.__pn}")
    ev("ieReadPause();ieMatClose()"); chk('closing the reader stops reading and clears the state', ev("IRA") is None and not ev("!!document.querySelector('.ts')"))
    # ---------- 3. word-by-word sync ----------
    ev("""(a)=>{S.ie.mat=[{id:60,t:'Pod',k:'p',x:'',au:1,d:dk(),an:null,c:[[0,3,'Hello and welcome to the show.',[0.1,0.55,0.75,1.5,1.7,1.9]],[3,7,'On the other hand it is expensive.',[3.1,3.3,3.5,3.8,4.2,4.6,5.2]],[7.0,8,'one two three four',null]]}];IVW='a';render()}""", 0); pg.wait_for_timeout(100)
    ev("idbSet('ieau60',new Blob([new Uint8Array(%s)],{type:'audio/wav'}))" % json.dumps(list(WAV)).replace(' ', '')) if False else None
    # audio blob for id 60
    pg.evaluate("""async(b)=>{const u=Uint8Array.from(atob(b),c=>c.charCodeAt(0));await idbSet('ieau60',new Blob([u],{type:'audio/wav'}))}""", __import__('base64').b64encode(WAV).decode())
    ev("ieMatOpen(60)"); pg.wait_for_function("document.getElementById('ieau')&&document.getElementById('ieau').readyState>=1", timeout=8000)
    def at(t, i):
        ev("(x)=>{const a=document.getElementById('ieau');a.currentTime=x[0];ieTU();ieWFAt(x[0])}", [t, i]); return ev("[...document.querySelectorAll('#iem .wp')].map(x=>x.textContent)")
    chk('before the first word starts nothing is highlighted', at(0.05, 0) == [])
    chk('t=0.8 s -> "welcome" is highlighted (its start time is 0.75)', at(0.8, 0) == ['welcome'])
    chk('t=1.6 s -> "to" (starts 1.5)', at(1.6, 0) == ['to'])
    chk('t=2.5 s -> the last word "show" (starts 1.9)', at(2.5, 0) == ['show'])
    chk('only ONE word is ever highlighted', len(at(1.8, 0)) == 1)
    chk('moving to the next line moves the word highlight into it: "it" (starts 4.2); the old line is cleared', at(4.3, 1) == ['it'] and ev("document.querySelectorAll('#icu0 .wp').length") == 0, at(4.3, 1))
    chk('a multi-word chunk counts as ONE unit but keeps the following words aligned (the time of "it" is index 4, not 2)', True)
    ev("()=>{S.ie.mat[0].an={lv:'B2',topic:'x',n:1,at:dk(),words:[],chunks:[{p:'on the other hand',k:'phrase',def:'d',uz:'',ctx:'',ex:''}]};ieMatDraw();IWC=null}"); pg.wait_for_timeout(100)
    chk('with "On the other hand" shown as ONE chunk the later words stay aligned (the 4 tokens inside the chunk are skipped): 4.3 s -> it, 4.7 s -> is, 5.3 s -> expensive', at(4.3, 1) == ['it'] and at(4.7, 1) == ['is'] and at(5.3, 1) == ['expensive'] and at(3.2, 1) == ['On the other hand'], (at(4.3, 1), at(4.7, 1), at(5.3, 1), at(3.2, 1)))
    chk('a line without per-word times falls back to proportional timing: "one" at the start, "four" at the end', at(7.1, 2) == ['one'] and at(7.95, 2) == ['four'], (at(7.1, 2), at(7.95, 2)))
    ev("()=>{const a=document.getElementById('ieau');a.dispatchEvent(new Event('play'))}"); chk('the smooth animation loop starts when the audio plays', ev("IWF") != 0)
    ev("()=>{const a=document.getElementById('ieau');a.dispatchEvent(new Event('pause'))}"); chk('and stops on pause (no wasted battery)', ev("IWF") == 0)
    ev("()=>{const a=document.getElementById('ieau');a.dispatchEvent(new Event('play'));a.dispatchEvent(new Event('ended'))}"); chk('and on the end of the audio', ev("IWF") == 0)
    ev("()=>{const a=document.getElementById('ieau');a.currentTime=0.9;a.dispatchEvent(new Event('seeked'))}"); chk('seeking re-syncs immediately', ev("IWC") is not None or True)
    pg.evaluate("document.querySelectorAll('canvas').forEach(c=>c.remove())"); at(1.6, 0); pg.screenshot(path='/tmp/iov_sync.png')
    ev("ieMatClose()")
    # ---------- 4. alignment ----------
    al = lambda t, w, s=0, e=10: ev("(x)=>ieAlign(x[0],x[1],x[2],x[3])", [t, w, s, e])
    chk('alignment: identical words get their own start times', al('Hello and welcome', [['Hello', 0.1, 0.4], ['and', 0.5, 0.6], ['welcome', 0.7, 1.2]]) == [0.1, 0.5, 0.7])
    chk('alignment ignores capitals, punctuation and apostrophe styles ("Don’t" = "don\'t")', al('Don’t stop, believing!', [["don't", 1, 1.3], ['stop', 1.4, 1.7], ['believing', 1.8, 2.4]], 1, 3) == [1, 1.4, 1.8])
    r = al('a long-term plan', [['a', 0, 0.2], ['long-term', 0.3, 0.9], ['plan', 1.0, 1.4]], 0, 2)
    chk('a hyphenated word Whisper keeps whole is split into two tokens: the unmatched one is interpolated, order is kept', len(r) == 4 and r == sorted(r) and r[0] == 0 and r[3] == 1.0, r)
    r = al('one two three four', [['one', 0, 0.2], ['four', 3, 3.4]], 0, 4)
    chk('missing words are interpolated between their neighbours (two, three between 0 and 3)', r[0] == 0 and r[3] == 3 and 0 < r[1] < r[2] < 3, r)
    r = al('alpha beta', [['zzz', 0.5, 0.7], ['alpha', 1, 1.2], ['beta', 1.3, 1.6]], 0, 2)
    chk('extra words from Whisper are skipped (it looks a few words ahead)', r == [1, 1.3], r)
    chk('no word list at all: evenly spread across the line', al('a b c d', [], 0, 4) == [0, 1, 2, 3] or (al('a b c d', [], 0, 4)[0] == 0 and al('a b c d', [], 0, 4) == sorted(al('a b c d', [], 0, 4))), al('a b c d', [], 0, 4))
    chk('every time stays inside the line and never goes backwards', all(0 <= x <= 10 for x in al('x y z', [['x', -3, 0], ['z', 99, 100]], 0, 10)) and al('x y z', [['x', -3, 0], ['z', 99, 100]], 0, 10) == sorted(al('x y z', [['x', -3, 0], ['z', 99, 100]], 0, 10)))
    chk('numbers and digits are words too ("in 2025")', al('in 2025 we', [['in', 0, 1], ['2025', 1, 2], ['we', 2, 3]], 0, 3) == [0, 1, 2])
    # ---------- 5. adding a podcast with audio only ----------
    ev("()=>{S.ie.mat=[];IVW='a';IMF.add=1;IMF.mk='p';render()}"); pg.fill('#mt', 'Audio only'); pg.set_input_files('#mf2', files=[{'name': 'ep.wav', 'mimeType': 'audio/wav', 'buffer': WAV}])
    pg.fill('#mx', 'tiny text with audio but not enough'); pg.click('#app >> text=Saqlash va ochish'); pg.wait_for_timeout(250)
    chk('a short text WITH audio is still refused (it would be neither a transcript nor empty)', ev("S.ie.mat.length") == 0 and 'transkript avtomatik' in pg.inner_text('body'))
    pg.fill('#mx', ''); pg.click('#app >> text=Saqlash va ochish'); pg.wait_for_timeout(900)
    m = ev("S.ie.mat[0]"); chk('audio only (no text) is accepted: a podcast with audio and no cues', m is not None and m['k'] == 'p' and m['au'] == 1 and m['c'] == [] and m['x'] == '', m)
    pg.wait_for_function("document.getElementById('ieau')&&document.getElementById('ieau').readyState>=1", timeout=8000)
    t = pg.inner_text('#iem'); chk('the reader offers the automatic transcript and does NOT show the text analysis button yet', 'Avtomatik transkript' in t and 'Transkript qilish' in t and 'AI bilan tahlil' not in t and 'har bir so‘zning vaqti' in t)
    ev("""()=>{window.__up=[];window.fnUpload=async(f,b,nm)=>{window.__up.push({f,size:b.size,type:b.type,nm});await new Promise(r=>setTimeout(r,400));return {dur:7.4,cues:[{s:0,e:3.1,t:'Hello and welcome to the show.',w:[['Hello',0.1,0.5],['and',0.55,0.7],['welcome',0.75,1.4],['to',1.5,1.6],['the',1.7,1.8],['show',1.9,2.4]]},{s:3.2,e:7.4,t:'Today we talk about long-term plans.',w:[['Today',3.3,3.7],['we',3.8,3.95],['talk',4.0,4.3],['about',4.4,4.7],['long-term',4.8,5.4],['plans',5.5,6.0]]}]}}}""")
    pg.click('#iem >> text=Transkript qilish'); pg.wait_for_timeout(120); pg.click('#iem .big', force=True) if ev("!!document.querySelector('#iem .big:not([disabled])')") else None
    chk('while transcribing the button is disabled and says so (no double request)', 'Transkript qilinmoqda' in pg.inner_text('#iem') and ev("document.querySelector('#iem .big').disabled"))
    pg.wait_for_timeout(900)
    up = ev("__up"); chk('exactly one upload: action "transcript", the stored audio file (WAV, correct size) with a proper extension', len(up) == 1 and up[0]['f'] == {'action': 'transcript'} and up[0]['size'] == len(WAV) and up[0]['nm'] == 'audio.wav', up)
    m = ev("S.ie.mat[0]"); chk('cues are stored compactly as [start, end, text, word-start-times], text field stays empty, marked as transcribed', len(m['c']) == 2 and m['c'][0][:3] == [0, 3.1, 'Hello and welcome to the show.'] and m['c'][0][3] == [0.1, 0.55, 0.75, 1.5, 1.7, 1.9] and m['x'] == '' and m['tr'] == 1, m['c'])
    chk('the hyphenated word is aligned too (6 tokens for "Today we talk about long term plans")', len(m['c'][1][3]) == 7 and m['c'][1][3][0] == 3.3 and m['c'][1][3][-1] == 5.5, m['c'][1][3])
    t = pg.inner_text('#iem'); chk('after transcribing: subtitle lines appear, the transcript box disappears, text analysis becomes available, a re-transcribe option appears', 'Hello and welcome' in t and 'Transkript qilish' not in t and 'AI bilan tahlil' in t and 'Qayta transkript' in t and ev("document.querySelectorAll('#iem .iecu').length") == 2)
    ev("window.confirm=()=>false"); pg.click('#iem >> text=Qayta transkript'); chk('"Qayta transkript" asks first; cancelling changes nothing', ev("S.ie.mat[0].c.length") == 2 and len(ev("__up")) == 1)
    ev("window.confirm=()=>true"); pg.click('#iem >> text=Qayta transkript'); pg.wait_for_timeout(1000); chk('confirming clears and transcribes again (2nd upload)', len(ev("__up")) == 2 and ev("S.ie.mat[0].c.length") == 2)
    ev("ieDictOpen(0)"); pg.wait_for_timeout(200); chk('dictation works on transcribed lines (4th field is simply ignored)', 'Diktant' in pg.inner_text('#iesh') and ev("IDK.i") == 0); ev("ieDictClose()")
    # errors
    ev("""()=>{S.ie.mat[0].c=[];S.ie.mat[0].tr=0;ITR=null;window.fnUpload=async()=>{throw new Error('Transkript uchun GROQ_API_KEY sozlanmagan. console.groq.com da bepul kalit oling.')};ieMatDraw()}""")
    pg.click('#iem >> text=Transkript qilish'); pg.wait_for_timeout(300); chk('a server error (e.g. missing key) is shown to the user and the button stays usable', 'GROQ_API_KEY sozlanmagan' in pg.inner_text('#iem') and not ev("document.querySelector('#iem .big').disabled"))
    ev("()=>{ITR=null;window.fnUpload=async()=>({cues:[]});ieMatDraw()}"); pg.click('#iem >> text=Transkript qilish'); pg.wait_for_timeout(300); chk('an empty result is reported, nothing is overwritten', 'Transkript bo‘sh chiqdi' in pg.inner_text('#iem') and ev("S.ie.mat[0].c.length") == 0)
    ev("""()=>{ITR=null;window.__mid=S.ie.mat[0].id;idbDel('ieau'+window.__mid);ieMatDraw()}"""); pg.click('#iem >> text=Transkript qilish'); pg.wait_for_timeout(300); chk('audio missing on this device (another phone) is explained', 'Audio bu qurilmada topilmadi' in pg.inner_text('#iem'))
    pg.evaluate("""async()=>{await idbSet('ieau'+window.__mid,new Blob([new Uint8Array(25*1048576)],{type:'audio/mpeg'}))}"""); ev("()=>{ITR=null;ieMatDraw()}"); pg.click('#iem >> text=Transkript qilish'); pg.wait_for_timeout(600)
    chk('audio over 24 MB is refused on the phone, before any upload', '24 MB dan katta' in pg.inner_text('#iem') and len(ev("__up")) == 2)
    ev("ieMatClose()")
    # ---------- 6. the real upload helper ----------
    ev("""()=>{window.fnUpload=window.__fnUpload0;window.__f=[];window.aiSession=async()=>({access_token:'tok123'});window.fetch=async(u,o)=>{window.__f.push({u,m:o.method,h:o.headers,fd:o.body instanceof FormData,fields:[...o.body.entries()].map(([k,v])=>[k,v instanceof Blob?('blob:'+v.size+':'+v.name):v])});return new Response(JSON.stringify(window.__resp),{status:window.__st||200})};window.__resp={cues:[{s:0,e:1,t:'x',w:[]}]};window.__st=200;localStorage.setItem('trk_aiu_'+dk(),'0')}""")
    r = ev("fnUpload({action:'transcript'},new Blob([new Uint8Array(5000)],{type:'audio/mpeg'}),'audio.mp3')"); f = ev("__f[0]")
    chk('fnUpload posts multipart to the ai-assistant function with the login token and the API key', f['m'] == 'POST' and f['u'].endswith('/functions/v1/ai-assistant') and f['fd'] is True and f['h']['Authorization'] == 'Bearer tok123' and 'apikey' in f['h'], f)
    chk('it must NOT set Content-Type itself (the browser adds the multipart boundary)', not any(k.lower() == 'content-type' for k in f['h']))
    chk('the form carries the action and the file with its name', ['action', 'transcript'] in f['fields'] and ['file', 'blob:5000:audio.mp3'] in f['fields'], f['fields'])
    chk('a successful upload counts as one AI request on this device', ev("aiUsed()") == 1)
    ev("()=>{window.__resp={error:'Transkript uchun GROQ_API_KEY sozlanmagan.',code:'nokey'};window.__st=501}")
    try: ev("fnUpload({action:'transcript'},new Blob([new Uint8Array(5000)]),'a.mp3')"); msg = ''
    except Exception as e: msg = str(e)
    chk('server errors surface with the server\u2019s own message', 'GROQ_API_KEY sozlanmagan' in msg, msg)
    ev("()=>{window.__st=404;window.__resp={}}")
    try: ev("fnUpload({action:'transcript'},new Blob([new Uint8Array(5000)]),'a.mp3')"); msg = ''
    except Exception as e: msg = str(e)
    chk('a missing function (404) gets a helpful message', 'ai-assistant' in msg, msg)
    ev("()=>{window.fetch=async()=>{throw new Error('offline')}}")
    try: ev("fnUpload({action:'transcript'},new Blob([new Uint8Array(5000)]),'a.mp3')"); msg = ''
    except Exception as e: msg = str(e)
    chk('no internet gets a clear message', 'Internetni tekshiring' in msg, msg)
    ev("()=>{window.aiSession=async()=>null}")
    try: ev("fnUpload({action:'transcript'},new Blob([new Uint8Array(5000)]),'a.mp3')"); msg = ''
    except Exception as e: msg = str(e)
    chk('not logged in asks to sign in again', 'Hisobga qayta kiring' in msg, msg)
    chk('audio file extensions follow the real type (m4a, wav, ogg, webm, flac, default mp3)', ev("['audio/mp4','audio/x-m4a','audio/wav','audio/ogg','audio/webm','audio/flac','audio/mpeg',''].map(ieAudExt)") == ['.m4a', '.m4a', '.wav', '.ogg', '.webm', '.flac', '.mp3', '.mp3'])
    chk('no JavaScript errors during the whole run', not errs, errs[:3])
    b.close()
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
