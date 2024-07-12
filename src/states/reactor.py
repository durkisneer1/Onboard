from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AppState
from core.room import Room
from core.settings import SCN_SIZE
from core.transitions import FadeTransition
from src.interactable import DoorInteractable, Interactable
from src.puzzles.dots import DotsPuzzle
from src.puzzles.freq import FreqPuzzle

if TYPE_CHECKING:
    from main import Engine


class ReactorRoom(Room):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine, room_image_path="assets/reactor.png")

        self.dots_tablet = Interactable(
            self.player, self.engine, pg.FRect(153, 84, 4, 12)
        )
        self.dots_puzzle = DotsPuzzle(self.engine)
        self.freq_tablet = Interactable(
            self.player, self.engine, pg.FRect(153, 84, 4, 12)
        )
        self.freq_puzzle = FreqPuzzle(self.engine)

        self.storage_door = DoorInteractable(self.player, self.engine, (34, 76))

        self.transition = FadeTransition(True, 300, pg.Vector2(SCN_SIZE))
        self.next_state = AppState.EMPTY

        self.player.rect.bottomleft = (32, 107)

        self.dots_puzzle.done = True  # DELETE ME

    def handle_events(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = AppState.PAUSE
            self.engine.state_dict[self.engine.current_state].last_frame = (
                self.engine.screen.copy()
            )

    def render(self):
        if not pg.mixer.music.get_busy() and self.next_state == AppState.EMPTY:
            pg.mixer.music.load("assets/reactor.mp3")
            pg.mixer.music.play(-1, fade_ms=500)

        self.engine.screen.fill("black")
        self.render_background()

        self.storage_door.update()
        if self.storage_door.event:
            self.transition.fade_in = False
            self.next_state = AppState.STORAGE
            pg.mixer.music.fadeout(700)

        self.player.update(self.dots_puzzle.active)

        if not self.dots_puzzle.done:
            self.dots_tablet.render()
            if self.dots_tablet.event:
                self.dots_puzzle.active = not self.dots_puzzle.active
            self.dots_puzzle.render()
        else:
            if not self.freq_puzzle.done:
                self.freq_tablet.render()
                if self.freq_tablet.event:
                    self.freq_puzzle.active = not self.freq_puzzle.active
                self.freq_puzzle.render()

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)

        if self.transition.event:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = self.next_state
            self.transition.fade_in = True
            self.next_state = AppState.EMPTY

    def render_extra_background_items(self, surface: pg.Surface, n: int):
        self.storage_door.render_layer(surface, n=n)
