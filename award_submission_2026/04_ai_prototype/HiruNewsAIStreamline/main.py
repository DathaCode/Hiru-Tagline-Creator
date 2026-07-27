"""
HiruNews AI Streamline — Processing Module (Phase 2 Prototype)
AI News Ingestion & Editorial Approval Companion

Architecture: PyQt6 shell with QWebEngineView rendering a React frontend.
Communication via Qt WebChannel bridge.
A local HTTP server is used to serve the frontend (avoids CORS issues with file://).

Lotus Technologies (Pvt) Ltd
Under Asia Broadcasting Corporation (Pvt) Ltd, Sri Lanka
Founder & Developer: Mr. Vidath Dulanjith — DevOps Engineer

SLASSCOM SNIA 2026 — Best Tech for Good Software Innovation
"""

import sys
import os
import logging
import threading
import socket
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PyQt6.QtWebChannel import QWebChannel

from backend.bridge import Bridge

# ─── Logging ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("HiruNewsAI")

# ─── Paths ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
INDEX_HTML = FRONTEND_DIR / "index.html"


# ─── Local HTTP Server ───────────────────────────────────────

class QuietHandler(SimpleHTTPRequestHandler):
    """HTTP handler that serves from frontend dir and suppresses access logs."""

    def log_message(self, format, *args):
        # Suppress noisy per-request logs
        pass

    def end_headers(self):
        # Add CORS and MIME type headers for JSX/JS files
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET")
        # Ensure .jsx files are served with correct MIME type
        if self.path.endswith('.jsx'):
            self.send_header("Content-Type", "application/javascript; charset=utf-8")
        super().end_headers()


def find_free_port():
    """Find an available port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def start_frontend_server(directory, port):
    """Start a local HTTP server in a daemon thread."""
    handler = partial(QuietHandler, directory=str(directory))
    server = HTTPServer(('127.0.0.1', port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info(f"Frontend server started at http://127.0.0.1:{port}")
    return server


# ─── Qt WebEngine ─────────────────────────────────────────────

class WebEnginePage(QWebEnginePage):
    """Custom page to handle JavaScript console messages for debugging."""

    def javaScriptConsoleMessage(self, level, message, line, source):
        level_map = {0: "INFO", 1: "WARNING", 2: "ERROR"}
        level_str = level_map.get(level, "DEBUG")
        logger.debug(f"[JS {level_str}] {source}:{line} — {message}")


class MainWindow(QMainWindow):
    """
    Main application window.
    Embeds QWebEngineView as the central widget, loading the React frontend
    from a local HTTP server to avoid file:// CORS restrictions.
    """

    def __init__(self, frontend_port):
        super().__init__()

        self.setWindowTitle(
            "HiruNews AI Streamline — Processing Module (Phase 2 Prototype)"
        )
        self.setMinimumSize(1280, 800)
        self.resize(1440, 900)

        # Try to set window icon
        icon_path = FRONTEND_DIR / "assets" / "logo.svg"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # ── WebEngineView ─────────────────────────────────────
        self.web_view = QWebEngineView(self)
        self.page = WebEnginePage(self.web_view)
        self.web_view.setPage(self.page)

        # Enable settings for modern web features
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)

        self.setCentralWidget(self.web_view)

        # ── WebChannel bridge ─────────────────────────────────
        self.bridge = Bridge(self)
        self.channel = QWebChannel(self.page)
        self.channel.registerObject("bridge", self.bridge)
        self.page.setWebChannel(self.channel)

        # ── Load the React frontend from local HTTP server ────
        if INDEX_HTML.exists():
            url = QUrl(f"http://127.0.0.1:{frontend_port}/index.html")
            logger.info(f"Loading frontend from: {url.toString()}")
            self.web_view.setUrl(url)
        else:
            logger.error(f"Frontend not found at: {INDEX_HTML}")
            self.web_view.setHtml(
                "<html><body style='background:#0A0A0B;color:#F5F5F7;"
                "font-family:Inter,sans-serif;display:flex;align-items:center;"
                "justify-content:center;height:100vh;margin:0;'>"
                "<div style='text-align:center;'>"
                "<h1>Frontend Not Found</h1>"
                f"<p style='color:#A1A1AA;'>Expected at: {INDEX_HTML}</p>"
                "</div></body></html>"
            )

        # Set background to match dark theme
        self.setStyleSheet("QMainWindow { background-color: #0A0A0B; }")
        self.web_view.setStyleSheet("QWebEngineView { background-color: #0A0A0B; }")


def main():
    # Enable high DPI
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

    # Start local HTTP server for the frontend
    port = find_free_port()
    server = start_frontend_server(FRONTEND_DIR, port)

    app = QApplication(sys.argv)
    app.setApplicationName("HiruNews AI Streamline")
    app.setApplicationVersion("1.0.0-prototype")
    app.setOrganizationName("Lotus Technologies (Pvt) Ltd")

    window = MainWindow(frontend_port=port)
    window.show()

    logger.info("HiruNews AI Streamline started successfully.")
    logger.info(f"Frontend: http://127.0.0.1:{port}/index.html")
    logger.info(f"Mock mode: {Bridge(window).get_app_info()}")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
