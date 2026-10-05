"""
Build Windows executable — HiruTaglineCreator v3.1 (Dark Theme)
Run: py -3 build_exe.py
"""
import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--icon=assets/app_icon.ico',
    '--name=HiruTaglineCreator_v3.1',
    '--add-data=templates;templates',
    '--add-data=assets;assets',
    '--add-data=config;config',
    '--hidden-import=PIL',
    '--hidden-import=PIL._tkinter_finder',
    '--clean',
    '--noconfirm',
])
