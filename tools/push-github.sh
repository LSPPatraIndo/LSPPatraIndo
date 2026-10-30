#!/usr/bin/env bash
# Push repo LSP Patra Indo ke GitHub dengan aman.
#
#   bash tools/push-github.sh
#
# Skrip ini:
#   1. meminta username + Personal Access Token (token tidak tampil di layar
#      dan tidak masuk riwayat Terminal),
#   2. memeriksa token benar-benar punya izin tulis ke repo,
#   3. menyimpan token ke Keychain macOS,
#   4. menjalankan git push ke branch main.
#
# Token TIDAK ditulis ke dalam berkas mana pun di repo ini.

set -uo pipefail

REPO="LSPPatraIndo/LSPPatraIndo"
BRANCH="main"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

bold() { printf "\033[1m%s\033[0m\n" "$*"; }
fail() { printf "\033[31m✗ %s\033[0m\n" "$*"; exit 1; }

json_field() { # $1=json $2=key
  python3 -c 'import json,sys
try:
    d = json.loads(sys.argv[1])
except Exception:
    print(""); raise SystemExit
v = d
for k in sys.argv[2].split("."):
    v = (v or {}).get(k) if isinstance(v, dict) else None
print("" if v is None else v)' "$1" "$2"
}

bold "== Push $REPO =="
echo "Gunakan akun yang punya akses tulis (pemilik org LSPPatraIndo)."
echo

read -r -p "Username GitHub : " GH_USER
read -r -s -p "Token (ghp_… / github_pat_…) : " GH_TOKEN
echo

[ -n "${GH_USER:-}" ] || fail "Username kosong."
[ -n "${GH_TOKEN:-}" ] || fail "Token kosong."

echo
echo "→ Memeriksa token…"
ME_JSON="$(curl -s -H "Authorization: Bearer $GH_TOKEN" https://api.github.com/user)"
ME="$(json_field "$ME_JSON" login)"
[ -n "$ME" ] || fail "Token tidak valid / kedaluwarsa. Buat token baru di https://github.com/settings/tokens"
echo "  token milik akun : $ME"

REPO_JSON="$(curl -s -H "Authorization: Bearer $GH_TOKEN" "https://api.github.com/repos/$REPO")"
CAN_PUSH="$(json_field "$REPO_JSON" permissions.push)"
if [ "$CAN_PUSH" != "True" ]; then
  cat <<EOF

✗ Akun "$ME" tidak punya izin tulis ke $REPO.

  Perbaiki dengan salah satu:
   • Login sebagai pemilik org di https://github.com/$REPO/settings/access
     lalu tambahkan "$ME" dengan role Write, ATAU
   • Buat token dari akun pemilik org (scope: repo, workflow, admin:org).

EOF
  exit 1
fi
echo "  izin tulis       : OK"

echo "→ Menyimpan kredensial ke Keychain…"
printf "protocol=https\nhost=github.com\nusername=%s\npassword=%s\n\n" "$GH_USER" "$GH_TOKEN" \
  | git credential-osxkeychain store || fail "Gagal menyimpan ke Keychain."

echo "→ Push ke origin/$BRANCH…"
GIT_TERMINAL_PROMPT=0 git push -u origin "$BRANCH" || fail "Push gagal. Jalankan ulang skrip ini."

echo
bold "✓ Selesai. Commit sudah ada di GitHub."
cat <<EOF

Langkah berikutnya (butuh akun pemilik org, di browser):
 1. https://github.com/$REPO/settings/pages
    Source → "GitHub Actions"
 2. Tab Actions → workflow "Build & Deploy ke GitHub Pages" → Run workflow
 3. Masih di Settings → Pages: Custom domain = lsppatraindo.id → Save,
    lalu centang "Enforce HTTPS" setelah DNS check hijau.

Setelah itu situs aktif di https://lsppatraindo.id
EOF
