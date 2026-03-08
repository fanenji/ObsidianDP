---
type: note
topic: data-platform
created: 2026-02-17
tags:
  - data-platform
  - openmetadata
---


# INSTALLAZIONE IN LOCALE

Installazione con docker in ~/Development/DP/openmetadata-docker

```yaml
curl -sL -o docker-compose.yml https://github.com/open-metadata/OpenMetadata/releases/download/1.11.0-release/docker-compose.yml
```

- Username: `admin@open-metadata.org`
- Password: `admin`


# PROGETTO TEST DBT


Creato progetto

/Users/stefano/Development/DP/dbt-projects/test_local_openmetadata

Installato pacchetto python

```yaml
pip install "openmetadata-ingestion[dbt]"
```

```bash
# DBT 
# https://docs.open-metadata.org/latest/connectors/ingestion/workflows/dbt
# https://docs.open-metadata.org/latest/connectors/ingestion/workflows/dbt/auto-ingest-dbt-core

pip install "openmetadata-ingestion[dbt]"==1.10.14

metadata --debug ingest-dbt
```

Configurazione dbt-project.yml

```yaml
vars:
  # Required OpenMetadata configuration
  openmetadata_host_port: "http://openmetadata-server.openmetadata-docker.orb.local"
  openmetadata_jwt_token: "your-jwt-token-here"
  openmetadata_service_name: "your-database-service-name"
```



# MCP

## CLAUDE CODE

Configurazione in
- ~/.claude/settings.json
- ~/Library/Application\ Support/Claude/claude_desktop_config.json

```other
{
  "mcpServers": {
    "openmetadata": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://openmetadata-test.dataliguria.it/mcp",
        "--auth-server-url=https://openmetadata-test.dataliguria.it/mcp",
        "--client-id=openmetadata",
        "--verbose",
        "--clean",
        "--header",
        "Authorization:${AUTH_HEADER}"
      ],
      "env": {
        "AUTH_HEADER": "Bearer eyJraWQiOiJHYjM4OWEtOWY3Ni1nZGpzLWE5MmotMDI0MmJrOTQzNTYiLCJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuLW1ldGFkYXRhLm9yZyIsInN1YiI6ImxkYWRtaW4iLCJyb2xlcyI6WyJBZG1pbiJdLCJlbWFpbCI6ImxkYWRtaW5AbGQub3JnIiwiaXNCb3QiOmZhbHNlLCJ0b2tlblR5cGUiOiJQRVJTT05BTF9BQ0NFU1MiLCJpYXQiOjE3NjU4MTg0OTYsImV4cCI6MTc3MzU5NDQ5Nn0.ZN2SxVCtgLYFnWDalhulWw7n_PpGZd2HLOuUNvi6RVlcD_0YGwl3GeltwesKA7NwP2UXvtrdsmWTV13DlVfwT2FqvflvvfWpdGiBplroogzyp2EPa_OnEKH7L75GvdbUsIPT8cifAQ9pRWfkDtbHv32tEHeYkeC8QYnxa_0MxJZalGF7Xody6gRIGBTp_TGUpDRtJWa8XXzERW0jh0k6RHH9hXqKRqM5CAXDE3dcWgffLuXPQaH6Lx1xbE81lPeIMj7ZmBQEtffHHAYWpnbKC-QTLiZe7wl6esHvySpGpZHbIvioymhsn7ss7ZW80xSBqx1mcLZQVbLUqrI8l0MyRg"
      }
    }
  }
}
```

## OPENCODE

**test opencode con devstral local**

test mcp openmetadata (vedi config in claude code)

/Users/stefano/.config/opencode/opencode.json

```other
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-local-mcp-server": {
      "type": "local",
      // Or ["bun", "x", "my-mcp-command"]
      "command": ["npx", "-y", "my-mcp-command"],
      "enabled": true,
      "environment": {
        "MY_ENV_VAR": "my_env_var_value",
      },
    },
  },
}
```

%% MOC START %%
_empty folder_
%% MOC END %%
