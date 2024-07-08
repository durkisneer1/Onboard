from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AppState
from core.settings import *
from core.surfaces import import_image, shift_colors
from core.transitions import FadeTransition
from src.interactable import Interactable
from src.player import Player
from src.puzzles.simon import SimonSaysPuzzle

if TYPE_CHECKING:
    from main import Engine


class StorageRoom:
    def __init__(self, engine: "Engine") -> None:
        self.engine = engine
        self.room_image = import_image("assets/storage.png", is_alpha=False)

        self.layers = [
            shift_colors(surface=self.room_image, color_sets=COLOR_SETS, n=2 - i)
            for i in range(3)
        ]

        self.player = Player(engine)

        simon_rect = pg.FRect(108, 81, 15, 15)
        self.simon = Interactable(self.player, self.engine, simon_rect)
        self.simon_puzzle = SimonSaysPuzzle(self.engine)

        self.transition = FadeTransition(True, 300, pg.Vector2(WIN_SIZE))

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.engine.last_state = self.engine.current_state
                self.engine.current_state = AppState.PAUSE
                self.engine.state_dict[
                    self.engine.current_state
                ].last_frame = self.engine.screen.copy()

    def render(self):
        self.engine.screen.fill("black")

        radius = 74
        for n, layer in enumerate(self.layers):
            surf = pg.Surface(layer.size)
            surf.fill("white")
            pg.draw.circle(
                surf,
                "black",
                (
                    self.player.rect.centerx - 32,
                    self.player.rect.centery - 27,
                ),
                radius,
            )
            surf.blit(layer, (0, 0), special_flags=pg.BLEND_RGB_ADD)
            surf.set_colorkey("white")
            self.engine.screen.blit(surf, (32, 27))
            radius -= 20

        if not self.simon_puzzle.done:
            self.simon.render()

        self.player.update(self.simon_puzzle.active)

        if self.simon.event and not self.simon_puzzle.done:
            self.simon_puzzle.reset()
            self.simon_puzzle.active = not self.simon_puzzle.active
        self.simon_puzzle.render()

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)

        if self.transition.event:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = AppState.MENU
            self.transition.fade_in = True
