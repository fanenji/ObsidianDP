---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - dbt
  - ci-cd
---

# NOTE

dbt-osmosis richiede esecuzione dbt build non si può quindi bloccare la build in fase di sviluppo.

In fase di CI/CD si può usare la pre-commit per bloccare la merge ed impedire il deploy della pipeline negli ambienti staging/prod

Vedi “Run in CI/CD”:

- [https://github.com/dbt-checkpoint/dbt-checkpoint/tree/main?tab=readme-ov-filerun-in-cicd](https://github.com/dbt-checkpoint/dbt-checkpoint/tree/main?tab=readme-ov-filerun-in-cicd)

# SCRIPT PROGETTO SQL

```yaml
dbt build
dbt docs generate
dbt-osmosis yaml refactor
pre-commit run --all-files
```

# SCRIPT PROGETTO MISTO SQL/PYTHON

IPOTESI

- file yaml di configurazione che definisce le dipendenze tra modelli e il flusso di elaborazione
- script python che legge yaml ed esegue la pipeline
