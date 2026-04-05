---
title: "Metadata-Driven Data Architecture: Leveraging draw.io and VSCode for Scalable Design"
source: https://medium.com/towards-data-engineering/metadata-driven-data-architecture-leveraging-draw-io-and-vscode-for-scalable-design-a785e96b0e4e
author:
  - "[[Jaco van der Laan]]"
published: 2025-09-17
created: 2026-04-04
description: "Metadata-Driven Data Architecture: Leveraging draw.io and VSCode for Scalable Design A practical workflow that connects draw.io, DuckDB, and VSCode to automate the creation and validation of data …"
tags:
  - clippings
  - architecture
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)## [Towards Data Engineering](https://medium.com/towards-data-engineering?source=post_page---publication_nav-37f58dd42be7-a785e96b0e4e---------------------------------------)

[![Towards Data Engineering](https://miro.medium.com/v2/resize:fill:76:76/1*oY6pUgtb7NF-tG2sxtTQyQ.png)](https://medium.com/towards-data-engineering?source=post_page---post_publication_sidebar-37f58dd42be7-a785e96b0e4e---------------------------------------)

Dive into data engineering with top Medium articles on big data, cloud, automation, and DevOps. Follow us for curated insights and contribute your expertise. Join our thriving community of professionals and enthusiasts shaping the future of data-driven solutions.

*A practical workflow that connects draw.io, DuckDB, and VSCode to automate the creation and validation of data models and mappings — ready for both engineers and business users.*

*💡 Not a Medium member? You can read this article for free using this* [*friend link*](https://medium.com/towards-data-engineering/metadata-driven-data-architecture-leveraging-draw-io-and-vscode-for-scalable-design-a785e96b0e4e?sk=a9dd52f59fcd795e3ef95ea34928423c)*.*

## Summary

> ✅ Use code (YAML/JSON) as the single source of truth  
> 🔄 Generate consistent draw.io diagrams from metadata  
> 🔍 Parse diagrams back into metadata when needed  
> ⚙️ Maintain and validate mappings in VSCode  
> 📤 Automatically publish diagrams to Confluence
> 
> 💡 Designed for teams that want visual clarity with code-based control

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*V-S8yyxN65HOWhFd)

## Part 1: Why Metadata-Driven Design Needs Visual & Text-Based Harmony

In a modern data architecture, metadata is the glue that connects business understanding to technical implementation. However, visualizing and managing this metadata at scale remains a challenge.

This series proposes a robust, scriptable workflow combining **draw.io** and **Visual Studio Code (VSCode)** to deliver clear, version-controlled, and business-friendly data models.

Our goal: **use diagrams as a view, not as the source of truth.** All diagrams are generated from metadata and can be parsed back to metadata when necessary.

## Part 2: Generating draw.io Diagrams from Metadata

We automatically generate draw.io diagrams (ERDs and Mapping Diagrams) using metadata stored in **DuckDB**. These diagrams:

- Reflect relationships, transformations, and logical data flow
- Are organized as separate `.drawio` files or pages within a multi-page file
- Are consistent in layout, styling, and component naming

Using Python scripts, we read metadata (e.g., relationships, transformations) and create draw.io XML structures, saving them as `.drawio` files.

## Part 3: Parsing draw.io Back into Metadata

Our workflow allows diagrams to be parsed back into structured metadata:

- Extract nodes, labels, positions, and relationships from the `.drawio` XML
- Update DuckDB metadata tables with business-friendly annotations
- Track changes or enrich existing mappings

Although not the primary update mechanism, this feature is useful for:

- Early conceptual design sessions
- Business stakeholder input
- Diagram reverse engineering

## Part 4: Organizing Diagrams and Code in VSCode

We use the [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) plugin for VSCode to:

- Visually open and edit `.drawio` diagrams
- Organize diagrams alongside mapping files
- Enable clickable navigation: from diagram components to YAML/JSON or SQL files

All components are stored in a Git repository, allowing version control, collaboration, and pull request reviews.

Example file structure:

```c
/data-models
  /mappings
    orders_to_dwh.yaml
  /diagrams
    orders_mapping.drawio
  /sql
    orders_to_dwh.sql
```

## Part 5: Maintaining Mappings in Code, Not in Diagrams

We strongly prefer maintaining mappings in structured text formats:

- **YAML or JSON** files define the data flow, transformations, filters, joins
- These are validated using **schemas**, **VSCode extensions**, or **custom Python scripts**
- GitHub Copilot can assist in authoring these files

Benefits:

- Easier diffs, reviews, and traceability
- Fully scriptable and testable
- Enables code-driven diagram generation

## Tools and Extensions:

- YAML Language Server
- JSON Schema validator
- GitHub Copilot
- Custom linters/validators

## Part 6: Automated Diagram Generation Pipeline

```c
YAML Mapping → Metadata DB → Python Script → draw.io XML → .drawio File
```

By maintaining a code-first approach, we ensure:

- Consistent layout and style across diagrams
- Reusable diagram components (functions, filters, joins)
- Easy regeneration after metadata updates

Scripts also handle component positioning, grouping, and color coding.

## Part 7: Publishing to Confluence

Draw.io files can be exported as SVG/PNG and embedded into Confluence pages:

- Python or CI pipelines can automate export
- Markdown or HTML descriptions accompany diagrams
- Business users get accessible, versioned views of metadata and mappings

This bridges the gap between technical metadata and business communication.

## Summary Workflow Diagram

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*Y-Xhj-wLTaX3f2kB)

## Next Steps

In future articles, we’ll provide:

- Sample Python scripts for draw.io generation and parsing
- YAML schema examples for mappings
- VSCode setup and plugin configuration
- Real-world use cases and templates for re-use

> *Let diagrams be a* ***view*** *of the system — not the bottleneck in your metadata lifecycle.*

✍️ **Written by Jaco van der Laan**  
Lead Data Modeler & Data Solution Architect — specializing in model-driven data engineering, enterprise data platforms, and high-governance environments in financial services.

⭐ Follow me on Medium → Jaco van der Laan on Medium  
🌐 Visit my website → [www.jacovanderlaan.com](https://www.jacovanderlaan.com/)  
🔗 Connect on LinkedIn → [linkedin.com/in/jacovanderlaan](https://www.linkedin.com/in/jacovanderlaan)

🧭 **Explore my publications:**  
[Model-Driven Data Architecture](https://medium.com/model-driven-data-architecture) | [Model-Driven Data Engineering](https://medium.com/model-driven-data-engineering) | [Model-Driven Data Deliver](https://medium.com/model-driven-data-delivery) y | [Business-Friendly Data Modeling](https://medium.com/business-friendly-data-modeling) | [Business-Friendly Data Mapping](https://medium.com/business-friendly-data-mapping) | [Business-Friendly Metadata](https://medium.com/business-friendly-metadata) | [Universal Data Models](https://medium.com/universal-data-models) | [Next-Gen Data Modeling](https://medium.com/next-gen-data-modeling)

[![Towards Data Engineering](https://miro.medium.com/v2/resize:fill:96:96/1*oY6pUgtb7NF-tG2sxtTQyQ.png)](https://medium.com/towards-data-engineering?source=post_page---post_publication_info--a785e96b0e4e---------------------------------------)

[![Towards Data Engineering](https://miro.medium.com/v2/resize:fill:128:128/1*oY6pUgtb7NF-tG2sxtTQyQ.png)](https://medium.com/towards-data-engineering?source=post_page---post_publication_info--a785e96b0e4e---------------------------------------)

[Last published 3 hours ago](https://medium.com/towards-data-engineering/quick-guide-event-driven-architecture-02713777b90b?source=post_page---post_publication_info--a785e96b0e4e---------------------------------------)

Dive into data engineering with top Medium articles on big data, cloud, automation, and DevOps. Follow us for curated insights and contribute your expertise. Join our thriving community of professionals and enthusiasts shaping the future of data-driven solutions.

[![Jaco van der Laan](https://miro.medium.com/v2/resize:fill:96:96/1*DuAJ6b9tKWTlEMnwgVDJBQ.jpeg)](https://medium.com/@jacovanderlaan?source=post_page---post_author_info--a785e96b0e4e---------------------------------------)

[![Jaco van der Laan](https://miro.medium.com/v2/resize:fill:128:128/1*DuAJ6b9tKWTlEMnwgVDJBQ.jpeg)](https://medium.com/@jacovanderlaan?source=post_page---post_author_info--a785e96b0e4e---------------------------------------)

[334 following](https://medium.com/@jacovanderlaan/following?source=post_page---post_author_info--a785e96b0e4e---------------------------------------)

Exploring Business & Logical Data Modeling. Writing on Clarity, Structure & Creative Approaches to Data Architecture.

## Responses (3)

S Parodi

What are your thoughts?  

```c
Only supports DuckDB ?
```

```c
Sounds cool, how does it differ from using lineage in dbt?
```

```c
Great article, is it extended version of what Erwin does today ? allows data Modeler to design ERD using UI , Later Erwin can do forward engineering to generate DDL for DB which can be executed on DB directly ?
```