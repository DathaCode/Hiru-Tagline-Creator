"""
HiruNews AI Streamline — QWebChannel Bridge
Exposes Python methods to the React frontend via Qt's WebChannel.

Lotus Technologies (Pvt) Ltd
Developer: Mr. Vidath Dulanjith — DevOps Engineer
"""

import json
import time
import logging
import threading
from pathlib import Path
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, QThread
from PyQt6.QtWidgets import QFileDialog

from . import mock_data
from .openai_client import is_mock_mode
from .transcription import transcribe
from .tagline_generator import generate
from .handoff_writer import write_handoff
from .session_store import save_session, load_session, list_sessions

logger = logging.getLogger(__name__)


class TranscriptionWorker(QThread):
    """Background worker for transcription to avoid blocking the UI."""
    finished = pyqtSignal(str)  # Emits JSON result
    progress = pyqtSignal(str)  # Emits JSON progress update

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            def on_progress(pct, msg):
                self.progress.emit(json.dumps({"percent": pct, "message": msg}))

            if is_mock_mode():
                # Simulate processing time for demo
                steps = [
                    (10, "Preparing audio file..."),
                    (25, "Sending to Whisper API..."),
                    (45, "Processing audio segments..."),
                    (65, "Identifying speakers..."),
                    (80, "Diarizing transcript..."),
                    (95, "Finalizing transcription..."),
                ]
                for pct, msg in steps:
                    on_progress(pct, msg)
                    time.sleep(0.4)

            segments = transcribe(self.file_path, on_progress)
            result = {"status": "complete", "segments": segments}
            self.finished.emit(json.dumps(result, ensure_ascii=False))

        except Exception as e:
            result = {"status": "error", "error": str(e)}
            self.finished.emit(json.dumps(result, ensure_ascii=False))


class TaglineWorker(QThread):
    """Background worker for tagline generation."""
    finished = pyqtSignal(str)

    def __init__(self, transcript: str, bulletin_slot: str):
        super().__init__()
        self.transcript = transcript
        self.bulletin_slot = bulletin_slot

    def run(self):
        try:
            if is_mock_mode():
                time.sleep(1.5)  # Simulate processing
            
            # Parse transcript if it's JSON
            try:
                segments = json.loads(self.transcript)
            except (json.JSONDecodeError, TypeError):
                segments = [{"speaker": "Speaker 1", "timestamp": "00:00:00", "text": self.transcript}]

            suggestions = generate(segments, self.bulletin_slot)
            result = {"status": "complete", "suggestions": suggestions}
            self.finished.emit(json.dumps(result, ensure_ascii=False))

        except Exception as e:
            result = {"status": "error", "error": str(e)}
            self.finished.emit(json.dumps(result, ensure_ascii=False))


class Bridge(QObject):
    """
    QWebChannel bridge object. Exposed to JavaScript as 'bridge'.
    React calls these methods; Python executes and returns results.
    """

    # Signals for pushing updates to React
    transcriptionProgress = pyqtSignal(str)
    transcriptionComplete = pyqtSignal(str)
    taglineComplete = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._transcription_worker = None
        self._tagline_worker = None
        self._main_window = parent

    @pyqtSlot(str, result=str)
    def start_transcription(self, file_path: str) -> str:
        """Start async transcription. Returns job_id immediately."""
        job_id = f"job_{int(time.time())}"
        logger.info(f"Starting transcription job {job_id} for: {file_path}")

        self._transcription_worker = TranscriptionWorker(file_path)
        self._transcription_worker.progress.connect(
            lambda data: self.transcriptionProgress.emit(data)
        )
        self._transcription_worker.finished.connect(
            lambda data: self.transcriptionComplete.emit(data)
        )
        self._transcription_worker.start()

        return json.dumps({"job_id": job_id, "status": "started"})

    @pyqtSlot(str, result=str)
    def get_transcription_status(self, job_id: str) -> str:
        """Check transcription status."""
        if self._transcription_worker and self._transcription_worker.isRunning():
            return json.dumps({"status": "processing"})
        return json.dumps({"status": "idle"})

    @pyqtSlot(str, str, result=str)
    def generate_taglines(self, transcript: str, bulletin_slot: str) -> str:
        """Start async tagline generation."""
        logger.info("Starting tagline generation...")

        self._tagline_worker = TaglineWorker(transcript, bulletin_slot)
        self._tagline_worker.finished.connect(
            lambda data: self.taglineComplete.emit(data)
        )
        self._tagline_worker.start()

        return json.dumps({"status": "started"})

    @pyqtSlot(str, str, str, result=str)
    def export_handoff(self, session_name: str, output_folder: str, approved_content_json: str) -> str:
        """Export approved content to ai_handoff.json."""
        try:
            approved_content = json.loads(approved_content_json)
            
            # If no output folder specified, use default data/sessions
            if not output_folder:
                output_folder = str(
                    Path(__file__).resolve().parent.parent / "data" / "sessions" / session_name
                )

            result = write_handoff(session_name, output_folder, approved_content)

            # Also save session data
            save_session(session_name, {
                "bulletin_slot": approved_content.get("bulletin_slot", "6:55 PM"),
                "priority": approved_content.get("priority", "Headline"),
                "status": "Approved",
                "suggestions_count": len(approved_content.get("suggestions", [])),
                "handoff_path": result.get("file_path", ""),
            })

            return json.dumps(result, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Export error: {e}")
            return json.dumps({"success": False, "error": str(e)})

    @pyqtSlot(result=str)
    def load_dashboard_data(self) -> str:
        """Return dashboard data (mock or from stored sessions)."""
        data = mock_data.get_dashboard_data()
        return json.dumps(data, ensure_ascii=False)

    @pyqtSlot(result=str)
    def browse_folder(self) -> str:
        """Open a native folder browser dialog."""
        folder = QFileDialog.getExistingDirectory(
            self._main_window,
            "Select Output Folder",
            "",
        )
        return json.dumps({"folder": folder if folder else ""})

    @pyqtSlot(result=str)
    def get_app_info(self) -> str:
        """Return application info for the UI."""
        return json.dumps({
            "name": "HiruNews AI Streamline",
            "version": "1.0.0-prototype",
            "phase": "Phase 2 Prototype",
            "developer": "Mr. Vidath Dulanjith",
            "company": "Lotus Technologies (Pvt) Ltd",
            "mock_mode": is_mock_mode(),
        })

    @pyqtSlot(str, str, result=str)
    def save_session_data(self, session_name: str, session_data_json: str) -> str:
        """Save session data to disk."""
        try:
            session_data = json.loads(session_data_json)
            result = save_session(session_name, session_data)
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @pyqtSlot(result=str)
    def list_all_sessions(self) -> str:
        """List all saved sessions."""
        sessions = list_sessions()
        return json.dumps(sessions, ensure_ascii=False)
