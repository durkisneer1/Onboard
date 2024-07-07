from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AppState
from core.settings import *
from core.surfaces import import_image
from src.player import Player
from core.transitions import FadeTransition

if TYPE_CHECKING:
    from main import Engine


class StorageRoom:
    def __init__(self, engine: "Engine") -> None:
        self.engine = engine
        self.room_image = import_image("assets/storage.png", is_alpha=False)

        color_sets = [
            [
                # Grey
                (26, 12, 49),
                (53, 54, 88),
                (104, 107, 114),
                (136, 151, 185),
                (195, 205, 220),
                (255, 255, 255),
            ],
            [
                # Red
                (30, 9, 13),
                (114, 13, 13),
                (140, 49, 0),
                (238, 0, 14),
            ],
            [
                # Blue
                (0, 51, 58),
                (14, 50, 174),
                (0, 147, 226),
                (0, 237, 235),
            ],
        ]
        self.layers = [
            self._shift_colors(
                surface=self.room_image, color_sets=color_sets, n=2 - i
            )
            for i in range(3)
        ]

        self.player = Player(engine)

        self.transition = FadeTransition(True, 300, pg.Vector2(WIN_SIZE))

    @staticmethod
    def _shift_colors(
        surface: pg.Surface, color_sets: list[list[tuple[int, int, int]]], n: int
    ) -> pg.Surface:
        surface = surface.copy()
        array = pg.PixelArray(surface)
        for colors in color_sets:
            for old_color, new_color in zip(colors, [(0, 0, 0)] * n + colors):
                array.replace(old_color, new_color)

        return surface

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

        self.player.update(False)  # FIXME: Change when puzzle implemented

        self.transition.update(self.engine.dt)
        self.transition.draw(self.engine.screen)

        if self.transition.event:
            self.engine.last_state = self.engine.current_state
            self.engine.current_state = AppState.MENU
            self.transition.fade_in = True
