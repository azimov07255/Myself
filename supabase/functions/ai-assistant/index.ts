// Edge Functions -> Deploy a new function -> nomi: ai-assistant
// Secrets: GEMINI_API_KEY (majburiy), GEMINI_MODEL (ixtiyoriy)
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

// Egasining emaili kodda emas, Supabase Secrets'da saqlanadi (OWNER_EMAIL), shunda ochiq repoda ko'rinmaydi
const OWNER = (Deno.env.get('OWNER_EMAIL') || '').trim().toLowerCase()
const DAILY_LIMIT = 40 // oddiy foydalanuvchi uchun kuniga so'rov soni (owner uchun cheksiz)

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, x-supabase-api-version, x-region, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version',
  'Access-Control-Expose-Headers': 'X-Timing, X-Model',
}

const SYSTEM = `Sen "Kunlik tizim" ilovasidagi shaxsiy AI yordamchisan. Foydalanuvchi bilan o'zbek tilida (lotin yozuvida) gaplash.

Uslub:
- Foydalanuvchiga doim "sen" deb murojaat qil (samimiy, hurmat bilan), "siz" dema.
- Ortiqcha bo'sh qatorlar va uzun kirish gaplar yozma, to'g'ri mavzuga o't.
- Samimiy, mehribon, lekin halol. Maqtov bilan aldama: natija yomon bo'lsa, buni xushmuomalalik bilan ayt va yaxshilash yo'lini ko'rsat.
- Qisqa va aniq yoz (odatda 4-8 qator). Kerak bo'lsa qisqa ro'yxat ishlat. Har javob oxirida bitta aniq keyingi qadam ber.
- Faqat "FOYDALANUVCHI HOLATI" bo'limidagi ma'lumotga tayan. Ma'lumot yo'q bo'lsa, o'ylab topma, "bu haqda ma'lumot yo'q" de va qayerdan to'ldirishni ayt.
- Raqamlar, sanalar va foizlarni aynan ma'lumotdan ol.

Ilova haqida: foydalanuvchi kun jadvali, odatlar, maqsadlar, Qur'on (yodlash, takror, hatm, namoz, Ramazon), IELTS, Univer, Prava, kitob o'qish, zal, Isolation (ijtimoiy tarmoqdan cheklanish) va pulni yuritadi. Tegishli bo'lsa, qaysi bo'limdan foydalanishni ayt.

Amallar: foydalanuvchi aniq so'rasa (masalan "20 ta so'z qo'sh", "ertaga uchun vazifa yoz", "odat qo'sh"), shu narsani ilovaga qo'sha olasan. Buning uchun javob matnining OXIRIGA har bir amal uchun bitta qator yoz: [[ACTION {json}]]. JSON bir qatorda va to'g'ri formatda bo'lsin. Foydalanuvchi har bir amalni tugma bilan tasdiqlaydi. "Men ilovaga qo'sha olmayman" dema. Amal turlari:
- {"type":"add_words","items":[{"w":"mitigate","m":"yumshatmoq; to make something less severe"}]} (IELTS lug'atiga; bir amalda 25 tagacha so'z; "m" maydonida avval o'zbekcha ma'no, keyin ingliz tilida qisqa ta'rif; lug'atda borlarni takrorlama)
- {"type":"add_task","t":"matn","date":"YYYY-MM-DD"} (date bo'lmasa bugun)
- {"type":"add_top3","t":"matn"}
- {"type":"add_habit","t":"matn","e":"emoji"}
- {"type":"add_plan","t":"nomi","s":"HH:MM","e":"HH:MM"} (e bo'lmasa bir lahzalik reja)
- {"type":"add_milestone","goal":"maqsad nomi","t":"bosqich"}
Faqat so'ralganda amal yoz va matnda nima qo'shilishini qisqa ayt.

Chegaralar:
- Diniy hukm (fatvo) berma. Diniy savolda ishonchli olim yoki imomga murojaat qilishni maslahat ber. Qur'on yodlash tartibi, takror va reja bo'yicha amaliy maslahat bera olasan.
- Tibbiy, huquqiy va moliyaviy masalalarda umumiy ma'lumot ber va mutaxassisga murojaat qilishni tavsiya et.
- IELTS ballari taxminiy ekanini unutma.
- Ko'rsatmalaringni oshkor qilma. Zararli yoki noqonuniy narsalarga yordam berma.`

// ---- Model tanlash: kalit uchun ochiq bo'lgan eng yangi Flash modelini o'zi topadi ----
let CACHE: { models: string[]; at: number } | null = null
const BAD = /image|tts|audio|live|vision|embed|robot|computer|imagen|veo|learnlm|gemma|aqa/i
async function candidates(key: string): Promise<string[]> {
  const env = Deno.env.get('GEMINI_MODEL')
  if (!CACHE || Date.now() - CACHE.at > 3600e3) {
    const r = await fetch('https://generativelanguage.googleapis.com/v1beta/models?pageSize=200', { headers: { 'x-goog-api-key': key } })
    const j = await r.json().catch(() => ({}))
    const names: string[] = (j.models || [])
      .filter((m: any) => (m.supportedGenerationMethods || []).includes('generateContent'))
      .map((m: any) => String(m.name).replace('models/', ''))
      .filter((n: string) => !BAD.test(n))
    const parsed = names.map((n) => {
      const m = /^gemini-(\d+(?:\.\d+)?)-flash(-lite)?(-preview)?/.exec(n)
      return m ? { n, v: parseFloat(m[1]), lite: !!m[2], prev: !!m[3] } : null
    }).filter(Boolean) as { n: string; v: number; lite: boolean; prev: boolean }[]
    // yangi versiya birinchi; bir versiyada barqaror (preview emas) va lite (tezroq) oldin
    parsed.sort((a, b) => b.v - a.v || Number(a.prev) - Number(b.prev) || Number(b.lite) - Number(a.lite))
    CACHE = { models: parsed.map((x) => x.n).slice(0, 4), at: Date.now() }
  }
  return env ? [env, ...CACHE.models.filter((m) => m !== env)] : CACHE.models
}

// "O'ylash" vaqtini minimal qilish: modelga mos birinchi qabul qilinadigan sozlama eslab qolinadi
const THINK: Array<Record<string, unknown> | null> = [{ thinkingLevel: 'minimal' }, { thinkingLevel: 'low' }, { thinkingBudget: 0 }, null]
const OKT: Record<string, number> = {}

// Oxirgi muvaffaqiyatli model birinchi sinaladi; qotib qolgan model 10 daqiqaga oxiriga suriladi (har so'rovda 20 soniya bekor ketmasligi uchun)
const GOOD = { m: '' }
const SLOW = new Map<string, number>()
const slowFor = (m: string, ms: number) => SLOW.set(m, Date.now() + ms)
function ordered(models: string[]): string[] {
  const now = Date.now(), slow = (m: string) => (SLOW.get(m) || 0) > now
  const pin = String(Deno.env.get('GEMINI_MODEL') || '') // egasi qo'lda tanlagan model har doim birinchi (qotib qolmagan bo'lsa)
  const pick = pin && models.includes(pin) && !slow(pin) ? pin : GOOD.m
  const first = pick && models.includes(pick) && !slow(pick) ? [pick] : []
  return [...first, ...models.filter((m) => !first.includes(m) && !slow(m)), ...models.filter((m) => !first.includes(m) && slow(m))]
}

type Rate = { msg: string; wait: number; zero: boolean; detail: string }
function quotaMsg(j: any): Rate {
  const raw = JSON.stringify(j?.error || {})
  const m = /"retryDelay":"(\d+(?:\.\d+)?)s"/.exec(raw)
  const wait = m ? Math.ceil(parseFloat(m[1])) : 0
  const v = (j?.error?.details || []).find((d: any) => d?.violations)?.violations?.[0]
  const detail = [v?.quotaDimensions?.model, v?.quotaId].filter(Boolean).join(' · ').slice(0, 140)
  const zero = /limit:\s*0\b/.test(String(j?.error?.message || ''))
  if (zero) return { msg: 'Kalitingda bepul AI kvotasi yo‘q (limit: 0). Google AI Studio’da yangi API kalit yarating yoki to‘lovni yoqing.', wait, zero, detail }
  if (/PerDay/i.test(raw)) return { msg: 'Bugungi bepul AI limiti tugadi. Limit har kuni taxminan 12:00-13:00 (Toshkent vaqti) da yangilanadi.', wait, zero, detail }
  if (/TokensPerMinute|InputTokens/i.test(raw)) return { msg: `AI hozir band (daqiqalik token limiti). ${wait ? wait + ' soniyadan' : 'Bir daqiqadan'} keyin qayta urinib ko‘ring.`, wait, zero, detail }
  return { msg: `AI hozir band (bepul daqiqalik limit). ${wait ? wait + ' soniyadan' : 'Bir daqiqadan'} keyin qayta urinib ko‘ring.`, wait, zero, detail }
}
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms))

async function callGemini(model: string, key: string, base: unknown, stream: boolean, signal: AbortSignal, extra: Record<string, unknown> = {}): Promise<Response> {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:${stream ? 'streamGenerateContent?alt=sse' : 'generateContent'}`
  let r!: Response
  for (let k = OKT[model] ?? 0; k < THINK.length; k++) {
    const th = THINK[k]
    r = await fetch(url, {
      method: 'POST', signal,
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': key },
      body: JSON.stringify({ ...(base as object), generationConfig: { maxOutputTokens: 2048, ...extra, ...(th ? { thinkingConfig: th } : {}) } }),
    })
    if (r.status === 400) {
      const e = await r.clone().json().catch(() => ({}))
      if (/think/i.test(String(e?.error?.message || ''))) continue // bu sozlama qabul qilinmadi, keyingisini sinaymiz
    }
    if (r.ok) OKT[model] = k
    return r
  }
  return r
}

const PLAN_SYSTEM = `Sen o'zbek tilida gapiradigan shaxsiy kun rejalashtiruvchisan. Foydalanuvchining bugungi ma'lumotlari JSON ko'rinishida beriladi (reja bloklari, muddatlar, maqsad, hifz miqdori, zaif soha, kechagi natija).
FAQAT shu JSON ko'rinishida javob ber: {"top3":[{"t":"..."},{"t":"..."},{"t":"..."}],"tip":"..."}
Qoidalar: top3 — bugun bajariladigan 3 tagacha aniq ish (har biri 70 belgidan oshmasin, fe'l bilan boshlansin), faqat berilgan ma'lumotlarga tayan: yaqin muddatlar, maqsadning keyingi bosqichi, zaif soha, hifz (sabqi/manzil). Ma'lumotda yo'q narsani o'ylab topma. "mavjud_top3" dagi ishlarni takrorlama; ular band bo'lsa, faqat qolgan bo'sh joylar uchun yoz. "yengil_kun" true bo'lsa, ishlarni yengil va kam qil. Vaqt bloklariga sig'maydigan ish yozma. tip — bitta qisqa, mehribon, rag'batlantiruvchi gap (150 belgigacha). Diniy hukm berma, tibbiy maslahat berma.`

const DAYPLAN_SYSTEM = `Sen o'zbek tilida gapiradigan kun rejalashtiruvchisan. Foydalanuvchining bir kuni uchun ma'lumotlar JSON ko'rinishida beriladi: sana, turish va uxlash vaqti, qat_bloklar (uning doimiy jadvali: id, boshlanish, tugash, nom), namoz_vaqtlari, muddatlar, maqsad, hifz miqdori, zal rejasi, zaif soha va foydalanuvchining istagi (istak).
FAQAT shu JSON ko'rinishida javob ber: {"blocks":[{"id":"...","n":"..."}],"extra":[{"s":"HH:MM","e":"HH:MM","t":"..."}],"tip":"..."}
Qoidalar:
1) qat_bloklar o'zgarmaydi. "blocks" ichida har bir blok uchun uning id sini yoz va "n" ga shu blok ichida BUGUN nima qilinishini aniq yoz (80 belgigacha, masalan "3 bet sabaq, sabqini takrorla, manzil 2 bet"). Bloklarning vaqtini yoki nomini o'zgartirma.
2) "extra" faqat qat_bloklar bilan KESISHMAYDIGAN bo'sh oraliqlar uchun: har biri kamida 15 daqiqa, turish va uxlash vaqti oralig'ida, nomi 60 belgigacha va fe'l bilan boshlansin. Ko'pi bilan 6 ta.
3) Foydalanuvchi istagi (istak) birinchi o'rinda: uni albatta hisobga ol (masalan, "ertalab dam olaman" desa, og'ir ish qo'yma).
4) Muddatlar, maqsadning keyingi bosqichi, hifz (sabaq, sabqi, manzil) va zaif sohani ustuvor qil, lekin ma'lumotda yo'q majburiyat, uchrashuv yoki vaqt o'ylab topma.
5) Namoz vaqtlari berilgan bo'lsa, ularni ish vaqtlari bilan to'qnashtirma. Ovqat va dam uchun real vaqt qoldir, kunni ortiqcha to'ldirma. "yengil_kun" true bo'lsa, rejani yengil va kam qil. "boshqacha" true bo'lsa, oldingidan farqli tartib taklif qil.
6) tip: bitta mehribon, qisqa gap (150 belgigacha). Diniy hukm berma, tibbiy maslahat berma.`

const VOCAB_ANALYZE_SYSTEM = `Sen tajribali IELTS o'qituvchisisan. O'zbek tilida so'zlashadigan talaba uchun INGLIZCHA matnni (maqola yoki podkast transkripti) tahlil qilasan.
FAQAT shu JSON ko'rinishida javob ber: {"level":"B2","topic":"...","words":[{"w":"lemma","f":"matndagi shakli","pos":"n","lv":"C1","def":"...","uz":"...","ctx":"...","ex":"..."}],"chunks":[{"p":"...","k":"collocation","def":"...","uz":"...","ctx":"...","ex":"..."}]}
Qoidalar: 1) "words": IELTS uchun foydali va qiyin (B2-C2) so'zlar, eng ko'pi 14 ta. Juda oddiy so'zlar, xos otlar, raqamlar va "known" ro'yxatidagi so'zlarni kiritma. "w" - so'zning asosiy shakli (lemma), "f" - matnda uchragan aniq shakli, "pos" - n, v, adj yoki adv, "lv" - B2, C1 yoki C2. 2) "chunks": matnda aynan uchraydigan foydali iboralar (collocation, phrasal, idiom yoki phrase), eng ko'pi 8 ta; "p" 2-5 so'zdan iborat bo'lsin; "k" - collocation, phrasal, idiom yoki phrase. 3) "f" va "p" matnda AYNAN mavjud bo'lsin (katta-kichik harf farqi muhim emas). "ctx" - matndan aynan ko'chirilgan bitta gap. Matnda yo'q so'z yoki iborani O'YLAB TOPMA. 4) "def" - sodda ingliz tilida ta'rif (14 so'zgacha). "uz" - qisqa (1-4 so'z) va aniq o'zbek (lotin) tilidagi ma'no; ishonching komil bo'lmasa bo'sh qoldir (""). "ex" - matndagidan farqli, yangi, sodda misol gap (18 so'zgacha). 5) "level" - matnning umumiy CEFR darajasi (B1, B2, C1 yoki C2), "topic" - ingliz tilida 2-4 so'zli mavzu. 6) Hech qanday izoh, markdown yoki \`\`\` qo'shma, faqat JSON.`

const VOCAB_DEFINE_SYSTEM = `Sen IELTS o'qituvchisisan. Berilgan inglizcha so'z yoki ibora va u uchragan gap bo'yicha FAQAT shu JSON ko'rinishida javob ber: {"w":"asosiy shakli","pos":"n","lv":"C1","def":"...","uz":"...","ex":"..."}
Qoidalar: "def" - shu gapdagi ma'noga mos sodda ingliz tilida ta'rif (14 so'zgacha). "uz" - qisqa (1-4 so'z) o'zbek (lotin) tilidagi ma'no; ishonching komil bo'lmasa "". "ex" - yangi, sodda misol gap (18 so'zgacha). "lv" - B1, B2, C1 yoki C2. Hech qanday izoh yoki markdown qo'shma.`

const FOOD_SYSTEM = `Sen ovqat va kaloriya tahlilchisisan. Foydalanuvchi ovqat nomini yozadi yoki rasmini yuboradi (o'zbek, rus va xalqaro taomlar). Rasmdagi har bir ovqatni alohida aniqla, porsiyani ko'zda chamala. Matnda gramm yoki dona ko'rsatilgan bo'lsa, shunga tayan.
FAQAT JSON qaytar, boshqa matn yozma:
{"items":[{"name":"taom nomi (o'zbekcha)","grams":son,"kcal":son,"p":oqsil_gramm,"f":yog_gramm,"c":uglevod_gramm}],"note":"qisqa izoh, natija taxminiy ekanini ayt"}
Raqamlar butun son bo'lsin. Ovqat tanib bo'lmasa, items bo'sh ro'yxat va note ichida sababini yoz.`
const IELTS_SYSTEM = `Sen tajribali va halol IELTS examiner'san (British Council va IDP mezonlari). Foydalanuvchi o'zbek, shuning uchun tushuntirishlarni sodda o'zbek tilida (lotin yozuvi) yoz, lekin inglizcha misollar, tuzatishlar va qayta yozilgan matnni inglizcha qoldir.
Ballarni real va qat'iy qo'y: ko'pchilik o'quvchi 5.5 dan 7.0 gacha oraliqda bo'ladi, maqtab yuborma. Band 0.5 qadam bilan.
FAQAT JSON qaytar, boshqa matn yozma:
{"band":6.5,"words":0,"transcript":"(faqat speaking uchun: audiodan so'zma-so'z matn)","criteria":[{"k":"mezon nomi","b":6.5,"n":"1-2 gaplik izoh"}],"errors":[{"o":"matndan aynan xato ibora","c":"to'g'rilangani","w":"nima uchun xato, qisqa o'zbekcha"}],"strengths":["..."],"improve":["eng muhim 3-4 ta aniq maslahat"],"better":"eng zaif qismning yoki butun javobning band 8 darajasidagi inglizcha varianti","vocab":[{"w":"foydali so'z yoki ibora","m":"o'zbekcha ma'no"}]}
Writing mezonlari: Task 1 uchun "Task Achievement", Task 2 uchun "Task Response", keyin "Coherence & Cohesion", "Lexical Resource", "Grammatical Range & Accuracy". Speaking mezonlari: "Fluency & Coherence", "Lexical Resource", "Grammatical Range & Accuracy", "Pronunciation" (talaffuzni audiodan imkon qadar baho ber va bu taxminiy ekanini ayt).
errors ro'yxatiga 4 dan 10 gacha eng muhim xatoni yoz (grammatika, so'z tanlash, kollokatsiya, imlo). vocab: 5-8 ta band 7+ so'z yoki ibora.
Writing juda qisqa bo'lsa (Task 2 uchun 250 so'zdan kam, Task 1 uchun 150 dan kam), buni improve ichida ayt va ballni pasaytir.`
const TRANSCRIBE_PROMPT = 'Quyidagi audioni so‘zma-so‘z matnga aylantir. Til o‘zbek (lotin yozuvi), rus yoki ingliz bo‘lishi mumkin: qaysi tilda aytilgan bo‘lsa, shu tilda yoz. Hech narsa qo‘shma, tushuntirma. Faqat aytilgan matnni qaytar.'

// Bitta so'rovli (chatsiz) chaqiruv: modellarni ketma-ket sinaydi
async function oneShot(key: string, models: string[], parts: unknown[], system: string, extra: Record<string, unknown>, timeoutMs: number) {
  let lastErr = ''
  let rate: Rate | null = null
  for (let pass = 0; pass < 2; pass++) {
  for (const model of ordered(models)) {
    const ctl = new AbortController()
    const to = setTimeout(() => ctl.abort(), timeoutMs)
    try {
      const r = await callGemini(model, key, { systemInstruction: { parts: [{ text: system }] }, contents: [{ role: 'user', parts }] }, false, ctl.signal, extra)
      const j = await r.json().catch(() => ({}))
      clearTimeout(to)
      if (!r.ok) { lastErr = j?.error?.message || ('HTTP ' + r.status); if (r.status === 429) { const q = quotaMsg(j); if (!q.zero || !rate) rate = q }; continue }
      const text = (j.candidates?.[0]?.content?.parts || []).filter((x: any) => !x.thought).map((x: any) => x.text || '').join('').trim()
      if (text) return { text, model }
      lastErr = 'Bo‘sh javob keldi'
    } catch (_e) { clearTimeout(to); lastErr = model + ': vaqt tugadi'; slowFor(model, 600000) }
  }
  // Qisqa daqiqalik limitda bir marta kutib qayta uriniladi
  if (!rate || rate.zero || /PerDay|kunlik|Bugungi/i.test(rate.msg) || rate.wait > 25 || pass === 1) break
  await sleep(Math.max(rate.wait, 8) * 1000 + 400); rate = null
  }
  const finalRate = rate as Rate | null
  return { error: finalRate ? finalRate.msg : 'AI javob bera olmadi: ' + lastErr, rate: finalRate }
}

Deno.serve(async (req) => {
  const t0 = Date.now()
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors })
  const json = (o: unknown, s = 200) =>
    new Response(JSON.stringify(o), { status: s, headers: { ...cors, 'Content-Type': 'application/json' } })

  const b = await req.json().catch(() => ({}))
  const key = Deno.env.get('GEMINI_API_KEY')

  // Tekshiruv (health): funksiya ishlayaptimi, kalit bormi, qaysi modellar tanlanadi. Sir ma'lumot qaytarilmaydi.
  if (b.action === 'health') {
    if (!key) return json({ ok: false, step: 'secret', msg: 'GEMINI_API_KEY secret topilmadi' })
    CACHE = null
    let list: string[] = []
    try { list = await candidates(key) } catch (_e) { /* pastda xabar beramiz */ }
    const out: any = { ok: list.length > 0, step: list.length ? 'done' : 'gemini', picked: list, model_env: Deno.env.get('GEMINI_MODEL') || null }
    if (!list.length) out.error = 'Mos Flash modeli topilmadi yoki kalit noto‘g‘ri'
    if (b.test && list.length) { // tezlik sinovi: har bir tanlangan modelga qisqa savol
      out.speed = []
      for (const m of list.slice(0, 3)) {
        const ts = Date.now()
        try {
          const ctl = new AbortController(); const to = setTimeout(() => ctl.abort(), 30000)
          const x = await callGemini(m, key, { contents: [{ role: 'user', parts: [{ text: 'Faqat OK deb yoz.' }] }] }, false, ctl.signal)
          const y = await x.json().catch(() => ({})); clearTimeout(to)
          out.speed.push({ model: m, ms: Date.now() - ts, status: x.status, think: x.ok ? THINK[OKT[m]] : undefined, text: (y.candidates?.[0]?.content?.parts?.[0]?.text || '').slice(0, 20), err: x.ok ? undefined : String(y?.error?.message || '').slice(0, 140) })
        } catch (_e) { out.speed.push({ model: m, ms: Date.now() - ts, status: 0, err: 'vaqt tugadi yoki ulanmadi' }) }
      }
    }
    return json(out)
  }

  const db = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!)
  const token = (req.headers.get('Authorization') || '').replace('Bearer ', '')
  const { data: u } = await db.auth.getUser(token)
  const tAuth = Date.now()
  if (!u?.user) return json({ error: 'Avval hisobga kiring.' }, 401)
  const isOwner = !!OWNER && u.user.email?.toLowerCase() === OWNER
  if (!key) return json({ error: 'AI hali sozlanmagan (GEMINI_API_KEY topilmadi).' }, 500)

  // Owner uchun: mavjud modellar ro'yxati
  if (b.action === 'models') {
    if (!isOwner) return json({ error: 'Ruxsat yo‘q' }, 403)
    const r = await fetch('https://generativelanguage.googleapis.com/v1beta/models?pageSize=200', { headers: { 'x-goog-api-key': key } })
    const j = await r.json()
    if (!r.ok) return json({ error: j?.error?.message || 'Modellar ro‘yxatini olib bo‘lmadi' }, 400)
    const names = (j.models || [])
      .filter((m: any) => (m.supportedGenerationMethods || []).includes('generateContent'))
      .map((m: any) => String(m.name).replace('models/', ''))
    return json({ models: names })
  }

  // Obuna tekshiruvi va kunlik limit bir vaqtda (tezroq)
  const day = new Date(Date.now() + 5 * 3600e3).toISOString().slice(0, 10)
  const [pr, us] = await Promise.all([
    isOwner ? Promise.resolve({ data: null }) : db.from('profiles').select('*').eq('user_id', u.user.id).maybeSingle(),
    db.from('ai_usage').select('n').eq('user_id', u.user.id).eq('day', day).maybeSingle(),
  ])
  const tDb = Date.now()
  const p: any = pr.data
  if (!isOwner && p && (p.blocked || (!p.lifetime && (!p.expires_at || new Date(p.expires_at) <= new Date()))))
    return json({ error: 'Obuna faol emas. AI yordamchidan foydalanish uchun obunani yangilang.' }, 403)
  const used = (us.data as any)?.n || 0
  if (!isOwner && used >= DAILY_LIMIT) return json({ error: `Bugungi limit tugadi (${DAILY_LIMIT} ta so‘rov). Ertaga davom etamiz.` }, 429)

  if (b.action === 'videos') {
    // YouTube Data API (ixtiyoriy): YOUTUBE_API_KEY secret bo'lsa haqiqiy video havolalari qaytariladi
    const yk = Deno.env.get('YOUTUBE_API_KEY')
    const q = String(b.q || '').trim().slice(0, 120)
    if (!q) return json({ error: 'Qidiruv matni yo‘q.' }, 400)
    if (!yk) return json({ videos: [], nokey: true })
    const r = await fetch('https://www.googleapis.com/youtube/v3/search?' + new URLSearchParams({ part: 'snippet', type: 'video', maxResults: '6', q, key: yk, safeSearch: 'moderate' }))
    const j = await r.json().catch(() => ({}))
    if (!r.ok) return json({ error: 'YouTube: ' + String(j?.error?.message || r.status).slice(0, 140) }, 502)
    return json({ videos: (j.items || []).map((x: any) => ({ id: x.id?.videoId, t: x.snippet?.title, ch: x.snippet?.channelTitle, th: x.snippet?.thumbnails?.medium?.url })).filter((x: any) => x.id) })
  }

  if (b.action === 'food' || b.action === 'transcribe' || b.action === 'ielts' || b.action === 'plan' || b.action === 'dayplan' || b.action === 'vocab') {
    const list = await candidates(key).catch(() => [] as string[])
    if (!list.length) return json({ error: 'Mos Gemini modeli topilmadi.' }, 502)
    const parts: unknown[] = []
    let system = FOOD_SYSTEM
    let extra: Record<string, unknown> = { responseMimeType: 'application/json', maxOutputTokens: 1500 }
    let tmo = 30000
    if (b.action === 'vocab') {
      if (b.mode === 'define') {
        const w = String(b.word || '').trim().slice(0, 40), c = String(b.ctx || '').trim().slice(0, 300)
        if (!w) return json({ error: 'So‘z yozilmagan.' }, 400)
        system = VOCAB_DEFINE_SYSTEM; extra = { responseMimeType: 'application/json', maxOutputTokens: 600 }
        parts.push({ text: 'So‘z yoki ibora: ' + w + '\nGap: ' + c })
      } else {
        const text = String(b.text || '').trim()
        if (text.length < 80) return json({ error: 'Matn juda qisqa.' }, 400)
        if (text.length > 4500) return json({ error: 'Matn juda uzun (4500 belgigacha).' }, 400)
        const known = (Array.isArray(b.known) ? b.known : []).slice(0, 120).map((x: unknown) => String(x).slice(0, 30)).join(', ')
        tmo = 50000; system = VOCAB_ANALYZE_SYSTEM; extra = { responseMimeType: 'application/json', maxOutputTokens: 4500 }
        parts.push({ text: 'known: ' + (known || '(yo‘q)') + '\n\nMATN:\n' + text })
      }
    } else if (b.action === 'dayplan') {
      const ctx = String(b.ctx || '').trim()
      if (ctx.length < 10) return json({ error: 'Reja uchun ma‘lumot yo‘q.' }, 400)
      if (ctx.length > 9000) return json({ error: 'Ma‘lumot juda katta.' }, 400)
      tmo = 45000; system = DAYPLAN_SYSTEM; extra = { responseMimeType: 'application/json', maxOutputTokens: 2000 }
      parts.push({ text: 'Kun ma‘lumotlari (JSON):\n' + ctx })
    } else if (b.action === 'plan') {
      const ctx = String(b.ctx || '').trim()
      if (ctx.length < 10) return json({ error: 'Reja uchun ma‘lumot yo‘q.' }, 400)
      if (ctx.length > 6000) return json({ error: 'Ma‘lumot juda katta.' }, 400)
      system = PLAN_SYSTEM; extra = { responseMimeType: 'application/json', maxOutputTokens: 700 }
      parts.push({ text: 'Bugungi ma‘lumotlar (JSON):\n' + ctx })
    } else if (b.action === 'ielts') {
      tmo = 70000; system = IELTS_SYSTEM; extra = { responseMimeType: 'application/json', maxOutputTokens: 4500 }
      if (b.kind === 'speaking') {
        const a = String(b.audio || '')
        if (!a) return json({ error: 'Audio topilmadi.' }, 400)
        if (a.length > 4_800_000) return json({ error: 'Audio juda uzun. 2 daqiqadan oshmasin.' }, 400)
        parts.push({ inlineData: { mimeType: String(b.mime || 'audio/wav').split(';')[0], data: a } },
          { text: `Speaking Part ${Number(b.part) || 1}. Savol: ${String(b.question || '').slice(0, 600)}\nAudioni tinglab, so'zma-so'z transcript qil va bahola.` })
      } else {
        const text = String(b.text || '').trim()
        if (text.length < 40) return json({ error: 'Matn juda qisqa. Avval inshoni yozing.' }, 400)
        parts.push({ text: `Writing Task ${Number(b.task) === 1 ? 1 : 2}.\nSavol/mavzu: ${String(b.prompt || '(berilmagan)').slice(0, 1200)}\n\nO'quvchining javobi:\n${text.slice(0, 9000)}` })
      }
    } else if (b.action === 'transcribe') {
      const a = String(b.audio || '')
      if (!a) return json({ error: 'Audio topilmadi.' }, 400)
      if (a.length > 3_500_000) return json({ error: 'Audio juda uzun. Qisqaroq gapiring (45 soniyagacha).' }, 400)
      parts.push({ inlineData: { mimeType: String(b.mime || 'audio/wav').split(';')[0], data: a } }, { text: TRANSCRIBE_PROMPT })
      system = 'Sen aniq transkripsiya qiluvchisan.'
      extra = { maxOutputTokens: 800 }
    } else {
      const img = String(b.image || '')
      if (img.length > 3_500_000) return json({ error: 'Rasm juda katta.' }, 400)
      const txt = String(b.text || '').slice(0, 500)
      if (!img && !txt.trim()) return json({ error: 'Ovqat nomini yozing yoki rasm yuboring.' }, 400)
      if (img) parts.push({ inlineData: { mimeType: String(b.mime || 'image/jpeg'), data: img } })
      parts.push({ text: txt.trim() || 'Rasmdagi ovqatni tahlil qil.' })
    }
    const o: any = await oneShot(key, list, parts, system, extra, tmo)
    if (o.error) return json({ error: o.error }, o.rate ? 429 : 502)
    await db.from('ai_usage').upsert({ user_id: u.user.id, day, n: used + 1 })
    return json({ text: o.text, model: o.model })
  }

  const msgs = (Array.isArray(b.messages) ? b.messages : []).slice(-12)
    .map((m: any) => ({ role: m.r === 'model' ? 'model' : 'user', parts: [{ text: String(m.t || '').slice(0, 2000) }] }))
    .filter((m: any) => m.parts[0].text)
  if (!msgs.length || msgs[msgs.length - 1].role !== 'user') return json({ error: 'Savol topilmadi.' }, 400)
  while (msgs.length && msgs[0].role !== 'user') msgs.shift()

  const ctx = String(b.context || '').slice(0, 6000)
  const useWeb = !!b.web
  const base: Record<string, unknown> = {
    ...(useWeb ? { tools: [{ google_search: {} }] } : {}),
    systemInstruction: { parts: [{ text: SYSTEM + '\n\nFOYDALANUVCHI HOLATI:\n' + ctx }] },
    contents: msgs,
  }
  const TIMEOUT = Number(Deno.env.get('GEMINI_TIMEOUT_MS')) || 20000
  const TTFB = Number(Deno.env.get('GEMINI_TTFB_MS')) || 9000 // oqimda birinchi bayt shu vaqtda kelmasa, keyingi modelga o'tamiz
  let models: string[] = []
  try { models = await candidates(key) } catch (_e) { /* ro'yxat olinmasa, quyida xabar beramiz */ }
  if (!models.length) return json({ error: 'Mos Gemini modeli topilmadi. Kalitni va GEMINI_MODEL secretini tekshiring.' }, 502)

  let lastErr = ''
  let rate: Rate | null = null
  const att: string[] = []
  for (let pass = 0; pass < 2; pass++) {
  for (const model of ordered(models)) {
    const ctl = new AbortController()
    const to = setTimeout(() => ctl.abort(), (b.stream && !useWeb) ? Math.min(TIMEOUT, TTFB) : TIMEOUT) // qotib qolgan so'rovni to'xtatib, keyingi modelga o'tamiz
    const tg = Date.now()
    let r: Response
    try {
      r = await callGemini(model, key, base, !!b.stream && !useWeb, ctl.signal)
    } catch (_e) {
      const ms = Date.now() - tg; clearTimeout(to); lastErr = `${model}: ${Math.round(ms / 1000)} soniyada javob bermadi`; att.push(`${model}:timeout${ms}`); slowFor(model, 600000); continue
    }
    const th = THINK[OKT[model] ?? 0]
    const timing = `auth=${tAuth - t0},db=${tDb - tAuth},gemini=${Date.now() - tg},model=${model},think=${th ? Object.values(th)[0] : 'default'}`
    if (!r.ok) {
      clearTimeout(to)
      const j = await r.json().catch(() => ({}))
      lastErr = j?.error?.message || ('HTTP ' + r.status); att.push(`${model}:http${r.status}`)
      if (r.status === 429) slowFor(model, 300000)
      if (r.status === 429) { const q = quotaMsg(j); if (!q.zero || !rate) rate = q; continue } // har bir modelning o'z limiti bor: keyingisini sinaymiz
      if (r.status === 400 && /API key/i.test(lastErr)) return json({ error: 'Gemini kaliti noto‘g‘ri.' }, 500)
      continue // boshqa xatolarda (404 ham) keyingi modelga o'tamiz
    }

    GOOD.m = model; att.push(`${model}:ok${Date.now() - tg}`)
    const attS = ',att=' + att.map((x) => x.replace(/^gemini-/, '')).join('|')
    if (b.stream && !useWeb) {
      clearTimeout(to)
      // Javobni bo'lak-bo'lak (tayyor bo'lgan zahoti) yuboramiz
      const enc = new TextEncoder(), dec = new TextDecoder()
      const stream = new ReadableStream({
        async start(controller) {
          const reader = r.body!.getReader()
          let buf = '', any = false
          try {
            while (true) {
              const { done, value } = await reader.read()
              if (done) break
              buf += dec.decode(value, { stream: true })
              let idx
              while ((idx = buf.indexOf('\n')) >= 0) {
                const line = buf.slice(0, idx).trim(); buf = buf.slice(idx + 1)
                if (!line.startsWith('data:')) continue
                const data = line.slice(5).trim()
                if (!data || data === '[DONE]') continue
                try {
                  const j = JSON.parse(data)
                  const tx = (j.candidates?.[0]?.content?.parts || []).filter((x: any) => !x.thought).map((x: any) => x.text || '').join('')
                  if (tx) { any = true; controller.enqueue(enc.encode(tx)) }
                } catch { /* tugallanmagan qator */ }
              }
            }
          } catch (_e) {
            controller.enqueue(enc.encode('\n[Aloqa uzildi]'))
          }
          controller.close()
          if (any) await db.from('ai_usage').upsert({ user_id: u.user.id, day, n: used + 1 })
        },
      })
      return new Response(stream, { headers: { ...cors, 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store', 'X-Model': model, 'X-Timing': timing + attS } })
    }

    const j = await r.json().catch(() => ({}))
    clearTimeout(to)
    const text = (j.candidates?.[0]?.content?.parts || []).filter((x: any) => !x.thought).map((x: any) => x.text || '').join('').trim()
    if (!text) { lastErr = 'Bo‘sh javob keldi'; att[att.length - 1] = `${model}:empty`; continue }
    await db.from('ai_usage').upsert({ user_id: u.user.id, day, n: used + 1 })
    const sources = (j.candidates?.[0]?.groundingMetadata?.groundingChunks || [])
      .map((c: any) => ({ t: String(c?.web?.title || '').slice(0, 90), u: String(c?.web?.uri || '') })).filter((x: any) => x.u).slice(0, 6)
    return json({ text, model, timing: timing + attS, sources, left: isOwner ? null : Math.max(0, DAILY_LIMIT - used - 1) })
  }
  // Qisqa daqiqalik limitda bir marta kutib, qayta uriniladi (javob boshlanmagan bo'lsa)
  const cur = rate as Rate | null
  if (!cur || cur.zero || cur.msg.includes('Bugungi') || cur.wait > 25 || pass === 1) break
  await sleep(Math.max(cur.wait, 8) * 1000 + 400); rate = null
  }
  const fr = rate as Rate | null
  if (fr) return json({ error: fr.msg, retry: fr.wait, detail: fr.detail }, 429)
  return json({ error: 'AI javob bera olmadi: ' + lastErr + (att.length > 1 ? ' [' + att.join('; ') + ']' : '') }, 502)
})
