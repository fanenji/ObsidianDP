---
title: Context is Important, Metadata Provides It
source: https://odsc.medium.com/context-is-important-metadata-provides-it-6ffdc777037e
author:
  - "[[ODSC - Open Data Science]]"
published: 2025-09-03
created: 2026-04-04
description: "Context is Important, Metadata Provides It Editor’s note: Nick Acosta is a speaker for ODSC West this October 28th to 30th. Be sure to check out his talk, “AI Driven Automation in Open-Source …"
tags:
  - clippings
  - opendata
  - ai
  - mcp
topic:
type: note
---
[Sitemap](https://odsc.medium.com/sitemap/sitemap.xml)

![](https://miro.medium.com/v2/resize:fit:1280/format:webp/0*4NImscvIGnfoRGI_.png)

*Editor’s note: Nick Acosta is a speaker for* *this October 28th to 30th. Be sure to check out his talk, “* [***AI Driven Automation in Open-Source Metadata Platforms: Embedding an MCP Server***](https://odsc.ai/speakers-portfolio/ai-driven-automation-in-open-source-metadata-platforms-embedding-an-mcp-server/)*,” there!*

Data scientists make flawed assumptions, AI agents produce misleading recommendations, and LLMs generate insights that appear superficially accurate but lack the nuanced depth necessary for sound business decision-making. Although all three groups are intelligent, and often have plenty of data at their disposal, issues are bound to arise when the proper context is unknown.

MCP gives all three context. MCP stands for Model Context Protocol and was developed and open-sourced by Anthropic to standardize integrations between AI and the tools and data sources that can provide critical information in ways that enable LLMs to understand and take action. Instead of every service building out an integration for every AI agent, MCP defines a protocol where any application can maintain a single MCP server implementation that exposes its functionality, which any AI system can connect to with standardized expectations of authentication, data exchange, and function calling.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*ST7kSINZqMMgzQbr.png)

*from Building Agents with Model Context Protocol*

Giving Data Scientists, agents, and LLMs access to tools through Model Context Protocol is necessary to provide additional context to their work, but it is not sufficient.

Say I am trying to build AI that the Sales team at my organization can use to target which of our accounts is most likely to churn. If a sales team member asked an LLM directly without context it would surely hallucinate, it would not have any information on my organization, its customers, or the accounts the team member owned. Exposing an LLM to data through MCP will only improve the model’s responses if that MCP server can provide the right context. A CRM could store important customer data, but it might have hundreds of references and copies of customer data, data that my sales teammates are not supposed to have access to, and lack product usage data that might indicate churn. Connecting an AI Agent to a CRM MCP might provide an LLM an account list, but would still lack the comprehensive, permission-appropriate context needed to make accurate churn predictions. We could add additional MCP servers, but this can quickly become unruly to maintain as the agents, users, use cases, and integrations grow. Context alone isn’t good enough, what we would really need is a unified view of our data ecosystem.

Metadata platforms are designed to store the complete data context from across an organization’s datasets, schemas, owners, usage, upstream pipelines, downstream dashboards, quality tests, and ML models. This can provide the data discovery, quality, lineage, observability, and governance necessary to give AI the comprehensive set of tools, resources, and prompts it needs to take action. Metadata platforms can maintain a Unified Knowledge Graph that provides this deeper context about data and creates a single source of truth across all your data systems across all departments across all time. Exposing a metadata platform’s knowledge graph to AI through MCP servers can give teams the ability to read the appropriate data for introspection and analysis while enabling an easy chat interface to write changes back and improve a knowledge graph even further!

![](https://miro.medium.com/v2/resize:fit:1372/format:webp/0*vLHKsOmH9A2D3_dS.jpg)

from [open-metadata.org/mcp](http://open-metadata.org/mcp)

[OpenMetadata](http://open-metadata.org/) is an open-source metadata platform that automatically discovers and catalogs data across your entire stack, maintains real-time lineage tracking, and enforces governance at scale. Through OpenMetadata’s [MCP Server](http://open-metadata.org/mcp), AI agents gain access to this knowledge graph and transform LLMs into organizationally-aware assistants that understand your business context.

## Come build AI Systems with proper context at ODSC West 2025

To learn more about MCP servers, metadata platforms, and how to build with them in open-source, check out my tutorial at ODSC West 2025! We will be using OpenMetadata, which has emerged as a leading open-source Unified Metadata Platform for data discovery, observability, and governance, and Goose, an extensible open source AI agent. We’ll cover:

- OpenMetadata, MCP Servers, Goose, and their impact on a data stack
- Walkthrough transformational use cases for AI that use metadata proactively
- Build a system you can extend to your data environment that prompts completely in open-source!

Be sure to check out my workshop at ODSC West for some hands-on experience! You can find [more details here](https://odsc.ai/speakers-portfolio/ai-driven-automation-in-open-source-metadata-platforms-embedding-an-mcp-server/)!

**About Author**

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/0*hkZBwCUbDlyOO6AM.png)

Nick Acosta is a Developer Advocate at Collate, where he is helping to make the OpenMetadata community the best place for open-source data discovery, observability, and governance. Nick lives in Los Angeles, California, and started in Developer Relations at IBM before leading devrel at Fivetran and Tecton. This is Nick’s third time running a hands-on lab at ODSC! In addition to being a Developer Advocate, Nick is a Graduate Student in the Institute of Pastoral Studies at Loyola Chicago.

[![ODSC - Open Data Science](https://miro.medium.com/v2/resize:fill:96:96/2*xmanz0nHjUWhZDxHWKKaYg.png)](https://odsc.medium.com/?source=post_page---post_author_info--6ffdc777037e---------------------------------------)

[![ODSC - Open Data Science](https://miro.medium.com/v2/resize:fill:128:128/2*xmanz0nHjUWhZDxHWKKaYg.png)](https://odsc.medium.com/?source=post_page---post_author_info--6ffdc777037e---------------------------------------)

[136 following](https://odsc.medium.com/following?source=post_page---post_author_info--6ffdc777037e---------------------------------------)

Our passion is bringing thousands of the best and brightest data scientists together under one roof for an incredible learning and networking experience.