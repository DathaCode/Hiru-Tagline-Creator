import tkinter as tk


class ToolTip:
    """Lightweight hover tooltip for any Tkinter widget."""

    def __init__(self, widget, text, delay=400):
        self.widget = widget
        self.text   = text
        self.delay  = delay
        self._id    = None
        self._tw    = None

        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _schedule(self, _event):
        self._id = self.widget.after(self.delay, self._show)

    def _show(self):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self._tw = tk.Toplevel(self.widget)
        self._tw.wm_overrideredirect(True)
        self._tw.wm_geometry(f"+{x}+{y}")
        lbl = tk.Label(
            self._tw, text=self.text,
            background="#ffffe1", relief=tk.SOLID, borderwidth=1,
            font=("Arial", 9), padx=6, pady=3,
        )
        lbl.pack()

    def _hide(self, _event=None):
        if self._id:
            self.widget.after_cancel(self._id)
            self._id = None
        if self._tw:
            self._tw.destroy()
            self._tw = None


def add_tooltip(widget, text):
    """Convenience function."""
    return ToolTip(widget, text)
