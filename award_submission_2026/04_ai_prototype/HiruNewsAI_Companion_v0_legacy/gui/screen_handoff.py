"""
Screen 5 — Handoff: export approved session to ai_handoff.json.
"""
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QFrame, QFileDialog, QMessageBox,
)
from PyQt5.QtCore import Qt, pyqtSignal
from core.session_model import Session
from core.handoff_writer import write_handoff
from core.approval_state import status_colour


class HandoffScreen(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, session: Session):
        super().__init__()
        self.session = session

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 22, 28, 22)
        root.setSpacing(18)

        title = QLabel("Handoff to HiruTaglineCreator")
        title.setObjectName("sectionTitle")
        root.addWidget(title)

        # Approval status card
        self._status_card = QFrame()
        self._status_card.setFrameShape(QFrame.StyledPanel)
        self._status_card.setStyleSheet(
            "QFrame { background: white; border: 1px solid #dddddd; "
            "border-radius: 4px; padding: 4px; }"
        )
        sc_layout = QVBoxLayout(self._status_card)
        sc_layout.setContentsMargins(14, 12, 14, 12)
        self._status_lbl = QLabel()
        self._status_lbl.setStyleSheet("font-size: 14px; font-weight: bold;")
        sc_layout.addWidget(self._status_lbl)
        self._summary_lbl = QLabel()
        self._summary_lbl.setStyleSheet("font-size: 12px; color: #555555;")
        self._summary_lbl.setWordWrap(True)
        sc_layout.addWidget(self._summary_lbl)
        root.addWidget(self._status_card)

        # Content preview
        preview_lbl = QLabel("<b>Approved Content Preview:</b>")
        root.addWidget(preview_lbl)
        self._preview = QTextEdit()
        self._preview.setReadOnly(True)
        self._preview.setFixedHeight(130)
        self._preview.setStyleSheet(
            "QTextEdit { font-family: 'Iskoola Pota','Noto Sans Sinhala','Segoe UI'; "
            "font-size: 13px; background: #fafafa; border: 1px solid #dddddd; }"
        )
        root.addWidget(self._preview)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #dddddd;")
        root.addWidget(sep)

        # Session name
        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("Session Name:"))
        self.session_name_edit = QLineEdit()
        self.session_name_edit.setPlaceholderText("e.g.  AKUREGODA")
        name_row.addWidget(self.session_name_edit)
        root.addLayout(name_row)

        # Output folder
        folder_row = QHBoxLayout()
        folder_row.addWidget(QLabel("Output Folder:"))
        self.folder_edit = QLineEdit("C:/HiruTaglines/")
        folder_row.addWidget(self.folder_edit)
        browse_btn = QPushButton("Browse...")
        browse_btn.setObjectName("secondaryBtn")
        browse_btn.setFixedWidth(90)
        browse_btn.clicked.connect(self._browse_folder)
        folder_row.addWidget(browse_btn)
        root.addLayout(folder_row)

        # Output path display
        self._out_path_lbl = QLabel()
        self._out_path_lbl.setStyleSheet("font-size: 11px; color: #555555;")
        root.addWidget(self._out_path_lbl)

        root.addStretch()

        # Result label
        self._result_lbl = QLabel()
        self._result_lbl.setAlignment(Qt.AlignCenter)
        self._result_lbl.setStyleSheet("font-size: 12px; color: #1a6b1a; font-weight: bold;")
        self._result_lbl.setWordWrap(True)
        root.addWidget(self._result_lbl)

        # Action buttons
        nav = QHBoxLayout()
        self.back_btn = QPushButton("← Back to Approval")
        self.back_btn.setObjectName("secondaryBtn")
        self.back_btn.setFixedWidth(180)
        self.back_btn.clicked.connect(self.back_requested.emit)
        nav.addWidget(self.back_btn)
        nav.addStretch()

        launch_btn = QPushButton("Launch HiruTaglineCreator")
        launch_btn.setObjectName("secondaryBtn")
        launch_btn.setFixedWidth(220)
        launch_btn.setEnabled(False)
        launch_btn.setToolTip("Launch HiruTaglineCreator v2.1 (integration available in Phase 3)")
        nav.addWidget(launch_btn)
        nav.addSpacing(8)

        self.export_btn = QPushButton("Export to HiruTaglineCreator  →")
        self.export_btn.setObjectName("primaryBtn")
        self.export_btn.setFixedWidth(260)
        self.export_btn.clicked.connect(self._on_export)
        nav.addWidget(self.export_btn)
        root.addLayout(nav)

    def refresh(self):
        colour = status_colour(self.session.approval_status)
        self._status_lbl.setText(
            f"Status: <span style='color:{colour};'>{self.session.approval_status}</span>"
        )
        self._status_lbl.setTextFormat(Qt.RichText)

        sugs = [s for s in self.session.suggestions if s.selected]
        self._summary_lbl.setText(
            f"Approved by: {self.session.editor_name}  ·  "
            f"Bulletin: {self.session.bulletin_slot}  ·  "
            f"Priority: {self.session.priority}  ·  "
            f"{len(sugs)} tagline set(s)"
        )

        lines = []
        for s in sugs:
            lines.append(f"▸ {s.topic_bed}")
            for t in s.tag_lines:
                lines.append(f"  {t}")
            lines.append(f"  {s.white_bed}")
            lines.append("")
        self._preview.setPlainText("\n".join(lines).strip())

        # Auto-fill session name from bulletin slot
        slot = self.session.bulletin_slot.replace(":", "").replace(" ", "")
        if not self.session_name_edit.text():
            self.session_name_edit.setText(f"SESSION_{slot}")

        self._update_output_path()
        self.export_btn.setEnabled(self.session.approval_status == "Approved")

    def _update_output_path(self):
        name = self.session_name_edit.text().strip() or "SESSION"
        folder = self.folder_edit.text().strip() or "C:/HiruTaglines/"
        date = self.session.date_str
        self._out_path_lbl.setText(
            f"Will export to:  {folder.rstrip('/')}/{name}_{date}/ai_handoff.json"
        )

    def _browse_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            self.folder_edit.setText(path.replace("/", "\\") + "\\")
            self._update_output_path()

    def _on_export(self):
        self.session.session_name = self.session_name_edit.text().strip() or "SESSION"
        self.session.handoff_path = self.folder_edit.text().strip() or "C:/HiruTaglines/"

        try:
            out = write_handoff(self.session, self.session.handoff_path)
        except Exception as exc:
            QMessageBox.critical(self, "Export Failed", str(exc))
            return

        self.session.exported_path = str(out)
        self._result_lbl.setText(f"Exported successfully:\n{out}")
        self.export_btn.setEnabled(False)
        self.back_btn.setEnabled(False)

        QMessageBox.information(
            self,
            "Export Complete",
            f"<b>ai_handoff.json</b> written to:<br>"
            f"<code>{out}</code><br><br>"
            f"Open HiruTaglineCreator v2.1 and load this session to continue.",
        )
