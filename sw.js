// Kunlik tizim: offline ishlash uchun service worker
const C = 'trk-v1';
const SHELL = ['./', 'index.html', 'favicon.svg', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(C).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((ks) => Promise.all(ks.filter((k) => k !== C).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const r = e.request, u = new URL(r.url);
  if (r.method !== 'GET' || u.hostname.endsWith('supabase.co')) return;
  // Ilovaning o‘z fayllari: avval internet (yangi versiya), bo‘lmasa keshdan
  if (u.origin === location.origin) {
    e.respondWith(
      fetch(r)
        .then((res) => { const cp = res.clone(); caches.open(C).then((c) => c.put(r, cp)); return res; })
        .catch(() => caches.match(r).then((m) => m || caches.match('index.html')))
    );
    return;
  }
  // Tashqi kutubxona va shriftlar: avval keshdan
  if (/jsdelivr|googleapis|gstatic/.test(u.hostname)) {
    e.respondWith(
      caches.match(r).then((m) => m || fetch(r).then((res) => { const cp = res.clone(); caches.open(C).then((c) => c.put(r, cp)); return res; }))
    );
  }
});
