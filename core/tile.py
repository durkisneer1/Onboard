import pygame as pg


class Tile:
    def __init__(self, engine, pos: pg.Vector2, image: pg.Surface, name: str):
        self.engine = engine

        self.name = name
        self.image = image
        self.rect = image.get_frect(bottomleft=pos)

    def draw(self):
        self.engine.screen.blit(self.image, self.rect)
