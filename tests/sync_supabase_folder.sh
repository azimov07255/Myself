#!/bin/bash
ROOT=$(cd "$(dirname "$0")/.." && pwd)
# server-setup/*.ts ni supabase/functions/*/index.ts ga ko'chiradi (funksiya kodini o'zgartirgandan keyin ishlating)
for n in ai-assistant create-user send-reminders telegram-bot widget; do mkdir -p $ROOT/supabase/functions/$n; cp $ROOT/server-setup/$n.ts $ROOT/supabase/functions/$n/index.ts; done; echo ko\'chirildi
