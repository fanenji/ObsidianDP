---
title: "Configurare Claude con server MCP di OpenMetadata"
type: conversation
topic: claude-code
created: 2026-02-13
tags:
  - claude-code
  - mcp
  - tools
  - openmetadata

---
> From: https://claude.ai/chat/838a8df9-232f-49f7-9fc2-d59158f1041c

# you asked

vorrei configurare claude desktop e claude code per usare il server mcp di openmetadata

---

# claude response

Per configurare Claude Desktop e Claude Code per usare il server MCP di OpenMetadata, devi seguire questi passaggi:

## 1. Installazione del Server MCP OpenMetadata

Prima di tutto, installa il server MCP di OpenMetadata:

```bash
npm install -g @modelcontextprotocol/server-openmetadata
```

oppure con npx (senza installazione globale):

```bash
npx @modelcontextprotocol/server-openmetadata
```

## 2. Configurazione di Claude Desktop

Modifica il file di configurazione di Claude Desktop:

**Su macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Su Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Aggiungi la configurazione del server MCP:

```json
{
  "mcpServers": {
    "openmetadata": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-openmetadata"
      ],
      "env": {
        "OPENMETADATA_HOST": "https://tua-istanza-openmetadata.com",
        "OPENMETADATA_TOKEN": "il-tuo-token-jwt"
      }
    }
  }
}
```

## 3. Configurazione di Claude Code

Per Claude Code, crea o modifica il file di configurazione:

`~/.config/claude-code/config.json`

Con la stessa struttura:

```json
{
  "mcpServers": {
    "openmetadata": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-openmetadata"
      ],
      "env": {
        "OPENMETADATA_HOST": "https://tua-istanza-openmetadata.com",
        "OPENMETADATA_TOKEN": "il-tuo-token-jwt"
      }
    }
  }
}
```

## 4. Ottenere le Credenziali OpenMetadata

Per ottenere il token JWT da OpenMetadata:

1. Accedi alla tua istanza OpenMetadata
2. Vai in **Settings** → **Bots** o **Service Accounts**
3. Crea un nuovo bot/service account
4. Genera un JWT token
5. Copia il token nella configurazione

## 5. Riavvio

Dopo aver salvato le configurazioni:
- **Claude Desktop**: riavvia completamente l'applicazione
- **Claude Code**: riavvia il terminale o ricarica la configurazione

Hai già un'istanza di OpenMetadata configurata o hai bisogno di aiuto anche per quella parte?
