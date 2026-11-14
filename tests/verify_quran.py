#!/usr/bin/env python3
"""Integrity checks for data/quran-mushaf.json (the Quran must never be silently damaged)."""
import json, re, sys, os, unicodedata
here = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(here, '..', 'data', 'quran-mushaf.json'), encoding='utf-8'))
REF = json.load(open(os.path.join(here, 'data', 'quran_ref_skeleton.json'), encoding='utf-8'))
STD = [7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,110,98,135,112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,83,182,88,75,85,54,53,89,59,37,35,38,29,18,45,60,49,62,55,78,96,29,22,24,13,14,11,11,18,12,12,30,52,52,44,28,28,20,56,40,31,50,40,46,42,29,19,36,25,22,17,19,26,30,20,15,21,11,8,8,19,5,8,8,11,11,8,3,9,5,4,7,3,6,3,5,4,5,6]
MARK = re.compile(r'^[\u0660-\u0669]+$'); ok = bad = 0
def chk(name, cond, extra=''):
    global ok, bad
    if cond: ok += 1; print('PASS', name)
    else: bad += 1; print('FAIL', name, extra)
def ar(n): return ''.join(chr(0x660 + int(c)) for c in str(n))
def sk(t):
    t = t.replace('\u2009','').replace('ٱ','ا').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ى','ي').replace('ی','ي').replace('ک','ك')
    t = t.replace('ئ','ي').replace('ؤ','و').replace('ء','')
    o = []
    for ch in t:
        c = ord(ch)
        if unicodedata.category(ch)[0]=='M' or c==0x640 or 0x6D6<=c<=0x6ED or 0x610<=c<=0x61A or 0x64B<=c<=0x65F or c==0x670 or ch==' ' or 0x660<=c<=0x669 or ch in '۞۩\u200f': continue
        o.append(ch)
    return ''.join(o)
P = D['p']
chk('604 pages', len(P) == 605 and P[0] is None)
chk('pages 1-2 have 8 lines, others 15', all(len(P[n]['r']) == (8 if n in (1,2) else 15) for n in range(1, 605)),
    [n for n in range(1,605) if len(P[n]['r']) != (8 if n in (1,2) else 15)][:5])
chk('verse counts per surah = standard table', D['cnt'] == STD and sum(STD) == 6236 and len(D['vp']) == 6236)
words = []; verse_words = {}; order = []
for n in range(1, 605):
    for r in P[n]['r']:
        if r[0] != 'x': continue
        chk_runs = sum(c for _, c in r[2]) == len(r[1])
        if not chk_runs: chk('row runs match word count (page %d)' % n, False)
        i = 0
        for k, c in r[2]:
            for w in r[1][i:i+c]: words.append((k, w)); verse_words.setdefault(k, []).append(w)
            if not order or order[-1] != k: order.append(k)
            i += c
chk('every verse key present exactly once in reading order', order == [s*1000+a for s in range(1,115) for a in range(1,STD[s-1]+1)])
nonmark = [w for _, w in words if not MARK.match(w)]
chk('77,429 words (standard Hafs count) + 6,236 verse numbers', len(nonmark) == 77429 and len(words) - len(nonmark) == 6236, (len(nonmark), len(words)))
chk('each verse ends with its own Arabic-Indic number', all(verse_words[k][-1] == ar(k % 1000) and not any(MARK.match(w) for w in verse_words[k][:-1]) for k in verse_words))
HZ = set('ءأإؤئ\u0654\u0655')
jt = lambda k: ' '.join(w for w in verse_words[k] if not MARK.match(w))
mism = [k for k in verse_words if sk(jt(k)) != REF['%d:%d' % divmod(k, 1000)][0]]
chk('letter skeleton of all 6,236 verses = independent source', not mism, mism[:5])
hz = [k for k in verse_words if sum(1 for c in jt(k) if c in HZ) != REF['%d:%d' % divmod(k, 1000)][1]]
chk('number of hamza signs in every verse = independent source', not hz, hz[:5])
chk('5:52: no stray space inside the word dairatun', not any(' \u0629' in w for w in verse_words[5052]) and any(w.startswith('دَ') and w.endswith(' ۚ') and 'ةٌ' in w for w in verse_words[5052]))
chk('11:13 reads iftaraahu (alif-wasla ... alif-maqsura)', verse_words[11013][2].startswith('\u0671') and '\u0649' in verse_words[11013][2])
chk('80:25 starts with hamza on alif', verse_words[80025][0][0] == '\u0623')
# banners / basmala
hdr = {}; bsm = 0; tops = {}
for n in range(1, 605):
    p = P[n]
    if 't' in p: tops[p['t']] = n
    for i, r in enumerate(p['r']):
        if r[0] == 'h': hdr.setdefault(r[1], []).append(n)
        if r[0] == 'b': bsm += 1
for s, n in tops.items(): hdr.setdefault(s, []).append(n)
chk('every surah has exactly one banner', sorted(hdr) == list(range(1, 115)) and all(len(v) == 1 for v in hdr.values()), [s for s in range(1,115) if len(hdr.get(s,[])) != 1])
chk('112 basmala rows (all surahs except Al-Fatihah and At-Tawbah)', bsm == 112, bsm)
chk('banner is on the same page as the surah start', all(hdr[s][0] == D['sp'][s-1] for s in range(1, 115)))
chk('start page of surah = page of its first verse', all(D['vp'][sum(STD[:s-1])] == D['sp'][s-1] for s in range(1, 115)))
chk('juz start pages are the standard 30', D['jp'] == [1,22,42,62,82,102,121,142,162,182,201,222,242,262,282,302,322,342,362,382,402,422,442,462,482,502,522,542,562,582])
chk('reading order never goes backwards across pages', all(D['vp'][i] <= D['vp'][i+1] for i in range(6235)))
# anchors taken from the real printed mushaf (user's screenshot of page 3)
r3 = [r for r in P[3]['r'] if r[0] == 'x']
chk('page 3 = Al-Baqarah 6-16 on 15 text lines (as in the printed page)', len(r3) == 15 and r3[0][2][0][0] == 2006)
chk('page 3 line 1 starts "inna alladhina kafaru sawaaon", line 15 ends "muhtadin 16"', [sk(w) for w in r3[0][1][:4]] == ['ان','الذين','كفروا','سوا'] and r3[14][1][-1] == '١٦' and sk(r3[14][1][-2]) == 'مهتدين')
chk('page 3 line 2 begins with the end of verse 5-6 as printed', r3[1][1][0] == 'لَا' and sk(r3[1][1][1]) == 'يومنون' and r3[1][1][2] == '٦')
chk('last page ends at An-Nas 6', order[-1] == 114006 and P[604]['r'][-1][0] in ('x','e'))
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
