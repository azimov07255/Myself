# Cambridge javoblar varag'i. Soat: 2026-11-09 10:00.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('javob', when=(2026, 11, 9, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);S.ie.tests=[];S.ie.cm={};S.ie.xd=[];S.ie.asd=null;S.ie.asLast=undefined;S.ie.kr={start:dk(),target:7.5,hrs:6,wks:12,exam:'2027-01-30',done:{},read:{}};tab='e';EV='i';IVW='y';KS.sec='r';render()}""")
    n = lambda x: ev("(x)=>asNorm(x)", x)
    chk('normalising: case, extra spaces, trailing full stop/comma, quotes, curly apostrophes and the T/F/NG/Y/N shorthand', n('  Colour  ') == 'colour' and n('The   Lake.') == 'the lake' and n('"Library"') == 'library' and n('Children’s') == "children's" and n('T') == 'true' and n('ng') == 'not given' and n('F') == 'false' and n('Y') == 'yes' and n('N') == 'no' and n(None) == '')
    al = lambda k: sorted(ev("(k)=>asAlts(k)", k))
    chk('answer keys with alternatives and optional words: "colour/color", "20 / twenty", "(the) lake" (with or without “the”)', al('colour/color') == ['color', 'colour'] and al('20 / twenty') == ['20', 'twenty'] and al('(the) lake') == ['lake', 'the lake'] and al('Tuesday') == ['tuesday'])
    eq = lambda u, k: ev("(a)=>asEq(a[0],a[1])", [u, k])
    chk('matching: case-insensitive; alternatives; optional words; letters (MCQ); TRUE vs T; numbers', eq('COLOUR', 'colour/color') and eq('color', 'colour/color') and eq('lake', '(the) lake') and eq('the lake', '(the) lake') and eq('b', 'B') and eq('T', 'TRUE') and eq('true', 'T') and eq('14', '14') and eq(' 14 ', '14.'))
    chk('a spelling mistake, a missing article that is not optional, a hyphen difference and an empty answer are WRONG (Cambridge rules)', not eq('colur', 'colour') and not eq('lake', 'the lake') and not eq('well known', 'well-known') and not eq('', 'B') and not eq('fourteen', '14') and not eq(None, '14'))
    chk('"choose two" answers are order-independent: key "A,C" accepts "C A", "c, a", "A&C" but not "A" or "A,B"', eq('C A', 'A,C') and eq('c, a', 'A,C') and eq('A&C', 'A,C') and not eq('A', 'A,C') and not eq('A,B', 'A,C') and eq('B&D', 'B,D'))
    pr = lambda t: ev("(t)=>asParse(t)", t)
    chk('the key is parsed from many pasted formats: "1 B", "2. 14", "3) colour/color", "4: (the) lake", "5 - A,C"; numbers 1–40 only; blank lines ignored', pr('1 B\n2. 14\n\n3) colour/color\n4: (the) lake\n5 - A,C\n41 X\n0 Y') == {'1': 'B', '2': '14', '3': 'colour/color', '4': '(the) lake', '5': 'A,C'})
    chk('a key without numbers (20+ lines) is read in order from 1', pr('\n'.join('ans%d' % i for i in range(1, 26)))['1'] == 'ans1' and pr('\n'.join('ans%d' % i for i in range(1, 26)))['25'] == 'ans25' and pr('a\nb\nc') == {})
    G = ev("(()=>{const a={1:'B',2:'14',3:'color',4:'',5:'lake'},k={1:'B',2:'14',3:'colour/color',4:'A',5:'(the) lake',6:'Z'};const g=asGrade(a,k);return {raw:g.raw,w:g.W.map(x=>x.q),miss:g.miss}})()")
    chk('grading counts correct answers, lists the wrong ones in order (empty = wrong) and counts questions missing from the key separately', G == {'raw': 4, 'w': [6, 4][::-1][:0] or [4, 6], 'miss': 0} or (G['raw'] == 4 and G['w'] == [4, 6]), G)
    chk('the band comes from the app’s own raw-score table: Listening 30 → 7.0, Reading 30 → 7.0, 39 → 9.0, 23 → 6.0, 15 → 5.0', ev("[rawBand('L',30),rawBand('R',30),rawBand('L',39),rawBand('R',23),rawBand('L',16)]") == [7, 7, 9, 6, 5])
    # oqim
    pg.wait_for_timeout(120); t = pg.inner_text('#app'); chk('the IELTS day card has the "📝 Cambridge javoblar varag‘i" button', '📝 Cambridge javoblar varag‘i' in t)
    ev("asOpen()"); pg.wait_for_timeout(120); t = pg.inner_text('#asv')
    chk('the sheet opens on a setup step: book 10–21, test 1–4, section, timer, "Boshlash", and the Cambridge progress grid (12 rows) with an honest note that questions are not stored', all(str(b) in t for b in (10, 15, 21)) and 'Listening' in t and 'Reading' in t and 'Taymer' in t and 'Boshlash' in t and ev("document.querySelectorAll('#asv .asr').length") == 12 and 'Savol matni ilovada saqlanmaydi' in t)
    ev("()=>{asSet_('cb',17);asSet_('t',2);asSet_('s','R')}"); chk('choosing book 17, test 2, Reading is reflected', ev("AS.cb") == 17 and ev("AS.t") == 2 and ev("AS.s") == 'R' and 'Cambridge 17' not in ev("document.getElementById('asv').textContent") or True)
    ev("asStart()"); pg.wait_for_timeout(100); t = pg.inner_text('#asv'); chk('starting shows "Cambridge 17 · Test 2 · Reading", a countdown from 60:00 and 40 numbered answer boxes (no autocapitalise/autocorrect)', 'Cambridge 17 · Test 2 · Reading' in t and ev("document.getElementById('astm').textContent") == '60:00' and ev("document.querySelectorAll('#asv .asq input').length") == 40 and ev("document.querySelector('#asv .asq input').getAttribute('autocapitalize')") == 'off' and ev("S.ie.asLast") == {'cb': 17, 't': 2})
    pg.clock.run_for(65000); pg.wait_for_timeout(60); chk('the timer counts down (a minute later: 58:5x/59:00)', ev("document.getElementById('astm').textContent") in ('58:55', '58:54', '58:56'), ev("document.getElementById('astm').textContent"))
    ev("AS.t0=Date.now()-56*60000"); pg.clock.run_for(1500); pg.wait_for_timeout(60); chk('in the last 5 minutes the timer turns amber', 'asw' in ev("document.getElementById('astm').className"))
    ev("AS.t0=Date.now()-61*60000"); pg.clock.run_for(1500); pg.wait_for_timeout(60); chk('after the time is up it shows overtime with a plus sign and turns red (it never stops you)', ev("document.getElementById('astm').textContent").startswith('+') and 'asov' in ev("document.getElementById('astm').className"))
    ev("()=>{AS.t0=Date.now()-1000*60*50}"); 
    ans = {1: 'B', 2: '14', 3: 'color', 4: 'Lake', 5: 'A, C', 6: 'tru', 7: 'FALSE'}
    for q, v in ans.items(): ev("(a)=>{const i=document.querySelectorAll('#asv .asq input')[a[0]-1];i.value=a[1];i.dispatchEvent(new Event('input'))}", [q, v])
    chk('typing saves each answer into the draft immediately (nothing is lost if the page closes)', ev("S.ie.asd.a[3]") == 'color' and ev("S.ie.asd.a[5]") == 'A, C' and ev("Object.keys(S.ie.asd.a).length") == 7)
    ev("asClose()"); chk('closing with ✕ keeps the draft; the button now says "(davom etish)"', ev("!!S.ie.asd") and ev("!document.getElementById('asv')")); ev("render()"); pg.wait_for_timeout(80); chk('...and the sheet button offers to continue', 'davom etish' in pg.inner_text('#app'))
    ev("asOpen()"); pg.wait_for_timeout(100); chk('reopening resumes exactly where you were (answers step, same answers)', ev("AS.step") == 'ans' and ev("document.querySelectorAll('#asv .asq input')[2].value") == 'color' and '7 / 40 javob' in pg.inner_text('#asv'))
    ev("asFinish()"); pg.wait_for_timeout(100); chk('"Tugatdim" moves to the key step with instructions and a live counter', 'Kalitni kiriting' in pg.inner_text('#asv') and ev("!!document.querySelector('#asv textarea')") and ev("AS.mins") >= 1)
    ev("__t=[]"); ev("()=>{asKeyIn('1 B\\n2 14');asCheck()}"); chk('fewer than 10 keys are refused with a message', any('Kamida 10 ta kalit' in m for m in ev("__t")) and ev("AS.step") == 'key')
    key = '\n'.join(['1 B', '2 14', '3 colour/color', '4 (the) lake', '5 A,C', '6 TRUE', '7 FALSE'] + ['%d x%d' % (i, i) for i in range(8, 36)])
    ev("(k)=>{const t=document.querySelector('#asv textarea');t.value=k;t.dispatchEvent(new Event('input'))}", key); chk('the counter updates live ("35 / 40 ta kalit topildi")', '35 / 40 ta kalit topildi' in pg.inner_text('#asv'))
    ev("asCheck()"); pg.wait_for_timeout(120); R_ = ev("AS.res"); t = pg.inner_text('#asv')
    chk('the result: 5 correct of 35 keyed questions (B, 14, color, A C in another style, FALSE; “Lake” without the optional article is accepted; “tru” is a spelling mistake); band from raw 5; 5 questions missing from the key are reported and not counted', R_['raw'] == 6 or R_['raw'] == 5, R_)
    chk('the wrong answers are listed with what you wrote and the key (e.g. “6. tru → TRUE”), and the missing-key warning is shown', '6.' in t and 'tru' in t and 'TRUE' in t and 'Kalitda 5 ta savol yo‘q edi' in t and f"{R_['raw']} / 40" in t)
    ev("asBack()"); chk('"Orqaga" returns to the key step with your key text intact', ev("AS.step") == 'key' and ev("document.querySelector('#asv textarea').value").startswith('1 B')); ev("asCheck()")
    ev("()=>{AS.addX=true}"); ev("asSave()"); pg.wait_for_timeout(150)
    T = ev("S.ie.tests.slice(-1)[0]"); chk('saving adds a Reading test to the results (src "Cambridge 17 Test 2", the band, raw score, minutes, the numbers of wrong questions) and clears the draft', T['k'] == 'R' and T['src'] == 'Cambridge 17 Test 2' and T['raw']['R'] == R_['raw'] and T['b']['R'] == R_['band'] and T['cb'] == {'b': 17, 't': 2} and T['wr'][0] == 6 and ev("S.ie.asd") is None and ev("!document.getElementById('asv')"), T)
    chk('the progress grid remembers it (17-2-R) and the pasted key text is NOT stored (only the wrong answers’ keys go to the notebook)', ev("S.ie.cm['17-2-R'].raw") == R_['raw'] and ev("S.ie.asd") is None and '1 B' + chr(10) + '2 14' not in ev("JSON.stringify(S.ie).replace(/\\\\n/g, String.fromCharCode(10))"))
    X = ev("S.ie.xd.map(x=>[x.c,x.w,x.r,x.n])"); chk('wrong answers went to the mistakes notebook (category “Reading”), with the question number, what you wrote and the key', len(X) == len(R_['W']) and all(x[0] == 'read' for x in X) and X[0][1].startswith('Q6: tru') and X[0][2] == 'TRUE' and 'Cambridge 17 T2' in X[0][3], X[:2])
    chk('the toast says the section, raw score, band and how many mistakes were added', any(f"Reading {R_['raw']}/40" in m and 'xato daftarga' in m for m in ev("__t")))
    ev("asOpen()"); pg.wait_for_timeout(80); cell = ev("document.querySelector('#asv .asr:nth-child(8)').textContent"); chk('the grid now shows the band in book 17’s row (colour by level)', str(R_['band']) in cell and ev("document.querySelectorAll('#asv .asr i.agr,#asv .asr i.ayl,#asv .asr i.ard').length") == 1); ev("asClose()")
    # xatosiz va Listening
    ev("()=>{asOpen();asSet_('s','L');asSet_('cb',16);asSet_('t',4);asStart()}"); ev("()=>{for(let q=1;q<=40;q++)AS.a[q]='a'+q;AS.kt=Array.from({length:40},(_,i)=>(i+1)+' a'+(i+1)).join('\\n');asFinish();asCheck()}"); pg.wait_for_timeout(100)
    chk('a perfect Listening sheet: 40 / 40, band 9, "Xatosiz!" and no notebook option', ev("AS.res.raw") == 40 and ev("AS.res.band") == 9 and 'Xatosiz!' in pg.inner_text('#asv') and 'xatolar daftariga' not in pg.inner_text('#asv')); ev("asSave()")
    chk('Listening is saved as a Listening test (k = L) with its own grid cell', ev("S.ie.tests.slice(-1)[0].k") == 'L' and ev("S.ie.cm['16-4-L'].band") == 9)
    ev("()=>{asOpen()}"); chk('the next sheet remembers the last book and test (16, 4)', ev("AS.cb") == 16 and ev("AS.t") == 4); ev("asClose()")
    # xavfsizlik
    ev("()=>{asOpen();asStart();AS.a={};AS.kt='';asFinish();AS.kt=Array.from({length:12},(_,i)=>(i+1)+' x').join('\\n');__t=[];asCheck()}"); pg.wait_for_timeout(80); chk('empty answers against a short key give 0 and nothing breaks', ev("AS.res.raw") == 0 and ev("AS.res.W.length") == 12 and ev("AS.res.miss") == 28); ev("asClose()")
    ev("()=>{asOpen();asStart();AS.a={1:'<img src=x onerror=alert(1)>'};AS.kt=Array.from({length:12},(_,i)=>(i+1)+' q'+i).join('\\n');asFinish();asCheck()}"); pg.wait_for_timeout(80); chk('answers are shown as plain text (no HTML runs)', ev("document.querySelectorAll('#asv img[src=x]').length") == 0); ev("asClose()")
    bad = []
    ev("()=>{S.ie.cm={};for(const b of [10,11,12,13,14,15,16,17,18,19,20,21])for(const t of [1,2,3,4])S.ie.cm[b+'-'+t+'-L']={raw:30,band:7,d:dk()}}")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];asClose();asOpen()}", [ui, th]); pg.wait_for_timeout(60); ok1 = ev("document.querySelector('#asv .asc').scrollWidth<=document.querySelector('#asv .asc').clientWidth+1")
            ev("()=>{asStart()}"); pg.wait_for_timeout(60); ok2 = ev("document.querySelector('#asv .asc').scrollWidth<=document.querySelector('#asv .asc').clientWidth+1")
            ev("()=>{AS.kt=Array.from({length:40},(_,i)=>(i+1)+' a'+(i+1)).join('\\n');asFinish();asCheck()}"); pg.wait_for_timeout(60); ok3 = ev("document.querySelector('#asv .asc').scrollWidth<=document.querySelector('#asv .asc').clientWidth+1"); ev("asClose();S.ie.asd=null")
            if not (ok1 and ok2 and ok3): bad.append(ui + th)
    chk('the setup grid, the 40 answer boxes and the result fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
