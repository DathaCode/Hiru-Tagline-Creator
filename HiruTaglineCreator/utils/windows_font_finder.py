"""
Find fonts using Windows Registry (most reliable method)
"""
import winreg
import os

class WindowsFontFinder:
    def __init__(self):
        self.font_registry = self._read_font_registry()
    
    def _read_font_registry(self):
        """
        Read installed fonts from Windows Registry (both HKLM and HKCU)
        """
        fonts = {}
        
        # Keys to check: Local Machine (System) and Current User (User)
        registry_keys_to_check = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts")
        ]
        
        for hkey, subkey in registry_keys_to_check:
            try:
                registry_key = winreg.OpenKey(hkey, subkey, 0, winreg.KEY_READ)
                i = 0
                while True:
                    try:
                        name, path, _ = winreg.EnumValue(registry_key, i)
                        
                        # If path is not absolute, it is usually in Windows Fonts
                        if not os.path.isabs(path):
                            path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', path)
                        
                        fonts[name] = path
                        i += 1
                    except OSError:
                        break
                
                winreg.CloseKey(registry_key)
            except Exception as e:
                # Some users might not have the HKCU fonts key, which is fine
                pass
                
        return fonts
    
    def find_font(self, font_name_keywords):
        """
        Find font path by searching for keywords in font names
        
        Args:
            font_name_keywords: List of keywords to search for (e.g., ['FM', 'Ganganee'])
        
        Returns:
            Font file path or None
        """
        keywords_lower = [k.lower() for k in font_name_keywords]
        
        for font_name, font_path in self.font_registry.items():
            font_name_lower = font_name.lower()
            
            # Check if all keywords are in the font name
            if all(keyword in font_name_lower for keyword in keywords_lower):
                if os.path.exists(font_path):
                    return font_path
        
        return None
    
    def find_fm_ganganee(self):
        """Find FM GANGANEE font"""
        # Try different keyword combinations
        searches = [
            ['fm', 'ganganee'],
            ['fmganganee'],
            ['ganganee'],
        ]
        
        for keywords in searches:
            path = self.find_font(keywords)
            if path:
                return path
        
        return None
    
    def find_fm_sandhyanee(self):
        """Find FM SANDHYANEE font"""
        searches = [
            ['fm', 'sandhyanee'],
            ['fmsandhyanee'],
            ['sandhyanee'],
        ]
        
        for keywords in searches:
            path = self.find_font(keywords)
            if path:
                return path
        
        return None
    
    def get_all_fm_fonts(self):
        """Get all FM fonts"""
        fm_fonts = {}
        
        for font_name, font_path in self.font_registry.items():
            if 'fm' in font_name.lower() and os.path.exists(font_path):
                fm_fonts[font_name] = font_path
        
        return fm_fonts

# Global instance
font_finder = WindowsFontFinder()
