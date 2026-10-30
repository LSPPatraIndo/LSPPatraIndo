"use strict";

const crypto = require("node:crypto");

const CONTENT_PATH = "data/content.json";
const LISTS = [
  "stats", "advantages", "scheme_cats", "schemes", "hero_roles", "ticker_items",
  "steps", "testimonials", "asesor", "tuk", "jadwal", "faq", "posts", "values",
  "struktur",
];
const ALLOWED_KEYS = new Set(["site", "pages", "page_html", ...LISTS]);
const MAX_BODY = 600_000;
const MAX_UPLOAD = 7_500_000;
const attempts = new Map();

function env(name, fallback) {
  return process.env[name] || fallback || "";
}

function adminUser() { return env("ADMIN_USER", "lsppatraindo"); }
function adminPass() { return env("ADMIN_PASS", "adminlsppatraindo"); }

function configured() {
  return Boolean(process.env.GITHUB_TOKEN && process.env.GITHUB_REPO && process.env.SESSION_SECRET);
}

function sha256(text) {
  return crypto.createHash("sha256").update(String(text), "utf8").digest("hex");
}

function b64url(buffer) {
  return Buffer.from(buffer).toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function fromB64url(text) {
  const pad = text.length % 4 ? "=".repeat(4 - (text.length % 4)) : "";
  return Buffer.from(text.replace(/-/g, "+").replace(/_/g, "/") + pad, "base64");
}

function signToken() {
  const hours = Number(env("SESSION_HOURS", "12"));
  const exp = Date.now() + hours * 3600_000;
  const payload = b64url(Buffer.from(JSON.stringify({ u: adminUser(), exp }), "utf8"));
  const sig = crypto.createHmac("sha256", env("SESSION_SECRET")).update(payload).digest();
  return { token: `${payload}.${b64url(sig)}`, exp };
}

function readToken(event) {
  const headers = event.headers || {};
  const header = headers.authorization || headers.Authorization || "";
  const token = String(header).replace(/^Bearer\s+/i, "").trim();
  if (!token || !token.includes(".")) return null;
  const [payload, sig] = token.split(".");
  try {
    const expected = crypto.createHmac("sha256", env("SESSION_SECRET")).update(payload).digest();
    const provided = fromB64url(sig);
    if (expected.length !== provided.length) return null;
    if (!crypto.timingSafeEqual(expected, provided)) return null;
    const data = JSON.parse(fromB64url(payload).toString("utf8"));
    if (!data || typeof data.exp !== "number" || data.exp < Date.now()) return null;
    return data;
  } catch {
    return null;
  }
}

function origins() {
  return env("ALLOWED_ORIGINS", "https://lsppatraindo.id,https://www.lsppatraindo.id,http://localhost:8080,http://127.0.0.1:8080")
    .split(",").map((s) => s.trim()).filter(Boolean);
}

function cors(event) {
  const headers = event.headers || {};
  const origin = headers.origin || headers.Origin || "";
  const list = origins();
  const allowed = !origin || list.includes(origin);
  return {
    "Access-Control-Allow-Origin": allowed ? (origin || list[0]) : list[0],
    "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
    "Access-Control-Allow-Headers": "Authorization, Content-Type",
    "Access-Control-Max-Age": "600",
    Vary: "Origin",
  };
}

function json(data, statusCode, headers) {
  return {
    statusCode: statusCode || 200,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...(headers || {}) },
    body: JSON.stringify(data),
  };
}

function parseBody(event) {
  const raw = event.isBase64Encoded ? Buffer.from(event.body || "", "base64").toString("utf8") : (event.body || "");
  try {
    return { raw, data: raw ? JSON.parse(raw) : {} };
  } catch {
    return { raw, data: null };
  }
}

function clientIp(event) {
  const h = event.headers || {};
  return h["x-nf-client-connection-ip"] || h["x-forwarded-for"] || "unknown";
}

function limited(ip) {
  const now = Date.now();
  const entry = attempts.get(ip);
  if (!entry || entry.until < now) return false;
  return entry.n >= 8;
}

function noteAttempt(ip) {
  const now = Date.now();
  const entry = attempts.get(ip);
  if (!entry || entry.until < now) attempts.set(ip, { n: 1, until: now + 600_000 });
  else entry.n += 1;
}

async function gh(path, init) {
  const opts = init || {};
  const res = await fetch(`https://api.github.com/repos/${env("GITHUB_REPO")}${path}`, {
    ...opts,
    headers: {
      Authorization: `Bearer ${env("GITHUB_TOKEN")}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "lsp-patra-admin-netlify",
      ...(opts.headers || {}),
    },
  });
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { raw: text.slice(0, 400) };
  }
  if (!res.ok) throw new Error(`GitHub ${opts.method || "GET"} ${path} → ${res.status} ${text.slice(0, 200)}`);
  return data;
}

async function readContent() {
  const file = await gh(`/contents/${CONTENT_PATH}?ref=${env("GITHUB_BRANCH", "main")}`);
  const text = Buffer.from(String(file.content || "").replace(/\n/g, ""), "base64").toString("utf8");
  return { content: JSON.parse(text), sha: file.sha };
}

function validate(content) {
  if (!content || typeof content !== "object" || Array.isArray(content)) return "Data harus berupa objek.";
  for (const key of Object.keys(content)) if (!ALLOWED_KEYS.has(key)) return `Bagian tidak dikenal: ${key}`;
  if (!content.site || typeof content.site !== "object") return "Bagian 'site' wajib ada.";
  if (!Array.isArray(content.pages) || !content.pages.length) return "Bagian 'pages' wajib berisi minimal satu halaman.";
  for (const key of LISTS) {
    if (content[key] !== undefined && !Array.isArray(content[key])) return `Bagian '${key}' harus berupa daftar.`;
  }
  if (content.page_html !== undefined && (typeof content.page_html !== "object" || Array.isArray(content.page_html))) {
    return "Bagian 'page_html' harus berupa objek.";
  }
  return null;
}

async function handle(kind, event) {
  const headers = cors(event);
  const method = event.httpMethod;

  if (method === "OPTIONS") return { statusCode: 204, headers };

  if (kind === "health") return json({ ok: true, configured: configured() }, 200, headers);

  if (kind === "login" && method === "POST") {
    if (!configured()) return json({ ok: false, error: "Backend belum dikonfigurasi." }, 500, headers);
    const ip = clientIp(event);
    if (limited(ip)) return json({ ok: false, error: "Terlalu banyak percobaan. Coba lagi 10 menit." }, 429, headers);

    const parsed = parseBody(event);
    if (!parsed.data) return json({ ok: false, error: "Data login tidak valid." }, 400, headers);
    const u = String(parsed.data.u || "").trim();
    const p = String(parsed.data.p || "");

    const userOk = crypto.timingSafeEqual(Buffer.from(sha256(u)), Buffer.from(sha256(adminUser())));
    const passOk = crypto.timingSafeEqual(Buffer.from(sha256(p)), Buffer.from(sha256(adminPass())));
    if (!userOk || !passOk) {
      noteAttempt(ip);
      await new Promise((r) => setTimeout(r, 350));
      return json({ ok: false, error: "Username atau kata sandi salah." }, 401, headers);
    }

    attempts.delete(ip);
    const { token, exp } = signToken();
    return json({ ok: true, token, exp, user: u }, 200, headers);
  }

  if (!configured()) return json({ ok: false, error: "Backend belum dikonfigurasi." }, 500, headers);
  const session = readToken(event);
  if (!session) return json({ ok: false, error: "Sesi tidak valid atau kedaluwarsa." }, 401, headers);

  try {
    if (kind === "content" && method === "GET") {
      const { content, sha } = await readContent();
      return json({ ok: true, content, sha }, 200, headers);
    }

    if (kind === "content" && method === "PUT") {
      const parsed = parseBody(event);
      if (!parsed.data) return json({ ok: false, error: "JSON tidak valid." }, 400, headers);
      if (Buffer.byteLength(parsed.raw, "utf8") > MAX_BODY) return json({ ok: false, error: "Data terlalu besar." }, 413, headers);
      const problem = validate(parsed.data.content);
      if (problem) return json({ ok: false, error: problem }, 422, headers);

      const current = await readContent();
      const pretty = JSON.stringify(parsed.data.content, null, 2) + "\n";
      const res = await gh(`/contents/${CONTENT_PATH}`, {
        method: "PUT",
        body: JSON.stringify({
          message: `admin: perbarui konten situs (${session.u})`,
          content: Buffer.from(pretty, "utf8").toString("base64"),
          sha: current.sha,
          branch: env("GITHUB_BRANCH", "main"),
        }),
      });
      return json({
        ok: true,
        commit: { sha: res.commit && res.commit.sha, url: res.commit && res.commit.html_url },
      }, 200, headers);
    }

    if (kind === "upload" && method === "POST") {
      const parsed = parseBody(event);
      if (!parsed.data) return json({ ok: false, error: "Data gambar tidak valid." }, 400, headers);
      if (Buffer.byteLength(parsed.raw, "utf8") > MAX_UPLOAD) return json({ ok: false, error: "Gambar terlalu besar (maks. 7 MB)." }, 413, headers);
      const match = /^data:image\/([a-zA-Z0-9.+-]+);base64,([\s\S]+)$/.exec(String(parsed.data.data || ""));
      if (!match) return json({ ok: false, error: "Format gambar tidak didukung." }, 422, headers);
      const type = match[1].toLowerCase();
      const ext = type === "jpeg" ? "jpg" : type === "svg+xml" ? "svg" : type.replace("+xml", "");
      if (!["jpg", "png", "webp", "gif", "svg"].includes(ext)) {
        return json({ ok: false, error: "Gunakan JPG, PNG, WebP, GIF, atau SVG." }, 422, headers);
      }
      const base = String(parsed.data.name || `berita-${Date.now()}`)
        .replace(/[^a-zA-Z0-9._-]/g, "-")
        .replace(new RegExp(`\\.${ext}$`), "")
        .slice(0, 80) || `berita-${Date.now()}`;
      const imagePath = `assets/img/uploads/${base}.${ext}`;
      const res = await gh(`/contents/${imagePath}`, {
        method: "PUT",
        body: JSON.stringify({
          message: `admin: unggah gambar berita (${session.u})`,
          content: match[2],
          branch: env("GITHUB_BRANCH", "main"),
        }),
      });
      return json({
        ok: true,
        path: imagePath,
        commit: { sha: res.commit && res.commit.sha, url: res.commit && res.commit.html_url },
      }, 200, headers);
    }

    if (kind === "status" && method === "GET") {
      const runs = await gh("/actions/runs?per_page=1");
      const run = (runs.workflow_runs || [])[0];
      return json({
        ok: true,
        run: run ? { status: run.status, conclusion: run.conclusion, url: run.html_url, sha: run.head_sha, updated_at: run.updated_at } : null,
      }, 200, headers);
    }

    return json({ ok: false, error: "Endpoint tidak ditemukan." }, 404, headers);
  } catch (err) {
    return json({ ok: false, error: String((err && err.message) || err).slice(0, 300) }, 502, headers);
  }
}

module.exports = { handle };
