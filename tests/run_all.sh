#!/bin/bash
# Hamma sinovlarni bir buyruqda ishga tushiradi. Ishlatish:  bash tests/run_all.sh
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd); export KT_ROOT=$ROOT; TMP=${TMPDIR:-/tmp}; JOBS=${JOBS:-4}
APP=$ROOT/tracker/index.html
echo "== src/ va index.html bir xilmi"; python3 $ROOT/tools/build_app.py --check || exit 1
T=$ROOT/tests
python3 - <<PY
import re
h=open("$APP",encoding="utf-8").read()
open("$TMP/t.js","w",encoding="utf-8").write(re.findall(r"<script>(.*?)</script>",h,re.S)[0])
PY
node --check $TMP/t.js || { echo "SINTAKSIS XATO"; exit 1; }
echo "== takroriy nomlar"; python3 $T/lint_dupes.py || { echo "TAKRORIY NOMLAR"; exit 1; }
cp -f $T/shot.py $TMP/shot.py
for f in app_gym_test app_ai_test app_tip_test; do cp -f $T/$f.js $TMP/${f/app_/}.js; done
fail=0
echo "== ilova mantiqi"; for f in gym_test ai_test tip_test; do out=$(node $TMP/$f.js 2>&1); n=$(echo "$out" | grep -c '^PASS'); bad=$(echo "$out" | grep -c -E '^FAIL|Error'); echo "$f: $n o'tdi, $bad xato"; [ "$bad" != "0" ] && { echo "$out" | grep -E '^FAIL|Error' | head -3; fail=1; }; done
echo "== sinxronlash va zaxira"; out=$(node $T/sync_test.js 2>&1); echo "sync_test: $(echo "$out" | grep -c '^PASS') o'tdi, $(echo "$out" | grep -c -E '^FAIL|Error') xato"; echo "$out" | grep -E '^FAIL|Error' | head -3; echo "$out" | grep -q -E '^FAIL|Error' && fail=1
echo "== Telegram (ilova)"; out=$(node $T/tg_client_test.js 2>&1); echo "tg_client_test: $(echo "$out" | grep -c '^PASS') o'tdi, $(echo "$out" | grep -c -E '^FAIL|Error') xato"; echo "$out" | grep -q -E '^FAIL|Error' && fail=1
echo "== supabase papkasi"; python3 $T/check_supabase_folder.py || fail=1
echo "== server"; mkdir -p $TMP/esb; (cd $TMP/esb && [ -d node_modules/esbuild ] || (npm init -y >/dev/null 2>&1; npm i esbuild >/dev/null 2>&1))
for f in server_models_test server_resilience_test server_food_voice_test server_plan_test server_ielts_web_test server_ratelimit_test server_telegram_test server_owner_test widget_server_test server_materials_test server_dict_test server_pack_test server_kurs_test server_tts_test server_hikoya_test server_coach_test server_limit_test server_mnemo_test; do cp -f $T/$f.js $TMP/esb/$f.js; out=$(cd $TMP/esb && node $f.js 2>&1); echo "$f: $(echo "$out" | grep -c '^PASS') o'tdi, $(echo "$out" | grep -c -E '^FAIL|Error') xato"; echo "$out" | grep -q -E '^FAIL|Error' && fail=1; done
echo "== brauzer (telefon o'lchami)"; python3 $T/smoke_browser.py || fail=1
echo "== CSS sinf nomlari to'qnashmasligi"; python3 $T/check_css_collisions.py || fail=1
echo "== brauzer sinovlari (parallel, $JOBS ta bir vaqtda)"
RES=$TMP/kt_res; rm -rf $RES; mkdir -p $RES
run_one(){ python3 "$T/$1.py" > "$RES/$1.txt" 2>&1; }
export -f run_one; export T RES
grep -v '^#' $T/browser_tests.txt | cut -d'|' -f1 | xargs -P $JOBS -I{} bash -c 'run_one {}'
while IFS='|' read -r n title; do
  case "$n" in \#*|"") continue;; esac
  echo "== $title"; out=$(cat "$RES/$n.txt"); echo "$out" | grep -E '^FAIL|passed'
  if echo "$out" | grep -q '^FAIL' || echo "$out" | grep -q 'Traceback'; then fail=1; echo "  XATO: $n"; echo "$out" | grep -E 'Error|Traceback' | head -2; fi
  echo "$out" | grep -q 'passed' || { fail=1; echo "  XATO: $n natija chiqarmadi"; }
done < $T/browser_tests.txt
[ "$fail" = "0" ] && echo "HAMMASI YAXSHI ✅" || echo "XATOLAR BOR ❌"
exit $fail
