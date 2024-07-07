from typing import TYPE_CHECKING

import pygame as pg

from core.settings import *

if TYPE_CHECKING:
    from main import Engine


class BaseState:
    def __init__(self, engine: "Engine") -> None:
        self.engine = engine

        self.surface_tint = pg.Surface(WIN_SIZE)
        self.surface_tint.fill((0, 0, 0))
        self.surface_tint.set_alpha(185)
        self.last_frame = None

    def handle_events(self, event):
        ...

    def render(self):
        ...
