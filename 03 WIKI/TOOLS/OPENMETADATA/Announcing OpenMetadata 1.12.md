---
title: "Announcing OpenMetadata 1.12"
source: "https://blog.open-metadata.org/announcing-openmetadata-1-12-9e15b66e7748"
author:
  - "[[Shawn Gordon]]"
published: 2026-02-24
created: 2026-02-26
description: "Announcing OpenMetadata 1.12 Standardize Quality Rules, Simplify Deployment, and Support Open Standards We’re excited to announce OpenMetadata 1.12, the latest release of our open-source metadata …"
tags:
  - "clippings"
  - tools
  - openmetadata

---
[Sitemap](https://blog.open-metadata.org/sitemap/sitemap.xml)## [OpenMetadata](https://blog.open-metadata.org/?source=post_page---publication_nav-3ebf5788f069-9e15b66e7748---------------------------------------)

[![OpenMetadata](https://miro.medium.com/v2/resize:fill:76:76/1*NTBaKucQjjMGziseWsSF5Q.png)](https://blog.open-metadata.org/?source=post_page---post_publication_sidebar-3ebf5788f069-9e15b66e7748---------------------------------------)

OpenMetadata is an open-source project that is driving Open Metadata standards for data. It unifies all the metadata in a single place in a Centralized Metadata store and helps people Discover, Collaborate, and Get their data right.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*GCc9VbwS054RNoekxpG2bQ.png)

## Standardize Quality Rules, Simplify Deployment, and Support Open Standards

We’re excited to announce OpenMetadata 1.12, the latest release of our open-source metadata platform. This release delivers on programmatic AI access, standardizes data quality at scale, simplifies deployment, and supports open standards. Highlights include:

- **AI SDK** provides programmatic access to OpenMetadata’s knowledge graph layer, enabling you to embed metadata intelligence into any application — custom chatbots, AI agents, or automated governance workflows in tools like Slack, GitHub, or n8n.
- **Data Quality Test Library** lets administrators create reusable SQL-based test templates that enforce consistent quality standards across the organization, eliminating scattered custom tests.
- **Kubernetes Orchestrator** removes the Airflow dependency for simplified cloud-native deployment — now you only need three components: application server, database, and search index.
- **Open Standards Support** includes ODCS 3.1 for data contracts and OpenLineage for lineage metadata ingestion, enabling interoperability with the broader data ecosystem.

Together with audit logs for transparency, column bulk operations for governance at scale, and significant improvements to lineage, this release empowers organizations to enforce standards while maintaining flexibility.

The Collate 1.12 release of the managed OpenMetadata service introduces powerful new AI capabilities. AI Studio gives you control over platform agents with customizable prompts. Combined with Auto Classification featuring custom recognizers, Data Diff column/row analysis, GitHub Metadata Sink, and dozens of other enhancements, Collate 1.12 extends OpenMetadata with enterprise-grade governance and AI-powered automation.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*M0ld3yfj_slS5GXZfQk-zw.png)

## MCP tooling, Semantic Search, and AI SDK

Release 1.12 introduces new tooling into OpenMetadata’s embedded Model Context Protocol (MCP) server, including lineage creation capabilities and data quality capabilities for test definitions, test case creation, and Root Cause Analysis.

Moreover, this release brings Semantic Search capabilities that leverage your data to create vector embeddings in OpenSearch, supporting Bedrock, OpenAI, and HuggingFace embeddings. This includes MCP tooling for Semantic Search as well.

Finally, the [OpenMetadata AI SDK](https://github.com/open-metadata/metadata-ai-sdk) provides programmatic access to OpenMetadata’s semantic layer via MCP, enabling you to embed metadata intelligence into any application or workflow. Build custom chatbots, automate governance tasks, and integrate OpenMetadata’s semantic understanding into tools like Slack, GitHub, n8n workflows, or any custom application.

- **Build on OpenMetadata’s Unified Metadata Graph:** Access lineage, quality metrics, ownership, and business meaning through a simple API, eliminating the need to reconstruct this complex knowledge graph yourself.
- **Intelligence for workflows:** Embed agents in your platform that bring OpenMetadata Semantic Intelligence into your existing AI systems.

**Why this matters:** Manually integrating metadata intelligence with multiple systems creates fragmented experiences and duplicated effort. The SDK lets you embed semantic intelligence wherever your teams work, bringing OpenMetadata to where work happens instead of forcing users to come to you.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*6MA-EVRj2i0JpMZtrm0a5w.png)

## Data Quality Test Library

The Data Quality Test Library transforms how organizations standardize data quality testing. Administrators create reusable, parameterized test definitions through a GUI, eliminating the inconsistency and technical complexity of custom SQL tests scattered across the organization. This provides a superior alternative to dbt’s generic tests while maintaining centralized governance.

- **Reusable test templates:** Define SQL-based test templates with parameters that users fill in through a no-code interface. For example, create an “ARR validation” test once, then apply it consistently across 20 different tables without rewriting SQL.
- **GUI-driven experience:** Unlike dbt’s YAML-based approach, which requires technical knowledge, administrators define tests through a visual interface, and users apply them through simple forms — no code required.
- **Centralized governance:** Admins control which tests are available organization-wide, disable irrelevant tests, and ensure everyone uses standardized definitions for critical business rules.

**Why this matters:** Organizations waste countless hours reinventing the same data quality tests with slight variations, undermining trust and consistency. The Test Library centralizes business logic into reusable templates, ensuring your rules mean the same thing across every table and transforming ad-hoc testing into standardized quality enforcement at scale.

⭐ **Like what you see in 1.12?** [**Star the OpenMetadata GitHub repo**](https://github.com/open-metadata/OpenMetadata) **to support the project and help the community grow!**

## Kubernetes Orchestrator

Kubernetes Orchestrator eliminates OpenMetadata’s Airflow dependency using Kubernetes as the native scheduler. This simplifies deployment from four components to three, making OpenMetadata truly cloud-native.

- **Simplified architecture:** Reduces infrastructure requirements to just application server, database (RDS/Postgres/MySQL), and search index (OpenSearch/Elasticsearch)
- **Cloud-native deployment:** Leverage existing Kubernetes clusters without managing separate Airflow installations
- **Easier operations:** Fewer components mean simpler monitoring, updates, and troubleshooting
- **Community-driven:** Built in response to feedback that Airflow complexity was creating deployment friction

**Why this matters:** Many teams reported that Airflow’s complexity made OpenMetadata deployment difficult, despite our original intent to leverage existing infrastructure. By using Kubernetes directly — which teams already run — we’ve removed this deployment barrier. This makes OpenMetadata accessible to more organizations while simplifying operations for everyone.

## Open Standards: ODCS 3.1 & OpenLineage

OpenMetadata 1.12 embraces open standards for contracts and lineage, enabling interoperability while maintaining our richer semantic model.

**ODCS 3.1 Support:**

- Import contracts in Open Data Contract Standard 3.1 format
- Export OpenMetadata contracts to ODCS for tool interoperability
- OpenMetadata’s contract spec provides additional capabilities for richer semantics (terms of service, ownership, quality definitions)

**OpenLineage Integration:**

- Native API ingestion of OpenLineage-compliant lineage metadata
- Support for Flink, Spark, Airflow, dbt, and other OpenLineage producers
- OpenMetadata’s lineage extended spec provides support beyond OpenLineage: APIs, OLTP systems, S3, data warehouses, dashboards, data models, and more

**Why this matters:** Open standards prevent vendor lock-in and enable best-of-breed tool selection. Organizations with existing ODCS contracts or OpenLineage implementations can adopt OpenMetadata without rewriting integrations. And OpenMetadata’s superset approach means you get standard compatibility plus enhanced capabilities and support — the best of both worlds.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*tupCL_Prj5iMt-l-o2Jxkw.png)

## User & AI Audit Logs

Comprehensive audit logs now track all user and AI agent actions across the platform, providing full visibility into who changed what, when, and why. Export capability and filtering by user or AI agent enable governance oversight and troubleshooting.

- **Complete activity tracking:** Every metadata change — whether by a human or an AI — creates an audit log entry showing the user, timestamp, affected entity, and the actual payload that changed.
- **AI agent accountability:** Track exactly which AI agents took which actions, ensuring transparency as agents create documentation, modify tags, or generate test cases.
- **Filtering and export:** Slice logs by user, agent, time range, or action type, then export results for compliance reporting, security audits, or offline analysis.

**Why this matters:** As AI agents increasingly make automated changes to metadata in partnership with human data teams, organizations need accountability and traceability. Audit logs provide the transparency enterprises require, letting you audit what agents and users have done.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*3UVeWhL32BCQllVtEDBAdA.png)

## Column Bulk Operations

Column Bulk Operations aggregates identical column names across all asset types for unified governance at scale.

- **Cross-asset aggregation:** Find all instances of a column name across tables, topics, containers, APIs, and search indexes in a single view
- **Bulk updates:** Set descriptions, tags, and glossary terms for all instances simultaneously
- **Flexible filtering:** Narrow operations by domain, tier, tags, or metadata status

**Why this matters:** When customer\_id appears in 50 tables with inconsistent documentation, governance becomes impossible. Column Bulk Operations treats identical column names as a single entity, allowing you to manage them once and achieve enterprise-wide metadata consistency.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*3xHNmu-iydcEvKk0Ckj6_w.png)

## Lineage Improvements

Continued investment in lineage brings significant usability and performance enhancements.

- **Column-only filtering:** View lineage for specific columns without visual noise from unrelated paths
- **Edge highlighting:** Hover over nodes to highlight connected edges; selection highlights the complete path
- **Stored procedure support:** Edit mode now supports stored procedures in lineage graphs
- **Column pagination:** Navigate large schemas with hundreds of columns more efficiently
- **Faster SQL parsing:** SQLglot integration dramatically speeds query parsing for complex lineages with thousands of nodes

**Why this matters:** Lineage graphs with thousands of nodes were difficult to navigate and slow to render. These improvements make complex enterprise lineages usable, letting teams actually understand data flows rather than getting lost in tangled spaghetti diagrams.

## Additional OpenMetadata Features

- **Explore Page Sidebar:** Quick-access panel showing asset details, lineage, and quality information without full-page navigation. Preview metadata, then return to the search results with a single click.
- **Test Case Import/Export:** Bulk operations on data quality tests at the table and multi-table levels through import/export workflows.
- **Data Contracts at Data Product Level:** Define contracts once at the data product level with automatic inheritance to all assets, centralizing governance definitions.
- **Distributed Search Indexing:** Multiple application servers share the indexing workload for better scalability with millions of assets.
- **Data Product Input/Output Ports:** Support for input/output port specifications with lineage visualization, aligning with data product specifications.
- **Timezone-Aware Freshness Tests:** Set specific time zones on freshness tests to match the database, preventing UTC misalignment.
- **Column Custom Properties:** Side panel drawer interface for column-level custom properties with improved navigation.
- **Snowflake Dynamic Table Metrics:** System metrics (INSERT, UPDATE, DELETE) support for Snowflake dynamic tables.
- **New Connectors:** StarRocks (highly requested by the community), SFTP for unstructured data, and Redshift Serverless.

## Collate 1.12 Features

The Collate managed OpenMetadata service extends the project with powerful enterprise capabilities:

- **AI Studio** provides visibility and control over platform agents with customizable prompts and restore-to-defaults capability, laying the foundation for custom agent creation in 2.0.
- **Custom Auto Classification** lets you create ML-powered recognizers for any classification — not just PII — with feedback loops for continuous improvement.
- **Data Diff Column/Row Analysis** provides a granular visual comparison of differences between source and target tables at the column, row, and character level.
- **GitHub Metadata Sink** (beta) brings metadata under version control, enabling code review workflows, CI/CD integration, and treating metadata with the same governance rigor as application code.
- **AskCollate Enhancements** include expanded entity support (metrics, knowledge center, dashboard data models), company context-awareness that fetches definitions from your glossary, MS Teams integration, enhanced transparency into thinking, and automatic chart generation.
- **SQL Studio Extensions** adds Postgres and Redshift support alongside existing Snowflake, Trino, and BigQuery, with secrets manager and hybrid deployment options.
- **Metadata Exporter — Entity History:** Export complete change tracking to Snowflake, BigQuery, or Databricks for custom dashboarding using your preferred BI tools.
- **Learning Resources:** Contextual tutorials and videos throughout the UI based on the current page, with admin customization for organization-specific materials.
- **New Collate Connectors:** Microsoft Fabric (beta) for unified metadata across the Microsoft data stack, Dremio for lakehouse platforms, and MuleSoft for API management.

Check out the [Collate 1.12 release blog](http://getcollate.io/blog/announcing-collate-1-12) for more details on these features.

## Try It Out and Learn More

Ready to get started? You can [install OpenMetadata 1.12](https://docs.open-metadata.org/) today, try it out with demo data in the [live sandbox](https://sandbox.open-metadata.org/), or sign up for [Collate’s free tier](https://www.getcollate.io/welcome) of managed OpenMetadata service.

If you have questions about setting up OpenMetadata, read our [documentation](https://docs.open-metadata.org/) to get started, [join the Slack community](https://slack.open-metadata.org/), and provide feedback on [GitHub](https://github.com/open-metadata/OpenMetadata).

⭐ [**Star the OpenMetadata GitHub repo**](https://github.com/open-metadata/OpenMetadata) **to support open source innovation and help more teams discover the project!**

[![OpenMetadata](https://miro.medium.com/v2/resize:fill:96:96/1*NTBaKucQjjMGziseWsSF5Q.png)](https://blog.open-metadata.org/?source=post_page---post_publication_info--9e15b66e7748---------------------------------------)

[![OpenMetadata](https://miro.medium.com/v2/resize:fill:128:128/1*NTBaKucQjjMGziseWsSF5Q.png)](https://blog.open-metadata.org/?source=post_page---post_publication_info--9e15b66e7748---------------------------------------)

[Last published 2 days ago](https://blog.open-metadata.org/announcing-openmetadata-1-12-9e15b66e7748?source=post_page---post_publication_info--9e15b66e7748---------------------------------------)

OpenMetadata is an open-source project that is driving Open Metadata standards for data. It unifies all the metadata in a single place in a Centralized Metadata store and helps people Discover, Collaborate, and Get their data right.

All things data, developer, sustainable energy enthusiast as well as prolific musician.

## More from Shawn Gordon and OpenMetadata

## Recommended from Medium

[

See more recommendations

](https://medium.com/?source=post_page---read_next_recirc--9e15b66e7748---------------------------------------)