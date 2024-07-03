import pygame as pg
from pytmx import load_pygame

from core.settings import *
from core.surfaces import load_tmx_layers
from core.enums import AppState
from src.player import Player
from src.states.cockpit import CockPit

class Engine:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((240, 135), pg.SCALED | pg.FULLSCREEN)
        pg.display.set_caption("The Astronaut")

        self.clock = pg.Clock()
        self.running = True
        self.dt = 0

        tile_set = load_pygame("assets/tilemap.tmx")
        self.collision_tiles = []
        self.all_tiles = []
        load_tmx_layers(self, tile_set, "Border", (self.collision_tiles, self.all_tiles))
        load_tmx_layers(self, tile_set, "Wall", self.all_tiles)
        load_tmx_layers(self, tile_set, "Decor", self.all_tiles)

        self.player = Player(self)
        self.state_dict = {
            AppState.COCKPIT: CockPit(self)
        }
        self.current_state = AppState.COCKPIT

    def run(self):
        while self.running:
            self.dt = self.clock.tick_busy_loop() / 1000

            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    self.running = False
                elif ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
                    self.running = False

            self.screen.fill((30, 9, 13))
            self.state_dict[self.current_state].render()
            self.player.update()

            pg.display.flip()


if __name__ == '__main__':
    engine = Engine()
    engine.run()
