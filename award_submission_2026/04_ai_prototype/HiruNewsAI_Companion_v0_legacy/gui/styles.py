"""
Shared QSS stylesheet — Hiru brand palette.
  Red   #a70003
  Dark  #1a0000
  Gold  #d4a017
  White #ffffff
  Light #f5f5f5
"""

MAIN_QSS = """
/* ── Base ─────────────────────────────────────────── */
QWidget {
    background-color: #f5f5f5;
    color: #1a0000;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}

/* ── Header bar (set via objectName="header") ────── */
QWidget#header {
    background-color: #1a0000;
}

QLabel#headerTitle {
    color: #ffffff;
    font-size: 18px;
    font-weight: bold;
    letter-spacing: 0.5px;
}

QLabel#headerSubtitle {
    color: #d4a017;
    font-size: 11px;
    font-weight: normal;
    letter-spacing: 0.3px;
}

QLabel#prototypeBadge {
    background-color: #d4a017;
    color: #1a0000;
    font-size: 10px;
    font-weight: bold;
    padding: 3px 8px;
    border-radius: 3px;
}

/* ── Step breadcrumb bar ─────────────────────────── */
QWidget#stepBar {
    background-color: #2a0a0a;
    border-bottom: 2px solid #a70003;
}

QLabel#stepActive {
    color: #ffffff;
    font-size: 12px;
    font-weight: bold;
    padding: 6px 14px;
    background-color: #a70003;
    border-radius: 0px;
}

QLabel#stepInactive {
    color: #888888;
    font-size: 12px;
    padding: 6px 14px;
}

QLabel#stepDone {
    color: #d4a017;
    font-size: 12px;
    padding: 6px 14px;
}

/* ── Section titles ──────────────────────────────── */
QLabel#sectionTitle {
    font-size: 15px;
    font-weight: bold;
    color: #a70003;
    padding-bottom: 4px;
    border-bottom: 2px solid #a70003;
}

/* ── AI warning banner ───────────────────────────── */
QLabel#aiBanner {
    background-color: #d4a017;
    color: #1a0000;
    font-size: 12px;
    font-weight: bold;
    padding: 8px 16px;
    border-radius: 4px;
}

/* ── Primary button ──────────────────────────────── */
QPushButton#primaryBtn {
    background-color: #a70003;
    color: #ffffff;
    font-size: 13px;
    font-weight: bold;
    padding: 9px 24px;
    border: none;
    border-radius: 4px;
}

QPushButton#primaryBtn:hover {
    background-color: #c0000a;
}

QPushButton#primaryBtn:disabled {
    background-color: #888888;
    color: #cccccc;
}

/* ── Secondary button ────────────────────────────── */
QPushButton#secondaryBtn {
    background-color: transparent;
    color: #a70003;
    font-size: 13px;
    font-weight: bold;
    padding: 9px 24px;
    border: 2px solid #a70003;
    border-radius: 4px;
}

QPushButton#secondaryBtn:hover {
    background-color: #fff0f0;
}

/* ── Approve button (green accent) ───────────────── */
QPushButton#approveBtn {
    background-color: #1a6b1a;
    color: #ffffff;
    font-size: 14px;
    font-weight: bold;
    padding: 11px 28px;
    border: none;
    border-radius: 4px;
}

QPushButton#approveBtn:hover {
    background-color: #22882a;
}

QPushButton#approveBtn:disabled {
    background-color: #888888;
    color: #cccccc;
}

/* ── Drop zone ───────────────────────────────────── */
QLabel#dropZone {
    background-color: #fff8f8;
    border: 2px dashed #a70003;
    border-radius: 8px;
    color: #a70003;
    font-size: 14px;
    font-weight: bold;
    padding: 40px;
}

QLabel#dropZone[dragActive="true"] {
    background-color: #ffe0e0;
    border-color: #1a0000;
}

/* ── Input fields ────────────────────────────────── */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 6px 8px;
    color: #1a0000;
    font-size: 13px;
    selection-background-color: #a70003;
    selection-color: #ffffff;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #a70003;
}

/* ── ComboBox ────────────────────────────────────── */
QComboBox {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 5px 10px;
    color: #1a0000;
}

QComboBox:focus {
    border: 2px solid #a70003;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    selection-background-color: #a70003;
    selection-color: #ffffff;
}

/* ── Progress bar ────────────────────────────────── */
QProgressBar {
    border: 1px solid #cccccc;
    border-radius: 4px;
    background-color: #f0f0f0;
    text-align: center;
    font-weight: bold;
    color: #1a0000;
    height: 22px;
}

QProgressBar::chunk {
    background-color: #a70003;
    border-radius: 4px;
}

/* ── Checkbox ─────────────────────────────────────── */
QCheckBox {
    font-size: 13px;
    spacing: 8px;
    color: #1a0000;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #aaaaaa;
    border-radius: 3px;
    background-color: #ffffff;
}

QCheckBox::indicator:checked {
    background-color: #1a6b1a;
    border-color: #1a6b1a;
}

/* ── Tag field group card ────────────────────────── */
QFrame#tagCard {
    background-color: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 6px;
    padding: 8px;
}

QFrame#tagCard[topicHighlight="true"] {
    border-left: 4px solid #a70003;
}

/* ── Warning label ───────────────────────────────── */
QLabel#warnLabel {
    color: #cc6600;
    font-size: 11px;
    font-style: italic;
}

/* ── Transcript text ─────────────────────────────── */
QTextEdit#transcriptArea {
    background-color: #ffffff;
    font-family: "Iskoola Pota", "Noto Sans Sinhala", "Segoe UI", sans-serif;
    font-size: 13px;
    line-height: 1.6;
    border: 1px solid #dddddd;
    border-radius: 4px;
    padding: 8px;
}

/* ── Scroll bar ──────────────────────────────────── */
QScrollBar:vertical {
    background: #f0f0f0;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #a70003;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* ── Separator line ──────────────────────────────── */
QFrame[frameShape="4"] {
    color: #dddddd;
}
"""
