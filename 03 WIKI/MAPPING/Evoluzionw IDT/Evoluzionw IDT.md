---
type: moc
topic: gis
created: 2026-01-15
tags: []
---

# INTRODUZIONE

Nel corso degli ultimi anni sono emerse alcune significative tendenze nel campo delle Infrastrutture di Dati Territoriali e nel modo in cui i dati geospaziali vengono elaborati e resi disponibili.

Alcune di queste tendenze hanno forti connessioni e punti di incontro con la Data Platform.

## Da WebGIS “generici” a WebGIS “dedicati”

Una tendenza in corso nel campo delle Infrastrutture di Dati Territoriali è quella di affiancare a tradizionali strumenti di interfaccia webgis generici (per esempio il visualizzatore standard del geoportale) strumenti “dedicati” a particolari casi d’uso che si adattano alle specificità di un determinato dominio al fine di facilitare l’utente nell’esplorazione dei dati (per esempio i visualizzatori dedicati per RQA e Atlante Geochimico).

Questa tendenza è già consolidata e in corso ma può essere facilitata ed accelerata dalla integrazione con strumenti di analisi/visualizzazione dedicati.

## **Cloud-native Geospatial**

Cloud-native Geospatial è un modo innovativo di lavorare con i dati spaziali basato su una serie di formati  (COG, Geoparquet) e standard (STAC) cloud-based che permettono di utilizzare il cloud per semplificare l’utilizzo di risorse geospaziali secondo un’ottica FAIR (Findable, Accessible, Interoperable, and Reusable).

In particolare l’approccio  Cloud-native Geospatial:

- facilita l’utilizzo dei dati da parte degli utenti
- permette di integrare meglio i dati cartografici in ambienti di Data Analytics / Data Science
- permette una migliore efficienza e una maggiore performance nella fase di analisi e visualizzazione
- semplifica la gestione della infrastruttura

Vedi:

- [https://www.ogc.org/ogc-topics/cloud-native-geospatial/](https://www.ogc.org/ogc-topics/cloud-native-geospatial/)
- [https://cloudnativegeo.org/](https://cloudnativegeo.org/)

## Spatial Data Science e ML

La Spatial Data Science è situata nell’intersezione tra i tradizionali metodi di analisi GIS e gli innovativi metodi della data science, di quest’ultima usa gli strumenti da analisi ed esplorazione (notebook) che vengono integrati con tool dedicati sia alle analisi (geopandas, duckdb) che alla visualizzazione di dati spaziali (leafmap).

Un esempio di campo di applicazione può essere l’analisi di immagini satellitari mediante algoritmi di machine learning.

## Spatial Big Data

Le analisi e la gestione di big data di tipo spaziale non possono essere effettuate mediante tradizionali strumenti GIS.

E’ necessaria una infrastruttura, quale la Data Platform,  che sia in grado di supportare e gestire i carichi di elaborazione.

Esistono strumenti di analisi geospaziale compatibili con l’architettura proposta (Apache Sedona ) e client di visualizzazione di nuova generazione  dedicati (Deck.gl, lonboard)

# INTEGRAZIONE

L’integrazione del sistema cartografico nella data platform avviene su tre livelli

## DATI

Sarà possibile integrare i dati cartografici nella data platform attraverso i meccanismi di ingestion e reverse ETL forniti dalla piattaforma.

Le funzioni di conversione formato saranno effettuate integrando GDAL nelle pipeline di ingresso e uscita dal sistema.

I dati cartografici verranno memorizzati sullo storage della data platform secondo gli standard attuali in particolare GeoParquet per i dati vettoriali e COG (Cloud Optimized Geotiff) per i dati raster.

## ANALISI

Le funzioni di analisi e trasformazione della data platform permetteranno di effettuare analisi specifiche di tipo cartografico e analisi integrate tra la dimensione geospaziale e le altre dimensioni.

Queste funzioni saranno effettuate mediante l’ausilio di specifici strumenti di Geospatial Analytics quali Geopandas, PostGis, DuckDB.

Questi strumenti saranno disponibili sia nelle pipeline di elaborazione che negli ambienti notebook di esplorazione.

La data platform fornirà inoltre servizi di analisi utilizzabili da sistemi esterni, sarà quindi possibile integrarne le funzionalità analitiche nella attuale IDT.

## REPORT

La data platform offrirà strumenti di reportistica cartografica sia per l’utilizzo dedicato che per l’integrazioni in dashboard integrate, in particolare è previsto:

- l’ampliamento delle funzionalità del componente cartografico di PowerBI (pbi-carto)
- lo sviluppo componenti cartografici specifici per Superset
- lo sviluppo di client cartografici orientati alla data analysis, quali [deck.gl](http://deck.gl) e lonboard, ottimizzati per la gestione di dataset di grandi dimensioni
- l’integrazione di strumenti di visualizzazione cartografica in ambiente notebook quali leafmap e lonboard

# VANTAGGI

I vantaggi della integrazione della componente cartografica possono essere sintetizzati nei seguenti punti:

- estensione delle analisi effettuabili nella data platform alla dimensione spaziale
- ampliamento delle possibilità analitiche della IDT regionale mediante l’integrazione con le funzionalità offerte dalla data platform, per esempio analisi di big data e algoritmi di machine learning
- utilizzo degli strumenti e dei processi implementati  sulla data platform all’interno della IDT regionale,  in un’ottica di riutilizzo e standardizzazione di strumenti/processi
- ampliamento dei settori regionali in cui vengono utilizzati dati, analisi e visualizzazioni di tipo cartografico
- maggior utilizzo e diffusione del patrimonio cartografico regionale



- [[NOTE]]
- [[ETL ATTUALE]]
- [[MODERN GIS STACK]]
- [[ARCHITETTURA]]
- [[SOFTWARE]]
- [[GEOPARQUET]]
- [ARCHITETTURA](1%20-%20LAVORO/1%20-%20PROGETTI/DATA%20PLATFORM%20(DP)/CARTOGRAFIA/ARCHITETTURA.md)
- [SOFTWARE](SOFTWARE.md)
- [PMTILES](obsidian://open?vault=Vault&file=30%20WIKI%2F00%20BOOKMARKS%2FLavoro%2FGEO%2FPMTiles%20Concepts%20%20Protomaps%20Docs)
- [[RICADUTE SU IDT]]
- [[INTEGRAZIONE SDI DP]]
- [[Ingestion Dati Geo]]

%% MOC START %%
- [[ARCHITETTURA]]
- [[EVOLUZIONE CARTOGRAFIA 2]]
- [[GEOPARQUET]]
- [[INTEGRAZIONE SDI DP]]
- [[MODERN GIS STACK]]
- [[NOTE]]
- [[RICADUTE SU IDT]]
- [[RQA PIPELINE CARTO]]
- [[SOFTWARE]]
%% MOC END %%
