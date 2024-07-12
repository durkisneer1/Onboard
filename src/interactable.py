from typing import TYPE_CHECKING

import pygame as pg

from core.settings import COLOR_SETS, ROOM_TOPLEFT
from core.surfaces import import_anim, import_image, shift_colors

if TYPE_CHECKING:
    from main import Engine
    from src.player import Player


class Interactable:
    def __init__(self, player: "Player", engine: "Engine", rect: pg.FRect):
        self.player = player
        self.engine = engine
        self.rect = rect

        self.active = False
        self.event = False
        self.popup = InteractablePopUp(player, engine, self)

    def render(self, handle_states: bool = True):
        self.handle_states(handle_states)

        self.popup.render()

        if self.active:
            pg.draw.rect(self.engine.screen, (232, 255, 117), self.rect, 1)

    def handle_states(self, active: bool = True):
        self.active = self.player.rect.colliderect(self.rect) if active else False
        self.event = pg.key.get_just_pressed()[pg.K_e] and self.active


class InteractablePopUp:
    def __init__(
        self, player: "Player", engine: "Engine", interactable: "Interactable"
    ):
        self.player = player
        self.engine = engine
        self.interactable = interactable

        self.popup_image = import_image("assets/popup1.png")
        self.rect = self.popup_image.get_rect(
            midbottom=interactable.rect.midtop - pg.Vector2(0, 1)
        )

        self.current_pos = pg.Vector2(0, self.rect.height)
        self.force = 1.5

        # to avoid visual bugs
        self.last_frame_pos = self.current_pos
        self.surface = pg.Surface(self.rect.size, pg.SRCALPHA)

        self.active = False
        self.animation_done = False

    def handle_fading(self):
        dy = 30 * self.force * self.engine.dt
        self.current_pos.y += -dy if self.active else dy

        self.current_pos.y = max(0, self.current_pos.y)
        self.current_pos.y = min(self.rect.height + 1, self.current_pos.y)

        self.animation_done = self.last_frame_pos == self.current_pos
        if not self.animation_done:
            self.surface = pg.Surface(self.rect.size, pg.SRCALPHA)
            self.force += self.force * self.engine.dt
        else:
            self.force = 1.5

        self.last_frame_pos = self.current_pos.copy()

        # we can just turn self.current_pos.y into an alpha value
        self.surface.set_alpha(int(255 - self.current_pos.y * 19))

        self.surface.blit(self.popup_image, self.current_pos)

    def render(self):
        self.active = self.interactable.active

        self.handle_fading()

        self.engine.screen.blit(self.surface, self.rect)


class DoorInteractable:
    def __init__(self, player: "Player", engine: "Engine", pos: tuple[int, int]):
        self.player = player
        self.engine = engine

        self.anim = import_anim("assets/door.png", 22, 32)
        self.rect = self.anim[0].get_frect(topleft=pos)

        self.current_frame = 0

        self.active = False
        self.event = False

        self.interactable = Interactable(player, engine, self.rect.inflate(1, 1))

    def update(self):
        if self.active:
            self.current_frame += 16 * self.engine.dt
        else:
            self.current_frame -= 16 * self.engine.dt

        self.current_frame = pg.math.clamp(self.current_frame, 0, len(self.anim) - 1)

        self.interactable.render()

        self.active = self.interactable.active
        self.event = self.interactable.event

    def render_layer(self, destination: pg.Surface, n: int = 0):
        if self.current_frame != 0:
            surf = self.anim[int(self.current_frame)]
            new_surf = shift_colors(surface=surf, color_sets=COLOR_SETS, n=2 - n)
            destination.blit(
                new_surf, (self.rect.x - ROOM_TOPLEFT[0], self.rect.y - ROOM_TOPLEFT[1])
            )
