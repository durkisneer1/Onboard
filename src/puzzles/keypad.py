from typing import TYPE_CHECKING

import pygame as pg

from core.buttons import NumButton
from core.settings import *

if TYPE_CHECKING:
    from main import Engine


class KeyPadPuzzle:
    def __init__(self, engine: "Engine"):
        self.engine = engine

        self.bg_dimmer = pg.Surface(WIN_SIZE)
        self.bg_dimmer.set_alpha(180)

        self.active = False
        self.done = False

        self.engine = engine
        self.buttons = [
            NumButton(engine, 3 * y + x, pg.Vector2(x, y) * 10, pg.Vector2(10, 10))
            for x in range(1, 4)
            for y in range(0, 3)
        ]

        self.code = [1, 2, 3, 4]
        self.user_in = []

        self.boop_sfx = pg.mixer.Sound("assets/boop.mp3")
        self.success_sfx = pg.mixer.Sound("assets/success.mp3")

    def render(self) -> None:
        if not self.active:
            return

        self.engine.screen.blit(self.bg_dimmer, (0, 0))

        for button in self.buttons:
            button.render()
            if not button.event:
                continue

            self.user_in.append(button.num)
            if len(self.user_in) != len(self.code):
                self.boop_sfx.play()
                continue

            if self.user_in == self.code:
                self.active = False
                self.done = True
                self.success_sfx.play()
