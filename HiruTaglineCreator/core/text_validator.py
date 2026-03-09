class TextValidator:
    """
    Validates TAG / White Bed text against word-count rules.
    """

    def __init__(self, settings):
        v = settings.get('validation') or {}
        self.max_words_warning    = v.get('max_words_warning', 9)
        self.max_words_with_short = v.get('max_words_with_short', 13)
        self.short_word_length    = v.get('short_word_length', 3)

    def validate_tag_line(self, text):
        """
        Returns (is_valid, message | None).
        - Up to 9 words → OK
        - 10-13 words with ≥3 short words (≤3 chars) → Warning but allowed
        - Otherwise → Error
        """
        words      = text.split()
        word_count = len(words)

        if word_count == 0:
            return True, None

        if word_count <= self.max_words_warning:
            return True, None

        short_words = [w for w in words if len(w) <= self.short_word_length]

        if word_count <= self.max_words_with_short and len(short_words) >= 3:
            return True, f"⚠ {word_count} words (OK – contains short words)"

        return False, f"✖ {word_count} words exceeds limit ({self.max_words_warning})"

    def validate_white_bed(self, text):
        return self.validate_tag_line(text)

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
