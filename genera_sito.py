#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generatore del sito "Museo della Dogana di Messina" — versione con
pannello di amministrazione (Decap CMS) per la modifica WYSIWYG dei
contenuti dopo la pubblicazione, pensata per hosting su Netlify
(gratuito, senza pubblicità, pagine pubbliche senza login).

Architettura:
- Le pagine .html sono "gusci" statici fissi (struttura, menu, QR,
  breadcrumb, navigazione tra oggetti): li genera questo script e
  normalmente NON si toccano più.
- I testi effettivi (titoli, descrizioni, immagini) vivono in file
  .json dentro /content/, che è esattamente ciò che Decap CMS
  modifica tramite il pannello /admin con un editor a campi/WYSIWYG.
- Un piccolo script (js/render.js) legge il file .json della pagina
  e lo inserisce nel punto giusto dello scheletro HTML.
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

LOREM = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do "
         "eiusmod tempor incididunt ut labore et dolore magna aliqua.")
LOREM_BREVE = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

SEZIONI = [
    {"slug": "sigilli", "titolo": "Sigilli doganali",
     "sottotitolo": "Piombi, sigilli, lucchetti e laminette",
     "n_item": 6, "prefisso_item": "Sigillo"},
    {"slug": "strumenti", "titolo": "Strumenti di accertamento",
     "sottotitolo": "Alcolometri, densimetri, bicchieri di campionamento",
     "n_item": 5, "prefisso_item": "Strumento"},
    {"slug": "contrassegni", "titolo": "Contrassegni di Stato",
     "sottotitolo": "Contrassegni e bolli di Stato",
     "n_item": 3, "prefisso_item": "Contrassegno"},
    {"slug": "campioni", "titolo": "Campioni di merce",
     "sottotitolo": "Lattine di gasolio, alcol e prodotti vari",
     "n_item": 3, "prefisso_item": "Campione"},
    {"slug": "registri", "titolo": "Registri e stampati doganali",
     "sottotitolo": "Registri, bollettari e modulistica storica",
     "n_item": 2, "prefisso_item": "Registro"},
    {"slug": "sicurezza", "titolo": "Attrezzature di sicurezza",
     "sottotitolo": "Maschere antigas e dotazioni di protezione",
     "n_item": 1, "prefisso_item": "Attrezzatura"},
]

PAGINE_STORIA = [
    {"slug": "storia-fabbricato", "titolo": "Storia del fabbricato"},
    {"slug": "storia-dogana", "titolo": "Storia della Dogana"},
]

SITE_TITLE = "Le vie dei tesori - La Dogana di Messina"
SITE_SUB = "Agenzia delle Dogane e dei Monopoli"

HEAD_LIBS = (
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>\n'
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/11.1.1/marked.min.js"></script>'
)

QR_SCRIPT = """
<script>
  (function(){
    var el = document.getElementById('qr-pagina');
    if(!el || typeof QRCode === 'undefined') return;
    new QRCode(el, {
      text: window.location.href,
      width: 120, height: 120,
      colorDark: "#12213a", colorLight: "#ffffff",
      correctLevel: QRCode.CorrectLevel.M
    });
  })();
</script>
"""


def nav_html(depth, active_slug=""):
    r = depth

    def cls(slug):
        return ' class="attivo"' if slug == active_slug else ''

    items = [
        ("home", f"{r}index.html", "Pagina principale"),
        ("storia-fabbricato", f"{r}pages/storia-fabbricato.html", "Storia del fabbricato"),
        ("storia-dogana", f"{r}pages/storia-dogana.html", "Storia della Dogana"),
    ]
    li = [f'<li><a href="{href}"{cls(s)}>{label}</a></li>' for s, href, label in items]
    li.append('<li><a href="#" class="sotto" style="pointer-events:none;color:#c99a5c;">Esposizioni</a></li>')
    for s in SEZIONI:
        href = f"{r}esposizioni/{s['slug']}/index.html"
        li.append(f'<li class="sotto"><a href="{href}"{cls(s["slug"])}>{s["titolo"]}</a></li>')
    return "\n      ".join(li)


def base_page(title, breadcrumb, active_slug, depth, body_inner, page_type, content_url, extra_js_vars=""):
    css = f"{depth}css/style.css"
    home = f"{depth}index.html"
    render_js = f"{depth}js/render.js"
    main_js = f"{depth}js/main.js"
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {SITE_TITLE}</title>
<meta name="description" content="{SITE_TITLE}: esposizione di strumenti e attrezzature tecniche.">
<link rel="stylesheet" href="{css}">
{HEAD_LIBS}
</head>
<body>

<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{home}">
      <span class="stemma">MD</span>
      <span class="brand-text">
        <span class="titolo">{SITE_TITLE}</span>
        <span class="sottotitolo">{SITE_SUB}</span>
      </span>
    </a>
    <button class="menu-btn" id="menu-btn" aria-label="Apri menu" aria-expanded="false">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
  </div>
  <nav class="site-nav" id="site-nav">
    <ul>
      {nav_html(depth, active_slug)}
    </ul>
  </nav>
</header>

<main>
  {breadcrumb}
  {body_inner}
</main>

<footer class="site-footer">
  <p>{SITE_TITLE} — {SITE_SUB}</p>
  <p>Contenuti gestiti tramite pannello di amministrazione.</p>
</footer>

<script>
  var PAGE_TYPE = "{page_type}";
  var CONTENT_URL = "{content_url}";
  {extra_js_vars}
</script>
<script src="{main_js}"></script>
<script src="{render_js}"></script>
{QR_SCRIPT}
</body>
</html>
"""


def breadcrumb_html(depth, parts):
    bits = [f'<a href="{href}">{label}</a>' if href else label for label, href in parts]
    return f'<p class="breadcrumb">{" &rsaquo; ".join(bits)}</p>'


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("creato:", path)


def write_json(path, data):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("creato:", path)


# ---------------------------------------------------------------------------
# js/main.js (menu mobile) e js/render.js (rendering contenuti dinamici)
# ---------------------------------------------------------------------------
write("js/main.js", """
document.addEventListener('DOMContentLoaded', function () {
  var btn = document.getElementById('menu-btn');
  var nav = document.getElementById('site-nav');
  if (!btn || !nav) return;
  btn.addEventListener('click', function () {
    var aperto = nav.classList.toggle('aperto');
    btn.setAttribute('aria-expanded', aperto ? 'true' : 'false');
  });
});
""")

write("js/render.js", """
/* Legge il file JSON di contenuto della pagina (gestito da Decap CMS
   nel pannello /admin) e lo inserisce nello scheletro HTML statico. */

function md(testo){
  if(!testo) return '';
  if(typeof marked !== 'undefined') return marked.parse(testo);
  return '<p>' + testo + '</p>';
}

function immagineHtml(src, alt){
  if(src){
    return '<img src="' + src + '" alt="' + (alt || '') + '" style="width:100%;border:1px solid var(--linea);border-radius:2px;margin-bottom:1rem;">';
  }
  return '<div class="placeholder-img">Nessuna immagine caricata</div>';
}

var TEMPLATES = {
  home: function(d){
    return '<p class="eyebrow">Esposizione permanente</p>' +
           '<h1>' + (d.title || '') + '</h1>' +
           md(d.intro);
  },
  page: function(d){
    return '<p class="eyebrow">Storia</p>' +
           '<h1>' + (d.title || '') + '</h1>' +
           immagineHtml(d.image, d.title) +
           md(d.body);
  },
  section: function(d){
    return '<p class="eyebrow">Esposizione</p>' +
           '<h1>' + (d.title || '') + '</h1>' +
           md(d.intro);
  },
  item: function(d){
    var html = '<h1>' + (d.title || '') + '</h1>' + immagineHtml(d.image, d.title) + md(d.description);
    html += '<dl class="campi-scheda">';
    html += '<dt>Provenienza / periodo</dt><dd>' + (d.provenienza || '&nbsp;') + '</dd>';
    html += '<dt>Note tecniche</dt><dd>' + md(d.note) + '</dd>';
    html += '</dl>';
    return html;
  }
};

document.addEventListener('DOMContentLoaded', function(){
  if (typeof PAGE_TYPE === 'undefined' || typeof CONTENT_URL === 'undefined') return;
  var target = document.getElementById('dyn-' + PAGE_TYPE);
  if(!target) return;
  fetch(CONTENT_URL)
    .then(function(r){ if(!r.ok) throw new Error('non trovato'); return r.json(); })
    .then(function(data){ target.innerHTML = TEMPLATES[PAGE_TYPE](data); })
    .catch(function(){ target.innerHTML = '<p class="provvisorio">Contenuto non ancora disponibile.</p>'; });
});
""")

# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
write_json("content/home.json", {"title": SITE_TITLE, "intro": LOREM})

schede_storia = "\n".join(f"""
    <div class="scheda">
      <a class="titolo-scheda" href="pages/{p['slug']}.html">{p['titolo']}</a>
    </div>""" for p in PAGINE_STORIA)

schede_sezioni = "\n".join(f"""
    <div class="scheda">
      <a class="titolo-scheda" href="esposizioni/{s['slug']}/index.html">{s['titolo']}</a>
      <p class="desc">{s['sottotitolo']}</p>
      <span class="conteggio">{s['n_item']} oggetti in esposizione</span>
    </div>""" for s in SEZIONI)

home_body = f"""
  <section class="hero" id="dyn-home"></section>

  <section>
    <h2>Storia</h2>
    <div class="griglia-sezioni">
      {schede_storia}
    </div>
  </section>

  <section style="margin-top:2rem;">
    <h2>Esposizioni</h2>
    <p class="desc" style="color:var(--testo-tenue);font-size:.88rem;margin-bottom:.4rem;">
      Ogni sezione è accessibile anche tramite il codice QR affisso presso la relativa vetrina.
    </p>
    <div class="griglia-sezioni">
      {schede_sezioni}
    </div>
  </section>

  <div class="blocco-qr">
    <div class="qr-riquadro" id="qr-pagina"></div>
    <div class="qr-testo"><strong>QR di questa pagina</strong>Inquadra per riaprire la pagina principale.</div>
  </div>
"""
write("index.html", base_page(
    title="Pagina principale", breadcrumb="", active_slug="home", depth="",
    body_inner=home_body, page_type="home", content_url="content/home.json",
))

# ---------------------------------------------------------------------------
# Pagine di storia
# ---------------------------------------------------------------------------
for p in PAGINE_STORIA:
    write_json(f"content/pages/{p['slug']}.json", {"title": p['titolo'], "image": "", "body": LOREM})
    body = f"""
  <a class="link-indietro" href="../index.html">&larr; Torna alla pagina principale</a>
  <section class="hero" id="dyn-page"></section>
  <div class="blocco-qr">
    <div class="qr-riquadro" id="qr-pagina"></div>
    <div class="qr-testo"><strong>QR di questa pagina</strong>Da stampare per il pannello informativo.</div>
  </div>
"""
    bc = breadcrumb_html("../", [("Home", "../index.html"), (p['titolo'], None)])
    write(f"pages/{p['slug']}.html", base_page(
        title=p['titolo'], breadcrumb=bc, active_slug=p['slug'], depth="../",
        body_inner=body, page_type="page", content_url=f"../content/pages/{p['slug']}.json",
    ))

# ---------------------------------------------------------------------------
# Sezioni espositive
# ---------------------------------------------------------------------------
for s in SEZIONI:
    slug = s['slug']; n = s['n_item']
    write_json(f"content/esposizioni/{slug}/index.json", {"title": s['titolo'], "intro": LOREM})

    voci = "\n".join(f"""
      <li>
        <span class="num">{s['prefisso_item']} {i:02d}</span>
        <a href="item-{i:02d}.html">{s['prefisso_item']} {i:02d}</a>
      </li>""" for i in range(1, n + 1))

    body = f"""
  <a class="link-indietro" href="../../index.html">&larr; Torna alla pagina principale</a>
  <section class="hero" id="dyn-section"></section>
  <h2>Oggetti in esposizione ({n})</h2>
  <ul class="elenco-item">{voci}</ul>
  <div class="blocco-qr">
    <div class="qr-riquadro" id="qr-pagina"></div>
    <div class="qr-testo"><strong>QR di questa pagina</strong>Panoramica della sezione "{s['titolo']}".</div>
  </div>
"""
    bc = breadcrumb_html("../../", [("Home", "../../index.html"), (s['titolo'], None)])
    write(f"esposizioni/{slug}/index.html", base_page(
        title=s['titolo'], breadcrumb=bc, active_slug=slug, depth="../../",
        body_inner=body, page_type="section",
        content_url=f"../../content/esposizioni/{slug}/index.json",
    ))

    for i in range(1, n + 1):
        num = f"{i:02d}"
        write_json(f"content/esposizioni/{slug}/item-{num}.json", {
            "title": f"{s['prefisso_item']} {num} — titolo da definire",
            "image": "", "description": LOREM_BREVE, "provenienza": LOREM_BREVE, "note": LOREM_BREVE,
        })
        prev_href = f"item-{i-1:02d}.html" if i > 1 else None
        next_href = f"item-{i+1:02d}.html" if i < n else None
        nav_prev = f'<a href="{prev_href}">&larr; Oggetto precedente</a>' if prev_href else '<span class="disabilitato">&larr; Oggetto precedente</span>'
        nav_next = f'<a href="{next_href}">Oggetto successivo &rarr;</a>' if next_href else '<span class="disabilitato">Oggetto successivo &rarr;</span>'

        body = f"""
  <a class="link-indietro" href="index.html">&larr; Torna a "{s['titolo']}"</a>
  <article class="scheda-oggetto">
    <p class="etichetta">{s['titolo']} — scheda {num} di {n:02d}</p>
    <div id="dyn-item"></div>
  </article>
  <div class="nav-item">{nav_prev}{nav_next}</div>
  <div class="blocco-qr">
    <div class="qr-riquadro" id="qr-pagina"></div>
    <div class="qr-testo"><strong>QR di questo oggetto</strong>Da esporre accanto al reperto in vetrina.</div>
  </div>
"""
        bc = breadcrumb_html("../../", [("Home", "../../index.html"), (s['titolo'], "index.html"), (f"Scheda {num}", None)])
        write(f"esposizioni/{slug}/item-{num}.html", base_page(
            title=f"{s['prefisso_item']} {num}", breadcrumb=bc, active_slug=slug, depth="../../",
            body_inner=body, page_type="item",
            content_url=f"../../content/esposizioni/{slug}/item-{num}.json",
        ))

print("\nPagine e contenuti generati.")
