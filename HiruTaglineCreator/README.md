# Hiru News Tagline Creator

Professional broadcast tagline (lower-third) graphics generator for TV news production.
It lets a producer type a headline in **Singlish** (Romanized Sinhala), see it rendered
live on the on-air template, and export broadcast-ready **1920×1080 transparent PNG**
overlays — with correct legacy **FM-font** Sinhala shaping.

> **Latest build:** [`dist/HiruTaglineCreator_v2.6.exe`](dist/HiruTaglineCreator_v2.6.exe) — a single-file Windows executable (~59 MB, no Python install required on the target machine).

---

## Table of Contents
- [What it does](#what-it-does)
- [How it works (the text pipeline)](#how-it-works-the-text-pipeline)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Architecture & project structure](#architecture--project-structure)
- [Templates & bed layout](#templates--bed-layout)
- [Fonts](#fonts)
- [Configuration & sessions](#configuration--sessions)
- [Running from source (development)](#running-from-source-development)
- [Building the executable](#building-the-executable)
- [The built product (.exe)](#the-built-product-exe)
- [System requirements](#system-requirements)
- [User workflow — using the app](#user-workflow--using-the-app)
- [License & support](#license--support)

---

## What it does

Sri Lankan TV news lower-thirds ("taglines") are built from stacked coloured **beds**:

- **Topic Bed** — the red title bar (white text on red, auto-expanding width).
- **TAG Bed** — the orange headline bar.
- **White Bed** — the white sub-headline bar (MAIN TAG only).

The app ships the two official on-air backplates (**MAIN TAG** and **SUB TAG**) as
1920×1080 templates. The operator types text, positions/scales it, previews it composited
on the real template, and exports each bed as its own transparent PNG that the playout /
graphics system (e.g. CasparCG, vMix, XPression) can key over live video.

The hard part it solves is **Sinhala text for legacy FM broadcast fonts**. Sinhala on TV
is still produced with old ASCII-mapped "FM" fonts (FM Ganganee, FM Sandhyanee), not
Unicode. This tool bridges modern Unicode input to those fonts automatically.

---

## How it works (the text pipeline)

Text goes through **two conversions** before it reaches a pixel:

```
  Operator types Singlish            "shree lanka"
        │
        ▼   utils/sinhala_unicode_converter.py  (phonetic transliteration)
  Sinhala Unicode                    "ශ්‍රී ලංකා"      ← shown in the yellow live-preview box
        │
        ▼   utils/fm_converter.py     (Unicode → FM ASCII, order-sensitive)
  FM ASCII string                    "Y%S ,xld"       ← renders correctly ONLY in an FM font
        │
        ▼   core/text_renderer.py     (PyQt5 QPainter + FM font)
  Rasterized glyphs on a 1920×1080 transparent canvas → PIL Image → PNG
```

Key details:

- **Stage 1 — Singlish → Unicode** (`sinhala_unicode_converter.convert_text`): phonetic
  transliteration (`k→ක`, `aa→ා`, `shree→ශ්‍රී`, rakaransaya/yansaya handling, etc.). The
  operator can toggle this off per bed with the **🇸🇮 Sinhala / 🌐 English** button to type
  raw text.
- **Stage 2 — Unicode → FM ASCII** (`fm_converter.convert_unicode_to_fm`): ~700 ordered
  `str.replace` rules that map Unicode conjuncts to the FM font's ASCII code points. **Order
  is non-negotiable** — complex conjuncts (rakaransaya `්‍ර`, yansaya `්‍ය`, vowel combos)
  must be replaced before their base consonants or the output garbles.
- **Mixed English handling**: Latin letters are escaped into the Unicode PUA range so they
  survive FM conversion, then split back out (`split_fm_and_english`) and drawn in **Arial**
  so embedded English words don't corrupt into FM glyphs.
- **Rendering engine**: PyQt5's `QPainter`/`QFontMetrics` is used (not Pillow's text engine)
  because it measures and lays out the FM glyphs correctly. The finished `QImage` is
  converted to a Pillow `Image` for compositing and PNG export.

---

## Features

- **Dual templates** — MAIN TAG (Topic + TAG + White beds) and SUB TAG (Topic + two-line TAG).
- **Live preview** — text is composited onto the actual template in real time (100 ms debounce).
- **Offline Singlish → Sinhala** conversion (no internet needed) with per-bed language toggle.
- **Automatic FM-font conversion** so Unicode input renders correctly for broadcast.
- **Auto-fit & manual adjustments** — text auto-compresses horizontally to fit its bed;
  operator can override with a **Horizontal Scale** slider (50–100%) and **Letter Spacing**
  slider (−10 to +30 px) on the selected TAG line.
- **Auto-expanding red Topic bed** — the red bar grows rightward to fit the title.
- **Multi-line TAG / White beds** with a dropdown selector to preview any specific line/pair.
- **Selective PNG generation** — export only the beds you need, as separate transparent PNGs.
- **Session workflow** — named sessions, JSON draft auto-save (default every 60 s), reload
  previous work, organized output folders.
- **Word-count validation** — warns when a bed exceeds its limit (Topic 12 / White 15 / TAG 20).
- **Keyboard shortcuts** — `Ctrl+N` new, `Ctrl+S` save, `Ctrl+O` open folder,
  `Ctrl+,` settings, `Ctrl+Del` clear, `F5` refresh preview.

---

## Tech stack

| Layer | Technology | Role |
|-------|-----------|------|
| Language | **Python 3.11+** | Application core |
| GUI | **Tkinter / ttk** | Main window, input beds, panels, dialogs |
| Text rendering | **PyQt5** (`QPainter`, `QFontDatabase`, `QFontMetrics`) | Correct FM-font glyph layout & rasterization |
| Imaging | **Pillow (PIL) ≥ 10** | Template load, alpha compositing, PNG export |
| Text conversion | Custom pure-Python modules | Singlish→Unicode and Unicode→FM ASCII |
| Packaging | **PyInstaller** | Single-file Windows `.exe` |
| Persistence | JSON (`config/`, session `draft.json`) | Settings & session drafts |

> ⚠️ **Dependency note:** `requirements.txt` currently lists only `Pillow` and `requests`,
> but **PyQt5 is a hard runtime dependency** ([text_renderer.py](core/text_renderer.py)
> exits if it can't import it). Install PyQt5 explicitly (`pip install PyQt5`) until it's
> added to `requirements.txt`. `requests` is present for potential update checks but isn't
> central to rendering.

---

## Architecture & project structure

The app follows a simple **GUI → core → utils** layering:

```
HiruTaglineCreator/
├── main.py                     # Entry point: load config, check fonts, launch window
│
├── gui/                        # Tkinter UI layer
│   ├── main_window.py          # Main window, the 3 input beds, adjustments, orchestration
│   ├── preview_panel.py        # Live composited preview + line/pair selectors
│   ├── generation_panel.py     # PNG generation, progress dialog, per-bed preview popups
│   └── settings_dialog.py      # Settings editor
│
├── core/                       # Business logic
│   ├── text_renderer.py        # PyQt5 FM-font rendering → PIL images (THE render engine)
│   ├── template_manager.py     # Template loading + hard-coded bed coordinates
│   ├── session_manager.py      # Session folders, draft.json auto-save, filenames
│   └── text_validator.py       # Per-bed word-count limits
│
├── utils/                      # Helpers
│   ├── fm_converter.py         # Unicode → FM ASCII (order-sensitive replace table)
│   ├── sinhala_unicode_converter.py  # Singlish → Sinhala Unicode (phonetic)
│   ├── font_finder.py          # Locate FM Ganganee/Sandhyanee .ttf on the machine
│   ├── font_checker.py         # Verify required fonts are installed at startup
│   ├── config_manager.py       # Load/merge settings JSON
│   ├── logger.py, tooltip.py   # Logging, UI tooltips
│   └── …                       # pillow_font_loader, windows_font_finder, etc.
│
├── templates/                  # MAIN_TAG.png / SUB_TAG.png (1920×1080 backplates)
├── assets/                     # app_icon.ico, placeholder_logo.png
├── config/                     # default_settings.json / settings.json
├── docs/                       # USER_GUIDE, FONT_INSTALLATION, CHANGELOG, workflow
├── logs/                       # Runtime log output
├── build_exe.py                # PyInstaller build script (current: v2.6)
├── HiruTaglineCreator_v*.spec  # PyInstaller spec files per version
└── dist/                       # Built executables (HiruTaglineCreator_v2.6.exe = latest)
```

**Startup flow** (`main.py`): load settings → verify FM fonts installed → load & validate
templates (must be 1920×1080) → init session manager → build main window → `mainloop()`.

---

## Templates & bed layout

Both templates are **1920×1080**. Text is drawn into fixed rectangular **beds** whose
pixel coordinates are defined in [core/template_manager.py](core/template_manager.py)
(`MAIN_TAG_BEDS` / `SUB_TAG_BEDS`) — these are the coordinates actually used at render time.

| Template | Beds | Notes |
|----------|------|-------|
| **MAIN TAG** | Topic (red, y=750, h=64, auto-width) · TAG (orange, x=140 y=814 w=1459 h=44) · White (x=141 y=898 w=1457 h=48) | Three-line lower-third |
| **SUB TAG** | Topic (red) · TAG (tall, h=141, **two text lines**) | No White bed |

- **Topic bed** grows rightward from x=126 up to a max width (1780 px), with 34 px padding,
  white text on `#a70003` red.
- **TAG/White** text is black (`#231F20`), left-aligned with 20 px padding, auto-compressed
  to fit and vertically centered.
- Font sizes are fixed to on-air spec: **Topic 50.4 px, TAG 60 px, White 48 px**
  (SUB TAG lines 50 px).

---

## Fonts

Two legacy FM broadcast fonts are **required** (they are not bundled — they must be
installed on the machine):

| Font | Used for | Detected file pattern |
|------|----------|-----------------------|
| **FM GANGANEE** | Topic bed | `*ganganee*.ttf` |
| **FM SANDHYANEE** | TAG & White beds | `*sandhyanee*.ttf` |

[utils/font_finder.py](utils/font_finder.py) searches `C:\Windows\Fonts` and the per-user
font folder (`%LOCALAPPDATA%\Microsoft\Windows\Fonts`) and loads them into PyQt5 via
`QFontDatabase.addApplicationFont`. If a font is missing, rendering falls back to Arial
(which will **not** shape Sinhala correctly). See [docs/FONT_INSTALLATION.md](docs/FONT_INSTALLATION.md).

---

## Configuration & sessions

- **Settings**: `config/default_settings.json` (shipped defaults) merged with
  `config/settings.json` (user overrides) via `ConfigManager`. Controls save location,
  auto-save interval, window size, date format, etc.
- **Sessions**: created under `C:/HiruTaglines/` by default as `SESSIONNAME_YYYY-MM-DD/`.
  Each session holds a `draft.json` (auto-saved, UTF-8, preserves both the raw Singlish and
  converted Unicode) and the exported PNGs.
- **Output filenames**: e.g. `TopicBed_2026-08-21.png`, `First_Three_Words_TAG_2026-08-21.png`,
  `..._WhiteBed_....png` (first three words of the text form the prefix).

---

## Running from source (development)

```bash
# 1. Install dependencies (note: PyQt5 is required in addition to requirements.txt)
pip install -r requirements.txt
pip install PyQt5

# 2. Ensure FM GANGANEE and FM SANDHYANEE fonts are installed on Windows

# 3. Run
python main.py
```

The app prints an **FM FONT VERIFICATION** block to the console on startup confirming which
`.ttf` files were loaded — check this first if Sinhala looks wrong.

---

## Building the executable

Built with **PyInstaller** in one-file, windowed mode. Two equivalent ways:

```bash
# Option A — the build script (bumps the version name here)
python build_exe.py

# Option B — the versioned spec file
pyinstaller HiruTaglineCreator_v2.6.spec
```

The build ([build_exe.py](build_exe.py)) bundles data folders and PIL hidden imports:

```
--onefile --windowed
--icon=assets/app_icon.ico
--name=HiruTaglineCreator_v2.6
--add-data=templates;templates
--add-data=assets;assets
--add-data=config;config
--hidden-import=PIL --hidden-import=PIL._tkinter_finder
--clean --noconfirm
```

Output lands in `dist/`. To cut a new version, bump the `--name` in `build_exe.py`
(and/or add a new `.spec`) and rebuild.

---

## The built product (.exe)

**Latest:** [`dist/HiruTaglineCreator_v2.6.exe`](dist/HiruTaglineCreator_v2.6.exe)

- **Single self-contained Windows executable** (~59 MB, UPX-compressed) — no Python install
  required on the target machine.
- **Windowed** (no console) with the Hiru app icon.
- **Bundles** the templates, assets, and config; the Python runtime, Tkinter, PyQt5, and
  Pillow are all packed inside.
- **Still requires the FM fonts** (Ganganee & Sandhyanee) to be installed on the target PC —
  fonts are intentionally not embedded.
- On launch it creates/uses `C:/HiruTaglines/` for sessions and output.

---

## System requirements

- **OS:** Windows 10 or later (Windows-only — relies on Windows font paths and `os.startfile`).
- **Fonts:** FM GANGANEE and FM SANDHYANEE installed.
- **RAM:** 4 GB minimum.
- **Disk:** ~500 MB free.
- **For development only:** Python 3.11+, PyQt5, Pillow, PyInstaller.

---

## User workflow — using the app

This is the end-to-end operator flow for the built executable
([`dist/HiruTaglineCreator_v2.6.exe`](dist/HiruTaglineCreator_v2.6.exe)). For deeper
operator instructions see [docs/USER_GUIDE.md](docs/USER_GUIDE.md) and
[USER_MANUAL.md](USER_MANUAL.md).

### 1. Launch
1. Make sure **FM GANGANEE** and **FM SANDHYANEE** are installed on the PC
   (see [docs/FONT_INSTALLATION.md](docs/FONT_INSTALLATION.md)).
2. Double-click **`HiruTaglineCreator_v2.6.exe`**. No installation is needed.
3. On startup the app verifies the FM fonts and loads the MAIN TAG / SUB TAG templates.
   If a font is missing you'll be warned — install it before continuing, otherwise Sinhala
   will not shape correctly.

### 2. Start a session
- Click **🆕 New** (top bar) and enter a session name (e.g. `AKUREGODA`). This creates a
  folder `SESSIONNAME_YYYY-MM-DD/` under `C:/HiruTaglines/` where all your PNGs and the
  auto-saved draft are kept.
- To resume earlier work, pick a session from the **Session** dropdown.
- Your work **auto-saves** (default every 60 s); **💾 Save** (or `Ctrl+S`) saves on demand.

### 3. Pick the template
Use the tabs on the left:
- **📺 MAIN TAG** — full lower-third: **Topic** (red) + **TAG** (orange) + **White** beds.
- **📋 SUB TAG** — **Topic** + a **two-line TAG** bed (no White bed).

### 4. Type your text
Enter text in each bed. Type in **Singlish** (e.g. `akuregoda`) and it is transliterated to
Sinhala automatically:
- **🔴 Topic Bed** — the single-line red title.
- **🟠 TAG Bed** — multi-line: **one headline per line** (paste multiple lines at once if you like).
- **⬜ White Bed** — the white sub-headline line(s) (MAIN TAG only).

Each bed shows a **yellow live-preview box** with the converted Sinhala and a **word count**
that turns red if it exceeds the bed's limit (Topic 12 / White 15 / TAG 20). Use the
**🇸🇮 Sinhala / 🌐 English** button on any bed to turn transliteration off and type raw text
(for embedded English words).

### 5. Watch the live preview
The right-hand **🎨 LIVE PREVIEW** panel composites your text onto the real template as you
type (brief pause to update). For multi-line TAG/White beds, use the **selector dropdown**
in the preview panel to choose which line (or SUB TAG pair) is shown.

### 6. Fine-tune (optional)
Under **🎛️ Text Adjustments** (applies to the selected TAG line):
- **Horizontal Scale** (50–100%) — compress the text width to fit gracefully. Leave at 100%
  to let it auto-fit. **🔄 Reset Scale** restores 100%.
- **Letter Spacing** (−10 to +30 px) — tighten or open up spacing. **🔄 Reset Spacing**
  restores 0.

### 7. Choose what to export (PNG Generation Panel)
Expand the **📸 PNG GENERATION PANEL** at the bottom left:
- Tick exactly which items to export — **Topic Bed**, individual **TAG lines**, and
  **White Bed** lines. Use **☑ Select All** / **☐ None** per group.
- A warning badge appears next to any line that exceeds its word limit.
- Click **👁️ Preview** next to any item to open a large popup showing exactly how that single
  PNG will render in isolation.
- The **SUMMARY** line shows how many items are selected.

### 8. Generate
- Click **📸 Generate Selected PNGs**.
- A **progress bar** counts through the render. Each selected bed/line is drawn onto its own
  transparent **1920×1080** canvas and saved as a separate PNG.
- Files are auto-named from the first three words + bed type + date, e.g.
  `TopicBed_2026-08-21.png`, `අකුරේගොඩ_නීතිඥවරයා_බිරිඳ_TAG_2026-08-21.png`.

### 9. Collect the output
- A **result summary** reports how many files exported (and any errors).
- Click **📂 Open Folder** (or the button in the summary) to open the session folder in
  Windows Explorer.
- Drag the transparent PNGs straight into your playout / graphics software
  (vMix, CasparCG, OBS, XPression, etc.) to key them over live video.

### Handy shortcuts
`Ctrl+N` new session · `Ctrl+S` save · `Ctrl+O` open folder · `Ctrl+,` settings ·
`Ctrl+Del` clear all · `F5` refresh preview.

---

## License & support

© 2026 Hiru News. All rights reserved.

- **Email:** vidath@lotustechnologies.lk
- **Website:** www.hirunews.lk
```
