# Yangi dizayn qatlami (90-ui2.css): HAMMA qoida faqat html.ui2 (yoki matn o'lchami/animatsiya tanlovi) ostida bo'lishi shart: klassik ko'rinish o'zgarmasligi kafolati.
import re, sys
css = re.sub(r'/\*.*?\*/', '', open('/mnt/user-data/outputs/src/css/90-ui2.css', encoding='utf-8').read() + open('/mnt/user-data/outputs/src/css/91-glass.css', encoding='utf-8').read(), flags=re.S)
OK = ('html.ui2', 'html[data-fs=', 'html[data-mo=')
bad, n = [], 0
def walk(t):
    global n
    i = 0
    while i < len(t):
        j = t.find('{', i)
        if j < 0: break
        head = t[i:j].strip(); depth = 1; k = j + 1
        while depth and k < len(t):
            depth += {'{': 1, '}': -1}.get(t[k], 0); k += 1
        body = t[j + 1:k - 1]
        if head.startswith('@media'): walk(body)
        elif head.startswith('@'): pass
        else:
            for sel in head.split(','):
                sel = sel.strip()
                if not sel: continue
                n += 1
                if not sel.startswith(OK): bad.append(sel)
        i = k
walk(css)
print('PASS' if not bad else 'FAIL', 'every rule of the new design layer is scoped (%d selectors checked)' % n, bad[:5])
print('%d passed, %d failed' % (0 if bad else 1, 1 if bad else 0))
sys.exit(1 if bad else 0)
