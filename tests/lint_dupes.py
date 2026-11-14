import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Takroriy nomlarni topadi: bir xil funksiya/const ikki marta e'lon qilinsa, keyingisi indamay oldingisini bosib ketadi.
import re,sys,collections
h=open((ROOT + '/tracker/index.html'),encoding='utf-8').read()
js=re.findall(r'<script>(.*?)</script>',h,re.S)[0]
decl=collections.defaultdict(list)
for i,l in enumerate(js.split('\n'),1):
    m=re.match(r'^(?:async\s+)?function\s+(\w+)\s*\(',l) or re.match(r'^(?:const|let|var)\s+(\w+)\s*=',l)
    if m:decl[m.group(1)].append(i)
bad=[(n,ls) for n,ls in decl.items() if len(ls)>1]
print('JS: ta\'riflar',len(decl),'| takroriylar:',bad or 'yo\'q')
css=re.findall(r'<style>(.*?)</style>',h,re.S)[0]
# bitta sinf nomi oddiy (qismlarga bog'lanmagan) qoida sifatida ikki xil joyda e'lon qilinsa ogohlantiradi
simple=collections.defaultdict(int)
for m in re.finditer(r'(?:^|\})\s*(\.[a-zA-Z][\w-]*)\s*\{',css):simple[m.group(1)]+=1
dup=[(k,v) for k,v in simple.items() if v>1]
base={'.bar','.wd','.ai','.aic','.tbb'}   # eskidan qolgan, zararsiz ekani tekshirilgan
new=[(k,v) for k,v in dup if k not in base]
print('CSS: yakka sinf qoidalari takrorlari:',dup or 'yo\'q')
if new:print('XATO: yangi CSS sinf nomi boshqa joyda allaqachon bor (ikkinchisi birinchisini buzadi):',new)
sys.exit(1 if bad or new else 0)
