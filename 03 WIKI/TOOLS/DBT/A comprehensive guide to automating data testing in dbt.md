---
title: A comprehensive guide to automating data testing in dbt
source: https://blog.devgenius.io/a-comprehensive-guide-to-automating-data-testing-in-dbt-a1ca8a1d588c
author:
  - "[[NULLIF() - An analytics engineering blog]]"
published: 2024-01-03
created: 2026-04-04
description: A comprehensive guide to managing data quality with dbt tests It’s no surprise that dbt has a long list of capabilities when it comes to data transformations, including; documentation, testing and …
tags:
  - clippings
  - dbt
  - data-quality
topic:
type: note
---
[Sitemap](https://blog.devgenius.io/sitemap/sitemap.xml)## [Dev Genius](https://blog.devgenius.io/?source=post_page---publication_nav-4e2c1156667e-a1ca8a1d588c---------------------------------------)

It’s no surprise that dbt has a long list of capabilities when it comes to data transformations, including; documentation, testing and data quality, deployments and lineage.

Ensuring data quality through testing has always been my favourite part of the analytics engineering role. From a very early point in my career, even when I had not yet integrated dbt as part of my stack, I was always so consumed by data quality, and suggesting improvements to the application that would in turn improve the quality of our data.

![](https://miro.medium.com/v2/resize:fit:1246/format:webp/1*Y8QNokpbifL38gsG4Jt1tg.png)

I have a strong affinity for cats, and data quality!

### Test types

dbt offers various testing types out of the box, including; `not null`, `unique`, `relationships` and `accepted values.`

- not\_null: validates that there are no `null` values present in a column.
- unique: validates that there are no duplicate values present in a column.
- relationships: validates that all of the records in a child table have a corresponding record in a parent table — also referred to as `referential integrity`.
- accepted\_values: validates that all of the values in a column are present in a supplied list of `values`. If any values other than those provided in the list are present, then the test will fail.

When run, dbt builds a `select` query for each test, if these queries return zero rows, the test passes. Check out the [dbt documentation](https://docs.getdbt.com/reference/resource-properties/data-tests) for optional parameters to be used alongside these tests.

In addition to out of the box testing above, there are also data tests. Data tests are SQL queries that live in your `tests/` directory as `.sql` files — that when run should return the failing records. They are also known as `singular` data tests, because they are one-off assertions usable for a single purpose.

Similar to the.sql models, these tests use Jinja in the ref statement of the query. It does so that it can tell dbt which model/source is being tested and thus when to run those tests. Running a `dbt test -m model_name` will run all the out-of-the-box and singular tests attributed to that model. In order to only run the singular data tests for a specific model, you would use the command: `dbt test --select test_type: singular`

### There is no need to reinvent the wheel

The [dbt package hub](https://hub.getdbt.com/) contains a list of useful packages that can be used to amplify the tests run in our project. A few of my favourites are linked below:

- [dbt\_utils](https://hub.getdbt.com/dbt-labs/dbt_utils/latest/): contains a list of SQL generators, Jinja helpers, generic tests, web and introspective macros that can be used to do things like generate a surrogate key, group by, and assert non-accepted values. This package is maintained by dbt Labs. Below is the source code for the generate\_surrogate\_key macro, which is what is run every time we call it in our SQL models.
```c
{%- macro generate_surrogate_key(field_list) -%}
    {{ return(adapter.dispatch('generate_surrogate_key', 'dbt_utils')(field_list)) }}
{% endmacro %}

{%- macro default__generate_surrogate_key(field_list) -%}

{%- if var('surrogate_key_treat_nulls_as_empty_strings', False) -%}
    {%- set default_null_value = "" -%}
{%- else -%}
    {%- set default_null_value = '_dbt_utils_surrogate_key_null_' -%}
{%- endif -%}

{%- set fields = [] -%}

{%- for field in field_list -%}

    {%- do fields.append(
        "coalesce(cast(" ~ field ~ " as " ~ dbt.type_string() ~ "), '" ~ default_null_value  ~"')"
    ) -%}

    {%- if not loop.last %}
        {%- do fields.append("'-'") -%}
    {%- endif -%}

{%- endfor -%}

{{ dbt.hash(dbt.concat(fields)) }}

{%- endmacro -%}
```

Below is an example of when generating a surrogate key would come in handy for models that lack a primary key. Although the example below is *(hopefully)* unlikely, it demonstrates the efficacy for situations where you need to denote a not null and unique key across your entire dataset. Assuming your users table lacked a `user_id` column, you could use the `full_name, gender` and `acquired_at` value to denote the unique key.

```c
WITH 

example_cte AS ( 
  SELECT 
    {{ dbt_utils.generate_surrogate_key(['full_name', 'gender', 'acquired_at']) }} AS surrogate_key, 
    full_name,
    gender,
    acquired_at
  FROM 
      {{ ref('users') }} 
) 

SELECT * FROM example_cte
```

In the.`yml` file for this `users` model, you could then assert that newly created surrogate key was both `unique` and `not_null`. Each time you tested this file, it would run the source code pasted above to ensure that this key passed both tests.

- [dbt\_expectations](https://hub.getdbt.com/calogica/dbt_expectations/latest/): contains a list of tests that `expect` the table, column and/or row values to look a certain way. There are a series of available tests in various categories, but some of my most commonly used are the REGEX pattern matching, as well as the matching data type tests.

While we could easily have reproduced the behind-the-scenes SQL that is being run in our own data warehouse, relying on packages like these allow for increased readability and speed when testing our data and asserting data quality.

### Ok, but why test?

Imagine you have an application that asks for full name, email, date of birth, sex, phone number, and province of residence when you sign-up for an account. The information added to this page upon acquisition will be the data in the users table. The following examples below assume that the application does not use required fields and all the assertions will happen in the backend with the database.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*J_IdpV0abo9p7CY3Otyq1g.png)

Example account sign-up page

**First & Last Names:** it would be fairly difficult to have tests on these two fields other than asserting that they are `not_null`. Given the variance in length and spelling of names, utilizing tests from the packages listed above is likely not going to be possible.

```c
version: 2 

models:
  - name: users  
    columns:
      - name: first_name
        description: The users first name. 
        tests: 
          - not_null
      - name: last_name 
        description: The users last name. 
        tests: 
          - not_null
```

**Email:** an email address is important during registration, because likely your users will have to validate their emails after signing up.  
This means that your email address will likely need to be *unique* (i.e. no other user has registered with that same email), and that the pattern of your email follows that of a *valid* email address which you can assert using the `dbt_expectations.expect_column_values_to_match_regex` test.

```c
version: 2 

models:
  - name: users  
    columns:
      - name: email
        description: The user's email address.
        tests: 
          - not_null
          - unique 
          - dbt_expectations.expect_column_values_to_match_regex: 
              regex: "%__@_%.__%"
```

**Date of Birth:** the input to the date of birth in the photo above is set by DD/MM/YYYY, so the application is expecting it to be in that format, and will only accept it once that format has been fulfilled. The birth date input needs to validate that the registrant is not born in the future, as well as the registrant is not older than a logical year of birth.

```c
version: 2 

models:
  - name: users  
    columns:
      - name: date_of_birth
        description: The user's date of birth. 
        tests: 
          - not_null
          - dbt_expectations.expect_column_values_to_match_regex: 
              regex: "^(0[1-9]|[1-2][0-9]|3[0-1])/(0[1-9]|1[0-2])/(19|20)\d{2}$"
```
```c
-- Singular data test to validate that the date of birth is not in the future
WITH 

assert_birthdate_is_valid AS ( 
  SELECT
    COUNT(*) AS total_users 
  FROM 
    {{ ref('users') }}
  WHERE 
     birth_date > CURRENT_DATE()
  HAVING total_users > 1 
) 

SELECT * FROM assert_birthdate_is_valid
```

**Sex at Birth:** as you can see from the image above, the input for sex at birth is a drop down with a set of standardized values. Whenever we have a set of standardized values, it is recommended to add an `accepted_values` test. This way, if the product ever saves a value that we don’t expect, the test will fail and we will be able to override the buggy data in our `users.sql` model or on the users profile.

```c
version: 2 

models:
  - name: users  
    columns:
      - name: sex_at_birth
        description: The user's sex at birth
        tests: 
          - not_null
          - accepted_values: 
              values: [value_1, value_2, value_3]
```

**Residence:** assuming that only Canadians can register for your application, the residence field on the registration image above should contain yet another standardized list of values. This means that we can utilize the `accepted_values` out-of-the-box test to add the list of Canadian provinces and territories. If the application allowed for Canadian and American registrations, the list of `accepted_values` list would become too long and not add much value. There has to be a trade off for the length of the list of `accepted_values` and the impact it has on the data quality.

```c
version: 2 

models:
  - name: users  
    columns:
      - name: residence 
        description: The user's Canadian residence. 
        tests: 
          - not_null
          - accepted_values: 
              values: [value_1, value_2, value_3, value_4, ... value_13]
```
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*yCg24aGfeHa1t2aWcfwWow.png)

Me after I’ve spent a tremendous amount of time adding high-impact tests to our data sources

Testing enhances the efficacy of user registration data by validating the accuracy and consistency of critical fields such as email, birth date & sex at birth – ensuring data quality and reliability. Its impact lies in providing a systematic and automated approach to early detection of data inconsistencies, fostering confidence among users and analysts while promoting scalability and long-term maintenance of high-quality user information in the data warehouse.

It’s important to note that dbt testing is part of a broader data testing and quality assurance strategy. While it can address certain aspects of data quality, additional measures, such as input validation at the application level, may be necessary to ensure the integrity of user registration information at the source.

**Katherine Chiodo, author of the weekly NULLIF() newsletter  
**Subscribe today! [https://nullifblog.ck.page/subscribenow](https://nullifblog.ck.page/subscribenow)  
Connect on LinkedIn: [https://www.linkedin.com/in/katherine-chiodo](https://www.linkedin.com/in/katherine-chiodo-811693135/)