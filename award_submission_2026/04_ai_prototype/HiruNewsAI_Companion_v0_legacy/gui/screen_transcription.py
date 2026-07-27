"""
Screen 2 — Transcription + Speaker Diarization view.
Shows processing progress, then a colour-coded editable transcript.
"""
from typing import List
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QScrollArea, QFrame, QStackedWidget,
    QTextEdit, QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from core.session_model import TranscriptLine

_COLOURS = [
    ("#a70003", "#fff0f0"),
    ("#1a4d8f", "#f0f4ff"),
    ("#1a6b1a", "#f0fff0"),
    ("#7a3b00", "#fff8f0"),
    ("#5a1a7a", "#f8f0ff"),
]


class ProcessingView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(18)
        layout.setContentsMargins(60, 60, 60, 60)

        icon = QLabel("⚙")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size: 52px; color: #a70003;")
        layout.addWidget(icon)

        self.status_lbl = QLabel("Initialising...")
        self.status_lbl.setAlignment(Qt.AlignCenter)
        self.status_lbl.setStyleSheet("font-size: 14px; color: #555555;")
        layout.addWidget(self.status_lbl)

        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setFixedWidth(500)
        layout.addWidget(self.bar, alignment=Qt.AlignCenter)

        note = QLabel(
            "Transcribing and diarizing your source material.\n"
            "Diarization is a GPT-based prototype heuristic — labelled in transcript."
        )
        note.setAlignment(Qt.AlignCenter)
        note.setStyleSheet("font-size: 11px; color: #888888;")
        note.setWordWrap(True)
        layout.addWidget(note)

    def update(self, pct: int, msg: str):
        self.bar.setValue(pct)
        self.status_lbl.setText(msg)


class EditableSegment(QFrame):
    """One speaker segment — label + editable text area."""

    def __init__(self, line: TranscriptLine, fg: str, bg: str):
        super().__init__()
        self.line = line
        self.setStyleSheet(
            f"QFrame {{ background: {bg}; border-left: 3px solid {fg}; "
            "border-radius: 0 4px 4px 0; margin: 2px 0; padding: 4px 0; }}"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(4)

        header = QHBoxLayout()
        spk = QLabel(f"<b style='color:{fg};'>{line.speaker}</b>")
        spk.setTextFormat(Qt.RichText)
        ts = QLabel(line.timestamp_str)
        ts.setStyleSheet("color: #888888; font-size: 11px;")
        header.addWidget(spk)
        header.addWidget(ts)
        header.addStretch()
        layout.addLayout(header)

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(line.text)
        self.text_edit.setFixedHeight(60)
        self.text_edit.setStyleSheet(
            "QTextEdit { border: 1px solid #e0e0e0; border-radius: 2px; "
            "background: white; font-family: 'Iskoola Pota', 'Noto Sans Sinhala', 'Segoe UI'; "
            "font-size: 13px; padding: 4px; }"
            "QTextEdit:focus { border: 1px solid #a70003; }"
        )
        self.text_edit.textChanged.connect(self._sync)
        layout.addWidget(self.text_edit)

    def _sync(self):
        self.line.text = self.text_edit.toPlainText()


class TranscriptView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Meta bar
        self.meta_lbl = QLabel()
        self.meta_lbl.setStyleSheet("font-size: 12px; color: #555555;")
        layout.addWidget(self.meta_lbl)

        # Diarization notice
        notice = QLabel(
            "  ⚠  Speaker identification is a GPT-based prototype heuristic. "
            "Click any segment to edit transcription errors."
        )
        notice.setObjectName("aiBanner")
        notice.setWordWrap(True)
        layout.addWidget(notice)

        # Scrollable segments
        self._segments_widget = QWidget()
        self._segments_layout = QVBoxLayout(self._segments_widget)
        self._segments_layout.setSpacing(6)
        self._segments_layout.setContentsMargins(2, 4, 8, 4)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self._segments_widget)
        scroll.setFrameShape(QFrame.NoFrame)
        layout.addWidget(scroll, stretch=1)

    def load(self, lines: List[TranscriptLine]):
        # Clear old
        for i in reversed(range(self._segments_layout.count())):
            w = self._segments_layout.itemAt(i).widget()
            if w:
                w.deleteLater()

        speaker_map: dict = {}
        colour_idx = 0
        for ln in lines:
            if ln.speaker not in speaker_map:
                speaker_map[ln.speaker] = _COLOURS[colour_idx % len(_COLOURS)]
                colour_idx += 1
            fg, bg = speaker_map[ln.speaker]
            seg = EditableSegment(ln, fg, bg)
            self._segments_layout.addWidget(seg)

        self._segments_layout.addStretch()

        speakers = len(speaker_map)
        dur = max((ln.end for ln in lines), default=0)
        self.meta_lbl.setText(
            f"{len(lines)} segments  ·  {speakers} speaker(s)  ·  {dur:.0f}s"
        )


class TranscriptionScreen(QWidget):
    back_requested = pyqtSignal()
    continue_requested = pyqtSignal()

    def __init__(self, session):
        super().__init__()
        self.session = session

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 22, 28, 22)
        root.setSpacing(16)

        title = QLabel("Transcription & Speaker Diarization")
        title.setObjectName("sectionTitle")
        root.addWidget(title)

        self._sub = QStackedWidget()
        self._proc = ProcessingView()
        self._transcript = TranscriptView()
        self._sub.addWidget(self._proc)       # index 0
        self._sub.addWidget(self._transcript) # index 1
        root.addWidget(self._sub, stretch=1)

        nav = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.back_btn.setObjectName("secondaryBtn")
        self.back_btn.setFixedWidth(140)
        self.back_btn.clicked.connect(self.back_requested.emit)
        nav.addWidget(self.back_btn)
        nav.addStretch()

        self.next_btn = QPushButton("Review Taglines  →")
        self.next_btn.setObjectName("primaryBtn")
        self.next_btn.setFixedWidth(200)
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.continue_requested.emit)
        nav.addWidget(self.next_btn)
        root.addLayout(nav)

    def set_progress(self, pct: int, msg: str):
        self._sub.setCurrentIndex(0)
        self._proc.update(pct, msg)

    def show_transcript(self, lines: List[TranscriptLine]):
        self.session.transcript = lines
        self._transcript.load(lines)
        self._sub.setCurrentIndex(1)
        self.next_btn.setEnabled(True)
