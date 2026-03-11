---
id: proj-chatgpt-extractor
name: "ChatGPT Conversation Extractor"
language: python
tier: 2
lifecycle_stage: stable
disposition: publish
score: null
jtbd_score: null
last_assessed: 2026-03-10
last_commit: 2025-07-07
visibility: public
tags: [python, chatgpt, data-export, cli, markdown, osint]
---

# ChatGPT Conversation Extractor

**One-liner:** Extract and archive ChatGPT conversations to searchable markdown files

---

## Identity

- **Problem Statement**: ChatGPT users who export their data get a massive JSON blob with no way to browse, search, or organize their conversations. The export format is opaque and the conversations are trapped in an unusable structure.
- **Target User**: Anyone who exports their ChatGPT data and wants to browse, search, or archive their conversations as readable markdown files. Secondary: OSINT practitioners and researchers who need to analyze conversation exports.
- **Origin Story**: Built to extract and organize personal ChatGPT conversation history for a blog post about fine-tuning GPT on personal writing voice. The tool made the data usable, so it became a standalone project.

## Technical Profile

- **Stack**: Python 3.6+ (standard library only)
- **Architecture**: Single-file CLI tool. Interactive menu system with automatic conversation classification (Project/GPT/Plain). Loads conversations.json, builds metadata index, presents browsing/search/export interface. Exports to markdown with YAML frontmatter or zip archives for batch operations.
- **Dependencies**: None — Python standard library only (json, os, re, zipfile, sys, datetime, dataclasses, typing)
- **Maturity**: Production

## Revenue Potential (JTBD — 12FP-1)

- **Who pays?**: Nobody — this is a free utility
- **What do they pay for?**: N/A
- **Why would they switch?**: Zero-dependency single-file tool that just works. No installation, no config, no accounts.
- **12FP-1 Score**: 0/3
- **Revenue Model**: None
- **Disposition**: Gift

## Current State

- **Last Active**: 2025-07-07
- **Known Issues**: None reported
- **Missing Features**:
  - Sample data for immediate testing out of the box
  - Unit tests for core functionality
- **Technical Debt**:
  - All versions share the same commit date (rapid development sprint)
  - MetadataIndex class referenced but implementation could be more complete
