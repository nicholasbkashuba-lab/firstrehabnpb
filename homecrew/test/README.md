# Tests

Two suites, both runnable without a Supabase project.

## Durability and multi-user — `durability.js`

29 scenarios covering every way a technician's work could be lost:
photos surviving a reload, two houses open at once, offline submit into the
outbox, reconnect flush, per-device and per-technician isolation, two tabs on
one phone, Reset and sign-out guards, and render cost with 400 clients.

`fake-supabase.js` is injected before the portal's own script and stands in for
`@supabase/supabase-js`. It exists so the failure paths can be driven on demand:
`window.__fail` takes the whole server down, `window.__failInsert` takes only
the write path down while leaving auth working. That distinction matters — the
first version of this suite conflated them and produced two false failures.

```bash
npm i --no-save playwright-core
python3 -m http.server 8912          # from the repo root
NODE_PATH=../node_modules node test/durability.js
```

## Row Level Security

The RLS scenarios run as SQL against the live project rather than the browser,
because they are about what Postgres will allow, not what the UI does. See the
block in `docs/TESTING.md`. Create throwaway crew and clients, assert, then
delete them — never leave fixtures in a project that also holds real addresses.
