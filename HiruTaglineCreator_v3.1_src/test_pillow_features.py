"""
Test if Pillow has text shaping support for Sinhala
"""
from PIL import Image, ImageDraw, ImageFont, features
import os

print("="*70)
print("PILLOW FEATURE DETECTION")
print("="*70)

print(f"\nRaqm (text shaping): {features.check('raqm')}")
print(f"FreeType: {features.check('freetype2')}")
print(f"WebP: {features.check('webp')}")

print("\n" + "="*70)
print("FONT RENDERING TEST")
print("="*70)

font_paths = {
    'FM GANGANEE':   r"C:\Users\Hp\AppData\Local\Microsoft\Windows\Fonts\FMGanganee x.ttf",
    'FM SANDHYANEE': r"C:\Users\Hp\AppData\Local\Microsoft\Windows\Fonts\FMSandhyanee x.ttf",
}

test_texts = [
    ("සිංහල",              "Simple Sinhala"),
    ("ප්‍රධානීගේ",          "Complex Sinhala with ZWJ"),
    ("2024 IMF ණය ගිවිසුම", "Mixed English + Sinhala"),
]

for fname, fpath in font_paths.items():
    print(f"\n--- {fname} ---")
    if not os.path.exists(fpath):
        print(f"  ✗ NOT FOUND: {fpath}")
        continue
    print(f"  ✓ Found: {fpath}")

    for i, (text, desc) in enumerate(test_texts):
        try:
            img  = Image.new('RGB', (900, 150), 'white')
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(fpath, 60)
            draw.text((20, 40), text, font=font, fill='black')
            out = f"test_{fname.replace(' ','_')}_{i+1}.png"
            img.save(out)
            bbox = font.getbbox(text)
            print(f"  [{i+1}] {desc} → saved {out}  (width={bbox[2]-bbox[0]}px)")
        except Exception as e:
            print(f"  [{i+1}] {desc} → ERROR: {e}")

print("\n" + "="*70)
print("Open the generated PNGs.  If they show boxes = Pillow cannot render Sinhala.")
print("="*70)
