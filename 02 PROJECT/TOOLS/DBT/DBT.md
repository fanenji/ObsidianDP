---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - dbt
  - tools

---
# LINKS

- [https://docs.getdbt.com/best-practices](https://docs.getdbt.com/best-practices)


# NOTES


**MONITORING & OBSERVABILITY**
- Log e Artifact su OpenSearch → Alerting
- DataKichen
- Elementary (observability)

**CONTRACTS**
- Utilizzo contracts per sorgenti e modelli critici

**EXPOSURES**

Vedi [[DBT Tests That Catch Real Bugs and How to Wire CI]]

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
