"""
Screen 3 — AI-Generated Taglines: editable tagline sets with word-count
warnings and a prominent "Requires Editor Approval" banner.
"""
from typing import List
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QFrame, QScrollArea, QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal

from core.models import TaglineSet, Session


class TaglineCard(QFrame):
    """
    One editable card for a single TaglineSet:
      - Topic Bed (single line)
      - TAG Lines (multi-line, one per line)
      - White Bed (single line)
    """

    def __init__(self, tagline_set: TaglineSet, index: int):
        super().__init__()
        self.tagline_set = tagline_set
        self.setObjectName("tagCard")
        self.setProperty("topicHighlight", "true")
        self.setFrameShape(QFrame.StyledPanel)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(14, 12, 14, 14)

        # Card header
        header = QLabel(f"Tagline Set {index}")
        header.setStyleSheet(
            "font-weight: bold; font-size: 13px; color: #a70003; "
            "padding-bottom: 6px; border-bottom: 1px solid #f0d0d0;"
        )
        layout.addWidget(header)

        # Topic Bed
        layout.addWidget(self._field_label("Topic Bed", "Red background — FM GANGANEE · max 6 words"))
        self.topic_edit = QLineEdit(tagline_set.topic_bed)
        self.topic_edit.setPlaceholderText("Sinhala title text...")
        self.topic_edit.setStyleSheet(
            "QLineEdit { border-left: 4px solid #a70003; border-radius: 0 4px 4px 0; "
            "padding-left: 10px; font-family: 'Iskoola Pota', 'Noto Sans Sinhala', 'Segoe UI'; }"
        )
        self.topic_edit.textChanged.connect(self._sync)
        layout.addWidget(self.topic_edit)
        self.topic_warn = QLabel()
        self.topic_warn.setObjectName("warnLabel")
        layout.addWidget(self.topic_warn)

        # TAG Lines
        layout.addWidget(self._field_label("TAG Lines", "White text on dark — max 10 words per line · one line per row"))
        self.tag_edit = QTextEdit()
        self.tag_edit.setPlaceholderText("One TAG line per row...")
        self.tag_edit.setPlainText("\n".join(tagline_set.tag_lines))
        self.tag_edit.setFixedHeight(80)
        self.tag_edit.setStyleSheet(
            "QTextEdit { border-left: 4px solid #555555; border-radius: 0 4px 4px 0; "
            "padding-left: 10px; font-family: 'Iskoola Pota', 'Noto Sans Sinhala', 'Segoe UI'; }"
        )
        self.tag_edit.textChanged.connect(self._sync)
        layout.addWidget(self.tag_edit)
        self.tag_warn = QLabel()
        self.tag_warn.setObjectName("warnLabel")
        layout.addWidget(self.tag_warn)

        # White Bed
        layout.addWidget(self._field_label("White Bed", "White background — bulletin slot / sign-off"))
        self.white_edit = QLineEdit(tagline_set.white_bed)
        self.white_edit.setPlaceholderText("e.g.  හිරු පුවත් — රාත්‍රී 6.55")
        self.white_edit.setStyleSheet(
            "QLineEdit { border-left: 4px solid #cccccc; border-radius: 0 4px 4px 0; "
            "padding-left: 10px; font-family: 'Iskoola Pota', 'Noto Sans Sinhala', 'Segoe UI'; }"
        )
        self.white_edit.textChanged.connect(self._sync)
        layout.addWidget(self.white_edit)

        # Source passage (read-only, collapsed)
        if tagline_set.source_text:
            src_lbl = QLabel(f"Source: {tagline_set.source_text[:120]}{'...' if len(tagline_set.source_text) > 120 else ''}")
            src_lbl.setStyleSheet("font-size: 11px; color: #888888; font-style: italic;")
            src_lbl.setWordWrap(True)
            layout.addWidget(src_lbl)

        # Initial warnings
        self._update_warnings()

    @staticmethod
    def _field_label(name: str, hint: str) -> QLabel:
        lbl = QLabel(f"<b>{name}</b>  <span style='color:#888;font-size:11px;'>({hint})</span>")
        lbl.setTextFormat(Qt.RichText)
        return lbl

    def _sync(self):
        self.tagline_set.topic_bed = self.topic_edit.text()
        self.tagline_set.tag_lines = [
            ln.strip()
            for ln in self.tag_edit.toPlainText().splitlines()
            if ln.strip()
        ]
        self.tagline_set.white_bed = self.white_edit.text()
        self.tagline_set.validate()
        self._update_warnings()

    def _update_warnings(self):
        topic_words = len(self.tagline_set.topic_bed.split()) if self.tagline_set.topic_bed else 0
        if topic_words > 6:
            self.topic_warn.setText(f"⚠  {topic_words} words (max 6 recommended)")
        else:
            self.topic_warn.setText(f"{topic_words} word{'s' if topic_words != 1 else ''}")
            self.topic_warn.setStyleSheet("font-size: 11px; color: #888888;")

        tag_warnings = []
        for i, line in enumerate(self.tagline_set.tag_lines, 1):
            w = len(line.split()) if line else 0
            if w > 10:
                tag_warnings.append(f"Line {i}: {w} words (max 10)")
        if tag_warnings:
            self.tag_warn.setText("⚠  " + "  |  ".join(tag_warnings))
            self.tag_warn.setObjectName("warnLabel")
        else:
            line_count = len(self.tagline_set.tag_lines)
            self.tag_warn.setText(f"{line_count} line{'s' if line_count != 1 else ''}")
            self.tag_warn.setStyleSheet("font-size: 11px; color: #888888;")


class SuggestionsScreen(QWidget):
    """
    Screen 3: displays editable AI-generated tagline cards with
    the mandatory AI approval warning banner.
    """
    back_requested = pyqtSignal()
    continue_requested = pyqtSignal()

    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self._cards: List[TaglineCard] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(14)

        # Section title
        title = QLabel("Step 3 — AI-Generated Taglines")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        # AI warning banner — always visible
        banner = QLabel(
            "  ⚠   Generated by AI — Requires Senior Editor Approval Before Broadcast   ⚠  "
        )
        banner.setObjectName("aiBanner")
        banner.setAlignment(Qt.AlignCenter)
        banner.setWordWrap(True)
        layout.addWidget(banner)

        # Instruction
        instr = QLabel(
            "Review and edit each tagline set below. "
            "All fields are editable — correct any errors before proceeding to approval."
        )
        instr.setStyleSheet("font-size: 12px; color: #555555;")
        instr.setWordWrap(True)
        layout.addWidget(instr)

        # Scrollable card area
        self._cards_widget = QWidget()
        self._cards_layout = QVBoxLayout(self._cards_widget)
        self._cards_layout.setSpacing(14)
        self._cards_layout.setContentsMargins(0, 0, 8, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self._cards_widget)
        scroll.setFrameShape(QFrame.NoFrame)
        layout.addWidget(scroll, stretch=1)

        # Nav buttons
        nav = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.back_btn.setObjectName("secondaryBtn")
        self.back_btn.setFixedWidth(140)
        self.back_btn.clicked.connect(self.back_requested.emit)
        nav.addWidget(self.back_btn)
        nav.addStretch()

        self.continue_btn = QPushButton("Proceed to Approval  →")
        self.continue_btn.setObjectName("primaryBtn")
        self.continue_btn.setFixedWidth(220)
        self.continue_btn.clicked.connect(self.continue_requested.emit)
        nav.addWidget(self.continue_btn)
        layout.addLayout(nav)

    def load_taglines(self, tagline_sets: List[TaglineSet]):
        # Clear existing cards
        for card in self._cards:
            card.deleteLater()
        self._cards.clear()

        self.session.tagline_sets = tagline_sets

        for i, ts in enumerate(tagline_sets, start=1):
            card = TaglineCard(ts, i)
            self._cards_layout.addWidget(card)
            self._cards.append(card)

        self._cards_layout.addStretch()
