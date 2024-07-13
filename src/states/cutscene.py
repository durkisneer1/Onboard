from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AppState
from core.settings import SCN_SIZE, WIN_SIZE
from core.transitions import FadeTransition
from src.states.base import BaseState
from core.surfaces import import_image

if TYPE_CHECKING:
    from main import Engine


class CutScene(BaseState):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)

        self.surf = import_image("assets/intro_cutscene.png")
        self.initial_slides = 3
        self.slides = self.initial_slides

        self.reset()

        self.transition = FadeTransition(True, 300, pg.Vector2(WIN_SIZE))

    def handle_events(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.next_state = AppState.MENU
            self.transition.fade_in = False

    def handle_slide(self):
        self.timer -= self.engine.dt
        if self.timer <= 0:
            if self.slides > 0:
                self.timer = 5
                self.scroll_dest.x -= WIN_SIZE[0]
                self.slides -= 1
            else:
                self.done = True
                self.next_state = AppState.COCKPIT
                self.transition.fade_in = False

        self.scroll.move_towards_ip(self.scroll_dest, 1500 * self.engine.dt)

    def reset(self) -> None:
        self.timer = 4
        self.slides = self.initial_slides
        self.scroll_dest = pg.Vector2()
        self.scroll = pg.Vector2()
        self.done = False

    def render(self):
        if not self.done:
            self.handle_slide()

        # Fill screen transparent during cutscenes so it doesnt overwrite display
        self.engine.screen.fill((0, 0, 0, 0))

        self.engine.display.blit(self.surf, self.scroll)

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.display)
        if self.transition.event:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = self.next_state
            self.transition.fade_in = True
            self.next_state = AppState.EMPTY
            self.reset()
