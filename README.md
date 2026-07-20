# First Rehabilitation of North Palm Beach — New Site

22-page static site. No frameworks, no build step needed for hosting — deploy the folder as-is.

## Drop your assets here (the site works without them, but shines with them)

| What | Where | Notes |
|---|---|---|
| Lighthouse hero video | `assets/media/lighthouse.mp4` | Plays full-screen behind the homepage hero. Keep it under ~15 MB (compress with Handbrake if needed). Add `assets/media/hero-poster.jpg` as the frame shown while it loads. |
| Clinic photo | `assets/media/clinic.jpg` | Homepage "Our Story" section |
| Founder photo | `assets/media/founder.jpg` | About page |
| Staff photos | `assets/team/david.jpg`, `laura.jpg`, `kayla.jpg`, `logan.jpg`, `nick.jpg` | Portrait orientation (4:5) looks best |
| Social gallery | `assets/social/post-1.jpg` … `post-8.jpg` | Square (1:1). These fill the rolling gallery on the homepage. Swap them whenever — just keep the filenames. |

Every image slot shows a labeled placeholder until you drop the file in, so you can see exactly what goes where by opening the site.

## The intake assistant

Every page has a chat-style intake assistant (bottom-right). It greets visitors shortly
after they arrive. "Ask a question" serves instant set answers (insurance, location and
hours, first visit, services, cost) from the FAQ list in `assets/js/intake.js` — no AI,
no API key, nothing to break — and anything typed becomes a front-desk message. For
appointments it collects: what they need, a short description, name, phone, email,
preferred call time, and insurance — then delivers the lead two ways at once:

1. **Supabase** — table `intake_leads` in the "First Rehabilitation App" project
   (supabase.com dashboard → Table Editor). This is the permanent record.
2. **Email** — a formatted copy to firstrehabnpb@gmail.com via FormSubmit.

No lead can be lost: every answer is saved on the visitor's device as they type, and if
their connection drops at the moment of submission, the lead is stored locally and re-sent
automatically the next time they're online on the site.

## Editing content

All content lives in `build.py` (phone, hours, team bios, condition copy, FAQ, podcast episodes).
Edit it, run `python3 build.py`, and every page regenerates. Or just hand it back to Claude with your changes.

## Hosting

Live deployment: Vercel project **firstrehabnpb-zywd** at
https://firstrehabnpb-zywd.vercel.app — imported from the GitHub repo
`nicholasbkashuba-lab/firstrehabnpb` (framework preset Other, no build command,
output directory `.`, production branch `claude/site-intake-agent-popup-hdfmxw`).
Every git push auto-deploys in about a minute. The older one-off projects
(firstrehab-site, firstrehabnpb, firstrehab, firstrehab-live) can be deleted
in the Vercel dashboard.

## Connecting the firstrehabnpb.com domain (kept at Wix)

1. Vercel dashboard → **firstrehab-site** → Settings → **Domains** → add
   `firstrehabnpb.com` and `www.firstrehabnpb.com`. Vercel displays the exact
   DNS records to use.
2. Wix dashboard → **Domains** → firstrehabnpb.com → **DNS Records** → replace
   the A record for `@` and the CNAME for `www` with the values Vercel showed.
3. DNS usually flips within an hour. The old Wix site keeps serving until then,
   so there is no downtime window.
