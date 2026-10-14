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

**History (Nick, 2026-10-14):** the Burns Rd clinic used to be connected to First
Rehabilitation and kept using the name after the split. Nick's goal is to win that brand
outright. The plan for that, kept to tactics that are legal and cannot backfire, is section 8.

What to do now:
- Always use the full name **First Rehabilitation of North Palm Beach** on listings, posts and
  signage, and never "First Rehab" on its own.
- Ask Google (in the review management screen) to remove or reassign reviews clearly about the
  other clinic. They are 5 stars, so this costs us review count; accuracy and a clean entity
  matter more, and a review that names their staff confuses our listing.
- Add a short, factual line to the About and Contact pages once the attorney in section 8 has
  seen it (ready text is there).

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
| **Mobile Therapy Group** team page | Lists "Laura Drumm, MS, OTR/L, CHT" with no address; it ranks #3 for "certified hand therapist palm beach gardens" | Correct as is: Laura also works for a second company (Nick, 2026-10-14). The fix is to make First Rehab visible in HER own records too: NPPES practice locations can list more than one address, and her LinkedIn, ASHT and HTCC entries should name First Rehabilitation of North Palm Beach as a practice location |

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

## 8. Winning the brand back (legal, and it compounds)

The goal is that anyone who searches "First Rehab" in northern Palm Beach County finds us first,
and that Google, insurers and AI tools never mix the two businesses again. Every tactic below
is lawful and none can be turned against us. Tactics that would backfire are listed at the end.

**Legal footing (attorney, this month).**
1. Have a Florida trademark attorney review who has rights to "First Rehab" and "First
   Rehabilitation" in this market. First Rehabilitation has used its name since 1991; the other
   clinic claims "over twenty years". A 1986 federal filing by an unrelated "FIRST REHAB, INC."
   for physical therapy services also exists (USPTO serials 73584664 and 73587603), so status
   and priority need a real search, not a guess. Bring any separation agreement from the split;
   it may already settle naming.
2. Depending on that advice: register the mark (federal or Florida), and if the attorney agrees
   it is supported, a cease-and-desist about the confusing name. The two misdirected reviews on
   our listing and the "first rehab pbg" searches are documented evidence of actual confusion.
3. Approve the disambiguation line before it ships. Ready text: "First Rehabilitation of North
   Palm Beach is an independent, family-owned clinic founded in 1991 by David Kashuba, Ph.D.,
   OTR. We operate one location, at 733 US Highway 1, Suite 2A, and are not affiliated with
   other clinics that use a similar name."

**Own every branded search.**
4. Make the entity unmistakable: the same full name, address and phone on NPPES, Healthgrades,
   Yelp, Apple Business Connect, Bing Places, Facebook, Instagram, LinkedIn and the website.
   Section 3 is the fix list.
5. Out-review them where it counts. Their West Palm Beach listing had about 155 reviews on
   2026-09-20 and their Palm Beach Gardens office has 92; we have 110 at our one office. A steady
   6 to 8 a month passes their biggest listing within about six months.
6. Optional: a small branded Google Ads campaign on our own name ("first rehabilitation north
   palm beach", "first rehab north palm beach") so the top of the page is ours even on a mixed
   query. Do not put their name or mark in ad text.

**Out-compete them on substance.** Their site has no schema, no meta descriptions and a lorem
ipsum location page. Ours has all of it plus a certified hand therapist, OT, a CORF, a wellness
gym and a podcast. Keep shipping depth; it already shows in search.

**Do not do any of these.** They break the law, Google's rules, or both, and would hand the
other side a counterclaim: fake or incentivized reviews (for us or against them), reporting
their listing as fake when it is a real clinic, disparaging statements about them anywhere,
bidding with their trademark in ad copy, or "negative SEO". The win comes from being the
obvious, better-documented First Rehabilitation, not from attacking the other one.

## 9. Cowork runbook

The browser work in sections 3, 4 and 6 is written up as one paste-ready prompt for a Cowork
session with Nick's browser: `docs/COWORK-LOCAL-FIXES.md`.
