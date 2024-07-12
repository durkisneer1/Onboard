from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from core.buttons import TextButton
from core.enums import AppState
from core.picker import Picker
from core.range_picker import RangePicker
from core.settings import SCN_SIZE
from core.transitions import FadeTransition
from src.states.base import BaseState

if TYPE_CHECKING:
    from main import Engine


class SettingsMenu(BaseState):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)

        self.bg = pg.Surface(SCN_SIZE)
        self.bg.fill("black")

        self.save_button = TextButton(
            engine, "Save Settings", pg.Vector2(-10, 52), pg.Vector2(130, 16)
        )
        self.display_mode_pick = Picker(
            engine,
            pg.Vector2(10, 10),
            "Display",
            ["FULLSCREEN", "WINDOWED"],
            "FULLSCREEN",
        )
        self.sfx_range = RangePicker(
            engine,
            pg.Vector2(10, 50),
            "SFX",
            [0, 100],
            100,
        )
        self.bgm_range = RangePicker(
            engine,
            pg.Vector2(10, 70),
            "BGM",
            [0, 100],
            100,
        )
        self.next_state = AppState.EMPTY

        self.transition = FadeTransition(True, 300, pg.Vector2(SCN_SIZE))

    def render(self):
        self.engine.screen.blit(self.bg, (0, 0))
        self.handle_ui()

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)
        if self.transition.event:
            self.engine.current_state = self.next_state
            self.transition.fade_in = True

    def handle_ui(self) -> None:
        self.save_button.render()
        self.display_mode_pick.render()
        self.bgm_range.render()
        self.sfx_range.render()

        if not self.save_button.event:
            return

        if (
            self.display_mode_pick.values[self.display_mode_pick.index] == "WINDOWED"
            and pg.display.is_fullscreen()
        ):
            pg.display.toggle_fullscreen()

        if (
            self.display_mode_pick.values[self.display_mode_pick.index] == "FULLSCREEN"
            and not pg.display.is_fullscreen()
        ):
            pg.display.toggle_fullscreen()

        self.next_state = AppState.MENU
        self.transition.fade_in = False
