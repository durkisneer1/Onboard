from typing import TYPE_CHECKING

import pygame as pg

from core.settings import SCN_SIZE
from core.surfaces import import_image

if TYPE_CHECKING:
    from main import Engine


class Button:
    def __init__(self, engine: "Engine", pos: pg.Vector2, surf: pg.Surface):
        self.engine = engine
        self.surface = surf
        self.pos = pos

        self.rect = self.surface.get_rect(topleft=pos)
        self.hovering = False
        self.holding = False
        self.event = False

    def render(self):
        # just some placeholders
        if self.holding:
            self.surface.fill((197, 205, 219))
        elif self.hovering:
            self.surface.fill((139, 151, 182))
        else:
            self.surface.fill((24, 13, 47))

        self.handle_states()
        self.engine.screen.blit(self.surface, self.rect)

    def handle_states(self):
        self.hovering: bool = self.rect.collidepoint(self.engine.mouse_pos)
        self.holding: bool = pg.mouse.get_pressed()[0] and self.hovering
        self.event: bool = pg.mouse.get_just_released()[0] and self.hovering


class NumButton(Button):
    def __init__(
        self,
        engine: "Engine",
        num: int,
        pos: pg.Vector2,
        surf_dict: dict[str, pg.Surface],
    ) -> None:
        shifted_pos = pos + (SCN_SIZE[0] / 2 - 40, SCN_SIZE[1] / 2 - 32)
        self.surf_dict = surf_dict
        super().__init__(engine, shifted_pos, surf_dict["idle"])
        font = pg.font.SysFont("Arial", 8)

        self.num = num
        self.rect = surf_dict["idle"].get_rect(topleft=shifted_pos)
        self.text = font.render(str(num), False, (24, 13, 47))
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def render(self):
        self.surface = (
            self.surf_dict["pressed"] if self.holding else self.surf_dict["idle"]
        )

        self.handle_states()
        self.engine.screen.blit(self.surface, self.rect)

        offset = 1 if self.holding else 0
        self.engine.screen.blit(self.text, self.text_rect.move(offset, offset))


class TextButton(Button):
    def __init__(
        self, engine: "Engine", text: str, pos: pg.Vector2, size: pg.Vector2
    ) -> None:
        shifted_pos = pos + (95, 55)
        surf = pg.Surface(size, pg.SRCALPHA)
        super().__init__(engine, shifted_pos, surf)
        font = pg.font.Font("assets/m5x7.ttf", 16)

        self.rect = surf.get_rect(topleft=shifted_pos)
        self.text_str = text
        self.text = font.render(text, False, (197, 205, 219))
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def render(self):
        color = (139, 151, 182) if self.hovering else (24, 13, 47)
        pg.draw.rect(self.surface, color, ((0, 0), self.surface.size), border_radius=4)

        self.handle_states()
        self.engine.screen.blit(self.surface, self.rect)

        self.engine.screen.blit(self.text, self.text_rect)


class SimonButton(Button):
    def __init__(
        self,
        engine: "Engine",
        num: int,
        pos: pg.Vector2,
        surf_dict: dict[str, pg.Surface],
    ) -> None:
        shifted_pos = pos + (SCN_SIZE[0] / 2 - 36, SCN_SIZE[1] / 2 - 24)
        self.surf_dict = surf_dict

        super().__init__(engine, shifted_pos, self.surf_dict["idle"])

        self.num = num
        self.glow = False

    def render(self, handle_states: bool = True):
        self.surface = (
            self.surf_dict["hover"] if self.hovering else self.surf_dict["idle"]
        )
        if self.holding:
            self.surface = self.surf_dict["pressed"]

        if self.glow:
            self.surface = self.surf_dict["glow"]

        if handle_states:
            self.handle_states()
        self.engine.screen.blit(self.surface, self.rect)


class MenuButton(Button):
    def __init__(
        self,
        engine: "Engine",
        text: str,
        pos: pg.Vector2,
        size: pg.Vector2,
        slide_offset: float,
    ) -> None:
        surf = pg.Surface(size, pg.SRCALPHA)
        super().__init__(engine, pos, surf)
        font = pg.font.Font("assets/m5x7.ttf", 16)

        self.rect = surf.get_frect(topleft=pos)
        self.text_str = text
        self.text = font.render(text, False, "white")
        self.text_rect = self.text.get_frect(center=self.rect.center)

        self.dest_x = self.rect.x

        self.scaled_surf = self.surface.copy()
        self.factor = 1

        self.slide_done = False
        self.slide_offset = slide_offset
        self.rect.x = -20 - self.slide_offset
        self.force = 250
        self.vel = pg.Vector2()

    def _handle_hover(self):
        if self.hovering:
            self.factor += self.engine.dt
        else:
            self.factor -= self.engine.dt

        self.factor = pg.math.clamp(self.factor, 1, 1.1)
        self.scaled_surf = pg.transform.scale_by(self.surface, self.factor)

    def _handle_interactions(self):
        self.handle_states()
        self._handle_hover()
        scaled_rect = self.scaled_surf.get_rect(center=self.rect.center)
        self.text_rect.center = self.rect.center
        self.engine.screen.blit(self.scaled_surf, scaled_rect)
        self.engine.screen.blit(self.text, self.text_rect)

    def _handle_slide(self):
        self.force -= 300 * self.engine.dt
        self.vel.x += self.force * self.engine.dt
        self.rect.x += self.vel.x * self.engine.dt
        self.text_rect.centerx = self.rect.centerx

        if self.rect.x >= self.dest_x:
            self.slide_done = True
            self.rect.x = self.dest_x
            self.text_rect.centerx = self.rect.centerx

        self.engine.screen.blit(self.surface, self.rect)
        self.engine.screen.blit(self.text, self.text_rect)

    def render(self):
        color = (193, 36, 88) if self.hovering else (24, 13, 47)
        pg.draw.rect(self.surface, color, ((0, 0), self.surface.size), border_radius=4)
        pg.draw.rect(
            self.surface,
            (249, 78, 109),
            ((0, 0), self.surface.size),
            border_radius=4,
            width=1,
        )

        if self.slide_done:
            self._handle_interactions()
        else:
            self._handle_slide()
