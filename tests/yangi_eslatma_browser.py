import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Eslatmalar auditi: mijozning eslatma qatorlari serverning (send-reminders.ts) haqiqiy mantig'i bo'yicha sinovdan o'tkaziladi. Soat: 2026-11-09 (dushanba) 07:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
SRV = """(()=>{window.srv=(rows,nowMs,st)=>{const fired=[],del=[];rows.forEach((r,i)=>{const loc=new Date(nowMs+(r.tz??300)*60000);const date=loc.toISOString().slice(0,10),nowMin=loc.getUTCHours()*60+loc.getUTCMinutes();const [h,m]=r.hhmm.split(':').map(Number);const delta=nowMin-(h*60+m),stamp=date+' '+r.hhmm;const kf=String(r.kind||''),at=kf.indexOf('@');const only=at>=0?kf.slice(at+1):'';if(only&&only!==date){if(only<date)del.push(i);return}if(delta<0||delta>2||!r.days.includes(loc.getUTCDay())||st[i]===stamp)return;fired.push(i);st[i]=stamp});return{fired,del}};
 window.simDay=(rows,y,mo,d)=>{const st={},out=rows.map(()=>[]);for(let mi=0;mi<1440;mi++){const tz=rows.length?(rows[0].tz??0):0;const ms=Date.UTC(y,mo-1,d,Math.floor(mi/60),mi%60)-tz*60000;const r=srv(rows,ms,st);r.fired.forEach(i=>out[i].push(mi))}return out}})()"""
with Run('es', when=(2026, 11, 9, 7, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev(SRV)
    ev("""()=>{window.toast=()=>{};window.ptTimes=()=>({Fajr:300,Dhuhr:735,Asr:900,Maghrib:1070,Isha:1180});
      S.rem={on:true,tg:false,blk:true,off:10,close:true,ct:'21:00',wake:false,nz:true,noff:10,zk:true,zam:'06:30',zpm:'18:30',yo:false,rz:false,custom:[{t:'Suv ich',time:'11:00'}]};
      S.hab=[{id:'h1',t:'Kitob',rt:'20:00',e:'📖',x:0}];
      S.bl=[{id:'uyqu1',t:'Uxlash',s:1380,e:1800,d:[0,1,2,3,4,5,6]},{id:'k1',t:'Dokon',s:540,e:1020,tr:20,d:[0,1,2,3,4,5,6]},{id:'w1',t:'IELTS Writing',s:480,e:600,d:[1,3,5]},{id:'e0',t:'Erta',s:5,e:30,d:[1]},{id:'o1',t:'Bir kunlik',s:660,e:720,tr:25,d:[3],on:'2026-11-11'},{id:'o0',t:'Otgan',s:660,e:720,d:[4],on:'2026-11-05'},{id:'o9',t:'Uzoq',s:660,e:720,d:[3],on:'2026-11-25'}];
      S.ex=undefined;S.ov=undefined;S.done={}}""")
    rows = ev("remRows()")
    import re
    kinds = [r.get('kind') for r in rows]
    chk('all reminder kinds follow the server’s rule “<base>[:id][@YYYY-MM-DD]” and nothing after the date; no row exists for blocks that are in the past or more than 7 days ahead (Otgan, Uzoq) or that would start before 00:00 after the lead time (Erta)', all((k is None) or re.fullmatch(r'[a-z]{1,3}(:[\w-]+)?(@\d{4}-\d\d-\d\d)?', k) for k in kinds) and not any('o0' in str(k) or 'o9' in str(k) or 'e0' in str(k) for k in kinds), kinds)
    chk('every row is well-formed for the server: time “HH:MM” in 00:00–23:59, weekdays 0–6 (not empty), a non-empty title, a numeric time-zone offset', all(re.fullmatch(r'([01]\d|2[0-3]):[0-5]\d', r['hhmm']) and r['days'] and all(isinstance(d, int) and 0 <= d <= 6 for d in r['days']) and r['title'] and isinstance(r['tz'], (int, float)) for r in rows), [r for r in rows if not re.fullmatch(r'([01]\d|2[0-3]):[0-5]\d', r['hhmm'])])
    chk('date-bound rows are only for the coming 7 days', all('2026-11-09' <= k.split('@')[1] <= '2026-11-16' for k in kinds if k and '@' in k), [k for k in kinds if k and '@' in k])
    chk('the same reminder is never sent twice by a duplicated row (no two rows share kind, time and weekdays)', len({(r.get('kind'), r['hhmm'], tuple(r['days'])) for r in rows if r.get('kind')}) == len([r for r in rows if r.get('kind')]))
    tg = lambda k: bool(re.fullmatch(r'nm:\w+', k) or re.fullmatch(r'blk:[\w-]+', k) or re.fullmatch(r'zk:(sb|sh)', k) or k == 'rz')
    base = lambda k: k.split('@')[0]
    chk('Telegram buttons: every block reminder (also the one-day ones) maps to the “✅ Bajardim” button and its callback fits Telegram’s 64-byte limit', all(tg(base(k)) and len(base(k).encode()) <= 64 for k in kinds if k and k.startswith('blk:')) and all(tg(base(k)) for k in kinds if k and k.startswith(('nm:', 'zk:'))))
    # simulyatsiya: dushanba, seshanba, chorshanba
    S1 = ev("simDay(remRows(),2026,11,9)"); S2 = ev("simDay(remRows(),2026,11,10)"); S3 = ev("simDay(remRows(),2026,11,11)")
    idx = lambda kind: [i for i, r in enumerate(rows) if r.get('kind') == kind]
    hm_ = lambda m: '%02d:%02d' % (m // 60, m % 60)
    def fires(S, kind): return [hm_(m) for i in idx(kind) for m in S[i]]
    chk('server simulation (every minute of 3 days): the daily Dokon reminder fires exactly once per day at 08:50 (09:00 minus the 10-minute lead) — never twice within the 2-minute window', fires(S1, 'blk:k1') == ['08:50'] and fires(S2, 'blk:k1') == ['08:50'] and fires(S3, 'blk:k1') == ['08:50'])
    chk('the weekly IELTS Writing reminder (Mon/Wed/Fri) fires on Monday and Wednesday at 07:50 but not on Tuesday; the 5-minute block (Erta) never fires', fires(S1, 'blk:w1') == ['07:50'] and fires(S2, 'blk:w1') == [] and fires(S3, 'blk:w1') == ['07:50'])
    chk('the “yo‘lga chiqish” reminder fires 20 minutes before the block (08:40) every day', fires(S1, 'tr:k1') == ['08:40'] and fires(S2, 'tr:k1') == ['08:40'])
    chk('the one-day block fires ONLY on its date (Wednesday 10 Nov+1 = 11 Nov): at 10:50, with its travel reminder at 10:35; not on Monday or Tuesday', fires(S1, 'blk:o1@2026-11-11') == [] and fires(S2, 'blk:o1@2026-11-11') == [] and fires(S3, 'blk:o1@2026-11-11') == ['10:50'] and fires(S3, 'tr:o1@2026-11-11') == ['10:35'])
    chk('prayer, zikr, habit, custom and close-the-day reminders each fire once a day at their time (Fajr 04:50, Zikr 06:30 and 18:30, habit 20:00, custom 11:00, close 21:00)', fires(S1, 'nm:fajr') == ['04:50'] and fires(S1, 'zk:sb') == ['06:30'] and fires(S1, 'zk:sh') == ['18:30'] and fires(S1, 'hb:h1') == ['20:00'] and [hm_(m) for i, r in enumerate(rows) if r['title'] == 'Suv ich' for m in S1[i]] == ['11:00'] and [hm_(m) for i, r in enumerate(rows) if r['title'] == 'Kunni yopish vaqti' for m in S1[i]] == ['21:00'])
    chk('the server deletes date-bound rows once their date has passed (one-day reminders disappear on their own the next day)', len(ev("srv(remRows(),Date.UTC(2026,10,12,9,0)-remRows()[0].tz*60000,{}).del")) >= 2)
    # S.ex va S.ov
    ev("()=>{S.ex={'2026-11-09':{w1:1}}}"); rw = ev("remRows()"); S1b = ev("simDay(remRows(),2026,11,9)"); S3b = ev("simDay(remRows(),2026,11,11)")
    ii = lambda R_, kind: [i for i, r in enumerate(R_) if r.get('kind') == kind]
    f = lambda R_, S, kind: [hm_(m) for i in ii(R_, kind) for m in S[i]]
    chk('a block you moved off today (“ertaga ko‘chirish”) no longer reminds you today (IELTS Writing excluded on Monday) but still does on Wednesday and Friday', f(rw, S1b, 'blk:w1') == [] and f(rw, S3b, 'blk:w1') == ['07:50'] and [r for r in rw if r.get('kind') == 'blk:w1'][0]['days'] == [3, 5])
    ev("()=>{S.ex=undefined;S.ov={'2026-11-09':{k1:{s:630,e:1020}}}}"); ro = ev("remRows()"); So = ev("simDay(remRows(),2026,11,9)"); So2 = ev("simDay(remRows(),2026,11,10)")
    chk('a block you shifted today (“Kechikdim”: Dokon now 10:30) reminds at the NEW time today only (10:20) and not at the old 08:50; its travel reminder follows (10:10)', f(ro, So, 'blk:k1') == [] and f(ro, So, 'blk:k1@2026-11-09') == ['10:20'] and f(ro, So, 'tr:k1@2026-11-09') == ['10:10'] and f(ro, So, 'tr:k1') == [], (f(ro, So, 'blk:k1@2026-11-09'), f(ro, So, 'tr:k1@2026-11-09')))
    chk('…tomorrow the normal reminders are back (08:50 and 08:40)', f(ro, So2, 'blk:k1') == ['08:50'] and f(ro, So2, 'tr:k1') == ['08:40'])
    ev("()=>{S.ov={'2026-11-10':{k1:{s:600,e:1020}}}}"); rt = ev("remRows()"); chk('a shift planned for tomorrow is also honoured (the 10:00 start reminds at 09:50 on Tuesday)', f(rt, ev("simDay(remRows(),2026,11,10)"), 'blk:k1@2026-11-10') == ['09:50'] and f(rt, ev("simDay(remRows(),2026,11,10)"), 'blk:k1') == [])
    pg.clock.set_system_time('2026-11-09T11:00:00'); ev("()=>{S.ov={'2026-11-09':{k1:{s:630,e:1020}}}}"); chk('…and a shifted block whose new reminder time has already passed today is not scheduled for today at all', not any(r.get('kind') == 'blk:k1@2026-11-09' for r in ev("remRows()"))); pg.clock.set_system_time('2026-11-09T07:00:00')
    ev("()=>{S.ex={'2026-11-09':{w1:1}};S.bl=S.bl.map(b=>b.id==='w1'?Object.assign({},b,{d:[1]}):b)}"); chk('a block that exists only on that weekday and is excluded has no weekly row left for today (nothing is sent)', not any(r.get('kind') == 'blk:w1' for r in ev("remRows()")))
    ev("()=>{S.rem.on=false;S.rem.tg=false}"); chk('with reminders switched off there are no rows at all', ev("remRows().length") == 0)
