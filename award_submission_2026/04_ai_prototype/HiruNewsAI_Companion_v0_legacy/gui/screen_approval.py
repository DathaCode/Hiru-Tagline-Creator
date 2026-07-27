"""
Screen 4 — Editor Approval: review panel, checklist, three-action decision.
"""
import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QCheckBox, QGroupBox, QFrame,
    QScrollArea, QMessageBox,
)
from PyQt5.QtCore import Qt, pyqtSignal
from core.session_model import Session
from core.approval_state import CHECKLIST_LABELS, status_colour


class ApprovalScreen(QWidget):
    back_requested  = pyqtSignal()
    approved        = pyqtSignal()
    changes_requested = pyqtSignal()
    rejected        = pyqtSignal()

    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self._checks: dict = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 22, 28, 22)
        root.setSpacing(16)

        title = QLabel("Editor Approval & Review")
        title.setObjectName("sectionTitle")
        root.addWidget(title)

        banner = QLabel(
            "  ⚠   No AI-generated content may be broadcast without completing all items below.   ⚠  "
        )
        banner.setObjectName("aiBanner")
        banner.setAlignment(Qt.AlignCenter)
        root.addWidget(banner)

        # Scrollable body
        body_widget = QWidget()
        body_layout = QVBoxLayout(body_widget)
        body_layout.setSpacing(16)
        body_layout.setContentsMargins(0, 0, 8, 0)

        # Content summary
        self._summary_lbl = QLabel()
        self._summary_lbl.setStyleSheet("font-size: 12px; color: #555555;")
        body_layout.addWidget(self._summary_lbl)

        # Tagline preview
        self._preview = QTextEdit()
        self._preview.setReadOnly(True)
        self._preview.setFixedHeight(120)
        self._preview.setStyleSheet(
            "QTextEdit { font-family: 'Iskoola Pota','Noto Sans Sinhala','Segoe UI'; "
            "font-size: 13px; border: 1px solid #dddddd; border-radius: 2px; background: #fafafa; }"
        )
        body_layout.addWidget(self._preview)

        # Editor details
        ed_group = QGroupBox("Editor Details")
        ed_form = QVBoxLayout(ed_group)
        ed_form.setContentsMargins(14, 14, 14, 14)
        ed_form.setSpacing(10)

        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("Full Name:"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Senior editor name...")
        self.name_edit.textChanged.connect(self._check_ready)
        name_row.addWidget(self.name_edit)
        ed_form.addLayout(name_row)

        role_row = QHBoxLayout()
        role_row.addWidget(QLabel("Role / Title:"))
        self.role_edit = QLineEdit()
        self.role_edit.setPlaceholderText("e.g. Senior News Editor")
        role_row.addWidget(self.role_edit)
        ed_form.addLayout(role_row)

        body_layout.addWidget(ed_group)

        # Approval checklist
        cl_group = QGroupBox("Approval Checklist — all items required")
        cl_layout = QVBoxLayout(cl_group)
        cl_layout.setContentsMargins(14, 14, 14, 14)
        cl_layout.setSpacing(10)

        for key, label in CHECKLIST_LABELS.items():
            cb = QCheckBox(label)
            cb.stateChanged.connect(self._check_ready)
            self._checks[key] = cb
            cl_layout.addWidget(cb)

        body_layout.addWidget(cl_group)

        # Notes
        body_layout.addWidget(QLabel("<b>Editor Notes / Comments:</b>"))
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText(
            "Corrections made, flagged items, source verification notes..."
        )
        self.notes_edit.setFixedHeight(80)
        body_layout.addWidget(self.notes_edit)

        body_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(body_widget)
        scroll.setFrameShape(QFrame.NoFrame)
        root.addWidget(scroll, stretch=1)

        # Three-action nav
        nav = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.back_btn.setObjectName("secondaryBtn")
        self.back_btn.setFixedWidth(140)
        self.back_btn.clicked.connect(self.back_requested.emit)
        nav.addWidget(self.back_btn)
        nav.addStretch()

        self.reject_btn = QPushButton("Reject")
        self.reject_btn.setObjectName("rejectBtn")
        self.reject_btn.setFixedWidth(110)
        self.reject_btn.clicked.connect(self._on_reject)
        nav.addWidget(self.reject_btn)
        nav.addSpacing(8)

        self.changes_btn = QPushButton("Request Changes")
        self.changes_btn.setObjectName("changesBtn")
        self.changes_btn.setFixedWidth(160)
        self.changes_btn.clicked.connect(self._on_changes)
        nav.addWidget(self.changes_btn)
        nav.addSpacing(8)

        self.approve_btn = QPushButton("Approve  ✓")
        self.approve_btn.setObjectName("approveBtn")
        self.approve_btn.setFixedWidth(140)
        self.approve_btn.setEnabled(False)
        self.approve_btn.clicked.connect(self._on_approve)
        nav.addWidget(self.approve_btn)
        root.addLayout(nav)

    def refresh(self):
        sugs = [s for s in self.session.suggestions if s.selected]
        self._summary_lbl.setText(
            f"Bulletin: {self.session.bulletin_slot}  ·  "
            f"Priority: {self.session.priority}  ·  "
            f"{len(sugs)} tagline set(s) selected for export"
        )
        lines = []
        for s in sugs:
            lines.append(f"▸ {s.topic_bed}")
            for t in s.tag_lines:
                lines.append(f"  {t}")
            lines.append(f"  {s.white_bed}")
            lines.append("")
        self._preview.setPlainText("\n".join(lines).strip())

    def _check_ready(self):
        all_checked = all(cb.isChecked() for cb in self._checks.values())
        has_name = bool(self.name_edit.text().strip())
        self.approve_btn.setEnabled(all_checked and has_name)

    def _commit(self, status: str):
        self.session.editor_name = self.name_edit.text().strip()
        self.session.editor_role = self.role_edit.text().strip()
        self.session.editor_notes = self.notes_edit.toPlainText().strip()
        self.session.approval_status = status
        self.session.approval_checklist = {
            k: cb.isChecked() for k, cb in self._checks.items()
        }
        self.session.approved_at = datetime.datetime.now().isoformat()

    def _on_approve(self):
        self._commit("Approved")
        self.approved.emit()

    def _on_changes(self):
        self._commit("Changes Requested")
        self.changes_requested.emit()

    def _on_reject(self):
        self._commit("Rejected")
        self.rejected.emit()
