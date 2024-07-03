import pygame as pg


class CockPit:
    def __init__(self, engine) -> None:
        self.engine = engine

    def render(self):
        for tile in self.engine.all_tiles:
            tile.draw()
