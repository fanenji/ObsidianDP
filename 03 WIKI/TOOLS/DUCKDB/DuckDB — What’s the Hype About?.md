---
title: DuckDB — What’s the Hype About?
source: https://medium.com/better-programming/duckdb-whats-the-hype-about-5d46aaa73196
author:
  - "[[Oliver Molander]]"
published: 2022-11-16
created: 2026-04-04
description: DuckDB — What’s the Hype About? This was a blog post that I already planned to write during the spring when I saw that the hype around DuckDB started taking new heights. Since then the discussion …
tags:
  - clippings
  - duckdb
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)## [Better Programming](https://medium.com/better-programming?source=post_page---publication_nav-d0b105d10f0a-5d46aaa73196---------------------------------------)

[![Better Programming](https://miro.medium.com/v2/resize:fill:76:76/1*QNoA3XlXLHz22zQazc0syg.png)](https://medium.com/better-programming?source=post_page---post_publication_sidebar-d0b105d10f0a-5d46aaa73196---------------------------------------)

Advice for programmers.

## This was a blog post that I already planned to write during the spring when I saw that the hype around DuckDB started taking new heights. Since then the discussion around DuckDB has only intensified in the developer and data engineering community. I currently see two trends within the data community with high engagement levels: DuckDB and Rust taking over data engineering. But what’s the hype around DuckDB really about? Let’s scratch the surface a little bit.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*4Weg6vDOBLdp_to5)

DuckDB Github stars over time

A lot of today’s acceleration in the data space can be coupled with the explosive rise of cloud data warehouses over the last few years. Cloud data warehouses have become the cornerstone of data stacks: companies and organizations of all sizes use a data warehouse to power analytics use cases. Snowflake’s meteoric rise — culminated by its blockbuster IPO in September 2020 that became the largest software IPO in history — has been the poster child of this trend.

When looking at the [3 Vs of Big Data](https://www.techtarget.com/whatis/definition/3Vs) (Velocity, Volume, Variety), many in the data community that I’ve spoken with lately have said that the most required dimension during the past years has been velocity.

As [noted by Mehdi Ouazza](https://www.linkedin.com/posts/mehd-io_bigdata-activity-6971089401825107968-L2WQ/?utm_source=share&utm_medium=member_desktop) (Staff Data Engineer at Trade Republic) — the truth is that everyone doesn’t have “Big” data — but a requirement for low latency consumption from micro-service on data assets processed out of your OLTP database is a common use case.

As [Mehdi](https://www.linkedin.com/in/mehd-io/) says, if one looks at some product trends (RocksDB, DuckDB, Clickhouse), they all provide an easier interface for low-latency consumption. Even some cloud data warehouse giants have invested in these applications, such as [Snowflake Unistore](https://www.snowflake.com/en/data-cloud/workloads/unistore/).

However, the current cloud data warehouse paradigm is still heavily skewed for a client-server use case and ignores a growing segment of users. As [noted by Tomasz Tunguz](https://www.linkedin.com/pulse/my-laptop-faster-than-your-cloud-announcing-tomasz-tunguz/?trackingId=NaXT7r7rnwuB0RwDF8%2B6yw%3D%3D) (investor at Redpoint Ventures):

> “Most workloads aren’t massive. Instead of requiring a scale-out database in the sky, most analyses are faster with an optimized database on your computer that can leverage the cloud when needed.”

DuckDB is changing this.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*e2CmG6U2nb9m55v0.png)

Google Trends search data for “DuckDB”

As visible through the Google Trends search data above — during the past few months there has been a growing discussion and palpable hype around DuckDB in the data community.

## The growing momentum

The growing momentum behind DuckDB becomes evident just by looking at posts on social media. E.g. [Robert Sahlin](https://www.linkedin.com/in/robertsahlin/) (Data Engineering Lead at MatHem), [noted the following](https://www.linkedin.com/posts/robertsahlin_read-bq-table-to-duckdb-directly-from-storage-activity-6949849237752852480-tod6?utm_source=linkedin_share&utm_medium=member_desktop_web) on LinkedIn back in July:

> “I’ve heard a lot of good things about DuckDB lately and have found podcasts with both Jordan Tigani (founder of MotherDuck and BigQuery celebrity) and Hannes Mühleisen (creator founder of DuckDB Labs) really good. Hence I had to give it a try. My first program was to create a DuckDB table by reading directly from a BigQuery table using the BigQuery Storage Read API since it supports arrow tables (and no compute). Turned out to be really easy, sharing as a gist. Can’t wait to experiment some more with DuckDB and with bigger data volumes, it sure has huge potential.”

And Robert is definitely not the only one excited about DuckDB when reading social media posts (I recommend just doing a search on the hashtag #duckdb on LinkedIn or Twitter). E.g. [Abhishek Choudhary](https://www.linkedin.com/in/iamabhishekchoudhary/) (Senior Lead Data Engineer Bayer) recently wrote the following on [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:6954034470370873345?utm_source=linkedin_share&utm_medium=member_desktop_web):

> “Opinion: One of the most exciting new technologies for Data Engineering/ Data Science is DuckDB. DuckDB is insanely fast and with Apache Arrow, the duo is capable of delivering astonishing results. Another important point behind DuckDB is it’s simple. It doesn’t claim any groundbreaking stuff but sticks to the core of simple and faster data access.”

However, my favorite social media comment about DuckDB is most likely by [Josh Wills](https://www.linkedin.com/in/josh-wills-13882b/), in a [Twitter thread](https://twitter.com/josh_wills/status/1565738898436661248) that discusses the “ [How Snowflake fails](https://benn.substack.com/p/how-snowflake-fails) ” blog post by the always entertaining Benn Stancil (I recommend subscribing to his [Substack](https://benn.substack.com/)):

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/0*VI1VPnZWb3OnOovW.png)

Find below some additional screenshots of tweets showcasing the interest that DuckDB currently catalyzes in the data community:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/0*-kziQTQd-etrviAc.png)

Image source Madrona

### Building a managed solution on top of DuckDB

It’s a pretty classic playbook — take an open source tool showcasing momentum and build a service on top of it. E.g. Databricks did this with Spark and Confluent with Kafka.

[Jordan Tigan](https://www.linkedin.com/in/jordantigani/) i, long-time product leader of BigQuery at Google (a BigQuery celebrity as noted by Robert Sahlin earlier), announced in May that he’s co-founding a serverless cloud version of DuckDB called [MotherDuck](https://motherduck.com/). Joining him is his Google colleague [Tino Tereshko](https://www.linkedin.com/in/valentinotereshko/).

Besides MotherDuck, we have [DuckDB Labs](https://www.duckdblabs.com/?ref=hackernoon.com), which is a commercial company formed by [Hannes Mühleisen](https://www.linkedin.com/in/hfmuehleisen/?originalSubdomain=nl) and the other creators of DuckDB in July 2021 to provide support, custom extensions, and even custom versions of the product as a way to monetize it.

As Lauren Balik noted in her “ [6 Reality-Based Predictions for Data in 2023](https://medium.com/@laurengreerbalik/6-reality-based-predictions-for-data-in-2023-bdcf006e6026) ” blog post — venture capitalists and data professionals are right to be flocking to DuckDB.

This interest materialized yesterday with MotherDuck announcing their [$47.5M funding round](https://techcrunch.com/2022/11/15/motherduck-secures-investment-from-andreessen-horowitz-to-commercialize-duckdb/) led by e.g. a16z (early investors in e.g. Databricks) and Redpoint Ventures (early investors in e.g. Snowflake). MotherDuck and DuckDB Labs also announced a [strategic partnership](https://duckdblabs.com/news/2022/11/15/motherduck-partnership.html) at the same time.

Jordan Tigani (co-founder at MotherDuck) commented the following to [TechCrunch](https://techcrunch.com/2022/11/15/motherduck-secures-investment-from-andreessen-horowitz-to-commercialize-duckdb/) when announcing the funding round:

> “Users want easy and fast answers to their questions — they don’t want to wait for the cloud… The fact is that a modern laptop is faster than a modern data warehouse. Cloud data vendors are focused on the performance of 100TB queries, which is not only irrelevant for the vast majority of users, but also distracts from vendors’ ability to deliver a great user experience.”

## But what’s this hype all about? Let’s scratch the surface a little bit.

DuckDB is an easy-to-use open source in-process OLAP database (that processes data in memory and doesn’t require a dedicated server/service) — ==described by many in simplified terms as the SQLite equivalent for analytical OLAP workloads.==

On HackerNoon, it was [once](https://hackernoon.com/what-the-heck-is-duckdb) described as “mutant offspring of SQLite and Redshift”.

As [noted by the MoterDuck team](https://motherduck.com/blog/six-reasons-duckdb-slaps/?utm_source=pocket_saves), as an in-process database, DuckDB is a storage and compute engine that enables developers, data scientists, data engineers and data analysts to power their code with extremely fast analyses using plain SQL. Further, DuckDB has the capability to analyze data where it might live, e.g. on the laptop or in the cloud. Additionally, [DuckDB comes with a simple CLI](https://duckdb.org/docs/api/cli) for quick prototyping — without the need for setup, permissions, creating and managing tables, etc.

Based on reading threads on e.g. HackerNews, Reddit and Twitter, there seems to be a lot to like about DuckDB, e.g.:

- Its performance for analytical workloads on single-node machines seems to be impressive and the setup is pain-free (you can technically start exploring DuckDB within 5 minutes).
- DuckDB is embeddable — like SQLite — and is optimized for analytics. The big deal here is the embeddable part (like a library without bringing in the typical PostgreSQL dependency), eliminating the network latency you usually get when talking to a database.
- DuckDB has also really low deployment effort — \`pip install duckdb\` and you are off to the races.
- Further DuckDB is fast — compared to querying Postgres, [DuckDB is 80X faster](https://www.dataduel.co/revisiting-data-query-speed-with-duckdb/) and when benchmarking other systems we can see [similarly impressive results](https://duckdb.org/2021/08/27/external-sorting.html).

These are some of the reasons DuckDB has [witnessed impressive growth](https://db-engines.com/en/ranking_trend/system/DuckDB) over the past 12 months.

In practice, any CPU can be mobilized to perform powerful analytics via DuckDB. Further, DuckDB is portable and modular, with no external dependencies. In concrete terms, this means that you can run DuckDB on a cloud virtual machine, in a cloud function, in the browser, or on your laptop as mentioned prior.

### Let’s take a step back

In the following section, I’m borrowing heavily [Kojo Osei](https://www.linkedin.com/in/kwosei/) ’s (investor at Matrix Partners) great [blog post from June](https://kojo.blog/duckdb/) about DuckDB.

As Kojo mentions, an emerging category of data warehouses sits at the intersection of analytical queries and embedded deployments. To illustrate why this is so compelling, he catgeorizes databases along two axes:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*xEIbdzo6jkaHOFEE)

Database workload types (image source Kojo Osei )

As visible above and noted by Kojo, current databases are optimized for analytical or transactional workloads. Analytical workloads — also called Online Analytical Processing (OLAP) — are complex queries on historical data. For example, you may want to analyze user signups broken down by demographics such as age and location. On the other hand, transactional workloads — also referred to as Online Transactional Processing (OLTP) — are optimized for quick real-time reads and writes.

Let’s move ahead to deployment types.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*2dPbCrs3NzjUINOX)

Database deployment types (image source Kojo Osei )

As visible above and noted by Kojo, current database technologies are deployed as stand-alone or embedded solutions. Stand-alone databases are typically deployed in a client-server paradigm. The database sits on a centralized server and is queried by a client application. Embedded databases run within the host process of whatever application is accessing the database.

Now some magic. When we merge these two axes we can see an innovation gap! As Kojo underlines, current innovation in OLAP databases has focused on stand-alone OLAP databases such as Snowflake, ClickHouse, and Redshift (don’t know why he left out BigQuery). This has led us to a situation where embedded analytics use cases have been overlooked and underserved. DuckDB is changing this.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*9tH6ZutCbUsocOSQ)

Image source Kojo Osei

### Use cases for DuckDB

Airbyte has [in their glossary](https://glossary.airbyte.com/term/duckdb/?fbclid=IwAR35TXxCxK5cmAVuwzD8lGnTbudO6m8NcK_Kyd4q-0l77uxTB5U8_szLHeY) a short summary of example use cases for DuckDB:

- Ultra-fast analytical use-case locally. E.g., a Taxi example in the [Airbyte glossary](https://glossary.airbyte.com/term/duckdb/?fbclid=IwAR35TXxCxK5cmAVuwzD8lGnTbudO6m8NcK_Kyd4q-0l77uxTB5U8_szLHeY) includes a 10 Year, 1.5 Billion row Taxi data example that still works on a laptop. See benchmarks [here](https://glossary.airbyte.com/term/duckdb/?fbclid=IwAR35TXxCxK5cmAVuwzD8lGnTbudO6m8NcK_Kyd4q-0l77uxTB5U8_szLHeY).
- It can be used as an SQL wrapper with zero copies (on top of parquets in S3).
- Bring your **data to the users** instead of having big roundtrips and latency by doing REST calls. Instead, you can put data inside the client. You can do 60 frames per second as data is where the query is.
- DuckDB on Kubernetes for a zero-copy layer to read S3 in the [Data Lake](https://glossary.airbyte.com/term/data-lake)! Inspired by [this](https://twitter.com/Ubunta/status/1584907743391272961) Tweet. The cheapest and fastest option to get started.

Based on [documentation](https://duckdb.org/docs/), DuckDB should be used when:

- Processing and storing tabular datasets, e.g. from CSV or Parquet files
- Doing interactive data analysis, e.g. joining & aggregate multiple large tables
- Having concurrent large changes, to multiple large tables, e.g. appending rows, adding/removing/updating columns
- Having large result set transfer to client

Based on [documentation](https://duckdb.org/docs/), DuckDB should not be used when:

- Having high-volume transactional use cases (e.g. tracking e-commerce orders)
- Writing to a single database from multiple concurrent processes
- Having large client/server installations for centralized enterprise data warehousing

To learn more about use cases for DuckDB, listen to [this The Data Engineering Podcast episode](https://www.dataengineeringpodcast.com/duckdb-in-process-olap-database-episode-270/) with Hannes Mühleisen, one of the creators of DuckDB (use case discussion starts at ca 14min).

## Final thoughts

There are many database management systems out there. But as [noted](https://duckdb.org/why_duckdb) by the DuckDB creators: there is no one-size-fits-all database system. All take different trade-offs to better adjust to specific use cases. DuckDB is no different.

When you think about selecting a database engine for your project you typically consider options focused on serving multiple concurrent users. Sometimes what you really need is an embedded database that is blazing fast for single-user workloads. Enter DuckDB.

Further, it seems like DuckDB also allows an entire community of SQL enthusiasts to be instantly productive in Python without ever learning more than very basic Pandas. There’s a growing number of data community members who never use Pandas for anything complex anymore because they favor SQL.

[Luis Velasco](https://www.linkedin.com/in/luisvelascouk/) (Data Solution Lead at Google) [summarized well on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:6963501218480431105/) a few months back why he thinks DuckDB is a big deal:

1\. We are living in the great disaggregation of the central data platforms era. The more extreme compute decentralized paradigm I can think of is a grid of laptops. The combo of technology like parquet + pyaArrow with vectorized execution makes it efficient to query large datasets in personal devices.

2\. With increased data literacy and improved coding skills in the vast majority of data workers, insight consumption is far from static — dashboards — but exploratory and self-service. So I envision data analysts accessing data in cloud storage, running embedded analysis locally with duckDB.

3\. SQL is more alive than ever before — period.

4\. Zero deployment effort — \`pip install duckdb\` and you are in

5\. Open Source — There is a vibrant community forming, with support in key pieces like pandas, dbt or apachesuperset, not to mention new startups like DuckDB Labs and MotherDuck

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*nI8qcOJp5kFHFp6ddZZdfQ.png)

==What do you think about the future of DuckDB?==

PS: I recommend watching [this “What is DuckDB” video](https://www.youtube.com/watch?v=vrjDyxWQTJ4&ab_channel=SeattleDataGuy) by The Seattle Data Guy where he discusses together with [Joseph Machado](https://www.linkedin.com/in/josephmachado1991/) (Senior Data Engineer at LinkedIn) about how DuckDB has entered the world of data by storm.

[![Oliver Molander](https://miro.medium.com/v2/resize:fill:96:96/1*W2bKKGQQshg1JU7Z4Mb6pw.png)](https://medium.com/@olivermolander?source=post_page---post_author_info--5d46aaa73196---------------------------------------)

[![Oliver Molander](https://miro.medium.com/v2/resize:fill:128:128/1*W2bKKGQQshg1JU7Z4Mb6pw.png)](https://medium.com/@olivermolander?source=post_page---post_author_info--5d46aaa73196---------------------------------------)

[49 following](https://medium.com/@olivermolander/following?source=post_page---post_author_info--5d46aaa73196---------------------------------------)

Preaching about the realities and possibilities of data and machine learning. Founder & investor.

## Responses (14)

S Parodi

What are your thoughts?  

```c
Awesome write up - really like how you gather so much brains to give enough context
```

5

```c
Another example of the rapid movement in the data ecosystem - great but also in need of some consolidation
```

5

```c
Another database? Not sure why they keep create them. Fast DB. I'd like to see it ingest 100B rows and see how it performs on aggregated queries. CLickhouse and Singlestore are very fast OLAP analytical database, not sure why this DB is trying to compete on a market already flooded.
```

17