# Kun yakuni qo'shimchalari, haftalik sharh, odat eslatmasi va arxivi. Soat: 2026-10-31 (shanba).
import sys, json
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('kunhafta') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);S.hab=[{id:'h1700000000000',t:'Kitob',e:'📖'},{id:'h1700000000001',t:'Suv ichish'}];S.habA=[];S.hb={};S.hk={};S.nm=S.nm||{d:{}};S.nm.d={};S.q.ny={};S.fm={};S.mood={};S.note={};S.water={};S.fl=[];S.money=[];S.ie.pr=[];S.goals=[{t:'Maqsad',ms:[{t:'A',x:1,xd:dAgo(2)},{t:'B',x:0}],p:0}];S.close={};S.wr={};S.wrd='';S.top={};
      const P=['fajr','dhuhr','asr','maghrib','isha'];for(let i=0;i<14;i++){const k=dAgo(i),hi=i%2===0;S.hb[k]=hi?{h1700000000000:true,h1700000000001:true}:{};S.nm.d[k]={};P.forEach(p=>S.nm.d[k][p]=hi?1:2);if(hi){S.q.ny[k]=1;S.fm[k]=30}S.mood[k]=hi?4:2;if(i<=4)S.ie.pr.push({id:i,d:k,k:'R',s:5,n:8})}
      S.money=[{id:1,d:dAgo(1),k:'in',a:5000000,c:'Maosh',w:'p',ac:'cash'},{id:2,d:dAgo(2),k:'out',a:1000000,c:'Ovqat',w:'p',ac:'cash'}]}""")
    # ---------- kun yakuni ----------
    pg.clock.set_system_time('2026-10-31T21:00:00')
    ev("()=>{S.hb[dk()]={};S.close={};tab='h';BV='m';WO=0;render()}"); pg.wait_for_timeout(120); t = pg.inner_text('#app')
    chk('after 20:00 the evening ritual shows the new steps: 4 habits (2 left), 5 mood, 6 gratitude', 'Kunni yopish' in t and '4. Odatlar (2 ta qoldi)' in t and '5. Kayfiyat' in t and '6. Bugun nimaga minnatdorsan?' in t)
    chk('the habits still to do are chips; the rest-day ones are left out', ev("document.querySelectorAll('.hero .rwch .chip').length") == 2)
    ev("hbS('h1700000000001',dk())"); pg.wait_for_timeout(60); chk('a habit put on rest for today leaves the list (1 left)', '(1 ta qoldi)' in pg.inner_text('#app')); ev("hbS('h1700000000001',dk())")
    pg.click('.hero .rwch .chip >> nth=0'); pg.wait_for_timeout(80); chk('tapping a chip marks that habit done and the count drops', ev("!!S.hb[dk()]['h1700000000000']") and '(1 ta qoldi)' in pg.inner_text('#app'))
    pg.click('.hero .rwch .chip >> nth=0'); pg.wait_for_timeout(80); chk('when all are done it says so', '✓ Hamma odat belgilangan' in pg.inner_text('#app'))
    pg.click('.hero .mood button >> nth=3'); pg.wait_for_timeout(60); chk('mood: the 4th face is saved and highlighted', ev("S.mood[dk()]") == 4 and ev("document.querySelector('.hero .mood button.on')") is not None)
    pg.fill('.hero textarea', 'Quron o‘qidim'); pg.press('.hero textarea', 'Tab'); pg.wait_for_timeout(60); chk('the gratitude line is saved as today\u2019s note', ev("S.note[dk()]") == 'Quron o‘qidim')
    ev("()=>{S.hab=[];render()}"); chk('without habits it explains where to add them', 'Odatlar bo‘limida odat qo‘shsang' in pg.inner_text('#app')); ev("S.hab=[{id:'h1700000000000',t:'Kitob',e:'📖'},{id:'h1700000000001',t:'Suv ichish'}]")
    ev("render()"); pg.click('.hero >> text=Kunni yopish >> nth=-1') if False else None
    ev("closeDay(dk(),true)"); pg.wait_for_timeout(80); chk('closing the day still works (summary screen)', 'Kun yopildi' in pg.inner_text('#app'))
    # ---------- haftalik sharh ----------
    a = ev("wrAgg(0)"); b = ev("wrAgg(7)")
    chk('this week vs the previous week: habits 57% vs 43%, prayers 20 vs 15, hifz 4 vs 3, focus 120 vs 90 min, IELTS days 5 vs 0, goal steps 1 vs 0, mood 3.1 vs 2.9', a['hab'] == 57 and b['hab'] == 43 and a['nm'] == 20 and b['nm'] == 15 and a['hf'] == 4 and b['hf'] == 3 and a['fm'] == 120 and b['fm'] == 90 and a['ie'] == 5 and b['ie'] == 0 and a['ms'] == 1 and b['ms'] == 0 and a['mood'] == 3.1 and b['mood'] == 2.9, (a, b))
    chk('money (personal): income 5 000 000 and expenses 1 000 000 this week, nothing last week', a['inn'] == 5000000 and a['out'] == 1000000 and b['inn'] == 0)
    rows = {r[0]: r for r in ev("wrRows()")}; chk('the rows show the value and the change from last week (+14%, +5, +1, +30 daq, +5, +1)', rows['Odatlar'][1] == '57%' and rows['Odatlar'][2] == '+14%' and rows['Namoz (farz)'][2] == '+5' and rows['Hifz: yangi bet'][2] == '+1' and rows['Fokus'][1] == '2 soat 0 daq' and rows['Fokus'][2] == '+30 daq' and rows['IELTS mashq kunlari'][2] == '+5' and rows['Maqsad bosqichlari'][2] == '+1' and rows['Kayfiyat'][2] == '+0.2', rows)
    chk('Saturday: no banner; the goals are for NEXT week (Mon 2 Nov)', ev("wrBar()") == '' and ev("wrTarget()") == '2026-11-02' and ev("wrRid()") is None)
    ev("()=>{tab='h';BV='t';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('Bugun → Tahlil shows the weekly review card above the Life panel', 'Haftalik sharh' in t and t.index('Haftalik sharh') < t.index('Hayot paneli') and 'Keyingi hafta uchun 3 ta maqsad' in t)
    pg.fill('#wrg0', 'Har kuni 5 bet hifz'); pg.fill('#wrg1', 'IELTS mock ishla'); pg.click('#app button >> text="Saqlash"'); pg.wait_for_timeout(100); g = ev("S.wr['2026-11-02'].g")
    chk('saving stores the non-empty goals under next Monday and says so', [x['t'] for x in g] == ['Har kuni 5 bet hifz', 'IELTS mock ishla'] and all(x['x'] == 0 for x in g) and any('saqlandi' in x for x in ev("__t")))
    pg.clock.set_system_time('2026-11-01T20:30:00'); ev("()=>{S.wrd='';tab='h';BV='m';render()}"); pg.wait_for_timeout(120)
    chk('Sunday evening: a banner invites to the review (the week of Oct 26 is being reviewed)', ev("wrRid()") == '2026-10-26' and 'Haftalik sharh tayyor' in pg.inner_text('#app') and ev("wrTarget()") == '2026-11-02')
    pg.click('#app >> text=Ko‘rish'); pg.wait_for_timeout(100); chk('"Ko‘rish" opens the review', ev("BV") == 't' and 'Keyingi hafta uchun 3 ta maqsad' in pg.inner_text('#app') and ev("document.getElementById('wrg0').value") == 'Har kuni 5 bet hifz')
    pg.click('#app button >> text="Saqlash"'); pg.wait_for_timeout(100); chk('after saving the banner is gone for this week', ev("S.wrd") == '2026-10-26' and ev("wrBar()") == '')
    ev("()=>{window.__sh=null;navigator.share=async o=>{window.__sh=o}}"); ev("S.wrd=''"); pg.click('#app >> text=📤 Ulashish'); pg.wait_for_timeout(100); sh = ev("__sh")
    chk('"Ulashish" opens the share sheet with a ready text: title, every row with its change, and next week\u2019s goals; it counts as reviewed', sh and '📅 Haftalik sharh' in sh['text'] and '• Odatlar: 43% (-14%)' in sh['text'] and 'Keyingi hafta maqsadlari:' in sh['text'] and '1. Har kuni 5 bet hifz' in sh['text'] and ev("S.wrd") == '2026-10-26', sh)
    ev("()=>{navigator.share=undefined;window.__cp='';navigator.clipboard.writeText=async t=>{window.__cp=t}}"); pg.click('#app >> text=📤 Ulashish'); pg.wait_for_timeout(100); chk('without a share sheet the text is copied instead', '📅 Haftalik sharh' in ev("__cp") and any('Nusxalandi' in x for x in ev("__t")))
    pg.clock.set_system_time('2026-11-02T10:00:00'); ev("()=>{S.wrd='';tab='h';BV='t';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('Monday: the previous week is still reviewed, but the goals are for THIS week; last week\u2019s plan can be ticked', ev("wrRid()") == '2026-10-26' and ev("wrTarget()") == '2026-11-02' and 'Shu hafta uchun 3 ta maqsad' in t)
    pg.click('#app .row >> text=Har kuni 5 bet hifz'); pg.wait_for_timeout(80); chk('ticking a goal of the week saves it as done', ev("S.wr['2026-11-02'].g[0].x") == 1)
    ev("()=>{document.getElementById('wrg1').value='Boshqa maqsad'}"); pg.click('#app button >> text="Saqlash"'); pg.wait_for_timeout(100); chk('saving again keeps the ticks of unchanged goals and replaces edited ones', ev("S.wr['2026-11-02'].g.map(x=>x.t+':'+x.x)") == ['Har kuni 5 bet hifz:1', 'Boshqa maqsad:0'])
    pg.clock.set_system_time('2026-10-31T21:00:00')
    # ---------- odat eslatmasi va arxivi ----------
    ev("()=>{S.hab=[{id:'h1700000000000',t:'Kitob',e:'📖'},{id:'h1700000000001',t:'Suv ichish'}];S.habA=[];S.rem.on=true;S.rem.tg=false;tab='o';OT='j';HV='m';render()}"); pg.wait_for_timeout(100)
    pg.click('#app span[onclick^="hbE(0)"]'); pg.wait_for_timeout(80); chk('the editor has a reminder time field and an "Arxivlash" button next to "O‘chirish"', ev("!!document.getElementById('hbrt')") and '📦 Arxivlash' in pg.inner_text('#hbs') and 'O‘chirish' in pg.inner_text('#hbs'))
    pg.fill('#hbrt', '22:00'); pg.click('#hbs >> text=Saqlash'); pg.wait_for_timeout(100); chk('a reminder time is saved on the habit and shown in its row', ev("S.hab[0].rt") == '22:00' and '🔔 22:00' in pg.inner_text('#app'))
    rr = [x for x in ev("remRows()") if x.get('kind', '').startswith('hb:')]; chk('the reminder rows include the habit: its time, a title with the emoji, every day, kind hb:<id>', len(rr) == 1 and rr[0]['hhmm'] == '22:00' and rr[0]['title'] == '🔔 📖 Kitob' and rr[0]['days'] == [0, 1, 2, 3, 4, 5, 6] and rr[0]['kind'] == 'hb:h1700000000000', rr)
    ev("S.rem.on=false"); chk('with reminders switched off there are no rows at all', ev("remRows()") == []); ev("S.rem.on=true")
    pg.click('#app span[onclick^="hbE(0)"]'); pg.click('#hbs >> text=Eslatmasiz'); pg.click('#hbs >> text=Saqlash'); pg.wait_for_timeout(100); chk('"Eslatmasiz" removes the time', ev("S.hab[0].rt") is None and not [x for x in ev("remRows()") if x.get('kind', '').startswith('hb:')])
    pg.click('#app span[onclick^="hbE(0)"]'); pg.fill('#hbrt', '07:30'); pg.click('#hbs >> text=Saqlash'); pg.wait_for_timeout(60)
    ev("S.hb[dAgo(1)]={h1700000000000:true}"); pg.click('#app span[onclick^="hbE(0)"]'); pg.click('#hbs >> text=📦 Arxivlash'); pg.wait_for_timeout(100)
    chk('archiving moves the habit out of the list (and its reminder) into the archive with today\u2019s date; its history stays', len(ev("S.hab")) == 1 and ev("S.hab[0].t") == 'Suv ichish' and ev("S.habA[0].t") == 'Kitob' and ev("S.habA[0].ar") == '2026-10-31' and ev("!!S.hb[dAgo(1)]['h1700000000000']") and not [x for x in ev("remRows()") if x.get('kind', '').startswith('hb:')])
    t = pg.inner_text('#app'); chk('the grid no longer shows it; an "Arxiv (1)" section lists it', ev("document.querySelectorAll('#app .mn .mr').length") == 1 and 'Arxiv (1)' in t)
    ev("document.querySelector('#app details.sd summary').click()") if False else None
    ev("document.querySelectorAll('#app details').forEach(d=>{if(d.textContent.includes('Arxiv'))d.open=true})"); pg.click('#app >> text=Qaytarish'); pg.wait_for_timeout(100)
    chk('restoring brings it back to the habit list (at the end), clears the archive date, keeps its reminder time and history', len(ev("S.hab")) == 2 and ev("S.hab[1].t") == 'Kitob' and ev("S.hab[1].ar") is None and ev("S.hab[1].rt") == '07:30' and len(ev("S.habA")) == 0 and 'Arxiv' not in pg.inner_text('#app'))
    ev("()=>{const x=S.hab.pop();x.ar=dk();S.habA=[x];render()}"); ev("hbArcDel('h1700000000000')"); chk('an archived habit can be deleted for good', len(ev("S.habA")) == 0)
