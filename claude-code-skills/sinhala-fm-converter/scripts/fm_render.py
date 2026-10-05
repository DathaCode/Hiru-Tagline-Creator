# -*- coding: utf-8 -*-
"""
Render words in the real FM font so a human (or Claude, by reading the PNG) can look
at them. Byte-correct output is not proof — this is the final check.

    py -3 fm_render.py ද්‍රෝහීයා ඕස්ට්‍රේලියාව
    py -3 fm_render.py --compare utils/fm_converter.py.bak ද්‍රෝහීයා

--compare renders a second column using another copy of the converter (a .bak, or the
copy in award_submission_2026/HiruTaglineCreator_v3.1_src/), which is how a before/after is demonstrated.

Output: fm_render.png next to this script, on the tag-bed orange (#ffaa3a).

Run from HiruTaglineCreator/:
    PYTHONIOENCODING=utf-8 py -3 ../claude-code-skills/sinhala-fm-converter/scripts/fm_render.py <words>
"""
import os
import sys

sys.path.insert(0, __file__.rsplit('\\', 1)[0].rsplit('/', 1)[0])
from _common import setup_stdout, converter_path, load           # noqa: E402
from PIL import Image, ImageDraw, ImageFont                      # noqa: E402

setup_stdout()
HERE = os.path.dirname(os.path.abspath(__file__))

FM_FONT = r'C:\Users\Hp\AppData\Local\Microsoft\Windows\Fonts\FMSandhyanee x.ttf'
if not os.path.isfile(FM_FONT):                      # FM GANGANEE is the TOPIC bed font
    FM_FONT = FM_FONT.replace('FMSandhyanee', 'FMGanganee')

args = sys.argv[1:]
other = None
if args and args[0] == '--compare':
    other = load(args[1], 'othconv').convert_unicode_to_fm
    args = args[2:]
if not args:
    args = ['ද්‍රෝහීයා', 'ඕස්ට්‍රේලියාව', 'හඳෙන්', 'ශ්‍රී ලංකා']

conv = load(converter_path()).convert_unicode_to_fm
fm = ImageFont.truetype(FM_FONT, 58)
lab = ImageFont.truetype('arial.ttf', 20)

width = 1500 if other else 1000
img = Image.new('RGB', (width, 110 + 95 * len(args)), '#ffaa3a')
d = ImageDraw.Draw(img)
d.text((30, 25), os.path.basename(FM_FONT) + ('   left: other copy   right: current'
                                              if other else '   current converter'),
       font=lab, fill='black')
y = 75
for w in args:
    d.text((30, y + 20), w, font=lab, fill='#553300')
    if other:
        d.text((250, y), other(w), font=fm, fill='black')
        d.text((870, y), conv(w), font=fm, fill='black')
    else:
        d.text((250, y), conv(w), font=fm, fill='black')
    print('%-20s -> %r' % (w, conv(w)))
    y += 95

out = os.path.join(HERE, 'fm_render.png')
img.save(out)
print('\nsaved %s — now LOOK at it' % out)
