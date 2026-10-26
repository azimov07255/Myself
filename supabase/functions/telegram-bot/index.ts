// Edge Function: telegram-bot   (Verify JWT = O'CHIQ bo'lishi kerak: Telegram o'zi chaqiradi)
// Secrets: TELEGRAM_BOT_TOKEN, TELEGRAM_WEBHOOK_SECRET
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
 
// Kalit qiymatlarini tozalaymiz: ortiqcha bo'sh joy, qo'shtirnoq yoki tokenning oldidagi "bot" so'zi xato qilmasin
const clean = (s: string | undefined) => String(s || '').trim().replace(/^["']|["']$/g, '').replace(/^bot(?=\d)/i, '').trim()
const TOKEN = clean(Deno.env.get('TELEGRAM_BOT_TOKEN'))
const SECRET = clean(Deno.env.get('TELEGRAM_WEBHOOK_SECRET'))
const api = (method: string, body: unknown) =>
  fetch(`https://api.telegram.org/bot${TOKEN}/${method}`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  }).then(async (r) => {
    const j = await r.json().catch(() => ({}))
    if (!j?.ok) console.error('telegram api', method, r.status, JSON.stringify(j).slice(0, 200)) // Logs'da ko'rinadi
    return j
  }).catch((e) => { console.error('telegram fetch failed', method, String(e)); return {} })
 
const PRAYERS: Record<string, string> = { fajr: 'Bomdod', dhuhr: 'Peshin', asr: 'Asr', maghrib: 'Shom', isha: 'Xufton' }
const localDate = (tz: number) => new Date(Date.now() + tz * 60000).toISOString().slice(0, 10)
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
 
const HELP = `🤖 <b>Kunlik tizim boti</b>
 
/bugun — bugungi holat (asosiy ishlar, vazifalar, namoz, suv)
/vazifa <i>matn</i> — bugunga vazifa qo‘shish
/suv — bir stakan suv (+1)
/stop — botni uzish
 
Eslatma xabarlaridagi <b>✅</b> tugmalarini bossang, ilovada belgilanadi (ilova keyingi ochilganda qo‘llanadi).`
 
Deno.serve(async (req) => {
  if (!SECRET || req.headers.get('x-telegram-bot-api-secret-token') !== SECRET) return new Response('no', { status: 403 })
  const u = await req.json().catch(() => null)
  if (!u) return new Response('ok')
  const db = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!)
  try {
    if (u.callback_query) await onCallback(db, u.callback_query)
    else if (u.message?.text) await onMessage(db, u.message)
  } catch (e) {
    // Telegram'ga doim 200 qaytariladi (aks holda xabarni qayta-qayta yuboradi), lekin xatoni yozib qo'yamiz
    const msg = String((e as Error)?.message || e)
    console.error('telegram-bot error:', msg)
    const chat = u.message?.chat?.id || u.callback_query?.message?.chat?.id
    if (chat) {
      const hint = /does not exist|schema cache|relation|Could not find/i.test(msg)
        ? '⚠️ Sozlash tugallanmagan: ma‘lumotlar bazasi jadvallari topilmadi. Egasi telegram.sql ni ishga tushirishi kerak.'
        : '⚠️ Vaqtincha xatolik. Birozdan keyin qayta urinib ko‘ring.'
      await api('sendMessage', { chat_id: chat, text: hint })
    }
  }
  return new Response('ok')
})
 
async function getLink(db: any, chat: number) {
  const { data, error } = await db.from('tg_links').select('*').eq('chat_id', chat).maybeSingle()
  if (error) throw new Error(error.message)
  return data
}
 
async function onMessage(db: any, m: any) {
  if (m.chat?.type !== 'private') return
  const chat = m.chat.id as number
  const text = String(m.text || '').trim()
  const parts = text.split(/\s+/)
  const cmd = parts[0].split('@')[0].toLowerCase()
  const arg = parts.slice(1).join(' ').trim()
  const send = (t: string, extra: Record<string, unknown> = {}) => api('sendMessage', { chat_id: chat, text: t, parse_mode: 'HTML', ...extra })
 
  if (cmd === '/start') {
    const code = arg.toUpperCase().replace(/[^A-Z0-9]/g, '')
    if (!code) {
      const l = await getLink(db, chat)
      await send(l ? '✅ Allaqachon ulangansan.\n\n' + HELP : 'Salom! Ulash uchun ilovada <b>Sozlama → Eslatmalar → Telegramga ulash</b> tugmasini bos.')
      return
    }
    const { data: row } = await db.from('tg_codes').select('*').eq('code', code).maybeSingle()
    if (!row || new Date(row.expires_at) < new Date()) { await send('❌ Kod eskirgan yoki noto‘g‘ri. Ilovada “Telegramga ulash” tugmasini qayta bos.'); return }
    await db.from('tg_links').delete().eq('chat_id', chat) // bu chat boshqa hisobga ulangan bo'lsa, uziladi
    await db.from('tg_links').upsert({ user_id: row.user_id, chat_id: chat, username: m.from?.username || null, tz: row.tz ?? 300 })
    await db.from('tg_codes').delete().eq('code', code)
    await send('✅ <b>Ulandi!</b> Endi eslatmalar shu yerga keladi.\n\n' + HELP)
    return
  }
 
  const link = await getLink(db, chat)
  if (!link) { await send('Avval ulang: ilovada <b>Sozlama → Eslatmalar → Telegramga ulash</b>.'); return }
  const d = localDate(link.tz ?? 300)
 
  if (cmd === '/yordam' || cmd === '/help') { await send(HELP); return }
  if (cmd === '/stop') { await db.from('tg_links').delete().eq('chat_id', chat); await send('Bot uzildi. Qayta ulash uchun ilovadan foydalan.'); return }
  if (cmd === '/suv') {
    await db.from('tg_inbox').insert({ user_id: link.user_id, kind: 'water', payload: { d, n: 1 } })
    await send('💧 +1 stakan. (Ilova keyingi ochilganda hisobga qo‘shiladi.)'); return
  }
  if (cmd === '/vazifa') {
    if (!arg) { await send('Matn yoz: <code>/vazifa Kitob o‘qish</code>'); return }
    const t = arg.slice(0, 200)
    await db.from('tg_inbox').insert({ user_id: link.user_id, kind: 'task', payload: { d, t } })
    await send('📝 Vazifa qo‘shildi: <b>' + esc(t) + '</b>\n(Ilova keyingi ochilganda ro‘yxatga tushadi.)'); return
  }
  if (cmd === '/bugun') {
    const { data: st } = await db.from('app_state').select('data').eq('user_id', link.user_id).maybeSingle()
    const s = st?.data || {}
    const top: any[] = s.top?.[d] || [], tasks: any[] = s.tasks?.[d] || [], nm = s.nm?.d?.[d] || {}
    const mark = (x: any) => (x.x ? '✅' : '⬜')
    const lines = [`📅 <b>${d}</b>`]
    if (top.length) lines.push('\n<b>Asosiy ishlar</b>', ...top.map((x) => `${mark(x)} ${esc(String(x.t))}`))
    if (tasks.length) lines.push('\n<b>Vazifalar</b>', ...tasks.slice(0, 12).map((x) => `${mark(x)} ${esc(String(x.t))}`))
    lines.push('\n<b>Namoz</b>', Object.entries(PRAYERS).map(([k, n]) => `${nm[k] === 1 ? '✅' : nm[k] === 2 ? '❌' : '⬜'} ${n}`).join('  '))
    lines.push(`\n💧 Suv: ${s.water?.[d] || 0}/8`)
    lines.push('\n<i>Ilovada hali qo‘llanmagan belgilar bunda ko‘rinmaydi.</i>')
    await send(lines.join('\n')); return
  }
  await send('Tushunmadim. Buyruqlar uchun /yordam ni bos.')
}
 
async function onCallback(db: any, q: any) {
  const chat = q.message?.chat?.id as number
  const answer = (t: string) => api('answerCallbackQuery', { callback_query_id: q.id, text: t })
  const link = chat ? await getLink(db, chat) : null
  if (!link) { await answer('Avval ilovada ulang.'); return }
  const data = String(q.data || '')
  const d = localDate(link.tz ?? 300)
  let ok = false
  if (/^nm:(fajr|dhuhr|asr|maghrib|isha|vitr)$/.test(data)) {
    await db.from('tg_inbox').insert({ user_id: link.user_id, kind: 'nm', payload: { d, p: data.slice(3) } }); ok = true
  } else if (/^blk:[\w-]{1,40}$/.test(data)) {
    await db.from('tg_inbox').insert({ user_id: link.user_id, kind: 'blk', payload: { d, id: data.slice(4) } }); ok = true
  } else if (/^zk:(sb|sh)$/.test(data)) {
    await db.from('tg_inbox').insert({ user_id: link.user_id, kind: 'zk', payload: { d, c: data.slice(3) } }); ok = true
  } else if (/^rz:[12]$/.test(data)) {
    await db.from('tg_inbox').insert({ user_id: link.user_id, kind: 'rz', payload: { d, v: Number(data.slice(3)) } }); ok = true
  }
  if (!ok) { await answer('Noma’lum tugma.'); return }
  await answer('Belgilandi ✅')
  await api('editMessageText', {
    chat_id: chat, message_id: q.message.message_id, parse_mode: 'HTML',
    text: esc(String(q.message.text || '')) + '\n\n✅ <b>Belgilandi</b>', reply_markup: { inline_keyboard: [] },
  })
}
