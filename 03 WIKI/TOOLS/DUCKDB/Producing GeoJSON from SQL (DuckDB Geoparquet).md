---
title: Producing GeoJSON from SQL, Part 2 (DuckDB/Geoparquet Edition)
source: https://blog.geomusings.com/2024/10/10/producing-geojson-from-sql-part-2-duckdb-geoparquet-edition/
author:
  - "[[Bill Dollins]]"
  - "[[View all posts by Bill Dollins]]"
published: 2024-10-10
created: 2026-04-04
description: A few months ago, I wrote a post about how to generate GeoJSON feature collections using pure SQL in PostGIS. After attending FOSS4GNA and learning more about GeoParquet and DuckDB, I wanted to modify the approach to use those tools. What is DuckDB? It is an in-process SQL database management system designed for fast analytical…
tags:
  - clippings
  - mapping
  - duckdb
topic:
type: note
---
A few months ago, [I wrote a post](https://blog.geomusings.com/2024/06/04/producing-geojson-with-sql/) about how to generate GeoJSON feature collections using pure SQL in PostGIS. After attending [FOSS4GNA](https://www.foss4gna.org/) and learning more about [GeoParquet](https://geoparquet.org/) and [DuckDB](https://duckdb.org/), I wanted to modify the approach to use those tools.

What is DuckDB? It is an in-process SQL database management system designed for fast analytical query processing. It is lightweight yet powerful, supporting complex operations such as OLAP (Online Analytical Processing) queries directly within applications. It also has the ability to natively read from external data formats, like Parquet and CSV, without the need for data loading or transformation, making it ideal for working with large datasets in data science and analytics workflows by providing a common proxy interface for those various formats.

What about GeoParquet? It is an extension of the [Parquet](https://parquet.apache.org/) file format, designed specifically for efficiently storing geospatial data. It builds on Parquet’s columnar storage advantages, such as optimized performance for read-heavy analytical workloads and compression, while adding support for geospatial data types like points, lines, and polygons. GeoParquet ensures that geospatial data is stored in a standardized way, making it easier to share and work with across different tools and platforms that support both Parquet and spatial data processing.

Why proxy a cloud-native format into one that is not? There is still a clear boundary between cloud and not-cloud in most geospatial workflows. In this case, my work is the first step toward a [Koop](https://koopjs.github.io/) provider that uses DuckDB to feed GeoParquet formatted data into software that requires feature services in the [GeoServices REST Specification](https://www.esri.com/content/dam/esrisites/sitecore-archive/Files/Pdfs/library/whitepapers/pdfs/geoservices-rest-spec.pdf) (PDF).

For this work, I used a combined data set of [Google, Microsoft, and OSM building footprints](https://beta.source.coop/repositories/vida/google-microsoft-osm-open-buildings/description/) in [GeoParquet 1.1.0](https://geoparquet.org/releases/v1.1.0/) format that I downloaded from Source Cooperative. I used the data set for Ireland because I was working on my laptop and it is reasonably sized.

With all of that front matter out of the way, let’s jump into some code. I’m following the same pattern that I used in the previous post, so the initial CTE accesses the external GeoParquet file with the read\_parquet() function of DuckDB. I also add a calculated OBJECTID column in preparation for eventual GeoServices integration. I am limited it to the first 1000 records for testing. This data set has over three million rows.

```
WITH geodata AS (
        
        
          

          SELECT
        
        
          

              ROW_NUMBER() OVER () AS OBJECTID,
        
        
          

              *
        
        
          

          FROM
        
        
          

              read_parquet('~/Downloads/IRL.parquet') LIMIT 1000)
        
        
          

          select json_object(
        
        
          

          'type', 'FeatureCollection',
        
        
          

              'features', array_agg(
        
        
          

                  json_object(
        
        
          

                      'type', 'Feature',
        
        
          

                      'geometry', ST_AsGeoJSON(geometry),
        
        
          

                      'properties', json_object(
        
        
          

                      'bf_source', bf_source,
        
        
          

                      'boundary_id', boundary_id,
        
        
          

                      'confidence', confidence,
        
        
          

                      'area_in_meters', area_in_meters,
        
        
          

                      's2_id', s2_id,
        
        
          

                      'country_iso', country_iso,
        
        
          

                      'geohash', geohash,
        
        
          

                      'OBJECTID', OBJECTID
        
        
          

                      )
        
        
          

                  )
        
        
          

                  )
        
        
          

          ) AS geojson_featurecollection
        
        
          

          FROM geodata;
```

DuckDB has spatial and JSON extensions ready to go. The spatial functions are similar to those in PostGIS, the JSON functions are a little more different and that was where most of the translation work happened.

From here, the next steps are to “genericize” the query so that it dynamically pulls in arbitrary columns and handles them. This version of the query has to know too much about the data set to be useful in a Koop provider.

One thing that jumped out at me is how fast DuckDB is. Even when I’m not limiting the query, it returns data quickly. For that reason, I want to push as much of the data handing down to DuckDB and have the Koop provider be a pass-through. In practice, that will be passing column selections and WHERE clauses down to DuckDB for handling. It looks to be fun.

So that’s where my work stands for now. I’ll post updates as I move forward.