"""
Text renderer for Hiru News Tagline Creator.
Uses FM Ganganee (Topic Bed) and FM Sandhyanee (Tag/White Beds) via PyQt5.
Unicode text is converted to FM ASCII via convert_unicode_to_fm() before rendering.
English letters are detected and rendered with Arial to avoid FM glyph corruption.

Font sizes:
  Topic Bed:  50.4px
  TAG Bed:    60px
  White Bed:  48px

Text scaling:
  - Short text renders at natural size (scale = 1.0), no stretching
  - Long text is compressed horizontally only (height unchanged)
  - Minimum floor: 0.5 (50% horizontal compression)
  - User's manual H-Scale slider overrides auto-fit when != 100
"""
import os
import sys
from PIL import Image

try:
    from PyQt5.QtGui import QGuiApplication, QImage, QPainter, QFont, QColor, QFontMetrics, QFontDatabase
    from PyQt5.QtCore import Qt, QRect
except ImportError:
    print("PyQt5 is required for proper Sinhala text rendering. Please install it.")
    sys.exit(1)

from utils.fm_converter import convert_unicode_to_fm, has_english_segments, split_fm_and_english
from utils.font_finder import find_fm_fonts

# Ensure QGuiApplication exists
_qapp = QGuiApplication.instance()
if not _qapp:
    _qapp = QGuiApplication(sys.argv)

# English/fallback font for Latin letters mixed into FM text
ENGLISH_FONT_NAME = 'Arial'


class TextRenderer:
    def __init__(self, settings, template_mgr=None):
        self.settings = settings
        self.template_mgr = template_mgr

        fm_paths = find_fm_fonts()

        self.TOPIC_FONT = None
        self.TAG_FONT = None
        self.WHITE_FONT = None

        ganganee_path = fm_paths.get('FM GANGANEE')
        sandhyanee_path = fm_paths.get('FM SANDHYANEE')

        print("\n" + "=" * 70)
        print("FM FONT VERIFICATION (PyQt5 Engine):")

        if ganganee_path and os.path.exists(ganganee_path):
            font_id = QFontDatabase.addApplicationFont(ganganee_path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    self.TOPIC_FONT = families[0]
                    print(f"  ✓ FM GANGANEE loaded: '{self.TOPIC_FONT}' from {ganganee_path}")

        if sandhyanee_path and os.path.exists(sandhyanee_path):
            font_id = QFontDatabase.addApplicationFont(sandhyanee_path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    self.TAG_FONT = families[0]
                    self.WHITE_FONT = families[0]
                    print(f"  ✓ FM SANDHYANEE loaded: '{self.TAG_FONT}' from {sandhyanee_path}")

        if not self.TOPIC_FONT:
            self.TOPIC_FONT = 'Arial'
            print("  ⚠️ TOPIC_FONT falling back to Arial")
        if not self.TAG_FONT:
            self.TAG_FONT = 'Arial'
        if not self.WHITE_FONT:
            self.WHITE_FONT = 'Arial'

        print("=" * 70 + "\n")

    def _get_qfont(self, font_name, size, letter_spacing=0, bold=False):
        """Create a QFont — bold is NOT forced (beds control via settings)."""
        font = QFont(font_name)
        font.setPixelSize(int(round(float(size))))
        if bold:
            font.setBold(True)
        if letter_spacing != 0:
            font.setLetterSpacing(QFont.AbsoluteSpacing, float(letter_spacing))
        return font

    def _measure_width(self, text, font):
        """Measure text width using QFontMetrics.horizontalAdvance."""
        fm = QFontMetrics(font)
        return fm.horizontalAdvance(text)

    def _measure_segments_width(self, segments, fm_font, eng_font):
        """Measure total width of mixed FM/English segments."""
        total = 0
        for seg_text, is_fm in segments:
            font = fm_font if is_fm else eng_font
            total += self._measure_width(seg_text, font)
        return total

    def _compute_fit_scale(self, width, available_width):
        """Scale factor: 1.0 if fits, else compress down to min 0.5."""
        if width <= available_width:
            return 1.0
        return max(available_width / width, 0.5)

    def _qimage_to_pil(self, qimage):
        """Convert QImage to PIL Image safely."""
        qimage = qimage.convertToFormat(QImage.Format_ARGB32)
        buffer = qimage.bits().asstring(qimage.sizeInBytes())
        return Image.frombuffer("RGBA", (qimage.width(), qimage.height()), buffer, "raw", "BGRA", 0, 1)

    def _draw_segments(self, painter, segments, fm_font, eng_font, x, y, h, scale, color):
        """Draw mixed FM/English text segments with appropriate fonts."""
        painter.setPen(QColor(color))
        painter.save()
        painter.translate(x, y)
        if scale < 1.0:
            painter.scale(scale, 1.0)

        cursor_x = 0
        for seg_text, is_fm in segments:
            font = fm_font if is_fm else eng_font
            painter.setFont(font)
            text_rect = QRect(cursor_x, -h // 2, 5000, h)
            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter | Qt.TextDontClip, seg_text)
            cursor_x += QFontMetrics(font).horizontalAdvance(seg_text)

        painter.restore()

    def render_topic_bed(self, text, bed_config, letter_spacing=0):
        """Render Topic Bed using FM GANGANEE font. Ignored letter_spacing per user request."""
        # Force letter_spacing to 0 for Topic bed
        letter_spacing = 0
        text = str(text)
        fm_text = convert_unicode_to_fm(text)
        font_name = self.TOPIC_FONT
        font_size = 50.4

        # Red bed left edge fills the gap (x=126, matches original template)
        bed_x = 126
        y = bed_config['y']
        
        # Original template red bar has slight anti-aliasing artifacts; 
        # ensure our new red bar covers the exact vertical space height=60
        h = bed_config['height']

        # Text left-aligned at x=160 (same as TAG/WHITE beds)
        # 160 - 126 = 34px left padding inside red bed
        LEFT_PAD = 34
        RIGHT_PAD = 34

        fm_font = self._get_qfont(font_name, font_size, letter_spacing)
        eng_font = self._get_qfont(ENGLISH_FONT_NAME, font_size, letter_spacing, bold=True)

        # Split into FM/English segments
        if has_english_segments(fm_text):
            segments = split_fm_and_english(fm_text)
        else:
            segments = [(fm_text, True)]

        text_width = self._measure_segments_width(segments, fm_font, eng_font)

        # Max bg width the red bed can grow to
        max_bg = bed_config.get('width_max', 1780)
        available_text_width = max_bg - LEFT_PAD - RIGHT_PAD

        # Compress only if text exceeds max available width
        scale = self._compute_fit_scale(text_width, available_text_width)
        scaled_text_w = text_width * scale

        # Red background width = left pad + scaled text + right pad
        bg_width = int(LEFT_PAD + scaled_text_w + RIGHT_PAD)
        bg_width = min(bg_width, max_bg)

        qimg = QImage(1920, 1080, QImage.Format_ARGB32)
        qimg.fill(QColor(0, 0, 0, 0))

        painter = QPainter(qimg)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # Red background — left edge at bed_x=126, width scales with text
        bg_color = QColor(bed_config.get('bg_color', '#a70003'))
        painter.fillRect(bed_x, y, bg_width, h, bg_color)

        # Text left-aligned at bed_x + LEFT_PAD (= 160, same as TAG/WHITE beds)
        text_x = bed_x + LEFT_PAD
        text_y = y + (h // 2)

        self._draw_segments(painter, segments, fm_font, eng_font,
                            text_x, text_y, h, scale,
                            bed_config.get('text_color', '#FFFFFF'))
        painter.end()

        print(f"  Topic: size={font_size}pt, bg={bg_width}px, scale={scale:.2f}, text_w={text_width:.0f}, font={font_name}")
        return self._qimage_to_pil(qimg)

    def render_tag_bed_text(self, text, bed_config, h_scale=100, letter_spacing=0):
        """Render TAG Bed using FM SANDHYANEE font."""
        text = str(text)
        fm_text = convert_unicode_to_fm(text)
        font_name = self.TAG_FONT
        font_size = 60

        x = bed_config['x']
        y = bed_config['y']
        w = bed_config['width']
        h = bed_config['height']

        fm_font = self._get_qfont(font_name, font_size, letter_spacing)
        eng_font = self._get_qfont(ENGLISH_FONT_NAME, font_size, letter_spacing, bold=True)

        if has_english_segments(fm_text):
            segments = split_fm_and_english(fm_text)
        else:
            segments = [(fm_text, True)]

        text_width = self._measure_segments_width(segments, fm_font, eng_font)
        available_width = w - 40

        if h_scale < 100:
            scale = h_scale / 100.0
        else:
            scale = self._compute_fit_scale(text_width, available_width)

        text_x = x + 20
        # Move text slightly downward for better vertical centering
        text_y = y + 22 + (h // 2)

        qimg = QImage(1920, 1080, QImage.Format_ARGB32)
        qimg.fill(QColor(0, 0, 0, 0))
        painter = QPainter(qimg)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        self._draw_segments(painter, segments, fm_font, eng_font,
                            text_x, text_y, h, scale,
                            bed_config.get('text_color', '#000000'))
        painter.end()

        img = self._qimage_to_pil(qimg)
        print(f"  TAG: size={font_size}pt, scale={scale:.2f}, font={font_name}")
        return img

    def render_white_bed_text(self, text, bed_config, h_scale=100, letter_spacing=0):
        """Render White Bed using FM SANDHYANEE font. Ignored h_scale and letter_spacing per user request."""
        # Force h_scale and letter_spacing to defaults for White bed
        h_scale = 100
        letter_spacing = 0
        text = str(text)
        fm_text = convert_unicode_to_fm(text)
        font_name = self.WHITE_FONT
        font_size = 48

        x = bed_config['x']
        y = bed_config['y']
        w = bed_config['width']
        h = bed_config['height']

        fm_font = self._get_qfont(font_name, font_size, letter_spacing)
        eng_font = self._get_qfont(ENGLISH_FONT_NAME, font_size, letter_spacing, bold=True)

        if has_english_segments(fm_text):
            segments = split_fm_and_english(fm_text)
        else:
            segments = [(fm_text, True)]

        text_width = self._measure_segments_width(segments, fm_font, eng_font)
        available_width = w - 40

        if h_scale < 100:
            scale = h_scale / 100.0
        else:
            scale = self._compute_fit_scale(text_width, available_width)

        text_x = x + 20
        text_y = y + (h // 2)

        qimg = QImage(1920, 1080, QImage.Format_ARGB32)
        qimg.fill(QColor(0, 0, 0, 0))
        painter = QPainter(qimg)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        self._draw_segments(painter, segments, fm_font, eng_font,
                            text_x, text_y, h, scale,
                            bed_config.get('text_color', '#000000'))
        painter.end()

        img = self._qimage_to_pil(qimg)
        print(f"  White: size={font_size}pt, scale={scale:.2f}, font={font_name}")
        return img

    def save_png(self, img, filepath):
        """Save PNG with UTF-8 filename support."""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            img.save(filepath, 'PNG')
            print(f"✓ Saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"✗ Save error: {e}")
            import re
            safe_path = re.sub(r'[^\x00-\x7F]+', '_', filepath)
            img.save(safe_path, 'PNG')
            print(f"✓ Saved (ASCII): {safe_path}")
            return safe_path
