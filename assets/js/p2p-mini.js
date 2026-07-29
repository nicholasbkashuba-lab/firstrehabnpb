// Floating Pain 2 Power mini-player.
// Sits beside the intake launcher on every page. Starts collapsed and opens
// ONLY on click — never on hover, never on a timer. The Spotify iframe is
// created on first open, so no third-party request happens until asked.
(function () {
  'use strict';
  var root = document.querySelector('[data-p2p]');
  if (!root) return;

  var btn = root.querySelector('.p2p-btn');
  var panel = root.querySelector('.p2p-panel');
  var closeBtn = root.querySelector('.p2p-x');
  var slot = root.querySelector('.p2p-embed');
  var loaded = false;

  function mountPlayer() {
    if (loaded || !slot) return;
    var iframe = document.createElement('iframe');
    iframe.src = slot.dataset.embed;
    iframe.title = slot.dataset.embedTitle || 'Pain 2 Power player';
    iframe.width = '100%';
    iframe.height = '152';
    iframe.frameBorder = '0';
    iframe.loading = 'lazy';
    iframe.style.borderRadius = '12px';
    iframe.allow = 'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture';
    slot.appendChild(iframe);
    loaded = true;
  }

  function open() {
    mountPlayer();
    // the assistant's teaser bubble occupies the same airspace — retire it
    var teaser = document.querySelector('.fri-teaser');
    if (teaser) teaser.classList.remove('show');
    panel.hidden = false;
    // next frame so the transition runs from the collapsed state
    requestAnimationFrame(function () { root.classList.add('is-open'); });
    btn.setAttribute('aria-expanded', 'true');
  }

  function close() {
    root.classList.remove('is-open');
    btn.setAttribute('aria-expanded', 'false');
    // keep the iframe mounted (so playback isn't killed) but hide the panel
    // once the collapse transition finishes
    setTimeout(function () {
      if (!root.classList.contains('is-open')) panel.hidden = true;
    }, 260);
  }

  function toggle() {
    root.classList.contains('is-open') ? close() : open();
  }

  btn.addEventListener('click', toggle);
  if (closeBtn) closeBtn.addEventListener('click', function () { close(); btn.focus(); });

  // Escape closes; click outside closes. Playback continues either way.
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && root.classList.contains('is-open')) { close(); btn.focus(); }
  });
  document.addEventListener('click', function (e) {
    if (root.classList.contains('is-open') && !root.contains(e.target)) close();
  });

  // Don't fight the intake assistant for the corner. Its open panel covers this
  // button anyway, so collapse the player and hide the button entirely while the
  // assistant is up, then restore it when the assistant closes.
  var intake = document.querySelector('.fri-root');
  if (intake && window.MutationObserver) {
    var sync = function () {
      var assistantOpen = intake.classList.contains('open');
      if (assistantOpen && root.classList.contains('is-open')) close();
      root.classList.toggle('is-hidden', assistantOpen);
    };
    new MutationObserver(sync).observe(intake, { attributes: true, attributeFilter: ['class'] });
    sync();
  }
})();
