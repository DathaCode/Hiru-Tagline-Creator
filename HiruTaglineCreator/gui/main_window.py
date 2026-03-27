import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import os
from PIL import Image, ImageDraw

from gui.preview_panel import PreviewPanel
from gui.generation_panel import GenerationPanel
from gui.settings_dialog import SettingsDialog
from core.text_renderer import TextRenderer
from core.text_validator import TextValidator
from utils.tooltip import add_tooltip
from utils.logger import log_info, log_error
from utils.sinhala_unicode_converter import convert_text


# ── Input widgets with Offline Unicode Conversion ───────────────────────────────

class TopicBedInput(ttk.Frame):
    def __init__(self, parent, app):
        ttk.Frame.__init__(self, parent)
        self.app = app
        self.sinhala_mode = tk.BooleanVar(value=True)

        hdr = ttk.Frame(self)
        hdr.pack(fill=tk.X)
        ttk.Label(
            hdr,
            text="🔴 TOPIC BED (Title) - Font: FM GANGANEE 50.4pt | Color: White on Red"
        ).pack(side=tk.LEFT, padx=5, pady=2)

        self.lang_btn = ttk.Button(
            hdr, text="🇸🇮 Sinhala", width=12, command=self.toggle_language
        )
        self.lang_btn.pack(side=tk.RIGHT, padx=5)

        self.entry = tk.Entry(self, font=("Arial", 12), width=60)
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.entry.bind('<KeyRelease>', self.on_change)

        # Real-time preview label for converted text (Unicode rendering)
        self.preview_label = tk.Label(
            self, font=("Iskoola Pota", 14), anchor=tk.W, justify=tk.LEFT,
            bg='white', fg='black'
        )
        self.preview_label.pack(fill=tk.X, padx=5, pady=2)

        self.word_label = ttk.Label(self, text="0 words")
        self.word_label.pack(anchor=tk.W, padx=5)

    def toggle_language(self):
        self.sinhala_mode.set(not self.sinhala_mode.get())
        if self.sinhala_mode.get():
            self.lang_btn.config(text="🇸🇮 Sinhala")
        else:
            self.lang_btn.config(text="🌐 English")
        self.on_change()

    def on_change(self, event=None):
        raw_text = self.entry.get()
        converted = convert_text(raw_text) if self.sinhala_mode.get() else raw_text
        self.preview_label.config(text=converted)
        words = len(converted.split())
        color = "red" if words > 12 else "black"
        warn  = " ⚠️ (max: 12)" if words > 12 else ""
        self.word_label.config(text=f"{words} words{warn}", foreground=color)
        if hasattr(self.app, 'schedule_preview_update'):
            self.app.schedule_preview_update()

    def get_text(self):
        """Returns the fully converted text for rendering."""
        return self.preview_label.cget('text')
        
    def get_raw_text(self):
        return self.entry.get()

    def set_text(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.on_change()


class TagBedInput(ttk.Frame):
    def __init__(self, parent, app):
        ttk.Frame.__init__(self, parent)
        self.app = app
        self.sinhala_mode = tk.BooleanVar(value=True)

        hdr = ttk.Frame(self)
        hdr.pack(fill=tk.X)
        ttk.Label(
            hdr,
            text="🟠 TAG BED (Multi-line) - Font: FM SANDHYANEE 60pt | Color: Black"
        ).pack(side=tk.LEFT, padx=5, pady=2)

        self.lang_btn = ttk.Button(
            hdr, text="🇸🇮 Sinhala", width=12, command=self.toggle_language
        )
        self.lang_btn.pack(side=tk.RIGHT, padx=5)

        # Input text area (Singlish)
        text_frame = ttk.Frame(self)
        self.text = tk.Text(text_frame, font=("Arial", 11), height=8, width=60, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, command=self.text.yview)
        self.text.config(yscrollcommand=scrollbar.set)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        self.text.bind('<KeyRelease>', self.on_change)
        self.text.bind('<ButtonRelease-1>', self.on_change)

        # Converted Preview area (Unicode text)
        preview_frame = ttk.Frame(self)
        self.preview = tk.Text(
            preview_frame, font=("Iskoola Pota", 12), height=8, width=60, 
            wrap=tk.WORD, bg='lightyellow', state=tk.DISABLED
        )
        preview_scroll = ttk.Scrollbar(preview_frame, command=self.preview.yview)
        self.preview.config(yscrollcommand=preview_scroll.set)
        self.preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        self.line_label = ttk.Label(self, text="0 lines")
        self.line_label.pack(anchor=tk.W, padx=5)

    def toggle_language(self):
        self.sinhala_mode.set(not self.sinhala_mode.get())
        if self.sinhala_mode.get():
            self.lang_btn.config(text="🇸🇮 Sinhala")
        else:
            self.lang_btn.config(text="🌐 English")
        self.on_change()

    def on_change(self, event=None):
        raw_text = self.text.get('1.0', tk.END).strip()
        
        if self.sinhala_mode.get():
            lines = raw_text.splitlines()
            converted_lines = [convert_text(line) for line in lines]
            converted = '\n'.join(converted_lines)
        else:
            converted = raw_text
            
        self.preview.config(state=tk.NORMAL)
        self.preview.delete('1.0', tk.END)
        self.preview.insert('1.0', converted)
        self.preview.config(state=tk.DISABLED)

        num_lines = len([l for l in converted.splitlines() if l.strip()])
        self.line_label.config(text=f"{num_lines} lines")

        if hasattr(self.app, '_on_tag_text_change'):
            self.app._on_tag_text_change()
        if hasattr(self.app, 'schedule_preview_update'):
            self.app.schedule_preview_update()

    def get_lines(self):
        """Returns list of converted Unicode lines from preview widget."""
        text = self.preview.get('1.0', tk.END).strip()
        return [line.strip() for line in text.splitlines() if line.strip()]
        
    def get_raw_text(self):
        return self.text.get('1.0', tk.END).strip()

    def set_text(self, text):
        self.text.delete('1.0', tk.END)
        self.text.insert('1.0', text)
        self.on_change()


class WhiteBedInput(ttk.Frame):
    def __init__(self, parent, app):
        ttk.Frame.__init__(self, parent)
        self.app = app
        self.sinhala_mode = tk.BooleanVar(value=True)

        hdr = ttk.Frame(self)
        hdr.pack(fill=tk.X)
        ttk.Label(
            hdr,
            text="⬜ WHITE BED (Single line) - Font: FM SANDHYANEE 48pt | Color: Black"
        ).pack(side=tk.LEFT, padx=5, pady=2)

        self.lang_btn = ttk.Button(
            hdr, text="🇸🇮 Sinhala", width=12, command=self.toggle_language
        )
        self.lang_btn.pack(side=tk.RIGHT, padx=5)

        self.entry = tk.Entry(self, font=("Arial", 12), width=60)
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.entry.bind('<KeyRelease>', self.on_change)

        self.preview_label = tk.Label(
            self, font=("Iskoola Pota", 13), anchor=tk.W, justify=tk.LEFT,
            bg='white', fg='black'
        )
        self.preview_label.pack(fill=tk.X, padx=5, pady=2)

        self.word_label = ttk.Label(self, text="0 words")
        self.word_label.pack(anchor=tk.W, padx=5)

    def toggle_language(self):
        self.sinhala_mode.set(not self.sinhala_mode.get())
        if self.sinhala_mode.get():
            self.lang_btn.config(text="🇸🇮 Sinhala")
        else:
            self.lang_btn.config(text="🌐 English")
        self.on_change()

    def on_change(self, event=None):
        raw_text = self.entry.get()
        converted = convert_text(raw_text) if self.sinhala_mode.get() else raw_text
        self.preview_label.config(text=converted)

        words = len(converted.split())
        color = "red" if words > 15 else "black"
        warn  = " ⚠️ (max: 15)" if words > 15 else ""
        self.word_label.config(text=f"{words} words{warn}", foreground=color)
        if hasattr(self.app, 'schedule_preview_update'):
            self.app.schedule_preview_update()

    def get_text(self):
        """Returns the fully converted text for rendering."""
        return self.preview_label.cget('text')
        
    def get_raw_text(self):
        return self.entry.get()

    def set_text(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.on_change()




class MainWindow(tk.Tk):
    def __init__(self, template_mgr, session_mgr, settings):
        super().__init__()
        self.template_mgr = template_mgr
        self.session_mgr  = session_mgr
        self.settings_mgr = settings

        self.title("🎬 Hiru News Tagline Creator v1.1")
        w = self.settings_mgr.get("window", "width",  1600)
        h = self.settings_mgr.get("window", "height", 1000)
        self.geometry(f"{w}x{h}")
        self.minsize(1100, 700)

        self.text_renderer = TextRenderer(self.settings_mgr.settings, self.template_mgr)
        self.validator      = TextValidator(self.settings_mgr.settings)

        self.current_template = "MAIN_TAG"
        
        # We track h_scale and letter_spacing
        self.adjustments = {'h_scale': 100, 'letter_spacing': 0}
        self._preview_timer = None

        self._build_ui()
        self._setup_shortcuts()
        self._setup_auto_save()
        log_info("Application window initialized")
        self.preview_panel.load_template(self.current_template)
        self.schedule_preview_update()

    def _build_ui(self):
        top = ttk.Frame(self, padding=(10, 6))
        top.pack(fill=tk.X)

        ttk.Label(top, text="Session:", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        self.session_var   = tk.StringVar()
        self.session_combo = ttk.Combobox(top, textvariable=self.session_var, state="readonly", width=28)
        self.session_combo.pack(side=tk.LEFT, padx=(6, 0))
        self.session_combo.bind("<<ComboboxSelected>>", self._on_session_selected)

        b1 = ttk.Button(top, text="🆕 New",      command=self._new_session); b1.pack(side=tk.LEFT, padx=4)
        b2 = ttk.Button(top, text="💾 Save",     command=self._save_session); b2.pack(side=tk.LEFT, padx=4)
        b3 = ttk.Button(top, text="📂 Open Folder", command=self._open_folder); b3.pack(side=tk.LEFT, padx=4)
        b4 = ttk.Button(top, text="⚙️ Settings", command=self._open_settings); b4.pack(side=tk.RIGHT, padx=4)

        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        left  = ttk.Frame(paned)
        right = ttk.Frame(paned)
        paned.add(left,  weight=4)
        paned.add(right, weight=6)

        self._build_left(left)
        self._build_right(right)

        bot = ttk.Frame(self, padding=(10, 4))
        bot.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(bot, textvariable=self.status_var, font=("Arial", 9), foreground="gray").pack(side=tk.LEFT)
        ttk.Button(bot, text="🗑️ Clear All", command=self._clear_all).pack(side=tk.RIGHT, padx=4)

    def _build_left(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.X)
        self.notebook.add(ttk.Frame(self.notebook), text="📺  MAIN TAG")
        self.notebook.add(ttk.Frame(self.notebook), text="📋  SUB TAG")
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

        outer = ttk.Frame(parent)
        outer.pack(fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(outer, orient=tk.VERTICAL)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._input_canvas = tk.Canvas(outer, yscrollcommand=vsb.set, highlightthickness=0)
        vsb.config(command=self._input_canvas.yview)
        self._input_canvas.pack(fill=tk.BOTH, expand=True)

        self.input_frame = ttk.Frame(self._input_canvas)
        self._icw = self._input_canvas.create_window((0, 0), window=self.input_frame, anchor=tk.NW)
        self.input_frame.bind('<Configure>', lambda e: self._input_canvas.configure(scrollregion=self._input_canvas.bbox(tk.ALL)))
        self._input_canvas.bind('<Configure>', lambda e: self._input_canvas.itemconfig(self._icw, width=e.width))

        # Topic BED
        self.topic_bed_frame = ttk.Frame(self.input_frame)
        self.topic_bed_frame.pack(fill=tk.X, padx=10, pady=10)
        self.topic_input = TopicBedInput(self.topic_bed_frame, self)
        self.topic_input.pack(fill=tk.X)

        # TAG BED
        self.tag_bed_frame = ttk.Frame(self.input_frame)
        self.tag_bed_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tag_input = TagBedInput(self.tag_bed_frame, self)
        self.tag_input.pack(fill=tk.BOTH, expand=True)

        # WHITE BED
        self.white_bed_frame = ttk.Frame(self.input_frame)
        self.white_bed_frame.pack(fill=tk.X, padx=10, pady=10)
        self.white_input = WhiteBedInput(self.white_bed_frame, self)
        self.white_input.pack(fill=tk.X)

        # Adjustment Panel (Horizontal Scaling)
        self.create_adjustment_panel()

        # GENERATION PANEL
        self.gen_panel = GenerationPanel(
            self.input_frame,
            session_mgr=self.session_mgr,
            text_renderer=self.text_renderer,
            validator=self.validator,
            get_inputs_fn=self._get_inputs,
            get_template_fn=lambda: self.current_template,
            get_adjustments_fn=lambda: self.adjustments,
        )
        self.gen_panel.pack(fill=tk.X, padx=6, pady=(8, 6))

    def create_adjustment_panel(self):
        adj_frame = ttk.LabelFrame(self.input_frame, text="🎛️ Text Adjustments (selected TAG line)")
        adj_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # ── Horizontal Scaling ──────────────────────────────────
        scale_frame = ttk.Frame(adj_frame)
        ttk.Label(scale_frame, text="Horizontal Scale:").pack(side=tk.LEFT, padx=5)
        
        self.h_scale_var = tk.IntVar(value=100)
        scale_slider = ttk.Scale(
            scale_frame,
            from_=50,
            to=100,
            variable=self.h_scale_var,
            orient=tk.HORIZONTAL,
            command=self.on_scale_change
        )
        scale_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.scale_value_label = ttk.Label(scale_frame, text="100%")
        self.scale_value_label.pack(side=tk.LEFT, padx=5)
        scale_frame.pack(fill=tk.X, padx=5, pady=(8, 2))
        
        ttk.Button(adj_frame, text="🔄 Reset Scale", command=self.reset_scaling).pack(anchor=tk.W, padx=5, pady=(0, 6))

        # ── Letter Spacing ──────────────────────────────────────
        ls_frame = ttk.Frame(adj_frame)
        ttk.Label(ls_frame, text="Letter Spacing: ").pack(side=tk.LEFT, padx=5)

        self.letter_spacing_var = tk.IntVar(value=0)
        ls_slider = ttk.Scale(
            ls_frame,
            from_=-10,
            to=30,
            variable=self.letter_spacing_var,
            orient=tk.HORIZONTAL,
            command=self.on_letter_spacing_change
        )
        ls_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.ls_value_label = ttk.Label(ls_frame, text="0 px")
        self.ls_value_label.pack(side=tk.LEFT, padx=5)
        ls_frame.pack(fill=tk.X, padx=5, pady=2)

        ttk.Button(adj_frame, text="🔄 Reset Spacing", command=self.reset_letter_spacing).pack(anchor=tk.W, padx=5, pady=(0, 6))

        ttk.Label(
            adj_frame,
            text="Horizontal Scale: compress text width | Letter Spacing: adjust space between characters",
            font=("Arial", 9, "italic"),
            foreground="gray"
        ).pack(padx=5, pady=2)

    def on_scale_change(self, value):
        val = int(float(value))
        self.h_scale_var.set(val)
        self.scale_value_label.config(text=f"{val}%")
        self.adjustments['h_scale'] = val
        self.schedule_preview_update()

    def reset_scaling(self):
        self.h_scale_var.set(100)
        self.adjustments['h_scale'] = 100
        self.scale_value_label.config(text="100%")
        self.schedule_preview_update()

    def on_letter_spacing_change(self, value):
        val = int(float(value))
        self.letter_spacing_var.set(val)
        self.ls_value_label.config(text=f"{val} px")
        self.adjustments['letter_spacing'] = val
        self.schedule_preview_update()

    def reset_letter_spacing(self):
        self.letter_spacing_var.set(0)
        self.adjustments['letter_spacing'] = 0
        self.ls_value_label.config(text="0 px")
        self.schedule_preview_update()

    def _build_right(self, parent):
        ttk.Label(parent, text="🎨  LIVE PREVIEW", font=("Arial", 11, "bold")).pack(anchor=tk.W, padx=6, pady=(4, 0))
        self.preview_panel = PreviewPanel(parent, self.template_mgr)
        self.preview_panel.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)
        # Wire TAG selector → live re-render
        self.preview_panel.on_tag_select_callback = self.schedule_preview_update

    def _on_tab_change(self, _event):
        try:
            idx = self.notebook.index(self.notebook.select())
            
            if idx == 0:
                new_template = "MAIN_TAG"
            else:
                new_template = "SUB_TAG"
                
            if getattr(self, 'current_template', None) == new_template:
                return
                
            print(f"\n{'='*60}")
            print(f"TAB SWITCH: {self.current_template} → {new_template}")
            print(f"{'='*60}")

            self.current_template = new_template
            self.preview_panel.load_template(self.current_template)

            # Update generation panel for new template type
            self.gen_panel.set_template_type(new_template)
            
            # Show/Hide logic exactly as requested
            if new_template == 'MAIN_TAG':
                print("  Layout: Topic Bed + TAG Bed + White Bed")
                if hasattr(self, 'topic_bed_frame'):
                    self.topic_bed_frame.pack(fill=tk.X, padx=10, pady=10, before=self.tag_bed_frame)
                if hasattr(self, 'tag_bed_frame'):
                    self.tag_bed_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, after=self.topic_bed_frame)
                if hasattr(self, 'white_bed_frame'):
                    self.white_bed_frame.pack(fill=tk.X, padx=10, pady=10, after=self.tag_bed_frame)
                self.gen_panel.set_topic_visible(True)
            else:
                print("  Layout: Topic Bed + TAG Bed (White Bed HIDDEN)")
                if hasattr(self, 'topic_bed_frame'):
                    self.topic_bed_frame.pack(fill=tk.X, padx=10, pady=10, before=self.tag_bed_frame)
                if hasattr(self, 'tag_bed_frame'):
                    self.tag_bed_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, after=self.topic_bed_frame)
                if hasattr(self, 'white_bed_frame'):
                    self.white_bed_frame.pack_forget()
                self.gen_panel.set_topic_visible(True)
            
            print(f"{'='*60}\n")
            self.schedule_preview_update()
        except Exception as e:
            print(f"\u2717 Tab switch error: {e}")
            import traceback
            traceback.print_exc()

    def get_topic_text_for_rendering(self):
        if hasattr(self, 'topic_input'):
            text = self.topic_input.preview_label.cget('text')
            if isinstance(text, bytes):
                text = text.decode('utf-8')
            text = str(text).strip()
            
            print(f"\n[GET TOPIC TEXT]")
            print(f"  Type: {type(text)}")
            print(f"  Length: {len(text)}")
            print(f"  Sample: '{text[:50]}...'")
            return text
        return ""

    def get_tag_lines_for_rendering(self):
        if hasattr(self, 'tag_input'):
            text = self.tag_input.preview.get('1.0', tk.END).strip()
            if isinstance(text, bytes):
                text = text.decode('utf-8')
            text = str(text)
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            print(f"\n[GET TAG LINES]")
            print(f"  Total lines: {len(lines)}")
            for i, line in enumerate(lines[:3]):
                print(f"  Line {i+1}: '{line[:50]}...'")
            return lines
        return []

    def get_white_text_for_rendering(self):
        if hasattr(self, 'white_input'):
            text = self.white_input.preview_label.cget('text')
            if isinstance(text, bytes):
                text = text.decode('utf-8')
            text = str(text).strip()
            
            print(f"\n[GET WHITE TEXT]")
            print(f"  Type: {type(text)}")
            print(f"  Sample: '{text[:50]}...'")
            return text
        return ""

    def _on_tag_text_change(self):
        tag_lines = self.tag_input.get_lines()
        self.gen_panel.update_tag_lines(tag_lines)
        self._push_text_labels()
        
    def schedule_preview_update(self):
        if self._preview_timer:
            self.after_cancel(self._preview_timer)
        self._preview_timer = self.after(100, self.update_preview)

    def get_selected_tag_index(self):
        try:
            return self.preview_panel.tag_selector.current()
        except Exception:
            return 0

    def update_preview(self):
        try:
            if not hasattr(self.preview_panel, 'template_image') or self.preview_panel.template_image is None:
                self.preview_panel.load_template(self.current_template)
            
            if self.preview_panel.template_image is None:
                return

            preview_img = self.preview_panel.template_image.copy().convert('RGBA')
            template_type = self.current_template
            renderer = self.text_renderer
            h_scale  = self.h_scale_var.get()
            letter_spacing = self.adjustments.get('letter_spacing', 0)

            # Get converted TAG lines from preview widget (correct Unicode)
            tag_lines = self.tag_input.get_lines() if hasattr(self, 'tag_input') else []

            # Update the TAG selector dropdown list
            if template_type == 'SUB_TAG':
                # Show pairs in the selector
                pairs = []
                for p in range(0, len(tag_lines), 2):
                    l1 = tag_lines[p][:25] if p < len(tag_lines) else ''
                    l2 = tag_lines[p+1][:25] if p+1 < len(tag_lines) else ''
                    pairs.append(f"Pair {len(pairs)+1}: {l1}...")
                self.preview_panel.tag_selector['values'] = pairs
                if pairs:
                    idx = self.preview_panel.selected_tag_index
                    if idx >= len(pairs):
                        idx = 0
                        self.preview_panel.selected_tag_index = 0
                    self.preview_panel.tag_selector.current(idx)
            else:
                self.preview_panel.update_tag_selector(tag_lines)

            # Respect the DROPDOWN selection — do NOT override with cursor position.
            selected_index = self.get_selected_tag_index()

            def get_bed(name):
                return self.template_mgr.get_bed_config(template_type, name)

            # TOPIC BED — both MAIN_TAG and SUB_TAG have a red title bar
            if hasattr(self, 'topic_input'):
                topic_text = self.get_topic_text_for_rendering()
                if topic_text:
                    try:
                        bed_config = get_bed('TOPIC_BED')
                        if bed_config:
                            # Clear the pre-baked red bar from the template so our
                            # dynamically-sized red bar is the only one visible.
                            bx = bed_config.get('x', 126)
                            by = bed_config.get('y', 750)
                            bh = bed_config.get('height', 64)
                            cw = 1800
                            clear_patch = Image.new('RGBA', (cw, bh), (0, 0, 0, 0))
                            preview_img.paste(clear_patch, (bx, by))
                            
                            topic_img = renderer.render_topic_bed(topic_text, bed_config, letter_spacing)
                            preview_img = Image.alpha_composite(preview_img, topic_img.convert('RGBA'))
                    except Exception as ex:
                        print(f'\u2717 Topic Bed render error: {ex}')
            
            # TAG BED — show the selected tag/pair in the dropdown
            if template_type == 'SUB_TAG':
                # SUB_TAG: render 2 lines per pair
                pair_count = (len(tag_lines) + 1) // 2
                if tag_lines and 0 <= selected_index < pair_count:
                    try:
                        bed_config = get_bed('TAG_BED')
                        if bed_config:
                            s = selected_index * 2
                            l1 = tag_lines[s] if s < len(tag_lines) else ''
                            l2 = tag_lines[s+1] if s+1 < len(tag_lines) else ''
                            tag_img = renderer.render_sub_tag_bed_text(
                                l1, l2, bed_config, h_scale, letter_spacing)
                            preview_img = Image.alpha_composite(preview_img, tag_img.convert('RGBA'))
                    except Exception as ex:
                        print(f'\u2717 SUB TAG Bed render error: {ex}')
            else:
                # MAIN_TAG: single line
                if tag_lines and 0 <= selected_index < len(tag_lines):
                    selected_line = tag_lines[selected_index]
                    try:
                        bed_config = get_bed('TAG_BED')
                        if bed_config:
                            tag_img = renderer.render_tag_bed_text(selected_line, bed_config, h_scale, letter_spacing)
                            preview_img = Image.alpha_composite(preview_img, tag_img.convert('RGBA'))
                    except Exception as ex:
                        print(f'\u2717 TAG Bed render error: {ex}')
            
            # WHITE BED — MAIN TAG only
            if template_type == 'MAIN_TAG':
                white_text = self.get_white_text_for_rendering()
                if white_text:
                    try:
                        bed_config = get_bed('WHITE_BED')
                        if bed_config:
                            white_img = renderer.render_white_bed_text(white_text, bed_config, h_scale, letter_spacing)
                            preview_img = Image.alpha_composite(preview_img, white_img.convert('RGBA'))
                    except Exception as ex:
                        print(f'\u2717 White Bed render error: {ex}')
            
            self.preview_panel.display_preview_image(preview_img)
            self.session_mgr.unsaved_changes = True
        except Exception as e:
            print(f'\u2717 Preview error: {e}')
            import traceback
            traceback.print_exc()

    def _get_inputs(self):
        """Returns exact converted text for PNG generation."""
        topic = self.get_topic_text_for_rendering()
        tags  = self.get_tag_lines_for_rendering()
        white = self.get_white_text_for_rendering() if self.current_template == "MAIN_TAG" else ""
        return topic, tags, white

    def _push_text_labels(self):
        topic = self.get_topic_text_for_rendering()
        white = self.get_white_text_for_rendering() if self.current_template == "MAIN_TAG" else ""
        self.gen_panel.update_text_labels(topic, white)

    def _on_session_selected(self, event=None):
        selected_session = self.session_var.get()
        if not selected_session:
            return
            
        self.session_mgr.current_session_path = os.path.join(self.session_mgr.base_dir, selected_session)
        
        draft = self.session_mgr.load_draft()
        if draft:
            content = draft.get("content", {})
            
            if "topic_bed_raw" in content:
                self.topic_input.set_text(content.get("topic_bed_raw", ""))
            else:
                self.topic_input.set_text(content.get("topic_bed", ""))
                
            if "tag_lines_raw" in content:
                self.tag_input.set_text(content.get("tag_lines_raw", ""))
            else:
                lines = content.get("tag_lines", [])
                self.tag_input.set_text("\n".join(lines))
                
            if "white_bed_raw" in content:
                self.white_input.set_text(content.get("white_bed_raw", ""))
            else:
                self.white_input.set_text(content.get("white_bed", ""))
            
            template_type = draft.get("template_type", "MAIN_TAG")
            if template_type == "MAIN_TAG":
                self.notebook.select(0)
            elif template_type == "SUB_TAG":
                self.notebook.select(1)
            
            adj = draft.get("adjustments", {})
            self.h_scale_var.set(adj.get("h_scale", 100))
            self.adjustments["h_scale"] = adj.get("h_scale", 100)
            self.scale_value_label.config(text=f"{self.adjustments['h_scale']}%")
            
            self.letter_spacing_var.set(adj.get("letter_spacing", 0))
            self.adjustments["letter_spacing"] = adj.get("letter_spacing", 0)
            self.ls_value_label.config(text=f"{self.adjustments['letter_spacing']} px")
            
            self.status_var.set(f"Loaded session '{selected_session}'")
            self.schedule_preview_update()
        else:
            self._clear_all()
            self.status_var.set(f"Session '{selected_session}' has no saved draft.")

    def _new_session(self):
        name = simpledialog.askstring("New Session", "Enter session name (e.g. AKUREGODA):", parent=self)
        if not name: return
        path = self.session_mgr.create_session(name.strip().upper())
        
        # Set session_var BEFORE refreshing the list so _refresh_session_list
        # recognises the new session and doesn't fall back to a previous one.
        folder_name = os.path.basename(path)
        self.session_var.set(folder_name)
        self._refresh_session_list()
        
        self._clear_all()
        self.status_var.set(f"Session '{name}' created → {path}")

    def _save_session(self):
        if not self.session_mgr.get_session_path():
            messagebox.showinfo("Save", "Create a session first (🆕 New).")
            return
        draft = {
            "session_name":   self.session_var.get(),
            "template_type":  self.current_template,
            "content": {
                "topic_bed": self.topic_input.get_text(), 
                "tag_lines": self.tag_input.get_lines(), 
                "white_bed": self.white_input.get_text(),
                "topic_bed_raw": self.topic_input.get_raw_text(),
                "tag_lines_raw": self.tag_input.get_raw_text(),
                "white_bed_raw": self.white_input.get_raw_text(),
            },
            "adjustments": self.adjustments,
        }
        self.session_mgr.save_draft(draft)
        self.status_var.set(f"Saved at {datetime.datetime.now().strftime('%H:%M:%S')}")

    def _refresh_session_list(self):
        sessions = self.session_mgr.list_sessions()
        self.session_combo['values'] = sessions
        current_session = self.session_var.get()
        if current_session in sessions:
            pass
        elif sessions:
            self.session_combo.current(0)
            self._on_session_selected()
        else:
            self.session_var.set("")

    def _open_folder(self):
        path = self.session_mgr.get_session_path()
        if not path: path = self.session_mgr.base_dir
        if path and os.path.exists(path): os.startfile(path)
        else: messagebox.showinfo("Folder", f"Path does not exist yet:\n{path}")

    def _open_settings(self):
        dlg = SettingsDialog(self, self.settings_mgr, self.template_mgr)
        self.wait_window(dlg)
        if dlg.result:
            self.validator = TextValidator(self.settings_mgr.settings)
            self._refresh_session_list()
            self.status_var.set("Settings saved")
            self.schedule_preview_update()

    def _clear_all(self):
        self.topic_input.set_text("")
        self.tag_input.set_text("")
        self.white_input.set_text("")
        self.reset_scaling()
        self.gen_panel.update_tag_lines([])
        self.schedule_preview_update()

    def _setup_auto_save(self):
        interval_s = self.settings_mgr.get("session", "auto_save_interval_seconds", 60)
        self.after(int(interval_s) * 1000, self._auto_save)

    def _auto_save(self):
        if self.session_mgr.get_session_path() and self.session_mgr.unsaved_changes:
            self._save_session()
            self.status_var.set(f"Auto-saved at {datetime.datetime.now().strftime('%H:%M:%S')}")
        self._setup_auto_save()

    def _setup_shortcuts(self):
        self.bind('<Control-n>',      lambda e: self._new_session())
        self.bind('<Control-s>',      lambda e: self._save_session())
        self.bind('<Control-o>',      lambda e: self._open_folder())
        self.bind('<Control-comma>',  lambda e: self._open_settings())
        self.bind('<Control-Delete>', lambda e: self._clear_all())
        self.bind('<F5>',             lambda e: self.schedule_preview_update())
