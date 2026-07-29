// Pain 2 Power video page — click-to-load YouTube players.
// The page ships only thumbnails; no YouTube script or iframe loads until a
// visitor presses play (same facade pattern as the Spotify show player).
(function () {
  'use strict';
  document.querySelectorAll('.vid-facade').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var iframe = document.createElement('iframe');
      iframe.src = btn.dataset.embed;
      iframe.title = btn.dataset.title || 'Pain 2 Power video';
      iframe.className = 'vid-embed';
      iframe.setAttribute('frameborder', '0');
      iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
      iframe.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
      iframe.allowFullscreen = true;
      btn.replaceWith(iframe);
      iframe.focus();
    });
  });
})();
