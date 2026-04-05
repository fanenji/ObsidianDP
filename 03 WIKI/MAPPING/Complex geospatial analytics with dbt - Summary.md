---
title: "Complex Geospatial Analytics with dbt — Summary"
type: note
topic: data-platform
created: 2026-04-04
tags:
  - mapping
  - dbt
  - geospatial
  - h3
  - snowflake
  - openstreetmap
source: "[[Complex geospatial analytics with dbt - Video Transcript]]"
speaker: Assaf Lavi (Nexar)
event: Big Things Conference, 2022
---

# Complex Geospatial Analytics with dbt

**Speaker:** Assaf Lavi, Principal Engineer @ Nexar
**Event:** Big Things Conference — June 19, 2022
**Video:** https://www.youtube.com/watch?v=UCEFHXUBqr0

---

## Context: Nexar and the Problem Space

**Nexar** is a dashcam company (~7–8 years old at the time) whose mission is to index the physical world the same way search engines index the web. With ~500,000 dashcams deployed on US roads and 4 trillion images collected, they produce enormous volumes of GPS and vision data used to provide:

- Road intelligence APIs (blockages, slowdowns, parking availability)
- AI training data for autonomous vehicles and mapping providers
- Services for OEMs, insurance companies, auto fleets, and public sector

The core data engineering challenge is **quantifying supply**: given a specific geographic area, do we have enough data to provide a service to a customer?

### The Raw Data Problem

Raw GPS data consists of timestamps, latitude, longitude, speed, and altitude — and it is **inherently messy** (satellite signal degradation causes noise). Even perfect GPS is meaningless without context: business stakeholders ask questions like:

- *"How many residential road miles do we cover in San Francisco this month?"*
- *"How many unique users drove through Manhattan last week?"*

These questions are framed in human geographic dimensions (road type, city, county, state) that don't exist in raw GPS. The entire engineering effort described in the talk is about **enriching GPS data with meaningful geospatial dimensions**.

---

## Stack

A standard Modern Data Stack:

```
GPS/Vision Data → Amazon S3 (Parquet/ORC) → Snowflake → dbt → Looker
```

Some preprocessing (H3 enrichment, OSM parsing) is done with **PySpark** before loading into Snowflake.

---

## Part 1 — dbt Techniques for Large Data

### 1.1 Development Environment Setup

#### Profiles and Dev Target

In `profiles.yml`, each developer defines their own schema as the `dev` target:

```yaml
nexar:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: ...
      database: ...
      schema: dev_assaf   # personal dev schema
```

Setting `dev` as the default target prevents accidentally running against production.

#### Partial Data in Dev via `target.name`

dbt models can reference the active target at runtime using Jinja:

```sql
SELECT * FROM {{ ref('postgres_rides') }}
{% if target.name == 'dev' %}
  WHERE loaded_at >= DATEADD(day, -3, CURRENT_DATE)
{% endif %}
```

This injects a 3-day filter in dev, enabling fast iteration without processing the full dataset.

#### Zero-Copy Clone for Dev Reset (Snowflake)

At the start of a new feature branch, developers run a dbt operation that:
1. Creates the dev schema if it doesn't exist (or drops and recreates it)
2. Clones the full production schema using **Snowflake Zero-Copy Cloning**

```sql
CREATE OR REPLACE SCHEMA {{ target.schema }}
  CLONE production.public;
```

This takes ~5 minutes and copies only metadata (no actual data movement). Developers get a full, isolated copy of production to work against safely.

---

### 1.2 Materialization Strategies for Large Tables

#### Standard Incremental

The default `table` materialization rebuilds the entire table on every run — impractical for large datasets. **Incremental** materialization processes only new data:

```sql
{{ config(materialized='incremental') }}

SELECT * FROM {{ ref('base_rides') }}
{% if is_incremental() %}
  WHERE loaded_at > (SELECT MAX(loaded_at) FROM {{ this }})
{% endif %}
```

- Requires a `loaded_at` (or similar) column to track the high watermark
- Works for daily, weekly, or any cadence — automatically picks up data since the last run
- **Recommended starting point** for any large dataset in dbt

#### Insert By Period (Advanced)

From the `dbt_utils` package. Best for data that is:
- Cleanly partitioned by time
- Bulk-updated once per day with **no late-arriving data**

This strategy chunks the source data into time periods and processes one chunk at a time. Key benefits:
- Avoids memory/resource limits for very large backfills
- Can be paused and resumed mid-backfill

**Trade-off:** Sensitive to late-arriving data. If records can arrive after their processing window, reprocessing is needed.

> Recommendation: start with incremental. If performance is poor, consider insert_by_period.

---

### 1.3 Manual Clustering Keys (Snowflake)

By default, Snowflake automatically partitions data internally. For very large tables with **predictable query patterns**, manual clustering can dramatically reduce scan costs:

```sql
{{ config(
    materialized='incremental',
    cluster_by=['operating_system', 'DATE(ride_start_at)']
) }}
```

When a query filters by `operating_system = 'Android'`, Snowflake's query optimizer prunes partitions and scans only relevant data.

**When to use it:**
- Query patterns are highly predictable (consistent filter columns)
- Table is very large and filter pruning is impactful

**When to avoid it:**
- Ad-hoc, unpredictable query patterns — manual clustering can hurt performance in those cases

> Manual clustering pairs extremely well with incremental materialization.

---

## Part 2 — Geospatial Data Engineering

### 2.1 OpenStreetMap (OSM) — Road Network

Nexar uses OSM as the authoritative road network definition. A full planet dump is downloaded periodically and pre-processed with PySpark.

**OSM Entity Model:**

| Entity | Description |
|---|---|
| **Node** | A single point in space (lat/lon) |
| **Way** | An ordered sequence of nodes (can be a road, river, building boundary) |
| **Relation** | A grouping of ways/nodes with shared meaning |

All entities carry **key-value tags**. The most important for roads is the `highway` tag on Way entities, whose value indicates road type:
- `motorway`, `trunk`, `primary`, `secondary`, `residential`, `service`, etc.

**Road segments** are derived as source→destination node pairs from Ways. **Road length** is computed as the sum of Haversine distances between consecutive nodes:

```sql
SUM(HAVERSINE(lat1, lon1, lat2, lon2))
```

This allows answering map-topology questions like: *"What is the distribution of road types by county in North Central Texas?"* — purely from OSM data, independent of Nexar's GPS data.

---

### 2.2 Who's on First — Place Identifiers

Rather than relying on city/country names (which are ambiguous — there are multiple Detroits, multiple Jerusalems), Nexar uses **[Who's on First](https://whosonfirst.org/)**, an open-source gazetteer of places.

**Key features:**

| Feature | Value |
|---|---|
| **Stable integer IDs** | Unique, unambiguous foreign keys — no name collisions |
| **Precise GeoJSON shapes** | Full polygon boundaries (not just bounding boxes) |
| **Administrative hierarchy** | Countries → Regions → Counties → Localities (cities/towns) |
| **Population metadata** | Filter by population threshold (e.g., "cities > 100,000 people in Europe") |
| **Git-based distribution** | Clone a repo per country/region; each place is a GeoJSON file |

**Why this matters:** Using stable IDs as foreign keys between tables is far more reliable than using names. Bounding boxes (used previously) produce inaccurate results; precise polygon shapes are critical for correct spatial queries.

The hierarchy allows grouping at any level: data in the 5 NYC boroughs, all cities in California, etc.

---

### 2.3 H3 — The Unifying Layer

**H3** is Uber's open-source hierarchical hexagonal grid system for the Earth's surface. Google has a similar system called **S2** (uses quadrilateral cells).

#### Why Hexagons?

Point-in-polygon queries are computationally expensive in any data warehouse. H3 solves this by replacing every geographic point or polygon with an **integer** (the hexagon ID). Equality checks on integers are orders of magnitude faster than spatial operations, especially in columnar storage systems like Snowflake.

#### How the Grid Works

- The Earth is divided into hexagons at multiple resolutions (levels 0–15)
- Each hexagon has 7 sub-hexagons at the next finer resolution
- Every location maps to exactly one hexagon at any resolution
- Parent hexagons can be computed from child hexagons using **bit-shift operations** (no lookup required)
- Resolution 12 ≈ 9–20m edge length — used for locating individual GPS samples

| Resolution | Approx. Edge Length | Use Case |
|---|---|---|
| 8 | ~460m | US States |
| 10 | ~65m | Cities |
| 12 | ~9–20m | Individual GPS samples / road segments |

#### Polyfill: Converting Polygons to H3

A geographic shape (e.g., California) is converted to a set of H3 hexagons at a chosen resolution ("polyfilling"). Instead of a point-in-polygon query, you do a set membership check:

```sql
-- Instead of: ST_CONTAINS(california_polygon, point)
-- Do: h3_index IN (SELECT h3_index FROM california_hexagons)
```

This converts spatial filtering to integer equality — fast, parallelizable, columnar-friendly.

---

### 2.4 GPS Map Matching

Raw GPS samples must be **snapped to the OSM road network** before assigning H3 indexes. A GPS reading captured while driving may be a few meters off the actual road due to signal noise.

The process:
1. Take the raw GPS point
2. Interpolate the most plausible position on the nearest OSM road segment (map matching)
3. Compute the H3 index at resolution 12 for that snapped position

This is done in PySpark before loading data into Snowflake, enriching every GPS sample with its H3 index.

---

### 2.5 The dbt Geo Layer

The enriched data (OSM + Who's on First + H3) is organized in dbt as a **geographic dimension layer** that all downstream models join against. The dependency graph follows this structure:

```
Who's on First (raw)         OSM (raw)
       │                         │
  WoF H3 hexagons           OSM nodes + road segments
  (by resolution:            (enriched with H3)
   localities, regions,           │
   counties, countries)           │
       └──────────┬───────────────┘
                  │
           HEX_EGG table
       (road segment × hexagon)
       + locality + region + county
                  │
         Daily rollup models
       (GPS samples / rides / users
        by road segment, per geography)
```

#### The HEX_EGG Table

The central join table combining:
- **H3 hexagon** at resolution 12 (precise location on a road)
- **OSM road segment** (road type, direction, length)
- **Who's on First locality, county, region** (human geography)

This is a cartesian product of hexagons × road segments, pre-enriched with all geographic dimensions. It is **expensive to build once** but makes all downstream queries trivially simple.

#### Example Rollup Query

```sql
-- Daily rides/users rollup per road segment
SELECT
    rs.source_node_id,
    rs.destination_node_id,
    rs.road_type,
    rs.locality_id,
    rs.county_id,
    rs.region_id,
    SUM(gps.samples)   AS daily_samples,
    COUNT(DISTINCT gps.ride_id) AS daily_rides,
    COUNT(DISTINCT gps.user_id) AS daily_users
FROM daily_gps_samples gps
JOIN road_segments rs
    ON gps.source_node_id = rs.source_node_id
    AND gps.destination_node_id = rs.destination_node_id
GROUP BY 1,2,3,4,5,6
```

**Result:** Analysts and executives can query this table without knowing anything about H3, OSM, or geospatial concepts. They simply filter by `locality_id` or `county_id` and group by `road_type`.

---

### 2.6 H3 UDFs in dbt (Snowflake)

Different geographic dimensions require different H3 resolutions:
- **Resolution 8** → US States
- **Resolution 10** → Cities / Localities
- **Resolution 12** → Individual GPS samples / road segments

Traversing between resolutions is done via **bitwise operations** (no lookup tables), implemented as SQL UDFs and managed in dbt:

```sql
-- Get resolution 8 parent from a resolution 12 index (bit shift)
CREATE FUNCTION h3_to_parent_8(h3_index BIGINT)
RETURNS BIGINT AS
$$
  -- zero out non-significant bits, shift to resolution 8
  (h3_index >> N) << N
$$;
```

dbt ensures these UDFs are:
- **Version controlled** (alongside models)
- **Consistently deployed** across dev and production
- **Tested** like any other data asset

---

## Key Takeaways

### General dbt Best Practices for Large Data

| Technique | When to Use |
|---|---|
| **Dev target + partial data** | Always — avoid running full datasets in development |
| **Zero-copy clone** | Start of every feature branch (Snowflake-specific) |
| **Incremental materialization** | Default choice for large tables |
| **Insert by period** | High-volume tables with clean time partitioning, no late data |
| **Manual clustering** | Very large tables with predictable, stable filter patterns |

### Geospatial Data Engineering Approach

| Problem | Solution |
|---|---|
| Raw GPS is noisy and meaningless | Map-match to OSM road network |
| Road topology and types | OpenStreetMap (nodes, ways, highway tags) |
| Ambiguous place names | Who's on First (stable integer IDs + precise GeoJSON shapes) |
| Expensive point-in-polygon queries | H3 hexagonal indexing — replace spatial ops with integer equality |
| Multi-resolution geography | H3 parent traversal via bit operations (fast, no joins) |
| Consistent UDF management | Implement H3 functions as dbt-managed SQL UDFs |

### The Core Insight

> By converting all geographic data — GPS samples, road segments, and place boundaries — into H3 integer indexes, every spatial join becomes an integer equality check. This is the fundamental reason why the system scales: columnar data warehouses (Snowflake, BigQuery, Databricks) are optimized for integer operations, not for polygon geometry.

The result: a non-technical analyst can query *"how many unique users drove on residential roads in San Francisco last month?"* with a simple GROUP BY query — with no knowledge of H3, OSM, or geospatial computation required.
