---
title: "Embedding an MCP Server into OpenMetadata — Summary"
type: note
topic: data-platform
created: 2026-04-04
tags:
  - openmetadata
  - mcp
  - ai
  - knowledge-graph
  - tools
source: "[[Embedding an MCP Server into OpenMetadata]]"
speakers:
  - Shihara (Collate)
  - Mohe (Collate)
event: OpenMetadata Community Meetup, May 21 2025
video: https://www.youtube.com/watch?v=AuYBaXC8-M4
---

# Embedding an MCP Server into OpenMetadata

**Speakers:** Shihara & Mohe, Collate
**Event:** OpenMetadata Community Meetup — May 21, 2025
**Video:** https://www.youtube.com/watch?v=AuYBaXC8-M4

---

## 1. Context: OpenMetadata Unified Knowledge Graph

OpenMetadata exists to address the growing complexity of modern data infrastructure — hundreds of services, everyone in the organisation acting as an analyst, thousands of tables, pipelines, and dashboards.

The platform provides:
- **90+ connectors** to extract physical metadata from heterogeneous sources into a single platform
- **Column-level lineage** — how data is transformed across pipelines and consumed in dashboards
- **Semantic enrichment** — PII detection, glossary terms, data classification, quality results
- **User activity layer** — permissions requests, documentation updates, ownership, questions

All of this is assembled into a **Unified Knowledge Graph**: a living, breathing graph that encodes not just the structure of data assets but the relationships, quality, governance policies, and user context around them.

### Knowledge Graph Contents

| Layer | Examples |
|---|---|
| Physical metadata | Tables, columns, schemas, data types, partitions |
| Lineage | Pipeline → table → dashboard (column-level) |
| Semantic | PII flags, data classification, glossary terms, account ID meaning |
| Quality | Profiling results, unique constraints, completeness checks, test results |
| Usage | Queries run against a table, join patterns, access frequency |
| Governance | Owners, teams, policies, tags |

---

## 2. The MCP Protocol

**MCP (Model Context Protocol)** is a standard that allows LLMs to call external tools. The pattern is:

```
User → LLM → MCP Server → External System (OpenMetadata) → LLM → Response
```

When a user asks an LLM "what is the customer ARR today?", the LLM calls the MCP server to fetch the right table metadata and context, then uses that context to formulate a precise, grounded answer.

MCP closes the gap between:
- **LLMs** (large, capable, but with no knowledge of your organisation's data)
- **OpenMetadata** (rich, structured, authoritative knowledge about all data assets)

---

## 3. Challenges with Traditional MCP Deployments

Before Collate's embedded solution, the standard MCP architecture had three major problems:

### 3.1 Local Server per User

Every user (data engineer, analyst, business user) had to:
1. Start a local MCP server on their laptop
2. Obtain and configure credentials to connect to the OpenMetadata API
3. Keep it running during their session

This is **not scalable** — it requires technical knowledge that most business users don't have, and creates operational overhead across the team.

### 3.2 OpenMetadata's Small Footprint Philosophy

OpenMetadata is designed to be simple to deploy: just four components to productionise. Adding a fifth, separately installed MCP server contradicts this philosophy and introduces another moving part for operators to manage.

### 3.3 Authentication and Authorization

MCP authentication has been a widely discussed challenge across the industry. The specific problem for OpenMetadata:
- All APIs are authenticated and controlled by a rich RBAC (Role-Based Access Control) system
- A generic MCP server would bypass per-user permissions
- A user without access to a `customers` table should **not** be able to ask the LLM "who are the paid customers?" and receive an answer sourced from that table
- Exposing the full knowledge graph to all users via LLM is a security anti-pattern

---

## 4. The Embedded MCP Solution

Collate's solution: implement the MCP server as an **OpenMetadata Application** — a pluggable module that runs **inside the OpenMetadata server process**.

### Architecture

```
OpenMetadata Server
├── Core REST APIs
├── Application Framework
│   ├── Data Insights (built-in)
│   ├── Search Indexing (built-in)
│   └── MCP Server Application  ← new
│       └── exposes /mcp/* endpoints alongside /api/* endpoints
```

When an operator enables the MCP Server application:
- No separate server to deploy or maintain
- MCP endpoints are exposed on the same host/port as the rest of OpenMetadata
- Any LLM client (Claude Desktop, Goose, ChatGPT) can connect directly to the OpenMetadata server's MCP endpoint

### Benefits

| Property | Description |
|---|---|
| **Out-of-the-box** | Install OpenMetadata, enable MCP app — done |
| **No per-user setup** | Every user in the organisation benefits immediately |
| **Not just an API wrapper** | Uses internal knowledge graph structures — lineage, schemas, quality, usage |
| **Production-ready** | Authentication and authorisation built in from day one |

---

## 5. Authentication: Personal Access Tokens

To preserve the per-user RBAC that OpenMetadata enforces:

1. Each user generates a **Personal Access Token** (PAT) from their profile page
   - Configurable expiry
   - Embeds the user's identity in the token
2. The user configures their LLM client (e.g. Claude Desktop) with their PAT as the MCP auth credential
3. Every MCP call made by the LLM is executed **on behalf of that user's identity**
4. All permissions, roles, inherited policies, and data restrictions apply automatically

**Effect:** The LLM can only surface data the user is already authorised to see. No privilege escalation through the AI layer.

---

## 6. Demo: Agentic Workflows

### 6.1 Data Analyst — Building a Dashboard

**Scenario:** Analyst wants to build a customer retention dashboard.

**Prompt:** "Get the relevant information related to the customers table, analyse it, and help me build a customer retention dashboard."

**What the MCP agent does:**
1. Searches OpenMetadata for tables matching "customers"
2. Fetches table metadata: descriptions, columns, tags, data quality results
3. Fetches associated queries (join patterns, SQL history)
4. Discovers related tables via lineage (orders, sales) — even though the user only asked about customers
5. Recommends `dim_customers` as the primary table because:
   - It has the highest data quality tier
   - It has the highest passing test results over recent days
6. Analyses `dim_customers` columns (29 columns, segmentation flags: new/returning/loyal, purchase history)
7. Extracts associated queries: customer segmentation distribution, at-risk customer identification
8. Generates a working customer retention dashboard (HTML/Python) using that context and sample data

**Key insight:** The MCP agent surfaces data quality ratings and usage patterns to guide table selection — not just raw metadata.

### 6.2 Data Steward — Bulk Ownership Assignment

**Scenario:** Steward wants to assign the "Data Team" as owner of all unowned customer-related tables.

**Prompt:** "Find all assets related to customers that have no owners. Find the Data Team. Assign Data Team as owner of all those assets."

**What the MCP agent does:**
1. Uses the search tool to find 4 tables matching "customer" criteria
2. Checks each for owner status — identifies the unowned ones
3. Fetches the `data-team` entity from OpenMetadata
4. PATCHes each table's ownership via the OpenMetadata API
5. Reports a summary: "Raw Customer, dim Customer, Customer Events — owner set to Data Team"

**Key insight:** This automates a governance workflow that would normally require manual UI work across dozens of assets.

---

## 7. Roadmap

At time of talk (May 2025):
- MCP server merged into the codebase that week
- Shipping in **OpenMetadata v1.8** (open source)
- More tools to be added continuously
- Planned use cases across all personas:

| Persona | Use Case |
|---|---|
| Data Analyst | Find right tables, understand queries, build dashboards |
| Data Governance | Create business glossary terms, set policies |
| Data Engineer | Check pipeline status, debug lineage |
| Data Steward | Bulk ownership assignment, tagging, classification |

---

## 8. Key Takeaways

| Topic | Summary |
|---|---|
| **Problem** | Per-user local MCP servers are not scalable and bypass RBAC |
| **Solution** | MCP embedded as an OpenMetadata Application — single deployment, all users benefit |
| **Auth** | Personal Access Tokens carry user identity and enforce existing permissions |
| **Power** | Full knowledge graph exposed: lineage, quality, usage, governance — not just schema |
| **Agentic AI** | LLMs can take actions (bulk ownership, schema discovery, dashboard generation) |
| **Version** | Available in OpenMetadata v1.8, open source |
