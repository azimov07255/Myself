# IELTS: B1 + grammar tahlili, darajalar, hammasini qo'shish/bekor qilish, bulutdagi audio, tahrirlash (✏️), qator tuzatish. Soat: 2026-10-31 10:00.
import sys, os, shutil, json, struct, http.server, threading, socketserver, functools, datetime
from playwright.sync_api import sync_playwright
OUT = '/mnt/user-data/outputs'; SITE = '/tmp/site_ied'
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
       "Residents, who had been waiting for years, were reluctant to accept higher taxes. Never before had the authorities invested so heavily in sustainable drainage.")
AN = {'level': 'B2', 'topic': 'urban floods',
 'words': [{'w': 'argue', 'f': 'argued', 'pos': 'v', 'lv': 'B1', 'def': 'say that something is true', 'uz': 'bahslashmoq', 'ctx': 'The plan mitigated the risk of flooding in low-lying districts, although critics argued that the scheme was far too expensive.', 'ex': 'He argued with me.'},
           {'w': 'expensive', 'f': 'expensive', 'pos': 'adj', 'lv': 'B1', 'def': 'costing a lot', 'uz': 'qimmat', 'ctx': '', 'ex': 'It is expensive.'},
           {'w': 'scheme', 'f': 'scheme', 'pos': 'n', 'lv': 'B2', 'def': 'a plan', 'uz': 'reja', 'ctx': '', 'ex': 'The scheme failed.'},
           {'w': 'reluctant', 'f': 'reluctant', 'pos': 'adj', 'lv': 'B2', 'def': 'unwilling', 'uz': 'istamaydigan', 'ctx': '', 'ex': 'He was reluctant.'},
           {'w': 'avoid', 'f': 'avoided', 'pos': 'v', 'lv': 'B2', 'def': 'keep away from', 'uz': 'qochmoq', 'ctx': '', 'ex': 'Avoid the traffic.'},
           {'w': 'mitigate', 'f': 'mitigated', 'pos': 'v', 'lv': 'C1', 'def': 'make less severe', 'uz': 'yumshatmoq', 'ctx': '', 'ex': 'Trees mitigate heat.'},
           {'w': 'drainage', 'f': 'drainage', 'pos': 'n', 'lv': 'C2', 'def': 'water removal system', 'uz': 'drenaj', 'ctx': '', 'ex': 'Drainage is poor.'},
           {'w': 'unicorn', 'f': 'unicorn', 'pos': 'n', 'lv': 'C1', 'def': 'x', 'uz': '', 'ctx': '', 'ex': ''}],
 'chunks': [{'p': 'higher taxes', 'k': 'collocation', 'lv': 'B1', 'def': 'bigger tax', 'uz': 'yuqori soliq', 'ctx': '', 'ex': 'We pay higher taxes.'},
            {'p': 'far too expensive', 'k': 'phrase', 'lv': 'B2', 'def': 'much too costly', 'uz': '', 'ctx': '', 'ex': 'It is far too expensive.'},
            {'p': 'low-lying districts', 'k': 'collocation', 'lv': 'C1', 'def': 'areas near sea level', 'uz': '', 'ctx': '', 'ex': 'Low-lying districts flood.'}],
 'grammar': [{'p': 'If the council had acted earlier, the city would have avoided', 'g': 'Third conditional', 'lv': 'C1', 'def': 'If + past perfect, would have + V3', 'uz': 'O‘tmishdagi bajarilmagan shart', 'ctx': 'If the council had acted earlier, the city would have avoided the worst flooding.', 'ex': 'If I had known, I would have come.'},
             {'p': 'Never before had the authorities invested', 'g': 'Negative inversion', 'lv': 'C2', 'def': 'Never before + auxiliary + subject + V3', 'uz': 'Inversiya', 'ctx': '', 'ex': 'Never had I seen it.'},
             {'p': 'who had been waiting for years', 'g': '', 'lv': 'B2', 'def': 'past perfect continuous', 'uz': '', 'ctx': '', 'ex': ''},
             {'p': 'a structure that is not in the text at all', 'g': 'Fake', 'lv': 'C1', 'def': '', 'uz': '', 'ctx': '', 'ex': ''},
             {'p': 'too short', 'g': 'Short', 'lv': 'B1', 'def': '', 'uz': '', 'ctx': '', 'ex': ''}]}
FAKE = """()=>{window.__st={};window.__cl=[];const bk={upload:async(p,b,o)=>{__cl.push(['up',p,o&&o.contentType,b.size]);__st[p]=b;return {error:null}},download:async p=>{__cl.push(['dl',p]);return __st[p]?{data:__st[p],error:null}:{data:null,error:{message:'not found'}}},remove:async a=>{__cl.push(['rm',...a]);a.forEach(p=>delete __st[p]);return {error:null}}};window.__sb={storage:{from:n=>{__cl.push(['bucket',n]);return bk}}};UID='u1'}"""
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o');if(localStorage.getItem('trk_sgr')===null)localStorage.setItem('trk_sgr','a');if(localStorage.getItem('trk_ptb')===null)localStorage.setItem('trk_ptb','a')}catch(e){}"); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.clock.install(time=datetime.datetime(2026, 10, 31, 10, 0, 0))
    pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') or r.request.url.startswith('data:') or r.request.url.startswith('blob:') else r.abort())
    pg.goto(f'http://127.0.0.1:{PORT}/index.html'); pg.wait_for_timeout(600)
    pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())"); ev = pg.evaluate
    ev("()=>{S.ob=1;S.ts=1;S.ie.words=[];S.ie.mat=[];S.ie.minlv=undefined;window.ieSay=t=>0;window.__fnAI0=fnAI;tab='e';EV='i';IVW='a';render()}")
    # ---------- 1. validation of the AI answer ----------
    res = ev("(x)=>{const r={words:[],chunks:[],grammar:[],lv:'',topic:''};ieMerge(r,x[1],x[0]);return r}", [TXT, AN])
    chk('B1 words are accepted now (argue B1, expensive B1) together with B2, C1 and C2', [w['lv'] for w in res['words']] == ['B1', 'B1', 'B2', 'B2', 'B2', 'C1', 'C2'] and 'unicorn' not in [w['w'] for w in res['words']], [(w['w'], w['lv']) for w in res['words']])
    chk('chunks keep their level too (B1, B2, C1)', [c['lv'] for c in res['chunks']] == ['B1', 'B2', 'C1'] and len(res['chunks']) == 3)
    g = res['grammar']
    chk('grammar: only structures that really occur in the text (3 kept; the invented one and the 2-word one are dropped)', [x['g'] for x in g] == ['Third conditional', 'Negative inversion', 'Grammar'], [(x['p'], x['g']) for x in g])
    chk('grammar items keep the formula, the Uzbek note, level and example; a missing name becomes "Grammar"', g[0]['def'] == 'If + past perfect, would have + V3' and g[0]['uz'].startswith('O‘tmish') and g[0]['lv'] == 'C1' and g[1]['ex'] == 'Never had I seen it.' and g[2]['g'] == 'Grammar')
    chk('an invented context sentence is blanked, a real one kept', g[0]['ctx'].startswith('If the council') and g[1]['ctx'] == '')
    r2 = ev("(x)=>{const r={words:[],chunks:[],lv:'',topic:''};ieMerge(r,{words:[{w:'drainage',f:'drainage',lv:'A1'},{w:'scheme',f:'scheme',lv:'B3'}],grammar:'nonsense'},x);return r}", TXT)
    chk('bad levels (A1, B3) are cleaned to empty; a malformed grammar field does not crash; an analysis object without "grammar" gets one', r2['words'][0]['lv'] == '' and r2['words'][1]['lv'] == '' and r2['grammar'] == [])
    # ---------- 2. analysis request + level selector ----------
    ev("""(a)=>{S.ie.mat=[{id:70,t:'Floods',k:'a',x:a,c:[],au:0,d:dk(),an:null}];window.__calls=[];window.fnAI=async(b)=>{window.__calls.push(b);return {text:window.__ans}};window.__ans=JSON.stringify(%s);IVW='a';render();ieMatOpen(70)}""" % json.dumps(AN), TXT); pg.wait_for_timeout(400)
    chk('the reader offers the level choice (B1 / B2 / C1 and above), B1 selected by default', 'B1+' in pg.inner_text('#iem') and ev("document.querySelector('#iem .chip.on').textContent") == 'B1+')
    pg.click('#iem .chip >> text="B2+"'); pg.wait_for_timeout(100); chk('choosing a level is remembered', ev("S.ie.minlv") == 'B2' and ev("document.querySelector('#iem .chip.on').textContent") == 'B2+')
    pg.click('#iem .chip >> text="B1+"'); pg.click('#iem >> text=AI bilan tahlil'); pg.wait_for_timeout(500)
    chk('the request carries the chosen minimum level and the text', ev("__calls.length") == 1 and ev("__calls[0].min") == 'B1' and ev("__calls[0].mode") == 'analyze')
    an = ev("S.ie.mat[0].an"); chk('result saved with 7 words, 3 chunks, 3 grammar structures', len(an['words']) == 7 and len(an['chunks']) == 3 and len(an['grammar']) == 3)
    chk('header counts include grammar', '7 so‘z · 3 chunk · 3 grammar' in pg.inner_text('#iems'), pg.inner_text('#iems'))
    # ---------- 3. results: filters, select all, add all, undo ----------
    ev("()=>{IMSEL={_o:1};ieMatDraw()}"); pg.wait_for_timeout(100)
    chips = ev("[...document.querySelectorAll('#iem .iesum .seg button')].map(b=>b.textContent)"); chk('filter chips: Hammasi, B1, B2, C1, C2, Chunklar, Grammar', chips == ['Hammasi', 'B1', 'B2', 'C1', 'C2', 'Chunklar', 'Grammar'], chips)
    rows = lambda: ev("document.querySelectorAll('#iem .ierow').length")
    chk('"Hammasi" lists words, chunks and grammar (7 + 3 + 3 = 13)', rows() == 13)
    for lab, cnt in [('B1', 3), ('B2', 5), ('C1', 3), ('C2', 2), ('Chunklar', 3), ('Grammar', 3)]:
        pg.click('#iem .iesum .seg button >> text="%s"' % lab); pg.wait_for_timeout(80)
        chk('filter %s shows %d rows' % (lab, cnt), rows() == cnt, rows())
    pg.click('#iem .iesum .seg button >> text="Hammasi"'); pg.wait_for_timeout(80)
    t = pg.inner_text('#iem .iesum'); chk('rows show the title, level, kind and the Uzbek meaning / grammar name', 'Third conditional' in t and 'bahslashmoq' in t and 'xavfni' not in t and 'grammar' in t and 'chunk' in t)
    chk('a colour legend explains the levels', ev("document.querySelectorAll('#iem .iesum .lgd').length") == 4)
    pg.click('#iem >> text=Hammasini belgilash'); pg.wait_for_timeout(100); chk('"☑ Hammasini belgilash" ticks every visible new item', ev("document.querySelectorAll('#iem .ierow input:checked').length") == 13 and 'Tanlanganlarni qo‘shish (13)' in pg.inner_text('#iem'))
    pg.click('#iem >> text=Tozalash'); pg.wait_for_timeout(100); chk('"☐ Tozalash" clears the ticks', ev("document.querySelectorAll('#iem .ierow input:checked').length") == 0)
    pg.click('#iem .iesum .seg button >> text="C1"'); pg.click('#iem >> text=Hammasini belgilash'); pg.click('#iem .iesum .seg button >> text="Hammasi"'); pg.wait_for_timeout(100)
    chk('select-all respects the active filter (only the 3 C1 items were ticked)', ev("document.querySelectorAll('#iem .ierow input:checked').length") == 3)
    ev("()=>{IMSEL={_o:1};ieMatDraw()}")
    pg.click('#iem .iesum .seg button >> text="B1"'); pg.wait_for_timeout(80); chk('the add-all button shows how many NEW items are visible (B1: 3)', '⚡ Ko‘ringanlarning hammasini qo‘shish (3)' in pg.inner_text('#iem'))
    pg.click('#iem >> text=Ko‘ringanlarning hammasini'); pg.wait_for_timeout(200)
    w = ev("S.ie.words.map(x=>[x.w,x.k,x.lv])"); chk('add-all adds ONLY what the filter shows (B1: argue, expensive, higher taxes; ...)', len(w) == 3 and sorted(x[0] for x in w) == ['argue', 'expensive', 'higher taxes'], w)
    chk('items are stored with their kind, level and the source material', all(x['src'] == 70 for x in ev("S.ie.words")) and ev("S.ie.words.find(x=>x.w==='higher taxes').k") == 'c' and ev("S.ie.words.find(x=>x.w==='argue').lv") == 'B1')
    chk('rows already in the vocabulary are ticked and disabled; the add-all counter drops to 0 for this filter', ev("document.querySelectorAll('#iem .ierow.hv input:disabled').length") == 3 and ev("[...document.querySelectorAll('#iem .iesum .big')].find(b=>b.textContent.includes('hammasini')).disabled") is True and '(0)' in pg.inner_text('#iem .iesum'))
    chk('an "undo" button appears with the count', '↩ Oxirgi 3 ta qo‘shilganni bekor qilish' in pg.inner_text('#iem'))
    ev("()=>{S.ie.words.find(x=>x.w==='argue').t=Date.now()}"); pg.click('#iem >> text=Bekor qilish'); pg.wait_for_timeout(150)
    chk('undo removes only items not studied yet (2 removed, "argue" which was already answered stays)', [x['w'] for x in ev("S.ie.words")] == ['argue'] and 'Oxirgi' not in pg.inner_text('#iem .iesum').split('Tanlanganlarni')[-1])
    pg.click('#iem .iesum .seg button >> text="Hammasi"'); pg.click('#iem >> text=Ko‘ringanlarning hammasini'); pg.wait_for_timeout(200)
    k = {x['k']: 0 for x in ev("S.ie.words")}; ws = ev("S.ie.words")
    chk('"Hammasi" + add-all adds everything not yet there (13 items in total, none twice)', len(ws) == 13 and len(set(x['w'].lower() for x in ws)) == 13, len(ws))
    gw = next(x for x in ws if x['k'] == 'g' and x['gn'] == 'Third conditional')
    chk('grammar items: the example fragment is the word, with the name, formula, Uzbek note, example, context and level', gw['w'].startswith('If the council had acted') and gw['d'] == 'If + past perfect, would have + V3' and gw['u'].startswith('O‘tmish') and gw['e'] == 'If I had known, I would have come.' and gw['lv'] == 'C1' and gw['box'] == 0 and gw['t'] == 0, gw)
    ev("ieUndoAdd()"); chk('undo again after the second batch removes the whole batch (all new, 12)', len(ev("S.ie.words")) == 1)
    ev("ieAddAll()"); ev("IMU=null;ieMatDraw()"); chk('the undo button disappears when the batch is forgotten', 'Oxirgi' not in pg.inner_text('#iem .iesum'))
    # ---------- 4. marks in the text ----------
    ev("()=>{S.ie.words=[];ieMatDraw()}"); pg.wait_for_timeout(100)
    chk('words are underlined in the colour of their level (lvB1/lvB2/lvC1/lvC2 classes)', all(ev("document.querySelectorAll('#iem mark.mw2.lv%s').length" % l) >= 1 for l in ['B1', 'B2', 'C1', 'C2']) and ev("document.querySelectorAll('#iem mark.mc.lvB1').length") >= 1)
    chk('words inside a grammar structure get a purple tint and still stay tappable', ev("document.querySelectorAll('#iem .iew.gtx').length") >= 8 and ev("document.querySelectorAll('#iem mark.gtx').length") >= 1)
    pg.click('#iem .iew.gtx >> text="council"'); pg.wait_for_timeout(120); t = pg.inner_text('#iesh')
    chk('tapping a plain word inside a grammar structure opens the grammar card: name, formula, Uzbek note, example, level', 'Third conditional' in t and 'If + past perfect' in t and 'bajarilmagan shart' in t and 'If I had known' in t and 'C1' in t and 'Lug‘atga qo‘shish' in t, t)
    chk('the card also offers to explain that single word', '“council” so‘zini izohlash' in t)
    pg.click('#iesh >> text=Lug‘atga qo‘shish'); pg.wait_for_timeout(150); chk('adding the grammar structure from the card works (k = g)', ev("S.ie.words.find(x=>x.k==='g')&&S.ie.words.find(x=>x.k==='g').gn") == 'Third conditional')
    ev("()=>{window.fnAI=async(b)=>{window.__calls.push(b);return {text:JSON.stringify({w:'council',pos:'n',lv:'B2',def:'a group of people who govern a town',uz:'kengash',ex:'The council met.'})}}}")
    pg.click('#iem .iew.gtx >> text="council"'); pg.click('#iesh >> text=so‘zini izohlash'); pg.wait_for_timeout(120); chk('"izohlash" switches to the normal word flow (ask the AI, with the sentence)', 'AI dan ma’nosini so‘rash' in pg.inner_text('#iesh') and 'If the council had acted' in pg.inner_text('#iesh'))
    ev("ieSheetClose()")
    pg.click('#iem mark.mw2.gtx >> text="avoided"'); pg.wait_for_timeout(100); chk('tapping a marked word that lies INSIDE a grammar structure opens the WORD card (not the grammar card)', 'avoid' in pg.inner_text('#iesh') and 'qochmoq' in pg.inner_text('#iesh') and 'Third conditional' not in pg.inner_text('#iesh')); ev("ieSheetClose()")
    ev("()=>{S.ie.words=[{id:5,w:'scheme',m:'reja',box:0,due:dk(),t:0}];ieMatDraw()}"); chk('a word already in the vocabulary is green whatever its level (green beats the level colour)', ev("getComputedStyle(document.querySelector('#iem mark.mw2.hv')).borderBottomColor") == 'rgb(93, 187, 99)', ev("getComputedStyle(document.querySelector('#iem mark.mw2.hv')).borderBottomColor"))
    ev("()=>{S.ie.mat[0].an.grammar=undefined;ieMatDraw()}"); chk('an old analysis without a grammar field still renders (no crash)', ev("document.querySelectorAll('#iem mark').length") >= 3 and 'grammar' in pg.inner_text('#iems'))
    ev("()=>{S.ie.mat[0].an.grammar=%s;ieMatDraw()}" % json.dumps(AN['grammar'][:3]))
    pg.evaluate("document.querySelectorAll('canvas').forEach(c=>c.remove());document.querySelector('#iem .iesum').open=true;document.querySelector('#iem .mfp').scrollTo(0,0)"); ev("()=>{IMSEL={_o:1};ieMatDraw()}"); pg.screenshot(path='/tmp/ied_results.png')
    ev("ieMatClose()")
    # ---------- 5. vocabulary cards and filters ----------
    ev("""()=>{S.ie.words=[{id:1,w:'If the council had acted earlier, the city would have avoided',m:'x',u:'Bajarilmagan shart',d:'If + past perfect, would have + V3',e:'If I had known, I would have come.',c:'If the council had acted earlier, the city would have avoided the worst flooding.',lv:'C1',k:'g',gn:'Third conditional',box:0,due:dk(),t:0},
      {id:2,w:'argue',m:'bahslashmoq',lv:'B1',k:'w',box:0,due:dk(),t:0},{id:3,w:'mitigate',m:'yumshatmoq',lv:'C1',k:'w',box:3,due:'2099-01-01',t:1},{id:4,w:'higher taxes',m:'soliq',lv:'B1',k:'c',box:2,due:'2099-01-01',t:1},{id:5,w:'drainage',m:'drenaj',lv:'C2',k:'w',box:1,due:'2099-01-01',t:1}];IR=0;IRM='z';ILF='a';IVW='l';render()}""")
    pg.wait_for_timeout(120); t = pg.inner_text('#app .hero')
    chk('a grammar card shows the example fragment and "grammar · level" first (even in cloze mode)', 'If the council had acted earlier' in t and 'grammar · C1' in t and 'Third conditional' not in t)
    pg.click('#app .hero >> text=Qaysi tuzilma'); pg.wait_for_timeout(100); t = pg.inner_text('#app .hero')
    chk('revealed: the name, the formula, the Uzbek note and the example', 'Third conditional' in t and 'If + past perfect' in t and 'Bajarilmagan shart' in t and 'If I had known' in t and 'Bildim' in t)
    ev("iAns(1)"); chk('answering a grammar card works like any card', ev("S.ie.words.find(x=>x.k==='g').box") == 1)
    pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); labs = ev("[...document.querySelectorAll('#app .seg.sc button')].map(b=>b.textContent)")
    chk('the vocabulary list has level chips and Grammar', labs[:2] == ['Hammasi', 'Yangi'] and 'B1' in labs and 'C2' in labs and 'Grammar' in labs and 'Chunklar' in labs, labs)
    def lst(lab): pg.click('#app .seg.sc button >> text="%s"' % lab); pg.wait_for_timeout(80); return ev("[...document.querySelectorAll('#app .row .t')].map(x=>x.textContent)")
    chk('list filter B1 -> argue + the B1 chunk', len(lst('B1')) == 2 and any('argue' in x for x in lst('B1')))
    chk('list filter C2 -> drainage only', len(lst('C2')) == 1 and 'drainage' in lst('C2')[0])
    chk('list filter Grammar -> the grammar card with its badge', len(lst('Grammar')) == 1 and 'grammar' in lst('Grammar')[0])
    chk('list filter Chunklar -> higher taxes only', len(lst('Chunklar')) == 1 and 'higher taxes' in lst('Chunklar')[0])
    ev("()=>{IQ=null;ILF='a'}"); ev("S.ie.words.push({id:9,w:'x1',m:'m1',box:0,due:'2099-01-01',t:1},{id:10,w:'x2',m:'m2',box:0,due:'2099-01-01',t:1},{id:11,w:'x3',m:'m3',box:0,due:'2099-01-01',t:1},{id:12,w:'x4',m:'m4',box:0,due:'2099-01-01',t:1})")
    seen = set()
    for _ in range(40): ev("ieQuiz()"); seen.add(str(ev("IQ.w.k")) + ':' + str(ev("IQ.opts.some(o=>o.k==='g')")))
    chk('the word quiz never uses grammar items (neither as question nor as an option)', not any(s.startswith('g') or s.endswith('True') for s in seen), seen)
    # ---------- 6. cloud audio ----------
    ev(FAKE)
    ev("()=>{S.ie.mat=[];S.ie.words=[];IVW='a';IMF.add=1;IMF.mk='p';render()}"); pg.fill('#mt', 'Cloud podcast')
    pg.fill('#mx', ''); pg.set_input_files('#mf2', files=[{'name': 'ep.wav', 'mimeType': 'audio/wav', 'buffer': WAV}]); pg.click('#app >> text=Saqlash va ochish'); pg.wait_for_timeout(1000)
    m = ev("S.ie.mat[0]"); cl = ev("__cl.filter(c=>c[0]==='up')")
    chk('a new podcast audio is uploaded to the private cloud folder of the user: books bucket, <uid>/i/<id>, with its type', len(cl) == 1 and cl[0][1] == 'u1/i/%d' % m['id'] and cl[0][2] == 'audio/wav' and cl[0][3] == len(WAV) and ev("__cl.filter(c=>c[0]==='bucket')[0][1]") == 'books', cl)
    chk('the material is marked as cloud-synced and remembers the size', m['cl'] == 1 and m['sz'] == len(WAV) and m['au'] == 1)
    chk('the cloud meter counts the podcast audio', abs(ev("cloudMB()") - len(WAV) / 1048576) < 0.001)
    ev("ieMatClose()")
    ev("""async()=>{await idbDel('ieau'+S.ie.mat[0].id);window.__cl=[]}""")
    ev("ieMatOpen(S.ie.mat[0].id)"); pg.wait_for_function("document.getElementById('ieau')&&document.getElementById('ieau').readyState>=1", timeout=8000)
    chk('on ANOTHER device (no local copy) opening the material downloads the audio from the cloud and plays it', ev("__cl.filter(c=>c[0]==='dl').length") == 1 and ev("document.getElementById('ieau').duration") > 7, ev("__cl"))
    ev("ieMatClose()"); ev("window.__cl=[]"); ev("ieMatOpen(S.ie.mat[0].id)"); pg.wait_for_function("document.getElementById('ieau')&&document.getElementById('ieau').readyState>=1", timeout=8000)
    chk('...and keeps it on that device: the next time there is no download', ev("__cl.filter(c=>c[0]==='dl').length") == 0)
    ev("ieMatClose()")
    ev("""async()=>{await idbDel('ieau'+S.ie.mat[0].id);delete __st['u1/i/'+S.ie.mat[0].id];window.__cl=[]}""")
    ev("ieMatOpen(S.ie.mat[0].id)"); pg.wait_for_timeout(500); t = pg.inner_text('#iepl')
    chk('if the download fails the player explains it and offers "Audio qo‘shish" (no crash)', 'Audio yuklanmadi' in t and 'Audio qo‘shish' in t, t)
    ev("ieMatClose()")
    # blob missing + cloud -> transcript fetches it
    ev("""async()=>{__st['u1/i/'+S.ie.mat[0].id]=new Blob([new Uint8Array(5000)],{type:'audio/mpeg'});window.__up=[];window.fnUpload=async(f,b,n)=>{window.__up.push({size:b.size,n});return {cues:[{s:0,e:2,t:'Hello there my friend.',w:[]}]}};S.ie.mat[0].c=[];S.ie.mat[0].x='';ieMatOpen(S.ie.mat[0].id)}""")
    pg.wait_for_timeout(500); pg.click('#iem >> text=Transkript qilish'); pg.wait_for_timeout(500)
    chk('the automatic transcript also works when the audio is only in the cloud (it is fetched first)', ev("__up.length") == 1 and ev("__up[0].size") == 5000 and ev("S.ie.mat[0].c.length") == 1, ev("__up"))
    ev("ieMatClose()")
    # cloud full
    ev("""()=>{window.__cl=[];S.qa.list.push({id:'big',cloud:1,sz:300*1048576});S.ie.mat=[];IMF.add=1;IMF.mk='p';IVW='a';render()}"""); pg.fill('#mt', 'Too big for cloud'); pg.set_input_files('#mf2', files=[{'name': 'ep.wav', 'mimeType': 'audio/wav', 'buffer': WAV}]); pg.click('#app >> text=Saqlash va ochish'); pg.wait_for_timeout(800)
    chk('when the cloud is full, the audio stays on this device, nothing is uploaded and the user is told', len(ev("__cl.filter(c=>c[0]==='up')")) == 0 and 'Bulut hajmi to‘lgan' in pg.inner_text('body') and ev("S.ie.mat[0].au") == 1 and not ev("S.ie.mat[0].cl"))
    ev("S.qa.list=S.qa.list.filter(x=>x.id!=='big')")
    ev("ieMatClose()")
    # logged out
    ev("()=>{window.__sb=null;UID=null;S.ie.mat=[];IMF.add=1;IMF.mk='p';IVW='a';render()}"); pg.fill('#mt', 'Offline user'); pg.set_input_files('#mf2', files=[{'name': 'ep.wav', 'mimeType': 'audio/wav', 'buffer': WAV}]); pg.click('#app >> text=Saqlash va ochish'); pg.wait_for_timeout(800)
    chk('not logged in: the audio is kept locally and everything keeps working (no cloud calls, no errors)', ev("S.ie.mat[0].au") == 1 and not ev("S.ie.mat[0].cl") and ev("!!document.getElementById('ieau')"))
    ev("ieMatClose()"); ev(FAKE)
    # delete -> cloud copy removed
    ev("()=>{S.ie.mat=[{id:777,t:'Del',k:'p',x:'',c:[[0,3,'abc def ghi jkl']],au:1,cl:1,sz:100,d:dk(),an:null}];window.__cl=[];window.confirm=()=>true;IVW='a';render()}")
    pg.evaluate("document.querySelector('.iemr .x[aria-label=\"O‘chirish\"]').click()"); pg.wait_for_timeout(150)
    chk('deleting a material also deletes its cloud audio', ev("__cl.filter(c=>c[0]==='rm')") == [['rm', 'u1/i/777']] and ev("S.ie.mat.length") == 0, ev("__cl"))
    # ---------- 7. the ✏️ edit sheet ----------
    ev("""(a)=>{S.ie.mat=[{id:80,t:'Phone podcast',k:'p',x:'',c:[[0,3,'Hello and welcome to the show today.',null],[3,6,'We talk about the weather and rain.',null],[6,8,'Thank you for listening to us.',null]],au:1,cl:1,sz:100,d:dk(),an:null},{id:81,t:'An article',k:'a',x:a,c:[],au:0,d:dk(),an:null}];IVW='a';render()}""", TXT)
    chk('every library row has a ✏️ pencil next to the ✕', ev("document.querySelectorAll('.iemr [aria-label=\"Tahrirlash\"]').length") == 2)
    pg.click('.iemr >> nth=0 >> [aria-label="Tahrirlash"]'); pg.wait_for_timeout(500)
    chk('the pencil in the list opens the reader and the edit sheet at once', ev("!!document.getElementById('iem')") and ev("!!document.getElementById('ied')") and 'Phone podcast' in ev("document.getElementById('edt').value"))
    chk('the sheet says the audio is in the cloud and will be fetched on opening (this device has no copy)', '☁ bulutda' in pg.inner_text('#ied'), pg.inner_text('#ied'))
    # attach audio from the phone through the pencil
    with pg.expect_file_chooser() as fc: pg.click('#ied button >> text="Almashtirish"')
    fc.value.set_files([{'name': 'phone.wav', 'mimeType': 'audio/wav', 'buffer': WAV}]); pg.wait_for_timeout(1200)
    chk('audio picked on the phone is stored locally, uploaded to the cloud, and the player appears at once', ev("S.ie.mat[0].au") == 1 and ev("S.ie.mat[0].cl") == 1 and ev("S.ie.mat[0].sz") == len(WAV) and len(ev("__cl.filter(c=>c[0]==='up')")) == 1 and ev("!!document.getElementById('ieau')"), ev("__cl"))
    chk('the sheet now says it is on this device and in the cloud', '✓ shu qurilmada va bulutda' in pg.inner_text('#ied'))
    pg.fill('#edt', 'Renamed podcast'); pg.click('#ied >> text=Saqlash'); pg.wait_for_timeout(150)
    chk('renaming works and closes the sheet', ev("S.ie.mat[0].t") == 'Renamed podcast' and not ev("!!document.getElementById('ied')") and 'Renamed podcast' in pg.inner_text('#iem'))
    # replace the transcript
    ev("S.ie.mat[0].an={words:[],chunks:[],grammar:[],lv:'B2',topic:'x',n:1,at:dk()}"); ev("ieEdSheet()"); pg.wait_for_timeout(200)
    pg.fill('#edx', 'short'); pg.click('#ied >> text=Saqlash'); pg.wait_for_timeout(100); chk('a transcript that is too short and not subtitles is refused', 'juda qisqa' in pg.inner_text('body') and ev("S.ie.mat[0].c.length") == 3 and ev("!!document.getElementById('ied')"))
    srt = "1\n00:00:00,000 --> 00:00:02,000\nNew first line of the corrected transcript.\n\n2\n00:00:02,000 --> 00:00:05,000\nAnd a second corrected line follows right here."
    pg.fill('#edx', srt); pg.click('#ied >> text=Saqlash'); pg.wait_for_timeout(200)
    chk('pasting new SRT replaces the cues (the AI analysis is cleared because the text changed)', ev("S.ie.mat[0].c.length") == 2 and ev("S.ie.mat[0].c[0][2]") == 'New first line of the corrected transcript.' and ev("S.ie.mat[0].an") is None and ev("S.ie.mat[0].x") == '')
    ev("ieEdSheet()"); pg.wait_for_timeout(150); pg.click('#ied >> text=Saqlash'); pg.wait_for_timeout(100); chk('saving without touching the text keeps everything (cues and analysis are not reset)', ev("S.ie.mat[0].c.length") == 2)
    # per-cue edit
    ev("ieEdSheet()"); pg.wait_for_timeout(150); pg.click('#ied >> text=Transkript qatorlarini tuzatish'); pg.wait_for_timeout(150)
    chk('"qatorlarini tuzatish" shows a ✏️ on every subtitle line', ev("document.querySelectorAll('#iem .iecu [aria-label=\"Qatorni tahrirla\"]').length") == 2 and not ev("!!document.getElementById('ied')"))
    ev("window.prompt=(m,v)=>'  Corrected   by hand  '"); ev("S.ie.mat[0].c[0][3]=[0.1,0.5]"); pg.click('#icu0 [aria-label="Qatorni tahrirla"]'); pg.wait_for_timeout(100)
    chk('editing a line trims it, saves it and drops its old word times (they are recomputed proportionally)', ev("S.ie.mat[0].c[0][2]") == 'Corrected by hand' and ev("S.ie.mat[0].c[0][3]") is None and 'Corrected by hand' in pg.inner_text('#icu0'))
    ev("window.prompt=()=>null"); pg.click('#icu1 [aria-label="Qatorni tahrirla"]'); chk('cancelling the prompt changes nothing', ev("S.ie.mat[0].c[1][2]").startswith('And a second'))
    ev("window.prompt=()=>'   '"); pg.click('#icu1 [aria-label="Qatorni tahrirla"]'); chk('an empty edit is ignored', ev("S.ie.mat[0].c[1][2]").startswith('And a second'))
    ev("IMF.ce=0;ieMatDraw()")
    # audio delete
    ev("window.confirm=()=>true;window.__cl=[]"); ev("ieEdSheet()"); pg.wait_for_timeout(150); pg.click('#ied >> text=Audioni o‘chirish'); pg.wait_for_timeout(500)
    chk('deleting the audio removes the local copy and the cloud copy, resets the flags and the player shows "Audio qo‘shish"', not ev("S.ie.mat[0].au") and not ev("S.ie.mat[0].cl") and ev("__cl.filter(c=>c[0]==='rm').length") == 1 and 'Audio qo‘shish' in pg.inner_text('#iepl'), ev("__cl"))
    # local-only audio can be pushed to the cloud
    ev("ieEdClose()")
    with pg.expect_file_chooser() as fc: pg.click('#iepl >> text=Audio qo‘shish')
    fc.value.set_files([{'name': 'again.wav', 'mimeType': 'audio/wav', 'buffer': WAV}]); pg.wait_for_timeout(1000)
    chk('the "Audio qo‘shish" button of the player attaches a new audio to a podcast that has none', ev("S.ie.mat[0].au") == 1 and ev("!!document.getElementById('ieau')"))
    ev("()=>{S.ie.mat[0].cl=0;ieEdSheet()}"); pg.wait_for_timeout(200); chk('audio only on this device offers "☁ Bulutga yuklash"', '☁ Bulutga yuklash' in pg.inner_text('#ied') and 'bulutga yuklanmagan' in pg.inner_text('#ied'))
    ev("window.__cl=[]"); pg.click('#ied >> text=Bulutga yuklash'); pg.wait_for_timeout(800); chk('and uploads it', ev("S.ie.mat[0].cl") == 1 and len(ev("__cl.filter(c=>c[0]==='up')")) == 1)
    with pg.expect_file_chooser() as fc: pg.click('#ied button >> text="Almashtirish"')
    open('/tmp/huge.mp3', 'wb').truncate(51 * 1048576); fc.value.set_files('/tmp/huge.mp3'); pg.wait_for_timeout(1500)
    chk('an audio over 50 MB (the cloud file limit) is refused with a message and the old audio stays', '50 MB dan katta' in pg.inner_text('body') and ev("S.ie.mat[0].sz") == len(WAV))
    ev("ieEdClose();ieMatClose()")
    # article editing
    pg.click('.iemr >> nth=1 >> [aria-label="Tahrirlash"]'); pg.wait_for_timeout(400)
    chk('an article edit sheet shows the text and has no audio section', ev("document.getElementById('edx').value").startswith('If the council') and 'Audio:' not in pg.inner_text('#ied'))
    ev("S.ie.mat[1].an={words:[],chunks:[],grammar:[],lv:'B2',topic:'x',n:1,at:dk()}")
    pg.fill('#edx', 'too short now'); pg.click('#ied >> text=Saqlash'); pg.wait_for_timeout(100); chk('an article text under 200 characters is refused', 'juda qisqa' in pg.inner_text('body') and ev("S.ie.mat[1].x").startswith('If the council'))
    pg.fill('#edx', TXT + ' One more sentence was added by the user to make the text different.'); pg.click('#ied >> text=Saqlash'); pg.wait_for_timeout(150)
    chk('a changed article text is saved and the old analysis is cleared (word positions would no longer match)', ev("S.ie.mat[1].x").endswith('different.') and ev("S.ie.mat[1].an") is None and 'tahlilni qayta qil' in pg.inner_text('body'))
    ev("ieMatClose()")
    # library list
    ev("""(a)=>{S.ie.words=[{id:1,w:'scheme',m:'x',box:0,due:dk(),t:0}];S.ie.mat=[{id:90,t:'Listed',k:'p',x:'',c:[[0,3,'one two three four five six']],au:1,cl:1,sz:10,d:dk(),an:{words:[{w:'scheme',f:'scheme',lv:'B2',def:'',uz:'',ctx:'',ex:'',pos:''}],chunks:[],grammar:[{p:'a b c',g:'G',lv:'B1',def:'',uz:'',ctx:'',ex:''}],lv:'B2',topic:'x',n:1,at:dk()}}];IVW='a';render()}""", TXT)
    t = pg.inner_text('.iemr'); chk('the library row shows the cloud badge and the counts with grammar and how many are in the vocabulary', 'audio ☁' in t and '1 so‘z, 0 chunk, 1 grammar (1 qo‘shilgan)' in t, t)
    chk('no JavaScript errors during the whole run', not errs, errs[:3])
    b.close()
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
