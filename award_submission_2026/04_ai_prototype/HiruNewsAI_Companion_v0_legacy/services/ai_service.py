"""
AI Service — transcription and tagline generation.

Runs in a QThread so the UI stays responsive.
If DEMO_MODE=true (or no API key), returns realistic mock Sinhala data.
"""
import json
import time
from typing import List
from PyQt5.QtCore import QThread, pyqtSignal
from core.models import Session, TranscriptSegment, TaglineSet

# ---------------------------------------------------------------------------
# Mock data — realistic Sinhala broadcast content for demo / no-API mode
# ---------------------------------------------------------------------------

_MOCK_TRANSCRIPT: List[dict] = [
    {"speaker": "Anchor",   "start": 0.0,  "end": 8.5,
     "text": "ශ්‍රී ලංකාවේ දිත්වා සුළිසුළං නිසා දකුණු පළාත්වල ජනතාව ආරක්ෂිත ස්ථාන කරා ගෙන යාමේ කටයුතු ආරම්භ කෙරේ."},
    {"speaker": "Reporter", "start": 8.5,  "end": 21.0,
     "text": "රජය විසින් දිස්ත්‍රික්ක 5ක ජනතාවට ඉවත් කිරීමේ නියෝග නිකුත් කර ඇති අතර, හමුදා සහ පොලිස් බලකා ක්‍රියාත්මක කර ඇත."},
    {"speaker": "Anchor",   "start": 21.0, "end": 32.0,
     "text": "නාවික හමුදාව සහ ගුවන් හමුදාව මෙහෙයුම් ආරම්භ කර ඇති අතර, ආපදා කළමනාකරණ මධ්‍යස්ථාන ජනතාවට විවෘත කෙරේ."},
    {"speaker": "Reporter", "start": 32.0, "end": 45.5,
     "text": "ගාල්ල, මාතර, හම්බන්තොට, රත්නපුර සහ කළුතර දිස්ත්‍රික්කවල ගංවතුර අනතුරු ඇඟවීම් ක්‍රියාත්මකව ඇත."},
    {"speaker": "Anchor",   "start": 45.5, "end": 58.0,
     "text": "ජනාධිපති කාර්යාලය සහ ආපදා කළමනාකරණ ඇමතිවරයා සිව්රු ශාලාවේ රැස්වී ක්ෂණික ත්‍රිවිධ හමුදා සහය ලබා දෙන ලෙස නියෝග කළේය."},
]

_MOCK_TAGLINES: List[dict] = [
    {
        "topic_bed": "දිත්වා සුළිසුළං අනතුරු ඇඟවීම",
        "tag_lines":  [
            "රජය ඉවත් කිරීමේ නියෝග නිකුත් කරයි",
            "දිස්ත්‍රික්ක 5ක ජනතාව ආරක්ෂිත ස්ථාන වෙත",
        ],
        "white_bed":  "හිරු පුවත් — රාත්‍රී 6.55",
        "source_text": "රජය විසින් දිස්ත්‍රික්ක 5ක ජනතාවට ඉවත් කිරීමේ නියෝග නිකුත් කර ඇති අතර...",
    },
    {
        "topic_bed": "හමුදා සහ පොලිස් ක්‍රියාත්මකයි",
        "tag_lines":  [
            "නාවික හමුදා මෙහෙයුම් ආරම්භ කෙරේ",
            "ආපදා මධ්‍යස්ථාන ජනතාවට විවෘතයි",
        ],
        "white_bed":  "හිරු පුවත් — රාත්‍රී 6.55",
        "source_text": "නාවික හමුදාව සහ ගුවන් හමුදාව මෙහෙයුම් ආරම්භ කර ඇති...",
    },
    {
        "topic_bed": "ගංවතුර අනතුරු ඇඟවීම ක්‍රියාත්මකයි",
        "tag_lines":  [
            "ගාල්ල, මාතර, හම්බන්තොට දිස්ත්‍රික්ක",
            "රත්නපුර හා කළුතරද ඇතුළත් වෙයි",
        ],
        "white_bed":  "හිරු පුවත් — රාත්‍රී 6.55",
        "source_text": "ගාල්ල, මාතර, හම්බන්තොට, රත්නපුර...",
    },
    {
        "topic_bed": "ජනාධිපති හදිසි රැස්වීමක් කැඳවයි",
        "tag_lines":  [
            "ත්‍රිවිධ හමුදා ක්ෂණික සහය ලබා දෙයි",
            "ආපදා ඇමති ජනාධිපති සමඟ සාකච්ඡාවේ",
        ],
        "white_bed":  "හිරු පුවත් — රාත්‍රී 6.55",
        "source_text": "ජනාධිපති කාර්යාලය සහ ආපදා කළමනාකරණ ඇමතිවරයා...",
    },
]


# ---------------------------------------------------------------------------
# QThread worker
# ---------------------------------------------------------------------------

class ProcessingWorker(QThread):
    progress = pyqtSignal(int, str)      # (percent, status_message)
    transcript_ready = pyqtSignal(list)  # list[TranscriptSegment]
    taglines_ready = pyqtSignal(list)    # list[TaglineSet]
    error = pyqtSignal(str)

    def __init__(self, session: Session, demo_mode: bool, api_key: str = ""):
        super().__init__()
        self.session = session
        self.demo_mode = demo_mode
        self.api_key = api_key

    def run(self):
        try:
            if self.demo_mode:
                self._run_demo()
            else:
                self._run_live()
        except Exception as exc:
            self.error.emit(str(exc))

    # ---- Demo mode --------------------------------------------------------

    def _run_demo(self):
        self.progress.emit(10, "Loading source material...")
        time.sleep(0.6)
        self.progress.emit(30, "Transcribing audio (demo mode)...")
        time.sleep(1.0)
        self.progress.emit(55, "Identifying speakers...")
        time.sleep(0.5)
        self.progress.emit(70, "Generating Sinhala taglines with AI...")
        time.sleep(1.2)
        self.progress.emit(90, "Validating content...")
        time.sleep(0.4)

        segments = [
            TranscriptSegment(
                speaker=d["speaker"],
                start_time=d["start"],
                end_time=d["end"],
                text=d["text"],
            )
            for d in _MOCK_TRANSCRIPT
        ]

        tagline_sets = []
        for i, d in enumerate(_MOCK_TAGLINES, start=1):
            ts = TaglineSet(
                id=i,
                topic_bed=d["topic_bed"],
                tag_lines=list(d["tag_lines"]),
                white_bed=d["white_bed"],
                source_text=d["source_text"],
            )
            ts.validate()
            tagline_sets.append(ts)

        self.progress.emit(100, "Complete.")
        self.transcript_ready.emit(segments)
        self.taglines_ready.emit(tagline_sets)

    # ---- Live mode (OpenAI) ----------------------------------------------

    def _run_live(self):
        import openai
        client = openai.OpenAI(api_key=self.api_key)

        # Step 1 — transcription
        self.progress.emit(15, "Uploading audio to OpenAI Whisper...")
        with open(self.session.source_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
            )
        self.progress.emit(50, "Transcription complete. Building transcript...")

        segments = []
        for i, seg in enumerate(response.segments or []):
            speaker = f"Speaker {(i % 2) + 1}"
            segments.append(TranscriptSegment(
                speaker=speaker,
                start_time=float(seg.start),
                end_time=float(seg.end),
                text=seg.text.strip(),
            ))

        self.transcript_ready.emit(segments)
        self.progress.emit(65, "Generating Sinhala taglines with GPT-4o...")

        # Step 2 — tagline generation via GPT-4o
        full_text = "\n".join(
            f"{seg.speaker} [{seg.start_time:.1f}s]: {seg.text}"
            for seg in segments
        )
        bulletin_slot = self.session.bulletin_slot
        prompt = (
            "You are an expert Sinhala broadcast journalist for Hiru News, Sri Lanka.\n\n"
            "Analyse the following news transcript and generate broadcast taglines in Sinhala Unicode.\n\n"
            f"TRANSCRIPT:\n{full_text}\n\n"
            "Generate up to 4 tagline sets. Return valid JSON matching this schema exactly:\n"
            '{"tagline_sets": [{"topic_bed": "<Sinhala, max 6 words>", '
            '"tag_lines": ["<Sinhala line, max 10 words>", "<Sinhala line, max 10 words>"], '
            f'"white_bed": "හිරු පුවත් — {bulletin_slot}", '
            '"source_text": "<key sentence from transcript>"}]}\n\n'
            "Rules: all Sinhala Unicode, factual, broadcast-appropriate, no opinion, JSON only."
        )

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        self.progress.emit(90, "Validating generated taglines...")

        raw = json.loads(completion.choices[0].message.content)
        tagline_sets = []
        for i, d in enumerate(raw.get("tagline_sets", []), start=1):
            ts = TaglineSet(
                id=i,
                topic_bed=d.get("topic_bed", ""),
                tag_lines=d.get("tag_lines", []),
                white_bed=d.get("white_bed", f"හිරු පුවත් — {bulletin_slot}"),
                source_text=d.get("source_text", ""),
            )
            ts.validate()
            tagline_sets.append(ts)

        self.progress.emit(100, "Complete.")
        self.taglines_ready.emit(tagline_sets)
