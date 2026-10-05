"""Check FM font glyph coverage for Sinhala Unicode."""
from fonttools import ttLib
import sys

paths = {
    'FM GANGANEE':   r'C:\Users\Hp\AppData\Local\Microsoft\Windows\Fonts\FMGanganee x.ttf',
    'FM SANDHYANEE': r'C:\Users\Hp\AppData\Local\Microsoft\Windows\Fonts\FMSandhyanee x.ttf',
}

for name, path in paths.items():
    print(f'\n--- {name} ---')
    tt = ttLib.TTFont(path)
    cm = tt.getBestCmap()
    si = [(cp, g) for cp, g in cm.items() if 0x0D80 <= cp <= 0x0DFF]
    print(f'  Sinhala Unicode glyphs: {len(si)}')
    if si:
        print('  Sample:', si[:5])
    first = sorted(cm.keys())[:20]
    print('  First 20 codepoints:')
    for cp in first:
        print(f'    U+{cp:04X}  {repr(chr(cp))}  -> {cm[cp]}')
