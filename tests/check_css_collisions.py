# Yangi CSS fayllaridagi (60 va undan keyingi) sinf nomlari eskilarini buzmasligini tekshiradi.
# Sabab: bir sinf nomi ikki joyda bo'lsa (masalan .mg), ikkinchi joydagi element ilovaning boshqa joyidagi uslubni "meros qilib" buziladi.
import os, re, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); d = os.path.join(root, 'src', 'css')
ALLOW = {'btn', 'x', 'h', 'mfp', 'ok', 'on', 'qopt', 't', 'nx', 'chip', 'big', 'seg', 'row', 'goal', 'hero', 'mu', 'bar', 'in', 'sc', 'st', 'hv', 'tm', 'ck', 'done', 'sd'}   # ataylab umumiy ishlatiladigan sinflar
cls = lambda css: set(re.findall(r'\.([A-Za-z_][\w-]*)', re.sub(r'\{[^}]*\}', '{}', re.sub(r'/\*.*?\*/', '', css, flags=re.S))))
old, new = {}, {}
for f in sorted(os.listdir(d)):
    n = int(re.match(r'(\d+)', f).group(1)); css = open(os.path.join(d, f), encoding='utf-8').read()
    if n >= 90: continue  # yangi dizayn qatlami: ataylab eski sinflarni qayta uslublaydi, tests/ui2_check.py uning hamma qoidasi html.ui2 ostida ekanini tekshiradi
    for c in cls(css): (new if n >= 60 else old).setdefault(c, []).append(f)
bad = {c: old[c] for c in new if c in old and c not in ALLOW}
if bad:
    print('XATO: yangi CSS sinf nomi eskisi bilan bir xil (nomini almashtiring):'); [print('  .%s  (yangi: %s, eski: %s)' % (c, ','.join(new[c]), ','.join(v))) for c, v in sorted(bad.items())]; sys.exit(1)
print('CSS sinf nomlari to\'qnashmaydi (%d yangi sinf tekshirildi)' % len(new))
