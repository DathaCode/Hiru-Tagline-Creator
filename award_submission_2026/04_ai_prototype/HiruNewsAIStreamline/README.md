# HiruNews AI Streamline — Processing Module

<p align="center">
  <strong>Phase 2 Prototype · AI News Ingestion & Editorial Approval Companion</strong>
</p>

<p align="center">
  <em>SLASSCOM SNIA 2026 — Best Tech for Good Software Innovation</em>
</p>

---

## Overview

**HiruNews AI Streamline** is an AI-powered news processing pipeline that transforms raw audio/video bulletins into broadcast-ready tagline graphics for Hiru News, Sri Lanka's #1 TV news network.

This prototype demonstrates the complete workflow:

1. **Upload** — Ingest raw audio, video, or transcript files
2. **Transcription** — AI-powered speech-to-text with speaker diarization (Whisper)
3. **AI Suggestions** — GPT generates structured Sinhala tagline sets
4. **Editor Review** — Human-in-the-loop approval with comprehensive checklist
5. **Handoff** — Export approved content to HiruTaglineCreator v2.1 for broadcast graphics

### Relationship to HiruTaglineCreator v2.1

This module is the **AI upstream companion** to [HiruTaglineCreator v2.1](../../HiruTaglineCreator/), the production broadcast graphics generator. The two modules form a complete pipeline:

```
Raw Audio/Video → [AI Streamline] → ai_handoff.json → [HiruTaglineCreator] → Broadcast PNGs
```

HiruTaglineCreator handles the final rendering of on-screen graphic overlays. AI Streamline handles everything before that: ingestion, transcription, AI-assisted tagline generation, and editorial approval.

---

## Architecture

```
┌──────────────────────────────────────────────────┐
│                  PyQt6 Shell                      │
│  ┌─────────────────────────────────────────────┐  │
│  │          QWebEngineView                      │  │
│  │  ┌───────────────────────────────────────┐   │  │
│  │  │        React 18 Frontend              │   │  │
│  │  │   (CDN-loaded, no build step)         │   │  │
│  │  │                                       │   │  │
│  │  │   6 screens with animations,          │   │  │
│  │  │   dark mode, glassmorphism            │   │  │
│  │  └───────────────────────────────────────┘   │  │
│  │              ↕ QWebChannel                    │  │
│  │  ┌───────────────────────────────────────┐   │  │
│  │  │        Python Backend                  │   │  │
│  │  │   OpenAI API, file I/O, JSON export   │   │  │
│  │  └───────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

- **PyQt6** — Desktop window shell with native window chrome
- **QWebEngineView** — Chromium-based web view rendering the React UI
- **QWebChannel** — Bridge for React ↔ Python communication
- **React 18** — UI framework (loaded via CDN, no build step)
- **OpenAI API** — Whisper (transcription) + GPT-4o (tagline generation)

---

## Installation

### Prerequisites

- Python 3.10+
- Internet connection (for CDN resources on first load)

### Setup

```bash
# Navigate to the project directory
cd HiruNewsAIStreamline

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env
```

### OpenAI API Key (Optional)

The app runs in **mock/demo mode** by default with realistic Sinhala sample data. No API key is needed for the demo.

To enable live AI features, edit `.env`:

```env
OPENAI_API_KEY=sk-your-actual-key-here
DEMO_MODE=false
```

---

## Running

```bash
python main.py
```

The PyQt6 window will open displaying the full React UI. Navigate through the 6 screens using the sidebar.

### Demo Flow (without API key)

1. Open the app → Upload screen loads
2. Drop any `.txt` file (or click to browse)
3. Fill in reporter name, select "6:55 PM", choose "Headline"
4. Click "Start AI Processing" → Watch the transcription animation
5. After ~2.5s, mock transcript appears with diarized speakers
6. Continue to AI Suggestions → 5 Sinhala tagline sets appear
7. Select suggestions via checkboxes
8. Proceed to Approval → Tick all 5 checklist items
9. Click Approve → Handoff screen loads
10. Enter session name, click Export → `ai_handoff.json` is written
11. Navigate to Dashboard → See stats, charts, and session history

### Browser Testing (without PyQt6)

The frontend can also be opened directly in a web browser for UI development:

```
Open frontend/index.html in Chrome/Edge
```

A mock bridge is provided that simulates all Python backend calls.

---

## Offline / CDN Fallback

If CDN resources are not available in your environment:

1. Download the following to `frontend/vendor/`:
   - React 18 UMD builds
   - ReactDOM 18 UMD
   - Babel Standalone
   - Recharts UMD
2. Update `frontend/index.html` to reference local paths
3. Download Google Fonts CSS and WOFF2 files to `frontend/assets/fonts/`

---

## Project Structure

```
HiruNewsAIStreamline/
├── main.py                        # PyQt6 shell
├── requirements.txt
├── .env.example
├── README.md
├── backend/
│   ├── __init__.py
│   ├── bridge.py                  # QWebChannel bridge
│   ├── openai_client.py           # OpenAI wrapper + mock fallback
│   ├── transcription.py           # Whisper transcription
│   ├── tagline_generator.py       # GPT tagline generation
│   ├── handoff_writer.py          # ai_handoff.json writer
│   ├── session_store.py           # Local JSON persistence
│   └── mock_data.py               # Realistic Sinhala sample data
├── frontend/
│   ├── index.html                 # React entry point (CDN imports)
│   ├── app.jsx                    # Main React app (all 6 screens)
│   ├── styles.css                 # Design system CSS
│   └── assets/
│       └── logo.svg               # Product logo
└── data/
    ├── dashboard.json
    └── sessions/
        └── ai_handoff_sample.json # Sample export
```

---

## Screenshots

See the screenshots directory for UI captures:
`/award_submission_2026/05_assets/screenshots/`

---

## Technology Stack

| Layer     | Technology                     |
|-----------|-------------------------------|
| Desktop   | PyQt6 + QWebEngineView        |
| Frontend  | React 18, Recharts            |
| Styling   | Custom CSS (dark mode)        |
| AI        | OpenAI Whisper + GPT-4o       |
| Bridge    | Qt QWebChannel                |
| Language  | Python 3.10+, JavaScript ES6  |

---

## Credits

**Founded & Developed by Mr. Vidath Dulanjith**
DevOps Engineer, Lotus Technologies (Pvt) Ltd

Under Asia Broadcasting Corporation (Pvt) Ltd, Sri Lanka

---

<p align="center">
  <sub>HiruNews AI Streamline — Phase 2 Prototype · v1.0.0 · April 2026</sub>
</p>
