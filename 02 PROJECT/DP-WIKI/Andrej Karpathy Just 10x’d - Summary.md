---
type: note
topic:
created: 2026-04-12
tags: []
---

The video explains how to implement Andrej Karpathy’s “LLM wiki” idea using Claude Code and Obsidian to turn raw documents (like YouTube transcripts or articles) into a linked markdown knowledge base that acts as a persistent second brain.[](https://www.youtube.com/watch?v=sboNwYmH3AY&vl=it)

## Core idea

Karpathy’s method is to feed raw text (PDFs, articles, transcripts) into Claude Code, which auto‑builds a markdown “wiki” with pages, indexes, and links instead of using a traditional vector database RAG stack. The LLM maintains index files, brief summaries, and relationships between concepts, people, tools, and sources, so you can query and explore via links rather than similarity search.[](https://www.youtube.com/watch?v=sboNwYmH3AY&vl=it)

## What Nate builds

Nate shows two concrete wikis: one for 36 of his recent YouTube videos and one as his personal second brain with meeting notes, business context, and planning. In Obsidian, each vault has a simple structure: a top‑level folder, a `raw` folder for source documents, and a `wiki` folder where Claude writes structured pages, an index, a log, and a `claw.md` project spec.[](https://www.youtube.com/watch?v=sboNwYmH3AY&vl=it)

## Setup and ingest workflow

He installs Obsidian as the visual front end, creates a new vault, and opens that folder in VS Code where he runs Claude Code from the terminal. He pastes Karpathy’s LLM‑wiki gist plus a wrapper prompt that tells Claude “you are my LLM wiki agent” and asks it to create the schema, raw/wiki folders, index, log, and `claw.md` automatically.[](https://www.youtube.com/watch?v=sboNwYmH3AY&vl=it)

To ingest content, he uses the Obsidian Web Clipper to save an article (the AI 2027 essay) directly into the `raw` folder, then tells Claude to “ingest” it. Claude reads the source, asks clarifying questions (what to emphasize, how granular to be, what the project is for), then splits it into multiple wiki pages (people, orgs, concepts, analysis, etc.) and wires up relationships that appear in Obsidian’s graph view.[](https://www.youtube.com/watch?v=sboNwYmH3AY&vl=it)

## How it’s used and integrated

For his YouTube vault, he batch‑ingested 36 transcripts in ~14 minutes, which produced about 23 wiki pages, plus typed entities like people, organizations, AI systems, and concepts with rich cross‑links. For the second‑brain vault, he adds meeting recordings, ClickUp summaries, and other business notes, and his “Herk 2” executive‑assistant agent reads from this wiki (via a configured path and instructions in `claw.md`) only when it needs persistent context.[](https://www.youtube.com/watch?v=sboNwYmH3AY&vl=it)

He also uses a “hot cache” file (e.g., `hot.md`) in the second‑brain wiki to store the most recent ~500 characters of context, so the agent can answer many follow‑ups without re‑crawling the whole wiki, which also reduced token usage versus his old “context files” approach.[](https://www.youtube.com/watch?v=sboNwYmH3AY&vl=it)

## LLM wiki vs traditional RAG

Nate summarizes the tradeoffs: the LLM wiki finds information by following indexes and links, giving deeper relationship understanding, while classic semantic‑search RAG uses embeddings and vector similarity. The wiki requires only markdown files (Obsidian optional) and tokens, whereas RAG needs an embedding model, vector DB, and chunking pipeline but scales better to millions of documents.[](https://www.youtube.com/watch?v=sboNwYmH3AY&vl=it)

For “hundreds of pages with good indexes,” the wiki works well and can cut token costs dramatically (one user cut ~95% when moving from scattered files to a wiki). For very large, enterprise‑scale corpora, he notes you still likely need traditional RAG, knowledge graphs, or similar infrastructure, at least with current models as of April 2026.