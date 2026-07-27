# SLASSCOM National Ingenuity Awards 2026
## Submission Package — Best Tech for Good Software Innovation

**Product:** HiruNews AI Streamline
**Submitting Entity:** Lotus Technologies (Pvt) Ltd, under Asia Broadcasting Corporation (Pvt) Ltd
**Product Founder & Main Developer:** Mr. Vidath Dulanjith — DevOps Engineer, Lotus Technologies (Pvt) Ltd
**Contact:** vidath@lotustechnologies.lk

**Links:**
- Asia Broadcasting Corporation: https://www.asiabroadcasting.lk/
- Hiru News: https://www.hirunews.lk/
- Hiru TV: https://www.hirutv.lk/

---

## What Is This Package?

This is the complete SLASSCOM SNIA 2026 submission package for **HiruNews AI Streamline** — an internally developed, production-grade AI-assisted broadcast news workflow system built by Lotus Technologies (Pvt) Ltd for Hiru News, Sri Lanka's #1 television news channel.

The package covers written submissions, a product brochure, a video script, a working prototype, and supporting visual assets.

---

## About the Product

**HiruNews AI Streamline** is a unified product comprising two integrated modules:

| Module | Name | Status |
|--------|------|--------|
| Module 1 | AI News Processing Engine | Prototype (Phase 2) |
| Module 2 | Broadcast Graphics Engine — HiruTaglineCreator v2.1 | **Production since August 2025** |

**Module 2 (HiruTaglineCreator v2.1)** is the live production system. It is the existing codebase located in `/HiruTaglineCreator/` in the root of this repository. It has been in daily use at Hiru News since August 2025 and has not been altered for this submission. It handles FM-compliant Sinhala font rendering, tagline PNG generation, and session management.

**Module 1 (HiruNewsAI_Companion)** is a new companion prototype developed for this submission to demonstrate the full envisioned workflow — media ingestion, AI transcription, multi-model tagline generation, and editorial approval queue — feeding directly into Module 2 via a JSON handoff file.

---

## Folder Structure

```
award_submission_2026/
├── 01_submission_document/     ← 8-section written answers for the SLASSCOM nomination form
├── 02_brochure/                ← 4-page product brochure (HTML source + export-ready PDF)
├── 03_video_script/            ← Full 5-minute video/screencast script for the graphics team
├── 04_ai_prototype/
│   └── HiruNewsAI_Companion/  ← Standalone PyQt5 prototype app (Module 1)
│       ├── main.py             ← Entry point
│       ├── core/               ← Business logic, session and handoff management
│       ├── gui/                ← PyQt5 UI windows and widgets
│       ├── services/           ← AI service integrations (OpenAI, Gemini, local LLM)
│       ├── assets/             ← Icons, fonts, images used by the prototype UI
│       ├── config/             ← App configuration and constants
│       ├── .env.example        ← API key template (never commit real keys)
│       └── requirements.txt    ← Python dependencies
├── 05_assets/
│   ├── diagrams/               ← Architecture and workflow diagrams
│   ├── screenshots/            ← App screenshots (production + prototype)
│   └── mockups/                ← UI mockups and design references
└── README.md                   ← This file
```

---

## Suggested Review Order for Judges

1. **Start here →** `01_submission_document/` — read the 8-section narrative to understand the problem, solution, and impact
2. **Visuals →** `02_brochure/` — open the brochure PDF for a concise visual overview
3. **Live demo context →** `05_assets/screenshots/` — see the production system in action
4. **Architecture →** `05_assets/diagrams/` — understand the end-to-end workflow
5. **Prototype →** `04_ai_prototype/HiruNewsAI_Companion/` — run `main.py` to explore the Phase 2 prototype (requires Python 3.10+, dependencies in `requirements.txt`, API keys in `.env`)
6. **Video →** See the video link provided in the submission form (script in `03_video_script/`)

---

## Key Facts at a Glance

- **Live in production:** August 2025 (Hiru News daily bulletins — 11:55 AM, 6:55 PM, 9:55 PM)
- **Proven under pressure:** Used during the Ditwa Cyclone (Nov–Dec 2025) to broadcast disaster alerts, evacuation orders, and government emergency directives faster than competing channels
- **Time saved:** ~30 minutes per bulletin | ~68% overall time reduction
- **Cost reduction:** ~45%
- **Reach:** Hiru News commands 90% of Sri Lankan internet users; 9M+ followers; primary news source for millions of Sinhala-speaking citizens
- **Human oversight retained:** Every AI output is reviewed and approved by senior journalists before broadcast

---

*Package prepared by Mr. Vidath Dulanjith — Lotus Technologies (Pvt) Ltd*
*SLASSCOM SNIA 2026 — Category: Best Tech for Good Software Innovation*
