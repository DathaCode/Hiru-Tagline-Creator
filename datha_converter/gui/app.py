"""
Datha Converter – Modern Dark-themed GUI
═════════════════════════════════════════
A standalone Sinhala text converter with three conversion modes:
  1. Singlish  →  Sinhala Unicode
  2. Sinhala Unicode  →  FM ASCII
  3. Singlish  →  FM ASCII (chained)

Built with tkinter + custom dark theme for a premium look.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time

from converter.singlish_to_sinhala import convert_singlish_to_sinhala
from converter.unicode_to_fm import convert_unicode_to_fm


# ═══════════════════════════════════════════════════════════════════
# Colour palette
# ═══════════════════════════════════════════════════════════════════
_COLORS = {
    "bg_dark":       "#0f1117",
    "bg_panel":      "#181b24",
    "bg_card":       "#1e2230",
    "bg_input":      "#252a3a",
    "bg_output":     "#1a1e2c",
    "border":        "#2d3348",
    "border_focus":  "#6c63ff",
    "text":          "#e4e6ef",
    "text_dim":      "#8b8fa8",
    "text_label":    "#b0b4cc",
    "accent":        "#6c63ff",
    "accent_hover":  "#7f78ff",
    "accent_active": "#5a52e0",
    "green":         "#4ade80",
    "green_dim":     "#22c55e",
    "orange":        "#fb923c",
    "red":           "#f87171",
    "cyan":          "#22d3ee",
    "header_grad_1": "#6c63ff",
    "header_grad_2": "#a78bfa",
    "mode_bg":       "#252a3a",
    "mode_selected": "#6c63ff",
    "copy_btn":      "#22c55e",
    "copy_hover":    "#16a34a",
    "clear_btn":     "#334155",
    "clear_hover":   "#475569",
    "swap_btn":      "#0ea5e9",
    "swap_hover":    "#0284c7",
    "scrollbar":     "#3b4066",
    "scrollbar_thumb": "#5a5f8a",
}


class DathaConverterApp(tk.Tk):
    """
    Main application window with a custom dark theme.
    """

    def __init__(self):
        super().__init__()

        self.title("⚡ Datha Converter — Sinhala Text Tools")
        self.geometry("1060x780")
        self.minsize(760, 620)
        self.configure(bg=_COLORS["bg_dark"])

        # Conversion mode: 0 = Singlish→Unicode, 1 = Unicode→FM, 2 = Singlish→FM
        self._mode = tk.IntVar(value=0)
        self._debounce_id = None

        self._apply_theme()
        self._build_ui()

        # Initial conversion trigger
        self.after(100, self._on_input_change)

    # ─────────────────────────────────────────────────────────────
    # Theme / ttk styling
    # ─────────────────────────────────────────────────────────────
    def _apply_theme(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Frame
        style.configure("Dark.TFrame", background=_COLORS["bg_dark"])
        style.configure("Card.TFrame", background=_COLORS["bg_card"])
        style.configure("Panel.TFrame", background=_COLORS["bg_panel"])

        # Label
        style.configure("Dark.TLabel",
                         background=_COLORS["bg_dark"],
                         foreground=_COLORS["text"],
                         font=("Segoe UI", 10))
        style.configure("Dim.TLabel",
                         background=_COLORS["bg_dark"],
                         foreground=_COLORS["text_dim"],
                         font=("Segoe UI", 9))
        style.configure("Card.TLabel",
                         background=_COLORS["bg_card"],
                         foreground=_COLORS["text"],
                         font=("Segoe UI", 10))
        style.configure("CardDim.TLabel",
                         background=_COLORS["bg_card"],
                         foreground=_COLORS["text_dim"],
                         font=("Segoe UI", 9))
        style.configure("Header.TLabel",
                         background=_COLORS["bg_dark"],
                         foreground=_COLORS["accent"],
                         font=("Segoe UI Semibold", 20))
        style.configure("SubHeader.TLabel",
                         background=_COLORS["bg_dark"],
                         foreground=_COLORS["text_dim"],
                         font=("Segoe UI", 10))

        # Radiobutton (for mode selector)
        style.configure("Mode.TRadiobutton",
                         background=_COLORS["bg_card"],
                         foreground=_COLORS["text"],
                         font=("Segoe UI", 10),
                         indicatorrelief="flat",
                         padding=(12, 8))
        style.map("Mode.TRadiobutton",
                   background=[("selected", _COLORS["mode_selected"]),
                               ("active", _COLORS["border"])],
                   foreground=[("selected", "#ffffff")])

    # ─────────────────────────────────────────────────────────────
    # Build UI
    # ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Root container
        root_frame = ttk.Frame(self, style="Dark.TFrame")
        root_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # ── Header ──────────────────────────────────────────────
        self._build_header(root_frame)

        # ── Mode selector ───────────────────────────────────────
        self._build_mode_selector(root_frame)

        # ── Main content (input + output) ───────────────────────
        content = ttk.Frame(root_frame, style="Dark.TFrame")
        content.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 16))
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=0)  # middle controls
        content.columnconfigure(2, weight=1)
        content.rowconfigure(0, weight=1)

        self._build_input_panel(content)
        self._build_middle_controls(content)
        self._build_output_panel(content)

        # ── Status bar ──────────────────────────────────────────
        self._build_status_bar(root_frame)

    # ── Header ──────────────────────────────────────────────────
    def _build_header(self, parent):
        hdr = ttk.Frame(parent, style="Dark.TFrame")
        hdr.pack(fill=tk.X, padx=24, pady=(20, 6))

        # Title row
        title_row = ttk.Frame(hdr, style="Dark.TFrame")
        title_row.pack(fill=tk.X)

        ttk.Label(title_row, text="⚡", style="Header.TLabel",
                  font=("Segoe UI Emoji", 22)).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Label(title_row, text="Datha Converter", style="Header.TLabel").pack(side=tk.LEFT)

        # version badge
        ver = tk.Label(title_row, text=" v1.0 ", bg=_COLORS["accent"],
                       fg="#ffffff", font=("Segoe UI Semibold", 8),
                       padx=6, pady=1)
        ver.pack(side=tk.LEFT, padx=(10, 0), pady=(6, 0))

        ttk.Label(hdr,
                  text="Singlish ↔ Sinhala Unicode ↔ FM ASCII  •  Real-time conversion",
                  style="SubHeader.TLabel").pack(anchor=tk.W, pady=(2, 0))

        # Separator line (accent gradient simulation)
        sep = tk.Frame(hdr, height=2, bg=_COLORS["accent"])
        sep.pack(fill=tk.X, pady=(10, 0))

    # ── Mode selector ───────────────────────────────────────────
    def _build_mode_selector(self, parent):
        outer = ttk.Frame(parent, style="Dark.TFrame")
        outer.pack(fill=tk.X, padx=24, pady=(12, 12))

        ttk.Label(outer, text="CONVERSION MODE",
                  style="Dim.TLabel",
                  font=("Segoe UI Semibold", 9)).pack(anchor=tk.W, pady=(0, 6))

        card = tk.Frame(outer, bg=_COLORS["bg_card"],
                        highlightbackground=_COLORS["border"],
                        highlightthickness=1, bd=0)
        card.pack(fill=tk.X)

        modes = [
            ("⌨  Singlish  →  Sinhala Unicode", 0),
            ("🔤  Sinhala Unicode  →  FM ASCII", 1),
            ("⚡  Singlish  →  FM ASCII (chained)", 2),
        ]

        self._mode_btns = []
        for i, (label, val) in enumerate(modes):
            btn = tk.Label(
                card, text=label,
                bg=_COLORS["bg_card"],
                fg=_COLORS["text"],
                font=("Segoe UI", 10),
                padx=18, pady=10,
                cursor="hand2",
                anchor="w",
            )
            btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            btn.bind("<Button-1>", lambda e, v=val: self._select_mode(v))
            btn.bind("<Enter>", lambda e, b=btn: self._mode_hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self._mode_hover(b, False))
            self._mode_btns.append(btn)

        self._highlight_mode(0)

    def _select_mode(self, mode_val):
        self._mode.set(mode_val)
        self._highlight_mode(mode_val)
        self._update_labels()
        self._on_input_change()

    def _highlight_mode(self, active):
        for i, btn in enumerate(self._mode_btns):
            if i == active:
                btn.configure(bg=_COLORS["mode_selected"], fg="#ffffff",
                              font=("Segoe UI Semibold", 10))
            else:
                btn.configure(bg=_COLORS["bg_card"], fg=_COLORS["text"],
                              font=("Segoe UI", 10))

    def _mode_hover(self, btn, entering):
        idx = self._mode_btns.index(btn)
        if idx == self._mode.get():
            return
        if entering:
            btn.configure(bg=_COLORS["border"])
        else:
            btn.configure(bg=_COLORS["bg_card"])

    # ── Input panel ─────────────────────────────────────────────
    def _build_input_panel(self, parent):
        frame = tk.Frame(parent, bg=_COLORS["bg_card"],
                         highlightbackground=_COLORS["border"],
                         highlightthickness=1, bd=0)
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Header row
        hdr = tk.Frame(frame, bg=_COLORS["bg_card"])
        hdr.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 4))

        self._input_label = tk.Label(
            hdr, text="📥  INPUT — Singlish",
            bg=_COLORS["bg_card"], fg=_COLORS["cyan"],
            font=("Segoe UI Semibold", 11), anchor="w"
        )
        self._input_label.pack(side=tk.LEFT)

        self._char_count_in = tk.Label(
            hdr, text="0 chars",
            bg=_COLORS["bg_card"], fg=_COLORS["text_dim"],
            font=("Segoe UI", 9)
        )
        self._char_count_in.pack(side=tk.RIGHT)

        # Text widget
        self.input_text = tk.Text(
            frame, wrap=tk.WORD,
            bg=_COLORS["bg_input"], fg=_COLORS["text"],
            insertbackground=_COLORS["accent"],
            selectbackground=_COLORS["accent"],
            selectforeground="#ffffff",
            font=("Iskoola Pota", 13),
            relief="flat", bd=0,
            padx=14, pady=10,
            undo=True,
        )
        self.input_text.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 6))
        self.input_text.bind("<KeyRelease>", self._debounced_change)
        self.input_text.bind("<Control-a>", self._select_all_input)

        # Placeholder
        self._show_placeholder(self.input_text, "Type Singlish or paste Sinhala Unicode here...")

        # Bottom actions
        btn_row = tk.Frame(frame, bg=_COLORS["bg_card"])
        btn_row.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

        self._make_btn(btn_row, "🗑  Clear", _COLORS["clear_btn"], _COLORS["clear_hover"],
                       self._clear_input).pack(side=tk.LEFT)
        self._make_btn(btn_row, "📋  Paste", _COLORS["clear_btn"], _COLORS["clear_hover"],
                       self._paste_input).pack(side=tk.LEFT, padx=(6, 0))

    # ── Middle controls (swap / convert arrow) ──────────────────
    def _build_middle_controls(self, parent):
        mid = tk.Frame(parent, bg=_COLORS["bg_dark"], width=56)
        mid.grid(row=0, column=1, sticky="ns", padx=4)
        mid.columnconfigure(0, weight=1)

        spacer = tk.Frame(mid, bg=_COLORS["bg_dark"])
        spacer.pack(expand=True)

        # Convert arrow
        arrow_btn = tk.Label(
            mid, text="→",
            bg=_COLORS["accent"], fg="#ffffff",
            font=("Segoe UI", 18, "bold"),
            width=3, height=1,
            cursor="hand2",
            relief="flat",
        )
        arrow_btn.pack(pady=(0, 8))
        arrow_btn.bind("<Button-1>", lambda e: self._on_input_change())
        arrow_btn.bind("<Enter>", lambda e: arrow_btn.configure(bg=_COLORS["accent_hover"]))
        arrow_btn.bind("<Leave>", lambda e: arrow_btn.configure(bg=_COLORS["accent"]))

        # Swap button
        swap_btn = tk.Label(
            mid, text="⇄",
            bg=_COLORS["swap_btn"], fg="#ffffff",
            font=("Segoe UI", 14),
            width=3, height=1,
            cursor="hand2",
            relief="flat",
        )
        swap_btn.pack(pady=(0, 0))
        swap_btn.bind("<Button-1>", lambda e: self._swap_panels())
        swap_btn.bind("<Enter>", lambda e: swap_btn.configure(bg=_COLORS["swap_hover"]))
        swap_btn.bind("<Leave>", lambda e: swap_btn.configure(bg=_COLORS["swap_btn"]))

        spacer2 = tk.Frame(mid, bg=_COLORS["bg_dark"])
        spacer2.pack(expand=True)

    # ── Output panel ────────────────────────────────────────────
    def _build_output_panel(self, parent):
        frame = tk.Frame(parent, bg=_COLORS["bg_card"],
                         highlightbackground=_COLORS["border"],
                         highlightthickness=1, bd=0)
        frame.grid(row=0, column=2, sticky="nsew", padx=(6, 0))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Header row
        hdr = tk.Frame(frame, bg=_COLORS["bg_card"])
        hdr.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 4))

        self._output_label = tk.Label(
            hdr, text="📤  OUTPUT — Sinhala Unicode",
            bg=_COLORS["bg_card"], fg=_COLORS["green"],
            font=("Segoe UI Semibold", 11), anchor="w"
        )
        self._output_label.pack(side=tk.LEFT)

        self._char_count_out = tk.Label(
            hdr, text="0 chars",
            bg=_COLORS["bg_card"], fg=_COLORS["text_dim"],
            font=("Segoe UI", 9)
        )
        self._char_count_out.pack(side=tk.RIGHT)

        # Output text widget
        self.output_text = tk.Text(
            frame, wrap=tk.WORD,
            bg=_COLORS["bg_output"], fg=_COLORS["green"],
            insertbackground=_COLORS["green"],
            selectbackground=_COLORS["green_dim"],
            selectforeground="#ffffff",
            font=("Iskoola Pota", 13),
            relief="flat", bd=0,
            padx=14, pady=10,
            state=tk.DISABLED,
        )
        self.output_text.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 6))

        # Bottom actions
        btn_row = tk.Frame(frame, bg=_COLORS["bg_card"])
        btn_row.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

        self._copy_btn = self._make_btn(
            btn_row, "📋  Copy to Clipboard",
            _COLORS["copy_btn"], _COLORS["copy_hover"],
            self._copy_output
        )
        self._copy_btn.pack(side=tk.LEFT)

    # ── Status bar ──────────────────────────────────────────────
    def _build_status_bar(self, parent):
        bar = tk.Frame(parent, bg=_COLORS["bg_panel"], height=30)
        bar.pack(fill=tk.X, side=tk.BOTTOM)

        self._status_label = tk.Label(
            bar, text="Ready",
            bg=_COLORS["bg_panel"], fg=_COLORS["text_dim"],
            font=("Segoe UI", 9), anchor="w", padx=16
        )
        self._status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        mode_label = tk.Label(
            bar, text="Datha Converter v1.0  •  by DathaCode",
            bg=_COLORS["bg_panel"], fg=_COLORS["text_dim"],
            font=("Segoe UI", 9), padx=16
        )
        mode_label.pack(side=tk.RIGHT)

    # ─────────────────────────────────────────────────────────────
    # Helper: create a styled button (Label that looks like a btn)
    # ─────────────────────────────────────────────────────────────
    def _make_btn(self, parent, text, bg, hover_bg, command):
        btn = tk.Label(
            parent, text=text,
            bg=bg, fg="#ffffff",
            font=("Segoe UI Semibold", 9),
            padx=14, pady=6,
            cursor="hand2",
            relief="flat",
        )
        btn.bind("<Button-1>", lambda e: command())
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
        return btn

    # ─────────────────────────────────────────────────────────────
    # Placeholder logic
    # ─────────────────────────────────────────────────────────────
    def _show_placeholder(self, widget, text):
        widget._placeholder = text
        widget._has_placeholder = True
        widget.insert("1.0", text)
        widget.configure(fg=_COLORS["text_dim"])
        widget.bind("<FocusIn>", lambda e: self._clear_placeholder(widget))
        widget.bind("<FocusOut>", lambda e: self._restore_placeholder(widget))

    def _clear_placeholder(self, widget):
        if getattr(widget, '_has_placeholder', False):
            widget.delete("1.0", tk.END)
            widget.configure(fg=_COLORS["text"])
            widget._has_placeholder = False

    def _restore_placeholder(self, widget):
        content = widget.get("1.0", tk.END).strip()
        if not content:
            widget._has_placeholder = True
            widget.insert("1.0", widget._placeholder)
            widget.configure(fg=_COLORS["text_dim"])

    # ─────────────────────────────────────────────────────────────
    # Actions
    # ─────────────────────────────────────────────────────────────
    def _debounced_change(self, event=None):
        if self._debounce_id:
            self.after_cancel(self._debounce_id)
        self._debounce_id = self.after(80, self._on_input_change)

    def _on_input_change(self, event=None):
        if getattr(self.input_text, '_has_placeholder', False):
            self._set_output("")
            return

        raw = self.input_text.get("1.0", tk.END).rstrip("\n")
        mode = self._mode.get()

        # Update input char count
        count_in = len(raw)
        self._char_count_in.config(text=f"{count_in} chars")

        if not raw.strip():
            self._set_output("")
            self._status_label.config(text="Ready")
            self._char_count_out.config(text="0 chars")
            return

        t0 = time.perf_counter()
        try:
            if mode == 0:
                # Singlish → Sinhala Unicode
                result = self._convert_lines(raw, convert_singlish_to_sinhala)
            elif mode == 1:
                # Sinhala Unicode → FM ASCII
                result = self._convert_lines(raw, convert_unicode_to_fm)
            else:
                # Singlish → FM ASCII (chained)
                def chained(text):
                    return convert_unicode_to_fm(convert_singlish_to_sinhala(text))
                result = self._convert_lines(raw, chained)

            elapsed = (time.perf_counter() - t0) * 1000
            self._set_output(result)
            count_out = len(result)
            self._char_count_out.config(text=f"{count_out} chars")
            self._status_label.config(
                text=f"Converted {count_in} → {count_out} chars  •  {elapsed:.1f} ms"
            )
        except Exception as ex:
            self._set_output(f"[Error] {ex}")
            self._status_label.config(text=f"Error: {ex}")

    def _convert_lines(self, text, converter_fn):
        """Apply converter_fn line-by-line to preserve line breaks."""
        lines = text.split('\n')
        return '\n'.join(converter_fn(line) for line in lines)

    def _set_output(self, text):
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", text)
        self.output_text.configure(state=tk.DISABLED)

    def _copy_output(self):
        text = self.output_text.get("1.0", tk.END).strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self._status_label.config(text="✓ Copied to clipboard!")
            self._flash_btn(self._copy_btn, "✓  Copied!", _COLORS["accent"])

    def _flash_btn(self, btn, temp_text, temp_bg):
        """Briefly flash the button to give visual feedback."""
        orig_text = btn.cget("text")
        orig_bg = btn.cget("bg")
        btn.configure(text=temp_text, bg=temp_bg)
        self.after(1200, lambda: btn.configure(text=orig_text, bg=orig_bg))

    def _clear_input(self):
        self.input_text.delete("1.0", tk.END)
        self._on_input_change()
        self._restore_placeholder(self.input_text)
        self._status_label.config(text="Input cleared")

    def _paste_input(self):
        try:
            clip = self.clipboard_get()
            if clip:
                self._clear_placeholder(self.input_text)
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", clip)
                self._on_input_change()
                self._status_label.config(text="Pasted from clipboard")
        except tk.TclError:
            self._status_label.config(text="Clipboard is empty")

    def _swap_panels(self):
        """Move output text into input (useful for chaining conversions)."""
        out_text = self.output_text.get("1.0", tk.END).strip()
        if out_text:
            self._clear_placeholder(self.input_text)
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", out_text)
            self._on_input_change()
            self._status_label.config(text="Swapped output → input")

    def _select_all_input(self, event=None):
        self.input_text.tag_add(tk.SEL, "1.0", tk.END)
        return "break"

    def _update_labels(self):
        mode = self._mode.get()
        if mode == 0:
            self._input_label.config(text="📥  INPUT — Singlish")
            self._output_label.config(text="📤  OUTPUT — Sinhala Unicode")
        elif mode == 1:
            self._input_label.config(text="📥  INPUT — Sinhala Unicode")
            self._output_label.config(text="📤  OUTPUT — FM ASCII")
        else:
            self._input_label.config(text="📥  INPUT — Singlish")
            self._output_label.config(text="📤  OUTPUT — FM ASCII")
