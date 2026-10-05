# -*- coding: utf-8 -*-
"""
Static audit of utils/fm_converter.py.

Two checks, both of which have caught real bugs:

  1. SHADOWED RULES — a s.replace() whose pattern an earlier replace has already
     consumed, so it can never fire. This is how the ද්‍රෝ bug was found: the bare
     'ද්‍ර'→'ø' rule sat above the four 'ද්‍ර'+vowel rules and killed all of them.

  2. LEAKING COMBINATIONS — consonant x vowel x (plain|rakaransaya|yansaya) pairs whose
     output still contains a Sinhala codepoint. FM fonts have no glyph in U+0D80–U+0DFF,
     so anything reported here renders as a blank box in the app.

Run from HiruTaglineCreator/:
    PYTHONIOENCODING=utf-8 py -3 ../claude-code-skills/sinhala-fm-converter/scripts/fm_audit.py
"""
import ast
import sys
from collections import defaultdict

sys.path.insert(0, __file__.rsplit('\\', 1)[0].rsplit('/', 1)[0])
from _common import setup_stdout, converter_path, load, leaks   # noqa: E402

setup_stdout()
PATH = converter_path()
CONV = load(PATH).convert_unicode_to_fm

IS_SINHALA = lambda t: any(0x0D80 <= ord(c) <= 0x0DFF for c in t)   # noqa: E731

# ── 1. shadowed rules ─────────────────────────────────────────────────────────
rules = []
for node in ast.walk(ast.parse(open(PATH, encoding='utf-8').read())):
    if (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute)
            and node.value.func.attr == 'replace' and len(node.value.args) == 2):
        try:
            rules.append((node.lineno,
                          ast.literal_eval(node.value.args[0]),
                          ast.literal_eval(node.value.args[1])))
        except ValueError:
            pass
rules.sort()

shadowed = []
for i, (ln, pat, rep) in enumerate(rules):
    if not IS_SINHALA(pat):
        continue
    probe = pat
    for _, p2, r2 in rules[:i]:
        probe = probe.replace(p2, r2)
    if probe != pat:
        shadowed.append((ln, pat, rep, probe))

print('converter    : %s' % PATH)
print('replace rules: %d' % len(rules))
print()
print('── shadowed rules (%d) ───────────────────────────────────────' % len(shadowed))
for ln, pat, rep, probe in shadowed:
    print('  line %-4d %-14r -> %-12r   input already became %r' % (ln, pat, rep, probe))
if not shadowed:
    print('  none')

# ── 2. leaking combinations ───────────────────────────────────────────────────
CONS = 'කඛගඝඞචඡජඣඤටඨඩඪණතථදධනපඵබභමඹයරලවශෂසහළෆඟඬඳ'
VOW = ['', 'ා', 'ැ', 'ෑ', 'ි', 'ී', 'ු', 'ූ', 'ෘ', 'ෙ', 'ේ', 'ෛ', 'ො', 'ෝ', 'ෞ', '්']
JOIN = (('', 'plain'), ('්‍ර', 'rakar'), ('්‍ය', 'yansa'))

bad = defaultdict(list)
total = 0
for c in CONS:
    for v in VOW:
        for mid, name in JOIN:
            total += 1
            w = c + mid + v
            L = leaks(CONV(w))
            if L:
                bad[(name, ''.join(L))].append(w)

n = sum(len(v) for v in bad.values())
print()
print('── leaking combinations (%d of %d) ──────────────────────────' % (n, total))
for (name, L), ws in sorted(bad.items()):
    print('  %-6s leftover %-6r %3d cases: %s' % (name, L, len(ws), ' '.join(ws[:25])))
if not bad:
    print('  none')
print()
print('Expected baseline on 2026-09-23: 19 shadowed, 44 leaking (all ඞ).')
print('Anything beyond that is new — see SKILL.md "Known gaps".')
