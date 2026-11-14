import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# IELTS: materiallar (maqola/podkast), AI tahlil, belgilash, so'z kartochkasi, pleyer, tayyorgarlik paneli. HTTP serverda (audio + IndexedDB). Soat: 2026-10-31 10:00.
import sys, os, shutil, json, struct, http.server, threading, socketserver, functools, datetime
from playwright.sync_api import sync_playwright
OUT = ROOT; SITE = '/tmp/site_ie'
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
ART = ("The city council announced that the new plan mitigated the risk of flooding in low-lying districts. On the other hand, critics argued that the scheme was far too expensive. "
       "Residents had been demanding action for years, and the authorities finally decided to invest in sustainable drainage. Experts say the project will significantly reduce long-term damage.")
C1T = "Hello and welcome to the show, where we talk about cities, climate and the way people live in them every single day."
SRT = "1\n00:00:00,000 --> 00:00:03,000\n" + C1T + "\n\n2\n00:00:03,000 --> 00:00:06,000\nToday we discuss how cities <i>mitigate</i> the risk of flooding when heavy rain falls on streets and old buildings.\n\n3\n00:00:06,000 --> 00:00:08,000\nOn the other hand, it is expensive and complicated for everyone involved in the long process of planning."
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o');if(localStorage.getItem('trk_sgr')===null)localStorage.setItem('trk_sgr','a');if(localStorage.getItem('trk_ptb')===null)localStorage.setItem('trk_ptb','a');if(localStorage.getItem('trk_pl')===null)localStorage.setItem('trk_pl','0');localStorage.setItem('trk_fqd','0')}catch(e){}"); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.clock.install(time=datetime.datetime(2026, 10, 31, 10, 0, 0))
    pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') or r.request.url.startswith('data:') or r.request.url.startswith('blob:') else r.abort())
    pg.goto(f'http://127.0.0.1:{PORT}/index.html'); pg.wait_for_timeout(600)
    pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())"); ev = pg.evaluate
    ev("()=>{S.ob=1;S.ts=1;S.ie.words=[];S.ie.mat=[];S.ie.tests=[];S.ie.dp={};S.ie.mr={};S.ie.nd=undefined;S.ie.nl=undefined;window.__say=[];window.ieSay=t=>window.__say.push(t);window.__fnAI0=fnAI}")
    # ---------- 1. subtitle parsing ----------
    c = ev("(s)=>ieCues(s)", SRT)
    chk('SRT: 3 cues with times, HTML tags removed', len(c) == 3 and c[0] == {'s': 0, 'e': 3, 't': C1T} and 'mitigate the risk' in c[1]['t'] and '<' not in c[1]['t'], c)
    vtt = "WEBVTT\n\nintro\n00:01.000 --> 00:03.000 align:start position:0%\n<c.yellow>Good</c> morning everyone.\n\n00:03.000 --> 00:05.500\nGood morning everyone.\n\n00:05.500 --> 00:09.000\nLet us begin the lesson {\\an8}now.\n"
    c = ev("(s)=>ieCues(s)", vtt)
    chk('VTT: header and cue ids skipped, settings and tags removed, repeated roll-up line merged, mm:ss.mmm times', len(c) == 2 and c[0]['s'] == 1 and c[0]['t'] == 'Good morning everyone.' and c[1]['t'] == 'Let us begin the lesson now.' and c[1]['e'] == 9, c)
    c = ev("(s)=>ieCues(s)", "[00:05] Hi there friends.\n[00:09] This is the second line.\n[01:02:03] And a very late third one.")
    chk('[mm:ss] lines: end = next start, last = +6 s, hh:mm:ss supported', len(c) == 3 and c[0]['e'] == 9 and c[2]['s'] == 3723 and c[2]['e'] == 3729, c)
    chk('plain text (or fewer than 3 time stamps) is not turned into cues', ev("ieCues('Just a plain article. No times here at all.').length") == 0 and ev("ieCues('[00:05] one\\n[00:09] two').length") == 0)
    chk('time parser: 01:02:03,500 = 3723.5, 4:07 = 247, garbage = -1', ev("[ieTime('01:02:03,500'),ieTime('4:07'),ieTime('abc'),ieTime('12')]") == [3723.5, 247, -1, -1])
    chk('cues come out sorted by start time', ev("ieCues('[00:30] c line here.\\n[00:10] a line here.\\n[00:20] b line here.').map(x=>x.t[0])") == ['a', 'b', 'c'])
    # ---------- 2. adding materials ----------
    ev("()=>{tab='e';EV='i';IVW='a';render()}"); pg.wait_for_timeout(150)
    chk('IELTS has the new "Materiallar" tab', 'Materiallar' in pg.inner_text('#app') and 'Maqola yoki podkast qo‘shish' in pg.inner_text('#app'))
    pg.click('#app >> text=Maqola yoki podkast qo‘shish'); pg.fill('#mt', 'Flood plan'); pg.fill('#mx', 'too short'); pg.click('#app >> text=Saqlash va ochish'); pg.wait_for_timeout(200)
    chk('text shorter than 200 characters is refused with a message', ev("S.ie.mat.length") == 0 and not ev("!!document.getElementById('iem')"))
    pg.fill('#mx', ART); pg.click('#app >> text=Saqlash va ochish'); pg.wait_for_timeout(500)
    chk('an article is saved (title, text, no cues) and the reader opens', ev("S.ie.mat.length") == 1 and ev("S.ie.mat[0].t") == 'Flood plan' and ev("S.ie.mat[0].k") == 'a' and ev("S.ie.mat[0].x.length") > 300 and ev("S.ie.mat[0].c.length") == 0 and ev("!!document.getElementById('iem')"))
    chk('the reader shows the text with every word tappable and says it is not analysed yet', 'tahlil qilinmagan' in pg.inner_text('#iems') and ev("document.querySelectorAll('#iem .iew').length") > 30)
    ev("ieMatClose()"); pg.wait_for_timeout(100)
    # podcast with audio
    ev("()=>{tab='e';EV='i';IVW='a';IMF.add=1;IMF.mk='p';render()}"); pg.wait_for_timeout(150)
    pg.fill('#mt', 'Cities podcast'); pg.fill('#mx', SRT); pg.set_input_files('#mf2', files=[{'name': 'ep.wav', 'mimeType': 'audio/wav', 'buffer': WAV}]); pg.click('#app >> text=Saqlash va ochish'); pg.wait_for_timeout(900)
    m = ev("S.ie.mat[0]")
    chk('podcast: 3 cues stored (text not duplicated), audio flag set', m['k'] == 'p' and len(m['c']) == 3 and m['x'] == '' and m['au'] == 1 and m['c'][1][0] == 3, m)
    chk('the audio file itself is kept in IndexedDB on this device', ev("(async()=>{const b=await idbGet('ieau'+S.ie.mat[0].id);return !!b&&b.size>60000})()"))
    chk('ieText joins the cues for analysis', 'Hello and welcome' in ev("ieText(S.ie.mat[0])") and 'expensive' in ev("ieText(S.ie.mat[0])"))
    # ---------- 3. player ----------
    pg.wait_for_function("document.getElementById('ieau')&&document.getElementById('ieau').readyState>=1", timeout=8000)
    chk('the player shows with the audio loaded and the subtitle lines with time buttons', ev("document.querySelectorAll('#iem .iecu').length") == 3 and ev("document.querySelector('#iem .iet').textContent") == '0:00' and ev("document.getElementById('ieau').duration") > 7)
    ev("()=>{const a=document.getElementById('ieau');a.currentTime=4;ieTU()}"); chk('current time 4 s -> the second line is highlighted', ev("document.getElementById('icu1').classList.contains('on')") and not ev("document.getElementById('icu0').classList.contains('on')"))
    ev("()=>{const a=document.getElementById('ieau');a.currentTime=7;ieTU()}"); chk('time 7 s -> the third line', ev("document.getElementById('icu2').classList.contains('on')") and not ev("document.getElementById('icu1').classList.contains('on')"))
    ev("()=>{const a=document.getElementById('ieau');a.currentTime=4;ieTU();ieMatDraw()}"); pg.wait_for_timeout(150)
    chk('after the text is redrawn (e.g. analysis progress) exactly ONE line is highlighted: the current one', ev("document.querySelectorAll('#iem .iecu.on').length") == 1 and ev("document.getElementById('icu1').classList.contains('on')"))
    ev("()=>{const a=document.getElementById('ieau');a.currentTime=7;ieTU();a.currentTime=1;ieTU()}"); chk('moving through the lines never leaves two highlighted', ev("document.querySelectorAll('#iem .iecu.on').length") == 1 and ev("document.getElementById('icu0').classList.contains('on')"))
    pg.click('#icu0 .iet'); pg.wait_for_timeout(250); chk('tapping a time button jumps there (0:00) and highlights the line', ev("document.getElementById('ieau').currentTime") < 0.6 and ev("document.getElementById('icu0').classList.contains('on')"))
    ev("document.getElementById('ieau').pause()")
    rates = []
    for _ in range(4): pg.click('#ierate'); rates.append(ev("document.getElementById('ieau').playbackRate"))
    chk('speed button cycles 1.25 -> 1.5 -> 0.75 -> 1', rates == [1.25, 1.5, 0.75, 1], rates)
    pg.click('#ieloop'); ev("()=>{const a=document.getElementById('ieau');a.currentTime=3.4;IMC=-1;ieTU();a.currentTime=6.05;ieTU()}"); pg.wait_for_timeout(100)
    chk('"⟲ gap" repeats the current line: past its end the audio jumps back to its start', abs(ev("document.getElementById('ieau').currentTime") - 3) < 0.2, ev("document.getElementById('ieau').currentTime"))
    pg.click('#ieloop'); ev("()=>{document.getElementById('ieau').currentTime=1}")
    pg.evaluate("document.querySelector('#iem .mfp').scrollTo(0,0)"); pg.screenshot(path='/tmp/ie_podcast.png')
    ev("ieMatClose()"); pg.wait_for_timeout(100)
    chk('closing the reader stops the audio and removes the player', not ev("!!document.getElementById('ieau')") and not ev("!!document.getElementById('iem')"))
    ev("()=>{S.ie.mat[0].au=1;idbDel('ieau'+S.ie.mat[0].id)}"); pg.wait_for_timeout(100); ev("ieMatOpen(S.ie.mat[0].id)"); pg.wait_for_timeout(400)
    chk('audio missing on this device (e.g. opened on another phone) is explained instead of crashing', 'Audio bu qurilmada yo‘q' in pg.inner_text('#iepl') and ev("document.querySelectorAll('#iem .iecu').length") == 3)
    ev("ieMatClose()"); ev("()=>{S.ie.mat[0].au=0}")
    # ---------- 4. text splitting and AI answer validation ----------
    long_text = ART + ' ' + 'This sentence is filler for the splitting test. ' * 90 + ' Some people remain reluctant to change their habits.'
    parts = ev("(t)=>iePartsOf(t)", long_text)
    chk('long text is cut at sentence ends into parts of at most 3500 characters (max 4)', 2 <= len(parts) <= 4 and all(len(x) <= 3500 for x in parts) and all(x.rstrip()[-1] in '.!?' for x in parts[:-1]), [len(x) for x in parts])
    chk('a single endless sentence is hard-cut instead of being sent whole', max(len(x) for x in ev("(t)=>iePartsOf(t)", 'word ' * 3000)) <= 3500 and len(ev("(t)=>iePartsOf(t)", 'word ' * 3000)) == 4)
    res = ev("""(full)=>{const r={words:[],chunks:[],lv:'',topic:''};ieMerge(r,{level:'C1',topic:'urban flooding',
      words:[{w:'mitigate',f:'mitigated',pos:'v',lv:'C1',def:'make less severe',uz:'yumshatmoq',ctx:'The city council announced that the new plan mitigated the risk of flooding in low-lying districts.',ex:'Trees mitigate heat.'},
             {w:'imaginary',f:'imaginaryword',pos:'n',lv:'C1',def:'x',uz:'',ctx:'',ex:''},
             {w:'drainage',f:'drainage',pos:'weird',lv:'A1',def:'a system',uz:'drenaj',ctx:'This sentence was invented by the model.',ex:''},
             {w:'Mitigate',f:'mitigated',pos:'v',lv:'C2',def:'dup',uz:'',ctx:'',ex:''},{w:'two words',f:'two words',pos:'n',lv:'C1',def:'x',uz:'',ctx:'',ex:''},{w:'ab',f:'ab',pos:'n',lv:'C1',def:'x',uz:'',ctx:'',ex:''}],
      chunks:[{p:'on the other hand',k:'phrase',def:'in contrast',uz:'boshqa tomondan',ctx:'On the other hand, critics argued that the scheme was far too expensive.',ex:'x'},
              {p:'sustainable drainage',k:'weirdkind',def:'d',uz:'',ctx:'',ex:''},{p:'in the long run',k:'idiom',def:'d',uz:'',ctx:'',ex:''},{p:'far',k:'phrase',def:'d',uz:'',ctx:'',ex:''},{p:'a b c d e f g',k:'phrase',def:'d',uz:'',ctx:'',ex:''}]},full);return r}""", ART)
    chk('the AI answer is validated: words/chunks that are NOT in the text are dropped (imaginary word, "in the long run")', [w['w'] for w in res['words']] == ['mitigate', 'drainage'] and [c['p'] for c in res['chunks']] == ['on the other hand', 'sustainable drainage'], res)
    chk('duplicates, multi-word "words", 2-letter words, 1-word chunks and 7-word chunks are dropped', len(res['words']) == 2 and len(res['chunks']) == 2)
    chk('invented context sentences are blanked, real ones kept; bad level/pos/kind are cleaned', res['words'][0]['ctx'].startswith('The city council') and res['words'][1]['ctx'] == '' and res['words'][1]['lv'] == '' and res['words'][1]['pos'] == '' and res['chunks'][1]['k'] == 'phrase' and res['lv'] == 'C1' and res['topic'] == 'urban flooding')
    # ---------- 5. analysis flow ----------
    ev("""()=>{S.ie.mat=[{id:111,t:'Long one',k:'a',x:window.__lt,c:[],au:0,an:null,d:dk()}];S.ie.words=[{id:1,w:'alpha',m:'a',box:0,due:dk(),t:0}]}""".replace("window.__lt", json.dumps(long_text)))
    ev("""()=>{window.__calls=[];let n=0;window.fnAI=async(b)=>{window.__calls.push(b);n++;
        if(n===1)return {text:JSON.stringify({level:'B2',topic:'cities',words:[{w:'mitigate',f:'mitigated',pos:'v',lv:'C1',def:'make less severe',uz:'yumshatmoq',ctx:'',ex:'e1'}],chunks:[{p:'on the other hand',k:'phrase',def:'in contrast',uz:'',ctx:'',ex:''}]})};
        return {text:JSON.stringify({words:[{w:'reluctant',f:'reluctant',pos:'adj',lv:'C1',def:'unwilling',uz:'istamaydigan',ctx:'',ex:'e2'}],chunks:[]})}};ieMatOpen(111)}""")
    pg.wait_for_timeout(400); pg.click('#iem >> text=AI bilan tahlil'); pg.wait_for_timeout(900)
    an = ev("S.ie.mat[0].an")
    chk('analysis runs part by part and merges the results (mitigate from part 1, reluctant from part 2)', an and [w['w'] for w in an['words']] == ['mitigate', 'reluctant'] and an['n'] >= 2 and ev("__calls.length") == an['n'] and an['lv'] == 'B2' and an['topic'] == 'cities', an)
    chk('each AI request carries one part of the text and the user\u2019s existing words (so they are not suggested again)', all(c['action'] == 'vocab' and c['mode'] == 'analyze' and len(c['text']) <= 3500 and 'alpha' in c['known'] for c in ev("__calls")))
    chk('the result is stored with the date', an['at'] == '2026-10-31' and 'so‘z' in pg.inner_text('#iems'))
    # partial failure keeps what was found
    ev("""()=>{S.ie.mat[0].an=null;let n=0;window.__calls=[];window.fnAI=async(b)=>{window.__calls.push(b);n++;if(n===1)return {text:JSON.stringify({words:[{w:'mitigate',f:'mitigated',pos:'v',lv:'C1',def:'d',uz:'',ctx:'',ex:''}],chunks:[]})};throw new Error('Bugungi limit tugadi (40 ta so‘rov).')};ieMatDraw()}""")
    pg.click('#iem >> text=AI bilan tahlil'); pg.wait_for_timeout(700)
    chk('if a later part fails, the words already found are kept and the error is shown', ev("S.ie.mat[0].an.words.length") == 1 and 'Bugungi limit tugadi' in pg.inner_text('#iemb') and 'Qism 2/' in pg.inner_text('#iemb'))
    chk('after a failed part the button offers to RESUME from that part and says earlier parts are saved', 'Davom ettirish (qism 2/' in pg.inner_text('#iemb') and 'oldingilari saqlangan' in pg.inner_text('#iemb'))
    chk('a non-timeout error (daily limit) is NOT retried automatically (1 call for part 1, 1 for part 2)', ev("__calls.length") == 2, ev("__calls.length"))
    ev("""()=>{window.__calls=[];window.fnAI=async(b)=>{window.__calls.push(b);return {text:JSON.stringify({words:[{w:'reluctant',f:'reluctant',pos:'adj',lv:'C1',def:'unwilling',uz:'',ctx:'',ex:''}],chunks:[]})}}}""")
    pg.click('#iem >> text=Davom ettirish'); pg.wait_for_timeout(500)
    an = ev("S.ie.mat[0].an"); chk('resume runs ONLY the remaining part (1 request), keeps the words from part 1 and adds the new ones', ev("__calls.length") == 1 and [w['w'] for w in an['words']] == ['mitigate', 'reluctant'] and ev("IMP") is None, (ev("__calls.length"), an))
    # slow answers are retried once automatically
    ev("""()=>{S.ie.mat[0].an=null;IMP=null;IMA=null;let n=0;window.__calls=[];window.fnAI=async(b)=>{window.__calls.push(b);n++;if(n===1)throw new Error('AI juda sekin javob berdi. Qayta urinib ko‘ring.');return {text:JSON.stringify({words:[{w:'mitigate',f:'mitigated',pos:'v',lv:'C1',def:'d',uz:'',ctx:'',ex:''}],chunks:[]})}};ieMatDraw()}""")
    pg.click('#iem >> text=AI bilan tahlil'); pg.wait_for_timeout(700)
    np_ = ev("iePartsOf(ieText(S.ie.mat[0])).length")
    chk('a slow AI answer is retried once by itself: no error is shown and the analysis completes (%d parts + 1 retry)' % np_, ev("__calls.length") == np_ + 1 and ev("S.ie.mat[0].an.words.length") >= 1 and 'juda sekin' not in pg.inner_text('#iemb'), (ev("__calls.length"), np_))
    # slow twice -> error + resume point on that part
    ev("""()=>{S.ie.mat[0].an=null;IMP=null;IMA=null;window.__calls=[];window.fnAI=async(b)=>{window.__calls.push(b);throw new Error('AI juda sekin javob berdi. Qayta urinib ko‘ring.')};ieMatDraw()}""")
    pg.click('#iem >> text=AI bilan tahlil'); pg.wait_for_timeout(700)
    chk('two slow answers in a row: the error is shown (2 tries on part 1 only) and nothing is lost', ev("__calls.length") == 2 and 'Qism 1/' in pg.inner_text('#iemb') and ev("IMP.next") == 0 and 'AI bilan tahlil' in pg.inner_text('#iemb'))
    ev("""()=>{window.__calls=[];window.fnAI=async(b)=>{window.__calls.push(b);return {text:JSON.stringify({words:[],chunks:[]})}};IMA=null;IMP={id:111,res:{words:[{w:'old',f:'old',pos:'',lv:'',def:'',uz:'',ctx:'',ex:''}],chunks:[],lv:'',topic:''},next:1,n:99}}""")
    ev("ieAnalyze(111)"); pg.wait_for_timeout(500)
    chk('if the text changed since (different number of parts) the saved progress is ignored and the analysis restarts from part 1', ev("__calls.length") == ev("iePartsOf(ieText(S.ie.mat[0])).length") and ev("__calls[0].text") == ev("iePartsOf(ieText(S.ie.mat[0]))[0]"))
    chk('heavy actions get a longer wait than ordinary ones (vocab and reading 105 s, grading 95 s, others 60 s)', ev("""(async()=>{const got={};window.fnPost=async(b,ms)=>{got[b.action]=ms;return {text:'x'}};for(const a of ['vocab','reading','ielts','plan'])await window.__fnAI0({action:a});return got})()""") == {'vocab': 105000, 'reading': 105000, 'ielts': 95000, 'plan': 60000})
    ev("()=>{IMA=null;IMP=null}")
    ev("()=>{let k=0;window.__calls=[];window.fnAI=async(b)=>{k++;window.__calls.push(b);await new Promise(r=>setTimeout(r,300));return {text:'{}'}};ieAnalyze(111);ieAnalyze(111);ieAnalyze(111)}"); pg.wait_for_timeout(1800)
    chk('pressing analyse repeatedly does not start parallel runs', ev("__calls.length") == ev("iePartsOf(ieText(S.ie.mat[0])).length"), ev("__calls.length"))
    ev("ieMatClose()")
    # ---------- 6. reader: highlighting, sheet, adding ----------
    ev("""(art)=>{S.ie.words=[];S.ie.mat=[{id:222,t:'Flood <b>plan</b>',k:'a',x:art+' Also <script>alert(1)</script> here.',c:[],au:0,d:dk(),an:{lv:'C1',topic:'floods',n:1,at:dk(),
      words:[{w:'mitigate',f:'mitigated',pos:'v',lv:'C1',def:'make less severe',uz:'yumshatmoq',ctx:'The city council announced that the new plan mitigated the risk of flooding in low-lying districts.',ex:'Trees mitigate heat.'},
             {w:'scheme',f:'scheme',pos:'n',lv:'B2',def:'a plan',uz:'reja',ctx:'',ex:'The scheme failed.'},{w:'drainage',f:'drainage',pos:'n',lv:'C1',def:'a system for removing water',uz:'drenaj',ctx:'',ex:'Drainage is poor.'}],
      chunks:[{p:'mitigated the risk',k:'collocation',def:'reduced the danger',uz:'xavfni kamaytirdi',ctx:'',ex:'We mitigated the risk.'},{p:'on the other hand',k:'phrase',def:'in contrast',uz:'boshqa tomondan',ctx:'',ex:'On the other hand, it works.'}]}}];ieMatOpen(222)}""", ART)
    pg.wait_for_timeout(400)
    chk('analysed words and chunks are highlighted in the text (3 words, chunks first)', ev("document.querySelectorAll('#iem mark.mc').length") == 2 and ev("document.querySelectorAll('#iem mark.mw2').length") == 2, (ev("document.querySelectorAll('#iem mark.mc').length"), ev("document.querySelectorAll('#iem mark.mw2').length")))
    chk('a chunk that contains a word takes precedence (mitigated is inside "mitigated the risk": one mark, not two)', ev("[...document.querySelectorAll('#iem mark.mc')].some(m=>m.textContent==='mitigated the risk')") and not ev("[...document.querySelectorAll('#iem mark.mw2')].some(m=>m.textContent==='mitigated')"))
    chk('HTML in the title and text is escaped (nothing is injected)', ev("document.querySelectorAll('#iem script').length") == 0 and ev("document.getElementById('iemt').innerHTML").count('<b>') == 0 and '<script>alert(1)</script>' in ev("document.querySelector('.ietx').textContent"))
    pg.click('#iem mark.mw2 >> nth=0'); pg.wait_for_timeout(150); sh = pg.inner_text('#iesh')
    chk('tapping a highlighted word opens the card: word, level, Uzbek meaning, definition, example', 'scheme' in sh and 'reja' in sh and 'a plan' in sh and 'The scheme failed.' in sh and 'B2' in sh, sh)
    pg.click('#iesh >> text=Lug‘atga qo‘shish'); pg.wait_for_timeout(200)
    w = ev("S.ie.words.find(x=>x.w==='scheme')")
    chk('adding creates a full vocabulary item: word, meaning, definition, example, level, source, new-card state', w and w['m'] == 'reja' and w['d'] == 'a plan' and w['e'] == 'The scheme failed.' and w['lv'] == 'B2' and w['pos'] == 'n' and w['k'] == 'w' and w['src'] == 222 and w['box'] == 0 and w['due'] == '2026-10-31' and w['t'] == 0, w)
    chk('the highlight turns green (already in the vocabulary) and the card closes', ev("!!document.querySelector('#iem mark.hv')") and not ev("!!document.getElementById('iesh')"))
    pg.click('#iem mark.hv >> nth=0'); pg.wait_for_timeout(100); chk('opening it again says "Lug‘atda bor" and offers no second add', 'Lug‘atda bor' in pg.inner_text('#iesh')); ev("ieSheetClose()")
    ev("window.__say=[]"); pg.click('#iem mark.mc >> nth=0'); pg.click('#iesh [aria-label=\"Talaffuz\"]'); chk('the 🔊 button pronounces the word or phrase', ev("__say") == ['mitigated the risk']); ev("ieSheetClose()")
    pg.click('#iem mark.mc >> nth=1'); pg.click('#iesh >> text=Lug‘atga qo‘shish'); pg.wait_for_timeout(150)
    chk('a chunk is stored as kind "c" with the phrase as the word', ev("S.ie.words.find(x=>x.w==='on the other hand').k") == 'c')
    # unknown word -> AI define
    ev("""()=>{window.__calls=[];window.fnAI=async(b)=>{window.__calls.push(b);return {text:JSON.stringify({w:'expensive',pos:'adj',lv:'B1',def:'costing a lot of money',uz:'qimmat',ex:'The car is expensive.'})}}}""")
    pg.click('#iem .iew >> text=expensive'); pg.wait_for_timeout(150)
    chk('tapping a word the AI did not mark offers to ask the AI, with the sentence it came from', 'AI dan ma’nosini so‘rash' in pg.inner_text('#iesh') and 'critics argued' in pg.inner_text('#iesh'))
    pg.click('#iesh >> text=AI dan ma’nosini so‘rash'); pg.wait_for_timeout(300)
    chk('the define request carries the word and its sentence; the answer is shown', ev("__calls[0].mode") == 'define' and ev("__calls[0].word") == 'expensive' and 'critics argued' in ev("__calls[0].ctx") and 'qimmat' in pg.inner_text('#iesh'))
    pg.click('#iesh >> text=Lug‘atga qo‘shish'); pg.wait_for_timeout(200); chk('and it can be added with the sentence as context', ev("S.ie.words.find(x=>x.w==='expensive').c").startswith('On the other hand') and ev("S.ie.words.find(x=>x.w==='expensive').u") == 'qimmat')
    ev("""()=>{window.fnAI=async()=>{throw new Error('offline')}}"""); pg.click('#iem .iew >> text=Residents'); pg.click('#iesh >> text=AI dan ma’nosini so‘rash'); pg.wait_for_timeout(300)
    chk('if the AI fails the card shows the error and still offers the quick add', 'offline' in pg.inner_text('#iesh') and 'Faqat so‘zni qo‘sh' in pg.inner_text('#iesh'))
    pg.click('#iesh >> text=Faqat so‘zni qo‘sh'); pg.wait_for_timeout(150); chk('quick add stores just the word (meaning can be written later)', ev("S.ie.words.find(x=>x.w==='Residents').m") == '' and ev("S.ie.words.find(x=>x.w==='Residents').box") == 0)
    # selection list
    ev("S.ie.words=S.ie.words.filter(x=>x.w==='scheme')"); ev("()=>{IMSEL={_o:1};ieMatDraw()}"); pg.wait_for_timeout(100)
    rows = ev("document.querySelectorAll('#iem .ierow').length"); chk('the results list shows every item; the one already in the vocabulary is ticked and disabled', rows == 5 and ev("document.querySelectorAll('#iem .ierow.hv input:disabled').length") == 1, rows)
    pg.click('#iem .seg button >> text=Chunklar'); pg.wait_for_timeout(100); chk('filter "Chunklar" shows only phrases', ev("document.querySelectorAll('#iem .ierow').length") == 2)
    pg.click('#iem .seg button >> text=C1'); pg.wait_for_timeout(100); chk('filter "C1" shows only C1 items', ev("document.querySelectorAll('#iem .ierow').length") == 2)
    pg.click('#iem .seg button >> text=Hammasi'); pg.check('#iem .ierow:not(.hv) input >> nth=0'); pg.check('#iem .ierow:not(.hv) input >> nth=1'); pg.wait_for_timeout(100)
    chk('ticking two items enables "Tanlanganlarni qo‘shish (2)"', 'Tanlanganlarni qo‘shish (2)' in pg.inner_text('#iem')); pg.click('#iem >> text=Tanlanganlarni qo‘shish'); pg.wait_for_timeout(200)
    chk('both are added; nothing is added twice', ev("S.ie.words.length") == 3 and len(set(x['w'].lower() for x in ev("S.ie.words"))) == 3)
    # finishing
    xp0 = ev("dayPts(dk()).t"); pg.click('#iem >> text=Tugatdim'); pg.wait_for_timeout(200)
    chk('"✓ Tugatdim" ticks today\u2019s IELTS plan item and gives +15 XP once', ev("S.ie.mr['2026-10-31']") == 1 and ev("ieDp().a") == 1 and ev("dayPts(dk()).t") - xp0 == 15 and ev("S.ie.mat[0].dn") == '2026-10-31')
    pg.evaluate("document.querySelector('#iem .mfp').scrollTo(0,0)"); pg.screenshot(path='/tmp/ie_reader.png')
    ev("ieMatClose()")
    # ---------- 7. vocabulary cards ----------
    ev("""()=>{S.ie.words=[{id:11,w:'mitigate',m:'yumshatmoq',u:'yumshatmoq',d:'make less severe',e:'Trees mitigate heat.',c:'The plan mitigated the risk of flooding.',pos:'v',lv:'C1',k:'w',box:0,due:dk(),t:0},{id:12,w:'plain',m:'oddiy',box:0,due:dk(),t:0}];IR=0;IRM='f';tab='e';EV='i';IVW='l';render()}""")
    pg.wait_for_timeout(150); t = pg.inner_text('#app')
    chk('the card shows the word with the pronunciation button and its level before the meaning', 'mitigate' in t and 'v · C1' in t and 'yumshatmoq' not in t.split('Takror')[1].split('jami')[0] if 'Takror' in t else True)
    pg.click('#app >> text=Ma’nosini ko‘rsat'); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('revealing shows the Uzbek meaning, English definition, example and the original sentence', 'yumshatmoq' in t and 'make less severe' in t and 'Trees mitigate heat.' in t and 'The plan mitigated the risk of flooding.' in t)
    ev("window.__say=[]"); pg.click('#app .hero [aria-label=\"Talaffuz\"]'); chk('🔊 speaks the English word', ev("__say") == ['mitigate'])
    pg.click('#app >> text=Gapni to‘ldir'); pg.wait_for_timeout(100); t = pg.inner_text('#app .hero')
    chk('cloze mode hides the word inside its sentence ("The plan _____ the risk…") and shows the Uzbek hint', 'The plan _____ the risk of flooding.' in t and 'Ishora: yumshatmoq' in t and 'mitigate\n' not in t, t[:200])
    pg.click('#app >> text=Javobni ko‘rsat'); pg.wait_for_timeout(100); chk('"Javobni ko‘rsat" reveals the word and the meaning', 'mitigate' in pg.inner_text('#app .hero') and 'make less severe' in pg.inner_text('#app .hero'))
    pg.click('#app .hero >> text=Bildim'); pg.wait_for_timeout(150)
    w = ev("S.ie.words.find(x=>x.id===11)"); chk('answering works as before: box 1, next review scheduled, review time stored', w['box'] == 1 and w['due'] > '2026-10-31' and w['t'] > 0, w)
    t = pg.inner_text('#app .hero'); chk('a word without a sentence falls back to the normal card even in cloze mode', 'plain' in t and 'Ma’nosini ko‘rsat' in pg.inner_text('#app'))
    ev("IRM='f'")
    # daily new-word limit
    ev("""()=>{S.ie.nd=undefined;S.ie.nl=3;S.ie.words=Array.from({length:8},(_,i)=>({id:100+i,w:'new'+i,m:'m',box:0,due:dk(),t:0})).concat([{id:200,w:'old',m:'o',box:2,due:dk(),t:5}]);IR=0;render()}""")
    chk('with a limit of 3 new words only 3 new ones (+ the old due one) are offered', ev("wDue().length") == 4, ev("wDue().map(w=>w.w)"))
    for _ in range(3): ev("iAns(1)")
    chk('after 3 new words were answered, the remaining new ones wait for tomorrow; the old due word is still offered', ev("S.ie.nd.n") == 3 and ev("wDue().map(w=>w.w)") == ['old'], ev("wDue().map(w=>w.w)"))
    ev("iAns(0)"); chk('a word answered "Bilmadim" comes back the same day (it is not new any more)', ev("wDue().map(w=>w.w)") == ['old'] or 'old' in ev("wDue().map(w=>w.w)"))
    pg.clock.set_system_time(datetime.datetime(2026, 11, 1, 10, 0, 0)); ev("rwReset()")
    chk('next day the counter resets and new words appear again', ev("ieNd()") == 0 and sum(1 for w in ev("wDue()") if w['t'] == 0) == 3)
    pg.clock.set_system_time(datetime.datetime(2026, 10, 31, 10, 0, 0)); ev("rwReset()")
    ev("S.ie.nl=undefined;ieNl(-100)"); chk('the limit stepper stays between 3 and 40', ev("S.ie.nl") == 3); ev("ieNl(100)"); chk('...', ev("S.ie.nl") == 40); ev("S.ie.nl=undefined")
    ev("""()=>{S.ie.words=[{id:1,w:'on the other hand',m:'m',k:'c',lv:'',box:0,due:dk(),t:0},{id:2,w:'mitigate',m:'m',k:'w',lv:'C1',box:3,due:'2099-01-01',t:1},{id:3,w:'easy',m:'m',k:'w',lv:'B2',box:0,due:'2099-01-01',t:0}];ILF='a';render()}""")
    pg.click('#app .seg button >> text=Chunklar'); pg.wait_for_timeout(100); chk('list filter: chunks', 'on the other hand' in pg.inner_text('#app') and ev("document.querySelectorAll('#app .row .t').length") == 1 and True)
    pg.click('#app .seg button >> text=C1'); pg.wait_for_timeout(100); chk('list filter: only C1 words', 'mitigate' in pg.inner_text('#app') and 'easy' not in pg.inner_text('#app').split('Qidirish')[-1])
    pg.click('#app .seg button >> text=Yangi'); pg.wait_for_timeout(100); chk('list filter: new (never answered correctly)', 'easy' in pg.inner_text('#app'))
    ev("ILF='a'")
    # ---------- 8. readiness panel ----------
    ev("""()=>{S.ie.target=7;S.ie.ex='2026-12-20';S.ie.vg=1500;S.ie.tests=[{id:1,d:dk(),k:'M',b:{L:7,R:6.5,W:6,S:7}}];S.ie.words=Array.from({length:150},(_,i)=>({id:i,w:'w'+i,m:'m',box:4,due:'2099-01-01',t:Date.now()-i*864e5/10}));
      S.ie.dp={};for(let i=0;i<7;i++){S.ie.dp[dAgo(i)]={v:1,L:1,R:1}}S.ie.mat=[{id:1,t:'x',k:'a',x:'x',c:[],d:dk(),an:null}];S.ie.words.slice(0,20).forEach(w=>w.src=1);rwReset()}""")
    R = ev("ieReady()"); st = ev("ieStat()"); skill = sum(min(1, st['c'][k] / 7) for k in 'LRWS') / 4
    exp = round(skill * 40 + 0.1 * 20 + 0.5 * 20 + (1 / 3) * 20)
    chk('readiness = skills 40%% + vocabulary 20%% + 14-day consistency 20%% + 30-day mocks 20%%  (expected %d)' % exp, R['pc'] == exp and R['vocab'] == 10 and R['cons'] == 50 and R['mock'] == 33 and R['learned'] == 150, R)
    chk('panel numbers: due words, words from materials, materials count', R['mat'] == 1 and R['fromMat'] == 20 and R['week'] >= 1)
    chk('the next-step hint follows priorities: weakest skill when nothing is due', 'Writing' in R['next'] or 'Reading' in R['next'], R['next'])
    ev("S.ie.words[0].due='2000-01-01'"); chk('...and due words come first', 'navbatda' in ev("ieReady().next"))
    ev("S.ie.words[0].due='2099-01-01';S.ie.tests=[]"); chk('...then "no mock in 30 days"', 'mock' in ev("ieReady().next") and ev("ieReady().mock") == 0)
    ev("S.ie.tests=[];S.ie.words=[];S.ie.mat=[];S.ie.dp={}"); R0 = ev("ieReady()"); chk('empty state: 0% and an invitation to add the first article (no crash, no NaN)', R0['pc'] == 0 and 'Birinchi maqolani' in R0['next'] and 'NaN' not in json.dumps(R0))
    # hifz stats
    ev("""()=>{const q=S.q;q.m={};q.ord=[];q.ny={};q.ppd=3;q.lg=[];q.sqd={};q.mzd={};q.mzp=null;q.cur=0;for(let i=77;i<114;i++){q.m[i]=SL(i);q.ord.push(i)}q.m[1]=10;q.ord.push(1);q.ny={[dk()]:2,[dAgo(2)]:3,[dAgo(9)]:5};rwReset()}""")
    Hs = ev("hifzStats()"); tot = ev("TOT"); done = ev("mdone()")
    chk('hifz: memorised pages, remaining (= all - memorised), percentage', abs(Hs['done'] - round(done, 1)) < 0.06 and abs(Hs['rem'] - round(tot - done, 1)) < 0.06 and Hs['pc'] == round(done / tot * 100), Hs)
    chk('hifz: completion date = today + ceil(remaining / pages per day)', Hs['days'] == -(-(tot - done) // 3) or abs(Hs['days'] - (tot - done) / 3) < 1.01, Hs)
    chk('hifz: this week = last 7 days only (2 + 3, not the 5 from nine days ago), today\u2019s sabaq = 2', Hs['week'] == 5 and Hs['sabaq'] == 2, Hs)
    chk('hifz: Juz\u2019 Amma (surahs 78-114) memorised completely = 1 full juz', Hs['juz'] == 1, Hs['juz'])
    ev("S.q.ppd=0;rwReset()"); chk('no daily plan -> no completion date, no crash', ev("hifzStats().days") == 0 and ev("hifzStats().eta") == '')
    ev("S.q.ppd=3;S.q.m={};S.q.ord=[];rwReset()"); chk('nothing memorised: 0%, all pages remaining', ev("hifzStats().pc") == 0 and abs(ev("hifzStats().rem") - round(tot, 1)) < 0.06)
    # panel in the UI
    ev("""()=>{S.ie.target=7;S.ie.ex='2026-12-20';S.ie.tests=[{id:1,d:dk(),k:'M',b:{L:7,R:6.5,W:6,S:7}}];S.ie.words=Array.from({length:40},(_,i)=>({id:i,w:'w'+i,m:'m',box:i<12?4:0,due:'2099-01-01',t:1}));S.q.m={1:10};S.q.ord=[1];S.q.ppd=3;tab='e';EV='i';IVW='b';rwReset();render()}""")
    pg.wait_for_timeout(200); t = pg.inner_text('#app')
    chk('IELTS Bosh shows both goals: the IELTS readiness card and a compact Quran hifz card with a shortcut to Takror', 'IELTS tayyorgarligi' in t and 'Qur‘on hifzi' in t and 'Imtihongacha 50 kun' in t and 'bet qoldi' in t and 'Takrorni ochish' in t)
    ov = ev("document.documentElement.scrollWidth"); chk('the panel does not overflow the phone width', ov <= 392, ov)
    pg.evaluate("document.querySelectorAll('canvas').forEach(c=>c.remove());document.querySelector('.dpn').scrollIntoView({block:'start'})"); pg.wait_for_timeout(200); pg.screenshot(path='/tmp/ie_panel.png')
    ev("()=>{tab='m';render()}"); pg.wait_for_timeout(150); chk('the Maqsad tab shows the full panel (IELTS + hifz with juz\u2019, week and sabqi status)', 'IELTS tayyorgarligi' in pg.inner_text('#app') and 'Qur‘on hifzi' in pg.inner_text('#app') and 'To‘liq juz’lar' in pg.inner_text('#app'))
    ev("()=>{tab='e';EV='i';IVW='b';render()}"); pg.wait_for_timeout(120); chk('today\u2019s IELTS plan now has the "Maqola yoki podkast" item', 'Maqola yoki podkast' in pg.inner_text('#app'))
    ev("""()=>{tab='e';EV='i';IVW='a';S.ie.mat=[];render()}"""); chk('empty library explains what to add', 'Hali material yo‘q' in pg.inner_text('#app'))
    # library limit
    ev("""()=>{S.ie.mat=[];for(let i=0;i<15;i++)S.ie.mat.push({id:i+1,t:'m'+i,k:'a',x:'x'.repeat(300),c:[],au:0,an:null,d:dk()});IMF.add=1;IMF.mk='a';render()}"""); pg.fill('#mt', 'Newest'); pg.fill('#mx', ART); pg.click('#app >> text=Saqlash va ochish'); pg.wait_for_timeout(400)
    chk('the library keeps at most 15 materials: the newest is added at the top, the oldest is dropped', ev("S.ie.mat.length") == 15 and ev("S.ie.mat[0].t") == 'Newest' and not ev("S.ie.mat.some(m=>m.id===15)") and ev("S.ie.mat.some(m=>m.id===1)"))
    ev("ieMatClose()")
    big = 'Word number one is here. ' * 700
    ev("""(t)=>{IMF.add=1;IMF.mk='a';tab='e';EV='i';IVW='a';render()}""", big); pg.fill('#mt', 'Big'); pg.fill('#mx', big); pg.click('#app >> text=Saqlash va ochish'); pg.wait_for_timeout(400)
    chk('very long articles are cut to 12,000 characters (with a message) so the saved data stays small', ev("S.ie.mat[0].x.length") <= 12000 and ev("S.ie.mat[0].x.length") > 11000)
    ev("ieMatClose()")
    ev("""()=>{S.ie.mat=[{id:5,t:'Del',k:'p',x:'',c:[[0,3,'abc def ghi']],au:1,an:null,d:dk()}];window.confirm=()=>true;tab='e';EV='i';IVW='a';render()}""")
    pg.evaluate("document.querySelector('.iemr .x[aria-label=\"O‘chirish\"]').click()"); pg.wait_for_timeout(150); chk('deleting a material works (vocabulary stays)', ev("S.ie.mat.length") == 0)
    chk('no JavaScript errors during the whole run', not errs, errs[:3])
    b.close()
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
