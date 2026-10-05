# 🎬 Hiru News Tagline Creator — Complete User Manual
**Version 1.1** | © 2026 Hiru News / Lotus Technologies | Support: vidath@lotustechnologies.lk

---

## Table of Contents

1. [Overview](#overview)
2. [System Requirements & Installation](#system-requirements--installation)
3. [Application Architecture](#application-architecture)
4. [First-Time Setup](#first-time-setup)
5. [Interface Walkthrough](#interface-walkthrough)
6. [Core Features — Detailed Guide](#core-features--detailed-guide)
   - [Dual Template Support (MAIN TAG / SUB TAG)](#1-dual-template-support)
   - [Singlish → Sinhala Unicode Converter](#2-singlish--sinhala-unicode-converter)
   - [Sinhala Unicode → FM ASCII Conversion](#3-sinhala-unicode--fm-ascii-conversion)
   - [Live Visual Preview](#4-live-visual-preview)
   - [Text Adjustments Panel](#5-text-adjustments-panel)
   - [PNG Generation Panel](#6-png-generation-panel)
   - [Session Management](#7-session-management)
   - [Settings Dialog](#8-settings-dialog)
7. [Keyboard Shortcuts](#keyboard-shortcuts)
8. [MAIN TAG Workflow](#main-tag-workflow)
9. [SUB TAG Workflow](#sub-tag-workflow)
10. [Text Beds — Specifications Reference](#text-beds--specifications-reference)
11. [File Naming & Output](#file-naming--output)
12. [Font Requirements & Troubleshooting](#font-requirements--troubleshooting)
13. [Development History — Challenges, Errors & Fixes](#development-history--challenges-errors--fixes)

---

## Overview

**Hiru News Tagline Creator** is a specialized, offline professional broadcast tool designed to generate transparent `1920×1080` PNG overlays for the Hiru News television channel's on-screen graphics system. It supports two layout types — **MAIN TAG** and **SUB TAG** — and handles the full Sinhala typography pipeline entirely on-device, without any internet connectivity requirement.

### What It Does
- Accepts Singlish (phonetic Sinhala) or direct Sinhala Unicode typing
- Converts text to **FM ASCII** — the legacy encoding expected by FM fonts used on broadcast systems
- Renders text at pixel-perfect positions onto transparent `1920×1080` canvases using **PyQt5**
- Outputs correctly ordered, named PNG files ready for direct use in vMix, CasparCG, OBS, or similar broadcast software

---

## System Requirements & Installation

| Requirement | Minimum | Recommended |
|---|---|---|
| **OS** | Windows 10 64-bit | Windows 11 64-bit |
| **RAM** | 4 GB | 8 GB |
| **Disk Space** | 500 MB free | 1 GB free |
| **Python** | 3.11+ (dev only) | 3.12 |
| **Display** | 1280×800 | 1920×1080 |

### Required Fonts (MANDATORY)
The application **cannot render Sinhala text** without these two fonts being installed on the system:

| Font Name | File | Used In |
|---|---|---|
| **FM GANGANEE** | `FMGanganee x.ttf` | Topic Bed (red headline bar) |
| **FM SANDHYANEE** | `FMSandhyanee x.ttf` | TAG Bed & White Bed |

**Font Install Path:**
```
C:\Users\[YourName]\AppData\Local\Microsoft\Windows\Fonts\
```
or the system-wide:
```
C:\Windows\Fonts\
```

**To install:**
1. Double-click the `.ttf` file
2. Click **"Install for all users"** (recommended) or **"Install"**
3. **Restart** the application after installation

### Required Python Packages (Development)
```
Pillow
PyQt5
```
Install with:
```bash
pip install -r requirements.txt
```

### Running from Source
```bash
python main.py
```

### Running the Executable
Double-click `HiruTaglineCreator_v1.1.exe` — no Python installation required.

---

## Application Architecture

```
HiruTaglineCreator/
├── main.py                    ← Entry point; startup checks
├── config/
│   ├── settings.json          ← User settings (auto-created)
│   └── default_settings.json  ← Factory defaults
├── core/
│   ├── template_manager.py    ← Loads & caches template PNGs
│   ├── session_manager.py     ← Sessions, draft save/load
│   ├── text_renderer.py       ← PyQt5 rendering engine (all beds)
│   └── text_validator.py      ← Word count validation rules
├── gui/
│   ├── main_window.py         ← Main UI, bed input widgets, tab logic
│   ├── generation_panel.py    ← PNG generation, progress dialog
│   ├── preview_panel.py       ← Live preview canvas
│   └── settings_dialog.py     ← Tabbed settings (Templates/Fonts/General)
├── utils/
│   ├── fm_converter.py        ← Sinhala Unicode → FM ASCII (762-line ruleset)
│   ├── sinhala_unicode_converter.py ← Singlish → Sinhala Unicode
│   ├── font_finder.py         ← Locates FM font .ttf files on disk
│   ├── font_checker.py        ← Validates font availability at startup
│   ├── config_manager.py      ← JSON settings read/write
│   └── logger.py              ← Application logging
├── templates/
│   ├── MAIN_TAG.png           ← 1920×1080 base template
│   └── SUB_TAG.png            ← 1920×1080 base template
└── assets/                    ← Icons and static resources
```

### Startup Sequence
```
main.py
  ↓ ConfigManager (load settings.json)
  ↓ check_fonts_installed() → exit if fonts missing
  ↓ TemplateManager (validate & cache MAIN_TAG.png, SUB_TAG.png)
  ↓ SessionManager (scan C:/HiruTaglines/ for existing sessions)
  ↓ MainWindow created → mainloop()
```

---

## First-Time Setup

### Step 1: Install Fonts
Install `FMGanganee x.ttf` and `FMSandhyanee x.ttf` as described above.

### Step 2: Place Template Files
Make sure both template files are present:
```
HiruTaglineCreator/templates/MAIN_TAG.png
HiruTaglineCreator/templates/SUB_TAG.png
```
If missing, the app will warn you on startup with a dialog. You can also configure template paths in **Settings → Templates**.

### Step 3: Configure Output Folder
Open **Settings (⚙️) → General → Default Save Location**.  
Default: `C:/HiruTaglines/`

Each session creates a subfolder here automatically.

### Step 4: Create Your First Session
Click **🆕 New** in the top bar and type a session name (e.g., `AKUREGODA`).  
A folder named `AKUREGODA_YYYY-MM-DD` is created at your save location.

---

## Interface Walkthrough

```
┌──────────────────────────────────────────────────────────────┐
│  Session: [AKUREGODA_2026-04-09 ▼]  🆕 New  💾 Save  📂 Open │  ← TOP BAR
│                                                    ⚙️ Settings│
├──────────────────┬───────────────────────────────────────────┤
│ 📺 MAIN TAG      │                                           │
│ 📋 SUB TAG       │           🎨 LIVE PREVIEW                 │
│──────────────────│                                           │
│ 🔴 TOPIC BED     │       [Template image with text           │
│ [Entry field   ] │        overlaid in real-time]             │
│ Preview label    │                                           │
│──────────────────│  Selected TAG: [Line 1 ▼]                 │
│ 🟠 TAG BED       │                                           │
│ [Multi-line    ] │                                           │
│ [text area     ] │                                           │
│ [preview area  ] │                                           │
│──────────────────│                                           │
│ ⬜ WHITE BED     │                                           │
│ [Entry field   ] │                                           │
│──────────────────│                                           │
│ 🎛️ Text Adjustments                                          │
│   Horizontal Scale: [====●=======] 100%  🔄 Reset           │
│   Letter Spacing:   [===●========]  0px  🔄 Reset           │
│──────────────────────────────────────────────────────────────│
│ 📸 PNG GENERATION PANEL                         ▲ Collapse   │
│  [✓] Topic Bed  |  [Preview text...]   👁️ Preview            │
│  TAG BEDS ☑ All  ☐ None                    (N lines)        │
│  [✓] 1. Line preview text...              👁️                 │
│  [✓] 2. Line preview text...              👁️                 │
│  [✓] White Bed  |  [Preview text...]   👁️ Preview            │
│  ─────────────────────────────────────────────────────────   │
│  SUMMARY: 4 of 4 selected         Output: C:/HiruTaglines/.. │
│  📸 Generate Selected PNGs    📂 Open Folder                  │
├──────────────────────────────────────────────────────────────┤
│ Ready                                          🗑️ Clear All   │  ← STATUS BAR
└──────────────────────────────────────────────────────────────┘
```

---

## Core Features — Detailed Guide

### 1. Dual Template Support

The application supports two distinct broadcast layout types, controlled via the tab selector at the top of the left panel.

#### MAIN TAG
Used for the **primary news story** graphic. Shows all three text beds:

| Bed | Role | Font | Size |
|---|---|---|---|
| 🔴 Topic Bed | Main headline / topic title | FM GANGANEE | 50.4 px |
| 🟠 TAG Bed | News tagline lines (multi) | FM SANDHYANEE | 60 px |
| ⬜ White Bed | Secondary static text | FM SANDHYANEE | 48 px |

#### SUB TAG
Used for **secondary extended taglines** that need two-line TAG beds. When this tab is active:
- The **White Bed is hidden** (SUB TAG templates have no white bar)
- The TAG Bed pairs **every 2 lines** into a single PNG
- The Topic Bed remains visible and functional

**Switching tabs is instant** — no data is lost. The Generation Panel, Preview, and bed visibility all update automatically.

---

### 2. Singlish → Sinhala Unicode Converter

Every input bed has a 🇸🇮 / 🌐 language toggle button. When set to **🇸🇮 Sinhala**, the text you type in standard English phonetics (Singlish) is instantly converted to Sinhala Unicode.

#### How It Works
The `sinhala_unicode_converter.py` module uses a phonetic mapping system:

| You type | Converts to |
|---|---|
| `pravruthi sakachchawa` | `ප්‍රවෘත්ති සාකච්ඡාව` |
| `dumriya` | `දුම්රිය` (special-cased, no Rakaransaya) |
| `akuregoda` | `අකුරේගෝදා` |
| `aniwaarya` | `අනිවාර්ය` |

#### Key Phonetic Rules

| Singlish | Sinhala |
|---|---|
| `k` | ක |
| `g` | ග |
| `th` | ත |
| `dh` | ද |
| `sh` | ශ |
| `ng` | ං |
| `ch` | ච |
| `aa` | ා |
| `ii` / `ee` | ී |
| `uu` / `oo` | ූ |
| `ru` | රු |

#### Real-Time Preview
Below each input field, a **preview label** (rendered with Iskoola Pota Unicode font) shows the converted Sinhala text so you can verify it before it reaches the rendering engine.

#### Per-Bed Toggle
Each bed has its own independent toggle:
- **🇸🇮 Sinhala** — Singlish conversion active
- **🌐 English** — Raw text mode (for English-only headlines)

---

### 3. Sinhala Unicode → FM ASCII Conversion

This is the **most critical** conversion step. FM fonts (`FM GANGANEE`, `FM SANDHYANEE`) are legacy fonts that store Sinhala glyphs mapped to standard ASCII positions — they are **not** Unicode-compliant fonts.

The `fm_converter.py` module (`convert_unicode_to_fm()`) converts standard Unicode Sinhala into the proprietary FM ASCII encoding required for the fonts to display correctly.

#### Conversion Pipeline (Order is Non-Negotiable)

```
Input Unicode Text
   ↓
1. Escape Latin A-Za-z → PUA range (preserve English letters)
2. Strip ZWJ (U+200D) and ZWNJ (U+200C)
3. Apply word-level exceptions (e.g., දුම්රිය)
4. Special punctuation pre-processing (, → ￦, ' → z, etc.)
5. Complex conjunct combos (yansaya+vowels, rakaransaya+vowels)
6. Bare conjuncts: ්ය → H, ්ර → %
7. Vowel combos (ෝ, ො, ේ, ෙ, etc.) with all consonants
8. Base consonant mappings (ග→., ස→i, ක→l, ම→u, etc.)
9. Vowel diacritics (ි→s, ා→d, ු→q, ්→a, etc.)
10. Post-processing: restore escaped punctuation
    ↓
FM ASCII Output (renderable with FM font)
```

#### Latin Letter Preservation (PUA Encoding)
When Sinhala text contains English words (e.g., `COVID-19`, `USA`), English letters are first mapped to Unicode PUA (Private Use Area) range `U+E041–U+E07A`. After FM conversion is complete, they are split into separate segments and rendered with **Arial** instead of the FM font — ensuring no garbling.

#### Key FM Mappings Reference

| Sinhala Unicode | FM ASCII |
|---|---|
| ග | `.` |
| ස | `i` |
| ක | `l` |
| ම | `u` |
| ත | `;` |
| ෙ (e vowel prefix) | `f` (placed before consonant) |
| ා | `d` |
| ් (hal kirima) | `a` |
| ්ය (yansaya) | `H` |
| ්ර (rakaransaya) | `%` |

---

### 4. Live Visual Preview

The right panel displays a real-time composite of all rendered beds overlaid on the loaded template image.

#### How Preview Works
1. On each key press, a **100 ms debounce timer** fires (`schedule_preview_update`)
2. The template image is copied in memory (`.copy().convert('RGBA')`)
3. The pre-baked red Topic bar in the PNG template is **erased** (cleared to transparent)
4. Each active bed is rendered fresh using the PyQt5 engine to a `1920×1080 RGBA` canvas
5. All layers are composited using `Image.alpha_composite()`
6. The composite is scaled to fit the preview canvas and displayed

#### Selected TAG Dropdown
Above the preview, a dropdown lets you select which TAG line (MAIN TAG) or pair (SUB TAG) is shown in the preview. The preview always shows the **dropdown-selected** line, not the cursor position, ensuring deliberate visual review.

#### Preview Popup (👁️)
Each line/pair in the Generation Panel has a **👁️** button that opens a full `960×580` resizable popup window showing an isolated composite preview of that specific element on the template.

---

### 5. Text Adjustments Panel

Located below the White Bed input. These controls apply to the **TAG Bed** and affect both preview and PNG output.

#### Horizontal Scale
- **Range:** 50% — 100%
- **Default:** 100%
- **Effect:** Compresses the text horizontally (narrows glyph width) without changing the font's vertical size
- **Use when:** A TAG line is too long to fit but reducing font size would make it too small
- Press **🔄 Reset Scale** to return to 100%

#### Letter Spacing
- **Range:** −10 px — +30 px
- **Default:** 0 px
- **Effect:** Adds or removes space between every character pair
- **Use when:** Text appears too tight (increase) or too spread out (decrease)
- Press **🔄 Reset Spacing** to return to 0 px

> **Note:** Adjustments do **not** apply to the Topic Bed or White Bed — those beds use automatic fit scaling only and ignore manual overrides to maintain broadcast consistency.

---

### 6. PNG Generation Panel

This collapsible panel (▲ Collapse / ▼ Expand) manages the final export.

#### Elements
- **Topic Bed checkbox** — include/exclude the Topic Bed PNG
- **TAG Beds section** — one checkbox per line (MAIN TAG) or per pair (SUB TAG)
  - Each row shows a truncated preview of the text
  - ⚠️ warnings appear next to lines exceeding word limits
  - 👁️ preview button per line/pair
- **White Bed checkbox** — include/exclude the White Bed PNG (MAIN TAG only)
- **☑ Select All / ☐ None** buttons for TAG lines
- **SUMMARY** — shows selected vs. total count
- **Output path** — shows the active session folder

#### Validation
Before generating, the app validates all selected TAG lines:
- Lines with **hard warnings (✖)** block generation (error dialog shown)
- Lines with **soft warnings** prompt a Yes/No dialog to continue

#### Word Count Limits

| Bed | Limit | Behaviour |
|---|---|---|
| Topic Bed | 12 words | ⚠️ warning label turns red |
| White Bed | 15 words | ⚠️ warning label turns red |
| TAG Bed | configurable | ⚠️ inline warning in panel |

#### Generation Process
1. Click **📸 Generate Selected PNGs**
2. A **modal Progress Bar dialog** appears showing `N of M files…`
3. For each selected element:
   - The template base image is composited with the text layer
   - The final PNG is saved to the session folder
   - File timestamps are set sequentially to preserve sort order in Explorer
4. A **Results Summary dialog** appears with:
   - Count of successfully generated files
   - Listview of all filenames
   - Errors tab (if any renders failed)
   - **📂 Open Folder** button

---

### 7. Session Management

Sessions are the primary organizational unit — all PNGs from one news broadcast segment go into one session folder.

#### Creating a Session
Click **🆕 New** → type a name (e.g., `AKUREGODA`) → press Enter.  
The folder `C:/HiruTaglines/AKUREGODA_2026-04-09/` is created automatically.

#### Session Dropdown
The top-left dropdown lists all sessions found in the save folder (sorted newest-first). Switching sessions:
1. Sets the active session path
2. Loads the saved draft (raw input text, adjustments, template mode)
3. Restores the TAG/Topic/White bed inputs exactly as they were

#### Draft Saving
- **Auto-save:** Runs every **60 seconds** in the background (configurable)
- **Manual save:** `Ctrl+S` or 💾 Save button
- Draft is stored as `draft.json` inside the session folder
- The JSON stores both the **converted Unicode output** and the **raw Singlish input** so both can be restored correctly

#### Draft JSON Structure
```json
{
  "session_name": "AKUREGODA",
  "template_type": "MAIN_TAG",
  "content": {
    "topic_bed": "...",       ← converted Unicode
    "topic_bed_raw": "...",   ← raw Singlish input
    "tag_lines": [...],
    "tag_lines_raw": "...",
    "white_bed": "...",
    "white_bed_raw": "..."
  },
  "adjustments": {
    "h_scale": 100,
    "letter_spacing": 0
  },
  "last_modified": "2026-04-09T15:23:01"
}
```

---

### 8. Settings Dialog

Open with **⚙️ Settings** button or `Ctrl+,`. Has four tabs:

#### 📁 Templates Tab
- Set file paths for MAIN_TAG.png and SUB_TAG.png
- Browse for new template files
- Dimension status (✓ if 1920×1080, ✗ otherwise)
- Read-only bed coordinates reference table

#### 🔤 Fonts Tab
- Shows install status (`✓ Installed` / `✗ NOT installed`) for FM GANGANEE and FM SANDHYANEE
- Renders a small preview image of each font if installed
- Font installation instructions

#### 💾 General Tab
- **Default Save Location** — where session folders are created
- **Auto-save** — enable/disable 60-second auto-save
- **Remember window position** — on/off
- **Date format** for PNG filenames: `YYYY-MM-DD`, `DD-MM-YYYY`, `MM-DD-YYYY`
- Validation limits overview

#### ℹ️ About Tab
- Version info, built-with list, contact details
- **📋 Copy System Info** — copies OS/Python/architecture info to clipboard for support tickets

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+S` | Save current session draft |
| `Ctrl+N` | Create a new session |
| `Ctrl+O` | Open current session folder in Explorer |
| `Ctrl+,` | Open Settings dialog |

---

## MAIN TAG Workflow

### Step 1: Select MAIN TAG Tab
Click **📺 MAIN TAG** tab. All three beds (Topic, TAG, White) are visible.

### Step 2: Enter Topic Bed Text
Type the news topic in the **Topic Bed** field.
- In **🇸🇮 Sinhala** mode: type phonetically (e.g., `karumara hamuwa`)
- The red preview label shows the converted Sinhala Unicode
- Limit: 12 words (warning shown if exceeded)
- The red background bar expands automatically with text width

### Step 3: Enter TAG Lines
In the **TAG Bed** multi-line area, type one tagline per line.
- Each line will become one PNG file
- Maximum recommended: 9 words per line
- The converted preview shows below the input area
- Lines auto-appear in the Generation Panel with checkboxes

### Step 4: Enter White Bed Text
Type a secondary text in the **White Bed** field.
- Single line only
- Limit: 15 words
- Rendered on the white bar area of the template

### Step 5: Adjust If Needed
Use the **Text Adjustments Panel** to compress or space out long TAG lines.

### Step 6: Review in Preview
- Select each TAG line in the **"Selected TAG" dropdown** to preview it
- Click **👁️** next to any line in the Generation Panel for a full popup preview

### Step 7: Generate PNGs
In the Generation Panel:
1. Uncheck any lines you don't need
2. Click **📸 Generate Selected PNGs**
3. Output files are named and ordered: `001_TopicBed_DATE.png`, `002_WORD1-WORD2-WORD3_TAG_DATE.png`, ..., `00N_WORD_WhiteBed_DATE.png`

---

## SUB TAG Workflow

### Step 1: Switch to SUB TAG Tab
Click **📋 SUB TAG** tab.
- White Bed input is automatically hidden
- Generation Panel switches to **paired mode**
- Template background updates to SUB_TAG template

### Step 2: Enter Topic Text
Same as MAIN TAG — Topic Bed remains available and works identically.

### Step 3: Enter TAG Lines in Pairs
In the TAG Bed area, type two consecutive lines per intended PNG:

**Example — 6 lines → 3 PNGs:**
```
ඕවුන් දැනටමත් යුරෝපීය රටක් වන සයිප්‍රසය වෙත
ප්‍රහාර එල්ල කරනු ලැබුවා
ශ්‍රම වාසනා අරමුදල ඈවර කරන්න
කැබිනට් මණ්ඩලයේ අනුමැතිය
වැලි හිඟතාවය නිසා
වැලි මිල ඉහළට
```

| PNG | Line 1 (Top Row) | Line 2 (Bottom Row) |
|---|---|---|
| PNG 1 | ඕවුන් දැනටමත් ... | ප්‍රහාර එල්ල... |
| PNG 2 | ශ්‍රම වාසනා ... | කැබිනට් මණ්ඩලයේ... |
| PNG 3 | වැලි හිඟතාවය නිසා | වැලි මිල ඉහළට |

> ⚠️ **Odd lines:** If you enter an odd number of lines, the last line is automatically paired with an empty second line.

### Step 4: Review Pairs in Generation Panel
Each pair appears as a single row:
```
[✓] 1-2. ඕවුන් දැනටමත්... / ප්‍රහාර එල්ල...   👁️
[✓] 3-4. ශ්‍රම වාසනා...  / කැබිනට් ...          👁️
```

### Step 5: Preview
Use the **"Selected TAG" dropdown** — it now shows `"Pair 1"`, `"Pair 2"`, etc.

### Step 6: Generate
Click **📸 Generate Selected PNGs**. Output files:
```
001_TopicBed_DATE.png
002_WORD1-WORD2_TAG_DATE.png   ← pair 1
003_WORD1-WORD2_TAG_DATE.png   ← pair 2
...
```

---

## Text Beds — Specifications Reference

### MAIN TAG Layout

| Bed | X | Y | Width | Height | Font | Size | Color |
|---|---|---|---|---|---|---|---|
| TOPIC BED | 96 | 572 | dynamic (min 370, max 1110) | 62 | FM GANGANEE | 50.4 px | White on `#a70003` |
| TAG BED | 104 | 617 | 1110 | 56 | FM SANDHYANEE | 60 px | Black |
| WHITE BED | 104 | 680 | 1110 | 48 | FM SANDHYANEE | 48 px | Black |

### SUB TAG Layout

| Bed | X | Y | Width | Height | Font | Size | Color |
|---|---|---|---|---|---|---|---|
| TOPIC BED | 96 | 572 | dynamic (min 370, max 1477) | 62 | FM GANGANEE | 50.4 px | White on `#a70003` |
| TAG BED | 122 | 751 | 1477 | 58 | FM SANDHYANEE | 50 px (×2 lines) | Black |

### Topic Bed Red Bar Behaviour
The Topic Bed's red background expands dynamically with text width:
- Left edge is always fixed at `x = 126`
- Width = `LEFT_PAD (34) + scaled_text_width + RIGHT_PAD (34)`
- Maximum width is capped at `width_max` from config
- The template's pre-baked static red bar is **erased** before every render so the dynamic bar is the only one visible

### SUB TAG Dual-Line Positions
Inside the SUB_TAG bed (58 px tall, spans `y=751` to `y=809`):
- Line 1 center: `y + 36 = 787`
- Line 2 center: `y + 103 = 854`

---

## File Naming & Output

### File Naming Convention
All output PNGs follow this pattern:
```
{SEQ}_{PREFIX}_{TYPE}_{DATE}.png
```

| Part | Example | Source |
|---|---|---|
| `SEQ` | `001`, `002` | Auto-incrementing (ensures Explorer sort order) |
| `PREFIX` | `ශ්‍රම-වාසනා-අරමුදල` | First 3 words of the text |
| `TYPE` | `TAG`, `TopicBed`, `WhiteBed` | Bed type |
| `DATE` | `2026-04-09` | Generation date |

**Full example:**
```
001_TopicBed_2026-04-09.png
002_ශ්‍රම-වාසනා-අරමුදල_TAG_2026-04-09.png
003_වැලි-හිඟතාවය-නිසා_TAG_2026-04-09.png
004_කැබිනට්-මණ්ඩලයේ_WhiteBed_2026-04-09.png
```

### File Timestamps
Each file's filesystem timestamp is set **1 second apart in sequence** using `os.utime()`. This guarantees correct sort order even when the OS resolves multiple files in the same second.

### Output Location
All files go to:
```
{default_save_location}/{SESSION_NAME}_{DATE}/
```
Example: `C:/HiruTaglines/AKUREGODA_2026-04-09/`

---

## Font Requirements & Troubleshooting

### Problem: App Exits at Startup ("Required fonts missing")
**Cause:** FM GANGANEE or FM SANDHYANEE fonts are not installed.  
**Fix:** Install both `.ttf` files. See **First-Time Setup** above.

### Problem: Sinhala characters show as boxes/question marks in preview
**Cause:** Iskoola Pota (the preview display font) may not be installed.  
**Fix:** Install `Iskoola Pota` from Windows optional fonts or Office.

### Problem: Generated PNG shows garbled characters
**Cause:** The FM font was not found and Arial was used as fallback.  
**Fix:** Check **Settings → Fonts** tab for `✗ NOT installed` indicators. Re-install the FM fonts.

### Problem: Template validation fails ("expected 1920×1080")
**Cause:** Wrong resolution template file placed in the templates folder.  
**Fix:** Ensure both `MAIN_TAG.png` and `SUB_TAG.png` are exactly `1920×1080` pixels.

---

## Development History — Challenges, Errors & Fixes

This section documents every significant technical challenge, bug, and design issue encountered during the development of Hiru News Tagline Creator from the initial prototype stage through to the current v1.1 release.

---

### 🟥 STAGE 1 — Initial Prototype (Pillow-based Renderer)

#### Challenge 1: Sinhala Text Rendering Failure with Pillow
**Problem:** The first prototype used `Pillow (PIL)` with `ImageDraw.text()` to render Sinhala Unicode. The output was completely garbled — consonant conjuncts were broken apart, vowel diacritics appeared in wrong positions, and the text was rendered left-to-right instead of applying Unicode BiDi rules.

**Root Cause:** Pillow has no built-in Unicode shaping engine. It does not support:
- OpenType GSUB/GPOS glyph substitution tables
- BiDi (bidirectional text) algorithm
- Sinhala conjunct glyph forming (rakaransaya, yansaya)

**Fix:** Migrated the rendering engine entirely to **PyQt5 (`QPainter`, `QFont`, `QFontMetrics`)**. PyQt5 uses the platform's native text shaping stack (HarfBuzz on Linux/Mac, DirectWrite/Uniscribe on Windows), which correctly handles all Sinhala Unicode conjunct forms.

The renderer creates a `QImage(1920, 1080, Format_ARGB32)`, paints text onto it, then converts to a Pillow `Image` via `qimage.bits().asstring()` → `Image.frombuffer("RGBA", ..., "BGRA")`. The BGRA→RGBA channel swap is critical.

---

#### Challenge 2: Font Not Found at Runtime (Standalone .exe)
**Problem:** When packaged as a single `.exe` with PyInstaller, the FM fonts were not found. `QFontDatabase.addApplicationFont()` returned `-1`, causing silent fallback to Arial, making all output unreadable.

**Root Cause:** The `.ttf` font files were not bundled into the executable, and system-wide font paths were hardcoded to `C:\Windows\Fonts\` which doesn't contain user-installed fonts.

**Fixes Applied:**
1. Created `utils/font_finder.py` (`find_fm_fonts()`) which searches multiple locations:
   - `C:\Windows\Fonts\`
   - `C:\Users\{user}\AppData\Local\Microsoft\Windows\Fonts\`
   - `C:\Users\{user}\AppData\Roaming\Microsoft\Windows\Fonts\`
2. Created `utils/windows_font_finder.py` which queries the Windows registry key `HKCU\Software\Microsoft\Windows NT\CurrentVersion\Fonts`
3. At startup, `find_fm_fonts()` is called and the resolved paths are fed directly to `QFontDatabase.addApplicationFont(path)`, guaranteeing font load even without system-wide install

---

#### Challenge 3: Transparent PNG Background Contamination
**Problem:** Early generated PNGs had a solid white or black background instead of full transparency. This made them unusable in broadcast compositing software.

**Root Cause:** `QImage` was initialized with `QImage.Format_RGB32` (no alpha channel), and `qimage.fill(Qt.white)` was called, baking in a white background.

**Fix:**
1. Changed format to `QImage.Format_ARGB32`
2. Changed fill to `QColor(0, 0, 0, 0)` (fully transparent black)
3. Verified alpha channel preservation through the BGRA → RGBA conversion
4. Saved final output using `img.save(filepath, 'PNG')` — PIL preserves the alpha channel correctly in PNG mode

---

### 🟧 STAGE 2 — FM Font Encoding System

#### Challenge 4: Unicode Text Refused to Display Correctly with FM Fonts
**Problem:** FM Ganganee and FM Sandhyanee are legacy fonts that predate Unicode. They store Sinhala glyphs mapped to Latin ASCII code points (e.g., glyph for `ස` is at position `i`, glyph for `ක` is at `l`). Passing Unicode Sinhala text to these fonts produced incorrect Latin characters.

**Root Cause:** These fonts are "encoding-hacked" — they are technically ASCII fonts where each ASCII character was replaced with a Sinhala glyph. There is no Unicode-to-glyph mapping. The text must be pre-converted to the specific FM ASCII encoding before rendering.

**Fix:** Built `utils/fm_converter.py` — a 762-line deterministic string replacement engine implementing the full GururLK FM font encoding table. The function `convert_unicode_to_fm(text)` applies ~400+ ordered `str.replace()` calls with strict precedence rules.

**Critical Rule:** Complex conjuncts (yansaya, rakaransaya with vowel combinations) must be replaced **before** their component characters. For example, `ශ්‍යෝ` → `fYHda` must be processed before `ශ` → `Y` and before `්ය` → `H`, or the multi-char sequence is permanently broken.

---

#### Challenge 5: Yansaya Incorrectly Applied to ර්ය Sequences
**Problem:** Words like `කාර්යාලය`, `අනිවාර්ය`, and `අනිවාර්යෙන්ම` were rendered with an incorrect Yansaya (ය-ාංශය) conjunct. The `ර්ය` sequence was being matched by the generic `්ය → H` (yansaya) rule, inserting the wrong glyph.

**Root Cause:** After stripping ZWJ/ZWNJ, `ර්ය` becomes phonetically "rya" (rar + ya), **not** a yansaya of another consonant. The generic sweeper `s.replace('්ය', 'H')` was hitting the `ර්‌ + ය` in these words.

**Fix (Conversation `f4c21746`):**
Two-step solution:
1. **Before** the `්ය → H` rule, insert: `s.replace('ර්ය', '\u00BEය')` — this converts only the `ར්` part to its FM code (`¾`) while leaving `ය` as Unicode
2. **Remove** the `ර්ය` block-level exception that was previously trying to map the entire sequence
3. The remaining `ය` then falls through naturally to `s.replace('ය', 'h')` at the base consonant stage

This ensured `කාර්යාලය` renders as `ldr¾hd,h` (correct) not `ldr¾Hdh` (wrong yansaya).

---

#### Challenge 6: English Letters Destroyed by FM Conversion
**Problem:** When a tagline contained English words mixed with Sinhala (e.g., `COVID-19 anaawaranaya`), the letters C, O, V, I, D were mapped to FM Sinhala glyphs (e.g., `C` → a specific Sinhala char in the font), producing unreadable output.

**Root Cause:** The FM conversion table maps many ASCII uppercase and lowercase letters to Sinhala glyphs because FM fonts are ASCII-encoded Sinhala fonts.

**Fix:** Implemented a **Private Use Area (PUA) escape system** in `fm_converter.py`:
1. **Before conversion:** `_escape_latin(text)` replaces every `A-Za-z` with `chr(0xE000 + ord(ch))` — mapping them out of ASCII range into PUA where the FM ruleset cannot touch them
2. **After conversion:** `has_english_segments()` detects PUA characters, `split_fm_and_english()` splits the text into `[(segment, is_fm), ...]` pairs
3. **During rendering:** FM segments use the FM font; English/PUA segments are decoded back and rendered with **Arial Bold** at the same size — both are drawn at matching positions via cursor tracking

---

#### Challenge 7: දුම්රිය Incorrectly Rendered with Rakaransaya
**Problem:** The word `දුම්රිය` (train) was being rendered with a Rakaransaya (්‍ර) conjunct: `දුම්‍රිය` — which is phonetically wrong and visually incorrect.

**Root Cause:** The generic rakaransaya rule `s.replace('්ර', '%')` was matching the `ම්‌ + ర` sequence in this word.

**Fix:** Added a **word-level exception** at the top of the conversion (before any conjunct rules):
```python
s = s.replace('දුම්රිය', '\u00FF\u00EF\u00DFh')
```
This converts the entire word to its correct FM representation in one atomic replacement, bypassing all subsequent conjunct rules. The same pattern was added to the Singlish converter's `word_mappings` dict.

---

### 🟨 STAGE 3 — Layout Engine & Alignment

#### Challenge 8: Topic Bed Red Background Not Scaling Correctly
**Problem:** The red background bar of the Topic Bed was either too short (leaving text without background) or fixed-width (not adapting to text length). On narrow topics it exceeded the text; on long topics it was clipped.

**Root Cause:** The initial implementation used a hardcoded `width` for the red rectangle instead of measuring the rendered text width.

**Fix:**
1. Measure the FM-converted text width using `QFontMetrics.horizontalAdvance()`
2. Compute: `bg_width = LEFT_PAD (34) + scaled_text_width + RIGHT_PAD (34)`
3. Cap at `width_max` from config (1110 for MAIN_TAG, 1477 for SUB_TAG)
4. Apply horizontal compression (`scale`) if text exceeds `width_max`
5. Erase the template's pre-baked static red bar via `Image.paste(transparent_patch, (bx, by))` before alpha-compositing the dynamic bar

---

#### Challenge 9: Topic Bed Left Alignment Mismatch with TAG/White Beds
**Problem:** The Topic Bed text left edge was visually misaligned with the TAG and White bed text. The red bar started at a different x-position than the text in the other beds.

**Root Cause:** The red bed left edge (`bed_x = 126`) and the text start position were computed independently. There was confusion between the bed background x-coordinate and the text x-coordinate, causing `LEFT_PAD` to be applied inconsistently.

**Fix (Conversation `59d4b2a9`):**  
Defined explicit, fixed constants in `render_topic_bed()`:
- Red bar left edge: `bed_x = 126` (pixel-tested against template)
- Text left edge: `text_x = bed_x + LEFT_PAD` = `126 + 34 = 160`
- TAG/White text also starts at `x + 20` offset from their config x-coordinates (both set to `104 + 20 = 124`... adjusted after pixel testing to align visually)

---

#### Challenge 10: Text Overflowing Right Boundary of TAG/White Beds
**Problem:** Long taglines would overflow the right boundary of the orange TAG bar or white bed, overlapping unintended areas of the broadcast graphic.

**Root Cause:** No auto-scaling was implemented in the initial version.

**Fix:**
- In `render_tag_bed_text()` and `render_white_bed_text()`: implemented `_compute_fit_scale()`:
  ```python
  def _compute_fit_scale(self, width, available_width):
      if width <= available_width:
          return 1.0
      return max(available_width / width, 0.5)  # min 50% compression
  ```
- `available_width = bed_width - 40` (20px padding each side)
- When `h_scale < 100` (manual slider): the slider value overrides auto-fit
- When `h_scale == 100`: auto-fit is applied

---

#### Challenge 11: PyQt5 Painter Transform Not Restoring After Scale
**Problem:** When horizontal scaling was applied (`painter.scale(h_scale, 1.0)`), subsequent drawing operations in the same image (e.g., rendering two lines in SUB TAG) used the accumulated transform, causing second lines to be shifted and scaled incorrectly.

**Root Cause:** `painter.scale()` accumulates on the current transformation matrix. Without proper `save()`/`restore()`, each successive draw call inherited the previous iterations' scaling.

**Fix:** Wrapped every scaled draw call with `painter.save()` / `painter.restore()`:
```python
painter.save()
painter.translate(x, y)
if scale < 1.0:
    painter.scale(scale, 1.0)
# ... draw text ...
painter.restore()
```
This isolates each segment's transform from all others.

---

### 🟦 STAGE 4 — Session Management

#### Challenge 12: Session Switch Not Restoring Input Fields
**Problem:** When switching sessions from the dropdown, the input fields were not populated with the previously saved content. The fields remained blank or showed the previous session's data.

**Root Cause (Conversation `5b1d966e`):** The session switch handler was only updating `session_mgr.current_session_path` but not calling `load_draft()` to fetch the saved content and populate the UI widgets.

**Fix:** Implemented `_on_session_selected()` in `MainWindow`:
1. Sets `session_mgr.current_session_path` from the dropdown selection
2. Calls `session_mgr.load_draft()` to load `draft.json`
3. Calls `topic_input.set_text()`, `tag_input.set_text()`, `white_input.set_text()` with **raw Singlish text** (so re-conversion fires correctly)
4. Restores `h_scale` and `letter_spacing` adjustments
5. Selects the correct notebook tab (MAIN_TAG or SUB_TAG) via `notebook.select(0/1)`
6. Schedules a preview update

---

#### Challenge 13: Session Dropdown Not Showing New Session After Creation
**Problem:** After clicking **🆕 New** and entering a name, the new session did not appear selected in the dropdown — the previous session remained selected.

**Root Cause:** The code refreshed the session list after creation but didn't set `session_var` to the new folder name before refreshing, so `_refresh_session_list()` fell back to the first item.

**Fix:** Added `self.session_var.set(folder_name)` **before** calling `_refresh_session_list()`, so the refresh finds the new value already set and preserves it.

---

#### Challenge 14: Raw vs. Converted Text Round-Trip Bug
**Problem:** When a session was saved and reloaded, the Singlish input was replaced with the converted Sinhala Unicode output. This meant re-editing was impossible — the user could not go back to the Singlish phonetic form.

**Root Cause:** The save code only stored the converted Unicode output (`.get_text()`), not the raw Singlish input (`.get_raw_text()`).

**Fix:** Updated `_save_session()` to store both:
```python
"content": {
    "topic_bed":     self.topic_input.get_text(),       # converted
    "topic_bed_raw": self.topic_input.get_raw_text(),   # raw Singlish
    "tag_lines":     self.tag_input.get_lines(),
    "tag_lines_raw": self.tag_input.get_raw_text(),
    ...
}
```
On load, the `_raw` field is preferred:
```python
if "topic_bed_raw" in content:
    self.topic_input.set_text(content["topic_bed_raw"])
else:
    self.topic_input.set_text(content.get("topic_bed", ""))
```

---

### 🟩 STAGE 5 — SUB TAG Feature

#### Challenge 15: SUB TAG PNG Generation Order Was Wrong
**Problem (Conversation `fb62a1de`):** When generating SUB TAG PNGs, the Topic Bed PNG was being saved **after** the TAG pairs instead of first. This broke the broadcast production workflow where Topic Bed must always be the first PNG in the folder.

**Root Cause:** The generation loop was iterating TAG pairs first, then Topic Bed.

**Fix:** Restructured the `_generate()` method in `generation_panel.py` with a strict ordering:
```
1. Generate Topic Bed (if selected)    → seq_num = 1
2. Generate TAG Beds (pairs/lines)     → seq_num = 2, 3, 4...
3. Generate White Bed (MAIN_TAG only)  → seq_num = last
```
Sequential numbering (`001_`, `002_`, `003_`) is prepended to every filename, and `os.utime()` sets file creation timestamps in sequence to enforce sort order.

---

#### Challenge 16: SUB TAG TAG Bed Height Was Too Short for Two Lines
**Problem:** The SUB_TAG template has a taller orange TAG bar (to accommodate two text lines), but the bed config was using the same `height: 56` as MAIN_TAG, causing the second line to render below the orange bar.

**Root Cause:** The initial implementation didn't distinguish between MAIN_TAG and SUB_TAG bed heights in the config.

**Fix:** Updated `default_settings.json` with separate SUB_TAG bed config:
```json
"sub_tag": {
  "TAG_BED": {
    "x": 122, "y": 751,
    "width": 1477, "height": 58
  }
}
```
And in `render_sub_tag_bed_text()`: uses `font_size = 50` (vs 60 for MAIN TAG) and fixed vertical line positions `[y + 36, y + 103]` to properly seat both lines within the bed.

---

#### Challenge 17: SUB TAG White Bed Not Being Hidden on Tab Switch
**Problem:** When switching from MAIN TAG to SUB TAG, the White Bed input frame remained visible in the UI despite SUB TAG not using a White Bed.

**Root Cause:** The tab-switch handler was not calling `white_bed_frame.pack_forget()`.

**Fix:** Updated `_on_tab_change()` to explicitly show/hide the white bed:
```python
if new_template == 'SUB_TAG':
    self.white_bed_frame.pack_forget()
    self.gen_panel.set_template_type('SUB_TAG')  # also hides white in gen panel
```
The Generation Panel's `set_template_type('SUB_TAG')` method hides `white_lf` as well, so both areas are consistently updated.

---

#### Challenge 18: SUB TAG Preview Showing Wrong Pair Selection
**Problem:** The live preview was always showing "Pair 1" regardless of which pair was selected in the "Selected TAG" dropdown.

**Root Cause:** The preview update code was ignoring the dropdown's selected index (`selected_tag_index`) and always using index 0 when computing which pair to render.

**Fix:** Implemented a `selected_tag_index` property on `PreviewPanel` and wired the dropdown's `<<ComboboxSelected>>` event to call `schedule_preview_update()`. The preview code now reads:
```python
selected_index = self.get_selected_tag_index()
s = selected_index * 2
l1 = tag_lines[s]
l2 = tag_lines[s+1] if s+1 < len(tag_lines) else ''
```

---

### 🟪 STAGE 6 — Text Adjustment Controls

#### Challenge 19: Letter Spacing Slider Affecting Topic Bed Unexpectedly
**Problem:** When the Letter Spacing slider was changed, the Topic Bed preview would also reflow differently, causing misalignment of the red background bar.

**Root Cause:** `render_topic_bed()` was receiving the `letter_spacing` parameter from `adjustments` and applying it to the font. Topic Bed uses a narrow, precise red bar width that depends on letter spacing being predictable.

**Fix:** Added an explicit override at the top of `render_topic_bed()`:
```python
def render_topic_bed(self, text, bed_config, letter_spacing=0):
    letter_spacing = 0  # Force 0; Topic bed must not inherit global spacing
```
Likewise, `render_white_bed_text()` forces both `h_scale = 100` and `letter_spacing = 0` to maintain consistent output regardless of the slider position.

---

#### Challenge 20: Slider Producing Float Values Causing IntVar Mismatch
**Problem:** The `ttk.Scale` widget returns float values through its `command` callback. Setting these directly to `tk.IntVar` caused a `ValueError` in some Tkinter builds.

**Root Cause:** `ttk.Scale` callbacks pass the value as a string representing a float (e.g., `"95.0"`), but `IntVar.set()` and downstream code expected clean integers.

**Fix:**
```python
def on_scale_change(self, value):
    val = int(float(value))  # convert "95.0" → 95
    self.h_scale_var.set(val)
    self.adjustments['h_scale'] = val
```

---

### 🟫 STAGE 7 — PNG Save & File System

#### Challenge 21: PNG Save Failure for Sinhala-Named Files on Windows
**Problem:** When the TAG text was Sinhala (e.g., `ශ්‍රම-වාසනා-අරමුදල`), the generated PNG filename caused an `OSError` on some Windows configurations because the path contained non-ASCII characters.

**Root Cause:** Some Windows builds with `cp1252` default encoding could not handle Unicode filenames in `open()` calls even with `encoding='utf-8'` specified on the mode (the filename itself is a different code path).

**Fix:** Added a fallback in `text_renderer.save_png()`:
```python
try:
    img.save(filepath, 'PNG')
except Exception as e:
    import re
    safe_path = re.sub(r'[^\x00-\x7F]+', '_', filepath)
    img.save(safe_path, 'PNG')
```
For complete safety, the Generation Panel also strips file-system forbidden characters `\ / : * ? " < > |` from the text prefix before constructing filenames.

---

#### Challenge 22: Files Not Sorted Correctly in Windows Explorer
**Problem:** Generated PNGs appeared in random order in Windows Explorer (not 001, 002, 003 sequence) because the files were created within the same second and Explorer sorts by timestamp.

**Root Cause:** `os.path.getctime()` and filesystem sort both rely on modification time; multiple files created in the same second get the same timestamp.

**Fix:** After saving each file, `os.utime()` sets incrementing timestamps:
```python
base_time = time.time()
file_counter = 0
# ... after each save ...
file_counter += 1
target_time = base_time + file_counter  # each file 1 second apart
os.utime(filepath, (target_time, target_time))
```
Combined with the `{SEQ:03d}_` numeric prefix in filenames, sort order is guaranteed by both name and timestamp.

---

### ⬛ STAGE 8 — QGuiApplication Singleton & Packaging

#### Challenge 23: `QGuiApplication` Must Not Be Created Multiple Times
**Problem:** When the `TextRenderer` module was imported, `QGuiApplication(sys.argv)` was called unconditionally. On second import (e.g., from two different modules), PyQt5 raised:
```
RuntimeError: QApplication already created
```

**Root Cause:** PyQt5 requires exactly one `QApplication` (or `QGuiApplication`) instance per process.

**Fix:** Guard at module level:
```python
_qapp = QGuiApplication.instance()
if not _qapp:
    _qapp = QGuiApplication(sys.argv)
```
This retrieves the existing instance if one exists, only creating it if not already present.

---

#### Challenge 24: PyInstaller Missing PyQt5 Plugins
**Problem:** The packaged `.exe` crashed on startup with:
```
qt.qpa.plugin: Could not load the Qt platform plugin "windows"
```

**Root Cause:** PyInstaller did not automatically include Qt's platform plugin DLL (`qwindows.dll`) in the bundle.

**Fix (`.spec` file):** Added explicit data collection in `HiruTaglineCreator_v1.1.spec`:
```python
from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files('PyQt5')
```
This bundles all Qt platform plugins, image format plugins, and supporting DLLs into the distribution.

---

## Quick Reference Card

| Task | Action |
|---|---|
| New session | 🆕 New → type name → Enter |
| Save work | `Ctrl+S` or 💾 Save |
| Switch template type | Click 📺 MAIN TAG or 📋 SUB TAG tab |
| Toggle Singlish/English | Click 🇸🇮 / 🌐 button on any bed |
| Preview one TAG line | Dropdown → select line OR 👁️ button |
| Compress long line | Horizontal Scale slider → reduce % |
| Export PNGs | 📸 Generate Selected PNGs |
| Open output folder | 📂 Open Folder or `Ctrl+O` |
| Settings | ⚙️ or `Ctrl+,` |
| Clear all inputs | 🗑️ Clear All |

---

*Last updated: April 2026 | Developed by Lotus Technologies for Hiru News*
