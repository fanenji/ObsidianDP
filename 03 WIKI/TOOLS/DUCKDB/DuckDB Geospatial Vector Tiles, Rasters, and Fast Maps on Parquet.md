---
title: "DuckDB Geospatial: Vector Tiles, Rasters, and Fast Maps on Parquet"
source: https://medium.com/@2nick2patel2/duckdb-geospatial-vector-tiles-rasters-and-fast-maps-on-parquet-f08ae70c73b8
author:
  - "[[Codastra]]"
published: 2025-11-29
created: 2026-04-04
description: "DuckDB Geospatial: Vector Tiles, Rasters, and Fast Maps on Parquet How to go from GeoParquet and imagery to production-ready web maps — without a heavyweight GIS stack. Use DuckDB’s spatial …"
tags:
  - clippings
  - mapping
  - duckdb
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)

## How to go from GeoParquet and imagery to production-ready web maps — without a heavyweight GIS stack.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*m0jZ14Le0Vf5b9LV11JMbg.png)

Use DuckDB’s spatial extension, vector tiles, and Parquet/GeoParquet to build fast, modern web maps directly on your data lake — no PostGIS cluster required.

You’ve got geospatial data sitting in Parquet or GeoParquet. Maybe some satellite imagery in cloud buckets. And you’d really like to turn all of that into a fast, interactive map… without spinning up PostGIS, a tile server, a cache layer, and three new incident types.

DuckDB’s spatial extension quietly changes that story. With vector tiles, raster support via GDAL, and columnar Parquet under the hood, you can build “just SQL” map backends that scale surprisingly far.

Let’s unpack how.

## Why Geospatial Belongs Inside DuckDB

Most geospatial stacks still assume a classic pattern: push data into a spatial database, then build everything around that database.

DuckDB flips the direction:

- **Data stays in Parquet / GeoParquet** in your lake or bucket.
- **DuckDB is the compute layer**, not the system of record.
- Geospatial becomes “just another analytic dimension,” alongside events, metrics, and time series.

That matters because:

- You avoid complex ETL into specialized GIS stores.
- The same SQL engine can join **geometries + business facts** in one shot.
- For many dashboards and APIs, “good enough” geospatial is really “fast and cheap” geospatial.

Let’s be real: most teams don’t need a full-blown enterprise GIS. They need “show me points in this polygon, on top of the rest of my analytics.”

## A 60-Second Primer on DuckDB Spatial

DuckDB’s `spatial` extension adds:

- A `GEOMETRY` type (POINT, LINESTRING, POLYGON, MULTI\*, etc.).
- A PostGIS-like set of `ST_` functions (`ST_Intersects`, `ST_Buffer`, `ST_Transform`, etc.).
- Table functions for reading vector formats (GeoParquet, Shapefile, GeoJSON, etc.).
- Integration with GDAL/PROJ/GEOS under the hood.

Basic setup:

```c
INSTALL spatial;
LOAD spatial;

-- Read GeoParquet with geometries
CREATE TABLE roads AS
SELECT *
FROM 's3://my-bucket/roads_geoparquet.parquet';

-- Quick spatial filter
SELECT name
FROM roads
WHERE ST_Intersects(geom, ST_GeomFromText('POLYGON(...)', 4326));
```

If your geometries are stored in GeoParquet as WKB, you can cast them with `ST_GeomFromWKB` and keep everything fully columnar. ([DuckDB](https://duckdb.org/2023/04/28/spatial.html?utm_source=chatgpt.com))

## Architecture: Fast Maps on Parquet

A “DuckDB-powered map backend” usually looks like this:

```c
+-----------------------+
|   Browser / MapLibre  |
|   (or Mapbox GL JS)   |
+-----------+-----------+
            |
            | HTTPS /tiles/{z}/{x}/{y}.mvt
            v
+-----------------------+
|   Tile API (Flask,    |
|   FastAPI, Node, …)   |
+-----------+-----------+
            |
            | SQL over DuckDB
            v
+-----------------------+
| DuckDB + spatial      |
| • GeoParquet (vector) |
| • COG / raster files  |
+-----------+-----------+
            |
            v
      Object Storage
  (S3 / GCS / local FS)
```

The key idea: **each tile request becomes a parameterized SQL query** into Parquet/GeoParquet (and sometimes rasters), which DuckDB can execute in milliseconds when scoped to a small geographic extent.

## Serving Vector Tiles Straight from DuckDB

Mapbox Vector Tiles (MVT) are the modern workhorse for basemaps and data overlays. Historically, you’d generate MVTs from PostGIS using `ST_AsMVT` and `ST_AsMVTGeom`.

DuckDB’s spatial extension is gaining the same capability with `ST_AsMVT` and `ST_AsMVTGeom`, enabling direct vector tile generation from DuckDB. ([Spatialists – geospatial news](https://spatialists.ch/posts/2025/09/10-vector-tiles-coming-to-duckdb/?utm_source=chatgpt.com)) Early examples already show tiles being streamed from DuckDB + Flask into MapLibre clients using large GeoParquet datasets stored in the cloud.

A minimal tile query conceptually looks like this (API surface may evolve, but the pattern stands):

```c
-- Parameters: :z, :x, :y
WITH tile_bounds AS (
  SELECT *
  FROM ST_TileEnvelope(:z, :x, :y) AS env   -- returns polygon in Web Mercator
),
features AS (
  SELECT
    id,
    name,
    ST_AsMVTGeom(
      ST_Transform(geom, 3857),    -- project to Web Mercator
      (SELECT env FROM tile_bounds),
      4096,                        -- tile extent
      64,                          -- buffer
      true                         -- clip geom
    ) AS geom
  FROM roads
  JOIN tile_bounds
    ON ST_Intersects(
         ST_Transform(geom, 3857),
         env
       )
)
SELECT ST_AsMVT(features, 'layer_name', 4096) AS mvt
FROM features;
```

Your HTTP handler simply passes `z/x/y` into this query and returns the `mvt` blob as `application/vnd.mapbox-vector-tile`.

A tiny Flask-ish sketch:

```c
import duckdb
from flask import Flask, Response

con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")

app = Flask(__name__)

@app.get("/tiles/<int:z>/<int:x>/<int:y>.mvt")
def tiles(z, x, y):
    [row] = con.execute(
        "SELECT mvt FROM generate_tile(?, ?, ?)",  # wrap SQL above in a VIEW/PROC
        [z, x, y],
    ).fetchall()
    return Response(row[0], mimetype="application/vnd.mapbox-vector-tile")
```

You might be wondering, “Is this actually fast enough?” For typical vector overlays (points, roads, polygons) where source data is columnar GeoParquet, the answer is often *yes*, especially with a warm cache and modest tile density.

## What About Rasters?

Vector is only half the story. Many use cases — remote sensing, NDVI, heatmaps — depend on raster data.

Officially, DuckDB’s spatial extension started with vector and didn’t ship a native raster type. But thanks to GDAL integration, people are already managing satellite imagery through the extension, exposing raster operations via SQL and DuckDB functions.

The emerging pattern looks like this:

1. **Store imagery as COGs** (Cloud Optimized GeoTIFF) in object storage.
2. Keep a **footprint/metadata table in Parquet or DuckDB**:
- raster ID, path, bbox, resolution, band info, etc.

3\. For each map request:

- Find overlapping rasters via `ST_Intersects` on the footprints.
- Use GDAL-backed functions to read a window (tile-sized) from each raster.
- Optionally compute indices (e.g., NDVI) or color ramps.
- Serve as PNG/JPEG tiles or even as derived vector contours.

A simplified SQL-ish pseudo-interface might look like:

```c
-- footprints table: id, path, bbox (GEOMETRY)
WITH tile AS (
  SELECT ST_TileEnvelope(:z, :x, :y) AS env
),
rasters AS (
  SELECT path
  FROM raster_footprints, tile
  WHERE ST_Intersects(bbox, env)
)
SELECT ST_RenderRasterTile(path, (SELECT env FROM tile), :z, :x, :y)
FROM rasters;
```

Under the hood, `ST_RenderRasterTile` would delegate to GDAL to read only the necessary window—a crucial trick to make this scale.

Is it as mature as decades-old raster engines? Not yet. But for many analytics workflows, pulling raster windows directly into DuckDB and joining them with tabular data is incredibly powerful.

## Real-World Use Cases

A few patterns I keep seeing:

## 1\. “Analytics First” Map Backends

Product teams already have Parquet-ified event or asset data. Adding a spatial column and a tile endpoint lets them ship:

- Store locator maps.
- Delivery coverage maps.
- IoT sensor maps.

…without standing up a separate geospatial database.

## 2\. Mobility & Transport Dashboards

Trips, routes, and stops are natural vector data. With DuckDB:

- Raw GPS trajectories live as Parquet.
- A `GEOMETRY` column represents linestrings.
- Aggregations (e.g., congestion per segment) run in the same engine that powers BI queries.

Tiles become just another view over analytics, not a separate pipeline.

## 3\. Environmental and Remote Sensing Analytics

Combining:

- Raster tiles from COGs (vegetation, temperature, flood risk).
- Vector layers of assets, buildings, or parcels.
- All queried via one SQL engine and visualized as tiles.

This is the kind of “spatial + analytics” blend GIS tools promised, but with a dev-friendly, file-centric approach.

## Gotchas and Practical Tips

A few lessons that save headaches:

- **Push as much as possible into GeoParquet.** Keep geometries and attributes together in columnar files; DuckDB is happiest there.
- **Use Web Mercator consistently for tiling.** Store source data in EPSG:4326, but project to 3857 at query time for tile math.
- **Tune memory limits.** DuckDB lets you control memory usage; for busy tile servers, nudge this up and consider on-disk `.duckdb` databases when you need persistence.
- **Cache aggressively.** Cloudfront, Varnish, or even an in-process LRU for hot tiles can slash compute.
- **Start simple.** One or two vector layers, a single tileset, then grow into multiple layers and styling.

## Wrapping Up

DuckDB geospatial isn’t trying to replace every GIS stack. But if your data already lives in Parquet/GeoParquet, it gives you a very tempting proposition:

- **No heavyweight geospatial database.**
- **No bespoke ETL to a tile pipeline.**
- **Just SQL over files + a thin HTTP layer = fast maps.**

If you’re curious, the next step is straightforward: take one existing GeoParquet dataset, install the spatial extension, and prototype a `/tiles/{z}/{x}/{y}` endpoint. You’ll learn more in an afternoon of tinkering than in a week of theory.

If this sparked ideas — or you’re already doing wild things with DuckDB Spatial — drop a comment, share your setup, and follow along. There’s a lot more coming in the geospatial + DuckDB world, and it’s moving quickly.

[![Codastra](https://miro.medium.com/v2/resize:fill:96:96/1*IZcptplBcXPdWGYUkOqYnA.png)](https://medium.com/@2nick2patel2?source=post_page---post_author_info--f08ae70c73b8---------------------------------------)

[![Codastra](https://miro.medium.com/v2/resize:fill:128:128/1*IZcptplBcXPdWGYUkOqYnA.png)](https://medium.com/@2nick2patel2?source=post_page---post_author_info--f08ae70c73b8---------------------------------------)

[662 following](https://medium.com/@2nick2patel2/following?source=post_page---post_author_info--f08ae70c73b8---------------------------------------)

Exploring where code meets creativity. Writing on AI, tech, and the craft of building systems with rhythm, clarity, and orchestration.