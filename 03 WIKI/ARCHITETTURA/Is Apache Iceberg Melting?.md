---
title: Is Apache Iceberg Melting?
source: https://medium.com/@andymadson/is-apache-iceberg-melting-c8fbb3771f52
author:
  - "[[Andymadson]]"
published: 2026-01-21
created: 2026-04-04
description: Is Apache Iceberg Melting? Data engineers have seen this pattern before. A few high-profile companies publish an architecture post, vendors amplify it, and within a year half the industry is “doing …
tags:
  - clippings
  - architecture
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*9d2Dc0EAeLi9zT5tO5rsSg.png)

Data engineers have seen this pattern before. A few high-profile companies publish an architecture post, vendors amplify it, and within a year half the industry is “doing the same thing” regardless of whether the underlying problem exists in their environment.

Apache Iceberg sits right in the middle of that skepticism. It started at Netflix and became a major open-source project with broad engine support. Nearly every modern analytics platform roadmap references it now, and it’s showing up in places that have nothing to do with Netflix’s original stack.

So is Iceberg the open table format of the future, or cargo cult behavior wrapped in technical credibility?

My take is blunt. Iceberg solves real, repeatable enterprise bottlenecks in cloud data lakes. The move toward lakehouse-style architecture is happening because those bottlenecks became operationally and financially unacceptable. Iceberg is not a fad. It’s infrastructure.

This piece is for practicing data engineers. It’s technical by design, but it also calls out the strategic drivers and operational trade-offs you’ll own after migration.

## The Cargo Cult Question Is Fair

A cargo cult migration usually looks something like this. An organization copies a reference architecture without matching the original constraints. They adopt a new format for a headline feature (often “time travel” or “ACID”) but keep the old operating model. They end up with more moving parts, more cost, and no measurable reliability or performance win.

Iceberg can absolutely be deployed this way. If you only convert a pile of Parquet files into “Iceberg tables” and don’t change how you handle metadata, maintenance, and write coordination, you won’t get the benefits you think you’re buying.

But that’s not Iceberg’s fault. It’s a mismatch between what Iceberg actually is and what teams expect it to be.

## What Iceberg Is (and What It Isn’t)

Iceberg is an open table format for huge analytic datasets. It adds SQL table semantics on top of files in object storage and makes those tables usable across multiple compute engines like Spark, Trino, Flink, Presto, Hive, and Impala.

Iceberg is not a storage engine. ==Your data still lives in Parquet, ORC, Avro, or similar formats==. It’s not a query engine either. You still need Spark, Trino, Flink, a warehouse engine, or something else to run queries. And it’s not a catalog by itself. Iceberg relies on a catalog layer to map a table name to the current metadata location and perform atomic updates of that pointer.

This matters because most “Iceberg disappointments” come from treating Iceberg like a database. You don’t install Iceberg and walk away. You operate an Iceberg-based table layer.

## Why Enterprises Needed an Open Table Format in the First Place

The lakehouse concept didn’t emerge from a marketing meeting. The underlying argument is straightforward. Enterprises want the low-cost, open-format storage benefits of a data lake combined with the reliability and management features historically associated with data warehouses.

In practice, the pressure came from a set of recurring pain points in traditional “files plus a metastore” data lakes.

**Correctness under concurrent reads and writes.** Traditional Hive-style tables on object storage weren’t built for high concurrency or transactional guarantees. When multiple pipelines write, backfill, or mutate partitions concurrently, data correctness becomes a social process instead of a technical guarantee.

**Object storage semantics.** At cloud scale, operations like directory listing and rename aren’t just slow. They can be unreliable or inconsistent depending on the storage system’s behavior. Iceberg explicitly avoids relying on file listing and rename operations, making it compatible with object stores without requiring consistent listing.

**Partitioning lock-in.** The moment you choose a partition scheme, you bake that decision into every downstream job. Changing it later often means rewriting huge volumes of data or supporting parallel layouts with manual query routing.

**Schema drift and long-lived tables.** Enterprises evolve schemas constantly. If schema evolution is risky, teams slow down changes or proliferate parallel tables. Both approaches compound data debt.

**Scan planning at scale.** A “table” with millions of files and partitions becomes a planning problem. If a query engine must enumerate everything to decide what to read, latency and cost explode.

Iceberg was designed to address these specific failure modes.

## The Iceberg Mechanics That Actually Solve Enterprise Bottlenecks

Iceberg’s value is in its metadata architecture and transaction model. If you understand those two things, the rest of the feature set makes sense.

## Atomic Commits and Serializable Isolation on Object Storage

Iceberg maintains table state in metadata files. Every change creates a new metadata file and replaces the old metadata with an atomic swap. The metadata tracks schema, partition configuration, custom properties, and snapshots.

The Iceberg spec lays out the core concurrency model clearly. Reads are isolated from concurrent writes and always use a committed snapshot. Writes support adding and removing files in a single operation and are never partially visible. Readers don’t acquire locks.

This isn’t a nice-to-have feature. It’s the difference between being able to run ingestion, backfills, and data quality remediation without coordinating over Slack.

Consider multi-team writes without handoffs. If your environment has multiple teams writing to the same fact table (separate pipelines for late-arriving events, corrections, and GDPR deletes, for example), the transaction model keeps readers from seeing partial states.

Reality check though. Iceberg uses optimistic concurrency. Conflicting commits can fail and require retries. Large maintenance operations can conflict with frequent writes. Cloudera’s optimization guidance explicitly calls out commit conflicts as something you need to plan for.

## Snapshot-Based Time Travel and Rollback That’s Operationally Useful

Iceberg supports reproducible queries by referencing a specific table snapshot, and it supports rollback to a known-good state when something goes wrong.

This matters in real operations. You can prove what data an ML model was trained on. You can reproduce a regulatory report exactly as of a cutoff time. You can roll back a bad load without rewriting the world.

Iceberg also supports branching and tagging. The official docs call out GDPR handling and audit retention as explicit use cases, not just developer convenience.

## Hidden Partitioning and Partition Evolution Without Rewriting the Table

Iceberg’s partitioning is “hidden.” You define transforms like `day(event_time)`, and Iceberg tracks the relationship between the source column and the partition values.

Two practical wins come out of this. Queries don’t have to encode physical partition paths to be efficient. Iceberg prunes files based on metadata. And you can evolve the partition spec over time. The evolution documentation shows different partition layouts coexisting within the same table, like month partitions for older data and day partitions for newer data.

This is one of the most underappreciated enterprise benefits. Partition schemes change because businesses change. Iceberg reduces the cost of adapting.

## Schema Evolution That Doesn’t Break Production

Iceberg supports schema evolution operations like add, drop, rename, update (safe widening), and reorder, including nested structures.

A key detail that makes this safe is the use of field IDs. The Iceberg specification requires column IDs to be stored as Parquet field IDs, enabling safe evolution even when names or positions change.

This isn’t theoretical. If you’ve ever had a “rename a column, break downstream jobs” incident, you already know why stable IDs matter.

## Efficient Scan Planning and Metadata-Driven Pruning

Iceberg is explicit about planning complexity. Operations should use O(1) remote calls to plan a scan, not O(n) calls that grow with table size like the number of partitions or files.

Iceberg’s metadata hierarchy (snapshots, manifest lists, manifests, data files) exists to support this. The spec notes that manifest list files store metadata about manifests, including partition stats and file counts, that can be used to avoid reading manifests that aren’t needed.

This is where you get tangible cost reductions. AWS published test results in an incremental processing scenario where Athena scanned 50% or less data for a given query on an Iceberg table compared to the original data before conversion. A separate enterprise case study reported nearly 50% reduction in I/O costs and 40–50% reduction in query latency for complex aggregations on larger datasets after moving to an Iceberg-style approach.

Don’t over-generalize these numbers. Your mileage will vary based on file sizing, partitioning, column stats, and the engine. But the mechanism is real. Richer metadata enables better pruning and better planning.

## Are Companies Copying Netflix, or Solving Repeatable Problems?

Netflix is part of Iceberg’s origin story, and it’s fair to be wary of “do what Netflix does” reasoning. But the adoption pattern around Iceberg is bigger than Netflix.

Here are credible signals that enterprises are adopting Iceberg to solve common constraints.

**Large companies outside Netflix are using Iceberg for internal lakehouse needs.** Apple has publicly discussed using Iceberg as part of its lakehouse and contributing engineering effort back into the project. An Apple engineering manager described Iceberg use “all over the place,” spanning hundreds of MB to many PB, with investments in features like maintenance procedures and row-level operations for regulatory compliance.

Expedia Group’s engineering blog describes a data lake on S3 backed by Hive Metastore and the complexity that created, then frames table formats including Iceberg as an alternative built to take advantage of the cloud and provide ACID transactions, time travel, and partition spec evolution.

Stripe has shared publicly via Trino Fest that they use Iceberg tables extensively and replaced legacy Hive tables. They also describe a real operational friction point: reading Iceberg metadata from S3 and building internal tooling around it.

Those aren’t “copy Netflix” stories. They’re “we hit the same lake pain points at scale and needed a table layer” stories.

**Cloud and platform vendors are standardizing around Iceberg interoperability.** This is where the lakehouse conversation stops being theoretical.

Microsoft has said that Fabric OneLake will support Apache Iceberg. The Microsoft and Snowflake partnership announcement frames Iceberg as a foundation for bidirectional access between Snowflake and Fabric.

AWS has steadily expanded Iceberg support across its analytics services, including documented Iceberg internals on EMR and multiple implementation guides and performance discussions for Athena, Glue, and Redshift.

Snowflake has published documentation describing support for integrating Apache Iceberg tables, including general availability updates around Snowflake Open Catalog (formerly Polaris Catalog).

From an enterprise architecture standpoint, this matters more than any single company blog post. It means the industry is building “multi-engine on open storage” as a supported default, not an edge case.

**Databricks acquiring Tabular is a serious ecosystem accelerant.** In June 2024, Databricks announced it agreed to acquire Tabular, the company founded by Ryan Blue, Daniel Weeks, and Jason Reid, the original creators of Apache Iceberg.

That move did two things for Iceberg adoption. It put more commercial muscle behind the core Iceberg team. And it made Iceberg interoperability a top-tier strategic priority for a major platform vendor, not a side project.

Databricks has also publicly announced full Apache Iceberg support in its platform, including the ability to query and govern Iceberg tables managed by external catalogs like AWS Glue, Hive Metastores, and Snowflake catalogs.

None of this proves Iceberg “wins” forever. But it does prove Iceberg has crossed the line from interesting OSS project to strategic enterprise standard under heavy investment.

## The Lakehouse Architecture Question: Is It Real?

If you define lakehouse adoption as “enterprises consolidating storage on open formats in object storage and enabling multiple engines to read and write with warehouse-like guarantees,” then yes, it’s real. The vendor roadmaps reflect it.

What’s not real is a magic end state where everything becomes one system and the mess disappears. Lakehouse architectures reduce duplication and simplify interoperability, but they also shift responsibilities onto the data engineering organization.

You own table maintenance (compaction, snapshot expiration, manifest rewrites) unless a managed service does it for you. You own write coordination patterns and concurrency constraints. You own catalog reliability and access control design.

This is why Iceberg isn’t a fad. It’s directly aligned with how cloud data platforms are converging. But it’s also why Iceberg isn’t a free upgrade.

## Practitioner Guidance: How to Avoid a Cargo Cult Migration

If you want Iceberg’s benefits, you need to adopt its operating model, not just its file layout.

## Choose the Catalog Strategy Deliberately

The catalog is not optional. It stores the current metadata pointer for tables and must support atomic updates to that pointer.

Iceberg defines a REST-based Catalog API with an OpenAPI spec. That REST catalog direction is showing up across the ecosystem. AWS Glue documents an Iceberg REST endpoint for connecting engines to a REST catalog hosted in the Data Catalog. Apache Polaris (incubating) positions itself as a fully-featured catalog implementing Iceberg’s REST API for multi-engine interoperability. Snowflake Open Catalog is described as a managed service for Apache Polaris built on the Apache Iceberg REST protocol.

If you already run Hive Metastore or Glue today, you can start there. But if your strategy is multi-engine and multi-platform long-term, treat REST catalog compatibility as a first-class requirement.

## Plan Maintenance as Product Work, Not a Background Task

Iceberg’s features rely on metadata staying healthy. Common maintenance work includes compaction of small files into larger files, snapshot expiration and cleanup, and manifest rewrites and clustering strategies.

Some managed offerings will handle portions of this for you. Snowflake’s documentation for Snowflake-managed Iceberg tables explicitly notes that Snowflake handles life-cycle maintenance such as compaction, with the option to disable it.

If you’re running Iceberg “open” with Spark or Trino on object storage, assume you own these maintenance loops.

## Make Partitioning and File Sizing Part of Your Standards

Iceberg makes partition evolution safer, but partitioning still matters for performance. AWS Redshift best practices guidance for querying Iceberg emphasizes strategic partitioning to reduce data scanned.

Don’t treat “Iceberg will optimize it” as a substitute for sane physical design. Iceberg makes it easier to change later, but you still pay for bad choices now.

## Validate Multi-Engine Behavior Early

Iceberg’s core promise is that multiple engines can safely work with the same tables.

In practice, “supports Iceberg” varies by engine and version. Validate your exact workload patterns. Test reads and writes. Test schema evolution operations you rely on. Test row-level operations if you need them. Test time travel and snapshot retention needs.

This isn’t fear-mongering. It’s normal engineering due diligence in an ecosystem where support matures over time.

## Use Real Success Criteria, Not Vibes

A migration is justified when you can show improvements. Fewer data correctness incidents during backfills and reprocessing. Lower scan costs due to better pruning and planning. Faster delivery of schema changes without breaking downstream jobs. Reduced duplication by sharing the same tables across engines and teams.

If you can’t name the bottleneck you’re removing, you’re at high risk of building a cargo cult lakehouse.

## Bottom Line

Apache Iceberg isn’t the future because Netflix used it first. It’s the future because the technical problems it solves are common in enterprise cloud data lakes: correctness under concurrency, safe evolution, scalable planning, and interoperability across engines and vendors.

Enterprises are moving toward lakehouse-style architectures because major platforms are building around open storage plus an open table layer. Microsoft, AWS, Snowflake, and Databricks are all explicitly investing in Iceberg interoperability.

If you adopt Iceberg with a clear bottleneck in mind and commit to the operating model (catalog plus maintenance plus engineering standards), you’ll get real benefits. If you adopt it as a badge, you’ll get a more complex data platform and no payoff.

That’s the line between format of the future and classic cargo cult. The line is under your control.

[![Andymadson](https://miro.medium.com/v2/resize:fill:96:96/1*ZpKpf-eVvpkrSznNg4zBrA.jpeg)](https://medium.com/@andymadson?source=post_page---post_author_info--c8fbb3771f52---------------------------------------)

[![Andymadson](https://miro.medium.com/v2/resize:fill:128:128/1*ZpKpf-eVvpkrSznNg4zBrA.jpeg)](https://medium.com/@andymadson?source=post_page---post_author_info--c8fbb3771f52---------------------------------------)

[6 following](https://medium.com/@andymadson/following?source=post_page---post_author_info--c8fbb3771f52---------------------------------------)

Tech Evangelist @ Dremio, Former Sr. Director of Data Analytics, and VP of Machine Learning.

## Responses (2)

S Parodi

What are your thoughts?  

```rb
DuckLake!
```

1

==Your data still lives in Parquet, ORC, Avro, or similar formats==

```rb
These are more file formats than storage engines. AWS S3, Azure Data Lake Store or Google Cloud Storage are your storage engine.
```