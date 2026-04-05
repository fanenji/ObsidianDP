---
title: "A Benchmark to Understand the Role of Knowledge Graphs on LLM Accuracy for Question Answering on Enterprise SQL Databases"
type: note
topic: data-platform
created: 2026-04-04
tags:
  - knowledge-graph
  - llm
  - sql
  - sparql
  - benchmark
  - ai
source: "arXiv:2311.07509v1 [cs.AI] — November 14, 2023"
authors:
  - Juan F. Sequeda (data.world)
  - Dean Allemang (data.world)
  - Bryon Jacob (data.world)
---

# A Benchmark to Understand the Role of Knowledge Graphs on Large Language Model's Accuracy for Question Answering on Enterprise SQL Databases

*Technical Report — November 14, 2023*

**Authors:** Juan F. Sequeda · Dean Allemang · Bryon Jacob — data.world

---

## Abstract

Enterprise applications of Large Language Models (LLMs) hold promise for question answering on enterprise SQL databases. However, the extent to which LLMs can accurately respond to enterprise questions in such databases remains unclear, given the absence of suitable Text-to-SQL benchmarks tailored to enterprise settings. Additionally, the potential of Knowledge Graphs (KGs) to enhance LLM-based question answering by providing business context is not well understood.

This study aims to evaluate the accuracy of LLM-powered question answering systems in the context of enterprise questions and SQL databases, while also exploring the role of knowledge graphs in improving accuracy. To achieve this, we introduce a benchmark comprising an enterprise SQL schema in the insurance domain, a range of enterprise queries encompassing reporting to metrics, and a contextual layer incorporating an ontology and mappings that define a knowledge graph.

**Primary finding:** question answering using GPT-4, with zero-shot prompts directly on SQL databases, achieves an accuracy of **16%**. Notably, this accuracy increases to **54%** when questions are posed over a Knowledge Graph representation of the enterprise SQL database. Therefore, investing in Knowledge Graph provides higher accuracy for LLM powered question answering systems.

**Keywords:** Knowledge Graphs · Large Language Models · Question Answering · SQL Databases · Benchmark · Retrieval Augmented Generation (RAG)

---

## 1 Introduction

Question answering — the ability to interact with data using natural language questions and obtaining accurate results — has been a long-standing challenge in computer science dating back to the 1960s. The field has advanced through Text-to-SQL approaches as a means of facilitating chatting with data stored in SQL databases. With the rise of Generative AI and Large Language Models (LLMs), question answering systems hold tremendous potential for transforming the way data-driven decision making is executed within enterprises.

While question answering systems have shown remarkable performance in several Text-to-SQL benchmarks (Spider, WikiSQL, KaggleDBQA), their implications for enterprise SQL databases remain obscure. Existing Question Answering and Text-to-SQL benchmarks, although valuable, are often misaligned with real-world enterprise settings:

1. These benchmarks typically overlook complex database schemas representing enterprise domains, which likely comprise hundreds of tables.
2. They also often disregard questions that are crucial for operational and strategic planning in an enterprise, including questions related to business reporting, metrics, and key performance indicators (KPIs).
3. A critical missing link is the absence of a business context layer — metadata, mappings, transformations, ontologies — that provides business semantics and knowledge about the enterprise.

Without these vital components, LLMs for enterprise question answering risk being disconnected from the reality of enterprise data, leading to hallucinations and uncontrolled outcomes. Their inability to provide explainable results can significantly impede their trustworthiness and adoption.

Knowledge Graphs (KGs) have been identified as a promising solution to fill the business context gaps in order to reduce hallucinations, thus enhancing the accuracy of LLMs. From an industry perspective, Gartner states: *"Knowledge graphs provide the perfect complement to LLM-based solutions where high thresholds of accuracy and correctness need to be attained."*

### Contributions

**1) A benchmark consisting of:**

- **Enterprise SQL Schema:** The OMG Property and Casualty Data Model, an enterprise relational database schema in the insurance domain.
- **Enterprise Question-Answer:** 43 natural language questions spanning two spectrums:
  1. Low to high question complexity (business reporting to KPI metrics)
  2. Low to high schema complexity (fewer to more tables required)
  
  These two spectrums form a quadrant: Low Question/Low Schema, High Question/Low Schema, Low Question/High Schema, and High Question/High Schema.
- **Context Layer:** An ontology describing Business Concepts, Attributes, and Relationships of the insurance domain, plus mappings from the SQL schema to the ontology. These can be used to create a Knowledge Graph representation of the SQL database.

**2) Benchmark results (GPT-4, zero-shot prompting):**

| Quadrant | w/o KG (SQL) | w/ KG (SPARQL) | Improvement |
|---|---|---|---|
| All Questions | 16.7% | 54.2% | 37.5% |
| Low Question/Low Schema | 25.5% | 71.1% | 45.6% |
| High Question/Low Schema | 37.4% | 66.9% | 29.5% |
| Low Question/High Schema | 0% | 35.7% | 35.7% |
| High Question/High Schema | 0% | 38.5% | 38.5% |

---

## 2 Research Question and Hypothesis

**RQ1:** To what extent can Large Language Models (LLMs) accurately answer enterprise natural language questions over enterprise SQL databases?

**RQ2:** To what extent can Knowledge Graphs improve the accuracy of LLMs to answer enterprise natural language questions over enterprise SQL databases?

**Hypothesis:** An LLM powered question answering system that answers a natural language question over a knowledge graph representation of the SQL database returns more accurate results than an LLM powered question answering system that answers a natural language question over the SQL database without a knowledge graph.

---

## 3 Benchmark Framework

### 3.1 Enterprise SQL Schema

The enterprise SQL schema used in the benchmark comes from the **P&C Data Model for Property And Casualty Insurance**, a standard model created by Object Management Group (OMG). This OMG specification addresses the data management needs of the Property and Casualty insurance community.

Main entities: Account, Activity, Agreement, Claim, Communication, Coverage, Event, Geographic Location, Insurable Object, Location Address, Money, Party, Policy, Policy Coverage Detail, Policy Deductible, Policy Limit, Product.

The physical data model consists of **199 tables** with a primary key each and **243 foreign keys**. SQL DDL: https://www.omg.org/cgi-bin/doc?dtc/13-04-15.ddl

For the current benchmark version, a subset of 13 tables is used: Claim, Claim_Amount, Loss_Payment, Loss_Reserve, Expense_Payment, Expense_Reserve, Claim_Coverage, Policy_Coverage_Detail, Policy, Policy_Amount, Agreement_Party_Role, Premium, Catastrophe.

*Figure 1: P&C Conceptual Model*

```
P&C Conceptual Data Model (Version 4g - 201108)

Legend:
  Focal Entity | Code Reference
  Major Entity | Event, Activity
  Business Data | Money

Key entities and relationships:
  Party ──────────────────────── interests identified
  Account ── groups customer or related
  Agreement ── legal entities covered
  Product ── provides → Policy
  Policy ── provisions specified in → Policy Coverage Detail
  Policy Coverage Detail ── defined for policy in → Coverage
  Coverage ── provided for → Policy Limit / Policy Deductible
  Insurable Object ── site of / attachment initially identified → Claim
  Claim ── defines potential settlement provisions
  Geographic Location ── is specific physical location for → Location Address
  Claim ── occurs at / centered at → Geographic Location
  Money ── amounts defined in (Reinsurance Coverage)
  Reinsurance Agreement ── provisions specified in → Reinsurance Coverage
```

### 3.2 Enterprise Questions

Questions are classified on two spectrums:

- **Low question complexity:** Business reporting use cases → SELECT-FROM SQL queries
- **High question complexity:** Metrics and KPIs → SQL queries with aggregations and mathematical functions

- **Low schema complexity:** 0–4 tables, denormalized schema
- **High schema complexity:** > 4 tables, normalized schema, many-to-many joins

*Figure 2: Four quadrants to classify questions*

| | **Low Schema Complexity** | **High Schema Complexity** |
|---|---|---|
| **High Question Complexity** | e.g. "What is the average time to settle a claim by policy number?" (Aggregation, Math, 4 tables) | e.g. "What is the total loss of each policy where loss is the sum of loss payment, Loss Reserve, Expense Payment, Expense Reserve Amount" (Aggregation, Math, 9 tables) |
| **Low Question Complexity** | e.g. "Return all the claims we have by claim number, open date and close date?" (Projection 3 columns, 1 table) | e.g. "What are the loss payment, Loss Reserve, Expense Payment, Expense Reserve Amount by Claim Number" (Projection 3 columns, 6 tables) |

The current benchmark version consists of **43 questions** (full list in Appendix 9.2).

### 3.3 Context Layer

The context layer consists of two parts:

- **Ontology:** Business Concepts, Attributes, and Relationships describing the insurance domain.
- **Mapping:** Transformation rules from the source SQL schema to the corresponding Business Concepts, Attributes, and Relationships in the target ontology.

The context layer is provided in machine-readable RDF: ontology in OWL and mapping in R2RML. These can be used to create the Knowledge Graph either in a virtualized or materialized way.

*Figure 3: Ontology describing relevant parts of the Property and Casualty data model*

```
Ontology graph (key nodes and relationships):

  Agent ────────────────────────── Catastrophe
    │                                   │
  sold by agent                    has catastrophe
    │                         ┌─────────┴──────────┐
  Policy ── has policy ──► Policy         Expense Payment
    │        Coverage          │           Loss Payment
  has policy   Detail ──►  Claim ◄──── Expense Reserve
    holder          │         │              Loss Reserve
    │          appears        │
  Policy      (premium)    Premium
  Holder
```

### 3.4 Scoring

The benchmark reports three scores:

**Execution Accuracy (EA):** Following the Spider benchmark metric. An execution is accurate if the result of the query matches the answer for the query. The order and labels of columns are not taken into account.

*Example:*

Question: *"Return all the claims we have by claim number, open date and close date?"*

| Claim Number | Open Date | Close Date |
|---|---|---|
| 12312701 | 2019-01-15 | 2019-01-31 |
| 12312702 | 2019-06-02 | 2019-06-27 |

The following answer is also accurate (different column order/labels):

| claim_number | claim_close_date | claim_open_date |
|---|---|---|
| 12312702 | 2019-06-27 | 2019-06-02 |
| 12312701 | 2019-01-31 | 2019-01-15 |

The following answer is **inaccurate** (missing claim number):

| claim_id | claim_close_date | claim_open_date |
|---|---|---|
| 1 | 2019-01-31 | 2019-01-15 |
| 2 | 2019-06-27 | 2019-06-02 |

**Overall Execution Accuracy (OEA):** Given the non-deterministic nature of LLMs, OEA = (# of EA) / Total Number of runs. Examples:
- 100% OEA: every single run returned an accurate answer
- 50% OEA: half of the runs returned an accurate answer
- 0% OEA: every run returned an inaccurate answer

**Average Overall Execution Accuracy (AOEA):** The average of OEA scores for a given set of questions (all questions in the benchmark, or questions per quadrant).

---

## 4 Experimental Setup

Benchmark and processing code available on GitHub: https://github.com/datadotworld/cwd-benchmark-data

### 4.1 Benchmark Setup

The data begins with the P&C Data Model (OMG excerpt). Data expressed as CSV tables corresponding to the DDL. Reference queries provided in both SQL and SPARQL.

Published benchmark components:
- The DDL for the relational database (text file)
- Sample data for the tables (CSV)
- An OWL file (RDF Turtle) describing the ontology of the knowledge graph
- An R2RML file (RDF Turtle) describing the mappings from relational schema to OWL ontology
- The questions (natural language) and reference queries (SQL and SPARQL)

### 4.2 Question Answering System Setup

**Parameters (OpenAI API):**
- `max_tokens = 2048`
- `n = 1`
- `temperature = 0.3`
- Timeout: 60 seconds

#### 4.2.1 Question Answering System for SQL

**SQL Zero-shot Prompt:**
```
Given the database described by the following DDL:
INSERT SQL DDL
Write a SQL query that answers the following question. Do not explain the query,
return just the query, so it can be run verbatim from your response.
Here's the question:
"INSERT QUESTION"
```

*Figure 4: Question Answering System for SQL*

```
┌──────────┐  ┌─────────┐  ┌────────┐
│ Question │  │ SQL DDL │  │ Answer │
└────┬─────┘  └────┬────┘  └───┬────┘
     └──────┬───────┘           │
            ▼                   │
   ┌──────────────────┐         │
   │ SQL Zero-shot    │         │
   │ Prompt           │         │
   └────────┬─────────┘         │
            ▼                   │
         ┌──────┐               │
         │ GPT-4│               │
         └──┬───┘               │
            ▼                   │
         ┌──────┐               │
         │ SQL  │               │
         └──┬───┘               │
            ▼                   │
   ┌────────────────┐           │
   │  SQL Database  │ ──────────┘
   └────────────────┘
```

#### 4.2.2 Question Answering System for Knowledge Graph

**SPARQL Zero-shot Prompt:**
```
Given the OWL model described in the following TTL file:
INSERT OWL ontology
Write a SPARQL query that answers the question. The data for your query is
available in a SERVICE identified by <mapped>. Do not explain the query,
return just the query, so it can be run verbatim from your response.
Here's the question:
"INSERT QUESTION"
```

*Figure 5: Question Answering System for Knowledge Graph*

```
┌──────────┐  ┌──────────────┐  ┌────────┐
│ Question │  │ OWL Ontology │  │ Answer │
└────┬─────┘  └──────┬───────┘  └───┬────┘
     └────────┬───────┘              │
              ▼                      │
   ┌─────────────────────┐           │
   │ SPARQL Zero-shot    │           │
   │ Prompt              │           │
   └──────────┬──────────┘           │
              ▼                      │
           ┌──────┐                  │
           │ GPT-4│                  │
           └──┬───┘                  │
              ▼                      │
           ┌────────┐                │
           │ SPARQL │                │
           └───┬────┘                │
               ▼                     │
   ┌───────────────────────┐         │
   │ Virtualized Knowledge │         │
   │ Graph                 │         │
   │  ◉──◉──◉             │         │
   └──────────┬────────────┘         │
    Mapping ──┘                      │
              ▼                      │
           ┌──────┐                  │
           │ SQL  │                  │
           └──┬───┘                  │
              ▼                      │
   ┌────────────────┐                │
   │  SQL Database  │ ───────────────┘
   └────────────────┘
```

### 4.3 Processing Setup

Each experimental session with 43 questions involves 86 calls to the LLM and 172 query executions (one Run in SQL and one in SPARQL). Data collected between **September 20, 2023 and October 13, 2023**. All failure modes are treated as unsuccessful execution (binary: succeeds or fails).

---

## 5 Results

Results are presented in four parts: 1) overall, 2) question quadrant, 3) partial accuracy, and 4) inaccurate results.

- **SPARQL** = questions over Knowledge Graph representation of the SQL database
- **SQL** = questions directly on SQL databases without a Knowledge Graph

### 5.1 Overall

*Table 1: Average Overall Execution Accuracy (AOEA) of Overall and Quadrant Results*

| | w/o KG (SQL) | w/ KG (SPARQL) | Improvement |
|---|---|---|---|
| **All Questions** | 16.7% | 54.2% | 37.5% |
| **Low Question/Low Schema** | 25.5% | 71.1% | 45.6% |
| **High Question/Low Schema** | 37.4% | 66.9% | 29.5% |
| **Low Question/High Schema** | 0% | 35.7% | 35.7% |
| **High Question/High Schema** | 0% | 38.5% | 38.5% |

*Figure 6: AOEA of SPARQL (54.2%) vs SQL (16.7%) — SPARQL accuracy is 3x SQL accuracy*

**Discussion:** Natural Language questions translated to SPARQL over a Knowledge Graph representation of the SQL database achieved 3x the accuracy of natural language questions translated to SQL and executed directly on the SQL database. This supports the hypothesis: *An LLM powered question answering system that answers a Natural Language question over a Knowledge Graph representation of the SQL database returns more accurate results than a LLM powered question answering system that answers a Natural Language question over the SQL database without a knowledge graph.*

### 5.2 Quadrant

*Figure 8: AOEA of SPARQL and SQL per quadrant*

- **Low Question/Low Schema:** SQL = 25.5%, SPARQL = 71.1% (2.8X the SQL accuracy)
- **High Question/Low Schema:** SQL = 37.4%, SPARQL = 66.9% (1.8X the SQL accuracy)
- **Low Question/High Schema:** SQL was not able to answer any question accurately. SPARQL = 35.7%
- **High Question/High Schema:** SQL was not able to answer any question accurately. SPARQL = 38.7%

> When a question requires more than 5 tables to provide an answer, SQL accuracy drops to zero.

### 5.3 Partial Accuracy

During manual analysis of generated SQL and SPARQL queries, two patterns of partially accurate answers were observed:

- **Overlap:** The columns returned are correct but are a subset of the accurate answer. In some cases, they include other columns not part of the expected answer (semantic overlap).
- **Return Identifier:** An internal identifier was returned instead of the appropriate label.

*Example — Question: "Return all the claims we have by claim number, open date and close date?"*

**SQL:**
```sql
SELECT Claim_Identifier, Claim_Open_Date, Claim_Close_Date
FROM Claim
```

**SPARQL:**
```sparql
SELECT ?claim ?claimOpenDate ?claimCloseDate
WHERE {
    ?claim a in:Claim ;
           in:claimNumber ?claimNumber ;
           in:claimOpenDate ?claimOpenDate ;
           in:claimCloseDate ?claimCloseDate .
}
```

In the SQL query, `Claim_Identifier` is returned as the claim number when the actual claim number is `company_claim_number`. In the SPARQL query, `?claim` (the IRI uniquely identifying each claim) is returned, not the claim number.

### 5.4 Inaccuracy

#### 5.4.1 SQL Inaccuracy

Three types of inaccuracies observed:

- **Column Name Hallucinations:** Column names that do not exist in the corresponding table.
- **Value Hallucinations:** Generated values applied as filters where that value does not exist in the database.
- **Join Hallucinations:** Generated joins that are not accurate.

#### 5.4.2 SPARQL Inaccuracy

- **Incorrect Path:** The generated query does not follow the correct path of properties in the ontology (e.g. goes from A to C when the correct path is A to B to C).
- **Incorrect Direction:** The generated query swaps the direction of a property (B to A, when correct is A to B).

**Discussion:** SQL inaccuracies are based on **hallucination** while SPARQL inaccuracies are based on **path inconsistency**. Notably, no hallucinated classes or properties were observed in SPARQL queries — likely because the prompt specified *"return just the query, so it can be run verbatim from your response"*, which may have discouraged hallucination.

---

## 6 Takeaways

The results support the hypothesis: *An LLM powered question answering system that answers a Natural Language question over a Knowledge Graph representation of the SQL database returns more accurate results than a LLM powered question answering system that answers a Natural Language question over the SQL database without a knowledge graph.*

**RQ1 Answer:** Using GPT-4 and zero-shot prompting, Enterprise Natural Language questions over Enterprise SQL databases achieved **16.7% AOEA**. For Low Question/Low Schema: 25.5%. For High Question/Low Schema: 37.4%. For both Low and High Question/High Schema: 0%.

**RQ2 Answer:** Using GPT-4 and zero-shot prompting, Enterprise Natural Language questions over a Knowledge Graph representation achieved **54.2% AOEA** (3x the SQL accuracy, +37.5% improvement). Per quadrant:
- Low Question/Low Schema: 71.1% (+45.6%)
- High Question/Low Schema: 66.9% (+29.5%)
- Low Question/High Schema: 35.7% (+35.7%)
- High Question/High Schema: 38.7% (+38.7%)

> **Context is crucial for accuracy.** Investing in context of SQL databases — in the form of an ontology that describes the semantics of the business domain and mappings connecting the physical schema to the ontology — is required to increase the accuracy of LLMs. This context needs to be treated as a first class citizen, managed in a metadata management system (i.e. data catalog) and ideally in a knowledge graph architecture.

---

## 7 Research Agenda

Generative AI and LLMs are following the traditional hype cycle, rapidly reaching the peak of inflated expectations. The combination of Knowledge Graphs with Large Language Models will be a way to address enterprise concerns in order to hit the Slope of Enlightenment and the Plateau of Productivity.

### 7.1 Benchmark Enhancements

**Enterprise SQL Schema:**
- Current version uses 13 tables (subset of 199). Increasing schema usage will shed light on how much harder this problem is.
- Database instantiation is manual (few rows per table). Different instantiations would identify false positive scenarios.
- Schema is in third-normal form. How would results change with star schema, snowflake schema, data vault, OBT, EAV?
- What happens if primary/foreign key constraints are absent or augmented?

**Enterprise Questions:**
- Current questions lack filtering (time periods, value ranges, etc.)
- Various rewordings of the same question should be tested
- Ambiguous questions, unanswerable questions, multi-turn conversations, multi-language

**Context Layer:**
- Current mappings are 1-1 table/column mappings. Extensions include: Conditions, Data as Concept, Join Concept, Distinct, Concat, Math, Case, Null, Join Attribute patterns
- Context can be provided in other graph formalisms: OpenCypher, Gremlin
- Context could come from previous queries or Slack/Teams conversations

**Scoring:**
- Measure semantic overlap for partial accuracy
- Measure time taken to produce an answer
- Follow HELM holistic evaluation approach

### 7.2 Research Topics

**Business Implications:** What does *accurate enough* mean in enterprise settings? How do LLM-powered systems compare to manual approaches (reviewing a dashboard)?

**Qualitative Evaluation and User Studies:** User satisfaction studies, impact of partial accuracy, different user personas (data analyst vs. executive).

**Knowledge Engineering Methodologies:** How can existing ontology and knowledge engineering methodologies adapt to an era of large amounts of data and LLMs?

**Diverse Domains:** The framework can be applied to any domain beyond insurance. Industry-specific LLMs (e.g. BloombergGPT for finance) could be tested.

**Explainability:** Hypothesis: *An LLM and Knowledge Graph powered question answering system provides explainability with higher user satisfaction compared to an LLM powered question answering system that doesn't use knowledge graphs.*

**Cost:** What are the monetary cost implications of achieving accurate answers? Can approaches be found that optimize cost?

**Pre and Post Processing:** What pre and post processing steps could be implemented to improve accuracy? Could it be determined if the data exist to answer a question? Could it be detected if a query will generate inaccurate results?

---

## 8 Summary and Conclusion

This paper investigates two research questions: 1) to what extent LLMs can accurately answer enterprise natural language questions over enterprise SQL databases, and 2) to what extent Knowledge Graphs can improve the accuracy of LLMs to answer enterprise natural language questions over enterprise SQL databases.

**Key results:**
- Enterprise Natural Language questions over Enterprise SQL databases: **16.7% AOEA**
- Enterprise Natural Language questions over a Knowledge Graph representation: **54.2% AOEA**
- For low schema complexity, KG accuracy was between **66.9% and 71.1%**
- For high schema complexity, accuracy without KG was **0%**, with KG was **35–38%**

**Conclusion:** These experimental results support the main conclusion: **investing in Knowledge Graph provides higher accuracy for LLM powered question answering systems.** Enterprises that want to achieve higher accuracy in LLM powered question answering systems must treat the business context and semantics as a first class citizen and invest in a data catalog platform with a knowledge graph architecture.

---

## References

1. Popescu, O.E., and Kautz, H. Towards a theory of natural language interfaces to databases. *IUI 2003*, pp. 149–157.
2. Finegan-Dollak, C. et al. Improving text-to-sql evaluation methodology. *ACL 2018*, pp. 351–360.
3. Deborah A. Dahl et al. Expanding the scope of the ATIS task. *Human Language Technology* (1994), 43–48.
4. Finegan-Dollak, C. et al. Improving text-to-SQL evaluation methodology. *ACL 2018*, pp. 351–360.
5. Galkin, M. et al. Towards foundation models for knowledge graph reasoning. 2023.
6. Giordani, A., and Moschitti, A. Automatic generation and reranking of sql-derived answers. *SEBD 2012*, pp. 59–76.
7. Godfrey, P., and Gryz, J. Answering queries by semantic caches. *DEXA'99*, pp. 485–498.
8. Green, B.F. et al. Baseball: An automatic question-answerer. *IRE-AIEE-ACM '61*.
9. Green, C.C., and Raphael, B. The use of theorem-proving techniques in question-answering systems. *ACM 1968*, pp. 169–181.
10. Hendrix, G.G. et al. Developing a natural language interface to complex data. *ACM Trans. Database Syst. 3*, 2 (1978), 105–147.
11. Lee, C.-H. et al. KaggleDBQA: Realistic evaluation of text-to-SQL parsers. *ACL-IJCNLP 2021*, pp. 2261–2273.
12. Li, F., and Jagadish, H.V. Constructing an interactive natural language interface for relational databases. *VLDB 8*, 1 (2014), 73–84.
13. Navid Yaghmazadeh et al. Sqlizer: Query synthesis from natural language. *OOPSLA 2017*, 63:1–63:26.
14. Pan, S. et al. Unifying large language models and knowledge graphs: A roadmap. *arXiv:306.08302* (2023).
15. Sequeda, J., and Lassila, O. *Designing and Building Enterprise Knowledge Graphs*. Morgan & Claypool, 2021.
16. Srinivasan Iyer et al. Learning a neural semantic parser from user feedback. *ACL 2017*, pp. 963–973.
17. Tang, L.R., and Mooney, R.J. Automated construction of database interfaces. *SIGDAT 2000*, pp. 133–141.
18. Tao Yu et al. Spider: A large-scale human-labeled dataset for text-to-SQL. *EMNLP 2018*, pp. 3911–3921.
19. Victor Zhong, C.X., and Socher, R. Seq2sql: Generating structured queries from natural language. *CoRR abs/1709.00103* (2017).
20. Woods, W.A. Transition network grammars for natural language analysis. *Commun. ACM 13*, 10 (1970), 591–606.
21. Wu, S. et al. Bloomberggpt: A large language model for finance. 2023.
22. Zelle, J.M., and Mooney, R.J. Learning to parse database queries using inductive logic programming. *AAAI 1996*, pp. 1050–1055.
