---
title: "AI That Quacks: Introducing DuckDB-NSQL-7B, A LLM for DuckDB SQL"
source: https://motherduck.com/blog/duckdb-text2sql-llm/
author:
  - "[[MotherDuck]]"
published: 2026-02-09
created: 2026-04-04
description: Our first Text2SQL model release!
tags:
  - clippings
  - duckdb
  - ai
topic:
type: note
---
## AI That Quacks: Introducing DuckDB-NSQL, a LLM for DuckDB SQL

2024/01/25 - 5 min read

BY

## What does a database have to do with AI, anyway?

After a truly new technology arrives, it makes the future a lot harder to predict. The one thing you can be sure of is that you’re probably not going to continue in the same straight line that you’ve been traveling. The truly impactful destinations are often just on the other side of a mountain that you can’t yet see the top of. This is also what makes technology so terrifying: once the mist clears you might find yourself in a totally new landscape without a map.

At MotherDuck, we’re excited about ways that AI can be used to help give people superpowers to understand their data. Someone with access to modern Google search would have looked like a wizard to people just a few decades ago; now we take it for granted that you can instantly settle any bet about how old is Morgan Freeman or when was the last time the Seattle Mariners won the World Series. Similarly, AI has the potential to divide the world into “things you did before AI” and “things you did afterwards.”

It was pretty clear to us that AI was already changing how people interact with their data when one of our early users mentioned they were spending a lot of their time cutting and pasting between ChatGPT and the MotherDuck query UI. That seems super inefficient, and since then we’ve been trying to figure out how to shorten feedback loops and make data practitioners better at their jobs. Any time you have to leave the query you’re writing to check documentation, it distracts you from all of the details you’re keeping track of in your head.

Two weeks ago, in order to help analysts stay focused on their SQL, we [launched “FixIt,”](https://motherduck.com/blog/introducing-fixit-ai-sql-error-fixer/) a feature that can pinpoint which line in your query has an error and suggest a fix. While “FixIt” is pretty simple, it can be surprisingly helpful. Instead of having to look up syntax for things like window functions with trailing averages or timestamp differencing, I can just write the SQL I think should work; if I get the ordering of arguments wrong, misspell something, or use the wrong quote type, “FixIt” will automatically write it correctly.

This week we’re taking the next step; in conjunction with [Numbers Station](https://www.numbersstation.ai/), we’re open sourcing a DuckDB specific text-to-SQL LLM. Our goal here is to give back to the DuckDB community and help seed interesting DuckDB applications. For the moment, we’ve chosen to trade off some expressivity for faster and less expensive inference by using a small-ish model size. If this turns out to be an interesting area we will follow up more.

We hope that you’ll come along with us as we continue to explore the ways that AI can make it easier to solve problems with data.

## About DuckDB-NSQL

We currently provide [text-to-SQL functionality](https://motherduck.com/docs/key-tasks/writing-sql-with-ai/) within MotherDuck, using OpenAI’s most powerful models, that are doing exceptionally well on text-to-SQL [benchmarks](https://yale-lily.github.io/spider) and have been proven useful in practice. We do, however, see a need for more lightweight models that enable DucKDB SQL assistance features at lower latency. Upon reviewing existing open models for text-to-SQL, we came to the realization that existing models and benchmarks primarily focus on analytical queries / SELECT statements.

Beyond fast analytical querying using regular SQL, a significant part of DuckDB's appeal lies in its [friendly SQL](https://duckdb.org/2022/05/04/friendlier-sql.html#group-by-all) syntax, support for [nested types](https://duckdb.org/docs/sql/data_types/overview#nesting), varied [data import](https://duckdb.org/docs/data/overview) options, and its diverse ecosystem of [extensions](https://duckdb.org/docs/stable/extensions/overview). Among others, extensions for querying Postgres, SQLite, and Iceberg tables, and support for JSON and GeoSpatial types.

We believe that text-to-SQL in the context of DuckDB is particularly useful if the model can help users leverage the full power of DuckDB, without having to go forth-and-back between the DuckDB documentation and the SQL shell. We’ve all been there!

With DuckDB-NSQL, we’re now releasing a text-to-SQL model that is aware of all documented features in DuckDB 0.9.2, including official extensions! Think of it as a documentation oracle that always gives you the exact DuckDB SQL query you are looking for.

The model was trained on about 200k synthetically generated and validated DuckDB SQL queries, guided by the DuckDB documentation, and more than 250k general [Text-2-SQL questions from Numbers Station](https://huggingface.co/datasets/NumbersStation/NSText2SQL), which makes the model not only capable of generating handy DuckDB snippets but also to generate SQL queries for answering analytical question.

We fully release the model weights on [Hugging Face](https://huggingface.co/motherduckdb/DuckDB-NSQL-7B-v0.1). and also release the model in a quantized [GGUF format](https://huggingface.co/motherduckdb/DuckDB-NSQL-7B-v0.1-GGUF), for use with llama.cpp.

*Read up more about how we created and evaluated DuckDB-NSQL-7B on [Numbers Station’s blog post](http://www.numbersstation.ai/post/duckdb-nsql-how-to-quack-in-sql)*

## How to use DuckDB-NSQL

The best thing is - You can try it out now on our [Hugging Face space](https://huggingface.co/spaces/motherduckdb/DuckDB-NSQL-7B).!

![Post asset](https://motherduck.com/_next/image/?url=https%3A%2F%2Fmotherduck-com-web-prod.s3.amazonaws.com%2Fassets%2Fimg%2Fdemo_sql_b4d708daed.gif&w=3840&q=75)

Post asset

To get a SQL snippet, simply prompt the model with a natural language instruction that describes what kind of query you want. The more literal the instruction is, the better!

Example 1: *create a new table called tmp from test.csv*

```sql
Copy codeCREATE TABLE tmp AS FROM read_csv_auto('test.csv');
```

Example 2: *get all columns ending with \_amount from taxi table*

```sql
Copy codeSELECT COLUMNS('.*_amount') FROM taxi;
```

Example 3: *get passenger count, trip distance and fare amount from taxi table and order by all of them*

```sql
Copy codeSELECT passenger_count, trip_distance, fare_amount FROM taxi ORDER BY ALL;
```

Example 4: *get longest trip in december 2022*

```sql
Copy codeSELECT MAX(trip_miles) FROM rideshare WHERE request_datetime BETWEEN '2022-12-01' AND '2022-12-31';
```

Thanks [OctoAI](https://octoai.cloud/) for providing us with a fast and scalable demo endpoint.

## Run DuckDB-NSQL locally

If you want to get the fully local experience with llama.cpp head to the [GitHub repo](https://github.com/NumbersStationAI/DuckDB-NSQL) or the [GGUF readme](https://huggingface.co/motherduckdb/DuckDB-NSQL-7B-v0.1-GGUF), you will find all the information you need there!

Have fun!

Start using MotherDuck now!

[Try 7 Days Free](https://motherduck.com/get-started/)