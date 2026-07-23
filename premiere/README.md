# Premiere Research Institute — Website Redesign

A bespoke, single-page marketing site for **Premiere Research Institute**, a neurological
clinical-research center in West Palm Beach, FL. Static HTML/CSS/JS — no build step, no
dependencies. Just open `index.html` or serve the folder.

## Preview
```bash
cd premiere
python3 -m http.server 8010
# → http://localhost:8010
```

## Design language
- **Palette:** midnight navy · synapse teal → violet gradient · warm amber · warm paper neutrals
- **Type:** Fraunces (editorial display serif) + Inter (UI/body), loaded from Google Fonts
- **Signature elements:** interactive neural-network canvas in the hero (pointer-reactive,
  reduced-motion & off-screen aware), gradient headline, scroll reveals, count-up stats,
  pulsing "Now enrolling" tags, single-open FAQ accordion, glassmorphism form cards.
- Fully responsive (desktop → tablet → mobile with slide-in nav) and `prefers-reduced-motion`
  aware. Accessible focus states, semantic landmarks, and `aria` labels throughout.

## Sections (all the current-site info, and more)
Hero · trust marquee · About · Research Areas (Alzheimer's/Memory, Parkinson's, Migraine, MS) ·
Why Participate · The Process · stats band · Our Team · mission quote · Community & Events
(+ "Invite Dr. Paul Winner to speak" form) · Newsletter + Special Edition · FAQ ·
Enroll / Contact · footer with Instagram / Facebook / TikTok.

## Brand assets
Built from the client-provided logo (`assets/img/logo-original.jpeg` — the "Discover Hope with
Premiere Research Institute" tree-brain mark). The tree mark was isolated from its white
background and exported to a transparent alpha PNG (`mark-mask.png`) used as a CSS mask, so the
mark recolors itself via `currentColor` — cream/white over the dark hero and footer, slate on the
light scrolled header. Favicons (`favicon-32.png`, `favicon-512.png`, `apple-touch-icon.png`) are
the mark on a midnight rounded square. The "Discover Hope with" tagline is kept in the lockup.

## Content notes / facts used
- **Address:** 4631 N. Congress Ave, Suite 200, West Palm Beach, FL 33407
- **Phone:** (561) 851-9400 · **Hours:** Mon–Fri, 9:00 AM – 4:30 PM
- **Team:** Paul Winner, DO, FAAN, FAHS (Senior Director); Reed Stone, MD, FAAN;
  Arnaldo Da Silva, MD; Robert Coppola, DO; Michael Alosilla, MD
- **Social:** instagram.com/premiereresearchinstitute · facebook.com/PremiereResearchInstitute ·
  tiktok.com/@askdrwinner

All body copy is original (written for this build), carrying the same information as the
current site. No clinical claims, patient testimonials, or credentials were invented.

## To go live — hand-offs for the owner
1. **Wire the forms.** The three forms (enroll, invite-to-speak, newsletter) validate and show
   a success state client-side only — there is no backend yet. In `assets/js/main.js`, POST
   `new FormData(form)` to an email/CRM endpoint (e.g. FormSubmit, Formspree, or a Supabase
   table) at the marked `NOTE:` before showing success.
2. **Special Edition Newsletter link.** The "2026 Issue" card links to `#newsletter` as a
   placeholder — point it at the real PDF/article URL.
3. **Real photography.** Doctor portraits use elegant monogram avatars by design. Drop in real
   headshots (replace `.ld-portrait` / `.tcard-portrait` with `<img>`) when available.
4. **Domain / analytics / meta image.** Set the real canonical domain, add an OG share image
   (`og:image`), and drop in an analytics tag if desired.
