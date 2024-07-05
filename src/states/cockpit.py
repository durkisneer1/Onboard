import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame as pg
import pygame.surfarray

from core.enums import AppState
from core.settings import *
from core.surfaces import import_image
from core.transitions import FadeTransition
from src.player import Player

if TYPE_CHECKING:
    from main import Engine


@dataclass
class Particle:
    x: int
    y: int
    vel: float


class CockPit:
    def __init__(self, engine: "Engine") -> None:
        self.engine = engine
        cockpit_image = import_image("assets/cockpit.png")

        self.cockpit_image = pg.image.load("assets/cockpit.png").convert_alpha()

        self.particle_colors = [(26, 12, 49), (53, 54, 91), (104, 107, 114)]
        color_sets = [
            [
                (26, 12, 49),
                (53, 54, 91),
                (104, 107, 114),
                (136, 151, 185),
                (195, 205, 220),
                (255, 255, 255),
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

        self.transition = FadeTransition(True, 300, WIN_SIZE)

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

        self.player.update()

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)

        if self.transition.event:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = AppState.MENU
            self.transition.fade_in = True

    def _render_particles(self, surface, color):
        for particle in self.particles:
            if (self.cockpit_image.get_at((particle.x, particle.y)) == (0,)*4
                and surface.get_at((particle.x, particle.y)) == (0, 0, 0, 255)
            ):
                surface.set_at((particle.x, particle.y), color)

    def _move_particles(self):
        for particle in self.particles.copy():
            if particle.x > 80:
                self.particles.remove(particle)
                continue

            particle.x += particle.vel * self.engine.dt

        self.particle_timer += self.engine.dt
        if self.particle_timer > 0.5:
            self.particle_timer = 0

            self.particles.append(
                Particle(x=0, y=random.randint(13, 53), vel=random.randint(100, 200))
            )
