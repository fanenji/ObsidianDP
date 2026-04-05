---
title: 10 Game-Changing dbt Tips I Wish I Knew Before My First Production Model
source: https://medium.com/tech-with-abhishek/https-medium-com-abhishekkrgupta0-10-dbt-production-tips-363f46b215f0
author:
  - "[[Abhishek Kumar Gupta]]"
published: 2025-05-25
created: 2026-04-04
description: Discover 10 expert tips for building production-ready dbt models. Avoid common pitfalls and scale your data engineering workflows with confidence.
tags:
  - clippings
  - dbt
topic:
type: note
---
## Lessons from production dbt workflows: contracts, tests, incremental logic, and model design.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*gzLs1iRxRHOCAHyYGsSjeQ.png)

> **Introduction:** When I started using dbt (data build tool) in production, I underestimated how much more there was to learn beyond the basics. From managing models to building maintainable workflows, there are tons of gotchas and best practices that make a real difference. In this article, I’ll share 10 battle-tested tips I learned the hard way while building production-grade pipelines using dbt with Snowflake.
> 
> Whether you’re just starting out or optimizing your current dbt setup, these tips will save you hours of debugging, improve model quality, and help you build with confidence.

1. **Follow the STG → INT → MART Pattern Religiously**  
	*Start with raw sources in the* `*staging (STG)*` *layer, do all transformations in the* `*intermediate (INT)*` *layer, and deliver outputs from the* `*mart (MART)*` *layer.*

**Why it matters:**

- Improves modularity and traceability
- Easier testing and debugging
- Enables reuse across marts
![STG → INT → MART model flow in dbt: A clean separation of source cleanup, transformation logic, and final reporting tables, with key fields like SYS_PK and LAST_PROCESSED_UTC tracked across layers.](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*BvrOjLpHNpqjUP6zjwK3aw.png)

STG → INT → MART model flow in dbt: A clean separation of source cleanup, transformation logic, and final reporting tables, with key fields like SYS\_PK and LAST\_PROCESSED\_UTC tracked across layers.

**2\. Use Contracts and Constraints to Prevent Bad Data Early**

*Add* `*contract.enforced: true*` *in your model config and define* `*data_types*`*,* `*not_null⁣ and*` `*unique*` *constraints in your YAML.*

```c
config:
  contract:
    enforced: true

columns:
  - name: id
    data_type: string
    constraints:
      - type: not_null
```

*To learn more about enforcing model contracts, check out the* [*dbt documentation on model contracts*](https://docs.getdbt.com/docs/mesh/govern/model-contracts)

**Why it matters:**

- Prevents silent data quality issues.
- Great for documenting assumptions explicitly.

**3\. Use Source Freshness Checks**  
*Define freshness parameters in your source YAML.*

```c
loaded_at_field: LAST_PROCESSED_UTC
freshness:
  warn_after: { count: 3, period: hour }
  error_after: { count: 6, period: hour }
```

**Why it matters:**

- Monitors stale source tables
- Helps trigger alerts for pipeline delays

**4\. Incremental Models are a Superpower (But Handle with Care)**

*Use* `*is_incremental()*` *logic in SQL:*

```c
where updated_at > (select max(updated_at) from {{ this }})
```

*For more details on configuring incremental models, refer to the* [*dbt documentation on incremental models*](https://docs.getdbt.com/docs/build/incremental-models)*.*

**Why it matters:**

- Saves compute on large tables
- But requires careful column tracking & deduplication
![How dbt leverages partitioned, incremental logic with tests and contracts to enforce quality at scale.](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*vp4XMFuLC_nWUVvruPsSZA.png)

How dbt leverages partitioned, incremental logic with tests and contracts to enforce quality at scale

**5\. Always Document Your Models (Even Briefly)**  
*Use model* `*.yml*` *files to add short descriptions, tags, and owners.*

```c
description: "Final sales mart for finance reporting"
meta:
  owner: abc.xyz@company.com
  tags: [finance, core]
```

**Why it matters:**

- Helps others (and future you!) understand model purpose quickly

**6\. Use Ref Macros & Avoid Hardcoding Dependencies**  
*Always use* `*{{ ref('model_name') }}*` *instead of full table names. Never do this:*

```c
from raw_data.sales  -- Bad
```

*Use:*

```c
from {{ ref('STG_RAW__SALES') }}  -- Good
```

**Why it matters:**

- Enables dependency tracking and DAG generation
- Ensures model ordering and build consistency

**7\. Version Control with Git + Branching is Non-Negotiable**  
*Use feature branches (*`*feature/abc*`*) and pull requests for every model change. Also use pre-commit hooks if possible.*

**Why it matters:**

- Prevents accidental overwrites
- Enables code review and testing

**8\. Write Tests for Critical Columns and Join Keys  
***Use built-in tests like:*

```c
- name: user_id
  tests:
    - not_null
    - unique
```

*Or write custom tests for conditions like negative values and foreign key mismatches.*

**Why it matters:**

- Catches edge cases and data bugs early

**9\. Use Tags to Organize and Deploy Selectively**  
*Add tags in YAML and use them in dbt commands:*

```c
meta:
  tags: [core, finance]

dbt run --select tag:finance
```

**Why it matters:**

- Enables partial builds and targeted runs
- Essential for large teams/projects

**10\. Use dbt Docs and Expose Them to Stakeholders**  
*Run:*

```c
dbt docs generate && dbt docs serve
```

*Host docs or use dbt Cloud to share lineage, descriptions, and tests with business users.*

**Why it matters:**

- Improves transparency
- Encourages business + engineering collaboration

**Conclusion:** dbt is powerful — but only if you use it with discipline. These 10 tips have helped me build scalable, production-grade data models that my team and business partners trust.

If you’re getting started or already building in dbt, I hope this guide gives you clarity and confidence.

👉 If you found this helpful, please 👏, comment, or follow me for more **production-ready dbt & data modelling tips**!

📖 **Ready to go deeper?** Check out the follow-up: [Beyond Basics: 7 Advanced dbt Patterns for Production-Grade Pipelines](https://medium.com/tech-with-abhishek/beyond-basics-7-advanced-dbt-patterns-for-production-grade-pipelines-6f4c3794700a)