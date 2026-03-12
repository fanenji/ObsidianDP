---
type: note
topic:
created: 2026-03-10
tags: []
---

DOCS: https://z3z1ma.github.io/dbt-osmosis/

- progetto gitlab con modifiche al codice fatte da khadija 
	- https://gitlab-test.dataliguria.it/data-platform/dbt/dbt-osmosis-1.2.2
- test con ollama http://10.11.9.76:11434/v1
- test du progetto locale dbt su macchina di khadija ==dbtlocalsetup==
- modificato .env per configurazione ollama -> ERRORE non carica modello si aspetta OpenAI (non legge .env)
- modificato codice nel venv locale per leggere .env (modifiche riportate da repo gitlab)
- test synthesize su progetto con modello devstral 
	- descrizioni tavole e colonne in inglese
	- mantiene inalterate descrizioni già esistenti
	- se deve generare poche descrizioni fornisce una descrizione migliore e + dettagliata
- MODIFICHE PROMPT:
	- gestione custom prompt
	- generare descrizioni in italiano
	- maggior dettaglio nelle descrizioni
- TEST SU VARI MODELLI
	


COMANDO
```shell

dbt build
dbt-osmosis yaml refactor --synthesize
```
