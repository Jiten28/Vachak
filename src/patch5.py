s=open('app.src.html',encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]); s=s.replace(a,b)

# ---- CSS: voice badge + busy ring ----
rep("@supports (height: 100dvh)","""@keyframes vspin { to { transform: rotate(360deg); } }
.vbadge { display: inline-flex; align-items: center; gap: 8px; max-width: 100%; border: 1px solid var(--line); background: var(--sheet); border-radius: 99px; padding: 5px 12px 5px 10px; font-size: .8rem; font-weight: 600; color: var(--ink-2); min-height: 32px; }
.vbadge:hover { border-color: var(--ink-3); }
.vbadge .dot { flex: none; width: 9px; height: 9px; border-radius: 50%; background: var(--ink-3); box-sizing: border-box; }
.vbadge[data-s="ready"] .dot { background: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
.vbadge[data-s="loading"] { border-color: var(--accent); }
.vbadge[data-s="loading"] .dot { width: 14px; height: 14px; background: transparent; border: 2px solid var(--accent-soft); border-top-color: var(--accent); animation: vspin .8s linear infinite; }
.vbadge[data-s="error"] .dot { background: var(--danger); }
.vbadge span:last-child { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.play { position: relative; }
.play.busy::after { content: ""; position: absolute; inset: -5px; border-radius: inherit; border: 3px solid transparent; border-top-color: var(--accent); border-right-color: var(--accent); animation: vspin .9s linear infinite; }
.play.busy svg { opacity: .75; }
.bufbar { height: 3px; border-radius: 3px; background: var(--line); overflow: hidden; position: relative; }
.bufbar[hidden] { display: none; }
.bufbar i { position: absolute; top: 0; bottom: 0; width: 38%; background: var(--accent); border-radius: 3px; animation: vslide 1.3s ease-in-out infinite; }
@keyframes vslide { 0% { left: -40%; } 100% { left: 102%; } }
@media (prefers-reduced-motion: reduce) { .vbadge .dot, .play.busy::after { animation-duration: 2.6s !important; } .bufbar i { animation-duration: 3s !important; } }
@supports (height: 100dvh)""")

# ---- markup ----
rep('<button class="btn quiet" id="voiceTip"','<button class="vbadge" id="voiceBadge" type="button" data-s="idle" title="Voice in use. Tap to change."><span class="dot" aria-hidden="true"></span><span id="voiceBadgeTxt">Voice</span></button>\n        <button class="btn quiet" id="voiceTip"')
rep('<div class="dock-row">','<div class="bufbar" id="bufbar" hidden aria-hidden="true"><i></i></div>\n      <div class="dock-row">')
rep("'rateSel','autoAdv',","'rateSel','autoAdv','voiceBadge','voiceBadgeTxt','bufbar',")

# ---- security: esc quotes, id/path validation ----
rep("""function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }""",
    """function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]; }); }""")
rep("""    Object.keys(v.files).forEach(function (k) { if (/\\.onnx$/.test(k)) onnx = k; else if (/\\.onnx\\.json$/.test(k)) cfg = k; });
    return {""","""    Object.keys(v.files).forEach(function (k) { if (!SAFE_PATH.test(k)) return; if (/\\.onnx$/.test(k)) onnx = k; else if (/\\.onnx\\.json$/.test(k)) cfg = k; });
    if (!onnx || !cfg) throw new Error('This voice entry is not valid.');
    return {""")
rep("var catalog = null, origin = null,","var SAFE_ID = /^[a-z]{2,3}_[A-Za-z]{2,4}-[A-Za-z0-9_]+-[a-z_]+$/, SAFE_PATH = /^[A-Za-z0-9_\\-]+(\\/[A-Za-z0-9_\\-]+)*\\.onnx(\\.json)?$/, warmed = {}, stageFn = null;\n  var catalog = null, origin = null,")
rep("return k.indexOf(kind === 'en' ? 'en_' : 'hi_') === 0 && q !== 'x_low'","return SAFE_ID.test(k) && catalog[k].files && k.indexOf(kind === 'en' ? 'en_' : 'hi_') === 0 && q !== 'x_low'")

# ---- Pack: stages + warm-up ----
rep("  function noop() {}\n","  function noop() {}\n  function stage(st, id) { try { if (stageFn) stageFn(st, id); } catch (e) {} }\n")
rep("""      await ensureEngine(onbytes);
      var vd = await voice(id, onbytes);
      workers();
      var pd = await ask(ph, 'phonemize', [text, vd]);
      var out = await ask(on, 'generate', [pd, vd, 0]);
      return URL.createObjectURL(out.file);
    }).catch(function (e) { reset(); throw e; });""","""      var cold = !warmed[id];
      if (cold) stage('engine', id);
      await ensureEngine(onbytes);
      if (!mem[id]) stage('voice', id);
      var vd = await voice(id, onbytes);
      if (cold) stage('start', id);
      workers();
      var pd = await ask(ph, 'phonemize', [text, vd]);
      if (cold) stage('speak', id);
      var out = await ask(on, 'generate', [pd, vd, 0]);
      warmed[id] = true; if (cold) stage('ready', id);
      return URL.createObjectURL(out.file);
    }).catch(function (e) { reset(); warmed = {}; stage('error', id); throw e; });""")
rep("async function remove() { reset(); mem = {};","async function remove() { reset(); warmed = {}; mem = {};")
rep("return { peekLocal: peekLocal,","""function warm(id) { return synth(/^hi_|^ne_|^sa_/.test(id) ? 'नमस्ते।' : 'Hello.', id); }
  return { warm: warm, isWarm: function (id) { return !!warmed[id]; }, onstage: function (f) { stageFn = f; }, peekLocal: peekLocal,""")

# ---- UI logic ----
rep("function setStatus(m) {","""var VB = { st: 'idle', stage: '', t0: 0, tick: null, wait: false };
var STAGE_TXT = { engine: 'Preparing the voice engine', voice: 'Loading the voice model', start: 'Warming up (first time only)', speak: 'Almost ready' };
function activeVoiceName() {
  if (S.engine === 'pack') { var id = S.pVoiceHi; return id ? Pack.label(id).split(' (')[0] : ''; }
  if (S.engine === 'google') return S.gVoiceHi || '';
  var v = S.voiceHi && window.speechSynthesis ? (speechSynthesis.getVoices() || []).filter(function (x) { return x.name === S.voiceHi; })[0] : null;
  return v ? v.name : '';
}
function renderBadge() {
  var eng = S.engine || 'browser', st = 'idle', txt;
  if (eng === 'pack' && PATHS.pack) {
    var nm = ''; try { nm = activeVoiceName(); } catch (e) {}
    if (VB.st === 'loading') { st = 'loading'; txt = (STAGE_TXT[VB.stage] || 'Loading the natural voice') + '… ' + Math.max(0, Math.round((Date.now() - VB.t0) / 1000)) + 's'; }
    else if (VB.st === 'error') { st = 'error'; txt = 'Natural voice failed. Tap to check'; }
    else if (S.pVoiceHi && Pack.isWarm(S.pVoiceHi)) { st = 'ready'; txt = 'Natural voice ready' + (nm ? ' · ' + nm : ''); }
    else { txt = 'Natural voice selected' + (nm ? ' · ' + nm : '') + ' · loads on play'; }
  } else if (eng === 'google') { st = S.gKey ? 'ready' : 'error'; txt = S.gKey ? 'Google Cloud voice' : 'Google voice needs an API key'; }
  else { var dn = ''; try { dn = activeVoiceName(); } catch (e) {} txt = 'Device voice' + (dn ? ' · ' + dn : ''); }
  el.voiceBadge.setAttribute('data-s', st); el.voiceBadgeTxt.textContent = txt;
  var busy = VB.wait || VB.st === 'loading';
  el.playBtn.classList.toggle('busy', busy && P.playing); el.bufbar.hidden = !(busy && P.playing);
  el.playBtn.setAttribute('aria-busy', busy && P.playing ? 'true' : 'false');
}
function setVBState(st, stg) {
  VB.st = st; VB.stage = stg || '';
  if (st === 'loading') { if (!VB.t0) VB.t0 = Date.now(); if (!VB.tick) VB.tick = setInterval(renderBadge, 1000); }
  else { VB.t0 = 0; if (VB.tick) { clearInterval(VB.tick); VB.tick = null; } }
  renderBadge();
}
Pack.onstage(function (stg) { if (stg === 'ready') setVBState('ready'); else if (stg === 'error') setVBState('error'); else setVBState('loading', stg); });
function maybeWarm() {
  if (S.engine !== 'pack' || !PATHS.pack) return;
  if (navigator.connection && navigator.connection.saveData) return;
  Pack.catalog().then(function () { Pack.defaults(); return Pack.installed(S.pVoiceHi).then(function (ok) { return ok || Pack.origin() === 'voices/'; }); })
    .then(function (ok) { if (ok && S.pVoiceHi && !Pack.isWarm(S.pVoiceHi)) return Pack.warm(S.pVoiceHi); })
    .catch(function () {}).then(renderBadge);
}
function setStatus(m) {""")
# play-wait flag around synth
rep("  try { url = await Pack.synth(u.speech, id, t, function (n) { got += n; setStatus('Downloading the voice, ' + Math.round(got / 1e6) + ' MB…'); }); } finally { setStatus(''); }",
    "  VB.wait = true; renderBadge();\n  try { url = await Pack.synth(u.speech, id, t, function (n) { got += n; setStatus('Downloading the voice, ' + Math.round(got / 1e6) + ' MB…'); }); } finally { VB.wait = false; setStatus(''); renderBadge(); }")
rep("function setPlayUI() {","function setPlayUI() {\n  renderBadge();")
# status text during cold start
rep("var got = 0; setStatus('Preparing the natural voice…');","var got = 0; setStatus(Pack.isWarm(id) ? '' : 'Preparing the natural voice… the first line takes a few seconds');")
# badge click, engine change, install finish, boot warm
rep("el.voiceTip.onclick = function () { openPanel('settings'); };","el.voiceTip.onclick = function () { openPanel('settings'); }; el.voiceBadge.onclick = function () { openPanel('settings'); renderBadge(); };")
rep("bindSeg('#segEngine', 'engine', function () { showEng(); checkVoiceQuality(); });","bindSeg('#segEngine', 'engine', function () { showEng(); checkVoiceQuality(); renderBadge(); maybeWarm(); });")
rep("sel.onchange = function () { S[key] = sel.value; save(key); refresh(); };","sel.onchange = function () { S[key] = sel.value; save(key); refresh(); renderBadge(); if (key === 'pVoiceHi') maybeWarm(); };")
rep("toast('Natural voice downloaded.'); }","S.engine = 'pack'; save('engine'); checkVoiceQuality(); toast('Natural voice downloaded and selected.'); maybeWarm(); renderBadge(); }")
rep("if (PATHS.pack && S.engine == null) Pack.peekLocal().then(function (ok) { if (ok && S.engine == null) { S.engine = 'pack'; checkVoiceQuality(); toast('Natural voice is on. It loads when you press play.', 4500); } });",
"""if (PATHS.pack && S.engine == null) Pack.peekLocal().then(function (ok) { if (ok && S.engine == null) { S.engine = 'pack'; checkVoiceQuality(); toast('Natural voice is selected. Getting it ready…', 4500); } }).then(function () { renderBadge(); maybeWarm(); });
renderBadge();
(window.requestIdleCallback || function (f) { setTimeout(f, 1200); })(function () { maybeWarm(); }, { timeout: 4000 });""")
# API key: remember only if asked
open('app.src.html','w',encoding='utf-8').write(s)
print('ok')
