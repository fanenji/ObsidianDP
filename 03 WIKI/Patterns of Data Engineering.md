---
title: "Patterns of Data Engineering: Timeless Practices from Convergent Evolution"
type: note
topic: data-platform
created: 2026-04-04
tags:
  - data-engineering
  - design-patterns
  - architecture
  - reference
  - convergent-evolution
source: https://dedp.online
authors:
  - Simon Späti
---

# Patterns of Data Engineering

*Timeless Practices from Convergent Evolution*

**Author:** Simon Späti — ssp.sh
**Source:** https://dedp.online

---

## Table of Contents

- About This Book
- Introduction
- Terminologies
- Part 1 — Introduction to Convergent Evolution and Data Engineering
  - Chapter 1: Introduction to the Field of Data Engineering
  - Chapter 2: Introduction to Data Engineering Design Patterns (DEDP)
- Part 2 — Mastering the Data Engineering Design Patterns
  - Chapter 4: Convergent Evolution (CE) Examples
  - Chapter 5: Data Engineering Patterns (DEP)
  - Chapter 6: Data Engineering Design Patterns (DEDP)
- Appendix

---

## About This Book

*"Patterns of Data Engineering: Timeless Practices from Convergent Evolution"* is an evolving online book that explores fundamental design patterns in data engineering discovered through the lens of convergent evolution.

**Release Model:** The book is released progressively with author feedback integrated continuously, rather than being published as a finished product.

**Author:** Simon Späti, drawing on 20+ years of experience in business intelligence and data engineering.

**Core Concept:** The author applies convergent evolution — where different systems independently develop similar solutions — to reveal universal patterns in data engineering. As noted, *"both a bird and a bee can fly but in different ways,"* illustrating how distinct approaches can solve identical problems.

### What Readers Will Gain

- Historical context and current state of data engineering
- Understanding of convergent evolution and resulting design patterns
- Comprehensive coverage spanning architectures, data modeling, and common pitfalls
- Practical guidance on navigating today's complex data landscapes

### Target Audience

Intermediate-level professionals including data engineers, architects, scientists, and analysts who understand SQL basics and have worked with databases and ETL tools. Builds on foundational knowledge from introductory texts.

### Structure

The book uses "Patterns" rather than "Design Patterns" to encompass broader scope:
- **Convergent Evolutions (CE):** Discovery methodology
- **Data Engineering Patterns (DEP):** Recurring practices
- **Data Engineering Design Patterns (DEDP):** Implementable solutions

---

## Introduction

This book introduces design patterns in data engineering through three interconnected parts, drawing parallels to convergent evolution in nature.

### Three-Part Structure

**Part 1 — Foundational Concepts**
Explores convergent evolution and its relevance to data engineering, establishing why design patterns matter for solving recurring system challenges.

**Part 2 — Practical Patterns**
Covers essential design patterns including materialized views versus single tables, semantic layers, and dimensional modeling. *"This section will apply software engineering patterns to data engineering, such as CI/CD, version control, and a test-driven approach."*

**Part 3 — Future Navigation**
Examines emerging technologies and trends, including *"new programming languages such as Rust for data engineering, and the advent of vectorized engines and WebAssembly."*

### Chapter Organization

The book uses three chapter formats:

| Format | Focus |
|---|---|
| **CE Chapters** | Compare contrasting concepts with definitions, history, and core concepts |
| **DEP Chapters** | Pattern recognition, characteristics, and implementation approaches |
| **DEDP Chapters** | Problem-solution frameworks with architectural guidance |

---

## Terminologies

### How to Read This Book

This resource differs from conventional IT books by presenting a narrative structure rather than a reference handbook. *"Each chapter builds up to the actual data engineering design patterns (DEDP)."* Skipping sections may result in missing historical context and foundational concepts.

The book employs a **bottom-up methodology**, examining data engineering terminology established over twenty years while moving beyond industry hype. It analyzes convergent evolution patterns to identify recurring foundational concepts, ultimately converting these findings into practical design patterns and best practices.

### Website Navigation

- Press `S` to search the entire book
- Use the burger icon to toggle the chapter panel
- Access theme options via the brush icon
- Interactive graphs at chapter endings show connections to related content
- Internal links: full-color underlines; external links: subtle underlines

### Common Abbreviations

| Abbreviation | Meaning |
|---|---|
| DE | Data Engineering |
| CE | Convergent Evolution |
| DEP | Data Engineering Pattern |
| DEDP | Data Engineering Design Pattern |
| MDS | Modern Data Stack |
| ODS | Open Data Stack |

### Callout Types

- **Note** — General commentary
- **Info** — Supplementary but relevant details
- **Example** — Illustrative instances
- **Idea** — Thought-provoking concepts for exploration

---

# Part 1 — Introduction to Convergent Evolution and Data Engineering

---

## Chapter 1: Introduction to the Field of Data Engineering

### 1.1 History and State of Data Engineering

**Data Warehouse Origins (1980s)**
The formal definition of data warehousing emerged in the 1980s through Bill Inmon's foundational work. SQL simultaneously became standardized as a database language, building on Edgar F. Codd's 1970 proposal to abstract data storage complexities.

**Dimensional Modeling (1996)**
Ralph Kimball's *The Data Warehouse Toolkit* established dimensional modeling principles that remain relevant today for structuring analytical data.

**Big Data Era (2000s)**
Google's groundbreaking papers on the Google File System (2003) and MapReduce (2004) launched the big data movement. Yahoo's Hadoop distributed file system (2006) provided the essential toolbox with components like HDFS, YARN, and MapReduce for parallel processing across distributed systems.

**Cloud and Modern Stack (2010s–Present)**
AWS, Google Cloud, and Azure democratized data infrastructure. Technologies like Redshift, Snowflake, Airflow (2014), Superset (2015), and dbt (2016) transformed the landscape. Maxime Beauchemin's 2017 article *"Rise of the Data Engineer"* formally defined the discipline, followed by his 2018 framework on Functional Data Engineering.

**Current State (2022–2025):**
- Declarative approaches dominating infrastructure and orchestration
- Metadata management focus through cataloging and lineage tools
- Rust emerging for memory-efficient data processing
- Data privacy regulations shaping governance requirements
- Data modeling renaissance addressing Modern Data Stack complexity
- Vector databases gaining prominence alongside traditional options
- Open Data Stack gaining adoption with standardized formats (Parquet, Iceberg, Delta Lake)

> *"AI will lead us back to the fundamentals"* rather than replace data engineering roles. Focus remains on data quality, modeling, and presentation — the foundation enabling advanced analytics regardless of tooling sophistication.

### 1.2 Challenges in Data Engineering

Challenges exist across the full lifecycle — from data generation to actionable insights — organized around the data engineering lifecycle and its underlying undercurrents.

#### Lifecycle Challenges

**Generation Phase**
Data proliferates exponentially from devices and applications, creating frequency and volume issues. Engineers cannot control source systems directly and must synchronize data carefully to avoid impacting production performance. Schema changes and tracking deletions present additional complexities.

**Storage Phase**
The "Three Vs" framework (volume, velocity, variety) encapsulates storage decisions. Organizations must choose between traditional databases, cloud storage, or newer technologies — each with distinct cost and performance tradeoffs.

**Ingestion/Integration Phase**
The process of combining disparate sources into unified destinations requires careful architectural planning. Key questions include data frequency requirements, storage layer modifications, format compatibility, and stakeholder needs.

**Transformation Phase**
Perhaps the most technically complex layer. Challenges include maintaining evolving requirements, selecting appropriate tools, and balancing persistence versus logical definitions.

**Serving Phase**
The user-facing layer where data becomes actionable. Success requires compelling storytelling, appropriate format selection (dashboards, notebooks, APIs), and effective KPI presentation.

#### Critical Undercurrents

**Orchestration:** Managing dependencies, tracking computations, and handling errors across increasingly complex tool ecosystems.

**Software Engineering:** Data engineers must adopt programming rigor (version control, testing, code reusability) while working with uncontrollable input data — a fundamental difference from traditional software development.

**Security & Governance:** Balancing innovation with data protection, managing permissions, and ensuring compliance.

**DataOps:** Implementing infrastructure-as-code, containerization, and cultural shifts toward agile, collaborative approaches.

**Data Architecture:** Designing scalable, flexible platforms demands extensive experience and careful balance between upfront planning and pragmatic development.

#### Historical Context

Traditional Business Intelligence faced critical limitations: slow integration of new sources, lack of transparency in transformation logic, limited real-time capabilities, and difficulty handling unstructured data. Modern data engineering patterns address these shortcomings through improved speed, accessibility, and flexibility.

---

## Chapter 2: Introduction to Data Engineering Design Patterns (DEDP)

### 2.1 Convergent Evolution

Convergent evolution occurs when *"two distinct evolutions' outcomes are the same."* Classic examples:
- Birds and bees both developed flight through different biological mechanisms
- Bats and whales independently developed echolocation
- Vertebrates and cephalopods developed camera-style eyes

**Relevance to Data Engineering:** The field repeatedly "reinvents" similar concepts under new terminology. *"Parlance evolves faster than technology."*

The author traces the evolution of a caching pattern through multiple iterations:
- **Materialized Views** (Oracle, 1998)
- **One Big Table / Wide Tables** (denormalization techniques)
- **Snapshotting** (temporal caching)
- **Semantic Layers** (modern metric-focused caching)

Each represents the same fundamental goal: rapid data retrieval.

**Key Arguments:**
1. **Avoiding Hype:** New terminology doesn't necessarily indicate new technology. Understanding historical context prevents chasing buzzwords.
2. **The Lindy Effect:** Older, battle-tested techniques likely remain relevant longer than trendy alternatives.
3. **Pattern Recognition:** Identifying convergent evolutions reveals underlying design patterns with enduring value.

### 2.2 Pattern vs. Design Pattern

**Pattern:** A *"repeated, identifiable design, procedure, or practice"* observed across contexts. Patterns emerge from analyzing and comparing similar evolutionary developments.

**Design Pattern:** In engineering contexts, represents *"best practices"* and *"solutions to general problems developers face during development."* Originates from the seminal *Design Patterns: Elements of Reusable Object-Oriented Software* (GoF).

**Data Engineering Design Patterns (DEDP):** Domain-specific applications tailored to address recurring challenges in the Data Engineering Lifecycle.

### 2.3 Three-Level Framework

The book organizes knowledge from bottom-up:

| Level | Description | Examples |
|---|---|---|
| **Convergent Evolutions (CE)** | Technologies and approaches used daily | dbt, Data Lake, Message Queue, Microservices |
| **Patterns (DEP)** | Common themes from similar technologies | Caching, ELT, Data Lineage, Observability |
| **Design Patterns (DEDP)** | Best-practice solutions to specific challenges | Dynamic Querying, Real-Time Platform, Cost Management |

> *"Use this diagram throughout the book as your navigation map."*

Multiple convergent evolutions feed into patterns, which subsequently inform design patterns — creating a coherent understanding of how data engineering concepts relate systematically.

---

# Part 2 — Mastering the Data Engineering Design Patterns

---

## Chapter 4: Convergent Evolution (CE) Examples

### 4.1 Bash-Script vs. Stored Procedure vs. Traditional ETL Tools vs. Python-Script

This chapter traces the evolution of data orchestration from Unix-era bash scripts through modern Python frameworks.

#### Bash Scripts and Cron

**Definition:** Bash scripts combine shell command execution with parameter handling. Cron provides time-based scheduling using expressions like `0 8 * * *` for daily 8 AM execution.

**Historical Context:** Unix shells emerged in the 1960s–1970s, with Bash arriving in 1989. Cron was integrated into Unix Version 7 (1979).

**Core Strengths:**
- Exceptional scripting flexibility combining Unix utilities
- Simple parameter adaptation across scenarios
- Portable across Unix systems with minimal overhead
- Standardized time-based scheduling syntax

#### Stored Procedures

**Definition:** Database-native code running directly on the database engine, written in languages like PL/SQL (Oracle) or T-SQL (Microsoft).

**Historical Context:** Emerged during the 1970s–1980s relational database era, with significant adoption following SQL standardization in the 1990s.

**Key Advantages:**
- Eliminates network latency through database-native execution
- Database engine handles parallelization and transactions
- Optimized performance for complex data operations
- Manages business logic persistence within databases

#### Traditional ETL Tools

**Definition:** Software applications (Informatica, SSIS, Oracle OWB) facilitating extract-transform-load operations through GUI-based drag-and-drop interfaces.

**Historical Context:** Emerged around 1998 as organizations sought consolidated data insights from multiple sources.

**Core Process:**
- **Extract:** Connect to diverse sources, retrieve relevant data
- **Transform:** Apply business logic including cleansing and deduplication
- **Load:** Move processed data into analytical destinations

#### Python Scripts and Frameworks

**Definition:** Flexible Python-based orchestration ranging from simple scripts to comprehensive frameworks (Airflow, Dagster, Kestra).

**Historical Context:** Libraries like NumPy, SciPy, and Pandas (2000s) transformed Python into a data processing powerhouse. Modern orchestrators emerged 2015–2022.

**Framework Types:**
- Workflow Orchestration: Basic task scheduling
- Data-aware Orchestration: Context-conscious task execution
- YAML Orchestration: Bridging code-first and no-code approaches
- Implicit Orchestration: Event-driven, DAG-less execution

#### Key Patterns Across Approaches

| Pattern | Description |
|---|---|
| **Data-Flow Modeling** | Unified orchestration abstraction managing data movement and transformation |
| **Business Transformation** | Encoding organizational logic into automated processes |
| **Reusability** | Progressing from procedural toward declarative, component-reuse approaches |
| **Implicit Orchestration** | Event-driven architecture eliminating traditional centralized orchestrators |

**Evolution Summary:** Orchestration evolved from procedural, imperative sequential execution toward declarative, object-oriented frameworks. Modern approaches emphasize tool-agnostic, asset-aware orchestration.

---

### 4.2 Schema Evolution vs. Data Contracts vs. NoSQL

#### Schema Evolution

Managing structural changes to databases while maintaining data integrity. Evolved from rigid, manual processes in early systems (Oracle, System R) to modern automated tools like Liquibase and Apache Kafka's Schema Registry. Core techniques include slowly changing dimensions, data vault modeling, and automated schema versioning.

#### NoSQL

Emerged in 2009 to prioritize flexibility and speed over rigid schemas. NoSQL databases (MongoDB, Cassandra, Redis) embed schema definitions within documents. The movement prioritized horizontal scalability and eventual consistency, trading strict ACID compliance for availability and partition tolerance.

#### Data Contracts

A formal agreement between data producers and consumers defining format, structure, and validation expectations. Popularized by Andrew Jones (GoCardless, 2019) and Chad Sanderson (2022). Tools include Protocol Buffers and Apache Avro.

#### Comparison

| Aspect | Schema Evolution | NoSQL | Data Contracts |
|---|---|---|---|
| **Focus** | Structural changes | Flexibility and speed | Producer-consumer agreement |
| **Granularity** | Table-level | Document-level | Fine-grained interface |
| **Implementation** | Migrations, registries | Embedded schemas | YAML/JSON declarations |

#### Convergent Patterns

All three approaches share four recurring patterns:

1. **Change Management** — handling modifications without breaking systems
2. **Data Versioning** — tracking schema evolution and enabling rollback capabilities
3. **Data Lineage** — understanding data origins and transformations
4. **Data Asset** — treating databases/tables as managed, documented artifacts

---

### 4.3 Data Warehouses vs. MDM vs. Data Lakes vs. Reverse-ETL vs. CDP

#### Data Warehouse

Established in the 1980s by IBM researchers Barry Devlin and Paul Murphy. Integrates data from multiple sources into *"a single source of truth"* for analytics and decision-making.

**Core functions:**
- Consolidating data from diverse sources
- Applying business logic through modeling
- Enabling complex analytical queries without disrupting operational systems
- Supporting historical data analysis

Modern innovations: dimensional modeling, Data Vault, cloud-native platforms (2010s–present).

#### Master Data Management (MDM)

Roots trace back to Hollerith's punch cards (1890). Formal MDM frameworks developed in the 1990s. Microsoft's Master Data Services (2008) brought MDM to broader audiences.

**Key characteristics:**
- Centralizes critical business data (customers, products, etc.)
- Ensures *"data uniformity, accuracy"* across systems
- Involves clear governance and stakeholder accountability
- Addresses data quality through fuzzy matching

#### Data Lake

Emerged around 2010 as alternatives to traditional warehouses, using the ELT pattern rather than ETL.

**Architecture layers:**
1. **Storage Layer:** Cloud object storage (S3, Azure Blob, GCS)
2. **File Formats:** Apache Parquet, Avro, ORC
3. **Table Formats:** Delta Lake, Apache Iceberg, Apache Hudi

#### Reverse ETL

Inverts traditional data flows — moving processed insights from centralized repositories back to operational systems. Term gained prominence around 2021 (Hightouch).

**Primary benefits:**
- Makes analytical insights accessible within familiar business tools
- Enables *"operational analytics"* with added context
- Facilitates data activation and consistent syncing

#### Customer Data Platform (CDP)

Specialized data warehouses focused exclusively on customer information. Term coined by David Raab in 2013; CRM systems date to 1985 (TeleMagic).

**Distinguishing features:**
- Real-time data processing capabilities
- GDPR and CCPA compliance handling
- Unified customer view across touchpoints
- Business-focused vs. engineering-focused

#### Underlying Patterns

| Pattern | Description |
|---|---|
| **Data Sharing** | Making information universally accessible through open standards |
| **Reusability** | Performing work once in centralized locations, reducing duplication |
| **Business Transformation (ETL)** | Converting raw data into actionable insights |
| **In-Memory/Ad-Hoc Querying** | Enabling flexible, real-time analysis without pre-aggregated reports |

---

### 4.4 Materialized Views vs. One Big Table vs. dbt Tables vs. Traditional OLAP vs. DWA

Five interconnected approaches that persist SQL queries for improved query performance and business intelligence.

#### Key Definitions

**Materialized Views (MVs):** Database objects containing pre-computed SQL query results, stored on disk. Oracle introduced them in 1998; Google BigQuery added support in 2020.

**Traditional OLAP Cubes:** Multidimensional data structures (SSAS, SAP BW) that pre-calculate metrics and enable sub-second analytical responses through organized dimension hierarchies.

**dbt Tables:** SQL statements enhanced with templating and macro capabilities, executable through dbt's framework to create lineage graphs, enable testing, and support reusable transformations.

**One Big Table (OBT):** Wide, denormalized tables containing many columns within a single granularity level, exploiting cheap cloud storage and columnar architecture to eliminate join overhead.

**Data Warehouse Automation (DWA):** Tools automating data warehouse design, ETL creation, and documentation through templates and metadata-driven approaches.

#### Common Patterns

All approaches share three underlying patterns:

1. **Cache** — *"Persisting complex SQL queries into a table, abstracting business logic"* for rapid retrieval
2. **Business Transformation** — Storing persistent business value through domain expertise and logic
3. **Reusability** — Templating and stacking transformations following DRY principles

#### Key Distinctions

| | MVs | OBT | OLAP Cubes | dbt Tables | DWA |
|---|---|---|---|---|---|
| **Type** | Technology | Modeling | Modeling | Technology | Tool |
| **Flexibility** | Fixed granularity | Fixed granularity | Flexible dimensions | Fixed granularity | Template-driven |
| **Storage** | Native DB tables | Native DB tables | Proprietary format | Native DB tables | Generated artifacts |

#### Historical Evolution

`SQL → Data Mart → Materialized View → BI Report → Traditional OLAP → Modern OLAP → dbt tables → OBT → Semantic Layer`

---

### 4.5 Business Intelligence, Semantic Layer, Modern OLAP, and Data Virtualization

#### Business Intelligence Dashboard/Report

**Core capabilities:**
- **Roll-up:** High-level KPI visualization enabling quick assessment
- **Drill-down:** Detailed exploration from summary views
- **Single source of truth:** Unified, automated reporting across organizations
- **User empowerment:** Self-service analytics for non-technical users

Modern BI tools shifted from rigid, pre-built structures (SSRS, Oracle OBIEE) toward declarative, lighter solutions prioritizing external metric availability and transparency.

#### Semantic Layer

A logical translation layer between data and business users, converting raw data into understandable business concepts. Calculates metrics at query time, bridging data sources and analytics tools through SQL, REST, or GraphQL interfaces.

**Historical Development:**
- **1991:** SAP BusinessObjects Universe introduced the concept
- **2008:** Master Data Management (MDM) emerged
- **2018–2019:** dbt and Looker popularized modern approaches
- **2022:** Modern semantic layer tools proliferated (MetricFlow, dbt, Cube)

#### Modern OLAP Systems

Enable multidimensional business analysis with query-time metric definition, contrasting with traditional systems like SSAS that required pre-processing. Modern systems (Druid, Pinot, ClickHouse) define measures dynamically, supporting streaming data and sub-second response times.

#### Data Virtualization / Federation

Provides *"seamless access to data from multiple sources without duplication,"* using tools like Dremio or Trino to query diverse systems without moving data.

| | Benefits | Drawbacks |
|---|---|---|
| **Data Virtualization** | Reduced data movement, lower governance costs, rapid prototyping | Slower than materialized queries, potential source system impact |

#### Underlying Patterns

All four approaches share:

1. **Visualization/Business Focus** — Making data accessible to business users
2. **Translation/Abstraction** — Converting complex technical structures into business terms
3. **Data Modeling** — Using facts, dimensions, and logical layers
4. **Speed and Efficiency** — Prioritizing rapid query responses
5. **Single Source of Truth** — Ensuring consistency and accuracy
6. **Metrics Emphasis** — Central focus on KPIs and business metrics

Two consistent design patterns emerge: **Ad-hoc Querying** and **Caching**.

---

## Chapter 5: Data Engineering Patterns (DEP)

Data Engineering Patterns are repeated, identifiable designs and practices in data engineering. They build on convergent evolution concepts to help practitioners recognize patterns, features, and implementation approaches that align with common industry procedures.

### Key Patterns Addressed

| Challenge | Approaches |
|---|---|
| **Caching for BI** | dbt, materialized views, OLAP, data virtualization |
| **Orchestration** | Cron, Python, frameworks, custom solutions |
| **Master Data Integration** | Unique entity handling, fuzzy joins |
| **Tool Stack Selection** | Docker, Kubernetes, cloud solutions |
| **Data Sharing** | File export/import, delta live tables, open standards |
| **Asset Integration** | Stateful assets with stateless infrastructure |

### 5.1 Cache Pattern

Data caching involves storing multiple copies of data in temporary storage locations for faster access. The practice emerged from 1980s data warehouse concepts and remains central to modern data engineering solutions.

#### Key Characteristics

- **Rapid data retrieval** — systems access cached data much faster than retrieving from primary storage repeatedly
- **Multiple storage approaches** — ranging from simple disk copies to in-memory solutions and GPU-accelerated caching
- **Widespread adoption** — used in materialized views, OBT, dbt tables, semantic layers, and traditional/modern OLAP systems

> Martin Kleppmann characterizes caching as *"denormalized, derived data"* and categorizes OLAP/Data Cubes as specialized materialized views.

#### Applications

- **BI dashboards** — providing updated insights without recalculating from raw data
- **Real-time analytics** — enabling instant metric access
- **Data pipelines** — storing intermediate results to reduce source load

#### Implementations

| Tool | Description |
|---|---|
| **Redis** | In-memory data structure store; instant read/write, multiple data structures, replication, clustering |
| **Memcached** | Distributed memory object caching; speeds dynamic web apps by reducing database load |
| **Cube Store** | Custom implementation using Parquet storage + Arrow in-memory + DataFusion query execution |

#### Advantages

- **Speed** — significantly faster data retrieval
- **Efficiency** — reduces repetitive heavy data processing
- **User experience** — improved satisfaction through faster access

#### Challenges

- **Query specificity** — only identical queries benefit; different filters require separate cache entries
- **Data freshness** — maintaining accuracy with rapidly changing data
- **Complexity** — managing invalidation and consistency across storage, networking, and data engineering
- **Maintenance overhead** — building and sustaining custom cache layers is resource-intensive

#### Modern Alternatives

- **Advanced query engines** — DuckDB and WebAssembly enable near real-time access without intermediate storage
- **Data streaming** — Apache Kafka and Flink process continuously changing data in real-time

> Note: Most alternatives implement caching internally — they are partial rather than complete substitutes.

---

### 5.2 Data-Asset Reusability Pattern

Addresses avoiding duplication of code and data assets. *"The pattern minimizes duplicated business logic"* by abstracting complex transformations into reusable components.

#### Four Sub-Patterns

| Sub-Pattern | Description |
|---|---|
| **Template Parameterization** | Using variables and templates (dbt, Jinja, CTEs) to write logic once and reference it multiple times |
| **Asset Materialization** | Persisting computed results as tables or views to avoid recomputation across downstream systems |
| **Logic Encapsulation** | Bundling complex operations into simplified abstractions like semantic layers or MDM systems |
| **Parametric-Driven Generation** | Automatically generating code from configurations — *"write once, generate many"* via DWA platforms |

#### Benefits and Trade-offs

**Advantages:**
- Reduced maintenance overhead
- Faster development cycles
- Improved governance through centralized logic

**Risks:**
- Substantial upfront investment
- Potential over-abstraction leading to unnecessary complexity
- Cultural shift required to embrace standardization across teams

**Real-world examples:** dbt's Jinja macros for SCD Type 2 implementations; semantic layers that hide multi-table joins behind simple metric definitions.

---

### 5.3 Workspace Packaging Pattern

Encapsulates team-specific data tools, business logic, and configurations into portable, deployable units for consistent execution across environments.

*"Workspaces are a declaration of tools and logic a team has built, that can be tested on development, test, and executed on production."*

#### Three Sub-Patterns

**Runtime Standardization**
Uses containerization (Docker, DuckDB, Infrastructure as Code) to ensure consistent environments across deployment targets, eliminating "works on my machine" failures.

**Domain Isolation**
Establishes clear boundaries and interfaces enabling independent team deployments through data contracts, APIs, and separate git repositories per domain.

**Component Abstraction**
Reduces code duplication by packaging reusable technical utilities into versioned, shareable components (PyPI packages, dbt packages, shared libraries).

#### Real-World Examples

**HelloDATA-BE:** Integration through Airflow where external teams can add custom dbt transformations or Python scripts via standardized workspaces containing Dockerfiles and DAGs.

**GitLab's approach:** Schema-based isolation (COMMON, SPECIFIC, WORKSPACE schemas) combined with shared utilities repositories and standardized dbt Docker images.

#### Implementation Considerations

- Suited for larger organizations with multiple teams requiring deployment consistency
- May be overkill for small teams or exploratory work
- Key trade-offs: learning curve, debugging across abstraction layers, containerization overhead

**Critical success factors:** Infrastructure built on IaC or Declarative Data Stacks (Kubernetes, Terraform). Clear documentation and well-defined interfaces.

---

## Chapter 6: Data Engineering Design Patterns (DEDP)

### Overview

Data Engineering Design Patterns (DEDP) represent higher-level architectural solutions to common data engineering challenges. Unlike DEPs, these are conceptual frameworks rather than ready-to-implement code.

> *"A general repeatable solution to a commonly occurring problem in software design."*

DEDPs operate beyond typical industry hype cycles, providing sustainable guidance for navigating data engineering decisions and building robust, long-term data platforms.

### What DEDPs Provide

- Architecture blueprints and conceptual integration guidance
- Examples of similar implementations
- Best practices for specific problems
- Framework for long-term, sustainable data architecture

### Key Design Patterns

| Pattern | Description |
|---|---|
| **Dynamic Querying** | Ad-hoc query capability without reprocessing |
| **Stratified Data Flow Modeling** | Layered data flow design |
| **Open Data Platform (Lakehouse)** | Unified analytics and data science workloads |
| **Asset-based Governance** | Data products as discoverable, trusted resources |
| **Declarative Pipelines** | Intent-driven rather than implementation-driven pipeline definition |

---

### 6.1 Dynamic Querying

Enables ad-hoc analysis without requiring full pipeline re-runs. Addresses the fundamental need to ask databases questions and receive immediate answers through a systematic approach combining speed, flexibility, and ease of use.

#### Core Problem

Organizations struggle with three challenges when implementing ad-hoc query systems:

1. **Speed constraints** — Slow responses undermine the interactive nature of ad-hoc analysis, especially with AI-driven workflows
2. **Visualization complexity** — Raw numbers lack context; comparative analysis across dimensions reveals patterns
3. **Operational overhead** — Traditional ETL-based approaches require significant re-processing when business requirements change

Without proper patterns, organizations resort to data lakes where querying demands extensive JSON parsing and domain expertise.

#### Design Considerations

Competing demands to balance:

| Trade-off | Options |
|---|---|
| **Pre-computation vs. flexibility** | Pre-aggregations deliver speed but sacrifice adaptability; query-time computation offers flexibility at performance cost |
| **Freshness vs. performance** | More frequent updates = fresher data + higher infrastructure costs + slower queries |
| **Complexity vs. control** | Managed solutions simplify operations but increase expenses; open-source demands engineering investment |

#### Solution Architecture

Successful implementations require three capabilities:

1. **Analytical engine** supporting fast responses with database simplicity
2. **Logical data model** as an abstraction layer between technical implementation and users (facts and dimensions)
3. **Simple onboarding** for new data and measures without pipeline reprocessing

#### Universal Analytics API — Four Pillars

| Pillar | Description |
|---|---|
| **No-code interface** | Produces YAML/extended SQL artifacts enabling domain experts to define queries |
| **Reusable templates** | Variables and parameterization prevent duplication across consumers |
| **Logical data model** | Decouples dimensional definitions from physical storage, enabling query-time optimization |
| **Materialization and caching** | Pre-aggregation achieves sub-second performance with autonomous invalidation tied to model changes |

#### Implementation Steps

**Step 1: Choose OLAP Engine**
Options range from lightweight embedded systems (DuckDB) to enterprise solutions (ClickHouse, Druid). Selection depends on data scale, deployment complexity, and whether the tool includes a built-in metrics layer.

**Step 2: Define Metrics Layer Location**
Metrics should be stored centrally using structured formats (YAML + SQL conversion). Tools like Cube, dbt Semantic Layer, and Rill provide standardized definitions preventing inconsistency across analytical tools.

```yaml
type: metrics_view
model: data_source
dimensions:
  - name: category
measures:
  - name: total_revenue
    expression: SUM(revenue)
```

**Step 3: Select Semantic Layer**

| Use Case | Recommended Tools |
|---|---|
| Enterprise scale | Cube, LookML |
| dbt-native environments | dbt Semantic Layer |
| Simple trials | Boring Semantic Layer, DuckDB macros |
| AI agents | Rill (MCP support) |

#### Common Pitfalls

- **Premature complexity** — Starting with oversized systems attempting to solve all problems simultaneously
- **Custom caching** — Building proprietary caching when integrated solutions exist
- **Manual security** — Repeating authentication/authorization logic instead of leveraging semantic layer built-ins
- **Ignoring metrics testing** — Well-stewarded, tested metrics become differentiation factors for AI implementations

#### Real-World Implementations

**Netflix — DataJunction:**
Stores metrics as semantic graph nodes with dependency tracking. Single definitions consumable across dashboards, experimentation platforms, and ad-hoc tools. Reduced metric onboarding from weeks to near-trivial effort.

**Airbnb — Minerva:**
Manages 12,000+ metrics and 4,000+ dimensions in GitHub-based YAML. Dynamically generates SQL using split-apply-combine strategies. Exposes MySQL wire protocol enabling consumption through any SQL-compatible tool.

**Google — Dremel/BigQuery:**
Pioneered columnar OLAP with in-situ querying, eliminating ETL by analyzing data where it lives using parallel multi-level execution trees.

**Meta — Scuba:**
In-memory distributed database serving nearly one million queries daily at sub-second latency through unified web-based notebook interface.

#### Related Patterns

- **Stratified Data Flow Modeling** — Provides clean, stable query surfaces
- **Semantic Layer as MVC** — Mental model mapping to software engineering patterns

> The dynamic querying pattern ultimately seeks to achieve *database simplicity combined with cache-level speed* through systematic abstraction, standardization, and intelligent materialization strategies.

---

## Appendix

### Author

**Simon Späti** is a father and technical writer/data engineer with two decades of experience focused on knowledge sharing. He created ssp.sh, which ranks as the top Google result for Data Engineering content.

**Contributions:**
- **Data Engineering Vault** — a knowledge management system featuring interconnected resources and visualization tools
- **Public Second Brain** — continuously updated notes available at ssp.sh/brain/
- **Personal Knowledge Management Workflow** — detailed insights into his organizational approach

Simon is active on LinkedIn, Twitter, and GitHub, and offers a newsletter subscription for updates on new projects and insights.
