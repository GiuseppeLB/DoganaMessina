#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera admin/config.yml per Decap CMS, con un modulo per ogni
pagina/scheda del sito. Da rilanciare insieme a genera_sito.py ogni
volta che si aggiunge una nuova sezione o un nuovo oggetto."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

SEZIONI = [
    {"slug": "sigilli", "titolo": "Sigilli doganali", "n_item": 6, "prefisso_item": "Sigillo"},
    {"slug": "strumenti", "titolo": "Strumenti di accertamento", "n_item": 5, "prefisso_item": "Strumento"},
    {"slug": "contrassegni", "titolo": "Contrassegni di Stato", "n_item": 3, "prefisso_item": "Contrassegno"},
    {"slug": "campioni", "titolo": "Campioni di merce", "n_item": 3, "prefisso_item": "Campione"},
    {"slug": "registri", "titolo": "Registri e stampati doganali", "n_item": 2, "prefisso_item": "Registro"},
    {"slug": "sicurezza", "titolo": "Attrezzature di sicurezza", "n_item": 1, "prefisso_item": "Attrezzatura"},
]
PAGINE_STORIA = [
    {"slug": "storia-fabbricato", "titolo": "Storia del fabbricato"},
    {"slug": "storia-dogana", "titolo": "Storia della Dogana"},
]

CAMPI_PAGE = """          - {label: "Titolo", name: "title", widget: "string"}
          - {label: "Immagine", name: "image", widget: "image", required: false}
          - {label: "Testo", name: "body", widget: "markdown"}"""

CAMPI_SECTION = """          - {label: "Titolo", name: "title", widget: "string"}
          - {label: "Testo introduttivo", name: "intro", widget: "markdown"}"""

CAMPI_ITEM = """          - {label: "Titolo oggetto", name: "title", widget: "string"}
          - {label: "Immagine", name: "image", widget: "image", required: false}
          - {label: "Descrizione", name: "description", widget: "markdown"}
          - {label: "Provenienza / periodo", name: "provenienza", widget: "string", required: false}
          - {label: "Note tecniche", name: "note", widget: "markdown", required: false}"""

righe = []
righe.append("""backend:
  name: git-gateway
  branch: main

# Le immagini caricate dall'editor vengono salvate qui nel repository
media_folder: "images/uploads"
public_folder: "/images/uploads"

# I contenuti pubblicati sono visibili a tutti senza login;
# solo l'accesso a /admin per MODIFICARE richiede l'accesso Netlify Identity.
publish_mode: simple

collections:

  - name: "home"
    label: "Pagina principale"
    files:
      - label: "Pagina principale"
        name: "home"
        file: "content/home.json"
        fields:
          - {label: "Titolo del sito", name: "title", widget: "string"}
          - {label: "Testo introduttivo", name: "intro", widget: "markdown"}

  - name: "storia"
    label: "Pagine di storia"
    files:""")

for p in PAGINE_STORIA:
    righe.append(f"""      - label: "{p['titolo']}"
        name: "{p['slug']}"
        file: "content/pages/{p['slug']}.json"
        fields:
{CAMPI_PAGE}""")

for s in SEZIONI:
    slug, titolo, n, pref = s['slug'], s['titolo'], s['n_item'], s['prefisso_item']
    righe.append(f"""
  - name: "{slug}"
    label: "{titolo}"
    files:
      - label: "{titolo} — testo generale"
        name: "{slug}-index"
        file: "content/esposizioni/{slug}/index.json"
        fields:
{CAMPI_SECTION}""")
    for i in range(1, n + 1):
        num = f"{i:02d}"
        righe.append(f"""      - label: "{pref} {num}"
        name: "{slug}-item-{num}"
        file: "content/esposizioni/{slug}/item-{num}.json"
        fields:
{CAMPI_ITEM}""")

config_yml = "\n".join(righe) + "\n"

path = os.path.join(ROOT, "admin", "config.yml")
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    f.write(config_yml)
print("creato: admin/config.yml")
