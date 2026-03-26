---
title: "Come installare il server mcp di Dremio"
type: conversation
topic: data-platform
created: 2026-02-13
tags:
  - dremio
  - mcp
---
<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Come installare il server mcp di Dremio nella versione self-hosted

Per installare il server MCP di Dremio in versione self-hosted, clona il repository GitHub ufficiale e configura l'accesso al tuo deployment Dremio tramite URI endpoint e token PAT.[^1_1][^1_2]

## Prerequisiti

Installa il package manager `uv` sul tuo sistema.  Identifica l'URI del tuo Dremio (es. `http://localhost:9047/` per Docker o `https://<host>:9047` per Kubernetes) e genera un Personal Access Token (PAT) dalle credenziali Dremio.  Assicurati di avere un client AI compatibile con MCP, come Claude.[^1_3][^1_1]

## Installazione

Apri il terminale, naviga nella directory desiderata e clona il repository: `git clone https://github.com/dremio/dremio-mcp`, poi `cd dremio-mcp`.  Verifica l'installazione con `uv run dremio-mcp-server --help`; dovresti vedere i comandi disponibili come `run`, `tools` e `config`.[^1_2][^1_1]

## Configurazione

Crea il file di configurazione DremioAI: `uv run dremio-mcp-server config create dremioai --uri <tuo-uri> --pat <tuo-pat>`.  Crea la configurazione per Claude: `uv run dremio-mcp-server config create claude`.  Verifica con `uv run dremio-mcp-server config list --type dremioai` e `--type claude`.[^1_4][^1_1]

## Avvio e Uso

Avvia il server con `uv run dremio-mcp-server run`.  Usa modalità come `FOR_DATA_PATTERNS` per query SQL naturali o `FOR_SELF` per analisi di performance, integrandolo con client AI per esplorare dati Dremio.  I job appaiono nella console Dremio filtrati per "External Tools".[^1_1][^1_2]
<span style="display:none">[^1_10][^1_5][^1_6][^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://lobehub.com/it/mcp/dremio-dremio-mcp?activeTab=deployment

[^1_2]: https://docs.dremio.com/current/mcp-server/

[^1_3]: https://docs.dremio.com/current/developer/mcp-server/

[^1_4]: https://lobehub.com/mcp/dremio-dremio-mcp

[^1_5]: https://www.reddit.com/r/mcp/comments/1k0lm0t/how_do_you_install_mcp_servers/

[^1_6]: https://lobehub.com/it/mcp/neelkamal0666-dremio-mcp?activeTab=deployment

[^1_7]: https://www.youtube.com/watch?v=Zfxj3a7_xJw

[^1_8]: https://www.dremio.com/blog/using-dremios-mcp-server-with-agentic-ai-frameworks/

[^1_9]: https://www.youtube.com/watch?v=Dy3-pF0Ks1U

[^1_10]: https://www.youtube.com/watch?v=MFdKrjp5Kv4
