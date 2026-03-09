---
type: note
topic: gis
created: 2026-01-15
tags:
  - architettura
  - idt
---

![[dp-geo-arch.png]]

**DATA SOURCES**

- DATI VETTORIALI DA DB REGIONALI (ORACLE / POSTGIS)
- DATI RASTER DA DTUFF
- SERVIZI OGC ESTERNI
- PRODOTTI (OSM / Overture Map)

**INGESTION**

- Mediante script Python (con GDAL/OGR) in container dedicato
