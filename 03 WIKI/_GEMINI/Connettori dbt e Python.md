---
title: "Connettori dbt e Python"
type: conversation
topic: data-platform
created: 2026-02-13
tags:
  - dbt
  - python
---
**Source:** https://aistudio.google.com/u/1/prompts/1aBD_VwyvYcrgX7qQgfVebl9Ve-W776U7

## System Instructions

Optional tone and style instructions for the model

---

### User

Quali connettori dbt gestiscono i modelli python? So che il connettore duckdb lo gestisce, altri?

---

### Model

Oltre al connettore **DuckDB** (che esegue il codice localmente o in-process), i connettori ufficiali dbt che supportano nativamente i **modelli Python** (`.py` files nella cartella `models/`) sono principalmente quelli legati alle piattaforme Cloud Data Warehouse moderne che dispongono di un runtime Python integrato.

Ecco la lista aggiornata dei connettori che gestiscono i modelli Python:

### 1. I "Big Three" (Pieno supporto ufficiale)
Questi sono i connettori principali per cui dbt Labs ha sviluppato la funzionalità:
*   **dbt-snowflake**: Utilizza l'API di **Snowpark**.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHO9TOKjrBvq18I4dxDnp5E8Us43l_UvncZuRnsJBoEwntw66b22FczkjTRbSFEaMZjvLSf4zf4SMKkbFuIZYF00X3yWOKOhbzFXSO9yDs25j8MLjLhi5ujT0G_VDWuoNFsedDp5JsEdJQvawndDqaLlclAjk3hC5hGlcMDeXZYb9UPu4nMc3aFGdFgkNKl2kkG9JXpsMGjbvVRZVlTG7rNflM_q-X3Vi0aI6ASCYvigtNVUmBF8HHf)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGusufxnogNP6wowuoUHvnNpoldMbUBJ1FWTF2ncfA8yKX5CjBygaQns7QFW3yJwpN3LwxEuGeQMj3g-XS79Q62HrDQYfupfLHKqN2Y4JEsEbZiUwoAVyjenxz4pa2nBs7ozwc%3D)] Il codice Python viene eseguito direttamente sui warehouse di Snowflake.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHO9TOKjrBvq18I4dxDnp5E8Us43l_UvncZuRnsJBoEwntw66b22FczkjTRbSFEaMZjvLSf4zf4SMKkbFuIZYF00X3yWOKOhbzFXSO9yDs25j8MLjLhi5ujT0G_VDWuoNFsedDp5JsEdJQvawndDqaLlclAjk3hC5hGlcMDeXZYb9UPu4nMc3aFGdFgkNKl2kkG9JXpsMGjbvVRZVlTG7rNflM_q-X3Vi0aI6ASCYvigtNVUmBF8HHf)]
*   **dbt-databricks**: Utilizza i cluster Spark di Databricks.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHO9TOKjrBvq18I4dxDnp5E8Us43l_UvncZuRnsJBoEwntw66b22FczkjTRbSFEaMZjvLSf4zf4SMKkbFuIZYF00X3yWOKOhbzFXSO9yDs25j8MLjLhi5ujT0G_VDWuoNFsedDp5JsEdJQvawndDqaLlclAjk3hC5hGlcMDeXZYb9UPu4nMc3aFGdFgkNKl2kkG9JXpsMGjbvVRZVlTG7rNflM_q-X3Vi0aI6ASCYvigtNVUmBF8HHf)]
*   **dbt-bigquery**: Utilizza **Dataproc** (cluster Spark gestiti da Google) o il più recente **BigQuery Studio** (tramite DataFrames BigQuery).[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHO9TOKjrBvq18I4dxDnp5E8Us43l_UvncZuRnsJBoEwntw66b22FczkjTRbSFEaMZjvLSf4zf4SMKkbFuIZYF00X3yWOKOhbzFXSO9yDs25j8MLjLhi5ujT0G_VDWuoNFsedDp5JsEdJQvawndDqaLlclAjk3hC5hGlcMDeXZYb9UPu4nMc3aFGdFgkNKl2kkG9JXpsMGjbvVRZVlTG7rNflM_q-X3Vi0aI6ASCYvigtNVUmBF8HHf)]

### 2. Altri Connettori
*   **dbt-duckdb**: Come hai menzionato, supporta i modelli Python eseguendoli in locale.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHO9TOKjrBvq18I4dxDnp5E8Us43l_UvncZuRnsJBoEwntw66b22FczkjTRbSFEaMZjvLSf4zf4SMKkbFuIZYF00X3yWOKOhbzFXSO9yDs25j8MLjLhi5ujT0G_VDWuoNFsedDp5JsEdJQvawndDqaLlclAjk3hC5hGlcMDeXZYb9UPu4nMc3aFGdFgkNKl2kkG9JXpsMGjbvVRZVlTG7rNflM_q-X3Vi0aI6ASCYvigtNVUmBF8HHf)] È eccellente per lo sviluppo locale o pipeline leggere, poiché non richiede un cluster esterno: il "motore" è la libreria DuckDB stessa installata nell'ambiente Python di dbt.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHO9TOKjrBvq18I4dxDnp5E8Us43l_UvncZuRnsJBoEwntw66b22FczkjTRbSFEaMZjvLSf4zf4SMKkbFuIZYF00X3yWOKOhbzFXSO9yDs25j8MLjLhi5ujT0G_VDWuoNFsedDp5JsEdJQvawndDqaLlclAjk3hC5hGlcMDeXZYb9UPu4nMc3aFGdFgkNKl2kkG9JXpsMGjbvVRZVlTG7rNflM_q-X3Vi0aI6ASCYvigtNVUmBF8HHf)]

### 3. Supporto parziale o tramite Workaround
Molti altri database (come **Postgres**, **Redshift** o **SQL Server**) non supportano nativamente i modelli Python di dbt perché il database stesso non ha un motore Python interno capace di processare DataFrame come fanno Snowpark o Spark.

Tuttavia, esistono soluzioni alternative per usare Python con questi connettori:
*   **dbt-fal**: È un adapter "wrapper" o un plugin che permette di eseguire script Python in locale (o nel cloud di fal) dopo o prima dei modelli dbt, e può scrivere i risultati indietro nel database (es. Postgres o BigQuery).[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHO9TOKjrBvq18I4dxDnp5E8Us43l_UvncZuRnsJBoEwntw66b22FczkjTRbSFEaMZjvLSf4zf4SMKkbFuIZYF00X3yWOKOhbzFXSO9yDs25j8MLjLhi5ujT0G_VDWuoNFsedDp5JsEdJQvawndDqaLlclAjk3hC5hGlcMDeXZYb9UPu4nMc3aFGdFgkNKl2kkG9JXpsMGjbvVRZVlTG7rNflM_q-X3Vi0aI6ASCYvigtNVUmBF8HHf)]
*   **dbt-spark (Open Source)**: Storicamente, il supporto per i modelli Python in `dbt-spark` era limitato o delegato a Databricks. Se usi Spark "vanilla" (es.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHO9TOKjrBvq18I4dxDnp5E8Us43l_UvncZuRnsJBoEwntw66b22FczkjTRbSFEaMZjvLSf4zf4SMKkbFuIZYF00X3yWOKOhbzFXSO9yDs25j8MLjLhi5ujT0G_VDWuoNFsedDp5JsEdJQvawndDqaLlclAjk3hC5hGlcMDeXZYb9UPu4nMc3aFGdFgkNKl2kkG9JXpsMGjbvVRZVlTG7rNflM_q-X3Vi0aI6ASCYvigtNVUmBF8HHf)] su un cluster EMR o Kubernetes generico), il supporto ufficiale per i modelli Python dbt potrebbe essere assente o sperimentale, poiché richiede un meccanismo standard per inviare il job Python al cluster che varia molto tra le diverse distribuzioni di Spark.

### In sintesi
Se il tuo obiettivo è usare la funzionalità nativa `dbt Python models` (dove definisci un file `.py` che ritorna un DataFrame), devi orientarti su **Snowflake**, **Databricks**, **BigQuery** o **DuckDB**. Su altre piattaforme, dovrai quasi sicuramente affidarti al classico SQL o a strumenti esterni di orchestrazione.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHO9TOKjrBvq18I4dxDnp5E8Us43l_UvncZuRnsJBoEwntw66b22FczkjTRbSFEaMZjvLSf4zf4SMKkbFuIZYF00X3yWOKOhbzFXSO9yDs25j8MLjLhi5ujT0G_VDWuoNFsedDp5JsEdJQvawndDqaLlclAjk3hC5hGlcMDeXZYb9UPu4nMc3aFGdFgkNKl2kkG9JXpsMGjbvVRZVlTG7rNflM_q-X3Vi0aI6ASCYvigtNVUmBF8HHf)]

---

### User

approfondisci su dbt-fal

---

### Model

È fondamentale fare una distinzione importante sullo stato attuale di questo strumento, perché la situazione è cambiata drasticamente nel **2024**.

Ecco l'approfondimento su **dbt-fal**:

### 1. Stato Attuale: Progetto Archiviato (Deprecated)
La notizia più importante è che **`dbt-fal` è stato ufficialmente dismesso**.
Nell'aprile 2024, il team di **fal.ai** (l'azienda dietro il progetto) ha annunciato l'archiviazione del repository GitHub per concentrarsi su una nuova piattaforma dedicata alla *generative media*.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHghuzADBqjtPwImk0RS1WVVnZP90HZWBFY0h5pfIiRREgswMsWYBGMlSYo-GZNLJEma0KvOVA1uLa04HeKz4bs9wuncLThOnQJGQC2aBDykR6q_Y-7EqIuHeeY)]
*   **Cosa significa per te:** Non riceverà più aggiornamenti, patch di sicurezza o supporto per le nuove versioni di dbt Core (es. le versioni 1.8+). Se provi a usarlo oggi su un nuovo progetto, rischierai conflitti di dipendenze.

### 2. A cosa serviva e come funzionava
Prima della dismissione, `dbt-fal` era molto popolare perché risolveva un problema specifico: permetteva di usare i **modelli Python** su database che non li supportavano (come **Postgres** o **Redshift**).[[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQG6P5PzO1OipIHLHw_1MPqoWwfHXZ-g9JVxiZtcdFE_GQqIJL2QPkyvnX0eL-Li7LZS_3e6e7xn6g89HCXbdOtIsCXw3AvNFWbyQeoVuRwCj-7n-87JJ9aVuBOFA7gle_yPFyszLB4FD1A%3D)]

Il suo funzionamento era ingegnoso ma diverso dai connettori nativi:
1.  **Esecuzione Locale ("Sidecar"):** Mentre Snowflake/BigQuery eseguono il Python *dentro* il loro cloud, `dbt-fal` scaricava i dati dal tuo database (es. Postgres) nella memoria della macchina dove stavi lanciando dbt (il tuo PC o un server CI/CD).
2.  **Elaborazione:** Convertiva i dati in un DataFrame Pandas, eseguiva il tuo script Python `.py`.
3.  **Scrittura:** Caricava il risultato finale indietro nel database come una nuova tabella.

**I vantaggi che offriva:**
*   Permetteva di fare machine learning leggero o statistiche complesse su Postgres/Redshift senza dover configurare un'infrastruttura esterna (come Airflow o K8s).
*   Gestiva le dipendenze Python in ambienti virtuali isolati per ogni modello.

### 3. Le alternative oggi (2025)
Dato che `dbt-fal` non è più mantenuto, se hai bisogno di eseguire Python su database non nativi (come Postgres), ecco le strade percorribili oggi:

*   **dbt-postgres-python (Fork della community):** Un membro della community ha creato un fork chiamato `dbt-postgres-python` per mantenere viva la funzionalità specifica per Postgres. È una soluzione "tampone" se hai assolutamente bisogno di questa funzionalità su un legacy Postgres, ma non è un prodotto supportato ufficialmente da dbt Labs.
*   **Orchestrazione Esterna (Consigliato):** La "best practice" moderna per chi usa Postgres/Redshift è non forzare dbt a fare tutto. Si usa uno strumento come **Dagster**, **Prefect** o **Airflow**.
    *   *Esempio:* Usi dbt per trasformare i dati SQL, poi l'orchestratore lancia uno script Python che legge da Postgres, elabora e riscrive, e infine lancia i test dbt finali.
*   **DuckDB per carichi locali:** Se il tuo obiettivo è solo trasformare dati con Python senza un warehouse costoso, usare il connettore **dbt-duckdb** è oggi la scelta standard più solida. DuckDB può leggere file esterni o collegarsi ad altri DB, processare in Python/SQL locale ad altissima velocità e salvare il risultato.

**In sintesi:** Se trovi vecchi tutorial su `dbt-fal`, considerali obsoleti. Non costruirci sopra nuove pipeline critiche.

---
