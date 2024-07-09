from typing import TYPE_CHECKING

import pygame as pg

from core.settings import WIN_HEIGHT, WIN_WIDTH
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
        self.hovering: bool = self.rect.collidepoint(pg.mouse.get_pos())
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
        shifted_pos = pos + (WIN_WIDTH / 2 - 40, WIN_HEIGHT / 2 - 32)
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

        self.engine.screen.blit(self.text, self.text_rect)


class TextButton(Button):
    def __init__(
        self, engine: "Engine", text: str, pos: pg.Vector2, size: pg.Vector2
    ) -> None:
        shifted_pos = pos + (95, 55)
        surf = pg.Surface(size, pg.SRCALPHA)
        super().__init__(engine, shifted_pos, surf)
        font = pg.font.SysFont("Arial", 8)

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
        shifted_pos = pos + (WIN_WIDTH / 2 - 36, WIN_HEIGHT / 2 - 24)
        self.surf_dict = surf_dict

        super().__init__(engine, shifted_pos, self.surf_dict["idle"])

        self.num = num

    def render(self, handle_states: bool = True):
        self.surface = (
            self.surf_dict["glow"] if self.hovering else self.surf_dict["idle"]
        )
        if self.holding:
            self.surface = self.surf_dict["pressed"]

        if handle_states:
            self.handle_states()
        self.engine.screen.blit(self.surface, self.rect)
