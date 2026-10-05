---
name: sinhala-fm-converter
description: Fix or extend the Sinhala Unicode → FM legacy font converter in HiruTaglineCreator. Use whenever a Sinhala word previews or generates incorrectly, a letter combination renders as a blank box, a rakaransaya/yansaya appears where it should not, or a new conversion rule must be added to utils/fm_converter.py.
---

# Sinhala → FM font conversion

Everything the newsroom sees goes through **one function**:

```
HiruTaglineCreator/utils/fm_converter.py  →  convert_unicode_to_fm(text)
```

`core/text_renderer.py` calls it at 4 places (lines 143, 208, 282, 316) — live preview and
generated PNG both. **Fix the rule, and preview + output are both fixed.** There is nowhere
else to patch.

> Before changing a rule, read [corrections-log.md](corrections-log.md). Several of these
> combinations have been fixed, re-broken by a later edit, and fixed again. The log says
> which word each rule exists for.

## The five rules that govern this file

**1. Order is the whole design.** The function is ~570 sequential `str.replace()` calls.
A replacement can only fire if an earlier one has not already eaten its input. Specific →
general, always: `ස්ට්‍රේ` before `ට්‍රේ` before `ට්`; every `ද්‍ර` + vowel rule before bare
`ද්‍ර`; every conjunct before the base-consonant table. A rule placed too early is the
single most common bug in this file — it silently kills every longer rule that contains it.

**2. ZWJ (U+200D) is the authority on ligatures.** `ක්‍ර` (with ZWJ) is rakaransaya → `%`.
`ක්ර` (no ZWJ) is a plain cluster and must render as two separate letters. Every yansaya
and rakaransaya pattern in the file therefore contains a literal ZWJ, and ZWJ is stripped
only at the very end (line ~840), never at the start. Do not "clean up" the input by
stripping ZWJ early — that bug cost a full debugging session in April 2026.

**3. Kombuwa vowels are typed before their consonant.** In FM fonts the `ෙ` glyph is `f`
and it sits *to the left* of the consonant, with a tail after it:

| Vowel | FM form | Example |
|---|---|---|
| `ෙ` | `f` + C | `දෙ` → `fo` |
| `ේ` | `f` + C + `a` | `තේ` → `f;a` |
| `ෛ` | `ff` + C | `කෛ` → `ffl` |
| `ො` | `f` + C + `d` | `කො` → `fld` |
| `ෝ` | `f` + C + `da` | `කෝ` → `flda` |
| `ෞ` | `f` + C + `!` | `කෞ` → `fl!` |

C is the consonant's FM code **plus** its `%` (rakaransaya) or `H` (yansaya) if it has one:
`ග්‍රෝ` → `f` + `.` + `%` + `da` = `f.%da`. Since Python's `str.replace` cannot reorder
characters, every such pair needs an explicit rule — or the generic
`_KOMBUWA_RE` safety net at line ~646 rebuilds it.

**4. No Sinhala codepoint may survive into the output.** FM fonts have **zero** glyphs in
U+0D80–U+0DFF, so a leftover `ෝ` renders as nothing — the blank box the user reports.
`find_unconverted_sinhala(fm_text)` in the same module returns any survivors; it must
return `[]`.

**5. Byte-correct is not proof.** The final check is always a PNG rendered in the real
FM font and looked at. See [verification.md](verification.md).

## Pipeline order (current line numbers)

```
124  NFC normalise        compose ෙ+ා → ෝ etc.
128  escape A-Za-z        → PUA U+E041.. so Latin survives
149  punctuation          , ' ( ) % / ? ! = . + : ;
170  ත්‍රෛ  ද්‍රෛ          word/cluster specials
176  ෛ + consonant        'ff' + base
219  ප්‍රෞ  ද්‍රෞ
225  yansaya  + ෝ ො ෙ
324  rakaransaya + ෝ ො ේ ෙ      ← ස්ට්‍රේ lives at 368, before ට්‍රේ
389  ද්‍ර bare → ø                ← must be here, not earlier
396  rakaransaya + ි ී
436  ර්‍ය exception → ¾ + ය       (never a ligature)
442  bare ්‍ය → H, bare ්‍ර → %
448  ෞ ෝ ො ේ ෙ + consonant      the big tables
646  kombuwa safety net           rebuilds whatever the tables missed
653  තු ශු භු ගු කු / රු රූ …
669  standalone vowels ආ ඇ ඈ ඌ ඖ ඒ ඕ
680  special conjunct glyphs      ඳි දු දී ර් ට් ඩි මි …
763  base consonants              ග ක ත ද …  (AFTER everything above)
824  standalone vowel signs       ැ ෑ ෙ ු ි ූ ී ා ්
840  strip leftover ZWJ/ZWNJ
846  restore escaped punctuation
```

## Changing a rule — checklist

1. Find the word the user reported and convert it before touching anything:
   ```bash
   cd HiruTaglineCreator
   PYTHONIOENCODING=utf-8 py -3 -c "import sys;sys.path.insert(0,'.');from utils.fm_converter import *;w='ද්‍රෝහීයා';print(repr(convert_unicode_to_fm(w)),find_unconverted_sinhala(convert_unicode_to_fm(w)))"
   ```
   Leftover Sinhala → a missing rule or a shadowed one. No leftovers but wrong shape → a
   wrong glyph byte; compare against a sibling consonant in the same table.
2. Run `scripts/fm_audit.py` — it reports every rule that can never fire because an
   earlier rule already consumed its pattern. That is how the `ද්‍රෝ` bug was found.
3. Add the rule **in the right block** (see the order above). Match the surrounding style:
   `\uXXXX` escapes with the literal glyph in a trailing comment.
4. Run `scripts/fm_regress.py`. Every word in the golden corpus must be unchanged except
   the ones you intended to change.
5. Run `scripts/fm_render.py <word>` and **look at the PNG**.
6. Append an entry to [corrections-log.md](corrections-log.md) — date, word, rule, reason.

## Characters drawn in Arial instead of FM

Latin `A-Za-z` and the quote marks `' " ‘ ’ “ ”` are escaped to Private Use codepoints at
the start of the function and drawn by `text_renderer` in bold Arial (see `_ARIAL_PUA`,
`split_fm_and_english()`). If the user reports a symbol that FM cannot draw, add it there —
do not invent an FM byte for it.

## Known gaps (as of 2026-09-23)

- **`ඞ` (kantaja naasikyaya) has no base mapping.** Only `ඞ්`→`Ù` and `ඞී`→`ü` exist, so
  any other `ඞ` combination leaks raw Unicode. Archaic letter, never seen in a tagline —
  left alone deliberately. All 44 remaining leak cases are this one letter.
- **`ක්ෂ` + vowel is shadowed.** `ෂෝ`→`fIda` fires before `ක්ෂෝ`→`fÌda`, so `ලක්ෂ` renders
  as `,laI` (ක් + ෂ written out) rather than the `Ì` ligature. Readable and in production
  for months — do **not** change without asking, it is a typographic preference, not a bug.
- **`ර්ණ`→`“` is shadowed** by `ර්`→`¾`; `වර්ණ` renders `j¾K`. Same story as above.
- `ඪී`, `ථී`, `ඞ්`, `ඡි` each appear twice with different values; the second is dead.
  Harmless, but do not add a third.
- `award_submission_2026/HiruTaglineCreator_v3.1_src/` (the SLASSCOM award fork) carries
  its own copy of this file. The user has asked for fixes to be ported there; after a
  change, copy the file across and run `fm_regress.py` from that folder too.
