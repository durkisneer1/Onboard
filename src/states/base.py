from typing import TYPE_CHECKING

import pygame as pg

from core.settings import SCN_SIZE

if TYPE_CHECKING:
    from main import Engine


class BaseState:
    def __init__(self, engine: "Engine") -> None:
        self.engine = engine

        self.surface_tint = pg.Surface(SCN_SIZE)
        self.surface_tint.fill((0, 0, 0))
        self.surface_tint.set_alpha(185)
        self.last_frame = pg.Surface((1, 1))

    def render(self): ...
