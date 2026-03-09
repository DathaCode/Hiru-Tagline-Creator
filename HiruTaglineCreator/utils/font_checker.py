import os
import tkinter as tk
from tkinter import messagebox
from PIL import ImageFont

def get_font_paths(font_name):
    """Returns a list of possible file paths for a given font name."""
    paths = []
    
    # Possible file names
    filenames = []
    if font_name == 'FM GANGANEE':
        filenames = ['FMGanganee x.ttf', 'FM_GANGANEE.ttf', 'fmganganee.ttf', 'FMGanganee.ttf']
    elif font_name == 'FM SANDHYANEE':
        filenames = ['FMSandhyanee x.ttf', 'FM_SANDHYANEE.ttf', 'fmsandhyanee.ttf', 'FMSandhyanee.ttf']
    else:
        filenames = [font_name + '.ttf', font_name.replace(" ", "").lower() + ".ttf"]
        
    # Directories to search
    dirs = [
        "C:\\Windows\\Fonts",
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'Fonts')
    ]
    
    for d in dirs:
        if os.path.exists(d):
            for f in filenames:
                paths.append(os.path.join(d, f))
                
    return paths

def show_font_installation_dialog(missing_fonts):
    """Show instructions for missing fonts and exit."""
    root = tk.Tk()
    root.withdraw()
    
    font_list = "\n".join([f"• {f}" for f in missing_fonts])
    msg = (f"Required System Fonts Missing:\n{font_list}\n\n"
           f"Please install these fonts and restart the application.\n\n"
           f"Fonts must be installed in Windows Fonts folder:\n"
           f"C:\\Windows\\Fonts\\ or your user Fonts folder.")
           
    messagebox.showerror("Missing Fonts", msg)
    root.destroy()

def check_fonts_installed():
    """Verify required fonts are installed in the system."""
    required_fonts = ['FM GANGANEE', 'FM SANDHYANEE']
    missing_fonts = []
    
    for font_name in required_fonts:
        found = False
        paths_to_try = get_font_paths(font_name)
        
        for path in paths_to_try:
            if os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, 20)
                    found = True
                    break
                except Exception:
                    pass
                    
        if not found:
            # Fallback direct try
            try:
                font = ImageFont.truetype(font_name, 20)
                found = True
            except Exception:
                pass
                
        if not found:
            missing_fonts.append(font_name)
            
    if missing_fonts:
        show_font_installation_dialog(missing_fonts)
        return False
        
    return True
