// 2-qadam: Edge Functions -> Deploy a new function -> nomi: send-reminders
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import webpush from 'npm:web-push@3.6.7'

const TG_TOKEN = String(Deno.env.get('TELEGRAM_BOT_TOKEN') || '').trim().replace(/^["']|["']$/g, '').replace(/^bot(?=\d)/i, '').trim()
// Eslatma turiga qarab tugma: namoz -> "O'qidim", reja bloki -> "Bajardim"
function tgButtons(kind: string) {
  if (/^nm:\w+$/.test(kind || '')) return { inline_keyboard: [[{ text: '✅ O‘qidim', callback_data: kind }]] }
  if (/^blk:[\w-]+$/.test(kind || '')) return { inline_keyboard: [[{ text: '✅ Bajardim', callback_data: kind }]] }
  return undefined
}

Deno.serve(async (req) => {
  if (req.headers.get('x-cron-secret') !== Deno.env.get('CRON_SECRET')) return new Response('no', { status: 403 })

  webpush.setVapidDetails(Deno.env.get('VAPID_SUBJECT')!, Deno.env.get('VAPID_PUBLIC')!, Deno.env.get('VAPID_PRIVATE')!)
  const db = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!)

  const { data: rems } = await db.from('reminders').select('*')
  const now = Date.now()
  let sent = 0

  for (const r of rems || []) {
    const loc = new Date(now + (r.tz ?? 300) * 60000) // mahalliy vaqt (UTC maydonlarida)
    const date = loc.toISOString().slice(0, 10)
    const nowMin = loc.getUTCHours() * 60 + loc.getUTCMinutes()
    const [h, m] = r.hhmm.split(':').map(Number)
    const delta = nowMin - (h * 60 + m)
    const stamp = date + ' ' + r.hhmm
    if (delta < 0 || delta > 2 || !r.days.includes(loc.getUTCDay()) || r.last_sent === stamp) continue

    // Telegram (agar ulangan bo'lsa)
    if (TG_TOKEN) {
      const { data: link } = await db.from('tg_links').select('chat_id').eq('user_id', r.user_id).maybeSingle()
      if (link) {
        try {
          const resp = await fetch(`https://api.telegram.org/bot${TG_TOKEN}/sendMessage`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: link.chat_id, text: `🔔 ${r.title}` + (r.body ? `\n${r.body}` : ''), reply_markup: tgButtons(r.kind) }),
          })
          if (resp.ok) sent++
          else if (resp.status === 403) await db.from('tg_links').delete().eq('user_id', r.user_id) // foydalanuvchi botni bloklagan
        } catch (_e) { /* keyingi daqiqada qayta urinilmaydi, push baribir ketgan */ }
      }
    }
    const { data: subs } = await db.from('push_subs').select('*').eq('user_id', r.user_id)
    for (const s of subs || []) {
      try {
        await webpush.sendNotification(
          { endpoint: s.endpoint, keys: { p256dh: s.p256dh, auth: s.auth } },
          JSON.stringify({ title: r.title, body: r.body })
        )
        sent++
      } catch (e) {
        if (e.statusCode === 404 || e.statusCode === 410) await db.from('push_subs').delete().eq('endpoint', s.endpoint)
      }
    }
    await db.from('reminders').update({ last_sent: stamp }).eq('id', r.id)
  }
  return new Response(JSON.stringify({ sent }))
})
