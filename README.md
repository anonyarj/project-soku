# Project Soku

Soku is a privacy-first, local-first personal AI assistant for Windows.

## Current v1 capabilities

- Wake phrase with fuzzy matching
- Local speech-to-text with Faster Whisper
- Local LLM through Ollama
- Multi-turn conversation
- Persistent SQLite memory
- Local text-to-speech
- Secure allowlisted desktop actions
- Open Chrome, VS Code, Calculator, and Notepad
- Open allowlisted websites
- Scroll and media controls
- Local action logging
- Experimental asynchronous speech for interruption/barge-in work
- Optional camera face-presence detection
- Optional hand gesture control
- Modular security layer

## Architecture

Microphone -> Wake detection -> Whisper -> Intent router
                                  |
                                  +-> Secure Action Engine
                                  |
                                  +-> Memory
                                  |
                                  +-> Ollama LLM -> Speech

## Security design

Soku does not expose arbitrary shell execution. Desktop actions are routed through
an allowlist. Website opening is limited to HTTPS and approved domains. High-risk
actions such as deleting files, purchases, installing software, and changing
security settings are intentionally not implemented without a confirmation layer.

The local memory database and action logs should not be committed to GitHub.

## Run

```powershell
.\.venv\Scripts\python.exe soku_main.py
```

## Optional computer-control packages

```powershell
.\.venv\Scripts\python.exe -m pip install pyautogui opencv-python
```

For experimental gestures:

```powershell
.\.venv\Scripts\python.exe -m pip install mediapipe
```

Then:

```powershell
.\.venv\Scripts\python.exe gestures.py
```

## Important limitation

This is a strong local assistant prototype, not a production-grade "Jarvis".
Android phone control requires a separate Android companion app and authenticated
device bridge. Emotion should not be inferred as fact from facial expressions;
Soku can observe visible cues and ask the user how they are feeling.
