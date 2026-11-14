import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Pomodoro + fon ovozlari, kun hikoyasi, kelajakka xat. Soat: 2026-11-05 10:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
with Run('fokus', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.aiOk=()=>true;window.confirm=()=>true;
      window.__ac=[];const mk=()=>({value:1,setTargetAtTime(v){this.value=v},setValueAtTime(){},exponentialRampToValueAtTime(){}});
      const node=type=>{const n={type,connect(){return n},disconnect(){n.d=1},start(){n.s=1},stop(){n.st=1},frequency:mk(),Q:mk(),gain:mk()};__ac.push(n);return n};
      window.AudioContext=function(){this.sampleRate=8000;this.currentTime=0;this.state='running';this.destination=node('dest');this.createGain=()=>node('gain');this.createBiquadFilter=()=>node('biquad');this.createOscillator=()=>node('osc');this.createBuffer=(c,n)=>({getChannelData:()=>new Float32Array(n)});this.createBufferSource=()=>node('src');this.resume=()=>{}};
      localStorage.removeItem('trk_pm');S.pm={};S.fl=[];S.fk={a:'IELTS'};PMI=0;PMN=null;S.hab=[];S.hb={};S.rw={};rwReset();tab='m';MQV='f';render()}""")
    t = pg.inner_text('#app')
    chk('the Goals screen has the "🍅 Fokus (Pomodoro)" card: 25:00 ready, presets 25/5, 50/10, 15/3, auto-continue, focus areas and the ambient sound chips', '🍅 Fokus (Pomodoro)' in t and '25:00' in t and '25/5' in t and '50/10' in t and '15/3' in t and 'Avto-davom' in t and 'Fon ovozi' in t and all(x in t for x in ['Yomg‘ir', 'To‘lqin', 'Shamol', 'Oq shovqin', 'Jigarrang']) and ev("document.querySelectorAll('#app input[type=range]').length") == 0)
    ev("pmStart()"); pg.wait_for_timeout(80); g = ev("pmG()")
    chk('starting: the work phase runs for 25 minutes, the button becomes "⏸ Pauza" and a floating "🍅 25:00" timer appears', g['ph'] == 'work' and abs(g['end'] - ev("Date.now()") - 25 * 60000) < 2000 and '⏸ Pauza' in pg.inner_text('#app') and '🍅' in ev("document.getElementById('pmb').textContent"))
    pg.clock.run_for(10000); pg.wait_for_timeout(60); chk('the display counts down (10 seconds later: 24:50) without re-rendering the page', ev("document.getElementById('pmt').textContent") in ('24:50', '24:49'))
    pg.click('#app >> text=⏸ Pauza'); pg.wait_for_timeout(60); g = ev("pmG()")
    chk('pausing keeps the remaining time (about 24:50), stops the clock and removes the floating timer', g['end'] == 0 and 24.5 * 60000 < g['left'] <= 24.9 * 60000 and ev("!document.getElementById('pmb')") and '▶ Davom etish' in pg.inner_text('#app'))
    pg.clock.run_for(60000); pg.click('#app >> text=▶ Davom etish'); pg.wait_for_timeout(60); g2 = ev("pmG()")
    chk('resuming continues from the remaining time (a minute of pause is not lost or counted)', abs((g2['end'] - ev("Date.now()")) - g['left']) < 2000)
    # tugash
    ev("()=>{S.fl=[];S.pm={};S.fm={};rwReset()}"); xp0 = ev("dayPts(dk()).t"); pg.clock.run_for(25 * 60000 + 2000); pg.wait_for_timeout(100); g = ev("pmG()")
    chk('when the 25 minutes end: 25 minutes are logged to the focus log under the chosen area, today\u2019s 🍅 count is 1, a toast and a chime follow', ev("S.fl.length") == 1 and ev("S.fl[0].m") == 25 and ev("S.fl[0].a") == 'IELTS' and ev("S.pm[dk()]") == 1 and any('25 daqiqa fokus tugadi' in m for m in ev("__t")) and ev("__ac.filter(n=>n.type==='osc').length") >= 2)
    ev("rwReset()"); chk('the focus minutes become XP automatically through the existing rule (1 XP per 5 minutes: +5 for 25 minutes)', ev("dayPts(dk()).t") - xp0 == 5 and ev("S.fm[dk()]") == 25)
    chk('with auto-continue the 5-minute break starts at once; the card says "Tanaffus"', g['ph'] == 'brk' and 4.5 * 60000 < g['end'] - ev("Date.now()") <= 5 * 60000 and 'Tanaffus' in pg.inner_text('#app') and g['cyc'] == 1)
    pg.clock.run_for(5 * 60000 + 2000); pg.wait_for_timeout(80); chk('after the break the next focus phase starts by itself', ev("pmG().ph") == 'work')
    # 4-chi pomodoro -> uzoq tanaffus
    ev("()=>{const g=pmG();g.cyc=3;g.ph='work';g.end=Date.now()+1000;pmS(g);clearInterval(PMI);PMI=setInterval(pmTick,500)}"); pg.clock.run_for(3000); pg.wait_for_timeout(80); g = ev("pmG()")
    chk('after the 4th focus session comes the LONG break (15 minutes) and the counter shows 4/4', g['ph'] == 'long' and 14 * 60000 < g['end'] - ev("Date.now()") <= 15 * 60000 and '4/4' in pg.inner_text('#app'))
    ev("pmStop()")
    # avto o'chiq
    ev("()=>{const g=pmG();g.auto=0;pmS(g);S.fl=[];S.pm={};pmStart()}"); pg.clock.run_for(25 * 60000 + 2000); pg.wait_for_timeout(80); g = ev("pmG()")
    chk('with auto-continue OFF the app waits after the session: the break is ready (05:00) but does not run until you press Start', g['ph'] == 'brk' and g['end'] == 0 and g['left'] == 5 * 60000 and '05:00' in pg.inner_text('#app') and ev("!document.getElementById('pmb')"))
    ev("pmStop()")
    # o'tkazish
    ev("()=>{const g=pmG();g.auto=1;pmS(g);S.fl=[];S.pm={};pmStart()}"); pg.clock.run_for(7 * 60000 + 5000); pg.click('#app >> text=⏭ O‘tkazish'); pg.wait_for_timeout(80)
    chk('skipping a focus phase after 7 minutes logs those 7 minutes (no 🍅 counted) and moves to the break', ev("S.fl.length") == 1 and ev("S.fl[0].m") == 7 and ev("S.pm[dk()]||0") == 0 and ev("pmG().ph") == 'brk')
    ev("pmStop()"); ev("()=>{S.fl=[];pmStart()}"); pg.clock.run_for(20000); pg.click('#app >> text=⏭ O‘tkazish'); pg.wait_for_timeout(60); chk('skipping within the first minute logs nothing', ev("S.fl.length") == 0)
    pg.click('#app >> text=⏹'); pg.wait_for_timeout(60); g = ev("pmG()"); chk('⏹ stops everything: idle, counter reset, no floating timer', g['ph'] == 'idle' and g['cyc'] == 0 and ev("!document.getElementById('pmb')") and '25:00' in pg.inner_text('#app'))
    # presetlar
    ev("pmSet('p','50')"); ev("pmStart()"); g = ev("pmG()"); chk('the 50/10 preset: a 50-minute focus phase', abs(g['end'] - ev("Date.now()") - 50 * 60000) < 2000)
    chk('presets are locked while running', ev("[...document.querySelectorAll('#app .pmc .chip')].filter(c=>/^\\d+\\/\\d+$/.test(c.textContent.trim())).every(c=>c.disabled)")); ev("pmStop();pmSet('p','15')"); ev("pmStart()"); chk('the 15/3 preset: 15 minutes', abs(ev("pmG().end") - ev("Date.now()") - 15 * 60000) < 2000); ev("pmStop();pmSet('p','25')")
    # fon ovozlari
    ev("()=>{localStorage.removeItem('trk_pm');PMN=null;__ac.length=0}")
    def snd(kind):
        ev("()=>{pmStop();__ac.length=0;pmSet('snd','%s');pmStart()}" % kind)
        r = ev("({k:PMN&&PMN.kind,types:__ac.map(n=>n.type)})"); return r
    r = snd('rain'); chk('"Yomg‘ir": pink noise through a high-pass filter → gain → output', r['k'] == 'rain' and 'highpass' in r['types'] and 'src' in r['types'] and 'gain' in r['types'], r)
    r = snd('wave'); chk('"To‘lqin": brown noise whose volume is swelled slowly by a low-frequency oscillator', r['k'] == 'wave' and 'osc' in r['types'] and r['types'].count('gain') >= 3, r)
    r = snd('wind'); chk('"Shamol": pink noise through a band-pass filter whose frequency drifts with an oscillator', r['k'] == 'wind' and 'bandpass' in r['types'] and 'osc' in r['types'], r)
    r = snd('white'); r2 = snd('brown'); chk('"Oq shovqin" and "Jigarrang" are simple looping noise sources', r['k'] == 'white' and r2['k'] == 'brown' and 'src' in r['types'] and 'src' in r2['types'])
    ev("pmSet('vol',0.5)"); pg.wait_for_timeout(60)
    ev("()=>{pmVol(100)}"); chk('the volume slider changes the volume live (100% → 0.6 gain, the master ceiling)', abs(ev("PMN.gain.gain.value") - 0.6) < 1e-6)
    ev("pmPause()"); chk('pausing stops the sound; so does finishing the focus phase (the break is silent)', ev("PMN") is None)
    ev("pmStart()"); ev("()=>{const g=pmG();g.end=Date.now()+500;pmS(g);clearInterval(PMI);PMI=setInterval(pmTick,500)}"); pg.clock.run_for(2000); pg.wait_for_timeout(100); chk('...the break after a session is silent', ev("pmG().ph") == 'brk' and ev("PMN") is None)
    ev("pmStop();pmSet('snd','rain');pmStart()"); ev("pmSet('snd','')"); chk('choosing "🔇 Yo‘q" while running stops the sound at once', ev("PMN") is None)
    ev("()=>{pmStop();window.AudioContext=undefined;window.webkitAudioContext=undefined;pmSet('snd','rain');pmStart()}"); chk('a browser without WebAudio still runs the timer (no crash, no sound)', ev("pmG().ph") == 'work' and ev("PMN") is None); ev("pmStop()")

    # tiklanish
    ev("()=>{S.fl=[];S.pm={};localStorage.setItem('trk_pm',JSON.stringify({p:'25',ph:'work',end:Date.now()+600000,left:0,cyc:0,snd:'',vol:.5,auto:1,t0:Date.now()-900000}))}"); pg.reload(); pg.wait_for_timeout(600); pg.clock.run_for(3500); pg.wait_for_timeout(200)
    chk('a running timer survives an app restart: the floating timer is back and counting', ev("!!document.getElementById('pmb')") and ev("pmG().ph") == 'work')
