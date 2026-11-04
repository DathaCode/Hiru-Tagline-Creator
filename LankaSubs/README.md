# LankaSubs – AI subtitles for Sinhala, Tamil & English videos

Upload a video → pick the subtitle language → Gemini listens, detects the spoken
language and translates → review/edit the lines → burn them into a new MP4.

Works for every combination: Sinhala ⇄ English, Sinhala ⇄ Tamil, English ⇄ Tamil,
and mixed-language speech.

## 1. Build the .exe (one time, on a Windows PC)

1. Install **Python 3.11 or newer** from https://python.org (tick *"Add python.exe to PATH"*).
2. Unzip this folder, then double-click **`build.bat`**.
   It installs the libraries, downloads FFmpeg, and builds the app (about 5–10 minutes).
3. Your app is at **`dist\LankaSubs\LankaSubs.exe`**. Zip the whole `dist\LankaSubs`
   folder to share it with your team. They don't need Python.

## 2. Get a Gemini API key (free)

1. Go to https://aistudio.google.com and sign in with a Google account.
2. Click **Get API key → Create API key**, and copy it.
3. In LankaSubs, click **⚙ Settings**, paste the key, and Save.

Each team member can use their own key (free-tier limits are per Google project,
so separate keys = separate limits).

## 3. Using the app

1. **Browse video…** and choose the language the subtitles should be in.
2. (Optional) Add context, e.g. *"news interview, speakers Kamal and Nirosha"*.
   Names and topic help Gemini translate more accurately.
3. Click **✨ Generate subtitles**. Long videos are processed in 5-minute parts.
4. Review the table. Edit text and times, add or delete lines.
   Double-click a time to play from there; the preview shows the current subtitle.
5. Set font size / position, then **🎬 Burn subtitles & save video**.

**Export SRT** saves the subtitles separately (handy as a backup or for YouTube);
**Import SRT** loads them back later.

## Notes

- **Privacy:** on Gemini's free tier, Google may use uploaded audio to improve its
  models. For confidential footage, enable billing on the key (paid tier).
- **Models:** `gemini-3.5-flash` (default) is fast and free-tier. Try `gemini-2.5-pro`
  in Settings if a difficult video comes out poorly (paid).
- **Fonts:** Noto Sans Sinhala / Tamil / Latin are bundled (SIL Open Font License).
  To use another font, put its .ttf in `fonts` and change the font names in
  `LANGUAGES` at the top of `engine.py`.
- **Broken Sinhala letters in the output video?** Your FFmpeg build lacks HarfBuzz.
  Replace `bin\ffmpeg.exe` with the *full* build from https://www.gyan.dev/ffmpeg/builds/.
- **"429 / quota" errors:** the app retries automatically; if it keeps failing,
  you've hit the free daily limit. Wait or enable billing.

## Files

| File | Purpose |
|---|---|
| `main.py` | Desktop window (PySide6): picker, editor, preview, export |
| `engine.py` | FFmpeg audio extraction, Gemini prompt, SRT/ASS, burn-in |
| `build.bat` | Builds `LankaSubs.exe` with PyInstaller |
| `run_dev.bat` | Runs from source while you make changes |
| `fonts/` | Bundled Sinhala/Tamil/Latin fonts |
| `bin/` | `ffmpeg.exe` goes here |
