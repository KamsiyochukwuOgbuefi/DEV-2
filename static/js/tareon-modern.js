document.addEventListener('DOMContentLoaded', function () {

  /* ---- scroll reveal ---- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

  /* ---- sticky header + padding offset ---- */
  var header = document.querySelector('.tareon-header');
  var bar = document.querySelector('.tareon-utility');
  function onScroll() {
    if (header && bar) {
      var y = window.scrollY || document.documentElement.scrollTop;
      if (y > bar.offsetHeight + 10) {
        header.classList.add('sticky');
        document.body.style.paddingTop = header.offsetHeight + 'px';
      } else {
        header.classList.remove('sticky');
        document.body.style.paddingTop = '0px';
      }
    }
    /* scroll-to-top visibility */
    var topBtn = document.querySelector('.scrollup');
    if (topBtn) {
      if (y > 400) { topBtn.classList.add('visible'); }
      else { topBtn.classList.remove('visible'); }
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- scroll to top ---- */
  var topBtn = document.querySelector('.scrollup');
  if (topBtn) {
    topBtn.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---- mobile menu toggle ---- */
  var toggle = document.querySelector('.navbar-toggle');
  var collapse = document.querySelector('.navbar-collapse');
  if (toggle && collapse) {
    toggle.addEventListener('click', function () {
      var open = collapse.classList.toggle('show');
      toggle.setAttribute('aria-expanded', open);
    });
    /* close mobile menu when clicking a link */
    collapse.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        collapse.classList.remove('show');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

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
      if (y < 800) heroImg.style.transform = 'scale(1.06) translateY(' + (y * 0.06) + 'px)';
    }, { passive: true });
  }

  /* ---- active nav link on scroll (by section id) ---- */
  var sections = document.querySelectorAll('section[id]');
  var navLinks = document.querySelectorAll('.navbar-nav > li > a[href^="#"]');
  if (sections.length && navLinks.length) {
    window.addEventListener('scroll', function () {
      var y = window.scrollY || document.documentElement.scrollTop;
      sections.forEach(function (sec) {
        var top = sec.offsetTop - 130;
        var bottom = top + sec.offsetHeight;
        var id = sec.getAttribute('id');
        if (y >= top && y < bottom) {
          navLinks.forEach(function (l) { l.classList.remove('active'); });
          var active = document.querySelector('.navbar-nav > li > a[href="#' + id + '"]');
          if (active) active.classList.add('active');
        }
      });
    }, { passive: true });
  }

});
