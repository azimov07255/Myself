#!/bin/bash
# server-setup/*.ts ni supabase/functions/*/index.ts ga ko'chiradi (funksiya kodini o'zgartirgandan keyin ishlating)
for n in ai-assistant create-user send-reminders telegram-bot widget; do mkdir -p /mnt/user-data/outputs/supabase/functions/$n; cp /mnt/user-data/outputs/server-setup/$n.ts /mnt/user-data/outputs/supabase/functions/$n/index.ts; done; echo ko\'chirildi
