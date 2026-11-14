// Edge Functions -> mavjud "create-user" funksiyasini shu kod bilan almashtiring va Deploy bosing
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

// Faqat shu email egasi (owner) boshqara oladi
// Egasining emaili kodda emas, Supabase Secrets'da saqlanadi (OWNER_EMAIL), shunda ochiq repoda ko'rinmaydi
const OWNER = (Deno.env.get('OWNER_EMAIL') || '').trim().toLowerCase()

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors })
  const json = (o: unknown, s = 200) =>
    new Response(JSON.stringify(o), { status: s, headers: { ...cors, 'Content-Type': 'application/json' } })

  const db = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!)
  const token = (req.headers.get('Authorization') || '').replace('Bearer ', '')
  const { data: u } = await db.auth.getUser(token)
  if (!OWNER || !u?.user || u.user.email?.toLowerCase() !== OWNER) return json({ error: 'Ruxsat yo‘q' }, 403)
  const me = u.user.id
  const b = await req.json()
  const fail = (m: string) => json({ error: m }, 400)

  if (b.action === 'list') {
    const { data: lu } = await db.auth.admin.listUsers({ perPage: 500 })
    const { data: pr } = await db.from('profiles').select('*')
    const { data: st } = await db.from('app_state').select('user_id,updated_at')
    const { data: py } = await db.from('payments').select('amount,created_at')
    const P: Record<string, any> = {}, L: Record<string, string> = {}
    for (const p of pr || []) P[p.user_id] = p
    for (const s of st || []) L[s.user_id] = s.updated_at
    const mk = (t: number) => { const d = new Date(t + 5 * 3600e3); return d.getUTCFullYear() * 12 + d.getUTCMonth() }
    const cur = mk(Date.now())
    let month = 0, prev = 0, total = 0
    for (const x of py || []) {
      const k = mk(new Date(x.created_at).getTime()), a = Number(x.amount)
      total += a; if (k === cur) month += a; else if (k === cur - 1) prev += a
    }
    const users = (lu?.users || []).map((x) => {
      const p = P[x.id]
      return {
        id: x.id, email: x.email, me: x.id === me, name: x.user_metadata?.name || p?.name || '',
        lifetime: p ? p.lifetime : true, expires_at: p?.expires_at || null, blocked: p?.blocked || false, last: L[x.id] || null,
      }
    })
    return json({ users, stats: { month, prev, total } })
  }

  if (b.action === 'create') {
    const email = String(b.login).includes('@') ? String(b.login) : b.login + '@trk.app'
    const { data, error } = await db.auth.admin.createUser({
      email, password: b.password, email_confirm: true, user_metadata: { name: b.name || '' },
    })
    if (error) return fail(error.message)
    const plan = Number(b.plan ?? 7)
    await db.from('profiles').upsert({
      user_id: data.user.id, name: b.name || '', lifetime: plan === -1,
      expires_at: plan === -1 ? null : new Date(Date.now() + plan * 864e5).toISOString(),
    })
    return json({ ok: true, id: data.user.id })
  }

  if (b.action === 'grant') {
    const { data: p } = await db.from('profiles').select('*').eq('user_id', b.id).maybeSingle()
    let row: Record<string, unknown>
    if (Number(b.days) === -1) row = { user_id: b.id, lifetime: true }
    else {
      const base = p?.expires_at && new Date(p.expires_at) > new Date() ? new Date(p.expires_at) : new Date()
      row = { user_id: b.id, lifetime: p?.lifetime || false, expires_at: new Date(base.getTime() + Number(b.days) * 864e5).toISOString() }
    }
    const { error } = await db.from('profiles').upsert(row)
    if (error) return fail(error.message)
    await db.from('payments').insert({ user_id: b.id, amount: Number(b.amount) || 0, days: Number(b.days) })
    return json({ ok: true })
  }

  if (b.action === 'block') {
    if (b.id === me) return fail('O‘zingni bloklab bo‘lmaydi')
    const { error } = await db.from('profiles').upsert({ user_id: b.id, blocked: !!b.blocked })
    if (error) return fail(error.message)
    return json({ ok: true })
  }

  if (b.action === 'setpass') {
    const { error } = await db.auth.admin.updateUserById(b.id, { password: b.password })
    if (error) return fail(error.message)
    return json({ ok: true })
  }

  if (b.action === 'delete') {
    if (b.id === me) return fail('O‘zingni o‘chirib bo‘lmaydi')
    const { error } = await db.auth.admin.deleteUser(b.id)
    if (error) return fail(error.message)
    return json({ ok: true })
  }

  if (b.action === 'revoke') {
    // Premiumni (umrbod yoki muddatli) qaytarib olish: b.days kun qoldiriladi (0 = darhol tugaydi)
    if (b.id === me) return fail('O‘zingdan premiumni qaytarib bo‘lmaydi')
    const d = Math.max(0, Number(b.days) || 0)
    const { error } = await db.from('profiles').upsert({
      user_id: b.id, lifetime: false, expires_at: new Date(Date.now() + d * 864e5).toISOString(),
    })
    if (error) return fail(error.message)
    const amt = Number(b.amount) || 0
    if (amt > 0) await db.from('payments').insert({ user_id: b.id, amount: -amt, days: -1 }) // qaytarilgan pul
    return json({ ok: true })
  }

  return fail('Noma‘lum amal')
})
