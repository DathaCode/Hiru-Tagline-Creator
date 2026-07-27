# Hiru News Tagline Creator — User Workflow

This document outlines the end-to-end user process and operational workflow for creating and exporting broadcast-ready news taglines using the application.

## 1. Application Launch & Configuration Check
* **Font Verification**: Upon startup, the application silently checks if the required FM fonts (`FM GANGANEE` and `FM SANDHYANEE`) are present on the system. If they are missing or improperly installed, the user is warned (or views the status in **Settings ⚙️** > **Fonts** tab).
* **Settings Load**: The application loads the default properties (colors, dimensions, save locations) from `config/settings.json`.
* **Template Load**: The background templates (`MAIN_TAG.png`, `SUB_TAG.png`) are loaded for the live preview.

## 2. Session Management
Before creating graphics, the user manages their workspace session (top bar):
* **🆕 New**: Creates a new session folder (e.g., `YYYY-MM-DD_HHMMSS`) in the default save directory (configurable in Settings). All PNGs generated in this batch will be saved here.
* **Session Dropdown**: Allows the user to select and resume previously created sessions.
* **📂 Open Folder**: Opens the current session's directory in Windows File Explorer.
* **Auto-Save**: The application continuously runs a background auto-save to prevent data loss during long news typing sessions.

## 3. Template Selection
The user chooses the type of graphic they are building using the main tabs on the left:
* **📺 MAIN TAG**: Used for the primary, top-level news story. Displays all three text beds: Topic Bed, TAG Bed, and White Bed.
* **📋 SUB TAG**: Used for secondary news lines. Only displays the TAG Bed and White Bed (Topic Bed is hidden).

## 4. Data Entry & Live Preview
The user enters text into the assigned bed fields:
* **🔴 Topic Bed**: A single-line main headline. Text is typed in Sinhala.
* **🟠 TAG Bed**: A multi-line input where the user types or pastes multiple sub-headlines (one sentence per line).
* **⬜ White Bed**: A single-line secondary static display text.

**Real-time Interactivity**:
* **Auto-Convert Toggle**: When enabled, regular standard Unicode Sinhala input is automatically translated into the legacy FM font encoding format required by `FM GANGANEE` and `FM SANDHYANEE`.
* **Live Update**: As the user types, the UI waits for a brief pause (debounce) and then updates the **Live Preview Panel** on the right, overlaying the text accurately on the template graphic.

## 5. Fine-Tuning (Adjustments)
If the text doesn't look perfect, the user can use sliders to adjust the currently selected element (chosen via the "Selected TAG" dropdown in the preview panel):
* **Font Size**: Increase/decrease the text scale.
* **Letter / Word Spacing**: Widen or condense the text to fit the bed gracefully.
* **X Position**: Nudge the text left or right.

## 6. Review & Validation (PNG Generation Panel)
Once data entry is complete, the user expands the **PNG Generation Panel** at the bottom left.
* **Selection**: The user selects exactly which elements they want to export (Topic Bed, individual TAG lines, White Bed). Checkboxes allow generating a batch or just re-exporting a single corrected line.
* **Validation**: Next to each TAG line, the system provides a real-time warning badge (e.g., `⚠️ 14 words exceeds limit`) based on configurable word-count rules to ensure readability on TV screens.
* **Individual Previews**: The user can click the **👁️** (EYE) icon next to any line to open a large, dedicated popup window showing exactly how that specific PNG will render in isolation.

## 7. Execution & Export
* The user clicks **"📸 Generate Selected PNGs"**.
* A final logic check runs. If there are severe validation errors, it warns the user.
* A modal **Progress Bar** appears, counting through the rendering process.
* **Rendering Engine (`text_renderer.py`)**: For each checked line, the background bed (e.g., the red expanding Topic block or the transparent TAG bounds) is drawn. The text is auto-sized to fit the designated width, cleanly layered over a transparent `1920x1080` canvas, and saved as an individual PNG.
* **File Naming**: Output PNGs are auto-named using the first 3 words of the text, the bed type, and the date (e.g., `අකුරේගොඩදී-නීතිඥවරයා-බිරිඳ_TAG_2026-02-23.png`).

## 8. Completion
* A **Result Summary Dialog** appears, showing how many files successfully exported and listing any internal errors on separate tabs.
* The user can click "Open Folder" from this dialogue to immediately retrieve their transparent `.png` files, which are now ready to be dragged directly into the TV station's broadcasting software (vMix, OBS, CasparCG, etc).
