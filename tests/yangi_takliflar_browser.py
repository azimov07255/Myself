import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Lug'at qidiruvida avtomatik to'ldirish: harflarga mos so'zlar ketma-ket chiqadi. Soat: 2026-11-03 10:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
WORDS = open((ROOT + '/data/words-v1.txt'), encoding='utf-8').read()
with Run('takliflar', when=(2026, 11, 3, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""(txt)=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);window.aiOk=()=>true;window.__nf=0;window.__fp=[];
      const of=window.fetch;window.fetch=async(u,o)=>{if(String(u).includes('data/words-v1.txt')){__nf++;if(window.__nofile)return new Response('',{status:404});return new Response(txt,{status:200})}return of(u,o)};
      window.fnPost=async b=>{__fp.push(b);return {nf:true}};window.fnAI=async b=>({text:JSON.stringify({w:b.word,lv:'B2',uz:['x'],defs:[],pos:['noun']})});
      localStorage.removeItem('trk_dqh');DQW=null;DQWP=null;DQC={};S.ie.words=[{id:1,w:'supplement',m:'qo‘shimcha',u:'qo‘shimcha',k:'w',lv:'C1',box:0,due:dk(),t:0},{id:2,w:'Past perfect',k:'g',m:'x',box:0,due:dk(),t:0}];tab='e';EV='i';IVW='l';render()}""", WORDS)
    sg = lambda: ev("[...document.querySelectorAll('#dqsg button')].map(b=>b.textContent.replace(/\\s+/g,' ').trim())")
    pg.click('#dqi'); pg.type('#dqi', 's', delay=30); pg.wait_for_timeout(250); a = sg()
    chk('typing one letter already shows suggestions starting with it (at most 8), the most common words first', 1 <= len(a) <= 8 and all(x.startswith('s') for x in a) and any(x.startswith('so') or x.startswith('s') for x in a), a)
    pg.type('#dqi', 'up', delay=40); pg.wait_for_timeout(250); b = sg()
    chk('each further letter narrows the list: "sup" gives words starting with sup, e.g. "support", with the typed part in bold', len(b) >= 4 and all(x.split(' ')[0].startswith('sup') for x in b) and any(x.startswith('support') for x in b) and ev("document.querySelector('#dqsg button b').textContent") == 'sup', b)
    chk('words from your own vocabulary come first with the "📚 lug‘atingda" label (grammar items are not suggested)', 'supplement' in b[0] and '📚 lug‘atingda' in b[0], b[:3])
    pg.type('#dqi', 'po', delay=40); pg.wait_for_timeout(250); c = sg(); chk('"suppo" → support, supporter, supportive…', len(c) >= 3 and all(x.startswith('suppo') for x in c) and c[0].startswith('support'), c)
    chk('the word list is downloaded only once while typing', ev("__nf") == 1)
    pg.keyboard.press('ArrowDown'); pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(80); chk('arrow keys move the highlight', ev("[...document.querySelectorAll('#dqsg button')].findIndex(b=>b.classList.contains('on'))") == 1)
    pg.keyboard.press('ArrowUp'); pg.keyboard.press('ArrowUp'); pg.keyboard.press('ArrowUp'); pg.wait_for_timeout(50); chk('...and can go back to "nothing selected"', ev("document.querySelectorAll('#dqsg button.on').length") == 0)
    pg.keyboard.press('ArrowDown'); pg.keyboard.press('Enter'); pg.wait_for_timeout(500)
    chk('Enter on a highlighted suggestion searches exactly that word', ev("DQ.q") == c[0].split(' ')[0] and any(f.get('word') == c[0].split(' ')[0] for f in ev("__fp")), ev("DQ.q"))
    chk('after the search the suggestion list is gone', ev("document.querySelectorAll('#dqsg button').length") == 0)
    ev("()=>{DQ.e=null;DQ.q='';__fp=[];render()}"); pg.click('#dqi'); pg.type('#dqi', 'abund', delay=30); pg.wait_for_timeout(250); d = sg(); pg.click('#dqsg button >> nth=0'); pg.wait_for_timeout(500)
    chk('tapping a suggestion searches it at once (no need to press "Qidir")', ev("DQ.q") == d[0].split(' ')[0] and len(ev("__fp")) == 1, d)
    ev("()=>{DQ.e=null;DQ.q='';render()}"); pg.click('#dqi'); pg.type('#dqi', 'xyzq', delay=30); pg.wait_for_timeout(250); chk('letters that start no word give an empty list without errors', sg() == [])
    pg.fill('#dqi', ''); pg.type('#dqi', '1', delay=20); pg.wait_for_timeout(150); chk('digits and symbols give no suggestions', sg() == [])
    pg.fill('#dqi', 'sup'); pg.dispatch_event('#dqi', 'input'); pg.wait_for_timeout(200); pg.fill('#dqi', ''); pg.dispatch_event('#dqi', 'input'); pg.wait_for_timeout(150); chk('clearing the box clears the list', sg() == [])
    # tarix
    ev("()=>{localStorage.setItem('trk_dqh',JSON.stringify(['take for granted','take off']));DQ.e=null;render()}"); pg.click('#dqi'); pg.type('#dqi', 'take f', delay=30); pg.wait_for_timeout(250); h = sg()
    chk('a phrase being typed is completed from previous searches ("🕘 oldingi")', len(h) == 1 and h[0].startswith('take for granted') and '🕘' in h[0], h)
    ev("()=>{DQ.e=null;render()}"); pg.click('#dqi'); pg.type('#dqi', 'Supp', delay=30); pg.wait_for_timeout(250); chk('capital letters are fine', len(sg()) >= 3)
    # to'liq fayl yuklanmasa ham ichki ro'yxat ishlaydi
    ev("()=>{window.__nofile=1;DQW=null;DQWP=null;DQ.e=null;render()}"); pg.click('#dqi'); pg.type('#dqi', 'supp', delay=30); pg.wait_for_timeout(300); e = sg()
    chk('if the optional full word file is missing, the built-in list still completes words (your own word first, then support, supply…)', len(e) >= 4 and e[0].startswith('supplement') and any(x.startswith('support') for x in e) and all(x.split(' ')[0].startswith('supp') for x in e), e)
    ev("()=>{window.__nofile=0}")
    # ikkala uslubda ko'rinish
    ev("()=>{DQW=null;DQWP=null;DQ.e=null;render()}"); pg.click('#dqi'); pg.type('#dqi', 'supp', delay=30); pg.wait_for_timeout(300)
    bad = []
    for ui in ('1', '2'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1]}", [ui, th]); pg.wait_for_timeout(60)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('the list does not overflow the screen in Klassik and Yangi, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
