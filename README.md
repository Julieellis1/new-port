# James® — Portfolio

A cinematic portfolio website for a creative developer & motion designer, built from scratch with an original motion system inspired by award-winning references.

## Motion system

- **GSAP 3 + ScrollTrigger** — scroll-driven and entrance animation
- **Lenis** — buttery inertial smooth scrolling
- Cinematic preloader choreography (curtain lift, clip-path expand, masked letter-roll)
- Blur-to-sharp reveals, scroll-scrubbed character highlights, pinned 3D services cube
- Continuous + scroll-scrubbed marquees, odometer counters, perspective de-skew
- Draggable testimonial rail, hover image reveals, letter-wave CTA, custom cursor
- `prefers-reduced-motion` fallbacks and mobile adaptations throughout

## Structure

- `index.html` — homepage (hero, clients, manifesto, services cube, works, stats, testimonials, pricing, journal, FAQ, CTA)
- `studio.html` — about page (photo collage, scroll-driven image wipe, values)
- `works.html` — project index with hover previews
- `assets/css/style.css` — design system
- `assets/js/main.js` — motion engine
- `assets/img/` — 20 AI-generated WebP images (dark cinematic art direction, no baked-in text)

## Run locally

```bash
cd new-port
python3 -m http.server 8000
# open http://localhost:8000
```

Libraries load from CDN (jsDelivr); fonts from Google Fonts. Content is placeholder — swap in real projects, bio and testimonials.
