---
title: "DuckDB PostGIS e GeoParquet"
type: conversation
topic: gis
created: 2026-02-13
tags:
  - duckdb
  - postgis
  - geoparquet
  - mapping

---
> From: https://chatgpt.com/c/680f87a2-0a2c-8008-89df-57a618317058

# you asked

ho db postgis, posso utilizzare duckdb per fare query sulle tavole di postgres con la sintassi postgres e scrivere il risultato su un file geoparquet?

---

# chatgpt response

Formalmente: sì, **DuckDB** può interagire con un database **PostGIS** (PostgreSQL con estensione spaziale), ma ci sono alcune precisazioni importanti:

- **DuckDB** ha un **connettore PostgreSQL** (`postgres_scanner` o tramite `postgres_attach`) che permette di **leggere** tabelle direttamente da un database PostgreSQL/PostGIS.
- Puoi eseguire **query SQL** su queste tabelle **dentro DuckDB**, usando una sintassi molto simile a quella di PostgreSQL.
- **DuckDB** supporta l'esportazione diretta in **GeoParquet** (tramite il supporto dei tipi geometrici nativi).
- Tuttavia, **non** viene usato automaticamente il parser SQL di PostgreSQL: devi assicurarti che la sintassi sia compatibile con DuckDB (molto simile, ma non sempre identica, soprattutto per funzioni PostGIS avanzate).

**Flusso operativo tipico**:
1. Collegare DuckDB al database PostGIS:
   ```sql
   INSTALL postgres_scanner;
   LOAD postgres_scanner;
   CREATE SCHEMA postgis_db;
   ATTACH DATABASE 'dbname=yourdb user=youruser password=yourpassword host=yourhost' AS postgis_db (TYPE POSTGRES);
   ```
2. Eseguire query sulle tabelle remote:
   ```sql
   SELECT * FROM postgis_db.public.your_table;
   ```
   oppure scrivere query più complesse compatibili con DuckDB.

3. Esportare in GeoParquet:
   ```sql
   COPY (SELECT * FROM postgis_db.public.your_table) 
   TO 'output_file.parquet' (FORMAT PARQUET, GEOMETRY 'geom');
   ```

---

**Limiti da considerare**:
- Funzioni spaziali di PostGIS (`ST_Transform`, `ST_Intersection`, ecc.) **non sono disponibili** direttamente in DuckDB. Se devi usarle, devi eseguirle **prima** sul database oppure usare estensioni di DuckDB come `spatial` (che ha però meno funzioni di PostGIS).
- DuckDB riconosce `GEOMETRY`/`GEOGRAPHY` se esportati correttamente.

---

**Conclusione:**  
- Sì, puoi interrogare tabelle PostGIS da DuckDB.
- Devi garantire compatibilità SQL.
- Puoi salvare direttamente in formato **GeoParquet**.

Vuoi che ti fornisca anche un esempio completo in Python (usando `duckdb` + `geopandas`)?
