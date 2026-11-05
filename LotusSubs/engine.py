"""
LotusSubs engine
- Extracts audio from a video with FFmpeg
- Sends audio chunks to Gemini to transcribe + translate (Sinhala / Tamil / English)
- Reads/writes SRT
- Burns the SUB TAG overlay images into the video with FFmpeg
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from typing import Callable, List, Optional

# ---------------------------------------------------------------- languages ---

LANGUAGES = {
    "English": {"font": "Noto Sans", "script": "Latin script"},
    "Sinhala": {"font": "Noto Sans Sinhala", "script": "Sinhala Unicode script (සිංහල)"},
    "Tamil": {"font": "Noto Sans Tamil", "script": "Tamil Unicode script (தமிழ்)"},
}

DEFAULT_MODEL = "gemini-3.5-flash"
CHUNK_SECONDS = 300  # 5-minute audio chunks keep Gemini's timestamps accurate


class CancelledError(Exception):
    pass


@dataclass
class Cue:
    start: float      # seconds
    end: float        # seconds
    original: str     # what was spoken (source language)
    text: str         # subtitle shown on the video (target language)


# ------------------------------------------------------------------ paths ----

def resource_dir() -> str:
    """Folder with bundled read-only resources (fonts)."""
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def app_dir() -> str:
    """Folder next to the .exe (or the script)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def fonts_dir() -> str:
    return os.path.join(resource_dir(), "fonts")


def find_ffmpeg() -> str:
    exe = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
    for folder in (os.path.join(app_dir(), "bin"), os.path.join(resource_dir(), "bin")):
        candidate = os.path.join(folder, exe)
        if os.path.isfile(candidate):
            return candidate
    on_path = shutil.which("ffmpeg")
    if on_path:
        return on_path
    raise FileNotFoundError(
        "FFmpeg was not found. Put ffmpeg.exe inside the 'bin' folder next to LotusSubs.exe."
    )


_NO_WINDOW = 0x08000000 if os.name == "nt" else 0  # hide console windows on Windows


def _run(cmd: List[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, creationflags=_NO_WINDOW, **kw)


# ------------------------------------------------------------ video info -----

def probe_video(ffmpeg: str, video: str) -> dict:
    """Return {'duration': seconds, 'width': w, 'height': h} using ffmpeg -i output."""
    out = _run([ffmpeg, "-hide_banner", "-i", video]).stderr.decode("utf-8", "replace")
    info = {"duration": 0.0, "width": 1920, "height": 1080, "has_audio": "Audio:" in out}
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", out)
    if m:
        h, mi, s = m.groups()
        info["duration"] = int(h) * 3600 + int(mi) * 60 + float(s)
    m = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})", out)
    if m:
        info["width"], info["height"] = int(m.group(1)), int(m.group(2))
    # handle rotated phone videos (rotation metadata)
    if re.search(r"rotate\s*:\s*-?(90|270)", out) or re.search(r"rotation of -?(90|270)", out):
        info["width"], info["height"] = info["height"], info["width"]
    return info


# ------------------------------------------------------------- time utils ----

def parse_time(value) -> float:
    """Accepts 83.5, '83.5', '01:23.500', '1:23', '00:01:23,500'."""
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip().replace(",", ".")
    if not s:
        raise ValueError("empty time")
    parts = s.split(":")
    if len(parts) > 3:
        raise ValueError(f"bad time: {value}")
    total = 0.0
    for p in parts:
        total = total * 60 + float(p)
    return total


def fmt_srt_time(t: float) -> str:
    t = max(0.0, t)
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"



# ----------------------------------------------------------------- Gemini ----

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "detected_language": {"type": "string"},
        "segments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "start": {"type": "string"},
                    "end": {"type": "string"},
                    "original": {"type": "string"},
                    "translation": {"type": "string"},
                },
                "required": ["start", "end", "original", "translation"],
            },
        },
    },
    "required": ["detected_language", "segments"],
}


def build_prompt(target: str, duration: float, context_hint: str = "") -> str:
    script = LANGUAGES[target]["script"]
    hint = f"\nContext about this video from the user: {context_hint}\n" if context_hint else ""
    return f"""You are a professional subtitler for Sri Lankan film, TV and online video.
The attached audio is {duration:.1f} seconds long. The speech may be Sinhala, Tamil, English,
or a mix of them (code-switching is common).
{hint}
Do the following:
1. Transcribe ALL spoken dialogue in its original language, split into subtitle segments.
   Each segment should be one natural phrase or sentence, 1 to 7 seconds long and at most
   about 80 characters. Follow the real speech timing closely.
2. Translate each segment into {target}, written in {script}. Use natural, fluent {target}
   that a native speaker would expect in subtitles, keeping the meaning, tone and context
   of the whole conversation, not word-for-word. Keep personal names and place names.
   If a segment is already in {target}, put a clean version of it as the translation.
   The translation is shown on a two-line TV caption bar: write it as ONE or TWO lines,
   each at most about 40 characters, with a "\\n" line break between the two lines,
   breaking at a natural phrase boundary. Never more than two lines.
3. Timestamps are relative to the start of THIS audio, formatted MM:SS.mmm
   (e.g. 01:07.250), and must lie between 00:00.000 and the audio length.
4. Skip silence, music and background noise. Never invent dialogue that is not spoken.
5. Set detected_language to the main spoken language (e.g. "Sinhala").
If there is no speech at all, return an empty segments list."""


def _gemini_call(client, model: str, audio_bytes: bytes, prompt: str, retries: int = 4):
    from google.genai import types

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_json_schema=RESPONSE_SCHEMA,
    )
    last_err = None
    for attempt in range(retries):
        try:
            resp = client.models.generate_content(
                model=model,
                contents=[types.Part.from_bytes(data=audio_bytes, mime_type="audio/mp3"), prompt],
                config=config,
            )
            text = (resp.text or "").strip()
            text = re.sub(r"^```(?:json)?|```$", "", text).strip()
            return json.loads(text)
        except json.JSONDecodeError as e:
            last_err = e
        except Exception as e:  # network, 429 rate limit, 5xx ...
            last_err = e
            msg = str(e)
            if "API key" in msg or "PERMISSION_DENIED" in msg or "API_KEY_INVALID" in msg:
                raise RuntimeError("Gemini rejected the API key. Check it in Settings.") from e
            if "NOT_FOUND" in msg and "model" in msg.lower():
                raise RuntimeError(f"Model '{model}' was not found. Pick another model.") from e
        time.sleep(5 * (attempt + 1) ** 2)  # 5s, 20s, 45s ... (helps with free-tier limits)
    raise RuntimeError(f"Gemini request failed after {retries} tries: {last_err}")


def clean_cues(cues: List[Cue], total: Optional[float] = None) -> List[Cue]:
    cues = [c for c in cues if c.text.strip()]
    cues.sort(key=lambda c: c.start)
    for i, c in enumerate(cues):
        if total:
            c.start = min(max(0.0, c.start), total)
            c.end = min(c.end, total)
        if c.end <= c.start + 0.3:
            c.end = c.start + max(1.0, min(4.0, len(c.text) / 15))
        if i + 1 < len(cues) and c.end > cues[i + 1].start:
            c.end = max(c.start + 0.3, cues[i + 1].start - 0.05)
    return cues


def generate_subtitles(
    video: str,
    target: str,
    api_key: str,
    model: str = DEFAULT_MODEL,
    context_hint: str = "",
    progress: Callable[[int, str], None] = lambda p, m: None,
    is_cancelled: Callable[[], bool] = lambda: False,
) -> tuple[List[Cue], str]:
    """Returns (cues, detected_language)."""
    from google import genai

    if target not in LANGUAGES:
        raise ValueError(f"Unsupported target language: {target}")
    if not api_key:
        raise RuntimeError("No Gemini API key. Add it in Settings.")

    ffmpeg = find_ffmpeg()
    info = probe_video(ffmpeg, video)
    if not info["has_audio"]:
        raise RuntimeError("This video has no audio track.")
    duration = info["duration"] or CHUNK_SECONDS
    n_chunks = max(1, int((duration + CHUNK_SECONDS - 1) // CHUNK_SECONDS))

    client = genai.Client(api_key=api_key)
    all_cues: List[Cue] = []
    languages: dict = {}

    with tempfile.TemporaryDirectory(prefix="lotussubs_") as tmp:
        for i in range(n_chunks):
            if is_cancelled():
                raise CancelledError()
            offset = i * CHUNK_SECONDS
            length = min(CHUNK_SECONDS, duration - offset) if info["duration"] else CHUNK_SECONDS
            progress(int(100 * i / n_chunks), f"Extracting audio part {i + 1}/{n_chunks}…")

            chunk = os.path.join(tmp, f"chunk_{i:03d}.mp3")
            r = _run([ffmpeg, "-hide_banner", "-y", "-ss", str(offset), "-t", str(length),
                      "-i", video, "-vn", "-ac", "1", "-ar", "16000",
                      "-c:a", "libmp3lame", "-b:a", "48k", chunk])
            if r.returncode != 0 or not os.path.isfile(chunk):
                raise RuntimeError("FFmpeg could not extract audio:\n" +
                                   r.stderr.decode("utf-8", "replace")[-800:])

            progress(int(100 * (i + 0.3) / n_chunks),
                     f"Gemini is listening & translating part {i + 1}/{n_chunks}…")
            with open(chunk, "rb") as f:
                data = _gemini_call(client, model, f.read(), build_prompt(target, length, context_hint))

            lang = (data.get("detected_language") or "").strip()
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
            chunk_cues = []
            for seg in data.get("segments", []):
                try:
                    s, e = parse_time(seg["start"]), parse_time(seg["end"])
                except (ValueError, KeyError, TypeError):
                    continue
                chunk_cues.append(Cue(offset + s, offset + e,
                                      str(seg.get("original", "")).strip(),
                                      str(seg.get("translation", "")).strip()))
            all_cues.extend(clean_cues(chunk_cues, offset + length))

    progress(100, "Done")
    detected = max(languages, key=languages.get) if languages else "Unknown"
    return clean_cues(all_cues, info["duration"] or None), detected


# -------------------------------------------------------------------- SRT ---

def cues_to_srt(cues: List[Cue], use_original: bool = False) -> str:
    out = []
    for i, c in enumerate(cues, 1):
        out.append(f"{i}\n{fmt_srt_time(c.start)} --> {fmt_srt_time(c.end)}\n"
                   f"{(c.original if use_original else c.text).strip()}\n")
    return "\n".join(out)


def srt_to_cues(content: str) -> List[Cue]:
    cues = []
    blocks = re.split(r"\n\s*\n", content.replace("\r\n", "\n").replace("\ufeff", "").strip())
    for b in blocks:
        lines = [l for l in b.split("\n") if l.strip() != ""]
        for idx, line in enumerate(lines):
            m = re.match(r"\s*([\d:.,]+)\s*-->\s*([\d:.,]+)", line)
            if m:
                text = "\n".join(lines[idx + 1:]).strip()
                cues.append(Cue(parse_time(m.group(1)), parse_time(m.group(2)), "", text))
                break
    return cues


# ------------------------------------------------------------------- burn ----

def _overlay_geometry(width: int, height: int, bed_w: int, bed_h: int, bed_x: int, bed_y: int):
    """Bed size and position on this video. The 1920x1080 layout is scaled to the video
    width and anchored to the bottom, so 16:9 video gets the exact template position."""
    s = width / 1920
    ow, oh = max(2, round(bed_w * s)), max(2, round(bed_h * s))
    return ow, oh, round(bed_x * s), height - round((1080 - bed_y) * s)


def burn_subtitles(
    video: str,
    cues: List[Cue],
    output: str,
    render_overlay: Callable[[str, str], None],
    bed: tuple,
    quality_crf: int = 20,
    progress: Callable[[int, str], None] = lambda p, m: None,
    is_cancelled: Callable[[], bool] = lambda: False,
) -> str:
    """render_overlay(text, png_path) writes one bed image; text "" means transparent.
    bed = (bed_w, bed_h, bed_x, bed_y) in 1920x1080 units.
    Each cue's bed is shown only from its start to its end time."""
    ffmpeg = find_ffmpeg()
    info = probe_video(ffmpeg, video)
    duration = info["duration"] or 1.0

    with tempfile.TemporaryDirectory(prefix="lotussubs_burn_") as tmp:
        render_overlay("", os.path.join(tmp, "blank.png"))
        entries, t = [], 0.0
        for i, c in enumerate(cues):
            if is_cancelled():
                raise CancelledError()
            progress(int(5 * i / max(1, len(cues))), f"Drawing subtitle {i + 1}/{len(cues)}…")
            name = f"sub_{i:05d}.png"
            render_overlay(c.text, os.path.join(tmp, name))
            if c.start > t:
                entries.append(("blank.png", c.start - t))
            start = max(c.start, t)
            if c.end > start:
                entries.append((name, c.end - start))
                t = c.end
        entries.append(("blank.png", max(1.0, duration - t)))
        with open(os.path.join(tmp, "overlay.ffconcat"), "w", encoding="utf-8") as f:
            f.write("ffconcat version 1.0\n")
            for name, dur in entries:
                f.write(f"file '{name}'\nduration {dur:.3f}\n")
            f.write("file 'blank.png'\n")  # the concat demuxer drops the last duration

        ow, oh, ox, oy = _overlay_geometry(info["width"], info["height"], *bed)
        graph = (f"[1:v]format=rgba,scale={ow}:{oh}[bed];"
                 f"[0:v][bed]overlay={ox}:{oy}:eof_action=pass:format=auto,format=yuv420p[v]")
        # Relative paths: the overlay images are referenced from inside tmp.
        cmd = [ffmpeg, "-hide_banner", "-y", "-i", os.path.abspath(video),
               "-f", "concat", "-safe", "0", "-i", "overlay.ffconcat",
               "-filter_complex", graph, "-map", "[v]", "-map", "0:a?",
               "-c:v", "libx264", "-preset", "medium", "-crf", str(quality_crf),
               "-c:a", "aac", "-b:a", "192k",
               "-movflags", "+faststart", "-progress", "pipe:1", "-nostats",
               os.path.abspath(output)]
        log_path = os.path.join(tmp, "ffmpeg.log")
        with open(log_path, "wb") as log:
            proc = subprocess.Popen(cmd, cwd=tmp, stdout=subprocess.PIPE, stderr=log,
                                    creationflags=_NO_WINDOW)
            for raw in proc.stdout:
                if is_cancelled():
                    proc.kill()
                    proc.wait()
                    try:
                        os.remove(output)
                    except OSError:
                        pass
                    raise CancelledError()
                line = raw.decode("utf-8", "replace").strip()
                if line.startswith("out_time_us=") or line.startswith("out_time_ms="):
                    try:
                        t = int(line.split("=")[1]) / 1_000_000
                        pct = min(99, 5 + int(95 * t / duration))
                        progress(pct, f"Burning subtitles… {pct}%")
                    except ValueError:
                        pass
            proc.wait()
        if proc.returncode != 0:
            with open(log_path, "rb") as f:
                tail = f.read().decode("utf-8", "replace")[-1500:]
            raise RuntimeError("FFmpeg failed while burning subtitles:\n" + tail)

    progress(100, "Video saved")
    return output
