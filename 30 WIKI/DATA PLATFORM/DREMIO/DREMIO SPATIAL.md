---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - dremio
  - spatial
  - gis
---

[https://docs.dremio.com/current/reference/sql/sql-functions/GEOSPATIAL/](https://docs.dremio.com/current/reference/sql/sql-functions/GEOSPATIAL/)

# DREMIO-UDF-GIS

[Dremio Geo Spatial Extensions - Announcements](https://community.dremio.com/t/dremio-geo-spatial-extensions-announcements/10280)

[https://github.com/sheinbergon/dremio-udf-gis](https://github.com/sheinbergon/dremio-udf-gis)

Dremio Geospatial Extensions

- Widespread OGC implementation for SQL (adheres to PostGIS standards)
    - Supported input formats: `WKT`, `WKB (HEX or BINARY)`
        - Supported output formats: `WKT`, `WKB`, `GeoJSON`
- Easily installable Maven-Central/Github artifacts shaded jar artifact
- Dremio CE version compatibility (new versions will be released with each community edition)
- Up-2-date Proj4J & JTS geometry based implementation
- Take the shaded jar for the desired version and place inside your Dremio installation (`$DREMIO_HOME/jars/3rdparty`)
- Restart your Dremio server(s)
