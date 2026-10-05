# -*- coding: utf-8 -*-
"""
Regression test for utils/fm_converter.py against a golden corpus.

    py -3 fm_regress.py            compare current converter against golden_corpus.tsv
    py -3 fm_regress.py --update   rewrite the golden file from the current converter
                                   (do this ONLY after a change has been verified
                                   visually — see verification.md)

The corpus is every word that has ever had a bug filed against it, plus everyday
newsroom vocabulary. A change that touches anything here needs an explanation.

Run from HiruTaglineCreator/:
    PYTHONIOENCODING=utf-8 py -3 ../claude-code-skills/sinhala-fm-converter/scripts/fm_regress.py
"""
import os
import sys

sys.path.insert(0, __file__.rsplit('\\', 1)[0].rsplit('/', 1)[0])
from _common import setup_stdout, converter_path, load, leaks   # noqa: E402

setup_stdout()
HERE = os.path.dirname(os.path.abspath(__file__))
GOLDEN = os.path.join(HERE, 'golden_corpus.tsv')
MOD = load(converter_path())
CONV = MOD.convert_unicode_to_fm

# No ZWJ → no ligature. Output must contain neither '%' (rakaransaya) nor 'H' (yansaya).
SUPPRESS = [
    'පොල්යාය', 'මල්යහන', 'පස්යාල', 'පාසල්යන', 'හිස්යාම', 'ගල්යාය', 'වෙල්යාය', 'මල්යාය',
    'පොත්රාක්කය', 'මල්රේණු', 'රන්රස', 'ගස්රිකිලි', 'බස්රිය', 'අත්රෙදි', 'අත්රෝදය',
    'කාසල්රි', 'ගම්රට', 'බස්රථය', 'දුම්රිය',
]

# ZWJ present → the ligature must survive ('%' or 'H', or a fused glyph like ø for ද්‍ර).
PRESERVE = [
    'මෙට්‍රික්', 'ශ්‍රේෂ්ඨාධිකරණය', 'ක්‍රීඩාව', 'ශක්‍ය', 'වාක්‍ය', 'ශ්‍රී ලංකා',
    'අත්‍යන්ත්‍ර', 'ක්‍රි', 'ප්‍රවෘත්ති', 'ත්‍රෛමාසික', 'ප්‍රෞඪ',
]

CORPUS = SUPPRESS + PRESERVE + [
    # ── ර්‍ය is house-style exempt: ZWJ present but never a ligature ──
    'ආර්‍යාව',
    # ── words with a dedicated fix behind them ──
    'හඳෙන්', 'ඕස්ට්‍රේලියාව',
    # ── ද්‍ර family (fixed 2026-09-23) ──
    'ද්‍රෝහීයා', 'ද්‍රෝහී', 'මහද්‍රෝහී', 'ද්‍රෝණ', 'ද්‍රෝහය', 'ද්‍රවය', 'ද්‍රාවණය',
    'ද්‍රවිඩ', 'ද්‍රේවා', 'ද්‍රැවිඩ',
    # ── everyday newsroom vocabulary ──
    'ජනාධිපති', 'අගමැති', 'පාර්ලිමේන්තුව', 'මැතිවරණය', 'අධිකරණය', 'පොලිසිය', 'රජය',
    'විරෝධතාව', 'ගිනිගැනීම', 'අනතුර', 'මරණ', 'රෝහල', 'සෞඛ්‍ය', 'අධ්‍යාපන', 'ආර්ථික',
    'විදේශ', 'ක්‍රීඩා', 'කෝටි', 'දෙමළ', 'සිංහල', 'මුස්ලිම්', 'කොළඹ', 'යාපනය', 'මහනුවර',
    'ගාල්ල', 'ත්‍රිකුණාමලය', 'අම්පාර', 'හදිසි ප්‍රවෘත්තිය', 'කාලගුණය', 'ගුවන් තොටුපළ',
    # ── mixed Sinhala + English (Latin must survive) ──
    'ජනාධිපති BREAKING', 'COVID රෝගීන්',
] + [
    # ── quote marks must be drawn in Arial, never FM (fixed 2026-10-05) ──
    "'ද්‍රෝහියා'", '"සෛල"', '“ද්‍රෝහියා”', '‘සෛල’', "රට's",
]

QUOTES = set('\'"‘’“”')

if '--update' in sys.argv:
    with open(GOLDEN, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# word\texpected FM output — regenerate with fm_regress.py --update\n')
        for w in CORPUS:
            fh.write('%s\t%s\n' % (w, CONV(w)))
    print('golden corpus written: %s (%d words)' % (GOLDEN, len(CORPUS)))
    raise SystemExit(0)

if not os.path.isfile(GOLDEN):
    raise SystemExit('no golden_corpus.tsv — run with --update first')

expected = {}
for line in open(GOLDEN, encoding='utf-8'):
    if line.startswith('#') or not line.strip():
        continue
    w, _, fm = line.rstrip('\n').partition('\t')
    expected[w] = fm

fails = missing = 0
for w in CORPUS:
    got = CONV(w)
    if w not in expected:
        missing += 1
        print('NEW      %-20s -> %r   (not in golden file)' % (w, got))
        continue
    if got != expected[w]:
        fails += 1
        print('CHANGED  %-20s golden=%-18r now=%-18r' % (w, expected[w], got))
    if leaks(got):
        fails += 1
        print('LEAK     %-20s -> %r   leftover %s' % (w, got, leaks(got)))

# ── invariants the golden file cannot vouch for ────────────────────────────────
for w in SUPPRESS:
    out = CONV(w)
    for glyph, what in (('%', 'rakaransaya'), ('H', 'yansaya')):
        if glyph in out:
            fails += 1
            print('LIGATURE %-20s -> %r   has %s but the word has no ZWJ' % (w, out, what))

for w in PRESERVE:
    out = CONV(w)
    if not any(g in out for g in ('%', 'H', 'ø')):
        fails += 1
        print('LOST     %-20s -> %r   ZWJ ligature disappeared' % (w, out))

for w in CORPUS:
    for seg, is_fm in MOD.split_fm_and_english(CONV(w)):
        if is_fm and QUOTES & set(seg):
            fails += 1
            print('FM QUOTE %-20s segment %r would draw a quote in the FM font' % (w, seg))

print()
print('%d words · %d changed/leaking · %d not yet in golden file' % (len(CORPUS), fails, missing))
print('PASS' if fails == 0 else 'FAIL — explain every change before shipping')
sys.exit(1 if fails else 0)
