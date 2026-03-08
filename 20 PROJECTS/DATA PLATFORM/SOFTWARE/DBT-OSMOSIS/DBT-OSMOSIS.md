---
type: note
topic: data-platform
created: 2026-02-17
tags:
  - data-platform
  - dbt
---


Prove su [localhost](http://localhost) progetto /Users/stefano/Development/DP/dbt-projects/test_osmosis_ste

REPO: [https://10.11.9.20/data-platform/dbt/test_osmosis_ste.git](https://10.11.9.20/data-platform/dbt/test_osmosis_ste.git)

# INSTALLAZIONE

```yaml
pip install dbt-osmosis dbt-dremio==1.10
```

# CONFIGURAZIONE

Configurato osmosis in dbt_project.yaml

```yaml
models:
  test_osmosis_ste:
    +dbt-osmosis: "_{model}.yml"   
    space_test_osmosis_ste:

...

vars:
  dbt-osmosis:
    sources:
      rete:
        path: "space_test_osmosis_ste/Source/source_table.yml"
```

# TEST GENERAZIONE YAML

lanciato dbt-osmosis yaml refactor → generato yaml e documentazione

modificato my_first_query

lanciato dbt-osmosis yaml refactor → NIENTE

lanciato **dbt build /  dbt docs generate / dbt-osmosis** yaml refactor → aggiornato documentazione

LANCIARE IN ORDINE

```bash
**dbt build
dbt docs generate
dbt-osmosis** yaml refactor
```

# TEST PERSISTENZA MODIFICHE MANUALI

- modificato manualmente source yaml con descrizione e aggiunto una colonna nella first query
- lanciato build / docs generate / osmosis → aggiunto colonna e mantenuto descrizione

# DATA_TYPE

A causa di bug introdotto nella versione 1.14 non viene popolato il data_type delle colonne.

FIX nella repo [https://10.11.9.20/data-platform/dbt/models/dbt-osmosis](https://10.11.9.20/data-platform/dbt/models/dbt-osmosis) (branch fix/data_type)

File: [https://10.11.9.20/data-platform/dbt/models/dbt-osmosis/-/blob/fix/data_type/src/dbt_osmosis/core/osmosis.py?ref_type=heads](https://10.11.9.20/data-platform/dbt/models/dbt-osmosis/-/blob/fix/data_type/src/dbt_osmosis/core/osmosis.py?ref_type=heads)

# **SYNTHESIS**

This feature can make large-scale doc scaffolding easier, but always review and refine any auto-generated text!

## INSTALLAZIONE

```yaml
pip install "dbt-osmosis[openai]”
```

## CONFIGURAZIONE

Non documentato, vedi codice modulo: [https://github.com/z3z1ma/dbt-osmosis/blob/7954ce947d4eac71d19ebd3422f47d25a82fa656/src/dbt_osmosis/core/llm.pyL4](https://github.com/z3z1ma/dbt-osmosis/blob/7954ce947d4eac71d19ebd3422f47d25a82fa656/src/dbt_osmosis/core/llm.pyL4)

```python
provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    
    required_env_vars = {
        "openai": ["OPENAI_API_KEY"],
        "azure-openai": [
            "AZURE_OPENAI_BASE_URL",
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_DEPLOYMENT_NAME",
        ],
        "lm-studio": ["LM_STUDIO_BASE_URL", "LM_STUDIO_API_KEY"],
        "ollama": ["OLLAMA_BASE_URL", "OLLAMA_API_KEY"],
        "google-gemini": ["GOOGLE_GEMINI_API_KEY"],
        "anthropic": ["ANTHROPIC_API_KEY"],
    }
    
export LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://10.11.9.76:11434
export OLLAMA_API_KEY=ollama
export OLLAMA_MODEL='qwen2.5-coder:14b-instruct-q4_K_M'
```

## UTILIZZO

```bash
dbt-osmosis yaml refactor --synthesize
```

# **NOTE**

- non prende i commenti sulle colonne (non si vedono neanche su dremio)
- non prende il tipo dato colonne → patch versione 1.14 salvata su repo gitlab


## DEVELOPMENT: ESECUZIONE CON OSMOSIS LOCALE 

TEST CLAUDE / DBT-OSMOSIS

esecuzione con osmosis locale

```other
cd /Users/stefano/Development/DP/dbt-osmosis
uv add dbt-dremio --dev
uv run dbt-osmosis yaml refactor --project-dir /Users/stefano/Development/DP/dbt-projects/test_local_4 --profiles-dir /Users/stefano/Development/DP/dbt-projects/test_local_4
```

## TEST LLM


Creato fork  in  [https://github.com/sparodi63/dbt-osmosis](https://github.com/sparodi63/dbt-osmosis)

### PROMPT

[https://drive.liguriadigitale.it/apps/files/files/2862989?dir=/DataPlatform&editing=false&openfile=true](https://drive.liguriadigitale.it/apps/files/files/2862989?dir=/DataPlatform&editing=false&openfile=true)

You are a helpful Python Developer and an Expert in dbt.

You will assist in understanding, updating, maintaining, fixing and adding new features on the open source project dbt- osmosis that extends dbt and is not being updated anymore.

This is the clone of a fork of dbt-osmosis, the remote url is [https://github.com/sparodi63/dbt-osmosis](https://github.com/sparodi63/dbt-osmosis)

Consider only the code in the main branch

- Your first task is to describe in detail what it does and produce a thorough documentation (complete with diagrams description and function explanation) provide also a detailed maintainace tasks breakdown
- The second task is to review and summarize the open issues on the original repository at this url: [https://github.com/z3z1ma/dbt-osmosis/issues](https://github.com/z3z1ma/dbt-osmosis/issues), give me an analysis report and a quick summary
- Suggest a solution for issue 278 “Bug: Empty config with empty tags and empty meta keys added.” Write an md file SOLUTION_278.md with a detailed explanation and a detailed plan
- Suggest improvements in the [llm.py](http://llm.py) module and write the suggestions in the LLM_IMPROVEMENTS.md with a plan on how to implement them

%% MOC START %%
_empty folder_
%% MOC END %%
