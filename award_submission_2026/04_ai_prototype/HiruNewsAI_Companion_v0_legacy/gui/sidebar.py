"""
Left sidebar with navigation buttons for all 6 screens.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

NAV_ITEMS = [
    ("upload",        "⬆  Upload"),
    ("transcription", "✍  Transcription"),
    ("suggestions",   "✦  Tagline Suggestions"),
    ("approval",      "✓  Editor Approval"),
    ("handoff",       "➤  Handoff"),
    ("dashboard",     "▦  Dashboard"),
]


class Sidebar(QWidget):
    nav_changed = pyqtSignal(str)  # emits screen key

    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header label
        header = QLabel("AI STREAMLINE")
        header.setObjectName("sidebarHeader")
        layout.addWidget(header)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #2a0a0a;")
        layout.addWidget(sep)

        # Nav buttons
        self._buttons: dict[str, QPushButton] = {}
        for key, label in NAV_ITEMS:
            btn = QPushButton(label)
            btn.setObjectName("navBtn")
            btn.setProperty("active", "false")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, k=key: self._on_click(k))
            layout.addWidget(btn)
            self._buttons[key] = btn

        layout.addStretch()

        # Bottom info
        info = QLabel("Lotus Technologies\n(Pvt) Ltd")
        info.setStyleSheet(
            "color: #444444; font-size: 10px; padding: 8px 16px;"
        )
        info.setWordWrap(True)
        layout.addWidget(info)

    def set_active(self, key: str):
        for k, btn in self._buttons.items():
            active = "true" if k == key else "false"
            btn.setProperty("active", active)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _on_click(self, key: str):
        self.set_active(key)
        self.nav_changed.emit(key)

    def set_enabled(self, key: str, enabled: bool):
        if key in self._buttons:
            self._buttons[key].setEnabled(enabled)
