---
title: The Downfall of the Data Engineer
source: https://maximebeauchemin.medium.com/the-downfall-of-the-data-engineer-5bfb701e5d6b
author:
  - "[[Maxime Beauchemin]]"
published: 2017-08-28
created: 2026-04-04
description: The Downfall of the Data Engineer This post follows up on The Rise of the Data Engineer, a recent post that was an attempt at defining data engineering and described how this new role relates to …
tags:
  - clippings
  - architecture
topic:
type: note
---
![](https://miro.medium.com/v2/resize:fit:2596/format:webp/1*K-_ioBR3zz6-5Jcek55Qeg.png)

This post follows up on [The Rise of the Data Engineer](https://medium.freecodecamp.org/the-rise-of-the-data-engineer-91be18f1e603), a recent post that was an attempt at defining **data engineering** and described how this new role relates to historical and modern roles in the data space.

In this post, I want to expose the challenges and risks that cripple data engineers and enumerates the forces that work against this discipline as it goes through its adolescence.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*0DUve9yaXG8_phw9Jt20JA.png)

While the title of this post is sensationalistic and the content quite pessimistic, keep in mind that I strongly believe in data engineering — I needed a strong title that contrasts with my previous article. Understanding and exposing the adversity that the role is facing is a first step towards finding solutions.

Also note that the views expressed here are my own, and are based on observations made while talking to people from dozens of data teams across Silicon Valley. These views are not the views of my employer, or directly related to my current position.

## Boredom & context switching

Watching paint dry is exciting in comparison to writing and maintaining [Extract Transform and Load (ETL)](https://en.wikipedia.org/wiki/Extract,_transform,_load) logic. Most ETL jobs take a long time to execute and errors or issues tend to happen at runtime or are post-runtime assertions. Since the development time to execution time ratio is typically low, being productive means juggling with multiple pipelines at once and inherently doing a lot of **context switching**. By the time one of your 5 running “big data jobs” has finished, you have to get back in the mind space you were in many hours ago and craft your next iteration. Depending on how caffeinated you are, how long it’s been since the last iteration, and how systematic you are, you may fail at restoring the full context in your short term memory. This leads to systemic, stupid errors that waste hours.

When the idle time between iteration cycles is counted in hours, it becomes tempting to work around the clock to keep your “plates spinning”. When 5–10 minutes of work at 11:30pm can save you 2–4 hours the next day, it tends to lead to unhealthy work-life balance.

## Consensus seeking

Whether you think that old-school data warehousing concepts are fading or not, the quest to achieve [conformed dimensions](https://en.wikipedia.org/wiki/Dimension_\(data_warehouse\)#Conformed_dimension) and conformed metrics is as relevant as it ever was. Most of us still hear people saying “single source of truth” every other day. The data warehouse needs to reflect the business, and the business should have clarity on how it thinks about analytics. Conflicting nomenclature and inconsistent data across different namespaces, or “ [data marts](https://en.wikipedia.org/wiki/Data_mart) ” are problematic. If you want to build trust in a way that supports decision-making, you need a minimum of **consistency** and **alignment**. In modern large organizations, where hundred of people are involved in the data generation side of the analytical process, consensus seeking is challenging, when not outright impossible in a timely fashion.

Historically, people used the pejorative term “ [data silo](https://en.wikipedia.org/wiki/Information_silo) ” to designate issues related to heterogenous analytics that would be scattered across platforms or use incompatible referential. Silos naturally spawn into existence as projects get started, teams drift and inevitably as acquisitions occur. It’s the task of the business intelligence (now data engineering) teams to solve these issues with methodologies that enforces consensus, like [Master Data Management](https://en.wikipedia.org/wiki/Master_data_management) (MDM), [data integration](https://en.wikipedia.org/wiki/Data_integration), and an ambitious [data warehousing](https://en.wikipedia.org/wiki/Data_warehouse) program. Nowadays, at modern fast pace companies, the silo problem quickly grows out of proportion, where you could use the term “dark matter” to qualify the result of the expansion of chaos that is taking place. With an army of not-so-qualified people pitching in, the resulting network of pipelines can quickly become chaotic, inconsistent and wasteful. If the data engineer is the “librarian of the data warehouse”, they might feel like their mission is akin to classifying publications in a gigantic recycling plant.

In a world where the dashboard lifecycles are counted in weeks, consensus becomes a background process that can hardly keep up with the rate of change and shifting focus of the business. Traditionalists would suggest starting a [data stewardship](https://en.wikipedia.org/wiki/Data_steward) and ownership program, but at a certain scale and pace, these efforts are a weak force that are no match for the expansion taking place.

## Change Management

Given that useful datasets become widely used and derived in ways that results in large and complex directed acyclic graphs (DAGs) of dependencies, altering logic or source data tends to break and/or invalidate downstream constructs. Downstream nodes like derived datasets, reports, dashboards, services and machine learning models may then need to be altered and/or re-computed to reflect upstream changes. Typically, the metadata around data lineage is usually incomplete or is buried in code that only a select few will have the capacity and patience to read. Upstream changes will inevitably break and invalidate downstream entities in intricate ways. Depending on how your organization values stability over accuracy, change can be scary and that can lead to **pipeline constipation**. If the data engineer’s incentives are geared towards stability, they will learn quickly that best way to not break anything is to not change anything.

Since pipelines are typically large and expensive, adequate unit or integration testing can be expected to be somewhat proportional. The point being: there’s only so much you can validate with sampled data and dry-runs. And if you thought a single environment was more chaos than you could handle, try to stay sane while throwing a dev and staging environment that use intricately different code and data! In my experience, it’s rare to find any sort of decent *dev* or *test* environments in the big data world. In many cases, the best you’ll find are some namespaced “sandboxes” that people use to support whatever undocumented process they see fit.

Data engineering has missed the boat on the “devops movement” and rarely benefit from the sanity and peace-of-mind it provides to modern engineers. They didn’t miss the boat because they didn’t show up, they missed the boat because the ticket was too expensive for their cargo.

## The worst seat at the table

Modern teams move fast, and whether your organization is engineering-driven, PM-driven or design-driven, and whether it wants to think of itself as data-driven, the data engineer won’t be driving much. You have to think of it as an infrastructure role, something that people take for granted and bring their attention to when it’s broken or falling short on its promises.

If there’s a data engineer that is part of the conversation at all, it’s probably to help the data scientists and analysts gathering the data they need. If the data of interest isn’t already available in the structured part of the data warehouse, chances are that the analyst will proceed with a short term solution querying raw data, while the data engineer may help in properly logging and eventually carrying that data into the warehouse. Most likely an answer is required in a timely fashion, and by the time the new dimensions and metrics are backfilled into the warehouse, it’s already old news and everyone has moved on. The analyst will get the glory for the insight, and everyone else may question the need for the slow background process of consolidating this new piece of information in the warehouse.

While “impact” — which implies velocity and disruption — is the most sought after word in employees’ performance review, data engineering is condemned to being a slow background process with little short term impact. Data engineers are many degrees removed from those who are “moving the needle”.

## Operational creep

Operational creep is a hard reality for professions that involve supporting the systems that they build. Q/A teams have largely been replaced by the “you support what you build” motto and most people in the field rally around this idea. This approach is regarded as the proper way to make engineer conscious and responsible for the [technical debt](https://en.wikipedia.org/wiki/Technical_debt) accumulating.

Since data engineering typically comes with a fairly high maintenance burden, operational creep comes fast and disarms engineers faster than you can hire them. Yes, modern tooling help people be more productive, but arguably that’s only machinery that allows pipeline builders to keep more plates spinning at once.

Moreover, operational creep can lead to high employee turnover, which ultimately lead to low quality, inconsistent, unmaintainable messes.

## Real software engineers?

People in the field have heard arguments as to whether data engineers were “real software engineers” or some different class of engineers. In some organization the role is different and may have different \[lower\] salary bands. Casual observation may suggest that the rate of data engineers with a computer science degree may be significantly lower than across software engineering as a whole.

The role, for the reasons depicted in this article, can suffer from a bad reputation that spins that viscous circle.

## But wait — there’s still hope!

Don’t quit just yet! There’s still a huge consensus around data being a key competitive advantage, and companies are investing more than ever in analytics. “Data maturity” follows a predictable growth curve that ultimately leads to the realization that data engineering is extremely important. As you read these words, hundreds of companies are doubling down on their long-term data strategy and investing in data engineering. **The role is alive, growing and well.**

With numerous companies plateauing on their data [ROI](https://en.wikipedia.org/wiki/Return_on_investment) and feeling the frustration of “data operational peak”, it’s inevitable that upcoming innovation will address the pain points described here, and eventually create a new era in data engineering.

One could argue that a possible path forward is de-specialization. If the proper tooling is made available, perhaps simple tasks can be deferred to information workers. Perhaps more complex workloads can become a dimension of common software engineering work, much like what happened to Q/A and release engineers while continuous delivery technologies and methodologies emerged.

In any case, proper tooling and methodology will define the path forward for the role, and I’m hopeful that it is possible to address most of the roots causes leading to the concerns expressed in this post.

I’m planning an upcoming blog post titled “Next generation, data-aware ETL” where I’ll be proposing a design for a new framework that has accessibility and maintainability at its very core. This yet-to-be-built framework would have a set of hard constraints, but in return will provide strong guarantees while enforcing best practices. Stay tuned!