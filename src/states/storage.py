from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AppState
from core.room import Room
from core.settings import COLOR_SETS, SCN_SIZE
from core.surfaces import import_image, shift_colors
from core.transitions import FadeTransition
from src.interactable import DoorInteractable, Interactable
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
        self.reactor_door = DoorInteractable(self.player, self.engine, (186, 76))

        self.transition = FadeTransition(True, 300, pg.Vector2(SCN_SIZE))
        self.next_state = AppState.EMPTY

        self.wirecut_layers = [
            shift_colors(
                surface=import_image("assets/storage_wires.png"),
                color_sets=COLOR_SETS,
                n=2 - i,
            )
            for i in range(3)
        ]

        self.player.rect.bottomleft = (32, 107)

    def handle_events(self, event):
        self.engine.diary.handle_events(event)

        if not any({self.simon_puzzle.active, self.wirecut_puzzle.active}):
            super().handle_events(event)

    def render(self):
        if not pg.mixer.music.get_busy() and self.next_state == AppState.EMPTY:
            pg.mixer.music.load("assets/storage.ogg")
            pg.mixer.music.play(-1, fade_ms=500)

        self.engine.screen.fill("black")
        self.render_background()

        if not self.simon_puzzle.done:
            self.simon.render()
        else:
            if not self.wirecut_puzzle.done:
                self.wires.render()
            else:
                self.reactor_door.update()

        self.cockpit_door.update()
        if self.cockpit_door.event:
            self.transition.fade_in = False
            self.next_state = AppState.COCKPIT
            pg.mixer.music.fadeout(700)

        if self.reactor_door.event:
            self.transition.fade_in = False
            self.next_state = AppState.REACTOR
            pg.mixer.music.fadeout(700)

        self.player.update(self.simon_puzzle.active or self.wirecut_puzzle.active)

        if not self.simon_puzzle.done:
            self.simon_puzzle.render()
            if self.simon.active:
                self.simon_puzzle.listen_for_keypress()
        else:
            if not self.wirecut_puzzle.done:
                self.wirecut_puzzle.render()
                if self.wires.active:
                    self.wirecut_puzzle.listen_for_keypress()

        if not self.simon_puzzle.active and not self.wirecut_puzzle.active:
            self.engine.diary.render()

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)

        if self.transition.event:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = self.next_state
            self.transition.fade_in = True
            self.next_state = AppState.EMPTY

    def render_extra_background_items(self, surface: pg.Surface, n: int):
        self.cockpit_door.render_layer(surface, n=n)
        self.reactor_door.render_layer(surface, n=n)
        if self.simon_puzzle.done:
            surface.blit(self.wirecut_layers[n], (77, 55))
