import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageFont, ImageDraw
import os
import sys
import platform

from utils.font_checker import get_font_paths


class SettingsDialog(tk.Toplevel):
    """
    Tabbed settings dialog — Templates · Fonts · General · About.
    """

    def __init__(self, parent, config_mgr, template_mgr):
        super().__init__(parent)
        self.title("⚙️  Settings")
        self.geometry("700x580")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self.config_mgr   = config_mgr
        self.template_mgr = template_mgr
        self.result        = False          # True if user clicks Save

        # Notebook
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))

        self._build_templates_tab()
        self._build_fonts_tab()
        self._build_general_tab()
        self._build_about_tab()

        # Bottom buttons
        btn = ttk.Frame(self, padding=8)
        btn.pack(fill=tk.X)
        ttk.Button(btn, text="🔄 Reset to Defaults", command=self._reset_defaults).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn, text="Cancel",               command=self.destroy).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn, text="✓ Save",               command=self._save).pack(side=tk.RIGHT, padx=4)

    # ═════════════════════════════════════════════  TEMPLATES TAB  ═════

    def _build_templates_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.add(tab, text="📁 Templates")

        for label, key, path_key in [
            ("MAIN TAG Template", "main_tag", "main_tag_path"),
            ("SUB TAG Template",  "sub_tag",  "sub_tag_path"),
        ]:
            lf = ttk.LabelFrame(tab, text=label, padding=8)
            lf.pack(fill=tk.X, pady=6)

            row = ttk.Frame(lf)
            row.pack(fill=tk.X)

            cur   = self.config_mgr.get("templates", path_key, f"templates/{key.upper()}.png")
            var   = tk.StringVar(value=cur)
            setattr(self, f"{key}_path_var", var)

            ttk.Label(row, text="File:").pack(side=tk.LEFT)
            ttk.Entry(row, textvariable=var, width=48).pack(side=tk.LEFT, padx=4)
            ttk.Button(row, text="📁 Browse…",
                       command=lambda v=var: self._browse_template(v)).pack(side=tk.LEFT)

            # Dimensions & preview
            info_row = ttk.Frame(lf)
            info_row.pack(fill=tk.X, pady=(4, 0))
            dims_lbl = ttk.Label(info_row, text="", foreground="gray")
            dims_lbl.pack(side=tk.LEFT)
            setattr(self, f"{key}_dims_lbl", dims_lbl)
            self._update_template_info(key)

        # Read-only bed specs
        spec_lf = ttk.LabelFrame(tab, text="Bed Region Specifications (read-only)", padding=8)
        spec_lf.pack(fill=tk.X, pady=6)
        specs = (
            "MAIN TAG:\n"
            "  • TOPIC BED: X=96  Y=572  W=variable  H=62\n"
            "  • TAG BED:   X=104 Y=617  W=1110  H=56\n"
            "  • WHITE BED: X=104 Y=680  W=1110  H=48\n\n"
            "SUB TAG:\n"
            "  • TAG BED:   X=122 Y=751  W=1477  H=58\n"
            "  • WHITE BED: X=140 Y=947  W=1457  H=45"
        )
        ttk.Label(spec_lf, text=specs, font=("Consolas", 9), justify=tk.LEFT).pack(anchor=tk.W)

    def _browse_template(self, var):
        path = filedialog.askopenfilename(
            filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")])
        if path:
            var.set(path)

    def _update_template_info(self, key):
        var = getattr(self, f"{key}_path_var")
        lbl = getattr(self, f"{key}_dims_lbl")
        path = var.get()
        if os.path.exists(path):
            try:
                img = Image.open(path)
                w, h = img.size
                ok = "✓" if (w, h) == (1920, 1080) else "✗ expected 1920×1080"
                lbl.config(text=f"Dimensions: {w} × {h} px  {ok}")
            except Exception:
                lbl.config(text="⚠ Cannot read image")
        else:
            lbl.config(text="⚠ File not found")

    # ═════════════════════════════════════════════  FONTS TAB  ═════════

    def _build_fonts_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.add(tab, text="🔤 Fonts")

        fonts_info = [
            ("TOPIC BED Font", "FM GANGANEE",   "අකුරේගොඩදී නීතිඥවරයා"),
            ("TAG BED Font",   "FM SANDHYANEE", "වෙඩික්කරුවන් දෙදෙනෙකු"),
            ("WHITE BED Font", "FM SANDHYANEE", "සහෝදරයින් දෙදෙනාට"),
        ]

        for label, font_name, sample in fonts_info:
            lf = ttk.LabelFrame(tab, text=label, padding=8)
            lf.pack(fill=tk.X, pady=4)

            installed = self._check_font(font_name)
            status = "✓ Installed" if installed else "✗ NOT installed"
            fg     = "green" if installed else "red"

            ttk.Label(lf, text=f"Font Name: {font_name}").pack(anchor=tk.W)
            ttk.Label(lf, text=f"Status: {status}", foreground=fg,
                      font=("Arial", 10, "bold")).pack(anchor=tk.W)

            # Render a small preview image if installed
            if installed:
                try:
                    preview = self._render_font_preview(font_name, sample)
                    if preview:
                        photo = ImageTk.PhotoImage(preview)
                        img_lbl = ttk.Label(lf, image=photo)
                        img_lbl.image = photo    # prevent GC
                        img_lbl.pack(anchor=tk.W, pady=4)
                except Exception:
                    ttk.Label(lf, text=f"Preview: {sample}").pack(anchor=tk.W)
            else:
                ttk.Label(lf, text=f"Preview: (install font to see preview)").pack(anchor=tk.W)

        # Installation instructions
        inst_lf = ttk.LabelFrame(tab, text="⚠️ Font Installation Instructions", padding=8)
        inst_lf.pack(fill=tk.X, pady=6)
        inst_text = (
            "Required fonts MUST be installed in:\n"
            "C:\\Windows\\Fonts\\  or  your user Fonts folder.\n\n"
            "1. Double-click font file (.ttf)\n"
            "2. Click 'Install' button\n"
            "3. Restart this application"
        )
        ttk.Label(inst_lf, text=inst_text, justify=tk.LEFT).pack(anchor=tk.W)

    def _check_font(self, font_name):
        paths = get_font_paths(font_name)
        for p in paths:
            if os.path.exists(p):
                return True
        try:
            ImageFont.truetype(font_name, 20)
            return True
        except Exception:
            return False

    def _render_font_preview(self, font_name, sample):
        paths = get_font_paths(font_name)
        font = None
        for p in paths:
            if os.path.exists(p):
                try:
                    font = ImageFont.truetype(p, 22)
                    break
                except Exception:
                    pass
        if not font:
            try:
                font = ImageFont.truetype(font_name, 22)
            except Exception:
                return None

        img = Image.new("RGBA", (420, 36), (245, 245, 245, 255))
        draw = ImageDraw.Draw(img)
        draw.text((6, 2), sample, font=font, fill="black")
        return img

    # ═════════════════════════════════════════════  GENERAL TAB  ═══════

    def _build_general_tab(self):
        tab = ttk.Frame(self.nb, padding=12)
        self.nb.add(tab, text="💾 General")

        # Save location
        loc_lf = ttk.LabelFrame(tab, text="Default Save Location", padding=8)
        loc_lf.pack(fill=tk.X, pady=4)
        self.save_loc_var = tk.StringVar(
            value=self.config_mgr.get("session", "default_save_location", "C:/HiruTaglines/"))
        row = ttk.Frame(loc_lf); row.pack(fill=tk.X)
        ttk.Entry(row, textvariable=self.save_loc_var, width=50).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(row, text="📁 Browse…", command=self._browse_save_loc).pack(side=tk.LEFT)

        # Session settings
        sess_lf = ttk.LabelFrame(tab, text="Session Settings", padding=8)
        sess_lf.pack(fill=tk.X, pady=4)

        self.autosave_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(sess_lf, text="Auto-save draft every 60 seconds",
                        variable=self.autosave_var).pack(anchor=tk.W)
        self.remember_var = tk.BooleanVar(
            value=self.config_mgr.get("window", "remember_position", True))
        ttk.Checkbutton(sess_lf, text="Remember window size and position",
                        variable=self.remember_var).pack(anchor=tk.W)

        # Date format
        date_lf = ttk.LabelFrame(tab, text="Date Format for Filenames", padding=8)
        date_lf.pack(fill=tk.X, pady=4)
        self.date_var = tk.StringVar(value="YYYY-MM-DD")
        for fmt, example in [("YYYY-MM-DD", "2026-02-20"),
                             ("DD-MM-YYYY", "20-02-2026"),
                             ("MM-DD-YYYY", "02-20-2026")]:
            ttk.Radiobutton(date_lf, text=f"{fmt}  ({example})",
                            variable=self.date_var, value=fmt).pack(anchor=tk.W)


        # Validation
        val_lf = ttk.LabelFrame(tab, text="Text Validation", padding=8)
        val_lf.pack(fill=tk.X, pady=4)
        ttk.Label(val_lf, text="Validation limits are now hard-coded per bed:\n• Topic: 12 words\n• White: 15 words\n• Tag: 20 words").pack(anchor=tk.W)

    def _browse_save_loc(self):
        d = filedialog.askdirectory()
        if d:
            self.save_loc_var.set(d)

    # ═════════════════════════════════════════════  ABOUT TAB  ═════════

    def _build_about_tab(self):
        tab = ttk.Frame(self.nb, padding=16)
        self.nb.add(tab, text="ℹ️ About")

        ttk.Label(tab, text="🎬  Hiru News Tagline Creator",
                  font=("Arial", 16, "bold")).pack(pady=(8, 2))
        ttk.Label(tab, text="Version 1.0.0",
                  font=("Arial", 11)).pack()
        ttk.Label(tab, text="Professional tagline graphics generator\n"
                            "for broadcast news production",
                  justify=tk.CENTER, foreground="gray").pack(pady=(4, 12))

        sep1 = ttk.Separator(tab); sep1.pack(fill=tk.X, pady=4)

        ttk.Label(tab, text="Built with:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(4, 0))
        for line in ["Python " + platform.python_version(),
                     "Tkinter GUI Framework",
                     "Pillow (PIL) Image Library",
                     "Unicode Conversion API"]:
            ttk.Label(tab, text=f"  • {line}").pack(anchor=tk.W)

        sep2 = ttk.Separator(tab); sep2.pack(fill=tk.X, pady=8)

        ttk.Label(tab, text="Features:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 2))
        for feat in ["Dual template support (MAIN TAG / SUB TAG)",
                     "Automatic Unicode conversion",
                     "Live preview with overlay",
                     "Selective PNG generation with progress",
                     "Session-based workflow  &  auto-save",
                     "Manual text adjustments",
                     "Text validation and warnings"]:
            ttk.Label(tab, text=f"  ✓ {feat}").pack(anchor=tk.W)

        sep3 = ttk.Separator(tab); sep3.pack(fill=tk.X, pady=8)

        ttk.Label(tab, text="📧  support@hirunews.lk\n"
                            "🌐  www.hirunews.lk\n\n"
                            "© 2026 Hiru News. All rights reserved.",
                  justify=tk.LEFT, foreground="gray").pack(anchor=tk.W)

        btn_row = ttk.Frame(tab); btn_row.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(btn_row, text="📋 Copy System Info",
                   command=self._copy_sys_info).pack(side=tk.LEFT)

    def _copy_sys_info(self):
        info = (
            f"App: Hiru News Tagline Creator v1.0.0\n"
            f"OS: {platform.platform()}\n"
            f"Python: {platform.python_version()}\n"
            f"Architecture: {platform.machine()}"
        )
        self.clipboard_clear()
        self.clipboard_append(info)
        messagebox.showinfo("Copied", "System info copied to clipboard.")

    # ═════════════════════════════════════════════  ACTIONS  ═══════════

    def _save(self):
        s = self.config_mgr.settings
        # Templates
        s.setdefault("templates", {})["main_tag_path"] = self.main_tag_path_var.get()
        s["templates"]["sub_tag_path"] = self.sub_tag_path_var.get()
        # Session
        s.setdefault("session", {})["default_save_location"] = self.save_loc_var.get()
        s["session"]["date_format"] = self.date_var.get()
        # Window
        s.setdefault("window", {})["remember_position"] = self.remember_var.get()

        # Validation
        # Validation constraints are now hardcoded in the UI classes.
        self.config_mgr.save()
        self.result = True
        self.destroy()

    def _reset_defaults(self):
        if messagebox.askyesno("Reset", "Reset all settings to factory defaults?"):
            if os.path.exists(self.config_mgr.config_file):
                os.remove(self.config_mgr.config_file)
            self.config_mgr.settings = self.config_mgr._load()
            self.config_mgr.save()
            messagebox.showinfo("Reset", "Settings reset. Please restart the application.")
            self.destroy()
