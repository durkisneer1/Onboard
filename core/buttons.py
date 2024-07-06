from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from main import Engine


class Button:
    def __init__(self, engine: "Engine", pos: pg.Vector2, size: pg.Vector2):
        self.engine = engine
        self.surface = pg.Surface(size)
        self.pos = pos

        self.rect = self.surface.get_rect(topleft=pos)
        self.hovering = False
        self.holding = False
        self.event = False

    def render(self):
        # just some placeholders
        if self.holding:
            self.surface.fill("white")
        elif self.hovering:
            self.surface.fill("darkgray")
        else:
            self.surface.fill((25, 25, 25))

        self.handle_states()
        self.engine.screen.blit(self.surface, self.rect)

    def handle_states(self):
        self.hovering: bool = self.rect.collidepoint(pg.mouse.get_pos())
        self.holding: bool = pg.mouse.get_pressed()[0] and self.hovering
        self.event: bool = pg.mouse.get_just_released()[0] and self.hovering


class NumButton(Button):
    def __init__(
        self, engine: "Engine", num: int, pos: pg.Vector2, size: pg.Vector2
    ) -> None:
        shifted_pos = pos + (95, 55)
        super().__init__(engine, shifted_pos, size)
        font = pg.font.SysFont("Arial", 8)

        self.num = num
        self.rect = pg.Rect(shifted_pos, size)
        self.text = font.render(str(num), False, "white")
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def render(self):
        super().render()
        self.engine.screen.blit(self.text, self.text_rect)
