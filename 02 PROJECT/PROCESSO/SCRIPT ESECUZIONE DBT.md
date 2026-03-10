---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - dbt
  - ci-cd
---
# PACKAGE PYTHON


Comando: **dbt-run**

Script python 
- Utilizzare pacchetto [questionary](https://pypi.org/project/questionary/) per TUI
- Prevedere workflow ridotti (non completi)


FLUSSO DBT
 - dbt build
 - dbt-osmosis yaml refactor
 - dbt docs generate
 - (eventuale) dbt docs serve o sistemi analoghi
 - pre-commit (controlli non bloccanti)
 
 
 GESTIONE COMMIT/PUSH GIT
 
![[Pasted image 20260309115452.png]]



# NOTA: dbt-checkpoint in CI/CD


dbt-osmosis richiede esecuzione dbt build non si può quindi bloccare la build in fase di sviluppo.
Il controllo della documentazione viene fatta nella fase CI/CD, se dbt-checkpoint fallisce: NO MERGE REQUEST

**dbt-checkpoint**: In fase di CI/CD si può usare la pre-commit per bloccare la merge ed impedire il deploy della pipeline negli ambienti staging/prod, vedi https://github.com/dbt-checkpoint/dbt-checkpoint/tree/main?tab=readme-ov-file#run-in-cicd




# PROGETTO MISTO SQL/PYTHON

**IPOTESI**
- file yaml di configurazione che definisce le dipendenze tra modelli e il flusso di elaborazione
- script python che legge yaml ed esegue la pipeline
