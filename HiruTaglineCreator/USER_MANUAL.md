# 🎬 Hiru News Tagline Creator v1.1 - User Manual

## Overview
Hiru News Tagline Creator is a specialized broadcasting tool designed to generate transparent PNG overlays for news graphic templates. It supports both **MAIN TAG** and **SUB TAG** layouts natively and performs advanced Sinhala Unicode text manipulations entirely offline.

## Core Features
### 1. Dual Template Support
- Toggle seamlessly between **MAIN TAG** (Topic, Tags, and White bed) and **SUB TAG** (Topic and Tags only, no White bed).
- UI inputs dynamically adapt based on the selected layout style.

### 2. Offline Singlish to Sinhala Unicode Converter
- Type naturally in Singlish (e.g., `pravruthi sakachchawa`) to automatically convert text into pristine Sinhala Unicode typography without hitting external APIs.
- Includes perfect translation rules for complex modifier conjuncts like Rakaransaya and Yansaya.

### 3. Language Toggle Switch
- Every input bed has an individual language toggle button to flip between Sinhala conversion mode (Singlish) and raw English text mode.

### 4. True 1:1 Live Visual Preview
- See an exact rendering preview of your final text overlay visually mapped against the official red/orange/white broadcast background templates.
- Features live character and bounding line counters to keep texts perfectly fitted.

### 5. Layout Engine
- Mathematical alignment ensures texts perfectly hug the exact left margins inside transparent pixel boxes.
- **Dynamic Down-scaling**: Auto-shrinks long typography mathematically strictly to prevent overlapping outside the right-side TAG boundaries.
- **Always-Bold Rendering**: All beds render flawlessly in Bold weight utilizing reliable layout libraries to prevent clipping of complex Sinhala ascenders and descenders.

## Text Adjustments Panel
If your texts are fitting awkwardly or letters appear squashed, utilize the `Text Adjustments` panel before generating:
- **Horizontal Scale**: Compress the text mathematically via percentage (e.g. `90%`) manually to squash long sentences entirely horizontally without scaling down their absolute vertical font size.
- **Letter Spacing**: Use the new slider to increase padding (spacing between letters) up to +30 pixels to restore legibility on condensed layouts.

## Generating PNGs
In the right-side GENERATION PANEL, you can manage your final outputs:
1. **Selective Toggles**: Enable or disable specific beds individually (e.g. uncheck Topic Bed to only export the TAG bed text line).
2. **Export with True Alpha**: Click **"Generate Selected PNGs"**. The app executes a direct pass outputting flawless PNG files with full 100% background transparency, ensuring only the isolated text renders without rigid background boxes.
3. Automatically opens the folder location containing your generated files.

## Session Management
- **Automatic Background Saving**: Project changes instantly auto-save locally over 60 seconds protecting against data loss.
- **Workspaces**: Create named sessions sets (e.g., "Press Conference 1") and switch interchangeably between isolated instances utilizing the top "Session" dropdown menu.
- **Quick Shortcuts**: Hit `Ctrl+S` to save explicitly, `Ctrl+N` for a new Draft, or `Ctrl+O` to rapidly map to the output folder.
