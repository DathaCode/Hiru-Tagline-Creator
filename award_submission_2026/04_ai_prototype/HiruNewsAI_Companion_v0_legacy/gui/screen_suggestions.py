"""
Screen 3 — AI Tagline Suggestions: editable suggestion cards with
word-count warnings and mandatory AI approval banner.
"""
from typing import List
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QCheckBox, QFrame, QScrollArea,
    QSizePolicy, QToolButton,
)
from PyQt5.QtCore import Qt, pyqtSignal
from core.session_model import TaglineSuggestion, Session

_WORD_LIMITS = {"topic_bed": 12, "tag_line": 9, "white_bed": 15}


class SuggestionCard(QFrame):
    regenerate_requested = pyqtSignal(int)   # emits suggestion id

    def __init__(self, sug: TaglineSuggestion):
        super().__init__()
        self.sug = sug
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(
            "QFrame { background: white; border: 1px solid #dddddd; "
            "border-left: 4px solid #a70003; border-radius: 0 4px 4px 0; }"
        )
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        root = QVBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(10)

        # Card header row
        hdr = QHBoxLayout()
        self.select_cb = QCheckBox(f"Suggestion {sug.id}")
        self.select_cb.setChecked(sug.selected)
        self.select_cb.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.select_cb.stateChanged.connect(self._sync_selected)
        hdr.addWidget(self.select_cb)
        hdr.addStretch()

        regen_btn = QToolButton()
        regen_btn.setText("↻ Regenerate")
        regen_btn.setStyleSheet(
            "QToolButton { color: #a70003; font-size: 11px; border: none; }"
            "QToolButton:hover { text-decoration: underline; }"
        )
        regen_btn.clicked.connect(lambda: self.regenerate_requested.emit(sug.id))
        hdr.addWidget(regen_btn)
        root.addLayout(hdr)

        # Topic Bed
        root.addWidget(self._field_lbl("Topic Bed", "Red background · max 12 words"))
        self.topic_edit = QLineEdit(sug.topic_bed)
        self.topic_edit.setStyleSheet(
            "QLineEdit { border-left: 4px solid #a70003; border-radius: 0 2px 2px 0; "
            "padding-left: 10px; font-family: 'Iskoola Pota','Noto Sans Sinhala','Segoe UI'; }"
        )
        self.topic_edit.textChanged.connect(self._sync)
        root.addWidget(self.topic_edit)

        self.topic_warn = QLabel()
        self.topic_warn.setStyleSheet("font-size: 11px; color: #888888;")
        root.addWidget(self.topic_warn)

        # TAG Lines
        root.addWidget(self._field_lbl("TAG Lines", "One per line · max 9 words each"))
        self.tag_edit = QTextEdit()
        self.tag_edit.setPlainText("\n".join(sug.tag_lines))
        self.tag_edit.setFixedHeight(76)
        self.tag_edit.setStyleSheet(
            "QTextEdit { border-left: 4px solid #555555; border-radius: 0 2px 2px 0; "
            "padding-left: 10px; font-family: 'Iskoola Pota','Noto Sans Sinhala','Segoe UI'; }"
        )
        self.tag_edit.textChanged.connect(self._sync)
        root.addWidget(self.tag_edit)

        self.tag_warn = QLabel()
        self.tag_warn.setStyleSheet("font-size: 11px; color: #888888;")
        root.addWidget(self.tag_warn)

        # White Bed
        root.addWidget(self._field_lbl("White Bed", "White background · max 15 words"))
        self.white_edit = QLineEdit(sug.white_bed)
        self.white_edit.setStyleSheet(
            "QLineEdit { border-left: 4px solid #cccccc; border-radius: 0 2px 2px 0; "
            "padding-left: 10px; font-family: 'Iskoola Pota','Noto Sans Sinhala','Segoe UI'; }"
        )
        self.white_edit.textChanged.connect(self._sync)
        root.addWidget(self.white_edit)

        # Source excerpt
        if sug.source_excerpt:
            src = QLabel(
                f"Source: {sug.source_excerpt[:110]}{'…' if len(sug.source_excerpt) > 110 else ''}"
            )
            src.setStyleSheet("font-size: 11px; color: #888888; font-style: italic;")
            src.setWordWrap(True)
            root.addWidget(src)

        self._update_warnings()

    @staticmethod
    def _field_lbl(name: str, hint: str) -> QLabel:
        lbl = QLabel(
            f"<b>{name}</b>  "
            f"<span style='color:#888;font-size:11px;'>({hint})</span>"
        )
        lbl.setTextFormat(Qt.RichText)
        return lbl

    def _sync(self):
        self.sug.topic_bed = self.topic_edit.text()
        self.sug.tag_lines = [
            ln.strip()
            for ln in self.tag_edit.toPlainText().splitlines()
            if ln.strip()
        ]
        self.sug.white_bed = self.white_edit.text()
        self.sug.validate(_WORD_LIMITS)
        self._update_warnings()

    def _sync_selected(self):
        self.sug.selected = self.select_cb.isChecked()

    def _update_warnings(self):
        tw = len(self.sug.topic_bed.split()) if self.sug.topic_bed else 0
        if tw > _WORD_LIMITS["topic_bed"]:
            self.topic_warn.setText(f"⚠  {tw} words (max {_WORD_LIMITS['topic_bed']})")
            self.topic_warn.setStyleSheet("font-size:11px; color:#cc6600;")
        else:
            self.topic_warn.setText(f"{tw} word{'s' if tw != 1 else ''}")
            self.topic_warn.setStyleSheet("font-size:11px; color:#888888;")

        tag_issues = []
        for i, ln in enumerate(self.sug.tag_lines, 1):
            w = len(ln.split()) if ln else 0
            if w > _WORD_LIMITS["tag_line"]:
                tag_issues.append(f"Line {i}: {w}w")
        if tag_issues:
            self.tag_warn.setText("⚠  " + "  |  ".join(tag_issues))
            self.tag_warn.setStyleSheet("font-size:11px; color:#cc6600;")
        else:
            n = len(self.sug.tag_lines)
            self.tag_warn.setText(f"{n} line{'s' if n != 1 else ''}")
            self.tag_warn.setStyleSheet("font-size:11px; color:#888888;")


class SuggestionsScreen(QWidget):
    back_requested = pyqtSignal()
    continue_requested = pyqtSignal()

    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self._cards: List[SuggestionCard] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 22, 28, 22)
        root.setSpacing(14)

        title = QLabel("AI Tagline Suggestions")
        title.setObjectName("sectionTitle")
        root.addWidget(title)

        banner = QLabel(
            "  ⚠   Generated by AI — Requires Senior Editor Approval Before Broadcast   ⚠  "
        )
        banner.setObjectName("aiBanner")
        banner.setAlignment(Qt.AlignCenter)
        root.addWidget(banner)

        instr = QLabel(
            "Review and edit each suggestion. Use checkboxes to select which sets to export. "
            "All text fields are editable."
        )
        instr.setStyleSheet("font-size: 12px; color: #555555;")
        instr.setWordWrap(True)
        root.addWidget(instr)

        # Scrollable cards
        self._cards_widget = QWidget()
        self._cards_layout = QVBoxLayout(self._cards_widget)
        self._cards_layout.setSpacing(12)
        self._cards_layout.setContentsMargins(0, 0, 8, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self._cards_widget)
        scroll.setFrameShape(QFrame.NoFrame)
        root.addWidget(scroll, stretch=1)

        nav = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.back_btn.setObjectName("secondaryBtn")
        self.back_btn.setFixedWidth(140)
        self.back_btn.clicked.connect(self.back_requested.emit)
        nav.addWidget(self.back_btn)
        nav.addStretch()

        count_lbl = QLabel()
        self._count_lbl = count_lbl
        count_lbl.setStyleSheet("font-size: 12px; color: #555555;")
        nav.addWidget(count_lbl)
        nav.addSpacing(16)

        self.next_btn = QPushButton("Proceed to Approval  →")
        self.next_btn.setObjectName("primaryBtn")
        self.next_btn.setFixedWidth(220)
        self.next_btn.clicked.connect(self.continue_requested.emit)
        nav.addWidget(self.next_btn)
        root.addLayout(nav)

    def load_suggestions(self, suggestions: List[TaglineSuggestion]):
        for card in self._cards:
            card.deleteLater()
        self._cards.clear()

        self.session.suggestions = suggestions
        for sug in suggestions:
            card = SuggestionCard(sug)
            self._cards_layout.addWidget(card)
            self._cards.append(card)
        self._cards_layout.addStretch()
        self._count_lbl.setText(f"{len(suggestions)} suggestion(s) generated")
