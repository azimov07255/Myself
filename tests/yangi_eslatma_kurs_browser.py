# Kurs eslatmalari: qatorlar, vaqtlar, shartlar, sozlama kartasi. Soat: 2026-11-03 10:00 (seshanba).
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('eslatma', when=(2026, 11, 3, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);window.aiOk=()=>true;
      S.rem=Object.assign(S.rem||{},{on:false,tg:false,ks:false,xs:false,yv:false,kw:false,kt:'18:00',xt:'20:00',yt:'19:30',blk:false,close:false,wake:false,nz:false,zk:false,rz:false,yo:false,custom:[]});S.hab=[];
      S.ie.kr={start:dk(),target:8,hrs:2,wks:12,exam:'',done:{},read:{}};S.ie.tests=[];S.ie.mock=[];S.ie.xd=[];S.ie.xdr={};S.ie.rmd={};S.ie.rmg=10;KS.sec='r';tab='e';IVW='y';render()}""")
    kinds = lambda: ev("remRows().map(r=>r.kind)"); rows = lambda: ev("remRows()")
    chk('with notifications and Telegram off there are no reminder rows at all (the course adds nothing)', rows() == [])
    ev("()=>{S.rem.on=true}"); chk('notifications on but every course reminder off: no course rows', not any(k in ('ks', 'xs', 'yv') or str(k).startswith('ksw') for k in kinds()))
    ev("()=>{S.rem.ks=true}"); r = [x for x in rows() if x['kind'] == 'ks']
    chk('"Kun vazifalari": one row at 18:00 every day, titled with the current week, listing up to 3 open tasks (strategy tasks start with 📖)', len(r) == 1 and r[0]['hhmm'] == '18:00' and r[0]['days'] == [0, 1, 2, 3, 4, 5, 6] and r[0]['title'] == '🎓 IELTS kursi: 1-hafta' and r[0]['body'].startswith('Bugun: 📖 ball hisoblash va imtihon kuni; ') and r[0]['body'].count(';') == 2 and len(r[0]['body']) <= 170, r)
    ev("ksRemTime('kt','19:15')"); chk('the time is changeable and applies to the row; an invalid time is ignored', [x['hhmm'] for x in rows() if x['kind'] == 'ks'] == ['19:15'] and not ev("ksRemTime('kt','bad')") and ev("S.rem.kt") == '19:15')
    sig0 = ev("JSON.stringify(remRows())"); ev("()=>{S.ie.kr.done.w1a='x'}"); sig1 = ev("JSON.stringify(remRows())")
    chk('the row text changes when you finish a task (so the new text is sent to the server at the next sync)', sig0 != sig1 and 'ball hisoblash' not in ev("remRows().find(r=>r.kind==='ks').body"))
    ev("()=>{const p=ksPlan();p[0].k.forEach(t=>{S.ie.kr.done['w1'+t.id]='x'})}"); chk('when every task of the week is done there is no "Kun vazifalari" row', 'ks' not in kinds())
    ev("()=>{S.ie.kr.done={};S.rem.ks=false}")
    ev("()=>{S.rem.xs=true}"); chk('"Xatolarni takrorlash": no row while nothing is due', 'xs' not in kinds())
    ev("()=>{for(let i=0;i<5;i++)xdPut('grammar','wrong '+i,'right '+i,'','m')}"); r = [x for x in rows() if x['kind'] == 'xs']
    chk('with 5 mistakes due: a row at 20:00 saying how many and roughly how long it takes (2 minutes)', len(r) == 1 and r[0]['hhmm'] == '20:00' and r[0]['body'] == '5 ta xato takrorlashga tayyor (taxminan 2 daqiqa).' and r[0]['title'] == '📓 Xatolarni takrorlash', r)
    ev("()=>{S.ie.xd.forEach(x=>{x.due=ksAdd(dk(),3)})}"); chk('mistakes that are due later do not count', 'xs' not in kinds()); ev("()=>{S.rem.xs=false}")
    ev("()=>{S.rem.yv=true;S.ie.rmd={[dk()]:3}}"); r = [x for x in rows() if x['kind'] == 'yv']
    chk('"Bugungi so‘zlar": while the daily goal is not reached there is a 19:30 row with the progress (3 / 10)', len(r) == 1 and r[0]['hhmm'] == '19:30' and r[0]['body'].startswith('Bugungi maqsad: 3 / 10'), r)
    ev("()=>{S.ie.rmd={[dk()]:10}}"); chk('once the goal is reached the row disappears', 'yv' not in kinds()); ev("()=>{S.rem.yv=false;S.ie.rmd={}}")
    ev("()=>{S.rem.kw=true;S.ie.rmd={[dk()]:12};S.ie.xdr={[dk()]:7};S.ie.kr.done={w1a:'x'}}"); r = [x for x in rows() if str(x['kind']).startswith('ksw')]
    chk('"Haftalik xulosa": one row on Sundays at 20:45, tied to the coming Sunday (2026-11-08), summarising tasks, new words and reviewed mistakes', len(r) == 1 and r[0]['kind'] == 'ksw@2026-11-08' and r[0]['days'] == [0] and r[0]['hhmm'] == '20:45' and r[0]['body'] == '1-hafta: 1/6 vazifa bajarildi; oxirgi 7 kunda 12 ta yangi so‘z, 7 ta xato takrorlandi.', r)
    ev("()=>{S.ie.kr.start=ksAdd(dk(),-200)}"); chk('after the course is over there are no course rows', not any(k in ('ks',) or str(k).startswith('ksw') for k in kinds()))
    ev("()=>{S.ie.kr=null;S.rem.ks=true;S.rem.xs=true;S.rem.yv=true}"); chk('without a started course only the notebook and word reminders can appear', 'ks' not in kinds() and not any(str(k).startswith('ksw') for k in kinds()))
    ev("()=>{S.ie.kr={start:dk(),target:8,hrs:2,wks:12,exam:'',done:{},read:{}};S.rem.ks=false;S.rem.xs=false;S.rem.yv=false;S.rem.kw=false}")
    chk('the existing reminders are untouched: an enabled custom reminder is still there next to the course ones', ev("(()=>{S.rem.custom=[{id:1,time:'07:00',t:'Water'}];S.rem.ks=true;const k=remRows().map(r=>r.title);S.rem.custom=[];return k.includes('Water')&&k.some(x=>x.startsWith('🎓'))})()"))
    ev("()=>{S.rem.ks=false}")
    # ---------- sozlama kartasi ----------
    ev("()=>{S.rem.on=false;S.rem.tg=false;KS.sec='r';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('the course settings have a "🔔 Kurs eslatmalari" card with four switches; without notifications it explains why nothing will arrive and offers the Settings button', '🔔 Kurs eslatmalari' in t and ev("document.querySelectorAll('#app [role=switch]').length") == 4 and 'avval bildirishnoma yoki Telegram yoqilgan' in t and 'Sozlamaga o‘tish' in t)
    ev("()=>{S.rem.on=true;render()}"); pg.wait_for_timeout(60); chk('with notifications on the warning is gone', 'avval bildirishnoma yoki Telegram' not in pg.inner_text('#app'))
    pg.click('#app [role=switch] >> nth=0'); pg.wait_for_timeout(80); chk('tapping a switch turns it on (✓, aria-checked) and reveals its time field', ev("S.rem.ks") is True and ev("document.querySelectorAll('#app [role=switch]')[0].getAttribute('aria-checked')") == 'true' and ev("document.querySelectorAll('#app .goal:has([role=switch]) input[type=time]').length") == 1)
    pg.fill('#app .goal:has([role=switch]) input[type=time]', '17:30'); pg.dispatch_event('#app .goal:has([role=switch]) input[type=time]', 'change'); pg.wait_for_timeout(80); chk('changing the time saves it', ev("S.rem.kt") == '17:30' and ev("remRows().find(r=>r.kind==='ks').hhmm") == '17:30')
    pg.click('#app [role=switch] >> nth=3'); pg.wait_for_timeout(80); chk('the weekly summary switch has no time field (fixed Sunday 20:45)', ev("S.rem.kw") is True and ev("document.querySelectorAll('#app .goal:has([role=switch]) input[type=time]').length") == 1)
    pg.click('#app [role=switch] >> nth=0'); pg.wait_for_timeout(80); chk('tapping again turns it off', ev("S.rem.ks") is False)
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1]}", [ui, th]); pg.wait_for_timeout(50)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('the card does not overflow the phone screen in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
