"""Konten situs LSP Patra Indo.

Semua data yang tampil di halaman dikumpulkan di sini agar mudah diperbarui
tanpa menyentuh markup. Lihat README.md untuk daftar data yang perlu diganti.
"""

# ---------------------------------------------------------------------------
# Identitas lembaga
# ---------------------------------------------------------------------------
SITE = {
    "name": "LSP Patra Indo",
    "legal": "Lembaga Sertifikasi Profesi Patra Indo",
    "domain": "lsppatraindo.id",
    "url": "https://lsppatraindo.id",
    "tagline": "Sertifikasi Kompetensi yang Diakui",
    "description": (
        "Lembaga Sertifikasi Profesi terlisensi BNSP untuk bidang pariwisata, "
        "perhotelan, kuliner, SPA, MICE, travel, dan ekonomi kreatif."
    ),
    "phone_display": "+62 812-3456-7890",
    "phone_link": "+6281234567890",
    "wa": "6281234567890",
    "email": "info@lsppatraindo.id",
    "email_sertifikasi": "sertifikasi@lsppatraindo.id",
    "address": "Gedung Patra Office Tower, Lantai 12, Jl. Gatot Subroto No. 123",
    "city": "Jakarta Selatan 12930",
    "hours": "Senin – Jumat, 08.00 – 17.00 WIB",
    "hours_sat": "Sabtu, 09.00 – 13.00 WIB",
    "maps_query": "Patra Office Tower, Jl. Gatot Subroto, Jakarta Selatan",
    "social": {
        "instagram": "https://instagram.com/lsppatraindo",
        "linkedin": "https://linkedin.com/company/lsppatraindo",
        "youtube": "https://youtube.com/@lsppatraindo",
        "facebook": "https://facebook.com/lsppatraindo",
    },
    "login_url": "https://siapkerja.kemnaker.go.id/",
    # URL Cloudflare Worker penyimpan formulir ke GitHub (lihat DEPLOY.md bagian 6).
    # Biarkan kosong bila formulir cukup dikirim ke WhatsApp.
    "form_endpoint": "",
    "founded": 2016,
}

# ---------------------------------------------------------------------------
# Navigasi
# ---------------------------------------------------------------------------
NAV = [
    {"label": "Beranda", "href": ""},
    {
        "label": "Profil",
        "children": [
            {"label": "Tentang Kami", "href": "tentang-kami/", "desc": "Sejarah, visi, misi, dan nilai lembaga"},
            {"label": "Struktur Organisasi", "href": "tentang-kami/#struktur", "desc": "Susunan pengurus dan manajemen"},
            {"label": "Daftar Asesor", "href": "daftar-asesor/", "desc": "Asesor kompetensi tersertifikasi BNSP"},
            {"label": "Tempat Uji Kompetensi", "href": "tuk/", "desc": "Lokasi TUK di berbagai kota"},
        ],
    },
    {
        "label": "Sertifikasi",
        "children": [
            {"label": "Skema Sertifikasi", "href": "skema-sertifikasi/", "desc": "Skema kompetensi di 7 bidang industri"},
            {"label": "Alur Sertifikasi", "href": "alur-sertifikasi/", "desc": "Lima langkah dari daftar hingga sertifikat"},
            {"label": "Persyaratan", "href": "persyaratan/", "desc": "Dokumen dan ketentuan peserta"},
            {"label": "Jadwal & Biaya", "href": "jadwal/", "desc": "Jadwal uji terdekat dan rincian biaya"},
            {"label": "FAQ", "href": "faq/", "desc": "Pertanyaan yang sering diajukan"},
        ],
    },
    {"label": "Jadwal & Biaya", "href": "jadwal/"},
    {"label": "Berita", "href": "berita/"},
    {"label": "Kontak", "href": "kontak/"},
]

# ---------------------------------------------------------------------------
# Halaman: (file body, slug/url, judul, deskripsi meta, label breadcrumb)
# ---------------------------------------------------------------------------
PAGES = [
    ("index", "", "LSP Patra Indo — Lembaga Sertifikasi Profesi Terlisensi BNSP",
     "Sertifikasi profesi resmi BNSP bidang pariwisata, perhotelan, kuliner, SPA, MICE, dan ekonomi kreatif. Proses terstruktur, asesor berpengalaman, sertifikat diakui nasional.",
     "Beranda"),
    ("tentang-kami", "tentang-kami", "Tentang Kami — Profil, Visi & Misi LSP Patra Indo",
     "Kenali LSP Patra Indo: lembaga sertifikasi profesi independen yang melaksanakan uji kompetensi berdasarkan SKKNI dan skema terlisensi BNSP.",
     "Tentang Kami"),
    ("skema-sertifikasi", "skema-sertifikasi", "Skema Sertifikasi — Daftar Skema Kompetensi BNSP",
     "Daftar skema sertifikasi LSP Patra Indo untuk bidang perhotelan, food & beverage, kuliner, SPA, MICE, travel, dan ekonomi kreatif.",
     "Skema Sertifikasi"),
    ("alur-sertifikasi", "alur-sertifikasi", "Alur Sertifikasi — Proses Uji Kompetensi 5 Langkah",
     "Alur pendaftaran dan uji kompetensi di LSP Patra Indo: konsultasi, registrasi, verifikasi, asesmen, hingga sertifikat terbit.",
     "Alur Sertifikasi"),
    ("persyaratan", "persyaratan", "Persyaratan Sertifikasi — Dokumen & Ketentuan Peserta",
     "Persyaratan umum, administrasi, dan dokumen portofolio yang perlu disiapkan peserta sertifikasi kompetensi LSP Patra Indo.",
     "Persyaratan"),
    ("daftar-asesor", "daftar-asesor", "Daftar Asesor Kompetensi — LSP Patra Indo",
     "Asesor kompetensi tersertifikasi BNSP di LSP Patra Indo beserta bidang keahlian dan wilayah kerja.",
     "Daftar Asesor"),
    ("tuk", "tuk", "Tempat Uji Kompetensi (TUK) — Lokasi & Fasilitas",
     "Daftar Tempat Uji Kompetensi LSP Patra Indo: TUK sewaktu, TUK tempat kerja, dan TUK mandiri di berbagai kota.",
     "Tempat Uji Kompetensi"),
    ("jadwal", "jadwal", "Jadwal Sertifikasi & Biaya — LSP Patra Indo",
     "Jadwal uji kompetensi terdekat, kuota, lokasi TUK, serta informasi biaya sertifikasi LSP Patra Indo.",
     "Jadwal & Biaya"),
    ("faq", "faq", "FAQ Sertifikasi — Pertanyaan yang Sering Diajukan",
     "Jawaban atas pertanyaan umum seputar pendaftaran, uji kompetensi, sertifikat, biaya, dan perpanjangan sertifikasi.",
     "FAQ"),
    ("berita", "berita", "Berita & Artikel — LSP Patra Indo",
     "Kabar kegiatan uji kompetensi, artikel industri, panduan sertifikasi, dan informasi terbaru dari LSP Patra Indo.",
     "Berita"),
    ("kontak", "kontak", "Kontak & Pendaftaran — LSP Patra Indo",
     "Hubungi LSP Patra Indo untuk konsultasi skema, jadwal uji kompetensi, kerja sama korporat, dan pendaftaran peserta.",
     "Kontak"),
]

# ---------------------------------------------------------------------------
# Statistik
# ---------------------------------------------------------------------------
STATS = [
    {"value": 23, "suffix": "+", "label": "Skema Sertifikasi", "note": "Terlisensi BNSP"},
    {"value": 40, "suffix": "+", "label": "Asesor Kompetensi", "note": "Tersertifikasi BNSP"},
    {"value": 3500, "suffix": "+", "label": "Peserta Tersertifikasi", "note": "Sejak 2016"},
    {"value": 150, "suffix": "+", "label": "Mitra Industri", "note": "Hotel, travel, F&B"},
]

# ---------------------------------------------------------------------------
# Keunggulan
# ---------------------------------------------------------------------------
ADVANTAGES = [
    {
        "icon": "shield",
        "title": "Lisensi Resmi BNSP",
        "text": "Seluruh proses asesmen mengacu pada skema yang terlisensi Badan Nasional Sertifikasi Profesi dan regulasi ketenagakerjaan.",
    },
    {
        "icon": "users",
        "title": "Asesor Berpengalaman",
        "text": "Asesor kami tersertifikasi BNSP dan aktif di industri, sehingga penilaian relevan dengan praktik kerja nyata.",
    },
    {
        "icon": "route",
        "title": "Proses Transparan",
        "text": "Alur, biaya, dan jadwal disampaikan sejak awal. Status pendaftaran dapat dipantau melalui admin pendamping.",
    },
    {
        "icon": "award",
        "title": "Sertifikat Diakui",
        "text": "Sertifikat kompetensi tercatat di sistem SIAPkerja Kemnaker dan diakui lintas industri, termasuk ASEAN.",
    },
]

# ---------------------------------------------------------------------------
# Skema sertifikasi
# ---------------------------------------------------------------------------
SCHEME_CATS = [
    {"id": "hotel", "label": "Perhotelan", "icon": "bed", "desc": "Housekeeping, front office, dan layanan tamu"},
    {"id": "fbs", "label": "Food & Beverage", "icon": "cup", "desc": "Layanan restoran, bar, dan kafe"},
    {"id": "kuliner", "label": "Kuliner & Pastry", "icon": "chef", "desc": "Pengolahan makanan dan pastry"},
    {"id": "spa", "label": "SPA & Wellness", "icon": "spark", "desc": "Terapi dan perawatan tubuh"},
    {"id": "mice", "label": "MICE & Event", "icon": "calendar", "desc": "Penyelenggaraan acara dan konferensi"},
    {"id": "travel", "label": "Travel & Tour", "icon": "globe", "desc": "Kepemanduan, ticketing, dan biro perjalanan"},
    {"id": "kreatif", "label": "Ekonomi Kreatif", "icon": "palette", "desc": "Pemasaran dan pengelolaan destinasi"},
]

SCHEMES = [
    {"name": "Resepsionis (Front Office)", "cat": "hotel", "level": "KKNI II", "units": 9, "featured": True,
     "desc": "Mengelola reservasi, penerimaan tamu, komunikasi telepon, dan administrasi front office."},
    {"name": "Room Attendant", "cat": "hotel", "level": "KKNI II", "units": 8, "featured": True,
     "desc": "Membersihkan dan menyiapkan kamar tamu sesuai standar kebersihan dan prosedur hotel."},
    {"name": "Public Area Cleaner", "cat": "hotel", "level": "KKNI II", "units": 6,
     "desc": "Menjaga kebersihan area umum, peralatan, dan bahan pembersih secara aman."},
    {"name": "Laundry Attendant", "cat": "hotel", "level": "KKNI II", "units": 7,
     "desc": "Menangani pencucian, penyetrikaan, dan penyimpanan linen serta pakaian tamu."},
    {"name": "Bell Boy", "cat": "hotel", "level": "KKNI II", "units": 6,
     "desc": "Menangani bagasi tamu, pengantaran, dan layanan pendukung di lobi."},

    {"name": "Waiter / Waitress", "cat": "fbs", "level": "KKNI II", "units": 8, "featured": True,
     "desc": "Melayani tamu di restoran, mulai dari penyambutan hingga penanganan pembayaran."},
    {"name": "Bartender", "cat": "fbs", "level": "KKNI III", "units": 9,
     "desc": "Menyiapkan minuman beralkohol dan non-alkohol, mengelola bar, serta menjaga standar higienitas."},
    {"name": "Barista", "cat": "fbs", "level": "KKNI II", "units": 8, "featured": True,
     "desc": "Mengoperasikan mesin espresso, menyajikan kopi, dan menjaga kualitas produk kafe."},
    {"name": "Supervisor F&B Service", "cat": "fbs", "level": "KKNI IV", "units": 11,
     "desc": "Mengawasi operasional layanan, menyusun jadwal, dan memastikan standar pelayanan."},

    {"name": "Cook (Commis)", "cat": "kuliner", "level": "KKNI II", "units": 9, "featured": True,
     "desc": "Menyiapkan bahan, mengolah masakan dasar, dan menjaga higiene di area dapur."},
    {"name": "Demi Chef", "cat": "kuliner", "level": "KKNI III", "units": 10,
     "desc": "Memimpin satu bagian dapur, mengendalikan porsi, dan mengawasi kualitas hidangan."},
    {"name": "Chef de Partie", "cat": "kuliner", "level": "KKNI IV", "units": 11,
     "desc": "Mengelola section dapur, menyusun menu, dan mengendalikan biaya bahan makanan."},
    {"name": "Commis Pastry", "cat": "kuliner", "level": "KKNI II", "units": 8,
     "desc": "Membuat roti, kue, dan dessert sesuai resep standar serta prosedur penyimpanan."},

    {"name": "Spa Therapist", "cat": "spa", "level": "KKNI III", "units": 9, "featured": True,
     "desc": "Melakukan terapi pijat, perawatan tubuh, dan wajah sesuai standar keselamatan kerja."},
    {"name": "Supervisor SPA", "cat": "spa", "level": "KKNI IV", "units": 10,
     "desc": "Mengelola operasional spa, mengatur terapis, dan menjaga kepuasan tamu."},

    {"name": "Event Planner", "cat": "mice", "level": "KKNI IV", "units": 10, "featured": True,
     "desc": "Merancang konsep acara, menyusun anggaran, dan mengoordinasikan pelaksanaan event."},
    {"name": "Conference Liaison Officer", "cat": "mice", "level": "KKNI III", "units": 7,
     "desc": "Menjadi penghubung peserta konferensi, mengatur registrasi, dan mendampingi narasumber."},

    {"name": "Pramuwisata (Tour Guide)", "cat": "travel", "level": "KKNI III", "units": 9, "featured": True,
     "desc": "Memandu wisatawan, menyampaikan interpretasi destinasi, dan menangani situasi darurat."},
    {"name": "Travel Consultant", "cat": "travel", "level": "KKNI III", "units": 8,
     "desc": "Menyusun paket perjalanan, menangani reservasi, dan memberikan konsultasi kepada pelanggan."},
    {"name": "Ticketing Officer", "cat": "travel", "level": "KKNI II", "units": 7,
     "desc": "Menerbitkan tiket, menghitung tarif, dan menangani perubahan jadwal penerbangan."},
    {"name": "Tour Leader", "cat": "travel", "level": "KKNI IV", "units": 10,
     "desc": "Memimpin rombongan wisata, mengelola itinerary, dan memastikan kepatuhan prosedur."},

    {"name": "Konsultan Pemasaran Pariwisata", "cat": "kreatif", "level": "KKNI IV", "units": 9,
     "desc": "Menyusun strategi pemasaran destinasi dan mengukur efektivitas kampanye wisata."},
    {"name": "Pengelola Desa Wisata", "cat": "kreatif", "level": "KKNI III", "units": 11,
     "desc": "Mengelola daya tarik desa wisata, memberdayakan masyarakat, dan menjaga keberlanjutan."},
]

# ---------------------------------------------------------------------------
# Teks bergerak (ticker & rotator hero)
# ---------------------------------------------------------------------------
HERO_ROLES = [
    "Perhotelan",
    "Food & Beverage",
    "Kuliner & Pastry",
    "SPA & Wellness",
    "MICE & Event",
    "Travel & Tour",
    "Ekonomi Kreatif",
]

TICKER_ITEMS = [
    {"text": "Terlisensi BNSP", "outline": False},
    {"text": "Diakui Nasional", "outline": True},
    {"text": f"{len(SCHEMES)} Skema Sertifikasi", "outline": False},
    {"text": "Asesor Bersertifikat", "outline": True},
    {"text": "E-Sertifikat SIAPkerja", "outline": False},
    {"text": "Uji Kompetensi Terstruktur", "outline": True},
]

# ---------------------------------------------------------------------------
# Alur sertifikasi
# ---------------------------------------------------------------------------
STEPS = [
    {"no": "01", "title": "Pilih Skema & Konsultasi", "duration": "Hari 1",
     "text": "Tentukan skema sesuai pengalaman kerja Anda, lalu konsultasikan dengan admin kami untuk memastikan kesesuaian dan ketersediaan jadwal."},
    {"no": "02", "title": "Registrasi & Unggah Dokumen", "duration": "Hari 1–2",
     "text": "Buat akun SIAPkerja, isi formulir pendaftaran, dan unggah dokumen persyaratan melalui halaman pendaftaran."},
    {"no": "03", "title": "Verifikasi & Pembayaran", "duration": "Hari 2–5",
     "text": "Tim kami memverifikasi kelengkapan administrasi. Setelah dinyatakan lengkap, lakukan pembayaran untuk mengunci kuota dan jadwal."},
    {"no": "04", "title": "Uji Kompetensi", "duration": "1–2 hari",
     "text": "Asesmen mandiri, observasi praktik, wawancara, dan penilaian portofolio bersama asesor di TUK yang ditetapkan."},
    {"no": "05", "title": "Pleno & Penerbitan Sertifikat", "duration": "4–7 minggu",
     "text": "Rapat pleno menetapkan keputusan kompeten, kemudian sertifikat diterbitkan BNSP dan tersedia di akun SIAPkerja Anda."},
]

# ---------------------------------------------------------------------------
# Testimoni
# ---------------------------------------------------------------------------
TESTIMONIALS = [
    {"name": "Dika Nanda P.", "role": "Kepala Koki, SPPG Pandean",
     "quote": "Prosesnya cepat dan asesornya sangat kompeten. Saya merekomendasikan sertifikasi di LSP Patra Indo untuk rekan-rekan yang ingin mengakui pengalaman kerjanya secara formal.",
     "initials": "DN", "tone": "teal"},
    {"name": "Wahyu Prasetyo", "role": "Koordinator Operasional Desa Wisata",
     "quote": "Awalnya ragu bisa menjawab pertanyaan asesor, tetapi pendampingan dilakukan dengan bahasa yang sederhana sehingga mudah dipahami dan saya jadi lebih percaya diri.",
     "initials": "WP", "tone": "gold"},
    {"name": "Yunani Rahmawati", "role": "Spa Therapist, Hotel Bintang Lima",
     "quote": "Setelah mengikuti uji kompetensi, saya lebih yakin dengan standar kerja saya. Ilmu yang didapat langsung terasa manfaatnya di tempat kerja.",
     "initials": "YR", "tone": "navy"},
]

# ---------------------------------------------------------------------------
# Asesor
# ---------------------------------------------------------------------------
ASESOR = [
    {"name": "Ahmad Fauzi, S.Par.", "initials": "AF", "field": "Perhotelan & Housekeeping", "city": "Jakarta", "year": 2017},
    {"name": "Siti Rahmawati, M.M.", "initials": "SR", "field": "Food & Beverage Service", "city": "Jakarta", "year": 2018},
    {"name": "Bagus Prakoso, S.Tr.Par.", "initials": "BP", "field": "Kuliner & Pastry", "city": "Bandung", "year": 2018},
    {"name": "Dewi Lestari, S.Psi.", "initials": "DL", "field": "SPA & Wellness", "city": "Yogyakarta", "year": 2019},
    {"name": "Rizky Ananda, M.Par.", "initials": "RA", "field": "MICE & Event Management", "city": "Jakarta", "year": 2017},
    {"name": "Putu Arini, S.St.Par.", "initials": "PA", "field": "Kepemanduan Wisata", "city": "Denpasar", "year": 2019},
    {"name": "Hendra Wijaya, M.B.A.", "initials": "HW", "field": "Travel & Ticketing", "city": "Surabaya", "year": 2020},
    {"name": "Maya Kusuma, S.E.", "initials": "MK", "field": "Ekonomi Kreatif & Pemasaran", "city": "Jakarta", "year": 2020},
]

# ---------------------------------------------------------------------------
# Tempat Uji Kompetensi
# ---------------------------------------------------------------------------
TUK = [
    {"name": "TUK Patra Indo Jakarta", "city": "Jakarta Selatan", "type": "TUK Sewaktu",
     "address": "Gedung Patra Office Tower, Lantai 12, Jl. Gatot Subroto No. 123", "schemes": 12},
    {"name": "TUK Patra Indo Bandung", "city": "Bandung", "type": "TUK Sewaktu",
     "address": "Jl. Asia Afrika No. 88, Sumur Bandung", "schemes": 8},
    {"name": "TUK Patra Indo Yogyakarta", "city": "Yogyakarta", "type": "TUK Sewaktu",
     "address": "Jl. Malioboro No. 45, Gedongtengen", "schemes": 7},
    {"name": "TUK Patra Indo Bali", "city": "Denpasar", "type": "TUK Sewaktu",
     "address": "Jl. Sunset Road No. 21, Kuta", "schemes": 9},
    {"name": "TUK Patra Indo Surabaya", "city": "Surabaya", "type": "TUK Sewaktu",
     "address": "Jl. Basuki Rahmat No. 101, Genteng", "schemes": 6},
    {"name": "TUK Mitra Hotel Nusantara", "city": "Jakarta Pusat", "type": "TUK Tempat Kerja",
     "address": "Kawasan industri perhotelan, Jl. MH Thamrin", "schemes": 5},
]

# ---------------------------------------------------------------------------
# Jadwal
# ---------------------------------------------------------------------------
JADWAL = [
    {"date": "12 Nov 2026", "scheme": "Resepsionis (Front Office)", "tuk": "Jakarta", "mode": "Hybrid", "quota": 20, "status": "open"},
    {"date": "18 Nov 2026", "scheme": "Barista", "tuk": "Bandung", "mode": "Offline", "quota": 16, "status": "open"},
    {"date": "25 Nov 2026", "scheme": "Cook (Commis)", "tuk": "Jakarta", "mode": "Offline", "quota": 12, "status": "almost"},
    {"date": "02 Des 2026", "scheme": "Spa Therapist", "tuk": "Yogyakarta", "mode": "Offline", "quota": 20, "status": "open"},
    {"date": "09 Des 2026", "scheme": "Pramuwisata (Tour Guide)", "tuk": "Bali", "mode": "Hybrid", "quota": 24, "status": "open"},
    {"date": "16 Des 2026", "scheme": "Event Planner", "tuk": "Jakarta", "mode": "Online", "quota": 18, "status": "wait"},
    {"date": "13 Jan 2027", "scheme": "Room Attendant", "tuk": "Surabaya", "mode": "Offline", "quota": 20, "status": "open"},
    {"date": "20 Jan 2027", "scheme": "Travel Consultant", "tuk": "Jakarta", "mode": "Online", "quota": 22, "status": "open"},
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
    {"q": "Apa itu sertifikasi kompetensi dan mengapa penting?",
     "a": "Sertifikasi kompetensi adalah proses pengakuan formal atas kemampuan kerja seseorang sesuai Standar Kompetensi Kerja Nasional Indonesia (SKKNI). Sertifikat ini menjadi bukti objektif kompetensi Anda bagi pemberi kerja, klien, dan mitra bisnis."},
    {"q": "Siapa yang dapat mengikuti sertifikasi di LSP Patra Indo?",
     "a": "Peserta dapat berasal dari tenaga kerja aktif, lulusan pendidikan vokasi, mahasiswa tingkat akhir, pelaku usaha, maupun individu yang ingin mengakui pengalaman kerjanya. Syarat utama adalah memenuhi persyaratan skema yang dipilih."},
    {"q": "Apakah harus memiliki akun SIAPkerja?",
     "a": "Ya. Akun SIAPkerja Kementerian Ketenagakerjaan diperlukan karena sertifikat kompetensi diterbitkan dalam bentuk elektronik dan tersimpan pada akun tersebut. Pembuatan akun gratis melalui siapkerja.kemnaker.go.id."},
    {"q": "Berapa lama proses hingga sertifikat terbit?",
     "a": "Rata-rata 4–7 minggu setelah uji kompetensi, tergantung penyelesaian rapat pleno dan penerbitan blanko oleh BNSP. Kami akan menginformasikan status secara berkala melalui admin pendamping."},
    {"q": "Berapa biaya sertifikasi?",
     "a": "Biaya berbeda untuk setiap skema dan lokasi TUK, serta dapat berubah sesuai ketentuan BNSP. Silakan hubungi admin untuk mendapatkan rincian biaya resmi dan opsi pembayaran bertahap."},
    {"q": "Apakah uji kompetensi bisa dilakukan secara online?",
     "a": "Sebagian asesmen dapat dilakukan secara daring, namun skema dengan komponen praktik tetap memerlukan kehadiran di TUK. Metode asesmen akan diinformasikan saat konfirmasi jadwal."},
    {"q": "Bagaimana jika hasil asesmen belum kompeten?",
     "a": "Peserta diberikan umpan balik dan kesempatan untuk melakukan asesmen ulang pada unit yang belum kompeten sesuai ketentuan, dengan biaya dan jadwal yang diinformasikan oleh admin."},
    {"q": "Bagaimana prosedur banding atau keberatan?",
     "a": "Peserta dapat mengajukan banding maksimal 7 hari kerja setelah keputusan pleno disampaikan. Prosedur lengkap diatur dalam dokumen Alur Banding yang dapat diminta kepada admin."},
    {"q": "Apakah sertifikat perlu diperbarui?",
     "a": "Masa berlaku sertifikat umumnya 3 tahun. Perpanjangan dapat dilakukan melalui skema sertifikasi ulang (re-sertifikasi) dengan menyerahkan bukti portofolio kegiatan kerja terkini."},
    {"q": "Apakah LSP Patra Indo menerima kerja sama korporat?",
     "a": "Ya. Kami melayani sertifikasi in-house untuk hotel, restoran, travel agency, dan institusi pendidikan dengan jadwal serta skema yang disesuaikan kebutuhan organisasi."},
]

# ---------------------------------------------------------------------------
# Berita
# ---------------------------------------------------------------------------
POSTS = [
    {"title": "Pembukaan Kelas Sertifikasi Batch November 2026", "date": "2026-10-20", "cat": "Pengumuman",
     "image": "train", "excerpt": "Pendaftaran kelas sertifikasi batch November 2026 resmi dibuka untuk sembilan skema prioritas dengan kuota terbatas."},
    {"title": "Mengapa Sertifikat Kompetensi Penting di Industri Perhotelan", "date": "2026-10-12", "cat": "Artikel",
     "image": "hotel", "excerpt": "Industri perhotelan semakin selektif dalam merekrut. Sertifikat kompetensi menjadi pembeda yang objektif di tahap seleksi."},
    {"title": "Uji Kompetensi Kepemanduan Wisata Digelar di TUK Bali", "date": "2026-10-05", "cat": "Kegiatan",
     "image": "guide", "excerpt": "Sebanyak 24 peserta mengikuti uji kompetensi skema Pramuwisata dengan metode observasi lapangan dan wawancara."},
    {"title": "Panduan Lengkap Membuat Akun SIAPkerja untuk Peserta", "date": "2026-09-28", "cat": "Panduan",
     "image": "about", "excerpt": "Langkah demi langkah membuat akun SIAPkerja, melengkapi profil, hingga memastikan data siap untuk penerbitan sertifikat."},
    {"title": "Standar Kompetensi Barista: Apa yang Diuji?", "date": "2026-09-15", "cat": "Artikel",
     "image": "fb", "excerpt": "Dari kalibrasi grinder hingga konsistensi ekstraksi, ini cakupan asesmen yang perlu Anda kuasai."},
    {"title": "Tips Lulus Uji Kompetensi Melalui Asesmen Mandiri", "date": "2026-09-01", "cat": "Tips",
     "image": "culinary", "excerpt": "Asesmen mandiri bukan formalitas. Cara mengisinya menentukan arah pembuktian kompetensi Anda di hadapan asesor."},
]

# ---------------------------------------------------------------------------
# Nilai & struktur
# ---------------------------------------------------------------------------
VALUES = [
    {"icon": "shield", "title": "Integritas", "text": "Menjunjung kejujuran dan konsistensi antara aturan, proses, dan keputusan."},
    {"icon": "scale", "title": "Independensi", "text": "Bebas dari pengaruh komersial maupun kepentingan pihak yang diases."},
    {"icon": "check-circle", "title": "Objektivitas", "text": "Keputusan berbasis bukti dan standar kompetensi, bukan opini pribadi."},
    {"icon": "lock", "title": "Kerahasiaan", "text": "Melindungi data peserta dan informasi organisasi klien."},
    {"icon": "award", "title": "Kompetensi", "text": "Personel asesmen dipilih dan dipantau sesuai kualifikasi BNSP."},
    {"icon": "bolt", "title": "Responsif", "text": "Layanan administrasi yang cepat, jelas, dan mudah diakses."},
]

STRUKTUR = [
    {"role": "Direktur", "name": "Drs. Bambang Setiawan, M.M.", "initials": "BS", "note": "Penanggung jawab lembaga"},
    {"role": "Manajer Sertifikasi", "name": "Rina Kartika, S.Par.", "initials": "RK", "note": "Perencanaan & pelaksanaan asesmen"},
    {"role": "Manajer Mutu", "name": "Agus Salim, S.T.", "initials": "AS", "note": "Sistem manajemen mutu & audit internal"},
    {"role": "Manajer Administrasi", "name": "Nur Hidayah, S.E.", "initials": "NH", "note": "Keuangan & administrasi peserta"},
    {"role": "Ketua Komite Imparsialitas", "name": "Prof. Dr. Hendro Wibowo", "initials": "HW", "note": "Pengawasan ketidakberpihakan"},
    {"role": "Koordinator TUK", "name": "Yoga Pratama, S.Tr.Par.", "initials": "YP", "note": "Kesiapan sarana & fasilitas uji"},
]
