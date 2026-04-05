---
tags:
  - slide
  - mapping
  - evoluzionw-idt
---

# PMTILES

[https://docs.protomaps.com/pmtiles/](https://docs.protomaps.com/pmtiles/)

[https://gdal.org/en/stable/drivers/vector/pmtiles.html](https://gdal.org/en/stable/drivers/vector/pmtiles.html)



# Lonboard 

A Python library for fast, interactive geospatial vector data visualization in Jupyter.

Building on cutting-edge technologies like [GeoArrow](https://github.com/geoarrow/geoarrow) and [GeoParquet](https://github.com/opengeospatial/geoparquet) in conjunction with [GPU-based map rendering](https://deck.gl/), Lonboard aims to enable visualizing large geospatial datasets interactively through a simple interface.



# deck.gl

[Learning Resources | deck.gl](https://deck.gl/docs/get-started/learning-resources)

Technical deep dive SLIDES

[https://docs.google.com/presentation/d/1qtXUQzMuIa8NYIKUa1RKfSwvgpeccY-wrPrYqsb_8rE/editslide=id.g7db7fb98fb_0_45](https://docs.google.com/presentation/d/1qtXUQzMuIa8NYIKUa1RKfSwvgpeccY-wrPrYqsb_8rE/editslide=id.g7db7fb98fb_0_45)

[Apache Sedona™](https://sedona.apache.org/)

[Jia Yu - How Apache Sedona is Revolutionizing Geospatial Data Analysis | PyData Seattle 2023](https://www.youtube.com/watch?v=AtgjdK2Gglg)

[Processing and publishing big data with GeoServer and Databricks in Azure](https://speakerdeck.com/simboss/processing-and-publishing-big-data-with-geoserver-and-databricks-in-azure)

[https://speakerdeck.com/simboss/processing-and-publishing-big-data-with-geoserver-and-databricks-in-azure](https://speakerdeck.com/simboss/processing-and-publishing-big-data-with-geoserver-and-databricks-in-azure)

# GDAL

GDAL (Geospatial Data Abstraction Library) è una libreria open source di conversione per i dati geografici sia raster che vettoriali.  È pubblicata dalla Open Source Geospatial Foundation (OSGeo) con licenza X/MIT.

Questa libreria presenta un singolo modello di dati astratto sia per dati raster che vettoriali, fornendo un’interfaccia uniforme alle applicazioni che la utilizzano.

E’ possibile utilizzarla sia tramite riga di comando mediante opportuni eseguibili (ogr2ogr, gdal-translate, …) che programmaticamente attraverso una serie di binding per diversi linguaggi, tra cui quello per Python.

E’ una delle librerie GIS più utilizzate sia in ambito open-source che proprietario e gestisce tutti i principali formati raster e vettoriali esistenti.

La velocità di implementazione di nuovi formati è molto elevata e permette alle applicazioni di utilizzarli in tempi rapidi. In particolareil supporto dei formati di tipo cloud-native, come il formato COG (Cloud Optimized Geotiff) e il formato GeoParquet, sono particolarmente indicati per l’utilizzo all’interno della data platform.

Nell’ambito del sistema GDAL si occupa della conversione del formato per i dati geografici nell’ambito della ingestion dei dati e del write-back sui sistemi esterni, ad esempio per rendere disponibili ai servizi della Infrastruttura di Dati Territoriale i dati elaborati dalla piattaforma.

# DuckDB

DuckDB è un database relazionale in-process, progettato per l’analisi dei dati ad alte prestazioni distribuito con licenza MIT.

Alcuni punti chiave:

1. Semplice e portatile: DuckDB non ha dipendenze esterne. È un sistema serverless che può essere incorporato direttamente nelle applicazioni.
2. Ampio supporto SQL: DuckDB offre un ricco dialetto SQL, con funzionalità che vanno oltre il semplice SQL. Supporta subquery correlate arbitrarie e nidificate, funzioni di finestra e tipi complessi come array e strutture.
3. Ottimizzato per l’analisi: DuckDB è progettato per l’elaborazione analitica. Utilizza un motore vettorializzato e parallelo, consentendo l’elaborazione di grandi moli di dati.
4. Sorgenti dati supportate: È uno strumento utile per l’analisi dati e l’interrogazione di dataset tabulari da file in vari formati, tra cui Parquet, CSV e JSON, utilizzabili in modalità cloud-native mediante SQL.
5. Bindings: DuckDB ha bindings diversi linguaggi tra cui Python, R, Java, Julia, ecc.

Sebbene DuckDB non sia specificamente un sistema di analisi geospaziale, presenta una “Spatial Extension” che implementa uno specifico tipo “GEOMETRY” basato sul modello standard “OGC/ISO Simple Features”.

L’estensione fornisce inoltre un ampio set di funzioni geografiche simili a quelle presenti in PostGIS. Inoltre permette, attraverso GDAL, la lettura e la scrittura di oltre 50 formati vettoriali e la loro analisi in maniera trasparente, come se fossero tavole di database interne.

Nell’ambito del sistema DuckDB si occupa delle analisi di tipo geografico integrabili nelle pipeline di elaborazione e nell’ambiente di data exploration. L’integrazione con GDAL ne permette l’utilizzo anche in fase di ingestion o write-back.

# Geopandas

GeoPandas è un progetto open source che estende Pandas per poter lavorare con dati geografici in Python, estendendone i tipi per consentire operazioni spaziali su tipi geometrici.

GeoPandas supporta una vasta gamma di operazioni geometriche: buffering, intersezione, unione calcoli di arre e lunghezze semplificazione, trasformazione e validazione.

Permette di effettuare in ambiente Python le stesse analisi effettuabili su un sistema come PostGIS ed è molto utilizzato in ambienti di tipo notebook.

Nell’ambito del sistema Geopandas può essere utilizzato per analisi spaziali nell’ambiente di esplorazione.

# leafmap

Leafmap è un pacchetto Python open source disegnato per rendere facilmente accessibili le analisi geospaziali interattive e la visualizzazione cartografica in un ambiente Jupyter, utilizzabile anche da utenti con competenze di programmazione limitate.

Leafmap offre diverse funzionalità di analisi geospaziale, alcune delle principali funzionalità supportate sono :

1. Visualizzazione di dati geospaziali: Leafmap consente di visualizzare dati vettoriali e raster su mappe interattive senza scrivere codice e con la possibilità di creare mappe tematiche e la interrogazione interattiva dei dati.
2. Analisi di dati vettoriali: si possono eseguire operazioni di analisi su dati vettoriali (calcolo aree, lunghezze, intersezioni, buffer e altre operazioni geometriche). Viene utilizzato il backend analitico WhiteboxTools utilizzabile direttamente nell’interfaccia di Leafmap.
3. Analisi di dati raster: Leafmap supporta l’analisi di dati raster, inclusi calcoli di statistiche, estrazione di valori pixel, maschere e altre operazioni basate su raster.

Leafmap supporta vari formati di dati vettoriali come Shapefile, GeoJSON, GeoParquet e qualsiasi formato supportato da GeoPandas.

Nell’ambito del sistema Leafmap si occupa dell’analisi spaziale e della visualizzazione cartografica nell’ambiente di data exploration.

# deck.gl

**deck.gl** è un framework javascript basato su **WebGL2** per l’analisi esplorativa e la visualizzazione di dataset geografici.

E’ un client cartografico molto performante nell’effettuare il rendering e l’aggiornamento di grandi dataset. Grazie al supporto di calcoli ad alta precisione e prestazioni elevate sulla GPU inoltre le API di deck.gl utilizzano il paradigma di programmazione reattiva, consentendo un rendering efficiente anche con carichi di dati pesanti e l’integrazione in ambiente React.

Il supporto di livelli di tipo WMS ne permette l’integrazione con la IDT regionale, mentre il supporto a livelli ti tipo TileLayer ne permette l’integrazione con servizi di mappe di base.

E’ integrabile in ambiente Jupyter mediante il pacchetto pydeck che offre un binding python alle API di [deck.gl](http://deck.gl) sia direttamente che attraverso leafmap.

Nell’ambito della data platform [deck.gl](http://deck.gl) può essere utilizzato per realizzare front-end cartografici orientati alla visualizzazione di grandi moli di dati sia in come client dedicati che integrati nell’ambiente di esplorazione notebook.

Essendo uno strumento orientato alla data analytics offre strumenti di visualizzazione migliori dei client cartografici generici come Leaflet e  OpenLayers e complementari a questi, estendo quindi le funzionalità generali della infrastruttura di dati territoriali regionali.

# PBI-Carto

Si tratta si un componente custom sviluppato internamente che permette di inserire in report PowerBI visualizzazioni cartografiche dei dati con una integrazione con l’infrastruttura cartografica regionale.

In particolare permette di:

- visualizzare dati in formato GeoJSON permettendone la rappresentazione tematica in base ai valori di un campo del dataset
- rappresentare su mappa e tematizzare dataset contenenti le coordinate (longitudine e latitudine)
- visualizzare una mappa di sfondo a scelta tra un ampio set di stili
- visualizzare livelli cartografici della banca dati regionale mediante i relativi servizi wms.

Nell’ambito della data platform questo componente permette di estendere e personalizzare le funzionalità cartografiche di PowerBI rispondendo meglio ai requisiti degli utenti.
