import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.text_renderer import TextRenderer

def test():
    renderer = TextRenderer({})

    print("\n--- Topic Bed ---")
    topic_config = {'x': 50, 'y': 50, 'width': 1000, 'height': 80, 'bg_color': '#a70003', 'text_color': '#FFFFFF'}
    # "හරසරින් පිළිගත් චීන අවුරුද්ද"
    topic_text = "හරසරින් පිළිගත් චීන අවුරුද්ද"
    img1 = renderer.render_topic_bed(topic_text, topic_config, letter_spacing=10) # 10 should be ignored
    img1.save("test_topic.png")

    print("\n--- Tag Bed ---")
    tag_config = {'x': 50, 'y': 150, 'width': 1800, 'height': 100, 'text_color': '#000000'}
    # "තරුණ වරදකරුවන්ගේ අභ්‍යාස විද්‍යාලයේ සිසුන් විභාගයට පෙනී සිටියා"
    tag_text = "තරුණ වරදකරුවන්ගේ අභ්‍යාස විද්‍යාලයේ සිසුන් විභාගයට පෙනී සිටියා"
    img2 = renderer.render_tag_bed_text(tag_text, tag_config, h_scale=100, letter_spacing=0)
    img2.save("test_tag.png")

    print("\n--- White Bed ---")
    white_config = {'x': 50, 'y': 300, 'width': 1800, 'height': 80, 'text_color': '#000000'}
    # "සියල්ල සිදුවන්නේ අදාළ ප්‍රකාශයෙන් පස්සේ"
    white_text = "සියල්ල සිදුවන්නේ අදාළ ප්‍රකාශයෙන් පස්සේ"
    img3 = renderer.render_white_bed_text(white_text, white_config, h_scale=50, letter_spacing=10) # should ignore
    img3.save("test_white.png")

    print("Success. Saved test_topic.png, test_tag.png, test_white.png")

if __name__ == '__main__':
    test()
