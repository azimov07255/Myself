import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# IELTS: qayta tartib, AI Reading mashqi, Xatolar daftari, gap tekshirish, diktant, AI hisoblagich va kontekst. Soat: 2026-10-31 10:00.
import sys, os, shutil, json, struct, http.server, threading, socketserver, functools, datetime
from playwright.sync_api import sync_playwright
OUT = ROOT; SITE = '/tmp/site_iea'
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
PASSAGE = ("Urban planners increasingly recognise that cities must mitigate the effects of heavy rainfall. In many coastal regions, sustainable drainage has become a priority for local authorities. "
           "Critics argue that the scheme is expensive, although supporters insist that long-term savings are significant. Residents often remain reluctant to accept higher taxes for projects whose benefits are invisible. "
           "However, recent studies suggest that investment in green infrastructure reduces flood damage by almost forty percent. The authorities therefore plan to extend the programme to twelve additional districts by the end of the decade.\n\n"
           "Meanwhile, engineers in several countries have experimented with permeable pavements, rooftop gardens and underground storage tanks, each of which absorbs or delays runoff during storms. Although these technologies require careful maintenance, "
           "municipal budgets in wealthier cities already include dedicated funding for them. Smaller towns, by contrast, frequently depend on national grants, which arrive unpredictably and rarely cover long-term upkeep.")
TOP = "[...document.querySelectorAll('#app .seg')].find(s=>s.textContent.includes('Bosh')&&s.textContent.includes('Materiallar'))"
SUB = "[...document.querySelectorAll('#app .seg')].find(s=>s.textContent.includes('Natijalar')&&s.textContent.includes('AI mashq'))"
def RJ(**k):
    d = {'title': 'Cities and rain', 'passage': PASSAGE, 'used': ['mitigate'],
         'questions': [{'t': 'tfng', 'q': 'Planners ignore heavy rainfall.', 'a': 'FALSE', 'why': 'Matn aksini aytadi.'},
                       {'t': 'tfng', 'q': 'Supporters say savings are significant.', 'a': 'TRUE', 'why': 'Uchinchi gap.'},
                       {'t': 'tfng', 'q': 'The programme will end in 2030.', 'a': 'NOT GIVEN', 'why': 'Sana aytilmagan.'},
                       {'t': 'mcq', 'q': 'What do residents often feel?', 'o': ['A. Eager', 'B. Reluctant', 'C. Angry', 'D. Bored'], 'a': 'B', 'why': 'reluctant'},
                       {'t': 'mcq', 'q': 'Flood damage falls by about…', 'o': ['A. 10%', 'B. 20%', 'C. 30%', 'D. 40%'], 'a': 'D', 'why': 'forty percent'},
                       {'t': 'mcq', 'q': 'Who plans the extension?', 'o': ['A. Residents', 'B. Critics', 'C. The authorities', 'D. Students'], 'a': 'C', 'why': 'The authorities'},
                       {'t': 'gap', 'q': 'Sustainable ____ is a priority.', 'a': 'drainage', 'why': 'matnda'},
                       {'t': 'gap', 'q': 'The programme covers ____ additional districts.', 'a': 'twelve', 'why': 'matnda'}]}
    d.update(k); return json.dumps({'text': json.dumps(d)})
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o');if(localStorage.getItem('trk_sgr')===null)localStorage.setItem('trk_sgr','a');if(localStorage.getItem('trk_ptb')===null)localStorage.setItem('trk_ptb','a')}catch(e){}"); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.clock.install(time=datetime.datetime(2026, 10, 31, 10, 0, 0))
    pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') or r.request.url.startswith('data:') or r.request.url.startswith('blob:') else r.abort())
    pg.goto(f'http://127.0.0.1:{PORT}/index.html'); pg.wait_for_timeout(600)
    pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())"); ev = pg.evaluate
    ev("()=>{S.ob=1;S.ts=1;S.ie.words=[];S.ie.mat=[];S.ie.tests=[];S.ie.wr=[];S.ie.pr=[];S.ie.ed={};S.ie.dp={};S.ie.mr={};window.__say=[];window.ieSay=t=>window.__say.push(t);window.__fnAI0=fnAI;tab='e';EV='i';IVW='b';render()}")
    # ---------- 1. tabs ----------
    top = ev("(" + TOP + ").textContent.length>0&&[...(" + TOP + ").children].map(b=>b.textContent.trim())")
    chk('IELTS has 5 top tabs (Bosh, Lug‘at, Kurs, Materiallar, Mashq) instead of 6 and they fit without scrolling', top == ['🏠 Bosh', '🔤 Lug‘at', '🎓 Kurs', '📰 Materiallar', '🎯 Mashq'] and not ev("(" + TOP + ").classList.contains('sc')"), top)
    chk('Bosh has no second row of tabs', ev("!(" + SUB + ")"))
    pg.click('#app .seg button >> text=Mashq'); pg.wait_for_timeout(120)
    sub = ev("[...(" + SUB + ").children].map(b=>b.textContent.trim())")
    chk('Mashq opens a sub-row: Natijalar, Writing, Speaking, AI mashq, Imtihon (all five fit the phone width, no scrolling)', sub == ['Natijalar', 'Writing', 'Speaking', 'AI mashq', 'Imtihon'] and ev('(' + SUB + ').scrollWidth<=(' + SUB + ').clientWidth+1'), sub)
    chk('the top tab "Mashq" stays highlighted for all four sub-screens, and each renders', all(
        (ev(f"()=>{{IVW='{v}';render()}}") or True) and 'Kechirasan' not in pg.inner_text('#app') and 'Mashq' in pg.evaluate("(" + TOP + ").querySelector('.on').textContent") for v in 'mwsx'))
    ev("()=>{IVW='l';render()}"); chk('leaving Mashq removes the sub-row', ev("!(" + SUB + ")"))
    ev("()=>{IVW='a';render()}"); chk('Materiallar still works', 'Kutubxona' in pg.inner_text('#app'))
    ev("()=>{S.ie.target=7;S.ie.ex='2026-12-20';S.ie.tests=[{id:1,d:dk(),k:'M',b:{L:7,R:6.5,W:6,S:7}},{id:2,d:dAgo(5),k:'M',b:{L:6,R:6,W:5.5,S:6}}];S.ie.words=[];IVW='b';render()}"); pg.wait_for_timeout(150)
    t = pg.inner_text('#app'); order = [t.index(s) for s in ['IELTS tayyorgarligi', 'Qur‘on hifzi', 'Bugungi reja']] + [t.rindex('Ko‘nikmalar'), t.index('Mock natijalari')]
    chk('Bosh is organised: readiness card -> hifz card -> today\u2019s plan -> skills -> mock trend', order == sorted(order), order)
    chk('the old duplicate hero ("Taxminiy umumiy ball") and the repeated counters row are gone', 'Taxminiy umumiy ball' not in t and 'ketma-ket mashq' not in t)
    chk('settings are tucked into a collapsed "Sozlamalar" block (target band, exam date, vocabulary goal)', ev("!!document.querySelector('#app details.sd')") and not ev("document.querySelector('#app details.sd').open") and 'Lug‘at maqsadi' in ev("document.querySelector('#app details.sd').textContent"))
    h_old = 2800; chk('the Bosh screen is much shorter than before (was ~2,900 px on the same data)', ev("document.documentElement.scrollHeight") < h_old, ev("document.documentElement.scrollHeight"))
    # ---------- 2. reading practice ----------
    ev("""()=>{S.ie.words=[{id:1,w:'mitigate',m:'x',box:0,due:dk(),t:0},{id:2,w:'scheme',m:'x',box:1,due:dk(),t:5},{id:3,w:'reluctant',m:'x',box:0,due:dk(),t:2},{id:4,w:'on the other hand',m:'x',box:0,k:'c',due:dk(),t:0},{id:5,w:'abundant',m:'x',box:5,due:dk(),t:9},{id:6,w:'cat',m:'x',box:0,due:dk(),t:1}];IVW='x';render()}""")
    chk('the 6-or-fewer weakest single words are chosen (lowest box first; chunks and 3-letter words skipped)', ev("ieRdPick()") == ['mitigate', 'reluctant', 'scheme', 'abundant'], ev("ieRdPick()"))
    ev("()=>{window.__calls=[];window.fnAI=async(b)=>{window.__calls.push(b);await new Promise(r=>setTimeout(r,300));return JSON.parse(window.__resp)};window.__resp=%s;}" % json.dumps(RJ()))
    pg.fill('#rdt', 'urban flooding'); pg.click('#app >> text=Mashq yaratish'); pg.click('#app >> text=Mashq yaratish') if False else None; pg.wait_for_timeout(120)
    chk('while the AI writes, the button is disabled and says so (no second request can start)', 'AI matn yozmoqda' in pg.inner_text('#app') and ev("document.querySelector('#app .big').disabled"))
    ev("ieRdGen()"); pg.wait_for_timeout(700)
    c = ev("__calls"); chk('exactly one request: action reading, the topic, the target band and the weak words', len(c) == 1 and c[0]['action'] == 'reading' and c[0]['topic'] == 'urban flooding' and c[0]['band'] == 7 and c[0]['words'] == ['mitigate', 'reluctant', 'scheme', 'abundant'], c)
    chk('the passage and 8 questions are shown, with the user\u2019s words highlighted inside the passage', ev("!!IRD.d") and ev("IRD.d.q.length") == 8 and ev("document.querySelectorAll('.ietx mark.mw2').length") >= 3 and 'Sariq belgilangan' in pg.inner_text('#app'))
    chk('only words that really occur in the passage are reported as "used" (abundant is not)', ev("IRD.d.used") == ['mitigate', 'reluctant', 'scheme'], ev("IRD.d.used"))
    # answer + check
    for i, v in enumerate(['FALSE', 'TRUE', 'TRUE']): ev(f"ieRdSet({i},'{v}')")
    ev("ieRdSet(3,'B')"); ev("ieRdSet(4,'D')"); ev("ieRdSet(5,'A')"); ev("ieRdSet(6,'Drainage.')"); ev("ieRdSet(7,'twelv')")
    ev("window.confirm=()=>true"); pg.click('#app >> text=Tekshirish'); pg.wait_for_timeout(200)
    chk('scoring: TFNG 2/3, MCQ 2/3, gap 2/2 (case, punctuation and a one-letter typo are tolerated) = 6/8', ev("IRD.sc") == 6 and ev("IRD.done") == 1 and '6 / 8' in pg.inner_text('#app'), ev("IRD.d.q.map(q=>q.ok)"))
    chk('every question shows the correct answer and the Uzbek explanation', 'To‘g‘ri javob: NOT GIVEN' in pg.inner_text('#app') and 'Sana aytilmagan.' in pg.inner_text('#app'))
    chk('the result is stored once (date, score, topic) and today\u2019s Reading plan item is ticked', ev("S.ie.pr.length") == 1 and ev("S.ie.pr[0].s") == 6 and ev("S.ie.pr[0].n") == 8 and ev("S.ie.pr[0].topic") == 'urban flooding' and ev("ieDp().R") == 1)
    ev("ieRdCheck()"); chk('checking again does not store it twice or change the score', ev("S.ie.pr.length") == 1)
    pg.evaluate("document.querySelectorAll('canvas').forEach(c=>c.remove());window.scrollTo(0,0)"); pg.screenshot(path='/tmp/iea_reading.png')
    pg.click('#app >> text=Materiallarga qo‘sh'); pg.wait_for_timeout(150); chk('the passage can be sent to Materiallar for word analysis', ev("S.ie.mat.length") == 1 and ev("S.ie.mat[0].k") == 'a' and ev("S.ie.mat[0].x").startswith('Urban planners'))
    pg.click('#app >> text=Yangi mashq'); pg.wait_for_timeout(100); chk('"Yangi mashq" returns to the setup form', not ev("!!IRD.d") and 'Mashq yaratish' in pg.inner_text('#app') and ev("!!document.getElementById('rdt')"))
    # validation of dishonest / broken AI answers
    def gen(resp):
        ev("(r)=>{window.__resp=r;IRD.d=null;IRD.err='';render()}", resp); ev("ieRdGen()"); pg.wait_for_timeout(600)
    bad_gap = RJ(); d = json.loads(json.loads(bad_gap)['text']); d['questions'][6]['a'] = 'zeppelin'; d['questions'][7]['a'] = 'a b c'
    gen(json.dumps({'text': json.dumps(d)})); chk('a gap answer that is NOT in the passage (or longer than 2 words) is dropped; the other 6 questions remain', ev("!!IRD.d") and ev("IRD.d.q.length") == 6 and ev("IRD.d.q.every(q=>q.t!=='gap')"), ev("IRD.d&&IRD.d.q.length"))
    d = json.loads(json.loads(RJ())['text']); d['questions'] = d['questions'][:3]
    gen(json.dumps({'text': json.dumps(d)})); chk('fewer than 5 verifiable questions -> a clear error, nothing shown', not ev("!!IRD.d") and 'ishonchli chiqmadi' in pg.inner_text('#app'))
    gen(RJ(passage='Too short to be a reading passage.')); chk('a too-short passage is refused with a message', not ev("!!IRD.d") and 'juda qisqa' in pg.inner_text('#app'))
    d = json.loads(json.loads(RJ())['text']); d['questions'][0]['a'] = 'MAYBE'; d['questions'][3]['o'] = ['A', 'B']; d['questions'][4]['a'] = 'Z'
    gen(json.dumps({'text': json.dumps(d)})); chk('invalid TFNG values, MCQ with 2 options and impossible letters are dropped (8 - 3 = 5 remain)', ev("IRD.d.q.length") == 5, ev("IRD.d&&IRD.d.q.length"))
    ev("()=>{window.fnAI=async()=>{throw new Error('Bugungi limit tugadi (40 ta so‘rov).')};IRD.d=null;render();ieRdGen()}"); pg.wait_for_timeout(300); chk('an AI/server error is shown in the setup card and the form stays usable', 'Bugungi limit tugadi' in pg.inner_text('#app') and not ev("document.querySelector('#app .big').disabled"))
    ev("S.ie.words=[];IRD.err='';render()"); chk('with fewer than 3 words the "use my words" box is disabled and explains why', ev("document.querySelector('#app input[type=checkbox]').disabled") and 'kamida 3 ta so‘z kerak' in pg.inner_text('#app'))
    # ---------- 3. sentence check ----------
    ev("""()=>{S.ie.words=[{id:11,w:'mitigate',m:'yumshatmoq',u:'yumshatmoq',d:'make less severe',e:'Trees mitigate heat.',pos:'v',lv:'C1',k:'w',box:0,due:dk(),t:0}];IR=1;IRM='f';ISC=null;IVW='l';render();window.__calls=[];window.fnAI=async(b)=>{window.__calls.push(b);return {text:JSON.stringify({ok:false,fix:'The plan reduces the risk.',better:'The plan mitigates the risk of floods.',note:'mitigate predlogsiz.'})}}}""")
    pg.click('#app >> text=Gap tuz va AI tekshirsin'); pg.wait_for_timeout(100); chk('the revealed card offers "Gap tuz", which opens a text box', ev("!!ISC") and ev("!!document.querySelector('#app textarea')"))
    pg.fill('#app textarea', 'short'); pg.click('#app >> text=Tekshirish'); pg.wait_for_timeout(100); chk('a too-short sentence is refused locally (no AI request spent)', ev("__calls.length") == 0 and 'Gap juda qisqa' in pg.inner_text('#app'))
    pg.fill('#app textarea', 'The plan mitigate to the risk of floods.'); pg.click('#app >> text=Tekshirish'); pg.wait_for_timeout(300)
    c = ev("__calls"); chk('the request carries the word and the student\u2019s sentence', len(c) == 1 and c[0]['mode'] == 'check' and c[0]['word'] == 'mitigate' and 'risk of floods' in c[0]['sentence'])
    t = pg.inner_text('#app'); chk('feedback: verdict, corrected sentence, better (band 7+) version and the note', '⚠ Tuzatish kerak' in t and 'The plan reduces the risk.' in t and 'mitigates the risk of floods' in t and 'mitigate predlogsiz.' in t)
    chk('usage is remembered on the word (tries and correct tries)', ev("S.ie.words[0].pu") == 1 and not ev("S.ie.words[0].po"))
    ev("()=>{iAns(1)}"); chk('answering the card closes the sentence box', ev("ISC") is None)
    # ---------- 4. error notebook ----------
    E = lambda o, c, t=None, w='izoh': dict(o=o, c=c, w=w, **({'t': t} if t else {}))
    ev("""(f)=>{S.ie.tests=[{id:1,d:dAgo(6),k:'W',b:{W:6},fb:{band:6,errors:f[0]}},{id:2,d:dAgo(3),k:'S',b:{S:6},fb:{band:6,errors:f[1]}},{id:3,d:dk(),k:'W',b:{W:6.5},fb:{band:6.5,errors:f[2]}}];S.ie.wr=[];S.ie.ed={};IVW='x';IED=null;render()}""",
       [[E('a lot of informations', 'a lot of information', 'grammar'), E('make a research', 'do research', 'collocation'), E('recieve', 'receive', 'spelling')],
        [E('A LOT of Informations', 'a lot of information.', 'grammar'), E('discuss about', 'discuss', 'vocab'), E('same one', 'same one', 'grammar'), E('weird thing', 'odd thing')],
        [E('make a research', 'do research', 'collocation'), E('in the other hand', 'on the other hand', 'banana')]])
    es = ev("ieErrs().map(e=>({o:e.o,n:e.n,t:e.t}))")
    chk('mistakes are merged across all feedbacks (case/punctuation ignored): "a lot of informations" x2, "make a research" x2', next(e for e in es if e['o'].lower().startswith('a lot of'))['n'] == 2 and next(e for e in es if e['o'] == 'make a research')['n'] == 2 and len(es) == 6, es)
    chk('entries where the "correction" equals the original are ignored; unknown/missing types become "other"', not any(e['o'] == 'same one' for e in es) and next(e for e in es if e['o'] == 'weird thing')['t'] == 'other' and next(e for e in es if e['o'] == 'in the other hand')['t'] == 'other')
    chk('the most repeated mistakes come first', ev("ieErrs()[0].n") == 2 and ev("ieErrs()[1].n") == 2)
    t = pg.inner_text('#app'); chk('the notebook card shows the totals, the types, the repeated mistakes and the latest ones', 'Xatolar daftari' in t and '6 xil' in t and 'Grammatika' in t and 'Kollokatsiya' in t and 'Qayta-qayta takrorlanayotgan' in t and 'a lot of information' in t)
    pg.evaluate("document.querySelectorAll('canvas').forEach(c=>c.remove())"); pg.screenshot(path='/tmp/iea_notebook.png')
    chk('Bosh shows a short notebook shortcut', (ev("()=>{IVW='b';render()}") or True) and 'Xatolar daftari: 6 xil xato' in pg.inner_text('#app')); ev("()=>{IVW='x';render()}")
    pg.click('#app >> text=Xatolarim bo‘yicha mashq'); pg.wait_for_timeout(150)
    chk('the drill starts with 5 of the open mistakes (the repeated ones included)', ev("IED.q.length") == 5 and ev("IED.q.some(q=>q.n>=2)") and 'Xatoni tuzat 1/5' in pg.inner_text('#app'))
    ev("()=>{window.__q=IED.q.map(q=>q.c)}"); score = 0
    for k in range(5):
        q = ev("IED.q[IED.i]")
        ans = q['c'] if k < 3 else ('zzz wrong answer' if k == 3 else q['c'].upper())
        pg.fill('#app input', ans); pg.click('#app >> text=Tekshirish'); pg.wait_for_timeout(80)
        chk('answer %d is judged correctly (%s)' % (k + 1, 'exact' if k < 3 else ('wrong' if k == 3 else 'upper-case')), ev("IED.res") == ('no' if k == 3 else 'ok') and q['c'] in pg.inner_text('#app') if k == 3 else ev("IED.res") == 'ok')
        pg.click('#app .goal >> text=Keyingisi') if k < 4 else pg.click('#app .goal >> text=Natija'); pg.wait_for_timeout(80)
    chk('the summary shows 4 / 5', ev("IED.end") == 1 and '4 / 5' in pg.inner_text('#app'))
    chk('each answer is remembered per mistake (correct counts go up, wrong goes to "bad")', sum(v['ok'] for v in ev("Object.values(S.ie.ed)")) == 4 and sum(v['bad'] for v in ev("Object.values(S.ie.ed)")) == 1)
    ev("()=>{IED=null;ieErrs().forEach(e=>{S.ie.ed[ieErrKey(e)]={ok:3,bad:0}});render()}"); chk('mistakes answered correctly 3 times leave the drill list (mastered)', ev("ieErrOpen().length") == 0 and 'Hamma xato o‘zlashtirilgan' in pg.inner_text('#app'))
    ev("()=>{S.ie.tests=[];S.ie.ed={};IED=null;render()}"); chk('with no AI-checked work the notebook explains how to fill it (no crash)', 'xatolaring shu yerda yig‘iladi' in pg.inner_text('#app'))
    ev("()=>{S.ie.tests=[{id:1,d:dk(),k:'W',fb:{errors:[{o:'x y',c:'z w'},{o:'a b',c:'c d'}]}}];IED=null;render()}"); chk('fewer than 3 open mistakes: no drill button, a hint instead', 'kamida 3 ta ochiq xato' in pg.inner_text('#app') and 'bo‘yicha mashq' not in pg.inner_text('#app').split('Mavzu')[0])
    # ---------- 5. dictation ----------
    ev("()=>{S.ie.tests=[];S.ie.words=[];IVW='a';IMF.add=0;render()}")
    srt = "1\n00:00:00,000 --> 00:00:03,000\nHello and welcome to the show, where we talk about cities and the way people live.\n\n2\n00:00:03,000 --> 00:00:06,000\nToday we discuss how cities mitigate the risk of flooding when heavy rain falls.\n\n3\n00:00:06,000 --> 00:00:08,000\nOn the other hand, the whole process is expensive and complicated for everyone involved."
    ev("()=>{IMF.add=1;IMF.mk='p';render()}"); pg.fill('#mt', 'Cities podcast'); pg.fill('#mx', srt); pg.set_input_files('#mf2', files=[{'name': 'ep.wav', 'mimeType': 'audio/wav', 'buffer': WAV}]); pg.click('#app >> text=Saqlash va ochish'); pg.wait_for_timeout(900)
    pg.wait_for_function("document.getElementById('ieau')&&document.getElementById('ieau').readyState>=1", timeout=8000)
    chk('podcast lines with audio get a ✍ dictation button next to the time button', ev("document.querySelectorAll('#iem .iecu [aria-label=\"Diktant\"]').length") == 3)
    pg.click('#icu1 [aria-label="Diktant"]'); pg.wait_for_timeout(300)
    chk('opening dictation plays that line (starts at 3.0 s) and shows the box', ev("!!document.getElementById('idt')") and 2.9 <= ev("document.getElementById('ieau').currentTime") < 3.6 and 'Diktant · 0:03' in pg.inner_text('#iesh'))
    ev("()=>{const a=document.getElementById('ieau');a.currentTime=6.3;ieTU()}"); chk('playback stops at the end of the line (6.0 s + small margin)', ev("document.getElementById('ieau').paused") is True and ev("IDK.stop") == 0)
    pg.click('#iesh >> text=Tekshirish'); pg.wait_for_timeout(100); chk('checking an empty box asks to type first', 'Avval eshitganingni yoz' in pg.inner_text('#iesh'))
    pg.fill('#idt', 'Today we discuss how cities the risk of flooding when heavy rain fall'); pg.click('#iesh >> text=Tekshirish'); pg.wait_for_timeout(150)
    r = ev("IDK.res"); chk('diff: 14 words in the line, 12 matched ("mitigate" missing, "falls" typed as "fall") = 86%', r['n'] == 14 and r['pct'] == 86 and [m.lower() for m in r['missed']] == ['mitigate', 'falls'], r)
    chk('correct words are green, missed words red; the missed ones are offered as buttons', ev("document.querySelectorAll('#iesh .dok').length") == 12 and ev("document.querySelectorAll('#iesh .dno').length") == 2 and '+ mitigate' in pg.inner_text('#iesh'))
    pg.evaluate("document.querySelector('#iem .mfs').scrollIntoView()"); pg.screenshot(path='/tmp/iea_dictation.png')
    pg.click('#iesh >> text=+ mitigate'); pg.wait_for_timeout(100); chk('tapping a missed word adds it to the vocabulary with the line as its context', ev("S.ie.words.find(x=>x.w==='mitigate').c").startswith('Today we discuss') and ev("S.ie.words.find(x=>x.w==='mitigate').src") == ev("S.ie.mat[0].id"))
    chk('finishing a dictation ticks today\u2019s Listening plan item', ev("ieDp().L") == 1)
    pg.click('#iesh >> text=Keyingi qator'); pg.wait_for_timeout(300); chk('"Keyingi qator" opens the next line', 'Diktant · 0:06' in pg.inner_text('#iesh') and ev("IDK.i") == 2)
    ev("ieDictClose()"); chk('closing stops the audio', ev("document.getElementById('ieau').paused") is True and not ev("!!document.getElementById('iesh')"))
    # pure diff
    d = lambda a, b: ev("(x)=>{const r=ieDiff(x[0],x[1]);return {pct:r.pct,miss:r.missed,extra:r.extra}}", [a, b])
    chk('diff: perfect answer (case and punctuation ignored) = 100%', d('Hello, World! It is OK.', 'hello world it is ok')['pct'] == 100)
    chk('diff: nothing typed = 0%, everything missed', d('one two three', '')['pct'] == 0 and len(d('one two three', '')['miss']) == 3)
    chk('diff: repeated words are matched in order ("the the" vs one "the" = 50%)', d('the the', 'the')['pct'] == 50)
    chk('diff: extra invented words are counted but do not break the match', d('a b c', 'a x b y c')['pct'] == 100 and d('a b c', 'a x b y c')['extra'] == 2)
    chk('diff: apostrophes and numbers are words (don\u2019t, 2025)', d("I don't know 2025", "i don't know 2025")['pct'] == 100)
    ev("ieMatClose()")
    # no audio -> no dictation button
    ev("()=>{S.ie.mat=[{id:9,t:'Text only',k:'p',x:'',c:[[0,3,'Hello and welcome to the show today.'],[3,6,'Now we begin the first section.']],au:0,d:dk()}];IVW='a';render();ieMatOpen(9)}"); pg.wait_for_timeout(400)
    chk('a podcast without audio shows no dictation buttons (only time buttons)', ev("document.querySelectorAll('#iem [aria-label=\"Diktant\"]').length") == 0 and ev("document.querySelectorAll('#iem .iet').length") == 2)
    ev("ieMatClose()")
    # ---------- 6. AI usage meter, context, quick questions ----------
    ev("()=>{window.fnAI=window.__fnAI0;localStorage.setItem('trk_aiu_2026-10-29','5');localStorage.setItem('trk_aiu_'+dk(),'0');window.fnPost=async b=>({text:'{}'})}")
    ev("fnAI({action:'plan'})"); ev("fnAI({action:'reading'})")
    chk('every successful AI call is counted today (2 calls = "AI: 2/40")', ev("aiUsed()") == 2 and ev("aiUseLabel()") == 'AI: 2/40 bugun' and ev("aiLeft()") == 38)
    chk('old days\u2019 counters are cleaned up automatically', ev("localStorage.getItem('trk_aiu_2026-10-29')") is None)
    ev("()=>{localStorage.setItem('trk_aiu_'+dk(),'40')}"); chk('at 40 the remaining count is 0 (never negative)', ev("aiLeft()") == 0)
    ev("()=>{S.ai=undefined;aiS();aiBuild();aiRender()}"); chk('the chat header shows the usage', 'AI: 40/40 bugun' in pg.inner_text('#aisub'))
    ev("aiClose()")
    ev("""()=>{aiS().sh={core:1,quran:1,study:1,health:1,money:0};S.q.m={1:10};S.q.ord=[1];S.q.ppd=3;S.ie.words=Array.from({length:30},(_,i)=>({id:i,w:'w'+i,m:'m',box:i<10?4:0,due:'2099-01-01',t:1}));S.ie.tests=[{id:1,d:dk(),k:'W',b:{W:6},fb:{errors:[{o:'make a research',c:'do research',t:'collocation'}]}}];S.ie.mat=[{id:1,t:'x',k:'a',x:'x',c:[],d:dk()}];S.ie.words[0].src=1;rwReset()}""")
    cx = ev("aiContext()")
    chk('chat context: IELTS readiness with its parts and the next step', 'IELTS tayyorgarlik:' in cx and 'ko‘nikmalar' in cx and 'Tavsiya:' in cx)
    chk('chat context: the student\u2019s real mistakes (type counts and the latest ones)', 'collocation 1' in cx and '“make a research” → “do research”' in cx)
    chk('chat context: exact hifz numbers (memorised, remaining, days, week, today, juz)', 'Hifz (aniq hisob): yodlangan 10/' in cx and 'bet qoldi' in cx and 'to‘liq juz’lar' in cx and 'bugungi sabaq' in cx)
    chk('chat context: materials and how many words came from them', 'IELTS materiallari: 1 ta' in cx and '1 ta so‘z qo‘shilgan' in cx)
    ev("()=>{aiS().sh={core:1,quran:0,study:0,health:0,money:0}}"); cx2 = ev("aiContext()")
    chk('PRIVACY: with the study and Quran switches off, none of that goes to the AI', 'IELTS tayyorgarlik' not in cx2 and 'Hifz (aniq' not in cx2 and 'make a research' not in cx2)
    ev("()=>{aiS().sh={core:1,quran:1,study:1,health:1,money:0}}")
    chk('quick questions were sharpened (IELTS plan with assessment, mistakes, hifz speed)', all(s in ev("AIQ.join('|')") for s in ['IELTS tayyorgarligimni baholab', 'Xatolarim bo‘yicha', 'Hifz tezligim']))
    chk('no JavaScript errors during the whole run', not errs, errs[:3])
    b.close()
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
