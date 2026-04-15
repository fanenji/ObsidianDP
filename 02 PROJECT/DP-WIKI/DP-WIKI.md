---
type: note
topic:
created: 2026-04-12
tags: []
---



## PROMPT

```
Obiettivo: costruire una wiki contenente la knowledge base per il progetto Data Platform

Lo spunto è l'articolo di Andej Karpathy 'LLM Knowledge Bases Thread by @karpathy.md' e il successivo gist 'Karpathy llm-wiki Gist.md' che trovi nella dir corrente: leggi e analizza i documenti di Karpathy.
Nella directory /examples invece trovi una serie di esempi di utilizzo da parte di alcuni utenti da cui puoi prendere spunto se ci sono cose che ritieni interessanti per il mio caso.

Il focus di questa wiki è relativo alla definizione e implementazione della architettura e dei processi della Data Platform

La directory /raw è già presente e contiene il materiale iniziale.
Il materiale della raw può essere in diversi formati:
- markdown
- pdf
- epub
- video
- immagini
Il materiale è di due tipologie diverse 
1. Libreria di articoli / video / libri su argomenti riguardanti le data platform
2. Note e documentazione di progetto
	- documentazione tecnica
	- documentazione utente
	- adr log
	- diagrammi architetturali
	- resoconti meeting
- Questo è importante perchè i documenti della libreria sono immutabili e nel tempo vengono semplicemente aggiunti nuovi documenti, mentre le note e la documentazione di progetto è in continuo divenire e  cambia nel tempo, serve un meccanismo di aggiornamento della wiki che tenga conto di questo

Questa è una lista provvisoria di funzionalità del sistema (da discutere e approfindire in fase di pianificazione):
		- ingestion in modalità bulk di nuovo materiale presente in /raw non ancora elaborato e incluso nella wiki (per esempio per ingestion iniziale del sistema)
		- ingestion di nuovo materiale per singolo documento a partire da URL (pagine html e PDF): salvataggio materiale grezzo nella dir /raw e successiva elaborazione per includere i contenuti nella /wiki  
		- elaborazione o rielaborazione di singolo file nella dir /raw  
		- trascrizione di video da link youtube -> salvataggio in /raw -> processamento nella wiki
		- trascrizioni meeting 
		- una pagina per ogni entità della wiki con sommario e cross-reference con source 
		- backlinks tra le varie entità (grafo)
		- costruzione di un glossario di riferimento
		- linting (check e controlli) (contraddizioni / orfani / cose importanti senza una pagina / inconsistenze)
		- funzione di ricerca di materiale 
		- salvataggio nella wiki di risposte interessanti a seguito di una ricerca / domanda   
		- log di ogni attività svolta

Mi piacerebbe inoltre un aiuto per: suggerimenti, evidenziare incongruenze o problemi, avere nuovi insight, produrre sintesi di documentazione

Analizza i documenti di Karpathy e gli esempi in examples e chiedimi tutto quello che non ti è chiaro e che manca, poi prepara un piano dettagliato prima di implementare la soluzione.

```

## TODO
- Creare /raw e caricare documenti
	- DP 03 WIKI [OK]
	- DP 02 PROJECT [OK]
	- Libri Calibre [OK]
	- documenti / diagrammi su wiki gitlab
	- documenti nextcloud




---

## LLM Wiki has three parts
1. **Raw sources** — A folder called `raw/`. This is where you put your documents — PDFs, markdown files, clipped articles, transcripts. The AI reads from this folder but never changes anything in it. Your originals stay exactly as they are.
2. **The wiki** — A folder called `wiki/`. The AI creates and owns everything in this folder. It builds pages, maintains cross-references, keeps a glossary, and updates an index. You browse it; the AI writes it.
3. **The schema** — A single file called `CLAUDE.md`. This is the instruction manual for the AI. It defines what types of pages exist, what workflow to follow when processing a new source, how to format pages, and when to check the wiki for problems. Think of it as the rulebook that turns a general-purpose AI into a disciplined wiki maintainer.

## Three operations
**Ingest:** You drop a document into `raw/` and tell the AI to process it. The AI reads it, creates summary pages, updates entity pages across the wiki, adds new terms to the glossary, updates the index, and logs what it did. A single source can touch 10-15 wiki pages.
**Query:** You ask questions. The AI reads the wiki (not the raw files) to put together answers. Good answers can be saved back into the wiki as analysis pages, so your questions make the knowledge base richer over time.
**Lint:** You ask the AI to health-check the wiki. It finds contradictions, stale information, orphan pages with no links, and missing cross-references. Think of it as spell-check for your knowledge base.