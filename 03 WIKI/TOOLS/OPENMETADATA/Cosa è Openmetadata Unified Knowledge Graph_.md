---
title: "Cosa è Openmetadata Unified Knowledge Graph_"
type: conversation
topic: data-platform
created: 2026-02-13
tags:
  - openmetadata
  - tools

---
<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Cosa è Openmetadata Unified Knowledge Graph?

OpenMetadata's Unified Knowledge Graph is a centralized repository that unifies metadata from various data assets, enabling discovery, observability, and governance across data ecosystems.[^1_1][^1_5]

## Core Concept

It structures metadata as a graph with entities (like datasets, tables, or models) as nodes and relationships (such as lineage or ownership) as edges, creating a single source of truth for data teams. This design supports scalability and customization through a schema-first architecture and APIs.[^1_5][^1_7][^1_1]

## Key Benefits

- Enhances data discovery by providing complete context and lineage visualization.[^1_1]
- Facilitates collaboration between technical and non-technical users via a streamlined UI.[^1_1]
- Powers features like data quality monitoring, compliance, and impact analysis.[^1_7][^1_5]


## Architecture Highlights

The graph integrates 100+ connectors for metadata ingestion, stored in a simple four-component system that's easy to deploy and upgrade. It differs from traditional databases by actively organizing metadata for interconnected insights, avoiding silos.[^1_7][^1_1]
<span style="display:none">[^1_2][^1_3][^1_4][^1_6][^1_8]</span>

<div align="center">⁂</div>

[^1_1]: https://open-metadata.org

[^1_2]: https://blog.open-metadata.org/introducing-the-model-context-protocol-mcp-in-openmetadata-e757385f4fb2

[^1_3]: https://datadeep.it/2023/10/04/knowledge-graph-una-guida-alla-rappresentazione-della-conoscenza/

[^1_4]: https://www.ai4business.it/intelligenza-artificiale/knowledge-graphs-limportanza-della-conoscenza-strutturata/

[^1_5]: https://www.xenonstack.com/blog/open-and-unified-metadata-platform

[^1_6]: https://www.sap.com/italy/resources/knowledge-graph

[^1_7]: https://atlan.com/openmetadata-explained/

[^1_8]: https://open-metadata.org/mcp


---

# Come funziona il Unified Metadata Graph di OpenMetadata

OpenMetadata's Unified Metadata Graph functions as a centralized, graph-based repository that actively organizes metadata from diverse data sources into interconnected nodes and edges for enhanced discovery and governance.[^2_1][^2_5]

## Metadata Ingestion

Metadata is ingested via a pull-based mechanism using over 100 connectors, where the platform retrieves data from sources like databases, pipelines, and dashboards rather than relying on pushes, ensuring consistency and reliability. This process populates entities (nodes such as tables or models) and their relationships (edges like lineage or ownership) into the graph structure.[^2_2][^2_5][^2_1]

## Graph Storage and Querying

Metadata is stored in a schema-first architecture with graph storage, enabling scalable queries for discovery through keyword search, associations (e.g., joined tables), and lineage tracing. The four-component system (API, ingestion, search, UI) supports extensibility, allowing custom entities and real-time updates via APIs.[^2_5][^2_1][^2_2]

## Key Operations

- **Lineage Tracking**: Visualizes data flow across assets with manual editing via drag-and-drop for accuracy.[^2_2]
- **Search and Discovery**: Combines advanced filters, profiling, and relationships for contextual asset location.[^2_2]
- **Governance Features**: Enforces versioning, tags, and compliance through the interconnected graph.[^2_1][^2_5]
<span style="display:none">[^2_10][^2_3][^2_4][^2_6][^2_7][^2_8][^2_9]</span>

<div align="center">⁂</div>

[^2_1]: https://open-metadata.org

[^2_2]: https://docs.open-metadata.org/latest/features

[^2_3]: https://github.com/open-metadata/OpenMetadata

[^2_4]: https://www.reddit.com/r/dataengineering/comments/1j4wzpj/openmetadata_and_python_models/?tl=es-es

[^2_5]: https://atlan.com/openmetadata-explained/

[^2_6]: https://github.com/nubank/NuOpenMetadata

[^2_7]: https://www.reddit.com/r/dataengineering/comments/1d6aem0/whats_your_experience_using_openmetadata/

[^2_8]: https://www.reddit.com/r/dataengineering/comments/yxrh9y/metadata_store_which_one_to_choose_openmetadata/

[^2_9]: https://www.reddit.com/r/dataengineering/comments/rfqxhh/why_openmetadata_is_the_right_choice_for_you/

[^2_10]: https://it.linkeddata.center/


---

# Come si integra OpenMetadata con data catalog esistenti

OpenMetadata si integra con data catalog esistenti attraverso un'ampia libreria di connettori pre-costruiti che supportano l'ingestione bidirezionale di metadata, consentendo la coesistenza e la federazione senza migrazioni forzate.[^3_1][^3_2]

## Connettori Supportati

La piattaforma offre oltre 100 connettori per data catalog come DataHub, Amundsen, Atlas, Alation e Collibra, permettendo di estrarre e sincronizzare entità, lineage e relazioni nel suo Unified Metadata Graph. Questi connettori operano in modalità pull per mantenere la consistenza, con supporto per ingestion programmata e real-time via webhook o API.[^3_2][^3_3][^3_1]

## Processo di Integrazione

- Configurare il connettore tramite YAML o UI, specificando credenziali e filtri per entità da importare.
- Eseguire l'ingestion per popolare il graph con metadata esistenti, preservando ownership e glossari.
- Abilitare federazione per query cross-catalog e lineage unificato, con opzioni per push-back di aggiornamenti.[^3_3]


## Vantaggi Operativi

Le integrazioni evitano silos promuovendo un single pane of glass per discovery e governance, con estensibilità via plugin custom per catalog non nativi. Questo approccio scala con ecosistemi ibridi, riducendo complessità operativa.[^3_1][^3_2][^3_3]

<div align="center">⁂</div>

[^3_1]: https://open-metadata.org

[^3_2]: https://atlan.com/openmetadata-explained/

[^3_3]: https://docs.open-metadata.org/latest/features
