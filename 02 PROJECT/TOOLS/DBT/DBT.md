---
type: note
topic: data-platform
created: 2026-02-17
tags:
  - data-platform
  - dbt
---

# METADATI

- owners (tecnico, analitycs, business)
- domain
- frequency
- sensitivity
- pii

# NESSIE BRANCH SU DBT

[https://community.dremio.com/t/how-work-with-branch-using-dbt-dremio-nessie/11792/4](https://community.dremio.com/t/how-work-with-branch-using-dbt-dremio-nessie/11792/4)

the same as source and ref macro . if you wan’t create table in custom branch write one custom macro for `create_table_as`  

Currently dbt for dremio adapter not support with branch you can try `dbt/include/dremio/macros/materializations/table/create_table_as.sql` this and modify it add branch support.

For dbt project use dbt dispatch `https://docs.getdbt.com/reference/dbt-jinja-functions/dispatch` with your own create_table_as macro

dremio nessie data source create table with branch can like this

`CREATE table dbtv4.myappv5 **AT  BRANCH prod** as select * from pg.public.sensor`

---

## INTERVENTI

Impostato pre_hook su raw.sql

```yaml
pre_hook="CREATE BRANCH IF NOT EXISTS test_dbt_create_branch IN Nessie;"
```

Creata macro /Users/stefano/Development/DP/dbt-projects/test_nessie_branch/macros/create_table_as.sql

Creata macro /Users/stefano/Development/DP/dbt-projects/test_nessie_branch/macros/relation.sql

MACRO DREMIO ORIGINALI

[https://github.com/dremio/dbt-dremio/blob/main/dbt/include/dremio/macros/materializations/table/create_table_as.sql](https://github.com/dremio/dbt-dremio/blob/main/dbt/include/dremio/macros/materializations/table/create_table_as.sql)

[https://github.com/dremio/dbt-dremio/blob/main/dbt/include/dremio/macros/adapters/relation.sql](https://github.com/dremio/dbt-dremio/blob/main/dbt/include/dremio/macros/adapters/relation.sql)

Gestito dispatch in dbt_project.yml

```yaml
dispatch:
  - macro_namespace: dbt_dremio
    search_order: ['test_nessie_branch', 'dbt_dremio']
```

DEFINIZIONE BRANCH IN UNA VARIABILE

- IN dbt_project.yml
- DA LINEA DI COMANDO
- IN VARIABILE D’AMBIENTE

```bash
dbt run --select raw --vars '{"branch": "test_nessie_branch"}' --debug
```

Modificato le due macro per leggere la variabile

```python
{%- set branch = var("branch") -%}
```

## **TODO**

- pre_hook in raw sql → richiamare macro ad-hoc [https://discourse.getdbt.com/t/local-variable-set-variable-usage-in-config-block/4915](https://discourse.getdbt.com/t/local-variable-set-variable-usage-in-config-block/4915)


# TEST SCRITTURA YAML DA SQL CON LLM

[https://docs.getdbt.com/blog/create-dbt-documentation-10x-faster-with-ChatGPT](https://docs.getdbt.com/blog/create-dbt-documentation-10x-faster-with-ChatGPT)

```other
Scrivimi un file yaml in stile dbt che descriva la tavola sottostante, scrivi le descizioni in italiano racchiuse da doppi apici ("). Il nome del modello è bus_MEDIA_GIORNALIERA
```

```sql
{{ config(
  object_storage_source="progetto_pilota_aria",
  database="space_progetto_pilota_aria",
  schema = "Business",
  materialized="view"
) }}

WITH valori_prep_media_gg AS (
SELECT
*
FROM {{ ref('bus_VALORI_PREP') }}
    -- this condition because we have 1 day from previous anno (for example: 31.12.2023) to calculate then media mobile 8 oraria
WHERE YEAR (DATA_DA) > (SELECT MIN (YEAR (DATA_DA)) FROM {{ ref('bus_VALORI_PREP') }})
    ),

calcolo_media_gg_val AS (
{{ media_gg ('VAL', "COD_VALID = '0'") }}
    ),

calcolo_media_gg_val_cor AS (
{{ media_gg ('VAL_COR', "COD_VALID = '0' AND COD_VALIDAZ = 'V'") }}
    ),

calcolo_media_gg_cert AS (
{{ media_gg ('CERT', "COD_VALIDAZ_REG = 'V'") }}
    ),

final as (
select t.*, b.MEDIA_GIORNALIERA_VAL_COR, b.VALORI_VALIDI_GG_VAL_COR, h.MEDIA_GIORNALIERA_CERT, h.VALORI_VALIDI_GG_CERT
from 
calcolo_media_gg_val t
left join
calcolo_media_gg_val_cor b on t.DATA = b.DATA AND t.COD_UBIC = b.COD_UBIC AND t.COD_CONF = b.COD_CONF AND t.SIGLA_PARAM = b.SIGLA_PARAM
left join 
calcolo_media_gg_cert h on h.DATA = b.DATA AND h.COD_UBIC = b.COD_UBIC AND h.COD_CONF = b.COD_CONF AND h.SIGLA_PARAM = b.SIGLA_PARAM )

select * from final
```

```yaml
version: 2

models:
  - name: bus_MEDIA_GIORNALIERA
    description: "Tabella che contiene le medie giornaliere dei valori misurati per diversi stati di validazione/correzione (Valore Grezzo, Corretto e Certificato)."
    
    columns:
      - name: DATA
        description: "Data di riferimento della media giornaliera."
        tests:
          - not_null
      
      - name: COD_UBIC
        description: "Codice identificativo dell'ubicazione della stazione di monitoraggio."
        tests:
          - not_null

      - name: COD_CONF
        description: "Codice identificativo della configurazione di misura."
        tests:
          - not_null

      - name: SIGLA_PARAM
        description: "Sigla del parametro misurato (es. NO2, PM10)."
        tests:
          - not_null

      - name: MEDIA_GIORNALIERA_VAL
        description: "Media giornaliera calcolata sui valori orari grezzi validi (COD_VALID = '0')."

      - name: VALORI_VALIDI_GG_VAL
        description: "Numero di valori orari validi utilizzati per il calcolo della media giornaliera MEDIA_GIORNALIERA_VAL."

      - name: MEDIA_GIORNALIERA_VAL_COR
        description: "Media giornaliera calcolata sui valori orari validati e corretti (COD_VALID = '0' AND COD_VALIDAZ = 'V')."

      - name: VALORI_VALIDI_GG_VAL_COR
        description: "Numero di valori orari validi utilizzati per il calcolo della media giornaliera MEDIA_GIORNALIERA_VAL_COR."

      - name: MEDIA_GIORNALIERA_CERT
        description: "Media giornaliera calcolata sui valori orari certificati (COD_VALIDAZ_REG = 'V')."

      - name: VALORI_VALIDI_GG_CERT
        description: "Numero di valori orari validi utilizzati per il calcolo della media giornaliera MEDIA_GIORNALIERA_CERT."
        
    tests:
      # Test per assicurare che la combinazione delle chiavi sia unica
      - unique:
          column_names: ["DATA", "COD_UBIC", "COD_CONF", "SIGLA_PARAM"]
```

%% MOC START %%
_empty folder_
%% MOC END %%
