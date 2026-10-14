---
name: podcast-guest
description: Research a Pain 2 Power guest and add or refresh their profile on firstrehabnpb.com/guests.html — background from the episode and from their own public pages, credentials, practice, and verified website and social links. Use when tools/guest-sync.py check reports a missing guest, when the episode watcher routine hands off a new guest, or when Nick says "add the guest", "guest page", "update <guest>'s profile", "link their socials", or "research the guest".
---

# Pain 2 Power guest profile

Nick, 2026-10-14: every guest gets a profile on /guests.html, built from what they said on
the show AND from researching them online, with their sites and socials linked, and it must
run without him. This skill is the research half. `tools/guest-sync.py` says what is
missing and refuses a file that is not fit to ship; `build.py` renders whatever passes.

These are real people, mostly physicians, on a medical practice's website. **A missing fact
is fine. A wrong fact is not.** When in doubt, leave it out and say so in `research_notes`.

## Order of work

1. `python3 tools/guest-sync.py check` lists episodes with no guest file. Episode labels
   are Spotify's numbering, the one in `EPISODES` in build.py.
2. **What they said on the show.** The episode's blurb in `EPISODES` (build.py), plus
   `transcript-full.md` (or `transcripts.md`) on the episode's media branch:
   `curl -s https://raw.githubusercontent.com/nicholasbkashuba-lab/firstrehabnpb/media/ep{NN}-clips/transcript-full.md`.
   Branch numbers have drifted from Spotify's before (`media/ep16-clips` holds Episode 17,
   Goodwin), so check the transcript's "Guest:" line names the right person.
3. **Who they are.** Search the web: Firecrawl (`mcp__Firecrawl__firecrawl_search` /
   `firecrawl_scrape`, via ToolSearch) when the session has it, otherwise WebSearch and
   WebFetch. Open each page you cite; a fact goes in only if you saw it on that page.
4. Write `content/guests/<slug>.json` (shape below). Slug = lowercase last name.
5. `python3 tools/guest-sync.py validate content/guests/<slug>.json` until it prints `ok`.
6. `python3 build.py`, then look at the guest's card in guests.html.
7. If you verified an Instagram handle, note it for the clip collaborator step in
   `pain2power-episode`. It still goes to Nick to confirm before a post uses it: a wrong
   handle fails the whole post on every platform.

## Sources

Best first: the guest's own website; their practice, hospital or employer profile; a
licensing or certification body; a university page; reputable local news. Healthgrades,
Vitals, WebMD, Doximity, ZoomInfo and people-search sites are never a fact's only source
(validate rejects them). Never use or mention review ratings. Two sources disagree → leave
the fact out and note it.

**Identity check.** Common names collide. Match specialty + Palm Beach County / South
Florida + a detail said on air (the practice name, usually). Cannot confirm → no web facts,
say so in `research_notes`.

**Links.** Only a link you can prove is theirs: linked FROM their official site or practice
profile, or its bio names them and their practice. Business accounts are fine and say so in
the label ("Pilates Life on Instagram"). `verified_by` records how you know. Never guess a
handle.

**Exclude** home addresses, family details not shared on air, lawsuits or disciplinary
matters, politics, ratings, anything not about their work or their episode.

**People already on the site** (First Rehabilitation's own staff, like Kayla Dorsey and Logan
Van Sant): no web research. Use the `TEAM` entry in build.py and link /about.html.

## Writing

Plain, warm, factual, third person. **No em or en dashes** (validate rejects them). No hype
words (renowned, world class, leading, cutting edge) unless quoting. No medical advice.
Numbers said on air are attributed to whoever said them ("he puts it at..."). HTML entities
for curly quotes and apostrophes (`&rsquo;` `&ldquo;` `&rdquo;`) and `&amp;`, to match the
rest of the site. `on_the_show` is 50 to 110 words; `headline` at most 70 characters.

## File shape

```json
{
  "slug": "butler",
  "name": "Matt Butler",
  "honorific": "Dr.",
  "credentials": "MD",
  "headline": "Hand and upper extremity orthopedic surgeon",
  "affiliation": {"name": "HSS Florida", "url": "https://..."},
  "location": "West Palm Beach, FL",
  "episodes": ["Episode 16"],
  "on_the_show": "What they said on the show, from the blurb and transcript only.",
  "on_the_show_quote": "a short verbatim quote, or empty",
  "background": [{"text": "One sentence.", "source": "https://the page you saw it on"}],
  "links": [{"type": "profile", "label": "Dr. Butler at HSS", "url": "https://...", "verified_by": "HSS physician directory"}],
  "instagram_handle": "",
  "phone_on_air": "",
  "research_notes": "what you could not verify",
  "researched": "YYYY-MM-DD"
}
```

`honorific` is `""`, `"Dr."` or `"Captain"`. `credentials` exactly as the guest's own site
writes them. Link `type` is one of website, profile, instagram, facebook, linkedin, x,
youtube, tiktok, podcast, book, other. A guest who comes back for a second episode gets
that label added to `episodes` in the same file, not a second file.

## Refreshing

`python3 tools/guest-sync.py stale --days 180` lists profiles due a re-check. Re-verify
affiliation and links (surgeons change practices: Dr. Elkhechen moved from Orthopaedic Care
Specialists to NYU Langone after his episode) and bump `researched`.
