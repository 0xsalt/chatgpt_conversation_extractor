#!/usr/bin/env python3
"""
extract_gpt_conversations.py

Author: Russ Swift + GPT-4
License: MIT License
Version: 1.3.1
Description: Extract, filter, and archive ChatGPT conversations from OpenAI data exports.

MIT License

Copyright (c) 2025 Russ Swift

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Full text continues in LICENSE if hosted on GitHub]

"""

import json
import os
import re
import zipfile
import sys
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple, Union

# Version handling
if "--version" in sys.argv:
    try:
        with open(".version", "r") as f:
            print(f.read().strip())
    except FileNotFoundError:
        print("1.0.0")
    exit()

# CONFIG
DEFAULT_INPUT_FILE = "conversations.json"
OUTPUT_DIR = "output_conversations"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Data classes for type safety and readability
@dataclass
class MessageData:
    """Represents a single message in a conversation."""
    author: str
    content: str
    role: str = "unknown"
    
    def __post_init__(self):
        """Validate message data after initialization."""
        if not self.author:
            self.author = "unknown"
        if not self.content:
            self.content = ""

@dataclass
class ConversationData:
    """Represents conversation metadata for processing and display."""
    index: int
    category: str
    title: str
    convo_id: str
    gizmo_id: str
    label: str
    timestamp: float
    
    def __post_init__(self):
        """Validate conversation data after initialization."""
        if not self.title:
            self.title = "Untitled"
        if not self.convo_id:
            self.convo_id = "unknown"
        if not self.gizmo_id:
            self.gizmo_id = "None"
        if self.timestamp < 0:
            self.timestamp = 0.0

@dataclass
class ExportData:
    """Represents conversation data for export operations."""
    conversation: Dict[str, Any]
    category: str
    title: str
    convo_id: str
    timestamp: float
    
    def __post_init__(self):
        """Validate export data after initialization."""
        if not self.title:
            self.title = "Untitled"
        if not self.convo_id:
            self.convo_id = "unknown"
        if self.timestamp < 0:
            self.timestamp = 0.0

def extract_messages(convo: Dict[str, Any]) -> List[MessageData]:
    """Extract messages from conversation mapping."""
    mapping = convo.get("mapping", {})
    messages = []
    for node in mapping.values():
        msg = node.get("message")
        if msg is None:
            continue
        author = msg.get("author", {}).get("role", "unknown")
        content = msg.get("content", {})
        parts = content.get("parts", [])
        if parts:
            message_data = MessageData(
                author=author,
                content=parts[0],
                role=author
            )
            messages.append(message_data)
    return messages

def generate_markdown_content(title: str, category: str, timestamp_str: str, convo_id: str, messages: List[MessageData]) -> str:
    """Generate markdown content with frontmatter."""
    content = f"---\n"
    content += f"title: \"{title}\"\n"
    content += f"category: \"{category}\"\n"
    content += f"timestamp: \"{timestamp_str}\"\n"
    content += f"id: \"{convo_id}\"\n"
    content += f"---\n\n"
    content += f"# {title}\n\n"
    
    # Convert MessageData objects to formatted strings
    formatted_messages = []
    for msg in messages:
        formatted_messages.append(f"**{msg.author.upper()}**:\n{msg.content}\n")
    
    content += "\n---\n\n".join(formatted_messages)
    return content

def export_conversations_to_zip(conversations: List[ExportData], zip_filename: str, output_dir: str) -> str:
    """Export multiple conversations to a zip file."""
    from io import StringIO
    zippath = os.path.join(output_dir, zip_filename)
    
    with zipfile.ZipFile(zippath, 'w') as zipf:
        for export_data in conversations:
            messages = extract_messages(export_data.conversation)
            if messages:
                timestamp_str = format_timestamp(export_data.timestamp)
                safe_title = sanitize_filename(export_data.title)
                filename = f"{export_data.category.upper()}-{timestamp_str}-{safe_title}__{export_data.convo_id[:8]}.md"
                content = generate_markdown_content(export_data.title, export_data.category, timestamp_str, export_data.convo_id, messages)
                zipf.writestr(filename, content)
                print(f"Saved: {filename}")
    
    return zippath

def validate_menu_choice(choice: str, valid_choices: Optional[List[str]] = None) -> Tuple[bool, str]:
    """Validate menu choice input."""
    if valid_choices is None:
        valid_choices = ["0", "1", "2", "3", "4", "5"]
    
    if choice not in valid_choices:
        return False, f"Invalid choice. Please enter one of: {', '.join(valid_choices)}"
    return True, choice  # Return the original choice when valid

def validate_numeric_input(input_str: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> Tuple[bool, Optional[int]]:
    """Validate numeric input with optional range."""
    if not input_str.strip():
        return True, None  # Empty input is valid for some cases
    
    try:
        value = int(input_str)
        if min_val is not None and value < min_val:
            return False, f"Value must be at least {min_val}"
        if max_val is not None and value > max_val:
            return False, f"Value must be at most {max_val}"
        return True, value
    except ValueError:
        return False, "Please enter a valid number"

def validate_range_input(input_str: str, max_val: int) -> Tuple[bool, Optional[Union[int, Tuple[int, int]]]]:
    """Validate range input (e.g., '50-100')."""
    if not input_str.strip():
        return True, None  # Empty input is valid
    
    if "-" in input_str:
        try:
            parts = input_str.split("-")
            if len(parts) != 2:
                return False, "Range format should be 'start-end' (e.g., '50-100')"
            
            start = int(parts[0])
            end = int(parts[1])
            
            if start < 0 or end < 0:
                return False, "Range values must be positive"
            if start > end:
                return False, "Start value must be less than or equal to end value"
            if end >= max_val:
                return False, f"End value must be less than {max_val}"
            
            return True, (start, end)
        except ValueError:
            return False, "Range values must be valid numbers"
    
    # Single number
    return validate_numeric_input(input_str, 0, max_val - 1)

def get_validated_input(prompt: str, validator_func, *args, **kwargs):
    """Get user input with validation and retry logic."""
    while True:
        user_input = input(prompt).strip()
        is_valid, result = validator_func(user_input, *args, **kwargs)
        
        if is_valid:
            return result
        
        print(f"{result}")
        print("Please try again.")

# Custom exception classes
class ConversationProcessingError(Exception):
    """Raised when there's an error processing conversation data."""
    pass

class FileOperationError(Exception):
    """Raised when there's an error with file operations."""
    pass

class InputValidationError(Exception):
    """Raised when user input validation fails."""
    pass

class ExportError(Exception):
    """Raised when there's an error during export operations."""
    pass

class UserExitError(Exception):
    """Raised when user chooses to exit the program."""
    pass

def sanitize_filename(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)[:60]

def classify_convo(convo: Dict[str, Any]) -> str:
    title = convo.get("title", "").lower()
    scope = convo.get("memory_scope", "")
    gizmo_id = convo.get("gizmo_id")
    if scope == "project_enabled":
        return "Project"
    if gizmo_id and scope != "project_enabled":
        return "GPT"
    return "Plain"

def format_timestamp(ts_float: float) -> str:
    try:
        dt = datetime.fromtimestamp(ts_float)
        return dt.strftime("%Y-%m-%d.%H%M.%S")
    except:
        return "unknown_time"

def format_date(ts_float: float) -> str:
    try:
        dt = datetime.fromtimestamp(ts_float)
        return dt.strftime("%Y-%m-%d")
    except:
        return "unknown_date"

def write_convo_markdown(convo: Dict[str, Any], category: str, title: str, convo_id: str, ts: float, output_dir: str) -> Optional[str]:
    """Write conversation to markdown file using modular functions."""
    timestamp_str = format_timestamp(ts)
    safe_title = sanitize_filename(title)
    filename = f"{category.upper()}-{timestamp_str}-{safe_title}__{convo_id[:8]}.md"
    filepath = os.path.join(output_dir, filename)

    messages = extract_messages(convo)
    if messages:
        content = generate_markdown_content(title, category, timestamp_str, convo_id, messages)
        with open(filepath, "w", encoding="utf-8") as out:
            out.write(content)
        print(f"Saved: {os.path.basename(filepath)}")
        return filepath
    else:
        print("No valid messages found to export.")
        return None

def main():
    """Main function with proper exception handling."""
    try:
        # HELP / FILE FLAG
        args = sys.argv[1:]
        if not args or "--help" in args or "-h" in args:
            print("""
Usage:
  $ python extract_gpt_conversations.py --file /path/to/conversations.json

Options:
  --file     Path to your exported conversations.json file
  -h, --help Show this help message

If no --file is provided, defaults to ./conversations.json
""")
            raise UserExitError("Help requested")

        if "--file" in args:
            try:
                file_index = args.index("--file") + 1
                INPUT_FILE = args[file_index]
            except IndexError:
                raise InputValidationError("Missing path after --file")
        else:
            INPUT_FILE = DEFAULT_INPUT_FILE

        # Load data
        try:
            with open(INPUT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileOperationError(f"File not found: {INPUT_FILE}")
        except json.JSONDecodeError as e:
            raise FileOperationError(f"Invalid JSON in {INPUT_FILE}: {e}")
        except Exception as e:
            raise FileOperationError(f"Error reading {INPUT_FILE}: {e}")

        # Classify all conversations
        try:
            classified = []
            for i, convo in enumerate(data):
                category = classify_convo(convo)
                title = convo.get("title", "Untitled")
                convo_id = convo.get("id", "unknown")
                gizmo_id = convo.get("gizmo_id", "None")
                ts = convo.get("create_time", 0)
                label = f"[{category}] [{format_date(ts)}] {title} ({gizmo_id})"
                conversation_data = ConversationData(
                    index=i,
                    category=category,
                    title=title,
                    convo_id=convo_id,
                    gizmo_id=gizmo_id,
                    label=label,
                    timestamp=ts
                )
                classified.append(conversation_data)
        except Exception as e:
            raise ConversationProcessingError(f"Error classifying conversations: {e}")

        # Build ASC index map for fuzzy search
        sorted_classified = sorted(enumerate(classified), key=lambda x: x[1].timestamp)  # by timestamp ASC

        # Menu
        print("\nSelect category to browse:")
        print("0: Project")
        print("1: GPT")
        print("2: Plain")
        print("3: List all chats sequentially ASC")
        print("4: List all chats sequentially DESC")
        print("5: Fuzzy search by keyword")

        choice = get_validated_input("\nEnter choice: ", validate_menu_choice)

        if choice == "5":
            try:
                keyword = input("Enter keyword to search for (case-insensitive, title match): ").lower()
                matched = [(idx, entry) for idx, entry in sorted_classified if keyword in entry.title.lower()]
                print(f"\n--- Matches ({len(matched)} results) ---")
                for global_idx, conversation_data in matched:
                    print(f"{global_idx}: {conversation_data.label}")
                sub_choice = input("\nEnter a number to extract one, or type 'zip' to export all to a zip: ").strip()
                if sub_choice == "zip":
                    # Generate current timestamp for zip filename
                    current_ts = datetime.now().timestamp()
                    timestamp_str = format_timestamp(current_ts)
                    zipname = f"{timestamp_str}-fuzzy_matches_{sanitize_filename(keyword)}.zip"
                    zippath = os.path.join(OUTPUT_DIR, zipname)
                    # Prepare conversations for zip export
                    conversations_to_export = []
                    for (global_idx, conversation_data) in matched:
                        export_data = ExportData(
                            conversation=data[conversation_data.index],
                            category=conversation_data.category,
                            title=conversation_data.title,
                            convo_id=conversation_data.convo_id,
                            timestamp=conversation_data.timestamp
                        )
                        conversations_to_export.append(export_data)
                    
                    # Export using modular function
                    try:
                        export_conversations_to_zip(conversations_to_export, zipname, OUTPUT_DIR)
                        print(f"Exported {len(matched)} results to {zippath}")
                        raise UserExitError("Export completed successfully")
                    except UserExitError:
                        raise
                    except Exception as e:
                        raise ExportError(f"Error exporting to zip: {e}")
                elif sub_choice.isdigit():
                    # Validate the numeric input
                    is_valid, result = validate_numeric_input(sub_choice, 0, len(data) - 1)
                    if is_valid and result is not None:
                        sel = result
                        convo = data[sel]
                        conversation_data = classified[sel]
                        try:
                            os.makedirs(OUTPUT_DIR, exist_ok=True)
                            write_convo_markdown(convo, conversation_data.category, conversation_data.title, conversation_data.convo_id, conversation_data.timestamp, OUTPUT_DIR)
                            raise UserExitError("Conversation exported successfully")
                        except UserExitError:
                            raise
                        except Exception as e:
                            raise ExportError(f"Error writing conversation: {e}")
                    else:
                        raise InputValidationError(result)
                else:
                    raise InputValidationError("Invalid input. Please enter a number or 'zip'.")
            except (UserExitError, ExportError, InputValidationError):
                raise
            except Exception as e:
                raise ConversationProcessingError(f"Error in fuzzy search: {e}")

        # Branch for 0–4
        if choice in ["0", "1", "2"]:
            selected_category = ["Project", "GPT", "Plain"][int(choice)]
            # Create consistent structure with global indices
            filtered = [(i, entry) for i, entry in enumerate(classified) if entry.category == selected_category]

        elif choice in ["3", "4"]:
            is_asc = choice == "3"
            sorted_with_indices = sorted(enumerate(classified), key=lambda x: x[1].timestamp, reverse=not is_asc)
            n = len(sorted_with_indices)
            if is_asc:
                filtered = [(i, entry) for i, (global_idx, entry) in enumerate(sorted_with_indices)]
            else:
                filtered = [(n - 1 - i, entry) for i, (global_idx, entry) in enumerate(sorted_with_indices)]

        else:
            raise InputValidationError("Invalid choice.")

        # Display output for filtered list
        print(f"Hint: There are {len(data)} available")
        range_input = input("How many at a time or what range? [e.g., 10, or 50-100, or {ENTER} for all]: ").strip()
        total = len(filtered)

        # Validate range input
        is_valid, result = validate_range_input(range_input, total)
        if not is_valid:
            raise InputValidationError(result)

        if result is None:  # Empty input - show all
            to_show = list(range(total))
        elif isinstance(result, tuple):  # Range input (start, end)
            start, end = result
            to_show = list(range(start, min(end + 1, total)))
        else:  # Single number
            step = result
            start = 0
            while start < total:
                end = min(start + step, total)
                print(f"\n--- Chats {start} to {end - 1} ---")
                for idx in range(start, end):
                    global_idx, conversation_data = filtered[idx]
                    print(f"{global_idx}: {conversation_data.label}")
                user_input = input("\nSelect chat # to extract or press ENTER to continue: ").strip()
                if user_input == "":
                    start += step
                    continue
                else:
                    # Validate numeric input
                    is_valid, result = validate_numeric_input(user_input, 0, len(data) - 1)
                    if is_valid and result is not None:
                        sel = result
                        # Find the conversation with the selected global index
                        for global_idx, conversation_data in filtered:
                            if global_idx == sel:
                                convo = data[conversation_data.index]
                                try:
                                    os.makedirs(OUTPUT_DIR, exist_ok=True)
                                    write_convo_markdown(convo, conversation_data.category, conversation_data.title, conversation_data.convo_id, conversation_data.timestamp, OUTPUT_DIR)
                                    raise UserExitError("Conversation exported successfully")
                                except UserExitError:
                                    raise
                                except Exception as e:
                                    raise ExportError(f"Error writing conversation: {e}")
                        raise InputValidationError("Invalid selection.")
                    else:
                        raise InputValidationError(result)
            raise UserExitError("No conversation selected.")

        # Final fallback: user selected a range or full dump
        print(f"\n--- Available Chats ---")
        for idx in to_show:
            global_idx, conversation_data = filtered[idx]
            print(f"{global_idx}: {conversation_data.label}")
        sel_input = input("\nSelect the conversation number to extract, or type 'zip' to export all to a zip: ").strip()
        if sel_input == "zip":
            # Generate current timestamp for zip filename
            current_ts = datetime.now().timestamp()
            timestamp_str = format_timestamp(current_ts)
            zipname = f"{timestamp_str}-range_export.zip"
            zippath = os.path.join(OUTPUT_DIR, zipname)
            # Prepare conversations for zip export
            conversations_to_export = []
            for idx in to_show:
                global_idx, conversation_data = filtered[idx]
                export_data = ExportData(
                    conversation=data[conversation_data.index],
                    category=conversation_data.category,
                    title=conversation_data.title,
                    convo_id=conversation_data.convo_id,
                    timestamp=conversation_data.timestamp
                )
                conversations_to_export.append(export_data)
            
            # Export using modular function
            try:
                export_conversations_to_zip(conversations_to_export, zipname, OUTPUT_DIR)
                print(f"Exported {len(to_show)} results to {zippath}")
                raise UserExitError("Export completed successfully")
            except UserExitError:
                raise
            except Exception as e:
                raise ExportError(f"Error exporting to zip: {e}")
        elif sel_input.isdigit():
            # Validate numeric input
            is_valid, result = validate_numeric_input(sel_input, 0, len(data) - 1)
            if is_valid and result is not None:
                sel = result
                # Find the conversation with the selected global index
                for global_idx, conversation_data in filtered:
                    if global_idx == sel:
                        convo = data[conversation_data.index]
                        try:
                            os.makedirs(OUTPUT_DIR, exist_ok=True)
                            write_convo_markdown(convo, conversation_data.category, conversation_data.title, conversation_data.convo_id, conversation_data.timestamp, OUTPUT_DIR)
                            raise UserExitError("Conversation exported successfully")
                        except UserExitError:
                            raise
                        except Exception as e:
                            raise ExportError(f"Error writing conversation: {e}")
                raise InputValidationError("Invalid selection.")
            else:
                raise InputValidationError(result)
        else:
            raise InputValidationError("Invalid input. Please enter a number or 'zip'.")

    except UserExitError as e:
        print(f"{e}")
        return 0
    except InputValidationError as e:
        print(f"Input Error: {e}")
        return 1
    except FileOperationError as e:
        print(f"File Error: {e}")
        return 1
    except ConversationProcessingError as e:
        print(f"Processing Error: {e}")
        return 1
    except ExportError as e:
        print(f"Export Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
