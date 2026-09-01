/* StarShack Landing Page — 交互脚本 */
(function () {
  'use strict';

  /* 1. 滚动入场动画 */
  var revealItems = document.querySelectorAll('.reveal');

  if (!('IntersectionObserver' in window)) {
    revealItems.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry, i) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          // 同组卡片依次错开出现
          var delay = (i % 3) * 80;
          setTimeout(function () { el.classList.add('is-visible'); }, delay);
          observer.unobserve(el);
        });
      },
      { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
    );

    revealItems.forEach(function (el) { observer.observe(el); });
  }

  /* 2. 导航高亮 */
  var sections = ['features', 'modules', 'community'].map(function (id) {
    return document.getElementById(id);
  }).filter(Boolean);

  var navLinks = Array.prototype.slice.call(
    document.querySelectorAll('.nav-links a')
  );

  function syncNav() {
    var pos = window.scrollY + 140;
    var currentId = null;

    sections.forEach(function (section) {
      if (section.offsetTop <= pos) currentId = section.id;
    });

    navLinks.forEach(function (link) {
      var isActive = link.getAttribute('href') === '#' + currentId;
      link.style.color = isActive ? '#FFFFFF' : '';
    });
  }

  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      syncNav();
      ticking = false;
    });
  }, { passive: true });

  syncNav();
})();
