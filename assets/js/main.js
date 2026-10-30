/* ==========================================================================
   LSP Patra Indo — main.js
   Navigasi, animasi, filter skema, penghitung statistik, formulir WhatsApp
   ========================================================================== */
(function () {
  'use strict';

  var doc = document;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  doc.documentElement.classList.add('js');

  /* ---------------------------------------------------------------------
     1. Header shadow saat halaman digulir
     --------------------------------------------------------------------- */
  var header = doc.getElementById('siteHeader');
  var toTop = doc.querySelector('.to-top');
  var lastScroll = 0;

  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle('is-scrolled', y > 8);
    if (toTop) toTop.classList.toggle('is-visible', y > 700);
    lastScroll = y;
  }
  var progressBar = doc.querySelector('.scroll-progress > i');

  function updateProgress() {
    if (!progressBar) return;
    var max = doc.documentElement.scrollHeight - window.innerHeight;
    var pct = max > 0 ? Math.min((window.scrollY || 0) / max, 1) * 100 : 0;
    progressBar.style.width = pct + '%';
  }

  window.addEventListener('scroll', function () {
    onScroll();
    updateProgress();
  }, { passive: true });
  window.addEventListener('resize', updateProgress, { passive: true });
  onScroll();
  updateProgress();

  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  }

  /* ---------------------------------------------------------------------
     2. Navigasi mobile
     --------------------------------------------------------------------- */
  var nav = doc.getElementById('primaryNav');
  var toggle = doc.querySelector('.nav-toggle');
  var closeBtn = doc.querySelector('.nav__close');
  var backdrop = doc.querySelector('.nav-backdrop');
  var body = doc.body;

  function openNav() {
    if (!nav || !toggle) return;
    nav.classList.add('is-open');
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Tutup menu');
    if (backdrop) backdrop.hidden = false;
    body.classList.add('nav-open');
    var first = nav.querySelector('.nav__close');
    if (first) first.focus({ preventScroll: true });
  }

  function closeNav(returnFocus) {
    if (!nav || !toggle) return;
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Buka menu');
    if (backdrop) backdrop.hidden = true;
    body.classList.remove('nav-open');
    if (returnFocus) toggle.focus({ preventScroll: true });
  }

  if (toggle) {
    toggle.addEventListener('click', function () {
      var isOpen = nav.classList.contains('is-open');
      isOpen ? closeNav(true) : openNav();
    });
  }
  if (closeBtn) closeBtn.addEventListener('click', function () { closeNav(true); });
  if (backdrop) backdrop.addEventListener('click', function () { closeNav(true); });

  doc.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav && nav.classList.contains('is-open')) closeNav(true);
  });

  /* Submenu: klik (desktop & mobile), hover tetap bekerja di desktop */
  doc.querySelectorAll('.has-mega > .nav__toggle').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var parent = btn.parentElement;
      var isMobile = window.matchMedia('(max-width: 1080px)').matches;
      var willOpen = !parent.classList.contains('is-open');

      doc.querySelectorAll('.has-mega.is-open').forEach(function (other) {
        if (other !== parent) {
          other.classList.remove('is-open');
          var b = other.querySelector('.nav__toggle');
          if (b) b.setAttribute('aria-expanded', 'false');
        }
      });

      parent.classList.toggle('is-open', willOpen);
      btn.setAttribute('aria-expanded', String(willOpen));
      if (isMobile && willOpen) {
        var firstLink = parent.querySelector('.mega__link');
        if (firstLink) firstLink.focus({ preventScroll: true });
      }
    });
  });

  /* Tutup menu setelah memilih tautan */
  if (nav) {
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        if (nav.classList.contains('is-open')) closeNav(false);
      });
    });
  }

  window.addEventListener('resize', function () {
    if (window.innerWidth > 1080 && nav && nav.classList.contains('is-open')) closeNav(false);
  }, { passive: true });

  /* ---------------------------------------------------------------------
     3. Animasi muncul saat digulir
     --------------------------------------------------------------------- */
  var revealEls = Array.prototype.slice.call(doc.querySelectorAll('[data-reveal]'));
  var pendingReveal = revealEls.slice();
  var revealObserver = null;

  function showReveal(el) {
    if (el.classList.contains('is-in')) return;
    var group = el.closest('[data-reveal-group]');
    if (group) {
      var siblings = Array.prototype.slice.call(group.querySelectorAll('[data-reveal]'));
      el.style.setProperty('--delay', Math.min(siblings.indexOf(el), 6) * 70 + 'ms');
    }
    el.classList.add('is-in');
    var idx = pendingReveal.indexOf(el);
    if (idx > -1) pendingReveal.splice(idx, 1);
    if (revealObserver) revealObserver.unobserve(el);
  }

  if (!('IntersectionObserver' in window) || reduceMotion) {
    revealEls.forEach(showReveal);
  } else {
    revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) showReveal(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    revealEls.forEach(function (el) { revealObserver.observe(el); });
  }

  /* ---------------------------------------------------------------------
     4. Penghitung statistik
     --------------------------------------------------------------------- */
  var counters = Array.prototype.slice.call(doc.querySelectorAll('[data-count]'));

  function formatNumber(n) {
    return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  }

  function runCounter(el) {
    var target = parseInt(el.getAttribute('data-count'), 10) || 0;
    if (reduceMotion) { el.textContent = formatNumber(target); return; }
    var duration = 1400;
    var start = null;

    function tick(ts) {
      if (!start) start = ts;
      var progress = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = formatNumber(target * eased);
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  if ('IntersectionObserver' in window && counters.length) {
    var countObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        runCounter(entry.target);
        countObserver.unobserve(entry.target);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { countObserver.observe(el); });
  } else {
    counters.forEach(function (el) { el.textContent = formatNumber(el.getAttribute('data-count')); });
  }

  /* ---------------------------------------------------------------------
     5. Filter skema sertifikasi
     --------------------------------------------------------------------- */
  var filterBar = doc.querySelector('.filter-bar');
  if (filterBar) {
    var chips = Array.prototype.slice.call(filterBar.querySelectorAll('[data-filter]'));
    var cards = Array.prototype.slice.call(doc.querySelectorAll('[data-cat]'));
    var countEl = doc.querySelector('[data-scheme-count]');
    var searchEl = doc.querySelector('[data-scheme-search]');
    var emptyEl = doc.querySelector('[data-scheme-empty]');
    var activeCat = 'all';

    function cardText(card) {
      return (card.textContent || '').toLowerCase().replace(/\s+/g, ' ');
    }

    function applyFilter(cat, query) {
      var q = (query || '').trim().toLowerCase();
      var shown = 0;

      cards.forEach(function (card) {
        var matchCat = cat === 'all' || card.getAttribute('data-cat') === cat;
        var matchText = !q || cardText(card).indexOf(q) !== -1;
        var match = matchCat && matchText;
        card.hidden = !match;
        if (match) shown++;
      });

      chips.forEach(function (c) {
        var active = c.getAttribute('data-filter') === cat;
        c.classList.toggle('is-active', active);
        c.setAttribute('aria-pressed', String(active));
      });

      if (countEl) countEl.textContent = shown + ' skema ditampilkan';
      if (emptyEl) emptyEl.hidden = shown !== 0;
    }

    function syncUrl(cat) {
      if (!history.replaceState) return;
      var url = cat === 'all' ? location.pathname : '#' + cat;
      history.replaceState(null, '', url);
    }

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        activeCat = chip.getAttribute('data-filter');
        applyFilter(activeCat, searchEl ? searchEl.value : '');
        syncUrl(activeCat);
      });
    });

    if (searchEl) {
      var debounce;
      searchEl.addEventListener('input', function () {
        clearTimeout(debounce);
        debounce = setTimeout(function () {
          applyFilter(activeCat, searchEl.value);
        }, 120);
      });
      searchEl.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
          searchEl.value = '';
          applyFilter(activeCat, '');
        }
      });
    }

    var hash = location.hash.replace('#', '');
    var validHash = chips.some(function (c) { return c.getAttribute('data-filter') === hash; });
    activeCat = validHash ? hash : 'all';
    applyFilter(activeCat, '');
  }

  /* ---------------------------------------------------------------------
     6. Formulir pendaftaran -> WhatsApp
     --------------------------------------------------------------------- */
  var form = doc.querySelector('[data-wa-form]');
  if (form) {
    var status = form.querySelector('.form-status');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      var data = new FormData(form);
      var fields = {
        nama: String(data.get('nama') || '').trim(),
        telepon: String(data.get('telepon') || '').trim(),
        email: String(data.get('email') || '').trim(),
        skema: String(data.get('skema') || '').trim(),
        pesan: String(data.get('pesan') || '').trim()
      };
      var name = fields.nama;
      var phone = fields.telepon;
      var email = fields.email;
      var scheme = fields.skema;
      var message = fields.pesan;

      /* Simpan kiriman ke repositori GitHub melalui Cloudflare Worker.
         Endpoint diatur di site_data.py (SITE["form_endpoint"]). Dikirim
         tanpa ditunggu agar tab WhatsApp tidak diblokir peramban. */
      var endpoint = form.getAttribute('data-endpoint');
      if (endpoint) {
        try {
          fetch(endpoint, {
            method: 'POST',
            mode: 'cors',
            keepalive: true,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              nama: name,
              telepon: phone,
              email: email,
              skema: scheme,
              pesan: message,
              _gotcha: String(data.get('_gotcha') || '')
            })
          }).catch(function () {});
        } catch (err) { /* diabaikan — WhatsApp tetap dibuka */ }
      }

      var lines = [
        'Halo LSP Patra Indo, saya ingin mendaftar sertifikasi.',
        '',
        'Nama: ' + name,
        'No. WhatsApp: ' + phone,
        'Email: ' + email,
        'Skema: ' + scheme
      ];
      if (message) lines.push('Catatan: ' + message);
      lines.push('', 'Mohon informasi persyaratan dan jadwal terdekat. Terima kasih.');

      var url = 'https://wa.me/' + form.getAttribute('data-wa') + '?text=' + encodeURIComponent(lines.join('\n'));

      if (status) {
        status.textContent = 'Membuka WhatsApp… Jika tidak terbuka otomatis, hubungi ' +
          form.getAttribute('data-phone') + '.';
        status.classList.add('is-visible');
      }
      window.open(url, '_blank', 'noopener');
    });
  }

  /* ---------------------------------------------------------------------
     7. Menandai tautan navigasi sesuai posisi gulir (halaman beranda)
     --------------------------------------------------------------------- */
  var sections = Array.prototype.slice.call(doc.querySelectorAll('section[id]'));
  var navLinks = Array.prototype.slice.call(doc.querySelectorAll('.nav__list > .nav__item > .nav__link[href*="#"]'));

  if (sections.length && navLinks.length && 'IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (link) {
          var href = link.getAttribute('href') || '';
          link.classList.toggle('is-active', href.endsWith('#' + entry.target.id));
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---------------------------------------------------------------------
     8. Tombol "Daftar" pada jadwal: teruskan nama skema ke formulir
     --------------------------------------------------------------------- */
  var schemeSelect = doc.querySelector('select[name="skema"]');
  if (schemeSelect) {
    doc.querySelectorAll('[data-pick-scheme]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var value = btn.getAttribute('data-pick-scheme');
        var options = Array.prototype.map.call(schemeSelect.options, function (o) { return o.value; });
        if (options.indexOf(value) !== -1) schemeSelect.value = value;
      });
    });
  }

  /* ---------------------------------------------------------------------
     9. Rotator kata pada hero (efek mengetik)
     --------------------------------------------------------------------- */
  var rotatorEl = doc.querySelector('[data-rotator]');
  if (rotatorEl) {
    var words = null;
    try { words = JSON.parse(rotatorEl.getAttribute('data-rotator')); } catch (err) { words = null; }

    if (words && words.length && !reduceMotion) {
      var state = { index: 0, char: words[0].length, deleting: true };
      var timer = null;

      var paint = function () {
        rotatorEl.textContent = words[state.index].slice(0, state.char);
      };

      var wait = function (ms) {
        timer = setTimeout(step, ms);
      };

      var step = function () {
        var word = words[state.index];

        if (!state.deleting) {
          state.char++;
          paint();
          if (state.char >= word.length) {
            state.deleting = true;
            wait(1900);
          } else {
            wait(52 + Math.random() * 46);
          }
        } else {
          state.char--;
          paint();
          if (state.char <= 0) {
            state.deleting = false;
            state.index = (state.index + 1) % words.length;
            wait(140);
          } else {
            wait(28);
          }
        }
      };

      paint();
      wait(1900);

      doc.addEventListener('visibilitychange', function () {
        clearTimeout(timer);
        if (!doc.hidden) wait(500);
      });
    }
  }

  /* ---------------------------------------------------------------------
     10. Reveal judul per kata
     --------------------------------------------------------------------- */
  var splitEls = Array.prototype.slice.call(doc.querySelectorAll('[data-split]'));

  function splitWords(root) {
    var walker = doc.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
    var nodes = [];
    while (walker.nextNode()) {
      if (walker.currentNode.nodeValue.trim()) nodes.push(walker.currentNode);
    }

    nodes.forEach(function (node) {
      var frag = doc.createDocumentFragment();
      node.nodeValue.split(/(\s+)/).forEach(function (part) {
        if (!part) return;
        if (/^\s+$/.test(part)) {
          frag.appendChild(doc.createTextNode(part));
          return;
        }
        var outer = doc.createElement('span');
        outer.className = 'sw';
        var inner = doc.createElement('span');
        inner.className = 'sw__i';
        inner.textContent = part;
        outer.appendChild(inner);
        frag.appendChild(outer);
      });
      node.parentNode.replaceChild(frag, node);
    });

    return Array.prototype.slice.call(root.querySelectorAll('.sw__i'));
  }

  var splitReady = [];
  var pendingSplit = [];
  var splitObserver = null;

  function markSplit(item) {
    if (item.el.classList.contains('is-split')) return;
    item.el.classList.add('is-split');
    var idx = pendingSplit.indexOf(item);
    if (idx > -1) pendingSplit.splice(idx, 1);
    if (splitObserver) splitObserver.unobserve(item.el);
  }

  if (splitEls.length) {
    splitEls.forEach(function (el) {
      var wordEls = splitWords(el);
      wordEls.forEach(function (w, i) {
        w.style.setProperty('--d', Math.min(i, 10) * 30 + 'ms');
      });
      splitReady.push({ el: el, words: wordEls });
    });

    if (reduceMotion || !('IntersectionObserver' in window)) {
      splitReady.forEach(markSplit);
    } else {
      splitObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var item = splitReady.filter(function (it) { return it.el === entry.target; })[0];
          if (item) markSplit(item);
        });
      }, { threshold: 0.15, rootMargin: '0px 0px -30px 0px' });

      splitReady.forEach(function (item) {
        pendingSplit.push(item);
        splitObserver.observe(item.el);
      });
    }
  }

  /* ---------------------------------------------------------------------
     11. Jaring pengaman: konten tidak boleh tertinggal tersembunyi
         saat pengguna melompat (anchor, muat ulang, gulir cepat)
     --------------------------------------------------------------------- */
  var sweepQueued = false;

  function sweep() {
    if (sweepQueued) return;
    sweepQueued = true;
    requestAnimationFrame(function () {
      sweepQueued = false;
      var limit = window.innerHeight - 20;

      pendingReveal.slice().forEach(function (el) {
        if (el.getBoundingClientRect().top < limit) showReveal(el);
      });
      pendingSplit.slice().forEach(function (item) {
        if (item.el.getBoundingClientRect().top < limit) markSplit(item);
      });
    });
  }

  window.addEventListener('scroll', sweep, { passive: true });
  window.addEventListener('resize', sweep, { passive: true });
  sweep();

  /* ---------------------------------------------------------------------
     12. Sorotan kartu mengikuti kursor
     --------------------------------------------------------------------- */
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches && !reduceMotion) {
    doc.querySelectorAll('.feature-card, .scheme-card, .post-card, .tuk-card, .person-card').forEach(function (card) {
      card.classList.add('spotlight');
      card.addEventListener('pointermove', function (e) {
        var rect = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - rect.left) + 'px');
        card.style.setProperty('--my', (e.clientY - rect.top) + 'px');
      });
      card.addEventListener('pointerleave', function () {
        card.style.removeProperty('--mx');
        card.style.removeProperty('--my');
      });
    });
  }

  /* ---------------------------------------------------------------------
     13. Pintasan tersembunyi ke panel admin
     Ctrl/Cmd + Shift + A — tidak ada tautan/teks yang menonjol di halaman.
     --------------------------------------------------------------------- */
  doc.addEventListener('keydown', function (e) {
    if (!(e.ctrlKey || e.metaKey) || !e.shiftKey || e.key.toLowerCase() !== 'a') return;
    var trigger = doc.querySelector('.footer__admin');
    if (!trigger) return;
    e.preventDefault();
    window.location.href = trigger.getAttribute('href');
  });
})();
