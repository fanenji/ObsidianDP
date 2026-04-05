---
title: 5 dbt Slim CI Tactics for Large Repos
source: https://medium.com/@kaushalsinh73/5-dbt-slim-ci-tactics-for-large-repos-33c6a1789a22
author:
  - "[[Neurobyte]]"
published: 2025-09-30
created: 2026-04-04
description: 5 dbt Slim CI Tactics for Large Repos Practical ways to keep PR builds fast, safe, and focused as your project — and team — grows. Five production-ready dbt Slim CI tactics to speed PR builds on …
tags:
  - clippings
  - dbt
  - ci-cd
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)

## Practical ways to keep PR builds fast, safe, and focused as your project — and team — grows.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*20slxxrpTP0f26jjlmmvyw.png)

Five production-ready dbt Slim CI tactics to speed PR builds on big repos: state-aware selectors, smart deferral, focused tests, partial parse, and artifact hygiene.

Big dbt repos are like big cities: powerful, but slow if you don’t plan the streets. Full builds on every pull request don’t scale — developers wait, reviewers guess, and flaky tests multiply. Slim CI is the antidote: run *only* what changed (and what depends on it) with high confidence. Below are five tactics that make Slim CI truly slim without cutting corners.

## 1) State-Aware Selection (and nothing else)

Slim CI starts with **selectors that trust the state**. Use `state:modified+` to capture the blast radius: changed models, their parents (data inputs), and children (consumers).

```c
# selectors.yml
selectors:
  - name: pr_scope
    definition:
      union:
        - method: state
          value: modified+       # changed + parents + children
        - method: config.materialized
          value: ephemeral       # allow ephemeral deps to materialize in graphs
    description: "Models impacted by this PR"

  - name: pr_tests
    definition:
      intersection:
        - method: test_type
          value: generic         # schema tests only (fast, focused)
        - method: state
          value: modified+       # test the impacted surface
```

**CLI:**

```c
dbt --warn-error --partial-parse --state target/artifacts \
  build --select pr_scope pr_tests
```

**Why it works:** You exercise the *smallest complete subgraph* that could be broken by the PR. No more surprise runs of distant, unrelated marts.

## 2) Smart Deferral to Prod (without lies)

Deferral lets dev builds reuse **already built relations** from a reference environment, so CI doesn’t re-materialize the world.

**Prep once:**

1. Nightly (or after main merges), publish artifacts to a durable location (e.g., object storage) alongside the **prod state**.
2. Grant CI read access to the prod schema/database.

**CI command:**

```c
dbt --warn-error --partial-parse \
  --defer --state s3://artifacts/dbt/main/last_success \
  build --select pr_scope
```

What happens:

- Nodes **touched by the PR** build in the CI schema.
- Everything else is **deferred** to the prod relations (read-only).
- The graph is evaluated as if it were complete, but only the changed slice is recomputed.

**Guardrails:**

- Add a `target.name: ci` with its own schema naming convention (e.g., `ci_${GITHUB_RUN_NUMBER}`) to avoid collisions.
- Block `--defer` when the reference environment is stale (see Tactic 5).

## 3) Tests That Matter in PRs (and the rest at night)

Let’s be real: running every test on every PR feels “safe” and *isn’t*. It burns time, raises flake risk, and numbs reviewers. Split your testing strategy:

**In PR CI (fast & focused):**

- **Generic schema tests** on the impacted surface (`unique`, `not_null`, `accepted_values`).
- A small set of **unit tests** (dbt v1.6+) for logic-heavy models that changed.
- **Contract checks** if you’ve adopted model contracts (great for downstream stability).
```c
# Schema tests for the impacted graph
dbt test --select pr_tests

# Unit tests (namespaced near the model)
dbt test --select state:modified,type:unit
```

**Nightly (deep & broad):**

- Data-heavier custom tests, source freshness, snapshot validations, end-to-end marts.

**Bonus:** Make broken **schema tests a merge blocker**, while nightly failures ping the owning team.

## 4) Partial Parse + Artifact-First Workflows

Large repos spend more time **planning** than **running**. Partial parse keeps planning near-instant by reusing metadata from prior runs.

**Always include:**

```c
dbt --partial-parse --state target/artifacts ...
```

**And make artifacts first-class citizens:**

- **Publish artifacts** (`manifest.json`, `run_results.json`, `catalog.json`) from your main branch to S3/GCS (or Git LFS) after green builds.
- **Consume artifacts** in PR CI via `--state` for slim selection, and to render PR summaries (e.g., “3 models changed, 7 tests executed, 0 failures”).

**GitHub Actions example:**

```c
# .github/workflows/dbt-ci.yml
jobs:
  slim-ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install dbt-core dbt-bigquery
      - name: Fetch state artifacts
        run: aws s3 cp s3://artifacts/dbt/main/last_success ./state/ --recursive
      - name: dbt Slim CI
        run: |
          dbt deps
          dbt --warn-error --partial-parse --state ./state \
            build --select pr_scope pr_tests --target ci
      - name: Upload PR summary
        if: always()
        run: python ./.ci/render_summary.py  # reads run_results.json
```

**Payoff:** Sub-minute planning for big DAGs, and tidy PR context for reviewers.

## 5) Hygiene: Contracts, Ownership, and “No Stale State” Rules

Slim CI is a trust exercise. These small guardrails make it dependable:

**a) Enforce model contracts where stability matters**

```c
# models/marts/orders.yml
models:
  - name: dim_customers
    contract:
      enforced: true
    columns:
      - name: customer_id
        data_type: string
        constraints:
          - type: not_null
          - type: primary_key
      - name: country
        data_type: string
```

Contracts fail fast when a PR changes column types or removes required fields — without a full build.

**b) Own your DAG**

Add `meta: {owner: "team-analytics"}` and a short description to each model. Route CI failures to the right Slack/label automatically.

**c) Never defer to stale**

Before running with `--defer`, verify the reference artifacts are fresh:

```c
python - <<'PY'
import json,sys,datetime,os
m=json.load(open('state/manifest.json'))
ts = datetime.datetime.fromisoformat(m['metadata']['generated_at'].replace('Z','+00:00'))
age=(datetime.datetime.now(datetime.timezone.utc)-ts).total_seconds()/3600
if age>6:
  print(f"State too old: {age:.1f}h"); sys.exit(2)
PY
```

**d) Keep schemas clean**

CI schemas should be ephemeral: destroy them on job completion or on a nightly janitor job to avoid surprises and quota waste.

## Example: a “just enough” Slim CI job

```c
# 1) Prep environment
dbt deps

# 2) Sanity-check the reference state
python .ci/check_state_freshness.py ./state/manifest.json --max-age-hours 6

# 3) Build only impacted models, deferring to prod for the rest
dbt --warn-error --partial-parse --state ./state --defer \
  build --select pr_scope --target ci

# 4) Run only focused tests for the impacted surface
dbt --warn-error --partial-parse --state ./state \
  test --select pr_tests --target ci
```

**What reviewers see:** “This PR touched 3 models, built 3, ran 14 schema tests, all green.” Enough context to approve without guessing.

## Tiny pitfalls to dodge (so you don’t learn the hard way)

- **Dangling refs:** If a PR deletes a model, ensure selectors include **parents** so failure appears early.
- **Ephemeral surprises:** Ephemeral models folding into different materializations can change performance; include them in `pr_scope`.
- **Snapshot drift:** Snapshots rarely need PR-time runs; validate them nightly unless a PR touches the snapshot logic itself.
- **Seed noise:** Seeds can be large. Gate PR seed refresh behind labels or a separate job.

## Conclusion

Slim CI isn’t a hack; it’s a discipline. Select the smallest safe graph, defer to truth you trust, run tests that matter, parse once, and demand clean artifacts. Do these five and your PRs feel light, your reviewers feel confident, and your main branch stops living in fear of “one tiny model change.”

[![Neurobyte](https://miro.medium.com/v2/resize:fill:96:96/1*iCEe0GKNIQENJVU8Gk4QlQ.jpeg)](https://medium.com/@kaushalsinh73?source=post_page---post_author_info--33c6a1789a22---------------------------------------)

[![Neurobyte](https://miro.medium.com/v2/resize:fill:128:128/1*iCEe0GKNIQENJVU8Gk4QlQ.jpeg)](https://medium.com/@kaushalsinh73?source=post_page---post_author_info--33c6a1789a22---------------------------------------)

[857 following](https://medium.com/@kaushalsinh73/following?source=post_page---post_author_info--33c6a1789a22---------------------------------------)

Tech enthusiast & lifelong learner sharing insights on gadgets, AI, and productivity. Writing to inspire curiosity & spark ideas.