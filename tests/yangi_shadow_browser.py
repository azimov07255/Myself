# Shadowing: har gapdan keyin takrorlash pauzasi, gapni 1-3 marta takrorlash, matnni yashirish (telefon ovozi va AI ovozi). Soat: 2026-11-05 10:00.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
ANS = 'First sentence is here. Second sentence follows it. The third one comes now! And the fourth and final one?'
with Run('shadow', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""(ans)=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);window.aiOk=()=>true;window.__sp=[];window.__cx=0;window.__fp=[];window.__au=[];
      window.__voices=[{name:'Ava (Premium)',lang:'en-US',localService:true}];
      window.__tts={getVoices:()=>window.__voices,speak:u=>__sp.push({t:u.text,rate:u.rate,u}),cancel:()=>{window.__cx++}};
      window.Audio=function(u){this.src=u||'';this.paused=true;this.duration=60;this.currentTime=0;this.playbackRate=1;__au.push(this);this.play=()=>{this.paused=false;return Promise.resolve()};this.pause=()=>{this.paused=true}};
      window.fnPost=async b=>{__fp.push(b);if(b.action==='tts')return {audio:btoa(String.fromCharCode(...new Uint8Array(480).fill(5))),rate:24000};return {}};
      localStorage.removeItem('trk_vsh');localStorage.removeItem('trk_vrp');localStorage.removeItem('trk_vhd');localStorage.removeItem('trk_vcn');S.ie.voc=undefined;S.ie.slow=0;S.ie.acc='us';VPR={};VP=null;
      SMD={a:ans,why:['x'],u:[]};SME='';SPQ={part:2,q:'Describe a place you like to visit.'};SFB=null;tab='e';EV='i';IVW='s';render()}""", ANS)
    pg.wait_for_timeout(200)
    chips = lambda: ev("[...document.querySelectorAll('#app .vp .chip')].map(c=>c.textContent.trim())")
    chk('the player has "🔁 Shadowing", "↻ 1×" and (for texts) "👁 Matn: ko‘rinadi" next to the speed chips', all(x in chips() for x in ['🔁 Shadowing', '↻ 1×', '👁 Matn: ko‘rinadi']), chips())
    ev("""()=>{const d=document.createElement('div');d.id='tmpv';document.body.appendChild(d);d.innerHTML=vpUi('ex',[{t:'One.',s:'A'},{t:'Two.',s:'A'}],{once:1})}""")
    chk('in exam ("once") mode there are no shadowing chips (and the preferences are ignored there)', ev("!document.getElementById('vp_ex').textContent.includes('Shadowing')"))
    pg.click('#app .vp .chip >> text=Shadowing'); pg.click('#app .vp .chip >> text=↻ 1×'); pg.click('#app .vp .chip >> text=Matn'); pg.wait_for_timeout(80)
    chk('the choices are saved on the device and the chips light up (shadowing on, repeat 2×, text hidden)', ev("localStorage.getItem('trk_vsh')") == '1' and ev("localStorage.getItem('trk_vrp')") == '2' and ev("localStorage.getItem('trk_vhd')") == '1' and '↻ 2×' in chips() and '👁 Matn: yashirin' in chips() and ev("document.querySelector('#app .vpt').classList.contains('vph')"))
    chk('hidden text is blurred but still tappable', 'blur' in ev("getComputedStyle(document.querySelector('#app .vpt')).filter") and ev("document.querySelectorAll('#app .vps').length") == 4)
    pg.click('#app .vp .chip >> text=↻ 2×'); pg.click('#app .vp .chip >> text=↻ 3×'); pg.wait_for_timeout(50); chk('the repeat chip cycles 1× → 2× → 3× → 1×', ev("localStorage.getItem('trk_vrp')") == '1')
    pg.click('#app .vp .chip >> text=Matn'); ev("vpStop()")
    # ---------- shadowing (telefon ovozi) ----------
    ev("()=>{localStorage.setItem('trk_vsh','1');localStorage.setItem('trk_vrp','1');vpStop();__sp=[];render()}"); pg.wait_for_timeout(100)
    pg.click('#app .vp >> text=🔊 Eshit'); pg.wait_for_timeout(60); ev("__sp[0].u.onend()"); pg.clock.run_for(1000); pg.wait_for_timeout(60)
    chk('shadowing: after a sentence the app WAITS for you to repeat it (nothing is spoken yet) and says "🎤 Takrorlang…"', ev("__sp.length") == 1 and '🎤 Takrorlang…' in pg.inner_text('#app .vp') and ev("VP.wt") == 1800, ev("VP&&VP.wt"))
    pg.clock.run_for(900); pg.wait_for_timeout(60); chk('after the wait (a short sentence = at least 1.8 s) the next sentence is spoken and highlighted', ev("__sp.length") == 2 and ev("__sp[1].t") == 'Second sentence follows it.' and ev("VP.i") == 1)
    ev("__sp[1].u.onend()"); pg.wait_for_timeout(30); chk('the wait grows with the sentence length (27 characters → 1.89 s; ~70 ms per character)', ev("VP.wt") == 1890)
    pg.click('#app .vp .chip >> text=0.75×'); pg.wait_for_timeout(60); ev("__sp[__sp.length-1].u.onend()"); pg.wait_for_timeout(30); chk('...and at 0.75× speed you get proportionally longer (27 chars → 1.89 s / 0.75 = 2.52 s)', abs(ev("VP.wt") - 1890 / 0.75) <= 1, ev("VP.wt"))
    ev("vpStop();VPR.spm.rate=1;__sp=[]")
    # pauza va o'tish
    pg.click('#app .vp >> text=🔊 Eshit'); pg.wait_for_timeout(60); ev("__sp[0].u.onend()"); pg.wait_for_timeout(30); pg.click('#app .vp >> text=⏸ Pauza'); pg.clock.run_for(6000); pg.wait_for_timeout(60)
    chk('pausing during the wait stops the countdown: nothing is spoken even after a long time', ev("__sp.length") == 1 and ev("VP.pz") == 1)
    pg.click('#app .vp >> text=▶ Davom etish'); pg.wait_for_timeout(60); chk('resuming goes straight on to the NEXT sentence (the finished one is not repeated)', ev("__sp.length") == 2 and ev("__sp[1].t") == 'Second sentence follows it.')
    ev("__sp[1].u.onend()"); pg.wait_for_timeout(30); pg.click('#app .vp button[aria-label="Keyingi gap"]'); pg.wait_for_timeout(60); n = ev("__sp.length"); pg.clock.run_for(5000); pg.wait_for_timeout(60)
    chk('⏭ during the wait cancels it and speaks the target sentence once (the old timer does not fire a second time)', ev("__sp[__sp.length-1].t") == 'The third one comes now!' and ev("__sp.length") == n)
    ev("__sp[__sp.length-1].u.onend()"); pg.wait_for_timeout(30); k = ev("__sp.length"); pg.click('#app .vp >> text=⏹ To‘xtatish'); pg.clock.run_for(6000); pg.wait_for_timeout(60); chk('⏹ during the wait stops everything for good', ev("VP") is None and ev("__sp.length") == k)
    # ---------- takrorlash soni ----------
    ev("()=>{localStorage.setItem('trk_vsh','0');localStorage.setItem('trk_vrp','2');vpStop();__sp=[];render()}"); pg.wait_for_timeout(100)
    pg.click('#app .vp >> text=🔊 Eshit'); pg.wait_for_timeout(60)
    seq = []
    for i in range(4):
        seq.append(ev("__sp[__sp.length-1].t")); ev("__sp[__sp.length-1].u.onend()"); pg.clock.run_for(400); pg.wait_for_timeout(40)
    chk('repeat 2× (without shadowing): every sentence is spoken twice in a row, with a counter "↻ 1/2", "↻ 2/2"', seq == ['First sentence is here.', 'First sentence is here.', 'Second sentence follows it.', 'Second sentence follows it.'] and '↻' in pg.inner_text('#app .vp'), seq)
    ev("vpStop();__sp=[];localStorage.setItem('trk_vsh','1');localStorage.setItem('trk_vrp','2')"); pg.click('#app .vp >> text=🔊 Eshit'); pg.wait_for_timeout(60)
    seq = []
    for i in range(3):
        seq.append(ev("__sp[__sp.length-1].t")); ev("__sp[__sp.length-1].u.onend()"); pg.clock.run_for(2000); pg.wait_for_timeout(40)
    chk('shadowing + repeat 2×: sentence, wait, same sentence again, wait, then the next', seq == ['First sentence is here.', 'First sentence is here.', 'Second sentence follows it.'], seq)
    ev("vpStop()")
    # ---------- imtihon rejimi ----------
    ev("()=>{__sp=[];vpStart('ex',0)}"); pg.wait_for_timeout(60); ev("__sp[0].u.onend()"); pg.clock.run_for(300); pg.wait_for_timeout(40)
    chk('in exam mode the shadowing/repeat preferences do not apply: the next sentence follows after the normal short gap', ev("__sp.length") == 2 and ev("__sp[1].t") == 'Two.'); ev("vpStop();document.getElementById('tmpv').remove()")
    # ---------- AI ovozi ----------
    ev("""()=>{ovSet('mode','ai');ovClear();localStorage.setItem('trk_vsh','1');localStorage.setItem('trk_vrp','1');vpStop();VPR={};render()}"""); pg.wait_for_timeout(600)
    ev("()=>{ovGen('spm');return 1}"); pg.wait_for_timeout(800); ready = ev("VPR.spm.ready")
    chk('(setup) the AI audio for the answer is prepared', ready is True)
    ev("__sp=[];__au.length=0"); pg.click('#app .vp >> text=🔊 Eshit'); pg.wait_for_timeout(300)
    chk('(setup) playback uses the audio element', ev("VP.eng") == 'ai' and ev("__au.length") == 1)
    ev("()=>{const a=__au[0];a.currentTime=60*0.25;a.ontimeupdate()}"); pg.wait_for_timeout(60)
    chk('AI voice + shadowing: when the audio crosses into the next sentence it is PAUSED for you to repeat ("🎤 Takrorlang…")', ev("__au[0].paused") is True and ev("VP.sw") == 1 and '🎤 Takrorlang…' in pg.inner_text('#app .vp'))
    ev("()=>{const a=__au[0];a.currentTime=60*0.3;a.ontimeupdate()}"); chk('while waiting, further time updates change nothing', ev("VP.i") == 0)
    pg.clock.run_for(2500); pg.wait_for_timeout(80); chk('after the wait the audio plays on and the highlight moves to sentence 2', ev("__au[0].paused") is False and ev("VP.i") == 1 and ev("VP.sw") == 0)
    ev("()=>{const a=__au[0];a.currentTime=60*0.5;a.ontimeupdate()}"); pg.wait_for_timeout(40); pg.click('#app .vp >> text=⏸ Pauza'); pg.clock.run_for(5000); pg.wait_for_timeout(60)
    chk('pausing during an AI wait keeps the audio paused even after the wait would have ended', ev("__au[0].paused") is True and ev("VP.pz") == 1)
    pg.click('#app .vp >> text=▶ Davom etish'); pg.wait_for_timeout(60); chk('resuming continues straight into the next sentence', ev("__au[0].paused") is False and ev("VP.i") == 2)
    ev("()=>{localStorage.setItem('trk_vrp','2');localStorage.setItem('trk_vsh','0');vpStop();__au.length=0;vpStart('spm',0)}"); pg.wait_for_timeout(300)
    ev("()=>{const a=__au[0];a.currentTime=60*0.25;a.ontimeupdate()}"); pg.wait_for_timeout(60)
    chk('AI voice + repeat 2×: crossing into the next sentence jumps BACK to the start of the one just heard (once), then goes on', ev("VP.i") == 0 and ev("__au[0].currentTime") == 0 and ev("VP.k") == 1 and ev("__au[0].paused") is False)
    ev("()=>{const a=__au[0];a.currentTime=60*0.25;a.ontimeupdate()}"); pg.wait_for_timeout(60); chk('...and the second time it moves on to sentence 2', ev("VP.i") == 1 and ev("VP.k") == 0)
    ev("()=>{localStorage.setItem('trk_vrp','1');localStorage.setItem('trk_vsh','0');vpStop();__au.length=0;vpStart('spm',0)}"); pg.wait_for_timeout(300)
    ev("()=>{const a=__au[0];a.currentTime=60*0.25;a.ontimeupdate()}"); pg.wait_for_timeout(60); chk('with shadowing off and repeat 1× nothing changes: no pause, straight on', ev("VP.i") == 1 and ev("__au[0].paused") is False and ev("VP.sw") in (0, None, False))
    ev("()=>{localStorage.setItem('trk_vsh','1');vpStop();__au.length=0;vpStart('spm',3)}"); pg.wait_for_timeout(300); ev("()=>{__au[0].currentTime=59;__au[0].onended()}"); pg.wait_for_timeout(60)
    chk('shadowing also waits after the LAST sentence of a piece before the next piece / the end', ev("VP&&VP.sw") == 1 and '🎤 Takrorlang…' in pg.inner_text('#app .vp'))
    pg.clock.run_for(3000); pg.wait_for_timeout(100); chk('...then the (single) piece is over and the player finishes', ev("VP") is None)
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];localStorage.setItem('trk_vsh','1');localStorage.setItem('trk_vrp','2');render()}", [ui, th]); pg.wait_for_timeout(50)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('the new chips do not overflow the phone screen in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light';localStorage.removeItem('trk_vsh');localStorage.removeItem('trk_vrp')}")
