import pygame as pg


class FadeTransition:
    def __init__(self, fade_in: bool, fade_speed: float, size: pg.Vector2) -> None:
        self.fade_in = fade_in
        self.init_fade = fade_in
        self.fade_speed = fade_speed
        self.image = pg.Surface(size)

        self.event = False
        self.alpha = 255 if fade_in else 0
        self.image.set_alpha(self.alpha)

    def _handle_fade_in(self, dt: float):
        if self.alpha > 0:
            self.alpha -= self.fade_speed * dt
            self.event = False
        else:
            self.alpha = 0
            if not self.init_fade:
                self.event = True

    def _handle_fade_out(self, dt: float):
        if self.alpha < 255:
            self.alpha += self.fade_speed * dt
            self.event = False
        else:
            self.alpha = 255
            if self.init_fade:
                self.event = True

    def update(self, dt: float):
        self._handle_fade_in(dt) if self.fade_in else self._handle_fade_out(dt)
        self.image.set_alpha(int(self.alpha))

    def draw(self, screen: pg.Surface):
        screen.blit(self.image)
