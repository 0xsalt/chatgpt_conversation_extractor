# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.1] - 2025-01-27

### Fixed
- Exception handling bug where successful operations were incorrectly reported as errors (CHATGPT-003)
- Proper exception re-raising for `UserExitError` in nested try-catch blocks
- Test output now shows positive results instead of warning messages

## [1.3.0] - 2025-01-27

### Added
- Comprehensive exception handling system (CHATGPT-003)
- Custom exception classes: `ConversationProcessingError`, `FileOperationError`, `InputValidationError`, `ExportError`, `UserExitError`
- Main function with proper exception handling structure
- Keyboard interrupt handling (Ctrl+C)
- Proper exit codes for different error conditions

### Changed
- Replaced all `exit()` calls with proper exception handling
- Improved error messages with meaningful context

## [1.2.0] - 2025-01-27

### Added
- Centralized input validation functions (CHATGPT-002)
- `validate_menu_choice()` for menu option validation
- `validate_numeric_input()` with range checking
- `validate_range_input()` for range format validation
- `get_validated_input()` with retry logic and user-friendly error messages

### Changed
- Improved error messages with consistent formatting
- Enhanced robustness against invalid user input

## [1.1.0] - 2025-01-27

### Changed
- Extracted repeated message extraction logic into `extract_messages()` function (CHATGPT-001)
- Created `generate_markdown_content()` for consistent markdown generation
- Added `export_conversations_to_zip()` for unified zip export functionality
- Eliminated code duplication across multiple export paths

## [1.0.0] - 2025-01-27

### Added
- Initial release with core extraction functionality
- Interactive menu system for browsing conversations
- Conversation classification (Project, GPT, Plain)
- Fuzzy search functionality with keyword matching
- Zip export capability for multiple conversations
- Markdown export with YAML frontmatter
- Timestamp-based sorting and filtering
