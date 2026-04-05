---
type: note
topic: gis
created: 2026-01-15
tags:
  - sdi
  - integrazione
  - mapping
  - evoluzionw-idt

---

# INTEGRAZIONE SDI/DP

# INTRODUZIONE

L’ingestion dei dati cartografici riguarda l’integrazione tra un sistema esistente,  la Spatial Data Infrastructure (SDI) di Regione Liguria, e la nuova Data Platform (DP) in costruzione.

In qualche modo le funzioni dei due sistemi si sovrappongono : nella SDI sono presenti funzioni di ETL tipiche di una DP e ambienti di database utilizzati per carichi di tipo analitico simil a quelli delle DP.

Nella SDI sono presenti sistemi, come l’ambiente Postgres/Postgis descritto in seguito, che possono essere assimilati ad ambienti tipici della DP (una sorta di Data Warehouse)

Questo determina anche la possibilità di avere diverse modalità di integrazione e rende in qualche modo sfumato il boundary tra i due sistemi

Trattandosi di sistemi con funzioni similari è necessario quindi stabilire in maniera chiara il boundary tra i due sistemi per definire le rispettive responsabilità e limitare il più possibile gli impatti sulla attuale SDI.

Alcuni strumenti adottati nella DP potrebbero essere estesi alla SDI, in modo da rendere i due sistemi più omogenei e manutenibili in una prospettiva futura (es: tool di orchestrazione, ambiente Kubernetes, utilizzo di python come linguaggio di scripting)

Questo convergenza permetterebbe l’utilizzo dei dati cartografici da parte di una maggior platea di utenti ed inoltre aiuterebbe l’evoluzione della SDI nelle sue parti più critiche e obsolete.

# TRASFORMAZIONE CRS

Un grosso vincolo nella fase di ingestion dei dati cartografici è rappresentato dalla necessità di effettuare trasformazioni del sistema di riferimento (CRS) mediante l’utilizzo di file di grigliati in modo da assicurare una trasformazione con livelli di errore trascurabili.

I dati nei sistemi cartografici di Regione Liguria sono in larga parte memorizzati utilizzando il sistema di riferimento storico Gauss-Boaga, è consigliabile trasformare i dati in fase di ingestion in un unico sistema di riferimento moderno (es: ETRF2K)

Non tutti gli strumenti di analisi geospaziale permettono l’utilizzo dei grigliati e questo pone un vincolo forte sulla scelta dello strumento.

# INTEGRAZIONE SDI/DP

Nella SDI di Regione Liguria sono presenti:

- un ambiente Postgres/Postgis (database “viscarto”) utilizzato dalla SDI come ambiente analitico
- un sistema di ETL (Geoscript) per elaborare e muovere i dati tra vari ambienti

Nel sistema Geoscript è presente uno script ETL che copia i dati dal database di gestione Oracle su un database Postgres/Postgis.

## AMBIENTE POSTGIS/VISCARTO

L'ambiente Postgres/viscarto è utilizzato dalla S.D.I. come ambiente analitico per

- accelerare le query per i sistemi di visualizzazione e analisi
- fornire servizi nativi di conversione CRS
- fornire funzioni si analisi geospaziale

Questo ambiente viene caricato dal sistema ETL Geoscript mediante uno script che legge i dati dagli ambienti gestionali Oracle e contiene la maggior parte dei dati cartografici. I dati sono copiati mediante schedulazioni giornaliere/mensili o mediante richiesta da parte dei gestori del sistema cartografico.

L’ambiente Postgres (viscarto) potrebbe essere utilizzato come ambiente di “staging” per l’alimentazione della DP con i seguenti vantaggi:

- molto performante
- funzioni spaziali robuste e potenti
- gestione nativa delle trasformazioni di coordinate
- funzioni avanzate di verifica e correzione delle geometrie

Le funzioni di verifica/correzione garantiscono che i dati caricati su Postgis sono geometricamente e topologicamente corretti

## SISTEMA GEOSCRIPT

Nella SDI regionale i processi di ETL tra i vari ambienti sono implementati mediante script groovy schedulati (Geoscript).

Gli script utilizzano GDAL/OGR per effettuare trasformazioni di formato ed eventuali trasformazioni di sistema di riferimento.

Gli script sono installati su una macchina Windows Server 2019 (srvcarto.regione.liguria.it) e sono  schedulati mediante Task Scheduler.

Le principali criticità del sistema sono:

- Ambiente Windows
- Linguaggio Groovy
- Versione di GDAL/OGR obsoleta
- Configurazione di GDAL/OGR su Windows complessa
- Difficoltà di monitoraggio delle pipeline

Sarebbe bene migrare il Sistema Geoscript in ambiente Ubuntu/Python con le seguenti caratteristiche:

- Macchina Ubuntu
- GDAL/OGR con supporto Oracle (OCI) e ECW
- Python

Il sistema potrebbe essere una VM o in ambiente containerizzato, è già disponibile una immagine Docker che soddisfa in pieno i requisiti necessari.

I test di migrazione effettuati su alcuni script con l’ausilio di LLM hanno dato ottimi risultati

Nel nuovo ambiente l’esecuzione degli script può essere schedulata mediante cron oppure orchestrata da un sistema esterno (es: Airflow).

# INGESTION DATI VETTORIALI

Di seguito vengono proposte due diverse ipotesi per ingestion dei dati cartografici nella DP.

La prima ipotesi utilizza una ETL a due fasi con utilizzo di Postgis/viscarto come ambiente di staging, la seconda una ETL singola che dalle sorgenti alimenta direttamente la DP.

## IPOTESI 1: INGESTION IN DUE FASI

Oracle → Postgis → DP

In questa ipotesi l'ingestion dei dati vettoriali avviene in due fasi

- caricamento dei dati su DB Oracle in Postgis (Database viscarto)
- caricamento dei dati da postgis sulla Data Platform

L’elaborazione può avvenire tutta in ambiente SDI o mista (fase 1 in ambiente SDI e fase 2 in ambiente DP)

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

- Si perdono tutti i vantaggi dell’ambiente Postgis

---

# METADATI

Le conversioni dei dati vengono guidate da un sistema di metadati che contiene l’elenco dei livelli da convertire e le informazioni necessarie agli script ETL per recuperare i dati dalla sorgente.

Il sistema Geoscript utilizza attualmente i metadati del Catalogo SIT di Regione Liguria.

Si propone di estendere il Catalogo SIT per gestire anche la copia dei dati sulla DP

---

# GEOPARQUET

- **Standard:** GeoParquet è uno standard OGC (Open Geospatial Consortium) adottato ufficialmente (versione 1.0.0 nel 2023, con versioni minori 1.0.1 e 1.1.0 successive). Definisce come memorizzare dati geospaziali vettoriali (punti, linee, poligoni) all'interno di file Apache Parquet, aggiungendo metadati specifici nel footer del file Parquet per descrivere le colonne geometriche, il loro CRS (Coordinate Reference System) e l'extent (bounding box).
- **Adozione (Molto Buona e Crescente):**
    - **Librerie GIS Core:** GDAL/OGR (la libreria fondamentale per molti software GIS) ha pieno supporto in lettura e scrittura per GeoParquet a partire dalla versione 3.5. Questo significa che QGIS, ArcGIS Pro (tramite GDAL), e molti altri strumenti basati su GDAL possono leggere e scrivere GeoParquet.
    - **Ecosistema Python:** GeoPandas (la libreria principale per l'analisi geospaziale vettoriale in Python) supporta nativamente la lettura e scrittura di GeoParquet, sfruttando `pyarrow`.
    - **Ecosistema Big Data:**
        - **Apache Sedona (GeoSpark):** Supporta la lettura e scrittura di GeoParquet, permettendo l'integrazione con pipeline Spark.
        - **DuckDB:** L'estensione `spatial` di DuckDB ha un buon supporto per la lettura e scrittura di GeoParquet.
    - **Database:** PostGIS (tramite GDAL), Google BigQuery, Snowflake e altri database cloud stanno aggiungendo o migliorando il supporto per l'importazione/esportazione o la query diretta di file GeoParquet.
    - **Cloud:** Diverse piattaforme cloud lo riconoscono come formato ottimale per dati vettoriali su object storage.
- **Maturità:** La versione 1.x è considerata stabile e matura. È semplice (aggiunge solo metadati a Parquet standard), ben definita e il supporto software è ampio.
- **GeoParquet 2.0 (In Sviluppo):**
    - **Stato:** Attualmente in fase di discussione e sviluppo all'interno del gruppo di lavoro OGC. Non c'è ancora una data di rilascio ufficiale o una bozza stabile ampiamente condivisa al di fuori dei gruppi di lavoro.
    - **Obiettivi Potenziali (Basati su Discussioni):** Potrebbe affrontare temi come:
        - Supporto migliorato per geometrie 3D e con misure (Z, M).
        - Standardizzazione di indici spaziali *all'interno* del file Parquet (anche se questo è complesso data la natura colonnare di Parquet).
        - Migliore integrazione con altri standard OGC (es. OGC API).
        - Gestione di metadati più complessi o schemi specifici.
    - **Impatto Attuale:** Al momento, l'industria si basa sulla versione 1.x. Non ci sono implementazioni significative della 2.0 e le specifiche non sono finalizzate. **Per le implementazioni attuali, si deve fare riferimento alla versione 1.1.0 dello standard.**

# GEOICEBERG

**GeoIceberg**

- **Concetto:** GeoIceberg non è (ancora) uno standard OGC formalizzato come GeoParquet. È più un'**iniziativa/proposta/insieme di convenzioni** che mira a standardizzare come rappresentare e gestire dati geospaziali (principalmente vettoriali) all'interno di tabelle Apache Iceberg. L'idea è di sfruttare le capacità di Iceberg (transazioni ACID, time travel, schema evolution, partizionamento nascosto) per grandi dataset geospaziali.
- **Approcci Potenziali:**
    1. **Iceberg Standard + GeoParquet:** Memorizzare i dati in file GeoParquet all'interno della struttura di una tabella Iceberg standard. La colonna geometrica viene trattata da Iceberg come un tipo binario (`BinaryType` per WKB) o stringa. Le informazioni spaziali (CRS, tipo geometria) sono nei metadati GeoParquet, non direttamente nei metadati Iceberg (se non come statistiche generiche min/max sui byte del WKB, che non sono spazialmente significative).
    2. **Iceberg con Tipi Geometrici UDT:** Introdurre User-Defined Types (UDT) per le geometrie direttamente nel motore di elaborazione (es. Spark con Sedona) e usarli nelle tabelle Iceberg. Iceberg memorizzerebbe questi UDT in modo serializzato. Questo richiede che il motore di query supporti questi UDT.
    3. **Estensioni ai Metadati Iceberg:** Proporre estensioni allo schema dei metadati di Iceberg (manifest file, ecc.) per includere informazioni spaziali specifiche (es. BBOX per ogni file di dati, CRS della tabella). Questo richiederebbe modifiche allo standard Iceberg stesso.
    4. **Indicizzazione Spaziale:** Sfruttare o estendere i meccanismi di ordinamento/indicizzazione di Iceberg (es. Z-order su colonne derivate come geohash o coordinate min/max) per accelerare le query spaziali.
- **Adozione (Molto Limitata e Frammentata):**
    - **Non è uno Standard:** Manca una specifica condivisa e concordata. Diverse organizzazioni o progetti potrebbero avere le loro "convenzioni GeoIceberg".
    - **Implementazioni Specifiche:** Esistono progetti o implementazioni specifiche che combinano Iceberg con dati spaziali, spesso usando l'approccio 1 (Iceberg + GeoParquet) o l'approccio 2 (Iceberg + UDT via Sedona).
        - **Apache Sedona/Spark:** Può leggere/scrivere tabelle Iceberg contenenti geometrie UDT o colonne WKB (provenienti da GeoParquet), ma l'intelligenza spaziale è fornita da Sedona, non intrinsecamente da Iceberg.
    - **Mancanza di Supporto Nativo:** I motori di query che supportano Iceberg (Spark, Trino, Dremio, Flink, DuckDB) non hanno necessariamente un supporto "GeoIceberg" nativo. Possono leggere tabelle Iceberg con colonne WKB, ma non possono eseguire query spaziali ottimizzate basate su metadati spaziali Iceberg (perché questi metadati standard non esistono). L'ottimizzazione deve avvenire a livello del motore di query (es. Sedona che analizza i file GeoParquet sottostanti o usa UDT).
- **Maturità:** **Bassa**. È un campo in evoluzione e sperimentazione. Non c'è una soluzione "GeoIceberg" standardizzata e ampiamente adottata. Le soluzioni attuali sono più delle integrazioni tra Iceberg e strumenti/formati geospaziali esistenti (come GeoParquet e Sedona).

---

# SINTESI CONCLUSIVA

Visti i notevoli vantaggi viene scelta l’ipotesi a 2 fasi con utilizzo di Postgis coma ambiente di staging.

La prima fase avviene mediante l’attuale pipeline migrata in ambiente python.

Per quanto riguarda la seconda fase si considerano tre ipotesi con utilizzo di diverse tecnologie:

- 1a) stessa tecnologia utilizzata dalla fase 1, la trasformazione di sistema di riferimento e la scrittura avviene mediante il tool ogr2ogr di GDAL.
- 1b) prevede di trasformare i dati utilizzando Geopandas e PyProj per la trasformazione di coordinate
- 1c) prevede l’utilizzo di DuckDb per scrivere i dati in Geoparquet su S3 e per effettuare le trasformazioni di sistema  di riferimento

Per le ipotesi 1b e 1c è necessario verificare la configurabilità di Pyproj per l’utilizzo di grigliati. In caso negativo verificare la possibilità di effettuare la trasformazione direttamente in fase di lettura dei dati utilizzando la funzione st_transform di Postgis.

Vista la scarsa adozione del formato GeoIceberg si preferisce in una prima fase limitare la scrittura dei dati cartografici al solo formato Geoparquet in versione 1.1.

# TABELLA RIASSUNTIVA

| **Ipotesi**                            | **Flusso Principale**                                           | **Trasformazione CRS (EPSG:7791)** | **Tecnologie Chiave (ETL)** |
| -------------------------------------- | --------------------------------------------------------------- | ---------------------------------- | --------------------------- |
| **Ipotesi 1a: ETL a 2 fasi             |                                                                 |                                    |                             |
| (GDAL/OGR)**                           |                                                                 |                                    |                             |
| Oracle → PostGIS (Geoscript/`ogr2ogr`) |                                                                 |                                    |                             |
| PostGIS → S3 (Geoscript/`ogr2ogr`)     | \- GDAL/OGR (Proj)                                              |                                    |                             |
| Python, GDAL                           |                                                                 |                                    |                             |
| **Ipotesi 1b: ETL a 2 fasi             |                                                                 |                                    |                             |
| (Python/GeoPandas)**                   | Oracle → PostGIS (Geoscript/`ogr2ogr`) PostGIS → S3 (Python/GP) | \- GeoPandas                       |                             |

- Postgis | Python, GeoPandas, PyProj, SQLAlchemy, Boto3/S3fs |
| **Ipotesi 1c: ETL a 2 fasi (Python/DuckDB)** | Oracle → PostGIS (Geoscript/`ogr2ogr`; PostGIS → S3 (Python/DuckDB) | - DuckDB
- Postgis | Python, DuckDB (Spatial, Postgres ext.), Boto3/S3fs (o DuckDB S3) |

**Conclusioni:**

1. Tecnologia Trasformazione:
    1. **Opzioni Basate su Postgis:** Aumenta ulteriormente il carico sul DB sorgente
    2. **Opzioni Basate su Python/DuckDB/GDAL:** Le alternative che eseguono la trasformazione in Python o DuckDB o mediante GDAL sono valide e spostano il carico da PostGIS al worker Python/DuckDB/GDAL. Offrono flessibilità ma condividono la **criticità della scalabilità single-node** e richiedono una **gestione della configurazione PROJ/grigliati**. La scelta tra GeoPandas / DuckDB / GDAL dipende dalle preferenze e dalle performance specifiche sui dati (GDAL affidabile e veloce, DuckDB potenzialmente più veloce).
    - **Ruolo di PostGIS:** il database `viscarto` mantiene un ruolo utile come **staging intermedio validato** e per mantenere la compatibilità con la SDI esistente.
1. **PoC Essenziali:** I test diventano ancora più cruciali per:
    - Verificare le **performance di `ST_Transform` in lettura da PostGIS**
    - Verificare le **performance e l'uso di memoria** delle trasformazioni in GDAL, GeoPandas e DuckDB su dataset rappresentativi.
    - Confermare la **corretta configurazione e funzionamento dei grigliati** negli ambienti Python/DuckDB.
    - Verificare la necessità o meno dell’utilizzo di Iceberg e Nessie per i dati cartografici
1. **Infrastruttura:** L'uso di **Kubernetes** per eseguire i task Python/GDAL/Spark rimane la scelta più efficiente e scalabile rispetto a una VM statica, data la disponibilità dell'immagine Docker.

---

# AZIONI

- Implementazione delle tre ipotesi di pipeline
- Test funzionali
- Verifica della corretta trasformazione delle coordinate
- Test di performance e scalabilità
- Confronto delle ipotesi e scelta della tecnologia
