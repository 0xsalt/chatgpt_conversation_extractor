# CHANGELOG

## v1.3.1 – Exception Handling Bug Fix (CHATGPT-003)
- Fixed exception handling bug where successful operations were incorrectly reported as errors
- Added proper exception re-raising for `UserExitError` in nested try-catch blocks
- Improved test output to show positive results instead of warning messages
- Enhanced user experience with correct success/error reporting

## v1.3.0 – Exception Handling and Error Management (CHATGPT-003)
- Implemented comprehensive exception handling system
- Added custom exception classes for different error types:
  - `ConversationProcessingError`: For conversation data processing errors
  - `FileOperationError`: For file I/O operations
  - `InputValidationError`: For user input validation failures
  - `ExportError`: For export operation errors
  - `UserExitError`: For graceful program exits
- Created main function with proper exception handling structure
- Replaced all `exit()` calls with proper exception handling
- Added graceful error handling with meaningful error messages
- Implemented keyboard interrupt handling (Ctrl+C)
- Added proper exit codes for different error conditions
- Enhanced script robustness and maintainability

## v1.2.0 – Input Validation and Error Handling (CHATGPT-002)
- Added centralized input validation functions
- Created `validate_menu_choice()` for menu option validation
- Added `validate_numeric_input()` with range checking
- Implemented `validate_range_input()` for range format validation
- Added `get_validated_input()` with retry logic and user-friendly error messages
- Improved error messages with consistent formatting
- Enhanced robustness against invalid user input
- All existing functionality preserved with better error handling

## v1.1.0 – Code Modularization (CHATGPT-001)
- Extracted repeated message extraction logic into `extract_messages()` function
- Created `generate_markdown_content()` for consistent markdown generation
- Added `export_conversations_to_zip()` for unified zip export functionality
- Eliminated code duplication across multiple export paths
- Improved code maintainability and testability
- All existing functionality preserved with no regression

## v1.0.0 – Initial Release
- Loads conversations.json and displays GPT/Project/Plain threads
- Allows selective markdown export of any chat
- Interactive menu system for browsing conversations
- Fuzzy search functionality with keyword matching
- Zip export capability for multiple conversations
- Conversation classification (Project, GPT, Plain)
- Timestamp-based sorting and filtering
