---
title: "Scaling Success: The dbt Ecosystem at BlaBlaCar"
source: https://medium.com/blablacar/scaling-success-the-dbt-ecosystem-at-blablacar-c214c4b8f0cb
author:
  - "[[Antoine Lefebvre]]"
published: 2025-09-17
created: 2026-04-04
description: "Scaling Success: The dbt Ecosystem at BlaBlaCar At BlaBlaCar, managing a vast data landscape powering multiple travel marketplaces requires robust and scalable solutions. Imagine managing 4,000 …"
tags:
  - clippings
  - dbt
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)## [BlaBlaCar](https://medium.com/blablacar?source=post_page---publication_nav-26d80095f25c-c214c4b8f0cb---------------------------------------)

[![BlaBlaCar](https://miro.medium.com/v2/resize:fill:76:76/1*dKV0NZOOmgMwsv-tybR1MA.png)](https://medium.com/blablacar?source=post_page---post_publication_sidebar-26d80095f25c-c214c4b8f0cb---------------------------------------)

BlaBlaCar is the world’s leading community-based travel app enabling 29 million members a year to carpool or travel by bus in 21 countries.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*6lduKg0IaGLsltKsKHr9bA.png)

At BlaBlaCar, managing a vast data landscape powering multiple travel marketplaces requires robust and scalable solutions.  
Imagine managing 4,000 tables and 300 reports across multiple business domains. That’s the daily reality at BlaBlaCar, and it’s precisely why our dbt ecosystem isn’t just an advantage, it’s essential.

## The Challenge: Managing Large-Scale Data at BlaBlaCar

BlaBlaCar operates multiple marketplaces, including Carpool, Operated Buses, and Train Marketplace, positioning us as the go-to platform for shared travel. With over 50 data professionals, 5 job families, 7 teams, and a data mesh architecture, we manage over 4,000 tables and 300 reports. This scale necessitates a solid foundation for data transformation and modeling.

### Why dbt at BlaBlaCar?

dbt (data build tool) emerged as a key solution due to its industry standard status, ability to manage dependencies, opinionated framework, and ease of writing transformations. These factors made dbt a perfect fit for our complex data environment.

### Why Tooling Matters

Tooling is foundational to scaling dbt usage, especially when dealing with 45+ data practitioners. Our key objectives for tooling include:

- Streamlining Developer Experience
- Improve productivity
- Ensuring Production stability & governance

The result is a powerful, scalable internal ecosystem that makes dbt safe, fast, and accessible for everyone.

## Key components of our dbt Ecosystem

Our dbt ecosystem is built on several key components related to the different steps of data engineering. Some components are existing tools that we simply integrated into our stack. Some others, we developed internally.

**Defining and organising data models:**

- **dbt Core:** We utilise dbt Core for our data transformations.
- **Multiple dbt Projects:** We maintain multiple dbt projects to manage various data domains.
- **Git Mono Repo:** All our dbt projects are managed within a single Git repository.
- **Document Generator:** Using dbt-osmosis to generate documentation directly from YAML files that live with the code, and to sync columns with assets in BigQuery.

**Testing data models:**

- **Developer Experience:** We enhance developer experience using Visual Studio Code with the dbt-power-user extension.
- **Dev Containers:** Consistent dbt environments using VS Code and Dev Containers. This eliminates “works on my machine” problems and simplifies onboarding.
- **Dev Environment:** Isolated BigQuery datasets for each dbt user using Terraform and upstream\_prod access. This prevents interference between developers and ensures faster development.

**Running data transformations:**

- **Airflow Orchestration:** Airflow is used to orchestrate our dbt workflows.
- **dbtDagGenerator:** This is a tool we developed internally. It generates the dbt tasks that will run in Airflow based on the dbt metadata.
- **Inter-DAG Dependencies:** Sensors are used to manage dependencies between Airflow DAGs.
- **CI/CD Checks:** dbt-dry-run, linting, and tag checks to ensure production readiness and enforce company standards.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ZEhH-oSobHGzRwf1b9_8bA.png)

dbt ecosystem key components

### dbt projects organisations

Here is an overview of how our dbt projects are organised:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*nTtN6Y4-XdTLRw6dlatrQA.png)

dbt projects organisation

Inside our main repository, we have a dbt folder that contains all of our dbt projects. The rest of the repository is mainly the definition of our airflow dags.  
Each data team has its own dbt folder. As we are organised as a data mesh, that also means that each dbt project corresponds to a specific domain.  
Inside each dbt folder, we have the classic dbt folder structure (macros, models, seeds, …) and then inside the model folder, we first have our layers:

- Staging: usually just views on top of the raw data with a bit of cleaning (field name, casting,…)
- Intermediate: these can be either ephemeral models that don’t need to be materialised or intermediate models that are used for several computations in our ELT process.
- Model: this is the main layer where we define our fact tables, dimension tables and marts (though marts can also have their own folder)
- Reporting: this layer is specifically for views that will be used to feed dashboards in BI tools

Optionally, there can be additional subfolders for subdomains to help with the readability and configuration.

In the rest of this article, we’ll deep-dive on the tools that we develop internally.

## dbtDagGenerator Framework

To automate the generation of Airflow DAGs, we developed the dbtDagGenerator framework. There are other solutions available to do so, notably Cosmos, a solution developed by Astronomer. While we did consider this as an option, we felt it was missing some features we wanted to have, the main one being the ability to define sensors in the dbt source configuration so that we automatically have sensors in the dags waiting on either db snapshotting tasks or the execution of dbt models in another DAG (Cross-projects dependencies).

Our framework works as follows:

1. Our CI/CD pipeline builds the dbt project and generates a manifest.
2. The manifest is synchronised with Airflow storage
3. DAGs in Airflow are calling the dbtDagGenerator (Python class), which reads the manifest and programmatically generates tasks in the DAG.
4. Each dbt model/test is transformed into an Airflow task based on the PythonVirtualenvOperator.
5. dbt sources with defined metadata are converted into ExternalTaskSensors or PythonVirtualenvOperator depending on whether the source is a table ingested from an external database or an external table in BigQuery based on a GSheet
6. dbt dependencies ({{ ref }}) are converted into Airflow task dependencies.

Here’s a simple table showing the mapping between dbt elements and Airflow tasks:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*R4oEyHj5WdSFGmGWnq7aXQ.png)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*V41vy5yz6jY2WnhRb2lffQ.png)

## Dev Containers

Dev Containers provide a consistent dbt environment by using VS Code and pre-configured Docker images. This ensures everyone works in the same environment, simplifying onboarding and freeing up local resources.

Concretely, we provide each user with the following setup:

- Python 3.11
- dbt-core & dbt-bigquery v1.9
- dbt Power User extension for VS Code
- SQLFluff for linting
- dbt-osmosis + an abstraction layer (using a VSCode shortcut) to generate the models.yml files in dbt projects.

### Implementation steps

We have asked our users to install the following tools:

- Rancher (or Docker)
- VS Code
- Dev Containers extension in VS Code
- Google Cloud CLI (gcloud)

Then, we defined a devcontainers.json file in a.devcontainer folder. In this file, we have defined all the VS Code extensions but also tools we want to install in the environment like Python, dbt, …

When the user opens the repository in VS Code, a prompt appears to reopen it in the Dev Container:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*PKe7lzgFDO-Gxnw6r2KlvA.png)

And that’s it. VS Code will reopen with all the tools and extensions we have defined in the configuration.

## Power User for dbt

This [extension](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user) for VS Code brings a ton of nice features to make the dbt developer experience smoother. It is possible to buy a license for premium features, but we simply use the free version. It allows us to:

- Run a dbt model from a click directly when editing it.
- Run dbt tests for that model.
- Estimate the BigQuery costs.
- Display the compiled SQL query.
- Preview the results of the query.
- Generate the dbt model yaml description.
- Display the lineage of the dbt model.

## Dev Environment

Our Dev Environment isolates BigQuery datasets using Terraform. Each dbt user has a separate dataset in a dedicated GCP project, preventing interference.

**Implementation details:**

- We have defined the list of users in Terraform.
- We have a Terraform module that then generates a dataset for each user (using a loop) with the appropriate settings and permissions.
- Each user then defined a local environment variable with the dataset\_id.
- ==The environment variable is then used in the Dev dbt profile so that all dbt commands target this dataset by default==.

Additionally, we make use of the dbt package [upstream\_prod](https://hub.getdbt.com/LewisDavies/upstream_prod/latest/) to make it possible to run intermediate models even though the upstream models and sources do not exist in the dev dataset. Without this, running models with dependencies would require running all the upstream models which would prove very costly (we are using BigQuery on-demand pricing model). But using this package, we can read from our production tables and write to the dev dataset. We call this “read from prod/write to dev”. This is dependent on the permissions of the user and is usually limited to the domain the user works on.

## CI/CD Checks

Our CI/CD checks are designed to prevent any code that would break something in production to be released. They include:

- [dbt-dry-run](https://pypi.org/project/dbt-dry-run/) for production readiness, checking for issues like missing columns and permissions.
- Automated code quality checks, including linting.
- Enforcement of company standards, such as mandatory table labels and columns definition.
- Checking that DAGs are able to load correctly within Airflow.

## Documentation Generator

We use dbt-osmosis to generate documentation. Documents are stored in Yaml files alongside the code, making maintenance easier. We can also sync columns with existing BigQuery tables. Here is an example structure of a dbt model documentation:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*UwpV179yDD9krjGa7DbXhg.png)

### What does dbt-osmosis allow us to do?

- We can generate the models.yml file (or update them) based on the columns that are present in the database schema. This requires to have run the model in dev environment if it’s a new model, or you can retrieve from production if it’s an existing model.
- We can propagate column description to downstream models. dbt-osmosis detects the fields that are carried from model to model and copies the description. If it’s a doc block, then it is kept as a doc block.

## Further Reading

For more information, check out the following resources:

- Medium article: [Scaling Success: dbt™ at BlaBlaCar](https://medium.com/blablacar/scaling-success-dbt-at-blablacar-545dd9e9844a)
- YouTube video at Forward Data Conference: [One Thousands and One dbt Models: How BlaBlaCar Moved to dbt in 12 months](https://www.youtube.com/watch?v=HQa6DuoqSv8)
- Medium article: [Data Pipelines Architecture at BlaBlaCar](https://medium.com/blablacar/data-pipelines-architecture-at-blablacar-3ca43403cb39)

[![BlaBlaCar](https://miro.medium.com/v2/resize:fill:96:96/1*dKV0NZOOmgMwsv-tybR1MA.png)](https://medium.com/blablacar?source=post_page---post_publication_info--c214c4b8f0cb---------------------------------------)

[![BlaBlaCar](https://miro.medium.com/v2/resize:fill:128:128/1*dKV0NZOOmgMwsv-tybR1MA.png)](https://medium.com/blablacar?source=post_page---post_publication_info--c214c4b8f0cb---------------------------------------)

[Last published Mar 27, 2026](https://medium.com/blablacar/beyond-the-dashboard-how-blablacar-pms-use-ai-to-self-serve-data-95ccd33ab1f9?source=post_page---post_publication_info--c214c4b8f0cb---------------------------------------)

BlaBlaCar is the world’s leading community-based travel app enabling 29 million members a year to carpool or travel by bus in 21 countries.

[![Antoine Lefebvre](https://miro.medium.com/v2/resize:fill:96:96/1*9d_8_fawHbTCFW3cAOGcpw.jpeg)](https://medium.com/@lefebvre.ant?source=post_page---post_author_info--c214c4b8f0cb---------------------------------------)

[![Antoine Lefebvre](https://miro.medium.com/v2/resize:fill:128:128/1*9d_8_fawHbTCFW3cAOGcpw.jpeg)](https://medium.com/@lefebvre.ant?source=post_page---post_author_info--c214c4b8f0cb---------------------------------------)

[6 following](https://medium.com/@lefebvre.ant/following?source=post_page---post_author_info--c214c4b8f0cb---------------------------------------)

Software Architecture enthusiast in particular towards APIs Design and Data modelling.

## Responses (1)

S Parodi

What are your thoughts?  

==The environment variable is then used in the Dev dbt profile so that all dbt commands target this dataset by default==

```c
Hi! In your architecture, what part of DBT (runtime) is touched by Teraform? In my past projects, I kept Teraform dedicated to platform-level operations (creating datasets/databases, grants etc) but all DBT runtime was separate (ie GitHub Actions or the like).
```