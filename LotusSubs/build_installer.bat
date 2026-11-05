@echo off
REM ===== LotusSubs: build the Windows installer (run build.bat first) =====
setlocal
cd /d "%~dp0"

if not exist dist\LotusSubs\LotusSubs.exe goto nobuild
if not exist dist\LotusSubs\_internal\python314.dll goto nobuild
if not exist dist\LotusSubs\bin\ffmpeg.exe goto nobuild

set ISCC=
for %%P in ("%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" "%ProgramFiles%\Inno Setup 6\ISCC.exe" "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe") do if exist %%P set ISCC=%%P
if not defined ISCC goto noinno

for /f "delims=" %%V in ('python -c "import version; print(version.APP_VERSION)"') do set VER=%%V
if not defined VER goto failed

%ISCC% /DAppVersion=%VER% installer\LotusSubs.iss
if errorlevel 1 goto failed
echo.
echo ==========================================================
echo  DONE!  Installer:  installer\Output\LotusSubs-Setup-%VER%.exe
echo  Send that one file to users.
echo ==========================================================
pause
exit /b 0

:nobuild
echo dist\LotusSubs is missing or incomplete. Run build.bat first.
pause
exit /b 1

:noinno
echo Inno Setup 6 was not found. Install it (free) from https://jrsoftware.org/isdl.php
echo or run:  winget install JRSoftware.InnoSetup
pause
exit /b 1

:failed
echo Installer build failed - see the messages above.
pause
exit /b 1
