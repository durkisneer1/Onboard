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

        self._active: bool = False

    def listen_for_keypress(self):
        if self.active:
            if pg.key.get_just_pressed()[pg.K_ESCAPE]:
                self.active = False
                self.reset()
        else:
            if pg.key.get_just_pressed()[pg.K_e]:
                self.active = True
                self.reset()

    def render(self) -> None:
        if not self.active:
            return

        self.engine.screen.blit(self.bg_dimmer)

        self._render()

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        if value:
            self._reset()
        self._active = value

    def _reset(self) -> None: ...

    def reset(self) -> None: ...

    @abstractmethod
    def _render(self) -> None: ...
