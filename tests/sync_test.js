// Sinxronlash, birlashtirish, zaxira va xatolarni yig'ish sinovlari (ikkita "qurilma" bitta soxta server bilan)
const fs=require('fs'),vm=require('vm');
const SRC=fs.readFileSync(process.env.APP_JS||'/tmp/t.js','utf8');
const ok=(l,c)=>{console.log((c?'PASS ':'FAIL ')+l);if(!c)process.exitCode=1};
const server={row:null,rpc:true,revcol:true,hist:[],errors:[],calls:[]};
const clone=o=>JSON.parse(JSON.stringify(o));
function makeDevice(name){
  const ls={};const toasts=[];
  const sb={
    auth:{getSession:async()=>({data:{session:null}}),signOut:async()=>{}},
    rpc:async(fn,args)=>{server.calls.push(fn);if(!server.rpc)return{error:{code:'PGRST202',message:'Could not find the function public.save_state'}};
      const{p_data,p_base}=args;
      if(!server.row){server.row={data:clone(p_data),rev:1};return{data:{ok:true,rev:1}}}
      if(p_base===server.row.rev){server.row={data:clone(p_data),rev:server.row.rev+1};return{data:{ok:true,rev:server.row.rev}}}
      return{data:{ok:false,rev:server.row.rev,data:clone(server.row.data)}}},
    from:tb=>({
      select:cols=>({eq:()=>({maybeSingle:async()=>{if(tb==='app_state'){if(/rev/.test(cols)&&!server.revcol)return{error:{message:'column app_state.rev does not exist'}};return{data:server.row?(/rev/.test(cols)?{data:clone(server.row.data),rev:server.row.rev}:{data:clone(server.row.data)}):null}}
          if(tb==='app_state_history'){const x=server.hist.find(h=>h.id===arguments[0]);return{data:server.hist[0]?clone(server.hist[0]):null}}return{data:null}}}),
        order:()=>({limit:async()=>({data:server.hist.map(h=>({id:h.id,day:h.day,kind:h.kind,created_at:'2026-10-25T10:00:00Z'}))})})}),
      upsert:async r=>{if(tb==='app_state'){server.row={data:clone(r.data),rev:server.row?server.row.rev:0};return{}}return{}},
      insert:async r=>{if(tb==='client_errors')server.errors.push(r);return{}},
      delete:()=>({eq:async()=>({}),neq:async()=>({})})}),
    storage:{from:()=>({})}};
  const app={_h:'',classList:{add(){},remove(){}},offsetWidth:0,set innerHTML(v){this._h=v},get innerHTML(){return this._h}};
  const mk=()=>({id:'',style:{},dataset:{},classList:{add(){},remove(){}},_h:'',set innerHTML(v){this._h=v},get innerHTML(){return this._h},remove(){},addEventListener(){},querySelector:()=>null});
  const win={addEventListener(){},scrollY:0,innerWidth:390,innerHeight:800,scrollTo(){},supabase:{createClient:()=>sb}};
  const sandbox={localStorage:{getItem:k=>ls[k]===undefined?null:ls[k],setItem:(k,v)=>{ls[k]=String(v)},removeItem:k=>{delete ls[k]}},
    window:win,supabase:win.supabase,console,JSON,Date,Math,Promise,Object,Array,Set,Map,String,Number,parseInt,parseFloat,isNaN,Intl,RegExp,Error,Symbol,encodeURIComponent,decodeURIComponent,URL,Blob,TextEncoder,TextDecoder,
    setTimeout:()=>0,clearTimeout(){},setInterval:()=>1,clearInterval(){},requestAnimationFrame:()=>0,
    confirm:()=>true,alert(){},scrollTo(){},matchMedia:()=>({matches:false,addEventListener(){}}),
    navigator:{onLine:true,vibrate(){},storage:{persist:async()=>true,persisted:async()=>false,estimate:async()=>({usage:5e6,quota:1e9})},userAgent:'TestUA'},
    document:{documentElement:{setAttribute(){},removeAttribute(){},classList:{add(){},remove(){}}},body:{appendChild(){},style:{}},querySelector:s=>s==='#app'?app:({value:'',content:'',innerHTML:''}),querySelectorAll:()=>[],activeElement:null,getElementById:()=>null,createElement:()=>mk(),head:{appendChild(){}},addEventListener(){}}};
  sandbox.__app=app;sandbox.globalThis=sandbox;vm.createContext(sandbox);
  const ex=`;S=load();UID='u1';S.ob=1;S.ts=S.ts||0;globalThis.T={get S(){return S},set S(v){S=v},get REV(){return REV},set REV(v){REV=v},get NORPC(){return NORPC},get SYNC(){return SYNC},push,pull,save,mrg,norm,blank,reportErr,render,get app(){return __app},histLoad,histRestore,histCard,get HIST(){return HIST},diagText,ensurePersist,sumS,errView,setTab(v){tab=v},get toasted(){return MERGED}}`;
  vm.runInContext(SRC+ex,sandbox);
  const T=sandbox.T;T.ls=ls;T.name=name;T.sb=sb;T.setApp=a=>a;return T}
(async()=>{
 // ---------- merge unit tests ----------
 const D=makeDevice('m'),mrg=D.mrg;
 const B={tasks:[{id:1,t:'a'},{id:2,t:'b'}],done:{'2026-10-24':{x:1}},name:'Aziz',n:1,days:[1,2]};
 let L=clone(B);L.tasks.push({id:3,t:'local'});let R=clone(B);R.tasks.push({id:4,t:'remote'});
 let m=mrg(B,L,R);ok('both devices add different items -> both kept (ids '+m.tasks.map(x=>x.id)+')',m.tasks.map(x=>x.id).sort().join()==='1,2,3,4');
 L=clone(B);L.tasks=L.tasks.filter(x=>x.id!==1);R=clone(B);R.tasks[1].t='b2';m=mrg(B,L,R);
 ok('local delete + remote edit of another item -> deletion kept AND remote edit applied',!m.tasks.some(x=>x.id===1)&&m.tasks.find(x=>x.id===2).t==='b2');
 L=clone(B);R=clone(B);R.tasks=R.tasks.filter(x=>x.id!==2);m=mrg(B,L,R);ok('remote delete of an item local did not touch -> stays deleted',!m.tasks.some(x=>x.id===2));
 L=clone(B);L.tasks[1].t='LOCAL-EDIT';R=clone(B);R.tasks=R.tasks.filter(x=>x.id!==2);m=mrg(B,L,R);ok('remote deleted but local edited the same item -> the edit is kept (nothing lost)',m.tasks.find(x=>x.id===2)&&m.tasks.find(x=>x.id===2).t==='LOCAL-EDIT');
 L=clone(B);L.done['2026-10-25']={y:1};L.done['2026-10-24'].z=1;R=clone(B);R.done['2026-10-26']={w:1};R.done['2026-10-24'].q=1;m=mrg(B,L,R);
 ok('date-keyed data merges per day and per key',m.done['2026-10-25'].y===1&&m.done['2026-10-26'].w===1&&m.done['2026-10-24'].z===1&&m.done['2026-10-24'].q===1&&m.done['2026-10-24'].x===1);
 L=clone(B);L.n=5;R=clone(B);R.n=9;m=mrg(B,L,R);ok('same value changed on both -> this device (the one saving) wins',m.n===5);
 L=clone(B);R=clone(B);R.name='Azimov';m=mrg(B,L,R);ok('only remote changed a value -> remote value taken',m.name==='Azimov');
 L=clone(B);L.days=[1,2,3];R=clone(B);R.days=[1];m=mrg(B,L,R);ok('plain arrays are atomic: local change wins',m.days.join()==='1,2,3');
 L={tasks:[{id:1,t:'L'}],k:1};R={tasks:[{id:2,t:'R'}],j:2};m=mrg({},L,R);ok('NO base (old install): union, nothing is lost ('+m.tasks.map(x=>x.id)+')',m.tasks.length===2&&m.k===1&&m.j===2);
 // ---------- two-device flows ----------
 const A=makeDevice('A'),Bd=makeDevice('B');
 A.S.hab=[{id:'h1',t:'Kitob'}];A.save();await A.push();
 ok('device A first save -> server rev 1, A knows rev 1',server.row&&server.row.rev===1&&A.REV===1&&A.SYNC==='ok');
 const ch=await Bd.pull();ok('device B (clean) pulls -> gets A\'s data, no merge needed',ch===true&&Bd.S.hab.length===1&&Bd.REV===1);
 // concurrent edits
 Bd.S.hab.push({id:'h2',t:'Namoz'});Bd.save();await Bd.push();
 ok('B saves -> rev 2',server.row.rev===2&&Bd.REV===2);
 A.S.hab.push({id:'h3',t:'Zal'});A.save();await A.push();
 const ids=server.row.data.hab.map(x=>x.id).sort().join();
 ok('A (stale rev 1) saves -> conflict detected, merged with B\'s change, nothing lost on the server (habits '+ids+')',ids==='h1,h2,h3'&&server.row.rev===3);
 ok('A\'s own copy now also contains B\'s habit',A.S.hab.some(x=>x.id==='h2'));
 // delete on A, edit on B
 await Bd.pull();A.S.hab=A.S.hab.filter(x=>x.id!=='h1');A.save();Bd.S.hab.find(x=>x.id==='h2').t='Namoz (5 vaqt)';Bd.save();
 await Bd.push();await A.push();
 const fin=server.row.data.hab;ok('delete on A + edit on B (concurrent): both respected ('+fin.map(x=>x.id+':'+x.t).join(', ')+')',!fin.some(x=>x.id==='h1')&&fin.find(x=>x.id==='h2').t==='Namoz (5 vaqt)');
 // pull when local unsynced and server newer -> merge + push
 await A.pull();await Bd.pull();Bd.S.hab.push({id:'h9',t:'Yangi B'});Bd.save();await Bd.push();
 A.S.hab.push({id:'h8',t:'Yangi A'});A.save();                 // A has an unsynced change and the server moved on
 const c2=await A.pull();await new Promise(r=>setImmediate(r));await new Promise(r=>setImmediate(r));
 ok('pull with an unsynced local edit merges (not overwrites) and pushes the result',c2===true&&server.row.data.hab.some(x=>x.id==='h8')&&server.row.data.hab.some(x=>x.id==='h9'));
 // nothing new on the server
 const c3=await A.pull();ok('pull with nothing new returns false (no pointless redraw)',c3===false);
 // edits made while a request is in flight must not be lost or marked as synced
 server.row=null;const E=makeDevice('E');E.S.hab=[{id:'e1',t:'x'}];E.save();
 const realRpc=E.sb.rpc;let injected=false;E.sb.rpc=async(fn,a)=>{if(!injected){injected=true;E.S.hab.push({id:'e2',t:'during flight'});E.save();E.push()}return realRpc(fn,a)};   // E.push() = the 700 ms debounce timer firing mid-flight
 await E.push();await new Promise(r=>setImmediate(r));await new Promise(r=>setImmediate(r));
 ok('edit made while a save is in flight is queued and reaches the server right after (server has e1 and e2)',server.row.data.hab.some(x=>x.id==='e1')&&server.row.data.hab.some(x=>x.id==='e2')&&server.row.rev===2);
 // two default habits with the same name but different ids must not both survive a merge
 server.row=null;const P=makeDevice('P'),Q=makeDevice('Q');P.S.hab=[{id:'hx1',t:'Tong va kech zikri'}];P.save();await P.push();
 Q.S.hab=[{id:'hy9',t:'Tong va kech zikri'},{id:'hq',t:'Boshqa'}];Q.save();await Q.push();
 ok('same-named habits created separately on two devices are merged into one ('+server.row.data.hab.map(x=>x.id).join(',')+')',server.row.data.hab.filter(x=>x.t==='Tong va kech zikri').length===1&&server.row.data.hab.some(x=>x.id==='hq'));
 // legacy server (SQL not run yet)
 server.rpc=false;server.revcol=false;const Lg=makeDevice('L');Lg.S.hab=[{id:'l1',t:'Eski'}];Lg.save();await Lg.push();
 ok('server without reliability.sql: app falls back to the old save mode and keeps working',Lg.NORPC===true&&server.row.data.hab.some(x=>x.id==='l1')&&Lg.SYNC==='ok');
 const Lg2=makeDevice('L2');const c4=await Lg2.pull();ok('...and the old pull rule still works',Lg2.S.hab&&Lg2.S.hab.some(x=>x.id==='l1'));
 server.rpc=true;server.revcol=true;
 // ---------- error reporter ----------
 const R2=makeDevice('R');R2.reportErr('boom A','stack1');R2.reportErr('boom A','stack1');for(let i=0;i<8;i++)R2.reportErr('boom '+i,'s');
 ok('error reporter: duplicates ignored, max 5 per session, fields filled ('+server.errors.length+' sent)',server.errors.length===5&&server.errors[0].ver&&server.errors[0].ua==='TestUA'&&server.errors[0].user_id==='u1');
 // safe render: a broken screen shows a friendly page instead of a blank app
 const Rr=makeDevice('Rr');Rr.S.ts=1;Rr.S.ob=1;Rr.S.top=undefined;Rr.S.done=null;Rr.setTab('h');Rr.render();
 ok('a crash while drawing shows the friendly recovery screen',/Kechirasan/.test(Rr.app.innerHTML)&&/Bosh sahifaga/.test(Rr.app.innerHTML));
 // ---------- server backups ----------
 server.hist=[{id:7,day:'2026-10-24',kind:'daily',data:{ob:1,ts:5,hab:[{id:'old1',t:'Eski odat'}],ie:{words:[{id:1,w:'a'}]},money:[{id:1}],done:{'2026-10-24':{x:1}}}}];
 const H=makeDevice('H');await H.histLoad();const card=H.histCard();
 ok('backups list loads and shows the date with a Restore button',H.HIST.length===1&&card.includes('2026-10-24')&&card.includes('histRestore(7)'));
 await H.histRestore(7);ok('restoring a backup replaces the data (and keeps a local copy for undo)',H.S.hab.some(x=>x.id==='old1')&&!!H.ls['trk_prerestore']);
 ok('summary text for the confirm dialog',/Odatlar: 1/.test(H.sumS(server.hist[0].data)));
 // diagnostics
 H.ensurePersist();await new Promise(r=>setImmediate(r));const dt=H.diagText();ok('diagnostics text has version, sync, storage and device',/Versiya: 2026/.test(dt)&&/Sinxron/.test(dt)&&/Doimiy xotira/.test(dt)&&/TestUA/.test(dt));
})();
