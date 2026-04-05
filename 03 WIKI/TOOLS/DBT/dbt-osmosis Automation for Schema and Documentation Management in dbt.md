---
title: "dbt-osmosis: Automation for Schema and Documentation Management in dbt"
source: https://blog.devgenius.io/dbt-osmosis-automation-for-schema-and-documentation-management-in-dbt-70ecfec3442a
author:
  - "[[Sendoa Moronta]]"
published: 2025-09-21
created: 2026-04-04
description: Automate dbt schema YAMLs, sync docs with your warehouse, and enforce standards with dbt-osmosis. Boost productivity & governance at scale.
tags:
  - clippings
  - dbt
topic:
type: note
---
[Sitemap](https://blog.devgenius.io/sitemap/sitemap.xml)## [Dev Genius](https://blog.devgenius.io/?source=post_page---publication_nav-4e2c1156667e-70ecfec3442a---------------------------------------)

> *How dbt-osmosis automates schema management, enforces documentation standards and scales governance for modern analytics engineering teams.*

dbt has revolutionized how data teams design and maintain analytics pipelines. By borrowing practices from software engineering — modularity, testing, version control, and lineage — it has raised the bar for analytics engineering.

But there’s one part of the workflow that remains a persistent pain point: **schema YAMLs and documentation.**

- Who hasn’t seen a model with undocumented new columns?
- Who hasn’t fought through a PR cluttered with poorly formatted YAML changes?
- Who hasn’t faced an audit only to realize half the sources lacked descriptions?

This is where [**dbt-osmosis**](https://github.com/z3z1ma/dbt-osmosis) comes in: an open-source tool that automates schema and documentation management in dbt projects, freeing teams from repetitive chores while enforcing consistency at scale.

### What is dbt-osmosis?

Think of it as the governance and consistency engine for your dbt project. While dbt core focuses on **executing models, tests and docs**, dbt-osmosis handles:

- Keeping **YAML files in sync** with your warehouse reality.
- Automatically generating and updating **documentation stubs**.
- Enforcing **team conventions** in schema files.
- Integrating with **pre-commit hooks and CI/CD pipelines** to block inconsistent code.
- Providing a **workbench** to interactively test SQL/Jinja within dbt context.

In short: **automation + standardization + productivity.**

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*Fgsp4bEkQIKfLqm7)

### The Problem It Solves

Imagine a project with hundreds of models and dozens of sources. In theory:

- Every model should have a schema YAML with column descriptions.
- Every new column should be added there.
- Every dropped column should be removed.
- Everything should follow consistent conventions.

In practice:

- Developers forget to document new columns.
- Obsolete columns linger in YAML files.
- Documentation drifts away from reality.
- PRs are clogged with messy YAML diffs.

The result is invisible technical debt: documentation loses credibility, schema files become noise and teams stop relying on them.

dbt-osmosis directly attacks this problem: **it automates synchronization between the warehouse and the repo.**

## Schema Synchronization

With a single command:

```c
dbt-osmosis yaml refactor --project-dir .
```

dbt-osmosis will:

1. Inspect your actual models and sources.
2. Create or update YAML columns.
3. Remove columns that no longer exist.
4. Reorganize the file based on rules (alphabetical, team-defined ordering, etc.).

So when someone adds `device_type` to the `events` model, the YAML updates automatically. If that column later disappears, dbt-osmosis cleans it up.

## Example

Supose that we add a new column in a model:

```c
select
    id,
    created_at,
    status,
    json_extract_scalar(payload, '$.device') as device_type
from raw.events
```

With `dbt-osmosis` can run:

```c
dbt-osmosis yaml refactor --project-dir .
```

Results in `models/events.yml`:

```c
models:
  - name: events
    description: "Event-level data with enriched metadata"
    columns:
      - name: id
        description: "Unique identifier"
      - name: created_at
        description: "Timestamp of the event"
      - name: status
        description: "Lifecycle status of the event"
      - name: device_type
        description: "Device type extracted from payload"
```

Without manual intervention. And id `device_type` remove in the model, osmosis remove in the YAML.

## Documentation Generation

dbt-osmosis ensures no column goes undocumented by:

- Adding placeholder descriptions for new columns.
- Propagating descriptions from upstream sources (inheritance).
- Enforcing a uniform standard: every column is documented — even if minimally.

This flips the team’s mindset: documentation is no longer optional. Everything has a stub, and it’s obvious where richer descriptions are needed.

## Interactive Workbench

Another gem is the **workbench**:

```c
dbt-osmosis workbench
```

This opens an interactive environment where you can:

- Run SQL queries within your dbt project context.
- Use Jinja/macros without running a full `dbt run`.
- Debug faster, especially in large projects where full runs take minutes or hours.

## pre-commit Integration

dbt-osmosis integrates seamlessly into **pre-commit hooks** and CI pipelines.

Example `pre-commit` setup:

```c
repos:
  - repo: https://github.com/z3z1ma/dbt-osmosis
    rev: v0.15.0
    hooks:
      - id: dbt-osmosis-yaml
```

This ensures:

- Every commit validates and corrects YAML automatically.
- No PR introduces inconsistent schemas.
- Documentation quality becomes **a repo policy, not a best practice suggestion.**

## Comparison with IDE Plugins

```c
| Tool                                 | Strength                                                  | Limitation                         |
| ------------------------------------ | --------------------------------------------------------- | ---------------------------------- |
| **dbt VS Code Extension (official)** | IntelliSense, live error checking, refactoring of \`ref()\` | Doesn’t manage YAML or docs        |
| **dbt Power User (community)**       | Navigation, snippets, lineage, query execution            | Doesn’t enforce schema consistency |
| **dbt-osmosis**                      | Sync, auto-docs, CI/CD, workbench                         | Doesn’t provide IDE autocompletion |
```

dbt-osmosis isn’t competing — it’s filling the automation and governance gap left by IDE plugins.

## Common Use Cases

1. **Large teams**  
	Manual discipline doesn’t scale. dbt-osmosis guarantees order without endless PR reviews.
2. **Legacy or migration projects**  
	For repos with neglected documentation, dbt-osmosis can bootstrap consistent YAMLs in minutes.
3. **Governance and compliance**  
	Regulated industries (finance, healthcare) can enforce documentation standards automatically.
4. **Mature data cultures**  
	When documentation is expected to be a living, reliable asset, dbt-osmosis makes it achievable.

## Strategic Value

Most teams obsess over models, tests and macros, while neglecting documentation. Without credible documentation:

- Lineage is hard to trust.
- Analysts lose confidence in models.
- Knowledge gets trapped in tribal silos.

dbt-osmosis changes this by making documentation part of the code lifecycle, not a manual chore.

In my view, it’s the missing piece in the dbt ecosystem:

- **dbt core** → modeling & testing
- **IDE extensions** → developer productivity
- **dbt-osmosis** → governance & documentation automation

> 🙌 Found this helpful?
> 
> If you enjoyed the article or found it useful, feel free to give it a few claps, it helps more people discover it on Medium.
> 
> Also, feel free to share it with others who might benefit.
> 
> I’d love to hear your thoughts, any feedback, questions or suggestions are more than welcome in the comments!
> 
> Thanks for reading!

## Responses (3)

S Parodi

What are your thoughts?  

```c
Thanks for the introduction and informative overview of dbt-osmosis! Do you find this valuable in conjunction with dbt's contracts and versioning? Or do you find any issue with conflicting behaviors since they are both reviewing and validating the yaml files against model changes?
```

1

```c
Thanks for this insightful overview of dbt-osmosis! Automating schema and documentation management clearly addresses a real pain point in analytics engineering. I’m curious—how does dbt-osmosis handle conflicts when team members make simultaneous…more
```

1

```c
On that example you only bring the column name, but not the column type to the yaml. What would it need for inferring also field type?
```