---
title: "DuckDB Postgres Query Engine"
type: conversation
topic: data-platform
created: 2026-02-13
tags:
  - duckdb
  - postgresql
  - gemini
  - tools

---
**Source:** https://aistudio.google.com/u/1/prompts/1Y3aMhvj9NdC1HxhfJSnqggT-4TYVhMLQ

## System Instructions

Optional tone and style instructions for the model

---

### User

the postgres_query in duckdb does use the posgres query engine or the duckdb emgine?

---

### Model

DuckDB's postgres_query Utilizes the DuckDB Engine for Query Processing

When using the postgres_query function within DuckDB, it is the powerful DuckDB query engine that executes the query, not the PostgreSQL engine. This is a key feature of DuckDB's Postgres scanner extension, which is designed to directly query data residing in a PostgreSQL database.

The DuckDB extension for PostgreSQL allows DuckDB to connect to a running PostgreSQL instance and read data directly from its tables.[1][2] Instead of sending the SQL query to PostgreSQL for processing, DuckDB's own vectorized query processing engine reads the PostgreSQL data and computes the results.[3] This direct data access is a core design principle of DuckDB, enabling it to perform analytics on various data sources without the need for data duplication.[3]

The process works through the postgres_scanner extension, which can be installed and loaded in DuckDB.[3] Once attached to a PostgreSQL database, users can execute analytical queries on PostgreSQL tables as if they were native DuckDB tables.[1] The extension leverages PostgreSQL's binary transfer mode to efficiently stream data directly into DuckDB's query engine.[3]

This approach can lead to significant performance improvements for complex analytical OLAP (Online Analytical Processing) queries compared to running them directly on PostgreSQL.[3][4] DuckDB's engine is optimized for such analytical workloads and can parallelize the scanning of PostgreSQL tables to enhance speed.[3]

It is important to distinguish this from pg_duckdb, a separate extension that embeds DuckDB within a PostgreSQL server, allowing PostgreSQL to use the DuckDB engine for certain queries.[5][6] However, when initiating a connection from DuckDB to PostgreSQL using the postgres extension and the postgres_query function, it is unequivocally the DuckDB engine driving the query execution.

---

### User

what if i want to query a postgres table in duckdb using the native postgres functions?

---

### Model

When you query a PostgreSQL table from within DuckDB, the default behavior is for DuckDB's engine to pull the data and process the query. This is powerful for analytical queries but doesn't leverage PostgreSQL's native functions. However, you do have options to execute queries using PostgreSQL's engine directly.

Using postgres_query to Execute Native PostgreSQL Functions

If you want to use functions that are specific to your PostgreSQL database, you can use the postgres_query table function.[1] This function allows you to send a raw SQL query to be executed directly by the PostgreSQL engine. The results are then returned to DuckDB.[1]

Here's how you would use it:

Install and Load the PostgreSQL Extension:
First, ensure you have the postgres extension installed and loaded in DuckDB.

code
SQL
download
content_copy
expand_less
INSTALL postgres;
LOAD postgres;

Attach to your PostgreSQL Database:
You need to create a named attachment to your PostgreSQL database.

code
SQL
download
content_copy
expand_less
ATTACH 'dbname=mydatabase user=myuser password=mypassword' AS pg_db (TYPE postgres);

Use postgres_query:
Now, you can use the postgres_query function to run a query with native PostgreSQL functions.

code
SQL
download
content_copy
expand_less
SELECT * FROM postgres_query('pg_db', 'SELECT my_postgres_function(column_name) FROM my_table');

In this example, my_postgres_function is a function that exists in your PostgreSQL database, and the entire SELECT statement within the single quotes is executed by PostgreSQL.

Pushing Down Operations to PostgreSQL

The DuckDB PostgreSQL scanner has a feature called "pushdown" that can offload certain operations to PostgreSQL.[2][3] This is particularly useful for filtering data at the source before it's transferred to DuckDB, which can significantly reduce the amount of data moved over the network.

You can use the postgres_scan_pushdown table function for this purpose.[2][3] While this allows for pushing down filters (the WHERE clause) and projections (selecting specific columns), it's important to note that it doesn't arbitrarily push down any function to be executed by PostgreSQL.[3][4] The pushdown is generally limited to basic filtering and column selection.

For more complex scenarios that require native PostgreSQL functions, using the postgres_query function is the most direct and reliable method.

Alternative: pg_duckdb for a Different Approach

It's also worth noting the existence of pg_duckdb, which is a PostgreSQL extension that embeds DuckDB inside of PostgreSQL.[5][6] This is the reverse of the scenario discussed above. With pg_duckdb, you can run DuckDB queries from within your PostgreSQL environment, which can be beneficial for accelerating analytical queries directly on your PostgreSQL data.

---
