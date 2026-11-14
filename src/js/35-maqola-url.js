// ---- Havoladan maqola/transkript olish (server sahifani o'qiydi; matn tekshirish uchun formaga tushadi) ----
async function ieUrlGet(){const u=(V('mu')||'').trim(),st=document.getElementById('mus');if(!u){toast('Havolani kiriting.');return}if(st)st.textContent='Olinmoqda…';
  try{const d=await fnPost({action:'article',url:u},40000);if(!d||!d.text)throw new Error('Matn kelmadi.');const t=document.getElementById('mt'),x=document.getElementById('mx');if(t&&!t.value.trim())t.value=String(d.title||d.host||'').slice(0,80);if(x)x.value=d.text;
    if(st)st.textContent='✓ '+d.host+' sahifasidan '+d.chars+' belgi olindi. Tekshirib, “Saqlash va ochish” ni bos. Faqat shaxsiy o‘qish uchun.'}
  catch(e){if(st)st.textContent='';toast(String(e.message||e).slice(0,160))}}
