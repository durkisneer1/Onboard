from typing import TYPE_CHECKING

import pygame as pg

from core.buttons import NumButton
from core.settings import SCN_SIZE
from core.surfaces import import_image
from src.puzzles.puzzle import Puzzle

if TYPE_CHECKING:
    from main import Engine


class KeyPadPuzzle(Puzzle):
    def __init__(self, engine: "Engine"):
        super().__init__(engine)
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

        self.code = [1, 5, 7, 2]
        self.user_in = []

        font = pg.Font("assets/m5x7.ttf", 16)
        self.hint = font.render("enter the code", False, (24, 13, 47))
        self.hint_pos = self.hint.get_rect(bottomleft=(4, SCN_SIZE[1]))

    def _render(self):
        for button in self.buttons:
            button.render()
            if not button.event:
                continue

            self.user_in.append(button.num)
            if len(self.user_in) != len(self.code):
                self.engine.sfx["boop"].play()
                continue

            if self.user_in == self.code:
                self.active = False
                self.done = True
                self.engine.sfx["success"].play()
            else:
                self.user_in.clear()
                self.engine.sfx["failure"].play()

        self.engine.screen.blit(self.hint, self.hint_pos)
