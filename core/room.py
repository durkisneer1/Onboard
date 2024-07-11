from abc import ABC, abstractmethod
from os import listdir, path
from typing import TYPE_CHECKING

import pygame as pg

from core.settings import *
from core.surfaces import import_anim, import_image, shift_colors
from src.player import Player

if TYPE_CHECKING:
    from main import Engine


class Room:
    def __init__(self, engine: "Engine", room_image_path: str) -> None:
        self.engine = engine
        self.player = Player(engine)

        if path.isfile(room_image_path):
            self.room_image = import_image(room_image_path)
            self.layers = [
                shift_colors(surface=self.room_image, color_sets=COLOR_SETS, n=2 - i)
                for i in range(3)
            ]
        # elif path.isdir(room_image_path):
        #     self.room_frames = [import_image(image_path, is_alpha=False) for image_path in listdir(room_image_path)]
        #     self.layers = [
        #         shift_colors(surface=frame, color_sets=COLOR_SETS, n=2 - i)
        #         for i in range(3)
        #         for frame in self.room_frames
        #     ]

    @abstractmethod
    def render(self): ...

    def render_background(self):
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
            layer = layer.copy()
            self.render_extra_background_items(layer, n)
            surf.blit(layer, (0, 0), special_flags=pg.BLEND_RGB_ADD)
            surf.set_colorkey("white")
            self.engine.screen.blit(surf, (32, 27))
            radius -= 20

    def render_extra_background_items(self, surface: pg.Surface, n: int): ...
