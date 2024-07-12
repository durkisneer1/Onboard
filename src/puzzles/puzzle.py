from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame as pg

from core.settings import SCN_SIZE

if TYPE_CHECKING:
    from main import Engine


class Puzzle(ABC):
    def __init__(self, engine: "Engine") -> None:
        self.engine: "Engine" = engine

        self.bg_dimmer: pg.Surface = pg.Surface(SCN_SIZE)
        self.bg_dimmer.set_alpha(180)

        self.active: bool = False

    def render(self) -> None:
        if not self.active:
            return

        self.engine.screen.blit(self.bg_dimmer, (0, 0))

        self._render()

    @abstractmethod
    def _render(self) -> None: ...
