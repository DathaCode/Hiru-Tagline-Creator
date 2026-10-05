"""
Find FM fonts dynamically across different Windows PC configurations
"""
import os
from pathlib import Path

def find_fm_fonts():
    """Find FM fonts in user and system directories"""
    
    # Possible directories
    search_dirs = [
        os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts'),  # C:\Windows\Fonts
        os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\Fonts'),  # User fonts
    ]
    
    font_paths = {}
    
    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
        
        try:
            files = os.listdir(search_dir)
        except:
            continue
        
        for filename in files:
            filename_lower = filename.lower()
            
            # Look for Ganganee
            if 'ganganee' in filename_lower and filename.endswith('.ttf'):
                full_path = os.path.join(search_dir, filename)
                if 'FM GANGANEE' not in font_paths:
                    font_paths['FM GANGANEE'] = full_path
                    print(f"✓ Found FM GANGANEE: {full_path}")
            
            # Look for Sandhyanee
            if 'sandhyanee' in filename_lower and filename.endswith('.ttf'):
                full_path = os.path.join(search_dir, filename)
                if 'FM SANDHYANEE' not in font_paths:
                    font_paths['FM SANDHYANEE'] = full_path
                    print(f"✓ Found FM SANDHYANEE: {full_path}")
            
            # Break if both found
            if len(font_paths) == 2:
                break
        
        if len(font_paths) == 2:
            break
    
    return font_paths

if __name__ == "__main__":
    fonts = find_fm_fonts()
    print("\nFound fonts:")
    for name, path in fonts.items():
        print(f"  {name}: {path}")
