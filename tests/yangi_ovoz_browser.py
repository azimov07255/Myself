import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Ovoz: pauzali pleyer (gap bo'yicha), telefon ovozini tanlash, AI (tabiiy) ovoz va uni saqlash. Soat: 2026-11-03 10:00.
import sys, json
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
ANS = 'First sentence is here. Second sentence follows it. The third one comes now! And the fourth and final one?'
with Run('ovoz', when=(2026, 11, 3, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""(ans)=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);window.aiOk=()=>true;window.__sp=[];window.__cx=0;window.__fp=[];window.__au=[];window.__fail='';
      window.__voices=[{name:'Samantha',lang:'en-US',localService:true},{name:'Ava (Premium)',lang:'en-US',localService:true},{name:'Daniel',lang:'en-GB',localService:true},{name:'Serena (Enhanced)',lang:'en-GB',localService:true},{name:'Zoe (Premium)',lang:'en-GB',localService:true},{name:'Kyoko',lang:'ja-JP',localService:true}];
      window.__tts={getVoices:()=>window.__voices,speak:u=>__sp.push({t:u.text,v:u.__voice&&u.__voice.name,pitch:u.pitch,rate:u.rate,u}),cancel:()=>{window.__cx++}};
      window.Audio=function(u){this.src=u||'';this.paused=true;this.duration=60;this.currentTime=0;this.playbackRate=1;__au.push(this);this.play=()=>{this.paused=false;return Promise.resolve()};this.pause=()=>{this.paused=true}};
      window.fnPost=async b=>{__fp.push(b);if(window.__fail)throw new Error(window.__fail);if(b.action==='tts')return {audio:btoa(String.fromCharCode(...new Uint8Array(480).fill(5))),rate:24000,model:'m'};return {}};
      localStorage.removeItem('trk_vcn');S.ie.voc=undefined;S.ie.slow=0;S.ie.acc='us';VPR={};VP=null;
      SMD={a:ans,why:['x'],u:[]};SME='';SPQ={part:2,q:'Describe a place you like to visit.'};SFB=null;tab='e';EV='i';IVW='s';render()}""", ANS)
    pg.wait_for_timeout(150); t = pg.inner_text('#app')
    chk('the model answer is a player: every sentence is a tappable span, with "🔊 Eshit", previous/next sentence only while playing, speed chips and the phone voice label', ev("document.querySelectorAll('#app .vps').length") == 4 and '🔊 Eshit' in t and '📱 Telefon ovozi' in t and ev("[...document.querySelectorAll('#app .vp .chip')].map(c=>c.textContent)")[:3] == ['0.75×', '1×', '1.25×'] and ev("document.querySelectorAll('#app .vp button[aria-label=\"Keyingi gap\"]').length") == 0, t[t.index('Namunaviy'):][:160])
    pg.click('#app .vp >> text=🔊 Eshit'); pg.wait_for_timeout(80)
    chk('playing starts with sentence 1 (highlighted) using the best phone voice: the "Premium" US voice, normal speed', ev("__sp.length") == 1 and ev("__sp[0].t") == 'First sentence is here.' and ev("__sp[0].v") == 'Ava (Premium)' and abs(ev("__sp[0].rate") - 0.95) < 1e-6 and ev("[...document.querySelectorAll('#app .vps')].findIndex(s=>s.classList.contains('on'))") == 0, ev("__sp.map(x=>[x.v,x.rate])"))
    chk('while playing the buttons are ⏸ Pauza, ⏹ To‘xtatish, ⏮ and ⏭, with "1 / 4"', all(s in pg.inner_text('#app') for s in ['⏸ Pauza', '⏹ To‘xtatish', '1 / 4']) and ev("document.querySelectorAll('#app .vp button[aria-label=\"Keyingi gap\"]').length") == 1)
    ev("__sp[0].u.onend()"); pg.clock.run_for(300); pg.wait_for_timeout(60)
    chk('when a sentence ends the next one starts and is highlighted', ev("__sp.length") == 2 and ev("__sp[1].t") == 'Second sentence follows it.' and ev("[...document.querySelectorAll('#app .vps')].findIndex(s=>s.classList.contains('on'))") == 1 and '2 / 4' in pg.inner_text('#app'))
    # pauza
    ev("window.__cx=0"); pg.click('#app .vp >> text=⏸ Pauza'); pg.wait_for_timeout(60); n0 = ev("__sp.length")
    chk('⏸ Pauza cancels the speech and shows "▶ Davom etish"', ev("__cx") >= 1 and '▶ Davom etish' in pg.inner_text('#app') and ev("VP.pz") == 1 and ev("VP.pl") == 0)
    ev("__sp[1].u.onend()"); pg.clock.run_for(600); pg.wait_for_timeout(60); chk('a late "end" event of the paused sentence does not move on', ev("__sp.length") == n0 and ev("VP.i") == 1)
    pg.click('#app .vp >> text=▶ Davom etish'); pg.wait_for_timeout(60)
    chk('"▶ Davom etish" continues from the SAME sentence (it is spoken again from its start), not from the beginning', ev("__sp.length") == n0 + 1 and ev("__sp[n0].t") == 'Second sentence follows it.' if False else (ev("__sp.length") == n0 + 1 and ev("__sp[%d].t" % n0) == 'Second sentence follows it.'))
    # navigatsiya
    pg.click('#app .vp button[aria-label="Keyingi gap"]'); pg.wait_for_timeout(60); chk('⏭ jumps to the next sentence at once', ev("VP.i") == 2 and ev("__sp[__sp.length-1].t") == 'The third one comes now!')
    pg.click('#app .vp button[aria-label="Oldingi gap"]'); pg.wait_for_timeout(60); chk('⏮ goes back one sentence', ev("VP.i") == 1 and ev("__sp[__sp.length-1].t") == 'Second sentence follows it.')
    pg.click('#app .vps >> nth=3'); pg.wait_for_timeout(60); chk('tapping a sentence jumps straight to it', ev("VP.i") == 3 and ev("__sp[__sp.length-1].t") == 'And the fourth and final one?')
    pg.click('#app .vp >> text=⏸ Pauza'); pg.click('#app .vps >> nth=0'); pg.wait_for_timeout(60); k0 = ev("__sp.length"); chk('while paused, tapping a sentence only moves the marker; ▶ Davom etish then speaks it', ev("VP.i") == 0 and ev("VP.pz") == 1 and ev("__sp.length") == k0)
    pg.click('#app .vp >> text=▶ Davom etish'); pg.wait_for_timeout(60); chk('...', ev("__sp[__sp.length-1].t") == 'First sentence is here.')
    pg.click('#app .vp .chip >> text=0.75×'); pg.wait_for_timeout(60); chk('changing the speed restarts the current sentence at that speed (0.95 × 0.75)', abs(ev("__sp[__sp.length-1].rate") - 0.7125) < 1e-6 and ev("VPR.spm.rate") == 0.75)
    ev("VPR.spm.rate=1;VP.rate=1")
    ev("window.__cx=0"); pg.click('#app .vp >> text=⏹ To‘xtatish'); pg.wait_for_timeout(60); n1 = ev("__sp.length"); ev("__sp[__sp.length-1].u.onend()"); pg.clock.run_for(600)
    chk('⏹ To‘xtatish stops everything; a late "end" does nothing; the button is "🔊 Eshit" again', ev("__cx") >= 1 and ev("VP") is None and ev("__sp.length") == n1 and '🔊 Eshit' in pg.inner_text('#app'))
    # oxirigacha
    pg.click('#app .vp >> text=🔊 Eshit'); pg.wait_for_timeout(40)
    for i in range(4):
        ev("__sp[__sp.length-1].u.onend()"); pg.clock.run_for(400); pg.wait_for_timeout(30)
    chk('after the last sentence it stops by itself and offers to listen again', ev("VP") is None and '🔊 Eshit' in pg.inner_text('#app'))
    # boshqa pleyer
    ev("""()=>{const d=document.createElement('div');d.id='tmpv';document.body.appendChild(d);d.innerHTML=vpUi('t1',[{t:'One.',s:'A'},{t:'Two.',s:'B'}],{once:1})+vpUi('t2',[{t:'Alpha.',s:'A'},{t:'Beta.',s:'A'}],{})}""")
    chk('"once" (exam) mode offers only play/stop: no pause, no ⏮ ⏭, no speed', ev("(()=>{const e=document.getElementById('vp_t1');return !e.textContent.includes('⏸')&&!e.querySelector('.chip')&&!e.querySelector('button[aria-label]')})()"))
    ev("vpStart('t2',0)"); pg.wait_for_timeout(40); ev("vpStart('t1',0)"); pg.wait_for_timeout(40); chk('starting one player stops the other', ev("VP.id") == 't1' and ev("__cx") >= 1)
    chk('in exam mode ⏸ is not available while playing (only ⏹ To‘xtatish)', ev("document.getElementById('vp_t1').textContent.includes('⏹ To‘xtatish')") and ev("!document.getElementById('vp_t1').textContent.includes('⏸')"))
    ev("vpStop();document.getElementById('tmpv').remove()")
    # ---------- telefon ovozlari ----------
    ev("localStorage.removeItem('trk_vcn')"); vv = lambda a, alt=False: ev("(x)=>{const v=ieVoice(x[0],x[1]);return v&&v.name}", [a, alt])
    chk('automatic choice prefers high-quality voices: US → "Ava (Premium)", UK → "Serena (Enhanced)"; the second speaker gets the second premium voice (US has only one, so it falls back to the usual list)', vv('us') == 'Ava (Premium)' and vv('uk') == 'Serena (Enhanced)' and vv('uk', True) == 'Zoe (Premium)' and vv('us', True) not in (None, 'Ava (Premium)'), (vv('us'), vv('uk'), vv('uk', True), vv('us', True)))
    ev("()=>{localStorage.setItem('trk_vcn',JSON.stringify({us:'Samantha',uk:'Daniel',b:'Daniel'}))}"); chk('a voice chosen in Settings wins over the automatic choice (US Samantha, UK Daniel, second speaker Daniel)', vv('us') == 'Samantha' and vv('uk') == 'Daniel' and vv('us', True) == 'Daniel')
    ev("()=>{localStorage.setItem('trk_vcn',JSON.stringify({us:'Voice that does not exist'}))}"); chk('a chosen voice that no longer exists is ignored (automatic again)', vv('us') == 'Ava (Premium)')
    ev("localStorage.removeItem('trk_vcn')")
    ev("()=>{tab='s';render();document.querySelectorAll('#app details').forEach(d=>{if(d.textContent.includes('🔊 Ovoz'))d.open=true})}"); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('Sozlama has a "🔊 Ovoz" card: phone voice is selected, with the tip about downloading Enhanced/Premium voices and selects for UK, US and the second speaker (only English voices; ★ marks high quality)', '🔊 Ovoz' in t and 'Enhanced' in t and ev("document.querySelectorAll('#app details select').length") >= 3 and 'Kyoko' not in t and ev("[...document.querySelectorAll('#app details select')][0].innerHTML.includes('★')"))
    pg.select_option('#app details select >> nth=1', 'Samantha'); pg.wait_for_timeout(100); chk('choosing a voice is saved on this device only (localStorage)', ev("JSON.parse(localStorage.getItem('trk_vcn')).us") == 'Samantha')
    ev("__sp=[]"); pg.click('#app details button[aria-label="Sinash"] >> nth=1'); pg.wait_for_timeout(60); chk('the ▶ test button speaks a sample with the chosen voice', ev("__sp.length") == 1 and 'IELTS' in ev("__sp[0].t"))
    ev("localStorage.removeItem('trk_vcn')")
    # ---------- AI ovozi ----------
    pg.click('#app details >> text=🎧 AI ovozi (tabiiy)'); pg.wait_for_timeout(120); t = pg.inner_text('#app')
    chk('AI voice mode shows accent (UK/US/AU), A and B voice choices grouped as female/male, and the cache line', ev("S.ie.voc.mode") == 'ai' and all(s in t for s in ['Aksent', 'A ovozi', 'B ovozi', 'keshni tozalash']) and ev("document.querySelectorAll('#app details optgroup').length") == 4 and 'Kore' in t and 'Charon' in t)
    ev("ovSet('acc','us')"); chk('the accent is saved', ev("S.ie.voc.acc") == 'us'); ev("ovSet('acc','uk')")
    ev("""()=>{SMD={a:Array.from({length:8},(_,i)=>'Sentence number '+(i+1)+' says something quite long about the lovely place that many people visit during the warm months of the year and love.').join(' '),why:[],u:[]};tab='e';IVW='s';render()}""")
    pg.wait_for_timeout(300); t = pg.inner_text('#app')
    chk('in AI mode a not-yet-prepared text offers "🎧 Tabiiy ovozni tayyorlash (N so‘rov)" with the number of pieces (about 800-character pieces)', '🎧 Tabiiy ovozni tayyorlash' in t and ev("ovChunks(VPR.spm.items).length") == 2 and '(2 so‘rov)' in t, t[t.index('Namunaviy'):][:260])
    pg.click('#app .vp >> text=🎧 Tabiiy ovozni tayyorlash'); pg.wait_for_timeout(300); n1 = len([x for x in ev("__fp") if x.get('action') == 'tts']); w1 = pg.inner_text('#app .vp'); pg.clock.run_for(23000); pg.wait_for_timeout(300); fp = [x for x in ev("__fp") if x.get('action') == 'tts']
    chk('preparing sends one request per piece (items with speakers, accent and both voices), waits between requests (1 request first, the second only after the pause with a visible countdown) and then shows "🎧 AI ovozi"', n1 == 1 and 'kutilmoqda' in w1 and len(fp) == 2 and fp[0]['acc'] == 'uk' and fp[0]['va'] == 'Kore' and fp[0]['vb'] == 'Charon' and all(i['s'] in 'AB' for x in fp for i in x['items']) and ev("VPR.spm.ready") is True and '🎧 AI ovozi' in pg.inner_text('#app'), len(fp))
    buf = ev("(async()=>{const c=ovChunks(VPR.spm.items)[0];const b=await idbGet(ovKey(c));const u=new Uint8Array(b);return [b.byteLength,String.fromCharCode(...u.slice(0,4)),String.fromCharCode(...u.slice(8,12)),new DataView(b).getUint32(24,true),new DataView(b).getUint16(22,true),new DataView(b).getUint16(34,true)]})()")
    chk('the audio is stored on the phone as a WAV file: RIFF/WAVE header, 24000 Hz, mono, 16-bit, 44 + 480 bytes', buf == [524, 'RIFF', 'WAVE', 24000, 1, 16], buf)
    ev("__fp=[]"); ev("()=>{VPR.spm.ready=undefined;vpDraw('spm')}"); ev("ovCheck('spm')"); pg.wait_for_timeout(200); ev("ovGen('spm')"); pg.wait_for_timeout(200); chk('preparing again asks nothing (everything is saved)', len(ev("__fp")) == 0 and ev("VPR.spm.ready") is True)
    ev("__sp=[];__au.length=0"); pg.click('#app .vp >> text=🔊 Eshit'); pg.wait_for_timeout(300)
    chk('playing in AI mode uses the saved audio (an audio element, no phone speech)', ev("__sp.length") == 0 and ev("__au.length") == 1 and ev("__au[0].src").startswith('blob:') and ev("__au[0].paused") is False and ev("VP.eng") == 'ai')
    a = ev("__au[0].duration")
    ev("()=>{const a=__au[0];a.currentTime=a.duration*0.7;a.ontimeupdate()}"); pg.wait_for_timeout(60); chk('the highlighted sentence follows the audio time (70% into piece 1 → a later sentence)', ev("VP.i") >= 1 and ev("[...document.querySelectorAll('#app .vps')].findIndex(s=>s.classList.contains('on'))") == ev("VP.i"))
    ev("__au[0].pause=function(){this.paused=true;window.__ap=1}"); pg.click('#app .vp >> text=⏸ Pauza'); pg.wait_for_timeout(60); chk('⏸ Pauza really pauses the audio (it can continue mid-sentence)', ev("__ap") == 1 and ev("__au[0].paused") is True and '▶ Davom etish' in pg.inner_text('#app'))
    ev("window.__ap=0"); pg.click('#app .vp >> text=▶ Davom etish'); pg.wait_for_timeout(60); chk('▶ Davom etish plays the same audio on', ev("__au[0].paused") is False)
    pg.click('#app .vp .chip >> text=1.25×'); pg.wait_for_timeout(60); chk('speed changes the audio playback rate', abs(ev("__au[0].playbackRate") - 1.25) < 1e-6)
    pg.click('#app .vps >> nth=0'); pg.wait_for_timeout(60); chk('tapping the first sentence seeks to the start of its piece', ev("VP.i") == 0 and ev("__au[0].currentTime") == 0)
    ev("__au[0].onended()"); pg.wait_for_timeout(100); chk('when piece 1 ends piece 2 starts on the same player', ev("VP.c") == 1 and ev("__au[0].src").startswith('blob:'))
    pg.click('#app .vps >> nth=1'); pg.wait_for_timeout(100); chk('jumping back to a sentence of piece 1 switches piece and starts it', ev("VP.c") == 0)
    ev("__au[0].onended()"); pg.wait_for_timeout(60); ev("__au[0].onended()"); pg.wait_for_timeout(100); chk('after the last piece the player finishes', ev("VP") is None and '🔊 Eshit' in pg.inner_text('#app'))
    # xato va zaxira
    ev("()=>{ovSet('b','Puck')}"); pg.wait_for_timeout(300); chk('changing a voice (A or B) means the audio is not prepared any more (a different cache key), so it must be made again', ev("VPR.spm.ready") is not True and '🎧 Tabiiy ovozni tayyorlash' in pg.inner_text('#app') or ev("VPR.spm.ready") is False)
    ev("()=>{window.__fail='AI ovoz limiti vaqtincha tugadi.';__fp=[]}"); pg.click('#app .vp >> text=🎧 Tabiiy ovozni tayyorlash'); pg.wait_for_timeout(300); pg.clock.run_for(140000); pg.wait_for_timeout(400); t = pg.inner_text('#app'); nreq = len([x for x in ev("__fp") if x.get('action') == 'tts'])
    chk('a rate-limit failure is retried twice automatically (65 s apart), then shows the reason and says the phone voice will be used; nothing is stuck', nreq == 3 and 'AI ovoz limiti' in t and 'Telefon ovozi ishlatiladi' in t and ev("VPR.spm.gen") is None and ev("VPR.spm.ready") is not True)
    ev("__sp=[]"); pg.click('#app .vp >> text=🔊 Eshit'); pg.wait_for_timeout(100); chk('and playing then falls back to the phone voice at once', ev("__sp.length") == 1 and ev("VP.eng") == 'dev'); ev("vpStop()")
    ev("window.__fail=''")
    ev("()=>{__fp=[]}"); ev("ovSample('a')"); pg.wait_for_timeout(500); ev("ovSample('a')"); pg.wait_for_timeout(300); chk('the ▶ voice sample makes ONE request (saved after the first time)', len([x for x in ev("__fp") if x.get('action') == 'tts']) == 1 and ev("__au.length") >= 2)
    # ---------- limitga chidamlilik (kutishlar qo'lda boshqariladi, soat tezligiga bog'liq emas) ----------
    ev("()=>{window.__fail='';ovSet('b','Charon');ovClear()}"); pg.wait_for_timeout(500)
    ev("()=>{window.__os=ovSleep;window.__rel=[];window.ovSleep=async(id,ms,why)=>{const R=VPR[id];if(R&&R.gen){R.gen.wait=Math.ceil(ms/1000);R.gen.why=why;vpDraw(id);await new Promise(r=>window.__rel.push(r));if(R.gen)R.gen.wait=0}}}")
    rel = lambda: (ev("()=>{const r=__rel.shift();r&&r()}"), pg.wait_for_timeout(250))
    ev("()=>{VPR.spm.ready=false;VPR.spm.err='';__fp=[];window.__flaky=1;const of=window.fnPost;window.fnPost=async b=>{if(window.__flaky&&b.action==='tts'){window.__flaky=0;__fp.push(b);throw new Error('AI ovoz limiti vaqtincha tugadi.')}return of(b)}}")
    ev("()=>{ovGen('spm');return 1}"); pg.wait_for_timeout(300); w = pg.inner_text('#app .vp')
    chk('when the first request hits the free limit the screen says so with a countdown ("bepul limit") instead of failing', 'bepul limit' in w and 'kutilmoqda' in w and ev("__fp.length") == 1, w[-140:])
    rel(); chk('after the wait it retries by itself and succeeds with piece 1 (then it pauses before piece 2)', ev("__fp.length") == 2 and 'kutilmoqda' in pg.inner_text('#app .vp') and ev("VPR.spm.gen.d") == 1)
    rel(); pg.wait_for_timeout(250); chk('...and finishes: all pieces saved, "🎧 AI ovozi", no error', ev("__fp.length") == 3 and ev("VPR.spm.ready") is True and ev("VPR.spm.err") == '' and '🎧 AI ovozi' in pg.inner_text('#app .vp'))
    ev("()=>{ovClear();VPR.spm.ready=false;__fp=[];window.fnPost=async b=>{__fp.push(b);if(b.action==='tts')throw new Error('Bugungi limit tugadi (40 ta so‘rov).');return {}}}"); pg.wait_for_timeout(400)
    ev("()=>{ovGen('spm');return 1}"); pg.wait_for_timeout(300); chk('the DAILY AI limit is not retried (waiting would not help): one request, a clear message, phone voice', ev("__fp.length") == 1 and 'Bugungi limit' in ev("VPR.spm.err") and 'Telefon ovozi' in ev("VPR.spm.err") and ev("VPR.spm.gen") is None and ev("__rel.length") == 0)
    ev("()=>{ovClear();VPR.spm.ready=false;__fp=[];window.__rel=[];window.fnPost=async b=>{__fp.push(b);if(b.action==='tts')return {audio:btoa(String.fromCharCode(...new Uint8Array(480).fill(5))),rate:24000};return {}}}"); pg.wait_for_timeout(400)
    ev("()=>{ovGen('spm');return 1}"); pg.wait_for_timeout(400); pg.click('#app .vp >> text=⏹ To‘xtatish'); pg.wait_for_timeout(80); rel(); pg.wait_for_timeout(200)
    chk('"⏹ To‘xtatish" during the wait cancels the preparation: the finished piece stays saved, no further request is sent, and a clear note explains how to continue', ev("__fp.length") == 1 and ev("VPR.spm.gen") is None and ev("VPR.spm.ready") is not True and 'saqlandi' in ev("VPR.spm.err"))
    ev("()=>{__fp=[];window.__rel=[]}"); pg.click('#app .vp >> text=🎧 Tabiiy ovozni tayyorlash'); pg.wait_for_timeout(500); chk('pressing the button again makes only the missing request (the saved piece is reused)', ev("__fp.length") == 1 and ev("VPR.spm.ready") is True)
    ev("()=>{window.ovSleep=window.__os}")
    # tuzilma
    ch = ev("(()=>{const it=Array.from({length:30},(_,i)=>({t:'Sentence number '+i+' with some more words to fill the line a bit.',s:i%2?'B':'A'}));const c=ovChunks(it);return [c.length,c.every(x=>x.items.length<=12),c.every(x=>x.items.reduce((a,y)=>a+y.t.length,0)<=850+60),c.flatMap(x=>x.items).length,c[0].items[1].s,c[1].a,c.every(x=>x.cum.every((f,i,a)=>i===0?f===0:f>a[i-1]))]})()")
    chk('long texts are cut into pieces of at most 12 turns and about 850 characters, keeping every sentence and speaker; each piece knows where each sentence starts (for highlighting)', ch[0] >= 3 and ch[1] and ch[2] and ch[3] == 30 and ch[4] == 'B' and ch[6], ch)
    ev("()=>{for(let i=0;i<85;i++)ovStore('tts:test'+i,new ArrayBuffer(1000))}"); pg.wait_for_timeout(1500); ix = ev("(async()=>{const x=await idbGet('tts:idx');return [x.length,x.some(y=>y.k==='tts:test0'),x.some(y=>y.k==='tts:test84')]})()")
    chk('the on-device cache keeps at most 80 audios (the oldest are removed first)', ix[0] <= 80 and ix[1] is False and ix[2] is True, ix)
    ev("ovClear()"); pg.wait_for_timeout(500); chk('"keshni tozalash" empties the cache', ev("(async()=>(await idbGet('tts:idx')).length)()") == 0)
    # Listening AI
    ev("""()=>{S.ie.voc.mode='ai';VPR={};LQ.d={title:'Joining a gym',sec:3,script:[{s:'A',t:'Hello, how can I help you today?'},{s:'B',t:'I would like to join the gym please.'},{s:'A',t:'Certainly, let me take your details.'}],qs:[]};LQ.once=0;LQ.played=0;LQ.pl=0;tab='e';EV='i';IVW='x';AXV=undefined;render()}""")
    ev("()=>{const d=document.createElement('div');d.id='tmpl';document.body.appendChild(d);d.innerHTML=vpUi('lq2',LQ.d.script.map(l=>({t:l.t,s:l.s})),{dlg:1})}"); ev("ovGen('lq2')"); pg.wait_for_timeout(600); fp = [x for x in ev("__fp") if x.get('action') == 'tts']
    chk('a two-person Listening script is sent with the speakers kept (A and B) so the server can use two voices', len(fp) >= 1 and [i['s'] for i in fp[-1]['items']] == ['A', 'B', 'A'], fp[-1] if fp else None); ev("document.getElementById('tmpl').remove()")
    # ko'rinish
    ev("()=>{S.ie.voc.mode='ai';SMD={a:'One short sentence. Another short sentence.',why:[],u:[]};tab='s';render();document.querySelectorAll('#app details').forEach(d=>{if(d.textContent.includes('🔊 Ovoz'))d.open=true})}")
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1]}", [ui, th]); pg.wait_for_timeout(60)
            for sc in ("tab='s'", "tab='e';IVW='s'"):
                ev("()=>{%s;render()}" % sc); pg.wait_for_timeout(40)
                if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th + sc)
    chk('the Ovoz settings and the player do not overflow the phone screen in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
