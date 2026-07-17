/* ============================================================
   FIRST REHABILITATION — Intake Assistant
   Chat-style concierge that greets visitors, collects inquiry +
   contact details, and delivers them to the clinic.

   Data safety, in order:
     1. Every answer is saved to localStorage immediately (drafts
        survive refreshes and navigation).
     2. Submissions insert into Supabase (insert-only anon policy).
     3. A copy is emailed to the clinic inbox via FormSubmit.
     4. If the network fails, the lead is queued locally and
        retried automatically on every page view + when the
        browser comes back online.
   ============================================================ */
(function () {
  'use strict';
  if (window.__friLoaded) return;
  window.__friLoaded = true;

  var CFG = {
    supabaseUrl: 'https://pclqpthqigsfteyluwqj.supabase.co',
    supabaseKey: 'sb_publishable_ERdB1Hn8B5cZ74Lq8otSKg_3bSwv5_K',
    table: 'intake_leads',
    notifyEmail: 'firstrehabnpb@gmail.com',
    phone: '561-624-4263',
    phoneHref: 'tel:+15616244263',
    autoOpenDelay: 4500,
    contactPageDelay: 1600
  };

  var KEYS = { draft: 'fr.intake.draft.v1', queue: 'fr.intake.queue.v1', done: 'fr.intake.done.v1', auto: 'fr.intake.auto.v1' };

  // Resolve asset base from this script's own URL so it works at any page depth.
  var base = '';
  var self = document.currentScript || (function () {
    var s = document.querySelectorAll('script[src]');
    for (var i = 0; i < s.length; i++) if (/intake\.js/.test(s[i].src)) return s[i];
    return null;
  })();
  if (self && self.src) base = self.src.replace(/assets\/js\/intake\.js.*$/, '');

  // ---------- tiny storage helpers (never throw) ----------
  function store(kind) {
    try { return kind === 's' ? window.sessionStorage : window.localStorage; } catch (e) { return null; }
  }
  function get(key, kind) {
    var s = store(kind); if (!s) return null;
    try { return JSON.parse(s.getItem(key)); } catch (e) { return null; }
  }
  function set(key, val, kind) {
    var s = store(kind); if (!s) return;
    try { s.setItem(key, JSON.stringify(val)); } catch (e) { /* full/blocked */ }
  }
  function del(key, kind) {
    var s = store(kind); if (!s) return;
    try { s.removeItem(key); } catch (e) {}
  }

  // ---------- DOM ----------
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  var chatIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>';
  var closeIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>';
  var sendIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>';

  var root = el('div', 'fri-root');
  root.innerHTML =
    '<div class="fri-teaser" role="button" tabindex="0" aria-label="Open chat assistant">' +
      '<button class="fri-teaser-x" aria-label="Dismiss">&#10005;</button>' +
      '👋 <strong>Hi there!</strong> Want us to call you about an appointment? I can take your info in under a minute.' +
    '</div>' +
    '<button class="fri-launcher" aria-label="Chat with First Rehabilitation" aria-haspopup="dialog">' + chatIcon + '<span class="fri-dot"></span></button>' +
    '<div class="fri-panel" role="dialog" aria-modal="false" aria-label="First Rehabilitation intake assistant">' +
      '<div class="fri-head">' +
        '<img src="' + base + 'assets/media/logo-dark.png" alt="">' +
        '<div class="fri-who">' +
          '<div class="fri-title">First Rehab Assistant</div>' +
          '<div class="fri-sub">Front desk replies within one business day</div>' +
        '</div>' +
        '<button class="fri-x" aria-label="Close chat">' + closeIcon + '</button>' +
      '</div>' +
      '<div class="fri-log" aria-live="polite"></div>' +
      '<div class="fri-bar">' +
        '<input class="fri-input" type="text" maxlength="600" placeholder="Type here&hellip;" aria-label="Your reply">' +
        '<button class="fri-send" aria-label="Send">' + sendIcon + '</button>' +
      '</div>' +
      '<div class="fri-privacy">This assistant provides general information, not medical advice.<br>Private &amp; secure &middot; or call <a href="' + CFG.phoneHref + '" style="color:inherit;font-weight:600;">' + CFG.phone + '</a></div>' +
    '</div>';

  var teaser, launcher, panel, log, input, sendBtn;

  // ---------- conversation engine ----------
  var flow = { state: 'intent', data: {} };
  var busy = false;      // true while bot is "typing"
  var chipsEl = null;

  var TOPICS = ['Physical Therapy', 'Occupational Therapy', 'Hand Therapy', 'Wellness & Gym', 'Not sure yet'];
  var INSURERS = ['Medicare', 'Blue Cross', 'Aetna', 'Humana', 'Self-pay', 'Skip'];

  var STEPS = {
    intent: {
      prompt: function () {
        return ['👋 Welcome to First Rehabilitation! I’m the clinic’s virtual assistant. I can answer questions about our services, hours, and insurance — or take your info so our front desk can call you back.',
                'What brings you in today?'];
      },
      chips: function () {
        return [
          { label: '📅 Request an appointment', value: 'appointment', cls: 'primary' },
          { label: '💬 Ask a question', value: 'faq' },
          { label: '👀 Just looking around', value: 'browsing' }
        ];
      },
      accept: function (v) {
        var t = v.toLowerCase();
        if (t.indexOf('appoint') > -1 || t === 'appointment') return { value: 'appointment', echo: 'Request an appointment' };
        if (t === 'faq' || t === 'question' || t === 'ask a question') return { value: 'faq', echo: 'Ask a question' };
        if (t === 'browsing' || t.indexOf('looking') > -1 || t.indexOf('brows') > -1) return { value: 'browsing', echo: 'Just looking around' };
        // Anything else typed here is a real question — hand it to the front desk.
        flow.data.pendingTyped = v;
        return { value: 'faq', echo: v };
      },
      save: 'intent',
      next: function (d) {
        if (d.intent === 'browsing') return 'browse_end';
        if (d.intent === 'faq') return 'faq';
        return 'topic';
      }
    },
    faq: {},
    browse_end: {
      terminal: true,
      prompt: function () {
        return ['Enjoy the site! I’ll be right here in the corner if anything starts aching. 😊 You can also call us anytime at <a href="' + CFG.phoneHref + '">' + CFG.phone + '</a>.'];
      },
      chips: function () {
        return [
          { label: '📅 Actually, book me in', value: 'restart-appointment' },
          { label: '💬 I do have a question', value: 'ask-faq' }
        ];
      }
    },
    topic: {
      prompt: function () { return ['Wonderful — what kind of care are you looking for?']; },
      chips: function () {
        return TOPICS.map(function (t) { return { label: t, value: t }; });
      },
      accept: function (v) { return { value: v, echo: v }; },
      save: 'topic',
      next: function () { return 'message'; }
    },
    message: {
      prompt: function (d) {
        return d.intent === 'question'
          ? ['Of course — what would you like to ask? I’ll pass it straight to our team.']
          : ['Tell me a little about what’s going on — where does it hurt, or what happened? A sentence or two is perfect. <span class="fri-note">No detailed medical history needed — just the basics, please.</span>'];
      },
      accept: function (v) {
        if (v.length < 2) return { error: 'Could you give me just a few words about it?' };
        return { value: v, echo: v };
      },
      save: 'message',
      next: function () { return 'name'; }
    },
    name: {
      prompt: function () { return ['Great — let’s get your contact details so our front desk can reach you. First, what’s your <strong>first and last name</strong>?']; },
      accept: function (v) {
        if (v.replace(/[^a-zA-ZÀ-ɏ]/g, '').length < 2) return { error: 'Please type your first and last name.' };
        return { value: v, echo: v };
      },
      save: 'full_name',
      next: function () { return 'phone'; }
    },
    phone: {
      prompt: function (d) {
        var first = (d.full_name || '').split(/\s+/)[0];
        return ['Thanks' + (first ? ', ' + esc(first) : '') + '! What’s the best <strong>phone number</strong> to reach you at?'];
      },
      accept: function (v) {
        var digits = v.replace(/\D/g, '');
        if (digits.length < 10 || digits.length > 15) {
          return { error: 'Hmm, that doesn’t look like a complete phone number — mind double-checking? (e.g. 561-555-1234)' };
        }
        return { value: v, echo: v };
      },
      save: 'phone',
      next: function () { return 'email'; }
    },
    email: {
      prompt: function () { return ['And your <strong>email address</strong>, in case we can’t reach you by phone? <span class="fri-note">Optional — tap Skip if you’d rather not.</span>']; },
      chips: function () { return [{ label: 'Skip', value: '__skip__' }]; },
      accept: function (v) {
        if (v === '__skip__') return { value: '', echo: 'Skip' };
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return { error: 'That email doesn’t look quite right — want to try again, or tap Skip?' };
        return { value: v, echo: v };
      },
      save: 'email',
      next: function (d) { return d.intent === 'question' ? 'confirm' : 'time'; }
    },
    time: {
      prompt: function () { return ['When’s the best time for us to call? We’re open Mon–Fri, 8:00 AM – 5:30 PM.']; },
      chips: function () {
        return [{ label: '☀️ Morning', value: 'Morning' }, { label: '🌤️ Afternoon', value: 'Afternoon' }, { label: 'Anytime', value: 'Anytime' }];
      },
      accept: function (v) { return { value: v, echo: v }; },
      save: 'preferred_time',
      next: function () { return 'insurance'; }
    },
    insurance: {
      prompt: function () { return ['Last one — who’s your insurance provider? We’ll verify your coverage before we call. <span class="fri-note">Optional.</span>']; },
      chips: function () {
        return INSURERS.map(function (t) { return { label: t, value: t === 'Skip' ? '__skip__' : t }; });
      },
      accept: function (v) {
        if (v === '__skip__') return { value: '', echo: 'Skip' };
        return { value: v, echo: v };
      },
      save: 'insurance',
      next: function () { return 'confirm'; }
    },
    confirm: {
      prompt: function (d) { return [summaryHTML(d), 'Did I get everything right?']; },
      rawFirst: true,
      chips: function () {
        return [{ label: '✓ Send to the clinic', value: 'send', cls: 'primary' }, { label: '↺ Start over', value: 'restart' }];
      },
      accept: function (v) {
        var t = v.toLowerCase();
        if (t === 'send' || t.indexOf('yes') === 0 || t.indexOf('send') > -1 || t === 'y') return { value: 'send', echo: 'Send it ✓' };
        if (t === 'restart' || t.indexOf('start over') > -1 || t.indexOf('no') === 0) return { value: 'restart', echo: 'Start over' };
        return { error: 'Tap “Send to the clinic” when you’re ready — or “Start over” to fix something.' };
      },
      next: function () { return null; } // handled specially
    }
  };

  function summaryHTML(d) {
    var rows = [
      ['For', d.intent === 'question' ? 'A question' : 'Appointment request'],
      ['Care', d.topic], ['Details', d.message], ['Name', d.full_name],
      ['Phone', d.phone], ['Email', d.email], ['Call time', d.preferred_time], ['Insurance', d.insurance]
    ];
    var html = '<div class="fri-summary">';
    for (var i = 0; i < rows.length; i++) {
      if (rows[i][1]) html += '<div><span class="k">' + rows[i][0] + '</span><span class="v">' + esc(rows[i][1]) + '</span></div>';
    }
    return html + '</div>';
  }

  function scrollLog() { log.scrollTop = log.scrollHeight; }

  function addUser(text) {
    log.appendChild(el('div', 'fri-msg user', esc(text)));
    scrollLog();
  }

  function addBotNow(html, raw) {
    var m = el('div', raw ? '' : 'fri-msg bot');
    m.innerHTML = raw ? html : html; // raw blocks (summary card) carry their own styling
    if (raw) { var w = el('div'); w.innerHTML = html; m = w.firstChild; }
    log.appendChild(m);
    scrollLog();
    return m;
  }

  // Queue of bot messages with a typing indicator between them.
  function botSay(messages, rawFirst, done) {
    busy = true;
    clearChips();
    var i = 0;
    function nextMsg() {
      if (i >= messages.length) { busy = false; if (done) done(); return; }
      var typing = el('div', 'fri-msg bot fri-typing', '<i></i><i></i><i></i>');
      log.appendChild(typing);
      scrollLog();
      var delay = Math.min(350 + messages[i].length * 6, 1100);
      setTimeout(function () {
        typing.remove();
        addBotNow(messages[i], rawFirst && i === 0);
        i++;
        nextMsg();
      }, delay);
    }
    nextMsg();
  }

  function clearChips() {
    if (chipsEl) { chipsEl.remove(); chipsEl = null; }
  }

  function showChips(defs) {
    clearChips();
    if (!defs || !defs.length) return;
    chipsEl = el('div', 'fri-chips');
    defs.forEach(function (c) {
      var b = el('button', 'fri-chip' + (c.cls ? ' ' + c.cls : ''), esc(c.label));
      b.addEventListener('click', function () { handleAnswer(c.value, c.label.replace(/^[^\w]*\s*/, '')); });
      chipsEl.appendChild(b);
    });
    log.appendChild(chipsEl);
    scrollLog();
  }

  function saveDraft() {
    set(KEYS.draft, { state: flow.state, data: flow.data, t: Date.now() });
  }

  // ---------- Set-answer FAQ mode (no external AI required) ----------
  // Curated, always-available answers grounded in the clinic's real facts.
  // Anything a visitor types that isn't a menu tap is captured as a lead and
  // emailed to the front desk — so no real question is ever dropped.
  var FAQ = [
    { q: 'What services do you offer?',
      a: 'We offer physical therapy, occupational therapy, certified hand therapy, and an on-site wellness &amp; gym program — all under one roof. We’ve been family-owned since 1991, with a 5.0&#9733; reputation across the Palm Beaches.' },
    { q: 'Do you take my insurance?',
      a: 'We accept most major plans — Medicare, Medicare Advantage, Blue Cross Blue Shield, Aetna, Humana, Tricare, the VA Community Care Network, workers’ comp, and self-pay. Our front desk will gladly verify your exact coverage before your first visit — just call <a href="' + CFG.phoneHref + '">' + CFG.phone + '</a>.' },
    { q: 'Do I need a referral to start?',
      a: 'In Florida you can usually begin an evaluation without a doctor’s referral, thanks to direct access. Some insurance plans still require one for coverage, so it’s worth a quick call to <a href="' + CFG.phoneHref + '">' + CFG.phone + '</a> so we can check yours.' },
    { q: 'Where are you located?',
      a: 'We’re at 733 US Highway 1, Suite 2A, North Palm Beach, FL 33408 — serving North Palm Beach, Palm Beach Gardens, Jupiter, Juno Beach, and West Palm Beach.' },
    { q: 'What are your hours?',
      a: 'We’re open Monday through Friday, 8:00&nbsp;AM to 5:30&nbsp;PM, and closed on weekends.' },
    { q: 'What should I bring to my first visit?',
      a: 'Bring your photo ID, insurance card, and any referral or imaging paperwork from your doctor, and wear comfortable clothing you can move in. Your first visit is an evaluation — a conversation about your goals plus a movement assessment, often with hands-on treatment that same day.' },
    { q: 'How much does it cost / do you offer self-pay?',
      a: 'Your cost depends on your insurance plan and benefits, and yes — we offer self-pay options. For an exact estimate, call our front desk at <a href="' + CFG.phoneHref + '">' + CFG.phone + '</a>; they’ll verify your coverage and explain any out-of-pocket cost before you start.' },
    { q: 'What is certified hand therapy?',
      a: 'Certified hand therapy is specialized care for the hand, wrist, and arm, provided by Laura Drumm, CHT — a Certified Hand Therapist. We treat conditions like carpal tunnel, tendon injuries, fractures, and arthritis, and we fabricate custom splints right in our clinic.' },
    { q: 'What conditions do you treat?',
      a: 'We treat a wide range of orthopedic and post-surgical conditions — back and neck pain, sciatica, shoulder, knee and hip pain, hand and wrist injuries, headaches, balance problems, sports injuries, work injuries, and auto-accident recovery. Tell us what’s going on and we’ll point you the right way.' }
  ];

  function showFaqMenu() {
    var chips = FAQ.map(function (f, i) { return { label: f.q, value: 'faq:' + i }; });
    chips.push({ label: '📅 Request an appointment', value: 'restart-appointment', cls: 'primary' });
    chips.push({ label: '📨 Leave a message for the front desk', value: 'frontdesk' });
    showChips(chips);
  }

  function answerFaq(i) {
    if (busy) return;
    var f = FAQ[i];
    if (!f) return;
    addUser(f.q);
    botSay([f.a, 'Anything else I can help with?'], false, function () { showFaqMenu(); });
  }

  // Turn a typed question into a captured front-desk lead.
  function startFrontDeskMessage(questionText) {
    flow.data.intent = 'question';
    if (questionText) flow.data.message = String(questionText).slice(0, 4000);
    saveDraft();
    if (questionText) {
      botSay(['Great question — I’ll pass it straight to our front desk so they can follow up personally.'], false, function () { runStep('name'); });
    } else {
      runStep('message');
    }
  }

  function enterFaqMode() {
    flow.state = 'faq';
    saveDraft();
    var typed = flow.data.pendingTyped;
    flow.data.pendingTyped = null;
    if (typed) { startFrontDeskMessage(typed); return; }
    botSay(['Happy to help! Tap a question below and I’ll answer right away — or I can take a message for our front desk. 😊'], false, function () { showFaqMenu(); });
  }

  function runStep(stateId, opts) {
    if (stateId === 'faq') {
      enterFaqMode();
      return;
    }
    flow.state = stateId;
    saveDraft();
    var step = STEPS[stateId];
    var msgs = step.prompt(flow.data);
    botSay(msgs, step.rawFirst, function () {
      if (step.chips) showChips(step.chips(flow.data));
      if (!step.terminal && !(opts && opts.noFocus) && window.matchMedia('(min-width: 641px)').matches) input.focus();
    });
  }

  function handleAnswer(value, echoOverride) {
    if (busy) return;
    var step = STEPS[flow.state];
    if (!step) return;

    // FAQ menu tap → instant canned answer.
    if (typeof value === 'string' && value.indexOf('faq:') === 0) {
      answerFaq(parseInt(value.slice(4), 10));
      return;
    }

    // Restart shortcuts available from chips
    if (value === 'restart' && flow.state === 'confirm') {
      addUser('Start over');
      flow.data = {};
      del(KEYS.draft);
      runStep('intent');
      return;
    }
    if (value === 'restart-appointment') {
      addUser('Request an appointment');
      flow.data = { intent: 'appointment' };
      runStep('topic');
      return;
    }
    if (value === 'frontdesk') {
      addUser('Leave a message for the front desk');
      flow.data = { intent: 'question' };
      runStep('message');
      return;
    }
    if (value === 'ask-faq' || value === 'ask-ai') {
      addUser('I have a question');
      flow.data.intent = 'faq';
      runStep('faq');
      return;
    }
    // Anything typed while browsing the FAQ becomes a front-desk lead.
    if (flow.state === 'faq') {
      addUser(echoOverride || value);
      startFrontDeskMessage(value);
      return;
    }
    if (step.terminal) return;

    var res = step.accept ? step.accept(value) : { value: value, echo: value };
    if (res.error) {
      addUser(echoOverride || value);
      botSay([res.error], false, function () { if (step.chips) showChips(step.chips(flow.data)); });
      return;
    }
    addUser(res.echo != null ? res.echo : (echoOverride || value));
    if (step.save) flow.data[step.save] = res.value;
    saveDraft();

    if (flow.state === 'confirm' && res.value === 'send') { submit(); return; }

    var nxt = step.next(flow.data);
    if (nxt) runStep(nxt);
  }

  // ---------- delivery ----------
  function refCode() {
    var abc = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789', out = '';
    for (var i = 0; i < 5; i++) out += abc.charAt(Math.floor(Math.random() * abc.length));
    return 'FR-' + out;
  }

  function leadPayload() {
    var d = flow.data;
    return {
      ref_code: d.ref_code,
      intent: d.intent || 'appointment',
      topic: d.topic || null,
      message: (d.message || '').slice(0, 4000),
      full_name: (d.full_name || '').slice(0, 200),
      phone: (d.phone || '').slice(0, 40),
      email: (d.email || '').slice(0, 200) || null,
      preferred_time: d.preferred_time || null,
      insurance: d.insurance || null,
      page: location.pathname,
      user_agent: (navigator.userAgent || '').slice(0, 300)
    };
  }

  function sendToSupabase(payload) {
    return fetch(CFG.supabaseUrl + '/rest/v1/' + CFG.table, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': CFG.supabaseKey,
        'Authorization': 'Bearer ' + CFG.supabaseKey,
        'Prefer': 'return=minimal'
      },
      body: JSON.stringify(payload)
    }).then(function (r) {
      if (!r.ok) throw new Error('supabase ' + r.status);
      return true;
    });
  }

  // Email the lead to the clinic inbox (firstrehabnpb@gmail.com) via FormSubmit.
  // Returns a promise so delivery can be tracked independently of the database.
  function sendEmail(payload) {
    return fetch('https://formsubmit.co/ajax/' + CFG.notifyEmail, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({
        _subject: (payload.intent === 'question' ? 'Website question ' : 'Appointment request ') + (payload.ref_code || '') + ' — ' + payload.full_name,
        _template: 'table',
        Reference: payload.ref_code,
        Type: payload.intent === 'question' ? 'Question / message' : 'Appointment request',
        Care: payload.topic || '—',
        Details: payload.message || '—',
        Name: payload.full_name,
        Phone: payload.phone,
        Email: payload.email || '—',
        'Preferred call time': payload.preferred_time || '—',
        Insurance: payload.insurance || '—',
        Page: payload.page
      })
    }).then(function (r) {
      if (!r.ok) throw new Error('email ' + r.status);
      return r.json();
    });
  }

  // Deliver a lead two ways at once — Supabase (permanent record) and email
  // (clinic inbox). Resolves if EITHER channel succeeds, so a lead still reaches
  // the clinic if one path is down; rejects only if both fail (then it's queued).
  function deliverLead(payload) {
    return new Promise(function (resolve, reject) {
      var pending = 2, anyOk = false;
      function settle(ok) {
        if (ok) anyOk = true;
        pending -= 1;
        if (pending === 0) { anyOk ? resolve() : reject(new Error('delivery failed')); }
      }
      sendToSupabase(payload).then(function () { settle(true); }, function () { settle(false); });
      sendEmail(payload).then(function () { settle(true); }, function () { settle(false); });
    });
  }

  function queueLead(payload) {
    var q = get(KEYS.queue) || [];
    q.push(payload);
    set(KEYS.queue, q.slice(-20)); // keep the queue bounded
  }

  function flushQueue() {
    var q = get(KEYS.queue) || [];
    if (!q.length) return;
    var payload = q[0];
    deliverLead(payload).then(function () {
      var rest = (get(KEYS.queue) || []).slice(1);
      if (rest.length) { set(KEYS.queue, rest); flushQueue(); }
      else del(KEYS.queue);
    }).catch(function () { /* still offline — try again later */ });
  }

  function submit() {
    flow.data.ref_code = refCode();
    var payload = leadPayload();
    busy = true;
    clearChips();
    var typing = el('div', 'fri-msg bot fri-typing', '<i></i><i></i><i></i>');
    log.appendChild(typing);
    scrollLog();

    deliverLead(payload).then(function () {
      typing.remove();
      busy = false;
      del(KEYS.draft);
      set(KEYS.done, { t: Date.now(), ref: payload.ref_code });
      flow.state = 'sent';
      botSay([
        'Perfect — it’s on its way! 🎉 Your reference number is <strong>' + payload.ref_code + '</strong>.',
        'Our front desk will call you back within one business day. Need us sooner? We’re at <a href="' + CFG.phoneHref + '">' + CFG.phone + '</a>, Mon–Fri 8:00–5:30.'
      ], false, function () {
        showChips([{ label: '📅 Send another request', value: 'restart-appointment' }]);
      });
    }).catch(function () {
      typing.remove();
      busy = false;
      queueLead(payload);
      del(KEYS.draft);
      flow.state = 'queued';
      botSay([
        'It looks like the connection hiccuped — but don’t worry, <strong>your info is saved safely on this device</strong> and will send itself automatically as soon as the connection returns.',
        'If it’s urgent, our front desk is at <a href="' + CFG.phoneHref + '">' + CFG.phone + '</a>.'
      ]);
    });
  }

  // ---------- open / close ----------
  var started = false;
  function openPanel(auto) {
    hideTeaser();
    root.classList.add('open');
    if (!started) {
      started = true;
      var draft = get(KEYS.draft);
      if (draft && draft.data && draft.state && STEPS[draft.state] && Date.now() - (draft.t || 0) < 72 * 3600e3) {
        flow.data = draft.data;
        botSay(['Welcome back — let’s pick up right where we left off. 😊'], false, function () {
          runStep(draft.state, { noFocus: auto });
        });
      } else {
        runStep('intent', { noFocus: auto });
      }
    }
    if (!auto) input.focus();
  }
  function closePanel() {
    root.classList.remove('open');
  }
  function hideTeaser() {
    teaser.classList.remove('show');
  }

  // ---------- contact-page appointment form ----------
  function initApptForm() {
    var form = document.getElementById('appt-form');
    if (!form) return;
    var err = document.getElementById('af-error');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.name.value.trim();
      var phone = form.phone.value.trim();
      var email = form.email.value.trim();
      var reason = form.reason.value.trim();
      var time = form.time.value;
      var digits = phone.replace(/\D/g, '');
      var problems = [];
      if (name.replace(/[^a-zA-ZÀ-ɏ]/g, '').length < 2) problems.push('your name');
      if (digits.length < 10 || digits.length > 15) problems.push('a complete phone number');
      if (reason.length < 3) problems.push('a brief reason for your visit');
      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) problems.push('a valid email (or leave it blank)');
      if (problems.length) {
        err.textContent = 'Please provide ' + problems.join(', ') + '.';
        err.style.display = 'block';
        return;
      }
      err.style.display = 'none';
      var payload = {
        ref_code: refCode(),
        intent: 'appointment',
        topic: 'Contact form',
        message: reason.slice(0, 4000),
        full_name: name.slice(0, 200),
        phone: phone.slice(0, 40),
        email: email.slice(0, 200) || null,
        preferred_time: time,
        insurance: null,
        page: location.pathname,
        user_agent: (navigator.userAgent || '').slice(0, 300)
      };
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.textContent = 'Sending…';
      var finish = function (offline) {
        form.hidden = true;
        var doneBox = document.getElementById('af-done');
        var msg = document.getElementById('af-done-msg');
        if (offline) {
          msg.innerHTML = 'Your connection hiccuped — but your request is saved safely on this device and will send itself the next time you’re online here. If it’s urgent, call <a href="' + CFG.phoneHref + '">' + CFG.phone + '</a>.';
        } else {
          msg.innerHTML += '<br><br>Your reference number: <strong>' + payload.ref_code + '</strong>';
        }
        doneBox.hidden = false;
        doneBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
      };
      deliverLead(payload).then(function () {
        finish(false);
      }).catch(function () {
        queueLead(payload);
        finish(true);
      });
    });
  }

  // ---------- boot ----------
  function boot() {
    initApptForm();
    document.body.appendChild(root);
    teaser = root.querySelector('.fri-teaser');
    launcher = root.querySelector('.fri-launcher');
    panel = root.querySelector('.fri-panel');
    log = root.querySelector('.fri-log');
    input = root.querySelector('.fri-input');
    sendBtn = root.querySelector('.fri-send');

    launcher.addEventListener('click', function () { openPanel(false); });
    root.querySelector('.fri-x').addEventListener('click', closePanel);
    teaser.addEventListener('click', function (e) {
      if (e.target.classList.contains('fri-teaser-x')) { hideTeaser(); return; }
      openPanel(false);
    });
    teaser.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openPanel(false); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && root.classList.contains('open')) closePanel();
    });

    function sendInput() {
      var v = input.value.trim();
      if (!v || busy) return;
      input.value = '';
      handleAnswer(v);
    }
    sendBtn.addEventListener('click', sendInput);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); sendInput(); }
    });

    // Retry any leads that failed to send on a previous visit.
    flushQueue();
    window.addEventListener('online', flushQueue);

    // Auto-greet: once per browser session, never after a completed submission.
    var done = get(KEYS.done);
    var alreadyAuto = get(KEYS.auto, 's');
    if (!done && !alreadyAuto) {
      var isContact = /contact\.html$/.test(location.pathname);
      var delay = isContact ? CFG.contactPageDelay : CFG.autoOpenDelay;
      setTimeout(function () {
        if (root.classList.contains('open')) return;
        set(KEYS.auto, 1, 's');
        if (window.matchMedia('(max-width: 640px)').matches) {
          teaser.classList.add('show');
          setTimeout(hideTeaser, 14000);
        } else {
          openPanel(true);
        }
      }, delay);
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
