"""
Session data model — single source of truth for one processing run.
"""
import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class TranscriptLine:
    speaker: str
    start: float   # seconds
    end: float
    text: str

    @property
    def timestamp_str(self) -> str:
        def fmt(s):
            m, sec = divmod(int(s), 60)
            return f"{m}:{sec:02d}"
        return f"[{fmt(self.start)} – {fmt(self.end)}]"


@dataclass
class TaglineSuggestion:
    id: int
    topic_bed: str = ""
    tag_lines: List[str] = field(default_factory=list)
    white_bed: str = ""
    source_excerpt: str = ""
    selected: bool = True
    warnings: List[str] = field(default_factory=list)

    def validate(self, limits: Dict[str, int]):
        self.warnings.clear()
        t_words = len(self.topic_bed.split()) if self.topic_bed else 0
        if t_words > limits.get("topic_bed", 12):
            self.warnings.append(f"Topic Bed: {t_words} words (max {limits['topic_bed']})")
        for i, ln in enumerate(self.tag_lines, 1):
            w = len(ln.split()) if ln else 0
            if w > limits.get("tag_line", 9):
                self.warnings.append(f"TAG {i}: {w} words (max {limits['tag_line']})")
        w_words = len(self.white_bed.split()) if self.white_bed else 0
        if w_words > limits.get("white_bed", 15):
            self.warnings.append(f"White Bed: {w_words} words (max {limits['white_bed']})")


@dataclass
class Session:
    # Source metadata
    reporter_name: str = ""
    location: str = ""
    bulletin_slot: str = "6:55 PM"
    priority: str = "Headline"
    source_path: str = ""
    source_type: str = "Audio Recording"

    # Processing state
    transcript: List[TranscriptLine] = field(default_factory=list)
    suggestions: List[TaglineSuggestion] = field(default_factory=list)

    # Approval
    editor_name: str = ""
    editor_role: str = ""
    approval_status: str = "Pending"   # "Pending" | "Approved" | "Changes Requested" | "Rejected"
    editor_notes: str = ""
    approval_checklist: Dict[str, bool] = field(default_factory=lambda: {
        "facts_verified": False,
        "no_defamatory_content": False,
        "broadcasting_standards": False,
        "sinhala_grammar_reviewed": False,
        "source_confidentiality": False,
    })
    approved_at: Optional[str] = None

    # Handoff
    session_name: str = ""
    handoff_path: str = ""
    exported_path: Optional[str] = None

    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

    @property
    def date_str(self) -> str:
        return datetime.datetime.fromisoformat(self.created_at).strftime("%Y%m%d")

    @property
    def is_approved(self) -> bool:
        return self.approval_status == "Approved"

    @property
    def checklist_complete(self) -> bool:
        return all(self.approval_checklist.values())

    def full_transcript(self) -> str:
        return "\n".join(
            f"{ln.speaker} {ln.timestamp_str}: {ln.text}"
            for ln in self.transcript
        )
