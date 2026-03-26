---
title: "Apache Sedona Coordinate Transform"
type: conversation
topic: gis
created: 2026-02-13
tags:
  - sedona
  - coordinate
---
> From: https://chatgpt.com/c/6808d8b6-ed20-8008-bf31-154247508cc4

# you asked

quale libreria viene utilizzata in apache sedona per le trasformazioni di coordinate?

---

# chatgpt response

In **Apache Sedona**, le trasformazioni di coordinate sono gestite tramite la libreria **Proj4j** (una variante leggera di PROJ.4). Proj4j è inclusa come dipendenza ed è utilizzata per la conversione tra sistemi di riferimento spaziali (CRS).

Tuttavia, va notato che il supporto per le trasformazioni CRS in Sedona è relativamente limitato rispetto ad altre librerie GIS come **GeoTools** o **Proj (PROJ.4/PROJ.6)**. In alcuni casi, può essere necessario effettuare le trasformazioni esternamente (ad esempio in GDAL/OGR o GeoPandas) prima di caricare i dati in Sedona.

Se stai lavorando in un contesto Spark con Sedona, la funzione principale per la trasformazione è:

```scala
ST_Transform(geometry, sourceCRS, targetCRS)
```

Questa funzione si basa su Proj4j per effettuare la trasformazione tra CRS specificati in formato EPSG o WKT.

Fammi sapere se ti serve un esempio pratico.

---

# you asked

E' possibile utilizzare file di grigliati di tipo .gsb per effettuare trasformazioni più precise?

---

# chatgpt response

No, **Apache Sedona** **non supporta l'uso di grigliati `.gsb`** (come quelli utilizzati per le trasformazioni NADCON, NTv2, ecc.) per le trasformazioni di coordinate. Questo perché Sedona si affida a **Proj4j**, che **non implementa il supporto per i grigliati** come fa invece la libreria **PROJ** (usata da software come GDAL, PostGIS, QGIS, ecc.).

### Alternative

Se hai bisogno di **trasformazioni di coordinate ad alta precisione** che utilizzano file `.gsb`, puoi valutare due approcci:

1. **Trasformare i dati prima di caricarli in Sedona**, usando:
   - **GDAL (ogr2ogr)**:
     ```bash
     ogr2ogr -s_srs EPSG:XXXX -t_srs EPSG:YYYY -f "GeoJSON" output.json input.shp
     ```
     (con l'opportuna configurazione per l'uso del grigliato nel sistema di coordinate)

   - **Pyproj / GeoPandas** (in Python), che usa PROJ internamente:
     ```python
     import geopandas as gpd
     gdf = gpd.read_file("input.shp")
     gdf = gdf.to_crs("EPSG:YYYY")  # PROJ gestirà i grigliati, se configurati
     gdf.to_file("output.geojson", driver="GeoJSON")
     ```

2. **Integrare un preprocessore** nel tuo pipeline Spark per gestire la trasformazione con librerie esterne (es. chiamate a script Python o GDAL tramite PySpark o sistemi di orchestrazione).

Se hai uno use case specifico, posso aiutarti a trovare la strategia più adatta.
