---
title: Understanding dbt. Monitoring
source: https://mbvyn.medium.com/understanding-dbt-monitoring-2844411093d2
author:
  - "[[Mykola-Bohdan Vynnytskyi]]"
published: 2025-06-22
created: 2026-04-04
description: Understanding dbt. Monitoring Introduction Welcome back to the Understanding dbt series! If you’ve been following along, you already know how dbt helps transform data, manage models, and even track …
tags:
  - clippings
  - dbt
  - monitoring
topic:
type: note
---
[Sitemap](https://mbvyn.medium.com/sitemap/sitemap.xml)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*BTbvO8XeYrOhlF2j)

Photo by Hannes Köttner on Unsplash

## Introduction

Welcome back to the *Understanding dbt* series!

If you’ve been following along, you already know how dbt helps transform data, manage models, and even track historical changes. However, there’s one more superpower every dbt project needs—monitoring.

Think about it: running models is great, but how do you know what succeeded, what failed, and how long things took? And if something breaks at 2 a.m., wouldn’t it be nice to get a Slack alert instead of waking up to confused messages from your team?

In this article, we’ll walk through how to monitor your dbt projects — whether you’re using dbt Cloud or dbt Core, parsing logs, checking artifacts, or setting up custom alerts. We’ll also share tips on best practices and how to make sure nothing slips through the cracks.

Oh — and as always, if you’re prepping for the dbt Analytics Engineering certification, don’t forget to check out the [Udemy practice tests](https://www.udemy.com/course/dbt-analytics-engineering-certification-practice-exam/?couponCode=D9D916A3A36934AAFE4E).

Ready? Let’s dive in.

## Why Monitoring Matters in dbt

Let’s be honest — when everything runs smoothly, we don’t usually think about monitoring. But the moment something fails in production or takes twice as long to run, we suddenly wish we had better visibility.

Monitoring isn’t just about catching failures, though that’s a big part of it. It’s also about understanding performance, data freshness, and reliability over time. Especially in production environments, being able to answer questions like:

- “Did this model run last night?”
- “How long did the transformation take?”
- “Why did this model fail?”
- “Is my data up-to-date?”

…can save your team hours of debugging and (possibly) some panicked Slack messages 😅

Whether you’re working solo or on a larger team, monitoring gives you confidence. It helps you:

- Catch issues early (before stakeholders do),
- Track and optimize model performance,
- Build trust in your data pipelines.

And the good news? dbt gives us the tools to do it, whether you’re using dbt Cloud with built-in dashboards or dbt Core with logs and JSON artifacts.

Let’s explore how it works in both environments, starting with dbt Cloud 👇

## Monitoring in dbt Cloud

If you’re using dbt Cloud, good news: monitoring is built right in. You don’t need to set up anything fancy — head to your dbt Cloud account and you’ll find plenty of helpful insights out of the box.

### Run History Dashboard

Every time a job runs, dbt Cloud logs:

- When the job started and finished
- Which models were executed
- Their status (success, failure, skipped, etc.)
- Execution time per model

This dashboard becomes your single source of truth for model behavior. You can click into any run, drill down into specific models, and even view logs — all from the UI.

### Alerts and Notifications

dbt Cloud lets you hook into:

- **Slack**
- **Email**
- **Webhooks**

You can configure alerts for failed runs, long execution times, or skipped models. This is extremely useful for catching issues early and looping in your team.

### CI/CD Monitoring

If you’re using dbt Cloud’s Continuous Integration feature, every pull request can trigger a test run.

This helps you:

- Catch model issues before they hit production
- Validate schema changes
- See how long new models will take to run

It’s especially handy in larger teams where lots of people are pushing changes.

### dbt Cloud API

For more custom needs, dbt Cloud offers an API. You can fetch run history, job statuses, and even trigger jobs programmatically — perfect for building dashboards or deeper integrations.

Next up, we’ll look at dbt Core, where you get similar insights — but you’ll need to roll up your sleeves a bit more.

Ready?

## Monitoring in dbt Core

If you’re using dbt Core, you don’t get the nice UI dashboards of dbt Cloud — but don’t worry, you still have powerful tools at your disposal.

You just need to know where to look 🔍

### Logs and Artifacts

Every time you run dbt locally or via a scheduler like Airflow or GitHub Actions, dbt generates helpful files inside the target/ folder:

- run\_results.json — details about what ran, status (success, skipped, error), and execution time.
- manifest.json — contains metadata about your project, models, dependencies, and configurations.
- dbt.log — the full log output of your run.

These files are goldmines for monitoring, debugging, and even building dashboards.

### How to Use Them

- **Quick check:** Open run\_results.json to see which models ran, their durations, and status.
- **Troubleshooting:** dbt.log contains detailed tracebacks for errors — great for fixing broken models.
- **Performance:** Sort run\_results.json by execution time to find slow models.
- **Alerts:** You can write a small script to parse run\_results.json and trigger alerts for failed models.

## Using dbt Artifacts for Custom Monitoring

If you want more control over your monitoring — especially when using dbt Core — you can build your own solutions using dbt’s artifacts. These JSON files (like manifest.json and run\_results.json) contain a *lot* of useful metadata.

Let’s break down what you can do with them 👇

### What Are dbt Artifacts?

**manifest.json**

Contains everything about your project — models, macros, sources, dependencies, tags, and configurations.

**run\_results.json**

Generated every time you run dbt. It stores:

- Which models ran
- Their execution status (success, error, skipped)
- Execution time
- Any messages or errors

### Custom Monitoring Dashboards

You can build your own dashboard using:

- Google Data Studio or Tableau
- A simple web app (Flask, Streamlit, etc.)
- Even a Notion page with summaries

Just parse run\_results.json regularly, store the results in a database, and visualize:

- Run durations over time
- Failure rate per model
- Which models fail most often

### Slack Alerts (DIY Style)

You can set up a job (in Python or Airflow or GitHub Actions) that:

1. Parses run\_results.json after every run
2. Checks for failed models
3. Sends a Slack message like:

> *⚠️ dbt run failed*
> 
> *Failed model: stg\_orders*
> 
> *Error: null value in column “order\_id” violates not-null constraint*
> 
> *Duration: 0.4s*

This way, you catch issues *immediately* without waiting for someone to notice broken dashboards later.

### Tools That Can Help

You don’t need a special library. Just use:

- **Python’s json module** for parsing
- **pandas** for data analysis (optional)
- **Airflow, GitHub Actions, or cron jobs** to automate the process

## Best Practices for Monitoring dbt Projects

Whether you’re using dbt Core or dbt Cloud, a strong monitoring strategy will save you time, headaches, and unexpected dashboard disasters.

Here are a few tips to keep your project healthy and observable 👇

### Track Every Run

Always log your runs — whether you’re using dbt Cloud’s Job History or saving run\_results.json and dbt.log in dbt Core. Set up retention or export logic so you can analyze trends over time.

### Monitor Model Performance

Keep an eye on:

- Which models take the longest to run
- Models that frequently fail
- Downstream impacts of failed runs

These help you prioritize refactoring and optimization.

### Build Your Own Checks

Add quality checks as part of your run:

- Use [dbt tests](https://docs.getdbt.com/docs/building-a-dbt-project/tests) (not null, unique, relationships)
- Create custom tests for business logic
- Parse run\_results.json to track test failures over time## [Understanding dbt. Tests](https://mbvyn.medium.com/understanding-dbt-tests-01c1642376a9?source=post_page-----2844411093d2---------------------------------------)

### In this article, we’ll explore one of the most important aspects of working with data — testing

mbvyn.medium.com

[View original](https://mbvyn.medium.com/understanding-dbt-tests-01c1642376a9?source=post_page-----2844411093d2---------------------------------------)

### Set Up Notifications

If you’re using dbt Cloud, configure email or Slack notifications for failed jobs.

If you’re on dbt Core, hook up your scheduler or scripts to alert you when things go wrong — before your BI team starts panicking 😅

### Let Your Team Know

Monitoring is great — but even better when shared. Build a small dashboard or document where others can check the latest run status, broken models, or upcoming changes.

## Conclusion

Monitoring might not be the flashiest part of a dbt project, but it’s one of the most important. Whether you’re building models for a small team or maintaining an entire data platform, knowing when something breaks — and why — can save hours of debugging and protect trust in your data.

In this article, we explored different ways to keep an eye on your dbt projects: from built-in Cloud features and alerting to custom solutions using artifacts like run\_results.json.

The best part? You don’t need fancy tools to get started — just a bit of structure and consistency.

And hey, if you’re preparing for the dbt Analytics Engineering Certification or want to sharpen your skills, I’ve built a [practice test course on Udemy with over 300 questions covering everything from models to tests and monitoring](https://www.udemy.com/course/dbt-analytics-engineering-certification-practice-exam/?couponCode=D9D916A3A36934AAFE4E).  
It’s helped a lot of folks already, and it might help you too.

Thanks for reading — see you in the next article!

[![Mykola-Bohdan Vynnytskyi](https://miro.medium.com/v2/resize:fill:96:96/1*9kkjIEn-SnZHKhvFuoOJlg.jpeg)](https://mbvyn.medium.com/?source=post_page---post_author_info--2844411093d2---------------------------------------)

[![Mykola-Bohdan Vynnytskyi](https://miro.medium.com/v2/resize:fill:128:128/1*9kkjIEn-SnZHKhvFuoOJlg.jpeg)](https://mbvyn.medium.com/?source=post_page---post_author_info--2844411093d2---------------------------------------)

[724 following](https://mbvyn.medium.com/following?source=post_page---post_author_info--2844411093d2---------------------------------------)

Data Engineer by day. Consultant, YouTuber, and course creator by night. I help teams and individuals solve data problems. Creator of the Parquet Reader app.

## Responses (1)

S Parodi

What are your thoughts?  [Christophebeliguieloundou](https://medium.com/@christophebeliguieloundou?source=post_page---post_responses--2844411093d2----0-----------------------------------)

[

Feb 7

](https://medium.com/@christophebeliguieloundou/good-article-f600e59f6aa8?source=post_page---post_responses--2844411093d2----0-----------------------------------)

```c
good article
```