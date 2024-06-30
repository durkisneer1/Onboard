import pygame as pg

from src.player import Player

class Engine:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((240, 135), pg.SCALED | pg.FULLSCREEN)
        pg.display.set_caption("The Astronaut")

        self.clock = pg.Clock()
        self.running = True
        self.dt = 0

        self.player = Player(self)

    def run(self):
        while self.running:
            self.dt = self.clock.tick_busy_loop() / 1000

            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    self.running = False
                elif ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
                    self.running = False

            self.screen.fill("black")
            self.player.update()

            pg.display.flip()


if __name__ == '__main__':
    engine = Engine()
    engine.run()
