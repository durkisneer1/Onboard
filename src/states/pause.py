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
            TextButton(engine, "Continue", pg.Vector2(90, 30), (50, 16)),
            TextButton(engine, "Menu", pg.Vector2(90, 50), (50, 16)),
        ]

    def handle_events(self, event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.engine.current_state = self.engine.last_state
            # fixes visual bug
            for button in self.buttons:
                button.hovering = False

    def render(self) -> None:
        self.engine.screen.blit(self.last_frame, (0, 0))
        self.engine.screen.blit(self.surface_tint, (0, 0))

        self.handle_buttons()

    def handle_buttons(self) -> None:
        for button in self.buttons:
            button.render()

            if button.event:
                button.hovering = False
                match button.text_str:
                    case "Continue":
                        self.engine.current_state = self.engine.last_state
                    case "Menu":
                        self.engine.current_state = AppState.MENU
                        self.engine.state_dict[
                            self.engine.last_state
                        ].transition.fade_in = True
                        self.engine.state_dict[
                            self.engine.last_state
                        ].transition.alpha = 255
