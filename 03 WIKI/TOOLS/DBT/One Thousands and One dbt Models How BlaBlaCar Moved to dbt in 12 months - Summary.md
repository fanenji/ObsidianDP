---
title: "One Thousand and One dbt Models: How BlaBlaCar Moved to dbt in 12 Months — Summary"
type: note
topic: data-platform
created: 2026-04-04
tags:
  - dbt
  - data-engineering
  - bigquery
  - airflow
  - migration
  - tools
source: "[[One Thousands and One dbt Models How BlaBlaCar Moved to dbt in 12 months]]"
speakers:
  - Thibault Ambard (BlaBlaCar)
  - Tushar Bhasin (BlaBlaCar)
event: Forward Data Conference
video: https://www.youtube.com/watch?v=JGkVDRrCHcs
---

# One Thousand and One dbt Models: How BlaBlaCar Moved to dbt in 12 Months

**Speakers:** Thibault Ambard & Tushar Bhasin, BlaBlaCar
**Event:** Forward Data Conference
**Video:** https://www.youtube.com/watch?v=JGkVDRrCHcs

---

## 1. Company and Team Context

**BlaBlaCar** is a European ride-sharing platform. At the time of this talk:

| Metric | Value |
|---|---|
| Data team size | ~50 people (ICs + managers) |
| Tables in production | 4,000–6,000 |
| Cloud platform | GCP / BigQuery |
| Orchestrator | Apache Airflow |
| Migration duration | 12 months |
| Models migrated | ~1,200 dbt models |

The data team is organised around a **data mesh** structure: domain teams each own their data products, with a central data platform team providing tooling and standards.

---

## 2. Why dbt? The Decision to Adopt

BlaBlaCar's pre-dbt state: SQL transformation pipelines managed directly in Airflow, with dependencies expressed as DAG structures in Python code. The problems:

### 2.1 Pain Points

| Problem | Description |
|---|---|
| **Manual dependency management** | Every upstream/downstream relationship had to be explicitly coded in Airflow; no automatic DAG derivation from SQL |
| **No lineage visibility** | Hard to answer "what breaks if I change this table?" |
| **No testing framework** | Data quality checks were ad hoc or non-existent |
| **No documentation standard** | Each team documented (or didn't) in their own way |
| **Difficult onboarding** | New engineers had to understand both the business logic and the Airflow topology simultaneously |

### 2.2 Why dbt Specifically

dbt addressed all of the above with an **opinionated framework**:
- SQL-first: analysts write SQL they already know
- Automatic DAG from `ref()` dependencies
- Built-in testing (`not_null`, `unique`, `accepted_values`, `relationships`)
- `schema.yml` documentation as code
- Materialisation strategies (`table`, `view`, `incremental`, `ephemeral`)
- `manifest.json` — a machine-readable representation of the entire DAG

The key insight: dbt is **opinionated enough** that it enforces consistency across 50 engineers without requiring constant governance policing.

---

## 3. Enablers: Making dbt Work with Airflow

Before migrating any models, the team built three critical integrations between dbt and Airflow:

### 3.1 DAG Generator

The most important enabler. Problem: Airflow needs a Python DAG file for every pipeline; writing those by hand for 1,200 models is impractical.

**Solution:** Generate Airflow DAGs automatically from `manifest.json`.

```
dbt compile → manifest.json → DAG generator → Airflow DAG Python files
```

- `manifest.json` contains the full DAG structure: every node, its dependencies, tests, and metadata
- The generator reads this and produces Airflow DAG files that mirror the dbt dependency graph
- Engineers never write Airflow DAG files for dbt models — they only write SQL and `schema.yml`

This eliminated the biggest operational overhead and made the migration scalable.

### 3.2 Python Virtual Environment Operator

dbt runs as a Python process. In Airflow, running arbitrary Python in the worker environment creates dependency conflicts between dbt's requirements and other libraries.

**Solution:** Use Airflow's `PythonVirtualenvOperator` to run each dbt invocation in an isolated virtual environment.

- Each dbt project gets its own pinned Python environment
- No cross-contamination between projects with different dbt versions or adapter versions
- Enables running multiple dbt projects in parallel without conflicts

### 3.3 Sensors for Source Dependencies

dbt sources represent external tables produced by upstream non-dbt pipelines (ingestion jobs, raw data loaders). These create cross-DAG dependencies that Airflow must respect.

**Solution:** Use Airflow sensors on `dbt source freshness` checks.

- The generated DAG inserts a sensor task before any model that depends on an external source
- The sensor waits until the source table has been updated within the configured freshness threshold
- No cross-DAG trigger coupling needed — the freshness check is the contract

---

## 4. The Migration: 120-Model "Spaghetti" Pipeline

The first major migration was a single high-risk pipeline:
- **120 interdependent models**
- Named "the spaghetti" internally — no clear layering, deep chains of dependencies
- **6 engineers** working in parallel
- **10 weeks** to complete

### 4.1 Process

1. **Discovery:** map existing SQL logic and dependencies manually (the existing Airflow DAG was the source of truth, but understanding what each model did required reading SQL)
2. **Layering:** restructure into dbt best practices — staging → intermediate → marts
3. **Parallel development:** 6 engineers each took a subset of models; used `dev_` dataset namespacing to isolate work
4. **Double-run validation:** at each step, run both the old pipeline and the new dbt model, then compare output row counts and key metrics (see §6.2)
5. **Cutover:** swap the Airflow DAG to point to dbt output; decommission old SQL

### 4.2 Outcome

The 10-week timeline felt long but was justified by the complexity and the zero-tolerance requirement for data quality regressions. Subsequent migrations of smaller pipelines were significantly faster.

---

## 5. Scaling: Onboarding 50 Engineers

After the initial migration proved the approach, the goal was to onboard the entire 50-person IC team to dbt.

### 5.1 DBT Dragons

To scale knowledge without creating a bottleneck on the 2 core authors:
- Identified **dbt champions** in each domain team — engineers who showed high engagement during early training
- Formed the **"DBT Dragons"** expert group: ~8-10 people who became the go-to contacts for dbt questions in their domain
- DBT Dragons attended deeper technical sessions; regular ICs attended onboarding workshops
- Reduced centralised support burden; faster feedback cycles within domain teams

### 5.2 Onboarding Tooling

Tools built specifically to lower the barrier for the 50 ICs:

| Tool | Purpose |
|---|---|
| **CLI setup scripts** | One-command environment setup: Python version, virtualenv, dbt adapter, profile config |
| **Query generator** | Interactive CLI to scaffold new dbt models with correct naming, materialisation, and `schema.yml` stubs |
| **Data quality module** | Automates the double-run validation (see §6.2) — runs old and new models in parallel, compares outputs |

---

## 6. Key Practices and Lessons Learned

### 6.1 Dev Datasets

A critical practice for safe parallel development:

- Each engineer works in a **personal dev dataset** in BigQuery (e.g. `dev_thibault.my_model`)
- The `target` in `profiles.yml` is set to the developer's personal dataset by default
- Production runs target the shared production dataset
- No risk of breaking production tables during development; no interference between engineers

dbt's `target` and `project` configuration makes this straightforward — but it requires explicit setup in the CLI setup script so every engineer has it correctly configured from day one.

### 6.2 Double-Run Data Quality Validation

When migrating a model from legacy SQL to dbt:
1. Run the **old query** against production and materialise results to a temporary table
2. Run the **new dbt model** against the same inputs and materialise results
3. Compare: row counts, key column distributions, spot-check sample rows
4. Only proceed with cutover when outputs are identical (or documented differences are intentional)

This was formalised into the **data quality module** — an internal tool that automates steps 1–3 and produces a diff report.

### 6.3 dbt-dry-run

Before running any dbt model in CI/CD, validate it with `dbt-dry-run`:
- Sends the compiled SQL to BigQuery's dry-run API
- Returns estimated bytes processed and validates syntax without executing
- Catches compilation errors, missing references, and expensive queries before they run
- Zero cost — BigQuery dry-run is free

This became a mandatory CI gate: no model merges to production without a passing dry-run.

### 6.4 Git Training

An unexpected onboarding bottleneck: many data analysts on the team had limited git experience.

- SQL was previously edited directly in web UIs or shared notebooks
- dbt requires git-based workflows: branches, pull requests, code review
- Had to run **git fundamentals training** alongside dbt training
- Lesson: don't assume git proficiency in a mixed analyst/engineer team

### 6.5 Node Selectors in Airflow

Once multiple dbt projects existed, running `dbt run` for an entire project on every schedule became wasteful.

**Solution:** use dbt's node selector syntax in the generated Airflow tasks:

```bash
dbt run --select +my_model   # run model and all its ancestors
dbt run --select my_model+   # run model and all its descendants
dbt run --select tag:daily   # run only models tagged "daily"
```

The DAG generator was extended to produce tasks that use selectors, enabling:
- Per-model scheduling within a project
- Partial project runs triggered by upstream sensors
- Efficient CI runs that only test affected models

### 6.6 dbt Project Consolidation

A consequence of the data mesh structure: each domain team created their own dbt project. Over 12 months, this proliferated to **50+ dbt projects**.

Problems with too many projects:
- Cross-project `ref()` is not supported natively — requires `source()` for cross-project references, losing lineage
- Version drift: different projects on different dbt versions
- CI overhead: 50 separate CI pipelines to maintain

Lesson: set **project creation governance early**. Define criteria for when a new project is warranted vs. when a new folder within an existing project suffices.

---

## 7. Architecture Summary

```
Source Systems (raw data)
        ↓
Ingestion Pipelines (non-dbt)
        ↓ [Airflow sensors on freshness]
dbt Sources (external table references)
        ↓
dbt Staging Models (1:1 with sources, light cleaning)
        ↓
dbt Intermediate Models (business logic)
        ↓
dbt Mart Models (final, business-facing tables)
        ↓
[manifest.json → DAG Generator → Airflow DAGs]
        ↓
Production BigQuery datasets
```

---

## 8. Metrics: 12-Month Outcomes

| Metric | Before | After |
|---|---|---|
| Dependency management | Manual in Airflow Python code | Automatic from `ref()` |
| Documentation | Ad hoc | `schema.yml` standard across all models |
| Testing | None or custom | Built-in + custom dbt tests |
| Lineage visibility | None | Full column-level lineage via dbt docs |
| New model onboarding time | Days (understand Airflow + SQL) | Hours (write SQL + YAML) |
| Dev isolation | None | Personal dev datasets |
| CI validation | None | dbt-dry-run on every PR |

---

## 9. Key Takeaways

| Topic | Summary |
|---|---|
| **DAG generator** | Automatically generate Airflow DAGs from `manifest.json` — the single most important enabler |
| **PythonVirtualenvOperator** | Isolate dbt execution environments to avoid dependency conflicts |
| **Sensors for freshness** | Decouple dbt pipelines from upstream ingestion via source freshness checks |
| **Dev datasets** | Every engineer needs a personal BigQuery dataset from day one |
| **Double-run validation** | Run old and new models in parallel during migration; compare outputs before cutover |
| **dbt-dry-run** | Mandatory CI gate — validates syntax and cost without executing |
| **DBT Dragons** | Domain champions reduce central team bottleneck at scale |
| **Git training** | Don't assume; many analysts need foundational git skills |
| **Project governance** | Limit project proliferation early — 50+ projects creates cross-project lineage and CI problems |
| **Node selectors** | Use selectors in Airflow tasks to enable per-model scheduling and partial runs |
