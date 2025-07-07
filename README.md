# ChatGPT Conversation Extractor

A Python script to extract, filter, and archive ChatGPT conversations from OpenAI data exports. This tool provides an interactive interface to browse, search, and export your ChatGPT conversations to markdown files or zip archives.

## Blog
[Fine-Tuning GPT on My Voice](https://0xsalt.github.io/posts/train_gpt_to_write/)

## Features

- **Interactive Menu System**: Browse conversations by category (Project, GPT, Plain)
- **Smart Classification**: Automatically categorizes conversations based on content
- **Fuzzy Search**: Search conversations by keyword in titles
- **Batch Export**: Export multiple conversations to zip files
- **Metadata Indexing**: Performance optimization with lazy loading
- **Markdown Export**: Clean, formatted output with frontmatter
- **No Dependencies**: Uses only Python standard library

## Quick Start

### Prerequisites
- Python 3.6 or higher
- Your ChatGPT export file (`conversations.json`)

### Setup
1. Download `extract_gpt_conversations.py`
2. Install dependencies (optional, for development/testing):
   ```bash
   pip install -r requirements.txt
   ```
3. Place your `conversations.json` file in the same directory
4. Run the script:
   ```bash
   python extract_gpt_conversations.py
   ```

### Usage Examples

**Basic usage (default file location):**
```bash
python extract_gpt_conversations.py
```

**Specify custom file location:**
```bash
python extract_gpt_conversations.py --file /path/to/your/conversations.json
```

**Get help:**
```bash
python extract_gpt_conversations.py --help
```

## How It Works

### 1. Data Loading & Processing
The script loads your `conversations.json` file and processes each conversation to extract:
- Title and metadata
- Message content and authors
- Timestamps and conversation IDs
- Automatic categorization

### 2. Interactive Menu
```
Select category to browse:
0: Project
1: GPT  
2: Plain
3: List all chats sequentially ASC
4: List all chats sequentially DESC
5: Fuzzy search by keyword
```

### 3. Conversation Classification
Conversations are automatically classified into three categories:
- **Project**: Contains code, technical discussions, or project-related content
- **GPT**: Conversations with GPT assistants or AI-related topics
- **Plain**: General conversations and other content

### 4. Export Options
- **Single Export**: Extract individual conversations to markdown files
- **Batch Export**: Export multiple conversations to zip archives
- **Fuzzy Search Export**: Export all matching conversations from keyword search

## Output Format

### Markdown Files
Exported conversations include:
- YAML frontmatter with metadata
- Formatted message content
- Author attribution
- Timestamps and conversation IDs

Example output:
```markdown
---
title: "Code Review Discussion"
category: "Project"
timestamp: "2024-01-27_14-30-00"
id: "abc123-def456"
---

# Code Review Discussion

**USER:**
Can you review this Python function?

**ASSISTANT:**
I'll analyze the code for you...
```

### File Naming Convention
- Individual files: `{CATEGORY}-{TIMESTAMP}-{TITLE}__{ID}.md`
- Zip archives: `{TIMESTAMP}-fuzzy_matches_{KEYWORD}.zip`

## Performance Features

### Metadata Indexing
The script creates a `.metadata` file to cache conversation information:
- SHA1 hash validation for change detection
- Pre-processed conversation metadata
- Lazy loading for optimal performance

### Lazy Loading
- **Display operations**: Use cached metadata (fast)
- **Export operations**: Load raw data only when needed
- **Performance improvement**: ~40% faster for large files

## Advanced Usage

### Fuzzy Search
Search for conversations by keyword:
```
Enter keyword to search for (case-insensitive, title match): python
```

### Batch Operations
Export multiple conversations at once:
```
Enter a number to extract one, or type 'zip' to export all to a zip: zip
```

### Range Selection
Browse conversations in chunks:
```
How many at a time or what range? [e.g., 10, or 50-100, or {ENTER} for all]: 20
```

## File Structure

```
your-directory/
├── extract_gpt_conversations.py    # Main script
├── conversations.json              # Your ChatGPT export
├── output_conversations/           # Generated output directory
│   ├── PROJECT-2024-01-27_14-30-00-Code_Review__abc123.md
│   ├── 2024-01-27_14-30-00-fuzzy_matches_python.zip
│   └── ...
└── conversations.json.metadata     # Performance cache (auto-generated)
```

## Troubleshooting

### Common Issues

**"File not found" error:**
- Ensure `conversations.json` is in the same directory as the script
- Use `--file` flag to specify custom path

**"Invalid JSON" error:**
- Verify your export file is complete and not corrupted
- Re-export from ChatGPT if needed

**Performance issues with large files:**
- The script automatically creates metadata cache for better performance
- First run may be slower, subsequent runs will be faster

### Error Handling
The script includes comprehensive error handling for:
- File operations
- JSON parsing
- User input validation
- Export operations

## Technical Details

### Dependencies
- **Python Standard Library Only**: No external packages required
- **Python 3.6+**: Uses modern Python features like dataclasses and type hints

### Architecture
- **Modular Design**: Separated concerns for maintainability
- **Type Safety**: Full type annotations for reliability
- **Error Handling**: Comprehensive exception management
- **Performance Optimization**: Metadata caching and lazy loading

### Data Structures
- `MessageData`: Individual message representation
- `ConversationData`: Conversation metadata
- `ExportData`: Export operation data
- `MetadataIndex`: Performance optimization cache

## License

MIT License - see the script header for full license text.

## Contributing

This script is designed to be self-contained and easy to use. If you find bugs or have feature requests, please open an issue on the repository.

## Roadmap

Planned features for upcoming releases:

- [ ] Include sample data for immediate testing out of the box
- [ ] Implement unit tests for core functionality

## Version History

- **v1.3.1**: Implemented lazy loading for better performance
- **v1.3.0**: Added metadata indexing for performance optimization
- **v1.2.0**: Improved error handling and user interface
- **v1.1.0**: Added fuzzy search and batch export
- **v1.0.0**: Initial release with basic extraction functionality

---

**Note**: This script processes your personal ChatGPT export data which may contain sensitive or private conversations.
