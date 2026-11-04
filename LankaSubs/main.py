"""LankaSubs - AI subtitles for Sinhala, Tamil and English videos (Gemini powered)."""
from __future__ import annotations

import os
import sys
import threading

from PySide6.QtCore import QSettings, Qt, QThread, QUrl, Signal
from PySide6.QtGui import QColor, QFont, QFontDatabase
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QAbstractItemView, QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox,
    QFileDialog, QFormLayout, QGroupBox, QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMessageBox, QProgressBar, QPushButton, QSlider, QSpinBox, QSplitter,
    QStyle, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

import engine
from engine import Cue

APP_NAME = "LankaSubs"
MODELS = ["gemini-3.5-flash", "gemini-2.5-flash", "gemini-2.5-pro"]
COL_START, COL_END, COL_ORIG, COL_TEXT = range(4)


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

    def __init__(self, video, cues, target, output, size, margin, box):
        super().__init__()
        self.args = (video, cues, target, output, size, margin, box)
        self._cancel = threading.Event()

    def cancel(self):
        self._cancel.set()

    def run(self):
        video, cues, target, output, size, margin, box = self.args
        try:
            engine.burn_subtitles(video, cues, target, output, size, margin, box,
                                  progress=lambda p, m: self.progress.emit(p, m),
                                  is_cancelled=self._cancel.is_set)
            self.finished_ok.emit(output)
        except engine.CancelledError:
            self.failed.emit("Cancelled.")
        except Exception as e:
            self.failed.emit(str(e))


# ------------------------------------------------------------ settings -------

class SettingsDialog(QDialog):
    def __init__(self, settings: QSettings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.settings = settings
        form = QFormLayout(self)

        self.key = QLineEdit(settings.value("api_key", os.environ.get("GEMINI_API_KEY", "")))
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
        note.setStyleSheet("color: gray;")
        form.addRow(note)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save); buttons.rejected.connect(self.reject)
        form.addRow(buttons)
        self.resize(520, 160)

    def save(self):
        self.settings.setValue("api_key", self.key.text().strip())
        self.settings.setValue("model", self.model.currentText().strip() or engine.DEFAULT_MODEL)
        self.accept()


# ------------------------------------------------------------ main window ----

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} – AI Subtitles (Sinhala • Tamil • English)")
        self.settings = QSettings(APP_NAME, APP_NAME)
        self.video_path = ""
        self.worker = None
        self.cues_target = "Sinhala"

        central = QWidget(); self.setCentralWidget(central)
        root = QVBoxLayout(central)

        # --- Step 1: video + language
        step1 = QGroupBox("1. Choose video and subtitle language")
        s1 = QHBoxLayout(step1)
        self.video_label = QLineEdit(); self.video_label.setReadOnly(True)
        self.video_label.setPlaceholderText("No video selected")
        browse = QPushButton("Browse video…"); browse.clicked.connect(self.pick_video)
        self.lang = QComboBox(); self.lang.addItems(list(engine.LANGUAGES))
        self.lang.setCurrentText(self.settings.value("target", "Sinhala"))
        self.hint = QLineEdit(); self.hint.setPlaceholderText("Optional context, e.g. 'village drama, 3 speakers'")
        self.gen_btn = QPushButton("✨ Generate subtitles"); self.gen_btn.clicked.connect(self.generate)
        settings_btn = QPushButton("⚙ Settings"); settings_btn.clicked.connect(self.open_settings)
        s1.addWidget(self.video_label, 3); s1.addWidget(browse)
        s1.addWidget(QLabel("Subtitles in:")); s1.addWidget(self.lang)
        s1.addWidget(self.hint, 2); s1.addWidget(self.gen_btn); s1.addWidget(settings_btn)
        root.addWidget(step1)

        # --- progress
        prow = QHBoxLayout()
        self.status = QLabel("Ready.")
        self.bar = QProgressBar(); self.bar.setRange(0, 100); self.bar.setValue(0)
        self.cancel_btn = QPushButton("Cancel"); self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_work)
        prow.addWidget(self.status, 2); prow.addWidget(self.bar, 3); prow.addWidget(self.cancel_btn)
        root.addLayout(prow)

        # --- Step 2: preview + editor
        step2 = QGroupBox("2. Review and edit subtitles (double-click a time to jump there)")
        s2 = QVBoxLayout(step2)
        split = QSplitter(Qt.Horizontal)

        left = QWidget(); lv = QVBoxLayout(left); lv.setContentsMargins(0, 0, 0, 0)
        self.video = QVideoWidget(); self.video.setMinimumSize(420, 236)
        self.video.setStyleSheet("background:black;")
        self.overlay = QLabel(""); self.overlay.setAlignment(Qt.AlignCenter); self.overlay.setWordWrap(True)
        self.overlay.setMinimumHeight(64)
        self.overlay.setStyleSheet("background:#111; color:white; padding:6px; border-radius:4px;")
        ctrl = QHBoxLayout()
        self.play_btn = QPushButton(); self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_btn.clicked.connect(self.toggle_play)
        self.seek = QSlider(Qt.Horizontal); self.seek.sliderMoved.connect(lambda v: self.player.setPosition(v))
        self.time_lbl = QLabel("00:00 / 00:00")
        ctrl.addWidget(self.play_btn); ctrl.addWidget(self.seek); ctrl.addWidget(self.time_lbl)
        lv.addWidget(self.video, 1); lv.addWidget(self.overlay); lv.addLayout(ctrl)

        right = QWidget(); rv = QVBoxLayout(right); rv.setContentsMargins(0, 0, 0, 0)
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Start", "End", "Original (spoken)", "Subtitle (shown)"])
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(COL_START, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(COL_END, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(COL_ORIG, QHeaderView.Stretch)
        hh.setSectionResizeMode(COL_TEXT, QHeaderView.Stretch)
        self.table.setWordWrap(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.cellDoubleClicked.connect(self.jump_to_row)
        self.table.itemChanged.connect(self.validate_item)
        tb = QHBoxLayout()
        for text, fn in (("➕ Add line", self.add_row), ("🗑 Delete", self.delete_rows),
                         ("📥 Import SRT", self.import_srt), ("📤 Export SRT", self.export_srt)):
            b = QPushButton(text); b.clicked.connect(fn); tb.addWidget(b)
        tb.addStretch()
        rv.addWidget(self.table, 1); rv.addLayout(tb)

        split.addWidget(left); split.addWidget(right)
        split.setStretchFactor(0, 2); split.setStretchFactor(1, 3)
        s2.addWidget(split)
        root.addWidget(step2, 1)

        # --- Step 3: style + burn
        step3 = QGroupBox("3. Style and export video")
        s3 = QHBoxLayout(step3)
        self.size = QSpinBox(); self.size.setRange(20, 120)
        self.size.setValue(int(self.settings.value("font_size", 54)))
        self.margin = QSpinBox(); self.margin.setRange(0, 400)
        self.margin.setValue(int(self.settings.value("margin", 60)))
        self.box = QCheckBox("Dark box behind text")
        self.box.setChecked(self.settings.value("box", "false") == "true")
        self.burn_btn = QPushButton("🎬 Burn subtitles && save video"); self.burn_btn.clicked.connect(self.burn)
        s3.addWidget(QLabel("Font size:")); s3.addWidget(self.size)
        s3.addWidget(QLabel("Distance from bottom:")); s3.addWidget(self.margin)
        s3.addWidget(self.box); s3.addStretch(); s3.addWidget(self.burn_btn)
        root.addWidget(step3)

        # --- player
        self.player = QMediaPlayer(self); self.audio = QAudioOutput(self)
        self.player.setAudioOutput(self.audio); self.player.setVideoOutput(self.video)
        self.player.positionChanged.connect(self.on_position)
        self.player.durationChanged.connect(lambda d: self.seek.setRange(0, d))
        self.player.playbackStateChanged.connect(self.on_play_state)

        self.apply_fonts()
        self.lang.currentTextChanged.connect(lambda _: self.apply_fonts())
        self.resize(1280, 820)

    # ---------------------------------------------------------------- fonts
    def apply_fonts(self):
        family = engine.LANGUAGES[self.lang.currentText()]["font"]
        self.overlay.setFont(QFont(family, 15))
        self.table.setFont(QFont("Noto Sans Sinhala", 10))  # covers Latin + Sinhala; Tamil falls back

    # -------------------------------------------------------------- helpers
    def api_key(self):
        return self.settings.value("api_key", "") or os.environ.get("GEMINI_API_KEY", "")

    def open_settings(self):
        SettingsDialog(self.settings, self).exec()

    def set_busy(self, busy: bool):
        for w in (self.gen_btn, self.burn_btn, self.lang):
            w.setEnabled(not busy)
        self.cancel_btn.setEnabled(busy)

    def on_progress(self, pct, msg):
        self.bar.setValue(pct); self.status.setText(msg)

    def cancel_work(self):
        if self.worker:
            self.worker.cancel(); self.status.setText("Cancelling…")

    # --------------------------------------------------------------- step 1
    def pick_video(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose video", self.settings.value("last_dir", ""),
            "Videos (*.mp4 *.mov *.mkv *.avi *.webm *.m4v *.wmv *.flv);;All files (*)")
        if not path:
            return
        self.settings.setValue("last_dir", os.path.dirname(path))
        self.video_path = path
        self.video_label.setText(path)
        self.player.setSource(QUrl.fromLocalFile(path))
        self.status.setText("Video loaded. Choose a language and click Generate.")

    def generate(self):
        if not self.video_path:
            return QMessageBox.information(self, APP_NAME, "Choose a video first.")
        if not self.api_key():
            QMessageBox.information(self, APP_NAME, "Add your Gemini API key first.")
            return self.open_settings()
        if self.table.rowCount() and QMessageBox.question(
                self, APP_NAME, "Replace the current subtitles?") != QMessageBox.Yes:
            return
        try:
            engine.find_ffmpeg()
        except FileNotFoundError as e:
            return QMessageBox.critical(self, APP_NAME, str(e))
        target = self.lang.currentText()
        self.settings.setValue("target", target)
        self.worker = GenerateThread(self.video_path, target, self.api_key(),
                                     self.settings.value("model", engine.DEFAULT_MODEL),
                                     self.hint.text().strip())
        self.worker.progress.connect(self.on_progress)
        self.worker.finished_ok.connect(lambda cues, lang: self.on_generated(cues, lang, target))
        self.worker.failed.connect(self.on_failed)
        self.set_busy(True); self.bar.setValue(0); self.worker.start()

    def on_generated(self, cues, lang, target):
        self.set_busy(False)
        self.cues_target = target
        self.load_cues(cues)
        self.status.setText(f"Detected speech: {lang} → {target}. {len(cues)} lines. Review, then burn.")
        if not cues:
            QMessageBox.warning(self, APP_NAME, "No speech was found in this video.")

    def on_failed(self, msg):
        self.set_busy(False); self.bar.setValue(0); self.status.setText("Stopped.")
        if msg != "Cancelled.":
            QMessageBox.critical(self, APP_NAME, msg)

    # --------------------------------------------------------------- table
    def load_cues(self, cues):
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        for c in cues:
            self._append(c)
        self.table.blockSignals(False)
        self.table.resizeRowsToContents()

    def _append(self, c: Cue, row=None):
        row = self.table.rowCount() if row is None else row
        self.table.insertRow(row)
        for col, val in ((COL_START, engine.fmt_srt_time(c.start)), (COL_END, engine.fmt_srt_time(c.end)),
                         (COL_ORIG, c.original), (COL_TEXT, c.text)):
            self.table.setItem(row, col, QTableWidgetItem(val))

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

    def validate_item(self, item):
        if item.column() in (COL_START, COL_END):
            try:
                engine.parse_time(item.text()); item.setBackground(QColor(0, 0, 0, 0))
            except ValueError:
                item.setBackground(QColor("#ffb3b3"))
        if item.column() == COL_TEXT:
            self.table.resizeRowToContents(item.row())

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

    def jump_to_row(self, row, _col):
        try:
            self.player.setPosition(int(engine.parse_time(self.table.item(row, COL_START).text()) * 1000))
            self.player.play()
        except (ValueError, AttributeError):
            pass

    def import_srt(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import SRT", "", "Subtitles (*.srt)")
        if path:
            with open(path, encoding="utf-8-sig", errors="replace") as f:
                self.load_cues(engine.srt_to_cues(f.read()))
            self.cues_target = self.lang.currentText()

    def export_srt(self):
        try:
            cues = self.read_cues()
        except ValueError as e:
            return QMessageBox.warning(self, APP_NAME, str(e))
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
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def on_play_state(self, state):
        icon = QStyle.SP_MediaPause if state == QMediaPlayer.PlayingState else QStyle.SP_MediaPlay
        self.play_btn.setIcon(self.style().standardIcon(icon))

    def on_position(self, ms):
        if not self.seek.isSliderDown():
            self.seek.setValue(ms)
        fmt = lambda x: f"{x // 60000:02d}:{(x // 1000) % 60:02d}"
        self.time_lbl.setText(f"{fmt(ms)} / {fmt(self.player.duration())}")
        t, text = ms / 1000, ""
        for r in range(self.table.rowCount()):
            try:
                s = engine.parse_time(self.table.item(r, COL_START).text())
                e = engine.parse_time(self.table.item(r, COL_END).text())
            except (ValueError, AttributeError):
                continue
            if s <= t < e:
                text = self.table.item(r, COL_TEXT).text() if self.table.item(r, COL_TEXT) else ""
                break
        self.overlay.setText(text)

    # --------------------------------------------------------------- step 3
    def burn(self):
        if not self.video_path:
            return QMessageBox.information(self, APP_NAME, "Choose a video first.")
        try:
            cues = self.read_cues()
        except ValueError as e:
            return QMessageBox.warning(self, APP_NAME, str(e))
        if not cues:
            return QMessageBox.information(self, APP_NAME, "There are no subtitles to burn yet.")
        target = self.lang.currentText()
        base = os.path.splitext(self.video_path)[0]
        out, _ = QFileDialog.getSaveFileName(self, "Save subtitled video",
                                             f"{base}_{target.lower()}_subs.mp4", "MP4 video (*.mp4)")
        if not out:
            return
        if not out.lower().endswith(".mp4"):
            out += ".mp4"
        if os.path.abspath(out) == os.path.abspath(self.video_path):
            return QMessageBox.warning(self, APP_NAME, "Choose a different file name than the original.")
        self.settings.setValue("font_size", self.size.value())
        self.settings.setValue("margin", self.margin.value())
        self.settings.setValue("box", "true" if self.box.isChecked() else "false")
        self.player.pause()
        self.worker = BurnThread(self.video_path, cues, target, out,
                                 self.size.value(), self.margin.value(), self.box.isChecked())
        self.worker.progress.connect(self.on_progress)
        self.worker.finished_ok.connect(self.on_burned)
        self.worker.failed.connect(self.on_failed)
        self.set_busy(True); self.bar.setValue(0); self.worker.start()

    def on_burned(self, out):
        self.set_busy(False)
        self.status.setText(f"Saved: {out}")
        if QMessageBox.question(self, APP_NAME, "Video saved!\n\nOpen the folder?") == QMessageBox.Yes:
            folder = os.path.dirname(out)
            if os.name == "nt":
                os.startfile(folder)

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            if QMessageBox.question(self, APP_NAME, "A job is still running. Quit anyway?") != QMessageBox.Yes:
                return event.ignore()
            self.worker.cancel(); self.worker.wait(5000)
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    if os.path.isdir(engine.fonts_dir()):
        for f in os.listdir(engine.fonts_dir()):
            if f.lower().endswith(".ttf"):
                QFontDatabase.addApplicationFont(os.path.join(engine.fonts_dir(), f))
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
