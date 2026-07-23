// Interactive Body Map — Level 2/3 behaviors + guided flow.
// Progressive enhancement: every page is a real, server-rendered URL (Level 1
// /body-map/, Level 2 /body-map/knee.html, Level 3 /body-map/knee/<part>.html)
// and works with no JS. This adds live layer isolation, structure highlighting,
// condition overlays, animated level transitions, and the tap-through guide.
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- Level 2: tissue layer toggles ----
  document.querySelectorAll('[data-layer-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var svg = document.querySelector('.bm-svg');
      if (!svg) return;
      var layer = btn.getAttribute('data-layer-toggle');
      document.querySelectorAll('[data-layer-toggle]').forEach(function (b) { b.classList.remove('is-on'); });
      btn.classList.add('is-on');
      if (layer === 'all') svg.removeAttribute('data-isolate');
      else svg.setAttribute('data-isolate', layer);
      svg.removeAttribute('data-active'); // clear any single-structure highlight
    });
  });

  // ---- Level 2: hover a structure (or its list row) highlights both ----
  function partsFor(id) { return document.querySelectorAll('.bm-svg [data-part="' + id + '"]'); }
  function rowsFor(id) { return document.querySelectorAll('.bm-struct[data-part="' + id + '"]'); }
  document.querySelectorAll('.bm-svg .bm-part').forEach(function (part) {
    var id = part.getAttribute('data-part') || part.id;
    part.addEventListener('mouseenter', function () { hi(id, true); });
    part.addEventListener('mouseleave', function () { hi(id, false); });
  });
  document.querySelectorAll('.bm-struct[data-part]').forEach(function (row) {
    var id = row.getAttribute('data-part');
    row.addEventListener('mouseenter', function () { hi(id, true); });
    row.addEventListener('mouseleave', function () { hi(id, false); });
  });
  function hi(id, on) {
    partsFor(id).forEach(function (p) { p.classList.toggle('is-hi', on); });
    rowsFor(id).forEach(function (r) { r.classList.toggle('is-hover', on); });
  }

  // ---- Level 3: condition selection swaps the illustration overlay ----
  var conds = document.querySelectorAll('.bm-cond[data-set-overlay]');
  if (conds.length) {
    var svg = document.querySelector('.bm-svg');
    conds.forEach(function (c) {
      c.setAttribute('tabindex', '0');
      c.setAttribute('role', 'button');
      c.setAttribute('aria-pressed', 'false');
      function toggle() {
        var ov = c.getAttribute('data-set-overlay');
        var active = svg.getAttribute('data-overlay') === ov;
        conds.forEach(function (o) { o.classList.remove('is-showing'); o.setAttribute('aria-pressed', 'false'); });
        if (active) { svg.removeAttribute('data-overlay'); }
        else { svg.setAttribute('data-overlay', ov); c.classList.add('is-showing'); c.setAttribute('aria-pressed', 'true'); }
      }
      c.addEventListener('click', toggle);
      c.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); } });
    });
  }

  // ---- Animated level transitions (fade/scale, then follow the link) ----
  if (!reduce) {
    document.querySelectorAll('a.bm-spot, a.bm-struct, a.bm-region-chip, a.bm-crumb-up').forEach(function (a) {
      a.addEventListener('click', function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank') return;
        var href = a.getAttribute('href');
        if (!href) return;
        e.preventDefault();
        var main = document.querySelector('main');
        main.classList.add('bm-leaving');
        setTimeout(function () { window.location.href = href; }, 240);
      });
    });
    // Entrance
    var main = document.querySelector('main');
    if (main && document.querySelector('.bm-stage, .bm-l1')) {
      main.classList.add('bm-entering');
      requestAnimationFrame(function () { requestAnimationFrame(function () { main.classList.remove('bm-entering'); }); });
    }
  }

  // ---- Guided "help me find my issue" tap-through ----
  var guide = document.querySelector('[data-guide]');
  if (guide) buildGuide(guide);

  function buildGuide(root) {
    // Pilot tree: every path resolves to the knee (the only wired region).
    // Non-diagnostic language throughout; framework extends to all regions later.
    var TREE = {
      start: { q: 'Where does it hurt most?', a: [
        { t: 'My knee', go: 'onset' },
        { t: 'Somewhere else', go: 'soon' }
      ]},
      onset: { q: 'Did it start suddenly, or come on gradually?', a: [
        { t: 'Suddenly (a specific moment)', go: 'sudden' },
        { t: 'Gradually, over time', go: 'gradual' }
      ]},
      sudden: { q: 'Since it started, does the knee feel unstable — like it might give way?', a: [
        { t: 'Yes, it feels unstable', result: 'ligament' },
        { t: 'No, but it catches or locks', result: 'meniscus' },
        { t: 'No — mostly just pain and swelling', result: 'meniscus' }
      ]},
      gradual: { q: 'Is the ache worse with rest and stiffness, or with a specific activity like stairs or jumping?', a: [
        { t: 'Stiff and achy, worse after rest', result: 'arthritis' },
        { t: 'Worse on stairs or after sitting', result: 'kneecap' },
        { t: 'Worse with jumping or repeated loading', result: 'tendon' }
      ]},
      soon: { q: null, note: 'The knee is our first fully-mapped region — more areas are coming soon. In the meantime, the fastest answer is a real evaluation.', result: 'general' }
    };
    var RESULTS = {
      ligament: { h: 'This often points toward a ligament', p: 'A knee that feels unstable after a sudden injury often involves a ligament like the ACL or MCL.', link: 'knee/acl.html', linkText: 'Explore the knee ligaments' },
      meniscus: { h: 'This often points toward the meniscus', p: 'Catching, locking, or pain along the joint line after a twist often involves a meniscus tear.', link: 'knee/medial-meniscus.html', linkText: 'Explore the meniscus' },
      arthritis: { h: 'This often points toward the cartilage', p: 'Stiffness and aching that’s worse after rest is a common pattern with knee osteoarthritis, a wearing of the joint cartilage.', link: 'knee/femoral-cartilage.html', linkText: 'Explore the cartilage' },
      kneecap: { h: 'This often points toward the kneecap', p: 'Pain on stairs or after sitting is a classic kneecap (patellofemoral) pattern.', link: 'knee/femoral-cartilage.html', linkText: 'Explore kneecap pain' },
      tendon: { h: 'This often points toward the patellar tendon', p: 'Pain just below the kneecap that flares with jumping or loading often involves the patellar tendon.', link: 'knee/patellar-tendon.html', linkText: 'Explore the patellar tendon' },
      general: { h: 'Let’s get you evaluated', p: 'An evaluation is the surest way to understand what’s going on.', link: null, linkText: null }
    };

    var stage = root.querySelector('.bm-guide-stage');
    var atRoot = (typeof BM_BASE !== 'undefined');
    function render(nodeKey) {
      var node = TREE[nodeKey];
      stage.innerHTML = '';
      var card = document.createElement('div'); card.className = 'bm-guide-card';
      if (node.q) {
        var h = document.createElement('p'); h.className = 'bm-guide-q'; h.textContent = node.q; card.appendChild(h);
        var opts = document.createElement('div'); opts.className = 'bm-guide-opts';
        node.a.forEach(function (opt) {
          var b = document.createElement('button'); b.type = 'button'; b.className = 'bm-guide-opt'; b.textContent = opt.t;
          b.addEventListener('click', function () { opt.result ? showResult(opt.result) : render(opt.go); });
          opts.appendChild(b);
        });
        card.appendChild(opts);
      } else if (node.note) {
        showResult(node.result, node.note); return;
      }
      stage.appendChild(card);
      stage.scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
    }
    function showResult(key, note) {
      var r = RESULTS[key];
      stage.innerHTML = '';
      var card = document.createElement('div'); card.className = 'bm-guide-card bm-guide-result';
      var h = document.createElement('h3'); h.textContent = r.h; card.appendChild(h);
      var p = document.createElement('p'); p.textContent = note || r.p; card.appendChild(p);
      var row = document.createElement('div'); row.className = 'bm-guide-actions';
      if (r.link) {
        var a = document.createElement('a'); a.className = 'btn btn-ink'; a.href = r.link; a.textContent = r.linkText;
        row.appendChild(a);
      }
      var cta = document.createElement('a'); cta.className = 'btn btn-coral'; cta.href = '../contact.html'; cta.textContent = "Let's get you evaluated";
      row.appendChild(cta);
      card.appendChild(row);
      var dis = document.createElement('p'); dis.className = 'bm-guide-disc'; dis.textContent = 'This is educational only and is not a diagnosis. Only an in-person evaluation can tell you what’s really going on.';
      card.appendChild(dis);
      var again = document.createElement('button'); again.type = 'button'; again.className = 'bm-guide-restart'; again.textContent = '↺ Start over';
      again.addEventListener('click', function () { render('start'); });
      card.appendChild(again);
      stage.appendChild(card);
      stage.scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
    }
    render('start');
  }
})();
