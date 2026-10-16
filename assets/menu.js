// 상단 전체 메뉴(☰) 열고 닫기
(function () {
  var btn = document.querySelector('.menu-btn');
  var panel = document.getElementById('site-menu');
  var dim = document.querySelector('.menu-dim');
  if (!btn || !panel) return;
  function open() {
    panel.hidden = false; dim.hidden = false;
    requestAnimationFrame(function () { document.body.classList.add('menu-open'); });
    btn.setAttribute('aria-expanded', 'true');
    var c = panel.querySelector('.menu-close'); if (c) c.focus();
  }
  function close() {
    document.body.classList.remove('menu-open');
    btn.setAttribute('aria-expanded', 'false');
    setTimeout(function () { panel.hidden = true; dim.hidden = true; }, 250);
    btn.focus();
  }
  btn.addEventListener('click', open);
  dim.addEventListener('click', close);
  panel.querySelector('.menu-close').addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) close(); });
  panel.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { if (!a.target) close(); }); });
})();
