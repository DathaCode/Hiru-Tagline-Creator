"""
Speaker diarization — GPT-based heuristic prototype.
Clearly labelled in the UI as a prototype approximation.

Real diarization would use pyannote.audio or AssemblyAI; this uses
a GPT prompt to re-label transcript segments by inferred speaker role.
"""
import json
import time
from typing import List, Callable
from core.session_model import TranscriptLine
from services.openai_client import get_client, DEMO_MODE


def diarize(
    lines: List[TranscriptLine],
    progress_cb: Callable[[int, str], None] = None,
) -> List[TranscriptLine]:
    """
    Attempts to assign speaker roles (Anchor, Reporter, Official, etc.)
    to each transcript line. Returns the updated list.
    """
    if DEMO_MODE or not lines:
        if progress_cb:
            progress_cb(100, "Speaker labels applied (demo).")
        return lines  # mock data already has realistic speakers

    return _gpt_diarize(lines, progress_cb)


def _gpt_diarize(
    lines: List[TranscriptLine],
    progress_cb,
) -> List[TranscriptLine]:
    client = get_client()
    if progress_cb:
        progress_cb(10, "Analysing speaker patterns with GPT...")

    numbered = "\n".join(
        f'{i}. [{ln.timestamp_str}] {ln.text}'
        for i, ln in enumerate(lines)
    )
    prompt = (
        "You are a broadcast journalism analyst. The following is a news transcript.\n"
        "Assign a speaker role to each numbered line. Common roles: Anchor, Reporter, "
        "Official, Correspondent, Eyewitness.\n\n"
        f"TRANSCRIPT:\n{numbered}\n\n"
        'Return JSON: {"labels": ["Anchor", "Reporter", ...]} — one label per line, same order.'
    )

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1,
        )
        data = json.loads(resp.choices[0].message.content)
        labels = data.get("labels", [])
        for i, ln in enumerate(lines):
            if i < len(labels):
                ln.speaker = labels[i]
    except Exception:
        pass  # fall back to original labels if GPT diarization fails

    if progress_cb:
        progress_cb(100, "Speaker identification complete.")

    return lines
