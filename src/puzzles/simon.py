import random
from typing import TYPE_CHECKING

import pygame as pg

from core.buttons import SimonButton
from core.settings import *

if TYPE_CHECKING:
    from main import Engine


class SimonSaysPuzzle:
    def __init__(self, engine: "Engine") -> None:
        self.engine = engine

        self.bg_dimmer = pg.Surface(WIN_SIZE)
        self.bg_dimmer.set_alpha(180)

        self.active = False
        self.done = False

        self.buttons = [
            SimonButton(engine, 4 * y + x, pg.Vector2(x, y) * 12)
            for x in range(1, 5)
            for y in range(0, 4)
        ]
        self.buttons.sort(key=lambda btn: btn.num)

        self.code = random.sample(range(1, 17), 6)
        # define game vars
        self.reset()

        self.tablet = pg.Surface((50, 50), pg.SRCALPHA)
        tablet_rect = pg.Rect(0, 0, 50, 50)
        pg.draw.rect(self.tablet, (104, 107, 114), tablet_rect, border_radius=2)
        self.tablet_pos = self.buttons[0].rect.topleft - pg.Vector2(1, 1)

        self.boop_sfx = pg.mixer.Sound("assets/boop.mp3")
        self.success_sfx = pg.mixer.Sound("assets/success.mp3")
        self.failure_sfx = pg.mixer.Sound("assets/failure.mp3")
        self.failure_sfx.set_volume(0.35)

    def reset(self) -> None:
        self.code = random.sample(range(1, 17), 6)
        self.user_in = []
        self.current_length = 2
        self.current_shown_num = 0  # index

        self.timer = 1
        self.player_turn = False
        self.wait_for_turns = False  # cooldown between turns

    def render(self) -> None:
        if not self.active:
            return

        self.engine.screen.blit(self.bg_dimmer, (0, 0))
        self.engine.screen.blit(self.tablet, self.tablet_pos)

        self._player_turn() if self.player_turn else self._simon_turn()

    def _simon_turn(self) -> None:
        for button in self.buttons:
            button.render(False)
            button.hovering = False

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
        self.buttons[self.code[self.current_shown_num] - 1].hovering = True

    def _player_turn(self) -> None:
        for button in self.buttons:
            button.render(True)

            if not button.event:
                continue

            self.user_in.append(button.num)
            if self.user_in == self.code:
                self._on_success()
                return

            self.boop_sfx.play()

            if len(self.user_in) != len(self.code[: self.current_length]):
                continue

            self._next_turn() if self.user_in == self.code[
                : self.current_length
            ] else self._on_failure()

    def _on_success(self) -> None:
        self.active = False
        self.done = True
        self.success_sfx.play()

    def _next_turn(self) -> None:
        self.current_length += 1
        self.user_in = []
        self.wait_for_turns = True
        self.player_turn = False

    def _on_failure(self) -> None:
        self.active = False
        self.reset()
        self.failure_sfx.play()