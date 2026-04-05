---
title: "DuckDB Spatial: Supercharged Geospatial SQL — Summary"
type: note
topic: data-platform
created: 2026-04-04
tags:
  - duckdb
  - geospatial
  - spatial
  - sql
  - python
  - mapping
source: "[[DuckDB Spatial Supercharged Geospatial SQL]]"
speaker: Max Gabrielsson (DuckDB Labs)
event: GeoPython 2024
slides: https://blobs.duckdb.org/papers/duckdb-spatial-geopython-2024.pdf
---

# DuckDB Spatial: Supercharged Geospatial SQL

**Speaker:** Max Gabrielsson, Software Engineer @ DuckDB Labs
**Event:** GeoPython 2024
**Video:** https://www.youtube.com/watch?v=hoyQnP8CiXE
**Slides:** https://blobs.duckdb.org/papers/duckdb-spatial-geopython-2024.pdf

---

## 1. What is DuckDB?

DuckDB is an **analytical embedded SQL database**:
- Originally a research project at CWI (National Research Institute, Amsterdam)
- Free and open source — MIT licensed, no dual license, no open core
- No external dependencies — runs almost everywhere (Windows, Linux, macOS, WebAssembly, mobile)
- Current version at time of talk: v0.10.3 (pre-release)
- Developed and supported by **DuckDB Labs** (~18 people, Amsterdam)

The core value proposition: **makes the most out of your laptop** for analytical workloads.

---

## 2. Why DuckDB — Three Core Focuses

### 2.1 Execution: Vector-at-a-Time Model

DuckDB's execution model addresses the trade-offs of the two classical approaches:

| Model | Used by | Pros | Cons |
|---|---|---|---|
| **Row-at-a-time** | SQLite, PostgreSQL, SQL Server | Low memory footprint | High CPU overhead (shuffling rows, not data) |
| **Column-at-a-time** | Pandas, most dataframe libraries | SIMD-friendly, efficient iteration | Very large memory footprint (whole column in memory) |
| **Vector-at-a-time** | DuckDB, many modern engines | Best of both worlds | — |

DuckDB processes a **chunk (vector) of rows** sized to fit in the **CPU cache** — so the working set never needs to go out to RAM during processing. Combined with **multi-threading**, this leverages all available cores (e.g., M3 laptops with 16 cores).

Additional unique feature: DuckDB's execution model is **optionally order-preserving**, unlike most database engines. This gives dataframe-like semantics — you can slice and dice rows and know that input/output rows remain correlated.

### 2.2 Storage: Columnar, Compressed, ACID

A common misconception is that DuckDB is an in-memory database. It is not. DuckDB has a **proper database file format** (one file = one database, like SQLite) with:

- **Columnar on-disk storage** — columns stored individually, enabling per-column statistics for fast predicate pushdown
- **Lightweight compression** — same-type, same-distribution data compresses much better than row-wise; achieves **3–5× storage reduction** in practice
- **Faster reads** — counter-intuitively, compressed reads are faster because disk I/O (not CPU) is the bottleneck; reading less data wins
- **ACID properties** — full transactional support: all-or-nothing pipeline transformations, no partial failures
- **Supports updates** — unlike Parquet

> "If you recognize the picture of a data project directory with CSVs, shapefiles, notebooks, zip files, and dreaded `final_v2.parquet` — you need a database. By not using one, you've offloaded all that data management work onto yourself."

### 2.3 UX: In-Process, No Config, Graceful Degradation

#### In-Process Deployment

DuckDB runs **inside the calling process** — no separate server, no config files, no environment variables, no Docker. Benefits:

- **Near-zero data transfer overhead** — no serialization/deserialization over a socket like with PostgreSQL
- **Embeddable as a component** — can run as a backend server (FastAPI), a client-side library, in the browser via WebAssembly, or on mobile
- **Shares memory with the host process** — enables zero-copy dataframe interoperability (see §3)

#### Graceful Degradation

When DuckDB runs out of RAM, it **spills intermediate results to disk** rather than crashing or aborting. Almost all operators (joins, aggregations, sorts) implement this. The goal: *always make progress*.

Benchmark result: compared to other engines under a 32 GB memory limit, DuckDB shows a smooth performance curve as data size exceeds RAM — other engines either abort, time out, or hit a sharp performance spike.

#### Friendly SQL

DuckDB's SQL dialect is a **superset of PostgreSQL's**. Notable extensions:
- `FROM` before `SELECT` (swap clause order)
- `GROUP BY ALL` — group by all non-aggregated columns automatically
- Dynamic column selections — useful for wide tables
- Nested types and lambda functions
- List comprehensions (Python-inspired)
- Unified function call syntax — `column.function()` style

---

## 3. Python Integration

DuckDB provides **three Python APIs**:

| API | Style | Notes |
|---|---|---|
| **Standard DB API** | Connections, cursors | Familiar if you've used any Python database driver |
| **PySpark-compatible API** | Spark-like | Drop-in replacement for PySpark code |
| **Relational API** | Chainable, lazy | Recommended — composable like a dataframe, but fully optimized |

### Relational API (Recommended)

The relational API is **completely lazy**: operators are chained in Python but nothing executes until a terminating call (`.show()`, `.to_table()`, `.fetchall()`). This lets DuckDB see the **entire query plan at once** and apply all optimizations before execution.

### Zero-Copy Dataframe Interoperability

Because DuckDB is in-process and shares the same address space as Python, it can read dataframes **directly from memory** without copying:

```python
import duckdb
import pandas as pd

df = pd.DataFrame(...)
result = duckdb.sql("SELECT * FROM df WHERE value > 100")  # reads df directly
```

Supported formats: **Pandas, Polars, NumPy, PyArrow** — scan them in SQL queries directly.

Results can also be exported back to any of these formats for downstream processing (e.g., plotting).

---

## 4. DuckDB Extensions

Extensions are **compiled modules** (plugins) downloadable and loadable at runtime from within DuckDB:

```sql
INSTALL spatial;
LOAD spatial;
```

They can provide: types, functions, operators, optimizer rules, table scans. DuckDB Labs' philosophy: *"anything not essential to DuckDB core should be an extension."*

Available official extensions include: JSON support, PostgreSQL/MySQL/SQLite integration, AWS/Azure connectors — and **spatial**.

---

## 5. The Spatial Extension

The `spatial` extension adds geospatial capabilities to DuckDB, modeled after **PostGIS**:

### 5.1 Core Capabilities

- **Simple Features geometry type** — points, linestrings, polygons, multi-geometries, geometry collections
- **100+ `ST_` functions** (counting overloads) — covering most of what PostGIS offers
- **Full 3D support** — Z, M, and ZM coordinate dimensions (intersection and all standard functions)
- **3,000+ built-in CRS definitions** — the entire default PROJ database is embedded; no local PROJ installation needed
- **GDAL integration** — reads any GDAL-supported spatial format (shapefiles, GeoJSON, GeoPackage, etc.) via `ST_Read()`
- **No runtime dependencies** — GDAL and PROJ are statically bundled into the binary; no version conflicts with local installs

### 5.2 Installation and Setup

```sql
INSTALL spatial;
LOAD spatial;
```

That is all. No other setup, no environment configuration.

Pre-built binaries available for: Windows, Linux, macOS (including ARM), WebAssembly.

---

## 6. Demo: NYC Taxi Dataset

The demo uses 1 million NYC taxi rides in Parquet format to illustrate a complete geospatial workflow.

### Step 1 — Load and Inspect

```python
import duckdb

duckdb.sql("INSTALL spatial; LOAD spatial;")

# Scan parquet file as a relation (lazy)
rides = duckdb.read_parquet("nyc_taxi.parquet")

# Inspect schema
duckdb.sql("SUMMARIZE rides").show()
# → Columns of interest: pickup_longitude, pickup_latitude, trip_distance
```

### Step 2 — Create Geometry Columns

Convert raw lat/lon columns to geometry using `ST_Point`, then reproject from WGS84 (EPSG:4326) to a local NYC CRS (EPSG:102718, in feet) using `ST_Transform`:

```python
from duckdb import FunctionExpression, ColumnExpression, ConstantExpression

# Helper functions returning DuckDB expressions
def make_point(lat_col, lon_col):
    return FunctionExpression("ST_Point",
        ColumnExpression(lon_col),
        ColumnExpression(lat_col)
    )

def transform(geom_expr, src_crs, dst_crs):
    return FunctionExpression("ST_Transform",
        geom_expr,
        ConstantExpression(src_crs),
        ConstantExpression(dst_crs)
    )

rides = rides.select(
    "*",
    transform(make_point("pickup_latitude", "pickup_longitude"),
              "EPSG:4326", "EPSG:102718").alias("pickup_geom"),
    transform(make_point("dropoff_latitude", "dropoff_longitude"),
              "EPSG:4326", "EPSG:102718").alias("dropoff_geom")
)
```

> This demonstrates the **Relational API expression builder**: compose queries programmatically without raw SQL strings, while still benefiting from DuckDB's full query optimizer.

### Step 3 — Spatial Data Cleaning

Use `ST_Distance` to detect impossible rides (aerial distance > reported trip distance):

```python
# Distance in feet → divide by 5280 for miles
dist_expr = FunctionExpression("ST_Distance",
    ColumnExpression("pickup_geom"),
    ColumnExpression("dropoff_geom")
) / 5280

rides = rides.select("*", dist_expr.alias("aerial_distance_mi"))

# Count suspicious rides
rides.filter("trip_distance < aerial_distance_mi").count().show()
# → 65,000 out of 1,000,000 rides (6.5% — very dirty dataset)

# Filter them out
clean_rides = rides.filter("trip_distance >= aerial_distance_mi")
```

### Step 4 — Read Shapefiles and Spatial Join

List available GDAL drivers and read NYC taxi zone shapefiles:

```python
# List GDAL drivers
duckdb.sql("SELECT * FROM ST_Drivers()").show()

# Read shapefile (calls GDAL internally)
zones = duckdb.sql("SELECT * FROM ST_Read('taxi_zones.shp')")

# Spatial join: assign each ride to its dropoff zone
result = clean_rides.join(
    zones,
    "ST_Within(dropoff_geom, zones.geometry)"
).aggregate(
    "zone_name, COUNT(*) AS trip_count, zones.geometry",
    "zone_name, zones.geometry"
).order("trip_count DESC")
```

### Step 5 — Visualize with GeoPandas

```python
# Convert geometry to WKT for GeoPandas compatibility
result_wkt = result.select(
    "zone_name",
    "trip_count",
    "ST_AsText(geometry).alias('geometry_wkt')"
)

# To GeoPandas
import geopandas as gpd
from shapely import wkt

df = result_wkt.to_df()
df["geometry"] = df["geometry_wkt"].apply(wkt.loads)
gdf = gpd.GeoDataFrame(df, geometry="geometry")
gdf.plot(column="trip_count", legend=True)
```

> **Note:** For a dataset of this size (1M rows, fits in RAM), GeoPandas alone would be comparably fast. DuckDB Spatial's advantage becomes evident with larger datasets, complex multi-join queries, or when data doesn't fit in memory.

---

## 7. Future Work (Roadmap at Time of Talk)

| Feature | Status / Notes |
|---|---|
| **Spatial indexes** | Planned — major upcoming feature |
| **Better projection handling** | Users currently juggle CRS info manually; automatic propagation planned |
| **More ST_ functions** | Ongoing |
| **Improved documentation** | New documentation system underway at DuckDB Labs |
| **GeoArrow integration** | Would enable native zero-copy exchange with GeoPandas (instead of WKT roundtrip) |
| **Spatial expressions in Python API** | Common spatial expressions exposed as Python objects, not just SQL strings |
| **Raster support** | Third-party contribution exists (via GDAL); under consideration for merge, but challenging due to memory pressure in vectorized execution (248 rasters × 512×512 × 4 bands ≈ 2 GB per vector batch) |

---

## 8. Related Projects

### QuackOSM
A tool by Camille Rochette (Wrocław University) for working with **OpenStreetMap data** using DuckDB:
- Automatic OSM data download and filtering by bounding box
- Export to GeoParquet
- Available as both CLI and Python module
- Very fast

### IBIS
A universal interface to databases and dataframes (by Voltron Labs). Supports DuckDB generally, with added DuckDB Spatial expression support contributed by Noel Mani. Provides a more dataframe-like API for spatial operations if the relational API feels too SQL-heavy.

### Spatial Data Management Course
A free online course by Prof. Krishanu Sankar (University of Tennessee), GEOG 414 — covering Python, GeoPandas, DuckDB, and PostGIS. Includes a web book, YouTube videos, and lab exercises.

---

## 9. Q&A Highlights

**Q: Can you use N-dimensional arrays (raster data) with DuckDB?**

A: A third-party contribution added GDAL-based raster support as a work in progress. The challenge is fundamental: DuckDB's vectorized model keeps 248 elements in memory simultaneously. For rasters (e.g., 512×512, 4 bands), a single vector batch ≈ 2 GB. May eventually be supported as an opt-in, use-at-your-own-risk feature.

**Q: Do you support 3D geometries?**

A: Yes — added as a major feature. Supports Z, M, and ZM coordinate dimensions, including intersection and all standard geometric operations, following PostGIS behaviour.

---

## Key Takeaways

| Topic | Summary |
|---|---|
| **Architecture** | In-process, vectorized, multi-threaded, columnar storage — no server, no config |
| **Spatial extension** | PostGIS-compatible, 100+ ST_ functions, GDAL + PROJ bundled, 3000+ CRS built-in |
| **Python workflow** | Lazy relational API → compose queries as expressions → zero-copy to/from Pandas/Polars/Arrow |
| **Data cleaning** | `ST_Distance` for validating trip distances against aerial distance |
| **Spatial joins** | `ST_Within`, `ST_Intersects` etc. work directly in SQL or relational API |
| **Visualization** | Convert geometry to WKT → GeoPandas → plot (native GeoArrow integration coming) |
| **Sweet spot** | Large datasets that don't fit in memory, complex multi-table spatial queries, local analytics without infrastructure |
| **Limitation** | Raster support experimental; visualization requires external libraries |
