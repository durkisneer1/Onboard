from typing import TYPE_CHECKING

import pygame as pg

from core.enums import AnimState
from core.settings import *
from core.surfaces import import_anim

if TYPE_CHECKING:
    from main import Engine


class Player:
    def __init__(self, engine: "Engine") -> None:
        self.engine = engine

        # animation
        self.animations = {
            AnimState.WALK: import_anim("assets/astrowalk.png", 21, 30),
            AnimState.IDLE: import_anim("assets/astroidle.png", 19, 30),
        }
        self.anim_state = AnimState.IDLE
        self.current_frame = 0
        self.frame = self.animations[AnimState.IDLE][0]
        self.anim_speed = 10
        self.left = False

        # kinematics
        self.speed = 40
        self.vel = pg.Vector2()
        self.rect = self.frame.get_frect(
            midbottom=(self.engine.screen.width / 2, GROUND_HEIGHT)
        )

    def animate(self, puzzle_active: bool):
        if self.vel.x and not puzzle_active:
            self.anim_state = AnimState.WALK
            self.left = self.vel.x < 0
        else:
            self.anim_state = AnimState.IDLE

        self.current_frame %= len(self.animations[self.anim_state])
        self.frame = pg.transform.flip(
            self.animations[self.anim_state][int(self.current_frame)],
            self.left,
            False,
        )
        self.current_frame += self.anim_speed * self.engine.dt

    def draw(self):
        dark = self.frame.copy()
        dark.fill("white", special_flags=pg.BLEND_RGB_SUB)
        self.engine.screen.blit(dark, self.rect.move(3, 0))
        self.engine.screen.blit(self.frame, self.rect)

    def move(self):
        keys = pg.key.get_pressed()

        direction = 0
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            direction -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            direction += 1
        self.vel.x = direction * self.speed

        self.rect.topleft += self.vel * self.engine.dt
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(self.rect.right, WIN_WIDTH)

    def update(self, puzzle_active: bool):
        if not puzzle_active:
            self.move()
        self.animate(puzzle_active)
        self.draw()
