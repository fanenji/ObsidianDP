# Quality Benchmark Summary — dbt Incremental Model
**Data:** 2026-04-03 · **Giudice:** Claude Code CLI · **Prompt:** incremental model con due sorgenti, window functions, 4 CTE, schema.yml completo

---

## Classifica complessiva

| Rank | Modello                                    | Backend | ref/src | no `*` | CTEs | Incr. | YAML | Docs | Naming | Window | **Tot /11** | **Overall /10** |
| ---- | ------------------------------------------ | ------- | :-----: | :----: | :--: | :---: | :--: | :--: | :----: | :----: | :---------: | :-------------: |
| 🥇 1 | `devstral-small-2:24b-instruct-2512-fp16`  | remote  |    1    |   0    |  1   |   1   |  2   |  1   |   1    |   2    |    **9**    |     **9.0**     |
| 🥇 1 | `nemotron-3-super:120b-a12b-q4_K_M`        | remote  |    1    |   0    |  1   |   2   |  2   |  0   |   1    |   2    |    **9**    |     **9.0**     |
| 🥉 3 | `gemma4:31b`                               | remote  |    1    |   0    |  1   |   2   |  1   |  0   |   1    |   2    |    **8**    |     **8.0**     |
| 4    | `RogerBen/qwen3.5-35b-opus-distill:latest` | remote  |    1    |   1    |  1   |   2   |  0   |  0   |   1    |   1    |    **7**    |     **7.0**     |
| 5    | `gemma4:26b`                               | local   |    0    |   0    |  1   |   1   |  0   |  0   |   1    |   0    |    **3**    |     **3.0**     |
| —    | `glm-4.7-flash:q8_0`                       | remote  |    0    |   0    |  0   |   0   |  0   |  0   |   0    |   0    |    **0**    |     **0.0**     |
| —    | `nemotron-cascade-2:30b`                   | remote  |    0    |   0    |  0   |   0   |  0   |  0   |   0    |   0    |    **0**    |     **0.0**     |
| —    | `qwen3.5:35b-a3b-coding-nvfp4`             | local   |    0    |   0    |  0   |   0   |  0   |  0   |   0    |   0    |    **0**    |     **0.0**     |

> **Nota:** i tre modelli con score 0 non hanno prodotto codice dbt valutabile (output troncato o assente). I punteggi riflettono solo la qualità del codice generato, non la velocità — per quella vedere i report speed.

---

## Analisi per modello

### 1. `devstral-small-2:24b-instruct-2512-fp16` — 9.0/10

**Punti di forza**
- Uso corretto di `{{ source() }}` per tutte le sorgenti
- Struttura CTE pulita con separazione logica degli step
- `schema.yml` eccellente: ogni colonna documentata con unità di misura e contesto, test di integrità referenziale inclusi
- Window functions con frame clause corretta
- Naming conventions snake_case coerenti

**Punti di debolezza**
- `SELECT *` nel SELECT finale: rompe la column-level lineage e nasconde le dipendenze downstream
- `is_incremental()` guard implementato in modo scorretto: usa `dbt_utils.is_incremental()` (macro inesistente) posizionato come espressione Jinja standalone fuori da un blocco `{% if %}`, il che causa errori a compile time

**Confronto con gli altri**
Miglior documentazione YAML del gruppo (unico con `column_docs = 1` tra i top 3). Supera `nemotron-3-super` sulla documentazione ma lo perde sull'implementazione incrementale dove commette un errore più grave.

---

### 1. `nemotron-3-super:120b-a12b-q4_K_M` — 9.0/10

**Punti di forza**
- Pattern incrementale completo e idiomatico: `{{ config(materialized='incremental') }}` + `{{ is_incremental() }}` guard correttamente posizionato
- 4 CTE ben nominate con separazione delle responsabilità
- Window functions con frame clause esplicita (`ROWS BETWEEN`)
- Uso di `{{ source() }}` coerente

**Punti di debolezza**
- `select * from final` terminale: violazione della regola no-SELECT-*
- 7 delle 12 colonne output prive di descrizione in `schema.yml` (`column_docs = 0`)
- Il test `relationships` in `schema.yml` referenzia `ref('stations')` invece di `source('air_quality', 'stations')`: errore di compile a test time
- Sintassi commenti Jinja non standard (`{{-- --}}` invece di `{# #}`)

**Confronto con gli altri**
L'unico insieme a `gemma4:31b` ad avere `incremental_correct = 2` (pattern completo). Perde su documentazione rispetto a devstral. Il bug nel test `relationships` è sottile ma bloccante in produzione.

---

### 3. `gemma4:31b` — 8.0/10

**Punti di forza**
- Pattern incrementale completo con strategia `merge` e `unique_key`
- Ragionamento architetturale corretto: include un lookback di 7 giorni nell'`is_incremental()` guard per gestire gli edge case delle rolling windows (dettaglio che gli altri modelli ignorano)
- Window functions con frame clause corretta
- `{{ source() }}` usato correttamente

**Punti di debolezza**
- `SELECT *` in `rolling_metrics` e nel SELECT finale (doppia violazione)
- `schema.yml` troncato: manca la documentazione della maggior parte delle 12 colonne output e i test `relationships`
- `column_docs = 0` per via del YAML incompleto

**Confronto con gli altri**
Il lookback window nell'incrementale è il contributo tecnico più sofisticato del gruppo — nessun altro modello lo ha considerato. Tuttavia il `SELECT *` doppio e lo YAML troncato abbassano il punteggio sotto i due leader. Con YAML completo e SELECT espliciti raggiungerebbe 9.5+.

---

### 4. `RogerBen/qwen3.5-35b-opus-distill:latest` — 7.0/10

**Punti di forza**
- Unico modello del gruppo con `no_select_star = 1`: SELECT espliciti ovunque
- Pattern incrementale completo (`incremental_correct = 2`)
- Struttura CTE logica e ben nominata
- `{{ source() }}` usato correttamente

**Punti di debolezza**
- **Bug runtime bloccante**: la CTE `rolling_metrics` referenzia `pm10_value` e `pm25_value`, colonne che non esistono in `daily_agg` (che espone solo `daily_max_pm10` e `daily_max_pm25`). Il modello fallisce ad ogni esecuzione
- Nessun `schema.yml` prodotto: zero test coverage, zero documentazione colonne
- `yaml_tests = 0`, `column_docs = 0`

**Confronto con gli altri**
È l'unico a non usare `SELECT *`, il che è notevole. Ma il bug di column reference è bloccante in produzione, e l'assenza totale di YAML elimina sia i test che la documentazione. Il risultato è paradossale: il modello più rigoroso nella forma ma con un errore logico grave nel corpo.

---

### 5. `gemma4:26b` — 3.0/10

**Punti di forza**
- Config incrementale presente e sintatticamente corretta
- Impostazione architetturale descritta correttamente nella prosa
- Naming conventions coerenti nel codice visibile

**Punti di debolezza**
- Output troncato: il corpo SQL termina alla prima CTE, il modello è incompleto
- Nessun `schema.yml`
- `{{ source() }}` e window functions non verificabili per via del troncamento
- L'`is_incremental()` guard è assente nel codice visibile

**Confronto con gli altri**
Penalizzato principalmente dal troncamento dell'output. Ciò che è visibile è incoraggiante (config corretta, naming OK), ma non è possibile valutare i criteri chiave. Potrebbe performare significativamente meglio con un `max_tokens` più alto nel benchmark.

---

### `glm-4.7-flash:q8_0`, `nemotron-cascade-2:30b`, `qwen3.5:35b-a3b-coding-nvfp4` — 0.0/10

Nessuno dei tre ha prodotto output valutabile:
- `glm-4.7-flash` — SQL troncato dopo `-- models/air`: output tagliato probabilmente per limite di token o crash del modello
- `nemotron-cascade-2` — Risposta testuale senza codice: il modello ha risposto alla domanda descrivendola invece di implementarla
- `qwen3.5:35b-a3b-coding-nvfp4` — Identico a nemotron-cascade-2: nessun codice generato

Per questi tre modelli il fallimento è da attribuire alla generazione, non alla qualità del codice. Non è possibile trarre conclusioni sulla loro capacità dbt.

---

## Osservazioni trasversali

**Problema comune: `SELECT *` nel SELECT finale**
Quattro modelli su cinque valutabili usano `SELECT *` nel SELECT finale o in una CTE intermedia. È il pattern anti-best-practice più diffuso nel gruppo.

**YAML documentation: il punto debole generale**
Solo `devstral-small-2` ha prodotto uno `schema.yml` completo con documentazione colonne. Tre modelli non hanno consegnato YAML, uno lo ha troncato. La documentazione dbt è sistematicamente sottovalutata dai modelli locali testati.

**Implementazione incrementale: divario netto**
`gemma4:31b` e `nemotron-3-super` hanno la migliore comprensione del pattern incrementale (score 2/2). `devstral-small-2` ha un errore grave nell'implementazione nonostante conosca la sintassi. `gemma4:26b` ha il config ma manca il guard.

**Troncamento output: problema infrastrutturale**
Tre modelli su otto hanno prodotto output troncato. È probabile che `max_tokens=2048` sia insufficiente per modelli con risposte verbose. Considerare di aumentarlo a 3000–4096 per i benchmark di qualità.

---

## Raccomandazioni

| Caso d'uso | Modello consigliato |
|------------|---------------------|
| Produzione (qualità massima) | `nemotron-3-super:120b` — pattern incrementale completo, da correggere SELECT * e YAML |
| Velocità + qualità bilanciata | `devstral-small-2:24b` — migliore YAML, da correggere is_incremental() |
| Modello da monitorare | `gemma4:31b` — logica incrementale più sofisticata, necessita YAML completo |
| Non utilizzare per dbt | `nemotron-cascade-2`, `qwen3.5:35b-a3b-coding-nvfp4` — non generano codice |

---

*Generato da analisi manuale dei report `quality_*.csv` · Giudice: Claude Code CLI*

---

PROMPT

You are a senior data engineer. Write production-ready dbt code for this scenario.

Source tables (MUST use {{ source('air_quality', 'table_name') }}):
- measurements: station_id (varchar), measured_at (timestamp), pm10_value (float), pm25_value (float),
  sensor_status (varchar: 'valid' | 'faulty' | 'maintenance')
- stations: station_id (varchar), station_name (varchar), municipality (varchar), region (varchar),
  altitude_m (int), is_active (boolean)

Requirements:
1. INCREMENTAL model: {{ config(materialized='incremental', unique_key='day_station_id') }}
2. Filter: only sensor_status = 'valid' AND is_active = true
3. Compute daily aggregates per station:
   - 7-day rolling average of PM10 and PM25 (window function with ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
   - daily max PM10 and daily max PM25
   - count of valid measurements that day
4. day_station_id must be a surrogate key combining the date and station_id
5. Join station metadata: station_name, municipality, region, altitude_m
6. Use exactly these four CTEs in order: raw_filtered → daily_agg → rolling_metrics → final
7. Add the is_incremental() guard so only new/updated data is processed on incremental runs

Also write a complete schema.yml that includes:
- A model-level description
- A description for EVERY output column
- Tests: unique + not_null on day_station_id; not_null on every metric column;
  a relationships test linking station_id back to the stations source table

---


JUDGE PROMPT

You are an expert dbt and SQL code reviewer. Evaluate the dbt code provided by the user.
Respond ONLY with a valid JSON object — no markdown fences, no text before or after the JSON.

Scoring criteria:
- uses_ref_source [0-1]: uses {{ source() }} macro for all source table references, no hardcoded schema.table
- no_select_star [0-1]: no SELECT * in any CTE or final SELECT
- has_ctes [0-1]: logic is split into named CTEs (WITH x AS (...))
- incremental_correct [0-2]: 0=no incremental config at all, 1=has {{ config(materialized='incremental') }} but missing is_incremental() guard, 2=both present and correct
- yaml_tests [0-2]: 0=missing or only trivial, 1=has not_null+unique only, 2=complete (includes relationships or other advanced tests)
- column_docs [0-1]: schema.yml has a description for the model AND for every output column
- naming_conventions [0-1]: all column aliases and model name are snake_case, no camelCase anywhere
- window_functions [0-2]: 0=missing or syntactically wrong, 1=present but frame clause (ROWS/RANGE BETWEEN) is missing or incorrect, 2=correct with proper frame clause

Return exactly this structure (fill in actual values):
{
  "uses_ref_source": {"score": 0, "comment": "..."},
  "no_select_star": {"score": 1, "comment": "..."},
  "has_ctes": {"score": 1, "comment": "..."},
  "incremental_correct": {"score": 2, "comment": "..."},
  "yaml_tests": {"score": 1, "comment": "..."},
  "column_docs": {"score": 0, "comment": "..."},
  "naming_conventions": {"score": 1, "comment": "..."},
  "window_functions": {"score": 2, "comment": "..."},
  "overall_score": 7.5,
  "summary": "One paragraph overall assessment."
}