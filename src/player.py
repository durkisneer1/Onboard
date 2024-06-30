from enum import IntEnum, auto

import pygame as pg

from core.surfaces import import_anim


class AnimState(IntEnum):
    WALK = auto()
    IDLE = auto()


class Player:
    def __init__(self, engine) -> None:
        self.engine = engine

        # animation
        self.animations = {
            AnimState.WALK: import_anim("assets/astrowalk.png", 21, 29),
            AnimState.IDLE: import_anim("assets/astroidle.png", 19, 30)
        }
        self.anim_state = AnimState.IDLE
        self.current_frame = 0
        self.frame = self.animations[AnimState.IDLE][0]
        self.rect = self.frame.get_frect(center=(self.engine.screen.width / 2, self.engine.screen.height / 2))
        self.anim_speed = 8
        self.left = False

        # kinematics
        self.direction = pg.Vector2()
        self.speed = 100

    def animate(self):
        if self.direction.x:
            self.anim_state = AnimState.WALK
            self.left = self.direction.x < 0
        else:
            self.anim_state = AnimState.IDLE

        self.current_frame += self.anim_speed * self.engine.dt
        self.current_frame %= len(self.animations[self.anim_state])

        self.frame = pg.transform.flip(
            self.animations[self.anim_state][int(self.current_frame)], self.left, False
        )

    def draw(self):
        self.engine.screen.blit(self.frame, self.rect)

    def update(self):
        keys = pg.key.get_pressed()
        self.direction = pg.Vector2()
        if keys[pg.K_a]:
            self.direction.x -= 1
        if keys[pg.K_d]:
            self.direction.x += 1

        self.rect.topleft += self.direction * self.speed * self.engine.dt

        self.animate()
        self.draw()
