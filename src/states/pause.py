from typing import TYPE_CHECKING

import pygame as pg

from core.settings import WIN_SIZE
from src.states.base import BaseState

if TYPE_CHECKING:
    from main import Engine


class Pause(BaseState):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.engine.current_state = self.engine.last_state

    def render(self):
        self.engine.screen.blit(self.last_frame, (0, 0))
        self.engine.screen.blit(self.surface_tint, (0, 0))
