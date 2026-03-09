"""
Text renderer for Hiru News Tagline Creator.
Uses Iskoola Pota Bold (iskpotab.ttf) - Unicode Sinhala, built into Windows.
FM GANGANEE / FM SANDHYANEE labels in the UI are editorial reference only.

Font sizes as specified:
  Topic Bed:  50.4px (starts at 50.4, auto-shrinks only if text too wide)
  TAG Bed:    60px   (starts at 60, horizontal squeeze via h_scale applied first)
  White Bed:  48px   (starts at 48, auto-shrinks only if text too wide)
"""
import os
import sys
from PIL import Image

try:
    from PyQt5.QtGui import QGuiApplication, QImage, QPainter, QFont, QColor, QFontMetrics
    from PyQt5.QtCore import Qt, QRect
except ImportError:
    print("PyQt5 is required for proper Sinhala text rendering. Please install it.")
    sys.exit(1)

# Ensure QGuiApplication exists to use QFont and QPainter safely
_qapp = QGuiApplication.instance()
if not _qapp:
    _qapp = QGuiApplication(sys.argv)

class TextRenderer:
    def __init__(self, settings, template_mgr=None):
        self.settings = settings
        self.template_mgr = template_mgr
        
        windir = os.environ.get('WINDIR', r'C:\Windows')
        font_dir = os.path.join(windir, 'Fonts')

        self.FONT_NAME = 'Iskoola Pota'
        self.FONT_BOLD = os.path.join(font_dir, 'iskpotab.ttf')
        self.FONT_NORMAL = os.path.join(font_dir, 'iskpota.ttf')

        print("\n" + "=" * 70)
        print("UNICODE FONT VERIFICATION (PyQt5 Engine):")
        print(f"  Iskoola Pota Bold:   {'OK' if os.path.exists(self.FONT_BOLD)   else 'MISSING'}")
        print(f"  Iskoola Pota Normal: {'OK' if os.path.exists(self.FONT_NORMAL) else 'MISSING'}")
        print("=" * 70 + "\n")

    def _get_qfont(self, size, letter_spacing=0):
        """Create a QFont with given pixel size, always bold, and optional letter spacing."""
        font = QFont(self.FONT_NAME)
        font.setPixelSize(int(round(float(size))))
        # Always bold for all beds
        font.setBold(True)
        # Apply letter spacing (absolute pixel spacing between characters)
        if letter_spacing != 0:
            font.setLetterSpacing(QFont.AbsoluteSpacing, float(letter_spacing))
        return font

    def _measure(self, text, font_size, letter_spacing=0):
        font = self._get_qfont(font_size, letter_spacing)
        fm = QFontMetrics(font)
        rect = fm.boundingRect(text)
        return rect.width(), fm.height()

    def calculate_best_fit_size(self, text, max_width, base_size, min_size=24, letter_spacing=0):
        """Search for optimal font size that fits text within max_width."""
        font_size = base_size
        while font_size >= min_size:
            w, h = self._measure(text, font_size, letter_spacing)
            if w <= (max_width - 40):
                print(f"    Best fit: {font_size}pt (width: {w}px, max: {max_width}px)")
                return font_size, w, h
            font_size -= 1
            
        print(f"    ⚠️ Text too long even at {min_size}pt!")
        w, h = self._measure(text, min_size, letter_spacing)
        return min_size, w, h

    def _qimage_to_pil(self, qimage):
        """Convert QImage to PIL Image safely using buffer mapping"""
        qimage = qimage.convertToFormat(QImage.Format_ARGB32)
        buffer = qimage.bits().asstring(qimage.sizeInBytes())
        return Image.frombuffer("RGBA", (qimage.width(), qimage.height()), buffer, "raw", "BGRA", 0, 1)

    def _render_squeezed_text(self, img_bg, text, font_size, tx, ty, tw, th, color, h_scale, letter_spacing=0):
        # Draw perfectly vertically centered text in full bed height 'th'
        # with extra height and width to avoid ligature/descender cutoffs
        qimg = QImage(tw + 80, th + 60, QImage.Format_ARGB32)
        qimg.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(qimg)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setFont(self._get_qfont(font_size, letter_spacing))
        painter.setPen(QColor(color))
        
        rect = QRect(40, 30, tw, th)
        painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter | Qt.TextDontClip, text)
        painter.end()
        
        temp_img = self._qimage_to_pil(qimg)
        
        if h_scale >= 100:
            img_bg.paste(temp_img, (max(0, tx - 40), max(0, ty - 30)), temp_img)
        else:
            new_w = max(1, int(temp_img.width * h_scale / 100))
            try:
                rs = Image.Resampling.LANCZOS
            except AttributeError:
                rs = Image.LANCZOS
            squeezed = temp_img.resize((new_w, temp_img.height), rs)
            img_bg.paste(squeezed, (max(0, tx - 40), max(0, ty - 30)), squeezed)

    def render_topic_bed(self, text, bed_config, letter_spacing=0):
        """
        Render Topic Bed with proper Unicode and left alignment using PyQt5 Engine
        """
        text = str(text)
        x = bed_config['x']
        y = bed_config['y']
        h = bed_config['height']
        
        font_size = 50.4
        text_width, text_height = self._measure(text, font_size, letter_spacing)
        
        bg_width = text_width + 80
        bg_width = max(bg_width, bed_config.get('width_min', 370))
        bg_width = min(bg_width, bed_config.get('width_max', 1110))
        
        qimg = QImage(1920, 1080, QImage.Format_ARGB32)
        qimg.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(qimg)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        
        # Red background
        bg_color = QColor(bed_config.get('bg_color', '#a70003'))
        painter.fillRect(x, y, bg_width, h, bg_color)
        
        # Draw text — shift up by 5px from center for visual correction
        painter.setFont(self._get_qfont(font_size, letter_spacing))
        tc = QColor(bed_config.get('text_color', '#FFFFFF'))
        painter.setPen(tc)
        
        text_x = x + 20
        rect = QRect(text_x, y - 5, bg_width - 20, h)
        painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter | Qt.TextDontClip, text)
        painter.end()
        
        print(f"  Topic: size={font_size}pt, bg={bg_width}px, pos=({text_x},{y})")
        return self._qimage_to_pil(qimg)

    def render_tag_bed_text(self, text, bed_config, h_scale=100, letter_spacing=0):
        """
        Render TAG Bed with proper Unicode and left alignment
        """
        text = str(text)
        x = bed_config['x']
        y = bed_config['y']
        w = bed_config['width']
        h = bed_config['height']
        
        target_width = w - 40
        available_width = target_width if h_scale >= 100 else int(target_width * 100 / max(1, h_scale))
        
        font_size, text_width, text_height = self.calculate_best_fit_size(text, available_width, 60, min_size=30, letter_spacing=letter_spacing)
        
        text_x = x + 20
        img = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
        
        if h_scale < 100:
            # Shift Y axis +10 down to visually align text better
            self._render_squeezed_text(img, text, font_size, text_x, y + 10, text_width, h, bed_config.get('text_color', '#000000'), h_scale, letter_spacing)
        else:
            qimg = QImage(1920, 1080, QImage.Format_ARGB32)
            qimg.fill(QColor(0,0,0,0))
            painter = QPainter(qimg)
            painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
            painter.setFont(self._get_qfont(font_size, letter_spacing))
            painter.setPen(QColor(bed_config.get('text_color', '#000000')))
            # Shift Y axis +10 down
            rect = QRect(text_x, y + 10, w - 20, h)
            painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter | Qt.TextDontClip, text)
            painter.end()
            img = self._qimage_to_pil(qimg)
            
        print(f"  TAG: size={font_size}pt, width={text_width}px/{target_width}px, pos=({text_x},{y})")
        return img

    def render_white_bed_text(self, text, bed_config, h_scale=100, letter_spacing=0):
        """
        Render White Bed with proper Unicode and left alignment
        """
        text = str(text)
        x = bed_config['x']
        y = bed_config['y']
        w = bed_config['width']
        h = bed_config['height']
        
        target_width = w - 40
        available_width = target_width if h_scale >= 100 else int(target_width * 100 / max(1, h_scale))
        
        font_size, text_width, text_height = self.calculate_best_fit_size(text, available_width, 48, min_size=28, letter_spacing=letter_spacing)
        
        text_x = x + 20
        img = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
        
        if h_scale < 100:
            self._render_squeezed_text(img, text, font_size, text_x, y, text_width, h, bed_config.get('text_color', '#000000'), h_scale, letter_spacing)
        else:
            qimg = QImage(1920, 1080, QImage.Format_ARGB32)
            qimg.fill(QColor(0,0,0,0))
            painter = QPainter(qimg)
            painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
            painter.setFont(self._get_qfont(font_size, letter_spacing))
            painter.setPen(QColor(bed_config.get('text_color', '#000000')))
            rect = QRect(text_x, y, w - 20, h)
            painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter | Qt.TextDontClip, text)
            painter.end()
            img = self._qimage_to_pil(qimg)
            
        print(f"  White: size={font_size}pt, width={text_width}px/{target_width}px, pos=({text_x},{y})")
        return img

    def save_png(self, img, filepath):
        """Save PNG with UTF-8 filename support"""
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
