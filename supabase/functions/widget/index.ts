// Edge Function: widget — iPhone vidjeti (Scriptable) uchun kichik xulosa beradi.
// Nomi aynan `widget`. Faqat ?t=<maxfiy token> bo'yicha o'qiydi, boshqa hech narsa ochilmaydi.
// Xulosada pul va salomatlik ma'lumoti YO'Q (ilova uni yubormaydi).
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const H = { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'Access-Control-Allow-Origin': '*' }
const J = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: H })

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') return new Response(null, { headers: { ...H, 'Access-Control-Allow-Headers': 'authorization, apikey, content-type' } })
  let t = new URL(req.url).searchParams.get('t') || ''
  if (!t && req.method === 'POST') { try { t = String((await req.json()).t || '') } catch { /* bo'sh */ } }
  if (!/^[a-f0-9]{32,64}$/.test(t)) return J({ error: 'Token noto‘g‘ri.' }, 400)
  const db = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!)
  const { data, error } = await db.from('widget_snap').select('snap,updated_at').eq('token', t).maybeSingle()
  if (error) return J({ error: 'Server xatosi.' }, 500)
  if (!data) return J({ error: 'Vidjet topilmadi. Ilovada vidjetni qayta yoqing.' }, 404)
  return J({ snap: data.snap, updated_at: data.updated_at })
})
