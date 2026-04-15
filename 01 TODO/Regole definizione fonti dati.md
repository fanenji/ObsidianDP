---
type: note
topic:
created: 2026-04-09
tags: []
---
---

TODO
- Specifiche per DBA
- Test Postgres public su db-test
- 

----


Regole per la definizione delle fonti dati su 
- OpenMetadata
- Dremio

PREREQUISITO
Un utente con accesso ai dati dello schema su cui risiedono le tabelle
- L'utente deve avere accesso alle tavole (preferibilmente) in sola lettura
- L'utente deve avere accesso in lettura alle tavole di sistema DBA_*

Definire sorgente dremio/omd che punta al db con l'utente definito

Regole per il nome:
- Nome dovrebbe comprendere: Server+Istanza+Schema/Utente

```
SCHEMA@SERVER_ISTANZA (RETE@AMB_DB_AMB)
SERVER_ISTANZA_SCHEMA (AMB_DB_AMB_RETE)
```

SCHEMI MULTIPLI
Se progetto prevede sorgenti da schemi diversi utilizzare utente con accesso agli oggetti dei vari schemi


FILTRI IN OpenMetadata
Tavole possono essere filtrate con regex, per esempio per filtrare tutte le tavole che iniziano per RQA

`^RQA.*`

---



![[Pasted image 20260415103303.png]]


