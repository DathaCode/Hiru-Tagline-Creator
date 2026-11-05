"""LotusSubs - AI subtitles on the Hiru SUB TAG bed, for Sinhala, Tamil and English videos."""
from __future__ import annotations

import os
import sys
import threading
import time

from PySide6.QtCore import QEvent, QSettings, QSizeF, Qt, QThread, QUrl, Signal
from PySide6.QtGui import (
    QColor, QFont, QFontDatabase, QIcon, QKeySequence, QPainter, QPalette, QPixmap, QShortcut,
)
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem
from PySide6.QtWidgets import (
    QAbstractItemView, QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox,
    QFileDialog, QFormLayout, QFrame, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView,
    QHBoxLayout, QHeaderView, QInputDialog, QLabel, QLineEdit, QMainWindow, QMessageBox, QPlainTextEdit,
    QProgressBar, QPushButton, QSlider, QSplitter, QStyle, QStyledItemDelegate, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget,
)

import admin
import engine
import subtag
import version
from engine import Cue

APP_NAME = version.APP_NAME
OLD_SETTINGS_NAME = "LankaSubs"  # the app's old name; its saved settings are copied over once
LOGO_PATH = os.path.join(engine.resource_dir(), "assets", "logo.png")
MODELS = ["gemini-3.5-flash", "gemini-2.5-flash", "gemini-2.5-pro"]
COL_START, COL_END, COL_ORIG, COL_TEXT = range(4)
VIDEO_EXTS = (".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".wmv", ".flv")

STYLE = """
QMainWindow, QDialog { background: #f4f5f7; }
QFrame#header { background: #a70003; }
QLabel#title { color: white; font-size: 17px; font-weight: 700; }
QLabel#subtitle { color: #ffd7d7; }
QFrame#card { background: white; border: 1px solid #dfe2e6; border-radius: 8px; }
QLabel#step { color: #a70003; font-weight: 700; }
QLabel#muted { color: #6b7280; }
QPushButton { padding: 6px 12px; border: 1px solid #c9ced6; border-radius: 6px; background: white; }
QPushButton:hover { background: #f0f2f5; }
QPushButton:disabled { color: #a0a6ad; background: #f4f5f7; }
QPushButton#primary { background: #f7a21b; border-color: #e08e00; color: #1f1f1f; font-weight: 700; padding: 7px 16px; }
QPushButton#primary:hover { background: #ffb43a; }
QPushButton#primary:disabled { background: #f6d9a8; border-color: #ecc98c; color: #8a7b62; }
QPushButton#light { background: transparent; color: white; border: 1px solid #e88a8c; }
QPushButton#light:hover { background: #bd1a1d; }
QLineEdit, QComboBox { padding: 5px 6px; border: 1px solid #c9ced6; border-radius: 6px; background: white; }
QProgressBar { border: 1px solid #dfe2e6; border-radius: 5px; background: white; max-height: 12px; }
QProgressBar::chunk { background: #f7a21b; border-radius: 4px; }
QTableWidget { background: white; border: 1px solid #dfe2e6; gridline-color: #eceef1;
               selection-background-color: #d6e6fb; selection-color: black; }
QHeaderView::section { background: #f4f5f7; border: none; border-bottom: 1px solid #dfe2e6; padding: 5px; font-weight: 600; }
"""


# ------------------------------------------------------------ workers --------

class GenerateThread(QThread):
    progress = Signal(int, str)
    finished_ok = Signal(list, str)
    failed = Signal(str)

    def __init__(self, video, target, api_key, model, hint):
        super().__init__()
        self.args = (video, target, api_key, model, hint)
        self._cancel = threading.Event()

    def cancel(self):
        self._cancel.set()

    def run(self):
        video, target, key, model, hint = self.args
        try:
            cues, lang = engine.generate_subtitles(
                video, target, key, model, hint,
                progress=lambda p, m: self.progress.emit(p, m),
                is_cancelled=self._cancel.is_set)
            self.finished_ok.emit(cues, lang)
        except engine.CancelledError:
            self.failed.emit("Cancelled.")
        except Exception as e:
            self.failed.emit(str(e))


class BurnThread(QThread):
    progress = Signal(int, str)
    finished_ok = Signal(str)
    failed = Signal(str)

    def __init__(self, video, cues, target, output):
        super().__init__()
        self.args = (video, cues, target, output)
        self._cancel = threading.Event()

    def cancel(self):
        self._cancel.set()

    def run(self):
        video, cues, target, output = self.args

        def render_overlay(text, path):
            (subtag.render(text, target) if text else subtag.blank()).save(path)

        try:
            w, h = subtag.bed_size()
            engine.burn_subtitles(video, cues, output, render_overlay,
                                  (w, h, subtag.BED_X, subtag.BED_Y),
                                  progress=lambda p, m: self.progress.emit(p, m),
                                  is_cancelled=self._cancel.is_set)
            self.finished_ok.emit(output)
        except engine.CancelledError:
            self.failed.emit("Cancelled.")
        except Exception as e:
            self.failed.emit(str(e))


# ------------------------------------------------------------ widgets --------

class VideoView(QGraphicsView):
    """Video with the SUB TAG bed drawn on top, at the same place the burn puts it."""
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        scene = QGraphicsScene(self)
        scene.setSceneRect(0, 0, subtag.FRAME_W, subtag.FRAME_H)
        self.setScene(scene)
        self.video = QGraphicsVideoItem()
        self.video.setSize(QSizeF(subtag.FRAME_W, subtag.FRAME_H))
        scene.addItem(self.video)
        self.bed = QGraphicsPixmapItem()
        self.bed.setTransformationMode(Qt.SmoothTransformation)
        self.bed.setZValue(1)
        scene.addItem(self.bed)
        self.hint = scene.addText("Drop a video here, or click Open video")
        self.hint.setDefaultTextColor(QColor("#9aa0a6"))
        self.hint.setFont(QFont("Noto Sans", 44))
        r = self.hint.boundingRect()
        logo = logo_pixmap(300)
        self.hint_logo = scene.addPixmap(logo)
        self.hint_logo.setTransformationMode(Qt.SmoothTransformation)
        self.hint_logo.setOpacity(0.85)
        top = (subtag.FRAME_H - r.height() - (logo.height() + 40 if not logo.isNull() else 0)) / 2
        self.hint_logo.setPos((subtag.FRAME_W - logo.width()) / 2, top)
        self.hint.setPos((subtag.FRAME_W - r.width()) / 2,
                         top + (logo.height() + 40 if not logo.isNull() else 0))

        self.setBackgroundBrush(Qt.black)
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setAcceptDrops(False)  # let the main window take dropped files
        self.setMinimumSize(420, 236)
        self.video.nativeSizeChanged.connect(lambda _: self._place_bed())

    def set_has_video(self, on: bool):
        self.hint.setVisible(not on)
        self.hint_logo.setVisible(not on)

    def set_bed(self, image):
        if image is None:
            self.bed.hide()
            return
        self.bed.setPixmap(QPixmap.fromImage(image))
        self._place_bed()
        self.bed.show()

    def _place_bed(self):
        """Same rule as the burn: the 1920x1080 layout scaled to the video width, bottom anchored."""
        ns = self.video.nativeSize()
        nw, nh = (ns.width(), ns.height()) if ns.width() > 0 and ns.height() > 0 else (subtag.FRAME_W, subtag.FRAME_H)
        fit = min(subtag.FRAME_W / nw, subtag.FRAME_H / nh)
        vw, vh = nw * fit, nh * fit
        vx, vy = (subtag.FRAME_W - vw) / 2, (subtag.FRAME_H - vh) / 2
        k = vw / subtag.FRAME_W
        self.bed.setScale(k)
        self.bed.setPos(vx + subtag.BED_X * k, vy + vh - (subtag.FRAME_H - subtag.BED_Y) * k)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def showEvent(self, event):
        super().showEvent(event)
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def mousePressEvent(self, event):
        self.clicked.emit()


class SubtitleDelegate(QStyledItemDelegate):
    """Multi-line editor for the subtitle column: Enter saves, Shift+Enter starts line 2."""

    def createEditor(self, parent, option, index):
        ed = QPlainTextEdit(parent)
        ed.setTabChangesFocus(True)
        ed.installEventFilter(self)
        return ed

    def setEditorData(self, editor, index):
        editor.setPlainText(index.data() or "")
        editor.selectAll()

    def setModelData(self, editor, model, index):
        model.setData(index, editor.toPlainText().strip())

    def updateEditorGeometry(self, editor, option, index):
        r = option.rect
        r.setHeight(max(r.height(), 84))
        editor.setGeometry(r)

    def eventFilter(self, obj, event):
        if (event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter)
                and not event.modifiers() & Qt.ShiftModifier):
            self.commitData.emit(obj)
            self.closeEditor.emit(obj)
            return True
        return super().eventFilter(obj, event)


def logo_pixmap(size: int) -> QPixmap:
    """The app logo scaled to size x size, or a null pixmap when assets/logo.png is missing."""
    pix = QPixmap(LOGO_PATH)
    if pix.isNull():
        return pix
    return pix.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)


def load_settings() -> QSettings:
    settings = QSettings(APP_NAME, APP_NAME)
    old = QSettings(OLD_SETTINGS_NAME, OLD_SETTINGS_NAME)
    if not settings.allKeys():
        for key in old.allKeys():
            settings.setValue(key, old.value(key))
    old.remove("api_key")  # don't leave a plain-text copy under the old name
    key = settings.value("api_key", "")
    if key and not key.startswith("dpapi:"):  # saved in plain text by an earlier version
        settings.setValue("api_key", admin.protect(key))
    return settings


def card(title: str | None = None):
    frame = QFrame(); frame.setObjectName("card")
    lay = QVBoxLayout(frame); lay.setContentsMargins(12, 10, 12, 10); lay.setSpacing(8)
    if title:
        lbl = QLabel(title); lbl.setObjectName("step"); lay.addWidget(lbl)
    return frame, lay


# ------------------------------------------------------------ settings -------

class SettingsDialog(QDialog):
    def __init__(self, settings: QSettings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.settings = settings
        form = QFormLayout(self)

        self.key = QLineEdit(admin.unprotect(settings.value("api_key", "")))
        self.key.setEchoMode(QLineEdit.Password)
        self.key.setPlaceholderText("Paste your key from aistudio.google.com")
        show = QCheckBox("Show")
        show.toggled.connect(lambda on: self.key.setEchoMode(QLineEdit.Normal if on else QLineEdit.Password))
        row = QHBoxLayout(); row.addWidget(self.key); row.addWidget(show)
        form.addRow("Gemini API key:", row)

        self.model = QComboBox(); self.model.setEditable(True); self.model.addItems(MODELS)
        self.model.setCurrentText(settings.value("model", engine.DEFAULT_MODEL))
        form.addRow("Model:", self.model)
        note = QLabel("Flash is fast and on the free tier. Pro is more accurate but paid.\n"
                      "Free-tier audio may be used by Google to improve its models.")
        note.setObjectName("muted")
        form.addRow(note)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save); buttons.rejected.connect(self.reject)
        form.addRow(buttons)
        self.resize(520, 160)

    def save(self):
        self.settings.setValue("api_key", admin.protect(self.key.text().strip()))
        self.settings.setValue("model", self.model.currentText().strip() or engine.DEFAULT_MODEL)
        self.accept()


# ------------------------------------------------------------ main window ----

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} – Hiru SUB TAG subtitles")
        self.settings = load_settings()
        self.video_path = ""
        self.worker = None
        self._bed_key = None
        self._bad_passwords = 0
        self._settings_locked_until = 0.0
        self.setAcceptDrops(True)

        central = QWidget(); self.setCentralWidget(central)
        root = QVBoxLayout(central); root.setContentsMargins(0, 0, 0, 0); root.setSpacing(0)

        # --- header: name, New session, Settings
        header = QFrame(); header.setObjectName("header")
        hl = QHBoxLayout(header); hl.setContentsMargins(16, 10, 16, 10)
        logo = QLabel(); logo.setPixmap(logo_pixmap(36)); logo.setVisible(not logo.pixmap().isNull())
        title = QLabel(APP_NAME); title.setObjectName("title")
        sub = QLabel("AI subtitles on the SUB TAG bed  •  Sinhala • Tamil • English"); sub.setObjectName("subtitle")
        self.new_btn = QPushButton("＋  New session"); self.new_btn.setObjectName("light")
        self.new_btn.setToolTip("Clear the video and all subtitles (Ctrl+N)")
        self.new_btn.clicked.connect(self.new_session)
        settings_btn = QPushButton("🔒  Settings"); settings_btn.setObjectName("light")
        settings_btn.setToolTip("Gemini key and model (admin password required)")
        settings_btn.clicked.connect(self.open_settings)
        about_btn = QPushButton("ⓘ  About"); about_btn.setObjectName("light")
        about_btn.clicked.connect(self.show_about)
        hl.addWidget(logo); hl.addSpacing(4)
        hl.addWidget(title); hl.addSpacing(12); hl.addWidget(sub); hl.addStretch()
        hl.addWidget(self.new_btn); hl.addWidget(settings_btn); hl.addWidget(about_btn)
        root.addWidget(header)

        body = QWidget(); bl = QVBoxLayout(body); bl.setContentsMargins(14, 12, 14, 12); bl.setSpacing(10)
        root.addWidget(body, 1)

        # --- step 1: video, language, generate
        c1, l1 = card("1  Video and language")
        row = QHBoxLayout()
        self.open_btn = QPushButton("📂  Open video…"); self.open_btn.clicked.connect(self.pick_video)
        self.video_label = QLabel("No video yet – open one or drop it on the window"); self.video_label.setObjectName("muted")
        self.video_label.setMinimumWidth(120)
        self.lang = QComboBox(); self.lang.addItems(list(engine.LANGUAGES))
        self.lang.setCurrentText(self.settings.value("target", "Sinhala"))
        self.hint = QLineEdit(); self.hint.setPlaceholderText("Optional context, e.g. 'news interview, speakers Kamal and Nirosha'")
        self.gen_btn = QPushButton("✨  Generate subtitles"); self.gen_btn.setObjectName("primary")
        self.gen_btn.clicked.connect(self.generate)
        row.addWidget(self.open_btn); row.addWidget(self.video_label, 1)
        row.addWidget(QLabel("Subtitles in:")); row.addWidget(self.lang)
        l1.addLayout(row)
        row2 = QHBoxLayout(); row2.addWidget(self.hint, 1); row2.addWidget(self.gen_btn)
        l1.addLayout(row2)
        bl.addWidget(c1)

        # --- step 2: preview + editor
        split = QSplitter(Qt.Horizontal); split.setChildrenCollapsible(False)

        c2, l2 = card("2  Preview (exactly as it will be burned)")
        self.view = VideoView(); self.view.clicked.connect(self.toggle_play)
        ctrl = QHBoxLayout()
        self.play_btn = QPushButton(); self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_btn.clicked.connect(self.toggle_play)
        self.seek = QSlider(Qt.Horizontal); self.seek.sliderMoved.connect(lambda v: self.player.setPosition(v))
        self.time_lbl = QLabel("00:00 / 00:00"); self.time_lbl.setObjectName("muted")
        ctrl.addWidget(self.play_btn); ctrl.addWidget(self.seek, 1); ctrl.addWidget(self.time_lbl)
        l2.addWidget(self.view, 1); l2.addLayout(ctrl)
        split.addWidget(c2)

        c3, l3 = card("3  Review and edit")
        tip = QLabel("Click a line to preview it • Double-click a time to play from there • "
                     "Shift+Enter puts the rest of a subtitle on line 2")
        tip.setObjectName("muted"); tip.setWordWrap(True)
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Start", "End", "Spoken", "Subtitle (max 2 lines)"])
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(COL_START, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(COL_END, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(COL_ORIG, QHeaderView.Interactive)
        hh.setSectionResizeMode(COL_TEXT, QHeaderView.Stretch)
        self.table.setColumnWidth(COL_ORIG, 170)
        self.table.verticalHeader().setDefaultSectionSize(48)
        self.table.setWordWrap(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setItemDelegateForColumn(COL_TEXT, SubtitleDelegate(self.table))
        self.table.cellDoubleClicked.connect(self.jump_to_row)
        self.table.currentCellChanged.connect(lambda r, *_: self.preview_row(r))
        self.table.itemChanged.connect(self.validate_item)
        tb = QHBoxLayout()
        for text, fn in (("➕ Add line", self.add_row), ("🗑 Delete", self.delete_rows)):
            b = QPushButton(text); b.clicked.connect(fn); tb.addWidget(b)
        tb.addStretch()
        for text, fn in (("📥 Import SRT", self.import_srt), ("📤 Export SRT", self.export_srt)):
            b = QPushButton(text); b.clicked.connect(fn); tb.addWidget(b)
        l3.addWidget(tip); l3.addWidget(self.table, 1); l3.addLayout(tb)
        split.addWidget(c3)
        split.setStretchFactor(0, 1); split.setStretchFactor(1, 1)
        split.setSizes([640, 700])
        bl.addWidget(split, 1)

        # --- step 4: progress + burn
        c4, l4 = card()
        frow = QHBoxLayout()
        step4 = QLabel("4  Export"); step4.setObjectName("step")
        self.status = QLabel("Open a video to start."); self.status.setMinimumWidth(200)
        self.bar = QProgressBar(); self.bar.setRange(0, 100); self.bar.setValue(0); self.bar.setTextVisible(False)
        self.cancel_btn = QPushButton("Cancel"); self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_work)
        self.burn_btn = QPushButton("🎬  Burn SUB TAG video"); self.burn_btn.setObjectName("primary")
        self.burn_btn.clicked.connect(self.burn)
        frow.addWidget(step4); frow.addSpacing(8); frow.addWidget(self.status, 3); frow.addWidget(self.bar, 2)
        frow.addWidget(self.cancel_btn); frow.addWidget(self.burn_btn)
        l4.addLayout(frow)
        bl.addWidget(c4)

        # --- player
        self.player = QMediaPlayer(self); self.audio = QAudioOutput(self)
        self.player.setAudioOutput(self.audio); self.player.setVideoOutput(self.view.video)
        self.player.positionChanged.connect(self.on_position)
        self.player.durationChanged.connect(lambda d: self.seek.setRange(0, d))
        self.player.playbackStateChanged.connect(self.on_play_state)

        QShortcut(QKeySequence("Ctrl+N"), self, self.new_session)
        QShortcut(QKeySequence("Ctrl+O"), self, self.pick_video)

        self.table.setFont(QFont("Noto Sans Sinhala", 10))  # covers Latin + Sinhala; Tamil falls back
        self.lang.currentTextChanged.connect(lambda _: self.refresh_after_edit())
        self.update_buttons()
        self.resize(1360, 860)

    # -------------------------------------------------------------- helpers
    def api_key(self):
        return admin.unprotect(self.settings.value("api_key", "")) or os.environ.get("GEMINI_API_KEY", "")

    def open_settings(self):
        """Settings hold the Gemini key and model, so only the admin may open them."""
        if time.monotonic() < self._settings_locked_until:
            secs = int(self._settings_locked_until - time.monotonic()) + 1
            return QMessageBox.warning(self, APP_NAME, f"Too many wrong passwords. Try again in {secs} s.")
        pw, ok = QInputDialog.getText(self, "Admin password",
                                      "Settings are locked.\nEnter the admin password:", QLineEdit.Password)
        if not ok:
            return
        if not admin.check_password(pw):
            self._bad_passwords += 1
            if self._bad_passwords >= 3:
                self._bad_passwords = 0
                self._settings_locked_until = time.monotonic() + 60
                return QMessageBox.warning(self, APP_NAME, "Wrong password. Settings are locked for 1 minute.")
            return QMessageBox.warning(self, APP_NAME, "Wrong password.")
        self._bad_passwords = 0
        SettingsDialog(self.settings, self).exec()

    def show_about(self):
        box = QMessageBox(self)
        box.setWindowTitle(f"About {APP_NAME}")
        box.setIconPixmap(logo_pixmap(96))
        box.setTextFormat(Qt.RichText)
        box.setText(f"<h3>{APP_NAME} {version.APP_VERSION}</h3>"
                    f"<p>AI subtitles on the Hiru SUB TAG bed<br>Sinhala • Tamil • English</p>"
                    f"<p>Developed by <b>{version.AUTHOR}</b><br>{version.COMPANY}</p>"
                    f"<p>{version.COPYRIGHT}</p>"
                    "<p style='color:#6b7280'>Speech recognition and translation by Google Gemini.<br>"
                    "Noto Sans fonts © Google, SIL Open Font License 1.1.<br>"
                    "Video processing by FFmpeg (ffmpeg.org).</p>")
        box.exec()

    def busy(self):
        return bool(self.worker and self.worker.isRunning())

    def update_buttons(self):
        busy = self.busy()
        for w in (self.open_btn, self.lang):
            w.setEnabled(not busy)
        self.gen_btn.setEnabled(not busy and bool(self.video_path))
        self.burn_btn.setEnabled(not busy and bool(self.video_path) and self.table.rowCount() > 0)
        self.cancel_btn.setEnabled(busy)

    def start_worker(self, worker):
        self.worker = worker
        worker.progress.connect(self.on_progress)
        worker.failed.connect(self.on_failed)
        worker.finished.connect(self.update_buttons)
        self.bar.setValue(0)
        worker.start()
        self.update_buttons()

    def on_progress(self, pct, msg):
        self.bar.setValue(pct); self.status.setText(msg)

    def cancel_work(self):
        if self.busy():
            self.worker.cancel(); self.status.setText("Cancelling…")

    def new_session(self):
        """One click: stop any job and clear the video, subtitles and progress."""
        if self.busy():
            self.worker.blockSignals(True)  # a cancelled job must not report into the new session
            self.worker.cancel(); self.worker.wait(5000)
        self.worker = None
        self.player.stop(); self.player.setSource(QUrl())
        self.video_path = ""
        self.video_label.setText("No video yet – open one or drop it on the window")
        self.hint.clear()
        self.table.setRowCount(0)
        self.bar.setValue(0); self.seek.setRange(0, 0); self.time_lbl.setText("00:00 / 00:00")
        self.view.set_has_video(False); self.show_bed("")
        self.status.setText("New session. Open a video to start.")
        self.update_buttons()

    # --------------------------------------------------------------- step 1
    def pick_video(self):
        if self.busy():
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose video", self.settings.value("last_dir", ""),
            "Videos (" + " ".join("*" + e for e in VIDEO_EXTS) + ");;All files (*)")
        if path:
            self.load_video(path)

    def load_video(self, path):
        self.settings.setValue("last_dir", os.path.dirname(path))
        self.video_path = path
        self.video_label.setText(os.path.basename(path)); self.video_label.setToolTip(path)
        self.player.setSource(QUrl.fromLocalFile(path))
        self.view.set_has_video(True)
        self.status.setText("Video loaded. Choose the subtitle language and click Generate.")
        self.update_buttons()

    def dragEnterEvent(self, event):
        urls = event.mimeData().urls()
        if urls and urls[0].toLocalFile().lower().endswith(VIDEO_EXTS) and not self.busy():
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.load_video(event.mimeData().urls()[0].toLocalFile())

    def generate(self):
        if not self.video_path:
            return QMessageBox.information(self, APP_NAME, "Choose a video first.")
        if not self.api_key():
            return QMessageBox.information(
                self, APP_NAME, "No Gemini API key is set up on this PC.\n"
                                "Ask your administrator to add it in ⚙ Settings.")
        if self.table.rowCount() and QMessageBox.question(
                self, APP_NAME, "Replace the current subtitles?") != QMessageBox.Yes:
            return
        try:
            engine.find_ffmpeg()
        except FileNotFoundError as e:
            return QMessageBox.critical(self, APP_NAME, str(e))
        target = self.lang.currentText()
        self.settings.setValue("target", target)
        worker = GenerateThread(self.video_path, target, self.api_key(),
                                self.settings.value("model", engine.DEFAULT_MODEL),
                                self.hint.text().strip())
        worker.finished_ok.connect(lambda cues, lang: self.on_generated(cues, lang, target))
        self.start_worker(worker)

    def on_generated(self, cues, lang, target):
        self.load_cues(cues)
        self.status.setText(f"Heard {lang}, wrote {target}: {len(cues)} lines. Review them, then burn.")
        self.update_buttons()
        if not cues:
            QMessageBox.warning(self, APP_NAME, "No speech was found in this video.")

    def on_failed(self, msg):
        self.bar.setValue(0); self.status.setText("Stopped.")
        if msg != "Cancelled.":
            QMessageBox.critical(self, APP_NAME, msg)

    # --------------------------------------------------------------- table
    def load_cues(self, cues):
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        for c in cues:
            self._append(c)
        self.table.blockSignals(False)
        self.refresh_after_edit()

    def _append(self, c: Cue, row=None):
        row = self.table.rowCount() if row is None else row
        self.table.insertRow(row)
        for col, val in ((COL_START, engine.fmt_srt_time(c.start)), (COL_END, engine.fmt_srt_time(c.end)),
                         (COL_ORIG, c.original), (COL_TEXT, c.text)):
            self.table.setItem(row, col, QTableWidgetItem(val))
        self.update_buttons()

    def read_cues(self, strict=True):
        cues, bad = [], []
        for r in range(self.table.rowCount()):
            get = lambda col: (self.table.item(r, col).text() if self.table.item(r, col) else "")
            try:
                s, e = engine.parse_time(get(COL_START)), engine.parse_time(get(COL_END))
                if e <= s:
                    raise ValueError
                cues.append(Cue(s, e, get(COL_ORIG), get(COL_TEXT)))
            except ValueError:
                bad.append(r + 1)
        if strict and bad:
            raise ValueError("Fix the times on line(s): " + ", ".join(map(str, bad[:15])) +
                             "\nUse HH:MM:SS,mmm and make End later than Start.")
        cues.sort(key=lambda c: c.start)
        return cues

    def mark_fit(self, item):
        """Amber when a subtitle is squeezed hard, red when it no longer fits the bed."""
        if item is None:
            return
        scale = subtag.fit_scale(item.text(), self.lang.currentText())
        if scale < subtag.MIN_SCALE:
            item.setBackground(QColor("#ffc9c9"))
            item.setToolTip("Too long for the bed – shorten it.")
        elif scale < 0.8:
            item.setBackground(QColor("#ffe7b3"))
            item.setToolTip(f"Squeezed to {scale:.0%} – consider shortening it.")
        else:
            item.setBackground(QColor(0, 0, 0, 0))
            item.setToolTip("")

    def validate_item(self, item):
        if item.column() in (COL_START, COL_END):
            try:
                engine.parse_time(item.text()); item.setBackground(QColor(0, 0, 0, 0))
            except ValueError:
                item.setBackground(QColor("#ffb3b3"))
        if item.column() == COL_TEXT:
            self.table.blockSignals(True)
            self.mark_fit(item)
            self.table.blockSignals(False)
            self.table.resizeRowToContents(item.row())
        self.show_bed(self.text_at(self.player.position()))

    def refresh_after_edit(self):
        self.table.blockSignals(True)
        for r in range(self.table.rowCount()):
            self.mark_fit(self.table.item(r, COL_TEXT))
        self.table.blockSignals(False)
        self.table.resizeRowsToContents()
        self._bed_key = None
        self.show_bed(self.text_at(self.player.position()))
        self.update_buttons()

    def add_row(self):
        rows = sorted({i.row() for i in self.table.selectedIndexes()})
        pos = self.player.position() / 1000
        if rows:
            r = rows[-1]
            try:
                pos = engine.parse_time(self.table.item(r, COL_END).text())
            except (ValueError, AttributeError):
                pass
            self._append(Cue(pos, pos + 2, "", ""), r + 1)
        else:
            self._append(Cue(pos, pos + 2, "", ""))

    def delete_rows(self):
        for r in sorted({i.row() for i in self.table.selectedIndexes()}, reverse=True):
            self.table.removeRow(r)
        self.show_bed(self.text_at(self.player.position()))
        self.update_buttons()

    def row_start_ms(self, row):
        try:
            return int(engine.parse_time(self.table.item(row, COL_START).text()) * 1000)
        except (ValueError, AttributeError):
            return None

    def preview_row(self, row):
        """While paused, selecting a line jumps to it so the preview shows that subtitle."""
        if row < 0 or not self.video_path or self.player.playbackState() == QMediaPlayer.PlayingState:
            return
        ms = self.row_start_ms(row)
        if ms is not None:
            self.player.setPosition(ms + 1)

    def jump_to_row(self, row, _col):
        ms = self.row_start_ms(row)
        if ms is not None and self.video_path:
            self.player.setPosition(ms)
            self.player.play()

    def import_srt(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import SRT", self.settings.value("last_dir", ""),
                                              "Subtitles (*.srt)")
        if path:
            with open(path, encoding="utf-8-sig", errors="replace") as f:
                self.load_cues(engine.srt_to_cues(f.read()))
            self.status.setText(f"Imported {self.table.rowCount()} lines from {os.path.basename(path)}.")

    def export_srt(self):
        try:
            cues = self.read_cues()
        except ValueError as e:
            return QMessageBox.warning(self, APP_NAME, str(e))
        if not cues:
            return QMessageBox.information(self, APP_NAME, "There are no subtitles to export yet.")
        base = os.path.splitext(self.video_path)[0] if self.video_path else "subtitles"
        path, _ = QFileDialog.getSaveFileName(self, "Export SRT",
                                              f"{base}.{self.lang.currentText().lower()}.srt",
                                              "Subtitles (*.srt)")
        if path:
            with open(path, "w", encoding="utf-8-sig") as f:
                f.write(engine.cues_to_srt(cues))
            self.status.setText(f"Saved {path}")

    # --------------------------------------------------------------- player
    def toggle_play(self):
        if not self.video_path:
            return self.pick_video()
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def on_play_state(self, state):
        icon = QStyle.SP_MediaPause if state == QMediaPlayer.PlayingState else QStyle.SP_MediaPlay
        self.play_btn.setIcon(self.style().standardIcon(icon))

    def text_at(self, ms):
        t = ms / 1000
        for r in range(self.table.rowCount()):
            try:
                s = engine.parse_time(self.table.item(r, COL_START).text())
                e = engine.parse_time(self.table.item(r, COL_END).text())
            except (ValueError, AttributeError):
                continue
            if s <= t < e:
                return self.table.item(r, COL_TEXT).text() if self.table.item(r, COL_TEXT) else ""
        return ""

    def show_bed(self, text):
        """The bed shows only while a subtitle is on screen, the same as the burned video."""
        key = (text, self.lang.currentText())
        if key == self._bed_key:
            return
        self._bed_key = key
        self.view.set_bed(subtag.render(text, key[1]) if text.strip() else None)

    def on_position(self, ms):
        if not self.seek.isSliderDown():
            self.seek.setValue(ms)
        fmt = lambda x: f"{x // 60000:02d}:{(x // 1000) % 60:02d}"
        self.time_lbl.setText(f"{fmt(ms)} / {fmt(self.player.duration())}")
        self.show_bed(self.text_at(ms))

    # --------------------------------------------------------------- burn
    def burn(self):
        if not self.video_path:
            return QMessageBox.information(self, APP_NAME, "Choose a video first.")
        try:
            cues = self.read_cues()
        except ValueError as e:
            return QMessageBox.warning(self, APP_NAME, str(e))
        cues = [c for c in cues if c.text.strip()]
        if not cues:
            return QMessageBox.information(self, APP_NAME, "There are no subtitles to burn yet.")
        base = os.path.splitext(self.video_path)[0]
        out, _ = QFileDialog.getSaveFileName(self, "Save subtitled video",
                                             f"{base}_subtag.mp4", "MP4 video (*.mp4)")
        if not out:
            return
        if not out.lower().endswith(".mp4"):
            out += ".mp4"
        if os.path.abspath(out) == os.path.abspath(self.video_path):
            return QMessageBox.warning(self, APP_NAME, "Choose a different file name than the original.")
        self.player.pause()
        worker = BurnThread(self.video_path, cues, self.lang.currentText(), out)
        worker.finished_ok.connect(self.on_burned)
        self.start_worker(worker)

    def on_burned(self, out):
        self.status.setText(f"Saved: {out}")
        if QMessageBox.question(self, APP_NAME, "Video saved!\n\nOpen the folder?") == QMessageBox.Yes:
            if os.name == "nt":
                os.startfile(os.path.dirname(out))

    def closeEvent(self, event):
        if self.busy():
            if QMessageBox.question(self, APP_NAME, "A job is still running. Quit anyway?") != QMessageBox.Yes:
                return event.ignore()
            self.worker.cancel(); self.worker.wait(5000)
        event.accept()


def light_palette() -> QPalette:
    pal = QPalette()
    for role, color in ((QPalette.Window, "#f4f5f7"), (QPalette.WindowText, "#1f2328"),
                        (QPalette.Base, "#ffffff"), (QPalette.AlternateBase, "#f8f9fa"),
                        (QPalette.Text, "#1f2328"), (QPalette.Button, "#ffffff"),
                        (QPalette.ButtonText, "#1f2328"), (QPalette.ToolTipBase, "#ffffff"),
                        (QPalette.ToolTipText, "#1f2328"), (QPalette.PlaceholderText, "#8a9099"),
                        (QPalette.Highlight, "#d6e6fb"), (QPalette.HighlightedText, "#000000"),
                        (QPalette.Mid, "#dfe2e6"), (QPalette.Dark, "#c9ced6")):
        pal.setColor(role, QColor(color))
    pal.setColor(QPalette.Disabled, QPalette.Text, QColor("#a0a6ad"))
    pal.setColor(QPalette.Disabled, QPalette.ButtonText, QColor("#a0a6ad"))
    pal.setColor(QPalette.Disabled, QPalette.WindowText, QColor("#a0a6ad"))
    return pal


def main():
    if os.name == "nt":  # own taskbar entry and icon, not python.exe's, when run from source
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("LotusSubs.LotusSubs")
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(version.APP_VERSION)
    app.setOrganizationName(version.COMPANY)
    if os.path.isfile(LOGO_PATH):
        app.setWindowIcon(QIcon(LOGO_PATH))
    app.setStyle("Fusion")
    app.setPalette(light_palette())  # Windows dark mode would otherwise give white text on these light cards
    app.setStyleSheet(STYLE)
    if os.path.isdir(engine.fonts_dir()):
        for f in os.listdir(engine.fonts_dir()):
            if f.lower().endswith(".ttf"):
                QFontDatabase.addApplicationFont(os.path.join(engine.fonts_dir(), f))
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
