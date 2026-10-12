# Clinic flyer (front + back, US Letter 8.5 x 11)

- `flyer.html` is the source. Facts are copied from build.py (PLANS, TEAM, hours, services).
  If any of those change, update this file too, then re-render.
- Render the print PDF and PNG previews:

      NODE_PATH=$(npm root -g) node flyer/render.js $PWD/flyer/flyer.html $PWD/flyer

- `img/hero.jpg` is a 2560x1440 frame from lighthouse-hd.mp4 (print-resolution, unlike hero-poster.jpg).
- `img/qr.png` points to /contact.html?utm_source=flyer&utm_medium=print&utm_campaign=clinic-flyer,
  so flyer scans show up as their own source in GA4 and Vercel Analytics.
- Printed through Canva: the PDF was imported as an editable Canva design.
