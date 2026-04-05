---
title: "FOSS4GE 2024: Towards Better Data Platforms with Semantic Metadata — Summary"
type: note
topic: data-platform
created: 2026-04-04
tags:
  - mapping
  - semantic
  - rdf
  - dcat
  - metadata
  - geonetwork
  - inspire
source: "[[FOSS4GE 2024  Towards better data platforms with semantic metadata]]"
speakers:
  - Florent Gravin (on behalf of Olivia Guyot)
  - Camp to Camp
event: FOSS4G Europe 2024, Tartu — July 4, 2024
video: https://www.youtube.com/watch?v=DjF2NC-43Rc
slides: https://talks.osgeo.org/foss4g-europe-2024/talk/K3TSFH/
---

# FOSS4GE 2024: Towards Better Data Platforms with Semantic Metadata

**Speakers:** Florent Gravin (presenting on behalf of Olivia Guyot), Camp to Camp
**Event:** FOSS4G Europe 2024 — General Track, Room QFieldCloud (246), July 4, 2024
**Video:** https://www.youtube.com/watch?v=DjF2NC-43Rc

---

## 1. What is Semantic Metadata?

Metadata describes data. Semantic metadata goes further: it describes **what connections a dataset has to the rest of the world**, using a formalised system of meaning rather than rigid structure.

The core idea: instead of a hierarchically structured XML document (where you know an element exists because it's at position X in a schema), semantic metadata is expressed as a **graph of relationships**.

---

## 2. RDF: The Foundation of Semantic Data

**RDF (Resource Description Framework)** is the simplest way to understand semantic data. It models all information as **triples**:

```
Subject → Predicate → Object
```

Each triple is called a **statement**. Examples:

| Subject | Predicate | Object |
|---|---|---|
| `<contact:OliviaGuyot>` | `rdf:type` | `foaf:Person` |
| `<contact:OliviaGuyot>` | `foaf:phone` | `"+41 ..."` (literal) |
| `<dataset:BePop>` | `rdf:type` | `dcat:Dataset` |
| `<dataset:BePop>` | `dct:title` | `"Population"` (literal) |
| `<dataset:BePop>` | `dct:publisher` | `<org:BelgianFPS>` |

Every subject, predicate, and object is either:
- A **URI** — a globally unique identifier pointing to a standardised concept
- A **literal** — plain text (e.g. a title, a date, a phone number)

---

## 3. Knowledge Graphs

When many RDF statements are combined, they form a **Knowledge Graph**: a network of nodes (objects) connected by typed edges (predicates).

The key property: **the graph is traversable**. From any node, you can follow edges to connected nodes, potentially reaching entirely different domains — from a dataset to its publisher, to their organisation, to their country, to a Wikipedia article about that country.

This is the vision Tim Berners-Lee described in 1999: the **Semantic Web**, where all data on the internet is interlinked and machine-readable. Wikidata is a well-known public example.

```
Dataset → published by → Organisation → located in → City → depicted by → Image
                                       ↓
                                       has school → School
```

---

## 4. Ontologies vs. Encodings

A critical distinction:

### 4.1 Ontologies

An **ontology** is a standardised vocabulary of terms — a collection of defined concepts and relationships. Examples:

| Ontology | Purpose |
|---|---|
| **DCAT** (W3C) | Describe datasets and data catalogs |
| **Dublin Core Terms** (dct) | General metadata (title, creator, date, etc.) |
| **FOAF** | People, organisations, social networks |
| **Schema.org** | Google's ontology for web content indexing |

DCAT is **not a format**. It is a set of terms (like `dcat:Dataset`, `dcat:Distribution`, `dct:publisher`) that give meaning to relationships. It does not impose XML, JSON, or any other structure.

### 4.2 Encodings

An encoding is how semantic data is serialised to disk or transmitted over the network. The same knowledge graph can be expressed in multiple encodings:

| Encoding | Notes |
|---|---|
| **Turtle** | Human-readable, concise — common for authoring |
| **JSON-LD** | JSON with a `@context` block — web-friendly |
| **RDF/XML** | The classic W3C format — verbose but widely supported |
| **N-Triples** | Line-by-line, one triple per line — easy to process |

**The graph is the same regardless of encoding.** Encoding is a matter of tooling preference, not semantic meaning.

### Example: Same graph in Turtle

```turtle
@prefix dcat: <http://www.w3.org/ns/dcat#>
@prefix dct: <http://purl.org/dc/terms/>

<dataset:BePop>
    a dcat:Dataset ;
    dct:title "Population" ;
    dct:publisher <org:BelgianFPS> ;
    dct:issued "2023-01-01"^^xsd:date .
```

---

## 5. Why Semantic Metadata Matters

### 5.1 Interoperability Beyond Geospatial

Traditional geospatial standards (ISO 19115, ISO 19139, WMS, CSW) are understood **only** by geospatial systems. A mainstream data warehouse, a search engine, or a BI tool has no concept of these formats.

Semantic metadata (via DCAT, Schema.org, etc.) is the native language of the web. Using it means:
- Google can index your catalog content and provide rich search results
- Non-geospatial systems can discover and consume your datasets
- You bridge the gap between GIS infrastructure and the mainstream data ecosystem

### 5.2 Backward Compatibility

XML schemas suffer from breaking changes. Migrating from ISO 19139 to ISO 19115-3 requires rewriting every metadata document because element positions and names change.

With semantic metadata: you can **add new predicates** to existing resources without breaking anything. Old consumers keep reading what they understand; new consumers discover and use the additional information. There is no concept of a breaking schema change.

### 5.3 Flexible Targeting

Because semantic metadata is a graph (not a document), the same resource can simultaneously satisfy multiple ontologies:

```turtle
<dataset:BePop>
    a dcat:Dataset ;           # satisfies DCAT
    a schema:Dataset ;         # satisfies Schema.org (Google indexing)
    a geodcat:Dataset ;        # satisfies GeoDCAT-AP
    dct:title "Population" .
```

A single metadata graph can produce ISO-compliant XML, DCAT-AP JSON-LD, and Schema.org markup from the same source — without transformation logic.

---

## 6. DCAT and GeoDCAT-AP in Europe

### 6.1 DCAT-AP

**DCAT-AP** (Application Profile for European Data Portals) is the set of guidelines from [SEMIC](https://joinup.ec.europa.eu/collection/semantic-interoperability-community-semic) on how to use DCAT to describe datasets across European open data catalogs.

### 6.2 GeoDCAT-AP

**GeoDCAT-AP** extends DCAT-AP specifically for geospatial data. Key properties:
- A complete GeoDCAT-AP metadata record contains enough information to derive **INSPIRE compliance** — SEMIC provides XSLT transforms for this
- Bridges the geospatial world (INSPIRE) with the broader open data world (DCAT-AP)
- Being adopted progressively across European national data portals

### 6.3 OGC GeoDCAT

The OGC is developing a non-European-specific equivalent: **OGC GeoDCAT** — best practices for representing geospatial metadata semantically for a global audience.

---

## 7. GeoNetwork and GeoNetwork-UI

### 7.1 GeoNetwork (Classic)

GeoNetwork is the dominant geospatial metadata catalog in the INSPIRE ecosystem. It is built on **strictly structured XML formats** (ISO 19139, CSW). This makes semantic metadata challenging to handle natively.

### 7.2 GeoNetwork-UI

**GeoNetwork-UI** is a modern sister project — a toolkit for building catalog frontends using contemporary web technologies. It has a **different metadata reading and writing model** that is more abstract than the classic GeoNetwork core.

This abstraction makes it possible to implement a **semantic-capable module** that:
1. Reads metadata expressed as DCAT/Turtle/JSON-LD
2. Internally represents it as an RDF graph
3. Outputs it in any required encoding (ISO XML, DCAT JSON-LD, Turtle, etc.)

### 7.3 Current GeoNetwork Semantic Capabilities

| Capability | Status |
|---|---|
| DCAT export (catalog endpoint) | Available via GeoNetwork for matters and CSW output |
| DCAT-AP / DCAT Mobility export | Available |
| Harvesting semantic catalogs | Supported |
| Import of DCAT/Turtle in new editor (GeoNetwork-UI) | Available — with automatic conversion between formats |

The video demo shows loading both `application/n-triples` DCAT and Turtle DCAT into the GeoNetwork-UI editor, with automatic format detection and conversion.

---

## 8. Tools and Libraries

Semantic data has mature tooling in all major languages:
- **Python:** `rdflib`, `pyLD`
- **Java:** Apache Jena, RDF4J
- **JavaScript:** `jsonld.js`, `n3.js`

With these libraries, you handle the knowledge graph directly — you do not need to write parsers for Turtle, JSON-LD, or XML separately. The library handles all encodings; you work with triples.

---

## 9. Practical Impact: What You Gain

| Benefit | How |
|---|---|
| **Google indexing** | Embed JSON-LD `Schema:Dataset` in your catalog pages → rich search results |
| **Cross-platform interoperability** | Cloud data warehouses, BI tools, open data portals — all understand DCAT |
| **Link datasets across platforms** | Reference external resources by URI — no data duplication |
| **INSPIRE compliance from DCAT** | GeoDCAT-AP + XSLT → valid INSPIRE records |
| **Schema evolution without breaking** | Add predicates; don't touch old ones |
| **Standardised contact/org references** | Point to shared LDAP/FOAF/Schema.org person URIs instead of duplicating |

---

## 10. Generative AI and Semantic Metadata

From the Q&A: generative AI is useful for **generating semantic metadata from unstructured text**:
- Given a dataset description in natural language, an LLM can extract the correct DCAT predicates and generate a Turtle or JSON-LD record
- Contextual extraction: "return all layers from South America" — the LLM can infer that "Brazil" implies South America without an explicit triple
- AI does not need to build the graph structure itself — it can interpret and answer questions over flat text, but formal semantic representation makes machine-to-machine interoperability reliable

The speaker's observation: semantic representation should be the **starting point** for any new dataset description effort — it is easier to work with small, composable pieces than a large rigid structure.

---

## 11. Key Takeaways

| Topic | Summary |
|---|---|
| **Semantic ≠ format** | DCAT, Dublin Core, FOAF are ontologies (vocabularies), not XML formats |
| **RDF is just triples** | Subject → Predicate → Object — everything is a URI or a literal |
| **Encodings are interchangeable** | Turtle, JSON-LD, RDF/XML all express the same graph |
| **Knowledge Graph** | All triples together form a navigable graph that can reach the entire web |
| **DCAT** | The standard ontology for describing datasets — adopted by EU open data portals |
| **GeoDCAT-AP** | European application profile for geospatial + INSPIRE compliance |
| **GeoNetwork-UI** | Modern toolkit with semantic module — can ingest and output multiple formats |
| **Key advantage** | No breaking schema changes; interoperable with the entire web, not just GIS tools |
| **Generative AI** | Useful for extracting semantic metadata from unstructured descriptions |
