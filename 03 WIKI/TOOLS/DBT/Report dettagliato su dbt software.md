---
type: note
topic: data-platform
created: 2026-03-15
tags:
  - tools
  - dbt
---

# **Architettare il Modern Data Lakehouse: Una Guida Completa a dbt, dallo Sviluppo alla Produzione**

[**<u>Report Web</u>**](https://gemini.google.com/share/cf98d1aaed50)

## **Parte 1: Introduzione a dbt: Il Framework di Analytics Engineering**

Questa sezione stabilisce la comprensione fondamentale di dbt,
posizionandolo non semplicemente come uno strumento, ma come un
framework completo che ridefinisce il modo in cui viene eseguita la
trasformazione dei dati. Coprirà la sua filosofia di base, le
caratteristiche chiave e il valore strategico.

### **1.1. Definire dbt: Più che una Semplice Trasformazione**

dbt, acronimo di "data build tool", è uno strumento open-source a riga
di comando che consente ad analisti e ingegneri di trasformare i dati
direttamente all'interno della loro piattaforma dati.<sup>1</sup> Si
posiziona in modo univoco come il tassello "T" (Transformation) nel
paradigma ELT (Extract, Load, Transform). A differenza degli strumenti
ETL tradizionali, dbt non gestisce l'estrazione o il caricamento dei
dati; la sua forza risiede nella capacità di trasformare in modo
performante i dati che sono già stati caricati in un data warehouse o in
un lakehouse.<sup>1</sup>

Nato nel 2016 all'interno di RJMetrics, dbt è stato concepito per
colmare una lacuna critica: applicare le best practice di ingegneria del
software al mondo dell'analisi dei dati.<sup>1</sup> La sua funzione
principale è quella di compilare ed eseguire codice analitico,
trasformando semplici istruzioni SQL SELECT in tabelle e viste
materializzate all'interno della piattaforma dati di
destinazione.<sup>1</sup> Questo approccio consente di costruire
pipeline di dati robuste e affidabili, gestendo la logica di
trasformazione come se fosse codice applicativo.

### **1.2. Filosofia di Base: Applicare l'Ingegneria del Software ai Dati**

Il principio cardine di dbt è quello di permettere agli "analytics
engineer" di operare con lo stesso rigore e le stesse metodologie degli
ingegneri del software.<sup>1</sup> Questo cambiamento di paradigma si
manifesta attraverso l'adozione di pratiche consolidate nel mondo dello
sviluppo software, applicate al ciclo di vita dei dati:

- **Version Control:** L'integrazione nativa con Git permette di
  versionare ogni singola modifica alla logica di trasformazione,
  abilitando flussi di lavoro collaborativi basati su branch, pull
  request e code review.<sup>4</sup>

- **Modularità:** I modelli di dati complessi vengono scomposti in unità
  più piccole e riutilizzabili, promuovendo il principio DRY (Don't
  Repeat Yourself) e rendendo le pipeline più facili da mantenere e
  comprendere.<sup>4</sup>

- **Testing Automatizzato:** dbt integra un framework di test che
  consente di definire e automatizzare controlli sulla qualità dei dati,
  garantendo l'integrità e l'affidabilità dei dataset
  prodotti.<sup>4</sup>

- **Continuous Integration/Continuous Deployment (CI/CD):** L'approccio
  basato su codice e test automatizzati si sposa perfettamente con le
  pipeline di CI/CD, permettendo di distribuire le modifiche in
  produzione in modo sicuro e controllato.<sup>4</sup>

L'obiettivo finale di questa filosofia è la creazione di codice
analitico affidabile, di alta qualità e manutenibile, che si traduca in
una "singola fonte di verità" per le metriche e le definizioni di
business aziendali.<sup>4</sup> L'innovazione di dbt non è stata tanto
l'invenzione di singole tecnologie, quanto la sintesi di strumenti
preesistenti (SQL, Git, Jinja, testing) in un framework coeso e
opinionato, specificamente progettato per il workflow
analitico.<sup>4</sup> Questa sintesi ha abbassato la barriera
d'ingresso per lo sviluppo di pipeline di dati robuste, poiché gli
analisti necessitano principalmente di competenze SQL, senza dover
padroneggiare linguaggi di programmazione complessi o framework di
orchestrazione.<sup>6</sup> Di conseguenza, l'impatto di dbt è stato
meno tecnologico e più sociologico, creando un "linguaggio condiviso"
che ha unito il mondo degli analisti di dati e degli ingegneri del
software, dando vita e formalizzando la figura professionale
dell'Analytics Engineer.

### **1.3. Caratteristiche e Funzionalità Chiave in Sintesi**

dbt offre un ricco set di funzionalità progettate per ottimizzare il
processo di trasformazione dei dati:

- **Trasformazione come Codice:** Gli utenti definiscono la logica di
  business tramite istruzioni SQL SELECT o, più recentemente, tramite
  DataFrame Python. dbt si occupa di generare il codice DDL (Data
  Definition Language) e DML (Data Manipulation Language) boilerplate
  necessario per creare o aggiornare tabelle e viste, gestire
  transazioni e cambiamenti di schema.<sup>4</sup>

- **Modularità e Riutilizzabilità:** Il cuore di dbt è la capacità di
  costruire modelli di dati riutilizzabili. Attraverso la funzione
  ref(), un modello può fare riferimento a un altro, creando una catena
  di dipendenze che dbt gestisce autonomamente. Questo promuove il
  principio DRY, evitando la duplicazione di codice.<sup>4</sup>

- **Templating con Jinja:** I file SQL in un progetto dbt possono
  contenere Jinja, un motore di templating per Python. Questo estende la
  potenza di SQL, permettendo l'uso di strutture di controllo (come if e
  for loop) e la creazione di macros, ovvero blocchi di codice SQL
  riutilizzabili, rendendo le query dinamiche e più potenti.<sup>4</sup>

- **Testing Automatizzato:** dbt permette di definire test di qualità
  dei dati direttamente nel progetto. Questi test possono essere
  generici (es. unicità di una chiave, assenza di valori nulli, valori
  accettati) o custom (basati su logiche di business specifiche),
  garantendo l'affidabilità dei dati prodotti.<sup>4</sup>

- **Documentazione Automatica e Lineage:** dbt è in grado di generare un
  sito web di documentazione per il progetto. Questo sito include
  descrizioni per modelli e colonne, i test definiti e, soprattutto, un
  Directed Acyclic Graph (DAG) interattivo che visualizza le dipendenze
  tra tutti i modelli, offrendo una chiara lineage dei dati.<sup>5</sup>

- **Gestione dei Pacchetti:** Similmente ai gestori di pacchetti nel
  software development (es. pip, npm), dbt ha un proprio package
  manager. Questo permette di installare e utilizzare pacchetti di
  codice dbt (contenenti macro e modelli) sviluppati dalla community,
  estendendo le funzionalità di base del proprio progetto.<sup>4</sup>

- **Snapshots:** Per le fonti di dati mutabili, dove i record possono
  cambiare nel tempo, dbt offre la funzionalità di snapshot. Questa
  permette di catturare e storicizzare lo stato di una tabella in un
  determinato momento, consentendo di ricostruire i valori
  storici.<sup>4</sup>

- **Seeds:** I file seed sono file CSV contenenti dati statici o che
  cambiano raramente (es. codici nazione, tabelle di lookup). dbt può
  caricare questi file direttamente nel data warehouse, rendendoli
  disponibili per essere utilizzati nei modelli.<sup>1</sup>

### **1.4. L'Ecosistema dbt: dbt Core vs. dbt Platform (Cloud)**

dbt si presenta in due versioni principali, ognuna adatta a esigenze
diverse <sup>4</sup>:

- **dbt Core:** È lo strumento open-source a riga di comando che
  costituisce il cuore di dbt. È pensato per utenti che preferiscono un
  controllo completo sul proprio ambiente, gestendo manualmente
  l'installazione, le dipendenze e l'orchestrazione delle esecuzioni (ad
  esempio tramite cron o strumenti come Airflow).<sup>4</sup>

- **dbt Platform (precedentemente dbt Cloud):** È la soluzione SaaS
  (Software as a Service) completamente gestita da dbt Labs. Offre
  un'esperienza integrata tramite un'interfaccia web che include un IDE
  (Studio IDE), scheduler di job, integrazione CI/CD, hosting della
  documentazione, monitoraggio e alerting. Semplifica notevolmente il
  deploy e la gestione dei progetti dbt, soprattutto per team di grandi
  dimensioni.<sup>2</sup>

La distinzione tra Core e Platform è fondamentale, poiché la scelta
iniziale impatta il modello operativo, i costi e le competenze tecniche
richieste al team. La tabella seguente fornisce un quadro comparativo
per guidare questa decisione.

**Tabella 1: dbt Core vs. dbt Platform: Confronto di Funzionalità e Casi
d'Uso**

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<thead>
<tr>
<th>Funzionalità</th>
<th>dbt Core</th>
<th>dbt Platform (Cloud)</th>
<th>Ideale per</th>
</tr>
<tr>
<th><strong>Ambiente di Sviluppo</strong></th>
<th>IDE locale a scelta (es. VSCode, Atom) + CLI</th>
<th>IDE web-based integrato (Studio IDE) + CLI</th>
<th>Core: Sviluppatori che preferiscono il proprio editor. Platform:
Team che cercano un'esperienza unificata e out-of-the-box.</th>
</tr>
<tr>
<th><strong>Scheduling dei Job</strong></th>
<th>Richiede un orchestratore esterno (es. cron, Airflow, Dagster,
Argo)</th>
<th>Scheduler integrato con interfaccia grafica, configurabile via
UI</th>
<th>Core: Team con infrastruttura di orchestrazione esistente. Platform:
Team che desiderano una soluzione di scheduling gestita.</th>
</tr>
<tr>
<th><strong>CI/CD</strong></th>
<th>Configurazione manuale in strumenti di CI/CD (es. GitHub Actions,
Jenkins)</th>
<th>Integrazione "chiavi in mano" con GitHub, GitLab, Azure DevOps per
build su Pull Request</th>
<th>Core: Team con competenze DevOps per configurare pipeline custom.
Platform: Team che vogliono implementare CI/CD rapidamente.</th>
</tr>
<tr>
<th><strong>Hosting Documentazione</strong></th>
<th>I file vengono generati localmente; richiede hosting separato (es.
S3, GitHub Pages)</th>
<th>Hosting automatico e gestito della documentazione, con controllo
degli accessi</th>
<th>Core: Flessibilità totale sull'hosting. Platform: Semplicità e
condivisione sicura della documentazione.</th>
</tr>
<tr>
<th><strong>Monitoraggio e Alerting</strong></th>
<th>Richiede integrazione con strumenti di monitoraggio esterni</th>
<th>Funzionalità integrate di alerting (email, Slack) e dashboard sui
tempi di esecuzione</th>
<th>Core: Integrazione con stack di observability esistente. Platform:
Soluzione di monitoraggio e alerting pronta all'uso.</th>
</tr>
<tr>
<th><strong>Costo</strong></th>
<th>Gratuito e open-source (costi legati all'infrastruttura di
esecuzione)</th>
<th>Modello di prezzo a sottoscrizione, basato su utente/utilizzo</th>
<th>Core: Team con budget limitato o che preferiscono soluzioni FOSS.
Platform: Team disposti a pagare per una soluzione gestita e un
time-to-value ridotto.</th>
</tr>
<tr>
<th><strong>Gestione</strong></th>
<th>L'utente è responsabile dell'installazione, degli aggiornamenti e
della manutenzione</th>
<th>Piattaforma completamente gestita da dbt Labs</th>
<th>Core: Controllo totale sull'ambiente. Platform: Riduzione del carico
operativo e di manutenzione.</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

Fonti: <sup>2</sup>

### **1.5. Vantaggi Strategici di dbt nel Modern Data Stack**

L'adozione di dbt all'interno di un'architettura dati moderna offre
vantaggi strategici che vanno oltre la semplice trasformazione:

- **Democratizzazione della Data Engineering:** dbt abbassa la barriera
  d'ingresso alla creazione di pipeline di dati. Analisti con solide
  competenze SQL possono ora costruire, testare e mantenere pipeline di
  qualità produttiva, riducendo la dipendenza da team di data
  engineering specializzati e accelerando il ciclo di
  analisi.<sup>2</sup>

- **Affidabilità e Collaborazione Migliorate:** La centralizzazione
  della logica di business in un repository Git condiviso migliora
  drasticamente la collaborazione. Si eliminano gli errori derivanti dal
  copia-incolla di codice SQL e si garantisce che tutte le analisi si
  basino su definizioni coerenti e versionate.<sup>4</sup>

- **Ottimizzazione di Performance e Costi:** dbt opera secondo un
  principio di "push-down", ovvero spinge l'esecuzione delle
  trasformazioni direttamente sulla piattaforma dati cloud (data
  warehouse o lakehouse), evitando costosi spostamenti di
  dati.<sup>5</sup> Funzionalità come i modelli incrementali, che
  processano solo i dati nuovi o modificati, e l'analisi dei metadati
  per ottimizzare i modelli lenti, contribuiscono a ridurre
  significativamente i tempi di esecuzione e i costi di calcolo
  associati.<sup>4</sup>

- **Flessibilità e Agnosticismo della Piattaforma:** Grazie a
  un'architettura basata su "adattatori" (adapter), dbt è agnostico
  rispetto al cloud provider (funziona su AWS, GCP, Azure) e supporta
  un'ampia gamma di piattaforme dati, tra cui Snowflake, BigQuery,
  Databricks, Redshift, Dremio, DuckDB e molte altre.<sup>5</sup> Questa
  flessibilità garantisce che l'investimento in competenze e processi
  dbt sia portabile tra diverse tecnologie.

## **Parte 2: Competenze Fondamentali: Installazione e Inizializzazione del Progetto**

Questa parte è un tutorial pratico che guida l'utente attraverso la
configurazione di un ambiente di sviluppo locale completo e la creazione
del suo primo progetto dbt, spiegando lo scopo di ogni file e directory
creati.

### **2.1. Preparazione dell'Ambiente di Sviluppo Locale**

Prima di installare dbt, è essenziale preparare un ambiente di sviluppo
pulito e isolato. Questo previene conflitti tra le dipendenze di diversi
progetti e garantisce la riproducibilità.

- **Prerequisiti:** È richiesta una familiarità di base con il terminale
  a riga di comando. Comandi come cd (change directory), ls (list
  contents) e pwd (print working directory) sono fondamentali per la
  navigazione nel file system.<sup>10</sup>

- **Installazione di Python:** dbt Core è un'applicazione Python e
  richiede una versione di Python 3.8 o successiva.<sup>12</sup> Per
  verificare la versione installata, è possibile eseguire il seguente
  comando nel terminale:  
  Bash  
  python3 --version

- **Ambienti Virtuali (venv):** La best practice assoluta per lo
  sviluppo Python è l'utilizzo di un ambiente virtuale. Questo crea una
  directory contenente un'installazione Python isolata, permettendo di
  installare le dipendenze di un progetto senza influenzare il sistema
  globale o altri progetti.<sup>12</sup> Per creare e attivare un
  ambiente virtuale, seguire questi passaggi:

  1.  **Creare l'ambiente virtuale:** Eseguire questo comando nella
      directory principale del progetto. Verrà creata una sottodirectory
      chiamata dbt-env.  
      Bash  
      python3 -m venv dbt-env

  2.  **Attivare l'ambiente virtuale:** Questo comando modifica il
      prompt del terminale per indicare che l'ambiente è attivo. Deve
      essere eseguito ogni volta che si inizia una nuova sessione di
      lavoro sul progetto.

      - **Su macOS/Linux:**  
        Bash  
        source dbt-env/bin/activate

      - **Su Windows (Command Prompt):**  
        Bash  
        dbt-env\Scripts\activate

Una volta attivato, qualsiasi pacchetto Python installato con pip verrà
inserito in questo ambiente isolato.

### **2.2. Installazione di dbt Core e degli Adattatori Essenziali**

Con l'ambiente virtuale attivo, si può procedere all'installazione di
dbt Core e degli adattatori necessari per connettersi alle piattaforme
dati.

- **Installazione tramite pip:** Il metodo raccomandato per
  l'installazione è pip, il package manager di Python.<sup>8</sup>

- **Struttura del Comando:** A partire dalle versioni più recenti, è
  necessario installare esplicitamente dbt-core insieme agli adattatori
  specifici. La sintassi è pip install dbt-core
  dbt-&lt;adapter-name&gt;.<sup>8</sup>

- **Esempio di Installazione:** Per gli scopi di questo report,
  installeremo dbt-core e gli adattatori per DuckDB e Dremio, che
  saranno approfonditi nella Parte 3.  
  Bash  
  pip install dbt-core dbt-duckdb dbt-dremio

- **Verifica dell'Installazione:** Dopo l'installazione, è buona norma
  verificare che dbt sia stato installato correttamente e sia
  accessibile dalla riga di comando.  
  Bash  
  dbt --version  
    
  Questo comando dovrebbe restituire la versione di dbt-core installata
  e le versioni degli adattatori. Se il comando non viene trovato,
  assicurarsi che l'ambiente virtuale sia attivo.<sup>13</sup>

### **2.3. Tutorial: Creare il Primo Progetto dbt con dbt init**

Il comando dbt init è lo strumento che permette di creare l'impalcatura
(scaffolding) di un nuovo progetto dbt, generando la struttura di
directory e i file di configurazione di base.

- **Guida Passo-Passo:**

  1.  **Navigare nella Directory di Lavoro:** Posizionarsi nella
      directory dove si desidera creare il progetto.

  2.  **Eseguire dbt init:** Lanciare il comando specificando il nome
      del progetto. Per questo tutorial, useremo
      jaffle\_shop\_lakehouse.  
      Bash  
      dbt init jaffle\_shop\_lakehouse

  3.  **Prompt Interattivo:** dbt avvierà un processo interattivo
      chiedendo a quale database connettersi e le relative credenziali.
      Per ora, è possibile interrompere questo processo (Ctrl+C), poiché
      configureremo la connessione manualmente nel prossimo
      passaggio.<sup>19</sup>

  4.  **Entrare nella Directory del Progetto:** Una volta creato,
      navigare all'interno della nuova directory.  
      Bash  
      cd jaffle\_shop\_lakehouse

  5.  **Esplorare la Struttura:** Usare ls -l o un esploratore di file
      per visualizzare la struttura di file e cartelle appena
      generata.<sup>10</sup>

### **2.4. Anatomia di un Progetto dbt: dbt\_project.yml e profiles.yml**

Due file sono al centro di ogni progetto dbt: dbt\_project.yml e
profiles.yml. La loro separazione è una scelta di progettazione
deliberata e critica che impone una best practice di sicurezza
fondamentale: la separazione del codice dai segreti. Poiché un progetto
dbt è destinato al controllo di versione con Git, commettere segreti
(password, chiavi API) in un repository è una grave vulnerabilità.
Posizionando profiles.yml in una directory esterna al progetto
(~/.dbt/), dbt previene la sua inclusione accidentale nel versioning,
spingendo gli sviluppatori a gestire le credenziali localmente o tramite
iniezione sicura di variabili d'ambiente nei sistemi di
CI/CD.<sup>10</sup> Questo non è solo un dettaglio organizzativo, ma un
meccanismo di protezione che guida verso un ciclo di sviluppo più sicuro
fin dall'inizio.

- **dbt\_project.yml:**

  - **Scopo:** È il file di configurazione principale del progetto.
    Definisce il nome del progetto, la versione, i percorsi per i
    diversi tipi di risorse (modelli, seed, test, ecc.) e le
    configurazioni di default per i modelli.<sup>10</sup>

  - **Esempio di Configurazione:**  
    YAML  
    name: 'jaffle\_shop\_lakehouse'  
    version: '1.0.0'  
    config-version: 2  
      
    \# Questo definisce quale profilo usare dal file profiles.yml  
    profile: 'jaffle\_shop\_lakehouse\_profile'  
      
    \# Definisce i percorsi per i vari tipi di file  
    model-paths: \["models"\]  
    analysis-paths: \["analyses"\]  
    test-paths: \["tests"\]  
    seed-paths: \["seeds"\]  
    macro-paths: \["macros"\]  
    snapshot-paths: \["snapshots"\]  
      
    \# Directory di output per i file compilati  
    target-path: "target"  
    \# Directory da pulire con 'dbt clean'  
    clean-targets:  
    - "target"  
    - "dbt\_packages"  
      
    \# Configurazioni di default per tutti i modelli nel progetto  
    models:  
    jaffle\_shop\_lakehouse:  
    \# Esempio: tutti i modelli in 'marts' saranno materializzati come
    tabelle  
    marts:  
    +materialized: table  
    \# Esempio: tutti i modelli in 'staging' saranno materializzati come
    viste  
    staging:  
    +materialized: view

- **profiles.yml:**

  - **Scopo:** Questo file contiene le credenziali di connessione alle
    piattaforme dati. È separato dal progetto per motivi di
    sicurezza.<sup>10</sup>

  - **Posizione:** Di default, dbt cerca questo file nella home
    directory dell'utente, in un percorso nascosto: ~/.dbt/profiles.yml.
    Se non esiste, deve essere creato.<sup>10</sup>

  - **Struttura:** Il file è organizzato per profili. Ogni profilo
    corrisponde a una configurazione nel dbt\_project.yml e contiene un
    blocco outputs con diversi target. I target permettono di definire
    ambienti separati (es. dev per lo sviluppo locale, prod per la
    produzione) con credenziali o configurazioni diverse.<sup>10</sup>

  - **Esempio di Struttura:**  
    YAML  
    jaffle\_shop\_lakehouse\_profile:  
    target: dev \# Il target di default da usare  
    outputs:  
    dev:  
    type: duckdb  
    path:../jaffle\_shop.duckdb \# Esempio per DuckDB  
    \#... altre configurazioni specifiche dell'adapter  
      
    prod:  
    type: dremio  
    \#... credenziali e configurazioni per l'ambiente di produzione

### **2.5. Comprendere la Struttura delle Directory Principali**

Il comando dbt init crea una struttura di directory standardizzata che
organizza i diversi componenti di un progetto.<sup>10</sup>

- models/: Il cuore del progetto. Contiene tutti i file .sql (e/o .py)
  che definiscono le trasformazioni. È buona pratica organizzarla in
  sottodirectory (es. staging, intermediate, marts).

- seeds/: Contiene file .csv per dati statici che possono essere
  caricati nel warehouse con il comando dbt seed.

- tests/: Contiene test personalizzati (chiamati anche "singular
  tests"). Si tratta di query SQL che devono restituire zero righe per
  passare.

- macros/: Contiene file .sql con macro Jinja riutilizzabili in tutto il
  progetto.

- snapshots/: Contiene le configurazioni per gli snapshot, usati per
  tracciare le modifiche ai dati nel tempo.

- analyses/: Contiene query SQL per analisi una tantum che non devono
  essere materializzate nel warehouse ma che beneficiano del versioning
  e del templating di dbt.

- target/: Questa directory viene creata automaticamente da dbt durante
  l'esecuzione dei comandi. Contiene il codice SQL compilato, i log e
  altri artefatti. **Deve essere sempre aggiunta al file .gitignore**
  per non essere versionata.

- dbt\_packages/: Questa directory viene creata quando si esegue dbt
  deps e contiene i pacchetti esterni scaricati. **Deve essere sempre
  aggiunta al file .gitignore**.

## **Parte 3: Architettura Avanzata: dbt nell'Open Data Lakehouse**

Questa è la sezione di approfondimento tecnico principale. Descrive in
dettaglio come utilizzare dbt per costruire un moderno data lakehouse su
S3, utilizzando formati di file aperti come Parquet e Iceberg e motori
di query come Dremio e DuckDB. Sarà ricca di esempi di configurazione e
diagrammi architettonici.

### **3.1. Principi Architettonici: La Medallion Architecture sul Lakehouse**

Un approccio consolidato per organizzare i dati in un data lakehouse è
la Medallion Architecture. Questo pattern prevede una strutturazione
logica dei dati in tre livelli, migliorando progressivamente la qualità
e l'usabilità dei dati man mano che attraversano la
pipeline.<sup>23</sup>

- **Livello Bronze (Raw Data):** È la zona di atterraggio per i dati
  grezzi provenienti dai sistemi sorgente. I dati vengono archiviati su
  S3 "as-is", mantenendo la struttura e il formato originali. In un
  progetto dbt, questi dati vengono definiti come sources nel file
  sources.yml. Questo livello garantisce che esista sempre una copia
  fedele e immutabile dei dati sorgente, fondamentale per la
  rielaborazione e l'auditing.

- **Livello Silver (Cleansed & Conformed Data):** I dati del livello
  Bronze vengono qui puliti, de-duplicati, conformati e integrati. È in
  questo strato che operano i primi livelli di modelli dbt, tipicamente
  i modelli di staging e intermediate. L'obiettivo è creare una visione
  d'impresa pulita e coerente delle entità di business chiave.

- **Livello Gold (Curated & Aggregated Data):** I dati vengono aggregati
  e modellati per specifici casi d'uso di business, come dashboard di
  Business Intelligence, analisi avanzate o input per modelli di Machine
  Learning. Questi sono i modelli di marts in dbt, che producono tabelle
  finali, spesso denormalizzate e ottimizzate per le letture.

Questa architettura a più livelli si adatta perfettamente al flusso di
lavoro di dbt, che gestisce le dipendenze tra i modelli in modo
automatico, e si allinea con i principi del data mesh, dove i dati
vengono trattati come prodotti.<sup>23</sup>

### **3.2. Lo Strato di Storage: Sfruttare S3 con Parquet e Apache Iceberg**

La scelta del formato dei file e della tecnologia di gestione delle
tabelle è cruciale per le prestazioni e l'affidabilità di un data
lakehouse.

#### **3.2.1. Lavorare con File Parquet**

Parquet è un formato di storage colonnare open-source, ottimizzato per
carichi di lavoro analitici. La sua struttura permette ai motori di
query di leggere solo le colonne necessarie per una specifica
interrogazione, riducendo drasticamente l'I/O e accelerando le
performance.<sup>25</sup> dbt, di per sé, non legge o scrive file.
Piuttosto, genera codice SQL che viene eseguito da un motore di query
(come DuckDB, Dremio o Spark). Se il motore di query supporta la lettura
e la scrittura di file Parquet su S3, allora dbt può essere utilizzato
per orchestrare queste operazioni.<sup>26</sup>

#### **3.2.2. Gestione Avanzata delle Tabelle con Apache Iceberg e dbt Catalog Integration**

Mentre Parquet definisce come i dati sono memorizzati *all'interno* di
un file, Apache Iceberg è un formato di tabella aperto che definisce
come i file sono organizzati per formare una tabella. Iceberg aggiunge
funzionalità tipiche dei database tradizionali al mondo dei data lake,
come transazioni ACID, evoluzione dello schema senza interruzioni
(schema evolution), partizionamento nascosto e time travel (la capacità
di interrogare la tabella com'era in un preciso momento
passato).<sup>23</sup>

dbt supporta nativamente la materializzazione dei modelli come tabelle
Iceberg, una funzionalità chiave per costruire un lakehouse
affidabile.<sup>30</sup> Esistono due approcci per la configurazione:

1.  **Approccio Legacy:** Utilizzare il campo di configurazione
    table\_format = 'iceberg' direttamente nel file del modello.

2.  **Approccio Moderno (Raccomandato):** Utilizzare l'**integrazione
    del catalogo** (catalog integration). Questo approccio, più recente
    e robusto, centralizza la configurazione del catalogo e la rende più
    manutenibile.<sup>33</sup>

Il cuore di Iceberg è il **Catalogo**, un servizio che tiene traccia dei
metadati della tabella (schema, partizioni, snapshot). dbt interagisce
con il catalogo tramite l'adattatore del motore di query. Ad esempio,
quando si utilizza dbt con Snowflake, si può configurare dbt per creare
tabelle Iceberg il cui metadato è gestito dal catalogo interno di
Snowflake o da un catalogo esterno come AWS Glue, Polaris o
Nessie.<sup>33</sup>

Un esempio di configurazione di un modello dbt per creare una tabella
Iceberg gestita da Snowflake potrebbe essere:

> SQL

{{  
config(  
materialized = "table",  
table\_format = "iceberg",  
external\_volume = "s3\_iceberg\_snow"  
)  
}}  
  
select \* from {{ ref('raw\_orders') }}

In questo caso, dbt istruisce Snowflake a creare una tabella in formato
Iceberg, scrivendo i file di dati nel volume esterno s3\_iceberg\_snow
(che punta a un bucket S3). dbt gestisce automaticamente il parametro
base\_location per organizzare i dati all'interno del volume, prevenendo
il disordine e il debito tecnico.<sup>33</sup>

### **3.3. Approfondimento sul Motore di Query: Dremio come Lakehouse Engine**

Dremio è una piattaforma open data lakehouse che offre un motore di
query SQL ad alte prestazioni in grado di interrogare i dati
direttamente dove risiedono, inclusi file Parquet e Iceberg su S3, senza
la necessità di copiarli o spostarli.<sup>35</sup>

#### **3.3.1. Configurazione dell'Adattatore dbt-dremio per Cloud e Software**

Per utilizzare dbt con Dremio, è necessario configurare correttamente
l'adattatore dbt-dremio nel file profiles.yml. La configurazione varia a
seconda che si utilizzi Dremio Cloud (la versione SaaS) o Dremio
Software (la versione self-hosted).<sup>17</sup>

La tabella seguente riassume i parametri di configurazione chiave,
fornendo una guida consolidata per prevenire errori comuni di
connessione.

**Tabella 2: Parametri di Configurazione Chiave dell'Adattatore
dbt-dremio**

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr>
<th>Parametro</th>
<th>Obbligatorio</th>
<th>Descrizione</th>
<th>Esempio (Cloud)</th>
<th>Esempio (Software)</th>
</tr>
<tr>
<th>type</th>
<th>Sì</th>
<th>Tipo di adattatore. Deve essere dremio.</th>
<th>dremio</th>
<th>dremio</th>
</tr>
<tr>
<th>threads</th>
<th>Sì</th>
<th>Numero di thread paralleli per l'esecuzione di dbt.</th>
<th>4</th>
<th>4</th>
</tr>
<tr>
<th>user</th>
<th>Sì</th>
<th>Email dell'utente per Dremio Cloud o username per Dremio
Software.</th>
<th>user@example.com</th>
<th>dremio_user</th>
</tr>
<tr>
<th>pat</th>
<th>Sì (Cloud)</th>
<th>Personal Access Token per l'autenticazione. Prevale su user/password
se presente.</th>
<th>{{ env_var('DREMIO_PAT') }}</th>
<th>{{ env_var('DREMIO_PAT') }}</th>
</tr>
<tr>
<th>password</th>
<th>Sì (Software, se non si usa PAT)</th>
<th>Password per l'autenticazione con username.</th>
<th>N/A</th>
<th>{{ env_var('DREMIO_PASSWORD') }}</th>
</tr>
<tr>
<th>cloud_host</th>
<th>Sì (Cloud)</th>
<th>Endpoint API di Dremio Cloud. Varia tra US e EU.</th>
<th>api.dremio.cloud</th>
<th>N/A</th>
</tr>
<tr>
<th>cloud_project_id</th>
<th>Sì (Cloud)</th>
<th>ID del progetto Dremio Cloud (Sonar) da utilizzare.</th>
<th>1ab23-c456-78d9-e01f-234g</th>
<th>N/A</th>
</tr>
<tr>
<th>software_host</th>
<th>Sì (Software)</th>
<th>Hostname o IP del nodo coordinatore del cluster Dremio.</th>
<th>N/A</th>
<th>192.168.1.100</th>
</tr>
<tr>
<th>port</th>
<th>Sì (Software)</th>
<th>Porta API del cluster Dremio. Default: 9047.</th>
<th>N/A</th>
<th>9047</th>
</tr>
<tr>
<th>use_ssl</th>
<th>Sì</th>
<th>Indica se usare TLS. true per Cloud, true o false per Software.</th>
<th>true</th>
<th>true</th>
</tr>
<tr>
<th>object_storage_source</th>
<th>No</th>
<th>Nome della sorgente Dremio (es. S3, Glue) dove materializzare le
tabelle. Default: $scratch.</th>
<th>MyS3Source</th>
<th>MyS3Source</th>
</tr>
<tr>
<th>dremio_space</th>
<th>No</th>
<th>Nome dello "Spazio" Dremio dove creare le viste. Default:
@username.</th>
<th>analytics_space</th>
<th>analytics_space</th>
</tr>
<tr>
<th>dremio_space_folder</th>
<th>No</th>
<th>Sottocartella all'interno dello Spazio per le viste.</th>
<th>gold_layer</th>
<th>gold_layer</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

Fonti: <sup>17</sup>

#### **3.3.2. Strategie di Materializzazione e Ottimizzazione con Dremio**

Quando si esegue dbt con Dremio, le materializzazioni si traducono in
oggetti specifici:

- materialized='table' crea tabelle fisiche (es. file Parquet/Iceberg)
  nella sorgente di object storage specificata
  (object\_storage\_source).<sup>17</sup>

- materialized='view' crea viste logiche all'interno di uno "Spazio"
  Dremio (dremio\_space).<sup>17</sup>

- materialized='incremental' aggiorna le tabelle fisiche in modo
  incrementale.

Una caratteristica potente di Dremio è la capacità di sincronizzare la
documentazione e i tag di dbt direttamente con il catalogo dati di
Dremio. Questo arricchisce la data discovery e la governance, rendendo
le descrizioni dei modelli e delle colonne di dbt visibili
nell'interfaccia di Dremio.<sup>37</sup>

### **3.4. Approfondimento sul Motore di Query: DuckDB per Sviluppo Locale e Interoperabilità S3**

DuckDB è un database analitico in-process, estremamente veloce, che sta
rivoluzionando lo sviluppo locale. La sua capacità di leggere e scrivere
direttamente su file remoti (come quelli su S3) lo rende uno strumento
eccezionale per un flusso di lavoro "local-first" su un'architettura
lakehouse.<sup>38</sup>

L'abbinamento di dbt-duckdb con l'accesso a S3 sta cambiando l'economia
e l'accessibilità dell'analytics engineering. Crea di fatto un
"lakehouse serverless e local-first", disaccoppiando il workflow di
sviluppo analitico dai costosi e sempre attivi calcoli dei data
warehouse cloud. Mentre i flussi di lavoro tradizionali di dbt
richiedevano una connessione a un data warehouse cloud (Snowflake,
BigQuery, ecc.), con costi di calcolo per ogni dbt run, l'adattatore
dbt-duckdb, combinato con l'estensione httpfs, permette a dbt di
utilizzare un motore locale, gratuito ed estremamente veloce (DuckDB)
per leggere e scrivere direttamente su uno storage a basso costo
(S3).<sup>18</sup> Ciò significa che un'intera pipeline ELT può essere
sviluppata, testata ed eseguita sul laptop di uno sviluppatore,
interagendo con il cloud solo per l'I/O dello storage, non per il
calcolo. Questo riduce drasticamente i costi di sviluppo e rispecchia
una tendenza moderna dello sviluppo software: strumenti locali potenti
che interagiscono senza soluzione di continuità con le risorse cloud.
Non si tratta solo di un nuovo adattatore, ma di un nuovo paradigma per
lo sviluppo con dbt, più accessibile, economico e portabile.

#### **3.4.1. Configurazione dell'Adattatore dbt-duckdb e delle Estensioni (httpfs, parquet)**

Per sfruttare appieno DuckDB, il file profiles.yml deve essere
configurato per caricare le estensioni necessarie e fornire le
credenziali per l'accesso a S3.<sup>18</sup>

**Tabella 3: Parametri Chiave dell'Adattatore dbt-duckdb per
l'Integrazione S3**

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<thead>
<tr>
<th>Parametro</th>
<th>Livello</th>
<th>Descrizione</th>
<th>Valore di Esempio</th>
</tr>
<tr>
<th>type</th>
<th>Output</th>
<th>Tipo di adattatore. Deve essere duckdb.</th>
<th>duckdb</th>
</tr>
<tr>
<th>path</th>
<th>Output</th>
<th>Percorso del file database DuckDB locale. Può essere omesso per un
database in memoria.</th>
<th>dbt_local.duckdb</th>
</tr>
<tr>
<th>extensions</th>
<th>Output</th>
<th>Lista di estensioni DuckDB da caricare. httpfs è essenziale per
l'accesso a S3.</th>
<th>['httpfs', 'parquet']</th>
</tr>
<tr>
<th>settings</th>
<th>Output</th>
<th>Blocco per le opzioni di configurazione di DuckDB e delle sue
estensioni.</th>
<th>(Vedi sotto)</th>
</tr>
<tr>
<th>s3_region</th>
<th>settings</th>
<th>Regione AWS del bucket S3.</th>
<th>eu-west-1</th>
</tr>
<tr>
<th>s3_access_key_id</th>
<th>settings</th>
<th>ID della chiave di accesso AWS.</th>
<th>{{ env_var('AWS_ACCESS_KEY_ID') }}</th>
</tr>
<tr>
<th>s3_secret_access_key</th>
<th>settings</th>
<th>Chiave di accesso segreta AWS.</th>
<th>{{ env_var('AWS_SECRET_ACCESS_KEY') }}</th>
</tr>
<tr>
<th>filesystems</th>
<th>Output</th>
<th>(Alternativa a settings) Blocco per configurare filesystem esterni
tramite fsspec.</th>
<th>[{'fs': 's3', 'key': '...', 'secret': '...'}]</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

Fonti: <sup>18</sup>

Un esempio completo di profiles.yml per dbt-duckdb con accesso a S3 è:

> YAML

local\_lakehouse:  
target: dev  
outputs:  
dev:  
type: duckdb  
path: jaffle\_shop.duckdb  
extensions:  
- httpfs  
- parquet  
settings:  
s3\_region: 'us-east-1'  
s3\_access\_key\_id: "{{ env\_var('S3\_ACCESS\_KEY\_ID') }}"  
s3\_secret\_access\_key: "{{ env\_var('S3\_SECRET\_ACCESS\_KEY') }}"

#### **3.4.2. Casi d'Uso: Sviluppo Local-First e Query Dirette su S3**

Con questa configurazione, uno sviluppatore può eseguire un'intera
pipeline lakehouse sul proprio laptop:

1.  **Definire una sorgente S3:** Nel file sources.yml, si può definire
    una tabella che legge direttamente da uno o più file Parquet su
    S3.  
    YAML  
    version: 2  
    sources:  
    - name: raw\_data\_s3  
    tables:  
    - name: customers  
    meta:  
    external\_location:
    "read\_parquet('s3://my-bronze-bucket/customers/\*.parquet')"

2.  **Materializzare su S3:** Un modello dbt può essere configurato per
    scrivere il suo output come un nuovo file Parquet in un altro
    percorso S3, utilizzando una materializzazione custom o un
    post-hook.  
    SQL  
    {{  
    config(  
    materialized='table'  
    )  
    }}  
    -- post-hook per esportare la tabella in Parquet su S3  
    -- {{ config(post\_hook="COPY (SELECT \* FROM {{ this }}) TO
    's3://my-gold-bucket/dim\_customers.parquet' (FORMAT 'parquet')")
    }}  
      
    SELECT \* FROM {{ source('raw\_data\_s3', 'customers') }}  
    --... logica di trasformazione...

Inoltre, dbt-duckdb supporta la connessione a MotherDuck, una versione
serverless e cloud di DuckDB, semplicemente modificando il path nel
profilo, offrendo un'opzione cloud-native per chi non vuole gestire un
database locale.<sup>40</sup>

### **3.5. Architettura di Riferimento: Scenario di una Pipeline Lakehouse Integrata**

Per consolidare i concetti, consideriamo un'architettura di riferimento
per il nostro progetto jaffle\_shop\_lakehouse.

**Diagramma Architettonico:**

+----------------+ +------------------+ +-------------+
+--------------------------+  
| Sorgenti |-----&gt;| S3 (Bronze) |-----&gt;| Query Engine|-----&gt;|
dbt (Trasformazione) |  
| (es. DB, API) | | (File Parquet) | | (Dremio o | | (Staging,
Intermediate) |  
+----------------+ +------------------+ | DuckDB) |
+-------------+------------+  
+-------------+ |  
|  
v  
+--------------------------+  
| S3 (Silver/Gold) |  
| (Tabelle Iceberg/Parquet)|  
+--------------------------+

**Scenario jaffle\_shop:**

1.  **Dati Sorgente:** I dati grezzi di customers e orders vengono
    estratti e caricati come file Parquet nel bucket S3
    s3://jaffle-shop-bronze/.

2.  **sources.yml in dbt:**  
    YAML  
    version: 2  
    sources:  
    - name: jaffle\_shop\_raw  
    schema: main \# Schema virtuale per DuckDB  
    tables:  
    - name: raw\_customers  
    meta:  
    external\_location:
    "read\_parquet('s3://jaffle-shop-bronze/customers.parquet')"  
    - name: raw\_orders  
    meta:  
    external\_location:
    "read\_parquet('s3://jaffle-shop-bronze/orders.parquet')"

3.  **Modello di Staging (models/staging/stg\_customers.sql):**  
    SQL  
    select  
    id as customer\_id,  
    first\_name,  
    last\_name  
    from {{ source('jaffle\_shop\_raw', 'raw\_customers') }}

4.  **Modello Mart (models/marts/fct\_orders.sql):**  
    SQL  
    {{  
    config(  
    materialized='incremental',  
    unique\_key='order\_id',  
    -- Configurazione per materializzare come tabella Iceberg con
    Dremio/Snowflake  
    -- table\_format='iceberg'  
    )  
    }}  
      
    select  
    o.id as order\_id,  
    o.user\_id as customer\_id,  
    o.order\_date,  
    o.status  
    from {{ source('jaffle\_shop\_raw', 'raw\_orders') }} as o  
      
    {% if is\_incremental() %}  
    where order\_date &gt; (select max(order\_date) from {{ this }})  
    {% endif %}

Questo progetto può essere eseguito sia localmente con DuckDB per uno
sviluppo rapido, sia in un ambiente di produzione con Dremio per
interrogazioni su larga scala, semplicemente cambiando il target nel
comando dbt run.

## **Parte 4: Eccellenza Ingegneristica: Sviluppo, Versioning e Best Practice**

Questa sezione codifica i principi e le pratiche necessarie per
costruire e mantenere un progetto dbt di alta qualità e scalabile. Si
passa da concetti astratti a consigli concreti e attuabili.

### **4.1. Il Ciclo di Vita dello Sviluppo dbt: dal Codice alla Produzione**

Il flusso di lavoro tipico di un analytics engineer che utilizza dbt
segue un percorso strutturato che rispecchia le best practice dello
sviluppo software <sup>42</sup>:

1.  **Creazione di un Feature Branch:** Ogni nuova funzionalità o
    correzione di bug inizia con la creazione di un nuovo branch in Git
    dal branch principale (es. main o develop). Questo isola il lavoro
    in corso e previene interferenze.

2.  **Sviluppo e Modifica dei Modelli:** Lo sviluppatore lavora nel
    proprio IDE locale, modificando i file .sql e .yml per implementare
    la logica di trasformazione richiesta.

3.  **Esecuzione e Test Locali:** Durante lo sviluppo, i modelli vengono
    eseguiti e testati ripetutamente contro un ambiente di sviluppo.
    Questo ambiente è tipicamente uno schema personale nel data
    warehouse, garantendo che le modifiche non impattino altri
    sviluppatori o l'ambiente di produzione.

4.  **Aggiunta di Test e Documentazione:** Parallelamente allo sviluppo
    del codice, vengono aggiunti o aggiornati i test di qualità dei dati
    e la documentazione per i nuovi modelli o le colonne modificate.

5.  **Apertura di una Pull Request (PR):** Una volta che lo sviluppo è
    completo e i test locali passano, lo sviluppatore apre una Pull
    Request. Questo è un meccanismo formale per proporre le modifiche al
    branch principale e avviare un processo di code review.

6.  **Continuous Integration (CI):** L'apertura della PR scatena
    automaticamente una pipeline di CI, che esegue tutti i modelli e i
    test in un ambiente isolato e temporaneo per convalidare le
    modifiche.

7.  **Merge e Continuous Deployment (CD):** Dopo l'approvazione della PR
    e il successo della CI, il branch viene unito (merged) al branch
    principale. Questo merge può a sua volta scatenare una pipeline di
    CD che distribuisce le modifiche in produzione.

### **4.2. Integrazione con Git e Flussi di Lavoro Collaborativi**

L'uso di un sistema di controllo di versione come Git è un prerequisito
non negoziabile per qualsiasi progetto dbt professionale.<sup>42</sup>

#### **4.2.1. Il Ruolo Fondamentale di Git**

Git fornisce la spina dorsale per la collaborazione, la tracciabilità
delle modifiche e la governance del codice. Ogni modifica è registrata,
attribuita a un autore e può essere ispezionata o annullata, creando una
storia completa e auditabile del progetto.

#### **4.2.2. Strategie di Branching per Team di Dati**

La scelta di una strategia di branching dipende dalla dimensione del
team, dalla complessità del progetto e dai requisiti di rilascio.

- **Direct Promotion (es. GitHub Flow):** In questa strategia semplice e
  veloce, i feature branch vengono creati direttamente dal branch main
  e, una volta completati e revisionati, vengono uniti di nuovo in main.
  Il branch main rappresenta sempre lo stato della produzione. Questo
  modello è ideale per team piccoli o per progetti che beneficiano di
  rilasci rapidi e continui.<sup>45</sup>

- **Indirect Promotion (es. GitFlow):** Questo approccio più strutturato
  introduce branch intermedi, come develop o qa. I feature branch
  vengono uniti in develop. I rilasci in produzione avvengono unendo
  develop in main a intervalli pianificati. Questo fornisce un ulteriore
  livello di validazione e test in un ambiente di staging ed è più
  adatto a team grandi, progetti complessi o ambienti con requisiti di
  conformità stringenti.<sup>45</sup>

Indipendentemente dalla strategia, è fondamentale utilizzare le **Pull
Request** per la revisione del codice e applicare **regole di protezione
dei branch** (branch protection rules) su main e altri branch a lunga
vita per impedire merge non autorizzati o non testati.<sup>42</sup>

### **4.3. Best Practice per un Progetto Scalabile e Manutenibile**

La struttura di un progetto dbt è un'applicazione diretta del principio
di ingegneria del software della "separazione delle responsabilità"
(separation of concerns) alla modellazione dei dati. Non è una
convenzione arbitraria, ma un pattern di progettazione che isola
deliberatamente diversi tipi di logica per massimizzare la
manutenibilità e la riusabilità.

Il layer di staging si occupa esclusivamente di creare un'interfaccia
pulita e coerente con i dati grezzi, gestendo le idiosincrasie della
fonte (rinominare, castare).<sup>47</sup> Questo isola il resto del
progetto dai cambiamenti a monte: se una colonna sorgente viene
rinominata, solo un modello di staging deve essere aggiornato.

Il layer intermediate si occupa di implementare logiche di business
complesse e riutilizzabili, unendo e trasformando i modelli di
staging.<sup>48</sup>

Infine, il layer marts si occupa della presentazione dei dati,
concentrandosi sulla selezione e l'organizzazione delle colonne per un
pubblico specifico (es. uno strumento di BI), agendo come "strato API"
per i consumatori di dati.<sup>48</sup> Questa separazione previene la
creazione di modelli monolitici e illeggibili e garantisce che una
modifica alla logica di business (layer intermedio) non richieda di
intervenire sul codice di pulizia della fonte (layer di staging), e che
una modifica al layout di un report finale (layer dei marts) non rischi
di compromettere la logica di business principale.

#### **4.3.1. Strutturazione del Progetto: Staging, Intermediate e Marts**

La directory models/ dovrebbe essere organizzata secondo una logica che
riflette il flusso dei dati e la Medallion Architecture.<sup>47</sup>

- models/staging: Contiene modelli che hanno una relazione uno-a-uno con
  le tabelle sorgente. Le uniche trasformazioni consentite sono
  rinominare le colonne (es. da user\_id a customer\_id), eseguire il
  casting dei tipi di dato (es. da string a timestamp) e altre pulizie
  di base. I file sono tipicamente prefissati con stg\_ (es.
  stg\_customers.sql).

- models/intermediate: Qui avviene la magia. Questi modelli uniscono
  diversi modelli di staging, applicano logiche di business complesse e
  preparano i dati per i modelli finali. Spesso non sono esposti
  direttamente agli utenti finali. I file possono essere prefissati con
  int\_ (es. int\_orders\_aggregated.sql).

- models/marts: Contiene i modelli finali, pronti per il consumo. Si
  tratta di tabelle ampie, denormalizzate, che uniscono dati da vari
  modelli intermedi per servire specifiche aree di business (es.
  marketing, finanza). I file sono spesso prefissati con dim\_ per le
  tabelle dimensionali (es. dim\_customers.sql) e fct\_ per le tabelle
  dei fatti (es. fct\_orders.sql).

#### **4.3.2. Convenzioni di Nomenclatura per Modelli, Colonne e Sorgenti**

Adottare e far rispettare una guida di stile è fondamentale per la
leggibilità e la manutenibilità a lungo termine.<sup>42</sup> Le
convenzioni raccomandate da dbt Labs includono <sup>52</sup>:

- **Case:** Usare snake\_case per tutti gli oggetti (modelli, colonne,
  schemi).

- **Nomi dei Modelli:** I modelli dovrebbero avere nomi al plurale (es.
  orders, customers).

- **Chiavi Primarie:** La chiave primaria di un modello dovrebbe essere
  nominata &lt;oggetto&gt;\_id (es. order\_id, customer\_id).

- **Colonne Booleane:** Prefissare le colonne booleane con is\_ o has\_
  (es. is\_active, has\_ordered).

- **Timestamp e Date:** Le colonne timestamp dovrebbero terminare con
  \_at (es. created\_at), mentre le date dovrebbero terminare con \_date
  (es. order\_date).

- **Nomi Espliciti:** Evitare abbreviazioni. Usare customer\_id invece
  di cust\_id.

#### **4.3.3. Scrivere Codice dbt Pulito, Modulare e DRY**

- **Usare ref() e source():** Non fare mai riferimento a una tabella
  hardcodando il suo nome (es. my\_schema.my\_table). Usare sempre le
  funzioni {{ ref('nome\_modello') }} e {{ source('nome\_sorgente',
  'nome\_tabella') }}. Questo permette a dbt di inferire automaticamente
  le dipendenze e costruire il DAG.<sup>42</sup>

- **Scomporre la Complessità:** Modelli SQL molto lunghi con numerose
  CTE (Common Table Expressions) sono difficili da leggere, testare e
  manutenere. È una best practice scomporli in modelli intermedi più
  piccoli e focalizzati. Ogni modello intermedio realizza un passo
  logico della trasformazione.<sup>42</sup>

- **Sfruttare le Macro:** Per logiche SQL ripetitive (es. conversione di
  valuta, calcolo di una metrica standard), creare una macro nella
  directory macros/. Questo centralizza la logica e la rende
  riutilizzabile in tutto il progetto, seguendo il principio
  DRY.<sup>42</sup>

- **Limitare i Dati in Sviluppo:** Per accelerare il ciclo di sviluppo
  locale, è possibile usare una condizione Jinja per limitare il volume
  di dati processati quando si esegue dbt in ambiente di sviluppo.  
  SQL  
  {% if target.name == 'dev' %}  
  where order\_date &gt;= dateadd('day', -30, current\_date)  
  {% endif %}  
    
  Questo esempio limita l'elaborazione agli ultimi 30 giorni di dati
  solo quando il target è dev.<sup>47</sup>

### **4.4. Una Cultura della Qualità: Approfondimento su Test e Documentazione in dbt**

Un progetto dbt non è completo senza un solido framework di test e una
documentazione chiara.

- **Testing:**

  - La filosofia è quella dello "shift left": identificare e correggere
    i problemi di qualità dei dati durante lo sviluppo, non quando hanno
    già causato danni in produzione.<sup>55</sup>

  - **Test Generici:** dbt fornisce quattro test generici pronti
    all'uso: unique, not\_null, accepted\_values e relationships. Si
    applicano facilmente nei file .yml a livello di colonna.  
    YAML  
    models:  
    - name: dim\_customers  
    columns:  
    - name: customer\_id  
    tests:  
    - unique  
    - not\_null  
    - name: status  
    tests:  
    - accepted\_values:  
    values: \['active', 'inactive'\]

  - **Test Singolari (Custom):** Per logiche di business più complesse,
    è possibile scrivere un test personalizzato. Si tratta di una query
    SQL salvata nella directory tests/ che, per passare, deve restituire
    zero righe.<sup>55</sup>

  - **Best Practice:** Ogni modello dovrebbe avere come minimo test
    unique e not\_null sulla sua chiave primaria.<sup>47</sup>

- **Documentazione:**

  - **Descrizioni:** È possibile aggiungere descrizioni a modelli e
    colonne direttamente nei file .yml usando la chiave description.
    Queste descrizioni appariranno nel sito di documentazione generato.

  - Blocchi doc: Per descrizioni lunghe o riutilizzabili, si può usare
    la funzione doc. Si crea un file markdown (es. docs/descriptions.md)
    e si definisce un blocco di documentazione.  
    {% docs customer\_id\_description %}  
    This is the unique identifier for a customer. It is generated from
    the source system.  
    {% enddocs %}  
    Questo blocco può poi essere referenziato nel file .yml:
    description: "{{ doc('customer\_id\_description') }}".50

  - **Generazione del Sito:** I comandi dbt docs generate e dbt docs
    serve vengono usati rispettivamente per generare gli artefatti della
    documentazione e per avviare un server web locale che la ospita,
    rendendola navigabile.<sup>7</sup>

## **Parte 5: Produzione: dallo Sviluppo Locale al Deploy su Kubernetes**

Questa sezione finale fornisce una guida pratica per rendere operativo
un progetto dbt, concentrandosi sulla containerizzazione e
l'orchestrazione con Kubernetes, come richiesto dall'utente.

### **5.1. Il Ciclo di Sviluppo Locale: un Flusso di Lavoro Pratico**

Sintetizzando le best practice, un ciclo di sviluppo locale concreto
potrebbe assomigliare a questo <sup>47</sup>:

1.  **Creare un branch:** git checkout -b feature/new-customer-logic

2.  **Sviluppare il codice:** Modificare i file .sql e .yml in un IDE
    come VSCode.

3.  **Eseguire il modello modificato e le sue dipendenze a valle:** dbt
    run --select +my\_changed\_model

4.  **Testare il modello modificato:** dbt test --select
    my\_changed\_model

5.  **Committare le modifiche:** git commit -m "feat: implement new
    customer logic"

6.  **Push e apertura della Pull Request:** git push origin
    feature/new-customer-logic

### **5.2. Containerizzare il Progetto dbt con Docker**

Per eseguire dbt in un ambiente di produzione come Kubernetes, il primo
passo è creare un'immagine Docker. Un container Docker incapsula il
codice del progetto dbt, le sue dipendenze Python e le configurazioni
necessarie, creando un artefatto portabile e riproducibile.

Un Dockerfile di esempio per un progetto dbt potrebbe essere:

> Dockerfile

\# Usa un'immagine Python ufficiale come base  
FROM python:3.11-slim  
  
\# Imposta la directory di lavoro nel container  
WORKDIR /usr/app/dbt  
  
\# Copia i requisiti e installa le dipendenze per sfruttare il caching
di Docker  
COPY requirements.txt.  
RUN pip install --no-cache-dir -r requirements.txt  
  
\# Copia l'intero progetto dbt nella directory di lavoro  
COPY..  
  
\# Specifica la directory del progetto dbt per i comandi successivi  
ENV DBT\_PROJECT\_DIR=.  
  
\# Imposta il punto di ingresso per eseguire i comandi dbt  
ENTRYPOINT \["dbt"\]

Il file requirements.txt conterrà le dipendenze, come dbt-core,
dbt-duckdb, ecc. L'immagine viene costruita con il comando docker build
-t mio-progetto-dbt:latest..

### **5.3. Orchestrazione su Kubernetes: Strategie e Pattern**

dbt Core è uno strumento a riga di comando e necessita di un
orchestratore esterno per essere eseguito in produzione. Kubernetes è
una scelta potente e flessibile per questo compito.<sup>57</sup> La
scelta dello strumento di orchestrazione su Kubernetes rappresenta un
compromesso diretto tra semplicità e controllo, riflettendo la maturità
operativa di un team. Un CronJob è il punto di ingresso, semplice e
dichiarativo, ideale per esecuzioni schedulate e stateless.<sup>60</sup>
Tuttavia, manca di controllo granulare, gestione delle dipendenze
esterne e osservabilità avanzata. Strumenti come Airflow e Argo
Workflows sono stati introdotti per risolvere queste limitazioni,
offrendo una gestione robusta delle dipendenze (anche tra sistemi
diversi), scheduling complesso, parametrizzazione, meccanismi di retry
avanzati e interfacce utente ricche per l'osservabilità.<sup>59</sup>
L'adozione di Airflow con KubernetesPodOperator o di Argo Workflows
rappresenta un livello superiore di maturità operativa, indicando la
necessità di gestire non solo il job dbt, ma un'intera piattaforma di
orchestrazione. La decisione, quindi, dovrebbe basarsi sulla complessità
dell'intero ecosistema dati, non solo della porzione dbt.

#### **5.3.1. Scheduling Semplice con Kubernetes CronJobs**

Il modo più semplice per eseguire dbt su una schedulazione fissa in
Kubernetes è tramite un oggetto CronJob.<sup>60</sup> Questo oggetto
crea un

Job a intervalli di tempo definiti, che a sua volta avvia un Pod per
eseguire il container dbt.

Un file cronjob.yaml di esempio:

> YAML

apiVersion: batch/v1  
kind: CronJob  
metadata:  
name: dbt-nightly-run  
spec:  
schedule: "0 2 \* \* \*" \# Esegui ogni notte alle 2:00 UTC  
jobTemplate:  
spec:  
template:  
spec:  
containers:  
- name: dbt-runner  
image: mio-progetto-dbt:latest  
command: \["dbt", "run", "--target", "prod"\]  
env:  
- name: DBT\_PROFILES\_DIR  
value: "/usr/app/dbt/.dbt"  
- name: DREMIO\_PAT  
valueFrom:  
secretKeyRef:  
name: dremio-credentials  
key: pat  
restartPolicy: OnFailure

In questo esempio, le credenziali sono gestite in modo sicuro. Viene
creato un Secret Kubernetes chiamato dremio-credentials. Il valore di
questo secret viene montato come variabile d'ambiente (DREMIO\_PAT) nel
pod. Il file profiles.yml all'interno del container sarà configurato per
leggere questa variabile d'ambiente tramite {{ env\_var('DREMIO\_PAT')
}}, evitando di hardcodare segreti nell'immagine Docker.<sup>60</sup>

#### **5.3.2. Orchestrazione Avanzata con Airflow o Argo Workflows**

Per pipeline complesse con dipendenze che vanno oltre dbt (es. attendere
il completamento di un job di ingestione prima di eseguire dbt), sono
necessari strumenti più potenti.

- **Airflow:** È l'orchestratore de facto nel mondo dei dati. Quando
  eseguito su Kubernetes, la best practice è usare il
  KubernetesPodOperator. Ogni task in un DAG di Airflow può lanciare un
  pod Kubernetes separato per eseguire un comando dbt specifico (es. dbt
  seed, dbt run, dbt test). Questo approccio garantisce un isolamento
  completo delle dipendenze e una gestione granulare delle risorse per
  ogni passo della pipeline.<sup>58</sup>

- **Argo Workflows:** È un motore di workflow nativo di Kubernetes,
  un'alternativa potente ad Airflow per i team profondamente integrati
  nell'ecosistema Kubernetes. Una pipeline dbt può essere definita come
  un Workflow CRD (Custom Resource Definition), dove ogni passo del DAG
  esegue il container dbt con comandi diversi. Argo è particolarmente
  forte nella gestione di DAG dinamici e parallelismo su larga
  scala.<sup>62</sup>

La tabella seguente offre un quadro comparativo per aiutare nella scelta
della giusta strategia di orchestrazione su Kubernetes.

**Tabella 4: Confronto delle Strategie di Orchestrazione Kubernetes per
dbt**

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr>
<th>Strategia</th>
<th>Semplicità / Costo di Setup</th>
<th>Gestione Dipendenze</th>
<th>Osservabilità</th>
<th>Ideale per</th>
</tr>
<tr>
<th><strong>Kubernetes CronJob</strong></th>
<th>Alta / Basso</th>
<th>Nessuna (job auto-contenuto)</th>
<th>Bassa (log del pod)</th>
<th>Schedulazioni semplici e fisse (es. esecuzioni notturne) senza
dipendenze esterne.</th>
</tr>
<tr>
<th><strong>Airflow su K8s</strong></th>
<th>Bassa / Alto</th>
<th>Ricca (cross-system, DAG-based, sensori)</th>
<th>Alta (UI di Airflow, log, metriche)</th>
<th>Pipeline complesse che orchestrano dbt insieme ad altri sistemi
(ingestione, reverse ETL, ML).</th>
</tr>
<tr>
<th><strong>Argo Workflows</strong></th>
<th>Media / Medio</th>
<th>Ricca (nativa di K8s, DAG-based, gestione artefatti)</th>
<th>Alta (UI di Argo, eventi K8s, metriche)</th>
<th>Team con forte expertise Kubernetes che necessitano di
un'orchestrazione nativa e scalabile per pipeline di dati e CI/CD.</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

Fonti: <sup>59</sup>

### **5.4. Implementazione di una Pipeline CI/CD per dbt su Kubernetes (Implementazione di Riferimento)**

Una pipeline di Continuous Integration/Continuous Deployment (CI/CD)
automatizza il processo di test e deploy del progetto dbt. Usando GitHub
Actions come esempio, una pipeline di deploy in produzione potrebbe
essere strutturata come segue <sup>57</sup>:

Un file di workflow di esempio, .github/workflows/deploy.yml:

> YAML

name: Deploy dbt to Production  
  
on:  
push:  
branches:  
- main \# Scatena il workflow al push sul branch main  
  
jobs:  
build-and-deploy:  
runs-on: ubuntu-latest  
steps:  
- name: Checkout code  
uses: actions/checkout@v3  
  
- name: Set up Docker Buildx  
uses: docker/setup-buildx-action@v2  
  
- name: Login to Docker Hub  
uses: docker/login-action@v2  
with:  
username: ${{ secrets.DOCKERHUB\_USERNAME }}  
password: ${{ secrets.DOCKERHUB\_TOKEN }}  
  
- name: Build and push dbt image  
uses: docker/build-push-action@v4  
with:  
context:.  
push: true  
tags: my-docker-repo/mio-progetto-dbt:latest  
  
- name: Set up Kubeconfig  
uses: azure/k8s-set-context@v3  
with:  
method: kubeconfig  
kubeconfig: ${{ secrets.KUBECONFIG }} \# Secret contenente la
configurazione del cluster  
  
- name: Deploy to Kubernetes  
run: |  
kubectl apply -f path/to/your/cronjob.yaml

Questo workflow, al merge su main, costruisce l'immagine Docker
aggiornata, la pusha in un registry e applica il manifest del CronJob al
cluster Kubernetes, aggiornando così il job di produzione con l'ultima
versione del codice.

## **6. Bibliografia e Sitografia**

Questa sezione fornisce un elenco completo e organizzato delle fonti
consultate per la stesura di questo report, permettendo un ulteriore
approfondimento.

### **Documentazione Ufficiale dbt Labs**

- dbt Docs: Introduction -
  [<u>https://docs.getdbt.com/docs/introduction</u>](https://docs.getdbt.com/docs/introduction)
  <sup>4</sup>

- dbt Docs: What is dbt? -
  [<u>https://www.getdbt.com/product/what-is-dbt</u>](https://www.getdbt.com/product/what-is-dbt)
  <sup>5</sup>

- dbt Docs: Manual Install Guide -
  [<u>https://docs.getdbt.com/guides/manual-install</u>](https://docs.getdbt.com/guides/manual-install)
  <sup>10</sup>

- dbt Docs: About dbt Projects -
  [<u>https://docs.getdbt.com/docs/build/projects</u>](https://docs.getdbt.com/docs/build/projects)
  <sup>21</sup>

- dbt Docs: Installation Overview -
  [<u>https://docs.getdbt.com/docs/core/installation-overview</u>](https://docs.getdbt.com/docs/core/installation-overview)
  <sup>8</sup>

- dbt Docs: pip Install -
  [<u>https://docs.getdbt.com/docs/core/pip-install</u>](https://docs.getdbt.com/docs/core/pip-install)
  <sup>12</sup>

- dbt Docs: init Command -
  [<u>https://docs.getdbt.com/reference/commands/init</u>](https://docs.getdbt.com/reference/commands/init)
  <sup>19</sup>

- dbt Docs: Best Practice Guides -
  [<u>https://docs.getdbt.com/best-practices</u>](https://docs.getdbt.com/best-practices)
  <sup>65</sup>

- dbt Docs: Best Practice Workflows -
  [<u>https://docs.getdbt.com/best-practices/best-practice-workflows</u>](https://docs.getdbt.com/best-practices/best-practice-workflows)
  <sup>43</sup>

- dbt Docs: How we structure our dbt projects -
  [<u>https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview</u>](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)
  <sup>49</sup>

- dbt Docs: How we style our dbt models -
  [<u>https://docs.getdbt.com/best-practices/how-we-style/1-how-we-style-our-dbt-models</u>](https://docs.getdbt.com/best-practices/how-we-style/1-how-we-style-our-dbt-models)
  <sup>52</sup>

- dbt Docs: Git Branching Strategies -
  [<u>https://docs.getdbt.com/blog/git-branching-strategies-with-dbt</u>](https://docs.getdbt.com/blog/git-branching-strategies-with-dbt)
  <sup>45</sup>

- dbt Docs: Deployments -
  [<u>https://docs.getdbt.com/docs/deploy/deployments</u>](https://docs.getdbt.com/docs/deploy/deployments)
  <sup>66</sup>

- dbt Docs: Deployment Environments -
  [<u>https://docs.getdbt.com/docs/deploy/deploy-environments</u>](https://docs.getdbt.com/docs/deploy/deploy-environments)
  <sup>67</sup>

- dbt Docs: dbt Cloud Features -
  [<u>https://docs.getdbt.com/docs/cloud/about-cloud/dbt-cloud-features</u>](https://docs.getdbt.com/docs/cloud/about-cloud/dbt-cloud-features)
  <sup>9</sup>

- dbt Docs: Cloud CLI Installation -
  [<u>https://docs.getdbt.com/docs/cloud/cloud-cli-installation</u>](https://docs.getdbt.com/docs/cloud/cloud-cli-installation)
  <sup>14</sup>

### **Documentazione Adattatori e Piattaforme Dati**

- **Apache Iceberg:**

  - Apache Iceberg Support -
    [<u>https://docs.getdbt.com/docs/mesh/iceberg/apache-iceberg-support</u>](https://docs.getdbt.com/docs/mesh/iceberg/apache-iceberg-support)
    <sup>30</sup>

  - Snowflake Iceberg Support -
    [<u>https://docs.getdbt.com/docs/mesh/iceberg/snowflake-iceberg-support</u>](https://docs.getdbt.com/docs/mesh/iceberg/snowflake-iceberg-support)
    <sup>33</sup>

  - Blog: Iceberg is an Implementation Detail -
    [<u>https://www.getdbt.com/blog/icebeg-is-an-implementation-detail</u>](https://www.getdbt.com/blog/icebeg-is-an-implementation-detail)
    <sup>32</sup>

  - Blog: Iceberg, Give it a REST -
    [<u>https://www.getdbt.com/blog/iceberg-give-it-a-rest</u>](https://www.getdbt.com/blog/iceberg-give-it-a-rest)
    <sup>34</sup>

- **Dremio:**

  - dbt Docs: Dremio Setup -
    [<u>https://docs.getdbt.com/docs/core/connect-data-platform/dremio-setup</u>](https://docs.getdbt.com/docs/core/connect-data-platform/dremio-setup)
    <sup>17</sup>

  - Dremio Docs: dbt Connector -
    [<u>https://docs.dremio.com/cloud/sonar/client-apps/dbt/</u>](https://docs.dremio.com/cloud/sonar/client-apps/dbt/)
    <sup>36</sup>

  - dbt Docs: Build Dremio Lakehouse Guide -
    [<u>https://docs.getdbt.com/guides/build-dremio-lakehouse</u>](https://docs.getdbt.com/guides/build-dremio-lakehouse)
    <sup>35</sup>

  - PyPI: dbt-dremio -
    [<u>https://pypi.org/project/dbt-dremio/</u>](https://pypi.org/project/dbt-dremio/)
    <sup>68</sup>

  - GitHub: dbt-dremio Walkthrough -
    [<u>https://github.com/dremio/dbt-dremio/blob/main/docs/walkthrough.md</u>](https://github.com/dremio/dbt-dremio/blob/main/docs/walkthrough.md)
    <sup>37</sup>

- **DuckDB:**

  - dbt Docs: DuckDB Setup -
    [<u>https://docs.getdbt.com/docs/core/connect-data-platform/duckdb-setup</u>](https://docs.getdbt.com/docs/core/connect-data-platform/duckdb-setup)
    <sup>18</sup>

  - dbt Docs: DuckDB Configs -
    [<u>https://docs.getdbt.com/reference/resource-configs/duckdb-configs</u>](https://docs.getdbt.com/reference/resource-configs/duckdb-configs)
    <sup>41</sup>

  - dbt Docs: DuckDB Quickstart -
    [<u>https://docs.getdbt.com/guides/duckdb</u>](https://docs.getdbt.com/guides/duckdb)
    <sup>11</sup>

  - MotherDuck Docs: dbt Integration -
    [<u>https://motherduck.com/docs/integrations/transformation/dbt/</u>](https://motherduck.com/docs/integrations/transformation/dbt/)
    <sup>40</sup>

  - GitHub: dbt-duckdb -
    [<u>https://github.com/duckdb/dbt-duckdb</u>](https://github.com/duckdb/dbt-duckdb)
    <sup>38</sup>

  - PyPI: dbt-duckdb -
    [<u>https://pypi.org/project/dbt-duckdb/1.3.3/</u>](https://pypi.org/project/dbt-duckdb/1.3.3/)
    <sup>39</sup>

- **Databricks/Lakehouse:**

  - Databricks Glossary: Medallion Architecture -
    [<u>https://www.databricks.com/glossary/medallion-architecture</u>](https://www.databricks.com/glossary/medallion-architecture)
    <sup>23</sup>

  - Databricks Resources: dbt Cloud and the Lakehouse -
    [<u>https://www.databricks.com/resources/demos/videos/partner/dbt-cloud-and-the-lakehouse</u>](https://www.databricks.com/resources/demos/videos/partner/dbt-cloud-and-the-lakehouse)
    <sup>69</sup>

  - Databricks Page: dbt with Databricks -
    [<u>https://pages.databricks.com/databricks-dbt-lakehouse-apj</u>](https://pages.databricks.com/databricks-dbt-lakehouse-apj)
    <sup>70</sup>

- **Snowflake:**

  - Snowflake Docs: Create dbt Project -
    [<u>https://docs.snowflake.com/en/sql-reference/sql/create-dbt-project</u>](https://docs.snowflake.com/en/sql-reference/sql/create-dbt-project)
    <sup>71</sup>

### **Guide e Tutorial della Community**

- **Installazione e Progetti:**

  - Devblog.it: Mastering dbt Core -
    [<u>https://devblogit.com/mastering-dbt-core-a-step-by-step-installation-guide</u>](https://devblogit.com/mastering-dbt-core-a-step-by-step-installation-guide)
    <sup>13</sup>

  - GetOrchestra.io: dbt Install Guide -
    [<u>https://www.getorchestra.io/guides/data-build-tool-install-a-comprehensive-guide</u>](https://www.getorchestra.io/guides/data-build-tool-install-a-comprehensive-guide)
    <sup>16</sup>

  - PopSQL: dbt init Command -
    [<u>https://popsql.com/learn-dbt/dbt-init</u>](https://popsql.com/learn-dbt/dbt-init)
    <sup>22</sup>

  - Medium: Building a dbt project from scratch -
    [<u>https://medium.com/refined-and-refactored/building-a-dbt-project-from-scratch-3789e937f15a</u>](https://medium.com/refined-and-refactored/building-a-dbt-project-from-scratch-3789e937f15a)
    <sup>15</sup>

- **Best Practice:**

  - Medium: Best Practices for Workflows -
    [<u>https://medium.com/@turkelturk/best-practices-for-workflows-a-guide-to-effective-dbt-use-fa925127647c</u>](https://medium.com/@turkelturk/best-practices-for-workflows-a-guide-to-effective-dbt-use-fa925127647c)
    <sup>47</sup>

  - B-EYE: Mastering dbt Best Practices -
    [<u>https://b-eye.com/blog/dbt-best-practices-efficient-data-workflows/</u>](https://b-eye.com/blog/dbt-best-practices-efficient-data-workflows/)
    <sup>42</sup>

  - Datafold: 7 dbt Testing Best Practices -
    [<u>https://www.datafold.com/blog/7-dbt-testing-best-practices</u>](https://www.datafold.com/blog/7-dbt-testing-best-practices)
    <sup>55</sup>

  - Medium: Setting up a dbt project -
    [<u>https://medium.com/@massimocapobianco/setting-up-a-dbt-project-a-short-guide-on-best-practices-and-lesser-known-features-8acb8148ed37</u>](https://medium.com/@massimocapobianco/setting-up-a-dbt-project-a-short-guide-on-best-practices-and-lesser-known-features-8acb8148ed37)
    <sup>50</sup>

  - The Data School: Organising a dbt Project -
    [<u>https://www.thedataschool.co.uk/curtis-paterson/organising-a-dbt-project-best-practices</u>](https://www.thedataschool.co.uk/curtis-paterson/organising-a-dbt-project-best-practices)
    <sup>48</sup>

  - Enable Data Union: dbt Style Guide -
    [<u>https://enabledataunion.org/docs/manage\_extend/guides/dbt-style-guide/</u>](https://enabledataunion.org/docs/manage_extend/guides/dbt-style-guide/)
    <sup>53</sup>

  - Airbyte: Best Practices for dbt Style Guide -
    [<u>https://airbyte.com/blog/best-practices-dbt-style-guide</u>](https://airbyte.com/blog/best-practices-dbt-style-guide)
    <sup>51</sup>

- **Deploy e Produzione:**

  - GitHub: dbt CI/CD on GKE -
    [<u>https://github.com/velascoluis/dbt-ci-cd-gke</u>](https://github.com/velascoluis/dbt-ci-cd-gke)
    <sup>57</sup>

  - GitHub: dbt Kubernetes CronJob Example -
    [<u>https://github.com/davidgasquez/kubedbt/blob/master/dbt-cronjob.yaml</u>](https://github.com/davidgasquez/kubedbt/blob/master/dbt-cronjob.yaml)
    <sup>60</sup>

  - Secoda: Mastering dbt Deployment -
    [<u>https://www.secoda.co/learn/mastering-dbt-deployment-best-practices-and-strategies-for-different-environments</u>](https://www.secoda.co/learn/mastering-dbt-deployment-best-practices-and-strategies-for-different-environments)
    <sup>72</sup>

  - Datacoves: Options for Deploying dbt -
    [<u>https://datacoves.com/post/dbt-deployment</u>](https://datacoves.com/post/dbt-deployment)
    <sup>61</sup>

  - Secoda: Version Control Basics for dbt -
    [<u>https://www.secoda.co/learn/version-control-basics-for-dbt-data-teams</u>](https://www.secoda.co/learn/version-control-basics-for-dbt-data-teams)
    <sup>44</sup>

- **Integrazioni Avanzate (Lakehouse, Parquet, Iceberg):**

  - Medium: dbt-DuckDB for Ingestion to Parquet on S3 -
    [<u>https://medium.com/@caiocvelasco/leveraging-dbt-duckdb-to-perform-an-ingestion-step-reading-from-postgres-converting-to-parquet-f8cd5b5fbf3a</u>](https://medium.com/@caiocvelasco/leveraging-dbt-duckdb-to-perform-an-ingestion-step-reading-from-postgres-converting-to-parquet-f8cd5b5fbf3a)
    <sup>3</sup>

  - Medium: Analytics Engineering on the Lakehouse using dbt &
    Databricks -
    [<u>https://anujsen02.medium.com/analytics-engineering-on-the-lakehouse-using-dbt-databricks-part-1-c4d773731ffe</u>](https://anujsen02.medium.com/analytics-engineering-on-the-lakehouse-using-dbt-databricks-part-1-c4d773731ffe)
    <sup>73</sup>

  - Medium: Optimal dbt on Lakehouse Design Patterns -
    [<u>https://medium.com/dbsql-sme-engineering/optimal-dbt-on-lakehouse-design-patterns-11efe702f509</u>](https://medium.com/dbsql-sme-engineering/optimal-dbt-on-lakehouse-design-patterns-11efe702f509)
    <sup>74</sup>

  - Ministry of Justice Blog: Building a Transaction Data Lake using
    Athena, Iceberg, and dbt -
    [<u>https://ministryofjustice.github.io/data-and-analytics-engineering/blog/posts/building-a-transaction-data-lake-using-amazon-athena-apache-iceberg-and-dbt/</u>](https://ministryofjustice.github.io/data-and-analytics-engineering/blog/posts/building-a-transaction-data-lake-using-amazon-athena-apache-iceberg-and-dbt/)
    <sup>31</sup>

  - YouTube: Create an Open Data Lakehouse with Dremio & dbt Labs -
    [<u>https://www.youtube.com/watch?v=9XtFz5QfnaA</u>](https://www.youtube.com/watch?v=9XtFz5QfnaA)
    <sup>75</sup>

- **Orchestrazione (Airflow, Argo):**

  - dbt Docs: Airflow and dbt Cloud Guide -
    [<u>https://docs.getdbt.com/guides/airflow-and-dbt-cloud</u>](https://docs.getdbt.com/guides/airflow-and-dbt-cloud)
    <sup>76</sup>

  - Astronomer: Combining Apache Airflow and dbt Core -
    [<u>https://www.astronomer.io/blog/airflow-and-dbt/</u>](https://www.astronomer.io/blog/airflow-and-dbt/)
    <sup>59</sup>

  - Pipekit: Orchestrating ELT with Argo Workflows and dbt -
    [<u>https://pipekit.io/blog/orchestrating-elt-with-argo-workflows-and-dbt</u>](https://pipekit.io/blog/orchestrating-elt-with-argo-workflows-and-dbt)
    <sup>62</sup>

  - Devtron: What is Argo Workflows? -
    [<u>https://devtron.ai/blog/argo-workflows/</u>](https://devtron.ai/blog/argo-workflows/)
    <sup>63</sup>

### **Forum e Discussioni della Community**

- dbt Community Forum:
  [<u>https://discourse.getdbt.com/</u>](https://discourse.getdbt.com/)

  - Writing Parquet files to S3 from dbt-spark -
    [<u>https://discourse.getdbt.com/t/is-there-a-way-to-write-only-parquet-files-aws-s3-from-dbt-spark-without-materializing-a-table-or-view/18305</u>](https://discourse.getdbt.com/t/is-there-a-way-to-write-only-parquet-files-aws-s3-from-dbt-spark-without-materializing-a-table-or-view/18305)
    <sup>26</sup>

  - dbt pipeline with parquet files -
    [<u>https://discourse.getdbt.com/t/dbt-pipeline-with-parquet-files/7928</u>](https://discourse.getdbt.com/t/dbt-pipeline-with-parquet-files/7928)
    <sup>27</sup>

  - dbt with Parquet in S3 via Trino -
    [<u>https://discourse.getdbt.com/t/question-on-using-dbt-with-parquet-in-s3-via-trino/5098</u>](https://discourse.getdbt.com/t/question-on-using-dbt-with-parquet-in-s3-via-trino/5098)
    <sup>28</sup>

  - Best Practices for Staging Models -
    [<u>https://discourse.getdbt.com/t/best-practices-for-managing-staging-models-in-large-scale-dbt-projects/19661</u>](https://discourse.getdbt.com/t/best-practices-for-managing-staging-models-in-large-scale-dbt-projects/19661)
    <sup>77</sup>

- Stack Overflow: dbt pipeline with parquet files -
  [<u>https://stackoverflow.com/questions/76064115/dbt-pipeline-with-parquet-files</u>](https://stackoverflow.com/questions/76064115/dbt-pipeline-with-parquet-files)
  <sup>29</sup>

- Reddit r/dataengineering:

  - Organizing dbt projects -
    [<u>https://www.reddit.com/r/dataengineering/comments/1hw9c0o/how\_should\_we\_organize\_our\_dbt\_projects\_with/</u>](https://www.reddit.com/r/dataengineering/comments/1hw9c0o/how_should_we_organize_our_dbt_projects_with/)
    <sup>78</sup>

  - dbt Layer Naming Conventions -
    [<u>https://www.reddit.com/r/dataengineering/comments/16bulr0/dbt\_layer\_naming\_conventions/</u>](https://www.reddit.com/r/dataengineering/comments/16bulr0/dbt_layer_naming_conventions/)
    <sup>79</sup>

  - Git branching strategy for Snowflake and dbt -
    [<u>https://www.reddit.com/r/dataengineering/comments/1g5w4y5/git\_branching\_strategy\_for\_snowflake\_and\_dbt/</u>](https://www.reddit.com/r/dataengineering/comments/1g5w4y5/git_branching_strategy_for_snowflake_and_dbt/)
    <sup>80</sup>

### **Fonti Generali**

- Wikipedia: Data build tool
  -(https://en.wikipedia.org/wiki/Data\_build\_tool) <sup>1</sup>

- Analytics8: dbt Overview -
  [<u>https://www.analytics8.com/blog/dbt-overview-what-is-dbt-and-what-can-it-do-for-my-data-pipeline/</u>](https://www.analytics8.com/blog/dbt-overview-what-is-dbt-and-what-can-it-do-for-my-data-pipeline/)
  <sup>7</sup>

- YouTube: What is dbt? (The Seattle Data Guy) -
  [<u>https://www.youtube.com/watch?v=8FZZivIfJVo</u>](https://www.youtube.com/watch?v=8FZZivIfJVo)
  <sup>81</sup>

- GetIndata Blog: Introduction to dbt Cloud -
  [<u>https://getindata.com/blog/introduction-dbt-cloud-features-capabilities-limitations/</u>](https://getindata.com/blog/introduction-dbt-cloud-features-capabilities-limitations/)
  <sup>2</sup>

#### Bibliografia

1.  en.wikipedia.org, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://en.wikipedia.org/wiki/Data\_build\_tool</u>](https://en.wikipedia.org/wiki/Data_build_tool)

2.  Introduction to dbt Cloud - features, capabilities and limitations -
    GetInData, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://getindata.com/blog/introduction-dbt-cloud-features-capabilities-limitations/</u>](https://getindata.com/blog/introduction-dbt-cloud-features-capabilities-limitations/)

3.  Leveraging dbt-DuckDB to perform an Ingestion Step (Reading from
    Postgres, converting to Parquet, and saving them into an S3 Bucket).
    | by Caio Velasco | Medium, accesso eseguito il giorno giugno 30,
    2025,
    [<u>https://medium.com/@caiocvelasco/leveraging-dbt-duckdb-to-perform-an-ingestion-step-reading-from-postgres-converting-to-parquet-f8cd5b5fbf3a</u>](https://medium.com/@caiocvelasco/leveraging-dbt-duckdb-to-perform-an-ingestion-step-reading-from-postgres-converting-to-parquet-f8cd5b5fbf3a)

4.  What is dbt? | dbt Developer Hub - dbt Docs - dbt Labs, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/docs/introduction</u>](https://docs.getdbt.com/docs/introduction)

5.  What is dbt? | dbt Labs, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://www.getdbt.com/product/what-is-dbt</u>](https://www.getdbt.com/product/what-is-dbt)

6.  7 Reasons To Choose dbt For Your Analytics Stack | Archetype
    Consulting, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://archetypeconsulting.com/blog/7-reasons-to-choose-dbt-for-your-analytics-stack</u>](https://archetypeconsulting.com/blog/7-reasons-to-choose-dbt-for-your-analytics-stack)

7.  dbt (Data Build Tool) Overview: What is dbt and What Can It Do for
    My Data Pipeline?, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://www.analytics8.com/blog/dbt-overview-what-is-dbt-and-what-can-it-do-for-my-data-pipeline/</u>](https://www.analytics8.com/blog/dbt-overview-what-is-dbt-and-what-can-it-do-for-my-data-pipeline/)

8.  About dbt Core and installation | dbt Developer Hub - dbt Docs,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/docs/core/installation-overview</u>](https://docs.getdbt.com/docs/core/installation-overview)

9.  The dbt platform features | dbt Developer Hub - dbt Docs, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/docs/cloud/about-cloud/dbt-cloud-features</u>](https://docs.getdbt.com/docs/cloud/about-cloud/dbt-cloud-features)

10. Quickstart for dbt Core from a manual install | dbt Developer Hub,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/guides/manual-install</u>](https://docs.getdbt.com/guides/manual-install)

11. Quickstart for dbt Core using DuckDB | dbt Developer Hub - dbt Docs,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/guides/duckdb</u>](https://docs.getdbt.com/guides/duckdb)

12. Install with pip | dbt Developer Hub, accesso eseguito il giorno
    giugno 30, 2025,
    [<u>https://docs.getdbt.com/docs/core/pip-install</u>](https://docs.getdbt.com/docs/core/pip-install)

13. Mastering dbt: Your Complete Step-by-Step Handbook 2025 - DevBlogIt,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://devblogit.com/mastering-dbt-core-a-step-by-step-installation-guide</u>](https://devblogit.com/mastering-dbt-core-a-step-by-step-installation-guide)

14. Install dbt CLI | dbt Developer Hub - dbt Docs, accesso eseguito il
    giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/docs/cloud/cloud-cli-installation</u>](https://docs.getdbt.com/docs/cloud/cloud-cli-installation)

15. Building a dbt project from scratch | by Alice Bui | Joon Solutions
    Global - Medium, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://medium.com/refined-and-refactored/building-a-dbt-project-from-scratch-3789e937f15a</u>](https://medium.com/refined-and-refactored/building-a-dbt-project-from-scratch-3789e937f15a)

16. Comprehensive Guide to Installing a Data Build Tool (dbt) -
    Orchestra, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://www.getorchestra.io/guides/data-build-tool-install-a-comprehensive-guide</u>](https://www.getorchestra.io/guides/data-build-tool-install-a-comprehensive-guide)

17. Dremio setup | dbt Developer Hub - dbt Docs - dbt Labs, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/docs/core/connect-data-platform/dremio-setup</u>](https://docs.getdbt.com/docs/core/connect-data-platform/dremio-setup)

18. DuckDB setup | dbt Developer Hub - dbt Docs - dbt Labs, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/docs/core/connect-data-platform/duckdb-setup</u>](https://docs.getdbt.com/docs/core/connect-data-platform/duckdb-setup)

19. About dbt init command | dbt Developer Hub - dbt Docs, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/reference/commands/init</u>](https://docs.getdbt.com/reference/commands/init)

20. 1\. Create a new dbt project - Conveyor docs, accesso eseguito il
    giorno giugno 30, 2025,
    [<u>https://docs.conveyordata.com/get-started/dbt/create-a-new-dbt-project</u>](https://docs.conveyordata.com/get-started/dbt/create-a-new-dbt-project)

21. About dbt projects | dbt Developer Hub - dbt Docs - dbt Labs,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/docs/build/projects</u>](https://docs.getdbt.com/docs/build/projects)

22. dbt init Command: Creating a New dbt Project - PopSQL, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://popsql.com/learn-dbt/dbt-init</u>](https://popsql.com/learn-dbt/dbt-init)

23. What is a Medallion Architecture? - Databricks, accesso eseguito il
    giorno giugno 30, 2025,
    [<u>https://www.databricks.com/glossary/medallion-architecture</u>](https://www.databricks.com/glossary/medallion-architecture)

24. From Fabric to Fantastic: How dbt Makes Your Lakehouses and
    Warehouses Shine, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://www.youtube.com/watch?v=ciiGvAZnPeo</u>](https://www.youtube.com/watch?v=ciiGvAZnPeo)

25. Create Parquet files in object storage - Teradata Developers Portal,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://developers.teradata.com/de/quickstarts/manage-data/create-parquet-files-in-object-storage/</u>](https://developers.teradata.com/de/quickstarts/manage-data/create-parquet-files-in-object-storage/)

26. Is there a way to write only parquet files AWS S3 from dbt-spark
    ..., accesso eseguito il giorno giugno 30, 2025,
    [<u>https://discourse.getdbt.com/t/is-there-a-way-to-write-only-parquet-files-aws-s3-from-dbt-spark-without-materializing-a-table-or-view/18305</u>](https://discourse.getdbt.com/t/is-there-a-way-to-write-only-parquet-files-aws-s3-from-dbt-spark-without-materializing-a-table-or-view/18305)

27. dbt pipeline with parquet files - Help, accesso eseguito il giorno
    giugno 30, 2025,
    [<u>https://discourse.getdbt.com/t/dbt-pipeline-with-parquet-files/7928</u>](https://discourse.getdbt.com/t/dbt-pipeline-with-parquet-files/7928)

28. Question on using DBT with Parquet in S3 via Trino? - In-Depth
    Discussions, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://discourse.getdbt.com/t/question-on-using-dbt-with-parquet-in-s3-via-trino/5098</u>](https://discourse.getdbt.com/t/question-on-using-dbt-with-parquet-in-s3-via-trino/5098)

29. dbt pipeline with parquet files - amazon s3 - Stack Overflow,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://stackoverflow.com/questions/76064115/dbt-pipeline-with-parquet-files</u>](https://stackoverflow.com/questions/76064115/dbt-pipeline-with-parquet-files)

30. Apache Iceberg Support | dbt Developer Hub, accesso eseguito il
    giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/docs/mesh/iceberg/apache-iceberg-support</u>](https://docs.getdbt.com/docs/mesh/iceberg/apache-iceberg-support)

31. Building a transaction data lake using Amazon Athena, Apache Iceberg
    and dbt, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://ministryofjustice.github.io/data-and-analytics-engineering/blog/posts/building-a-transaction-data-lake-using-amazon-athena-apache-iceberg-and-dbt/</u>](https://ministryofjustice.github.io/data-and-analytics-engineering/blog/posts/building-a-transaction-data-lake-using-amazon-athena-apache-iceberg-and-dbt/)

32. Iceberg Is An Implementation Detail | dbt Developer Blog, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/blog/icebeg-is-an-implementation-detail</u>](https://docs.getdbt.com/blog/icebeg-is-an-implementation-detail)

33. Snowflake and Apache Iceberg | dbt Developer Hub - dbt Docs, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/docs/mesh/iceberg/snowflake-iceberg-support</u>](https://docs.getdbt.com/docs/mesh/iceberg/snowflake-iceberg-support)

34. Iceberg?? Give it a REST - dbt Labs, accesso eseguito il giorno
    giugno 30, 2025,
    [<u>https://www.getdbt.com/blog/iceberg-give-it-a-rest</u>](https://www.getdbt.com/blog/iceberg-give-it-a-rest)

35. Build a data lakehouse with dbt Core and Dremio Cloud | dbt
    Developer Hub - dbt Docs, accesso eseguito il giorno giugno 30,
    2025,
    [<u>https://docs.getdbt.com/guides/build-dremio-lakehouse</u>](https://docs.getdbt.com/guides/build-dremio-lakehouse)

36. dbt - Dremio Documentation, accesso eseguito il giorno giugno 30,
    2025,
    [<u>https://docs.dremio.com/cloud/sonar/client-apps/dbt/</u>](https://docs.dremio.com/cloud/sonar/client-apps/dbt/)

37. dbt-dremio/docs/walkthrough.md at main · dremio/dbt-dremio · GitHub,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://github.com/dremio/dbt-dremio/blob/main/docs/walkthrough.md</u>](https://github.com/dremio/dbt-dremio/blob/main/docs/walkthrough.md)

38. duckdb/dbt-duckdb: dbt (http://getdbt.com) adapter for DuckDB
    (http://duckdb.org) - GitHub, accesso eseguito il giorno giugno 30,
    2025,
    [<u>https://github.com/duckdb/dbt-duckdb</u>](https://github.com/duckdb/dbt-duckdb)

39. dbt-duckdb - PyPI, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://pypi.org/project/dbt-duckdb/1.3.3/</u>](https://pypi.org/project/dbt-duckdb/1.3.3/)

40. dbt with DuckDB and MotherDuck | MotherDuck Docs, accesso eseguito
    il giorno giugno 30, 2025,
    [<u>https://motherduck.com/docs/integrations/transformation/dbt/</u>](https://motherduck.com/docs/integrations/transformation/dbt/)

41. DuckDB configurations | dbt Developer Hub, accesso eseguito il
    giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/reference/resource-configs/duckdb-configs</u>](https://docs.getdbt.com/reference/resource-configs/duckdb-configs)

42. Mastering dbt: Best Practices for Efficient Data Workflows - B EYE,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://b-eye.com/blog/dbt-best-practices-efficient-data-workflows/</u>](https://b-eye.com/blog/dbt-best-practices-efficient-data-workflows/)

43. Best practices for workflows | dbt Developer Hub, accesso eseguito
    il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/best-practices/best-practice-workflows</u>](https://docs.getdbt.com/best-practices/best-practice-workflows)

44. Understanding the Role of Version Control Systems in dbt Data ...,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://www.secoda.co/learn/version-control-basics-for-dbt-data-teams</u>](https://www.secoda.co/learn/version-control-basics-for-dbt-data-teams)

45. Getting Started with git Branching Strategies and dbt | dbt
    Developer Blog - dbt Docs, accesso eseguito il giorno giugno 30,
    2025,
    [<u>https://docs.getdbt.com/blog/git-branching-strategies-with-dbt</u>](https://docs.getdbt.com/blog/git-branching-strategies-with-dbt)

46. The simplest Git branching flow for dbt Cloud - DEV Community,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://dev.to/panasenco/simplest-git-branching-dbt-cloud-44p1</u>](https://dev.to/panasenco/simplest-git-branching-dbt-cloud-44p1)

47. Best Practices for Workflows: A Guide to Effective dbt Use | by
    Turkel - Medium, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://medium.com/@turkelturk/best-practices-for-workflows-a-guide-to-effective-dbt-use-fa925127647c</u>](https://medium.com/@turkelturk/best-practices-for-workflows-a-guide-to-effective-dbt-use-fa925127647c)

48. Organising a dbt Project: Best Practices - The Data School, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://www.thedataschool.co.uk/curtis-paterson/organising-a-dbt-project-best-practices</u>](https://www.thedataschool.co.uk/curtis-paterson/organising-a-dbt-project-best-practices)

49. How we structure our dbt projects | dbt Developer Hub - dbt Docs,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview</u>](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)

50. Setting up a dbt project: A short guide on best practices and
    lesser-known features - Medium, accesso eseguito il giorno giugno
    30, 2025,
    [<u>https://medium.com/@massimocapobianco/setting-up-a-dbt-project-a-short-guide-on-best-practices-and-lesser-known-features-8acb8148ed37</u>](https://medium.com/@massimocapobianco/setting-up-a-dbt-project-a-short-guide-on-best-practices-and-lesser-known-features-8acb8148ed37)

51. Best Practices for dbt Style Guide: Optimal Usage - Airbyte, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://airbyte.com/blog/best-practices-dbt-style-guide</u>](https://airbyte.com/blog/best-practices-dbt-style-guide)

52. How we style our dbt models | dbt Developer Hub - dbt Docs - dbt
    Labs, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/best-practices/how-we-style/1-how-we-style-our-dbt-models</u>](https://docs.getdbt.com/best-practices/how-we-style/1-how-we-style-our-dbt-models)

53. dbt Style Guide - enable data union, accesso eseguito il giorno
    giugno 30, 2025,
    [<u>https://enabledataunion.org/docs/manage\_extend/guides/dbt-style-guide/</u>](https://enabledataunion.org/docs/manage_extend/guides/dbt-style-guide/)

54. Structure - dbt\_project\_evaluator, accesso eseguito il giorno
    giugno 30, 2025,
    [<u>https://dbt-labs.github.io/dbt-project-evaluator/latest/rules/structure/</u>](https://dbt-labs.github.io/dbt-project-evaluator/latest/rules/structure/)

55. 7 dbt Testing Best Practices - Datafold, accesso eseguito il giorno
    giugno 30, 2025,
    [<u>https://www.datafold.com/blog/7-dbt-testing-best-practices</u>](https://www.datafold.com/blog/7-dbt-testing-best-practices)

56. Steps to enhance dbt(data build tool) dev workflow :
    r/dataengineering - Reddit, accesso eseguito il giorno giugno 30,
    2025,
    [<u>https://www.reddit.com/r/dataengineering/comments/1ahwltd/steps\_to\_enhance\_dbtdata\_build\_tool\_dev\_workflow/</u>](https://www.reddit.com/r/dataengineering/comments/1ahwltd/steps_to_enhance_dbtdata_build_tool_dev_workflow/)

57. velascoluis/dbt-ci-cd-gke: CICD pipeline that deploys a dbt ... -
    GitHub, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://github.com/velascoluis/dbt-ci-cd-gke</u>](https://github.com/velascoluis/dbt-ci-cd-gke)

58. A Comprehensive Guide to Airflow on Kubernetes at Scale - Tipalti,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://tipalti.com/blog/comprehensive-guide-to-airflow-on-kubernetes-at-scale/</u>](https://tipalti.com/blog/comprehensive-guide-to-airflow-on-kubernetes-at-scale/)

59. How to Combine Apache Airflow® and dbt Core - Astronomer, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://www.astronomer.io/blog/airflow-and-dbt/</u>](https://www.astronomer.io/blog/airflow-and-dbt/)

60. kubedbt/dbt-cronjob.yaml at master · davidgasquez/kubedbt · GitHub,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://github.com/davidgasquez/kubedbt/blob/master/dbt-cronjob.yaml</u>](https://github.com/davidgasquez/kubedbt/blob/master/dbt-cronjob.yaml)

61. Consider the Options for Deploying dbt - Datacoves, accesso eseguito
    il giorno giugno 30, 2025,
    [<u>https://datacoves.com/post/dbt-deployment</u>](https://datacoves.com/post/dbt-deployment)

62. Orchestrating ELT with Argo Workflows and dbt - Pipekit, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://pipekit.io/blog/orchestrating-elt-with-argo-workflows-and-dbt</u>](https://pipekit.io/blog/orchestrating-elt-with-argo-workflows-and-dbt)

63. What is Argo Workflows? Understanding Its Role in Kubernetes
    Automation - Devtron, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://devtron.ai/blog/argo-workflows/</u>](https://devtron.ai/blog/argo-workflows/)

64. Argo Workflows: The Best Way to Run Kubernetes Workflows - Pipekit,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://pipekit.io/blog/argo-workflows-the-best-way-to-run-kubernetes-workflows</u>](https://pipekit.io/blog/argo-workflows-the-best-way-to-run-kubernetes-workflows)

65. Best practice guides | dbt Developer Hub - dbt Docs - dbt Labs,
    accesso eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/best-practices</u>](https://docs.getdbt.com/best-practices)

66. Deploy dbt | dbt Developer Hub - dbt Docs, accesso eseguito il
    giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/docs/deploy/deployments</u>](https://docs.getdbt.com/docs/deploy/deployments)

67. Deployment environments | dbt Developer Hub - dbt Docs, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/docs/deploy/deploy-environments</u>](https://docs.getdbt.com/docs/deploy/deploy-environments)

68. dbt-dremio - PyPI, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://pypi.org/project/dbt-dremio/</u>](https://pypi.org/project/dbt-dremio/)

69. dbt Cloud and the Lakehouse - Databricks, accesso eseguito il giorno
    giugno 30, 2025,
    [<u>https://www.databricks.com/resources/demos/videos/partner/dbt-cloud-and-the-lakehouse</u>](https://www.databricks.com/resources/demos/videos/partner/dbt-cloud-and-the-lakehouse)

70. Data transformation in the lakehouse made simple with dbt Labs and
    Databricks, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://pages.databricks.com/databricks-dbt-lakehouse-apj</u>](https://pages.databricks.com/databricks-dbt-lakehouse-apj)

71. CREATE DBT PROJECT - Snowflake Documentation, accesso eseguito il
    giorno giugno 30, 2025,
    [<u>https://docs.snowflake.com/en/sql-reference/sql/create-dbt-project</u>](https://docs.snowflake.com/en/sql-reference/sql/create-dbt-project)

72. Mastering dbt Deployment: Best Practices and Strategies for
    Different Environments, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://www.secoda.co/learn/mastering-dbt-deployment-best-practices-and-strategies-for-different-environments</u>](https://www.secoda.co/learn/mastering-dbt-deployment-best-practices-and-strategies-for-different-environments)

73. Analytics Engineering on the Lakehouse using DBT & Databricks
    (part-1 ), accesso eseguito il giorno giugno 30, 2025,
    [<u>https://anujsen02.medium.com/analytics-engineering-on-the-lakehouse-using-dbt-databricks-part-1-c4d773731ffe</u>](https://anujsen02.medium.com/analytics-engineering-on-the-lakehouse-using-dbt-databricks-part-1-c4d773731ffe)

74. DBT on Lakehouse Design Patterns Part 1: Optimized ELT | by
    Databricks SQL SME, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://medium.com/dbsql-sme-engineering/optimal-dbt-on-lakehouse-design-patterns-11efe702f509</u>](https://medium.com/dbsql-sme-engineering/optimal-dbt-on-lakehouse-design-patterns-11efe702f509)

75. Build an Open Lakehouse with dbt Labs and Dremio - YouTube, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://www.youtube.com/watch?v=9XtFz5QfnaA</u>](https://www.youtube.com/watch?v=9XtFz5QfnaA)

76. Airflow and dbt | dbt Developer Hub - dbt Docs, accesso eseguito il
    giorno giugno 30, 2025,
    [<u>https://docs.getdbt.com/guides/airflow-and-dbt-cloud</u>](https://docs.getdbt.com/guides/airflow-and-dbt-cloud)

77. Best Practices for Managing Staging Models in Large-Scale dbt
    Projects ?? - Help, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://discourse.getdbt.com/t/best-practices-for-managing-staging-models-in-large-scale-dbt-projects/19661</u>](https://discourse.getdbt.com/t/best-practices-for-managing-staging-models-in-large-scale-dbt-projects/19661)

78. How should we organize our dbt projects with dbt-core? :
    r/dataengineering - Reddit, accesso eseguito il giorno giugno 30,
    2025,
    [<u>https://www.reddit.com/r/dataengineering/comments/1hw9c0o/how\_should\_we\_organize\_our\_dbt\_projects\_with/</u>](https://www.reddit.com/r/dataengineering/comments/1hw9c0o/how_should_we_organize_our_dbt_projects_with/)

79. dbt Layer Naming Conventions : r/dataengineering - Reddit, accesso
    eseguito il giorno giugno 30, 2025,
    [<u>https://www.reddit.com/r/dataengineering/comments/16bulr0/dbt\_layer\_naming\_conventions/</u>](https://www.reddit.com/r/dataengineering/comments/16bulr0/dbt_layer_naming_conventions/)

80. Git branching strategy for snowflake and dbt : r/dataengineering -
    Reddit, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://www.reddit.com/r/dataengineering/comments/1g5w4y5/git\_branching\_strategy\_for\_snowflake\_and\_dbt/</u>](https://www.reddit.com/r/dataengineering/comments/1g5w4y5/git_branching_strategy_for_snowflake_and_dbt/)

81. What Is DBT and Why Is It So Popular - Intro To Data Infrastructure
    Part 3 - YouTube, accesso eseguito il giorno giugno 30, 2025,
    [<u>https://www.youtube.com/watch?v=8FZZivIfJVo</u>](https://www.youtube.com/watch?v=8FZZivIfJVo)
