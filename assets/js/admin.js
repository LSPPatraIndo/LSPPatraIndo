/* Panel admin LSP Patra Indo — login, editor data situs, unggah gambar, simpan. */
(function () {
  'use strict';

  var meta = function (name) {
    var el = document.querySelector('meta[name="' + name + '"]');
    return el ? (el.getAttribute('content') || '').trim() : '';
  };

  var API = meta('lsp-admin-api').replace(/\/+$/, '');
  var REPO = meta('lsp-gh-repo') || 'LSPPatraIndo/LSPPatraIndo';
  var BRANCH = meta('lsp-gh-branch') || 'main';
  var CONTENT_PATH = 'data/content.json';
  var SESSION_KEY = 'lsp_admin_session';
  var LOCAL_CONTENT_KEY = 'lsp_admin_local_content_v1';
  var SOURCE_BASE = '../src/pages/';

  /* SHA-256 kredensial panel (username dan kata sandi). */
  var ADMIN_USER_HASH = '7512be04af304d77e53ced4b28de5c0e686ae347db30aa13a364d241b4a8f55f';
  var ADMIN_PASS_HASH = '58275838125cdb81a4b2632bca36e258c1e287a9901e228456637abfb94610af';

  var ICONS = ['shield', 'users', 'route', 'award', 'bed', 'cup', 'chef', 'spark', 'calendar',
    'globe', 'palette', 'scale', 'check-circle', 'lock', 'bolt', 'star', 'map-pin', 'phone',
    'mail', 'clock', 'arrow', 'briefcase'];

  var LABELS = {
    q: 'Pertanyaan', a: 'Jawaban', desc: 'Deskripsi', text: 'Teks', name: 'Nama',
    role: 'Jabatan / Peran', quote: 'Kutipan', initials: 'Inisial', tone: 'Warna kartu',
    field: 'Bidang keahlian', city: 'Kota', year: 'Tahun', cat: 'Kategori', level: 'Level KKNI',
    units: 'Jumlah unit', featured: 'Tampil di beranda', no: 'Nomor langkah', duration: 'Durasi',
    date: 'Tanggal', scheme: 'Skema', tuk: 'Lokasi TUK', mode: 'Metode', quota: 'Kuota',
    status: 'Status', title: 'Judul', image: 'Gambar berita', excerpt: 'Ringkasan',
    value: 'Angka', suffix: 'Akhiran', label: 'Label', note: 'Catatan', icon: 'Ikon',
    id: 'ID (huruf kecil)', outline: 'Gaya garis luar', address: 'Alamat', schemes: 'Jumlah skema',
    type: 'Jenis TUK', slug: 'Slug URL', description: 'Meta description', crumb: 'Nama breadcrumb',
    file: 'Berkas sumber', name_legal: 'Nama legal', domain: 'Domain', url: 'URL situs',
    tagline: 'Tagline', phone_display: 'Telepon (tampilan)', phone_link: 'Telepon (tautan)',
    wa: 'Nomor WhatsApp', email: 'Email utama', email_sertifikasi: 'Email sertifikasi',
    hours: 'Jam layanan', hours_sat: 'Jam layanan Sabtu', maps_query: 'Kueri peta',
    login_url: 'URL login SIAPkerja', founded: 'Tahun berdiri', form_endpoint: 'Endpoint formulir',
    admin_api: 'URL backend admin', github_repo: 'Repo GitHub', github_branch: 'Branch GitHub',
    instagram: 'Instagram', linkedin: 'LinkedIn', youtube: 'YouTube', facebook: 'Facebook',
    legal: 'Nama legal lengkap',
  };

  var SITE_HELP = {
    name: 'Nama pendek, dipakai di logo dan judul.',
    legal: 'Nama lengkap lembaga untuk footer dan data terstruktur.',
    domain: 'Domain tanpa https://',
    url: 'URL penuh dengan https:// (memengaruhi canonical, sitemap, OG).',
    wa: 'Format internasional tanpa tanda +, contoh 6281234567890.',
    phone_link: 'Untuk tautan tel:, contoh +6281234567890.',
    form_endpoint: 'URL Cloudflare Worker formulir (boleh kosong).',
    admin_api: 'URL backend panel admin (Netlify Functions/Worker). Jika kosong, panel memakai mode lokal + token GitHub.',
    github_repo: 'Format pemilik/repo.',
    github_branch: 'Branch yang dibangun GitHub Actions.',
    maps_query: 'Alamat yang dicari di Google Maps.',
  };

  var SELECTS = {
    'schemes.cat': function (c) { return (c.scheme_cats || []).map(function (x) { return x.id; }); },
    'jadwal.status': function () { return ['open', 'almost', 'wait']; },
    'advantages.icon': function () { return ICONS; },
    'values.icon': function () { return ICONS; },
    'scheme_cats.icon': function () { return ICONS; },
    'testimonials.tone': function () { return ['teal', 'gold', 'navy']; },
    'tuk.type': function () { return ['TUK Sewaktu', 'TUK Tempat Kerja', 'TUK Mandiri']; },
    'jadwal.mode': function () { return ['Offline', 'Online', 'Hybrid']; },
  };

  var SECTIONS = [
    { key: 'site', label: 'Identitas & Kontak', kind: 'object', help: 'Nama lembaga, telepon, WhatsApp, email, alamat, jam layanan, dan sosial media.' },
    { key: 'pages', label: 'Judul & SEO', kind: 'array', noAdd: true, fields: ['slug', 'title', 'description', 'crumb'], primary: 'slug', help: 'Judul tab peramban, meta description, dan nama breadcrumb tiap halaman.' },
    { key: 'page_html', label: 'Teks Halaman (HTML)', kind: 'page_html', help: 'Edit isi markup tiap halaman. Kosongkan untuk kembali ke berkas sumber src/pages/.' },
    { key: 'schemes', label: 'Skema Sertifikasi', kind: 'array', fields: ['name', 'cat', 'level', 'units', 'featured', 'desc'], primary: 'name', help: 'Daftar skema yang tampil di beranda dan halaman skema.' },
    { key: 'scheme_cats', label: 'Bidang Industri', kind: 'array', fields: ['id', 'label', 'icon', 'desc'], primary: 'label', help: 'Kategori/filter skema di halaman skema.' },
    { key: 'stats', label: 'Statistik', kind: 'array', fields: ['value', 'suffix', 'label', 'note'], primary: 'label', help: 'Angka penghitung di beranda.' },
    { key: 'advantages', label: 'Keunggulan', kind: 'array', fields: ['icon', 'title', 'text'], primary: 'title', help: 'Kartu keunggulan di beranda.' },
    { key: 'hero_roles', label: 'Teks Berputar', kind: 'lines', help: 'Satu bidang per baris; tampil berganti di hero beranda.' },
    { key: 'ticker_items', label: 'Ticker Berjalan', kind: 'array', fields: ['text', 'outline'], primary: 'text', help: 'Teks marquee di beranda. Centang "garis luar" untuk gaya outline.' },
    { key: 'steps', label: 'Alur Sertifikasi', kind: 'array', fields: ['no', 'title', 'duration', 'text'], primary: 'title', help: 'Lima langkah proses sertifikasi.' },
    { key: 'jadwal', label: 'Jadwal & Biaya', kind: 'array', fields: ['date', 'scheme', 'tuk', 'mode', 'quota', 'status'], primary: 'scheme', help: 'Jadwal uji kompetensi terdekat.' },
    { key: 'asesor', label: 'Daftar Asesor', kind: 'array', fields: ['name', 'initials', 'field', 'city', 'year'], primary: 'name', help: 'Asesor kompetensi beserta bidang dan kota.' },
    { key: 'tuk', label: 'Tempat Uji (TUK)', kind: 'array', fields: ['name', 'city', 'type', 'address', 'schemes'], primary: 'name', help: 'Lokasi TUK dan fasilitasnya.' },
    { key: 'faq', label: 'FAQ', kind: 'array', fields: ['q', 'a'], primary: 'q', help: 'Pertanyaan umum; juga dipakai data terstruktur Google.' },
    { key: 'posts', label: 'Berita', kind: 'array', fields: ['title', 'date', 'cat', 'image', 'excerpt'], primary: 'title', help: 'Kartu berita di beranda dan halaman berita. Gambar bisa dipilih langsung dari perangkat.' },
    { key: 'testimonials', label: 'Testimoni', kind: 'array', fields: ['name', 'role', 'quote', 'initials', 'tone'], primary: 'name', help: 'Testimoni peserta di beranda.' },
    { key: 'values', label: 'Nilai Lembaga', kind: 'array', fields: ['icon', 'title', 'text'], primary: 'title', help: 'Nilai integritas, independensi, dan lainnya.' },
    { key: 'struktur', label: 'Struktur Organisasi', kind: 'array', fields: ['role', 'name', 'initials', 'note'], primary: 'role', help: 'Susunan pengurus pada halaman tentang kami.' },
  ];

  var el = function (id) { return document.getElementById(id); };
  var state = {
    content: null, sha: null, mode: '', token: '', dirty: false,
    section: 'site', busy: false, deployTimer: null, pageSources: {}, fromLocal: false,
  };

  /* ------------------------------------------------------------- utilitas */

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function humanize(key) {
    if (LABELS[key]) return LABELS[key];
    return key.replace(/_/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
  }

  function toast(message, isError) {
    var box = el('toast');
    if (!box) return;
    var item = document.createElement('div');
    item.className = 'adm-toast__item' + (isError ? ' is-err' : '');
    item.textContent = message;
    box.appendChild(item);
    setTimeout(function () { item.remove(); }, isError ? 8000 : 4500);
  }

  function setSaveState(text, kind) {
    var node = el('save-state');
    if (!node) return;
    node.textContent = text;
    node.className = 'adm-savebar__state' + (kind ? ' is-' + kind : '');
  }

  function markDirty() {
    state.dirty = true;
    setSaveState('Ada perubahan belum disimpan', 'dirty');
  }

  function getPath(obj, path) {
    return path.split('.').reduce(function (acc, k) {
      return acc == null ? acc : acc[/^\d+$/.test(k) ? Number(k) : k];
    }, obj);
  }

  function setPath(obj, path, value) {
    var parts = path.split('.');
    var last = parts.pop();
    var target = parts.reduce(function (acc, k) {
      return acc[/^\d+$/.test(k) ? Number(k) : k];
    }, obj);
    target[/^\d+$/.test(last) ? Number(last) : last] = value;
  }

  function b64encode(text) {
    var bytes = new TextEncoder().encode(text);
    var bin = '';
    for (var i = 0; i < bytes.length; i += 1) bin += String.fromCharCode(bytes[i]);
    return btoa(bin);
  }

  function b64decode(text) {
    var bin = atob(String(text || '').replace(/\n/g, ''));
    var bytes = Uint8Array.from(bin, function (c) { return c.charCodeAt(0); });
    return new TextDecoder().decode(bytes);
  }

  function slugify(text) {
    return String(text || '').toLowerCase().normalize('NFKD')
      .replace(/[^\w\s-]/g, '').trim().replace(/\s+/g, '-').slice(0, 48) || 'berita';
  }

  async function sha256(text) {
    if (!window.crypto || !window.crypto.subtle) {
      throw new Error('Peramban tidak mendukung verifikasi aman. Buka situs lewat https:// atau localhost.');
    }
    var buf = await window.crypto.subtle.digest('SHA-256', new TextEncoder().encode(String(text)));
    return Array.prototype.map.call(new Uint8Array(buf), function (b) {
      return b.toString(16).padStart(2, '0');
    }).join('');
  }

  async function localCredentialsMatch(user, pass) {
    try {
      var values = await Promise.all([sha256(user), sha256(pass)]);
      var same = values[0].length === ADMIN_USER_HASH.length;
      for (var i = 0; i < values[0].length; i += 1) {
        if (values[0][i] !== ADMIN_USER_HASH[i]) same = false;
      }
      var passOk = values[1].length === ADMIN_PASS_HASH.length;
      for (var j = 0; j < values[1].length; j += 1) {
        if (values[1][j] !== ADMIN_PASS_HASH[j]) passOk = false;
      }
      return same && passOk;
    } catch (err) {
      return false;
    }
  }

  /* ------------------------------------------------------------ API layer */

  function session() {
    try {
      return JSON.parse(sessionStorage.getItem(SESSION_KEY) || 'null');
    } catch (err) {
      return null;
    }
  }

  function saveSession(data) {
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(data));
  }

  function clearSession() {
    sessionStorage.removeItem(SESSION_KEY);
  }

  async function workerCall(path, options) {
    var opts = options || {};
    var headers = { 'Content-Type': 'application/json' };
    if (state.token) headers.Authorization = 'Bearer ' + state.token;
    var res = await fetch(API + path, {
      method: opts.method || 'GET',
      headers: headers,
      body: opts.body ? JSON.stringify(opts.body) : undefined,
    });
    var data = null;
    try {
      data = await res.json();
    } catch (err) {
      data = { ok: false, error: 'Respons backend tidak dapat dibaca.' };
    }
    if (res.status === 401) {
      clearSession();
      showLogin('Sesi berakhir. Silakan masuk kembali.');
      throw new Error('Sesi berakhir.');
    }
    if (!res.ok || data.ok === false) throw new Error(data.error || ('Gagal (' + res.status + ')'));
    return data;
  }

  async function ghCall(path, options) {
    var opts = options || {};
    var headers = { Accept: 'application/vnd.github+json', Authorization: 'Bearer ' + state.token };
    var res = await fetch('https://api.github.com/repos/' + REPO + path, {
      method: opts.method || 'GET',
      headers: headers,
      body: opts.body ? JSON.stringify(opts.body) : undefined,
    });
    var data = null;
    try {
      data = await res.json();
    } catch (err) {
      data = { message: 'Respons GitHub tidak dapat dibaca.' };
    }
    if (!res.ok) throw new Error(data.message || ('GitHub error ' + res.status));
    return data;
  }

  function encodePath(path) {
    return path.split('/').map(encodeURIComponent).join('/');
  }

  async function loadContent() {
    if (state.mode === 'worker') {
      var res = await workerCall('/content');
      state.content = res.content;
      state.sha = res.sha;
      state.fromLocal = false;
      return;
    }
    if (state.mode === 'token') {
      var file = await ghCall('/contents/' + CONTENT_PATH + '?ref=' + encodeURIComponent(BRANCH));
      state.content = JSON.parse(b64decode(file.content));
      state.sha = file.sha;
      state.fromLocal = false;
      return;
    }

    var raw = null;
    try {
      raw = localStorage.getItem(LOCAL_CONTENT_KEY);
    } catch (err) {
      raw = null;
    }
    if (raw) {
      try {
        state.content = JSON.parse(raw);
        state.sha = null;
        state.fromLocal = true;
        return;
      } catch (err) {
        localStorage.removeItem(LOCAL_CONTENT_KEY);
      }
    }
    var response = await fetch('../data/content.json?t=' + Date.now(), { cache: 'no-store' });
    if (!response.ok) throw new Error('Data situs tidak dapat dimuat (' + response.status + ').');
    state.content = await response.json();
    state.sha = null;
    state.fromLocal = false;
  }

  async function refreshSha() {
    var file = await ghCall('/contents/' + CONTENT_PATH + '?ref=' + encodeURIComponent(BRANCH));
    state.sha = file.sha;
  }

  async function saveContent() {
    if (state.mode === 'worker') {
      await processImages();
      return workerCall('/content', { method: 'PUT', body: { content: state.content } });
    }
    if (state.mode === 'token') {
      await processImages();
      if (!state.sha) await refreshSha();
      var text = JSON.stringify(state.content, null, 2) + '\n';
      var res = await ghCall('/contents/' + CONTENT_PATH, {
        method: 'PUT',
        body: {
          message: 'admin: perbarui konten situs',
          content: b64encode(text),
          sha: state.sha,
          branch: BRANCH,
        },
      });
      return { ok: true, commit: { sha: res.commit.sha, url: res.commit.html_url } };
    }

    try {
      localStorage.setItem(LOCAL_CONTENT_KEY, JSON.stringify(state.content));
    } catch (err) {
      throw new Error('Penyimpanan peramban penuh. Hapus beberapa gambar berita atau unduh JSON lalu sambungkan GitHub.');
    }
    return { ok: true, local: true };
  }

  async function deployStatus() {
    if (state.mode === 'worker') {
      var res = await workerCall('/status');
      return res.run;
    }
    var runs = await ghCall('/actions/runs?per_page=1');
    var run = (runs.workflow_runs || [])[0];
    return run ? { status: run.status, conclusion: run.conclusion, url: run.html_url } : null;
  }

  /* --------------------------------------------------------------- gambar */

  function imageSrc(value) {
    var image = String(value == null ? '' : value).trim();
    if (!image) return '';
    if (/^(data:|https?:\/\/|\/\/|\/)/.test(image)) return image;
    if (image.indexOf('assets/') === 0) return '../' + image;
    return '../assets/img/photos/' + image + '.jpg';
  }

  function dataUrlInfo(dataUrl) {
    var match = /^data:image\/([a-zA-Z0-9.+-]+);base64,([\s\S]+)$/.exec(String(dataUrl || ''));
    if (!match) return null;
    var type = match[1].toLowerCase();
    var ext = type === 'jpeg' ? 'jpg' : type === 'svg+xml' ? 'svg' : type.replace('+xml', '');
    if (['jpg', 'png', 'webp', 'gif', 'svg'].indexOf(ext) === -1) return null;
    return { ext: ext, type: type, base64: match[2] };
  }

  function readFileAsDataUrl(file) {
    return new Promise(function (resolve, reject) {
      var reader = new FileReader();
      reader.onload = function () { resolve(String(reader.result || '')); };
      reader.onerror = function () { reject(new Error('File tidak dapat dibaca.')); };
      reader.readAsDataURL(file);
    });
  }

  function loadImage(src) {
    return new Promise(function (resolve, reject) {
      var img = new Image();
      img.onload = function () { resolve(img); };
      img.onerror = function () { reject(new Error('Gambar tidak dapat dibaca.')); };
      img.src = src;
    });
  }

  async function prepareImage(file) {
    if (!/^image\//.test(file.type)) throw new Error('Berkas harus berupa gambar (JPG, PNG, WebP, atau GIF).');
    if (file.size > 15 * 1024 * 1024) throw new Error('Ukuran gambar maksimal 15 MB.');
    var original = await readFileAsDataUrl(file);
    var img = await loadImage(original);
    var maxW = 1600;
    var maxH = 1200;
    var scale = Math.min(1, maxW / img.width, maxH / img.height);

    if (scale === 1 && file.size <= 450 * 1024 && file.type !== 'image/gif') return original;

    var canvas = document.createElement('canvas');
    canvas.width = Math.max(1, Math.round(img.width * scale));
    canvas.height = Math.max(1, Math.round(img.height * scale));
    var ctx = canvas.getContext('2d');
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg', 0.84);
  }

  async function uploadImage(dataUrl, title) {
    var info = dataUrlInfo(dataUrl);
    if (!info) throw new Error('Format gambar tidak didukung.');
    var name = slugify(title) + '-' + Date.now().toString(36) + '.' + info.ext;
    var path = 'assets/img/uploads/' + name;

    if (state.mode === 'worker') {
      var res = await workerCall('/upload', {
        method: 'POST',
        body: { name: name, data: dataUrl },
      });
      return res.path || path;
    }

    await ghCall('/contents/' + encodePath(path), {
      method: 'PUT',
      body: {
        message: 'admin: unggah gambar berita',
        content: info.base64,
        branch: BRANCH,
      },
    });
    return path;
  }

  async function processImages() {
    if (state.mode === 'local') return 0;
    var posts = state.content.posts || [];
    var uploaded = 0;
    for (var i = 0; i < posts.length; i += 1) {
      var image = String(posts[i].image || '');
      if (!/^data:image\//i.test(image)) continue;
      setSaveState('Mengunggah gambar berita ' + (i + 1) + '…');
      posts[i].image = await uploadImage(image, posts[i].title || 'berita');
      uploaded += 1;
    }
    return uploaded;
  }

  /* --------------------------------------------------------------- render */

  function currentSection() {
    for (var i = 0; i < SECTIONS.length; i += 1) if (SECTIONS[i].key === state.section) return SECTIONS[i];
    return SECTIONS[0];
  }

  function renderNav() {
    var nav = el('section-nav');
    nav.innerHTML = SECTIONS.map(function (section) {
      var value = state.content[section.key];
      var count = Array.isArray(value) ? value.length : '';
      return '<button type="button" class="adm-nav__btn' + (section.key === state.section ? ' is-active' : '') +
        '" data-section="' + section.key + '"><span>' + esc(section.label) + '</span>' +
        (count === '' ? '' : '<small>' + count + '</small>') + '</button>';
    }).join('');
  }

  function fieldControl(path, key, value, sectionKey, extraClass) {
    var cls = 'adm-field' + (extraClass ? ' ' + extraClass : '');
    var id = 'f_' + path.replace(/[^\w]/g, '_');
    var label = '<label for="' + id + '">' + esc(humanize(key)) + '</label>';
    var selectOptions = SELECTS[sectionKey + '.' + key];
    var hint = sectionKey === 'site' && SITE_HELP[key] ? '<span class="adm-hint">' + esc(SITE_HELP[key]) + '</span>' : '';

    if (typeof value === 'boolean') {
      return '<div class="' + cls + '"><label class="adm-check" for="' + id + '">' +
        '<input type="checkbox" id="' + id + '" data-path="' + path + '"' + (value ? ' checked' : '') + '>' +
        '<span>' + esc(humanize(key)) + '</span></label></div>';
    }

    if (selectOptions) {
      var options = selectOptions(state.content) || [];
      var current = String(value == null ? '' : value);
      if (options.indexOf(current) === -1) options = [current].concat(options);
      return '<div class="' + cls + '">' + label + '<select id="' + id + '" data-path="' + path + '">' +
        options.map(function (option) {
          return '<option value="' + esc(option) + '"' + (option === current ? ' selected' : '') + '>' +
            esc(option) + '</option>';
        }).join('') + '</select>' + hint + '</div>';
    }

    if (typeof value === 'number') {
      return '<div class="' + cls + '">' + label + '<input type="number" id="' + id + '" data-path="' + path +
        '" value="' + esc(value) + '">' + hint + '</div>';
    }

    var text = value == null ? '' : String(value);
    var long = ['description', 'desc', 'text', 'a', 'quote', 'excerpt', 'address', 'note'].indexOf(key) !== -1 || text.length > 90;
    if (long) {
      return '<div class="' + cls + ' adm-col--full">' + label + '<textarea id="' + id + '" data-path="' + path +
        '" rows="' + (text.length > 160 ? 6 : 3) + '">' + esc(text) + '</textarea>' + hint + '</div>';
    }
    var type = /^(https?:|mailto:)/.test(text) ? 'url' : 'text';
    var readonly = key === 'slug' || key === 'file' || key === 'id' ? ' readonly aria-readonly="true"' : '';
    return '<div class="' + cls + '">' + label + '<input type="' + type + '" id="' + id + '" data-path="' + path +
      '" value="' + esc(text) + '" spellcheck="false"' + readonly + '>' +
      (readonly && key === 'slug' ? '<span class="adm-hint">Slug dipakai sebagai URL halaman — jangan diubah.</span>' : hint) + '</div>';
  }

  function imageControl(path, value) {
    var image = value == null ? '' : String(value);
    var preview = imageSrc(image);
    var isData = /^data:image\//i.test(image);
    var pathField = isData
      ? '<input type="hidden" data-path="' + path + '" value="' + esc(image) + '">' +
        '<input type="text" class="adm-image-path" value="Gambar dipilih dari perangkat" disabled>'
      : '<input type="text" class="adm-image-path" data-path="' + path + '" value="' + esc(image) +
        '" spellcheck="false" placeholder="train atau assets/img/uploads/namafile.jpg">';

    return '<div class="adm-field adm-image-field adm-col--full">' +
      '<label>Gambar berita</label>' +
      '<div class="adm-image-row">' +
      '<img class="adm-image-preview" data-preview="' + esc(path) + '"' + (preview ? ' src="' + esc(preview) + '"' : '') + ' alt=""' +
      (preview ? '' : ' hidden') + '>' +
      '<div class="adm-image-side">' +
      '<input class="adm-file" type="file" accept="image/jpeg,image/png,image/webp,image/gif" data-image-input="' + esc(path) + '">' +
      '<button class="adm-btn adm-btn--danger adm-btn--sm adm-image-clear" type="button" data-image-clear="' + esc(path) + '">Hapus gambar</button>' +
      '<span class="adm-hint">Pilih file dari perangkat. Gambar otomatis diperkecil; saat disimpan, gambar diunggah ke repositori.</span>' +
      '</div></div>' +
      pathField +
      '<span class="adm-hint">Boleh juga memakai nama gambar bawaan (train, hotel, guide, about, fb, culinary) atau path <code>assets/img/uploads/…</code>.</span>' +
      '</div>';
  }

  function renderObjectSection(section) {
    var data = state.content[section.key] || {};
    var keys = Object.keys(data).filter(function (k) { return k !== 'social'; });
    var social = data.social && typeof data.social === 'object' ? data.social : null;

    var html = '<div class="adm-card"><div class="adm-card__head"><h3>Data lembaga</h3></div><div class="adm-row adm-row--3">' +
      keys.map(function (key) {
        var full = ['description', 'address', 'legal'].indexOf(key) !== -1 ? ' adm-col--full' : '';
        return fieldControl(section.key + '.' + key, key, data[key], section.key, full);
      }).join('') + '</div></div>';

    if (social) {
      html += '<div class="adm-card"><div class="adm-card__head"><h3>Media sosial</h3></div><div class="adm-row">' +
        Object.keys(social).map(function (key) {
          return fieldControl(section.key + '.social.' + key, key, social[key], section.key);
        }).join('') + '</div></div>';
    }
    return html;
  }

  function renderLinesSection(section) {
    var lines = (state.content[section.key] || []).join('\n');
    return '<div class="adm-card"><div class="adm-card__head"><h3>' + esc(section.label) +
      '</h3><span class="adm-card__handle">satu baris = satu entri</span></div>' +
      '<div class="adm-field"><textarea data-lines="' + section.key + '" rows="8">' + esc(lines) + '</textarea>' +
      '<span class="adm-hint">Kosongkan baris yang tidak dipakai.</span></div></div>';
  }

  function renderArraySection(section) {
    var list = state.content[section.key] || [];
    if (!list.length) {
      return '<div class="adm-card"><p class="adm-empty">Belum ada entri. Gunakan tombol <strong>Tambah entri</strong>.</p></div>';
    }
    var fields = section.fields || Object.keys(list[0] || {});
    return list.map(function (item, index) {
      var primary = section.primary ? item[section.primary] : '';
      var title = primary ? String(primary) : 'Entri #' + (index + 1);
      return '<article class="adm-card" data-index="' + index + '">' +
        '<div class="adm-card__head">' +
        '<span class="adm-badge">#' + (index + 1) + '</span>' +
        '<h3>' + esc(title.length > 70 ? title.slice(0, 70) + '…' : title) + '</h3>' +
        '<div class="adm-card__tools">' +
        '<button type="button" class="adm-btn adm-btn--ghost-dark adm-btn--sm" data-move="up" data-index="' + index + '" title="Naikkan">↑</button>' +
        '<button type="button" class="adm-btn adm-btn--ghost-dark adm-btn--sm" data-move="down" data-index="' + index + '" title="Turunkan">↓</button>' +
        '<button type="button" class="adm-btn adm-btn--ghost-dark adm-btn--sm" data-dup="' + index + '">Duplikat</button>' +
        '<button type="button" class="adm-btn adm-btn--danger adm-btn--sm" data-del="' + index + '">Hapus</button>' +
        '</div></div>' +
        '<div class="adm-row adm-row--3">' +
        fields.map(function (key) {
          if (section.key === 'posts' && key === 'image') {
            return imageControl(section.key + '.' + index + '.image', item.image);
          }
          var full = ['desc', 'text', 'a', 'quote', 'excerpt', 'address', 'note', 'description'].indexOf(key) !== -1 ? ' adm-col--full' : '';
          return fieldControl(section.key + '.' + index + '.' + key, key, item[key], section.key, full);
        }).join('') + '</div>' +
        (item.file ? '<input type="hidden" data-path="' + section.key + '.' + index + '.file" value="' + esc(item.file) + '">' : '') +
        '</article>';
    }).join('');
  }

  function renderPageHtmlSection(section) {
    var pages = state.content.pages || [];
    var overrides = state.content.page_html || {};
    var html = '<div class="adm-help-box"><strong>Mode lanjutan.</strong> Isi ini adalah markup halaman (tanpa header/footer). ' +
      'Pertahankan placeholder seperti <code>{{BASE}}</code>, <code>{{SCHEMES_ALL}}</code>, dan token lain agar komponen dinamis tetap bekerja. ' +
      'Kosongkan kotak lalu simpan untuk kembali memakai berkas sumber.</div>';

    html += pages.map(function (page) {
      var slug = String(page.slug == null ? '' : page.slug);
      var current = overrides[slug] || '';
      return '<div class="adm-card adm-page-body">' +
        '<div class="adm-card__head"><h3>' + esc(page.crumb || page.file || 'Halaman') + '</h3>' +
        '<span class="adm-card__handle">' + esc(slug || '/') + '</span></div>' +
        '<div class="adm-field"><textarea data-page-html="' + esc(slug) + '" rows="14" ' +
        'placeholder="Memuat berkas sumber…" spellcheck="false">' + esc(current) + '</textarea></div>' +
        '</div>';
    }).join('');
    return html;
  }

  function hydratePageHtml() {
    var pages = state.content.pages || [];
    var bySlug = {};
    pages.forEach(function (page) { bySlug[String(page.slug == null ? '' : page.slug)] = page; });
    var nodes = el('editor').querySelectorAll('[data-page-html]');
    Array.prototype.forEach.call(nodes, function (node) {
      if (node.value.trim()) return;
      var slug = node.getAttribute('data-page-html');
      var page = bySlug[slug];
      if (!page || !page.file) return;
      var file = page.file + '.html';
      if (state.pageSources[file]) {
        node.value = state.pageSources[file];
        return;
      }
      fetch(SOURCE_BASE + encodeURIComponent(file), { cache: 'force-cache' })
        .then(function (res) {
          if (!res.ok) throw new Error('sumber tidak tersedia');
          return res.text();
        })
        .then(function (text) {
          state.pageSources[file] = text;
          if (node.isConnected && !node.value.trim()) node.value = text;
        })
        .catch(function () {
          node.placeholder = 'Berkas sumber tidak dapat dimuat. Perubahan tetap bisa ditulis manual.';
        });
    });
  }

  function renderEditor() {
    if (!state.content) return;
    var section = currentSection();
    el('section-title').textContent = section.label;
    el('section-help').textContent = section.help || '';

    var isPosts = section.key === 'posts';
    var canAdd = section.kind === 'array' && section.noAdd !== true;
    el('add-btn').hidden = !canAdd || isPosts;
    el('add-post-btn').hidden = !isPosts;

    var html = '';
    if (section.kind === 'object') html = renderObjectSection(section);
    else if (section.kind === 'lines') html = renderLinesSection(section);
    else if (section.kind === 'page_html') html = renderPageHtmlSection(section);
    else html = renderArraySection(section);

    el('editor').innerHTML = html;
    if (section.kind === 'page_html') hydratePageHtml();
    renderNav();
  }

  /* -------------------------------------------------------------- interaksi */

  function syncImagePreview(path, value) {
    var nodes = document.querySelectorAll('[data-preview]');
    Array.prototype.forEach.call(nodes, function (img) {
      if (img.getAttribute('data-preview') !== path) return;
      var src = imageSrc(value);
      if (src) {
        img.src = src;
        img.hidden = false;
      } else {
        img.removeAttribute('src');
        img.hidden = true;
      }
    });
  }

  async function handleImageInput(input) {
    var path = input.getAttribute('data-image-input');
    var file = input.files && input.files[0];
    if (!path || !file) return;
    try {
      toast('Memproses gambar…');
      var dataUrl = await prepareImage(file);
      setPath(state.content, path, dataUrl);
      markDirty();
      renderEditor();
      toast('Gambar siap. Klik Simpan untuk menyimpan atau menerbitkan.');
    } catch (err) {
      input.value = '';
      toast(err.message || 'Gambar gagal diproses.', true);
    }
  }

  function addEntry() {
    var section = currentSection();
    if (section.kind !== 'array' || section.noAdd) return;
    var list = state.content[section.key] || [];
    var template;

    if (section.key === 'posts') {
      template = {
        title: '',
        date: new Date().toISOString().slice(0, 10),
        cat: 'Pengumuman',
        image: '',
        excerpt: '',
      };
    } else if (list.length) {
      template = JSON.parse(JSON.stringify(list[list.length - 1]));
      Object.keys(template).forEach(function (key) {
        if (key === 'file') return;
        if (typeof template[key] === 'number') template[key] = 0;
        else if (typeof template[key] === 'boolean') template[key] = false;
        else template[key] = '';
      });
    } else {
      template = {};
      (section.fields || []).forEach(function (key) { template[key] = ''; });
    }

    list.push(template);
    state.content[section.key] = list;
    markDirty();
    renderEditor();

    var cards = el('editor').querySelectorAll('.adm-card');
    var last = cards[cards.length - 1];
    if (last) {
      last.scrollIntoView({ behavior: 'smooth', block: 'center' });
      var first = last.querySelector('[data-path$=".title"]') || last.querySelector('[data-path]');
      if (first && first.focus) first.focus({ preventScroll: true });
    }
  }

  function bindEditorEvents() {
    var editor = el('editor');

    editor.addEventListener('input', function (event) {
      var target = event.target;

      if (target.hasAttribute && target.hasAttribute('data-page-html')) {
        var slug = target.getAttribute('data-page-html');
        if (!state.content.page_html || typeof state.content.page_html !== 'object') state.content.page_html = {};
        if (target.value.trim()) state.content.page_html[slug] = target.value;
        else delete state.content.page_html[slug];
        markDirty();
        return;
      }

      if (target.dataset.path) {
        var value = target.type === 'checkbox' ? target.checked : target.value;
        if (target.type === 'number') value = value === '' ? 0 : Number(value);
        setPath(state.content, target.dataset.path, value);
        if (/\.image$/.test(target.dataset.path)) syncImagePreview(target.dataset.path, value);
        markDirty();
      } else if (target.dataset.lines) {
        var lines = target.value.split('\n').map(function (line) { return line.trim(); }).filter(Boolean);
        state.content[target.dataset.lines] = lines;
        markDirty();
      }
    });

    editor.addEventListener('change', function (event) {
      var target = event.target;
      if (target.matches && target.matches('[data-image-input]')) {
        handleImageInput(target);
        return;
      }
      if (target.tagName === 'SELECT') markDirty();
    });

    editor.addEventListener('click', function (event) {
      var button = event.target.closest('button');
      if (!button) return;
      var section = currentSection();
      var list = state.content[section.key];

      if (button.dataset.imageClear != null) {
        var imagePath = button.getAttribute('data-image-clear');
        setPath(state.content, imagePath, '');
        markDirty();
        renderEditor();
        toast('Gambar dihapus. Pilih file baru atau isi nama gambar.');
      } else if (button.dataset.del != null) {
        var index = Number(button.dataset.del);
        if (!window.confirm('Hapus entri ini?')) return;
        list.splice(index, 1);
        markDirty();
        renderEditor();
      } else if (button.dataset.dup != null) {
        var copy = JSON.parse(JSON.stringify(list[Number(button.dataset.dup)]));
        list.splice(Number(button.dataset.dup) + 1, 0, copy);
        markDirty();
        renderEditor();
      } else if (button.dataset.move) {
        var from = Number(button.dataset.index);
        var to = button.dataset.move === 'up' ? from - 1 : from + 1;
        if (to < 0 || to >= list.length) return;
        var moved = list.splice(from, 1)[0];
        list.splice(to, 0, moved);
        markDirty();
        renderEditor();
      }
    });

    el('section-nav').addEventListener('click', function (event) {
      var button = event.target.closest('[data-section]');
      if (!button) return;
      state.section = button.dataset.section;
      renderEditor();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    el('add-btn').addEventListener('click', addEntry);
    el('add-post-btn').addEventListener('click', addEntry);
  }

  /* ------------------------------------------------------------- alur UI */

  function showLogin(message) {
    el('login-view').hidden = false;
    el('panel-view').hidden = true;
    el('savebar').hidden = true;
    el('logout-btn').hidden = true;
    el('conn-chip').hidden = true;
    el('local-notice').hidden = true;
    el('connect-card').hidden = true;
    if (message) {
      var box = el('login-error');
      box.textContent = message;
      box.hidden = false;
    } else {
      var errorBox = el('login-error');
      errorBox.textContent = '';
      errorBox.hidden = true;
    }
    el('adm-pass').value = '';
    if (state.deployTimer) clearInterval(state.deployTimer);
    state.deployTimer = null;
  }

  function updateConnectionUi() {
    var chip = el('conn-chip');
    chip.hidden = false;
    chip.className = 'adm__chip is-live';
    if (state.mode === 'worker') {
      chip.textContent = 'Server · live';
    } else if (state.mode === 'token') {
      chip.textContent = 'GitHub · live';
    } else {
      chip.textContent = 'Mode lokal';
      chip.className = 'adm__chip is-off';
    }
    el('local-notice').hidden = state.mode !== 'local';
    el('deploy-link').hidden = state.mode === 'local';
    el('save-btn').textContent = state.mode === 'local' ? 'Simpan di perangkat' : 'Simpan & terbitkan';
  }

  function showPanel() {
    el('login-view').hidden = true;
    el('panel-view').hidden = false;
    el('savebar').hidden = false;
    el('logout-btn').hidden = false;
    el('connect-card').hidden = true;
    el('deploy-link').href = 'https://github.com/' + REPO + '/actions';
    updateConnectionUi();
    setSaveState('Belum ada perubahan');
    renderEditor();
  }

  async function startSession(data) {
    state.mode = data.mode;
    state.token = data.token || '';
    state.content = null;
    setSaveState('Memuat data…');
    await loadContent();
    state.dirty = false;
    showPanel();
    var count = Object.keys(state.content || {}).length;
    if (state.mode === 'local') {
      toast('Berhasil masuk (mode lokal). ' + count + ' bagian data dimuat.');
    } else {
      toast('Berhasil masuk. ' + count + ' bagian data dimuat.');
    }
  }

  function initLogin() {
    el('login-form').addEventListener('submit', async function (event) {
      event.preventDefault();
      var errorBox = el('login-error');
      errorBox.hidden = true;
      var user = el('adm-user').value.trim();
      var pass = el('adm-pass').value;

      if (!user || !pass) {
        errorBox.textContent = 'Username dan kata sandi wajib diisi.';
        errorBox.hidden = false;
        return;
      }

      var button = el('login-submit');
      button.disabled = true;
      button.textContent = 'Memeriksa…';

      try {
        var workerDone = false;

        if (API) {
          try {
            var res = await fetch(API + '/login', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ u: user, p: pass }),
            });
            var data = await res.json().catch(function () { return {}; });
            if (!res.ok || !data.ok) throw new Error(data.error || 'Login gagal.');
            state.token = data.token;
            saveSession({ mode: 'worker', token: data.token, exp: data.exp, user: data.user });
            await startSession({ mode: 'worker', token: data.token });
            workerDone = true;
          } catch (workerErr) {
            var canUseLocal = await localCredentialsMatch(user, pass);
            if (!canUseLocal) throw workerErr;
            toast('Backend tidak merespons. Masuk dengan mode lokal.', true);
          }
        }

        if (!workerDone) {
          var valid = await localCredentialsMatch(user, pass);
          if (!valid) throw new Error('Username atau kata sandi salah.');
          saveSession({ mode: 'local', token: '', user: user });
          await startSession({ mode: 'local' });
        }
      } catch (err) {
        errorBox.textContent = err.message || 'Login gagal.';
        errorBox.hidden = false;
      } finally {
        button.disabled = false;
        button.textContent = 'Masuk';
      }
    });

    el('token-form').addEventListener('submit', async function (event) {
      event.preventDefault();
      var errorBox = el('login-error');
      errorBox.hidden = true;
      var token = el('adm-token').value.trim();
      if (!token) return;
      state.token = token;
      try {
        var repo = await ghCall('');
        if (!repo.permissions || !repo.permissions.push) {
          throw new Error('Token ini tidak punya izin tulis ke ' + REPO + '.');
        }
        saveSession({ mode: 'token', token: token, user: 'token' });
        await startSession({ mode: 'token', token: token });
        el('adm-token').value = '';
      } catch (err) {
        errorBox.textContent = err.message || 'Token tidak valid.';
        errorBox.hidden = false;
      }
    });
  }

  async function connectGitHub(token) {
    state.token = token;
    var repo = await ghCall('');
    if (!repo.permissions || !repo.permissions.push) {
      throw new Error('Token ini tidak punya izin tulis ke ' + REPO + '.');
    }

    var keepLocal = state.dirty || state.fromLocal;
    state.mode = 'token';
    if (keepLocal) {
      await refreshSha();
      state.dirty = true;
    } else {
      state.sha = null;
      await loadContent();
      state.dirty = false;
    }
    state.fromLocal = false;
    saveSession({ mode: 'token', token: token, user: 'token' });
    showPanel();
    if (keepLocal) {
      setSaveState('Terhubung ke GitHub — klik Simpan & terbitkan', 'dirty');
      toast('GitHub terhubung. Data lokal siap diterbitkan.');
    } else {
      toast('GitHub terhubung. Data terbaru dimuat.');
    }
  }

  function initConnect() {
    el('connect-gh-btn').addEventListener('click', function () {
      el('connect-card').hidden = false;
      el('connect-error').hidden = true;
      el('connect-token').focus();
    });

    el('connect-cancel').addEventListener('click', function () {
      el('connect-card').hidden = true;
      el('connect-token').value = '';
    });

    el('connect-form').addEventListener('submit', async function (event) {
      event.preventDefault();
      var errorBox = el('connect-error');
      var button = el('connect-submit');
      var token = el('connect-token').value.trim();
      errorBox.hidden = true;
      if (!token) {
        errorBox.textContent = 'Token wajib diisi.';
        errorBox.hidden = false;
        return;
      }
      button.disabled = true;
      button.textContent = 'Menghubungkan…';
      try {
        await connectGitHub(token);
        el('connect-token').value = '';
        el('connect-card').hidden = true;
      } catch (err) {
        state.mode = 'local';
        state.token = '';
        errorBox.textContent = err.message || 'Token tidak valid.';
        errorBox.hidden = false;
        updateConnectionUi();
      } finally {
        button.disabled = false;
        button.textContent = 'Sambungkan & muat data';
      }
    });
  }

  function initPanel() {
    el('logout-btn').addEventListener('click', function () {
      if (state.dirty && !window.confirm('Ada perubahan belum disimpan. Keluar tetap?')) return;
      clearSession();
      state.content = null;
      state.token = '';
      state.dirty = false;
      state.fromLocal = false;
      showLogin();
      toast('Anda sudah keluar.');
    });

    el('reload-btn').addEventListener('click', async function () {
      if (state.dirty && !window.confirm('Muat ulang akan membuang perubahan belum disimpan. Lanjut?')) return;
      try {
        if (state.mode === 'local') {
          try { localStorage.removeItem(LOCAL_CONTENT_KEY); } catch (err) { /* abaikan */ }
          state.fromLocal = false;
        }
        await loadContent();
        state.dirty = false;
        setSaveState('Data dimuat ulang');
        renderEditor();
        toast('Data terbaru dimuat.');
      } catch (err) {
        toast(err.message, true);
      }
    });

    function downloadJson() {
      var blob = new Blob([JSON.stringify(state.content, null, 2)], { type: 'application/json' });
      var link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'content-' + new Date().toISOString().slice(0, 10) + '.json';
      link.click();
      URL.revokeObjectURL(link.href);
    }

    el('download-btn').addEventListener('click', downloadJson);
    el('download-json-btn').addEventListener('click', downloadJson);

    el('save-btn').addEventListener('click', async function () {
      if (state.busy) return;
      var button = el('save-btn');
      state.busy = true;
      button.disabled = true;
      button.textContent = 'Menyimpan…';
      setSaveState(state.mode === 'local' ? 'Menyimpan di perangkat…' : 'Mengirim ke GitHub…');
      try {
        var result = await saveContent();
        state.dirty = false;

        if (result.local) {
          state.fromLocal = true;
          setSaveState('Tersimpan di perangkat ini', 'ok');
          toast('Perubahan tersimpan di peramban ini. Hubungkan GitHub untuk menerbitkan ke semua pengunjung.');
        } else {
          state.fromLocal = false;
          setSaveState('Tersimpan — situs sedang dibangun…', 'ok');
          toast('Tersimpan. GitHub Actions sedang membangun situs.');
          await loadContent();
          state.dirty = false;
          renderEditor();
          el('deploy-link').hidden = false;
          watchDeploy();
        }
      } catch (err) {
        setSaveState('Gagal menyimpan', 'err');
        toast(err.message || 'Gagal menyimpan.', true);
      } finally {
        state.busy = false;
        button.disabled = false;
        button.textContent = state.mode === 'local' ? 'Simpan di perangkat' : 'Simpan & terbitkan';
      }
    });

    initConnect();

    window.addEventListener('beforeunload', function (event) {
      if (!state.dirty) return;
      event.preventDefault();
      event.returnValue = '';
    });
  }

  function watchDeploy() {
    if (state.deployTimer) clearInterval(state.deployTimer);
    var started = Date.now();
    var checks = 0;

    state.deployTimer = setInterval(async function () {
      checks += 1;
      if (Date.now() - started > 5 * 60 * 1000 || checks > 40) {
        clearInterval(state.deployTimer);
        state.deployTimer = null;
        return;
      }
      try {
        var run = await deployStatus();
        if (!run) return;
        if (run.status === 'completed') {
          clearInterval(state.deployTimer);
          state.deployTimer = null;
          if (run.conclusion === 'success') {
            setSaveState('Terbit — perubahan sudah live di situs', 'ok');
            toast('Build selesai. Perubahan sudah tampil di lsppatraindo.id.');
          } else {
            setSaveState('Build gagal — periksa tab Actions', 'err');
            toast('Build gagal. Buka tab Actions untuk melihat log.', true);
          }
        } else {
          setSaveState('Membangun situs… (' + run.status + ')');
        }
      } catch (err) {
        /* diamkan, coba lagi pada interval berikutnya */
      }
    }, 7000);
  }

  async function boot() {
    initLogin();
    initPanel();
    bindEditorEvents();

    var existing = session();
    if (!existing || (existing.mode !== 'local' && !existing.token)) {
      showLogin();
      if (!API) {
        el('setup-notice').hidden = false;
      } else {
        fetch(API + '/health').then(function (res) { return res.json(); }).then(function (data) {
          if (!data.configured) el('setup-notice').hidden = false;
        }).catch(function () {
          el('setup-notice').hidden = false;
        });
      }
      return;
    }

    state.token = existing.token || '';
    state.mode = existing.mode;
    try {
      await startSession(existing);
    } catch (err) {
      clearSession();
      showLogin(err.message || 'Sesi tidak valid. Silakan masuk kembali.');
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
