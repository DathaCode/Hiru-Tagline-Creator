"""
Sinhala Unicode → FM ASCII Converter
Based on GururLK conversion logic (gurulk.com)

Converts Sinhala Unicode text to FM-Malithi compatible ASCII characters.
The output renders correctly ONLY when an FM font (FM-Ganganee, FM-Sandhyanee, etc.)
is active on the rendering surface.

CRITICAL: The order of replacements is non-negotiable.
Complex conjuncts (rakaransaya, yansaya, ෙ+consonant combos) MUST be replaced
before their component base characters, or the output will be garbled.
"""


# PUA offset for Latin letter escaping
_LATIN_PUA_BASE = 0xE000


def _escape_latin(text):
    """Replace A-Za-z with PUA equivalents so they survive FM conversion."""
    result = []
    for ch in text:
        if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
            result.append(chr(_LATIN_PUA_BASE + ord(ch)))
        else:
            result.append(ch)
    return ''.join(result)


def has_english_segments(text):
    """Check if converted text contains PUA-encoded English characters."""
    for ch in text:
        code = ord(ch)
        if _LATIN_PUA_BASE + 0x41 <= code <= _LATIN_PUA_BASE + 0x7A:
            return True
    return False


def split_fm_and_english(text):
    """
    Split FM-converted text into segments of (string, is_fm).
    PUA-encoded chars (English letters) → (original_letter, False)
    Regular chars (FM ASCII) → (text, True)
    """
    segments = []
    current = []
    current_is_fm = True

    for ch in text:
        code = ord(ch)
        is_pua = (_LATIN_PUA_BASE + 0x41 <= code <= _LATIN_PUA_BASE + 0x7A)

        if is_pua:
            if current and current_is_fm:
                segments.append((''.join(current), True))
                current = []
            current_is_fm = False
            current.append(chr(code - _LATIN_PUA_BASE))  # restore original letter
        else:
            if current and not current_is_fm:
                segments.append((''.join(current), False))
                current = []
            current_is_fm = True
            current.append(ch)

    if current:
        segments.append((''.join(current), current_is_fm))

    return segments


def convert_unicode_to_fm(text):
    """
    Convert a Sinhala Unicode string to FM-Malithi ASCII-mapped string.

    Args:
        text: Raw Sinhala Unicode string

    Returns:
        FM ASCII string ready for rendering with an FM font
    """
    if not text:
        return text

    s = str(text)

    # ══════════════════════════════════════════════════════════════
    # Escape Latin letters (A-Za-z) to PUA range so they survive
    # the FM conversion and can be rendered with a regular font.
    # ══════════════════════════════════════════════════════════════
    s = _escape_latin(s)

    # ══════════════════════════════════════════════════════════════
    # Strip Zero-Width Joiner/Non-Joiner — Sinhala Unicode uses
    # ZWJ in yansaya (්‍ය) and rakaransaya (්‍ර). Stripping them
    # makes ්ය and ්ර patterns match correctly.
    # ══════════════════════════════════════════════════════════════
    s = s.replace('\u200D', '')  # ZWJ
    s = s.replace('\u200C', '')  # ZWNJ

    # ══════════════════════════════════════════════════════════════
    # Special punctuation pre-processing
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ද්ර', 'ø')
    s = s.replace(',', '\uFFE6')        # ￦ placeholder
    s = s.replace("'", 'z')
    s = s.replace('(', '^')
    s = s.replace(')', '&')
    s = s.replace('%', ']')
    s = s.replace('/', '$')
    s = s.replace('\u2013', '-')         # en-dash → hyphen
    s = s.replace('?', '@')
    s = s.replace('!', '\u00E6')         # æ
    s = s.replace('=', '}')
    s = s.replace('.', "'")
    s = s.replace('+', '\u00AC')         # ¬
    s = s.replace(':', '(')
    s = s.replace('\u00F7', '')          # ÷ → empty
    s = s.replace(';', '\u00A6')         # ¦

    # ══════════════════════════════════════════════════════════════
    # ත්රෛ special
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ත්රෛ', 'ff;%')

    # ══════════════════════════════════════════════════════════════
    # ෛ (ai vowel) conjuncts
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ශෛ', 'ffY')
    s = s.replace('චෛ', 'ffp')
    s = s.replace('ජෛ', 'ffc')
    s = s.replace('කෛ', 'ffl')
    s = s.replace('මෛ', 'ffu')
    s = s.replace('පෛ', 'ffm')
    s = s.replace('දෛ', 'ffo')
    s = s.replace('තෛ', 'ff;')
    s = s.replace('නෛ', 'ffk')
    s = s.replace('ධෛ', 'ffO')
    s = s.replace('වෛ', 'ffj')

    # ══════════════════════════════════════════════════════════════
    # ප්රෞ
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ප්රෞ', 'fm%!')

    # ══════════════════════════════════════════════════════════════
    # ්ය + ෝ (yansaya + oo vowel)
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ෂ්යෝ', 'fIHda')
    s = s.replace('ඡ්යෝ', 'fPHda')
    s = s.replace('ඪ්යෝ', 'fVHda')
    s = s.replace('ඝ්යෝ', 'f>Hda')
    s = s.replace('ඛ්යෝ', 'fLHda')
    s = s.replace('ළ්යෝ', 'f<Hda')
    s = s.replace('ඵ්යෝ', 'fMHda')
    s = s.replace('ඨ්යෝ', 'fGHda')
    s = s.replace('ශ්යෝ', 'fYHda')
    s = s.replace('ක්ෂ්යෝ', 'f\u00CCHda')  # Ì
    s = s.replace('බ්යෝ', 'fnHda')
    s = s.replace('ච්යෝ', 'fpHda')
    s = s.replace('ඩ්යෝ', 'f\u00E2Hda')  # â
    s = s.replace('ෆ්යෝ', 'f*Hda')
    s = s.replace('ග්යෝ', 'f.Hda')
    s = s.replace('ජ්යෝ', 'fcHda')
    s = s.replace('ක්යෝ', 'flHda')
    s = s.replace('ල්යෝ', 'f,Hda')
    s = s.replace('ම්යෝ', 'fuHda')
    s = s.replace('න්යෝ', 'fkHda')
    s = s.replace('ප්යෝ', 'fmHda')
    s = s.replace('ද්යෝ', 'foHda')
    s = s.replace('ස්යෝ', 'fiHda')
    s = s.replace('ට්යෝ', 'fgHda')
    s = s.replace('ව්යෝ', 'fjHda')
    s = s.replace('ත්යෝ', 'f;Hda')
    s = s.replace('භ්යෝ', 'fNHda')
    s = s.replace('ධ්යෝ', 'fOHda')
    s = s.replace('ථ්යෝ', 'f:Hda')

    # ══════════════════════════════════════════════════════════════
    # ්ය + ො (yansaya + o vowel)
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ෂ්යො', 'fIHd')
    s = s.replace('ශ්යො', 'fYHd')
    s = s.replace('ඛ්යො', 'fLHd')
    s = s.replace('ක්ෂ්යො', 'f\u00CCHd')
    s = s.replace('බ්යො', 'fnHd')
    s = s.replace('ව්යො', 'fjHd')
    s = s.replace('ඩ්යො', 'fvHd')
    s = s.replace('ෆ්යො', 'f*Hd')
    s = s.replace('ග්යො', 'f.Hd')
    s = s.replace('ජ්යො', 'fcHd')
    s = s.replace('ක්යො', 'flHd')
    s = s.replace('ම්යො', 'fuHd')
    s = s.replace('ප්යො', 'fmHd')
    s = s.replace('ද්යො', 'foHd')
    s = s.replace('ස්යො', 'fiHd')
    s = s.replace('ට්යො', 'fgHd')
    s = s.replace('ව්යො', 'fjHd')
    s = s.replace('ත්යො', 'f;Hd')
    s = s.replace('භ්යො', 'fNHd')
    s = s.replace('ධ්යො', 'fOHd')
    s = s.replace('ථ්යො', 'f:Hd')

    # ══════════════════════════════════════════════════════════════
    # ්ය + ෙ (yansaya + e vowel)
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ෂ්යෙ', 'fIH')
    s = s.replace('ඡ්යෙ', 'fPH')
    s = s.replace('ළ්යෙ', 'f<H')
    s = s.replace('ණ්යෙ', 'fKH')
    s = s.replace('ච්යෙ', 'fpH')
    s = s.replace('ල්යෙ', 'f,H')
    s = s.replace('න්යෙ', 'fkH')
    s = s.replace('ශ්යෙ', 'fYH')
    s = s.replace('ඛ්යෙ', 'fLH')
    s = s.replace('ක්ෂ්යෙ', 'f\u00CCH')
    s = s.replace('බ්යෙ', 'fnH')
    s = s.replace('ඩ්යෙ', 'fvH')
    s = s.replace('ෆ්යෙ', 'f*H')
    s = s.replace('ග්යෙ', 'f.H')
    s = s.replace('ජ්යෙ', 'fcH')
    s = s.replace('ක්යෙ', 'flH')
    s = s.replace('ම්යෙ', 'fuH')
    s = s.replace('ප්යෙ', 'fmH')
    s = s.replace('ද්යෙ', 'foH')
    s = s.replace('ස්යෙ', 'fiH')
    s = s.replace('ට්යෙ', 'fgH')
    s = s.replace('ව්යෙ', 'fjH')
    s = s.replace('ත්යෙ', 'f;H')
    s = s.replace('භ්යෙ', 'fNH')
    s = s.replace('ධ්යෙ', 'fOH')
    s = s.replace('ථ්යෙ', 'f:H')

    # ══════════════════════════════════════════════════════════════
    # ්ර + ෝ (rakaransaya + oo vowel)
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ෂ්රෝ', 'fI%da')
    s = s.replace('ඝ්රෝ', 'f>%da')
    s = s.replace('ශ්රෝ', 'fY%da')
    s = s.replace('ක්ෂ්රෝ', 'f\u00CC%da')
    s = s.replace('බ්රෝ', 'fn%da')
    s = s.replace('ඩ්රෝ', 'fv%da')
    s = s.replace('ෆ්රෝ', 'f*%da')
    s = s.replace('ග්රෝ', 'f.%da')
    s = s.replace('ක්රෝ', 'fl%da')
    s = s.replace('ප්රෝ', 'fm%da')
    s = s.replace('ද්රෝ', 'f\u00F8da')  # ø
    s = s.replace('ස්රෝ', 'fi%da')
    s = s.replace('ට්රෝ', 'fg%da')
    s = s.replace('ත්රෝ', 'f;%da')

    # ══════════════════════════════════════════════════════════════
    # ්ර + ො (rakaransaya + o vowel)
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ශ්රො', 'fY%d')
    s = s.replace('ඩ්රො', 'fv%d')
    s = s.replace('ෆ්රො', 'f*%d')
    s = s.replace('ග්රො', 'f.%d')
    s = s.replace('ක්රො', 'fl%d')
    s = s.replace('ප්රො', 'fm%d')
    s = s.replace('ද්රො', 'f\u00F8d')
    s = s.replace('ස්රො', 'fi%d')
    s = s.replace('ට්රො', 'fg%d')
    s = s.replace('ත්රො', 'f;%d')

    # ══════════════════════════════════════════════════════════════
    # ්ර + ේ (rakaransaya + ee vowel)
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ශ්රේ', 'fYa%')
    s = s.replace('බ්රේ', 'f\u00ED%')  # í
    s = s.replace('ඩ්රේ', 'f\u00E2%')  # â
    s = s.replace('ෆ්රේ', 'f*a%')
    s = s.replace('ග්රේ', 'f.a%')
    s = s.replace('ක්රේ', 'fla%')
    s = s.replace('ප්රේ', 'fma%')
    s = s.replace('ද්රේ', 'f\u00F8a')  # ø
    s = s.replace('ස්රේ', 'fia%')
    s = s.replace('ත්රේ', 'f;a%')
    s = s.replace('ධ්රේ', 'f\u00E8%')  # è

    # ══════════════════════════════════════════════════════════════
    # ්ර + ෙ (rakaransaya + e vowel)
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ෂ්රෙ', 'fI%')
    s = s.replace('ශ්රෙ', 'fY%')
    s = s.replace('බ්රෙ', 'fn%')
    s = s.replace('ෆ්රෙ', 'f*%')
    s = s.replace('ග්රෙ', 'f.%')
    s = s.replace('ක්රෙ', 'fl%')
    s = s.replace('ප්රෙ', 'fm%')
    s = s.replace('ද්රෙ', 'f\u00F8')
    s = s.replace('ස්රෙ', 'fi%')
    s = s.replace('ත්රෙ', 'f;%')
    s = s.replace('භ්රෙ', 'fN%')
    s = s.replace('ධ්රෙ', 'fO%')

    # ══════════════════════════════════════════════════════════════
    # ්ර + ි (rakaransaya + i vowel)
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ඳ්රි', '\u00A2%')
    s = s.replace('ඨ්රි', '\u00C0%')
    s = s.replace('ඛ්රි', '\u00C5%')
    s = s.replace('ච්රි', '\u00D1%')
    s = s.replace('ඵ්රි', '\u00DD%')
    s = s.replace('ට්රි', '\u00E1%')
    s = s.replace('ඩ්රි', '\u00E4%')
    s = s.replace('ඬ්රි', '\u00E7%')
    s = s.replace('ධ්රි', '\u00EA%')
    s = s.replace('ථ්රි', '\u00D3%')
    s = s.replace('බ්රි', '\u00EC%')
    s = s.replace('ම්රි', '\u00F1%')
    s = s.replace('ඹ්රි', '\u00F4%')
    s = s.replace('ව්රි', '\u00FA%')
    s = s.replace('ඡ්රි', '\u00FD%')
    s = s.replace('ජ්රි', '\u00F0%')
    s = s.replace('්රි', 's%')

    # ══════════════════════════════════════════════════════════════
    # ්ර + ී (rakaransaya + ii vowel)
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ඳ්රී', '\u00A3%')
    s = s.replace('ඨ්රී', '\u00C1%')
    s = s.replace('ච්රී', '\u00D6%')
    s = s.replace('ඵ්රී', '\u00DA%')
    s = s.replace('ට්රී', '\u00E0%')
    s = s.replace('ඩ්රී', '\u00E3%')
    s = s.replace('ඬ්රී', '\u00E9%')
    s = s.replace('ධ්රී', '\u00EB%')
    s = s.replace('ථ්රී', '\u00D3%')
    s = s.replace('බ්රී', '\u00EE%')
    s = s.replace('ම්රී', '\u00F3%')
    s = s.replace('ඹ්රී', '\u00F6%')
    s = s.replace('ව්රී', '\u00F9%')
    s = s.replace('ජ්රී', '\u00D4%')
    s = s.replace('්රී', 'S%')

    # ══════════════════════════════════════════════════════════════
    # Yansaya bare (්ය) and Rakaransaya bare (්ර)
    # ══════════════════════════════════════════════════════════════
    s = s.replace('්ය', 'H')
    s = s.replace('්ර', '%')

    # ══════════════════════════════════════════════════════════════
    # ෞ (au vowel) with consonants
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ෂෞ', 'fI!')
    s = s.replace('ඡෞ', 'fP!')
    s = s.replace('ශෞ', 'fY!')
    s = s.replace('බෞ', 'fn!')
    s = s.replace('චෞ', 'fp!')
    s = s.replace('ඩෞ', 'fv!')
    s = s.replace('ෆෞ', 'f*!')
    s = s.replace('ගෞ', 'f.!')
    s = s.replace('ජෞ', 'fc!')
    s = s.replace('කෞ', 'fl!')
    s = s.replace('ලෞ', 'f,!')
    s = s.replace('මෞ', 'fu!')
    s = s.replace('නෞ', 'fk!')
    s = s.replace('පෞ', 'fm!')
    s = s.replace('දෞ', 'fo!')
    s = s.replace('රෞ', 'fr!')
    s = s.replace('සෞ', 'fi!')
    s = s.replace('ටෞ', 'fg!')
    s = s.replace('තෞ', 'f;!')
    s = s.replace('භෞ', 'fN!')
    s = s.replace('ඤෞ', 'f[!')

    # ══════════════════════════════════════════════════════════════
    # ෝ (oo vowel) with consonants
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ෂෝ', 'fIda')
    s = s.replace('ඹෝ', 'fUda')
    s = s.replace('ඡෝ', 'fPda')
    s = s.replace('ඪෝ', 'fVda')
    s = s.replace('ඝෝ', 'f>da')
    s = s.replace('ඛෝ', 'fLda')
    s = s.replace('ළෝ', 'f<da')
    s = s.replace('ඟෝ', 'f\u00DBda')  # Û
    s = s.replace('ණෝ', 'fKda')
    s = s.replace('ඵෝ', 'fMda')
    s = s.replace('ඨෝ', 'fGda')
    s = s.replace('ඬෝ', 'f~da')
    s = s.replace('ශෝ', 'fYda')
    s = s.replace('ඥෝ', 'f{da')
    s = s.replace('ඳෝ', 'f|da')
    s = s.replace('ක්ෂෝ', 'f\u00CCda')
    s = s.replace('බෝ', 'fnda')
    s = s.replace('චෝ', 'fpda')
    s = s.replace('ඩෝ', 'fvda')
    s = s.replace('ෆෝ', 'f*da')
    s = s.replace('ගෝ', 'f.da')
    s = s.replace('හෝ', 'fyda')
    s = s.replace('ජෝ', 'fcda')
    s = s.replace('කෝ', 'flda')
    s = s.replace('ලෝ', 'f,da')
    s = s.replace('මෝ', 'fuda')
    s = s.replace('නෝ', 'fkda')
    s = s.replace('පෝ', 'fmda')
    s = s.replace('දෝ', 'foda')
    s = s.replace('රෝ', 'frda')
    s = s.replace('සෝ', 'fida')
    s = s.replace('ටෝ', 'fgda')
    s = s.replace('වෝ', 'fjda')
    s = s.replace('තෝ', 'f;da')
    s = s.replace('භෝ', 'fNda')
    s = s.replace('යෝ', 'fhda')
    s = s.replace('ඤෝ', 'f[da')
    s = s.replace('ධෝ', 'fOda')
    s = s.replace('ථෝ', 'f:da')

    # ══════════════════════════════════════════════════════════════
    # ො (o vowel) with consonants
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ෂො', 'fId')
    s = s.replace('ඹො', 'fUd')
    s = s.replace('ඡො', 'fPd')
    s = s.replace('ඪො', 'fVd')
    s = s.replace('ඝො', 'f>d')
    s = s.replace('ඛො', 'fLd')
    s = s.replace('ළො', 'f<d')
    s = s.replace('ඟො', 'f\u00D5d')  # Õ
    s = s.replace('ණො', 'fKd')
    s = s.replace('ඵො', 'fMd')
    s = s.replace('ඨො', 'fGd')
    s = s.replace('ඬො', 'f~da')
    s = s.replace('ශො', 'fYd')
    s = s.replace('ඥො', 'f{d')
    s = s.replace('ඳො', 'f|d')
    s = s.replace('ක්ෂො', 'f\u00CCd')
    s = s.replace('බො', 'fnd')
    s = s.replace('චො', 'fpd')
    s = s.replace('ඩො', 'fvd')
    s = s.replace('ෆො', 'f*d')
    s = s.replace('ගො', 'f.d')
    s = s.replace('හො', 'fyd')
    s = s.replace('ජො', 'fcd')
    s = s.replace('කො', 'fld')
    s = s.replace('ලො', 'f,d')
    s = s.replace('මො', 'fud')
    s = s.replace('නො', 'fkd')
    s = s.replace('පො', 'fmd')
    s = s.replace('දො', 'fod')
    s = s.replace('රො', 'frd')
    s = s.replace('සො', 'fid')
    s = s.replace('ටො', 'fgd')
    s = s.replace('වො', 'fjd')
    s = s.replace('තො', 'f;d')
    s = s.replace('භො', 'fNd')
    s = s.replace('යො', 'fhd')
    s = s.replace('ඤො', 'f[d')
    s = s.replace('ධො', 'fOd')
    s = s.replace('ථො', 'f:d')

    # ══════════════════════════════════════════════════════════════
    # ේ (ee vowel) with consonants
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ෂේ', 'fIa')
    s = s.replace('ඹේ', 'f\u00F2')   # ò
    s = s.replace('ඡේ', 'f\u00FE')   # þ
    s = s.replace('ඪේ', 'f\\a')
    s = s.replace('ඝේ', 'f>a')
    s = s.replace('ඛේ', 'f\u00C4')   # Ä
    s = s.replace('ළේ', 'f<a')
    s = s.replace('ගේ', 'f.a')
    s = s.replace('ඟේ', 'f\u00D5a')  # Õ
    s = s.replace('ණේ', 'fKa')
    s = s.replace('ඵේ', 'fMa')
    s = s.replace('ඨේ', 'fGa')
    s = s.replace('ඬේ', 'f\u00E5')   # å
    s = s.replace('ශේ', 'fYa')
    s = s.replace('ඥේ', 'f{a')
    s = s.replace('ඳේ', 'f|a')
    s = s.replace('ක්ෂේ', 'f\u00CCa')
    s = s.replace('බේ', 'f\u00ED')    # í
    s = s.replace('චේ', 'f\u00C9')    # É
    s = s.replace('ඩේ', 'f\u00E2')    # â
    s = s.replace('ෆේ', 'f*')
    s = s.replace('හේ', 'fya')
    s = s.replace('පේ', 'fma')
    s = s.replace('කේ', 'fla')
    s = s.replace('ලේ', 'f,a')
    s = s.replace('මේ', 'f\u00EF')    # ï
    s = s.replace('නේ', 'fka')
    s = s.replace('ජේ', 'f\u00CA')    # Ê
    s = s.replace('දේ', 'foa')
    s = s.replace('රේ', 'f\u00BE')    # ¾
    s = s.replace('සේ', 'fia')
    s = s.replace('ටේ', 'f\u00DC')    # Ü
    s = s.replace('වේ', 'f\u00F5')    # õ
    s = s.replace('තේ', 'f;a')
    s = s.replace('භේ', 'fNa')
    s = s.replace('යේ', 'fha')
    s = s.replace('ඤේ', 'f[a')
    s = s.replace('ධේ', 'f\u00E8')    # è
    s = s.replace('ථේ', 'f:a')

    # ══════════════════════════════════════════════════════════════
    # ෙ (e vowel) with consonants
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ෂෙ', 'fI')
    s = s.replace('ඹෙ', 'fU')
    s = s.replace('ඓ', 'ft')
    s = s.replace('ඡෙ', 'fP')
    s = s.replace('ඪෙ', 'fV')
    s = s.replace('ඝෙ', 'f>')
    s = s.replace('ඛෙ', 'fn')
    s = s.replace('ළෙ', 'f<')
    s = s.replace('ඟෙ', 'f\u00DB')    # Û
    s = s.replace('ණෙ', 'fK')
    s = s.replace('ඵෙ', 'fM')
    s = s.replace('ඨෙ', 'fG')
    s = s.replace('ඬෙ', 'f~')
    s = s.replace('ශෙ', 'fY')
    s = s.replace('ඥෙ', 'f{')
    s = s.replace('ඳෙ', 'f\u00CB')    # Ë
    s = s.replace('ක්ෂෙ', 'f\u00CC')  # Ì
    s = s.replace('බෙ', 'fn')
    s = s.replace('චෙ', 'fp')
    s = s.replace('ඩෙ', 'fv')
    s = s.replace('ෆෙ', 'f*')
    s = s.replace('ගෙ', 'f.')
    s = s.replace('හෙ', 'fy')
    s = s.replace('ජෙ', 'fc')
    s = s.replace('කෙ', 'fl')
    s = s.replace('ලෙ', 'f,')
    s = s.replace('මෙ', 'fu')
    s = s.replace('නෙ', 'fk')
    s = s.replace('පෙ', 'fm')
    s = s.replace('දෙ', 'fo')
    s = s.replace('රෙ', 'fr')
    s = s.replace('සෙ', 'fi')
    s = s.replace('ටෙ', 'fg')
    s = s.replace('වෙ', 'fj')
    s = s.replace('තෙ', 'f;')
    s = s.replace('භෙ', 'fN')
    s = s.replace('යෙ', 'fh')
    s = s.replace('ඤෙ', 'f[')
    s = s.replace('ධෙ', 'fO')
    s = s.replace('ථෙ', 'f:')

    # ══════════════════════════════════════════════════════════════
    # u/uu vowel special cases for common consonants
    # ══════════════════════════════════════════════════════════════
    s = s.replace('තු', ';=')
    s = s.replace('ශු', 'Y=')
    s = s.replace('භු', 'N=')
    s = s.replace('ගු', '.=')
    s = s.replace('කු', 'l=')
    s = s.replace('තූ', ';+')
    s = s.replace('ශූ', 'Y+')
    s = s.replace('භූ', 'N+')
    s = s.replace('ගූ', '.+')
    s = s.replace('කූ', 'l+')
    s = s.replace('රු', 're')
    s = s.replace('රූ', 'rE')

    # ══════════════════════════════════════════════════════════════
    # Standalone vowels
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ආ', 'wd')
    s = s.replace('ඇ', 'we')
    s = s.replace('ඈ', 'wE')
    s = s.replace('ඌ', 'W!')
    s = s.replace('ඖ', 'T!')
    s = s.replace('ඒ', 'ta')
    s = s.replace('ඕ', '\u00B4')       # ´

    # ══════════════════════════════════════════════════════════════
    # Special conjunct characters
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ඳි', '\u00A2')      # ¢
    s = s.replace('ඳී', '\u00A3')      # £
    s = s.replace('දූ', '\u00A5')      # ¥
    s = s.replace('දී', '\u00A7')      # §
    s = s.replace('ලූ', '\u00C6')      # Æ
    s = s.replace('ර්ය', '\u00A9')     # ©
    s = s.replace('ඳූ', '\u00AA')      # ª
    s = s.replace('ර්', '\u00BE')      # ¾
    s = s.replace('ඨි', '\u00C0')      # À
    s = s.replace('ඨී', '\u00C1')      # Á
    s = s.replace('ඡී', '\u00C2')      # Â
    s = s.replace('ඛ්', '\u00C4')      # Ä
    s = s.replace('ඛි', '\u00C5')      # Å
    s = s.replace('ලු', '\u00A8')      # ¨
    s = s.replace('ඛී', '\u00C7')      # Ç
    s = s.replace('දි', '\u00C8')      # È
    s = s.replace('ච්', '\u00C9')      # É
    s = s.replace('ජ්', '\u00CA')      # Ê
    s = s.replace('රී', '\u00CD')      # Í
    s = s.replace('ඪී', '\u00CE')      # Î
    s = s.replace('ඪී', '\u00D0,')     # Ð,
    s = s.replace('චි', '\u00D1')      # Ñ
    s = s.replace('ථී', '\u00D2')      # Ò
    s = s.replace('ථී', '\u00D3')      # Ó
    s = s.replace('ජී', '\u00D4')      # Ô
    s = s.replace('චී', '\u00D6')      # Ö
    s = s.replace('ඞ්', '\u00D9')      # Ù
    s = s.replace('ඵී', '\u00DA')      # Ú
    s = s.replace('ට්', '\u00DC')      # Ü
    s = s.replace('ඵි', '\u00DD')      # Ý
    s = s.replace('රි', '\u00DF')      # ß
    s = s.replace('ටී', '\u00E0')      # à
    s = s.replace('ටි', '\u00E1')      # á
    s = s.replace('ඩ්', '\u00E2')      # â
    s = s.replace('ඩී', '\u00E3')      # ã
    s = s.replace('ඩි', '\u00E4')      # ä
    s = s.replace('ඬ්', '\u00E5')      # å
    s = s.replace('ඬි', '\u00E7')      # ç
    s = s.replace('ධ්', '\u00E8')      # è
    s = s.replace('ඬී', '\u00E9')      # é
    s = s.replace('ධි', '\u00EA')      # ê
    s = s.replace('ධී', '\u00EB')      # ë
    s = s.replace('ථි', '\u00D3')      # Ó
    s = s.replace('බි', '\u00EC')      # ì
    s = s.replace('බ්', '\u00ED')      # í
    s = s.replace('බී', '\u00EE')      # î
    s = s.replace('ම්', '\u00EF')      # ï
    s = s.replace('ජි', '\u00F0')      # ð
    s = s.replace('මි', '\u00F1')      # ñ
    s = s.replace('ඹ්', '\u00F2')      # ò
    s = s.replace('මී', '\u00F3')      # ó
    s = s.replace('ඹි', '\u00F4')      # ô
    s = s.replace('ව්', '\u00F5')      # õ
    s = s.replace('ඹී', '\u00F6')      # ö
    s = s.replace('ඳු', '\u00F7')      # ÷
    s = s.replace('වී', '\u00F9')      # ù
    s = s.replace('ඟු', '\u00D5=')     # Õ=
    s = s.replace('වි', '\u00FA')      # ú
    s = s.replace('ඞ්', '\u00FB')      # û
    s = s.replace('ඞී', '\u00FC')      # ü
    s = s.replace('ඡි', '\u00FD')      # ý
    s = s.replace('ඡ්', '\u00FE')      # þ
    s = s.replace('දු', '\u00FF')      # ÿ
    s = s.replace('ර්ණ', '\u201C')     # "
    s = s.replace('ණී', '\u0152')      # Œ
    s = s.replace('ණි', '\u201A')      # ‚

    # ══════════════════════════════════════════════════════════════
    # Rare/extra mappings
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ජී', '\u00D4')      # Ô
    s = s.replace('ඡි', '\u00F0')      # ð
    s = s.replace('ඩි', '\u00E4')      # ä
    s = s.replace('ඤු', '\u00FB')      # û

    # NOTE: ැ and ෑ are right-side vowels in FM fonts.
    # They go AFTER the consonant char (e.g. කැ = l+e, නෑ = k+E).
    # The standalone fallbacks ැ→e and ෑ→E in the vowel diacritics
    # section below handle this correctly — no combos needed.

    # ══════════════════════════════════════════════════════════════
    # Base consonants (MUST come AFTER all conjunct/vowel combos)
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ග', '.')
    s = s.replace('ළු', '\u00BF')      # ¿
    s = s.replace('ෂ', 'I')
    s = s.replace('ං', 'x')
    s = s.replace('ඃ', '#')
    s = s.replace('ඹ', 'U')
    s = s.replace('ඡ', 'P')
    s = s.replace('ඪ', 'V')
    s = s.replace('ඝ', '>')
    s = s.replace('ඊ', 'B')
    s = s.replace('ඣ', 'CO')
    s = s.replace('ඛ', 'L')
    s = s.replace('ළ', '<')
    s = s.replace('ඟ', '\u00D5')       # Õ
    s = s.replace('ණ', 'K')
    s = s.replace('ඵ', 'M')
    s = s.replace('ඨ', 'G')
    s = s.replace('ෆ', '*')
    s = s.replace('ල', ',')
    s = s.replace('රැ', '/')
    s = s.replace('ථ', ':')
    s = s.replace('ත', ';')
    s = s.replace('රෑ', '?')
    # NOTE: ක→C, ෑ→E, ත→F, න→J removed — they were wrong duplicates
    # that shadowed the correct lowercase mappings (ක→l, න→k) below.
    # In FM Ganganee, uppercase J ≠ න (it maps to a different glyph).
    s = s.replace('ෘ', 'D')
    s = s.replace('ඬ', '~')
    s = s.replace('භ', 'N')
    s = s.replace('ධ', 'O')
    s = s.replace('ඍ', 'R')
    s = s.replace('ඔ', 'T')
    s = s.replace('ඪ', 'V')
    s = s.replace('උ', 'W')
    s = s.replace('ශ', 'Y')
    s = s.replace('ඤ', '[')
    s = s.replace('ඉ', 'b')
    s = s.replace('ජ', 'c')
    s = s.replace('ට', 'g')
    s = s.replace('ය', 'h')
    s = s.replace('ස', 'i')
    s = s.replace('ව', 'j')
    s = s.replace('න', 'k')
    s = s.replace('ක', 'l')
    s = s.replace('ප', 'm')
    s = s.replace('බ', 'n')
    s = s.replace('ද', 'o')
    s = s.replace('ච', 'p')
    s = s.replace('ර', 'r')
    s = s.replace('එ', 't')
    s = s.replace('ම', 'u')
    s = s.replace('ඩ', 'v')
    s = s.replace('අ', 'w')
    s = s.replace('හ', 'y')
    s = s.replace('ඥ', '{')
    s = s.replace('ඳ', '|')
    s = s.replace('ක්ෂ', '\u00CC')     # Ì

    # ══════════════════════════════════════════════════════════════
    # Vowel diacritics (standalone, after base consonants)
    # ══════════════════════════════════════════════════════════════
    s = s.replace('ැ', 'e')
    s = s.replace('ෑ', 'E')
    s = s.replace('ෙ', 'f')
    s = s.replace('ු', 'q')
    s = s.replace('ි', 's')
    s = s.replace('ූ', 'Q')
    s = s.replace('ී', 'S')
    s = s.replace('ෘ', 'D')
    s = s.replace('ෲ', 'DD')
    s = s.replace('ෟ', '!')
    s = s.replace('ා', 'd')
    s = s.replace('්', 'a')

    # ══════════════════════════════════════════════════════════════
    # Post-processing: restore pre-escaped punctuation
    # ══════════════════════════════════════════════════════════════
    s = s.replace('\uFFE6', '"')        # ￦ → "
    s = s.replace('\u2018', 'z')        # ' → z
    s = s.replace('\uFFEB', '^')        # ￫ → ^
    s = s.replace('\uFFE9', '&')        # ￩ → &
    s = s.replace('\uFFD4', ')')        # ￔ → )
    s = s.replace('\uFFD3', '@')        # ￓ → @
    s = s.replace('\uFFD2', '`')        # ￒ → `
    s = s.replace('\uFFCF', '}')        # ￏ → }
    s = s.replace('\uFFCE', "'")        # ￎ → '
    s = s.replace('\uFFCD', '\u00A4')   # ￍ → ¤
    s = s.replace('\uFFCC', '\u2022')   # ￌ → •
    s = s.replace('\uFFCA', '\u203A')   # ￊ → ›
    s = s.replace('\uFEB6', '\u2219')   # ﾶ → ∙
    s = s.replace('\uFFD5', ']')        # ￕ → ]
    s = s.replace('\u201C', '\u2014')   # " → —
    s = s.replace('\u201D', '\u02DC')   # " → ˜

    return s
