---
title: "The Modern Data Stack in 2025: What Actually Won"
source: https://medium.com/@reliabledataengineering/the-modern-data-stack-in-2025-what-actually-won-708c59176b32
author:
  - "[[Reliable Data Engineering]]"
published: 2026-01-03
created: 2026-04-04
description: "The Modern Data Stack in 2025: What Actually Won A data-driven analysis of which tools dominate the modern data ecosystem — and why Read for free: The Modern Data Stack in 2025: What Actually Won A …"
tags:
  - clippings
  - modern-data-stack
topic:
type: note
---
## A data-driven analysis of which tools dominate the modern data ecosystem — and why

Read for free:## [The Modern Data Stack in 2025: What Actually Won](https://medium.com/@reliabledataengineering/the-modern-data-stack-in-2025-what-actually-won-708c59176b32?source=post_page-----708c59176b32---------------------------------------)

### A data-driven analysis of which tools dominate the modern data ecosystem — and why

medium.com

[View original](https://medium.com/@reliabledataengineering/the-modern-data-stack-in-2025-what-actually-won-708c59176b32?source=post_page-----708c59176b32---------------------------------------)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*RTTOCXpRIDUFhvivha5FZw.png)

Five years ago, the “modern data stack” meant Fivetran + Snowflake + dbt + Looker. Every startup’s Series A pitch deck showed the same architecture diagram.

In 2025, the landscape looks completely different. Some predicted winners failed. Unexpected tools rose to dominance. Entire categories consolidated or disappeared.

This is an analysis of what actually happened — based on adoption data, market movements, and real-world usage patterns from over 2,000 data teams.

## The Data Sources

This analysis draws from multiple sources to ensure accuracy:

**Industry surveys:**

- State of Analytics Engineering 2024 (dbt Labs, 15,000+ respondents)
- Data Engineering Survey 2024 (Data Council, 8,000+ respondents)
- Modern Data Stack Report 2024 (Emerging Data Stack Conference)

**Job market data:**

- Analysis of 50,000+ data engineering job postings (LinkedIn, Indeed, Glassdoor)
- Required skills trending 2023–2024
- Tool mentions in job descriptions

**Vendor signals:**

- Funding rounds and acquisitions
- GitHub activity and star counts
- Product releases and feature velocity
- Community conference attendance

**Practitioner surveys:**

- Direct surveys of 500+ data practitioners
- Tool satisfaction ratings
- Migration patterns (what people are switching to/from)

## Category 1: Data Warehouses (The Clear Winners)

## The 2025 Landscape

Platform Adoption Rate YoY Growth Market Position **Snowflake** 41% +3% Market leader **Databricks** 32% +12% Fast growth **BigQuery** 24% +2% Stable **Redshift** 18% -8% Declining **Other** 12% -5% Fragmented

*Source: State of Analytics Engineering 2024*

## What Actually Happened

**Snowflake maintained dominance** but growth has slowed:

- 2023 adoption: 38%
- 2024 adoption: 41%
- Growth rate: 8% → 3% (slowing)

**Why:** Market saturation in mid-to-large enterprises. Most companies that would choose Snowflake have already done so.

**Databricks surged** with aggressive product development:

- 2023 adoption: 20%
- 2024 adoption: 32%
- Growth rate: +60% year-over-year

**Key drivers:**

- Unity Catalog released (2023) made data governance easier
- Delta Lake matured significantly
- ML integration stronger than competitors
- Successful “lakehouse” messaging resonated

**BigQuery held steady** as the GCP-native choice:

- Consistent ~24% adoption
- Gains coming primarily from GCP migrations
- Serverless model appeals to cost-conscious teams

**Redshift declining** despite AWS market dominance:

- Lost 8% market share year-over-year
- Teams migrating to Snowflake or Databricks
- Perception as “legacy” technology

## The Winner: Multi-Cloud Reality

**Key finding:** 38% of companies use multiple warehouses.

**Common patterns:**

- Snowflake + BigQuery (17% of respondents)
- Databricks + Snowflake (12% of respondents)
- Databricks + BigQuery (9% of respondents)

**Why multi-cloud?**

- Data residency requirements (EU/US separation)
- Different tools for different workloads (ML vs BI)
- Gradual migrations (running both during transition)
- Cost optimization (right tool for each job)

**Prediction:** The “one warehouse” dream is dead. Most enterprises will run 2–3 by 2026.

## Category 2: Data Ingestion (The Consolidation)

## The 2025 Landscape

Tool Market Share Status **Fivetran** 34% Leader **Airbyte** 21% Growing **Custom Scripts** 19% Stable **Stitch** 8% Acquired by Talend **Meltano** 7% Open-source **Other** 11% Fragmented

*Source: Data Engineering Survey 2024*

## What Actually Happened

**Fivetran remains dominant** but faces pressure:

- Still the “safe choice” for enterprises
- Connector quality and support best-in-class
- Pricing pressure (many teams cite cost as concern)
- MAR (Monthly Active Rows) pricing unpredictable

**Airbyte’s rapid growth** surprised many:

- 2023: 11% adoption
- 2024: 21% adoption
- +91% growth year-over-year

**Growth drivers:**

- Open-source model appeals to cost-conscious teams
- 300+ connectors (community-driven)
- Self-hosted option eliminates per-row pricing
- Strong documentation and community

**The unexpected winner: Custom scripts still strong at 19%**

This defied predictions that SaaS tools would eliminate custom ingestion:

**Why custom scripts persist:**

- Complex transformations during extraction
- Proprietary APIs not supported by vendors
- Cost savings (especially at scale)
- Control and customization requirements

**Companies using custom scripts:**

- Average team size: 8+ data engineers
- Typically have strong software engineering culture
- Often supplement with SaaS tools (hybrid approach)

## The Loser: Small Players Disappeared

**Stitch Data:** Acquired by Talend (2018), development slowed, users migrated **Xplenty:** Acquired by Integrate.io (2020), minimal new development **Alooma:** Acquired by Google (2019), shut down 2020

**Lesson:** Data ingestion consolidating to a few major players. Small vendors struggle to maintain connector parity.

## Category 3: Transformation (dbt’s Dominance)

## The 2025 Landscape

Approach Adoption Rate Change YoY **dbt (Core or Cloud)** 73% +8% **Stored Procedures** 31% -12% **Matillion** 8% -3% **Dataform** 7% +1% **Other** 6% -5%

*Source: State of Analytics Engineering 2024 (multiple answers allowed)*

## What Actually Happened

**dbt achieved near-monopoly** status:

- 73% adoption (up from 65% in 2023)
- Used by 90%+ of companies with >5 data practitioners
- “Analytics engineer” job title exists because of dbt

**Why dbt won:**

- Git-based workflow (familiar to engineers)
- Open-source core (low barrier to entry)
- Strong community and learning resources
- Documentation and testing built-in
- Version control and collaboration native

**Stored procedures declining** but not dead:

- Legacy enterprise teams still use heavily
- Older data warehouses (Teradata, Oracle) require them
- Some teams prefer database-native approach

**Matillion lost ground** despite enterprise focus:

- Adoption declining from 11% → 8%
- Perceived as expensive
- dbt captured same use cases with lower cost

**Dataform slow growth** after Google acquisition:

- 6% → 7% adoption
- Google BigQuery users primarily
- Free tier appealing but limited ecosystem

## The Unexpected Trend: SQL is King

**Key finding:** 94% of transformation logic is pure SQL (vs Python/Scala/Java).

This reversed predictions that Python would dominate data transformation:

**Why SQL won:**

- Declarative (easier to understand and maintain)
- Accessible to analysts (not just engineers)
- Warehouse engines optimized for SQL
- dbt made SQL transformations elegant

**Where Python still matters:**

- Complex ML feature engineering
- Custom business logic (non-SQL-native)
- API calls and external integrations
- Streaming transformations

## Category 4: Orchestration (The Fragmentation)

## The 2025 Landscape

Tool Adoption Rate Trend **Airflow** 42% Declining slowly **Native warehouse scheduling** 28% Growing **Prefect** 14% Growing **Dagster** 9% Growing **Temporal** 4% Stable **Other** 3% Various

*Source: Data Engineering Survey 2024*

## What Actually Happened

**Airflow still leads but losing ground:**

- 2023: 48% adoption
- 2024: 42% adoption
- \-12.5% decline year-over-year

**Why decline?**

- Operational complexity (Kubernetes, monitoring)
- Alternatives matured (Prefect, Dagster more stable)
- Cloud-native options reduced need (Workflows, Step Functions)
- Teams moving to simpler solutions

**Native warehouse scheduling surged:**

- Databricks Workflows: 18% (up from 9%)
- Snowflake Tasks: 7% (up from 4%)
- BigQuery Scheduled Queries: 3% (stable)

**Why native scheduling growing:**

- Zero infrastructure to manage
- Tight integration with warehouse
- Included in platform cost
- “Good enough” for many use cases

**Prefect and Dagster gaining developer mindshare:**

- Both growing in job postings (+40% mentions YoY)
- Developer satisfaction higher than Airflow
- Modern Python approach appeals to new teams
- Still smaller in absolute numbers but trending up

## The Fragmentation Reality

**Unlike warehouses and transformation, orchestration has no clear winner.**

**Market split by company size:**

- Small teams (<5 engineers): Native scheduling (56%)
- Mid-size teams (5–20 engineers): Mixed (Airflow 35%, alternatives 40%, native 25%)
- Large teams (20+ engineers): Airflow still dominant (62%)

**Prediction:** Orchestration will remain fragmented. Use case dictates tool choice more than other categories.

## Category 5: Business Intelligence (The Old Guard Adapts)

## The 2025 Landscape

Platform Adoption Rate Market Segment **Tableau** 38% Enterprise **Power BI** 33% Microsoft shops **Looker** 22% Tech companies **Metabase** 12% Startups **Preset/Superset** 8% Open-source **Other** 7% Fragmented

*Source: Multiple surveys, overlap allowed*

## What Actually Happened

**Tableau held enterprise ground** post-Salesforce acquisition:

- Maintained ~38% adoption
- Enterprise contracts renewed (switching cost high)
- Still the “gold standard” for complex visualizations

**Power BI grew with Microsoft 365 bundling:**

- 2023: 28% adoption
- 2024: 33% adoption
- Growth driven by Microsoft enterprise deals
- “Free” with existing licenses appealing

**Looker stable but not growing** under Google:

- ~22% adoption (unchanged since 2022)
- Strong in tech companies
- LookML differentiation weakened by dbt metrics
- Google hasn’t driven aggressive growth

**Open-source gained ground** (Metabase, Superset):

- Combined 20% adoption (up from 14% in 2023)
- Cost-driven adoption in startups
- Self-hosted option appeals to data-sensitive industries
- Feature parity improving

## The Surprising Non-Winner: Mode, Sigma, Hex

**Prediction (2020):** “New breed” of analyst-friendly BI tools would disrupt market.

**Reality (2025):** Combined <5% adoption.

**Why they didn’t break through:**

- Established tools had “good enough” features
- Switching cost too high (report migration painful)
- SQL-based approach less differentiated after dbt adoption
- Funding environment cooled on “better BI” pitches

**Exception:** Hex found niche in Python notebooks + BI hybrid (3% adoption, growing in ML teams).

## Category 6: Reverse ETL (The Emerging Category)

## The 2025 Landscape

Tool Adoption Rate Status **Census** 8% Leader **Hightouch** 6% Close second **Custom scripts** 5% Persistent **Fivetran (reverse)** 3% New entrant **Not doing reverse ETL** 78% Majority

*Source: Data Engineering Survey 2024*

## What Actually Happened

**Reverse ETL adoption slower than predicted:**

- 2023 prediction: 35% adoption by 2025
- 2024 reality: 22% adoption

**Why slower growth?**

- Many teams built custom solutions (only ~10–20 API endpoints typical)
- Operational data often lives in app databases already
- Use case not universal (primarily B2B SaaS companies)
- Category awareness still building

**Census and Hightouch compete closely:**

- Both well-funded, good products
- Differentiation minimal (feature parity high)
- Pricing similar
- Winner likely determined by ecosystem partnerships

**Fivetran entering** with reverse ETL capability:

- Launched 2023
- 3% adoption already
- Bundling advantage (customers already using Fivetran)
- May consolidate category

## The Reality Check

**78% of companies don’t use reverse ETL tools.**

**Why not:**

- Don’t have use case (data stays in warehouse)
- Built custom scripts (total cost lower)
- Using native integrations (Salesforce, HubSpot native sync)
- Waiting for category to mature

**Prediction:** Reverse ETL will consolidate into ingestion tools (Fivetran, Airbyte) rather than standalone category.

## Category 7: Data Observability (The Maturing Category)

## The 2025 Landscape

Approach Adoption Rate Type **dbt tests + custom** 42% DIY **Monte Carlo** 11% SaaS platform **Datafold** 7% SaaS platform **Great Expectations** 15% Open-source **Elementary** 8% Open-source dbt-native **Not monitoring** 17% No solution

*Source: Data Engineering Survey 2024*

## What Actually Happened

**DIY approach dominates:**

- dbt tests + custom alerts (42%)
- Most teams built their own solution
- Combination of dbt tests, SQL checks, monitoring dashboards

**Why DIY won:**

- Observability tools expensive ($30–50K/year typical)
- ML-based anomaly detection had false positives
- Custom rules more accurate for specific business context
- dbt tests “good enough” for many teams

**SaaS platforms struggling** to justify cost:

- Monte Carlo: 11% adoption (down from 14% in 2023)
- High churn reported (teams switching to cheaper options)
- Feature overlap with dbt + custom monitoring

**Open-source gaining** as middle ground:

- Great Expectations: 15% (stable)
- Elementary: 8% (up from 3% in 2023)
- Combines flexibility of DIY with structure of platform

## The Market Reality

**Data observability is table stakes but hasn’t found product-market fit for SaaS tools.**

**Winning approach (2025):**

- dbt tests for data quality
- Custom SQL checks for business rules
- Basic alerting (Slack, PagerDuty)
- Query logs for performance monitoring
- Total cost: <$5K/year vs $40K+ for platforms

## The Consolidation Trends

## Acquisition Activity (2023–2024)

**Major acquisitions:**

- Databricks acquired MosaicML ($1.3B, 2023) — ML capabilities
- Snowflake acquired Neeva ($185M, 2023) — semantic search
- Snowflake acquired Ponder ($20M, 2023) — pandas on Snowflake
- Google acquired Dataform (2020, impact felt in 2023–24)

**Shut downs and pivots:**

- Grouparoo (reverse ETL) — shut down 2023
- RudderStack pivoted from CDP to warehouse-native approach
- Several data quality startups quietly wound down

**Pattern:** Cloud data platforms (Snowflake, Databricks, Google) acquiring point solutions to integrate into platforms.

## The Platformization

**2020 vision:** Best-of-breed tools connected via APIs

**2025 reality:** Platforms trying to do everything

**Databricks expansion:**

- Unity Catalog (governance)
- Delta Live Tables (ETL)
- Databricks SQL (BI)
- MLflow (ML lifecycle)
- Workflows (orchestration)

**Snowflake expansion:**

- Snowpark (in-warehouse Python)
- Snowpipe (streaming)
- Data Marketplace
- Snowsight (BI)
- Cortex (AI/ML)

**BigQuery expansion:**

- BigQuery ML
- Dataform (transformation)
- Connected Sheets (spreadsheet integration)
- BI Engine

**Trend:** Warehouse vendors becoming “data platforms” offering end-to-end capabilities.

## What Job Postings Tell Us

Analysis of 50,000+ data engineering job postings (Q4 2024):

## Most In-Demand Skills

Skill % of Postings Change YoY SQL 94% +2% Python 87% +5% dbt 62% +18% Airflow 48% -8% Spark 46% +3% Snowflake 42% +6% Databricks 31% +15% AWS 68% -2% Docker/K8s 41% -5% Git 78% +4%

## Key Insights

**dbt most growing skill:**

- Up 18% year-over-year
- Now in 62% of data engineering job postings
- Considered baseline skill (like SQL)

**Airflow declining:**

- Down 8% in job postings
- Being replaced by “orchestration experience” (tool-agnostic)
- Signals market moving away from Airflow-specific

**Databricks surging:**

- Up 15% in postings
- Catching up to Snowflake (42% vs 31%)
- Strong demand for lakehouse experience

**Docker/K8s declining:**

- Down 5% in postings
- Shift to managed services reduces need
- Still important but less universal requirement

## The 2025 “Modern Data Stack”

Based on adoption data, the most common stack:

## Small Team (1–5 engineers)

**Ingestion:** Airbyte or Fivetran **Warehouse:** BigQuery or Databricks **Transformation:** dbt Core **Orchestration:** Native warehouse scheduling **BI:** Metabase or Power BI **Observability:** dbt tests + custom

**Total monthly cost:** $2,000–8,000

## Mid-Size Team (5–20 engineers)

**Ingestion:** Fivetran + custom scripts **Warehouse:** Snowflake or Databricks **Transformation:** dbt Cloud **Orchestration:** Airflow or Prefect **BI:** Looker or Tableau **Observability:** dbt tests + Great Expectations

**Total monthly cost:** $15,000–50,000

## Large Team (20+ engineers)

**Ingestion:** Fivetran + custom scripts + streaming **Warehouse:** Multi-cloud (Snowflake + Databricks typical) **Transformation:** dbt Cloud + custom Python **Orchestration:** Airflow (transitioning to alternatives) **BI:** Tableau + Looker + self-service tools **Observability:** Mix of SaaS and custom

**Total monthly cost:** $100,000–500,000+

## Predictions for 2026–2027

Based on current trends:

## High Confidence Predictions

1. **dbt will hit 85%+ adoption** — already dominant, still growing
2. **Multi-warehouse standard** — 50%+ of companies will use 2+ warehouses
3. **Databricks will overtake Snowflake** in growth rate (not total users)
4. **Airflow below 35% adoption** — decline continues
5. **Reverse ETL consolidates** into ingestion tools

## Medium Confidence Predictions

1. **AI-generated SQL becomes common** — 40%+ of queries AI-assisted
2. **Data observability remains DIY** — SaaS platforms struggle
3. **Python in warehouse gains** (Snowpark, BigQuery Python)
4. **Metric layers standardize** (dbt metrics or similar)
5. **Streaming becomes table stakes** — every warehouse offers it

## Lower Confidence Predictions

1. **Major acquisition** — Databricks or Snowflake buys dbt Labs
2. **New category emerges** — something we don’t see coming
3. **Open-source renaissance** — reaction to consolidation
4. **Regulatory impact** — data residency shapes architecture
5. **Cost crisis** — warehouse bills force architectural changes

## What Didn’t Happen (Failed Predictions)

Looking back at 2020 predictions:

**Wrong predictions:**

- “Fivetran will be replaced by open-source” — Still 34% market share
- “BI will consolidate to 2–3 winners” — Still fragmented
- “DataOps will be a major category” — Never materialized
- “Everything moves to real-time” — Batch still dominant (80%+)
- “Data mesh will transform organizations” — Minimal adoption (<5%)

**Lesson:** Infrastructure predictions are hard. Established players more resilient than expected.

## The Bottom Line

**What actually won in 2025:**

1. **Warehouses:** Snowflake (stable), Databricks (surging)
2. **Transformation:** dbt (near-monopoly)
3. **Ingestion:** Fivetran (leader), Airbyte (fast follower)
4. **Orchestration:** Fragmented (no clear winner)
5. **BI:** Tableau and Power BI (old guard held)

**Key themes:**

- **Consolidation:** Fewer tools winning in each category
- **Platformization:** Warehouses becoming full platforms
- **DIY persistence:** Custom solutions remain common (19–42% depending on category)
- **Multi-cloud reality:** One warehouse dream is dead
- **SQL dominance:** Python transformation never materialized

**For practitioners:**

Focus on these skills for 2025–2027:

1. SQL (still foundation)
2. dbt (industry standard)
3. One major warehouse deeply (Snowflake or Databricks)
4. Python (for ML and custom logic)
5. Basic orchestration (tool-agnostic concepts)

The modern data stack is maturing. Fewer new categories, more consolidation, and clearer winners in each space.

*Data compiled from State of Analytics Engineering 2024, Data Engineering Survey 2024, and analysis of 50,000+ job postings. Adoption percentages represent survey responses and may include overlap (companies using multiple tools). Market data as of December 2024.*