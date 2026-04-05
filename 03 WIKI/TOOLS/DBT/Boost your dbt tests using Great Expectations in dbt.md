---
title: Boost your dbt tests using Great Expectations in dbt
source: https://zoltanctoth.medium.com/boost-your-dbt-tests-using-great-expectations-in-dbt-1c2d33d53fb3
author:
  - "[[Zoltan C. Toth]]"
published: 2022-09-26
created: 2026-04-04
description: Boost your dbt tests using Great Expectations in dbt The Data Build Tool (dbt™) made a hit as the central component of the modern data stack in the past years. It has been gaining traction ever …
tags:
  - clippings
  - dbt
  - data-quality
topic:
type: note
---
[Sitemap](https://zoltanctoth.medium.com/sitemap/sitemap.xml)

[The Data Build Tool (dbt](https://www.getdbt.com/) ™[)](https://www.getdbt.com/) made a hit as the central component of the modern data stack in the past years. It has been gaining traction ever since, and it has done this for a reason: it’s easy to use, doesn’t require any programming skills besides SQL, and is an exceptionally focused tool. It helps you build, run, document, and **test** SQL-based data pipelines. Obviously then, this is a tool that we should learn more about!

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*wZdwhjEGMCNBnNCalprV_Q.png)

dbt’s place in the Modern Data Stack. Source: dbtlabs.com

## dbt Testing Basics

dbt offers three types of tests: singular, generic, and custom generic tests.

### Singular Tests

You implement a singular test in the form of a SQL expression, and as a general rule, they should return the number of failing rows. If a singular test returns zero records, it passes.

Take the example of working with a user table that has an age column. Now, as the oldest person alive is less than [125 years old](https://en.wikipedia.org/wiki/Oldest_people), it’s safe to think of age 125 as a maximum accepted value in the age column of a database table.

Translating this into a singular test would look like this:

```c
SELECT COUNT(*) FROM {{ ref('users') }} WHERE age NOT BETWEEN 0 and 125
```

### Generic tests

dbt supports four [generic test types](https://docs.getdbt.com/docs/building-a-dbt-project/tests#generic-tests): *not\_null, unique, relationships,* and *accepted values.*

These tests are straightforward to implement, as you can add them to the models’ definitions (such as schema.yml).

```c
models:
  - name: dim_listings_cleansed
    description: Cleansed table which contains Airbnb listings.
    columns:
       - name: listing_id
         description: Primary key for the listing
         tests:
           - unique
           - not_null
           - relationships:
              to: ref('listings')
              field: id
```

### Custom Generic Tests

You can convert a singular test into a generic test using the `test` macro. Just put the following code into a file under the `macros` folder, and you’ll be able to use your *age validation test* as a generic test right away:

Now you’ll be able to use `valid_age` as a generic test:

```c
models:
  - name: users
    columns:
       - name: age
         description: User age
         tests:
           - valid_age
```

## Advanced testing with dbt-expectations

dbt-expectations is a dbt package inspired by the Great Expectations project, so let’s cover Great Expectations first.

### Great Expectations

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*1vid2qiAyMCbD30d2Tvo9A.png)

source: Great Expectations on GitHub

Great Expectations is among the most popular open-source projects for data-pipeline testing available today. It supports up to [300 expectation definitions](https://greatexpectations.io/expectations/) (a.k.a. tests). If you want to [look for outliers](https://greatexpectations.io/expectations/expect_column_values_to_not_be_outliers), regulate the [number of values of a categorical variable](https://greatexpectations.io/expectations/expect_column_distinct_values_to_be_in_set), or [test geocoordinates](https://greatexpectations.io/expectations/expect_column_values_to_be_valid_degree_decimal_coordinates), Great Expectations probably has a test for it you can use. Now, many of its tests are available in dbt, too!

### dbt-expectations

[dbt-expectations](https://github.com/calogica/dbt-expectations) — a project inspired by Great Expectations - implement many Great Expectations tests for dbt.

dbt-expectations is extremely simple to install when you want to test your data; add these lines to the `packages.yml` file in your dbt project folder:

Once you’ve set up the project definition, install the package using the following command:

```c
dbt deps
```

When dbt-expectations is installed, you’ll have access to a [plethora of tests](https://github.com/calogica/dbt-expectations#available-tests). Some of the tests I like the most and the ones I cover in my courses are:

- [expect\_column\_values\_to\_match\_regex](https://github.com/calogica/dbt-expectations#expect_column_values_to_match_regex): Validates a value against a regular expression.
- [expect\_column\_values\_to\_be\_within\_n\_stdevs](http://expect_column_values_to_be_within_n_stdevs/): Guards against outliers in a column.
- [expect\_table\_column\_count\_to\_equal\_other\_table](https://github.com/calogica/dbt-expectations#expect_table_column_count_to_equal_other_table): Makes sure that a transformation (like a data cleansing step) doesn’t change the shape of the source table.

### dbt-expectation Tests in Practice

You can use dbt-expectations as generic tests. Some of these tests work on individual columns, such as *expect\_column\_values\_to\_match\_regex*, while some others test whole tables such as *expect\_table\_column\_count\_to\_equal\_other\_table*.

An example of a real-world `models.yml` file I’ve created for my [online dbt course](https://www.udemy.com/course/complete-dbt-data-build-tool-bootcamp-zero-to-hero-learn-dbt/?couponCode=STEEPESTDISCOUNT) will show you how to use these in practice:

## Want to learn more?

Don’t just take my word for it. I obviously think dbt is a fantastic tool and should be used by as many people and companies as possible. So come and check out my course on Udemy called the [Complete dbt (data build tool) Bootcamp: Zero to Hero](https://www.udemy.com/course/complete-dbt-data-build-tool-bootcamp-zero-to-hero-learn-dbt/?couponCode=STEEPESTDISCOUNT)!

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*VEzpQJFa9UVoIqQzKs8diw.png)

A deep dive into dbt-expectations and test debugging

In this course, we start learning dbt from scratch through a real-world example of Airbnb data and go through both the theoretical and practical aspects of dbt, such as:

- models and sources
- slowly changing dimensions
- advanced testing and test debugging
- documentation
- lineages
- and dashboards, to name a few.

**If you sign up through** [**this link**](https://www.udemy.com/course/complete-dbt-data-build-tool-bootcamp-zero-to-hero-learn-dbt/?couponCode=STEEPESTDISCOUNT) **today, you’ll get the largest discount Udemy lets me give to students.**

Happy dbting!

*dbt Mark and the dbt logo are trademarks of dbt Labs, Inc.*

[![Zoltan C. Toth](https://miro.medium.com/v2/resize:fill:96:96/1*JqYL_GJOOwuVtdVK47YCuQ.jpeg)](https://zoltanctoth.medium.com/?source=post_page---post_author_info--1c2d33d53fb3---------------------------------------)

[![Zoltan C. Toth](https://miro.medium.com/v2/resize:fill:128:128/1*JqYL_GJOOwuVtdVK47YCuQ.jpeg)](https://zoltanctoth.medium.com/?source=post_page---post_author_info--1c2d33d53fb3---------------------------------------)

[12 following](https://zoltanctoth.medium.com/following?source=post_page---post_author_info--1c2d33d53fb3---------------------------------------)

Data Engineer, Author, Instructor — Distributed Systems, Databricks, dbt