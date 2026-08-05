document.getElementById('yr').textContent = new Date().getFullYear();
var b = document.getElementById('burger'), n = document.getElementById('navlinks');
b.addEventListener('click', function(){
  var open = n.classList.toggle('open');
  b.setAttribute('aria-expanded', open);
});
n.addEventListener('click', function(e){ if(e.target.tagName==='A') n.classList.remove('open'); });

/* Everything below is decoration. Guard it on the reduced-motion query and on
   IntersectionObserver so an older browser just gets the static page. */
var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
document.querySelectorAll('.proto-col, .pkg, .led-grp, .stat, .protect-grid > *')
  .forEach(function(el){ el.classList.add('reveal'); });
var revealables = document.querySelectorAll('.reveal');

if(still || !('IntersectionObserver' in window)){
  revealables.forEach(function(el){ el.classList.add('in'); });
} else {
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en, i){
      if(!en.isIntersecting) return;
      setTimeout(function(){ en.target.classList.add('in'); }, i * 70);
      io.unobserve(en.target);
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: .12 });
  revealables.forEach(function(el){ io.observe(el); });

  /* Count the stat numbers up once, when the bar first comes into view. */
  var counters = document.querySelectorAll('[data-count]');
  var cio = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(!en.isIntersecting) return;
      cio.unobserve(en.target);
      var target = parseInt(en.target.dataset.count, 10), t0 = null;
      requestAnimationFrame(function step(ts){
        if(t0 === null) t0 = ts;
        var p = Math.min((ts - t0) / 900, 1);
        en.target.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if(p < 1) requestAnimationFrame(step);
      });
    });
  }, { threshold: .6 });
  counters.forEach(function(el){ cio.observe(el); });
}

/* Nav: drop shadow once scrolled, and mark the section you are in. */
var nav = document.querySelector('.nav');
var sections = Array.prototype.filter.call(
  document.querySelectorAll('main section[id]'),
  function(s){ return document.querySelector('.nav-links a[href="#' + s.id + '"]'); }
);
function onScroll(){
  nav.classList.toggle('stuck', window.scrollY > 8);
  var y = window.scrollY + 140, active = null;
  sections.forEach(function(s){ if(s.offsetTop <= y) active = s.id; });
  document.querySelectorAll('.nav-links a').forEach(function(a){
    a.classList.toggle('here', !!active && a.getAttribute('href') === '#' + active);
  });
}
addEventListener('scroll', onScroll, { passive:true });
onScroll();

/* ==========================================================================
   VISUAL LAYER
   All of this is decoration on top of a document that already works. Every
   block below is guarded: if the feature is missing, or the visitor asked for
   reduced motion, the page just sits there as plain HTML and nothing breaks.
   ========================================================================== */
(function(){
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- reading progress on articles ---- */
  var article = document.querySelector('.prose.article');
  if (article && !calm) {
    var bar = document.createElement('div');
    bar.className = 'readbar';
    document.body.appendChild(bar);
    var onRead = function(){
      var box = article.getBoundingClientRect();
      var total = box.height - window.innerHeight;
      var done = total > 0 ? (-box.top) / total : 0;
      bar.style.width = Math.max(0, Math.min(1, done)) * 100 + '%';
    };
    addEventListener('scroll', onRead, { passive: true });
    addEventListener('resize', onRead);
    onRead();
  }

  /* ---- hero parallax ----
     Transform only, and only above 900px. On a phone this costs more than it
     is worth and the hero already stacks. */
  var heroArt = document.querySelector('.hero-art');
  var heroPhoto = document.querySelector('.hero-photo');
  if (heroArt && !calm && matchMedia('(min-width:900px)').matches) {
    var ticking = false;
    var park = function(){
      var y = window.scrollY;
      if (y > window.innerHeight) { ticking = false; return; }
      heroArt.style.transform = 'translate3d(0,' + (y * 0.16) + 'px,0)';
      if (heroPhoto) heroPhoto.style.transform = 'translate3d(0,' + (y * 0.09) + 'px,0)';
      ticking = false;
    };
    addEventListener('scroll', function(){
      if (!ticking) { ticking = true; requestAnimationFrame(park); }
    }, { passive: true });
  }

  /* ---- the home-base pulse on the coast map ----
     Started only when the map is actually on screen, so it is not animating
     off in a scrolled-past section burning battery. */
  var pulse = document.querySelector('.coast .pulse');
  if (pulse && !calm && 'IntersectionObserver' in window) {
    new IntersectionObserver(function(es){
      es.forEach(function(e){
        pulse.style.animation = e.isIntersecting ? 'hqpulse 2.8s ease-out infinite' : 'none';
      });
    }, { threshold: .1 }).observe(pulse.closest('svg'));
  }

  /* ---- map <-> county list cross-highlight ---- */
  var maps = document.querySelectorAll('.coast');
  Array.prototype.forEach.call(maps, function(map){
    var cities = map.querySelectorAll('.city');
    var focus = function(slug){
      Array.prototype.forEach.call(map.querySelectorAll('.cty'), function(c){
        if (c.classList.contains('on')) return;
        c.classList.toggle('hi', !!slug && c.dataset.cty === slug);
      });
      Array.prototype.forEach.call(cities, function(c){
        c.classList.toggle('dim', !!slug && c.dataset.in !== slug);
      });
    };
    Array.prototype.forEach.call(map.querySelectorAll('.cty'), function(c){
      c.addEventListener('mouseenter', function(){ focus(c.dataset.cty); });
      c.addEventListener('focus', function(){ focus(c.dataset.cty); });
    });
    map.addEventListener('mouseleave', function(){ focus(null); });
    /* the corridor list beside the map drives the same highlight */
    var host = map.closest('.mapwrap');
    if (!host) return;
    Array.prototype.forEach.call(host.querySelectorAll('.co[href]'), function(link){
      var slug = (link.getAttribute('href').split('/').pop() || '').replace('.html', '');
      link.addEventListener('mouseenter', function(){ focus(slug); });
      link.addEventListener('mouseleave', function(){ focus(null); });
    });
  });

  /* ---- protocol explorer ----
     Progressive enhancement: the markup ships with every panel visible and a
     tablist that does nothing. If this runs, panels collapse to one at a time.
     If it does not, all 25 checks are still on the page and readable. */
  var pex = document.querySelector('.pex');
  if (pex) {
    var tabs = pex.querySelectorAll('.pex-tab');
    var panels = pex.querySelectorAll('.pex-panel');
    var show = function(i){
      Array.prototype.forEach.call(tabs, function(t, n){
        t.setAttribute('aria-selected', n === i ? 'true' : 'false');
        t.setAttribute('tabindex', n === i ? '0' : '-1');
      });
      Array.prototype.forEach.call(panels, function(p, n){
        p.setAttribute('data-on', n === i ? '1' : '0');
      });
    };
    Array.prototype.forEach.call(tabs, function(t, i){
      t.addEventListener('click', function(){ show(i); });
      t.addEventListener('keydown', function(e){
        var j = e.key === 'ArrowDown' || e.key === 'ArrowRight' ? i + 1
              : e.key === 'ArrowUp'   || e.key === 'ArrowLeft'  ? i - 1 : -1;
        if (j < 0 || j >= tabs.length) return;
        e.preventDefault(); show(j); tabs[j].focus();
      });
    });
    show(0);
  }
})();
