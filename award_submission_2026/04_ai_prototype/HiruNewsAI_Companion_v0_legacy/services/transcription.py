"""
Transcription service — OpenAI Whisper or mock.
"""
import time
from typing import List, Callable
from core.session_model import TranscriptLine
from services.openai_client import get_client, DEMO_MODE

# Realistic mock transcript (Ditwa Cyclone scenario)
_MOCK_LINES = [
    (0.0,  8.5,  "Anchor",   "ශ්‍රී ලංකාවේ දිත්වා සුළිසුළං නිසා දකුණු පළාත්වල ජනතාව ආරක්ෂිත ස්ථාන කරා ගෙන යාමේ කටයුතු ආරම්භ කෙරේ."),
    (8.5,  21.0, "Reporter", "රජය විසින් දිස්ත්‍රික්ක 5ක ජනතාවට ඉවත් කිරීමේ නියෝග නිකුත් කර ඇති අතර, හමුදා සහ පොලිස් බලකා ක්‍රියාත්මක කර ඇත."),
    (21.0, 32.0, "Anchor",   "නාවික හමුදාව සහ ගුවන් හමුදාව මෙහෙයුම් ආරම්භ කර ඇති අතර, ආපදා කළමනාකරණ මධ්‍යස්ථාන ජනතාවට විවෘත කෙරේ."),
    (32.0, 45.5, "Reporter", "ගාල්ල, මාතර, හම්බන්තොට, රත්නපුර සහ කළුතර දිස්ත්‍රික්කවල ගංවතුර අනතුරු ඇඟවීම් ක්‍රියාත්මකව ඇත."),
    (45.5, 57.0, "Official", "ජනාධිපති කාර්යාලය සහ ආපදා කළමනාකරණ ඇමතිවරයා ක්ෂණික ත්‍රිවිධ හමුදා සහය ලබා දෙන ලෙස නියෝග කළේය."),
    (57.0, 68.0, "Anchor",   "ආපදා කළමනාකරණ මධ්‍යස්ථානය අනතුරු ඇඟවීම් කාලීනව ජනතාව දැනුවත් කිරීම සඳහා හිරු නාලිකාව සමඟ කටයුතු කරයි."),
]


def transcribe(
    source_path: str,
    progress_cb: Callable[[int, str], None] = None,
) -> List[TranscriptLine]:
    """
    Returns a list of TranscriptLine objects.
    Uses Whisper API if key is configured, otherwise returns mock data.
    """
    if progress_cb:
        progress_cb(10, "Preparing audio...")

    if DEMO_MODE:
        return _mock_transcribe(progress_cb)
    return _live_transcribe(source_path, progress_cb)


def _mock_transcribe(progress_cb) -> List[TranscriptLine]:
    steps = [
        (25, "Uploading to Whisper (demo)..."),
        (50, "Transcribing audio..."),
        (70, "Segmenting speakers..."),
        (90, "Finalising transcript..."),
    ]
    for pct, msg in steps:
        time.sleep(0.5)
        if progress_cb:
            progress_cb(pct, msg)

    return [
        TranscriptLine(speaker=spk, start=s, end=e, text=t)
        for s, e, spk, t in _MOCK_LINES
    ]


def _live_transcribe(source_path: str, progress_cb) -> List[TranscriptLine]:
    client = get_client()
    if progress_cb:
        progress_cb(20, "Uploading audio to OpenAI Whisper...")

    with open(source_path, "rb") as f:
        resp = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )

    if progress_cb:
        progress_cb(70, "Processing transcript segments...")

    lines = []
    for i, seg in enumerate(resp.segments or []):
        speaker = f"Speaker {(i % 2) + 1}"
        lines.append(TranscriptLine(
            speaker=speaker,
            start=float(seg.start),
            end=float(seg.end),
            text=seg.text.strip(),
        ))

    if progress_cb:
        progress_cb(90, "Transcript ready.")

    return lines
