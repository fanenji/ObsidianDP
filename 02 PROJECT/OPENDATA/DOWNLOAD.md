---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - data-platform
  - opendata
---

# FUNZIONI

- Controlli
- Caching
- Eventuale copia/symlink su area dedicata
- URL provisioning
- Notifiche
- Logging
- Eventuale gestione richieste asincrone

# NOTE

- Download sincrono → Preparare i dati sulla DP in tutti i formati disponibili
- Download asincrono → utilizzare solo in casi eccezionali (segnalati mediante FLAG)
- Allegare metadati (descrizione, schema e lineage del dataset) → FRICTIONLESS?

# DUBBI

- Si possono effettuare tutti i dl in modalità sincrona?
    - Semplificherebbe il sistema
    - Quali casi possono richiedere modalità asincrona?
    - Conversione dinamica del formato (es: parquet → CSV)


# SCHEMA


SOURCE
SOURCE_TYPE
- SQL
- FILE
- S3
- …
SQL
- type
- connect_string
- user
- pwd

FILE
- path\url

S3
- url

NOTE
- usr/pwd su db o file configurazione?
