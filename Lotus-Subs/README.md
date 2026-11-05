# LotusSubs – AI subtitles on the Hiru SUB TAG bed

Open a video → pick the subtitle language → Gemini listens, detects the spoken
language and translates → review/edit the lines → burn them into a new MP4.

Every subtitle is shown on the orange **SUB TAG bed** from HiruTaglineCreator, at the
exact position the SUB TAG template uses on a 1920×1080 frame. The red title bar is not
used. The bed appears only while someone is speaking, and holds up to two lines.

Works for every combination: Sinhala ⇄ English, Sinhala ⇄ Tamil, English ⇄ Tamil,
and mixed-language speech.

## 1. Build the .exe (one time, on a Windows PC)

1. Install **Python 3.11 or newer** from https://python.org (tick *"Add python.exe to PATH"*).
2. Unzip this folder, then double-click **`build.bat`**.
   It installs the libraries, downloads FFmpeg, and builds the app (about 5–10 minutes).
3. Your app is at **`dist\LotusSubs\LotusSubs.exe`**. Zip the whole `dist\LotusSubs`
   folder to share it with your team. They don't need Python.

## 2. Get a Gemini API key (free)

1. Go to https://aistudio.google.com and sign in with a Google account.
2. Click **Get API key → Create API key**, and copy it.
3. In LotusSubs, click **⚙ Settings**, paste the key, and Save.

Each team member can use their own key (free-tier limits are per Google project,
so separate keys = separate limits).

## 3. Using the app

1. **Open video…** (or drop a video on the window) and choose the language the
   subtitles should be in.
2. (Optional) Add context, e.g. *"news interview, speakers Kamal and Nirosha"*.
   Names and topic help Gemini translate more accurately.
3. Click **✨ Generate subtitles**. Long videos are processed in 5-minute parts.
4. Review the table. The preview shows the SUB TAG bed exactly as it will be burned.
   - Click a line to preview it; double-click a time to play from there.
   - Edit a subtitle and press **Enter** to save; **Shift+Enter** starts line 2.
   - **Amber** = the line is squeezed narrower to fit; **red** = too long for the bed, shorten it.
5. **🎬 Burn SUB TAG video** saves a new MP4 next to the original (`…_subtag.mp4`).

**＋ New session** (Ctrl+N) clears the video and all subtitles in one click.
**Export SRT** saves the subtitles separately (handy as a backup or for YouTube);
**Import SRT** loads them back later. A long imported line is split onto two lines automatically.

## Notes

- **Layout:** the bed's position and the text's size and spacing are set at the top of
  `subtag.py`. Videos that aren't 16:9 get the same layout scaled to the video width and
  anchored to the bottom.
- **Fonts:** subtitles use Noto Sans Sinhala / Tamil / Latin Bold, bundled in `fonts`
  (SIL Open Font License).
- **Privacy:** on Gemini's free tier, Google may use uploaded audio to improve its
  models. For confidential footage, enable billing on the key (paid tier).
- **Models:** `gemini-3.5-flash` (default) is fast and free-tier. Try `gemini-2.5-pro`
  in Settings if a difficult video comes out poorly (paid).
- **"429 / quota" errors:** the app retries automatically; if it keeps failing,
  you've hit the free daily limit. Wait or enable billing.

## Files

| File | Purpose |
|---|---|
| `main.py` | Desktop window (PySide6): video, editor, live SUB TAG preview, export |
| `subtag.py` | Draws a subtitle on the SUB TAG bed (used by the preview and the burn) |
| `engine.py` | FFmpeg audio extraction, Gemini prompt, SRT, burn-in |
| `assets/logo.png` | App logo: window, taskbar and .exe icon, header, empty preview |
| `assets/subtag_bed.png` | The orange bed, cut from HiruTaglineCreator's `templates/SUB_TAG.png` |
| `build.bat` | Builds `LotusSubs.exe` with PyInstaller |
| `run_dev.bat` | Runs from source while you make changes |
| `fonts/` | Bundled Sinhala/Tamil/Latin fonts |
| `bin/` | `ffmpeg.exe` goes here (not in git – it's over GitHub's 100 MB limit) |
