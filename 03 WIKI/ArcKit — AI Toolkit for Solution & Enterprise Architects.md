---
title: "ArcKit — AI Toolkit for Solution & Enterprise Architects"
source: "https://medium.com/@davidroliver/arckit-ai-toolkit-for-solution-enterprise-architects-528fa51c7c72"
author:
  - "[[David R Oliver]]"
published: 2026-02-23
created: 2026-03-15
description: "ArcKit — AI Toolkit for Solution & Enterprise Architects These AI-based Architectural tools are used across the UK Government and the NHS. Introduction Every architect has lived through the same …"
tags:
  - "clippings"
topic:
type: "note"
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Mastodon](https://me.dm/@davidroliver)

These AI-based Architectural tools are used across the UK Government and the NHS.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/0*xwL0e9LIFc7DBSZD)

Photo by Anton Savinov on Unsplash

## Introduction

Every architect has lived through the same scene. Halfway through a design review, someone asks: “Didn’t we already decide this?” You know you did. You remember the debate. But the decision is buried in a Confluence page nobody can find, or locked inside someone’s head who left the organisation six months ago.

Architecture governance is supposed to prevent this. In practice, it creates paperwork that nobody maintains. Requirements documents go stale. ADRs sit in “Proposed” limbo for months. Vendor evaluations are repeated because the last one wasn’t captured properly.

ArcKit is an open-source toolkit that changes the economics of governance work. Instead of spending hours formatting documents, you spend minutes generating structured first drafts and hours on the thinking that matters.

## What Is ArcKit?

[ArcKit](https://github.com/tractorjuice/arc-kit) is an MIT-licensed Enterprise Architecture Governance toolkit created by [Mark Craddock](https://medium.com/@mcraddock). It provides over 50 AI-assisted slash commands that generate structured governance artefacts — requirements documents, ADRs, high-level designs, Wardley Maps, vendor evaluations, procurement documents, and UK Government compliance assessments.

It works with multiple AI coding assistants: Claude Code (as a plugin), Google Gemini CLI (as an extension), OpenAI Codex CLI, and OpenCode CLI. The Claude Code integration is the most complete, providing the full suite of commands, autonomous research agents, automation hooks, and bundled MCP servers.

The key insight behind ArcKit is that architecture governance follows repeatable patterns. A requirements document always needs functional requirements, non-functional requirements, data requirements, and integration requirements. An ADR always needs context, decision, consequences, and alternatives considered. A vendor evaluation always needs pricing, capability mapping, and risk assessment. Rather than starting from scratch each time, ArcKit generates comprehensive first drafts that follow these patterns, and then you review and refine.

The important word there is “first draft.” ArcKit does not replace architectural thinking. It removes the friction that stops architects from doing governance properly.

## The ADR Problem — And How ArcKit Solves It

Architecture Decision Records are the canonical example of governance that architects know they should maintain, but rarely do consistently. The friction is real: opening a blank document, remembering the template structure, writing up alternatives you already mentally discarded, documenting consequences you consider obvious. By the time you’ve formatted the document, the meeting has moved on, and the decision lives in someone’s Slack message instead.

ArcKit’s \`/arckit:adr\` command changes this. You describe the decision context in natural language — “We need to choose between Kafka and RabbitMQ for event streaming, considering our existing AWS investment and the team’s Java expertise” — and it generates a structured ADR with:

- A clear context section that frames the problem
- Multiple alternatives with pros, cons, and trade-offs
- A recommended decision with rationale
- Consequences (positive and negative)
- Implementation notes and review dates

The generated ADR follows a deliberate dependency chain. ArcKit expects you to have already generated requirements (via \`/arckit:requirements\`), so the ADR can reference specific requirement IDs. This traceability — decisions linked to requirements, which are linked to stakeholder goals — is the kind of rigour that manual processes almost never achieve.

Beyond ADRs, ArcKit covers the full governance lifecycle:

![](https://miro.medium.com/v2/resize:fit:640/format:webp/0*0jM5obcUC8j0Jmao.png)

Each command follows the same pattern: you provide context in plain language, ArcKit generates a structured artefact using proven templates, and you review and refine.

## Proven in the UK Government and the NHS

ArcKit is not theoretical. It has been widely adopted across the NHS and UK public sector, where governance requirements are particularly demanding, and documentation standards are non-negotiable.

The toolkit includes dedicated UK Government compliance commands:

- /arckit:tcop— Assesses against all 13 points of the B Technology Code of Practice
- /arckit:ai-playbook— Evaluates against the UK Government AI Playbook and Algorithmic Transparency Recording Standard (ATRS)
- /arckit:secure — Generates Secure by Design assessments covering NCSC Cyber Assessment Framework, Cyber Essentials, and UK GDPR
- /arckit:mod-secure— Ministry of Defence Secure by Design with JSP 440, IAMM, and clearance pathways
- /arckit:dpia — Data Protection Impact Assessment for UK GDPR Article 35
- /arckit:sobc — Strategic Outline Business Case following HM Treasury Green Book five-case model
- /arckit:risk — Risk register following HM Treasury Orange Book 2023

Fourteen public demonstration repositories showcase complete deliverable sets for real-world-style projects:

- [NHS Appointment Booking](https://github.com/tractorjuice/arckit-test-project-v7-nhs-appointment) — Digital health platform with NHS Spine integration, GDPR safeguards, GDS Service Standard assessment, and Secure by Design compliance
- [Cabinet Office GenAI Platform](https://github.com/tractorjuice/arckit-test-project-v9-cabinet-office-genai) — Cross-government GenAI platform with responsible AI guardrails  
	[HMRC Tax Assistant](https://github.com/tractorjuice/arckit-test-project-v2-hmrc-chatbot) — Conversational AI service with PII protection and bilingual support
- [ONS Data Platform](https://github.com/tractorjuice/arckit-test-project-v8-ons-data-platform) — Official statistics analytics with Five Safes governance
- [Scottish Courts GenAI](https://github.com/tractorjuice/arckit-test-project-v14-scottish-courts) — Scottish Courts and Tribunals Service GenAI strategy with MLOps and FinOps
- [National Highways Data Architecture](https://github.com/tractorjuice/arckit-test-project-v11-national-highways-data) — Strategic road network data platform
- [UK Government API Aggregator](https://github.com/tractorjuice/arckit-test-project-v19-gov-api-aggregator) — Unified access to 240+ UK Government APIs across 34+ departments

Each repository contains a complete set of artefacts — from principles and stakeholders through requirements, data models, ADRs, and compliance assessments. They demonstrate what consistent governance documentation looks like when the friction of creating it is removed.

For architects working in regulated environments, this matters. An NHS digital service needs GDS Service Standard compliance, DPIA, Secure by Design assessment, and clinical safety evidence. Generating the structure for all of these in an afternoon — rather than spending weeks on formatting — means more time for the substantive clinical and technical thinking that actually protects patients.

## Knowledge Compounds

The real power of ArcKit is not any single command. It is what happens over months of use.

Consider the traditional approach: you write an ADR for Project A’s database selection. Six months later, Project B faces a similar decision. You vaguely remember the first decision but cannot find it, so you start from scratch. The same vendor evaluation, the same trade-off analysis, the same conclusions — all duplicated because your past work was not accessible.

ArcKit’s artefacts are structured Markdown files with consistent naming conventions (\`ARC-ADR-001.md\`, \`ARC-REQ-001.md\`). This means they are searchable, parseable, and — critically — accessible to AI assistants in future sessions.

When you start a new project and run \`/arckit:research\`, the research agent can reference vendor evaluations from previous projects. When you write an ADR, the context includes decisions from related work. Requirements from one project inform non-functional requirements in the next.

This is knowledge compounding. Each artefact you create makes every future artefact slightly better, because the AI has more context about your organisation’s decisions, constraints, and preferences.

The compound effect accelerates over time:

**Month 1:** You generate standalone artefacts. The AI uses its general knowledge.  
**Month 3:** The AI references your previous ADRs and requirements. Vendor evaluations build on earlier research.  
**Month 6:** You have an organisational corpus. New architects can query it. Patterns emerge across projects.  
**Month 9:** The corpus becomes a competitive advantage. Governance that once took weeks takes hours, and the quality is higher because it builds on accumulated institutional knowledge.

ArcKit supports this with cross-session memory via the Model Context Protocol (MCP) memory server, which stores key decisions, vendor insights, and lessons learned across sessions. When you start a new session, the AI surfaces relevant context from previous work, so you don't need to remember where anything lives.

For teams adopting ArcKit, this means new joiners inherit the team’s accumulated knowledge from day one. Instead of spending their first months building context by reading old documents, they ask questions and the AI surfaces relevant decisions, patterns, and lessons.

## Security is a Priority

Architects deal with sensitive information daily — system designs, security assessments, vendor pricing, and internal network topologies. Any tool that processes this information must take security seriously.

### Skills: Controlled Generation

ArcKit’s 51 slash commands are implemented as skills — structured Markdown templates that define what the AI generates. Each skill specifies the output format, required inputs, and validation criteria. This is not free-form prompting; it is constrained generation that produces predictable, auditable outputs.

Skills follow a deliberate dependency sequence. You cannot generate a meaningful ADR without requirements to reference. You cannot produce a design review without a design to review. This dependency chain is not just good practice — **it prevents the AI from hallucinating nonexistent context**.

### Hooks: Automated Safety Nets

Hooks are scripts that execute automatically at specific points in the AI workflow. ArcKit includes automation hooks for:

- Session initialisation — Loads project context so the AI understands what it is working on
- Project context injection — Automatically provides relevant state from previous sessions
- Filename enforcement — Validates that generated artefacts follow naming conventions
- Output validation — Checks generated content against expected structure (e.g., validates Wardley Map coordinates are mathematically consistent)

Beyond the built-in hooks, the community has contributed security-focused hooks that prevent common risks:

- File protection — Blocks writes to sensitive files (\`.env\`, credentials, configuration files with secrets). Uses a three-layer detection model: path-based rules, keyword matching, and regex content scanning
- Secret detection — Scans user prompts for API keys, tokens, and passwords before they reach the AI. Catches patterns for OpenAI, Anthropic, GitHub, AWS, Slack, and other common services
- Secret file scanning — Examines content being written to files, blocking anything that contains credential patterns

These hooks execute locally, before any data leaves your machine. If you accidentally paste an API key into your prompt, the hook blocks it before it reaches the AI model. If the AI tries to write a file containing a hardcoded password, the hook prevents the write.

The security model follows a principle of defence in depth: even if one layer misses something, the next layer catches it. Path-based rules catch obvious cases (writing to \`.env\`). Keyword matching catches less obvious cases (a file named \`production-config.yaml\`). Regex scanning catches the cases where sensitive content appears in otherwise innocent files.

### Plugins: Extending Safely

ArcKit integrates with Claude Code as a plugin, which means it operates within Claude Code’s existing permission model. Users approve tool access, sandbox restrictions limit file system writes, and MCP servers provide controlled access to external services.

The bundled MCP servers (AWS Knowledge, Microsoft Learn, Google Developer Knowledge) provide read-only access to vendor documentation. They do not send your project data to these services — they fetch public documentation to inform research and technology evaluations.

For organisations requiring the strongest data-handling guarantees, ArcKit works with Claude Code, configured for AWS Bedrock. In this mode:

- Zero data retention — Prompts and responses are not stored after processing
- No training — Your artefacts never train AI models
- UK data sovereignty — Run in \`eu-west-2\` (London) for UK data residency
- VPC endpoints — Private connectivity with no internet exposure
- Full audit logging — CloudTrail integration for compliance evidence

This combination — structured skills that constrain generation, hooks that prevent data leakage, and Bedrock for zero-retention processing — addresses the data handling concerns that have historically blocked AI adoption in regulated environments.

## Using ArcKit with Claude Code

### Installation

ArcKit installs as a Claude Code plugin with a single command:

```c
claude /plugin marketplace add tractorjuice/arc-kit
```

This makes all 51 commands available in any Claude Code session. The plugin includes hooks that automatically load the project context when you start working in a project directory.

### Your First Project

Create a project directory and start generating artefacts:

```c
mkdir -p ~/arc-projects/my-first-project
cd ~/arc-projects/my-first-project
claude
```

Inside Claude Code:

```c
/arckit:principles # Define architecture principles
/arckit:stakeholders # Map stakeholders, drivers, and goals
/arckit:requirements # Generate requirements (FR, NFR, DR, INT)
/arckit:data-model # Create data model with GDPR matrix
/arckit:adr # Document architecture decisions
/arckit:diagram # Generate architecture diagrams
/arckit:hldr # Run a formal HLD review
```

Each command creates structured Markdown files in a \`projects/\` directory. The files follow consistent naming conventions (\`ARC-PRIN-001.md\`, \`ARC-REQ-001.md\`, \`ARC-ADR-001.md\`) and cross-reference each other.

### UK Government Compliance

For public sector projects, add compliance assessments:

```c
/arckit:tcop # Technology Code of Practice (all 13 points)
/arckit:secure # Secure by Design (NCSC CAF, Cyber Essentials, UK GDPR)
/arckit:dpia # Data Protection Impact Assessment
/arckit:sobc # Strategic Outline Business Case (Green Book)
/arckit:risk # Risk register (Orange Book)
/arckit:ai-playbook # AI Playbook + ATRS assessment
```

### Research and Procurement

ArcKit includes commands for technology research and procurement:

```c
/arckit:research # Technology evaluation with web search
/arckit:research-aws # AWS-specific research
/arckit:research-azure # Azure-specific research
/arckit:rfp # Generate Request for Proposal
/arckit:sow # Generate Statement of Work
/arckit:gcloud # Search G-Cloud marketplace
/arckit:vendor # Vendor capability evaluation
```

The research commands use bundled MCP servers to access current vendor documentation, so evaluations reflect the latest service offerings rather than the AI’s training data cutoff.

### Autonomous Research Agents

For deeper analysis, ArcKit provides five autonomous research agents (Claude Code only). These agents work through multi-step research workflows without requiring constant direction:

```c
/arckit:deep-research # Extended technology evaluation
/arckit:wardley # Wardley Map strategic analysis
```

The agents follow structured processes — gathering requirements, searching documentation, evaluating alternatives, and producing formatted deliverables — while you focus on other work.

## Complementary Tools: ArcKit and Knowledge Vaults

ArcKit generates governance artefacts for specific projects. It answers “what did we decide for Project X?” But architecture knowledge also needs a persistent home — somewhere that captures patterns, concepts, and institutional knowledge that transcends individual projects.

Tools like [ArchitectKB](https://github.com/DavidROliverBA/ArchitectKB) fill this complementary role. Where ArcKit handles the governance process (requirements, procurement, reviews), a knowledge vault handles persistent knowledge (ADRs, concepts, patterns, people, meetings). The two work together: ArcKit generates structured artefacts, and you distil the insights into your knowledge vault, where they compound over time.

The separation matters. Governance artefacts have a lifecycle — they are created, reviewed, approved, and eventually superseded. Knowledge persists. The pattern you identified in Project A’s vendor evaluation is relevant to Project B’s technology selection, even though the original governance artefacts have moved on.

## Getting Started

ArcKit is free, open source, and takes five minutes to install. Here is a suggested path:

1\. **Install the plugin** — \`claude /plugin marketplace add tractorjuice/arc-kit\`  
2\. **Explore a demo project** — Clone one of the [14 demonstration repositories](https://github.com/tractorjuice?tab=repositories&q=arckit-test-project) to see what complete governance looks like  
3\. **Start a real projec** t— Pick a current piece of work and generate principles, requirements, and an ADR  
4\. **Add compliance** — If you are in the public sector, run the TCoP and Secure by Design assessments  
5\. **Build the habit** — Every new decision gets an ADR. Every vendor evaluation uses the research command. Let the artefacts compound

The friction of governance work is the reason most organisations do not do it well. ArcKit removes that friction. The thinking — the actual architecture — is still yours. ArcKit just makes it feasible to capture it consistently.

I write about where knowledge and solution architecture meet to design and build the systems of the future.
