"""
Screen 2 — Transcription: shows processing progress, then the
speaker-diarized transcript.
"""
from typing import List
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QProgressBar, QTextEdit, QFrame, QStackedWidget,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QTextCharFormat, QFont

from core.models import TranscriptSegment

# Speaker colour map — cycles for any number of speakers
_SPEAKER_COLOURS = [
    ("#a70003", "#fff0f0"),  # red on light red
    ("#1a4d8f", "#f0f4ff"),  # navy on light blue
    ("#1a6b1a", "#f0fff0"),  # green on light green
    ("#7a3b00", "#fff8f0"),  # brown on cream
]


class ProcessingPanel(QWidget):
    """Shown while the AI worker is running."""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(60, 40, 60, 40)

        icon = QLabel("⚙")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size: 48px; color: #a70003;")
        layout.addWidget(icon)

        self.status_lbl = QLabel("Initialising...")
        self.status_lbl.setAlignment(Qt.AlignCenter)
        self.status_lbl.setStyleSheet("font-size: 14px; color: #555555;")
        layout.addWidget(self.status_lbl)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(480)
        layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        note = QLabel(
            "Processing your source material with AI.\n"
            "This may take up to 60 seconds for longer audio files."
        )
        note.setAlignment(Qt.AlignCenter)
        note.setStyleSheet("font-size: 12px; color: #888888;")
        note.setWordWrap(True)
        layout.addWidget(note)

    def update(self, percent: int, message: str):
        self.progress_bar.setValue(percent)
        self.status_lbl.setText(message)


class TranscriptionScreen(QWidget):
    """
    Screen 2: shows processing progress while the worker runs,
    then reveals the speaker-diarized transcript when complete.
    """
    back_requested = pyqtSignal()
    continue_requested = pyqtSignal()

    def __init__(self, session):
        super().__init__()
        self.session = session

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        # Section title
        title = QLabel("Step 2 — Transcription")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        # Sub-stack: processing panel vs transcript panel
        self._sub_stack = QStackedWidget()
        self.processing_panel = ProcessingPanel()
        self._sub_stack.addWidget(self.processing_panel)   # index 0

        self._transcript_panel = self._build_transcript_panel()
        self._sub_stack.addWidget(self._transcript_panel)  # index 1
        self._sub_stack.setCurrentIndex(0)
        layout.addWidget(self._sub_stack, stretch=1)

        # Nav buttons
        nav = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.back_btn.setObjectName("secondaryBtn")
        self.back_btn.setFixedWidth(140)
        self.back_btn.clicked.connect(self.back_requested.emit)
        nav.addWidget(self.back_btn)
        nav.addStretch()

        self.continue_btn = QPushButton("Review Taglines  →")
        self.continue_btn.setObjectName("primaryBtn")
        self.continue_btn.setFixedWidth(200)
        self.continue_btn.setEnabled(False)
        self.continue_btn.clicked.connect(self.continue_requested.emit)
        nav.addWidget(self.continue_btn)
        layout.addLayout(nav)

    def _build_transcript_panel(self) -> QWidget:
        panel = QWidget()
        vbox = QVBoxLayout(panel)
        vbox.setSpacing(10)
        vbox.setContentsMargins(0, 0, 0, 0)

        meta_row = QHBoxLayout()
        self._meta_lbl = QLabel()
        self._meta_lbl.setStyleSheet("font-size: 12px; color: #555555;")
        meta_row.addWidget(self._meta_lbl)
        meta_row.addStretch()
        vbox.addLayout(meta_row)

        self._transcript_view = QTextEdit()
        self._transcript_view.setObjectName("transcriptArea")
        self._transcript_view.setReadOnly(True)
        vbox.addWidget(self._transcript_view, stretch=1)

        return panel

    # --- Public API --------------------------------------------------------

    def set_progress(self, percent: int, message: str):
        self._sub_stack.setCurrentIndex(0)
        self.processing_panel.update(percent, message)

    def show_transcript(self, segments: List[TranscriptSegment]):
        self.session.transcript = segments

        # Build coloured HTML transcript
        speaker_map: dict = {}
        colour_idx = 0
        html_parts = []

        for seg in segments:
            if seg.speaker not in speaker_map:
                fg, bg = _SPEAKER_COLOURS[colour_idx % len(_SPEAKER_COLOURS)]
                speaker_map[seg.speaker] = (fg, bg)
                colour_idx += 1

            fg, bg = speaker_map[seg.speaker]
            html_parts.append(
                f'<p style="margin:6px 0; background:{bg}; padding:6px 10px; '
                f'border-radius:4px; border-left:3px solid {fg};">'
                f'<span style="color:{fg}; font-weight:bold;">{seg.speaker}</span> '
                f'<span style="color:#888888; font-size:11px;">{seg.timestamp}</span><br>'
                f'<span style="font-family: Iskoola Pota, Noto Sans Sinhala, Segoe UI; '
                f'font-size:13px;">{seg.text}</span>'
                f"</p>"
            )

        self._transcript_view.setHtml("".join(html_parts))

        speakers = set(seg.speaker for seg in segments)
        total_dur = max((seg.end_time for seg in segments), default=0)
        self._meta_lbl.setText(
            f"{len(segments)} segments  ·  {len(speakers)} speaker(s)  ·  "
            f"{total_dur:.0f}s duration"
        )

        self._sub_stack.setCurrentIndex(1)
        self.continue_btn.setEnabled(True)
