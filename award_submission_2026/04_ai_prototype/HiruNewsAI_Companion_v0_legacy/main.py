"""
HiruNews AI Streamline — Processing Module (Phase 2 Prototype)
AI News Ingestion & Editorial Approval Companion

Lotus Technologies (Pvt) Ltd
Under Asia Broadcasting Corporation (Pvt) Ltd, Sri Lanka
Founder & Developer: Mr. Vidath Dulanjith — DevOps Engineer

SLASSCOM SNIA 2026 — Best Tech for Good Software Innovation
"""
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from gui.main_window import MainWindow
from gui.screen_upload import UploadScreen
from gui.screen_transcription import TranscriptionScreen
from gui.screen_suggestions import SuggestionsScreen
from gui.screen_approval import ApprovalScreen
from gui.screen_handoff import HandoffScreen
from gui.screen_dashboard import DashboardScreen
from core.session_model import Session
from services import transcription as svc_transcription
from services import diarization as svc_diarization
from services import tagline_generator as svc_tags


class PipelineWorker(QThread):
    """Runs transcription -> diarization -> tag generation off the main thread."""
    progress       = pyqtSignal(int, str)
    transcript_done = pyqtSignal(list)
    tags_done      = pyqtSignal(list)
    error          = pyqtSignal(str)

    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def run(self):
        try:
            # Stage 1: transcription (0-50%)
            def t_prog(pct, msg):
                self.progress.emit(int(pct * 0.5), msg)

            lines = svc_transcription.transcribe(
                self.session.source_path or "",
                progress_cb=t_prog,
            )
            self.progress.emit(50, "Identifying speakers...")

            # Stage 2: diarization (50-65%)
            lines = svc_diarization.diarize(lines, progress_cb=None)
            self.transcript_done.emit(lines)
            self.progress.emit(65, "Generating tagline suggestions...")

            # Stage 3: tagline generation (65-100%)
            def g_prog(pct, msg):
                self.progress.emit(65 + int(pct * 0.35), msg)

            tags = svc_tags.generate(
                lines,
                bulletin_slot=self.session.bulletin_slot,
                progress_cb=g_prog,
            )
            self.tags_done.emit(tags)

        except Exception as exc:
            self.error.emit(str(exc))


class AppController:
    """Wires all 6 screens and the pipeline worker together."""

    SCREEN_ORDER = [
        "upload", "transcription", "suggestions",
        "approval", "handoff", "dashboard",
    ]

    def __init__(self, window: MainWindow):
        self.window = window
        self.session = Session()
        self.worker: PipelineWorker = None

        # Build screens
        self.upload        = UploadScreen(self.session)
        self.transcription = TranscriptionScreen(self.session)
        self.suggestions   = SuggestionsScreen(self.session)
        self.approval      = ApprovalScreen(self.session)
        self.handoff       = HandoffScreen(self.session)
        self.dashboard     = DashboardScreen()

        pairs = list(zip(self.SCREEN_ORDER, [
            self.upload, self.transcription, self.suggestions,
            self.approval, self.handoff, self.dashboard,
        ]))
        for key, widget in pairs:
            window.register_screen(key, widget)

        window.show_screen("upload")

        # ── Signal wiring ────────────────────────────────────
        self.upload.start_requested.connect(self._start_pipeline)

        self.transcription.back_requested.connect(lambda: window.show_screen("upload"))
        self.transcription.continue_requested.connect(lambda: window.show_screen("suggestions"))

        self.suggestions.back_requested.connect(lambda: window.show_screen("transcription"))
        self.suggestions.continue_requested.connect(self._go_approval)

        self.approval.back_requested.connect(lambda: window.show_screen("suggestions"))
        self.approval.approved.connect(self._go_handoff)
        self.approval.changes_requested.connect(lambda: window.show_screen("suggestions"))
        self.approval.rejected.connect(self._on_rejected)

        self.handoff.back_requested.connect(lambda: window.show_screen("approval"))

        window.screen_requested.connect(self._on_screen_shown)

    def _start_pipeline(self):
        self.window.show_screen("transcription")
        self.transcription.set_progress(0, "Starting pipeline...")

        self.worker = PipelineWorker(self.session)
        self.worker.progress.connect(self.transcription.set_progress)
        self.worker.transcript_done.connect(self.transcription.show_transcript)
        self.worker.tags_done.connect(self.suggestions.load_suggestions)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    def _go_approval(self):
        self.approval.refresh()
        self.window.show_screen("approval")

    def _go_handoff(self):
        self.handoff.refresh()
        self.window.show_screen("handoff")

    def _on_rejected(self):
        QMessageBox.information(
            self.window, "Session Rejected",
            "This session has been marked as Rejected and will not be exported."
        )

    def _on_error(self, msg: str):
        body = "\n\n".join([
            "An error occurred during AI processing:",
            msg,
            "If you have no API key, ensure DEMO_MODE=true in your .env file.",
        ])
        QMessageBox.critical(self.window, "Processing Error", body)
        self.window.show_screen("upload")

    def _on_screen_shown(self, key: str):
        titles = {
            "upload":        "Step 1 — Upload Source Material",
            "transcription": "Step 2 — Transcription & Diarization",
            "suggestions":   "Step 3 — AI Tagline Suggestions",
            "approval":      "Step 4 — Editor Approval",
            "handoff":       "Step 5 — Handoff to HiruTaglineCreator",
            "dashboard":     "Dashboard",
        }
        self.window.set_screen_title(titles.get(key, ""))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("HiruNews AI Streamline")
    app.setApplicationVersion("0.1-prototype")
    app.setOrganizationName("Lotus Technologies (Pvt) Ltd")
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    window = MainWindow()
    controller = AppController(window)  # noqa: F841

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
