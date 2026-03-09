"""
Hiru News Tagline Creator
Version: 1.0.0
Description: Professional broadcast tagline graphics generator
"""

import sys
import tkinter as tk
from tkinter import messagebox

from utils.config_manager import ConfigManager
from utils.font_checker import check_fonts_installed
from core.template_manager import TemplateManager
from core.session_manager import SessionManager
from gui.main_window import MainWindow

def show_template_setup_dialog():
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning(
        "Templates Missing",
        "Template files (MAIN_TAG.png / SUB_TAG.png) not found or invalid.\n\n"
        "Please place valid 1920x1080 templates in the 'templates' folder."
    )
    root.destroy()

def ask_user_load_draft():
    root = tk.Tk()
    root.withdraw()
    result = messagebox.askyesno(
        "Unsaved Draft",
        "An unsaved draft was found from a previous session.\nWould you like to recover it?"
    )
    root.destroy()
    return result

def main():
    """
    Application entry point
    """
    print("Hiru News Tagline Creator v1.0.0")
    print("Initializing...")
    
    # 1. Load settings
    config_mgr = ConfigManager()
    
    # 2. Check required fonts
    if not check_fonts_installed():
        print("Required fonts missing. Exiting...")
        sys.exit(1)
    
    # 3. Initialize template manager
    template_mgr = TemplateManager(config_mgr)
    
    # 4. Validate templates exist
    if not template_mgr.validate_templates():
        show_template_setup_dialog()
    else:
        # load main and sub tag for testing
        template_mgr.load_template("MAIN_TAG")
        template_mgr.load_template("SUB_TAG")
    
    # 5. Initialize session manager
    session_mgr = SessionManager(config_mgr)
    
    # 6. Create main window
    app = MainWindow(template_mgr, session_mgr, config_mgr)
    
    # 7. Check for unsaved draft
    if session_mgr.has_draft():
        # Prevent ask on startup if no main GUI or just a demo
        # If we uncomment below, it prompts every time there's a draft
        # if ask_user_load_draft():
        #    session_mgr.load_draft_into_ui(app)
        pass # Draft loading dialog check postponed for better user experience until UI exists
    
    # 8. Start main loop
    app.mainloop()

if __name__ == "__main__":
    main()
