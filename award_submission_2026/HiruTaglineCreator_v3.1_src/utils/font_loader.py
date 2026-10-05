"""
Font loader with dynamic paths for cross-device compatibility
"""
from PIL import ImageFont
import os
from utils.font_finder import find_fm_fonts

class FontLoader:
    def __init__(self):
        self.font_cache = {}
        # Dynamically detect fonts on any machine
        self.font_paths = find_fm_fonts()
        
        # Verify fonts exist
        print("\n" + "="*60)
        print("FONT DETECTION:")
        for name, path in self.font_paths.items():
            exists = os.path.exists(path)
            status = "✓" if exists else "✗"
            print(f"  {status} {name}: {path}")
            
        if not self.font_paths:
            print("  ✗ NO FM FONTS FOUND on this system!")
            print("  Please install FMGanganee and FMSandhyanee.")
        print("="*60 + "\n")
    
    def get_font(self, font_name, size):
        """Get font with size"""
        cache_key = f"{font_name}_{size}"
        
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        font_path = self.font_paths.get(font_name)
        
        if not font_path or not os.path.exists(font_path):
            print(f"⚠️ Font '{font_name}' not found! Using Arial fallback")
            try:
                font = ImageFont.truetype("arial.ttf", size)
            except:
                font = ImageFont.load_default()
        else:
            try:
                font = ImageFont.truetype(font_path, size)
            except Exception as e:
                print(f"✗ Error loading {font_name}: {e}")
                try:
                    font = ImageFont.truetype("arial.ttf", size)
                except:
                    font = ImageFont.load_default()
        
        self.font_cache[cache_key] = font
        return font
    
    def is_available(self, font_name):
        """Check if font is available"""
        path = self.font_paths.get(font_name)
        return path and os.path.exists(path)
    
    def get_path(self, font_name):
        """Get font path"""
        return self.font_paths.get(font_name)

# Global instance
font_loader = FontLoader()