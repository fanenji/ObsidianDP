---
title: Airflow vs Dagster vs Kestra
source: https://juhache.substack.com/p/data-engineering-orchestration-kestra
author:
  - "[[Julien Hurault]]"
published: 2024-03-13
created: 2026-04-04
description: Ju Data Engineering Weekly - Ep 53
tags:
  - clippings
  - kestra
topic:
type: note
---
### Ju Data Engineering Weekly - Ep 53

After the successful [collaboration](https://juhache.substack.com/p/from-data-engineer-to-yaml-engineer-ed2) with [Benoit Pimpaud](https://open.substack.com/users/23621089-benoit-pimpaud?utm_source=mentions), [Emmanuel](https://www.linkedin.com/in/emmanuel-darras/), CEO of Kestra, reached out to me.

We had an interesting conversation about the state of orchestrators and the features important for Data engineers in their day-to-day projects.

He proposed to support one of my posts, which I gladly accepted, as I've been eager to benchmark various orchestrators for a long time.

I focused on three open-source orchestrators: Airflow, Dagster, and Kestra.

Airflow was chosen as the established orchestrator with the biggest market presence. Dagster is selected for its emphasis on data engineering tasks, and Kestra as the newcomer with its YAML-based declarative orchestration.

This post doesn't aim to choose the best tool, but rather to explore their differences in the data engineering context.

*Note: While this post is sponsored, there have been no influence on the editorial direction.*

## Brief Intro & Semantic

Let's quickly dive into each tool to gain a high-level understanding of their concepts.

Airflow operates as an orchestrator, executing DAGs composed of individual tasks.

![](https://substackcdn.com/image/fetch/$s_!cqWm!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F366c3ee1-058f-44f3-bb10-ca5b08f53654_1608x1080.png)

DAGs and tasks are defined using Python and can be built using a library of predefined operators.

![](https://substackcdn.com/image/fetch/$s_!332h!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2864d502-aaec-46e4-8935-bc461b87524b_1384x258.png)

Example of Airflow DAG

Kestra is also a task-based orchestrator.

![Beyond Storing Data: How to Use DuckDB, MotherDuck and Kestra for ETL](https://substackcdn.com/image/fetch/$s_!FL7E!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7a6e69c-990b-46ba-bd93-bdbe38dae2ce_1080x652.png)

[Beyond Storing Data: How to Use DuckDB, MotherDuck and Kestra for ETL]

In Kestra, DAGs are referred to as "Flows" and consist of a sequence of tasks defined in YAML files and provided either by Kestra core or via plugins.

![](https://substackcdn.com/image/fetch/$s_!RG0K!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F81648e75-c291-473a-bf9b-d8270ef6e29c_1408x1286.png)

[Example of a Kestra Flow]

Dagster approaches orchestration differently.

Instead of viewing the orchestration job as a graph of tasks to execute, Dagster considers it as a graph of “software assets”:

> An **asset** is an object in persistent storage, such as a table, file, or persisted machine learning model.
> 
> A **software-defined asset** is a description, in code, of an asset that should exist and how to produce and update that asset.

Each node of a Dagster dag corresponds to a data object and not to a task.

As for Airflow, Dagster DAGs are defined in Python:

![](https://substackcdn.com/image/fetch/$s_!XBGa!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c58265e-0f46-4ff5-8798-87333bfada60_1350x612.png)

Example of a Dagster asset

## Connectors

It's usually not recommended to run data transformations directly inside the orchestrator.

Instead, the orchestrator should mainly trigger external services like Lambda, ECS Tasks, and Step Functions, which embed the business logic.

In this context, Airflow's history and large community support are hard to beat in terms of the number of connectors supported (at least for now).

For example, consider the list of AWS services supported:

![](https://substackcdn.com/image/fetch/$s_!IhNK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e390732-89a6-4fd9-8fa5-8fa94a51a75b_886x1254.png)

Kestra and Dagster implement only some of them but offer the possibility to fall back to boto3 (Dagster) or AWS CLI (Kestra) if needed.

Kestra distinguishes itself on this topic by providing pipeline blueprints. These blueprints simplify the process of starting new workflows by requiring only the copying and pasting of a YAML file.

![](https://substackcdn.com/image/fetch/$s_!HR1O!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90d762c0-7937-4b68-a128-c52552597b96_1924x998.png)

## Automation

All three platforms can schedule tasks regularly with CRON triggers. However, they offer different advanced automation tools.

### Sensors

Sensors are tasks designed to stop the workflow until something specific happens outside the system: waiting for a queue to empty or a file to appear in a storage service.

Dagster proposes simple Python function decorators where the developer is free to implement his own sensor logic.

![](https://substackcdn.com/image/fetch/$s_!8MhV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7206a68a-374f-4438-9811-7d507ae5cf7c_1320x500.png)

Dagster sensor

Airflow and Kestra go a step further by providing pre-built sensors.

Example of Airflow sensors:

![](https://substackcdn.com/image/fetch/$s_!A2yM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ec1d0b9-b4d6-48b6-aa60-52f516f474c6_1306x646.png)

List of commonly used sensors source

Here's an example of the Kestra S3 Sensor (among others):

![](https://substackcdn.com/image/fetch/$s_!7GP0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52446f05-12ec-4439-b727-322a1a0e2917_814x538.png)

with a special mention for the HTTP sensor:

![](https://substackcdn.com/image/fetch/$s_!4KrM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4811255d-2690-439a-9783-b792facab4b0_1354x1226.png)

Calling an API every 30s until a certain payload value is matched

### Auto-Materialization

Dagster provides a unique feature that automatically materializes assets.

As projects get bigger and workflows get more complicated, it can be difficult to keep track of when a specific dataset will be updated.

Dagster's allows users to define asset-specific auto materialization rules that are reflected to the upstream dependencies automatically.

This can be great for the orchestration of big dbt projects with lots of dependencies and enables rules such as:

- “The events table should always have data from at most 1 hour ago.”
- “By 9 AM, the signups table should contain all of yesterday’s data.”

![](https://substackcdn.com/image/fetch/$s_!sBwW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc838732-fca4-4869-8e20-d4844966f756_1338x568.png)

## Scalability

When selecting an orchestrator, its performance under heavy loads is often overlooked during testing.

For instance, in a project I worked on, we encountered an issue where workers in AWS MWAA (managed Airflow) were lost at a specific scale.

I ran a little test by setting up each orchestrator on my Mac M3 using Docker.

I then executed 100, 500, and 1000 tasks at the same time in each orchestrator and recorded how long the entire process took.

- For Airflow, I created a main DAG that triggered sub-DAGs. Each sub-DAG ran tasks using the PythonOperator to print messages.
	Deployment [doc](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).
- For Dagster, I used the `@op(out=DynamicOut())` feature to run multiple tasks in parallel, each just printing a message.
	Deployment [example](https://github.com/dagster-io/dagster/tree/1.6.9/examples/deploy_docker).
- In Kestra, I used `io.kestra.core.tasks.flows.ForEachItem` for initiating sub-flows, where each sub-flow executes a single print task.
	Deployment [doc](https://kestra.io/docs/installation/docker).

It's crucial to note that I did not fine-tune the setup of each tool; I followed the get-started guide.

The results are as follows:

![](https://substackcdn.com/image/fetch/$s_!9b5k!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faed00a43-7189-4d89-a1ff-54af7c0e9e9b_1202x714.png)

I was surprised by the performance gap.

The difference may arise from Airflow and Dagster being written in Python, while Kestra is developed in Java.

Kestra seems to have greatly optimized its executor, which is useful in data engineering where processing is handled by external workers and not handled inside the orchestrator.

## Dev Experience

Each of these tools approaches the dev experience differently.

Indeed, Airflow and Dagster both offer high-level Python constructs that developers can directly mix with custom Python code. This approach provides a significant amount of freedom, enabling easy customization according to specific project requirements.

However, the risk lies in this flexibility; without strong best practices, projects can become challenging to maintain.

Kestra adopts a different approach by using YAML as the primary user interface and not a scripting language.

While this may make building dynamic behaviors more complex, once you understand how the blocks/plugins are constructed, creating new flows becomes very fast: you are just configuring blocks vs coding / maintaining Python files.

In conclusion, the choice among these three tools depends on what factors weigh more heavily in your decision matrix, as each tool has distinct strengths and focal points:

- Airflow is recognized for its stability and solid community support.
- Dagster is great at handling complex data engineering tasks: freshness-based materialization, dbt DAG parsing and backfilling.
- Kestra distinguishes itself with its YAML approach, which speeds up the development process, and its good scheduling performance.

---

Thanks for reading and special thanks to the Kestra team for the collaboration,

\-Ju

![](https://substackcdn.com/image/fetch/$s_!DpHT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1bc08199-f17c-41b1-8533-5a78ac76ef0b_300x300.png)

*I would be grateful if you could help me to improve this newsletter. Don’t hesitate to share with me what you liked/disliked and the topic you would like to be tackled.*

*P.S. You can reply to this email; it will get to me.*