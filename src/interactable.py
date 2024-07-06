from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from main import Engine
    from src.player import Player


class Interactable:
    def __init__(self, player: "Player", engine: "Engine", rect: pg.Rect):
        self.player = player
        self.engine = engine
        self.rect = rect

        self.active = False
        self.event = False

    def render(self):
        self.handle_states()

        if self.active:
            pg.draw.rect(self.engine.screen, (232, 255, 117), self.rect, 1)

    def handle_states(self):
        self.active = self.player.rect.colliderect(self.rect)
        self.event = pg.key.get_just_pressed()[pg.K_e] and self.active
