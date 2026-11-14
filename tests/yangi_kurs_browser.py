import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# IELTS kursi: reja, avtomatik progress, strategiyalar, xatolar daftari. Soat: 2026-11-03 10:00 (seshanba).
import sys, json
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
with Run('kurs', when=(2026, 11, 3, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);window.aiOk=()=>true;window.__req=[];window.__fail='';
      window.fnAI=async b=>{__req.push(b);if(window.__fail)throw new Error(window.__fail);if(b.action==='iex'&&b.kind==='fix')return {text:JSON.stringify({items:[{w:'People is',r:'People are',c:'grammar',n:'people ko‘plik'},{w:'make a research',r:'do research',c:'vocab',n:'research bilan do'},{w:'citys',r:'cities',c:'spelling',n:'y → ies'},{w:'bad',r:'bad',c:'grammar'},{w:'x',r:'y',c:'weird'}],band:6.5,sum:'Grammatika va imlo xatolari bor.'})};
        if(b.action==='iex'&&b.kind==='errors')return {text:JSON.stringify({patterns:[{t:'Artikl tushib qoladi',why:'o‘zbek tilida artikl yo‘q',fix:'Har otdan oldin a/the ni tekshiring',ex:['I have car -> I have a car']},{t:'Ko‘plik -s',why:'-',fix:'ko‘plikni tekshiring',ex:[]}],plan:['Har kuni 5 ta gap yozing','Daftarni takrorlang']})};return {text:'{}'}};
      S.ie.kr=null;S.ie.tests=[];S.ie.mock=[];S.ie.xd=[];S.ie.xdr={};S.ie.xdai=null;S.ie.rmd={};S.ie.target=7;KS={sec:'r',wk:0,sx:'',su:null,fx:null,fxB:null,fxS:'',xf:'a',xc:'grammar',busy:0,err:'',ai:0,rv:null,sf:'all'};tab='e';EV='i';IVW='y';render()}""")
    t = pg.inner_text('#app')
    chk('without a course the Kurs tab shows the setup: description, target band chips (6.5 … 9), hours per day (1-7), exam date and a start button', '12 haftalik reja' in t and ev("(()=>{const g=[...document.querySelectorAll('#app .goal')].find(g=>g.textContent.includes('12 haftalik reja'));return g.querySelectorAll('.rwch')[0].querySelectorAll('button').length})()") == 6 and ev("(()=>{const g=[...document.querySelectorAll('#app .goal')].find(g=>g.textContent.includes('12 haftalik reja'));return g.querySelectorAll('.rwch')[1].querySelectorAll('button').length})()") == 7 and ev("!!document.getElementById('ksex')") and 'Kursni boshlash' in t)
    chk('defaults: target 7 and 2 hours are preselected', ev("(()=>{const g=[...document.querySelectorAll('#app .goal')].find(g=>g.textContent.includes('12 haftalik reja'));return [...g.querySelectorAll('.rwch')[0].querySelectorAll('.on')].map(b=>b.textContent)})()") == ['7'] and ev("(()=>{const g=[...document.querySelectorAll('#app .goal')].find(g=>g.textContent.includes('12 haftalik reja'));return [...g.querySelectorAll('.rwch')[1].querySelectorAll('.on')].map(b=>b.textContent)})()") == ['2 soat'])
    secs = ev("[...document.querySelectorAll('#app .seg.sc')[0].querySelectorAll('button')].map(b=>b.textContent)")
    chk('the section bar (Reja, Strategiya, Xatolar, So‘z yo‘li) is visible BEFORE the course is started, so the word roadmap, strategies and notebook are always reachable', secs == ['📅 Reja', '🧭 Strategiya', '📓 Xatolar', '🗺 So‘z yo‘li'], secs)
    pg.click('#app .seg.sc >> text=So‘z yo‘li'); pg.wait_for_timeout(150); chk('"🗺 So‘z yo‘li" opens the vocabulary roadmap without a course (stages, daily goal)', 'IELTS 8+ yo‘l xaritasi' in pg.inner_text('#app') and 'Asos 1' in pg.inner_text('#app') and ev("S.ie.kr") is None)
    pg.click('#app .seg.sc >> text=Strategiya'); pg.wait_for_timeout(100); chk('"🧭 Strategiya" works without a course too (cards, but no "O‘qidim" button)', ev("document.querySelectorAll('#app .goal').length") == ev("KST.length") and '✓ O‘qidim' not in pg.inner_text('#app'))
    pg.click('#app .seg.sc >> text=Xatolar'); pg.wait_for_timeout(100); chk('"📓 Xatolar" works without a course', '📓 Xatolar daftari' in pg.inner_text('#app'))
    pg.click('#app .seg.sc >> text=Reja'); pg.wait_for_timeout(100); chk('"📅 Reja" returns to the course setup', 'Kursni boshlash' in pg.inner_text('#app'))
    pg.click('#app .goal:has-text("12 haftalik reja") .rwch >> nth=0 >> text="8"'); pg.click('#app .goal:has-text("12 haftalik reja") .rwch >> nth=1 >> text=3 soat'); pg.fill('#ksex', '2027-02-01'); pg.dispatch_event('#ksex', 'change'); pg.wait_for_timeout(60)
    pg.click('#app >> text=Kursni boshlash'); pg.wait_for_timeout(150); k = ev("S.ie.kr"); t = pg.inner_text('#app')
    chk('starting saves the course (start today, target 8, 3 h/day, 12 weeks, exam date) and updates the general target', k['start'] == '2026-11-03' and k['target'] == 8 and k['hrs'] == 3 and k['wks'] == 12 and k['exam'] == '2027-02-01' and ev("S.ie.target") == 8, k)
    chk('the header shows "IELTS 8+ kursi", "Hafta 1 / 12", progress and the exam countdown (90 days)', 'IELTS 8+ kursi' in t and 'Hafta 1 / 12' in t and 'Imtihongacha 90 kun' in t and 'Umumiy jarayon' in t, t[:200])
    # ---------- reja tuzilmasi ----------
    P = ev("(()=>{const p=ksPlan();return p.map(w=>w.k.map(t=>t.id+':'+t.g+':'+(t.q?t.q.k:'')))})()"); allg = ev("ksPlan().flatMap(w=>w.k.map(t=>t.g))"); rid = ev("ksPlan().flatMap(w=>w.k.filter(t=>t.q&&t.q.k==='read').flatMap(t=>t.q.ids))"); sids = ev("KST.map(c=>c.id)")
    chk('the plan has 12 weeks, each with 5-7 tasks, and task ids are unique inside a week', len(P) == 12 and all(5 <= len(w) <= 8 for w in P) and all(len(set(x.split(':')[0] for x in w)) == len(w) for w in P), [len(w) for w in P])
    ok_go = all(g == '' or g in ('w', 's', 'a', 'k', 'y', 'xd') or g in ('m:R', 'm:L', 'm:W', 'm:S', 'm:M') or (g.startswith('st:') and g[3:] in sids) for g in allg)
    chk('every "start" button points to a real screen and every strategy referenced by a task exists in the library', ok_go and all(i in sids for i in rid) and len(set(sids)) == len(sids) >= 22, [g for g in allg if not (g == '' or g in ('w', 's', 'a', 'k', 'y', 'xd') or g.startswith('m:') or g.startswith('st:'))])
    c3 = lambda m, hi: ev("(a)=>ksTpl(a[0],a[1])[2].k.find(t=>t.id==='b').q.n", [m, hi])
    chk('weekly volume scales with the hours per day: Reading tests in week 3 = 2 (1 h), 3 (2 h), 4 (3 h), 5 (4 h)', [c3(.6, 0), c3(1, 0), c3(1.4, 0), c3(1.8, 0)] == [2, 3, 4, 5], [c3(.6, 0), c3(1, 0), c3(1.4, 0), c3(1.8, 0)])
    w6 = lambda hi: ev("(h)=>ksTpl(1,h)[5].k.length", hi); w9 = lambda hi: ev("(h)=>ksTpl(1,h)[8].k.length", hi)
    chk('a target of 7.5+ adds Band-8 tasks (week 6 and week 9) that lower targets do not get', w6(True) == w6(False) + 1 and w9(True) == w9(False) + 1)
    # ---------- bugun va hafta ----------
    td = ev("[...document.querySelectorAll('#app .goal')].find(g=>g.textContent.includes('Bugun uchun')).querySelectorAll('.kst').length"); chk('"📌 Bugun uchun" shows up to 3 open tasks of the current week with ▶ buttons', td == 3 and ev("[...document.querySelectorAll('#app .goal')].find(g=>g.textContent.includes('Bugun uchun')).querySelectorAll('.btn').length") == 3)
    chk('the week card lists all 6 tasks of week 1 with the week title and dates (11-03 — 11-09)', '1-hafta (hozirgi)' in t and 'Poydevor: format va boshlang‘ich daraja' in t and '11-03 — 11-09' in t and '0 / 6 vazifa' in t)
    pg.click('#app .kck >> nth=3'); pg.wait_for_timeout(100); wk1 = ev("Object.keys(S.ie.kr.done)")
    chk('ticking a task stores it by week and id; the week shows 1 / 6', wk1 == ['w1a'] and '1 / 6 vazifa' in pg.inner_text('#app'), wk1)
    pg.click('#app .kck.on >> nth=0'); pg.wait_for_timeout(80); chk('ticking it again un-ticks it', ev("Object.keys(S.ie.kr.done)") == [] and '0 / 6 vazifa' in pg.inner_text('#app'))
    # ---------- avtomatik progress ----------
    ev("()=>{S.ie.tests.push({id:1,d:dk(),k:'R',src:'x',min:60,b:{R:6.5},raw:{R:28}});S.ie.tests.push({id:2,d:dk(),k:'M',src:'m',min:0,b:{L:7,W:6.5,S:6.5},raw:{}});render()}"); pg.wait_for_timeout(100)
    pr = ev("(()=>{const p=ksPlan()[0].k;return p.map(t=>ksProg(t,0).done)})()")
    chk('results you log in the app tick the matching tasks by themselves: a Reading test -> diagnostic Reading; a full mock -> Listening, Writing and Speaking diagnostics too', pr == [False, True, True, True, True, False], pr)
    ev("()=>{S.ie.tests.push({id:3,d:ksAdd(dk(),-30),k:'R',b:{R:7}});render()}"); chk('results from other weeks do not count towards this week', ev("S.ie.tests.length") == 3 and ev("ksProg(ksPlan()[2].k[1],2).c") == 0)
    ev("()=>{S.ie.rmd={[dk()]:20};render()}"); pv = ev("ksProg(ksPlan()[0].k[5],0)"); chk('vocabulary progress is read from the roadmap: 20 of 49 new words this week (3 h/day) and the task shows 20 / 49', pv['c'] == 20 and pv['n'] == 49 and '20 / 49' in pg.inner_text('#app'), pv)
    ev("()=>{S.ie.rmd={[dk()]:60};render()}"); chk('...and completes itself at the target', ev("ksProg(ksPlan()[0].k[5],0).done"))
    ev("()=>{S.ie.kr.read={gband:dk(),gtime:dk()};render()}"); chk('marking both strategies as read completes the "Strategiya" task automatically', ev("ksProg(ksPlan()[0].k[0],0).done"))
    ev("()=>{xdPut('grammar','a1','b1','', 'm');xdPut('grammar','a2','b2','', 'm');xdPut('vocab','a3','b3','', 'm');xdPut('vocab','a4','b4','', 'm');xdPut('spelling','a5','b5','', 'm');render()}"); chk('mistakes added to the notebook count towards "xato" tasks of that week (5 added -> done)', ev("ksProg({q:{k:'xd',n:5}},0).done"))
    # ---------- hafta tanlash ----------
    ev("()=>{KS.wk=0;render()}"); pg.click('#app .goal .h >> text=▶'); pg.wait_for_timeout(100); chk('▶ shows week 2 (not marked as current) and ◀ goes back', '2-hafta' in pg.inner_text('#app') and '2-hafta (hozirgi)' not in pg.inner_text('#app') and ev("KS.wk") == 2)
    pg.click('#app .row >> text=7. Speaking I'); pg.wait_for_timeout(100); chk('tapping a week in the overview opens it', '7-hafta' in pg.inner_text('#app') and 'Speaking I' in pg.inner_text('#app') and ev("KS.wk") == 7)
    ev("()=>{KS.wk=0;render()}")
    # ---------- vaqt o'tishi ----------
    pg.clock.set_system_time('2026-11-12T10:00:00'); ev("render()"); pg.wait_for_timeout(80); t = pg.inner_text('#app')
    chk('9 days later the course is in week 2 and "Bugun uchun" lists week-2 tasks', 'Hafta 2 / 12' in t and ev("ksCw()") == 2 and 'Writing Task 2 tuzilmasi' in ev("[...document.querySelectorAll('#app .goal')].find(g=>g.textContent.includes('Bugun uchun')).textContent"))
    pg.clock.set_system_time('2026-11-16T10:00:00'); ev("()=>{S.ie.tests=[];S.ie.kr.done={};S.ie.kr.read={};S.ie.xd=[];S.ie.rmd={};render()}"); pg.wait_for_timeout(80); chk('behind schedule (late in the week with nothing done) -> a clear warning', 'orqada' in pg.inner_text('#app'))
    pg.clock.set_system_time('2026-11-12T10:00:00')
    ev("()=>{const p=ksPlan();S.ie.kr.done={};p[1].k.forEach(t=>{S.ie.kr.done['w2'+t.id]='x'});render()}"); chk('when the whole week is done -> a congratulation', 'hamma vazifasi bajarildi' in pg.inner_text('#app'))
    pg.clock.set_system_time('2027-03-01T10:00:00'); ev("render()"); pg.wait_for_timeout(80); t = pg.inner_text('#app'); chk('after 12 weeks the course is "yakunlandi" and there is no "Bugun uchun"; the exam date has passed', 'yakunlandi' in t and 'Bugun uchun' not in t and 'Imtihon sanasi o‘tgan' in t)
    pg.clock.set_system_time('2026-11-03T10:00:00'); ev("()=>{S.ie.kr.start=ksAdd(dk(),2);render()}"); pg.wait_for_timeout(80); chk('a course that starts in the future says so ("2 kundan keyin") and stays in week 1', '2 kundan keyin' in pg.inner_text('#app') and ev("ksCw()") == 1 and 'Bugun uchun' not in pg.inner_text('#app')); ev("()=>{S.ie.kr.start=dk();S.ie.kr.done={};render()}")
    chk('date helpers work across month and year ends', ev("[ksAdd('2026-12-30',5),ksAdd('2027-03-01',-1),ksDiff('2026-11-03','2027-02-01'),ksAdd('2026-03-28',2)]") == ['2027-01-04', '2027-02-28', 90, '2026-03-30'])
    # ---------- sozlamalar ----------
    pg.click('#app .goal:has-text("Sozlamalar") .rwch >> nth=0 >> text="7"'); pg.wait_for_timeout(80); chk('changing the target to 7 re-plans (the Band-8 tasks disappear) and updates the general target', ev("S.ie.kr.target") == 7 and ev("S.ie.target") == 7 and ev("ksPlan()[5].k.length") == w6(False))
    pg.click('#app .goal:has-text("Sozlamalar") .rwch >> nth=1 >> text=1 soat'); pg.wait_for_timeout(80); chk('changing hours per day scales the volume at once', ev("S.ie.kr.hrs") == 1 and ev("ksPlan()[2].k[1].q.n") == 2)
    ev("ksSet('exam','2026-11-10')"); chk('changing the exam date updates the countdown (7 days)', 'Imtihongacha 7 kun' in pg.inner_text('#app'))
    ev("()=>{S.ie.kr.done={w1a:'x'};S.ie.xd=[];for(let i=0;i<5;i++)xdPut('grammar','w'+i,'r'+i,'','m');S.ie.words=[{id:1,w:'keep',m:'x',k:'w',box:0,due:dk(),t:0}]}"); ev("ksReset()"); pg.wait_for_timeout(100); chk('"Kursni qayta boshlash" returns to the setup but keeps your mistakes notebook and words', ev("S.ie.kr") is None and 'Kursni boshlash' in pg.inner_text('#app') and len(ev("S.ie.xd")) == 5 and len(ev("S.ie.words")) == 1)
    # ---------- IELTS Bosh kartochkasi ----------
    ev("()=>{IVW='b';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('the IELTS home screen offers the course before it is started ("Boshlash")', '🎓 IELTS kursi' in t and 'Boshlash' in t)
    ev("()=>{KS.su={t:8,h:2,ex:''};ksStart();IVW='b';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('...and after starting shows the current week, progress and today\u2019s first two tasks', 'Kurs: 1-hafta' in t and 'Bugun uchun:' in t and ev("document.querySelectorAll('#app .goal')[0].textContent").count('▪') == 2)
    pg.click('#app >> text=Kursni ochish'); pg.wait_for_timeout(100); chk('"Kursni ochish" opens the plan', ev("IVW") == 'y' and ev("KS.sec") == 'r' and 'Hafta 1 / 12' in pg.inner_text('#app'))
    pg.click('#app .kst >> nth=1 >> .btn'); pg.wait_for_timeout(100); chk('a task\u2019s ▶ opens the right tool (Reading diagnostic -> Mashq with Reading selected)', ev("IVW") == 'm' and ev("IK") == 'R')
    ev("()=>{IVW='y';KS.sec='r';render()}")
    # ---------- STRATEGIYALAR ----------
    ev("()=>{KS.sec='s';KS.sx='';KS.sf='all';render()}"); pg.wait_for_timeout(100); cards = ev("document.querySelectorAll('#app .goal').length")
    chk('the strategy library lists all cards, closed by default, with a course-section bar and a skill filter (Hammasi, Reading, Listening, Writing Task 1/2, Speaking, Umumiy)', cards == len(sids) and ev("[...document.querySelectorAll('#app .seg.sc')[0].querySelectorAll('button')].map(b=>b.textContent)") == ['📅 Reja', '🧭 Strategiya', '📓 Xatolar', '🗺 So‘z yo‘li'] and ev("[...document.querySelectorAll('#app .seg.sc')[1].querySelectorAll('button')].map(b=>b.textContent)") == ['Hammasi', 'Reading', 'Listening', 'Writing Task 1', 'Writing Task 2', 'Speaking', 'Umumiy'] and ev("document.querySelectorAll('#app ol').length") == 0)
    pg.click('#app >> text=Listening >> nth=1') if False else ev("()=>{KS.sf='L';render()}"); n = ev("document.querySelectorAll('#app .goal').length"); chk('filtering by Listening shows only its 4 cards', n == 4 and all('Listening' in x for x in ev("[...document.querySelectorAll('#app .goal')].map(g=>g.textContent)")), n)
    ev("()=>{KS.sf='all';render()}"); pg.click('#app .goal >> nth=0 >> .h'); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('opening a card shows what it tests, numbered steps, pitfalls, timing and the Band 8+ tip', 'True / False / Not Given' in t and 'Strategiya' in t and 'Tuzoqlar' in t and '🎯 Band 8+ maslahat' in t and 'Cheklov so‘zlariga' in t and ev("document.querySelectorAll('#app ol li').length") >= 3)
    pg.click('#app >> text=✓ O‘qidim'); pg.wait_for_timeout(100); chk('"✓ O‘qidim" marks it read (a chip appears) and the course task that needs it completes by itself', ev("!!S.ie.kr.read.tfng") and '✓ o‘qildi' in pg.inner_text('#app'))
    pg.click('#app >> text=Belgini olib tashlash'); pg.wait_for_timeout(80); chk('and it can be un-marked', ev("!S.ie.kr.read.tfng"))
    ev("()=>{KS.sx=''}")
    # ---------- XATOLAR DAFTARI ----------
    ev("()=>{S.ie.xd=[];S.ie.xdr={};S.ie.xdai=null;__req=[];__t=[];KS.sec='x';KS.xf='a';KS.fx=null;KS.fxS='';KS.err='';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('the notebook screen: the intro, the AI checker, the manual form (9 categories), no statistics while it is empty', '📓 Xatolar daftari' in t and '🔍 Matnni tekshir (AI)' in t and '➕ Qo‘lda qo‘shish' in t and ev("document.querySelectorAll('#app .goal')[2].querySelectorAll('.chip').length") == 9 and '📊 Statistika' not in t)
    ev("()=>{KS.xc='vocab';render()}"); pg.fill('#xdw', ''); pg.fill('#xdr', 'do research'); pg.click('#app >> text=+ >> nth=0') if False else ev("xdAdd()"); chk('an empty field is refused with a message', len(ev("S.ie.xd")) == 0 and any('yozing' in x for x in ev("__t")))
    pg.fill('#xdw', 'make a research'); pg.fill('#xdr', 'do research'); pg.fill('#xdn', 'research bilan do ishlatiladi'); ev("xdAdd()"); pg.wait_for_timeout(100); x = ev("S.ie.xd[0]")
    chk('a manual entry is saved with category, both texts, the note, box 0 and due today', x['c'] == 'vocab' and x['w'] == 'make a research' and x['r'] == 'do research' and x['n'].startswith('research') and x['box'] == 0 and x['due'] == '2026-11-03' and x['src'] == 'm', x)
    pg.fill('#xdw', 'make a research'); pg.fill('#xdr', 'do research'); ev("xdAdd()"); chk('the same mistake cannot be added twice', len(ev("S.ie.xd")) == 1 and any('allaqachon' in x for x in ev("__t")))
    # AI tekshiruv
    pg.fill('#xdt', 'short'); ev("xdFix()"); pg.wait_for_timeout(80); chk('a too short text is refused locally (no request)', 'Kamida 20 belgi' in pg.inner_text('#app') and len(ev("__req")) == 0)
    TX = 'People is very important for the development of citys and they does not know it.'; pg.fill('#xdt', TX); pg.click('#app >> text=Xatolarni top'); pg.wait_for_timeout(400); t = pg.inner_text('#app'); rq = ev("__req")
    chk('the checker sends ONE request with the text and shows the estimated band, the summary and the found mistakes (invalid ones are dropped, an unknown category becomes grammar)', len(rq) == 1 and rq[0]['kind'] == 'fix' and rq[0]['text'] == TX and 'Taxminiy Writing bahosi: 6.5' in t and 'Grammatika va imlo xatolari bor.' in t and 'People is' in t and 'citys' in t and ev("KS.fx.items.length") == 4 and ev("KS.fx.items[3].c") == 'grammar', t[:200])
    pg.click('#app .yxw >> nth=0 >> text=Daftarga'); pg.wait_for_timeout(100); chk('"➕ Daftarga" adds one (marked as AI) and the row turns into "✓ daftarda"', len(ev("S.ie.xd")) == 2 and ev("S.ie.xd[1].src") == 'ai' and ev("document.querySelectorAll('#app .yxw')[0].textContent").count('✓ daftarda') == 1)
    ev("xdFixAll()"); pg.wait_for_timeout(100); chk('"Hammasini daftarga qo‘sh" adds the rest (the item you already entered by hand is skipped, the unknown category becomes grammar)', len(ev("S.ie.xd")) == 4 and any('2 ta xato' in x for x in ev("__t")))
    ev("__t=[]"); ev("xdFixAll()"); chk('pressing it again adds nothing and says so', len(ev("S.ie.xd")) == 4 and any('allaqachon' in x for x in ev("__t")))
    ev("()=>{window.__fail='Bugungi limit tugadi (40 ta so‘rov).';KS.fx=null}"); pg.fill('#xdt', TX); ev("xdFix()"); pg.wait_for_timeout(300); chk('an AI failure shows the reason and keeps your text', 'Bugungi limit tugadi' in pg.inner_text('#app') and ev("KS.fxS") == TX); ev("window.__fail=''")
    ev("window.aiOk=()=>false"); ev("xdFix()"); pg.wait_for_timeout(80); chk('not signed in: a clear message', 'hisobga kirish' in pg.inner_text('#app')); ev("window.aiOk=()=>true")
    # statistika, filtr, o'chirish
    ev("()=>{KS.err='';KS.fx=null;render()}"); pg.wait_for_timeout(80); t = pg.inner_text('#app')
    chk('statistics show counts per category (biggest first) and the last four weeks of new mistakes', '📊 Statistika' in t and 'Oxirgi 4 hafta' in t and '0 → 0 → 0 → 4' in t.replace('\n', ' '))
    ev("xdFilt('spelling')"); pg.wait_for_timeout(80); chk('the category filter shows only that category', ev("document.querySelectorAll('#app .row').length") == 1 and 'citys' in pg.inner_text('#app')); ev("xdFilt('a')")
    pg.click('#app .row >> nth=0 >> .x'); pg.wait_for_timeout(100); chk('a mistake can be deleted', len(ev("S.ie.xd")) == 3)
    # naqshlar
    ev("()=>{S.ie.xd=S.ie.xd.slice(0,2);__req=[];render()}"); ev("xdAi()"); chk('pattern analysis needs at least 3 mistakes', any('kamida 3' in x for x in ev("__t")) and len(ev("__req")) == 0)
    ev("()=>{xdPut('grammar','I have car','I have a car','','m');xdPut('spelling','recieve','receive','','m');xdPut('grammar','he go','he goes','','m');render()}"); ev("xdAi()"); pg.wait_for_timeout(400); rq = ev("__req"); t = pg.inner_text('#app')
    chk('the analysis sends the mistakes as category / wrong / right (at most 40) and shows patterns with reason, fix and examples, plus a weekly plan; it is saved', len(rq) == 1 and rq[0]['kind'] == 'errors' and rq[0]['items'][0].keys() == {'c', 'w', 'r'} and len(rq[0]['items']) == 5 and 'Artikl tushib qoladi' in t and 'I have car -&gt; I have a car'.replace('&gt;', '>') in t and 'Bir haftalik reja' in t and 'Daftarni takrorlang' in t and ev("S.ie.xdai.p.length") == 2)
    # takrorlash
    ev("()=>{S.ie.xd.forEach((x,i)=>{x.box=i%3;x.due='2026-11-03'});S.ie.xd[0].due='2026-11-10';render()}"); pg.wait_for_timeout(80); chk('the review button shows how many are due today (those due later are not counted)', 'Takrorlash (4)' in pg.inner_text('#app'))
    pg.click('#app >> text=Takrorlash (4)'); pg.wait_for_timeout(100); r = ev("KS.rv"); chk('review starts with the least-learned first (lowest box), shows the wrong text only', len(r['q']) == 4 and ev("(()=>{const a=KS.rv.q.map(id=>S.ie.xd.find(x=>x.id===id).box);return a.join()===[...a].sort().join()})()") and ev("document.querySelector('#app .goal s').textContent") == ev("S.ie.xd.find(x=>x.id===KS.rv.q[0]).w"))
    q0 = ev("KS.rv.q[0]"); pg.click('#app >> text=To‘g‘risini ko‘rsat'); pg.wait_for_timeout(80); chk('"To‘g‘risini ko‘rsat" reveals the correct form and the note', ev("S.ie.xd.find(x=>x.id===KS.rv.q[0]).r") in pg.inner_text('#app'))
    b0 = ev("(id)=>S.ie.xd.find(x=>x.id===id).box", q0); pg.click('#app >> text=Eslay oldim'); pg.wait_for_timeout(80); x = ev("(id)=>S.ie.xd.find(y=>y.id===id)", q0)
    chk('"Eslay oldim" raises the box and moves the next review into the future (box 1 -> +1 day, box 2 -> +3 days)', x['box'] == b0 + 1 and x['due'] == ev("(a)=>ksAdd(dk(),[0,1,3,7,14,30][a])", x['box']) and x['ok'] == 1, x)
    q1 = ev("KS.rv.q[1]"); pg.click('#app >> text=To‘g‘risini ko‘rsat'); pg.click('#app >> text=Qiynaldim'); pg.wait_for_timeout(80); y = ev("(id)=>S.ie.xd.find(z=>z.id===id)", q1); chk('"Qiynaldim" sends it back to box 0, due today', y['box'] == 0 and y['due'] == '2026-11-03' and y['bad'] == 1, y)
    for _ in range(2):
        pg.click('#app >> text=To‘g‘risini ko‘rsat'); pg.click('#app >> text=Eslay oldim'); pg.wait_for_timeout(60)
    t = pg.inner_text('#app'); chk('the review ends with a score, and today\u2019s review count is stored (4)', 'Takrorlash tugadi' in t and '3 / 4' in t and ev("S.ie.xdr['2026-11-03']") == 4, t[:120])
    pg.click('#app >> text=Yopish'); pg.wait_for_timeout(60)
    ev("()=>{S.ie.kr={start:dk(),target:8,hrs:2,wks:12,exam:'',done:{},read:{}};render()}"); chk('reviews count towards the course task "Xatolar daftarini takrorlang"', ev("ksProg({q:{k:'xrev',n:4}},0).done"))
    ev("()=>{S.ie.xd=[];for(let i=0;i<450;i++)xdPut('grammar','w'+i,'r'+i,'','m')}"); chk('the notebook keeps at most 400 mistakes (the oldest are dropped)', ev("S.ie.xd.length") == 400 and ev("S.ie.xd[0].w") == 'w50')
    # ---------- ko'rinish ----------
    ev("()=>{S.ie.xd=[];for(let i=0;i<12;i++)xdPut(['grammar','vocab','spelling'][i%3],'wrong sentence number '+i,'right sentence number '+i,'a longer explanation of the rule '+i,'m');KS.fx={items:[{c:'grammar',w:'x y',r:'z',n:'n'}],band:6.5,sum:'s'};KS.fxS='text';render()}")
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1]}", [ui, th])
            for sec in ('r', 's', 'x'):
                ev("(s)=>{KS.sec=s;KS.sx='tfng';render()}", sec); pg.wait_for_timeout(40)
                if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th + sec)
    chk('the course plan, strategies and notebook do not overflow the phone screen in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
