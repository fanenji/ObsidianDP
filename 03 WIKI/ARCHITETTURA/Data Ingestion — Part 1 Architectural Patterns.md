---
title: "Data Ingestion — Part 1: Architectural Patterns"
source: https://medium.com/the-modern-scientist/the-art-of-data-ingestion-powering-analytics-from-operational-sources-467552d6c9a2
author:
  - "[[janmeskens]]"
published: 2023-11-27
created: 2026-04-04
description: "Data Ingestion — Part 1: Architectural Patterns Over the course of two articles, I will thoroughly explore data ingestion, a fundamental process that bridges the operational and analytical worlds …"
tags:
  - clippings
  - architecture
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)## [The Modern Scientist](https://medium.com/the-modern-scientist?source=post_page---publication_nav-a812fbb05bb7-467552d6c9a2---------------------------------------)

[![The Modern Scientist](https://miro.medium.com/v2/resize:fill:76:76/1*9FbQbOV7VrXIwo_U-Q3mQA.png)](https://medium.com/the-modern-scientist?source=post_page---post_publication_sidebar-a812fbb05bb7-467552d6c9a2---------------------------------------)

The Modern Scientist aspires to connect builders & the curious to forward-thinking ideas. Either you are novice or expert, TMS will share contents that fulfils your ambition and interest. Write with us: [shorturl.at/hjO39](http://shorturl.at/hjO39)

Over the course of two articles, I will thoroughly explore data ingestion, a fundamental process that bridges the operational and analytical worlds. Ingestion is critical for transporting data from a multitude of sources in its original operational environment — often referred to as the ‘operational plane’ — to the sphere of analysis, or the ‘analytical plane’. This transition is essential for unlocking the full potential of analytical empowerment.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*KgViPR7-lyNP5BH-m6z6nQ.png)

Data Ingestion serves as the critical link between the operational plane — where data originates — and the analytical plane — where data is transformed into analytical products such as AI models, dashboards, and APIs (Image credit: Author ).

The essence of this empowerment is the ability to generate data-driven insights and implement artificial intelligence models, relying on a diverse array of data sources. The analytical capacity of an organization often directly correlates with the number of data sources it can effectively analyze. Therefore, choosing the right data ingestion strategies is crucial. These strategies must be robust enough to handle a wide range of relevant data sources, from standard operational applications like CRMs, ERPs, and financial systems to more unconventional ones such as IoT sensors, APIs, and diverse formats like (scraped) documents, images, and videos.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*NdgmV6-n7IFDtJkMhrXkLg.png)

Data ingestion forms a key piece in the broader data platform puzzle. The choice of ingestion strategies hinges on underlying architectural designs and can be executed through a diverse range of tool flavors. (Image: Author ).

When taking a broader view, it becomes clear that data ingestion, while just one element, is a crucial component of the larger data platform puzzle within an organization. This data platform typically serves as a cornerstone in digital transformation initiatives, aiding organizations in achieving their business objectives. At its core, a data platform comprises various architectural patterns and an array of tools, each playing a vital role in its functionality and effectiveness.

In the **first of two articles dedicated to data ingestion**, this piece explores the architectural paradigms that guide the selection of suitable data ingestion technology. My aim is to distill each pattern to its essence, shedding light on the strategic implications they hold for the data ingestion process. The ambition behind presenting these patterns is to identify and surmount the hurdles that often complicate what should theoretically be the most straightforward yet absolutely essential task: integrating data within your analytical framework. Grasping the strategic gravity of data ingestion is imperative for guaranteeing a fluid transition and effective utilization of data across the vast expanse of an organization’s data ecosystem.

## Pattern 1: Unified Data Repository

The first architectural approach we examine is the *Unified Data Repository* pattern, where a single storage system caters to both the operational application needs and analytical processing. Typically, this system is a Relational Database Management System (RDBMS). In such a setup, the same database is utilized for both everyday operations and data analysis, eliminating the necessity for data transfer between distinct storage solutions.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*CX3FnWK1O5LwuYDEmO-Vkg.png)

A unified data repository addresses the requirements of operational applications and supports analytical processing. Analytical insights are generated through virtualization, using views, or by duplicating and transforming data (Image credit: Author ).

Within this approach, there are two prevalent sub-patterns:

1. **Virtualization** — This involves the creation of virtual database layers, or views, that provide an analytical perspective atop operational tables within the database. It’s a way to ‘see’ the data through an analytical lens without physically altering or duplicating the data.
2. **Duplication and Transformation** — Here, operational data is replicated in a format more conducive to analysis. This can be implemented via stored procedures, materialized views, or within the operational application’s storage layer itself, effectively creating a parallel version of the data optimized for analytical queries.

While this model offers simplicity in data management and the availability of raw data, it does come with significant limitations:

- **Data Integration Challenges** — The model inherently struggles with integrating data from disparate physical databases, as it relies on a single storage system. To overcome this, one might resort to techniques like linked servers or cross-database queries, which, however, tend to introduce additional complexity and are generally not preferred.
- **Potential for System Interference** — Operational and analytical processes operating concurrently on the same database can cause mutual interference, leading to increased load and potentially degrading the performance of both the operational applications and the analytical processing.
- **Performance Trade-offs** — The differing optimization needs of Online Transaction Processing (OLTP) systems, which prioritize efficient handling of high volumes of transactions, and Online Analytical Processing (OLAP) systems, which are optimized for complex query processing, means that a system that tries to do both will likely be suboptimal for each task.
- **Tightly Coupled** — The unified data repository pattern leads to a strong interconnection between the operational and analytical domains, resulting in restricted or no flexibility in either area.

Given these constraints, the Unified Data Repository approach is typically not recommended for handling large datasets or when dealing with multiple physical data sources. It may be suitable for smaller-scale applications operating on a robust database where the scale does not tip towards complexity.

## Pattern 2: Data Virtualization

Building upon the initial pattern, the Data Virtualization approach leverages specialized software to establish a virtualized data layer over multiple underlying data sources. This intermediary layer allows for the execution of queries that are partially processed by the original data sources, integrating the results into a cohesive dataset for analysis.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*0dZuHmrvmsz3lan7Hn1zdA.png)

A virtualized data layer orchestrates the execution of real-time queries across a range of underlying data sources (Image credit: Author ).

Key benefits of this approach include:

1. **Near-Real-Time Data Access** — Since data is not physically relocated to an analytical database but queried directly at the source, this pattern offers swift data availability, closely approximating real-time.
2. **Intelligent Caching** — Data virtualization systems are typically designed with advanced caching capabilities, which can minimize the demand on source systems and optimize performance.

However, this approach also introduces several concerns:

- **Source System Limitations** — If the source databases are not optimized for certain query types, their performance bottlenecks could extend to the virtual layer, particularly if it is dependent on source responses for query execution.
- **Network Overhead** — A virtualization layer that interfaces with data sources distributed across different network zones may experience latency, impacting overall performance.
- **Historical Data Tracking** — As the virtual layer does not inherently store data, it presents challenges for historical analysis, commonly referred to as “time travel”, across the data ingestion timeline.

It’s important to note that specific data virtualization solutions may offer unique mechanisms to address these issues. My overarching recommendation for any significant architectural decision, including this one, is to thoroughly test the data virtualization solution with your particular infrastructure. This will help understand its capabilities and limitations, allowing for appropriate scaling and fine-tuning to optimize the integration and analysis processes.

## Pattern 3: ETL

ETL, standing for Extract, Transform, Load, represents a well-established paradigm in data processing. Initially, data is harvested from its source (*Extract*), thereafter refined on an ETL server (*Transform*), and ultimately, the polished output is deposited into an analytics-focused database (*Load*).

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*g3y7yZvmVhfmC7chWiUV5Q.png)

ETL servers carry out the ETL processes configured in the design interface. These pipelines manage the extraction of data from its origins, its transformation into a format suitable for analysis, and its subsequent loading into a data platform such as a Data Warehouse or Operational Data Store. Data products typically access and utilize the information stored within these platforms (Image credit: Author ).

For years, a multitude of ETL tool providers have supported this method, offering a variety of specialized transformation techniques and design styles. The prevalent style involves a graphical interface where users can interlink Extract, Transform, and Load operations within an intuitive visual workflow. These processes are often further customizable through scripting or direct SQL queries.

The prime benefits of ETL include:

- **Centralized Logic** — ETL processes enable the consolidation of the full transformation logic in a single, manageable environment, thereby not just facilitating data ingestion but also shaping data to meet analytical requisites.
- **User-Friendly Design** — The visual nature of ETL tools democratizes the data transformation process, empowering users across skill levels to participate in data pipeline creation.

However, ETL is not without its drawbacks, which have led to the emergence of alternative models:

1. **Dependence on Specific Vendors** — ETL tool dependence can lead to a form of vendor lock-in, making transitions to other platforms costly and complex, particularly if the current tool changes pricing or discontinues features.
2. **Performance Constraints** — ETL transformations are executed by designated servers, which may not scale comparably to the high-performance compute resources available in modern data warehouses, thus becoming potential bottlenecks. This scenario presents a paradox: despite having a highly efficient data warehouse engine for query execution, the entire pipeline’s throughput is throttled by the ETL server, which processes transformations at a considerably slower pace.
3. **Opaque Data Lineage** — The simplification into visual components often masks the complexity of data transformation, rendering the understanding and auditing of the data’s journey (data lineage) challenging for those outside the ETL tool’s environment.
4. **Limited Scalability** — While ETL tools are designed for broad accessibility, they may lack robust capabilities for scaling and industrialization (as for example described in ==[DataOps](https://www.gartner.com/en/information-technology/glossary/dataops)== ==frameworks==), which are critical as data platforms grow.
5. **Rigidity** — Inflexibility arises when ETL tools cannot accommodate unique data ingestion requirements, leading to workaround solutions that contribute to technical debt.

These common limitations of the ETL pattern can often be addressed by specific ETL vendors. Particularly when ETL tools are integrated into comprehensive suites designed for a particular cloud DWH, issues related to speed and performance can be mitigated. Nonetheless, it’s crucial to stay ahead in understanding the development trajectory of the ETL tool, making sure it continues to align with evolving data ingestion requirements like growing data volumes or emerging types of data sources.

## Pattern 4: ELT

ELT, sharing the basic steps of ETL, diverges by restructuring and redefining these processes. In ELT:

- **EL** — Extract and Load operations are carried out first, transferring raw data directly to the data platform without immediate transformation.
- **T** — Transformation occurs subsequently, converting raw data into actionable insights. Crucially, transformation tasks can operate independently and on different schedules from the extraction and loading.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Z0Fudfvo2Vy4suPiK4sHWw.png)

ELT pipelines are divided into two distinct segments: the EL component, which handles the ingestion of data into the data platform, and the Transformation component, which executes within the data platform to process and refine the data (Image credit: Author ).

This restructured process addresses several ETL limitations:

1. **Enhanced Flexibility** — Separating extraction/loading from transformation tools increases adaptability, enabling the selection of diverse tools for different data types and transformation standards.
2. **Aligned Performance** — Transformation takes place within the data platform, leveraging its full computational power, and is particularly effective for handling massive data sets with distributed computing engines.
3. **Improved Scalability** — The flexibility inherent in ELT facilitates the choice of transformation tools that excel in automation and scalability.

Despite these improvements, the ELT model introduces new complexities:

- **Governance of Multiple Tools** — Using different tools for extraction, loading, and transformation necessitates stringent governance to manage licensing, pricing, update cycles, and support structures.
- **Orchestration Challenges** — A more varied toolkit requires sophisticated orchestration, often based on Directed Acyclic Graphs (DAG), to ensure that transformations proceed only after successful data extraction and loading.

The ELT pattern is a personal favorite for its flexibility, but it demands a commitment to managing a multi-tool landscape and a complex orchestration strategy.

## Emerging Patterns

Beyond the established patterns, new methodologies and patterns are continuously arising. This section discusses two such emerging patterns: push and stream processing.

### Push (vs Pull)

Traditional patterns mentioned earlier are typically of the “Pull” variety, where the analytical plane actively retrieves data from the operational plane. In contrast, “Push” methodologies invert this flow: the operational plane proactively sends, or ‘pushes’, data to the analytical plane as soon as changes occur, such as Create, Read, Update, and Delete (CRUD) operations.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*NOdyt_qBq7qZXABLaEZZJQ.png)

While traditional patterns follow the “Pull” strategy, “Push” might be an option in certain situations (Image credit: Author ).

The push approach is often found within streaming architectures (discussed next) but is not confined to them. Fundamentally, it involves the operational plane initiating data transfer to an endpoint designated by the analytical plane. This setup usually mandates that development teams implement the push mechanism, either through separate components or by enhancing existing operational applications.

The primary benefit of this approach is that it allows analytical teams to concentrate on data value transformation without the distraction of constructing ingestion pipelines — the operational systems take care of data delivery. However, there’s are two significant drawbacks:

- **Requirement for a dedicated application development** **team —** This becomes problematic with pre-packaged software, Software as a Service (SaaS) offerings, or external hardware like IoT devices, where such a team may not be present or readily available. Under these circumstances, establishing a specialized ‘data integration team’ to facilitate the push into the analytical environment might be necessary, but this can quickly turn into a bottleneck.
- **Handling Push Failures —** Pull-based architectures generally demonstrate greater resilience to pipeline disruptions compared to push architectures. In the event of a pull failure, the analytical platform can reinitiate the process. However, if a push fails, the analytical platform may remain unaware of the missing push message. To counteract this drawback, push-based pipelines are often incorporated into highly available streaming architectures, designed for concurrent operation and robust availability.

The push pattern is most suitable for organizations that have a high software development maturity and/or can negotiate data pushing capabilities when procuring off-the-shelf solutions. In scenarios where this is not viable, it might be prudent to combine push with other data ingestion patterns to ensure smooth and efficient data integration.

### Stream Processing

Stream processing, also known as stream processing or event streaming, is the [continuous flow of data as it’s generated](https://www.confluent.io/learn/data-streaming/), enabling real-time processing and analysis for immediate insights. These systems are crucial for instant decision-making tasks and support high-volume, low-latency processing for activities like financial trades, real-time analytics, and IoT monitoring.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*8gcz8vPwnDL524LM-e-iQg.png)

In general, streaming middleware can be used to facilitate data ingestion in two ways: (1) by using an ETL/ELT consumer that picks up streaming messages and pushes them to the analytical plane or (2) by leveraging the streaming cache as a source for analytics (Image credit: Author ).

When marrying stream processing with analytics, two approaches stand out:

- **Adapting ELT (or even ETL) for Streaming** — This involves extracting real-time events and loading them into data platforms, preserving familiar workflows with novel data sources through bespoke or specialized streaming consumers.
- **Leveraging Streaming Caches** — Centralized, durable streaming caches act as a high-performance repository for event data. Some novel patterns utilize these caches analytically, creating a modern, efficient variant of shared data storage. A major consideration here is the integration of streaming data with static data sources, which may never pass through the streaming cache.

The unification of streaming data and more static data is being blueprinted in data architecture patterns like [KAPPA and LAMBDA](https://nexocode.com/blog/posts/lambda-vs-kappa-architecture/). These two architectures provide a way to bring both worlds together (when needed).

## Conclusions

The strategic integration of data ingestion methods is a cornerstone in the evolving landscape of data analytics. This article has highlighted four primary data ingestion patterns — Unified Data Repository, Data Virtualization, ETL, and ELT — each with unique advantages and constraints. As we dissected these patterns, we saw the Unified Data Repository’s simplicity but limited scalability, the near-real-time capability of Data Virtualization at the potential cost of performance, the centralized control of ETL shadowed by potential bottlenecks and rigidity, and the flexibility and scalability of ELT balanced against orchestration challenges.

Further, the emerging stream processing paradigms underscore the industry’s pivot towards real-time analytics. These methods, while relatively nascent, are paving the way for a more instantaneous and dynamic approach to data processing, accommodating the ceaseless velocity of information generation.

In [my subsequent article](https://medium.com/@meskensjan/data-ingestion-part-2-tool-selection-strategy-07c6ca7aeddb), I will delve more deeply into selecting the appropriate data ingestion tool for your data platform. A critical consideration in this process is the architectural pattern within which this tool will integrate.

*Questions? Feedback? Connect with me on* [*LinkedIn*](https://www.linkedin.com/in/janmeskens/) *or contact me directly at Jan@Sievax.be!*

*This article is proudly brought to you by* [*Sievax*](http://www.sievax.be/)*, the consulting firm dedicated to guiding you towards data excellence. Interested in learning more? Visit our* [*website*](http://www.sievax.be/)*! We offer a* [*Data Strategy Masterclass*](https://sievax.be/academy/data-ai-strategy-masterclass/) *that provides a deeper understanding of the world of data strategy.*

[![The Modern Scientist](https://miro.medium.com/v2/resize:fill:96:96/1*9FbQbOV7VrXIwo_U-Q3mQA.png)](https://medium.com/the-modern-scientist?source=post_page---post_publication_info--467552d6c9a2---------------------------------------)

[![The Modern Scientist](https://miro.medium.com/v2/resize:fill:128:128/1*9FbQbOV7VrXIwo_U-Q3mQA.png)](https://medium.com/the-modern-scientist?source=post_page---post_publication_info--467552d6c9a2---------------------------------------)

[Last published Mar 27, 2026](https://medium.com/the-modern-scientist/reproducible-ai-versioning-models-prompts-and-data-96dd0337af65?source=post_page---post_publication_info--467552d6c9a2---------------------------------------)

The Modern Scientist aspires to connect builders & the curious to forward-thinking ideas. Either you are novice or expert, TMS will share contents that fulfils your ambition and interest. Write with us: [shorturl.at/hjO39](http://shorturl.at/hjO39)

[![janmeskens](https://miro.medium.com/v2/resize:fill:96:96/1*lis5rj9zbTz_-alrl4atqA.jpeg)](https://medium.com/@meskensjan?source=post_page---post_author_info--467552d6c9a2---------------------------------------)

[![janmeskens](https://miro.medium.com/v2/resize:fill:128:128/1*lis5rj9zbTz_-alrl4atqA.jpeg)](https://medium.com/@meskensjan?source=post_page---post_author_info--467552d6c9a2---------------------------------------)

[80 following](https://medium.com/@meskensjan/following?source=post_page---post_author_info--467552d6c9a2---------------------------------------)

Data Strategy Consultant | Speaking, sketching and writing about the data world | "I believe that usable data will always lead to valuable data."

## Responses (28)

S Parodi

What are your thoughts?  

```c
Amazing article.

Very thorough, extremely clear and actually really interesting to see a topic, which has almost become a commodity term in the field, explained so many angles.

Looking forward to some more of your content 👍👍
```

71

```c
Do you draw these on a tablet?
```

14

```c
Very Insightful and detailed !!! Thank you
```

21