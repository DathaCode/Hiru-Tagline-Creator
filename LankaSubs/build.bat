@echo off
REM ===== LankaSubs: build the Windows .exe =====
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 goto nopython

if not exist .venv python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller
if errorlevel 1 goto failed

if exist bin\ffmpeg.exe goto build
echo Downloading FFmpeg (gyan.dev essentials build)...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile ffmpeg.zip; Expand-Archive ffmpeg.zip -DestinationPath ffmpeg_tmp -Force; New-Item -ItemType Directory -Force bin | Out-Null; Get-ChildItem ffmpeg_tmp -Recurse -Filter ffmpeg.exe | Select-Object -First 1 | Copy-Item -Destination bin\ffmpeg.exe; Remove-Item ffmpeg.zip; Remove-Item ffmpeg_tmp -Recurse -Force"
if not exist bin\ffmpeg.exe goto noffmpeg

:build
pyinstaller --noconfirm --clean --windowed --name LankaSubs --add-data "fonts;fonts" main.py
if errorlevel 1 goto failed
xcopy /E /I /Y bin dist\LankaSubs\bin >nul
echo.
echo ==========================================================
echo  DONE!  Your app is in:  dist\LankaSubs\LankaSubs.exe
echo  Zip the whole dist\LankaSubs folder to share with your team.
echo ==========================================================
pause
exit /b 0

:nopython
echo Python was not found. Install Python 3.11+ from python.org
echo and tick "Add python.exe to PATH" during setup, then run this again.
pause
exit /b 1

:noffmpeg
echo Could not download FFmpeg automatically.
echo Download "ffmpeg-release-essentials.zip" from https://www.gyan.dev/ffmpeg/builds/
echo and copy ffmpeg.exe (from its bin folder) into this project's "bin" folder.
pause
exit /b 1

:failed
echo Build failed - see the messages above.
pause
exit /b 1
