---
title: "Geocomputation with Python"
type: note
topic: data-platform
created: 2026-04-04
tags:
  - python
  - gis
  - geocomputation
  - geopandas
  - rasterio
  - reference
source: https://py.geocompx.org/
authors:
  - Michael Dorman
  - Anita Graser
  - Jakub Nowosad
  - Robin Lovelace
---

# Geocomputation with Python

*Dorman, M., Graser, A., Nowosad, J., & Lovelace, R. (2025). Geocomputation with Python. CRC Press.*

Source: https://py.geocompx.org/ | GitHub: https://github.com/geocompx/geocompy

---

## Table of Contents

- Welcome
- Preface
- 1. Geographic data in Python
- 2. Attribute data operations
- 3. Spatial data operations
- 4. Geometry operations
- 5. Raster-vector interactions
- 6. Reprojecting geographic data
- 7. Geographic data I/O
- 8. Making maps with Python
- References

---

## Welcome

This is the online home of *Geocomputation with Python*, a book on reproducible geographic data analysis with open source software. Published by Chapman & Hall/CRC in their Python Series.

Following the Free and Open Source Software for Geospatial (FOSS4G) movement, this is an open source book. The project code is hosted on GitHub, ensuring the content remains reproducible, transparent, and accessible. The community can contribute by opening issues, making typo corrections, or submitting improvements.

The book's website is built automatically using GitHub Actions, which runs the code with each change to verify correctness and reproducibility. Users can execute the code using GitHub CodeSpaces (requires a GitHub account).

### Citation

> Dorman, M., Graser, A., Nowosad, J., & Lovelace, R. (2025). *Geocomputation with Python*. CRC Press.

---

## Preface

*Geocomputation with Python* is an introductory resource for working with geographic data using Python. The book provides cohesive coverage of both vector and raster geographic data models with a consistent learning curve.

### Key Features

1. Mastering fundamental operations
2. Integrating vector and raster dataset operations
3. Clear explanation of every code line to prevent confusion
4. Practical example datasets demonstrating real-world geographic research applications

### How It Differs from Related Resources

| Resource | Difference |
|---|---|
| *Learning Geospatial Analysis with Python* / *Geoprocessing with Python* | Rely on low-level GDAL interfaces requiring more code |
| *Introduction to Python for Geographic Data Analysis* | Covers broader GIS topics; Geocompy has narrower scope but equal raster/vector emphasis |
| *Geographic Data Science with Python* | Covers advanced topics earlier in the sequence |
| *Python for Geospatial Data Analysis* | Addresses automation of proprietary software; Geocompy focuses on open-source packages |

This book is a sister project to *Geocomputation with R*, sharing structure and theoretical foundations while serving the Python community.

### Prerequisites

- Python language familiarity
- Ability to run Python code and install packages
- Knowledge of `numpy` and `pandas`
- Understanding of geographic concepts (coordinate systems, projections, file formats)

### Software Versions

**Python:** 3.11.4

| Package | Version |
|---|---|
| numpy | 2.0.1 |
| pandas | 2.2.2 |
| geopandas | 1.0.1 |
| rasterio | 1.3.10 |
| shapely | 2.0.5 |
| matplotlib | 3.9.0 |

### Acknowledgements

The book acknowledges contributions from the Python community, package developers (numpy, pandas, shapely, geopandas, rasterio), and GitHub contributors including Will Deakin, Sean Gillies, Josh Cole, and Jt Miclat.

---

## 1 Geographic Data in Python

### Overview

This chapter introduces two fundamental geographic data models — vector and raster — and demonstrates their implementation in Python. The vector model represents features using points, lines, and polygons, while the raster model divides space into regular grid cells.

### 1.1 Vector Data

#### Core Classes

Vector geographic data in Python relies on three hierarchical classes:

- **GeoDataFrame**: Represents vector layers with geometry columns
- **GeoSeries**: Represents geometry columns within GeoDataFrames
- **Shapely geometries**: Individual geometry objects (points, lines, polygons, etc.)

The **geopandas** package provides the primary interface for vector data:

```python
import geopandas as gpd
import shapely
import pandas as pd

gdf = gpd.read_file('data/world.gpkg')
```

#### Geometry Types

The Simple Features standard defines seven common geometry types:

| Type | Description |
|---|---|
| POINT | Single coordinate location |
| LINESTRING | Connected sequence of points |
| POLYGON | Closed ring of points forming an area |
| MULTIPOINT | Multiple discrete points |
| MULTILINESTRING | Multiple line sequences |
| MULTIPOLYGON | Multiple polygon areas |
| GEOMETRYCOLLECTION | Mixed geometry types |

```python
point = shapely.Point([5, 2])
linestring = shapely.LineString([(1,5), (4,4), (4,1), (2,2)])
polygon = shapely.Polygon([(1,5), (2,2), (4,1), (4,4), (1,5)])
```

#### Creating Vector Layers from Scratch

```python
lnd_point = shapely.Point(0.1, 51.5)
lnd_geom = gpd.GeoSeries([lnd_point], crs=4326)
lnd_data = {
  'name': ['London'],
  'temperature': [25],
  'geometry': lnd_geom
}
lnd_layer = gpd.GeoDataFrame(lnd_data)
```

#### Geometry Properties

```python
linestring.length   # Returns numeric value
polygon.area        # Returns area in CRS units
gdf.envelope        # Returns bounding boxes
```

> **Important:** Meaningful area and length calculations require projected CRS (typically in meters), not geographic CRS (in degrees).

### 1.2 Raster Data

Rasters consist of two components:

1. **Metadata**: Transform matrix (origin, resolution), CRS, dimensions
2. **Values**: Numpy array with cell values

```python
import rasterio
import numpy as np

src = rasterio.open('data/srtm.tif')
data = src.read(1)  # Read first band
```

Access metadata via `.meta` property (driver, data type, dimensions, CRS, affine transform).

#### Creating Rasters from Scratch

```python
elev = np.arange(1, 37).reshape(6, 6)
new_transform = rasterio.transform.from_origin(
    west=-1.5, north=1.5, xsize=0.5, ysize=0.5
)

new_dataset = rasterio.open(
    'output/elev.tif', 'w',
    driver='GTiff',
    height=elev.shape[0],
    width=elev.shape[1],
    count=1,
    dtype=elev.dtype,
    crs=4326,
    transform=new_transform
)
new_dataset.write(elev, 1)
new_dataset.close()
```

### 1.3 Coordinate Reference Systems

#### Geographic CRS

Use longitude and latitude to identify locations on Earth's surface. Reference an ellipsoidal surface adjusted by a datum (e.g. WGS84 — geocentric).

#### Projected CRS

Convert Earth's 3D surface to 2D Cartesian coordinates (Easting/Northing), typically in meters. All projections introduce distortions, preserving different properties:

- **Conformal**: Preserves local shape
- **Equal-area**: Preserves area
- **Equidistant**: Preserves distance
- **Azimuthal**: Preserves direction

```python
gdf.crs              # Query CRS
zion.to_crs(4326)    # Reproject to WGS84

import pyproj
pyproj.CRS.from_epsg(4326)
```

### 1.4 Key Packages

| Package | Purpose |
|---|---|
| geopandas | Vector layer operations |
| shapely | Individual geometry operations |
| rasterio | Raster data I/O and metadata |
| pyproj | CRS management |
| numpy | Array operations for raster data |

---

## 2 Attribute Data Operations

### Prerequisites

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import rasterio

world = gpd.read_file('data/world.gpkg')
src_elev = rasterio.open('output/elev.tif')
```

### 2.1 Vector Attribute Manipulation

#### Subsetting

```python
world.iloc[0:3, :]              # Position-based: first 3 rows
world.iloc[:, 0:3]              # First 3 columns
world[['name_long', 'geometry']]  # Name-based
world.loc[:, 'name_long':'pop']   # Column slice
world.drop([2, 3, 5])             # Drop rows
world.drop(['name_long', 'continent'], axis=1)  # Drop columns
world[['name_long', 'pop']].rename(columns={'pop': 'population'})
```

#### Boolean Subsetting

| Symbol | Meaning |
|---|---|
| `==` | Equal to |
| `!=` | Not equal to |
| `>`, `<` | Greater/Less than |
| `>=`, `<=` | Greater/Less than or equal |
| `&`, `\|`, `~` | Logical: And, Or, Not |

```python
small_countries = world[world['area_km2'] < 10000]
idx_asia = world['continent'] == 'Asia'
world.loc[idx_small & idx_asia, ['name_long', 'continent', 'area_km2']]
world[world['continent'].isin(['North America', 'South America'])]
```

#### Aggregation

```python
# Without geometry
world_agg1 = world.groupby('continent')[['pop']].sum().reset_index()

# With geometry using dissolve
world_agg2 = world[['continent', 'pop', 'geometry']] \
    .dissolve(by='continent', aggfunc='sum').reset_index()

# Multiple functions
world_agg3 = world.dissolve(
    by='continent',
    aggfunc={'name_long': 'count', 'pop': 'sum', 'area_km2': 'sum'}
).rename(columns={'name_long': 'n'}).reset_index()
```

Available functions: `'first'`, `'last'`, `'min'`, `'max'`, `'sum'`, `'mean'`, `'median'`.

#### Joining

```python
coffee_data = pd.read_csv('data/coffee_data.csv')
world_coffee = pd.merge(world, coffee_data, on='name_long', how='left')
```

Join types: **left** (keeps all from first, `NaN` for unmatched), **inner** (only matching rows).

#### Creating and Removing Attributes

```python
world2['pop_dens'] = world2['pop'] / world2['area_km2']  # New column
world2['con_reg'] = world['continent'] + ':' + world2['region_un']  # String concat
world2[['continent', 'region_un']] = world2['con_reg'].str.split(':', expand=True)
world2 = pd.DataFrame(world2.drop('geom', axis=1))  # Remove geometry
```

### 2.2 Raster Attribute Manipulation

#### Subsetting

```python
elev = src_elev.read(1)    # Single band → 2D array
elev[1, 2]                  # Single cell
elev[1, 2] = 0              # Modify cell
elev3d = src_elev.read()   # All bands → 3D array (layers, rows, cols)
elev3d[0, 1, 2]             # Three-index access
```

#### Summarizing

```python
np.mean(elev)
np.nanmean(elev)                        # Ignores NaN
freq = np.unique(grain, return_counts=True)
plt.hist(elev.flatten())               # Histogram
```

---

## 3 Spatial Data Operations

### Prerequisites

```python
import scipy.ndimage, scipy.stats
import shapely, geopandas as gpd
import rasterio, rasterio.merge, rasterio.features

nz = gpd.read_file('data/nz.gpkg')
nz_height = gpd.read_file('data/nz_height.gpkg')
world = gpd.read_file('data/world.gpkg')
```

### 3.1 Spatial Operations on Vector Data

#### Spatial Subsetting

```python
canterbury = nz[nz['Name'] == 'Canterbury']
sel = nz_height.intersects(canterbury.geometry.iloc[0])
canterbury_height = nz_height[sel]

# Disjoint (non-overlapping)
sel = nz_height.disjoint(canterbury.geometry.iloc[0])

# Multiple geometries
sel = nz_height.intersects(canterbury_southland.union_all())
```

#### Topological Relations

| Method | Description |
|---|---|
| `.intersects()` | Features touch, cross, or are within |
| `.disjoint()` | Features don't relate spatially |
| `.within()` | Feature is completely inside another |
| `.touches()` | Shares boundary without overlapping |
| `.contains()` | Feature completely encloses another |
| `.crosses()` | Features intersect in a crossing pattern |
| `.overlaps()` | Features partially overlap |

```python
points.intersects(poly.iloc[0])   # Boolean Series
points.within(poly.iloc[0])
points.distance(poly.iloc[0]) < 0.2  # Distance-based
```

#### Spatial Joining

```python
np.random.seed(11)
bb = world.total_bounds
x = np.random.uniform(low=bb[0], high=bb[2], size=10)
y = np.random.uniform(low=bb[1], high=bb[3], size=10)
random_points = gpd.GeoDataFrame({'geometry': gpd.points_from_xy(x, y, crs=4326)})
random_joined = random_points.sjoin(world, how='left')
```

#### Non-Overlapping Joins

```python
crs = 27700
cycle_hire_buffers = cycle_hire.copy().to_crs(crs)
cycle_hire_buffers.geometry = cycle_hire_buffers.buffer(20)
cycle_hire_buffers = gpd.sjoin(cycle_hire_buffers, cycle_hire_osm.to_crs(crs), how='left')
# Aggregate duplicates
cycle_hire_buffers = cycle_hire_buffers[['id','capacity','geometry']] \
    .dissolve(by='id', aggfunc='mean').reset_index()
```

#### Spatial Aggregation

```python
nz_height2 = gpd.sjoin(nz_height[['elevation','geometry']], nz[['Name','geometry']], how='left')
nz_height2 = nz_height2.groupby('Name')[['elevation']].mean().reset_index()
nz2 = pd.merge(nz[['Name','geometry']], nz_height2, on='Name', how='left')
```

#### Area-Weighted Interpolation (Incongruent Layers)

1. Calculate original areas: `nz['area'] = nz.area`
2. Create intersections: `nz_grid = nz.overlay(grid)`
3. Calculate intersection areas: `nz_grid['area_sub'] = nz_grid.area`
4. Compute area proportions: `nz_grid['area_prop'] = nz_grid['area_sub'] / nz_grid['area']`
5. Calculate weighted values: `nz_grid['population'] = nz_grid['Population'] * nz_grid['area_prop']`

For *extensive* variables (counts): sum the weighted parts. For *intensive* variables (density): compute weighted means.

#### Distance Relations

```python
nz_highest = nz_height.sort_values(by='elevation', ascending=False).iloc[:3, :]
canterbury_centroid = canterbury.centroid.iloc[0]
nz_highest.distance(canterbury_centroid)
```

### 3.2 Spatial Operations on Raster Data

#### Spatial Subsetting

```python
list(src_elev.sample([(0.1, 0.1)]))   # Extract at coordinates

# Boolean masking
masked_elev = elev.copy().astype('float64')
masked_elev[mask] = np.nan

# Condition-based
elev2 = elev.copy().astype('float64')
elev2[elev2 < 20] = np.nan
```

#### Map Algebra

Four operation types:

| Type | Description |
|---|---|
| Local | Per-cell operations |
| Focal | Neighborhood operations |
| Zonal | Operations on irregular zones |
| Global | Per-raster operations |

**Local operations:**
```python
elev + elev
elev.astype(int)**2
np.log(elev)
elev > 5

# Reclassification
recl = elev.copy()
recl[(elev > 0)  & (elev <= 12)] = 1
recl[(elev > 12) & (elev <= 24)] = 2
recl[(elev > 24) & (elev <= 36)] = 3

# NDVI = (NIR - Red) / (NIR + Red)
landsat = src_landsat.read()
ndvi = (landsat[3] - landsat[2]) / (landsat[3] + landsat[2])
```

**Focal operations (3×3 window):**
```python
import scipy.ndimage

elev_min    = scipy.ndimage.minimum_filter(elev, size=3)
elev_max    = scipy.ndimage.maximum_filter(elev, size=3)
elev_mean   = scipy.ndimage.uniform_filter(elev, size=3)
elev_median = scipy.ndimage.median_filter(elev, size=3)

# Mode (categorical)
grain_mode = scipy.ndimage.generic_filter(
    grain,
    lambda x: scipy.stats.mode(x.flatten())[0],
    size=3
)
```

**Terrain metrics** (slope, aspect) via GDAL:
```python
os.system('gdaldem slope input.tif output_slope.tif')
os.system('gdaldem aspect input.tif output_aspect.tif')
```

**Zonal operations:**
```python
z = {i: elev[grain == i].mean().round(1) for i in np.unique(grain)}
```

#### Merging Rasters

```python
src_1 = rasterio.open('data/aut.tif')
src_2 = rasterio.open('data/ch.tif')
out_image, out_transform = rasterio.merge.merge([src_1, src_2])
# Methods: 'first' (default), 'last', 'min', 'max'
```

#### Raster vs. Vector Equivalents

| Raster Operation | Vector Equivalent |
|---|---|
| Distance raster with max distance | Buffer |
| Reclassification | Dissolve |
| Overlay with mask | Clipping |
| Zonal aggregation | Spatial aggregation |

---

## 4 Geometry Operations

### 4.1 Geometric Operations on Vector Data

#### Simplification

The Douglas-Peucker algorithm reduces vertex counts using a tolerance in map units:

```python
seine_simp = seine.simplify(2000)

# Topology-aware (topojson)
import topojson as tp
topo = tp.Topology(us_states9311, prequantize=False)
us_states_simp2 = topo.toposimplify(100000).to_gdf()
```

#### Centroids

```python
gdf.centroid                  # Center of mass (may fall outside polygon)
gdf.representative_point()    # Guaranteed to be inside the polygon
```

#### Buffers

```python
seine_buff_5km = seine.buffer(5000)          # Returns GeoSeries
seine_buff = seine.copy()
seine_buff.geometry = seine.buffer(5000)     # Replace geometry column
```

#### Affine Transformations

```python
gdf.translate(xoff=0, yoff=100000)
gdf.scale(xfact=0.5, yfact=0.5, origin='centroid')
gdf.rotate(angle=90, origin='centroid')
gdf.affine_transform([a, b, d, e, xoff, yoff])  # Custom 6-parameter transform
```

#### Pairwise Geometry Operations

```python
geom_a.intersection(geom_b)           # Overlapping area
geom_a.difference(geom_b)             # A minus B
geom_a.union(geom_b)                  # Combined area
geom_a.symmetric_difference(geom_b)   # Either but not both
```

#### Geometry Unions

```python
regions = us_states[['REGION', 'geometry', 'total_pop_15']] \
    .dissolve(by='REGION', aggfunc='sum').reset_index()
```

#### Type Transformations

```python
# Shapely-level
shapely.LineString(multipoint.geoms)    # MultiPoint → LineString
shapely.Polygon(multipoint.geoms)       # MultiPoint → Polygon
shapely.MultiPoint(linestring.coords)   # LineString → MultiPoint

# GeoDataFrame-level
gdf.explode(index_parts=True)           # Multi-part → single-part
gdf.dissolve()                          # Single-part → multi-part
```

### 4.2 Geometric Operations on Raster Data

#### Extent and Origin

```python
r_pad = np.pad(r, ((rows, rows), (cols, cols)), constant_values=18)
xmin_new = xmin - dx * cols
ymax_new = ymax - dy * rows
new_transform = rasterio.transform.from_origin(west=xmin_new, north=ymax_new,
                                               xsize=dx, ysize=abs(dy))
```

#### Aggregation and Disaggregation

```python
# Aggregation (factor < 1, e.g. 0.2 = 5x coarser)
factor = 0.2
r = src.read(1, out_shape=(int(src.height * factor), int(src.width * factor)),
             resampling=rasterio.enums.Resampling.average)
new_transform = src.transform * src.transform.scale(
    (src.width / r.shape[1]), (src.height / r.shape[0])
)
```

#### Resampling

```python
rasterio.warp.reproject(
    source=rasterio.band(src, 1),
    destination=rasterio.band(dst, 1),
    src_transform=src.transform, src_crs=src.crs,
    dst_transform=dst_transform, dst_crs=src.crs,
    resampling=rasterio.enums.Resampling.nearest
)
```

Resampling methods:
- `nearest`: Categorical rasters
- `bilinear` / `cubic` / `lanczos`: Continuous rasters (increasing smoothness)
- `average` / `min` / `max` / `median` / `mode` / `sum`: Summary methods

---

## 5 Raster-Vector Interactions

### 5.1 Introduction

Three main techniques:

1. Raster cropping and masking using vector objects
2. Extracting raster values using different vector types
3. Raster-vector conversion (rasterization and vectorization)

### 5.2 Raster Masking and Cropping

```python
import rasterio.mask

# Masking only (pixels outside boundary → NoData)
out_image, out_transform = rasterio.mask.mask(src, shapes, crop=False)

# Cropping + masking (reduces extent)
out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
```

Requirements: matching projections, valid NoData value, updated metadata when writing.

### 5.3 Raster Extraction

#### Extraction to Points

```python
import rasterstats

rasterstats.point_query(points, raster_path, interpolate='nearest')
rasterstats.point_query(points, raster_path, interpolate='bilinear')
```

#### Extraction to Lines (Elevation Profile)

1. Project line to projected CRS
2. Create equally-spaced points: `line.interpolate(distance)`
3. Extract values at each point using point extraction

#### Extraction to Polygons

```python
rasterstats.zonal_stats(polygons, raster_path, stats=['mean', 'min', 'max', 'count', 'median'])
np.unique(raster_array, return_counts=True)  # Categorical rasters
```

### 5.4 Rasterization

```python
import rasterio.features

# Presence/absence
out = rasterio.features.rasterize(
    [(geom, 1) for geom in geometries],
    out_shape=template.shape,
    transform=template.transform
)

# Summing values in overlapping cells
out = rasterio.features.rasterize(
    [(geom, value) for geom, value in zip(geometries, values)],
    out_shape=template.shape,
    transform=template.transform,
    merge_alg=rasterio.enums.MergeAlg.add
)
```

Options: `all_touched=True` (all intersecting cells) or `False` (centroids/Bresenham).

### 5.5 Spatial Vectorization

#### Raster to Polygons

```python
shapes = list(rasterio.features.shapes(raster_array, transform=src.transform))
geometries = [shapely.geometry.shape(s[0]) for s in shapes]
values = [s[1] for s in shapes]
gdf = gpd.GeoDataFrame({'geometry': geometries, 'value': values}, crs=src.crs)
```

#### Raster to Points

```python
rows, cols = np.meshgrid(np.arange(src.height), np.arange(src.width), indexing='ij')
xs, ys = rasterio.transform.xy(src.transform, rows.flatten(), cols.flatten())
gdf = gpd.GeoDataFrame({'geometry': gpd.points_from_xy(xs, ys), 'value': values})
```

#### Raster to Contours

```bash
gdal_contour -a elev dem.tif contours.gpkg -i 50.0
```

### 5.6 Distance to Nearest Geometry

Combines multiple concepts:
1. Extract boundary from dissolved polygon
2. Aggregate raster to coarser resolution
3. Convert pixels to point geometries (exclude NaN)
4. Calculate distances using `.distance()`
5. Rasterize distances back to grid

---

## 6 Reprojecting Geographic Data

### 6.1 Coordinate Reference Systems

CRSs can be described as:
- Simple statements: "lon/lat coordinates"
- Proj-strings (outdated): `+proj=longlat +ellps=WGS84 +datum=WGS84`
- **Authority:Code** (recommended): `EPSG:4326`
- WKT (unambiguous): full specification — "when WKT values conflict with identifier attributes, the WKT values shall prevail"

#### Querying and Setting CRS

```python
# Vector
world.crs
world.crs.is_geographic
world.crs.axis_info[0].unit_name
world.crs.to_authority()
world.set_crs(4326)
world.set_crs(3857, allow_override=True)

# Raster
src_nlcd.crs
```

> **Important:** `.set_crs()` only updates metadata — it does **not** transform coordinates.

### 6.2 When to Reproject

- Publishing data online (geographic CRS typically required)
- Comparing or combining objects with different CRSs
- Performing geometric calculations (projected CRS required)

### 6.3 Selecting an Appropriate CRS

**Geographic CRS:** WGS84 (`EPSG:4326`) — standard for web mapping and GPS.

**UTM zones:** Divides Earth into 60 longitude zones. Conformal but distorts with distance from zone center. Restrict to 6° from central meridian.

```python
def lonlat2UTM(lon, lat):
    utm = (math.floor((lon + 180) / 6) % 60) + 1
    utm += 32600 if lat > 0 else 32700
    return utm
```

**Custom projections:**

| Projection | Use case |
|---|---|
| LAEA (Lambert Azimuthal Equal-Area) | Equal-area preservation |
| AEQD (Azimuthal Equidistant) | Accurate straight-line distances from center |
| LCC (Lambert Conformal Conic) | Regions spanning thousands of km |
| STERE (Stereographic) | Polar regions |

### 6.4 Reprojecting Vector Data

```python
lnd_layer2 = lnd_layer.to_crs(27700)
cycle_hire_osm_projected = cycle_hire_osm.to_crs(27700)
```

### 6.5 Reprojecting Raster Data

```python
dst_transform, dst_width, dst_height = rasterio.warp.calculate_default_transform(
    src_nlcd.crs, dst_crs,
    src_nlcd.width, src_nlcd.height,
    *src_nlcd.bounds
)

dst_kwargs = src_nlcd.meta.copy()
dst_kwargs.update({'crs': dst_crs, 'transform': dst_transform,
                   'width': dst_width, 'height': dst_height})

dst_nlcd = rasterio.open('output/nlcd_4326.tif', 'w', **dst_kwargs)
rasterio.warp.reproject(
    source=rasterio.band(src_nlcd, 1),
    destination=rasterio.band(dst_nlcd, 1),
    src_transform=src_nlcd.transform, src_crs=src_nlcd.crs,
    dst_transform=dst_transform, dst_crs=dst_crs,
    resampling=rasterio.enums.Resampling.nearest
)
dst_nlcd.close()
```

Resampling methods: `nearest` (categorical), `bilinear` (continuous), `average`/`mode` (coarser destination).

### 6.6 Custom Map Projections

**WKT-based custom CRS:**
```python
lon, lat = zion.to_crs(4326).union_all().centroid.coords[0]
my_wkt = f'''PROJCS["Custom_AEQD",
 GEOGCS["GCS_WGS_1984",
  DATUM["WGS_1984", SPHEROID["WGS_1984",6378137.0,298.257223563]],
  PRIMEM["Greenwich",0.0],
  UNIT["Degree",0.0174532925199433]],
 PROJECTION["Azimuthal_Equidistant"],
 PARAMETER["Central_Meridian",{lon}],
 PARAMETER["Latitude_Of_Origin",{lat}],
 UNIT["Meter",1.0]]'''
zion_aeqd = zion.to_crs(my_wkt)
```

**Proj-string projections:**
```python
world.to_crs('+proj=moll').plot()         # Mollweide (equal-area)
world.to_crs('+proj=wintri').plot()        # Winkel tripel (minimal distortion)
world.to_crs('+proj=laea +x_0=0 +y_0=0 +lon_0=-74 +lat_0=40').plot()  # LAEA
```

---

## 7 Geographic Data I/O

### 7.1 Introduction

Geographic data I/O involves reading data into Python and writing processed results to files or databases. "Mistakes made at the outset of projects can lead to large problems later down the line."

### 7.2 Retrieving Open Data

Key data sources:
- GEOSS portal and Copernicus Data Space Ecosystem (raster)
- SEDAC portal (NASA), INSPIRE geoportal (vector)
- EarthExplorer, NASA EarthData Search

```python
import urllib.request, zipfile

url = 'https://naciscdn.org/naturalearth/10m/cultural/ne_10m_airports.zip'
urllib.request.urlretrieve(url, 'output/ne_10m_airports.zip')
zipfile.ZipFile('output/ne_10m_airports.zip', 'r').extractall('output')
```

### 7.3 Geographic Data Packages

```python
# cartopy — Natural Earth data
import cartopy
filename = cartopy.io.shapereader.natural_earth(
    resolution='10m', category='cultural', name='admin_2_counties'
)
counties = gpd.read_file(filename)

# osmnx — OpenStreetMap
import osmnx as ox
parks = ox.features.features_from_place(query='leeds uk', tags={'leisure': 'park'})

# Geocoding
result = gpd.tools.geocode('54 Frith St, London W1D 4SJ, UK', timeout=10)
```

### 7.4 File Formats

GDAL provides unified access to 200+ vector and raster formats.

| Format | Type | Notes |
|---|---|---|
| ESRI Shapefile (.shp) | Vector | Partially open; 2GB limit, 255 cols, 10-char names |
| GeoJSON (.geojson) | Vector | Open; good for web |
| GeoPackage (.gpkg) | Vector/Raster | Open; modern Shapefile replacement |
| GeoTIFF (.tif) | Raster | Open; widely supported |
| Cloud Optimized GeoTIFF (COG) | Raster | Partial reads via HTTP |
| KML (.kml) | Vector | Open; Google-based |

### 7.5 Data Input

#### Vector

```python
gdf = gpd.read_file('data/world.gpkg')

# WHERE filtering
tanzania = gpd.read_file('data/world.gpkg', where='name_long="Tanzania"')

# Spatial filtering
tanzania_buf = tanzania.to_crs(32736).buffer(50000).to_crs(4326)
tanzania_neigh = gpd.read_file('data/world.gpkg', mask=tanzania_buf)

# CSV with coordinates
cycle_hire = pd.read_csv('data/cycle_hire_xy.csv')
geom = gpd.points_from_xy(cycle_hire['X'], cycle_hire['Y'], crs=4326)
cycle_hire_xy = gpd.GeoDataFrame(data=cycle_hire, geometry=geom)

# WKT
world_wkt['geometry'] = gpd.GeoSeries.from_wkt(world_wkt['WKT'])

# Remote
gpd.read_file("zip+https://github.com/.../coutwildrnp.zip")
```

#### Raster

```python
src = rasterio.open('data/srtm.tif')

# Windowed reading (large/remote files)
w = rasterio.windows.from_bounds(left=xmin, bottom=ymin, right=xmax, top=ymax,
                                  transform=src.transform)
r = src.read(1, window=w)

# Point sampling
values = src.sample([(-21.94, 64.15)])
```

### 7.6 Data Output

#### Vector

```python
world.to_file('output/world.gpkg')              # Write
world.to_file('output/file.gpkg', mode='a')     # Append
world.to_file('output/file.gpkg', layer='name') # Named layer
```

#### Raster

```python
dst = rasterio.open(
    'output/r.tif', 'w',
    driver='GTiff', height=r.shape[0], width=r.shape[1],
    count=1, dtype=r.dtype, crs=4326, transform=new_transform
)
dst.write(r, 1)
dst.close()

# Multiband
dst_kwds.update(count=3)
dst = rasterio.open('output/r3.tif', 'w', **dst_kwds)
dst.write(r*1, 1); dst.write(r*2, 2); dst.write(r*3, 3)
dst.close()
```

#### No Data Handling

```python
# Float arrays
r = np.array([1.1, 2.1, np.nan, 4.1]).reshape(2, 2)

# Integer arrays (flag value)
r = np.array([1, 2, -9999, 4]).reshape(2, 2).astype(np.int32)
dst = rasterio.open('output/r.tif', 'w', nodata=-9999, ...)

# Reading back — convert to float
mask = r == src.nodata
r = r.astype(np.float64)
r[mask] = np.nan

# Or use masked arrays
r = src.read(masked=True)
```

---

## 8 Making Maps with Python

### 8.1 Introduction

> "Poorly constructed maps can undermine your audience's ability to comprehend crucial data and diminish the presentation of professional investigations."

The chapter covers **static maps** (`.plot()` / `rasterio.plot.show()`) and **interactive maps** (`.explore()`).

### 8.2 Static Maps

#### Minimal Examples

```python
nz.plot()                      # Vector
rasterio.plot.show(nz_elev)    # Raster
```

#### Styling

```python
nz.plot(color='lightgrey', edgecolor='blue')
nz_height.plot(markersize=100)

fig, ax = plt.subplots(figsize=(4, 4))
nz_height.plot(markersize=100, ax=ax)
```

#### Symbology

```python
nz.plot(column='Median_income', legend=True)
nz.plot(column='Median_income', legend=True, cmap='Reds')
nz.plot(column='Island', legend=True, cmap='Set1')
nz.plot(column='Island', legend=True, cmap='Set1', legend_kwds={'loc': 4})

# Raster with colorbar
fig, ax = plt.subplots()
i = plt.imshow(nz_elev.read(1), cmap='BrBG')
rasterio.plot.show(nz_elev, cmap='BrBG', ax=ax)
fig.colorbar(i, ax=ax)
```

Popular colormaps: `'Reds'`, `'Set1'`, `'plasma'`, `'viridis'`, `'BrBG'`. Append `_r` to reverse.

#### Labels

```python
fig, ax = plt.subplots()
nz.plot(ax=ax, color='lightgrey', edgecolor='grey')
nz.apply(
    lambda x: ax.annotate(text=x['Name'], xy=x.geometry.centroid.coords[0], ha='center'),
    axis=1
)
```

#### Layers

```python
# Method 1
base = nz.plot(color='none')
nz_height.plot(ax=base, color='red')

# Method 2
fig, ax = plt.subplots()
nz.plot(ax=ax, color='none')
nz_height.plot(ax=ax, color='red')

# Raster + vector
fig, ax = plt.subplots(figsize=(5, 5))
rasterio.plot.show(nz_elev, ax=ax)
nz.to_crs(nz_elev.crs).plot(ax=ax, color='none', edgecolor='red')

# Draw order
base = layer1.plot(zorder=1)
layer2.plot(ax=base, zorder=2)
```

#### Basemaps

```python
import contextily as cx

nzw = nz[nz['Name'] == 'Nelson'].to_crs(epsg=3857)
fig, ax = plt.subplots(figsize=(7, 7))
nzw.plot(color='none', ax=ax)
cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik)
cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
```

#### Faceted Maps

```python
vars = ['Land_area', 'Population', 'Median_income', 'Sex_ratio']
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(6, 6))
ax = ax.flatten()
for i in range(len(vars)):
    nz.plot(ax=ax[i], column=vars[i], legend=True)
    ax[i].set_title(vars[i])
    ax[i].xaxis.set_visible(False)
    ax[i].yaxis.set_visible(False)
```

#### Exporting

```python
plt.savefig('output/map.jpg')
plt.savefig('output/map.svg', dpi=300)
# Formats: .jpg, .png, .svg, .pdf
```

### 8.3 Interactive Maps

Based on the Leaflet JavaScript library via **geopandas** `.explore()`.

#### Minimal

```python
nz.explore()
```

#### Styling

```python
nz.explore(color='green', style_kwds={'color':'black', 'opacity':0.3})

# Points
nz_height.explore(
    color='green',
    style_kwds={'color':'black', 'opacity':0.5, 'fillOpacity':0.1},
    marker_kwds={'radius': 20}
)
nz_height.explore(marker_type='marker')
```

`style_kwds` keys: `stroke`, `color`, `weight`, `opacity`, `fill`, `fillColor`, `fillOpacity`

Marker types: `'circle_marker'` (radius in px, default), `'circle'` (radius in m), `'marker'` (PNG icon)

#### Layers

```python
m = nz.explore(name='Polygons (adm. areas)')
nz_height.explore(m=m, color='red', name='Points (elevation)')
folium.LayerControl(collapsed=False).add_to(m)
m
```

#### Symbology

```python
nz.explore(column='Median_income', legend=True, cmap='Reds',
           style_kwds={'color':'black', 'weight': 0.5})
```

#### Basemaps

```python
nz.explore(tiles='OpenStreetMap')
nz.explore(tiles='CartoDB positron')
nz.explore(tiles='CartoDB dark_matter')
```

#### Exporting

```python
m = nz.explore(name='Polygons (adm. areas)')
nz_height.explore(m=m, color='red', name='Points (elevation)')
folium.LayerControl(collapsed=False).add_to(m)
m.save('output/map.html')
```

---

## References

Bivand, Roger. 2021. "Progress in the R Ecosystem for Representing and Handling Spatial Data." *Journal of Geographical Systems* 23 (4): 515–46.

Bivand, Roger, Edzer Pebesma, and Virgilio Gómez-Rubio. 2013. *Applied Spatial Data Analysis with R*. Springer.

Boeing, Geoff. 2017. "OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks." *Computers, Environment and Urban Systems* 65: 126–39.

Bossche, Joris Van den, et al. 2023. "Geopandas/Geopandas: V0.14.0." Zenodo.

Brewer, Cynthia A. 2015. *Designing Better Maps: A Guide for GIS Users*. Second. Esri Press.

Burrough, P. A., Rachael McDonnell, and Christopher D. Lloyd. 2015. *Principles of Geographical Information Systems*. Third. Oxford University Press.

Douglas, David H, and Thomas K Peucker. 1973. "Algorithms for the Reduction of the Number of Points Required to Represent a Digitized Line or Its Caricature." *Cartographica* 10 (2): 112–22.

Gillies, Sean et al. 2007–. "Shapely: Manipulation and Analysis of Geometric Objects." GitHub.

Harris, Charles R., et al. 2020. "Array Programming with NumPy." *Nature* 585 (7825): 357–62.

Horn, B. K. P. 1981. "Hill Shading and the Reflectance Map." *Proceedings of the IEEE* 69 (1): 14–47.

Hunter, J. D. 2007. "Matplotlib: A 2D Graphics Environment." *Computing in Science & Engineering* 9 (3): 90–95.

Jenny, Bernhard, et al. 2017. "A Guide to Selecting Map Projections for World and Hemisphere Maps." In *Choosing a Map Projection*. Springer.

Lovelace, Robin, Jakub Nowosad, and Jannes Muenchow. 2019. *Geocomputation with R*. CRC Press.

McKinney, Wes. 2010. "Data Structures for Statistical Computing in Python." *SciPy Proceedings*.

Open Geospatial Consortium. 2019. "Well-Known Text Representation of Coordinate Reference Systems." OGC Standard 18-010r7.

Pebesma, Edzer, and Roger Bivand. 2023. *Spatial Data Science: With Applications in R*. CRC Press.

Šavrič, Bojan, Bernhard Jenny, and Helen Jenny. 2016. "Projection Wizard – An Online Map Projection Selection Tool." *The Cartographic Journal* 53 (2): 177–85.

Tennekes, Martijn, and Jakub Nowosad. 2022. *Elegant and Informative Maps with Tmap*.

Tobler, Waldo R. 1979. "Smooth Pycnophylactic Interpolation for Geographical Regions." *JASA* 74 (367): 519–30.

Tomlin, C. Dana. 1990. *Geographic Information Systems and Cartographic Modeling*. Prentice Hall.

Virtanen, Pauli, et al. 2020. "SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python." *Nature Methods* 17: 261–72.

Zevenbergen, Lyle W., and Colin R. Thorne. 1987. "Quantitative Analysis of Land Surface Topography." *Earth Surface Processes and Landforms* 12 (1): 47–56.
