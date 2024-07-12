from random import randint
from math import sin

import pygame as pg

from core.settings import SCN_SIZE


class BaseWave:
    def __init__(self, y_offset: float) -> None:
        self.amplitude = 4
        self.stretch = 4
        self.y_offset = y_offset
        self.points = []

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, MatchWave) or isinstance(other, TemplateWave):
            return False
        return self.amplitude == other.amplitude and self.stretch == other.stretch

    def calculate(self):
        return [
            (
                i + SCN_SIZE[0] / 2 - 40,
                sin(i / self.stretch) * self.amplitude
                + (SCN_SIZE[1] / 2 + self.y_offset),
            )
            for i in range(80)
        ]

    def draw(self, screen: pg.Surface, color: str):
        pg.draw.lines(screen, color, False, self.points, 1)


class MatchWave(BaseWave):
    def __init__(self):
        super().__init__(-20)
        self.points = self.calculate()

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
        super().__init__(20)
        self.reset()

    def reset(self):
        self.amplitude = randint(1, 9)
        self.stretch = randint(1, 9)
        self.points = self.calculate()
