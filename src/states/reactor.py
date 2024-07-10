from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AppState
from core.room import Room
from core.settings import *
from core.transitions import FadeTransition
from src.interactable import Interactable
from src.puzzles.dots import DotsPuzzle

if TYPE_CHECKING:
    from main import Engine


class ReactorRoom(Room):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine, room_image_path="assets/reactor.png")

        self.dots_tablet = Interactable(
            self.player, self.engine, pg.FRect(153, 84, 4, 12)
        )
        self.dots_puzzle = DotsPuzzle(self.engine)

        storage_rect = pg.FRect(23, 77, 5, 30)
        self.storage_door = Interactable(self.player, self.engine, storage_rect)

        self.transition = FadeTransition(True, 300, pg.Vector2(WIN_SIZE))
        self.next_state = AppState.EMPTY

        self.player.rect.bottomleft = storage_rect.bottomright

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.engine.last_state = self.engine.current_state
                self.engine.current_state = AppState.PAUSE
                self.engine.state_dict[
                    self.engine.current_state
                ].last_frame = self.engine.screen.copy()

    def render(self):
        self.engine.screen.fill("black")
        self.render_background()

        if not self.dots_puzzle.done:
            self.dots_tablet.render()

        self.storage_door.render()
        if self.storage_door.event:
            self.transition.fade_in = False
            self.next_state = AppState.STORAGE

        self.player.update(self.dots_puzzle.active)

        if self.dots_tablet.event and not self.dots_puzzle.done:
            self.dots_puzzle.active = not self.dots_puzzle.active
        self.dots_puzzle.render()

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)

        if self.transition.event:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = self.next_state
            self.transition.fade_in = True
