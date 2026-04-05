---
title: The Ultimate dbt Core Cheat Sheet
source: https://towardsdev.com/the-ultimate-dbt-core-cheat-sheet-9a8bb7b99eb6
author:
  - "[[Mihir Samant]]"
published: 2025-08-04
created: 2026-04-04
description: 🚀The Ultimate dbt Core Cheat Sheet 🚀 What is dbt Core? I’ve been working with dbt Core for a while now, and it’s honestly changed how I think about data transformations. dbt (data build …
tags:
  - clippings
  - dbt
topic:
type: note
---
[Sitemap](https://towardsdev.com/sitemap/sitemap.xml)## [Towards Dev](https://towardsdev.com/?source=post_page---publication_nav-a648dc4ecb66-9a8bb7b99eb6---------------------------------------)

[![Towards Dev](https://miro.medium.com/v2/resize:fill:76:76/1*c2OaLMtxURd1SJZOGHALWA.png)](https://towardsdev.com/?source=post_page---post_publication_sidebar-a648dc4ecb66-9a8bb7b99eb6---------------------------------------)

A publication for sharing projects, ideas, codes, and new theories.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*aiGHy4VCLVWIzOYRBe3Kkw.jpeg)

## What is dbt Core?

I’ve been working with dbt Core for a while now, and it’s honestly changed how I think about data transformations. dbt (data build tool) is this brilliant open-source tool that lets you write modular SQL and manage your data transformations like actual software. Instead of writing messy, one-off scripts, you get to version control your analytics code, test your data, and build reliable pipelines. It compiles your SQL and runs it against your warehouse, turning raw data into something analysts can actually use. If you’re tired of spaghetti SQL and broken data pipelines, dbt is your new best friend.

## Core Concepts You Need to Know

**Models** — These are just SQL files that create tables or views. Think of them as your data transformations.

**Sources** — The raw tables you’re reading from (but not creating). Your starting point.

**Seeds** — CSV files you can load directly into your warehouse. Great for lookup tables.

**Snapshots** — How you track changes in data over time. SCD Type 2 made easy.

**Macros** — Reusable chunks of SQL. Like functions, but for SQL.

**Tests** — Your data quality checks. Because nobody likes bad data.

## Getting Started

## Project Setup

```c
# Start fresh
dbt init my_project

cd my_project # Connect to your warehouse

dbt debug  # Check your connection
```

## Your dbt\_project.yml (The Heart of Everything)

```c
name: 'my_analytics'
version: '1.0.0'
config-version: 2

# Where stuff lives
model-paths: ["models"]
test-paths: ["tests"]
seed-paths: ["data"]
macro-paths: ["macros"]

# Build settings
target-path: "target"
clean-targets: ["target", "dbt_packages"]
# Model configurations
models:
  my_analytics:
    staging:
      +materialized: view
    marts:
      +materialized: table
      +schema: analytics
```

## Essential Commands

## Development Workflow

```c
# The big three you'll use constantly
dbt run          # Build all models
dbt test         # Run all tests
dbt build        # Run + test everything (my favorite)

# More specific stuff
dbt run --select model_name              # Just one model
dbt run --select +model_name             # Model + upstream
dbt run --select model_name+             # Model + downstream
dbt run --select @model_name             # Model + both directions

# Target specific things
dbt run --select tag:daily               # Models with 'daily' tag
dbt run --select models/staging          # Everything in staging folder
dbt run --exclude tag:slow               # Skip the slow stuff
```

## Development Tricks

```c
# Check what will run without running it
dbt run --dry-run

# Full refresh (rebuilds from scratch)
dbt run --full-refresh
# Run failed models only
dbt retry
# Compile but don't run (great for debugging)
dbt compile
```

## Testing & Quality

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*8uETnLsEOeg9nuFjWinkJw.gif)

```c
# Test everything
dbt test

# Test one model
dbt test --select model_name

# Test sources
dbt test --select source:*

# Just data tests
dbt test --exclude test_type:schema
```

## Model Organization Patterns

## Folder Structure That Actually Works

```c
models/
├── staging/          # Raw data cleanup
│   ├── _sources.yml
│   └── stg_customers.sql
├── intermediate/     # Business logic
│   └── int_customer_orders.sql
└── marts/           # Final output
    ├── core/
    │   └── dim_customers.sql
    └── finance/
        └── fct_revenue.sql
```

## Naming Conventions I Swear By

- **Sources**: Keep original names
- **Staging**: `stg_{source}_{table}`
- **Intermediate**: `int_{business_concept}`
- **Facts**: `fct_{business_process}`
- **Dimensions**: `dim_{business_entity}`

## SQL Patterns & Best Practices

## The CTEs Pattern Everyone Should Use

```c
-- models/marts/fct_orders.sql
with

orders as (
    select * from {{ ref('stg_orders') }}
),
customers as (
    select * from {{ ref('dim_customers') }}
),
final as (
    select
        orders.order_id,
        orders.customer_id,
        customers.customer_name,
        orders.order_date,
        orders.total_amount
    from orders
    left join customers using (customer_id)
)
select * from final
```

## Staging Model Template

```c
-- models/staging/stg_customers.sql
with

source as (
    select * from {{ source('raw_data', 'customers') }}
),
renamed as (
    select
        id as customer_id,
        first_name,
        last_name,
        email,
        created_at,
        updated_at
    from source
)
select * from renamed
```

## Configuration Magic

## Model-Level Config

```c
-- At the top of your model
{{ config(
    materialized='table',
    indexes=[
      {'columns': ['customer_id'], 'type': 'btree'},
    ],
    pre_hook="alter table {{ this }} add constraint pk_customer primary key (customer_id)",
    post_hook="grant select on {{ this }} to role analytics_users"
) }}
```

## Schema.yml for Documentation & Tests

```c
models:
  - name: dim_customers
    description: "Customer dimension table"
    columns:
      - name: customer_id
        description: "Primary key"
        tests:
          - unique
          - not_null
      - name: email
        description: "Customer email"
        tests:
          - unique
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: email
```

## Testing Strategies

## Built-in Tests (The Basics)

```c
tests:
  - unique
  - not_null
  - accepted_values:
      values: ['pending', 'shipped', 'delivered']
  - relationships:
      to: ref('dim_customers')
      field: customer_id
```

## Custom Tests (tests/generic/)

```c
-- tests/generic/test_valid_email.sql
{% test valid_email(model, column_name) %}
    select {{ column_name }}
    from {{ model }}
    where {{ column_name }} not like '%@%.%'
{% endtest %}
```

## Singular Tests (tests/)

```c
-- tests/assert_positive_revenue.sql
select *
from {{ ref('fct_revenue') }}
where revenue < 0
```

## Macros That’ll Save Your Life

## Date Macros

```c
-- macros/date_helpers.sql
{% macro date_spine(start_date, end_date) %}
    select 
        date_day
    from (
        {{ dbt_utils.date_spine(
            datepart="day",
            start_date="'" ~ start_date ~ "'",
            end_date="'" ~ end_date ~ "'"
        ) }}
    )
{% endmacro %}
```

## Environment-Specific Logic

```c
-- Different behavior in prod vs dev
select *
from my_huge_table
{% if target.name == 'prod' %}
where created_at >= current_date - 365
{% else %}
where created_at >= current_date - 7  -- Just last week in dev
{% endif %}
```

## Sources & Seeds

## Sources Configuration

```c
# models/staging/_sources.yml
sources:
  - name: raw_data
    description: "Raw application data"
    tables:
      - name: customers
        description: "Customer data from app DB"
        freshness:
          warn_after: {count: 24, period: hour}
          error_after: {count: 48, period: hour}
        columns:
          - name: id
            tests:
              - unique
              - not_null
```

## Working with Seeds

```c
# Load CSV files
dbt seed

# Specific seed
dbt seed --select seed_name

# Full refresh seeds
dbt seed --full-refresh
```

## Environment Management

## profiles.yml Setup

```c
my_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: your_account
      user: your_username
      password: your_password
      role: developer
      database: DEV_DB
      warehouse: DEV_WH
      schema: your_schema
    prod:
      type: snowflake
      account: your_account
      user: service_account
      password: "{{ env_var('DBT_PASSWORD') }}"
      role: transformer
      database: PROD_DB
      warehouse: PROD_WH
      schema: analytics
```

## Environment Variables

```c
# Set in your shell or CI/CD
export DBT_PASSWORD="super_secret_password"
export DBT_PROFILES_DIR="/path/to/profiles"

# Use in dbt
password: "{{ env_var('DBT_PASSWORD') }}"
```

## Performance Tips That Actually Work

## Incremental Models

```c
{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}

select * from {{ source('raw', 'orders') }}
{% if is_incremental() %}
    where updated_at >= (select max(updated_at) from {{ this }})
{% endif %}
```

## Optimization Strategies

- Use views for staging, tables for marts
- Incremental models for large, append-only data
- Snapshots for tracking changes
- Proper indexing in post-hooks
- Partition large tables by date

## Debugging & Troubleshooting

## Common Issues & Solutions

```c
# Check compiled SQL
dbt compile --select model_name
# Look in target/compiled/

# Debug connection issues
dbt debug

# Check dependencies
dbt deps

# Clean everything
dbt clean
```

## Logging & Visibility

```c
-- Add logging to your models
{{ log("Processing " ~ this ~ " at " ~ run_started_at, info=true) }}

-- Check row counts
{% set row_count %}
    select count(*) from {{ ref('my_model') }}
{% endset %}
{{ log("Row count: " ~ row_count, info=true) }}
```

## Documentation & Maintenance

## Generate Docs

```c
dbt docs generate
dbt docs serve  # Opens browser
```

## Version Control Best Practices

- Use meaningful commit messages
- Branch for features
- Review SQL changes carefully
- Tag releases
- Document breaking changes

## Pro Tips

1. **Start Small**: Begin with staging models, then build up
2. **Test Early**: Write tests as you go, not after
3. **Use refs()**: Never hardcode table names
4. **Modular Thinking**: Each model should do one thing well
5. **Document Everything**: Future you will thank you
6. **Monitor Performance**: Use `dbt compile` to check generated SQL
7. **Environment Parity**: Keep dev/prod configs similar
8. **Incremental Strategy**: Don’t rebuild everything every time

Remember, dbt is just SQL with superpowers or SQL on Steroids. Start with what you know and gradually add complexity. The magic happens when you embrace the patterns and let dbt handle the heavy lifting.

[![Towards Dev](https://miro.medium.com/v2/resize:fill:96:96/1*c2OaLMtxURd1SJZOGHALWA.png)](https://towardsdev.com/?source=post_page---post_publication_info--9a8bb7b99eb6---------------------------------------)

[![Towards Dev](https://miro.medium.com/v2/resize:fill:128:128/1*c2OaLMtxURd1SJZOGHALWA.png)](https://towardsdev.com/?source=post_page---post_publication_info--9a8bb7b99eb6---------------------------------------)

[Last published 13 hours ago](https://towardsdev.com/salesforce-cdp-snowflake-connection-solved-private-link-bfbfa9a4e62a?source=post_page---post_publication_info--9a8bb7b99eb6---------------------------------------)

A publication for sharing projects, ideas, codes, and new theories.

## Responses (1)

S Parodi

What are your thoughts?  

```c
Please add information about vars.
```