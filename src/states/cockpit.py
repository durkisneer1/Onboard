import pygame as pg


class CockPit:
    def __init__(self, engine) -> None:
        self.engine = engine

    def render(self):
        for tile in self.engine.cockpit_tiles:
            tile.draw()
        for tile in self.engine.decor_tiles:
            tile.draw()
