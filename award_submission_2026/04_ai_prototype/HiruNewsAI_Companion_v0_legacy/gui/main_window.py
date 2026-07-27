"""
Main window — sidebar + header + stacked screen area + status bar.
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QStackedWidget, QAction, QMessageBox,
)
from PyQt5.QtCore import pyqtSignal
from gui.sidebar import Sidebar
from gui.theme import APP_QSS, RED, GOLD, DARK
from services.openai_client import DEMO_MODE


class MainWindow(QMainWindow):
    # Emitted by AppController after construction to keep controller alive
    screen_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "HiruNews AI Streamline \u2014 Processing Module (Phase 2 Prototype)"
        )
        self.setMinimumSize(1060, 720)
        self.resize(1180, 800)
        self.setStyleSheet(APP_QSS)

        # ── Menu bar ──────────────────────────────────────────
        menu = self.menuBar()
        help_menu = menu.addMenu("Help")
        about_act = QAction("About HiruNews AI Streamline", self)
        about_act.triggered.connect(self._show_about)
        help_menu.addAction(about_act)

        # ── Central widget ────────────────────────────────────
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        # Header bar
        root.addWidget(self._build_header())

        # Body: sidebar + content
        body = QHBoxLayout()
        body.setSpacing(0)
        body.setContentsMargins(0, 0, 0, 0)

        self.sidebar = Sidebar()
        self.sidebar.nav_changed.connect(self._on_nav)
        body.addWidget(self.sidebar)

        # Content stack
        self.stack = QStackedWidget()
        self.stack.setObjectName("contentArea")
        body.addWidget(self.stack, stretch=1)

        root.addLayout(body, stretch=1)

        # ── Status bar ────────────────────────────────────────
        self._build_status_bar()

        # Track screen keys for stacked navigation
        self._screen_keys: list = []
        self._screen_title_lbl: QLabel = None  # assigned in _build_header

    def _build_header(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("headerBar")
        bar.setFixedHeight(58)
        h = QHBoxLayout(bar)
        h.setContentsMargins(18, 0, 18, 0)
        h.setSpacing(10)

        # Red accent strip
        strip = QWidget()
        strip.setFixedSize(4, 36)
        strip.setStyleSheet(f"background-color: {RED};")
        h.addWidget(strip)

        # Titles column
        col = QVBoxLayout()
        col.setSpacing(2)
        app_title = QLabel("HiruNews AI Streamline")
        app_title.setObjectName("appTitle")
        col.addWidget(app_title)

        self._screen_title_lbl = QLabel("Processing Module \u2014 Phase 2 Prototype")
        self._screen_title_lbl.setObjectName("screenTitle")
        col.addWidget(self._screen_title_lbl)
        h.addLayout(col)

        h.addStretch()

        # Demo mode badge
        if DEMO_MODE:
            demo = QLabel("DEMO MODE")
            demo.setStyleSheet(
                f"color:{DARK}; background:{GOLD}; font-size:10px; "
                "font-weight:bold; padding:3px 8px; border-radius:3px;"
            )
            h.addWidget(demo)

        proto = QLabel("PROTOTYPE \u2014 Phase 2")
        proto.setObjectName("protoBadge")
        h.addWidget(proto)

        return bar

    def _build_status_bar(self):
        sb = self.statusBar()
        mode = "DEMO MODE" if DEMO_MODE else "LIVE API"
        sb.showMessage(
            f"HiruNews AI Streamline  |  PROTOTYPE BUILD  |  Phase 2  |  {mode}  "
            "|  Lotus Technologies (Pvt) Ltd"
        )

    def set_screen_title(self, title: str):
        if self._screen_title_lbl:
            self._screen_title_lbl.setText(title)

    # ── Screen management ─────────────────────────────────────

    def register_screen(self, key: str, widget: QWidget):
        self.stack.addWidget(widget)
        self._screen_keys.append(key)

    def show_screen(self, key: str):
        if key in self._screen_keys:
            idx = self._screen_keys.index(key)
            self.stack.setCurrentIndex(idx)
            self.sidebar.set_active(key)
            self.screen_requested.emit(key)

    def _on_nav(self, key: str):
        self.show_screen(key)

    def _show_about(self):
        QMessageBox.about(
            self,
            "HiruNews AI Streamline",
            "<b>HiruNews AI Streamline</b><br>"
            "AI-Powered End-to-End Broadcast News Production<br><br>"
            "<b>Version:</b> 0.1 Prototype (Phase 2)<br>"
            "<b>Organization:</b> Lotus Technologies (Pvt) Ltd<br>"
            "<b>Parent:</b> Asia Broadcasting Corporation (Pvt) Ltd<br><br>"
            "<b>Founder &amp; Developer:</b> Mr. Vidath Dulanjith<br>"
            "DevOps Engineer, Lotus Technologies<br><br>"
            "<i>Submitted for SLASSCOM SNIA 2026<br>"
            "Best Tech for Good Software Innovation</i>",
        )
