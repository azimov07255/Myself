#!/usr/bin/env python3
"""data/ielts-lists-v1.json va data/words-v1.txt dan src/js/58-data-lugat.js ni yaratadi (ilova ichiga joylanadigan lug'at ma'lumotlari).
Ro'yxatlarni o'zgartirsangiz shuni qayta ishga tushiring, so'ng tools/build_app.py."""
import json, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lists = json.load(open(os.path.join(root, 'data', 'ielts-lists-v1.json'), encoding='utf-8'))
words = open(os.path.join(root, 'data', 'words-v1.txt'), encoding='utf-8').read().split('\n')[:9000]
js = ("// ---- AVTOMATIK YARATILGAN (tools/make_data_js.py): lug'at ma'lumotlari ilovaning ichida, alohida fayl kerak emas ----\n"
      "// NGSL 1.2 va NAWL 1.2 (Browne, Culligan, Phillips), CC BY-SA 4.0, newgeneralservicelist.com\n"
      "const DATA_LISTS=%s;\nconst DATA_WORDS=%s;\n" % (json.dumps(lists, ensure_ascii=False, separators=(',', ':')), json.dumps('\n'.join(words), ensure_ascii=False)))
open(os.path.join(root, 'src', 'js', '58-data-lugat.js'), 'w', encoding='utf-8').write(js)
print('yozildi:', len(js), 'bayt;', len(words), "so'z (avtomatik to'ldirish asosi)")
