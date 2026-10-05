/* Staff lead inbox.
   Reads public.intake_leads and writes outcomes through public.set_lead_status().
   This page carries no secret: the publishable key is the same one intake.js ships.
   Access is enforced in the database: rows are readable only by signed-in users whose
   email is in public.lead_staff, and the only write path is the set_lead_status RPC.
   Every lead field is visitor-supplied, so it is rendered with textContent, never HTML. */
(function () {
  'use strict';

  var API = 'https://pclqpthqigsfteyluwqj.supabase.co';
  var KEY = 'sb_publishable_ERdB1Hn8B5cZ74Lq8otSKg_3bSwv5_K';
  var SESSION_KEY = 'fr-staff-session';
  var STATUSES = [
    ['new', 'Needs a call'],
    ['contacted', 'Contacted'],
    ['booked', 'Booked'],
    ['no_show', 'No-show'],
    ['not_a_fit', 'Not a fit']
  ];
  var LABEL = {};
  STATUSES.forEach(function (s) { LABEL[s[0]] = s[1]; });
  var TABS = [['new', 'Needs a call'], ['contacted', 'Contacted'], ['booked', 'Booked'], ['closed', 'No-show / not a fit'], ['all', 'All']];

  var state = { session: null, leads: [], tab: 'new' };
  var root = document.getElementById('staff-app');

  function el(tag, attrs, text) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'class') n.className = attrs[k];
      else n.setAttribute(k, attrs[k]);
    });
    if (text != null) n.textContent = text;
    return n;
  }

  function loadSession() {
    try { return JSON.parse(sessionStorage.getItem(SESSION_KEY) || 'null'); } catch (e) { return null; }
  }
  function saveSession(s) {
    try {
      if (s) sessionStorage.setItem(SESSION_KEY, JSON.stringify(s));
      else sessionStorage.removeItem(SESSION_KEY);
    } catch (e) { /* storage blocked: session lives in memory only */ }
  }
  function toSession(r) {
    return {
      access_token: r.access_token,
      refresh_token: r.refresh_token,
      expires_at: Date.now() + (r.expires_in || 3600) * 1000,
      email: (r.user && r.user.email) || ''
    };
  }

  function authRequest(grant, body) {
    return fetch(API + '/auth/v1/token?grant_type=' + grant, {
      method: 'POST',
      headers: { 'apikey': KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }).then(function (r) {
      return r.json().then(function (j) {
        if (!r.ok) throw new Error(j.error_description || j.msg || 'Sign-in failed');
        return toSession(j);
      });
    });
  }

  function freshToken() {
    var s = state.session;
    if (!s) return Promise.reject(new Error('signed out'));
    if (s.expires_at - Date.now() > 60000) return Promise.resolve(s.access_token);
    return authRequest('refresh_token', { refresh_token: s.refresh_token }).then(function (n) {
      n.email = n.email || s.email;
      state.session = n; saveSession(n);
      return n.access_token;
    });
  }

  function api(path, opts) {
    opts = opts || {};
    return freshToken().then(function (tok) {
      return fetch(API + path, {
        method: opts.method || 'GET',
        headers: {
          'apikey': KEY,
          'Authorization': 'Bearer ' + tok,
          'Content-Type': 'application/json'
        },
        body: opts.body ? JSON.stringify(opts.body) : undefined
      });
    }).then(function (r) {
      if (r.status === 401) { signOut('Your session expired. Please sign in again.'); throw new Error('expired'); }
      return r.json().then(function (j) {
        if (!r.ok) throw new Error((j && (j.message || j.hint)) || ('Request failed (' + r.status + ')'));
        return j;
      });
    });
  }

  function ago(iso) {
    var mins = Math.round((Date.now() - new Date(iso).getTime()) / 60000);
    if (mins < 60) return mins <= 1 ? 'just now' : mins + ' min ago';
    var hrs = Math.round(mins / 60);
    if (hrs < 24) return hrs + ' hr ago';
    var days = Math.round(hrs / 24);
    return days === 1 ? 'yesterday' : days + ' days ago';
  }
  function when(iso) {
    return new Date(iso).toLocaleString('en-US', { timeZone: 'America/New_York', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
  }

  /* ---------- sign in ---------- */
  function renderLogin(msg) {
    root.textContent = '';
    var card = el('div', { class: 'staff-card staff-login' });
    card.appendChild(el('h1', null, 'Lead inbox'));
    card.appendChild(el('p', null, 'Front desk only. Sign in with your First Rehab app account.'));
    var form = el('form', { novalidate: '' });
    var l1 = el('label', { class: 'staff-field' }); l1.appendChild(el('span', null, 'Email'));
    var email = el('input', { type: 'email', autocomplete: 'username', required: '' }); l1.appendChild(email);
    var l2 = el('label', { class: 'staff-field' }); l2.appendChild(el('span', null, 'Password'));
    var pw = el('input', { type: 'password', autocomplete: 'current-password', required: '' }); l2.appendChild(pw);
    var btn = el('button', { class: 'staff-btn', type: 'submit' }, 'Sign in');
    var err = el('p', { class: 'staff-error', role: 'alert' }, msg || '');
    form.appendChild(l1); form.appendChild(l2); form.appendChild(btn); form.appendChild(err);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!email.value || !pw.value) { err.textContent = 'Enter your email and password.'; return; }
      btn.disabled = true; err.textContent = '';
      authRequest('password', { email: email.value.trim(), password: pw.value }).then(function (s) {
        state.session = s; saveSession(s); pw.value = '';
        loadLeads();
      }).catch(function (x) {
        btn.disabled = false; err.textContent = x.message || 'Sign-in failed';
      });
    });
    card.appendChild(form);
    root.appendChild(card);
    email.focus();
  }

  function signOut(msg) {
    var s = state.session;
    state.session = null; state.leads = []; saveSession(null);
    if (s) fetch(API + '/auth/v1/logout', { method: 'POST', headers: { 'apikey': KEY, 'Authorization': 'Bearer ' + s.access_token } }).catch(function () {});
    renderLogin(msg);
  }

  /* ---------- inbox ---------- */
  function loadLeads() {
    root.textContent = '';
    root.appendChild(el('p', { class: 'staff-empty' }, 'Loading leads…'));
    var cols = 'id,created_at,ref_code,intent,topic,message,full_name,phone,email,preferred_time,insurance,page,status,status_note,status_updated_at,status_by';
    api('/rest/v1/intake_leads?select=' + cols + '&status=neq.test&order=created_at.desc&limit=500')
      .then(function (rows) { state.leads = rows; renderInbox(); })
      .catch(function (x) { if (x.message !== 'expired') renderLogin('Could not load leads: ' + x.message); });
  }

  function inTab(lead, tab) {
    if (tab === 'all') return true;
    if (tab === 'closed') return lead.status === 'no_show' || lead.status === 'not_a_fit';
    return lead.status === tab;
  }

  function renderInbox() {
    root.textContent = '';
    var head = el('div', { class: 'staff-head' });
    head.appendChild(el('h1', null, 'Lead inbox'));
    var who = el('div', { class: 'staff-who' }, 'Signed in as ' + (state.session.email || 'staff'));
    var out = el('button', { class: 'staff-btn staff-btn-quiet', type: 'button' }, 'Sign out');
    out.addEventListener('click', function () { signOut(); });
    who.appendChild(out);
    head.appendChild(who);
    root.appendChild(head);

    if (!state.leads.length) {
      root.appendChild(el('p', { class: 'staff-empty' },
        'No leads are visible to this account. If you work the front desk, ask Nick to add your email to the lead list.'));
      return;
    }

    var c = { new: 0, contacted: 0, booked: 0, closed: 0 };
    var last30 = Date.now() - 30 * 86400000, worked30 = 0, booked30 = 0;
    state.leads.forEach(function (l) {
      if (l.status === 'no_show' || l.status === 'not_a_fit') c.closed++; else if (c[l.status] != null) c[l.status]++;
      if (new Date(l.created_at).getTime() >= last30) {
        if (l.status !== 'new') worked30++;
        if (l.status === 'booked') booked30++;
      }
    });
    var stats = el('div', { class: 'staff-stats' });
    [[c.new, 'Need a call'], [c.contacted, 'Contacted'], [c.booked, 'Booked'],
     [worked30 ? Math.round(100 * booked30 / worked30) + '%' : '–', 'Booked, last 30 days']].forEach(function (s) {
      var b = el('div', { class: 'staff-stat' });
      b.appendChild(el('b', null, String(s[0]))); b.appendChild(el('span', null, s[1]));
      stats.appendChild(b);
    });
    root.appendChild(stats);

    var tabs = el('div', { class: 'staff-tabs', role: 'group', 'aria-label': 'Filter leads' });
    TABS.forEach(function (t) {
      var b = el('button', { class: 'staff-tab', type: 'button', 'aria-pressed': String(state.tab === t[0]) }, t[1]);
      b.addEventListener('click', function () { state.tab = t[0]; renderInbox(); });
      tabs.appendChild(b);
    });
    root.appendChild(tabs);

    var shown = state.leads.filter(function (l) { return inTab(l, state.tab); });
    if (!shown.length) { root.appendChild(el('p', { class: 'staff-empty' }, 'Nothing here.')); return; }
    var list = el('ul', { class: 'staff-list' });
    shown.forEach(function (l) { list.appendChild(renderLead(l)); });
    root.appendChild(list);
  }

  function renderLead(l) {
    var li = el('li', { class: 'staff-lead' });
    var top = el('div', { class: 'staff-lead-top' });
    top.appendChild(el('h2', null, l.full_name || '(no name)'));
    top.appendChild(el('span', { class: 'staff-age', title: when(l.created_at) }, ago(l.created_at) + ' · ' + when(l.created_at)));
    li.appendChild(top);

    var contact = el('div', { class: 'staff-contact' });
    var digits = String(l.phone || '').replace(/[^\d+]/g, '');
    if (digits) contact.appendChild(el('a', { href: 'tel:' + digits }, l.phone));
    if (l.email) contact.appendChild(el('a', { href: 'mailto:' + String(l.email).replace(/[\s<>"]/g, '') }, l.email));
    li.appendChild(contact);

    var meta = [];
    if (l.preferred_time) meta.push('Best time: ' + l.preferred_time);
    if (l.insurance) meta.push('Insurance: ' + l.insurance);
    if (l.intent === 'question') meta.push('Question, not a booking');
    if (l.page) meta.push('From ' + l.page);
    if (l.ref_code) meta.push('Ref ' + l.ref_code);
    if (meta.length) li.appendChild(el('p', { class: 'staff-meta' }, meta.join(' · ')));
    if (l.message) li.appendChild(el('p', { class: 'staff-msg' }, l.message));

    var chips = el('div', { class: 'staff-chips', role: 'group', 'aria-label': 'Outcome for ' + (l.full_name || 'this lead') });
    var noteRow = el('div', { class: 'staff-note-row' });
    var note = el('input', { class: 'staff-note', type: 'text', maxlength: '500', placeholder: 'Note (optional): left voicemail, booked Tue 10am…', 'aria-label': 'Note' });
    note.value = l.status_note || '';
    var saveNote = el('button', { class: 'staff-btn staff-btn-quiet', type: 'button' }, 'Save note');
    var stamp = el('p', { class: 'staff-stamp', 'aria-live': 'polite' });
    function setStamp() {
      stamp.textContent = l.status_updated_at
        ? 'Updated ' + when(l.status_updated_at) + (l.status_by ? ' by ' + l.status_by : '')
        : '';
    }
    setStamp();

    function apply(status, btn) {
      var all = li.querySelectorAll('button');
      Array.prototype.forEach.call(all, function (b) { b.disabled = true; });
      stamp.textContent = 'Saving…';
      api('/rest/v1/rpc/set_lead_status', { method: 'POST', body: { lead_id: l.id, new_status: status, note: note.value } })
        .then(function (r) {
          l.status = r.status; l.status_note = r.status_note;
          l.status_updated_at = r.status_updated_at; l.status_by = r.status_by;
          if (btn === saveNote || inTab(l, state.tab)) {
            Array.prototype.forEach.call(chips.children, function (b) { b.setAttribute('aria-pressed', String(b.dataset.s === l.status)); });
            Array.prototype.forEach.call(all, function (b) { b.disabled = false; });
            setStamp();
          } else {
            renderInbox();
          }
        })
        .catch(function (x) {
          Array.prototype.forEach.call(all, function (b) { b.disabled = false; });
          if (x.message !== 'expired') stamp.textContent = 'Not saved: ' + x.message;
        });
    }

    STATUSES.forEach(function (s) {
      var b = el('button', { class: 'staff-chip', type: 'button', 'aria-pressed': String(l.status === s[0]) }, s[1]);
      b.dataset.s = s[0];
      b.addEventListener('click', function () { if (l.status !== s[0]) apply(s[0], b); });
      chips.appendChild(b);
    });
    saveNote.addEventListener('click', function () { apply(l.status, saveNote); });

    li.appendChild(chips);
    noteRow.appendChild(note); noteRow.appendChild(saveNote);
    li.appendChild(noteRow);
    li.appendChild(stamp);
    return li;
  }

  state.session = loadSession();
  if (state.session) loadLeads(); else renderLogin();
})();
