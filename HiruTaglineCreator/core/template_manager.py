import os
from PIL import Image

# ─── Bed coordinates measured directly from template pixel data ────────────────
#
# MAIN_TAG layout (1920×1080):
#   RED bar   (Topic Bed bg): x=126, y=754, extends rightward, height=60
#   ORANGE    (TAG Bed):      x=140, y=814, width=1459, height=44
#   WHITE     (White Bed):    x=141, y=898, width=1457, height=48
#
# SUB_TAG layout (1920×1080):
#   RED bar   (topic line):   x=126, y=754, extends rightward, height=60
#   ORANGE 1  (TAG Bed):      x=140, y=814, width=1459, height=44
#   ORANGE 2  (White Bed):    x=140, y=907, width=1459, height=48

MAIN_TAG_BEDS = {
    'TOPIC_BED': {
        'x': 126,
        'y': 754,
        'width_min': 485,       # minimum width (matches existing red bar)
        'width_max': 1780,      # max allowed width
        'height': 60,
        'bg_color':   '#a70003',
        'text_color': '#FFFFFF',
        'font': 'FM GANGANEE',
        'alignment': 'center',
        'expand_mode': 'rightward'
    },
    'TAG_BED': {
        'x': 140,
        'y': 814,
        'width': 1459,
        'height': 44,
        'text_color': '#000000',
        'font': 'FM SANDHYANEE',
        'alignment': 'center'
    },
    'WHITE_BED': {
        'x': 141,
        'y': 898,
        'width': 1457,
        'height': 48,
        'text_color': '#000000',
        'font': 'FM SANDHYANEE',
        'alignment': 'center'
    }
}

SUB_TAG_BEDS = {
    'TOPIC_BED': {
        'x': 126,
        'y': 754,
        'width_min': 485,
        'width_max': 1780,
        'height': 60,
        'bg_color':   '#a70003',
        'text_color': '#FFFFFF',
        'font': 'FM GANGANEE',
        'alignment': 'center',
        'expand_mode': 'rightward'
    },
    'TAG_BED': {
        'x': 140,
        'y': 814,
        'width': 1459,
        'height': 44,
        'text_color': '#000000',
        'font': 'FM SANDHYANEE',
        'alignment': 'center'
    }
    # Note: SUB_TAG has no WHITE_BED — only Topic + TAG beds
}


class TemplateManager:
    """
    Loads and manages template images and bed configurations.
    """
    def __init__(self, settings):
        self.settings = settings
        self.main_path = self.settings.get("templates", "main_tag_path", "templates/MAIN_TAG.png")
        self.sub_path  = self.settings.get("templates", "sub_tag_path",  "templates/SUB_TAG.png")
        self.loaded_images = {}

    def validate_templates(self):
        """Verify templates exist and are 1920x1080px."""
        valid = True
        for name, path in [("MAIN_TAG", self.main_path), ("SUB_TAG", self.sub_path)]:
            if not os.path.exists(path):
                print(f"Warning: Template not found: {path}")
                valid = False
                continue
            try:
                with Image.open(path) as img:
                    if img.size != (1920, 1080):
                        print(f"Warning: {name} dimensions are {img.size}, expected 1920x1080")
                        valid = False
            except Exception as e:
                print(f"Error validating {name}: {e}")
                valid = False
        return valid

    def load_template(self, template_type):
        """Load MAIN_TAG or SUB_TAG image."""
        path = self.main_path if template_type == "MAIN_TAG" else self.sub_path
        if not os.path.exists(path):
            return None
        try:
            img = Image.open(path).convert("RGBA")
            self.loaded_images[template_type] = img
            return img
        except Exception as e:
            print(f"Error loading template {template_type}: {e}")
            return None

    def get_bed_config(self, template_type, bed_name):
        """Return bed region specifications."""
        beds = MAIN_TAG_BEDS if template_type == "MAIN_TAG" else SUB_TAG_BEDS
        return beds.get(bed_name)

    def get_template_image(self, template_type="MAIN_TAG"):
        """Return a fresh PIL Image copy for compositing."""
        if template_type in self.loaded_images:
            return self.loaded_images[template_type].copy()
        return self.load_template(template_type)
