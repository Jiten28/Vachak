/* Vachak service worker: keeps the app working offline.
   - App files are cached on install and refreshed in the background.
   - Voice files (voices/, vendor/piper/) are cached by the app itself in "vachak-voices-v1";
     this worker only serves them from there when present, so nothing is stored twice. */
const VERSION = 'v1';
const SHELL = 'vachak-shell-' + VERSION;
const PRECACHE = [
  './', 'index.html', 'manifest.webmanifest',
  'vendor/fonts/fonts.css',
  'vendor/fonts/tiro-devanagari-hindi-devanagari-400-normal.woff2',
  'vendor/fonts/tiro-devanagari-hindi-latin-400-normal.woff2',
  'vendor/fonts/tiro-devanagari-hindi-latin-ext-400-normal.woff2',
  'vendor/fonts/hanken-grotesk-latin-wght-normal.woff2',
  'vendor/fonts/hanken-grotesk-latin-ext-wght-normal.woff2',
  'vendor/pdfjs/pdf.min.js', 'vendor/pdfjs/pdf.worker.min.js',
  'icons/icon-192.png', 'icons/icon-512.png', 'icons/maskable-512.png', 'icons/apple-touch-icon.png', 'icons/favicon.png'
];
self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(SHELL).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys()
    .then((keys) => Promise.all(keys.filter((k) => k.startsWith('vachak-shell-') && k !== SHELL).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;
  if (/\/(voices|vendor\/piper)\//.test(url.pathname)) {
    e.respondWith(caches.match(req).then((hit) => hit || fetch(req)));
    return;
  }
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).then((res) => {
      if (res.ok) { const copy = res.clone(); caches.open(SHELL).then((c) => c.put('index.html', copy)); }
      return res;
    }).catch(() => caches.match('index.html').then((r) => r || caches.match('./'))));
    return;
  }
  e.respondWith(caches.match(req).then((hit) => {
    const net = fetch(req).then((res) => {
      if (res.ok && res.status === 200) { const copy = res.clone(); caches.open(SHELL).then((c) => c.put(req, copy)); }
      return res;
    }).catch(() => hit);
    return hit || net;
  }));
});
