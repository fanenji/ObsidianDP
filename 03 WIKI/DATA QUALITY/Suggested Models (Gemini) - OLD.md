---
type: ai-conversation
topic: data-quality
created: 2026-01-15
tags:
  - data-quality
  - llm
  - gemini
---

## MODELLI

1. **Qwen Coder 2.5 14B**
2. **Llama 3.1 8B**
3. **Mistral "Codestral" 22B**
4. **DeepSeek-Coder V2 16B**

## ALTRI

- **Devstral Small (24B)**

## GEMINI

For local data quality generation, you need a model that balances **SQL proficiency** (to write the tests) with **reasoning capabilities** (to understand *what* to test based on column names like "birth_date" vs "transaction_date").

Since you are using **Ollama** (via OpenMetadata), all the models below are available directly through the Ollama library.

Here are the best open-source models for this specific work, ranked by their suitability for Data Engineering tasks.

### 1. Qwen 2.5 Coder (The Current Leader)

Alibaba's Qwen 2.5 "Coder" series is currently widely considered the best open-weight model for coding and SQL tasks, often outperforming larger Llama models in benchmarks.

- **Best Size for On-Prem:** 14B or 32B (if you have the VRAM). Even the 7B is excellent.
- **Ollama Tag:** `ollama run qwen2.5-coder`

| **Pros**                                                                                                                             | **Cons**                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| **SQL Expert:** specifically fine-tuned for code and SQL; understands complex joins and data types better than general models.       | **Chinese Origin:** Some strict enterprise security policies may flag it due to its origin (Alibaba), though the weights are open. |
| **Context Window:** Massive context support (up to 128k), meaning you can feed it very large table schemas without cutting off text. |                                                                                                                                    |
| **Logic:** Excellent at "reasoning" (e.g., inferring that `net_revenue` should be `gross - tax`).                                    |                                                                                                                                    |

### 2. Llama 3.1 (The Safe Standard)

Meta’s latest model is the industry standard. It is a "general purpose" model, which means it is very good at understanding natural language descriptions of your data ("This table contains customer PII") but slightly less specialized in SQL syntax nuances than Qwen Coder.

- **Best Size for On-Prem:** 8B (lightweight) or 70B (heavy duty).
- **Ollama Tag:** `ollama run llama3.1`

| **Pros**                                                                                                           | **Cons**                                                                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **English NLP:** Best-in-class at understanding the *business context* from your table comments and documentation. | **Strict Safety:** Meta models are heavily aligned; sometimes they refuse to generate code if they misinterpret a prompt as "unsafe" (less common in 3.1, but possible). |
| **Ecosystem:** Widely supported; if you hit a bug, someone else has likely fixed it.                               | **Resource Heavy:** The jump from 8B to 70B is huge. There is no "middle ground" (like a 32B model) in the official lineup.                                              |
| **License:** Very permissive community license widely accepted by western enterprises.                             |                                                                                                                                                                          |

### 3. Mistral "Codestral" / Mistral Nemo

Mistral (French AI lab) produces highly efficient models. **Codestral** is their 22B parameter model dedicated to code. Alternatively, **Mistral Nemo (12B)** is a great middle-ground collaboration with NVIDIA.

- **Best Size for On-Prem:** 22B (Codestral) or 12B (Nemo).
- **Ollama Tag:** `ollama run codestral` or `ollama run mistral-nemo`

| **Pros**                                                                                                                 | **Cons**                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| **Code Specialization:** Codestral is trained specifically for code generation and tests (Python/SQL/dbt YAML).          | **Hardware Awkwardness:** The 22B size is awkward for some GPUs (too big for 24GB VRAM unless quantized). |
| **Efficiency:** Mistral models generally punch above their weight class (a 12B Mistral often beats a 14B generic model). |                                                                                                           |

### 4. DeepSeek-Coder V2 (The Specialist)

A specialized "Mixture-of-Experts" (MoE) model. It is exceptionally strong at coding tasks and often beats GPT-4 in coding benchmarks.

- **Best Size for On-Prem:** The "Lite" version (16B) is manageable; the full version is massive (230B+).
- **Ollama Tag:** `ollama run deepseek-coder-v2`

| **Pros**                                                                             | **Cons**                                                                                                                                                   |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SOTA Coding:** arguably the smartest open-source coding model available right now. | **Complex Architecture:** Being a "Mixture of Experts," it can be slower to run (inference latency) on older hardware compared to dense models like Llama. |
| **Huge Context:** Supports very long contexts natively.                              | **VRAM Hungry:** Even the smaller versions can be heavy on memory requirements compared to a simple Llama 8B.                                              |

---

### Hardware Guide: Which one can you run?

Your choice will depend on the **GPU VRAM** available on your on-prem server.

- **< 16GB VRAM (Consumer GPU / Laptop):**
    - *Recommendation:* **Llama 3.1 (8B)** or **Qwen 2.5 Coder (7B)**.
    - *Reason:* These will run fast and leave room for the OS.
- **24GB VRAM (e.g., Nvidia A10, RTX 3090/4090):**
    - *Recommendation:* **Qwen 2.5 Coder (14B)** or **Mistral Nemo (12B)**.
    - *Reason:* You can run these at high precision (FP16) or run slightly larger models (like Codestral 22B) heavily compressed (4-bit quantization).
- **48GB - 80GB VRAM (e.g., A6000, A100, H100):**
    - *Recommendation:* **Qwen 2.5 Coder (32B)**.
    - *Reason:* This is the "sweet spot" for performance. It is smart enough to handle complex data logic but fits comfortably on a single enterprise GPU.

### Final Recommendation for Data Quality

Start with **Qwen 2.5 Coder (14B)** or **32B** depending on your hardware.
It has the best balance of understanding "code logic" (required for writing SQL/dbt tests) and "schema reasoning" (understanding that a column named `email` needs a regex check).

## LOCAL CPU

Yes, absolutely. Running on a CPU is all about keeping the model size small (fewer "parameters") so it fits in your RAM and doesn't take 5 minutes to generate one sentence.

For your use case (reading a schema and suggesting tests), you need a model that is smart at **SQL/Code** but small enough to run fast.

Here are the best **CPU-friendly** models available on Ollama today.

### Top Recommendation: Qwen 2.5 Coder (3B)

This is currently the "pound-for-pound" champion for coding tasks on low-end hardware. It is specifically trained for code and SQL, making it surprisingly capable for its tiny size.

- **Size:** ~2 GB RAM required.
- **Ollama Command:** `ollama run qwen2.5-coder:3b`
- **Pros:**
    - **Specialized:** It is fine-tuned for code, so it understands `CREATE TABLE` and data types better than general chat models of the same size.
    - **Fast:** On a modern CPU (like an M1/M2/M3 Mac or decent Intel i5/i7), it feels almost instantaneous.
    - **Context:** Supports decent context length, so you can paste a medium-sized schema without issue.
- **Cons:**
    - **Reasoning Limits:** It might struggle with very complex business logic (e.g., "suggest a test that correlates revenue with tax laws in Italy") compared to larger models.

### Runner Up: Microsoft Phi-3.5 Mini (3.8B)

Microsoft designed this model specifically to punch above its weight class by training it on "textbook quality" data. It is widely considered the smartest "small" model for reasoning.

- **Size:** ~2.5 GB RAM required.
- **Ollama Command:** `ollama run phi3.5`
- **Pros:**
    - **Reasoning:** Excellent at understanding instructions. If you ask it to "Suggest tests for columns that look like PII", it is very good at inferring context.
    - **Context Window:** It has a massive **128k context window**, meaning you can feed it huge table schemas or even documentation files, and it won't "forget" the beginning.
- **Cons:**
    - **Less SQL Focus:** It is a generalist model. It writes good code, but Qwen Coder is slightly sharper on syntax.

### The Balanced Option: Llama 3.2 (3B)

Released by Meta specifically for edge devices (laptops, phones). It is a shrunk-down version of the powerful Llama 3.1.

- **Size:** ~2.2 GB RAM required.
- **Ollama Command:** `ollama run llama3.2`
- **Pros:**
    - **Tool Use:** It is trained to be very good at using "tools" or formatting output as JSON, which is helpful if you want the suggested tests in a specific format to copy-paste into dbt/Soda.
    - **Ecosystem:** Because it's Llama, it works with almost every prompt template out there.
- **Cons:**
    - In pure coding benchmarks, it often trails slightly behind Qwen Coder.

### The "Ultra-Light" Option: Gemma 2 (2B)

If you are running on a very old server or a machine with **< 4GB of RAM**, this is your best bet. It comes from Google DeepMind.

- **Size:** ~1.5 GB RAM required.
- **Ollama Command:** `ollama run gemma2:2b`
- **Pros:**
    - **Extremely Fast:** It will fly even on older CPUs.
    - **Lightweight:** You can run this alongside your other services (Dremio, Docker) without it choking the server.
- **Cons:**
    - **"Dumb":** At 2B parameters, it hallucinates more often. It might suggest a test for a column that doesn't exist if the schema is too complex.

### Summary Comparison Table for CPU

| **Model**               | **Best Use Case**        | **RAM Needed** | **SQL Ability** | **Speed** |
| ----------------------- | ------------------------ | -------------- | --------------- | --------- |
| **Qwen 2.5 Coder (3B)** | **Best Overall for You** | ~2GB           | ⭐⭐⭐⭐⭐           | ⚡⚡⚡⚡      |
| **Phi-3.5 Mini (3.8B)** | Complex Reasoning        | ~2.5GB         | ⭐⭐⭐⭐            | ⚡⚡⚡       |
| **Llama 3.2 (3B)**      | General Chat / JSON      | ~2.2GB         | ⭐⭐⭐             | ⚡⚡⚡⚡      |
| **Gemma 2 (2B)**        | Extremely Old Hardware   | ~1.5GB         | ⭐⭐              | ⚡⚡⚡⚡⚡     |

**My Advice:**
Start with **Qwen 2.5 Coder 3B**. It strikes the perfect balance for a Data Platform engineer: it speaks "SQL" fluently and is light enough to run on almost any CPU without slowing down your other services.

## BDMX

If you are looking at server-grade deployment (e.g., you have a cluster of A100/H100s or are using an API provider) and want to compare **DBRX** against the other heavyweights like **Llama 3.1 70B**, **Qwen 2.5 72B**, and **DeepSeek**, the landscape changes.

**The short answer:** DBRX was the king of open-source coding models for about two months (March–May 2024). Today, it has been surpassed by **Qwen 2.5** and **Llama 3.1**.

Here is how DBRX stacks up against the current "Big Model" leaders for Data Engineering tasks.

### 1. The Direct Competitor: DBRX vs. Qwen 2.5 (72B)

**Qwen 2.5 (72B)** is the current gold standard for open-source coding and SQL.

- **Architecture:**
    - *DBRX:* Mixture-of-Experts (132B params total, 36B active).
    - *Qwen 2.5:* Dense model (72B params).
- **Comparison:**
    - **SQL & Code:** Qwen 2.5 significantly outperforms DBRX on coding benchmarks (HumanEval, MBPP, Spider). Qwen is widely considered to be close to GPT-4o / Claude 3.5 Sonnet level for pure coding.
    - **Context Window:** Qwen supports up to **128k** tokens. DBRX is natively **32k**. For large schema analysis, Qwen wins.
    - **Language Support:** Qwen is multilingual; DBRX is heavily English-focused.
- **Verdict:** **Qwen 2.5 Wins.** If your goal is generating complex SQL queries or dbt tests, Qwen 2.5 72B is "smarter" and understands nuance better than DBRX.

### 2. The Generalist: DBRX vs. Llama 3.1 (70B)

**Llama 3.1 70B** is the industry standard "workhorse."

- **Comparison:**
    - **Reasoning:** Llama 3.1 is better at "following instructions" and general reasoning. If you ask it to "Explain *why* this data quality test failed in a business context," Llama usually gives a more coherent answer.
    - **Ecosystem:** Llama is supported everywhere. DBRX requires specific loader optimizations because of its unique MoE architecture.
    - **Knowledge Cutoff:** Llama 3.1 is fresher.
- **Verdict:** **Llama 3.1 70B Wins on General Reasoning.** It generates better documentation and descriptions. However, for pure SQL syntax, it trades blows with DBRX (with Qwen beating them both).

### 3. The Architecture Rival: DBRX vs. Mixtral 8x22B

Both DBRX and Mixtral are **Mixture-of-Experts (MoE)** models.

- **Comparison:**
    - **Performance:** DBRX generally beats the older Mixtral 8x7B, but trades blows with the newer **Mixtral 8x22B**.
    - **Specialization:** DBRX was trained by Databricks specifically on coding and technical data. It often writes better Spark/Databricks-specific code than Mixtral.
- **Verdict:** **Tie / Context Dependent.** DBRX is still very strong if your stack is explicitly Databricks (Spark SQL, Unity Catalog), as its training data heavily favored that ecosystem.

### 4. The "Godzilla": Llama 3.1 (405B)

If you have infinite compute (e.g., 8x H100s), Llama 405B is in a different league entirely. It rivals GPT-4o. DBRX cannot compete here.

---

### Why you might still choose DBRX

Despite being older, DBRX has one specific niche where it shines: **Databricks Specifics.**

If your platform uses **Delta Lake, Spark SQL, and Unity Catalog** heavily, DBRX has "muscle memory" for this syntax that generic models sometimes miss. It knows the difference between a standard SQL `MERGE` and a Delta Lake `MERGE` intimately because it was trained by the company that built it.

### Final Ranking for "Big" Open Models (Data Eng Focus)

1. **Qwen 2.5 (72B):** The current king of open-source coding. Best for writing complex SQL checks and dbt tests.
2. **Llama 3.1 (70B):** The safest choice. Excellent all-rounder, great at writing descriptions and business logic.
3. **DeepSeek V3:** (Just released) Highly efficient and rivals Qwen in coding, but more complex to deploy.
4. **DBRX:** Excellent for Spark/Databricks stacks, but slightly behind the curve on general reasoning and pure Python proficiency compared to the newer models above.

**Recommendation:**
If you are deploying a large model to power your Data Quality platform, deploy **Qwen 2.5 72B**. It gives you the highest "SQL IQ" available in the open market today.
