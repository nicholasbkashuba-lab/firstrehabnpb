# Brand reference

## Colors
| Token | Hex | Use |
|---|---|---|
| `--navy` | `#0B1D2D` | Primary. Backgrounds, headings, dark sections. |
| `--navy-2` | `#102A40` | Footer, raised panels on navy. |
| `--gold` | `#CBA15A` | Accent. Eyebrows, rules, primary buttons, active states. |
| `--gold-lt` | `#E0BE7E` | Gold hover only. |
| `--white` | `#FFFFFF` | Light sections. |
| `--paper` | `#F4F5F6` | Alternating light sections. |
| `--gray` | `#6B7178` | Secondary text, labels. |

Status colors (portal only): `--ok #2E9E5B`, `--watch #D89A2B`, `--bad #C0392B`.

Gold is an accent, not a background. Large gold fills read cheap against navy — the mockups use it for rules, small buttons, and single words.

## Type
- **Montserrat** 600/700/800 — display. Nearly always uppercase, letter-spacing `.12em`–`.22em`. The tracking is the signature; don't tighten it.
- **Nunito Sans** 300/400/600/700 — body. Substitutes for Avenir Next, which isn't web-licensed.

Body copy is 15–17px at 1.65 line-height. The audience skews 55+ — don't shrink it.

## Voice
Plain, competent, unhurried. It's a trust purchase: someone is handing over keys to an empty house.

- Concrete over superlative. "Timestamped photo report after every visit" beats "unparalleled service."
- No exclamation marks outside the flyer's "Contact Us Today!"
- Never manufacture fear. The hurricane and water-damage risks are real and speak for themselves.
- "Home watch," two words, lowercase mid-sentence.

Taglines in circulation: *We watch. You relax.* / *Professional. Reliable. Local.* / *That's the HomeCrew Standard.*

## Logo
Vector, inline SVG in both HTML files (nav, portal login, portal header, report header). White house chevron with overhang, four-pane gold gable window, white H legs, gold crossbar, gold plinths.

The compact version (portal top bar) drops the plinths — below ~28px they turn to mush.

Extract from the source for physical use: truck decals, polos, monument sign. It's resolution-independent.

## Assets
| File | Size | Use |
|---|---|---|
| `home-watch-stuart-fl.{webp,jpg}` | 2000×1150 | Desktop hero |
| `home-watch-stuart-fl-mobile.{webp,jpg}` | 1000×900 | Mobile hero |
| `firefighter-turnout-gear.{webp,jpg}` | 1100×594 | Firefighter card — **placeholder, low-res source** |
| `homecrew-home-watch-stuart-fl-og.jpg` | 1200×630 | Social link previews |

Filenames are keyword-descriptive on purpose. Google reads them as a local relevance signal. Keep that pattern for new images and always write real alt text.
