---
title: Why aren’t you using dbt Exposures?
source: https://blog.dataengineerthings.org/why-arent-you-using-dbt-exposures-78b11e15be02
author:
  - "[[Matthew Senick]]"
published: 2025-06-29
created: 2026-04-04
description: Struggling with messy data updates and unknown dashboard dependencies? Learn how dbt exposures simplify lineage, impact analysis, and stakeholder trust.
tags:
  - clippings
  - dbt
topic:
type: note
---
## Skipping Them Is Just Making Your Life Harder

It’s 3:37 p.m. on a Friday. A field in the final layer of your dbt project needs a critical update before the end of the day. Your Slack is buzzing, the product team is waiting on an update to a KPI, and your manager just asked, “How will this change affect all of the dashboards I showed off to the VP yesterday?”

*Cue internal panic.*

You start spelunking through BI tools, tracing semantic dependencies, opening up dashboards, and scrolling through docs last updated in “9 months ago.” It’s a disaster.

Wouldn’t it be nice to just… know where a table or field was being used?

*Enter:* **dbt Exposures,** a documentation feature that sits directly within your dbt project, telling you exactly how dbt models are being referenced in downstream applications of your data warehouse.

### What is a dbt Exposure?

In dbt projects, an *exposure* is a documented reference to the end-use of your data. That dashboard in Looker? That monthly marketing report in Mode? A machine learning model that runs on warehouse data? Those are all exposures.

Think of it like telling your dbt project, “Hey, people actually use this model and here is where it is used.” Suddenly, your models don’t just end at `fct_customer_subscriptions`, they branch into actual business impact.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*KS7gyTEh9T3AqjgWtJJ8Nw.png)

## 4 Reasons You Should Be Using dbt Exposures

## 1\. You Actually Care Where Your Data Ends Up

Be honest, no one builds a model just to admire it in the DAG. Your work ends up in dashboards, slide decks, or wherever your brain can imagine. Exposures make those connections **explicit.**

*Think of Exposures as receipts for your data’s impact and usage.*

Exposures are the language that applications of your data use to tell your dbt project how models are being utilized.

## 2\. A Lineage Graph the Business Cares About

Without exposures, your dbt lineage ends at your final layer. With exposures, you get the full picture. You see exactly the assets that leverage your data, reframing your DAG as a value-added data supply chain.

Once broader data consumers know that you are aware of exactly how they are using the data, they’ll start treating you less like a magical black box and more like a strategic partner who *actually* understands how data impacts them.

Using a tool like dbt Elementary, you’ll even be able to easily quantify the impact of your data on business use cases. Rather than simply providing data to the business, you will also be able to say exactly how much different data is being used.

## 3\. No More “Who Touched the Revenue Model?”

If a dashboard breaks or numbers appear suspicious, every analytics team member is notified and enters resolution mode. Exposures provide you with precise details about what was downstream of the model you are looking to update, including who owns the asset and other critical information.

This turns the classic Slack message:

*“Hey, did someone change something in the revenue model?”*

Into:

*“Hey, I updated the* `*channel_type*` *field in our customer acquisition model. I see it feeds into the Finance dashboard. Want me to update your dashboard formula?"*

Look at you -> proactive, informed, and most importantly, driving the conversation.

## 4\. Guiding Model Review Sessions

Most of us don’t remember what we did last Tuesday, let alone what a model did last quarter. Exposures make it easy to answer questions like:

- “Why did we create this?”
- “Who owns this dashboard?”
- “Is this model still being used?”

They’re also searchable, version-controlled, and right there in your dbt repository.

## How to Actually Use dbt Exposures

Alright, you’re sold. Now what?

Here’s a dead-simple example of a dbt Exposure for a dashboard:

```c
exposures:
  - name: executive_revenue_dashboard
    type: dashboard
    maturity: high
    url: https://looker.yourcompany.com/dashboards/executive_revenue_dashboard
    description: |
      Executive-facing dashboard showing monthly revenue KPIs.
      Used in monthly reviews for business units and end of month
      financial reporting
    depends_on:
      - ref('fct_revenue')
      - ref('dim_date')
    owner:
      name: Joe Analyst
      email: joe.analyst@company.com
```

That’s it. You can do this for dashboards, notebooks, apps, or whatever your heart desires. And the `depends_on` section means your DAG knows exactly which models power that use case. The only item stopping you is your ability to generate these YAML objects. With most modern BI tool API, this should be more than possible!

Pro tip: If you’re using *dbt Cloud*, this all gets visualized in your project, making everyone think you're more organized than you feel.

## Implementation Options

You’ve got choices:

- **Manual**: Write exposures YAML by hand. Simple.
- **Scripted**: Use your BI tool’s API to auto-generate exposure files from dashboards.
- **dbt Cloud Integration**: *dbt Cloud* has a few BI tools ([ex. Tableau](https://docs.getdbt.com/docs/cloud-integrations/downstream-exposures-tableau#set-up-downstream-exposures)) that natively integrate to generate exposures within your project

No matter which path you pick, the payoff is better change management, tighter lineage, and fewer “Oh no, what did I break?” moments.

## So… Why Aren’t You Using Them?

If you’re investing time in building great data models but stopping short of documenting how they’re used, you’re missing the point.

Exposures are one of the cheapest, fastest, most underused ways to make your dbt project not just useful, but **valuable**. They bridge the gap between your SQL and your stakeholders. And once you add them, they’re hard to live without.

So next time your manager asks, “Will this break anything?”, you can say, “Let me check the exposures.”