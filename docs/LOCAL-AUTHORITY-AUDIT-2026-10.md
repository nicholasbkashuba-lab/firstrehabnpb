# Why nearby clinics outrank us, and what to do about it (2026-10-14)

Evidence gathered 2026-10-14: Google Places results for four core queries, organic results for
four more, a raw-HTML teardown of nine competitor sites (JSON-LD, titles, H1s, word counts), the
NPPES NPI Registry, Healthgrades, Yelp, LinkedIn and every review on our Google Business Profile.
Raw competitor HTML from the teardown is not committed (it is third-party content).

## 1. The short answer: it is not their schema

None of the clinics that beat us in the map pack has better structured data than we do. Most
have a plugin's generic Organization and WebPage nodes and nothing else: no address, no hours,
no clinician markup. Only Gold Coast and Select carry a MedicalClinic node. Nobody has FAQPage,
Person, MedicalTherapy or BlogPosting markup. We already ship all of those. Schema is a tie we
already win, so more of it will not move rankings.

Organically we are already strong: #1 for "physical therapy north palm beach fl" and #1 for
"certified hand therapist palm beach gardens" in the results pulled today, ahead of Select,
PBOI, HSS and the chains.

Where we lose is the **map pack outside North Palm Beach** and the **directory layer**. Those run on:

| Driver | What the winners have | Us |
|---|---|---|
| **Proximity** | An office inside the searched city. Synergy and Comprehensive Hand are in Jupiter, CORA and Gold Coast in Palm Beach Gardens | One office in North Palm Beach. We cannot change this, so we win on the other drivers |
| **Review volume and recency** | Synergy 734, CORA 236, Better Life 154, Comprehensive Hand 126 | 110, but only 8 in the last 12 months and none since Aug 14 |
| **Visible proof on the page** | Synergy prints "5.0 from 734 reviews"; Gold Coast quotes Google reviews on location pages; CORA runs a review widget | Service pages showed no reviews. **Fixed today.** |
| **Institutional trust** | Synergy is in the HSS Rehabilitation Network; Select is Select Medical; PBOI is an ortho group | CORF certification, the WPTV feature and surgeon podcast guests were barely shown. **Fixed today** (CORF in the Medicare guide, WPTV on the homepage) |
| **Clean citations** | Consistent NAP across NPI, Healthgrades, Yelp | Several wrong records (section 3) |
| **Directory presence** | Zocdoc, Yelp, Healthgrades and ASHT pages rank on page one for our terms | Thin or wrong listings |

The pattern behind the "hidden scheme" is plain: a physical office in the town, hundreds of
recent reviews shown on the page, and a big-name affiliation. Two of those three we can match.

## 2. A name collision is costing us reviews

**FIRST Rehab** (thefirstrehab.com) is a separate clinic with offices in West Palm Beach, Lake
Worth/Atlantis and **3375 Burns Rd, Palm Beach Gardens** (Google: "FIRST Rehab of Palm Beach
Gardens", 4.9 from 92). Its site has no schema, no meta descriptions and a lorem-ipsum PBG page.

At least two reviews on **our** listing were written for them: one names "FIRST REHAB on Burns
Rd" and their staff (Rob, Lonn, Ashley); another says "or at any of their locations". Searches
on our profile include "first rehab pbg". Google and patients are mixing the two brands.

What to do:
- Always use the full name **First Rehabilitation of North Palm Beach** on listings, posts and
  signage, and never "First Rehab" on its own.
- Ask Google (in the review management screen) to move or remove reviews clearly about the
  other clinic. They are 5 stars, so this is optional; accuracy is the point.
- **Owner decision:** whether the site should say it is not affiliated with other clinics
  using a similar name. It is not added yet, because the history between the two businesses
  is unknown here.

## 3. Wrong records that feed Google, insurers and AI answers

Each of these is verified today. NPPES is the source that Healthgrades, Medical News Today,
Doximity and insurer directories copy, so fixing it fixes many listings downstream.

| Record | What's wrong | Fix (owner) |
|---|---|---|
| **NPI 1730224049**, organization (DBA First Rehabilitation Inc) | Phones 561-624-1457 and 561-840-4204, not 561-624-4263. Last updated 2013 | Log in to nppes.cms.hhs.gov as the authorized official and update phone, fax and practice location |
| **NPI 1679603468**, David Kashuba | Practice address 8895 N Military Trail, Palm Beach Gardens (old office) | Update to 733 US Highway 1, Suite 2A |
| **NPI 1861459695**, Laura Drumm | Practice address 50 S Old Dixie Hwy, Jupiter, with Comprehensive Hand & PT's phone (561-575-4770) | Laura updates her own record (free, 10 minutes) |
| **Healthgrades** group page | Lists only "David Kashuba, PT" (he is an OT), phone **(561) 412-1046**, no other clinicians | Claim the free provider/practice profiles; fix the phone; add all five clinicians. Ask whether 412-1046 is an old tracking number |
| **LinkedIn** company page | Describes "David Kashuba, **M.D.**" | Change to "David Kashuba, Ph.D., OTR" now. Calling a non-physician "M.D." is a licensing risk, not just an SEO one |
| **Yelp** (24 reviews, 4.7) | Address "Bldg 2, Ste A" | Change to "733 US Highway 1, Suite 2A" |
| **Medical News Today** provider page | "David Kashuba, PT, Physical Therapist" | Corrects itself from NPPES; request a fix if it does not |
| **Facebook / Instagram / site** | "79,000", "80,000", "87,000" and "180,000" patients, and "37" or "39" years, depending on where you look | Pick one current set of numbers and use it everywhere |
| **Mobile Therapy Group** team page | Lists "Laura Drumm, MS, OTR/L, CHT" with no address; it ranks #3 for "certified hand therapist palm beach gardens" | **Owner question:** does Laura still work with them? If yes, fine. If not, ask them to remove it |

## 4. Directories that rank on page one for our money terms

- **ASHT Find a Therapist** ranks #6 for "certified hand therapist palm beach gardens" and lists
  other local CHTs. Laura can list her First Rehab practice address (ASHT membership required),
  and the HTCC "Find a CHT" directory is free for certified therapists. These are the most
  relevant links a hand therapy page can earn.
- **Zocdoc** ranks #1 for "physical therapist that accepts medicare palm beach gardens". It is
  paid per booking; worth a trial only if the front desk can take online bookings.
- **Healthgrades** ranks on page one for "physical therapy north palm beach". Claim it (above).
- **Yelp** appears for every query. Keep the profile accurate, but do not ask for Yelp reviews
  (Yelp penalizes solicitation).

## 5. Links worth earning (no schemes)

1. **Podcast guests.** More than a dozen surgeons and specialists have been on Pain 2 Power. A link
   from each guest's own practice site to their episode page is relevant, local and earned.
   The 2026-09 sweeps note outreach emails drafted 2026-09-03 that pointed at the generic
   podcast page because the episode recaps don't exist. Recap pages (allowed under the freeze,
   since Nick asks for them directly) make those asks land.
2. **WPTV.** The station already featured Dave. Offer a seasonal follow-up (fall prevention
   for snowbirds, pickleball injuries) to Shannon Cake.
3. **Sites Nick builds.** Legends Radio (where the show airs), RegenOrtho, Abacoa Podiatry and
   ELITE Sports Medicine are genuine referral and media relationships. A contextual link on a
   relevant page (the show page on Legends; a "rehab partners" mention where the referral
   relationship is real) is fine. A sitewide footer link on every client site is a link scheme.
   Don't do that.
4. **The November patient education event.** An event page on each partner's site linking to
   the hosts is natural.

## 6. Google Business Profile changes to consider (owner approval needed)

- **Add the category "Rehabilitation center".** Searches on our profile include "physical
  rehab near me", "rehabilitation center near me" and "physical rehab in north palm beach";
  our categories today are Physical Therapy Clinic, Physiotherapist, Wellness Program and
  Occupational therapist.
- **Review velocity** is the lever that matters most. The capture system already exists
  (`content/reviews/`). History shows it works when someone runs it: about a dozen reviews in
  the last week of Aug 2023 and another dozen in Aug 2025, then nothing. Make it weekly, not a burst.
- Clear the listing's pending edit.
- Add new photos monthly (team, gym, splint fabrication); competitors with big review counts
  also show large, recent photo sets.

## 7. Shipped in PR #104 from this audit

- A "From our patients" section on the hand therapy, occupational therapy and physical therapy
  pages: three verbatim Google review excerpts each, matched to the service, first name and
  last initial, linked to the listing. No review schema.
- The WPTV feature (April 2025) is now the homepage's first press mention.
- Reviews written for the other clinic are explicitly excluded in `build.py`.
