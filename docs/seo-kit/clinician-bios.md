> **STATUS (2026-10-14): reference only.** Credentials below were corrected to the verified set. The live implementation is TEAM and person_schema() in build.py, which already emits Person schema with hasCredential. Use the intake sheet in this file to collect each clinician's long-form bio, specialties and fun fact, then fill TEAM[n]["bio"] etc.

# Clinician Bio Pages: Template, Intake Sheet, and Schema

Purpose: every clinician gets a dedicated page (/team/first-last/) with real credentials, because authority and entity recognition depend on verifiable people. **Do not invent or guess any credential, license, school, or year.** Fill every placeholder from the clinician themselves before publishing.

## People to build

| Page | Name | Role (confirm) | Notes |
|---|---|---|---|
| 1 | Laura Drumm | Certified Hand Therapist | Leads hand therapy |
| 2 | David Kashuba, Ph.D., OTR | Founder, CEO and Occupational Therapist | Verified 2026-10-14 (NPI 1679603468, OTR). He is an occupational therapist, never "DPT" or "PT" |
| 3 | Kayla Dorsey, PT, DPT | Physical Therapist | Verified 2026-10-14 (NPI 1689128993) |
| 4 | Logan Van Sant, PT, DPT | Physical Therapist | Licensed PT verified (NPI 1962367136); DPT per Nick |
| 5 | Joan "Joni" Janik, OTD | Occupational Therapist | Licensed OT verified (NPI 1578393849); OTD per Nick; legal name Joan, goes by Joni |

## Intake sheet (send to each clinician)

1. Full name as it should appear, and preferred first name
2. Job title
3. Degrees and schools (with years)
4. Florida license type and number (stored internally; publish only if the clinician agrees)
5. Certifications (for example CHT, CSCS), with issuing body
6. Years in practice and years at First Rehab
7. Clinical focus (3 to 5 areas the clinician is truly strong in)
8. Professional memberships (for example APTA, AOTA, ASHT)
9. Talks, podcast episodes (Pain 2 Power), publications
10. A short personal paragraph (hobbies, why they got into therapy)
11. A professional headshot (clear, recent, consistent style)
12. Public profile links (LinkedIn, directory pages) they are comfortable linking

## Page template (about 350 to 450 words each)

**H1:** [Name], [credentials], [Title] at First Rehabilitation of North Palm Beach

**Intro (2 sentences):** who they are and who they help most.

**H2: What [First name] focuses on** (3 to 5 bullets from the intake sheet)

**H2: Background and credentials** (degrees, certifications, memberships)

**H2: Outside the clinic** (the personal paragraph; plain, warm tone)

**H2: Questions patients ask [First name]** (3 visible Q&As, such as "What can I expect in my first visit with you?")

**CTA:** book or call; link to the relevant service page and glossary.

*Medically reviewed / bio verified by the clinician on [TODO: date].*

## Schema (one block per bio page, placeholders must be replaced)

Replace `https://REPLACE-WITH-YOUR-DOMAIN.com` with the real domain. Only keep properties whose data is real and visible or verifiable.

```json
{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "mainEntity": {
    "@type": "Person",
    "@id": "https://REPLACE-WITH-YOUR-DOMAIN.com/team/laura-drumm/#person",
    "name": "Laura Drumm",
    "jobTitle": "Certified Hand Therapist",
    "worksFor": { "@id": "https://REPLACE-WITH-YOUR-DOMAIN.com/#clinic" },
    "url": "https://REPLACE-WITH-YOUR-DOMAIN.com/team/laura-drumm/",
    "image": "https://REPLACE-WITH-YOUR-DOMAIN.com/wp-content/uploads/team/laura-drumm.jpg",
    "description": "TODO: one-sentence bio that matches the visible page",
    "knowsAbout": ["Hand therapy", "Upper extremity rehabilitation"],
    "hasCredential": [
      {
        "@type": "EducationalOccupationalCredential",
        "credentialCategory": "certification",
        "name": "Certified Hand Therapist (CHT)",
        "recognizedBy": { "@type": "Organization", "name": "Hand Therapy Certification Commission" }
      }
    ],
    "sameAs": [
      "TODO: LinkedIn URL (only if the clinician approves)"
    ]
  }
}
```

Repeat the same shape for the other four people, changing `@id`, `name`, `jobTitle`, `url`, `image`, `knowsAbout`, and credentials. Credential entries to use (degrees are stated by Nick; licenses and certifications still need confirmation):

```json
{ "@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "Doctor of Physical Therapy (DPT)" }
{ "@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "Doctor of Occupational Therapy (OTD)" }
{ "@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "Doctor of Philosophy (Ph.D.)" }
```

- Kayla Dorsey and Logan Van Sant: `jobTitle` "Physical Therapist", credential DPT.
- Joni Janik: `jobTitle` "Occupational Therapist", credential OTD.
- Laura Drumm: CHT credential as shown above; her underlying PT or OT degree and license are not yet confirmed.
- David Kashuba: credentials Ph.D. and OTR; the `"founder"` linkage from the clinic node already exists in build.py.
- Do not add a license-based claim until the clinician confirms it.

## Rules

- Consistency matters: the name, title, and photo must match everywhere (site, Google Business Profile, directories, podcast pages).
- Do not state outcomes, rankings, or "best" claims.
- Never publish a license number, on the page or in schema (CLAUDE.md).
- Keep the visible page and the schema identical in substance.
