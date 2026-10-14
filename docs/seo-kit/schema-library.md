> **STATUS (2026-10-14): reference.** The site already ships almost all of this from build.py (MedicalClinic org node, Person, MedicalTherapy, MedicalCondition, BlogPosting + WebPage reviewedBy, Breadcrumb, FAQPage, PodcastSeries/Episode, VideoObject, JobPosting, Service, DefinedTermSet). Use this file for rules (visible-match, one @id per entity, no self-serving review markup) and for any NEW page type, e.g. an Event page for the November patient event.

# Schema Library: First Rehabilitation of North Palm Beach

Everything here is JSON-LD for `<script type="application/ld+json">`. Replace `DOMAIN` with the real domain (for example `https://example.com`) and every `TODO` before publishing. `scripts/check_schema_visible_match.py` fails the build if any placeholder or mismatch remains.

## 0. Rules that apply to every block

1. **Visible-match rule.** Every question, answer, term, name, date, and fact in schema must appear on the page a visitor sees. No hidden text, no sitewide generic blocks. (Google spam policy: structured data must reflect visible content.)
2. **One entity, one `@id`.** The clinic is `DOMAIN/#clinic`, the site is `DOMAIN/#website`, each person is `DOMAIN/team/first-last/#person`. Other blocks reference these ids instead of redefining them. If an SEO plugin also outputs a clinic/organization node, disable the plugin's version (duplicate nodes confuse entity recognition).
3. **No schema that Google will not use, and no risky schema.**
   - Do **not** mark up the clinic's own reviews with `Review` or `AggregateRating`. Self-serving review markup is ineligible for rich results and invites a manual action.
   - Do **not** use `HowTo` (rich results were removed) or add `speakable`.
   - `FAQPage` is optional. FAQ rich results ended 7 May 2026; keep the markup only where the same Q&As are visible and specific to the page.
   - Never put license numbers, patient stories, outcomes, or ratings in schema.
4. **Google says no special schema is needed for AI Overviews or AI Mode.** Schema helps machines understand pages. Do not expect it to move rankings by itself.
5. **Dates** use ISO 8601 with timezone (`2026-10-14T09:00:00-04:00`). **URLs** are absolute and canonical. **Images** are real files on the site.
6. **Validate** in Google's Rich Results Test and validator.schema.org, and run the local checker.

## 1. Sitewide graph (already built)

`build_schema.py` outputs `MedicalClinic` + `Physiotherapy` (`#clinic`), `WebSite` (`#website`), and `PodcastSeries`. Keep it as the only place the clinic is defined. Fill hours, phone, logo, image, and `sameAs` with real values.

## 2. Blog post (`BlogPosting` + `MedicalWebPage` + breadcrumb)

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["WebPage", "MedicalWebPage"],
      "@id": "DOMAIN/blog/SLUG/#webpage",
      "url": "DOMAIN/blog/SLUG/",
      "name": "TODO: page title (matches the visible H1)",
      "isPartOf": { "@id": "DOMAIN/#website" },
      "about": { "@id": "DOMAIN/#clinic" },
      "breadcrumb": { "@id": "DOMAIN/blog/SLUG/#breadcrumb" },
      "primaryImageOfPage": { "@type": "ImageObject", "url": "DOMAIN/wp-content/uploads/TODO.jpg" },
      "lastReviewed": "TODO: 2026-10-14",
      "reviewedBy": { "@id": "DOMAIN/team/TODO-reviewer/#person" },
      "mainContentOfPage": { "@type": "WebPageElement", "cssSelector": "article" }
    },
    {
      "@type": "BlogPosting",
      "@id": "DOMAIN/blog/SLUG/#article",
      "mainEntityOfPage": { "@id": "DOMAIN/blog/SLUG/#webpage" },
      "headline": "TODO: same as visible H1",
      "description": "TODO: same as meta description",
      "image": ["DOMAIN/wp-content/uploads/TODO.jpg"],
      "datePublished": "TODO: ISO date",
      "dateModified": "TODO: ISO date",
      "author": { "@id": "DOMAIN/team/TODO-author/#person" },
      "reviewedBy": { "@id": "DOMAIN/team/TODO-reviewer/#person" },
      "publisher": { "@id": "DOMAIN/#clinic" },
      "inLanguage": "en-US",
      "articleSection": "TODO: category",
      "citation": [
        { "@type": "CreativeWork", "name": "TODO: primary source title", "url": "TODO: source URL" }
      ]
    },
    {
      "@type": "BreadcrumbList",
      "@id": "DOMAIN/blog/SLUG/#breadcrumb",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "DOMAIN/" },
        { "@type": "ListItem", "position": 2, "name": "Blog", "item": "DOMAIN/blog/" },
        { "@type": "ListItem", "position": 3, "name": "TODO: post title" }
      ]
    }
  ]
}
```

Optional: add `"about": { "@type": "MedicalCondition", "name": "TODO: e.g. Rotator cuff tear" }` to the `BlogPosting` when the post is about one condition. The `citation` entries must match the visible "Sources" list.

## 3. Service page (`MedicalWebPage` + `Service`)

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["WebPage", "MedicalWebPage"],
      "@id": "DOMAIN/services/SLUG/#webpage",
      "url": "DOMAIN/services/SLUG/",
      "name": "TODO: visible H1",
      "isPartOf": { "@id": "DOMAIN/#website" },
      "mainEntity": { "@id": "DOMAIN/services/SLUG/#service" },
      "breadcrumb": { "@id": "DOMAIN/services/SLUG/#breadcrumb" },
      "lastReviewed": "TODO: ISO date",
      "reviewedBy": { "@id": "DOMAIN/team/TODO-reviewer/#person" }
    },
    {
      "@type": "Service",
      "@id": "DOMAIN/services/SLUG/#service",
      "name": "TODO: e.g. Certified Hand Therapy",
      "serviceType": "TODO: e.g. Hand therapy",
      "description": "TODO: two sentences, same as visible intro",
      "provider": { "@id": "DOMAIN/#clinic" },
      "areaServed": [
        { "@type": "City", "name": "North Palm Beach" },
        { "@type": "City", "name": "Jupiter" },
        { "@type": "City", "name": "Palm Beach Gardens" }
      ],
      "audience": { "@type": "PeopleAudience", "suggestedMinAge": 18 }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "DOMAIN/services/SLUG/#breadcrumb",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "DOMAIN/" },
        { "@type": "ListItem", "position": 2, "name": "Services", "item": "DOMAIN/services/" },
        { "@type": "ListItem", "position": 3, "name": "TODO: service name" }
      ]
    }
  ]
}
```

Create one page and one block per service (physical therapy, occupational therapy, hand therapy, balance and fall prevention, post-surgical rehab, auto accident and personal-injury therapy, wellness). Only list areas the service page actually names.

## 4. Location / service-area page (Jupiter)

Use a `WebPage` that points at the existing clinic. **Do not** create a second `LocalBusiness` or an address in Jupiter.

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "DOMAIN/locations/jupiter-fl/#webpage",
  "url": "DOMAIN/locations/jupiter-fl/",
  "name": "Physical & Occupational Therapy for Jupiter, FL Residents",
  "isPartOf": { "@id": "DOMAIN/#website" },
  "about": { "@id": "DOMAIN/#clinic" },
  "spatialCoverage": { "@type": "City", "name": "Jupiter", "containedInPlace": { "@type": "AdministrativeArea", "name": "Florida" } },
  "breadcrumb": {
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Home", "item": "DOMAIN/" },
      { "@type": "ListItem", "position": 2, "name": "Locations", "item": "DOMAIN/locations/" },
      { "@type": "ListItem", "position": 3, "name": "Jupiter, FL" }
    ]
  }
}
```

## 5. Glossary (`DefinedTermSet`)

One `DefinedTerm` per visible entry. The generator should read the glossary markdown so schema and page can never drift.

```json
{
  "@context": "https://schema.org",
  "@type": "DefinedTermSet",
  "@id": "DOMAIN/resources/therapy-glossary/#termset",
  "name": "Physical & Occupational Therapy Glossary",
  "url": "DOMAIN/resources/therapy-glossary/",
  "hasDefinedTerm": [
    {
      "@type": "DefinedTerm",
      "name": "Plan of care",
      "description": "A written roadmap of your goals, treatments, how often you'll come, and how long therapy is expected to last.",
      "inDefinedTermSet": { "@id": "DOMAIN/resources/therapy-glossary/#termset" }
    }
  ]
}
```

## 6. Patient education event (`Event`)

Publish only after the date, time, and place are confirmed. Remove the block when the event ends or set status accordingly.

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "TODO: event title (matches page H1)",
  "description": "TODO: same as visible description",
  "startDate": "TODO: 2026-11-TT:TT:00-05:00",
  "endDate": "TODO: ISO date-time",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "name": "TODO: venue",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "TODO",
      "addressLocality": "North Palm Beach",
      "addressRegion": "FL",
      "postalCode": "TODO",
      "addressCountry": "US"
    }
  },
  "organizer": { "@id": "DOMAIN/#clinic" },
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "DOMAIN/events/TODO/"
  }
}
```

## 7. Podcast episode page and video

Each Pain 2 Power episode page needs the visible title, description, and a transcript or detailed summary, plus the embedded player.

```json
{
  "@context": "https://schema.org",
  "@type": "PodcastEpisode",
  "@id": "DOMAIN/podcast/SLUG/#episode",
  "url": "DOMAIN/podcast/SLUG/",
  "name": "TODO: episode title",
  "description": "TODO: visible description",
  "datePublished": "TODO: ISO date",
  "episodeNumber": 0,
  "partOfSeries": { "@id": "DOMAIN/podcast/#series" },
  "associatedMedia": {
    "@type": "AudioObject",
    "contentUrl": "TODO: audio file URL",
    "duration": "PT0M"
  }
}
```

For YouTube or clip pages use `VideoObject` with `name`, `description`, `thumbnailUrl`, `uploadDate`, `duration`, and `embedUrl`, all matching the visible page. Guest consent and release are required before publishing guest names.

## 8. FAQ page (optional)

Generated from `first_rehab_qa_training.py` by `build_schema.py`. It validates but produces no rich result since 7 May 2026. Publish only if every Q&A is visible on the `/faq/` page word for word.

## 9. Page-type map

| Page | Blocks |
|---|---|
| Home | Sitewide graph |
| Service pages | Section 3, plus breadcrumb |
| Location pages | Section 4 |
| Clinician bios | `ProfilePage` + `Person` (see `clinician-bios.md`) |
| Blog posts | Section 2 |
| Glossary | Section 5 |
| FAQ page | Section 8 (optional) |
| Event page | Section 6 (once confirmed) |
| Podcast episode / video pages | Section 7 |
| Contact | Sitewide graph (no extra clinic node) |

## 10. What not to build

- "Hidden" blogs, hidden FAQ text, or schema describing content not on the page.
- Reviews or ratings markup for First Rehab.
- A second business node for each city.
- Medical claims in schema (for example, "treats" or "cures" statements).
- Markup copied from a competitor without checking it against the visible page.
