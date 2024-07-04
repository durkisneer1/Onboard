from typing import TYPE_CHECKING

import pygame as pg

from core.settings import WIN_SIZE

if TYPE_CHECKING:
    from main import Engine


class Pause:
    def __init__(self, engine: "Engine", previous_state) -> None:
        self.engine = engine
        self.previous_state = previous_state

        self.last_frame = None
        self.screen_darkener = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.screen_darkener.fill((0, 0, 0, 185))

        self.active = False

        self.next_state = None

    def render(self):
        # get last frame, darken it
        if not self.active:
            self.last_frame = self.engine.screen.copy()
            self.active = True
        self.engine.screen.blit(self.last_frame, (0, 0))
        self.engine.screen.blit(self.screen_darkener, (0, 0))

        self.next_state = None

        keys = pg.key.get_just_pressed()
        if keys[pg.K_ESCAPE]:
            # switch to the previous state (unpause the game)
            self.next_state = self.previous_state
            self.active = False
