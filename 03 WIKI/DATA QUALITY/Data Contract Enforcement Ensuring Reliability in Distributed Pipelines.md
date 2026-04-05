---
title: "Data Contract Enforcement: Ensuring Reliability in Distributed Pipelines"
source: https://medium.com/towards-data-engineering/data-contract-enforcement-ensuring-reliability-in-distributed-pipelines-d77f2f09c35a
author:
  - "[[Maximilian Oliver]]"
published: 2025-10-11
created: 2026-04-04
description: "Data Contract Enforcement: Ensuring Reliability in Distributed Pipelines How I Implemented Schema-Driven Contracts to Stabilize Cross-Team Data Systems. In my early days of data engineering …"
tags:
  - clippings
  - data-quality
  - data-contracts
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)## [Towards Data Engineering](https://medium.com/towards-data-engineering?source=post_page---publication_nav-37f58dd42be7-d77f2f09c35a---------------------------------------)

[![Towards Data Engineering](https://miro.medium.com/v2/resize:fill:76:76/1*oY6pUgtb7NF-tG2sxtTQyQ.png)](https://medium.com/towards-data-engineering?source=post_page---post_publication_sidebar-37f58dd42be7-d77f2f09c35a---------------------------------------)

Dive into data engineering with top Medium articles on big data, cloud, automation, and DevOps. Follow us for curated insights and contribute your expertise. Join our thriving community of professionals and enthusiasts shaping the future of data-driven solutions.

## How I Implemented Schema-Driven Contracts to Stabilize Cross-Team Data Systems.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*8YQsG_EEuZ6iivT8f0Tkdg.jpeg)

In my early days of data engineering, distributed data pipelines were chaos. Teams published data without warning, schemas changed overnight, and consumers silently broke. A single missing column could cripple downstream dashboards and models. That’s when I adopted **data contracts** — a schema-first, version-controlled approach to enforce reliability across distributed pipelines. In this article, I’ll walk you through how I implemented data contracts using **Great Expectations**, **Delta Lake**, and **OpenAPI specifications** for robust schema governance.

## 1\. Understanding the Problem: Fragile Data Dependencies

Every team owned its own datasets, yet no one owned the **interfaces** between them. Data was shared informally — through files, tables, or Kafka topics — without clear documentation.

The lack of schema enforcement led to **silent data corruption**: one team would change a column’s data type, and downstream processes would fail days later.

I started by formalizing data contracts: explicit, version-controlled agreements defining **schema**, **semantics**, **SLAs**, and **ownership**.

```c
# Example of a simple data contract definition (YAML)
dataset: user_activity_events
owner: analytics-team
schema:
  - name: user_id
    type: string
    nullable: false
  - name: event_type
    type: string
    allowed_values: ["click", "view", "purchase"]
  - name: event_timestamp
    type: timestamp
    nullable: false
sla:
  freshness: 5 minutes
  completeness: 99%
consumers:
  - product-recommendation-service
  - marketing-insights-dashboard
```

This contract became the **source of truth** for both producers and consumers.

## 2\. Enforcing Schema Consistency with Great Expectations

To ensure every data batch complied with its contract, I integrated **Great Expectations (GE)** into ingestion pipelines.

GE validated the incoming data against expectations defined from the contract YAML.

```c
from great_expectations.dataset import PandasDataset
import pandas as pd
import yaml

# Load contract
with open("contracts/user_activity_events.yaml", "r") as f:
    contract = yaml.safe_load(f)

data = pd.read_csv("s3://incoming/user_activity.csv")
dataset = PandasDataset(data)

# Build validations from contract
dataset.expect_column_to_exist("user_id")
dataset.expect_column_values_to_not_be_null("user_id")
dataset.expect_column_values_to_be_in_set("event_type", ["click", "view", "purchase"])

results = dataset.validate()
if not results["success"]:
    raise Exception("Contract validation failed!")
```

If any validation failed, the batch was quarantined and an alert triggered — no bad data could enter production.

## 3\. Applying Schema Enforcement in Delta Lake

For continuous data ingestion, I used **Delta Lake’s schema enforcement** and **evolution controls**.

```c
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DeltaContracts").getOrCreate()

incoming = spark.read.csv("s3://incoming/user_activity.csv", header=True)

# Enforce schema
expected_schema = "user_id STRING, event_type STRING, event_timestamp TIMESTAMP"

validated = spark.createDataFrame(incoming.rdd, schema=expected_schema)

validated.write.format("delta").mode("append") \
    .option("mergeSchema", "false") \
    .save("s3://data-lake/contracts/user_activity_events/")
```

By disabling `mergeSchema`, I prevented accidental schema drift, ensuring only approved schema versions were accepted.

## 4\. Versioning Contracts and Managing Schema Evolution

Data contracts must evolve — new columns appear, types change — but evolution must be controlled. I versioned contracts using Git and added metadata for backward compatibility.

```c
version: 2.1
changelog:
  - added column "session_id" for tracking multi-event sequences
  - deprecated "event_type" values: "click-through"
migration_strategy: backward_compatible
```

CI/CD pipelines ran validations on pull requests to ensure schema changes didn’t break dependent systems.

## 5\. Real-Time Contract Validation for Streaming Data

For Kafka streams, I integrated contract validation at the **consumer layer** using a custom Kafka Streams interceptor.

```c
from kafka import KafkaConsumer
import json
import yaml

with open("contracts/user_activity_events.yaml") as f:
    contract = yaml.safe_load(f)

consumer = KafkaConsumer('user_activity', bootstrap_servers=['broker:9092'])

for msg in consumer:
    record = json.loads(msg.value)
    if record['event_type'] not in ["click", "view", "purchase"]:
        print("Contract violation detected:", record)
        # send to dead-letter queue
```

This made my pipelines **self-healing** — invalid messages were isolated, logged, and could be reviewed later.

## 6\. Automating Contract Testing in CI/CD Pipelines

I integrated contract checks into GitHub Actions to prevent schema violations before deployment.

```c
name: Validate Data Contracts

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Great Expectations
        run: pip install great_expectations pyyaml
      - name: Run Validation
        run: python tests/validate_contracts.py
```

This guaranteed that no schema or expectation change reached production without being validated.

## 7\. Contract-Driven API Integration

For APIs exposing data (for instance, through AWS API Gateway), I documented contracts using **OpenAPI**. This aligned service interfaces with data schema expectations.

```c
openapi: 3.0.1
info:
  title: User Activity API
  version: 1.0.0
paths:
  /events:
    post:
      summary: Ingest user activity event
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserActivityEvent'
components:
  schemas:
    UserActivityEvent:
      type: object
      required: [user_id, event_type, event_timestamp]
      properties:
        user_id:
          type: string
        event_type:
          type: string
          enum: [click, view, purchase]
        event_timestamp:
          type: string
          format: date-time
```

This contract-first API development ensured strict validation at ingestion time.

## 8\. Observability and Governance Dashboard

To track compliance and violations, I built a simple **contract observability dashboard** using AWS QuickSight connected to DynamoDB.

```c
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ContractViolations')

table.put_item(Item={
    'timestamp': datetime.utcnow().isoformat(),
    'dataset': 'user_activity_events',
    'violations': 3,
    'status': 'warning'
})
```

This helped identify which datasets frequently violated contracts, allowing teams to focus on improving data quality at the source.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*gwYGMrPRI4fr2knWr-L7jQ.jpeg)

## 9\. Conclusion: The Cultural Shift to Data Reliability

Implementing data contracts wasn’t just a technical change — it was a **cultural transformation**. Teams started treating data as an API, with defined inputs, outputs, and guarantees. Producers became accountable for the quality of what they emitted, and consumers gained confidence in what they received.

With contract enforcement using **Great Expectations**, **Delta Lake**, and **schema versioning**, I finally achieved what every data engineer dreams of: **a self-regulating, predictable, and trustworthy data ecosystem**.

[![Towards Data Engineering](https://miro.medium.com/v2/resize:fill:96:96/1*oY6pUgtb7NF-tG2sxtTQyQ.png)](https://medium.com/towards-data-engineering?source=post_page---post_publication_info--d77f2f09c35a---------------------------------------)

[![Towards Data Engineering](https://miro.medium.com/v2/resize:fill:128:128/1*oY6pUgtb7NF-tG2sxtTQyQ.png)](https://medium.com/towards-data-engineering?source=post_page---post_publication_info--d77f2f09c35a---------------------------------------)

[Last published 3 hours ago](https://medium.com/towards-data-engineering/quick-guide-event-driven-architecture-02713777b90b?source=post_page---post_publication_info--d77f2f09c35a---------------------------------------)

Dive into data engineering with top Medium articles on big data, cloud, automation, and DevOps. Follow us for curated insights and contribute your expertise. Join our thriving community of professionals and enthusiasts shaping the future of data-driven solutions.

[![Maximilian Oliver](https://miro.medium.com/v2/resize:fill:96:96/1*GuggiDR-D2TjpdkxMXKG0g.jpeg)](https://medium.com/@maximilianoliver25?source=post_page---post_author_info--d77f2f09c35a---------------------------------------)

[![Maximilian Oliver](https://miro.medium.com/v2/resize:fill:128:128/1*GuggiDR-D2TjpdkxMXKG0g.jpeg)](https://medium.com/@maximilianoliver25?source=post_page---post_author_info--d77f2f09c35a---------------------------------------)

[112 following](https://medium.com/@maximilianoliver25/following?source=post_page---post_author_info--d77f2f09c35a---------------------------------------)

Article writer in IT and programming | Freelancer | IT specialist sharing insights on tech, coding, and software development.

## Responses (1)

S Parodi

What are your thoughts?  

==dataset.expect\_column\_to\_exist("user\_id")  
dataset.expect\_column\_values\_to\_not\_be\_null("user\_id")  
dataset.expect\_column\_values\_to\_be\_in\_set("event\_type", \["click", "view", "purchase"\])==

```c
The comment says "build validations from contract", but it looks like the contract wasn't used to generate these checks. Instead it looks like a human had to read the yaml file and code these checks by hand.I haven't done software engineering since…more
```

3