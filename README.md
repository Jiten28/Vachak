# वाचक · Vachak

Open a Hindi, Sanskrit or English PDF and listen to it in a natural voice. Click any line to start reading from it.
Installable on **iOS, Android, Mac and Windows**; works offline; handles PDFs of 2,000+ pages (pages are read lazily).

- Repairs legacy-font Devanagari (e.g. Gita Press scans with embedded text) into proper Unicode.
- Bhagavad Gita (701 slokas) built in.
- **Natural voice pack** (Piper neural voices, run fully in the browser) downloaded once inside the app, then offline.
- 8 colour themes x light/dark/system. Platform-shaped UI: iPhone, Android and desktop styles (Settings > Interface style to preview).

## Deploy (GitHub Pages)
1. Create a repo, push this folder, Settings > Pages > Source: **GitHub Actions**.
2. The workflow in `.github/workflows/pages.yml` downloads the voice files at deploy time (`scripts/fetch-voices.mjs`) and publishes the site.
3. Open the Pages URL on a phone/computer and use **Install app** (iOS: Share > Add to Home Screen).

## Run locally
    python3 -m http.server 8000     # then open http://localhost:8000
Voices are only present after running `node scripts/fetch-voices.mjs`.

## Rebuild after editing
Edit `src/app.src.html`, then `python3 src/palettes.py && python3 src/build.py` (writes `index.html`).

## Notes and limits
- Scanned (image-only) PDFs have no text; OCR is not included.
- iOS Safari pauses audio when the screen locks unless the app is installed to the Home Screen.
- Check the licence of each Piper voice you ship (see `voices/README.md`).
- Libraries: PDF.js (Apache-2.0), piper-tts-web / onnxruntime-web (MIT).
