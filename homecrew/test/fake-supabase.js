/* A stand-in for @supabase/supabase-js, injected before the portal's own
   script runs. It exists so the LIVE code paths — sign-in, the crew check,
   inserts, storage uploads, the outbox — can be driven deterministically,
   including the failure modes a real server will not produce on demand.
   window.__fail flips the server between working and unreachable. */
window.__fail = false;
window.__failInsert = false;   // server unreachable for writes only
window.__inserted = [];
window.__uploaded = [];

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
  function net() { if (window.__fail) throw new Error('Failed to fetch'); }

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
          return {
            select: function () {
              try { net(); } catch (e) { return { eq: function(){return this;}, order: function(){return this;},
                limit: function(){return this;},
                single: function(){return Promise.resolve({data:null,error:{message:'Failed to fetch'}});},
                maybeSingle: function(){return Promise.resolve({data:null,error:{message:'Failed to fetch'}});},
                then: function(r){return Promise.resolve({data:null,error:{message:'Failed to fetch'}}).then(r);} }; }
              if (table === 'crew') {
                var me = window.__me || USERS['tech1@test.invalid'];
                return result({ full_name: me.name, role: me.role, active: true });
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
                      if (window.__fail || window.__failInsert) {
                        return Promise.resolve({ data: null, error: { message: 'Failed to fetch' } });
                      }
                      seq++;
                      var row = { id: 'insp-' + seq, inspection_no: 'HC-2026-' + String(seq).padStart(4, '0') };
                      window.__inserted.push({ row: row, payload: payload });
                      return Promise.resolve({ data: row, error: null });
                    },
                  };
                },
              };
            },
            update: function () { return { eq: function () { try { net(); } catch (e) {
              return Promise.resolve({ error: { message: 'Failed to fetch' } }); }
              return Promise.resolve({ error: null }); } }; },
          };
        },
        storage: {
          from: function () {
            return {
              upload: function (path, blob) {
                if (window.__fail || window.__failInsert) {
                  return Promise.resolve({ error: { message: 'Failed to fetch' } });
                }
                window.__uploaded.push({ path: path, size: blob && blob.size });
                return Promise.resolve({ data: { path: path }, error: null });
              },
            };
          },
        },
        functions: { invoke: function () { return Promise.resolve({ data: null, error: { message: 'not deployed' } }); } },
      };
    },
  };
})();
