---
title: "dbt YAML schema for daily media calculations"
type: conversation
topic: data-platform
created: 2026-02-13
tags:
  - dbt
  - yaml
---
> From: https://claude.ai/chat/77158dd1-92a8-4a75-88cf-22bc539cf30e

# you asked

Scrivimi un file yaml in stile dbt che descriva la tavola sottostante, scrivi le descizioni in italiano racchiuse da doppi apici ("). Il nome del modello è bus_MEDIA_GIORNALIERA
{{ config( object_storage_source="progetto_pilota_aria", database="space_progetto_pilota_aria", schema = "Business", materialized="view" ) }}
WITH valori_prep_media_gg AS ( SELECT * FROM {{ ref('bus_VALORI_PREP') }} -- this condition because we have 1 day from previous anno (for example: 31.12.2023) to calculate then media mobile 8 oraria WHERE YEAR (DATA_DA) > (SELECT MIN (YEAR (DATA_DA)) FROM {{ ref('bus_VALORI_PREP') }}) ),
calcolo_media_gg_val AS ( {{ media_gg ('VAL', "COD_VALID = '0'") }} ),
calcolo_media_gg_val_cor AS ( {{ media_gg ('VAL_COR', "COD_VALID = '0' AND COD_VALIDAZ = 'V'") }} ),
calcolo_media_gg_cert AS ( {{ media_gg ('CERT', "COD_VALIDAZ_REG = 'V'") }} ),
final as ( select t.*, b.MEDIA_GIORNALIERA_VAL_COR, b.VALORI_VALIDI_GG_VAL_COR, h.MEDIA_GIORNALIERA_CERT, h.VALORI_VALIDI_GG_CERT from calcolo_media_gg_val t left join calcolo_media_gg_val_cor b on t.DATA = b.DATA AND t.COD_UBIC = b.COD_UBIC AND t.COD_CONF = b.COD_CONF AND t.SIGLA_PARAM = b.SIGLA_PARAM left join calcolo_media_gg_cert h on h.DATA = b.DATA AND h.COD_UBIC = b.COD_UBIC AND h.COD_CONF = b.COD_CONF AND h.SIGLA_PARAM = b.SIGLA_PARAM )
select * from final

---

# claude response

**bus_MEDIA_GIORNALIERA.yml**
```text
version: 2

models:
  - name: bus_MEDIA_GIORNALIERA
    description: "Modello che calcola le medie giornaliere dei valori misurati (VAL, VAL_COR e CERT) a partire dai dati preparati. Include il conteggio dei valori validi per giorno e applica diverse condizioni di validazione in base al tipo di valore."
    
    columns:
      - name: DATA
        description: "Data di riferimento per il calcolo della media giornaliera"
        tests:
          - not_null
      
      - name: COD_UBIC
        description: "Codice identificativo dell'ubicazione/stazione di misurazione"
        tests:
          - not_null
      
      - name: COD_CONF
        description: "Codice configurazione dello strumento di misura"
        tests:
          - not_null
      
      - name: SIGLA_PARAM
        description: "Sigla del parametro ambientale misurato (es. PM10, NO2, O3)"
        tests:
          - not_null
      
      - name: MEDIA_GIORNALIERA_VAL
        description: "Media giornaliera calcolata sui valori VAL con codice di validità uguale a '0'"
      
      - name: VALORI_VALIDI_GG_VAL
        description: "Numero di valori validi utilizzati per calcolare la media giornaliera VAL"
      
      - name: MEDIA_GIORNALIERA_VAL_COR
        description: "Media giornaliera calcolata sui valori VAL_COR (valori corretti) con codice di validità '0' e codice di validazione 'V'"
      
      - name: VALORI_VALIDI_GG_VAL_COR
        description: "Numero di valori validi utilizzati per calcolare la media giornaliera VAL_COR"
      
      - name: MEDIA_GIORNALIERA_CERT
        description: "Media giornaliera calcolata sui valori CERT (valori certificati) con codice di validazione regionale 'V'"
      
      - name: VALORI_VALIDI_GG_CERT
        description: "Numero di valori validi utilizzati per calcolare la media giornaliera CERT"

```

Ho creato il file YAML in stile dbt per il modello `bus_MEDIA_GIORNALIERA`. Il file include:

- **Descrizione del modello**: spiega che calcola le medie giornaliere di tre tipologie di valori (VAL, VAL_COR e CERT) con diverse condizioni di validazione
- **Colonne chiave**: DATA, COD_UBIC, COD_CONF, SIGLA_PARAM con test di `not_null` per garantire l'integrità dei dati
- **Colonne di output**: le tre medie giornaliere e i rispettivi contatori di valori validi

Tutte le descrizioni sono in italiano e racchiuse tra doppi apici come richiesto. Se hai bisogno di modifiche o ulteriori dettagli, fammi sapere!
