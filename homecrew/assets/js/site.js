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
