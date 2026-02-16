import os
import re
from pathlib import Path

# --- Configuration ---
# Must match the directory used in the bash script
SOURCE_DIR = Path.home() / "Clipboard_Captures"
# The name of the final output file
OUTPUT_FILE = Path.home() / "Transcript_Assembly.md"
# The starting number for the prompt/response sequence
START_INDEX = 1

def assemble_transcript():
    """Reads all chronological text files and assembles them into a structured Markdown file."""
    
    if not SOURCE_DIR.exists():
        print(f"Error: Source directory not found at {SOURCE_DIR}")
        return

    # 1. Get all text files, sorted chronologically by filename (timestamp)
    # Glob returns an iterable of all files matching the pattern *.txt
    # and we sort them to ensure correct chronological order.
    # We use list() for easy indexing later.
    try:
        file_list = sorted(list(SOURCE_DIR.glob("*.txt")))
    except Exception as e:
        print(f"Error reading files from source directory: {e}")
        return

    if not file_list:
        print(f"No text files found in {SOURCE_DIR}. Nothing to assemble.")
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
