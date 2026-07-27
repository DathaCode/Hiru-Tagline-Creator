"""
Data models for HiruNews AI Streamline prototype.
"""
from dataclasses import dataclass, field
from typing import List
import datetime


@dataclass
class TranscriptSegment:
    speaker: str          # e.g. "Speaker 1", "Anchor", "Reporter"
    start_time: float     # seconds
    end_time: float
    text: str             # Sinhala or English text

    @property
    def timestamp(self) -> str:
        start = str(datetime.timedelta(seconds=int(self.start_time)))[2:]
        end   = str(datetime.timedelta(seconds=int(self.end_time)))[2:]
        return f"[{start} – {end}]"


@dataclass
class TaglineSet:
    """One complete tagline set: topic bed + tag lines + white bed."""
    id: int
    topic_bed: str = ""          # Sinhala — FM GANGANEE, red background
    tag_lines: List[str] = field(default_factory=list)   # Sinhala lines
    white_bed: str = ""          # Sinhala — white background
    source_text: str = ""        # the transcript passage this came from
    word_warnings: List[str] = field(default_factory=list)  # validation messages

    def validate(self):
        self.word_warnings.clear()
        topic_words = len(self.topic_bed.split()) if self.topic_bed else 0
        if topic_words > 8:
            self.word_warnings.append(f"Topic Bed: {topic_words} words (max 8 recommended)")
        for i, line in enumerate(self.tag_lines, 1):
            w = len(line.split()) if line else 0
            if w > 12:
                self.word_warnings.append(f"TAG Line {i}: {w} words (max 12 recommended)")


@dataclass
class Session:
    """Represents one bulletin processing session."""
    bulletin_slot: str = "6:55 PM"      # "11:55 AM", "6:55 PM", "9:55 PM"
    priority: str = "Normal"             # "Normal", "Breaking News", "Developing"
    source_type: str = "Audio Recording" # "Audio Recording", "Video", "Press Release", "Text"
    source_path: str = ""
    source_text: str = ""                # for text/press release input
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    transcript: List[TranscriptSegment] = field(default_factory=list)
    tagline_sets: List[TaglineSet] = field(default_factory=list)
    approved: bool = False
    approved_by: str = ""
    approved_at: str = ""
    approval_notes: str = ""

    @property
    def session_id(self) -> str:
        dt = datetime.datetime.fromisoformat(self.created_at)
        slot = self.bulletin_slot.replace(":", "").replace(" ", "")
        return f"{dt.strftime('%Y%m%d')}_{slot}"

    @property
    def full_transcript_text(self) -> str:
        return "\n".join(
            f"{seg.speaker} {seg.timestamp}: {seg.text}"
            for seg in self.transcript
        )
