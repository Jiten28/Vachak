const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 512, height: 512 } });
  const fonts = 'file://' + path.resolve('vendor/fonts/fonts.css');
  const make = (size, { round, scale }) => `<!doctype html><link rel="stylesheet" href="${fonts}"><style>
  html,body{margin:0;background:transparent}
  .i{width:${size}px;height:${size}px;display:grid;place-items:center;position:relative;overflow:hidden;
     background:radial-gradient(90% 90% at 25% 15%, #17909E 0%, #0A5563 55%, #073A45 100%);${round ? `border-radius:${size * 0.225}px;` : ''}}
  .g{font-family:"Tiro Devanagari Hindi",serif;color:#fff;font-size:${size * 0.56 * scale}px;line-height:1;transform:translate(-${size * 0.035}px,-${size * 0.02}px)}
  .w{position:absolute;right:${size * (0.2 - (1 - scale) * 0.1)}px;top:${size * (0.26 + (1 - scale) * 0.1)}px;display:flex;gap:${size * 0.03}px;align-items:center}
  .w i{display:block;width:${size * 0.04}px;border-radius:${size}px;background:#F4C95D}
  </style><div class="i"><div class="g">व</div><div class="w"><i style="height:${size * 0.07}px"></i><i style="height:${size * 0.15}px"></i><i style="height:${size * 0.1}px"></i></div></div>`;
  const jobs = [['icon-512.png', 512, { round: true, scale: 1 }], ['icon-192.png', 192, { round: true, scale: 1 }], ['maskable-512.png', 512, { round: false, scale: 0.78 }],
                ['apple-touch-icon.png', 180, { round: false, scale: 0.9 }], ['favicon.png', 48, { round: true, scale: 1 }]];
  for (const [f, size, o] of jobs) {
    await p.setViewportSize({ width: size, height: size }); await p.setContent(make(size, o)); await p.waitForTimeout(300);
    await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: 'icons/' + f, omitBackground: true });
  }
  await b.close();
})();
