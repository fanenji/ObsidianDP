---
title: Airflow vs Kestra
source: https://www.reddit.com/r/dataengineering/comments/1hmfxrg/airflow_vs_kestra/
author:
  - "[[[deleted]]]"
published: 2024-12-26
created: 2026-04-04
description:
tags:
  - clippings
  - architecture
  - kestra
topic:
type: note
---
Sto pensando di costruire un po' di esempi, un'infrastruttura di container ospitata localmente durante le vacanze di fine anno. In particolare, sto cercando di gestire dati che sono normalmente piuttosto schifosi in un ambiente SQL/RDBMS tradizionale. Sto cercando di rivedere alcuni processi ETL/ELT per i flussi di lavoro dei dati esistenti nella mia testa.

Credo che quello che sto considerando possa essere fatto con Airflow abbastanza facilmente, ma che l'esperienza di aggiornamento e distribuzione dell'UI/UX/Code non sia un granché. Sono sicuro che potrei costruire rapidamente un'immagine docker con le librerie aggiuntive che mi serviranno abbastanza facilmente. Mi sono anche imbattuto in Kestra, che sembra possa risolvere l'esperienza Ui/UX e collegarsi a github ecc. in modo più carino out of the box, ma non mi è molto chiaro come fare build personalizzate per includere le librerie di dati aggiuntive di cui avrò bisogno.

Ci sono commenti generali su trappole, insidie, difetti ecc. con Kestra di cui dovrei essere a conoscenza? Non prenderò in considerazione la versione a pagamento durante i miei esperimenti.

---

## Comments

> **Zamyatin\_Y** · [2024-12-26](https://reddit.com/r/dataengineering/comments/1hmfxrg/comment/m3uwbow/) · 7 points
> 
> Il prossimo corso di data engineering su Zoom inizierà a gennaio e userà Kestra come strumento di orchestrazione (gli anni passati usavano prefect e airflow, se non sbaglio).
> 
> Immagino potresti dare un'occhiata a quella settimana specifica e saperne di più sullo strumento.
> 
> > **\[eliminato\]** · [2024-12-26](https://reddit.com/r/dataengineering/comments/1hmfxrg/comment/m3uxaaj/) · 4 points
> > 
> > Grazie per questo. Chi tiene il corso / dove posso trovare maggiori informazioni?
> > 
> > > **Zamyatin\_Y** · [2024-12-26](https://reddit.com/r/dataengineering/comments/1hmfxrg/comment/m3uxh8i/) · 7 points
> > > 
> > > [https://github.com/DataTalksClub/data-engineering-zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)

> **No-Routine1610** · [2024-12-26](https://reddit.com/r/dataengineering/comments/1hmfxrg/comment/m3x8t1k/) · 7 points
> 
> Usiamo Kestra su un cluster K8s per orchestrare processi ELT da S3 a un DB Clickhouse e per attivare alcuni usps in un MariaDB. Sono stato coinvolto nella configurazione e nella distribuzione iniziale di alcuni flussi.
> 
> In generale, è facile e veloce iniziare con Kestra e se non si incontrano casi complessi, si andrà bene e si lavorerà velocemente. In questo progetto specifico, questo è il motivo per cui abbiamo scelto Kestra, tuttavia i miei sentimenti sono contrastanti.
> 
> Grande apprezzamento per Kestra che ha un provider Terraform per distribuire i flussi.
> 
> Contro/insidie:
> 
> - A parte la documentazione, che è discreta, non c'è un vero supporto della community se si incontrano problemi. O lo si capisce con tentativi ed errori o è tutto.
> - Sarà necessario codice personalizzato se si deve connettere un'origine dati per cui non esiste un connettore Kestra.
> - È un PITA eseguire il debug degli operatori backend che vengono eseguiti in background quando si invocano alcune espressioni YAML. Per l'archiviazione dei dati intermedi, abbiamo avuto una soluzione S3 personalizzata con una pessima implementazione che ha finito per produrre 400 e il massimo che si ottiene è lo stack di chiamate Java troncato. Alla fine non abbiamo mai scoperto il problema perché non siamo nemmeno riusciti a far restituire a Kestra la risposta HTTP e abbiamo avuto bisogno di una soluzione alternativa. Questo non sarebbe mai successo con Airflow :)
> - la versione OSS non gestisce alcun tipo di autorizzazione adeguata e supporta solo l'autenticazione di base limitata per la sua interfaccia web.
> 
> TLDR: se si hanno casi d'uso più semplici e origini dati generiche e tutto funziona OOB, si andrà bene con Kestra. Potrebbe però diventare fastidioso se lo si "supera" o si incontrano problemi.

> **Beautiful-Hotel-3094** · [2024-12-26](https://reddit.com/r/dataengineering/comments/1hmfxrg/comment/m3vts1a/) · 6 points
> 
> Airflow ha molto più supporto/community se si sceglie un SaaS. Se si riesce a separare correttamente l'orchestrazione dalla logica di business e ad avere un modo per eseguire il debug localmente senza dipendenze da Airflow, si è a posto con Airflow. Questo è il mio contributo, da una società dove abbiamo circa 2.500 DAG, ognuno dei quali viene eseguito con una cadenza di 5 minuti-trimestrale, ognuno con un certo numero di task. Il supporto per Airflow non è eguagliabile da nessun altro strumento di orchestrazione al momento.
> 
> > **sonne887** · [2024-12-26](https://reddit.com/r/dataengineering/comments/1hmfxrg/comment/m3wvobp/) · 1 points
> > 
> > Hai qualche template per separare l'orchestrazione del modello di business?
> > 
> > > **Beautiful-Hotel-3094** · [2024-12-26](https://reddit.com/r/dataengineering/comments/1hmfxrg/comment/m3x1cna/) · 2 points
> > > 
> > > Non c'è un template, devi solo creare un repository separato per tutto il tuo codice Python e impacchettarlo in un'immagine. Poi, in un repository Airflow separato, usi quell'immagine e Airflow solo per orchestrarlo.

> **homelymonster** · [2024-12-26](https://reddit.com/r/dataengineering/comments/1hmfxrg/comment/m3tzitt/) · 3 points
> 
> Perché non Apache NiFi
> 
> > **\[eliminato\]** · [2024-12-26](https://reddit.com/r/dataengineering/comments/1hmfxrg/comment/m3u8xl5/) · 4 points
> > 
> > Ho letto diverse cose negative, quindi, ad essere onesti, l'avevo scartata come opzione.
> > 
> > Voglio assolutamente continuare a usare Python per i flussi di lavoro perché è lì che il resto del mio ecosistema dati è più robusto. Vedo che i processori Python sono stati aggiunti relativamente di recente. Dovrei andare a cercare.
> > 
> > Edit: Ho scorso la documentazione. Credo ci sia una certa complessità che vorrei evitare. Dato che lo stack sottostante di NiFi è Java, e l'interfaccia Python è un server che comunicherà con il processo Java chiamante (tramite un processo Java invocato per comunicare con il server Python), il mio processo appare come "definisci processo in Python-->stack Java-->invocazioni Python per dati spaziali-->sostituisci l'elaborazione allo stack C sottostante, a volte tramite un wrapper.
> > 
> > Quindi, l'interfaccia sembra buona, ma il lato dati sembra eccessivamente complicato.