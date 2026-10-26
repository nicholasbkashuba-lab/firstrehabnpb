/* Consent-gated Google Analytics 4 (added 2026-10-26).
   head() in build.py emits this file with data-ga="<measurement id>" on every page.
   Nothing loads from Google until the visitor clicks Allow; "No thanks" is
   remembered and nothing loads, ever. The appointment form sits on most pages
   and the intake chat on all of them, so GA must not start on its own.
   window.gtag is defined here, before any choice, so the gtag('event', ...) calls
   in main.js and intake.js only queue into dataLayer and send nothing unless
   gtag.js is later loaded. Vercel Web Analytics is cookieless and is not gated. */
(() => {
  "use strict";
  const me = document.currentScript;
  const id = me && me.dataset.ga;
  if (!id) return;
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  // Consent Mode v2: everything denied until the visitor accepts.
  window.gtag("consent", "default", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "denied" });
  window.gtag("set", "ads_data_redaction", true);
  window.gtag("set", "url_passthrough", false);

  const KEY = "fr-consent";
  let choice = null;
  try { choice = localStorage.getItem(KEY); } catch (_) {}

  const load = () => {
    window.gtag("consent", "update", { analytics_storage: "granted" });
    const s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
    document.head.appendChild(s);
    window.gtag("js", new Date());
    // No Google Signals, no ad personalization, and the page path only (no query strings).
    window.gtag("config", id, { allow_google_signals: false, allow_ad_personalization_signals: false, page_location: location.origin + location.pathname });
  };

  if (choice === "granted") { load(); return; }
  if (choice === "denied") return;

  const bar = document.createElement("div");
  bar.className = "consent-bar";
  bar.setAttribute("role", "region");
  bar.setAttribute("aria-label", "Cookie choice");
  bar.innerHTML = "<p>May we count visits with Google Analytics? It helps us see which pages help people. Nothing you type into a form or the chat is shared.</p>" +
    '<div class="consent-actions"><button type="button" class="btn btn-coral" data-c="granted">Allow</button>' +
    '<button type="button" class="btn btn-ghost" data-c="denied">No thanks</button></div>';
  bar.addEventListener("click", (e) => {
    const b = e.target.closest("[data-c]");
    if (!b) return;
    try { localStorage.setItem(KEY, b.dataset.c); } catch (_) {}
    if (b.dataset.c === "granted") load();
    bar.remove();
  });
  const show = () => document.body.appendChild(bar);
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", show, { once: true });
  else show();
})();
