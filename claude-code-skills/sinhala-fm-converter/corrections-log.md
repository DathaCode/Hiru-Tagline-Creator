# Sinhala rendering corrections — full history

Every correction made to `HiruTaglineCreator/utils/fm_converter.py`, oldest first.

Sources: git history of the repo, and the claude-mem observation database
(`~/.claude-mem/claude-mem.db`) for the April 2026 sessions whose chat transcripts were
deleted by Claude Code's 30-day cleanup. Where a fix was reported by the user in their own
words, those words are quoted — they are the best description of the symptom.

---

## 2026-03-13 · `feaedcd` — converter created (v1.3)

709 lines, ~500 `str.replace()` rules. Ordering contract established in the docstring:
*"The order of replacements is non-negotiable."*

---

## 2026-03-17 · `8583cc6` "rakaransa/ rendering issue fixed"

| Change | Detail |
|---|---|
| `ශ්‍රේ` → `fYa%` | was `fYa` — the rakaransaya `%` was missing entirely |
| **new block** `්‍ර` + `ි` | 17 rules: `ඳ්‍රි`→`¢%`, `ඨ්‍රි`→`À%`, `ඛ්‍රි`→`Å%`, `ච්‍රි`→`Ñ%`, `ඵ්‍රි`→`Ý%`, `ට්‍රි`→`á%`, `ඩ්‍රි`→`ä%`, `ඬ්‍රි`→`ç%`, `ධ්‍රි`→`ê%`, `ථ්‍රි`→`Ó%`, `බ්‍රි`→`ì%`, `ම්‍රි`→`ñ%`, `ඹ්‍රි`→`ô%`, `ව්‍රි`→`ú%`, `ඡ්‍රි`→`ý%`, `ජ්‍රි`→`ð%`, generic `්‍රි`→`s%` |
| **new block** `්‍ර` + `ී` | 14 rules + generic `්‍රී`→`S%` |
| moved | a stray `බ්‍රි` rule had been sitting inside the bare-yansaya block; deleted from there |

Why: consonants that have their own *i/ii* ligature glyph (`ට`+`ි` = `á`, not `g`+`s`)
need that glyph **plus** `%`, which the generic rule could not produce.

---

## 2026-04-07 · `fb40e36` "train raka"

Added a word-level exception: `දුම්රිය` (train) → `ÿïßh`, placed before all conjunct
rules. `ම්` + `ර` is a compound-word boundary, not a rakaransaya, but at the time ZWJ was
being stripped early so the general rule could not tell the difference.
**Removed again on 2026-04-27** once ZWJ gating made it unnecessary.

---

## 2026-04-08 · `5274353` "ර් + Yansaya (්‍ය)"

`ර්‍ය` is never a yansaya ligature in this house style.

- deleted `ර්ය` → `©`
- added `ර්‍ය` → `¾` + `ය` (ර් converted immediately, ය left as Unicode so the vowel
  tables can still pick it up)

Check word: `ආර්‍යාව` → `wd¾hdj`.

---

## 2026-04-27 → 04-29 · ZWJ-aware rewrite (no commit of its own; landed in `0c5e342`)

The largest correction in the project's history. Transcript purged; recovered from
claude-mem observations #1–#16 and user prompts #1–#6.

**What the user reported** (2026-04-27):

> "වෙල්යාය and මල්යාය also previews incorrectly, these are the examples for both, these
> words should be exactly as it is…
> 1. පොල්යාය, මල්යහන, අත්යන්ත්‍ර, පස්යාල, පාසල්යන, හිස්යාම, ගල්යාය
> 2. පොත්රාක්කය, මල්රේණු, රන්රස, ගස්රිකිලි, බස්රිය, අත්රෙදි, අත්රෝදය, කාසල්රි
> 3. හඳෙන් ඕස්ට්‍රේලියාව
> …mentioned words need to preview and generate exactly as mentioned (without rakaransaya
> or yansaya)"

**Root cause:** lines 98–99 stripped ZWJ/ZWNJ *before* any conjunct rule ran, so
`ශ්‍ර` (real rakaransaya) and `ශ්ර` (plain cluster) became the same string. Every
`ල්ය`, `ත්ර`, `ම්ර` cluster then got a ligature it should never have had.

**The fix** (applied by `_apply_zwj_fix.py`, since deleted):

1. ZWJ/ZWNJ stripping moved from the **start** of the function to just before the
   post-processing block at the end.
2. **78 yansaya** patterns rewritten `්ය` → `්‍ය` (ZWJ required to fire).
3. **83 rakaransaya** patterns rewritten `්ර` → `්‍ර`.
4. `ඳෙ` → `f|` — was `fË` (U+00CB). Decided by rendering both in FM Sandhyanee and
   looking: `Ë` is the wrong glyph. Now consistent with `ඳේ` / `ඳෝ` / `ඳො`.
   Check word: `හඳෙන්` → `yf|ka`.
5. New rule `ට්‍රේ` → `fga%`.
6. `දුම්රිය` word exception deleted (see 2026-04-07) — ZWJ gating handles it; still
   converts to `ÿïßh`.
7. Verified with 25 string cases plus two rendered PNGs (suppression + preservation).

**Also investigated, no change made:** `ඕ` → `´` (U+00B4). Seven candidate encodings were
rendered at 60pt and 96pt (`T!`, `Tda`, `fTda`, `wda`, `Td`, `T`); `´` was kept.

---

## 2026-04-28 → 04-29 · the `ඕස්ට්‍රේලියාව` saga

Five rounds. Worth reading before touching any 3-consonant cluster.

> "still ඕස්ට්‍රේලියාව showing incorrectly."
> "ඕස්ට්‍රේලියාව - should include ට්‍රේ like this - ට්‍රේ"
> "ට්‍රේ combination previews wrong (fix only this word)"
> "ඕස්ට්‍රේලියාව word have small issue - න් / ට් refer these two letters, hal vowel
> applying differently, should be apply correctly for ට්‍රේ letter"

The cluster is `ස්` + `ට` + `්‍ර` + `ේ` — the kombuwa has to jump left over *two*
consonants while `ස` keeps its hal. `ට්‍රේ`→`fga%` alone put the kombuwa in the wrong
place. Resolved with a longer, more specific rule placed **before** it:

```python
s = s.replace('ස්ට්‍රේ', 'iafÜ%')   # ස + hal, then kombuwa, then ට් glyph (Ü) + rakaransaya
s = s.replace('ට්‍රේ',  'fga%')
```

Check word: `ඕස්ට්‍රේලියාව` → `´iafÜ%,shdj`.

---

## 2026-07-27 · `0c5e342` "SLASSCOM version + latest original"

Committed the April work, plus:

| Change | Detail |
|---|---|
| `ෛ` table completed | 31 new rules (`ෂෛ`…`ථෛ`), mirroring the `ෙ` list so every consonant is covered |
| `ෆේ` → `f*a` | was `f*` — missing the `a` tail |
| `ස්ට්‍රේ` → `iafÜ%` | the Australia fix above |

---

## 2026-08-21 · `df9e057` "Readme update and removed test files"

Filled gaps in the yansaya + o/oo tables: `ණ්‍යෝ`→`fKHda`, and `ඡ ඪ ඝ ළ ඵ ඨ ණ ච ල න` for
`්‍යො`. Same pattern as always — a consonant missing from a table leaks its vowel sign.

---

## 2026-09-23 · `ද්‍රෝහීයා` (this session)

**Reported:** `ද්‍රෝහීයා` previewed as `දු□හීයා` — the `ෝ` rendered as a blank box.

**Root cause:** `s.replace('ද්‍ර', 'ø')` sat at line 110, in the punctuation
pre-processing block — before everything. `ද්‍රෝ` became `ø` + `ෝ`, and the four
hand-written rules further down were unreachable:

```
line 292  'ද්‍රෝ' -> 'føda'   never fired — input was already 'øෝ'
line 306  'ද්‍රො' -> 'fød'    never fired
line 321  'ද්‍රේ' -> 'føa'    never fired
line 338  'ද්‍රෙ' -> 'fø'     never fired
```

The orphaned `ෝ` was then emitted as raw U+0DDD, which FM Sandhyanee has no glyph for.
This had been broken since v1.3 — it only surfaced now because no tagline had used
`ද්‍ර` + a kombuwa vowel before.

**Changes:**

| # | Change |
|---|---|
| 1 | bare `ද්‍ර`→`ø` moved from line 110 down to line ~389, below every `ද්‍ර`+vowel rule and above the `්‍රි`/`්‍රී` rules (so `ද්‍රි`→`øs`, `ද්‍රී`→`øS` still work) |
| 2 | added `ද්‍රෛ` → `ffø` (beside `ත්‍රෛ`) and `ද්‍රෞ` → `fø!` (beside `ප්‍රෞ`) — both must stay above the move point |
| 3 | added `_KOMBUWA_RE` safety net (line ~646): rebuilds any consonant + `ෙ ේ ෛ ො ෝ ෞ` pair the tables miss. Runs after every explicit rule, so hand-tuned glyphs still win. Cut the "raw Sinhala in output" cases from **277 to 44** (the 44 are all `ඞ`) |
| 4 | input is now `unicodedata.normalize('NFC', …)` — some IMEs emit `ෝ` as `ෙ`+`ා` (U+0DD9 U+0DCF), which matched no rule at all |
| 5 | added `find_unconverted_sinhala(fm_text)` helper for tests |

**Verified:** `ද්‍රෝහීයා` → `fødayShd`, rendered and visually confirmed in FM Sandhyanee.
71-word regression corpus: 64 unchanged, 7 changed — all 7 are `ද්‍ර` + kombuwa and all 7
were broken before.

---

## 2026-10-05 · quote marks drawn in Arial

**Reported:** `'ද්‍රෝහියා'` and `"සෛල"` rendered with wrong quote glyphs — `"` came out as
a comma pair (`,සෛල,`) and `'` as a stray tick.

**Root cause:** neither FM Sandhyanee nor FM Ganganee has a usable quote glyph. `"` was
passed through untouched, and FM's `"` slot is the comma glyph; `'` was mapped to `z`,
which is not a quote either.

**Fix:** quote marks now take the same route as English letters — escaped to PUA at the
start of `convert_unicode_to_fm()` (`_ARIAL_PUA`: `"`→U+E022, `'`→U+E027, `‘ ’ “ ”`→
U+E100–E103), split back out by `split_fm_and_english()`, and drawn by `text_renderer` in
the English font (Arial, bold). Curly quotes are included because Word pastes produce them.
The old `'`→`z` rule is gone (unreachable). Applies to all three beds.

**Verified:** rendered through the real `TextRenderer.render_tag_bed_text()`; `fm_regress.py`
now fails if any quote mark lands in an FM segment (confirmed it catches the old code).

---

## Reference lists

### Must render WITHOUT a ligature (plain clusters, no ZWJ)

`පොල්යාය` `මල්යහන` `පස්යාල` `පාසල්යන` `හිස්යාම` `ගල්යාය` `වෙල්යාය` `මල්යාය`
`පොත්රාක්කය` `මල්රේණු` `රන්රස` `ගස්රිකිලි` `බස්රිය` `අත්රෙදි` `අත්රෝදය` `කාසල්රි`
`ගම්රට` `බස්රථය` `දුම්රිය`

### Must KEEP the ligature (ZWJ present)

`මෙට්‍රික්` `ශ්‍රේෂ්ඨාධිකරණය` `ක්‍රීඩාව` `ශක්‍ය` `වාක්‍ය` `ශ්‍රී ලංකා` `අත්‍යන්ත්‍ර`
`ආර්‍යාව` `ක්‍රි`

### Words with a dedicated fix behind them

| Word | Expected FM | Fixed on |
|---|---|---|
| `හඳෙන්` | `yf\|ka` | 2026-04-27 |
| `ඕස්ට්‍රේලියාව` | `´iafÜ%,shdj` | 2026-04-29 |
| `දුම්රිය` | `ÿïßh` | 2026-04-07 / 04-27 |
| `ආර්‍යාව` | `wd¾hdj` | 2026-04-08 |
| `ද්‍රෝහීයා` | `fødayShd` | 2026-09-23 |
