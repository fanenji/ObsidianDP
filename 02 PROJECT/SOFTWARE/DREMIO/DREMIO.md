---
type: note
topic: data-platform
created: 2026-02-21
tags:
  - data-platform
  - dremio
---


Import dati geo da postgis

PROBLEMA: **[Dremio Limit 32000 bytes of a field](https://community.dremio.com/t/how-to-handle-dremio-limit-32000-bytes-of-a-field/6315)**

```other
ALTER SYSTEM SET limits.single_field_size_bytes = 1000000;
SELECT wkb_geometry FROM postgis.public."ctemi_corine";
```

```other
CREATE VDS "test_geo"."test_comuni_2" as
select * from
Samples."samples.dremio.com"."SF_incidents2016.json"
```

%% MOC START %%
_empty folder_
%% MOC END %%
