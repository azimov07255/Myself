# supabase/ papkasi: nusxalar server-setup bilan bir xilmi, config hammasini e'lon qilganmi, maxfiy narsa yo'qmi
import os,re,sys
R='/mnt/user-data/outputs/supabase';S='/mnt/user-data/outputs/server-setup';bad=[]
cfg=open(R+'/config.toml',encoding='utf-8').read()
fns=sorted(d for d in os.listdir(R+'/functions'))
for n in fns:
    a=open(f'{R}/functions/{n}/index.ts',encoding='utf-8').read();b=open(f'{S}/{n}.ts',encoding='utf-8').read()
    if a!=b:bad.append(f'{n}: supabase/ va server-setup/ nusxalari farq qiladi (bash tests/sync_supabase_folder.sh)')
    if f'[functions.{n}]' not in cfg:bad.append(f'{n}: config.toml da e\'lon qilinmagan (Deploy bo\'lmaydi)')
    if re.search(r'eyJ[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{20}|\d{8,}:[A-Za-z0-9_-]{30,}|BEGIN (RSA|PRIVATE)|@gmail\.com',a):bad.append(f'{n}: maxfiy yoki shaxsiy ma\'lumotga o\'xshash matn bor')
if not re.search(r'\[functions\.telegram-bot\]\s*verify_jwt\s*=\s*false',cfg):bad.append('telegram-bot uchun verify_jwt = false yo\'q (bot ishlamay qoladi)')
if os.path.isdir(R+'/migrations'):bad.append('migrations/ papkasi bor: eski SQL qayta ishga tushib xato berishi mumkin')
print('supabase/ papkasi:',len(fns),'ta funksiya |',('muammo: '+'; '.join(bad)) if bad else 'hammasi joyida')
sys.exit(1 if bad else 0)
