---
title: Quando duckdb e iceberg sono sufficienti?
source: https://www.reddit.com/r/dataengineering/comments/1im5kgl/when_is_duckdb_and_iceberg_enough/
author:
  - "[[haragoshi]]"
published: 2025-02-10
created: 2026-04-04
description:
tags:
  - clippings
  - duckdb
topic:
type: note
---
Sento che c'è così tanto potenziale per allontanarsi dai massicci data warehouse verso un'archiviazione puramente basata su file in iceberg e un calcolo in-process come duckdb. Personalmente non conosco nessuno che lo faccia né ho sentito esperti parlare dell'utilizzo di questo schema.

Semplificherebbe l'architettura, ridurrebbe il vendor locking e ridurrebbe il costo di archiviazione e caricamento dei dati.

Per carichi di lavoro medi, come qualche TB di archiviazione dati all'anno, qualcosa del genere è ideale IMO. È una strategia a lungo termine valida costruire il proprio data warehouse attorno a questi strumenti?

---

## Comments

> **caksters** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc0dk6n/) · 43 points
> 
> Duckdb è progettato per essere utilizzato da un singolo utente. L'utilizzo tipico è locale, quando si desidera elaborare dati usando la sintassi SQL in modo rapido. Duckdb consente la parallelizzazione e permette di interrogare vari formati di dati (csv, avro, file di db).
> 
> È veloce, semplice e ottimo per attività che richiedono l'aggregazione di dati o la join di diversi dataset (carichi di lavoro OLAP).
> 
> Tuttavia, è un database per singolo utente e il progetto non può essere condiviso tra i membri del team. Se sto lavorando con il database, creerà un file di blocco e un altro utente (il tuo compagno di squadra o un'applicazione) non potrà utilizzarlo senza soluzioni alternative poco sicure e complicate.
> 
> In altre parole, è utilizzato per un caso d'uso specifico e non è realmente un'alternativa per un data warehouse di livello enterprise.
> 
> > **patate\_volante** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc0eol1/) · 28 points
> > 
> > OP non sta parlando di file locali qui, ma di file iceberg su un'archiviazione condivisa come S3. È possibile avere molti utenti che leggono i dati contemporaneamente usando duckdb su S3. Per le scritture, è un po' più delicato, ma iceberg usa la concorrenza ottimistica, quindi in teoria funziona.
> > 
> > > **caksters** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc0gre0/) · 10 points
> > > 
> > > Già, hai ragione. Se archivi i dati su iceberg, puoi leggerli come vuoi, quindi niente ti impedisce di leggerli usando duckdb. Duckdb in questo caso è un mezzo per consumare i dati. Stavo pensando più all'utilizzo di duckdb come livello di archiviazione dati persistente con .db
> > > 
> > > **unexpectedreboots** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc2o5hg/) · 5 points
> > > 
> > > AFAIK, duckdb non supporta ancora la scrittura su iceberg.
> 
> > **haragoshi** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc0gb3s/) · 11 points
> > 
> > Sì, DuckDB è single-user. Non sto suggerendo di usare DuckDB al posto di Snowflake, cioè un database relazionale multiutente.
> > 
> > Sto suggerendo di usare DuckDB per fare l'ETL, ad esempio eseguendo l'elaborazione in-process nel tuo codice Python (come faresti con pandas). Puoi quindi usare Iceberg come storage su S3 come in questo commento .
> > 
> > Gli utenti a valle, come i dashboard o le app BI, possono quindi ottenere i dati di cui hanno bisogno da lì. Iceberg è conforme ad ACID e puoi effettuare query direttamente in modo simile a un database. Altre soluzioni di database stanno diventando o sono già compatibili con Iceberg, come Snowflake o Databricks, quindi puoi integrarti con le architetture esistenti.
> > 
> > > **caksters** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc0gzhz/) · 6 points
> > > 
> > > Sono con te.
> > > 
> > > Non credo che importi molto se usi duckdb per la trasformazione o se usi pandas nativo. DuckDb è più la parte T del tuo processo ETL/ELT
> > > 
> > > **DynamicCast** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc1a4hs/) · 2 points
> > > 
> > > DuckDB non può collegarsi a tutte le sorgenti dati, è comunque necessario ottenere i dati in un formato che possa elaborare
> > > 
> > > **OMG\_I\_LOVE\_CHIPOTLE** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc0lott/) · 3 points
> > > 
> > > La tua domanda è praticamente solo "quando Iceberg è abbastanza" e la risposta è che dovrebbe essere la tua impostazione predefinita a meno che tu non sappia di aver bisogno di un sistema OLTP come archivio principale. La maggior parte delle app pensa di averne bisogno, ma non è così.

> **HowSwayGotTheAns** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc0fyzf/) · 13 points
> 
> Se si trascorre abbastanza tempo in questo settore, si noterà che gli esperti del settore promuovono costantemente nuovi modelli, tecnologie o prodotti.
> 
> DuckDB è un progetto impressionante che sfrutta un altro progetto fantastico, Apache Arrow. Iceberg è anche un progetto interessante che risolve alcuni problemi che realisticamente nessun team di una sola persona ha bisogno di risolvere.
> 
> DuckDB+Iceberg non può essere uno standard d'oro per team medi e piccoli, ma potrebbe soddisfare le vostre esigenze.
> 
> Soprattutto se si esegue principalmente l'elaborazione batch di dati per l'analisi.

> **pknpkn21** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc0f3f4/) · 8 points
> 
> Ci sono benchmark che mostrano DuckDB con prestazioni migliori rispetto a Spark e ai data warehouse cloud per dataset più piccoli in GB, il che è prevedibile. Ma una funzionalità chiave che manca in DuckDB è la capacità di leggere Iceberg Catalog.
> 
> Il caso d'uso ideale sarebbe quello di utilizzare un DuckDB self-hosted per ambienti inferiori per sviluppo e test, a condizione che il codice di trasformazione abbia la capacità di funzionare senza problemi su motori diversi.
> 
> > **\[eliminato\]** · 2025-02-10 · 0 points
> > 
> > Sì. È aperto da molto tempo ormai. Non sono sicuro se sia la loro massima priorità, dato che ogni fornitore sta creando la propria versione del catalogo nonostante la definizione REST fornita da Iceberg.
> > 
> > > **pknpkn21** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc1txe8/) · 1 points
> > > 
> > > Sì. È aperto da molto tempo ormai. Non sono sicuro se sia la loro massima priorità, dato che ogni fornitore sta creando la propria versione del catalogo nonostante la definizione REST fornita da Iceberg.

> **pescennius** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc0jlma/) · 5 points
> 
> Penso che basti già se gli unici consumatori sono tecnici (come gli scienziati dei dati) e possono eseguire DuckDB localmente e gestire cose come le viste condivise tramite git (DBT, sqlmesh, script, ecc.).
> 
> Penso che l'architettura di cui stai parlando diventi veramente mainstream quando gli strumenti BI si presentano semplicemente con i propri motori di query simili a DuckDB. Se PowerBI, Tableau o Looker eseguissero semplicemente DuckDB sul client, i dati sorgente potrebbero essere Iceberg o Delta. [Rill](https://www.rilldata.com/) sta già andando in quella direzione. La maggior parte delle organizzazioni non avrebbe bisogno di Snowflake. Solo le aziende con dataset veramente grandi (più di 2 TB) avrebbero davvero bisogno di warehouse dedicati.

> **LargeSale8354** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc0re8x/) · 5 points
> 
> Direi di costruire attorno a loro per ora, mentre soddisfano le tue esigenze attuali, ma pianifica il cambiamento.
> 
> Fin dall'era di Hadoop ho avuto dei dubbi insistenti sul data warehouse senza warehouse. Far funzionare uno stack tecnologico per eseguire un processo per una demo di vendita è una cosa. Partecipare a un webinar interattivo e sembra più comune che raro imbattersi in problemi di concorrenza e prestazioni.
> 
> Hadoop è stato presentato come l'assassino degli appliance DW. Ciò che i suoi sostenitori non sono riusciti a considerare è che non tutto si adatta a un paradigma map-reduce. E la concorrenza non ha avuto un ruolo di primo piano nei loro test.
> 
> Un vecchio ingegnere SAN mi ha fatto un corso accelerato sull'archiviazione. La capacità di storage è economica, le prestazioni di storage non lo sono. Certo, oggi abbiamo gli SSD che hanno innalzato il livello minimo delle prestazioni di storage.
> 
> AWS ha il suo prodotto S3 Tables basato su Iceberg. GCP ha Colossus come file system distribuito sottostante. Il pezzo che manca è la tecnologia che sfrutta al meglio le caratteristiche di storage. Sfuggire al vendor lock-in ha lo svantaggio di rinunciare al vantaggio del fornitore. Si finisce per limitarsi alla tecnologia del denominatore comune.
> 
> > **haragoshi** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc2vj2c/) · 3 points
> > 
> > Il mio problema con Hadoop e Spark è che sono strumenti distribuiti che funzionano meglio su larga scala. Per un carico di lavoro medio, probabilmente non è necessario un sistema distribuito e non si vuole la complessità. Se riesco a far entrare i dati sul mio laptop, probabilmente non dovrei usare Spark/Hadoop.

> **Mythozz2020** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc1m5vr/) · 5 points
> 
> Stiamo eseguendo PoC usando DuckDb per eseguire codice PySpark non modificato con file parquet esistenti memorizzati in GCS.
> 
> Se i tuoi dati sono inferiori a un terabyte, vale la pena provare duckdb..
> 
> A. Mappare i file parquet a un dataset pyarrow
> 
> B. Mappare il dataset pyarrow a una tabella duck usando duckdb.from\_arrow().
> 
> C. Mappare la tabella duckdb a un dataframe spark
> 
> D. Eseguire il codice pyspark senza un cluster spark.
> 
> [https://duckdb.org/docs/api/python/spark\_api.html](https://duckdb.org/docs/api/python/spark_api.html)
> 
> Al momento stiamo effettuando test su server Linux standard con 40 core, ma c'è sempre la possibilità di creare cluster più grandi in kubernetes con più core..

> **aacreans** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc28hvc/) · 4 points
> 
> Il supporto di DuckDB per Iceberg è piuttosto scarso. La mancanza di supporto per il catalog e il predicate pushdown lo rende quasi inutilizzabile per grandi quantità di dati su S3 tbh

> **mertertrern** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc31f8a/) · 4 points
> 
> Dovresti installare PyIceberg \[duckdb,s3fs\] per ottenere una migliore compatibilità con Iceberg Catalog, ma potresti sicuramente usare DuckDB in-memory come passaggio di trasformazione incorporato nella tua pipeline senza bisogno di Snowflake o Databricks, a condizione che l'output sia una tabella PyArrow o un RecordBatchReader che puoi poi portare avanti con PyIceberg/PyArrow, e gestisci le dimensioni dei tuoi dataset in base alla RAM del tuo host DuckDB.
> 
> Ti appoggerai molto a PyIceberg e PyArrow per l'infrastruttura qui, con DuckDB che funge più da chiamata di funzione per eseguire rapide trasformazioni tra i livelli nel tuo modello di dati. Probabilmente userei comunque qualcosa come DLT (non Databricks) per ingerire prima nel tuo livello bronzo/grezzo.
> 
> > **haragoshi** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc32qx8/) · 2 points
> > 
> > Cos'è DLT?
> > 
> > > **mertertrern** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc35gg2/) · 2 points
> > > 
> > > È un pratico framework ELT scritto in Python che a me piace. Guarda tu stesso: [https://dlthub.com/](https://dlthub.com/)

> **patate\_volante** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc0frwk/) · 2 points
> 
> Sono d'accordo sul potenziale. Direi che i limiti sono che 1) le query e le join complesse richiederanno molto tempo e 2) le scritture ad alta frequenza possono diventare costose e problematiche in alcuni casi limite concorrenti. In breve, se il calcolo è intensivo e/o relazionale, è comunque meglio avere un database relazionale dedicato in esecuzione. Altrimenti, si ottengono molti vantaggi da duck e iceberg: semplicità, costo, scalabilità.

> **Signal-Indication859** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc3a288/) · 2 points
> 
> potrebbe essere fattibile + può semplificare la tua architettura e risparmiare sui costi, soprattutto quando si ha a che fare con carichi di lavoro non molto grandi. Personalmente penso che le persone si buttino su configurazioni costose troppo presto. La tendenza sta cambiando verso sistemi più leggeri, basati su file, in quanto riducono la complessità e il vendor lock-in. Tieni solo presente che, man mano che le tue esigenze crescono, potresti incontrare dei limiti, ma per ora va benissimo.
> 
> Con duckdb potresti anche semplicemente impostare alcune app di dati interattive di base come parte di questa architettura con preswald. È open source e ti permette di lavorare con DuckDB e CSV senza gonfiore

> **turbolytics** · [2025-02-11](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc6vygh/) · 2 points
> 
> Quali sono le tue esigenze? Hai bisogno di RBAC o di sicurezza a livello di colonna? Duckdb non è una sostituzione diretta per questo, quindi penso che ci siano ancora molte ragioni legittime per utilizzare database tradizionali.
> 
> Sto lavorando su una serie di sistemi che trasmettono in streaming grandi volumi di dati su storage object e usano duckdb in memoria per effettuare query su di essi. Sono però tutte query programmatiche da macchine, quindi possiamo utilizzare controlli di accesso basati su IAM.
> 
> Quindi sì, assolutamente duckdb e lo storage object stanno prendendo parte dei data warehouse tradizionali. E no, non è una sostituzione diretta... ancora :) :)

> **CrowdGoesWildWoooo** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc0nxxa/) · 1 points
> 
> Dipende davvero dalla dimensione del tuo file.
> 
> Pochi GB aggiunti a pochi TB in un anno, potrebbero funzionare.
> 
> 10-100 GB elaborati ogni settimana. Userei strumenti più appropriati come Athena.
> 
> Il problema con DuckDB è che ha una scalabilità limitata. Se si presume che la dimensione sia costante e si sa che DuckDB funzionerà per la routine di elaborazione, ottimo, puoi usarlo. Cosa succede se l'anno prossimo sarà 5-10 volte quello dell'anno scorso, ora le prestazioni iniziano a degradare.
> 
> Ora, se inizia a degradare, con DuckDB non hai una chiara idea di quale sia il "problema". Diciamo che con Snowflake posso osservare il profilo della query, è a causa di spill? Potatura inefficiente?

> **WeakRelationship2131** · [2025-02-10](https://reddit.com/r/dataengineering/comments/1im5kgl/comment/mc2ru4w/) · 1 points
> 
> Sì, passare a un'archiviazione basata su file con strumenti come Iceberg e DuckDB ha perfettamente senso per carichi di lavoro medi. Abbandonare quei massicci data warehouse può far risparmiare molto in termini di complessità, dipendenza dal fornitore e costi. Basta essere consapevoli che, sebbene funzioni bene per casi d'uso più semplici, il ridimensionamento a carichi di lavoro più grandi o query complesse potrebbe incontrare alcuni limiti. Nel complesso, sicuramente una strategia solida a seconda delle esigenze specifiche e dei piani di crescita.