/* ============================================================================
   LEGENDS RADIO 100.3 — front-end behaviour
   Persistent live player (real WLML stream) · client-side "On Air Now" engine
   computed in the station's Eastern time · scroll reveals · counters · nav ·
   marquees · forms. Zero dependencies. Reduced-motion aware.
   Data (schedule/stream) is injected by build.py as window.LEGENDS_*.
   ========================================================================== */
(function () {
  "use strict";
  var RM = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var SCHEDULE = window.LEGENDS_SCHEDULE || {};
  var STREAM = window.LEGENDS_STREAM || "";
  var POPOUT = window.LEGENDS_POPOUT || "https://legendsradio.com/listen-live/";

  /* ---------------------------------------------------------------- header */
  var header = $(".site-header");
  function onScroll() { if (header) header.classList.toggle("scrolled", window.scrollY > 24); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ------------------------------------------------------------- mobile nav */
  var toggle = $(".nav-toggle"), links = $(".nav-links");
  function closeNav() {
    if (!toggle) return;
    toggle.setAttribute("aria-expanded", "false");
    links.classList.remove("open");
    document.body.classList.remove("nav-open");
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      links.classList.toggle("open", !open);
      document.body.classList.toggle("nav-open", !open);
    });
    $$(".nav-links a").forEach(function (a) { a.addEventListener("click", closeNav); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeNav(); });
  }

  /* ================================================================ PLAYER */
  var audio = $("#legends-audio");
  var player = $(".player");
  var playBtns = $$("[data-play]");           // hero button + player button share control
  var volInput = $(".player-vol input");
  var vinyls = $$(".vinyl");
  var eqs = $$(".eq");
  var state = { playing: false, loading: false };

  function setEq(on) { eqs.forEach(function (e) { e.classList.toggle("playing", on); }); }
  function setVinyl(on) { vinyls.forEach(function (v) { v.classList.toggle("spinning", on); }); }
  function reflectUI() {
    if (player) player.classList.toggle("playing", state.playing);
    if (player) player.classList.toggle("loading", state.loading);
    playBtns.forEach(function (b) {
      b.setAttribute("aria-pressed", String(state.playing));
      b.classList.toggle("playing", state.playing);
      var lbl = b.querySelector("[data-play-label]");
      if (lbl) lbl.textContent = state.playing ? "Pause" : (b.dataset.playLabelText || "Listen Live");
    });
    setEq(state.playing); setVinyl(state.playing);
  }

  function play() {
    if (!audio) return;
    state.loading = true; reflectUI();
    // (re)attach the live source each play so we always reconnect to the live edge
    if (!audio.src) audio.src = STREAM;
    var p = audio.play();
    if (p && p.catch) p.catch(function () { onError(); });
  }
  function pause() { if (audio) { audio.pause(); try { audio.removeAttribute("src"); audio.load(); } catch (e) {} } }
  function toggle_() { state.playing ? pause() : play(); }

  function onError() {
    state.playing = false; state.loading = false; reflectUI();
    if (player) {
      var meta = $(".player-meta .p-host", player);
      if (meta) meta.innerHTML = 'Stream unavailable — <a href="' + POPOUT + '" target="_blank" rel="noopener" style="color:var(--gold);text-decoration:underline">open the pop-out player</a>';
    }
  }

  if (audio) {
    audio.addEventListener("playing", function () { state.playing = true; state.loading = false; reflectUI(); });
    audio.addEventListener("pause", function () { state.playing = false; state.loading = false; reflectUI(); });
    audio.addEventListener("waiting", function () { state.loading = true; reflectUI(); });
    audio.addEventListener("error", onError);
    audio.addEventListener("stalled", function () { /* keep trying */ });
    // volume
    var savedVol = parseFloat(localStorage.getItem("legends_vol"));
    audio.volume = isNaN(savedVol) ? 0.85 : savedVol;
    if (volInput) {
      volInput.value = String(Math.round(audio.volume * 100));
      volInput.addEventListener("input", function () {
        audio.volume = Math.min(1, Math.max(0, volInput.value / 100));
        localStorage.setItem("legends_vol", String(audio.volume));
      });
    }
  }
  playBtns.forEach(function (b) { b.addEventListener("click", toggle_); });

  // keyboard: space toggles when not typing in a field
  document.addEventListener("keydown", function (e) {
    if (e.code === "Space" && !/^(INPUT|TEXTAREA|SELECT|BUTTON|A)$/.test(document.activeElement.tagName)) {
      e.preventDefault(); toggle_();
    }
  });

  /* ===================================================== ON AIR NOW engine */
  // Current time in the station's timezone (America/New_York), tz-safe anywhere.
  function nowET() {
    var parts;
    try {
      parts = new Intl.DateTimeFormat("en-US", {
        timeZone: "America/New_York", weekday: "short", hour: "2-digit",
        minute: "2-digit", hour12: false
      }).formatToParts(new Date());
    } catch (e) { var d = new Date(); return { day: d.getDay(), min: d.getHours() * 60 + d.getMinutes() }; }
    var map = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 }, o = {};
    parts.forEach(function (p) { o[p.type] = p.value; });
    var h = parseInt(o.hour, 10); if (h === 24) h = 0;
    return { day: map[o.weekday], min: h * 60 + parseInt(o.minute, 10) };
  }
  function toMin(hhmm) { var a = hhmm.split(":"); return parseInt(a[0], 10) * 60 + parseInt(a[1], 10); }
  function fmt(hhmm) {
    var m = toMin(hhmm), h = Math.floor(m / 60), mm = m % 60;
    var ap = h >= 12 ? "PM" : "AM", h12 = h % 12; if (h12 === 0) h12 = 12;
    return h12 + (mm ? ":" + (mm < 10 ? "0" + mm : mm) : "") + " " + ap;
  }

  function currentSlot() {
    var t = nowET(), day = SCHEDULE[t.day] || [], i;
    for (i = 0; i < day.length; i++) {
      var s = toMin(day[i].start), e = toMin(day[i].end);
      if (e <= s) e = 1440; // safety
      if (t.min >= s && t.min < e) {
        return { slot: day[i], day: t.day, idx: i, now: t.min, start: s, end: e };
      }
    }
    return null;
  }
  function nextSlot(cur) {
    if (!cur) return null;
    var day = SCHEDULE[cur.day] || [];
    if (cur.idx + 1 < day.length) return day[cur.idx + 1];
    var nd = (cur.day + 1) % 7, nday = SCHEDULE[nd] || [];
    return nday[0] || null;
  }

  function paintNowPlaying() {
    var cur = currentSlot();
    var nxt = nextSlot(cur);
    var showName = cur ? cur.slot.show : "Nonstop Legends";
    var hostName = cur ? (cur.slot.host || "The Great American Songbook") : "The Great American Songbook";
    var timeStr = cur ? (fmt(cur.slot.start) + " – " + fmt(cur.slot.end) + " ET") : "";

    // hero now-playing card
    var hc = $("#np-show"); if (hc) hc.textContent = showName;
    var hh = $("#np-host"); if (hh) hh.textContent = hostName;
    var ht = $("#np-time"); if (ht) ht.textContent = timeStr;
    var hn = $("#np-next"); if (hn && nxt) hn.innerHTML = "Up next · <b>" + nxt.show + "</b> at " + fmt(nxt.start);

    // sticky player meta
    var ps = $(".player .p-show"); if (ps) ps.textContent = showName;
    var ph = $(".player .p-host");
    if (ph && ph.querySelector("a") === null) ph.textContent = hostName + (cur && !state.playing ? " · " + timeStr : "");

    // Media Session (lock-screen / OS media controls)
    if ("mediaSession" in navigator) {
      try {
        navigator.mediaSession.metadata = new MediaMetadata({
          title: showName, artist: hostName,
          album: "Legends Radio 100.3 FM",
          artwork: [{ src: (window.LEGENDS_ARTWORK || ""), sizes: "512x512", type: "image/png" }]
        });
      } catch (e) {}
    }

    // schedule grid live highlight + progress
    $$(".sched-row").forEach(function (row) { row.classList.remove("live"); var b = $(".s-progress", row); if (b) b.style.width = "0"; });
    if (cur) {
      var sel = '.sched-row[data-day="' + cur.day + '"][data-idx="' + cur.idx + '"]';
      var row = $(sel);
      if (row) {
        row.classList.add("live");
        var pct = ((cur.now - cur.start) / (cur.end - cur.start)) * 100;
        var bar = $(".s-progress", row); if (bar) bar.style.width = Math.max(2, Math.min(100, pct)) + "%";
      }
    }
  }
  if (Object.keys(SCHEDULE).length) { paintNowPlaying(); setInterval(paintNowPlaying, 30000); }

  /* --------------------------------------------------------- schedule tabs */
  var tabs = $$(".sched-tabs button");
  if (tabs.length) {
    function showDay(day) {
      tabs.forEach(function (t) { t.setAttribute("aria-selected", String(t.dataset.day === day)); });
      $$("[data-sched-day]").forEach(function (panel) {
        panel.hidden = panel.dataset.schedDay !== day;
      });
    }
    tabs.forEach(function (t) { t.addEventListener("click", function () { showDay(t.dataset.day); }); });
    // default to today (ET)
    showDay(String(nowET().day));
  }

  /* ------------------------------------------------------------- marquees */
  $$(".marquee-track").forEach(function (track) {
    var html = track.innerHTML; track.innerHTML = html + html; // duplicate for seamless -50% loop
  });

  /* ----------------------------------------------------- reveal on scroll */
  var reveals = $$(".reveal");
  if (RM || !("IntersectionObserver" in window)) {
    reveals.forEach(function (r) { r.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (r) { io.observe(r); });
  }

  /* ------------------------------------------------------------- counters */
  function runCounter(el) {
    var target = parseFloat(el.dataset.count) || 0;
    var suffix = el.dataset.suffix || "";
    var dur = 1400, t0 = null;
    if (RM) { el.textContent = format(target) + ""; wrapSuffix(el, suffix); return; }
    function format(n) { return Math.round(n).toLocaleString("en-US"); }
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur), eased = 1 - Math.pow(1 - p, 3);
      el.textContent = format(target * eased);
      if (p < 1) requestAnimationFrame(step); else { el.textContent = format(target); wrapSuffix(el, suffix); }
    }
    requestAnimationFrame(step);
  }
  function wrapSuffix(el, suffix) { if (suffix) { var s = document.createElement("span"); s.className = "suffix"; s.textContent = suffix; el.appendChild(s); } }
  var counters = $$("[data-count]");
  if (counters.length) {
    if (RM || !("IntersectionObserver" in window)) { counters.forEach(runCounter); }
    else {
      var co = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { runCounter(e.target); co.unobserve(e.target); } });
      }, { threshold: 0.6 });
      counters.forEach(function (c) { co.observe(c); });
    }
  }

  /* ---------------------------------------------------------------- forms */
  $$("form[data-endpoint]").forEach(function (form) {
    var status = $(".form-status", form);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var btn = $("[type=submit]", form); var orig = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
      var data = new FormData(form);
      fetch(form.dataset.endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (r) { if (!r.ok) throw new Error("bad"); return r.json().catch(function () { return {}; }); })
        .then(function () {
          if (status) { status.className = "form-status ok"; status.textContent = form.dataset.success || "Thank you — we’ll be in touch shortly."; }
          form.reset();
        })
        .catch(function () {
          if (status) { status.className = "form-status err"; status.innerHTML = 'Something went wrong. Please call us at <a href="tel:+15614696700" style="color:inherit;text-decoration:underline">(561) 469-6700</a>.'; }
        })
        .finally(function () { if (btn) { btn.disabled = false; btn.textContent = orig; } });
    });
  });

  /* --------------------------------------------------- footer year + boot */
  var y = $("#year"); if (y) y.textContent = new Date().getFullYear();
  reflectUI();
})();
