# वाचक · Vachak

**Live app: https://vachak.vercel.app/**

Open a Hindi, Sanskrit or English PDF and listen to it in a natural voice. Click any line to start reading from it.
Installable on **iOS, Android, Mac and Windows**; works offline; handles PDFs of 2,000+ pages (pages are read lazily).

- Repairs legacy-font Devanagari (e.g. Gita Press scans with embedded text) into proper Unicode.
- Bhagavad Gita (701 slokas) built in.
- **Natural voice pack** (Piper neural voices, run fully in the browser) downloaded once inside the app, then offline.
- **Story shelf**: 22 Hindi and English stories (moral, motivational, bedtime), grouped as long night reads, break-time stories and quick stories. Stories read page by page, like the Gita, with no chapter headings.
- **Seek bar**: a draggable progress dot on the player. Tap or drag to jump to any page or line and playback continues from there.
- Compact (Spotify-style) or full player, with scrolling titles and a voice/speed popover.
- 11 flat, three-colour themes (background, text, detail), e.g. Cocoa, Oat, Racing, Tamra, each in light and dark (or follow system). Platform-shaped UI: iPhone, Android, Windows, Mac (Settings > Interface style to preview).
- Optional setting to keep reading when the phone screen is locked.

## Deploy (GitHub Pages)

1. Create a repo, push this folder, Settings > Pages > Source: **GitHub Actions**.
2. The workflow in `.github/workflows/pages.yml` downloads the voice files at deploy time (`scripts/fetch-voices.mjs`) and publishes the site.
3. Open the Pages URL on a phone/computer and use **Install app** (iOS: Share > Add to Home Screen).

## Run locally

    python3 -m http.server 8000     # then open http://localhost:8000

Voices are only present after running `node scripts/fetch-voices.mjs`.

## Rebuild after editing

Edit `src/app.src.html`, then `python3 -I src/palettes.py && python3 -I src/stories.py && python3 -I src/build.py` (writes `index.html`).

## Notes and limits

- Scanned (image-only) PDFs have no text; OCR is not included.
- iOS Safari pauses audio when the screen locks unless the app is installed to the Home Screen.
- Check the licence of each Piper voice you ship (see `voices/README.md`).
- Libraries: PDF.js (Apache-2.0), piper-tts-web / onnxruntime-web (MIT).

## Security notes

- A strict Content-Security-Policy (script hashes, no `eval`, no third-party scripts) is embedded in `index.html` by `src/build.py`; the page also refuses to render inside a frame.
- PDFs are parsed with `isEvalSupported: false` (mitigates CVE-2024-4367 in the bundled PDF.js 3.11) and every piece of PDF text is HTML-escaped before display.
- Files never leave the device. Only the optional Google Cloud voice sends text (with your own API key) to Google; restrict that key to this site's address in Google Cloud.
- Voice names and file paths from the voice list are validated before use.

## Adding stories or another language

Stories live in `src/stories.py`, `src/stories_long.py` and `src/stories_night.py` (one `book(...)` call each, with a `lang` code). Write paragraphs in order; they are split into pages automatically. Start a closing paragraph with `सीख:` or `Moral:` to style it as the moral. Run `python3 -I src/stories.py && python3 -I src/build.py`. A new `lang` code gets its own shelf tab automatically; add its display name to `LNAME` in `src/app.src.html`.

## Author

Created and maintained by **Jiten Kumar**, AI/ML Engineer and Data Scientist, Hyderabad, India.
GitHub: [Jiten28](https://github.com/Jiten28) · Live app: https://vachak.vercel.app/ · Repository: https://github.com/Jiten28/Vachak

The stories on the shelf are original retellings written for this project. Please keep this credit if you fork or reuse the project.
