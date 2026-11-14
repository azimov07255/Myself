# AI Listening, materialdan savollar, talaffuz tekshiruvi. Soat: 2026-10-31 10:00.
import sys, json
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
LINES = ["Good morning, I would like to join your gym, could you tell me about the membership options?", "Of course. We have monthly and yearly plans, and the monthly plan costs forty five pounds.",
 "That sounds fine. Is there a swimming pool included in that price?", "Yes, the pool is open every day from six in the morning until ten at night.", "Great. And where exactly is the gym located, I am new to this area.",
 "We are on Green Street, right next to the central library, about ten minutes from the station.", "Perfect. Do I need to bring any documents to sign up today?", "Just your passport or a driving licence, and we will take a photo for your card.",
 "Can I also book a personal trainer for my first week?", "Certainly, our trainer Maria is free on Friday morning, and she charges twenty pounds per hour.", "Friday works well for me. What time does she start?",
 "She starts at nine o'clock, so please arrive ten minutes early to fill in the form.", "Thank you very much, you have been really helpful today.", "You are welcome, and we look forward to seeing you on Friday."]
SCRIPT = [{'s': 'A' if i % 2 == 0 else 'B', 't': t} for i, t in enumerate(LINES)]
QS = [{'t': 'gap', 'q': 'The monthly plan costs ____ pounds.', 'a': 'forty five', 'why': 'Ikkinchi replika.'}, {'t': 'gap', 'q': 'The gym is on ____ Street.', 'a': 'Green', 'why': 'Oltinchi replika.'},
      {'t': 'gap', 'q': 'The pool closes at ____ at night.', 'a': 'ten', 'why': 'To‘rtinchi.'}, {'t': 'gap', 'q': 'The trainer Maria is free on ____ morning.', 'a': 'Friday', 'why': '10-replika.'},
      {'t': 'gap', 'q': 'She charges ____ pounds per hour.', 'a': 'twenty', 'why': '10-replika.'},
      {'t': 'mcq', 'q': 'What documents are needed?', 'o': ['Bank card', 'Passport or driving licence', 'Student card', 'Tax number'], 'a': 'B', 'why': '8-replika.'},
      {'t': 'mcq', 'q': 'Where is the gym?', 'o': ['Next to the station', 'Next to the central library', 'Near the pool', 'Opposite the bank'], 'a': 'B', 'why': '6-replika.'},
      {'t': 'mcq', 'q': 'What time does the trainer start?', 'o': ['Eight', 'Nine o’clock', 'Ten', 'Eleven'], 'a': 'B', 'why': '12-replika.'},
      {'t': 'gap', 'q': 'The shop sells ____ daily.', 'a': 'zeppelin', 'why': 'yo‘q'}]
GOOD = {'title': 'Joining a gym', 'script': SCRIPT, 'questions': QS}
with Run('y12a') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.aiOk=()=>true;window.__sp=[];window.__voices=[{name:'Alex',lang:'en-US',localService:true},{name:'Samantha',lang:'en-US',localService:true},{name:'Daniel',lang:'en-GB',localService:true}];
      window.__tts={getVoices:()=>window.__voices,speak:u=>window.__sp.push({t:u.text,v:u.__voice&&u.__voice.name,pitch:u.pitch,rate:u.rate,u}),cancel:()=>{window.__cx=(window.__cx||0)+1}};S.ie.words=[];S.ie.mat=[];S.ie.pr=[];S.ie.lp=[];S.ie.pt=[];S.ie.mk=null;S.ie.target=7;tab='e';EV='i';IVW='x';AXO.l=true;AXO.t=true;render()}""")
    # ---------- voices ----------
    chk('a second voice for the other speaker: the preferred voice first, another one second; with only one voice both are the same', ev("[ieVoice('us').name,ieVoice('us',1).name,ieVoice('uk',1).name]") == ['Samantha', 'Alex', 'Daniel'])
    # ---------- validation ----------
    qz = lambda q, t='friday green ten forty five': ev("(x)=>qzClean(x[0],x[1]).map(q=>q.t+':'+q.a)", [q, t])
    chk('qzClean keeps valid questions and drops: bad TFNG value, MCQ with 2 options, gap not in the text, gap longer than 2 words, gap without a blank', qz([{'t': 'tfng', 'q': 'a', 'a': 'MAYBE'}, {'t': 'tfng', 'q': 'b', 'a': 'true'}, {'t': 'mcq', 'q': 'c', 'o': ['a', 'b'], 'a': 'A'}, {'t': 'mcq', 'q': 'd', 'o': list('abcd'), 'a': 'c'}, {'t': 'gap', 'q': 'x ____', 'a': 'zeppelin'}, {'t': 'gap', 'q': 'x ____', 'a': 'friday green ten'}, {'t': 'gap', 'q': 'no blank', 'a': 'friday'}, {'t': 'gap', 'q': 'x ____', 'a': 'Friday'}]) == ['tfng:TRUE', 'mcq:C', 'gap:friday'])
    v = lambda j: ev("(x)=>{try{const r=lqValid(x);return {q:r.q.length,s:r.script.length,sp:r.script.map(l=>l.s).join('')}}catch(e){return {err:e.message}}}", j)
    r = v(GOOD); chk('a good listening exercise is accepted: 14 lines, the 8 answerable questions (the invented-answer one is dropped)', r['q'] == 8 and r['s'] == 14, r)
    chk('speakers other than A/B become A; one-word lines are dropped', v(dict(GOOD, script=[{'s': 'C', 't': 'Hello there my friend'}] + SCRIPT + [{'s': 'A', 't': 'Hi'}]))['sp'].startswith('A') and v(dict(GOOD, script=SCRIPT + [{'s': 'A', 't': 'Hi'}]))['s'] == 14)
    chk('fewer than 8 lines or under 120 words -> "too short"', 'juda qisqa' in v(dict(GOOD, script=SCRIPT[:5])).get('err', ''))
    chk('fewer than 5 verifiable questions -> refused', 'ishonchli chiqmadi' in v(dict(GOOD, questions=QS[:3])).get('err', ''))
    chk('garbage -> refused', 'yozuv bermadi' in v({'x': 1}).get('err', ''))
    # ---------- generation ----------
    ev("""(g)=>{window.__calls=[];window.fnAI=async(b)=>{window.__calls.push(b);await new Promise(r=>setTimeout(r,200));return {text:JSON.stringify(g)}};LQ={topic:'booking a gym',sec:3,busy:0,err:'',d:null,pl:0,i:-1,tok:0,played:0,once:0};render()}""", GOOD)
    pg.click('#app summary >> text="🎧 AI Listening mashqi"') if not ev("document.querySelector('#app details.sd[open] input[placeholder^=Mavzu]')") else None
    chk('the Listening section offers a topic, four sections and one AI request', 'Section 3' in pg.inner_text('#app') and 'Listening mashqi yaratish' in pg.inner_text('#app'))
    pg.click('#app button >> text="✨ Listening mashqi yaratish"'); pg.wait_for_timeout(80)
    chk('while the AI works the button is disabled', ev("LQ.busy") == 1 and ev("[...document.querySelectorAll('#app .big')].some(b=>b.disabled)"))
    R.pg.clock.run_for(400); pg.wait_for_timeout(200)
    c = ev("__calls"); chk('one request: action iex, kind listening, the topic, the chosen section and the target band', len(c) == 1 and c[0]['action'] == 'iex' and c[0]['kind'] == 'listening' and c[0]['topic'] == 'booking a gym' and c[0]['section'] == 3 and c[0]['band'] == 7, c)
    t = pg.inner_text('#app'); chk('the exercise is shown with its title and questions but WITHOUT the script text', 'Joining a gym' in t and 'The monthly plan costs' in t and 'right next to' not in t and '▶ Tinglash' in t)
    # ---------- playback ----------
    pg.click('#app >> text="▶ Tinglash"'); pg.wait_for_timeout(100)
    chk('playing starts with line 1 spoken by speaker A (first voice, higher pitch)', ev("__sp.length") == 1 and ev("__sp[0].t") == LINES[0] and ev("__sp[0].v") == 'Samantha' and ev("__sp[0].pitch") > 1.0, ev("__sp.map(x=>[x.v,x.pitch])"))
    pg.click('#app input.rgp >> nth=0'); pg.keyboard.type('forty five'); ev("__sp[0].u.onend()"); pg.clock.run_for(400); pg.wait_for_timeout(60)
    chk('line 2 (speaker B) is spoken with the SECOND voice and a lower pitch', ev("__sp.length") == 2 and ev("__sp[1].v") == 'Alex' and ev("__sp[1].pitch") < 1.0)
    ev("__sp[1].u.onend()"); pg.clock.run_for(400); pg.wait_for_timeout(60)
    chk('while it plays, the answer box keeps focus and what you typed (no re-render per line)', ev("document.activeElement.className") == 'rgp' and ev("document.activeElement.value") == 'forty five' and 'Replika 3 / 14' in pg.inner_text('#lqs'), (ev("document.activeElement.className"), pg.inner_text('#lqs')))
    ev("window.__cx=0"); pg.click('#app >> text="⏹ To‘xtatish"'); pg.wait_for_timeout(60); n0 = ev("__sp.length"); ev("__sp[2].u.onend()"); pg.clock.run_for(500)
    chk('"To‘xtatish" cancels the speech and a late "end" of the stopped line does not continue', ev("__cx") >= 1 and ev("__sp.length") == n0 and ev("LQ.pl") == 0)
    ev("window.__sp=[]"); pg.click('#app >> text="▶ Tinglash"'); pg.wait_for_timeout(60)
    for i in range(14):
        ev("(i)=>window.__sp[i].u.onend()", i) if i < len(ev("__sp")) else None; pg.clock.run_for(400); pg.wait_for_timeout(30)
    chk('after the last line it stops by itself and offers "Qayta tinglash" (heard 1 time)', ev("LQ.pl") == 0 and ev("LQ.played") == 1 and '▶ Qayta tinglash' in pg.inner_text('#app') and len(ev("__sp")) == 14, (ev("LQ.played"), len(ev("__sp"))))
    pg.check('#app label:has-text("faqat bir marta") input'); pg.wait_for_timeout(60); chk('"only once, like in the exam" disables replaying', ev("[...document.querySelectorAll('#app button')].find(b=>b.textContent.includes('Qayta tinglash')).disabled") is True)
    pg.uncheck('#app label:has-text("faqat bir marta") input')
    # ---------- answering ----------
    ev("""()=>{const a=QZ.l.ans;a[0]='Forty-five';a[1]='green';a[2]='nine';a[3]='friday';a[4]='twenty';a[5]='B';a[6]='A';a[7]='B';render()}""")
    ev("ieDp().L=0;S.ie.lp=[];window.confirm=()=>true;mkStart()"); pg.click('#app >> text="✅ Tekshirish"'); pg.wait_for_timeout(100)
    chk('checking: 6 / 8 (punctuation and capitals ignored: "Forty-five" = "forty five"; "nine" and "A" are wrong)', ev("QZ.l.sc") == 6 and '6 / 8' in pg.inner_text('#app') and 'To‘g‘ri javob: ten' in pg.inner_text('#app'))
    chk('the transcript opens after checking', 'We are on Green Street' in pg.inner_text('#app') and 'A:' in pg.inner_text('#app'))
    chk('the result is stored and today\u2019s Listening plan item is ticked', ev("S.ie.lp.length") == 1 and ev("S.ie.lp[0].s") == 6 and ev("S.ie.lp[0].n") == 8 and ev("S.ie.lp[0].sec") == 3 and ev("ieDp().L") == 1)
    chk('an active mock gets the Listening raw score on the 40-scale (6/8 = 30)', ev("S.ie.mk.L") == 30)
    pg.click('#app >> text="📰 Materiallarga qo‘sh"'); chk('the script can be sent to Materiallar (speaker labels kept)', ev("S.ie.mat[0].k") == 'a' and ev("S.ie.mat[0].x").startswith('A: Good morning') and ev("S.ie.mat[0].t") == 'Joining a gym')
    pg.click('#app >> text="Yangi mashq"'); chk('"Yangi mashq" returns to the form', ev("LQ.d") is None and 'Listening mashqi yaratish' in pg.inner_text('#app'))
    ev("()=>{window.fnAI=async()=>{throw new Error('Bugungi limit tugadi (40 ta so‘rov).')};LQ.err=''}"); pg.click('#app button >> text="✨ Listening mashqi yaratish"'); pg.wait_for_timeout(300)
    chk('an AI error is shown and the button stays usable', 'Bugungi limit tugadi' in pg.inner_text('#app') and not ev("[...document.querySelectorAll('#app .big')].some(b=>b.disabled)"))
    # ---------- questions from a material ----------
    TXT = ("The city council announced that the new plan mitigated the risk of flooding in low-lying districts. Critics argued that the scheme was far too expensive for residents. " * 3)
    LONG = ("Sentence number %d is a perfectly ordinary sentence about the weather in the city today. ")
    ev("""(a)=>{S.ie.mat=[{id:10,t:'Floods',k:'a',x:a[0],c:[],au:0,d:dk(),an:null},{id:11,t:'Long text',k:'a',x:a[1],c:[],au:0,d:dk(),an:null}];tab='e';EV='i';IVW='a';render();IMF.add=0;ieMatOpen(10)}""", [TXT, ''.join(LONG % i for i in range(70))]); pg.wait_for_timeout(400)
    chk('the reader has a "📝 Savollar" button for texts', '📝 Savollar' in pg.inner_text('#iem'))
    MQ = {'questions': [{'t': 'tfng', 'q': 'Critics liked the scheme.', 'a': 'FALSE', 'why': 'Tanqid qilishdi.'}, {'t': 'tfng', 'q': 'The plan cost 5 million.', 'a': 'NOT GIVEN', 'why': 'Narx aytilmagan.'},
          {'t': 'mcq', 'q': 'What did the plan reduce?', 'o': ['Noise', 'Flood risk', 'Traffic', 'Crime'], 'a': 'B', 'why': 'mitigated'}, {'t': 'mcq', 'q': 'Who criticised it?', 'o': ['Critics', 'Judges', 'Pilots', 'Chefs'], 'a': 'A', 'why': 'critics'},
          {'t': 'gap', 'q': 'The districts are ____ .', 'a': 'low-lying', 'why': 'matn'}, {'t': 'gap', 'q': 'The scheme was far too ____ .', 'a': 'expensive', 'why': 'matn'}, {'t': 'gap', 'q': 'x ____', 'a': 'zeppelin', 'why': ''}]}
    ev("(g)=>{window.__calls=[];window.fnAI=async(b)=>{window.__calls.push(b);return {text:JSON.stringify(g)}}}", MQ)
    pg.click('#iem >> text="📝 Savollar"'); pg.wait_for_timeout(100); chk('the sheet explains what will happen and offers to generate (1 AI request)', 'Materialdan savollar' in pg.inner_text('#iemz') and 'Savollar tuz' in pg.inner_text('#iemz'))
    pg.click('#iemz >> text="✨ Savollar tuz"'); pg.wait_for_timeout(300); c = ev("__calls")
    chk('one request with kind material and the text of the material', len(c) == 1 and c[0]['kind'] == 'material' and c[0]['text'].startswith('The city council') and len(c[0]['text']) <= 3600)
    chk('6 verifiable questions are shown (the one with an answer not in the text is dropped)', ev("QZ.m.q.length") == 6 and ev("document.querySelectorAll('#iemz .rdq').length") == 6)
    for i, a in enumerate(['FALSE', 'NOT GIVEN', 'B', 'A']): ev("qzSet('m',%d,'%s')" % (i, a))
    ev("QZ.m.ans[4]='Low-Lying';QZ.m.ans[5]='expensiv'"); xp = ev("S.ie.pr.length"); pg.click('#iemz >> text="✅ Tekshirish"'); pg.wait_for_timeout(100)
    chk('6 / 6: gap answers tolerate capitals and a one-letter typo', ev("QZ.m.sc") == 6 and '6 / 6' in pg.inner_text('#iemz'))
    chk('the result is saved as a Reading practice (source: material) and today\u2019s Reading item is ticked', ev("S.ie.pr.length") == xp + 1 and ev("S.ie.pr[S.ie.pr.length-1].src") == 'material' and ev("S.ie.pr[S.ie.pr.length-1].topic") == 'Floods' and ev("ieDp().R") == 1)
    ev("mzClose()"); pg.click('#iem >> text="📝 Savollar"'); pg.wait_for_timeout(80); chk('reopening the same material shows the same finished quiz (not a new request)', '6 / 6' in pg.inner_text('#iemz') and len(ev("__calls")) == 1)
    ev("ieMatClose()"); ev("ieMatOpen(11)"); pg.wait_for_timeout(300); pg.click('#iem >> text="📝 Savollar"'); pg.wait_for_timeout(80)
    chk('another material starts fresh; a long text is split into parts to choose from', 'Matn' in pg.inner_text('#iemz') and ev("document.querySelectorAll('#iemz .seg button').length") >= 2)
    pg.click('#iemz .seg button >> nth=1'); pg.click('#iemz >> text="✨ Savollar tuz"'); pg.wait_for_timeout(300)
    chk('the chosen part (2nd) is what is sent', ev("__calls.length") == 2 and ev("__calls[1].text") == ev("iePartsOf(ieText(S.ie.mat[1]))[1]"))
    ev("()=>{delete QZ.m;window.fnAI=async()=>({text:JSON.stringify({questions:[MQ_X]})});}".replace('MQ_X', json.dumps(MQ['questions'][0]))); pg.evaluate("mzDraw()"); pg.click('#iemz >> text="✨ Savollar tuz"'); pg.wait_for_timeout(300)
    chk('fewer than 4 usable questions -> an error message instead of a broken quiz', 'ishonchli chiqmadi' in pg.inner_text('#iemz') and ev("QZ.m") is None)
    ev("ieMatClose()")
    # ---------- pronunciation ----------
    ev("""()=>{S.ie.words=[{id:1,w:'mitigate',m:'x',e:'Trees mitigate the heat in crowded cities.',c:'The new plan mitigated the risk of flooding in low-lying districts.',box:0,due:dk(),t:1},{id:2,w:'bad',m:'x',e:'Too short.',c:'',box:0,due:dk(),t:1}];S.ie.mat=[];PT={ref:'',busy:0,rec:null,res:null,heard:'',err:''};IVW='x';AXO.t=true;render()}""")
    src = ev("ptSources()"); chk('sentence sources: vocabulary examples and contexts of 5-25 words (too-short ones are skipped)', sorted(src) == sorted(['Trees mitigate the heat in crowded cities.', 'The new plan mitigated the risk of flooding in low-lying districts.']), src)
    ev("S.ie.words=[]"); pg.click('#app >> text="🎲 Lug‘at yoki materialdan gap"'); pg.wait_for_timeout(60); chk('with no source a clear message appears', 'Gap manbasi yo‘q' in pg.inner_text('#app'))
    pg.fill('#ptr', 'Too short'); pg.click('#app >> text="Olish"'); chk('an own sentence needs at least 3 words', 'Kamida 3 so‘zli gap' in pg.inner_text('body'))
    REF = 'The new plan mitigated the risk of flooding in low-lying districts.'
    pg.fill('#ptr', REF); pg.click('#app >> text="Olish"'); pg.wait_for_timeout(60)
    chk('the sentence is shown with model buttons (normal and slow) and the record button', REF in pg.inner_text('#app') and '🔊 Namuna' in pg.inner_text('#app') and '🐢 Sekin' in pg.inner_text('#app') and '🎙 O‘qishni boshlash' in pg.inner_text('#app'))
    ev("window.__sp=[]"); pg.click('#app >> text="🐢 Sekin"'); chk('the slow model is spoken at a low rate', abs(ev("__sp[0].rate") - 0.6) < 0.02 and ev("__sp[0].t") == REF)
    ev("""()=>{window.__rec=0;navigator.mediaDevices.getUserMedia=async()=>({getTracks:()=>[{stop(){window.__rec++}}]});window.MediaRecorder=class{constructor(){this.mimeType='audio/mp4'}start(){}stop(){this.ondataavailable({data:new Blob([new Uint8Array(4000)])});setTimeout(()=>this.onstop(),0)}};
      window.__up=[];window.fnUpload=async(f,b,n)=>{window.__up.push([f,b.size,n]);return window.__resp}}""")
    ev("(r)=>{window.__resp=r}", {'cues': [{'t': 'The new plan mitigated the risk of flooding in low lying district'}], 'dur': 5})
    ev("window.aiOk=()=>false"); pg.click('#app >> text="🎙 O‘qishni boshlash"'); chk('not signed in: a clear message, nothing recorded', 'hisobga kirish' in pg.inner_text('body') and ev("PT.rec") is None); ev("window.aiOk=()=>true")
    pg.click('#app >> text="🎙 O‘qishni boshlash"'); pg.wait_for_timeout(100); chk('recording starts and the button changes to "⏹ Tugatish"', ev("!!PT.rec") and '⏹ Tugatish' in pg.inner_text('#app'))
    pg.click('#app >> text="⏹ Tugatish"'); pg.clock.run_for(50); pg.wait_for_timeout(300)
    chk('stopping uploads the recording to the transcript action (extension from the type: .m4a) and releases the microphone', ev("__up.length") == 1 and ev("__up[0][0]") == {'action': 'transcript'} and ev("__up[0][2]") == 'say.m4a' and ev("__rec") == 1, ev("__up"))
    r = ev("PT.res"); chk('result: 10 of 12 words matched = 83%; the 2 missed words are ("low-lying" heard as two words) found', r['pct'] >= 75 and r['pct'] <= 92 and len(r['missed']) >= 1, r)
    t = pg.inner_text('#app'); chk('the result screen shows the percentage, coloured words, chips to hear the missed words and what the app heard', '%' in t and ev("document.querySelectorAll('#app .dno').length") >= 1 and ev("document.querySelectorAll('#app .dok').length") >= 8 and 'Ilova nimani eshitdi' in t)
    chk('the attempt is stored and today\u2019s Speaking item is ticked', ev("S.ie.pt.length") == 1 and ev("S.ie.pt[0].p") == r['pct'] and ev("ieDp().S") == 1)
    ev("window.__sp=[]"); pg.click('#app .rwch .chip >> nth=0'); chk('a missed-word chip speaks that word', len(ev("__sp")) == 1)
    ev("(r)=>{window.__resp=r}", {'cues': [{'t': 'The new plan mitigated the risk of flooding in low-lying districts.'}], 'dur': 5}); pg.click('#app >> text="🎙 O‘qishni boshlash"'); pg.wait_for_timeout(60); pg.click('#app >> text="⏹ Tugatish"'); pg.clock.run_for(50); pg.wait_for_timeout(300)
    chk('a perfect reading = 100% and the average of the last attempts is shown', ev("PT.res.pct") == 100 and 'o‘rtachasi' in pg.inner_text('#app') and ev("S.ie.pt.length") == 2)
    ev("(r)=>{window.__resp=r}", {'cues': [{'t': '   '}], 'dur': 1}); pg.click('#app >> text="🎙 O‘qishni boshlash"'); pg.wait_for_timeout(60); pg.click('#app >> text="⏹ Tugatish"'); pg.clock.run_for(50); pg.wait_for_timeout(300)
    chk('if nothing was heard the user is told and nothing is stored', 'eshitilmadi' in pg.inner_text('#app') and ev("S.ie.pt.length") == 2)
    ev("()=>{window.fnUpload=async()=>{throw new Error('Transkript uchun GROQ_API_KEY sozlanmagan.')}}"); pg.click('#app >> text="🎙 O‘qishni boshlash"'); pg.wait_for_timeout(60); pg.click('#app >> text="⏹ Tugatish"'); pg.clock.run_for(50); pg.wait_for_timeout(300)
    chk('a server error (e.g. missing Groq key) is shown on the card', 'GROQ_API_KEY' in pg.inner_text('#app'))
    ev("()=>{navigator.mediaDevices.getUserMedia=async()=>{throw new Error('denied')}}"); pg.click('#app >> text="🎙 O‘qishni boshlash"'); pg.wait_for_timeout(100); chk('a denied microphone gives a helpful message', 'Mikrofonga ruxsat' in pg.inner_text('body'))
