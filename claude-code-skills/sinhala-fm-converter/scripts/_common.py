# -*- coding: utf-8 -*-
"""Shared helpers for the fm_converter check scripts."""
import importlib.util
import io
import os
import sys


def setup_stdout():
    """Windows consoles default to cp1252 and die on Sinhala. Force UTF-8."""
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith('utf'):
        return
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def converter_path():
    """Locate utils/fm_converter.py from the CWD or from this script's location."""
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.abspath(os.path.join(here, '..', '..', '..'))
    for p in (os.path.join(os.getcwd(), 'utils', 'fm_converter.py'),
              os.path.join(repo, 'HiruTaglineCreator', 'utils', 'fm_converter.py')):
        if os.path.isfile(p):
            return p
    raise SystemExit('fm_converter.py not found — run this from HiruTaglineCreator/')


def load(path, name='fmconv'):
    """Import a converter module by file path (works for .py and .bak copies)."""
    if not path.endswith('.py'):                      # e.g. fm_converter.py.bak
        import shutil
        import tempfile
        tmp = os.path.join(tempfile.gettempdir(), name + '.py')
        shutil.copyfile(path, tmp)
        path = tmp
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def leaks(fm_text):
    """Sinhala codepoints left in FM output — FM fonts have no glyph for these."""
    return [c for c in fm_text if 0x0D80 <= ord(c) <= 0x0DFF]
