from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from main import Engine


class Tile:
    def __init__(self, engine: "Engine", pos: pg.Vector2, image: pg.Surface, name: str):
        self.engine = engine

        self.name = name
        self.image = image
        self.rect = image.get_frect(bottomleft=pos)

    def draw(self):
        self.engine.screen.blit(self.image, self.rect.move(-self.engine.camera))
