import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame as pg
import pygame.surfarray

from core.enums import AppState
from core.settings import *
from core.surfaces import import_image, shift_colors
from core.transitions import FadeTransition
from src.interactable import Interactable
from src.player import Player
from src.puzzles.keypad import KeyPadPuzzle

if TYPE_CHECKING:
    from main import Engine


@dataclass
class Particle:
    x: float
    y: float
    vel: float


class CockPit:
    particle_colors = [(26, 12, 49), (53, 54, 88), (104, 107, 114)]

    def __init__(self, engine: "Engine") -> None:
        self.engine = engine
        self.cockpit_image = import_image("assets/cockpit.png")

        self.layers = [
            shift_colors(surface=self.cockpit_image, color_sets=COLOR_SETS, n=2 - i)
            for i in range(3)
        ]

        self.particles = [
            Particle(x=0, y=random.randint(13, 53), vel=random.randint(100, 200))
            for _ in range(6)
        ]

        self.player = Player(engine)

        keypad_rect = pg.FRect(177, 77, 7, 9)
        self.keypad = Interactable(self.player, self.engine, keypad_rect)
        self.keypad_puzzle = KeyPadPuzzle(engine)

        self.transition = FadeTransition(True, 300, pg.Vector2(WIN_SIZE))

        pg.mixer_music.load("assets/cockpit.mp3")
        # pg.mixer_music.play()

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

        radius = 74
        for n, layer in enumerate(self.layers):
            surf = pg.Surface(layer.size)
            surf.fill("white")
            pg.draw.circle(
                surf,
                "black",
                (
                    self.player.rect.centerx - 32,
                    self.player.rect.centery - 27,
                ),
                radius,
            )
            self._render_particles(surf, self.particle_colors[n])
            surf.blit(layer, (0, 0), special_flags=pg.BLEND_RGB_ADD)
            surf.set_colorkey("white")
            self.engine.screen.blit(surf, (32, 27))
            radius -= 20

        self._move_particles()

        if not self.keypad_puzzle.done:
            self.keypad.render()

        self.player.update(self.keypad_puzzle.active)

        if self.keypad.event and not self.keypad_puzzle.done:
            self.keypad_puzzle.user_in = []
            self.keypad_puzzle.active = not self.keypad_puzzle.active
        self.keypad_puzzle.render()

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)
        if self.transition.event:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = AppState.MENU
            self.transition.fade_in = True

    def _render_particles(self, surface, color):
        for particle in self.particles:
            if self.cockpit_image.get_at((particle.x, particle.y)) == (
                0,
            ) * 4 and surface.get_at((particle.x, particle.y)) == (0, 0, 0, 255):
                surface.set_at((particle.x, particle.y), color)

    def _move_particles(self):
        for p in self.particles:
            p.x += p.vel * self.engine.dt
            p.x %= 80
