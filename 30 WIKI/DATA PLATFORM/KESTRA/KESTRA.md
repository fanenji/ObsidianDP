---
type: note
topic: dp
created: 2026-03-03
tags:
  - kestra
  - ci-cd
  - dbt
---
# GitFlow


![[Pasted image 20260206112552.png]]


![[Pasted image 20260304125846.png]]



## COMPONENTI

- Utente DEV (lavora in ambiente di sviluppo dbt)
- GitLab
- Kestra DEV (dev/pre-prod)
- Kestra PROD

### GitLab

Contiene:
- repo dei progetti dbt
- repo kestra per copia flows da dev a prod (/data-platform/kestra/kestraflow)
- procedure ci/cd


## FASE 0 - SVILUPPO

**Utente DEV esegue Script dbt-creator** 

**Script dbt-creator** crea progetto dbt in ambiente dev con 
- **profiles dbt**
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

Progetto dbt su branch dev (sviluppo) su cui avviene lo sviluppo dbt [RISCRIVERE]

NOTA: se si vuole modificare flow kestra bisogna farlo su Kestra


## FASE 1 - DA DEV A TEST (PRE-PROD)

**Passaggio da dev a pre-prod/test**
- **Merge Request** da parte di utente (adesso automatica potrebbe richiedere approvazione)
- **Git**: viene eseguita pipeline ci/cd .gitlab-ci.yaml stage deploy_preprod che effettua copia del flow su Kestra dal namespace dev.kestra al namespace test.kestra:
			1. curl get pipeline
			2. cambio namespace
			3. curl post pipeline


## FASE 2 - DA TEST A PROD

NOTA: push_flows e syncFlows lavorano su repo git **KestraFlow**

**Prerequisito**
- **push_flows**: pipeline Kestra (schedulata e/o a comando) che effettua push pipeline kestra del namespace test.kestra su git (repo KestraFlow branch test)
	- Serve per sincronizzare gli ambienti Kestra (sviluppo e produzione)
	- Funzionale per la fase 3 (da pre-prod a prod) che richiede la copia dei flow kestra nell'ambiente di produzione (vedi SyncFlow)
	- Per sincronizzazione flow Kestra tra ambienti dev e prod viene utilizzato il repository Git **KestraFlow**

**Passaggio a prod**
- Merge Request da parte di utente. Previa approvazione
	- **Git**: viene eseguita pipeline ci/cd .gitlab-ci.yaml stage deploy_prod
		- esegue pipeline Kestra **merge-request**
			- effettua copia del flow su git da branch pre-prod al branch prod
	- **syncFlows**: Pipeline kestra che effettua pull da git a kestra di produzione namespace prod.kestra



## TODO

- Uniformare nomi (test, pre-prod)
- Usare sempre una convenzione (camel-case o snake-case) 
- Rinominare merge-request? (copia del flow su git da branch pre-prod al branch prod)
- Namespace kestra (es: dev.kestra) 
	- ridondante 
	- è necessario? 
	- perchè non usare namespace del progetto? (utile per eventuali progetti con + pipeline) 
- Verificare git switch su git.progetto.dev
- PROMOZIONE A PROD DEI FLOW KESTRA: push_flows e syncFlows sono schedulati e usano repo git KestraFlow: perchè? perchè non usare ci/cd con api kestra?



