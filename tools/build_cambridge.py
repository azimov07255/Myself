#!/usr/bin/env python3
"""Cambridge Thematic IELTS Reading Words PDF -> ixcham cambridge-sozlar.json (faqat SHAXSIY foydalanish uchun; GitHub'ga YUKLAMANG).
Ishlatish: python3 tools/build_cambridge.py <pdf> <chiqish.json>
Format: {"v":1,"src":"...","p":[{"i":1,"t":"Manatees","s":"Cambridge IELTS Academic 20","ts":[1,21]}],"w":[[passageIdx,test,no,word,pos,def,uz,example]]}"""
import sys, re, json, collections, subprocess, pdfplumber
pdf_path = sys.argv[1]; out = sys.argv[2]
cl = lambda s: re.sub(r'\s+', ' ', (s or '').replace('-\n', '-').replace('\n', ' ')).strip()
P = []; words = []; warn = []
TXT = subprocess.run(['pdftotext', '-layout', pdf_path, '-'], capture_output=True).stdout.decode('utf-8', 'replace').split('\f')
with pdfplumber.open(pdf_path) as pdf:
    N = len(pdf.pages)
    first_test = None
    # 1) mazmun (birinchi "TEST 1" sahifasigacha)
    for pn in range(1, N):
        tx = TXT[pn] if pn < len(TXT) else ''
        if re.search(r'^\s*TEST\s+1\b', tx, re.M) and 'Word' in tx: first_test = pn; break
        for tb in pdf.pages[pn].extract_tables():
            for r in tb:
                c = [cl(x) for x in r if x and cl(x)]
                if len(c) >= 4 and re.fullmatch(r'\d{1,3}', c[0]) and re.fullmatch(r'[\d, ]+', c[2] if len(c) > 2 else ''):
                    P.append({'no': int(c[0]), 't': c[1], 'ts': [int(x) for x in re.findall(r'\d+', c[2])], 's': ' '.join(c[3:])})
    # 2) so'zlar (bir sahifada bir nechta "TEST n" sarlavhasi bo'lishi mumkin: jadval o'zidan oldingi eng yaqin sarlavhaga tegishli)
    cur = None; same = {}
    for pn in range(first_test, N):
        pg = pdf.pages[pn]; tx = TXT[pn] if pn < len(TXT) else ''
        for m in re.finditer(r'TEST\s+(\d+)\s*\n\s*The text is exactly the same as the text in Test\s+(\d+)', tx): same[int(m.group(1))] = int(m.group(2))
        W = pg.extract_words(); heads = []
        for i, w in enumerate(W[:-1]):
            if w['text'] == 'TEST' and re.fullmatch(r'\d+', W[i + 1]['text']): heads.append((w['top'], int(W[i + 1]['text'])))
        if not heads:
            m = re.search(r'^\s*TEST\s+(\d+)\b', tx, re.M)
            if m: cur = int(m.group(1))
        for tbl in pg.find_tables():
            top = tbl.bbox[1]; tt = cur
            for hy, hn in heads:
                if hy <= top + 2: tt = hn
            if tt is None: continue
            for r in tbl.extract():
                c = [cl(x) for x in r if x and cl(x)]
                if not c or not re.fullmatch(r'\d{1,3}', c[0] or ''): continue
                if len(c) < 4: warn.append((pn + 1, 'qisqa qator', c)); continue
                no = int(c[0]); w = c[1]; d = c[2]; u = c[3]; e = c[4] if len(c) > 4 else ''
                pos = ''
                mm = re.match(r'^(.*?)\s*\(([A-Za-z\- ]{2,22})\)\s*$', w)
                if mm: w, pos = mm.group(1).strip(), mm.group(2).strip().lower()
                if not w: warn.append((pn + 1, "bo'sh so'z", c)); continue
                words.append({'test': tt, 'no': no, 'w': w, 'pos': pos, 'd': d, 'u': u, 'e': e})
        if heads: cur = heads[-1][1]
        try: pg.flush_cache()
        except Exception: pass
# maqolalarni tartiblab, test -> maqola xaritasi
P.sort(key=lambda x: x['no'])
t2p = {}
for i, p in enumerate(P):
    p['i'] = i + 1
    for t in p['ts']: t2p.setdefault(t, i + 1)
tests = sorted({w['test'] for w in words})
missing_map = [t for t in tests if t not in t2p]
# xaritasiz testlar uchun alohida "maqola" yaratamiz
extra = {}
for t in missing_map:
    P.append({'no': 9000 + t, 't': 'Test %d (maqola nomi mazmunda topilmadi)' % t, 'ts': [t], 's': '', 'i': len(P) + 1}); t2p[t] = len(P)
rows = [[t2p[w['test']], w['test'], w['no'], w['w'], w['pos'], w['d'], w['u'], w['e']] for w in words]
data = {'v': 1, 'src': 'Cambridge Thematic IELTS Reading Words (1-225 tests)', 'p': [{'i': p['i'], 't': p['t'], 's': p['s'], 'ts': p['ts']} for p in P], 'x': {str(k): v for k, v in sorted(same.items())}, 'w': rows}
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
cnt = collections.Counter(w['test'] for w in words)
print('SAME_AS', same)
print('PASSAGES', len(P), 'WORDS', len(words), 'TESTS_WITH_WORDS', len(tests), 'WARN', len(warn))
print('TESTS_MISSING_WORDS', [t for t in range(1, 226) if t not in cnt], 'not explained by SAME_AS:', [t for t in range(1, 226) if t not in cnt and t not in same])
print('TESTS_MISSING_PASSAGE_MAP', missing_map)
print('MULTI_TEST_PASSAGES', sum(1 for p in P if len(p['ts']) >= 2), 'SINGLE', sum(1 for p in P if len(p['ts']) == 1))
print('MIN/MAX per test', min(cnt.values()), max(cnt.values()))
for w in warn[:6]: print('WARN', w)
