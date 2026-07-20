// Careers page: role preselect + application form.
// Delivery mirrors the proven intake-assistant pattern (see intake.js):
// the application goes two ways at once — INSERT into the dedicated Supabase
// job_applications table (publishable key, INSERT-only via RLS) and an email
// to the clinic inbox via FormSubmit. Either channel succeeding counts.
(function () {
  var CFG = {
    supabaseUrl: 'https://pclqpthqigsfteyluwqj.supabase.co',
    supabaseKey: 'sb_publishable_ERdB1Hn8B5cZ74Lq8otSKg_3bSwv5_K', // safe by design: INSERT-only
    table: 'job_applications',
    notifyEmail: 'firstrehabnpb@gmail.com'
  };

  var form = document.getElementById('careers-form');
  if (!form) return;
  var errEl = document.getElementById('cf-error');
  var doneEl = document.getElementById('cf-done');
  var select = document.getElementById('cf-position');

  // "Apply for this role" buttons preselect the position before jumping to the form.
  document.querySelectorAll('[data-role]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var role = btn.getAttribute('data-role');
      Array.prototype.forEach.call(select.options, function (o) {
        if (o.textContent === role) select.value = o.value || o.textContent;
      });
    });
  });

  function setError(msg) { errEl.textContent = msg || ''; }

  function sendToSupabase(app) {
    return fetch(CFG.supabaseUrl + '/rest/v1/' + CFG.table, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': CFG.supabaseKey,
        'Authorization': 'Bearer ' + CFG.supabaseKey,
        'Prefer': 'return=minimal'
      },
      body: JSON.stringify(app)
    }).then(function (r) { if (!r.ok) throw new Error('supabase ' + r.status); return true; });
  }

  function sendEmail(app) {
    return fetch('https://formsubmit.co/ajax/' + CFG.notifyEmail, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({
        _subject: 'New Job Application: ' + app.position + ' — ' + app.name,
        _template: 'table',
        _autoresponse: 'Thank you for applying to First Rehabilitation of North Palm Beach for the ' +
          app.position + ' role. Your application has been received and our team will review it. ' +
          'Questions? Call 561-624-4263 (Mon-Fri 8:00 AM-5:30 PM, Sat 8:00 AM-12:30 PM). ' +
          '- First Rehabilitation of North Palm Beach, 733 US Highway 1, Suite 2A, North Palm Beach, FL 33408',
        Type: 'Job application (careers page)',
        Position: app.position,
        Name: app.name,
        Email: app.email,
        Phone: app.phone || '—',
        'Resume link': app.resume_url || '—',
        Message: app.message || '—'
      })
    }).then(function (r) { if (!r.ok) throw new Error('email ' + r.status); return r.json(); });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    setError('');

    // Honeypot: humans never see this field; bots fill it. Pretend success.
    if (form.website.value) { form.hidden = true; doneEl.hidden = false; return; }

    var app = {
      name: form.name.value.trim(),
      email: form.email.value.trim(),
      phone: form.phone.value.trim(),
      position: select.value,
      message: form.message.value.trim(),
      resume_url: form.resume_url.value.trim()
    };

    if (!app.name) { setError('Please enter your full name.'); form.name.focus(); return; }
    if (!app.email || app.email.indexOf('@') < 1) { setError('Please enter a valid email address.'); form.email.focus(); return; }
    if (!app.position) { setError('Please choose a position.'); select.focus(); return; }
    if (app.resume_url && !/^https?:\/\//i.test(app.resume_url)) {
      setError('The resume link should start with http:// or https:// — paste the share link from Google Drive or Dropbox.');
      form.resume_url.focus(); return;
    }

    var btn = form.querySelector('button[type=submit]');
    btn.disabled = true;
    btn.textContent = 'Sending…';

    // Two channels at once; either succeeding counts (mirrors intake.js).
    new Promise(function (resolve, reject) {
      var pending = 2, anyOk = false;
      function settle(ok) {
        if (ok) anyOk = true;
        pending -= 1;
        if (pending === 0) { anyOk ? resolve() : reject(new Error('delivery failed')); }
      }
      sendToSupabase(app).then(function () { settle(true); }, function () { settle(false); });
      sendEmail(app).then(function () { settle(true); }, function () { settle(false); });
    }).then(function () {
      form.hidden = true;
      var sub = document.querySelector('#apply .af-sub');
      if (sub) sub.hidden = true;
      doneEl.hidden = false;
      doneEl.scrollIntoView({ block: 'center', behavior: 'smooth' });
    }).catch(function () {
      btn.disabled = false;
      btn.innerHTML = 'Send Application <span class="arr">&rarr;</span>';
      setError('Something went wrong sending your application. Please email it to firstrehabnpb@gmail.com or call 561-624-4263 — we would still love to hear from you.');
    });
  });
})();
