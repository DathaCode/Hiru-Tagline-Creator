@echo off
REM Run LotusSubs from source (for testing changes without rebuilding the .exe)
cd /d "%~dp0"
if not exist .venv (python -m venv .venv & call .venv\Scripts\activate.bat & pip install -r requirements.txt) else call .venv\Scripts\activate.bat
python main.py
