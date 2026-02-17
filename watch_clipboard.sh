#!/usr/bin/bash

# --- Configuration ---
DEST_DIR="./chat/captures"
CLIPBOARD_SELECTION="clipboard"
PREVIEW_LINES=2    # Lines to show at top/bottom
MIN_LINES_FOR_OMISSION=8
CHECK_INTERVAL=0.5 # How often to check the clipboard (in seconds)

# --- Initialize ---
mkdir -p "$DEST_DIR"
# Store the current clipboard so we don't immediately save what's already there
LAST_CLIP=$(xclip -selection "$CLIPBOARD_SELECTION" -o 2>/dev/null)
CAPTURE_COUNT=0

clear
echo "🚀 Clipboard Watcher Started!"
echo "Saving to: $DEST_DIR"
echo "Instructions: Just copy text in your browser. I will handle the rest."
echo "Press [Ctrl+C] to stop."
echo "--------------------------------------------------"

# --- The Watch Loop ---
while true; do
    # 1. Grab the current clipboard content
    CURRENT_CLIP=$(xclip -selection "$CLIPBOARD_SELECTION" -o 2>/dev/null)
    
    # 2. Check if the content is different from the last saved content
    # AND check that it isn't empty
    if [[ "$CURRENT_CLIP" != "$LAST_CLIP" && -n "$CURRENT_CLIP" ]]; then
        
        # Increment counter
        ((CAPTURE_COUNT++))
        
        # 3. Generate filename and save
        TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
        FILENAME="${TIMESTAMP}.md"
        FILE_PATH="$DEST_DIR/$FILENAME"
        echo "$CURRENT_CLIP" > "$FILE_PATH"

        # 4. Generate the Fancy Preview
        LINE_COUNT=$(echo "$CURRENT_CLIP" | wc -l)
        
        echo -e "\n✅ [Capture #$CAPTURE_COUNT] Saved: $FILENAME"
        echo "--------------------------------------------------"
        
        if [ "$LINE_COUNT" -le "$MIN_LINES_FOR_OMISSION" ]; then
            echo "$CURRENT_CLIP"
        else
            echo "$CURRENT_CLIP" | head -n "$PREVIEW_LINES"
            echo "..."
            echo "--- (Omitted $((LINE_COUNT - 2 * PREVIEW_LINES)) lines) ---"
            echo "..."
            echo "$CURRENT_CLIP" | tail -n "$PREVIEW_LINES"
        fi
        
        echo "--------------------------------------------------"

        # 5. Update LAST_CLIP so we don't save the same thing twice
        LAST_CLIP="$CURRENT_CLIP"
    fi

    # Wait a bit before checking again to save CPU
    sleep "$CHECK_INTERVAL"
done
