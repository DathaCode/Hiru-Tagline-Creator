"""
Screen 4 — Editor Approval: mandatory editorial checklist before export.
"""
import datetime
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QCheckBox, QTextEdit, QFrame, QMessageBox,
    QFileDialog, QGroupBox,
)
from PyQt5.QtCore import Qt, pyqtSignal

from core.models import Session
from core.handoff import export_handoff

_CHECKLIST_ITEMS = [
    ("factual",   "Factual accuracy verified against source material"),
    ("grammar",   "Grammar, language, and Sinhala text correct"),
    ("legal",     "Legal and compliance review complete"),
    ("sources",   "Confidential sources — no identifying details in taglines"),
    ("editorial", "Editorial standards and Hiru News style guide met"),
]


class ApprovalScreen(QWidget):
    """
    Screen 4: editor signs off with name + checklist, then exports
    ai_handoff.json to the sessions folder for HiruTaglineCreator.
    """
    back_requested = pyqtSignal()
    export_complete = pyqtSignal(str)  # emits the export file path

    def __init__(self, session: Session, settings):
        super().__init__()
        self.session = session
        self.settings = settings
        self._checkboxes: dict = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        # Section title
        title = QLabel("Step 4 — Editor Approval")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        # Reminder banner
        reminder = QLabel(
            "  ⚠   No content may be exported for broadcast without completing all items below.   ⚠  "
        )
        reminder.setObjectName("aiBanner")
        reminder.setAlignment(Qt.AlignCenter)
        layout.addWidget(reminder)

        # Summary of taglines
        self._summary_lbl = QLabel()
        self._summary_lbl.setStyleSheet("font-size: 12px; color: #555555;")
        layout.addWidget(self._summary_lbl)

        # Editor details group
        editor_group = QGroupBox("Editor Details")
        editor_group.setStyleSheet(
            "QGroupBox { font-weight: bold; color: #1a0000; border: 1px solid #dddddd; "
            "border-radius: 6px; margin-top: 8px; padding-top: 12px; }"
            "QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; }"
        )
        eg_layout = QVBoxLayout(editor_group)
        eg_layout.setContentsMargins(16, 14, 16, 14)
        eg_layout.setSpacing(8)

        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("Senior Editor Name:"))
        self.editor_name = QLineEdit()
        self.editor_name.setPlaceholderText("Full name and title...")
        self.editor_name.textChanged.connect(self._check_ready)
        name_row.addWidget(self.editor_name)
        eg_layout.addLayout(name_row)

        layout.addWidget(editor_group)

        # Approval checklist group
        checklist_group = QGroupBox("Editorial Checklist — all items must be confirmed")
        checklist_group.setStyleSheet(
            "QGroupBox { font-weight: bold; color: #1a0000; border: 1px solid #dddddd; "
            "border-radius: 6px; margin-top: 8px; padding-top: 12px; }"
            "QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; }"
        )
        cl_layout = QVBoxLayout(checklist_group)
        cl_layout.setContentsMargins(16, 14, 16, 14)
        cl_layout.setSpacing(10)

        for key, text in _CHECKLIST_ITEMS:
            cb = QCheckBox(text)
            cb.setStyleSheet("font-size: 13px;")
            cb.stateChanged.connect(self._check_ready)
            self._checkboxes[key] = cb
            cl_layout.addWidget(cb)

        layout.addWidget(checklist_group)

        # Notes
        notes_lbl = QLabel("Notes / Comments (optional):")
        notes_lbl.setStyleSheet("font-weight: bold;")
        layout.addWidget(notes_lbl)
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText(
            "Any editorial notes, corrections made, or flagged items..."
        )
        self.notes_edit.setFixedHeight(80)
        layout.addWidget(self.notes_edit)

        layout.addStretch()

        # Export status
        self._status_lbl = QLabel()
        self._status_lbl.setStyleSheet("font-size: 12px; color: #1a6b1a; font-weight: bold;")
        self._status_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._status_lbl)

        # Nav buttons
        nav = QHBoxLayout()
        self.back_btn = QPushButton("← Back to Taglines")
        self.back_btn.setObjectName("secondaryBtn")
        self.back_btn.setFixedWidth(180)
        self.back_btn.clicked.connect(self.back_requested.emit)
        nav.addWidget(self.back_btn)
        nav.addStretch()

        self.export_btn = QPushButton("Approve & Export to HiruTaglineCreator")
        self.export_btn.setObjectName("approveBtn")
        self.export_btn.setFixedWidth(310)
        self.export_btn.setEnabled(False)
        self.export_btn.clicked.connect(self._on_approve)
        nav.addWidget(self.export_btn)
        layout.addLayout(nav)

    def refresh_summary(self):
        sets = self.session.tagline_sets
        self._summary_lbl.setText(
            f"Bulletin: {self.session.bulletin_slot}  ·  "
            f"Priority: {self.session.priority}  ·  "
            f"{len(sets)} tagline set{'s' if len(sets) != 1 else ''} to export"
        )

    def _check_ready(self):
        all_checked = all(cb.isChecked() for cb in self._checkboxes.values())
        has_name = bool(self.editor_name.text().strip())
        self.export_btn.setEnabled(all_checked and has_name)

    def _on_approve(self):
        name = self.editor_name.text().strip()
        now = datetime.datetime.now().isoformat()

        self.session.approved = True
        self.session.approved_by = name
        self.session.approved_at = now
        self.session.approval_notes = self.notes_edit.toPlainText().strip()

        # Export
        output_dir = self.settings.handoff_output_path
        try:
            out_path = export_handoff(self.session, output_dir)
        except Exception as exc:
            QMessageBox.critical(self, "Export Failed", str(exc))
            return

        self._status_lbl.setText(
            f"Exported successfully:  {out_path}"
        )
        self.export_btn.setEnabled(False)
        self.back_btn.setEnabled(False)

        msg = QMessageBox(self)
        msg.setWindowTitle("Export Complete")
        msg.setIcon(QMessageBox.Information)
        msg.setText(
            f"<b>Approved by {name}</b><br><br>"
            f"ai_handoff.json has been exported to:<br>"
            f"<code>{out_path}</code><br><br>"
            f"Open HiruTaglineCreator v2.1 and load this session to continue."
        )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

        self.export_complete.emit(str(out_path))
