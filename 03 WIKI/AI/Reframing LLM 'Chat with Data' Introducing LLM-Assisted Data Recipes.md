---
title: "Reframing LLM 'Chat with Data': Introducing LLM-Assisted Data Recipes"
source: https://towardsdatascience.com/reframing-llm-chat-with-data-introducing-llm-assisted-data-recipes-f4096ac8c44b/
author:
  - "[[Matthew Harris]]"
published: 2024-01-26
created: 2026-04-04
description: A conversational data analysis pattern for increased transparency and safety with reduced costs
tags:
  - clippings
  - ai
topic:
type: note
---
*TL;DR*

*In this article, we cover some of the limitations in using Large Language Models (LLMs) to ‘Chat with Data’, proposing a ‘Data Recipes’ methodology which may be an alternative in some situations. Data Recipes extends the idea of reusable code snippets but includes data and has the advantage of being programmed conversationally using an LLM. This enables the creation of a reusable Data Recipes Library – for accessing data and generating insights – which offers more transparency for LLM-generated code with a human-in-the-loop to moderate recipes as required. Cached results from recipes – sourced from SQL queries or calls to external APIs – can be refreshed asynchronously for improved response times. The proposed solution is a variation of the LLMs As Tool Makers (LATM) architecture which splits the workflow into two streams: (i) A low transaction volume / high-cost stream for creating recipes; and (ii) A high transaction volume / low-cost stream for end-users to use recipes. Finally, by having a library of recipes and associated data integration, it is possible to create a ‘Data Recipes Hub’ with the possibility of community contribution.*

## Using LLMs for conversational data analysis

There are some very clever patterns now that allow people to ask questions in natural language about data, where a Large Language Model (LLM) generates calls to get the data and summarizes the output for the user. Often referred to as ‘ [Chat with Data](https://www.google.com/search?q=chat+with+data&oq=chat+with+data&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORiABDIHCAEQABiABDIHCAIQABiABDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIICAcQABgWGB4yCAgIEAAYFhgeMggICRAAGBYYHqgCALACAA&sourceid=chrome&ie=UTF-8) ‘, I’ve previously posted some articles illustrating this technique, for example using Open AI assistants to [help people prepare for climate change](https://medium.com/towards-data-science/preparing-for-climate-change-with-an-ai-assistant-cdceb5ce4426). There are many more advanced examples out there it can be an amazing way to lower the technical barrier for people to gain insights from complicated data.

![Examples of using LLMs to generate SQL queries from user inputs, and summarize output to provide an answer. Sources: Langchain SQL Agents](https://towardsdatascience.com/wp-content/uploads/2024/01/1A5ZcclVsx5bvgmqRSl4djA.png)

Examples of using LLMs to generate SQL queries from user inputs, and summarize output to provide an answer. Sources: Langchain SQL Agents

![Examples of using LLMs to generate API calls from user inputs, and summarize output to provide an answer. Sources: Langchain Interacting with APIs](https://towardsdatascience.com/wp-content/uploads/2024/01/1OTD6a2TQFmi-M-gR9FMvzw.png)

Examples of using LLMs to generate API calls from user inputs, and summarize output to provide an answer. Sources: Langchain Interacting with APIs

The method for accessing data typically falls into the following categories …

1. **Generating Database queries**: The LLM converts natural language to a query language such as SQL or Cypher
2. **Generating API Queries**: The LLM converts natural language to text used to call APIs

The application executes the LLM-provided suggestion to get the data, then usually passes the results back to the LLM to summarize.

## Getting the Data Can be a Problem

It’s amazing that these techniques now exist, but in turning them into production solutions each has its advantages and disadvantages …

![LLMs can generate text for executing database queries and calling external APIs, but each has its advantages and disadvantages](https://towardsdatascience.com/wp-content/uploads/2024/01/19wKohSKhXVo1frDsyQTJjQ.png)

LLMs can generate text for executing database queries and calling external APIs, but each has its advantages and disadvantages

For example, generating SQL supports all the amazing things a modern database query language can do, such as aggregation across large volumes of data. However, the data might not already be in a database where SQL can be used. It could be ingested and then queried with SQL, but building pipelines like this can be complex and costly to manage.

Accessing data directly through APIs means the data doesn’t have to be in a database and opens up a huge world of publically available datasets, but there is a catch. Many APIs do not support aggregate queries like those supported by SQL, so the only option is to extract the low-level data, and then aggregate it. This puts more burden on the LLM application and can require extraction of large amounts of data.

So both techniques have limitations.

## Passing Data Directly through LLMs Doesn’t Scale

On top of this, another major challenge quickly emerges when operationalizing LLMs for data analysis. Most solutions, such as [Open AI Assistants](https://platform.openai.com/docs/assistants/overview) can generate function calls for the caller to execute to extract data, but the output is [then passed back to the LLM](https://platform.openai.com/docs/assistants/tools/submitting-functions-outputs). It’s unclear exactly what happens internally at OpenAI, but it’s not very difficult to pass enough data to cause a token limit breach, suggesting the LLM is being used to process the raw data in a prompt. [Many patterns](https://python.langchain.com/docs/use_cases/sql/) do something along these lines, passing the output of function calling back to the LLM. This, of course, does not scale in the real world where data volumes required to answer a question can be large. It soon becomes expensive and often fails.

## LLM Code Generation Can be Slow, Expensive, and Unstable

One way around this is to instead perform the analysis by having the LLM generate the code for the task. For example, if the user asks for a count of records in a dataset, have the LLM generate a snippet of Python to count records in the raw data, execute it, and pass that information back to the user. This requires far fewer tokens compared to passing in the raw data to the LLM.

It is fairly well established that [LLMs are pretty good at generating code](https://evalplus.github.io/leaderboard.html). Not yet perfect, for sure, but a lot of the world right now is using tools like [GitHub Copilot](https://github.blog/2022-09-07-research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/) for software development. It is becoming a common pattern in LLM applications to have them generate and execute code as part of solving tasks. [OpenAI’s code interpreter](https://platform.openai.com/docs/assistants/tools) and frameworks such as [autogen](https://microsoft.github.io/autogen/) and Open AI assistants take this a step further in implementing iterative processes that can even debug generated code. Also, the concept of LLMs As Tool Makers (LATM) is established (see for example [Cai et al, 2023](https://arxiv.org/abs/2305.17126)).

But here there are some challenges too.

Any LLM process generating code, especially if that process goes through an iterative cycle to debug code, can quickly incur significant costs. This is because the best models needed for high-quality code generation are often the most expensive, and to debug code a history of previous attempts is required at each step in an iterative process, burning through tokens. It’s also quite slow, depending on the number of iterations required, leading to a poor user experience.

As many of us have also found, code generation is not perfect – yet – and will on occasion fail. Agents can get themselves lost in code debugging loops and though generated code may run as expected, the results may simply be incorrect due to bugs. For most applications, a human still needs to be in the loop.

## Remembering Data ‘Facts’ Has Limitations

Code generation cost and performance can be improved by implementing some sort of memory where information from previous identical requests can be retrieved, eliminating the requirement for repeat LLM calls. Solutions such as [memgpt](https://memgpt.ai/) work with frameworks like autogen and offer a neat way of doing this.

Two issues arise from this. First, data is often volatile and any specific answer (ie ‘Fact’) based on data can change over time. If asked today " *Which humanitarian organizations are active in the education sector in Afghanistan?"*, the answer will likely be different next month. Various memory strategies could be applied to ignore memory after some time, but the most trustworthy method is to simply get the information again.

Another issue is that our application may have generated an answer for a particular situation, for example, the population of a specific country. The memory will work well if another user asks exactly the same question, but isn’t useful if they ask about a different country. Saving ‘Facts’ is only half of the story if we are hoping to be able to reuse previous LLM responses.

## So What Can We Do About It?

Given all of the above, we have these key issues to solve:

- We need an approach that would work with databases and APIs
- We want to be able to support aggregate queries using API data
- We want to avoid using LLMs to summarize data and instead use code
- We want to save on costs and performance by using memory
- Memory needs to be kept up-to-date with data sources
- Memory should be generalizable, containing *skills* as well as facts
- Any code used needs to be reviewed by a human for accuracy and safety

Phew! That’s a lot to ask.

## Introducing LLM-Assisted Data Recipes

![Data Recipes architecture: LLM-assisted generation of reusable recipes (skills) which can be used for conversational data analysis](https://towardsdatascience.com/wp-content/uploads/2024/01/1t6NLo1alxgMJg3k-sHN6Zw.png)

Data Recipes architecture: LLM-assisted generation of reusable recipes (skills) which can be used for conversational data analysis

The idea is that we split the workflow into two streams to optimize costs and stability, as proposed with the [LATM architecture](https://arxiv.org/pdf/2305.17126.pdf), with some additional enhancements for managing data and memories specific to Data Recipes …

**Stream 1: Recipes Assistant**

This stream uses LLM agents and more powerful models to generate code snippets (recipes) via a conversational interface. The LLM is instructed with information about data sources – API specifications and Database Schema – so that the person creating recipes can more easily conversationally program new skills. Importantly, the process implements a review stage where generated code and results can be verified and modified by a human before being committed to memory. For best code generation, this stream uses more powerful models and autonomous agents, incurring higher costs per request. However, there is less traffic so costs are controlled.

**Stream 2: Data Analysis Assistant**

This stream is used by the wider group of end-users who are asking questions about data. The system checks memory to see if their request exists as a fact, e.g. " *What’s the population of Mali?*". If not, it checks recipes to see if it has a skill to get the answer, eg ‘ *How to get the population of any country* ‘. If no memory or skill exists, a request is sent to the recipes assistant queue for the recipe to be added. Ideally, the system can be pre-populated with recipes before launch, but the recipes library can actively grow over time based on user telemetry. Note that the end user stream does not generate code or queries on the fly and therefore can use less powerful LLMs, is more stable and secure, and incurs lower costs.

**Asynchronous Data Refresh**

To improve response times for end-users, recipes are refreshed asynchronously where feasible. The recipe memory contains code that can be run on a set schedule. Recipes can be preemptively executed to prepopulate the system, for example, retrieving the total population of all countries before end-users have requested them. Also, cases that require aggregation across large volumes of data extracted from APIs can be run out-of-hours, mitigating -albeit in part— the limitation of aggregate queries using API data.

**Memory Hierarchy – remembering skills as well as facts**

The above implements a hierarchy of memory to save ‘facts’ which can be promoted to more general ‘skills’. Memory retrieval promotion to recipes are achieved through a combination of semantic search and LLM reranking and transformation, for example prompting an LLM to generate a general intent and code, eg ‘ *Get total population for any country* ‘ from a specific intent and code, eg ‘ *What’s the total population of Mali?*‘.

Additionally, by automatically including recipes as available functions to the code generation LLM, its reusable toolkit grows such that new recipes are efficient and call prior recipes rather than generating all code from scratch.

## Some Additional Benefits of Data Recipes

By capturing data analysis requests from users and making these highly visible in the system, transparency is increased. LLM-generated code can be closely scrutinized, optimized, and adjusted, and answers produced by such code are well-understood and reproducible. This acts to reduce the uncertainty many LLM applications face around factual grounding and hallucination.

Another interesting aspect of this architecture is that it captures specific data analysis requirements and the frequency these are requested by users. This can be used to invest in more heavily utilized recipes bringing benefits to end users. For example, if a recipe for generating a humanitarian response situation report is accessed frequently, the recipe code for that report can improved proactively.

## Data Recipes Hub

This approach opens up the possibility of a community-maintained library of data recipes spanning multiple domains – a Data Recipes Hub. Similar to code snippet websites that already exist, it would add the dimension of data as well as help users in creation by providing LLM-assisted conversational programming. Recipes could receive reputation points and other such social platform feedback.

![Data Recipes - code snippets with data, created with LLM assistance - could be contributed by the community to a Data Recipes Hub. Image Source: DALL·E 3](https://towardsdatascience.com/wp-content/uploads/2024/01/1bJOXXg9QYvVQj51ZamfJPg.png)

Data Recipes – code snippets with data, created with LLM assistance – could be contributed by the community to a Data Recipes Hub. Image Source: DALL·E 3

## Limitations of Data Recipes

As with any architecture, it may not work well in all situations. A big part of data recipes is geared towards reducing costs and risks associated with creating code on the fly and instead building a reusable library with more transparency and human-in-the-loop intervention. It will of course be the case that a user can request something new not already supported in the recipe library. We can build a queue for these requests to be processed, and by providing LLM-assisted programming expect development times to be reduced, but there will be a delay to the end-user. However, this is an acceptable trade-off in many situations where it is undesirable to let loose LLM-generated, unmoderated code.

Another thing to consider is the asynchronous refresh of recipes. Depending on the amount of data required, this may become costly. Also, this refresh might not work well in cases where the source data changes rapidly and users require this information very quickly. In such cases, the recipe would be run every time rather than the result retrieved from memory.

The refresh mechanism should help with data aggregation tasks where data is sourced from APIs, but there still looms the fact that the underlying raw data will be ingested as part of the recipe. This of course will not work well for massive data volumes, but it’s at least limiting ingestion based on user demand rather than trying to ingest an entire remote dataset.

Finally, as with all ‘Chat with Data’ applications, they are only ever going to be as good as the data they have access to. If the desired data doesn’t exist or is of low quality, then perceived performance will be poor. Additionally, common inequity and bias exist in datasets so it’s important a data audit is carried out before presenting insights to the user. This isn’t specific to Data Recipes of course, but one of the biggest challenges posed in operationalizing such techniques. Garbage in, garbage out!

## Conclusions

The proposed architecture aims to address some of the challenges faced with LLM "Chat With Data", by being …

- **Transparent** – Recipes are highly visible and reviewed by a human before being promoted, mitigating issues around LLM hallucination and summarization
- **Deterministic** – Being code, they will produce the same results each time, unlike LLM summarization of data
- **Performant –** Implementing a memory that captures not only facts but skills, which can be refreshed asynchronously, improves response times
- **Inexpensive** — By structuring the workflow into two streams, the high-volume end-user stream can use lower-cost LLMs
- **Secure** – The main group of end-users do not trigger the generation and execution of code or queries on the fly, and any code undergoes human assessment for safety and accuracy