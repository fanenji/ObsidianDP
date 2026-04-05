---
title: "Mastering dbt Observability: Monitoring, Alerting, and SLAs for Analytics Pipelines"
source: https://medium.com/tech-with-abhishek/mastering-dbt-observability-monitoring-alerting-and-slas-for-analytics-pipelines-a6704dcd01b3
author:
  - "[[Abhishek Kumar Gupta]]"
published: 2025-11-21
created: 2026-04-04
description: "Mastering dbt Observability: Monitoring, Alerting, and SLAs for Analytics Pipelines Modern analytics pipelines are only as valuable as they are reliable. Stakeholders care less about how elegant the …"
tags:
  - clippings
  - dbt
  - monitoring
  - observability
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Mastodon](https://me.dm/@abhishekkgupta0)## [Tech with Abhishek](https://medium.com/tech-with-abhishek?source=post_page---publication_nav-f9b6be363a21-a6704dcd01b3---------------------------------------)

[![Tech with Abhishek](https://miro.medium.com/v2/resize:fill:76:76/1*3DNIUqR0e-kHFWIXdq0REQ.png)](https://medium.com/tech-with-abhishek?source=post_page---post_publication_sidebar-f9b6be363a21-a6704dcd01b3---------------------------------------)

Real-world AI, Cloud, and Data Engineering articles.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*jQ-PdDRdvQ_T3dX1nd6fSw.jpeg)

Observability turns dbt projects into reliable, monitored data products with clear SLAs

Modern analytics pipelines are only as valuable as they are reliable. Stakeholders care less about how elegant the SQL is and more about whether numbers are correct, fresh, and delivered on time. Observability for dbt is how analytics engineers make that reliability visible and enforceable: monitoring runs, surfacing failures quickly, tracking freshness, and measuring data SLAs across the stack.

*This article goes deep into how to design observability for dbt: native job monitoring and alerts, working with dbt artifacts, building your own observability models, defining SLAs/SLOs, and integrating with observability tools.*

## Why Observability Matters for dbt Pipelines

Observability in dbt is about answering three questions quickly:

1. Are jobs running as expected?
2. Is the data correct and fresh?
3. If something breaks, can the team see it and fix it fast?

Without structured observability, teams end up firefighting: silent failures, stale dashboards, and last‑minute surprises before exec reviews. With the right patterns, dbt becomes a data product platform with reliability characteristics you can measure, improve, and communicate through SLAs and SLOs.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*dZ--7Gu_sZCgH8zrudUPHg.png)

Good observability answers whether dbt jobs are running, data is correct, and data is fresh — all at a glance.

## Native dbt Cloud Monitoring and Alerts

dbt Cloud provides first‑class monitoring for runs and jobs:

- **Job history and run details:** Each job run records status, timing, the triggered user or schedule, and logs.
- **Job notifications:** You can configure alerts for job success/failure, warnings, and timeouts to email or Slack via “job notifications.”
- **Retry behavior:** Jobs support retry policies so transient warehouse issues don’t immediately cause incidents.

### Example: Configuring Job Notifications (dbt Cloud)

In dbt Cloud UI, for a given job:

Add notification rules like:

- “On failure → notify #data‑alerts Slack channel and on‑call email.”
- “On success of nightly prod job → notify BI team email.”

> This gives you coarse‑grained observability for when whole jobs fail or succeed. The rest of the article focuses on going much deeper.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*xptokBFKydM0w5rtnJLCqA.jpeg)

Native dbt Cloud monitoring and job notifications provide the first layer of observability.

## Understanding dbt Artifacts: The Foundation of Custom Observability

Every dbt run produces artifacts that describe what happened: models built, tests executed, timings, failures, and lineage. These artifacts are JSON files you can parse and load into your warehouse.

**Key artifacts for observability:**

- `run_results.json`: Results of the last run—status, timings, failure messages per node (model/test/snapshot).
- `manifest.json`: Complete graph of your project—nodes, dependencies, config, tags, exposures.
- `sources.json` / freshness outputs: Freshness check results for sources, including status and lag.

**Example:** `**run_results.json**` **(conceptual)**

For each executed node, you typically get:

- `unique_id` – node identifier (e.g. `model.my_project.fact_orders`)
- `status` – `success`, `error`, `skip`, `warn`
- `execution_time` – seconds spent on that node
- `thread_id` – which worker ran it
- `message` – error details or extra info

> These structures are stable and documented, and they’re exactly what you need to fuel custom dashboards and SLOs.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*L6oGuXYZ_liw_HTly4K0Tw.jpeg)

## Loading Artifacts into Your Warehouse

To move from logs to analytics, a common pattern is:

1. Store artifacts after each run (in S3/GCS/Azure Blob or a dbt Cloud artifact store).
2. Ingest artifacts into raw JSON tables (e.g., one row per artifact file).
3. Model artifacts in dbt into structured tables (jobs, runs, model metrics, test metrics, freshness).
4. Expose these meta‑tables to BI tools for observability dashboards.

**Example: Simple Artifact Landing Table (Snowflake/BigQuery style)**

You might land `run_results.json` as:

```c
-- raw.run_results: one row per run_results file
select
  parse_json(raw_content) as run_results_json,
  load_timestamp
from raw_run_results_files;
```

Then in dbt, parse into a structured model:

```c
-- models/observability/run_results_flat.sql
with base as (

    select
      run_results_json,
      load_timestamp
    from {{ ref('raw_run_results') }}

),

flattened as (

    select
      load_timestamp as ingested_at,
      value:unique_id::string              as unique_id,
      value:status::string                 as status,
      value:execution_time::float          as execution_time,
      value:thread_id::string              as thread_id,
      value:message::string                as message
    from base,
    lateral flatten(input => run_results_json:results) as f

)

select *
from flattened;
```

> This gives you a fact table of node executions you can slice by model, status, and time.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*JopOV8Q63aEI40pN9oyeXw.jpeg)

A simple pattern: capture dbt artifacts, land them in the warehouse, then model them for observability.

## Defining Data SLAs and SLOs with dbt

dbt Labs distinguishes data SLAs (contracts about data timeliness/reliability) and SLOs (measurable target levels like “99% of runs succeed on time”).

**Common SLA dimensions:**

- Freshness: e.g., “Daily revenue dashboard refreshed by 8:00 AM local time.”
- Success rate: e.g., “99.5% of nightly prod dbt runs succeed monthly.”
- Latency: e.g., “Critical models complete in < 30 minutes.”

**dbt gives you primitives to enforce these:**

- Source freshness checks via `sources:` and `freshness:` blocks in YAML.
- Tests for data quality (unique, not\_null, relationships, custom tests).
- Artifacts + observability models to track whether SLAs were met historically.

**Example: Source Freshness SLA**

```c
version: 2

sources:
  - name: core
    tables:
      - name: orders
        freshness:
          warn_after: { count: 2, period: hour }
          error_after: { count: 4, period: hour }
        loaded_at_field: loaded_at
```

Running `dbt source freshness` yields a JSON/console report. You can ingest that into a `source_freshness` table and flag SLA breaches (e.g., `status = "error"` or lag > threshold).

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*5kVVii_xVib8NMfIspL9ww.jpeg)

SLAs and SLOs make data reliability measurable and visible for stakeholders.

## Building an Observability Model Layer in dbt

With run and freshness data in your warehouse, you can now build structured observability marts.

**Typical models:**

- `obs_job_runs` – per job run: status, duration, environment, triggered\_by.
- `obs_node_runs` – per node: status, duration, model/test type, tags.
- `obs_sla_results` – per SLA: on-time vs late vs failed.
- `obs_data_quality` – rolled-up view of test pass rates by domain or team.

**Example: SLA Results Model (Conceptual)**

```c
-- models/observability/obs_sla_results.sql
with runs as (
    select
      job_id,
      started_at,
      finished_at,
      status,
      date_trunc('day', started_at) as run_day
    from {{ ref('obs_job_runs') }}
),

evaluated as (
    select
      job_id,
      run_day,
      count(*)                                 as runs,
      sum(case when status = 'success' then 1 else 0 end) as successes,
      sum(case when status != 'success' then 1 else 0 end) as failures
    from runs
    group by job_id, run_day
)

select
  job_id,
  run_day,
  runs,
  successes,
  failures,
  successes::float / runs as success_rate
from evaluated;
```

> You can compare `success_rate` against SLO targets (e.g., 0.995) for each job or domain.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*rBOyIfcQrwdxJE4zbDPwoQ.jpeg)

An observability model layer turns raw artifacts into structured metadata for dashboards and alerts.

## Alerting Strategies: Native + External Observability Tools

### Native dbt Cloud Alerts

- **Job notifications:** Direct to email, Slack, or webhooks.
- **Run/schedule monitoring:** Use dbt Cloud’s “Monitor jobs and alerts” to track job health, configure fail/warn behavior, and see historical trends.

> This is simple and effective, especially for small teams.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*iv-DCKwF6UlShGac57Letg.jpeg)

dbt integrates naturally into broader observability stacks for anomaly detection and incident workflows

## External Observability Tools

To go beyond “job passed/failed,” teams integrate dbt with:

- **Metaplane:** Monitors dbt tests, freshness, schema changes; provides dbt-native integration and alerting.
- **Databand, Bigeye, Monte Carlo, Elastic Observability:** Use dbt artifacts, warehouse metrics, and logs to detect anomalies in run time, row counts, freshness, and test failure patterns.

**Common patterns:**

- Push metrics (job duration, failure counts, test failure counts) to Datadog/Prometheus/Elastic using custom exporters or webhooks.
- Configure alerts: e.g., “if failure rate for `obs_sla_results` > 0.5% over 24 hours, send PagerDuty alert.”

> This turns dbt into a first‑class citizen of your broader observability stack.

**Example: Building a dbt Observability Dashboard**

Once you have models like `obs_job_runs` and `obs_node_runs`, building a dashboard in Looker/Tableau/Power BI is straightforward.

**Useful tiles:**

- **Job SLA tile**: % of prod jobs that finished before SLA time.
- **Failure trend**: Failed runs per day/week, broken down by environment.
- **Slowest models**: Top N models by median/95th percentile runtime.
- **Data quality overview**: Count of failing tests by severity (error vs warn) over time.

> This dashboard is great to show in read-outs with engineering and business stakeholders to demonstrate the health of your data platform.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*qGpsv93FYY7z4mIuF3wpIw.jpeg)

A dedicated observability dashboard makes the health of dbt pipelines easy to monitor and discuss

## Incident Response and On-Call Playbook

Observability is only useful if it drives action. A solid on-call playbook might include:

1. Alert fires (dbt job failed, SLA breached, or anomaly detected).
2. Check observability dashboard: Which job/model failed? Is it isolated or part of a pattern?
3. Inspect artifacts/logs: Open the run in dbt Cloud, look at `run_results` and model logs to identify root cause.
4. Assess impact: Which downstream dashboards/exposures depend on this model? (Use manifest/lineage.)
5. Communicate: Notify stakeholders (e.g., “Sales dashboard delayed by 30 minutes while we re-run job X”).
6. Fix & follow-up: Patch model, add missing test or guardrail, update SLA/SLO docs if needed.

> Documenting this process and linking it to your dbt observability dashboards closes the loop from detection → diagnosis → resolution → prevention.

## Conclusion

dbt observability is not just about catching red error states; it is about building a consistent, measurable contract between your data platform and the business. By combining native dbt Cloud monitoring, rich artifacts, and external observability tools, teams can design pipelines with clear SLAs, visible health, and trustworthy outcomes.

Over time, this turns your dbt project from “a collection of models” into a reliable data product — complete with uptime charts, SLOs, and incident playbooks that leadership understands and respects.

## 💡 Final Thoughts

Observability is where analytics engineering meets reliability engineering. The same discipline that transformed application uptime can transform how organizations think about the reliability of data and metrics.

> “A great data platform doesn’t just produce tables; it produces confidence — measured, monitored, and improved over time.”

**👉 If** you’ve built clever dbt observability patterns — custom dashboards, artifact tricks, or integrations with tools like Datadog/Metaplane/Databand — share your stories and approaches in the comments. Your lessons can help the broader community build more trustworthy analytics pipelines.

[![Tech with Abhishek](https://miro.medium.com/v2/resize:fill:96:96/1*3DNIUqR0e-kHFWIXdq0REQ.png)](https://medium.com/tech-with-abhishek?source=post_page---post_publication_info--a6704dcd01b3---------------------------------------)

[![Tech with Abhishek](https://miro.medium.com/v2/resize:fill:128:128/1*3DNIUqR0e-kHFWIXdq0REQ.png)](https://medium.com/tech-with-abhishek?source=post_page---post_publication_info--a6704dcd01b3---------------------------------------)

[Last published 6 days ago](https://medium.com/tech-with-abhishek/dbt-tips-that-senior-engineers-swear-by-but-rarely-document-af9978e535d4?source=post_page---post_publication_info--a6704dcd01b3---------------------------------------)

Real-world AI, Cloud, and Data Engineering articles.

[![Abhishek Kumar Gupta](https://miro.medium.com/v2/resize:fill:96:96/1*EyqcUd4VgjYXp8UQ6vRNiA.jpeg)](https://medium.com/@abhishekkrgupta0?source=post_page---post_author_info--a6704dcd01b3---------------------------------------)

[![Abhishek Kumar Gupta](https://miro.medium.com/v2/resize:fill:128:128/1*EyqcUd4VgjYXp8UQ6vRNiA.jpeg)](https://medium.com/@abhishekkrgupta0?source=post_page---post_author_info--a6704dcd01b3---------------------------------------)

[86 following](https://medium.com/@abhishekkrgupta0/following?source=post_page---post_author_info--a6704dcd01b3---------------------------------------)

I build smart data systems that think, act, and fix themselves. Writing real-world guides on GenAI, LLMs, observability, and everything in between.