from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AppState
from core.settings import SCN_SIZE, WIN_SIZE
from src.states.base import BaseState

if TYPE_CHECKING:
    from main import Engine


def ease_in_back(x: float):
    c1 = 1.70158
    c3 = c1 + 1

    return c3 * x * x * x - c1 * x * x


class SplashScreen(BaseState):
    def __init__(self, engine: "Engine"):
        super().__init__(engine)
        self.engine = engine

        self.center = pg.Vector2(WIN_SIZE[0] / 2, WIN_SIZE[1] / 2)
        self.logo = pg.image.load("assets/pygame_ce_powered.png").convert_alpha()
        self.logo = pg.transform.scale_by(self.logo, 0.5)
        self.logo_rect = self.logo.get_rect(center=self.center.xy)

        # between 0 and 1
        self.tween_progress = 0

        self.animation_start = pg.time.get_ticks()

    def render(self):
        self.engine.display.fill("black")

        if (
            pg.time.get_ticks() - self.animation_start > 2000
            and self.tween_progress < 1
        ):
            self.tween_progress += self.engine.dt
            self.logo_rect.y = (
                -ease_in_back(self.tween_progress) * 770
                + self.center.y
                - self.logo_rect.height / 2
            )

        elif self.tween_progress >= 1:
            self.engine.current_state = AppState.MENU

        self.engine.display.blit(self.logo, self.logo_rect)
