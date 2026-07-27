"""
Screen 1 — Upload: drag-and-drop source material + bulletin metadata.
"""
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QFileDialog, QGroupBox, QFormLayout,
    QFrame, QListWidget, QListWidgetItem, QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal


class DropZone(QLabel):
    file_dropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("dropZone")
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(140)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setAcceptDrops(True)
        self.setText(
            "Drag & drop audio, video, or press release file here\n\n"
            "Supported: .mp3  .wav  .m4a  .mp4  .mov  .txt  .pdf  .docx"
        )

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            self.setStyleSheet("border-color: #1a6b1a; color: #1a6b1a;")
            event.acceptProposedAction()

    def dragLeaveEvent(self, _):
        self.setStyleSheet("")

    def dropEvent(self, event):
        self.setStyleSheet("")
        urls = event.mimeData().urls()
        if urls:
            self.file_dropped.emit(urls[0].toLocalFile())


class UploadScreen(QWidget):
    start_requested = pyqtSignal()   # user clicked Start AI Processing

    def __init__(self, session):
        super().__init__()
        self.session = session
        self._files: list = []

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 22, 28, 22)
        root.setSpacing(18)

        # Title
        title = QLabel("Upload Source Material")
        title.setObjectName("sectionTitle")
        root.addWidget(title)

        # Drop zone
        self.drop_zone = DropZone()
        self.drop_zone.file_dropped.connect(self._add_file)
        root.addWidget(self.drop_zone)

        # Browse row
        browse_row = QHBoxLayout()
        browse_row.addStretch()
        browse_btn = QPushButton("Browse File...")
        browse_btn.setObjectName("secondaryBtn")
        browse_btn.setFixedWidth(150)
        browse_btn.clicked.connect(self._browse)
        browse_row.addWidget(browse_btn)
        root.addLayout(browse_row)

        # File list
        self.file_list = QListWidget()
        self.file_list.setFixedHeight(90)
        self.file_list.setStyleSheet(
            "QListWidget { border: 1px solid #dddddd; border-radius: 2px; "
            "background: white; font-size: 12px; }"
            "QListWidget::item { padding: 4px 8px; }"
        )
        root.addWidget(self.file_list)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #dddddd;")
        root.addWidget(sep)

        # Metadata form
        meta_group = QGroupBox("Bulletin Metadata")
        form = QFormLayout(meta_group)
        form.setContentsMargins(14, 14, 14, 14)
        form.setSpacing(12)

        self.reporter_edit = QLineEdit()
        self.reporter_edit.setPlaceholderText("Reporter / source name...")
        form.addRow("Reporter:", self.reporter_edit)

        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("Location / dateline...")
        form.addRow("Location:", self.location_edit)

        self.slot_combo = QComboBox()
        self.slot_combo.addItems(["11:55 AM", "6:55 PM", "9:55 PM"])
        self.slot_combo.setCurrentIndex(1)
        form.addRow("Bulletin Slot:", self.slot_combo)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Breaking", "Headline", "Minor"])
        self.priority_combo.setCurrentIndex(1)
        form.addRow("Priority:", self.priority_combo)

        root.addWidget(meta_group)
        root.addStretch()

        # Start button
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.start_btn = QPushButton("Start AI Processing  →")
        self.start_btn.setObjectName("primaryBtn")
        self.start_btn.setFixedWidth(230)
        self.start_btn.clicked.connect(self._on_start)
        btn_row.addWidget(self.start_btn)
        root.addLayout(btn_row)

    def _browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Source File", "",
            "Media & Documents (*.mp3 *.wav *.m4a *.mp4 *.mov *.txt *.pdf *.docx);;All Files (*)"
        )
        if path:
            self._add_file(path)

    def _add_file(self, path: str):
        if path in self._files:
            return
        self._files.append(path)
        name = os.path.basename(path)
        size = os.path.getsize(path) / 1024 if os.path.exists(path) else 0
        item = QListWidgetItem(f"  {name}  ({size:.1f} KB)")
        self.file_list.addItem(item)
        self.session.source_path = path
        ext = os.path.splitext(path)[1].lower()
        if ext in (".txt", ".pdf", ".docx"):
            self.session.source_type = "Press Release"
        elif ext in (".mp4", ".mov"):
            self.session.source_type = "Video"
        else:
            self.session.source_type = "Audio Recording"

    def _on_start(self):
        self.session.reporter_name = self.reporter_edit.text().strip()
        self.session.location = self.location_edit.text().strip()
        self.session.bulletin_slot = self.slot_combo.currentText()
        self.session.priority = self.priority_combo.currentText()
        self.start_requested.emit()
