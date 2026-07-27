"""
Dark Theme — HiruTaglineCreator v3.1
Matches the HiruNews AI Streamline UI palette exactly.

Color hierarchy (mirrors AI Streamline):
  BG_DARK  (#0d1117) — window, canvas, all bare frames  ← dominant base
  BG_CARD  (#161b22) — elevated panels (LabelFrames, buttons)
  BG_ROW   (#21262d) — hover states, table rows, alt backgrounds
  BG_INPUT (#0d1117) — text entry fields (same as base)
"""

import tkinter as tk
from tkinter import ttk

# ── Palette — exact match to HiruNews AI Streamline CSS variables ────────
# Source: award_submission_2026/04_ai_prototype/HiruNewsAIStreamline/frontend/styles.css
BG_DARK   = "#0A0A0B"   # --bg-primary   : near-pure black, neutral (no blue tint)
BG_CARD   = "#131316"   # --bg-secondary : very dark charcoal
BG_ROW    = "#1C1C21"   # --bg-tertiary  : elevated panels / hover states
BG_INPUT  = "#131316"   # same as BG_CARD — inputs are elevated from base
FG_TEXT   = "#F5F5F7"   # --text-primary
FG_MUTED  = "#A1A1AA"   # --text-secondary
ACCENT    = "#a70003"   # Hiru red (broadcast brand — MAIN TAG / LabelFrame headers)
GOLD      = "#d4a017"   # gold accent
BORDER    = "#27272F"   # --border
SUCCESS   = "#10B981"   # --success
WARNING   = "#F59E0B"   # --warning


def apply_dark_theme(root: tk.Tk) -> None:
    """
    Call this as the VERY FIRST thing inside MainWindow.__init__(),
    before _build_ui() is called.  Sets:
      1. Tk option database  → all future tk.Widget instances inherit dark defaults
      2. ttk.Style           → all ttk widgets styled dark
      3. root background     → window chrome
    """
    # ── 1. Tk option database ───────────────────────────────────────────
    # Base color is BG_DARK — so all frames/labels default to #0d1117
    root.option_add("*Background",         BG_DARK,  "startupFile")
    root.option_add("*Foreground",         FG_TEXT,  "startupFile")
    root.option_add("*activeBackground",   BG_ROW,   "startupFile")
    root.option_add("*activeForeground",   FG_TEXT,  "startupFile")
    root.option_add("*disabledForeground", FG_MUTED, "startupFile")
    root.option_add("*highlightBackground", BG_DARK, "startupFile")
    root.option_add("*highlightColor",     BORDER,   "startupFile")

    # Input widgets — BG_ROW so they stand out clearly against BG_DARK
    root.option_add("*Entry.Background",          BG_ROW,    "startupFile")
    root.option_add("*Entry.Foreground",          FG_TEXT,   "startupFile")
    root.option_add("*Entry.insertBackground",    FG_TEXT,   "startupFile")
    root.option_add("*Entry.selectBackground",    ACCENT,    "startupFile")
    root.option_add("*Entry.selectForeground",    "#ffffff",  "startupFile")
    root.option_add("*Entry.relief",              "flat",    "startupFile")
    root.option_add("*Entry.highlightThickness",  "1",       "startupFile")
    root.option_add("*Entry.highlightBackground", BORDER,    "startupFile")

    root.option_add("*Text.Background",           BG_ROW,    "startupFile")
    root.option_add("*Text.Foreground",           FG_TEXT,   "startupFile")
    root.option_add("*Text.insertBackground",     FG_TEXT,   "startupFile")
    root.option_add("*Text.selectBackground",     ACCENT,    "startupFile")
    root.option_add("*Text.selectForeground",     "#ffffff",  "startupFile")
    root.option_add("*Text.relief",               "flat",    "startupFile")
    root.option_add("*Text.highlightThickness",   "1",       "startupFile")
    root.option_add("*Text.highlightBackground",  BORDER,    "startupFile")

    root.option_add("*Canvas.Background",        BG_DARK,   "startupFile")
    root.option_add("*Canvas.highlightThickness","0",       "startupFile")

    root.option_add("*Listbox.Background",       BG_CARD,   "startupFile")
    root.option_add("*Listbox.Foreground",       FG_TEXT,   "startupFile")
    root.option_add("*Listbox.selectBackground", ACCENT,    "startupFile")
    root.option_add("*Listbox.selectForeground", "#ffffff",  "startupFile")
    root.option_add("*Listbox.relief",           "flat",    "startupFile")

    root.option_add("*Scrollbar.Background",     BG_DARK,   "startupFile")
    root.option_add("*Scrollbar.troughColor",    BG_DARK,   "startupFile")
    root.option_add("*Scrollbar.relief",         "flat",    "startupFile")

    root.option_add("*Menu.Background",          BG_CARD,   "startupFile")
    root.option_add("*Menu.Foreground",          FG_TEXT,   "startupFile")
    root.option_add("*Menu.activeBackground",    ACCENT,    "startupFile")
    root.option_add("*Menu.activeForeground",    "#ffffff",  "startupFile")
    root.option_add("*Menu.relief",              "flat",    "startupFile")

    # ── 2. Window background ────────────────────────────────────────────
    root.configure(bg=BG_DARK)

    # ── 3. ttk.Style ────────────────────────────────────────────────────
    style = ttk.Style(root)
    style.theme_use("clam")

    # TFrame — uses BG_DARK so bare frames are invisible against window bg
    style.configure("TFrame",
                    background=BG_DARK)
    style.configure("Card.TFrame",
                    background=BG_CARD)

    # TLabel — BG_DARK base so labels sit on the dark background
    style.configure("TLabel",
                    background=BG_DARK,
                    foreground=FG_TEXT)
    style.configure("Muted.TLabel",
                    background=BG_DARK,
                    foreground=FG_MUTED)
    style.configure("Card.TLabel",
                    background=BG_CARD,
                    foreground=FG_TEXT)

    # TButton — BG_CARD base so buttons are slightly elevated from BG_DARK
    style.configure("TButton",
                    background=BG_CARD,
                    foreground=FG_TEXT,
                    bordercolor=BORDER,
                    darkcolor=BG_CARD,
                    lightcolor=BG_CARD,
                    relief="flat",
                    padding=(8, 4),
                    focusthickness=0,
                    focuscolor=BG_CARD)
    style.map("TButton",
              background=[("active", BG_ROW), ("pressed", ACCENT)],
              foreground=[("active", FG_TEXT), ("pressed", "#ffffff")],
              relief=[("pressed", "flat")])

    # TEntry
    style.configure("TEntry",
                    fieldbackground=BG_ROW,
                    foreground=FG_TEXT,
                    insertcolor=FG_TEXT,
                    bordercolor=BORDER,
                    lightcolor=BORDER,
                    darkcolor=BORDER,
                    relief="flat")
    style.map("TEntry",
              fieldbackground=[("readonly", BG_CARD)],
              foreground=[("readonly", FG_MUTED)])

    # TNotebook — dark background, red active tab
    style.configure("TNotebook",
                    background=BG_DARK,
                    borderwidth=0,
                    tabmargins=[0, 0, 0, 0])
    style.configure("TNotebook.Tab",
                    background=BG_CARD,
                    foreground=FG_MUTED,
                    padding=(12, 5),
                    borderwidth=0,
                    focuscolor=BG_CARD)
    style.map("TNotebook.Tab",
              background=[("selected", ACCENT), ("active", BG_ROW)],
              foreground=[("selected", "#ffffff"), ("active", FG_TEXT)],
              expand=[("selected", [1, 1, 1, 0])])

    # TLabelframe — BG_CARD so panels appear as elevated "cards" on dark bg
    style.configure("TLabelframe",
                    background=BG_CARD,
                    bordercolor=BORDER,
                    relief="groove",
                    borderwidth=1)
    style.configure("TLabelframe.Label",
                    background=BG_CARD,
                    foreground=FG_MUTED,
                    font=("Arial", 9, "bold"))

    # TScrollbar
    style.configure("TScrollbar",
                    background=BG_DARK,
                    troughcolor=BG_DARK,
                    bordercolor=BG_DARK,
                    arrowcolor=BORDER,
                    relief="flat",
                    arrowsize=12)
    style.map("TScrollbar",
              background=[("active", BG_ROW), ("pressed", ACCENT)],
              arrowcolor=[("active", FG_MUTED)])

    # TCombobox
    style.configure("TCombobox",
                    fieldbackground=BG_CARD,
                    background=BG_CARD,
                    foreground=FG_TEXT,
                    selectbackground=ACCENT,
                    selectforeground="#ffffff",
                    bordercolor=BORDER,
                    arrowcolor=FG_MUTED,
                    relief="flat",
                    insertcolor=FG_TEXT)
    style.map("TCombobox",
              fieldbackground=[("readonly", BG_CARD), ("disabled", BG_DARK)],
              foreground=[("readonly", FG_TEXT), ("disabled", FG_MUTED)],
              background=[("active", BG_ROW)],
              arrowcolor=[("active", FG_TEXT)])
    root.option_add("*TCombobox*Listbox.Background",       BG_CARD,  "startupFile")
    root.option_add("*TCombobox*Listbox.Foreground",       FG_TEXT,  "startupFile")
    root.option_add("*TCombobox*Listbox.selectBackground", ACCENT,   "startupFile")
    root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff", "startupFile")

    # TProgressbar
    style.configure("TProgressbar",
                    background=ACCENT,
                    troughcolor=BG_ROW,
                    bordercolor=BG_DARK,
                    lightcolor=ACCENT,
                    darkcolor=ACCENT,
                    thickness=6)

    # TScale
    style.configure("Horizontal.TScale",
                    background=BG_DARK,
                    troughcolor=BG_ROW,
                    sliderlength=18,
                    sliderrelief="flat",
                    bordercolor=BORDER)
    style.map("Horizontal.TScale",
              background=[("active", ACCENT)])

    # TCheckbutton — BG_DARK base so checkboxes sit on dark background
    style.configure("TCheckbutton",
                    background=BG_DARK,
                    foreground=FG_TEXT,
                    focuscolor=BG_DARK,
                    indicatorcolor=BG_CARD,
                    indicatorrelief="flat")
    style.map("TCheckbutton",
              background=[("active", BG_DARK)],
              foreground=[("active", FG_TEXT)],
              indicatorcolor=[("selected", ACCENT), ("active", BG_ROW)])

    # TRadiobutton
    style.configure("TRadiobutton",
                    background=BG_DARK,
                    foreground=FG_TEXT,
                    focuscolor=BG_DARK,
                    indicatorcolor=BG_CARD)
    style.map("TRadiobutton",
              background=[("active", BG_DARK)],
              foreground=[("active", FG_TEXT)],
              indicatorcolor=[("selected", ACCENT)])

    # TSeparator
    style.configure("TSeparator",
                    background=BORDER)

    # TPanedwindow
    style.configure("TPanedwindow",
                    background=BG_DARK)
    style.configure("Sash",
                    background=BORDER,
                    sashthickness=4)


def patch_widget_colors(widget) -> None:
    """
    Recursively walk a widget tree and force dark colors on raw tk widgets
    that ignore ttk.Style (tk.Text, tk.Entry, tk.Canvas, tk.Listbox, tk.Label).
    Call this AFTER the UI is fully built.
    """
    try:
        wclass = widget.winfo_class()
        if wclass == "Text":
            widget.configure(
                bg=BG_ROW, fg=FG_TEXT,
                insertbackground=FG_TEXT,
                selectbackground=ACCENT,
                selectforeground="#ffffff",
                relief="flat",
                highlightthickness=1,
                highlightbackground=BORDER,
                highlightcolor=ACCENT
            )
        elif wclass == "Entry":
            widget.configure(
                bg=BG_ROW, fg=FG_TEXT,
                insertbackground=FG_TEXT,
                selectbackground=ACCENT,
                selectforeground="#ffffff",
                relief="flat",
                highlightthickness=1,
                highlightbackground=BORDER,
                highlightcolor=ACCENT
            )
        elif wclass == "Canvas":
            widget.configure(bg=BG_DARK, highlightthickness=0)
        elif wclass == "Listbox":
            widget.configure(
                bg=BG_CARD, fg=FG_TEXT,
                selectbackground=ACCENT,
                selectforeground="#ffffff",
                relief="flat"
            )
        elif wclass == "Label":
            # raw tk.Label — override light defaults
            try:
                widget.configure(bg=BG_DARK, fg=FG_TEXT)
            except Exception:
                pass
        elif wclass == "Frame":
            # raw tk.Frame
            try:
                widget.configure(bg=BG_DARK)
            except Exception:
                pass
    except Exception:
        pass
    for child in widget.winfo_children():
        patch_widget_colors(child)
