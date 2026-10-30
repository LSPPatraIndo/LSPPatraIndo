# Panduan Deploy — GitHub + Hostinger (`lsppatraindo.id`)

> **Status: sudah aktif.**
> - Repo: <https://github.com/LSPPatraIndo/LSPPatraIndo> (branch `main`)
> - Situs: <https://lsppatraindo.id> — GitHub Pages, Source **GitHub Actions**
> - Custom domain + **Enforce HTTPS** aktif (sertifikat Let's Encrypt untuk
>   `lsppatraindo.id` dan `www.lsppatraindo.id`)
> - DNS Hostinger: `A @` → 4 IP GitHub Pages, `CNAME www` → `lsppatindo.github.io`
>
> Bagian 1–4 di bawah adalah catatan prosesnya (sudah dijalankan). Untuk
> kegiatan sehari-hari cukup lihat **bagian 5** (mengubah data).

Alur akhirnya:

```
ubah site_data.py / src/pages  →  git push  →  GitHub Actions build  →  lsppatraindo.id
```

Tidak ada FTP manual, tidak ada unggah ulang: **GitHub menjadi satu-satunya
sumber data situs**.

---

## 1. Push pertama dari komputer ini

Repo lokal sudah disiapkan (`git init`, remote `origin`, commit awal).
Sisa satu hal: **kredensial**. GitHub tidak menerima kata sandi biasa,
gunakan *Personal Access Token* (PAT).

### 1a. Buat token

1. Buka <https://github.com/settings/tokens> → **Generate new token**.
   - Pilih **Fine-grained token** (disarankan):
     - *Repository access* → **Only select repositories** → `LSPPatraIndo/LSPPatraIndo`
     - *Permissions → Repository permissions* → **Contents: Read and write**
       (tambahkan **Issues: Read and write** bila memakai notifikasi formulir)
     - *Expiration*: 90 hari (catat tanggalnya)
   - Atau **Tokens (classic)** dengan centang `repo`.
2. Salin token (`github_pat_...` atau `ghp_...`) — hanya tampil sekali.

### 1b. Push

```bash
cd /Users/bigsur/Documents/DEEPSEEK/LSPPATRA
git push -u origin main
```

Saat diminta:
- `Username`: `LSPPatraIndo`
- `Password`: **tempel token**, bukan kata sandi akun.

Agar tidak ditanya berulang, simpan token (macOS):

```bash
git config --global credential.helper osxkeychain
```

Cek berhasil:

```bash
git log --oneline -1
git ls-remote --heads origin
```

---

## 2. Aktifkan GitHub Pages

1. Buka **Settings → Pages** di repo.
2. **Source**: pilih **GitHub Actions** (bukan “Deploy from a branch”).
3. Buka tab **Actions** → workflow **Build & Deploy ke GitHub Pages** →
   **Run workflow** (atau tunggu push berikutnya).
4. Setelah job *build* dan *deploy* hijau, halaman sementara tersedia di
   `https://lsppatindo.github.io/LSPPatraIndo/`.

Workflow (`.github/workflows/deploy.yml`) menjalankan `python3 build.py`
setiap push, jadi `index.html`, `sitemap.xml`, dan `robots.txt` selalu
dibangun ulang dari `site_data.py` + `src/pages/*.html`.

---

## 3. Arahkan domain Hostinger ke GitHub Pages

Di **hPanel Hostinger → Domains → `lsppatraindo.id` → DNS / Nameservers →
DNS Zone**, **hapus** record bawaan yang menunjuk ke parkir/website Hostinger
(biasanya `A @` ke IP Hostinger dan `CNAME www` ke `lsppatraindo.id`), lalu
tambahkan record berikut.

### Record wajib

| Type | Name | Value / Points to | TTL |
| --- | --- | --- | --- |
| A | `@` | `185.199.108.153` | 3600 |
| A | `@` | `185.199.109.153` | 3600 |
| A | `@` | `185.199.110.153` | 3600 |
| A | `@` | `185.199.111.153` | 3600 |
| CNAME | `www` | `lsppatindo.github.io` | 3600 |

### Opsional (IPv6)

| Type | Name | Value |
| --- | --- | --- |
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |

Catatan penting:

- `CNAME www` **tanpa** `https://` dan **tanpa** garis miring di akhir.
- Jangan membuat `CNAME www` ke domain sendiri (loop).
- Propagasi DNS umumnya 5–60 menit, maksimal 24 jam.

Cek dari terminal:

```bash
dig +short lsppatraindo.id A
dig +short www.lsppatraindo.id CNAME
```

Hasil `A` harus keempat IP `185.199.10x.153` dan `CNAME` ke
`lsppatindo.github.io.`.

---

## 4. Pasang domain kustom di GitHub

1. **Settings → Pages → Custom domain** → isi `lsppatraindo.id` → **Save**.
   (Berkas `CNAME` di repo sudah berisi domain ini.)
2. Tunggu pemeriksaan DNS hijau, lalu centang **Enforce HTTPS**.
   Sertifikat Let's Encrypt biasanya terbit dalam 15–60 menit setelah DNS benar.
3. Uji: `https://lsppatraindo.id`, `https://www.lsppatraindo.id`
   (otomatis dialihkan), dan `https://lsppatraindo.id/tentang-kami/`.

---

## 5. Alur kerja mengubah data (semua lewat GitHub)

### Cara A — langsung di GitHub (tanpa terminal)

1. Buka `site_data.py` di repo → ikon pensil (**Edit**).
2. Ubah data (telepon, WhatsApp, alamat, skema, asesor, jadwal, berita, FAQ).
3. **Commit changes** ke `main`.
4. Workflow berjalan otomatis ±1 menit, situs terbarui.

### Cara B — dari komputer

```bash
cd /Users/bigsur/Documents/DEEPSEEK/LSPPATRA
# edit site_data.py atau src/pages/*.html
python3 build.py          # pratinjau lokal: python3 -m http.server 8080
git add -A
git commit -m "update data jadwal & kontak"
git push
```

**Aturan:** jangan mengedit `index.html` / `<halaman>/index.html` langsung —
file itu hasil build dan akan tertimpa. Edit sumbernya:
`site_data.py` (data) dan `src/pages/*.html` (markup).

---

## 6. Opsional — formulir pendaftaran masuk ke GitHub

Saat ini formulir mengirim ringkasan ke WhatsApp admin. Bila data pendaftar
juga harus **tersimpan di repositori**, aktifkan Worker berikut (gratis).

1. **Buat token** (fine-grained, repo `LSPPatraIndo/LSPPatraIndo`):
   - Contents: **Read and write**
   - Issues: **Read and write** (opsional, untuk notifikasi)
2. **Cloudflare** → <https://dash.cloudflare.com> → **Workers & Pages** →
   **Create** → **Worker** → beri nama `lsp-form` → **Deploy**.
3. **Edit code** → tempel seluruh isi `tools/github-form-worker.js` → **Deploy**.
4. **Settings → Variables and Secrets**:

   | Nama | Jenis | Nilai |
   | --- | --- | --- |
   | `GITHUB_TOKEN` | Secret | token langkah 1 |
   | `GITHUB_REPO` | Text | `LSPPatraIndo/LSPPatraIndo` |
   | `GITHUB_BRANCH` | Text | `main` |
   | `ALLOWED_ORIGIN` | Text | `https://lsppatraindo.id` |
   | `CREATE_ISSUE` | Text | `1` (opsional) |

5. Salin URL Worker, mis. `https://lsp-form.<akun>.workers.dev`.
6. Isi di `site_data.py`:

   ```python
   "form_endpoint": "https://lsp-form.<akun>.workers.dev",
   ```

7. `python3 build.py` → commit → push.

Hasil: setiap kiriman formulir membuat berkas baru di
`data/pendaftar/YYYYMMDD-HHmmss-nama-xxxx.md` (dan Issue berlabel
`pendaftaran` bila `CREATE_ISSUE=1`). WhatsApp tetap terbuka seperti biasa.

Rekomendasi keamanan tambahan: aktifkan **Turnstile** atau rate limit pada
Worker bila formulir mulai menerima spam.

---

## 7. Panel admin (`/admin/`)

Panel untuk mengubah **seluruh data situs** tanpa menyentuh kode. Setiap
penyimpanan membuat commit ke `data/content.json`, lalu GitHub Actions
membangun ulang halaman sehingga perubahan terbit di `lsppatraindo.id` dalam
±1 menit.

### Cara membuka

| Cara | Keterangan |
| --- | --- |
| Ikon kunci kecil di footer | Tampil samar (opasitas 0,28), menguat saat kursor diarahkan |
| Langsung | <https://lsppatraindo.id/admin/> |
| Pintasan | `Ctrl`/`Cmd` + `Shift` + `A` di halaman mana pun |

Halaman admin memakai `noindex, nofollow`, tidak ada di `sitemap.xml`, dan tidak
ditautkan dari menu utama.

### Apa yang bisa diedit

Identitas & kontak, media sosial, judul + meta description tiap halaman,
statistik, keunggulan, teks berputar hero, ticker, skema + kategori bidang,
alur sertifikasi, jadwal, asesor, TUK, FAQ, berita, testimoni, nilai lembaga,
dan struktur organisasi.

> Teks naratif juga bisa diubah dari menu **Teks Halaman (HTML)**, atau lewat
> `src/pages/*.html` seperti biasa.

### Login

Username panel: `lsppatraindo`. Kata sandi hanya disimpan sebagai secret
`ADMIN_PASS` di backend (tidak ditulis di HTML maupun repositori).

> **Penting:** backend Netlify sudah aktif dan dapat menerbitkan perubahan.
> Gunakan kata sandi yang kuat dan jaga kerahasiaan tautan `/admin/`.

1. **Login lokal (langsung aktif)** — username + kata sandi diverifikasi di
   peramban memakai hash SHA-256. Perubahan disimpan di `localStorage`
   peramban tersebut. Cocok untuk menyiapkan konten sebelum terbit.
2. **SSO backend (aktif)** — username + kata sandi diperiksa server Netlify
   Functions; kata sandi tidak pernah dikirim ke pengunjung. Backend memakai
   kredensial yang sama dan menerbitkan perubahan ke GitHub.
3. **Token GitHub** — fine-grained token (Contents: RW) untuk menerbitkan
   perubahan dari mode lokal. Token hanya ada di `sessionStorage` tab dan
   hilang saat tab ditutup.

### Berita + gambar

Menu **Berita** punya tombol **Tambah berita**. Setiap berita dapat memakai
gambar bawaan (ketik nama seperti `train`) atau **pilih file dari perangkat**
(JPG/PNG/WebP/GIF). Gambar otomatis diperkecil, lalu diunggah ke
`assets/img/uploads/` saat disimpan/diterbitkan. Di mode lokal gambar disimpan
sebagai data URL di peramban; saat GitHub dihubungkan, gambar ikut diunggah.

### Teks halaman

Menu **Teks Halaman (HTML)** memuat markup tiap halaman. Kosongkan kotak lalu
simpan untuk kembali ke sumber `src/pages/*.html`. Pertahankan placeholder
seperti `{{BASE}}` dan `{{POSTS_ALL}}` agar komponen dinamis tetap bekerja.

### 7a. Backend panel admin (Netlify Functions — sudah aktif)

Backend yang dipakai situs saat ini:

- Situs Netlify: <https://lsp-patra-indo-admin.netlify.app>
- Basis API: `https://lsp-patra-indo-admin.netlify.app/.netlify/functions`
- Kode: `netlify/functions/*.js` (login, content, upload, status, health)
- `SITE["admin_api"]` di `site_data.py` sudah diarahkan ke basis API tersebut.

Endpoint: `POST /login`, `GET/PUT /content`, `POST /upload`, `GET /status`,
`GET /health`. Token GitHub hanya disimpan sebagai **secret Netlify**, tidak
pernah dikirim ke peramban.

Untuk mengubah/menyegarkan backend:

```bash
netlify deploy --prod --dir netlify/public --functions netlify/functions
```

Environment variables di Netlify (Site configuration → Environment variables):

| Nama | Nilai |
| --- | --- |
| `ADMIN_USER` | `lsppatraindo` |
| `ADMIN_PASS` | kata sandi panel (secret) |
| `SESSION_SECRET` | teks acak panjang |
| `GITHUB_TOKEN` | fine-grained token (Contents: RW, Actions: Read) |
| `GITHUB_REPO` | `LSPPatraIndo/LSPPatraIndo` |
| `GITHUB_BRANCH` | `main` |
| `ALLOWED_ORIGINS` | `https://lsppatraindo.id,https://www.lsppatraindo.id` |

### 7b. Alternatif: Cloudflare Worker

Kode `tools/admin-worker.js` tetap disediakan bila ingin pindah ke Cloudflare.

1. Buat **fine-grained token** GitHub untuk repo ini:
   - *Contents*: **Read and write**
   - *Actions*: **Read-only** (untuk menampilkan status build)
2. Buka <https://dash.cloudflare.com> → **Workers & Pages** → **Create** →
   **Worker** → nama `lsp-admin` → **Deploy**.
3. **Edit code** → tempel seluruh isi `tools/admin-worker.js` → **Deploy**.
4. **Settings → Variables and Secrets**:

   | Nama | Jenis | Nilai |
   | --- | --- | --- |
   | `ADMIN_USER` | Text | `lsppatraindo` (default bila kosong) |
   | `ADMIN_PASS` | **Secret** | kata sandi panel (wajib) |
   | `SESSION_SECRET` | **Secret** | teks acak panjang, mis. hasil `openssl rand -hex 32` |
   | `GITHUB_TOKEN` | **Secret** | token langkah 1 |
   | `GITHUB_REPO` | Text | `LSPPatraIndo/LSPPatraIndo` |
   | `GITHUB_BRANCH` | Text | `main` |
   | `ALLOWED_ORIGINS` | Text | `https://lsppatraindo.id,https://www.lsppatraindo.id` |
   | `SESSION_HOURS` | Text | `12` |

5. Salin URL Worker, mis. `https://lsp-admin.<akun>.workers.dev`.
6. Isi di `site_data.py`:

   ```python
   "admin_api": "https://lsp-admin.<akun>.workers.dev",
   ```

7. `python3 build.py` → commit → push. Buka `/admin/` dan masuk.

### 7c. Keamanan yang sudah diterapkan

- Kata sandi hanya ada di **secret backend**, tidak di HTML.
- Perbandingan kata sandi memakai hash SHA-256 + waktu respons disamakan.
- Token sesi ditandatangani **HMAC-SHA256**, berlaku 12 jam, disimpan di
  `sessionStorage` (hilang saat tab ditutup).
- Pembatasan 8 percobaan login per 10 menit per IP.
- `PUT /content` memvalidasi struktur data, ukuran maksimum 600 KB, dan hanya
  menerima kunci yang dikenal.
- `POST /upload` membatasi gambar maksimum 8 MB dan hanya menerima tipe gambar
  yang diizinkan; nama berkas dibersihkan sebelum disimpan.
- CORS dibatasi ke domain resmi.

Tetap disarankan: ganti kata sandi panel secara berkala, aktifkan 2FA pada akun
GitHub/Netlify, dan jangan bagikan tautan `/admin/`.

---

## 8. Jika memilih hosting Hostinger (cPanel), bukan GitHub Pages

Repo tetap dipakai sebagai sumber data; hanya penerbitannya yang berbeda:

- **Cara cepat**: jalankan `python3 build.py`, lalu unggah seluruh isi folder
  ke `public_html/` lewat File Manager/FTP. `.htaccess` ikut terunggah dan
  mengatur HTTPS, `www` → non-`www`, kompresi, serta cache.
- **Otomatis**: hPanel → **Advanced → GIT** → *Deploy from GitHub* →
  repo `LSPPatraIndo/LSPPatraIndo`, branch `main`. Tambahkan perintah build
  `python3 build.py` bila Python tersedia di hosting; jika tidak, commit hasil
  build (file HTML) agar ikut ter-deploy.
- **Opsional (FTP)**: gunakan GitHub Actions dengan
  [`SamKirkland/FTP-Deploy-Action`](https://github.com/SamKirkland/FTP-Deploy-Action)
  dan simpan kredensial FTP di **Settings → Secrets and variables → Actions**.
- Pada opsi ini, **jangan** pasang custom domain di GitHub Pages; arahkan DNS
  `A @` ke IP Hostinger dan `CNAME www` ke `lsppatraindo.id`.

---

## 9. Pemecahan masalah

| Gejala | Penyebab & solusi |
| --- | --- |
| `remote: Permission to ... denied to <user>` | Akun yang tersimpan di Keychain tidak punya akses tulis. Tambahkan akun itu sebagai member/collaborator **Write**, atau hapus kredensial lama: `printf "protocol=https\nhost=github.com\n\n" \| git credential-osxkeychain erase` lalu push ulang dengan token akun yang berhak. |
| `git push` → `Authentication failed` | Gunakan PAT sebagai *password*, bukan kata sandi akun. |
| `remote: Permission denied` | Token tidak punya akses ke repo; buat ulang dengan scope `repo` / Contents RW. |
| Actions gagal di langkah build | Cek tab **Actions** → log; biasanya ada salah sintaks di `site_data.py`. Uji lokal: `python3 build.py`. |
| Pages 404 setelah deploy | **Settings → Pages → Source** harus **GitHub Actions**, bukan branch. |
| Domain “DNS check unsuccessful” | Record `A @` belum lengkap / masih ada record parkir Hostinger. Tunggu propagasi, cek `dig`. |
| HTTPS tidak bisa dicentang | Tunggu sertifikat terbit (hingga 24 jam), pastikan `www` CNAME benar. |
| Situs tampil tanpa CSS | Build tidak jalan; pastikan folder `assets/` ikut ter-commit (`git status`). |
| Halaman baru 404 | Pastikan `<slug>/index.html` ada atau jalankan `python3 build.py`. |
| Formulir tidak tersimpan | `SITE["form_endpoint"]` kosong, Worker belum di-deploy, atau `ALLOWED_ORIGIN` tidak cocok dengan domain. |
| Panel admin: “Backend admin belum diatur” | Normal bila `SITE["admin_api"]` kosong — login lokal tetap bekerja; sambungkan token GitHub atau deploy Worker untuk terbit langsung. |
| Panel admin: login selalu “username atau kata sandi salah” | Cek `ADMIN_USER`/`ADMIN_PASS` di Worker, atau terkena batas 8 percobaan/10 menit. |
| Panel admin: “Sesi berakhir” | Token HMAC kedaluwarsa (12 jam) atau `SESSION_SECRET` berubah — masuk ulang. |
| Panel admin: simpan gagal 422 | Struktur JSON tidak valid (mis. `pages` kosong). Muat ulang lalu ulangi perubahan. |
| Panel admin: simpan gagal 409 | `data/content.json` berubah di tempat lain; klik **Muat ulang** lalu simpan lagi. |
| Perubahan tersimpan tapi situs belum berubah | Tunggu ±1 menit; cek tab **Actions** bila build gagal. |
