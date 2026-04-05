---
type: note
topic: gis
created: 2026-01-15
tags:
  - etl
  - raster
  - mapping
  - ingestion-dati-geo

---

# **Analisi Dati Raster**

- **Flusso:** (Evolved) Geoscript usa script Python/GDAL (`gdalwarp`, `gdal_translate`) per leggere i raster sorgente, riproiettare in EPSG:7791, convertire in formato Cloud Optimized GeoTIFF (COG) e scrivere i file COG direttamente su MinIO S3.
- **Valutazione:** Questo approccio è **generalmente valido e raccomandato** per i dati raster. COG è lo standard de facto per l'accesso efficiente a dati raster su object storage. Utilizzare GDAL (tramite Python) nell'ambiente evoluto di Geoscript è la scelta corretta.
- **Criticità:**
    - **Risorse Computazionali:** La trasformazione raster può essere molto intensiva (CPU, I/O, RAM). Il server Geoscript deve essere adeguatamente dimensionato. Potrebbe essere necessario parallelizzare i processi per grandi volumi di dati.
    - **Gestione Errori:** Implementare un error handling robusto per i comandi GDAL è essenziale.
    - **Orchestrazione:** Necessita di essere schedulato e monitorato (cron o, meglio, orchestratore DP).
    - **Catalogazione:** Come vengono scoperti e catalogati questi COG? Devono essere registrati nel Data Catalog (DataHub/OpenMetadata)? Geoscript dovrebbe inviare metadati al catalogo? O il catalogo ha meccanismi di scansione S3? Questo aspetto va definito per garantire la *discoverability* dei raster nella DP. Solitamente i COG non sono gestiti da Iceberg, ma direttamente referenziati tramite il loro path S3.
    - **Aggiornamenti:** Definire la strategia per aggiornare/sovrascrivere i COG esistenti.

# CATALOGHI RASTER

Ok, approfondiamo come integrare i dati raster (COG su MinIO) nel sistema di catalogazione della Data Platform e come implementare un server STAC.

**1. Catalogazione dei Dati Raster nella Data Platform (DP)**

Il flusso proposto prevede che i file COG (Cloud Optimized GeoTIFF) vengano scritti su MinIO (S3) dal processo evoluto di Geoscript/Python. A differenza dei dati vettoriali che vengono registrati in Iceberg/Nessie, i COG solitamente non sono gestiti da formati tabellari come Iceberg. La sfida è renderli *discoverabili*, *comprensibili* e *utilizzabili* attraverso gli strumenti della DP.

**Componenti Coinvolti nella Catalogazione Raster:**

- **MinIO (Object Storage):** Memorizza fisicamente i file COG. La struttura delle directory (prefissi S3) è importante per l'organizzazione (es. `s3://nome-bucket/raster/ortofoto/anno=2023/tile_id.tif`).
- **Data Catalog (DataHub / OpenMetadata):** Il catalogo centrale dove i metadati tecnici e di business dei COG devono essere registrati. Gli utenti cercano qui i dati disponibili.
- **Processo di Ingestion Raster (ex-Geoscript/Python):** Il processo che crea i COG. Deve essere responsabile anche di *generare e/o inviare* i metadati al Data Catalog.
- **Dremio (Potenziale):** Potrebbe (con limitazioni) accedere ai COG, ma non è il suo punto di forza principale. La catalogazione primaria avviene nel Data Catalog.
- **Strumenti di Analisi (Python/Geopandas/Rasterio, QGIS, etc.):** Devono poter trovare il *path S3* del COG desiderato tramite il Data Catalog per poi accedervi.

**Implementazione del Processo di Catalogazione Raster:**

L'obiettivo è creare una "scheda" nel Data Catalog (DataHub/OpenMetadata) per ogni *dataset* raster logico (es. "Ortofoto Regione Liguria 2023") o potenzialmente per ogni file COG individuale se la granularità richiesta è molto alta.

**Opzione A: Catalogazione a Livello di Dataset (Raccomandata)**

1. **Definizione del Dataset Logico:** Si identifica un insieme coerente di file COG come un unico dataset (es. tutte le tile di un'ortofoto di un certo anno).
2. **Estrazione/Generazione Metadati:** Durante o dopo la creazione dei COG, il processo Python/GDAL estrae o genera metadati chiave:
    - **Tecnici:**
        - Formato: COG (Cloud Optimized GeoTIFF)
        - Sistema di Riferimento Coordinate (CRS): Es. EPSG:7791
        - Risoluzione Spaziale (GSD - Ground Sample Distance)
        - Estensione Geografica (Bounding Box) del dataset completo.
        - Numero di Bande, Tipi di Dati per Banda.
        - Path S3 Base: Il prefisso comune su MinIO dove si trovano i file COG del dataset (es. `s3://nome-bucket/raster/ortofoto/anno=2023/`). Questo è FONDAMENTALE per permettere agli strumenti di accedere ai dati.
        - Eventuali convenzioni di Naming dei file (es. basato su tile ID).
    - **Di Business/Descrittivi:**
        - Nome Dataset (es. "Ortofoto AGEA 2023 - Regione Liguria")
        - Descrizione (contenuto, scopo, fonte originale)
        - Data di Acquisizione/Produzione/Aggiornamento
        - Proprietario/Responsabile del Dato (Owner)
        - Tag/Keywords (es. "ortofoto", "immagine aerea", "copertura suolo", "2023")
        - Licenza d'Uso
        - Link a Documentazione Esterna
        - Data Lineage (da dove proviene il dato sorgente, quale processo lo ha generato - l'orchestratore può aiutare a tracciare questo).
1. **Invio al Data Catalog:** Lo script Python, al termine del processo di generazione dei COG per un dataset, utilizza le API del Data Catalog scelto (DataHub o OpenMetadata) per:
    - Creare o aggiornare un'entità di tipo "Dataset" (o tipo specifico se disponibile, es. "Raster Dataset").
    - Popolare tutti i metadati raccolti (tecnici, business, lineage, ownership, tag).
    - **Cruciale:** Inserire il **Path S3 Base** in un campo dedicato o nella descrizione, in modo che gli utenti sappiano dove trovare i file COG effettivi.

**Opzione B: Catalogazione a Livello di Singolo File COG**

- Simile all'Opzione A, ma si crea un'entità nel Data Catalog per *ogni* file `.tif` generato.
- **Pro:** Massima granularità, si possono avere metadati specifici per file (es. BBOX preciso del singolo file).
- **Contro:** Genera un numero potenzialmente enorme di entry nel catalogo, rendendo la ricerca più complessa; sovraccarico maggiore nell'invio dei metadati; spesso l'utente cerca il *dataset* completo, non il singolo tile.
- **Quando Utile:** Se i singoli file rappresentano entità logicamente distinte (es. singole scene satellitari acquisite in date diverse). Per le ortofoto (spesso un mosaico), l'approccio a livello di dataset è più comune.

**Come Funziona per l'Utente:**

1. L'utente cerca nel Data Catalog (es. cerca "ortofoto liguria 2023").
2. Trova l'entry del dataset raster.
3. Legge la descrizione, il CRS, la risoluzione, il BBOX, l'owner, etc.
4. Trova il **Path S3 Base** (es. `s3://nome-bucket/raster/ortofoto/anno=2023/`).
5. Utilizza questo path nel suo strumento di analisi (QGIS, Python con `rasterio`, etc.) per accedere ai COG. Gli strumenti che supportano COG su S3 potranno leggere i dati in streaming senza scaricare l'intero file.

**Integrazione con Dremio:**

- Dremio non è ottimizzato per la catalogazione o l'analisi diretta di grandi collezioni di file COG sparsi.
- Potrebbe essere possibile creare un "External Source" S3 in Dremio e tentare di definire un formato per i COG, ma le funzionalità di query sarebbero limitate rispetto ai dati tabellari.
- È più probabile che Dremio venga usato per accedere ai *metadati* sui raster (se questi metadati, come il path S3, fossero caricati anche in una tabella Iceberg dedicata nel Data Lake - ridondante rispetto al Data Catalog ma possibile) o per unire dati vettoriali con informazioni derivate dai raster (es. un punto unito con il valore del pixel sottostante estratto da un processo separato).
- **La fonte primaria per scoprire e accedere ai COG rimane il Data Catalog + accesso diretto S3.**

**2. Implementazione di un Server STAC**

**Cos'è STAC (SpatioTemporal Asset Catalog)?**
STAC è uno standard aperto che definisce una specifica API e una struttura JSON per descrivere asset geospaziali (immagini satellitari, ortofoto, dati SAR, dati vettoriali, etc.), rendendoli facilmente ricercabili e indicizzabili. È diventato lo standard de facto per catalogare collezioni di dati geospaziali, specialmente raster.

**Perché implementare STAC?**

- **Standardizzazione:** Permette a client generici (browser STAC, plugin QGIS, librerie Python come `pystac-client`) di cercare e scoprire i dati raster in modo uniforme.
- **Interoperabilità:** Facilita la condivisione e l'integrazione dei dati con altre piattaforme o utenti che conoscono STAC.
- **Ricerca Spazio-Temporale:** Progettato specificamente per query basate su area di interesse (AOI) e intervallo di tempo.
- **Metadati Ricchi:** Definisce campi standard per metadati comuni (EO - Electro-Optical, SAR, etc.) ma è estensibile.

**Implementazione con Server Python:**

Esistono diverse librerie e framework Python per costruire API STAC:

- **`stac-fastapi`:** Un framework popolare e robusto basato su FastAPI e Pydantic. Offre diverse opzioni di backend per memorizzare l'indice STAC:
    - **`stac-fastapi.pgstac`:** Utilizza un backend PostgreSQL/PostGIS (con l'estensione `pgstac`). È una soluzione molto performante e scalabile, adatta a grandi cataloghi. Richiede un database Postgres.
    - **`stac-fastapi.elasticsearch`:** Utilizza Elasticsearch come backend. Ottimo per query testuali complesse unite a quelle spaziali/temporali. Richiede un cluster Elasticsearch.
    - **`stac-fastapi.memory`:** Backend in memoria, utile per test o cataloghi molto piccoli (non persistente).
    - **Backend Custom:** È possibile implementare backend propri (es. per leggere da un DB NoSQL o altro).
- **`pygeoapi`:** Un framework OGC API più ampio che supporta anche STAC come *feature*, oltre ad altre API OGC (Features, Coverages, Maps). Può usare diversi backend.
- **`stac-server-python` (meno attivo recentemente):** Un'implementazione di riferimento iniziale.

**Processo di Implementazione (usando `stac-fastapi.pgstac` come esempio):**

1. **Setup Backend (PostgreSQL/PostGIS + pgstac):**
    - Provisionare un database PostgreSQL con estensione PostGIS.
    - Installare l'estensione `pgstac` nel database. Questo crea le tabelle e le funzioni necessarie per indicizzare gli Item STAC in modo efficiente.
1. **Installazione `stac-fastapi`:**
    - Installare le librerie necessarie: `pip install stac-fastapi-pgstac uvicorn` (uvicorn è un server ASGI).
1. **Configurazione:**
    - Configurare `stac-fastapi` per connettersi al database `pgstac`. Solitamente tramite variabili d'ambiente o file di configurazione.
1. **Esecuzione Server API:**
    - Avviare il server FastAPI: `uvicorn stac_fastapi.pgstac.app:app --reload` (per sviluppo). Per produzione, usare un server più robusto come Gunicorn dietro un reverse proxy (Nginx/Traefik).
    - Idealmente, deployare l'applicazione come container su Kubernetes.
1. **Popolamento Catalogo STAC:** Questo è il passaggio chiave che si integra con la DP.
    - **Generazione Metadati STAC:** Il processo Python/GDAL (che crea i COG) deve essere modificato per generare anche i metadati in formato STAC JSON per ogni asset (file COG). La libreria `pystac` è lo strumento standard per questo:

```python
import pystac
from datetime import datetime
import rasterio # Per ottenere info dal COG

# Esempio per un singolo COG
cog_s3_path = "s3://nome-bucket/raster/ortofoto/anno=2023/tile_001.tif"
# Ottieni BBOX, CRS, date, etc. dal COG o da altre fonti
with rasterio.open(cog_s3_path) as ds:
    bbox = list(ds.bounds)
    crs_epsg = ds.crs.to_epsg()
    # ... estrai altre info ...

item = pystac.Item(id='ortofoto_2023_tile_001',
                 geometry=pystac.geometry.bbox_to_geometry(bbox), # Geometria dell'asset
                 bbox=bbox,
                 datetime=datetime.utcnow(), # Data/ora dell'asset
                 properties={
                     'proj:epsg': crs_epsg,
                     'gsd': 0.5 # Esempio Ground Sample Distance
                     # ... altri metadati ...
                 },
                 collection='ortofoto-liguria-2023') # ID della collezione STAC a cui appartiene

# Aggiungi l'Asset (il file COG stesso)
item.add_asset(
    key='image',
    asset=pystac.Asset(
        href=cog_s3_path, # URL S3 accessibile!
        media_type=pystac.MediaType.COG,
        title='COG Image',
        roles=['data']
    )
)
# Aggiungi estensioni STAC se necessario (es. 'eo', 'proj')
item.stac_extensions.append('<https://stac-extensions.org/eo/v1.0.0/schema.json>')
item.properties['eo:bands'] = [...] # Definizione bande

# Validare l'item STAC
item.validate()
item_dict = item.to_dict() # Ottieni il JSON
```

    - **Caricamento nell'API STAC:** Lo script Python, dopo aver generato l'Item STAC JSON, deve inviarlo all'API STAC (es. `stac-fastapi`) tramite una richiesta HTTP POST all'endpoint appropriato (es. `/collections/{collection_id}/items`). `stac-fastapi` si occuperà di validare il JSON e inserirlo nel backend `pgstac`. Questo può avvenire alla fine del processo di generazione del COG.

**Relazione tra Data Catalog (DataHub/OpenMetadata) e STAC Server:**

Sono sistemi complementari, non esclusivi:

- **Data Catalog:** Vista *Enterprise* di tutti i dati (tabellari, raster, vettoriali, documentali, BI report...). Focalizzato su discovery generale, governance, lineage, ownership per un pubblico aziendale ampio. Può contenere un link all'endpoint STAC per i dataset raster.
- **STAC Server:** Catalogo *specializzato* per dati geospaziali (principalmente raster/immagini). Offre API standardizzate per ricerca spazio-temporale avanzata, ottimizzate per client GIS e librerie geospaziali.

**Scenario Integrato:**

1. Il processo di ingestion raster crea il COG su MinIO.
2. Genera i metadati STAC (`pystac`) e li invia all'API del server STAC (`stac-fastapi`), che li indicizza nel suo backend (es. `pgstac`).
3. Genera/estrae metadati più generali per il Data Catalog (includendo una descrizione, owner, tag, e l'**endpoint STAC del dataset/collezione** o un link all'interfaccia browser STAC).
4. Invia i metadati generali all'API del Data Catalog (DataHub/OpenMetadata).

L'utente può scoprire i dati raster sia tramite il Data Catalog (vista generale) sia tramite l'API STAC (ricerca specializzata geospaziale).

| **Componente/Approccio** | **Scopo**                                                                                              | **Meccanismo**                                                                                            | **Note**                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Data Catalog (DP)**    | Catalogo centrale Enterprise per discovery/governance di *tutti* i dati (inclusi raster).              | Ingestion process invia metadati (descrittivi, tecnici, **Path S3**, lineage, owner) via API al catalogo. | Focus su Dataset logici (es. "Ortofoto 2023"). Essenziale per rendere i COG utilizzabili dalla DP.                               |
| **Server STAC**          | Catalogo *specializzato* standard per asset geospaziali (raster/vettori) con API per ricerca avanzata. | API Python (es. `stac-fastapi`+`pgstac`) popolata da ingestion process (via `pystac`).                    | Complementare al Data Catalog. Ottimo per interoperabilità e client GIS. Richiede infrastruttura dedicata (API + backend DB/ES). |

# **Conclusioni Sintetiche**

1. **Raster:** L'approccio di generazione COG è standard. La **priorità è definire e implementare il processo di catalogazione** (sia nel Data Catalog centrale che, opzionalmente, via STAC).
2. **Catalogazione:** Entrambi i sistemi (Data Catalog generale e STAC specifico) hanno valore e possono coesistere per soddisfare diverse esigenze di discovery.
