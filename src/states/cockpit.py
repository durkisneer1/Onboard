import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame as pg
import pygame.surfarray

from core.buttons import NumButton
from core.enums import AppState
from core.settings import *
from core.surfaces import import_image
from core.transitions import FadeTransition
from src.interactable import Interactable
from src.player import Player

if TYPE_CHECKING:
    from main import Engine


@dataclass
class Particle:
    x: float
    y: float
    vel: float


class CockPit:
    def __init__(self, engine: "Engine") -> None:
        self.engine = engine
        self.cockpit_image = pg.image.load("assets/cockpit.png").convert_alpha()

        self.particle_colors = [(26, 12, 49), (53, 54, 88), (104, 107, 114)]
        color_sets = [
            [
                # Grey
                (26, 12, 49),
                (53, 54, 88),
                (104, 107, 114),
                (136, 151, 185),
                (195, 205, 220),
                (255, 255, 255),
            ],
            [
                # Red
                (30, 9, 13),
                (114, 13, 13),
                (140, 49, 0),
                (238, 0, 14)
            ],
            [
                # Blue
                (0, 51, 58),
                (14, 50, 174),
                (0, 147, 226),
                (0, 237, 235)
            ]
        ]
        self.layers = [
            self._shift_colors(
                surface=self.cockpit_image, color_sets=color_sets, n=2 - i
            )
            for i in range(3)
        ]

        self.particles: list[Particle] = []
        self.particle_timer = 0.0

        self.player = Player(engine)

        keypad_rect = pg.Rect(177, 77, 7, 9)
        self.keypad = Interactable(self.player, self.engine, keypad_rect)
        self.keypad_puzzle = KeyPadPuzzle(engine)

        self.transition = FadeTransition(True, 300, pg.Vector2(WIN_SIZE))

    @staticmethod
    def _shift_colors(
            surface: pg.Surface, color_sets: list[list[tuple[int, int, int]]], n: int
    ) -> pg.Surface:
        surface = surface.copy()
        array = pg.PixelArray(surface)
        for colors in color_sets:
            for old_color, new_color in zip(colors, [(0, 0, 0)] * n + colors):
                array.replace(old_color, new_color)

        return surface

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.engine.last_state = self.engine.current_state
                self.engine.current_state = AppState.PAUSE
                self.engine.state_dict[
                    self.engine.current_state
                ].last_frame = self.engine.screen.copy()
            elif event.key == pg.K_RETURN:
                self.transition.fade_in = False

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
                    int(self.player.rect.centerx) - 32,
                    int(self.player.rect.centery) - 27,
                ),
                radius,
            )
            self._render_particles(surf, self.particle_colors[n])
            surf.blit(layer, (0, 0), special_flags=pg.BLEND_RGB_ADD)
            surf.set_colorkey("white")
            self.engine.screen.blit(surf, (32, 27))
            radius -= 20

        self._move_particles()

        self.keypad.render()

        self.player.update(self.keypad_puzzle.active)

        if self.keypad.event:
            self.keypad_puzzle.keypad.user_in = []
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
        self.particles = [p for p in self.particles if p.x <= 80]
        for p in self.particles:
            p.x += p.vel * self.engine.dt

        self.particle_timer += self.engine.dt
        if self.particle_timer > 0.5:
            self.particle_timer = 0

            self.particles.append(
                Particle(x=0, y=random.randint(13, 53), vel=random.randint(100, 200))
            )


class KeyPadPuzzle:
    def __init__(self, engine: "Engine"):
        self.engine = engine
        self.keypad = KeyPad(engine)

        self.bg_dimmer = pg.Surface(WIN_SIZE)
        self.bg_dimmer.set_alpha(180)

        self.active = False

    def render(self) -> None:
        if not self.active:
            return

        self.engine.screen.blit(self.bg_dimmer, (0, 0))

        keys = pg.key.get_just_pressed()

        self.keypad.render()


class KeyPad:
    def __init__(self, engine: "Engine") -> None:
        self.engine = engine
        self.buttons = [
            NumButton(engine, 3 * y + x, pg.Vector2(x, y) * 10, pg.Vector2(10, 10))
            for x in range(1, 4)
            for y in range(0, 3)
        ]

        self.code = [1, 2, 3, 4]
        self.user_in = []

    def render(self):
        for button in self.buttons:
            button.render()
            if not button.event:
                continue

            self.user_in.append(button.num)
            if len(self.user_in) != len(self.code):
                continue

        if self.user_in == self.code:
            print("correct!")
