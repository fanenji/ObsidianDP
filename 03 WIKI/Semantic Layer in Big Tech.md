---
title: "Secrets of the Semantic Layer in Big Tech: How Uber, Netflix, and Airbnb Manage Metrics"
source: "https://pub.towardsai.net/secrets-of-the-semantic-layer-in-big-tech-how-uber-netflix-and-airbnb-manage-metrics-1b9f7680ac25"
author:
  - "[[Sergey Gromov]]"
published: 2026-03-13
created: 2026-03-20
description: "Secrets of the Semantic Layer in Big Tech: How Uber, Netflix, and Airbnb Manage Metrics — and How You Can Apply It in Your Company Over the past few years, everyone in the data world has been …"
tags:
  - "clippings semantic-layer"
topic:
type: "note"
---

## How Uber, Netflix, and Airbnb Manage Metrics

We build Enterprise AI. We teach what we learn. Join 100K+ AI practitioners on Towards AI Academy. Free: 6-day Agentic AI Engineering Email Guide: [https://email-course.towardsai.net/](https://email-course.towardsai.net/)

Over the past few years, everyone in the data world has been talking about the semantic layer.

BI vendors sell it as a convenient metrics model. The modern data stack calls it the metrics layer. AI teams claim that without it, it’s impossible to build analytical agents.

But if you look closely at the architectures of major technology companies — Uber, Netflix, Airbnb, LinkedIn, Spotify — it becomes clear that they mean something very different from what is usually implied by the term *semantic layer*.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*ANaraf2NBmmJpQPfMXEvsw.png)

For them, it is not just a layer of metrics inside a BI tool.

It is a separate piece of infrastructure within the data platform.

A platform that manages the definitions of business metrics, their computation, data quality, access control, and how those metrics are used across BI, machine learning, products, and even AI systems.

What makes this especially interesting is that many of these companies have partially revealed their architectures in engineering blogs, research papers, and architecture talks. If you assemble these fragments together, a rather surprising picture emerges.

In this article, we will try to do exactly that.

We will collect publicly available evidence from Big Tech engineering materials and reconstruct what the real architecture of a semantic layer looks like.

We will examine how the metric platforms at Uber and LinkedIn work, why Netflix built Metrics Repo, how Airbnb designed Minerva, why Spotify placed an API in front of the data warehouse, and what role the semantic layer is beginning to play in artificial intelligence systems.

The result will be something like a map:  
how the semantic layer actually works in large technology companies, and which principles can be applied in more typical organizations.

And perhaps the most interesting conclusion may be somewhat unexpected:

in Big Tech, the semantic layer is not a BI feature at all — it is one of the key architectural layers of a modern data platform.

## 1\. Semantic Layer Architectures in Large Companies

## 1.1 Uber

***Metric Platform Architecture***

Uber built a centralized platform called **uMetric** that manages the entire lifecycle of metrics:

- definition
- discovery
- computation
- quality validation
- consumption

In practice, this is both a **semantic layer and a metric platform**.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*ck7oIbCglCOSGDUAerqsjA.png)

Uber publicly describes its internal uMetric platform as a unified metrics platform covering the full lifecycle of a metric: definition, discovery, planning, computation, quality, and consumption.

Moreover, Uber explicitly states that the platform extends metrics into **machine learning features**, meaning it is no longer just an analytics dictionary but a bridge between analytics and ML.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*YNZK9uM7x6PqQ_qSX1XWKg.png)

In 2025, Uber also described its conversational data agent **Finch**. It operates on curated single-table data marts and a semantic layer built on metadata. It uses metadata, aliases for columns and values stored in OpenSearch, allowing the LLM to generate more accurate WHERE filters and significantly reduce errors.

**Insight**

*At Uber, the semantic layer has effectively become a* ***control plane for machines****, not just for analysts.*

*The most valuable evidence here is that for their AI agent they did not rely on the idea that “the LLM will figure out the schema itself.” Instead, they rely on curated marts, metadata aliases, and governed access.*

*In other words, real enterprise AI built on top of data does not rely on raw SQL generation. It relies on a* ***pre-constructed semantic context****.*

**Core Idea of the System**

The main idea behind the system is to eliminate discrepancies between metrics calculated by different teams.

**Simplified Architecture**

\[Event streams\] → \[Data pipelines\] → \[Metric definitions\] → \[Metric computation engine\] → \[Quality validation\] → \[Metric API\] → \[Dashboards / ML / Apps\]

**Key Insight**

> Uber explicitly states that its metric system is used not only for analytics but also as an **ML feature platform**.
> 
> Which effectively means: **semantic layer = feature layer for ML**

## 1.2 Netflix

**Metrics Repo — Metrics as Code**

Netflix built a system called **Metrics Repo**, a framework for centralized metric definitions.

In describing its experimentation platform, Netflix explains that Metrics Repo is an internal Python framework where users define programmatically generated SQL queries and metric definitions. The system then centralizes these definitions.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*U-AsyhxW9qfDuhQksQCgxA.jpeg)

In a more recent overview of analytics engineering at Netflix, the company emphasizes that creating and using metrics internally is *“often more complex than it should be.”* In other words, even at Netflix’s level of maturity, the problem of inconsistent metric definitions has not completely disappeared.

There is another important signal as well. In a separate article on cloud efficiency, Netflix describes an **analytics data layer** that provides time-series efficiency analytics for financial engineering use cases.

**Insight**

*Netflix reveals something that is rarely discussed publicly:*

*in large companies, the semantic layer is often not a single universal system. Instead, it consists of* ***domain-specific metric repositories and analytical layers*** *for particular use cases — experimentation, efficiency analytics, creative analytics, and so on.*

*In other words, the real architecture is closer to* ***federated semantic governance*** *than to the idea of “one semantic layer to rule them all.”*

*This is not a direct quote — it is a conclusion drawn from how Netflix describes its various metric frameworks and domain-specific analytics layers.*

**Key Idea**

Metrics are defined **programmatically**, not inside a BI tool.

As a result, metric computation moves out of ETL pipelines and closer to analysts.

**Architecture**

\[Raw data\] → \[Data warehouse\] → \[Metrics Repo (definitions in code)\] → \[Experimentation platform\] → \[Statistics engine\] → \[Dashboards / decision systems\]

**Key Insight**

> Metrics Repo is used not only for BI, but primarily for:
> 
> **A/B testing, product experimentation, causal inference**
> 
> This is confirmed by Netflix’s research paper on its experimentation platform. In other words, the semantic layer at Netflix is part of a **scientific experimentation platform**.

## 1.3 LinkedIn

**Unified Metrics Platform**

LinkedIn built the **Unified Metrics Platform (UMP)**. The main problem it was designed to solve: different teams were calculating the same metrics in different ways.

To address this, LinkedIn centralized:

- metric definitions
- computation
- serving

**Architecture**

\[Raw events\] → \[Kafka\] → \[Batch + stream processing\] → \[Metrics computation\] → \[Metrics store\] → \[Metrics API\] → \[Dashboards / services\]

**Key Insight**

> LinkedIn turned the semantic layer into a **real service**. Not a SQL model. But a **metrics API**.

## 1.4 Spotify

**Semantic Layer Inside the Experimentation Platform**

Spotify built its own experimentation platform. Its architecture looks roughly like this:

\[Product events\] → \[Data lake\] → \[Metric definitions\] → \[Experimentation engine\] → \[Statistical analysis\] → \[Decision dashboards\]

**Core Principle**

> Metrics must be **reproducible**. In other words, every experiment must rely on the **same metric definitions**.

**1.5 Airbnb**

**Minerva — A Semantic Layer for the Entire Company**

Airbnb built a system called **Minerva**.

Airbnb explicitly states that Minerva plays a central role in its new data warehouse architecture. It ingests fact and dimension tables, denormalizes data, and serves it to downstream applications through APIs.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*17TXRr-Vcvk_al649WxjjA.jpeg)

They also revealed the scale of the system:

- more than **12,000 metrics**
- more than **4,000 dimensions**
- more than **200 data producers** across different company functions.

Metric and dimension definitions are stored in a **centralized GitHub repository** and go through code review, static validation, and test runs.

The system supports:

- quality checks, backfills, version control for definitions
- cost attribution, GDPR selective deletion, access control
- auto-deprecation policies, usage-based retention

Airbnb summarizes the goal very clearly: **“define once, use everywhere.”**

**Insight**

*The main “secret” is not in the formulas. It is that Airbnb’s semantic layer is* ***not a UI feature and not a BI capability*** *— it is an engineering discipline.*

*Metrics are treated as code.  
Metadata is mandatory.  
Review processes exist.  
Intermediate computations are reused.  
Deprecation and lifecycle management are formalized.*

*In other words, Minerva solves not only the problem of “how to compute a KPI”, but also the problem of “how to prevent business meaning from fragmenting across hundreds of teams.”*

*Airbnb explicitly explains that standardizing tables was not enough. Standardization had to happen* ***at the metric level****, because users consume metrics, dimensions, and reports — not tables.*

*Minerva manages:*

- *metrics*
- *dimensions*
- *KPI computation*

**Core Idea**

> **define once, use everywhere**

**Architecture**

\[Data warehouse\] → \[Semantic layer (Minerva)\] → \[Metrics computation\] → \[Metrics API\] → \[Analytics tools\]

Airbnb also notes that it extended its **Data Quality Score** to Minerva metrics and dimensions.

This is a crucial signal: a metric is not considered a complete object unless it has a **trust signal**.

**Insight**

*A true enterprise semantic layer almost always consists of three components:*

1. *a definition of meaning*
2. *a computation mechanism*
3. *a trust / quality signal*

*Without the third component, it is merely a dictionary of formulas rather than an enterprise-grade semantic layer. This conclusion is clearly supported by the combination of* ***Minerva + Data Quality Score*** *at Airbnb and the separate* ***quality pillar*** *in Uber’s uMetric platform.*

**1.6 Pinterest**

In a recent article on text-to-SQL, Pinterest explains that before interpreting a query they enrich the context with:

- table and column descriptions
- standardized glossary terms
- metric definitions
- data quality caveats
- recommended date ranges

They also explain that without this context an LLM only sees raw tables and columns and therefore loses the business meaning of the data.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*j5LLRRkIrZ9MV5MgXYTb-Q.png)

Pinterest further states that this context is maintained automatically through:

- AI-generated documentation
- join-based glossary propagation
- search-based semantic matching

**Insight**

*This provides very strong evidence of a new trend. In the AI era, the semantic layer is no longer just something like: Revenue = SUM(x)*

*It also includes:*

- *synonyms for fields*
- *data quality caveats*
- *acceptable date ranges*
- *valid join paths*

*These are exactly the elements that are often missing from traditional BI semantic layer products — even though they are critical for* ***text-to-SQL systems and agent-driven analytics****.*

## 2\. Big Tech Semantic Layer Matrix

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*7BtJGw9283wsHYNYNRuOtg.jpeg)

## 4\. What Is Really Happening (Intersection of Principles)

When these practices are combined, they form a unified architecture of the Big Tech semantic layer.

**\[Data sources\] → \[Data warehouse / lakehouse\] → \[Transformation layer\] → \[Metric definitions (Git)\] → \[Metric computation engine\] → \[Metrics catalog\] → \[Metrics API\] → \[BI / ML / applications / AI\]**

This represents a **complete enterprise-grade semantic layer architecture**.

In practice, reproducing this architecture inside a typical company is not trivial.

Most organizations already have:

· a data warehouse

· transformation tools

· BI dashboards

But they usually lack the **semantic modeling layer** that connects business meaning with the underlying data structures.

This is precisely where tools like [**DataForge**](https://dataforge.one/) become useful. Instead of embedding metric logic inside BI tools or SQL pipelines, [DataForge](https://dataforge.one/) allows teams to design a centralized semantic model of facts, dimensions, and business metrics — effectively acting as the architectural layer described throughout this article.

In other words, it helps implement the same principles used by companies like Uber, Airbnb, and LinkedIn — but in a form accessible to ordinary data teams.

## 5\. What Differentiates Typical Companies from Big Tech

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*KXjJXQD9h9igl8GARk2dkQ.jpeg)

## 6\. Big Tech Map: What Each Company Actually Built

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*nqtqpLwo6E6wC7QZ26MCzg.jpeg)

This matrix highlights a key observation:

Big Tech companies do not always explicitly use the term *semantic layer*. However, when they publish architecture details, the same components repeatedly appear:

- metric definitions
- centralized computation
- serving layer / APIs
- governance
- data quality
- catalogs
- reuse across tools

## 7\. The Evolution of the Semantic Layer: 2010 → 2026

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*bqVC-jE2_8F2l4qEslEIWg.png)

**Phase 1–2010–2014 / “Metrics Live in Reports and Pipelines”**

In the early stage, metrics were scattered across ETL pipelines, reporting tools, and individual teams. LinkedIn explicitly states that before UMP, reporting was **fragmented, siloed, and ad-hoc**, and different stakeholders calculated the same metrics differently. This strongly resembles the typical state of enterprise analytics environments in the early 2010s.

**Phase 2–2015–2019 / Standardization and Experimentation**

At this stage, companies began centralizing metrics primarily to support **A/B testing and reliable experimentation**. In 2019, Netflix introduced **Metrics Repo** as a unified way to define metrics and generate SQL programmatically. By that time, LinkedIn already had the **Unified Metrics Platform (UMP)** supporting both A/B testing and reporting. At this stage, the semantic layer emerged not from BI tooling but from the need to ensure **reproducibility and consistency**.

**Phase 3–2020–2022 / Metrics-as-Code and the Serving Layer**

Between 2020 and 2021, companies like Spotify, Uber, and Airbnb began openly presenting the next stage:

- metric definitions in code or Git
- centralized metric lifecycle management
- API or service layers
- governance
- quality validation

Spotify introduced an API in front of the warehouse. Uber developed the full-lifecycle uMetric platform. Airbnb published details about Minerva and the Minerva API. At this stage, the semantic layer stopped being just a BI model and became a **separate platform layer**.

**Phase 4–2023–2024 / Open Ecosystems and Composability**

In 2024, Google opened the Looker semantic layer to external tools through the **Open SQL Interface** and a growing connector ecosystem. During the same period, Meta published its work on **composable data management** and the challenge of inconsistent semantics across different systems. At this stage, the semantic layer began to be viewed as part of a broader **interoperability architecture**.

**Phase 5–2024–2026 / Semantic Layer as the AI Context Layer**

Between 2024 and 2025, Google explicitly connected the semantic layer to **Gemini, the Conversational Analytics API, and MCP**, stating that AI should query the semantic layer rather than generate raw SQL. Uber had already hinted at this earlier through the concept of **“metrics and ML features as a service.”.** At this stage, the semantic layer becomes more than an analytics abstraction.

It becomes a **governed context layer for AI agents**.

## 8\. “Intersection Map”: Which Secrets Are Shared by Everyone

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*5qTCZqp6nsTRpLOvADPnPg.jpeg)

## 11\. What Needs to Be Done to Reach the Top Level

The goal is not to **“buy a semantic layer”**, but to move through six maturity stages.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*eRlpIc0g48MAYNlrKjh7Sw.png)

**Level 1 — Stop the Chaos:** Critical KPIs must not live in Excel, BI-calculated fields, or ad-hoc SQL as the primary source of truth. LinkedIn and Uber explicitly show that the main reason for building their platforms was the duplication and inconsistency of metrics across teams.

**Level 2 — Define Once:** Move metric definitions into a centralized **specification / code layer**. This can be implemented using:

- [DataForge](https://dataforge.one/), YAML, DSL, dbt metadata, LookML-style modeling layers, an internal repository

This is exactly how Uber, Airbnb, Netflix, and Google manage metrics.

**Level 3 — Compute Once:** A metric must be computed **the same way everywhere**: dashboards, experimentation systems, ad-hoc analysis, applications. This pattern is clearly visible in LinkedIn’s **UMP**, Uber’s **uMetric**, and Spotify’s **Metrics Catalog**.

**Level 4 — Serve Everywhere:** It is not enough to maintain a repository of metric definitions. You also need a **serving layer**, such as:

- APIs, query layers, open SQL interfaces, semantic endpoints

This pattern appears clearly in the architectures of **Spotify, Airbnb, and Google**.

**Level 5 — Add Trust:** Without quality checks, validation, ownership, and review processes, a semantic layer cannot reach enterprise-grade maturity. Airbnb’s **Data Quality Score**, Uber’s **metric-level quality checks**, and Stripe’s **data quality platform** demonstrate that **trust is not optional — it is a fundamental component of a mature architecture**.

**Level 6 — Ground AI on It:** The next top-level step is to use the semantic layer as **context for AI and analytical agents**. Today, the clearest public example comes from Google through the integration of:

- Looker
- Gemini
- Conversational Analytics API
- MCP

## What Needs to Be Done to Move Toward the Big Tech Level

**Step 1**

Implement **metrics-as-code**

> Example: metric: revenue, definition: sum(order\_amount), dimension: country, owner: finance

**Step 2**

Create a Unified Metrics Catalog. The catalog should include:

- formulas
- descriptions
- owners
- lineage
- quality checks

**Step 3**

Centralize Metric Computation. A metric should be computed **once**.

Not: in BI tools, in SQL queries, in Excel

**Step 4**

Build a Metrics API. So that metrics can be used by:

- BI systems, notebooks, machine learning pipelines, applications

**Step 5**

Add Governance. Every metric should include:

- an owner, a description, validation tests

## 12\. The Honest Conclusion of This Article

So what is the most “secret” insight — even though it is publicly documented? The most underestimated conclusion is this:

> **leading technology companies do not build the semantic layer as a thin layer on top of BI.**

They build it as a **product for managing business meaning**, including:

- code
- reviews
- ownership
- lineage
- quality
- access control
- backfills
- deprecation policies
- APIs and agent consumption

This pattern can be observed simultaneously in the architectures of **Airbnb, Uber, Netflix, and Pinterest**. If you examine the architectures of **Uber, Netflix, LinkedIn, Airbnb, and Spotify**, one thing becomes clear:

- The semantic layer is **not a tool**.
- It is the **operating system of business metrics**.

And that is why Big Tech builds it as:

- a platform
- a service
- an API
- a governance layer

Big Tech does not build the semantic layer as a polished BI feature.

Big Tech builds the semantic layer as a **platform layer for definitions, computation, serving, trust, and now AI grounding**.

Not every company publicly exposes a single unified semantic layer.

But in every top-tier company, the **organs of that layer are visible**:

- catalogs
- metric definitions
- serving APIs
- quality layers
- semantic interoperability
- experimentation reuse

This is also the direction in which the data tooling ecosystem is evolving.

Instead of treating semantic layers as features inside BI tools, a [new category](https://dataforge.one/) of platforms is emerging that treats the semantic layer as a **first-class architectural component** of the data platform.

Most BI semantic layers are simply **data models**.

The semantic layer in Big Tech is **metrics infrastructure**.

Feel free to reach out to me on [LinkedIn](https://www.linkedin.com/in/gromovsergey/) if you want to discuss semantic layer architecture.

[![Towards AI](https://miro.medium.com/v2/resize:fill:96:96/1*JyIThO-cLjlChQLb6kSlVQ.png)](https://pub.towardsai.net/?source=post_page---post_publication_info--1b9f7680ac25---------------------------------------)

[![Towards AI](https://miro.medium.com/v2/resize:fill:128:128/1*JyIThO-cLjlChQLb6kSlVQ.png)](https://pub.towardsai.net/?source=post_page---post_publication_info--1b9f7680ac25---------------------------------------)

[Last published 7 hours ago](https://pub.towardsai.net/statistics-the-fundamentals-d3ecbaba6e81?source=post_page---post_publication_info--1b9f7680ac25---------------------------------------)

We build Enterprise AI. We teach what we learn. Join 100K+ AI practitioners on Towards AI Academy. Free: 6-day Agentic AI Engineering Email Guide: [https://email-course.towardsai.net/](https://email-course.towardsai.net/)

## Responses (2)

S Parodi

What are your thoughts?  

```c
Very good article. Need of metric layer is very clear but few question

How this is different from DataProduct, Is it not capturing metrics.. 

How AI or Agent can sit on top of this does not it need NLtosql
```

```c
Loved every bit of this article. Keep creating amazing content!
```

## More from Sergey Gromov and Towards AI

## Recommended from Medium

[

See more recommendations

](https://medium.com/?source=post_page---read_next_recirc--1b9f7680ac25---------------------------------------)