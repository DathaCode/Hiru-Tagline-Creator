# FM font encoding — reference

## What an FM font actually is

FM Sandhyanee, FM Ganganee and FM Malithi are **pre-Unicode** Sinhala typefaces. They carry
Sinhala glyphs at **Latin-1 / Latin-Extended codepoints** and have **zero** glyphs in the
Sinhala Unicode block U+0D80–U+0DFF (verified with `check_font_glyphs.py`, which reads the
TTF cmap with fontTools).

So `'fmd,Hdh'` is not Latin text — each byte selects a Sinhala glyph. And a Sinhala
character that survives conversion selects **nothing**: it renders as a blank box or
disappears. That is the signature of every "word previews incorrectly" report in this
project.

Font files:

```
C:\Users\Hp\AppData\Local\Microsoft\Windows\Fonts\FMSandhyanee x.ttf    TAG / WHITE bed
C:\Users\Hp\AppData\Local\Microsoft\Windows\Fonts\FMGanganee x.ttf      TOPIC bed
```

Known slots: `Ë` U+00CB Edieresis · `|` U+007C bar · `â` U+00E2 · `Ì` U+00CC · `ï` U+00EF ·
`Ü` U+00DC · `¾` U+00BE · `ø` U+00F8 · `ÿ` U+00FF · `´` U+00B4.

## The three shapes that cause every bug

### 1. Kombuwa (ෙ-class vowels) — glyph goes BEFORE the consonant

| Vowel | Pattern | Example |
|---|---|---|
| `ෙ` | `f` + C | `දෙ` → `fo` |
| `ේ` | `f` + C + `a` | `තේ` → `f;a` |
| `ෛ` | `ff` + C | `කෛ` → `ffl` |
| `ො` | `f` + C + `d` | `කො` → `fld` |
| `ෝ` | `f` + C + `da` | `කෝ` → `flda` |
| `ෞ` | `f` + C + `!` | `කෞ` → `fl!` |

C includes the consonant's rakaransaya `%` or yansaya `H`:
`ග්‍රෝ` → `f.%da`, `ක්‍යෝ` → `flHda`.

Many consonants have a **single fused glyph** for consonant+vowel that must be used
instead of the two-part form — `මේ`→`fï` (not `fua`), `ඩේ`→`fâ`, `බේ`→`fí`, `ටේ`→`fÜ`,
`වේ`→`fõ`, `ජේ`→`fÊ`, `චේ`→`fÉ`, `රේ`→`f¾`, `ඹේ`→`fò`, `ඡේ`→`fþ`, `ඬේ`→`få`,
`ධේ`→`fè`, `ඛේ`→`fÄ`. This is why the tables are enumerated by hand rather than generated.

### 2. Rakaransaya `්‍ර` and yansaya `්‍ය` — ZWJ decides

| Unicode | Meaning | FM |
|---|---|---|
| `ක` + `්` + **ZWJ** + `ර` | rakaransaya ligature | `l%` |
| `ක` + `්` + `ර` | plain cluster, two letters | `la` + `r` |
| `ක` + `්` + **ZWJ** + `ය` | yansaya ligature | `lH` |
| `ක` + `්` + `ය` | plain cluster | `la` + `h` |

Two consonants break the pattern and get their own glyph instead of base+`%`:

- `ද්‍ර` → `ø` (one glyph, **no** `%`) — hence `ද්‍රෝ`→`føda`, `ද්‍රි`→`øs`
- `ර්‍ය` → `¾` + `ය` (house style: never a ligature)

Consonants with an *i/ii* ligature glyph take that glyph + `%`:
`ට්‍රි`→`á%`, `බ්‍රී`→`î%`, `ව්‍රි`→`ú%`, generic fallbacks `්‍රි`→`s%`, `්‍රී`→`S%`.

### 3. Hal kirima `්` and right-side vowels

`්` → `a` (plain), but most consonants have a fused hal glyph: `ම්`→`ï`, `ට්`→`Ü`,
`ර්`→`¾`, `ඩ්`→`â`, `බ්`→`í`, `ව්`→`õ`, `ධ්`→`è`, `ච්`→`É`, `ජ්`→`Ê`, `ඛ්`→`Ä`,
`ඹ්`→`ò`, `ඡ්`→`þ`, `ඬ්`→`å`, `ඞ්`→`Ù`.

Right-side vowels need no reordering and have plain fallbacks:
`ා`→`d` · `ැ`→`e` · `ෑ`→`E` · `ි`→`s` · `ී`→`S` · `ු`→`q` · `ූ`→`Q` · `ෘ`→`D` · `ං`→`x`.

Fused exceptions: `දු`→`ÿ`, `දූ`→`¥`, `දි`→`È`, `දී`→`§`, `ලු`→`¨`, `ලූ`→`Æ`, `ළු`→`¿`,
`රු`→`re`, `රූ`→`rE`, `රි`→`ß`, `රී`→`Í`, `තු`→`;=`, `කු`→`l=`, `ගු`→`.=`, `ශු`→`Y=`,
`භු`→`N=`, `ඟු`→`Õ=`.

## Other pipeline behaviour worth knowing

- **Latin passthrough.** `A-Za-z` are escaped to PUA (U+E041…) at the start so FM rules
  cannot mangle them, then split back out by `split_fm_and_english()`; `text_renderer`
  draws those runs in a normal English font (bold). That is why mixed
  "ජනාධිපති BREAKING" taglines work.
- **Quote marks go to Arial**, not FM: `'` `"` `‘` `’` `“` `”` are escaped to PUA
  (`_ARIAL_PUA`) alongside Latin letters and drawn in the English font. FM fonts have no
  usable quote glyph — FM's `"` slot is a comma. Add any other character the FM fonts
  cannot draw to `_ARIAL_PUA` the same way.
- **Other punctuation is remapped**, not passed through: `,`→`"` · `.`→`'` · `(`→`^` · `)`→`&` ·
  `%`→`]` · `/`→`$` · `?`→`@` · `!`→`æ` · `=`→`}` · `:`→`(` · `;`→`¦` · `+`→`¬` ·
  en-dash → hyphen.
- **NFC normalisation** runs first (added 2026-09-23): `ෙ`+`ා` → `ෝ`, `ෙ`+`්` → `ේ`,
  `ෙ`+`ෟ` → `ෞ`. Without it, decomposed input from some IMEs matches no rule.
- **Base consonants run last**, after every conjunct and vowel combination. Anything added
  below that block will be dead code.
- `ක→C`, `ෑ→E`, `ත→F`, `න→J` were removed as wrong duplicates that shadowed the correct
  lowercase mappings (`ක→l`, `න→k`). Do not reintroduce them.
