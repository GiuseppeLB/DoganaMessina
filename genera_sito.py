#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generatore statico per il sito "Museo della Dogana di Messina".
Crea tutte le pagine HTML a partire da template comuni, con testo
segnaposto in latino (lorem ipsum) da sostituire con i contenuti reali.
Pensato per essere sincronizzato/importato in Publii o pubblicato
direttamente su GitHub Pages.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

LOREM = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
         "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
         "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris "
         "nisi ut aliquip ex ea commodo consequat.")

LOREM_BREVE = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

# ---------------------------------------------------------------------------
# Definizione delle sezioni espositive (modulare: aggiungere una voce qui
# e rilanciare lo script per creare una nuova sezione, es. "sequestri").
# ---------------------------------------------------------------------------
SEZIONI = [
    {
        "slug": "sigilli",
        "titolo": "Sigilli doganali",
        "sottotitolo": "Piombi, sigilli, lucchetti e laminette",
        "n_item": 6,
        "prefisso_item": "Sigillo",
    },
    {
        "slug": "strumenti",
        "titolo": "Strumenti di accertamento",
        "sottotitolo": "Alcolometri, densimetri, bicchieri di campionamento",
        "n_item": 5,
        "prefisso_item": "Strumento",
    },
    {
        "slug": "contrassegni",
        "titolo": "Contrassegni di Stato",
        "sottotitolo": "Contrassegni e bolli di Stato",
        "n_item": 3,
        "prefisso_item": "Contrassegno",
    },
    {
        "slug": "campioni",
        "titolo": "Campioni di merce",
        "sottotitolo": "Lattine di gasolio, alcol e prodotti vari",
        "n_item": 3,
        "prefisso_item": "Campione",
    },
    {
        "slug": "registri",
        "titolo": "Registri e stampati doganali",
        "sottotitolo": "Registri, bollettari e modulistica storica",
        "n_item": 2,
        "prefisso_item": "Registro",
    },
    {
        "slug": "sicurezza",
        "titolo": "Attrezzature di sicurezza",
        "sottotitolo": "Maschere antigas e dotazioni di protezione",
        "n_item": 1,
        "prefisso_item": "Attrezzatura",
    },
]

# Pagine di storia (semplici, senza sotto-item)
PAGINE_STORIA = [
    {
        "slug": "storia-fabbricato",
        "titolo": "Storia del fabbricato",
        "sottotitolo": "La sede storica della Dogana di Messina",
    },
    {
        "slug": "storia-dogana",
        "titolo": "Storia della Dogana",
        "sottotitolo": "Le origini e l'evoluzione dell'ufficio doganale",
    },
]

SITE_TITLE = "Museo della Dogana di Messina"
SITE_SUB = "Agenzia delle Dogane e dei Monopoli"

# ---------------------------------------------------------------------------
# Frammenti HTML comuni
# ---------------------------------------------------------------------------

HEAD_EXTRA = """<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>"""

QR_SCRIPT = """
<script>
  (function(){
    var el = document.getElementById('qr-pagina');
    if(!el || typeof QRCode === 'undefined') return;
    new QRCode(el, {
      text: window.location.href,
      width: 120,
      height: 120,
      colorDark: "#12213a",
      colorLight: "#ffffff",
      correctLevel: QRCode.CorrectLevel.M
    });
  })();
</script>
"""

def nav_html(depth, active_slug=""):
    """depth = numero di livelli di risalita ('' , '../', '../../')"""
    r = depth

    def cls(slug):
        return ' class="attivo"' if slug == active_slug else ''

    items = [
        ("home", f"{r}index.html", "Pagina principale"),
        ("storia-fabbricato", f"{r}pages/storia-fabbricato.html", "Storia del fabbricato"),
        ("storia-dogana", f"{r}pages/storia-dogana.html", "Storia della Dogana"),
    ]
    li = []
    for slug, href, label in items:
        li.append(f'<li><a href="{href}"{cls(slug)}>{label}</a></li>')

    li.append('<li><a href="#" class="sotto" style="pointer-events:none;color:#c99a5c;">Esposizioni</a></li>')
    for s in SEZIONI:
        href = f"{r}esposizioni/{s['slug']}/index.html"
        li.append(f'<li class="sotto"><a href="{href}"{cls(s["slug"])}>{s["titolo"]}</a></li>')

    return "\n      ".join(li)


def base_page(title, breadcrumb, active_slug, depth, content, extra_head=""):
    css = f"{depth}css/style.css"
    home = f"{depth}index.html"
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {SITE_TITLE}</title>
<meta name="description" content="{SITE_TITLE}: esposizione di strumenti e attrezzature tecniche.">
<link rel="stylesheet" href="{css}">
{extra_head}
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
  {content}
</main>

<footer class="site-footer">
  <p>{SITE_TITLE} — {SITE_SUB}</p>
  <p>Contenuti in fase di redazione. Struttura del sito generata automaticamente.</p>
</footer>

<script src="{depth}js/main.js"></script>
</body>
</html>
"""


def breadcrumb_html(depth, parts):
    """parts: lista di tuple (etichetta, href|None)"""
    bits = []
    for label, href in parts:
        if href:
            bits.append(f'<a href="{href}">{label}</a>')
        else:
            bits.append(label)
    return f'<p class="breadcrumb">{" &rsaquo; ".join(bits)}</p>'


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("creato:", path)


# ---------------------------------------------------------------------------
# 1) main.js
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

# ---------------------------------------------------------------------------
# 2) Home page
# ---------------------------------------------------------------------------
schede = []
for s in SEZIONI:
    schede.append(f"""
    <div class="scheda">
      <a class="titolo-scheda" href="esposizioni/{s['slug']}/index.html">{s['titolo']}</a>
      <p class="desc">{s['sottotitolo']}</p>
      <span class="conteggio">{s['n_item']} oggetti in esposizione</span>
    </div>""")

schede_storia = "\n".join(f"""
    <div class="scheda">
      <a class="titolo-scheda" href="pages/{p['slug']}.html">{p['titolo']}</a>
      <p class="desc">{p['sottotitolo']}</p>
    </div>""" for p in PAGINE_STORIA)

home_content = f"""
  <section class="hero">
    <p class="eyebrow">Esposizione permanente</p>
    <h1>{SITE_TITLE}</h1>
    <p class="provvisorio">{LOREM}</p>
  </section>

  <section>
    <h2>Storia</h2>
    <div class="griglia-sezioni">
      {schede_storia}
    </div>
  </section>

  <section style="margin-top:2rem;">
    <h2>Esposizioni</h2>
    <p class="desc" style="color:var(--testo-tenue);font-size:.88rem;margin-bottom:.4rem;">
      Ogni sezione è accessibile direttamente tramite il codice QR affisso
      presso la relativa vetrina, oppure dal menu di navigazione.
    </p>
    <div class="griglia-sezioni">
      {"".join(schede)}
    </div>
  </section>

  <div class="blocco-qr">
    <div class="qr-riquadro" id="qr-pagina"></div>
    <div class="qr-testo">
      <strong>QR di questa pagina</strong>
      Inquadra per riaprire la pagina principale da smartphone.
    </div>
  </div>
"""
write("index.html", base_page(
    title="Pagina principale",
    breadcrumb="",
    active_slug="home",
    depth="",
    content=home_content,
    extra_head=HEAD_EXTRA,
) + QR_SCRIPT.replace("</body>", "").replace("</html>", ""))

# nota: aggiungo lo script QR subito prima della chiusura del body
def inject_qr(html):
    return html.replace("</body>", QR_SCRIPT + "</body>")

# ricreo la home correttamente (metodo pulito, sovrascrivo)
home_html = base_page(
    title="Pagina principale",
    breadcrumb="",
    active_slug="home",
    depth="",
    content=home_content,
    extra_head=HEAD_EXTRA,
)
write("index.html", inject_qr(home_html))

# ---------------------------------------------------------------------------
# 3) Pagine di storia
# ---------------------------------------------------------------------------
for p in PAGINE_STORIA:
    content = f"""
  <a class="link-indietro" href="../index.html">&larr; Torna alla pagina principale</a>
  <section class="hero">
    <p class="eyebrow">Storia</p>
    <h1>{p['titolo']}</h1>
    <p class="provvisorio">{LOREM}</p>
  </section>

  <div class="placeholder-img">Immagine segnaposto — {p['titolo']}</div>

  <p class="provvisorio">{LOREM}</p>
  <p class="provvisorio">{LOREM_BREVE}</p>

  <div class="blocco-qr">
    <div class="qr-riquadro" id="qr-pagina"></div>
    <div class="qr-testo">
      <strong>QR di questa pagina</strong>
      Da stampare ed esporre presso il relativo pannello informativo.
    </div>
  </div>
"""
    bc = breadcrumb_html("../", [("Home", "../index.html"), (p['titolo'], None)])
    html = base_page(
        title=p['titolo'],
        breadcrumb=bc,
        active_slug=p['slug'],
        depth="../",
        content=content,
        extra_head=HEAD_EXTRA,
    )
    write(f"pages/{p['slug']}.html", inject_qr(html))

# ---------------------------------------------------------------------------
# 4) Sezioni espositive: pagina generale + schede oggetto
# ---------------------------------------------------------------------------
for s in SEZIONI:
    slug = s['slug']
    n = s['n_item']

    # ---- indice della sezione (pagina generale) ----
    voci = []
    for i in range(1, n + 1):
        num = f"{i:02d}"
        voci.append(f"""
      <li>
        <span class="num">{s['prefisso_item']} {num}</span>
        <a href="item-{num}.html">{s['prefisso_item']} {num} — <span class="provvisorio-inline">titolo da definire</span></a>
      </li>""")

    content = f"""
  <a class="link-indietro" href="../../index.html">&larr; Torna alla pagina principale</a>
  <section class="hero">
    <p class="eyebrow">Esposizione</p>
    <h1>{s['titolo']}</h1>
    <p class="provvisorio">{LOREM}</p>
  </section>

  <p class="provvisorio">{LOREM}</p>

  <h2>Oggetti in esposizione ({n})</h2>
  <ul class="elenco-item">
    {"".join(voci)}
  </ul>

  <div class="blocco-qr">
    <div class="qr-riquadro" id="qr-pagina"></div>
    <div class="qr-testo">
      <strong>QR di questa pagina</strong>
      Inquadra per accedere alla panoramica della sezione "{s['titolo']}".
    </div>
  </div>
"""
    bc = breadcrumb_html("../../", [("Home", "../../index.html"), (s['titolo'], None)])
    html = base_page(
        title=s['titolo'],
        breadcrumb=bc,
        active_slug=slug,
        depth="../../",
        content=content,
        extra_head=HEAD_EXTRA,
    )
    write(f"esposizioni/{slug}/index.html", inject_qr(html))

    # ---- schede singolo oggetto ----
    for i in range(1, n + 1):
        num = f"{i:02d}"
        prev_href = f"item-{i-1:02d}.html" if i > 1 else None
        next_href = f"item-{i+1:02d}.html" if i < n else None

        nav_prev = f'<a href="{prev_href}">&larr; Oggetto precedente</a>' if prev_href else '<span class="disabilitato">&larr; Oggetto precedente</span>'
        nav_next = f'<a href="{next_href}">Oggetto successivo &rarr;</a>' if next_href else '<span class="disabilitato">Oggetto successivo &rarr;</span>'

        content = f"""
  <a class="link-indietro" href="index.html">&larr; Torna a "{s['titolo']}"</a>
  <article class="scheda-oggetto">
    <p class="etichetta">{s['titolo']} — scheda {num} di {n:02d}</p>
    <h1>{s['prefisso_item']} {num} — <span class="provvisorio-inline">titolo da definire</span></h1>

    <div class="placeholder-img">Immagine segnaposto — {s['prefisso_item']} {num}</div>

    <p class="provvisorio">{LOREM}</p>

    <dl class="campi-scheda">
      <dt>Descrizione</dt>
      <dd class="provvisorio" style="margin:0;">{LOREM_BREVE}</dd>
      <dt>Provenienza / periodo</dt>
      <dd class="provvisorio" style="margin:0;">{LOREM_BREVE}</dd>
      <dt>Note tecniche</dt>
      <dd class="provvisorio" style="margin:0;">{LOREM_BREVE}</dd>
    </dl>
  </article>

  <div class="nav-item">
    {nav_prev}
    {nav_next}
  </div>

  <div class="blocco-qr">
    <div class="qr-riquadro" id="qr-pagina"></div>
    <div class="qr-testo">
      <strong>QR di questo oggetto</strong>
      Da stampare ed esporre accanto al reperto in vetrina.
    </div>
  </div>
"""
        bc = breadcrumb_html("../../", [
            ("Home", "../../index.html"),
            (s['titolo'], "index.html"),
            (f"{s['prefisso_item']} {num}", None),
        ])
        html = base_page(
            title=f"{s['prefisso_item']} {num}",
            breadcrumb=bc,
            active_slug=slug,
            depth="../../",
            content=content,
            extra_head=HEAD_EXTRA,
        )
        write(f"esposizioni/{slug}/item-{num}.html", inject_qr(html))

# ---------------------------------------------------------------------------
# 5) Sezione modello "_template" — per creare nuove esposizioni (es. sequestri)
# ---------------------------------------------------------------------------
tpl_readme = """MODELLO PER UNA NUOVA SEZIONE ESPOSITIVA
==========================================

Per aggiungere una nuova esposizione (es. "Oggetti sequestrati"):

1. Copiare l'intera cartella "esposizioni/_template" e rinominarla con
   lo slug della nuova sezione (es. "esposizioni/sequestri").
2. Aprire "index.html" nella nuova cartella e aggiornare:
   - il tag <title> e il testo dell'intestazione (h1)
   - l'elenco puntato "Oggetti in esposizione", con un <li> per ogni
     scheda-oggetto che si vuole creare
3. Copiare "item-01.html" tante volte quanti sono gli oggetti della
   sezione, rinominando in item-02.html, item-03.html, ecc., e
   aggiornare i link "Oggetto precedente / Oggetto successivo".
4. Aggiungere la nuova sezione al menu di navigazione: aprire ogni
   pagina del sito (o, più semplicemente, rilanciare lo script
   "genera_sito.py" dopo aver aggiunto la nuova voce all'elenco
   SEZIONI presente in cima al file) in modo che il menu venga
   rigenerato automaticamente ovunque.
5. Ogni pagina mostra già in automatico, in fondo, il proprio codice
   QR (generato dal proprio URL): basta stampare la pagina o
   fotografare il riquadro per ottenere il codice da affiggere in
   vetrina.

In alternativa, il modo più semplice e coerente è aggiungere la nuova
sezione all'elenco SEZIONI in "genera_sito.py" e rilanciare lo script:
tutte le pagine (indice, schede oggetto, menu di navigazione su TUTTO
il sito) vengono create/aggiornate automaticamente.
"""
write("esposizioni/_template/LEGGIMI.txt", tpl_readme)

s = {"slug": "_template", "titolo": "Nuova esposizione (modello)",
     "sottotitolo": "Copiare questa cartella per creare una nuova sezione", "n_item": 1,
     "prefisso_item": "Oggetto"}

content_tpl_index = f"""
  <a class="link-indietro" href="../../index.html">&larr; Torna alla pagina principale</a>
  <section class="hero">
    <p class="eyebrow">Modello di sezione</p>
    <h1>{s['titolo']}</h1>
    <p class="provvisorio">{LOREM}</p>
  </section>

  <p class="provvisorio">
    Questa cartella non compare nel menu del sito: è un modello da copiare
    per creare nuove sezioni espositive (vedi file LEGGIMI.txt in questa
    stessa cartella). Il modo consigliato resta comunque aggiungere la
    nuova sezione allo script "genera_sito.py" e rilanciarlo.
  </p>

  <h2>Oggetti in esposizione (1)</h2>
  <ul class="elenco-item">
    <li>
      <span class="num">Oggetto 01</span>
      <a href="item-01.html">Oggetto 01 — <span class="provvisorio-inline">titolo da definire</span></a>
    </li>
  </ul>
"""
bc = breadcrumb_html("../../", [("Home", "../../index.html"), (s['titolo'], None)])
html = base_page(
    title=s['titolo'], breadcrumb=bc, active_slug="", depth="../../",
    content=content_tpl_index, extra_head=HEAD_EXTRA,
)
write("esposizioni/_template/index.html", inject_qr(html))

content_tpl_item = f"""
  <a class="link-indietro" href="index.html">&larr; Torna a "{s['titolo']}"</a>
  <article class="scheda-oggetto">
    <p class="etichetta">{s['titolo']} — scheda 01 di 01</p>
    <h1>Oggetto 01 — <span class="provvisorio-inline">titolo da definire</span></h1>
    <div class="placeholder-img">Immagine segnaposto — Oggetto 01</div>
    <p class="provvisorio">{LOREM}</p>
    <dl class="campi-scheda">
      <dt>Descrizione</dt>
      <dd class="provvisorio" style="margin:0;">{LOREM_BREVE}</dd>
      <dt>Provenienza / periodo</dt>
      <dd class="provvisorio" style="margin:0;">{LOREM_BREVE}</dd>
      <dt>Note tecniche</dt>
      <dd class="provvisorio" style="margin:0;">{LOREM_BREVE}</dd>
    </dl>
  </article>

  <div class="nav-item">
    <span class="disabilitato">&larr; Oggetto precedente</span>
    <span class="disabilitato">Oggetto successivo &rarr;</span>
  </div>
"""
bc = breadcrumb_html("../../", [("Home", "../../index.html"), (s['titolo'], "index.html"), ("Oggetto 01", None)])
html = base_page(
    title="Oggetto 01", breadcrumb=bc, active_slug="", depth="../../",
    content=content_tpl_item, extra_head=HEAD_EXTRA,
)
write("esposizioni/_template/item-01.html", inject_qr(html))

print("\nGenerazione completata.")
