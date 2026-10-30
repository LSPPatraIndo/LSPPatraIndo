#!/usr/bin/env python3
"""Membuat aset brand LSP Patra Indo: favicon, ikon PWA, dan gambar OG.

Jalankan sekali:  python3 tools/make_assets.py
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
FONTS = Path(__file__).resolve().parent / "fonts"

NAVY_950 = (6, 26, 46)
NAVY_900 = (10, 33, 56)
NAVY_800 = (14, 43, 71)
TEAL = (19, 162, 150)
GOLD = (201, 162, 39)
GOLD_LIGHT = (228, 206, 147)
WHITE = (255, 255, 255)
SAND = (251, 248, 242)


def font(weight: int, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / f"PlusJakartaSans-{weight}.ttf"), size)


def vgrad(size, top, bottom):
    w, h = size
    img = Image.new("RGB", size)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img


def star_points(cx, cy, outer, inner, points=5, rotation=-90):
    pts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        a = math.radians(rotation + i * 180 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def rounded_gradient(size, radius, c1, c2):
    base = vgrad(size, c1, c2).convert("RGBA")
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    base.putalpha(mask)
    return base


def make_icon(size: int) -> Image.Image:
    pad = int(size * 0.04)
    inner = size - pad * 2
    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    tile = rounded_gradient((inner, inner), int(inner * 0.235), (26, 62, 96), NAVY_950)
    icon.alpha_composite(tile, (pad, pad))
    d = ImageDraw.Draw(icon)

    # cincin emas tipis
    d.ellipse(
        [pad + inner * 0.14, pad + inner * 0.14, pad + inner * 0.86, pad + inner * 0.86],
        outline=(201, 162, 39, 120),
        width=max(1, int(size * 0.008)),
    )
    d.polygon(star_points(size / 2, size / 2, inner * 0.30, inner * 0.125), fill=GOLD)
    return icon


def make_og() -> None:
    W, H = 1200, 630
    canvas = vgrad((W, H), (12, 41, 68), (6, 26, 46)).convert("RGBA")

    # Foto di sisi kanan
    photo = Image.open(IMG / "photos" / "hero.jpg").convert("RGB")
    target_w, target_h = 520, H
    ratio = max(target_w / photo.width, target_h / photo.height)
    photo = photo.resize((int(photo.width * ratio) + 1, int(photo.height * ratio) + 1), Image.LANCZOS)
    left = (photo.width - target_w) // 2
    top = (photo.height - target_h) // 2
    photo = photo.crop((left, top, left + target_w, top + target_h)).convert("RGBA")
    canvas.paste(photo, (W - target_w, 0))

    # Gradien agar foto menyatu dengan latar
    fade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fade)
    edge = W - target_w          # 680
    for x in range(0, edge + 320):
        if x <= edge - 150:
            a = 255
        else:
            a = int(255 * max(0.0, 1 - (x - (edge - 150)) / 470) ** 1.25)
        fd.line([(x, 0), (x, H)], fill=NAVY_950 + (min(255, a),))
    canvas = Image.alpha_composite(canvas, fade)

    # Overlay gelap di bawah foto
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for y in range(H):
        a = int(150 * (y / H) ** 2)
        sd.line([(0, y), (W, y)], fill=NAVY_950 + (a,))
    canvas = Image.alpha_composite(canvas, shade)

    # Pola grid halus
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, W, 68):
        gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 8))
    for y in range(0, H, 68):
        gd.line([(0, y), (W, y)], fill=(255, 255, 255, 8))
    canvas = Image.alpha_composite(canvas, grid)

    d = ImageDraw.Draw(canvas)

    # Logo
    mark = make_icon(74)
    canvas.alpha_composite(mark, (72, 54))
    d = ImageDraw.Draw(canvas)
    d.text((162, 58), "LSP PATRA INDO", font=font(800, 30), fill=WHITE)
    d.text((164, 96), "LEMBAGA SERTIFIKASI PROFESI", font=font(600, 13), fill=GOLD_LIGHT)

    # Judul
    d.text((72, 200), "Sertifikasi Kompetensi", font=font(800, 56), fill=WHITE)
    d.text((72, 264), "yang Diakui BNSP", font=font(800, 56), fill=GOLD_LIGHT)

    # Subjudul
    d.text((74, 352), "Perhotelan · Kuliner · SPA · MICE · Travel · Ekonomi Kreatif",
           font=font(500, 21), fill=(214, 226, 236))

    # Chip
    chips = ["Terlisensi BNSP", "Sertifikat diakui nasional", "Asesor bersertifikat"]
    x = 72
    for label in chips:
        f = font(600, 17)
        tw = d.textlength(label, font=f)
        w = int(tw) + 38
        d.rounded_rectangle([x, 418, x + w, 464], radius=23,
                            fill=(255, 255, 255, 26), outline=(255, 255, 255, 60), width=1)
        d.ellipse([x + 14, 435, x + 22, 443], fill=GOLD)
        d.text((x + 30, 430), label, font=f, fill=(238, 244, 249))
        x += w + 12

    # Domain
    d.line([(72, 524), (392, 524)], fill=(201, 162, 39, 150), width=2)
    d.text((72, 542), "lsppatraindo.id", font=font(600, 22), fill=GOLD_LIGHT)

    canvas.convert("RGB").save(IMG / "og-image.jpg", quality=91, optimize=True, progressive=True)
    print("  ✓ assets/img/og-image.jpg")


FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="LSP Patra Indo">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#1a3e60"/>
      <stop offset="1" stop-color="#061a2e"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="60" height="60" rx="15" fill="url(#g)"/>
  <circle cx="32" cy="32" r="23" fill="none" stroke="#c9a227" stroke-opacity=".45" stroke-width="1.5"/>
  <path d="M32 15.6l4.6 10.2 11.1 1.4-8.2 7.6 2.2 11-9.7-5.5-9.7 5.5 2.2-11-8.2-7.6 11.1-1.4z" fill="#c9a227"/>
</svg>
"""


def main() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    (IMG / "favicon.svg").write_text(FAVICON_SVG, encoding="utf-8")
    print("  ✓ assets/img/favicon.svg")

    make_icon(512).save(IMG / "icon-512.png", optimize=True)
    make_icon(192).save(IMG / "icon-192.png", optimize=True)
    make_icon(180).convert("RGB").save(IMG / "apple-touch-icon.png", optimize=True)
    print("  ✓ ikon 512 / 192 / apple-touch")

    make_og()


if __name__ == "__main__":
    main()
