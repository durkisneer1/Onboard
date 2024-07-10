from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AppState
from core.room import Room
from core.settings import *
from core.transitions import FadeTransition
from src.interactable import Interactable
from src.puzzles.simon import SimonSaysPuzzle

if TYPE_CHECKING:
    from main import Engine


class StorageRoom(Room):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine, room_image_path="assets/storage.png")

        self.simon = Interactable(self.player, self.engine, pg.FRect(108, 81, 15, 15))
        self.simon_puzzle = SimonSaysPuzzle(self.engine)

        cockpit_rect = pg.FRect(32, 77, 5, 30)
        self.cockpit_door = Interactable(self.player, self.engine, cockpit_rect)
        self.reactor_door = Interactable(
            self.player, self.engine, pg.FRect(203, 77, 5, 30)
        )

        self.transition = FadeTransition(True, 300, pg.Vector2(WIN_SIZE))
        self.next_state = AppState.EMPTY

        self.player.rect.bottomleft = cockpit_rect.bottomright

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.engine.last_state = self.engine.current_state
                self.engine.current_state = AppState.PAUSE
                self.engine.state_dict[self.engine.current_state].last_frame = (
                    self.engine.screen.copy()
                )

    def render(self):
        self.engine.screen.fill("black")
        self.render_background()

        if not self.simon_puzzle.done:
            self.simon.render()

        self.cockpit_door.render()
        if self.cockpit_door.event:
            self.transition.fade_in = False
            self.next_state = AppState.COCKPIT

        self.reactor_door.render()
        if self.reactor_door.event:
            self.transition.fade_in = False
            self.next_state = AppState.REACTOR

        self.player.update(self.simon_puzzle.active)

        if self.simon.event and not self.simon_puzzle.done:
            self.simon_puzzle.reset()
            self.simon_puzzle.active = not self.simon_puzzle.active
        self.simon_puzzle.render()

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)

        if self.transition.event:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = self.next_state
            self.transition.fade_in = True
