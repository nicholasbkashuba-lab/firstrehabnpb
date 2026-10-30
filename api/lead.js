/**
 * Website lead endpoint: emails every form submission to the clinic.
 *
 * Replaces FormSubmit, which went down on 2026-10-28 (Cloudflare 521) and took
 * every email notification on this site with it. Same file in each Design of
 * Man client site, with one difference here: First Rehab's browser code already
 * saves every submission to its own Supabase project ("First Rehabilitation
 * App": intake_leads, job_applications, ask_dave_questions, dad_jokes), so this
 * endpoint does NOT store anything. It only emails.
 *
 *   1. Email the office through Resend (LEAD_TO, cc LEAD_CC, from LEAD_FROM).
 *   2. If CONFIRM_FROM is set, and the source is an appointment-type form
 *      (CONFIRM_SOURCES), send the visitor a short confirmation. It never
 *      repeats what they typed beyond their first name: no reason, no message.
 *      Careers, dad-joke and Ask Dave submissions never get one.
 *
 * Success means emailed. The browser counts Supabase OR this email as delivered
 * (intake.js deliverLead), so a failure here only matters when Supabase failed
 * too. JSON callers get {"success":"true"|"false"}, the shape FormSubmit used.
 * A plain HTML form post is redirected to its `_next` (same site only).
 *
 * Zero dependencies, CommonJS: this site deploys with no install step.
 *
 * Environment:
 *   RESEND_API_KEY  enables email. Without it every call reports failure.
 *   LEAD_TO         comma-separated office recipients
 *   LEAD_CC         comma-separated copies (hello@designofman.com)
 *   LEAD_FROM       verified Resend sender, "Name <addr@domain>"
 *   CONFIRM_FROM    optional sender for the patient confirmation
 */

"use strict";

const SITE = "firstrehabnpb.com";
const PHONE = "561-624-4263";
const PRACTICE = "First Rehabilitation of North Palm Beach";
const { officeEmail, confirmEmail } = require("./_email.js");
const BRAND = { name: PRACTICE, color: "#0E3A47", accent: "#F4A261", accentInk: "#0E3A47", kicker: "#F4A261" };

const TIMEOUT_MS = 8000;

// Sources that send no phone or email of their own (podcast page forms): they
// are a heads-up to the clinic, not a lead, so a name and contact are optional.
const ANON_SOURCES = ["dad-joke", "ask-dave"];
// Only these get the visitor confirmation email.
const CONFIRM_SOURCES = ["intake"];

const OK = { success: "true" };
const NOT_OK = { success: "false" };

function clean(v, max) {
  if (typeof v === "number") v = String(v);
  return typeof v === "string" ? v.replace(/[\r\n]+/g, " ").trim().slice(0, max) : "";
}
// Read a field by name regardless of case ("Name" or "name"): the browser code
// labels email fields for humans. A lone dash is the "not given" placeholder.
function field(body, key, max) {
  for (const k of Object.keys(body)) {
    if (k.toLowerCase() === key) {
      const v = clean(body[k], max);
      if (v && !/^[-–—]+$/.test(v)) return v;
    }
  }
  return "";
}
function list(v) {
  return String(v || "").split(",").map((a) => a.trim()).filter(Boolean);
}
function emailOk(e) {
  return /^[^\s@<>]+@[^\s@<>]+\.[a-z]{2,}$/i.test(e);
}

function finish(req, res, body, ok) {
  const wantsJson = /json/i.test(String(req.headers["content-type"] || "")) ||
    /json/i.test(String(req.headers.accept || ""));
  if (!wantsJson) {
    let next = "/";
    try {
      const u = new URL(String(body._next || "/"), "https://" + SITE);
      if (u.hostname.replace(/^www\./, "") === SITE) next = u.pathname + u.search;
    } catch (e) { /* keep "/" */ }
    if (ok) {
      res.statusCode = 303;
      res.setHeader("Location", next);
      return res.end();
    }
    res.statusCode = 502;
    res.setHeader("Content-Type", "text/html; charset=utf-8");
    return res.end(`<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Please call us</title><body style="font-family:system-ui,sans-serif;max-width:32rem;margin:3rem auto;padding:0 1rem;line-height:1.5"><h1>We could not send your request</h1><p>Please call <a href="tel:${PHONE.replace(/\D/g, "")}">${PHONE}</a> and we will book you directly.</p><p><a href="javascript:history.back()">Go back</a></p></body>`);
  }
  res.statusCode = ok ? 200 : 502;
  res.setHeader("Content-Type", "application/json");
  return res.end(JSON.stringify(ok ? OK : NOT_OK));
}

async function resend(payload) {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(TIMEOUT_MS),
  });
  if (!r.ok) throw new Error(`resend ${r.status} ${await r.text()}`);
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    res.statusCode = 405;
    return res.end();
  }
  const body = req.body && typeof req.body === "object" ? req.body : {};

  // Honeypot: a bot gets a cheerful success and nothing is sent.
  if (clean(body._honey, 100)) return finish(req, res, body, true);

  const source = clean(body.source, 60) || "website";
  const anon = ANON_SOURCES.includes(source);
  const name = field(body, "name", 200) ||
    [field(body, "first_name", 100), field(body, "last_name", 100)].filter(Boolean).join(" ");
  const phone = field(body, "phone", 50);
  const email = field(body, "email", 200);

  // Every visible field goes in the email, in the order it arrived. Fields
  // starting with "_" are FormSubmit-style controls, not visitor answers.
  const fields = [];
  for (const [k, v] of Object.entries(body)) {
    if (k.startsWith("_") || ["source"].includes(k)) continue;
    const val = clean(Array.isArray(v) ? v.join(", ") : v, 4000);
    if (val) fields.push([k.replace(/_/g, " "), val]);
  }

  if (anon) {
    if (!fields.length) return finish(req, res, body, false);
  } else if (!name || (!phone && !emailOk(email))) {
    return finish(req, res, body, false);
  }

  let emailed = false;
  const to = list(process.env.LEAD_TO);
  if (process.env.RESEND_API_KEY && to.length && process.env.LEAD_FROM) {
    const subject = (clean(body._subject, 150) || `New website request (${SITE})`) +
      (!name || subjectHasName(body._subject, name) ? "" : ` — ${name}`);
    const payload = {
      from: process.env.LEAD_FROM,
      to,
      subject,
      html: officeEmail({
        brand: BRAND,
        title: titleFor(body, source),
        fields: Object.entries(body).filter(([k]) => !k.startsWith("_") && k !== "source"),
        meta: { site: SITE, source: source === "intake" ? "website chat or contact form" : source.replace(/-/g, " ") },
      }),
      text: fields.map(([k, v]) => `${k}: ${v}`).join("\n") +
        `\n\n-- Sent from ${SITE} (${source}). The website also saves this to Supabase (First Rehabilitation App).`,
    };
    const cc = list(process.env.LEAD_CC);
    if (cc.length) payload.cc = cc;
    if (emailOk(email)) payload.reply_to = email;
    try {
      await resend(payload);
      emailed = true;
    } catch (err) {
      console.error("lead: email failed", err && err.message);
    }
  } else {
    console.warn("lead: email not configured (RESEND_API_KEY / LEAD_TO / LEAD_FROM)");
  }

  if (emailed && CONFIRM_SOURCES.includes(source) && process.env.CONFIRM_FROM && emailOk(email)) {
    const first = !name || /https?:|www\.|[<>]/i.test(name) ? "there" : name.split(/\s+/)[0];
    try {
      await resend({
        from: process.env.CONFIRM_FROM,
        to: [email],
        reply_to: to[0],
        subject: `We received your request: ${PRACTICE}`,
        html: confirmEmail({
          brand: BRAND, first, phone: PHONE, site: SITE,
          ref: refOf(body),
          promise: "Your request came through and our team will contact you within one business day.",
        }),
        text: [
          `Hi ${first},`,
          "",
          `Thank you for reaching out to ${PRACTICE}. Your request came through and our team will contact you within one business day.`,
          "",
          `If it's urgent, call us at ${PHONE}.`,
          "",
          PRACTICE,
          `https://www.${SITE}`,
        ].join("\n"),
      });
    } catch (err) {
      console.error("lead: confirmation failed", err && err.message);
    }
  }

  return finish(req, res, body, emailed);
};

function subjectHasName(subject, name) {
  return typeof subject === "string" && name && subject.includes(name);
}

// The heading on the clinic's email: what kind of request this is.
function titleFor(body, source) {
  if (source === "careers") return "New job application";
  if (source === "dad-joke") return "New dad joke for Pain 2 Power";
  if (source === "ask-dave") return "New Ask Dave question";
  if (source === "recovered") return "Recovered appointment request";
  const type = String(body.Type || body.type || body.intent || "").toLowerCase();
  if (type.indexOf("question") > -1) return "New website question";
  return "New appointment request";
}

// The chat's reference number ("Reference" from intake.js), when well formed.
function refOf(body) {
  const r = field(body, "reference", 20) || field(body, "ref", 20) || "";
  return /^[A-Z]{2}-[A-Z0-9]{5}$/.test(r) ? r : "";
}
