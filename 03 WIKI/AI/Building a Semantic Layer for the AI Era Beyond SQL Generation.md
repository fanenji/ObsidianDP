---
title: "Building a Semantic Layer for the AI Era: Beyond SQL Generation"
source: https://blog.dataengineerthings.org/semantic-layer-for-ai-beyond-sql-aae652837a5a
author:
  - "[[Mahdi Karabiben]]"
published: 2025-11-25
created: 2026-04-04
description: In 2022, the semantic layer was just a fancy way to generate SQL for dashboards that didn't really need it. In 2025, it’s the only way to make AI agents actually useful. Here is why we need to stop optimizing for BI and start building for business context.
tags:
  - clippings
  - ai
topic:
type: note
---
[Sitemap](https://blog.dataengineerthings.org/sitemap/sitemap.xml)

[Mastodon](https://me.dm/@mahdiqb)## [Data Engineer Things](https://blog.dataengineerthings.org/?source=post_page---publication_nav-f2ba5b8f6eb3-aae652837a5a---------------------------------------)

[![Data Engineer Things](https://miro.medium.com/v2/resize:fill:76:76/1*HtZXPy85bDrTZm9tMXi6aQ.png)](https://blog.dataengineerthings.org/?source=post_page---post_publication_sidebar-f2ba5b8f6eb3-aae652837a5a---------------------------------------)

Things learned in our data engineering journey and ideas on data and engineering.

Featured

## A guide to capturing the “What, Why, and Who” for Agent functionality

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*2c8Z6-9RN5Bgad6v)

Photo by Joshua Sortino on Unsplash

In 2022, at the peak of the Modern Data Stack craze (R.I.P.), I—like thousands of fellow data folks—was convinced that semantic layers were the final missing piece of the data stack puzzle: The component that would magically create a universal link between data teams’ technical pipelines and actual business use cases.

**The intuition was right:** there was a massive gap in the stack. Business logic and context (metrics definitions, non-technical entity definitions, use cases, etc.) were scattered everywhere, from Google Docs to SQL snippets. A consumer-agnostic semantic layer—not one owned by a BI tool (looking at you, [Looker Modeler](https://cloud.google.com/blog/products/data-analytics/introducing-looker-modeler))—was the ideal home for this context.

The timing, however, was awfully wrong.

In 2022, data teams were building platforms for one main category of use cases: **analytics.** And so, although the theoretical appeal of the semantic layer was logical, I — like many data engineers — struggled to argue for it. Deep down, I knew that outside of niche use cases (like an analyst toying with a metric in a notebook), these definitions and business logic would be used by the BI tool 95% of the time. So, why go through the hassle of adding yet another layer to an already complex stack just to feed a dashboard?

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*MyPhBe77SV4Gz_Q3W3OiDA.png)

Why the push for semantic layers in 2022 was difficult to justify (image by author)

This, fortunately, changed with the advent of LLMs and the new ocean of use cases they brought to the enterprise. In the data space, a collective belief is getting louder: the days of “analytics = looking at charts” are numbered. ==The future consists of AI agents consuming and interacting with data to perform actions and provide recommendations.==

And here is the million-dollar plot twist: **a context-rich semantic layer is the most efficient path to unlocking the power of these new workflows.**

Similar to

[Maxime Beauchemin](https://medium.com/u/9f4d525c99e2?source=post_page---user_mention--aae652837a5a---------------------------------------)

’s era-defining article [*The Rise of the Data Engineer*](https://medium.com/free-code-camp/the-rise-of-the-data-engineer-91be18f1e603) *(2017)*, I think we need a collective reckoning moment to embrace the rise of the semantic layer. But we have to ask: is the 2022-themed YAML really the best we can do for the AI era?

## Why yesterday’s semantic layers are not it

Over the past five years or so, we’ve seen many semantic layer implementations. We’ve had open-source projects like [Cube](https://github.com/cube-js/cube), extensions to existing components like [dbt Metrics](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl), proprietary BI options like [Looker Modeler](https://cloud.google.com/blog/products/data-analytics/introducing-looker-modeler), and Big Tech implementations like Airbnb’s [Minerva](https://medium.com/airbnb-engineering/how-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70).

All these implementations shared one characteristic: their goal was to turn `YAML + Query Context` into `SQL` in an efficient, governed, and centralized manner.

These tools solved the massive headache of metric consistency for dashboards, and I’m not arguing that they’re obsolete or not valuable. But sticking strictly to the above goal traps us in a ‘How’ mindset.

As we move beyond the “Analytics = BI” world and look at tomorrow’s use cases, it becomes clear that the above approach is (very) lacking. LLMs and AI agents are infinitely more capable than BI tools, and limiting their context to “join customers and orders using the `customer_id` column” is an incredible underuse of their capabilities.

Let’s look at a concrete example: **Churn Rate**. In the “Old World” semantic layer, we defined it purely by the math:

```c
# The 2022 Semantic Layer
metric:
  name: churn_rate
  label: "Churn Rate"
  type: ratio
  numerator: lost_customers
  denominator: active_customers
  filters:
    - field: is_test_account
      operator: is
      value: false
```

This tells the machine **how** to calculate a number. But it fails to answer the questions an AI Agent actually cares about when trying to solve a business problem, like *what* the number is or *why* it matters.

A semantic layer for the future needs to capture the rest of the picture (in addition to **The How**):

- **The What:** “Churn is defined as a customer cancelling their subscription or failing to renew within 30 days.”
- **The Why:** “We track this to monitor product health and trigger the following intervention workflows for Customer Success: <intervention\_workflows>”
- **The Who:** “Owned by the Growth Team; primary stakeholder is the VP of Customer Success.”

And perhaps most importantly, the future’s semantic layer needs to acknowledge that this context is **alive:** Business logic is not a stone tablet; instead, definitions change as strategies pivot. We need to shift from viewing the semantic layer as static — a snapshot in time that required an engineering ticket to update — to treating it as a component that evolves at the speed of business, capturing changes in real-time so that AI Agents never make decisions based on expired logic.

With this in mind, is a YAML block of calculation logic really the peak of what we can offer to our AI Agents?

## The semantic layer we (& our AI) deserve

Like with many technologies, optimizing a component for AI requires going back to the drawing board and rethinking the fundamentals. We have to ask a simple question: *What information do AI agents need to unlock their prowess and explore/leverage data in brand new ways?*

The answer is provided above: the *What, Why, Who,* and *How*.

Instead of taking yesterday’s metrics layer and awkwardly adapting it, let’s build a layer that centralizes knowledge across the various dimensions of the business. This new layer needs to pull information from a wide range of sources—from Google Docs and Slack discussions to metric trees, BI dashboards specs, and query history.

It needs to centralize and distill this into a format that Agents can efficiently interact with (a knowledge graph for example) to understand the nuance of the data. This obviously requires significant pre-work, ranging from gathering the information to standardizing metadata across the tangled web of tools that form a typical modern data stack.

## So, where to begin?

The aim here isn’t to push you to go build this theoretical layer in a corner.

I think the best lesson we learned from the Modern Data Stack era is that metadata, like happiness, is only valuable when shared. And it can only be shared across systems if there’s a standard representation for it. My wish is that, as a community, we manage to standardize how we represent the “business context” beyond just SQL snippets.

However, as a data practitioner, there is one major thing you can start doing today: **document, document, document.**

And not just as prep work for some futuristic AI agent; documenting the business context in a centralized and governed manner is the fundamental homework that data teams have neglected for too long. Even if you don’t leverage a semantic layer tomorrow, mapping this context bridges the notorious gap between technical pipelines and business reality. It turns ‘data’ into ‘knowledge,’ which is a universal necessity regardless of the tools you use.

The path from a Google Doc to a standard machine-readable representation is shorter than ever (thanks, LLM gods!), and there is almost no friction regarding the *format* in which you document. What matters is that you start consolidating the context—the what, why, who, and how—so that you are ready for the day the semantic layer we were promised finally sees the light of day — whether it’s an evolution of today’s options or a brand new technology.

*For more data engineering content, you can subscribe to my newsletter, Data Espresso, in which I discuss various topics related to data engineering and technology in general:*## [Data Espresso | Mahdi Karabiben | Substack](https://dataespresso.substack.com/?source=post_page-----aae652837a5a---------------------------------------)

### Data engineering updates and commentary to accompany your afternoon espresso. Click to read Data Espresso, by Mahdi…

dataespresso.substack.com

[View original](https://dataespresso.substack.com/?source=post_page-----aae652837a5a---------------------------------------)

## Responses (8)

S Parodi

What are your thoughts?  

```c
The solution you’re looking for here is an ontology based on RDF/OWL with SHACL definitions. It’ll allow you to document everything relevant to your data model, business rules etc. And it’ll give your AI inference and reasoning options it can use to draw conclusions, map routes etc.
```

10

```c
What resonates here is the shift of business meaning, not just transformations, into the lakehouse itself. We’re doing this now through integrated silver models that carry evolving definitions, ownership, and intent upstream. If that context stays…more
```

10

```c
I think, a data catalog with glossary metric definitions (What) in a natural language or business language which is more natural to LLM, metrics ownerships (Who) and SQL samples attached to the metrics definitions (How) is the right place. Why? is a…more
```

5