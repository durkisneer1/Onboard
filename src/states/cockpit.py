import random
from typing import TYPE_CHECKING
import pygame as pg
from dataclasses import dataclass

if TYPE_CHECKING:
    from main import Engine


@dataclass
class Particle:
    x: int
    y: int
    vel: float


class CockPit:
    def __init__(self, engine) -> None:
        self.engine: "Engine" = engine

        self.cockpit_image = pg.image.load("assets/cockpit.png").convert_alpha()

        self.colors = [(26, 12, 49), (53, 54, 91), (104, 107, 114)]
        self.layers = [self._shift_colors(surface=self.cockpit_image, colors=self.colors, n=2-i) for i in range(3)]

        self.particles: list[Particle] = []
        self.particle_timer = 0.0

    @staticmethod
    def _shift_colors(surface: pg.Surface, colors: list[tuple[int, int, int]], n: int) -> pg.Surface:
        surface = surface.copy()
        array = pg.PixelArray(surface)
        for old_color, new_color in zip(colors, [(0, 0, 0)] * n + colors):
            array.replace(old_color, new_color)
        return surface

    # @staticmethod
    # def _surface_mask_color(surface: pygame.Surface, color: tuple[int, int, int]) -> pygame.Surface:
    #     surface.set_colorkey(color)
    #     array = pygame.surfarray.array_colorkey(surface)
    #     surface.set_colorkey(None)
    #     return pygame.surfarray.make_surface(array).convert()

    def render(self):
        self.engine.screen.fill("black")

        radius = 64
        for layer in self.layers:
            surf = pg.Surface(layer.size)
            surf.fill("black")
            pg.draw.circle(
                surf,
                "white",
                (int(self.engine.player.rect.centerx) - 32,
                 int(self.engine.player.rect.centery) - 27),
                radius
            )
            surf.blit(layer, (0, 0), special_flags=pg.BLEND_RGB_MULT)
            surf.set_colorkey("black")
            self.engine.screen.blit(surf, (32, 27))
            radius -= 16

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
                Particle(
                    x=27,
                    y=random.randint(45, 85),
                    vel=random.randint(100, 200)
                )
            )
