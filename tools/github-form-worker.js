/**
 * Cloudflare Worker — penyimpan formulir pendaftaran ke GitHub.
 *
 * Setiap kiriman formulir disimpan sebagai satu berkas Markdown di
 * repositori: data/pendaftar/YYYYMMDD-HHmmss-nama.md
 * (opsional: sekaligus dibuatkan GitHub Issue sebagai notifikasi).
 *
 * Cara pakai singkat (detail di DEPLOY.md bagian 6):
 *   1. Buat fine-grained token GitHub: Contents = Read/Write,
 *      Issues = Read/Write, hanya untuk repo LSPPatraIndo/LSPPatraIndo.
 *   2. Cloudflare Dashboard → Workers & Pages → Create Worker → tempel berkas ini.
 *   3. Settings → Variables and Secrets, tambahkan:
 *        GITHUB_TOKEN   (secret)  token dari langkah 1
 *        GITHUB_REPO    "LSPPatraIndo/LSPPatraIndo"
 *        GITHUB_BRANCH  "main"
 *        ALLOWED_ORIGIN "https://lsppatraindo.id"
 *        CREATE_ISSUE   "1" (opsional)
 *   4. Deploy, lalu isi SITE["form_endpoint"] di site_data.py dengan URL Worker,
 *      jalankan `python3 build.py`, commit & push.
 */

const MAX = { nama: 120, telepon: 40, email: 160, skema: 160, pesan: 2000 };

function corsHeaders(request, env) {
  const origin = request.headers.get("Origin") || "";
  const allowed = (env.ALLOWED_ORIGIN || "https://lsppatraindo.id")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  const ok = allowed.includes("*") || allowed.includes(origin);
  return {
    "Access-Control-Allow-Origin": ok ? origin || allowed[0] : allowed[0],
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

function reply(request, env, body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
      ...corsHeaders(request, env),
    },
  });
}

function base64utf8(text) {
  const bytes = new TextEncoder().encode(text);
  let bin = "";
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin);
}

function clean(value, key) {
  return String(value ?? "")
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "")
    .trim()
    .slice(0, MAX[key] || 200);
}

function slug(text) {
  return (
    text
      .toLowerCase()
      .normalize("NFKD")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 40) || "pendaftar"
  );
}

function jakartaStamp(date) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Jakarta",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date);
  const get = (t) => parts.find((p) => p.type === t)?.value || "00";
  return {
    file: `${get("year")}${get("month")}${get("day")}-${get("hour")}${get("minute")}${get("second")}`,
    human: `${get("day")}/${get("month")}/${get("year")} ${get("hour")}:${get("minute")} WIB`,
  };
}

async function github(env, path, init = {}) {
  const res = await fetch(`https://api.github.com/repos/${env.GITHUB_REPO}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${env.GITHUB_TOKEN}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "lsp-patra-form-worker",
      ...(init.headers || {}),
    },
  });
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { raw: text };
  }
  if (!res.ok) {
    throw new Error(`GitHub ${init.method || "GET"} ${path} → ${res.status} ${text.slice(0, 300)}`);
  }
  return data;
}

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(request, env) });
    }
    if (request.method !== "POST") {
      return reply(request, env, { ok: false, error: "Gunakan POST." }, 405);
    }
    if (!env.GITHUB_TOKEN || !env.GITHUB_REPO) {
      return reply(request, env, { ok: false, error: "Worker belum dikonfigurasi." }, 500);
    }

    // Batasi ukuran badan permintaan.
    const raw = await request.text();
    if (raw.length > 12_000) {
      return reply(request, env, { ok: false, error: "Data terlalu besar." }, 413);
    }

    let input;
    try {
      input = JSON.parse(raw || "{}");
    } catch {
      return reply(request, env, { ok: false, error: "Format data tidak valid." }, 400);
    }

    // Honeypot: bot biasanya mengisi kolom tersembunyi.
    if (clean(input._gotcha, "nama")) {
      return reply(request, env, { ok: true, saved: false });
    }

    const data = {
      nama: clean(input.nama, "nama"),
      telepon: clean(input.telepon, "telepon"),
      email: clean(input.email, "email"),
      skema: clean(input.skema, "skema") || "Belum menentukan",
      pesan: clean(input.pesan, "pesan"),
    };

    if (!data.nama || !data.telepon || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(data.email)) {
      return reply(request, env, { ok: false, error: "Nama, WhatsApp, dan email wajib valid." }, 422);
    }

    const stamp = jakartaStamp(new Date());
    const branch = env.GITHUB_BRANCH || "main";
    const random = Math.random().toString(36).slice(2, 6);
    const file = `data/pendaftar/${stamp.file}-${slug(data.nama)}-${random}.md`;
    const ua = request.headers.get("User-Agent") || "-";

    const markdown = `# Pendaftaran — ${data.nama}

| Field | Nilai |
| --- | --- |
| Nama | ${data.nama} |
| WhatsApp | ${data.telepon} |
| Email | ${data.email} |
| Skema | ${data.skema} |
| Waktu | ${stamp.human} |
| Sumber | ${request.headers.get("Referer") || "-"} |
| Peramban | ${ua.slice(0, 160)} |

## Catatan peserta

${data.pesan || "_(kosong)_"}
`;

    await github(env, `/contents/${encodeURI(file)}`, {
      method: "PUT",
      body: JSON.stringify({
        message: `pendaftaran: ${data.nama} (${data.skema})`,
        content: base64utf8(markdown),
        branch,
      }),
    });

    if (env.CREATE_ISSUE === "1" || env.CREATE_ISSUE === "true") {
      await github(env, "/issues", {
        method: "POST",
        body: JSON.stringify({
          title: `Pendaftaran baru: ${data.nama} — ${data.skema}`,
          body: markdown,
          labels: ["pendaftaran"],
        }),
      });
    }

    return reply(request, env, { ok: true, saved: true, file });
  },
};
