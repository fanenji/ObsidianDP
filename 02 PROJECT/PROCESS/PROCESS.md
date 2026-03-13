---
type: moc
topic: data-platform
created: 2026-01-15
tags:
  - data-platform
  - dbt
---

# WORKFLOW DBT 1 ( SQL)

L’intero processo viene effettuato tramite dbt/dremio

- Ingestion
- Tranformation

Vincoli

- Fonti dati configurate su Dremio (relazionali, file su s3)
- Intera trasformazione effettuata tramite query sql in dbt

NOTA:

# WORKFLOW DBT 2 (SQL + PYTHON)

Se è necessario eseguire delle trasformazioni sia con sql che con python si può:

- utilizzare modelli sql per le trasformazioni con target dremio
- utilizzare modelli python per le trasformazioni con target duckdb

IPOTESI PER ORCHESTRAZIONE FASI

- file yaml di configurazione che definisce le dipendenze tra modelli e il flusso di elaborazione
- script python che legge yaml ed esegue la pipeline

[DBT CREATOR](./DBT CREATOR.md)

[SCRIPT ESECUZIONE DBT](./SCRIPT ESECUZIONE DBT.md)

# NOTE

CONVERSAZIONE CON ChatGPT: [https://chatgpt.com/share/68d53d7a-0df4-8000-8040-d7d2924dee09](https://chatgpt.com/share/68d53d7a-0df4-8000-8040-d7d2924dee09)

## VSCODE

- installato estensione Datamates
- creato account su altimate
    - [s.parodi@liguriadigitale.it](mailto:s.parodi@liguriadigitale.it) / 7s6D1I29KM2ilz
    - [https://dpliguriadigitale.app.myaltimate.com](https://dpliguriadigitale.app.myaltimate.com/)
    - INSTANCE NAME: dpliguriadigitale
    - API KEY: 4ee1b27e536ca5bbf754c518b2fdecb9
- installato estensione “Power User for dbt”
- PROBLEMA: non vede profiles.yaml → spostato profiles.yaml su home dir del progetto

%% MOC START %%
- [[AMBIENTI]]
- [[DBT CREATOR]]
- [[DEFINIZIONE METADATI]]
- [[SCRIPT ESECUZIONE DBT]]
%% MOC END %%
