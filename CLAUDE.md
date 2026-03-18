# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

This is an Obsidian vault. Key conventions:
- Notes use YAML frontmatter
- Cross-links use [[wikilink]] syntax
- Templater plugin is used for auto-insertion
- Do not assume plugin capabilities without checking documentation first
- Use the Obsidian CLI whenever possible

## What This Repository Is

This is an Obsidian personal knowledge management vault synced via iCloud and backed up to GitHub (`git@github.com:fanenji/ObsidianDP.git`). 
The vault contains the knowledge regarding a Data Engineering project called "Data Platform".
Data Platform is a Data Lakehouse based on the "Modern Data Stack" paradigm.
The architecture is brefly described in the document: [[Sintesi Architettura (Claude)]]
It is not a software project — there are no build steps, tests, or package managers.

## Git Workflow

The **obsidian-git** plugin commit and sync on demand with the message format `vault backup: {{date}} - {{hostname}}`. Manual git operations are fine but avoid force-pushing or rebasing since the vault may be open on another device simultaneously. When committing manually, use descriptive messages.

## Folder Numbering System

The vault uses a numbered prefix hierarchy:

- `00 TODO/` — Active task and to-do tracking with Kanban view
- `01 INBOX/` — Inbox for new, unsorted items
  - 'Clippings' - Clipping from web pages via Obsidian Web Clipper
  - 'Journal' - Temporary location for daily and journal notes
- `02 PROJECT/` — Raccoglie le note relative al progetto Data Platform
  - `MAPPING/` — Note relative alle procedure di ingestion dei dati cartografici
  - `MEETING/` — Note riassuntive dei meeting effettuati
  - `OPENDATA/` — Note relative all'integrazione della DP con il sistema OpenData
  - `PROCESS/` — Note relative al processo di ELT e alla sua gestione (CI/CD)
  - `TOOLS/` — Note relative agli strumenti software utilizzati (dbt, OpenMetadata, ecc.)
- `03 WIKI/` — Reference and knowledge base notes
  - `AI/` — Documentazione sull'uso di strumenti AI in ambito data platforms
  - `DATA QUALITY/` — Documentazione su Data Quality (strumenti e pratiche) 
  - `MAPPING/` — Documentazione relativa all'integrazione della DP con l'infrastruttura di gestione dei dati cartografici 
  - `TOOLS/` — Documentazione relativa a vari strumenti software utilizzati (dbt, Dremio, ecc.)
- `90 ARCHIVE/` — Archived notes no longer actively used
- `99 System/` — System config, attachments, canvas files
  - `attachments/` — All binary attachments (images, PDFs, Postman collections, etc.)
  - `scripts/` — Scripting files
- `Templates/` — Note templates (canonical location)
  - `Bases/` — Bases templates

## Templates

Templates live in `Templates/`. When creating a new note from a template, use the Templater plugin (hotkey: configured in `.obsidian/hotkeys.json`).

## Attachments

All attachments go to `99 System/attachments/` (configured in `.obsidian/app.json` as `attachmentFolderPath`).

## Key Obsidian Settings

- Links update automatically on file rename (`alwaysUpdateLinks: true`)
- Delete confirmation is disabled (`promptDelete: false`)
- ZK Prefixer creates journal notes in `00 INBOX/` with timestamp format `YYYY-MM-DD HHmm`

## Community Plugins

Four community plugins are installed (managed via `.obsidian/plugins/`):
- **obsidian-git** — Automated git backups
- **folder-notes** — Folder overview notes (like Notion)
- **terminal** — Embedded terminal with zsh on macOS
- **tasks** — Track tasks
- **task-list-kanban** — Organize tasks in a kanban view
- **omnisearch** — Search engine
- **tasks** — Track tasks

Do not install, remove, or modify plugins by editing plugin files directly — use the Obsidian UI or the Obsidian CLI.

## Python Scripts

When writing Python scripts, handle edge cases proactively: empty collections, missing/null fields, duplicates, and nested structures. Test with edge cases before presenting as complete.
