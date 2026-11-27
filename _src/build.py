#!/usr/bin/env python3
"""Static site generator for legalmarketingfirm.net.

Run:  python3 _src/build.py      (from the repo root)
Writes every page as <path>/index.html so GitHub Pages serves clean URLs.
"""
import json, os, re, shutil, sys, html
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from data_services import SERVICES, SVC, GROUPS
from data_practices import PRACTICES, PRC, COMBO, COMBO_SERVICES, COMBO_PRACTICES
from data_cities import CITIES
from data_states import STATES, INITIAL_HUBS
from data_insights import ARTICLES, RESEARCH, REVIEWED, AUTHOR, AUTHOR_ROLE

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE = 'https://www.legalmarketingfirm.net'
EMAIL = 'hello@legalmarketingfirm.net'
GA = 'G-HBNSL2MQQ1'
TODAY = date.today().isoformat()
VER = TODAY.replace('-', '')
ORG_ID = SITE + '/#organization'
WEB_ID = SITE + '/#website'
PAGES = []          # (path, priority) for sitemap
CALC_N = [0]

def e(s): return html.escape(str(s), quote=True)

# ------------------------------------------------------------------ icons
ICONS = {
 'arrow-right': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
 'arrow-left': '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
 'menu': '<line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/>',
 'x': '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
 'chevron-down': '<path d="m6 9 6 6 6-6"/>', 'chevron-up': '<path d="m18 15-6-6-6 6"/>',
 'check': '<path d="M20 6 9 17l-5-5"/>',
 'clock': '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
 'shield-check': '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
 'mail': '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
 'tv': '<rect width="20" height="15" x="2" y="7" rx="2" ry="2"/><polyline points="17 2 12 7 7 2"/>',
 'globe': '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
 'trending-up': '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
 'crosshair': '<circle cx="12" cy="12" r="10"/><line x1="22" x2="18" y1="12" y2="12"/><line x1="6" x2="2" y1="12" y2="12"/><line x1="12" x2="12" y1="6" y2="2"/><line x1="12" x2="12" y1="22" y2="18"/>',
 'monitor': '<rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/>',
 'map-pin': '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
 'search': '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
 'sparkles': '<path d="M12 3l1.9 5.8L20 10.7l-6.1 1.9L12 18.4l-1.9-5.8L4 10.7l6.1-1.9z"/><path d="M19 17v4"/><path d="M17 19h4"/>',
 'message-square': '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 'file-text': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>',
 'star': '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
 'video': '<path d="m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
 'target': '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
 'compass': '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
 'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
 'radio': '<circle cx="12" cy="12" r="2"/><path d="M16.24 7.76a6 6 0 0 1 0 8.49"/><path d="M7.76 16.24a6 6 0 0 1 0-8.49"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/><path d="M4.93 19.07a10 10 0 0 1 0-14.14"/>',
 'calculator': '<rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" x2="16" y1="6" y2="6"/><line x1="16" x2="16" y1="14" y2="18"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/>',
 'scale': '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
}
def ic(name, size=20, cls='ic'):
    return f'<svg class="{cls}" width="{size}" height="{size}" aria-hidden="true"><use href="#i-{name}"/></svg>'
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + ''.join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items()) + '</defs></svg>'
ARROW = ic('arrow-right', 18)

# ------------------------------------------------------------------ chrome
NAV = [('Services', '/services/'), ('Practice Areas', '/practice-areas/'), ('Markets', '/markets/'), ('Results', '/results/'),
       ('Insights', '/insights/'), ('About', '/about/'), ('Contact', '/contact/')]

def header(path):
    def on(href): return ' class="on" aria-current="page"' if (path == href or (href != '/' and path.startswith(href))) else ''
    links = ''.join(f'<a href="{h}"{on(h)}>{t}</a>' for t, h in NAV)
    mlinks = f'<a href="/"{on("/") if path=="/" else ""}>Home</a>' + links
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="hdr-in">
<a href="/" class="hdr-logo" aria-label="Legal Marketing Firm home"><img src="/assets/logo-wordmark.png" alt="Legal Marketing Firm" width="160" height="22"></a>
<nav class="hdr-nav" aria-label="Primary">{links}</nav>
<a href="/free-marketing-audit/" class="btn btn-accent btn-sm hdr-cta">Free Marketing Audit</a>
<button class="hdr-burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mnav">{ic('menu')}</button>
</div>
<nav id="mnav" class="mnav" aria-label="Mobile" hidden>{mlinks}<a href="/tools/" >Free Tools</a><a href="/free-marketing-audit/" class="mnav-cta">Free Marketing Audit →</a></nav>
</header>'''

def footer():
    svc = ''.join(f'<a href="/{s["slug"]}/">{e(s["name"].replace("Law Firm ", ""))}</a>' for s in SERVICES[:10])
    prc = ''.join(f'<a href="/practice-areas/{p["slug"]}/">{e(p["name"])}</a>' for p in PRACTICES[:8])
    mk = ''.join(f'<a href="/markets/{STATES[a][1]}/">{e(STATES[a][0])}</a>' for a in INITIAL_HUBS[:8])
    return f'''<footer class="ftr"><div class="wrap ftr-in">
<div class="ftr-top"><img src="/assets/logo-stacked.png" alt="Legal Marketing Firm" height="56" width="160">
<p style="max-width:420px;font-size:14px">A legal marketing firm for law firms: SEO, paid search, AI search and integrated advertising tied to one outcome — more signed clients. <a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div class="ftr-cols">
<div><h2>Services</h2>{svc}<a href="/services/">All services →</a></div>
<div><h2>Practice Areas</h2>{prc}<a href="/practice-areas/">All practice areas →</a></div>
<div><h2>Markets</h2>{mk}<a href="/markets/">All markets →</a></div>
<div><h2>Free Tools</h2><a href="/tools/law-firm-marketing-budget-calculator/">Marketing Budget Calculator</a><a href="/tools/marketing-roi-calculator/">ROI Calculator</a><a href="/tools/cost-per-lead-calculator/">Cost Per Lead Calculator</a><a href="/tools/intake-conversion-calculator/">Intake Conversion Calculator</a><a href="/tools/ai-visibility-audit/">AI Visibility Audit</a><a href="/tools/">All tools →</a></div>
<div><h2>Company</h2><a href="/about/">About</a><a href="/results/">Results</a><a href="/insights/">Insights</a><a href="/contact/">Contact</a><a href="/free-marketing-audit/">Free Marketing Audit</a><a href="/privacy-policy/">Privacy Policy</a><a href="/terms/">Terms</a></div>
</div>
<div class="ftr-bot"><span>© {date.today().year} LegalMarketingFirm.net. All rights reserved. We are a marketing agency, not a law firm, and do not provide legal advice.</span><span>Results shown are marketing metrics, not case outcomes.</span></div>
</div></footer>'''

def cta_band(h=None, btn='Get Your Free Marketing Audit', href='/free-marketing-audit/'):
    h = h or 'The Scoreboard Is Public. <em>Is Your Firm on It?</em>'
    return f'''<section class="cta-band"><div class="wrap cta-in"><h2 class="cta-h">{h}</h2>
<a href="{href}" class="btn btn-primary btn-lg">{btn} {ARROW}</a></div></section>'''

def crumbs_html(items):
    out = []
    for i, (t, h) in enumerate(items):
        if i == len(items) - 1: out.append(f'<span aria-current="page">{e(t)}</span>')
        else: out.append(f'<a href="{h}">{e(t)}</a><span aria-hidden="true">/</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ''.join(out) + '</nav>'

def crumbs_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, "item": SITE + h} for i, (t, h) in enumerate(items)]}

ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": ORG_ID, "name": "Legal Marketing Firm",
       "alternateName": "LegalMarketingFirm.net", "url": SITE + '/', "logo": SITE + "/assets/logo-stacked.png", "email": EMAIL,
       "description": "A legal marketing firm for law firms: SEO, paid search, AI search optimization and integrated advertising tied to qualified intake and signed cases.",
       "areaServed": {"@type": "Country", "name": "United States"},
       "knowsAbout": ["Legal marketing", "Law firm SEO", "Google Ads for law firms", "Local Services Ads", "Generative engine optimization", "Answer engine optimization", "AI search optimization", "Law firm intake optimization"],
       "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "email": EMAIL, "areaServed": "US", "availableLanguage": "English"},
       "founder": {"@id": SITE + "/about/#matt-hensler"}}
WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "@id": WEB_ID, "url": SITE + '/', "name": "Legal Marketing Firm", "publisher": {"@id": ORG_ID}}
PERSON = {"@context": "https://schema.org", "@type": "Person", "@id": SITE + "/about/#matt-hensler", "name": AUTHOR, "jobTitle": "Head of Strategy",
          "worksFor": {"@id": ORG_ID}, "url": SITE + "/about/", "sameAs": ["https://www.linkedin.com/in/mjhensler"],
          "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Full Sail University"}, {"@type": "CollegeOrUniversity", "name": "DePaul University"}]}

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def faq_block(faqs, dark=True, first_open=True):
    items = []
    for i, (q, a) in enumerate(faqs):
        op = first_open and i == 0
        items.append(f'<div class="acc-item{" open" if op else ""}"><button type="button" class="acc-q" aria-expanded="{str(op).lower()}">{e(q)}<span class="acc-plus" aria-hidden="true">+</span></button><div class="acc-a"{"" if op else " hidden"}><p>{e(a)}</p></div></div>')
    return f'<div class="acc{" dark" if dark else ""}">' + ''.join(items) + '</div>'

def faq_section(faqs, title='Frequently Asked <em>Questions.</em>', sub=''):
    return f'''<section class="band"><div class="wrap sec faq-grid"><div class="stack-sm"><span class="eyebrow">FAQ</span><h2 class="h2">{title}</h2>{f'<p class="body-lg">{e(sub)}</p>' if sub else ''}</div>{faq_block(faqs)}</div></section>'''

def page(path, title, desc, body, schema=None, crumbs=None, ptype='page', market='', practice='', cta=True, cta_h=None,
         robots='index, follow', priority=0.6, og_type='website', sitemap=True, canonical=None):
    canonical = canonical or (SITE + path)
    sch = [ORG, WEBSITE] if path == '/' else [ORG]
    if crumbs: sch.append(crumbs_schema(crumbs))
    sch += (schema or [])
    sch_html = '\n'.join('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False, separators=(',', ':')) + '</script>' for s in sch)
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Legal Marketing Firm">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/og-image.jpg">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/og-image.jpg">
<meta name="theme-color" content="#03182A">
<link rel="icon" type="image/png" href="/assets/logo-stacked.png">
{sch_html}
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA}');</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Rubik:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Source+Serif+4:ital,wght@0,400;0,600;1,400;1,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={VER}">
</head>
<body data-page-type="{ptype}" data-market="{e(market)}" data-practice="{e(practice)}">
{header(path)}
<div id="main">
{body}
</div>
{cta_band(cta_h) if cta else ''}
{footer()}
{SPRITE}
<script src="/assets/site.js?v={VER}" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, path.strip('/'), 'index.html') if path != '/' else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(doc)
    if sitemap and robots.startswith('index'): PAGES.append((path, priority))

def redirect(path, to):
    out = os.path.join(ROOT, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Redirecting…</title><link rel="canonical" href="{SITE}{to}"><meta name="robots" content="noindex, follow"><meta http-equiv="refresh" content="0; url={to}"><script>location.replace("{to}"+location.search)</script></head><body><p>This page moved to <a href="{to}">{SITE}{to}</a>.</p></body></html>')

# ------------------------------------------------------------------ shared blocks
PRACTICE_OPTS = [p['name'] for p in PRACTICES] + ['Other']
GOAL_CARDS = [('maintain', 'Maintain Business', 5, 'Minimum recommended investment to maintain business and market presence.'),
              ('moderate', 'Moderate Growth', 10, 'Generate consistent leads and steadily grow your client base.'),
              ('accelerated', 'Accelerated Growth', 15, 'Increase case volume and capture greater market share.'),
              ('expansion', 'Market Expansion', 25, 'Enter new markets and aggressively pursue new business.')]
STATE_ABBRS = sorted(set([c['st'] for c in CITIES]) | {'AK','AR','CT','DE','HI','KS','ME','MD','MT','NH','NJ','OH','RI','VT','WV','WY'})

def calc(heading, intro, ptype, placement, market='', practice='', city='', state='', wrap=True, full=False):
    CALC_N[0] += 1
    cid = f'calc{CALC_N[0]}'
    goals = ''.join(f'''<label class="goal"><input type="radio" name="goal" value="{k}"{" checked" if k=="moderate" else ""}><span class="g-pct">{p}%</span><span class="g-name">{n}</span><span class="g-desc">{d}</span></label>''' for k, n, p, d in GOAL_CARDS)
    popts = '<option value="">Select…</option>' + ''.join(f'<option{" selected" if practice==o else ""}>{e(o)}</option>' for o in PRACTICE_OPTS)
    sopts = '<option value="">—</option>' + ''.join(f'<option{" selected" if state==a else ""}>{a}</option>' for a in STATE_ABBRS)
    h_tag = 'h1' if full else 'h2'
    block = f'''<section class="calc" id="{cid}" data-calc data-page-type="{ptype}" data-placement="{placement}" data-market="{e(market)}" data-practice="{e(practice)}" aria-labelledby="{cid}-h">
<form class="calc-form calc-in" novalidate>
<div class="calc-head"><span class="eyebrow">Free Tool · Law Firm Marketing Budget Calculator</span><{h_tag} id="{cid}-h">{heading}</{h_tag}><p>{intro}</p></div>
<div class="calc-fields">
<div class="cf"><label for="{cid}-rev">Annual gross firm revenue <span class="req">*</span></label><div class="money"><span aria-hidden="true">$</span><input id="{cid}-rev" name="revenue" type="text" inputmode="decimal" data-money autocomplete="off" required aria-describedby="{cid}-rev-err" placeholder="2,000,000"></div><p class="err-msg" id="{cid}-rev-err" role="alert" hidden>Enter your annual revenue (greater than $0).</p></div>
<div class="cf"><label for="{cid}-cur">Current monthly marketing investment <span class="hint">(optional)</span></label><div class="money"><span aria-hidden="true">$</span><input id="{cid}-cur" name="current" type="text" inputmode="decimal" data-money autocomplete="off" aria-describedby="{cid}-cur-hint {cid}-cur-err" placeholder="5,000"></div><p class="hint" id="{cid}-cur-hint">Media, agency fees, staff and tools. Leave blank if unsure; $0 is fine.</p><p class="err-msg" id="{cid}-cur-err" role="alert" hidden>Enter $0 or more, or leave it blank.</p></div>
</div>
<fieldset class="goals"><legend>Growth objective</legend>{goals}</fieldset>
<div class="calc-foot"><p class="calc-fine">Planning recommendations from LegalMarketingFirm.net — not industry averages or guaranteed outcomes. Total investment includes agency fees, media, personnel, technology and production.</p>
<button type="submit" class="btn btn-accent btn-lg">Calculate My Marketing Budget {ARROW}</button></div>
</form>
<div class="gate" hidden>
<div class="stack-xs"><h3>Your Personalized Marketing Budget Is Ready.</h3><p>Unlock your recommended monthly and annual investment and discover how your current budget aligns with your growth goals.</p></div>
<form class="gate-form" novalidate>
<input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">
<div class="gate-fields">
<div class="cf"><label for="{cid}-fn">First name <span class="req">*</span></label><input id="{cid}-fn" name="first_name" type="text" autocomplete="given-name" required></div>
<div class="cf"><label for="{cid}-ln">Last name <span class="req">*</span></label><input id="{cid}-ln" name="last_name" type="text" autocomplete="family-name" required></div>
<div class="cf"><label for="{cid}-firm">Firm name <span class="req">*</span></label><input id="{cid}-firm" name="firm_name" type="text" autocomplete="organization" required></div>
<div class="cf"><label for="{cid}-em">Business email <span class="req">*</span></label><input id="{cid}-em" name="email" type="email" autocomplete="email" required></div>
<div class="cf"><label for="{cid}-web">Firm website <span class="req">*</span></label><input id="{cid}-web" name="site" type="url" inputmode="url" autocomplete="url" placeholder="https://" required></div>
<div class="cf"><label for="{cid}-pa">Primary practice area <span class="req">*</span></label><select id="{cid}-pa" name="practice_area" required>{popts}</select></div>
<div class="cf"><label for="{cid}-ph">Phone <span class="hint">(optional)</span></label><input id="{cid}-ph" name="phone" type="tel" autocomplete="tel"></div>
<div class="cf"><label for="{cid}-city">City <span class="hint">(optional)</span></label><input id="{cid}-city" name="city" type="text" autocomplete="address-level2" value="{e(city)}"></div>
<div class="cf"><label for="{cid}-st">State <span class="hint">(optional)</span></label><select id="{cid}-st" name="state" autocomplete="address-level1">{sopts}</select></div>
</div>
<label class="check"><input type="checkbox" name="consent"> Send me occasional legal marketing insights by email. (Optional — unsubscribe anytime.)</label>
<p class="privacy-note">We use your contact details and the figures you entered to send your results, prepare your report and follow up about our services. We don’t sell your information. See our <a href="/privacy-policy/">Privacy Policy</a>.</p>
<p class="status" role="alert" hidden></p>
<button type="submit" class="btn btn-accent btn-lg">Unlock My Marketing Budget {ARROW}</button>
</form></div>
<div class="results-panel" hidden aria-live="polite">
<h3 class="h2-md" style="font-size:clamp(24px,2.8vw,34px)">Your Recommended Marketing Budget</h3>
<div class="r-big"><div class="hl"><span class="mono-label">Recommended monthly budget</span><span class="v" data-r="monthly"></span></div><div><span class="mono-label">Recommended annual budget</span><span class="v" data-r="annual"></span></div><div><span class="mono-label">Growth objective</span><span class="v" style="font-size:22px;color:#fff" data-r="goal"></span></div></div>
<div class="r-compare" hidden>
<p class="r-msg"></p>
<div class="results-bars" style="padding:0;background:none">
<div class="bar-row"><div class="bar-head"><span>Current monthly investment</span><span class="bar-v" data-r="bar-cur-v"></span></div><div class="bar-track"><div class="bar" data-r="bar-cur" style="--w:0%"></div></div></div>
<div class="bar-row feat"><div class="bar-head"><span>Recommended monthly investment</span><span class="bar-v" data-r="bar-rec-v"></span></div><div class="bar-track"><div class="bar" data-r="bar-rec" style="--w:0%"></div></div></div>
</div>
<div class="r-grid"><div><span class="mono-label">Current monthly</span><span class="v" data-r="cur-m"></span></div><div><span class="mono-label">Current annual</span><span class="v" data-r="cur-a"></span></div><div><span class="mono-label">Current % of revenue</span><span class="v" data-r="cur-pct"></span></div><div><span class="mono-label">Monthly investment gap</span><span class="v" data-r="gap-m"></span></div><div><span class="mono-label">Annual investment gap</span><span class="v" data-r="gap-a"></span></div></div>
</div>
<div class="r-actions"><a href="/contact/" class="btn btn-accent btn-lg" data-act="plan">Get Your Personalized Marketing Plan {ARROW}</a><button type="button" class="btn btn-inverse btn-lg" data-act="report">Download Your Marketing Budget Report</button></div>
<p class="calc-fine">We’ve also emailed your results and a PDF report. Our framework provides general planning recommendations and does not guarantee growth outcomes.{'' if full else ' <a href="/tools/law-firm-marketing-budget-calculator/">See the full calculator and methodology</a>.'}</p>
</div>
</section>'''
    return f'<section class="wrap sec">{block}</section>' if wrap else block

PROOF = {
 'intake': ('+50%', 'Client intake form completions', 'The clearest signal of new business: more prospects completing the firm’s intake form.'),
 'visibility': ('+220%', 'Search visibility (Google & AI)', 'A large increase in how often the firm appeared across Google and AI search results.'),
 'paid': ('+62%', 'Paid search performance', 'Better results from the same paid search investment after restructuring and tracking.'),
 'reviews': ('+20%', 'Google reviews growth', 'A steadier flow of genuine client reviews.'),
 'social': ('+133%', 'Social media engagement', 'More engagement from content built around attorney expertise.'),
}
SCORE = [('Client Intake Forms', 'Client Intake Form Completions', '+50%', 50), ('Search Visibility', 'Search Visibility (Google & AI)', '+220%', 220),
         ('Web Traffic', 'Total Web Traffic', '+90%', 90), ('Paid Search', 'Paid Search Performance', '+62%', 62),
         ('Google Reviews', 'Google Reviews Growth', '+20%', 20), ('Social Engagement', 'Social Media Engagement', '+133%', 133)]

def proof_block(key):
    v, lbl, txt = PROOF[key]
    return f'''<section class="wrap sec-bottom"><div class="results" style="border-radius:10px">
<div class="results-feat" style="min-height:240px"><span class="mono-label dark">Real client result · {e(lbl)}</span><span class="results-feat-num" style="font-size:clamp(64px,26cqi,150px)" data-count="{v}">{v}</span></div>
<div class="results-bars"><span class="mono-label">Proof</span><p class="body-lg" style="color:#fff">{e(txt)}</p><p style="font-size:14px;color:var(--navy-300)">From a single multi-channel law firm engagement. Marketing metrics, not case outcomes; client name withheld for confidentiality.</p><a class="textlink" href="/results/law-firm-marketing-case-study/">Read the case study {ic("arrow-right",16)}</a></div>
</div></section>'''

def cards(items):
    return '<div class="cards">' + ''.join(f'<a class="card-link" href="{h}"><h3>{e(t)}</h3>{f"<p>{e(d)}</p>" if d else ""}<span class="go">{e(go)} →</span></a>' for t, d, h, go in items) + '</div>'

def svc_card(slug, go='Explore'):
    s = SVC[slug]; return (s['name'], s['lede'].split('. ')[0].rstrip('.') + '.', f'/{slug}/', go)

def head_block(crumbs, eyebrow, h1, lede, extra=''):
    return f'''<section class="wrap page-head">{crumbs_html(crumbs)}<span class="eyebrow">{eyebrow}</span><h1 class="h1">{h1}</h1><p class="lede" style="max-width:680px">{lede}</p>{extra}</section>'''

def market_city_url(c): return f'/markets/{c["state_slug"]}/{c["slug"]}/'

# ================================================================== HOME
def build_home():
    board = ''.join(f'<div class="board-cell"><span class="mono-label">{e(s[0])}</span><span class="board-num" data-count="{s[2]}">{s[2]}</span></div>' for s in SCORE[1:])
    channel_items = [
        ('01', 'tv', 'Traditional & Streaming', 'Broadcast TV, CTV/streaming, radio and outdoor — brand authority campaigns built to dominate your local market and stay top-of-mind when clients need you most.', ['TV & CTV', 'Radio', 'Billboard/OOH'], '/law-firm-tv-advertising/'),
        ('02', 'globe', 'Search Engine Optimization', 'Dominate local and national search for high-intent legal queries. Technical SEO, content authority and Google Business Profile management built to drive intake — not just rankings on paper.', ['Local SEO', 'Content Strategy', 'GBP Management'], '/law-firm-seo/'),
        ('03', 'trending-up', 'Google Ads & Paid Search', 'High-intent PPC campaigns built for legal — not broad traffic. LSAs for pay-per-lead, Google Ads for keyword control. Both, done right.', ['Google Ads', 'Local Services Ads', 'Retargeting'], '/law-firm-ppc/'),
        ('04', 'crosshair', 'AI Search Optimization (GEO)', 'Get recommended in ChatGPT, Perplexity, Gemini and Google AI Overviews when potential clients ask AI who to hire. The search strategy most firms haven’t touched yet.', ['ChatGPT Visibility', 'GEO', 'AEO', 'Entity Optimization'], '/law-firm-ai-search-optimization/'),
        ('05', 'monitor', 'Social Media & Reputation', 'Organic content, paid social and review management that builds trust before a prospect ever calls.', ['Meta Ads', 'Organic Content', 'Review Strategy'], '/law-firm-social-media/'),
        ('06', 'mail', 'Email, Text, Video & Intake', 'Nurture sequences, consent-based SMS, attorney video and intake optimization that keep prospects moving toward a signed retainer.', ['Email', 'SMS', 'Attorney Video', 'Intake'], '/law-firm-intake-optimization/'),
    ]
    body = f'''<section class="wrap hero-board">
<div class="hero-copy"><span class="eyebrow">Live Scoreboard · Real Client</span>
<h1 class="h-hero">A Legal Marketing Firm Built to Drive <em>Cases,</em> Not Just Clicks.</h1>
<p class="lede hero-sub">Most legal marketing firms run campaigns. <strong>We build growth systems.</strong> SEO, Google Ads, AI search optimization and integrated advertising — every channel, every dollar tied to one outcome: more signed clients for your firm.</p>
<div class="btns"><a href="/free-marketing-audit/" class="btn btn-accent btn-lg">Get Your Free Marketing Audit {ARROW}</a><a href="/results/" class="btn btn-inverse btn-lg">See Real Results</a></div></div>
<div class="board" aria-label="Client results scoreboard"><div class="board-feat"><span class="mono-label dark">Client Intake Forms</span><span class="board-feat-num" data-count="+50%">+50%</span></div>{board}</div>
</section>
<div class="rule"></div>
<section class="wrap sec stack-xl">
<h2 class="h2-xl section-title" style="max-width:960px">The Firms That Show Up in AI Search <em>Today</em> Own Tomorrow’s Market.</h2>
<div class="ai-duo">
<div class="ai-duo-item"><span class="mega" data-count="3×">3×</span><h3>ChatGPT Weekly Users Tripled in About 14 Months</h3><p>From 300M to 900M weekly users (OpenAI, Feb 2026). More of your future clients now start their search by asking AI.</p></div>
<div class="ai-duo-item"><span class="mega" data-count="5×">5×</span><h3>Higher Conversion Rate Than Traditional Search</h3><p>AI search traffic converts at 14.2% vs. Google’s 2.8% — about five times higher. People asking AI who to hire are ready to call.</p></div>
</div>
<div class="row-between"><p class="body-lg callout-urgency" style="max-width:680px">Most law firms haven’t done anything about AI search yet. That’s your window. The firms AI tools cite now build an advantage that compounds.</p>
<a href="/law-firm-ai-search-optimization/" class="btn btn-inverse btn-md">See How AI Search Works {ARROW}</a></div>
</section>
<section class="band"><div class="wrap sec stack-lg">
<div class="row-between end"><h2 class="h2 section-title" style="max-width:820px">We Don’t Run Campaigns. <em>We Build Growth Systems.</em></h2><a href="/services/" class="textlink">Here’s How We Do It {ic("arrow-right",16)}</a></div>
<div class="grid-cells pillars">
<div class="pillar"><span class="mono-k">Legal-First</span><h3>Built Around How Legal Clients Actually Think.</h3><p>We don’t pretend to be attorneys. But we know how people search for one, what earns their trust and what makes them call.</p></div>
<div class="pillar"><span class="mono-k">Outcome-Based</span><h3>More Intake. Better Leads. Cases That Convert.</h3><p>We focus on driving qualified intake and work alongside your team to make sure the leads coming in are worth your time.</p></div>
<div class="pillar"><span class="mono-k">Full-Funnel</span><h3>One Strategy. Every Channel.</h3><p>TV, CTV, radio, Google Ads, SEO, AI search, social, email, text — unified, not siloed.</p></div>
<div class="pillar"><span class="mono-k">AI-Enhanced</span><h3>Speed and Judgment. Not One or the Other.</h3><p>AI accelerates our work. Experienced legal marketing professionals make every strategic call.</p></div>
</div></div></section>
{calc('Are You Investing Enough in <em>Marketing?</em>', 'Enter your revenue and growth goal to see a recommended monthly and annual marketing budget for your firm.', 'home', 'home_featured')}
<section class="rule-top"><div class="wrap sec stack-lg">
<div class="stack-sm"><span class="eyebrow">Legal Marketing Services · Channel Board</span><h2 class="h2" style="max-width:900px">Every Channel. One Legal <em>Marketing Firm.</em></h2></div>
{channel_board(channel_items)}
</div></section>
<section class="band"><div class="wrap sec stack-lg">
<div class="row-between end"><h2 class="h2" style="max-width:820px">Marketing Built for Your <em>Practice.</em></h2><a href="/practice-areas/" class="textlink">All practice areas {ic("arrow-right",16)}</a></div>
<div class="chips-links">{''.join(f'<a href="/practice-areas/{p["slug"]}/">{e(p["name"])}</a>' for p in PRACTICES)}</div>
</div></section>
<section class="wrap sec stack-lg">
<div class="row-between end"><h2 class="h2" style="max-width:820px">From Major Metros to the Markets <em>Others Overlook.</em></h2><a href="/markets/" class="textlink">All markets {ic("arrow-right",16)}</a></div>
<p class="body-lg" style="max-width:760px">We help law firms win search, AI and paid visibility in 163 U.S. markets — with a focus on the smaller and mid-size cities where a focused firm can lead.</p>
<div class="chips-links">{''.join(f'<a href="{market_city_url(c)}">{e(c["name"])}, {c["st"]}</a>' for c in CITIES if c["pri"]=="priority")}</div>
</section>
<section class="band"><div class="wrap sec stack-lg">
<div class="row-between end"><h2 class="h2" style="max-width:820px">Straight Answers on Legal <em>Marketing.</em></h2><a href="/insights/" class="textlink">All insights {ic("arrow-right",16)}</a></div>
{cards([(a['title'], a['answer'][:150].rsplit(' ',1)[0]+'…', f"/insights/{a['slug']}/", 'Read') for a in ARTICLES[:6]])}
</div></section>'''
    page('/', 'Legal Marketing Firm | SEO, PPC & AI Search for Law Firms',
         'Grow your law firm with results-driven legal marketing, SEO, Google Ads, AI search optimization and integrated advertising. Request a free marketing audit.',
         body, ptype='home', priority=1.0)

def channel_board(items, sel=3):
    rows = ''
    for n, icon, t, b, tags, href in items:
        rows += f'''<div class="svc-item"><button type="button" class="svc-btn"><span class="svc-n">{n}</span><span class="svc-t">{e(t)}</span>{ic("arrow-right",16,"ic svc-chev")}</button>
<div class="svc-inline"><p>{e(b)}</p><div class="tags">{''.join(f'<span>{e(x)}</span>' for x in tags)}</div><a class="textlink" href="{href}">Explore {e(t)} {ic("arrow-right",16)}</a></div>
<template class="svc-icon"><svg>{ICONS[icon]}</svg></template></div>'''
    return f'''<div class="svc" data-sel="{sel}"><div class="svc-list">{rows}</div>
<div class="svc-detail" aria-live="polite"><div class="svc-detail-icon"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"></svg></div>
<span class="svc-detail-n mono-k"></span><h3 class="svc-detail-t"></h3><p class="svc-detail-b"></p><div class="tags lg svc-detail-tags"></div><a class="textlink svc-detail-link" href="/services/">Explore {ic("arrow-right",16)}</a></div></div>'''

# ================================================================== SERVICES
STEPS4 = [('01', 'Diagnostic Discovery', 'Before we recommend anything, we audit your current marketing, search landscape, intake pipeline and competitors. No assumptions.'),
          ('02', 'Strategy Blueprint', 'A multi-channel plan with clear priorities, channel mix, budget allocation and KPIs — all tied to intake volume and case growth.'),
          ('03', 'AI-Powered Execution', 'We launch and manage every channel using AI tools to accelerate performance — while experienced strategists maintain oversight and judgment.'),
          ('04', 'Measure & Scale', 'Clear reporting against real business goals — cases, intake, search share. We don’t set and forget. Ever.')]
HUB_FAQ = [('How is your legal marketing agency different from other legal marketing firms?', 'Most legal marketing firms focus on one channel and run generic campaigns. We operate as a full-channel legal marketing agency — every channel works together under one strategy built for your firm. We report on intake volume and signed clients, not traffic and clicks.'),
           ('How quickly will I see results?', 'Paid search (Google Ads, LSA) can produce intake leads within the first few weeks. SEO, AI search optimization and reputation building compound over 3–6 months or longer, depending on your market.'),
           ('What if I already have a marketing team or agency?', 'No problem. We work as an extension of your team, integrate with existing vendors, or audit what’s working before making recommendations.'),
           ('How do you ensure lead quality, not just lead volume?', 'We target high-intent, case-specific searches and audiences. Your feedback on the cases coming through is what helps us continuously refine targeting, messaging and strategy.'),
           ('Do you work with firms of all sizes?', 'Yes — from solo practitioners building a first marketing foundation to multi-location firms competing for regional markets.')]

def steps_html(steps):
    return '<div class="steps">' + ''.join(f'<div class="step"><span class="step-n">{n}</span><h3>{e(t)}</h3><p>{e(b)}</p></div>' for n, t, b in steps) + '</div>'

def build_services_hub():
    cr = [('Home', '/'), ('Services', '/services/')]
    groups = ''
    for g in GROUPS:
        items = [s for s in SERVICES if s['group'] == g]
        groups += f'<div class="stack-sm"><h2 class="h2-md" style="font-size:26px">{e(g)}</h2>{cards([(s["name"], s["lede"].split(". ")[0]+".", "/"+s["slug"]+"/", "Explore") for s in items])}</div>'
    body = head_block(cr, 'Legal Marketing Services', 'Law Firm Marketing <em>Services.</em>', 'We deploy the channel mix your firm needs — not a generic package. Every tactic serves a defined role in moving a prospect from search to signed client.') + \
        f'<section class="wrap sec-bottom stack-xl">{groups}</section>' + \
        f'<section class="rule-top"><div class="wrap sec stack-lg"><h2 class="h2" style="max-width:900px">No Templates. No Generic Playbooks. <em>Just a Clear Path to Win Your Market.</em></h2>{steps_html(STEPS4)}</div></section>' + \
        calc('Calculate Your Law Firm <em>Marketing Budget.</em>', 'See what your firm should consider investing across all channels, based on revenue and growth goals.', 'services_hub', 'services_hub') + \
        faq_section(HUB_FAQ, 'Straight Answers to Hard <em>Questions.</em>', 'Attorneys don’t have time for runaround answers. Neither do we.')
    page('/services/', 'Law Firm Marketing Services | Legal Marketing Firm',
         'Law firm marketing services: SEO, local SEO, Google Ads, Local Services Ads, AI search optimization, web design, content, video, TV and intake optimization.',
         body, schema=[faq_schema(HUB_FAQ), {"@context": "https://schema.org", "@type": "ItemList", "name": "Law firm marketing services",
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s['name'], "url": SITE + '/' + s['slug'] + '/'} for i, s in enumerate(SERVICES)]}],
         crumbs=cr, ptype='services_hub', priority=0.9)

AI_STATS = [('900M', 'ChatGPT Weekly Users', 'Up from 300M in about 14 months', 'Source: OpenAI, Feb 2026', False),
            ('357%', 'Growth in AI Referral Traffic', 'June 2024 → June 2025', 'Source: SimilarWeb, 2025', False),
            ('14.2%', 'AI Search Conversion Rate', 'vs. 2.8% for Google — about 5×', 'Source: AI Search Statistics 2026', True),
            ('80%', 'of AI-cited pages don’t rank', 'in Google’s top 100', 'Source: Ahrefs, Aug 2025', False)]

def build_service(s):
    path = f'/{s["slug"]}/'
    cr = [('Home', '/'), ('Services', '/services/'), (s['name'], path)]
    deliv = ''.join(f'<div>{ic("check",20,"ic gold")}<div><h3>{e(t)}</h3><p>{e(b)}</p></div></div>' for t, b in s['deliv'])
    steps = steps_html([(f'0{i+1}', t, b) for i, (t, b) in enumerate(s['steps'])])
    kpis = ''.join(f'<li>{e(k)}</li>' for k in s['kpis'])
    prob = ''.join(f'<p>{e(p)}</p>' for p in s['problem'])
    ai_extra = ''
    if s['slug'] == 'law-firm-ai-search-optimization':
        stats = ''.join(f'<div class="aistat{" feat" if f else ""}"><span class="aistat-v" data-count="{v}">{v}</span><div class="aistat-txt"><span class="aistat-l">{e(l)}</span><span class="aistat-l2">{e(l2)}</span><span class="aistat-src">{e(src)}</span></div></div>' for v, l, l2, src, f in AI_STATS)
        ai_extra = f'''<section class="wrap sec-bottom"><div class="grid-cells aistats">{stats}</div></section>
<section class="band"><div class="wrap sec two-col"><div class="stack-sm" style="align-content:start"><span class="eyebrow">What Is GEO?</span><h2 class="h2-xl">If You’re Not in AI Search, You’re <em>Invisible to a Growing Share of Clients.</em></h2></div>
<div class="prose"><p>Generative engine optimization (GEO) is the practice of positioning your firm to be cited and recommended when AI tools answer legal questions. It’s different from traditional SEO — ranking #1 on Google doesn’t mean you appear in ChatGPT.</p>
<p>According to Ahrefs, most pages cited in AI answers don’t rank in Google’s top 100, so your current SEO investment offers limited protection in AI search.</p>
<p>The firms that build AI search presence now will be hard to displace. The ones that wait will be playing catch-up against competitors who are already being recommended by name.</p>
<blockquote class="quote" style="font-size:19px">AI can generate content. It can’t generate the judgment to know which direction is right for your firm, your market and your clients. That’s where our experience lives.</blockquote></div></div></section>'''
    sub_links = ''
    if s['slug'] in ('law-firm-ai-search-optimization', 'law-firm-geo', 'law-firm-aeo'):
        sub_links = ' · '.join(f'<a href="/{x}/">{e(SVC[x]["name"])}</a>' for x in ('law-firm-ai-search-optimization', 'law-firm-geo', 'law-firm-aeo') if x != s['slug'])
    combo_links = ''
    for cs, cname, cparent in COMBO_SERVICES:
        if cparent == s['slug']:
            combo_links = '<div class="stack-sm"><h3 class="h2-md" style="font-size:22px">By practice area</h3><div class="chips-links">' + ''.join(f'<a href="/practice-areas/{p}/{cs}/">{e(PRC[p]["name"])} {e(cname)}</a>' for p in COMBO_PRACTICES) + '</div></div>'
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<span class="eyebrow">Legal Marketing Services · {e(s["group"])}</span><h1 class="h1">{e(s["name"])}</h1><p class="lede" style="max-width:720px">{e(s["lede"])}</p>
<div class="btns" style="margin-top:8px"><a href="/free-marketing-audit/" class="btn btn-accent btn-lg">Get Your Free Marketing Audit {ARROW}</a><a href="/results/" class="btn btn-inverse btn-lg">See Real Results</a></div>{f'<p style="font-size:14px">Related: {sub_links}</p>' if sub_links else ''}</section>
{ai_extra}
<section class="band"><div class="wrap sec two-col"><div class="stack-sm" style="align-content:start"><span class="eyebrow">The Problem</span><h2 class="h2">Why {e(s["short"])} Underperforms for <em>Most Firms.</em></h2></div><div class="prose">{prob}</div></div></section>
<section class="wrap sec stack-lg"><div class="stack-sm"><span class="eyebrow">Deliverables</span><h2 class="h2">What You <em>Get.</em></h2></div><div class="deliv">{deliv}</div></section>
<section class="rule-top"><div class="wrap sec stack-lg"><div class="stack-sm"><span class="eyebrow">Process</span><h2 class="h2">How It <em>Works.</em></h2></div>{steps}</div></section>
<section class="band"><div class="wrap sec two-col"><div class="stack-sm" style="align-content:start"><span class="eyebrow">Measurement</span><h2 class="h2">What We <em>Report On.</em></h2><p class="body-lg">Every report connects activity to inquiries and, where your intake data allows, to signed cases.</p></div><div class="prose-lg"><ul>{kpis}</ul></div></div></section>
{proof_block(s["proof"]).replace('class="wrap sec-bottom"','class="wrap sec"')}
{calc('Calculate Your Law Firm <em>Marketing Budget.</em>', f'Planning {e(s["short"])} alongside your other channels? Start with a total budget recommendation based on your revenue and growth goals.', 'service', 'service_'+s['slug'].replace('-','_'))}
{faq_section(s["faqs"], f'{e(s["short"])} <em>Questions.</em>')}
<section class="wrap sec stack-lg"><div class="stack-sm"><span class="eyebrow">Related</span><h2 class="h2">Works Best <em>Together.</em></h2></div>
{cards([svc_card(x) for x in s["rel_s"]])}
<div class="stack-sm"><h3 class="h2-md" style="font-size:22px">For your practice</h3><div class="chips-links">{''.join(f'<a href="/practice-areas/{p}/">{e(PRC[p]["name"])} marketing</a>' for p in s["rel_p"])}<a href="/practice-areas/">All practice areas</a></div></div>
{combo_links}
<div class="stack-sm"><h3 class="h2-md" style="font-size:22px">In your market</h3><div class="chips-links">{''.join(f'<a href="/markets/{STATES[a][1]}/">{e(STATES[a][0])}</a>' for a in INITIAL_HUBS)}<a href="/markets/">All markets</a></div></div>
</section>'''
    schema = [{"@context": "https://schema.org", "@type": "Service", "name": s['name'], "serviceType": s['name'], "description": s['desc'],
               "provider": {"@id": ORG_ID}, "areaServed": {"@type": "Country", "name": "United States"}, "audience": {"@type": "BusinessAudience", "audienceType": "Law firms"}, "url": SITE + path},
              faq_schema(s['faqs'])]
    page(path, f'{s["name"]} | Legal Marketing Firm', s['desc'], body, schema=schema, crumbs=cr, ptype='service', priority=0.8)

# ================================================================== PRACTICES
def build_practice_hub():
    cr = [('Home', '/'), ('Practice Areas', '/practice-areas/')]
    body = head_block(cr, 'Marketing by Practice Area', 'Legal Marketing by <em>Practice Area.</em>', 'Every practice has its own client journey, competition and advertising rules. We build strategy around yours.') + \
        f'<section class="wrap sec-bottom">{cards([(p["name"], p["intro"].split(". ")[0]+".", "/practice-areas/"+p["slug"]+"/", "Explore") for p in PRACTICES])}</section>' + \
        calc('How Much Should Your Firm Invest in <em>Marketing?</em>', 'Budget needs vary by practice and market. Start with a recommendation based on your revenue and growth goals.', 'practice_hub', 'practice_hub')
    page('/practice-areas/', 'Law Firm Marketing by Practice Area | Legal Marketing Firm',
         'Marketing strategies for personal injury, workers compensation, family law, criminal defense, employment law, estate planning, immigration and more.',
         body, crumbs=cr, ptype='practice_hub', priority=0.9)

def build_practice(p):
    path = f'/practice-areas/{p["slug"]}/'
    cr = [('Home', '/'), ('Practice Areas', '/practice-areas/'), (p['name'], path)]
    ch = [(SVC[sl]['name'], why, f'/{sl}/', 'Explore') for sl, why in p['channels']]
    combos = ''
    if p['slug'] in COMBO_PRACTICES:
        combos = f'<section class="wrap sec-bottom stack-sm"><h2 class="h2-md">{e(p["name"])} Marketing <em>Services.</em></h2>' + cards([(f'{p["name"]} Law Firm {cn}', COMBO[(p["slug"], cs)][0].split(". ")[0] + '.', f'{path}{cs}/', 'Explore') for cs, cn, _ in COMBO_SERVICES]) + '</section>'
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<span class="eyebrow">Practice Area Marketing</span><h1 class="h1">Marketing for {e(p["name"])} <em>Law Firms.</em></h1><p class="lede" style="max-width:720px">{e(p["intro"])}</p>
<div class="btns" style="margin-top:8px"><a href="/free-marketing-audit/" class="btn btn-accent btn-lg">Get Your Free Marketing Audit {ARROW}</a></div></section>
<section class="band"><div class="wrap sec two-col"><div class="stack-sm" style="align-content:start"><span class="eyebrow">Client Acquisition</span><h2 class="h2">How {e(p["name"])} Clients <em>Search.</em></h2></div><div class="prose"><p>{e(p["search"])}</p></div></div></section>
<section class="wrap sec stack-lg"><div class="stack-sm"><span class="eyebrow">Recommended Channels</span><h2 class="h2">Where {e(p["name"])} Firms <em>Win.</em></h2></div>{cards(ch)}</section>
{combos}
<section class="band"><div class="wrap sec"><div class="grid-cells geo">
<div class="geo-pillar"><span class="geo-n">01</span><div><h3>Competition</h3><p>{e(p["competition"])}</p></div></div>
<div class="geo-pillar"><span class="geo-n">02</span><div><h3>Intake</h3><p>{e(p["intake"])}</p></div></div>
<div class="geo-pillar"><span class="geo-n">03</span><div><h3>Advertising considerations</h3><p>{e(p["ads"])} This is general information, not legal advice; review your jurisdiction’s rules with qualified counsel.</p></div></div>
<div class="geo-pillar"><span class="geo-n">04</span><div><h3>Measurement</h3><p>We track every inquiry to its source and report on qualified leads and signed cases, so budget moves toward what works for your {e(p["firms"].replace(" firms",""))} practice.</p></div></div>
</div></div></section>
{calc(f'How Much Should {e(p["name"])} Firms Invest in <em>Marketing?</em>', f'Get a recommended monthly and annual marketing budget for your {e(p["name"].lower())} practice based on revenue and growth goals.', 'practice', 'practice_'+p['slug'].replace('-','_'), practice=p['name'])}
{faq_section(p["faqs"], f'{e(p["name"])} Marketing <em>Questions.</em>')}
<section class="wrap sec stack-sm"><span class="eyebrow">Explore</span><div class="chips-links"><a href="/results/">Case study</a><a href="/markets/">Markets we serve</a><a href="/services/">All services</a>{''.join(f'<a href="/practice-areas/{o["slug"]}/">{e(o["name"])}</a>' for o in PRACTICES if o["slug"]!=p["slug"])}</div></section>'''
    page(path, f'{p["name"]} Law Firm Marketing | Legal Marketing Firm',
         f'Marketing for {p["firms"]}: client acquisition, the right channels, competition, intake and advertising considerations. Get a free marketing audit.',
         body, schema=[faq_schema(p['faqs'])], crumbs=cr, ptype='practice', practice=p['name'], priority=0.8)

def build_combo(pslug, cs, cname, parent):
    p, s = PRC[pslug], SVC[parent]
    search, structure, conv, comp = COMBO[(pslug, cs)]
    path = f'/practice-areas/{pslug}/{cs}/'
    name = f'{p["name"]} Law Firm {cname}'
    cr = [('Home', '/'), ('Practice Areas', '/practice-areas/'), (p['name'], f'/practice-areas/{pslug}/'), (cname, path)]
    deliv = ''.join(f'<div>{ic("check",20,"ic gold")}<div><h3>{e(t)}</h3><p>{e(b)}</p></div></div>' for t, b in s['deliv'][:4])
    others = [(f'{p["name"]} {cn}', f'/practice-areas/{pslug}/{c2}/') for c2, cn, _ in COMBO_SERVICES if c2 != cs] + \
             [(f'{PRC[o]["name"]} {cname}', f'/practice-areas/{o}/{cs}/') for o in COMBO_PRACTICES if o != pslug]
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<span class="eyebrow">{e(p["name"])} · {e(cname)}</span><h1 class="h1">{e(name)}</h1><p class="lede" style="max-width:720px">{e(search)}</p>
<div class="btns" style="margin-top:8px"><a href="/free-marketing-audit/" class="btn btn-accent btn-lg">Get Your Free Marketing Audit {ARROW}</a></div></section>
<section class="band"><div class="wrap sec"><div class="grid-cells geo">
<div class="geo-pillar"><span class="geo-n">01</span><div><h3>Campaign structure</h3><p>{e(structure)}</p></div></div>
<div class="geo-pillar"><span class="geo-n">02</span><div><h3>Conversion path</h3><p>{e(conv)}</p></div></div>
<div class="geo-pillar"><span class="geo-n">03</span><div><h3>Compliance considerations</h3><p>{e(comp)} General information only; confirm requirements for your jurisdiction with qualified counsel.</p></div></div>
<div class="geo-pillar"><span class="geo-n">04</span><div><h3>Measurement</h3><p>{e(s["kpis"][0])}, {e(s["kpis"][1].lower())} and {e(s["kpis"][2].lower())} — reported monthly and tied to your intake outcomes.</p></div></div>
</div></div></section>
<section class="wrap sec stack-lg"><div class="stack-sm"><span class="eyebrow">Core deliverables</span><h2 class="h2">What’s <em>Included.</em></h2><p class="body-lg">The {e(s["name"])} foundation, tailored to {e(p["firms"])}. <a href="/{parent}/">See the full {e(s["name"])} service</a>.</p></div><div class="deliv">{deliv}</div></section>
{proof_block(s["proof"])}
{calc(f'Plan Your {e(p["name"])} <em>Marketing Budget.</em>', f'Before scaling {e(cname)}, set a total budget that matches your growth goal.', 'practice_service', f'combo_{pslug}_{cs}'.replace('-','_'), practice=p['name'])}
<section class="wrap sec stack-sm"><span class="eyebrow">Related</span><div class="chips-links"><a href="/practice-areas/{pslug}/">{e(p["name"])} marketing</a><a href="/{parent}/">{e(s["name"])}</a>{''.join(f'<a href="{h}">{e(t)}</a>' for t, h in others)}</div></section>'''
    schema = [{"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": s['name'], "provider": {"@id": ORG_ID},
               "audience": {"@type": "BusinessAudience", "audienceType": p['name'] + ' law firms'}, "areaServed": {"@type": "Country", "name": "United States"}, "url": SITE + path}]
    page(path, f'{name} | Legal Marketing Firm', f'{name}: specialty-specific search behavior, campaign structure, conversion path and compliance considerations for {p["firms"]}.',
         body, schema=schema, crumbs=cr, ptype='practice_service', practice=p['name'], priority=0.7)

# ================================================================== MARKETS
TIER_COPY = {
 'major': ('a major metro legal market', 'Competition here is intense: national advertisers, large firms and specialized agencies bid on the same searches, and paid search costs reflect it. Firms win by narrowing focus — specific case types, neighborhoods and languages — and by building AI search visibility before competitors do.',
           'In a market this competitive, efficiency matters more than volume. Tight paid search structure, strong reviews, specialized content and fast intake usually outperform simply spending more.'),
 'mid': ('a mid-size legal market', 'Mid-size markets often have a handful of heavy advertisers and many firms with underbuilt digital presence. That gap is the opportunity: a firm with strong local SEO, steady reviews and answer content can climb quickly.',
         'Local SEO, Local Services Ads and targeted Google Ads usually lead, supported by practice content that answers local questions and positions your firm for AI search.'),
 'small': ('a smaller legal market', 'Smaller markets are where focused firms can lead. Search and AI visibility competition is often light, paid search costs are lower, and a strong Google Business Profile plus a steady stream of reviews can put a firm on top of the map.',
           'A strong local foundation — profile, reviews, fast website, clear practice pages — plus Local Services Ads or a lean Google Ads campaign often delivers the best return. TV and radio can be surprisingly affordable here, too.'),
}
SCORE_METRICS = [('Search visibility', 'Local organic and map-pack visibility for priority legal searches'), ('AI citations', 'How often AI assistants mention local firms for legal prompts'),
                 ('Review benchmarks', 'Review counts, ratings and recency among leading firms'), ('Website performance', 'Speed, mobile experience and conversion paths'),
                 ('Paid search competition', 'Advertiser density on high-intent legal terms'), ('Social presence', 'Active, credible social profiles among local firms')]

def build_markets_hub():
    cr = [('Home', '/'), ('Markets', '/markets/')]
    blocks = ''
    for ab in sorted(STATES, key=lambda a: STATES[a][0]):
        nm, sl, _ = STATES[ab]
        cs = [c for c in CITIES if c['st'] == ab]
        blocks += f'<div class="state-block"><h3><a href="/markets/{sl}/">{e(nm)}</a> <span class="mono-k" style="margin-left:8px">{len(cs)} market{"s" if len(cs)!=1 else ""}</span></h3><div class="chips-links">{"".join(f"<a href=\"{market_city_url(c)}\">{e(c['name'])}</a>" for c in cs)}</div></div>'
    pri = ''.join(f'<a href="{market_city_url(c)}">{e(c["name"])}, {c["st"]}</a>' for c in CITIES if c['pri'] == 'priority')
    body = head_block(cr, 'Markets · Legal Marketing Agency by City', 'Legal Marketing Agency <em>by City.</em>',
        'We help law firms across the country win search, AI and paid visibility in their markets — from major metros to the smaller cities where a focused firm can lead. We work remotely with firms in every market listed; we don’t claim local offices.') + \
        f'''<section class="wrap sec-bottom stack-lg"><div class="stack-sm"><span class="eyebrow">Smaller-market priorities</span><h2 class="h2">Where Focused Firms Can <em>Lead.</em></h2><p class="body-lg" style="max-width:760px">In many smaller and mid-size markets, competition for search and AI visibility is lighter and costs are lower. These are the markets we’re prioritizing first.</p></div><div class="chips-links">{pri}</div></section>
<section class="band"><div class="wrap sec two-col"><div class="stack-sm" style="align-content:start"><span class="eyebrow">How we prioritize markets</span><h2 class="h2">Opportunity <em>Scoring.</em></h2><p class="body-lg">We weigh six factors when deciding where to invest in local research and content.</p></div>
<div class="prose-lg"><div class="table-wrap"><table><tr><th>Factor</th><th>Weight</th></tr><tr><td>SEO competition</td><td>30%</td></tr><tr><td>Prospective law firms</td><td>25%</td></tr><tr><td>Search demand</td><td>15%</td></tr><tr><td>Specialized agency competition</td><td>15%</td></tr><tr><td>Metro population</td><td>10%</td></tr><tr><td>Relationships / proof</td><td>5%</td></tr></table></div><p style="font-size:14px;color:var(--navy-300)">Local scoreboards are published only after we measure them.</p></div></div></section>
<section class="wrap sec stack-sm"><span class="eyebrow">All markets by state</span><h2 class="h2">{len(CITIES)} Markets in {len(STATES)} <em>States.</em></h2>{blocks}</section>''' + \
        calc('Calculate Your Law Firm <em>Marketing Budget.</em>', 'Wherever you practice, start with a budget recommendation based on your revenue and growth goals.', 'markets_hub', 'markets_hub')
    page('/markets/', 'Legal Marketing Agency by City | Legal Marketing Firm',
         f'Law firm marketing in {len(CITIES)} U.S. markets across {len(STATES)} states — SEO, Google Ads, AI search optimization and more for firms in major metros and smaller cities.',
         body, crumbs=cr, ptype='markets_hub', priority=0.9)

def build_state(ab):
    nm, sl, blurb = STATES[ab]
    path = f'/markets/{sl}/'
    cr = [('Home', '/'), ('Markets', '/markets/'), (nm, path)]
    cs = [c for c in CITIES if c['st'] == ab]
    groups = ''
    for t, label in (('major', 'Major metro markets'), ('mid', 'Mid-size markets'), ('small', 'Smaller markets')):
        g = [c for c in cs if c['tier'] == t]
        if g: groups += f'<div class="stack-sm"><h3 class="h2-md" style="font-size:22px">{label}</h3><div class="chips-links">{"".join(f"<a href=\"{market_city_url(c)}\">{e(c['name'])}</a>" for c in g)}</div></div>'
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<span class="eyebrow">Markets · {e(nm)}</span><h1 class="h1">Law Firm Marketing in <em>{e(nm)}.</em></h1><p class="lede" style="max-width:720px">{e(blurb)}</p>
<div class="btns" style="margin-top:8px"><a href="/free-marketing-audit/" class="btn btn-accent btn-lg">Get Your Free Marketing Audit {ARROW}</a></div></section>
<section class="band"><div class="wrap sec stack-lg"><div class="stack-sm"><span class="eyebrow">Regional market directory</span><h2 class="h2">{e(nm)} <em>Markets.</em></h2></div>{groups}</div></section>
<section class="wrap sec two-col"><div class="stack-sm" style="align-content:start"><span class="eyebrow">Statewide trends</span><h2 class="h2">What’s Changing for {e(nm)} <em>Firms.</em></h2></div>
<div class="prose"><p>Across {e(nm)}, as everywhere, more prospects are starting their search with AI assistants, the map pack is decisive for “near me” searches, and reviews influence both. Firms that keep their information consistent, publish clear answers about {e(nm)} law and respond fast to every inquiry are best positioned.</p>
<p><strong>Advertising rules.</strong> Lawyer advertising in {e(nm)} is governed by state rules of professional conduct and bar guidance, which can differ from other states on testimonials, case results, disclaimers and specialization claims. Review current {e(nm)} requirements with qualified counsel before launching campaigns. This page is general information, not legal advice.</p></div></section>
<section class="band"><div class="wrap sec stack-lg"><div class="stack-sm"><span class="eyebrow">Services</span><h2 class="h2">How We Help {e(nm)} <em>Law Firms.</em></h2></div>
{cards([svc_card(x) for x in ['law-firm-seo','law-firm-local-seo','law-firm-google-ads','law-firm-local-services-ads','law-firm-ai-search-optimization','law-firm-intake-optimization']])}
<div class="chips-links">{''.join(f'<a href="/practice-areas/{p["slug"]}/">{e(p["name"])}</a>' for p in PRACTICES[:8])}</div></div></section>
{calc(f'Plan Your {e(nm)} Law Firm <em>Marketing Investment.</em>', f'Get a recommended monthly and annual budget for your {e(nm)} firm based on revenue and growth goals.', 'state', 'state_'+sl.replace('-','_'), market=nm, state=ab)}'''
    page(path, f'{nm} Law Firm Marketing Agency | Legal Marketing Firm',
         f'Law firm marketing in {nm}: SEO, Google Ads, AI search optimization and more for firms in {", ".join(c["name"] for c in cs[:4])}{" and more" if len(cs)>4 else ""}.',
         body, crumbs=cr, ptype='state', market=nm, priority=0.7 if ab in INITIAL_HUBS else 0.6)

ROCKFORD_SUBS = [('seo', 'SEO', 'law-firm-seo'), ('ppc', 'PPC', 'law-firm-ppc'), ('web-design', 'Web Design', 'law-firm-web-design'),
                 ('ai-search', 'AI Search', 'law-firm-ai-search-optimization'), ('personal-injury-marketing', 'Personal Injury Marketing', None)]

def build_city(c):
    nm, sl, _ = STATES[c['st']]
    path = market_city_url(c)
    city = c['name']
    cr = [('Home', '/'), ('Markets', '/markets/'), (nm, f'/markets/{sl}/'), (city, path)]
    tier_label, overview, works = TIER_COPY[c['tier']]
    nearby = [x for x in CITIES if x['st'] == c['st'] and x['slug'] != c['slug']]
    score = ''.join(f'<div><span class="mono-label">{e(t)}</span><span class="pend">Audit pending</span><span style="font-size:13px;color:var(--navy-300)">{e(d)}</span></div>' for t, d in SCORE_METRICS)
    faqs = [(f'How much does law firm marketing cost in {city}?', f'It depends on your practice area, competition and goals. Our framework recommends 5% to 25% of annual revenue depending on your growth objective; use the calculator on this page for a personalized figure for your {city} firm.'),
            (f'Do you have an office in {city}?', f'No. We work with law firms in {city} and across {nm} remotely, with regular strategy calls and reporting. We never create fake local listings for our clients either.'),
            (f'What marketing works best for {city} law firms?', works),
            (f'Can {city} law firms show up in ChatGPT and AI search?', 'Yes. Consistent firm information, steady reviews, clear answer content and credible mentions all improve the odds that AI assistants mention your firm. We track a set of local prompts to measure progress; no one can guarantee placement.')]
    subs = ''
    if c['slug'] == 'rockford' and c['st'] == 'IL':
        subs = f'<section class="wrap sec-bottom stack-sm"><span class="eyebrow">Rockford services</span><h2 class="h2-md">Rockford Law Firm <em>Marketing Services.</em></h2>' + cards([(f'Rockford Law Firm {t}', '', f'{path}{s}/', 'Explore') for s, t, _ in ROCKFORD_SUBS]) + '</section>'
    if c['slug'] == 'rockford' and c['st'] == 'IL':
        ch, ci = 'How Much Should Your Rockford Law Firm Spend on <em>Marketing?</em>', 'Whether your firm is maintaining its presence in the Rockford area or expanding into surrounding markets, use our calculator to estimate a marketing budget aligned with your growth goals.'
    else:
        ch, ci = f'Calculate Your {e(city)} Law Firm <em>Marketing Budget.</em>', f'Get a recommended monthly and annual marketing budget for your {e(city)} firm based on revenue and growth goals.'
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<span class="eyebrow">Markets · {e(city)}, {c["st"]}</span><h1 class="h1">Law Firm Marketing in <em>{e(city)}, {e(nm)}.</em></h1>
<p class="lede" style="max-width:720px">SEO, Google Ads, AI search optimization and integrated advertising for {e(city)} law firms — built to drive cases, not just clicks.</p>
<div class="btns" style="margin-top:8px"><a href="/free-marketing-audit/" class="btn btn-accent btn-lg">Get Your Free {e(city)} Marketing Audit {ARROW}</a><a href="/markets/{sl}/" class="btn btn-inverse btn-lg">{e(nm)} Markets</a></div></section>
<section class="band"><div class="wrap sec two-col"><div class="stack-sm" style="align-content:start"><span class="eyebrow">Local market overview</span><h2 class="h2">The {e(city)} Legal <em>Market.</em></h2></div>
<div class="prose"><p>We treat {e(city)} as {tier_label}. {e(overview)}</p><p>{e(STATES[c["st"]][2])}</p>{f'<p>Nearby {e(nm)} markets: ' + ', '.join(f'<a href="{market_city_url(x)}">{e(x["name"])}</a>' for x in nearby[:8]) + '.</p>' if nearby else ''}</div></div></section>
<section class="wrap sec stack-lg"><div class="row-between end"><div class="stack-sm"><span class="eyebrow">{e(city)} Local Legal Marketing Scoreboard</span><h2 class="h2">How {e(city)} Firms <em>Measure Up.</em></h2></div><a href="/free-marketing-audit/" class="textlink">Request your {e(city)} scoreboard {ic("arrow-right",16)}</a></div>
<div class="grid-cells score-pending">{score}</div>
<p class="note-box">We publish local scores only after we measure them. Our {e(city)} benchmark of law firm search visibility, AI citations, reviews, website performance, paid search competition and social presence is in progress. Want your firm’s numbers first? <a href="/free-marketing-audit/">Request a free audit.</a></p></section>
{calc(ch, ci, 'city', 'city_'+c['slug'].replace('-','_'), market=f'{city}, {c["st"]}', city=city, state=c['st'])}
<section class="band"><div class="wrap sec stack-lg"><div class="stack-sm"><span class="eyebrow">Services</span><h2 class="h2">What We Do for {e(city)} <em>Firms.</em></h2></div>
{cards([svc_card(x) for x in ['law-firm-local-seo','law-firm-google-ads','law-firm-ai-search-optimization','law-firm-local-services-ads','law-firm-seo','law-firm-intake-optimization']])}</div></section>
{subs}
<section class="wrap sec stack-sm"><span class="eyebrow">Practice specialties</span><h2 class="h2-md">Marketing for {e(city)} <em>Practices.</em></h2><div class="chips-links">{''.join(f'<a href="/practice-areas/{p["slug"]}/">{e(p["name"])}</a>' for p in PRACTICES[:10])}</div></section>
{proof_block("intake")}
{faq_section(faqs, f'{e(city)} Law Firm Marketing <em>Questions.</em>')}'''
    from collections import Counter
    dupe = Counter(x['name'] for x in CITIES)[city] > 1 or city in [v[0] for v in STATES.values()]
    tcity = 'New York City' if (city == 'New York' and c['st'] == 'NY') else (f'{city}, {c["st"]}' if dupe else city)
    page(path, f'{tcity} Law Firm Marketing Agency | Legal Marketing Firm',
         f'{city} legal marketing agency: law firm SEO, attorney advertising, lawyer marketing and AI search optimization for {city}, {c["st"]} firms. Free marketing audit.',
         body, schema=[faq_schema(faqs)], crumbs=cr, ptype='city', market=f'{city}, {c["st"]}', priority=0.6 if c['pri'] else 0.5)

def build_rockford_sub(sub, title, parent):
    c = next(x for x in CITIES if x['slug'] == 'rockford' and x['st'] == 'IL')
    base = market_city_url(c)
    path = f'{base}{sub}/'
    name = f'Rockford Law Firm {title}'
    cr = [('Home', '/'), ('Markets', '/markets/'), ('Illinois', '/markets/illinois/'), ('Rockford', base), (title, path)]
    if parent:
        s = SVC[parent]
        intro = f'{s["lede"]} Rockford is a market where a focused firm can lead: competition for search and AI visibility is often lighter, and paid search costs lower, than in Chicago.'
        deliv = ''.join(f'<div>{ic("check",20,"ic gold")}<div><h3>{e(t)}</h3><p>{e(b)}</p></div></div>' for t, b in s['deliv'][:4])
        mid = f'<section class="wrap sec stack-lg"><div class="stack-sm"><span class="eyebrow">Deliverables</span><h2 class="h2">What’s <em>Included.</em></h2><p class="body-lg"><a href="/{parent}/">See the full {e(s["name"])} service</a>.</p></div><div class="deliv">{deliv}</div></section>'
        practice = ''
    else:
        p = PRC['personal-injury']
        intro = f'{p["intro"]} In Rockford, focused PI firms can win the map pack, capture urgent searches efficiently and build AI visibility before larger competitors arrive.'
        mid = f'<section class="wrap sec stack-lg"><div class="stack-sm"><span class="eyebrow">Recommended channels</span><h2 class="h2">Where Rockford PI Firms <em>Win.</em></h2></div>{cards([(SVC[sl]["name"], why, "/"+sl+"/", "Explore") for sl, why in p["channels"]])}</section>'
        practice = 'Personal Injury'
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<span class="eyebrow">Markets · Rockford, IL</span><h1 class="h1">{e(name)}</h1><p class="lede" style="max-width:720px">{e(intro)}</p>
<div class="btns" style="margin-top:8px"><a href="/free-marketing-audit/" class="btn btn-accent btn-lg">Get Your Free Rockford Marketing Audit {ARROW}</a><a href="{base}" class="btn btn-inverse btn-lg">Rockford Overview</a></div></section>
{mid}
{calc('How Much Should Your Rockford Law Firm Spend on <em>Marketing?</em>', 'Whether your firm is maintaining its presence in the Rockford area or expanding into surrounding markets, use our calculator to estimate a marketing budget aligned with your growth goals.', 'city_service', 'rockford_'+sub.replace('-','_'), market='Rockford, IL', practice=practice, city='Rockford', state='IL')}
<section class="wrap sec stack-sm"><span class="eyebrow">More for Rockford firms</span><div class="chips-links">{''.join(f'<a href="{base}{s2}/">Rockford {e(t2)}</a>' for s2, t2, _ in ROCKFORD_SUBS if s2 != sub)}<a href="{base}">Rockford overview</a><a href="/markets/illinois/">Illinois markets</a></div></section>'''
    page(path, f'{name} | Legal Marketing Firm', f'{name}: {title.lower()} for Rockford, Illinois law firms, built to drive qualified intake. Free marketing audit.',
         body, crumbs=cr, ptype='city_service', market='Rockford, IL', practice=practice, priority=0.5)

# ================================================================== RESULTS
def build_results():
    cr = [('Home', '/'), ('Results', '/results/')]
    bars = ''
    for lbl, long, v, n in sorted(SCORE, key=lambda x: -x[3]):
        feat = lbl == 'Client Intake Forms'
        bars += f'<div class="bar-row{" feat" if feat else ""}"><div class="bar-head"><span>{e(long)}</span><span class="bar-v" data-count="{v}">{v}</span></div><div class="bar-track"><div class="bar" style="--w:{n/220*100:.1f}%"></div></div></div>'
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<span class="eyebrow">Client Results · Full Scoreboard</span><h1 class="h1">We Don’t Talk About Results. <em>We Show Them.</em></h1><p class="lede" style="max-width:640px">Every metric below comes from a real law firm engagement. No projections, no industry averages, no cherry-picked click data.</p></section>
<section class="wrap results-sec"><div class="results">
<div class="results-feat"><span class="mono-label dark">The #1 Result That Matters · Client Intake Form Completions</span><span class="results-feat-num" data-count="+50%">+50%</span><p>More prospects completing the firm’s intake form — the leading indicator of new signed cases, and the number we’re here to move.</p></div>
<div class="results-bars"><span class="mono-label">Every Metric Moved</span>{bars}</div></div></section>
<section class="band"><div class="wrap sec two-col">
<div class="stack-md" style="justify-items:start;align-content:start"><span class="badge">Law Firm · Multi-Channel Strategy</span><h2 class="h2-md">Full-Channel <em>Law Firm Engagement.</em></h2>
<p class="body-lg">This firm had a solid reputation and strong attorneys — but weak digital visibility, inconsistent intake and marketing spend that wasn’t producing measurable ROI.</p>
<p class="body-lg">We built a unified legal marketing strategy: SEO, paid search, social media, review generation, content development and AI-powered production working together.</p>
<a href="/results/law-firm-marketing-case-study/" class="btn btn-inverse btn-md">Read the Full Case Study {ARROW}</a></div>
<div class="facts"><div class="fact"><span class="mono-k">Channels Deployed</span><p>SEO, Google Ads, Local Services Ads, Google Reviews, Social Media, Content &amp; Video, Email Nurture</p></div>
<div class="fact"><span class="mono-k">The #1 Result That Matters</span><p>+50% client intake form completions. Intake forms are inquiries, not signed cases; they’re the leading indicator we track toward new clients.</p></div>
<div class="fact"><span class="mono-k">How We Got There</span><p>Unified strategy across every channel, AI-accelerated content production and systematic review generation — all tied to intake outcomes, not vanity metrics.</p></div></div>
</div></section>
{calc('Is Your Firm Investing Enough to <em>Get Results Like These?</em>', 'See what your firm should consider investing in marketing, based on revenue and growth goals.', 'results', 'results')}'''
    page('/results/', 'Legal Marketing Case Studies & Results | Legal Marketing Firm',
         'Real law firm marketing results: +50% client intake form completions, +220% search visibility, +90% web traffic from a full-channel engagement.',
         body, crumbs=cr, ptype='results', priority=0.8)

def build_case_study():
    path = '/results/law-firm-marketing-case-study/'
    cr = [('Home', '/'), ('Results', '/results/'), ('Case Study', path)]
    rows = ''.join(f'<tr><td>{e(long)}</td><td><strong style="color:var(--gold-400)">{v}</strong></td></tr>' for lbl, long, v, n in SCORE)
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<span class="eyebrow">Case Study · Multi-Channel Law Firm Engagement</span><h1 class="h1">Law Firm Marketing <em>Case Study.</em></h1><p class="lede" style="max-width:720px">How a unified, full-channel strategy produced +50% client intake form completions and +220% search visibility for a law firm with a strong reputation and underbuilt digital presence.</p></section>
<section class="wrap sec-bottom"><div class="layout-2"><div class="prose-lg">
<h2 class="mt-0">The situation</h2><p>The firm had experienced attorneys and good client relationships, but its digital visibility lagged competitors, intake was inconsistent and marketing spend was difficult to tie to results.</p>
<h2>What we did</h2><ul><li><strong>SEO:</strong> technical fixes, rebuilt practice pages and answer content.</li><li><strong>Paid search:</strong> restructured Google Ads, added Local Services Ads and conversion tracking.</li><li><strong>Reviews:</strong> a consistent, compliant review request process.</li><li><strong>Social and video:</strong> attorney-led content and paid amplification.</li><li><strong>Email nurture:</strong> follow-up for unbooked inquiries.</li><li><strong>AI-accelerated production:</strong> faster research and content, with expert review on every piece.</li></ul>
<h2>Results</h2><div class="table-wrap"><table><tr><th>Metric</th><th>Change</th></tr>{rows}</table></div>
<h2>Methodology</h2><p>Metrics compare a defined period after launch with the firm’s prior baseline, using the firm’s analytics, ad platform, review and social data. “Search visibility” combines Google ranking visibility and observed AI search appearances. “Paid search performance” reflects conversion results from paid search. Intake form completions are inquiries, not signed cases.</p>
<p class="note-box">These are marketing metrics from one engagement, not case outcomes, and not a promise of similar results. The client’s name is withheld for confidentiality; details are shared with permission.</p>
</div>
<aside class="aside"><div class="aside-box"><h3>Want a scoreboard like this?</h3><p>Start with a free audit of your firm’s search, paid and AI visibility.</p><a href="/free-marketing-audit/" class="btn btn-accent btn-md">Get Your Free Audit</a></div>
<div class="aside-box"><h3>Services used</h3><ul>{''.join(f'<li><a href="/{x}/">{e(SVC[x]["name"])}</a></li>' for x in ['law-firm-seo','law-firm-google-ads','law-firm-local-services-ads','law-firm-reputation-management','law-firm-social-media','law-firm-email-marketing'])}</ul></div></aside>
</div></section>
{calc('Plan Your Firm’s <em>Marketing Budget.</em>', 'See what your firm should consider investing, based on revenue and growth goals.', 'case_study', 'case_study')}'''
    schema = [{"@context": "https://schema.org", "@type": "Article", "headline": "Law Firm Marketing Case Study: +50% Client Intake Form Completions, +220% Search Visibility",
               "author": {"@id": SITE + "/about/#matt-hensler"}, "publisher": {"@id": ORG_ID}, "dateModified": REVIEWED, "mainEntityOfPage": SITE + path}]
    page(path, 'Law Firm Marketing Case Study | Legal Marketing Firm', 'A full-channel law firm marketing case study: +50% intake form completions, +220% search visibility, +90% traffic. Channels, approach and methodology.',
         body, schema=schema, crumbs=cr, ptype='case_study', priority=0.7, og_type='article')

# ================================================================== INSIGHTS
def byline():
    return f'<div class="byline"><span>By <a href="/about/"><strong>{AUTHOR}</strong></a>, {AUTHOR_ROLE}</span><span>Reviewed {date.fromisoformat(REVIEWED).strftime("%B %-d, %Y")}</span></div>'

def build_insights_hub():
    cr = [('Home', '/'), ('Insights', '/insights/')]
    body = head_block(cr, 'Insights · Research, Guides & Answers', 'Law Firm Marketing <em>Insights.</em>', 'Straight answers to the questions law firm owners ask about budgets, search, AI visibility, intake and growth — reviewed by our strategy team.') + \
        f'''<section class="wrap sec-bottom stack-lg"><h2 class="h2-md">Answers</h2>{cards([(a["title"], a["answer"][:140].rsplit(" ",1)[0]+"…", f"/insights/{a['slug']}/", a["tag"]) for a in ARTICLES])}</section>
<section class="band"><div class="wrap sec stack-lg"><div class="stack-sm"><h2 class="h2-md">Research &amp; Guides</h2><p class="body-lg">We publish data only after we’ve measured it, with methodology and limitations disclosed.</p></div>{cards([(r["title"], r["what"], f"/insights/{r['slug']}/", "Guide" if r.get("guide") else "Methodology") for r in RESEARCH])}</div></section>'''
    page('/insights/', 'Law Firm Marketing Insights | Legal Marketing Firm', 'Research, guides and straight answers on law firm marketing budgets, SEO, Google Ads, AI search, intake and ROI.',
         body, crumbs=cr, ptype='insights_hub', priority=0.8)

def build_article(a):
    path = f'/insights/{a["slug"]}/'
    cr = [('Home', '/'), ('Insights', '/insights/'), (a['title'], path)]
    src = ''
    if a['sources']:
        src = '<h2>Sources</h2><ul class="sources">' + ''.join(f'<li><a href="{u}" rel="noopener" target="_blank">{e(t)}</a></li>' for t, u in a['sources']) + '</ul>'
    rel = ''.join(f'<li><a href="{h}">{e(link_title(h))}</a></li>' for h in a['links'])
    faqs = ''.join(f'<h3>{e(q)}</h3><p>{e(ans)}</p>' for q, ans in a['faqs'])
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<span class="eyebrow">Insights · {e(a["tag"])}</span><h1 class="h1" style="max-width:900px">{e(a["title"])}</h1>{byline()}</section>
<section class="wrap sec-bottom"><div class="layout-2"><article class="prose-lg">
<div class="answer"><span class="mono-k">Short answer</span>{e(a["answer"])}</div>
{a["body"]}
<h2>Frequently asked questions</h2>{faqs}
{src}
<p class="note-box">This article is general marketing information, not legal advice. Attorney advertising rules vary by state.</p>
</article>
<aside class="aside"><div class="aside-box"><h3>Get your free marketing audit</h3><p>See where your firm stands across search, paid and AI visibility.</p><a href="/free-marketing-audit/" class="btn btn-accent btn-md">Request Audit</a></div>
<div class="aside-box"><h3>Related</h3><ul>{rel}</ul></div>
<div class="aside-box"><h3>Budget calculator</h3><p>How much should your firm invest?</p><a href="/tools/law-firm-marketing-budget-calculator/" class="textlink">Calculate your budget {ic("arrow-right",16)}</a></div></aside>
</div></section>
{calc('How Much Should Your Firm Spend on <em>Marketing?</em>', 'Get a personalized monthly and annual budget based on your revenue and growth goals.', 'article', 'article_'+a['slug'].replace('-','_')) if a['calc'] else ''}'''
    schema = [{"@context": "https://schema.org", "@type": "Article", "headline": a['title'], "description": a['desc'], "author": {"@id": SITE + "/about/#matt-hensler", "@type": "Person", "name": AUTHOR},
               "publisher": {"@id": ORG_ID}, "datePublished": REVIEWED, "dateModified": REVIEWED, "mainEntityOfPage": SITE + path}, faq_schema(a['faqs'])]
    page(path, f'{a["title"][0].upper()+a["title"][1:].rstrip("?")}{"?" if a["title"].endswith("?") else ""} | Legal Marketing Firm', a['desc'], body, schema=schema, crumbs=cr, ptype='article', priority=0.7, og_type='article')

def build_research(r):
    path = f'/insights/{r["slug"]}/'
    cr = [('Home', '/'), ('Insights', '/insights/'), (r['title'], path)]
    meth = ''.join(f'<li>{e(m)}</li>' for m in r['method'])
    if r.get('guide'):
        ex = ''.join(f'<tr><td>${rev:,}</td>' + ''.join(f'<td>${rev*p//100:,}</td>' for p in (5, 10, 15, 25)) + '</tr>' for rev in (250000, 500000, 1000000, 2000000, 5000000, 10000000, 25000000, 50000000))
        main = f'''<div class="answer"><span class="mono-k">Short answer</span>Plan your total marketing investment as a share of revenue: 5% to maintain, 10% for moderate growth, 15% for accelerated growth and 25% for market expansion. Then allocate across channels based on where your clients search and what you can measure.</div>
<h2>Growth investment framework</h2><div class="table-wrap"><table><tr><th>Objective</th><th>Revenue %</th><th>Description</th></tr><tr><td>Maintain Business</td><td>5%</td><td>Minimum recommended investment to maintain business and market presence.</td></tr><tr><td>Moderate Growth</td><td>10%</td><td>Generate consistent leads and steadily grow your client base.</td></tr><tr><td>Accelerated Growth</td><td>15%</td><td>Increase case volume and capture greater market share.</td></tr><tr><td>Market Expansion</td><td>25%</td><td>Enter new markets and aggressively pursue new business.</td></tr></table></div>
<h2>Annual budget examples</h2><div class="table-wrap"><table><tr><th>Revenue</th><th>5%</th><th>10%</th><th>15%</th><th>25%</th></tr>{ex}</table></div>
<h2>Allocating the budget</h2><ul><li><strong>Capture demand:</strong> Google Ads, Local Services Ads and local SEO for people searching now.</li><li><strong>Build visibility:</strong> SEO, content and AI search optimization that compound.</li><li><strong>Build trust:</strong> reviews, video and social.</li><li><strong>Build recognition:</strong> TV, CTV, radio and outdoor where the market and budget support it.</li><li><strong>Convert:</strong> intake systems, tracking and follow-up.</li></ul>
<h2>Methodology and limitations</h2><ul>{meth}</ul>'''
        status = ''
    else:
        main = f'''<div class="answer"><span class="mono-k">What it is</span>{e(r["what"])}</div>
<p class="note-box"><strong>Status: in progress.</strong> No data has been published yet. We’ll release findings only after measurement, with the methodology below.</p>
<h2>Planned methodology</h2><ul>{meth}</ul>
<h2>Get the results</h2><p>Leave your email and we’ll send the findings when they’re published.</p>'''
        status = research_form(r['title'])
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<span class="eyebrow">Insights · Research</span><h1 class="h1" style="max-width:900px">{e(r["title"])}</h1>{byline()}</section>
<section class="wrap sec-bottom"><div class="layout-2"><article class="prose-lg">{main}{status}</article>
<aside class="aside"><div class="aside-box"><h3>Budget calculator</h3><p>Get a personalized recommendation.</p><a href="/tools/law-firm-marketing-budget-calculator/" class="textlink">Calculate your budget {ic("arrow-right",16)}</a></div><div class="aside-box"><h3>Free marketing audit</h3><p>See where your firm stands today.</p><a href="/free-marketing-audit/" class="btn btn-accent btn-md">Request Audit</a></div></aside></div></section>
{calc('Calculate Your Law Firm <em>Marketing Budget.</em>', 'Apply the framework to your firm in under a minute.', 'research', 'research_'+r['slug'].replace('-','_')) if r.get('guide') else ''}'''
    schema = [{"@context": "https://schema.org", "@type": "Article", "headline": r['title'], "description": r['desc'], "author": {"@id": SITE + "/about/#matt-hensler", "@type": "Person", "name": AUTHOR},
               "publisher": {"@id": ORG_ID}, "dateModified": REVIEWED, "mainEntityOfPage": SITE + path}]
    page(path, f'{r["title"]} | Legal Marketing Firm', r['desc'], body, schema=schema, crumbs=cr, ptype='research', priority=0.6, og_type='article')

def research_form(title):
    return f'''<form class="form-dark" data-lead-form="Research updates: {e(title)}" novalidate style="background:var(--navy-900);border:1px solid var(--line);border-radius:10px;padding:24px">
<input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">
<div class="form-body gate-fields"><div class="cf"><label for="rf-name">Name <span class="req">*</span></label><input id="rf-name" name="name" type="text" autocomplete="name" required></div>
<div class="cf"><label for="rf-em">Email <span class="req">*</span></label><input id="rf-em" name="email" type="email" autocomplete="email" required></div>
<div class="cf"><label for="rf-firm">Firm</label><input id="rf-firm" name="firm" type="text" autocomplete="organization"></div></div>
<p class="privacy-note form-body">We’ll email you when this research is published. See our <a href="/privacy-policy/">Privacy Policy</a>.</p>
<p class="status" role="alert" hidden></p><p class="ok" tabindex="-1" hidden>Thanks — we’ll send it when it’s published.</p>
<div class="form-body"><button type="submit" class="btn btn-accent btn-md">Notify Me</button></div></form>'''

def link_title(h):
    for s in SERVICES:
        if h == f'/{s["slug"]}/': return s['name']
    for p in PRACTICES:
        if h == f'/practice-areas/{p["slug"]}/': return f'{p["name"]} marketing'
    for a in ARTICLES:
        if h == f'/insights/{a["slug"]}/': return a['title'][0].upper() + a['title'][1:]
    for r in RESEARCH:
        if h == f'/insights/{r["slug"]}/': return r['title']
    m = {'/tools/law-firm-marketing-budget-calculator/': 'Marketing Budget Calculator', '/tools/cost-per-lead-calculator/': 'Cost Per Lead Calculator', '/tools/marketing-roi-calculator/': 'Marketing ROI Calculator',
         '/tools/intake-conversion-calculator/': 'Intake Conversion Calculator', '/tools/ai-visibility-audit/': 'AI Visibility Audit', '/about/': 'About us', '/results/': 'Results', '/free-marketing-audit/': 'Free marketing audit', '/markets/': 'Markets'}
    if h in m: return m[h]
    if h.startswith('/practice-areas/personal-injury/ppc/'): return 'Personal Injury Law Firm PPC'
    return h.strip('/').split('/')[-1].replace('-', ' ').title()

# ================================================================== TOOLS
TOOLS = [
 ('law-firm-marketing-budget-calculator', 'Marketing Budget Calculator', 'How much should your firm invest? Personalized monthly and annual budgets.', 'calculator'),
 ('marketing-roi-calculator', 'Marketing ROI Calculator', 'Estimate signed cases, fee revenue and return from your marketing spend.', 'trending-up'),
 ('cost-per-lead-calculator', 'Cost Per Lead Calculator', 'Calculate cost per lead and cost per signed case.', 'target'),
 ('intake-conversion-calculator', 'Intake Conversion Calculator', 'See what improving intake conversion could be worth.', 'phone'),
 ('ai-visibility-audit', 'AI Visibility Audit', 'Find out whether AI assistants mention your firm.', 'crosshair'),
 ('legal-marketing-scorecard', 'Legal Marketing Scorecard', 'A 0–100 score across SEO, paid search and AI visibility.', 'star'),
 ('seo-audit', 'SEO Audit', 'A technical and content SEO review of your firm’s website.', 'search'),
]

def build_tools_hub():
    cr = [('Home', '/'), ('Free Tools', '/tools/')]
    body = head_block(cr, 'Free Tools', 'Free Law Firm Marketing <em>Tools.</em>', 'Calculators and audits to help you plan, measure and improve your firm’s marketing. Every tool states its assumptions; none of them predicts guaranteed results.') + \
        f'<section class="wrap sec-bottom">{cards([(t, d, f"/tools/{s}/", "Open tool") for s, t, d, _ in TOOLS])}</section>'
    page('/tools/', 'Free Law Firm Marketing Tools | Legal Marketing Firm', 'Free tools for law firms: marketing budget calculator, ROI calculator, cost per lead calculator, intake conversion calculator and AI visibility audit.',
         body, crumbs=cr, ptype='tools_hub', priority=0.8)

CALC_FAQ = [('What percentage should law firms spend on marketing?', 'Our framework recommends 5% to maintain business, 10% for moderate growth, 15% for accelerated growth and 25% for market expansion. These are planning guidelines.'),
            ('What is included in a marketing budget?', 'Media, agency fees, marketing staff, website, SEO, AI search, creative, PR and technology.'),
            ('How is monthly spend calculated?', 'Multiply annual revenue by the selected percentage and divide by 12.'),
            ('Does more spend guarantee clients?', 'No. Strategy, competition, intake and conversion affect outcomes.')]

def build_budget_tool():
    path = '/tools/law-firm-marketing-budget-calculator/'
    cr = [('Home', '/'), ('Free Tools', '/tools/'), ('Marketing Budget Calculator', path)]
    ex = ''.join(f'<tr><td>${rev:,}</td>' + ''.join(f'<td>${rev*p//100:,}</td>' for p in (5, 10, 15, 25)) + '</tr>' for rev in (250000, 500000, 1000000, 2000000, 5000000, 10000000, 25000000, 50000000))
    body = f'''<section class="wrap" style="padding-top:clamp(28px,4vw,48px)">{crumbs_html(cr)}</section>
<section class="wrap" style="padding-top:20px;padding-bottom:clamp(40px,6vw,72px)">{calc('How Much Should Your Law Firm Spend on <em>Marketing?</em>', 'Your marketing budget should reflect your growth ambitions. Whether you are maintaining your existing business or expanding into new markets, discover how much your firm should consider investing in marketing.', 'tool', 'tool_page', wrap=False, full=True)}</section>
<section class="band"><div class="wrap sec"><div class="layout-2"><div class="prose-lg">
<h2 class="mt-0">Growth investment framework</h2>
<div class="table-wrap"><table><tr><th>Objective</th><th>Revenue %</th><th>Description</th></tr><tr><td>Maintain Business</td><td>5%</td><td>Minimum recommended investment to maintain business and market presence.</td></tr><tr><td>Moderate Growth</td><td>10%</td><td>Generate consistent leads and steadily grow your client base.</td></tr><tr><td>Accelerated Growth</td><td>15%</td><td>Increase case volume and capture greater market share.</td></tr><tr><td>Market Expansion</td><td>25%</td><td>Enter new markets and aggressively pursue new business.</td></tr></table></div>
<p>These are LegalMarketingFirm.net planning recommendations, not measured industry averages or guaranteed outcomes. Total marketing investment includes agency fees, media, personnel, technology and production. Consider cash flow, profitability and acquisition costs.</p>
<h2>How the calculator works</h2>
<div class="table-wrap"><table><tr><th>Output</th><th>Formula</th></tr><tr><td>Recommended annual budget</td><td>Annual revenue × selected percentage</td></tr><tr><td>Recommended monthly budget</td><td>Recommended annual budget ÷ 12</td></tr><tr><td>Current annual spend</td><td>Current monthly spend × 12</td></tr><tr><td>Current revenue percentage</td><td>Current annual spend ÷ annual revenue × 100</td></tr><tr><td>Monthly investment gap</td><td>max(0, recommended monthly − current monthly)</td></tr><tr><td>Annual investment gap</td><td>max(0, recommended annual − current annual)</td></tr></table></div>
<h2>Example: accelerated growth</h2>
<div class="table-wrap"><table><tr><th>Input / output</th><th>Value</th></tr><tr><td>Annual revenue</td><td>$2,000,000</td></tr><tr><td>Current monthly spend</td><td>$5,000</td></tr><tr><td>Current annual spend</td><td>$60,000</td></tr><tr><td>Current investment</td><td>3%</td></tr><tr><td>Selected objective</td><td>Accelerated Growth (15%)</td></tr><tr><td>Recommended monthly / annual</td><td>$25,000 / $300,000</td></tr><tr><td>Monthly / annual gap</td><td>$20,000 / $240,000</td></tr></table></div>
<h2>Annual budget examples by revenue</h2>
<div class="table-wrap"><table><tr><th>Revenue</th><th>5%</th><th>10%</th><th>15%</th><th>25%</th></tr>{ex}</table></div>
<h2>Frequently asked questions</h2>{''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in CALC_FAQ)}
<p class="byline" style="margin-top:12px">Methodology reviewed by <a href="/about/"><strong style="margin-left:4px">{AUTHOR}</strong></a>, {AUTHOR_ROLE} · Updated {date.fromisoformat(REVIEWED).strftime("%B %-d, %Y")}</p>
</div>
<aside class="aside"><div class="aside-box"><h3>Related reading</h3><ul><li><a href="/insights/how-much-should-a-law-firm-spend-on-marketing/">How much should a law firm spend on marketing?</a></li><li><a href="/insights/how-much-does-law-firm-marketing-cost/">How much does law firm marketing cost?</a></li><li><a href="/insights/law-firm-marketing-budget-guide/">Law firm marketing budget guide</a></li><li><a href="/insights/how-to-market-a-personal-injury-law-firm/">Personal injury marketing</a></li></ul></div>
<div class="aside-box"><h3>Need help allocating it?</h3><p>We’ll show you where each dollar should go.</p><a href="/free-marketing-audit/" class="btn btn-accent btn-md">Free Marketing Audit</a></div></aside>
</div></div></section>'''
    schema = [{"@context": "https://schema.org", "@type": "WebApplication", "name": "Law Firm Marketing Budget Calculator", "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
               "url": SITE + path, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@id": ORG_ID},
               "description": "Calculate a recommended monthly and annual law firm marketing budget based on revenue and growth goals."}, faq_schema(CALC_FAQ)]
    page(path, 'Law Firm Marketing Budget Calculator | Free Budget Tool',
         'Calculate your recommended monthly and annual law firm marketing budget based on revenue and growth goals with our free calculator.',
         body, schema=schema, crumbs=cr, ptype='tool', priority=0.9)

def simple_tool(slug, title, h1, desc, intro, tool, fields, assumptions, related):
    path = f'/tools/{slug}/'
    cr = [('Home', '/'), ('Free Tools', '/tools/'), (title, path)]
    f_html = ''.join(f'<div class="cf"><label for="{slug}-{n}">{e(l)}{" <span class=\"req\">*</span>" if req else " <span class=\"hint\">(optional)</span>"}</label>{"<div class=\"money\"><span aria-hidden=\"true\">$</span>" if money else ""}<input id="{slug}-{n}" name="{n}" type="text" inputmode="decimal" data-num{" data-money" if money else ""}{" required" if req else ""} placeholder="{ph}">{"</div>" if money else ""}</div>' for n, l, money, req, ph in fields)
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<span class="eyebrow">Free Tools</span><h1 class="h1">{h1}</h1><p class="lede" style="max-width:680px">{e(intro)}</p></section>
<section class="wrap sec-bottom"><div class="layout-2"><div class="tool"><form data-tool="{tool}" novalidate class="stack-md"><div class="calc-fields">{f_html}</div><p class="status" role="alert" hidden></p><div><button type="submit" class="btn btn-accent btn-lg">Calculate {ARROW}</button></div></form>
<div class="tool-out" aria-live="polite" hidden></div>
<div class="prose-lg" style="font-size:15px"><h2 style="font-size:20px;margin-top:0">Assumptions</h2><ul>{"".join(f"<li>{e(a)}</li>" for a in assumptions)}</ul><p style="color:var(--navy-300)">Estimates only, based on the numbers you enter. Not a forecast or guarantee.</p></div></div>
<aside class="aside"><div class="aside-box"><h3>Related</h3><ul>{"".join(f'<li><a href="{h}">{e(link_title(h))}</a></li>' for h in related)}</ul></div><div class="aside-box"><h3>Want a real plan?</h3><p>Get a free audit of your firm’s marketing.</p><a href="/free-marketing-audit/" class="btn btn-accent btn-md">Free Marketing Audit</a></div></aside></div></section>
{calc('Next: How Much Should Your Firm <em>Invest?</em>', 'Get a personalized monthly and annual marketing budget based on revenue and growth goals.', 'tool', 'tool_'+slug.replace('-','_'))}'''
    schema = [{"@context": "https://schema.org", "@type": "WebApplication", "name": title, "applicationCategory": "BusinessApplication", "operatingSystem": "Any", "url": SITE + path,
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@id": ORG_ID}, "description": desc}]
    page(path, f'{title} for Law Firms | Legal Marketing Firm', desc, body, schema=schema, crumbs=cr, ptype='tool', priority=0.7)

def audit_tool(slug, title, h1, desc, intro, gets):
    path = f'/tools/{slug}/'
    cr = [('Home', '/'), ('Free Tools', '/tools/'), (title, path)]
    g = ''.join(f'<div>{ic("check",20,"ic gold")}<div><h3>{e(t)}</h3><p>{e(b)}</p></div></div>' for t, b in gets)
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<span class="eyebrow">Free Tools · Expert-Reviewed</span><h1 class="h1">{h1}</h1><p class="lede" style="max-width:680px">{e(intro)}</p></section>
<section class="wrap sec-bottom stack-lg"><div class="deliv">{g}</div>
<div class="layout-2">{audit_form(title)}<aside class="aside"><div class="aside-box"><h3>How it works</h3><p>This isn’t an instant automated score. Our strategists review your firm manually and email your results, typically within 5 business days.</p></div></aside></div></section>'''
    page(path, f'{title} for Law Firms | Legal Marketing Firm', desc, body, crumbs=cr, ptype='tool', priority=0.7)

def audit_form(form_name, budget=False):
    popts = '<option value="">Select…</option>' + ''.join(f'<option>{e(o)}</option>' for o in PRACTICE_OPTS)
    sopts = '<option value="">—</option>' + ''.join(f'<option>{a}</option>' for a in STATE_ABBRS)
    bud = '<div class="cf"><label for="af-bud">Monthly marketing budget</label><select id="af-bud" name="budget"><option value="">Select…</option><option>Under $5k</option><option>$5–15k</option><option>$15–50k</option><option>$50k+</option><option>Not sure</option></select></div>' if budget else ''
    return f'''<form class="form-dark" data-lead-form="{e(form_name)}" novalidate style="background:var(--navy-900);border:1px solid var(--line);border-radius:12px;padding:clamp(22px,3vw,36px)">
<input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">
<div class="form-body stack-md"><h2 class="h2-md" style="font-size:26px">Request your {e(form_name.lower()) if form_name != "Free marketing audit" else "free audit"}</h2>
<div class="gate-fields">
<div class="cf"><label for="af-fn">First name <span class="req">*</span></label><input id="af-fn" name="first_name" type="text" autocomplete="given-name" required></div>
<div class="cf"><label for="af-ln">Last name <span class="req">*</span></label><input id="af-ln" name="last_name" type="text" autocomplete="family-name" required></div>
<div class="cf"><label for="af-firm">Firm name <span class="req">*</span></label><input id="af-firm" name="firm" type="text" autocomplete="organization" required></div>
<div class="cf"><label for="af-em">Business email <span class="req">*</span></label><input id="af-em" name="email" type="email" autocomplete="email" required></div>
<div class="cf"><label for="af-web">Firm website <span class="req">*</span></label><input id="af-web" name="firm_website" type="url" placeholder="https://" autocomplete="url" required></div>
<div class="cf"><label for="af-pa">Primary practice area <span class="req">*</span></label><select id="af-pa" name="practice_area" required>{popts}</select></div>
<div class="cf"><label for="af-ph">Phone</label><input id="af-ph" name="phone" type="tel" autocomplete="tel"></div>
<div class="cf"><label for="af-city">City</label><input id="af-city" name="city" type="text" autocomplete="address-level2"></div>
<div class="cf"><label for="af-st">State</label><select id="af-st" name="state">{sopts}</select></div>
{bud}
</div>
<div class="cf"><label for="af-det">Anything we should know?</label><textarea id="af-det" name="details" placeholder="Goals, markets, competitors, current agencies…"></textarea></div>
<label class="check"><input type="checkbox" name="consent"> Send me occasional legal marketing insights by email. (Optional)</label>
<p class="privacy-note">We use your details to prepare your audit and follow up about our services. We don’t sell your information. See our <a href="/privacy-policy/">Privacy Policy</a>.</p></div>
<p class="status" role="alert" hidden></p>
<p class="ok" tabindex="-1" hidden>Thanks — request received. A strategist will email you within one business day, and your results typically arrive within 5 business days.</p>
<div class="form-body"><button type="submit" class="btn btn-accent btn-lg">Request My Free Audit {ARROW}</button></div>
</form>'''

def build_tools():
    build_tools_hub(); build_budget_tool()
    simple_tool('marketing-roi-calculator', 'Marketing ROI Calculator', 'Law Firm Marketing <em>ROI Calculator.</em>',
        'Estimate signed cases, fee revenue and return on marketing spend for your law firm.', 'Estimate how many signed cases and how much fee revenue your monthly marketing could produce, and what return that represents.',
        'roi', [('spend', 'Monthly marketing spend', True, True, '20,000'), ('leads', 'Leads per month', False, True, '60'), ('conv', 'Lead-to-signed-case rate (%)', False, True, '10'), ('value', 'Average fee per signed case', True, True, '10,000')],
        ['ROI = (estimated fee revenue − marketing spend) ÷ marketing spend.', 'Fee revenue = leads × conversion rate × average fee.', 'Contingency fees may be realized months or years later; this treats them as expected value.'],
        ['/insights/how-to-measure-law-firm-marketing-roi/', '/tools/cost-per-lead-calculator/', '/law-firm-marketing-strategy/'])
    simple_tool('cost-per-lead-calculator', 'Cost Per Lead Calculator', 'Law Firm <em>Cost Per Lead</em> Calculator.',
        'Calculate cost per lead and cost per signed case for your law firm’s marketing.', 'Calculate what each lead and each signed case costs you — the numbers that matter more than clicks.',
        'cpl', [('spend', 'Marketing spend (period)', True, True, '15,000'), ('leads', 'Leads in the period', False, True, '50'), ('signed', 'Signed cases in the period', False, False, '5')],
        ['Cost per lead = spend ÷ leads.', 'Cost per signed case = spend ÷ signed cases.', 'Use the same period and channel for all three numbers.'],
        ['/insights/what-is-a-good-cost-per-lead-for-law-firms/', '/tools/marketing-roi-calculator/', '/law-firm-ppc/'])
    simple_tool('intake-conversion-calculator', 'Intake Conversion Calculator', 'Law Firm <em>Intake Conversion</em> Calculator.',
        'See how many more cases and how much more revenue improving intake conversion could produce for your law firm.', 'See what improving your lead-to-client conversion rate could be worth — often more than increasing ad spend.',
        'intake', [('leads', 'Leads per month', False, True, '80'), ('conv', 'Current lead-to-client rate (%)', False, True, '8'), ('target', 'Target lead-to-client rate (%)', False, True, '12'), ('value', 'Average fee per signed case', True, False, '8,000')],
        ['Signed cases = leads × conversion rate.', 'Added annual revenue = added cases per month × average fee × 12.', 'Assumes lead volume and quality stay constant.'],
        ['/insights/how-to-improve-law-firm-intake-conversion/', '/law-firm-intake-optimization/', '/tools/marketing-roi-calculator/'])
    audit_tool('ai-visibility-audit', 'AI Visibility Audit', 'Is Your Firm Visible in <em>AI Search?</em>', 'Find out whether ChatGPT, Gemini, Perplexity and Google AI Overviews mention your law firm. Free, expert-reviewed AI visibility audit.',
        'We test the prompts your prospects use across major AI assistants and show where your firm is mentioned, cited or missing — and what to fix first.',
        [('Prompt testing', 'Practice- and city-specific prompts run across major AI tools.'), ('Mention and citation log', 'Where your firm appears, which sources are cited and who’s recommended instead.'), ('Entity check', 'Consistency of your firm’s information across profiles and directories.'), ('Priority fixes', 'The changes most likely to improve visibility.')])
    audit_tool('legal-marketing-scorecard', 'Legal Marketing Scorecard', 'Your Legal Marketing <em>Scorecard.</em>', 'Get a 0–100 legal marketing scorecard across SEO, paid search and AI search visibility — the TriSearch Growth Audit.',
        'The TriSearch Growth Audit scores your firm from 0 to 100 across 12 signals in three pillars — SEO, paid search and AI search (GEO) — and shows where you’re winning and losing to competitors.',
        [('SEO pillar', 'Technical health, practice pages, local visibility and authority.'), ('Paid search pillar', 'Ad presence, landing pages, tracking and competitive position.'), ('GEO pillar', 'AI mentions, entity consistency and citable content.'), ('One-page report', 'A clear score, grade and priority list.')])
    audit_tool('seo-audit', 'SEO Audit', 'Free Law Firm <em>SEO Audit.</em>', 'Request a free technical and content SEO audit of your law firm’s website, reviewed by a strategist.',
        'A strategist reviews your site’s technical health, practice pages, local signals and content gaps — and tells you what to fix first.',
        [('Technical review', 'Indexation, speed, mobile, structured data and internal links.'), ('Practice page review', 'Coverage, depth and search intent match.'), ('Local signals', 'Google Business Profile, reviews and citations.'), ('Content gaps', 'Questions competitors answer that you don’t.')])
    redirect('/tools/marketing-budget-calculator/', '/tools/law-firm-marketing-budget-calculator/')
    redirect('/tools/budget-planner/', '/tools/law-firm-marketing-budget-calculator/')

# ================================================================== CORE: about / contact / audit / legal
def build_about():
    cr = [('Home', '/'), ('About', '/about/')]
    body = f'''{head_block(cr, 'About Legal Marketing Firm', 'Legal Marketing Built Around <em>Signed Cases.</em>', 'We’re a legal marketing firm for law firms. We combine SEO, paid search, AI search optimization and integrated advertising into one strategy — and measure it by qualified intake and signed clients.')}
<section class="band"><div class="wrap sec two-col"><div class="stack-sm" style="align-content:start"><span class="eyebrow">Our approach</span><h2 class="h2">The TriSearch <em>Framework.</em></h2></div>
<div class="prose"><p>Prospects now find law firms in three places: traditional search, paid search and AI assistants. Our TriSearch Intelligence framework treats them as one system — so the content that ranks also gets cited, and the paid campaigns that capture demand also teach us what to build next.</p>
<p>We’re outcome-focused: every engagement starts with a diagnostic, sets targets tied to intake and signed cases, and reports against them. We use AI to move faster; experienced strategists make every call.</p>
<p>We’re a marketing agency, not a law firm. We don’t provide legal advice, and we work with your attorneys to keep marketing within your jurisdiction’s advertising rules.</p></div></div></section>
<section class="wrap sec two-col" id="matt-hensler"><div class="stack-sm" style="align-content:start"><span class="eyebrow">Leadership</span><h2 class="h2">{AUTHOR}</h2><p class="mono-k">Head of Strategy</p></div>
<div class="prose"><p>Matt leads strategy at Legal Marketing Firm and reviews our published insights and tools. He brings 15+ years across integrated marketing, agency leadership, digital media and the restaurant and hospitality industry, with a focus on building measurable growth systems.</p>
<p>Matt holds an MA from Full Sail University, where he graduated as valedictorian, and a BA from DePaul University.</p>
<p><a href="https://www.linkedin.com/in/mjhensler" rel="noopener" target="_blank">Connect on LinkedIn</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p></div></section>
<section class="band"><div class="wrap sec stack-lg"><h2 class="h2">How We <em>Work.</em></h2>{steps_html(STEPS4)}</div></section>'''
    page('/about/', 'About Our Legal Marketing Agency | Legal Marketing Firm', 'Meet Legal Marketing Firm: our TriSearch approach to SEO, paid search and AI search for law firms, and the team behind it.',
         body, schema=[PERSON], crumbs=cr, ptype='about', priority=0.6)

def build_contact():
    cr = [('Home', '/'), ('Contact', '/contact/')]
    chips = ''.join(f'<button type="button" class="chip">{x}</button>' for x in ["Workers' comp", 'Personal injury', 'Family law', 'Criminal defense', 'Employment law', 'Estate planning', 'Other'])
    body = f'''<main class="contact" id="contact-flow" style="padding-top:clamp(28px,4vw,48px)">
{crumbs_html(cr)}
<h1 class="h1" style="font-size:clamp(32px,4vw,52px)">Contact Our Legal Marketing <em>Agency.</em></h1>
<p class="lede">Tell us about your firm and we’ll follow up within one business day. Prefer email? <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<div class="stack-xs"><div class="c-meta"><span>Let’s Build Your Strategy</span><span class="c-step-label">Question 1 of 3</span></div><div class="c-progress"><span></span><span></span><span></span><span></span></div></div>
<div class="c-step" data-step="0"><h2 class="h-contact">What’s your primary <em>practice area?</em></h2><div class="chips" data-field="practice">{chips}</div></div>
<div class="c-step" data-step="1" hidden><h2 class="h-contact">What’s your monthly <em>marketing budget?</em></h2><div class="chips" data-field="budget"><button type="button" class="chip">Under $5k</button><button type="button" class="chip">$5–15k</button><button type="button" class="chip">$15k+</button></div></div>
<div class="c-step" data-step="2" hidden><h2 class="h-contact">Where should we <em>send your plan?</em></h2>
<form class="card" id="lead-form" novalidate><input type="text" name="hp" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">
<div class="fields"><label class="field"><span>Your name</span><input name="name" type="text" placeholder="Jordan Smith" autocomplete="name" required></label><label class="field"><span>Firm name</span><input name="firm" type="text" placeholder="Smith &amp; Partners LLP" autocomplete="organization" required></label><label class="field"><span>Email</span><input name="email" type="email" placeholder="you@firm.com" autocomplete="email" required></label><label class="field"><span>Phone</span><input name="phone" type="tel" placeholder="(555) 000-0000" autocomplete="tel"></label></div>
<p class="form-err" role="alert" hidden></p>
<button type="submit" class="btn btn-accent btn-lg btn-full">Let’s Build Your Strategy {ARROW}</button>
<p class="form-note">We use your details to follow up about your request. See our <a href="/privacy-policy/">Privacy Policy</a>.</p></form></div>
<div class="c-step" data-step="3" hidden><span class="eyebrow">Request received</span><h2 class="h-contact">Thanks. <em>We’ll be in touch.</em></h2><p class="lede" style="max-width:560px">A strategist will email you within one business day to schedule your 30-minute review.</p><div><a href="/results/" class="btn btn-inverse btn-md">See Real Results</a></div></div>
<a href="#" class="c-back" hidden>{ic("arrow-left",16)}Back</a>
<div class="grid-cells assure"><div>{ic("clock",20,"ic gold")}Reply within one business day</div><div>{ic("shield-check",20,"ic gold")}No contract, no obligation</div><div>{ic("mail",20,"ic gold")}<a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
</main>'''
    body = body.replace('<main class="contact"', '<div class="contact"').replace('</main>', '</div>')
    page('/contact/', 'Contact Our Legal Marketing Agency | Legal Marketing Firm', 'Contact Legal Marketing Firm to build a marketing strategy for your law firm. Email hello@legalmarketingfirm.net or tell us about your firm.',
         body, schema=[{"@context": "https://schema.org", "@type": "ContactPage", "url": SITE + "/contact/", "about": {"@id": ORG_ID}}], crumbs=cr, ptype='contact', cta=False, priority=0.7)

def build_audit():
    path = '/free-marketing-audit/'
    cr = [('Home', '/'), ('Free Marketing Audit', path)]
    gets = [('0–100 TriSearch score', 'Your firm scored across 12 signals in three pillars: SEO, paid search and AI search (GEO).'),
            ('Competitor comparison', 'Where you stand against the firms winning your market.'),
            ('AI visibility check', 'Whether AI assistants mention or cite your firm for key prompts.'),
            ('Priority fixes', 'The handful of changes most likely to increase qualified intake.'),
            ('One-page report', 'Clear, visual and easy to share with your partners.'),
            ('30-minute review', 'A walkthrough with a strategist — no obligation.')]
    g = ''.join(f'<div>{ic("check",20,"ic gold")}<div><h3>{e(t)}</h3><p>{e(b)}</p></div></div>' for t, b in gets)
    faqs = [('Is the audit really free?', 'Yes. No contract and no obligation.'), ('How long does it take?', 'Your report typically arrives within 5 business days.'),
            ('Who reviews it?', 'A strategist reviews every audit manually; it isn’t an automated score.'), ('What do you need from us?', 'Just your website and a few details. We may ask about your current channels and goals.')]
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<span class="eyebrow">Free · TriSearch Growth Audit</span><h1 class="h1">Get Your Free Law Firm <em>Marketing Audit.</em></h1><p class="lede" style="max-width:720px">See exactly where your firm stands across search, paid and AI visibility — and what to fix first to win more cases.</p></section>
<section class="wrap sec-bottom stack-lg"><div class="deliv">{g}</div><div class="layout-2">{audit_form("Free marketing audit", budget=True)}
<aside class="aside"><div class="aside-box"><h3>What happens next</h3><ul><li>1. We confirm your request within one business day.</li><li>2. A strategist audits your firm.</li><li>3. You get your one-page report and a 30-minute review.</li></ul></div><div class="aside-box"><h3>Prefer email?</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></aside></div></section>
{faq_section(faqs, 'Audit <em>Questions.</em>')}'''
    page(path, 'Free Law Firm Marketing Audit | Legal Marketing Firm', 'Request a free law firm marketing audit: a 0–100 TriSearch score across SEO, paid search and AI search, competitor comparison and priority fixes.',
         body, schema=[faq_schema(faqs)], crumbs=cr, ptype='audit', cta=False, priority=0.9)

def build_legal():
    upd = date.fromisoformat(REVIEWED).strftime('%B %-d, %Y')
    cr = [('Home', '/'), ('Privacy Policy', '/privacy-policy/')]
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<h1 class="h1">Privacy <em>Policy.</em></h1><p class="byline">Last updated {upd}</p></section>
<section class="wrap sec-bottom"><div class="prose-lg">
<p>This policy explains how LegalMarketingFirm.net (“we,” “us”) collects and uses information through this website. Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Information you give us</h2><ul><li><strong>Contact and audit forms:</strong> name, firm, email, phone, website, practice area, location, budget range and anything you write in the form.</li>
<li><strong>Marketing budget calculator:</strong> the contact details above plus the financial figures you enter (annual revenue, current monthly marketing spend and growth objective) and the results we calculate from them.</li>
<li><strong>Email preferences:</strong> whether you opt in to marketing emails. This is optional and unchecked by default.</li></ul>
<h2>Information collected automatically</h2><ul><li><strong>Analytics:</strong> we use Google Analytics 4 to understand site usage (pages viewed, device, approximate location, referring site). We do not send your name, email, phone or financial figures to Google Analytics or advertising platforms.</li>
<li><strong>Attribution:</strong> your browser stores the first page you visited, the referring site and any campaign (UTM) parameters in local storage so we can tell which marketing brought you here. This is sent with any form you submit.</li></ul>
<h2>How we use it</h2><ul><li>To respond to your request, prepare audits and send calculator results and reports.</li><li>To follow up about our services.</li><li>To send marketing emails if you opted in (you can unsubscribe anytime).</li><li>To improve our website and marketing.</li></ul>
<h2>Where it’s stored</h2><p>Form submissions are stored in a Google Sheet in our Google Workspace account and delivered to our team by email. Access is restricted to our team. We don’t sell your information.</p>
<h2>Retention</h2><p>We keep submissions for as long as needed to respond, provide services and maintain business records, and delete them on request unless we’re required to keep them.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete your information by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>. Depending on where you live (for example, California), you may have additional rights under state privacy law; we’ll honor applicable requests.</p>
<h2>Personalized reports</h2><p>Calculator reports are generated for you and emailed to the address you provide. They aren’t published on the web.</p>
<h2>Changes</h2><p>We’ll update this page if our practices change.</p></div></section>'''
    page('/privacy-policy/', 'Privacy Policy | Legal Marketing Firm', 'How LegalMarketingFirm.net collects, uses and stores information submitted through this website.', body, crumbs=cr, ptype='legal', cta=False, priority=0.2)
    cr = [('Home', '/'), ('Terms', '/terms/')]
    body = f'''<section class="wrap page-head">{crumbs_html(cr)}<h1 class="h1">Website <em>Terms.</em></h1><p class="byline">Last updated {upd}</p></section>
<section class="wrap sec-bottom"><div class="prose-lg">
<p>By using LegalMarketingFirm.net you agree to these terms.</p>
<h2>Not legal advice</h2><p>We’re a marketing agency, not a law firm. Content on this site is general marketing information, not legal advice, and using this site doesn’t create an attorney-client relationship. Attorney advertising rules vary by jurisdiction; consult qualified counsel.</p>
<h2>Tools and calculators</h2><p>Our calculators and audits provide planning estimates based on the information you enter and our stated assumptions. They are not forecasts or guarantees of results.</p>
<h2>Results</h2><p>Results described on this site are marketing metrics from specific engagements. They are not case outcomes and don’t guarantee similar results.</p>
<h2>Intellectual property</h2><p>Site content, design and the TriSearch name and framework belong to LegalMarketingFirm.net. You may share links and brief quotations with attribution.</p>
<h2>Third-party links</h2><p>We link to other sites for reference and aren’t responsible for their content.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent permitted by law, we aren’t liable for losses arising from your use of the site or reliance on its content.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of California.</p>
<h2>Contact</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></section>'''
    page('/terms/', 'Website Terms | Legal Marketing Firm', 'Terms of use for LegalMarketingFirm.net, including disclaimers for tools, calculators and results.', body, crumbs=cr, ptype='legal', cta=False, priority=0.2)

# ================================================================== misc files
def build_misc():
    nf = f'''<section class="wrap page-head" style="min-height:50vh"><span class="eyebrow">404</span><h1 class="h1">That Page Isn’t on the <em>Scoreboard.</em></h1><p class="lede">The page you’re looking for doesn’t exist or has moved.</p><div class="btns"><a href="/" class="btn btn-accent btn-lg">Go Home</a><a href="/services/" class="btn btn-inverse btn-lg">Services</a><a href="/markets/" class="btn btn-inverse btn-lg">Markets</a></div></section>'''
    page('/404/', 'Page Not Found | Legal Marketing Firm', 'This page could not be found.', nf, robots='noindex, follow', sitemap=False)
    shutil.move(os.path.join(ROOT, '404', 'index.html'), os.path.join(ROOT, '404.html')); os.rmdir(os.path.join(ROOT, '404'))
    urls = ''.join(f'<url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr:.1f}</priority></url>\n' for p, pr in PAGES)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'''# Search engines and AI crawlers are intentionally allowed: we want our public content to be indexed and cited.
User-agent: *
Allow: /
Disallow: /_src/

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: {SITE}/sitemap.xml
''')
    llms = f'''# Legal Marketing Firm (LegalMarketingFirm.net)

> A legal marketing firm for law firms: SEO, paid search, AI search optimization (GEO/AEO) and integrated advertising, measured by qualified intake and signed cases. Contact: {EMAIL}. We are a marketing agency, not a law firm.

## Core
- [Services]({SITE}/services/): all law firm marketing services
- [Practice areas]({SITE}/practice-areas/): marketing by practice
- [Markets]({SITE}/markets/): {len(CITIES)} U.S. markets
- [Results]({SITE}/results/): case study scoreboard
- [Free marketing audit]({SITE}/free-marketing-audit/): TriSearch Growth Audit (0–100 across SEO, paid search, GEO)

## Tools
- [Law Firm Marketing Budget Calculator]({SITE}/tools/law-firm-marketing-budget-calculator/): framework of 5% / 10% / 15% / 25% of revenue by growth objective

## Answers
''' + ''.join(f'- [{a["title"]}]({SITE}/insights/{a["slug"]}/): {a["answer"][:160]}…\n' for a in ARTICLES)
    open(os.path.join(ROOT, 'llms.txt'), 'w').write(llms)

def clean():
    keep = {'.git', '_src', 'assets', 'CNAME', '.gitignore', 'og-image.jpg', 'README.md'}
    for n in os.listdir(ROOT):
        if n in keep: continue
        p = os.path.join(ROOT, n)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

if __name__ == '__main__':
    clean()
    build_home(); build_services_hub()
    for s in SERVICES: build_service(s)
    build_practice_hub()
    for p in PRACTICES: build_practice(p)
    for pslug in COMBO_PRACTICES:
        for cs, cn, parent in COMBO_SERVICES: build_combo(pslug, cs, cn, parent)
    build_markets_hub()
    for ab in STATES: build_state(ab)
    for c in CITIES: build_city(c)
    for sub, t, parent in ROCKFORD_SUBS: build_rockford_sub(sub, t, parent)
    build_results(); build_case_study()
    build_insights_hub()
    for a in ARTICLES: build_article(a)
    for r in RESEARCH: build_research(r)
    build_tools(); build_about(); build_contact(); build_audit(); build_legal(); build_misc()
    print(f'Built {len(PAGES)} indexable pages, {CALC_N[0]} calculator instances.')
