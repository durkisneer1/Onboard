import random
from typing import TYPE_CHECKING

import pygame as pg

from core.buttons import SimonButton
from core.settings import SCN_SIZE
from core.surfaces import import_image
from src.puzzles.puzzle import Puzzle

if TYPE_CHECKING:
    from main import Engine


class SimonSaysPuzzle(Puzzle):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)
        self.done = False

        btn_surfs = {
            "idle": import_image("assets/simon_button_idle.png", is_alpha=False),
            "pressed": import_image("assets/simon_button_pressed.png", is_alpha=False),
            "glow": import_image("assets/simon_button_glow.png", is_alpha=False),
            "hover": import_image("assets/simon_button_hover.png", is_alpha=False),
        }

        self.buttons = [
            SimonButton(engine, 4 * y + x, pg.Vector2(x, y) * 12, btn_surfs)
            for x in range(1, 5)
            for y in range(0, 4)
        ]
        self.buttons.sort(key=lambda btn: btn.num)

        # define game vars
        self._reset()

        self.tablet = pg.Surface((50, 50), pg.SRCALPHA)
        tablet_rect = pg.Rect(0, 0, 50, 50)
        pg.draw.rect(self.tablet, (104, 107, 114), tablet_rect, border_radius=2)
        self.tablet_pos = self.buttons[0].rect.topleft - pg.Vector2(1, 1)

        self.hint = engine.px_font.render("repeat the pattern", False, (24, 13, 47))
        self.hint_pos = self.hint.get_rect(bottomleft=(4, SCN_SIZE[1]))

    def _reset(self):
        self.code = random.sample(range(1, 17), 6)
        self.user_in = []
        self.current_length = 2
        self.current_shown_num = 0  # index

        self.timer = 1
        self.player_turn = False
        self.wait_for_turns = False  # cooldown between turns

        # fixes bug when you re-enter the puzzle and the previous button is
        # still in glowing/hovering state for 1 frame
        for button in self.buttons:
            button.glow = False
            button.hovering = False

    def _render(self):
        self.engine.screen.blit(self.tablet, self.tablet_pos)

        self._player_turn() if self.player_turn else self._simon_turn()

        self.engine.screen.blit(self.hint, self.hint_pos)

    def _simon_turn(self) -> None:
        for button in self.buttons:
            button.render(False)
            button.hovering = False
            button.glow = False

        # highlight button for some time
        self.timer -= self.engine.dt
        if self.timer <= 0:
            self.timer = 1
            if self.wait_for_turns:
                self.wait_for_turns = False
                return
            self.current_shown_num += 1
        elif self.wait_for_turns:
            return

        # if we're done highlighting stuff
        if self.current_shown_num > self.current_length - 1:
            self.player_turn = True
            self.current_shown_num = 0
            return

        # highlight current button
        self.buttons[self.code[self.current_shown_num] - 1].glow = True

    def _player_turn(self) -> None:
        for button in self.buttons:
            button.render(True)

            if not button.event:
                continue

            self.user_in.append(button.num)
            if self.user_in == self.code:
                self._on_success()
                return

            self.engine.sfx["boop"].play()

            if len(self.user_in) != len(self.code[: self.current_length]):
                continue

            (
                self._next_turn()
                if self.user_in == self.code[: self.current_length]
                else self._on_failure()
            )

    def _on_success(self):
        self.active = False
        self.done = True
        self.engine.sfx["success"].play()

    def _next_turn(self):
        self.current_length += 1
        self.user_in = []
        self.wait_for_turns = True
        self.player_turn = False

    def _on_failure(self):
        self.active = False
        self._reset()
        self.engine.sfx["failure"].play()
