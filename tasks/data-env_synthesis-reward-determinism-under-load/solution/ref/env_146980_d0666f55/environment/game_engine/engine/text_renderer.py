"""Floating text renderer for damage numbers, status effects, and labels.

Renders text overlays with configurable transparency so that the game
scene beneath remains partially visible through the text.
"""

import pygame


class FloatingText:
    """Represents a single floating text element with position, color, and alpha."""

    def __init__(self, text, x, y, color, alpha, font_size=28):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.alpha = alpha
        self.font_size = font_size
        self.lifetime = 120  # frames
        self.age = 0
        self.dy = -0.5  # float upward

    def update(self):
        """Update text position and age."""
        self.age += 1
        self.y += self.dy
        return self.age < self.lifetime

    @property
    def alive(self):
        return self.age < self.lifetime


class TextRenderer:
    """Manages and renders floating text overlays with transparency."""

    def __init__(self):
        self.font_cache = {}
        self.texts = []

    def _get_font(self, size):
        """Get or create a cached font at the specified size."""
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.Font(None, size)
        return self.font_cache[size]

    def add_text(self, text, x, y, color=(255, 255, 255), alpha=180, font_size=28):
        """Add a floating text element."""
        ft = FloatingText(text, x, y, color, alpha, font_size)
        self.texts.append(ft)
        return ft

    def clear(self):
        """Remove all floating text elements."""
        self.texts.clear()

    def update(self):
        """Update all floating text positions, removing expired ones."""
        self.texts = [t for t in self.texts if t.update()]

    def render(self, target):
        """Render all floating text elements onto the target surface."""
        for ft in self.texts:
            font = self._get_font(ft.font_size)
            r, g, b = ft.color[0], ft.color[1], ft.color[2]
            text_surf = font.render(ft.text, True, (r, g, b, ft.alpha))
            target.blit(text_surf, (int(ft.x), int(ft.y)))

    def render_single(self, target, text, x, y, color, alpha, font_size=28):
        """Render a single text element without adding it to the managed list."""
        font = self._get_font(font_size)
        r, g, b = color[0], color[1], color[2]
        text_surf = font.render(text, True, (r, g, b, alpha))
        target.blit(text_surf, (int(x), int(y)))
        return text_surf
