---
type: moc
topic: data-platform
created: 2026-02-21
tags:
  - data-platform
  - api
---

## NOTE

- Gestione content-type (html/json)
- Versionamento api
- Gestione link / HATEOAS
- Gestione paginazione
- Filtri con CQL

## ESEMPI

Hugging Face Data Viewer

**HUGGING FACE DATASET VIEWER**

[🤗 Dataset viewer](https://huggingface.co/docs/datasets-server/index)

[jamescalam/world-cities-geo · Datasets at Hugging Face](https://huggingface.co/datasets/jamescalam/world-cities-geo)

API

- ROWS: [https://datasets-server.huggingface.co/rows?dataset=jamescalam%2Fworld-cities-geo&config=default&split=train&offset=0&length=100](https://datasets-server.huggingface.co/rows?dataset=jamescalam%2Fworld-cities-geo&config=default&split=train&offset=0&length=100)
- SEARCH: [https://datasets-server.huggingface.co/search?dataset=jamescalam/world-cities-geo&config=default&split=train&query=Italy](https://datasets-server.huggingface.co/search?dataset=jamescalam/world-cities-geo&config=default&split=train&query=Italy)
- FILTER: [https://datasets-server.huggingface.co/filter?dataset=jamescalam/world-cities-geo&config=default&split=train&where=country='Italy'](https://datasets-server.huggingface.co/filter?dataset=jamescalam/world-cities-geo&config=default&split=train&where=country=%27Italy%27)

%% MOC START %%
- [[SISTEMA API - CONFIGURATORE API]]
- [[SISTEMA API - SCRIPT GROOVY]]
%% MOC END %%
