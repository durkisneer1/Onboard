from typing import TYPE_CHECKING

import pygame as pg

from core.buttons import MenuButton
from core.enums import AppState
from core.settings import SCN_SIZE
from core.transitions import FadeTransition
from src.states.base import BaseState

if TYPE_CHECKING:
    from main import Engine


class Menu(BaseState):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)

        self.bg = pg.image.load("assets/bg.png").convert()

        self.game_button = MenuButton(
            engine, "start", pg.Vector2(4, 4), pg.Vector2(50, 16), 0
        )
        self.settings_button = MenuButton(
            engine, "settings", pg.Vector2(4, 24), pg.Vector2(50, 16), 20
        )
        self.exit_button = MenuButton(
            engine, "exit", pg.Vector2(4, 44), pg.Vector2(50, 16), 40
        )

        self.transition = FadeTransition(True, 300, pg.Vector2(SCN_SIZE))
        self.next_state = (
            AppState.EMPTY
        )  # Change this to the state you want to transition to initially (for debugging)

        self.intro_shown = False

    def render(self):
        if not pg.mixer.music.get_busy():
            pg.mixer.music.load("assets/theme.ogg")
            pg.mixer.music.play(-1, fade_ms=500)

        self.engine.screen.blit(self.bg)

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
            self.next_state = (
                self.engine.last_state if self.intro_shown else AppState.INTRO
            )
            self.intro_shown = True

        self.settings_button.render()
        if self.settings_button.event:
            self.transition.fade_in = False
            self.next_state = AppState.SETTINGS

        self.exit_button.render()
        if self.exit_button.event:
            self.engine.handle_exit()
