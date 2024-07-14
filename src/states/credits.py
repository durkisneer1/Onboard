from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AppState
from core.settings import SCN_SIZE, WIN_SIZE
from core.transitions import FadeTransition
from src.states.base import BaseState

if TYPE_CHECKING:
    from main import Engine


class Credits(BaseState):
    def __init__(self, engine: "Engine"):
        super().__init__(engine)
        self.engine = engine
        self.credits = pg.image.load("assets/credits.png").convert()

        self.transition = FadeTransition(True, 300, pg.Vector2(SCN_SIZE))

        self.timer_out = False
        self.timer = 0

    def handle_events(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.transition.fade_in = False

    def render(self):
        if not pg.mixer.music.get_busy():
            pg.mixer.music.load("assets/theme.ogg")
            pg.mixer.music.play(-1, fade_ms=500)

        self.engine.screen.blit(self.credits, (0, 0))

        self.timer += self.engine.dt
        if self.timer > 10 and not self.timer_out:
            self.timer_out = True
            self.transition.fade_in = False

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)
        # switch
        if self.transition.event:
            self.engine.current_state = AppState.MENU
            self.transition.fade_in = True
            self.next_state = AppState.EMPTY
