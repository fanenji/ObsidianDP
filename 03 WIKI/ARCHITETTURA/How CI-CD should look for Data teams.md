---
title: "Principles of effective data delivery: How CI/CD should look for Data teams (Miniseries Part 3)"
source: https://medium.com/orchestras-data-release-pipeline-blog/principles-of-effective-data-delivery-how-ci-cd-should-look-for-data-teams-miniseries-part-3-396deb5af97a
author:
  - "[[Hugo Lu]]"
published: 2023-08-23
created: 2026-04-04
description: "Principles of effective data delivery: How CI/CD should look for Data teams (Miniseries Part 3) Data Teams have grown exponentially over the last 5 years, but there is little consensus in terms of …"
tags:
  - clippings
  - ci-cd
  - processo
topic:
type: note
---
![](https://miro.medium.com/v2/resize:fit:4800/format:webp/1*eDsMOOGpCH6ivEGV7X3zrw.jpeg)

Data is moving to its next stage of maturity: consensus around principles of effective data delivery. Photo by Suzanne D. Williams on Unsplash

In the [last two parts](https://medium.com/orchestras-data-release-pipeline-blog/how-ci-cd-works-for-data-science-pipelines-miniseries-part-2-70f3c184c131) of this miniseries, we took a look at the principles underpinning continuous integration and continuous development, and how they impact software engineering and machine learning engineering processes.

We saw the fundamental goal of each team is important in determining the practical steps that constitute best practice in CI/CD for both software engineering and machine learning engineering. Areas of similarity include the use of test-driven development, co-pilots, git control for code, and separated environments for staging and production.

However there are differences too. Machine Learning engineers do not just ship code, but are responsible for deploying machine learning models reliably and efficiently into production. This means additional services are required to adequately monitor machine learning models (and their outputs) in order to continuously monitor the efficacy and reliability of deployed models. Furthermore, the wide variety of use-cases inherent to machine learning engineering mean implementation detail is rarely the same for different companies.

We can therefore make (and test) a few assumptions regarding how CI/CD for Data teams should look:

**1\. The fundamental principles of CI/CD in software engineering should apply to any code Data Teams write and maintain**

**2\. If data teams have different use-cases, we should expect the implementation detail to differ as well**

**3\. Data teams may need additional tools to achieve best-practice if they are responsible for more than simply shipping code**

A guiding principle of [Orchestra](https://getorchestra.io/) is that Data teams are responsible for more than shipping code. Data teams ship *data*. This can be considered an object such as a file or table that is available for use by other parts of the business via a store such as a data lake or data warehouse. This definition is beneficial as it does not restrict the data team’s responsibility for a data source to a specific location. For example, if the data team uses a data warehouse to clean customer data and returns this customer data to a CRM, then the state of the data in the CRM can also be the responsibility of the data team.

Furthermore, data teams are responsible for supporting resources. These may include docs, dashboards, and alerting systems that monitor data quality. We do not include these responsibilities in the study since there is little evidence to support that such resources significantly benefit from version control (and hence, CI/CD).

Data teams’ key responsibilities

1\. Data teams are responsible for deploying code reliably and efficiently that facilitates the ingestion, transformation, and serving of data

2\. Data teams are responsible for the state of data objects or assets in data sources such as data warehouses or data lakes

We’ve so far established some assumptions regarding what measures and tools data teams should use to achieve best practice. We’ve also defined the key responsibilities of a data team, and how they differ from software engineering or data science teams. Before diving into the implementation detail, we can examine the findings we’ve collated from speaking to hundreds of data teams that underpin best practice CI/CD in data.

## Principles of CI/CD principles in data

Rather than reinvent the wheel, we can draw heavily on the findings of Accelerate to structure how we think about the “Key capabilities” data teams should have in order to be high performing. The authors of accelerate divided these into categories:

1. **Continuous Delivery**
2. **Architecture**
3. **Product and process**
4. **Lean management and monitoring**
5. **Cultural**

We focus on (1) and (2). While it would make sense to spend more time on 3–5, we acknowledge that the authors of Accelerate surveyed thousands of respondents, whereas our knowledge of less tangible characteristics of successful data teams is far more anecdotal (for now).

After speaking to hundreds of data teams, the data suggests that high-performing data teams show the following characteristics *with respect to the management of Data* (we do not repeat the 24 characteristics here in the context of maintaining software to avoid simply regurgitating Accelerate).

**Continuous Delivery**

1. **Store raw data in partitions and version control the code that results in the materialisation of data**. Storing raw data in partitions can be thought of as version control, as any given period’s data is separated into its own object store. Accessing data for a given period and all those prior i.e. a version is easily achievable when raw data is stored in partitions. In order to be able to access different versions of materialised data i.e. now raw, the code that generates that data ought to be version controlled. This code in its simplest form would be a repository of SQL files.
2. **Automate your deployment process**; deployment in this context is the extent to which changes to data in production environments do not require manual intervention. Teams use a data release pipeline, which should consist of a data transformation, data orchestration tool with observability at minimum
3. **Implement continuous integration**: code should trigger the ephemeral materialisation of data assets on which all tests are run quickly to discover serious regressions which developers fix immediately. This is why specifying data schema is so important, since it allows quick testing of data as there is a standard or expectation to test it against.
4. **Use trunk-based development methods**: Characterised by fewer than three active branches in a code repository. We have not validated this but it feels intuitive that no more than three active branches would be positive for large data teams with analysts working on different sets of data; the data may even be lower since sql repositories are more likely to have files that are “bottlenecks” i.e. have multiple dependencies, which increases the likelihood branches are conflicting
5. **Implement test automation** ***efficiently***; data tests should be run continuously and only pass where the data is releasable. We add “efficiently” since a simple way to achieve this is to run all data tests on vast production replica datasets on any commit to a main branch; this would not constitute best practice and is likely to be prohibitively expensive for data teams when data volumes become large.
6. **Clone data into production**; *(6) in Accelerate is to ensure “Test Data Management”, as software systems require data in order to facilitate tests. Testing data does not require any additional data, however what is required is the ability to clone data into production.* The staging environment(s) can be thought of as a test data suite, where changes in code can be reflected in ephemeral data tables that are subsequently tested for quality. When these quality checks pass, this data should be flat cloned into production, ensuring that what is in production always reflects data of sufficient quality. There are fewer variables between staging and production environments with data than in software (you cannot parameterise a data table) which makes this a robust an efficient solution
7. **Shift left on security**: *This is an area data teams have historically overlooked. It is non-trivial to ensure that data infrastructure conforms to security standards. Even ensuring third party applications are network segregated is no easy task. This is compounded by the fact that data teams typically use 8–12 separate tools to release data into production. Assessing security requirements before building infrastructure is advisable.*
8. **Implement continuous delivery**; the data should be in a deployable state throughout its lifecycle. In addition to ensuring that data in production passes quality checks, in data we see this has important implications for Business Intelligence and Application management — if a team uses a semantic layer which is housed in a separate repo to sql files, there is a risk underlying tables changes but the semantic layer does not, which could lead to a loss in continuous delivery (users’ queries on the data via a BI tool fail). Implementing continuous delivery is therefore non-trivial in data as well, due to how it is served to consumers.

8b) Ensure state is available: data consumers may not necessarily be business users in a BI context. Indeed, in large organisations it is common for one team to be responsible for data in the data lake and another for data in a warehouse. In order for these teams to operate effectively, upstream data producers must not only deliver the data continuously but also deliver its state continuously. This means allowing downstream consumers to infer the state of the data, either by querying a resource directly or by querying the data. For example, downstream consumers should query the upstream producer’s latest job status to ensure clean data is being consumed, or they could agree data sources are consumable if a set of data quality checks pass.

**Architecture capabilities**

1. “Build loosely coupled architecture” is what is included in “Accelerate”. We propose: **Build the architecture for the job**. Software organisations benefit from loosely couple architectures because of their size but also the way they communicate (typically in real-time via HTTP or queues). Data teams can resemble these in large organisations, but sometimes benefit from more monolithic or tightly coupled architectures as these enable teams to move more quickly and are easier to orchestrate. This heterogeneity justifies loosely coupled or tightly coupled data architecture depending on individual circumstances
2. **Architect for empowered teams**; let data teams choose what they want to use, subject to cost — *Editor’s note: if I didn’t have faith in my data team to pick good tools, I would probably ask a software engineer to do something first. This has the advantage of ensuring there is communication between software teams or data producers when a data team does eventually get employed and data consumers i.e. data teams. This is critical and doing this often results in nice, event-based systems where expensive data ingestion tools are not needed.*

10b) Model data using a framework: data should be modelled using an established framework e.g. medallion, facts and measures, datavault etc.

10c) Model data sparingly: the less data models are used, the better, as this improves cost and promotes simplicity

**Product and process capabilities**

1. Gather and implement stakeholder feedback: understand what business users want
2. Make the flow of work visible through a value stream: w *e have not really seen much anecdotal evidence to support this, but it is included for completeness*
3. Work in small batches: implementing an agile approach to iterating on data is valuable. Data teams can work extremely well when tasks are forced to be specced out.
4. Allow data teams some creative agency; often data teams are required to translate the needs of stakeholders into code. Data teams should have the creative agency to choose how the needs of stakeholders are met.

**Lean Management and monitoring capabilities**

1. **Have a lightweight change approval process**: *limited anecdotal evidence to support*
2. **Monitor health across application and infrastructure to inform business decisions**: *limited anecdotal evidence to support*
3. **Check system health proactively**; in the context of the data itself, this could relate to data quality checks, however **with** robust orchestration it is almost redundant if data is being cloned effectively from staging to production. Data should be available, so tests can be implemented to ensure query speeds on warehouses are not too long, that data is not null in applications, and the like. Non-deployment-critical data quality tests would also fall into this category. The distinction between non-deployment-critical and deployment-critical data quality tests is imperative to understand. Software can be affected by exogenous changes post-deployment; if a third party API changes their schema, prod-deployed applications can fail. This does not apply to Data in Production; exogenous shocks to the system should result in bad-data, and this bad-data should be caught by data quality testing *before it propagates to Prod.* If there is a test capable of ascertaining data quality in production, that test should live in the staging environment.
4. **Improve processes and manage work with WIP limits**: we have only anecdotal evidence that this would be beneficial to Data Teams, who typically work with “a lot on their plate”. Most do not follow a full agile methodology because ticket sizes for tasks typically take up a much smaller amount of time than most software teams.
5. **Visualise work**: included for completeness

**Cultural capabilities**

1. **Support a generative culture**: it’s difficult to deny the generative culture outlined by Westrum would be beneficial for data organisations. What should definitely be included here is a culture that prioritises planning, bridging between teams (specifically operations and engineering) and collaboration.
2. **Encourage and support learning**
3. **Support and facilitate collaboration between data consumers and data producers, or align them into one**: Without collaboration between data consumers and producers, stacks become overly complicated as siloed teams take their raw inputs as given. THere are often significant benefits that can be reaped from close collaboration between teams early on in a company’s journey, which are largely down to improved communication and simpler data stacks / cleaner data that results. Aligning them into one is preferable and draws on the principle of “Data Mesh”, where individuals with domain specific knowledge can self-serve their data requirements i.e. do not need a data team
4. Provide resources and tools that make work meaningful
5. Support or embody transformational leadership

There are 24 characteristics outlined in Accelerate and it makes sense to use these as a starting point for what characteristics successful Data Teams should exhibit. It’s clear there’s an enormous amount of overlap but the devil is in the detail; some principles that may hold true in software delivery are likely to be less effective for data teams. There are also clear areas where the 24 characteristics require extension.

In the final section, we’ll propose another idea which is helpful when extending these principles to prioritising implementation details.

## A hierarchy of data needs

A natural starting point for the next article is to take the 24 characteristics and move on to what they mean practically, understanding what they mean for implementing a data stack that allows data teams of all shapes and sizes to succeed and reliably and efficiently release quality data into Production.

Rather than jump straight into what we believe best practice looks like, we suggest the following heuristic for choosing tooling that is intrinsically tied to the 24 characteristics above:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*YAPM6hvzY6dbrLyO)

1. **Security** (Characteristic 7): security should always be considered first as it is often a non-negotiable business obligation. Sometimes it may ignored entirely, since sometimes younger businesses do not care about it all. This has always astounded us.
2. **Functionality** (Characteristics 1–9): If security requirements can be met, the tooling chosen must achieve the desired outcome sufficiently well. If it doesn’t do that, there is no point in going with it. Note — this would include ensuring latency requirements are met
3. **Reliability (**Continuous Delivery): the tooling chosen must lead to reliable outcomes where data is reliably deployed to production. Without this, the efficacy of any data team will be significantly hampered by regular errors in data in production environments
4. **Cost and time to maintain (Architecture Capabilities)** is much higher up than in the world of software, since data teams rarely get an architectural carte blanche but instead have their utility intrinsically tied to business value. The ability to deliver on this is necessarily diminished if tooling / data stacks are very costly in dollar cost or time to maintain
5. **Flexibility (Architecture Capabilities)** is important, but arguably not as important as the other items. Flexibility is effectively the extent to which you value the future / your discount rate; if you value your future state more than the average person, you probably want a stack that is flexible for future needs. However given the future is uncertain, we believe it makes more logical sense to prioritise the present *predominantly. F* lexibility, while an important consideration, is not the most important consideration
6. **Simplicity (all)** is the data nirvana. When you have a fully secure, functional, reliable, and flexible architecture, you can begin to simplify it. Simplicity in many ways brings benefits to flexibility, reliability and cost, but given it often affects all of these a little bit itself, we have decided to give it its own section.

We believe that when tooling and processes are chosen using these criteria, Data Teams will stand themselves in adequate stead to execute on the 24 characteristics that *could* lead to success within a Data Team.

## Areas to continue on

In the next part of the miniseries, we’ll examine some of the DORA metrics and what these could look like for Data Teams. We’ll see there are important extensions to these that need to be made to accurately measure a Data Team’s performance and that “what good looks like” for a software team isn’t the same for a Data Team. We’ll then dive into some implementation detail for different profiles of Data Team.

## On Orchestra

We believe data tooling should exist in the context of releasing quality data and running quality data operations. We believe framing the capabilities of a data tool within the context of how it can help release data in a more robust way is necessary for the elevation of data teams into the stratosphere of value, occupied only by the greatest individual contributors in software teams. What we’re building will give Data Teams the ability to deploy data in an extremely robust way in a fraction of the time and with a fraction of the cost, leaving data teams time to focus on what really matters: creating business value.

[Learn more about Orchestra here](https://getorchestra.io/?utm_campaign=2023_8_orchestra_medium_account_medium_social).

### Examples and citations

We hope the findings in this miniseries resonate, and we appreciate there is limited scientifically collated quantitative data to support these conclusions — that is beyond the scope of the miniseries. There are, however, some references to various ideas we have managed to collate below. **Please note this list is incomplete, and in the process of being constantly updated**.

(1) Storing raw data in partitions:

[Robert Chang on Medium](https://medium.com/@rchang/a-beginners-guide-to-data-engineering-part-ii-47c4e7cbda71)

[Yashwanth Reddy Nukala on Linkedin](https://www.linkedin.com/pulse/understanding-data-partitioning-engineering-key-nukala/)

(8) ensuring state is available

[Zach Wilson on Substack](https://eczachly.substack.com/p/writing-data-to-production-is-a-contract?utm_campaign=post&utm_medium=web)

## References

1. Accelerate: The Science of Lean Software and Devops: Building and Scaling High Performing Technology Organizations. Kim, Forsgren and Humble, 2018