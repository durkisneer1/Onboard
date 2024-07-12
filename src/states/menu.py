from typing import TYPE_CHECKING

import pygame as pg

from core.settings import SCN_SIZE
from core.buttons import TextButton
from core.enums import AppState
from core.transitions import FadeTransition
from src.states.base import BaseState

if TYPE_CHECKING:
    from main import Engine


class Menu(BaseState):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)

        self.bg = pg.Surface(SCN_SIZE)
        self.bg.fill("black")

        self.game_button = TextButton(
            engine, "Start", pg.Vector2(90, 32), pg.Vector2(50, 16)
        )

        self.settings_button = TextButton(
            engine, "Settings", pg.Vector2(90, 52), pg.Vector2(50, 16)
        )

        self.transition = FadeTransition(True, 300, pg.Vector2(SCN_SIZE))
        self.next_state = (
            AppState.EMPTY
        )  # Change this to the state you want to transition to initially (for debugging)

    def handle_events(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.transition.fade_in = False

    def render(self):
        self.engine.screen.blit(self.bg, (0, 0))

        self.handle_buttons()

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)

        # switch
        if self.transition.event:
            # self.engine.current_state = self.engine.last_state
            self.engine.current_state = self.next_state
            self.transition.fade_in = True
            self.next_state = AppState.EMPTY

    def handle_buttons(self):
        self.game_button.render()
        if self.game_button.event:
            self.transition.fade_in = False
            self.next_state = AppState.INTRO

        self.settings_button.render()
        if self.settings_button.event:
            self.transition.fade_in = False
            self.next_state = AppState.SETTINGS
