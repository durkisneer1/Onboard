from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AppState
from core.settings import SCN_SIZE
from core.transitions import FadeTransition
from src.states.base import BaseState

if TYPE_CHECKING:
    from main import Engine


class CutScene(BaseState):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)

        self.surf = pg.Surface((SCN_SIZE[0] * 2, SCN_SIZE[1]))
        pg.draw.rect(self.surf, "gray", ((0, 0), SCN_SIZE))
        pg.draw.rect(self.surf, "white", ((SCN_SIZE[0], 0), SCN_SIZE))

        self.reset()

        self.transition = FadeTransition(True, 300, pg.Vector2(SCN_SIZE))

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next_state = AppState.MENU
                self.transition.fade_in = False

    def handle_slide(self):
        self.timer -= self.engine.dt
        if self.timer <= 0:
            if self.scroll_dest.x > -self.surf.width:
                self.timer = 3
                self.scroll_dest.x -= SCN_SIZE[0]
            else:
                self.done = True
                self.next_state = AppState.COCKPIT
                self.transition.fade_in = False

        self.scroll.move_towards_ip(self.scroll_dest, 300 * self.engine.dt)

    def reset(self) -> None:
        self.timer = 3
        self.scroll_dest = pg.Vector2()
        self.scroll = pg.Vector2()
        self.done = False

    def render(self):
        if not self.done:
            self.handle_slide()
        self.engine.screen.blit(self.surf, self.scroll)

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)
        if self.transition.event:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = self.next_state
            self.transition.fade_in = True
            self.next_state = AppState.EMPTY
            self.reset()
