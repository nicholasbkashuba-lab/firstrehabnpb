// Podcast page community features: "Ask Dave" questions + dad-joke submissions
// and the approved-jokes feed. Delivery + key reuse mirrors careers.js/intake.js:
// the Supabase publishable key is INSERT-only via RLS (jokes are also forced
// approved=false by policy, and only approved=true rows are readable). Nothing
// a visitor submits can appear publicly until the owner flips `approved` in the
// Supabase Table Editor.
(function () {
  var CFG = {
    supabaseUrl: 'https://pclqpthqigsfteyluwqj.supabase.co',
    supabaseKey: 'sb_publishable_ERdB1Hn8B5cZ74Lq8otSKg_3bSwv5_K' // safe by design
  };

  function insertRow(table, row) {
    return fetch(CFG.supabaseUrl + '/rest/v1/' + table, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': CFG.supabaseKey,
        'Authorization': 'Bearer ' + CFG.supabaseKey,
        'Prefer': 'return=minimal'
      },
      body: JSON.stringify(row)
    }).then(function (r) { if (!r.ok) throw new Error(table + ' ' + r.status); return true; });
  }

  // Simple client-side rate gate: one submission per form per minute.
  function gated(key) {
    var last = +(localStorage.getItem(key) || 0);
    return (Date.now() - last) < 60000;
  }
  function stamp(key) { try { localStorage.setItem(key, String(Date.now())); } catch (e) {} }

  function wireForm(formId, opts) {
    var form = document.getElementById(formId);
    if (!form) return;
    var errEl = form.querySelector('.af-error');
    var doneEl = document.getElementById(formId + '-done');
    function setError(msg) {
      errEl.textContent = msg || '';
      errEl.style.display = msg ? 'block' : 'none';
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      setError('');
      // Honeypot: humans never see this field; bots fill it. Pretend success.
      if (form.website && form.website.value) { form.hidden = true; doneEl.hidden = false; return; }
      if (gated('fr-gate-' + formId)) {
        setError('Easy there — please wait a minute before sending another.');
        return;
      }
      var row, err = opts.validate(form);
      if (err) { setError(err); return; }
      row = opts.row(form);
      var btn = form.querySelector('button[type=submit]');
      btn.disabled = true;
      var original = btn.innerHTML;
      btn.textContent = 'Sending…';
      insertRow(opts.table, row).then(function () {
        stamp('fr-gate-' + formId);
        form.hidden = true;
        doneEl.hidden = false;
      }).catch(function () {
        btn.disabled = false;
        btn.innerHTML = original;
        setError('Something went wrong sending that. Please try again, or call 561-624-4263.');
      });
    });
  }

  wireForm('ask-dave-form', {
    table: 'ask_dave_questions',
    validate: function (f) {
      if (f.question.value.trim().length < 5) return 'Please write your question first.';
      if (f.email.value && f.email.value.indexOf('@') < 1) return 'That email doesn’t look right — it’s optional, so you can also leave it blank.';
      return '';
    },
    row: function (f) {
      return {
        name: f.name.value.trim() || null,
        email: f.email.value.trim() || null,
        question: f.question.value.trim()
      };
    }
  });

  wireForm('dad-joke-form', {
    table: 'dad_jokes',
    validate: function (f) {
      if (f.joke.value.trim().length < 5) return 'Please write your joke first — the cornier the better.';
      return '';
    },
    row: function (f) {
      return {
        first_name: f.first_name.value.trim() || null,
        joke: f.joke.value.trim()
      };
    }
  });

  // Approved-jokes feed: fetch only approved rows, newest first, cap 20.
  // The whole section stays hidden unless at least one approved joke exists —
  // no empty states, ever.
  var feed = document.getElementById('joke-feed');
  if (feed) {
    fetch(CFG.supabaseUrl + '/rest/v1/dad_jokes?select=first_name,joke&approved=eq.true&order=created_at.desc&limit=20', {
      headers: { 'apikey': CFG.supabaseKey, 'Authorization': 'Bearer ' + CFG.supabaseKey }
    }).then(function (r) { return r.ok ? r.json() : []; }).then(function (rows) {
      if (!rows || !rows.length) return; // section stays hidden
      var list = feed.querySelector('.joke-list');
      rows.forEach(function (j) {
        var card = document.createElement('figure');
        card.className = 'joke-card';
        var p = document.createElement('p');
        p.textContent = j.joke; // textContent: user data is never injected as HTML
        card.appendChild(p);
        if (j.first_name) {
          var by = document.createElement('figcaption');
          by.className = 'joke-by';
          by.textContent = '— ' + j.first_name;
          card.appendChild(by);
        }
        list.appendChild(card);
      });
      feed.hidden = false;
    }).catch(function () { /* feed simply stays hidden */ });
  }
})();
