---
title: "RDF Ontology Integration in OpenMetadata"
type: note
topic: data-platform
created: 2026-04-04
tags:
  - openmetadata
  - rdf
  - sparql
  - knowledge-graph
  - tools
---

https://github.com/open-metadata/OpenMetadata/issues/22853


# RDF Ontology Integration in OpenMetadata: Architecture and Implementation

**Issue #22853** | Author: @harshach | Status: CLOSED (COMPLETED)
Published: August 9, 2025 | Last Updated: March 22, 2026

---

## Executive Summary

OpenMetadata's RDF integration introduces a sophisticated knowledge graph layer that enriches the metadata catalog with semantic capabilities. This feature enables semantic search, graph-based analytics, reasoning, and standards-compliant data catalog federation.

---

## Purpose and Motivation

### Why RDF Integration?

1. **Semantic Interoperability**: Participation in the broader semantic web ecosystem
2. **Advanced Querying**: SPARQL enables graph traversal beyond traditional SQL
3. **Standards Compliance**: W3C standards (RDF, SPARQL, DCAT) ensure compatibility
4. **Knowledge Graph Leverage**: Existing entity relationships in JsonSchema are mapped to standards
5. **Reasoning Capabilities**: RDFS/OWL reasoning infers new relationships
6. **Federation**: Cross-catalog queries using standardized protocols

### Design Principles

- **Non-intrusive**: RDF operates alongside existing functionality
- **Pluggable**: Multiple RDF storage backends supported
- **Standards-based**: Full W3C specification compliance
- **Performance-conscious**: Asynchronous updates, caching, query optimization
- **Extensible**: Easy ontology mapping and reasoning rule additions

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ OpenMetadata Application                                        │
├─────────────────────────────────────────────────────────────────┤
│ REST API Layer                                                  │
│ ┌─────────────┐ ┌──────────────┐ ┌────────────────────────┐   │
│ │ Entity APIs │ │ RDF APIs     │ │ Search & Analytics API │   │
│ └─────────────┘ └──────────────┘ └────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│ Service Layer                                                   │
│ ┌─────────────────────┐ ┌─────────────────────────────────┐   │
│ │ Entity Repositories │ │ RDF Repository                  │   │
│ │ - Create/Update     │ │ ┌─────────────┐ ┌────────────┐ │   │
│ │ - Delete            │─┼─▶│ RDF Updater │ │SPARQL Query│ │   │
│ └─────────────────────┘ │ └─────────────┘ └────────────┘ │   │
│                         └─────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│ RDF Translation Layer                                           │
│ ┌──────────────┐ ┌───────────────┐ ┌────────────────────┐     │
│ │ JSON-LD      │ │ Entity to RDF │ │ SQL to SPARQL      │     │
│ │ Contexts     │ │ Converters    │ │ Translator         │     │
│ └──────────────┘ └───────────────┘ └────────────────────┘     │
├─────────────────────────────────────────────────────────────────┤
│ Storage Layer                                                   │
│ ┌────────────────────────┐ ┌─────────────────────────────┐    │
│ │ Apache Jena Fuseki     │ │ QLever                      │    │
│ │ (Default Backend)      │ │ (High-Performance Backend)  │    │
│ └────────────────────────┘ └─────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. RDF Repository

Central orchestrator for RDF operations (`org.openmetadata.service.rdf.RdfRepository`):

```java
public class RdfRepository {
  // Core operations
  public void createEntity(EntityInterface entity)
  public void updateEntity(EntityInterface original, EntityInterface updated)
  public void deleteEntity(EntityReference reference)
  // Query operations
  public JsonNode executeSparqlQuery(String query)
  public void executeSparqlUpdate(String update)
  // Advanced features
  public SemanticSearchResult semanticSearch(String query, String entityType)
  public List<SimilarEntity> findSimilarEntities(String entityType, UUID entityId)
  public RecommendationResult getUserRecommendations(UUID userId)
}
```

### 2. Entity to RDF Conversion

**Ontology Mapping** (`resources/rdf/openmetadata.ttl`):

```turtle
@prefix om: <https://open-metadata.org/ontology/> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .

# Service hierarchy
om:Service a rdfs:Class ;
  rdfs:subClassOf dcat:DataService .
om:DatabaseService rdfs:subClassOf om:Service .
om:MessagingService rdfs:subClassOf om:Service .
om:DashboardService rdfs:subClassOf om:Service .

# Data asset hierarchy
om:DataAsset a rdfs:Class ;
  rdfs:subClassOf dcat:Dataset .
om:Table rdfs:subClassOf om:DataAsset .
om:Dashboard rdfs:subClassOf om:DataAsset .
om:Pipeline rdfs:subClassOf om:DataAsset .
```

**JSON-LD Context Example**:

```json
{
  "@context": {
    "@vocab": "https://open-metadata.org/ontology/",
    "name": "http://purl.org/dc/terms/title",
    "description": "http://purl.org/dc/terms/description",
    "owner": {
      "@id": "https://open-metadata.org/ontology/owner",
      "@type": "@id"
    }
  }
}
```

### 3. RDF Updater

Handles entity conversion and synchronization (`org.openmetadata.service.rdf.RdfUpdater`):

```java
public class RdfUpdater {
  public static void createEntity(EntityInterface entity) {
    Model model = convertEntityToRdf(entity);
    rdfRepository.addModel(model);
  }
  
  private static Model convertEntityToRdf(EntityInterface entity) {
    // 1. Load appropriate JSON-LD context
    // 2. Convert entity to JSON
    // 3. Apply JSON-LD processing
    // 4. Generate RDF model
  }
}
```

### 4. SPARQL Query Engine

**SQL to SPARQL Translation**:

```java
public class SqlToSparqlTranslator {
  public String translate(String sql) {
    // Parse SQL using Apache Calcite
    SqlNode sqlNode = parser.parse(sql);
    // Convert to SPARQL
    return convertToSparql(sqlNode);
  }
}
```

**Example Translation**:

```sql
-- SQL
SELECT name, description FROM table WHERE service = 'MySQL'
```

```sparql
-- SPARQL equivalent
PREFIX om: <https://open-metadata.org/ontology/>
SELECT ?name ?description WHERE {
  ?table a om:Table ;
    om:name ?name ;
    om:description ?description ;
    om:service/om:name "MySQL" .
}
```

### 5. Advanced Features

**Semantic Search**:

```java
public SemanticSearchResult semanticSearch(String query, String entityType) {
  // 1. Generate embeddings for query
  float[] queryEmbedding = embeddingService.embed(query);
  // 2. Find similar entities using vector similarity
  String sparql = buildSemanticSearchQuery(queryEmbedding, entityType);
  // 3. Execute query and rank results
  return executeAndRankResults(sparql);
}
```

**Lineage Inference**:

```sparql
# Transitive lineage query
PREFIX om: <https://open-metadata.org/ontology/>
SELECT ?downstream WHERE {
  <entity-uri> om:hasDownstreamLineage+ ?downstream .
}
```

---

## Implementation Details

### Entity Lifecycle Integration

RDF updates integrated via hooks in `EntityRepository`:

```java
public abstract class EntityRepository<T extends EntityInterface> {
  protected void postCreate(T entity) {
    if (rdfEnabled) RdfUpdater.createEntity(entity);
  }
  protected void postUpdate(T original, T updated) {
    if (rdfEnabled) RdfUpdater.updateEntity(original, updated);
  }
  protected void postDelete(T entity, boolean hardDelete) {
    if (rdfEnabled && hardDelete) RdfUpdater.deleteEntity(entity.getEntityReference());
  }
}
```

### Storage Backend Abstraction

```java
public interface RdfStorageInterface {
  void executeUpdate(String sparqlUpdate);
  JsonNode executeQuery(String sparqlQuery);
  void loadData(Model model, String graphUri);
  void deleteGraph(String graphUri);
}

public class FusekiStorage implements RdfStorageInterface { ... }
public class QLeverStorage implements RdfStorageInterface { ... }
```

### Performance Optimizations

- **Asynchronous Updates**: Changes queued for async processing
- **Batch Operations**: Multiple updates combined into single SPARQL operations
- **Caching**: Query results cached with TTL expiration
- **Connection Pooling**: HTTP connection reuse to RDF backend

### Security

- **Authentication**: Basic auth and custom authentication support
- **Query Validation**: SPARQL queries validated before execution
- **Resource Limits**: Query timeout and result size limits
- **Access Control**: Integration with OpenMetadata permissions

---

## REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/rdf/status` | RDF service status |
| `GET` | `/api/v1/rdf/entity/{entityType}/{id}` | Get entity as RDF |
| `POST` | `/api/v1/rdf/sparql` | Execute SPARQL query |
| `POST` | `/api/v1/rdf/sparql/update` | Execute SPARQL update |
| `GET` | `/api/v1/rdf/graph/explore/{entityType}/{id}` | Graph exploration |
| `GET` | `/api/v1/rdf/search/semantic` | Semantic search |
| `GET` | `/api/v1/rdf/search/similar/{entityType}/{id}` | Find similar entities |
| `GET` | `/api/v1/rdf/recommendations/user/{userId}` | User recommendations |
| `POST` | `/api/v1/rdf/lineage/infer` | Lineage inference |

---

## SPARQL Query Examples

**Find all tables with PII data:**

```sparql
PREFIX om: <https://open-metadata.org/ontology/>
PREFIX tag: <https://open-metadata.org/tag/>
SELECT ?table ?column WHERE {
  ?table a om:Table ;
    om:hasColumn ?column .
  ?column om:hasTag tag:PII .
}
```

**Data asset discovery by domain:**

```sparql
PREFIX om: <https://open-metadata.org/ontology/>
SELECT ?asset ?type WHERE {
  ?asset om:domain <https://open-metadata.org/domain/Marketing> ;
    a ?type .
  ?type rdfs:subClassOf om:DataAsset .
}
```

**Impact analysis (transitive lineage):**

```sparql
PREFIX om: <https://open-metadata.org/ontology/>
SELECT ?impacted WHERE {
  <table-uri> om:hasDownstreamLineage+ ?impacted .
  FILTER EXISTS { ?impacted om:hasOwner ?owner }
}
```

---

## Configuration

```yaml
rdfConfiguration:
  enabled: true
  storageType: FUSEKI       # or QLEVER
  remoteEndpoint: http://fuseki:3030/openmetadata
  username: admin
  password: ${RDF_PASSWORD}
  dataset: openmetadata
  baseUri: https://metadata.company.com/
  queryTimeout: 30000
  maxResultSize: 10000
  enableInference: true
  reasonerType: RDFS        # or OWL
```

### Initial Data Load

```bash
./openmetadata-app-rdf-index \
  --config openmetadata.yaml \
  --entities "table,dashboard,pipeline" \
  --batch-size 1000
```

---

## Use Cases

| Use Case | Capability |
|----------|-----------|
| Semantic Data Discovery | Natural language queries, concept-based search, cross-domain discovery |
| Advanced Lineage | Transitive queries, multi-hop impact analysis, pattern detection |
| Compliance & Governance | Tag-based asset discovery, regulatory tracking, automated enforcement |
| Recommendation Engine | Similar dataset suggestions, collaborative filtering, usage pattern analysis |
| Federation & Integration | Multi-instance queries, external knowledge graph linking, standards-based exchange |

---

## Future Enhancements

1. **Enhanced Reasoning**: SWRL rules, probabilistic reasoning, temporal reasoning
2. **Graph Analytics**: Apache Spark GraphX integration, GNNs, community detection
3. **Advanced Visualization**: Interactive explorer, 3D visualization, AR lineage
4. **Federation Improvements**: Distributed query optimization, entity resolution, blockchain trust
5. **AI/ML Integration**: Graph-based feature engineering, knowledge graph embeddings, automated ontology learning

---

> **Source**: [open-metadata/OpenMetadata#22853](https://github.com/open-metadata/OpenMetadata/issues/22853)
