---
type: ai-conversation
topic: data-quality
created: 2026-03-19
tags:
  - ai-gen
  - data-quality
  - llm
  - claude
  - gemini
---

**Source:** Gemini AI Studio — [[#Gemini conversation]]
**Source:** Claude Code — [[#Claude conversation]]

---

## Gemini conversation

**Source:** https://aistudio.google.com/u/1/prompts/12pyOVNHefRrcRS5vjPsrwEwHKb3hi-Tr

### User

I have a Data Platform based on the following components:

- Dremio / Trino / Duckdb as Query engines
- Data is stored in Iceberg tables and Parquet files
- dbt for managing the transformations and tests
- Kestra / Airflow for orchestration
- DataHub as a Data Catalog

I'm searching for a Data Quality Tool with the following requisites:

- Opensource
- Deployed on premises (no cloud)
- Integration with local llm for suggesting possible quality test
- A Dashboard to have an overview of the situation
- Alerting features (slack / email)

Please suggest some tool with the requested features

---

### Model

Based on your current stack (Dremio/Trino, Iceberg, dbt, DataHub) and your requirements for an **on-premise**, **open-source** tool with **Local LLM** integration, the best recommendation is **OpenMetadata**.

While you already use DataHub, **OpenMetadata** is currently ahead in providing out-of-the-box "AI Agent" features that work with local LLMs (via Ollama) to suggest quality tests.

Here is a detailed breakdown of the best options:

#### 1. The "All-in-One" Solution: OpenMetadata

This is the closest match to your specific request for a tool that natively integrates local LLMs for suggestions and includes a dashboard.

- **Local LLM Integration:** OpenMetadata has introduced an "AI Assistant" feature that supports **Ollama**. This allows you to run a model like Llama 3 or Mistral on-premise. It can scan your table schemas/metadata and suggest descriptions and data quality tests without data leaving your infrastructure.
- **Dashboard:** It has a dedicated **Data Quality & Profiling** tab. You can view test success/failure rates, history, and profile statistics (min, max, null counts) directly in the UI.
- **Execution Engine:** It natively connects to **Trino**, **Dremio**, and **DuckDB** to run these tests. You don't need a separate execution engine; it pushes the query computation to your existing engines.
- **Alerting:** Built-in alerts (Slack, Email, MS Teams) when tests fail.

**How it works with your stack:** You would connect OpenMetadata to Trino/Dremio. It scans the Iceberg tables, the local LLM (via Ollama) suggests "Column A should not be null" or "Column B values should be between 1-100", and you confirm these tests in the UI. OpenMetadata then schedules and runs them.

#### 2. The "Build on What You Have" Solution: dbt + dbt-expectations + DataHub

Since you already have **dbt** and **DataHub**, you can achieve the same result without adding a massive new platform, though the "LLM suggestion" part requires a small custom workflow.

- **Execution:** Use the **[dbt-expectations](https://hub.getdbt.com/calogica/dbt_expectations/latest/)** package.
- **Dashboard:** **DataHub** allows you to visualize dbt test results via the `datahub` dbt plugin.
- **Local LLM Integration (The "Gap"):** No native "click-to-suggest" button. Requires a custom Python script using `langchain` + `ollama`.

#### 3. The "Standard" Alternative: Great Expectations (GX)

- **On-Premise:** Fully open-source and runs locally.
- **Dashboard:** Generates **Data Docs** (static HTML). Can be ingested into DataHub.
- **LLM Integration:** Requires a custom Profiler using your local LLM.

#### Summary

| Feature | **OpenMetadata** | **dbt + DataHub** | **Great Expectations** |
| :--- | :--- | :--- | :--- |
| **Test Engine** | Native (pushes to Trino/Dremio) | dbt (runs via Trino/Dremio) | Python/Pandas or SQL |
| **Local LLM** | **Native** (via Ollama) | Custom Script required | Custom Script required |
| **Dashboard** | **Built-in Interactive UI** | DataHub UI (via ingestion) | Static HTML (Data Docs) |
| **Alerting** | Native (Slack/Email) | Via Airflow/Kestra | Native (Slack/Email) |
| **Deployment** | Docker / Kubernetes (On-prem) | Existing Infrastructure | Docker / Python Package |

**Recommendation:** OpenMetadata is the only tool that offers the full package out-of-the-box for on-premise deployment.

---

## Claude conversation

> [!info] Context
> Architecture reference: [[Sintesi Architettura (Claude)]]
> LLM model rankings reference: [[Model Suggestions for llm.py]]

### Tool selection

**Q:** Given the Data Platform architecture, suggest a Data Quality tool (opensource, on-prem, local LLM integration, dashboard, alerting).

**A:** **OpenMetadata is already in the stack** — no new component needed.

| Requirement | OpenMetadata support |
|---|---|
| Opensource | ✓ Apache 2.0 |
| On-premises | ✓ Already deployed |
| Local LLM | ✓ Native Ollama integration — suggests DQ tests from schema |
| Dashboard | ✓ Built-in Data Quality & Profiling UI |
| Alerting Slack/Email | ✓ Native Webhook alerts (Slack, Email, MS Teams) |
| Dremio connector | ✓ Native — pushes test execution to Dremio |

**dbt** (also already in the stack) complements naturally: write tests in dbt YAML → OpenMetadata ingests results via its dbt connector → surfaces them in the DQ dashboard. Kestra orchestrates the runs.

> [!tip] Zero new components
> Activate OpenMetadata's Data Quality module + connect dbt test results to it.

---

### LLM model selection

**Q:** Do the model suggestions from [[Model Suggestions for llm.py]] apply to the DQ use case?

**A:** Partially yes. The DQ suggestion task (schema → constraint suggestions) maps to the **structured output/reasoning** category, same as dbt-osmosis. Key differences:

- OpenMetadata connects to **Ollama directly** via its UI settings — it does not use `llm.py`
- The task requires schema reasoning + domain understanding more than pure SQL generation
- Only Ollama-based models are directly applicable (LM Studio requires custom base URL support in OpenMetadata)

**Ollama-only ranking for DQ:**

| Rank | Model | Notes |
|---|---|---|
| 1 | `devstral-small-2:24b-instruct-2512-fp16` | Best quality, slower (fp16) |
| 2 | `qwen2.5-coder:14b-instruct-q4_K_M` | Best speed/quality ratio |
| 3 | `deepseek-coder-v2:16b-lite-instruct-q4_K_M` | Solid alternative |

---

### Large model evaluation (80–120B range)

**Q:** Evaluate Qwen3.5-122B-A10B, Mistral-Small-4, Qwen3-coder-next. Other suggestions in the 80–120B range?

#### Candidate evaluation

| Model | Assessment |
|---|---|
| **Qwen3.5-122B-A10B** | Strong pick — MoE with ~10B active params. Fast inference with 122B-scale knowledge. Fits both tasks (structured JSON + schema reasoning). |
| **Mistral-Small-4** | 119B total / 6B active (MoE, 128 experts, 4 active per token). 256k context window, configurable reasoning (fast ↔ deep), multimodal. Excellent fit — see details below. |
| **Qwen3-coder-next** | Uncertain — verify availability on Ollama before planning around it. |

#### Mistral-Small-4 specs

| Spec | Value |
|---|---|
| Total params | 119B |
| Active params/token | 6B (8B w/ embeddings) |
| Experts | 128 total, 4 active |
| Context window | 256k |
| Reasoning | Configurable (fast ↔ deep) |
| Multimodal | Yes (text + image) |

#### Other suggestions in the 80–120B range

| Model | Params | Notes |
|---|---|---|
| **Qwen3-72B** | 72B dense | Strongest dense model for instruction-following at this tier |
| **Qwen2.5-72B-Instruct** | 72B dense | Excellent all-rounder, very reliable on Ollama |
| **Llama 3.3 70B** | 70B dense | Strong instruction following |
| **Mistral-Large-2** | 123B dense | Fits range, excellent but slower (dense) |

#### MoE head-to-head: Mistral-Small-4 vs Qwen3.5-122B-A10B

| | **Mistral-Small-4** | **Qwen3.5-122B-A10B** |
|---|---|---|
| Total params | 119B | 122B |
| Active params/token | 6B | ~10B |
| Context window | **256k** | ~32k |
| Reasoning mode | **Configurable** | Fixed |
| Code specialization | General | General |

**Use-case split:**

- **dbt-osmosis** → `Qwen3.5-122B-A10B`: higher active params, stronger for structured JSON + SQL generation
- **OpenMetadata DQ suggestions** → `Mistral-Small-4`: 256k context handles large schemas, configurable reasoning for fast vs deep suggestions

> [!tip] Practical recommendation
> Install both. Point **OpenMetadata** at `mistral-small-4` and **dbt-osmosis** at `qwen3.5-122b-a10b`.
