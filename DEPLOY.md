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

## 7. Jika memilih hosting Hostinger (cPanel), bukan GitHub Pages

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

## 8. Pemecahan masalah

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
