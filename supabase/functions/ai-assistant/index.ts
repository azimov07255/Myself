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
FAQAT shu JSON ko'rinishida javob ber: {"level":"B2","topic":"...","words":[{"w":"lemma","f":"matndagi shakli","pos":"n","lv":"B1","def":"...","uz":"...","ctx":"...","ex":"..."}],"chunks":[{"p":"...","k":"collocation","lv":"B2","def":"...","uz":"...","ctx":"...","ex":"..."}],"grammar":[{"p":"...","g":"Third conditional","lv":"C1","def":"...","uz":"...","ctx":"...","ex":"..."}]}
Qoidalar: 1) "words": IELTS uchun foydali so'zlar, eng ko'pi 12 ta. Har birining CEFR darajasi "lv": B1, B2, C1 yoki C2. So'rovdagi "daraja" dan past darajali so'zlarni kiritma. Juda oddiy so'zlar, xos otlar, raqamlar va "known" ro'yxatidagi so'zlarni kiritma. "w" - so'zning asosiy shakli (lemma), "f" - matnda uchragan aniq shakli, "pos" - n, v, adj yoki adv. 2) "chunks": matnda aynan uchraydigan foydali iboralar (collocation, phrasal, idiom yoki phrase), eng ko'pi 6 ta; "p" 2-5 so'zdan iborat bo'lsin; "k" - collocation, phrasal, idiom yoki phrase; "lv" - B1, B2, C1 yoki C2. 3) "grammar": matnda aynan uchraydigan foydali grammatik tuzilmalar (shart gaplar, majhul nisbat, inversiya, ergash gaplar, reported speech, modal perfect, taqqoslash, cleft gaplar va h.k.), eng ko'pi 4 ta. "p" - tuzilmani ko'rsatadigan, matndan AYNAN ko'chirilgan 3-10 so'zli parcha; "g" - tuzilma nomi inglizcha (4 so'zgacha); "lv" - B1, B2, C1 yoki C2; "def" - qoida yoki formula sodda ingliz tilida (masalan: If + past perfect, would have + V3); "uz" - 12 so'zgacha o'zbekcha izoh. Oddiy tuzilmalarni (masalan present simple) kiritma. 4) "f" va "p" matnda AYNAN mavjud bo'lsin (katta-kichik harf farqi muhim emas). "ctx" - matndan aynan ko'chirilgan bitta gap. Matnda yo'q so'z, ibora yoki tuzilmani O'YLAB TOPMA. 5) "def" - sodda ingliz tilida ta'rif (14 so'zgacha). "uz" - qisqa (1-4 so'z; grammarda 12 so'zgacha) va aniq o'zbek (lotin) tilidagi ma'no; ishonching komil bo'lmasa bo'sh qoldir (""). "ex" - matndagidan farqli, yangi, sodda misol gap (18 so'zgacha). 6) "level" - matnning umumiy CEFR darajasi (B1, B2, C1 yoki C2), "topic" - ingliz tilida 2-4 so'zli mavzu. 7) Hech qanday izoh, markdown yoki \`\`\` qo'shma, faqat JSON.`

const VOCAB_DEFINE_SYSTEM = `Sen IELTS o'qituvchisisan. Berilgan inglizcha so'z yoki ibora va u uchragan gap bo'yicha FAQAT shu JSON ko'rinishida javob ber: {"w":"asosiy shakli","pos":"n","lv":"C1","def":"...","uz":"...","ex":"..."}
Qoidalar: "def" - shu gapdagi ma'noga mos sodda ingliz tilida ta'rif (14 so'zgacha). "uz" - qisqa (1-4 so'z) o'zbek (lotin) tilidagi ma'no; ishonching komil bo'lmasa "". "ex" - yangi, sodda misol gap (18 so'zgacha). "lv" - B1, B2, C1 yoki C2. Hech qanday izoh yoki markdown qo'shma.`

const READING_SYSTEM = `Sen IELTS Academic Reading materiallari yozuvchisisan. FAQAT shu JSON ko'rinishida javob ber: {"title":"...","passage":"...","questions":[{"t":"tfng","q":"...","a":"TRUE","why":"..."},{"t":"mcq","q":"...","o":["...","...","...","..."],"a":"B","why":"..."},{"t":"gap","q":"... ____ ...","a":"...","why":"..."}],"used":["..."]}
Qoidalar: 1) "passage" - ORIGINAL, o'zing yozgan akademik matn: 220-320 so'z, 3-4 paragraf (paragraflar bo'sh qator bilan ajratilgan), berilgan "band" darajasiga mos. Mavjud mashhur matndan ko'chirma qilma. 2) Aniq 8 ta savol: 3 ta "tfng" (a: TRUE, FALSE yoki NOT GIVEN), 3 ta "mcq" (4 ta variant, a: A, B, C yoki D harfi), 2 ta "gap" (matndagi gapni to'ldirish; javob matnda AYNAN uchraydigan 1-2 so'z). 3) Har bir javob matndan aniq tekshirilsin. NOT GIVEN faqat matnda umuman aytilmagan da'vo uchun, FALSE - matnga zid da'vo uchun. 4) "so'zlar" ro'yxati berilsa, ularning har birini matnda tabiiy ishlat va ishlatganlaringni "used" ga yoz. 5) "why" - qisqa o'zbekcha izoh, matndan dalil bilan (25 so'zgacha). 6) Bahsli siyosiy yoki diniy da'volardan qoch. 7) Hech qanday izoh, markdown qo'shma, faqat JSON.`

const VOCAB_CHECK_SYSTEM = `Sen IELTS o'qituvchisisan. O'quvchi berilgan inglizcha so'z yoki iborani gapda ishlatdi. Uni to'g'ri va tabiiy ishlatganini tekshir. FAQAT shu JSON ko'rinishida javob ber: {"ok":true,"fix":"...","better":"...","note":"..."}
Qoidalar: "ok" - so'z ma'nosi, grammatikasi va kollokatsiyasi to'g'ri bo'lsa true, aks holda false. "fix" - agar ok false bo'lsa, o'quvchi gapining to'g'rilangan varianti (o'quvchining fikrini saqlagan holda), aks holda "". "better" - shu so'z saqlangan, tabiiyroq va band 7+ darajadagi variant. "note" - 1-2 gap sodda o'zbek (lotin) tilida: nima to'g'ri yoki xato, qaysi kollokatsiya yoki predlog kerak. Hech qanday markdown qo'shma.`

const COACH_SYSTEM = `Sen foydalanuvchining shaxsiy haftalik murabbiyisan (IELTS, Qur'on hifzi va kundalik odatlar). Foydalanuvchining oxirgi 7 kunlik JSON ma'lumoti beriladi. FAQAT shu JSON ko'rinishida javob ber: {"summary":"...","wins":["..."],"focus":[{"t":"...","why":"..."}],"week":[{"d":"Du","tasks":["..."]}],"tip":"..."}
Qoidalar: 1) "summary" - 2 gap: o'tgan haftaning haqiqiy holati, ma'lumotga tayanib va raqamlar bilan. 2) "wins" - 2-3 ta aniq yutuq (faqat ma'lumotda bor narsa). 3) "focus" - aynan 3 ta ustuvor yo'nalish: "t" - qisqa nom, "why" - ma'lumotdagi raqam bilan sabab. 4) "week" - aynan 7 kun, "kunlar" ro'yxatidagi tartibda; "d" - shu ro'yxatdagi kun nomi. Har kunga 2-3 ta aniq, vaqti ko'rsatilgan vazifa (masalan "IELTS lug'at: 15 daqiqa"). Vazifalar "kunlik_maqsad_xp" dan oshib ketmasin; "yengil_kun" bo'lsa kam va yengil bo'lsin. 5) Faqat berilgan ma'lumotga tayan: yo'q ma'lumotni o'ylab topma; ma'lumoti yo'q bo'lim uchun "birinchi qadam" taklif qil. 6) Qur'on yodlash bo'yicha faqat reja (necha bet, qachon takror) taklif qil, diniy hukm berma. Tibbiy maslahat berma. 7) "tip" - bitta mehribon rag'batlantiruvchi gap (140 belgigacha). 8) O'zbek (lotin) tilida yoz, hech qanday markdown yoki izoh qo'shma.`

const FOOD_SYSTEM = `Sen ovqat va kaloriya tahlilchisisan. Foydalanuvchi ovqat nomini yozadi yoki rasmini yuboradi (o'zbek, rus va xalqaro taomlar). Rasmdagi har bir ovqatni alohida aniqla, porsiyani ko'zda chamala. Matnda gramm yoki dona ko'rsatilgan bo'lsa, shunga tayan.
FAQAT JSON qaytar, boshqa matn yozma:
{"items":[{"name":"taom nomi (o'zbekcha)","grams":son,"kcal":son,"p":oqsil_gramm,"f":yog_gramm,"c":uglevod_gramm}],"note":"qisqa izoh, natija taxminiy ekanini ayt"}
Raqamlar butun son bo'lsin. Ovqat tanib bo'lmasa, items bo'sh ro'yxat va note ichida sababini yoz.`
const IELTS_SYSTEM = `Sen tajribali va halol IELTS examiner'san (British Council va IDP mezonlari). Foydalanuvchi o'zbek, shuning uchun tushuntirishlarni sodda o'zbek tilida (lotin yozuvi) yoz, lekin inglizcha misollar, tuzatishlar va qayta yozilgan matnni inglizcha qoldir.
Ballarni real va qat'iy qo'y: ko'pchilik o'quvchi 5.5 dan 7.0 gacha oraliqda bo'ladi, maqtab yuborma. Band 0.5 qadam bilan.
FAQAT JSON qaytar, boshqa matn yozma:
{"band":6.5,"words":0,"transcript":"(faqat speaking uchun: audiodan so'zma-so'z matn)","criteria":[{"k":"mezon nomi","b":6.5,"n":"1-2 gaplik izoh"}],"errors":[{"o":"matndan aynan xato ibora","c":"to'g'rilangani","w":"nima uchun xato, qisqa o'zbekcha","t":"grammar"}],"strengths":["..."],"improve":["eng muhim 3-4 ta aniq maslahat"],"better":"eng zaif qismning yoki butun javobning band 8 darajasidagi inglizcha varianti","vocab":[{"w":"foydali so'z yoki ibora","m":"o'zbekcha ma'no"}]}
Writing mezonlari: Task 1 uchun "Task Achievement", Task 2 uchun "Task Response", keyin "Coherence & Cohesion", "Lexical Resource", "Grammatical Range & Accuracy". Speaking mezonlari: "Fluency & Coherence", "Lexical Resource", "Grammatical Range & Accuracy", "Pronunciation" (talaffuzni audiodan imkon qadar baho ber va bu taxminiy ekanini ayt).
errors ro'yxatiga 4 dan 10 gacha eng muhim xatoni yoz (grammatika, so'z tanlash, kollokatsiya, imlo). Har bir xatoda "t" - xato turi, FAQAT shu qiymatlardan biri: grammar, vocab, collocation, spelling, other. vocab: 5-8 ta band 7+ so'z yoki ibora.
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

// ---- Linkdan maqola olish (SSRF himoyasi: faqat ochiq veb-sahifalar, yo'naltirish va hajm cheklangan) ----
class ArtErr extends Error { status: number; constructor(m: string, s: number) { super(m); this.status = s } }
function articleBadHost(h: string): boolean {
  const x = h.toLowerCase().replace(/\.$/, '')
  if (!x.includes('.') || x.includes(':') || x.startsWith('[') || /^\d+\.\d+\.\d+\.\d+$/.test(x)) return true   // IP manzillar va nuqtasiz nomlar
  return /(^|\.)(localhost|local|internal|lan|home|corp|intranet|test|invalid)$/.test(x)
}
function privateIp(ip: string): boolean {
  const m = ip.match(/^(\d+)\.(\d+)\.(\d+)\.(\d+)$/)
  if (m) { const a = +m[1], b = +m[2]; return a === 10 || a === 127 || a === 0 || (a === 169 && b === 254) || (a === 172 && b >= 16 && b <= 31) || (a === 192 && b === 168) || (a === 100 && b >= 64 && b <= 127) || a >= 224 }
  const v = ip.toLowerCase(); return v === '::1' || v === '::' || v.startsWith('fc') || v.startsWith('fd') || v.startsWith('fe8') || v.startsWith('fe9') || v.startsWith('fea') || v.startsWith('feb')
}
async function resolvesPrivate(host: string): Promise<boolean> {
  try {
    const d: any = (globalThis as any).Deno
    if (!d || typeof d.resolveDns !== 'function') return false
    for (const t of ['A', 'AAAA']) { try { const r: string[] = await d.resolveDns(host, t); if (r.some(privateIp)) return true } catch (_e) { /* yozuv yo'q */ } }
  } catch (_e) { /* qo'llab-quvvatlanmaydi */ }
  return false
}
async function fetchArticlePage(start: URL): Promise<{ html: string; url: string }> {
  let cur = start
  for (let hop = 0; hop < 4; hop++) {
    if (!/^https?:$/.test(cur.protocol) || cur.username || cur.password || articleBadHost(cur.hostname) || await resolvesPrivate(cur.hostname)) throw new ArtErr('Bu havola ruxsat etilmagan (faqat ochiq veb-sahifalar).', 400)
    const ctl = new AbortController(); const to = setTimeout(() => ctl.abort(), 12000)
    let r: Response
    try { r = await fetch(cur.toString(), { redirect: 'manual', signal: ctl.signal, headers: { 'User-Agent': 'Mozilla/5.0 (compatible; KunlikTizim/1.0)', Accept: 'text/html,application/xhtml+xml,text/plain;q=0.9' } }) }
    catch (_e) { clearTimeout(to); throw new ArtErr('Sahifa ochilmadi yoki juda sekin javob berdi.', 504) }
    clearTimeout(to)
    if (r.status >= 300 && r.status < 400) { const loc = r.headers.get('location'); if (!loc) throw new ArtErr('Sahifa noto‘g‘ri yo‘naltirdi.', 502); try { cur = new URL(loc, cur) } catch (_e) { throw new ArtErr('Sahifa noto‘g‘ri yo‘naltirdi.', 502) } continue }
    if (!r.ok) throw new ArtErr(r.status === 404 ? 'Sahifa topilmadi (404).' : (r.status === 401 || r.status === 403) ? 'Sahifa kirishni rad etdi (yopiq yoki pullik).' : 'Sahifa xatosi: HTTP ' + r.status, 502)
    const ct = (r.headers.get('content-type') || '').toLowerCase()
    if (ct && !/text\/(html|plain)|application\/xhtml/.test(ct)) throw new ArtErr('Bu havola matnli sahifa emas (PDF, rasm yoki fayl).', 415)
    const rd = r.body ? r.body.getReader() : null; const chunks: Uint8Array[] = []; let n = 0
    if (rd) { for (;;) { const { done, value } = await rd.read(); if (done) break; if (value) { chunks.push(value); n += value.length; if (n > 1500000) { try { await rd.cancel() } catch (_e) { /* */ } break } } } }
    const all = new Uint8Array(n); let o = 0; for (const c of chunks) { all.set(c, o); o += c.length }
    return { html: new TextDecoder('utf-8', { fatal: false }).decode(all), url: cur.toString() }
  }
  throw new ArtErr('Havola juda ko‘p marta yo‘naltiriladi.', 400)
}
function decEnt(s: string): string {
  return s.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#0*39;|&apos;/g, "'")
    .replace(/&rsquo;|&#8217;/g, '’').replace(/&lsquo;|&#8216;/g, '‘').replace(/&ldquo;|&rdquo;|&#8220;|&#8221;/g, '"').replace(/&ndash;|&mdash;|&#8211;|&#8212;/g, '—')
    .replace(/&#(\d+);/g, (_m, n) => String.fromCodePoint(Math.min(+n, 0x10FFFF))).replace(/&#x([0-9a-f]+);/gi, (_m, h) => String.fromCodePoint(Math.min(parseInt(h, 16), 0x10FFFF)))
}
function extractArticle(html: string): { title: string; text: string } {
  const tm = html.match(/<meta[^>]+property=["']og:title["'][^>]+content=["']([^"']+)["']/i) || html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)
  const title = decEnt(tm ? tm[1] : '').replace(/\s+/g, ' ').trim().slice(0, 120)
  const h = html.replace(/<!--[\s\S]*?-->/g, '').replace(/<(script|style|noscript|svg|iframe|form|nav|header|footer|aside|button|select|template)\b[\s\S]*?<\/\1>/gi, '')
  const pick = (tag: string) => { const m = h.match(new RegExp('<' + tag + '\\b[^>]*>([\\s\\S]*?)<\\/' + tag + '>', 'i')); return m ? m[1] : '' }
  const body = pick('article') || pick('main') || pick('body') || h
  const out: string[] = []; let prev = ''
  for (const m of body.matchAll(/<(p|h2|h3|li)\b[^>]*>([\s\S]*?)<\/\1>/gi)) {
    const tag = m[1].toLowerCase()
    const x = decEnt(m[2].replace(/<br\s*\/?>/gi, ' ').replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim()
    if (tag === 'p' ? x.length < 40 : tag === 'li' ? x.length < 60 : (x.length < 5 || x.length > 120)) continue
    if (x === prev) continue
    prev = x; out.push(x)
  }
  let text = out.join('\n\n'); if (text.length > 12000) text = text.slice(0, 12000).replace(/\s+\S*$/, '')
  return { title, text }
}

Deno.serve(async (req) => {
  const t0 = Date.now()
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors })
  const json = (o: unknown, s = 200) =>
    new Response(JSON.stringify(o), { status: s, headers: { ...cors, 'Content-Type': 'application/json' } })

  // Oddiy so'rov JSON, audio yuklash esa multipart (fayl base64 ga o'tmasin: 33% kichikroq va tezroq)
  let form: FormData | null = null
  let b: any = {}
  if (/multipart\/form-data/i.test(req.headers.get('content-type') || '')) {
    form = await req.formData().catch(() => null)
    b = form ? { action: String(form.get('action') || '') } : {}
  } else b = await req.json().catch(() => ({}))
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
  if (b.action === 'article') {   // AI emas: kunlik AI limitiga kirmaydi, lekin kirish va obuna tekshiriladi
    const raw = String(b.url || '').trim().slice(0, 500)
    let u0: URL
    try { u0 = new URL(raw) } catch (_e) { return json({ error: 'Havola noto‘g‘ri. https:// bilan boshlanadigan to‘liq havolani kiriting.' }, 400) }
    try {
      const pgx = await fetchArticlePage(u0); const ar = extractArticle(pgx.html)
      if (ar.text.length < 300) return json({ error: 'Sahifadan matn topilmadi (u JavaScript bilan yuklanadi yoki yopiq). Matnni qo‘lda nusxalab qo‘ying.' }, 422)
      return json({ title: ar.title, text: ar.text, host: new URL(pgx.url).hostname, chars: ar.text.length })
    } catch (e) { if (e instanceof ArtErr) return json({ error: e.message }, e.status); return json({ error: 'Sahifani o‘qib bo‘lmadi.' }, 502) }
  }
  const used = (us.data as any)?.n || 0
  if (!isOwner && used >= DAILY_LIMIT) return json({ error: `Bugungi limit tugadi (${DAILY_LIMIT} ta so‘rov). Ertaga davom etamiz.` }, 429)

  // Audiodan transkript (Groq Whisper, bepul tarif): jumlalar va HAR BIR SO'ZNING vaqti
  if (b.action === 'transcript') {
    const gk = Deno.env.get('GROQ_API_KEY')
    if (!gk) return json({ error: 'Transkript uchun GROQ_API_KEY sozlanmagan. console.groq.com da bepul kalit oling va Supabase → Edge Functions → Secrets ga GROQ_API_KEY nomi bilan qo‘shing.', code: 'nokey' }, 501)
    const f = form ? form.get('file') : null
    if (!f || typeof f === 'string') return json({ error: 'Audio fayl topilmadi.' }, 400)
    const file = f as File
    if (file.size < 2000) return json({ error: 'Audio fayl juda kichik.' }, 400)
    if (file.size > 24 * 1048576) return json({ error: 'Audio 24 MB dan katta (bepul tarif chegarasi 25 MB). Qisqaroq yoki kichikroq hajmdagi audio tanlang.' }, 413)
    const fd = new FormData()
    fd.append('file', file, file.name || 'audio.mp3')
    fd.append('model', 'whisper-large-v3-turbo')
    fd.append('response_format', 'verbose_json')
    fd.append('timestamp_granularities[]', 'word')
    fd.append('timestamp_granularities[]', 'segment')
    fd.append('language', 'en')
    fd.append('temperature', '0')
    const ctl = new AbortController(); const to = setTimeout(() => ctl.abort(), 110000)
    let gr: Response
    try { gr = await fetch('https://api.groq.com/openai/v1/audio/transcriptions', { method: 'POST', headers: { Authorization: 'Bearer ' + gk }, body: fd, signal: ctl.signal }) }
    catch (_e) { clearTimeout(to); return json({ error: 'Transkript vaqti tugadi yoki Groq bilan ulanib bo‘lmadi. Qisqaroq audio bilan urinib ko‘ring.' }, 504) }
    clearTimeout(to)
    const gj: any = await gr.json().catch(() => ({}))
    if (!gr.ok) {
      const gm = String(gj?.error?.message || '').slice(0, 160)
      if (gr.status === 401) return json({ error: 'GROQ_API_KEY noto‘g‘ri yoki o‘chirilgan.' }, 502)
      if (gr.status === 429) return json({ error: 'Groq bepul limiti vaqtincha tugadi (soatiga/kuniga). Birozdan keyin urinib ko‘ring.' }, 429)
      if (gr.status === 413) return json({ error: 'Audio Groq uchun juda katta (25 MB gacha).' }, 413)
      return json({ error: 'Transkript xatosi: ' + (gm || ('HTTP ' + gr.status)) }, 502)
    }
    const r2 = (x: unknown) => Math.round(Number(x) * 100) / 100
    const segs: any[] = Array.isArray(gj.segments) ? gj.segments : []
    const words: any[] = Array.isArray(gj.words) ? gj.words : []
    let cues = segs.map((sg: any) => {
      const s = Number(sg.start) || 0, e = Number(sg.end) || s
      return {
        s: r2(s), e: r2(e), t: String(sg.text || '').replace(/\s+/g, ' ').trim(),
        w: words.filter((w: any) => Number(w.start) >= s - 0.15 && Number(w.start) < e + 0.05).slice(0, 90)
          .map((w: any) => [String(w.word || '').slice(0, 40), r2(w.start), r2(w.end)]),
      }
    }).filter((c) => c.t)
    if (!cues.length && String(gj.text || '').trim()) cues = [{ s: 0, e: r2(gj.duration), t: String(gj.text).trim(), w: [] }]
    if (!cues.length) return json({ error: 'Audioda nutq topilmadi.' }, 422)
    await db.from('ai_usage').upsert({ user_id: u.user.id, day, n: used + 1 })
    return json({ cues: cues.slice(0, 800), dur: r2(gj.duration), lang: String(gj.language || 'en') })
  }

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

  if (b.action === 'food' || b.action === 'transcribe' || b.action === 'ielts' || b.action === 'plan' || b.action === 'dayplan' || b.action === 'vocab' || b.action === 'reading' || b.action === 'coach') {
    const list = await candidates(key).catch(() => [] as string[])
    if (!list.length) return json({ error: 'Mos Gemini modeli topilmadi.' }, 502)
    const parts: unknown[] = []
    let system = FOOD_SYSTEM
    let extra: Record<string, unknown> = { responseMimeType: 'application/json', maxOutputTokens: 1500 }
    let tmo = 30000
    if (b.action === 'coach') {
      const cx = String(b.ctx || '').trim()
      if (cx.length < 20) return json({ error: 'Murabbiy uchun ma‘lumot yo‘q.' }, 400)
      if (cx.length > 9000) return json({ error: 'Ma‘lumot juda katta.' }, 400)
      tmo = 45000; system = COACH_SYSTEM; extra = { responseMimeType: 'application/json', maxOutputTokens: 3500 }
      parts.push({ text: 'Ma‘lumotlar (JSON):\n' + cx })
    } else if (b.action === 'reading') {
      const topic = String(b.topic || '').trim().slice(0, 80) || 'a current academic topic'
      const band = Math.min(9, Math.max(5, Number(b.band) || 7))
      const words = (Array.isArray(b.words) ? b.words : []).slice(0, 8).map((x: unknown) => String(x).replace(/[^\p{L}' -]/gu, '').slice(0, 30)).filter(Boolean)
      tmo = 48000; system = READING_SYSTEM; extra = { responseMimeType: 'application/json', maxOutputTokens: 5000 }
      parts.push({ text: 'Mavzu: ' + topic + '\nband: ' + band + '\nso\'zlar: ' + (words.length ? words.join(', ') : '(berilmagan)') })
    } else if (b.action === 'vocab') {
      if (b.mode === 'check') {
        const w = String(b.word || '').trim().slice(0, 40), s = String(b.sentence || '').trim().slice(0, 300)
        if (!w) return json({ error: 'So‘z yozilmagan.' }, 400)
        if (s.length < 8) return json({ error: 'Gap juda qisqa.' }, 400)
        system = VOCAB_CHECK_SYSTEM; extra = { responseMimeType: 'application/json', maxOutputTokens: 700 }
        parts.push({ text: 'So‘z yoki ibora: ' + w + '\nO‘quvchining gapi: ' + s })
      } else if (b.mode === 'define') {
        const w = String(b.word || '').trim().slice(0, 80), c = String(b.ctx || '').trim().slice(0, 300)
        if (!w) return json({ error: 'So‘z yozilmagan.' }, 400)
        system = VOCAB_DEFINE_SYSTEM; extra = { responseMimeType: 'application/json', maxOutputTokens: 600 }
        parts.push({ text: 'So‘z yoki ibora: ' + w + '\nGap: ' + c })
      } else {
        const text = String(b.text || '').trim()
        if (text.length < 80) return json({ error: 'Matn juda qisqa.' }, 400)
        if (text.length > 4500) return json({ error: 'Matn juda uzun (4500 belgigacha).' }, 400)
        const known = (Array.isArray(b.known) ? b.known : []).slice(0, 120).map((x: unknown) => String(x).slice(0, 30)).join(', ')
        tmo = 38000; system = VOCAB_ANALYZE_SYSTEM; extra = { responseMimeType: 'application/json', maxOutputTokens: 4000 }
        const min = ['B1', 'B2', 'C1'].includes(String(b.min)) ? String(b.min) : 'B1'
        parts.push({ text: 'daraja: ' + min + ' va undan yuqori\nknown: ' + (known || '(yo‘q)') + '\n\nMATN:\n' + text })
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
