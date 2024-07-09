from typing import TYPE_CHECKING

import pygame as pg  # why

from core.settings import WIN_HEIGHT, WIN_WIDTH
from core.surfaces import import_image  # why

if TYPE_CHECKING:
    from main import Engine


class Picker:
    def __init__(
        self,
        engine: "Engine",
        pos: pg.Vector2,
        text: str,
        values: list[str],
        default: str,
    ) -> None:
        self.engine = engine
        self.pos = pos
        self.text = text
        self.values = values
        self.default = default
        font = pg.font.Font("assets/m5x7.ttf", 16)
        self.values_surfaces = list(
            map(lambda x: font.render(x, False, "white"), self.values)
        )
        self.text_surface = font.render(self.text, False, "white")

        self.index = self.values.index(self.default)

    def val(self) -> str:
        return self.values[self.index]

    def render(self):
        click: bool = pg.mouse.get_just_pressed()[0]
        rect = self.values_surfaces[self.index].get_rect()
        rect.top = self.pos.y
        rect.right = (
            WIN_WIDTH - self.pos.x - 20
        )  # the 20 is for the controls width actually no f*ck the controls
        hovering: bool = rect.collidepoint(pg.mouse.get_pos())
        holding: bool = pg.mouse.get_pressed()[0] and hovering
        event: bool = pg.mouse.get_just_released()[0] and hovering

        if event:
            self.index += 1
            self.index %= len(self.values)

        self.engine.screen.blit(self.text_surface, self.pos)
        if hovering:
            pg.draw.rect(self.engine.screen, [30, 30, 30], rect.inflate(10, 2), 0, 5)
        if holding:
            pg.draw.rect(self.engine.screen, [30, 100, 30], rect.inflate(10, 2), 0, 5)
        self.engine.screen.blit(self.values_surfaces[self.index], rect)
