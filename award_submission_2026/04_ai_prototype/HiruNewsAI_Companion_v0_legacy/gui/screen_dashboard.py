"""
Screen 6 — Dashboard: stats cards, bar chart (QPainter), recent sessions table.
All data from /data/dashboard.json.
"""
import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QSizePolicy, QPushButton,
)
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from core.approval_state import status_colour

_DATA_PATH = Path(__file__).parent.parent / "data" / "dashboard.json"

_STATUS_BG = {
    "Approved":           "#e8f5e9",
    "Rejected":           "#ffebee",
    "Changes Requested":  "#fff3e0",
    "Pending Review":     "#f3f3f3",
}


# ── Bar chart widget ──────────────────────────────────────────────────────────

class BarChart(QWidget):
    """Draws a simple bar chart using QPainter — no external libs required."""

    def __init__(self, data: list):
        super().__init__()
        self._data = data  # list of {"date": "...", "count": N}
        self.setMinimumHeight(160)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def paintEvent(self, _event):
        if not self._data:
            return

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        pad_l, pad_r, pad_t, pad_b = 40, 16, 14, 36

        chart_w = w - pad_l - pad_r
        chart_h = h - pad_t - pad_b

        max_val = max(d["count"] for d in self._data) or 1
        n = len(self._data)
        bar_w = max(8, int(chart_w / n * 0.55))
        gap = int(chart_w / n)

        # Y-axis
        p.setPen(QPen(QColor("#dddddd"), 1))
        for tick in range(0, max_val + 1, max(1, max_val // 4)):
            y = pad_t + chart_h - int(tick / max_val * chart_h)
            p.drawLine(pad_l, y, w - pad_r, y)
            p.setPen(QPen(QColor("#888888"), 1))
            p.setFont(QFont("Segoe UI", 8))
            p.drawText(2, y + 4, str(tick))
            p.setPen(QPen(QColor("#dddddd"), 1))

        # Bars
        for i, d in enumerate(self._data):
            bh = int(d["count"] / max_val * chart_h)
            x = pad_l + i * gap + (gap - bar_w) // 2
            y = pad_t + chart_h - bh

            # Bar fill
            p.fillRect(x, y, bar_w, bh, QColor("#a70003"))

            # Value label above bar
            p.setPen(QPen(QColor("#1a1a1a"), 1))
            p.setFont(QFont("Segoe UI", 8, QFont.Bold))
            p.drawText(QRect(x - 4, y - 18, bar_w + 8, 16), Qt.AlignCenter, str(d["count"]))

            # Date label below
            p.setPen(QPen(QColor("#666666"), 1))
            p.setFont(QFont("Segoe UI", 8))
            date_short = d["date"][5:]  # MM-DD
            p.drawText(
                QRect(x - 8, pad_t + chart_h + 4, bar_w + 16, 20),
                Qt.AlignCenter, date_short
            )

        p.end()


# ── Stat card widget ──────────────────────────────────────────────────────────

class StatCard(QFrame):
    def __init__(self, value: str, label: str, accent: str = "#a70003"):
        super().__init__()
        self.setObjectName("statCard")
        self.setStyleSheet(
            f"QFrame#statCard {{ background: white; border: 1px solid #dddddd; "
            f"border-top: 3px solid {accent}; border-radius: 4px; }}"
        )
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(90)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(4)

        val_lbl = QLabel(value)
        val_lbl.setAlignment(Qt.AlignCenter)
        val_lbl.setStyleSheet(f"font-size: 30px; font-weight: bold; color: {accent};")
        layout.addWidget(val_lbl)

        lbl = QLabel(label)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 11px; color: #666666;")
        layout.addWidget(lbl)


# ── Dashboard screen ──────────────────────────────────────────────────────────

class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        self._data = self._load_data()
        self._build_ui()

    def _load_data(self) -> dict:
        if _DATA_PATH.exists():
            with open(_DATA_PATH, encoding="utf-8") as f:
                return json.load(f)
        return {"stats": {}, "daily_counts": [], "recent_sessions": []}

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 22, 28, 22)
        root.setSpacing(20)

        # Title row
        title_row = QHBoxLayout()
        title = QLabel("Dashboard")
        title.setObjectName("sectionTitle")
        title_row.addWidget(title)
        title_row.addStretch()
        refresh_btn = QPushButton("↻ Refresh")
        refresh_btn.setObjectName("secondaryBtn")
        refresh_btn.setFixedWidth(100)
        refresh_btn.clicked.connect(self._refresh)
        title_row.addWidget(refresh_btn)
        root.addLayout(title_row)

        # Stat cards
        stats = self._data.get("stats", {})
        cards_row = QHBoxLayout()
        cards_row.setSpacing(14)
        cards_row.addWidget(StatCard(
            str(stats.get("generated_today", 0)),
            "Taglines Generated Today", "#a70003"
        ))
        cards_row.addWidget(StatCard(
            str(stats.get("approved_today", 0)),
            "Taglines Approved", "#1a6b1a"
        ))
        cards_row.addWidget(StatCard(
            str(stats.get("pending_review", 0)),
            "Pending Review", "#cc6600"
        ))
        avg = stats.get("avg_time_seconds", 0)
        cards_row.addWidget(StatCard(
            f"{avg}s",
            "Avg Time per Tagline", "#1a4d8f"
        ))
        root.addLayout(cards_row)

        # Bar chart section
        chart_lbl = QLabel("<b>Taglines Created — Last 7 Days</b>")
        root.addWidget(chart_lbl)

        chart_frame = QFrame()
        chart_frame.setStyleSheet(
            "background: white; border: 1px solid #dddddd; border-radius: 4px;"
        )
        chart_frame.setFixedHeight(200)
        chart_inner = QVBoxLayout(chart_frame)
        chart_inner.setContentsMargins(8, 12, 8, 8)
        self._chart = BarChart(self._data.get("daily_counts", []))
        chart_inner.addWidget(self._chart)
        root.addWidget(chart_frame)

        # Recent sessions table
        table_lbl = QLabel("<b>Recent Sessions</b>")
        root.addWidget(table_lbl)

        self._table = QTableWidget()
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(
            ["Session", "Bulletin Slot", "Taglines", "Status", "Timestamp"]
        )
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.setAlternatingRowColors(True)
        self._table.setStyleSheet("alternate-background-color: #fafafa;")
        self._populate_table()
        root.addWidget(self._table, stretch=1)

    def _populate_table(self):
        sessions = self._data.get("recent_sessions", [])
        self._table.setRowCount(len(sessions))
        for row, s in enumerate(sessions):
            status = s.get("status", "")
            colour = status_colour(status)
            bg = _STATUS_BG.get(status, "#f3f3f3")

            items = [
                s.get("name", ""),
                s.get("bulletin_slot", ""),
                str(s.get("tagline_count", "")),
                status,
                s.get("timestamp", ""),
            ]
            for col, val in enumerate(items):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                if col == 3:
                    item.setForeground(QColor(colour))
                self._table.setItem(row, col, item)

    def _refresh(self):
        self._data = self._load_data()
        self._chart._data = self._data.get("daily_counts", [])
        self._chart.update()
        self._populate_table()
