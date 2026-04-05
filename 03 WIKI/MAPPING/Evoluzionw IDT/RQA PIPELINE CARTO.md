---
type: note
topic: gis
created: 2026-01-15
tags:
  - rqa
  - pipeline
  - mapping
  - evoluzionw-idt

---

Script groovy schedulati con utilizzo di

- GDAL/OGR (ogr2ogr) per copia dati da Oracle a Postgis
- Comandi SQL per elaborazione dati su Postgis (via jdbc)

Schedulazione mediante Windows Task Manager

## **COUNT RECORD**

- v_rqa_indicatori_gg 3367482
- v_rqa_indicatori_gg_cor 830557
- v_rqa_indicatori_aa 12732
- v_rqa_indicatori_aa_cor 1195

## load_postgis_full

ESECUZIONE: OGNI NOTTE ALLE 01:00

- load_postgis: copia le tavole base su postgis mediante GDAL/OGR (tavola cartografica, indicatori, configurazioni, ecc.)
- load_postgis_cor_mv: calcolo viste materializzate su postgis mediante esecuzione di comandi sql
- download: preparazione file per download (lettura da postgis e scrittura file in formato shape+csv e geopackage mediante GDAL/OGR)

## load_postgis_cor

ESECUZIONE: OGNI GIORNO ALLE 07:00 E ALLE ORE 16:00

- copia da Oracle a Postigis delle tavole degli indicatori (mediante GDAL/OGR)
- refresh viste materializzate
- tuning tavole e viste materializzate (vacuum analyze)

## load_postgis_corsto_aa

ESECUZIONE: UNA VOLTA ALL’ANNO (A RICHIESTA)

- copia da Oracle a Postigis delle tavole degli indicatori storici annuali (mediante GDAL/OGR)
- creazione e tuning tavola derivata degli indicatori storici annuali
- creazione vista finale

## load_postgis_corsto_gg

ESECUZIONE: UNA VOLTA ALL’ANNO (A RICHIESTA)

- copia da Oracle a Postigis delle tavole degli indicatori storici giornalieri (mediante GDAL/OGR)
- creazione e tuning tavola derivata degli indicatori storici giornalieri
- creazione vista finale
