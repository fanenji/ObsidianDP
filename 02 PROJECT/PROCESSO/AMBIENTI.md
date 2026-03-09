---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - ci-cd
---



# ORGANIZZAZIONE K8S


Unico cluster kubernetes con 3 ambienti separati mediante **namespace**

- sviluppo
- produzione
- test (per aggiornamenti software)

Un unico repository GitLab controlla l’intera infrastruttura


# FASI

- SVILUPPO 
- TEST
- PRE-PRODUZIONE (STAGING)
- PRODUZIONE

Le prime due fasi avvengono sull'ambiente di sviluppo, le altre due sull'ambiente di produzione


# COMPONENTI


## DREMIO/NESSIE/MINIO

Ambiente di sviluppo

- Una istanza Dremio che punta ad un catalogo Nessie basato su un bucket Minio

Ambiente di produzione

- Due istanze Dremio che puntano a due cataloghi Nessie basati su due bucket Minio diversi
    - PROD
    - STAGING

La presenza di due istanze Dremio permette l’isolamento dell’ambiente di produzione da quello di staging per garantire che le risorse dedicate all’ambiente di produzione non siano compromesse dall’esecuzione delle pipeline in staging

Sia la parte dati (PDS Dremio su Nessie) che la parte del layer semantico (VDS Dremio) sono suddivise in ambienti (bucket S3, cataloghi Nessie e spazi Dremio) tra loto isolati

- **DEV:** Ambiente di sviluppo delle pipeline 
- **SANDBOX**: Ambiente per esperimenti e prove effimere
- **STAGING:** Ambiente di pre-produzione in cui si testa la pipeline prima della messa in produzione
- **PROD:** Ambiente di produzione

Gli ambienti DEV e SANDBOX sono su k8s di sviluppo mentre gli ambienti STAGING e PROD su k8s di produzione su due diverse istanze di Dremio (con relativi cataloghi Nessie e bucket Minio)

In questa configurazione sono garantiti al meglio i seguenti requisiti
- L’ambiente di produzione è isolato dall’ambiente di sviluppo
- L’ambiente di staging è il più simile possibile all’ambiente di produzione
- L’ambiente di staging è isolato dall’ambiente di produzione (utilizzo di due istanze di Dremio con risorse dedicate)

### DREMIO


Differenziare ambienti mediante appositi spazi su Dremio, es:

- dev
- sandbox
- staging
- prod

Questi spazi contengono le cartelle dei singoli progetti con i relativi layer semantici

Es:

```yaml
- dev
    - Progetto_1
        - Application
            - query1
            - …
        - Business
            - queryN
            - …
        - Staging
		        - queryM
		        - …
    - Progetto_2
        - …
- staging
    - Progetto_1
        - …
- prod
    - Progetto_1
        - …
```

Presumibilmente lo spazio “dev” sarà presente solo sull’istanza Dremio del ambiente di sviluppo mentre gli spazi “stg” e “prd” saranno sull’istanza Dremio del ambiente di produzione.

Lo spazio “prd” potrebbe essere presente nel ambiente di sviluppo per effettuare eventuali confronti tra i dati prodotti da una pipeline in produzione e la stessa pipeline modificata nell’ambiente di sviluppo.

Le cartelle di progetto negli spazi “dev” e “stg” possono essere effimeri (cancellati quando non servono), l’eventuale esecuzione delle pipeline dbt ricrea comunque lo spazio relativo.

### NESSIE


Due ipotesi

1. Isolare gli ambienti mediante cartelle separate
2. Utilizzare Branch e Merge con Nessie

#### CARTELLE SEPARATE

Le tavole (PDS) dei singoli progetti sono contenute in cartelle alla radice della source nessie

All’interno di ogni cartella sono presenti le cartelle dei singoli progetti con all’interno le PDS del progetto

Anche per quanto riguarda i dati fisici gli spazi di progetto negli ambienti “dev” e “stg” possono essere effimeri (cancellati quando non servono), l’eventuale esecuzione delle pipeline dbt ricrea comunque lo spazio relativo.

NOTA DBT

Nel profiles.yml indicare nei diversi object_storage_path il path con riferimento all’ambiente:

- object_storage_path: dev.test_local_4
- object_storage_path: stg.test_local_4
- object_storage_path: prd.test_local_4

#### BRANCH

- Un branch di produzione “main”
- Un branch per ogni progetto “project-xxx”
- I branch di progetto sono creati e gestiti dal progetto dbt attraverso l’uso di macro, sono effimeri e possono essere cancellati dopo la fase di sviluppo

**WORKFLOW CI/CD**
- Sviluppo avviene su branch “project-xxx” in ambiente dev
- APERTURA PULL REQUEST →
    - creazione branch “project-xxx” in ambiente prod
    - esecuzione dbt
- APPROVAZIONE MANUALE PR →
    - merge del branch “project-xxx” su main
    - cancellazione branch “project-xxx”


==L’opzione branch su Nessie potrebbe essere problematica:==
- ==l’utilizzo mediante dbt richiede implementazione di macro custom==
- ==il merge su prod non regolato in maniera estremamente stringente può portare a problemi di consistenza nei dati (esecuzione per errore sul branch main invece che sul branch di progetto)==



# CODICE DBT

- Repo Git per ogni progetto dbt
- Branch
    - main (prod)
    - staging (potrebbe non essere necessario)
    - feature-xxx

# KESTRA

Due istanze Kestra
- Kestra DEV
- Kestra PROD



# GitLab

UNICA ISTANZA PER TUTTE LE PIATTAFORME



# REFERENCES

[[CI-CD]]

