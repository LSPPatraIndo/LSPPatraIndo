"""Konten situs LSP Pariwisata Citra Indonesia.

Semua data yang tampil di halaman dikumpulkan di sini agar mudah diperbarui
tanpa menyentuh markup. Lihat README.md untuk daftar data yang perlu diganti.
"""

# ---------------------------------------------------------------------------
# Identitas lembaga
# ---------------------------------------------------------------------------
SITE = {
    'name': 'LSP Pariwisata Citra Indonesia',
    'legal': 'Lembaga Sertifikasi Profesi Pariwisata Citra Indonesia',
    'domain': 'lsppatraindo.id',
    'url': 'https://lsppatraindo.id',
    'tagline': 'LSP Bidang Wisata Golf Pertama di Indonesia',
    'description': 'Lembaga Sertifikasi Profesi (LSP/P3) terlisensi BNSP untuk bidang Golf dan Pariwisata.',
    'phone_display': '+62 821 7220 608',
    'phone_link': '+6282322266585',
    'wa': '6282322266585',
    'email': 'info@lsppatraindo.id',
    'email_sertifikasi': 'sertifikasi@lsppatraindo.id',
    'address': 'Jl. Hang Lekiu Km 4, Sambau, Nongsa, Kota Batam, Kepulauan Riau 29465',
    'city': 'Batam',
    'hours': 'Senin – Jumat, 08.00 – 16.00 WIB',
    'hours_sat': 'Sabtu, 09.00 – 13.00 WIB',
    'maps_query': 'MECA Travel, Hang Lekiu Km 4, Batam',
    'social': {
        'instagram': 'https://instagram.com/lsppatraindo',
        'linkedin': 'https://linkedin.com/company/lsppatraindo',
        'youtube': 'https://youtube.com/@lsppatraindo',
        'facebook': 'https://facebook.com/lsppatraindo',
    },
    'login_url': 'https://siapkerja.kemnaker.go.id/',
    'form_endpoint': '',
    'admin_api': 'https://lsp-patra-indo-admin.netlify.app/.netlify/functions',
    'github_repo': 'LSPPatraIndo/LSPPatraIndo',
    'github_branch': 'main',
    'founded': 2026,
    'logo': '',
}

# ---------------------------------------------------------------------------
# Navigasi
# ---------------------------------------------------------------------------
NAV = [
    {'label': 'Beranda', 'href': ''},
    {
        'label': 'Profil',
        'children': [
            {'label': 'Tentang Kami', 'href': 'tentang-kami/', 'desc': 'Sejarah, visi, misi, dan nilai lembaga'},
            {'label': 'Struktur Organisasi', 'href': 'tentang-kami/#struktur', 'desc': 'Susunan pengurus dan manajemen'},
            {'label': 'Daftar Asesor', 'href': 'daftar-asesor/', 'desc': 'Asesor kompetensi tersertifikasi BNSP'},
            {'label': 'Tempat Uji Kompetensi', 'href': 'tuk/', 'desc': 'Lokasi TUK Golf dan Pariwisata'},
        ],
    },
    {
        'label': 'Sertifikasi',
        'children': [
            {'label': 'Skema Sertifikasi', 'href': 'skema-sertifikasi/', 'desc': 'Dua bidang: Golf dan Pariwisata'},
            {'label': 'Alur Sertifikasi', 'href': 'alur-sertifikasi/', 'desc': 'Lima langkah dari daftar hingga sertifikat'},
            {'label': 'Persyaratan', 'href': 'persyaratan/', 'desc': 'Dokumen dan ketentuan peserta'},
            {'label': 'Jadwal & Biaya', 'href': 'jadwal/', 'desc': 'Jadwal uji terdekat dan rincian biaya'},
            {'label': 'FAQ', 'href': 'faq/', 'desc': 'Pertanyaan yang sering diajukan'},
        ],
    },
    {'label': 'Jadwal & Biaya', 'href': 'jadwal/'},
    {'label': 'Berita', 'href': 'berita/'},
    {'label': 'Kontak', 'href': 'kontak/'},
]

# Navigasi kolom "Informasi" di footer. Dapat diubah dari panel admin.
NAV_FOOTER = [
    {'label': 'Tentang Kami', 'href': 'tentang-kami/'},
    {'label': 'Alur Sertifikasi', 'href': 'alur-sertifikasi/'},
    {'label': 'Persyaratan', 'href': 'persyaratan/'},
    {'label': 'Jadwal & Biaya', 'href': 'jadwal/'},
    {'label': 'Daftar Asesor', 'href': 'daftar-asesor/'},
    {'label': 'Tempat Uji Kompetensi', 'href': 'tuk/'},
    {'label': 'FAQ', 'href': 'faq/'},
]

# Tautan kecil di bagian paling bawah footer (tautan Login admin tetap).
NAV_LEGAL = [
    {'label': 'Bantuan', 'href': 'faq/'},
    {'label': 'Kontak', 'href': 'kontak/'},
    {'label': 'Sitemap', 'href': 'sitemap.xml'},
]

# ---------------------------------------------------------------------------
# Halaman: (file body, slug/url, judul, deskripsi meta, label breadcrumb)
# ---------------------------------------------------------------------------
PAGES = [
    (
        'index',
        '',
        'LSP Pariwisata Citra Indonesia — Lembaga Sertifikasi Profesi Terlisensi BNSP',
        'Sertifikasi profesi resmi BNSP bidang Golf dan Pariwisata. Proses terstruktur, asesor berpengalaman, sertifikat diakui nasional.',
        'Beranda',
    ),
    (
        'tentang-kami',
        'tentang-kami',
        'Tentang Kami — Profil, Visi & Misi LSP Pariwisata Citra Indonesia',
        'Kenali LSP Pariwisata Citra Indonesia: lembaga sertifikasi profesi independen di bidang Golf dan Pariwisata yang melaksanakan uji kompetensi berdasarkan SKKNI dan skema terlisensi BNSP.',
        'Tentang Kami',
    ),
    (
        'skema-sertifikasi',
        'skema-sertifikasi',
        'Skema Sertifikasi Golf & Pariwisata — LSP Pariwisata Citra Indonesia',
        'Daftar skema sertifikasi LSP Pariwisata Citra Indonesia untuk bidang Golf dan Pariwisata, dari caddy, starter & marshall, hingga tour guide dan manajemen destinasi.',
        'Skema Sertifikasi',
    ),
    (
        'alur-sertifikasi',
        'alur-sertifikasi',
        'Alur Sertifikasi — Proses Uji Kompetensi 5 Langkah',
        'Alur pendaftaran dan uji kompetensi di LSP Pariwisata Citra Indonesia: konsultasi, registrasi, verifikasi, asesmen, hingga sertifikat terbit.',
        'Alur Sertifikasi',
    ),
    (
        'persyaratan',
        'persyaratan',
        'Persyaratan Sertifikasi — Dokumen & Ketentuan Peserta',
        'Persyaratan umum, administrasi, dan dokumen portofolio yang perlu disiapkan peserta sertifikasi kompetensi LSP Pariwisata Citra Indonesia.',
        'Persyaratan',
    ),
    (
        'daftar-asesor',
        'daftar-asesor',
        'Daftar Asesor Kompetensi — LSP Pariwisata Citra Indonesia',
        'Asesor kompetensi tersertifikasi BNSP di LSP Pariwisata Citra Indonesia beserta bidang keahlian dan wilayah kerja.',
        'Daftar Asesor',
    ),
    (
        'tuk',
        'tuk',
        'Tempat Uji Kompetensi (TUK) — Lokasi & Fasilitas',
        'Daftar Tempat Uji Kompetensi LSP Pariwisata Citra Indonesia: TUK sewaktu, TUK tempat kerja, dan TUK mandiri di berbagai kota.',
        'Tempat Uji Kompetensi',
    ),
    (
        'jadwal',
        'jadwal',
        'Jadwal Sertifikasi & Biaya — LSP Pariwisata Citra Indonesia',
        'Jadwal uji kompetensi terdekat, kuota, lokasi TUK, serta informasi biaya sertifikasi LSP Pariwisata Citra Indonesia.',
        'Jadwal & Biaya',
    ),
    (
        'faq',
        'faq',
        'FAQ Sertifikasi — Pertanyaan yang Sering Diajukan',
        'Jawaban atas pertanyaan umum seputar pendaftaran, uji kompetensi, sertifikat, biaya, dan perpanjangan sertifikasi.',
        'FAQ',
    ),
    (
        'berita',
        'berita',
        'Berita & Artikel — LSP Pariwisata Citra Indonesia',
        'Kabar kegiatan uji kompetensi, artikel industri, panduan sertifikasi, dan informasi terbaru dari LSP Pariwisata Citra Indonesia.',
        'Berita',
    ),
    (
        'kontak',
        'kontak',
        'Kontak & Pendaftaran — LSP Pariwisata Citra Indonesia',
        'Hubungi LSP Pariwisata Citra Indonesia untuk konsultasi skema Golf dan Pariwisata, jadwal uji kompetensi, kerja sama korporat, dan pendaftaran peserta.',
        'Kontak',
    ),
]

# Override markup halaman dari panel admin (opsional).
# Format: {"slug-halaman": "<section>…</section>"} — bila kosong, build
# memakai berkas sumber di src/pages/*.html seperti biasa.
PAGE_HTML = {}

# ---------------------------------------------------------------------------
# Statistik
# ---------------------------------------------------------------------------
STATS = [
    {'value': 10, 'suffix': '+', 'label': 'Skema Sertifikasi', 'note': 'Terlisensi BNSP'},
    {'value': 18, 'suffix': '+', 'label': 'Asesor Kompetensi', 'note': 'Bersertifikat metodologi'},
    {'value': 199, 'suffix': '+', 'label': 'Peserta Tersertifikasi', 'note': 'Sejak 2026'},
    {'value': 100, 'suffix': '+', 'label': 'Tempat Uji Kompetensi', 'note': 'Golf resort, travel, dan hotel'},
]

# ---------------------------------------------------------------------------
# Keunggulan
# ---------------------------------------------------------------------------
ADVANTAGES = [
    {
        'icon': 'shield',
        'title': 'Lisensi Resmi BNSP',
        'text': 'Seluruh proses asesmen mengacu pada skema yang terlisensi Badan Nasional Sertifikasi Profesi dan regulasi ketenagakerjaan.',
    },
    {
        'icon': 'users',
        'title': 'Asesor Berpengalaman',
        'text': 'Asesor kami tersertifikasi BNSP dan aktif di industri Golf dan Pariwisata, sehingga penilaian relevan dengan praktik kerja nyata.',
    },
    {
        'icon': 'route',
        'title': 'Proses Transparan',
        'text': 'Alur, biaya, dan jadwal disampaikan sejak awal. Status pendaftaran dapat dipantau melalui admin pendamping.',
    },
    {
        'icon': 'award',
        'title': 'Sertifikat Diakui',
        'text': 'Sertifikat kompetensi tercatat di sistem SIAPkerja Kemnaker dan diakui lintas industri, termasuk ASEAN.',
    },
]

# ---------------------------------------------------------------------------
# Skema sertifikasi
# ---------------------------------------------------------------------------
SCHEME_CATS = [
    {'id': 'golf', 'label': 'Golf', 'icon': 'star', 'desc': 'Operasional lapangan, caddy, dan manajemen golf'},
    {
        'id': 'pariwisata',
        'label': 'Pariwisata',
        'icon': 'globe',
        'desc': 'Kepemanduan, perencanaan destinasi, dan humas',
    },
]
SCHEMES = [
    {
        'name': 'Porter',
        'cat': 'golf',
        'level': 'KKNI II',
        'units': 6,
        'featured': True,
        'desc': 'Menangani penerimaan tamu, tas golf, dan kebutuhan logistik di area klub golf.',
    },
    {
        'name': 'Starter and Marshall',
        'cat': 'golf',
        'level': 'KKNI III',
        'units': 8,
        'featured': True,
        'desc': 'Mengatur alur permainan, memastikan kepatuhan aturan, dan menjaga keselamatan di lapangan.',
    },
    {
        'name': 'Golf Profesional',
        'cat': 'golf',
        'level': 'KKNI IV',
        'units': 10,
        'featured': True,
        'desc': 'Memberikan pelajaran golf, menilai kemampuan pemain, dan mengelola program latihan.',
    },
    {
        'name': 'Golf Operation Manager',
        'cat': 'golf',
        'level': 'KKNI IV',
        'units': 12,
        'desc': 'Mengelola operasional lapangan, jadwal tee time, dan koordinasi tim layanan golf.',
    },
    {
        'name': 'Golfing Assistant-caddy',
        'cat': 'golf',
        'level': 'KKNI II',
        'units': 7,
        'desc': 'Mendampingi pemain, membawa peralatan, dan memberikan informasi lapangan selama permainan.',
    },
    {
        'name': 'Overland Tour Guide',
        'cat': 'pariwisata',
        'level': 'KKNI III',
        'units': 9,
        'featured': True,
        'desc': 'Memandu perjalanan darat, menyusun narasi, dan mengelola logistik rombongan wisata.',
    },
    {
        'name': 'National Tour Guide',
        'cat': 'pariwisata',
        'level': 'KKNI IV',
        'units': 10,
        'featured': True,
        'desc': 'Memandu wisatawan nusantara dan mancanegara dengan interpretasi destinasi yang profesional.',
    },
    {
        'name': 'Perencana Kegiatan Wisata Destinasi',
        'cat': 'pariwisata',
        'level': 'KKNI IV',
        'units': 9,
        'desc': 'Merancang program wisata destinasi, anggaran, dan jadwal kegiatan yang berkelanjutan.',
    },
    {
        'name': 'Manajer Humas Destinasi',
        'cat': 'pariwisata',
        'level': 'KKNI IV',
        'units': 8,
        'desc': 'Mengelola komunikasi publik, kemitraan, dan citra destinasi wisata.',
    },
    {
        'name': 'Pramuwisata Madya',
        'cat': 'pariwisata',
        'level': 'KKNI IV',
        'units': 10,
        'featured': True,
        'desc': 'Memandu wisata dengan penguasaan interpretasi, etika, dan penanganan situasi darurat.',
    },
]

# ---------------------------------------------------------------------------
# Teks bergerak (ticker & rotator hero)
# ---------------------------------------------------------------------------
HERO_ROLES = ['Golf', 'Pariwisata']
TICKER_ITEMS = [
    {'text': 'Terlisensi BNSP', 'outline': False},
    {'text': 'Diakui Nasional', 'outline': True},
    {'text': '10 Skema Sertifikasi', 'outline': False},
    {'text': 'Asesor Bersertifikat', 'outline': True},
    {'text': 'E-Sertifikat SIAPkerja', 'outline': False},
    {'text': 'Uji Kompetensi Terstruktur', 'outline': True},
]

# ---------------------------------------------------------------------------
# Alur sertifikasi
# ---------------------------------------------------------------------------
STEPS = [
    {
        'no': '01',
        'title': 'Pilih Skema & Konsultasi',
        'duration': 'Hari 1',
        'text': 'Tentukan skema sesuai pengalaman kerja Anda, lalu konsultasikan dengan admin kami untuk memastikan kesesuaian dan ketersediaan jadwal.',
    },
    {
        'no': '02',
        'title': 'Registrasi & Unggah Dokumen',
        'duration': 'Hari 1–2',
        'text': 'Buat akun SIAPkerja, isi formulir pendaftaran, dan unggah dokumen persyaratan melalui halaman pendaftaran.',
    },
    {
        'no': '03',
        'title': 'Verifikasi & Pembayaran',
        'duration': 'Hari 2–5',
        'text': 'Tim kami memverifikasi kelengkapan administrasi. Setelah dinyatakan lengkap, lakukan pembayaran untuk mengunci kuota dan jadwal.',
    },
    {
        'no': '04',
        'title': 'Uji Kompetensi',
        'duration': '1–2 hari',
        'text': 'Asesmen mandiri, observasi praktik, wawancara, dan penilaian portofolio bersama asesor di TUK yang ditetapkan.',
    },
    {
        'no': '05',
        'title': 'Pleno & Penerbitan Sertifikat',
        'duration': '4–7 minggu',
        'text': 'Rapat pleno menetapkan keputusan kompeten, kemudian sertifikat diterbitkan BNSP dan tersedia di akun SIAPkerja Anda.',
    },
]

# ---------------------------------------------------------------------------
# Testimoni
# ---------------------------------------------------------------------------
TESTIMONIALS = [
    {
        'name': 'Dika Nanda P.',
        'role': 'Golf Operation Manager',
        'quote': 'Prosesnya cepat dan asesornya sangat kompeten. Saya merekomendasikan sertifikasi di LSP Pariwisata Citra Indonesia untuk rekan-rekan yang ingin mengakui pengalaman kerjanya secara formal.',
        'initials': 'DN',
        'tone': 'teal',
    },
    {
        'name': 'Wahyu Prasetyo',
        'role': 'Overland Tour Guide',
        'quote': 'Awalnya ragu bisa menjawab pertanyaan asesor, tetapi pendampingan dilakukan dengan bahasa yang sederhana sehingga mudah dipahami dan saya jadi lebih percaya diri.',
        'initials': 'WP',
        'tone': 'gold',
    },
    {
        'name': 'Yunani Rahmawati',
        'role': 'National Tour Guide',
        'quote': 'Setelah mengikuti uji kompetensi, saya lebih yakin dengan standar kerja saya. Ilmu yang didapat langsung terasa manfaatnya di tempat kerja.',
        'initials': 'YR',
        'tone': 'navy',
    },
]

# ---------------------------------------------------------------------------
# Asesor
# ---------------------------------------------------------------------------
ASESOR = [
    {
        'name': 'Rina Sartika',
        'initials': 'RS',
        'field': 'Pariwisata',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007376.2024',
    },
    {
        'name': 'Juniarti Sarumpaet',
        'initials': 'JS',
        'field': 'Pariwisata',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007377.2024',
    },
    {
        'name': 'Willy Rachdiyan',
        'initials': 'WR',
        'field': 'Pariwisata',
        'city': 'Bandung',
        'year': 2024,
        'license': 'MET 000.007378.2024',
    },
    {
        'name': 'Zitachila Virginia Rahmallah',
        'initials': 'ZV',
        'field': 'Pariwisata',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007379.2024',
    },
    {
        'name': 'Enly Yunaeni, S.E., M.M.',
        'initials': 'EY',
        'field': 'Golfing dan Wisata',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007380.2024',
    },
    {
        'name': 'Adi Nugraha Lumban Tobing',
        'initials': 'AN',
        'field': 'Kepemanduan Wisata',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007382.2024',
    },
    {
        'name': 'Eny Widyawati',
        'initials': 'EW',
        'field': 'Travel & Ticketing',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007383.2024',
    },
    {
        'name': 'Cholifah Edelenbos',
        'initials': 'CE',
        'field': 'Wisata',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007385.2024',
    },
    {
        'name': 'Heru Bagiyo Susianto',
        'initials': 'HB',
        'field': 'Golfing',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007386.2024',
    },
    {
        'name': 'Soearto Sapan',
        'initials': 'SS',
        'field': 'Golfing',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007388.2024',
    },
    {
        'name': 'Dr. Suyono, M.M.',
        'initials': 'SU',
        'field': 'Golfing',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007389.2024',
    },
    {
        'name': 'Zainal Abidin',
        'initials': 'ZA',
        'field': 'Golfing',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007390.2024',
    },
    {
        'name': 'Nur Aniliza Binti Imran',
        'initials': 'NA',
        'field': 'Golfing Assistant',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007391.2024',
    },
    {
        'name': 'Nur Krisya Saputri',
        'initials': 'NK',
        'field': 'Golfing Assistant',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007392.2024',
    },
    {
        'name': 'Liza Rizal',
        'initials': 'LR',
        'field': 'Golfing Assistant',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007393.2024',
    },
    {
        'name': 'Ade Saptri Lumban Batu',
        'initials': 'AS',
        'field': 'Tourism',
        'city': 'Batam',
        'year': 2024,
        'license': 'MET 000.007394.2024',
    },
]

# ---------------------------------------------------------------------------
# Tempat Uji Kompetensi
# ---------------------------------------------------------------------------
TUK = [
    {
        'name': 'TUK Batam Hills',
        'city': 'Kota Batam',
        'type': 'TUK Tempat Kerja',
        'address': 'Batam Hills Golf Resort, Batam',
        'schemes': 5,
    },
    {
        'name': 'TUK Mecca Travel',
        'city': 'Kota Batam',
        'type': 'TUK Tempat Kerja',
        'address': 'Jl. Hang Lekiu Km 4, Batam',
        'schemes': 5,
    },
]

# ---------------------------------------------------------------------------
# Jadwal
# ---------------------------------------------------------------------------
JADWAL = [
    {
        'date': '12 Nov 2026',
        'scheme': 'Golfing Assistant-caddy',
        'tuk': 'Batam',
        'mode': 'Offline',
        'quota': 20,
        'status': 'open',
    },
    {
        'date': '18 Nov 2026',
        'scheme': 'Starter and Marshall',
        'tuk': 'Batam',
        'mode': 'Offline',
        'quota': 16,
        'status': 'open',
    },
    {
        'date': '25 Nov 2026',
        'scheme': 'Overland Tour Guide',
        'tuk': 'Batam',
        'mode': 'Hybrid',
        'quota': 12,
        'status': 'almost',
    },
    {
        'date': '02 Des 2026',
        'scheme': 'National Tour Guide',
        'tuk': 'Batam',
        'mode': 'Offline',
        'quota': 20,
        'status': 'open',
    },
    {
        'date': '09 Des 2026',
        'scheme': 'Golf Profesional',
        'tuk': 'Batam',
        'mode': 'Offline',
        'quota': 24,
        'status': 'open',
    },
    {
        'date': '16 Des 2026',
        'scheme': 'Pramuwisata Madya',
        'tuk': 'Batam',
        'mode': 'Online',
        'quota': 18,
        'status': 'wait',
    },
    {
        'date': '13 Jan 2027',
        'scheme': 'Perencana Kegiatan Wisata Destinasi',
        'tuk': 'Batam',
        'mode': 'Offline',
        'quota': 20,
        'status': 'open',
    },
    {
        'date': '20 Jan 2027',
        'scheme': 'Golf Operation Manager',
        'tuk': 'Batam',
        'mode': 'Online',
        'quota': 22,
        'status': 'open',
    },
]

STATUS_LABEL = {
    "open": ("Dibuka", "is-open"),
    "almost": ("Hampir penuh", "is-almost"),
    "wait": ("Menunggu kuota", "is-wait"),
}

# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------
FAQ = [
    {
        'q': 'Apa itu sertifikasi kompetensi dan mengapa penting?',
        'a': 'Sertifikasi kompetensi adalah proses pengakuan formal atas kemampuan kerja seseorang sesuai Standar Kompetensi Kerja Nasional Indonesia (SKKNI). Sertifikat ini menjadi bukti objektif kompetensi Anda bagi pemberi kerja, klien, dan mitra bisnis.',
    },
    {
        'q': 'Siapa yang dapat mengikuti sertifikasi di LSP Pariwisata Citra Indonesia?',
        'a': 'Peserta dapat berasal dari tenaga kerja aktif, lulusan pendidikan vokasi, mahasiswa tingkat akhir, pelaku usaha, maupun individu yang ingin mengakui pengalaman kerjanya. Syarat utama adalah memenuhi persyaratan skema yang dipilih.',
    },
    {
        'q': 'Apakah harus memiliki akun SIAPkerja?',
        'a': 'Ya. Akun SIAPkerja Kementerian Ketenagakerjaan diperlukan karena sertifikat kompetensi diterbitkan dalam bentuk elektronik dan tersimpan pada akun tersebut. Pembuatan akun gratis melalui siapkerja.kemnaker.go.id.',
    },
    {
        'q': 'Berapa lama proses hingga sertifikat terbit?',
        'a': 'Rata-rata 4–7 minggu setelah uji kompetensi, tergantung penyelesaian rapat pleno dan penerbitan blanko oleh BNSP. Kami akan menginformasikan status secara berkala melalui admin pendamping.',
    },
    {
        'q': 'Berapa biaya sertifikasi?',
        'a': 'Biaya berbeda untuk setiap skema dan lokasi TUK, serta dapat berubah sesuai ketentuan BNSP. Silakan hubungi admin untuk mendapatkan rincian biaya resmi dan opsi pembayaran bertahap.',
    },
    {
        'q': 'Apakah uji kompetensi bisa dilakukan secara online?',
        'a': 'Sebagian asesmen dapat dilakukan secara daring, namun skema dengan komponen praktik tetap memerlukan kehadiran di TUK. Metode asesmen akan diinformasikan saat konfirmasi jadwal.',
    },
    {
        'q': 'Bagaimana jika hasil asesmen belum kompeten?',
        'a': 'Peserta diberikan umpan balik dan kesempatan untuk melakukan asesmen ulang pada unit yang belum kompeten sesuai ketentuan, dengan biaya dan jadwal yang diinformasikan oleh admin.',
    },
    {
        'q': 'Bagaimana prosedur banding atau keberatan?',
        'a': 'Peserta dapat mengajukan banding maksimal 7 hari kerja setelah keputusan pleno disampaikan. Prosedur lengkap diatur dalam dokumen Alur Banding yang dapat diminta kepada admin.',
    },
    {
        'q': 'Apakah sertifikat perlu diperbarui?',
        'a': 'Masa berlaku sertifikat umumnya 3 tahun. Perpanjangan dapat dilakukan melalui skema sertifikasi ulang (re-sertifikasi) dengan menyerahkan bukti portofolio kegiatan kerja terkini.',
    },
    {
        'q': 'Apakah LSP Pariwisata Citra Indonesia menerima kerja sama korporat?',
        'a': 'Ya. Kami melayani sertifikasi in-house untuk golf club, golf resort, travel agency, pengelola destinasi wisata, dan institusi pendidikan dengan jadwal serta skema yang disesuaikan kebutuhan organisasi.',
    },
]

# ---------------------------------------------------------------------------
# Berita
# ---------------------------------------------------------------------------
POSTS = [
    {
        'title': 'Pembukaan Kelas Sertifikasi Batch November 2026',
        'date': '2026-10-20',
        'cat': 'Pengumuman',
        'image': 'train',
        'excerpt': 'Pendaftaran kelas sertifikasi batch November 2026 resmi dibuka untuk sepuluh skema Golf dan Pariwisata dengan kuota terbatas.',
    },
    {
        'title': 'Mengapa Sertifikat Kompetensi Penting di Industri Golf dan Pariwisata',
        'date': '2026-10-12',
        'cat': 'Artikel',
        'image': 'hero',
        'excerpt': 'Industri golf dan pariwisata semakin selektif dalam merekrut. Sertifikat kompetensi menjadi pembeda yang objektif di tahap seleksi.',
    },
    {
        'title': 'Uji Kompetensi Kepemanduan Wisata Digelar di TUK Batam',
        'date': '2026-10-05',
        'cat': 'Kegiatan',
        'image': 'guide',
        'excerpt': 'Sebanyak 24 peserta mengikuti uji kompetensi skema National Tour Guide dengan metode observasi lapangan dan wawancara.',
    },
    {
        'title': 'Panduan Lengkap Membuat Akun SIAPkerja untuk Peserta',
        'date': '2026-09-28',
        'cat': 'Panduan',
        'image': 'about',
        'excerpt': 'Langkah demi langkah membuat akun SIAPkerja, melengkapi profil, hingga memastikan data siap untuk penerbitan sertifikat.',
    },
    {
        'title': 'Standar Kompetensi Golfing Assistant-caddy: Apa yang Diuji?',
        'date': '2026-09-15',
        'cat': 'Artikel',
        'image': 'fb',
        'excerpt': 'Dari pemahaman lapangan hingga pelayanan kepada pemain, ini cakupan asesmen yang perlu Anda kuasai.',
    },
    {
        'title': 'Tips Lulus Uji Kompetensi Melalui Asesmen Mandiri',
        'date': '2026-09-01',
        'cat': 'Tips',
        'image': 'culinary',
        'excerpt': 'Asesmen mandiri bukan formalitas. Cara mengisinya menentukan arah pembuktian kompetensi Anda di hadapan asesor.',
    },
]

# ---------------------------------------------------------------------------
# Nilai & struktur
# ---------------------------------------------------------------------------
VALUES = [
    {
        'icon': 'shield',
        'title': 'Integritas',
        'text': 'Menjunjung kejujuran dan konsistensi antara aturan, proses, dan keputusan.',
    },
    {
        'icon': 'scale',
        'title': 'Independensi',
        'text': 'Bebas dari pengaruh komersial maupun kepentingan pihak yang diases.',
    },
    {
        'icon': 'check-circle',
        'title': 'Objektivitas',
        'text': 'Keputusan berbasis bukti dan standar kompetensi, bukan opini pribadi.',
    },
    {'icon': 'lock', 'title': 'Kerahasiaan', 'text': 'Melindungi data peserta dan informasi organisasi klien.'},
    {
        'icon': 'award',
        'title': 'Kompetensi',
        'text': 'Personel asesmen dipilih dan dipantau sesuai kualifikasi BNSP.',
    },
    {'icon': 'bolt', 'title': 'Responsif', 'text': 'Layanan administrasi yang cepat, jelas, dan mudah diakses.'},
]
STRUKTUR = [
    {'role': 'Direktur', 'name': 'Enly Yunaeni, S.E., M.M.', 'initials': 'EY', 'note': 'Penanggung jawab lembaga'},
    {
        'role': 'Manajer Sertifikasi',
        'name': 'Zainal Abidin',
        'initials': 'ZA',
        'note': 'Perencanaan & pelaksanaan asesmen',
    },
    {
        'role': 'Manajer Manajemen Mutu',
        'name': 'Mohammad Riza Radyanto',
        'initials': 'RR',
        'note': 'Sistem manajemen mutu & audit internal',
    },
    {
        'role': 'Manajer Administrasi',
        'name': 'Nur Hidayah, S.E.',
        'initials': 'NH',
        'note': 'Keuangan & administrasi peserta',
    },
    {
        'role': 'Ketua Komite Skema',
        'name': 'Heru Bagiyo Susianto',
        'initials': 'HB',
        'note': 'Bertanggung jawab pada pengembangan skema',
    },
]


# ---------------------------------------------------------------------------
# Override dari panel admin (/admin/)
# ---------------------------------------------------------------------------
# Panel admin menulis data/content.json lewat Worker, lalu GitHub Actions
# menjalankan build.py sehingga perubahan langsung terbit di situs.
# Berkas ini tetap menjadi nilai awal (fallback) bila JSON belum ada/rusak.
# Set LSP_NO_OVERRIDE=1 untuk mengabaikan override (dipakai tools/export_content.py).
_LIST_OVERRIDES = {
    "nav": "NAV",
    "footer_nav": "NAV_FOOTER",
    "footer_legal": "NAV_LEGAL",
    "stats": "STATS",
    "advantages": "ADVANTAGES",
    "scheme_cats": "SCHEME_CATS",
    "schemes": "SCHEMES",
    "hero_roles": "HERO_ROLES",
    "ticker_items": "TICKER_ITEMS",
    "steps": "STEPS",
    "testimonials": "TESTIMONIALS",
    "asesor": "ASESOR",
    "tuk": "TUK",
    "jadwal": "JADWAL",
    "faq": "FAQ",
    "posts": "POSTS",
    "values": "VALUES",
    "struktur": "STRUKTUR",
}


def _apply_content_overrides() -> None:
    """Terapkan data/content.json (bila ada) di atas nilai bawaan modul."""
    import json
    import os
    from pathlib import Path

    if os.environ.get("LSP_NO_OVERRIDE"):
        return

    path = Path(__file__).resolve().parent / "data" / "content.json"
    if not path.is_file():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return
    if not isinstance(data, dict):
        return

    site = data.get("site")
    if isinstance(site, dict):
        for key, value in site.items():
            if key == "social" and isinstance(value, dict):
                for skey, svalue in value.items():
                    if skey in SITE["social"] and isinstance(svalue, str) and svalue.strip():
                        SITE["social"][skey] = svalue.strip()
                continue
            if key not in SITE or key == "social":
                continue
            if key == "logo" and isinstance(value, str):
                # Logo boleh dikosongkan dari panel admin.
                SITE[key] = value.strip()
                continue
            if isinstance(value, (str, int, float)) and str(value).strip():
                SITE[key] = value.strip() if isinstance(value, str) else value

    for json_key, module_name in _LIST_OVERRIDES.items():
        value = data.get(json_key)
        # Navigasi boleh dikosongkan lewat panel admin; daftar konten lain
        # tetap memakai nilai bawaan bila JSON berisi daftar kosong.
        if isinstance(value, list) and (value or json_key in {"nav", "footer_nav", "footer_legal"}):
            globals()[module_name][:] = value

    pages = data.get("pages")
    if isinstance(pages, list) and pages:
        by_slug = {p.get("slug", ""): p for p in pages if isinstance(p, dict)}
        updated = []
        for body_file, slug, title, desc, crumb in PAGES:
            patch = by_slug.get(slug) or {}
            updated.append((
                body_file,
                slug,
                (patch.get("title") or title).strip(),
                (patch.get("description") or desc).strip(),
                (patch.get("crumb") or crumb).strip(),
            ))
        PAGES[:] = updated

    page_html = data.get("page_html")
    if isinstance(page_html, dict):
        for slug, body in page_html.items():
            if isinstance(slug, str) and isinstance(body, str) and body.strip():
                PAGE_HTML[slug] = body


_apply_content_overrides()
