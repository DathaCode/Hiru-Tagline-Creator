---
name: tagline-app
description: Architecture and behaviour of the HiruTaglineCreator desktop app — GUI panels, bed geometry, preview, PNG generation, templates and sessions. Use when changing anything outside the Sinhala converter, such as the UI, bed positions, text scaling, filenames or the session folder layout.
---

# HiruTaglineCreator — app architecture

Windows desktop tool that turns Sinhala text into 1920×1080 broadcast tagline PNGs for
Hiru News. **Working copy: `HiruTaglineCreator/`** (see the folder table below).

## Stack, and the one surprising thing about it

- **Tkinter** for the whole UI (`gui/`).
- **PyQt5 for text rendering only** — `core/text_renderer.py` draws with `QPainter` /
  `QFont` / `QImage` into a `QImage`, then converts to PIL for compositing. Qt is used
  because it shapes and letter-spaces FM text correctly; Tk cannot. A headless
  `QGuiApplication` is created at import time.
- **Pillow** composites text over the template PNG and writes the file.
- Python 3.14, PyInstaller `--onefile`.

## Layout

```
main.py                    entry: config → font check → templates → session → MainWindow
gui/main_window.py         window, the three bed input widgets, Sinhala/Singlish toggle
gui/preview_panel.py       live preview canvas, zoom, TAG/White line selectors, warnings
gui/generation_panel.py    checkbox list of lines, per-line preview, batch PNG generation
gui/settings_dialog.py     bed geometry / font / colour editor → config/settings.json
core/text_renderer.py      Unicode → FM → Qt render → PIL composite   ← all rendering
core/text_validator.py     word-count limits: topic 12, white 15, tag 20
core/template_manager.py   loads templates/MAIN_TAG.png, templates/SUB_TAG.png (1920×1080)
core/session_manager.py    session folders + draft.json autosave
utils/fm_converter.py      Sinhala Unicode → FM bytes   ← see ../sinhala-fm-converter/
utils/sinhala_unicode_converter.py   offline Singlish → Sinhala Unicode (typing aid)
utils/font_finder.py, windows_font_finder.py, pillow_font_loader.py, font_checker.py
config/settings.json       live config (bed geometry, fonts, colours, paths)
config/default_settings.json   factory reset values
templates/                 MAIN_TAG.png, SUB_TAG.png
```

## The three beds

| Bed | Font | Size | Colour | Notes |
|---|---|---|---|---|
| TOPIC | FM GANGANEE | 50.4 pt | white on `#a70003` | red background box **grows with the text**, between `width_min` 370 and `width_max` 1110 (MAIN) / 1477 (SUB) |
| TAG | FM SANDHYANEE | 60 pt | black | MAIN: one line. SUB: two lines at 50 pt |
| WHITE | FM SANDHYANEE | 48 pt | black | h-scale and letter-spacing are **forced to defaults** in `render_white_bed_text()` — a deliberate revert after the user rejected the change on 2026-04-29 |

Geometry lives in `config/settings.json` under `beds.main_tag` / `beds.sub_tag`, per bed:
`x`, `y`, `width`, `height`, colours, font. Do not hard-code positions in the renderer.

**Text scaling.** Short text renders at natural size (scale 1.0, never stretched). Long
text is compressed **horizontally only**, floor 0.5. A manual H-Scale slider value other
than 100 overrides the auto-fit.

**Mixed English.** `convert_unicode_to_fm()` escapes `A-Za-z` into a PUA range so FM rules
cannot mangle them; `split_fm_and_english()` splits the result into runs and the renderer
draws English runs in a normal bold English font.

## MAIN_TAG vs SUB_TAG

`SUB_TAG` pairs TAG BED lines into two-line tags, and the pairing is **empty-line
delimited** (changed 2026-05-15 from sequential pairing). Consequences that are easy to
re-break:

- `TagBedInput.get_lines(preserve_empty=True)` must be used for SUB_TAG, otherwise blank
  lines are filtered out and the pairing collapses. Four call sites need it:
  `get_tag_lines_for_rendering()`, `_on_tag_text_change()`, `update_preview()` and
  `generation_panel`.
- Pair lookup uses `pair_lines[selected_index]`, **not** `selected_index * 2` arithmetic.
- Pairs where both lines are empty are skipped in the selector.
- SUB_TAG output filenames use `_SUB_`, not `_TAG_`; the name prefix falls back to line 2
  when line 1 is empty.

## Output

Generated into the session folder:

```
<default_save_location>/<session>/NNN_<prefix>_TAG_<date>.png
                                 NNN_<prefix>_SUB_<date>.png
                                 NNN_<prefix>_WhiteBed_<date>.png
                                 NNN_TopicBed_<date>.png
                                 draft.json          autosaved every 60 s
```

`session.default_save_location` in settings.json is currently
`F:/AIML projects/tagline creator outputs`.

## Fonts

FM Ganganee and FM Sandhyanee must be installed. `font_checker.check_fonts_installed()`
runs at startup and exits if they are missing. Paths are hard-coded first, then searched:

```
C:\Users\Hp\AppData\Local\Microsoft\Windows\Fonts\FMGanganee x.ttf
C:\Users\Hp\AppData\Local\Microsoft\Windows\Fonts\FMSandhyanee x.ttf
```

Per-user font installs (`AppData\Local\...\Fonts`) are invisible to some APIs — that is why
`windows_font_finder.py` exists. `pillow_font_loader.py` reports whether Raqm shaping is
available.

## Folders in the repo root

| Folder | What it is |
|---|---|
| `HiruTaglineCreator/` | **the working copy** — edit here |
| `award_submission_2026/` | SLASSCOM SNIA 2026 package (document, brochure, video script, AI prototype) |
| `award_submission_2026/HiruTaglineCreator_v3.1_src/` | the award fork of the app; receives `fm_converter.py` fixes |
| `config/` | a stray root-level `settings.json`; the app reads `HiruTaglineCreator/config/` |
