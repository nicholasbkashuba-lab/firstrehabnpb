/* A stand-in for @supabase/supabase-js, injected before the portal's own
   script runs. It exists so the LIVE code paths — sign-in, the crew check,
   inserts, storage uploads, the outbox, draft sync — can be driven
   deterministically, including the failure modes a real server will not
   produce on demand.

   window.__fail        server unreachable, everything
   window.__failInsert  server unreachable for WRITES only (auth still works)

   The two are separate because conflating them hid a real bug once: signing
   in flushed the outbox before the assertion could see anything queued, and
   the suite reported a failure that was the double's fault, not the app's.

   SERVER STATE lives in window.__drafts and window.__blobs. A Playwright
   context is a device; two contexts share no memory, which is exactly right.
   To model "the tablet sees what the phone uploaded", the test lifts these
   two objects out of one context and injects them into the other. Blobs are
   held as base64 so that transfer is a plain JSON copy. */
window.__fail = false;
window.__failInsert = false;
window.__inserted = [];
window.__uploaded = [];
window.__removed = [];
window.__drafts = {};   /* id -> row, the inspection_drafts table */
window.__blobs = {};    /* storage path -> base64, the bucket */

(function () {
  var USERS = {
    'tech1@test.invalid': { id: 'u-tech1', name: 'T. One', role: 'technician' },
    'tech2@test.invalid': { id: 'u-tech2', name: 'T. Two', role: 'technician' },
    'owner@test.invalid': { id: 'u-owner', name: 'O. Owner', role: 'owner' },
  };
  var CLIENTS = [
    { id: 'c1', full_name: 'Test Client Alpha', email: 'alpha@test.invalid', phone: '(772) 555-0001',
      mailing_addr: '', notes: '', properties: [
        { id: 'p1', address: '1 Test Way, Vero Beach FL 32960', county: 'Indian River', route_order: 10,
          package: 'gold', visit_frequency: 'weekly', gate_code: '1111', key_box_code: '2222',
          assigned_to: 'u-tech1', active: true, property_type: 'Single family' }] },
    { id: 'c2', full_name: 'Test Client Bravo', email: 'bravo@test.invalid', phone: '(772) 555-0002',
      mailing_addr: '', notes: '', properties: [
        { id: 'p2', address: '2 Test Way, Stuart FL 34994', county: 'Martin', route_order: 10,
          package: 'silver', visit_frequency: 'weekly', gate_code: '3333', key_box_code: '4444',
          assigned_to: 'u-tech1', active: true, property_type: 'Single family' },
        { id: 'p3', address: '3 Test Way, Stuart FL 34996', county: 'Martin', route_order: 20,
          package: 'bronze', visit_frequency: 'biweekly', gate_code: '5555', key_box_code: '6666',
          assigned_to: 'u-tech2', active: true, property_type: 'Condo' }] },
    { id: 'c3', full_name: 'Test Client Charlie', email: 'charlie@test.invalid', phone: '(561) 555-0003',
      mailing_addr: '', notes: '', properties: [
        { id: 'p4', address: '4 Test Way, Jupiter FL 33477', county: 'Palm Beach', route_order: 10,
          package: 'gold', visit_frequency: 'monthly', gate_code: '7777', key_box_code: '8888',
          assigned_to: 'u-tech2', active: true, property_type: 'Estate' }] },
  ];
  var LAST_VISIT = [
    { property_id: 'p1', last_inspected_on: '2026-07-01' },   // long overdue
    { property_id: 'p2', last_inspected_on: '2026-07-25' },   // overdue
    { property_id: 'p3', last_inspected_on: null },           // never visited
    { property_id: 'p4', last_inspected_on: '2026-08-04' },   // fresh
  ];

  var seq = 0;
  var clock = 0;          /* monotonic stamp so "newer" is decidable in a test */
  function stamp() { clock += 1000; return new Date(1785000000000 + clock).toISOString(); }
  function net() { if (window.__fail) throw new Error('Failed to fetch'); }
  function down() { return window.__fail || window.__failInsert; }
  function me() { return window.__me || USERS['tech1@test.invalid']; }
  var ERR = { message: 'Failed to fetch' };

  function b64(blob) {
    return new Promise(function (res) {
      var fr = new FileReader();
      fr.onload = function () { res(String(fr.result).split(',')[1] || ''); };
      fr.onerror = function () { res(''); };
      fr.readAsDataURL(blob);
    });
  }
  function unb64(s) {
    var bin = atob(s || ''), arr = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
    return new Blob([arr], { type: 'image/jpeg' });
  }

  function result(data) {
    var o = {
      data: data, error: null,
      select: function () { return o; },
      eq: function () { return o; },
      order: function () { return o; },
      limit: function () { return o; },
      single: function () { return Promise.resolve({ data: Array.isArray(data) ? data[0] : data, error: null }); },
      maybeSingle: function () { return Promise.resolve({ data: Array.isArray(data) ? data[0] : data, error: null }); },
      then: function (res) { return Promise.resolve({ data: data, error: null }).then(res); },
    };
    return o;
  }
  function failing() {
    var o = {
      data: null, error: ERR,
      select: function () { return o; }, eq: function () { return o; },
      order: function () { return o; }, limit: function () { return o; },
      single: function () { return Promise.resolve({ data: null, error: ERR }); },
      maybeSingle: function () { return Promise.resolve({ data: null, error: ERR }); },
      then: function (r) { return Promise.resolve({ data: null, error: ERR }).then(r); },
    };
    return o;
  }

  /* ---------------------------------------------------------------
     inspection_drafts — a real little table, because the sync logic
     is only worth testing against something that actually filters,
     stamps updated_at, and enforces "your rows only".
  ---------------------------------------------------------------- */
  function draftsTable() {
    function mine() {
      var uid = me().id;
      return Object.keys(window.__drafts)
        .map(function (k) { return window.__drafts[k]; })
        .filter(function (r) { return r.crew_id === uid; });
    }
    return {
      select: function () {
        if (down()) return failing();
        var rows = mine(), o;
        o = {
          eq: function (col, val) {
            rows = rows.filter(function (r) { return r[col] === val; });
            return o;
          },
          order: function () {
            rows = rows.slice().sort(function (a, b) {
              return String(b.updated_at).localeCompare(String(a.updated_at));
            });
            return o;
          },
          limit: function () { return o; },
          single: function () {
            return Promise.resolve(rows.length
              ? { data: JSON.parse(JSON.stringify(rows[0])), error: null }
              : { data: null, error: { message: 'no rows' } });
          },
          maybeSingle: function () {
            return Promise.resolve({ data: rows.length ? JSON.parse(JSON.stringify(rows[0])) : null, error: null });
          },
          then: function (r) {
            return Promise.resolve({ data: JSON.parse(JSON.stringify(rows)), error: null }).then(r);
          },
        };
        return o;
      },
      upsert: function (row) {
        return {
          select: function () {
            return {
              single: function () {
                if (down()) return Promise.resolve({ data: null, error: ERR });
                var saved = JSON.parse(JSON.stringify(row));
                saved.crew_id = row.crew_id || me().id;
                saved.updated_at = stamp();          /* the trigger, in miniature */
                window.__drafts[saved.id] = saved;
                return Promise.resolve({ data: { updated_at: saved.updated_at }, error: null });
              },
            };
          },
        };
      },
      delete: function () {
        return {
          eq: function (col, val) {
            if (down()) return Promise.resolve({ error: ERR });
            Object.keys(window.__drafts).forEach(function (k) {
              var r = window.__drafts[k];
              if (r[col] === val && r.crew_id === me().id) delete window.__drafts[k];
            });
            return Promise.resolve({ error: null });
          },
        };
      },
      insert: function () { return { select: function () { return { single: function () {
        return Promise.resolve({ data: null, error: ERR }); } }; } }; },
      update: function () { return { eq: function () { return Promise.resolve({ error: null }); } }; },
    };
  }

  window.supabase = {
    createClient: function () {
      return {
        auth: {
          signInWithPassword: function (c) {
            net();
            var u = USERS[String(c.email).toLowerCase()];
            if (!u || !String(c.password).length) return Promise.resolve({ data: null, error: { message: 'bad creds' } });
            window.__me = u;
            return Promise.resolve({ data: { user: { id: u.id, email: c.email } }, error: null });
          },
          getSession: function () { return Promise.resolve({ data: { session: null }, error: null }); },
          signOut: function () { return Promise.resolve({ error: null }); },
        },
        from: function (table) {
          if (table === 'inspection_drafts') return draftsTable();
          return {
            select: function () {
              try { net(); } catch (e) { return failing(); }
              if (table === 'crew') {
                var u = me();
                return result({ full_name: u.name, role: u.role, active: true });
              }
              if (table === 'clients') return result(JSON.parse(JSON.stringify(CLIENTS)));
              if (table === 'property_last_visit') return result(LAST_VISIT);
              if (table === 'inspections') return result([]);
              return result([]);
            },
            insert: function (payload) {
              return {
                select: function () {
                  return {
                    single: function () {
                      if (down()) return Promise.resolve({ data: null, error: ERR });
                      seq++;
                      var row = { id: 'insp-' + seq, inspection_no: 'HC-2026-' + String(seq).padStart(4, '0') };
                      window.__inserted.push({ row: row, payload: payload });
                      return Promise.resolve({ data: row, error: null });
                    },
                  };
                },
              };
            },
            update: function () { return { eq: function () {
              return Promise.resolve({ error: down() ? ERR : null }); } }; },
            delete: function () { return { eq: function () {
              return Promise.resolve({ error: down() ? ERR : null }); } }; },
          };
        },
        storage: {
          from: function () {
            return {
              upload: async function (path, blob) {
                if (down()) return { error: ERR };
                window.__blobs[path] = await b64(blob);
                window.__uploaded.push({ path: path, size: blob && blob.size });
                return { data: { path: path }, error: null };
              },
              /* A blob: URL is a legitimate signed URL as far as fetch() is
                 concerned, and it keeps the round trip real: the portal asks
                 for a URL, fetches it, and gets bytes back. */
              createSignedUrl: function (path) {
                if (down()) return Promise.resolve({ data: null, error: ERR });
                if (!window.__blobs[path]) return Promise.resolve({ data: null, error: { message: 'not found' } });
                return Promise.resolve({
                  data: { signedUrl: URL.createObjectURL(unb64(window.__blobs[path])) }, error: null });
              },
              remove: function (paths) {
                if (down()) return Promise.resolve({ error: ERR });
                (paths || []).forEach(function (p) { window.__removed.push(p); delete window.__blobs[p]; });
                return Promise.resolve({ data: [], error: null });
              },
            };
          },
        },
        functions: { invoke: function () { return Promise.resolve({ data: null, error: { message: 'not deployed' } }); } },
      };
    },
  };
})();
