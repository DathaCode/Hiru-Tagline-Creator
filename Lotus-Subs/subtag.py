"""
SUB TAG overlay: draws a subtitle on the orange Hiru SUB TAG bed.

Geometry is the HiruTaglineCreator SUB_TAG template's TAG bed (1920x1080 frame):
bed at x=140 y=814, 1460x142, two text lines centred at y=850 and y=917, text left
aligned 20px inside the bed, long lines squeezed horizontally down to 50%.
assets/subtag_bed.png is that bed cut out of templates/SUB_TAG.png with the red
title bar and red left edge removed.

Text is Noto Sans (Sinhala / Tamil / Latin) drawn by Qt, which shapes all three scripts.
"""
from __future__ import annotations

import os
from typing import List

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QColor, QFont, QFontMetrics, QImage, QPainter

import engine

FRAME_W, FRAME_H = 1920, 1080
BED_X, BED_Y = 140, 814              # bed position on the 1920x1080 frame
TEXT_PAD = 20                        # left padding inside the bed (tagline: x + 20)
LINE_CENTERS = (36, 103)             # line centres, relative to the bed top
SINGLE_LINE_CENTER = 71              # a one-line subtitle sits in the middle of the bed
LINE_RECT_H = 60
FONT_PX = 46
TEXT_COLOR = "#231F20"
MIN_SCALE = 0.5                      # horizontal squeeze floor, same as the tagline app

_bed: QImage | None = None


def bed_image() -> QImage:
    global _bed
    if _bed is None:
        _bed = QImage(os.path.join(engine.resource_dir(), "assets", "subtag_bed.png"))
        if _bed.isNull():
            raise FileNotFoundError("assets/subtag_bed.png is missing.")
        _bed = _bed.convertToFormat(QImage.Format_ARGB32_Premultiplied)
    return _bed


def bed_size() -> tuple[int, int]:
    b = bed_image()
    return b.width(), b.height()


def text_font(target: str = "Sinhala") -> QFont:
    font = QFont()
    first = engine.LANGUAGES.get(target, engine.LANGUAGES["Sinhala"])["font"]
    font.setFamilies([first] + [f for f in ("Noto Sans Sinhala", "Noto Sans Tamil", "Noto Sans") if f != first])
    font.setPixelSize(FONT_PX)
    font.setBold(True)
    return font


def available_width() -> int:
    return bed_size()[0] - 2 * TEXT_PAD


def split_lines(text: str, font: QFont) -> List[str]:
    """At most two lines. Explicit line breaks win; one long line is broken near the middle."""
    lines = [l.strip() for l in text.replace("\r", "").split("\n") if l.strip()]
    if len(lines) > 2:
        lines = [lines[0], " ".join(lines[1:])]
    if len(lines) == 1:
        fm = QFontMetrics(font)
        words = lines[0].split()
        if fm.horizontalAdvance(lines[0]) > available_width() and len(words) > 1:
            best = min(range(1, len(words)),
                       key=lambda i: abs(fm.horizontalAdvance(" ".join(words[:i])) -
                                         fm.horizontalAdvance(" ".join(words[i:]))))
            lines = [" ".join(words[:best]), " ".join(words[best:])]
    return lines


def fit_scale(text: str, target: str = "Sinhala") -> float:
    """Narrowest horizontal scale any line needs; below MIN_SCALE the text overflows the bed."""
    font = text_font(target)
    fm = QFontMetrics(font)
    widths = [fm.horizontalAdvance(l) for l in split_lines(text, font)]
    return min([min(1.0, available_width() / w) for w in widths if w], default=1.0)


def render(text: str, target: str = "Sinhala") -> QImage:
    """The bed with the subtitle on it, bed-sized (place it at BED_X, BED_Y on 1920x1080)."""
    img = bed_image().copy()
    font = text_font(target)
    lines = split_lines(text, font)
    if not lines:
        return img
    fm = QFontMetrics(font)
    centers = (SINGLE_LINE_CENTER,) if len(lines) == 1 else LINE_CENTERS

    p = QPainter(img)
    p.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
    p.setFont(font)
    p.setPen(QColor(TEXT_COLOR))
    for line, cy in zip(lines, centers):
        width = fm.horizontalAdvance(line)
        scale = 1.0 if width <= available_width() else max(available_width() / width, MIN_SCALE)
        p.save()
        p.translate(TEXT_PAD, cy)
        p.scale(scale, 1.0)
        p.drawText(QRect(0, -LINE_RECT_H // 2, 5000, LINE_RECT_H),
                   Qt.AlignLeft | Qt.AlignVCenter | Qt.TextDontClip, line)
        p.restore()
    p.end()
    return img


def blank() -> QImage:
    w, h = bed_size()
    img = QImage(w, h, QImage.Format_ARGB32_Premultiplied)
    img.fill(Qt.transparent)
    return img
