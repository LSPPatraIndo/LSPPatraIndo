# Data pendaftar

Folder ini menampung data formulir pendaftaran yang dikirim dari halaman
`/kontak/`, bila fitur **formulir → GitHub** diaktifkan (lihat `DEPLOY.md`
bagian 6).

- Satu kiriman = satu berkas Markdown: `YYYYMMDD-HHmmss-nama-xxxx.md`
- Berkas dibuat otomatis oleh Cloudflare Worker (`tools/github-form-worker.js`)
  memakai GitHub API, langsung di branch `main`.
- Jangan menghapus folder ini; `.gitkeep` menjaga folder tetap ada di repo.

Tanpa Worker, formulir tetap berfungsi tetapi data hanya dikirim ke WhatsApp
admin dan tidak tersimpan di repositori.
