---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - dbt
  - tools

---
# LINK


[How to get started with dbt](https://www.blef.fr/get-started-dbt/)

[Quickstart for dbt Core using GitHub Codespaces | dbt Developer Hub](https://docs.getdbt.com/guides/codespace?step=1)

[Modern Data Modeling: Start with the End?](https://www.adventofdata.com/modern-data-modeling-start-with-the-end)

[Zero to dbt](https://www.youtube.com/watch?v=a3fRALauYWs&list=PL0QYlrC86xQlj9UDGiEwhXQuSjuSyPJHl&index=48)

[dbt for Data Transformation - Hands-on Tutorial - KDnuggets](https://www.kdnuggets.com/2021/07/dbt-data-transformation-tutorial.html)

[How to Build a Mature dbt Project from Scratch | dbt Developer Blog](https://docs.getdbt.com/blog/how-to-build-a-mature-dbt-project-from-scratch)

[How to manage and schedule dbt](https://www.blef.fr/manage-and-schedule-dbt/)

[Testing Dbt Macros](https://leo-godin.medium.com/testing-dbt-macros-a80e76243ae4)

[INTEGRAZIONI](1%20-%20LAVORO/1%20-%20PROGETTI/DATA%20PLATFORM%20(DP)/MATERIALI/DBT/INTEGRAZIONI.md)



# MONITORING & OBSERVABILITY

- Log e Artifact su OpenSearch → Alerting
- Docs
    - [https://medium.com/@oravidov/dbt-observability-101-how-to-monitor-dbt-run-and-test-results-f7e5f270d6b6](https://medium.com/@oravidov/dbt-observability-101-how-to-monitor-dbt-run-and-test-results-f7e5f270d6b6)
    - [https://discourse.getdbt.com/t/how-to-add-observability-to-your-dbt-deployment/3451](https://discourse.getdbt.com/t/how-to-add-observability-to-your-dbt-deployment/3451)
    - [https://www.getdbt.com/coalesce-2021/observability-within-dbt](https://www.getdbt.com/coalesce-2021/observability-within-dbt)
- DataKichen
- Elementary (observability)
- Gestione log: [https://medium.com/@oravidov/dbt-observability-101-how-to-monitor-dbt-run-and-test-results-f7e5f270d6b6](https://medium.com/@oravidov/dbt-observability-101-how-to-monitor-dbt-run-and-test-results-f7e5f270d6b6)

# DATA_TESTS

- unit test
    - [https://github.com/mjirv/dbt-datamocktool](https://github.com/mjirv/dbt-datamocktool)
    - [https://github.com/josephmachado/unit_test_dbt](https://github.com/josephmachado/unit_test_dbt)
    - [https://github.com/EqualExperts/dbt-unit-testing](https://github.com/EqualExperts/dbt-unit-testing)
    - [https://github.com/dm03514/dbt-model-tests](https://github.com/dm03514/dbt-model-tests)
- quality test  
    - [https://github.com/calogica/dbt-expectations](https://github.com/calogica/dbt-expectations)
- custom test (suite di test in package condiviso)
- source freshness test

# VARIE

- Utilizzo contracts per sorgenti e modelli critici
- Tool per controlli in fase di sviluppo e CI: [https://github.com/dbt-checkpoint/dbt-checkpoint?tab=readme-ov-file](https://github.com/dbt-checkpoint/dbt-checkpoint?tab=readme-ov-file)
- vs code: [https://github.com/AltimateAI/vscode-dbt-power-user](https://github.com/AltimateAI/vscode-dbt-power-user)

# BEST PRACTICES

- [https://docs.getdbt.com/best-practices](https://docs.getdbt.com/best-practices)
- [https://medium.com/@turkelturk/best-practices-for-workflows-a-guide-to-effective-dbt-use-fa925127647c](https://medium.com/@turkelturk/best-practices-for-workflows-a-guide-to-effective-dbt-use-fa925127647c)
- [https://medium.com/dkatalis/6-lesser-known-best-practices-in-dbt-data-build-tool-f94687abf89d](https://medium.com/dkatalis/6-lesser-known-best-practices-in-dbt-data-build-tool-f94687abf89d)
- [https://www.getdbt.com/coalesce-2021/how-to-build-a-mature-dbt-project-from-scratch](https://www.getdbt.com/coalesce-2021/how-to-build-a-mature-dbt-project-from-scratch)
- [https://www.adventofdata.com/modern-data-modeling-start-with-the-end/](https://www.adventofdata.com/modern-data-modeling-start-with-the-end/)
- test
    - [https://www.datafold.com/blog/7-dbt-testing-best-practices](https://www.datafold.com/blog/7-dbt-testing-best-practices)
    - [https://servian.dev/unit-testing-in-dbt-part-1-d0cc20fd189a](https://servian.dev/unit-testing-in-dbt-part-1-d0cc20fd189a)


# EXPOSURES

[https://blog.stackademic.com/dbt-tests-that-catch-real-bugs-and-how-to-wire-ci-9e96508b8c73](https://blog.stackademic.com/dbt-tests-that-catch-real-bugs-and-how-to-wire-ci-9e96508b8c73)

> Exposures (tie models to dashboards/apps; great for impact analysis)

```other
exposures:
  - name: rev_dashboard
    type: dashboard
    url: https://bi.yourco.com/revenue
    depends_on:
      - ref('gold_revenue_daily')
    owner:
      name: Finance
      email: finance-data@yourco.com
```

# INTEGRAZIONI


## DuckDB

[MotherDuck + dbt: Better Together](https://motherduck.com/blog/motherduck-duckdb-dbt/)

[DuckDBT: Not a database or a dbt adapter but a secret third thing – DuckCon 3 (San Francisco)](https://www.youtube.com/watch?v=NQmOiEJ8fEs)

[dbt-duckdb](https://pypi.org/project/dbt-duckdb/1.3.3/)

[Unleashing DuckDB & dbt for local analytics triumphs](https://www.youtube.com/watch?v=asxGh2TrNyI)

[https://github.com/mehd-io/dbt-duckdb-tutorial](https://github.com/mehd-io/dbt-duckdb-tutorial)

[Use dbt and Duckdb instead of Spark in data pipelines](https://medium.com/datamindedbe/use-dbt-and-duckdb-instead-of-spark-in-data-pipelines-9063a31ea2b5)

[dbt + DuckDB vs Spark: What's the best way to build data pipelines in 2023?](https://www.youtube.com/watch?v=ByhkMe70ZI4)

## Postgis

[https://www.youtube.com/watch?v=QBJY0jdnou0](https://www.youtube.com/watch?v=QBJY0jdnou0)

## Dremio

- [https://docs.dremio.com/current/sonar/client-applications/clients/dbt/](https://docs.dremio.com/current/sonar/client-applications/clients/dbt/)
- [https://docs.getdbt.com/docs/core/connect-data-platform/dremio-setup](https://docs.getdbt.com/docs/core/connect-data-platform/dremio-setup)

[How to Use dbt on Dremio - A Step-by-Step Guide](https://www.youtube.com/watch?v=Eocv6CBLBqk)

[Create an Open Data Lakehouse with Dremio & dbt Labs - Step-by-Step Tutorial](https://www.youtube.com/watch?v=WL0by3s1Lo0)

[Intro to dbt with Dremio - 1 - Dremio & Python Environment Setup](https://www.youtube.com/watch?v=TGemN4TfM7g)

%% MOC START %%
_empty folder_
%% MOC END %%
