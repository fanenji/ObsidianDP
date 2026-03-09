---
type: note
topic: data-platform
created: 2026-01-30
tags:
  - dp
  - schema
---

- Vengono fatte modifiche problematiche alla fonte che non sono bloccate dai test sulla fonte -> la PDS viene creata
- Le modifiche sulla fonte provocano problemi alle VDS -> le VDS sono rotte


**SOLUZIONI**
- 1) in prod doppia pipeline
	- stage
	- prod (solo se stage ok)
- 2) se errore in vds rollback su ultimo tag valido
- 3) pds su branch "ingestion" merge su main solo alla fine
