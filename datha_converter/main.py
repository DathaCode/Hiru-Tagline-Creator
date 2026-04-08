"""
Datha Converter v1.0
Standalone Sinhala Text Converter

Conversion modes:
  1. Singlish → Sinhala Unicode
  2. Sinhala Unicode → FM ASCII
  3. Singlish → FM ASCII (chained)
"""
import sys
import os

# Ensure the package root is on the path when running from exe or directly
if getattr(sys, 'frozen', False):
    _base = sys._MEIPASS
else:
    _base = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _base)

from gui.app import DathaConverterApp

if __name__ == '__main__':
    app = DathaConverterApp()
    app.mainloop()
