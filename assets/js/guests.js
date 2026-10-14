// Pain 2 Power guests: directory filter chips + search (/guests.html), and the
// clip "show all" button on each profile (/guests/<slug>.html).
// Every card ships in the HTML; this only hides the ones that do not match,
// so the page reads fine with JavaScript off. ?q= and #category deep link.
(function () {
  'use strict';
  // Profile pages: the first six clips show, the rest wait behind a button.
  var moreBtn = document.querySelector('[data-gmore-btn]');
  if (moreBtn) {
    moreBtn.addEventListener('click', function () {
      var hidden = document.querySelectorAll('[data-gmore]');
      hidden.forEach(function (li) { li.hidden = false; });
      moreBtn.remove();
      var first = hidden[0] && hidden[0].querySelector('button');
      if (first) first.focus();
    });
  }
  var grid = document.querySelector('[data-ggrid]');
  if (!grid) return;
  var cards = Array.prototype.slice.call(grid.querySelectorAll('[data-guest]'));
  var chips = Array.prototype.slice.call(document.querySelectorAll('.gchip'));
  var input = document.querySelector('[data-gsearch]');
  var count = document.querySelector('[data-gcount]');
  var empty = document.querySelector('[data-gempty]');
  var cat = 'all';

  function apply() {
    var q = (input.value || '').trim().toLowerCase();
    var terms = q ? q.split(/\s+/) : [];
    var shown = 0;
    cards.forEach(function (c) {
      var ok = (cat === 'all' || c.dataset.cat === cat) &&
        terms.every(function (t) { return c.dataset.hay.indexOf(t) !== -1; });
      c.hidden = !ok;
      if (ok) shown++;
    });
    count.textContent = shown === cards.length
      ? 'Showing all ' + cards.length + ' guests'
      : 'Showing ' + shown + ' of ' + cards.length + ' guests';
    empty.hidden = shown !== 0;
  }

  function choose(key) {
    cat = key;
    chips.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.cat === key)); });
    apply();
  }

  chips.forEach(function (b) {
    b.addEventListener('click', function () {
      choose(b.dataset.cat);
      if (history.replaceState) history.replaceState(null, '', b.dataset.cat === 'all' ? location.pathname + location.search : '#' + b.dataset.cat);
    });
  });
  input.addEventListener('input', apply);

  var params = new URLSearchParams(location.search);
  if (params.get('q')) input.value = params.get('q');
  var hash = location.hash.slice(1);
  if (hash && chips.some(function (b) { return b.dataset.cat === hash; })) choose(hash); else apply();
})();
