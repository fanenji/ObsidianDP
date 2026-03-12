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

This is an Obsidian personal knowledge management vault synced via iCloud and backed up to GitHub (`git@github.com:fanenji/Obsidian.git`). It is not a software project — there are no build steps, tests, or package managers.

## Git Workflow

The **obsidian-git** plugin commit and sync on demand with the message format `vault backup: {{date}} - {{hostname}}`. Manual git operations are fine but avoid force-pushing or rebasing since the vault may be open on another device simultaneously. When committing manually, use descriptive messages.

## Folder Numbering System

The vault uses a numbered prefix hierarchy:

- `00 TODO/` — Active task and to-do tracking with Kanban view
- `01 INBOX/` — Inbox for new, unsorted items
  - 'Clippings' - Clipping from web pages via Obsidian Web Clipper
  - 'Journal' - Temporary location for daily and journal notes
- `20 PROJECTS/` — Project folders (geographic/infrastructure projects)
  - `AI/` — AI-related projects (Claude Code, LocalAI, OpenCode, etc.)
  - `OBSIDIAN/` — Obsidian meta-notes
- `30 WIKI/` — Reference and knowledge base notes
  - `AI/` — AI tools and references
  - `OBSIDIAN/` — Obsidian reference docs
  - `TOOLS/` — Notes and docs gor various tools
- `40 NOTE/` — Work and operational notes
  - `MAC/` — macOS-related notes
  - `STEFANO/` — Personal notes (hardware, backups, home lab, etc.)
- `50 IDEE/` — Ideas and exploratory notes (geospatial, ML, tooling)
- `90 ARCHIVE/` — Archived work projects no longer actively used
- `99 System/` — System config, attachments, canvas files
  - `agents/` — Claude Code agents and skills
  - `attachments/` — All binary attachments (images, PDFs, Postman collections, etc.)
  - `canvas/` — Canvas files
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
