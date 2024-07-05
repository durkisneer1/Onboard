from typing import TYPE_CHECKING

import pygame as pg

from core.buttons import Button
from core.settings import *
from core.transitions import FadeTransition
from src.states.base import BaseState

if TYPE_CHECKING:
    from main import Engine


class Menu(BaseState):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)

        self.placeholder = pg.Surface(WIN_SIZE)
        self.placeholder.fill("purple")

        self.buttons = [
            #               position     size
            Button(engine, (175, 110), (60, 20)),
            Button(engine, (175, 85), (60, 20)),
            Button(engine, (175, 60), (60, 20)),
        ]

        self.transition = FadeTransition(True, 300, WIN_SIZE)

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.transition.fade_in = False

    def render(self):
        self.engine.screen.blit(self.placeholder, (0, 0))

        self.update_buttons()

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)
        # switch
        if self.transition.event:
            self.engine.current_state = self.engine.last_state
            self.transition.fade_in = True

    def update_buttons(self):
        for button in self.buttons:
            button.render()
