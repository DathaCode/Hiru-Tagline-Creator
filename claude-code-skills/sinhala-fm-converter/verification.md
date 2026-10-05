# Verifying a converter change

Four steps. Skipping the last one is how wrong glyphs (`ඳෙ`→`fË`) survived for months.

All commands run from `HiruTaglineCreator/`. `PYTHONIOENCODING=utf-8` is not optional —
the Windows console is cp1252 and will raise `UnicodeEncodeError` on any Sinhala output.

## 1. Convert the reported word

```bash
PYTHONIOENCODING=utf-8 py -3 -c "import sys;sys.path.insert(0,'.');\
from utils.fm_converter import convert_unicode_to_fm as c, find_unconverted_sinhala as l;\
w='ද්‍රෝහීයා';print(repr(c(w)), l(c(w)))"
```

Reading the result:

| Symptom | Cause |
|---|---|
| `find_unconverted_sinhala` returns characters | a missing rule, or a rule shadowed by an earlier one → step 2 |
| no leftovers, but the shape is wrong | wrong glyph byte — compare with a sibling consonant in the same table |
| `%` or `H` present in a word with no ZWJ | a pattern lost its ZWJ |
| kombuwa in the wrong place | the `f` prefix is missing or the tail (`a`/`d`/`da`/`!`) is wrong |

## 2. Static audit

```bash
PYTHONIOENCODING=utf-8 py -3 ../claude-code-skills/sinhala-fm-converter/scripts/fm_audit.py
```

Reports rules that can never fire, and every consonant×vowel combination that still leaks
raw Sinhala. Baseline on 2026-09-23: **19 shadowed, 44 leaking (all `ඞ`)**. A new entry
means the change broke something.

## 3. Regression corpus

```bash
PYTHONIOENCODING=utf-8 py -3 ../claude-code-skills/sinhala-fm-converter/scripts/fm_regress.py
```

75 words — every word that has ever had a bug filed against it, plus everyday newsroom
vocabulary. Must print `PASS`. If a word changed, be able to say why; then re-bless the
file with `--update` **after** step 4, and log the change in `corrections-log.md`.

The script also asserts two things a golden file cannot: no-ZWJ words must contain no `%`
or `H`, and ZWJ words must keep their ligature.

## 4. Look at it

```bash
PYTHONIOENCODING=utf-8 py -3 ../claude-code-skills/sinhala-fm-converter/scripts/fm_render.py ද්‍රෝහීයා
# before/after against the backup copy:
PYTHONIOENCODING=utf-8 py -3 ../claude-code-skills/sinhala-fm-converter/scripts/fm_render.py \
    --compare utils/fm_converter.py.bak ද්‍රෝහීයා ද්‍රෝහී
```

Writes `fm_render.png` in FM Sandhyanee on the tag-bed orange. **Open it and read the
Sinhala.** If working as Claude, read the PNG back with the Read tool — it renders as an
image and the glyphs are legible at 58pt.

## 5. Then the app itself

Launch and type the word into the TAG BED field; the live preview uses the same function.

```bash
py -3 main.py
```

A build is only needed for the newsroom — see `../build-release/SKILL.md`.

## Safety net

Any patch script should copy `utils/fm_converter.py` to `utils/fm_converter.py.bak` before
writing. The `.bak` doubles as the "before" side of `fm_render.py --compare`. Delete it
once the change is committed.
