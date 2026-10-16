// 메인 이미지 슬라이더: 좌우 버튼, 점 표시, 자동 넘김(마우스·터치 중에는 멈춤)
document.querySelectorAll('.slider').forEach(function (slider) {
  var track = slider.querySelector('.slider-track');
  var slides = Array.prototype.slice.call(track.children);
  var dotsBox = slider.querySelector('.slider-dots');
  var current = 0, timer = null, paused = false;
  slides.forEach(function (_, i) {
    var d = document.createElement('button');
    d.type = 'button'; d.setAttribute('aria-label', (i + 1) + '번째 사진');
    d.addEventListener('click', function () { go(i); });
    dotsBox.appendChild(d);
  });
  var dots = dotsBox.children;
  function go(i) {
    current = (i + slides.length) % slides.length;
    var s = slides[current];
    var center = window.matchMedia('(max-width: 860px)').matches;
    var pad = parseFloat(getComputedStyle(track).paddingLeft) || 0;
    var left = center ? s.offsetLeft - (track.clientWidth - s.offsetWidth) / 2 : s.offsetLeft - pad;
    if (current === 0) left = 0;
    track.scrollTo({ left: left, behavior: 'smooth' });
  }
  function nearest() {
    var center = window.matchMedia('(max-width: 860px)').matches;
    var pad = parseFloat(getComputedStyle(track).paddingLeft) || 0;
    var ref = center ? track.scrollLeft + track.clientWidth / 2 : track.scrollLeft + pad;
    if (track.scrollLeft + track.clientWidth >= track.scrollWidth - 4) return slides.length - 1;
    var best = 0, bd = Infinity;
    slides.forEach(function (s, i) {
      var c = center ? s.offsetLeft + s.offsetWidth / 2 : s.offsetLeft, d = Math.abs(c - ref);
      if (d < bd) { bd = d; best = i; }
    });
    return best;
  }
  function mark() {
    current = nearest();
    for (var i = 0; i < dots.length; i++) dots[i].classList.toggle('on', i === current);
  }
  track.addEventListener('scroll', function () { window.requestAnimationFrame(mark); }, { passive: true });
  slider.querySelector('.prev').addEventListener('click', function () { go(current - 1); });
  slider.querySelector('.next').addEventListener('click', function () { go(current + 1); });
  ['mouseenter', 'touchstart', 'focusin'].forEach(function (e) { slider.addEventListener(e, function () { paused = true; }, { passive: true }); });
  ['mouseleave', 'touchend', 'focusout'].forEach(function (e) { slider.addEventListener(e, function () { paused = false; }, { passive: true }); });
  var delay = parseInt(slider.dataset.autoplay || '0', 10);
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (delay && !reduce) timer = setInterval(function () { if (!paused && !document.hidden) go(current + 1); }, delay);
  mark();
});
