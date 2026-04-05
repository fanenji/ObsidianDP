---
type: note
topic: data-platform
created: 2026-03-15
tags:
  - tools
  - kestra
---

# **Analisi Comparativa di Sistemi di Orchestrazione per Data Platform On-Premise su Kubernetes**

## **1. Sintesi Riepilogativa**

**Scopo Principale:** Il presente documento ha l'obiettivo di fornire
un'analisi tecnica comparativa approfondita dei sistemi di
orchestrazione open source per data platform, focalizzandosi
specificamente su soluzioni implementabili on-premise all'interno di
ambienti Kubernetes. Una valutazione centrale riguarda le capacità
native di autenticazione e autorizzazione di ciascuno strumento e le
possibilità di integrazione con meccanismi di sicurezza personalizzati o
esterni, al fine di supportare una decisione strategica informata.

**Principali Risultanze:** L'analisi ha rivelato che, sebbene tutti gli
strumenti esaminati siano open source e compatibili con Kubernetes per
l'installazione on-premise, le loro funzionalità native di
autenticazione e autorizzazione per ambienti self-hosted presentano
notevoli differenze. Funzionalità di livello enterprise, come il Single
Sign-On (SSO) completo e un Role-Based Access Control (RBAC) granulare,
spesso richiedono l'integrazione con sistemi esterni o sono
caratteristiche più mature nelle versioni commerciali o cloud dei
prodotti. La dicitura "open-source e on-premise" non implica
automaticamente la disponibilità di funzionalità di sicurezza complete e
pronte all'uso. La maggior parte degli orchestratori open source, quando
installati autonomamente, offre meccanismi di sicurezza di base ma si
affida a sistemi esterni o a configurazioni personalizzate significative
per un'autenticazione di livello enterprise (SSO tramite OIDC/SAML) e un
RBAC granulare. Questa constatazione rappresenta un fattore di
pianificazione critico per le implementazioni on-premise.

**Panoramica delle Principali Raccomandazioni:** Strumenti come Apache
Airflow, grazie a Flask AppBuilder, offrono opzioni di autenticazione
integrate più mature. Le soluzioni native per Kubernetes, quali Argo
Workflows e Flyte, sfruttano efficacemente il RBAC di Kubernetes per la
sicurezza dell'esecuzione e propongono OIDC per l'accesso alle API e
alle interfacce utente. Altri, come le versioni open source di Dagster e
Prefect, necessitano tipicamente di soluzioni basate su reverse-proxy
per un'autenticazione robusta delle UI/API. Temporal, d'altro canto,
offre un modello a plugin flessibile ma che richiede un maggiore impegno
di sviluppo per la personalizzazione della sicurezza.

**Compromessi Critici:** Emerge un compromesso fondamentale: gli
orchestratori con funzionalità di sicurezza integrate più ricche possono
presentare una curva di apprendimento più ripida o paradigmi
architetturali differenti. Al contrario, quelli con una sicurezza di
base più semplice richiedono un maggiore sforzo di integrazione esterna
e competenze specifiche per il consolidamento della sicurezza in
contesti on-premise. Le organizzazioni devono quindi considerare
l'investimento in termini di competenze e risorse necessarie per
integrare e gestire componenti di sicurezza esterni o sviluppare
soluzioni personalizzate. La scelta dell'orchestratore potrebbe essere
influenzata dalla facilità con cui si integra con l'infrastruttura di
sicurezza aziendale esistente.

## **2. Introduzione**

**Contesto:** Le data platform moderne sono diventate un pilastro
fondamentale per le organizzazioni che mirano a sfruttare i propri dati
per ottenere vantaggi competitivi. L'orchestrazione dei flussi di dati
(workflow) assume un ruolo critico nella gestione della complessità
intrinseca di tali piattaforme, specialmente in contesti di
installazione on-premise su infrastrutture Kubernetes. Questi ambienti
pongono sfide e requisiti specifici, tra cui la necessità di un
controllo granulare, una sicurezza robusta e un'integrazione trasparente
con i sistemi aziendali esistenti, motivazioni che spesso guidano la
scelta verso soluzioni on-premise.

**Scopo del Rapporto:** Il presente rapporto si propone di condurre
un'analisi comparativa dettagliata dei principali strumenti di
orchestrazione open source. La valutazione è mirata a determinarne
l'idoneità architetturale, le funzionalità specifiche per la gestione
dei dati, la facilità di implementazione e gestione all'interno di
cluster Kubernetes e, in modo preponderante, le capacità di
autenticazione e autorizzazione intrinseche ed estensibili, essenziali
per garantire un funzionamento sicuro in ambienti on-premise.

**Nota Metodologica:** L'analisi si basa su una revisione completa della
documentazione ufficiale, delle specifiche tecniche, delle discussioni
all'interno delle comunità di sviluppo (come issue GitHub e forum) e di
recensioni specialistiche. L'attenzione è rigorosamente rivolta alle
versioni open source e self-hosted degli strumenti, implementabili su
Kubernetes. Si escludono esplicitamente le funzionalità esclusive dei
servizi cloud gestiti dai vendor, a meno che non forniscano chiarimenti
sull'architettura o sulla filosofia della versione open source, o
evidenzino una significativa lacuna in quest'ultima.

**Promemoria su Ambito e Vincoli:** Si ribadiscono i vincoli
fondamentali della richiesta: licenza open source, capacità di
installazione on-premise obbligatoria (nessuna dipendenza da control
plane cloud gestiti dal vendor per le funzionalità di base) e
implementazione nativa o ben supportata su Kubernetes. Il nucleo
dell'analisi verterà sulla postura di sicurezza, con particolare enfasi
sui meccanismi di autenticazione e autorizzazione. Il vincolo
"on-premise Kubernetes" favorisce intrinsecamente gli strumenti che sono
nativi per Kubernetes o che dispongono di artefatti di deployment maturi
e ben mantenuti per Kubernetes (come chart Helm o Operator). La qualità
di tali artefatti influisce direttamente sulla complessità e
sull'affidabilità dell'installazione. Strumenti con una migliore
integrazione K8s tendono a offrire percorsi più diretti per sfruttare le
funzionalità di sicurezza native di K8s (come ServiceAccount,
NetworkPolicy, gestione dei Secret) e gli strumenti di monitoraggio,
potendo così ridurre l'onere operativo e migliorare la postura di
sicurezza complessiva.

## **3. Sistemi di Orchestrazione Candidati: Panoramica e Conformità ai Vincoli**

**Logica di Selezione:** La scelta dei sistemi di orchestrazione da
analizzare – Apache Airflow, Dagster, Prefect, Argo Workflows, Flyte,
Temporal e Luigi – è stata guidata dalla loro notorietà nella comunità
open source, dalla completezza delle funzionalità offerte per
l'orchestrazione di data platform e dal supporto documentato per
installazioni on-premise in ambienti Kubernetes.

**Introduzione agli Strumenti:**

- **Apache Airflow:** Originariamente sviluppato da Airbnb <sup>1</sup>,
  Airflow è una piattaforma matura per la creazione, la schedulazione e
  il monitoraggio programmatico di workflow complessi, definiti come
  Grafi Aciclici Diretti (DAG) in Python.<sup>2</sup> È ampiamente
  utilizzato per pipeline ETL, training di modelli ML e automazione di
  task infrastrutturali.

- **Dagster:** Dagster adotta un approccio "asset-centric",
  focalizzandosi sui dati prodotti e consumati dai workflow piuttosto
  che sui task stessi.<sup>2</sup> Scritto in Python, è progettato per
  l'intero ciclo di vita dello sviluppo dei dati, con enfasi su
  testabilità, osservabilità e integrazione con lo stack di dati
  moderno.

- **Prefect:** Prefect è un sistema di orchestrazione di workflow
  moderno, anch'esso basato su Python, che enfatizza la creazione di
  pipeline di dati dinamiche e resilienti.<sup>5</sup> La sua filosofia
  "code-as-workflows" permette di trasformare qualsiasi funzione Python
  in un workflow orchestrabile.

- **Argo Workflows:** Parte dell'ecosistema Argo (progetto CNCF), Argo
  Workflows è un motore di workflow container-native specificamente
  progettato per Kubernetes.<sup>7</sup> I workflow sono definiti come
  Custom Resource Definitions (CRD) di Kubernetes, con ogni passo
  eseguito come un container. È ideale per job paralleli, pipeline CI/CD
  e elaborazione dati su larga scala.

- **Flyte:** Sviluppato originariamente da Lyft, Flyte è una piattaforma
  di orchestrazione nativa per Kubernetes, fortemente tipizzata e
  orientata alla riproducibilità, particolarmente adatta per workflow di
  machine learning e di elaborazione dati complessi.<sup>7</sup> I
  workflow sono definiti in Python e versionati.

- **Temporal:** Temporal è una piattaforma open source per
  l'orchestrazione di workflow duraturi e fault-tolerant, basata sul
  paradigma "workflow-as-code".<sup>7</sup> Non è limitato a pipeline di
  dati, ma eccelle nella gestione di processi di business complessi e di
  lunga durata, offrendo SDK in vari linguaggi.

- **Luigi:** Sviluppato da Spotify <sup>2</sup>, Luigi è un modulo
  Python per la costruzione di pipeline di batch job complesse. Si
  concentra sulla gestione delle dipendenze e sulla visualizzazione dei
  workflow, con un approccio più semplice rispetto ad altri strumenti
  più recenti.

**Verifica di Conformità ai Vincoli:**

<table>
<colgroup>
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 16%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome Strumento</strong></th>
<th><strong>Paradigma Principale</strong></th>
<th><strong>Linguaggio Definizione Workflow</strong></th>
<th><strong>Licenza Open Source</strong></th>
<th><strong>Metodo Deployment K8s Ufficiale</strong></th>
<th><strong>Focus Primario UI Auth (OSS Self-Hosted)</strong></th>
</tr>
<tr>
<th>Apache Airflow</th>
<th>Task-centric DAG</th>
<th>Python</th>
<th>Apache 2.0 <sup>13</sup></th>
<th>Helm Chart <sup>14</sup></th>
<th>RBAC integrato (FAB)</th>
</tr>
<tr>
<th>Dagster</th>
<th>Asset-centric</th>
<th>Python</th>
<th>Apache 2.0 <sup>15</sup></th>
<th>Helm Chart <sup>16</sup></th>
<th>Esterno/Reverse Proxy</th>
</tr>
<tr>
<th>Prefect</th>
<th>Dynamic Python Workflows</th>
<th>Python</th>
<th>Apache 2.0 <sup>17</sup></th>
<th>Helm Chart <sup>18</sup></th>
<th>Basic Auth, Esterno/Reverse Proxy</th>
</tr>
<tr>
<th>Argo Workflows</th>
<th>K8s-native Container Steps</th>
<th>YAML (K8s CRD)</th>
<th>Apache 2.0 <sup>20</sup></th>
<th>K8s CRD, Manifests/Helm <sup>7</sup></th>
<th>Token K8s, SSO (OIDC)</th>
</tr>
<tr>
<th>Flyte</th>
<th>K8s-native, Typed Workflows</th>
<th>Python</th>
<th>Apache 2.0 <sup>22</sup></th>
<th>Helm Chart <sup>23</sup></th>
<th>OIDC/OAuth2</th>
</tr>
<tr>
<th>Temporal</th>
<th>Durable Workflow-as-code</th>
<th>Go, Java, Python, TypeScript</th>
<th>MIT <sup>24</sup></th>
<th>Kubernetes Operator, Helm <sup>25</sup></th>
<th>Plugin Custom (JWT, mTLS)</th>
</tr>
<tr>
<th>Luigi</th>
<th>Pythonic Task Dependencies</th>
<th>Python</th>
<th>Apache 2.0 <sup>27</sup></th>
<th>luigi.contrib.kubernetes <sup>28</sup>, Scheduler come servizio</th>
<th>Esterno/Reverse Proxy (per UI centralizzata)</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

La disponibilità di un metodo di deployment K8s ufficiale, come un Helm
chart ben mantenuto o un Operator, può significare diversi livelli di
maturità operativa e facilità di gestione per le configurazioni
on-premise. Gli Operator, ad esempio, tendono a fornire una gestione del
ciclo di vita più automatizzata. Questa differenza può influenzare le
competenze richieste al team operativo e l'onere di manutenzione a lungo
termine. Sebbene tutti gli strumenti elencati siano "open source", la
vitalità e il supporto delle rispettive comunità, così come la
disponibilità di documentazione completa e aggiornata specificamente per
le *installazioni OSS self-hosted su K8s*, variano in modo
significativo.<sup>1</sup> Uno strumento con una comunità forte e
attiva, focalizzata sulle implementazioni OSS K8s, offrirà probabilmente
migliori risorse per la risoluzione dei problemi, più soluzioni
contribuite dalla comunità per le sfide comuni on-premise (inclusa la
sicurezza) e una prospettiva di manutenzione a lungo termine più
affidabile.

## **4. Analisi Dettagliata dei Sistemi di Orchestrazione**

Questa sezione fornisce un'analisi approfondita per ciascuno strumento
selezionato, coprendo architettura, funzionalità chiave, modalità di
deployment in Kubernetes on-premise, pro e contro, e un esame
dettagliato dei meccanismi di autenticazione e autorizzazione.

**4.1. Apache Airflow**

- 4.1.1. Panoramica Architetturale e Componenti Chiave:  
  L'architettura di Apache Airflow è distribuita e comprende diversi
  componenti principali che interagiscono per orchestrare i workflow.3

  - **Scheduler:** È il cuore di Airflow; monitora tutti i task e i DAG,
    quindi innesca i task quando le loro dipendenze sono soddisfatte.

  - **Webserver:** Fornisce un'interfaccia utente basata su Flask per
    visualizzare lo stato dei DAG, monitorare l'avanzamento, gestire le
    esecuzioni e configurare il sistema.<sup>2</sup>

  - **Metadata Database:** Un database relazionale (tipicamente
    PostgreSQL o MySQL in produzione <sup>33</sup>) che memorizza lo
    stato di tutti i task, le connessioni, le variabili e la cronologia
    delle esecuzioni.

  - **Executor:** Definisce come i task vengono eseguiti. Per ambienti
    Kubernetes, il KubernetesExecutor è la scelta prevalente, poiché
    lancia ogni task come un pod Kubernetes separato.<sup>2</sup> Altre
    opzioni includono LocalExecutor (per test) e CeleryExecutor (per una
    distribuzione più tradizionale basata su code di messaggi).

  - **Workers:** Quando si utilizza KubernetesExecutor, i worker sono i
    pod K8s che eseguono effettivamente la logica dei task. Con
    CeleryExecutor, sono processi worker separati.

  - **DAG Processor:** Un componente che analizza i file DAG dalla
    cartella dei DAG e li serializza nel database dei
    metadati.<sup>34</sup>

  - **Triggerer (opzionale):** Un servizio separato e ad alta
    disponibilità che esegue task differibili (deferred tasks),
    permettendo allo scheduler e ai worker di gestire altri task nel
    frattempo.<sup>34</sup> In un setup K8s on-premise, è fondamentale
    garantire la sincronizzazione dei file DAG tra i componenti
    (scheduler, worker, webserver) e una configurazione robusta per il
    database dei metadati.

- 4.1.2. Funzionalità Principali per l'Orchestrazione di Data
  Platform:  
  Airflow offre un ricco set di funzionalità 2:

  - **Definizione di Workflow come DAG Python:** I workflow sono
    definiti interamente in Python, consentendo una grande flessibilità
    e la generazione dinamica di DAG.

  - **Libreria Estesa di Operatori e Hook:** Una vasta collezione di
    operatori predefiniti per interagire con numerosi sistemi esterni
    (database, cloud storage, API, etc.) e hook per creare connessioni.

  - **TaskFlow API:** Un modo più Pythonic per definire i task
    utilizzando decoratori, semplificando il passaggio di dati tra task.

  - **UI Web Completa:** L'interfaccia utente permette il monitoraggio
    dettagliato, la visualizzazione dei grafi dei DAG, la gestione delle
    esecuzioni, la visualizzazione dei log e la configurazione delle
    connessioni.

  - **Estensibilità:** L'architettura a plugin consente di estendere
    Airflow con operatori, hook e interfacce personalizzate.

  - **Schedulazione Avanzata:** Supporto per schedulazioni basate su
    cron, intervalli di tempo e trigger esterni.

- 4.1.3. Deployment in Ambiente Kubernetes On-Premise:  
  Il metodo principale per il deployment di Airflow su Kubernetes è
  attraverso l'official Helm chart.14 Questo chart facilita la
  configurazione di tutti i componenti di Airflow per un ambiente K8s.  
  L'utilizzo del KubernetesExecutor è la pratica standard in questo
  contesto, dove ogni task di Airflow viene eseguito come un pod
  Kubernetes indipendente.2 Questo offre isolamento, scalabilità e una
  gestione delle risorse più granulare.  
  Considerazioni critiche per un deployment K8s on-premise includono 33:

  - **Sincronizzazione dei DAG:** I file DAG devono essere accessibili
    allo scheduler e ai worker. Metodi comuni includono l'uso di
    git-sync per sincronizzare da un repository Git, l'inclusione dei
    DAG nell'immagine Docker, o l'utilizzo di volumi persistenti
    condivisi.

  - **Persistenza dei Log:** I log dei task devono essere archiviati in
    modo persistente, ad esempio su un sistema di file distribuito o un
    servizio di logging esterno, specialmente se i pod worker sono
    effimeri.

  - **Connessione al Database dei Metadati:** Il database deve essere
    altamente disponibile e accessibile da scheduler, webserver e
    worker.

  - **Gestione delle Risorse K8s:** Definizione appropriata di richieste
    e limiti di risorse per i pod worker per garantire stabilità e
    prestazioni.

- **4.1.4. Pro e Contro:**

  - **Pro:**

    - **Maturità e Adozione:** Piattaforma consolidata con una vasta
      base di utenti e anni di sviluppo in produzione.<sup>1</sup>

    - **Comunità Ampia:** Una delle più grandi comunità open source, che
      si traduce in abbondante documentazione, tutorial e
      supporto.<sup>1</sup>

    - **Estensibilità e Integrazioni:** Vasta gamma di provider e plugin
      per l'integrazione con quasi tutti i sistemi di dati e
      cloud.<sup>35</sup>

    - **Flessibilità Python-Native:** La definizione dei DAG in Python
      offre un controllo completo e la possibilità di logiche
      complesse.<sup>2</sup>

    - **Scalabilità con KubernetesExecutor:** Buona capacità di scalare
      orizzontalmente l'esecuzione dei task.<sup>2</sup>

  - **Contro:**

    - **Curva di Apprendimento Ripida:** Può essere complesso per i
      nuovi utenti, specialmente per quanto riguarda i concetti di base
      e la configurazione avanzata.<sup>35</sup>

    - **Complessità di Setup e Gestione On-Premise:** La configurazione
      e la manutenzione, specialmente in K8s, possono essere
      onerose.<sup>1</sup>

    - **Scheduler come Potenziale Bottleneck:** Se non configurato
      correttamente, lo scheduler può diventare un punto di contesa in
      installazioni molto grandi.

    - **UI a Volte Macchinosa:** Alcuni utenti trovano l'interfaccia
      utente meno intuitiva rispetto a strumenti più
      moderni.<sup>38</sup>

    - **Passaggio Dati tra Task (XComs):** Il meccanismo nativo XComs
      per passare piccole quantità di dati tra task ha delle limitazioni
      in termini di dimensione e usabilità.<sup>35</sup>

- 4.1.5. Autenticazione e Autorizzazione:  
  La sicurezza dell'interfaccia web e delle API di Airflow, in un
  contesto self-hosted, è gestita per impostazione predefinita da Flask
  AppBuilder (FAB).41

  - **Nativa (Self-Hosted K8s):**

    - **Autenticazione:** FAB supporta nativamente l'autenticazione
      basata su database, dove gli utenti vengono creati con username e
      password.<sup>41</sup>

    - **Autorizzazione (RBAC):** FAB fornisce un sistema RBAC completo.
      Include ruoli predefiniti (Admin, User, Viewer, Op, Public) e la
      possibilità di creare ruoli personalizzati con permessi granulari.
      Questo include il controllo dell'accesso a livello di singolo
      DAG.<sup>41</sup>

    - **Cifratura dei Secret:** Le informazioni sensibili (password
      delle connessioni, variabili) memorizzate nel database dei
      metadati sono cifrate utilizzando una chiave Fernet. Questa chiave
      deve essere generata e configurata in modo consistente su tutti i
      componenti di Airflow (scheduler, webserver, worker).<sup>33</sup>
      La sua gestione sicura è cruciale.

  - **Integrazione Personalizzata/Esterna (tramite FAB in
    webserver\_config.py):**

    - **LDAP:** Airflow supporta l'integrazione con server LDAP tramite
      il backend di autenticazione LDAP di FAB. Richiede l'installazione
      del pacchetto apache-airflow\[ldap\] e la configurazione di
      parametri come l'URI del server LDAP, l'utente di bind, i filtri
      per utenti e gruppi nel file webserver\_config.py.<sup>41</sup>

    - **OAuth/OIDC:** L'integrazione con provider OAuth 2.0 / OpenID
      Connect (come Google, Azure AD, Okta, Keycloak) è supportata da
      FAB.<sup>41</sup> La configurazione avviene in
      webserver\_config.py, specificando client ID, client secret, URL
      di discovery, scope richiesti, e mappature dei ruoli.

    - **SAML:** L'integrazione SAML con Airflow è possibile, tipicamente
      attraverso un bridge OIDC (se il provider SAML lo supporta e FAB è
      configurato per OIDC) o utilizzando un security manager SAML
      personalizzato per FAB. Il snippet <sup>141</sup> menziona un
      backend airflow.contrib.auth.backends.saml\_auth e opzioni di
      configurazione SAML dirette in airflow.cfg, suggerendo che
      potrebbero esistere o essere esistite integrazioni più dirette. La
      documentazione di FAB <sup>48</sup> non elenca SAML tra i metodi
      di autenticazione standard, ma la sua architettura permette
      security manager personalizzati. Il pacchetto airflow-with-saml su
      conda-forge <sup>49</sup> indica la disponibilità di soluzioni
      pacchettizzate dalla comunità.

    - **Kerberos:** Airflow include il supporto nativo per
      l'autenticazione Kerberos per i task che interagiscono con servizi
      Kerberizzati (es. HDFS, Hive).<sup>33</sup> Questo è separato
      dall'autenticazione dell'UI/API.

  - **Considerazioni per On-Premise K8s:**

    - La gestione sicura della chiave Fernet è fondamentale (es. tramite
      Kubernetes Secrets).

    - Le credenziali del database dei metadati devono essere protette.

    - È necessario implementare NetworkPolicies per limitare l'accesso
      di rete ai componenti di Airflow (webserver, scheduler, database).

    - Il file webserver\_config.py contenente la configurazione di
      sicurezza deve essere distribuito in modo consistente ai pod del
      webserver.

    - I pod worker che eseguono task potrebbero necessitare di
      ServiceAccount Kubernetes specifici se devono interagire con l'API
      di Kubernetes o con API di provider cloud.<sup>33</sup>

L'utilizzo di Flask AppBuilder in Airflow fornisce un insieme di
funzionalità di autenticazione e RBAC relativamente maturo e ricco per
la sua versione open source, specialmente se confrontato con alcuni
orchestratori più recenti. Tuttavia, questa stessa dipendenza implica
che la sua configurazione di sicurezza è legata al modello di FAB e può
risultare complessa. Sebbene potente, una configurazione errata può
facilmente portare a vulnerabilità. L'Helm chart ufficiale aiuta a
standardizzare il deployment, ma il consolidamento della sicurezza
rimane una responsabilità cruciale dell'operatore. È necessario gestire
attentamente la separazione tra la sicurezza a livello di esecuzione
(ServiceAccount K8s per i worker) e la sicurezza dell'UI/API (FAB).

**4.2. Dagster**

- 4.2.1. Panoramica Architetturale e Componenti Chiave:  
  L'architettura di Dagster è progettata per la moderna ingegneria dei
  dati, con una chiara separazione tra i servizi di sistema e il codice
  utente.4

  - **Dagster Webserver (Dagit):** Fornisce l'interfaccia utente (UI)
    per lo sviluppo, il monitoraggio e l'operatività delle pipeline,
    oltre a un'API GraphQL.<sup>4</sup>

  - **Dagster Daemon:** Un servizio che esegue funzionalità di
    background come la schedulazione, l'esecuzione di sensori per
    trigger esterni e la gestione della coda di esecuzione dei
    job.<sup>4</sup>

  - **User Code Deployments (Code Locations):** Il codice definito
    dall'utente (assets, job, schedules, sensors) è ospitato in processi
    server gRPC separati, chiamati "code locations".<sup>4</sup> Questo
    isola il codice utente dal sistema Dagster principale, permettendo
    dipendenze e versionamenti indipendenti.

  - **Storages:** Dagster utilizza diversi tipi di storage
    configurabili:

    - RunStorage: Memorizza informazioni sulle esecuzioni dei job (es.
      PostgreSQL, MySQL, SQLite).<sup>4</sup>

    - EventLogStorage: Archivia gli eventi strutturati generati durante
      le esecuzioni.<sup>4</sup>

    - ScheduleStorage e SensorStorage: Memorizzano lo stato degli
      scheduler e dei sensori.

  - **Concetti Fondamentali:**

    - **Software-Defined Assets (SDA):** L'astrazione principale. Un
      asset è un oggetto dati (es. una tabella, un file, un modello ML)
      prodotto da un calcolo. Le pipeline sono definite come grafi di
      asset e le loro dipendenze.<sup>2</sup>

    - **Ops:** Unità di calcolo riutilizzabili. Possono essere usate per
      costruire job, ma l'approccio basato su asset è generalmente
      preferito.<sup>2</sup>

    - **Jobs:** Unità di esecuzione che comprende un grafo di ops o un
      sottoinsieme di asset da materializzare.<sup>2</sup>

    - **Resources:** Servizi esterni configurabili (es. connessioni a
      database, API client) resi disponibili agli asset e agli
      ops.<sup>4</sup>

    - **IO Managers:** Definiscono come gli output degli asset/ops
      vengono memorizzati e come gli input vengono caricati, permettendo
      di astrarre la logica di I/O.<sup>4</sup>

    - **Schedules e Sensors:** Meccanismi per automatizzare l'esecuzione
      di job o la materializzazione di asset, rispettivamente basati su
      intervalli di tempo o eventi esterni.<sup>4</sup>

- 4.2.2. Funzionalità Principali per l'Orchestrazione di Data
  Platform:  
  Dagster si distingue per 2:

  - **Programmazione Asset-Centric:** Modella le pipeline in termini di
    asset di dati e le loro interdipendenze, rendendo i flussi più
    intuitivi.

  - **Osservabilità e Lineage Integrati:** La UI (Dagit) fornisce una
    visualizzazione chiara del lineage dei dati, dello stato delle
    materializzazioni e dei metadati associati.

  - **Tipizzazione Forte e Validazione:** Supporto per la definizione di
    schemi e tipi per gli input/output, aiutando a garantire la qualità
    dei dati.

  - **Testabilità:** Progettato per facilitare i test unitari e di
    integrazione delle pipeline.

  - **Sviluppo Locale Iterativo:** Ottima esperienza di sviluppo locale
    con feedback rapido.

  - **Automazione Dichiarativa:** Oltre alla schedulazione cron,
    supporta politiche di "freshness" e sensori per un'orchestrazione
    intelligente basata sullo stato degli asset.

  - **Integrazioni:** Buona integrazione con strumenti dell'ecosistema
    dati come dbt, Airbyte, Fivetran.

- 4.2.3. Deployment in Ambiente Kubernetes On-Premise:  
  L'official Helm chart è il metodo primario per il deployment di
  Dagster Open Source su Kubernetes.4 Il chart permette di configurare
  il webserver Dagit, il daemon, e le user code deployments.  
  Dagster può lanciare esecuzioni di job o singoli op come pod o job
  Kubernetes attraverso K8sRunLauncher e k8s\_job\_executor.4 Questo
  permette isolamento delle esecuzioni e scalabilità orizzontale. La
  configurazione avviene tramite il file values.yaml dell'Helm chart 59,
  che gestisce aspetti come le immagini Docker per le code location, le
  risorse K8s, e la connessione agli storage.

- **4.2.4. Pro e Contro:**

  - **Pro:**

    - **Paradigma Moderno Asset-Centric:** Molto apprezzato dai team di
      dati per la sua intuitività e allineamento con i moderni flussi di
      lavoro sui dati.<sup>32</sup>

    - **Eccellente Esperienza di Sviluppo Locale e Test:** Facilita
      cicli di sviluppo rapidi e robusti.<sup>32</sup>

    - **Forte Osservabilità e Lineage:** La UI Dagit offre
      visualizzazioni chiare e metadati dettagliati.<sup>32</sup>

    - **Buona Integrazione con dbt:** Considerata una delle migliori
      integrazioni con dbt nel panorama degli
      orchestratori.<sup>32</sup>

  - **Contro:**

    - **Autenticazione/Autorizzazione OSS Limitata:** La versione open
      source di Dagit non include meccanismi di autenticazione o RBAC
      integrati per l'UI/API; questi sono principalmente funzionalità di
      Dagster+ (la versione commerciale/cloud).<sup>61</sup>

    - **Comunità più Piccola di Airflow:** Sebbene in crescita, la
      comunità non è vasta come quella di Airflow, il che può tradursi
      in meno risorse di terze parti o risposte immediate a problemi
      specifici.<sup>55</sup>

    - **API e Documentazione:** Alcuni utenti hanno trovato l'API
      verbosa o soggetta a cambiamenti, e la documentazione per
      configurazioni OSS complesse a volte può essere
      carente.<sup>32</sup>

    - **Costi Potenziali:** Se le funzionalità avanzate di Dagster+
      diventano necessarie, si introduce un costo.<sup>65</sup>

- **4.2.5. Autenticazione e Autorizzazione:**

  - **Nativa (Self-Hosted K8s OSS - Dagit UI/API):**

    - Dagster Open Source, e specificamente il suo webserver Dagit,
      **non include alcun meccanismo di autenticazione o autorizzazione
      integrato**.<sup>61</sup> Questa è una distinzione cruciale
      rispetto alla sua controparte commerciale, Dagster+, che offre
      funzionalità complete di SSO e RBAC.<sup>62</sup>

    - Una discussione su GitHub <sup>63</sup> conferma questa mancanza e
      il fatto che gli utenti tipicamente ricorrono a soluzioni esterne.
      L'unica funzionalità "nativa" menzionata per limitare l'accesso in
      OSS è la possibilità di configurare un'istanza Dagit in modalità
      di sola lettura (read-only), che impedisce modifiche tramite UI ma
      non autentica gli utenti.<sup>63</sup>

  - **Integrazione Personalizzata/Esterna (per Dagit UI/API):**

    - **Reverse Proxy:** L'approccio standard e raccomandato dalla
      comunità per mettere in sicurezza Dagit in un ambiente self-hosted
      è posizionarlo dietro un reverse proxy (es. Nginx, Caddy,
      Traefik). Il proxy gestisce l'autenticazione prima di inoltrare le
      richieste a Dagit.<sup>63</sup>

    - **LDAP/OIDC/SAML:** L'integrazione con questi protocolli di
      identità avviene *attraverso il reverse proxy*. Ad esempio, si può
      usare Authelia (che può interfacciarsi con LDAP) <sup>70</sup>, o
      configurare il proxy per utilizzare un provider OIDC o SAML. Dagit
      stesso non gestisce direttamente questi protocolli in OSS. Google
      IAP (Identity-Aware Proxy) e AWS ALB Authenticate sono menzionati
      come opzioni cloud per questo scopo, che possono essere adattate
      on-premise con strumenti equivalenti.<sup>63</sup>

    - **RBAC:** Non esiste un RBAC nativo in Dagit OSS. Qualsiasi
      controllo degli accessi basato sui ruoli deve essere implementato
      a livello del reverse proxy o del sistema di autenticazione
      esterno. Questo di solito significa un controllo di accesso più
      grossolano (accesso completo o nessun accesso alla UI/API)
      piuttosto che permessi granulari sulle singole pipeline o asset, a
      meno che il proxy non sia in grado di ispezionare le richieste
      GraphQL e applicare logiche complesse, il che è atipico e
      complesso. La possibilità di deployare istanze Dagit multiple con
      diverse configurazioni di accesso è stata suggerita come un
      workaround complesso.<sup>63</sup>

  - **Considerazioni per On-Premise K8s:**

    - È essenziale prevedere il deployment e la configurazione di un
      reverse proxy con i moduli di autenticazione appropriati.

    - Gestione sicura delle configurazioni e dei secret del proxy
      all'interno di Kubernetes.

    - Utilizzo di NetworkPolicies per limitare l'accesso diretto ai pod
      di Dagit, forzando il traffico attraverso il proxy.

    - Le autorizzazioni per l'esecuzione dei job stessi all'interno di
      Kubernetes sono gestite tramite i ServiceAccount K8s associati ai
      pod dei job, separatamente dalla UI/API auth.

Esiste un divario significativo nelle funzionalità di autenticazione e
autorizzazione tra Dagster Open Source e Dagster+. Per le installazioni
on-premise OSS su K8s, la sicurezza dell'interfaccia Dagit è in gran
parte una responsabilità dell'utente, da implementare esternamente a
Dagster stesso. Questo aggiunge complessità al deployment e alla
gestione operativa. La facilità d'uso di Dagster per lo sviluppo delle
pipeline potrebbe essere controbilanciata dalla complessità di metterlo
in sicurezza in un ambiente multiutente on-premise.

**4.3. Prefect**

- 4.3.1. Panoramica Architetturale e Componenti Chiave:  
  Prefect (versioni 2.0 e 3.0) è un orchestratore di workflow Pythonic
  che enfatizza la flessibilità e l'esperienza dello sviluppatore.2

  - **Prefect Server/API:** Il backend che orchestra le esecuzioni dei
    flow, memorizza metadati (stati, log, artefatti) e serve l'UI e
    l'API GraphQL. In un setup self-hosted, questo server viene eseguito
    on-premise.<sup>2</sup>

  - **Database:** Utilizzato dal Prefect Server per la persistenza dei
    metadati. SQLite è supportato per lo sviluppo locale, ma PostgreSQL
    è raccomandato per la produzione.<sup>72</sup>

  - **Agent:** Un processo leggero e polivalente che interroga il
    Prefect Server (o Prefect Cloud) per nuove esecuzioni di flow da
    avviare e le esegue nell'infrastruttura specificata.<sup>2</sup>

  - **Work Pools:** Definiscono come e dove gli agenti eseguono i flow.
    Possono essere configurati per diversi tipi di infrastruttura (es.
    Kubernetes, Docker, processi locali) e gestiscono la
    concorrenza.<sup>6</sup>

  - **Flows:** L'unità fondamentale di orchestrazione, definita da una
    funzione Python decorata con @flow. I flow possono contenere task e
    subflow.<sup>5</sup>

  - **Tasks:** Funzioni Python decorate con @task, rappresentano singole
    unità di lavoro all'interno di un flow.<sup>6</sup>

  - **Subflows:** Flow che possono essere chiamati e orchestrati
    all'interno di altri flow, promuovendo la modularità.<sup>6</sup>

  - **Deployments:** Definizioni di come un flow dovrebbe essere
    eseguito, includendo schedulazione, parametri, infrastruttura e
    trigger.<sup>6</sup> L'architettura di Prefect 2.0/3.0 è progettata
    per essere dinamica, eliminando la necessità di DAG statici
    pre-registrati.<sup>6</sup>

- 4.3.2. Funzionalità Principali per l'Orchestrazione di Data
  Platform:  
  Prefect offre 5:

  - **Workflow Dinamici e Pythonic:** Definizione di flow e task
    direttamente in Python, con supporto per logica condizionale nativa,
    loop e programmazione asincrona (async/await).

  - **Nessuna Pre-registrazione dei Flow:** I flow possono essere
    eseguiti e deployati senza una registrazione manuale anticipata.

  - **Blocks:** Un sistema sicuro e validato con Pydantic per la
    gestione della configurazione di sistemi esterni (es. credenziali
    AWS, connessioni a database).

  - **Notifiche e Automazioni:** Capacità di inviare notifiche e
    definire automazioni basate sugli stati dei flow run.

  - **UI per Osservabilità:** Interfaccia web per monitorare le
    esecuzioni, visualizzare log e gestire i deployment.

  - **Schedulazione Flessibile:** Supporto per schedulazioni basate su
    cron, intervalli, e trigger da eventi.

  - **Caching dei Task:** Meccanismi per il caching dei risultati dei
    task per evitare riesecuzioni.

- 4.3.3. Deployment in Ambiente Kubernetes On-Premise:  
  Prefect può essere deployato on-premise su Kubernetes utilizzando
  l'official Helm chart.18 Questo chart permette di installare il
  Prefect Server (API e UI) e configurare agenti che operano all'interno
  del cluster K8s.  
  I flow run vengono tipicamente eseguiti come Kubernetes Jobs o pod,
  gestiti da un agente configurato con un work pool di tipo
  Kubernetes.18 Questo garantisce che ogni esecuzione di flow possa
  avere il proprio ambiente isolato e le proprie risorse. La
  configurazione include la specificazione dell'immagine Docker, delle
  richieste di risorse K8s e delle variabili d'ambiente.

- **4.3.4. Pro e Contro:**

  - **Pro:**

    - **Facilità d'Uso e Esperienza Sviluppatore:** Molto Pythonic, con
      una curva di apprendimento generalmente più bassa rispetto ad
      Airflow per iniziare.<sup>76</sup>

    - **Workflow Dinamici:** Eccellente supporto per pipeline definite
      dinamicamente al runtime.<sup>5</sup>

    - **Buona Gestione degli Errori e Osservabilità:** Particolarmente
      con Prefect Cloud, ma anche l'OSS offre buone basi.<sup>76</sup>

    - **Scalabilità con Agenti/Work Pools:** L'architettura agent-based
      si adatta bene a diversi ambienti, incluso K8s.<sup>76</sup>

  - **Contro:**

    - **Comunità più Piccola di Airflow:** Sebbene attiva e in crescita,
      non ha la stessa dimensione e quantità di risorse di terze parti
      di Airflow.<sup>76</sup>

    - **Funzionalità Avanzate Cloud-Centric:** Molte funzionalità
      avanzate di sicurezza e gestione (SSO, RBAC granulare, audit log)
      sono primariamente offerte in Prefect Cloud.<sup>72</sup>

    - **Documentazione a Volte Carente:** Per configurazioni OSS
      complesse o funzionalità più recenti, la documentazione potrebbe
      non essere sempre esaustiva o aggiornata.<sup>81</sup>

    - **Cambiamenti Frequenti:** Essendo un progetto in rapida
      evoluzione, possono verificarsi breaking changes tra le
      versioni.<sup>81</sup>

- **4.3.5. Autenticazione e Autorizzazione:**

  - **Nativa (Self-Hosted K8s OSS):**

    - **Basic Authentication:** Il server Prefect self-hosted può essere
      protetto con una stringa di autenticazione base (formato
      username:password) configurabile tramite le impostazioni
      server.api.auth\_string (per il server) e api.auth\_string (per i
      client che comunicano con l'API).<sup>19</sup> L'Helm chart
      supporta la configurazione di questa basic auth tramite Kubernetes
      Secrets.<sup>19</sup>

    - **CSRF Protection:** È possibile abilitare la protezione CSRF per
      il server API.<sup>82</sup>

    - **RBAC:** La versione open source del server Prefect **non include
      un sistema RBAC granulare integrato**. Le funzionalità di RBAC
      sono una caratteristica di Prefect Cloud.<sup>72</sup>
      L'autenticazione base fornisce un singolo livello di accesso
      "amministrativo".

  - **Integrazione Personalizzata/Esterna:**

    - **Reverse Proxy:** Similmente a Dagster, l'approccio comune per
      implementare meccanismi di autenticazione più robusti (come OIDC,
      SAML, o integrazione LDAP) per l'UI e l'API del server Prefect
      self-hosted è quello di utilizzare un reverse proxy (es. Nginx,
      Traefik, OAuth2-Proxy).<sup>86</sup> Il proxy gestisce il flusso
      di autenticazione e poi inoltra le richieste autenticate al server
      Prefect.

    - **LDAP/OIDC/SAML:** L'integrazione con questi protocolli IdP
      avviene tipicamente tramite il reverse proxy. Prefect Cloud,
      d'altra parte, supporta direttamente OIDC e SAML.<sup>85</sup>
      Discussioni della comunità <sup>87</sup> confermano che l'SSO per
      installazioni self-hosted richiede soluzioni personalizzate o
      l'uso di un reverse proxy.

    - **RBAC:** Qualsiasi forma di RBAC granulare per la versione OSS
      dovrebbe essere imposta dal sistema di autenticazione esterno o
      dal reverse proxy, poiché non è una funzionalità nativa del server
      open source.

  - **Considerazioni per On-Premise K8s:**

    - L'Helm chart facilita la configurazione della basic auth
      utilizzando Kubernetes Secrets.

    - È cruciale gestire in modo sicuro la stringa di autenticazione
      base.

    - NetworkPolicies dovrebbero essere usate per proteggere l'accesso
      diretto al server Prefect, forzando il traffico attraverso il
      reverse proxy se utilizzato per l'autenticazione avanzata.

    - La configurazione di CORS (api.cors\_allowed\_origins, etc.) è
      importante quando si accede all'API da domini diversi,
      specialmente se l'UI è servita dietro un proxy.<sup>82</sup>

Prefect Open Source segue un modello simile a Dagster OSS per quanto
riguarda l'autenticazione: viene fornita un'autenticazione di base, ma
funzionalità di livello enterprise come SSO e RBAC granulare sono
principalmente appannaggio della versione Cloud. Questo spinge le
installazioni on-premise OSS verso soluzioni basate su reverse proxy per
una sicurezza avanzata. L'aspetto "developer-friendly" di Prefect
potrebbe essere messo alla prova dalla complessità aggiuntiva derivante
dalla configurazione e gestione di componenti di autenticazione esterni
per un funzionamento sicuro on-premise. La distinzione nelle
funzionalità di sicurezza tra OSS e Cloud è un punto decisionale chiave.

**4.4. Argo Workflows**

- 4.4.1. Panoramica Architetturale e Componenti Chiave:  
  Argo Workflows è un motore di workflow open source, nativo per
  Kubernetes, implementato come una Custom Resource Definition (CRD) di
  Kubernetes.7

  - **Workflow Controller:** Il componente principale che osserva le
    risorse Workflow (CRD) e gestisce il loro ciclo di vita,
    orchestrando l'esecuzione dei passi come pod Kubernetes.

  - **Argo Server:** Un server opzionale che fornisce un'API REST e
    un'interfaccia utente web per visualizzare, gestire e sottomettere i
    workflow.<sup>9</sup>

  - **Workflow CRD:** La definizione della risorsa personalizzata
    Workflow che descrive la struttura del workflow, i task, le
    dipendenze, gli input/output e i template.

  - **Executor:** Il componente all'interno di ogni pod worker che
    esegue la logica del task (es. container, script). Argo Workflows
    supporta diversi executor (Docker, PNS, Kubelet, Kubernetes API).
    Ogni passo di un workflow Argo viene eseguito come un container
    all'interno di un pod Kubernetes.<sup>8</sup>

- 4.4.2. Funzionalità Principali per l'Orchestrazione di Data
  Platform:  
  Argo Workflows offre un ampio set di funzionalità focalizzate
  sull'esecuzione di job su Kubernetes 8:

  - **Esecuzione Container-Native:** Ogni passo è un container, offrendo
    isolamento e riproducibilità.

  - **Definizione di Workflow basata su DAG e Passi:** Supporta sia la
    definizione di dipendenze complesse tramite DAG sia sequenze lineari
    di passi.

  - **Gestione degli Artefatti:** Supporto integrato per la gestione di
    input e output (artefatti) da/verso S3, GCS, Artifactory, HTTP, Git,
    ecc.

  - **Workflow Templating:** Permette di creare template di workflow
    riutilizzabili.

  - **Schedulazione (CronWorkflows):** Supporto per la schedulazione
    periodica di workflow tramite una CRD CronWorkflow.

  - **API REST e CLI:** Interfacce complete per l'interazione
    programmatica e da riga di comando.

  - **Controllo del Parallelismo e Risorse K8s:** Sfrutta le primitive
    di Kubernetes per la gestione delle risorse, l'affinità dei nodi, le
    tolleranze, i volumi, ecc.

  - **Parametrizzazione, Loop e Condizionali:** Supporto per workflow
    dinamici.

  - **Retry, Timeout, Suspend/Resume:** Meccanismi robusti per la
    gestione del ciclo di vita delle esecuzioni.

- 4.4.3. Deployment in Ambiente Kubernetes On-Premise:  
  Argo Workflows viene installato direttamente su un cluster
  Kubernetes.21 Il deployment tipicamente comporta l'applicazione di
  manifest YAML che definiscono le CRD necessarie, il Workflow
  Controller, e opzionalmente l'Argo Server. Sono disponibili anche Helm
  chart mantenuti dalla comunità o dai vendor.  
  Essendo K8s-native, sfrutta direttamente le capacità di Kubernetes per
  la schedulazione, la scalabilità e la gestione delle risorse, senza
  dipendenze esterne significative oltre a Kubernetes stesso e,
  opzionalmente, uno storage per gli artefatti.

- **4.4.4. Pro e Contro:**

  - **Pro:**

    - **Veramente K8s-Native:** Progettato da zero per Kubernetes, si
      integra profondamente con l'ecosistema.<sup>7</sup>

    - **Altamente Scalabile:** Eredita la scalabilità di
      Kubernetes.<sup>8</sup>

    - **Ideale per CI/CD e Elaborazione Parallela:** Molto efficiente
      per job batch, pipeline CI/CD e carichi di lavoro che beneficiano
      di un'elevata parallelizzazione.<sup>8</sup>

    - **Configurazione Flessibile tramite YAML:** Allineato con le
      pratiche dichiarative di Kubernetes.<sup>8</sup>

    - **Parte dell'Ecosistema Argo (CNCF):** Beneficia della sinergia
      con altri progetti Argo come Argo CD, Argo Events, Argo
      Rollouts.<sup>9</sup>

  - **Contro:**

    - **Richiede Competenze Kubernetes:** L'installazione, la
      configurazione e la gestione richiedono una solida comprensione di
      Kubernetes.<sup>95</sup>

    - **UI più Semplice Rispetto ad Airflow:** L'interfaccia utente,
      sebbene funzionale, è generalmente considerata meno ricca di
      funzionalità rispetto a quella di Airflow.<sup>96</sup>

    - **Comunità più Piccola di Airflow:** Sebbene attiva e in crescita,
      la comunità specificamente per Argo Workflows è più piccola di
      quella di Airflow.<sup>95</sup>

    - **Setup Può Essere Complesso:** Nonostante la natura K8s-native,
      la configurazione iniziale per scenari di produzione può essere
      complessa.<sup>97</sup>

    - **Sfide nella Gestione Multi-Cluster:** Sebbene possibile, la
      gestione di Argo Workflows su più cluster può presentare
      complessità operative se non orchestrata con strumenti aggiuntivi
      come Argo CD <sup>98</sup> (questi snippet si riferiscono spesso
      ad ArgoCD, ma le sfide di frammentazione e overhead possono essere
      rilevanti per l'ecosistema).

- **4.4.5. Autenticazione e Autorizzazione:**

  - **Nativa (Self-Hosted K8s):**

    - **Modalità di Autenticazione dell'Argo Server:** L'Argo Server può
      operare in diverse modalità di autenticazione <sup>99</sup>:

      - server: Utilizza il ServiceAccount Kubernetes dell'Argo Server
        stesso per autenticarsi all'API di Kubernetes.

      - client: (Default da v3.0+) Utilizza il token bearer Kubernetes
        del client che effettua la richiesta. Questo significa che
        l'autenticazione dell'utente all'Argo Server è di fatto delegata
        a Kubernetes (es. l'utente si autentica a kubectl o all'API K8s,
        e quel token viene passato).

      - sso: Abilita il Single Sign-On.

    - Per impostazione predefinita, alcune installazioni rapide
      potrebbero deployare l'Argo Server senza autenticazione,
      rendendolo accessibile a chiunque abbia accesso alla
      rete.<sup>100</sup> È cruciale configurare una modalità di
      autenticazione sicura.

  - **Integrazione Personalizzata/Esterna:**

    - **OIDC/OAuth2 (SSO):** L'Argo Server supporta l'integrazione SSO
      tramite OIDC.<sup>9</sup> Questo permette di integrarsi con
      Identity Provider (IdP) come Dex (spesso condiviso con Argo CD),
      Okta, Keycloak, ecc. La configurazione avviene principalmente nel
      workflow-controller-configmap.yaml e richiede la creazione di
      client OIDC e secret K8s per client ID e secret.

    - **LDAP/SAML:** L'integrazione diretta con LDAP o SAML non è
      menzionata come funzionalità nativa dell'Argo Server. Tuttavia, è
      comunemente realizzata utilizzando un bridge OIDC come Dex, che
      può essere configurato a sua volta per utilizzare LDAP o SAML come
      upstream identity provider.<sup>102104</sup>

    - **RBAC:**

      - Argo Workflows si affida pesantemente al **RBAC di Kubernetes**
        per l'autorizzazione.<sup>9</sup>

      - I permessi per l'esecuzione dei workflow sono determinati dal
        **ServiceAccount Kubernetes** assegnato ai pod del workflow
        (specificato in workflow.spec.serviceAccountName o il SA default
        del namespace).<sup>106</sup> È fortemente sconsigliato usare il
        SA default in produzione.<sup>107</sup>

      - **SSO RBAC (da v2.12+):** Questa funzionalità permette di
        mappare utenti o gruppi OIDC a ServiceAccount Kubernetes
        specifici all'interno dello stesso namespace dell'Argo Server.
        Questo avviene tramite annotazioni sui ServiceAccount (es.
        workflows.argoproj.io/rbac-rule: "'admin' in
        groups").<sup>101</sup> Questo abilita un controllo degli
        accessi più granulare basato sull'identità dell'utente SSO,
        traducendo i permessi OIDC in permessi K8s.

      - **Delega RBAC SSO per Namespace (da v3.3+):** Estende SSO RBAC
        permettendo ai proprietari dei namespace di definire le proprie
        mappature utenti/gruppi OIDC a ServiceAccount all'interno dei
        loro namespace, promuovendo un modello di self-service per i
        permessi.<sup>101</sup>

  - **Considerazioni per On-Premise K8s:**

    - È imperativo configurare una modalità di autenticazione sicura per
      l'Argo Server, andando oltre l'impostazione predefinita
      potenzialmente insicura.

    - Una profonda comprensione del RBAC di Kubernetes (Roles,
      ClusterRoles, RoleBindings, ServiceAccounts) è essenziale per una
      configurazione sicura.

    - Gestione sicura dei client secret OIDC e corretta configurazione
      dei callback URL.

    - Attenzione ai permessi concessi ai ServiceAccount utilizzati dai
      workflow, seguendo il principio del minimo privilegio.

Il modello di sicurezza di Argo Workflows è intrinsecamente legato a
Kubernetes. La sua forza risiede nello sfruttare il RBAC di Kubernetes,
ma ciò implica anche che la sua sicurezza dipende dalla corretta
configurazione del RBAC sottostante e dalla comprensione che
l'amministratore ha di esso. Per i team già esperti nella sicurezza di
Kubernetes, Argo Workflows offre un modello di autenticazione e
autorizzazione naturale e potente. Tuttavia, per i team meno familiari
con il RBAC di K8s, la curva di apprendimento è ripida e c'è un rischio
maggiore di errori di configurazione che potrebbero portare a
vulnerabilità.<sup>100</sup>

**4.5. Flyte**

- 4.5.1. Panoramica Architetturale e Componenti Chiave:  
  Flyte è una piattaforma di orchestrazione nativa per Kubernetes,
  progettata per la riproducibilità, la scalabilità e la manutenibilità
  di workflow complessi, con un focus particolare su machine learning e
  pipeline di dati.7

  - **FlyteAdmin:** Il servizio del control plane che espone l'API
    principale di Flyte, gestisce la registrazione dei workflow, la
    creazione dei launch plan, il tracciamento delle esecuzioni e
    l'archiviazione dei metadati.<sup>10</sup>

  - **FlytePropeller:** Un operatore Kubernetes che monitora le CRD di
    Flyte (es. FlyteWorkflow) e orchestra l'esecuzione effettiva dei
    workflow, traducendo i nodi del grafo in pod Kubernetes o altre
    risorse.<sup>10</sup>

  - **FlyteConsole:** L'interfaccia utente web per visualizzare,
    monitorare e interagire con i workflow, i task e le
    esecuzioni.<sup>10</sup>

  - **FlyteKit:** L'SDK Python (e altri SDK per Java/Scala) utilizzato
    per definire task, workflow e launch plan in modo programmatico.
    Enfatizza la forte tipizzazione.<sup>10</sup>

  - **Flytectl:** L'utility a riga di comando per interagire con
    FlyteAdmin (registrare workflow, lanciare esecuzioni,
    ecc.).<sup>10</sup>

  - **Data Plane:** L'ambiente in cui i task vengono eseguiti,
    tipicamente pod Kubernetes. Flyte gestisce il passaggio di dati tra
    i task, spesso utilizzando un object storage (S3, GCS, MinIO) come
    backend. L'architettura è suddivisa in user plane (FlyteKit,
    Flytectl, FlyteConsole), control plane (FlyteAdmin) e data plane
    (FlytePropeller e i pod di esecuzione).<sup>10</sup>

- 4.5.2. Funzionalità Principali per l'Orchestrazione di Data
  Platform:  
  Flyte si distingue per 7:

  - **Fortemente Tipizzato:** Input e output dei task sono tipizzati, il
    che aiuta a rilevare errori in fase di compilazione e garantisce
    l'integrità dei dati.

  - **Riproducibilità e Versionamento:** Ogni entità (task, workflow,
    launch plan) è versionabile, garantendo la riproducibilità delle
    esecuzioni.

  - **Scalabilità K8s-Native:** Sfrutta appieno Kubernetes per la
    scalabilità e la gestione delle risorse.

  - **Adatto per ML e Pipeline Complesse:** Offre funzionalità
    specifiche per il machine learning come il caching dei task, la
    parallelizzazione e la gestione di dataset strutturati.

  - **Estensibilità tramite Plugin:** Supporta plugin per integrare
    diversi backend di calcolo e servizi.

  - **Isolamento dei Task:** Ogni task viene eseguito in un proprio
    container.

  - **Data Lineage e Caching:** Tracciamento del lineage dei dati e
    caching intelligente dei risultati dei task.

- 4.5.3. Deployment in Ambiente Kubernetes On-Premise:  
  Flyte viene deployato su un cluster Kubernetes utilizzando gli
  official Helm charts (flyte-binary per installazioni più semplici o
  flyte-core per componenti separati e scalabili).23 L'installazione
  richiede un cluster Kubernetes, un database relazionale (PostgreSQL è
  comunemente usato) per FlyteAdmin, e un object store (come MinIO
  on-premise, o S3/GCS se accessibili) per lo scambio di dati e
  artefatti tra i task.23  
  La configurazione on-premise deve gestire l'esposizione di FlyteAdmin
  e FlyteConsole tramite Ingress, la configurazione del DNS e la
  sicurezza della comunicazione tra i componenti.

- **4.5.4. Pro e Contro:**

  - **Pro:**

    - **Architettura K8s-Native:** Progettato specificamente per
      Kubernetes, il che garantisce un'ottima integrazione e
      scalabilità.<sup>109</sup>

    - **Forti Garanzie di Riproducibilità e Versionamento:** Cruciale
      per ML e auditabilità.<sup>10</sup>

    - **Sistema di Tipi Robusto:** Migliora l'affidabilità e riduce gli
      errori runtime.<sup>10</sup>

    - **Scalabile:** Adatto per carichi di lavoro di grandi dimensioni e
      complessi.<sup>29</sup>

    - **Supporto per ML:** Funzionalità specifiche per pipeline di
      machine learning.<sup>29</sup>

  - **Contro:**

    - **Curva di Apprendimento più Ripida:** La forte tipizzazione e i
      concetti specifici di Flyte possono richiedere un investimento
      iniziale maggiore per l'apprendimento.<sup>64</sup>

    - **Richiede Competenze Kubernetes:** Per il deployment e la
      gestione on-premise, è necessaria una buona conoscenza di
      Kubernetes.<sup>64</sup>

    - **Comunità più Piccola di Airflow:** Sebbene in crescita, la
      comunità non è paragonabile a quella di Airflow in termini di
      dimensioni e risorse disponibili.<sup>29</sup>

    - **UI e CLI-Driven:** L'interfaccia utente è funzionale ma alcuni
      potrebbero trovarla meno ricca di Airflow; molte operazioni
      avanzate sono gestite via CLI (flytectl).<sup>110</sup>

- **4.5.5. Autenticazione e Autorizzazione:**

  - **Nativa (Self-Hosted K8s):**

    - **Autenticazione per FlyteAdmin/FlyteConsole:** FlyteAdmin, il
      componente centrale che serve l'API e l'UI, supporta
      l'autenticazione tramite **OAuth 2.0 e OpenID Connect
      (OIDC)**.<sup>112</sup> Questo è il meccanismo primario per
      proteggere l'accesso all'interfaccia di gestione e alle API.

    - FlyteAdmin include un server di autorizzazione OAuth2.0 integrato
      (adatto per test o setup semplici) ma raccomanda l'uso di un
      Identity Provider (IdP) esterno per ambienti di produzione,
      delegando ad esso la gestione delle identità e l'emissione dei
      token.<sup>112</sup>

  - **Integrazione Personalizzata/Esterna:**

    - **OIDC:** È il metodo principale per l'autenticazione degli
      utenti. Flyte si integra con provider IdP che supportano OIDC come
      Okta, Google Cloud Identity, Azure AD, Keycloak.<sup>112</sup> La
      configurazione avviene tramite i valori dell'Helm chart di Flyte,
      specificando l'URL dell'issuer, client ID, client secret, e
      redirect URI.

    - **LDAP/SAML:** FlyteAdmin non supporta direttamente LDAP o SAML.
      L'integrazione con questi sistemi richiederebbe l'uso di un IdP
      OIDC che funga da bridge, ad esempio Keycloak o Dex configurati
      per autenticare gli utenti tramite LDAP o SAML e poi emettere
      token OIDC a Flyte.<sup>112</sup> Le fonti non menzionano supporto
      diretto SAML/LDAP per Flyte stesso.

    - **RBAC:**

      - L'autorizzazione per l'**esecuzione dei task** all'interno di
        Kubernetes si basa sul **RBAC di Kubernetes**. I pod dei task
        Flyte vengono eseguiti con specifici ServiceAccount Kubernetes,
        e i permessi di questi ServiceAccount determinano a quali
        risorse K8s o cloud i task possono accedere.<sup>116</sup>

      - Per quanto riguarda il **controllo degli accessi degli utenti a
        FlyteAdmin/FlyteConsole** (es. chi può vedere quali
        progetti/domini, chi può lanciare esecuzioni), la documentazione
        OSS fornita non dettaglia un sistema RBAC granulare integrato in
        FlyteAdmin stesso che utilizzi, ad esempio, i group claim OIDC
        per assegnare ruoli Flyte specifici.<sup>112</sup> Mentre
        l'autenticazione OIDC è ben definita, l'autorizzazione a livello
        di applicazione Flyte per utenti autenticati sembra meno
        specificata per la versione OSS. <sup>117</sup> menziona "User
        management" in relazione a RBAC ma sembra essere in un contesto
        specifico AWS e non un RBAC generale di Flyte OSS.

  - **Considerazioni per On-Premise K8s:**

    - Configurazione sicura dell'integrazione OIDC con l'IdP scelto,
      inclusa la gestione dei client secret.

    - Gestione attenta dei ServiceAccount Kubernetes e dei relativi
      Role/RoleBinding per i permessi di esecuzione dei workflow.

    - Corretta configurazione del DNS e dell'Ingress per esporre
      FlyteAdmin e FlyteConsole in modo sicuro.

    - Considerare la necessità di un IdP OIDC che possa fare da bridge
      se l'autenticazione aziendale si basa su LDAP/SAML.

Flyte adotta un approccio moderno per la sicurezza del suo control
plane, standardizzando su OIDC/OAuth2 per l'autenticazione. Questo è un
punto di forza. Tuttavia, i dettagli specifici su un sistema RBAC
interno a Flyte per gli utenti (che vada oltre il RBAC di Kubernetes per
l'esecuzione dei pod) nella versione open source sono meno chiari dalle
fonti esaminate. Mentre l'accesso API è protetto tramite OIDC, il
controllo granulare su ciò che gli utenti autenticati possono fare
all'interno di Flyte (ad esempio, accedere a progetti/domini specifici,
eseguire determinate azioni) potrebbe dipendere pesantemente da come i
group claim OIDC possono essere mappati o se è necessario implementare
logiche di autorizzazione personalizzate a livello dell'infrastruttura
di esecuzione K8s. Questo potrebbe rappresentare una lacuna per scenari
on-premise multi-tenant complessi se non supportato nativamente in modo
esplicito.

**4.6. Temporal**

- 4.6.1. Panoramica Architetturale e Componenti Chiave:  
  Temporal è una piattaforma di orchestrazione distribuita,
  fault-tolerant, progettata per eseguire workflow duraturi e stateful.5

  - **Temporal Server:** È il backend che gestisce l'orchestrazione. È
    composto da quattro servizi scalabili indipendentemente
    <sup>120</sup>:

    - Frontend Service: Gestisce le chiamate API gRPC, il routing, il
      rate limiting e l'autorizzazione.

    - History Service: Mantiene lo stato mutabile, le code e i timer per
      le esecuzioni dei workflow. Organizzato in shard per la
      scalabilità.

    - Matching Service: Ospita le Task Queue e smista i task ai Worker.

    - Worker Service: Esegue workflow di background interni al sistema.

  - **Persistence Store:** Un database (supportati PostgreSQL, MySQL,
    Cassandra) che memorizza lo stato dei workflow, la cronologia degli
    eventi e le code di task.<sup>5</sup>

  - **Visibility Store:** Un datastore (Elasticsearch raccomandato per
    la produzione) utilizzato per indicizzare e interrogare i metadati
    dei workflow (es. per listare workflow in esecuzione).<sup>120</sup>

  - **Worker Processes:** Processi sviluppati dall'utente che ospitano
    l'implementazione dei workflow e delle activity. I worker effettuano
    il polling delle Task Queue ospitate dal Matching Service per
    ricevere lavoro.<sup>5</sup>

  - **SDK:** Temporal fornisce SDK in diversi linguaggi (Go, Java,
    Python, TypeScript,.NET, PHP) per definire workflow e activity e per
    interagire con il Temporal Server.<sup>121</sup> Il paradigma è
    "workflow-as-code", dove la logica del workflow è scritta in un
    linguaggio di programmazione standard.<sup>121</sup>

- 4.6.2. Funzionalità Principali per l'Orchestrazione di Data
  Platform:  
  Temporal eccelle in 7:

  - **Esecuzione Duratura e Affidabile:** I workflow possono durare
    secondi, giorni o anni, e il loro stato è preservato anche in caso
    di fallimenti dei worker o del server.

  - **Fault Tolerance e Retry Automatici:** Meccanismi robusti per la
    gestione dei fallimenti delle activity, con retry configurabili e
    compensazioni.

  - **Workflow Stateful:** Ideale per processi che richiedono la
    gestione di uno stato complesso nel tempo.

  - **Supporto Multilingua:** Gli SDK permettono di scrivere logica di
    workflow e activity nel linguaggio preferito.

  - **Scalabilità:** Progettato per scalare a milioni di workflow
    concorrenti.

  - **Capacità Event-Driven:** I workflow possono reagire a segnali
    esterni e attendere eventi.

  - **Visibilità e Debugging:** Strumenti per interrogare lo stato dei
    workflow e ispezionare la cronologia degli eventi.

- 4.6.3. Deployment in Ambiente Kubernetes On-Premise:  
  Per il deployment on-premise su Kubernetes, Temporal offre un Temporal
  Operator 25 che semplifica l'installazione e la gestione dei
  componenti del Temporal Server. In alternativa, sono disponibili Helm
  chart mantenuti dalla comunità o da vendor.  
  Un'installazione self-hosted richiede la configurazione e la gestione
  del persistence store (es. PostgreSQL) e del visibility store (es.
  Elasticsearch).5 L'Operator può aiutare a gestire lo schema del
  database. La configurazione della rete, della persistenza e della
  sicurezza (TLS, autenticazione) è cruciale.120

- **4.6.4. Pro e Contro:**

  - **Pro:**

    - **Estrema Affidabilità e Durabilità:** Ideale per workflow critici
      e di lunga durata che non possono permettersi perdite di
      stato.<sup>121</sup>

    - **Scalabilità Elevata:** Progettato per gestire un grande volume
      di esecuzioni concorrenti.<sup>121</sup>

    - **Forte Tolleranza ai Guasti:** Gestisce automaticamente retry e
      recupero da fallimenti.<sup>121</sup>

    - **Supporto Poliglotta:** Flessibilità nella scelta del linguaggio
      di programmazione per i worker.<sup>121</sup>

    - **Modello di Programmazione Potente:** Consente di esprimere
      logiche di business complesse direttamente nel
      codice.<sup>121</sup>

  - **Contro:**

    - **Curva di Apprendimento Ripida:** Il modello di programmazione
      (workflow, activity, segnali, query) è unico e può richiedere
      tempo per essere assimilato, specialmente per chi proviene da
      orchestratori basati su DAG.<sup>80</sup>

    - **Overhead Operativo Self-Hosted:** La gestione on-premise di
      Temporal, inclusi database e Elasticsearch, può essere complessa e
      onerosa.<sup>80</sup>

    - **Meno Focalizzato su ETL/Data Pipeline Tradizionali:** Sebbene
      possa orchestrare qualsiasi processo, non è specificamente
      ottimizzato per pipeline ETL classiche come Airflow o Dagster, che
      hanno più connettori e astrazioni specifiche per i
      dati.<sup>121</sup>

    - **UI Potrebbe Essere Considerata Basilare:** L'interfaccia web
      fornita con la versione open source è funzionale ma potrebbe non
      avere tutte le funzionalità di visualizzazione avanzate di altri
      strumenti.<sup>124</sup>

- 4.6.5. Autenticazione e Autorizzazione:  
  La sicurezza in un'istanza Temporal self-hosted è un aspetto che
  richiede una configurazione attenta e, spesso, lo sviluppo di
  componenti personalizzati.125

  - **Nativa (Self-Hosted K8s):**

    - **mTLS (Mutual TLS):** Temporal supporta mTLS per cifrare la
      comunicazione tra i servizi del Temporal Server (internode) e tra
      i client (worker, CLI, UI) e il Frontend Service
      (frontend).<sup>120</sup> Questa è la base per l'autenticazione a
      livello di trasporto e la cifratura.

    - **Interfacce Plugin per Auth/Authz:** Temporal fornisce due
      interfacce plugin chiave per implementare logica di autenticazione
      e autorizzazione personalizzata a livello API <sup>125</sup>:

      - ClaimMapper: Responsabile di estrarre e tradurre token di
        autenticazione (es. JWT) in un insieme di "claim" (attestazioni)
        che Temporal può comprendere, tipicamente riguardanti l'identità
        e i permessi dell'utente.

      - Authorizer: Riceve i claim mappati e il target della chiamata
        API, e decide se permettere o negare l'operazione.

    - **Default JWT ClaimMapper:** Temporal fornisce un ClaimMapper JWT
      di default che può validare token JWT firmati (RSA, ECDSA) e
      estrarre permessi da un claim specifico (es. permissions). I
      permessi sono tipicamente definiti per namespace (es.
      my-namespace:read, my-namespace:write) e mappati a ruoli Temporal
      interni (RoleReader, RoleWriter, RoleWorker,
      RoleAdmin).<sup>125</sup>

    - **Default Authorizer (Nop):** Se non viene configurato un
      Authorizer personalizzato, Temporal utilizza un nopAuthorizer che
      permette tutte le chiamate API.<sup>125</sup> Questo rende la
      configurazione di un Authorizer personalizzato essenziale per la
      produzione.

  - **Integrazione Personalizzata/Esterna:**

    - **OIDC:** Il pattern comune per l'integrazione OIDC è configurare
      un IdP esterno per emettere token JWT. Questi token vengono poi
      presentati dai client al Frontend Service di Temporal. Il
      ClaimMapper (default o custom) valida il JWT e ne estrae i claim.
      L'Authorizer personalizzato utilizza questi claim per prendere
      decisioni di accesso.<sup>125</sup> Questo permette di usare
      provider come Keycloak, Okta, Auth0.

    - **LDAP/SAML:** L'integrazione diretta con LDAP o SAML non è
      nativa. Richiederebbe un IdP OIDC che funga da bridge (es.
      Keycloak, Dex) per autenticare gli utenti tramite LDAP/SAML e
      quindi emettere token JWT che Temporal può consumare attraverso il
      ClaimMapper.

    - **RBAC:** Il Role-Based Access Control in Temporal self-hosted
      viene implementato attraverso la logica personalizzata scritta
      nell'Authorizer. Questo Authorizer può basare le sue decisioni sui
      ruoli o gruppi estratti dal token JWT (tramite il ClaimMapper) e
      mappati a permessi specifici sulle API di Temporal o sui
      namespace.<sup>125</sup> Temporal Cloud offre RBAC integrato, ma
      per la versione self-hosted, è una responsabilità di sviluppo.

  - **Considerazioni per On-Premise K8s:**

    - Configurazione sicura di mTLS, inclusa la gestione dei certificati
      CA e dei certificati per i servizi e i client.

    - Sviluppo e deployment di implementazioni personalizzate per
      ClaimMapper e Authorizer. Questo richiede competenze di
      programmazione (tipicamente in Go, dato che il server è in Go).

    - Gestione sicura delle chiavi di firma JWT (se si usa un emittente
      JWT interno) o della configurazione del provider OIDC (JWKS URI,
      ecc.).

    - L'Operator o gli Helm chart possono aiutare a configurare alcuni
      aspetti, ma la logica di auth/authz personalizzata rimane esterna
      ad essi.

Il modello di sicurezza self-hosted di Temporal è estremamente
flessibile grazie alle sue interfacce ClaimMapper e Authorizer.
Tuttavia, questa flessibilità implica che fornisce meccanismi di base
minimi "pronti all'uso" per l'autenticazione utente e RBAC a livello di
API. Una sicurezza robusta è un compito di sviluppo e integrazione. Per
i team che scelgono Temporal on-premise su K8s, è necessario allocare
risorse di sviluppo per costruire logiche di autenticazione e
autorizzazione personalizzate. Sebbene ciò offra la massima adattabilità
a qualsiasi IdP o modello di ruoli personalizzato, rappresenta un
investimento iniziale significativo rispetto a strumenti con gestione
utenti più integrata o integrazione IdP più semplice.

**4.7. Luigi**

- 4.7.1. Panoramica Architetturale e Componenti Chiave:  
  Luigi è un pacchetto Python che aiuta a costruire pipeline complesse
  di job batch.2

  - **Task:** L'unità di lavoro fondamentale in Luigi. Ogni task è una
    classe Python che eredita da luigi.Task. Definisce le dipendenze
    (requires()), l'output (output()), e la logica di esecuzione
    (run()).<sup>12</sup>

  - **Target:** Rappresenta l'output di un task (es. un file locale, un
    oggetto S3, una riga in un database). Luigi usa i target per
    determinare se un task è già stato completato (idempotenza): se il
    target esiste, il task viene saltato.<sup>12</sup> Tipi comuni
    includono LocalTarget, S3Target, PostgresTarget.

  - **Parameter:** Permette di parametrizzare i task, rendendoli
    riutilizzabili con diverse configurazioni.<sup>130</sup>

  - **Central Scheduler (luigid):** Un demone opzionale che fornisce
    un'interfaccia web per visualizzare i grafi delle dipendenze, lo
    stato dei task e per prevenire l'esecuzione simultanea dello stesso
    task con gli stessi parametri.<sup>12</sup> Non esegue i task
    direttamente ma coordina i worker.

  - **Worker:** Il processo che effettivamente esegue la logica del
    metodo run() di un task. Può comunicare con il central scheduler.

- 4.7.2. Funzionalità Principali per l'Orchestrazione di Data
  Platform:  
  Le principali funzionalità di Luigi includono 2:

  - **Gestione delle Dipendenze tra Task:** Definizione chiara delle
    dipendenze tramite il metodo requires().

  - **Esecuzione Idempotente basata su Target:** I task vengono eseguiti
    solo se i loro output (target) non esistono.

  - **Parametrizzazione dei Task:** Facile configurazione dei task
    tramite parametri.

  - **Interfaccia Utente tramite Central Scheduler:** Visualizzazione
    dei workflow e del loro stato.

  - **Estensibilità:** Possibilità di creare task e target
    personalizzati.

  - **Supporto per Sistemi Esterni:** Include contributi per Hadoop,
    Hive, Spark, database relazionali, ecc..<sup>128</sup>

  - **Operazioni Atomiche sui File:** Per HDFS e file locali, garantendo
    che le pipeline non falliscano con dati parziali.<sup>12</sup>

- 4.7.3. Deployment in Ambiente Kubernetes On-Premise:  
  Luigi può essere eseguito in ambienti Kubernetes.

  - Il modulo luigi.contrib.kubernetes.KubernetesJobTask permette di
    definire task Luigi che vengono eseguiti come Kubernetes
    Job.<sup>28</sup> Ogni task Luigi può quindi lanciare un pod K8s per
    la sua esecuzione.

  - Il central scheduler (luigid), se utilizzato, verrebbe eseguito come
    un servizio/pod separato all'interno del cluster Kubernetes,
    esponendo la sua UI.

  - I worker Luigi (che eseguono i task KubernetesJobTask) possono
    anch'essi girare come pod o processi all'interno del cluster, o
    persino esternamente se possono comunicare con l'API di Kubernetes e
    il central scheduler.

- **4.7.4. Pro e Contro:**

  - **Pro:**

    - **Semplicità e Python-Native:** Facile da imparare e utilizzare,
      specialmente per sviluppatori Python e per job batch
      semplici.<sup>1</sup>

    - **Buona Gestione delle Dipendenze:** Il modello basato su task e
      target è efficace per definire e tracciare le
      dipendenze.<sup>130</sup>

    - **Idempotenza:** Il controllo dell'esistenza dei target previene
      riesecuzioni inutili.<sup>128</sup>

  - **Contro:**

    - **Scalabilità Limitata:** Meno scalabile rispetto a orchestratori
      più moderni e distribuiti, specialmente per un numero molto
      elevato di task o workflow complessi.<sup>1</sup>

    - **UI Basilare:** L'interfaccia utente del central scheduler è
      semplice e offre funzionalità di visualizzazione e monitoraggio
      limitate rispetto ad Airflow o Dagster.<sup>1</sup>

    - **Nessuna Schedulazione Avanzata Integrata:** Non ha un sistema di
      schedulazione sofisticato come Airflow; tipicamente si affida a
      cron per l'avvio periodico dei workflow.<sup>128</sup>

    - **Comunità e Integrazioni Ridotte:** Comunità più piccola e meno
      attiva nello sviluppo core rispetto ad Airflow; meno integrazioni
      predefinite.<sup>31</sup>

    - **Mancanza di Autenticazione Nativa per il Central Scheduler:** La
      UI di luigid non ha meccanismi di sicurezza integrati.

    - **Supporto Limitato per Workflow Dinamici:** I grafi delle
      dipendenze sono generalmente statici.<sup>128</sup>

- **4.7.5. Autenticazione e Autorizzazione:**

  - **Nativa (Self-Hosted K8s - Central Scheduler luigid):**

    - Il central scheduler di Luigi (luigid) **non dispone di alcun
      meccanismo di autenticazione o autorizzazione
      integrato**.<sup>131</sup> La sua funzione principale è la
      visualizzazione dei task e la prevenzione di esecuzioni duplicate,
      non la gestione sicura degli accessi.

  - **Integrazione Personalizzata/Esterna (per luigid):**

    - **Reverse Proxy:** L'approccio universalmente consigliato per
      mettere in sicurezza l'interfaccia web di luigid è posizionarla
      dietro un reverse proxy (es. Nginx, Apache HTTP Server, Caddy,
      Traefik) che gestisca l'autenticazione (es. Basic Auth,
      autenticazione basata su certificati client, integrazione con
      sistemi SSO tramite moduli del proxy).<sup>134</sup>

    - **LDAP/OIDC/SAML:** Qualsiasi integrazione con questi protocolli
      IdP avverrebbe esclusivamente tramite il reverse proxy. Luigi
      stesso non interagisce con questi sistemi per l'autenticazione
      dell'UI. Il progetto luigi-project (un framework UI separato, da
      non confondere con l'orchestratore Luigi) ha un plugin OIDC
      <sup>137</sup>, ma questo non è applicabile direttamente alla
      messa in sicurezza di luigid.

    - **RBAC:** Non esiste un sistema RBAC nativo per luigid. Qualsiasi
      forma di controllo degli accessi sarebbe molto grossolana (es.
      permettere o negare l'accesso all'intera UI) e gestita interamente
      dal reverse proxy. Non c'è modo di definire ruoli o permessi
      granulari all'interno di Luigi per l'accesso all'UI.

  - **Considerazioni per On-Premise K8s:**

    - È indispensabile deployare luigid dietro un reverse proxy che
      fornisca autenticazione se l'accesso all'UI deve essere ristretto.

    - Configurare NetworkPolicies in Kubernetes per limitare l'accesso
      diretto al pod/servizio di luigid, forzando il traffico attraverso
      il proxy.

    - La sicurezza dei task stessi (es. credenziali usate dai task per
      connettersi a database) è responsabilità dello sviluppatore del
      task e deve essere gestita tramite meccanismi standard (es. K8s
      Secrets montati nei pod KubernetesJobTask).

Il central scheduler di Luigi è fondamentalmente uno strumento di
visualizzazione e locking con una sicurezza intrinseca minima o nulla.
La sua messa in sicurezza in un ambiente on-premise è interamente una
questione di infrastruttura esterna. Per qualsiasi ambiente multiutente
o che gestisce dati sensibili, Luigi è utilizzabile solo se viene
implementato un robusto livello di autenticazione/autorizzazione esterno
davanti alla sua UI. Questo lo rende meno adatto per organizzazioni che
cercano un orchestratore con funzionalità di sicurezza integrate e
pronte all'uso.

## **5. Analisi Comparativa**

Questa sezione confronta i sistemi di orchestrazione analizzati sulla
base di diversi criteri chiave, con un focus particolare sulle loro
capacità di autenticazione e autorizzazione in contesti on-premise su
Kubernetes.

**5.1. Set di Funzionalità e Funzionalità**

- **Definizione dei Workflow:**

  - **Apache Airflow, Luigi, Dagster, Prefect, Flyte:** Utilizzano
    principalmente Python per la definizione dei workflow, offrendo
    grande flessibilità e la possibilità di creare logiche complesse e
    dinamiche.<sup>2</sup> Airflow e Luigi sono tradizionalmente basati
    su DAG, mentre Dagster introduce il concetto di "asset" come entità
    di prima classe <sup>2</sup>, e Prefect e Flyte enfatizzano workflow
    più dinamici e Python-nativi.<sup>5</sup>

  - **Argo Workflows:** Definisce i workflow tramite YAML, in linea con
    le CRD di Kubernetes, rendendolo intrinsecamente
    container-native.<sup>8</sup>

  - **Temporal:** Utilizza un approccio "workflow-as-code" con SDK in
    vari linguaggi (Go, Java, Python, etc.), permettendo di scrivere
    logica di workflow complessa direttamente nel codice
    applicativo.<sup>121</sup>

- **Capacità di Schedulazione:**

  - **Airflow:** Offre un sistema di schedulazione robusto basato su
    espressioni cron e intervalli, con la possibilità di trigger esterni
    tramite sensori.<sup>3</sup>

  - **Dagster, Prefect, Flyte:** Supportano schedulazioni cron, basate
    su intervalli e, in modo significativo, trigger event-driven tramite
    sensori o meccanismi simili, permettendo un'orchestrazione più
    reattiva.<sup>2</sup>

  - **Argo Workflows:** Dispone di CronWorkflows per la schedulazione
    periodica e può essere integrato con Argo Events per trigger
    event-driven.<sup>2</sup>

  - **Temporal:** I workflow possono essere avviati su richiesta,
    schedulati (tramite funzionalità di "scheduled start") o triggerati
    da eventi esterni tramite segnali.<sup>11</sup>

  - **Luigi:** Non ha un sistema di schedulazione avanzato integrato; si
    affida tipicamente a cron esterno per l'avvio periodico dei
    workflow.<sup>128</sup>

- **Monitoraggio e Osservabilità:**

  - Tutti gli strumenti forniscono interfacce utente per il
    monitoraggio, ma con livelli di dettaglio e usabilità variabili.
    Airflow <sup>2</sup>, Dagster <sup>32</sup> e Prefect <sup>5</sup>
    offrono UI web ricche. L'UI di Argo Workflows <sup>94</sup> e Flyte
    <sup>10</sup> sono funzionali ma talvolta considerate più orientate
    agli sviluppatori o meno feature-rich. L'UI di Luigi (luigid) è la
    più basilare.<sup>1</sup>

  - Il logging è una funzionalità standard, ma la persistenza e
    l'aggregazione in K8s richiedono configurazione (es. volumi
    persistenti, integrazione con sistemi di logging centralizzati).

  - Dagster e Flyte pongono una forte enfasi sul data lineage e sulla
    tracciabilità degli asset/dati.<sup>10</sup>

- **Gestione dei Dati e Error Handling:**

  - Il passaggio di dati tra task è gestito diversamente: XComs in
    Airflow (con limitazioni) <sup>35</sup>, IO Managers in Dagster
    <sup>4</sup>, output/input diretti in Prefect e Flyte (spesso via
    object storage) <sup>6</sup>, artefatti in Argo Workflows
    <sup>9</sup>, e activity results/workflow state in
    Temporal.<sup>120</sup>

  - Tutti gli strumenti offrono meccanismi di retry e gestione degli
    errori, ma Temporal è particolarmente robusto in questo ambito
    grazie alla sua architettura stateful e duratura.<sup>7</sup>

- **Estensibilità:**

  - Airflow è noto per la sua vasta libreria di operatori e
    plugin.<sup>3</sup> Dagster, Prefect e Flyte sono anch'essi
    estensibili tramite codice Python e plugin.<sup>2</sup> Argo
    Workflows e Temporal, essendo più focalizzati sull'esecuzione di
    codice arbitrario in container o come funzioni, sono intrinsecamente
    estensibili. Si osserva una divergenza negli approcci: Airflow e
    Luigi rappresentano orchestratori di task più tradizionali. Dagster
    e Prefect si concentrano maggiormente sull'esperienza dello
    sviluppatore e sulla gestione dei dati come asset. Argo Workflows,
    Flyte e Temporal sono più orientati al cloud-native, al
    "workflow-as-code" e a scenari event-driven. La scelta del set di
    funzionalità "migliore" dipende fortemente dall'ecosistema esistente
    dell'organizzazione, dalle competenze del team e dalla natura dei
    workflow di dati (ETL, ML, event-driven, processi di business di
    lunga durata).

**5.2. Facilità d'Uso, Deployment e Manutenzione**

- **Curva di Apprendimento:**

  - Luigi è generalmente considerato il più semplice per iniziare, data
    la sua natura Pythonic diretta e il focus su job
    batch.<sup>130</sup>

  - Prefect e Dagster mirano a una buona esperienza sviluppatore e
    possono essere relativamente facili da approcciare per chi ha
    familiarità con Python, sebbene i loro concetti più avanzati (asset,
    blocchi, IO manager) richiedano studio.<sup>55</sup>

  - Airflow ha una curva di apprendimento più ripida a causa della sua
    architettura complessa e dei numerosi concetti da
    assimilare.<sup>35</sup>

  - Argo Workflows e Flyte, essendo K8s-native, richiedono una solida
    comprensione di Kubernetes per il deployment e la
    gestione.<sup>64</sup>

  - Temporal presenta una curva di apprendimento significativa a causa
    del suo paradigma di programmazione unico e dei concetti di workflow
    duraturi.<sup>80</sup>

- **Complessità del Deployment K8s:**

  - Strumenti con Helm chart ufficiali e ben mantenuti (Airflow
    <sup>14</sup>, Dagster <sup>16</sup>, Prefect <sup>18</sup>, Flyte
    <sup>23</sup>) o Operator (Temporal <sup>25</sup>) tendono a
    semplificare il deployment iniziale.

  - Argo Workflows, essendo una CRD K8s, si integra nativamente ma la
    sua configurazione può essere dettagliata.<sup>8</sup>

  - Luigi richiede una configurazione più manuale per l'esecuzione dei
    task in K8s (KubernetesJobTask) e per il deployment del central
    scheduler.<sup>28</sup>

- **Overhead Operativo On-Premise:**

  - Strumenti con più dipendenze esterne (es. Airflow che necessita di
    un database robusto e opzionalmente Celery con un message broker
    <sup>33</sup>; Temporal che richiede un database e Elasticsearch
    <sup>5</sup>) comportano un maggiore overhead di gestione
    on-premise.

  - La necessità di configurare reverse proxy per l'autenticazione
    UI/API per Dagster OSS, Prefect OSS e Luigi luigid aggiunge un
    ulteriore livello di complessità operativa.<sup>63</sup>

- **Qualità della Documentazione (per OSS K8s):**

  - Airflow, data la sua maturità, ha una documentazione vasta, sebbene
    a volte possa essere dispersiva.

  - La documentazione per le configurazioni OSS K8s di strumenti più
    recenti o con un forte focus commerciale sulla versione cloud può
    talvolta essere meno completa o aggiornata rispetto alle loro
    controparti cloud.<sup>32</sup> Gli strumenti K8s-native come Argo
    Workflows e Flyte possono integrarsi più facilmente in un ecosistema
    Kubernetes esistente se le competenze K8s sono elevate, ma possono
    risultare complessi in caso contrario. Il costo totale di proprietà
    (TCO) per le soluzioni on-premise non riguarda solo il software
    (gratuito), ma anche l'infrastruttura e le competenze umane
    necessarie per implementarle, metterle in sicurezza e mantenerle.

**5.3. Scalabilità e Prestazioni**

- **Scalabilità Orizzontale:**

  - Gli strumenti K8s-native (Argo Workflows, Flyte) e quelli con
    architetture di worker distribuite che si mappano bene su K8s
    (Airflow con KubernetesExecutor, Dagster e Prefect con i rispettivi
    executor K8s, Temporal) sono generalmente più scalabili
    orizzontalmente per l'esecuzione dei task/workflow.<sup>2</sup> Ogni
    task o workflow può essere eseguito in un pod separato, permettendo
    a Kubernetes di gestire la scalabilità.

  - Luigi è spesso citato come meno scalabile per workflow estremamente
    grandi o complessi, data la sua architettura più centralizzata per
    alcuni aspetti.<sup>1</sup>

- **Prestazioni dello Scheduler/Control Plane:**

  - Lo scheduler di Airflow può diventare un bottleneck in installazioni
    molto grandi se non attentamente configurato e scalato (es. con più
    istanze in modalità HA).

  - I control plane di Flyte (FlyteAdmin) e Temporal (Temporal Server
    con i suoi servizi shardati) sono progettati per la scalabilità.

  - Il daemon di Dagster e il server di Prefect, quando deployati su
    K8s, possono essere scalati, ma la logica di schedulazione
    centralizzata potrebbe avere limiti intrinseci rispetto ad
    architetture completamente distribuite.

  - Argo Workflows affida gran parte della schedulazione a Kubernetes
    stesso.

- **Gestione di Elevati Volumi di Workflow/Task:**

  - La capacità di gestire un gran numero di DAG/workflow e task dipende
    dall'efficienza del database dei metadati, dalla capacità dello
    scheduler/control plane di gestire il carico e dall'efficienza con
    cui i worker vengono allocati e rilasciati. Gli strumenti K8s-native
    beneficiano della capacità di K8s di gestire rapidamente la
    creazione e distruzione di pod. La scelta dipende dalle esigenze di
    scala attuali e future. Sovradimensionare per uno strumento meno
    scalabile o sottostimare la complessità di scalare uno strumento
    distribuito può essere costoso.

**5.4. Maturità, Comunità ed Ecosistema**

- **Maturità del Progetto:**

  - Apache Airflow e Luigi sono i progetti più maturi, con una lunga
    storia di utilizzo in produzione.<sup>1</sup>

  - Dagster, Prefect, Flyte e Temporal sono più recenti ma hanno
    guadagnato una significativa trazione e maturità, spesso
    introducendo paradigmi più moderni.<sup>29</sup>

  - Argo Workflows beneficia dell'essere parte dell'ecosistema CNCF e
    della sua stretta integrazione con Kubernetes.<sup>9</sup>

- **Dimensioni e Attività della Comunità:**

  - Airflow ha di gran lunga la comunità più grande e attiva, con un
    vasto ecosistema di provider, plugin e risorse di
    supporto.<sup>1</sup>

  - Le comunità di Dagster, Prefect, Flyte e Temporal sono in crescita e
    molto attive, spesso con un forte supporto diretto dagli
    sviluppatori principali tramite canali come Slack.<sup>29</sup>

  - La comunità di Luigi per lo sviluppo core è considerata meno attiva
    rispetto ad Airflow.<sup>128</sup>

- **Ecosistema e Integrazioni:**

  - Airflow eccelle per il numero di integrazioni di terze parti
    disponibili.<sup>36</sup>

  - Strumenti più recenti stanno rapidamente espandendo le loro
    integrazioni, spesso concentrandosi sullo stack di dati moderno (es.
    dbt, data lake, piattaforme ML).

- **Qualità della Documentazione e Supporto per OSS On-Prem K8s:**

  - La qualità varia. Airflow ha molta documentazione, ma può essere
    difficile navigare. Per gli strumenti più nuovi, la documentazione
    per scenari OSS on-premise complessi, specialmente per la sicurezza,
    potrebbe non essere sempre al livello di quella per le loro offerte
    cloud. Una comunità ampia spesso significa soluzioni più prontamente
    disponibili per problemi comuni e più strumenti di terze parti, ma
    non equivale sempre a una migliore idoneità per esigenze moderne
    specifiche come l'autenticazione nativa K8s o l'approccio
    asset-centric.

**5.5. Sicurezza: Autenticazione e Autorizzazione**

La tabella seguente riassume le capacità di autenticazione e
autorizzazione per le versioni open source self-hosted su Kubernetes
degli strumenti analizzati.

<table>
<colgroup>
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 12%" />
</colgroup>
<thead>
<tr>
<th><strong>Caratteristica / Strumento</strong></th>
<th><strong>Apache Airflow (FAB)</strong></th>
<th><strong>Dagster (OSS Dagit)</strong></th>
<th><strong>Prefect (OSS Server)</strong></th>
<th><strong>Argo Workflows</strong></th>
<th><strong>Flyte (OSS Admin)</strong></th>
<th><strong>Temporal (Self-Hosted)</strong></th>
<th><strong>Luigi (luigid)</strong></th>
</tr>
<tr>
<th><strong>Auth UI/API Nativa (OSS K8s)</strong></th>
<th>DB (Username/Pwd) <sup>41</sup></th>
<th>Nessuna <sup>61</sup></th>
<th>Basic Auth (User:Pwd) <sup>82</sup></th>
<th>Opzionale: Token K8s (client mode), SSO <sup>99</sup></th>
<th>OIDC/OAuth2 <sup>112</sup></th>
<th>mTLS, Plugin Custom (JWT) <sup>125</sup></th>
<th>Nessuna <sup>131</sup></th>
</tr>
<tr>
<th><strong>RBAC Nativo (OSS K8s)</strong></th>
<th>Granulare (Ruoli FAB, permessi DAG) <sup>41</sup></th>
<th>Nessuno (solo UI read-only) <sup>63</sup></th>
<th>Nessuno (Basic Auth è singolo livello) <sup>73</sup></th>
<th>K8s RBAC per pod; SSO RBAC (mappa OIDC a SA) <sup>101</sup></th>
<th>K8s RBAC per pod; Auth API non RBAC OSS <sup>114</sup></th>
<th>Plugin Custom Authorizer <sup>125</sup></th>
<th>Nessuno</th>
</tr>
<tr>
<th><strong>Integrazione LDAP (OSS K8s)</strong></th>
<th>Diretta (via FAB) <sup>45</sup></th>
<th>Via Reverse Proxy <sup>70</sup></th>
<th>Via Reverse Proxy <sup>89</sup></th>
<th>Via OIDC Bridge (es. Dex) <sup>102</sup></th>
<th>Via OIDC Bridge (es. Keycloak) <sup>112</sup></th>
<th>Via OIDC Bridge + Plugin Custom <sup>126</sup></th>
<th>Via Reverse Proxy</th>
</tr>
<tr>
<th><strong>Integrazione OIDC (OSS K8s)</strong></th>
<th>Diretta (via FAB) <sup>46</sup></th>
<th>Via Reverse Proxy <sup>63</sup></th>
<th>Via Reverse Proxy <sup>87</sup></th>
<th>Diretta (Argo Server) <sup>101</sup></th>
<th>Diretta (FlyteAdmin) <sup>112</sup></th>
<th>Plugin Custom ClaimMapper (JWT) <sup>126</sup></th>
<th>Via Reverse Proxy</th>
</tr>
<tr>
<th><strong>Integrazione SAML (OSS K8s)</strong></th>
<th>Via FAB (custom o OIDC bridge) <sup>48</sup></th>
<th>Via Reverse Proxy <sup>63</sup></th>
<th>Via Reverse Proxy <sup>87</sup></th>
<th>Via OIDC Bridge (es. Dex con SAML IdP) <sup>104</sup></th>
<th>Via OIDC Bridge (es. Keycloak con SAML IdP) <sup>112</sup></th>
<th>Via OIDC Bridge + Plugin Custom <sup>126</sup></th>
<th>Via Reverse Proxy</th>
</tr>
<tr>
<th><strong>Meccanismo Auth/Authz K8s Primario</strong></th>
<th>K8s SA per worker pod; FAB per UI/API</th>
<th>K8s SA per job pod; Proxy per UI/API</th>
<th>K8s SA per flow run pod; Proxy per UI/API</th>
<th>K8s RBAC e SA per pod; Token K8s o OIDC per API</th>
<th>K8s RBAC e SA per pod; OIDC per API/UI</th>
<th>K8s SA per worker pod; Plugin Custom per API</th>
<th>K8s SA per task pod; Proxy per UI</th>
</tr>
<tr>
<th><strong>Facilità Integrazione Sicurezza Custom</strong></th>
<th>Media (config. FAB)</th>
<th>Alta (necessario proxy esterno)</th>
<th>Alta (necessario proxy esterno)</th>
<th>Media-Alta (config. K8s RBAC, OIDC)</th>
<th>Media-Alta (config. OIDC, K8s RBAC)</th>
<th>Alta (richiede sviluppo plugin Go)</th>
<th>Alta (necessario proxy esterno)</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

Per ottenere un'autenticazione di livello enterprise (SSO OIDC/SAML) e
un RBAC granulare in installazioni OSS K8s self-hosted, la maggior parte
degli strumenti richiede una configurazione esterna significativa
(reverse proxy, integrazione IdP) o uno sviluppo personalizzato. Gli
strumenti K8s-native tendono a delegare l'autorizzazione dell'esecuzione
al RBAC di Kubernetes. Airflow si distingue per le opzioni più integrate
tramite FAB. Argo Workflows e Flyte offrono una buona integrazione OIDC
per il loro control plane. Dagster, Prefect (versioni OSS) e Luigi si
affidano principalmente a soluzioni esterne per la sicurezza
dell'UI/API. Temporal offre un framework potente ma che richiede
sviluppo per l'auth/authz personalizzata. La scelta dell'approccio di
sicurezza "migliore" dipende fortemente dall'infrastruttura di identity
management esistente nell'organizzazione, dalle competenze interne su
Kubernetes e dalla disponibilità di risorse di sviluppo. Non esiste uno
strumento "più sicuro" pronto all'uso per tutti gli scenari on-premise.

**Tabella: Riepilogo Generale Pro e Contro (Contesto On-Premise K8s &
Sicurezza)**

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome Strumento</strong></th>
<th><strong>Pro Chiave (On-Prem K8s &amp; Auth)</strong></th>
<th><strong>Contro Chiave (On-Prem K8s &amp; Auth)</strong></th>
</tr>
<tr>
<th>Apache Airflow</th>
<th>Auth/RBAC UI/API maturo e integrato (FAB); Scalabile con
K8sExecutor; Vasta comunità.</th>
<th>Complesso da configurare e gestire on-prem; Curva di apprendimento
ripida per la sicurezza FAB; Gestione Fernet key critica.</th>
</tr>
<tr>
<th>Dagster (OSS)</th>
<th>Ottima esperienza di sviluppo locale; Forte lineage e osservabilità;
Helm chart per K8s.</th>
<th>Nessuna auth/RBAC UI/API nativa in OSS; Richiede reverse proxy per
sicurezza; Comunità più piccola.</th>
</tr>
<tr>
<th>Prefect (OSS)</th>
<th>Pythonic e dinamico; Buona esperienza sviluppatore; Helm chart per
K8s; Basic Auth nativa.</th>
<th>RBAC/SSO avanzato solo in Cloud; Richiede reverse proxy per auth
UI/API robusta; Documentazione OSS per auth complessa limitata.</th>
</tr>
<tr>
<th>Argo Workflows</th>
<th>K8s-native (CRD); Scalabile; Auth API via token K8s o OIDC; SSO RBAC
mappa utenti OIDC a SA K8s.</th>
<th>Richiede forte expertise K8s per auth/RBAC; UI più semplice; Setup
OIDC/RBAC può essere complesso.</th>
</tr>
<tr>
<th>Flyte (OSS)</th>
<th>K8s-native; Fortemente tipizzato e versionato; Auth API/UI via OIDC;
K8s RBAC per esecuzione task.</th>
<th>RBAC granulare utenti Flyte OSS meno chiaro; Richiede expertise K8s;
Comunità più piccola.</th>
</tr>
<tr>
<th>Temporal</th>
<th>Altamente affidabile e scalabile per workflow stateful; Auth/Authz
API flessibile tramite plugin custom; Supporto mTLS nativo.</th>
<th>Richiede sviluppo custom (Go) per ClaimMapper/Authorizer; Overhead
operativo per DB/Elasticsearch; Curva di apprendimento ripida.</th>
</tr>
<tr>
<th>Luigi</th>
<th>Semplice per batch Python; KubernetesJobTask per K8s.</th>
<th>Nessuna auth/RBAC nativa per UI (luigid); Richiede reverse proxy per
qualsiasi sicurezza UI; Scalabilità limitata; UI basilare.</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## **6. Raccomandazioni e Conclusioni**

**Riepilogo dei Requisiti Utente:** La richiesta principale verte sulla
selezione di un sistema di orchestrazione open source, implementabile
on-premise in un ambiente Kubernetes, con una particolare attenzione
alla disponibilità e personalizzazione dei meccanismi di autenticazione
e autorizzazione.

**Raccomandazioni Personalizzate:**

- **Scenario 1: Massima Integrazione con Sicurezza K8s-Native e
  Competenze K8s Avanzate Esistenti:**

  - **Argo Workflows** o **Flyte** emergono come scelte primarie.
    Entrambi sono profondamente integrati con Kubernetes. Argo Workflows
    utilizza direttamente i token bearer K8s o l'OIDC per
    l'autenticazione dell'Argo Server e si affida pesantemente al RBAC
    di Kubernetes, con la possibilità di mappare utenti/gruppi OIDC a
    ServiceAccount K8s per un controllo più fine.<sup>99</sup> Flyte
    adotta OIDC per l'autenticazione del suo control plane (FlyteAdmin)
    e utilizza il RBAC di K8s per i permessi di esecuzione dei
    task.<sup>112</sup> La familiarità con il RBAC di K8s è cruciale per
    entrambi.

- **Scenario 2: Necessità di Funzionalità Auth/RBAC Integrate Ricche e
  Ecosistema Python Maturo:**

  - **Apache Airflow** si distingue per le sue capacità di
    autenticazione e RBAC più complete integrate nella versione open
    source, grazie a Flask AppBuilder (FAB).<sup>41</sup> Offre supporto
    nativo (tramite FAB) per LDAP, OAuth/OIDC e un modello RBAC
    granulare. Questo riduce la necessità di componenti esterni per la
    sicurezza base dell'UI/API, ma richiede una configurazione attenta
    di FAB.

- **Scenario 3: Flessibilità per Auth Personalizzata e Workflow Stateful
  Complessi:**

  - **Temporal** offre il modello più flessibile per l'autenticazione e
    l'autorizzazione grazie alle sue interfacce ClaimMapper e
    Authorizer.<sup>125</sup> Questo permette un'integrazione su misura
    con qualsiasi sistema di identità, ma richiede uno sforzo di
    sviluppo significativo (tipicamente in Go). È ideale se
    l'organizzazione ha le risorse per tale sviluppo e necessita della
    durabilità di Temporal per workflow complessi.

- **Scenario 4: Approccio Moderno Asset-Centric e Disponibilità a
  Gestire Auth Esterna:**

  - **Dagster (OSS)** o **Prefect (OSS)** sono validi se le loro moderne
    filosofie di sviluppo (asset-centric per Dagster, Pythonic e
    dinamico per Prefect) sono prioritarie e il team è disposto a
    implementare e gestire l'autenticazione per l'UI/API tramite un
    reverse proxy.<sup>63</sup> Questo permette di sfruttare IdP
    esistenti (LDAP, OIDC, SAML) tramite il proxy.

- **Scenario 5: Workflow Batch più Semplici e Sicurezza Esterna Basilare
  Sufficiente:**

  - **Luigi** potrebbe essere considerato se i workflow sono
    relativamente semplici, l'ambiente è strettamente controllato, e una
    semplice autenticazione gestita da un reverse proxy davanti all'UI
    di luigid è accettabile.<sup>134</sup> Le sue capacità di sicurezza
    intrinseche sono nulle.

**Considerazioni Chiave per la Decisione Finale:**

- **Infrastruttura di Identity Provider Esistente:** La compatibilità e
  la facilità di integrazione con sistemi LDAP, OIDC o SAML aziendali
  esistenti sono fondamentali. Strumenti con supporto OIDC diretto
  (Argo, Flyte, Airflow via FAB) o che si integrano facilmente tramite
  proxy (Dagster, Prefect) possono essere preferibili.

- **Competenze del Team su Kubernetes e Sicurezza:** Strumenti
  K8s-native come Argo Workflows e Flyte richiedono una profonda
  comprensione di K8s RBAC. La configurazione sicura di Airflow (FAB,
  Fernet key) o lo sviluppo di plugin per Temporal richiedono competenze
  specifiche.

- **Risorse di Sviluppo Disponibili per Integrazione Personalizzata:**
  Se si sceglie Temporal o si necessita di integrazioni auth complesse
  per Dagster/Prefect/Luigi tramite proxy, è necessario allocare risorse
  di sviluppo.

- **Complessità e Tipologia dei Workflow di Dati:** Workflow ETL
  tradizionali, pipeline ML, processi event-driven o task di lunga
  durata stateful possono indirizzare verso strumenti con
  caratteristiche più adatte (es. Temporal per stateful, Flyte/Dagster
  per ML, Airflow per ETL generico).

- **Overhead Operativo e di Manutenzione a Lungo Termine:** Considerare
  la complessità della gestione on-premise dello strumento stesso, delle
  sue dipendenze (database, message queue, Elasticsearch) e dei
  componenti di sicurezza aggiuntivi (reverse proxy, IdP).

**Considerazioni Conclusive:** La scelta ottimale di un sistema di
orchestrazione è fortemente dipendente dal contesto specifico
dell'organizzazione. Questo rapporto fornisce le informazioni tecniche
necessarie per prendere una decisione informata, allineata con le
capacità tecniche, la postura di sicurezza e la visione della data
platform aziendale. Si sottolinea l'importanza di effettuare Proof of
Concept (PoC) per validare le integrazioni di sicurezza e la
compatibilità con i carichi di lavoro specifici prima di una decisione
definitiva. La scelta di un orchestratore per ambienti on-premise
Kubernetes non riguarda solo le funzionalità, ma anche la maturità
operativa richiesta per metterlo in sicurezza e mantenerlo. "Open
Source" non equivale a "costo operativo zero", specialmente per quanto
riguarda la sicurezza. Un'implementazione di successo richiede una
visione olistica che includa l'orchestratore stesso, le sue dipendenze,
l'ambiente Kubernetes e i componenti di sicurezza esterni.

#### Bibliografia

1.  Apache Airflow vs Luigi-The Tale of Two Workflow Managers -
    ProjectPro, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://www.projectpro.io/article/apache-airflow-vs-luigi/750</u>](https://www.projectpro.io/article/apache-airflow-vs-luigi/750)

2.  12 Best Open-Source Data Orchestration Tools in 2025 - Airbyte,
    accesso eseguito il giorno maggio 9, 2025,
    [<u>https://airbyte.com/top-etl-tools-for-sources/data-orchestration-tools</u>](https://airbyte.com/top-etl-tools-for-sources/data-orchestration-tools)

3.  Apache Airflow: Definition, Architecture Overview, Use Cases - Data
    Engineer Academy, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://dataengineeracademy.com/blog/apache-airflow-architecture-overview-use-cases/</u>](https://dataengineeracademy.com/blog/apache-airflow-architecture-overview-use-cases/)

4.  Open Source deployment architecture overview | Dagster Docs, accesso
    eseguito il giorno maggio 9, 2025,
    [<u>https://docs.dagster.io/guides/deploy/oss-deployment-architecture</u>](https://docs.dagster.io/guides/deploy/oss-deployment-architecture)

5.  Self-hosted Temporal Workflows made easy with Northflank, accesso
    eseguito il giorno maggio 9, 2025,
    [<u>https://northflank.com/guides/self-hosted-temporal-workflows-made-easy-with-northflank</u>](https://northflank.com/guides/self-hosted-temporal-workflows-made-easy-with-northflank)

6.  Prefect architecture overview — Restack, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://www.restack.io/docs/prefect-knowledge-prefect-architecture-guide</u>](https://www.restack.io/docs/prefect-knowledge-prefect-architecture-guide)

7.  Top Open Source Workflow Orchestration Tools in 2025 - Bytebase,
    accesso eseguito il giorno maggio 9, 2025,
    [<u>https://www.bytebase.com/blog/top-open-source-workflow-orchestration-tools/</u>](https://www.bytebase.com/blog/top-open-source-workflow-orchestration-tools/)

8.  What is Argo Workflows? Templates, Use Cases & Tutorial - Spacelift,
    accesso eseguito il giorno maggio 9, 2025,
    [<u>https://spacelift.io/blog/argo-workflows</u>](https://spacelift.io/blog/argo-workflows)

9.  The workflow engine for Kubernetes - Argo Workflows, accesso
    eseguito il giorno maggio 9, 2025,
    [<u>https://argo-workflows.readthedocs.io/en/latest/</u>](https://argo-workflows.readthedocs.io/en/latest/)

10. User guide | Union.ai Docs, accesso eseguito il giorno maggio 9,
    2025,
    [<u>https://docs.flyte.org/en/latest/user\_guide/introduction.html</u>](https://docs.flyte.org/en/latest/user_guide/introduction.html)

11. Temporal development and production features, accesso eseguito il
    giorno maggio 9, 2025,
    [<u>https://docs.temporal.io/evaluate/development-production-features</u>](https://docs.temporal.io/evaluate/development-production-features)

12. How to Build a Data Orchestration Pipeline Using Luigi in Python? -
    Airbyte, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://airbyte.com/data-engineering-resources/luigi-python-data-pipeline</u>](https://airbyte.com/data-engineering-resources/luigi-python-data-pipeline)

13. Understanding Apache Airflow License - FAQ October 2024 - Restack,
    accesso eseguito il giorno maggio 9, 2025,
    [<u>https://www.restack.io/docs/airflow-faq-database-erd-ref-09</u>](https://www.restack.io/docs/airflow-faq-database-erd-ref-09)

14. Kubernetes — Airflow Documentation, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/kubernetes.html</u>](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/kubernetes.html)

15. dagster/LICENSE at master - GitHub, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://github.com/dagster-io/dagster/blob/master/LICENSE</u>](https://github.com/dagster-io/dagster/blob/master/LICENSE)

16. Deploying Dagster to Kubernetes with Helm, accesso eseguito il
    giorno maggio 9, 2025,
    [<u>https://docs.dagster.io/guides/deploy/deployment-options/kubernetes/deploying-to-kubernetes</u>](https://docs.dagster.io/guides/deploy/deployment-options/kubernetes/deploying-to-kubernetes)

17. prefect/LICENSE at main - GitHub, accesso eseguito il giorno maggio
    9, 2025,
    [<u>https://github.com/PrefectHQ/prefect/blob/main/LICENSE</u>](https://github.com/PrefectHQ/prefect/blob/main/LICENSE)

18. prefect-kubernetes, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://docs.prefect.io/integrations/prefect-kubernetes</u>](https://docs.prefect.io/integrations/prefect-kubernetes)

19. Helm - Prefect Docs, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://docs.prefect.io/v3/manage/server/examples/helm</u>](https://docs.prefect.io/v3/manage/server/examples/helm)

20. Apache License 2.0 - argoproj/argo-workflows - GitHub, accesso
    eseguito il giorno maggio 9, 2025,
    [<u>https://github.com/argoproj/argo-workflows/blob/master/LICENSE</u>](https://github.com/argoproj/argo-workflows/blob/master/LICENSE)

21. Argo Server - Argo Workflows - The workflow engine for Kubernetes -
    Read the Docs, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://argo-workflows.readthedocs.io/en/latest/argo-server/</u>](https://argo-workflows.readthedocs.io/en/latest/argo-server/)

22. flyte/LICENSE at master · flyteorg/flyte - GitHub, accesso eseguito
    il giorno maggio 9, 2025,
    [<u>https://github.com/flyteorg/flyte/blob/master/LICENSE</u>](https://github.com/flyteorg/flyte/blob/master/LICENSE)

23. Planning your deployment | Union.ai Docs, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://www.union.ai/docs/flyte/deployment/flyte-deployment/planning/</u>](https://www.union.ai/docs/flyte/deployment/flyte-deployment/planning/)

24. MIT license - temporalio/temporal-cafe - GitHub, accesso eseguito il
    giorno maggio 9, 2025,
    [<u>https://github.com/temporalio/temporal-cafe/blob/main/LICENSE</u>](https://github.com/temporalio/temporal-cafe/blob/main/LICENSE)

25. Temporal Operator: Overview, accesso eseguito il giorno maggio 9,
    2025,
    [<u>https://temporal-operator.pages.dev/</u>](https://temporal-operator.pages.dev/)

26. Temporal Operator - OperatorHub.io, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://operatorhub.io/operator/temporal-operator</u>](https://operatorhub.io/operator/temporal-operator)

27. luigi/LICENSE at master · spotify/luigi - GitHub, accesso eseguito
    il giorno maggio 9, 2025,
    [<u>https://github.com/spotify/luigi/blob/master/LICENSE</u>](https://github.com/spotify/luigi/blob/master/LICENSE)

28. luigi.contrib.kubernetes module — Luigi 3.6.0 documentation, accesso
    eseguito il giorno maggio 9, 2025,
    [<u>https://luigi.readthedocs.io/en/latest/api/luigi.contrib.kubernetes.html</u>](https://luigi.readthedocs.io/en/latest/api/luigi.contrib.kubernetes.html)

29. Top 17 Data Orchestration Tools for 2025: Ultimate Review - lakeFS,
    accesso eseguito il giorno maggio 9, 2025,
    [<u>https://lakefs.io/blog/data-orchestration-tools-2023/</u>](https://lakefs.io/blog/data-orchestration-tools-2023/)

30. Argo Support: All the Options to Get Support for Argo Projects |
    Codefresh, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://codefresh.io/learn/argo-cd/argo-support-all-the-options-to-get-support-for-argo-projects/</u>](https://codefresh.io/learn/argo-cd/argo-support-all-the-options-to-get-support-for-argo-projects/)

31. luigi vs prefect: Which Tool is Better for Your Next Project? -
    ProjectPro, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://www.projectpro.io/compare/luigi-vs-prefect</u>](https://www.projectpro.io/compare/luigi-vs-prefect)

32. For those who have worked with Airflow and Dagster. Is Airflow in
    any aspect better? : r/dataengineering - Reddit, accesso eseguito il
    giorno maggio 9, 2025,
    [<u>https://www.reddit.com/r/dataengineering/comments/126js1x/for\_those\_who\_have\_worked\_with\_airflow\_and/</u>](https://www.reddit.com/r/dataengineering/comments/126js1x/for_those_who_have_worked_with_airflow_and/)

33. Production Deployment — Airflow Documentation, accesso eseguito il
    giorno maggio 9, 2025,
    [<u>https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/production-deployment.html</u>](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/production-deployment.html)

34. Architecture Overview — Airflow Documentation, accesso eseguito il
    giorno maggio 9, 2025,
    [<u>https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html</u>](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)

35. Apache Airflow Overview - Geniusee, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://geniusee.com/single-blog/apache-airflow-overview-what-it-is-and-how-it-works</u>](https://geniusee.com/single-blog/apache-airflow-overview-what-it-is-and-how-it-works)

36. Apache Airflow, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://airflow.apache.org/</u>](https://airflow.apache.org/)

37. Documentation | Apache Airflow, accesso eseguito il giorno maggio 9,
    2025,
    [<u>https://airflow.apache.org/docs/</u>](https://airflow.apache.org/docs/)

38. Apache Airflow Reviews 2025: Details, Pricing, & Features | G2,
    accesso eseguito il giorno maggio 9, 2025,
    [<u>https://www.g2.com/products/apache-airflow/reviews</u>](https://www.g2.com/products/apache-airflow/reviews)

39. Apache Airflow Review 2024: Pricing, Features, Alternatives -
    Datamation, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://www.datamation.com/applications/apache-airflow-review/</u>](https://www.datamation.com/applications/apache-airflow-review/)

40. Top 7 Data Orchestration Tools: 2024 - DataChannel, accesso eseguito
    il giorno maggio 9, 2025,
    [<u>https://www.datachannel.co/blogs/top-7-data-orchestration-tools-2024</u>](https://www.datachannel.co/blogs/top-7-data-orchestration-tools-2024)

41. Securing Airflow: Managing Authentication and Authorization ...,
    accesso eseguito il giorno maggio 9, 2025,
    [<u>https://reintech.io/blog/securing-airflow-authentication-authorization</u>](https://reintech.io/blog/securing-airflow-authentication-authorization)

42. Airflow Authentication and Authorization: A Comprehensive Guide -
    SparkCodehub, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://www.sparkcodehub.com/airflow/advanced/auth</u>](https://www.sparkcodehub.com/airflow/advanced/auth)

43. Flask AppBuilder (FAB) auth manager — apache-airflow-providers-fab
    Documentation, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://airflow.apache.org/docs/apache-airflow-providers-fab/stable/auth-manager/index.html</u>](https://airflow.apache.org/docs/apache-airflow-providers-fab/stable/auth-manager/index.html)

44. Access Control with FAB auth manager — apache-airflow-providers ...,
    accesso eseguito il giorno maggio 9, 2025,
    [<u>https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html</u>](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html)

45. FAB auth manager authentication — apache-airflow-providers-fab
    Documentation, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://airflow.apache.org/docs/apache-airflow-providers-fab/stable/auth-manager/webserver-authentication.html</u>](https://airflow.apache.org/docs/apache-airflow-providers-fab/stable/auth-manager/webserver-authentication.html)

46. Airflow LDAP Integration Guide - Restack, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://www.restack.io/docs/airflow-knowledge-airflow-ldap-integration</u>](https://www.restack.io/docs/airflow-knowledge-airflow-ldap-integration)

47. Implementing Single Sign On (SSO) Authentication in Apache Airflow -
    NextLytics AG, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://www.nextlytics.com/blog/implementing-single-sign-on-sso-authentication-in-apache-airflow</u>](https://www.nextlytics.com/blog/implementing-single-sign-on-sso-authentication-in-apache-airflow)

48. Security — Flask AppBuilder, accesso eseguito il giorno maggio 9,
    2025,
    [<u>https://flask-appbuilder.readthedocs.io/en/latest/security.html#authentication-methods</u>](https://flask-appbuilder.readthedocs.io/en/latest/security.html#authentication-methods)

49. Airflow With Saml - Anaconda.org, accesso eseguito il giorno maggio
    9, 2025,
    [<u>https://anaconda.org/conda-forge/airflow-with-saml</u>](https://anaconda.org/conda-forge/airflow-with-saml)

50. Data Pipeline Architecture: 5 Design Patterns with Examples |
    Dagster Guides, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://dagster.io/guides/data-pipeline/data-pipeline-architecture-5-design-patterns-with-examples</u>](https://dagster.io/guides/data-pipeline/data-pipeline-architecture-5-design-patterns-with-examples)

51. Data Orchestration Tools: 10 Key Features & 10 Platforms to Know |
    Dagster Guides, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://dagster.io/guides/data-platform/data-orchestration-tools-10-key-features-10-platforms-to-know</u>](https://dagster.io/guides/data-platform/data-orchestration-tools-10-key-features-10-platforms-to-know)

52. Data Orchestration Showdown: Airflow vs. Dagster - Trifork, accesso
    eseguito il giorno maggio 9, 2025,
    [<u>https://trifork.com/blog/data-orchestration-showdown-airflow-vs-dagster/</u>](https://trifork.com/blog/data-orchestration-showdown-airflow-vs-dagster/)

53. Concepts | Dagster Docs, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://docs.dagster.io/concepts</u>](https://docs.dagster.io/concepts)

54. Concepts | Dagster Docs, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://docs.dagster.io/getting-started/concepts</u>](https://docs.dagster.io/getting-started/concepts)

55. Catalog - Bring trust and visibility to your data, accesso eseguito
    il giorno maggio 9, 2025,
    [<u>https://www.castordoc.com/fr/data-strategy/dagster-vs-luigi-comparing-two-workflow-tools</u>](https://www.castordoc.com/fr/data-strategy/dagster-vs-luigi-comparing-two-workflow-tools)

56. Data Observability in 2025: Pillars, Pros/Cons & Best Practices |
    Dagster Guides, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://dagster.io/guides/data-governance/data-observability-in-2025-pillars-pros-cons-best-practices</u>](https://dagster.io/guides/data-governance/data-observability-in-2025-pillars-pros-cons-best-practices)

57. Dagster + lakeFS: How to Troubleshoot and Reproduce Data, accesso
    eseguito il giorno maggio 9, 2025,
    [<u>https://lakefs.io/blog/dagster-lakefs-how-to-troubleshoot-and-reproduce-data/</u>](https://lakefs.io/blog/dagster-lakefs-how-to-troubleshoot-and-reproduce-data/)

58. Airflow vs. Dagster: Orchestration Story for your Data Platform -
    DEV Community, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://dev.to/chaets/airflow-vs-dagster-orchestration-story-for-your-data-platform-3pko</u>](https://dev.to/chaets/airflow-vs-dagster-orchestration-story-for-your-data-platform-3pko)

59. Kubernetes agent configuration - Dagster Docs, accesso eseguito il
    giorno maggio 9, 2025,
    [<u>https://docs.dagster.io/dagster-plus/deployment/deployment-types/hybrid/kubernetes/configuration</u>](https://docs.dagster.io/dagster-plus/deployment/deployment-types/hybrid/kubernetes/configuration)

60. Kubernetes agent setup - Dagster Docs, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://docs.dagster.io/dagster-plus/deployment/deployment-types/hybrid/kubernetes/setup</u>](https://docs.dagster.io/dagster-plus/deployment/deployment-types/hybrid/kubernetes/setup)

61. Authentication and access control - Dagster Docs, accesso eseguito
    il giorno maggio 9, 2025,
    [<u>https://docs.dagster.io/dagster-plus/features/authentication-and-access-control/</u>](https://docs.dagster.io/dagster-plus/features/authentication-and-access-control/)

62. User roles and permissions in Dagster+ - Dagster Docs, accesso
    eseguito il giorno maggio 9, 2025,
    [<u>https://docs.dagster.io/dagster-plus/features/authentication-and-access-control/rbac/user-roles-permissions</u>](https://docs.dagster.io/dagster-plus/features/authentication-and-access-control/rbac/user-roles-permissions)

63. Support Auth & RBAC in Dagit · Issue \#2219 · dagster-io/dagster -
    GitHub, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://github.com/dagster-io/dagster/issues/2219</u>](https://github.com/dagster-io/dagster/issues/2219)

64. Data Orchestration Tools That Your Data Team Should Know - Hevo
    Academy, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://hevoacademy.com/tools-and-technologies/best-data-orchestration-tools/</u>](https://hevoacademy.com/tools-and-technologies/best-data-orchestration-tools/)

65. Dagster+ Pricing | Hybrid and serverless deployment, accesso
    eseguito il giorno maggio 9, 2025,
    [<u>https://dagster.io/pricing</u>](https://dagster.io/pricing)

66. Dagster & Dask: Optimize Data Workflow Orchestration | Orchestra,
    accesso eseguito il giorno maggio 9, 2025,
    [<u>https://www.getorchestra.io/guides/dagster-dask-optimize-data-workflow-orchestration</u>](https://www.getorchestra.io/guides/dagster-dask-optimize-data-workflow-orchestration)

67. Role-based access control - Dagster Docs, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://docs.dagster.io/dagster-plus/features/authentication-and-access-control/rbac/</u>](https://docs.dagster.io/dagster-plus/features/authentication-and-access-control/rbac/)

68. Setting up Okta SSO for Dagster+ - Dagster Docs, accesso eseguito il
    giorno maggio 9, 2025,
    [<u>https://docs.dagster.io/dagster-plus/features/authentication-and-access-control/sso/okta-sso</u>](https://docs.dagster.io/dagster-plus/features/authentication-and-access-control/sso/okta-sso)

69. OneLogin SSO - Dagster Docs, accesso eseguito il giorno maggio 9,
    2025,
    [<u>https://docs.dagster.io/dagster-plus/features/authentication-and-access-control/sso/onelogin-sso</u>](https://docs.dagster.io/dagster-plus/features/authentication-and-access-control/sso/onelogin-sso)

70. People happy with dagster, what does your deployment look like? -
    Reddit, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://www.reddit.com/r/dataengineering/comments/1jdhvk7/people\_happy\_with\_dagster\_what\_does\_your/</u>](https://www.reddit.com/r/dataengineering/comments/1jdhvk7/people_happy_with_dagster_what_does_your/)

71. Prefect Docs, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://docs.prefect.io/v3/get-started</u>](https://docs.prefect.io/v3/get-started)

72. Host Prefect server, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://docs.prefect.io/v3/manage/self-host</u>](https://docs.prefect.io/v3/manage/self-host)

73. Prefect server overview, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://docs.prefect.io/v3/manage/server/index</u>](https://docs.prefect.io/v3/manage/server/index)

74. Prefect architecture overview - Restack, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://www.restack.io/docs/prefect-knowledge-prefect-architecture-diagram</u>](https://www.restack.io/docs/prefect-knowledge-prefect-architecture-diagram)

75. Prefect is a workflow orchestration framework for building resilient
    data pipelines in Python. - GitHub, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://github.com/PrefectHQ/prefect</u>](https://github.com/PrefectHQ/prefect)

76. Prefect vs. Airflow: 2025 Comparison for Workflow Orchestration ...,
    accesso eseguito il giorno maggio 9, 2025,
    [<u>https://blog.adyog.com/2025/01/18/prefect-vs-airflow-2025-comparison-for-workflow-orchestration-excellence/</u>](https://blog.adyog.com/2025/01/18/prefect-vs-airflow-2025-comparison-for-workflow-orchestration-excellence/)

77. &lt; Marvin&gt; how can I deploy prefect to my on prem server I al
    Prefect Community \#ask-marvin, accesso eseguito il giorno maggio 9,
    2025,
    [<u>https://linen.prefect.io/t/26821010/ulva73b9p-how-can-i-deploy-prefect-to-my-on-prem-server-i-al</u>](https://linen.prefect.io/t/26821010/ulva73b9p-how-can-i-deploy-prefect-to-my-on-prem-server-i-al)

78. prefect-server 2025.5.2200058 - Artifact Hub, accesso eseguito il
    giorno maggio 9, 2025,
    [<u>https://artifacthub.io/packages/helm/prefect/prefect-server</u>](https://artifacthub.io/packages/helm/prefect/prefect-server)

79. Run flows on Kubernetes - Prefect docs, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://docs.prefect.io/v3/deploy/infrastructure-examples/kubernetes</u>](https://docs.prefect.io/v3/deploy/infrastructure-examples/kubernetes)

80. Airflow vs Temporal vs Prefect: Pros and Cons | bugfree.ai, accesso
    eseguito il giorno maggio 9, 2025,
    [<u>https://www.bugfree.ai/knowledge-hub/airflow-vs-temporal-vs-prefect-pros-and-cons</u>](https://www.bugfree.ai/knowledge-hub/airflow-vs-temporal-vs-prefect-pros-and-cons)

81. Prefect Reviews 2025: Details, Pricing, & Features | G2, accesso
    eseguito il giorno maggio 9, 2025,
    [<u>https://www.g2.com/products/prefect/reviews</u>](https://www.g2.com/products/prefect/reviews)

82. Configure settings and profiles - Prefect Docs, accesso eseguito il
    giorno maggio 9, 2025,
    [<u>https://docs.prefect.io/v3/develop/settings-and-profiles</u>](https://docs.prefect.io/v3/develop/settings-and-profiles)

83. Prefect UI not working with Server API Auth (username:password)
    \#16724 - GitHub, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://github.com/PrefectHQ/prefect/issues/16724</u>](https://github.com/PrefectHQ/prefect/issues/16724)

84. Security: Prefect Shared Responsibility Model, accesso eseguito il
    giorno maggio 9, 2025,
    [<u>https://www.prefect.io/security-prefect-shared-responsibility-model</u>](https://www.prefect.io/security-prefect-shared-responsibility-model)

85. Prefect UI Authentication Guide — Restack, accesso eseguito il
    giorno maggio 9, 2025,
    [<u>https://www.restack.io/docs/prefect-knowledge-prefect-ui-authentication-guide</u>](https://www.restack.io/docs/prefect-knowledge-prefect-ui-authentication-guide)

86. &lt; Marvin&gt; I have a self hosted prefect how do I add security
    Prefect Community \#ask-marvin, accesso eseguito il giorno maggio 9,
    2025,
    [<u>https://linen.prefect.io/t/27112287/ulva73b9p-i-have-a-self-hosted-prefect-how-do-i-add-security</u>](https://linen.prefect.io/t/27112287/ulva73b9p-i-have-a-self-hosted-prefect-how-do-i-add-security)

87. Hi there I m trying to setup auth0 authentication on a self Prefect
    Community \#ask-community, accesso eseguito il giorno maggio 9,
    2025,
    [<u>https://linen.prefect.io/t/27107666/hi-there-i-m-trying-to-setup-auth0-authentication-on-a-self-</u>](https://linen.prefect.io/t/27107666/hi-there-i-m-trying-to-setup-auth0-authentication-on-a-self-)

88. &lt; Marvin&gt; With prefect 3 core the self hosted version is it
    Prefect Community \#marvin-ai, accesso eseguito il giorno maggio 9,
    2025,
    [<u>https://linen.prefect.io/t/27109431/ulva73b9p-with-prefect-3-core-the-self-hosted-version-is-it-</u>](https://linen.prefect.io/t/27109431/ulva73b9p-with-prefect-3-core-the-self-hosted-version-is-it-)

89. Securing Self-Hosted Apps with Pocket ID / OAuth2-Proxy | theSynAck,
    accesso eseguito il giorno maggio 9, 2025,
    [<u>https://thesynack.com/posts/securing-with-oauth2-proxy/?ref=selfh.st</u>](https://thesynack.com/posts/securing-with-oauth2-proxy/?ref=selfh.st)

90. Single Sign-on (SSO) - Prefect Docs, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://orion-docs.prefect.io/2.8.0/ui/sso/</u>](https://orion-docs.prefect.io/2.8.0/ui/sso/)

91. Configure single sign-on (SSO) for your Prefect Cloud users.,
    accesso eseguito il giorno maggio 9, 2025,
    [<u>https://docs.prefect.io/v3/manage/cloud/manage-users/configure-sso</u>](https://docs.prefect.io/v3/manage/cloud/manage-users/configure-sso)

92. Argo Workflows - Google Cloud Console, accesso eseguito il giorno
    maggio 9, 2025,
    [<u>https://console.cloud.google.com/marketplace/product/google/argo-workflows</u>](https://console.cloud.google.com/marketplace/product/google/argo-workflows)

93. click-to-deploy/k8s/argo-workflows/README.md at master - GitHub,
    accesso eseguito il giorno maggio 9, 2025,
    [<u>https://github.com/GoogleCloudPlatform/click-to-deploy/blob/master/k8s/argo-workflows/README.md</u>](https://github.com/GoogleCloudPlatform/click-to-deploy/blob/master/k8s/argo-workflows/README.md)

94. Argo Workflows: The Basics and a Quick Tutorial - Codefresh, accesso
    eseguito il giorno maggio 9, 2025,
    [<u>https://codefresh.io/learn/argo-workflows/</u>](https://codefresh.io/learn/argo-workflows/)

95. codefresh.io, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://codefresh.io/learn/argo-workflows/argo-workflows-vs-airflow-5-key-differences-and-how-to-choose/#:~:text=Argo%20Workflows%2C%20being%20a%20Kubernetes,potentially%20impact%20long%2Dterm%20sustainability.</u>](https://codefresh.io/learn/argo-workflows/argo-workflows-vs-airflow-5-key-differences-and-how-to-choose/#:~:text=Argo%20Workflows%2C%20being%20a%20Kubernetes,potentially%20impact%20long%2Dterm%20sustainability.)

96. Argo Workflows vs. Airflow: 5 Key Differences & How to Choose -
    Codefresh, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://codefresh.io/learn/argo-workflows/argo-workflows-vs-airflow-5-key-differences-and-how-to-choose/</u>](https://codefresh.io/learn/argo-workflows/argo-workflows-vs-airflow-5-key-differences-and-how-to-choose/)

97. 20 Best Workflow Orchestration Tools Reviewed in 2025 - The Digital
    Project Manager, accesso eseguito il giorno maggio 9, 2025,
    [<u>https://thedigitalprojectmanager.com/tools/workflow-orchestration-tools/</u>](https://thedigitalprojectmanager.com/tools/workflow-orchestration-tools/)

98. Common Challenges and Limitations of ArgoCD - Devtron, accesso
    eseguito il giorno maggio 9, 2025,
    [<u>https://devtron.ai/blog/common-challenges-and-limitations-of-argocd/</u>](https://devtron.ai/blog/common-challenges-and-limitations-of-argocd/)

99. Argo Server Auth Mode - Argo Workflows - The workflow engine for
    ..., accesso eseguito il giorno maggio 9, 2025,
    [<u>https://argo-workflows.readthedocs.io/en/latest/argo-server-auth-mode/</u>](https://argo-workflows.readthedocs.io/en/latest/argo-server-auth-mode/)

100. Argo Workflows - Uncovering the Hidden Misconfigurations - E.V.A -
     Information Security, accesso eseguito il giorno maggio 9, 2025,
     [<u>https://www.evasec.io/blog/argo-workflows-uncovering-the-hidden-misconfigurations</u>](https://www.evasec.io/blog/argo-workflows-uncovering-the-hidden-misconfigurations)

101. Argo Server SSO - Argo Workflows - The workflow engine for
     Kubernetes - Read the Docs, accesso eseguito il giorno maggio 9,
     2025,
     [<u>https://argo-workflows.readthedocs.io/en/latest/argo-server-sso/</u>](https://argo-workflows.readthedocs.io/en/latest/argo-server-sso/)

102. 5 Reasons to Use Argo CD for Your Cloud Native Applications -
     CloudTweaks, accesso eseguito il giorno maggio 9, 2025,
     [<u>https://cloudtweaks.com/2025/04/5-reasons-to-use-argo-cd-for-your-cloud-native-applications/</u>](https://cloudtweaks.com/2025/04/5-reasons-to-use-argo-cd-for-your-cloud-native-applications/)

103. Argo Workflows SSO - Tremolo Security, accesso eseguito il giorno
     maggio 9, 2025,
     [<u>https://www.tremolo.io/post/argo-workflows-sso</u>](https://www.tremolo.io/post/argo-workflows-sso)

104. Use Argo CD Dex for authentication, accesso eseguito il giorno
     maggio 9, 2025,
     [<u>https://argo-workflows.readthedocs.io/en/latest/argo-server-sso-argocd/</u>](https://argo-workflows.readthedocs.io/en/latest/argo-server-sso-argocd/)

105. docs/argo-server-sso.md · main · Redpoint Games / Argo Workflows ·
     GitLab, accesso eseguito il giorno maggio 9, 2025,
     [<u>https://src.redpoint.games/redpointgames/argo-workflows/-/blob/main/docs/argo-server-sso.md</u>](https://src.redpoint.games/redpointgames/argo-workflows/-/blob/main/docs/argo-server-sso.md)

106. Security - Argo Workflows - The workflow engine for Kubernetes,
     accesso eseguito il giorno maggio 9, 2025,
     [<u>https://argo-workflows.readthedocs.io/en/latest/security/</u>](https://argo-workflows.readthedocs.io/en/latest/security/)

107. Workflow RBAC - Argo Workflows - The workflow engine for
     Kubernetes - Read the Docs, accesso eseguito il giorno maggio 9,
     2025,
     [<u>https://argo-workflows.readthedocs.io/en/latest/workflow-rbac/</u>](https://argo-workflows.readthedocs.io/en/latest/workflow-rbac/)

108. Flyte Architecture Overview | Restackio, accesso eseguito il giorno
     maggio 9, 2025,
     [<u>https://www.restack.io/p/flyte-answer-architecture-cat-ai</u>](https://www.restack.io/p/flyte-answer-architecture-cat-ai)

109. Flyte Vs Argo Comparison | Restackio, accesso eseguito il giorno
     maggio 9, 2025,
     [<u>https://www.restack.io/p/flyte-answer-vs-argo-cat-ai</u>](https://www.restack.io/p/flyte-answer-vs-argo-cat-ai)

110. Orchestra vs. Flyte: key differences 2024, accesso eseguito il
     giorno maggio 9, 2025,
     [<u>https://www.getorchestra.io/guides/orchestra-vs-flyte-key-differences-2024</u>](https://www.getorchestra.io/guides/orchestra-vs-flyte-key-differences-2024)

111. Data Orchestration Tool Analysis: Airflow, Dagster, Flyte - DEV
     Community, accesso eseguito il giorno maggio 9, 2025,
     [<u>https://dev.to/datamonk\_/different-orchestration-tool-analysis-airflow-dagster-flyte-192d</u>](https://dev.to/datamonk_/different-orchestration-tool-analysis-airflow-dagster-flyte-192d)

112. Authenticating in Flyte - Flyte Docs, accesso eseguito il giorno
     maggio 9, 2025,
     [<u>https://docs.flyte.org/en/latest/deployment/configuration/auth\_setup.html</u>](https://docs.flyte.org/en/latest/deployment/configuration/auth_setup.html)

113. Understanding Authentication - Flyte Docs, accesso eseguito il
     giorno maggio 9, 2025,
     [<u>https://docs.flyte.org/en/latest/deployment/configuration/auth\_appendix.html</u>](https://docs.flyte.org/en/latest/deployment/configuration/auth_appendix.html)

114. Security Overview - Flyte Docs, accesso eseguito il giorno maggio
     9, 2025,
     [<u>https://docs.flyte.org/en/latest/deployment/security/index.html</u>](https://docs.flyte.org/en/latest/deployment/security/index.html)

115. Configuring user verification with SAML authentication and an LDAP
     domain user account | FortiClient 7.4.1 | Fortinet Document
     Library, accesso eseguito il giorno maggio 9, 2025,
     [<u>https://docs.fortinet.com/document/forticlient/7.4.1/ems-administration-guide/334169/configuring-user-verification-with-saml-authentication-and-an-ldap-domain-user-account</u>](https://docs.fortinet.com/document/forticlient/7.4.1/ems-administration-guide/334169/configuring-user-verification-with-saml-authentication-and-an-ldap-domain-user-account)

116. Multiple Kubernetes Cluster Deployment - Flyte Docs, accesso
     eseguito il giorno maggio 9, 2025,
     [<u>https://docs.flyte.org/en/latest/deployment/deployment/multicluster.html</u>](https://docs.flyte.org/en/latest/deployment/deployment/multicluster.html)

117. Enabling AWS resources | Union.ai Docs, accesso eseguito il giorno
     maggio 9, 2025,
     [<u>https://union.ai/docs/flyte//user-guide/integrations/enabling-aws-resources/</u>](https://union.ai/docs/flyte//user-guide/integrations/enabling-aws-resources/)

118. Permission | Feast: the Open Source Feature Store, accesso eseguito
     il giorno maggio 9, 2025,
     [<u>https://docs.feast.dev/getting-started/concepts/permission</u>](https://docs.feast.dev/getting-started/concepts/permission)

119. Kubernetes RBAC: A Step-by-Step Guide for Securing Your Cluster -
     Trilio, accesso eseguito il giorno maggio 9, 2025,
     [<u>https://trilio.io/kubernetes-best-practices/kubernetes-rbac/</u>](https://trilio.io/kubernetes-best-practices/kubernetes-rbac/)

120. Temporal Service | Temporal Platform Documentation, accesso
     eseguito il giorno maggio 9, 2025,
     [<u>https://docs.temporal.io/clusters</u>](https://docs.temporal.io/clusters)

121. Temporal Technologies Reviews - Read Customer Reviews of
     Temporal.io, accesso eseguito il giorno maggio 9, 2025,
     [<u>https://temporal-technologies.tenereteam.com/</u>](https://temporal-technologies.tenereteam.com/)

122. Nine ways to use Temporal in your AI Workflows, accesso eseguito il
     giorno maggio 9, 2025,
     [<u>https://temporal.io/blog/nine-ways-to-use-temporal-in-your-ai-workflows</u>](https://temporal.io/blog/nine-ways-to-use-temporal-in-your-ai-workflows)

123. Temporal vs. Argo Workflows - Pipekit, accesso eseguito il giorno
     maggio 9, 2025,
     [<u>https://pipekit.io/blog/temporal-vs-argo-workflows</u>](https://pipekit.io/blog/temporal-vs-argo-workflows)

124. ServiceNow Orchestration vs Temporal comparison - PeerSpot, accesso
     eseguito il giorno maggio 9, 2025,
     [<u>https://www.peerspot.com/products/comparisons/servicenow-orchestration\_vs\_temporal</u>](https://www.peerspot.com/products/comparisons/servicenow-orchestration_vs_temporal)

125. Temporal Platform security features - Temporal Docs, accesso
     eseguito il giorno maggio 9, 2025,
     [<u>https://docs.temporal.io/self-hosted-guide/security</u>](https://docs.temporal.io/self-hosted-guide/security)

126. Implementing Role-Based Authentication for Self-Hosted Temporal -
     Bitovi, accesso eseguito il giorno maggio 9, 2025,
     [<u>https://www.bitovi.com/blog/implementing-role-based-authentication-for-self-hosted-temporal</u>](https://www.bitovi.com/blog/implementing-role-based-authentication-for-self-hosted-temporal)

127. Role-Based Auth for Self-Hosted Temporal : r/selfhosted - Reddit,
     accesso eseguito il giorno maggio 9, 2025,
     [<u>https://www.reddit.com/r/selfhosted/comments/1k6ttvu/rolebased\_auth\_for\_selfhosted\_temporal/</u>](https://www.reddit.com/r/selfhosted/comments/1k6ttvu/rolebased_auth_for_selfhosted_temporal/)

128. Deep Dive into the Concepts of Luigi - Akash R Chandran's blog,
     accesso eseguito il giorno maggio 9, 2025,
     [<u>https://blog.akashrchandran.in/deep-dive-into-the-concepts-of-luigi</u>](https://blog.akashrchandran.in/deep-dive-into-the-concepts-of-luigi)

129. Airflow and Luigi: Detailed Workflow Management Review -
     RisingWave, accesso eseguito il giorno maggio 9, 2025,
     [<u>https://risingwave.com/blog/airflow-and-luigi-detailed-workflow-management-review/</u>](https://risingwave.com/blog/airflow-and-luigi-detailed-workflow-management-review/)

130. Dagster vs Luigi: Comparing Two Workflow Tools - CastorDoc, accesso
     eseguito il giorno maggio 9, 2025,
     [<u>https://www.castordoc.com/data-strategy/dagster-vs-luigi-comparing-two-workflow-tools</u>](https://www.castordoc.com/data-strategy/dagster-vs-luigi-comparing-two-workflow-tools)

131. luigi Features — b2luigi latest documentation, accesso eseguito il
     giorno maggio 9, 2025,
     [<u>https://software.belle2.org/b2luigi/features/luigi\_features.html</u>](https://software.belle2.org/b2luigi/features/luigi_features.html)

132. Using the Central Scheduler — Luigi 3.6.0 documentation, accesso
     eseguito il giorno maggio 9, 2025,
     [<u>https://luigi.readthedocs.io/en/stable/central\_scheduler.html</u>](https://luigi.readthedocs.io/en/stable/central_scheduler.html)

133. luigi/examples/kubernetes.py at master · spotify/luigi - GitHub,
     accesso eseguito il giorno maggio 9, 2025,
     [<u>https://github.com/spotify/luigi/blob/master/examples/kubernetes.py</u>](https://github.com/spotify/luigi/blob/master/examples/kubernetes.py)

134. Integration of Luigi with authentication provider that does not
     have ..., accesso eseguito il giorno maggio 9, 2025,
     [<u>https://github.com/SAP/luigi/discussions/2643</u>](https://github.com/SAP/luigi/discussions/2643)

135. Luigi Documentation, accesso eseguito il giorno maggio 9, 2025,
     [<u>https://luigi.readthedocs.io/\_/downloads/en/latest/pdf/</u>](https://luigi.readthedocs.io/_/downloads/en/latest/pdf/)

136. accesso eseguito il giorno gennaio 1, 1970,
     [<u>https://luigi.readthedocs.io/en/latest/luigi\_visualiser.html</u>](https://luigi.readthedocs.io/en/latest/luigi_visualiser.html)

137. Documentation - Luigi - The Enterprise-Ready Micro Frontend ...,
     accesso eseguito il giorno maggio 9, 2025,
     [<u>https://docs.luigi-project.io/docs/auth-oidc?section=overview</u>](https://docs.luigi-project.io/docs/auth-oidc?section=overview)

138. Luigi Core API - Documentation - Luigi - The Enterprise-Ready Micro
     Frontend Framework, accesso eseguito il giorno maggio 9, 2025,
     [<u>https://docs.luigi-project.io/docs/luigi-core-api</u>](https://docs.luigi-project.io/docs/luigi-core-api)

139. Extending Flyte | Union.ai Docs, accesso eseguito il giorno maggio
     9, 2025,
     [<u>https://www.union.ai/docs/flyte/architecture/extending-flyte/</u>](https://www.union.ai/docs/flyte/architecture/extending-flyte/)

140. Dagster vs. Airflow: a comprehensive comparison | Modal Blog,
     accesso eseguito il giorno maggio 9, 2025,
     [<u>https://modal.com/blog/dagster-vs-airflow-article</u>](https://modal.com/blog/dagster-vs-airflow-article)

141. FAQ: Airflow on EKS – RBAC, SAML, SSO, OAuth - Restack, accesso
     eseguito il giorno maggio 9, 2025,
     [<u>https://www.restack.io/docs/airflow-faq-aws-eks-rbac</u>](https://www.restack.io/docs/airflow-faq-aws-eks-rbac)
