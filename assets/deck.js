/* Numerical Methods course: HTML slide viewer (works from a web server or straight from disk) */
(function () {
  'use strict';
  var C = window.COURSE, N = window.LECTURE;
  var me = C.filter(function (l) { return l.n === N; })[0];
  var slides = [].slice.call(document.querySelectorAll('#stage > section'));
  var stage = document.getElementById('stage'), view = document.getElementById('view');
  var cur = 0, total = slides.length;
  var $ = function (id) { return document.getElementById(id); };
  var pad = function (n) { return (n < 10 ? '0' : '') + n; };
  var file = function (l) { return 'L' + pad(l.n) + '.html'; };

  /* ---------- top bar ---------- */
  var prevL = C.filter(function (l) { return l.n === N - 1 && l.ready; })[0], nextL = C.filter(function (l) { return l.n === N + 1 && l.ready; })[0];
  var sel = $('lecsel');
  C.forEach(function (l) {
    var o = document.createElement('option'); o.value = file(l); o.textContent = 'Lecture ' + l.n + ': ' + l.title + (l.ready ? '' : ' (coming)');
    if (!l.ready) o.disabled = true;
    if (l.n === N) o.selected = true; sel.appendChild(o);
  });
  sel.addEventListener('change', function () { location.href = sel.value; });
  function setLink(id, l, label) {
    var a = $(id);
    if (l) { a.href = file(l); a.title = 'Lecture ' + l.n + ': ' + l.title; a.querySelector('span').textContent = label + ' ' + l.n; }
    else a.classList.add('dis');
  }
  setLink('prevlec', prevL, 'Lecture'); setLink('nextlec', nextL, 'Lecture');
  if (me.lab) { $('labbtn').href = '../labs/' + me.lab; } else { $('labbtn').style.display = 'none'; }

  /* ---------- scaling ---------- */
  function fit() {
    var w = view.clientWidth, h = view.clientHeight;
    stage.style.transform = 'scale(' + Math.min(w / 1920, h / 1080) + ')';
  }
  window.addEventListener('resize', fit);

  /* ---------- fragments ---------- */
  function frags(sec) { return [].slice.call(sec.querySelectorAll('.frag')); }
  function revealed(sec) { return frags(sec).filter(function (f) { return f.classList.contains('vis'); }).length; }
  function setFrags(sec, n) { frags(sec).forEach(function (f, i) { f.classList.toggle('vis', i < n); }); }

  /* ---------- lazy mounting of live code and widgets ---------- */
  function mount(sec) {
    if (sec._mounted) return; sec._mounted = true;
    if (window.Runner) window.Runner.mountAll(sec);
    if (window.Widgets) window.Widgets.mountAll(sec);
  }

  /* ---------- navigation ---------- */
  function fitMath(root) {   // shrink display equations that are wider than their box
    [].forEach.call(root.querySelectorAll('.katex-display'), function (el) {
      el.style.fontSize = '';
      var w = el.clientWidth, sw = el.scrollWidth;
      if (w > 0 && sw > w + 2) el.style.fontSize = Math.max(0.55, (w / sw) * 0.98).toFixed(3) + 'em';
    });
  }
  function show(i, fromHash, allFrags) {
    i = Math.max(0, Math.min(total - 1, i));
    slides.forEach(function (s, k) { s.classList.toggle('off', k !== i); });
    cur = i;
    mount(slides[i]);
    fitMath(slides[i]);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { if (cur === i) fitMath(slides[i]); });
    if (allFrags) setFrags(slides[i], frags(slides[i]).length);
    else if (!fromHash || !slides[i]._seen) setFrags(slides[i], 0);
    slides[i]._seen = true;
    $('count').textContent = (i + 1) + ' / ' + total;
    if (!fromHash) history.replaceState(null, '', '#' + (i + 1));
    renderNotes(); markList();
    document.title = me.title + ' (' + (i + 1) + '/' + total + ') · Numerical Methods';
    setTimeout(function () { window.dispatchEvent(new Event('resize')); }, 30);
  }
  function next() {
    var s = slides[cur], f = frags(s), r = revealed(s);
    if (r < f.length) { f[r].classList.add('vis'); return; }
    if (cur < total - 1) show(cur + 1); else endCard();
  }
  function prev() {
    closeEnd();
    var s = slides[cur], r = revealed(s);
    if (r > 0) { frags(s)[r - 1].classList.remove('vis'); return; }
    if (cur > 0) show(cur - 1, false, true);
  }
  $('nexts').addEventListener('click', next);
  $('prevs').addEventListener('click', prev);

  function endCard() {
    if ($('endcard')) return;
    var d = document.createElement('div'); d.id = 'endcard';
    var h = '<div><h2>End of Lecture ' + N + '</h2><p>' + me.title + '</p><div class="row">';
    if (nextL) h += '<a class="go" href="' + file(nextL) + '">Lecture ' + nextL.n + ': ' + nextL.title + ' →</a>';
    if (me.lab) h += '<a href="../labs/' + me.lab + '">Open the lab</a>';
    h += '<a href="../index.html">Course home</a><button type="button" id="stay">Stay here</button></div></div>';
    d.innerHTML = h; document.body.appendChild(d);
    $('stay').addEventListener('click', closeEnd); $('stay').focus();
    d.addEventListener('click', function (e) { if (e.target === d) closeEnd(); });
  }
  function closeEnd() { var e = $('endcard'); if (e) e.remove(); }

  /* ---------- speaker notes (only if notes/LNN.js was kept) ---------- */
  var notesOn = false;
  if (!window.DECK_NOTES) $('notesbtn').style.display = 'none';
  function renderNotes() {
    var box = $('notes');
    $('notesbtn').classList.toggle('on', notesOn);
    if (!notesOn || !window.DECK_NOTES) { box.hidden = true; return; }
    var t = window.DECK_NOTES[slides[cur].id] || '(no notes for this slide)';
    box.hidden = false; box.innerHTML = '<b>Speaker notes · slide ' + (cur + 1) + '</b>'; box.appendChild(document.createTextNode(t));
  }
  $('notesbtn').addEventListener('click', function () { notesOn = !notesOn; renderNotes(); });

  /* ---------- slide list ---------- */
  var list = $('list');
  (function buildList() {
    var ol = document.createElement('ol');
    slides.forEach(function (s, i) {
      var t = s.getAttribute('data-title') || (s.querySelector('h1,h2') || {}).textContent || ('Slide ' + (i + 1));
      var li = document.createElement('li'), a = document.createElement('a');
      a.href = '#' + (i + 1); a.innerHTML = '<span>' + (i + 1) + '</span>'; a.appendChild(document.createTextNode(t.trim()));
      a.addEventListener('click', function (e) { e.preventDefault(); show(i, false, true); list.hidden = true; });
      li.appendChild(a); ol.appendChild(li);
    });
    list.appendChild(ol);
  })();
  function markList() { [].forEach.call(list.querySelectorAll('a'), function (a, i) { a.classList.toggle('cur', i === cur); }); }
  $('listbtn').addEventListener('click', function () { list.hidden = !list.hidden; if (!list.hidden) { var c = list.querySelector('a.cur'); if (c) c.scrollIntoView({ block: 'center' }); } });

  /* ---------- fullscreen with auto-hiding bar ---------- */
  function toggleFs() {
    if (!document.fullscreenElement) { (document.documentElement.requestFullscreen || function () {}).call(document.documentElement); }
    else document.exitFullscreen();
  }
  $('fsbtn').addEventListener('click', toggleFs);
  document.addEventListener('fullscreenchange', function () { document.body.classList.toggle('fs', !!document.fullscreenElement); poke(); setTimeout(fit, 60); });
  var idleT;
  function poke() { document.body.classList.remove('idle'); clearTimeout(idleT); idleT = setTimeout(function () { document.body.classList.add('idle'); }, 2500); }
  document.addEventListener('mousemove', poke);
  $('helpbtn').addEventListener('click', function () { var h = $('help'); h.hidden = !h.hidden; });

  /* ---------- pop-up details for clickable cards ---------- */
  function openModal(id) {
    var t = document.getElementById(id); if (!t) return;
    closeModal();
    var m = document.createElement('div'); m.id = 'modal'; m.setAttribute('role', 'dialog'); m.setAttribute('aria-modal', 'true');
    var box = document.createElement('div'); box.appendChild(t.content.cloneNode(true));
    var x = document.createElement('button'); x.type = 'button'; x.className = 'x'; x.textContent = '×'; x.setAttribute('aria-label', 'Close');
    x.addEventListener('click', closeModal); box.appendChild(x); m.appendChild(box); document.body.appendChild(m);
    m.addEventListener('click', function (e) { if (e.target === m) closeModal(); });
    fitMath(box);
    if (window.Runner) window.Runner.mountAll(box);
    if (window.Widgets) window.Widgets.mountAll(box);
    x.focus();
  }
  function closeModal() { var m = $('modal'); if (m) m.remove(); }
  document.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('[data-modal]'); if (b) { e.preventDefault(); openModal(b.getAttribute('data-modal')); } });

  /* ---------- keyboard ---------- */
  var typed = '';
  document.addEventListener('keydown', function (e) {
    var tag = (e.target.tagName || '').toLowerCase(), k = e.key;
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    if ($('modal')) { if (k === 'Escape') closeModal(); return; }
    if (k === 'Escape' && e.target !== document.body && e.target.blur) { e.target.blur(); }
    var isRange = tag === 'input' && e.target.type === 'range';
    var inWidget = e.target.closest && e.target.closest('[data-widget]');
    if (k !== 'PageDown' && k !== 'PageUp') {
      if (isRange && /^(Arrow|Home|End)/.test(k)) return;
      if (tag === 'select' || tag === 'textarea' || (tag === 'input' && !isRange)) return;
      if (inWidget && (k === ' ' || k === 'Enter')) return;
    }
    if (/^[0-9]$/.test(k)) { typed += k; return; }
    if (k === 'Enter' && typed) { show(parseInt(typed, 10) - 1, false, true); typed = ''; e.preventDefault(); return; }
    typed = '';
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ' || k === 'ArrowDown') { e.preventDefault(); if ($('endcard')) return; next(); }
    else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'ArrowUp' || k === 'Backspace') { e.preventDefault(); prev(); }
    else if (k === 'Home') show(0);
    else if (k === 'End') show(total - 1, false, true);
    else if (k === 'f' || k === 'F') toggleFs();
    else if ((k === 'n' || k === 'N') && window.DECK_NOTES) { notesOn = !notesOn; renderNotes(); }
    else if (k === 's' || k === 'S') $('listbtn').click();
    else if (k === 'a' || k === 'A') { setFrags(slides[cur], frags(slides[cur]).length); }
    else if (k === 'Escape') { closeEnd(); $('help').hidden = true; list.hidden = true; }
    else if (k === '[' && prevL) location.href = file(prevL);
    else if (k === ']' && nextL) location.href = file(nextL);
    else if ((k === 'l' || k === 'L') && me.lab) location.href = '../labs/' + me.lab;
  });

  /* ---------- touch swipe ---------- */
  var sx = null, sy = null;
  view.addEventListener('touchstart', function (e) { if (e.target.closest && e.target.closest('[data-widget]')) { sx = null; return; } sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
  view.addEventListener('touchend', function (e) {
    if (sx === null) return;
    var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) { dx < 0 ? next() : prev(); }
    sx = null;
  });

  /* ---------- start ---------- */
  window.addEventListener('hashchange', function () { var n = parseInt(location.hash.slice(1), 10); if (n && n - 1 !== cur) show(n - 1, true, true); });
  var start = parseInt(location.hash.slice(1), 10);
  fit(); show(start ? start - 1 : 0, false, !!start); poke();
})();
