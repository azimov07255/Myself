import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# So'z o'yinlari va matnni audioga moslash. Soat: 2026-10-31 10:00.
import sys, re, json, random
sys.path.insert(0, ROOT + '/tests')
from _pw import Run, wav
TX = ("Hello and welcome to the show. Today we talk about cities, climate and the way people live in them every single day. It is a big topic! "
      "Many experts say that the plan to reduce flooding in low-lying districts was far too expensive, although residents remained reluctant to accept higher taxes. In 2023, almost twelve percent of homes were affected. Thank you for listening.")
def words_of(text): return re.findall(r"[A-Za-z0-9’']+", text)
def whisper(tokens, start=0.0, step=0.3, gap=0.0):
    t, W = start, []
    for w in tokens: W.append([w, round(t, 2), round(t + step - 0.05, 2)]); t += step
    cues = [{'s': W[i][1], 'e': W[min(i + 9, len(W) - 1)][2], 't': ' '.join(x[0] for x in W[i:i + 10]), 'w': W[i:i + 10]} for i in range(0, len(W), 10)]
    return cues, round(t, 2)
WORDS = [('mitigate', 'yumshatmoq'), ('scheme', 'reja'), ('reluctant', 'istamaydigan'), ('drainage', 'drenaj'), ('expensive', 'qimmat'), ('argue', 'bahslashmoq'), ('district', 'tuman'), ('avoid', 'qochmoq'), ('tax', 'soliq'), ('climate', 'iqlim')]
with Run('oyn') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    def setup(n=10, boxes=None):
        ev("""(a)=>{S.ie.words=a[0].slice(0,a[1]).map((w,i)=>({id:i+1,w:w[0],m:w[1],u:w[1],box:(a[2]||[])[i]!==undefined?a[2][i]:(i<6?0:5),due:'2099-01-01',t:1,k:'w'}));S.ie.gm={};S.ie.gb={};window.__say=[];window.ieSay=t=>window.__say.push(t);tab='e';EV='i';IVW='l';GM=null;rwReset();render()}""", [WORDS, n, boxes])
    setup()
    # ---------- 1. pool and entry card ----------
    chk('the pool needs 4 words with a meaning: 3 words -> none', (setup(3) or True) and ev("gmPool(4)") is None); setup()
    ev("S.ie.words.push({id:50,w:'If the council had acted',m:'x',u:'x',k:'g',box:0,due:'2099-01-01',t:1},{id:51,w:'nomeaning',m:'',box:0,due:'2099-01-01',t:1})")
    ids = set(); [ids.update(w['id'] for w in ev("gmPool(4)")) for _ in range(30)]
    chk('grammar items and words without a meaning are never used; the weakest words (lowest box) are preferred', ids <= {1, 2, 3, 4, 5, 6}, ids)
    ev("render()"); t = pg.inner_text('#app'); chk('the vocabulary screen shows "🎮 So‘z o‘yinlari" with three games and their best results', '🎮 So‘z o‘yinlari' in t and 'Juftlashtirish' in t and 'Imlo' in t and 'Tezkor test' in t and 'eng yaxshi: —' in t)
    setup(3); ev("render()"); pg.click('#app .gmb >> nth=0'); pg.wait_for_timeout(100); chk('with fewer than 4 words a game does not start; the user is told what is needed', ev("GM") is None and 'kamida 4 ta' in pg.inner_text('body') and 'kamida 4 ta' in pg.inner_text('#app')); setup()
    # ---------- 2. matching ----------
    ev("gmStart('match')"); pg.wait_for_timeout(100)
    chk('the match game shows 6 words on the left and their 6 meanings on the right (shuffled)', ev("GM.items.length") == 6 and ev("document.querySelectorAll('.gmc > div')[0].children.length") == 6 and ev("document.querySelectorAll('.gmc > div')[1].children.length") == 6 and 'Juftlashtirish' in pg.inner_text('#app'))
    ids = ev("GM.items.map(w=>w.id)")
    ev("gmPick('l',%d)" % ids[0]); ev("gmPick('r',%d)" % ids[1]); chk('a wrong pair adds a mistake and clears the selection', ev("GM.bad") == 1 and ev("GM.sel") is None and not ev("GM.done[%d]" % ids[0]))
    ev("gmPick('l',%d)" % ids[0]); ev("gmPick('l',%d)" % ids[2]); chk('picking two words on the same side just moves the selection', ev("GM.sel.id") == ids[2] and ev("GM.bad") == 1)
    ev("gmPick('r',%d)" % ids[2]); chk('a right pair is matched and its buttons turn green and disabled', ev("GM.done[%d]" % ids[2]) == 1 and ev("document.querySelectorAll('.gmb.ok:disabled').length") == 2)
    ev("gmPick('l',%d)" % ids[2]); chk('a matched word cannot be picked again', ev("GM.sel") is None)
    ev("gmPick('r',%d)" % ids[3]); ev("gmPick('l',%d)" % ids[3]); chk('you can start from the meaning side as well', ev("GM.done[%d]" % ids[3]) == 1)
    xp0 = ev("dayPts(dk()).t"); R.at(2026, 10, 31, 10, 5, 0)
    ev("()=>{GM.t0=Date.now()}"); R.at(2026, 10, 31, 10, 5, 12)
    for i in (ids[0], ids[1], ids[4], ids[5]): ev("gmPick('l',%d)" % i); ev("gmPick('r',%d)" % i)
    chk('finishing shows the time and the mistakes, saves the best time and marks today as "played"', ev("GM.end") == 1 and 11500 <= ev("GM.ms") <= 13500 and 'soniya' in pg.inner_text('#app') and '1 ta xato' in pg.inner_text('#app') and ev("S.ie.gb.match") == ev("GM.ms") and ev("S.ie.gm[dk()]") == 1)
    chk('the first result is a record ("🏆 yangi rekord")', '🏆 yangi rekord' in pg.inner_text('#app'))
    chk('playing earns +5 XP for the day', ev("dayPts(dk()).t") - xp0 == 5, (xp0, ev("dayPts(dk()).t")))
    def play_match(secs):
        ev("gmStart('match')"); ids = ev("GM.items.map(w=>w.id)"); R.at(2026, 10, 31, 11, 0, 0); ev("()=>{GM.t0=Date.now()}"); R.at(2026, 10, 31, 11, 0, secs)
        for i in ids: ev("gmPick('l',%d)" % i); ev("gmPick('r',%d)" % i)
        return ev("[GM.nb,GM.ms,S.ie.gb.match]")
    s = play_match(30); chk('a slower second game is not a record; the best time stays', s[0] == 0 and s[2] < s[1])
    s = play_match(5); chk('a faster game is a new record and replaces the best time', s[0] == 1 and s[2] == s[1] and s[1] < 6500)
    chk('a second and third game on the same day do not give more XP', ev("dayPts(dk()).t") - xp0 == 5 and ev("S.ie.gm[dk()]") == 3)
    # ---------- 3. spelling ----------
    ev("gmStart('spell')"); pg.wait_for_timeout(100); w = ev("GM.items[0]")
    t = pg.inner_text('#app'); chk('spelling: shows the meaning, a 🔊 button and a hint button (8 rounds)', w['u'] in t and '🔊 Eshit' in t and '💡 Ishora' in t and '1 / 8' in t and ev("GM.items.length") == 8)
    ev("window.__say=[]"); pg.click('#app >> text=Eshit'); chk('🔊 speaks the English word with the chosen accent', ev("__say") == [w['w']])
    pg.click('#app >> text=Ishora'); chk('the hint shows the first letter and the length', '%s' % w['w'][0] in pg.inner_text('#app') and '(%d harf)' % len(w['w']) in pg.inner_text('#app'))
    pg.fill('#gmi', '  ' + w['w'].upper() + ' '); pg.click('#app >> text=Tekshirish'); pg.wait_for_timeout(80); chk('capitals and spaces are ignored: the answer counts as correct', ev("GM.sc") == 1 and 'To‘g‘ri' in pg.inner_text('#app'))
    pg.click('#app >> text=Keyingisi'); w2 = ev("GM.items[1]"); pg.fill('#gmi', w2['w'][:-1] + 'x'); pg.click('#app >> text=Tekshirish'); pg.wait_for_timeout(80)
    chk('a misspelling is wrong: the correct spelling is shown and the word is remembered as a mistake', ev("GM.sc") == 1 and w2['w'] in pg.inner_text('#app') and ev("GM.wrong") == [w2['id']] and '✗' in pg.inner_text('#app'))
    for _ in range(6): ev("gmSpellNext()"); ev("()=>{GM.ans=GM.items[GM.i].w;gmSpellCheck()}")
    ev("gmSpellNext()"); t = pg.inner_text('#app'); chk('the result screen shows the score and the wrong words with a "🔁 Takrorga" button', ev("GM.end") == 1 and '7 / 8' in t and w2['w'] in t and '🔁 Takrorga' in t, t[:200])
    ev("S.ie.words.find(x=>x.id==%d).due='2099-01-01'" % w2['id']); pg.click('#app >> text=Takrorga'); chk('"Takrorga" puts the word into today\u2019s vocabulary review', ev("S.ie.words.find(x=>x.id==%d).due" % w2['id']) == ev("dk()"))
    chk('the best spelling score is saved', ev("S.ie.gb.spell") == 7)
    # ---------- 4. speed quiz ----------
    R.at(2026, 10, 31, 12, 0, 0); ev("gmStart('speed')"); pg.wait_for_timeout(100)
    chk('the speed quiz starts a timer and shows a meaning with 4 different options (one is right)', ev("GMT") != 0 and ev("GM.q.opts.length") == 4 and len(set(o['id'] for o in ev("GM.q.opts"))) == 4 and any(o['id'] == ev("GM.q.w.id") for o in ev("GM.q.opts")) and '60 s' in pg.inner_text('#gmt'))
    right = lambda: ev("GM.q.opts.findIndex(o=>o.id===GM.q.w.id)"); wrong = lambda: ev("GM.q.opts.findIndex(o=>o.id!==GM.q.w.id)")
    ev("gmSpAns(%d)" % right()); chk('a right answer: score and streak go up, the right button is green', ev("GM.sc") == 1 and ev("GM.streak") == 1 and ev("GM.best") == 1 and ev("document.querySelectorAll('.gmb.ok').length") == 1)
    ev("gmSpAns(%d)" % wrong()); chk('answering twice on the same question is ignored', ev("GM.sc") == 1 and ev("GM.bad") == 0)
    ev("gmSpNext()"); ev("gmSpAns(%d)" % right()); ev("gmSpNext()"); ev("gmSpAns(%d)" % wrong())
    chk('a wrong answer resets the streak, counts a mistake, shows the wrong button red and remembers the word', ev("GM.bad") == 1 and ev("GM.streak") == 0 and ev("GM.best") == 2 and len(ev("GM.wrong")) == 1 and ev("document.querySelectorAll('.gmb.gmw').length") == 1)
    R.at(2026, 10, 31, 12, 1, 5); ev("gmSpTick()"); pg.wait_for_timeout(100)
    chk('after 60 seconds the game ends by itself: the timer stops, the result and the longest streak are shown', ev("GM.end") == 1 and ev("GMT") == 0 and '2 ta to‘g‘ri' in pg.inner_text('#app') and 'Eng uzun ketma-ketlik: 2' in pg.inner_text('#app'))
    ev("gmSpAns(0)"); chk('answers after the end are ignored', ev("GM.sc") == 2)
    chk('the best speed score is saved and a new best is flagged the first time', ev("S.ie.gb.speed") == 2 and '🏆 yangi rekord' in pg.inner_text('#app'))
    pg.click('#app >> text=← Lug‘at'); pg.wait_for_timeout(100); chk('"← Lug‘at" leaves the game: the timer is cleared and the vocabulary screen is back', ev("GM") is None and ev("GMT") == 0 and '🎮 So‘z o‘yinlari' in pg.inner_text('#app'))
    # ---------- 5. alignment: the algorithm ----------
    tok = words_of(TX); C, dur = whisper(tok, 0.5)
    al = lambda text, cues, d: ev("(x)=>{const r=ieAlignTx(x[0],x[1],x[2]);return r.err?r:{ratio:r.ratio,n:r.n,cues:r.cues}}", [text, cues, d])
    r = al(TX, C, dur)
    chk('a perfect audio transcript matches every word (100%)', abs(r['ratio'] - 1) < 1e-9 and r['n'] == len(tok))
    chk('the original text is kept exactly: the cues together read like the text (only whitespace differs)', ' '.join(c[2] for c in r['cues']) == re.sub(r'\s+', ' ', TX).strip(), [c[2] for c in r['cues']])
    chk('each cue has one start time per word, in order, and cue times never go backwards', all(len(c[3]) == len(words_of(c[2])) for c in r['cues']) and all(r['cues'][i][0] <= r['cues'][i + 1][0] for i in range(len(r['cues']) - 1)) and all(c[1] > c[0] for c in r['cues']))
    first = next(w for w in sum((c['w'] for c in C), []) if w[0] == 'Hello'); chk('word start times come from the audio ("Hello" starts at its Whisper time)', r['cues'][0][3][0] == first[1] and r['cues'][0][0] == first[1])
    chk('short sentences are merged into the next cue (every cue has 4+ words except possibly the last)', all(len(words_of(c[2])) >= 4 for c in r['cues'][:-1]), [len(words_of(c[2])) for c in r['cues']])
    rnd = random.Random(7); noisy = [w for w in tok if rnd.random() > 0.08]; noisy = ['expensiv' if w == 'expensive' else '12' if w == 'twelve' else w for w in noisy]; noisy = noisy[:20] + ['uh', 'um'] + noisy[20:]
    Cn, dn = whisper(noisy, 0.5); rn = al(TX, Cn, dn)
    chk('with speech-recognition errors (missing words, a typo, "12" for "twelve", extra "uh um") most words still match (80-97%)', 0.8 <= rn['ratio'] <= 0.97, rn['ratio'])
    ts = [x for c in rn['cues'] for x in c[3]]; chk('unmatched words get times between their neighbours: all times in order and inside the audio', all(ts[i] <= ts[i + 1] for i in range(len(ts) - 1)) and ts[0] >= 0 and ts[-1] <= dn + 1)
    other, do = whisper(words_of("Completely different recording about football matches and the weather forecast for next weekend including some rain and wind across the northern region today"), 0)
    chk('an unrelated audio gives a very low match', al(TX, other, do)['ratio'] < 0.2)
    chk('very short text or audio is refused', 'juda qisqa' in al('Hello there friend.', C, dur).get('err', '') and 'juda qisqa' in al(TX, [{'w': [['a', 0, 1]]}], 3).get('err', ''))
    longs = ' '.join(['word%d' % i for i in range(40)]) + '. Yes. No. Maybe so. Okay then, let us start the lesson properly today.'
    Cl, dl = whisper(words_of(longs), 0); rl = al(longs, Cl, dl)
    chk('a 40-word sentence is split into pieces of at most 26 words, with no word lost', all(len(words_of(c[2])) <= 26 for c in rl['cues']) and ' '.join(c[2] for c in rl['cues']) == longs, [len(words_of(c[2])) for c in rl['cues']])
    chk('the very short sentences "Yes. No. Maybe so." are merged with a neighbour', not any(c[2] in ('Yes.', 'No.') for c in rl['cues']))
    # ---------- 6. alignment: the flow in the app ----------
    AN = {'words': [{'w': 'scheme', 'f': 'scheme', 'pos': 'n', 'lv': 'B2', 'def': 'a plan', 'uz': 'reja', 'ctx': '', 'ex': ''}], 'chunks': [], 'grammar': [], 'lv': 'B2', 'topic': 'x', 'n': 1, 'at': '2026-10-31'}
    def mat(**k):
        m = {'id': 91, 't': 'Pod', 'k': 'p', 'x': TX, 'c': [], 'au': 1, 'd': '2026-10-31', 'an': AN}; m.update(k); return m
    R.put_audio('ieau91', wav()); ev("(m)=>{S.ie.mat=[m];window.__up=[];window.fnUpload=async(f,b,n)=>{window.__up.push([f,b.size,n]);await new Promise(r=>setTimeout(r,200));return window.__resp};IVW='a';render();ieMatOpen(91)}", mat())
    pg.wait_for_function("document.getElementById('ieau')&&document.getElementById('ieau').readyState>=1", timeout=8000)
    t = pg.inner_text('#iem'); chk('a podcast with audio and a plain text (no times) offers "🎯 Matnni audioga moslash" instead of the transcript box', '🎯 Matnni audioga moslash' in t and 'Moslash' in t and 'Avtomatik transkript' not in t and 'yoki audiodan yangi transkript' in t)
    ev("(r)=>{window.__resp=r}", {'cues': C, 'dur': dur}); pg.click('#iem button >> text="Moslash"'); pg.wait_for_timeout(80)
    chk('while aligning the button is disabled and says so; a second click does not send a second request', 'Moslanmoqda' in pg.inner_text('#iem') and ev("document.querySelector('#iem .big').disabled"))
    pg.wait_for_timeout(700); m = ev("S.ie.mat[0]")
    chk('one request to the transcript action with the stored audio file (WAV)', len(ev("__up")) == 1 and ev("__up[0][0]") == {'action': 'transcript'} and ev("__up[0][2]") == 'audio.wav')
    chk('the material now has timed cues with per-word times, its text field is empty, flagged as aligned; the AI analysis is kept', len(m['c']) >= 5 and all(len(c) == 4 for c in m['c']) and m['x'] == '' and m['al'] == 1 and m['an'] is not None)
    chk('the alignment box disappears, the subtitle lines and the dictation buttons appear', '🎯 Matnni audioga moslash' not in pg.inner_text('#iem') and ev("document.querySelectorAll('#iem .iecu').length") == len(m['c']) and ev("document.querySelectorAll('#iem .iecu [aria-label=\"Diktant\"]').length") == len(m['c']))
    ev("(a)=>{const a0=document.getElementById('ieau');a0.currentTime=a[0];ieTU();ieWFAt(a[0])}", [m['c'][0][3][2] + 0.01]); chk('the words now follow the audio: at the 3rd word\u2019s time that word is lit', ev("document.querySelector('#iem .wp').textContent") == 'welcome', ev("[...document.querySelectorAll('#iem .wp')].map(x=>x.textContent)"))
    ev("ieMatClose()")
    # partial / failing
    def fresh(resp, **k):
        ev("(a)=>{S.ie.mat=[a[0]];IAL=null;window.__up=[];window.__resp=a[1];ieMatOpen(91)}", [mat(**k), resp]); pg.wait_for_timeout(500)
    half, dh = whisper([w for i, w in enumerate(tok) if i % 5 < 3], 0.5)   # 60% of the words
    fresh({'cues': half, 'dur': dh}); pg.click('#iem button >> text="Moslash"'); pg.wait_for_timeout(900)
    chk('a partial match (about 60%) is applied with a warning that some places may be inexact', len(ev("S.ie.mat[0].c")) >= 3 and 'noaniq' in pg.inner_text('body') and ev("S.ie.mat[0].x") == '')
    fresh({'cues': other, 'dur': do}); pg.click('#iem button >> text="Moslash"'); pg.wait_for_timeout(900)
    chk('a text that does not belong to the audio (<45%) is refused: nothing changes and the user is told', 'mos kelmadi' in pg.inner_text('#iem') and len(ev("S.ie.mat[0].c")) == 0 and ev("S.ie.mat[0].x") == TX)
    ev("()=>{window.fnUpload=async()=>{throw new Error('Transkript uchun GROQ_API_KEY sozlanmagan.')};IAL=null;ieMatDraw()}"); pg.click('#iem button >> text="Moslash"'); pg.wait_for_timeout(300); chk('a server error is shown on the card and the button works again', 'GROQ_API_KEY' in pg.inner_text('#iem') and not ev("document.querySelector('#iem .big').disabled"))
    ev("()=>{window.fnUpload=async()=>({cues:[],dur:0});IAL=null;ieMatDraw()}"); pg.click('#iem button >> text="Moslash"'); pg.wait_for_timeout(300); chk('an empty answer from the server is reported ("too short")', 'juda qisqa' in pg.inner_text('#iem'))
    ev("ieMatClose()")
    # the card conditions
    def card(**k):
        ev("(m)=>{S.ie.mat=[m];IMT=null;ieMatOpen(m.id)}", mat(**k)); pg.wait_for_timeout(400); return pg.inner_text('#iem')
    t = card(x='', c=[]); chk('audio but NO text -> the transcript box (not the alignment box)', 'Avtomatik transkript' in t and '🎯 Matnni audioga moslash' not in t); ev("ieMatClose()")
    t = card(c=[[0, 3, TX[:40], None]], x=''); chk('a podcast that already has timed lines shows neither box', '🎯 Matnni' not in t and 'Avtomatik transkript' not in t and ev("document.querySelectorAll('#iem .iecu').length") == 1); ev("ieMatClose()")
    t = card(au=0); chk('no audio -> no alignment box', '🎯 Matnni' not in t and 'Avtomatik transkript' not in t); ev("ieMatClose()")
    t = card(x='short text only'); chk('a text under 200 characters is not offered for alignment', '🎯 Matnni' not in t); ev("ieMatClose()")
    ev("(m)=>{S.ie.mat=[m];window.__tr=0;window.ieTranscribe=id=>{window.__tr=id};ieMatOpen(91)}", mat()); pg.wait_for_timeout(400); pg.click('#iem >> text=yoki audiodan yangi transkript'); chk('"yoki audiodan yangi transkript" still lets the user transcribe from the audio instead', ev("__tr") == 91)
