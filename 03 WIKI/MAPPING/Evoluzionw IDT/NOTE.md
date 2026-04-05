---
type: note
topic: gis
created: 2026-01-15
tags:
  - mapping
  - evoluzionw-idt
---

# DATI

- [https://overturemaps.org/](https://overturemaps.org/)

# TOOLS

- gdal/ogr
- dbt
- duckdb
- dremio
- geopandas
- pmtiles
- [https://github.com/felt/tippecanoe](https://github.com/felt/tippecanoe)

# INGESTION

Source (DB Oracle/Postgis, Servizi, ecc..) → Geoparquet in S3  (con Python/GDAL/OGR)

Convertire tutti i dati in ETRF2K/UTM32

Livelli puntuali: geometry + colonne lat/lon WGS84

Per iceberg: [https://www.dremio.com/blog/loading-data-into-apache-iceberg-just-got-easier-with-dremio-24-3-and-dremio-cloud/](https://www.dremio.com/blog/loading-data-into-apache-iceberg-just-got-easier-with-dremio-24-3-and-dremio-cloud/)



# DREMIO

Test **dremio-udf-gis**

# PROCESSING

- dbt
- DuckDB
- GeoPandas
