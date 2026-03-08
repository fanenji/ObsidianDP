---
tags: ["cherrypick_snapshot"]
---

WAP (WRITE-AUDIT-PUBLISH) PATTERN

Write-Audit-Publish (WAP) is one of several key design patterns in data engineering that emphasize data quality and integrity, especially within data orchestration workflows. It works in three stages:

1. writing data to a non-production environment,
2. auditing this data to identify and rectify quality issues
3. publishing data to production.

Data developers use write-audit-publish with data orchestration tools to automate and monitor quality control processes throughout the data pipeline.

[Write-Audit-Publish in data pipelines | Dagster Blog](https://dagster.io/blog/python-write-audit-publish)

[Streamlining Data Quality in Apache Iceberg with write-audit-publish & branching](https://www.dremio.com/blog/streamlining-data-quality-in-apache-iceberg-with-write-audit-publish-branching/)

USING IGEBERG BRANCH

> In this approach, we will first create a new branch from our existing Iceberg table, stage the newly written changes (made by an ETL job) to this branch, make the necessary validations, and based on the quality checks, publish the new data to the main branch or just decide to drop the branch. The publish operation is facilitated by Iceberg’s **[cherry-pick](https://iceberg.apache.org/docs/latest/spark-procedures/cherrypick_snapshot)** procedure, which basically creates a new snapshot from an existing snapshot without altering or removing the original one.

![[excalidraw.com_HighRes-99-2048x1920.png]]
