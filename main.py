import pygame as pg

from core.enums import AppState
from src.player import Player
from src.states.cockpit import CockPit
from src.states.pause import Pause


class Engine:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((240, 135), pg.SCALED | pg.FULLSCREEN)
        pg.display.set_caption("The Astronaut")

        self.clock = pg.Clock()
        self.running = True
        self.dt = 0

        self.state_dict = {
            AppState.COCKPIT: CockPit(self),
            AppState.PAUSE: Pause(self, AppState.COCKPIT),
        }
        self.current_state = AppState.COCKPIT

    def run(self):
        while self.running:
            self.dt = self.clock.tick_busy_loop() / 1000

            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    self.running = False

            # self.screen.fill((30, 9, 13))
            self.state_dict[self.current_state].render()

            # if we want to switch the state
            if self.state_dict[self.current_state].next_state is not None:
                self.current_state = self.state_dict[self.current_state].next_state

            pg.display.flip()


if __name__ == "__main__":
    engine = Engine()
    engine.run()
