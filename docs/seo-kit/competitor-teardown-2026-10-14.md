# Competitor teardown, 2026-10-14

Raw HTML of each page below was pulled on 2026-10-14 and parsed for title, meta description,
H1, JSON-LD types and visible word count. The raw HTML is third-party content and is not
committed. Conclusions and actions are in `docs/LOCAL-AUTHORITY-AUDIT-2026-10.md`; this file is
the evidence behind section 1 of it.

## Per page

| Site / page | Title tag | H1 | JSON-LD types (deduplicated) | Words |
|---|---|---|---|---|
| Synergy Health & Wellness, home (Jupiter) | Jupiter Physical Therapy \| Synergy Health & Wellness | Physical Therapy in Jupiter, Florida | Organization+Place, PostalAddress, GeoCoordinates, OpeningHoursSpecification, WebPage, WebSite, BreadcrumbList | ~730 |
| Synergy, OT page | Jupiter Occupational Therapy \| Synergy Health & Wellness | Occupational Therapy in Jupiter, Florida | Same as home | ~970 |
| CORA Physical Therapy, Palm Beach Gardens | CORA Palm Beach Gardens - CORA Physical Therapy | CORA Palm Beach Gardens | Organization, WebPage, WebSite, BreadcrumbList (Yoast default) | ~820 |
| Gold Coast PT, Palm Beach Gardens | Physical Therapy Palm Beach Gardens FL \| Gold Coast Physical Therapy | Gold Coast Physical Therapy PALM BEACH GARDENS | MedicalClinic, PostalAddress, OpeningHoursSpecification, City, Service, OfferCatalog, MedicalWebPage, BreadcrumbList | ~1,050 |
| Gold Coast PT, hand therapy page | Hand & Upper Extremity Therapy - Gold Coast Physical Therapy | Hand & Upper Extremity Therapy | Service, OfferCatalog, PeopleAudience, MedicalWebPage, Organization | ~770 |
| Comprehensive Hand & PT, home (Jupiter) | Comprehensive Hand & Physical Therapy | none | Organization, WebPage, WebSite, BreadcrumbList | ~1,770 |
| Select Physical Therapy, North Palm Beach | Select Physical Therapy \| North Palm Beach | North Palm Beach | MedicalClinic, MedicalOrganization, MedicalSpecialty, PostalAddress, GeoCoordinates | ~990 |
| Palm Beach Orthopaedic Institute (PBOI), therapy page | Physical Therapy West Palm Beach, Jupiter \| Occupational Therapy… | Physical & Occupational Therapy | Hospital, AggregateRating, PostalAddress, ContactPoint, ReserveAction | ~1,870 |
| TheraHealth, Medicare page | Physical Therapist Medicare in Palm Beach County: In-Home or At Our Cl… | none | Organization, WebPage, WebSite, BreadcrumbList | ~1,400 |
| Mobile Therapy Group, home | HOME | Mobile Therapy Group | none | ~1,330 |
| FIRST Rehab (thefirstrehab.com), home | The First Rehab | none | none; no meta description either | ~720 |

Their Palm Beach Gardens location page (checked separately on the same day) carries lorem
ipsum placeholder text.

## What we ship, for comparison

MedicalClinic + MedicalBusiness org node with address, geo, hours (Saturday included),
10 areaServed cities, medicalSpecialty, availableService and sameAs; Person ×5 with verified
credentials (hasCredential); MedicalTherapy per service; MedicalCondition per condition;
BlogPosting + WebPage reviewedBy; FAQPage; PodcastSeries + episodes; VideoObject;
DefinedTermSet (glossary); BreadcrumbList; JobPosting; Service per location page. No review
markup, deliberately.

## Reading it

1. **Schema is not the gap.** Nobody nearby has richer markup than we do, and the two with a
   MedicalClinic node (Gold Coast, Select) are not the ones beating us hardest. Do not spend
   more time on schema to win rankings; keep it accurate and matched to the visible page.
2. **Their titles front-load the city they are physically in** ("Jupiter Physical Therapy",
   "Physical Therapy Palm Beach Gardens FL"). That works for them because they have an office
   there. We cannot copy it honestly for towns we serve from North Palm Beach, and the GSC data
   already shows city pages earn almost no clicks for us (CLAUDE.md, location-page thesis).
3. **Word count is not the gap either.** Most competitor pages run 700 to 1,100 words. Our
   service pages, the Medicare guide (insurance page ~1,850) and the glossary are deeper.
4. **What they have that we lack is off-page:** review volume shown on the page (Synergy 734,
   CORA 236, Better Life 154, Comprehensive Hand 126 against our 110), a big-name affiliation
   (HSS network, Select Medical, an orthopaedic group), and clean directory citations. Those
   are the levers in the audit.
5. **Don't copy PBOI's AggregateRating.** Self-serving review markup on your own site breaks
   Google's review snippet rules. CLAUDE.md already forbids it.

## Rankings observed the same day (organic, not the map pack)

- "physical therapy north palm beach fl": First Rehab #1.
- "certified hand therapist palm beach gardens": First Rehab #1; Mobile Therapy Group (Laura's
  second employer) #3; ASHT Find a Therapist #6.
- "physical therapist that accepts medicare palm beach gardens": Zocdoc #1.
- "physical therapy north palm beach": Healthgrades on page one.

Re-check with `tools/gsc.py queries` for our own positions; a live SERP is not visible from the
sandbox, so these are point-in-time observations from search tools.
