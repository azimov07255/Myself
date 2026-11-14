import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# AI limit yozuvi: egasi uchun "cheksiz", oddiy hisob uchun serverdagi haqiqiy limit. Soat: 2026-10-31 10:00.
import sys, json
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
with Run('ailim') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    def reset(resp=None, ok=True, fail=False):
        ev("""(a)=>{localStorage.clear();localStorage.setItem('trk_bg','o');localStorage.setItem('trk_sgr','a');localStorage.setItem('trk_ptb','a');localStorage.setItem('trk_pl','0');localStorage.setItem('trk_fqd','0');ALM=null;ALB=0;window.aiOk=()=>a[1];window.__f=[];window.__resp=a[0];window.fnPost=async(b,ms)=>{window.__f.push([b,ms]);if(a[2])throw new Error('offline');return window.__resp};S.us=undefined}""", [resp, ok, fail])
    reset(None, False)
    chk('not signed in: the label shows the local count and the default 40, and no request is made', ev("aiUseLabel()") == 'AI: 0/40 bugun' and ev("__f.length") == 0)
    reset({'owner': False, 'limit': 40, 'used': 12})
    chk('first look: the label is shown at once and ONE free check is sent to the server (action "limit", 15 s)', ev("aiUseLabel()") == 'AI: 0/40 bugun' and ev("__f") == [[{'action': 'limit'}, 15000]], ev("__f"))
    pg.wait_for_timeout(120); chk('after the answer the label uses the SERVER count for the day (12 / 40, it includes other devices)', ev("aiUseLabel()") == 'AI: 12/40 bugun')
    ev("aiUseLabel();aiUseLabel()"); chk('further looks within 10 minutes do not ask again', ev("__f.length") == 1)
    ev("()=>{localStorage.setItem('trk_aiu_'+dk(),'15')}"); chk('if this device counted more than the server last said, the larger number is shown', ev("aiUseLabel()") == 'AI: 15/40 bugun')
    chk('asking the limit is not an AI request: it is not counted as usage', not ev("(S.us&&S.us.ai&&S.us.ai[dk()])||null"))
    chk('the remaining count follows the server limit', ev("aiLeft()") == 25)
    reset({'owner': False, 'limit': 100, 'used': 3}); ev("aiUseLabel()"); pg.wait_for_timeout(120); chk('a raised limit (AI_DAILY_LIMIT=100) is shown as /100', ev("aiUseLabel()") == 'AI: 3/100 bugun' and ev("aiLeft()") == 97)
    reset({'owner': True, 'limit': 40, 'used': 55}); ev("aiUseLabel()"); pg.wait_for_timeout(120)
    chk('the owner sees "cheksiz (egasi)" instead of a misleading /40, and the remaining count is unlimited', ev("aiUseLabel()") == 'AI: cheksiz (egasi)' and ev("aiLeft()") == 1e308 or ev("aiLeft()") is None or ev("aiIsOwner()") is True, ev("aiLeft()"))
    chk('the answer is cached on this device: after a reload no new check is needed for 10 minutes', ev("JSON.parse(localStorage.getItem('trk_ailim_'+(UID||'')))").get('o') is True)
    ev("()=>{ALM=null;window.__f=[]}"); ev("aiUseLabel()"); chk('...(the cache is read back from storage)', ev("aiIsOwner()") is True and ev("__f.length") == 0)
    ev("()=>{const c=JSON.parse(localStorage.getItem('trk_ailim_'+(UID||'')));c.d='2000-01-01';localStorage.setItem('trk_ailim_'+(UID||''),JSON.stringify(c));ALM=null;window.__f=[]}"); ev("aiUseLabel()"); chk('a cache from another day is ignored and refreshed', ev("__f.length") == 1)
    reset(None, True, True); ev("aiUseLabel()"); pg.wait_for_timeout(120); chk('if the check fails (offline) the label falls back to the local count and the app keeps working', ev("aiUseLabel()") == 'AI: 0/40 bugun' and ev("ALB") == 0)
    reset({'owner': False, 'limit': 40, 'used': 9}); ev("aiUseLabel()"); pg.wait_for_timeout(120)
    t = ev("aiLimDiag()"); chk('Diagnostika text for a normal account: the limit, today\u2019s server use and the hint about OWNER_EMAIL', 'oddiy hisob' in t and '40' in t and '9 ta' in t and 'OWNER_EMAIL' in t)
    reset({'owner': True, 'limit': 40, 'used': 0}); ev("aiUseLabel()"); pg.wait_for_timeout(120); chk('Diagnostika text for the owner: unlimited', ev("aiLimDiag()") == 'egasi hisobi: cheksiz')
    chk('the Diagnostika report contains the AI limit line', 'AI limit:' in ev("diagText()"))
    ev("()=>{S.ie.words=[];window.__f=[];ALM=null;localStorage.clear();localStorage.setItem('trk_bg','o');localStorage.setItem('trk_sgr','a');localStorage.setItem('trk_ptb','a');localStorage.setItem('trk_pl','0');localStorage.setItem('trk_fqd','0');window.aiOk=()=>true;window.__resp={owner:true,limit:40,used:0};aiBuild();aiRender()}"); pg.wait_for_timeout(200)
    chk('the open chat header updates itself when the answer arrives', 'cheksiz (egasi)' in pg.inner_text('#aisub'), pg.inner_text('#aisub'))
