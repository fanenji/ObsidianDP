---
type: note
topic: gis
created: 2026-03-18
tags:
  - mapping
  - sedona
---

# **Analisi del Supporto per File di Grigliati di Spostamento (GSB) nella Funzione ST\_Transform di Apache Sedona**

**I. Sommario Esecutivo**

Il presente rapporto analizza la capacità della funzione ST\_Transform
di Apache Sedona di utilizzare direttamente file di grigliati di
spostamento (formato.gsb o equivalenti come NTv2) per trasformazioni di
coordinate ad alta precisione, in particolare quelle che coinvolgono
cambi di datum. L'analisi si basa sulla documentazione ufficiale di
Sedona (versioni recenti fino alla 1.7.1), discussioni della comunità,
issue tracker e l'esame delle librerie sottostanti.

**Risultato Chiave:** Sulla base delle prove disponibili, la funzione
ST\_Transform di Apache Sedona, nelle sue implementazioni per Apache
Spark e Apache Flink, **non supporta direttamente** l'uso di file di
grigliati di spostamento GSB tramite parametri espliciti o stringhe PROJ
che li referenziano. La documentazione ufficiale descrive l'uso di
codici EPSG e, in versioni più recenti, stringhe WKT, ma omette
qualsiasi riferimento a parametri per specificare file di griglia o
trasformazioni basate su griglia come +nadgrids.

**Sintesi delle Prove:** L'assenza di menzioni di GSB, NADGRIDS, NTv2 o
stringhe PROJ complete nella documentazione API di ST\_Transform per le
versioni Spark/Flink <sup>1</sup> è la prova principale. Ricerche nei
canali della comunità (issue GitHub <sup>8</sup>, Stack Overflow
<sup>12</sup>) non hanno rivelato discussioni o richieste relative al
supporto diretto di GSB in ST\_Transform. Sebbene la libreria
sottostante GeoTools, utilizzata da Sedona <sup>14</sup>, possieda la
capacità intrinseca di eseguire trasformazioni basate su griglia
<sup>22</sup>, questa funzionalità non sembra essere esposta tramite
l'interfaccia standard di ST\_Transform in Sedona per Spark/Flink.
Un'eccezione degna di nota è l'applicazione SedonaSnow per Snowflake,
che sembra in grado di gestire trasformazioni basate su griglia
<sup>26</sup>, suggerendo che il motore di trasformazione centrale
potrebbe avere la capacità, ma non è accessibile tramite parametri
standard nelle implementazioni Spark/Flink.

**Raccomandazione Primaria:** In assenza di supporto diretto, gli utenti
che necessitano di trasformazioni basate su GSB all'interno
dell'ecosistema Spark/Sedona devono ricorrere a soluzioni alternative.
Le opzioni più praticabili includono l'uso di User-Defined Functions
(UDF) Spark che incapsulano librerie esterne come pyproj (che a sua
volta utilizza PROJ) o potenzialmente le API Python di GDAL. Queste
soluzioni alternative introducono complessità aggiuntive legate alla
gestione delle dipendenze, alla distribuzione dei file GSB sui nodi
worker e alla potenziale riduzione delle prestazioni dovuta all'overhead
delle UDF. Un'alternativa consiste nell'eseguire le trasformazioni come
passo di pre-elaborazione esterno utilizzando strumenti come ogr2ogr
prima dell'ingestione dei dati in Sedona. La scelta della soluzione
alternativa dipende dai requisiti specifici di performance, dalla
complessità dell'infrastruttura e dalla familiarità del team con le
diverse tecnologie.

**II. Introduzione**

Le trasformazioni di coordinate sono un'operazione fondamentale
nell'analisi di dati geospaziali, consentendo l'integrazione e il
confronto di dati provenienti da diverse fonti con differenti sistemi di
riferimento delle coordinate (CRS). Mentre le trasformazioni tra
proiezioni cartografiche sono relativamente comuni, le trasformazioni
che coinvolgono un cambio di datum geodetico richiedono spesso un
livello di precisione più elevato. I file di grigliati di spostamento
(grid shift files), comunemente nei formati GSB (Grid Shift Binary) o
NTv2 (National Transformation version 2), forniscono correzioni basate
su griglia per modellare accuratamente le distorsioni locali tra datum,
ottenendo così trasformazioni più precise rispetto ai metodi basati su
parametri medi (come le trasformazioni Helmert a 3 o 7 parametri).

Apache Sedona è un sistema di calcolo distribuito ad alte prestazioni
progettato per elaborare dati spaziali su larga scala, estendendo
piattaforme come Apache Spark, Apache Flink e Snowflake.<sup>14</sup>
Offre un ricco set di funzioni SQL spaziali, tra cui ST\_Transform, per
la manipolazione e l'analisi di dati geospaziali distribuiti. Data
l'importanza delle trasformazioni di datum ad alta precisione in molti
domini applicativi (es. catasto, ingegneria civile, monitoraggio
ambientale), sorge la questione se Sedona fornisca meccanismi integrati
per sfruttare i file GSB direttamente all'interno della sua funzione
ST\_Transform.

Questo rapporto indaga sistematicamente la presenza o l'assenza di
supporto diretto per i file GSB nella funzione ST\_Transform di Apache
Sedona. L'analisi si basa su un esame approfondito della documentazione
ufficiale più recente (incluse API, note di rilascio e tutorial), una
ricerca mirata nelle risorse della comunità (forum, issue tracker) e una
valutazione delle capacità delle librerie sottostanti, principalmente
GeoTools. Infine, qualora il supporto diretto risulti assente, verranno
identificate e valutate le soluzioni alternative praticabili all'interno
dell'ecosistema Spark/Sedona. L'obiettivo è fornire una risposta
definitiva e basata su prove concrete, utile a professionisti tecnici
che necessitano di implementare trasformazioni di coordinate basate su
griglia nei loro workflow Sedona.

**III. Analisi di ST\_Transform nella Documentazione di Apache Sedona**

Un'analisi dettagliata della documentazione ufficiale di Apache Sedona
relativa alla funzione ST\_Transform è fondamentale per determinare il
livello di supporto per le trasformazioni basate su griglia GSB.

Firma della Funzione e Parametri Documentati:

Le documentazioni API per le diverse versioni recenti di Sedona (ad
esempio, 1.3.x, 1.4.x, 1.5.x, 1.6.x, 1.7.x) presentano in modo
consistente la funzione ST\_Transform.1 La firma tipica richiede la
geometria di input, un identificatore per il CRS di origine (spesso
dedotto dall'SRID della geometria stessa) e un identificatore per il CRS
di destinazione. I metodi documentati per specificare i CRS sono
principalmente:

1.  Codici EPSG: Stringhe nella forma 'EPSG:xxxx' (es. 'EPSG:4326',
    'EPSG:32649').

2.  Stringhe WKT (Well-Known Text): A partire dalla versione 1.3.0, è
    stato documentato il supporto per specificare i CRS tramite stringhe
    in formato OGC WKT v1.<sup>1</sup>

Assenza di Supporto Esplicito per GSB/NADGRIDS/PROJ:

Un punto cruciale è l'assenza totale, in tutta la documentazione
esaminata per le implementazioni Spark e Flink 1, di qualsiasi menzione
relativa a parametri o sintassi per:

- Specificare percorsi a file GSB.

- Utilizzare direttive +nadgrids all'interno di stringhe PROJ.

- Specificare nomi di trasformazioni NTv2 definite esternamente.

- Passare stringhe PROJ complete che potrebbero contenere riferimenti a
  file di griglia.

Questa omissione è significativa se confrontata con altri sistemi
geospaziali come PostGIS, la cui funzione ST\_Transform supporta
esplicitamente l'uso di stringhe PROJ.4 complete, incluso il parametro
+nadgrids per invocare trasformazioni basate su griglia.<sup>34</sup>

Note sulla Gestione dei CRS:

La documentazione di Sedona mostra attenzione ai dettagli relativi ai
CRS. Ad esempio, le note di rilascio della versione 1.5.0 31 specificano
un cambiamento nel comportamento predefinito per diverse funzioni
(inclusa ST\_Transform), richiedendo che i dati di input siano in ordine
longitudine/latitudine e introducendo la funzione ST\_FlipCoordinates
per gestire eventuali inversioni necessarie.1 Inoltre, l'introduzione di
funzioni come ST\_BestSRID 1 (per determinare un SRID ottimale per una
geometria) e funzioni per calcoli sferoidali (ST\_DistanceSpheroid,
ST\_AreaSpheroid 19) dimostra la consapevolezza degli sviluppatori di
Sedona riguardo a concetti avanzati di CRS e datum. Tuttavia, queste
funzionalità, pur essendo correlate, non implicano direttamente il
supporto per l'uso controllato di file GSB da parte dell'utente
all'interno di ST\_Transform.

Contesto Specifico: Sedona su Snowflake:

Un'informazione rilevante proviene da un articolo della community di
Snowflake.26 L'articolo spiega che la funzione ST\_TRANSFORM nativa di
Snowflake fallisce per trasformazioni che richiedono file di griglia
(viene fornito l'esempio da EPSG:4326 a EPSG:7844). La soluzione
proposta è utilizzare la funzione sedonasnow.sedona.ST\_TRANSFORM
fornita dall'applicazione SedonaSnow Native App, disponibile sul
Marketplace di Snowflake. L'articolo mostra che questa funzione
specifica di Sedona riesce a eseguire la trasformazione. Questo
suggerisce fortemente che il motore di trasformazione sottostante
utilizzato da Sedona (probabilmente basato su GeoTools/PROJ) è in grado
di gestire le trasformazioni basate su griglia, ma che l'interfaccia
della funzione ST\_Transform standard nelle implementazioni Spark/Flink
non espone i parametri necessari affinché l'utente possa specificare e
utilizzare direttamente i file GSB.

In sintesi, l'analisi della documentazione ufficiale porta a concludere
che, nonostante la presenza di funzionalità geodetiche avanzate e un
potenziale supporto nel motore sottostante (come evidenziato dal caso
Snowflake), la funzione ST\_Transform di Sedona per Spark e Flink non è
stata progettata o documentata per accettare parametri diretti per
l'utilizzo di file GSB. L'enfasi è posta sull'uso di codici EPSG e
stringhe WKT.

**IV. Conoscenza della Comunità e Problemi Segnalati**

Oltre alla documentazione ufficiale, l'analisi delle discussioni della
comunità, dei bug report e delle domande degli utenti può fornire
ulteriori indicazioni sul supporto effettivo o sulle problematiche
riscontrate nell'utilizzo di ST\_Transform con file GSB.

Ricerca su GitHub Issues:

Una ricerca negli issue tracker di Apache Sedona su GitHub 8 non ha
rivelato segnalazioni di bug o richieste di funzionalità (feature
request) specifiche riguardanti l'aggiunta del supporto diretto per file
GSB, direttive NADGRIDS o trasformazioni NTv2 all'interno della funzione
ST\_Transform. Gli issue esistenti relativi a ST\_Transform o alle
trasformazioni CRS tendono a concentrarsi su altri aspetti, come la
gestione dell'ordine delle coordinate 31 o la compatibilità con formati
specifici.

Un issue particolarmente pertinente è il \#1397.<sup>10</sup> In questo
issue, un utente chiede se sia possibile specificare un *metodo* di
trasformazione specifico (identificato da un codice EPSG, es. 1612)
quando si trasforma tra due datum (es. da EPSG:4258 a EPSG:4326),
sottolineando come la scelta della trasformazione influenzi
l'accuratezza. La risposta di uno sviluppatore esterno (con esperienza
in Apache SIS, un'altra libreria geospaziale) conferma che Sedona
utilizza GeoTools e che, sebbene librerie come PROJ e SIS permettano di
selezionare trasformazioni specifiche (tramite codice EPSG o basandosi
sull'area di interesse), questo livello di controllo non è attualmente
esposto nell'API di Sedona. Questo rafforza l'idea che la mancanza di
supporto per GSB sia legata all'interfaccia della funzione, che non
permette la specificità richiesta per le trasformazioni basate su
griglia.

Ricerca su Stack Overflow e Forum:

Anche le ricerche su piattaforme come Stack Overflow 12 non mostrano
domande o discussioni focalizzate sull'uso diretto di file GSB con
ST\_Transform in Sedona. Le domande esistenti riguardano l'uso base
della funzione, la corretta specificazione dei CRS tramite EPSG, la
gestione dell'ordine delle coordinate 38, o confronti generali con le
funzionalità di PostGIS. Ad esempio, in 13, viene discussa la
trasformazione di coordinate nel contesto di GeoMesa e Spark, e una
delle risposte suggerisce di consultare la documentazione di Sedona per
ST\_Transform, la quale, come già stabilito, non menziona il supporto
GSB.

Altre discussioni <sup>34</sup> illustrano come utilizzare i file
GSB/NTv2 in *PostGIS* tramite il parametro +nadgrids nelle stringhe
PROJ.4, evidenziando per contrasto l'assenza di un meccanismo analogo
documentato per Sedona.

Contesto Legacy (GeoSpark):

Un rapido controllo della documentazione relativa alle versioni
precedenti sotto il nome GeoSpark 39 conferma che anche in passato non
vi era menzione di supporto per GSB o NADGRIDS in ST\_Transform.

L'assenza di discussioni specifiche nella comunità riguardo al supporto
diretto di GSB suggerisce che gli utenti che necessitano di questa
funzionalità probabilmente non si aspettano che sia supportata
nativamente da ST\_Transform e si orientano direttamente verso soluzioni
alternative, come le UDF, o utilizzano altri strumenti (es. PostGIS,
GDAL) per la pre-elaborazione. La discussione nell'issue GitHub \#1397
<sup>10</sup> indica che la necessità di un controllo più fine sulle
trasformazioni è riconosciuta, ma non è soddisfatta dall'attuale
interfaccia di ST\_Transform.

**V. Investigazione delle Librerie Sottostanti (GeoTools)**

Per comprendere appieno le potenzialità e le limitazioni di
ST\_Transform in Sedona, è utile esaminare le capacità della libreria
geospaziale sottostante che Sedona utilizza per le operazioni di
trasformazione delle coordinate.

Identificazione della Dipendenza:

Apache Sedona, in particolare per le sue funzionalità Java/Scala e le
funzioni SQL, si basa pesantemente sulla libreria GeoTools. Questo è
evidente dalle dipendenze Maven specificate nella documentazione di
installazione e negli esempi, che tipicamente includono
org.datasyslab:geotools-wrapper.14 Il versioning di questo wrapper è
spesso legato alla versione di GeoTools che incapsula; ad esempio,
geotools-wrapper:1.7.1-28.5 utilizzato da Sedona 1.7.1 18 suggerisce
l'uso di GeoTools versione 28.5. Versioni precedenti di Sedona
utilizzavano versioni corrispondenti di GeoTools (es. Sedona 1.4.1 con
geotools-wrapper:1.4.0-28.2 19, Sedona 1.5.1 con 1.5.1-28.2 15).

Capacità di GeoTools relative a GSB/NADGRID/NTv2:

GeoTools è una libreria geospaziale Java matura e potente che implementa
le specifiche Open Geospatial Consortium (OGC). È noto che GeoTools
supporta trasformazioni di datum basate su griglia, inclusi i formati
NTv2 e NADCON (che utilizza file.las/.los o.laa/.loa, funzionalmente
simili ai.gsb per NAD27/NAD83).22 La documentazione di GeoTools e le
discussioni della comunità confermano questa capacità:

- La classe NADCONTransform <sup>22</sup> implementa specificamente la
  trasformazione NADCON utilizzando file di griglia.

- Discussioni su GIS Stack Exchange <sup>23</sup> e issue su GitHub
  <sup>24</sup> mostrano come gli utenti utilizzino file.gsb (NTv2) con
  GeoTools, tipicamente posizionando i file in un percorso specifico
  delle risorse (org/geotools/referencing/factory/gridshift/) affinché
  vengano rilevati automaticamente dal motore di trasformazione.

- Anche JOSM, che utilizza GeoTools, menziona la necessità di database
  di shift (datum grids) per certe trasformazioni.<sup>42</sup>

- PostGIS stesso, che supporta +nadgrids <sup>43</sup>, si integra o
  interagisce con librerie come PROJ, che sono anche alla base di molte
  funzionalità di GeoTools.

L'utilizzo di queste trasformazioni in GeoTools richiede tipicamente che
i file di griglia siano presenti in un percorso noto alla libreria (come
il percorso delle risorse menzionato) o che la configurazione
dell'ambiente (es. variabili d'ambiente o proprietà di sistema Java) sia
impostata per indicare dove trovare questi file.

Il Divario tra Libreria e Funzione Sedona:

Emerge qui una chiara discrepanza:

1.  La libreria sottostante, GeoTools (nella versione utilizzata da
    Sedona recente, es. 28.x), *possiede* la capacità tecnica di
    eseguire trasformazioni basate su GSB/NTv2.<sup>22</sup>

2.  L'interfaccia della funzione ST\_Transform esposta da Sedona agli
    utenti tramite SQL o l'API DataFrame *non include* i parametri
    necessari per specificare quali file di griglia utilizzare o per
    selezionare esplicitamente una pipeline di trasformazione basata su
    griglia.<sup>1</sup>

Questa situazione è ulteriormente confermata dalla discussione
nell'issue GitHub \#1397 <sup>10</sup>, dove si evidenzia che, sebbene
librerie come PROJ (usata da GeoTools) o Apache SIS permettano la
selezione esplicita dell'operazione di trasformazione (che è ciò che
servirebbe per forzare l'uso di una griglia specifica), questa
funzionalità non è accessibile tramite l'attuale interfaccia di
ST\_Transform in Sedona.

Pertanto, la limitazione non risiede in un'incapacità fondamentale del
motore di trasformazione utilizzato da Sedona, ma piuttosto
nell'interfaccia della funzione SQL/DataFrame ST\_Transform che non
espone i meccanismi di controllo necessari per l'uso diretto e
specificato dall'utente dei file GSB nelle implementazioni per Spark e
Flink. Questo implica che per ottenere trasformazioni basate su GSB, è
necessario aggirare l'interfaccia standard di ST\_Transform.

**VI. Soluzioni Alternative per Trasformazioni Basate su GSB in
Sedona/Spark**

Data l'assenza di supporto diretto per i file GSB nella funzione
ST\_Transform standard di Sedona per Spark e Flink, gli utenti che
necessitano di questo tipo di trasformazione ad alta precisione devono
implementare soluzioni alternative (workaround) all'interno
dell'ecosistema Spark/Sedona.

**Approccio 1: User-Defined Functions (UDF) Spark**

Questo è l'approccio più comune per estendere le funzionalità di
Spark/Sedona. Consiste nell'incapsulare la logica di trasformazione, che
utilizza una libreria esterna capace di gestire i file GSB, all'interno
di una UDF Spark.

- **Concetto:** Si definisce una funzione (tipicamente in Python o
  Scala/Java) che prende in input la geometria (es. come stringa WKT o
  array di byte WKB) e gli identificatori CRS di origine e destinazione.
  All'interno della UDF, si utilizza una libreria esterna (come pyproj
  per Python, o le API Java di GeoTools/PROJ) per eseguire la
  trasformazione, assicurandosi che questa libreria possa accedere ai
  file GSB necessari. La UDF restituisce quindi la geometria
  trasformata.

- **Implementazione con pyproj (Python UDF):**

  - **Dipendenze:** Richiede che la libreria pyproj (un wrapper Python
    per la libreria PROJ) sia installata su tutti i nodi worker del
    cluster Spark.

  - **Gestione File GSB:** I file.gsb necessari devono essere
    distribuiti e resi accessibili su ogni nodo worker. Questo può
    essere fatto tramite filesystem condivisi, includendoli nelle
    immagini Docker dei worker, o distribuendoli tramite l'opzione
    --files di Spark. È cruciale che la libreria PROJ sottostante sia
    configurata per trovare questi file, solitamente impostando la
    variabile d'ambiente PROJ\_LIB in modo appropriato sui worker.

  - **Logica UDF:** La UDF creerebbe un oggetto pyproj.Transformer
    specificando i CRS di origine e destinazione. La libreria PROJ, se
    configurata correttamente, selezionerà automaticamente la
    trasformazione basata su griglia appropriata se disponibile per la
    coppia di CRS e l'area geografica. Il metodo transform del
    Transformer verrebbe quindi utilizzato. È necessario gestire la
    serializzazione/deserializzazione delle geometrie tra il formato
    DataFrame (es. WKB letto da Sedona) e il formato richiesto da
    pyproj.

  - **Performance:** Le UDF Python introducono un overhead dovuto alla
    serializzazione dei dati tra JVM e Python e all'esecuzione del
    codice Python. Questo può impattare le prestazioni su dataset molto
    grandi rispetto a funzioni native implementate in Scala/Java.

- **Implementazione con GDAL (Python UDF):**

  - **Dipendenze:** Richiede le librerie Python di GDAL installate sui
    worker.

  - **Gestione File GSB:** Simile a pyproj, GDAL (che utilizza PROJ)
    necessita dell'accesso ai file GSB e della configurazione corretta
    della sua directory dati (GDAL\_DATA) e di PROJ\_LIB.

  - **Logica UDF:** Si potrebbero usare le funzioni di trasformazione
    delle coordinate delle API Python di GDAL
    (osr.CoordinateTransformation). Un'alternativa, meno elegante
    all'interno di una UDF, potrebbe essere chiamare l'utility ogr2ogr
    tramite subprocess, ma questo è generalmente sconsigliato per
    performance e gestione degli errori.

  - **Performance:** Simili considerazioni sull'overhead delle UDF
    Python.

- **Pro:**

  - Mantiene l'elaborazione all'interno del framework Spark/Sedona.

  - Sfrutta librerie Python/Java geospaziali mature e ampiamente
    utilizzate.

  - Flessibilità nell'implementare logiche di trasformazione complesse.

- **Contro:**

  - Complessità nella gestione delle dipendenze delle librerie esterne
    su tutti i nodi worker.

  - Complessità nella distribuzione e configurazione dell'accesso ai
    file GSB sui worker (PROJ\_LIB, GDAL\_DATA).

  - Potenziale impatto negativo sulle prestazioni a causa dell'overhead
    delle UDF (specialmente Python).

  - Richiede una gestione attenta degli errori all'interno della UDF.

**Approccio 2: Elaborazione Esterna / Pre-elaborazione**

Questo approccio sposta la trasformazione basata su GSB al di fuori del
job Spark/Sedona principale, eseguendola come passo preliminare o
separato.

- **Concetto:** Utilizzare uno strumento esterno, tipicamente l'utility
  a riga di comando ogr2ogr di GDAL, per leggere i dati dalla fonte
  originale, applicare la trasformazione GSB e scrivere i dati
  trasformati in un formato (es. GeoParquet, PostGIS) che può poi essere
  letto da Spark/Sedona senza ulteriori trasformazioni di datum
  complesse.

- **Implementazione con ogr2ogr:**

  - **Strumento:** ogr2ogr è uno strumento estremamente versatile per la
    conversione e trasformazione di dati vettoriali.<sup>44</sup> Può
    leggere da numerose fonti, incluse basi di dati come Oracle Spatial
    <sup>44</sup> o PostGIS.<sup>47</sup>

  - **Trasformazione:** Utilizzando le opzioni -s\_srs e -t\_srs,
    ogr2ogr invoca la libreria PROJ sottostante. Se PROJ è configurato
    correttamente per trovare i file GSB (tramite PROJ\_LIB), applicherà
    automaticamente la trasformazione basata su griglia appropriata. Non
    è necessario specificare esplicitamente il file GSB nel comando
    ogr2ogr se PROJ è configurato correttamente.

  - **Output:** ogr2ogr può scrivere in formati ottimizzati per data
    lake, come GeoParquet <sup>49</sup>, che possono poi essere letti
    efficientemente da Sedona.<sup>20</sup> Può anche scrivere
    direttamente in PostGIS o altri database.

  - **Esecuzione:** Questo passo può essere eseguito prima
    dell'ingestione nel data lake, oppure orchestrato come un task
    separato in un workflow (es. usando Airflow con BashOperator o
    KubernetesPodOperator per eseguire il comando ogr2ogr
    <sup>59</sup>).

  - **Performance:** Le prestazioni di ogr2ogr possono essere
    ottimizzate. Ad esempio, per caricamenti in PostGIS, --config
    PG\_USE\_COPY YES può accelerare significativamente
    l'inserimento.<sup>53</sup> L'opzione GDAL\_CACHEMAX può influenzare
    le operazioni che richiedono caching.<sup>73</sup> La conversione
    diretta tra formati efficienti (es. PostGIS a GeoParquet) può essere
    relativamente veloce.<sup>49</sup>

- **Pro:**

  - Sfrutta l'implementazione C++ ottimizzata di GDAL/PROJ,
    potenzialmente più performante delle UDF Python.

  - Separa la complessità della trasformazione GSB dal job Spark/Sedona
    principale.

  - Le dipendenze (GDAL, file GSB) sono necessarie solo nell'ambiente di
    esecuzione di ogr2ogr.

- **Contro:**

  - Aggiunge un passo ETL separato al workflow complessivo.

  - Potrebbe richiedere la scrittura di dati intermedi su storage.

  - Richiede l'orchestrazione di questo passo esterno.

**Approccio 3: SedonaSnow Native App (Solo per Snowflake)**

- **Concetto:** Se l'ambiente operativo è Snowflake, si può installare e
  utilizzare l'applicazione "SedonaSnow" dal Marketplace di Snowflake.
  Come indicato in <sup>26</sup>, la funzione
  sedonasnow.sedona.ST\_TRANSFORM fornita da questa app sembra essere in
  grado di gestire trasformazioni che richiedono file di griglia.

- **Pro:**

  - Soluzione integrata e potenzialmente ottimizzata all'interno
    dell'ambiente Snowflake.

  - Utilizza la sintassi SQL familiare di Sedona.

- **Contro:**

  - Applicabile solo agli utenti Snowflake.

  - Dipende da un'applicazione specifica del Marketplace.

  - Meno trasparenza sul meccanismo esatto di gestione dei file GSB
    (probabilmente gestito internamente dall'app).

**Tabella Comparativa delle Soluzioni Alternative**

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
<th><strong>Caratteristica</strong></th>
<th><strong>UDF Spark (pyproj)</strong></th>
<th><strong>UDF Spark (GDAL Python)</strong></th>
<th><strong>ogr2ogr Esterno</strong></th>
<th><strong>SedonaSnow App (Snowflake)</strong></th>
</tr>
<tr>
<th><strong>Integrazione Spark</strong></th>
<th>Alta</th>
<th>Alta</th>
<th>Bassa (passo separato)</th>
<th>N/A (Specifico Snowflake)</th>
</tr>
<tr>
<th><strong>Complessità Impl.</strong></th>
<th>Media (UDF, deps, GSB)</th>
<th>Media (UDF, deps, GSB)</th>
<th>Bassa (script ogr2ogr)</th>
<th>Bassa (Installazione App)</th>
</tr>
<tr>
<th><strong>Dipendenze Worker</strong></th>
<th>pyproj, PROJ, GSB files</th>
<th>gdal, PROJ, GSB files</th>
<th>Nessuna (solo dove gira ogr2ogr)</th>
<th>SedonaSnow App</th>
</tr>
<tr>
<th><strong>Gestione File GSB</strong></th>
<th>Distribuzione + PROJ_LIB sui worker</th>
<th>Distribuzione + PROJ_LIB sui worker</th>
<th>PROJ_LIB dove gira ogr2ogr</th>
<th>Gestita internamente dall'app</th>
</tr>
<tr>
<th><strong>Performance Potenziale</strong></th>
<th>Media (overhead UDF Python)</th>
<th>Media (overhead UDF Python)</th>
<th>Alta (GDAL C++)</th>
<th>Potenzialmente Alta (Nativa)</th>
</tr>
<tr>
<th><strong>Manutenibilità</strong></th>
<th>Media (deps, UDF)</th>
<th>Media (deps, UDF)</th>
<th>Media (script, orchestrazione)</th>
<th>Bassa (gestita da vendor)</th>
</tr>
<tr>
<th><strong>Flessibilità</strong></th>
<th>Alta</th>
<th>Alta</th>
<th>Media (limitata a ogr2ogr)</th>
<th>Bassa (legata a Snowflake)</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

La scelta della soluzione alternativa più adatta dipende dal contesto
specifico. Le UDF offrono la massima integrazione ma presentano sfide di
deployment e potenziali colli di bottiglia prestazionali. L'elaborazione
esterna con ogr2ogr può essere più performante e isolare le dipendenze,
ma richiede un passo aggiuntivo nel workflow. Per gli utenti Snowflake,
l'app SedonaSnow rappresenta un'opzione dedicata.

**VII. Conclusioni e Raccomandazioni**

L'analisi condotta sulla documentazione ufficiale di Apache Sedona,
sulle risorse della comunità e sulle librerie sottostanti porta a
concludere che la funzione ST\_Transform, nelle sue implementazioni
standard per Apache Spark e Apache Flink, **non fornisce supporto
diretto** per l'utilizzo di file di grigliati di spostamento (GSB, NTv2)
tramite parametri specifici o stringhe PROJ avanzate.

- **Mancanza di Supporto Diretto:** Nonostante la libreria GeoTools, su
  cui Sedona si basa <sup>14</sup>, sia capace di eseguire
  trasformazioni basate su griglia <sup>22</sup>, l'interfaccia della
  funzione ST\_Transform esposta in Sedona per Spark/Flink non include i
  parametri necessari (come percorsi ai file GSB, direttive +nadgrids o
  codici EPSG per specifiche pipeline di trasformazione) per invocare e
  controllare queste operazioni.<sup>1</sup> Questa limitazione è
  confermata dall'assenza di documentazione in merito e dalla mancanza
  di discussioni o segnalazioni specifiche nella comunità.<sup>8</sup>
  L'eccezione notevole è l'ambiente Snowflake, dove l'applicazione
  SedonaSnow sembra abilitare tali trasformazioni <sup>26</sup>,
  suggerendo una capacità latente nel core ma non esposta
  universalmente.

- **Necessità di Soluzioni Alternative:** Gli utenti che richiedono la
  precisione offerta dalle trasformazioni basate su griglia GSB
  all'interno di un ambiente Spark/Sedona devono implementare soluzioni
  alternative.

**Azioni Raccomandate:**

1.  **Utilizzo di UDF Spark con pyproj:** Per gli utenti che
    preferiscono mantenere l'elaborazione interamente all'interno di
    Spark, si raccomanda l'implementazione di una User-Defined Function
    (UDF) Python che utilizzi la libreria pyproj.

    - **Requisiti:** Installazione di pyproj su tutti i nodi worker;
      distribuzione dei file.gsb necessari sui worker; configurazione
      della variabile d'ambiente PROJ\_LIB sui worker affinché PROJ
      possa localizzare i file di griglia.

    - **Vantaggi:** Integrazione nel flusso Spark; flessibilità.

    - **Svantaggi:** Complessità di setup (dipendenze, distribuzione
      file GSB, configurazione PROJ\_LIB); potenziale overhead
      prestazionale delle UDF Python su grandi volumi di dati.

2.  **Pre-elaborazione con ogr2ogr:** Per scenari dove le prestazioni
    sono critiche o si preferisce isolare le dipendenze complesse, si
    raccomanda di eseguire la trasformazione GSB come passo di
    pre-elaborazione utilizzando l'utility ogr2ogr di GDAL.

    - **Workflow:** ogr2ogr legge i dati sorgente, applica la
      trasformazione (invocando PROJ, che userà i file GSB se PROJ\_LIB
      è configurata) e scrive i dati trasformati in un formato (es.
      GeoParquet <sup>49</sup>) leggibile da Sedona.

    - **Vantaggi:** Sfrutta l'implementazione C++ ottimizzata di
      GDAL/PROJ; isola le dipendenze complesse; potenzialmente più
      performante per grandi trasformazioni batch.

    - **Svantaggi:** Richiede un passo ETL aggiuntivo; necessita di
      orchestrazione esterna; potrebbe richiedere storage intermedio.

3.  **Valutazione di SedonaSnow (per utenti Snowflake):** Gli utenti che
    operano nell'ecosistema Snowflake dovrebbero valutare l'utilizzo
    dell'applicazione SedonaSnow Native App, che, secondo la
    documentazione della community Snowflake <sup>26</sup>, abilita
    trasformazioni basate su griglia tramite la sua versione di
    ST\_Transform.

Prospettive Future:

Sebbene attualmente non supportato direttamente, è possibile che future
versioni di Apache Sedona possano esporre un controllo più granulare
sulle pipeline di trasformazione di GeoTools/PROJ, potenzialmente
abilitando il supporto per GSB o la selezione esplicita di
trasformazioni (come discusso in 10). Tuttavia, allo stato attuale, le
soluzioni alternative rimangono l'unica via praticabile per ottenere
trasformazioni basate su GSB nell'ambiente standard Spark/Flink con
Sedona.

**VIII. Riferimenti**

<sup>1</sup>

- **Documentazione Apache Sedona:**
  [<u>https://sedona.apache.org/</u>](https://sedona.apache.org/)

- **Documentazione GeoTools:**
  [<u>https://geotools.org/</u>](https://geotools.org/)

- **Documentazione PROJ:** [<u>https://proj.org/</u>](https://proj.org/)

- **Documentazione pyproj:**
  [<u>https://pyproj4.github.io/pyproj/stable/</u>](https://pyproj4.github.io/pyproj/stable/)

- **Documentazione GDAL:** [<u>https://gdal.org/</u>](https://gdal.org/)

- **Documentazione PostGIS
  ST\_Transform:**([<u>https://postgis.net/docs/ST\_Transform.html</u>](https://postgis.net/docs/ST_Transform.html))

- **Issue GitHub Sedona \#1397:**
  [<u>https://github.com/apache/sedona/issues/1397</u>](https://github.com/apache/sedona/issues/1397)

- **Articolo Community Snowflake su
  ST\_TRANSFORM:**([<u>https://community.snowflake.com/s/article/100405-P0000-Failed-to-transform-the-coordinates-from-SRID-to-another-when-using-ST-TRANSFORM-function</u>](https://community.snowflake.com/s/article/100405-P0000-Failed-to-transform-the-coordinates-from-SRID-to-another-when-using-ST-TRANSFORM-function))#
  Analisi del Supporto per File di Grigliati di Spostamento (GSB) nella
  Funzione ST\_Transform di Apache Sedona

**I. Sommario Esecutivo**

Il presente rapporto analizza la capacità della funzione ST\_Transform
di Apache Sedona di utilizzare direttamente file di grigliati di
spostamento (formato.gsb o equivalenti come NTv2) per trasformazioni di
coordinate ad alta precisione, in particolare quelle che coinvolgono
cambi di datum. L'analisi si basa sulla documentazione ufficiale di
Sedona (versioni recenti fino alla 1.7.1), discussioni della comunità,
issue tracker e l'esame delle librerie sottostanti.

**Risultato Chiave:** Sulla base delle prove disponibili, la funzione
ST\_Transform di Apache Sedona, nelle sue implementazioni per Apache
Spark e Apache Flink, **non supporta direttamente** l'uso di file di
grigliati di spostamento GSB tramite parametri espliciti o stringhe PROJ
che li referenziano. La documentazione ufficiale descrive l'uso di
codici EPSG e, in versioni più recenti, stringhe WKT, ma omette
qualsiasi riferimento a parametri per specificare file di griglia o
trasformazioni basate su griglia come +nadgrids.

**Sintesi delle Prove:** L'assenza di menzioni di GSB, NADGRIDS, NTv2 o
stringhe PROJ complete nella documentazione API di ST\_Transform per le
versioni Spark/Flink <sup>1</sup> è la prova principale. Ricerche nei
canali della comunità (issue GitHub <sup>8</sup>, Stack Overflow
<sup>12</sup>) non hanno rivelato discussioni o richieste relative al
supporto diretto di GSB in ST\_Transform. Sebbene la libreria
sottostante GeoTools, utilizzata da Sedona <sup>14</sup>, possieda la
capacità intrinseca di eseguire trasformazioni basate su griglia
<sup>22</sup>, questa funzionalità non sembra essere esposta tramite
l'interfaccia standard di ST\_Transform in Sedona per Spark/Flink.
Un'eccezione degna di nota è l'applicazione SedonaSnow per Snowflake,
che sembra in grado di gestire trasformazioni basate su griglia
<sup>26</sup>, suggerendo che il motore di trasformazione centrale
potrebbe avere la capacità, ma non è accessibile tramite parametri
standard nelle implementazioni Spark/Flink.

**Raccomandazione Primaria:** In assenza di supporto diretto, gli utenti
che necessitano di trasformazioni basate su GSB all'interno
dell'ecosistema Spark/Sedona devono ricorrere a soluzioni alternative.
Le opzioni più praticabili includono l'uso di User-Defined Functions
(UDF) Spark che incapsulano librerie esterne come pyproj (che a sua
volta utilizza PROJ) o potenzialmente le API Python di GDAL. Queste
soluzioni alternative introducono complessità aggiuntive legate alla
gestione delle dipendenze, alla distribuzione dei file GSB sui nodi
worker e alla potenziale riduzione delle prestazioni dovuta all'overhead
delle UDF. Un'alternativa consiste nell'eseguire le trasformazioni come
passo di pre-elaborazione esterno utilizzando strumenti come ogr2ogr
prima dell'ingestione dei dati in Sedona. La scelta della soluzione
alternativa dipende dai requisiti specifici di performance, dalla
complessità dell'infrastruttura e dalla familiarità del team con le
diverse tecnologie.

**II. Introduzione**

Le trasformazioni di coordinate sono un'operazione fondamentale
nell'analisi di dati geospaziali, consentendo l'integrazione e il
confronto di dati provenienti da diverse fonti con differenti sistemi di
riferimento delle coordinate (CRS). Mentre le trasformazioni tra
proiezioni cartografiche sono relativamente comuni, le trasformazioni
che coinvolgono un cambio di datum geodetico richiedono spesso un
livello di precisione più elevato. I file di grigliati di spostamento
(grid shift files), comunemente nei formati GSB (Grid Shift Binary) o
NTv2 (National Transformation version 2), forniscono correzioni basate
su griglia per modellare accuratamente le distorsioni locali tra datum,
ottenendo così trasformazioni più precise rispetto ai metodi basati su
parametri medi (come le trasformazioni Helmert a 3 o 7 parametri).

Apache Sedona è un sistema di calcolo distribuito ad alte prestazioni
progettato per elaborare dati spaziali su larga scala, estendendo
piattaforme come Apache Spark, Apache Flink e Snowflake.<sup>14</sup>
Offre un ricco set di funzioni SQL spaziali, tra cui ST\_Transform, per
la manipolazione e l'analisi di dati geospaziali distribuiti. Data
l'importanza delle trasformazioni di datum ad alta precisione in molti
domini applicativi (es. catasto, ingegneria civile, monitoraggio
ambientale), sorge la questione se Sedona fornisca meccanismi integrati
per sfruttare i file GSB direttamente all'interno della sua funzione
ST\_Transform.

Questo rapporto indaga sistematicamente la presenza o l'assenza di
supporto diretto per i file GSB nella funzione ST\_Transform di Apache
Sedona. L'analisi si basa su un esame approfondito della documentazione
ufficiale più recente (incluse API, note di rilascio e tutorial), una
ricerca mirata nelle risorse della comunità (forum, issue tracker) e una
valutazione delle capacità delle librerie sottostanti, principalmente
GeoTools. Infine, qualora il supporto diretto risulti assente, verranno
identificate e valutate le soluzioni alternative praticabili all'interno
dell'ecosistema Spark/Sedona. L'obiettivo è fornire una risposta
definitiva e basata su prove concrete, utile a professionisti tecnici
che necessitano di implementare trasformazioni di coordinate basate su
griglia nei loro workflow Sedona.

**III. Analisi di ST\_Transform nella Documentazione di Apache Sedona**

Un'analisi dettagliata della documentazione ufficiale di Apache Sedona
relativa alla funzione ST\_Transform è fondamentale per determinare il
livello di supporto per le trasformazioni basate su griglia GSB.

Firma della Funzione e Parametri Documentati:

Le documentazioni API per le diverse versioni recenti di Sedona (ad
esempio, 1.3.x, 1.4.x, 1.5.x, 1.6.x, 1.7.x) presentano in modo
consistente la funzione ST\_Transform.1 La firma tipica richiede la
geometria di input, un identificatore per il CRS di origine (spesso
dedotto dall'SRID della geometria stessa) e un identificatore per il CRS
di destinazione. I metodi documentati per specificare i CRS sono
principalmente:

1.  Codici EPSG: Stringhe nella forma 'EPSG:xxxx' (es. 'EPSG:4326',
    'EPSG:32649').

2.  Stringhe WKT (Well-Known Text): A partire dalla versione 1.3.0, è
    stato documentato il supporto per specificare i CRS tramite stringhe
    in formato OGC WKT v1.<sup>1</sup>

Assenza di Supporto Esplicito per GSB/NADGRIDS/PROJ:

Un punto cruciale è l'assenza totale, in tutta la documentazione
esaminata per le implementazioni Spark e Flink 1, di qualsiasi menzione
relativa a parametri o sintassi per:

- Specificare percorsi a file GSB.

- Utilizzare direttive +nadgrids all'interno di stringhe PROJ.

- Specificare nomi di trasformazioni NTv2 definite esternamente.

- Passare stringhe PROJ complete che potrebbero contenere riferimenti a
  file di griglia.

Questa omissione è significativa se confrontata con altri sistemi
geospaziali come PostGIS, la cui funzione ST\_Transform supporta
esplicitamente l'uso di stringhe PROJ.4 complete, incluso il parametro
+nadgrids per invocare trasformazioni basate su griglia.<sup>34</sup> La
mancanza di documentazione su come fornire questi parametri specifici
per le griglie indica che tale funzionalità non è un'interfaccia utente
prevista o supportata per ST\_Transform in Sedona per Spark/Flink.

Note sulla Gestione dei CRS:

La documentazione di Sedona mostra attenzione ai dettagli relativi ai
CRS. Ad esempio, le note di rilascio della versione 1.5.0 31 specificano
un cambiamento nel comportamento predefinito per diverse funzioni
(inclusa ST\_Transform), richiedendo che i dati di input siano in ordine
longitudine/latitudine e introducendo la funzione ST\_FlipCoordinates
per gestire eventuali inversioni necessarie.1 Inoltre, l'introduzione di
funzioni come ST\_BestSRID 1 (per determinare un SRID ottimale per una
geometria) e funzioni per calcoli sferoidali (ST\_DistanceSpheroid,
ST\_AreaSpheroid 19) dimostra la consapevolezza degli sviluppatori di
Sedona riguardo a concetti avanzati di CRS e datum. Tuttavia, queste
funzionalità, pur essendo correlate, non implicano direttamente il
supporto per l'uso controllato di file GSB da parte dell'utente
all'interno di ST\_Transform. Dimostrano che Sedona può gestire
complessità geodetiche, ma non che esponga l'interfaccia per le griglie
GSB.

Contesto Specifico: Sedona su Snowflake:

Un'informazione rilevante proviene da un articolo della community di
Snowflake.26 L'articolo spiega che la funzione ST\_TRANSFORM nativa di
Snowflake fallisce per trasformazioni che richiedono file di griglia
(viene fornito l'esempio da EPSG:4326 a EPSG:7844), un problema comune
quando non è disponibile il supporto per NADGRIDS/NTv2. La soluzione
proposta è utilizzare la funzione sedonasnow.sedona.ST\_TRANSFORM
fornita dall'applicazione SedonaSnow Native App, disponibile sul
Marketplace di Snowflake. L'articolo mostra che questa funzione
specifica di Sedona riesce a eseguire la trasformazione. Questo
suggerisce fortemente che il motore di trasformazione sottostante
utilizzato da Sedona (probabilmente basato su GeoTools/PROJ) è in grado
di gestire le trasformazioni basate su griglia, ma che l'interfaccia
della funzione ST\_Transform standard nelle implementazioni Spark/Flink
non espone i parametri necessari affinché l'utente possa specificare e
utilizzare direttamente i file GSB. La capacità esiste nel nucleo, ma
non è accessibile tramite l'API pubblica standard per Spark/Flink.

In sintesi, l'analisi della documentazione ufficiale porta a concludere
che, nonostante la presenza di funzionalità geodetiche avanzate e un
potenziale supporto nel motore sottostante (come evidenziato dal caso
Snowflake), la funzione ST\_Transform di Sedona per Spark e Flink non è
stata progettata o documentata per accettare parametri diretti per
l'utilizzo di file GSB. L'enfasi è posta sull'uso di codici EPSG e
stringhe WKT.

**IV. Conoscenza della Comunità e Problemi Segnalati**

Oltre alla documentazione ufficiale, l'analisi delle discussioni della
comunità, dei bug report e delle domande degli utenti può fornire
ulteriori indicazioni sul supporto effettivo o sulle problematiche
riscontrate nell'utilizzo di ST\_Transform con file GSB.

Ricerca su GitHub Issues:

Una ricerca negli issue tracker di Apache Sedona su GitHub 8 non ha
rivelato segnalazioni di bug o richieste di funzionalità (feature
request) specifiche riguardanti l'aggiunta del supporto diretto per file
GSB, direttive NADGRIDS o trasformazioni NTv2 all'interno della funzione
ST\_Transform. Gli issue esistenti relativi a ST\_Transform o alle
trasformazioni CRS tendono a concentrarsi su altri aspetti, come la
gestione dell'ordine delle coordinate 31 o la compatibilità con formati
specifici.

Un issue particolarmente pertinente è il \#1397.<sup>10</sup> In questo
issue, un utente chiede se sia possibile specificare un *metodo* di
trasformazione specifico (identificato da un codice EPSG, es. 1612)
quando si trasforma tra due datum (es. da EPSG:4258 a EPSG:4326),
sottolineando come la scelta della trasformazione influenzi
l'accuratezza. La risposta di uno sviluppatore esterno (con esperienza
in Apache SIS, un'altra libreria geospaziale) conferma che Sedona
utilizza GeoTools e che, sebbene librerie come PROJ e SIS permettano di
selezionare trasformazioni specifiche (tramite codice EPSG o basandosi
sull'area di interesse), questo livello di controllo non è attualmente
esposto nell'API di Sedona. Questo rafforza l'idea che la mancanza di
supporto per GSB sia legata all'interfaccia della funzione, che non
permette la specificità richiesta per le trasformazioni basate su
griglia. La necessità è riconosciuta, ma la funzionalità non è
implementata nell'interfaccia pubblica.

Ricerca su Stack Overflow e Forum:

Anche le ricerche su piattaforme come Stack Overflow 12 non mostrano
domande o discussioni focalizzate sull'uso diretto di file GSB con
ST\_Transform in Sedona. Le domande esistenti riguardano l'uso base
della funzione, la corretta specificazione dei CRS tramite EPSG, la
gestione dell'ordine delle coordinate 38, o confronti generali con le
funzionalità di PostGIS. Ad esempio, in 13, viene discussa la
trasformazione di coordinate nel contesto di GeoMesa e Spark, e una
delle risposte suggerisce di consultare la documentazione di Sedona per
ST\_Transform, la quale, come già stabilito, non menziona il supporto
GSB.

Altre discussioni <sup>34</sup> illustrano come utilizzare i file
GSB/NTv2 in *PostGIS* tramite il parametro +nadgrids nelle stringhe
PROJ.4, evidenziando per contrasto l'assenza di un meccanismo analogo
documentato per Sedona. Questo confronto implicito rafforza l'idea che
tale funzionalità non sia presente in Sedona.

Contesto Legacy (GeoSpark):

Un rapido controllo della documentazione relativa alle versioni
precedenti sotto il nome GeoSpark 39 conferma che anche in passato non
vi era menzione di supporto per GSB o NADGRIDS in ST\_Transform. La
funzionalità non è stata rimossa, semplicemente non sembra essere mai
stata implementata nell'interfaccia SQL/DataFrame.

L'assenza di discussioni specifiche nella comunità riguardo al supporto
diretto di GSB suggerisce che gli utenti che necessitano di questa
funzionalità probabilmente non si aspettano che sia supportata
nativamente da ST\_Transform e si orientano direttamente verso soluzioni
alternative, come le UDF, o utilizzano altri strumenti (es. PostGIS,
GDAL) per la pre-elaborazione. La discussione nell'issue GitHub \#1397
<sup>10</sup> indica che la necessità di un controllo più fine sulle
trasformazioni è riconosciuta, ma non è soddisfatta dall'attuale
interfaccia di ST\_Transform. L'evidenza collettiva dalla comunità è
quindi coerente con le conclusioni tratte dalla documentazione
ufficiale.

**V. Investigazione delle Librerie Sottostanti (GeoTools)**

Per comprendere appieno le potenzialità e le limitazioni di
ST\_Transform in Sedona, è utile esaminare le capacità della libreria
geospaziale sottostante che Sedona utilizza per le operazioni di
trasformazione delle coordinate.

Identificazione della Dipendenza:

Apache Sedona, in particolare per le sue funzionalità Java/Scala e le
funzioni SQL, si basa pesantemente sulla libreria GeoTools. Questo è
evidente dalle dipendenze Maven specificate nella documentazione di
installazione e negli esempi, che tipicamente includono
org.datasyslab:geotools-wrapper.14 Il versioning di questo wrapper è
spesso legato alla versione di GeoTools che incapsula; ad esempio,
geotools-wrapper:1.7.1-28.5 utilizzato da Sedona 1.7.1 18 suggerisce
l'uso di GeoTools versione 28.5. Versioni precedenti di Sedona
utilizzavano versioni corrispondenti di GeoTools (es. Sedona 1.4.1 con
geotools-wrapper:1.4.0-28.2 19, Sedona 1.5.1 con 1.5.1-28.2 15).
L'utilizzo di versioni relativamente recenti di GeoTools è importante
perché implica che Sedona eredita le capacità (e potenzialmente le
limitazioni) di queste versioni.

Capacità di GeoTools relative a GSB/NADGRID/NTv2:

GeoTools è una libreria geospaziale Java matura e potente che implementa
le specifiche Open Geospatial Consortium (OGC).84 È noto che GeoTools
supporta trasformazioni di datum basate su griglia, inclusi i formati
NTv2 e NADCON (che utilizza file.las/.los o.laa/.loa, funzionalmente
simili ai.gsb per NAD27/NAD83).22 La documentazione di GeoTools e le
discussioni della comunità confermano questa capacità:

- La classe NADCONTransform <sup>22</sup> implementa specificamente la
  trasformazione NADCON utilizzando file di griglia.

- Discussioni su GIS Stack Exchange <sup>23</sup> e issue su GitHub
  <sup>24</sup> mostrano come gli utenti utilizzino file.gsb (NTv2) con
  GeoTools, tipicamente posizionando i file in un percorso specifico
  delle risorse (org/geotools/referencing/factory/gridshift/) affinché
  vengano rilevati automaticamente dal motore di trasformazione.

- Anche JOSM, che utilizza GeoTools, menziona la necessità di database
  di shift (datum grids) per certe trasformazioni.<sup>42</sup>

- PostGIS stesso, che supporta +nadgrids <sup>43</sup>, si integra o
  interagisce con librerie come PROJ, che sono anche alla base di molte
  funzionalità di GeoTools.

L'utilizzo di queste trasformazioni in GeoTools richiede tipicamente che
i file di griglia siano presenti in un percorso noto alla libreria (come
il percorso delle risorse menzionato) o che la configurazione
dell'ambiente (es. variabili d'ambiente o proprietà di sistema Java) sia
impostata per indicare dove trovare questi file. GeoTools fa affidamento
su queste configurazioni per localizzare e applicare le griglie corrette
durante il processo di trasformazione.

Il Divario tra Libreria e Funzione Sedona:

Emerge qui una chiara discrepanza:

1.  La libreria sottostante, GeoTools (nella versione utilizzata da
    Sedona recente, es. 28.x), *possiede* la capacità tecnica di
    eseguire trasformazioni basate su GSB/NTv2.<sup>22</sup>

2.  L'interfaccia della funzione ST\_Transform esposta da Sedona agli
    utenti tramite SQL o l'API DataFrame *non include* i parametri
    necessari per specificare quali file di griglia utilizzare o per
    selezionare esplicitamente una pipeline di trasformazione basata su
    griglia.<sup>1</sup>

Questa situazione è ulteriormente confermata dalla discussione
nell'issue GitHub \#1397 <sup>10</sup>, dove si evidenzia che, sebbene
librerie come PROJ (usata da GeoTools) o Apache SIS permettano la
selezione esplicita dell'operazione di trasformazione (che è ciò che
servirebbe per forzare l'uso di una griglia specifica), questa
funzionalità non è accessibile tramite l'attuale interfaccia di
ST\_Transform in Sedona. La funzione Sedona agisce come un wrapper di
livello superiore che non espone tutte le opzioni di configurazione fine
disponibili nel motore GeoTools/PROJ sottostante.

Pertanto, la limitazione non risiede in un'incapacità fondamentale del
motore di trasformazione utilizzato da Sedona, ma piuttosto
nell'interfaccia della funzione SQL/DataFrame ST\_Transform che non
espone i meccanismi di controllo necessari per l'uso diretto e
specificato dall'utente dei file GSB nelle implementazioni per Spark e
Flink. Questo implica che per ottenere trasformazioni basate su GSB, è
necessario aggirare l'interfaccia standard di ST\_Transform.

**VI. Soluzioni Alternative per Trasformazioni Basate su GSB in
Sedona/Spark**

Data l'assenza di supporto diretto per i file GSB nella funzione
ST\_Transform standard di Sedona per Spark e Flink, gli utenti che
necessitano di questo tipo di trasformazione ad alta precisione devono
implementare soluzioni alternative (workaround) all'interno
dell'ecosistema Spark/Sedona.

**Approccio 1: User-Defined Functions (UDF) Spark**

Questo è l'approccio più comune per estendere le funzionalità di
Spark/Sedona. Consiste nell'incapsulare la logica di trasformazione, che
utilizza una libreria esterna capace di gestire i file GSB, all'interno
di una UDF Spark.

- **Concetto:** Si definisce una funzione (tipicamente in Python o
  Scala/Java) che prende in input la geometria (es. come stringa WKT o
  array di byte WKB) e gli identificatori CRS di origine e destinazione.
  All'interno della UDF, si utilizza una libreria esterna (come pyproj
  per Python, o le API Java di GeoTools/PROJ) per eseguire la
  trasformazione, assicurandosi che questa libreria possa accedere ai
  file GSB necessari. La UDF restituisce quindi la geometria
  trasformata.

- **Implementazione con pyproj (Python UDF):**

  - **Dipendenze:** Richiede che la libreria pyproj (un wrapper Python
    per la libreria PROJ <sup>148</sup>) sia installata su tutti i nodi
    worker del cluster Spark.

  - **Gestione File GSB:** I file.gsb necessari devono essere
    distribuiti e resi accessibili su ogni nodo worker. Questo può
    essere fatto tramite filesystem condivisi, includendoli nelle
    immagini Docker dei worker, o distribuendoli tramite l'opzione
    --files di Spark. È cruciale che la libreria PROJ sottostante sia
    configurata per trovare questi file, solitamente impostando la
    variabile d'ambiente PROJ\_LIB in modo appropriato sui worker.

  - **Logica UDF:** La UDF creerebbe un oggetto pyproj.Transformer
    specificando i CRS di origine e destinazione. La libreria PROJ, se
    configurata correttamente, selezionerà automaticamente la
    trasformazione basata su griglia appropriata se disponibile per la
    coppia di CRS e l'area geografica. Il metodo transform del
    Transformer verrebbe quindi utilizzato. È necessario gestire la
    serializzazione/deserializzazione delle geometrie tra il formato
    DataFrame (es. WKB letto da Sedona) e il formato richiesto da
    pyproj.

  - **Performance:** Le UDF Python introducono un overhead dovuto alla
    serializzazione dei dati tra JVM e Python e all'esecuzione del
    codice Python. Questo può impattare le prestazioni su dataset molto
    grandi rispetto a funzioni native implementate in Scala/Java.

- **Implementazione con GDAL (Python UDF):**

  - **Dipendenze:** Richiede le librerie Python di GDAL installate sui
    worker.

  - **Gestione File GSB:** Simile a pyproj, GDAL (che utilizza PROJ)
    necessita dell'accesso ai file GSB e della configurazione corretta
    della sua directory dati (GDAL\_DATA) e di PROJ\_LIB.

  - **Logica UDF:** Si potrebbero usare le funzioni di trasformazione
    delle coordinate delle API Python di GDAL
    (osr.CoordinateTransformation). Un'alternativa, meno elegante
    all'interno di una UDF, potrebbe essere chiamare l'utility ogr2ogr
    tramite subprocess, ma questo è generalmente sconsigliato per
    performance e gestione degli errori.

  - **Performance:** Simili considerazioni sull'overhead delle UDF
    Python.

- **Pro:**

  - Mantiene l'elaborazione all'interno del framework Spark/Sedona.

  - Sfrutta librerie Python/Java geospaziali mature e ampiamente
    utilizzate.<sup>148</sup>

  - Flessibilità nell'implementare logiche di trasformazione complesse.

- **Contro:**

  - Complessità nella gestione delle dipendenze delle librerie esterne
    su tutti i nodi worker.

  - Complessità nella distribuzione e configurazione dell'accesso ai
    file GSB sui worker (PROJ\_LIB, GDAL\_DATA).

  - Potenziale impatto negativo sulle prestazioni a causa dell'overhead
    delle UDF (specialmente Python).

  - Richiede una gestione attenta degli errori all'interno della UDF.

**Approccio 2: Elaborazione Esterna / Pre-elaborazione**

Questo approccio sposta la trasformazione basata su GSB al di fuori del
job Spark/Sedona principale, eseguendola come passo preliminare o
separato.

- **Concetto:** Utilizzare uno strumento esterno, tipicamente l'utility
  a riga di comando ogr2ogr di GDAL, per leggere i dati dalla fonte
  originale, applicare la trasformazione GSB e scrivere i dati
  trasformati in un formato (es. GeoParquet, PostGIS) che può poi essere
  letto da Spark/Sedona senza ulteriori trasformazioni di datum
  complesse.

- **Implementazione con ogr2ogr:**

  - **Strumento:** ogr2ogr è uno strumento estremamente versatile per la
    conversione e trasformazione di dati vettoriali.<sup>44</sup> Può
    leggere da numerose fonti, incluse basi di dati come Oracle Spatial
    <sup>44</sup> o PostGIS.<sup>47</sup>

  - **Trasformazione:** Utilizzando le opzioni -s\_srs e -t\_srs,
    ogr2ogr invoca la libreria PROJ sottostante. Se PROJ è configurato
    correttamente per trovare i file GSB (tramite PROJ\_LIB), applicherà
    automaticamente la trasformazione basata su griglia appropriata. Non
    è necessario specificare esplicitamente il file GSB nel comando
    ogr2ogr se PROJ è configurato correttamente.<sup>46</sup>

  - **Output:** ogr2ogr può scrivere in formati ottimizzati per data
    lake, come GeoParquet <sup>49</sup>, che possono poi essere letti
    efficientemente da Sedona.<sup>20</sup> Può anche scrivere
    direttamente in PostGIS o altri database. L'output può essere
    diretto verso storage S3 specificando il percorso
    /vsis3/.<sup>62</sup>

  - **Esecuzione:** Questo passo può essere eseguito prima
    dell'ingestione nel data lake, oppure orchestrato come un task
    separato in un workflow (es. usando Airflow con BashOperator o
    KubernetesPodOperator per eseguire il comando ogr2ogr
    <sup>59</sup>). La gestione degli errori e la tolleranza ai
    fallimenti in questo contesto richiedono attenzione, specialmente
    quando si scrive su S3 (es. gestione di upload
    interrotti).<sup>69</sup>

  - **Performance:** Le prestazioni di ogr2ogr possono essere
    ottimizzate. Ad esempio, per caricamenti in PostGIS, --config
    PG\_USE\_COPY YES può accelerare significativamente
    l'inserimento.<sup>53</sup> L'opzione GDAL\_CACHEMAX può influenzare
    le operazioni che richiedono caching <sup>73</sup>, sebbene il suo
    impatto dipenda dal workflow specifico. La conversione diretta tra
    formati efficienti (es. PostGIS a GeoParquet) può essere
    relativamente veloce.<sup>49</sup> Tuttavia, l'importazione di dati
    molto grandi (es. planet OSM) può richiedere tempi
    significativi.<sup>152</sup>

- **Pro:**

  - Sfrutta l'implementazione C++ ottimizzata di GDAL/PROJ,
    potenzialmente più performante delle UDF Python.

  - Separa la complessità della trasformazione GSB dal job Spark/Sedona
    principale.

  - Le dipendenze (GDAL, file GSB) sono necessarie solo nell'ambiente di
    esecuzione di ogr2ogr.

- **Contro:**

  - Aggiunge un passo ETL separato al workflow complessivo.

  - Potrebbe richiedere la scrittura di dati intermedi su storage.

  - Richiede l'orchestrazione di questo passo esterno e la gestione
    della sua affidabilità.

**Approccio 3: SedonaSnow Native App (Solo per Snowflake)**

- **Concetto:** Se l'ambiente operativo è Snowflake, si può installare e
  utilizzare l'applicazione "SedonaSnow" dal Marketplace di Snowflake.
  Come indicato in <sup>26</sup>, la funzione
  sedonasnow.sedona.ST\_TRANSFORM fornita da questa app sembra essere in
  grado di gestire trasformazioni che richiedono file di griglia.

- **Pro:**

  - Soluzione integrata e potenzialmente ottimizzata all'interno
    dell'ambiente Snowflake.

  - Utilizza la sintassi SQL familiare di Sedona.

- **Contro:**

  - Applicabile solo agli utenti Snowflake.

  - Dipende da un'applicazione specifica del Marketplace.

  - Meno trasparenza sul meccanismo esatto di gestione dei file GSB
    (probabilmente gestito internamente dall'app).

**Tabella Comparativa delle Soluzioni Alternative**

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
<th><strong>Caratteristica</strong></th>
<th><strong>UDF Spark (pyproj)</strong></th>
<th><strong>UDF Spark (GDAL Python)</strong></th>
<th><strong>ogr2ogr Esterno</strong></th>
<th><strong>SedonaSnow App (Snowflake)</strong></th>
</tr>
<tr>
<th><strong>Integrazione Spark</strong></th>
<th>Alta</th>
<th>Alta</th>
<th>Bassa (passo separato)</th>
<th>N/A (Specifico Snowflake)</th>
</tr>
<tr>
<th><strong>Complessità Impl.</strong></th>
<th>Media (UDF, deps, GSB)</th>
<th>Media (UDF, deps, GSB)</th>
<th>Bassa (script ogr2ogr)</th>
<th>Bassa (Installazione App)</th>
</tr>
<tr>
<th><strong>Dipendenze Worker</strong></th>
<th>pyproj, PROJ, GSB files</th>
<th>gdal, PROJ, GSB files</th>
<th>Nessuna (solo dove gira ogr2ogr)</th>
<th>SedonaSnow App</th>
</tr>
<tr>
<th><strong>Gestione File GSB</strong></th>
<th>Distribuzione + PROJ_LIB sui worker</th>
<th>Distribuzione + PROJ_LIB sui worker</th>
<th>PROJ_LIB dove gira ogr2ogr</th>
<th>Gestita internamente dall'app</th>
</tr>
<tr>
<th><strong>Performance Potenziale</strong></th>
<th>Media (overhead UDF Python)</th>
<th>Media (overhead UDF Python)</th>
<th>Alta (GDAL C++)</th>
<th>Potenzialmente Alta (Nativa)</th>
</tr>
<tr>
<th><strong>Manutenibilità</strong></th>
<th>Media (deps, UDF)</th>
<th>Media (deps, UDF)</th>
<th>Media (script, orchestrazione)</th>
<th>Bassa (gestita da vendor)</th>
</tr>
<tr>
<th><strong>Flessibilità</strong></th>
<th>Alta</th>
<th>Alta</th>
<th>Media (limitata a ogr2ogr)</th>
<th>Bassa (legata a Snowflake)</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

La scelta della soluzione alternativa più adatta dipende dal contesto
specifico. Le UDF offrono la massima integrazione ma presentano sfide di
deployment e potenziali colli di bottiglia prestazionali. L'elaborazione
esterna con ogr2ogr può essere più performante e isolare le dipendenze,
ma richiede un passo aggiuntivo nel workflow. Per gli utenti Snowflake,
l'app SedonaSnow rappresenta un'opzione dedicata.

**VII. Conclusioni e Raccomandazioni**

L'analisi condotta sulla documentazione ufficiale di Apache Sedona,
sulle risorse della comunità e sulle librerie sottostanti porta a
concludere che la funzione ST\_Transform, nelle sue implementazioni
standard per Apache Spark e Apache Flink, **non fornisce supporto
diretto** per l'utilizzo di file di grigliati di spostamento (GSB, NTv2)
tramite parametri specifici o stringhe PROJ avanzate.

- **Mancanza di Supporto Diretto:** Nonostante la libreria GeoTools, su
  cui Sedona si basa <sup>14</sup>, sia capace di eseguire
  trasformazioni basate su griglia <sup>22</sup>, l'interfaccia della
  funzione ST\_Transform esposta in Sedona per Spark/Flink non include i
  parametri necessari (come percorsi ai file GSB, direttive +nadgrids o
  codici EPSG per specifiche pipeline di trasformazione) per invocare e
  controllare queste operazioni.<sup>1</sup> Questa limitazione è
  confermata dall'assenza di documentazione in merito e dalla mancanza
  di discussioni o segnalazioni specifiche nella comunità.<sup>8</sup>
  L'eccezione notevole è l'ambiente Snowflake, dove l'applicazione
  SedonaSnow sembra abilitare tali trasformazioni <sup>26</sup>,
  suggerendo una capacità latente nel core ma non esposta
  universalmente.

- **Necessità di Soluzioni Alternative:** Gli utenti che richiedono la
  precisione offerta dalle trasformazioni basate su griglia GSB
  all'interno di un ambiente Spark/Sedona devono implementare soluzioni
  alternative.

**Azioni Raccomandate:**

1.  **Utilizzo di UDF Spark con pyproj:** Per gli utenti che
    preferiscono mantenere l'elaborazione interamente all'interno di
    Spark, si raccomanda l'implementazione di una User-Defined Function
    (UDF) Python che utilizzi la libreria pyproj.

    - **Requisiti:** Installazione di pyproj su tutti i nodi worker;
      distribuzione dei file.gsb necessari sui worker; configurazione
      della variabile d'ambiente PROJ\_LIB sui worker affinché PROJ
      possa localizzare i file di griglia.

    - **Vantaggi:** Integrazione nel flusso Spark; flessibilità.

    - **Svantaggi:** Complessità di setup (dipendenze, distribuzione
      file GSB, configurazione PROJ\_LIB); potenziale overhead
      prestazionale delle UDF Python su grandi volumi di dati.

2.  **Pre-elaborazione con ogr2ogr:** Per scenari dove le prestazioni
    sono critiche o si preferisce isolare le dipendenze complesse, si
    raccomanda di eseguire la trasformazione GSB come passo di
    pre-elaborazione utilizzando l'utility ogr2ogr di GDAL.

    - **Workflow:** ogr2ogr legge i dati sorgente, applica la
      trasformazione (invocando PROJ, che userà i file GSB se PROJ\_LIB
      è configurata) e scrive i dati trasformati in un formato (es.
      GeoParquet <sup>49</sup>) leggibile da Sedona.

    - **Vantaggi:** Sfrutta l'implementazione C++ ottimizzata di
      GDAL/PROJ; isola le dipendenze complesse; potenzialmente più
      performante per grandi trasformazioni batch.

    - **Svantaggi:** Richiede un passo ETL aggiuntivo; necessita di
      orchestrazione esterna; potrebbe richiedere storage intermedio.

3.  **Valutazione di SedonaSnow (per utenti Snowflake):** Gli utenti che
    operano nell'ecosistema Snowflake dovrebbero valutare l'utilizzo
    dell'applicazione SedonaSnow Native App, che, secondo la
    documentazione della community Snowflake <sup>26</sup>, abilita
    trasformazioni basate su griglia tramite la sua versione di
    ST\_Transform.

Prospettive Future:

Sebbene attualmente non supportato direttamente, è possibile che future
versioni di Apache Sedona possano esporre un controllo più granulare
sulle pipeline di trasformazione di GeoTools/PROJ, potenzialmente
abilitando il supporto per GSB o la selezione esplicita di
trasformazioni (come discusso in 10). Tuttavia, allo stato attuale, le
soluzioni alternative rimangono l'unica via praticabile per ottenere
trasformazioni basate su GSB nell'ambiente standard Spark/Flink con
Sedona.

**VIII. Riferimenti**

<sup>1</sup>

- **Documentazione Apache Sedona:**
  [<u>https://sedona.apache.org/</u>](https://sedona.apache.org/)

- **Documentazione GeoTools:**
  [<u>https://geotools.org/</u>](https://geotools.org/)

- **Documentazione PROJ:** [<u>https://proj.org/</u>](https://proj.org/)

- **Documentazione pyproj:**
  [<u>https://pyproj4.github.io/pyproj/stable/</u>](https://pyproj4.github.io/pyproj/stable/)

- **Documentazione GDAL:** [<u>https://gdal.org/</u>](https://gdal.org/)

- **Documentazione PostGIS
  ST\_Transform:**([<u>https://postgis.net/docs/ST\_Transform.html</u>](https://postgis.net/docs/ST_Transform.html))

- **Issue GitHub Sedona \#1397:**
  [<u>https://github.com/apache/sedona/issues/1397</u>](https://github.com/apache/sedona/issues/1397)

- **Articolo Community Snowflake su
  ST\_TRANSFORM:**([<u>https://community.snowflake.com/s/article/100405-P0000-Failed-to-transform-the-coordinates-from-SRID-to-another-when-using-ST-TRANSFORM-function</u>](https://community.snowflake.com/s/article/100405-P0000-Failed-to-transform-the-coordinates-from-SRID-to-another-when-using-ST-TRANSFORM-function))

#### Bibliografia

1.  Function - Apache Sedona™, accesso eseguito il giorno aprile 23,
    2025,
    [<u>https://sedona.apache.org/latest/api/sql/Function/</u>](https://sedona.apache.org/latest/api/sql/Function/)

2.  Function - Apache Sedona™, accesso eseguito il giorno aprile 23,
    2025,
    [<u>https://sedona.apache.org/1.6.0/api/sql/Function/</u>](https://sedona.apache.org/1.6.0/api/sql/Function/)

3.  Function - Apache Sedona™, accesso eseguito il giorno aprile 23,
    2025,
    [<u>https://sedona.apache.org/1.4.1/api/sql/Function/</u>](https://sedona.apache.org/1.4.1/api/sql/Function/)

4.  Function - Apache Sedona™, accesso eseguito il giorno aprile 23,
    2025,
    [<u>https://sedona.apache.org/1.5.0/api/sql/Function/</u>](https://sedona.apache.org/1.5.0/api/sql/Function/)

5.  Function - Apache Sedona™ (incubating), accesso eseguito il giorno
    aprile 23, 2025,
    [<u>https://sedona.apache.org/1.3.1-incubating/api/sql/Function/</u>](https://sedona.apache.org/1.3.1-incubating/api/sql/Function/)

6.  Function (Flink) - Apache Sedona™, accesso eseguito il giorno aprile
    23, 2025,
    [<u>https://sedona.apache.org/latest/api/flink/Function/</u>](https://sedona.apache.org/latest/api/flink/Function/)

7.  Function (Snowflake) - Apache Sedona™, accesso eseguito il giorno
    aprile 23, 2025,
    [<u>https://sedona.apache.org/latest/api/snowflake/vector-data/Function/</u>](https://sedona.apache.org/latest/api/snowflake/vector-data/Function/)

8.  Issues · apache/sedona - GitHub, accesso eseguito il giorno aprile
    23, 2025,
    [<u>https://github.com/apache/sedona/issues</u>](https://github.com/apache/sedona/issues)

9.  sedona/docs/api/sql/Function.md at master · apache/sedona - GitHub,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://github.com/apache/sedona/blob/master/docs/api/sql/Function.md</u>](https://github.com/apache/sedona/blob/master/docs/api/sql/Function.md)

10. Specify custom transformation parameters/wkt string from
    CoordinateSystem A til CoordinateSystem B. · Issue \#1397 ·
    apache/sedona - GitHub, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://github.com/apache/sedona/issues/1397</u>](https://github.com/apache/sedona/issues/1397)

11. CDN grid st\_transform() problems with Windows and macOS · Issue
    \#1815 · r-spatial/sf, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://github.com/r-spatial/sf/issues/1815</u>](https://github.com/r-spatial/sf/issues/1815)

12. apache-sedona error while trying to convert to pandas - Stack
    Overflow, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://stackoverflow.com/questions/75820616/apache-sedona-error-while-trying-to-convert-to-pandas</u>](https://stackoverflow.com/questions/75820616/apache-sedona-error-while-trying-to-convert-to-pandas)

13. How do you project geometries from one EPSG to another with
    Spark/Geomesa?, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://stackoverflow.com/questions/62558462/how-do-you-project-geometries-from-one-epsg-to-another-with-spark-geomesa</u>](https://stackoverflow.com/questions/62558462/how-do-you-project-geometries-from-one-epsg-to-another-with-spark-geomesa)

14. Working with Apache Sedona | Delta Lake, accesso eseguito il giorno
    aprile 23, 2025,
    [<u>https://delta.io/blog/apache-sedona/</u>](https://delta.io/blog/apache-sedona/)

15. Apache Sedona Version Issues - pyspark - Stack Overflow, accesso
    eseguito il giorno aprile 23, 2025,
    [<u>https://stackoverflow.com/questions/78227990/apache-sedona-version-issues</u>](https://stackoverflow.com/questions/78227990/apache-sedona-version-issues)

16. GeoSpatial with SparkSQL/Python in Synapse Spark Pool using
    apache-sedona?, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://learn.microsoft.com/en-sg/answers/questions/841928/geospatial-with-sparksql-python-in-synapse-spark-p</u>](https://learn.microsoft.com/en-sg/answers/questions/841928/geospatial-with-sparksql-python-in-synapse-spark-p)

17. Read Geojson file using Sedona Context in Databric... - Databricks
    Community, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://community.databricks.com/t5/data-engineering/read-geojson-file-using-sedona-context-in-databricks/td-p/93228</u>](https://community.databricks.com/t5/data-engineering/read-geojson-file-using-sedona-context-in-databricks/td-p/93228)

18. geotools-wrapper - org.datasyslab - Maven Central - Sonatype,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://central.sonatype.com/artifact/org.datasyslab/geotools-wrapper</u>](https://central.sonatype.com/artifact/org.datasyslab/geotools-wrapper)

19. Release notes - Apache Sedona™, accesso eseguito il giorno aprile
    23, 2025,
    [<u>https://sedona.apache.org/1.4.1/setup/release-notes/</u>](https://sedona.apache.org/1.4.1/setup/release-notes/)

20. Spatial SQL app - Apache Sedona™, accesso eseguito il giorno aprile
    23, 2025,
    [<u>https://sedona.apache.org/latest/tutorial/sql/</u>](https://sedona.apache.org/latest/tutorial/sql/)

21. Apache Sedona pyspark version issues - python - Stack Overflow,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://stackoverflow.com/questions/79076235/apache-sedona-pyspark-version-issues</u>](https://stackoverflow.com/questions/79076235/apache-sedona-pyspark-version-issues)

22. NADCONTransform (Geotools modules 32-SNAPSHOT API), accesso eseguito
    il giorno aprile 23, 2025,
    [<u>https://docs.geotools.org/stable/javadocs/org/geotools/referencing/operation/transform/NADCONTransform.html</u>](https://docs.geotools.org/stable/javadocs/org/geotools/referencing/operation/transform/NADCONTransform.html)

23. Specifying EPSG transformation method in GeoTools? - GIS
    StackExchange, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://gis.stackexchange.com/questions/313512/specifying-epsg-transformation-method-in-geotools</u>](https://gis.stackexchange.com/questions/313512/specifying-epsg-transformation-method-in-geotools)

24. GeoTools/jGridShift reports gsb files as invalid · Issue \#6 ·
    icsm-au/transformation\_grids, accesso eseguito il giorno aprile 23,
    2025,
    [<u>https://github.com/icsm-au/transformation\_grids/issues/6</u>](https://github.com/icsm-au/transformation_grids/issues/6)

25. Use high precision to convert image from one EPSG defined CRS to
    another - Geographic Information Systems Stack Exchange - GIS
    StackExchange, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://gis.stackexchange.com/questions/349062/use-high-precision-to-convert-image-from-one-epsg-defined-crs-to-another</u>](https://gis.stackexchange.com/questions/349062/use-high-precision-to-convert-image-from-one-epsg-defined-crs-to-another)

26. Query using ST\_TRANSFORM() function fails with "failed to transform
    coordinates from SRID" error - Snowflake Community, accesso eseguito
    il giorno aprile 23, 2025,
    [<u>https://community.snowflake.com/s/article/100405-P0000-Failed-to-transform-the-coordinates-from-SRID-to-another-when-using-ST-TRANSFORM-function</u>](https://community.snowflake.com/s/article/100405-P0000-Failed-to-transform-the-coordinates-from-SRID-to-another-when-using-ST-TRANSFORM-function)

27. Apache Sedona™, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://sedona.apache.org/</u>](https://sedona.apache.org/)

28. Overview - Apache Sedona™, accesso eseguito il giorno aprile 23,
    2025,
    [<u>https://sedona.apache.org/1.6.1/setup/overview/</u>](https://sedona.apache.org/1.6.1/setup/overview/)

29. Release notes - Apache Sedona™ (incubating), accesso eseguito il
    giorno aprile 23, 2025,
    [<u>https://sedona.apache.org/1.3.0-incubating/setup/release-notes/</u>](https://sedona.apache.org/1.3.0-incubating/setup/release-notes/)

30. Function - Apache Sedona™, accesso eseguito il giorno aprile 23,
    2025,
    [<u>https://sedona.apache.org/1.4.1/api/flink/Function/</u>](https://sedona.apache.org/1.4.1/api/flink/Function/)

31. Release notes - Apache Sedona™, accesso eseguito il giorno aprile
    23, 2025,
    [<u>https://sedona.apache.org/1.5.0/setup/release-notes/</u>](https://sedona.apache.org/1.5.0/setup/release-notes/)

32. Release notes - Apache Sedona™, accesso eseguito il giorno aprile
    23, 2025,
    [<u>https://sedona.apache.org/1.6.1/setup/release-notes/</u>](https://sedona.apache.org/1.6.1/setup/release-notes/)

33. Releases · apache/sedona - GitHub, accesso eseguito il giorno aprile
    23, 2025,
    [<u>https://github.com/apache/incubator-sedona/releases</u>](https://github.com/apache/incubator-sedona/releases)

34. ST\_Transform - PostGIS, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://postgis.net/docs/ST\_Transform.html</u>](https://postgis.net/docs/ST_Transform.html)

35. Use NTv2 grid files in PostGIS ST\_Transform - GIS StackExchange,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://gis.stackexchange.com/questions/310567/use-ntv2-grid-files-in-postgis-st-transform</u>](https://gis.stackexchange.com/questions/310567/use-ntv2-grid-files-in-postgis-st-transform)

36. Release notes - Apache Sedona™, accesso eseguito il giorno aprile
    23, 2025,
    [<u>https://sedona.apache.org/1.5.1/setup/release-notes/</u>](https://sedona.apache.org/1.5.1/setup/release-notes/)

37. Release notes - Apache Sedona™, accesso eseguito il giorno aprile
    23, 2025,
    [<u>https://sedona.apache.org/latest/setup/release-notes/</u>](https://sedona.apache.org/latest/setup/release-notes/)

38. Apache Iceberg - Project Nessie: Transactional Catalog for Data
    Lakes with Git-like semantics, accesso eseguito il giorno aprile 23,
    2025,
    [<u>https://projectnessie.org/iceberg/iceberg/</u>](https://projectnessie.org/iceberg/iceberg/)

39. Parameter - Apache Sedona™ (incubating), accesso eseguito il giorno
    aprile 23, 2025,
    [<u>https://sedona.apache.org/1.3.1-incubating/archive/api/sql/GeoSparkSQL-Parameter/</u>](https://sedona.apache.org/1.3.1-incubating/archive/api/sql/GeoSparkSQL-Parameter/)

40. Release notes - Apache Sedona™ (incubating), accesso eseguito il
    giorno aprile 23, 2025,
    [<u>https://sedona.apache.org/1.2.1-incubating/setup/release-notes/</u>](https://sedona.apache.org/1.2.1-incubating/setup/release-notes/)

41. Constructor - Apache Sedona™ (incubating), accesso eseguito il
    giorno aprile 23, 2025,
    [<u>https://sedona.apache.org/1.3.1-incubating/api/sql/Constructor/</u>](https://sedona.apache.org/1.3.1-incubating/api/sql/Constructor/)

42. 12186 (extend projection support in josm core) - OpenStreetMap,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://josm.openstreetmap.de/ticket/12186</u>](https://josm.openstreetmap.de/ticket/12186)

43. PostGIS 3.2.0beta3 Manual - OSGeo Download, accesso eseguito il
    giorno aprile 23, 2025,
    [<u>https://download.osgeo.org/postgis/docs/postgis-3.2.0beta3.pdf</u>](https://download.osgeo.org/postgis/docs/postgis-3.2.0beta3.pdf)

44. ogr2ogr — GDAL documentation, accesso eseguito il giorno aprile 23,
    2025,
    [<u>https://gdal.org/en/stable/programs/ogr2ogr.html</u>](https://gdal.org/en/stable/programs/ogr2ogr.html)

45. Ogr2ogr Basics Cheat Sheet - April 20, 2025 - Mapscaping.com,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://mapscaping.com/ogr2ogr-basics-cheat-sheet/</u>](https://mapscaping.com/ogr2ogr-basics-cheat-sheet/)

46. How to specify transformation method when using ogr2ogr to reproject
    geometry?, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://gis.stackexchange.com/questions/290148/how-to-specify-transformation-method-when-using-ogr2ogr-to-reproject-geometry</u>](https://gis.stackexchange.com/questions/290148/how-to-specify-transformation-method-when-using-ogr2ogr-to-reproject-geometry)

47. OGR2OGR Cheatsheet - Boston GIS, accesso eseguito il giorno aprile
    23, 2025,
    [<u>http://www.bostongis.com/printerfriendly.aspx?content\_name=ogr\_cheatsheet</u>](http://www.bostongis.com/printerfriendly.aspx?content_name=ogr_cheatsheet)

48. Using ogr2ogr to convert data between GeoJSON, PostGIS and Esri
    Shapefile, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://morphocode.com/using-ogr2ogr-convert-data-formats-geojson-postgis-esri-geodatabase-shapefiles/</u>](https://morphocode.com/using-ogr2ogr-convert-data-formats-geojson-postgis-esri-geodatabase-shapefiles/)

49. Geoparquet: Geospatial vector Data using Apache Parquet - bert -
    WordPress.com, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://bertt.wordpress.com/2022/12/20/geoparquet-geospatial-vector-data-using-apache-parquet/</u>](https://bertt.wordpress.com/2022/12/20/geoparquet-geospatial-vector-data-using-apache-parquet/)

50. ogr2ogr: encoding issues when importing from Oracle Spatial to
    PostGIS, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://gis.stackexchange.com/questions/189472/ogr2ogr-encoding-issues-when-importing-from-oracle-spatial-to-postgis</u>](https://gis.stackexchange.com/questions/189472/ogr2ogr-encoding-issues-when-importing-from-oracle-spatial-to-postgis)

51. Using ogr2ogr to export an Oracle Spatial table with measured
    geometries (3302) to a shapefile ignores the measure values -
    Geographic Information Systems Stack Exchange - GIS StackExchange,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://gis.stackexchange.com/questions/364942/using-ogr2ogr-to-export-an-oracle-spatial-table-with-measured-geometries-3302</u>](https://gis.stackexchange.com/questions/364942/using-ogr2ogr-to-export-an-oracle-spatial-table-with-measured-geometries-3302)

52. PostgreSQL / PostGIS — GDAL documentation, accesso eseguito il
    giorno aprile 23, 2025,
    [<u>https://gdal.org/en/stable/drivers/vector/pg.html</u>](https://gdal.org/en/stable/drivers/vector/pg.html)

53. How to speed up appending to PostGIS tables with ogr2ogr - Robin's
    Blog, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://blog.rtwilson.com/how-to-speed-up-appending-to-postgis-tables-with-ogr2ogr/</u>](https://blog.rtwilson.com/how-to-speed-up-appending-to-postgis-tables-with-ogr2ogr/)

54. ogr2ogr filegdb to postgis change geometry column and SRID - GIS
    StackExchange, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://gis.stackexchange.com/questions/233997/ogr2ogr-filegdb-to-postgis-change-geometry-column-and-srid</u>](https://gis.stackexchange.com/questions/233997/ogr2ogr-filegdb-to-postgis-change-geometry-column-and-srid)

55. Spatial database architecture with Apache Parquet, PostgresSQL and
    PostGIS on on-premises bare-metal S3/MinIo cluster - Stack Overflow,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://stackoverflow.com/questions/72226505/spatial-database-architecture-with-apache-parquet-postgressql-and-postgis-on-on</u>](https://stackoverflow.com/questions/72226505/spatial-database-architecture-with-apache-parquet-postgressql-and-postgis-on-on)

56. (Geo)Parquet — GDAL documentation, accesso eseguito il giorno aprile
    23, 2025,
    [<u>https://gdal.org/en/stable/drivers/vector/parquet.html</u>](https://gdal.org/en/stable/drivers/vector/parquet.html)

57. Spatial File Format conversion using OGR2OGR | GDAL/OGR Tutorial -
    YouTube, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://www.youtube.com/watch?v=qFJ7nZ246yM</u>](https://www.youtube.com/watch?v=qFJ7nZ246yM)

58. GeoParquet - Apache Sedona™, accesso eseguito il giorno aprile 23,
    2025,
    [<u>https://sedona.apache.org/1.7.0/tutorial/files/geoparquet-sedona-spark/</u>](https://sedona.apache.org/1.7.0/tutorial/files/geoparquet-sedona-spark/)

59. Mastering Reliable Apache Airflow Deployment with Kubernetes -
    Toolify.ai, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://www.toolify.ai/ai-news/mastering-reliable-apache-airflow-deployment-with-kubernetes-179251</u>](https://www.toolify.ai/ai-news/mastering-reliable-apache-airflow-deployment-with-kubernetes-179251)

60. How to best run Apache Airflow tasks on a Kubernetes cluster? -
    Stack Overflow, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://stackoverflow.com/questions/50926418/how-to-best-run-apache-airflow-tasks-on-a-kubernetes-cluster</u>](https://stackoverflow.com/questions/50926418/how-to-best-run-apache-airflow-tasks-on-a-kubernetes-cluster)

61. Use the KubernetesPodOperator | Cloud Composer, accesso eseguito il
    giorno aprile 23, 2025,
    [<u>https://cloud.google.com/composer/docs/composer-3/use-kubernetes-pod-operator</u>](https://cloud.google.com/composer/docs/composer-3/use-kubernetes-pod-operator)

62. How to efficiently access files with GDAL from an S3 bucket using
    VSIS3?, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://gis.stackexchange.com/questions/201831/how-to-efficiently-access-files-with-gdal-from-an-s3-bucket-using-vsis3</u>](https://gis.stackexchange.com/questions/201831/how-to-efficiently-access-files-with-gdal-from-an-s3-bucket-using-vsis3)

63. Apache Airflow KubernetesPodOperator: A Comprehensive Guide -
    SparkCodehub, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://www.sparkcodehub.com/airflow/operators/kubernetes-pod-operator</u>](https://www.sparkcodehub.com/airflow/operators/kubernetes-pod-operator)

64. Mastering Apache Airflow KubernetesExecutor: A Comprehensive Guide
    to Scalable, Isolated Task Execution - SparkCodehub, accesso
    eseguito il giorno aprile 23, 2025,
    [<u>https://www.sparkcodehub.com/apache-airflow-kubernetes-executor</u>](https://www.sparkcodehub.com/apache-airflow-kubernetes-executor)

65. Best practices for orchestrating MLOps pipelines with Airflow |
    Astronomer Documentation, accesso eseguito il giorno aprile 23,
    2025,
    [<u>https://www.astronomer.io/docs/learn/airflow-mlops/</u>](https://www.astronomer.io/docs/learn/airflow-mlops/)

66. Best Practices - Apache Airflow, accesso eseguito il giorno aprile
    23, 2025,
    [<u>https://airflow.apache.org/docs/apache-airflow/2.4.0/best-practices.html</u>](https://airflow.apache.org/docs/apache-airflow/2.4.0/best-practices.html)

67. KubernetesPodOperator — apache-airflow-providers-cncf-kubernetes
    Documentation, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html</u>](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html)

68. What is the best practice to setup service network inside the DAG? ·
    apache airflow · Discussion \#27218 - GitHub, accesso eseguito il
    giorno aprile 23, 2025,
    [<u>https://github.com/apache/airflow/discussions/27218</u>](https://github.com/apache/airflow/discussions/27218)

69. airflow logging to S3 · Issue \#34 · airflow-helm/charts - GitHub,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://github.com/airflow-helm/charts/issues/34</u>](https://github.com/airflow-helm/charts/issues/34)

70. Error when migrating gdal function proximity to aws s3 - GIS
    StackExchange, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://gis.stackexchange.com/questions/485013/error-when-migrating-gdal-function-proximity-to-aws-s3</u>](https://gis.stackexchange.com/questions/485013/error-when-migrating-gdal-function-proximity-to-aws-s3)

71. writeRaster to an S3 destination through GDAL fails · Issue \#1209 ·
    rspatial/terra - GitHub, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://github.com/rspatial/terra/issues/1209</u>](https://github.com/rspatial/terra/issues/1209)

72. Improving performance when importing file geodatabase into
    PostgreSQL?, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://gis.stackexchange.com/questions/172690/improving-performance-when-importing-file-geodatabase-into-postgresql</u>](https://gis.stackexchange.com/questions/172690/improving-performance-when-importing-file-geodatabase-into-postgresql)

73. Configuration options — GDAL documentation, accesso eseguito il
    giorno aprile 23, 2025,
    [<u>https://gdal.org/en/stable/user/configoptions.html</u>](https://gdal.org/en/stable/user/configoptions.html)

74. Configuration options - gdalcubes, accesso eseguito il giorno aprile
    23, 2025,
    [<u>https://gdalcubes.github.io/source/concepts/config.html</u>](https://gdalcubes.github.io/source/concepts/config.html)

75. Setting Config Options for GDAL using Python - GIS StackExchange,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://gis.stackexchange.com/questions/378199/setting-config-options-for-gdal-using-python</u>](https://gis.stackexchange.com/questions/378199/setting-config-options-for-gdal-using-python)

76. \[gdal-dev\] How to improve gdal\_rasterize perfomance?, accesso
    eseguito il giorno aprile 23, 2025,
    [<u>https://gdal-dev.osgeo.narkive.com/5Y7lxhnU/how-to-improve-gdal-rasterize-perfomance</u>](https://gdal-dev.osgeo.narkive.com/5Y7lxhnU/how-to-improve-gdal-rasterize-perfomance)

77. GDAL Config Quick Reference - CRAN, accesso eseguito il giorno
    aprile 23, 2025,
    [<u>https://cran.r-project.org/web/packages/gdalraster/vignettes/gdal-config-quick-ref.html</u>](https://cran.r-project.org/web/packages/gdalraster/vignettes/gdal-config-quick-ref.html)

78. How can I improve performance of gdalwarp and gdal\_translate
    pipeline?, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://gis.stackexchange.com/questions/360162/how-can-i-improve-performance-of-gdalwarp-and-gdal-translate-pipeline</u>](https://gis.stackexchange.com/questions/360162/how-can-i-improve-performance-of-gdalwarp-and-gdal-translate-pipeline)

79. spatialx-project/geolake: Universal solution for geospatial data
    tailored to data lakehouse systems for the first time in the
    industry - GitHub, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://github.com/spatialx-project/geolake</u>](https://github.com/spatialx-project/geolake)

80. (PDF) GeoLake: Bringing Geospatial Support to Lakehouses -
    ResearchGate, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://www.researchgate.net/publication/376632924\_GeoLake\_Bringing\_Geospatial\_Support\_to\_Lakehouses</u>](https://www.researchgate.net/publication/376632924_GeoLake_Bringing_Geospatial_Support_to_Lakehouses)

81. Compile the code - Apache Sedona™, accesso eseguito il giorno aprile
    23, 2025,
    [<u>https://sedona.apache.org/1.5.1/setup/compile/</u>](https://sedona.apache.org/1.5.1/setup/compile/)

82. Communication and Support — GeoTools 34-SNAPSHOT User Guide, accesso
    eseguito il giorno aprile 23, 2025,
    [<u>https://docs.geotools.org/latest/userguide/welcome/support.html</u>](https://docs.geotools.org/latest/userguide/welcome/support.html)

83. Vector grids — GeoTools 32-SNAPSHOT User Guide, accesso eseguito il
    giorno aprile 23, 2025,
    [<u>https://docs.geotools.org/stable/userguide.old/extension/grid.html</u>](https://docs.geotools.org/stable/userguide.old/extension/grid.html)

84. PostGIS 3.4.4 Manual - OSGeo Download, accesso eseguito il giorno
    aprile 23, 2025,
    [<u>http://download.osgeo.org/postgis/docs/postgis-3.4.4-en.pdf</u>](http://download.osgeo.org/postgis/docs/postgis-3.4.4-en.pdf)

85. Interview with Kyle Barron on GeoArrow and GeoParquet, and the
    Future of Geospatial Data Analysis, accesso eseguito il giorno
    aprile 23, 2025,
    [<u>https://cloudnativegeo.org/blog/2024/12/interview-with-kyle-barron-on-geoarrow-and-geoparquet-and-the-future-of-geospatial-data-analysis/</u>](https://cloudnativegeo.org/blog/2024/12/interview-with-kyle-barron-on-geoarrow-and-geoparquet-and-the-future-of-geospatial-data-analysis/)

86. How Geospatial Data Lakes Will Change Everything (And No One's
    Talking About It), accesso eseguito il giorno aprile 23, 2025,
    [<u>https://www.youtube.com/watch?v=r5OEhc1ghX8</u>](https://www.youtube.com/watch?v=r5OEhc1ghX8)

87. GeoParquet Example - Cloud-Optimized Geospatial Formats Guide,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://guide.cloudnativegeo.org/geoparquet/geoparquet-example.html</u>](https://guide.cloudnativegeo.org/geoparquet/geoparquet-example.html)

88. Introducing GeoParquet: Towards geospatial compatibility between
    Data Clouds - CARTO, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://carto.com/blog/introducing-geoparquet-geospatial-compatibility</u>](https://carto.com/blog/introducing-geoparquet-geospatial-compatibility)

89. How GeoParquet Enables Working With Geospatial Vector Data in the
    Cloud, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://www.geoweeknews.com/news/geoparquet-geospatial-vector-data-cloud-management-storage</u>](https://www.geoweeknews.com/news/geoparquet-geospatial-vector-data-cloud-management-storage)

90. Introducing the Geoparquet data format - GetInData, accesso eseguito
    il giorno aprile 23, 2025,
    [<u>https://getindata.com/blog/introducing-geoparquet-data-format/</u>](https://getindata.com/blog/introducing-geoparquet-data-format/)

91. Apache Iceberg and Parquet now support GEO - Wherobots, accesso
    eseguito il giorno aprile 23, 2025,
    [<u>https://wherobots.com/apache-iceberg-and-parquet-now-support-geo/</u>](https://wherobots.com/apache-iceberg-and-parquet-now-support-geo/)

92. Iceberg GEO: Technical Insights and Implementation Strategies,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://wherobots.com/blog/iceberg-geo-technical-insights-and-implementation-strategies/</u>](https://wherobots.com/blog/iceberg-geo-technical-insights-and-implementation-strategies/)

93. Apache Iceberg now supports geospatial data types natively - Hacker
    News, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://news.ycombinator.com/item?id=43020756</u>](https://news.ycombinator.com/item?id=43020756)

94. Searching the Spatial Data Lake: Bringing GeoParquet to Apache
    Lucene :: FOSS4G NA 2024, accesso eseguito il giorno aprile 23,
    2025,
    [<u>https://talks.osgeo.org/foss4g-na-2024/talk/JZNQHN/</u>](https://talks.osgeo.org/foss4g-na-2024/talk/JZNQHN/)

95. Geospatial Support · Issue \#10260 · apache/iceberg · GitHub,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://github.com/apache/iceberg/issues/10260</u>](https://github.com/apache/iceberg/issues/10260)

96. Embracing Geospatial as a Primary Data Type: A Call to Action for
    the Data Community, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://cloudnativegeo.org/blog/2024/07/embracing-geospatial-as-a-primary-data-type-a-call-to-action-for-the-data-community/</u>](https://cloudnativegeo.org/blog/2024/07/embracing-geospatial-as-a-primary-data-type-a-call-to-action-for-the-data-community/)

97. Add geometry type to iceberg · Issue \#2586 · apache/iceberg -
    GitHub, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://github.com/apache/iceberg/issues/2586</u>](https://github.com/apache/iceberg/issues/2586)

98. The Complete Guide to Cloud Optimized GeoTIFF (COG) - Atlas.co,
    accesso eseguito il giorno aprile 23, 2025,
    [<u>https://atlas.co/blog/the-complete-guide-to-cloud-optimized-geotiff-cog/</u>](https://atlas.co/blog/the-complete-guide-to-cloud-optimized-geotiff-cog/)

99. How to Make the Most of Apache Iceberg for Your Cloud Data Lakehouse
    | Informatica, accesso eseguito il giorno aprile 23, 2025,
    [<u>https://www.informatica.com/blogs/how-to-make-the-most-of-apache-iceberg-for-your-cloud-data-lakehouse.html.html.html.html.html.html.html</u>](https://www.informatica.com/blogs/how-to-make-the-most-of-apache-iceberg-for-your-cloud-data-lakehouse.html.html.html.html.html.html.html)

100. Developer's Guide to COG - Cloud Optimized GeoTIFF, accesso
     eseguito il giorno aprile 23, 2025,
     [<u>https://cogeo.org/developers-guide.html</u>](https://cogeo.org/developers-guide.html)

101. Cloud Optimized GeoTIFF, accesso eseguito il giorno aprile 23,
     2025, [<u>https://cogeo.org/</u>](https://cogeo.org/)

102. Apache Iceberg - Apache Iceberg™, accesso eseguito il giorno aprile
     23, 2025,
     [<u>https://iceberg.apache.org/</u>](https://iceberg.apache.org/)

103. Cloud Optimized GeoTIFF(COG):Create COG, Upload on AWS (S3) Bucket,
     Access through QGIS & OpenLayers - YouTube, accesso eseguito il
     giorno aprile 23, 2025,
     [<u>https://www.youtube.com/watch?v=IE\_5oBATJT0</u>](https://www.youtube.com/watch?v=IE_5oBATJT0)

104. What is the reason for using GeoServer to provide access to
     Cloud-Optimized GeoTIFFs, accesso eseguito il giorno aprile 23,
     2025,
     [<u>https://gis.stackexchange.com/questions/448891/what-is-the-reason-for-using-geoserver-to-provide-access-to-cloud-optimized-geot</u>](https://gis.stackexchange.com/questions/448891/what-is-the-reason-for-using-geoserver-to-provide-access-to-cloud-optimized-geot)

105. Building a Data Lakehouse with Amazon S3 and Dremio on Apache
     Iceberg Tables - AWS, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://aws.amazon.com/blogs/apn/building-a-data-lakehouse-with-amazon-s3-and-dremio-on-apache-iceberg-tables/</u>](https://aws.amazon.com/blogs/apn/building-a-data-lakehouse-with-amazon-s3-and-dremio-on-apache-iceberg-tables/)

106. How Apache Iceberg is Built for Open Optimized Performance -
     Dremio, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://www.dremio.com/blog/how-apache-iceberg-is-built-for-open-optimized-performance/</u>](https://www.dremio.com/blog/how-apache-iceberg-is-built-for-open-optimized-performance/)

107. Top Reasons to Attend the Subsurface Conference for Apache Iceberg
     Fans | Dremio, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://www.dremio.com/blog/top-reasons-to-attend-the-subsurface-conference-for-apache-iceberg-fans/</u>](https://www.dremio.com/blog/top-reasons-to-attend-the-subsurface-conference-for-apache-iceberg-fans/)

108. Dremio says it has dramatically improved query performance on
     Iceberg data lakes, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://siliconangle.com/2024/08/27/dremio-says-dramatically-improved-query-performance-iceberg-data-lakes/</u>](https://siliconangle.com/2024/08/27/dremio-says-dramatically-improved-query-performance-iceberg-data-lakes/)

109. How Z-Ordering in Apache Iceberg Helps Improve Performance |
     Dremio, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://www.dremio.com/blog/how-z-ordering-in-apache-iceberg-helps-improve-performance/</u>](https://www.dremio.com/blog/how-z-ordering-in-apache-iceberg-helps-improve-performance/)

110. Spec - Apache Iceberg™, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://iceberg.apache.org/spec/</u>](https://iceberg.apache.org/spec/)

111. Top 10 Query Engines for Apache Iceberg: A Complete Comparison -
     Estuary.dev, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://estuary.dev/blog/comparison-query-engines-for-apache-iceberg/</u>](https://estuary.dev/blog/comparison-query-engines-for-apache-iceberg/)

112. Why Trino is the PostgreSQL of analytics? - Starburst, accesso
     eseguito il giorno aprile 23, 2025,
     [<u>https://www.starburst.io/blog/trino-postgresql-analytics/</u>](https://www.starburst.io/blog/trino-postgresql-analytics/)

113. Use Apache Iceberg in a data lake to support incremental data
     processing - AWS, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://aws.amazon.com/blogs/big-data/use-apache-iceberg-in-a-data-lake-to-support-incremental-data-processing/</u>](https://aws.amazon.com/blogs/big-data/use-apache-iceberg-in-a-data-lake-to-support-incremental-data-processing/)

114. Optimizing Data Storage and Querying with Trino, MinIO, and Apache
     Iceberg | Upsolver, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://www.upsolver.com/blog/trino-minio-iceberg</u>](https://www.upsolver.com/blog/trino-minio-iceberg)

115. Exploring Global Internet Speeds using Apache Iceberg and
     ClickHouse, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://clickhouse.com/blog/exploring-global-internet-speeds-with-apache-iceberg-clickhouse</u>](https://clickhouse.com/blog/exploring-global-internet-speeds-with-apache-iceberg-clickhouse)

116. Apache Iceberg optimization: Solving the small files problem in
     Amazon EMR - AWS, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://aws.amazon.com/blogs/big-data/apache-iceberg-optimization-solving-the-small-files-problem-in-amazon-emr/</u>](https://aws.amazon.com/blogs/big-data/apache-iceberg-optimization-solving-the-small-files-problem-in-amazon-emr/)

117. Data Lakehouse Versioning Comparison: (Nessie, Apache Iceberg,
     LakeFS) - Dremio, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://www.dremio.com/blog/data-lakehouse-versioning-comparison-nessie-apache-iceberg-lakefs/</u>](https://www.dremio.com/blog/data-lakehouse-versioning-comparison-nessie-apache-iceberg-lakefs/)

118. Data as Code: Project Nessie brings a Git-like experience for
     Apache Iceberg Tables, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://www.youtube.com/watch?v=Gg6loPa\_L9Q</u>](https://www.youtube.com/watch?v=Gg6loPa_L9Q)

119. Project Nessie: Transactional Catalog for Data Lakes with Git-like
     semantics, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://projectnessie.org/</u>](https://projectnessie.org/)

120. Seeking Recommendations for Data Versioning and Change Tracking in
     Esri, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://community.esri.com/t5/data-management-questions/seeking-recommendations-for-data-versioning-and/td-p/1290950</u>](https://community.esri.com/t5/data-management-questions/seeking-recommendations-for-data-versioning-and/td-p/1290950)

121. Official Geospatial Support - Dremio Community, accesso eseguito il
     giorno aprile 23, 2025,
     [<u>https://community.dremio.com/t/official-geospatial-support/12447</u>](https://community.dremio.com/t/official-geospatial-support/12447)

122. Frequently Asked Questions - Icechunk, accesso eseguito il giorno
     aprile 23, 2025,
     [<u>https://icechunk.io/en/latest/faq/</u>](https://icechunk.io/en/latest/faq/)

123. Unlock raster analytics & visualizations - now in your lakehouse! -
     Carto, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://carto.com/blog/unlock-raster-analytics-visualizations-now-in-your-lakehouse</u>](https://carto.com/blog/unlock-raster-analytics-visualizations-now-in-your-lakehouse)

124. How To Use Cloud Optimized GeoTIFFs (COGs) | Vermont Center for
     Geographic Information, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://vcgi.vermont.gov/resources/how-and-education-resources/how-use-cloud-optimized-geotiffs-cogs</u>](https://vcgi.vermont.gov/resources/how-and-education-resources/how-use-cloud-optimized-geotiffs-cogs)

125. Raster Loaders - Wherobots Documentation, accesso eseguito il
     giorno aprile 23, 2025,
     [<u>https://docs.wherobots.com/latest/references/wherobotsdb/raster-data/Raster-loader/</u>](https://docs.wherobots.com/latest/references/wherobotsdb/raster-data/Raster-loader/)

126. Building a Spatial Data Lakehouse - Wherobots, accesso eseguito il
     giorno aprile 23, 2025,
     [<u>https://wherobots.com/building-a-spatial-data-lakehouse/</u>](https://wherobots.com/building-a-spatial-data-lakehouse/)

127. Optimizing read performance - AWS Prescriptive Guidance, accesso
     eseguito il giorno aprile 23, 2025,
     [<u>https://docs.aws.amazon.com/prescriptive-guidance/latest/apache-iceberg-on-aws/best-practices-read.html</u>](https://docs.aws.amazon.com/prescriptive-guidance/latest/apache-iceberg-on-aws/best-practices-read.html)

128. Iceberg GEO: Technical Insights and Implementation Strategies -
     Wherobots, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://wherobots.com/iceberg-geo-technical-insights-and-implementation-strategies/</u>](https://wherobots.com/iceberg-geo-technical-insights-and-implementation-strategies/)

129. Performance - Apache Iceberg™, accesso eseguito il giorno aprile
     23, 2025,
     [<u>https://iceberg.apache.org/docs/1.8.0/performance/</u>](https://iceberg.apache.org/docs/1.8.0/performance/)

130. Iceberg 101: Ten Tips to Optimize Performance - Upsolver, accesso
     eseguito il giorno aprile 23, 2025,
     [<u>https://www.upsolver.com/blog/optimize-iceberg-performance</u>](https://www.upsolver.com/blog/optimize-iceberg-performance)

131. The Ultimate Guide to Apache Iceberg - IOMETE, accesso eseguito il
     giorno aprile 23, 2025,
     [<u>https://iomete.com/the-ultimate-guide-to-apache-iceberg</u>](https://iomete.com/the-ultimate-guide-to-apache-iceberg)

132. Apache Iceberg | Dremio Documentation, accesso eseguito il giorno
     aprile 23, 2025,
     [<u>https://docs.dremio.com/cloud/sonar/query-manage/supported-data-formats/iceberg</u>](https://docs.dremio.com/cloud/sonar/query-manage/supported-data-formats/iceberg)

133. Apache Iceberg | Dremio Documentation, accesso eseguito il giorno
     aprile 23, 2025,
     [<u>https://docs.dremio.com/24.3.x/sonar/query-manage/data-formats/apache-iceberg/</u>](https://docs.dremio.com/24.3.x/sonar/query-manage/data-formats/apache-iceberg/)

134. Apache Iceberg: The Definitive Guide - Dremio, accesso eseguito il
     giorno aprile 23, 2025,
     [<u>https://www.dremio.com/wp-content/uploads/2023/02/apache-iceberg-TDG\_ER1.pdf</u>](https://www.dremio.com/wp-content/uploads/2023/02/apache-iceberg-TDG_ER1.pdf)

135. Leveraging Apache Iceberg Metadata Tables in Dremio for Effective
     Data Lakehouse Auditing, accesso eseguito il giorno aprile 23,
     2025,
     [<u>https://www.dremio.com/blog/apache-iceberg-metadata-tables/</u>](https://www.dremio.com/blog/apache-iceberg-metadata-tables/)

136. Dremio Unveils New Features to Enhance Apache Iceberg Data
     Lakehouse Performance, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://www.bigdatawire.com/2024/08/30/dremio-unveils-new-features-to-enhance-apache-iceberg-data-lakehouse-performance/</u>](https://www.bigdatawire.com/2024/08/30/dremio-unveils-new-features-to-enhance-apache-iceberg-data-lakehouse-performance/)

137. Introduction to Dremio Arctic: Catalog Versioning and Iceberg Table
     Optimization - YouTube, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://www.youtube.com/watch?v=6DT6YJZycpY</u>](https://www.youtube.com/watch?v=6DT6YJZycpY)

138. Iceberg Partitioning and Performance Optimizations in Trino -
     Starburst, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://www.starburst.io/blog/iceberg-partitioning-and-performance-optimizations-in-trino-partitioning/</u>](https://www.starburst.io/blog/iceberg-partitioning-and-performance-optimizations-in-trino-partitioning/)

139. Geospatial functions — Trino 474 Documentation, accesso eseguito il
     giorno aprile 23, 2025,
     [<u>https://trino.io/docs/current/functions/geospatial.html</u>](https://trino.io/docs/current/functions/geospatial.html)

140. Iceberg connector — Trino 474 Documentation, accesso eseguito il
     giorno aprile 23, 2025,
     [<u>https://trino.io/docs/current/connector/iceberg.html</u>](https://trino.io/docs/current/connector/iceberg.html)

141. Top 10 Query Engines for Apache Iceberg: A Complete Comparison -
     Estuary.dev, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://estuary.dev/comparison-query-engines-for-apache-iceberg/</u>](https://estuary.dev/comparison-query-engines-for-apache-iceberg/)

142. Wherobots and PostgreSQL + PostGIS: A Synergy in Spatial Analysis,
     accesso eseguito il giorno aprile 23, 2025,
     [<u>https://wherobots.com/blog/wherobots-postgresql-postgis-better-together/</u>](https://wherobots.com/blog/wherobots-postgresql-postgis-better-together/)

143. Creating an Iceberg table with a geometry column with Sedona -
     Stack Overflow, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://stackoverflow.com/questions/79564000/creating-an-iceberg-table-with-a-geometry-column-with-sedona</u>](https://stackoverflow.com/questions/79564000/creating-an-iceberg-table-with-a-geometry-column-with-sedona)

144. Iceberg Performance Benchmarks: Tabular, Snowflake, AWS Glue and
     Upsolver Compared, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://www.upsolver.com/blog/iceberg-performance-benchmark</u>](https://www.upsolver.com/blog/iceberg-performance-benchmark)

145. Nessie Catalog: Key Features, Use Cases & How to Use - lakeFS,
     accesso eseguito il giorno aprile 23, 2025,
     [<u>https://lakefs.io/blog/nessie-catalog/</u>](https://lakefs.io/blog/nessie-catalog/)

146. Best Practices - Project Nessie: Transactional Catalog for Data
     Lakes with Git-like semantics, accesso eseguito il giorno aprile
     23, 2025,
     [<u>https://projectnessie.org/guides/best-practices/</u>](https://projectnessie.org/guides/best-practices/)

147. What is Nessie, Catalog Versioning and Git-for-Data? - Dremio,
     accesso eseguito il giorno aprile 23, 2025,
     [<u>https://www.dremio.com/blog/what-is-nessie-catalog-versioning-and-git-for-data/</u>](https://www.dremio.com/blog/what-is-nessie-catalog-versioning-and-git-for-data/)

148. PROJ 6 drops +datum= specification; transform degraded in workflows
     · Issue \#1146 · r-spatial/sf - GitHub, accesso eseguito il giorno
     aprile 23, 2025,
     [<u>https://github.com/r-spatial/sf/issues/1146</u>](https://github.com/r-spatial/sf/issues/1146)

149. How to change the coordinate transformation function in Oracle? -
     GIS StackExchange, accesso eseguito il giorno aprile 23, 2025,
     [<u>https://gis.stackexchange.com/questions/292414/how-to-change-the-coordinate-transformation-function-in-oracle</u>](https://gis.stackexchange.com/questions/292414/how-to-change-the-coordinate-transformation-function-in-oracle)

150. GDAL Virtual File Systems (compressed, network hosted, etc...):
     /vsimem, /vsizip, /vsitar, /vsicurl, accesso eseguito il giorno
     aprile 23, 2025,
     [<u>https://lira.no-ip.org:8443/doc/libgdal-doc/gdal/gdal\_virtual\_file\_systems.html</u>](https://lira.no-ip.org:8443/doc/libgdal-doc/gdal/gdal_virtual_file_systems.html)

151. GDAL Virtual File Systems (compressed, network hosted, etc...):
     /vsimem, /vsizip, /vsitar, /vsicurl, accesso eseguito il giorno
     aprile 23, 2025,
     [<u>https://gdal.org/en/stable/user/virtual\_file\_systems.html</u>](https://gdal.org/en/stable/user/virtual_file_systems.html)

152. GDAL ogr2ogr is taking too long while importing OSM data to
     PostGIS - Stack Overflow, accesso eseguito il giorno aprile 23,
     2025,
     [<u>https://stackoverflow.com/questions/79049461/gdal-ogr2ogr-is-taking-too-long-while-importing-osm-data-to-postgis</u>](https://stackoverflow.com/questions/79049461/gdal-ogr2ogr-is-taking-too-long-while-importing-osm-data-to-postgis)
