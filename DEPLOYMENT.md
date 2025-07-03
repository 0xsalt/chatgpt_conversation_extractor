# Deployment Guide

This guide explains how to package and deploy the ChatGPT Conversation Extractor script.

## Minimal Package

To run the script on any system, you only need **2 files**:

### Required Files
1. **`extract_gpt_conversations.py`** - The main script
2. **`conversations.json`** - Your ChatGPT export file

### Optional Files (for GitHub repo)
- **`README.md`** - Documentation (this file)
- **`DEPLOYMENT.md`** - This deployment guide
- **`LICENSE`** - MIT license file

## Dependencies

**No external dependencies required!** The script uses only Python standard library modules:

- `json` - JSON parsing
- `os` - File system operations
- `re` - Regular expressions
- `zipfile` - ZIP archive creation
- `sys` - System operations
- `datetime` - Date/time handling
- `dataclasses` - Data structures
- `typing` - Type hints

## Python Version Requirements

- **Minimum**: Python 3.6+
- **Recommended**: Python 3.8+

## Deployment Steps

### 1. Single User Deployment
```bash
# Create directory
mkdir chatgpt-extractor
cd chatgpt-extractor

# Copy files
cp extract_gpt_conversations.py .
cp conversations.json .

# Run script
python extract_gpt_conversations.py
```

### 2. GitHub Repository Deployment
```bash
# Clone or download repository
git clone <repository-url>
cd chatgpt-extractor

# Add your conversations.json file
cp /path/to/your/conversations.json .

# Run script
python extract_gpt_conversations.py
```

### 3. Distribution Package
Create a zip file containing:
```
chatgpt-extractor/
├── extract_gpt_conversations.py
├── README.md
├── DEPLOYMENT.md
└── LICENSE
```

Users then add their own `conversations.json` file.

## File Permissions

Ensure the script is executable:
```bash
chmod +x extract_gpt_conversations.py
```

## Testing Deployment

Before distributing, test the minimal package:

1. Create a clean directory
2. Copy only `extract_gpt_conversations.py`
3. Add a test `conversations.json` file
4. Run the script and verify all features work

## Performance Considerations

### Large Files
- Files >100MB may take longer to process initially
- Metadata caching improves subsequent runs
- Consider splitting very large exports if needed

### Memory Usage
- Script loads entire JSON file into memory
- For very large files (>500MB), consider processing in chunks

## Troubleshooting Deployment

### Common Issues
1. **Python not found**: Ensure Python 3.6+ is installed
2. **Permission denied**: Make script executable with `chmod +x`
3. **File not found**: Verify `conversations.json` is in the same directory

### Platform-Specific Notes
- **Windows**: Use `python` or `python3` command
- **macOS**: May need to use `python3` explicitly
- **Linux**: Should work with `python` or `python3`

## Security Considerations

- The script processes personal data
- No data is sent to external services
- All processing happens locally
- Generated files contain conversation content

## License Distribution

Include the MIT license when distributing:
- Copy the license text from the script header
- Or include a separate `LICENSE` file
- Ensure license attribution is maintained 