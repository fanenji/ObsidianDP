---
title: 5 DuckDB GeoParquet Joins That Feel Instant
source: https://medium.com/@Nexumo_/5-duckdb-geoparquet-joins-that-feel-instant-88a6bf5a4670
author:
  - "[[Nexumo]]"
published: 2025-12-24
created: 2026-04-04
description: 5 DuckDB GeoParquet Joins That Feel Instant Use DuckDB + GeoParquet to run real spatial joins on a laptop — fast enough for dashboards, ad-hoc analysis, and “just one more question.” Learn 5 …
tags:
  - clippings
  - duckdb
  - geoparquet
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)

## Use DuckDB + GeoParquet to run real spatial joins on a laptop — fast enough for dashboards, ad-hoc analysis, and “just one more question.”

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*YwTnppvjHSYYPmiVPEb9qQ.png)

*Learn 5 fast DuckDB + GeoParquet join patterns for spatial analytics: point-in-polygon, bbox prefiltering, R-tree joins, nearest, and tiles.*

Let’s be real: “spatial analytics” usually comes with a side of pain. Big files. Slow joins. And that moment when you realize your “quick query” is actually an overnight job.

DuckDB changes the vibe. Pair it with **GeoParquet** and you can do serious geospatial joins in plain SQL, with performance that’s genuinely surprising when you first see it.

Below are **five join patterns** I keep reaching for — because they map cleanly to real workloads and they scale better than the naive “CROSS JOIN then filter” approach.

## A quick mental model: DuckDB + GeoParquet in one picture

GeoParquet is basically Parquet plus geospatial metadata; geometry is commonly stored as bytes (often WKB), and tools can interpret it as a geometry column.

DuckDB’s **spatial extension** gives you a `GEOMETRY` type and spatial predicates like `ST_Intersects`, `ST_Within`, `ST_Contains`, plus a lot more.

```c
GeoParquet (lake / files)
   |  read_parquet()
   v
DuckDB tables/views (GEOMETRY)
   |  JOIN ... ON ST_Intersects(...)
   v
Aggregates / features / export
```

One more thing: DuckDB has been investing heavily in spatial join performance (including a dedicated `SPATIAL_JOIN` operator for common predicate joins), so “this used to be slow” isn’t always true anymore.

## 1) Point-in-Polygon join that doesn’t melt your CPU

This is the classic: points (events, pickups, sensors) joined to polygons (neighborhoods, sales regions, admin boundaries).

## When it matters

- “How many deliveries per district?”
- “Which ward is each complaint in?”
- “Count check-ins by neighborhood”

## The join (DuckDB SQL)

```c
INSTALL spatial;
LOAD spatial;

-- Views directly over GeoParquet
CREATE VIEW events AS
SELECT
  event_id,
  ST_GeomFromWKB(geom) AS geom
FROM read_parquet('events.geoparquet');

CREATE VIEW districts AS
SELECT
  district_name,
  ST_GeomFromWKB(geom) AS geom
FROM read_parquet('districts.geoparquet');

SELECT
  d.district_name,
  count(*) AS events
FROM events e
JOIN districts d
  ON ST_Within(e.geom, d.geom)
GROUP BY 1
ORDER BY events DESC;
```

**Why this is faster than it looks:** spatial joins used to fall back to expensive nested-loop behavior, but DuckDB’s spatial join work focuses on avoiding quadratic “compare everything to everything” patterns by using bounding-box logic and R-tree strategies under the hood for common cases.

**Practical tip:** if your points are *really* points, `ST_Contains` / `ST_Within` is semantically cleaner than `ST_Intersects`, but test both—performance and edge cases can differ.

## 2) Bounding-box prefilter join (the “cheap first, exact second” trick)

You know what’s not glamorous? Rectangles.

You know what’s fast? Rectangles.

Most spatial predicates imply one simple truth: **if two geometries intersect, their bounding boxes intersect**. DuckDB’s spatial join discussion leans hard into this because it’s the gateway to pruning massive candidate sets before doing expensive geometry math.

## Pattern: two-phase join

1. filter candidates using bounding boxes (cheap comparisons)
2. confirm with `ST_Intersects` (exact, expensive)

A practical version is to store bbox columns alongside geometry in GeoParquet (xmin/ymin/xmax/ymax). That gives you “rectangle math” without recomputing envelopes for every row.

```c
-- Assume both datasets include bbox columns: xmin, ymin, xmax, ymax
CREATE VIEW a AS SELECT *, ST_GeomFromWKB(geom) AS g FROM read_parquet('a.geoparquet');
CREATE VIEW b AS SELECT *, ST_GeomFromWKB(geom) AS g FROM read_parquet('b.geoparquet');

SELECT a.id, b.id
FROM a
JOIN b
  ON a.xmin <= b.xmax
 AND a.xmax >= b.xmin
 AND a.ymin <= b.ymax
 AND a.ymax >= b.ymin
 AND ST_Intersects(a.g, b.g);
```

Let’s be real: this looks like busywork until you run it on tens of millions of rows and watch it go from “nope” to “okay, wow.”

## 3) Region-of-interest join with an R-tree index (fast filters, fast joins)

Sometimes you’re not joining two huge datasets. Sometimes you’re asking:

> *“Give me all features within* this *area.”*

This is where **R-tree indexing** shines. DuckDB supports R-tree indexes for `GEOMETRY`, and (importantly) it can use them for common spatial predicates when the query region is known at planning time.

## Pattern: index the big table, filter by a constant geometry

```c
INSTALL spatial;
LOAD spatial;

CREATE TABLE pois AS
SELECT
  name,
  ST_GeomFromWKB(geom) AS geom
FROM read_parquet('pois.geoparquet');

-- Bulk-load index after data load (usually better)
CREATE INDEX pois_rtree ON pois USING RTREE (geom);

-- “Constant” region of interest: envelope around a city center
SELECT name
FROM pois
WHERE ST_Within(geom, ST_MakeEnvelope(72.77, 18.89, 72.99, 19.20));
```

DuckDB’s own docs are blunt about why this matters: full scans don’t scale for spatial filtering, and R-trees let you skip huge parts of the dataset via bounding rectangles.

## 4) Nearest-neighbor join that’s actually usable

Nearest-neighbor is the join everyone wants (“closest store”, “nearest clinic”, “nearest road segment”)… and the join that quietly ruins your afternoon if you do it naively.

## A production-ish pattern

- narrow candidates with a distance window or bbox expansion
- then compute exact distances and rank
```c
CREATE VIEW users AS
SELECT user_id, ST_GeomFromWKB(geom) AS geom
FROM read_parquet('users.geoparquet');

CREATE VIEW stores AS
SELECT store_id, ST_GeomFromWKB(geom) AS geom
FROM read_parquet('stores.geoparquet');

-- 1) candidate filter: only stores within ~2km (adjust to your CRS)
WITH candidates AS (
  SELECT
    u.user_id,
    s.store_id,
    ST_Distance(u.geom, s.geom) AS dist
  FROM users u
  JOIN stores s
    ON ST_DWithin(u.geom, s.geom, 2000)
)
SELECT *
FROM (
  SELECT
    user_id, store_id, dist,
    row_number() OVER (PARTITION BY user_id ORDER BY dist) AS rn
  FROM candidates
)
WHERE rn = 1;
```

DuckDB’s spatial join notes even highlight how predicate choice can dramatically change performance — especially when implementations are optimized and avoid extra allocation overhead.

The human takeaway: don’t treat “nearest” as one query. Treat it as **candidate generation + exact ranking**.

## 5) Tile-based join (make the join smaller on purpose)

If your data is big, the join strategy that wins is often the one that refuses to join the whole world at once.

Tile the space. Join within tiles. Merge results.

This is the approach behind a lot of scalable spatial systems, and DuckDB gives you tools to make it practical — like functions for computing spatial order keys (e.g., Hilbert indexing) that help you cluster nearby geometries.

## Pattern: compute a spatial key, then join within that neighborhood

```c
-- Example: assign points to a Hilbert cell (you choose bounds + resolution)
CREATE VIEW p AS
SELECT
  *,
  ST_GeomFromWKB(geom) AS g,
  ST_Hilbert(ST_X(ST_Centroid(ST_GeomFromWKB(geom))),
             ST_Y(ST_Centroid(ST_GeomFromWKB(geom))),
             0, 0, 100, 100) AS hkey
FROM read_parquet('points.geoparquet');

CREATE VIEW poly AS
SELECT
  *,
  ST_GeomFromWKB(geom) AS g,
  ST_Hilbert(ST_X(ST_Centroid(ST_GeomFromWKB(geom))),
             ST_Y(ST_Centroid(ST_GeomFromWKB(geom))),
             0, 0, 100, 100) AS hkey
FROM read_parquet('polygons.geoparquet');

-- Join within a key band, then do the exact predicate
SELECT p.id, poly.region
FROM p
JOIN poly
  ON abs(p.hkey - poly.hkey) <= 5000
 AND ST_Intersects(p.g, poly.g);
```

Is this perfect? No. You’ll tune the bounds, the key window, and probably add bbox prefilters too.

But when you’re staring at a huge join and thinking “there’s no way,” tiling is how you make it *possible*.

## Final thoughts: speed comes from being picky

Fast spatial analytics isn’t about one magic function. It’s about getting picky early:

- prune with bounding boxes before exact predicates
- use R-trees where a region-of-interest filter dominates
- break “nearest” into candidates + ranking
- tile big joins so you’re never comparing everything to everything

If you’re using DuckDB + GeoParquet today, I’d love to hear what your pain point is: point-in-polygon? nearest? something weirder?

Drop a comment with your dataset shape (rows, geometry types, what you’re joining), follow for more practical SQL performance posts, and if you want a next step — try rewriting one of your slow spatial joins using the bbox-first pattern and compare timings.

[![Nexumo](https://miro.medium.com/v2/resize:fill:96:96/1*ZsbgHlcAcVSKsILknh8-0w.png)](https://medium.com/@Nexumo_?source=post_page---post_author_info--88a6bf5a4670---------------------------------------)

[![Nexumo](https://miro.medium.com/v2/resize:fill:128:128/1*ZsbgHlcAcVSKsILknh8-0w.png)](https://medium.com/@Nexumo_?source=post_page---post_author_info--88a6bf5a4670---------------------------------------)

[881 following](https://medium.com/@Nexumo_/following?source=post_page---post_author_info--88a6bf5a4670---------------------------------------)

Next-move engineering for builders - fast, clear, measurable. Systems, data, and AI you can ship today.