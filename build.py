#!/usr/bin/env python3
"""Generator situs statis LSP Patra Indo.

Jalankan:  python3 build.py
Output  :  index.html, <slug>/index.html, sitemap.xml, robots.txt, .htaccess

Konten halaman berada di src/pages/*.html dan dapat memakai placeholder
seperti {{SCHEMES_ALL}} atau {{FAQ_ALL}} yang diisi dari site_data.py.
"""

import html
import json
from datetime import date
from pathlib import Path

from site_data import (
    SITE, PAGES, STATS, ADVANTAGES, SCHEMES, SCHEME_CATS, STEPS, TESTIMONIALS,
    ASESOR, TUK, JADWAL, FAQ, POSTS, VALUES, STRUKTUR, HERO_ROLES, TICKER_ITEMS,
    PAGE_HTML,
)
from site_ui import (
    icon, esc, wa_link, header_html, footer_html, scheme_card, faq_item,
    post_card, asesor_card, jadwal_rows,
)

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src" / "pages"
TODAY = date.today().isoformat()
YEAR = date.today().year

PRIORITY = {"": "1.0", "skema-sertifikasi": "0.9", "jadwal": "0.9", "kontak": "0.8",
            "alur-sertifikasi": "0.8", "persyaratan": "0.8"}

# Naikkan nilai ini saat admin.css/admin.js berubah agar peramban tidak
# memakai berkas lama dari cache.
ADMIN_ASSET_VERSION = "20261030b"


# ---------------------------------------------------------------------------
# Data turunan untuk template
# ---------------------------------------------------------------------------
def stats_html() -> str:
    out = []
    for s in STATS:
        out.append(f"""
      <div class="stat">
        <p class="stat__value"><span data-count="{s['value']}">0</span><span class="stat__suffix">{s['suffix']}</span></p>
        <p class="stat__label">{s['label']}</p>
        <p class="stat__note">{s['note']}</p>
      </div>""")
    return "".join(out)


def advantages_html() -> str:
    return "".join(f"""
      <article class="feature-card">
        <span class="feature-card__icon">{icon(a['icon'])}</span>
        <h3>{a['title']}</h3>
        <p>{a['text']}</p>
      </article>""" for a in ADVANTAGES)


def cat_tabs() -> str:
    tabs = ['<button class="chip is-active" type="button" data-filter="all">Semua skema</button>']
    for c in SCHEME_CATS:
        tabs.append(f'<button class="chip" type="button" data-filter="{c["id"]}">{c["label"]}</button>')
    return "".join(tabs)


def schemes_html(only_featured: bool = False) -> str:
    items = [s for s in SCHEMES if s.get("featured")] if only_featured else SCHEMES
    return "".join(scheme_card(s, "{{BASE}}") for s in items)


def schemes_count_html() -> str:
    return "".join(f"""
      <a class="cat-card" href="{{{{BASE}}}}skema-sertifikasi/#{c['id']}" data-cat-link="{c['id']}">
        <span class="cat-card__icon">{icon(c['icon'])}</span>
        <span class="cat-card__label">{c['label']}</span>
        <span class="cat-card__count">{sum(1 for s in SCHEMES if s['cat'] == c['id'])} skema</span>
        <span class="cat-card__desc">{c['desc']}</span>
      </a>""" for c in SCHEME_CATS)


def steps_html(compact: bool = False) -> str:
    out = []
    for s in STEPS:
        out.append(f"""
      <li class="step">
        <span class="step__no">{s['no']}</span>
        <div class="step__body">
          <h3>{s['title']}</h3>
          <p>{s['text']}</p>
          <span class="step__time">{icon('clock', 'ico ico--xs')} {s['duration']}</span>
        </div>
      </li>""")
    return "".join(out)


def testimonials_html() -> str:
    return "".join(f"""
      <figure class="quote-card" data-slide>
        <span class="quote-card__mark">{icon('quote', 'quote-card__mark-ico')}</span>
        <div class="quote-card__stars" role="img" aria-label="5 dari 5 bintang">
          {''.join(icon('star', 'quote-card__star') for _ in range(5))}
        </div>
        <blockquote><p>{t['quote']}</p></blockquote>
        <figcaption class="quote-card__author">
          <span class="avatar avatar--{t['tone']}">{t['initials']}</span>
          <span><strong>{t['name']}</strong><small>{t['role']}</small></span>
        </figcaption>
      </figure>""" for t in TESTIMONIALS)


def faq_html(limit=None) -> str:
    items = FAQ[:limit] if limit else FAQ
    return "".join(faq_item(q, i + 1, open_first=(i == 0)) for i, q in enumerate(items))


def posts_html(limit=None) -> str:
    items = POSTS[:limit] if limit else POSTS
    return "".join(post_card(p, "{{BASE}}") for p in items)


def post_categories_html() -> str:
    """Chip filter berita, dibuat dari kategori yang benar-benar dipakai."""
    cats = []
    for post in POSTS:
        cat = str(post.get("cat", "")).strip()
        if cat and cat not in cats:
            cats.append(cat)
    chips = ['<button class="chip is-active" type="button" data-post-filter="all" aria-pressed="true">Semua</button>']
    for cat in cats:
        chips.append(
            f'<button class="chip" type="button" data-post-filter="{esc(cat)}" aria-pressed="false">{esc(cat)}</button>'
        )
    return "".join(chips)


def asesor_html() -> str:
    return "".join(asesor_card(a) for a in ASESOR)


def tuk_html() -> str:
    return "".join(f"""
      <article class="tuk-card">
        <div class="tuk-card__head">
          <span class="tag tag--soft">{t['type']}</span>
          <span class="tuk-card__city">{icon('map-pin', 'ico ico--xs')} {t['city']}</span>
        </div>
        <h3>{t['name']}</h3>
        <p class="tuk-card__address">{t['address']}</p>
        <p class="tuk-card__meta">{t['schemes']} skema tersedia</p>
      </article>""" for t in TUK)


def values_html() -> str:
    return "".join(f"""
      <article class="value-card">
        <span class="value-card__icon">{icon(v['icon'])}</span>
        <h3>{v['title']}</h3>
        <p>{v['text']}</p>
      </article>""" for v in VALUES)


def struktur_html() -> str:
    return "".join(f"""
      <article class="person-card person-card--plain">
        <span class="person-card__avatar" aria-hidden="true">{p['initials']}</span>
        <p class="person-card__role person-card__role--top">{p['role']}</p>
        <h3 class="person-card__name">{p['name']}</h3>
        <p class="person-card__note">{p['note']}</p>
      </article>""" for p in STRUKTUR)


def jadwal_cards_html() -> str:
    """Tampilan kartu jadwal untuk layar kecil."""
    out = []
    for j in JADWAL:
        label, cls = STATUS_LABEL_LOCAL[j["status"]]
        out.append(f"""
      <article class="jcard">
        <div class="jcard__top"><span class="jcard__date">{j['date']}</span><span class="status {cls}"><i></i>{label}</span></div>
        <h3>{j['scheme']}</h3>
        <ul class="jcard__meta">
          <li>{icon('map-pin', 'ico ico--xs')} TUK {j['tuk']}</li>
          <li>{icon('users', 'ico ico--xs')} Kuota {j['quota']} peserta</li>
          <li>{icon('info', 'ico ico--xs')} Metode {j['mode']}</li>
        </ul>
        <a class="btn btn--outline btn--sm btn--block" href="{{{{BASE}}}}kontak/#daftar" data-pick-scheme="{j['scheme']}">Daftar jadwal ini</a>
      </article>""")
    return "".join(out)


STATUS_LABEL_LOCAL = {
    "open": ("Dibuka", "is-open"),
    "almost": ("Hampir penuh", "is-almost"),
    "wait": ("Menunggu kuota", "is-wait"),
}


TICKER_STAR = ('<svg class="ticker__star" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
               '<path d="m12 3.6 2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8L3.5 9.8l5.9-.9z"/></svg>')


def ticker_group(hidden: bool = False) -> str:
    items = "".join(
        f'<span class="ticker__item{" ticker__item--outline" if t["outline"] else ""}">'
        f'{t["text"]} {TICKER_STAR}</span>'
        for t in TICKER_ITEMS
    )
    attr = ' aria-hidden="true"' if hidden else ""
    return f'<div class="ticker__group"{attr}>{items}</div>'


def ticker_html() -> str:
    return ticker_group() + "\n" + ticker_group(True)


def rotator_json() -> str:
    return html.escape(json.dumps(HERO_ROLES, ensure_ascii=False), quote=True)


def tokens(base: str) -> dict:
    return {
        "{{BASE}}": base,
        "{{YEAR}}": str(YEAR),
        "{{SITE_NAME}}": SITE["name"],
        "{{SITE_LEGAL}}": SITE["legal"],
        "{{DOMAIN}}": SITE["domain"],
        "{{URL}}": SITE["url"],
        "{{PHONE}}": SITE["phone_display"],
        "{{PHONE_LINK}}": SITE["phone_link"],
        "{{EMAIL}}": SITE["email"],
        "{{EMAIL_SERTIFIKASI}}": SITE["email_sertifikasi"],
        "{{ADDRESS}}": SITE["address"],
        "{{CITY}}": SITE["city"],
        "{{HOURS}}": SITE["hours"],
        "{{WA}}": SITE["wa"],
        "{{FORM_ENDPOINT}}": SITE.get("form_endpoint", ""),
        "{{ADMIN_API}}": SITE.get("admin_api", ""),
        "{{GH_REPO}}": SITE.get("github_repo", "LSPPatraIndo/LSPPatraIndo"),
        "{{GH_BRANCH}}": SITE.get("github_branch", "main"),
        "{{WA_LINK}}": wa_link("Halo LSP Patra Indo, saya ingin berkonsultasi mengenai sertifikasi kompetensi."),
        "{{WA_LINK_SKEMA}}": wa_link("Halo LSP Patra Indo, saya ingin menanyakan ketersediaan skema sertifikasi dan biayanya."),
        "{{WA_LINK_KORPORAT}}": wa_link("Halo LSP Patra Indo, saya ingin berdiskusi mengenai kerja sama sertifikasi korporat."),
        "{{MAPS}}": SITE["maps_query"],
        "{{STATS}}": stats_html(),
        "{{ADVANTAGES}}": advantages_html(),
        "{{CAT_TABS}}": cat_tabs(),
        "{{CAT_CARDS}}": schemes_count_html(),
        "{{SCHEMES_ALL}}": schemes_html(),
        "{{SCHEMES_FEATURED}}": schemes_html(only_featured=True),
        "{{SCHEME_OPTIONS}}": "".join(f'<option value="{x["name"]}">{x["name"]}</option>' for x in SCHEMES),
        "{{SCHEME_COUNT}}": str(len(SCHEMES)),
        "{{STEPS}}": steps_html(),
        "{{TESTIMONIALS}}": testimonials_html(),
        "{{FAQ_ALL}}": faq_html(),
        "{{FAQ_HOME}}": faq_html(6),
        "{{POSTS_ALL}}": posts_html(),
        "{{POSTS_HOME}}": posts_html(3),
        "{{POST_CATS}}": post_categories_html(),
        "{{POST_COUNT}}": str(len(POSTS)),
        "{{ASESOR}}": asesor_html(),
        "{{TUK}}": tuk_html(),
        "{{JADWAL_ROWS}}": jadwal_rows(),
        "{{JADWAL_CARDS}}": jadwal_cards_html(),
        "{{VALUES}}": values_html(),
        "{{STRUKTUR}}": struktur_html(),
        "{{TICKER_GROUPS}}": ticker_html(),
        "{{ROTATOR_WORDS}}": rotator_json(),
    }


# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------
def jsonld(slug: str, title: str, desc: str, canonical: str) -> str:
    org = {
        "@type": ["EducationalOrganization", "Organization"],
        "@id": f"{SITE['url']}/#organization",
        "name": SITE["legal"],
        "alternateName": SITE["name"],
        "url": SITE["url"],
        "description": SITE["description"],
        "email": SITE["email"],
        "telephone": SITE["phone_link"],
        "foundingDate": str(SITE["founded"]),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": SITE["address"],
            "addressLocality": "Jakarta Selatan",
            "addressRegion": "DKI Jakarta",
            "postalCode": "12930",
            "addressCountry": "ID",
        },
        "areaServed": {"@type": "Country", "name": "Indonesia"},
        "sameAs": list(SITE["social"].values()),
    }
    graph = [org]

    if not slug:
        graph.append({
            "@type": "WebSite",
            "@id": f"{SITE['url']}/#website",
            "url": SITE["url"],
            "name": SITE["name"],
            "inLanguage": "id-ID",
            "publisher": {"@id": f"{SITE['url']}/#organization"},
        })

    graph.append({
        "@type": "WebPage",
        "@id": canonical + "#webpage",
        "url": canonical,
        "name": title,
        "description": desc,
        "inLanguage": "id-ID",
        "isPartOf": {"@id": f"{SITE['url']}/#website"},
        "about": {"@id": f"{SITE['url']}/#organization"},
    })

    if slug:
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Beranda", "item": SITE["url"] + "/"},
                {"@type": "ListItem", "position": 2, "name": title.split(" — ")[0], "item": canonical},
            ],
        })

    if slug == "faq":
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in FAQ
            ],
        })

    if slug == "skema-sertifikasi":
        graph.append({
            "@type": "ItemList",
            "name": "Skema Sertifikasi LSP Patra Indo",
            "numberOfItems": len(SCHEMES),
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "item": {"@type": "Course", "name": s["name"], "description": s["desc"],
                          "provider": {"@id": f"{SITE['url']}/#organization"}}}
                for i, s in enumerate(SCHEMES)
            ],
        })

    return ('<script type="application/ld+json">'
            + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
            + "</script>")


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
def head_html(meta: dict, base: str, canonical: str) -> str:
    og_image = f"{SITE['url']}/assets/img/og-image.jpg"
    title, desc = meta["title"], meta["desc"]
    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0A1F35">
<meta name="author" content="{SITE['legal']}">
<meta name="geo.region" content="ID-JK">
<meta name="geo.placename" content="Jakarta Selatan">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="id_ID">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{SITE['legal']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og_image}">

<link rel="icon" href="{base}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{base}assets/img/apple-touch-icon.png">
<link rel="manifest" href="{base}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/css/style.css">
<link rel="stylesheet" href="{base}assets/css/sections.css">
<link rel="stylesheet" href="{base}assets/css/pages.css">
<link rel="stylesheet" href="{base}assets/css/motion.css">
{jsonld(meta['slug'], title, desc, canonical)}
</head>"""


def render(page: tuple) -> Path:
    body_file, slug, title, desc, crumb = page
    base = "" if slug == "" else "../"
    canonical = f"{SITE['url']}/{slug + '/' if slug else ''}"

    body = PAGE_HTML.get(slug) or (SRC / f"{body_file}.html").read_text(encoding="utf-8")
    meta = {"slug": slug, "title": title, "desc": desc, "crumb": crumb}

    for key, value in tokens(base).items():
        body = body.replace(key, value)
    # Pass kedua: token yang tersisip lewat komponen (mis. kartu skema)
    body = body.replace("{{BASE}}", base)

    html = f"""{head_html(meta, base, canonical)}
<body class="page-{slug or 'home'}">
{header_html(slug, base)}
<main id="main">
{body}
</main>
{footer_html(base)}
<script src="{base}assets/js/main.js" defer></script>
</body>
</html>
"""
    out = ROOT / "index.html" if slug == "" else ROOT / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Berkas pendukung
# ---------------------------------------------------------------------------
def write_sitemap() -> None:
    urls = []
    for body_file, slug, title, desc, crumb in PAGES:
        loc = f"{SITE['url']}/{slug + '/' if slug else ''}"
        urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{'weekly' if slug in ('', 'berita', 'jadwal') else 'monthly'}</changefreq>
    <priority>{PRIORITY.get(slug, '0.7')}</priority>
  </url>""")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")

    (ROOT / "site.webmanifest").write_text(json.dumps({
        "name": SITE["legal"],
        "short_name": SITE["name"],
        "description": SITE["description"],
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#0A1F35",
        "lang": "id",
        "icons": [
            {"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (ROOT / ".htaccess").write_text("""# LSP Patra Indo — konfigurasi Apache
Options -Indexes
DirectoryIndex index.html

<IfModule mod_rewrite.c>
  RewriteEngine On

  # HTTPS + non-www
  RewriteCond %{HTTPS} !=on
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
  RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
  RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]

  # URL tanpa ekstensi .html -> folder/index.html
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteCond %{REQUEST_FILENAME}\\.html -f
  RewriteRule ^(.+?)/?$ $1.html [L]
</IfModule>

ErrorDocument 404 /404.html

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/json
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType image/jpeg "access plus 6 months"
  ExpiresByType image/png "access plus 6 months"
  ExpiresByType image/webp "access plus 6 months"
  ExpiresByType image/gif "access plus 6 months"
  ExpiresByType image/svg+xml "access plus 6 months"
  ExpiresByType text/html "access plus 0 seconds"
</IfModule>

<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
""", encoding="utf-8")


def write_404() -> None:
    body = (SRC / "404.html").read_text(encoding="utf-8")
    for key, value in tokens("").items():
        body = body.replace(key, value)
    meta = {"slug": "404", "title": "Halaman tidak ditemukan — LSP Patra Indo",
            "desc": "Halaman yang Anda cari tidak tersedia."}
    html = f"""{head_html(meta, "", SITE['url'] + '/404.html').replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex, follow">')}
<body class="page-404">
{header_html("404", "")}
<main id="main">
{body}
</main>
{footer_html("")}
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    (ROOT / "404.html").write_text(html, encoding="utf-8")


def write_admin() -> None:
    """Bangun /admin/ — halaman panel, tidak masuk sitemap dan noindex."""
    body = (SRC / "admin.html").read_text(encoding="utf-8")
    for key, value in tokens("../").items():
        body = body.replace(key, value)
    body = body.replace("{{BASE}}", "../")

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">
<meta name="referrer" content="same-origin">
<title>Panel Admin — LSP Patra Indo</title>
<meta name="theme-color" content="#0a1f35">
<meta name="lsp-admin-api" content="{esc(SITE.get('admin_api', ''))}">
<meta name="lsp-gh-repo" content="{esc(SITE.get('github_repo', 'LSPPatraIndo/LSPPatraIndo'))}">
<meta name="lsp-gh-branch" content="{esc(SITE.get('github_branch', 'main'))}">
<link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../assets/css/admin.css?v={ADMIN_ASSET_VERSION}">
</head>
<body class="adm-body">
{body}
<script src="../assets/js/admin.js?v={ADMIN_ASSET_VERSION}" defer></script>
</body>
</html>
"""
    out = ROOT / "admin" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


def main() -> None:
    built = [render(p) for p in PAGES]
    write_404()
    write_admin()
    write_sitemap()
    for path in built:
        print("  ✓", path.relative_to(ROOT))
    print("  ✓", (ROOT / "admin" / "index.html").relative_to(ROOT))
    print(f"\nSelesai: {len(built)} halaman + 404 + panel admin, sitemap, robots, manifest, htaccess.")


if __name__ == "__main__":
    main()
