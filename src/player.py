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
            AnimState.IDLE: import_anim("assets/astroidle.png", 19, 30),
        }
        self.anim_state = AnimState.IDLE
        self.current_frame = 0
        self.frame = self.animations[AnimState.IDLE][0]
        self.anim_speed = 10

        # kinematics
        self.speed = 40
        self.vel = pg.Vector2()
        self.on_ground = True
        self.rect = self.frame.get_frect(
            midbottom=(self.engine.screen.width / 2, GROUND_HEIGHT)
        )

    # @staticmethod
    # def generate_shadow(anim_dict: dict[AnimState, list[pg.Surface]]) -> dict[AnimState, list[pg.Surface]]:
    #     shadow_dict = {}
    #     for key in anim_dict.keys():
    #         shadow_frames = []
    #         for frame in anim_dict[key]:
    #             shadow = frame.copy()
    #             shadow.fill("white", special_flags=pg.BLEND_RGB_SUB)
    #             shadow_frames.append(shadow)
    #         shadow_dict[key] = shadow_frames
    #     return shadow_dict

    def animate(self):
        self.anim_state = AnimState.WALK if self.vel.x else AnimState.IDLE

        self.current_frame %= len(self.animations[self.anim_state])
        self.frame = pg.transform.flip(
            self.animations[self.anim_state][int(self.current_frame)],
            self.vel.x < 0,
            False,
        )
        self.current_frame += self.anim_speed * self.engine.dt

    def draw(self):
        dark = self.frame.copy()
        dark.fill("white", special_flags=pg.BLEND_RGB_SUB)
        self.engine.screen.blit(dark, self.rect.move(3, 0))
        self.engine.screen.blit(self.frame, self.rect)

    def check_collisions(self, axis: Axis):
        pass

        if self.rect.bottom > GROUND_HEIGHT:
            self.rect.bottom = GROUND_HEIGHT
            self.on_ground = True

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
