import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AppState
from core.room import Room
from core.settings import *
from core.transitions import FadeTransition
from src.interactable import Interactable
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

        self.keypad = Interactable(self.player, self.engine, pg.FRect(177, 77, 7, 9))
        self.keypad_puzzle = KeyPadPuzzle(engine)

        self.postit = Interactable(self.player, self.engine, pg.FRect(164, 81, 5, 5))
        self.postit_puzzle = PostItPuzzle(engine)

        self.storage_door = Interactable(
            self.player, self.engine, pg.FRect(203, 77, 5, 30)
        )

        self.transition = FadeTransition(True, 300, pg.Vector2(WIN_SIZE))
        self.next_state = AppState.EMPTY

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
            pg.mixer.music.load("assets/cockpit.mp3")
            pg.mixer.music.play(-1, fade_ms=500)

        self.engine.screen.fill("black")

        self.render_background()
        self._move_particles()

        if not self.keypad_puzzle.done:
            self.keypad.render()

        self.postit.render(not self.keypad.active)

        self.storage_door.render()
        if self.storage_door.event:
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

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)
        if self.transition.event:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = self.next_state
            self.transition.fade_in = True
            self.next_state = AppState.EMPTY

    def render_extra_background_items(self, surface: pg.Surface, n: int):
        self._render_particles(surface, self.particle_colors[n])

    def _render_particles(self, surface, color):
        for particle in self.particles:
            if self.room_image.get_at((particle.x, particle.y)) == (
                0,
            ) * 4 and surface.get_at((particle.x, particle.y)) == (0, 0, 0, 255):
                surface.set_at((particle.x, particle.y), color)

    def _move_particles(self):
        for p in self.particles:
            p.x += p.vel * self.engine.dt
            p.x %= 80
