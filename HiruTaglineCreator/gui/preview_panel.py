import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

class PreviewPanel(ttk.Frame):
    """
    Live preview panel with template rendering and text overlay.
    """
    def __init__(self, parent, template_mgr):
        super().__init__(parent)
        
        self.template_mgr = template_mgr
        self.zoom_level = "Fit"
        self.selected_tag_index = 0
        self.current_preview_img = None
        self.photo_img = None
        self.on_tag_select_callback = None  # Set by MainWindow after build
        
        # Tools Frame (Zoom, Tag Selector)
        tools_frame = ttk.Frame(self)
        tools_frame.pack(anchor=tk.W, pady=5, fill=tk.X)
        
        ttk.Label(tools_frame, text="Zoom:").pack(side=tk.LEFT)
        self.zoom_var = tk.StringVar(value="Fit")
        zoom_combo = ttk.Combobox(
            tools_frame,
            textvariable=self.zoom_var,
            values=["Fit", "50%", "75%", "100%"],
            state="readonly",
            width=10
        )
        zoom_combo.pack(side=tk.LEFT, padx=(5, 15))
        zoom_combo.bind('<<ComboboxSelected>>', self.on_zoom_change)
        
        ttk.Label(tools_frame, text="Selected TAG:").pack(side=tk.LEFT)
        self.tag_selector = ttk.Combobox(tools_frame, state="readonly", width=15)
        self.tag_selector.pack(side=tk.LEFT, padx=5)
        self.tag_selector.bind('<<ComboboxSelected>>', self.on_tag_select)
        
        # Warning label
        self.warning_label = ttk.Label(
            self,
            text="",
            foreground="red",
            font=("Arial", 10, "bold")
        )
        self.warning_label.pack(anchor=tk.W, pady=(0, 5))

        # Canvas for preview display
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.h_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
        self.v_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg='black', 
                              xscrollcommand=self.h_scroll.set, 
                              yscrollcommand=self.v_scroll.set)
                              
        self.h_scroll.config(command=self.canvas.xview)
        self.v_scroll.config(command=self.canvas.yview)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        
        self.canvas.bind('<Configure>', self.on_canvas_resize)
        
        self.last_render_args = None

    def on_zoom_change(self, event):
        self.zoom_level = self.zoom_var.get()
        if self.current_preview_img:
            self.display_image(self.current_preview_img)

    def on_tag_select(self, event):
        self.selected_tag_index = self.tag_selector.current()
        # Trigger re-render via MainWindow callback
        if self.on_tag_select_callback:
            self.on_tag_select_callback()
            
    def on_canvas_resize(self, event):
        if self.zoom_level == "Fit" and self.current_preview_img:
            self.display_image(self.current_preview_img)

    def load_template(self, template_type):
        """Loads the base template image so MainWindow can composite text on it."""
        self.template_image = self.template_mgr.get_template_image(template_type)

    def display_preview_image(self, img):
        """Called by MainWindow with the fully composited image (Template + Texts)"""
        self.current_preview_img = img
        self.display_image(img)

    def display_image(self, img):
        if not img: return
        w, h = img.size
        
        if self.zoom_level == "Fit":
            cw = self.canvas.winfo_width()
            ch = self.canvas.winfo_height()
            
            if cw > 10 and ch > 10:
                scale = min(cw / w, ch / h)
                new_w = max(1, int(w * scale))
                new_h = max(1, int(h * scale))
                try:
                    resampling = Image.Resampling.LANCZOS
                except AttributeError:
                    resampling = Image.LANCZOS
                img = img.resize((new_w, new_h), resampling)
        else:
            scale_map = {"50%": 0.5, "75%": 0.75, "100%": 1.0}
            scale = scale_map.get(self.zoom_level, 1.0)
            if scale != 1.0:
                new_w = max(1, int(w * scale))
                new_h = max(1, int(h * scale))
                try:
                    resampling = Image.Resampling.LANCZOS
                except AttributeError:
                    resampling = Image.LANCZOS
                img = img.resize((new_w, new_h), resampling)
                
        self.photo_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        # Center in canvas if smaller
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        
        img_w = self.photo_img.width()
        img_h = self.photo_img.height()
        
        x_pos = max(0, (cw - img_w) // 2)
        y_pos = max(0, (ch - img_h) // 2)
        
        self.canvas.create_image(x_pos, y_pos, anchor=tk.NW, image=self.photo_img)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def update_tag_selector(self, tag_lines):
        if not tag_lines:
            self.tag_selector['values'] = []
            self.tag_selector.set('')
            self.selected_tag_index = 0
            return
            
        values = [f"Line {i+1}" for i in range(len(tag_lines))]
        self.tag_selector['values'] = values
        
        if self.selected_tag_index >= len(tag_lines):
            self.selected_tag_index = max(0, len(tag_lines) - 1)
            
        self.tag_selector.current(self.selected_tag_index)

    def check_warnings(self, tag_lines, white_text):
        warnings = []
        
        for i, line in enumerate(tag_lines):
            word_count = len(line.split())
            if word_count > 9:
                short_words = [w for w in line.split() if len(w) <= 3]
                if word_count > 13 or len(short_words) < 3:
                    warnings.append(f"Line {i+1} exceeds limit ({word_count} words)")
                    
        if white_text:
            word_count = len(white_text.split())
            if word_count > 9:
                warnings.append(f"White Bed exceeds limit ({word_count} words)")
                
        if warnings:
            self.warning_label.config(text="⚠️ " + " | ".join(warnings))
        else:
            self.warning_label.config(text="")
