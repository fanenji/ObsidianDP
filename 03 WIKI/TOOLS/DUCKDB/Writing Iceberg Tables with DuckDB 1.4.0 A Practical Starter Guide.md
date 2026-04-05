---
title: "Writing Iceberg Tables with DuckDB 1.4.0: A Practical Starter Guide"
source: https://dwickyferi.medium.com/writing-iceberg-tables-with-duckdb-1-4-0-a-practical-starter-guide-54d6da4c4bce
author:
  - "[[Dwicky Feri]]"
published: 2025-09-17
created: 2026-04-04
description: "Writing Iceberg Tables with DuckDB 1.4.0: A Practical Starter Guide I love tools that let me move fast without a huge setup. DuckDB 1.4.0 is one of those tools when it comes to analytics. The new …"
tags:
  - clippings
  - duckdb
  - iceberg
topic:
type: note
---


![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*-SoS_KBWNZB5euCN5-XrDA.png)

duckdb-writer-iceberg

I love tools that let me move fast without a huge setup. DuckDB 1.4.0 is one of those tools when it comes to analytics. The new Iceberg integration means I can now write open table formats directly from my laptop. This post shares the exact steps I followed to write Iceberg tables with DuckDB and Docker, plus a few things I learned along the way.

## Why DuckDB + Iceberg?

DuckDB is a lightweight database that runs anywhere: command line, Python, or even inside a notebook. Iceberg is an open table format designed for large analytics workloads. Together, they give me a simple way to build tables that work with big data engines like Spark, Flink, and Trino, while keeping the authoring experience friendly.

## What You Need

- Docker and Docker Compose installed
- DuckDB CLI version 1.4.0 (or a notebook with the same version)
- This repository cloned locally

Once everything is in place, open a terminal in the project folder.

## Start the Local Iceberg Stack

I rely on Docker to spin up the Iceberg services (catalog, REST server, etc.).

```c
docker compose up -d
```

When the containers are healthy, DuckDB will be able to connect to the catalog over REST. If you prefer using MinIO as the object store, run:

```c
docker compose -f docker-compose-minio.yml up -d
```

## Run the DuckDB Script

The project ships with \`code.sql\`, a simple script that creates a table, inserts sample rows, and checks the results. Execute it with the DuckDB CLI:

```c
duckdb < code.sql
```

You can fill code.sql with:

```c
INSTALL httpfs; INSTALL iceberg;
LOAD httpfs;  LOAD iceberg;

-- S3/MinIO
CREATE OR REPLACE SECRET minio_s3 (
  TYPE S3,
  KEY_ID  'minioadmin',
  SECRET  'minioadmin',
  ENDPOINT '<minio>:9000',
  URL_STYLE 'path',
  USE_SSL false
);

CREATE OR REPLACE SECRET iceberg_rest (
  TYPE ICEBERG,
  TOKEN 'dummy'
);

-- WAJIB: beri ENDPOINT (REST Catalog)
ATTACH 'icelake' AS icelake (
  TYPE ICEBERG,
  ENDPOINT 'http://<Lakekeeper_catalog>:8181/catalog/',
  SECRET iceberg_rest
);

CREATE SCHEMA IF NOT EXISTS icelake.datalake;

CREATE TABLE icelake.datalake.customer(
  customer_name STRING, customer_address STRING
);

INSERT INTO icelake.datalake.customer VALUES ('Dwicky Feriansyah Putra','Jakarta');
SELECT * FROM icelake.datalake.customer;
```

Behind the scenes, DuckDB loads the \`iceberg\` extension, connects to the catalog from Docker, and writes the table files to the warehouse folder. The script finishes by querying the table so you can confirm the new rows.

You can check full code in:## [GitHub - dwickyfp/duckdb-iceberg-writer: A practical example of using DuckDB to write tables into…](https://github.com/dwickyfp/duckdb-iceberg-writer?source=post_page-----54d6da4c4bce---------------------------------------)

### A practical example of using DuckDB to write tables into Apache Iceberg format. This repository demonstrates how to set…

github.com

[View original](https://github.com/dwickyfp/duckdb-iceberg-writer?source=post_page-----54d6da4c4bce---------------------------------------)

## Conclusion

DuckDB 1.4.0 makes the Iceberg authoring workflow feel approachable. With just Docker and a small SQL script, you get a production-grade table format running locally. If you’re exploring modern data lakehouse patterns, this setup is an easy way to prototype before scaling out.

Happy experimenting! Let me know what you build with DuckDB and Iceberg.

[![Dwicky Feri](https://miro.medium.com/v2/resize:fill:96:96/1*boqgMRa52tt9-dYIi6WQgg@2x.jpeg)](https://dwickyferi.medium.com/?source=post_page---post_author_info--54d6da4c4bce---------------------------------------)

[![Dwicky Feri](https://miro.medium.com/v2/resize:fill:128:128/1*boqgMRa52tt9-dYIi6WQgg@2x.jpeg)](https://dwickyferi.medium.com/?source=post_page---post_author_info--54d6da4c4bce---------------------------------------)

[18 following](https://dwickyferi.medium.com/following?source=post_page---post_author_info--54d6da4c4bce---------------------------------------)

Software Engineer | Python Developer | AI & Big Data | Data Engineer | AI Engineer | Medium Writer