import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Writing: banki, reja, Task 1 grafik, band 8; parafraza; so'z oilasi; eksport. Soat: 2026-10-31 10:00.
import sys, json, re
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
PLAN = {'type': 'opinion', 'ideas': {'for': [{'p': 'Free education widens access', 'why': 'Hamma o‘qiy oladi'}, {'p': 'Graduates earn more and pay taxes', 'why': 'Daromad'}], 'against': [{'p': 'Taxpayers carry the cost', 'why': 'Soliq yuki'}]},
        'outline': {'intro': 'Paraphrase the question and state your opinion.', 'body1': {'point': 'Access to education', 'support': 'Poorer students benefit most.', 'example': 'Germany abolished tuition fees in 2014.'}, 'body2': {'point': 'Cost to the state', 'support': 'Budgets are limited.', 'example': 'Some countries cut other services.'}, 'conclusion': 'Restate the opinion.'},
        'phrases': ['It is widely believed that', 'On balance'], 'tip': 'Savolga to‘g‘ridan-to‘g‘ri javob ber.'}
def CH(t='line', **k):
    c = {'type': t, 'title': 'Internet users', 'unit': '%', 'labels': ['2000', '2005', '2010', '2015'], 'series': [{'name': 'Uzbekistan', 'values': [2, 8, 30, 55]}, {'name': 'Kazakhstan', 'values': [3, 12, 40, 70]}], 'prompt': 'The graph below shows the percentage of internet users. Summarise the information.'}
    if t == 'pie': c['series'] = [{'name': 'Share', 'values': [40, 30, 20, 10]}]
    c.update(k); return c
with Run('y12b') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.aiOk=()=>true;S.ie.words=[];S.ie.mat=[];S.ie.wr=[];S.ie.tests=[];S.ie.dr='';WE.k=2;WE.p='';WE.ch=null;WX.bank=0;WX.plan=0;WX.cb=0;WX.rw=null;WX.pl=null;tab='e';EV='i';IVW='w';render()}""")
    # ---------- topic bank ----------
    t = pg.inner_text('#app'); chk('Writing Task 2 shows "🎲 Mavzular banki" and "✨ Reja va g‘oyalar" (no Band 8 button without a draft)', '🎲 Mavzular banki' in t and '✨ Reja va g‘oyalar' in t and 'Band 8 variant' not in t and '📊 Task 1 grafik' not in t)
    chk('the bank has 6 categories with 5 original Task 2 questions each', ev("Object.keys(WXT).length") == 6 and all(len(v) == 5 for v in ev("Object.values(WXT)")) and all(len(q) > 60 for v in ev("Object.values(WXT)") for q in v))
    pg.click('#app >> text="🎲 Mavzular banki"'); pg.wait_for_timeout(60); chk('opening the bank shows the category chips and the questions of the first category', ev("document.querySelectorAll('#app .goal .seg button').length") == 6 and ev("document.querySelectorAll('#app .goal .row').length") == 5)
    pg.click('#app .goal .seg button >> text="Texnologiya"'); pg.wait_for_timeout(60); chk('switching category lists that category\u2019s questions', 'Social media has changed' in pg.inner_text('#app'))
    pg.click('#app .goal .row >> nth=1'); pg.wait_for_timeout(60); chk('tapping a question makes it the essay topic and closes the bank', 'Many jobs are now done by machines' in ev("WE.p") and not ev("WX.bank") and 'Many jobs are now done' in pg.inner_text('#app'))
    # ---------- plan ----------
    ev("()=>{WE.p='';WX.pl=null;WX.perr=''}"); pg.click('#app >> text="✨ Reja va g‘oyalar"'); pg.wait_for_timeout(60)
    ev("""(p)=>{S.ie.words=Array.from({length:5},(_,i)=>({id:i+1,w:'word'+i+'abc',m:'m',box:0,due:dk(),t:1,k:'w'}));window.__calls=[];window.fnAI=async(b)=>{window.__calls.push(b);return {text:JSON.stringify(window.__r)}};window.__r=p;render()}""", PLAN)
    pg.click('#app >> text="Reja tuz"'); pg.wait_for_timeout(60); chk('a plan without a topic is refused with a message (no request)', 'mavzu yoz' in pg.inner_text('#app') and ev("__calls.length") == 0)
    pg.fill('#wxt', 'Some people think that universities should be free. Do you agree?'); pg.click('#app >> text="Reja tuz"'); pg.wait_for_timeout(300)
    c = ev("__calls"); chk('one request: kind plan with the topic', len(c) == 1 and c[0]['kind'] == 'plan' and c[0]['topic'].startswith('Some people think'))
    t = pg.inner_text('#app'); chk('the result shows the essay type, ideas for and against with Uzbek reasons, the outline with examples, phrases and the tip', 'opinion' in t and 'Free education widens access' in t and 'Taxpayers carry the cost' in t and 'Germany abolished tuition fees' in t and 'On balance' in t and 'to‘g‘ridan-to‘g‘ri' in t)
    chk('the topic is kept as the essay topic', ev("WE.p").startswith('Some people think'))
    chk('your weak vocabulary words are suggested for the essay', ev("document.querySelectorAll('#app .goal .rwch .chip').length") >= 5 and 'zaif so‘zlaring' in pg.inner_text('#app'))
    v = lambda j: ev("(x)=>{try{wxPlanValid(x);return 'ok'}catch(e){return e.message}}", j)
    bad = json.loads(json.dumps(PLAN)); bad['outline']['body2']['point'] = ''; chk('a plan with a missing outline part is refused', 'to‘liq chiqmadi' in v(bad))
    bad = json.loads(json.dumps(PLAN)); bad['ideas'] = {'for': [], 'against': []}; chk('a plan without any ideas is refused', 'to‘liq chiqmadi' in v(bad))
    # ---------- chart validation + drawing ----------
    cv = lambda c: ev("(x)=>{try{const r=chValid(x);return {ok:1,t:r.type,n:r.labels.length}}catch(e){return {err:e.message}}}", c)
    chk('valid line, bar, pie and table data are accepted', all(cv(CH(t)).get('ok') for t in ['line', 'bar', 'pie', 'table']))
    chk('unknown type is refused', 'turini' in cv(CH('radar')).get('err', ''))
    chk('fewer than 3 or more than 8 labels are refused', 'noto‘g‘ri' in cv(CH(labels=['a', 'b'], series=[{'name': 'x', 'values': [1, 2]}])).get('err', '') and 'noto‘g‘ri' in cv(CH(labels=list('abcdefghi'), series=[{'name': 'x', 'values': list(range(9))}])).get('err', ''))
    chk('a series whose length differs from the labels is refused', 'noto‘g‘ri' in cv(CH(series=[{'name': 'x', 'values': [1, 2]}])).get('err', ''))
    chk('negative or non-numeric values are refused', 'noto‘g‘ri' in cv(CH(series=[{'name': 'x', 'values': [1, -2, 3, 4]}])).get('err', '') and 'noto‘g‘ri' in cv(CH(series=[{'name': 'x', 'values': [1, 'a', 3, 4]}])).get('err', ''))
    chk('a pie with two series or a total far from 100 is refused', 'doira' in cv(CH('pie', series=[{'name': 'a', 'values': [50, 50, 0, 0]}, {'name': 'b', 'values': [1, 1, 1, 1]}])).get('err', '') and 'yig‘indisi' in cv(CH('pie', series=[{'name': 'a', 'values': [10, 10, 10, 10]}])).get('err', ''))
    chk('a too short prompt is refused', 'topshiriq' in cv(CH(prompt='Short.')).get('err', ''))
    chk('the data table text (sent to the grader with the topic) lists every label with all series', ev("(x)=>chTable(x)", CH()) == 'Internet users (%):\n2000: Uzbekistan 2, Kazakhstan 3\n2005: Uzbekistan 8, Kazakhstan 12\n2010: Uzbekistan 30, Kazakhstan 40\n2015: Uzbekistan 55, Kazakhstan 70')
    svg = lambda c: ev("(x)=>chSvg(x)", c)
    s = svg(CH('line')); chk('a line chart has one polyline per series, a point per value and axis labels', s.count('<polyline') == 2 and s.count('<circle') == 8 and '2015' in s and 'Uzbekistan' in s and 'viewBox' in s)
    s = svg(CH('bar')); chk('a bar chart has labels x series bars', s.count('<rect') >= 8 + 2 and 'role="img"' in s)
    s = svg(CH('pie')); chk('a pie has one slice per label and a legend with the values', s.count('<path') == 4 and '(40%)' in s)
    s = svg(CH('table')); chk('a table renders as an HTML table with a header row', '<table class="chtb">' in s and s.count('<tr>') == 5 and '<th>Kazakhstan</th>' in s)
    s = svg(CH('line', labels=['<script>x</script>', 'b', 'c', 'd'], title='<img src=x onerror=1>')); chk('labels and titles are escaped (no HTML injection into the chart)', '<script>' not in s and '&lt;script&gt;' in s and '<img' not in s)
    # ---------- chart flow ----------
    ev("()=>{WE.k=2;WE.p='';WX.plan=0;render()}"); pg.click('#app .seg button >> text="Task 1 (20 daq)"'); pg.wait_for_timeout(80)
    chk('on Task 1 the bank is replaced by "📊 Task 1 grafik"', '📊 Task 1 grafik' in pg.inner_text('#app') and 'Mavzular banki' not in pg.inner_text('#app'))
    ev("(c)=>{window.__calls=[];window.__r=c}", CH('line')); pg.click('#app >> text="📊 Task 1 grafik"'); pg.wait_for_timeout(60); pg.click('#app .goal .seg button >> text="Chiziqli"'); pg.click('#app button >> text="Grafik yarat"'); pg.wait_for_timeout(300)
    c = ev("__calls"); chk('one request: kind task1 with the chosen chart type', len(c) == 1 and c[0]['kind'] == 'task1' and c[0]['chart'] == 'line')
    chk('the chart is shown above the essay box and the topic = prompt + data table (so the grader can check accuracy)', ev("!!document.querySelector('#app svg[role=img]')") and 'The graph below shows' in ev("WE.p") and 'Uzbekistan 55' in ev("WE.p") and ev("WE.k") == 1)
    ev("()=>{S.ie.dr='In 2000 internet use was very low in both countries, at two and three percent. By 2015 it had risen sharply to fifty five and seventy percent, and Kazakhstan stayed ahead throughout the whole period.';render()}")
    ev("window.alert=()=>{}"); pg.click('#app >> text="Inshoni saqlash"'); pg.wait_for_timeout(120)
    w = ev("S.ie.wr[S.ie.wr.length-1]"); chk('the saved essay keeps the chart data and the topic with the data; the chart is cleared afterwards', w['k'] == 1 and w['ch']['type'] == 'line' and 'Uzbekistan 55' in w['t'] and ev("WE.ch") is None)
    ev("(c)=>{window.__r=c;WE.k=1;WX.cb=1;render()}", CH('pie', series=[{'name': 's', 'values': [10, 10, 10, 10]}])); pg.click('#app button >> text="Grafik yarat"'); pg.wait_for_timeout(300)
    chk('invalid AI data shows a message and no chart', 'yig‘indisi' in pg.inner_text('#app') and ev("WE.ch") is None)
    ev("(c)=>{window.__r=c;WX.cerr=''}", CH('bar')); pg.click('#app button >> text="Grafik yarat"'); pg.wait_for_timeout(300); ev("wK(2)"); chk('switching to Task 2 removes the chart and its topic', ev("WE.ch") is None and ev("WE.p") == '')
    # ---------- band 8 rewrite ----------
    ev("()=>{WE.k=2;WE.p='Do you agree?';S.ie.dr='In my opinion technology is good for peoples because it make life more easy and people can do many things faster than before.';window.__calls=[];window.__r={rewrite:'In my view, technology is beneficial because it simplifies life and allows people to accomplish a great deal more in less time.',changes:[{o:'good for peoples',n:'beneficial to people',why:'Predlog va ko‘plik'},{o:'make life more easy',n:'simplifies life',why:'Ixcham'}],note:'Aniq misol qo‘sh.'};render()}")
    chk('with a draft of 80+ characters "✨ Band 8 variant" appears', '✨ Band 8 variant' in pg.inner_text('#app'))
    pg.click('#app >> text="✨ Band 8 variant"'); pg.wait_for_timeout(300); c = ev("__calls")
    chk('one request: kind rewrite with the task, the topic and the draft', len(c) == 1 and c[0]['kind'] == 'rewrite' and c[0]['task'] == 2 and c[0]['prompt'] == 'Do you agree?' and c[0]['text'].startswith('In my opinion'))
    t = pg.inner_text('#app'); chk('the result shows the rewrite, each change as old → new with the reason, and the tip', 'In my view, technology is beneficial' in t and 'beneficial to people' in t and 'Predlog va ko‘plik' in t and 'Aniq misol' in t)
    ev("()=>{window.__r={rewrite:'short',changes:[]};WX.rw=null}"); pg.click('#app >> text="✨ Band 8 variant"'); pg.wait_for_timeout(300); chk('a too short AI rewrite is rejected with a message', 'qayta yozmadi' in pg.inner_text('#app'))
    ev("()=>{WX.rerr='';WX.rw=null;S.ie.dr='short';render()}"); chk('the draft is never changed by the rewrite', ev("S.ie.dr") == 'short')
    # ---------- paraphrase ----------
    ov = lambda a, b: ev("(x)=>pzOverlap(x[0],x[1])", [a, b])
    chk('overlap: identical = 100%, unrelated = 0%, common words are ignored, word endings do not matter (mitigated/mitigates)', ov('The council mitigated flooding risks', 'The council mitigated flooding risks') == 1 and ov('The council mitigated flooding risks', 'Dogs enjoy sunny afternoons') == 0 and 0 < ov('The council mitigated flooding risks', 'The authority mitigates floods') < 1)
    ev("""()=>{S.ie.mat=[{id:1,t:'T',k:'a',x:'Many people prefer to live in big cities because there are more jobs and better schools available there for everyone. Short one.',c:[],au:0,d:dk()}];PZ={orig:'',ans:'',busy:0,err:'',res:null};S.ie.pz=[];IVW='x';AXO.p=true;WE.k=2;window.__calls=[];window.__r={meaning:true,ok:true,better:'A large number of individuals choose urban life for its opportunities.',note:'Yaxshi: tuzilma o‘zgargan.'};render()}""")
    pg.click('#app >> text="🎲 Materialdan gap"'); pg.wait_for_timeout(60); chk('a sentence of 8-30 words is taken from the materials (the 2-word one is skipped)', 'Many people prefer to live in big cities' in pg.inner_text('#app') and 'Short one' not in ev("PZ.orig"))
    pg.fill('#app textarea >> nth=-1', 'Cities'); ev("PZ.ans='Cities'"); pg.click('#app >> text="Tekshirish"'); pg.wait_for_timeout(60); chk('a variant under 5 words is refused locally', 'Kamida 5 so‘zli' in pg.inner_text('#app') and ev("__calls.length") == 0)
    ev("()=>{PZ.ans='Many people prefer to live in big cities because there are more jobs and better schools available there.';render()}"); ev("window.confirm=()=>false"); pg.click('#app >> text="Tekshirish"'); pg.wait_for_timeout(60)
    chk('a variant that copies most of the words asks for confirmation; cancelling sends nothing', ev("__calls.length") == 0)
    ev("()=>{PZ.ans='A large number of individuals choose urban life for its opportunities.';render()}"); pg.click('#app >> text="Tekshirish"'); pg.wait_for_timeout(300); c = ev("__calls")
    chk('one request: kind para with the original and the student\u2019s variant', len(c) == 1 and c[0]['kind'] == 'para' and c[0]['orig'].startswith('Many people') and c[0]['para'].startswith('A large number'))
    t = pg.inner_text('#app'); chk('the verdict, the overlap percentage, the AI note and a band 7+ variant are shown', '✅ Yaxshi paraphrase' in t and '% i takrorlangan' in t and 'tuzilma o‘zgargan' in t and 'urban life' in t and ev("S.ie.pz.length") == 1)
    ev("()=>{window.__r={meaning:false,ok:false,better:'',note:'Ma’no o‘zgardi.'};PZ.res=null}"); pg.click('#app >> text="Tekshirish"'); pg.wait_for_timeout(300); chk('a variant that changes the meaning is flagged', '✗ Ma’no o‘zgarib ketgan' in pg.inner_text('#app'))
    # ---------- word family ----------
    WF = {'forms': [{'pos': 'n', 'w': 'sustainability'}, {'pos': 'v', 'w': 'sustain'}, {'pos': 'adj', 'w': 'sustainable'}, {'pos': 'xx', 'w': 'ignored-pos'}], 'colloc': [{'p': 'sustainable development', 'ex': 'We need sustainable development.'}, {'p': 'sustain growth', 'ex': ''}], 'syn': ['maintain', 'support'], 'note': 'Predlogsiz: sustain growth.'}
    ev("""(w)=>{S.ie.words=[{id:7,w:'sustain',m:'qo‘llab-quvvatlamoq',u:'qo‘llab-quvvatlamoq',box:0,due:dk(),t:0,k:'w'},{id:8,w:'If I had known',m:'x',u:'x',k:'g',gn:'Third conditional',box:0,due:dk(),t:0}];S.ie.gm={};window.__calls=[];window.__r=w;IR=1;IRM='f';IVW='l';render()}""", WF)
    pg.wait_for_timeout(100); chk('the revealed card offers "📚 Shakllari va kollokatsiyalari"', '📚 Shakllari va kollokatsiyalari' in pg.inner_text('#app .hero'))
    pg.click('#app .hero >> text=📚 Shakllari'); pg.wait_for_timeout(300); c = ev("__calls"); chk('one request: kind wfam with the word', len(c) == 1 and c[0]['kind'] == 'wfam' and c[0]['word'] == 'sustain')
    w = ev("S.ie.words[0].wf"); chk('forms, collocations, synonyms and the note are stored; an unknown part of speech is cleaned', len(w['f']) == 4 and w['f'][3]['pos'] == '' and len(w['c']) == 2 and w['s'] == ['maintain', 'support'] and w['n'].startswith('Predlogsiz'))
    t = pg.inner_text('#app .hero'); chk('the card now shows the forms (n/v/adj), collocations with examples, synonyms and the warning; the button is gone', 'n: sustainability' in t and 'sustainable development' in t and 'We need sustainable development.' in t and 'Sinonim: maintain, support' in t and 'Predlogsiz' in t and '📚' not in t)
    ev("()=>{S.ie.words.reverse();IR=1;render()}"); chk('grammar cards never get the button', '📚' not in pg.inner_text('#app .hero'))
    ev("()=>{S.ie.words.reverse();S.ie.words[0].wf=undefined;window.fnAI=async()=>{throw new Error('Bugungi limit tugadi.')};IR=1;render()}"); pg.click('#app .hero >> text=📚 Shakllari'); pg.wait_for_timeout(300); chk('an AI error is shown on the card', 'Bugungi limit tugadi' in pg.inner_text('#app .hero'))
    ev("()=>{window.aiOk=()=>false;WFE='';render()}"); chk('not signed in: no button', '📚' not in pg.inner_text('#app .hero')); ev("window.aiOk=()=>true")
    # ---------- export ----------
    ev("""()=>{S.ie.words=[{id:1,w:'mitigate',m:'yumshatmoq',u:'yumshatmoq',d:'make less severe',e:'Trees "mitigate" heat.',c:'The plan\\tmitigated\\nthe risk.',lv:'C1',k:'w',box:0,due:dk(),t:1,wf:{f:[],c:[{p:'mitigate risk',ex:''}],s:[],n:''}},
      {id:2,w:'on the other hand',m:'boshqa tomondan',u:'boshqa tomondan',d:'in contrast',e:'',c:'',lv:'B2',k:'c',box:4,due:dk(),t:1},{id:3,w:'If the council had acted',m:'x',u:'Shart',d:'If + past perfect',e:'If I had known <b>.',c:'',lv:'C1',k:'g',gn:'Third conditional',box:1,due:dk(),t:1},{id:4,w:'<script>alert(1)</script>',m:'x',u:'x',lv:'',k:'w',box:5,due:dk(),t:1}];EXS='a';IVW='l';GM=null;render()}""")
    tsv = ev("exTsv(S.ie.words)").split('\n'); chk('Anki file: one line per word, three tab-separated fields (word, back, tags)', len(tsv) == 4 and all(l.count('\t') == 2 for l in tsv), tsv)
    f = tsv[0].split('\t'); chk('the back holds the Uzbek meaning, the definition, the example and the context; tabs/newlines inside fields become spaces; collocations are added', f[1] == 'yumshatmoq<br>make less severe<br><i>Trees &quot;mitigate&quot; heat.</i><br>The plan mitigated the risk.<br>Kollokatsiya: mitigate risk' and '\n' not in f[1], f[1])
    chk('tags carry the level and the kind (word / chunk / grammar)', f[2] == 'IELTS C1 word' and tsv[1].split('\t')[2] == 'IELTS B2 chunk' and tsv[2].split('\t')[2] == 'IELTS C1 grammar' and tsv[3].split('\t')[2] == 'IELTS word')
    chk('grammar cards start with their bold name; HTML in the data is escaped', tsv[2].split('\t')[1].startswith('<b>Third conditional</b><br>Shart') and '&lt;b&gt;' in tsv[2] and '<script>' not in tsv[3] and '&lt;script&gt;' in tsv[3])
    csv = ev("exCsv(S.ie.words)"); rows = csv.split('\r\n'); chk('Excel file: UTF-8 BOM, a header with 9 columns and one CRLF-separated row per word', csv.startswith('\ufeff"So‘z"') and len(rows) == 5 and rows[0].count('","') == 8, rows[0])
    chk('CSV quotes are doubled and newlines/tabs removed', '"Trees ""mitigate"" heat."' in rows[1] and '\n' not in rows[1] and '\t' not in rows[1] and rows[1].endswith('"mitigate risk"'))
    ev("EXS='n';render()"); chk('"O‘rganilmaganlar" exports only words below box 4 (2 of 4)', len(ev("exWords()")) == 2 and 'O‘rganilmaganlar (2)' in pg.inner_text('#app'))
    ev("EXS='a';render()")
    with pg.expect_download() as dl: pg.click('#app >> text="Anki (matn fayli)"')
    d = dl.value; chk('the Anki button downloads "ielts-lugat-<date>.txt" with exactly that content', d.suggested_filename == 'ielts-lugat-2026-10-31.txt' and open(d.path(), encoding='utf-8').read() == ev("exTsv(S.ie.words)"), d.suggested_filename)
    with pg.expect_download() as dl: pg.click('#app >> text="Excel (CSV)"')
    d = dl.value; chk('the Excel button downloads a .csv', d.suggested_filename == 'ielts-lugat-2026-10-31.csv' and open(d.path(), encoding='utf-8').read().startswith('\ufeff'))
    pg.click('#app >> text="🖨 Chop etish"'); pg.wait_for_timeout(80); chk('"Chop etish" opens a clean printable table with every word (buttons are hidden on paper)', ev("!!document.getElementById('prn')") and ev("document.querySelectorAll('#prn tr').length") == 5 and ev("!!document.querySelector('#prn .noprint')") and '<script>' not in ev("document.getElementById('prn').innerHTML"))
    ev("exPrintClose()"); chk('closing removes it', not ev("!!document.getElementById('prn')"))
    ev("()=>{S.ie.words=[];render()}"); pg.click('#app >> text="🖨 Chop etish"'); chk('with no words the export buttons say so', 'uchun so‘z yo‘q' in pg.inner_text('body') and not ev("!!document.getElementById('prn')"))
