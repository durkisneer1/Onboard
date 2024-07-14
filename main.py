import pygame as pg

import core.surfaces as surfaces
from core.enums import AppState
from core.settings import FACTOR, SCN_SIZE, WIN_SIZE
from src.states.cockpit import CockPit
from src.states.credits import Credits
from src.states.cutscene import CutScene
from src.states.menu import Menu
from src.states.pause import Pause
from src.states.reactor import ReactorRoom
from src.states.settings_screen import SettingsMenu
from src.states.splash_screen import SplashScreen
from src.states.storage import StorageRoom
from src.diary import Diary

surfaces.surface_debug = False


class Engine:
    def __init__(self) -> None:
        pg.init()
        self.display = pg.display.set_mode(WIN_SIZE, pg.FULLSCREEN)
        self.screen = pg.Surface(SCN_SIZE, pg.SRCALPHA)
        pg.display.set_caption("The Astronaut")
        self.clock = pg.Clock()
        self.running = True
        self.dt = 0
        self.mouse_pos = pg.Vector2()

        self.px_font = pg.Font("assets/m5x7.ttf", 16)

        self.sfx = {
            "boop": pg.mixer.Sound("assets/boop.mp3"),
            "success": pg.mixer.Sound("assets/success.mp3"),
            "failure": pg.mixer.Sound("assets/failure.mp3"),
            "cut": pg.mixer.Sound("assets/cut.mp3"),
            "door open": pg.mixer.Sound("assets/door open.mp3"),
            "door close": pg.mixer.Sound("assets/door close.mp3"),
        }

        self.state_dict = {
            AppState.PAUSE: Pause(self),
            AppState.MENU: Menu(self),
            AppState.COCKPIT: CockPit(self),
            AppState.STORAGE: StorageRoom(self),
            AppState.REACTOR: ReactorRoom(self),
            AppState.SETTINGS: SettingsMenu(self),
            AppState.INTRO: CutScene(self),
            AppState.SPLASH: SplashScreen(self),
            AppState.CREDITS: Credits(self),
        }
        self.current_state = AppState.MENU  # MENU is default

        # Needed for accesing the settings and then going back to the last state
        self.last_state = AppState.INTRO

        self.diary = Diary(self)

        # pg.mixer.music.set_volume(0)
        # for sfx in self.sfx.values():
        #     sfx.set_volume(0)

    def run(self):
        while self.running:
            self.dt = self.clock.tick_busy_loop(30) / 1000
            self.mouse_pos = pg.Vector2(pg.mouse.get_pos()) / FACTOR

            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    self.running = False
                self.state_dict[self.current_state].handle_events(ev)

            self.state_dict[self.current_state].render()

            scaled_screen = pg.transform.scale_by(self.screen, FACTOR)
            self.display.blit(scaled_screen, (0, 0))

            pg.display.flip()


if __name__ == "__main__":
    engine = Engine()
    engine.run()
