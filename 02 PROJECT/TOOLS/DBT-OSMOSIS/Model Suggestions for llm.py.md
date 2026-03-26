
## Endpoint scanned

| Endpoint                     | Provider | Models found |
| ---------------------------- | -------- | ------------ |
| `http://10.11.9.76:11434/v1` | Ollama   | 14           |
|                              |          |              |


## Task types in llm.py

llm.py performs two categories of tasks that have different requirements:

1. **Structured JSON generation** — model spec, staging spec, semantic analysis → requires high instruction-following accuracy, low temperature (`0.3`)
2. **Free-text generation** — column/table descriptions, NL→SQL → requires good SQL/dbt context understanding, medium temperature (`0.5–0.7`)

---

## Recommended configurations

### 3. Best all-round

**`qwen3.5:27b`** (Q4_K_M consigliato)

Modello denso di nuova generazione (architettura ibrida Gated DeltaNet + Gated Attention + sparse MoE). **Prima scelta su Ollama** per tutti i task di llm.py: eccelle sia sulla generazione JSON strutturata (IFEval 95%, thinking mode) sia sulla documentazione free-text e NL→SQL. Context window 262K token — ottimo per repository dbt di grandi dimensioni.

**Thinking mode** — abilitato di default; gestirlo in base al task:
- JSON strutturato (temp `0.3`): lasciarlo attivo, migliora l'accuratezza
- Free-text / NL docs (temp `0.5–0.7`): disabilitarlo aggiungendo `/no_think` al system prompt per ridurre la latenza

```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://10.11.9.76:11434/v1
OLLAMA_API_KEY=ollama
OLLAMA_MODEL=qwen3.5:27b   # verificare il tag esatto disponibile su Ollama
```

> **vs qwen3-coder-30b su Ollama**: qwen3-coder-30B ha solo 3.3B parametri attivi (MoE sparse), il che lo rende velocissimo e leggero (~5 GB VRAM) ma lo penalizza sui task NL free-text. Qwen3.5-27B è più lento (~15 GB VRAM in q4) ma copre tutti i requisiti di llm.py con qualità superiore — è la scelta giusta come modello unico.

### 4. Best quality on Ollama (alternativa coding-focused)

**`devstral-small-2:24b-instruct-2512-fp16`**

Mistral's coding model at 24B in full fp16 precision — highest quality on the remote server. Best for structured JSON and staging model specs. Slower than quantized alternatives due to fp16.

```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://10.11.9.76:11434/v1
OLLAMA_API_KEY=ollama
OLLAMA_MODEL=devstral-small-2:24b-instruct-2512-fp16
```

### 5. Best speed/quality ratio on Ollama

**`qwen2.5-coder:14b-instruct-q4_K_M`**

14B coder instruct with q4 quantization — fast and reliable for SQL and JSON output.

```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://10.11.9.76:11434/v1
OLLAMA_API_KEY=ollama
OLLAMA_MODEL=qwen2.5-coder:14b-instruct-q4_K_M
```

---

## Full rankings

| Rank | Model                                        | Provider | Params       | Best for                      | Notes                                                    |
| ---- | -------------------------------------------- | -------- | ------------ | ----------------------------- | -------------------------------------------------------- |
| 3    | `qwen3.5:27b`                                | Ollama   | 27B (ibrido) | Tutti i task — all-round      | **Best** — thinking mode, IFEval 95%, 262K ctx           |
| 4    | `devstral-small-2:24b-instruct-2512-fp16`    | Ollama   | 24B fp16     | Structured JSON, staging spec | Mistral coding model, slower; alternativa coding-focused |
| 5    | `qwen2.5-coder:14b-instruct-q4_K_M`          | Ollama   | 14B q4       | SQL, model spec, NL-to-SQL    | Good speed/quality ratio                                 |
| 6    | `deepseek-coder-v2:16b-lite-instruct-q4_K_M` | Ollama   | 16B q4       | SQL, staging transforms       | Solid alternative                                        |
| 7    | `nemotron-3-nano:30b`                        | Ollama   | 30B tot / 3.5B att | Reasoning con tool calling | MoE + Mamba-2 SSM; forte su AIME25 (99.2%), debole su coding/JSON vs qwen3.5; supporto Ollama da verificare |
| 8    | `qwen2.5:14b`                                | Ollama   | 14B          | NL documentation              | Not a coder model, less reliable for JSON                |
| 9    | `gemma3:27b`                                 | Ollama   | 27B          | Free-text descriptions        | Not optimized for code or JSON                           |

---

## Models to avoid

| Model | Reason |
|---|---|
| `text-embedding-nomic-embed-text-v1.5` | Embedding model — not generative |
| `deepseek-ocr:latest` | Specialized for OCR, not relevant |
| `glm-4.7-flash:latest` | Primarily Chinese-language oriented |
| `gemma3:4b-it-fp16` | Too small (4B) for reliable structured JSON |
| `gemma2:9b` | Too small for complex instruction following |
| `qwen/qwen3-4b-thinking-2507` | 4B thinking model — slow and too small |
| `codegemma:7b-code-q4_K_M` | Base (non-instruct) model — cannot follow chat instructions |
