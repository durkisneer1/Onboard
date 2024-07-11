import pygame as pg

import core.surfaces as surfaces
from core.enums import AppState
from core.settings import *
from src.states.cockpit import CockPit
from src.states.cutscene import CutScene
from src.states.menu import Menu
from src.states.pause import Pause
from src.states.reactor import ReactorRoom
from src.states.settings_screen import SettingsMenu
from src.states.storage import StorageRoom

surfaces.surface_debug = False


class Engine:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(WIN_SIZE, pg.SCALED | pg.FULLSCREEN)
        pg.display.set_caption("The Astronaut")
        self.clock = pg.Clock()
        self.running = True
        self.dt = 0

        self.state_dict = {
            AppState.PAUSE: Pause(self),
            AppState.MENU: Menu(self),
            AppState.COCKPIT: CockPit(self),
            AppState.STORAGE: StorageRoom(self),
            AppState.REACTOR: ReactorRoom(self),
            AppState.SETTINGS: SettingsMenu(self),
            AppState.INTRO: CutScene(self),
        }
        self.current_state = AppState.MENU  # MENU is default
        # Needed for accesing the settings and then going back to the last state
        self.last_state = self.current_state

    def run(self):
        while self.running:
            self.dt = self.clock.tick_busy_loop(60) / 1000

            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    self.running = False
                self.state_dict[self.current_state].handle_events(ev)

            self.state_dict[self.current_state].render()

            pg.display.flip()


if __name__ == "__main__":
    engine = Engine()
    engine.run()
