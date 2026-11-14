# Vidjet: xulosa, yuborish, sozlama kartochkasi, Scriptable skripti. Soat: 2026-10-31 (shanba) 10:00.
import sys, json, subprocess
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('vidjet') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);S.hab=[{id:'h1',t:'Kitob'},{id:'h2',t:'Suv'},{id:'h3',t:'Zal'},{id:'h4',t:'Dam odati'}];S.hb={};S.hk={};S.hb[dk()]={h1:true,h2:true};S.hk[dk()]={h4:1};S.nm=S.nm||{d:{}};S.nm.d={};S.nm.d[dk()]={fajr:1,dhuhr:1,asr:2,maghrib:1,isha:0,vitr:1};S.q.ny={};S.q.ny[dk()]=1;S.q.ppd=3;S.fm={};S.fm[dk()]=25;S.top={};S.top[dk()]=[{t:'Misol',x:1},{t:'Hifz sabaq',x:0},{t:'Zal',x:0},{t:'To‘rtinchi',x:0}];
      S.bl=[{id:'a1',t:'Dars',s:540,e:600,d:[0,1,2,3,4,5,6]},{id:'b2',t:'Zal',s:1320,e:1380,d:[6]},{id:'c3',t:'Yakshanba ishi',s:1100,e:1160,d:[0]},{id:'uyqu9',t:'Uyqu',s:1000,e:1100,d:[0,1,2,3,4,5,6]}];S.ie.ex='2026-12-20';S.goals=[{t:'Tugagan',ms:[{t:'a',x:1}],p:0},{t:'IELTS 7.0',ms:[{t:'a',x:1},{t:'b',x:0}],p:0}];S.wd=undefined}""")
    sn = ev("wdSnap()")
    chk('the snapshot: weekday and date, habits done/total (the rest-day habit is left out: 2 of 3), 3 fard prayers (vitr not counted, missed ones not counted), hifz 1 of 3, focus 25', sn['v'] == 1 and sn['d'] == '2026-10-31' and sn['dow'] == 'Shanba' and sn['dd'] == '31 oktyabr' and sn['hab'] == [2, 3] and sn['nm'] == [3, 5] and sn['hf'] == [1, 3] and sn['fm'] == 25, sn)
    chk('top-3 (at most 3, with done flags), the first unfinished goal with its percent, days to the IELTS exam (50)', len(sn['top']) == 3 and sn['top'][0] == {'t': 'Misol', 'x': 1} and sn['gl'] == {'t': 'IELTS 7.0', 'p': 50} and sn['ie'] == 50, sn)
    chk('the next block today: after 10:00, the sleep block and other days\u2019 blocks excluded → "Dars" (09:00) already passed, so "Zal 22:00"', sn['nx'] == {'t': 'Zal', 'at': '22:00'}, sn['nx'])
    ev("S.bl=[]"); chk('no blocks left today → no "next" entry', ev("wdSnap().nx") is None); ev("S.ie.ex=''"); chk('without an exam date the snapshot has none', ev("wdSnap().ie") is None)
    s = json.dumps(sn, ensure_ascii=False); chk('privacy: the snapshot has no money, mood, water, notes or health keys, and stays small (under 1 KB)', not any(k in s for k in ['money', 'pul', 'mood', 'water', 'note', 'kayfiyat']) and len(s.encode()) < 1024, len(s.encode()))
    # push / on / off with a fake database
    ev("""()=>{window.__up=[];window.__del=[];window.__fail=null;window.wdDb=()=>({from:tb=>({upsert:async row=>{window.__up.push([tb,row]);return window.__fail?{error:{message:window.__fail}}:{error:null}},delete:()=>({eq:async(c,v)=>{window.__del.push([tb,c,v]);return {error:null}}})})});UID=null;tab='s';render()}""")
    ev("wdOn()"); chk('not signed in: a clear message and nothing happens', any('hisobga kiring' in x for x in ev("__t")) and ev("S.wd") is None)
    ev("UID='11111111-2222-3333-4444-555555555555'"); ev("wdOn()"); pg.wait_for_timeout(200)
    w = ev("S.wd"); chk('turning it on creates a random 32-hex secret and saves the switch', w['on'] == 1 and len(w['t']) == 32 and all(c in '0123456789abcdef' for c in w['t']))
    up = ev("__up"); chk('and sends the snapshot at once: one upsert to widget_snap with the user, the token and the snapshot', len(up) == 1 and up[0][0] == 'widget_snap' and up[0][1]['user_id'] == '11111111-2222-3333-4444-555555555555' and up[0][1]['token'] == w['t'] and up[0][1]['snap']['v'] == 1 and 'updated_at' in up[0][1])
    ev("wdPush()"); pg.wait_for_timeout(100); chk('an unchanged snapshot is not sent again within 10 minutes', len(ev("__up")) == 1)
    ev("S.fm[dk()]=40"); ev("wdPush()"); pg.wait_for_timeout(100); chk('a changed snapshot is sent', len(ev("__up")) == 2 and ev("__up[1][1].snap.fm") == 40)
    ev("wdPush(true)"); pg.wait_for_timeout(100); chk('"Hozir yangila" sends even when nothing changed', len(ev("__up")) == 3)
    ev("()=>{S.wd.on=0}"); ev("S.fm[dk()]=50"); ev("wdPush()"); pg.wait_for_timeout(100); chk('switched off: nothing is sent', len(ev("__up")) == 3); ev("S.wd.on=1")
    ev("()=>{window.__fail='relation \"public.widget_snap\" does not exist';WDQ={sig:'',t:0}}"); ev("wdPush(true)"); pg.wait_for_timeout(100); chk('a missing table gives a helpful instruction (run widget.sql)', 'widget.sql' in ev("WDG.err") and ev("WDG.busy") == 0)
    ev("()=>{window.__fail='Boshqa xato';WDQ={sig:'',t:0}}"); ev("wdPush(true)"); pg.wait_for_timeout(100); chk('another database error is shown as it is and does not break anything', ev("WDG.err") == 'Boshqa xato'); ev("window.__fail=null")
    old = ev("S.wd.t"); ev("wdNew()"); pg.wait_for_timeout(200); chk('"Kalitni almashtirish" makes a new secret (the old one stops working) and sends again', ev("S.wd.t") != old and len(ev("S.wd.t")) == 32 and ev("__up[__up.length-1][1].token") == ev("S.wd.t"))
    # settings card
    ev("()=>{WDG.err='';WDG.ok='10:05';render()}"); ev("document.querySelectorAll('#app details').forEach(d=>{if(d.textContent.includes('Vidjet'))d.open=true})"); pg.wait_for_timeout(60); t = pg.inner_text('#app')
    chk('Sozlama has the "📱 Vidjet (iPhone)" group: it shows it is on, the masked key (not the whole secret), the last update, the buttons and the 4 setup steps', 'Vidjet (iPhone)' in t and 'Yoqilgan' in t and ev("S.wd.t.slice(0,4)+'…'+S.wd.t.slice(-4)") in t and ev("S.wd.t") not in t and 'Oxirgi yangilash: 10:05' in t and all(s in t for s in ['Skriptni nusxalash', 'Hozir yangila', 'Kalitni almashtirish', 'Scriptable', 'widget.sql']))
    ev("window.__cp='';navigator.clipboard.writeText=async x=>{window.__cp=x}"); pg.click('#app details:has(summary:has-text("Vidjet")) button >> text=Skriptni nusxalash'); pg.wait_for_timeout(100); sc = ev("__cp")
    tok = ev("S.wd.t"); chk('the copied script holds this project\u2019s widget URL with the token and the public key, and no unreplaced placeholders', ('/functions/v1/widget?t=' + tok) in sc and '__URL__' not in sc and '__KEY__' not in sc and 'supabase.co' in sc and 'Bearer' in sc)
    open('/tmp/wd_script.js', 'w', encoding='utf-8').write(sc)
    res = subprocess.run(['node', '/mnt/user-data/outputs/tests/widget_script_test.js', '/tmp/wd_script.js'], capture_output=True, text=True, timeout=60)
    lines = [l for l in res.stdout.splitlines() if l.startswith(('PASS', 'FAIL'))]
    for l in lines: chk('Scriptable simulation: ' + l[5:], l.startswith('PASS'))
    chk('the Scriptable simulation ran all 13 checks without crashing', len(lines) == 13 and not res.stderr.strip(), res.stderr[:200])
    pg.click('#app details:has(summary:has-text("Vidjet")) button >> text="O‘chirish"'); pg.wait_for_timeout(200)
    chk('"O‘chirish" removes the row on the server (by user id) and switches it off', ev("__del") == [['widget_snap', 'user_id', '11111111-2222-3333-4444-555555555555']] and ev("S.wd") == {'on': 0, 't': ''})
    ev("render()"); ev("document.querySelectorAll('#app details').forEach(d=>{if(d.textContent.includes('Vidjet'))d.open=true})"); chk('after that the card offers to turn it on again and says what is (not) sent', 'Vidjetni yoqish' in pg.inner_text('#app') and 'Pul va salomatlik ma‘lumoti yuborilmaydi' in pg.inner_text('#app'))
