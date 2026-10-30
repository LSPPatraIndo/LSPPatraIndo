# Website LSP Patra Indo

Situs statis profesional untuk **Lembaga Sertifikasi Profesi Patra Indo** (`lsppatraindo.id`).
Dibangun tanpa framework, tanpa database, dan tanpa proses build berantai — cukup unggah
folder ini ke hosting apa pun (cPanel, Netlify, Vercel, GitHub Pages).

---

## 1. Menjalankan secara lokal

```bash
cd LSPPATRA
python3 -m http.server 8080
```

Buka <http://localhost:8080>. Jangan membuka `index.html` langsung lewat `file://`
karena tautan memakai URL bersih berbasis folder (`tentang-kami/`).

---

## 2. Struktur proyek

```
LSPPATRA/
├── index.html                 ← hasil build (jangan diedit manual)
├── tentang-kami/index.html
├── skema-sertifikasi/index.html
├── alur-sertifikasi/index.html
├── persyaratan/index.html
├── daftar-asesor/index.html
├── tuk/index.html
├── jadwal/index.html
├── faq/index.html
├── berita/index.html
├── kontak/index.html
├── 404.html
├── sitemap.xml · robots.txt · site.webmanifest · .htaccess
├── CNAME                      ← lsppatraindo.id (custom domain GitHub Pages)
├── .nojekyll                  ← agar GitHub Pages tidak memproses Jekyll
├── DEPLOY.md                  ← panduan GitHub + DNS Hostinger
│
├── .github/workflows/deploy.yml  ← build otomatis + deploy GitHub Pages
├── data/pendaftar/            ← data formulir yang masuk ke GitHub (opsional)
│
├── assets/
│   ├── css/style.css          ← token desain, dasar, header, footer
│   ├── css/sections.css       ← hero, kartu, alur, testimoni, FAQ, berita
│   ├── css/pages.css          ← halaman dalam, formulir, tabel, responsif
│   ├── js/main.js             ← navigasi, animasi, filter, formulir
│   └── img/                   ← foto, favicon, ikon PWA, og-image
│
├── src/pages/*.html           ← ISI halaman (sumber yang diedit)
├── site_data.py               ← SEMUA data: kontak, skema, asesor, jadwal, FAQ
├── site_ui.py                 ← komponen header/footer/kartu + ikon SVG
├── build.py                   ← generator halaman + sitemap
├── tools/make_assets.py       ← generator favicon, ikon, og-image
└── tools/github-form-worker.js ← Worker penyimpan formulir ke GitHub (opsional)
```

### Alur kerja mengubah konten

1. Ubah data di `site_data.py` (kontak, skema, jadwal, asesor, FAQ, berita) atau
   markup di `src/pages/*.html`.
2. Jalankan:

```bash
python3 build.py
```

3. Hasilnya: seluruh `*.html`, `sitemap.xml`, `robots.txt`, `.htaccess` diperbarui.

> Jangan mengedit file `index.html` / `<halaman>/index.html` secara langsung —
> perubahan akan tertimpa saat build berikutnya.

---

## 3. ⚠️ Data yang WAJIB diganti sebelum online

Semua nilai contoh berikut **wajib** disesuaikan dengan data resmi lembaga.

| Data | Lokasi | Nilai saat ini (contoh) |
|---|---|---|
| Nomor telepon | `site_data.py` → `SITE["phone_display"]`, `phone_link` | `+62 812-3456-7890` |
| Nomor WhatsApp | `SITE["wa"]` | `6281234567890` |
| Email | `SITE["email"]`, `email_sertifikasi` | `info@lsppatraindo.id` |
| Alamat kantor | `SITE["address"]`, `city` | Gedung Patra Office Tower … |
| Titik peta | `SITE["maps_query"]` | `Patra Office Tower, Jl. Gatot Subroto, Jakarta Selatan` |
| Sosial media | `SITE["social"]` | `instagram.com/lsppatraindo` dll. |
| Jam layanan | `SITE["hours"]`, `hours_sat` | Senin–Jumat 08.00–17.00 |
| Login SIAPkerja | `SITE["login_url"]` | `https://siapkerja.kemnaker.go.id/` |
| Statistik | `STATS` | 23 skema, 40+ asesor, 3.500+ peserta, 150+ mitra |
| Daftar skema | `SCHEMES` | 23 skema contoh — **sesuaikan dengan skema yang benar-benar terlisensi** |
| Asesor | `ASESOR` | Nama & bidang contoh |
| Struktur pengurus | `STRUKTUR` | Nama & jabatan contoh |
| Jadwal | `JADWAL` | Tanggal Nov 2026 – Jan 2027 |
| TUK | `TUK` | 6 lokasi contoh |
| Testimoni | `TESTIMONIALS` | Testimoni contoh |

**Catatan penting:** nomor lisensi BNSP, kode skema, dan ruang lingkup sengaja tidak
dicantumkan sebagai angka tertentu agar tidak menimbulkan klaim yang belum terverifikasi.
Setelah data resmi tersedia, tambahkan pada bagian legalitas (`src/pages/tentang-kami.html`)
dan footer.

---

## 4. Deployment

> **Ringkas:** repo GitHub sudah terhubung (`origin` → `LSPPatraIndo/LSPPatraIndo`),
> penerbitan otomatis lewat GitHub Actions ke `lsppatraindo.id` (GitHub Pages).
> Langkah lengkap ada di **[DEPLOY.md](DEPLOY.md)** — push pertama, DNS Hostinger,
> custom domain, sampai formulir yang menyimpan data ke repo.

### a. cPanel / hosting Apache (XAMPP juga)

1. Jalankan `python3 build.py` untuk memastikan output terbaru.
2. Unggah **seluruh isi folder** ke `public_html/` (termasuk `.htaccess`).
3. Aktifkan SSL (Let's Encrypt) di cPanel.
4. `.htaccess` sudah mengatur: HTTPS, redirect `www` → non-`www`, kompresi, cache,
   serta header keamanan dasar.

### b. Netlify / Vercel

- Netlify: drag & drop folder proyek ke dashboard. Tidak perlu build command.
- Vercel: `vercel --prod` dari folder ini, framework preset **Other**.

### c. GitHub Pages

- Push ke repositori, aktifkan Pages pada branch `main` (root).
- URL bersih (`/tentang-kami/`) otomatis bekerja karena setiap halaman berupa folder
  dengan `index.html`.

### Setelah domain aktif

1. Arahkan DNS `lsppatraindo.id` dan `www` ke hosting.
2. Daftarkan situs di [Google Search Console](https://search.google.com/search-console),
   submit `https://lsppatraindo.id/sitemap.xml`.
3. Perbarui `SITE["url"]` bila domain final berbeda (memengaruhi canonical, sitemap, OG).

---

## 5. Fitur yang sudah tersedia

- **11 halaman** + halaman 404 kustom.
- **Desain responsif** (desktop, tablet, mobile) dengan menu drawer.
- **Animasi teks & interaksi:**
  - *Ticker* teks berjalan (marquee) di beranda, berhenti saat kursor diarahkan.
  - *Headline berputar* (efek mengetik) untuk 7 bidang sertifikasi di hero.
  - *Reveal per kata* pada judul halaman dan judul seksi saat masuk layar.
  - Penghitung angka statistik, sorotan kartu mengikuti kursor, progress bar gulir.
  - Pencarian skema instan + filter bidang + status kosong.
  - Semua animasi otomatis nonaktif bila pengguna mengaktifkan *reduce motion*.
- **Filter skema** per bidang + sinkronisasi hash (`/skema-sertifikasi/#spa`).
- **Formulir pendaftaran** yang mengirim ringkasan data ke WhatsApp admin
  (tanpa server/backend — mudah diganti ke Formspree/email).
- **SEO**: meta description unik, canonical, Open Graph/Twitter Card, JSON-LD
  (`EducationalOrganization`, `WebSite`, `BreadcrumbList`, `FAQPage`, `ItemList`),
  sitemap.xml, robots.txt.
- **Aksesibilitas**: skip link, landmark, fokus terlihat, kontras WCAG AA
  (lolos audit axe pada seluruh halaman), `prefers-reduced-motion`.
- **Performa**: gambar lokal terkompresi, `loading="lazy"`, tanpa library eksternal
  selain font Google (dengan fallback sistem).
- **PWA ringan**: manifest + ikon 192/512.

---

## 6. Catatan pengembangan lanjutan

- **Halaman detail berita** belum dibuat. Saat ini kartu berita mengarah ke `/berita/`.
  Untuk menambah artikel, buat halaman baru dan tambahkan ke `PAGES` di `build.py`.
- **Formulir** bekerja via `wa.me`. Bila ingin data masuk ke email/Google Sheets,
  ganti handler di `assets/js/main.js` (bagian `data-wa-form`).
- **Gambar** berasal dari Unsplash (lisensi bebas pakai). Ganti dengan foto asli
  kegiatan lembaga di `assets/img/photos/` dengan nama file yang sama, atau
  perbarui referensinya di `src/pages/` dan `site_data.py`.
- **Menambah skema**: tambah entri pada `SCHEMES` (dan `SCHEME_CATS` bila bidang baru),
  lalu jalankan `python3 build.py`.
- **Regenerasi aset brand** (bila logo berubah):

```bash
python3 tools/make_assets.py
```

---

## 7. Mengatur teks bergerak & animasi

| Ingin mengubah | Lokasi |
|---|---|
| Kata yang berputar di hero | `site_data.py` → `HERO_ROLES` |
| Teks ticker berjalan | `site_data.py` → `TICKER_ITEMS` (tambahkan `"outline": True` untuk gaya teks garis) |
| Kecepatan ticker | `assets/css/motion.css` → `.ticker { --ticker-speed: 46s; }` |
| Kecepatan mengetik | `assets/js/main.js` bagian *9. Rotator* (`wait(52 + Math.random() * 46)`) |
| Judul yang dianimasikan per kata | tambahkan atribut `data-split` pada elemen judul |
| Elemen yang muncul saat digulir | tambahkan `data-reveal` (dan `data-reveal-group` pada pembungkus untuk efek berurutan) |

Mematikan seluruh animasi teks: hapus baris `<link ... motion.css>` di `build.py`
lalu jalankan ulang build, atau cukup andalkan pengaturan *reduce motion* pengguna.

---

## 8. Kredit

- Tipografi: [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) (SIL Open Font License).
- Foto: [Unsplash](https://unsplash.com) (Unsplash License).
- Ikon: SVG inline buatan sendiri (tanpa dependensi ikon eksternal).
