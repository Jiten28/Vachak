import re
s=open('app.src.html',encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)

# ================= CSS =================
CSS = r"""
/* ---- sidebar toggle, marquee, popover, compact player, stories ---- */
.menu-btn { display: inline-grid; }
@media (min-width: 861px) {
  .app { transition: grid-template-columns .24s ease, gap .24s ease; }
  .app[data-rail="collapsed"] { grid-template-columns: 0 minmax(0, 1fr); gap: 0; }
  .app[data-rail="collapsed"] .rail { visibility: hidden; opacity: 0; overflow: hidden; pointer-events: none; padding: 0; }
  .rail { transition: opacity .18s ease, visibility 0s; }
}
.scrim.clear { background: transparent; }
.mq { overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.mq.run { text-overflow: clip; -webkit-mask-image: linear-gradient(90deg, #000 calc(100% - 22px), transparent); mask-image: linear-gradient(90deg, #000 calc(100% - 22px), transparent); }
.mq.run > span { display: inline-block; will-change: transform; animation: mq var(--mq-t, 8s) ease-in-out infinite alternate; }
@keyframes mq { 0%, 14% { transform: translateX(0); } 86%, 100% { transform: translateX(var(--mq-x, 0px)); } }
@media (prefers-reduced-motion: reduce) { .mq.run > span { animation: none; } .mq.run { -webkit-mask-image: none; mask-image: none; text-overflow: ellipsis; } }
.tune-btn { display: none; position: relative; }
.tune-btn[data-s="loading"]::after { content: ""; position: absolute; inset: 3px; border-radius: 50%; border: 2px solid transparent; border-top-color: var(--accent); animation: vspin .9s linear infinite; }
.tune-btn[data-s="error"]::after { content: ""; position: absolute; top: 6px; right: 6px; width: 8px; height: 8px; border-radius: 50%; background: var(--danger); }
.pop { position: fixed; z-index: 58; right: 28px; bottom: 120px; width: min(390px, calc(100vw - 24px)); max-height: min(72vh, 600px); overflow: auto; background: var(--panel); border: 1px solid var(--line); border-radius: var(--r-sheet); box-shadow: 0 22px 60px -14px rgba(0,0,0,.55); padding: 6px 16px 16px; visibility: hidden; opacity: 0; transform: translateY(10px) scale(.985); transition: opacity .16s ease, transform .16s ease, visibility 0s .16s; }
.pop.open { visibility: visible; opacity: 1; transform: none; transition-delay: 0s; }
.pop h2 { font-size: 1rem; margin: 10px 0 4px; }
.pop .grp { margin-top: 14px; }
.pop .grp-t { font-size: .72rem; letter-spacing: .09em; text-transform: uppercase; color: var(--ink-3); font-weight: 700; margin: 0 0 7px; }
.vopt { display: flex; width: 100%; align-items: center; gap: 11px; text-align: left; background: transparent; border: 1px solid var(--line); border-radius: var(--r-ctl); padding: 9px 12px; margin: 0 0 6px; min-height: 48px; position: relative; overflow: hidden; }
.vopt:hover { border-color: var(--ink-3); }
.vopt[aria-checked="true"] { border-color: var(--accent); background: var(--accent-soft); }
.vopt .rd { flex: none; width: 18px; height: 18px; border-radius: 50%; border: 2px solid var(--ink-3); }
.vopt[aria-checked="true"] .rd { border-color: var(--accent); background: radial-gradient(var(--accent) 42%, transparent 46%); }
.vopt .tt { flex: 1; min-width: 0; }
.vopt .tt b { display: block; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.vopt .tt small { color: var(--ink-2); font-size: .8rem; }
.vopt .dl { flex: none; font-size: .78rem; font-weight: 700; color: var(--accent); padding: 4px 9px; border: 1px solid var(--accent); border-radius: 99px; }
.vopt .pg { position: absolute; left: 0; bottom: 0; height: 3px; width: 0; background: var(--accent); transition: width .2s; }
.pop .row2 { display: flex; align-items: center; justify-content: space-between; gap: 10px; flex-wrap: wrap; }
.pop .foot { margin-top: 14px; display: flex; gap: 8px; flex-wrap: wrap; }
.story { display: grid; grid-template-columns: 50px minmax(0, 1fr); gap: 12px; align-items: center; width: 100%; text-align: left; padding: 10px 12px; background: var(--sheet); border: 1px solid var(--line); border-radius: var(--r-card); margin: 0 0 8px; }
.story:hover { border-color: var(--ink-3); }
.story .cv { width: 50px; height: 62px; border-radius: 6px 10px 10px 6px; display: grid; place-items: center; font-family: var(--f-read); font-size: 1.5rem; color: var(--accent-ink); background: linear-gradient(135deg, var(--accent), var(--accent-2)); box-shadow: inset 4px 0 0 rgba(0,0,0,.18); }
.story .tt b { display: block; font-weight: 700; line-height: 1.3; }
.story .tt small { display: block; color: var(--ink-2); font-size: .82rem; margin-top: 2px; }
.story .tt .meta { color: var(--ink-3); font-size: .78rem; margin-top: 4px; }
.story-h { font-weight: 400; font-size: 1.5em; line-height: 1.3; margin: 1.2em 0 .5em; text-align: left; }
.story-h:first-child { margin-top: 0; }
.seek { -webkit-appearance: none; appearance: none; background: transparent; }
.seek::-webkit-slider-runnable-track { height: 4px; border-radius: 3px; background: linear-gradient(90deg, var(--accent) var(--pct, 0%), var(--line) var(--pct, 0%)); }
.seek::-moz-range-track { height: 4px; border-radius: 3px; background: var(--line); }
.seek::-moz-range-progress { height: 4px; border-radius: 3px; background: var(--accent); }
.seek::-webkit-slider-thumb { -webkit-appearance: none; width: 14px; height: 14px; border-radius: 50%; background: var(--accent); margin-top: -5px; border: 0; }
.seek::-moz-range-thumb { width: 14px; height: 14px; border-radius: 50%; background: var(--accent); border: 0; }
.dock, .dock-row, .main { min-width: 0; }
.dock { grid-template-columns: minmax(0, 1fr); }
.now { min-width: 0; }
.now .l1, .now .l2 { max-width: 100%; }
"""
rep("@keyframes vspin { to { transform: rotate(360deg); } }", CSS + "@keyframes vspin { to { transform: rotate(360deg); } }")

# compact player + phone dock (inside a new media block placed after the main mobile block)
MOB = r"""
@media (max-width: 860px) {
  .vbadge, .field { max-width: 100%; }
  .dock-row { flex-wrap: wrap; min-width: 0; }
  :root[data-player="compact"] .dock { padding: 0 12px 6px; gap: 0; overflow: hidden; margin-bottom: 6px; }
  :root[data-player="compact"] .seek { order: -1; height: 22px; margin: 0 -12px; width: calc(100% + 24px); }
  :root[data-player="compact"] .seek::-webkit-slider-runnable-track { height: 3px; border-radius: 0; }
  :root[data-player="compact"] .seek::-webkit-slider-thumb { opacity: 0; width: 18px; height: 18px; margin-top: -7.5px; }
  :root[data-player="compact"] .seek:active::-webkit-slider-thumb { opacity: 1; }
  :root[data-player="compact"] .seek::-moz-range-thumb { opacity: 0; }
  :root[data-player="compact"] .seek { margin-top: -2px; margin-bottom: -6px; }
  :root[data-player="compact"] .dock-row { flex-wrap: nowrap; gap: 2px; align-items: center; }
  :root[data-player="compact"] .dock-row > .now { order: 0; flex: 1 1 0; min-width: 0; padding-right: 6px; }
  :root[data-player="compact"] .now .l1 { font-size: .92rem; }
  :root[data-player="compact"] .now .l2 { font-size: .76rem; }
  :root[data-player="compact"] .transport { order: 1; gap: 0; }
  :root[data-player="compact"] .transport .icon-btn { width: 38px; height: 38px; }
  :root[data-player="compact"] .play { width: 44px; height: 44px; }
  :root[data-player="compact"] .play svg { width: 20px; height: 20px; }
  :root[data-player="android"] .play, :root[data-platform="android"][data-player="compact"] .play { width: 46px; height: 46px; border-radius: 16px; }
  :root[data-player="compact"] .tune-btn { order: 2; display: inline-grid; width: 38px; height: 38px; }
  :root[data-player="compact"] .vbadge, :root[data-player="compact"] .field, :root[data-player="compact"] .toggle, :root[data-player="compact"] #voiceTip, :root[data-player="compact"] .bufbar { display: none; }
  :root[data-player="compact"] .stage { padding-bottom: 28px; }
  :root[data-player="full"] .tune-btn { display: none; }
  :root[data-player="full"] .dock-row > .now { flex: 1 1 100%; order: -1; min-width: 0; }
  :root[data-player="full"] .vbadge { flex: 1 1 auto; min-width: 0; }
}
"""
rep("@supports (height: 100dvh)", MOB + "@supports (height: 100dvh)")

# platform flavours: Windows (Fluent) and Mac
PLAT = r"""
/* Windows: Fluent-style layers, left accent bar on the selected item, command-bar buttons */
:root[data-platform="windows"] body { background: radial-gradient(900px 520px at 6% -8%, color-mix(in srgb, var(--accent) 11%, transparent), transparent 65%), radial-gradient(700px 420px at 100% 100%, color-mix(in srgb, var(--accent-2) 8%, transparent), transparent 60%), var(--bg); }
:root[data-platform="windows"] .rail { background: color-mix(in srgb, var(--panel) 72%, transparent); border: 1px solid var(--line); border-radius: 8px; padding: 12px 10px 0; }
:root[data-platform="windows"] .toc button, :root[data-platform="windows"] .lib button { border-radius: 4px; position: relative; }
:root[data-platform="windows"] .toc button:hover, :root[data-platform="windows"] .lib button:hover { background: color-mix(in srgb, var(--ink) 6%, transparent); border-color: transparent; }
:root[data-platform="windows"] .toc button[aria-current="true"] { background: color-mix(in srgb, var(--ink) 8%, transparent); color: var(--ink); }
:root[data-platform="windows"] .toc button[aria-current="true"]::before { content: ""; position: absolute; left: 0; top: 22%; bottom: 22%; width: 3px; border-radius: 2px; background: var(--accent); }
:root[data-platform="windows"] .sheet { border-radius: 8px; box-shadow: 0 1.5px 4px rgba(0,0,0,.10), 0 0 0 1px var(--line); }
:root[data-platform="windows"] .dock { border-radius: 8px; background: color-mix(in srgb, var(--panel) 84%, transparent); -webkit-backdrop-filter: blur(24px) saturate(1.4); backdrop-filter: blur(24px) saturate(1.4); box-shadow: 0 1.5px 4px rgba(0,0,0,.10), 0 0 0 1px var(--line); }
:root[data-platform="windows"] .btn { border-radius: 4px; border-bottom-color: color-mix(in srgb, var(--ink) 28%, var(--line)); font-weight: 600; }
:root[data-platform="windows"] .btn.primary { border-bottom-color: color-mix(in srgb, #000 30%, var(--accent)); }
:root[data-platform="windows"] .icon-btn { border-radius: 4px; }
:root[data-platform="windows"] .play { box-shadow: none; }
:root[data-platform="windows"] .tabs { background: transparent; border: 0; border-radius: 0; padding: 0; }
:root[data-platform="windows"] .tabs button { border-radius: 4px; position: relative; padding: 7px 14px; }
:root[data-platform="windows"] .tabs button[aria-selected="true"] { background: transparent; box-shadow: none; color: var(--ink); }
:root[data-platform="windows"] .tabs button[aria-selected="true"]::after { content: ""; position: absolute; left: 18%; right: 18%; bottom: 0; height: 3px; border-radius: 2px; background: var(--accent); }
:root[data-platform="windows"] .seg { border-radius: 4px; } :root[data-platform="windows"] .seg button { border-radius: 3px; }
:root[data-platform="windows"] .toggle input { -webkit-appearance: none; appearance: none; position: relative; width: 42px; height: 22px; border-radius: 11px; border: 1px solid var(--ink-3); background: transparent; margin: 0; cursor: pointer; transition: background .15s; }
:root[data-platform="windows"] .toggle input::after { content: ""; position: absolute; top: 4px; left: 4px; width: 12px; height: 12px; border-radius: 50%; background: var(--ink-2); transition: transform .15s, width .15s; }
:root[data-platform="windows"] .toggle input:checked { background: var(--accent); border-color: var(--accent); }
:root[data-platform="windows"] .toggle input:checked::after { background: var(--accent-ink); transform: translateX(21px); }
:root[data-platform="windows"] .toggle input:active::after { width: 16px; }
:root[data-platform="windows"] .pop, :root[data-platform="windows"] .panel { border-radius: 8px; }
:root[data-platform="windows"] ::-webkit-scrollbar { width: 12px; height: 12px; } :root[data-platform="windows"] ::-webkit-scrollbar-thumb { background: color-mix(in srgb, var(--ink) 28%, transparent); border-radius: 6px; border: 3px solid transparent; background-clip: content-box; }
/* Mac: frosted sidebar, soft segmented control, switch toggles */
:root[data-platform="mac"] .rail { background: color-mix(in srgb, var(--panel) 58%, transparent); -webkit-backdrop-filter: blur(30px) saturate(1.8); backdrop-filter: blur(30px) saturate(1.8); border: 1px solid color-mix(in srgb, var(--line) 70%, transparent); border-radius: 12px; padding: 12px 10px 0; }
:root[data-platform="mac"] .toc button, :root[data-platform="mac"] .lib button { border-radius: 7px; }
:root[data-platform="mac"] .toc button[aria-current="true"] { background: var(--accent); color: var(--accent-ink); }
:root[data-platform="mac"] .toc button[aria-current="true"] .e, :root[data-platform="mac"] .toc button[aria-current="true"] .n { color: var(--accent-ink); opacity: .85; }
:root[data-platform="mac"] .seg, :root[data-platform="mac"] .tabs { background: color-mix(in srgb, var(--ink) 9%, var(--panel)); border: 0; border-radius: 9px; padding: 2px; }
:root[data-platform="mac"] .seg button, :root[data-platform="mac"] .tabs button { border-radius: 7px; }
:root[data-platform="mac"] .seg button[aria-pressed="true"], :root[data-platform="mac"] .tabs button[aria-selected="true"] { background: var(--sheet); color: var(--ink); box-shadow: 0 1px 3px rgba(0,0,0,.25), 0 0 0 .5px rgba(0,0,0,.08); }
:root[data-platform="mac"] .dock { border-radius: 14px; background: color-mix(in srgb, var(--panel) 80%, transparent); -webkit-backdrop-filter: blur(26px) saturate(1.7); backdrop-filter: blur(26px) saturate(1.7); }
:root[data-platform="mac"] .sheet { border-radius: 12px; }
:root[data-platform="mac"] .play { box-shadow: none; }
:root[data-platform="mac"] .btn { border-radius: 8px; font-weight: 600; }
:root[data-platform="mac"] .toggle input { -webkit-appearance: none; appearance: none; position: relative; width: 40px; height: 24px; border-radius: 12px; background: color-mix(in srgb, var(--ink) 18%, transparent); border: 0; margin: 0; cursor: pointer; transition: background .2s; }
:root[data-platform="mac"] .toggle input::after { content: ""; position: absolute; top: 2px; left: 2px; width: 20px; height: 20px; border-radius: 50%; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,.35); transition: transform .2s; }
:root[data-platform="mac"] .toggle input:checked { background: var(--accent); }
:root[data-platform="mac"] .toggle input:checked::after { transform: translateX(16px); }
"""
rep("@keyframes vspin { to { transform: rotate(360deg); } }", PLAT + "@keyframes vspin { to { transform: rotate(360deg); } }")

# ================= markup =================
rep('<button class="btn quiet" id="voiceTip"','<button class="icon-btn tune-btn" id="tuneBtn" type="button" aria-label="Voice and speed" aria-haspopup="dialog" data-s="idle"><svg class="i"><use href="#i-sliders"/></svg></button>\n        <button class="btn quiet" id="voiceTip"')
rep('<div class="scrim" id="scrim"></div>','<div class="scrim" id="scrim"></div>\n<div class="pop" id="pop" role="dialog" aria-label="Voice and speed" aria-hidden="true"><span class="grab" id="grabPop" aria-hidden="true"></span><div id="popBody"></div></div>')
rep('<button type="button" id="libPaste">','<button type="button" id="libStories"><b>Story shelf</b><span id="libStoriesSub">Stories in Hindi and English</span></button>\n        <button type="button" id="libPaste">')
rep("'rateSel','autoAdv',","'rateSel','autoAdv','pop','popBody','tuneBtn','libStories','libStoriesSub','grabPop',")
rep('<div class="l1" id="nowTitle">—</div><div class="l2" id="nowSub">—</div>','<div class="l1 mq" id="nowTitle"><span>—</span></div><div class="l2 mq" id="nowSub"><span>—</span></div>')
rep("window.GITA = /*__GITA__*/;","window.GITA = /*__GITA__*/;\nwindow.STORIES = /*__STORIES__*/;")
rep("rail: store.get","rail: store.get") if False else None

# ================= state =================
rep("ui: store.get('ui', 'auto'),","ui: store.get('ui', 'auto'), player: store.get('player', 'compact'), rail: store.get('rail', 'open'),")

# ================= marquee =================
rep("function setStatus(m) {","""function setMq(node, text) {
  var sp = node.firstElementChild;
  if (!sp || sp.tagName !== 'SPAN') { node.textContent = ''; sp = document.createElement('span'); node.appendChild(sp); node.classList.add('mq'); }
  if (sp.textContent !== text) { sp.textContent = text; node.title = text; }
  fitMq(node);
}
function fitMq(node) {
  var sp = node.firstElementChild; if (!sp) return;
  node.classList.remove('run'); node.style.removeProperty('--mq-x');
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var over = Math.ceil(sp.scrollWidth - node.clientWidth);
  if (over > 6) { node.style.setProperty('--mq-x', -(over + 14) + 'px'); node.style.setProperty('--mq-t', Math.max(5, over / 26 + 3).toFixed(1) + 's'); node.classList.add('run'); }
}
function fitAllMq() { fitMq(el.nowTitle); fitMq(el.nowSub); }
window.addEventListener('resize', fitAllMq);
if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitAllMq);
function setStatus(m) {""")
rep("  el.nowTitle.textContent = DOC ? DOC.title : '—';","  setMq(el.nowTitle, DOC ? DOC.title : '—');")
# nowSub line
i=s.index("  el.nowSub.textContent = "); j=s.index("\n",i); line=s[i:j]
assert line.rstrip().endswith(';')
s=s[:i]+line.replace("el.nowSub.textContent = ","setMq(el.nowSub, ",1).rstrip()[:-1]+");"+s[j:]
rep("el.seek.max = Math.max(1, n); el.seek.value = P.page;","el.seek.max = Math.max(1, n); el.seek.value = P.page;\n  el.seek.style.setProperty('--pct', Math.min(100, ((P.page - 1 + (m && m.units.length ? Math.min(1, P.idx / m.units.length) : 0)) / Math.max(1, n)) * 100).toFixed(2) + '%');")
rep("el.seek.oninput = function () { el.pgInput.value = el.seek.value; };","el.seek.oninput = function () { el.pgInput.value = el.seek.value; el.seek.style.setProperty('--pct', ((el.seek.value - 1) / Math.max(1, el.seek.max - 1) * 100) + '%'); };")

# ================= books / stories =================
rep("function buildTextPage() {","""function buildBookPage(n) {
  var ch = DOC.book.ch[n - 1];
  var units = [{ kind: 'head', head: true, text: ch.t, speech: toSpeech(ch.t) + '।', ok: true, para: true, lines: [], gap: 900 }];
  ch.p.forEach(function (p) {
    var first = true;
    splitSentences(p).forEach(function (sp) {
      var t = p.slice(sp[0], sp[1]).trim(); if (!t) return;
      var speech = toSpeech(t);
      if (units.length && !isSpeakable(speech)) { units[units.length - 1].text += ' ' + t; return; }
      units.push({ text: t, speech: speech, ok: isSpeakable(speech), para: first, lines: [] }); first = false;
    });
  });
  return { n: n, kind: 'book', units: units, lines: [] };
}
function buildTextPage() {""")
rep("var m = DOC.kind === 'gita' ? buildGitaPage(n) : DOC.kind === 'text'","var m = DOC.kind === 'gita' ? buildGitaPage(n) : DOC.kind === 'book' ? buildBookPage(n) : DOC.kind === 'text'")
rep("      if (u.para || !open) { if (open) h += '</p>'; h += '<p>'; open = true; }\n      h += '<span class=\"u'",
    "      if (u.head) { if (open) h += '</p>'; open = false; h += '<h3 class=\"story-h\"><span class=\"u\" data-i=\"' + i + '\">' + esc(u.text) + '</span></h3>'; return; }\n      if (u.para || !open) { if (open) h += '</p>'; h += '<p>'; open = true; }\n      h += '<span class=\"u'")
rep("var unitLabel = DOC && DOC.kind === 'gita' ? 'Chapter' : 'Page';","var unitLabel = DOC && (DOC.kind === 'gita' || DOC.kind === 'book') ? 'Chapter' : 'Page';")
rep("DOC && DOC.kind === 'gita' && +b.dataset.p === P.page ? 'true'","DOC && (DOC.kind === 'gita' || DOC.kind === 'book') && +b.dataset.p === P.page ? 'true'")
rep("  } else if (DOC.kind === 'gita') chips += '<span class=\"chip\">Sanskrit</span>';","  } else if (DOC.kind === 'gita') chips += '<span class=\"chip\">Sanskrit</span>';\n  else if (DOC.kind === 'book') chips += '<span class=\"chip\">' + esc(LNAME[DOC.book.lang] || DOC.book.lang) + '</span><span class=\"chip off\">Story</span>';")
rep("var meta = DOC.kind === 'gita' ? '18 chapters · 701 slokas' :","var meta = DOC.kind === 'gita' ? '18 chapters · 701 slokas' : DOC.kind === 'book' ? DOC.pages + (DOC.pages === 1 ? ' chapter' : ' chapters') + ' · ' + esc(DOC.book.sub) :")
rep("  } else if (DOC && DOC.kind === 'pdf' && outlineItems.length) {","  } else if (DOC && DOC.kind === 'book') {\n    el.tocLabel.textContent = 'Chapters';\n    DOC.book.ch.forEach(function (c, i) { h += '<button type=\"button\" data-p=\"' + (i + 1) + '\"><span class=\"n\">' + (i + 1) + '</span><span class=\"t' + (DOC.book.lang === 'en' ? ' lat' : '') + '\" lang=\"' + esc(DOC.book.lang) + '\">' + esc(c.t) + '</span></button>'; });\n  } else if (DOC && DOC.kind === 'pdf' && outlineItems.length) {")
rep("async function openText(text) {","""var LNAME = { hi: 'हिन्दी', en: 'English', sa: 'संस्कृतम्' };
async function openBook(id, startPage) {
  var b = (window.STORIES || []).filter(function (x) { return x.id === id; })[0]; if (!b) return;
  resetDoc();
  DOC = { kind: 'book', title: b.title, pages: b.ch.length, key: 'book:' + id, legacy: false, book: b };
  setTabs(false); renderDocCard(); renderToc();
  var pos = store.get('pos.' + DOC.key, null);
  await showPage(startPage || (pos && pos.p) || 1, startPage ? 0 : (pos && pos.i) || 0);
  setPlayUI();
}
function storyMinutes(b) { var w = b.ch.reduce(function (a, c) { return a + c.p.join(' ').split(/\\s+/).length; }, 0); return Math.max(1, Math.round(w / (b.lang === 'en' ? 150 : 120))); }
function buildStories(filter) {
  var all = window.STORIES || [], langs = []; all.forEach(function (b) { if (langs.indexOf(b.lang) < 0) langs.push(b.lang); });
  filter = filter || store.get('shelf', 'all'); if (filter !== 'all' && langs.indexOf(filter) < 0) filter = 'all';
  var opts = [['all', 'All']].concat(langs.map(function (l) { return [l, esc(LNAME[l] || l)]; }));
  var h = '<div class="group"><div class="row">' + seg('segShelf', opts, filter) + '<span class="hint">Short stories, retold in simple language. More languages can be added to the shelf.</span></div><div id="shelfList">';
  all.filter(function (b) { return filter === 'all' || b.lang === filter; }).forEach(function (b) {
    var mins = storyMinutes(b);
    h += '<button type="button" class="story" data-id="' + esc(b.id) + '"><span class="cv" lang="' + esc(b.lang) + '" aria-hidden="true">' + esc(Array.from(b.title)[0]) + '</span><span class="tt"><b lang="' + esc(b.lang) + '">' + esc(b.title) + '</b><small>' + esc(b.sub) + '</small><span class="meta">' + esc(LNAME[b.lang] || b.lang) + ' · ' + b.ch.length + ' chapters · about ' + mins + ' min</span></span></button>';
  });
  el.panelBody.innerHTML = h + '</div></div>';
  $('#segShelf').addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; store.set('shelf', b.dataset.v); buildStories(b.dataset.v); });
  $('#shelfList').addEventListener('click', function (e) { var b = e.target.closest('.story'); if (!b) return; closePanel(); openBook(b.dataset.id); });
}
async function openText(text) {""")
rep("  } else buildSettings();\n  el.panel.classList.add('open');","  } else if (kind === 'stories') { el.panelTitle.textContent = 'Story shelf'; buildStories(); }\n  else buildSettings();\n  el.panel.classList.add('open');")
rep("el.libPaste.onclick =","el.libStories.onclick = function () { closeRail(); openPanel('stories'); };\nel.libPaste.onclick =")
rep("window.__vachak = { Pack: Pack,","window.__vachak = { openBook: openBook, Pack: Pack,")

# ================= sidebar toggle (desktop) + popover plumbing =================
rep("el.menuBtn.onclick = openRail;","""function applyRail() {
  var c = S.rail === 'collapsed' && !narrow.matches, lab = narrow.matches ? 'Open library' : (c ? 'Show library' : 'Hide library');
  el.app.setAttribute('data-rail', c ? 'collapsed' : 'open'); el.menuBtn.setAttribute('aria-expanded', String(!c)); el.menuBtn.setAttribute('aria-label', lab); el.menuBtn.title = lab;
  setTimeout(fitAllMq, 260);
}
el.menuBtn.onclick = function () { if (narrow.matches) openRail(); else { S.rail = S.rail === 'collapsed' ? 'open' : 'collapsed'; save('rail'); applyRail(); } };
if (narrow.addEventListener) narrow.addEventListener('change', function () { applyRail(); closePop(true); }); applyRail();""")
rep("function openRail() { closePanel(true);","function openRail() { closePop(true); el.scrim.classList.remove('clear'); closePanel(true);")
rep("  if (!el.rail.classList.contains('open')) el.scrim.classList.remove('open');\n  setNav(","  scrimCheck();\n  setNav(")
rep("function closeRail(fromPop) { el.rail.classList.remove('open'); if (!el.panel.classList.contains('open')) el.scrim.classList.remove('open');","function closeRail(fromPop) { el.rail.classList.remove('open'); scrimCheck();")
rep("  el.panel.classList.add('open'); el.scrim.classList.add('open'); el.panel.setAttribute('aria-hidden', 'false'); setNav('settings'); pushSheet();","  closePop(true); el.scrim.classList.remove('clear');\n  el.panel.classList.add('open'); el.scrim.classList.add('open'); el.panel.setAttribute('aria-hidden', 'false'); setNav('settings'); pushSheet();")
rep("el.scrim.onclick = function () { closePanel(); closeRail(); };","el.scrim.onclick = function () { closePop(); closePanel(); closeRail(); };")
rep("if (sheetPushed) { sheetPushed = false; closePanel(true); closeRail(true); } });","if (sheetPushed) { sheetPushed = false; closePop(true); closePanel(true); closeRail(true); } });")
rep("if (e.key === 'Escape' && (el.panel.classList.contains('open') || el.rail.classList.contains('open'))) { closePanel(); closeRail(); return; }","if (e.key === 'Escape' && (el.panel.classList.contains('open') || el.rail.classList.contains('open') || el.pop.classList.contains('open'))) { closePop(); closePanel(); closeRail(); return; }")
rep("  var b = e.target.closest('button'); if (!b) return;\n  if (b.dataset.go === 'library')","  var b = e.target.closest('button'); if (!b) return; closePop(true);\n  if (b.dataset.go === 'library')")

POP = r"""
function scrimCheck() { if (!el.panel.classList.contains('open') && !el.rail.classList.contains('open') && !el.pop.classList.contains('open')) { el.scrim.classList.remove('open'); el.scrim.classList.remove('clear'); } }
function closePop(fromPop) {
  if (!el.pop.classList.contains('open')) return;
  el.pop.classList.remove('open'); el.pop.setAttribute('aria-hidden', 'true'); scrimCheck();
  try { (narrow.matches ? el.tuneBtn : el.voiceBadge).focus({ preventScroll: true }); } catch (e) {}
  if (fromPop !== true) popSheet();
}
function openPop() {
  if (el.pop.classList.contains('open')) { closePop(); return; }
  closePanel(true); closeRail(true);
  buildPop();
  if (!narrow.matches) { var r = el.dock.getBoundingClientRect(); el.pop.style.bottom = Math.max(12, innerHeight - r.top + 10) + 'px'; el.pop.style.right = Math.max(12, innerWidth - r.right + 4) + 'px'; el.scrim.classList.add('clear'); }
  else { el.pop.style.bottom = ''; el.pop.style.right = ''; el.scrim.classList.remove('clear'); }
  el.pop.classList.add('open'); el.pop.setAttribute('aria-hidden', 'false'); el.scrim.classList.add('open'); pushSheet();
}
function popOpt(act, id, title, sub, checked, right) {
  return '<button type="button" class="vopt" role="radio" aria-checked="' + checked + '" data-act="' + act + '" data-id="' + esc(id) + '"><span class="rd" aria-hidden="true"></span><span class="tt"><b>' + esc(title) + '</b><small>' + esc(sub) + '</small></span>' + (right || '') + '<span class="pg"></span></button>';
}
async function buildPop() {
  var eng = S.engine || 'browser', h = '<h2>Voice and speed</h2>';
  var bn = ''; try { bn = (window.speechSynthesis ? (speechSynthesis.getVoices() || []).filter(function (v) { return v.name === S.voiceHi; })[0] : null); bn = bn ? bn.name : ''; } catch (e) {}
  var rows = popOpt('browser', 'browser', 'Device voice', bn || 'Built into this phone or computer', eng === 'browser');
  if (S.gKey) rows += popOpt('google', 'google', 'Google Cloud voice', 'Uses your API key', eng === 'google');
  var packRows = '';
  if (PATHS.pack) {
    try {
      await Pack.catalog(); Pack.defaults();
      for (var q = 0; q < 2; q++) {
        var kind = q ? 'en' : 'hi', ids = Pack.list(kind), cur = q ? S.pVoiceEn : S.pVoiceHi, shown = [];
        var inst = await Promise.all(ids.map(function (id) { return Pack.installed(id).then(function (ok) { return ok || Pack.origin() === 'voices/'; }); }));
        ids.forEach(function (id, i) { if (inst[i] || id === cur) shown.push([id, inst[i]]); });
        var extra = 0; ids.forEach(function (id, i) { if (!inst[i] && id !== cur && extra < (q ? 2 : 3)) { shown.push([id, false]); extra++; } });
        packRows += '<div class="grp"><p class="grp-t">Natural voices · ' + (q ? 'English' : 'Hindi and Sanskrit') + '</p>' + shown.map(function (x) {
          var id = x[0], lab = Pack.label(id), nm = lab.split(' (')[0], sub = (q ? 'English' : 'Hindi') + ' · ' + (lab.match(/, (\w+),/) || [0, ''])[1];
          return popOpt('pack-' + kind, id, nm, x[1] ? sub + ' · ready' : sub, eng === 'pack' && id === cur, x[1] ? '' : '<span class="dl">Download · ' + lab.replace(/.*, (\d+ MB)\)/, '$1') + '</span>');
        }).join('') + '</div>';
      }
    } catch (e) { packRows = '<div class="grp"><p class="hint" style="color:var(--ink-2)">Natural voices are not available offline right now.</p></div>'; }
  }
  h += '<div class="grp"><p class="grp-t">Voice</p><div role="radiogroup" aria-label="Voice">' + rows + '</div></div>' + packRows;
  h += '<div class="grp"><p class="grp-t">Speed</p>' + seg('segRate', [[0.7, '0.7×'], [0.8, '0.8×'], [0.9, '0.9×'], [1, '1×'], [1.1, '1.1×'], [1.25, '1.25×'], [1.5, '1.5×']], closestRate(S.rate)) + '</div>';
  h += '<div class="grp"><label class="toggle"><input type="checkbox" id="popAuto"' + (S.auto ? ' checked' : '') + '>Continue to the next page automatically</label></div>';
  h += '<div class="foot"><button type="button" class="btn" id="popTest">Play a sample</button><button type="button" class="btn quiet" id="popMore">Manage voices in Settings</button></div>';
  el.popBody.innerHTML = h;
}
function selectPackVoice(kind, id) {
  S[kind === 'en' ? 'pVoiceEn' : 'pVoiceHi'] = id; save(kind === 'en' ? 'pVoiceEn' : 'pVoiceHi'); S.engine = 'pack'; save('engine');
  checkVoiceQuality(); renderBadge(); maybeWarm(); buildPop();
  if (P.playing) { var i = P.idx; P.token++; P.playing = false; stopAudio(); P.idx = i; play(); }
}
async function sampleVoice() {
  var was = P.playing; if (was) pause();
  var t = ++P.token; stopAudio();
  var sample = [{ speech: 'नमस्ते। यह मेरी आवाज़ है, जो आपके लिए पुस्तक पढ़ेगी।' }, { speech: 'Hello. This is the voice that will read your book.' }];
  for (var i = 0; i < sample.length; i++) { if (t !== P.token) return; await speakUnit(sample[i], t); }
}
el.popBody.addEventListener('click', async function (e) {
  var b = e.target.closest('button'); if (!b) return;
  if (b.id === 'popTest') { sampleVoice(); return; }
  if (b.id === 'popMore') { closePop(); openPanel('settings'); return; }
  var r = b.closest('#segRate'); if (r) { el.rateSel.value = String(closestRate(+b.dataset.v)); el.rateSel.dispatchEvent(new Event('change')); Array.prototype.forEach.call(r.children, function (x) { x.setAttribute('aria-pressed', x === b); }); return; }
  var act = b.dataset.act; if (!act) return;
  if (act === 'browser' || act === 'google') { S.engine = act; save('engine'); checkVoiceQuality(); renderBadge(); buildPop(); if (P.playing) { var i = P.idx; P.token++; P.playing = false; stopAudio(); P.idx = i; play(); } return; }
  var kind = act.split('-')[1], id = b.dataset.id;
  if (b.querySelector('.dl')) {
    b.disabled = true; var pg = b.querySelector('.pg'), dl = b.querySelector('.dl');
    try { await Pack.install([id], function (p, m) { pg.style.width = Math.round(p * 100) + '%'; dl.textContent = Math.round(p * 100) + '%'; }); toast('Voice downloaded.'); }
    catch (x) { b.disabled = false; dl.textContent = 'Retry'; toast('Download failed: ' + x.message, 4500); return; }
  }
  selectPackVoice(kind, id);
});
el.popBody.addEventListener('change', function (e) { if (e.target.id === 'popAuto') { S.auto = e.target.checked; save('auto'); el.autoAdv.checked = S.auto; } });
el.voiceBadge.onclick = openPop; el.tuneBtn.onclick = openPop;
dragSheet(el.grabPop, el.pop, function () { closePop(); });
"""
rep("el.voiceBadge.onclick = function () { openPanel('settings'); renderBadge(); };","")
# insert popover block right after dragSheet wiring
rep("dragSheet(el.grabRail, el.rail, function () { closeRail(); }); dragSheet(el.grabPanel, el.panel, function () { closePanel(); });","dragSheet(el.grabRail, el.rail, function () { closeRail(); }); dragSheet(el.grabPanel, el.panel, function () { closePanel(); });"+POP)
# tune button state mirrors the badge
rep("  el.voiceBadge.setAttribute('data-s', st);","  el.tuneBtn.setAttribute('data-s', st); el.voiceBadge.setAttribute('data-s', st);")

# ================= settings: interface style + player size =================
rep("[['auto', 'Auto'], ['ios', 'iPhone'], ['android', 'Android'], ['desktop', 'Desktop']], S.ui)","[['auto', 'Auto'], ['ios', 'iPhone'], ['android', 'Android'], ['windows', 'Windows'], ['mac', 'Mac']], S.ui)")
rep("""'<span class="hint">Auto matches your device. Change it to preview the other styles.</span></div>' +""","""'<span class="hint">Auto matches your device. Change it to preview the other styles.</span></div>' +
    '<div class="row"><span class="lab">Player size on phones</span>' + seg('segPlayer', [['compact', 'Compact'], ['full', 'Full']], S.player) + '<span class="hint">Compact keeps the player slim so the page gets more room. Voice and speed are one tap away.</span></div>' +""")
rep("  bindSeg('#segUi', 'ui', applyPlatform);","  bindSeg('#segUi', 'ui', applyPlatform);\n  bindSeg('#segPlayer', 'player', applyPlayer);")
rep("function applyPlatform() {","function applyPlayer() { document.documentElement.setAttribute('data-player', S.player === 'full' ? 'full' : 'compact'); setTimeout(function () { if (typeof fitAllMq === 'function') fitAllMq(); }, 50); }\nfunction applyPlatform() {")
rep("applyPlatform(); applyTheme();","applyPlatform(); applyPlayer(); applyTheme();")
rep("el.libStories.onclick =","el.libStoriesSub.textContent = (window.STORIES || []).length + ' stories · Hindi, English';\nel.libStories.onclick =")
open('app.src.html','w',encoding='utf-8').write(s)
print('patched')
