---
type: note
topic:
created: 2026-03-10
tags: []
---

DOCS: https://z3z1ma.github.io/dbt-osmosis/

- progetto gitlab con modifiche al codice fatte da khadija 
	- https://gitlab-test.dataliguria.it/data-platform/dbt/dbt-osmosis-1.2.2
- documentazione con Claude del modulo llm.py
- suggerimento modelli in /llm-models-suggestion.md
- benchmark per test di modelli e prompt in dir /benchmark
- test con 
	- ollama http://10.11.9.76:11434/v1 
	- lm-studio http://127.0.0.1:1234/v1
- test su progetto dbt demo_dremio in dbt-osmosis-1.2.2
	- descrizioni tavole e colonne in inglese
	- mantiene inalterate descrizioni già esistenti
	- se deve generare poche descrizioni fornisce una descrizione migliore e + dettagliata

TODO
- MODIFICHE PROMPT:
	- gestione custom prompt
	- descrizioni in italiano
	- maggior dettaglio nelle descrizioni
- SPIEGAZIONE FLUSSO ELABORAZIONE DEL MODULO llm.py
- BENCHMARK - script che prende le elaborazioni effettuate e crea tabella riassuntiva
- TEST MODELLI
- MODELLI DEDICATI PER DIVERSI TASK: vedi [[Model Suggestions for llm.py]]







COMANDO
```shell

dbt build
dbt-osmosis yaml refactor --synthesize
```
