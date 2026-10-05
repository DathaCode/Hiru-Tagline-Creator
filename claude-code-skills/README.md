# claude-code-skills — Hiru News Tagline Creator

Project knowledge base for Claude Code. Everything a fresh session needs to work on
this repo **without any chat history**.

| Skill | Read it when |
|---|---|
| [sinhala-fm-converter/SKILL.md](sinhala-fm-converter/SKILL.md) | Any Sinhala word previews/generates wrong, or a conversion rule must be added or changed. **This is the skill that matters most — almost every bug in this project is here.** |
| [tagline-app/SKILL.md](tagline-app/SKILL.md) | Working on the GUI, the beds, preview, generation, templates or sessions. |
| [build-release/SKILL.md](build-release/SKILL.md) | Building a new `.exe`, bumping a version, or shipping to the newsroom. |

## Supporting references (inside `sinhala-fm-converter/`)

- [encoding-reference.md](sinhala-fm-converter/encoding-reference.md) — how FM legacy fonts
  encode Sinhala, the kombuwa rule, the special single-glyph ligatures, and the exact
  order the conversion pipeline runs in.
- [corrections-log.md](sinhala-fm-converter/corrections-log.md) — **every Sinhala rendering
  correction ever made to this project**, dated, with the word that triggered it and the
  rule that fixed it. Check here before "fixing" anything — several of these were
  re-broken and re-fixed more than once.
- [verification.md](sinhala-fm-converter/verification.md) — how to prove a change is correct
  (three scripts + a visual render check). Never ship a converter change without this.

## Scripts

Live in [sinhala-fm-converter/scripts/](sinhala-fm-converter/scripts/). Run them from
`HiruTaglineCreator/`:

```bash
PYTHONIOENCODING=utf-8 py -3 ../claude-code-skills/sinhala-fm-converter/scripts/fm_audit.py
PYTHONIOENCODING=utf-8 py -3 ../claude-code-skills/sinhala-fm-converter/scripts/fm_regress.py
PYTHONIOENCODING=utf-8 py -3 ../claude-code-skills/sinhala-fm-converter/scripts/fm_render.py ද්‍රෝහීයා
```

## Housekeeping

These skills are plain Markdown and are read on demand. To make them invocable as real
Claude Code skills (`/sinhala-fm-converter`), copy or symlink the skill folders into
`.claude/skills/`. The root `CLAUDE.md` already points every session here.
