---
title: "Iceberg GEO: Technical Insights and Implementation Strategies"
source: https://wherobots.com/blog/iceberg-geo-technical-insights-and-implementation-strategies/
author:
  - "[[Ben Pruden]]"
published: 14.02.2025
created: 2026-04-04
description: In our previous blog post, we announced Apache Iceberg and Parquet’s support for spatial data types and discussed their significance. Today, we take a closer look at these GEO data types in Iceberg (collectively Iceberg GEO in this blog), exploring design, key features, and implementation considerations.
tags:
  - clippings
  - mapping
topic:
type: note
---
In [our previous blog post](https://wherobots.com/apache-iceberg-and-parquet-now-support-geo/), we announced Apache Iceberg and Parquet’s support for spatial data types and discussed their significance. These enhancements significantly improve the economics of utilizing geospatial data in end solutions. Organizations will be capable of creating higher value, lower cost products, faster over time. Today, we take a closer look at these GEO data types in Iceberg (collectively Iceberg GEO), exploring design, key features, and implementation considerations. We will also demonstrate how to leverage these new Iceberg features with Apache Sedona and Wherobots in an upcoming blog post.

## The Story Behind Iceberg Support for GEO Types

The foundation for Iceberg GEO can be traced back to early 2022 with the launch of the GeoParquet project, which aimed to standardize spatial data exchange across different vendors in the cloud-native and big data ecosystem. This initiative was a crucial first step toward unifying spatial data formats in modern data platforms. Its history, and how GeoParquet will become just Parquet, is described in this [GeoParquet community blog post.](https://cloudnativegeo.org/blog/2025/02/geoparquet-2.0-going-native/)

As interest in spatial data support for lakehouses grew, early design explorations took shape through projects like [GeoLake](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10363173). Wherobots later expanded on these concepts, developing [Havasu](https://github.com/wherobots/havasu/commits/main/) in 2023, a production-ready extension of Iceberg designed to support geometry, geography, and raster data in cloud data lakehouses. Havasu’s geometry encoding was inspired by GeoParquet, while its storage format remained fully Parquet-compatible, inheriting Iceberg’s key features such as ACID transactions, schema evolution, time travel, and data versioning.

Recognizing the value and need to bring native spatial support to Iceberg, the cloud native spatial community ultimately decided that integrating these features directly into Iceberg would be more beneficial than maintaining a separate extension. This direction would ensure that spatial data was well supported by Iceberg without modifications.

In early 2024, the spatial and Iceberg communities formally initiated discussions on adding GEO data type to Iceberg, using Havasu’s design as a reference. The collaboration involved many community members at Wherobots, CARTO, Planet, Apple, Databricks, Snowflake, and others. Through joint efforts and extensive discussions, [the proposal](https://github.com/apache/iceberg/pull/10981) was refined and successfully merged.

## Iceberg GEO Type Definitions and Storage

The Iceberg GEO proposal introduces two spatial data types: geometry and geography. This distinction addresses the varying levels of spatial data processing support across different engines. Some primarily work with geometry, while others emphasize geography. The primary distinction between these types is how edges between points are interpolated. All other aspects of the Iceberg GEO proposal such as encoding, and bounds apply to both unless explicitly stated otherwise.

#### Geometry Type

The geometry type represents spatial objects in a planar space using Cartesian geometry, assuming all calculations, including distance and area measurements, are performed on a flat surface. It is best suited for applications requiring high-precision, local-scale spatial operations, such as urban planning, country-level modeling, and traffic engineering. Geometry uses planar edge interpolation, where edges between vertices are treated as straight lines.

#### Geography Type

The geography type represents spatial objects on the ellipsoidal surface of the Earth, making it more appropriate for global-scale applications such as satellite tracking, aviation navigation, and long-distance routing. Unlike geometry, geography accounts for the Earth’s curvature, ensuring that spatial operations like distance and area calculations reflect real-world geography. It requires non-planar edge interpolation algorithms, which define how edges between points behave on a curved surface.

#### Edge Interpolation Algorithms

Since the Earth is not flat, different interpolation methods impact the accuracy of spatial operations. The community identified six primary interpolation algorithms: Planar, Spherical, Vincenty, Thomas, Andoyer, and Karney. Taking Planar and Spherical as examples, planar interpolation assumes straight-line edges in a Cartesian plane and is used in the Geometry type while spherical interpolation models edges as geodesic curves on a sphere and could be used in the Geography type.

Details of all interpolation methods can be found in [this paper](https://isprs-archives.copernicus.org/articles/XLII-4-W14/45/2019/). The Iceberg Geography type requires implementations to explicitly specify which non-planar interpolation algorithm is used, ensuring consistency in spatial computations across different engines.

#### Encoding

Both Iceberg GEO types follow the [OGC Simple Feature Access v1.2.1 data model](https://www.ogc.org/publications/standard/sfa/), supporting geometric objects such as points, polygons, line strings, and geometry collections. It uses the [ISO Well-Known Binary (WKB)](https://www.iso.org/standard/60343.html) format for encoding, which supports higher-dimensional geometries (Z and M values) but does not include a Spatial Reference Identifier (SRID). A more detailed comparison of WKB variants can be found in the [GEOS library documentation](https://libgeos.org/specifications/wkb/).

To ensure consistency across spatial tools, Iceberg GEO enforces a longitude-latitude (X, Y) coordinate order, aligning with standards used in GeoPandas, Apache Sedona, and Google Maps.

#### Coordinate Reference Systems (CRS)

Both geometry and geography types support CRS definitions using either a SRID (e.g., srid:4326) or a PROJJSON string (e.g., projjson: {…}), which provides a self-contained CRS definition. SRIDs are storage efficient for well-known coordinate systems, while PROJJSON allows detailed CRS specifications. A minor difference between the Geometry and Geography type is that the former allows any CRS, whereas the latter only allows geographic CRS, which only makes sense in the context of non-planar edge interpolation.

#### Lower and Upper Bounds

Iceberg GEO extends Iceberg’s lower and upper bounds statistics for spatial data by defining bounds based on the westernmost, easternmost, northernmost, and southernmost extents of spatial objects. While these longitude and latitude bounds can theoretically define the bounding box of a data file in Iceberg, allowing query predicates to be checked against it, they help optimize spatial filtering operations like ST\_Intersects. However, certain complexities must be considered.

This bounding method is necessary for handling objects that cross the antimeridian (±180° longitude), where the lower longitude bound may be greater than the upper bound. Additionally, for non-planar edge interpolation used in the Geography type, a shape’s bounding box may not always be defined by its vertices, requiring a more precise bounding approach. For example, the territorial waters of Fiji span both hemispheres, with points at (179°E, 18°S), (-179°W, 18°S), (-179°W, 16°S), and (179°E, 16°S). A naive min/max longitude calculation might incorrectly assume the bounding box extends from -179°W to 179°E, nearly covering the entire globe. Instead, Iceberg GEO correctly identifies 179°E as the westernmost point and -179°W as the easternmost, ensuring accurate query filtering and optimization.

For geography types, longitude bounds must fall within \[-180, 180\], while latitude bounds must be within \[-90, 90\].

## Operations and Catalogs

#### DDL, DML, and DQL

Iceberg GEO is natively supported by Iceberg’s table operations, allowing spatial data to be stored, modified, and queried efficiently. When defining a table schema, users can specify geometry or geography columns with optional CRS parameters.

For data manipulation, Iceberg GEO supports inserting, updating, and deleting spatial data using formats such as WKB and WKT. Queries can leverage spatial functions like ST\_Intersects, ST\_Contains, and ST\_Distance, enabling efficient spatial filtering and analysis. Iceberg’s manifest metadata optimizes query execution by pruning unnecessary data files, significantly improving performance for large datasets.

#### Z-Ordering

Iceberg GEO does not define a specific behavior for Z-ordering spatial objects, but engines can implement custom solutions. A common approach is to compute spatial indices such as H3 or S2 and use them for Z-order clustering. This helps preserve spatial locality in storage, improving query performance by reducing unnecessary scans.

#### Compaction

Compaction in Iceberg consolidates small files to improve performance. For spatial data, compaction can leverage Z-ordering to group spatially related objects together, enhancing data locality and reducing read overhead. During compaction, Iceberg needs to recalculate the lower and upper bounds for spatial objects to maintain accurate spatial statistics, ensuring that query pruning remains effective.

#### Catalog Support

Iceberg GEO is fully compatible with the Iceberg REST catalog, which stores metadata in JSON format and allows seamless integration across multiple compute engines. For catalogs like Apache Polaris, AWS Glue, and Hive Metastore, additional change may be required to recognize the new geometry and geography types. However, since Iceberg GEO follows Iceberg’s existing metadata structures, the effort required for adaptation is minimal.

## Migrating from Havasu-Iceberg to Native Iceberg GEO on Wherobots

With the geo types now merged into Apache Iceberg, Wherobots will soon begin assisting customers in migrating all Havasu-Iceberg tables to native Iceberg tables. This transition will streamline spatial data management while ensuring full compatibility with the Apache Iceberg ecosystem.

- If you are using Wherobots-managed Havasu tables, we will handle the migration automatically. Your existing code and workflows will remain unaffected, and you will receive a notification once the migration is complete.
- For those using self-managed Havasu tables on Wherobots, we will provide migration tools to help transition your datasets to native Iceberg tables efficiently.
- Users relying on raster types in Havasu will have a dedicated migration solution available soon. Stay tuned for further updates.

Wherobots is the best compute engine for processing spatial data, makes using Iceberg very easy, and has been tuned for working efficiently with Iceberg tables. Our technologies continue to enhance cost performance and data governance, ensuring the best possible experience for spatial data workloads.

If you want to get started working with our Iceberg enabled Spatial Intelligence Cloud, and begin taking advantage of all the benefits of Iceberg GEO, sign up for a [Wherobots pro account](https://aws.amazon.com/marketplace/pp/prodview-ndy62v6hhwrne?sr=0-1&ref_=beagle&applicationId=AWSMPContessa) on the AWS marketplace, which includes $400 in compute credits. We are hosting regular getting started sessions, and the historical ones can be viewed on our [Wherobots Youtube channel](https://www.youtube.com/@wherobots). As we mentioned upfront, expect to see additional content along with demonstrations in our blog moving forward.

Sign up for our newsletter to stay up to date with everything we are doing to enable the spatial community to embrace the modern geospatial lake-house.