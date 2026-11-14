#!/usr/bin/env python3
"""
Builds data/quran-mushaf.json (15-line Madinah Mushaf layout) from the per-word line data.

Source (not stored in this repo): github.com/zonetecde/mushaf-layout  ->  src/data/mushaf-layout/page-N.json
and src/data/surahs.json  (data derived from King Fahd Glorious Quran Printing Complex / QUL).
Usage:  python3 build_quran.py <path-to-mushaf-layout-main/src/data> <out.json>

The Quran text is copied word-for-word and never edited. Only layout (which line a word sits on)
and the surah banner / basmala rows are added.
"""
import json, re, sys, glob, os
src = sys.argv[1]; out = sys.argv[2]
MARK = re.compile(r'^[\u0660-\u0669]+$')
sur = json.load(open(os.path.join(src, 'surahs.json'), encoding='utf-8'))
pages = {}
for f in glob.glob(os.path.join(src, 'mushaf-layout', 'page-*.json')):
    d = json.load(open(f, encoding='utf-8')); pages[d['pageId']] = d
assert sorted(pages) == list(range(1, 605)), 'need pages 1..604'

# Corrections of the only 3 word-level errors found by cross-checking (each confirmed by TWO independent sources:
# the verse-level text of the same dataset and the independent Quran text of the 'quran-cloud' package).
FIX = {
    # 5:52  a stray space was inside one word:  دَآئِرَ ةٌۭ  ->  دَآئِرَةٌۭ
    5052:  (lambda w: ' \u0629' in w, lambda w: w.replace(' \u0629', '\u0629')),
    # 11:13 wrong spelling "iftaraahu" (alif + alif)  ->  ٱفْتَرَىٰهُ  (alif-wasla ... alif-maqsura + small alif)
    11013: (lambda w: w == 'افْتَرَاهُ ۖ', lambda w: 'ٱفْتَرَىٰهُ ۖ'),
    # 80:25 hamza missing on the first letter: اَنَّا -> أَنَّا
    80025: (lambda w: w.startswith('\u0627\u064e'), lambda w: '\u0623' + w[1:]),
}
fixed = set()
OUT = [None]; sp = {}; vp = {}; bsm = None
nwords = 0
for n in range(1, 605):
    d = pages[n]; L = {}; starts = []
    for v in d['verses']:
        s, a = v['surahNumber'], v['verseNumber']
        key = s * 1000 + a
        if a == 1: starts.append((s, v['words'][0]['lineNumber']))
        vp.setdefault(key, n)
        for w in v['words']:
            tx = w['text']
            if key in FIX and FIX[key][0](tx): tx = FIX[key][1](tx); fixed.add(key)
            L.setdefault(w['lineNumber'], []).append((tx, key)); nwords += 1
        if key == 1001 and bsm is None:
            bsm = [w['text'] for w in v['words'] if not MARK.match(w['text'])][:4]
    slot = {}; top = None
    for s, l1 in starts:
        if s in (1, 9): hl, bl = l1 - 1, None
        else: hl, bl = l1 - 2, l1 - 1
        if bl is not None:
            assert bl >= 1 and bl not in L, (n, s, 'basmala slot taken')
            slot[bl] = ['b']
        if hl >= 1:
            assert hl not in L and hl not in slot, (n, s, 'header slot taken')
            slot[hl] = ['h', s]
        else:
            assert top is None; top = s          # banner sits above the grid (line 1 holds the basmala)
    rows = []
    for ln in range(1, 16):
        if ln in L:
            ws = [t for t, _ in L[ln]]; runs = []
            for _, k in L[ln]:
                if runs and runs[-1][0] == k: runs[-1][1] += 1
                else: runs.append([k, 1])
            rows.append(['x', ws, runs])
        elif ln in slot: rows.append(slot[ln])
        else: rows.append(['e'])
    page = {'r': rows}
    if top: page['t'] = top
    if n in (1, 2):                                   # 8-line pages: keep only the used lines, centred by the reader
        while rows and rows[0] == ['e']: rows.pop(0)
        while rows and rows[-1] == ['e']: rows.pop()
        page['c'] = 1
    OUT.append(page)
    names_sp = [s for s, _ in starts]
    for s in names_sp: sp[s] = n
assert fixed == set(FIX), ('corrections not applied', set(FIX) - fixed)
vlist = [vp[s * 1000 + a] for s in range(1, 115) for a in range(1, sur[s - 1]['totalAyah'] + 1)]
JUZ = [(1,1),(2,142),(2,253),(3,93),(4,24),(4,148),(5,82),(6,111),(7,88),(8,41),(9,93),(11,6),(12,53),(15,1),(17,1),
       (18,75),(21,1),(23,1),(25,21),(27,56),(29,46),(33,31),(36,28),(39,32),(41,47),(46,1),(51,31),(58,1),(67,1),(78,1)]
jp = [vp[s * 1000 + a] for s, a in JUZ]
data = {'v': 1, 'jp': jp,
        'names': [x['arabic'] for x in sur], 'hd': [x['arabicLong'] for x in sur],
        'cnt': [x['totalAyah'] for x in sur], 'bsm': bsm,
        'sp': [sp[i] for i in range(1, 115)], 'vp': vlist, 'p': OUT}
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('pages', len(OUT) - 1, '| word entries', nwords, '| verses', len(vlist), '| bytes', os.path.getsize(out))
