---
name: build-release
description: Build and ship a HiruTaglineCreator Windows executable with PyInstaller — version bump, spec files, dist layout and the known build failures. Use when asked to build a new exe, cut a version, or package the app for the newsroom.
---

# Building a release

Latest shipped: **v3.1** (2026-10-05), `HiruTaglineCreator/dist/HiruTaglineCreator_v3.1.exe`,
≈59 MB, onefile, no console window.

## Procedure

1. **Verify the change first.** If `utils/fm_converter.py` was touched, all four steps in
   `../sinhala-fm-converter/verification.md` must pass before building. A bad converter
   ships silently — the exe looks fine until a word is typed.
2. **Bump the version in two places** (they must match, or the spec and the build script
   disagree):
   - `build_exe.py` → `--name=HiruTaglineCreator_vX.Y`
   - copy the latest `HiruTaglineCreator_vX.Y.spec` → `HiruTaglineCreator_vX.Y.spec`, updating both
     the `name=` in `EXE(...)` and the filename.
3. **Close any running copy of the exe.** PyInstaller fails with `PermissionError` if the
   target exe is open — this has bitten before.
4. Build:
   ```bash
   cd HiruTaglineCreator
   py -3 build_exe.py
   # or, from the spec:
   py -3 -m PyInstaller HiruTaglineCreator_vX.Y.spec --noconfirm
   ```
5. Smoke-test `dist/HiruTaglineCreator_vX.Y.exe`: type a Sinhala tagline, check the live
   preview, generate one PNG. Include a word from
   `../sinhala-fm-converter/corrections-log.md` if the converter changed.
6. Commit source + spec. The exe itself is large; follow whatever the repo has been doing
   (dist exes have historically been committed).

## What gets bundled

```python
'--onefile', '--windowed', '--icon=assets/app_icon.ico',
'--add-data=templates;templates',   # MAIN_TAG.png, SUB_TAG.png
'--add-data=assets;assets',
'--add-data=config;config',         # settings.json ships inside the exe
'--hidden-import=PIL', '--hidden-import=PIL._tkinter_finder',
'--clean', '--noconfirm',
```

PyQt5 and Pillow are picked up automatically. `requirements.txt` lists only
`Pillow>=10.0.0` and `requests>=2.31.0` — **PyQt5 and pyinstaller are missing from it**;
install them separately on a fresh machine.

## Fonts are NOT bundled

FM Ganganee and FM Sandhyanee are per-user Windows font installs and are not embedded.
Any target PC needs them installed or the app exits at startup with a font error. Ship the
two TTFs alongside the exe.

## Known build noise

| Message | Meaning |
|---|---|
| `Hidden import "sip" not found` | harmless, PyQt5 5.15 does not need it |
| `PermissionError: dist\...exe` | the exe is running — close it |
| UPX warnings | `upx=True` in the spec; harmless |

## dist/ layout

`dist/` also holds `config/`, `logs/` and `templates/` next to the exes — the onefile build
unpacks its own copies at runtime, but these are what a hand-copied install uses. The full
version history (`HiruTaglineCreator.exe` through `v2.6.exe`) lives there; v1.x builds are
~61 MB, the original Feb 2026 build is ~30 MB.
