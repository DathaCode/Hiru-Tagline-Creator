from core.text_renderer import TextRenderer
from utils.fm_converter import convert_unicode_to_fm

tr = TextRenderer({})

test_words = ['මෙට්රික්', 'ශ්රේෂ්ඨාධිකරණය', 'ක්රි']
print('FM Conversion:')
for w in test_words:
    print(f'{w} -> {convert_unicode_to_fm(w)}')

bed = {'width_min': 485, 'width_max': 1780, 'bg_color': '#a70003', 'text_color': '#FFFFFF', 'x': 126, 'y': 754, 'height': 60}
img = tr.render_topic_bed('මෙට්රික් ශ්රේෂ්ඨාධිකරණය', bed)
tr.save_png(img, 'test_topic_rakar.png')
