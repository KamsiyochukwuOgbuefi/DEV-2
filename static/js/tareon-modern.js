document.addEventListener('DOMContentLoaded', function () {
  /* ---- scroll reveal ---- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

  /* ---- sticky header ---- */
  var header = document.querySelector('.tareon-header');
  var bar = document.querySelector('.tareon-utility');
  function onScroll() {
    if (header && bar) {
      var y = window.scrollY || document.documentElement.scrollTop;
      if (y > bar.offsetHeight + 10) { header.classList.add('sticky'); document.body.style.paddingTop = header.offsetHeight + 'px'; }
      else { header.classList.remove('sticky'); document.body.style.paddingTop = '0px'; }
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---- counters: render final values instantly (SEO + no flash of zero) ---- */
  document.querySelectorAll('[data-count]').forEach(function (el) {
    el.textContent = el.getAttribute('data-count');
  });

  /* ---- testimonial slider ---- */
  var slides = document.querySelectorAll('.th-testimonial-slide');
  var idx = 0, prev = document.getElementById('tPrev'), next = document.getElementById('tNext');
  if (slides.length) {
    function show(i) {
      idx = (i + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.style.display = k === idx ? 'block' : 'none'; });
    }
    show(0);
    if (next) next.addEventListener('click', function () { show(idx + 1); });
    if (prev) prev.addEventListener('click', function () { show(idx - 1); });
    setInterval(function () { show(idx + 1); }, 6000);
  }

  /* ---- hero parallax ---- */
  var heroImg = document.querySelector('.th-hero__image');
  if (heroImg) {
    window.addEventListener('scroll', function () {
      var y = window.scrollY || 0;
      if (y < 800) heroImg.style.transform = 'scale(1.06) translateY(' + (y * 0.08) + 'px)';
    }, { passive: true });
  }
});
