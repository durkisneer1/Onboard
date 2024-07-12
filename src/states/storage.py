from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AppState
from core.room import Room
from core.settings import *
from core.transitions import FadeTransition
from src.interactable import Interactable, DoorInteractable
from src.puzzles.simon import SimonSaysPuzzle
from src.puzzles.wirecut import WireCut

if TYPE_CHECKING:
    from main import Engine


class StorageRoom(Room):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine, room_image_path="assets/storage.png")

        self.simon = Interactable(self.player, self.engine, pg.FRect(108, 81, 15, 15))
        self.simon_puzzle = SimonSaysPuzzle(self.engine)
        self.wires = Interactable(self.player, self.engine, pg.FRect(108, 81, 15, 15))
        self.wirecut_puzzle = WireCut(self.engine)

        self.cockpit_door = DoorInteractable(self.player, self.engine, (33, 76))
        self.reactor_door = DoorInteractable(self.player, self.engine, (185, 76))

        self.transition = FadeTransition(True, 300, pg.Vector2(WIN_SIZE))
        self.next_state = AppState.EMPTY

        self.player.rect.bottomleft = (32, 107)

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.engine.last_state = self.engine.current_state
                self.engine.current_state = AppState.PAUSE
                self.engine.state_dict[self.engine.current_state].last_frame = (
                    self.engine.screen.copy()
                )

    def render(self):
        if not pg.mixer.music.get_busy() and self.next_state == AppState.EMPTY:
            pg.mixer.music.load("assets/storage.mp3")
            pg.mixer.music.play(-1, fade_ms=500)

        self.engine.screen.fill("black")
        self.render_background()

        if not self.simon_puzzle.done:
            self.simon.render()
        elif self.simon_puzzle.done:
            self.wires.render()

        self.cockpit_door.update()
        if self.cockpit_door.event:
            self.transition.fade_in = False
            self.next_state = AppState.COCKPIT
            pg.mixer.music.fadeout(700)

        # if self.wirecut_puzzle.done:
        self.reactor_door.update()
        if self.reactor_door.event:
            self.transition.fade_in = False
            self.next_state = AppState.REACTOR
            pg.mixer.music.fadeout(700)

        self.player.update(self.simon_puzzle.active or self.wirecut_puzzle.active)

        if not self.simon_puzzle.done:
            self.simon_puzzle.render()
            if self.simon.event:
                self.simon_puzzle.reset()
                self.simon_puzzle.active = not self.simon_puzzle.active
        else:
            self.wirecut_puzzle.render()
            if self.wires.event:
                self.wirecut_puzzle.active = not self.wirecut_puzzle.active

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)

        if self.transition.event:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = self.next_state
            self.transition.fade_in = True
            self.next_state = AppState.EMPTY

    def render_extra_background_items(self, surface: pg.Surface, n: int):
        self.cockpit_door.render_layer(surface, n=n)
        # if self.wirecut_puzzle.done:
        self.reactor_door.render_layer(surface, n=n)
