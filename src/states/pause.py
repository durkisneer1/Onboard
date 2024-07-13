from typing import TYPE_CHECKING

import pygame as pg

from core.buttons import TextButton
from core.enums import AppState
from core.settings import SCN_SIZE
from src.states.base import BaseState

if TYPE_CHECKING:
    from main import Engine


class Pause(BaseState):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)

        self.buttons = [
            TextButton(engine, "Continue", pg.Vector2(0, 0), pg.Vector2(50, 16)),
            TextButton(engine, "Menu", pg.Vector2(0, 20), pg.Vector2(50, 16)),
        ]

    def handle_events(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.engine.current_state = self.engine.last_state
            # fixes visual bug
            for button in self.buttons:
                button.hovering = False

    def render(self):
        self.engine.screen.blit(self.last_frame, (0, 0))
        self.engine.screen.blit(self.surface_tint, (0, 0))

        self.handle_buttons()

    def handle_buttons(self):
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
