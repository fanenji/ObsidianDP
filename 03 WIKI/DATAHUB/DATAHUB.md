---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - datahub
---

- [https://datahubproject.io/](https://datahubproject.io/)
- INTRO VIDEO [https://www.youtube.com/watch?v=VY57iRdG-Us&t=6s](https://www.youtube.com/watch?v=VY57iRdG-Us&t=6s)
- GITHUB [https://github.com/datahub-project/datahub](https://github.com/datahub-project/datahub)
- YOUTUBE [https://www.youtube.com/@DataHubProject/videos](https://www.youtube.com/@DataHubProject/videos)
- SLACK [https://app.slack.com/client/TUMKD5EGJ/CV2KB471C](https://app.slack.com/client/TUMKD5EGJ/CV2KB471C)
- [https://atlan.com/linkedin-datahub-metadata-management-open-source](https://atlan.com/linkedin-datahub-metadata-management-open-source)

**DEMO** [https://demo.datahubproject.io/](https://demo.datahubproject.io/)

# **COSA FA**

- Ingestion
    - schedulazione
    - UI o CLI (con yaml)
    - Source → Sink (REST o KAFKA)
- Transformers
- Profiling
- API: molto complete
    - python, java
    - GraphQL, OpenAPI
- CLI
- Actions Framework
- Search
- Schema History
- Domains (logical grouping)
- Glossary
- Tags
- Data Products
- Access Policy
- Usage & query history
- Lineage
- Tests

# UTILIZZI

- Data Discovery
- Data Observability
- Data Lineage
- Data Quality
    - Reliability
    - Completeness
    - Timeliness
    - Consistency
    - Veracity
- Data Governance
    - OwnerShip
    - Discoverability
    - Compliancy

# **Integrations**

[https://datahubproject.io/integrations/](https://datahubproject.io/integrations/)

# ARCHITETTURA

[https://github.com/datahub-project/datahub/blob/master/docs/architecture/architecture.md](https://github.com/datahub-project/datahub/blob/master/docs/architecture/architecture.md)

![[1 - LAVORO/attachments/DATAHUB/Untitled.png]]

![[1 - LAVORO/attachments/DATAHUB/Untitled 1.png]]

**DataHub's infrastructure is stream-oriented**

Modello a eventi → [https://engineering.linkedin.com/blog/2020/datahub-popular-metadata-architectures-explained](https://engineering.linkedin.com/blog/2020/datahub-popular-metadata-architectures-explained)

![[1 - LAVORO/attachments/DATAHUB/Untitled 2.png]]

> **The benefits**

> With this evolution, clients can interface with the metadata database in different ways depending on their needs. They get a stream-based metadata log (for ingestion and for change consumption), low latency lookups on metadata, the ability to have full-text and ranked search on metadata attributes, and graph queries on metadata relationships, as well as full scan and analytics capabilities. Different use cases and applications with different extensions to the core metadata model can be built on top of this metadata stream without sacrificing consistency or freshness. You can also integrate this metadata with your preferred developer tools, such as git, by authoring and versioning this metadata alongside code. Refinements and enrichments of metadata can be performed by processing the metadata change log at low latency or by batch processing the compacted metadata log as a table on the data lake.

> **The downsides**

> Sophistication often goes hand in hand with complexity. A third-generation metadata system will typically have a few moving parts that will need to be set up for the entire system to be humming along well. **Companies with a small number of data engineers might find themselves turned off by the amount of work it takes to get a simple use case off the ground and wonder if the initial investment in time and effort is worth the long term payoff.** However, third-generation metadata systems like DataHub are starting to make big advances in usability and out-of-the-box experience for adopters to ensure that this doesn’t happen.

[https://atlan.com/openmetadata-vs-datahub/](https://atlan.com/openmetadata-vs-datahub/)

> DataHub uses a [Kafka-mediated](https://kafka.apache.org/) ingestion engine to store the data in three separate layers - [MySQL](https://www.mysql.com/), [Elasticsearch](https://www.elastic.co/), and [neo4j](https://neo4j.com/) using a [Kafka stream](https://kafka.apache.org/documentation/streams/).

> The data in these layers is served via an API service layer. In addition to the standard [REST API](https://aws.amazon.com/what-is/restful-api/), DataHub also supports Kafka and [GraphQL](https://graphql.org/) for downstream consumption. DataHub uses the [Pegasus Definition Language](https://linkedin.github.io/rest.li/pdl_schema) (PDL) with custom annotations to store the model metadata.

![[1 - LAVORO/attachments/DATAHUB/Untitled 3.png]]

CONTAINER

![[1 - LAVORO/attachments/DATAHUB/Untitled 4.png]]

[TEST](1%20-%20LAVORO/1%20-%20PROGETTI/DATA%20PLATFORM%20(DP)/MATERIALI/DATAHUB/TEST.md)

%% MOC START %%
- [[DATAHUB DBT]]
- [[DATAHUB DREMIO]]
- [[NOTE DATAHUB]]
%% MOC END %%
