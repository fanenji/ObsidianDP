---
title: Chill Your Data with Iceberg Write Audit Publish
source: https://medium.com/expedia-group-tech/chill-your-data-with-iceberg-write-audit-publish-746c9eb3db48
author:
  - "[[Vincent DANIEL]]"
published: 2025-09-02
created: 2026-04-04
description: Apache Iceberg introduces WAP + Branching, enabling teams to write data into an isolated branch, perform audits and validations, and only publish to the main branch once the data passes quality checks. This ensures zero disruption to production and avoids unnecessary duplication.
tags:
  - clippings
  - ci-cd
  - wap
  - nessie
  - iceberg
topic:
type: note
---
## EXPEDIA GROUP TECHNOLOGY — DATA

## A strategic shift toward data flows that are version-controlled, testable, and auditable

Ensuring data quality in production environments is critical — but challenging — especially when test environments lack access to live data. Traditional approaches often involve duplicating production tables for User Acceptance Testing (UAT) and validation, leading to resource overhead, governance challenges, and inconsistencies.

![People row boats in spring](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*iE2enMFwR2FLl72L)

Photo by Yu Kato on Unsplash

## What is Write‑Audit‑Publish?

**Write‑Audit‑Publish (WAP)** is a robust data validation workflow that improves data quality by staging data changes through three steps:

![Write New data is written to an isolated, non-production environment, preventing disruption to production. Audit The data is validated with quality checks such as, NULL detection, Duplicate checks or schema integrity. Publish After passing audits, data is atomically committed to the production environment, ensuring consistency and accuracy.](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*PFgk_9Fta0bTwLyN.png)

Source: Write-Audit-Publish Stages

1. **Write**  
	New data is written to an **isolated**, non-production environment, preventing disruption to production.
2. **Audit**  
	The data is **validated** with quality checks such as, NULL detection, Duplicate checks or schema integrity.
3. **Publish**  
	After passing audits, data is **atomically committed** to the production environment, ensuring consistency and accuracy.

This method reduces risk, enhances reviewability, and ensures only clean data enters production systems. Apache Iceberg offers a powerful alternative which allows teams to validate and test changes using isolated branches — **without touching or duplicating production data**.

## A different approach with Iceberg WAP

Apache Iceberg introduces **Write‑Audit‑Publish**, enabling teams to write data into an **isolated branch**, perform **audits and validations**, and only **publish to the main branch** once the data passes quality checks. This ensures zero disruption to production and avoids unnecessary duplication.

```rb
┌───────────────────┐
                     │    Main Branch    │
                     └────────┬──────────┘
                              │
                     Create WAP Branch
                              │
                     ┌────────▼────────┐
                     │   UAT Branch    │
                     └────────┬────────┘
                              │
              Write Data → Perform Validations & Audits
                              │
                     ┌────────▼────────┐
                     │ Validation Pass?│
                     └───────┬─────────┘
                     ┌───────┴───────────────┐
                     │                       │
                 Yes ▼                       ▼ No
              ┌──────────────┐        ┌────────────┐
              │ Fast-Forward │        │  Delete    │
              └──────┬───────┘        │  Branch    │
                     │                └────────────┘
                     ▼
             ┌───────────────────┐
             │   Main Branch     │
             │     Updated       │
             └───────────────────┘
```

Here’s how WAP works with Iceberg:

1. **Write (on a WAP branch)**  
	Data is written to a hidden branch (e.g.,`uat_branch`) that doesn’t impact production.
2. **Audit (from the WAP branch)**  
	Teams can validate data directly on this branch using SQL, Trino or Spark — without affecting users or the main table.
3. **Publish**  
	Once validated, publishing is done via **fast-forwarding** the metadata to production — efficiently and atomically.

## WAP: Generic vs Iceberg comparison

![WAP: Generic vs Iceberg Comparison](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*8sv2o8UnIazUv7lT.png)

WAP: Generic vs Iceberg comparison

## Why this matters

In many enterprise data platforms, production environments are secured, making direct access to production data from test either restricted or impossible. This often leads to:

- Data duplication for testing purposes
- Risk of stale or inconsistent data in UAT
- Operational overhead in maintaining cloned environments

## Key benefits:

- **No code duplication**  
	Reuse the same Extract, Transform, Load (ETL) logic and pipelines across production and UAT — no need for separate workflows.
- **Isolated testing environments**  
	Branches act as safe sandboxes for testing transformations or validations without impacting production.
- **Minimal storage overhead**  
	No full table duplication — branches reuse underlying data files, reducing storage and compute costs.
- **Significant cost savings**  
	By avoiding duplicated tables, redundant jobs, and unnecessary storage, this approach reduces infrastructure and operational expenses.
- **Efficient promotion to production**  
	Publishing changes is a fast metadata operation — no file rewrites, table swaps, or downtime.
- **Auditability and traceability**  
	Each branch and commit is versioned, making it easy to track, validate, and roll back changes.
- **Built-in rollback support**  
	Easily discard or revert branches if validation fails — production remains untouched.
- **Support for concurrent writers**  
	Enable multiple developers or pipelines to test and validate independently in isolated branches.

## Step-by-step implementation

### Enable WAP on the table

First, ensure that the WAP pattern is enabled on your target table:

```rb
ALTER TABLE prod.db.table SET TBLPROPERTIES ( 'write.wap.enabled' = 'true' );
```

### Create the UAT branch

Create a new branch starting from a specific snapshot (e.g., snapshot 3) and retain it for 7 days:

```rb
ALTER TABLE prod.db.table CREATE BRANCH \`uat_branch\` AS OF VERSION 3 RETAIN 7 DAYS;
```

### Perform writes on the UAT branch

Set the Spark session to write to the `uat_branch`:

```rb
SET spark.wap.branch = uat_branch;
```

Then, perform your data insertion or updates:

```rb
INSERT INTO prod.db.table VALUES (3, 'c');
```

### Audit the UAT branch

After the write operations, validate the data quality on the `uat_branch`. This can include checks for data integrity, completeness, and consistency.

### Publish changes to the main branch

Once the data quality checks are successful, publish the changes from `uat_branch` to the main branch:

```rb
CALL catalog_name.system.fast_forward('prod.db.table', 'main', 'uat_branch');
```

Only an Iceberg branch (e.g., uat\_branch) that is an ancestor of another branch (e.g., main) can be fast-forwarded to match the state of that other branch. If any ancestor snapshot has been deleted, you might encounter the following error message:

> *“Cannot fast-forward: main is not an ancestor of branch\_uat.”*

This occurs because Iceberg requires a direct lineage between branches for fast-forwarding to work.

You can use the set\_current\_snapshot procedure to set the current snapshot of the current table state. This procedure does not require the target snapshot to be an ancestor of the current table state. This makes it especially useful when fast-forwarding fails due to missing ancestor snapshots.

### Expire the UAT branch

After the changes are published, the `uat_branch` will be automatically removed when its retention period expires (7 days in this case).

## Extending branch retention

Sometimes you may want to keep a branch around longer than its initial retention period to allow extended testing or audits. Iceberg lets you update a branch’s retention period by recreating or replacing the branch starting from its current state with a new retention window.

For example, to extend the retention of the `uat_branch` from 7 days to 14 days, you can run:

```rb
ALTER TABLE prod.db.table 
CREATE OR REPLACE BRANCH uat_branch AS OF BRANCH uat_branch RETAIN 14 DAYS;
```

This command resets the branch starting point to its current version while updating the retention period.

**Key points:**

- This operation does not affect the branch data but updates how long snapshots and metadata are kept before automatic cleanup.
- Extending retention increases storage requirements, so plan accordingly.
- Avoid concurrent writes while changing retention to prevent conflicts.

By managing branch retention flexibly, teams gain more control over their data lifecycle and can accommodate longer validation windows without duplicating data or environments.

## Why drop a branch?

When a branch is used for testing or validation and **the data quality checks fail**, it’s best to drop the branch immediately instead of waiting for its retention period to expire(if one exists). This approach helps because:

- **Avoids confusion:** Keeping a failed test branch around can mislead teams into thinking it’s still active or valid.
- **Frees resources early:** Dropping the branch immediately releases metadata and any associated resources sooner, reducing storage overhead.
- **Maintains clean environment:** It keeps the branching structure tidy by removing invalid or obsolete branches quickly.
- **Prevents accidental usage:** Eliminates the risk that stale or failed test data might accidentally be queried or used.

In essence, dropping branches right after test failures ensures your environment stays clean, efficient, and focused only on valid, tested data.

## Why disable WAP?

Disabling WAP blocks writes on all branches. This can be helpful for **temporarily** making **branches read-only**, but should only be done with a clear understanding of the potential impact on other processes that rely on WAP.

## Lightweight auditing with historical tags

Beyond branching for WAP, Iceberg also supports **tags**, which are immutable, named pointers to snapshots. These enable low-overhead saving of historical versions — ideal for audit, compliance, or long-term snapshots:

```rb
-- Tag end-of-week snapshot, retain for 7 days
ALTER TABLE prod.db.table CREATE TAG \`EOW-01\`
  AS OF VERSION 7 RETAIN 7 DAYS;
-- Tag end-of-month snapshot, retain for 6 months
ALTER TABLE prod.db.table CREATE TAG \`EOM-01\`
  AS OF VERSION 30 RETAIN 180 DAYS;
-- Tag end-of-year snapshot indefinitely
ALTER TABLE prod.db.table CREATE TAG \`EOY-2024\`
  AS OF VERSION 365;
```

These tags inform `expire_snapshots` not to **clean up the referenced snapshots** —even as other intermediate snapshots are discarded.

You can then query past states directly using:

```rb
SELECT * FROM prod.db.table VERSION AS OF 'EOM-01';
```

Tags serve as a **fast** and **cost-effective alternative to backup tables** with snapshots and selective retention baked in.

## Disadvantages

While branching and tagging offer numerous advantages, there are some important downsides to consider:

### Storage overhead

Each branch and tag introduces additional metadata — and in some implementations, data duplication — into the system. In large-scale environments with heavy branching and extensive tagging, this can result in substantial storage overhead. Teams must adopt effective data retention, pruning, and cleanup strategies to prevent unnecessary data bloat.

### Complexity

Managing a growing number of branches and tags adds organizational complexity:

- Ensuring consistent naming conventions becomes crucial to maintain clarity.
- Understanding the branching structure requires discipline and tooling.
- Orphaned or stale branches and tags must be regularly pruned to avoid confusion and drift.

Without strong governance, teams can quickly lose visibility into the role and status of each branch or tag.

### Schema evolution with branches

The schema associated with a table is shared across all branches, meaning that when writing data to a branch, the table’s current schema is always used for validation. In contrast, querying a tag relies on the schema tied to the snapshot at the time the tag was created. This difference can introduce confusion when schema evolution occurs frequently, so teams must carefully manage compatibility between branches and snapshots.

## Cost Savings in Practice: Expedia Group

One of the biggest advantages of Iceberg WAP is **cost efficiency**. Traditionally, each release required duplicating production tables and reprocessing the same ETL pipeline twice — once in test (UAT) and again in production. This doubled compute costs, inflated storage usage, and added operational overhead to keep UAT environments in sync.

With Iceberg branches, data is **written once** into a temporary branch, validated in place, and then promoted to production through a lightweight metadata fast-forward. This means the test run is the production run — **eliminating duplicate work**. At scale, this shift can reduce release costs by **up to 99%**.

At Expedia, this change was transformative. Previously, every new pipeline required several terabytes of duplicated UAT data and a full second run of the ETL process. After adopting WAP:

- UAT tables were replaced with **temporary Iceberg branches**, avoiding full data copies.
- ETL pipelines were **executed only once**, reused seamlessly across test and production.
- Publishing became nearly instantaneous, as it was just a metadata operation.

The results were clear:

- **~30% lower storage consumption** by eliminating UAT table duplication.
- **Up to 99% reduction in release costs**, since pipelines no longer reprocessed data twice.
- **Faster, safer deployments** with cleaner governance and traceable audit history.

By removing the need to reprocess data twice, Iceberg WAP turns testing and release from a costly bottleneck into a **lightweight, scalable, and cost-effective workflow**.

## Final thoughts

The Iceberg WAP model isn’t just a technical improvement — it’s a shift toward **version-controlled, testable, and auditable data pipelines**. By validating in isolated branches and publishing with lightweight metadata operations, teams reduce risk, cut costs, and speed up delivery.

The result: **cleaner data, lower overhead, and greater trust** in production.

## Further reading

Explore how this pattern is implemented in real-world scenarios:

- [AWS Blog: Write-Audit-Publish with Iceberg and Glue Data Quality](https://aws.amazon.com/blogs/big-data/build-write-audit-publish-pattern-with-apache-iceberg-branching-and-aws-glue-data-quality/)
- [Netflix’s Approach to Scaling Iceberg Data Quality](https://vutr.substack.com/p/how-does-netflix-ensure-the-data?r=2rj6sg&utm_campaign=post&utm_medium=web&triedRedirect=true)
- [Iceberg Docs: Branching & Tagging](https://iceberg.apache.org/docs/latest/branching/)

> [Learn about life at Expedia Group](https://careers.expediagroup.com/life/)