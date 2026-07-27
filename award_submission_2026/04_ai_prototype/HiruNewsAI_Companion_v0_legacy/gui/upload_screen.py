"""
Screen 1 — Upload: file selection + bulletin settings.
"""
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFileDialog, QGroupBox, QFormLayout, QSizePolicy,
    QFrame,
)
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent


class DropZoneLabel(QLabel):
    """Drag-and-drop target that also accepts file-browser selection."""
    file_dropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("dropZone")
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(160)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setAcceptDrops(True)
        self._reset_text()

    def _reset_text(self):
        self.setText(
            "Drag & drop audio / video / press release file here\n\n"
            "or click Browse to select a file\n\n"
            "Supported: .mp3  .mp4  .wav  .m4a  .txt  .pdf"
        )

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            self.setProperty("dragActive", "true")
            self.style().unpolish(self)
            self.style().polish(self)
            event.acceptProposedAction()

    def dragLeaveEvent(self, _event):
        self.setProperty("dragActive", "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def dropEvent(self, event: QDropEvent):
        self.setProperty("dragActive", "false")
        self.style().unpolish(self)
        self.style().polish(self)
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            self._show_file(path)
            self.file_dropped.emit(path)

    def _show_file(self, path: str):
        name = os.path.basename(path)
        size_kb = os.path.getsize(path) / 1024 if os.path.exists(path) else 0
        self.setText(f"Selected file:\n\n{name}\n({size_kb:.1f} KB)")
        self.setStyleSheet("border-color: #1a6b1a; color: #1a6b1a;")


class UploadScreen(QWidget):
    """
    Screen 1: select source material + configure bulletin settings,
    then click Process to kick off the AI worker.
    """
    process_requested = pyqtSignal()  # emitted when user clicks Process

    def __init__(self, session, settings):
        super().__init__()
        self.session = session
        self.settings = settings

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(20)

        # Section title
        title = QLabel("Step 1 — Upload Source Material")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        if settings.demo_mode:
            demo_note = QLabel(
                "Running in demo mode — no API key configured. "
                "Realistic mock Sinhala data will be used."
            )
            demo_note.setObjectName("aiBanner")
            demo_note.setWordWrap(True)
            layout.addWidget(demo_note)

        # Drop zone
        self.drop_zone = DropZoneLabel()
        self.drop_zone.file_dropped.connect(self._on_file_selected)
        layout.addWidget(self.drop_zone)

        # Browse button
        browse_row = QHBoxLayout()
        browse_row.addStretch()
        self.browse_btn = QPushButton("Browse File...")
        self.browse_btn.setObjectName("secondaryBtn")
        self.browse_btn.setFixedWidth(160)
        self.browse_btn.clicked.connect(self._browse)
        browse_row.addWidget(self.browse_btn)
        layout.addLayout(browse_row)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        layout.addWidget(sep)

        # Bulletin settings
        settings_group = QGroupBox("Bulletin Settings")
        settings_group.setStyleSheet(
            "QGroupBox { font-weight: bold; color: #a70003; border: 1px solid #dddddd; "
            "border-radius: 6px; margin-top: 8px; padding-top: 12px; }"
            "QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; }"
        )
        form = QFormLayout(settings_group)
        form.setSpacing(12)
        form.setContentsMargins(16, 16, 16, 16)

        self.slot_combo = QComboBox()
        self.slot_combo.addItems(["11:55 AM", "6:55 PM", "9:55 PM"])
        self.slot_combo.setCurrentIndex(1)
        form.addRow("Bulletin Slot:", self.slot_combo)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Normal", "Breaking News", "Developing"])
        form.addRow("Priority:", self.priority_combo)

        self.source_type_combo = QComboBox()
        self.source_type_combo.addItems(
            ["Audio Recording", "Video", "Press Release", "Live Feed", "Text Input"]
        )
        form.addRow("Source Type:", self.source_type_combo)

        layout.addWidget(settings_group)

        layout.addStretch()

        # Process button
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.process_btn = QPushButton("Process with AI  →")
        self.process_btn.setObjectName("primaryBtn")
        self.process_btn.setFixedWidth(220)
        self.process_btn.clicked.connect(self._on_process)
        btn_row.addWidget(self.process_btn)
        layout.addLayout(btn_row)

    def _browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Source Material",
            "",
            "Media & Text Files (*.mp3 *.mp4 *.wav *.m4a *.txt *.pdf *.docx);;All Files (*)",
        )
        if path:
            self._on_file_selected(path)
            self.drop_zone._show_file(path)

    def _on_file_selected(self, path: str):
        self.session.source_path = path
        ext = os.path.splitext(path)[1].lower()
        if ext in (".txt", ".pdf", ".docx"):
            self.source_type_combo.setCurrentText("Press Release")
        elif ext in (".mp4", ".mov", ".avi"):
            self.source_type_combo.setCurrentText("Video")
        else:
            self.source_type_combo.setCurrentText("Audio Recording")

    def _on_process(self):
        self.session.bulletin_slot = self.slot_combo.currentText()
        self.session.priority = self.priority_combo.currentText()
        self.session.source_type = self.source_type_combo.currentText()
        self.process_requested.emit()
