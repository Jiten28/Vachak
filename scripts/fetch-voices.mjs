// Downloads the natural Hindi and English voices into ./voices so they ship with the app.
// Runs automatically in the GitHub Pages workflow. Run it yourself with: node scripts/fetch-voices.mjs
// Optional: VOICES="hi_IN-priyamvada-medium,en_US-lessac-medium" node scripts/fetch-voices.mjs
import { mkdir, writeFile, access } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HF = 'https://huggingface.co/rhasspy/piper-voices/resolve/main/';
const OUT = join(dirname(fileURLToPath(import.meta.url)), '..', 'voices');
const exists = (p) => access(p).then(() => true, () => false);

const all = await (await fetch(HF + 'voices.json')).json();
const ok = (k) => all[k] && !['x_low', 'low'].includes(all[k].quality);
let want = (process.env.VOICES || '').split(',').map((s) => s.trim()).filter(Boolean);
if (!want.length) {
  const hi = Object.keys(all).filter((k) => k.startsWith('hi_IN-') && ok(k));
  const pref = ['hi_IN-priyamvada-medium', 'hi_IN-pratham-medium'].filter((k) => hi.includes(k));
  want = (pref.length ? pref : hi.slice(0, 2));
  const en = ['en_US-lessac-medium', 'en_GB-alba-medium'].find((k) => all[k]) || Object.keys(all).find((k) => k.startsWith('en_') && ok(k));
  if (en) want.push(en);
}
if (!want.length) throw new Error('No voices found. Is huggingface.co reachable?');

const catalog = {};
for (const id of want) {
  const v = all[id];
  if (!v) { console.warn('Skipping unknown voice', id); continue; }
  catalog[id] = v;
  for (const rel of Object.keys(v.files)) {
    if (!/\.(onnx|onnx\.json)$/.test(rel)) continue;
    const dest = join(OUT, rel);
    if (await exists(dest)) { console.log('have', rel); continue; }
    console.log('get ', rel);
    const r = await fetch(HF + rel);
    if (!r.ok) throw new Error(rel + ' -> ' + r.status);
    await mkdir(dirname(dest), { recursive: true });
    await writeFile(dest, Buffer.from(await r.arrayBuffer()));
  }
}
await mkdir(OUT, { recursive: true });
await writeFile(join(OUT, 'voices.json'), JSON.stringify(catalog));
console.log('Voices ready:', Object.keys(catalog).join(', '));
