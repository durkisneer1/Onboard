from typing import TYPE_CHECKING

import pygame as pg

from core.buttons import NumButton
from core.settings import *
from core.surfaces import import_image

if TYPE_CHECKING:
    from main import Engine


class KeyPadPuzzle:
    def __init__(self, engine: "Engine"):
        self.engine = engine

        self.bg_dimmer = pg.Surface(WIN_SIZE)
        self.bg_dimmer.set_alpha(180)

        self.active = False
        self.done = False

        btn_surfs = {
            "idle": import_image("assets/keypad_button_idle.png"),
            "pressed": import_image("assets/keypad_button_pressed.png"),
        }

        self.buttons = [
            NumButton(engine, 3 * y + x, pg.Vector2(x, y) * 16, btn_surfs)
            for x in range(1, 4)
            for y in range(0, 3)
        ]
        self.buttons.append(NumButton(engine, 0, pg.Vector2(2, 3) * 16, btn_surfs))

        self.code = [1, 2, 3, 4, 0]
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
