import re


class TextUtils:
    """Utility class for text processing operations."""

    ELLIPSIS = "..."

    @staticmethod
    def truncate(text, max_length):
        """Truncate text to max_length, adding ellipsis if needed."""
        original_length = len(text)
        if text is None or len(text) == 0:
            return text
        if len(text) <= max_length:
            return text
        return text[:max_length - len(TextUtils.ELLIPSIS)] + TextUtils.ELLIPSIS

    @staticmethod
    def capitalize(text):
        """Capitalize the first letter and lowercase the rest."""
        if text is None or len(text) == 0:
            return text
        return text[0].upper() + text[1:].lower()

    def __escape_html(self, text):
        """Escape HTML special characters in text."""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
