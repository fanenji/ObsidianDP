---
title: Data Pipelines Architecture at BlaBlaCar
source: https://medium.com/blablacar/data-pipelines-architecture-at-blablacar-3ca43403cb39
author:
  - "[[Antoine Lefebvre]]"
published: 2025-01-10
created: 2026-04-04
description: Data Pipelines Architecture at BlaBlaCar Like many tech companies nowadays, BlaBlaCar’s data stack has evolved a lot over the years. New tools are gaining in popularity and rightly so as they bring …
tags:
  - clippings
  - architecture
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)## [BlaBlaCar](https://medium.com/blablacar?source=post_page---publication_nav-26d80095f25c-3ca43403cb39---------------------------------------)

[![BlaBlaCar](https://miro.medium.com/v2/resize:fill:76:76/1*dKV0NZOOmgMwsv-tybR1MA.png)](https://medium.com/blablacar?source=post_page---post_publication_sidebar-26d80095f25c-3ca43403cb39---------------------------------------)

BlaBlaCar is the world’s leading community-based travel app enabling 29 million members a year to carpool or travel by bus in 21 countries.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*7Wrrka3ZFBqLtAP8)

Like many tech companies nowadays, BlaBlaCar’s data stack has evolved a lot over the years. New tools are gaining in popularity and rightly so as they bring better practises and ways of managing data. At BlaBlaCar, our data pipelines have undergone a significant transformation over the last 3 years, adopting a robust software development lifecycle (SDLC). This includes version control for SQL, comprehensive code reviews, and automated testing for all deployments.

While these practices are standard in modern data engineering, they represent a substantial advancement from our processes just a few years ago. We have also greatly invested in the tooling to improve the productivity of our data practitioners.

This article will outline our current data pipeline architecture from end to end. We won’t go into the details of what it used to be or what it might become. This is purely an inventory of the existing architecture.

## Overall Architecture

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*WF6rgdSTc1GlwdMO)

Data pipelines at BlaBlaCar follow a “classic” ELT architecture:

- Data Ingestion utilises a variety of tools. We primarily rely on Google Dataflow for replicating production databases and on Rivery, a SaaS solution, for ingesting data from external APIs. Custom Python scripts handle additional API integrations and Google Sheets ingestion, although this approach is currently being reevaluated for greater efficiency.
- Load is usually also managed by the solution that extracts the data (e.g. Dataflow and Rivery). In some cases, we store the data in GCS first and then load the data in BigQuery with the BigQuery APIs
- Transform: we launch dbt commands from Airflow. This will be detailed further below.

All of these steps are orchestrated through Airflow (Google Cloud Composer). It is at the heart of our ecosystem. We fully rely on Airflow to chain up the different tasks and optimise the runtime of our data pipelines. We have explored alternative options (such as Dagster) but as of today, we think Airflow fits our needs the best (in terms of integrations and scheduling needs). Also migration costs to a different orchestrator would be high.

## Ingestions (Extract and Load)

Our main sources of data are:

- Databases:  
	Relational SQL Databases (production): MariaDB, Postgres, Oracle.  
	Non-relational Databases: BigTable
- External APIs (e.g. Google Ads, Salesforce, Facebook Ads, Zendesk,…)
- Google Sheets
- Google Cloud Storage: JSON or CSV files (static or uploaded/updated daily)
- Kafka Events (tracking events / Domain Events)

## Databases Ingestion

All database ingestions are managed by Dataflow (a managed Google Cloud Service to execute distributed data workflows). We have built custom Dataflow templates to manage the different use cases including custom optimisations and features (e.g. handling encrypted PII Data). The Dataflow jobs are triggered by Airflow. Data teams define the configuration of the snapshotting in the Airflow DAG and decide on the schedule.

To make use of the Dataflow template, we provide a Python library that can be used directly in Airflow. Data teams only need to provide the configuration of the DB and of the tables they want to snapshot.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*fWuCeJFRbLIXs_NH)

Snapshotting Tasks in Airflow

Snapshotting Configuration in Python:

```rb
SNAPSHOTTED_TABLES = [
{
  'cluster_name': 'communication',
  'destination': {
    'bq_project_id': 'prod-bbc',
    'bq_dataset_id': 'snapshot',
    },
  'databases': [
    {
    'db_name': 'communication',
    'tables': [
      {
      'table_name': 'notifications',
      'primary_key': 'id',
      },
  …
      ],
    },
  ],
},
…
# Code that creates the snapshotting Tasks
generate_snapshot_flow(SNAPSHOTTED_TABLES, dag, start, end, env='prod')
```

In summer 2022, we explored using Airbyte instead of building our own tooling. At the time, Airbyte’s performance (referring here to a self hosted version) was not meeting our expectations. This might have changed though and we might re-assess in the future. The main challenge will be to integrate the extra features we require such as handling encrypted PII Data.

## External APIs Ingestion

The majority of our APIs ingestion is done via a SaaS platform called [Rivery](https://rivery.io/). While Rivery has a scheduling feature, we prefer to rely on Airflow to launch the ingestions using the Rivery API. This allows us to create dependencies in Airflow with downstream tasks that are dependent on these ingestions.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*OmwOiLayZNb38we5)

Rivery Interface

Typically, for each ingestion, we have one Airflow task to launch the River (a Rivery job) and then one task to check the completion.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*SzO3Wb4XRPqD2GIW)

Airflow DAG triggering Data ingestion through Rivery

We also have a few legacy Python scripts that extract data from other APIs. These are run by Airflow directly.

## Google Sheets Ingestion

Google Sheets are often ingested in BigQuery either by creating an external table or by loading the data directly into a BigQuery table.

This is done directly in Airflow using Python scripts.

Recently, we have explored using dbt to do so. We use a dbt package called [dbt-external-tables](https://github.com/dbt-labs/dbt-external-tables) to define the Google Sheets as source tables and the package creates them for us. We will gradually roll out this solution as it makes it easier to have everything defined in our dbt projects.

## GCS Files Ingestion

Some partners share files with us on a regular basis through GCS. Most of the time, they have dedicated GCS buckets in which they drop files on a predefined schedule.

Similarly to the Google Sheets ingestion, we can either load the data into BigQuery or create external tables pointing to the files in GCS. The creation of external tables can be done either via dbt (preferred way) or via custom Python scripts (within airflow). Loading data directly into BigQuery is done with Python scripts in Airflow.

Either way, we sometimes have a Sensor Task in Airflow that checks if the files have been uploaded/updated and that waits for the upload to happen.

## Kafka Events Ingestion

There are 3 sources of events today:

- Front End Tracking Events: They are sent from the frontend applications to a HTTP API that produces events in Kafka
- Back End Tracking Events: They are sent from the backend services to another HTTP API that produces events in Kafka
- Other Backend Events: Those are events generated by backend services when there is a change of state to an entity. Events are sent directly to Kafka

We then have a Java application called Freeway that reads from Kafka and streams the event to BigQuery. Freeway validates the schema of the events to avoid any data quality issues. A BigQuery table is created for each type of event and for each version. Our data pipelines can then use those tables as source tables.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*NnpdIOuFCjKtT5Bq)

## Data Transformations

Before Summer 2023, data transformations were managed through SQL queries that were orchestrated in Airflow. The dependencies between these SQL transformations were manually defined in the DAGs and were complex to manage.

In particular, we had one major legacy DAG which contained the majority of the transformations. It became so complex that Data Engineers were not confident in making modifications or trying to simplify it.

Additional transformations that did not have dependencies on the tables in this DAG were then added in separate DAGs and a few dozen extra DAGs were created this way.

We decided to move to dbt to make dependency management easier and to start introducing best practices in the way we develop data pipelines. To know more about our integration with dbt, check out this other article written by [Tushar Bhasin](mailto:tushar.bhasin@blablacar.com): [Scaling Success: dbt™ at BlaBlaCar](https://medium.com/blablacar/scaling-success-dbt-at-blablacar-545dd9e9844a)

Our migration to dbt prioritised speed and minimising disruption to the existing data warehouse. We adopted a one-to-one mapping of Airflow DAGs to dbt projects, allowing us to quickly transition without extensive query rewriting. Consequently, we currently maintain a large number of dbt projects (over 30), varying significantly in size from a single model to over 100. While effective for the initial migration, we are exploring strategies to consolidate and optimise these projects for long-term maintainability.

## Overall Setup

All the code (dbt projects and Airflow DAGs) is stored in a git repository. We have separate folders for the dbt projects and for the Airflow DAGs. We use Airflow to orchestrate the dbt run commands. We have developed a middleware that generates an Airflow DAG based on a dbt project (we call it the dbt DAG generator). It creates a DAG in which there is one task per dbt model. Each task performs a dbt run for that model. We are leveraging the dependencies generated in the dbt manifest file to add the dependencies between the Airflow tasks. Hence the lineage in Airflow is the same as the one in dbt. We are therefore able to visualise that lineage in Airflow but we also benefit from the additional capabilities from Airflow: retry mechanism, backfill, UI (lineage visualisation), code in Python (ability to customise), etc…

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*WLJoHK5jmWvmu76h)

*Example of dbt DAG in Airflow*

The development flow is as follows:

1. Data Engineers / Data Analysts get the latest version of the code from GitHub (git pull)
2. They modify / create models in the dbt projects folder
3. They test locally (this will be described in a later section) their modifications
4. In case of a new dbt project, they create an Airflow DAG using our dbt DAG generator python library (this will be described in a later section)
5. They push their code to git. A Pull Request is opened.
6. When the PR is merged, a CI/CD process synchronises the code with our Airflow instance.
7. The updated data pipeline is then executed at the next scheduled time.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*rfpRUTbca6cy4HwY)

In BigQuery, the data is organised in various datasets. We are organised as a Data Mesh with various functional domains. For each domain we usually have 3 or 4 datasets including:

- a staging layer where the data ingested lands
- an intermediate layer when we have data transformations that are not meant to be exposed to other domains
- a model layer where we have tables that not specific to a given use case (usually fact and dimension tables)
- A mart/reporting layer that contains tables specific to a use case (usually aggregated data) or that feeds a Dashboard.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*h1fTSIdYZ8ss7bx_)

## Feature Store Pipelines

To support ML use cases, and more specifically inference in production services, we developed a feature store which is an object store designed to ingest data and then serve it with low latency through an HTTP API.

Our feature store, ingests data from domain events (streaming) and the data warehouse (batch) to create states (business entities like users or trips) and feature sets (combinations of states used for machine learning models). Feature ingestion pipelines allow for the addition of new features (directly from domain events) and client-defined features (CDFs) which may involve external computations. These pipelines handle both batch and streaming data, including backfilling, and apply encodings to feature values. Feature serving offers both batch (high-throughput) and online (low-latency) access though the latter is the most commonly used.

Our feature store is backed by BigTable which offers many interesting features such as values historicization and low latency. The application itself is a JAVA application with 2 main components:

- State Builder: it is in charge of processing incoming streaming events, extracting data from them and then storing the data (potentially transformed) in BigTable
- Serve: this is the API that allows applications to retrieve the states and feature sets data.

## Reverse ETLs

Once we have processed data into our data warehouse, we have several outgoing pipelines that serve the following functions:

- Share data with external partners. For example, we send calculated customer attributes to our CRM system to be able to send target marketing emails
- Provide calculated metrics to internal and external systems. For example, Engineering teams can compute business metrics (like conversion rate) and track them in Datadog.
- Provide data to production systems. For example, we compute the driver cancellation rates to optimise our search results.

To run these Reverse ETL pipelines we rely on different technologies:

- DataFlow: We use DataFlow to copy data from BigQuery to other databases such as PostgreSQL and Redis. For now, we mainly use Batch DataFlow jobs. That means we schedule at regular intervals (once a day in most cases) DataFlow jobs that copy the data from BigQuery. We also have a couple of streaming jobs for recent use cases.
- Share files through GCS
- Share reports via Google Sheets
- SFTP (orchestrated through Airflow): We use SFTP to send files to some of our external partners
- SFTP server backed by GCS: We drop files in a GCS bucket and external partners connected through SFTP to access the files from GCS
- Direct Connection to BigQuery: Some production services are directly connected to BigQuery with the corresponding Client (Java mainly). We either provide them with a Service Account or we configure the access for their Service Account if they already have one.
- Webhooks: We build payloads based on BigQuery results and push to a HTTP API.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*xfdLq0YCaW093jGR)

## Further Applications

This well-structured data architecture opens doors to a multitude of data applications. For example, the rich data stored in BigQuery can be leveraged for data visualisation, providing insights into user behaviour, market trends, and platform performance. At BlaBlaCar, our main visualisation tool is Tableau. We also use Looker Studio and Google Sheets for more ad-hoc needs.

We perform a lot of analyses either directly in the BigQuery UI or through Python Notebooks. We recently explored new solutions like Count or Hex and we might consider adding such a solution to our data stack in the future.

Furthermore, this warehouse data serves as the perfect training ground for machine learning models. Current use cases include personalised recommendations, fraud detection, and dynamic pricing optimization, all contributing to an enhanced user experience and business growth.

As BlaBlaCar continues to refine and expand its data capabilities, the possibilities for data-driven innovation are ever growing.

## Conclusion

BlaBlaCar’s data pipeline architecture, as detailed above, has undergone significant evolution, embracing modern data engineering principles (often “stolen” from the Software Engineers practices’) like version control, testing, and CI/CD. This robust ELT framework, orchestrated by Airflow and powered by tools like dbt or Dataflow, enables efficient data ingestion, transformation, and loading from diverse sources.

The Data Mesh approach, focusing on data products and domain-specific data squads, promotes data quality, consistency, and reusability. This foundation not only supports current data operations but also lays the groundwork for future expansion into areas like real-time data processing and advanced analytics.

## What next?

Like many Modern Data Stacks, our architecture is complex and composed of various moving parts. We will need to continue investing in Monitoring and Data Quality. This will go, as an example, through the implementation of dbt tests which are almost non-existent today. With the growth of the number of data products that we maintain, we will need to add SLOs to track the health of these data products. Finally, with an ever-growing amount of data ingested, we will need to continue our efforts to reduce the amount of data processed and the number of data assets that we create. This is how we will stay sustainable as a data organisation.

*Thanks to Albert Konrad, David Witkowski, Jean-Baptiste Even and* [*Thomas Pocreau*](https://medium.com/@thomasPoc) *for their review and feedback.*

[![BlaBlaCar](https://miro.medium.com/v2/resize:fill:96:96/1*dKV0NZOOmgMwsv-tybR1MA.png)](https://medium.com/blablacar?source=post_page---post_publication_info--3ca43403cb39---------------------------------------)

[![BlaBlaCar](https://miro.medium.com/v2/resize:fill:128:128/1*dKV0NZOOmgMwsv-tybR1MA.png)](https://medium.com/blablacar?source=post_page---post_publication_info--3ca43403cb39---------------------------------------)

[Last published Mar 27, 2026](https://medium.com/blablacar/beyond-the-dashboard-how-blablacar-pms-use-ai-to-self-serve-data-95ccd33ab1f9?source=post_page---post_publication_info--3ca43403cb39---------------------------------------)

BlaBlaCar is the world’s leading community-based travel app enabling 29 million members a year to carpool or travel by bus in 21 countries.

[![Antoine Lefebvre](https://miro.medium.com/v2/resize:fill:96:96/1*9d_8_fawHbTCFW3cAOGcpw.jpeg)](https://medium.com/@lefebvre.ant?source=post_page---post_author_info--3ca43403cb39---------------------------------------)

[![Antoine Lefebvre](https://miro.medium.com/v2/resize:fill:128:128/1*9d_8_fawHbTCFW3cAOGcpw.jpeg)](https://medium.com/@lefebvre.ant?source=post_page---post_author_info--3ca43403cb39---------------------------------------)

[6 following](https://medium.com/@lefebvre.ant/following?source=post_page---post_author_info--3ca43403cb39---------------------------------------)

Software Architecture enthusiast in particular towards APIs Design and Data modelling.