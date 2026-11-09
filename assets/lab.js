/* Lab page: tabs (remembered per lab), lazy mounting of widgets and code boxes */
(function () {
  'use strict';
  var tabs = [].slice.call(document.querySelectorAll('.tabs button')), panes = [].slice.call(document.querySelectorAll('.pane'));
  var key = 'nm-lab-tab:' + location.pathname.split('/').pop();
  function open(i) {
    tabs.forEach(function (t, k) { t.classList.toggle('on', k === i); t.setAttribute('aria-selected', String(k === i)); });
    panes.forEach(function (p, k) { p.hidden = k !== i; });
    var p = panes[i];
    if (p && !p._m) { p._m = true; window.Runner.mountAll(p); window.Widgets.mountAll(p); }
    try { localStorage.setItem(key, String(i)); } catch (e) {}
    setTimeout(function () { window.dispatchEvent(new Event('resize')); }, 30);
  }
  tabs.forEach(function (t, i) { t.addEventListener('click', function () { open(i); }); });
  var start = 0;
  var hm = /^#tab(\d+)$/.exec(location.hash); if (hm) start = Math.min(tabs.length - 1, +hm[1] - 1);
  else { try { var s = parseInt(localStorage.getItem(key), 10); if (s >= 0 && s < tabs.length) start = s; } catch (e) {} }
  open(start);
})();
