#!/usr/bin/env python3

import sys
import os
import re
from pathlib import Path

# --- Configuration ---

# Setup paths relative to the current working directory
working_dir = Path.cwd()
chat_dir = working_dir / "chat"
captures_dir = chat_dir / "captures"

SOURCE_DIR=captures_dir
OUTPUT_FILE = chat_dir / "Transcript_Assembly.md"

if not chat_dir.exists():
    print(f"Error: chat directory not found at {chat_dir}")
    sys.exit(1)

if not captures_dir.exists():
    print(f"Error: Captures directory not found at {captures_dir}")
    sys.exit(1)

# The starting number for the prompt/response sequence
START_INDEX = 1

def assemble_transcript():
    """Reads all chronological markdown files and assembles them into a structured Markdown file."""
    
    if not SOURCE_DIR.exists():
        print(f"Error: Source directory not found at {SOURCE_DIR}")
        return

    # 1. Get all markdown files, sorted chronologically by filename (timestamp)
    # Glob returns an iterable of all files matching the pattern *.md
    # and we sort them to ensure correct chronological order.
    # We use list() for easy indexing later.
    try:
        file_list = sorted(list(SOURCE_DIR.glob("*.md")))
    except Exception as e:
        print(f"Error reading files from source directory: {e}")
        return

    if not file_list:
        print(f"No markdown files found in {SOURCE_DIR}. Nothing to assemble.")
        return
        
    current_index = START_INDEX
    output_lines = []

    # 2. Iterate through the files and apply the alternating pattern
    for i, file_path in enumerate(file_list):
        # Determine if the current file is a PROMPT (even index 0, 2, 4...) or a RESPONSE (odd index 1, 3, 5...)
        is_prompt = (i % 2 == 0)
        
        # Determine the header text
        if is_prompt:
            header = f"# PROMPT {current_index}"
        else:
            header = f"# RESPONSE {current_index}"
        
        output_lines.append(header)
        
        # 3. Read the content of the file
        try:
            content = file_path.read_text(encoding="utf-8").strip()
        except Exception as e:
            content = f"[[ERROR READING FILE {file_path.name}: {e}]]"
        
        # Append content, enclosed in a markdown blockquote for clean separation
        output_lines.append(f"> {content.replace(chr(10), chr(10) + '> ')}") # Ensure every line of content is quoted
        output_lines.append("\n---\n") # Separator between entries

        # having trouble with this:
        #output_lines.append(f"*Edit this prompt/response in emacs: `(find-file \"./captures/{file_path.name}\")`*\n\n")
        output_lines.append(f"Edit this prompt/response in emacs: (find-file \"./captures/{file_path.name}\")\n\n")
        
        # Only increment the index after a full Prompt/Response cycle (i.e., after the Response)
        if not is_prompt:
            current_index += 1

    # 4. Write all assembled content to the final Markdown file
    try:
        OUTPUT_FILE.write_text("\n".join(output_lines), encoding="utf-8")
        print(f"\n✨ SUCCESS! Transcript assembled into:\n{OUTPUT_FILE}")
        print(f"Total entries processed: {current_index - 1}")
    except Exception as e:
        print(f"Error writing to output file {OUTPUT_FILE}: {e}")

if __name__ == "__main__":
    assemble_transcript()
