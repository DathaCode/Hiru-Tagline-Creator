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

---

## 📌 How to Use the SUB TAG Feature

The **SUB TAG** layout is used when you need **two lines of text per TAG PNG** — typically for longer news taglines that span two rows on the broadcast graphic.

### Key Differences from MAIN TAG

| Feature        | MAIN TAG                      | SUB TAG                              |
|----------------|-------------------------------|--------------------------------------|
| TAG Bed Lines  | 1 line per PNG                | **2 lines per PNG** (paired)         |
| White Bed      | ✅ Available                  | ❌ Hidden (not used)                 |
| Topic Bed      | ✅ Available                  | ✅ Available (same as MAIN TAG)      |
| TAG Bed Height | Single-line (thin orange bar) | Double-line (taller orange bar)      |

### Step-by-Step Workflow

#### Step 1: Switch to SUB TAG Tab
- Click the **"SUB TAG"** tab at the top of the application.
- The White Bed input field will automatically **hide**.
- The Generation Panel will switch to **paired mode**.

#### Step 2: Enter Topic Text
- Type your topic in the **Topic Bed** input field (same as MAIN TAG).
- Example: `මැදපෙරදිග අර්බුදය`

#### Step 3: Paste TAG Lines (2 Lines Per TAG)
- In the **TAG BED** text area, paste your tag lines.
- Every **2 consecutive lines** will be grouped into **one PNG**.

**Example input (6 lines → 3 PNGs):**
```
ඕවුන් දැනටමත් යුරෝපීය රටක් වන සයිප්‍රසය වෙත
ප්‍රහාර එල්ල කරනු ලැබුවා
ශ්‍රම වාසනා අරමුදල ඈවර කරන්න
කැබිනට් මණ්ඩලයේ අනුමැතිය
වැලි හිඟතාවය නිසා
වැලි මිල ඉහළට
```

This produces:
| PNG   | Line 1 (Top)                                     | Line 2 (Bottom)                   |
|-------|--------------------------------------------------|-----------------------------------|
| PNG 1 | ඕවුන් දැනටමත් යුරෝපීය රටක් වන සයිප්‍රසය වෙත   | ප්‍රහාර එල්ල කරනු ලැබුවා          |
| PNG 2 | ශ්‍රම වාසනා අරමුදල ඈවර කරන්න                     | කැබිනට් මණ්ඩලයේ අනුමැතිය         |
| PNG 3 | වැලි හිඟතාවය නිසා                                | වැලි මිල ඉහළට                     |

#### Step 4: Review Paired Checkboxes
- The **Generation Panel** will show checkboxes for each **pair**, not individual lines.
- Example: `1-2. ඕවුන් දැනටමත්... / ප්‍රහාර එල්ල...`
- Uncheck any pair you don't want to generate.

#### Step 5: Preview
- Use the **"Selected TAG"** dropdown in the Preview Panel to cycle through pairs.
- The dropdown will show **"Pair 1", "Pair 2"**, etc.
- Click the **👁️** button next to any pair in the Generation Panel for a full preview popup.

#### Step 6: Generate PNGs
- Click **"📸 Generate Selected PNGs"**.
- Output files are saved to the active session folder.
- File order: `001_TopicBed_...` → `002_..._TAG_...` → `003_..._TAG_...` → etc.

### ⚠️ Important Notes

1. **Line Pairing Rule**: Lines are paired strictly in order — Line 1+2, Line 3+4, Line 5+6, and so on. If you have an **odd number** of lines, the last line will be paired with an empty second line.

2. **Line Order Matters**: Make sure your text lines are in the correct order before pasting. The first line of each pair appears on the **top row** of the orange bed, and the second line appears on the **bottom row**.

3. **No White Bed**: SUB TAG mode does not generate White Bed PNGs. If you need a White Bed, switch back to the MAIN TAG tab.

4. **Topic Bed Works the Same**: The Topic Bed (red bar) behaves identically in both MAIN TAG and SUB TAG modes.

