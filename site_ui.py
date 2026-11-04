"""Komponen markup dan ikon untuk situs LSP Pariwisata Citra Indonesia."""

import html as _html
from urllib.parse import quote
from site_data import SITE, NAV, NAV_FOOTER, NAV_LEGAL, SCHEME_CATS, STATUS_LABEL, JADWAL

# ---------------------------------------------------------------------------
# Ikon (stroke 24x24)
# ---------------------------------------------------------------------------
ICONS = {
    "arrow": '<path d="M4 12h15"/><path d="m13 6 6 6-6 6"/>',
    "arrow-up-right": '<path d="M7 17 17 7"/><path d="M8 7h9v9"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "check": '<path d="m20 6-11 11-5-5"/>',
    "check-circle": '<circle cx="12" cy="12" r="9"/><path d="m8.4 12.2 2.5 2.4 4.7-5"/>',
    "phone": '<path d="M6.8 3.5H5.4A2.9 2.9 0 0 0 2.5 6.4c0 8.3 6.8 15.1 15.1 15.1a2.9 2.9 0 0 0 2.9-2.9v-1.4l-4.4-1.5-1.5 2a13 13 0 0 1-5.3-5.3l2-1.5z"/>',
    "mail": '<rect x="2.5" y="4.5" width="19" height="15" rx="3"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    "map-pin": '<path d="M20 10.5c0 5.4-8 11-8 11s-8-5.6-8-11a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10.5" r="2.8"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7.5V12l3.2 2"/>',
    "star": '<path d="m12 3.6 2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8L3.5 9.8l5.9-.9z"/>',
    "shield": '<path d="M12 2.8 20 6v5.7c0 4.6-3.3 8.1-8 9.5-4.7-1.4-8-4.9-8-9.5V6z"/><path d="m9 12 2.2 2.2L15.5 10"/>',
    "users": '<circle cx="9" cy="8.5" r="3.3"/><path d="M2.8 20c.5-3.3 3-5.2 6.2-5.2s5.7 1.9 6.2 5.2"/><path d="M16.2 5.6a3.2 3.2 0 0 1 0 6.2"/><path d="M18 14.9c2.1.5 3.4 2.1 3.7 4.4"/>',
    "route": '<circle cx="6" cy="6" r="2.6"/><circle cx="18" cy="18" r="2.6"/><path d="M8.6 6H14a4 4 0 0 1 0 8h-4a4 4 0 0 0 0 8h5.4"/>',
    "award": '<circle cx="12" cy="9" r="5.5"/><path d="m8.5 13.4-1.6 7 5.1-2.6 5.1 2.6-1.6-7"/>',
    "bed": '<path d="M3 18v-9"/><path d="M3 12h18a3 3 0 0 1 3 3v3"/><path d="M3 18h21"/><path d="M7 12V9a1.5 1.5 0 0 1 1.5-1.5h3A1.5 1.5 0 0 1 13 9v3"/><circle cx="19" cy="9.5" r="2"/>',
    "cup": '<path d="M4 8h13v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M17 9.5h1.8a2.7 2.7 0 0 1 0 5.4H17"/><path d="M7 3.5v2M11 3v2.5M15 3.5v2"/>',
    "chef": '<path d="M7 21h10"/><path d="M6 17h12v-2a5 5 0 0 0 1.2-9.6A4.2 4.2 0 0 0 12 4.2 4.2 4.2 0 0 0 4.8 5.4 5 5 0 0 0 6 15z"/><path d="M9 12.5v3M12 11v4.5M15 12.5v3"/>',
    "spark": '<path d="m12 3 1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="m18.5 15.5.9 2.1 2.1.9-2.1.9-.9 2.1-.9-2.1-2.1-.9 2.1-.9z"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="M7.5 14h2M12 14h2M16.5 14h.5M7.5 17.5h2M12 17.5h2"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3.2 9.5h17.6M3.2 14.5h17.6"/><path d="M12 3c2.4 2.4 3.7 5.5 3.7 9s-1.3 6.6-3.7 9c-2.4-2.4-3.7-5.5-3.7-9S9.6 5.4 12 3Z"/>',
    "palette": '<path d="M12 3a9 9 0 0 0 0 18c1.4 0 2-1 2-2s.7-2 2-2h1.5a3.5 3.5 0 0 0 3.5-3.5C21 7.4 17 3 12 3Z"/><circle cx="8" cy="10" r="1.2"/><circle cx="12" cy="7.5" r="1.2"/><circle cx="16" cy="10" r="1.2"/><circle cx="7" cy="14.5" r="1.2"/>',
    "scale": '<path d="M12 3v18M7 21h10"/><path d="M12 6 4 8l3 6h2l3-6"/><path d="M12 6l8 2-3 6h-2l-3-6"/>',
    "lock": '<rect x="4.5" y="10" width="15" height="11" rx="3"/><path d="M8 10V7.5a4 4 0 0 1 8 0V10"/>',
    "bolt": '<path d="M13.5 2.5 4 14h6l-1.5 7.5L19 10h-6z"/>',
    "quote": '<path d="M9.5 6C6.5 7 5 9.4 5 13v5h5v-6H7.5c0-2 .8-3.2 2.6-3.9z" fill="currentColor" stroke="none"/><path d="M18.5 6C15.5 7 14 9.4 14 13v5h5v-6h-2.5c0-2 .8-3.2 2.6-3.9z" fill="currentColor" stroke="none"/>',
    "download": '<path d="M12 3.5v11"/><path d="m7.5 10.5 4.5 4.5 4.5-4.5"/><path d="M4 17.5v1.5a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-1.5"/>',
    "file": '<path d="M14 3.5H7.5a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2V8z"/><path d="M14 3.5V8h4.5"/><path d="M8.5 12.5h7M8.5 16h5"/>',
    "building": '<rect x="4" y="3.5" width="16" height="17" rx="2"/><path d="M9 8h1.5M13.5 8H15M9 12h1.5M13.5 12H15M9 16h1.5M13.5 16H15"/>',
    "graduation": '<path d="m2.8 8.5 9.2-4 9.2 4-9.2 4z"/><path d="M6.5 10.4V16c0 1.4 2.5 2.6 5.5 2.6s5.5-1.2 5.5-2.6v-5.6"/><path d="M21.2 8.5v5"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5"/><circle cx="12" cy="7.8" r="1" fill="currentColor" stroke="none"/>',
    "whatsapp": '<path fill="currentColor" stroke="none" d="M12.04 2.5a9.4 9.4 0 0 0-8.03 14.3L2.5 21.5l4.83-1.48a9.4 9.4 0 1 0 4.71-17.52Zm5.5 13.36c-.23.65-1.35 1.25-1.87 1.3-.5.06-1.1.1-3.1-.7-2.4-1-3.92-3.5-4.04-3.7-.12-.2-.9-1.3-.9-2.4 0-1.1.6-1.64.8-1.86.2-.22.44-.28.6-.28h.42c.14 0 .33-.05.5.4l.7 1.7c.06.14.1.3.02.47l-.3.47c-.1.13-.2.27-.09.47.1.2.5.84 1.06 1.33.72.64 1.32.84 1.51.93.19.1.3.08.41-.04l.55-.65c.13-.16.26-.12.43-.06l1.62.76c.17.08.28.12.32.19.04.07.04.4-.2 1.05Z"/>',
    "instagram": '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r="1" fill="currentColor" stroke="none"/>',
    "linkedin": '<rect x="3.5" y="3.5" width="17" height="17" rx="4"/><path d="M7.5 10.5V17M7.5 7.6v.1"/><path d="M11.5 17v-3.6a2.4 2.4 0 0 1 4.8 0V17"/><path d="M11.5 10.5V17"/>',
    "youtube": '<rect x="2.5" y="5.5" width="19" height="13" rx="4"/><path d="m10.5 9.5 5 2.5-5 2.5z"/>',
    "facebook": '<path d="M14.5 21v-7.5h2.6l.4-3h-3V8.7c0-.9.3-1.5 1.6-1.5H17.7V4.5c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.4-4 4v2.1H8.7v3h2.6V21"/>',
    "play": '<circle cx="12" cy="12" r="9"/><path d="m10 8.5 5.5 3.5L10 15.5z"/>',
}

SOCIAL_ICONS = [("instagram", "Instagram"), ("linkedin", "LinkedIn"), ("youtube", "YouTube"), ("facebook", "Facebook")]


def icon(name: str, cls: str = "ico") -> str:
    body = ICONS.get(name, ICONS["check"])
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
        f'focusable="false">{body}</svg>'
    )


def esc(text: str) -> str:
    return _html.escape(text, quote=True)


def wa_link(message: str) -> str:
    return f"https://wa.me/{SITE['wa']}?text={quote(message)}"


def _asset_href(value: str, base: str) -> str:
    """Lokasi aset yang diunggah panel admin (logo, gambar berita, dll.)."""
    path = str(value or "").strip()
    if not path:
        return ""
    if path.startswith(("data:", "http://", "https://", "//", "/")):
        return path
    if path.startswith("assets/"):
        return base + path
    return f"{base}assets/img/{path}"


def brand_mark_html(base: str, light: bool = False) -> str:
    """Tampilkan logo unggahan admin; bila kosong pakai lambang bawaan."""
    logo = _asset_href(SITE.get("logo", ""), base)
    if logo:
        extra = " brand__logo--light" if light else ""
        return f'<span class="brand__logo-wrap"><img class="brand__logo{extra}" src="{esc(logo)}" alt="" loading="eager" decoding="async"></span>'
    return (f'<span class="brand__mark">{icon("shield", "brand__shield")}'
            f'<span class="brand__star">{icon("star", "brand__star-ico")}</span></span>')


# ---------------------------------------------------------------------------
# Header / navigasi
# ---------------------------------------------------------------------------
def _nav_href(href: str, base: str) -> str:
    """Dukung tautan internal (tentang-kami/), absolut (/kontak/), dan eksternal."""
    value = str(href or "").strip()
    if not value:
        return base
    if value.startswith(("http://", "https://", "mailto:", "tel:", "#", "/")):
        return value
    return base + value


def _nav_active(href: str, current: str) -> bool:
    value = str(href or "").strip()
    if not value or value.startswith(("http://", "https://", "mailto:", "tel:", "#", "/")):
        return False
    return value.split("#")[0].rstrip("/") == current.rstrip("/")


def _nav_item(item: dict, current: str, base: str, index: int) -> str:
    label = str(item.get("label") or "").strip()
    href = str(item.get("href") or "").strip()
    raw_children = item.get("children") if isinstance(item.get("children"), list) else []
    children = [c for c in raw_children if isinstance(c, dict) and str(c.get("label") or "").strip()]
    active = _nav_active(href, current)
    if not children:
        aria = ' aria-current="page"' if active else ""
        return (
            f'<li class="nav__item"><a class="nav__link{" is-active" if active else ""}" '
            f'href="{esc(_nav_href(href, base))}"{aria}>{esc(label)}</a></li>'
        )

    is_open = current != "" and any(_nav_active(c.get("href", ""), current) for c in children if isinstance(c, dict))
    slug = "".join(ch if ch.isalnum() else "-" for ch in label.lower()).strip("-") or "menu"
    panel_id = f"menu-{index}-{slug}"
    links = "".join(
        f'<li><a class="mega__link" href="{esc(_nav_href(c.get("href", ""), base))}">'
        f'<span class="mega__title">{esc(str(c.get("label") or ""))}</span>'
        f'<span class="mega__desc">{esc(str(c.get("desc") or ""))}</span>'
        f'<span class="mega__arrow">{icon("arrow", "ico ico--xs")}</span></a></li>'
        for c in children if isinstance(c, dict)
    )
    return (
        f'<li class="nav__item has-mega">'
        f'<button class="nav__link nav__toggle{" is-active" if is_open else ""}" type="button" '
        f'aria-expanded="false" aria-controls="{panel_id}">{esc(label)}'
        f'{icon("chevron-down", "ico ico--xs nav__chev")}</button>'
        f'<div class="mega" id="{panel_id}">'
        f'<div class="mega__panel"><p class="mega__label">{esc(label)}</p>'
        f'<ul class="mega__list">{links}</ul></div></div></li>'
    )


def nav_html(current: str, base: str) -> str:
    items = "".join(
        _nav_item(n, current, base, i) for i, n in enumerate(NAV)
        if isinstance(n, dict) and str(n.get("label") or "").strip()
    )
    return (
        '<div class="nav__mobile-head">'
        '<span class="nav__mobile-title">Menu</span>'
        '<button class="nav__close" type="button" aria-label="Tutup menu"><span></span><span></span></button>'
        '</div>'
        f'<ul class="nav__list">{items}</ul>'
    )


def header_html(current: str, base: str) -> str:
    return f"""
<div class="scroll-progress" aria-hidden="true"><i></i></div>

<a class="skip-link" href="#main">Lewati ke konten</a>

<aside class="topbar" aria-label="Informasi kontak cepat">
  <div class="container topbar__inner">
    <p class="topbar__note">{icon("clock", "ico ico--xs")} <span>{SITE["hours"]}</span></p>
    <div class="topbar__links">
      <a href="tel:{SITE["phone_link"]}">{icon("phone", "ico ico--xs")} {SITE["phone_display"]}</a>
      <a href="mailto:{SITE["email"]}" class="topbar__mail">{icon("mail", "ico ico--xs")} {SITE["email"]}</a>
      <a class="topbar__login" href="{SITE["login_url"]}" target="_blank" rel="noopener">
        Login SIAPkerja {icon("arrow-up-right", "ico ico--xs")}
      </a>
    </div>
  </div>
</aside>

<header class="site-header" id="siteHeader">
  <div class="container header__inner">
    <a class="brand" href="{base}" aria-label="{SITE['legal']} — Beranda">
      {brand_mark_html(base)}
      <span class="brand__text">
        <strong>{esc(SITE["name"])}</strong>
        <span>Lembaga Sertifikasi Profesi</span>
      </span>
    </a>

    <nav class="nav" id="primaryNav" aria-label="Navigasi utama">
      {nav_html(current, base)}
      <div class="nav__mobile-extra">
        <a class="btn btn--primary btn--block" href="{base}kontak/#daftar">Daftar Sertifikasi {icon("arrow", "ico ico--xs")}</a>
        <p class="nav__mobile-contact">{icon("phone", "ico ico--xs")} <a href="tel:{SITE['phone_link']}">{SITE['phone_display']}</a></p>
      </div>
    </nav>

    <div class="header__actions">
      <a class="btn btn--primary btn--sm header__cta" href="{base}kontak/#daftar">
        <span>Daftar Sertifikasi</span>{icon("arrow", "ico ico--xs")}
      </a>
      <button class="nav-toggle" type="button" aria-controls="primaryNav" aria-expanded="false" aria-label="Buka menu">
        <span></span><span></span>
      </button>
    </div>
  </div>
</header>
<div class="nav-backdrop" hidden></div>
"""


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
def footer_html(base: str) -> str:
    year = 2026
    location = str(SITE.get("address") or "").strip()
    city = str(SITE.get("city") or "").strip()
    if city and city.lower() not in location.lower():
        location = f"{location}, {city}" if location else city
    socials = "".join(
        f'<a class="social" href="{SITE["social"][k]}" target="_blank" rel="noopener" aria-label="{label}">{icon(k)}</a>'
        for k, label in SOCIAL_ICONS
    )
    skema_links = "".join(
        f'<li><a href="{base}skema-sertifikasi/#{c["id"]}">{c["label"]}</a></li>' for c in SCHEME_CATS
    )
    footer_links = "".join(
        f'<li><a href="{esc(_nav_href(n.get("href", ""), base))}">{esc(str(n.get("label") or ""))}</a></li>'
        for n in NAV_FOOTER if isinstance(n, dict) and str(n.get("label") or "").strip()
    )
    legal_links = "".join(
        f'<li><a href="{esc(_nav_href(n.get("href", ""), base))}">{esc(str(n.get("label") or ""))}</a></li>'
        for n in NAV_LEGAL if isinstance(n, dict) and str(n.get("label") or "").strip()
    )
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer__top">
      <div class="footer__brand">
        <a class="brand brand--light" href="{base}">
          {brand_mark_html(base, light=True)}
          <span class="brand__text"><strong>{esc(SITE["name"])}</strong><span>Lembaga Sertifikasi Profesi</span></span>
        </a>
        <p class="footer__desc">{SITE['legal']} melaksanakan sertifikasi kompetensi berdasarkan SKKNI dan skema yang terlisensi BNSP, dengan komitmen penuh pada integritas dan ketidakberpihakan.</p>
        <div class="footer__socials">{socials}</div>
      </div>

      <nav class="footer__col" aria-label="Skema sertifikasi">
        <h2>Bidang Sertifikasi</h2>
        <ul>{skema_links}</ul>
      </nav>

      <nav class="footer__col" aria-label="Informasi">
        <h2>Informasi</h2>
        <ul>
          {footer_links}
        </ul>
      </nav>

      <div class="footer__col footer__contact">
        <h2>Hubungi Kami</h2>
        <ul class="footer__contact-list">
          <li>{icon("map-pin", "ico ico--xs")}<span>{location}</span></li>
          <li>{icon("phone", "ico ico--xs")}<a href="tel:{SITE['phone_link']}">{SITE['phone_display']}</a></li>
          <li>{icon("mail", "ico ico--xs")}<a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
          <li>{icon("clock", "ico ico--xs")}<span>{SITE['hours']}</span></li>
        </ul>
        <a class="btn btn--ghost-light btn--sm" href="{base}kontak/">Kirim pesan {icon("arrow", "ico ico--xs")}</a>
      </div>
    </div>

    <div class="footer__bottom">
      <p>&copy; {year} {SITE['legal']}. Seluruh hak cipta dilindungi.</p>
      <ul class="footer__legal">
        {legal_links}
        <li><a class="footer__admin" href="{base}admin/" title="Login admin" aria-label="Login admin">{icon("lock", "ico ico--xs")}<span>Login admin</span></a></li>
      </ul>
      <p class="footer__badge">{icon("shield", "ico ico--xs")} Terlisensi BNSP</p>
    </div>
  </div>

  <a class="fab fab--wa" href="{wa_link(f'Halo {SITE["name"]}, saya ingin bertanya tentang sertifikasi kompetensi.')}"
   target="_blank" rel="noopener" aria-label="Chat WhatsApp">
  {icon("whatsapp", "fab__ico")}
  <span class="fab__label">Tanya Admin</span>
  </a>
  <button class="to-top" type="button" aria-label="Kembali ke atas">{icon("arrow", "ico")}</button>
</footer>
"""


# ---------------------------------------------------------------------------
# Potongan komponen
# ---------------------------------------------------------------------------
def page_intro(eyebrow: str, title: str, lead: str, crumb: str, base: str, crumb_url: str = "") -> str:
    """Hero halaman dalam (breadcrumb + judul)."""
    return f"""
<section class="page-hero">
  <div class="page-hero__bg" aria-hidden="true"></div>
  <div class="container page-hero__inner">
    <nav class="crumbs" aria-label="Breadcrumb">
      <ol>
        <li><a href="{base}">Beranda</a></li>
        <li><span aria-current="page">{crumb}</span></li>
      </ol>
    </nav>
    <p class="eyebrow eyebrow--light">{eyebrow}</p>
    <h1 class="page-hero__title">{title}</h1>
    <p class="page-hero__lead">{lead}</p>
  </div>
</section>
"""


def scheme_card(s: dict, base: str, i: int = 0) -> str:
    # Data dari panel admin bisa saja merujuk bidang yang sudah dihapus.
    # Jangan sampai build gagal: tampilkan sebagai "Lainnya".
    cat = next((c for c in SCHEME_CATS if c.get("id") == s.get("cat")), None)
    if not cat:
        cat = {"id": "lainnya", "label": "Lainnya", "icon": "award"}
    cat_id = esc(str(s.get("cat") or cat.get("id") or "lainnya"))
    level = esc(str(s.get("level") or "—"))
    units = esc(str(s.get("units") or "—"))
    return f"""
<article class="scheme-card" data-cat="{cat_id}">
  <div class="scheme-card__top">
    <span class="scheme-card__icon">{icon(cat.get('icon', 'award'))}</span>
    <span class="tag">{level}</span>
  </div>
  <h3 class="scheme-card__title">{esc(str(s.get('name') or 'Skema Sertifikasi'))}</h3>
  <p class="scheme-card__desc">{esc(str(s.get('desc') or ''))}</p>
  <div class="scheme-card__meta">
    <span>{units} unit kompetensi</span>
    <span class="dot" aria-hidden="true"></span>
    <span>{esc(str(cat.get('label') or 'Lainnya'))}</span>
  </div>
  <a class="scheme-card__cta" href="{base}kontak/#daftar">Tanya skema ini {icon("arrow", "ico ico--xs")}</a>
</article>
"""


def faq_item(item: dict, i: int, open_first: bool = False) -> str:
    opened = " open" if open_first else ""
    return f"""
<details class="faq-item"{opened}>
  <summary class="faq-item__q"><span class="faq-item__no">{i:02d}</span><span>{item['q']}</span><span class="faq-item__icon" aria-hidden="true"></span></summary>
  <div class="faq-item__a"><p>{item['a']}</p></div>
</details>
"""


def post_image_src(p: dict, base: str) -> str:
    """Lokasi gambar berita: nama lama, path unggahan, URL, atau data URL."""
    image = str(p.get("image", "")).strip()
    if not image:
        return f"{base}assets/img/photos/hero.jpg"
    if image.startswith(("data:", "http://", "https://", "//")):
        return image
    if image.startswith("assets/"):
        return base + image
    return f"{base}assets/img/photos/{image}.jpg"


def post_card(p: dict, base: str) -> str:
    from datetime import date
    try:
        d = date.fromisoformat(str(p.get("date") or "").strip())
    except (TypeError, ValueError):
        d = date.today()
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
             "Agustus", "September", "Oktober", "November", "Desember"][d.month - 1]
    title = str(p.get("title") or "Berita")
    cat = str(p.get("cat") or "Berita")
    return f"""
<article class="post-card" data-post-cat="{esc(cat)}">
  <a class="post-card__media" href="{base}berita/" aria-label="{esc(title)}">
    <img src="{esc(post_image_src(p, base))}" alt="" loading="lazy" width="720" height="480">
    <span class="tag tag--dark">{esc(cat)}</span>
  </a>
  <div class="post-card__body">
    <p class="post-card__date"><time datetime="{d.isoformat()}">{d.day} {bulan} {d.year}</time></p>
    <h3 class="post-card__title"><a href="{base}berita/">{esc(title)}</a></h3>
    <p class="post-card__excerpt">{esc(str(p.get('excerpt') or ''))}</p>
    <span class="post-card__more">Baca selengkapnya {icon("arrow", "ico ico--xs")}</span>
  </div>
</article>
"""


def asesor_card(a: dict) -> str:
    license_html = ""
    if str(a.get("license") or "").strip():
        license_html = f'<li>{icon("file", "ico ico--xs")} {esc(str(a["license"]))}</li>'
    return f"""
<article class="person-card">
  <span class="person-card__avatar" aria-hidden="true">{esc(str(a.get('initials') or 'AS'))}</span>
  <h3 class="person-card__name">{esc(str(a.get('name') or ''))}</h3>
  <p class="person-card__role">{esc(str(a.get('field') or ''))}</p>
  <ul class="person-card__meta">
    <li>{icon("map-pin", "ico ico--xs")} {esc(str(a.get('city') or ''))}</li>
    <li>{icon("shield", "ico ico--xs")} Asesor sejak {esc(str(a.get('year') or ''))}</li>
    {license_html}
  </ul>
</article>
"""


def jadwal_rows() -> str:
    rows = []
    for j in JADWAL:
        label, cls = STATUS_LABEL.get(j.get("status"), ("Dibuka", "is-open"))
        scheme = str(j.get("scheme") or "")
        rows.append(f"""
      <tr>
        <td data-label="Tanggal"><strong>{esc(str(j.get('date') or ''))}</strong></td>
        <td data-label="Skema">{esc(scheme)}</td>
        <td data-label="TUK">{esc(str(j.get('tuk') or ''))}</td>
        <td data-label="Metode"><span class="tag tag--soft">{esc(str(j.get('mode') or ''))}</span></td>
        <td data-label="Kuota">{esc(str(j.get('quota') or '—'))} peserta</td>
        <td data-label="Status"><span class="status {cls}"><i></i>{label}</span></td>
        <td data-label="Aksi"><a class="btn btn--outline btn--sm" href="{{{{BASE}}}}kontak/#daftar" data-pick-scheme="{esc(scheme)}">Daftar</a></td>
      </tr>""")
    return "".join(rows)
