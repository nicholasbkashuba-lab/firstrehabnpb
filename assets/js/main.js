// First Rehabilitation — v2 interactions
(function () {
  // Nudge the hero video: some browsers need an explicit play() after load,
  // and Low Power Mode pauses autoplay until the page is interacted with.
  const heroVideo = document.querySelector('.hero-media video');
  if (heroVideo) {
    const tryPlay = () => heroVideo.play().catch(() => {});
    tryPlay();
    heroVideo.addEventListener('canplay', tryPlay);
    document.addEventListener('touchstart', tryPlay, { once: true, passive: true });
    document.addEventListener('click', tryPlay, { once: true });
    document.addEventListener('visibilitychange', () => { if (!document.hidden) tryPlay(); });
  }

  const header = document.querySelector('.site-header');
  const onScroll = () => header && header.classList.toggle('scrolled', window.scrollY > 40);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile nav
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    const setOpen = (open) => {
      links.classList.toggle('open', open);
      toggle.classList.toggle('active', open);
      document.body.classList.toggle('nav-locked', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    toggle.addEventListener('click', () => setOpen(!links.classList.contains('open')));
    // Escape closes the menu and returns focus to the toggle
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && links.classList.contains('open')) {
        setOpen(false);
        toggle.focus();
      }
    });
    links.querySelectorAll('li').forEach((li) => {
      const item = li.querySelector(':scope > a.nav-item');
      const dd = li.querySelector(':scope > .dropdown');
      if (item && dd) {
        item.addEventListener('click', (e) => {
          if (window.matchMedia('(max-width: 1260px)').matches) {
            e.preventDefault();
            li.classList.toggle('open-sub');
          }
        });
      }
    });
  }

  // Scroll reveals
  const io = new IntersectionObserver(
    (entries) => entries.forEach((en) => en.isIntersecting && en.target.classList.add('in')),
    { threshold: 0.12 }
  );
  document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

  // Seamless marquees & tickers: tag alternating tilts BEFORE cloning so the
  // pattern stays identical across the loop seam even with an odd item count,
  // then duplicate the content once — the roll animation travels exactly -50%.
  document.querySelectorAll('.marquee, .ticker').forEach((track) => {
    Array.from(track.children).forEach((el, i) =>
      el.classList.add(i % 2 ? 'tilt-b' : 'tilt-a'));
    track.innerHTML += track.innerHTML;
  });

  // Animated counters (instant for prefers-reduced-motion users)
  const easeOut = (t) => 1 - Math.pow(1 - t, 3);
  const runCounter = (el) => {
    const target = parseFloat(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      el.textContent = target.toLocaleString() + suffix;
      return;
    }
    const dur = 1600;
    const start = performance.now();
    const step = (now) => {
      const p = Math.min((now - start) / dur, 1);
      const val = Math.round(target * easeOut(p));
      el.textContent = val.toLocaleString() + suffix;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const cio = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting && !en.target.dataset.done) {
        en.target.dataset.done = '1';
        runCounter(en.target);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('[data-count]').forEach((el) => cio.observe(el));

  // Body map: sync hotspot + list hover
  const link = (key, on) => {
    document.querySelectorAll(`[data-bm="${key}"]`).forEach((el) => el.classList.toggle('hot', on));
  };
  document.querySelectorAll('[data-bm]').forEach((el) => {
    el.addEventListener('mouseenter', () => link(el.dataset.bm, true));
    el.addEventListener('mouseleave', () => link(el.dataset.bm, false));
    el.addEventListener('focus', () => link(el.dataset.bm, true));
    el.addEventListener('blur', () => link(el.dataset.bm, false));
  });
})();

// Body map: tap-to-learn panel
(function () {
  const panel = document.getElementById('bm-panel');
  const dataEl = document.getElementById('bm-data');
  if (!panel || !dataEl) return;
  const DATA = JSON.parse(dataEl.textContent);
  const show = (key) => {
    const d = DATA[key];
    if (!d) return;
    panel.classList.remove('flash');
    void panel.offsetWidth; // restart animation
    panel.classList.add('flash');
    panel.innerHTML =
      '<span class="cond-tag">' + d.tag + '</span>' +
      '<h3>' + d.name + '</h3>' +
      '<p>' + d.lede + '</p>' +
      '<ul class="check-list">' + d.treats.map(t => '<li>' + t + '</li>').join('') + '</ul>' +
      '<a class="bm-cta" href="' + d.url + '">Explore this treatment &rarr;</a>';
    document.querySelectorAll('#bodymap [data-bm]').forEach(el =>
      el.classList.toggle('hot', el.dataset.bm === key));
    if (window.matchMedia('(max-width: 880px)').matches) {
      panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  };
  document.querySelectorAll('#bodymap [data-bm]').forEach((el) => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      show(el.dataset.bm);
    });
  });
})();
