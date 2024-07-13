import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AppState
from core.room import Room
from core.settings import SCN_SIZE
from core.transitions import FadeTransition
from src.interactable import DoorInteractable, Interactable
from src.puzzles.keypad import KeyPadPuzzle
from src.puzzles.postit import PostItPuzzle

if TYPE_CHECKING:
    from main import Engine


@dataclass
class Particle:
    x: float
    y: float
    vel: float


class CockPit(Room):
    particle_colors = [(26, 12, 49), (53, 54, 88), (104, 107, 114)]

    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine, room_image_path="assets/cockpit.png")
        self.particles = [
            Particle(x=0, y=random.randint(13, 53), vel=random.randint(100, 200))
            for _ in range(6)
        ]

        self.keypad = Interactable(self.player, self.engine, pg.FRect(177, 84, 7, 9))
        self.keypad_puzzle = KeyPadPuzzle(engine)
        self.last_keypad = Interactable(self.player, self.engine, pg.FRect(44, 77, 5, 14))
        self.last_keypad_puzzle = KeyPadPuzzle(engine)
        self.last_keypad_puzzle.code = [1, 2, 3, 4]

        self.postit = Interactable(self.player, self.engine, pg.FRect(164, 88, 5, 5))
        self.postit_puzzle = PostItPuzzle(engine)

        self.storage_door = DoorInteractable(self.player, self.engine, (185, 76))

        self.transition = FadeTransition(True, 300, pg.Vector2(SCN_SIZE))
        self.next_state = AppState.EMPTY

    def handle_events(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = AppState.PAUSE
            self.engine.state_dict[self.engine.current_state].last_frame = (
                self.engine.screen.copy()
            )

    def render(self):
        if not pg.mixer.music.get_busy() and self.next_state == AppState.EMPTY:
            pg.mixer.music.load("assets/cockpit.mp3")
            pg.mixer.music.play(-1, fade_ms=500)

        self.engine.screen.fill("black")

        self.render_background()
        self._move_particles()

        if not self.keypad_puzzle.done:
            self.keypad.render()
        else:
            self.storage_door.update()
        
        if not self.last_keypad_puzzle.done:
            self.last_keypad.render()

        self.postit.render(not self.keypad.active)

        if self.keypad_puzzle.done and self.storage_door.event:
            self.transition.fade_in = False
            self.next_state = AppState.STORAGE
            pg.mixer.music.fadeout(700)

        self.player.update(self.keypad_puzzle.active or self.postit_puzzle.active)

        if self.keypad.event and not self.keypad_puzzle.done:
            self.keypad_puzzle.user_in = []
            self.keypad_puzzle.active = not self.keypad_puzzle.active
        self.keypad_puzzle.render()

        if self.postit.event:
            self.postit_puzzle.active = not self.postit_puzzle.active

        self.postit_puzzle.render()
        if self.last_keypad.event and not self.last_keypad_puzzle.done:
            self.last_keypad_puzzle.user_in = []
            self.last_keypad_puzzle.active = not self.last_keypad_puzzle.active
        self.last_keypad_puzzle.render()

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)
        if self.transition.event:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = self.next_state
            self.transition.fade_in = True
            self.next_state = AppState.EMPTY

    def render_extra_background_items(self, surface: pg.Surface, n: int):
        self._render_particles(surface, self.particle_colors[n])
        if self.keypad_puzzle.done:
            self.storage_door.render_layer(surface, n=n)

    def _render_particles(self, surface, color):
        for particle in self.particles:
            if surface.get_at((particle.x, particle.y)) == (0, 0, 0, 0):
                surface.set_at((particle.x, particle.y), color)

    def _move_particles(self):
        for p in self.particles:
            p.x += p.vel * self.engine.dt
            p.x %= 80
