import pygame as pg

from core.settings import *
from core.surfaces import import_anim
from core.enums import AnimState


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
        self.pos = pg.Vector2(self.engine.screen.width / 2, GROUND_HEIGHT)
        self.rect = self.frame.get_frect(midbottom=self.pos)
        self.anim_speed = 10
        self.left = False

        # kinematics
        self.x_dir = 0
        self.speed = 40

    def animate(self):
        if self.x_dir:
            self.anim_state = AnimState.WALK
            self.left = self.x_dir < 0
        else:
            self.anim_state = AnimState.IDLE

        self.current_frame += self.anim_speed * self.engine.dt
        self.current_frame %= len(self.animations[self.anim_state])

        self.frame = pg.transform.flip(
            self.animations[self.anim_state][int(self.current_frame)], self.left, False
        )
        self.rect = self.frame.get_frect(midbottom=self.pos)

    def draw(self):
        self.engine.screen.blit(self.frame, self.rect.move(-self.engine.camera))

    def update(self):
        keys = pg.key.get_pressed()
        self.x_dir = 0
        if keys[pg.K_a]:
            self.x_dir -= 1
        if keys[pg.K_d]:
            self.x_dir += 1

        self.animate()

        self.pos.x += self.x_dir * self.speed * self.engine.dt
        self.rect.midbottom = self.pos

        pos_from_mid = (WIN_WIDTH / 2) - self.pos.x

        self.draw()
