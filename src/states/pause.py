from typing import TYPE_CHECKING

import pygame as pg

from core.buttons import TextButton
from core.enums import AppState
from core.settings import *
from src.states.base import BaseState

if TYPE_CHECKING:
    from main import Engine


class Pause(BaseState):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)

        self.buttons = [
            TextButton(engine, "Continue", pg.Vector2(100, 10), (40, 16)),
            TextButton(engine, "Settings", pg.Vector2(100, 30), (40, 16)),
            TextButton(engine, "Menu", pg.Vector2(100, 50), (40, 16)),
        ]

    def handle_events(self, event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.engine.current_state = self.engine.last_state

    def render(self) -> None:
        self.engine.screen.blit(self.last_frame, (0, 0))
        self.engine.screen.blit(self.surface_tint, (0, 0))

        self.handle_buttons()

    def handle_buttons(self) -> None:
        for button in self.buttons:
            button.render()

            if button.event:
                self.engine.last_state = AppState.PAUSE
                match button.text_str:
                    case "Continue":
                        self.engine.current_state = self.engine.last_state
                    case "Menu":
                        self.engine.current_state = AppState.MENU
                    case "Settings":
                        self.engine.current_state = AppState.SETTINGS
