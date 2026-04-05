---
title: "dltHub: ELT as Python Code"
source: https://dlthub.com/
author:
published:
created: 2026-04-04
description: Write any custom data source, achieve data democracy, modernise legacy systems and reduce cloud costs.
tags:
  - clippings
  - architecture
topic:
type: note
---
## Lightweight Python code to move data

We focus on the needs & constraints of Python-first data platform teams: how to write any data source, achieve data democracy, modernise legacy systems and reduce cloud costs.

##### Trusted By

![](https://cdn.sanity.io/images/nsq559ov/production/6dcf506c00fafe7ba9b1e2e7ec8d5f4b48e35e1c-320x92.png?w=2000&auto=format)

### 10M+

PyPi Downloads

### 8,000+

OSS companies in production

### 600+

Snowflake customers in production

##### OPEN SOURCE

## pip install dlt and go

dlt (data load tool) is the most popular production-ready open source Python library for moving data. It loads data from various and often messy data sources into well-structured, live datasets.

Unlike other non-Python solutions, with dlt library, there's no need to use any backends or containers. We do not replace your data platform, deployments, or security models. Simply import it into your favorite AI code editor, or add it to your Jupyter Notebook. You can load data from any source that produces Python data structures, including APIs, files, databases, and more.

```
import dlt
from dlt.sources.filesystem import filesystem

resource = filesystem(
    bucket_url="s3://example-bucket",
    file_glob="*.csv"
)

pipeline = dlt.pipeline(
    pipeline_name="filesystem_example",
    destination="duckdb",
    dataset_name="filesystem_data",
)

pipeline.run(resource)
```

![An image with the command "pip install "dlt[hub]" in the middle, and logos of REST API sources around it](https://cdn.sanity.io/images/nsq559ov/production/0dc1cafc5f0f7b74e7993f903e7c23227d5edd70-1014x972.png?w=2000&auto=format)

An image with the command "pip install "dlt\[hub\]" in the middle, and logos of REST API sources around it

##### DLTHUB CONTEXT

## Made for LLMs: Data source to Live Reports in Python

**dltHub Context** is a hub of AI-native context assets, including skills, commands, hooks, `AGENT.md`, coding files and more, allowing you and an LLM to code any dlt pipeline from any REST API to any dlt destination - within minutes.  
  
We already support more than [10,100 sources](https://dlthub.com/workspace), and see a clear path toward hundreds of thousands. Go from writing pipeline code to ingesting data and delivering reports via Notebooks, all in one flow, with outputs tailored to data users.

##### DLTHUB VISION

## From Open Source EL to Data Infrastructure That Feels Like Python

dlt makes extracting and loading data simple and Pythonic. With **dltHub**, we’re taking the next step - extending into ELT, storage, and runtime.  
  
dltHub transforms complex data workflows into something any Python developer can run: deploy pipelines, transformations, and notebooks.  
  
We’re building **dltHub** in close collaboration with users in highly regulated industries like finance and healthcare - where governance, security, and compliance (like BCBS 239 for risk reporting) are non-negotiable. dltHub brings those guarantees while preserving Pythonic simplicity, complete data lineage, observability, and quality control - all in a platform that feels as natural as writing code.  
  
Our goal is to make dltHub available to **individual developers, small teams, and enterprises alike.** The first release - **dltHub for individual developers** - is coming in **Q1 2026**.

![{testimonial.author?.name}](https://cdn.sanity.io/images/nsq559ov/production/ffd02636208b8a793d250e3c96127c0ea3c47f3e-152x40.svg?w=400&auto=format)

Julien Chaumond CTO/Co-Founder at Hugging Face

![{testimonial.author?.name}](https://cdn.sanity.io/images/nsq559ov/production/cf0f294252d5cf9762dd5d3f00d6aca7c3cae665-113x40.svg?w=400&auto=format)

Maximilian Eber CPTO & Co-Founder at Taktile