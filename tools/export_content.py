#!/usr/bin/env python3
"""Ekspor data bawaan site_data.py menjadi data/content.json.

Berkas hasilnya dipakai panel admin (/admin/) sebagai sumber data yang bisa
diedit. Nilai di site_data.py tetap menjadi fallback bila JSON kosong/rusak.

Jalankan:
    python3 tools/export_content.py            # buat/segarkan data/content.json
    python3 tools/export_content.py --check    # bandingkan tanpa menulis
"""

import json
import os
import sys
from pathlib import Path

os.environ["LSP_NO_OVERRIDE"] = "1"  # baca nilai bawaan, bukan hasil override

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import site_data as d  # noqa: E402

OUT = ROOT / "data" / "content.json"

LISTS = {
    "stats": d.STATS,
    "advantages": d.ADVANTAGES,
    "scheme_cats": d.SCHEME_CATS,
    "schemes": d.SCHEMES,
    "hero_roles": d.HERO_ROLES,
    "ticker_items": d.TICKER_ITEMS,
    "steps": d.STEPS,
    "testimonials": d.TESTIMONIALS,
    "asesor": d.ASESOR,
    "tuk": d.TUK,
    "jadwal": d.JADWAL,
    "faq": d.FAQ,
    "posts": d.POSTS,
    "values": d.VALUES,
    "struktur": d.STRUKTUR,
}


def build_payload() -> dict:
    payload = {
        "site": dict(d.SITE),
        "pages": [
            {"file": f, "slug": slug, "title": title, "description": desc, "crumb": crumb}
            for f, slug, title, desc, crumb in d.PAGES
        ],
    }
    payload.update(LISTS)
    return payload


def main() -> None:
    payload = build_payload()
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    if "--check" in sys.argv:
        current = OUT.read_text(encoding="utf-8") if OUT.is_file() else ""
        print("sama" if current == text else "berbeda")
        return

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    total = sum(len(v) for k, v in payload.items() if isinstance(v, list))
    print(f"✓ {OUT.relative_to(ROOT)} — {len(payload['pages'])} halaman, "
          f"{total} entri daftar, {len(payload['site'])} field identitas")


if __name__ == "__main__":
    main()
