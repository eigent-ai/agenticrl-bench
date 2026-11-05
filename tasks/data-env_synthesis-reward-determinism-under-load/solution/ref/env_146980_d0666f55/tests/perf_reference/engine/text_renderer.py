import pygame
class FloatingText:
    def __init__(self, text, x, y, color, alpha, font_size=28):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.alpha = alpha
        self.font_size = font_size
        self.lifetime = 120
        self.age = 0
        self.dy = -0.5
    def update(self):
        self.age += 1
        self.y += self.dy
        return self.age < self.lifetime
    @property
    def alive(self):
        return self.age < self.lifetime
class TextRenderer:
    def __init__(self):
        self.font_cache = {}
        self.texts = []
    def _get_font(self, size):
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.Font(None, size)
        return self.font_cache[size]
    def add_text(self, text, x, y, color=(255, 255, 255), alpha=180, font_size=28):
        ft = FloatingText(text, x, y, color, alpha, font_size)
        self.texts.append(ft)
        return ft
    def clear(self):
        self.texts.clear()
    def update(self):
        self.texts = [t for t in self.texts if t.update()]
    def render(self, target):
        for ft in self.texts:
            font = self._get_font(ft.font_size)
            r, g, b = ft.color[0], ft.color[1], ft.color[2]
            text_surf = font.render(ft.text, True, (r, g, b))
            text_surf.set_alpha(ft.alpha)
            target.blit(text_surf, (int(ft.x), int(ft.y)))
    def render_single(self, target, text, x, y, color, alpha, font_size=28):
        font = self._get_font(font_size)
        r, g, b = color[0], color[1], color[2]
        text_surf = font.render(text, True, (r, g, b))
        text_surf.set_alpha(alpha)
        target.blit(text_surf, (int(x), int(y)))
        return text_surf
