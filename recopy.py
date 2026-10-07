#!/usr/bin/env python3
"""Rewrite new-port copy for Adebiyi Thompson. No em dashes in new copy.
Order matters: specific replacements containing 'James' run BEFORE the global rename."""
import re, os

REPO = os.path.expanduser("~/workspace/new-port-repo")
IDX = f"{REPO}/index.html"
WRK = f"{REPO}/works.html"
STU = f"{REPO}/studio.html"

def sub(path, old, new, count=1):
    with open(path) as f:
        s = f.read()
    assert old in s, f"NOT FOUND in {path}: {old[:70]}"
    s = s.replace(old, new, count)
    with open(path, "w") as f:
        f.write(s)

def rem_section(path, start_marker, end_marker):
    with open(path) as f:
        s = f.read()
    i = s.index(start_marker)
    j = s.index(end_marker)
    assert i < j, f"markers out of order in {path}"
    s = s[:i] + s[j:]
    with open(path, "w") as f:
        f.write(s)

# ============ PHASE 1: specific replacements that contain the old name ============
sub(IDX, "<title>James® — Creative Developer & Motion Designer</title>",
          "<title>Adebiyi Thompson — Web Designer</title>")
sub(IDX, '<meta name="description" content="James is a creative developer and motion designer crafting cinematic digital experiences. Available for select projects worldwide.">',
          '<meta name="description" content="Adebiyi Thompson is a web designer in Lagos crafting fast, modern websites for businesses worldwide. Available for select projects.">')
sub(WRK, "<title>Works — James®</title>", "<title>Works — Adebiyi Thompson</title>")
sub(WRK, '<meta name="description" content="Selected works by James — brand identities, cinematic websites and motion systems.">',
          '<meta name="description" content="Selected works by Adebiyi Thompson: websites for agencies, churches, schools, clinics and local businesses.">')
sub(STU, "<title>Studio — James®</title>", "<title>Studio — Adebiyi Thompson</title>")
sub(STU, '<meta name="description" content="The studio behind the work: how James thinks, what he values, and the process behind cinematic websites.">',
          '<meta name="description" content="The practice behind the work: how Adebiyi Thompson thinks, what he values, and the process behind fast, modern websites.">')
sub(STU, '<h2 class="display cta-title" data-wave>Work with James</h2>',
          '<h2 class="display cta-title" data-wave>Work with Adebiyi</h2>')
sub(STU, "James® is the independent practice of James — creative developer and motion designer. Strategy, identity, motion and code under one roof, with the obsession of a studio and the speed of a freelancer.",
          "Adebiyi Thompson is an independent web designer in Lagos. Web design, branding, ideation and SEO under one roof, with the obsession of a studio and the speed of a freelancer.")

# ============ PHASE 2: global rename + email + journal link removal ============
for p in (IDX, WRK, STU):
    sub(p, "James®", "Adebiyi Thompson")
    sub(p, "hello@james.studio", "hello@adebiyithompson.com")
    sub(p, '<a href="index.html#journal" class="nl">Journal</a>\n', '')
    sub(p, '<li><a href="index.html#journal">Journal</a></li>', '')

# ============ PHASE 3: index.html copy ============
sub(IDX, '<div class="hero-side" data-hero-chrome>Lagos — Worldwide<br>Portfolio 2026</div>',
          '<div class="hero-side" data-hero-chrome>Lagos, Nigeria<br>Portfolio 2026</div>')
sub(IDX, '<h1 class="display h-xl hero-title" data-hero-title>Creative Developer</h1>',
          '<h1 class="display h-xl hero-title" data-hero-title>Web Designer</h1>')
sub(IDX, "I design and build cinematic digital experiences — where motion, code and art direction move as one. Currently taking on select projects.",
          "I design and build fast, modern websites for businesses that want to look established and get found on Google. Currently taking on select projects.")

sub(IDX, '<div class="kicker" data-reveal>Selected clients</div>',
          '<div class="kicker" data-reveal>Selected work</div>')
sub(IDX, "<h2 class=\"display h-lg\" data-reveal>Trusted by teams<br>with taste</h2>",
          "<h2 class=\"display h-lg\" data-reveal>Recent projects<br>across 10 industries</h2>")
sub(IDX, "Over the past six years I've partnered with startups, studios and brands to ship websites that feel alive — work that wins attention and keeps it.",
          "Recent work spans SEO agencies, churches, schools, clinics and local businesses. Every project is designed and built by hand: mobile-first, fast, and shipped on time.")
for old_name, new_name in [("Northbeam", "xylvar"), ("Arcadia", "Movaldem"),
                           ("Lumen Co.", "Esriltor"), ("Fieldnotes", "Premier HVAC"),
                           ("Vantage", "Bomorn Haven"), ("Mono&amp;Co", "ZoeSmile"),
                           ("Halcyon", "Litmern"), ("Orbital", "VoltEdge")]:
    sub(IDX, f">{old_name}</div>", f">{new_name}</div>")

sub(IDX, "Motion is not decoration. It is the interface between attention and meaning — and I choreograph it with intent.",
          "Good design is not decoration. It is how a business earns trust in the first five seconds, and I build every page to earn it.")
sub(IDX, "Every project starts from the same question: what should this feel like? From that feeling I build the system — art direction, interaction model, motion language, and code — until the experience is unmistakably alive.",
          "Every project starts from the same question: what should this do for the business? From that answer I build the site: structure, copy, design and code, until it is fast, clear and unmistakably alive.")

sub(IDX, "Capabilities — scroll to rotate", "Capabilities: scroll to rotate")
sub(IDX, '<div class="face-num">01 / Strategy</div><h3>Strategy</h3><p>Positioning, narrative and creative direction — the thinking that makes the work inevitable.</p>',
          '<div class="face-num">01 / Web Design</div><h3>Web Design</h3><p>Custom, mobile-first websites designed to convert visitors into customers. No templates, no page builders, just fast hand-built pages.</p>')
sub(IDX, '<div class="face-num">02 / Identity</div><h3>Identity</h3><p>Visual identities and design systems built to flex across screens, motion and print.</p>',
          '<div class="face-num">02 / Branding</div><h3>Branding</h3><p>Identities with a point of view. Logos, color systems and art direction that make small businesses look established.</p>')
sub(IDX, '<div class="face-num">03 / Motion</div><h3>Motion</h3><p>Choreographed interfaces, scroll narratives and micro-interactions with cinematic timing.</p>',
          '<div class="face-num">03 / Ideation</div><h3>Ideation</h3><p>Naming, concepts and creative direction. The thinking before the pixels, so the pixels have something to say.</p>')
sub(IDX, '<div class="face-num">04 / Design</div><h3>Design</h3><p>High-performance websites engineered by hand — no templates, no shortcuts.</p>',
          '<div class="face-num">04 / SEO</div><h3>SEO</h3><p>Technical audits, on-page fixes and monthly retainers backed by live SERP data. Plain-English reporting, no vanity metrics.</p>')

sub(IDX, "<h2 class=\"display h-lg\" data-reveal>Work that<br>moves people</h2>",
          "<h2 class=\"display h-lg\" data-reveal>Work that<br>earns trust</h2>")
sub(IDX, "Nebula — Nebula — Nebula —&nbsp;", "VoltEdge — VoltEdge — VoltEdge —&nbsp;")
sub(IDX, '<img src="assets/img/work-nebula.webp" alt="Nebula brand identity project">',
          '<img src="assets/img/work-nebula.webp" alt="VoltEdge e-commerce project">')
sub(IDX, '<div class="tags"><span>Brand Identity</span><span>Art Direction</span><span>2026</span></div>\n        <span>A luminous identity for a space-tech startup, from logotype to launch film.</span>',
          '<div class="tags"><span>E-commerce</span><span>Web Design</span><span>2026</span></div>\n        <span>A 29-page electronics store with cart, checkout and wishlist, built from scratch.</span>')
sub(IDX, "Pulse — Pulse — Pulse —&nbsp;", "Esriltor — Esriltor — Esriltor —&nbsp;")
sub(IDX, '<img src="assets/img/work-pulse.webp" alt="Pulse fintech app project">',
          '<img src="assets/img/work-pulse.webp" alt="Esriltor estate agency project">')
sub(IDX, '<div class="tags"><span>Product</span><span>Motion System</span><span>2025</span></div>\n        <span>Fintech app with a living motion system — every number, chart and transition choreographed.</span>',
          '<div class="tags"><span>Estate Agency</span><span>Web Design</span><span>2026</span></div>\n        <span>A 19-page estate agency site with listings, filters and viewing forms.</span>')
sub(IDX, "Terra — Terra — Terra —&nbsp;", "xylvar — xylvar — xylvar —&nbsp;")
sub(IDX, '<img src="assets/img/work-terra.webp" alt="Terra architecture studio website">',
          '<img src="assets/img/work-terra.webp" alt="xylvar SEO agency project">')
sub(IDX, '<div class="tags"><span>Web Design</span><span>Development</span><span>2025</span></div>\n        <span>Award-nominated portfolio site for an architecture studio — concrete poetry in the browser.</span>',
          '<div class="tags"><span>SEO Agency</span><span>Branding</span><span>2026</span></div>\n        <span>A light, confident marketing site for an SEO agency, with honest copy throughout.</span>')

sub(IDX, "<h2 class=\"display h-lg\" data-reveal>Proof in<br>motion</h2>",
          "<h2 class=\"display h-lg\" data-reveal>The work<br>so far</h2>")
sub(IDX, '<div class="stat-num" data-count="48"></div><p>Projects shipped across brand, web and motion.</p>',
          '<div class="stat-num" data-count="11"></div><p>Live projects shipped across web, brand and SEO.</p>')
sub(IDX, '<div class="stat-num" data-count="12"></div><p>International design awards and honourable mentions.</p>',
          '<div class="stat-num" data-count="94"></div><p>Pages designed and built, mobile-first.</p>')
sub(IDX, '<div class="stat-num" data-count="6"></div><p>Years crafting interfaces that feel cinematic.</p>',
          '<div class="stat-num" data-count="10"></div><p>Industries covered, from churches to clinics.</p>')

# remove invented sections: testimonials, pricing, journal
rem_section(IDX, "<!-- ============ TESTIMONIALS ============ -->", "<!-- ============ PRICING ============ -->")
rem_section(IDX, "<!-- ============ PRICING ============ -->", "<!-- ============ JOURNAL ============ -->")
rem_section(IDX, "<!-- ============ JOURNAL ============ -->", "<!-- ============ FAQ ============ -->")

# faq
sub(IDX, "Most builds run 4–8 weeks: one week of discovery and direction, two to three weeks of design and motion, then development, tuning and launch. Partner engagements run month to month.",
          "Most websites run 3 to 6 weeks: one week of direction and structure, two to three weeks of design and build, then testing and launch. Larger platforms are scoped individually.")
sub(IDX, '<button class="faq-q">Do you work with existing brands and codebases?<span class="plus"></span></button>',
          '<button class="faq-q">Can you redesign my existing website?<span class="plus"></span></button>')
sub(IDX, "Yes. I can extend an existing identity into motion, or rebuild the front-end of a product while your team keeps shipping. The only requirement is taste alignment.",
          "Yes. I can rebuild your current site with stronger structure, faster pages and clearer copy, without losing what already works.")
sub(IDX, '<button class="faq-q">How do you handle performance with heavy animation?<span class="plus"></span></button>',
          '<button class="faq-q">Will my website show up on Google?<span class="plus"></span></button>')
sub(IDX, "GPU-friendly transforms only, lazy-loaded media, reduced-motion fallbacks, and simplified mobile behavior. Cinematic should never mean sluggish.",
          "Every build ships with the SEO fundamentals done right: clean structure, fast pages, proper meta and semantic HTML. Monthly SEO retainers are available if you want ongoing growth.")
sub(IDX, '<button class="faq-q">Can you join as a contractor inside our team?<span class="plus"></span></button>',
          '<button class="faq-q">Do you build e-commerce stores?<span class="plus"></span></button>')
sub(IDX, "That's exactly what the Partner tier is for — embedded capacity with the taste of a studio and the speed of a freelancer.",
          "Yes. Product catalogs, carts, checkout flows and wishlists, all custom-built and mobile-first. See VoltEdge in the works archive for a full example.")
sub(IDX, "Lagos, working worldwide across time zones. Async-first process, weekly live reviews. It hasn't mattered yet.",
          "Lagos, Nigeria, working worldwide across time zones. Async-first process with weekly live reviews. It hasn't mattered yet.")

# cta + footer (index)
sub(IDX, '<h2 class="display cta-title" data-wave>Let\'s make it move</h2>',
          '<h2 class="display cta-title" data-wave>Let\'s build yours</h2>')
sub(IDX, "Have a project with a pulse? Tell me what it should feel like.",
          "Have a project in mind? Tell me what it should do for your business.")
sub(IDX, "<p>Cinematic websites, identities and motion systems — designed and built by hand.</p>",
          "<p>Fast, modern websites for businesses that want to look established. Designed and built by hand.</p>")
sub(IDX, "<span>Motion study — original build inspired by award-winning references.</span>",
          "<span>Designed and built by hand.</span>")

# ============ PHASE 4: works.html ============
sub(WRK, "A rolling archive of identities, websites and motion systems. Hover any row to preview.",
          "A rolling archive of real, shipped projects. Hover any row to preview.")
sub(WRK, "2024 — 2026 — 2024 — 2026 —&nbsp;", "2026 · Shipped · 2026 · Shipped ·&nbsp;")

projects = [
    ("xylvar", "SEO Agency Website", "https://xylvar.pages.dev", "work-nebula.webp"),
    ("Movaldem", "Church Platform", "https://movaldem.teta.dpdns.org", "work-pulse.webp"),
    ("Esriltor", "Estate Agency", "https://julieellis1.github.io/portfolio-demos/esriltor/", "work-terra.webp"),
    ("Premier HVAC", "HVAC Company", "https://julieellis1.github.io/portfolio-demos/premier-hvac/", "work-flux.webp"),
    ("Bomorn Haven", "Restaurant", "https://julieellis1.github.io/portfolio-demos/bomorn-haven/", "service-motion.webp"),
    ("ZoeSmile", "Dental Clinic", "https://zoesmile.teta.dpdns.org", "service-identity.webp"),
    ("Litmern Consults", "Consulting Firm", "https://julieellis1.github.io/portfolio-demos/litmern-consults/", "service-design.webp"),
    ("SAG Ministry", "Ministry Website", "https://test.teta.dpdns.org", "service-strategy.webp"),
    ("Marksheet", "School Platform", "https://marksheet.top", "hero-bg-1.webp"),
    ("Clinic Staff App", "Hospital Web App", "https://omh.teta.dpdns.org", "hero-bg-2.webp"),
    ("VoltEdge", "E-commerce Store", "https://julieellis1.github.io/portfolio-demos/voltedge/", "hero-bg-3.webp"),
]
with open(WRK) as f:
    s = f.read()
rows = []
for i, (name, cat, url, img) in enumerate(projects, 1):
    rows.append(
        f'    <a href="{url}" target="_blank" rel="noopener" class="work-row" data-reveal data-hover-image="assets/img/{img}" data-cursor="View">\n'
        f'      <span class="idx">{i:02d}</span><h3>{name}</h3><span class="yr">{cat} — 2026</span>\n'
        f'    </a>')
new_block = "\n".join(rows)
s2 = re.sub(r'(    <a href="#" class="work-row".*?</a>\n){6}', new_block + "\n", s, flags=re.S)
assert s2 != s, "works rows regex did not match"
with open(WRK, "w") as f:
    f.write(s2)

sub(WRK, "More projects available on request — including work under NDA.",
          "All eleven projects are live and clickable.")
sub(WRK, "<p>Cinematic websites, identities and motion systems — designed and built by hand.</p>",
          "<p>Fast, modern websites for businesses that want to look established. Designed and built by hand.</p>")
sub(WRK, "<span>Motion study — original build inspired by award-winning references.</span>",
          "<span>Designed and built by hand.</span>")

# ============ PHASE 5: studio.html ============
sub(STU, "No account managers, no handoffs lost in translation. You talk to the person who designs it, animates it and ships it — which is why the work feels coherent down to the last easing curve.",
          "No account managers, no handoffs lost in translation. You talk to the person who designs it and ships it, which is why the work feels coherent down to the last pixel.")
sub(STU, "Scroll to wipe from process to product — every project travels from rough sketch to cinematic launch.",
          "Scroll to wipe from process to product: every project travels from rough sketch to launch.")
sub(STU, '<div class="v-num">01</div><h3>Feeling first</h3><p>Every build starts with the emotion it should evoke. Layout, type and motion all serve that feeling — never the other way around.</p>',
          '<div class="v-num">01</div><h3>Business first</h3><p>Every build starts with what it should do for the business. Layout, copy and design all serve that goal, never the other way around.</p>')
sub(STU, '<div class="v-num">02</div><h3>Motion with intent</h3><p>Animation is interface, not decoration. If a transition doesn\'t communicate something, it doesn\'t ship.</p>',
          '<div class="v-num">02</div><h3>Fast by default</h3><p>A slow site is an unfinished site. Hand-built pages, optimized media and no bloat, so every page loads in a blink.</p>')
sub(STU, '<div class="v-num">03</div><h3>Performance is taste</h3><p>A stuttering site is an unfinished site. Sixty frames per second is the minimum bar for cinematic.</p>',
          '<div class="v-num">03</div><h3>Original, always</h3><p>No templates, no page builders, no shortcuts. Everything is designed and engineered by hand for the project at hand.</p>')
sub(STU, '<div class="v-num">04</div><h3>Original, always</h3><p>No templates, no page builders, no shortcuts. Everything is designed and engineered by hand for the project at hand.</p>',
          '<div class="v-num">04</div><h3>Honest SEO</h3><p>No vanity metrics, no invented numbers. Technical fixes and plain-English reporting backed by real search data.</p>')
sub(STU, "<p>Cinematic websites, identities and motion systems — designed and built by hand.</p>",
          "<p>Fast, modern websites for businesses that want to look established. Designed and built by hand.</p>")
sub(STU, "<span>Motion study — original build inspired by award-winning references.</span>",
          "<span>Designed and built by hand.</span>")

print("all replacements applied")
