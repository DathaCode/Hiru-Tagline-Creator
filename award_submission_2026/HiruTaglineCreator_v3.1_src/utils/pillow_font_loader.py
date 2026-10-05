"""
Enhanced font loader with Raqm text shaping support
"""
from PIL import Image, ImageDraw, ImageFont, features
import os

class PillowFontLoader:
    def __init__(self):
        self.font_cache = {}
        self.has_raqm = features.check('raqm')

        print("\n" + "="*70)
        print("PILLOW FEATURES:")
        print(f"  Raqm (text shaping): {self.has_raqm}")
        print(f"  FreeType: {features.check('freetype2')}")
        if not self.has_raqm:
            print("\n  ⚠️  Raqm not available — Sinhala complex shaping may be limited")
        print("="*70 + "\n")

        self.font_paths = self._find_fm_fonts()
        self._verify_sinhala_rendering()

    # ── font discovery ──────────────────────────────────────────────────

    def _find_fm_fonts(self):
        fonts = {}

        # Strategy 1: Known user paths
        candidates = {
            'FM GANGANEE':   r"C:\Users\Hp\AppData\Local\Microsoft\Windows\Fonts\FMGanganee x.ttf",
            'FM SANDHYANEE': r"C:\Users\Hp\AppData\Local\Microsoft\Windows\Fonts\FMSandhyanee x.ttf",
        }
        for name, path in candidates.items():
            if os.path.exists(path):
                fonts[name] = path
                print(f"  ✓ Found (hardcoded): {name}")

        # Strategy 2: Search Windows font dirs
        if len(fonts) < 2:
            search_dirs = [
                os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts'),
                os.path.expanduser(r'~\AppData\Local\Microsoft\Windows\Fonts'),
                os.path.expanduser(r'~\AppData\Roaming\Microsoft\Windows\Fonts'),
            ]
            for search_dir in search_dirs:
                if not os.path.isdir(search_dir):
                    continue
                try:
                    for fn in os.listdir(search_dir):
                        fl = fn.lower()
                        if 'ganganee' in fl and 'FM GANGANEE' not in fonts:
                            fonts['FM GANGANEE'] = os.path.join(search_dir, fn)
                            print(f"  ✓ Found (search): FM GANGANEE = {fn}")
                        if 'sandhyanee' in fl and 'FM SANDHYANEE' not in fonts:
                            fonts['FM SANDHYANEE'] = os.path.join(search_dir, fn)
                            print(f"  ✓ Found (search): FM SANDHYANEE = {fn}")
                        if len(fonts) == 2:
                            break
                except Exception as e:
                    print(f"  Search error in {search_dir}: {e}")

        # Strategy 3: Registry
        if len(fonts) < 2:
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                     r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts",
                                     0, winreg.KEY_READ)
                i = 0
                while True:
                    try:
                        name, path, _ = winreg.EnumValue(key, i)
                        nl = name.lower()
                        if 'ganganee' in nl and 'FM GANGANEE' not in fonts:
                            if not os.path.isabs(path):
                                path = os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts', path)
                            if os.path.exists(path):
                                fonts['FM GANGANEE'] = path
                        if 'sandhyanee' in nl and 'FM SANDHYANEE' not in fonts:
                            if not os.path.isabs(path):
                                path = os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts', path)
                            if os.path.exists(path):
                                fonts['FM SANDHYANEE'] = path
                        i += 1
                        if len(fonts) == 2:
                            break
                    except OSError:
                        break
                winreg.CloseKey(key)
            except Exception as e:
                print(f"  Registry search failed: {e}")

        return fonts

    def _verify_sinhala_rendering(self):
        print("VERIFYING SINHALA RENDERING:")
        test_text = "සිංහල"
        for font_name, font_path in self.font_paths.items():
            try:
                font = self._load_font_file(font_path, 50)
                bbox = font.getbbox(test_text)
                w = bbox[2] - bbox[0]
                status = f"width={w}px" if w > 0 else "width=0 — may show boxes"
                mark = "✓" if w > 0 else "⚠"
                print(f"  {mark} {font_name}: {status}")
            except Exception as e:
                print(f"  ✗ {font_name}: {e}")
        print()

    # ── public API ──────────────────────────────────────────────────────

    def _load_font_file(self, path, size):
        """Load a font file, preferring Raqm layout engine when available."""
        if self.has_raqm:
            try:
                return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
            except Exception:
                pass
        return ImageFont.truetype(path, size)

    def get_font(self, font_name, size):
        size = int(round(size))
        key  = f"{font_name}_{size}"
        if key in self.font_cache:
            return self.font_cache[key]

        path = self.font_paths.get(font_name)
        if not path:
            print(f"⚠️  Font '{font_name}' not found — falling back to Arial")
            try:
                font = ImageFont.truetype("arial.ttf", size)
            except Exception:
                font = ImageFont.load_default()
            self.font_cache[key] = font
            return font

        try:
            font = self._load_font_file(path, size)
            self.font_cache[key] = font
            return font
        except Exception as e:
            print(f"✗ Error loading {font_name} @ {size}pt: {e}")
            try:
                font = ImageFont.truetype("arial.ttf", size)
            except Exception:
                font = ImageFont.load_default()
            self.font_cache[key] = font
            return font

    def is_available(self, font_name):
        return font_name in self.font_paths


# Global singleton
pillow_font_loader = PillowFontLoader()
