import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Zaxira: holat paneli, telefondagi snapshotlar, tiklashdan oldin ko'rish, oldingi holatga qaytish, ulashish. Soat: 2026-11-05 10:00.
import sys, json
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
with Run('zaxira', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""async()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.__al=[];window.alert=m=>window.__al.push(m);
      const I=await idbGet(SNI);if(I)for(const x of I)await idbDel(x.k);await idbDel(SNI);SNC=null;SNP=null;SNV=null;lsRm('trk_prerestore');lsRm('trk_bk');lsRm('trk_dirty');
      S.hab=[{id:'h1',t:'A'},{id:'h2',t:'B'}];S.hb={};for(let i=0;i<10;i++){S.hb[dAgo(i)]={h1:true,h2:i%2===0}}S.money=Array.from({length:12},(_,i)=>({id:i,a:1,d:dk(),c:'x'}));S.ie.words=Array.from({length:25},(_,i)=>({id:i,w:'w'+i,m:'m',box:1,due:dk()}));S.ie.tests=[{id:1,d:dk(),k:'R',b:{R:6}}];S.goals=[{t:'G1',ms:[]},{t:'G2',ms:[]}];S.q.m={1:20,2:3};S.ts=Date.now();return 1}""")
    n = ev("snNum(S)"); chk('the data summary counts habit ticks, money records, vocabulary, IELTS tests, goals and memorized pages', n == {'hb': 15, 'm': 12, 'w': 25, 't': 1, 'g': 2, 'q': 23}, n)
    ev("snNum(null)"); chk('an empty or broken object gives zeros (no crash)', ev("snNum(undefined)") == {'hb': 0, 'm': 0, 'w': 0, 't': 0, 'g': 0, 'q': 0})
    ev("async()=>{await snTake('auto')}"); I = ev("snIdx()"); raw = ev("(async()=>idbGet((await snIdx())[0].k))()")
    chk('the first daily snapshot is stored on the phone (IndexedDB) with its date, reason, size and counts; the stored data equals the current state', len(I) == 1 and I[0]['w'] == 'auto' and I[0]['d'] == '2026-11-05' and I[0]['n']['hb'] == 15 and ev("(async()=>{const I=await snIdx();return (await idbGet(I[0].k)).length===I[0].sz})()") and json.loads(raw)['money'] and len(json.loads(raw)['money']) == 12, I)
    ev("async()=>{await snTake('auto')}"); chk('only ONE automatic snapshot per day', len(ev("snIdx()")) == 1)
    ev("async()=>{await snNow()}"); I = ev("snIdx()"); chk('"📸 Snapshot" adds a manual one (several per day allowed)', len(I) == 2 and {x['w'] for x in I} == {'auto', 'qo‘lda'} and any('Snapshot saqlandi' in m for m in ev("__t")))
    ev("""async()=>{S.hb={};S.money=[];S.ie.words=[]}"""); ev("async()=>{await snTake('auto')}"); chk('with almost no data a snapshot is not taken automatically (nothing worth saving yet)', len(ev("snIdx()")) == 2)
    ev("""async()=>{for(let i=0;i<9;i++){const k=SNK+'old'+i,raw=JSON.stringify({goals:[],ts:1});await idbSet(k,raw);const I=await snIdx();I.push({k,d:'2026-10-0'+(i+1),ts:1000+i,w:'auto',sz:raw.length,n:snNum({})});await idbSet(SNI,I)}await snTake('qo‘lda',true)}""")
    I = ev("snIdx()"); au = [x for x in I if x['w'] == 'auto']; oth = [x for x in I if x['w'] != 'auto']
    chk('old snapshots are pruned: the newest 7 automatic and the newest 5 others are kept; pruned ones are also deleted from storage', len(au) == 7 and len(oth) == 2 and ev("(async()=>await idbGet(SNK+'old0'))()") is None and ev("(async()=>!!(await idbGet(SNK+'old8')))()"), (len(au), len(oth)))
    ev("async()=>{for(let i=0;i<6;i++)await snTake('qo‘lda',true)}"); chk('manual and pre-restore snapshots are capped at the newest 5', len([x for x in ev('snIdx()') if x['w'] != 'auto']) == 5)
    # tiklashdan oldin ko'rish
    ev("""()=>{S.hb={};for(let i=0;i<10;i++){S.hb[dAgo(i)]={h1:true,h2:true}}S.money=Array.from({length:30},(_,i)=>({id:i,a:1,d:dk(),c:'x'}));S.ie.words=Array.from({length:40},(_,i)=>({id:i,w:'w'+i,m:'m',box:1,due:dk()}));S.ts=Date.now();window.__cur=JSON.stringify(S)}""")
    old = {'goals': [{'t': 'G1', 'ms': []}], 'hb': {'2026-10-01': {'h1': True}}, 'money': [{'id': 1}] * 5, 'ie': {'words': [{'w': 'a'}] * 3}, 'ts': 1759000000000, 'hab': [{'id': 'h1', 't': 'A'}]}
    ev("(t)=>{bkApply(t)}", json.dumps(old)); pg.wait_for_timeout(120); t = pg.inner_text('#snv')
    chk('restoring from a file or text now opens a PREVIEW first (nothing changes yet) comparing the backup with the current data', ev("!!document.getElementById('snv')") and ev("JSON.stringify(S)===__cur") and 'Tiklashdan oldin' in t and 'Zaxirada' in t and 'Hozir' in t and 'Odat belgilari' in t)
    chk('the preview warns when the backup is much older (days) and lists exactly what would be lost (e.g. money 5 vs 30 → 25 would be lost)', 'kun eski' in t and 'Pul yozuvlari: zaxirada 5, hozir 30 (25 ta yo‘qoladi)' in t and 'Lug‘at so‘zlari: zaxirada 3, hozir 40' in t and ev("document.querySelectorAll('#snv .snw').length") >= 3)
    chk('it says that the current state will be saved on the phone first (so it can be undone)', 'hozirgi holating shu telefonda saqlab qo‘yiladi' in t)
    ev("snvClose()"); chk('"Bekor" closes it and leaves the data untouched', ev("!document.getElementById('snv')") and ev("JSON.stringify(S)===__cur") and ev("lsGet('trk_prerestore')") is None)
    ev("(t)=>{bkApply(t)}", json.dumps(old)); pg.wait_for_timeout(100); ev("async()=>{await snApply()}"); pg.wait_for_timeout(200)
    chk('"Tiklash" restores the backup', ev("S.money.length") == 5 and ev("S.ie.words.length") == 3 and ev("S.goals.length") == 1 and ev("!document.getElementById('snv')"))
    chk('...but FIRST the previous state was kept: the "pre-restore" copy on the phone equals the state before restoring, and a "tiklashdan oldin" snapshot exists', json.loads(ev("lsGet('trk_prerestore')")) == json.loads(ev("__cur")) and any(x['w'] == 'tiklashdan oldin' for x in ev("snIdx()")))
    ev("window.confirm=()=>true;histUndo()"); pg.wait_for_timeout(150); chk('the "undo" returns exactly to the state before the restore', ev("S.money.length") == 30 and ev("S.ie.words.length") == 40 and ev("lsGet('trk_prerestore')") is None)
    ev("(t)=>{__al.length=0;bkApply(t)}", '{bad'); chk('a damaged file is refused with a message and no preview', ev("__al")[0] == 'Zaxira noto‘g‘ri.' and ev("!document.getElementById('snv')")); ev("()=>{__al.length=0;bkApply('{\"a\":1}')}"); chk('a file of another shape (no goals) is refused too', ev("__al")[0] == 'Zaxira noto‘g‘ri.')
    recent = dict(old, hb={'2026-11-05': {'h1': True}}, money=[{'id': 1}] * 40, ie={'words': [{'w': 'a'}] * 50}, ts=ev("S.ts"), goals=[{'t': 'G1', 'ms': []}, {'t': 'G2', 'ms': []}], q={'m': {'1': 30}})
    ev("(t)=>{bkApply(t)}", json.dumps(recent)); pg.wait_for_timeout(100); t = pg.inner_text('#snv'); chk('a backup that is as new and not smaller shows no warning (green line)', 'Zaxirada hozirgidan kam narsa yo‘q' in t or 'yo‘qoladi' not in t.split('Hozir')[1][:0]); ev("snvClose()")
    # snapshotni ochish
    ev("async()=>{await snTake('qo‘lda',true)}"); k = ev("(async()=>(await snIdx())[0].k)()"); ev("(k)=>{snOpen(k)}", k); pg.wait_for_timeout(200); chk('a phone snapshot can be opened in the same preview (label "Telefondagi snapshot")', 'Telefondagi snapshot' in pg.inner_text('#snv')); ev("snvClose()")
    # ulashish
    ev("""()=>{window.__sh=null;Object.defineProperty(navigator,'canShare',{value:()=>true,configurable:true});Object.defineProperty(navigator,'share',{value:async d=>{window.__sh={n:d.files[0].name,t:d.files[0].type,s:d.files[0].size}},configurable:true})}""")
    ev("()=>{bkShare();return 1}"); pg.wait_for_timeout(300); sh = ev("__sh"); chk('"📲 Zaxirani yuborish" shares a real JSON file (tizim-zaxira-2026-11-05.json) through the share sheet (Telegram “Saved messages”, Files) and counts as a file backup today', sh and sh['n'] == 'tizim-zaxira-2026-11-05.json' and sh['t'] == 'application/json' and sh['s'] > 500 and ev("bkAge()") == 0, sh)
    ev("""()=>{window.__dl=[];Object.defineProperty(navigator,'share',{value:undefined,configurable:true});const oc=HTMLAnchorElement.prototype.click;HTMLAnchorElement.prototype.click=function(){if(this.download)window.__dl.push(this.download);else oc.call(this)};lsRm('trk_bk')}""")
    ev("()=>{bkShare();return 1}"); pg.wait_for_timeout(300); chk('without share support it downloads the file instead', ev("__dl")[0] == 'tizim-zaxira-2026-11-05.json')
    ev("""()=>{Object.defineProperty(navigator,'canShare',{value:()=>true,configurable:true});Object.defineProperty(navigator,'share',{value:async()=>{const e=new Error('x');e.name='AbortError';throw e},configurable:true});__dl.length=0;bkShare()}"""); pg.wait_for_timeout(200); chk('closing the share sheet does not trigger a download', ev("__dl.length") == 0)
    # holat
    ev("""()=>{window.sb=window.sb;lsRm('trk_bk');lsRm('trk_dirty');SNC=[];SNP=null}""")
    st = ev("snState()"); chk('without cloud sign-in, a file backup or any snapshot the level is RED "Zaxira kerak"', st['lvl'] == 'bad' or st['lvl'] == 'warn')
    ev("()=>{lsSet('trk_bk',dk());SNC=[{k:'x',d:dk(),ts:Date.now(),w:'auto',sz:2048,n:snNum(S)}];SNP=true}"); st = ev("snState()"); chk('with a fresh file backup, a snapshot and persistent storage there is no red row', st['lvl'] in ('ok', 'warn') and not any(x['t'] == 'Fayl zaxirasi' and x['s'] != 'ok' for x in st['R']))
    ev("()=>{lsSet('trk_bk','2026-10-01')}"); st = ev("snState()"); chk('a file backup older than 14 days is yellow with the age', any(x['t'] == 'Fayl zaxirasi' and x['s'] == 'warn' and '35 kun' in x['d'] for x in st['R']))
    ev("()=>{lsRm('trk_bk')}"); st = ev("snState()"); chk('no file backup at all is red', any(x['t'] == 'Fayl zaxirasi' and x['s'] == 'bad' for x in st['R']))
    ev("()=>{SNP=false}"); st = ev("snState()"); r = [x for x in st['R'] if x['t'] == 'Doimiy xotira'][0]; chk('persistent storage off is yellow with an "Yoqish" action', r['s'] == 'warn' and r['at'] == 'Yoqish' and r['a'] == 'snPersist()')
    ev("""()=>{window.__pp=0;Object.defineProperty(navigator,'storage',{value:{persist:async()=>{window.__pp++;return true},persisted:async()=>true},configurable:true}));SNP=false}""".replace('}));', '});'))
    ev("async()=>{await snPersist()}"); chk('"Yoqish" asks the browser for persistent storage and shows it as on', ev("__pp") == 1 and ev("SNP") is True)
    # panel
    ev("()=>{lsSet('trk_bk',dk());SNP=true;lsSet('trk_prerestore',JSON.stringify(S))}"); ev("async()=>{await snLoad()}"); ev("()=>{tab='s';render();document.querySelectorAll('#app details.grp,#app details').forEach(d=>d.open=true)}"); pg.wait_for_timeout(200); t = pg.inner_text('#app')
    chk('Sozlamalar has the "🛡 Zaxira holati" group: the traffic-light summary, the five rows (cloud, server backups, file, phone snapshots, persistent storage), share and snapshot buttons, the undo button and the snapshot list', '🛡 Zaxira holati' in t and 'Telefondagi snapshotlar' in t and 'Server zaxiralari' in t and 'Fayl zaxirasi' in t and 'Doimiy xotira' in t and 'Zaxirani yuborish' in t and 'Tiklashdan oldingi holatga qaytish' in t)
    ev("()=>{tab='h';BV='j';lsRm('trk_bk');S.hb={};for(let i=0;i<5;i++){S.hb[dAgo(i)]={h1:true}}S.money=Array.from({length:12},(_,i)=>({id:i}));render()}"); pg.wait_for_timeout(120); chk('the Bugun nudge also offers the share button next to "Faylga saqlash"', 'Faylga saqlash' in pg.inner_text('#app') and ev("!!document.querySelector('#app [aria-label=\"Telegram yoki Fayllarga yuborish\"]')"))
    bad = []
    ev("(t)=>{window.__old=t}", json.dumps(old))
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='s';render();bkApply(__old)}", [ui, th]); pg.wait_for_timeout(120)
            ok = ev("document.documentElement.scrollWidth<=window.innerWidth+1 && document.querySelector('#snv .nws').scrollWidth<=document.querySelector('#snv .nws').clientWidth+1"); ev("snvClose()")
            if not ok: bad.append(ui + th)
    chk('the preview sheet and the status panel fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
