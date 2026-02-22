# AI Chat Localizer

A simple, durable system for capturing browser-based AI conversations (Gemini, ChatGPT, etc.) and converting them into a navigable local web of Markdown and HTML files.

## 🚀 Why this exists
Browser-based chats are ephemeral and locked in "The Cloud." This tool gives you **data sovereignty** by allowing you to:
1. **Capture:** Watch your clipboard and save Prompts/Responses as individual files.
2. **Assemble:** Combine captures into a single "Full Transcript" and a series of linked HTML pages.
3. **Browse:** Use Emacs (specifically `eww`) to fly through your history with keyboard-driven speed.
4. **Search:** Use `ag` (The Silver Searcher) or `grep` to instantly find that one specific breakthrough in a sea of past encounters.

## 🛠️ Components

### 1. `chat-capture.sh` (The Watcher)
A Bash script that monitors the Linux clipboard. 
- **How it works:** Every time you copy text, it creates a new `.md` file in `./chat/captures/`.
- **Feature:** Includes a terminal preview to help you track your progress.
- **Requirement:** `xclip` (e.g., `sudo pacman -S xclip`)

### 2. `chat-assemble.py` (The Builder)
A Python script that builds the localized web.
- **How it works:** Sorts files by timestamp and alternates labels between **PROMPT** and **RESPONSE**.
- **Output:** Creates a master `full_transcript.html` and individual pages with **Next/Previous** navigation.
- **Requirement:** `cmark-gfm` (e.g., `sudo pacman -S cmark-gfm`)

## Usage: example result

To see an example of the output, look at chat folder in this repo.

## 📖 Usage Workflow

Step 0: Preparation
`cd` into your working folder for the topic of interest.

Step 1: **Start the Watcher:**

```
./chat-capture.sh
```

Step 2: Capture the Conversation

Simply copy your Prompt, then copy the AI's Response. The terminal will show snippets of what you captured to keep you on track.

Resulting Files:

```
chat/captures/
├── 20260222_144201_capture.md  <-- Prompt
└── 20260222_144215_capture.md  <-- Response
```

Step 3. Build the Local Web:

Run the assembler to generate the HTML site:
  
```
python chat-assemble.py
```

Resulting structure:

```
chat/
├── full_transcript.html       <-- The "Master List"
├── full_transcript.md
└── captures/
    ├── 20260222_144201_capture.html  <-- Linked page
    └── 20260222_144201_capture.md
```

Step 4: Review in Emacs

Open chat/full_transcript.html in eww.

* Each entry includes a Lisp-powered "Edit" link to jump directly to the source .md file.

* Use the Next/Previous links in the captures to read the session like a book.
    
## How it was Developed

This script was built through an iterative dialogue with Gemini (free version). For a
detailed look at the logic, the alternative approaches considered, and
the evolution of the code, check the contents of the chat/
folder in this repository.

## License

See LICENSE file