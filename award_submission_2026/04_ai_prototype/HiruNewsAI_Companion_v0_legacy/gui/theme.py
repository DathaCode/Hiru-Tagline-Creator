"""
Visual theme — Hiru brand palette and shared QSS.
"""

# ── Brand colours ────────────────────────────────────────────
RED    = "#a70003"
DARK   = "#1a0000"
GOLD   = "#d4a017"
WHITE  = "#ffffff"
BG     = "#f5f5f5"
PANEL  = "#ffffff"
TEXT   = "#1a1a1a"
MUTED  = "#666666"
BORDER = "#dddddd"
GREEN  = "#1a6b1a"
ORANGE = "#cc6600"

SIDEBAR_BG     = "#1a0000"
SIDEBAR_ACTIVE = "#a70003"
SIDEBAR_HOVER  = "#2a0a0a"
SIDEBAR_TEXT   = "#ffffff"
SIDEBAR_MUTED  = "#aaaaaa"

APP_QSS = f"""
/* ── Root ───────────────────────────────────────────────── */
QMainWindow, QDialog {{
    background-color: {BG};
}}

QWidget {{
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
    color: {TEXT};
}}

/* ── Header bar ─────────────────────────────────────────── */
QWidget#headerBar {{
    background-color: {DARK};
    border-bottom: 3px solid {RED};
}}

QLabel#appTitle {{
    color: {WHITE};
    font-size: 16px;
    font-weight: bold;
}}

QLabel#screenTitle {{
    color: {GOLD};
    font-size: 13px;
    font-weight: bold;
}}

QLabel#protoBadge {{
    background-color: {GOLD};
    color: {DARK};
    font-size: 10px;
    font-weight: bold;
    padding: 3px 8px;
    border-radius: 3px;
}}

/* ── Sidebar ────────────────────────────────────────────── */
QWidget#sidebar {{
    background-color: {SIDEBAR_BG};
    border-right: 1px solid #2a0a0a;
}}

QLabel#sidebarHeader {{
    color: {GOLD};
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
    padding: 12px 16px 6px 16px;
}}

QPushButton#navBtn {{
    background-color: transparent;
    color: {SIDEBAR_MUTED};
    font-size: 13px;
    text-align: left;
    padding: 10px 16px;
    border: none;
    border-radius: 0px;
    border-left: 3px solid transparent;
}}

QPushButton#navBtn:hover {{
    background-color: {SIDEBAR_HOVER};
    color: {WHITE};
}}

QPushButton#navBtn[active="true"] {{
    background-color: {SIDEBAR_ACTIVE};
    color: {WHITE};
    border-left: 3px solid {GOLD};
    font-weight: bold;
}}

/* ── Status bar ─────────────────────────────────────────── */
QStatusBar {{
    background-color: {DARK};
    color: {SIDEBAR_MUTED};
    font-size: 11px;
    border-top: 1px solid #2a0a0a;
}}

QStatusBar QLabel {{
    color: {SIDEBAR_MUTED};
    font-size: 11px;
    padding: 0 6px;
}}

/* ── Content area ───────────────────────────────────────── */
QWidget#contentArea {{
    background-color: {BG};
}}

/* ── Section title ──────────────────────────────────────── */
QLabel#sectionTitle {{
    font-size: 15px;
    font-weight: bold;
    color: {RED};
    border-bottom: 2px solid {RED};
    padding-bottom: 5px;
}}

/* ── AI warning banner ──────────────────────────────────── */
QLabel#aiBanner {{
    background-color: {GOLD};
    color: {DARK};
    font-size: 12px;
    font-weight: bold;
    padding: 8px 16px;
    border-radius: 4px;
}}

/* ── Stat cards ─────────────────────────────────────────── */
QFrame#statCard {{
    background-color: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 6px;
    border-top: 3px solid {RED};
}}

QLabel#statValue {{
    font-size: 28px;
    font-weight: bold;
    color: {RED};
}}

QLabel#statLabel {{
    font-size: 11px;
    color: {MUTED};
}}

/* ── Buttons ────────────────────────────────────────────── */
QPushButton#primaryBtn {{
    background-color: {RED};
    color: {WHITE};
    font-weight: bold;
    padding: 9px 22px;
    border: none;
    border-radius: 2px;
}}

QPushButton#primaryBtn:hover  {{ background-color: #c0000a; }}
QPushButton#primaryBtn:disabled {{ background-color: #999999; color: #cccccc; }}

QPushButton#secondaryBtn {{
    background-color: transparent;
    color: {RED};
    font-weight: bold;
    padding: 9px 22px;
    border: 2px solid {RED};
    border-radius: 2px;
}}

QPushButton#secondaryBtn:hover {{ background-color: #fff0f0; }}

QPushButton#approveBtn {{
    background-color: {GREEN};
    color: {WHITE};
    font-size: 13px;
    font-weight: bold;
    padding: 10px 24px;
    border: none;
    border-radius: 2px;
}}

QPushButton#approveBtn:hover    {{ background-color: #22882a; }}
QPushButton#approveBtn:disabled {{ background-color: #999999; color: #cccccc; }}

QPushButton#rejectBtn {{
    background-color: {DARK};
    color: {WHITE};
    font-weight: bold;
    padding: 10px 24px;
    border: none;
    border-radius: 2px;
}}

QPushButton#changesBtn {{
    background-color: {ORANGE};
    color: {WHITE};
    font-weight: bold;
    padding: 10px 24px;
    border: none;
    border-radius: 2px;
}}

/* ── Drop zone ──────────────────────────────────────────── */
QLabel#dropZone {{
    background-color: #fff8f8;
    border: 2px dashed {RED};
    border-radius: 6px;
    color: {RED};
    font-size: 14px;
    padding: 40px;
}}

/* ── Inputs ─────────────────────────────────────────────── */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {PANEL};
    border: 1px solid #cccccc;
    border-radius: 2px;
    padding: 6px 8px;
    color: {TEXT};
    selection-background-color: {RED};
    selection-color: {WHITE};
}}

QLineEdit:focus, QTextEdit:focus {{ border: 2px solid {RED}; }}

QComboBox {{
    background-color: {PANEL};
    border: 1px solid #cccccc;
    border-radius: 2px;
    padding: 5px 10px;
    color: {TEXT};
}}

QComboBox:focus {{ border: 2px solid {RED}; }}
QComboBox QAbstractItemView {{
    background-color: {PANEL};
    selection-background-color: {RED};
    selection-color: {WHITE};
}}

/* ── Progress bar ───────────────────────────────────────── */
QProgressBar {{
    border: 1px solid #cccccc;
    border-radius: 2px;
    background-color: #f0f0f0;
    text-align: center;
    font-weight: bold;
    height: 22px;
}}

QProgressBar::chunk {{ background-color: {RED}; border-radius: 2px; }}

/* ── Checkboxes ─────────────────────────────────────────── */
QCheckBox {{
    font-size: 13px;
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px; height: 18px;
    border: 2px solid #aaaaaa;
    border-radius: 3px;
    background-color: {WHITE};
}}

QCheckBox::indicator:checked {{
    background-color: {GREEN};
    border-color: {GREEN};
}}

/* ── Tables ─────────────────────────────────────────────── */
QTableWidget {{
    background-color: {PANEL};
    gridline-color: {BORDER};
    border: 1px solid {BORDER};
}}

QTableWidget QHeaderView::section {{
    background-color: {DARK};
    color: {WHITE};
    font-weight: bold;
    padding: 6px;
    border: none;
}}

QTableWidget::item:selected {{
    background-color: #fff0f0;
    color: {TEXT};
}}

/* ── Scrollbars ─────────────────────────────────────────── */
QScrollBar:vertical {{
    background: #f0f0f0; width: 10px; border-radius: 5px;
}}

QScrollBar::handle:vertical {{
    background: {RED}; border-radius: 5px; min-height: 20px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

/* ── Group boxes ────────────────────────────────────────── */
QGroupBox {{
    border: 1px solid {BORDER};
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 12px;
    font-weight: bold;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 4px;
    color: {RED};
}}
"""
