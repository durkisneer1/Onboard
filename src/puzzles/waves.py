from random import randint
from math import sin

import pygame as pg

from core.settings import SCN_SIZE


class BaseWave:
    colors = {
        "blue": (94, 233, 233),
        "red": (218, 36, 36),
        "dblue": (40, 144, 220),
        "dred": (114, 13, 13),
    }

    def __init__(self, y_offset: float, color: str) -> None:
        self.amplitude = 4
        self.stretch = 4
        self.y_offset = y_offset
        self.color = self.colors[color]
        self.bloom_color = self.colors[f"d{color}"]
        self.points = []
        self.bloom = pg.Surface(SCN_SIZE, pg.SRCALPHA)

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, MatchWave) or isinstance(other, TemplateWave):
            return False
        return self.amplitude == other.amplitude and self.stretch == other.stretch

    def calculate(self):
        self.points = [
            (
                i + SCN_SIZE[0] / 2 - 36,
                sin(i / self.stretch) * self.amplitude
                + (SCN_SIZE[1] / 2 + self.y_offset),
            )
            for i in range(72)
        ]
        pg.draw.lines(self.bloom, self.bloom_color, False, self.points, 6)
        self.bloom = pg.transform.gaussian_blur(self.bloom, 4)
        self.bloom.set_alpha(80)

    def draw(self, screen: pg.Surface):
        screen.blit(self.bloom, (0, 0))
        pg.draw.lines(screen, self.color, False, self.points, 1)


class MatchWave(BaseWave):
    def __init__(self):
        super().__init__(-14, "red")
        self.calculate()

    def edit_attribute(
        self, attribute: str, inc: bool = False, dec: bool = False
    ) -> None:
        if inc is False and dec is False:
            return

        current_value = getattr(self, attribute)

        if inc and current_value < 9:
            setattr(self, attribute, current_value + 1)
        elif dec and current_value > 1:
            setattr(self, attribute, current_value - 1)

        self.points = self.calculate()

    def edit_amp(self, inc: bool = False, dec: bool = False) -> None:
        self.edit_attribute("amplitude", inc, dec)

    def edit_stretch(self, inc: bool = False, dec: bool = False) -> None:
        self.edit_attribute("stretch", inc, dec)


class TemplateWave(BaseWave):
    def __init__(self):
        super().__init__(14, "blue")
        self.reset()

    def reset(self):
        self.amplitude = randint(1, 9)
        self.stretch = randint(1, 9)
        self.calculate()
