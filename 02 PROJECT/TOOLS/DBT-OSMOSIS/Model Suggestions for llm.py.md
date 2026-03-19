
## Endpoints scanned

| Endpoint | Provider | Models found |
|---|---|---|
| `http://10.11.9.76:11434/v1` | Ollama | 14 |
| `http://127.0.0.1:1234/v1` | LM Studio | 7 |

## Task types in llm.py

llm.py performs two categories of tasks that have different requirements:

1. **Structured JSON generation** — model spec, staging spec, semantic analysis → requires high instruction-following accuracy, low temperature (`0.3`)
2. **Free-text generation** — column/table descriptions, NL→SQL → requires good SQL/dbt context understanding, medium temperature (`0.5–0.7`)

---

## Recommended configurations

### 1. Best overall — LM Studio (localhost)

**`qwen/qwen3-coder-30b`**

Dedicated coder model at 30B, runs on MLX (Apple Silicon) for low latency. Best for all structured JSON tasks, SQL generation with `{{ ref() }}`, staging transforms, and semantic analysis.

```bash
LLM_PROVIDER=lm-studio
LM_STUDIO_BASE_URL=http://127.0.0.1:1234/v1
LM_STUDIO_API_KEY=lm-studio
LM_STUDIO_MODEL=qwen/qwen3-coder-30b
```

### 2. Best for NL docs — LM Studio

**`qwen3.5-35b-a3b-mlx-lm`**

MoE architecture — fast despite the size. Best for `generate_style_aware_*()` and `suggest_documentation_improvements()` where free-text quality matters more than JSON precision.

```bash
LLM_PROVIDER=lm-studio
LM_STUDIO_BASE_URL=http://127.0.0.1:1234/v1
LM_STUDIO_API_KEY=lm-studio
LM_STUDIO_MODEL=qwen3.5-35b-a3b-mlx-lm
```

### 3. Best quality on Ollama

**`devstral-small-2:24b-instruct-2512-fp16`**

Mistral's coding model at 24B in full fp16 precision — highest quality on the remote server. Best for structured JSON and staging model specs. Slower than quantized alternatives due to fp16.

```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://10.11.9.76:11434/v1
OLLAMA_API_KEY=ollama
OLLAMA_MODEL=devstral-small-2:24b-instruct-2512-fp16
```

### 4. Best speed/quality ratio on Ollama

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

| Rank | Model                                        | Provider  | Params   | Best for                              | Notes                                     |
| ---- | -------------------------------------------- | --------- | -------- | ------------------------------------- | ----------------------------------------- |
| 1    | `qwen/qwen3-coder-30b`                       | LM Studio | 30B      | JSON, SQL, staging, semantic analysis | **First choice**                          |
| 2    | `qwen3.5-35b-a3b-mlx-lm`                     | LM Studio | 35B MoE  | NL docs, voice-aware generation       | Fast due to MoE                           |
| 3    | `devstral-small-2:24b-instruct-2512-fp16`    | Ollama    | 24B fp16 | Structured JSON, staging spec         | Mistral coding model, slower              |
| 4    | `qwen2.5-coder:14b-instruct-q4_K_M`          | Ollama    | 14B q4   | SQL, model spec, NL-to-SQL            | Good speed/quality ratio                  |
| 5    | `deepseek-coder-v2:16b-lite-instruct-q4_K_M` | Ollama    | 16B q4   | SQL, staging transforms               | Solid alternative                         |
| 6    | `qwen2.5:14b`                                | Ollama    | 14B      | NL documentation                      | Not a coder model, less reliable for JSON |
| 7    | `gemma3:27b`                                 | Ollama    | 27B      | Free-text descriptions                | Not optimized for code or JSON            |

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
