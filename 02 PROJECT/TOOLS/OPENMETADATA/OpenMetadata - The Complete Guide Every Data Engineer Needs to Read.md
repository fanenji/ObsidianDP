---
title: "OpenMetadata: The Complete Guide Every Data Engineer Needs to Read"
source: "https://medium.com/tech-with-abhishek/openmetadata-the-complete-guide-every-data-engineer-needs-to-read-b4bf3429b009"
author:
  - "[[Abhishek Kumar Gupta]]"
published: 2026-03-02
created: 2026-04-05
description: "OpenMetadata: The Complete Guide Every Data Engineer Needs to Read Most data teams have a metadata problem and don’t know it. Tables get created, pipelines get built, dashboards get shipped — and …"
tags:
  - "clippings"
topic:
type: "note"
---

Most data teams have a metadata problem and don’t know it.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*5k6DB-DY5duzrfVfkkyTvA.png)

OpenMetadata

**Tables get created, pipelines get built, dashboards get shipped — and three months later, nobody knows:**

- What does this column actually mean?
- Where does this number come from?
- Who owns this table?
- Is this data even trustworthy?

That’s not an engineering problem. That’s a **visibility problem**. And it gets worse every week as the data estate grows.

OpenMetadata is the open-source answer to that problem. Not just a data catalog, not just a lineage tool — an **all-in-one platform** for data discovery, observability, quality, governance, and collaboration.

***This article covers everything:*** *what it is, how it works, every major feature, how to set it up, and how to actually use it in real pipelines — from zero to production-ready.*

## What Is OpenMetadata, Really?

OpenMetadata is an **open-source metadata platform** built around a unified metadata model and an open API standard.

**That last part matters. Unlike many tools that are proprietary black boxes, OpenMetadata:**

- Stores everything in a standard, open schema
- Exposes a full REST API for every operation
- Provides a Python SDK so you can automate everything programmatically
- Supports 90+ connectors to databases, warehouses, lakes, BI tools, pipelines, and ML platforms

> Think of it as the **central nervous system** for your data ecosystem — it knows what data exists, what shape it’s in, where it came from, who owns it, and whether it’s trustworthy.

## What problem it actually solves

**Without OpenMetadata (or something like it):**

- Engineers spend hours hunting for the right table.
- Analysts trust data that’s broken.
- Governance is spreadsheets and Slack threads.
- Debugging pipelines means manual tracing through code.

**With OpenMetadata:**

- Every asset is discoverable in seconds.
- Lineage shows exactly what feeds what.
- Quality gates catch problems before they hit dashboards.
- Ownership and policies are enforced automatically.

## Architecture: How It All Fits Together

Before diving into features, it helps to understand what’s running under the hood.

### OpenMetadata has four main components:

### 1\. OpenMetadata Server

The core service. It exposes the REST API, stores metadata, handles search, and runs the UI. Everything else talks to this.

### 2\. Metadata Store

Built on MySQL (or compatible databases). Stores all entities — tables, pipelines, dashboards, users, tags, lineage — in a structured, versioned schema.

### 3\. Elasticsearch / OpenSearch

Powers search and discovery. When you search for a table name or filter by tag, it’s hitting Elasticsearch under the hood.

### 4\. Ingestion Framework

A Python-based framework that connects to your data sources and pulls metadata into the server. Runs as standalone scripts, Airflow DAGs, or scheduled jobs.

## Deployment options

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*0EC15fXC7ZoPhDmGlY5U7g.png)

## Getting Started: Docker Setup in Minutes

The fastest way to get OpenMetadata running locally:

```rb
# Download the docker-compose file
curl -sL https://github.com/open-metadata/OpenMetadata/releases/download/1.3.0-release/docker-compose.yml -o docker-compose.yml

# Start all services
docker compose up -d

# Check services are healthy
docker compose ps
```

Once running, open `http://localhost:8585` in your browser.

**Default credentials:**

```rb
Username: admin
Password: admin
```

**For Kubernetes/Helm in production:**

```rb
# Add Helm repo
helm repo add open-metadata https://helm.open-metadata.org
helm repo update

# Install dependencies (Airflow, MySQL, Elasticsearch)
helm install openmetadata-dependencies open-metadata/openmetadata-dependencies

# Install OpenMetadata
helm install openmetadata open-metadata/openmetadata
```

## Feature 1: Data Discovery

The most immediate value from OpenMetadata is **finding data fast**.

### The Unified Catalog

Every asset in your ecosystem — tables, views, dashboards, ML models, pipelines, topics — becomes searchable from one place.

**You can search and filter by:**

- Asset name, description, or column name
- Owner or team
- Tags and classifications
- Domain
- Tier (Gold, Silver, Bronze)
- Data quality status
- Recently updated

### Natural Language Search

You don’t need to remember exact table names. Type “orders last year” and OpenMetadata finds relevant assets using semantic search.

### Asset Pages

Every asset gets a rich page with:

- Full schema with column names, types, descriptions
- Owner and team
- Tags and classification
- Linked glossary terms
- Data quality status
- Lineage graph
- Activity feed and comments
- Sample data
- Profiling stats

### Tiers

OpenMetadata lets you tag datasets with **Data Tiers** — Gold, Silver, Bronze — to signal to consumers which assets are production-grade vs experimental.

```rb
Tier.Gold   → Production, well-tested, documented
Tier.Silver → Stable but less critical
Tier.Bronze → Experimental, use with caution
```

## Feature 2: Metadata Ingestion

None of the catalog features matter if metadata doesn’t flow in. OpenMetadata has **90+ connectors** and a flexible ingestion framework.

## How Ingestion Works

1. You define a **Service** (e.g., your Snowflake connection).
2. You configure an **Ingestion Pipeline** (what to extract: schema, profiling, lineage, usage).
3. OpenMetadata connects and pulls metadata on a schedule.

## Connector Categories

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*z9z0w184wt1JJyY6JeAZ-w.png)

### Example: Configuring Snowflake Ingestion via YAML

```rb
# snowflake-ingestion.yaml
source:
  type: snowflake
  serviceName: prod-snowflake
  serviceConnection:
    config:
      type: Snowflake
      username: "${SNOWFLAKE_USER}"
      password: "${SNOWFLAKE_PASSWORD}"
      account: "${SNOWFLAKE_ACCOUNT}"
      warehouse: COMPUTE_WH
      database: ANALYTICS
      role: ANALYST

  sourceConfig:
    config:
      type: DatabaseMetadata
      markDeletedTables: true
      includeTables: true
      includeViews: true
      schemaFilterPattern:
        includes:
          - "PUBLIC"
          - "ANALYTICS.*"

sink:
  type: metadata-rest
  config: {}

workflowConfig:
  openMetadataServerConfig:
    hostPort: http://localhost:8585/api
    authProvider: openmetadata
    securityConfig:
      jwtToken: "${OM_JWT_TOKEN}"
```

**Run it:**

```rb
metadata ingest -c snowflake-ingestion.yaml
```

### Python SDK: Programmatic Ingestion

```rb
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)

# Connect to OpenMetadata
server_config = OpenMetadataConnection(
    hostPort="http://localhost:8585/api",
    authProvider="openmetadata",
    securityConfig=OpenMetadataJWTClientConfig(
        jwtToken="your-jwt-token"
    ),
)
metadata = OpenMetadata(server_config)

# Search for a table
tables = metadata.list_entities(entity=Table)
for table in tables.entities:
    print(table.fullyQualifiedName)
```

## Feature 3: Data Lineage

Lineage is where OpenMetadata goes from “nice catalog” to “genuinely powerful platform.”

### What It Captures

- **Table-level lineage** — which tables feed which tables
- **Column-level lineage** — which column feeds which column, through SQL transformations
- **Cross-platform lineage** — from S3 → Spark → Snowflake → dbt → Tableau, in one graph

### How Lineage Gets Built

OpenMetadata builds lineage in three ways:

1. **Automated** — Connectors parse query logs, dbt manifests, and pipeline metadata.
2. **Manual** — You can draw lineage directly in the UI when automated capture isn’t possible.
3. **API** — Push lineage programmatically via the Python SDK.

### dbt Lineage Integration

If you use dbt, OpenMetadata can ingest your `manifest.json` and automatically build the full model-to-model lineage graph:

```rb
# dbt-ingestion.yaml
source:
  type: dbt
  serviceName: analytics-dbt
  serviceConnection:
    config:
      type: dbt
      dbtConfigSource:
        dbtManifestFilePath: /path/to/manifest.json
        dbtCatalogFilePath: /path/to/catalog.json
        dbtRunResultsFilePath: /path/to/run_results.json
  sourceConfig:
    config:
      type: DBTMetadata
      dbtUpdateDescriptions: true
      includeTags: true
```

> Run this and every dbt model, its sources, and its downstream dependencies appear as linked nodes in the lineage graph.

### Pushing Lineage via Python SDK

```rb
from metadata.generated.schema.type.entityLineage import EntitiesEdge
from metadata.generated.schema.api.lineage.addLineage import AddLineageRequest

# Get table entities
source_table = metadata.get_by_name(
    entity=Table,
    fqn="snowflake_service.analytics_db.public.raw_orders"
)
target_table = metadata.get_by_name(
    entity=Table,
    fqn="snowflake_service.analytics_db.public.fct_orders"
)

# Create lineage edge
lineage_request = AddLineageRequest(
    edge=EntitiesEdge(
        fromEntity=EntityReference(
            id=source_table.id,
            type="table"
        ),
        toEntity=EntityReference(
            id=target_table.id,
            type="table"
        ),
    )
)

metadata.add_lineage(lineage_request)
```

## What You See in the UI

**The lineage view gives you:**

- An **interactive graph** showing upstream and downstream dependencies.
- The ability to **expand nodes** to see multi-hop lineage.
- **Lineage layers** — you can toggle between data lineage, governance lineage, and observability views.
- **Impact analysis** — click any node and see what would break if it changed.
- **Root cause tracing** — when a dashboard shows wrong numbers, trace back to the broken source table.

## Feature 4: Data Quality

OpenMetadata has a built-in data quality testing engine — no Great Expectations setup required, though it supports that too.

## Two Types of Tests

**Table-level tests:**

- Row count is between N and M
- Row count equals a specific number
- A column exists
- Column names match a set
- No duplicate rows
- Table is fresh (data inserted within X hours)
- Compare two tables for differences

**Column-level tests:**

- Values not null
- Values unique
- Values between min and max
- Values in a predefined set
- String matches a regex pattern
- No duplicate values
- Mean, median, standard deviation within expected range
- Null proportion below threshold

## No-Code Test Setup

You don’t need to write YAML or code to create tests.

1. Navigate to any table.
2. Click the **Data Observability** tab.
3. Click **Add Test**.
4. Select table-level or column-level.
5. Pick the test type, fill in parameters, done.

## SQL-Based Custom Tests

When built-in tests aren’t enough, write your own:

```rb
-- Custom test: no orders should have negative amount
SELECT COUNT(*) as failed_rows
FROM orders
WHERE amount < 0
```

> If this returns anything > 0, the test fails.

## Test Suites

Group related tests into **Test Suites** so you can run all quality checks for a dataset together and get a consolidated pass/fail report.

## Quality as Part of Lineage

One of OpenMetadata’s most powerful features: quality test results propagate through the lineage graph.

If `raw_orders` fails a freshness test, OpenMetadata marks every downstream asset — `fct_orders`, `customer_ltv`, the Looker dashboard — as potentially affected. You see health signals on every node, not just the source.

## Feature 5: Data Governance

Governance in OpenMetadata isn’t a separate module — it’s woven into every part of the platform.

## Business Glossary

A Business Glossary lets you define the **official meaning of terms** across your organization.

Instead of every team having a different definition of “active user” or “revenue”, you define it once in the glossary, and every data asset can be linked to those official terms.

**Structure:**

**Glossary** (e.g., “Finance Terms”) → **Term** (e.g., “Net Revenue”) — > Definition, synonyms, related terms, linked assets, owners

When a table column is tagged with a glossary term, anyone viewing that column sees the authoritative definition instantly.

## Tags and Classification

Tags organize assets by any criteria:

- Business domain: `Finance`, `Marketing`, `Product`
- Sensitivity: `PII.Email`, `PII.Phone`, `Confidential`
- Status: `Deprecated`, `Draft`, `Certified`
- Custom: whatever your team needs

## Auto-Classification and PII Detection

OpenMetadata automatically scans column names and data samples to detect and tag PII:

- Columns named `email`, `ssn`, `phone_number` → auto-tagged `PII.Sensitive`
- Columns containing patterns matching credit card numbers → auto-tagged `PII.CreditCard`

**You can also configure auto-classification rules:**

```rb
{
  "name": "PII_Classification",
  "policyType": "Lifecycle",
  "rules": [
    {
      "name": "DetectEmail",
      "condition": "columnNameMatches('.*email.*')",
      "action": "addTag('PII.Email')"
    },
    {
      "name": "DetectSSN",
      "condition": "columnNameMatches('.*ssn.*|.*social_security.*')",
      "action": "addTag('PII.Sensitive')"
    }
  ]
}
```

## Roles and Policies (RBAC)

OpenMetadata has a full **Role-Based Access Control** system:

**Built-in Roles:**

- `Admin` — full access
- `Data Steward` — manage metadata, tags, quality
- `Data Consumer` — view and search
- `Data Engineer` — manage pipelines and lineage

**Custom Roles:**

```rb
{
  "name": "FinanceDataOwner",
  "policies": [
    {
      "name": "FinanceDataPolicy",
      "rules": [
        {
          "effect": "allow",
          "resources": ["table"],
          "operations": ["ViewAll", "EditDescription", "EditTags"],
          "condition": "inDomain('Finance')"
        }
      ]
    }
  ]
}
```

**Restricting PII Access:**

```rb
{
  "name": "SensitiveDataPolicy",
  "rules": [
    {
      "effect": "deny",
      "resources": ["table"],
      "operations": ["ViewAll"],
      "condition": "hasTag('PII.Sensitive') AND !hasRole('DataSteward')"
    }
  ]
}
```

**Require Documentation Before Publishing:**

```rb
{
  "name": "DocumentationPolicy",
  "rules": [
    {
      "effect": "deny",
      "operations": ["Publish"],
      "condition": "!hasDescription() OR !hasOwner()"
    }
  ]
}
```

## Ownership

Every asset can be assigned an owner — a user or team. Ownership is:

- Visible on every asset page
- Searchable and filterable
- Enforced in policies (“only owner can edit”)
- Used in impact alerts (“you own a table that was flagged for quality issues”)

## Feature 6: Data Observability and Alerting

Knowing something is wrong *after* your CEO spots it in a meeting is too late.

## Data Profiler

OpenMetadata’s built-in profiler computes and tracks metrics over time for every table:

- Row count (with historical trend)
- Null counts per column
- Unique value counts
- Min, max, mean, standard deviation
- Value distributions

> This gives you a **baseline** and lets you spot anomalies — sudden row count drops, unexpected nulls appearing, distributions shifting.

## Anomaly Detection

**OpenMetadata uses profiler history to automatically detect:**

- Unexpected row count changes
- Sudden increases in null values
- Schema drift (new or removed columns)
- Data freshness violations

## Alerts and Notifications

**You can configure alerts that fire when:**

- A test fails
- An asset is updated or deleted
- A quality metric crosses a threshold
- A pipeline fails

**Notifications go to:**

- Slack
- Teams
- Email
- Webhook (any system)

**Example alert config:**

```rb
# Alert: Slack notification on test failure
name: "Quality Alert"
alertType: Observability
filteringRules:
  resources:
    - "table"
  filters:
    - name: "TestResult"
      effect: include
      condition: "FAILED"
destinations:
  - type: Slack
    config:
      webhookUrl: "${SLACK_WEBHOOK_URL}"
```

## Incident Management

When data quality degrades, OpenMetadata tracks it as an **incident**:

- Incident created when test fails.
- Assigned to an owner.
- Status tracked: Open → In Progress → Resolved.
- Timeline of when issue appeared and was fixed.
- Linked to affected downstream assets.

> This closes the loop between “something broke” and “someone fixed it” with full audit trail.

## Feature 7: Collaboration

Data work is team work. OpenMetadata has collaboration features built into every asset.

## Descriptions and Documentation

Every asset, table, column, pipeline, and dashboard can have a rich Markdown description. This is the first place someone lands when they discover an asset.

## Activity Feeds

**Every change to every asset is tracked in an activity feed:**

- Column description updated by X
- Tag added by Y
- Test case created by Z
- Owner changed

> You see this at the asset level and in a global feed.

## Announcements

Data owners can post **announcements** on assets — deprecation notices, migration plans, temporary quality issues. Anyone watching the asset gets notified.

## Tasks and Conversations

**You can start a conversation on any asset or column, tag teammates, and create tasks:**

- “Please add description to this column”
- “Review and certify this table”
- “Investigate why this test is failing”

> Tasks track who needs to do what, creating accountability without leaving the platform.

## Following and Watching

Users can **follow** assets they care about and get notified when those assets change — similar to watching a GitHub repo.

## Feature 8: The Python SDK

The Python SDK is how you automate OpenMetadata programmatically.

**Install it:**

```rb
pip install openmetadata-ingestion
```

## Connect and Authenticate

```rb
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)

config = OpenMetadataConnection(
    hostPort="http://localhost:8585/api",
    authProvider="openmetadata",
    securityConfig=OpenMetadataJWTClientConfig(
        jwtToken="your-jwt-token"
    ),
)

metadata = OpenMetadata(config)
```

## Search and Retrieve Assets

```rb
from metadata.generated.schema.entity.data.table import Table

# Search by name
table = metadata.get_by_name(
    entity=Table,
    fqn="snowflake_service.analytics_db.public.orders"
)

print(table.name)
print(table.description)
print(table.owner)

# List all tables in a schema
tables = metadata.list_entities(entity=Table)
for t in tables.entities:
    print(t.fullyQualifiedName.__root__)
```

## Update Descriptions Programmatically

```rb
from metadata.generated.schema.type.basic import Markdown

# Update a table description
metadata.patch_description(
    entity=Table,
    source=table,
    description="This table contains all confirmed orders from the production system."
)
```

## Add Custom Tags via SDK

```rb
from metadata.generated.schema.type.tagLabel import TagLabel, TagSource, LabelType, State

tag_label = TagLabel(
    tagFQN="Classification.PII.Email",
    source=TagSource.Classification,
    labelType=LabelType.Automated,
    state=State.Confirmed
)

metadata.patch_tag(
    entity=Table,
    source=table,
    tag_label=tag_label
)
```

## Create a Database Service

```rb
from metadata.generated.schema.api.services.createDatabaseService import (
    CreateDatabaseServiceRequest,
)
from metadata.generated.schema.entity.services.databaseService import (
    DatabaseServiceType,
    DatabaseConnection,
)
from metadata.generated.schema.entity.services.connections.database.snowflakeConnection import (
    SnowflakeConnection,
)

create_service = CreateDatabaseServiceRequest(
    name="prod-snowflake",
    serviceType=DatabaseServiceType.Snowflake,
    connection=DatabaseConnection(
        config=SnowflakeConnection(
            username="data_engineer",
            password="secret",
            account="xy12345.snowflakecomputing.com",
            warehouse="COMPUTE_WH",
            database="ANALYTICS",
        )
    ),
)

service = metadata.create_or_update(create_service)
print(f"Service created: {service.fullyQualifiedName}")
```

## Feature 9: Domains and Data Products

Larger organizations need to organize assets by business domain.

## Domains

Domains map to business functions — Finance, Marketing, Product, Data Platform.

**Each domain has:**

- An owner (the domain steward)
- A collection of assets belonging to that domain
- Governance policies scoped to that domain

Assets get assigned to domains, making it easy to explore “all Finance tables” or “everything owned by the Product team.”

## Data Products

A **Data Product** is a curated, named, governed collection of assets that represents a business capability:

- `Customer 360` → all tables, pipelines, and dashboards related to customer data
- `Revenue Analytics` → tables and models that produce revenue metrics
- `Real-time Events` → Kafka topics and stream processing jobs

Data Products formalize the idea that data has producers and consumers, with clear ownership, contracts, and quality guarantees.

## Feature 10: Metadata Versioning

Every change to every asset is tracked and versioned.

**When someone updates a description, adds a tag, changes an owner, or adds a column, OpenMetadata:**

1. Creates a new version of the entity.
2. Records what changed, who changed it, and when.
3. Lets you view and diff any two versions.
4. Lets you restore a previous version if needed.

**This is invaluable for:**

- Auditing who changed what and when.
- Understanding why a dataset looks different from yesterday.
- Rollback when a mistake is made.

## Feature 11: AI-Powered Features (2025+)

OpenMetadata has been shipping AI capabilities that go beyond search.

## Semantic Search

Natural language queries against the catalog — “find customer tables updated this week” — return ranked, relevant results using vector embeddings rather than keyword matching.

## Auto-Description Generation

OpenMetadata can use AI to generate draft descriptions for tables and columns based on:

- Column names and types
- Sample data
- Existing documentation in similar assets

This dramatically reduces the documentation burden on engineers.

## Text-to-SQL

Ask a plain English question and OpenMetadata generates SQL to answer it against your connected warehouse — directly inside the platform.

**Example:**

> “What’s the total revenue from US customers in Q1 2025?”

OpenMetadata converts this to SQL, runs it (read-only), and returns the result inline.

## Feature 12: Data Insights and Reports

OpenMetadata tracks platform-level usage and health metrics so you can answer questions like:

- Which tables are most queried?
- What percentage of tables have descriptions?
- What percentage of tables have owners?
- Which datasets have the most open quality issues?
- How has data coverage improved over time?

**These insights help data platform teams:**

- Track adoption and engagement
- Prioritize documentation efforts
- Report on governance maturity

## Putting It All Together: A Real Workflow

Here’s what a realistic OpenMetadata-powered workflow looks like end to end:

### 1\. Day 1: Connect Your Sources

```rb
# Ingest Snowflake schema
metadata ingest -c snowflake-ingestion.yaml

# Ingest dbt lineage
metadata ingest -c dbt-ingestion.yaml

# Ingest Airflow pipeline metadata
metadata ingest -c airflow-ingestion.yaml
```

Now every table, column, and pipeline is in the catalog with lineage.

### 2\. Day 2: Set Up Quality Tests

Navigate to your most critical tables and add:

- Freshness tests (“data should arrive every day by 8 AM”)
- Row count tests (“orders table should have 10K–100K rows daily”)
- Column null checks (“order\_id should never be null”)
- Business rule tests (“amount should always be positive”)

### 3\. Day 3: Configure Governance

- Add owners to every Gold-tier table.
- Tag PII columns (or let auto-classification do it).
- Link columns to business glossary terms.
- Set up Slack alerts for quality failures.

### 4\. Week 2 Onwards: Operate

- Engineers search the catalog before building new pipelines.
- Analysts check column descriptions before trusting data.
- When a dashboard breaks, the lineage graph shows exactly what upstream table caused it.
- When a test fails at 6 AM, the owner gets a Slack alert with context before the business wakes up.

## Common Patterns Worth Knowing

### Pattern 1: Automate Metadata from Airflow

OpenMetadata integrates with Airflow to capture pipeline metadata automatically:

```rb
# In your Airflow DAG
from airflow_provider_openmetadata.hooks.openmetadata import OpenMetadataHookhook = OpenMetadataHook(openmetadata_conn_id="openmetadata_default")
metadata = hook.get_conn()# Lineage is captured automatically when DAGs run
```

### Pattern 2: Validate Before Loading

Run quality checks as a gate in your pipeline:

```rb
from metadata.ingestion.ometa.ometa_api import OpenMetadata

def validate_table_quality(fqn: str, min_rows: int):
    """Block pipeline if quality checks fail"""
    table = metadata.get_by_name(entity=Table, fqn=fqn)
    test_results = metadata.get_test_case_results(table.id)

    failed = [r for r in test_results if r.testCaseStatus == "Failed"]
    if failed:
        raise ValueError(f"Quality gate failed for {fqn}: {len(failed)} failed tests")

    print(f"Quality gate passed for {fqn}")

# Use in pipeline
validate_table_quality(
    fqn="snowflake.analytics.public.raw_orders",
    min_rows=1000
)
```

### Pattern 3: Track Schema Changes in CI/CD

Integrate OpenMetadata metadata checks into your CI pipeline:

```rb
# .github/workflows/data-quality.yml
- name: Check Schema Compatibility
  run: |
    python check_schema_changes.py \
      --table analytics.public.orders \
      --expected-columns order_id,user_id,amount,created_at
```

## What OpenMetadata Is Not

Knowing what it *doesn’t* do saves you from over-relying on it:

- **Not a query engine** — it doesn’t run compute on your data (except lightweight profiling).
- **Not a transformation tool** — it doesn’t replace dbt, Spark, or SQL.
- **Not an orchestrator** — it doesn’t schedule pipelines (though it integrates with tools that do).
- **Not a data warehouse** — it stores metadata, not the actual data.
- **Not a replacement for Great Expectations** — it integrates GX but isn’t a full testing framework replacement.

Use it to *know* about your data. Use everything else to *process* it.

## OpenMetadata vs Alternatives

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*K2Z9380aAJgVWQWFzQitAQ.png)

## Closing Thoughts

Metadata is the thing most data teams build last and wish they had built first.

Every painful “where does this number come from?” conversation, every broken dashboard no one can explain, every onboarding session where a new engineer spends a week reverse-engineering table structures — these are metadata problems.

OpenMetadata doesn’t magically fix all of those. But it gives you the **infrastructure to fix them once and maintain them forever**:

- Discovery so engineers find data in minutes, not hours.
- Lineage so impact analysis takes seconds, not days.
- Quality gates so broken data gets caught before it reaches the business.
- Governance so ownership, access, and compliance aren’t spreadsheets.
- Collaboration so knowledge stays in the platform, not in someone’s head.

If you’re a solo data engineer at a startup, start with the catalog and lineage — the ROI is immediate. If you’re at a scaling team, invest in quality tests and governance policies early; retrofitting them later is painful.

The data teams that are genuinely trustworthy to their business aren’t necessarily the ones with the best Spark clusters or the most sophisticated dbt models. They’re the ones who know what their data means, where it comes from, and whether it can be trusted.

**OpenMetadata is how you build that foundation.**

**👉** *I write about data engineering, platform design, and the practical side of making data teams run well. If you’re using OpenMetadata or evaluating it, I’d love to hear what your experience has been — drop it in the comments.*

[![Tech with Abhishek](https://miro.medium.com/v2/resize:fill:96:96/1*3DNIUqR0e-kHFWIXdq0REQ.png)](https://medium.com/tech-with-abhishek?source=post_page---post_publication_info--b4bf3429b009---------------------------------------)

[![Tech with Abhishek](https://miro.medium.com/v2/resize:fill:128:128/1*3DNIUqR0e-kHFWIXdq0REQ.png)](https://medium.com/tech-with-abhishek?source=post_page---post_publication_info--b4bf3429b009---------------------------------------)

[Last published Mar 29, 2026](https://medium.com/tech-with-abhishek/dbt-tips-that-senior-engineers-swear-by-but-rarely-document-af9978e535d4?source=post_page---post_publication_info--b4bf3429b009---------------------------------------)

Real-world AI, Cloud, and Data Engineering articles.

[![Abhishek Kumar Gupta](https://miro.medium.com/v2/resize:fill:96:96/1*EyqcUd4VgjYXp8UQ6vRNiA.jpeg)](https://medium.com/@abhishekkrgupta0?source=post_page---post_author_info--b4bf3429b009---------------------------------------)

[![Abhishek Kumar Gupta](https://miro.medium.com/v2/resize:fill:128:128/1*EyqcUd4VgjYXp8UQ6vRNiA.jpeg)](https://medium.com/@abhishekkrgupta0?source=post_page---post_author_info--b4bf3429b009---------------------------------------)

[86 following](https://medium.com/@abhishekkrgupta0/following?source=post_page---post_author_info--b4bf3429b009---------------------------------------)

I build smart data systems that think, act, and fix themselves. Writing real-world guides on GenAI, LLMs, observability, and everything in between.