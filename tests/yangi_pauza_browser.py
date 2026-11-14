# Speaking: yozuvdan pauza o'lchash (spPauses), ko'rsatkichlar va oldingi urinish bilan solishtirish. Soat: 2026-11-05 10:00.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('pauza', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.alert=m=>window.__t.push('ALERT '+m);
      window.mkWav=(segs,noise)=>{const rate=12000;let n=0;segs.forEach(s=>n+=Math.round(s[1]*rate));const buf=new ArrayBuffer(44+n*2),dv=new DataView(buf);const W=(o,s)=>{for(let i=0;i<s.length;i++)dv.setUint8(o+i,s.charCodeAt(i))};W(0,'RIFF');dv.setUint32(4,36+n*2,true);W(8,'WAVE');W(12,'fmt ');dv.setUint32(16,16,true);dv.setUint16(20,1,true);dv.setUint16(22,1,true);dv.setUint32(24,rate,true);dv.setUint32(28,rate*2,true);dv.setUint16(32,2,true);dv.setUint16(34,16,true);W(36,'data');dv.setUint32(40,n*2,true);
        let p=0,seed=7;const rnd=()=>{seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x7fffffff-.5};
        segs.forEach(s=>{const k=Math.round(s[1]*rate);for(let i=0;i<k;i++){const amp=s[0]==='s'?0.3*Math.sin(2*Math.PI*180*i/rate)*(0.6+0.4*Math.sin(2*Math.PI*3*i/rate))+0.06*rnd():(noise||0.01)*rnd()*2;dv.setInt16(44+p*2,Math.max(-1,Math.min(1,amp))*32767,true);p++}});return buf}}""")
    SC = "[['q',.5],['s',2],['q',1.0],['s',2],['q',.4],['s',2],['q',2.0],['s',1],['q',.5]]"
    r = ev("(()=>{const r=spPauses(mkWav(%s));return r})()" % SC)
    chk('a recording with speech, a 1.0 s pause, a 0.4 s gap and a 2.0 s pause is measured correctly: 2 pauses (the 0.4 s gap is ignored), longest ≈ 2.0 s, total ≈ 3.0 s, speaking span ≈ 10.4 s, 1 long pause', r and r['n'] == 2 and abs(r['longest'] - 2.0) <= 0.2 and abs(r['total'] - 3.0) <= 0.3 and abs(r['span'] - 10.4) <= 0.3 and r['long'] == 1, r)
    r2 = ev("(()=>spPauses(mkWav(%s,0.03)))()" % SC)
    chk('it still works with a noisy background (silence is not silent): same 2 pauses', r2 and r2['n'] == 2 and abs(r2['total'] - 3.0) <= 0.35, r2)
    chk('leading and trailing silence is not counted as pauses (only gaps between speech)', r and r['span'] < 10.6 and ev("spPauses(mkWav([['q',3],['s',3],['q',3]])).n") == 0)
    chk('speech without gaps gives 0 pauses and longest 0', ev("(()=>{const r=spPauses(mkWav([['s',6]]));return [r.n,r.longest,r.total]})()") == [0, 0, 0])
    chk('a gap of 0.65 s counts, 0.5 s does not (threshold 0.6 s)', ev("spPauses(mkWav([['s',2],['q',.65],['s',2]])).n") == 1 and ev("spPauses(mkWav([['s',2],['q',.5],['s',2]])).n") == 0)
    chk('nothing to measure -> null: all silence, a very quiet recording, a too short one', ev("spPauses(mkWav([['q',5]]))") is None and ev("spPauses(mkWav([['s',0.2]]))") is None and ev("spPauses(new ArrayBuffer(100))") is None and ev("spPauses(null)") is None)
    chk('it accepts an ArrayBuffer and a typed array view (also with an offset)', ev("(()=>{const b=mkWav([['s',2],['q',1],['s',2]]),u=new Uint8Array(b),big=new Uint8Array(b.byteLength+10);big.set(u,10);return [spPauses(b).n,spPauses(u).n,spPauses(big.subarray(10)).n]})()") == [1, 1, 1])
    # ---------- ko'rsatkichlar ----------
    ev("""()=>{window.__tr=Array.from({length:30},(_,i)=>'word'+i).join(' ');SPQ={part:2,q:'Describe a place you like.'};S.ie.tests=[]}""")
    html = lambda f: ev("(f)=>ieSpM(f).replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ')", f)
    base = {'transcript': ' '.join('word%d' % i for i in range(30)), 'dur': 20, 'band': 6.5}
    h = html(dict(base, pa={'n': 2, 'longest': 2.0, 'total': 3.0, 'span': 10.4, 'long': 1}))
    chk('the metrics card shows the pauses: count, longest, total and share, plus the speaking speed without pauses (30 words in 7.4 s of speech = 243/min)', 'Pauzalar (0,6 s dan uzun): 2 ta · eng uzuni 2 s · jami 3 s (29%)' in h and 'Sof gapirish tezligi (pauzasiz): 243' in h and 'bitta-ikkita uzun pauza bor' in h, h)
    h = html(dict(base, pa={'n': 6, 'longest': 4.5, 'total': 9.0, 'span': 20, 'long': 3}))
    chk('many or very long pauses get the matching advice (plan your thoughts, use connectors)', 'pauza ko‘p yoki uzun' in h and '(45%)' in h)
    chk('no pauses and fast speech: "pauzasiz va tez"; no pauses at a normal pace: "pauzalar me’yorida"', 'pauzasiz va tez' in html(dict(base, dur=10, pa={'n': 0, 'longest': 0, 'total': 0, 'span': 9, 'long': 0})) and 'pauzalar me’yorida' in html(dict(base, dur=15, pa={'n': 0, 'longest': 0, 'total': 0, 'span': 14, 'long': 0})))
    h = html(base); chk('older records without pause data still show the old metrics and no pause lines (nothing breaks)', 'Tezlik:' in h and 'Pauzalar' not in h)
    # ---------- oldingi urinish ----------
    prev = {'id': 1, 'd': '2026-11-03', 'k': 'S', 'b': {'S': 6}, 'fb': {'transcript': ' '.join('w%d' % i for i in range(20)), 'dur': 20, 'q': 'Describe a place you like.', 'pa': {'n': 5, 'longest': 3, 'total': 8, 'span': 19, 'long': 2}}}
    ev("(p)=>{S.ie.tests=[p]}", prev); h = html(dict(base, q='Describe a place you like.', pa={'n': 2, 'longest': 2.0, 'total': 3.0, 'span': 10.4, 'long': 1}))
    chk('the same question answered before: "Oldingi urinish" compares speed (60 → 90, +30), pauses (5 → 2) and band (6 → 6.5)', 'Oldingi urinish (3-noyabr): 60 → 90 so‘z/daq (+30); pauzalar 5 → 2; band 6 → 6.5' in h, h)
    chk('a different question is not compared; unsaved feedback takes the question from the current card', 'Oldingi urinish' not in html(dict(base, q='Another question?')) and 'Oldingi urinish' in html(dict(base)))
    ev("()=>{SPQ={part:2,q:'Something else'}}"); chk('...and with a different current question there is no comparison', 'Oldingi urinish' not in html(dict(base))); ev("()=>{SPQ={part:2,q:'Describe a place you like.'}}")
    # ---------- saqlash ----------
    ev("""(f)=>{SFB=Object.assign({},f,{pa:{n:2,longest:2,total:3,span:10.4,long:1}});SDUR=20;S.ie.tests=[];spSaveAI()}""", base)
    e = ev("S.ie.tests[S.ie.tests.length-1].fb"); chk('saving the result keeps the pause data and the question with the feedback (so later attempts can be compared)', e['pa']['n'] == 2 and e['q'] == 'Describe a place you like.' and e['dur'] == 20, e)
    # ---------- yozib olish oqimi ----------
    ev("""()=>{S.ie.tests=[];SPQ={part:2,q:'Describe a place you like.'};SFB=null;window.aiOk=()=>true;
      Object.defineProperty(navigator,'mediaDevices',{value:{getUserMedia:async()=>({getTracks:()=>[{stop(){}}]})},configurable:true});
      window.MediaRecorder=function(){this.mimeType='audio/mp4';this.start=()=>{};this.stop=()=>{this.ondataavailable&&this.ondataavailable({data:new Blob([new Uint8Array(6000)])});this.onstop&&this.onstop()}};
      window.toWav=async()=>mkWav(%s);window.fnAI=async b=>({text:JSON.stringify({band:6.5,transcript:'I like the old town of my city because it is quiet.',fluency:6,lexical:6,grammar:6,pron:6,tips:['x']})});
      window.__req=[];const of=window.fnAI;window.fnAI=async b=>{__req.push(b);return of(b)};tab='e';EV='i';IVW='s';render()}""" % SC)
    ev("()=>{spRec();return 1}"); pg.wait_for_timeout(200); ev("()=>{if(SREC)SREC.mr.stop();return 1}"); pg.wait_for_timeout(600)
    chk('in the real recording flow the pauses are measured from the recorded audio and attached to the feedback (no extra request: the same single AI request as before)', ev("SFB&&SFB.pa&&SFB.pa.n") == 2 and len(ev("__req")) == 1 and ev("__req[0].mime") == 'audio/wav', (ev("SFB&&SFB.pa"), ev("__t")))
    chk('the feedback screen shows the pause line', 'Pauzalar (0,6 s dan uzun): 2 ta' in pg.inner_text('#app'))
    ev("()=>{window.toWav=async()=>mkWav([['q',3]])}"); ev("()=>{SFB=null;spRec();return 1}"); pg.wait_for_timeout(200); ev("()=>{if(SREC)SREC.mr.stop();return 1}"); pg.wait_for_timeout(600)
    chk('if the audio cannot be measured (silence) the feedback still works, simply without pause data', ev("SFB&&SFB.band") == 6.5 and ev("SFB.pa") is None and 'Pauzalar' not in pg.inner_text('#app'))
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];SFB=Object.assign({},SFB,{transcript:'I like the old town of my city because it is quiet and calm.',dur:30,pa:{n:6,longest:4.5,total:9,span:25,long:3}});render()}", [ui, th]); pg.wait_for_timeout(50)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('the card does not overflow the phone screen in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
