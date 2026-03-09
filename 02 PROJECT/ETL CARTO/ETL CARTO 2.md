
# TODO

- test script su srvcarto2svil
- test gdalwarp con grid

# AMBIENTE SVIL

- Creata dir di progetto: **F:\GeoETL**
- Installato Python 3.12
- Configurato come ambiente default (PATH)
- Intallato uv mediante shell
- creato venv in geoETL: “uv venv”
- attivare con → .venv\Scripts\activate
- definito variabile d’ambiente GEOETL_HOME

# COMANDO OGR2OGR

Impostare variabile d’ambiente per rendere indipendente comando ogr2ogr dall’ambiente

- Imposta OGR2OGR_CMD nel tuo .env o nell’ambiente di esecuzione (es: OGR2OGR_CMD=OGR2OGR.bat su Windows, OGR2OGR_CMD=ogr2ogr su Linux).
- Nel codice, usa sempre os.environ.get("OGR2OGR_CMD", "ogr2ogr") per ottenere il comando.

OPZIONI

- Ambiente Docker → file .env o Dockerfile
- Ambiente Windows → file .env o variabile ambiente

**IMPOSTARE IN .env**

```other
# Docker / Linux
OGR2OGR_CMD=ogr2ogr

# Windows
OGR2OGR_CMD=OGR2OGR.bat
```

```other
ogr2ogr_cmd = os.environ.get("OGR2OGR_CMD", "ogr2ogr")
comando_args = [
    ogr2ogr_cmd,
    # ...altri argomenti...
]
```

# PIANO MIGRAZIONE

SUDDIVISO IN DUE FASI

- FASE 1: script in geoscript/etl su srvcarto
- FASE 2: test porting script su container
- FASE 3: schedulazione airflow

## FASE 1

- Creare dir ETL su geoscript
- Copiare file groovy da esercizio
- Creare .env

GESTIONE AMBIENTE PYTHON

- Utilizzare uv + pyproject.toml

Conversione groovy → python

- Gestione OGR2OGR_CMD
- [config.properties](http://config.properties) → .env
- Gestione parametri con argparse
- Gestione log con uuid

## FASE 2

- conversione script python in dag airflow
- esecuzione ogr2ogr con job k8s

# ELENCO SCRIPT

SCRIPT

- bilancio-idrico/scrivi-shape
- cem/elabora-richiesta
- centri-impiego/aggiorna
- geoportale/load_postgis_catalog
- geoserver/cache_controlla_timeout
- geoserver/cache_elabora_richiesta
- geoserver/cache_sched
- geoserver/cache_create
- geoserver/cluster_postgis_table
- geoserver/postgis_cache_mngr
- geoserver/update_cache
- libioss/load_postgis
- psa/scarico_iren (usa certificati)
- rqa/download
- rqa/load_postgis_cor_mv
- rqa/load_postgis_corsto_aa
- rqa/load_postgis_corsto_gg
- rqa/load_postgis
- scuoladigitale/aggiorna
- sentieri/create_kml_gpx
- varie/architetture_post_1945_download

NOTA: geoserver/update_cache è richiamata da servizio

- geoservices-be\WEB-INF\REST\geoserver\update_cache.groovy
- geoservices-gest\WEB-INF\REST\geoserver\update_cache.groovy

# REPO GIT

- GDAL (BASE IMAGE): [https://git.liguriadigitale.it/GEO/gdal-docker](https://git.liguriadigitale.it/GEO/gdal-docker)
- GEOSCRIPT: [https://git.liguriadigitale.it/GEO/geoscript-docker](https://git.liguriadigitale.it/GEO/geoscript-docker)

# GDAL-FULL (BASE IMAGE)

Immagine con build multi-stage in Docker/gdal-full

GDAL con supporto

- Oracle OCI
- ECW
- Grigliati GSB
- Python

GESTIONE

- FILE GRID PER PROJ: mount della dir con grigliati su /usr/share/proj
- TNSNAMES.ORA:
- DIR PER DATI: mount della dir con i dati su /data
- ENV: gestione variabili d’ambiente con file .env

REPO

[https://git.liguriadigitale.it/GEO/gdal-docker](https://git.liguriadigitale.it/GEO/gdal-docker)

# GEOSCRIPT

Porting sistema geoscript in ambiente Ubuntu/Pyhon

Basato su immagine gdal-full

Script montati in /srv/geoscript/

RUN CONTAINER

```other
docker compose down && docker compose build && docker compose up -d
```

ESECUZIONE SCRIPT

Creata shell "run_script"

```bash
# ESCUZIONE DA HOST
docker compose run --rm geoscript bash /srv/geoscript/run <script_da_lanciare>
# ES:
docker compose run --rm geoscript bash /srv/geoscript/run dp/ora_to_pg.py --id 56
```

# TEST

```bash
cd /Users/stefano/Development/Docker/geoscript

# TEST INFO
docker compose run --rm geoscript ogrinfo --formats | grep OCI
docker compose run --rm geoscript gdalinfo --formats | grep ECW

# TEST RASTER
docker compose run --rm geoscript gdal_translate /data/mosaico_CTR5K_TRATTO.ecw /data/TEST.tif -of COG -a_srs EPSG:3003 -co BIGTIFF=YES -co NUM_THREADS=ALL_CPUS -co COMPRESS=JPEG -co RESAMPLING=AVERAGE --config GDAL_NUM_THREADS ALL_CPUS

# TEST ORACLE
docker compose run --rm geoscript ogr2ogr -update -append \
/data/test.shp OCI:georef/MedioVere_2011@"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=amb_db.regione.liguria.it)(PORT=1521))(CONNECT_DATA=(SID=sit)))":RQA_UBICAZIONI \
-s_srs "+proj=tmerc +lat_0=0 +lon_0=9.000000000 +k=0.999600 +x_0=1500000 +y_0=0 +ellps=intl +nadgrids=@43340719_44471019_R40_F00.gsb,null +units=m +no_defs" -t_srs EPSG:7791 \
--config OGR_TRUNCATE YES

docker compose run --rm geoscript ogr2ogr -update -append \
/data/test.shp OCI:georef/MedioVere_2011@AMB_DB_SIT:RQA_UBICAZIONI \
-s_srs "+proj=tmerc +lat_0=0 +lon_0=9.000000000 +k=0.999600 +x_0=1500000 +y_0=0 +ellps=intl +nadgrids=@43340719_44471019_R40_F00.gsb,null +units=m +no_defs" -t_srs EPSG:7791 \
--config OGR_TRUNCATE YES

./run_cmd gdalinfo /data/mosaico_CTR5K_TRATTO.ecw

./run_cmd ogrinfo -ro \
	OCI:georef/MedioVere_2011@"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=amb_db.regione.liguria.it)(PORT=1521))(CONNECT_DATA=(SID=sit)))":RQA_UBICAZIONI

ogrinfo -ro \
	OCI:georef/MedioVere_2011@amb_db_sit:RQA_UBICAZIONI

./run gdal_translate \
	/data/mosaico_CTR5K_TRATTO.ecw /data/TEST.tif -of COG \
	-a_srs EPSG:3003 -co BIGTIFF=YES -co NUM_THREADS=ALL_CPUS -co \
	COMPRESS=JPEG -co RESAMPLING=AVERAGE --config GDAL_NUM_THREADS ALL_CPUS

ogr2ogr -update -append /data/test.shp \
  OCI:georef/MedioVere_2011@amb_db_sit:RQA_UBICAZIONI \
	-s_srs "+proj=tmerc +lat_0=0 +lon_0=9.000000000 +k=0.999600 +x_0=1500000 +y_0=0 +ellps=intl +nadgrids=@43340719_44471019_R40_F00.gsb,null +units=m +no_defs" \
	-t_srs EPSG:7791 \
  --config PG_USE_COPY YES --config OGR_TRUNCATE YES

ogr2ogr -update -append -f "PostgreSQL" PG:"host=geoservizi-db-test.regione.liguria.it port=5432 dbname=viscarto user=viscarto password=viscarto active_schema=varie" \
  OCI:georef/MedioVere_2011@amb_db_sit:RQA_UBICAZIONI \
	-s_srs "+proj=tmerc +lat_0=0 +lon_0=9.000000000 +k=0.999600 +x_0=1500000 +y_0=0 +ellps=intl +nadgrids=@43340719_44471019_R40_F00.gsb,null +units=m +no_defs" \
	-t_srs EPSG:7791 \
  --config PG_USE_COPY YES --config OGR_TRUNCATE YES
```

# TRASFORMAZIONI CON GRIGLIATI

```other
# DA GB A ETRK2K
-s_srs "+proj=tmerc +lat_0=0 +lon_0=9.000000000 +k=0.999600 +x_0=1500000 +y_0=0 +ellps=intl +nadgrids=@43340719_44471019_R40_F00.gsb,null +units=m +no_defs" -t_srs EPSG:7791 \
```

[PROMPTS](GEOSCRIPT NEW/PROMPTS.md)

[CONVERSIONI](GEOSCRIPT NEW/CONVERSIONI.md)

[REST API](GEOSCRIPT NEW/REST API.md)

[KUBERNETES](GEOSCRIPT NEW/KUBERNETES.md)

[DUE IMMAGINI](GEOSCRIPT NEW/DUE IMMAGINI.md)

