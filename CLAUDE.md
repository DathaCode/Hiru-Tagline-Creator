# HiruTaglineCreator

Windows desktop app that turns Sinhala text into 1920×1080 broadcast tagline PNGs for
Hiru News. Tkinter UI, PyQt5 text rendering, Pillow compositing, PyInstaller onefile.
Working copy: **`HiruTaglineCreator/`** (the `_v2.1`, `_v3.1`, `_v3.1_src` folders are
frozen snapshots).

## Read these before working

| File | When |
|---|---|
| [claude-code-skills/sinhala-fm-converter/SKILL.md](claude-code-skills/sinhala-fm-converter/SKILL.md) | **any Sinhala word renders wrong** — the single most common bug class here |
| [claude-code-skills/sinhala-fm-converter/corrections-log.md](claude-code-skills/sinhala-fm-converter/corrections-log.md) | before changing any conversion rule — every past fix, and the word behind it |
| [claude-code-skills/tagline-app/SKILL.md](claude-code-skills/tagline-app/SKILL.md) | GUI, beds, preview, generation, sessions |
| [claude-code-skills/build-release/SKILL.md](claude-code-skills/build-release/SKILL.md) | building an exe / cutting a version |

## The one thing to know

Sinhala is stored as Unicode but **rendered with legacy FM fonts**, which carry Sinhala
glyphs at Latin codepoints and have no glyphs at all in U+0D80–U+0DFF.
`utils/fm_converter.py` translates between them with ~580 ordered `str.replace()` calls.
**Order is the design** — a rule placed too early silently kills every longer rule that
contains its pattern. If a Sinhala character survives into the output, the app draws a
blank box; that is what "previews incorrectly" almost always means.

Never change a conversion rule without running the four checks in
[verification.md](claude-code-skills/sinhala-fm-converter/verification.md), ending with a
rendered PNG that someone actually looks at.

## Commands

```bash
cd HiruTaglineCreator
py -3 main.py                                    # run the app
py -3 build_exe.py                               # build the exe (bump the version first)

# converter checks (PYTHONIOENCODING=utf-8 is required — the console is cp1252)
PYTHONIOENCODING=utf-8 py -3 ../claude-code-skills/sinhala-fm-converter/scripts/fm_audit.py
PYTHONIOENCODING=utf-8 py -3 ../claude-code-skills/sinhala-fm-converter/scripts/fm_regress.py
PYTHONIOENCODING=utf-8 py -3 ../claude-code-skills/sinhala-fm-converter/scripts/fm_render.py <word>
```

## Fonts

`FM GANGANEE` (topic bed) and `FM SANDHYANEE` (tag/white beds) must be installed at
`C:\Users\Hp\AppData\Local\Microsoft\Windows\Fonts\`. The app exits at startup without them.
