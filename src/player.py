import pygame as pg

from core.settings import *
from core.surfaces import import_anim
from core.enums import AnimState, Axis


class Player:
    def __init__(self, engine) -> None:
        self.engine = engine

        # animation
        self.animations = {
            AnimState.WALK: import_anim("assets/astrowalk.png", 21, 30),
            AnimState.IDLE: import_anim("assets/astroidle.png", 19, 30)
        }
        self.anim_state = AnimState.IDLE
        self.current_frame = 0
        self.frame = self.animations[AnimState.IDLE][0]
        self.rect = self.frame.get_frect(midbottom=(self.engine.screen.width / 2, GROUND_HEIGHT))
        self.anim_speed = 10

        # kinematics
        self.speed = 40
        self.vel = pg.Vector2()
        self.on_ground = True

    def animate(self):
        self.anim_state = AnimState.WALK if self.vel.x else AnimState.IDLE

        self.current_frame %= len(self.animations[self.anim_state])
        self.frame = pg.transform.flip(
            self.animations[self.anim_state][int(self.current_frame)], self.vel.x < 0, False
        )
        self.current_frame += self.anim_speed * self.engine.dt

    def draw(self):
        self.engine.screen.blit(self.frame, self.rect)

    def check_collisions(self, axis: Axis):
        for tile in self.engine.collision_tiles:
            if not self.rect.colliderect(tile.rect):
                continue

            if axis == Axis.X:
                if self.vel.x > 0:
                    self.rect.right = tile.rect.left
                elif self.vel.x < 0:
                    self.rect.left = tile.rect.right
            elif axis == Axis.Y:
                if self.vel.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.vel.y = 0

    def update(self):
        keys = pg.key.get_pressed()
        if self.on_ground:
            if keys[pg.K_SPACE] or keys[pg.K_UP]:
                self.vel.y = -64
                self.on_ground = False
        else:
            self.vel.y += GRAVITY * self.engine.dt

        direction = 0
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            direction -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            direction += 1
        self.vel.x = direction * self.speed

        self.rect.x += self.vel.x * self.engine.dt
        self.check_collisions(Axis.X)
        self.rect.y += self.vel.y * self.engine.dt
        self.check_collisions(Axis.Y)

        self.animate()
        self.draw()
