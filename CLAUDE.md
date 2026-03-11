# ChatGPT Conversation Extractor — Guidelines

## Project Overview

Single-file Python tool that extracts, filters, and exports ChatGPT conversations from OpenAI data exports (`conversations.json`) to markdown files or zip archives. Zero external dependencies — uses only the Python standard library.

**Key file:** `extract_gpt_conversations.py` (the entire tool)

## Using This Tool with Claude

If you're an AI assistant (Claude, etc.) helping a user with this project, here's how to operate it:

### Running the Script

```bash
# Interactive mode (default) — presents a menu
python extract_gpt_conversations.py

# Specify a custom conversations.json path
python extract_gpt_conversations.py --file /path/to/conversations.json

# Check version
python extract_gpt_conversations.py --version
```

### What It Expects

- **Input:** A `conversations.json` file from ChatGPT's data export (Settings > Data Controls > Export Data)
- **Output:** Markdown files in `output_conversations/` directory, or zip archives for batch exports
- **Python:** 3.6+ (uses dataclasses and type hints)

### How to Help Users

1. **Getting their data:** Guide users to export from ChatGPT: Settings > Data Controls > Export Data. OpenAI emails a download link. The zip contains `conversations.json`.

2. **Running the tool:** The script is interactive. It loads conversations, classifies them (Project/GPT/Plain), and presents a menu. Users browse by category, list sequentially, or fuzzy-search by keyword.

3. **Exporting:** Users can export individual conversations to markdown or batch-export to zip. Output lands in `output_conversations/`.

4. **Troubleshooting:** If the script can't find `conversations.json`, use `--file` to point at it. The file must be valid JSON from OpenAI's export format.

### Programmatic Integration

The script is designed for interactive CLI use. To integrate into automated workflows:

- The main entry point is `main()` at the bottom of the script
- Core functions are modular: `extract_messages()`, `generate_markdown_content()`, `export_conversations_to_zip()`
- Data classes (`MessageData`, `ConversationData`, `ExportData`) define the data model
- Classification logic in `classify_convo()` uses `memory_scope` and `gizmo_id` fields

### Output Format

Exported markdown files include YAML frontmatter:

```markdown
---
title: "Conversation Title"
category: "Project"
timestamp: "2024-01-27_14-30-00"
id: "abc123-def456"
---

# Conversation Title

**USER:**
Message content...

**ASSISTANT:**
Response content...
```

File naming: `{CATEGORY}-{TIMESTAMP}-{TITLE}__{ID}.md`

## Architecture

- **Single file:** Everything lives in `extract_gpt_conversations.py`
- **No dependencies:** Python standard library only (json, os, re, zipfile, sys, datetime, dataclasses, typing)
- **Classification:** Three categories — Project (code/technical), GPT (AI assistants), Plain (everything else)
- **Performance:** Metadata caching with SHA1 hash validation for change detection

## Git Workflow

### Branch Naming Convention

| Range | Purpose | Example |
|-------|---------|---------|
| `0xx-name` | Features | `010-sample-data` |
| `3xx-name` | Fixes and polish | `300-docs-polish` |
| `5xx-name` | Research & POCs (never merge) | `500-experiment` |

### Rules

- Never commit directly to main
- Rebase before merge (linear history)
- Fast-forward merges only (`--ff-only`)

## Key Decisions

- **Single-file architecture:** Intentional simplicity — the tool is one script you can drop anywhere
- **No external dependencies:** Maximizes portability — runs on any system with Python 3.6+
- **Interactive CLI:** Designed for human exploration of conversation history, not batch automation
- **Three-category classification:** Project/GPT/Plain covers the useful groupings without over-categorizing
