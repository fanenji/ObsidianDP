---
type: moc
topic: gis
created: 2026-01-15
tags: []
---

L’ingestion dei dati cartografici riguarda l’integrazione tra un sistema esistente,  la Spatial Data Infrastructure (SDI) di Regione Liguria, e la nuova Data Platform (DP) in costruzione.

In qualche modo le funzioni dei due sistemi si sovrappongono ed esistono diverse possibilità di integrazione: nella SDI sono presenti funzioni di ETL tipiche di una DP e ambienti di database utilizzati per carichi di tipo analitico simil a quelli delle DP.

Nella SDI sono presenti sistemi, come l’ambiente Postgres/Postgis descritto in seguito, che possono essere assimilati ad ambienti tipici della DP (una sorta di Data Warehouse)

TODO:

- definizione boundary tra sistemi
- adozione tool della dp su altri sistemi (es: orchestrazione)
- revisione etl cartografia in ambiente k8s/python

# DEEP RESEARCH

SDI/DP E LORO INTEGRAZIONE

[https://gemini.google.com/share/2bb06e660eee](https://gemini.google.com/share/2bb06e660eee)

# INTEGRAZIONE SDI/DP

Nella SDI di Regione Liguria sono presenti:

- un ambiente Postgres/Postgis (database “viscarto”) utilizzato dalla S.D.I. come ambiente analitico
- un sistema di ETL (Geoscript) per elaborare e muovere i dati tra vari ambienti

Nel sistema Geoscript è presente uno script ETL che copia i dati dal database di gestione Oracle su un database Postgres/Postgis.

## AMBIENTE POSTGIS/VISCARTO

L'ambiente Postgres/viscarto è utilizzato dalla S.D.I. come ambiente analitico per

- accelerare le query per i sistemi di visualizzazione e analisi
- fornire servizi nativi di conversione CRS
- fornire funzioni cartografiche avanzate non presenti sui db Oracle

L’ambiente Postgres (viscarto) potrebbe essere utilizzato come ambiente di “staging” per l’alimentazione della DP con i seguenti vantaggi:

- performante
- funzioni spaziali robuste e potenti
- gestione nativa delle trasformazioni di coordinate
- funzioni avanzate di verifica e correzione delle geometrie garantiscono che i dati caricati su Postgis sono geometricamente e topologicamente corretti

## SISTEMA GEOSCRIPT

Nella SDI regionale i processi di ETL tra i vari ambienti sono implementati mediante script groovy schedulati (Geoscript).

Gli script utilizzano GDAL/OGR per effettuare trasformazioni di formato ed eventuali trasformazioni di sistema di riferimento.

Gli script sono installati su una macchina Windows Server 2019 (srvcarto.regione.liguria.it) e sono  schedulati mediante Task Scheduler.

Le principali criticità del sistema sono:

- Ambiente Windows (preferibile utilizzare macchina Ubuntu)
- Linguaggio Groovy (preferibile utilizzare script python)
- Versione di GDAL/OGR obsoleta
- Configurazione di GDAL/OGR su Windows complessa
- Difficoltà di monitoraggio delle pipeline

Sarebbe bene migrare il Sistema Geoscript in ambiente Ubuntu/Python con le seguenti caratteristiche:

- Macchina Ubuntu
- GDAL/OGR con supporto Oracle (OCI) e ECW
- Python

Il sistema potrebbe essere una VM o in ambiente containerizzato, è disponibile una immagine Docker che soddisfa in pieno i requisiti necessari.

Nel nuovo ambiente l’esecuzione degli script può essere schedulata mediante cron oppure orchestrata da un sistema esterno (es: Airflow).

# INGESTION DATI VETTORIALI

Di seguito propongo due diverse ipotesi di ETL per ingestion dei dati cartografici nella DP.

La prima ipotesi utilizza una ETL a due fasi con utilizzo di Postgis/viscarto come ambiente di staging, la seconda una ETL singola che dalle sorgenti alimenta direttamente la DP.

## IPOTESI 1: INGESTION IN DUE FASI

Oracle → Postgis → DP

In questa ipotesi l'ingestion dei dati vettoriali avviene in due fasi

- caricamento dei dati su DB Oracle in Postgis (Database viscarto)
- caricamento dei dati da postgis sulla Data Platform

L’elaborazione avviene tutta in ambiente Geoscript

### VANTAGGI

- Procedure di copia dei dati nella SDI regionale sono già presenti e funzionanti.
- Postgis/viscarto contiene già larga parte dei dati provenienti da Oracle
- La copia dei dati su postgis può essere facilmente ampliata per nuovi dati necessari alla data platform e non ancora presenti mediante le attuali procedure.
- Le performance e le funzionalità di Postgis lo rendono l’ambiente ideale per alimentare la DP
- Le funzioni di validazione e trasformazione delle geometrie presenti su Postgis permettono una verifica sulla bontà della trasformazione
- La possibilità di effettuare trasformazioni di coordinate mediante l’utilizzo nativo dei grigliati installati sul db server risolve il problema della trasformazione all’interno della DP

### SVANTAGGI

- ETL in due fasi: necessaria sincronizzazione e gestione errori

### FASE 1 - Da Oracle a Postgis

La copia dei dati avviene mediante uno script che:

- legge la configurazione dei livelli sul Catalogo SIT
- costruisce opportunamente la configurazione per ogr
- esegue il comando ogr2ogr

I dati sono aggiornati in modalità diverse a seconda della frequenza di aggiornamento

- schedulazione giornaliera per livelli modificati giornalmente
- schedulazione mensile per livelli modificati mensilmente
- a comando per azione del SITAR

L’orchestrazione può avvenire in due modalità:

- schedulazione cron su sistema Geoscript
- nel sistema di orchestrazione della DP (Airflow o analogo)

### FASE 2 - Da Postgis a Data Platform

I dati vengono letti dal DB Postgis e scritti su Object Storage S3

- GeoParquet come formato file
- Eventualmente Iceberg/GeoIceberg come formato tabellare

I dati sono trasformati nel sistema di riferimento EPSG:7791 (RDN2008 / UTM zone 32N)

L’orchestrazione avviene nel sistema di orchestrazione della DP (Airflow o analogo)

## IPOTESI 2: INGESTION IN UNA FASE

Oracle → DP

In questa ipotesi l’ingestion dei dati cartografici sulla DP avviene all’interno del sistema Geoscript attraverso un processo parallelo a quello che alimenta Postgis

L’ingestion dei dati puà avenire nel sistema Geoscript o nel sistema della DP.

### VANTAGGI

- Unico processo evita la necessità di sincronizzazione in cascata

### SVANTAGGI

- Si perdono le funzionalità presenti sull’ambiente Postgis

## ANALISI IPOTESI

[ETL VETTORIALI](ETL VETTORIALI/ETL VETTORIALI.md)

## SINTESI RISULTATI

[SINTESI](ETL VETTORIALI/SINTESI.md) 

---

# INGESTION DATI RASTER

L’ingestion dei dati cartografici avviene all’interno del sistema Geoscript o della DP attraverso l’utilizzo di script Python che effettuano

- la trasformazione del sistema di coordinate mediante il comando gdalwarp
- la trasformazione di formato mediante il comando gdal_translate

I dati sono convertiti in formato COG e salvati su Object Storage S3 della DP

[ETL RASTER](./ETL RASTER.md)

---

# METADATI

Le conversioni dei dati vengono guidate da un sistema di metadati che contiene l’elenco dei livelli da convertire e le informazioni necessarie agli script ETL per recuperare i dati dalla sorgente.

Il sistema Geoscript utilizza attualmente i metadati del Catalogo SIT di Regione Liguria.

Si propone di estendere il Catalogo SIT per gestire anche la copia dei dati sulla DP

---

[BRAINSTORM](1%20-%20LAVORO/1%20-%20PROGETTI/DATA%20PLATFORM%20(DP)/CARTOGRAFIA/INGESTION%20DATI%20GEO/BRAINSTORM.md)

%% MOC START %%
- [[30 WIKI/DATA PLATFORM/CARTOGRAFIA/INGESTION DATI GEO/BRAINSTORM]]
- [[ETL ATTUALE]]
- [[ETL RASTER]]
- [[ETL VETTORIALI]]
%% MOC END %%
