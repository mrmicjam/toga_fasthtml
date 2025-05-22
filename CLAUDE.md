# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a boilerplate app that demonstrates how to embed a FastHTML web application inside a Toga native application. The architecture consists of:

- **Toga App (app.py)**: Native desktop wrapper that creates a WebView and manages the web server lifecycle
- **FastHTML App (fasthtml_app/main.py)**: Web application served via ASGI using Daphne server
- **Server Integration**: Uses Daphne (not uvicorn) for better mobile support

## Key Architecture Details

The `FastHTMLApp` class in `app.py` manages the integration:
- Runs Daphne ASGI server in a background thread with dynamic port allocation
- Uses Toga WebView to display the FastHTML app
- Coordinates startup timing to ensure server is ready before loading WebView
- Handles graceful shutdown of both server and GUI components

## Common Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the application:**
```bash
python app.py
```

**Update dependencies (requires pip-tools):**
```bash
pip install pip-tools
python -m piptools compile requirements.in
```

**Run tests:**
```bash
pytest
```

**Run specific test file:**
```bash
pytest test_app.py -v
pytest test_fasthtml_app.py -v
```

## Development Notes

- The server uses dynamic port allocation (port=0) to avoid conflicts
- Daphne is preferred over uvicorn for mobile compatibility
- WebView URL is set only after server confirms it's listening
- Cleanup handler ensures server shutdown on app exit