---
type: note
topic:
created: 2026-04-12
tags: []
---
https://www.youtube.com/watch?v=v1suC9lWJ2I


The video shows how Allie K. Miller built “Claudeopedia,” a Claude Code–driven knowledge management system that lives in Obsidian, with a visual “jellyfish” graph front-end and automated ingestion workflows.[](https://cs50.harvard.edu/x/gallery/)

## Core idea of Claudeopedia

- Allie uses Claude Code plus Obsidian to create a **live** wiki of AI-related knowledge stored as real markdown files on her laptop.[](https://cs50.harvard.edu/x/gallery/)
    
- The system auto-extracts entities (people, tools, concepts), builds cross-references, flags contradictions, and renders an interactive HTML graph (“jellyfish”) you can explore from the desktop.[](https://cs50.harvard.edu/x/gallery/)
    

## The /wiki ingestion workflow

- She shows a `/wiki` terminal shortcut where she pastes a URL (e.g., a Forbes article about using Claude Co‑work) or a PDF (Claude Mythos system card) to ingest.[](https://cs50.harvard.edu/x/gallery/)
    
- Claude fetches the content (via link-reading or a Chrome plugin), generates a note title, creates tags (e.g., Claude Co‑work, Allie, tutorial, founder), timestamps it, and stores raw source text plus processed entity pages in Obsidian folders.[](https://cs50.harvard.edu/x/gallery/)
    
- After ingestion, Claude updates related entity files (e.g., the Claude Co‑work note, Allie’s note, index), summarizes key insights, notes “first time seen” facts, and checks for contradictions between sources, reporting if it finds none.[](https://cs50.harvard.edu/x/gallery/)
    

## Entity pages, cross-links, and visualization

- Each entity (e.g., Dario, Claude Co‑work, Claude Mythos, Project Glasswing, model welfare) has its own Obsidian page with key views, summaries, and cross-references to all sources that mention it.[](https://cs50.harvard.edu/x/gallery/)
    
- The HTML jellyfish visualization reads those markdown files and renders nodes for entities and edges for relationships; selecting a node shows a preview and lets her open the full Obsidian note.[](https://cs50.harvard.edu/x/gallery/)
    
- She repeatedly refreshes the visualization as new sources are ingested, debugging when node counts or edges (e.g., linking Jodie Cook and Claude Co‑work) lag behind the underlying Obsidian data.[](https://cs50.harvard.edu/x/gallery/)
    

## Automation: YouTube, transcripts, and “wiki-last-30”

- For YouTube links, she configured the system so that whenever Claude sees a YouTube URL, it automatically runs a script to grab the transcript, saves it as raw text, and then processes it into the wiki.[](https://cs50.harvard.edu/x/gallery/)
    
- She demonstrates ingesting an Amanda Askell video on model welfare, which creates a new Amanda Askell entity page, links it to existing concepts like model welfare, and updates the graph edges.[](https://cs50.harvard.edu/x/gallery/)
    
- A second skill, `/wiki-last-30`, is adapted from Matt Van Horn’s “last 30 days” repo: run via cron once a week (when her laptop is open), it pulls the last 30 days of AI news and ingests it into Claudeopedia automatically.[](https://cs50.harvard.edu/x/gallery/)
    

## Credits and design influences

- She credits Anthropic (Claude/Claude Code) as the core engine, Andrej Karpathy for the original LLM wiki structure (entities, contradiction checks, Obsidian layout), and Matt Van Horn for the last-30-days skill.[](https://cs50.harvard.edu/x/gallery/)
    
- Allie calls the visualization the “jellyfish,” mentions iterating on layout (too vertical vs wider spread), and jokes about legends, visual polish, and the inherent chaos of working with these systems.