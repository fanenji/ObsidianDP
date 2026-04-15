---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - data-platform
  - api
---

## Descrizione

Sistema per configurare un sistema di API in sola lettura a partire da metadati su db/json

# Struttura API

**Landing Page**

- Titolo / Descrizione
- Link a SwaggerUI (html/json)
- Link a lista dataset
- Contact Info

[http://localhost:8080/geoservices/apps/ogc-api/LandingPage.html](http://localhost:8080/geoservices/apps/ogc-api/LandingPage.html)

**SwaggerUI**

UI [http://geoservizi.datasiel.net:8083/geoserver/ogc/features/openapi?f=text%2Fhtml](http://geoservizi.datasiel.net:8083/geoserver/ogc/features/openapi?f=text%2Fhtml)

Def API: [http://geoservizi.datasiel.net:8083/geoserver/M1237/ogc/features/openapi?f=application%2Fvnd.oai.openapi%2Bjson%3Bversion%3D3.0](http://geoservizi.datasiel.net:8083/geoserver/M1237/ogc/features/openapi?f=application%2Fvnd.oai.openapi%2Bjson%3Bversion%3D3.0)

- DatasetList
- Dataset
- Item

**METADATI**

| **/conformance**      | **standard  supportati**       |
| --------------------- | ------------------------------ |
| /datasets             | lista dataset                  |
| /datasets/{datasetId} | descrizione dataset + metadati |

**DATI**

| **/datasets/{datasetId}/items**      | **lista elementi del dataset** |
| ------------------------------------ | ------------------------------ |
| /datasets/{datasetId}/items/{itemId} | dati singolo elemento          |
