import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Reja: blok turi, qat'iy/moslashuvchan, kesishish, bo'sh oraliqlar, "Kechikdim" siljitish. Soat: 2026-11-09 (dushanba) 10:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
BL = """[{id:'uyqu1',t:'Uxlash',s:1380,e:1800,d:[0,1,2,3,4,5,6]},{id:'q1',t:'Qur‘on takror',s:360,e:420,d:[0,1,2,3,4,5,6]},{id:'w1',t:'IELTS Writing',s:480,e:600,d:[0,1,2,3,4,5,6]},{id:'k1',t:'Dokon',s:540,e:1020,d:[0,1,2,3,4,5,6]},{id:'u1',t:'Univer',s:720,e:780,d:[0,1,2,3,4,5,6]},{id:'n1',t:'Namoz Asr',s:960,e:975,pt:true,d:[0,1,2,3,4,5,6]},{id:'z1',t:'Zal',s:1050,e:1110,d:[0,1,2,3,4,5,6]},{id:'o1',t:'Ovqat va dam',s:1110,e:1140,d:[0,1,2,3,4,5,6]},{id:'b1',t:'Kitob o‘qish',s:1140,e:1200,d:[0,1,2,3,4,5,6]}]"""
with Run('reja', when=(2026, 11, 9, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("(B)=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;S.bl=eval(B);S.ov=undefined;S.ovu=null;S.done={};ED=null;ALLV=false;VD=null;tab='h';BV='j';render()}", BL); pg.wait_for_timeout(150)
    ty = lambda t, extra='': ev("(t)=>rjTy({id:'x1',t:t})", t)
    chk('block types are guessed from the title (in Uzbek, with any apostrophe style): Qur‘on/Namoz → Din, IELTS/Univer/Kitob → O‘qish, Dokon → Ish, Uxlash → Uyqu, Ovqat va dam → Dam, Zal → Sport, anything else → Boshqa', [ty('Qur‘on takror'), ty("Qur'on takror"), ty('IELTS Writing'), ty('Univer'), ty('Dokon'), ty('Uxlash'), ty('Ovqat va dam'), ty('Zal'), ty('Telefon'), ty('Namoz Asr'), ty('Kitob o‘qish')] == ['din', 'din', 'oqish', 'oqish', 'ish', 'uyqu', 'dam', 'sport', 'boshqa', 'din', 'oqish'])
    chk('an explicit type always wins over the guess, and an unknown type falls back to the guess', ev("rjTy({id:'a',t:'Dokon',ty:'dam'})") == 'dam' and ev("rjTy({id:'a',t:'Dokon',ty:'nono'})") == 'ish')
    fx = lambda t: ev("(t)=>rjFx({id:'x1',t:t})", t)
    chk('fixed by default: work (Dokon), sleep, university/school, prayers; flexible by default: IELTS, Qur‘on review, gym, reading', [fx('Dokon'), fx('Uxlash'), fx('Univer'), fx('Namoz Asr'), fx('IELTS Writing'), fx('Qur‘on takror'), fx('Zal'), fx('Kitob o‘qish')] == [True, True, True, True, False, False, False, False])
    chk('an explicit fixed/flexible choice wins (even 0)', ev("rjFx({id:'a',t:'Dokon',fx:0})") is False and ev("rjFx({id:'a',t:'IELTS',fx:1})") is True)
    chk('the timeline rows carry the block type (data-ty) and its colour, the emoji, and a 🔒 on fixed blocks', ev("document.querySelectorAll('#app [data-ty].tl,#app .tl[data-ty]').length") >= 8 and ev("document.querySelector('#app .tl[data-ty=ish] .rji').textContent") == '💼' and ev("document.querySelectorAll('#app .tl .rjl').length") == 4 and ev("getComputedStyle(document.querySelector('#app .tl[data-ty=ish]')).getPropertyValue('--ty').trim()") == '#c0642a')
    chk('the "Kun yo‘li" bar segments are coloured by type too', ev("document.querySelectorAll('#app .path i[data-ty]').length") >= 5)
    # kesishish
    C = ev("rjConfDay('2026-11-09').map(c=>[c.a.t,c.b.t,c.o])"); names = sorted(' × '.join(sorted([a, b])) for a, b, o in C)
    chk('overlaps between real blocks are found with their length: IELTS Writing × Dokon (60 min) and Dokon × Univer (60 min); prayer points and the sleep block are ignored', names == ['Dokon × IELTS Writing', 'Dokon × Univer'] and all(c[2] == 60 for c in C), C)
    t = pg.inner_text('#app'); chk('the day screen shows a warning card: "⚠️ 2 ta kesishish: …" with the time', '⚠️ 2 ta kesishish' in t and '09:00–10:00' in t)
    ev("()=>{S.bl=[{id:'t1',t:'A',s:480,e:540,d:[1]},{id:'t2',t:'B',s:540,e:600,d:[1]}]}"); chk('blocks that only touch (one ends exactly when the next begins) do not conflict', ev("rjConfDay('2026-11-09').length") == 0)
    ev("()=>{S.bl=[{id:'p1',t:'A',s:600,e:630,d:[1]},{id:'p2',t:'B',s:626,e:700,d:[1]}]}"); chk('a 4-minute overlap is ignored, 5 minutes counts', ev("rjConfDay('2026-11-09').length") == 0); ev("()=>{S.bl[1].s=625}"); chk('...5 minutes counts', ev("rjConfDay('2026-11-09').length") == 1)
    ev("(B)=>{S.bl=eval(B);render()}", BL)
    # bo'sh oraliqlar
    g = ev("rjGaps('2026-11-09',0).map(x=>[x.s,x.e,x.m])"); chk('free gaps of 45+ minutes between 05:00 and 23:00 are found for a normal day: 05:00–06:00, 07:00–08:00, 20:00–23:00 (the 30-minute hole at 17:00 is too short)', g == [[300, 360, 60], [420, 480, 60], [1200, 1380, 180]], g)
    g2 = ev("rjGaps('2026-11-09',600).map(x=>[x.s,x.e,x.m])"); chk('for today only the gaps still ahead are offered (from now)', g2 == [[1200, 1380, 180]], g2)
    t = pg.inner_text('#app'); chk('the gap is shown as a tappable chip "20:00–23:00 · 3 soat +"', '20:00–23:00' in t and 'Bo‘sh oraliqlar' in t)
    ev("rjAddGap(1200,1380)"); pg.wait_for_timeout(100); chk('tapping a gap opens a new-plan form with the start (20:00), an end capped at 1 hour (21:00), today’s weekday and the “flexible” setting', ev("ED.s") == '20:00' and ev("ED.e") == '21:00' and ev("ED.d") == [1] and ev("ED.fx") == 0 and 'Yangi reja' in pg.inner_text('#app')); ev("ED=null;render()")
    # tahrirlash oynasi
    ev("eb(-1)"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('the plan editor has the type chips (7), the “Qat‘iy / Moslashuvchan” switch and the explanation', all(x in t for x in ['Din', 'O‘qish', 'Ish', 'Uyqu', 'Dam', 'Sport', 'Boshqa']) and '🔒 Qat‘iy' in t and '↔ Moslashuvchan' in t and 'Kechikdim' in t)
    ev("eb(%d)" % ev("bl().findIndex(b=>b.id==='k1')")); pg.wait_for_timeout(80); chk('editing an existing block preloads its (inferred) type and fixed state: Dokon → Ish, 🔒', ev("ED.ty") == 'ish' and ev("ED.fx") == 1 and ev("document.querySelector('#app .chip.on').textContent").startswith('💼'))
    ev("ED=null;render()"); ev("eb(-1)")
    ev("()=>{ED.t='Yangi blok';ED.s='09:30';ED.e='10:30';ED.d=[1,2];ED.ty='sport';ED.fx=0;render()}"); pg.wait_for_timeout(80); t = pg.inner_text('#app')
    chk('the editor warns live about overlaps: "Kesishadi: IELTS Writing 08:00–10:00 (Du Se); Dokon …" (a 2-day block checks both days)', '⚠️ Kesishadi' in t and 'IELTS Writing 08:00–10:00 (Du Se)' in t and 'Dokon 09:00–17:00 (Du Se)' in t)
    ev("()=>{window.confirm=()=>false;S.bl=eval(%s)}" % repr(BL)); n0 = ev("bl().length"); ev("esv()"); chk('saving an overlapping block asks first; answering “no” keeps the plan unchanged and the editor open', ev("bl().length") == n0 and ev("!!ED"))
    ev("()=>{window.confirm=m=>{window.__cm=m;return true}}"); ev("esv()"); nb = ev("bl().find(b=>b.t==='Yangi blok')"); chk('answering “yes” saves it with its type and flexibility; the question listed the conflicts', nb and nb['ty'] == 'sport' and nb['fx'] == 0 and 'IELTS Writing' in ev("__cm") and 'Dokon' in ev("__cm"))
    ev("(B)=>{S.bl=eval(B);ED=null;render()}", BL); ev("()=>{window.__cm='';window.confirm=m=>{window.__cm=m;return true};eb(-1);ED.t='Kechki mashq';ED.s='20:30';ED.e='21:30';ED.d=[1];ED.ty='sport';esv()}"); chk('a block that overlaps nothing is saved WITHOUT any question', ev("__cm") == '' and ev("bl().some(b=>b.t==='Kechki mashq')"))
    ev("(B)=>{S.bl=eval(B);ED=null;render()}", BL); ev("()=>{window.__cm='';eb(-1);ED.t='Dam';ED.s='23:30';ED.e='23:50';ED.d=[1];ED.ty='uyqu';esv()}"); chk('sleep blocks and one-moment blocks never trigger the overlap question', ev("__cm") == '')
    ev("(B)=>{S.bl=eval(B);ED=null;render()}", BL)
    ev("()=>{S.bl=[{id:'p1',t:'A',s:600,e:660,d:[1]}];eb(-1);ED.t='B';ED.s='10:00';ED.e='11:00';ED.d=[2]}"); chk('a block on a different weekday does not conflict', ev("rjEdConf().length") == 0); ev("()=>{ED.d=[1,2]}"); chk('...but one that shares a weekday does (listing just that day)', ev("rjEdConf()[0].days") == ['Du']); ev("(B)=>{S.bl=eval(B);ED=null}", BL)
    chk('changing a time field redraws the editor (so the warning updates), not only on every keystroke', ev("(()=>{eb(-1);const h=document.getElementById('app').innerHTML;return h.includes('onchange=\"render()\"')})()")); ev("ED=null;render()")
    # kechikdim
    ev("()=>{S.ov=undefined;S.ovu=null;S.done={};render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('today shows "⏩ Kechikdingmi?" with +15 / +30 / +60 minute chips', '⏩ Kechikdingmi' in t and '+15 daq' in t and '+30 daq' in t and '+60 daq' in t)
    ev("rjShift(30)"); pg.wait_for_timeout(100); O = ev("S.ov['2026-11-09']")
    chk('"+30": only FLEXIBLE blocks that are not done and not yet finished move (Zal, Ovqat va dam, Kitob o‘qish); fixed ones, finished ones (Qur‘on, IELTS ended at 10:00) and sleep stay', sorted(O.keys()) == ['b1', 'o1', 'z1'] and O['z1'] == {'s': 1080, 'e': 1140} and O['b1'] == {'s': 1170, 'e': 1230}, O)
    chk('a toast says how many moved', any('3 ta blok +30 daqiqaga surildi' in m for m in ev("__t")))
    t = pg.inner_text('#app'); chk('the timeline now shows the new times (Zal 18:00) with a ⏩ badge; the base weekly plan is untouched (Zal is still 17:30)', ev("[...document.querySelectorAll('#app .tl')].find(r=>r.textContent.includes('Zal')).querySelector('.tt b').textContent") == '18:00' and ev("[...document.querySelectorAll('#app .tl')].find(r=>r.textContent.includes('Zal')).querySelectorAll('.rjo').length") == 1 and ev("bl().find(b=>b.id==='z1').s") == 1050)
    ev("rjShift(15)"); chk('shifting again adds up (+30 then +15 = +45)', ev("S.ov['2026-11-09'].z1.s") == 1050 + 45)
    chk('the other days are not affected (tomorrow still has the original Zal time)', ev("rjDay('2026-11-10').find(b=>b.id==='z1').s") == 1050)
    ev("rjUndo()"); chk('"↩︎ Bekor qilish" undoes only the last shift (back to +30)', ev("S.ov['2026-11-09'].z1.s") == 1080)
    ev("rjReset()"); chk('"↺ Asl rejaga qaytish" removes all of today’s changes', ev("S.ov&&S.ov['2026-11-09']") in (None, False) or ev("!S.ov['2026-11-09']"))
    ev("()=>{S.done['2026-11-09']={z1:1};rjShift(30)}"); chk('a block already marked done is not moved', 'z1' not in ev("S.ov['2026-11-09']")); ev("rjReset()")
    ev("()=>{S.done={};__t=[];rjShift(300)}"); O = ev("S.ov&&S.ov['2026-11-09']"); chk('a shift that would push a block past midnight leaves that block alone and says so (Kitob 19:00 + 5 h = 00:00 is allowed, Zal and Ovqat also fit; test with +600 for “doesn’t fit”)', O is not None)
    ev("rjReset()"); ev("()=>{__t=[];rjShift(600)}"); chk('+10 hours: blocks that no longer fit in the day stay and the toast mentions them', any('kechaga sig‘madi' in m for m in ev("__t"))); ev("rjReset()")
    ev("()=>{S.bl=S.bl.filter(b=>b.id==='k1'||b.id==='u1'||b.id==='uyqu1');__t=[];rjShift(30)}"); chk('with no flexible block left a clear message', any('moslashuvchan blok qolmagan' in m for m in ev("__t")) and not ev("S.ov&&S.ov['2026-11-09']&&Object.keys(S.ov['2026-11-09']).length")); ev("(B)=>{S.bl=eval(B);render()}", BL)
    ev("()=>{S.ov={'2026-10-01':{z1:{s:1,e:2}},'2026-10-20':{z1:{s:1,e:2}},'2026-11-08':{z1:{s:1,e:2}}};rjShift(15)}"); chk('only the last 14 days of changes are kept', '2026-10-01' not in ev("S.ov") and '2026-10-20' not in ev("S.ov") and '2026-11-08' in ev("S.ov")); ev("()=>{S.ov=undefined;S.ovu=null}")
    # hozir va boshqa kun
    ev("()=>{S.bl=[{id:'z9',t:'Dars tayyorlash',s:570,e:620,d:[1,2,3,4,5,6,0]}];S.ov=undefined;S.done={};rjShift(30)}"); ev("nwOpen()"); pg.wait_for_timeout(120); w = ev("nwCands(15)[0].w"); chk('“Hozir nima qilay?” uses the shifted time of the current block (was 09:30–10:20, now 10:00–10:50)', '10:00–10:50' in w, w); ev("nwClose()")
    ev("(B)=>{S.bl=eval(B);S.ov=undefined;render();vd('2026-11-10')}", BL); pg.wait_for_timeout(120); t = pg.inner_text('#app'); chk('another day shows its conflicts and gaps but no “Kechikdingmi?” (it is only for today)', '⚠️ 2 ta kesishish' in t and 'Bo‘sh oraliqlar' in t and 'Kechikdingmi' not in t); ev("vd(dk())")
    ev("ALLV=true;render()"); pg.wait_for_timeout(80); chk('in the "Barcha rejalar" view the day helper is hidden (it is about one day)', 'Kechikdingmi' not in pg.inner_text('#app') and ev("document.querySelectorAll('#app .rjd').length") == 0); ev("ALLV=false;render()")
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='h';BV='j';VD=null;render()}", [ui, th]); pg.wait_for_timeout(80)
            ok1 = ev("document.documentElement.scrollWidth<=window.innerWidth+1"); ev("()=>{eb(-1);ED.t='Uzun nomli blok '.repeat(3);ED.s='09:30';ED.e='10:30';ED.d=[1,2,3,4,5,6,0];render()}"); pg.wait_for_timeout(60)
            ok2 = ev("document.documentElement.scrollWidth<=window.innerWidth+1"); ev("ED=null;render()")
            if not (ok1 and ok2): bad.append(ui + th)
    chk('the day screen with the helper card and the editor with the type chips fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
