# HiruNews AI Streamline — Processing Module
## Phase 2 Prototype

AI-powered news ingestion, transcription, speaker diarization, Sinhala tagline generation, and editorial approval — the upstream companion to HiruTaglineCreator v2.1.

---

### What is this?

This is the **Phase 2 prototype** of **HiruNews AI Streamline**, a product by **Lotus Technologies (Pvt) Ltd** under Asia Broadcasting Corporation (Pvt) Ltd, Sri Lanka.

It demonstrates the AI processing layer that sits *upstream* of HiruTaglineCreator:

```
Audio / Video / Press Release
         ↓
   AI Transcription (Whisper)
         ↓
  Speaker Diarization (GPT heuristic)
         ↓
  Sinhala Tagline Generation (GPT-4o-mini)
         ↓
  Editor Review & Approval (HITL — mandatory)
         ↓
  ai_handoff.json  →  HiruTaglineCreator v2.1
```

---

### Relationship to HiruTaglineCreator

| | HiruTaglineCreator v2.1 | HiruNews AI Streamline (this app) |
|---|---|---|
| **Status** | Production — live since Aug 2025 | Phase 2 prototype |
| **Role** | Broadcast graphics rendering | AI ingestion & editorial approval |
| **Input** | Singlish text / ai_handoff.json | Audio / video / press release |
| **Output** | FM-font PNG taglines | ai_handoff.json |

---

### Installation

```bash
pip install -r requirements.txt
```

### API Key Setup

```bash
cp .env.example .env
# Edit .env and set:
# OPENAI_API_KEY=sk-your-key-here
```

If no key is set, the app runs in **demo mode** with realistic Sinhala mock data — fully navigable for demo and screen recording.

### Run

```bash
py -3 main.py
```

### Six Screens

1. **Upload** — drag-and-drop audio/video/press release + bulletin metadata
2. **Transcription** — Whisper API transcription with GPT-based speaker diarization
3. **Tagline Suggestions** — GPT-4o-mini generates 5 Sinhala broadcast tagline sets (editable)
4. **Editor Approval** — mandatory editorial checklist before any content can be exported
5. **Handoff** — exports `ai_handoff.json` to target session folder for HiruTaglineCreator
6. **Dashboard** — tagline production stats, 7-day bar chart, recent sessions table

### Known Limitations (Prototype)

- Speaker diarization is a GPT heuristic — not a true audio diarization model
- PDF/DOCX source files are not parsed; upload as audio for best results
- "Launch HiruTaglineCreator" button is a stub — integration is Phase 3
- Dashboard data is loaded from `data/dashboard.json` (pre-populated sample)

---

### Credits

**Founder & Developer:** Mr. Vidath Dulanjith — DevOps Engineer, Lotus Technologies (Pvt) Ltd  
**Organization:** Lotus Technologies (Pvt) Ltd, under Asia Broadcasting Corporation (Pvt) Ltd  
**Submission:** SLASSCOM National Ingenuity Awards 2026 — Best Tech for Good Software Innovation
