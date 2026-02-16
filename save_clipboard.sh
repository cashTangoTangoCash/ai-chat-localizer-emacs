#!/usr/bin/bash

# --- Configuration ---
# The destination directory where the files will be saved.
# Adjust this to your preferred location.
DEST_DIR="$HOME/Clipboard_Captures"

# The clipboard selection to use.
# 'clipboard' is typically used for Ctrl+C.
# 'primary' is typically used for simple selection/middle-click paste.
CLIPBOARD_SELECTION="clipboard"

# --- Script Logic ---

# 1. Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# 2. Generate a timestamp for the filename
# %Y%m%d_%H%M%S gives a sortable filename like 20251124_221348.txt
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILENAME="${TIMESTAMP}.txt"

# 3. Use xclip to get the clipboard content and save it to the file
# The -selection flag specifies which clipboard to read from.
# The '>>' appends the content, but since the file is new, it just saves it.
# The '||' handles the case where xclip fails (e.g., if the clipboard is empty).
xclip -selection "$CLIPBOARD_SELECTION" -o > "$DEST_DIR/$FILENAME"

# 4. (Optional) Provide feedback on success or failure
if [ $? -eq 0 ]; then
    echo "Clipboard content saved to: $DEST_DIR/$FILENAME"
else
    # Check if the file was created (meaning xclip succeeded but maybe had a small error)
    if [ -f "$DEST_DIR/$FILENAME" ] && [ ! -s "$DEST_DIR/$FILENAME" ]; then
        echo "Warning: Clipboard was empty, created an empty file: $DEST_DIR/$FILENAME"
        # Optional: Remove the empty file if you don't want it
        # rm "$DEST_DIR/$FILENAME"
    else
        echo "Error: Failed to read from the clipboard using xclip."
        # If you see this, ensure xclip is installed and X is running.
    fi
fi
