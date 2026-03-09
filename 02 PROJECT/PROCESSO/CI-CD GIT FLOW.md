---
type: note
topic: data-platform
created: 2026-03-04
tags:
  - ci-cd
  - kestra
  - git
---
# DIAGRAMMI



![[Pasted image 20260206112552.png|347]]

![[04_09_56.jpg]]


## ATTORI

- Utente 
- GitLab
- Kestra DEV (ambiente dev/pre-prod)
- Kestra PROD (a)


### Utente

Utente sviluppatore dei progetti dbt

Ruolo:
- Responsabile dello sviluppo e test dei processi dbt
	- sviluppo in ambiente dev
- Effettua le Merge Request per la promozione dei processi
	- da ambiente dev ad ambiente test (pre-prod)
	- da ambiente test (pre-prod) ad ambiente prod

### GitLab

Repository del codice sorgente.

Le repository contenute su GitLab sono:
1. Repository del template cookie-cutter del progetto dbt (in ==/dbt/models/cookiecutter-dbt-template-kestra==) a partire dal quale vengono create le repository dei singoli progetti dbt
2. Repository dei progetti dbt (in ==/data-platform/dbt/==) creati a partire dal template. Ogni repository contiene:
		1. il progetto con il codice e la configurazione di dbt
		2. una directory /flows/ che contiene il flow base Kestra definito in un file \<progetto\>.yaml che viene inviato a Kestra per poter orchestrare la pipeline
		3. un file .gitlab-ci.yml che contiene la definizione della pipeline ci/cd nei vari stage (dev->test/pre-prod->prod)
		4. un comando di esecuzione del processo dbt (sh o python)
		La repository contiene i branch dedicati ad ogni ambiente (dev, test, pre-prod, prod)
3. Repository che contiene tutti flow Kestra per tutti i progetti dbt (in ==/data-platform/kestra/kestraflow==): utilizzato per copiare i flow Kestra da ambiente Kestra DEV ad ambiente Kestra PROD 

I ruoli svolti da GitLab sono:
- Gestione del versioning e del branching delle repository descritte
- Gestione della procedura di ci/cd per la promozione degli artefatti nei vari ambienti effettuata attraverso un meccanismo di Merge Request. Artefatti:
	- Progetto dbt (viene effettuata commit su relativo branch target)
	- Pipeline Kestra (invio della definizione della pipeline nel relativo namespace Kestra e gestione dei branch della repo kestraflow)



### Kestra

Orchestratore delle pipeline.  

Esistono due istanze Kestra separate:
- sviluppo (Kestra DEV)
- produzione (Kestra PROD)

Entrambi contengono:
- Pipeline di esecuzione dei progetti dbt 
- Pipeline di sincronizzazione dell'ambiente kestra di prod con quello di sviluppo
	- la sincronizzazione avviene utilizzando una repo git come serbatoio di interscambio
	- una pipeline si occupa di scrivere i vari flow dall'ambiente Kestra di sviluppo su git
	- un'altra pipeline copia i flow da git all'ambiente KEstra di produzione

Responsabilità:
- Esecuzione e schedulazione delle pipeline dbt e sincronizzazione kestra 


## FASI

### FASE 0 - SVILUPPO

**Utente esegue Script dbt-creator** che crea progetto dbt in ambiente dev con 
- **profili dbt**
	- dev (svil: branch base durante sviluppo)
	- pre-prod (test: branch utilizato in fase di test e pre-produzione)
	- main (prod: branch utilizzato in produzione)
- **Configurazione pipeline kestra** (in dir /flows/) 
	- contiene file yaml (definizione pipeline kestra): 
	- serve per inizializzare il flow su kestra (su namespace dev.kestra)
		- https://kestra-test.dataliguria.it/ui/main/namespaces/edit/dev.kestra
	- non viene poi più utilizzata
- **Creazione pipeline ci/cd gitlab** (in file .gitlab-ci.yaml) 
	- contiene questi stage
		- stage deploy_preprod
			- copia pipeline kestra da dev (dev.kestra) a pre-prod (test.kestra)
		- stage deploy_prod
			- copia pipeline kestra pre-prod (test.kestra) -> prod (prod.kestra)

NOTA: Nel progetto dbt di ogni progetto abbiamo
- profili
- pipeline kestra di base
- pipeline ci/cd

**Utente DEV sviluppa il progetto dbt che viene salvato sul branch dev della repo **

NOTA - ATTENZIONE: se si deve modificare flow kestra bisogna farlo su Kestra e non sul file yaml della repo del progetto (che serve solo per l'inizializzazione del floe)


### FASE 1 - DA DEV A TEST (PRE-PROD)

**Passaggio da dev a test/pre-prod**
- Utente effettua una **Merge Request** (adesso automatica potrebbe richiedere approvazione)
- Previa autorizzazione della MR **GitLab** esegue la pipeline ci/cd (.gitlab-ci.yaml) nello stage deploy_preprod che effettua copia del flow su Kestra dal namespace dev.kestra al namespace test.kestra. Le operazioni effettuate sono:
			1. curl (GET) della pipeline da Kestra DEV
			2. cambio namespace
			3. curl (POST) della pipeline su Kestra DEV


### FASE 2 - DA TEST A PROD


Per poter effettuare la promozione nell'ambiente prod è necessario sincronizzare le pipeline Kestra tra gli ambienti DEV e PROD. 
La sincronizzazione avviene mediante due pipeline Kestra (push_flows e syncFlows) che utilizzano una repo GitLab come serbatoio di interscambio
- push_flows: scrive le pipeline presenti sull'ambiente Kestra DEV nel namespace test.kestra (pipeline che hanno passato la fase 1) nella repo GitLab ==/data-platform/kestra/kestraflow==
- syncFlow: legge le pipeline dalla repo GitLab ==/data-platform/kestra/kestraflow== e le scrive sul Kestra PROD nel namespace prod.kestra

La pipeline push_flows è schedulata e asincrona rispetto alla procedura ci/cd che avviene a seguito della approvazione della Merge Request (pre-requisito)
Anche la pipeline syncFlows è schedulata e asincrona rispetto alla procedura ci/cd. La pipeline sarà disponibile nell'ambiente Kestra PROD solo dopo che viene eseguita syncFlows, 

**Passaggio a prod**
- Merge Request da parte di utente. Previa approvazione
	- **GitLab** esegue la pipeline ci/cd .gitlab-ci.yaml stage deploy_prod la quale esegue pipeline Kestra **merge-request** (mediante curl POST) che effettua copia del flow su git da branch pre-prod al branch prod




## NOTE / DUBBI / TODO

- Namespace kestra: dev.progetto.flow
- Uniformare nomi (test, pre-prod) e stile (camelCase o snake-case) 
- Rinominare merge-request (copia del flow su git da branch test/pre-prod al branch prod). es: merge-test-to-prod
- Fasi: dev/test/pre-prod/prod (necessario?)




