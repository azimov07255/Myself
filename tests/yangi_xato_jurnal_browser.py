import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Xatolar jurnali va iPhone sinov ro'yxati. Soat: 2026-11-09 10:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
with Run('xato', when=(2026, 11, 9, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    err = lambda m, f='https://x.example/app.js', l=5, c=3: ev("(a)=>{window.dispatchEvent(new ErrorEvent('error',{message:a[0],filename:a[1],lineno:a[2],colno:a[3],error:new Error(a[0])}))}", [m, f, l, c])
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);errLog.clear();localStorage.removeItem('trk_qa');S.hab=[];tab='h';render()}""")
    chk('the journal starts empty and the app keeps working', ev("errLog.list().length") == 0)
    err('boom one', 'https://x.example/assets/app.js?v=3', 12, 7)
    L = ev("errLog.list()"); chk('a JS error is recorded: message, file name (without path/query), line, column, version, screen and a time', len(L) == 1 and L[0]['m'] == 'boom one' and L[0]['s'] == 'app.js' and L[0]['l'] == 12 and L[0]['c'] == 7 and L[0]['k'] == 'err' and L[0]['v'] == ev("APP_VER") and L[0]['p'] == 'h' and L[0]['t'] > 0, L)
    err('boom one', 'https://x.example/assets/app.js?v=3', 12, 7); err('boom one', 'https://x.example/assets/app.js', 12, 7)
    L = ev("errLog.list()"); chk('the same error repeating is counted (×3), not listed again', len(L) == 1 and L[0]['n'] == 3)
    err('boom two', '', 1, 1); chk('a different error is a new entry', len(ev("errLog.list()")) == 2)
    ev("()=>{window.dispatchEvent(new PromiseRejectionEvent('unhandledrejection',{promise:Promise.resolve(),reason:new Error('rejected promise')}))}"); L = ev("errLog.list()"); chk('unhandled promise rejections are recorded too (kind "rej")', L[-1]['k'] == 'rej' and L[-1]['m'] == 'rejected promise')
    ev("()=>{window.dispatchEvent(new PromiseRejectionEvent('unhandledrejection',{promise:Promise.resolve(),reason:'plain text reason'}))}"); chk('a non-Error reason (plain text) is recorded as text', ev("errLog.list().slice(-1)[0].m") == 'plain text reason')
    n = len(ev("errLog.list()")); err('ResizeObserver loop completed with undelivered notifications.'); err('ResizeObserver loop limit exceeded'); err('Script error.'); chk('harmless browser noise (ResizeObserver, cross-origin “Script error.”) is ignored', len(ev("errLog.list()")) == n)
    err('x' * 500); chk('very long messages are cut to 200 characters', len(ev("errLog.list().slice(-1)[0].m")) == 200)
    ev("()=>{for(let i=0;i<80;i++)errLog.add('err','unique '+i,'f.js',i,1,'')}"); L = ev("errLog.list()"); chk('only the last 50 entries are kept', len(L) == 50 and L[-1]['m'] == 'unique 79')
    ev("errLog.clear()"); chk('clearing empties the journal', ev("errLog.list().length") == 0)
    # nuqta
    ev("()=>{tab='h';render()}"); chk('no red dot on the settings icon while nothing is new', ev("document.querySelectorAll('.tbar .edot').length") == 0)
    err('new problem'); ev("render()"); pg.wait_for_timeout(60); chk('a new unseen error puts a small red dot on the ⚙️ icon', ev("document.querySelectorAll('.tbar .edot').length") == 1 and ev("errLog.unseen()") == 1)
    ev("()=>{tab='s';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('Settings has the "🩺 Xatolar jurnali (1)" group that lists the error with its place and says nothing is sent anywhere', '🩺 Xatolar jurnali (1)' in t or ev("document.body.textContent.includes('Xatolar jurnali (1)')"))
    ev("()=>{document.querySelectorAll('#app details').forEach(d=>d.open=true)}"); pg.wait_for_timeout(80); t = pg.inner_text('#app'); chk('the group explains it stays on the device, shows the yellow status, the error text and the buttons', 'hech qayerga yuborilmaydi' in t and '1 ta xato yozilgan' in t and 'new problem' in t and 'Hisobotni yuborish' in t)
    ev("()=>{tab='h';render()}"); pg.wait_for_timeout(60); chk('after the group was opened the dot goes away', ev("document.querySelectorAll('.tbar .edot').length") == 0)
    # hisobot
    ev("()=>{errLog.clear();errLog.add('err','sample failure','main.js',44,9,'at foo (main.js:44:9)\\nat bar (main.js:50:1)');S.hab=[{id:'h1',t:'MAXFIY ODAT NOMI'}];S.notes='MAXFIY'}")
    rep = ev("xjReport()")
    chk('the report has the version/build, device, screen, PWA mode, language/time zone, data size and the error with place and stack', all(x in rep for x in ['Kunlik tizim: xato hisoboti', 'Versiya: ' + ev("APP_VER"), 'Qurilma:', 'Ekran:', 'PWA:', 'Hajm: ma‘lumot', 'sample failure @ main.js:44:9', 'at foo (main.js:44:9)']), rep[:300])
    chk('the report contains NO personal data from the app (habit names, notes, money…)', 'MAXFIY' not in rep)
    ev("()=>{window.__cp='';Object.defineProperty(navigator,'clipboard',{value:{writeText:async t=>{window.__cp=t}},configurable:true});xjCopy()}"); chk('"📋" copies the report', ev("__cp").startswith('Kunlik tizim: xato hisoboti'))
    ev("()=>{window.__sh=null;Object.defineProperty(navigator,'share',{value:async d=>{window.__sh=d},configurable:true});xjShare()}"); pg.wait_for_timeout(200); chk('"📲 Hisobotni yuborish" shares the report as text through the share sheet', ev("__sh") and ev("__sh.text").startswith('Kunlik tizim: xato hisoboti'))
    ev("()=>{window.__cp='';Object.defineProperty(navigator,'share',{value:undefined,configurable:true});xjShare()}"); pg.wait_for_timeout(200); chk('without share support it copies instead', ev("__cp") != '')
    # sinov ro'yxati
    ev("()=>{tab='s';render();document.querySelectorAll('#app details').forEach(d=>d.open=true)}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('the iPhone checklist lists the 22 areas to test with ✅/❌ buttons and a counter', '📋 iPhone sinov ro‘yxati (0 ✅ · 0 ❌ / 22)' in t.replace('\n', ' ') or '0 ✅ · 0 ❌ / 22' in t)
    ev("xqSet('bugun','ok')"); chk('✅ marks an item (saved on the device)', ev("JSON.parse(localStorage.getItem('trk_qa')).bugun.s") == 'ok'); ev("xqSet('bugun','ok')"); chk('pressing ✅ again clears it', 'bugun' not in ev("JSON.parse(localStorage.getItem('trk_qa'))"))
    ev("()=>{window.prompt=()=>'Tugma bosilmadi';xqSet('hozir','bad')}"); q = ev("JSON.parse(localStorage.getItem('trk_qa'))"); chk('❌ asks what failed and stores the short note', q['hozir']['s'] == 'bad' and q['hozir']['n'] == 'Tugma bosilmadi')
    ev("()=>{window.prompt=()=>null;xqSet('oyin','bad')}"); chk('cancelling the question does not mark it', 'oyin' not in ev("JSON.parse(localStorage.getItem('trk_qa'))"))
    ev("()=>{window.prompt=()=>'x'.repeat(500);xqSet('ai','bad')}"); chk('notes are cut to 160 characters', len(ev("JSON.parse(localStorage.getItem('trk_qa')).ai.n")) == 160)
    ev("xqSet('maqsad','ok')"); rep = ev("xjReport()"); chk('the report adds the checklist result: counts and each ❌ item with its note', 'Sinov ro‘yxati: ✅ 1 ta, ❌ 2 ta, jami 22' in rep and '❌ 🎯 “Hozir nima qilay?”' in rep and 'Tugma bosilmadi' in rep)
    ev("()=>{tab='s';render();document.querySelectorAll('#app details').forEach(d=>d.open=true)}"); pg.wait_for_timeout(100); chk('the list shows the note under a ❌ item and the counter updates (1 ✅ · 2 ❌)', 'Tugma bosilmadi' in pg.inner_text('#app') and '1 ✅ · 2 ❌' in pg.inner_text('#app'))
    # xavfsizlik
    ev("()=>{errLog.clear();localStorage.setItem('trk_errs','not json')}"); chk('a damaged journal in storage does not break anything (treated as empty)', ev("errLog.list().length") == 0 and ev("xjReport().includes('Xatolar (0)')"))
    ev("()=>{localStorage.setItem('trk_qa','{broken')}"); chk('a damaged checklist does not break either', ev("Object.keys(xqS()).length") == 0)
    bad = []
    ev("()=>{errLog.clear();for(let i=0;i<8;i++)errLog.add('err','Uzun xato matni '.repeat(8)+i,'file'+i+'.js',i,1,'');localStorage.removeItem('trk_qa')}")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='s';render();document.querySelectorAll('#app details').forEach(d=>d.open=true)}", [ui, th]); pg.wait_for_timeout(80)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('the group fits the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
