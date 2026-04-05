---
title: Are You Using Elementary for DBT?
source: https://leo-godin.medium.com/are-you-using-elementary-for-dbt-f9a56ecbef42
author:
  - "[[Leo Godin]]"
published: 2023-09-17
created: 2026-04-04
description: Are You Using Elementary for DBT? Well You Should It’s Elementary Elementary is a dbt package and CLI that provides a lot of infrastructure most of us would need to implement on our own. Project …
tags:
  - clippings
  - dbt
  - observability
topic:
type: note
---
[Sitemap](https://leo-godin.medium.com/sitemap/sitemap.xml)

## Well You Should

### It’s Elementary

Elementary is a dbt package and CLI that provides a lot of infrastructure most of us would need to implement on our own. Project metadata mart? Check. Test-level Slack integration. Yup. Test and run dashboard. You betcha. Think of Elementary as the other stuff needed to maintain a data pipeline. When someone asks, “How do I manage all this stuff?” Channel your inner Sherlock and say, “It’s Elementary my dear.”

Here are some of my favorite features of Elementary.

### Artifact Metadata (Data Mart About Your Dbt Project)

At the heart of Elementary is a data mart containing all the information about your dbt project. If it is a thing in dbt, then Elementary creates a dimension table for it. Models, tests, runs, test results, exposures, metrics, etc. It’s all there, automatically maintained, and included in a single dbt package.

While I’d love to create a tutorial on setting up the Elementary dbt package, it’s unnecessary. Add it to packages.yml, set the DB and schema in dbt\_project.yml, then run “dbt run -s elementary”. That’s it. From there, it just automatically works. Take a look at the [docs](https://docs.elementary-data.com/dbt/dbt-artifacts) to see which artifacts are stored. To pique your curiosity, here is a list.

- dbt\_run\_results
- dbt\_models
- dbt\_tests
- dbt\_sources
- dbt\_exposures
- dbt\_metrics
- dbt\_snapshots

Having this metadata store makes operational tasks trivial. Let’s say I want to see if my model run time is changing significantly. A simple query will tell me. *Even this SQL92-trained data engineer can figure that out.*

```c
with stats as (
    select 
        name as model_name,
        execute_started_at,
        execution_time,
        avg(execution_time) over(partition by name) as mean_execution_time,
        stddev_pop(execution_time) over(partition by name) as stddev_execution_time
    from \`leogodin217-dbt-tutorial\`.enterprise_sales_elementary.model_run_results 
    where name = 'accounts'
)
select 
    model_name,
    execute_started_at,
    (execution_time - mean_execution_time) / stddev_execution_time as stddev_from_mean
from stats 
order by execute_started_at
```
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*8_QFU2rjkobZ18IBPh56Lw.png)

Dbt Model Run Time (Picture from the author)

### Dashboard

The Elementary dashboard provides data faceted over multiple views. Funny story. I never really used the dashboard when first introduced to Elementary. It seemed rudimentary. We would create our own, better, dashboard. *Yeah, of course we would.* Well, as is often the case, a VP was looking at it every day and asking questions I could not answer.

Fast forward a bit, and the Elementary dashboard is the first thing I look at in the morning right after checking Airflow to ensure our nightly jobs ran. The folks at Elementary Data cut all the cruft and provided a dashboard with the most important information needed to monitor a dbt project. Everything is simple and intuitive.

*A Few Dashboard Examples*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*SP1UNVgc74CgESen_Hor3A.png)

Elementary Testing Dashboard (Picture by the author)

Look at this. Latest test results, including the test query and failing rows! This is a game changer when we get to Slack alerts and interacting with business partners.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*CpySsQ43apsSrR-GLXfUcQ.png)

Elementary latest test results (Picture by the author)

Test results over time for a specific model and test

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*rllapfsWqVOtoilS-PBm_Q.png)

Elementary tests resiults over time (Picture by the author)

As you can see, there is quite a lot there and I skipped a couple views. Why create our own dashboard if this one can be created and shared to Azure, Slack or S3 with a simple command. *“edr report”,* by the way.

### Slack Alerts — Tying It All Together

Much of Elementary helps data/analytics engineers manage their dbt pipeline. Slack alerts help you communicate with your team, management and upstream partners. Just like the rest of Elementary’s features, these alerts offer a ton of configurability at the individual test level.

Imagine dealing with account data that is managed by your customer success team. You often find data quality issues when a nightly job runs. Wouldn’t it be great to run data-quality tests on the source data before you run the pipeline. With Elementary, you can run these tests and send results to the Slack channel for customer success. It could include enough information to determine the failing rows and tag key people.

This is what the alert might look like. It’s not perfect, but for such little effort it is pretty darn good. Putting a link to the Elementary dashboard in the description would allow them to see the failed rows in table format.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*EQ6EeZ6w1_D5bgs8sC6MEw.png)

## In Summary

I know. You’re ready for this thing to wrap up. So, instead of writing about every feature, how about just a list of a few more things Elementary does.

- Several different anomaly tests
- Advanced schema tests
- End-to-end pipeline view (Airflow, GitHub Actions, Looker and Tableau)
- Python tests
- Probably more I’ve forgetting about
- Test lineage
- Fantastic support through Slack or GitHub issues..

It’s Elementary my dear. If I had to choose a single dbt package, Elementary would be the clear choice. Combined with the CLI, this tool provides most of what is needed to manage the operational aspects of a dbt pipeline. In short, Elementary makes your life easier with minimal setup and configuration.

[![Leo Godin](https://miro.medium.com/v2/resize:fill:96:96/0*kkwZ8D_UzFGPeDg_.png)](https://leo-godin.medium.com/?source=post_page---post_author_info--f9a56ecbef42---------------------------------------)

[![Leo Godin](https://miro.medium.com/v2/resize:fill:128:128/0*kkwZ8D_UzFGPeDg_.png)](https://leo-godin.medium.com/?source=post_page---post_author_info--f9a56ecbef42---------------------------------------)

[184 following](https://leo-godin.medium.com/following?source=post_page---post_author_info--f9a56ecbef42---------------------------------------)

I’m Leo and I love data! Recovering mansplainer, currently working as a senior data engineer at Shopify. BS in computer science and a MS in data science.