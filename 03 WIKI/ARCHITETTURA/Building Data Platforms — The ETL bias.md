---
title: Building Data Platforms — The ETL bias
source: https://medium.com/codex/building-data-platforms-the-etl-bias-d589733ce4cc
author:
  - "[[João Vazao Vasques]]"
published: 2021-05-30
created: 2026-04-04
description: Building Data Platforms I — The ETL bias [Second part is now live – https://link.medium.com/f6Ixe9Htbhb] [Part III is now available here] This is the first article of the Building Data Platforms …
tags:
  - clippings
  - architecture
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)## [CodeX](https://medium.com/codex?source=post_page---publication_nav-29038077e4c6-d589733ce4cc---------------------------------------)

[![CodeX](https://miro.medium.com/v2/resize:fill:76:76/1*VqH0bOrfjeUkznphIC7KBg.png)](https://medium.com/codex?source=post_page---post_publication_sidebar-29038077e4c6-d589733ce4cc---------------------------------------)

Everything connected with Tech & Code. Follow to join our 1M+ monthly readers

==\[Second part is now live –== ==[https://link.medium.com/f6Ixe9Htbhb\]](https://link.medium.com/f6Ixe9Htbhb])==

\[Part III is now available [here](https://joaovasques.medium.com/building-data-platforms-iii-the-evolution-of-the-software-engineer-bdb3d9c1dd71)\]

This is the first article of the Building Data Platforms series. Why doing this in the first place you might be asking? It is simple. If you step back and look at the way the software industry approaches Data you see it has not fundamentally changed if we compare to other shifts that happened in the last 10–15 years. We got new tools such as Kafka, Spark, Flink and Snowflake but we haven’t changed the mindset of how we build Data Platforms. As you will see, this has a lot of consequences that go from lack of productivity, broken systems, knowledge silos, unhappy people, etc.

Let’s start this series with what I consider to be the biggest problem in building Data Platforms — the ETL bias.

## What is ETL?

ETL stands for Extract, Transform and Load and became quite popular in 1970s. During that decade, companies started to have multiple data repositories and wanted to persist relevant information in one place for analysis. ETL became the de facto standard to perform these type of actions.

### Extract

This step is responsible for reading data from a set of Data sources. These usually are relational databases, NoSQL databases, JSON, CVS or XML files, etc. Most of the times, this step requires direct read only access to where the data is located.

### Transform

Translates the source data to match the format of the destination system. Operations in this stage include changing data types, combining or splitting fields, applying more complex formulas to derive new fields.

### Load

This steps takes the Data that was resulted from the Transform stage and persists it into a target data system. It is very common for the target system to be a Data Warehouse or in a file system.

ETLs can be chained together to create pipelines of computations and are usually scheduled to run with a given frequency (e.g. hourly, daily, monthly, etc).

Now that we have a definition of what ETL is, let’s start to understand some of the problems it has.

## The first Data Product

The first Data Product in a company is usually the same and answers the following need

> “We need metrics and KPIs about our main product”.

It is important to mention that we are not talking about Platforms yet but a simple Data Product. The goal of this Data Product is to allow everyone in the company to use Data for analytics.

Most of the times, the first Data Product is done using some sort of ETL like the one below.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*KYnMFi7S5JaeoKlJvd7p4A.jpeg)

A classic ETL pipeline

Let’s take a close look of is happening here:

- We have a read only replica of the main operational database
- We fully understand the domain model and schema
- There is a cron job (or a visual drag and drop tool) that runs a set of MongoDB and SQL queries, applies some transformations and loads it into another SQL database (e.g. another Postgres/MySQL instance because people don’t have time to learn a new database technology.)

The domain is small and its knowledge is shared across all engineering the team, the mapping logic from the operational system to the KPIs is quite simple which makes it quite fast to ship. After the ETL pipeline is done the company is able pull data out of its operational system and has a nice set of dashboards to power its business.

The first Data Product is a **massive success** and everyone is happy with it.

![TODO](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ntrZ3s0n7-8VrqHLyDp3NQ.jpeg)

## Complexity kicks in

There is a point in time where every company starts to break their monolith into smaller components — the so called Microservices. In this journey to microservices, engineering teams usually apply and API best practices with the goals of encapsulating complexity (via higher order abstractions) while making the system extensible. All of this under the mantras of operational reliability, developer speed and experience with the ultimate goal of building a better product faster.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*aG7VGMEShINnguKhUmY55Q.jpeg)

During the expansion to microservices teams might decide to adapt different database technologies because they make sense under the domain and scope their system operates in. Since systems communicate via APIs there is no problem in having a different database technology.

A couple of months after the company decided to break the monolith engineers are shipping code faster, the product is stable and new features are being built. The quest to break the monolith was a success!

But, what about our Data Product?

Over the last months, the ETL has grown and became more complex. Instead of having to query one database to fetch data, the ETL has to connect to multiple data sources. Besides this obvious increase in complexity, what else has changed?

**Ownership —** maintaining and developing the ETL is now a shared responsibility of the first engineers that built it. These engineers now work on different systems responsible for specific domains. Who is the owner of the ETL?

**Database technology —** Different systems might have different database technologies (e.g. MongoDB, MySQL, Postgres, Cassandra, etc..). This means the ETL logic will have a mix of all of those technologies with different query languages. This increases the complexity of the business logic that the ETL needs to implement.

**Stability—** the main goal of having APIs is to allow teams to change their systems without breaking their clients logic. However, since ETLs (most of the times) connect to read only databases, changes in the schema might break the ETL and cause **data downtime** (I will go deeper on this topic later in this series). Also, building data extraction APIs in the operational systems is not considered a priority because the team needs to focus on building and improving the main product.

There is a point in time where companies realizes they need to have an owner for their Data Product, for their ETL. They might acknowledge it because:

- People are opening issues complaining about missing data
- ETL pipelines are breaking more often and engineers are spending more time fixing them
- Engineers claim the query logic of the data product is too complex and they lack deep knowledge on a specific database
- Building complex data objects require deeper database expertise

The solution is simple

> They need to have a Data Engineering Team

## Rise and fall

The company now has a Data Engineering team with extensive knowledge in some of the databases that are being used. In the beginning, the team might be able to fix some of problems related to performance and stability of the current ETL pipelines. After that happens, there is a positive trend in the organisation. That trend is based on the following facts:

1. There is (at last!) a team that has extensive knowledge of different database technologies
2. There is a single team that knows the nuances of several systems, because they need to know their ontologies
3. The data collection process is working correctly
4. Engineering teams can focus in building features because the Data component is being taken cared of

The Data Engineering team has done what many considered to be impossible

> **They have made Data Products great again**

Happiness of having a Data driven company — [source](https://giphy.com/gifs/borat-great-success-a0h7sAqON67nO)

Armed with this new positive and bullish vibe towards Data, Product and Engineering teams start planning new features. With these new features come important changes to the product to support new use cases and new metrics to be made available. The backlog of the Data Engineering team starts to become packed with new issues to support new features and other areas in the business such as Customer facing teams. This leads to a set of meetings with engineering teams to discuss changes in Data models and how they impact the current ETL pipelines. With multiple changes to be made, engineers suddenly realize that the complexity of changing data pipeline DAGs is non trivial. Keeping the current Data Products up to date is not as simple as it initially people thought.

Because no one wants to be in the place where they constantly fixing broken data pipelines, the consequences are simple: new features will not be shipped as fast as Product and other business units planned. This leads to frustration, friction and a general feeling that..

> **“Data is slowing us down”**

The fact is, they are all right.

## Why is Data Broken and slow?

The question about Data being broken and slow is not new. Everyone that works or has worked on Data systems knows this.

I believe the root of the problem is not related to technical experience but with a mindset of looking at Data. Since ETL became a standard, Data teams were responsible of maintaining them and ensuring they worked. Data teams were mostly groups of people with very technical knowledge of databases (the so called DBAs)

Product and Engineering teams did not consider Data as a first class citizen because Data teams existed exactly to “deal with Data”. It did not make sense for a team building features to worry about who needs the data they produce. That has been the standard in the industry for quite some time (I’d say since the 70s). However, let me ask you the following question

> “If Data is the most precious asset in a company, does it make sense to have only one team responsible for it?”

The answer is of course **No**. However, the way the majority of companies deal with Data is still the same and results from what I call the ETL bias. This means that there is one team (Data Engineering) that must:

- Pull Data from all operational systems
- Know all database schemas in the company
- Build all the data models for reporting

While other engineering teams must:

- Build features for the product
- Not worry about “data stuff” to avoid slowing the product development

In order for companies to be successful and use Data for their advantage they need to change their mindset. In recent years, Agile and DevOps changed the way software is built. If we look back to the reasons behind those two movements they solved the same problem: something was fundamentally slowing down companies. Back then it software and dealing with infrastructure. Today it is data.

In the second part of this series, we will cover how I think R&D teams should approach Data because, as we all know, Data is the most important asset in a XXI century modern Internet company. It is time for it to start being treated as such.

[![CodeX](https://miro.medium.com/v2/resize:fill:96:96/1*VqH0bOrfjeUkznphIC7KBg.png)](https://medium.com/codex?source=post_page---post_publication_info--d589733ce4cc---------------------------------------)

[![CodeX](https://miro.medium.com/v2/resize:fill:128:128/1*VqH0bOrfjeUkznphIC7KBg.png)](https://medium.com/codex?source=post_page---post_publication_info--d589733ce4cc---------------------------------------)

[Last published 15 hours ago](https://medium.com/codex/i-built-a-data-quality-system-that-catches-errors-before-they-reach-production-ee1cb310011b?source=post_page---post_publication_info--d589733ce4cc---------------------------------------)

Everything connected with Tech & Code. Follow to join our 1M+ monthly readers

[![João Vazao Vasques](https://miro.medium.com/v2/resize:fill:96:96/1*B5fSvuLnbNw3CZVesYMSDQ@2x.jpeg)](https://medium.com/@joaovasques?source=post_page---post_author_info--d589733ce4cc---------------------------------------)

[![João Vazao Vasques](https://miro.medium.com/v2/resize:fill:128:128/1*B5fSvuLnbNw3CZVesYMSDQ@2x.jpeg)](https://medium.com/@joaovasques?source=post_page---post_author_info--d589733ce4cc---------------------------------------)

[390 following](https://medium.com/@joaovasques/following?source=post_page---post_author_info--d589733ce4cc---------------------------------------)

Blockchain Analytics @Chainlink | Alumni of: @Unbabel, @talkdesk, @Uniplaces |1x startup founder| Taekwondo black belt

## Responses (6)

S Parodi

What are your thoughts?  

```c
Joao, I like your conclusion. At first data product ownership must be fixed. You cannot solve this problem every decade with the next IT silver bullet.
```

8

```c
Very nicly said - at metrolink.ai we try to fix this !
```

2

```c
Good article! I recommend the articles https://martinfowler.com/articles/data-monolith-to-mesh.html and https://martinfowler.com/articles/data-mesh-principles.html on the same subject, but more focused on potential changes in organization.
```

1