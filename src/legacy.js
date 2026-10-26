/* Repairs Devanagari text extracted from PDFs that use legacy (non-Unicode) fonts,
   such as Gita Press editions. Visual-order glyphs are mapped to Unicode and reordered. */
(function (root) {
  var FULL = {
    'Ĝ':'श्र','Ē':'प्र','č':'त्र','³':'क्ष','´':'ज्ञ','ď':'द्र','Ĕ':'ब्र','Ā':'ग्र','þ':'क्र','Đ':'ध्र','ĕ':'भ्र','ā':'घ्र','Ğ':'स्र','Ė':'म्र','Ą':'छ्र','ě':'व्र','ȍ':'ष्ट्र',
    'ƞ':'रू','Ɲ':'रु','Ɵ':'दु','Ɠ':'हु','Ơ':'दू','ơ':'दृ','ƕ':'हृ','Ɣ':'हू',
    'ǣ':'क्त','Ƕ':'त्त','Ǽ':'द्व','ǽ':'द्ध','ȃ':'न्न','Ȍ':'ष्ट','Ȏ':'ष्ठ','ȁ':'द्य','Ȇ':'श्च','ȋ':'श्न','Ȉ':'श्व','ȅ':'व्य',
    'Ȓ':'ह्म','ȑ':'ह्न','ȓ':'ह्य','ȕ':'ह्व','Ȋ':'श्ल','Ȁ':'द्म','Ȅ':'द्म','Ǩ':'ञ्ज','À':'ञ्च','Ǥ':'ङ्ग','ǻ':'द्भ','ǿ':'द्द','ǩ':'ट्ट','Ƿ':'त्त्','ś':'ण्य','Ð':'य्य',
    'ǂ':'ों','ƶ':'ें','ƹ':'ैं','ɡ':'ी','ɟ':'ी','ɠ':'ी','ƭ':'ीं','Ǔ':'ओं'
  };
  var HALF = {'×':'स्','Ê':'न्','Æ':'त्','Ï':'म्','Ö':'ष्','Ë':'प्','Å':'ण्','¼':'च्','·':'क्','¸':'ख्','¹':'ग्','º':'घ्','¾':'ज्','Ò':'ल्','É':'ध्','Í':'ब्','Ç':'थ्','Î':'भ्','Õ':'श्','Û':'क्ष्'};
  var REPH_PRE = 'ɉɊɋɌɍ';            // reph + i-matra, written before the cluster
  var REPH_POST = {'µ':'','ǋ':'','ǃ':'','Ǆ':'','Ʒ':'े','Ʈ':'ी'}; // reph written after the cluster
  var Z = /[क-हक़-य़]/;
  function isMatraI(c) { var n = c.charCodeAt(0); return n >= 0x22E && n <= 0x23F || n === 0x1F6 && false; }
  function isCons(c) { return c && (Z.test(c) || FULL[c] !== undefined && /[क-ह]$/.test(FULL[c]) ); }
  function isHalf(c) { return HALF[c] !== undefined; }
  var VOWELSIGN_CLEAN = FULL;

  // Reads one consonant cluster starting at i; returns the end index (exclusive) and its text.
  function readCluster(a, i) {
    var out = '';
    while (i < a.length) {
      var c = a[i];
      if (isHalf(c)) { out += HALF[c]; i++; continue; }
      if (Z.test(c)) {
        out += c; i++;
        if (a[i] === '्' && i + 1 < a.length) { out += a[i]; i++; continue; }
        if (a[i] === '़') { out += a[i]; i++; }
        return [i, out];
      }
      if (FULL[c] !== undefined && /[क-ह]$/.test(FULL[c])) { out += FULL[c]; i++; return [i, out]; }
      break;
    }
    return [i, out];
  }

  function convert(src) {
    var a = Array.from(src), out = [], i, n = a.length;
    function tail() { return out; }
    for (i = 0; i < n; i++) {
      var c = a[i];
      if (isMatraI(c) || REPH_PRE.indexOf(c) >= 0) {
        var pre = REPH_PRE.indexOf(c) >= 0 ? 'र्' : '';
        var r = readCluster(a, i + 1);
        if (r[1]) { out.push(pre + r[1] + 'ि'); i = r[0] - 1; }
        else { out.push(pre ? pre + 'ि' : 'ि'); }
        continue;
      }
      if (REPH_POST[c] !== undefined) {
        // pull the previous cluster back off the output
        var s = out.join(''), j = s.length, k;
        // walk back: consonant (+ halant-joined predecessors)
        var m = s.match(/((?:[क-हक़-य़]़?्)*[क-हक़-य़]़?)([ा-ौंँः]*)$/);
        if (m) { out = [s.slice(0, s.length - m[0].length) + 'र्' + m[1] + m[2] + REPH_POST[c]]; }
        else { out.push('र्' + REPH_POST[c]); }
        continue;
      }
      if (FULL[c] !== undefined) { out.push(FULL[c]); continue; }
      if (HALF[c] !== undefined) { out.push(HALF[c]); continue; }
      out.push(c);
    }
    var t = out.join('');
    // remove any stray legacy glyphs we could not map
    t = t.replace(/[¡-¿À-ɏɐ-ʯΐ-Ͽ]/g, '');
    t = t.replace(/्\s+([ािीुूृेैोौंँः])/g, '$1');      // "भ् ा" artefacts
    t = t.replace(/््/g, '्');
    // vowel sign displaced past a danda or comma ("चाहिय।े")
    t = t.replace(/([।॥,.;?!])([ेैोौ])/g, '$2$1');
    // the old fonts drop the space after words ending in a nasal vowel sign ("हैंऔर"); put it back
    t = t.replace(/(ें|ैं|ों|ीं)(?=[क-ह])/g, function (m, a, off, str) { return a === 'ों' && str.substr(off + 2, 2) === 'ने' ? m : m + ' '; });
    return t;
  }

  function looksLegacy(s) {
    var legacy = (s.match(/[³´µÆÊ×Ā-ɏɐ-ʯ]/g) || []).length;
    var dev = (s.match(/[ऀ-ॿ]/g) || []).length;
    return legacy > 20 && legacy / Math.max(1, dev + legacy) > 0.03;
  }

  var api = { convert: convert, looksLegacy: looksLegacy };
  if (typeof module !== 'undefined') module.exports = api; else root.LegacyDevanagari = api;
})(typeof self !== 'undefined' ? self : this);
