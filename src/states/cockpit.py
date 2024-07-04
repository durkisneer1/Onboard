import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame as pg
import pygame.surfarray

from core.enums import AppState
from core.surfaces import import_image
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

        self.colors = [(26, 12, 49), (53, 54, 91), (104, 107, 114)]  # wall tile colors
        self.layers = [self._surface_mask_color(cockpit_image, i) for i in self.colors]

        self.particles: list[Particle] = []
        self.particle_timer = 0.0

        self.player = Player(engine)

    @staticmethod
    def _surface_mask_color(
        surface: pygame.Surface, color: tuple[int, int, int]
    ) -> pygame.Surface:
        surface.set_colorkey(color)
        array = pygame.surfarray.array_colorkey(surface)
        surface.set_colorkey(None)
        return pygame.surfarray.make_surface(array).convert()

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.engine.last_state = self.engine.current_state
                self.engine.current_state = AppState.PAUSE
                self.engine.state_dict[self.engine.current_state].last_frame = self.engine.screen.copy()

    def render(self):
        self.engine.screen.fill("black")
        # self._render_particles()

        # FIXME: Inefficient Surface Instantiation
        for n, layer in enumerate(self.layers):
            radius = 64 - 16 * (2 - n)
            for color in self.colors[0 : n + 1]:
                img = layer.copy()
                img.fill(color, special_flags=pg.BLEND_RGB_ADD)
                circle_surf = pg.Surface((radius * 2, radius * 2))
                circle_surf.fill("white")
                pg.draw.circle(circle_surf, "black", (radius, radius), radius)
                circle_surf.blit(
                    img,
                    (
                        -(self.player.rect.centerx - radius - 32),
                        -(self.player.rect.centery - radius - 27),
                    ),
                    special_flags=pg.BLEND_RGB_MAX,
                )

                circle_surf.set_colorkey("white", pg.RLEACCEL)
                pos = pg.Vector2(self.player.rect.center).elementwise() - radius
                self.engine.screen.blit(circle_surf, pos)
                radius -= 16

        self.player.update()

    def _render_particles(self):
        for particle in self.particles.copy():
            if particle.x > 110:
                self.particles.remove(particle)
                continue

            particle.x += particle.vel * self.engine.dt
            self.engine.screen.set_at((particle.x, particle.y), 0x353658)

        self.particle_timer += self.engine.dt
        if self.particle_timer > 0.5:
            self.particle_timer = 0
            self.particles.append(
                Particle(x=27, y=random.randint(45, 85), vel=random.randint(100, 200))
            )
