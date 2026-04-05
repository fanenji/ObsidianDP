---
title: "Geospatial Tables in the Open Lakehouse: A New Era for Iceberg & Parquet — Summary"
type: note
topic: data-platform
created: 2026-04-04
tags:
  - mapping
  - iceberg
  - geoparquet
  - parquet
  - lakehouse
  - spatial
source: "[[Geospatial Tables in the Open Lakehouse A New Era for Iceberg & Parquet]]"
speakers:
  - Jia Yu (Wherobots, Co-Founder & CTO)
  - Chris Holmes (Planet, Creator of GeoParquet)
  - Szehon Ho (Databricks, Iceberg PMC)
  - Vikram Gundeti (Foursquare, CTO)
event: Wherobots Livestream, May 8 2025
video: https://www.youtube.com/watch?v=m5SvI2MjCmk
---

# Geospatial Tables in the Open Lakehouse: A New Era for Iceberg & Parquet

**Speakers:**
- **Jia Yu** — Co-Founder & CTO, Wherobots (host)
- **Chris Holmes** — Creator of GeoParquet, Planet Fellow at Planet
- **Szehon Ho** — Iceberg PMC Member, Software Engineer at Databricks (previously Apple)
- **Vikram Gundeti** — CTO at Foursquare (previously Amazon, founding engineer on Alexa)

**Event:** Wherobots Livestream — May 8, 2025
**Video:** https://www.youtube.com/watch?v=m5SvI2MjCmk

---

## 1. The Problem: Geospatial Data in the Data Ecosystem

Before GeoParquet and native geospatial types in Iceberg, the state of geospatial data in the broader data ecosystem was fragmented:

- **No interoperability**: every system stored spatial data differently — same choices most of the time, but not identical
- **Silo formats**: GeoJSON (verbose, no index, not cloud-native), Shapefile (10-char column limit, 2 GB max), GeoPackage (SQLite-based, too complex for mainstream tools)
- **Cloud warehouse lock-in**: BigQuery, Snowflake, Redshift all supported geospatial, but you couldn't easily move data between them — each used different conventions for spherical edges, CRS representation, etc.
- **No standard for cloud storage**: data on S3 in Parquet with spatial columns had no metadata convention — each team made their own choices

Foursquare example: billions of GPS pings, impressions, and place events per day — stored in custom folder structures on S3, with manually written GDPR deletion tools, fixed partitioning schemes impossible to evolve without rebuilding pipelines.

---

## 2. GeoParquet: Origins and Purpose

**GeoParquet** was created to standardise how geospatial data is stored in Parquet files.

### 2.1 Origins (Chris Holmes)

Two parallel efforts that merged:
1. **OGC initiative** — Javier Deator from Carto pushed for OGC engagement with cloud data warehouses. Pain point: no standard format to pass data between BigQuery, Snowflake, Redshift
2. **GeoArrow community** — had already implemented GeoParquet/GeoArrow in R (geopandas) and was looking for a standard

Key insight: BigQuery, Snowflake, and Redshift all support Parquet natively. If you standardise the geospatial metadata in Parquet, all three can interoperate without custom code — you don't need to convince mainstream data tools to support a "crazy new format".

### 2.2 How GeoParquet Works

Parquet has a metadata system that allows attaching key-value metadata at the file and column level. GeoParquet uses this mechanism to store:
- CRS (Coordinate Reference System) definition
- Geometry encoding (WKB — Well-Known Binary)
- Bounding box / covering information
- Edge interpolation behaviour (spherical vs. planar)

No changes to the Parquet file format itself — just standardised metadata conventions.

### 2.3 GeoParquet vs. Other Formats

| Format | Pros | Cons |
|---|---|---|
| **GeoJSON** | Web-friendly, human-readable | No index, verbose, not cloud-native |
| **Shapefile** | Widespread | 10-char column names, 2 GB limit, multi-file |
| **GeoPackage** | SQLite-based, solid | Too complex for mainstream data tools |
| **GeoParquet** | Compact (≈ zip shapefile size, no unzip needed), fast, columnar, nesting support, interoperable with all major data platforms | Requires spatial-aware reader for geometry columns |

Performance: GeoParquet is approximately the size of a zipped shapefile — but you don't unzip it. Reading is much faster than any row-wise format.

---

## 3. Geospatial Types in Apache Iceberg

### 3.1 What Iceberg Adds vs. Raw Parquet

Parquet is a file format. Iceberg is a **table format** — it manages a collection of Parquet files as a logical table with:

| Feature | Benefit |
|---|---|
| **Schema tracking per file** | Handle schema evolution across millions of files without breaking queries |
| **File metadata / statistics** | Skip files without opening them — no need to scan a million files to find matches |
| **No file listing on S3** | Cloud storage is slow at listing directories; Iceberg never does file listings |
| **ACID transactions** | Concurrent readers and writers, no partial failures, full rollback support |
| **Compaction, re-partitioning, sorting** | Optimise data layout over time without stopping the world |
| **Time travel** | Query a table as of any past snapshot |

The three buckets Szehon identifies: **functionality**, **performance**, **ACID transactions**.

### 3.2 The Geo Type Proposal

In **February 2025**, geospatial types were introduced into Apache Parquet and Iceberg. This was the result of ~1 year of community work across GeoParquet contributors, Iceberg PMC, and geospatial professionals.

The proposal adds two geo types with two configurable parameters:
- **CRS** — Coordinate Reference System (e.g. EPSG:4326, EPSG:3857)
- **Edge interpolation** — how line segments between two points are interpreted (spherical/geodesic vs. planar/Cartesian)

These types are versioned into **Iceberg V3**.

### 3.3 Debates During the Design Process

The hardest problems were not about geometry classes (points, polygons — already standardised by OGC) or serialisation (WKB — already standard). The core debate:

> The same WKB bytes can represent **different places on Earth** depending on the CRS and edge interpolation convention the writer used.

This is a problem no other data type in Iceberg has — integers and strings don't change meaning depending on the system that produced them. Getting enough metadata so that a reader can correctly interpret what a writer produced took significant effort.

Tension between:
- **Completeness** — geospatial has many obscure edge cases (anti-meridian, spherical vs. planar edges, different CRS authority codes)
- **Compactness** — Iceberg types are serialised; you can't put verbose JSON-based CRS definitions inline

Resolution: two parameters (CRS + edge interpolation) stored as compact identifiers — enough to correctly interpret any real-world dataset, without trying to specify every possible obscure case.

### 3.4 Native Bounding Box Statistics

A key performance benefit of the native geo type in Parquet:

**Before (GeoParquet as binary column):**
- Bounding box statistics stored at the **file level** only
- Predicate pushdown: either skip the entire file or read the entire file

**After (native geo type in Parquet):**
- Bounding box statistics stored at the **row group level** within each Parquet file
- Predicate pushdown: skip individual row groups — much finer-grained pruning
- Combined with Iceberg's file-level statistics: two levels of spatial pruning before any geometry is decoded

---

## 4. Iceberg vs. Delta Lake

From Szehon (Databricks employee, Iceberg PMC):

| Property | Iceberg | Delta Lake |
|---|---|---|
| **Writes** | Slightly slower — rewrites full metadata | Fast — only writes delta (incremental changes) |
| **Reads** | Fast — metadata fully materialised | Slower — must reconstruct state from deltas |
| **Open source governance** | Multi-vendor (Netflix, Apple, Databricks, Snowflake, etc.) | Primarily Databricks-driven in perception |
| **Geo types** | In V3 spec (2025) | Not yet; will likely adopt Parquet geo type when available |
| **Interoperability** | Iceberg REST Catalog, Polaris | Databricks-native tooling preferred |

Databricks' stated direction: make Delta and Iceberg more **interoperable** — get the best of both formats. The geo types were defined at the Parquet level (not Iceberg-specific) specifically so that Delta Lake and any other Parquet-based format can adopt the same definition.

Foursquare's experience: started with both, switched predominantly to Iceberg because Delta Lake's open-source/proprietary boundary was unclear — difficult to know which features required Databricks compute.

---

## 5. Compute/Storage Separation and Vendor Lock-in

The most significant architectural shift Iceberg enables:

**Before:** data was coupled to the compute engine. BigQuery stored data in its format; Snowflake in its format. Moving between them required full data export/re-import.

**After:** data lives on object storage (S3/GCS/ADLS) in Iceberg format. Any compatible engine (Spark, Flink, Trino, DuckDB, Snowflake, BigQuery) can read it natively without loading.

### Implications

| Stakeholder | Benefit |
|---|---|
| **Data consumers** | Use best engine for each job; switch engines without migrating data |
| **Data providers (e.g. governments)** | Put data on a bucket once; anyone reads it — no server to run, compute cost shifts to consumers |
| **Satellite / geospatial data companies** | One Iceberg table, readable by all customers in all clouds — no per-platform distribution pipelines |
| **Small organisations** | No need to lock into an expensive cloud data warehouse |

Foursquare's places open data set: previously had to replicate to S3, Snowflake, and Hugging Face separately. With Iceberg, one storage location — all platforms read it natively.

### DuckDB + GeoParquet/Iceberg

A particularly powerful combination: for region-specific ad hoc analysis, **DuckDB + Iceberg/GeoParquet** lets you do sophisticated geospatial queries on a laptop — no cluster required. (See also: [[DuckDB Spatial Supercharged Geospatial SQL - Summary]])

---

## 6. Implementation Timeline and Adoption

| Milestone | Date / Status |
|---|---|
| Parquet geo type specification | Merged Feb 2025 |
| Iceberg V3 geo type specification | Near-final vote (at time of talk, May 2025) |
| Wherobots (Havasu) early implementation | Available now on Wherobots Cloud |
| Java/Rust/Python Iceberg reference implementations | In progress |
| Snowflake / BigQuery / Spark native support | Pending V3 spec finalisation |
| Delta Lake geo type support | Planned (will reuse Parquet geo type definition) |

Note: the Parquet release is a prerequisite for full Iceberg V3 implementation in most engines. The Iceberg spec can be adopted independently, but implementations that want to use native Parquet row-group statistics need both.

---

## 7. Catalog Standardisation

A key remaining piece for the full open lakehouse story: **catalog interoperability**.

Iceberg delegates catalog management to an external interface. Historical implementation: Hive Metastore (Thrift-based, old but widely deployed). Modern implementation: **Iceberg REST Catalog** — a modern API-first catalog spec.

With a standardised catalog:
- Compute engines discover tables without engine-specific configuration
- **Access control and governance** can be enforced at the catalog level (Polaris, Unity Catalog, etc.)
- **Observability** — which rows, columns, and files were accessed, by whom, at what frequency — can be captured centrally
- **Data providers** gain visibility: instead of losing control after data is copied, they can track usage patterns and manage access via catalog policies

---

## 8. Foursquare's Geospatial Architecture

Foursquare processes:
- Billions of GPS pings per day
- Billions of place event impressions per day
- Places dataset: now open source (GeoParquet format)

Key use cases where Iceberg geo types will help:
- **Ad measurement by proximity**: determine which GPS pings are near a billboard (direction + proximity) → currently requires scanning all data; spatial filter pushdown will prune aggressively
- **GDPR deletion**: previously required custom bloom filter implementations and heavy custom tooling; Iceberg ACID + row-level delete handles this natively
- **Schema evolution**: changing partitioning on billion-row tables was previously a full rebuild; Iceberg handles it as a metadata-only operation

Current state: Iceberg adopted for most new non-geospatial workloads; beginning transition of geospatial workloads as V3 implementations mature.

---

## 9. Best Practices and What's Next

From the panel:

1. **File sizing matters**: too few large files → poor parallelism; too many small files → high metadata overhead. Regular compaction is necessary for good read performance.
2. **Partitioning is a first-class concern**: Iceberg lets you change partition schemes without rebuilding, but you need to think about spatial partitioning strategies (space-filling curves like XZ2 are being explored for geo workloads).
3. **Catalog is not optional**: you need both the table format and a catalog to have a complete, discoverable, governed system.
4. **Ecosystem adoption is the next step**: most geospatial users don't want to tune file sizes or pick CRS codes. The value comes when tools abstract these details and it "just works".
5. **Data provider access control**: Iceberg REST Catalog + access policies is the path to giving data providers back visibility and control over who accesses their data — essential for public sector and open data publishers.

---

## 10. Key Takeaways

| Topic | Summary |
|---|---|
| **GeoParquet** | Standardised metadata for geospatial columns in Parquet; interoperable across all major data platforms |
| **Iceberg V3 geo types** | Native geometry type with CRS + edge interpolation; row-group bounding box statistics |
| **Key performance win** | Row-group-level spatial statistics → fine-grained predicate pushdown (vs. file-level only before) |
| **ACID for geo** | GDPR deletion, concurrent compaction, schema evolution — all now straightforward |
| **Vendor lock-in solved** | Storage/compute separation: any engine reads Iceberg tables from object storage |
| **DuckDB synergy** | DuckDB + GeoParquet/Iceberg → powerful geospatial analytics on a laptop |
| **Delta Lake** | Will adopt Parquet geo type; Databricks working on Iceberg interoperability |
| **Catalog** | Missing piece — Iceberg REST Catalog + governance layer needed for full story |
| **Available now** | Wherobots Cloud (Havasu); other engines in progress pending V3 finalisation |
