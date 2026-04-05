---
title: "Why Every Data Lake Needs a Control Plane: Lessons from Apache Iceberg"
source: https://medium.com/@amitgil87/why-every-data-lake-needs-a-control-plane-lessons-from-apache-iceberg-2c035d4386ef
author:
  - "[[Amit Gilad]]"
published: 2025-09-11
created: 2026-04-04
description: Data Lake Architecture
tags:
  - clippings
  - architecture
  - iceberg
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)

Over the past year, I’ve spoken with dozens of companies that either migrated their existing platforms to **Apache Iceberg** or built **greenfield projects** directly on Iceberg. Almost all of them saw **better performance** than their old stack right out of the gate — queries ran faster, they had to freedom to use any query engine they desired on top of the same data, adoption looked promising.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*GJLCCQEsD3ExOB9F)

But then reality set in. For those who migrated, Iceberg delivered performance gains, **but not the transformative leap they had hoped for**. And as datasets grew, another problem appeared: **storage costs started to climb sharply**. Organizations were expanding their data lakes without fully understanding how Iceberg’s maintenance procedures work or when to run them. Old snapshots piled up, delete files accumulated along side with small data files and tables quietly bloated in the background.

This is not a technology failure — it’s an **operational gap**. Without a **control plane** to orchestrate and enforce table hygiene across catalogs and query engines, every team ends up with its own defaults, its own maintenance schedules, and blind spots that silently eat into cost and compliance.

That’s why I’m starting a **series of deep dives** into the **critical role of a control plane for data lakes**. Each post will unpack one operational aspect that, if unmanaged, turns Iceberg from a performance boost into a hidden cost center.

We’ll begin here with the most fundamental task: **expiring snapshots**.

We’ll begin here with **expiring snapshots** task:  
At its core, snapshot expiration is about keeping your lake lean and fast — removing old table history, reclaiming storage, and shrinking metadata. And in our next posts we will talk about each procedure and its importance:

- **Rewrite Data Files (Compaction)**  
	Consolidates small files into larger ones and merges delete files into base data files. Critical for Merge-on-Read (MOR) tables to physically apply deletes and reduce query overhead.
- **Rewrite Manifests**  
	Optimizes manifest lists and manifest files by consolidating metadata, which reduces planning time and lowers query latency.
- **Rewrite Position Delete Files**  
	Cleans up dangling delete files that no longer match any data, keeping reads efficient and ensuring GDPR hard deletes are fully applied.
- **Remove Orphan Files**  
	Deletes stray files left behind by failed jobs or mislocated writers. Prevents “dark storage” costs and ensures only tracked data is kept in the table location.
- **Expire Snapshots (covered in this post)**  
	Deletes snapshots and their referenced data files that exceed retention policies, reclaiming storage and shrinking metadata.
- **Maintain Puffin Files (Statistics & Indexing)**  
	Puffin files are auxiliary files introduced in Iceberg to store column-level statistics and advanced indexes (like min/max values, bloom filters, or histograms). They improve query performance by allowing engines to prune data more aggressively without scanning all manifests or row groups.  
	Maintenance matters because Puffin files can drift out of sync as data evolves — if not updated, engines may stop benefiting from them or use stale statistics. A control plane can schedule Puffin file refreshes alongside compaction and snapshot expiration to ensure query planners always leverage the freshest statistics.

## Why expiration matters (storage & performance)

Each write creates a **snapshot**: a pointer to a set of manifests → data/delete files. Over time:

- **Storage creeps**: deleted/replaced files remain referenced by old snapshots.
- **Metadata grows**: more manifests/manifest lists, bigger metadata JSONs.
- **Snapshot Selection:** When a query targets a specific snapshot (e.g., for time travel), the query engine must locate and load the corresponding metadata files (manifest lists, manifest files, and associated data file entries). While Iceberg’s design aims for efficient metadata access, a very large number of snapshots can lead to larger metadata files and potentially slower initial query planning if the engine needs to traverse a long history of changes to find the relevant snapshot.

Iceberg’s maintenance guidance is explicit: **expire snapshots regularly** to delete unneeded data files and keep metadata small.

Yet in practice, without a **lake-wide control plane**:

- One team sets retention to 7 days, another leaves it at “forever.”
- Spark jobs expire snapshots, but Athena’s tables keep old versions.
- Ops assumes cleanup happened, but orphan files pile up unseen.

This is the silent fragmentation that kills performance and inflates costs.

## Estimating the Impact Before You Expire Snapshots

Not every table requires snapshot expiration on the same schedule — some grow quickly and accumulate massive amounts of metadata, while others remain fairly static. The challenge is that without visibility, teams either run expiration blindly on a schedule or don’t run it at all. A **preview of the impact** changes this dynamic: it helps you understand whether a table is truly suffering from metadata bloat or storage creep, or if expiration would have little effect. By seeing the potential space reclaimed and the number of files that would be affected before you execute, you can prioritize which tables to clean up, avoid unnecessary jobs, and make expiration a data-driven decision rather than a guess.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*MMz52rnCRCvMvSVEUzV7DA.png)

## Story Time

Take a simple use case: a table created as part of a daily ingestion pipeline by an employee who later left the company. The pipeline kept running, appending new data every day, but no maintenance procedures were ever put in place except for a generic compaction job that ran once a day. Without snapshot expiration, every snapshot the table ever created was still retained, along with its manifests and delete files. Over months, the table ballooned in size — not just in raw data, but in metadata overhead. Query planning started to slow down, and storage costs quietly climbed as “deleted” or replaced files were still pinned by old snapshots. What started as a well-functioning ingestion job turned into a silent tax on performance and storage simply because expiration policies were never applied.

## The DR/GDPR tension: time travel vs. purge(Needs rewrite)

### Disaster Recovery (branches/tags)

Iceberg lets you name and retain important points in time with branches and tags. Expiration will not remove any snapshot still referenced by a branch/tag; refs have their own retention (`max-ref-age-ms`). The default is “keep forever,” so you must set it, otherwise storage won’t drop.

A control plane ensures that **ref retention is enforced consistently** across catalogs. Without it, one branch/tag can hold gigabytes or even terabytes of data forever because no one set its policy.

### GDPR / Right-to-be-Forgotten

- **Copy-on-Write (COW)**: writes rewrite data files; expiring old snapshots clears physically deleted records.
- **Merge-on-Read (MOR)**: deletes create delete files; data files with sensitive rows may still be referenced by newer snapshots. To physically purge, run **compaction** (rewrite data files to apply deletes), then expire older snapshots.

Here too, defaults matter. If one table runs expiration daily but another never does, GDPR guarantees fall apart. A control plane coordinates **compaction → expiration → orphan cleanup** in the right order.

## Set table-level defaults (the “seatbelts”)

Iceberg exposes three key retention knobs:

- `history.expire.max-snapshot-age-ms` — default max snapshot age (5 days by default)
- `history.expire.min-snapshots-to-keep` — minimum snapshots to keep (default 1)
- `history.expire.max-ref-age-ms` — default max age for refs (branches/tags). The `main` branch never expires.

You can set these in Spark, Athena, or Trino — but **without a control plane** these defaults diverge across teams. [**Lakeops**](https://lakeops.dev/), for example, enforces a single policy across all tables and allow customizations per table.

## Run expiration safely (Spark, Trino)

**Spark SQL**

```c
CALL prod.system.expire_snapshots(table => 'prod.events');
CALL prod.system.expire_snapshots(
  table => 'prod.events',
  older_than => TIMESTAMP '2025-08-26 00:00:00',
  retain_last => 10
);
```

**Trino / Starburst**

```c
ALTER TABLE prod.events
  EXECUTE expire_snapshots(retention_threshold => '7d');
```

The key addition: a **control plane schedules these calls across all tables and engines**. Otherwise, you rely on scattered Airflow DAGs or Lambda scripts, with no central visibility.

## Retaining Recovery Points with Snapshot Tags

One of the most powerful but underused features in Iceberg is **tags**. Tags let you mark a specific snapshot with a friendly name and optional retention period. This means you can aggressively expire older snapshots to save storage, while still keeping **intentional rollback points** for operations, audits, or compliance.

## Why tags matter

- **Disaster Recovery**: tag a snapshot before a risky migration. Even if normal expiration policies would delete it, the tag protects it for the duration you specify.
- **GDPR Compliance Audits**: tag the table state before running GDPR purge jobs, giving you a checkpoint to validate the effect before the tag expires.
- **Release Safety**: engineering teams can tag the snapshot before a pipeline upgrade and roll back instantly if something breaks.

## Creating tags

**Spark SQL**:

```c
ALTER TABLE prod.events CREATE TAG dr_sept_2025 RETAIN 90 DAYS;
ALTER TABLE prod.events CREATE TAG pre_schema_update RETAIN 7 DAYS;
```

**Trino**:

```c
ALTER TABLE prod.events
  ADD SNAPSHOT REFERENCE 'dr_sept_2025'
  AS OF SNAPSHOT 1234567890
  RETAIN 90 DAYS;
```

## Expiration with tags

When you run `expire_snapshots`, Iceberg will **skip any snapshot referenced by a tag** until its retention period is over. That means you can reclaim storage aggressively, while still having defined rollback points.

## Tags + control plane

Without a control plane, tags can become “immortal” references that block cleanup forever. A control plane (like [**Lakeops**](https://lakeops.dev/)) enforces tag policies, tracks their lifecycle, and reports which tags are consuming storage — turning tags into a governance tool rather than a storage liability.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*hfx5BAileR7ZHWPa14-Isg.png)

## Branches & tags for DR that don’t block cleanup

Use **tags** for DR points and let them auto-expire according to your business use case:

```c
ALTER TABLE prod.events CREATE TAG day_2025_09 RETAIN 90 DAYS;
```

Refs prevent snapshot GC until their retention elapses — set ref retention or you will never reclaim space.

But remember: tags live across the whole lake, not just one table. A control plane tracks and expires them globally — otherwise you think you reclaimed storage, but hidden tags keep snapshots pinned forever.

## What does this mean for storage (and $$)?

- **Direct savings**: data files referenced only by expired snapshots become deletable.
- **Metadata savings**: fewer manifests and smaller metadata files → cheaper planning, faster queries.
- **Compliance savings**: GDPR and DR rules actually enforced lake-wide.

With no control plane, you can’t measure or prove these savings — finance sees a bill, but engineering can’t show where retention failed.

## A sane default policy you can roll out today

**Spark SQL**:

```c
ALTER TABLE prod.events SET TBLPROPERTIES (
  'history.expire.max-snapshot-age-ms'='1209600000',   -- 14 days
  'history.expire.min-snapshots-to-keep'='10',
  'history.expire.max-ref-age-ms'='7776000000'         -- 90 days
);
```
```c
CALL prod.system.expire_snapshots(table => 'prod.events');
```

**Trino**:

```c
ALTER TABLE prod.events EXECUTE expire_snapshots(retention_threshold => '14d');
```
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*mMVO4erlES-Ne2wy)

## Final thought

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*tBVI6UDho0JPDdSLBg2v3A.png)

Snapshot expiration is not a “vacuum once a quarter” chore — it’s **core hygiene**. Do it daily, tie it to your ref (DR) policy, and for MOR tables, make compaction + expiration a matched pair.

But hygiene alone isn’t enough. **Without a control plane, your lake drifts**: defaults diverge, jobs fail silently, orphan files pile up, tags never expire, and GDPR promises break.

That’s why solutions like [**Lakeops**](https://lakeops.dev/) exist — to provide the missing governance layer, orchestrating policies across catalogs, engines, and teams. With it, your “time travel superpower” stays a feature. Without it, it becomes a **storage tax**.

[![Amit Gilad](https://miro.medium.com/v2/resize:fill:96:96/0*xvR5XgaE05qBIsOk.jpg)](https://medium.com/@amitgil87?source=post_page---post_author_info--2c035d4386ef---------------------------------------)

[![Amit Gilad](https://miro.medium.com/v2/resize:fill:128:128/0*xvR5XgaE05qBIsOk.jpg)](https://medium.com/@amitgil87?source=post_page---post_author_info--2c035d4386ef---------------------------------------)

[59 following](https://medium.com/@amitgil87/following?source=post_page---post_author_info--2c035d4386ef---------------------------------------)

CEO and co-founder of LakeOps, building tools to simplify and scale data infrastructure. With a background in software engineering and system design