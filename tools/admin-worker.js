/**
 * Cloudflare Worker — backend panel admin LSP Patra Indo.
 *
 * Login SSO (username + password) diperiksa DI SINI, bukan di browser, sehingga
 * kata sandi tidak pernah ikut terkirim ke pengunjung. Setelah login, Worker
 * membaca dan menulis data/content.json di repositori GitHub. Commit tersebut
 * memicu GitHub Actions yang membangun ulang situs dalam ±1 menit.
 *
 * Environment variables (Settings → Variables and Secrets):
 *   ADMIN_USER      lsppatraindo              (boleh Text)
 *   ADMIN_PASS      b@tam2026                 (WAJIB Secret)
 *   SESSION_SECRET  kalimat acak panjang      (WAJIB Secret)
 *   GITHUB_TOKEN    fine-grained PAT          (WAJIB Secret)
 *                   → Contents: Read and write, Actions: Read-only
 *   GITHUB_REPO     LSPPatraIndo/LSPPatraIndo
 *   GITHUB_BRANCH   main
 *   ALLOWED_ORIGINS https://lsppatraindo.id,https://www.lsppatraindo.id
 *   SESSION_HOURS   12
 *
 * Endpoint:
 *   POST /login    {u, p}        → {ok, token, exp}
 *   GET  /content                → {ok, content, sha}
 *   PUT  /content  {content}     → {ok, commit:{sha, url}}
 *   GET  /status                 → {ok, run:{...}}
 *   GET  /health                 → {ok, configured}
 */

const CONTENT_PATH = "data/content.json";
const LISTS = [
  "stats", "advantages", "scheme_cats", "schemes", "hero_roles", "ticker_items",
  "steps", "testimonials", "asesor", "tuk", "jadwal", "faq", "posts", "values",
  "struktur",
];
const ALLOWED_KEYS = new Set(["site", "pages", ...LISTS]);
const MAX_BODY = 600_000;

const enc = new TextEncoder();
const attempts = new Map(); // ip → { n, until }

/* ---------------------------------------------------------------- utilitas */

function b64urlFromBytes(bytes) {
  let bin = "";
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function bytesFromB64url(text) {
  const pad = text.length % 4 ? "=".repeat(4 - (text.length % 4)) : "";
  const bin = atob(text.replace(/-/g, "+").replace(/_/g, "/") + pad);
  return Uint8Array.from(bin, (c) => c.charCodeAt(0));
}

async function key(secret) {
  return crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign", "verify"]);
}

async function sha256(text) {
  const digest = await crypto.subtle.digest("SHA-256", enc.encode(text));
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function signToken(env) {
  const hours = Number(env.SESSION_HOURS || 12);
  const exp = Date.now() + hours * 3600_000;
  const payload = b64urlFromBytes(enc.encode(JSON.stringify({ u: env.ADMIN_USER || "admin", exp })));
  const sig = await crypto.subtle.sign("HMAC", await key(env.SESSION_SECRET), enc.encode(payload));
  return { token: `${payload}.${b64urlFromBytes(new Uint8Array(sig))}`, exp };
}

async function readToken(env, request) {
  const header = request.headers.get("Authorization") || "";
  const token = header.replace(/^Bearer\s+/i, "").trim();
  if (!token || !token.includes(".")) return null;
  const [payload, sig] = token.split(".");
  try {
    const ok = await crypto.subtle.verify("HMAC", await key(env.SESSION_SECRET), bytesFromB64url(sig), enc.encode(payload));
    if (!ok) return null;
    const data = JSON.parse(new TextDecoder().decode(bytesFromB64url(payload)));
    if (!data || typeof data.exp !== "number" || data.exp < Date.now()) return null;
    return data;
  } catch {
    return null;
  }
}

function allowedOrigins(env) {
  return (env.ALLOWED_ORIGINS || "https://lsppatraindo.id,https://www.lsppatraindo.id,http://localhost:8080,http://127.0.0.1:8080")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

function cors(request, env) {
  const origin = request.headers.get("Origin") || "";
  const list = allowedOrigins(env);
  const ok = !origin || list.includes(origin);
  return {
    "Access-Control-Allow-Origin": ok ? origin || list[0] : list[0],
    "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
    "Access-Control-Allow-Headers": "Authorization, Content-Type",
    "Access-Control-Max-Age": "600",
    Vary: "Origin",
  };
}

function send(request, env, data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...cors(request, env) },
  });
}

function clientIp(request) {
  return request.headers.get("CF-Connecting-IP") || request.headers.get("X-Forwarded-For") || "unknown";
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

function b64utf8(text) {
  const bytes = enc.encode(text);
  let bin = "";
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin);
}

/* -------------------------------------------------------------- GitHub API */

async function gh(env, path, init = {}) {
  const res = await fetch(`https://api.github.com/repos/${env.GITHUB_REPO}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${env.GITHUB_TOKEN}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "lsp-patra-admin",
      ...(init.headers || {}),
    },
  });
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { raw: text.slice(0, 400) };
  }
  if (!res.ok) throw new Error(`GitHub ${init.method || "GET"} ${path} → ${res.status} ${text.slice(0, 200)}`);
  return data;
}

async function readContent(env) {
  const file = await gh(env, `/contents/${CONTENT_PATH}?ref=${env.GITHUB_BRANCH || "main"}`);
  const bin = atob(String(file.content || "").replace(/\n/g, ""));
  const bytes = Uint8Array.from(bin, (c) => c.charCodeAt(0));
  return { content: JSON.parse(new TextDecoder().decode(bytes)), sha: file.sha, commit: file.commit && file.commit.sha };
}

function validate(content) {
  if (!content || typeof content !== "object" || Array.isArray(content)) return "Data harus berupa objek.";
  const keys = Object.keys(content);
  for (const k of keys) if (!ALLOWED_KEYS.has(k)) return `Bagian tidak dikenal: ${k}`;
  if (!content.site || typeof content.site !== "object") return "Bagian 'site' wajib ada.";
  if (!Array.isArray(content.pages) || !content.pages.length) return "Bagian 'pages' wajib berisi minimal satu halaman.";
  for (const listKey of LISTS) {
    if (content[listKey] !== undefined && !Array.isArray(content[listKey])) return `Bagian '${listKey}' harus berupa daftar.`;
  }
  return null;
}

/* ------------------------------------------------------------------ router */

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors(request, env) });
    }

    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "").replace(/^\/api/, "") || "/";
    const configured = Boolean(env.ADMIN_USER && env.ADMIN_PASS && env.GITHUB_TOKEN && env.GITHUB_REPO && env.SESSION_SECRET);

    if (path === "/health") return send(request, env, { ok: true, configured });

    if (path === "/login" && request.method === "POST") {
      if (!configured) return send(request, env, { ok: false, error: "Worker belum dikonfigurasi." }, 500);
      const ip = clientIp(request);
      if (limited(ip)) return send(request, env, { ok: false, error: "Terlalu banyak percobaan. Coba lagi 10 menit." }, 429);

      let body = {};
      try {
        body = await request.json();
      } catch {
        return send(request, env, { ok: false, error: "Data login tidak valid." }, 400);
      }
      const u = String(body.u || "").trim();
      const p = String(body.p || "");
      const [uOk, pOk] = await Promise.all([sha256(u), sha256(p)]);
      const [euOk, epOk] = await Promise.all([sha256(env.ADMIN_USER), sha256(env.ADMIN_PASS)]);

      let same = uOk.length === euOk.length;
      for (let i = 0; i < uOk.length; i += 1) if (uOk[i] !== euOk[i]) same = false;
      let samePass = pOk.length === epOk.length;
      for (let i = 0; i < pOk.length; i += 1) if (pOk[i] !== epOk[i]) samePass = false;

      if (!same || !samePass) {
        noteAttempt(ip);
        await new Promise((r) => setTimeout(r, 350));
        return send(request, env, { ok: false, error: "Username atau kata sandi salah." }, 401);
      }

      attempts.delete(ip);
      const { token, exp } = await signToken(env);
      return send(request, env, { ok: true, token, exp, user: u });
    }

    /* semua endpoint di bawah butuh sesi */
    if (!configured) return send(request, env, { ok: false, error: "Worker belum dikonfigurasi." }, 500);
    const session = await readToken(env, request);
    if (!session) return send(request, env, { ok: false, error: "Sesi tidak valid atau kedaluwarsa." }, 401);

    try {
      if (path === "/content" && request.method === "GET") {
        const { content, sha, commit } = await readContent(env);
        return send(request, env, { ok: true, content, sha, commit });
      }

      if (path === "/content" && request.method === "PUT") {
        const raw = await request.text();
        if (raw.length > MAX_BODY) return send(request, env, { ok: false, error: "Data terlalu besar." }, 413);
        let body;
        try {
          body = JSON.parse(raw);
        } catch {
          return send(request, env, { ok: false, error: "JSON tidak valid." }, 400);
        }
        const problem = validate(body.content);
        if (problem) return send(request, env, { ok: false, error: problem }, 422);

        const pretty = JSON.stringify(body.content, null, 2) + "\n";
        const current = await readContent(env);
        const res = await gh(env, `/contents/${CONTENT_PATH}`, {
          method: "PUT",
          body: JSON.stringify({
            message: `admin: perbarui konten situs (${session.u})`,
            content: b64utf8(pretty),
            sha: current.sha,
            branch: env.GITHUB_BRANCH || "main",
          }),
        });
        return send(request, env, {
          ok: true,
          commit: { sha: res.commit && res.commit.sha, url: res.commit && res.commit.html_url },
          deploy_url: `https://github.com/${env.GITHUB_REPO}/actions`,
        });
      }

      if (path === "/status" && request.method === "GET") {
        const runs = await gh(env, "/actions/runs?per_page=1");
        const run = (runs.workflow_runs || [])[0];
        return send(request, env, {
          ok: true,
          run: run
            ? { status: run.status, conclusion: run.conclusion, url: run.html_url, sha: run.head_sha, updated_at: run.updated_at }
            : null,
        });
      }

      return send(request, env, { ok: false, error: "Endpoint tidak ditemukan." }, 404);
    } catch (err) {
      return send(request, env, { ok: false, error: String((err && err.message) || err).slice(0, 300) }, 502);
    }
  },
};
