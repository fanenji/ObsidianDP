---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - data-platform
  - dbt
---

**Tool interattivo per creazione nuovi progetti dbt**


# SCRIPT 
[https://gitlab-test.dataliguria.it/data-platform/dbt/models/dbt-project-creator](https://gitlab-test.dataliguria.it/data-platform/dbt/models/dbt-project-creator)

# TEMPLATE PROGETTO DBT

[https://gitlab-test.dataliguria.it/data-platform/dbt/models/cookiecutter-dbt-template](https://gitlab-test.dataliguria.it/data-platform/dbt/models/cookiecutter-dbt-template)

[https://gitlab-test.dataliguria.it/data-platform/dbt/models/cookiecutter-dbt-template-test](https://gitlab-test.dataliguria.it/data-platform/dbt/models/cookiecutter-dbt-template-test)


# TODO

**SCRIPT DBT-CREATOR**

- modifica default
- slug “-” → “_”

# **REPO TEMPLATE**

NOTA: vedi progetto test_local_4

**MODIFICHE**

- cartelle modelli direttamente sotto models
- modifica profiles.yaml
- levare “space_”
- .dbtignore/.gitignore → file “.ipynb_checkpoints”
- modifica source.yml
- modifica create_pdf con riferimento a source
- packages.yml (dbt_utils)

# **SCRIPT**

**MODIFICHE**

- Aggiunta istruzioni inizializzazione progetto

# NOTE

```other
#### INSTALLAZIONE ----------------------------

# FROM GITLAB 
GIT_SSL_NO_VERIFY=true pip install git+https://10.11.9.20/data-platform/dbt/models/dbt-project-creator.git

# FROM LOCAL SOURCE
git clone https://10.11.9.20/data-platform/dbt/models/dbt-project-creator.git

cd dbt-project-creator
python3 -m venv .venv
source .venv/bin/activate

GIT_SSL_NO_VERIFY=true pip install -r requirements.txt
dbt deps

# CREATO SCRIPT /Users/stefano/Development/DP/dbt-projects/_install_dbt_project_creator.sh

#### ESECUZIONE ------------------------------
source dbt-project-creator/.venv/bin/activate
dbt-creator

# CREATO SCRIPT /Users/stefano/Development/DP/dbt-projects/create.sh
```
