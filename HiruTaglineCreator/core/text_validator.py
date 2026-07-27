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

    def validate_all(self, tag_lines, white_lines):
        """
        Returns (all_valid: bool, errors: list[str]).
        white_lines may be a list of strings or a single string (backward compat).
        """
        errors    = []
        all_valid = True

        for i, line in enumerate(tag_lines):
            valid, msg = self.validate_tag_line(line)
            if msg:
                errors.append(f"TAG Line {i + 1}: {msg}")
            if not valid:
                all_valid = False

        if isinstance(white_lines, str):
            white_lines = [white_lines] if white_lines else []

        for i, line in enumerate(white_lines):
            if line:
                valid, msg = self.validate_white_bed(line)
                if msg:
                    label = f"White Bed {i + 1}" if len(white_lines) > 1 else "White Bed"
                    errors.append(f"{label}: {msg}")
                if not valid:
                    all_valid = False

        return all_valid, errors
