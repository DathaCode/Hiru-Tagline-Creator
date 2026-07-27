class TextValidator:
    """
    Validates TAG / White Bed text against word-count rules.
    """

    def __init__(self, settings=None):
        # Validation limits are now hard-coded per bed
        self.limits = {
            'topic': 12,
            'white': 15,
            'tag': 20
        }

    def validate_tag_line(self, text):
        """
        Returns (is_valid, message | None).
        - Up to 20 words → OK
        - Otherwise → Error
        """
        words      = text.split()
        word_count = len(words)

        if word_count == 0 or word_count <= self.limits['tag']:
            return True, None

        return False, f"✖ {word_count} words exceeds limit ({self.limits['tag']})"

    def validate_white_bed(self, text):
        words      = text.split()
        word_count = len(words)

        if word_count == 0 or word_count <= self.limits['white']:
            return True, None

        return False, f"✖ {word_count} words exceeds limit ({self.limits['white']})"

    def validate_all(self, tag_lines, white_text):
        """
        Returns (all_valid: bool, errors: list[str]).
        Warnings are included in errors list but all_valid may still be True.
        """
        errors    = []
        all_valid = True

        for i, line in enumerate(tag_lines):
            valid, msg = self.validate_tag_line(line)
            if msg:
                errors.append(f"TAG Line {i + 1}: {msg}")
            if not valid:
                all_valid = False

        if white_text:
            valid, msg = self.validate_white_bed(white_text)
            if msg:
                errors.append(f"White Bed: {msg}")
            if not valid:
                all_valid = False

        return all_valid, errors
