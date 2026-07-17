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
after they arrive, and collects: what they need, a short description, name, phone, email,
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

## Deploying to Vercel

1. Push this folder to a GitHub repo (or drag-and-drop the folder at vercel.com/new)
2. Framework preset: **Other** — no build command, output directory = root
3. You'll get a preview URL like `firstrehab-site.vercel.app`
4. When ready: in Wix's domain settings, point your domain's DNS at Vercel (Vercel shows you the exact A/CNAME records under Project → Settings → Domains)

The live Wix site stays untouched until you flip DNS.
