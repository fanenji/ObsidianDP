---
title: "Property Graphs vs. Rigid Ontologies: Choosing the Right Foundation for Enterprise AI Memory"
source: https://medium.com/graph-praxis/property-graphs-vs-rigid-ontologies-choosing-the-right-foundation-for-enterprise-ai-memory-defe5df2ae95
author:
  - "[[Alexander Shereshevsky]]"
published: 2026-01-20
created: 2026-04-02
description: "Property Graphs vs. Rigid Ontologies: Choosing the Right Foundation for Enterprise AI Memory Part 1 of the “Knowledge Graphs for Enterprise AI Memory” series You’ve decided that vector search …"
tags:
  - clippings
  - knowledge-graph
  - ontology
  - ai
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)## [Graph Praxis](https://medium.com/graph-praxis?source=post_page---publication_nav-4877625dfe3e-defe5df2ae95---------------------------------------)

[![Graph Praxis](https://miro.medium.com/v2/resize:fill:57:57/1*rUElHORNRlPmVu9QZUkR-A.png)](https://medium.com/graph-praxis?source=post_page---post_publication_sidebar-4877625dfe3e-defe5df2ae95---------------------------------------)

Where knowledge graph theory meets production reality. Enterprise architectures for Graph RAG, dynamic ontologies, and AI agents that actually remember.

*Part 1 of the “Knowledge Graphs for Enterprise AI Memory” series*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*3kGpd9ENWLO8MaKshSrvtw.png)

You’ve decided that vector search alone isn’t cutting it. Your RAG system returns semantically similar chunks, but it can’t answer “which projects does Sarah manage that depend on the delayed infrastructure migration?” That question requires understanding *relationships* — and relationships are where knowledge graphs shine.

But here’s where most teams stumble: they start researching knowledge graphs and immediately fall into a religious war between RDF/OWL purists and property graph pragmatists. One camp insists on formal ontologies with inference engines. The other just wants to model their data and move on.

After building knowledge graphs for enterprise AI systems across financial services, pharma, and legal tech, I’ve developed a clear position: **property graphs win for 90% of AI memory use cases**. This article explains why — and when the other 10% matters.

## The Core Trade-off: Flexibility vs. Formalism

Both approaches model entities and relationships. The difference lies in how strictly they enforce structure and what capabilities that structure enables.

**Property graphs** (FalkorDB, Neo4j, Kuzu) store nodes and edges with arbitrary key-value properties attached to both. There’s no central authority that declares which node types can exist or which relationships are valid. You can add a new property to any node without updating a schema. You can create relationship types on the fly.

**RDF/OWL graphs** (Stardog, GraphDB, Virtuoso) enforce a formal ontology — a declared vocabulary of classes, properties, and logical constraints. Every triple must conform to the ontology. The payoff: you get inference engines that can derive new facts from existing ones.

Here’s the same information modeled both ways:

## Property Graph (Cypher)

```c
// Create nodes with flexible properties
CREATE (sarah:Person {
  name: "Sarah Chen",
  title: "Engineering Manager",
  department: "Platform",
  hire_date: date("2019-03-15"),
  slack_handle: "@schen"  // Added later, no schema change needed
})

CREATE (migration:Project {
  name: "Infrastructure Migration",
  status: "delayed",
  target_date: date("2024-06-01"),
  risk_level: "high"  // Business decided to track this last week
})

// Create relationship with its own properties
CREATE (sarah)-[:MANAGES {
  since: date("2023-01-01"),
  allocation_pct: 40
}]->(migration)
```

## RDF/OWL (Turtle + SPARQL)

```c
# First, define the ontology (required before any data)
@prefix org: <http://example.org/ontology/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

org:Person a owl:Class .
org:Project a owl:Class .
org:manages a owl:ObjectProperty ;
    rdfs:domain org:Person ;
    rdfs:range org:Project .
org:name a owl:DatatypeProperty ;
    rdfs:range xsd:string .
# ... 20 more property definitions ...

# Then, add data conforming to ontology
org:sarah a org:Person ;
    org:name "Sarah Chen" ;
    org:title "Engineering Manager" ;
    org:manages org:migration .

org:migration a org:Project ;
    org:name "Infrastructure Migration" ;
    org:status "delayed" .
```

Notice the difference in overhead. The property graph version is self-describing — you understand the model by reading the data. The RDF version requires understanding the ontology first, and adding that `slack_handle` property requires ontology modification and revalidation.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*GFjZxpSGkMXkZQ1y0KTTSA.png)

## Why This Matters for AI Memory Systems

Enterprise AI memory has a unique characteristic that favors flexibility: **your extraction models will improve**.

When you first build your knowledge graph, you might extract basic entities:

```c
# Week 1: Basic extraction
entities = extract_entities(document)
# Returns: [("Sarah Chen", "PERSON"), ("Infrastructure Migration", "PROJECT")]
```

Three months later, your extraction pipeline has evolved:

```c
# Week 12: Richer extraction with relationships and attributes
entities = extract_entities_v3(document)
# Returns: [
#   {"name": "Sarah Chen", "type": "PERSON", "role": "manager", 
#    "sentiment": "concerned", "mentioned_with": ["budget", "timeline"]},
#   {"name": "Infrastructure Migration", "type": "PROJECT",
#    "phase": "execution", "health": "at_risk", 
#    "blockers": ["vendor_delay", "resource_gap"]}
# ]
```

With property graphs, you ingest this richer data immediately. Old nodes gain new properties; new relationship types appear organically. Your graph *grows* with your capabilities.

With rigid ontologies, each extraction improvement triggers ontology renegotiation. In my experience, teams either:

- Slow their ML iteration to match ontology governance (bad for AI development)
- Accumulate technical debt by jamming new data into an ill-fitting schema (bad for data quality)
- Abandon the ontology entirely (wasted effort)

## The 10% Where RDF Wins

Formal ontologies aren’t pointless — they’re specialized tools for specific problems:

## 1\. Cross-Organization Data Sharing

When multiple enterprises must share knowledge graphs with guaranteed interoperability, agreed-upon ontologies prevent chaos. Healthcare’s SNOMED CT and pharmaceuticals’ ChEMBL work precisely because everyone commits to the same formal vocabulary.

```c
# Query works across any system using the standard ontology
SELECT ?drug ?target ?disease
WHERE {
  ?drug chembl:hasTarget ?target .
  ?target sio:isAssociatedWith ?disease .
  ?disease rdf:type doid:Disease .
}
```

## 2\. Regulatory Explainability Requirements

Some domains require provable reasoning chains. If a regulator asks “why did your system flag this transaction?”, you need more than “the embedding similarity was high.”

OWL inference provides auditable logic:

```c
# Ontology rule
org:HighRiskTransaction owl:equivalentClass [
  owl:intersectionOf (
    org:Transaction
    [owl:onProperty org:amount ; owl:minCardinality 100000]
    [owl:onProperty org:destination ; owl:someValuesFrom org:HighRiskJurisdiction]
  )
] .

# Given data, reasoner automatically derives:
org:txn_4521 a org:HighRiskTransaction .  # Inferred, with full explanation
```

## 3\. Complex Hierarchical Reasoning

When you need inference like “if X is a subclass of Y, and entity A is type X, then A is also type Y” — and this matters for your queries — RDF’s RDFS/OWL inference is purpose-built for it.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*hgtx9b-Yu6q6H-j4NtC71Q.png)

## Practical Architecture: Property Graphs for AI Memory

Here’s the architecture pattern I recommend for enterprise AI memory systems:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*5Pu44zoXZW7Eb79YvIRd5Q.png)

The key insight: **schema constraints belong in your application layer, not your database layer**. You can enforce business rules in code while keeping the underlying graph flexible:

```c
class ProjectNode:
    """Application-level schema for Project entities."""
    
    required_properties = ["name", "status"]
    optional_properties = ["target_date", "risk_level", "owner_id"]
    valid_statuses = ["planning", "active", "delayed", "completed"]
    
    @classmethod
    def validate(cls, node_data: dict) -> bool:
        # Check required fields
        for prop in cls.required_properties:
            if prop not in node_data:
                raise ValidationError(f"Missing required property: {prop}")
        
        # Validate enums
        if node_data.get("status") not in cls.valid_statuses:
            raise ValidationError(f"Invalid status: {node_data['status']}")
        
        return True
    
    @classmethod
    def to_cypher(cls, node_data: dict) -> str:
        cls.validate(node_data)
        props = ", ".join(f"{k}: ${k}" for k in node_data.keys())
        return f"CREATE (p:Project {{{props}}})"
```

This gives you:

- **Flexible storage**: The graph accepts any properties
- **Enforced contracts**: Your application validates before writing
- **Easy evolution**: Change validation rules without database migrations
- **Type safety where needed**: Python/TypeScript catch issues at development time
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*V0GC9RAhaQChP9afhkBTdg.png)

Note how relationships carry their own properties (allocation percentage, escalation reason, severity). This is natural in property graphs but awkward in RDF, which requires reification — creating a node to represent the relationship itself.

## Code Example: Hybrid Retrieval with Property Graphs

Here’s a complete retrieval function combining vector search and graph traversal using FalkorDB:

```c
from falkordb import FalkorDB
from typing import Optional
import numpy as np

class KnowledgeGraphRetriever:
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.db = FalkorDB(host=host, port=port)
        self.graph = self.db.select_graph("ai_memory")
    
    def setup_vector_index(self, dim: int = 1536):
        """Create vector index for entity embeddings (run once)."""
        self.graph.query("""
            CREATE VECTOR INDEX entity_embeddings 
            FOR (n:Entity) 
            ON (n.embedding) 
            OPTIONS {
                dimension: $dim,
                similarityFunction: 'cosine'
            }
        """, params={"dim": dim})
    
    def retrieve(
        self, 
        query_embedding: list[float],
        query_text: str,
        top_k: int = 5,
        traversal_depth: int = 2
    ) -> dict:
        """
        Hybrid retrieval: vector search + graph expansion.
        
        Returns nodes, relationships, and a flattened context string
        suitable for LLM consumption.
        """
        
        # Stage 1: Vector search for seed nodes
        # FalkorDB's vector search with KNN
        seed_result = self.graph.query("""
            CALL db.idx.vector.queryNodes(
                'Entity',
                'embedding',
                $top_k,
                vecf32($embedding)
            ) YIELD node, score
            RETURN node, score
            ORDER BY score DESC
        """, params={"embedding": query_embedding, "top_k": top_k})
        
        seed_nodes = []
        for record in seed_result.result_set:
            node = record[0]
            seed_nodes.append(node)
        
        if not seed_nodes:
            return {"nodes": [], "relationships": [], "context_string": ""}
        
        # Get seed node IDs for traversal
        seed_names = [n.properties.get("name") for n in seed_nodes]
        
        # Stage 2: Graph traversal from seed nodes (variable-length paths)
        # FalkorDB supports efficient variable-length path queries
        expanded_result = self.graph.query("""
            MATCH (seed:Entity)
            WHERE seed.name IN $seed_names
            
            // Traverse 1 to N hops, collecting connected subgraph
            OPTIONAL MATCH path = (seed)-[*1..$depth]-(connected)
            
            WITH seed, connected, relationships(path) as rels
            WHERE connected IS NOT NULL
            
            RETURN DISTINCT 
                seed,
                connected,
                rels
            LIMIT 100
        """, params={"seed_names": seed_names, "depth": traversal_depth})
        
        # Stage 3: Deduplicate and structure results
        all_nodes = {}
        all_relationships = []
        seen_rels = set()
        
        # Add seed nodes first
        for node in seed_nodes:
            node_id = node.properties.get("name", str(id(node)))
            if node_id not in all_nodes:
                all_nodes[node_id] = {
                    "id": node_id,
                    "labels": node.labels,
                    "properties": node.properties
                }
        
        # Process traversal results
        for record in expanded_result.result_set:
            seed_node, connected_node, rels = record
            
            # Add connected node
            if connected_node:
                node_id = connected_node.properties.get("name", str(id(connected_node)))
                if node_id not in all_nodes:
                    all_nodes[node_id] = {
                        "id": node_id,
                        "labels": connected_node.labels,
                        "properties": connected_node.properties
                    }
            
            # Add relationships
            if rels:
                for rel in rels:
                    rel_key = (rel.src_node, rel.relation, rel.dest_node)
                    if rel_key not in seen_rels:
                        seen_rels.add(rel_key)
                        all_relationships.append({
                            "type": rel.relation,
                            "start": rel.src_node,
                            "end": rel.dest_node,
                            "properties": rel.properties if hasattr(rel, 'properties') else {}
                        })
        
        # Stage 4: Format for LLM context
        context = self._format_context(all_nodes, all_relationships)
        
        return {
            "nodes": list(all_nodes.values()),
            "relationships": all_relationships,
            "context_string": context
        }
    
    def _format_context(self, nodes: dict, relationships: list) -> str:
        """Convert graph structure to natural language for LLM."""
        lines = ["## Relevant Entities\n"]
        
        for node in nodes.values():
            label = node["labels"][0] if node["labels"] else "Entity"
            name = node["properties"].get("name", "Unknown")
            props = ", ".join(
                f"{k}: {v}" for k, v in node["properties"].items() 
                if k not in ["name", "embedding"]
            )
            lines.append(f"- **{label}**: {name} ({props})")
        
        lines.append("\n## Relationships\n")
        
        for rel in relationships:
            start_name = rel["start"]
            end_name = rel["end"]
            rel_props = ", ".join(
                f"{k}={v}" for k, v in rel["properties"].items()
            )
            lines.append(
                f"- {start_name} --[{rel['type']}]--> {end_name}"
                + (f" ({rel_props})" if rel_props else "")
            )
        
        return "\n".join(lines)
```
```c
# Usage
retriever = KnowledgeGraphRetriever(
    host="localhost",
    port=6379  # FalkorDB runs on Redis protocol
)
query = "What projects is Sarah managing that are at risk?"
query_embedding = embed_model.encode(query)  # Your embedding model
results = retriever.retrieve(
    query_embedding=query_embedding.tolist(),
    query_text=query,
    top_k=5,
    traversal_depth=2
)
# Pass to LLM
response = llm.generate(
    system="Answer based on the following knowledge graph context.",
    context=results["context_string"],
    question=query
)
```

==**Why FalkorDB?**== ==FalkorDB uses GraphBLAS (sparse matrix algebra) under the hood, achieving sub-10ms query latency even for complex traversals. It runs on the Redis protocol, making deployment familiar for teams already using Redis infrastructure. Native vector indexing means you don’t need a separate vector database — the hybrid retrieval pattern above runs entirely within FalkorDB.==

## Migration Path: Starting Flexible, Adding Constraints Later

If you’re worried about starting too loose, here’s the migration path I recommend:

**Phase 1: Permissive Ingestion**

- Ingest everything your extractors produce
- Track which properties actually appear in practice
- Monitor query patterns to understand access needs

**Phase 2: Emergent Schema Discovery**

- Analyze property frequency and co-occurrence
- Identify natural entity types from clustering
- Document the implicit schema that emerged

**Phase 3: Soft Constraints**

- Add application-layer validation for high-value entity types
- Create indexes on frequently-queried properties
- Implement property coercion for consistency

**Phase 4: Hardened Core (Ongoing)**

- Lock down schema for stable, high-traffic node types
- Keep edge types flexible for evolving relationship discovery
- Export formal ontology *if* interoperability needs arise

This path gives you speed when you need it (early experimentation) and rigor when you’ve earned it (proven patterns).

## Conclusion

Property graphs aren’t a compromise — they’re the right tool for AI memory systems where extraction capabilities evolve, business requirements shift, and time-to-value matters. RDF/OWL has its place in regulated industries with stable ontologies and cross-organization data sharing, but that’s a small fraction of enterprise AI projects.

==The practical advice:== ==**start with property graphs, enforce schema in your application layer, and export to formal ontologies only when interoperability demands it**====. Your future self — the one debugging why the ontology migration broke production at 2 AM== — will thank you.

[![Graph Praxis](https://miro.medium.com/v2/resize:fill:72:72/1*rUElHORNRlPmVu9QZUkR-A.png)](https://medium.com/graph-praxis?source=post_page---post_publication_info--defe5df2ae95---------------------------------------)

[![Graph Praxis](https://miro.medium.com/v2/resize:fill:96:96/1*rUElHORNRlPmVu9QZUkR-A.png)](https://medium.com/graph-praxis?source=post_page---post_publication_info--defe5df2ae95---------------------------------------)

[Last published Mar 24, 2026](https://medium.com/graph-praxis/multi-lora-for-knowledge-graphs-one-model-many-domains-b6c1f4c96953?source=post_page---post_publication_info--defe5df2ae95---------------------------------------)

Where knowledge graph theory meets production reality. Enterprise architectures for Graph RAG, dynamic ontologies, and AI agents that actually remember.

[![Alexander Shereshevsky](https://miro.medium.com/v2/resize:fill:72:72/1*Yam5uYmyyy1ZE3QqSBDekA.jpeg)](https://medium.com/@shereshevsky?source=post_page---post_author_info--defe5df2ae95---------------------------------------)

[![Alexander Shereshevsky](https://miro.medium.com/v2/resize:fill:96:96/1*Yam5uYmyyy1ZE3QqSBDekA.jpeg)](https://medium.com/@shereshevsky?source=post_page---post_author_info--defe5df2ae95---------------------------------------)

[35 following](https://medium.com/@shereshevsky/following?source=post_page---post_author_info--defe5df2ae95---------------------------------------)

## Responses (5)

S Parodi

What are your thoughts?  [Modeller](https://medium.com/@brett_12578?source=post_page---post_responses--defe5df2ae95----0-----------------------------------)

[

Mar 18

](https://medium.com/@brett_12578/property-graphs-are-shite-imho-no-data-normalisation-so-one-can-have-copied-and-conflicting-data-68fa51ef4452?source=post_page---post_responses--defe5df2ae95----0-----------------------------------)

```c
property graphs are shite, imho, no data normalisation, so one can have copied and conflicting data on nodes, its like having a json database with edges, sure its fast, but its crap and a long term maintenance nightmare.rdf/owl is old-fashioned…more
```

2

```c
Some of the reasoning is correct. Indeed using RDF is a must when interoperability is required.Still, a lot of it is biased or incompetent. "RDF/OWL graphs (Stardog, GraphDB, Virtuoso) enforce a formal ontology — a declared vocabulary of classes…more
```

3

```c
"With rigid ontologies, each extraction improvement triggers ontology renegotiation" - What are you talking about? you will get the same benfit with an ontology. query with SPARQL
```

2