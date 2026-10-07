/* ============================================================
   JAMES® — Motion Engine
   Original implementation. Techniques observed from reference
   material, rebuilt from scratch with GSAP + ScrollTrigger + Lenis.
   ============================================================ */
(function () {
  'use strict';

  gsap.registerPlugin(ScrollTrigger);
  var REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FINE_POINTER = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---------------- Smooth scroll (Lenis) ---------------- */
  var lenis = null;
  if (!REDUCED && typeof Lenis !== 'undefined') {
    lenis = new Lenis({ lerp: 0.09, wheelMultiplier: 1 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
  }
  function scrollToTarget(sel) {
    var el = document.querySelector(sel);
    if (!el) return;
    if (lenis) lenis.scrollTo(el, { offset: -80 });
    else el.scrollIntoView({ behavior: 'smooth' });
  }
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (id.length > 1 && document.querySelector(id)) { e.preventDefault(); scrollToTarget(id); }
    });
  });

  /* ---------------- Split text helpers ---------------- */
  function splitChars(el) {
    var text = el.textContent;
    el.textContent = '';
    el.setAttribute('aria-label', text);
    var frag = document.createDocumentFragment();
    text.split(/(\s+)/).forEach(function (part) {
      if (!part) return;
      if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
      var w = document.createElement('span'); w.className = 'word';
      part.split('').forEach(function (c) {
        var m = document.createElement('span'); m.className = 'mask';
        var ch = document.createElement('span'); ch.className = 'ch'; ch.textContent = c;
        m.appendChild(ch); w.appendChild(m);
      });
      frag.appendChild(w);
    });
    el.appendChild(frag);
    return el.querySelectorAll('.ch');
  }
  function splitWords(el, cls) {
    var out = [];
    var html = el.innerHTML;
    el.innerHTML = '';
    html.split(/(\s+)/).forEach(function (part) {
      if (!part) return;
      if (/^\s+$/.test(part)) { el.appendChild(document.createTextNode(' ')); return; }
      var w = document.createElement('span'); w.className = 'word';
      part.split('').forEach(function (c) {
        var ch = document.createElement('span'); ch.className = cls || 'hl-char'; ch.textContent = c;
        w.appendChild(ch); out.push(ch);
      });
      el.appendChild(w);
    });
    return out;
  }

  /* ---------------- Preloader + hero entrance ---------------- */
  var preloader = document.getElementById('preloader');
  var page = document.getElementById('page');

  function heroIntro() {
    var tl = gsap.timeline({ defaults: { ease: 'expo.out' } });
    // masked letter roll on hero title
    document.querySelectorAll('[data-hero-title]').forEach(function (t) {
      var chars = splitChars(t);
      gsap.set(chars, { yPercent: 110 });
      tl.to(chars, { yPercent: 0, duration: 1.1, stagger: 0.028 }, 0.1);
    });
    // thumbnails stagger
    var thumbs = document.querySelectorAll('[data-hero-thumb]');
    if (thumbs.length) {
      gsap.set(thumbs, { y: 40, opacity: 0 });
      tl.to(thumbs, { y: 0, opacity: 1, duration: 0.9, stagger: 0.09 }, 0.5);
    }
    // chrome fade
    var chrome = document.querySelectorAll('[data-hero-chrome]');
    if (chrome.length) {
      gsap.set(chrome, { y: 16, opacity: 0 });
      tl.to(chrome, { y: 0, opacity: 1, duration: 0.8, stagger: 0.07 }, 0.7);
    }
    // hero image clip expand
    var heroImg = document.querySelector('[data-hero-img]');
    if (heroImg) {
      gsap.set(heroImg, { clipPath: 'inset(12% 8% 12% 8% round 24px)' });
      tl.to(heroImg, { clipPath: 'inset(0% 0% 0% 0% round 0px)', duration: 1.4, ease: 'expo.inOut' }, 0.3);
    }
    return tl;
  }

  function runPreloader() {
    if (!preloader) { heroIntro(); return; }
    if (REDUCED) {
      preloader.style.display = 'none';
      document.querySelectorAll('[data-hero-title]').forEach(function (t) { splitChars(t); });
      return;
    }
    var logo = preloader.querySelector('.pl-logo');
    var tl = gsap.timeline();
    // stage 1: logo in, page hidden behind a thin letterbox slit
    if (page) gsap.set(page, { clipPath: 'polygon(9% 88%, 91% 88%, 91% 94%, 9% 94%)' });
    gsap.set(logo, { opacity: 0, y: 20 });
    tl.to(logo, { opacity: 1, y: 0, duration: 0.9, ease: 'expo.out' }, 0.2)
      // stage 2: curtain lift — overlay collapses, page expands from the slit
      .to(preloader, { scaleY: 0, transformOrigin: 'top', duration: 1.4, ease: 'expo.inOut' }, 1.2)
      .to(logo, { opacity: 0, y: -20, duration: 0.5, ease: 'expo.in' }, 1.5);
    if (page) tl.to(page, { clipPath: 'polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)', duration: 1.6, ease: 'expo.inOut' }, 1.2);
    tl.set(preloader, { display: 'none' })
      .add(heroIntro(), '-=0.55');
  }
  // lock scroll during preload
  if (lenis) lenis.stop();
  window.addEventListener('load', function () {
    runPreloader();
    if (lenis) lenis.start();
    ScrollTrigger.refresh();
  });
  // fallback if load already fired
  if (document.readyState === 'complete') {
    runPreloader();
    if (lenis) lenis.start();
  }

  /* ---------------- Hero background crossfade ---------------- */
  var bgImgs = document.querySelectorAll('.hero-bg img');
  if (bgImgs.length > 1 && !REDUCED) {
    var bi = 0;
    bgImgs[0].classList.add('on');
    gsap.set(bgImgs[0], { opacity: 1 });
    setInterval(function () {
      var prev = bgImgs[bi];
      bi = (bi + 1) % bgImgs.length;
      var next = bgImgs[bi];
      next.classList.add('on');
      gsap.to(next, { opacity: 1, duration: 1.6, ease: 'sine.inOut' });
      gsap.to(prev, { opacity: 0, duration: 1.6, ease: 'sine.inOut', onComplete: function () { prev.classList.remove('on'); } });
    }, 6000);
  } else if (bgImgs.length) { bgImgs[0].style.opacity = 1; }

  /* ---------------- Hero parallax on scroll ---------------- */
  document.querySelectorAll('[data-hero-parallax]').forEach(function (el) {
    if (REDUCED) return;
    gsap.to(el, {
      yPercent: -18, opacity: 0.15, ease: 'none',
      scrollTrigger: { trigger: el.closest('.hero') || el, start: 'top top', end: 'bottom top', scrub: true }
    });
  });

  /* ---------------- Blur-to-sharp reveals ---------------- */
  document.querySelectorAll('[data-reveal]').forEach(function (el) {
    if (REDUCED) { el.style.opacity = 1; return; }
    var delay = parseFloat(el.getAttribute('data-delay') || 0);
    gsap.fromTo(el, { opacity: 0, y: 36, filter: 'blur(16px)' }, {
      opacity: 1, y: 0, filter: 'blur(0px)', duration: 1.1, ease: 'expo.out', delay: delay,
      scrollTrigger: { trigger: el, start: 'top 88%', once: true }
    });
  });

  /* ---------------- Scroll-scrubbed char highlight ---------------- */
  document.querySelectorAll('[data-highlight]').forEach(function (el) {
    var chars = splitWords(el, 'hl-char');
    if (REDUCED) { chars.forEach(function (c) { c.style.opacity = 1; }); return; }
    gsap.to(chars, {
      opacity: 1, stagger: 0.06, ease: 'none',
      scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 45%', scrub: 0.6 }
    });
  });

  /* ---------------- Fast letter cascade ---------------- */
  document.querySelectorAll('[data-cascade]').forEach(function (el) {
    var chars = splitChars(el);
    if (REDUCED) return;
    gsap.set(chars, { opacity: 0, filter: 'blur(6px)' });
    gsap.to(chars, {
      opacity: 1, filter: 'blur(0px)', duration: 0.5, stagger: 0.008, ease: 'power2.out',
      scrollTrigger: { trigger: el, start: 'top 85%', once: true }
    });
  });

  /* ---------------- Continuous marquee ---------------- */
  document.querySelectorAll('[data-marquee]').forEach(function (track) {
    if (REDUCED) return;
    var w = track.scrollWidth / 2;
    gsap.to(track, { x: -w, duration: parseFloat(track.getAttribute('data-speed') || 22), ease: 'none', repeat: -1 });
  });

  /* ---------------- Scroll-scrubbed marquee ---------------- */
  document.querySelectorAll('[data-marquee-scrub]').forEach(function (el) {
    if (REDUCED) return;
    var dir = el.getAttribute('data-dir') === 'right' ? 1 : -1;
    gsap.fromTo(el, { xPercent: dir > 0 ? -12 : 0 }, {
      xPercent: dir > 0 ? 0 : -12, ease: 'none',
      scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: 1 }
    });
  });

  /* ---------------- Pinned 3D cube ---------------- */
  var cubePin = document.querySelector('[data-cube-pin]');
  var cube = document.querySelector('[data-cube]');
  if (cubePin && cube && !REDUCED) {
    gsap.to(cube, {
      rotationY: -270, ease: 'none',
      scrollTrigger: { trigger: cubePin, start: 'top top', end: '+=300%', pin: true, scrub: 0.8 }
    });
  }

  /* ---------------- Perspective de-skew ---------------- */
  document.querySelectorAll('[data-deskew]').forEach(function (el) {
    if (REDUCED) return;
    gsap.fromTo(el, { rotationX: 14, rotationY: -10, transformPerspective: 1200, y: 60 }, {
      rotationX: 0, rotationY: 0, y: 0, ease: 'none',
      scrollTrigger: { trigger: el, start: 'top 95%', end: 'top 40%', scrub: 1 }
    });
  });

  /* ---------------- Odometer counters ---------------- */
  document.querySelectorAll('[data-count]').forEach(function (el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    if (REDUCED) { el.textContent = target; return; }
    var cols = [];
    String(target).split('').forEach(function (d) {
      var col = document.createElement('span'); col.className = 'digit-col';
      for (var i = 0; i <= 9; i++) { var s = document.createElement('span'); s.textContent = i; col.appendChild(s); }
      el.appendChild(col); cols.push({ col: col, digit: parseInt(d, 10) });
    });
    ScrollTrigger.create({
      trigger: el, start: 'top 85%', once: true,
      onEnter: function () {
        cols.forEach(function (c, i) {
          gsap.to(c.col, { y: -(c.digit * 1.15) + 'em', duration: 1.6, delay: i * 0.12, ease: 'expo.out' });
        });
      }
    });
  });

  /* ---------------- Draggable rail ---------------- */
  document.querySelectorAll('[data-drag]').forEach(function (rail) {
    var down = false, startX = 0, startL = 0;
    rail.addEventListener('pointerdown', function (e) { down = true; startX = e.clientX; startL = rail.scrollLeft; });
    window.addEventListener('pointermove', function (e) { if (down) rail.scrollLeft = startL - (e.clientX - startX); });
    window.addEventListener('pointerup', function () { down = false; });
  });

  /* ---------------- Hover image reveal ---------------- */
  var hoverBox = document.getElementById('hover-reveal');
  if (hoverBox && FINE_POINTER && !REDUCED) {
    var hx = gsap.quickTo(hoverBox, 'left', { duration: 0.5, ease: 'expo.out' });
    var hy = gsap.quickTo(hoverBox, 'top', { duration: 0.5, ease: 'expo.out' });
    window.addEventListener('mousemove', function (e) { hx(e.clientX); hy(e.clientY); });
    document.querySelectorAll('[data-hover-image]').forEach(function (link) {
      link.addEventListener('mouseenter', function () {
        var img = hoverBox.querySelector('img');
        img.src = link.getAttribute('data-hover-image');
        gsap.to(hoverBox, { opacity: 1, scale: 1, duration: 0.45, ease: 'expo.out' });
      });
      link.addEventListener('mouseleave', function () {
        gsap.to(hoverBox, { opacity: 0, scale: 0.85, duration: 0.35, ease: 'expo.in' });
      });
    });
  }

  /* ---------------- CTA letter wave (scrubbed) ---------------- */
  document.querySelectorAll('[data-wave]').forEach(function (el) {
    var chars = splitChars(el);
    if (REDUCED) return;
    chars.forEach(function (c, i) { gsap.set(c, { y: (i % 2 === 0 ? 0.12 : -0.12) + 'em' }); });
    gsap.to(chars, {
      y: '0em', stagger: { each: 0.05 }, ease: 'none',
      scrollTrigger: { trigger: el, start: 'top 95%', end: 'top 35%', scrub: 1 }
    });
  });

  /* ---------------- Progressive blur gradient (CTA) ---------------- */
  document.querySelectorAll('.cta-blur').forEach(function (wrap) {
    if (REDUCED) return;
    for (var i = 1; i <= 8; i++) {
      var l = document.createElement('div');
      var start = 100 - i * 12;
      l.style.position = 'absolute'; l.style.inset = '0';
      l.style.backdropFilter = 'blur(' + (i * 4) + 'px)';
      l.style.webkitBackdropFilter = 'blur(' + (i * 4) + 'px)';
      var m = 'linear-gradient(to bottom, transparent ' + start + '%, black 100%)';
      l.style.maskImage = m; l.style.webkitMaskImage = m;
      wrap.appendChild(l);
    }
  });

  /* ---------------- FAQ accordion ---------------- */
  document.querySelectorAll('.faq-item').forEach(function (item) {
    var q = item.querySelector('.faq-q');
    var a = item.querySelector('.faq-a');
    q.addEventListener('click', function () {
      var open = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(function (o) {
        o.classList.remove('open');
        gsap.to(o.querySelector('.faq-a'), { maxHeight: 0, duration: 0.5, ease: 'expo.out' });
      });
      if (!open) {
        item.classList.add('open');
        gsap.to(a, { maxHeight: a.scrollHeight + 'px', duration: 0.6, ease: 'expo.out' });
      }
    });
  });

  /* ---------------- Image wipe (studio page) ---------------- */
  document.querySelectorAll('[data-wipe]').forEach(function (frame) {
    var top = frame.querySelector('.wipe-top');
    if (!top || REDUCED) return;
    gsap.to(top, {
      xPercent: -101, ease: 'none',
      scrollTrigger: { trigger: frame.closest('.wipe-wrap'), start: 'top top', end: 'bottom bottom', scrub: 1 }
    });
  });

  /* ---------------- Collage cards drift ---------------- */
  document.querySelectorAll('.collage-card').forEach(function (card, i) {
    if (REDUCED) return;
    gsap.from(card, {
      y: 120, opacity: 0, rotation: (i % 2 ? 10 : -10), duration: 1.2, ease: 'expo.out', delay: 0.15 * i,
      scrollTrigger: { trigger: card.closest('.collage'), start: 'top 70%', once: true }
    });
    gsap.to(card, {
      y: (i % 2 ? -40 : 40), ease: 'none',
      scrollTrigger: { trigger: card.closest('.collage'), start: 'top bottom', end: 'bottom top', scrub: 1.2 }
    });
  });

  /* ---------------- Custom cursor ---------------- */
  var cursor = document.getElementById('cursor');
  if (cursor && FINE_POINTER && !REDUCED) {
    var cx = gsap.quickTo(cursor, 'left', { duration: 0.18, ease: 'power2.out' });
    var cy = gsap.quickTo(cursor, 'top', { duration: 0.18, ease: 'power2.out' });
    window.addEventListener('mousemove', function (e) { cx(e.clientX); cy(e.clientY); });
    document.querySelectorAll('[data-cursor]').forEach(function (el) {
      el.addEventListener('mouseenter', function () {
        cursor.classList.add('big');
        cursor.querySelector('.cursor-label').textContent = el.getAttribute('data-cursor');
      });
      el.addEventListener('mouseleave', function () { cursor.classList.remove('big'); });
    });
  } else if (cursor) { cursor.style.display = 'none'; }

  /* ---------------- Burger menu ---------------- */
  var burger = document.getElementById('burger');
  var links = document.getElementById('navLinks');
  if (burger && links) {
    burger.addEventListener('click', function () { links.classList.toggle('open'); });
  }

  /* ---------------- Footer year ---------------- */
  var yr = document.getElementById('year');
  if (yr) yr.textContent = new Date().getFullYear();

  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
