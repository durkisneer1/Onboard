from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from main import Engine


class Button:
    def __init__(self, engine: "Engine", pos: tuple[int], size: tuple[int]):
        self.engine = engine
        self.surface = pg.Surface(size)
        self.pos = pos

        self.rect = self.surface.get_rect(topleft=pos)
        self.hovering = False
        self.holding = False
        self.event = False

    def render(self):
        # just some placeholders
        if self.holding:
            self.surface.fill("white")
        elif self.hovering:
            self.surface.fill("darkgray")
        else:
            self.surface.fill("black")

        self.handle_movement()
        self.engine.screen.blit(self.surface, self.rect)

        if self.event:
            print("button event")

    def handle_movement(self):
        mouse_pos = pg.mouse.get_pos()
        self.hovering = False
        if self.rect.collidepoint(mouse_pos):
            self.hovering = True

        mouse_pressed = pg.mouse.get_pressed()
        self.holding = False
        if mouse_pressed[0] and self.hovering:
            self.holding = True

        mouse_released = pg.mouse.get_just_released()
        self.event = False
        if mouse_released[0] and self.hovering:
            self.event = True
