---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - data-platform
  - api
---
Script che configura il sistema di API dinamico

Utilizza libreria grestlet

In /geoscripts/opendata/api



**GESTIONE HEADER**

Content-Type

- application/json
- text/html

**GESTIONE PATH**

Lettura pathvar*

**CASI**

- pathvar1=null -> landing page
- pathvar1='openapi' -> swagger
- pathvar1='datasets' -> datasets list
    - pathvar2={dataset_id} -> dataset description + metadata
        - pathvar3='items' -> items list
            - pathvar4={item_id} -> item data
