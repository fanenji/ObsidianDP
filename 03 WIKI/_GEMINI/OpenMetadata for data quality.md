---
title: "OpenMetadata for data quality"
type: conversation
topic: data-platform
created: 2026-02-13
tags:
  - openmetadata
  - data-quality
---
**Source:** https://aistudio.google.com/u/1/prompts/12pyOVNHefRrcRS5vjPsrwEwHKb3hi-Tr

---

### User

I have a Data Platform based on the followind components:

- Dremio / Trino / Duckdb as Queery engines
- Data is stored in Iceberg tables and Parquet files
- dbt for managing the trasfomations and tests
- Kestra / Airflow for orchestration
- DataHub as a Data Catalog

I’m searching for a Data Quality Tool with the following requisites:

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

### 1. The "All-in-One" Solution: OpenMetadata
This is the closest match to your specific request for a tool that natively integrates local LLMs for suggestions and includes a dashboard.

*   **Why it fits:**
    *   **Local LLM Integration:** OpenMetadata has introduced an "AI Assistant" feature that supports **Ollama**. This allows you to run a model like Llama 3 or Mistral on-premise. It can scan your table schemas/metadata and suggest descriptions and data quality tests without data leaving your infrastructure.
    *   **Dashboard:** It has a dedicated **Data Quality & Profiling** tab. You can view test success/failure rates, history, and profile statistics (min, max, null counts) directly in the UI.
    *   **Execution Engine:** It natively connects to **Trino**, **Dremio**, and **DuckDB** to run these tests. You don't need a separate execution engine; it pushes the query computation to your existing engines.
    *   **Alerting:** Built-in alerts (Slack, Email, MS Teams) when tests fail.
*   **How it works with your stack:** You would connect OpenMetadata to Trino/Dremio. It scans the Iceberg tables, the local LLM (via Ollama) suggests "Column A should not be null" or "Column B values should be between 1-100", and you confirm these tests in the UI. OpenMetadata then schedules and runs them.

### 2. The "Build on What You Have" Solution: dbt + dbt-expectations + DataHub
Since you already have **dbt** and **DataHub**, you can achieve the same result without adding a massive new platform, though the "LLM suggestion" part requires a small custom workflow.

*   **The Tooling:**
    *   **Execution:** Use the **[dbt-expectations](https://hub.getdbt.com/calogica/dbt_expectations/latest/)** package. It allows you to write Great Expectations-style tests directly in your dbt YAML files (e.g., `expect_column_values_to_be_unique`).
    *   **Dashboard:** **DataHub** allows you to visualize dbt test results. You can configure the `datahub` dbt plugin to ingest test outcomes (Pass/Fail) so they appear in your DataHub catalog on the "Validation" or "Quality" tab of the dataset.
    *   **Local LLM Integration (The "Gap"):** There is no native "click-to-suggest" button in DataHub for this yet. You would create a simple Python script using a local LLM library (like `langchain` + `ollama`).
        *   *Script logic:* Read your dbt `schema.yml` $\rightarrow$ Send schema to Local LLM with prompt "Suggest data quality tests for dbt" $\rightarrow$ LLM outputs YAML snippets $\rightarrow$ You paste them into your dbt project.
*   **Pros:** deeply integrated into your existing transformation workflows.
*   **Cons:** The LLM part is manual or requires a custom script, whereas OpenMetadata has it in the UI.

### 3. The "Standard" Alternative: Great Expectations (GX)
If you want a dedicated testing framework separate from dbt.

*   **On-Premise:** Fully open-source and runs locally.
*   **Dashboard:** Generates **Data Docs**, which are static HTML websites hosting your test results. These are excellent but aren't a "live" dashboard unless you host the HTML files.
*   **LLM Integration:** GX has "interactive" features, but for local LLM suggestions, you would typically use their Python API to inject a custom "Profiler" that uses your local LLM to propose expectations.
*   **Note:** You can ingest GX results into DataHub to use DataHub as the dashboard.

### Summary Recommendation

| Feature | **OpenMetadata** (Recommended) | **dbt + DataHub** (Minimal Change) | **Great Expectations** |
| :--- | :--- | :--- | :--- |
| **Test Engine** | Native (pushes to Trino/Dremio) | dbt (runs via Trino/Dremio) | Python/Pandas or SQL |
| **Local LLM** | **Native** (via Ollama integration) | Custom Script required | Custom Script required |
| **Dashboard** | **Built-in Interactive UI** | DataHub UI (via ingestion) | Static HTML (Data Docs) |
| **Alerting** | Native (Slack/Email) | Via dbt Cloud or Airflow/Kestra | Native (Slack/Email) |
| **Deployment** | Docker / Kubernetes (On-prem) | Existing Infrastructure | Docker / Python Package |

**My advice:**
Since you specifically asked for **integration with local LLM for suggesting tests** and a **dashboard**, **OpenMetadata** is the only tool that offers this package "out of the box" for on-premise deployment right now.

If you prefer to stick strictly to your current tools, I would recommend using **dbt-expectations** and writing a small utility script to have your local LLM generate the YAML config for you.

---

### User

Are you sure Openmetadata has a Dremio connector?

---

### Model

Based on your specific constraints—especially the need for **Local LLM integration** and **On-premise** deployment—the best fit for your stack is **OpenMetadata**.

While most tools require you to send metadata to a cloud to get AI suggestions, OpenMetadata has built a native integration with **Ollama** that runs entirely on your infrastructure.

### Top Recommendation: OpenMetadata
OpenMetadata is an open-source "Data Catalog + Data Quality" platform. It fits your request because it treats Data Quality as a first-class citizen with a dedicated dashboard, not just a side feature.

*   **How it meets your needs:**
    *   **Local LLM Integration:** It has a built-in AI Assistant that connects to a local **Ollama** instance. It can scan your schema and suggest descriptions and **Data Quality Tests** (e.g., "ReviewCount should be between 0 and 5") without any data leaving your network.
    *   **Dashboard:** It provides a "Data Quality" tab for every table, showing test pass/fail history, profiling stats (nulls, min/max, distinct), and lineage.
    *   **Alerting:** Native integration with Slack, MS Teams, and Email for test failures.
    *   **Architecture:** Deploys via Docker/Kubernetes on-prem.

*   **Integration with your Stack:**
    *   **Trino & Iceberg:** It has native, production-grade connectors for both. Since your data is in Iceberg and queryable via Trino, OpenMetadata can profile your data effectively through these channels.
    *   **Dremio:** *Note:* OpenMetadata does **not** have a dedicated "Dremio" connector in its main release yet.
        *   *Workaround:* You can connect it to **Trino** to profile the underlying Iceberg data (recommended). Alternatively, you can use the OpenMetadata **Database Service (JDBC)** connector to connect to Dremio using Dremio's JDBC driver, though this is less "plug-and-play" than the Trino connector.
    *   **dbt:** It ingests your dbt `manifest.json` and `catalog.json` to populate lineage and descriptions automatically.

### Alternative: Soda Core + Custom Wrapper
If you prefer a lightweight CLI tool over a full platform, **Soda Core** is the industry standard for open-source data quality.

*   **Pros:** It has a working **Dremio** connector (via `soda-dremio`). It is excellent at running checks inside your orchestration pipeline (Kestra/Airflow).
*   **Cons:**
    *   **No Native Local LLM:** You would need to write a Python script that asks your Local LLM to "generate a SodaCL YAML file based on this schema," whereas OpenMetadata has this in the UI.
    *   **Dashboard:** Soda Core is CLI-only. The dashboard (Soda Cloud) is SaaS. To get an on-prem dashboard, you would have to ingest Soda's JSON output into DataHub or build a custom Grafana view.

### Summary Comparison

| Feature | **OpenMetadata** (Winner) | **Soda Core** | **dbt (dbt-expectations)** |
| :--- | :--- | :--- | :--- |
| **Local LLM** | **Native (Ollama)** | Manual / Custom Script | Manual / Custom Script |
| **Dashboard** | **Built-in UI** | Requires SaaS or Custom | DataHub (via ingestion) |
| **Dremio Support** | Via JDBC or Trino/Iceberg | **Native (`soda-dremio`)** | Native (via dbt adapter) |
| **Orchestration** | Kestra/Airflow triggers | Kestra/Airflow triggers | Runs within dbt |
| **Alerting** | Slack / Email / Teams | Slack / Email (CLI) | Via dbt/Orchestrator |

**My Advice:**
Deploy **OpenMetadata**. Connect it to **Ollama** for the AI requirements and to **Trino** to scan your Iceberg data. This gives you the dashboard, alerting, and "AI suggestions" out of the box while keeping everything on-prem.

---

### User

what are the best opensource models for this kind of work? make a list with pros and cons of every model.

---

### Model

For local data quality generation, you need a model that balances **SQL proficiency** (to write the tests) with **reasoning capabilities** (to understand *what* to test based on column names like "birth_date" vs "transaction_date").[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)]

Since you are using **Ollama** (via OpenMetadata), all the models below are available directly through the Ollama library.[[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)]

Here are the best open-source models for this specific work, ranked by their suitability for Data Engineering tasks.

### 1. Qwen 2.5 Coder (The Current Leader)
Alibaba's Qwen 2.5 "Coder" series is currently widely considered the best open-weight model for coding and SQL tasks, often outperforming larger Llama models in benchmarks.[[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)]
*   **Best Size for On-Prem:** 14B or 32B (if you have the VRAM).[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)] Even the 7B is excellent.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)]
*   **Ollama Tag:** `ollama run qwen2.5-coder`

| **Pros** | **Cons** |
| :--- | :--- |
| **SQL Expert:** specifically fine-tuned for code and SQL; understands complex joins and data types better than general models.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)] | **Chinese Origin:** Some strict enterprise security policies may flag it due to its origin (Alibaba), though the weights are open.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)] |
| **Context Window:** Massive context support (up to 128k), meaning you can feed it very large table schemas without cutting off text.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)] | |
| **Logic:** Excellent at "reasoning" (e.g., inferring that `net_revenue` should be `gross - tax`). | |

### 2. Llama 3.1 (The Safe Standard)
Meta’s latest model is the industry standard.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)] It is a "general purpose" model, which means it is very good at understanding natural language descriptions of your data ("This table contains customer PII") but slightly less specialized in SQL syntax nuances than Qwen Coder.[[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)]
*   **Best Size for On-Prem:** 8B (lightweight) or 70B (heavy duty).[[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)]
*   **Ollama Tag:** `ollama run llama3.1`

| **Pros** | **Cons** |
| :--- | :--- |
| **English NLP:** Best-in-class at understanding the *business context* from your table comments and documentation.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)] | **Strict Safety:** Meta models are heavily aligned; sometimes they refuse to generate code if they misinterpret a prompt as "unsafe" (less common in 3.1, but possible).[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)] |
| **Ecosystem:** Widely supported; if you hit a bug, someone else has likely fixed it.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)] | **Resource Heavy:** The jump from 8B to 70B is huge.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)] There is no "middle ground" (like a 32B model) in the official lineup.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)] |
| **License:** Very permissive community license widely accepted by western enterprises.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)] | |

### 3. Mistral "Codestral" / Mistral Nemo
Mistral (French AI lab) produces highly efficient models.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)] **Codestral** is their 22B parameter model dedicated to code.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)] Alternatively, **Mistral Nemo (12B)** is a great middle-ground collaboration with NVIDIA.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)]
*   **Best Size for On-Prem:** 22B (Codestral) or 12B (Nemo).[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)]
*   **Ollama Tag:** `ollama run codestral` or `ollama run mistral-nemo`[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)]

| **Pros** | **Cons** |
| :--- | :--- |
| **Code Specialization:** Codestral is trained specifically for code generation and tests (Python/SQL/dbt YAML). | **Hardware Awkwardness:** The 22B size is awkward for some GPUs (too big for 24GB VRAM unless quantized).[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)] |
| **Efficiency:** Mistral models generally punch above their weight class (a 12B Mistral often beats a 14B generic model).[[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)] | |

### 4. DeepSeek-Coder V2 (The Specialist)
A specialized "Mixture-of-Experts" (MoE) model.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)] It is exceptionally strong at coding tasks and often beats GPT-4 in coding benchmarks.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)]
*   **Best Size for On-Prem:** The "Lite" version (16B) is manageable; the full version is massive (230B+).[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)]
*   **Ollama Tag:** `ollama run deepseek-coder-v2`[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)]

| **Pros** | **Cons** |
| :--- | :--- |
| **SOTA Coding:** arguably the smartest open-source coding model available right now.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)] | **Complex Architecture:** Being a "Mixture of Experts," it can be slower to run (inference latency) on older hardware compared to dense models like Llama.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)] |
| **Huge Context:** Supports very long contexts natively.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)] | **VRAM Hungry:** Even the smaller versions can be heavy on memory requirements compared to a simple Llama 8B.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)] |

---

### Hardware Guide: Which one can you run?

Your choice will depend on the **GPU VRAM** available on your on-prem server.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)]

*   **< 16GB VRAM (Consumer GPU / Laptop):**
    *   *Recommendation:* **Llama 3.1 (8B)** or **Qwen 2.5 Coder (7B)**.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)]
    *   *Reason:* These will run fast and leave room for the OS.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)]
*   **24GB VRAM (e.g., Nvidia A10, RTX 3090/4090):**
    *   *Recommendation:* **Qwen 2.5 Coder (14B)** or **Mistral Nemo (12B)**.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)]
    *   *Reason:* You can run these at high precision (FP16) or run slightly larger models (like Codestral 22B) heavily compressed (4-bit quantization).[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)]
*   **48GB - 80GB VRAM (e.g., A6000, A100, H100):**
    *   *Recommendation:* **Qwen 2.5 Coder (32B)**.
    *   *Reason:* This is the "sweet spot" for performance.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)] It is smart enough to handle complex data logic but fits comfortably on a single enterprise GPU.[[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)]

### Final Recommendation for Data Quality
Start with **Qwen 2.5 Coder (14B)** or **32B** depending on your hardware.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFWTWuOFrt5bWQp0vodxGqEYfPYO6QLD0RrNIBEQc7mona5NqHkLS0ScwCMHv8wqKqPgUtbuHeXuyzGsLBnw0aFHiqKomK-io1psfVGFFybQo8rBmrqylyirTXdiEbmuYaGJ0kE5FuEfx_qv5jgB8HoTATbDlde1McrAt1J1n7SPBTEA2ah5b1LoVxEkiTaNIadFtcehpOp2qejiuN5eyZQ_tk%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFCAJRrTTniGuPfiz2EmO4c65bvKEn2Br3nMfjdN3TBuDA-evnEJcp6H_qr6p39in4MOEHd75hm8FJBv-d0R-dCZWH7KITQWRU3j0jI5NguajGcUHYeA09XYMKD_4AyRuoK7QBgQ98%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHDIf16_UvMgLQzvSXW7rLOU0CYKHSW35ZTrL3ksGl17pXZ51AjSX6hQekwiAjtLDqkiv3erK1KOn-LiLKEwbhV_yToGGy-52ndSOA3hWpS-LCX4-0hw3pjMBwdHksW-ObU73IYUbSU-kIdCNthv2k2tUAmDWsJ423T0Vie3Mtvj698NBSjW-qI9wxKRhugLA6UK_pUlbyKFAx_p1ZIWFY%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFjqC75dh2vhkfrxPJ6MDvBnaXbdxaNKx0NU3Rl9BpDs-PZmFNFa3Gybn1jZUf6Rw0s4ZRbJ9cLOja8q51p3oMaUlXKBoX_cIt3vIT2WoZPIHbnGHpzoacPHrVIny4khOd-rPfEjIwo8FA6zHy4VPbigxdeOjmfrHfJfrJpt5ZMWnd7USqolZNW3-4S8z-7kX4NCEgXnE-FfZ1rLqLilgs%3D)]
It has the best balance of understanding "code logic" (required for writing SQL/dbt tests) and "schema reasoning" (understanding that a column named `email` needs a regex check).

---

### User

Is there any small model that can run on cpu?

---

### Model

Yes, absolutely. Running on a CPU is all about keeping the model size small (fewer "parameters") so it fits in your RAM and doesn't take 5 minutes to generate one sentence.

For your use case (reading a schema and suggesting tests), you need a model that is smart at **SQL/Code** but small enough to run fast.

Here are the best **CPU-friendly** models available on Ollama today.

### Top Recommendation: Qwen 2.5 Coder (3B)
This is currently the "pound-for-pound" champion for coding tasks on low-end hardware. It is specifically trained for code and SQL, making it surprisingly capable for its tiny size.

*   **Size:** ~2 GB RAM required.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHSOpZ1XTo9B0jf0GIsnde8uzKKtO3MG6cc2sQYTSB-M52SwGUFq8d0fFSHaJ4hxdJUbHf-Utt2oH6bh50IGyeRT1W2smqDDp_IAOnnnsgA3-meL43xmQxcycbtY5Iwf9YXtmAKr5Ybpp8ZaWYWcOaALVd7pc11THEkTNJUNZb4_lC_KHUHGL_JylQgEGrMdSVAGW9O8A%3D%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFyRYXueurQQ63v84SmC7d9RU6M3OpbMKPZo539ygGfP8z1-1fzCAPGWIxEC3dj-A6XK7Wl7qvchOihsHJFjEFg8E2bC4pbnOjkjJ6lu9yZV6RFtvbmYD635UVMg8XpCzzvObqnWVBgMw%3D%3D)]
*   **Ollama Command:** `ollama run qwen2.5-coder:3b`
*   **Pros:**
    *   **Specialized:** It is fine-tuned for code, so it understands `CREATE TABLE` and data types better than general chat models of the same size.
    *   **Fast:** On a modern CPU (like an M1/M2/M3 Mac or decent Intel i5/i7), it feels almost instantaneous.
    *   **Context:** Supports decent context length, so you can paste a medium-sized schema without issue.
*   **Cons:**
    *   **Reasoning Limits:** It might struggle with very complex business logic (e.g., "suggest a test that correlates revenue with tax laws in Italy") compared to larger models.

### Runner Up: Microsoft Phi-3.5 Mini (3.8B)
Microsoft designed this model specifically to punch above its weight class by training it on "textbook quality" data. It is widely considered the smartest "small" model for reasoning.

*   **Size:** ~2.5 GB RAM required.
*   **Ollama Command:** `ollama run phi3.5`
*   **Pros:**
    *   **Reasoning:** Excellent at understanding instructions. If you ask it to "Suggest tests for columns that look like PII", it is very good at inferring context.
    *   **Context Window:** It has a massive **128k context window**, meaning you can feed it huge table schemas or even documentation files, and it won't "forget" the beginning.
*   **Cons:**
    *   **Less SQL Focus:** It is a generalist model. It writes good code, but Qwen Coder is slightly sharper on syntax.

### The Balanced Option: Llama 3.2 (3B)
Released by Meta specifically for edge devices (laptops, phones). It is a shrunk-down version of the powerful Llama 3.1.

*   **Size:** ~2.2 GB RAM required.[[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFyRYXueurQQ63v84SmC7d9RU6M3OpbMKPZo539ygGfP8z1-1fzCAPGWIxEC3dj-A6XK7Wl7qvchOihsHJFjEFg8E2bC4pbnOjkjJ6lu9yZV6RFtvbmYD635UVMg8XpCzzvObqnWVBgMw%3D%3D)]
*   **Ollama Command:** `ollama run llama3.2`
*   **Pros:**
    *   **Tool Use:** It is trained to be very good at using "tools" or formatting output as JSON, which is helpful if you want the suggested tests in a specific format to copy-paste into dbt/Soda.
    *   **Ecosystem:** Because it's Llama, it works with almost every prompt template out there.
*   **Cons:**
    *   In pure coding benchmarks, it often trails slightly behind Qwen Coder.[[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHOSLkuc-1J4v2llrBApQ8P2h-d3HOSYIfJBQkuuxCcAX8haJv6EM8tranPOggbHvRo_zSotvR3LRcg6lnpxYsL8tHEVuDiN1P_Kh16evkeezphLP2G8fnDRpL5KPwJE_8Jw0aYcIRe8Wlv9KHL75zHx-qts4_iM8i8mnh5_W224u78VvdcxpTxBaPo32U9yGI%3D)]

### The "Ultra-Light" Option: Gemma 2 (2B)
If you are running on a very old server or a machine with **< 4GB of RAM**, this is your best bet. It comes from Google DeepMind.[[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFKEwRIqNd8WVspuJs5va1gvvyGrAt2M4K0KZo-sNJEVCGfJblhIbj-l0iSEDOfHky90ok-U2r6raFW9KGrK7u8RJkzLscF_qXcxxtumO7Fg7rRLEuKNsJ95hjA1oKPyOcjAhXWcNA%3D)]

*   **Size:** ~1.5 GB RAM required.
*   **Ollama Command:** `ollama run gemma2:2b`
*   **Pros:**
    *   **Extremely Fast:** It will fly even on older CPUs.
    *   **Lightweight:** You can run this alongside your other services (Dremio, Docker) without it choking the server.
*   **Cons:**
    *   **"Dumb":** At 2B parameters, it hallucinates more often. It might suggest a test for a column that doesn't exist if the schema is too complex.

### Summary Comparison Table for CPU

| Model | Best Use Case | RAM Needed | SQL Ability | Speed |
| :--- | :--- | :--- | :--- | :--- |
| **Qwen 2.5 Coder (3B)** | **Best Overall for You** | ~2GB | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡ |
| **Phi-3.5 Mini (3.8B)** | Complex Reasoning | ~2.5GB | ⭐⭐⭐⭐ | ⚡⚡⚡ |
| **Llama 3.2 (3B)** | General Chat / JSON | ~2.2GB | ⭐⭐⭐ | ⚡⚡⚡⚡ |
| **Gemma 2 (2B)** | Extremely Old Hardware | ~1.5GB | ⭐⭐ | ⚡⚡⚡⚡⚡ |

**My Advice:**
Start with **Qwen 2.5 Coder 3B**.[[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHOSLkuc-1J4v2llrBApQ8P2h-d3HOSYIfJBQkuuxCcAX8haJv6EM8tranPOggbHvRo_zSotvR3LRcg6lnpxYsL8tHEVuDiN1P_Kh16evkeezphLP2G8fnDRpL5KPwJE_8Jw0aYcIRe8Wlv9KHL75zHx-qts4_iM8i8mnh5_W224u78VvdcxpTxBaPo32U9yGI%3D)] It strikes the perfect balance for a Data Platform engineer: it speaks "SQL" fluently and is light enough to run on almost any CPU without slowing down your other services.

---

### User

what about DBRX?

---

### Model

**DBRX** (by Databricks) is essentially the "final boss" of open-source models.

It is an incredible model, but it is **completely different** from the "small CPU" models we just discussed. It is massive, resource-hungry, and likely **impossible to run** on your standard on-premise infrastructure unless you have a dedicated AI super-server.

Here is the breakdown of why DBRX is likely **not** the right fit for a standard local Data Platform setup:

### 1. The Hardware Barrier
DBRX is a **Mixture-of-Experts (MoE)** model with **132 Billion** parameters.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEtU5HgbL3SX-WJVuyyplfBG3_CllW62SfqLqNZeOGjN72vFbLfwoX3MLZU8SlgpcGLTZSrQD9uPG3dxawwVLbAmM906Nr5Hli6yAJbdgi7-flR9fI7lPkkuPf-FsL1PjodLQqkKj1XE_qJWjTr-mRmnxyYhODX_KSxDIO7MYU5xQ8j)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGAyHKuQf250OFuef9c1mdAUpg19mTlT1_nFkPkqCoIeBxTnM2LgdWEHsOu55voTUtcc6__-H2LiGmXS_4EJiJ_yjT1jhmBePgcG98eaabyGKKrD8ytkCu3_XOfTxs5UxfxheYSXF0%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQH--aMbFIOIdvaztk1_cxsUQua5DBsGOIKo9txgj5kGvO2pd9tOjYJyIcSnTAeBI4gLQbG-uKSojHzapv2hGjO91dF2LMk5mTe0QfV6vgeUj-_gbizMYErN3prJqhqf6JOoyzcei8WL32M_HG_pC9dgo573996KzsbCFe4fvA629otqHWUWQRKUwsIMBH7SBwww7lZQsSX2xvXO)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGxN_YB354B8KBFvY6tK9awx-hdL44SaharEmBqfAlXlVdYpe_sojyeEDTH_KqmDcy4vNoUCVOZz0wlztPc6P8Cw5m5_Fj3FcN6zNWnesetA8FPh9n0brt8N7Evx2_A3TqY29a27zadI6G9774Xmg%3D%3D)][[5](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGZhUajwayWBp4eCSh2wh6-MBtDbqNXL8n3trdz7JQLtgCPoGBsMCIf6d_PyiGJL4TS7jje74Zn-9_PxLiofHf8oqG9oYIyuTGCEx_9yY98xjP6IEBE-essmYh1hTXL1j24fpt-6QHPwWHo1dz33RpUHGcBgT6Z6TxpRaeuHc_BqP_pQkiRVfpIqBrTb1KOf98HPGPN1XgklINcZ6a3SdtdX7mHMDookeIbvkRJcc7EVcpG)][[6](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFlIAua-8lQ0yLtaZoLQBjges74qn3Jp1XvdlKT-7r7hdGxcXSpnpaeICHIHOUPM1Q9DwKEl0kzJhbYGN1ybeWCMlJaH48gy2sfJqHEcAYSADT6a4n_7gcRW8G2dbBR3QA%3D)] Even though it is efficient (it only uses 36B active parameters per token), it still needs to load all 132B weights into memory.

*   **To run it normally (FP16):** You need **~320 GB of VRAM**. (This requires roughly 4x Nvidia A100 80GB GPUs linked together).[[7](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQE0vNK4Zy3kvkFbWVVsHSwtIYfUQqu1PITPudqBMfb-Fcg3dE28JOQ6PI8sBHgFJs7qYWFtLumFteVBzY2bFZYVkS_QWQn-ZPT7vZaXvDfm9bnoGjNLrFym7rebvZM%3D)]
*   **To run it compressed (4-bit quantization):** You need **~90 GB of VRAM/RAM**.
    *   *Can it run on CPU?* Theoretically yes, if you have a server with 128GB+ of system RAM. However, it will be **painfully slow** (0.5 to 1 token per second). It would take minutes to generate a single test case.

### 2. It is "Older" (In AI Years)
DBRX was released in **March 2024**.[[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGAyHKuQf250OFuef9c1mdAUpg19mTlT1_nFkPkqCoIeBxTnM2LgdWEHsOu55voTUtcc6__-H2LiGmXS_4EJiJ_yjT1jhmBePgcG98eaabyGKKrD8ytkCu3_XOfTxs5UxfxheYSXF0%3D)][[8](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEHMP4ucnn69_S8tqro3yGgSpNWwCu-bQ3bGykToxq9QSE6UB2ANN4ltE3c25ISLJ158lJ_-XWfIXG5SjPwNyXzJfg8NtRdBl2DPZyRbSwm69kwyh78god4lXtRDncEBD-Wt3zTaaVqyQ%3D%3D)] In the fast-moving AI world, that is a long time ago.
*   **Qwen 2.5 (released late 2024)** and **Llama 3.1** have effectively made DBRX obsolete for most users.
*   **Benchmark Reality:** The **Qwen 2.5 32B** model (which fits on a single consumer GPU or runs decently on a CPU with 32GB RAM) often matches or outperforms DBRX in coding and SQL tasks, despite being **4x smaller**.

### 3. Pros & Cons Summary

| Feature | **DBRX** | **Qwen 2.5 (32B)** |
| :--- | :--- | :--- |
| **Total Size** | **132 Billion Params** (Huge) | **32 Billion Params** (Manageable) |
| **Active Params** | 36B | 32B (Dense) |
| **Hardware Needed** | 4x Enterprise GPUs (or 128GB RAM Mac Studio) | 1x Consumer GPU (24GB VRAM) or 64GB System RAM |
| **Speed** | Slow (unless on massive cluster) | Fast |
| **Coding Skill** | Excellent (State-of-the-Art in early 2024) | Excellent (Matches DBRX with less hardware) |[[9](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQESFmo8LF-lpJu3LgSvWsu7CLOe9J4Wrj9EhZg2q9FC9OPeaSysopN5XXTr-Uq1Io54yuA_cNuX1YvN_Syx05ldxipS5UCOXB1L_s5FbwZwccecGuzCzmwo33bkKFxlhpbhlc3dQQEZ06p7UPltkVXNno_cMrLBwivNanBktQQEKbPlj5I%3D)]

### Verdict
**Do not use DBRX** for your local Data Platform unless you already own a GPU cluster with \$100,000+ worth of hardware.

**Stick to Qwen 2.5 Coder (32B)**. It gives you 95% of DBRX's intelligence but runs on a standard server you likely already have.

---

### User

i didn't mean to use it locally, compare it to the big models.

---

### Model

If you are looking at server-grade deployment (e.g., you have a cluster of A100/H100s or are using an API provider) and want to compare **DBRX** against the other heavyweights like **Llama 3.1 70B**, **Qwen 2.5 72B**, and **DeepSeek**, the landscape changes.

**The short answer:** DBRX was the king of open-source coding models for about two months (March–May 2024). Today, it has been surpassed by **Qwen 2.5** and **Llama 3.1**.

Here is how DBRX stacks up against the current "Big Model" leaders for Data Engineering tasks.

### 1. The Direct Competitor: DBRX vs. Qwen 2.5 (72B)
**Qwen 2.5 (72B)** is the current gold standard for open-source coding and SQL.

*   **Architecture:**
    *   *DBRX:* Mixture-of-Experts (132B params total, 36B active).
    *   *Qwen 2.5:* Dense model (72B params).
*   **Comparison:**
    *   **SQL & Code:** Qwen 2.5 significantly outperforms DBRX on coding benchmarks (HumanEval, MBPP, Spider). Qwen is widely considered to be close to GPT-4o / Claude 3.5 Sonnet level for pure coding.
    *   **Context Window:** Qwen supports up to **128k** tokens. DBRX is natively **32k**. For large schema analysis, Qwen wins.
    *   **Language Support:** Qwen is multilingual; DBRX is heavily English-focused.
*   **Verdict:** **Qwen 2.5 Wins.** If your goal is generating complex SQL queries or dbt tests, Qwen 2.5 72B is "smarter" and understands nuance better than DBRX.

### 2. The Generalist: DBRX vs. Llama 3.1 (70B)
**Llama 3.1 70B** is the industry standard "workhorse."

*   **Comparison:**
    *   **Reasoning:** Llama 3.1 is better at "following instructions" and general reasoning. If you ask it to "Explain *why* this data quality test failed in a business context," Llama usually gives a more coherent answer.
    *   **Ecosystem:** Llama is supported everywhere. DBRX requires specific loader optimizations because of its unique MoE architecture.
    *   **Knowledge Cutoff:** Llama 3.1 is fresher.
*   **Verdict:** **Llama 3.1 70B Wins on General Reasoning.** It generates better documentation and descriptions. However, for pure SQL syntax, it trades blows with DBRX (with Qwen beating them both).

### 3. The Architecture Rival: DBRX vs. Mixtral 8x22B
Both DBRX and Mixtral are **Mixture-of-Experts (MoE)** models.

*   **Comparison:**
    *   **Performance:** DBRX generally beats the older Mixtral 8x7B, but trades blows with the newer **Mixtral 8x22B**.
    *   **Specialization:** DBRX was trained by Databricks specifically on coding and technical data. It often writes better Spark/Databricks-specific code than Mixtral.
*   **Verdict:** **Tie / Context Dependent.** DBRX is still very strong if your stack is explicitly Databricks (Spark SQL, Unity Catalog), as its training data heavily favored that ecosystem.

### 4. The "Godzilla": Llama 3.1 (405B)
If you have infinite compute (e.g., 8x H100s), Llama 405B is in a different league entirely. It rivals GPT-4o. DBRX cannot compete here.

---

### Why you might still choose DBRX
Despite being older, DBRX has one specific niche where it shines: **Databricks Specifics.**

If your platform uses **Delta Lake, Spark SQL, and Unity Catalog** heavily, DBRX has "muscle memory" for this syntax that generic models sometimes miss. It knows the difference between a standard SQL `MERGE` and a Delta Lake `MERGE` intimately because it was trained by the company that built it.

### Final Ranking for "Big" Open Models (Data Eng Focus)

1.  **Qwen 2.5 (72B):** The current king of open-source coding. Best for writing complex SQL checks and dbt tests.
2.  **Llama 3.1 (70B):** The safest choice. Excellent all-rounder, great at writing descriptions and business logic.
3.  **DeepSeek V3:** (Just released) Highly efficient and rivals Qwen in coding, but more complex to deploy.
4.  **DBRX:** Excellent for Spark/Databricks stacks, but slightly behind the curve on general reasoning and pure Python proficiency compared to the newer models above.

**Recommendation:**
If you are deploying a large model to power your Data Quality platform, deploy **Qwen 2.5 72B**. It gives you the highest "SQL IQ" available in the open market today.

---
