// Kunlik tizim: offline ishlash uchun service worker
const C = 'trk-v2';
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
  // Mushaf matni va shriftlari (katta, o‘zgarmaydi): avval keshdan, bo‘lmasa internetdan
  if (u.origin === location.origin && /\/(fonts|data)\//.test(u.pathname)) {
    e.respondWith(
      caches.match(r).then((m) => m || fetch(r).then((res) => { if (res.ok) { const cp = res.clone(); caches.open(C).then((c) => c.put(r, cp)); } return res; }))
    );
    return;
  }
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

// Bildirishnomalar (push)
self.addEventListener('push', (e) => {
  let d = { title: 'Kunlik tizim', body: '' };
  try { d = e.data.json(); } catch (x) {}
  e.waitUntil(self.registration.showNotification(d.title, { body: d.body, icon: 'icon-192.png', badge: 'icon-192.png', tag: d.title }));
});
self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  e.waitUntil(clients.matchAll({ type: 'window', includeUncontrolled: true }).then((l) => {
    for (const c of l) { if ('focus' in c) return c.focus(); }
    return clients.openWindow('./');
  }));
});
