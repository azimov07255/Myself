# Ishonchlilik: ikki qurilma o'rtasida qo'shish, zaxira, server eslatma formati. Soat: 2026-11-09 10:00.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
AUD = """(()=>{const res=[];function walk(o,p){if(Array.isArray(o)){if(o.length&&o.every(x=>x&&typeof x==='object'&&!Array.isArray(x))){const ids=o.map(x=>x.id);const noid=ids.some(i=>i===undefined);const dup=!noid&&new Set(ids).size!==ids.length;if((noid||dup)&&p!=='S.pr.st')res.push(p+' ['+o.length+'] '+(noid?'NOID':'DUPID'))}o.forEach((x,i)=>{if(x&&typeof x==='object')walk(x,p+'['+i+']')})}else if(o&&typeof o==='object'){Object.keys(o).forEach(k=>walk(o[k],p+'.'+k))}}walk(S,'S');return res})()"""
with Run('ish', when=(2026, 11, 9, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;S.q.m[1]=10;S.q.tk=undefined;S.nf=undefined;S.km=[];S.kv={};S.f5=[];
      tqLog({m:'b',pa:1,pb:1,pg:2,t:'x'});tqLog({m:'b',pa:1,pb:1,pg:2,t:'y',w:'n'});nkAdd('pom',3,1000,[]);kmPre(0);kmSet(S.km[0].id,3);
      f5Start('Dokon');F5.ph='ask';f5Enough();f5Start('Dokon');F5.ph='ask';f5Enough();nkS().dv=5000;nkPay(2000);nkPay(1000);
      nkS().c[0].s='2026-11-01';nkS().c[0].e='2026-11-01';S.pm={};nkEval();S.ik={h:6,d:{}};S.ex={'2026-11-09':{a:1}};S.ov={'2026-11-09':{a:{s:1,e:2}}};S.kc={'2026-11-09':1};S.ie.cm={'17-2-L':{raw:30,band:7,d:dk()}}}""")
    A = ev(AUD); chk('after using every new feature there is NO list in the saved data that two devices could not merge safely (every list item has a unique id; the old index-based license-steps list is the only exception)', A == [], A)
    chk('new ⚡ 5-minute entries, sadaqa payments and contract breaches get unique ids when they are created', all(isinstance(e['id'], str) and e['id'] for e in ev("S.f5")) and len({e['id'] for e in ev("S.f5")}) == 2 and all(e['id'] for e in ev("nkS().pd")) and all(e['id'].startswith('g') and 'cid' in e for e in ev("nkS().lg")), (ev("S.f5"), ev("nkS().lg")[:2]))
    # eski ma'lumotni ko'chirish
    ev("""()=>{S.f5=[{d:'2026-11-01',t:'a',c:0,m:5},{d:'2026-11-01',t:'a',c:0,m:5},{d:'2026-11-02',t:'b',c:1,m:30}];S.nf.lg=[{d:'2026-11-01',id:777,v:0,n:3,pen:10,m:'pom'},{d:'2026-11-02',id:777,v:1,n:3,pen:10,m:'pom'}];S.nf.pd=[{d:'2026-11-03',a:1000},{d:'2026-11-03',a:1000}]}""")
    ev("syIds(S)"); f5 = ev("S.f5.map(e=>e.id)"); lg = ev("S.nf.lg"); pd = ev("S.nf.pd.map(e=>e.id)")
    chk('old saved entries get stable ids: identical ⚡ entries on the same day are told apart (#1, #2); contract breaches keep their contract id in “cid” and get their own id; payments get ids', len(set(f5)) == 3 and f5[0].endswith('#1') and f5[1].endswith('#2') and [e['cid'] for e in lg] == [777, 777] and len({e['id'] for e in lg}) == 2 and len(set(pd)) == 2, (f5, lg, pd))
    before = ev("JSON.stringify([S.f5,S.nf.lg,S.nf.pd])"); ev("syIds(S);syIds(S)"); chk('running it again changes nothing (ids never change once given)', ev("JSON.stringify([S.f5,S.nf.lg,S.nf.pd])") == before)
    chk('loading data from the cloud or from a restore applies the same fix (norm)', ev("(()=>{const o=norm({f5:[{d:'2026-11-01',t:'z',c:0,m:5}],nf:{c:[],lg:[],pd:[{d:'2026-11-01',a:5}],x:[],bq:{},dv:0}});return !!o.f5[0].id&&!!o.nf.pd[0].id})()"))
    # ikki qurilma
    ev("""()=>{S.f5=[];S.nf.lg=[];S.nf.pd=[];S.km=[];S.kv={};S.q.tk=undefined;S.nf.c=[];
      window.__B=JSON.parse(JSON.stringify(norm(JSON.parse(JSON.stringify(S)))));
      const mk=()=>JSON.parse(JSON.stringify(window.__B));
      const A=mk(),Bd=mk();
      A.f5=[{id:'f5:a1',d:'2026-11-09',t:'Dokon',c:0,m:5}];Bd.f5=[{id:'f5:b1',d:'2026-11-09',t:'Zal',c:1,m:30}];
      A.nf=A.nf||{};A.nf.pd=[{id:'p:a',d:'2026-11-09',a:1000}];Bd.nf=Bd.nf||{};Bd.nf.pd=[{id:'p:b',d:'2026-11-09',a:5000}];
      A.nf.lg=[{id:'g1',cid:1,d:'2026-11-08',v:0,n:3,pen:10,m:'pom'}];Bd.nf.lg=[{id:'g2',cid:1,d:'2026-11-09',v:0,n:3,pen:10,m:'pom'}];
      A.km=[{id:'ma',t:'Suv',ty:'num',u:'',g:8,dir:'up'}];Bd.km=[{id:'mb',t:'Vazn',ty:'num',u:'kg',g:0,dir:'down'}];
      A.kv={'2026-11-09':{ma:5}};Bd.kv={'2026-11-09':{mb:70}};
      A.q.tk={g:{u:'bet',n:5},gn:{u:'bet',n:0},d:{'2026-11-09':[{id:'t1',m:'b',pg:3,t:'A'}]},cy:{on:0,days:30,start:'',p:0,n:0,last:''},cyn:{on:0,days:30,start:'',p:0,n:0,last:''}};
      Bd.q.tk={g:{u:'bet',n:5},gn:{u:'bet',n:0},d:{'2026-11-09':[{id:'t2',m:'b',pg:4,t:'B',w:'n'}]},cy:{on:0,days:30,start:'',p:0,n:0,last:''},cyn:{on:0,days:30,start:'',p:0,n:0,last:''}};
      window.__M=mrg(window.__B,A,Bd)}""")
    ids = lambda path: sorted(ev("(p)=>{let o=window.__M;for(const k of p.split('.'))o=o&&o[k];return (o||[]).map(x=>x.id)}", path))
    chk('two devices that each added something while offline do not overwrite each other: both ⚡ entries, both sadaqa payments, both contract-breach records and both takror entries survive the merge', ids('f5') == ['f5:a1', 'f5:b1'] and ids('nf.pd') == ['p:a', 'p:b'] and ids('nf.lg') == ['g1', 'g2'] and sorted(ev("window.__M.q.tk.d['2026-11-09'].map(x=>x.id)")) == ['t1', 't2'])
    chk('…and both devices’ own metrics (🧮 Suv and Vazn) and their daily values are kept', ids('km') == ['ma', 'mb'] and ev("window.__M.kv['2026-11-09']") == {'ma': 5, 'mb': 70})
    ev("""()=>{const mk=()=>JSON.parse(JSON.stringify(window.__M));const A=mk(),Bd=mk();A.q.tk.d['2026-11-09']=A.q.tk.d['2026-11-09'].filter(x=>x.id!=='t1');window.__M2=mrg(window.__M,A,Bd)}""")
    chk('deleting a takror entry on one device really removes it after the merge (the other device does not bring it back)', sorted(ev("window.__M2.q.tk.d['2026-11-09'].map(x=>x.id)")) == ['t2'])
    # zaxira
    ev("""()=>{S.f5=[{id:'f5:z',d:'2026-11-09',t:'x',c:0,m:5}];S.km=[{id:'mz',t:'Suv',ty:'num',u:'',g:8,dir:'up'}];S.kv={'2026-11-09':{mz:4}};S.rt={d:{'2026-11-09':{w1:{q:'x',m:5,r:3,h:10,t:'T'}}},sk:{}};S.ik={h:5,d:{'2026-11-09':{x:{W:1},m:{W:60}}}};S.ex={'2026-11-09':{b1:1}};S.ov={'2026-11-09':{b1:{s:600,e:660}}};S.kc={'2026-11-09':1};S.ie.cm={'17-2-L':{raw:30,band:7,d:'2026-11-09'}};tqLog({m:'b',pa:1,pb:1,pg:3,t:'q'});S.q.tk.cyn.on=1;
      window.__BK=JSON.stringify(S);window.__R=norm(Object.assign(blank(),JSON.parse(window.__BK)))}""")
    keys = ev("['f5','km','kv','rt','ik','ex','ov','kc','ie','nf'].every(k=>JSON.stringify(window.__R[k])===JSON.stringify(S[k]))")
    chk('a backup (the exact text the app exports) restored through the same loader brings back every new section: ⚡, metrics, metric values, rituals, IELTS day, exclusions, shifts, closed days, Cambridge grid, Nafs data', keys and ev("JSON.stringify(window.__R.q.tk)==JSON.stringify(S.q.tk)"))
    # server formati
    ev("""()=>{S.rem.on=true;S.rem.blk=true;S.rem.off=10;S.bl=[{id:'k1',t:'Dokon',s:540,e:1020,tr:20,d:[0,1,2,3,4,5,6]},{id:'o5',t:'Bir kunlik',s:660,e:720,tr:25,d:[3],on:'2026-11-11'},{id:'x9',t:'Uzoq',s:660,e:720,d:[3],on:'2026-11-25'}]}""")
    rows = ev("remRows().map(r=>[r.kind,r.title,r.days,r.hhmm])")
    def srv(kind):
        at = kind.find('@'); base = kind[:at] if at >= 0 else kind; only = kind[at + 1:] if at >= 0 else ''
        return base, only
    dated = [r for r in rows if '@' in str(r[0])]
    chk('server rule: a date-bound reminder is “<base>@<YYYY-MM-DD>” and nothing after the date — the server compares exactly that text with today’s date. Our one-day reminders now follow it (blk:o5@2026-11-11, tr:o5@2026-11-11)', len(dated) == 2 and all(len(srv(r[0])[1]) == 10 and srv(r[0])[1] == '2026-11-11' for r in dated) and {srv(r[0])[0] for r in dated} == {'blk:o5', 'tr:o5'}, rows)
    chk('regular repeating reminders have no “@” at all, so they keep firing every week, and a one-day block 14 days away gets none yet', all('@' not in str(r[0]) for r in rows if r[0] in ('blk:k1', 'tr:k1')) and not any('x9' in str(r[0]) for r in rows))
    chk('the date-bound rows fire only on their weekday (Wednesday = 3) at the right minute (blk: 10:50, tr: 10:35)', all(r[2] == [3] for r in dated) and sorted(r[3] for r in dated) == ['10:35', '10:50'])
